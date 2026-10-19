# Memo Status: Proyek Distribusi Rokok (Madju PRO & Sukses Alami SKT)

**Tanggal:** 2026-10-19  
**Dari:** EVE (Chief of Staff)  
**Kepada:** Adam (Lead Architect & System/App)  
**Perihal:** Status awal proyek tracking distribusi rokok

## Ringkasan Status Saat Ini
- **Fase 0 (Fondasi)** selesai: Django project terinstall di `/root/ai-team/projects/distribusi/app/`
  - Model DB: Product, Reseller, StockMovement, Transaction, ChatSession
  - 2 produk terisi: Madju PRO SKT (800 bks), Sukses Alami SKT (800 bks)
  - 6 reseller dummy: Rudi, Ichsan, Tantri, Jarwo, Egi, Bu Yuli
  - Stok awal total: 2.000 bks (termasuk 200 bks sample per produk)
  - Admin user: admin / admin123
  - Frontend: Tailwind CDN + Leaflet.js CDN (responsive)
  - `.env` sudah ada dengan TELEGRAM_BOT_TOKEN dan DJANGO_SECRET_KEY (tidak diubah)

## Workflow Utama (Terimplementasi)
1. **Input:** Sales kirim laporan harian via Telegram ke bot `@PMDistribusiRokoBot`
2. **Webhook:** `telegram_webhook` di `views.py` memvalidasi token, mendelegasikan ke profil Hermes `pm-distribusi`
3. **Profil Hermes (`pm-distribusi`):**
   - Menggunakan SOUL.md dari `/root/.hermes/profiles/pm-distribusi/SOUL.md` (persona Dasiyah/Jeng Yah)
   - Memanggil LLM (thinkingmachines/inkling:free + fallback meta-llama/llama-3.3-70b-instruct:free) via OpenRouter
   - Tools tersedia: `cek_stok`, `catat_penjualan`, `catat_sample`, `catat_retur`, `cek_piutang`, `tanya_ke_owner`, `selesai`
   - Konversi unit wajib: 1 slop = 10 bks, 1 bal = 100 bks, 1 karton = 400 bks
4. **Eksekusi Transaksi:**
   - LLM memilih tool sesuai pesan (contoh: "Jual Madju PRO 50 bks ke Rudi")
   - Tool menjalankan fungsi di `commands.py` dengan transaksi atomic:
     - Buat Transaction (status unpaid)
     - Buat StockMovement (tipe out/sample/return)
     - Update Product.stock
     - Update Reseller.credit (piutang)
   - Semua disimpan ke SQLite (`db.sqlite3`)
5. **Output Dashboard:**
   - `/`: total stok, revenue mingguan, top reseller, piutang, grafik harian
   - `/stock/`: tabel produk + stok
   - `/resellers/`: tabel reseller + tier + piutang
   - `/map/`: peta reseller dengan Leaflet.js (butuh lat/lng)
   - `/inventory/`: command center stok & movimentasi

## Blokir Saat Ini
- **Fase 1 blokir:** Menunggu Ical konfirmasi kode SAB/SATB/SKB/SKTB ke sales (Agus) — ini diperlukan untuk parser laporan harian Fase 1.
- Tanpa konfirmasi kode, tidak bisa melanjutkan ke implementasi pola laporan terstruktur dari Telegram.

## Catatan Teknis & Arsitektur
- **Tech Stack:** Django 5.x + SQLite + Tailwind CDN + Leaflet.js CDN
- **Integrasi:** Telegram Bot API + OpenRouter (LLM gratis)
- **File penting:** `models.py`, `views.py`, `agent.py`, `commands.py`, `SOUL.md`
- **Migrasi Arsitektur:** Sedang beralih dari `agent.py` embedded ke profil Hermes mentuh (`pm-distribusi`) sesuai standar tim — semua agen harus berupa profil Hermes dengan SOUL.md, terlihat di Ruang/Mission Control, punya cron & konfigurasi model sendiri.
  - Berkas migrasi: `/root/ai-team/projects/distribusi/MIGRASI_DASIYAH.md`
  - Langkah tersisa: ubah `views.py` delegation ke Hermes API, buat cron profile, uji end-to-end

## Role Tim & SOP
- **Developer:** Membangun & refine kode (SOP: hasil wajib audit sebelum ke EVE/Adam)
- **Auditor:** Review teknis (format, bug, kalkulasi) — output LULUS diperlukan ke EVE
- **EVE (Saya):** Operations, delegasi agen, monitor kesehatan tim, koordinasi via file memo & Telegram ke Ical
- **Adam:** Lead Architect — review arsitektur, verifikasi kode dari IDE, pastikan efisiensi resource & sinkronisasi codebase lokal-VPS
- **Ical:** Owner — hanya menerima hasil LULUS kedua lapis audit (Layer 1 Auditor + Layer 2 EVE)

## Rekomendasi untuk Adam
1. Verifikasi struktur Django app sesuai standar tim (model, views, konfigurasi)
2. Pastikan tidak ada penggunaan model berbayar dalam konfigurasi (semua fallback `:free`)
3. Review pola delegation webhook → Hermes profile untuk konsistensi dengan standar agen tim
4. Konfirmasi bila ada arsitektur yang perlu disesuaikan sebelum Fase 1 dimulai

**Status:** Siap melanjutkan ke Fase 1 setelah Ical memberikan konfirmasi kode produk ke sales.

---  
*Catatan: Informasi ini berdasarkan file review di direktori proyek dan arsitektur tim. Untuk verifikasi teknis langsung, silakan cek kode di `/root/ai-team/projects/distribusi/app/`.*