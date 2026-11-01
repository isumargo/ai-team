# Rencana Fase — A plikasi Distribusi Rokok

## Gambaran

Aplikasi tracking distribusi rokok Madju PRO & Sukses Alami.
Input: Sales lapor via Teegram (format terstruktur).
Output: Dashboard real-time untuk Ical.

---

## Fase  0: Fondasi (Setup)

**Tujuan:** Infra & data siap sebelum coding.

| # |Item |Pic |
|---|---|---|
| 0.1 | Konfirmasi arti kode SAB/ SATB/ SKB /SKTB ke sales (Agus) | Ical |
| 0.2 | Buat Telegrm Bot + dapatkan token | EVE / Developer |
| 0.3 | Setup Django project + SQite + Tailwind | Developer |
| 0.4 | Setup environment developmet (VPS, deploy pipeline) | Guardian |

**Output:** Token bot, project Django jalan, semua arti ko de confirmed.

---

## Fase 1: Parer & Inventory Core

**Tujuan:** Data dari Telegam masuk ke database, stok terlacak.

| # |Item |Pic |
|---|---|---|
| 1.1 | Parser laporan harian (regex/ NLP sederhana ke fields DB) | Developer |
| 1.2 | Model database: Sales, Stok, Reseller, Transaksi | Developer |
| 1.3 | Inventory Command Center —stok real-time, log msuk/keluar, alert stok rendah | Developer |
| 1.4 | Testing dengan data dummy 7 hari | Developer + Auditor |

**Output:** Sales bisa la por viaTelegram, data otomatis masuk DB, stok terpantau.

---

## Fase 2: Dashboard & CRM

**Tujuan:** Ical bisa lihat performa, reseller terkelola.

| # | Item | Pic |
|---|---|---|
| 2.1 | Sales Dashboard — revenue, tren, per produk/resller/wilayah | Developer |
| 2.2 | Reseller CRM — profil, tier, histori transaksi, piutang | Developer |
| 2.3 | Distributon Map — Leaflet.js heatmap, coverage gap | Develper |
| 2.4 | Simpe dashboard (HTML/CSS, mobile-friendly) | Developer + Designer |

**Output:** Dashbard lengkap, 6 resller terdata, Ical bisa pantau dari HP.

---

## Fase 3: Executive View & Otomasi

**Tujuan:** One-screen overview, notifikasi otomatis.

| # | Item | Pic |
|---|---|---|
| 3.1 | Executive Dashboard —satu layar: stok, revenue, top resller, alert | Developr |
| 3.2 | Auto-reply Telegam ke sales( konfirmasi laporan diterima) | Developer |
| 3.3 | Laporan otomatis mingguan ke Ical (Telegam PDF/teks) | Developer |
| 3.4 | Alert anomali — transaksi tidak wajar, stok negatif, piutang telat | Developer + Auditor |

**Output:** Satu layar holistic, sales dapet auto-reply, laporan mingguan otomatis.

---

##Fase 4: Scale & Iterasi

**Tujuan:** Siap ekspansi, pilto portfolio.

| # | Item | Pic |
|---|---|---|
| 4.1 | Evaluasi penggunaan 30hari → perbaikan UX/ bug | PM + semua agen |
| 4.2 | Tambah fitur berdasarkan feedback Ical & sales | PM |
| 4.3 | Siapkan portfolio case study + pitch deck | Sales + Marketer |
| 4.4 | Dokumentasi teknis (b uat pabrik) | Developer |

**Output:** Aplikasi stabil, portfolio siap pitch.

---

## Timeline Estimasi

| Fase | Estimasi | Mulai |
|------|--------|-------|
| Fase 0 | 1-2 hari | Sekarang |
| Fase 1 | 3-5 hari | Setelah Fase 0 |
| Fase 2 | 3-5 hari | Setelah Fase 1 |
| Fase 3 | 2-3 hari | Setelah Fase 2 |
| Fase 4 | Jalan paralel | Setelah Fase 2 |

**Total ke MVP (Fase 0-2):** ~7-12 hari
**Total ke full (Fase 0- 3):** ~9-15 hari

---

## Prioritas Sekarang

1. **Ical konfirmasi kode SAB/SATB/SKB/SKTB** —ini blocking Fase 1
2. **EV E deploy Developer** —mulai Fase0.1-0.3
3. **Guar dian** setup VPS environment

---

## Catatan

- Tech stack: Django + Tailwind + Leaflet.js + SQLite (dari brainstorm)
- 6 reseller test: Rudi, Ichsan, Tantri, Jarwo, Egi,Bu Yuli
- Semua hasil developer wajib audit sebelum ke EVE
- Setiap selesai fase → push ke GitH ub