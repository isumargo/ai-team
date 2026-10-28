# Memo Koordinasi: Ringkasan Semua Proyek & Infrastruktur untuk Adam (Lead Architect)

**Tanggal:** 2026-10-19  
**Dari:** EVE (Chief of Staff)  
**Kepada:** Adam (Lead Architect & System/App)  
**Perihal:** Ringkasan lengkap proyek bisnis dan infrastruktur tim AI yang sedang berjalan

## 1. Proyek Bisnis Utama

### A. Distribusi Rokok Madju PRO & Sukses Alami SKT
- Lokasi: `/root/ai-team/projects/distribusi/`
- Stack: Django 5.x + SQLite + Tailwind CDN + Leaflet.js CDN
- Fitur:
  - Input laporan sales via Telegram bot `@PMDistribusiRokoBot`
  - Webhook `telegram_webhook` mendelegasikan ke profil Hermes `pm-distribusi`
  - Profil Hermes menggunakan SOUL.md (persona Dasiyah/Jeng Yah) + LLM gratis (thinkingmachines/inkling:free + fallback)
  - Tools: cek_stok, catat_penjualan, catat_sample, catat_retur, cek_piutang, tanya_ke_owner, selesai
  - Transaksi atomic: Transaction, StockMovement, update Product.stock & Reseller.credit
  - Output dashboard: `/` (total stok, revenue mingguan, top reseller, piutang, grafik harian)
  - Halaman lain: `/stock/`, `/resellers/`, `/map/` (Leaflet.js), `/inventory/`
- Status: Fase 0 (fondasi) selesai. Menunggu Fase 1: Ical konfirmasi kode produk SAB/SATB/SKB/SKTB ke sales (Agus) untuk aktivasi parser laporan harian.
- Tim: Developer (kode), Auditor (review teknis), EVE (operasional), Adam (arsitektur & review kode)

### B. (Opsional) Proyek Lain
Saat ini fokus utama adalah distribusi rokok. Proyek lain belum diaktifkan menungan hasil audit dan konfirikasi Ical.

## 2. Infrastruktur & Sistem Pendukung

### A. Mission Control Dashboard
- Teknologi: HTML/CSS/JS, membaca file status per agen di `/root/ai-team/status/<agent>.json`
- Deploy: Nginx `proxy_pass` ke `localhost:3001` (Ruang) via `/etc/nginx/sites-available/mission-control`
- Auth: HTTP basic (user: `ical`, pass: `mc-raminesia-2026`)
- URL target: `mc.raminesia.com` (DNS A record belum dibuat di Rumahweb)

### B. Ruang 3D Virtual Office
- Sumber: `github.com/yugienugraha/ruang`
- Lokasi: `/root/.local/share/ruang`
- Jalankan: systemd user service `ruang.service` (port 3001)
- Catatan: Mengganti proyek lama `serve.py` port 8080 ( sudah dimatikan )

### C. Backup System
- Skrip: `backup.py` (no_agent, zero token)
- Cron: tiap 6 jam (job ID `47ea3d5b8d17`)
- Lokasi: `/root/backups/` (isi: ai-team/, config.yaml, USER.md, skills/, memories/, AGENTS.md)
- Retensi: maks 200MB total, backup terlama dihapus otomatis
- Ukuran per backup: ~0.9MB

### D. OpenRouter Cost Monitor
- Skrip: `check_usage.py` v2
- Cron: tiap 30 menit (job ID `98c8436a58f9`)
- Fungsi: alert per $1 increment via Telegram, auto‑switch ke model gratis (`nvidia/nemotron-3-super-120b-a12b:free`) saat penggunaan mencapai $5
- State file: `alert-state.json` (deduplikasi alert)

### E. DNS & Nginx
- Domain utama: `raminesia.com` (hosting Rumahweb, bukan Cloudflare)
- Subdomain aktif yang sudah di‑Nginx:
  - `distro.raminesia.com` → Django app distribusi (port 8080) via `/etc/nginx/sites-available/distro`
  - `mc.raminesia.com` → Mission Control (proxied to localhost:3001)
- Resolusi DNS: gunakan `resolvectl query` (UDP 53 diblokir di VPS) atau `getent hosts` untuk entri `/etc/hosts`
- SSL: sertifikat via `certbot --nginx` (tidak mendukung `--dry-run`; untuk uji coba gunakan `certonly` atau `renew`)

### F. Session Monitor
- Skrip: `session_monitor.py`
- Cron: tiap 15 menit
- Model saat ini: `nvidia/nemotron-3-super-120b-a12b:free` (via OpenRouter)

### G. Model & Fallback Tim (semua via OpenRouter)
- EVE (Chief of Staff): `deepseek/deepseek-v4-pro` → fallback `deepseek/deepseek-chat`
- Sub‑agene (Analyst, Developer, Strategist, dsb.): 
  - Utama: `nvidia/nemotron-3-super-120b-a12b:free` (gratis)
  - Fallback: `google/gemini-3-flash-preview` (termurah)
- Semua konfigurasi sudah dibersihkan dari model berbayar; semua fallback berjalan di tier `:free` atau Gemini direct.

## 3. Arsitektur Tim & SOP (untuk review Adam)

### A. Prinsip Agen Hermes
- Setiap agen tim **harus** berupa profil Hermes (bukan skrip tertanam) dengan:
  - `SOUL.md` yang menentukan persona, tugas, konversi unit, aturan transaksi, dll.
  - Terlihat di Ruang/Mission Control sebagai agen fungsional
  - Punya konfigurasi model sendiri (`config.yaml` di profil) dan cron jobs
- Migrasi sedang berjalan untuk profil `pm-distribusi` (lihat `/root/ai-team/projects/distribusi/MIGRASI_DASIYAH.md`)
  - Langkah tersisa:
    1. Ubah `views.py`: ganti panggilan ke `DasiyahAgent` dengan delegasi ke Hermes profile `pm-distribusi` via API
    2. Buat cron profil `pm-distribusi` (heartbeat aktif)
    3. Uji end-to-end: Telegram → webhook → DB

### B. Alur Kerja & Kualitas
1. Developer menulis kode → file hasil berada di direktori agen (misal: `agents/developer/`)
2. Hasil wajib melalui **Audit Lapisan 1** (Auditor Agent) – review teknis: format, bug, kalkulasi
3. Hasil LULUS Auditor dilanjutkan ke **EVE** (Chief of Staff) untuk review substansi & konteks
4. Hasil LULUS kedua lapis baru dilaporkan ke Ical (pemilik)
5. Komunikasi inter‑agen **lewat file** di `/root/ai-team/memo/` (bukan chat looping)
6. SOP Efisiensi Token:
   - Maksimal 3x retry per perintah/API call yang gagal
   - Output padat, to‑the‑point, tanpa preamble/penutup basa‑basi
   - Untuk file besar (>500 baris): gunakan `grep`, `head/tail`, atau `offset+limit` – jangan baca seluruh file ke konteks
   - Sanitasi file sampah: Guardian membersihkan log/cache sementara rutin; file >7 hari tanpa akses di `reports/` diarsipkan atau dihapus

### C. Role Tim Tercatat di AGENTS.md
- **Adam (Lead Architect & System/App)**: arsitektur teknis, fondasi sistem, standar kode, delegasi tugas teknis, review output AI Team, menjamin efisiensi resource, performa, sinkronisasi codebase lokal‑VPS
- **EVE (Chief of Staff)**: operasional VPS, brainstormer strategis, delegasi tugas harian ke agen, merekrut agen baru, mengawasi kesehatan tim via Guardian & Auditor, komunikasi antar‑agen via file, hanya melaporkan hasil LULUS AUDIT ke Ical
- **Guardian Agent**: SysAdmin VPS, monitoring resource, self‑healing, sanitasi biaya API, eskalsasi ke EVE & Adam jika ada insiden
- **Auditor Agent**: QA & review hasil kerja seluruh agen (lapisan 1 teknis), output: LULUS / REVISI / TOLAK
- **Agen Fungsional** (Shared Services): Analyst, Developer, Strategist, Marketer, Designer, Sales – semua proyek dapat memanfaatkan mereka
- **Manajer Proyek** (per bisnis): misal PM Distribusi untuk proyek distribusi rokok

## 4. Rekomendasi untuk Adam (Lead Architect)
1. **Verifikasi struktur Django distribusi** – pastikan sesuai standar tim (model, views, konfigurasi, tidak ada model berbayar)
2. **Review migrasi profil Hermes** – konfirmasi bahwaDelegasi webhook → profil Hermes `pm-distribusi` mengikuti pola yang sama dengan agen lain yang akan datang
3. **Periksa konfigurasi Nginx** untuk subdomain `distro.raminesia.com` dan `mc.raminesia.com` – pastikan proxy ke port yang benar (8080 untuk Django, 3001 untuk Ruang)
4. **Pastikan semua konfigurasi fallback OpenRouter** menggunakan tier `:free` atau Gemini direct (tidak ada model berbayar)
5. **Jika ada saran peningkatan arsitektur** (misal: penggunaan Docker, Redis, atau penyederhanaan), silakan catat di memo agar EVE bisa koordinasi dengan tim terkait
6. **Konfirmasi bila ada blokir teknis** sebelum Fase 1 distribusi dimulai (misal: butuh library tambahan, atau perubahan DB schema)

---  
*Informasi di atas berdasarkan file terbaru di repositori dan catatan infrastruktur. Untuk detail teknis spesifik, silakan periksa direktori yang disebutkan atau tanya langsung kepada EVE untuk klarifikasi.*  
