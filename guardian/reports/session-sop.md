# SOP: Kapan `/new` Session, Kapan Lanjut

> Target: EVE & semua agen | Dibuat: 2026-10-18 | Versi: 1.0

---

## Trigger `/new` — LAKUKAN

### 1. Token mendekati batas kompresi
- **Kuning (>=500K token / 50%):** pertimbangkan `/new`
- **Merah (>=800K token / 80%):** HARUS `/new` — kompresi bisa gagal

Cara cek: Guardian kirim alert otomatis tiap 15 menit.

### 2. Compression Failure Terdeteksi
- `compression_fallback_streak` > 0 → kompresi gagal beruntun
- `compression_overload_streak` > 0 → kritis, `/new` sekarang
- Guardian kirim alert — jangan abaikan.

### 3. Topik Ganti Total
- Proyek baru? Bisnis baru? → `/new`
- Contoh: selesai ngerjain Distribusi, mau bahas Ruang → session baru

### 4. Setelah Deliverable Besar Selesai
- Misi selesai → `/new` bersihin konteks, mulai fresh
- Contoh: selesai deploy feature, selesai riset pasar

### 5. Cost per-Session Mulai Gede
- Session cost > $3 → pertimbangkan reset
- Session cost > $5 → harus `/new`

### 6. Konteks "Terpolusi"
- Terlalu banyak debugging bolak-balik? Banyak error tidak relevan?
- `/new` — jangan bawa-bawa history sampah ke sesi baru

---

## JANGAN `/new` — LANJUT AJA

### 1. Token Masih Rendah (< 200K)
- Masih banyak ruang, kompresi masih jauh
- Lanjut aja, hemat overhead session baru

### 2. Masih Ngerjain Task yang Sama
- Fitur sama, debug yang sama, file yang sama
- Session baru = harus reload konteks dari awal → boros token

### 3. Butuh Konteks Percakapan Sebelumnya
- Keputusan sebelumnya direferensikan? Diskusi panjang belum selesai?
- Kalau `/new`, agen lupa semua → malah tanya ulang

### 4. Diskusi Strategis / Brainstorming
- Butuh benang merah dari awal sampai akhir
- Kalau dipecah-pecah → kesimpulan hilang

### 5. Cost Rendah & Prompt Cache Aktif
- `cache_read_tokens` tinggi = kena prompt caching → murah
- `/new` = reset cache → malah lebih mahal di awal

---

## Aturan Tambahan

### `/compress` — Alternatif Sebelum `/new`
- Kalau `compression_ineffective_count` masih 0
- Kalau token masih di bawah ambang kompresi (50%)
- `/compress` bisa ngurangin ~80% token tanpa bikin sesi baru
- **Tapi:** kalau `compression_fallback_streak` udah > 0 → jangan `/compress`, langsung `/new`

### Agent Boleh Kasih Rekomendasi
- EVE bisa minta agen: "cek, mending `/new` atau lanjut?"
- Agent cek token usage dan compression health, kasih rekomendasi

### Guardian Monitor Otomatis
- Script: `/root/ai-team/guardian/session_monitor.py`
- Cron: setiap 15 menit via cronjob Hermes
- Alert ke: Telegram (EVE) atau local report
- Alert berisi: token level, cost, compression status

---

## Quick Reference

| Situasi | Aksi |
|---------|------|
| Token < 200K | Tetap lanjut |
| Token 200K–500K | Aman, monitor aja |
| Token 500K–800K | Pertimbangkan `/new` |
| Token > 800K | HARUS `/new` |
| Compression gagal | `/new` sekarang |
| Topik ganti | `/new` |
| Task sama, token rendah | Lanjut |
| Cost > $5/session | `/new` |

---

*Last update: Guardian cek setiap 15 menit, laporkan anomaly.*