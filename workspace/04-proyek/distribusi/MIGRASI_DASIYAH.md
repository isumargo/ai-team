# Migrasi Dasiyah — Hermes Profile

Status: konfigurasi model profil sudah diset & terverifikasi (lihat `config.yaml` profil `pm-distribusi` — routing model dikelola terpusat di runtime, bukan didokumentasikan di sini).
Bot `@PMDistribusiRokoBot` (token baru) aktif, webhook set ke `distro.raminesia.com`.

Arsitektur target (per AGENTS.md):
- Webhook `telegram_webhook` → delegasi ke Hermes profile `pm-distribusi` (bukan `agent.py` embedded)
- Dasiyah harus terlihat di Ruang/Mission Control sebagai agen fungsional
- `SOUL.md` sudah lengkap (persona, konversi unit, eskalasi)

Kondisi aktual (2026-11-02):
- ✅ Webhook aktif di `distro.raminesia.com`, service `distribusi.service` jalan (Gunicorn)
- ✅ Pipeline parser → DB terhubung (`JUAL`/`STOK`/`PIUTANG`/`CONTOH`/`RETUR`)
- ✅ Balasan AI (pesan bebas) normal — bukan error generik
- ✅ 23 tes otomatis lulus
- ✅ Semua profil Hermes diverifikasi bisa merespons (model mati sudah diganti)

Langkah tersisa (manual/dev):
1. Uji end-to-end dari akun Telegram nyata (kirim `STOK`, `JUAL madju pro 1 bks rudi`, `halo dasiyah`)
2. Audit formal L1 (Auditor) + L2 (EVE) → status `LULUS AUDIT`
3. Ensure `cron` profile `pm-distribusi` heartbeat aktif
