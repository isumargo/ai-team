"""Tes untuk proyek distribusi roko.

Fokus: jalur yang dipakai sales tiap hari lewat Telegram —
parser → commands → DB, plus keamanan webhook.
Panggilan AI (LLM) dimock supaya tes tidak bergantung jaringan/kuota.
"""

import json
from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse
from django.conf import settings

from . import commands, parser
from .models import Product, Reseller, StockMovement, Transaction


class ParserTests(TestCase):
    """Format pesan sales → perintah terstruktur."""

    def test_jual_dengan_harga(self):
        hasil = parser.parse_message("JUAL Madju Pro 100 bks ke Rudi 8500")
        self.assertEqual(hasil["action"], "JUAL")
        self.assertEqual(hasil["product"], "Madju Pro")
        self.assertEqual(hasil["qty"], 100)
        self.assertEqual(hasil["reseller"], "ke Rudi")
        self.assertEqual(hasil["price"], 8500)

    def test_jual_tanpa_harga(self):
        hasil = parser.parse_message("jual Madju Pro 50 bks Rudi")
        self.assertEqual(hasil["action"], "JUAL")
        self.assertEqual(hasil["qty"], 50)
        self.assertIsNone(hasil["price"])

    def test_stok_tanpa_produk(self):
        self.assertEqual(parser.parse_message("STOK")["action"], "STOK")
        self.assertIsNone(parser.parse_message("STOK")["product"])

    def test_stok_dengan_produk(self):
        hasil = parser.parse_message("stok Madju Pro")
        self.assertEqual(hasil["action"], "STOK")
        self.assertEqual(hasil["product"], "Madju Pro")

    def test_piutang(self):
        self.assertEqual(parser.parse_message("PIUTANG")["action"], "PIUTANG")
        self.assertEqual(parser.parse_message("piutang Budi")["reseller"], "Budi")

    def test_contoh_dan_retur(self):
        self.assertEqual(parser.parse_message("CONTOH Madju Pro 5 bks Budi")["action"], "CONTOH")
        self.assertEqual(parser.parse_message("RETUR Madju Pro 5 bks Budi")["action"], "RETUR")

    def test_pesan_bebas_gagal_diparse(self):
        self.assertIn("error", parser.parse_message("halo dasiyah, gimana stok?"))


class CommandsTests(TestCase):
    """Perintah terstruktur → efek nyata di database."""

    def setUp(self):
        self.produk = Product.objects.create(
            name="Madju Pro", sku="MP-12", price_buy=7600, price_sell=8600, stock=500
        )
        self.reseller = Reseller.objects.create(name="Budi Santoso", credit=0)

    def test_penjualan_memperbarui_stok_transaksi_dan_piutang(self):
        balasan = commands.process_sales("Madju Pro", 100, "Budi Santoso")

        self.assertIn("✅", balasan)
        self.produk.refresh_from_db()
        self.reseller.refresh_from_db()

        self.assertEqual(self.produk.stock, 400)
        self.assertEqual(self.reseller.credit, 860000)
        self.assertEqual(Transaction.objects.count(), 1)
        self.assertEqual(StockMovement.objects.filter(movement_type="out").count(), 1)

    def test_penjualan_tidak_kena_harga_tetap(self):
        commands.process_sales("Madju Pro", 10, "Budi Santoso", price=8000)
        transaksi = Transaction.objects.get()
        self.assertEqual(transaksi.price_per_unit, 8000)
        self.assertEqual(transaksi.total, 80000)

    def test_penjualan_ditolak_kalau_stok_kurang(self):
        balasan = commands.process_sales("Madju Pro", 9999, "Budi Santoso")
        self.assertIn("❌", balasan)
        self.assertEqual(Transaction.objects.count(), 0)
        self.produk.refresh_from_db()
        self.assertEqual(self.produk.stock, 500)

    def test_produk_tidak_ditemukan(self):
        balasan = commands.process_sales("Produk Hantu", 1, "Budi Santoso")
        self.assertIn("tidak ditemukan", balasan)
        self.assertEqual(Transaction.objects.count(), 0)

    def test_reseller_tidak_ditemukan(self):
        balasan = commands.process_sales("Madju Pro", 1, "Siapa Saya")
        self.assertIn("tidak ditemukan", balasan)
        self.assertEqual(Transaction.objects.count(), 0)

    def test_sample_kurangi_stok_tanpa_piutang(self):
        balasan = commands.process_sample("Madju Pro", 5, "Budi Santoso")
        self.assertIn("✅", balasan)
        self.produk.refresh_from_db()
        self.reseller.refresh_from_db()
        self.assertEqual(self.produk.stock, 495)
        self.assertEqual(self.reseller.credit, 0)

    def test_retur_tambah_stok(self):
        commands.process_return("Madju Pro", 5, "Budi Santoso")
        self.produk.refresh_from_db()
        self.assertEqual(self.produk.stock, 505)

    def test_cek_stok(self):
        balasan = commands.get_stock()
        self.assertIn("Madju Pro", balasan)
        self.assertIn("500", balasan)

    def test_cek_stok_satu_produk(self):
        balasan = commands.get_stock("Madju Pro")
        self.assertIn("Madju Pro", balasan)
        self.assertIn("500", balasan)

    def test_cek_piutang(self):
        commands.process_sales("Madju Pro", 10, "Budi Santoso")
        balasan = commands.get_receivables()
        self.assertIn("Budi Santoso", balasan)
        self.assertIn("86.000", balasan)


class WebhookTests(TestCase):
    """Endpoint Telegram: keamanan + routing parser-vs-AI."""

    def setUp(self):
        self.produk = Product.objects.create(
            name="Madju Pro", sku="MP-12", price_buy=7600, price_sell=8600, stock=500
        )
        self.reseller = Reseller.objects.create(name="Budi Santoso", credit=0)
        self.token = settings.TELEGRAM_BOT_TOKEN

    def _url(self, token):
        return f"/webhook/{token}/"

    def test_token_salah_ditolak(self):
        response = self.client.post(
            self._url("token-ngawur"), data=json.dumps({"message": {}}), content_type="application/json"
        )
        self.assertEqual(response.status_code, 401)

    def test_perintah_stok_tidak_pakai_ai(self):
        with patch("distribusi.views.send_telegram_message") as kirim:
            response = self.client.post(
                self._url(self.token),
                data=json.dumps({"message": {"chat": {"id": 1}, "text": "STOK"}}),
                content_type="application/json",
            )
        self.assertEqual(response.status_code, 200)
        kirim.assert_called_once()
        self.assertIn("Madju Pro", kirim.call_args[0][1])

    def test_perintah_jual_masuk_database(self):
        with patch("distribusi.views.send_telegram_message"):
            self.client.post(
                self._url(self.token),
                data=json.dumps(
                    {"message": {"chat": {"id": 1}, "text": "JUAL Madju Pro 100 bks Budi Santoso"}}
                ),
                content_type="application/json",
            )
        self.assertEqual(Transaction.objects.count(), 1)
        self.produk.refresh_from_db()
        self.assertEqual(self.produk.stock, 400)

    def test_pesan_bebas_diarahkan_ke_ai(self):
        with patch("distribusi.views.send_telegram_message") as kirim, \
             patch("distribusi.views.DasiyahAgent") as agen:
            agen.return_value.process_message.return_value = "Halo Mas!"
            self.client.post(
                self._url(self.token),
                data=json.dumps(
                    {"message": {"chat": {"id": 1}, "text": "halo dasiyah"}}
                ),
                content_type="application/json",
            )
        agen.return_value.process_message.assert_called_once()
        kirim.assert_called_once()
        self.assertEqual(kirim.call_args[0][1], "Halo Mas!")

    def test_json_rusak_ditolak(self):
        response = self.client.post(
            self._url(self.token), data="bukan json", content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)

    def test_get_tidak_diterima(self):
        response = self.client.get(self._url(self.token))
        self.assertEqual(response.status_code, 405)
