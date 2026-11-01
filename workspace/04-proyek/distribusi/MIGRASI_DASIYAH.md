# Migrasi Dasiyah — Hermes Profile

Status: Model `thinkingmachines/inkling:free` + fallback `meta-llama/llama-3.3-70b-instruct:free` sudah di-set di `config.yaml`.
Bot `@PMDistribusiRokoBot` (token baru) aktif, webhook set ke `distro.raminesia.com`.

Arsitektur target (per AGENTS.md):
- Webhook `telegram_webhook` → delegasi ke Hermes profile `pm-distribusi` (bukan `agent.py` embedded)
- Dasiyah harus terlihat di Ruang/Mission Control sebagai agen fungsional
- `SOUL.md` sudah lengkap (persona, konversi unit, eskalasi)

Langkah tersisa (manual/dev):
1. Ubah `views.py`: `agent = DasiyahAgent()` → panggil Hermes `process_message` via API/profile
2. Pastikan `cron` profile `pm-distribusi` ada (heartbeat aktif)
3. Uji end-to-end Telegram → webhook → DB
