# Mission Control — Spesifikasi Produk

## 1. User & Masalah
- **User:** Hanya Ical (1 orang)
- **Masalah:** Ga tau agent lagi ngapain, sulit monitor progres, ga ada overview sistem

## 2. Fitur MVP

### Dashboard (halaman utama)
- Statistik: jumlah agent, task aktif, biaya OpenRouter, health VPS
- Ringkasan status semua agent (nama, role, status, task terakhir)

### Agents (daftar semua agent)
- Nama, role, status real-time (🟢 kerja / ⏳ idle / 🔴 error / 🔵 cron)
- Task yang sedang dikerjakan
- Model yang digunakan
- Folder kerja

### Activity Log
- Kejadian terbaru: cron selesai, task baru, error, alert
- Urut waktu (terbaru di atas)
- Bisa difilter per agent

### Office 2D (virtual kantor)
- Tiap agent = karakter di ruangan
- Status real-time: kerja (di meja), idle (di pantry), error (merah berkedip), offline (di luar)
- Animasi: berjalan, mengetik, idle
- Klik karakter → lihat detail agent

### Kontrol
- **Check Now** — trigger Guardian cek biaya saat itu juga
- **Set Limit** — input angka → ubah batas auto-switch ($1-$10)
- **Test Agent** — ping agent, cek response

## 3. Data Flow

```
Agent → tulis /root/ai-team/status/<agent>.json
  │
  ▼
Dashboard baca semua file status → refresh tiap 5 detik
  │
  ▼
Kontrol (Set Limit) → tulis /root/ai-team/guardian/config.json
  │
  ▼
Guardian baca config.json setiap cron → ikuti limit baru
```

## 4. Format Status File (/root/ai-team/status/<agent>.json)

```json
{
  "agent": "guardian",
  "role": "System Administrator",
  "status": "cron",
  "task": "check_usage.py — cek biaya OpenRouter",
  "model": "none (script)",
  "last_activity": "2026-10-17T14:37:20Z",
  "cost_current": 1.10,
  "cost_limit": 5.00
}
```

## 5. Tech Stack
- **Frontend:** HTML + CSS + Tailwind-like CSS + vanilla JS
- **Backend:** NONE — baca file JSON langsung dari filesystem
- **Server:** Buka file HTML langsung di browser (file:///) atau via `python3 -m http.server`
- **Refresh:** `setInterval` tiap 5 detik fetch ulang status file

## 6. Yang Tidak Termasuk (Phase 2)
- Kanban board (task tracking per proyek)
- Schedule (jadwal cron lengkap)
- User authentication
- Mobile responsive (desktop-first)