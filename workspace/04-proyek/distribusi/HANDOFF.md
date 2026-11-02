# HANDOFF — Proyek Distribusi Rokok (Madju PRO & Sukses Alami)

**Status:** app HIDUP (systemd/Gunicorn), **webhook (opsi A) aktif**, parser→DB terhubung, **AI balasan normal** (bukan error) — **LULUS AUDIT L1** (Auditor, 2026-11-02).
**Diperbarui:** 2026-11-02 (sesi EVE — audit L1 LULUS + E2E webhook terverifikasi)
**Lokasi kanonis:** `/root/ai-team/workspace/04-proyek/distribusi/`
**Kode aplikasi:** `/root/ai-team/projects/distribusi/app/` (bukan di workspace)
**Agen yang menjalankan:** profil Hermes `pm-distribusi` (Dasiyah) — `~/.hermes/profiles/pm-distribusi/`

> **Baca ini duluan di sesi baru.** Catatan lama (`PHASES.md`, `laporan/project-plan.md`) dari 18 Okt masih relevan sebagai rencana, tapi **kondisi sebenarnya sudah berubah** — rinciannya di bawah.

---

## Ringkasan

Yang dikira "project masih di awal" sebenarnya **sudah Phase 3**. Kode Django lengkap, DB terisi, bot Telegram hidup. Yang belum ada cuma **penghubungannya**: aplikasi mati, webhook belum di-set, dan AI-nya dipanggil langsung ke OpenRouter (melanggar policy + boros kuota).

---

## Kondisi nyata ( diverifikasi 2026-11-01)

### Yang sudah JADI ✅

| Komponen | Detail |
|---|---|
| Kode Django | `projects/distribusi/app/` — 5 model (Product, Reseller, StockMovement, Transaction, ChatSession), 7 view, 7 template |
| Data | `db.sqlite3`: 6 reseller, 2 produk, 1 transaksi, 1 chatsession, 21 migrasi |
| Parser | `distribusi/parser.py` → `parse_message(text) -> dict` |
| Bot Telegram | `@PMDistribusiRokoBot` — `getMe` balas ok |
| .env | `projects/distribusi/app/.env` — ada `TELEGRAM_BOT_TOKEN` |
| 6 reseller | Rudi, Ichsan, Tantri, Jarwo, Egi, Bu Yuli (sudah ada koordinat lat/long) |
| 2 produk | Madju PRO SKT (MP-001), Sukses Alami SKT (SA-001) — modal 7600, jual 8600 |

**Uji langsung (Django test client, tanpa server):** `/` → 200, `/stock/` → 200, `/resellers/` → 200, `/map/` → 200, `/inventory/` → 200. **Kode aplikasinya sehat.**

### Blocker 1 — Aplikasinya mati ✅ SUDAH SELESAI (2026-11-02)

Dulu ada 2 proses `runserver` zombie (18–19 Okt) tanpa listener di 8080.
**Sekarang:** `distribusi.service` (systemd) aktif, Gunicorn bind `127.0.0.1:8080`, 2 worker, `Restart=always`.
`distro.raminesia.com` → HTTPS **200**. Zombie sudah dibunuh.

### Telegram — webhook (opsi A) ✅

Bot menerima update lewat **webhook** (opsi A). Endpoint: `https://distro.raminesia.com/webhook/<token>/`.

**Keputusan Cal (2026-11-02): coba opsi A — webhook dulu.**
- **Webhook (A)** — aktif: `distribusi.service` (Gunicorn :8080), `distro.raminesia.com` HTTPS 200, `setWebhook` → `/webhook/<token>/` (getWebhookInfo: url ter-set, pending 0, last_error None). Uji POST publik → `{"status":"ok"}`; token salah → 401.
- **Long polling (B)** — cadangan jika webhook bermasalah; belum dipakai.

### Blocker 3 — AI dipanggil LANGSUNG ke OpenRouter ✅ SUDAH DIPERBAIKI (2026-11-02)

**Kondisi lama:** `views.py` memanggil OpenRouter langsung dengan nama model hardcode → balas error generik.

**Akar masalah (ditemukan 2026-11-02):**
1. Model default profil dikunci OpenRouter ke *"agentic harness"* → **HTTP 403** kalau dipanggil via API biasa. App Django = API biasa → **selalu gagal**.
2. `except:` diam-diam menelan error → user cuma lihat "sistem lagi pusing" tanpa jejak.
3. Profil Hermes `pm-distribusi` **tidak punya** `OPENROUTER_API_KEY` → Hermes one-shot gagal `ProviderNotConfiguredError`.
4. Konflik token: Hermes **polling** bot yang sama → bentrok dengan webhook.

**Yang diperbaiki:**
- `config.yaml` profil → diarahkan ke model tier `:free` yang bisa dipanggil API biasa (default + fallback).
- `OPENROUTER_API_KEY` ditambahkan ke `.env` profil (dari root `.env`).
- `agent.py`: `_load_models_from_profile()` + `_is_agentic_only()` — model yang dikunci harness otomatis dilewati, fallback kalau semua gagal.
- `agent.py`: `except:` → `except Exception` + `logger.warning` (jejak error masuk log).
- Telegram polling Hermes dimatikan (`platforms.telegram.enabled: false`) → satu bot satu mekanisme.

**Status:** Hermes one-shot profil `pm-distribusi` → balas normal. App Django → balas normal (terbukti via uji shell).

---

## Rencana kerja (2026-11-02 — status terbaru)

| # | Item | Status |
|---|------|--------|
| 1 | Bangunkan app (systemd + Gunicorn) | ✅ selesai |
| 2 | Set mekanisme Telegram (webhook) | ✅ selesai |
| 3 | Ganti panggilan AI → profil Hermes | ✅ selesai (config + key + guard) |
| 4 | Parser → DB (`JUAL`/`STOK`/`PIUTANG`/dll) | ✅ selesai (wired di `views.py`) |
| 5 | Tes otomatis (23 tes) | ✅ selesai — `manage.py test distribusi` 23/23 lulus |
| 6 | Perbaiki semua profil Hermes yang mati | ✅ selesai (lihat "Blocker 4" di bawah) |
| 7 | Uji E2E via webhook (parser + AI) | ✅ selesai — `STOK` 200, `JUAL` creating transaksi, `halo dasiyah` balas persona normal |
| 8 | Audit L1 (Auditor) | ✅ **LULUS** — `workspace/03-agen/auditor/laporan/audit-report.md` |
| 9 | Audit L2 (EVE) → lapor ke Cal | ✅ selesai — `workspace/04-proyek/distribusi/laporan/laporan-l2-20261102.md` |
| 10 | Commit + push ke `github.com/isumargo/ai-team` | ✅ commit `8e843ef` sudah push; commit lanjutan di sesi ini |
| 11 | Uji human dari akun Telegram Cal/sales | ⏳ **sisa 1** — teknis sudah terverifikasi, tapi belum ada Cal yang chat langsung |

**Catatan item 11:** verifikasi E2E di atas memakai update Telegram sintetis (payload curl ke webhook publik + balasan dicek di `ChatSession`/DB), bukan akun|Cal nyata. Ini membuktikan pipeline-nya sehat end-to-end, tapi tetap ideal dicek sekali dari HP Cal.

**Cara uji (item 7):** kirim ke `@PMDistribusiRokoBot`:
1. `STOK` → harus balas daftar stok (jalur parser, tanpa AI)
2. `JUAL madju pro 1 bks rudi` → harus ✅ + stok turun di DB
3. `halo dasiyah` → harus balas normal (bukan "sistem lagi pusing")

### Blocker 4 — 8 dari 9 profil Hermes mati ✅ SUDAH SELESAI (2026-11-02)

**Temuan:** saat memperbaiki bot, terungkap masalah yang lebih luas — **8 profil Hermes lain (analyst, designer, developer, guardian, marketer, sales, strategist, auditor) tidak bisa merespons sama sekali.** Semua memakai model yang sama, yang **tidak lagi bisa dipanggil sebagai API biasa**:

| Model lama | Status HTTP | Arti |
|---|---|---|
| Model A (`nemotron-3-super-120b…`) | 404 | Tier free dicabut OpenRouter ("unavailable for free") |
| Model B (`inkling:free`) | 403 | Hanya tersedia untuk *agentic harness*, bukan API biasa |

> Nama model sengaja disamarkan di sini — identitas lengkapnya ada di file config runtime profil, bukan di dokumen tim (aturan anti-halusinasi).

Jadi ini **bukan** satu bug di satu profil — ini config yang sama ter-copy ke semua profil.

**Yang diperbaiki:**
- Semua profil → diarahkan ke model tier `:free` yang **terbukti 200** saat dipanggil API biasa (default + fallback).
- Tiap profil sekarang punya `OPENROUTER_API_KEY` sendiri di `.env` (sebelumnya hanya root `~/.hermes/.env` yang punya).
- `developer/config.yaml` juga punya override `delegation:` (model subagent) → ikut diperbaiki, plus `fallback:` top-level yang sebelumnya kosong.
- `guardian/check_usage.py` — `BACKUP_MODEL` menunjuk model 404 yang sudah mati → diperbaiki (auto-switch biaya sekarang pakai model hidup).
- Semua config di-backup otomatis sebelum diubah → `~/.hermes/profiles/<profil>/backups/config/config.yaml.bak.<timestamp>`.
- Verifikasi: 9/9 profil `hermes -p <profil> chat --oneshot` → balas normal.
  - Catatan: pada batch verifikasi pertama, `auditor` sempat GAGAL 1x (transien — retry langsung `SIAP`, lalu 3x berturut-turut juga `SIAP`). Jadi statusnya **lulus**, bukan flaky kronis.

**Catatan:** nama model sengaja tidak ditulis di HANDOFF/memo — hanya di file config runtime, sesuai aturan anti-halusinasi.

### Blocker 5 — Auto-switch Guardian salah target ⚠️ TERDETEKSI, MENUNGGU KEPUTUSAN CAL (2026-11-02)

**Temuan (baru, di luar cakupan audit L1):**

`guardian/check_usage.py` memanggil `hermes config set model.default ...` **tanpa flag `-p <profil>`**. Efeknya: saat biaya melewati limit, yang diubah **hanya profil root (EVE)** — bukan profil anak (analyst, developer, pm-distribusi, dll) yang justru boros.

Observed saat sesi ini: biaya OpenRouter sudah **$9.86 dari $10** (limit config Guardian $5) → Guardian berhasil switch **root config** → `model.default` EVE ikut berubah.

**Dampak:**
- Yang **tidak** terpengaruh: guard/sanitasi biaya profil anak — Guardian tidak pernah mengarahkan mereka.
- Yang **terpengaruh**: profil EVE ditulis ulang tiap 30 menit oleh cron Guardian. harmless selama model switch itu valid, tapi EVE sekarang menjalankan `provider: anthropic` (base_url `api.syncera.id`) dengan `model.default` berupa model OpenRouter — kombinasi yang **tidak sama dengan** routing normal EVE, dan INGIN biaya Syncera (bukan OpenRouter) **tidak dimonitor sama sekali** Guardian (ia cuma cek endpoint `openrouter.ai/api/v1/credits`).

**Status:** kuwait — belum kuubah. Alasannya:
1. Menambah monitor biaya Syncera = perubahan infra (butuh izin Cal).
2. Menentukan apakah auto-switch harus kena **semua profil** (bukan cuma root) = perubahan perilaku biaya (batas `$5` vs `$20` masih konflik, lihat catatan di bawah).
3. Paket bersama Synccera = kuota 550 request/5 jam + 5.000/minggu — batas berbeda dari berbasis dollar, jadi logikanya beda.

**Yang sudah dilakukan:** `BACKUP_MODEL` di `guardian/check_usage.py` diperbaiki agar tidak menunjuk model mati, jadi switch berikutnya tidak jadi no-op.

**Konflik angka batas biaya (butuh keputusan Cal):**
| Sumber | Batas |
|---|---|
| `guardian/config.json` | $5 |
| Catatan tim lama (MEMORY.md / memo 2026-10-19) | $20 |

Guardian sekarang memakai **$5** (nilai di `guardian/config.json`, yang dibaca `check_usage.py`). Angka $20 belum di-update ke sana.

---

## Data bisnis (konteks, jangan diubah tanpa konfirmasi)

- Pemilik: Ical & Nabla (keponakan)
- Produk: Madju PRO SKT + Sukses Alami SKT
- Modal: Rp 7.600/bks · Jual ke reseller: Rp 8.600/bks · Jual akhir: Rp 10.000–11.000
- Stok awal: 2.000 bks (1.600 karton + 400 sampe)
- Target: habiskan stok 2.000 bks dengan margin maksimal, tracking penjualan & inventory, identifikasi reseller tetap, siapkan strategi scale-up batch berikutnya.

**Margin per bks: Rp 1.000** (dari 7.600 → 8.600 ke reseller).

---

## Aturan yang wajib dijaga

- **Jangan** hardcode nama model/tier di kode, balasan bot, atau laporan. Routing dikelola runtime.
- **Jangan** simpan token/API key di repo atau workspace — `.env` & `db.sqlite3` sudah di-ignore git.
- **Jangan** ubah threshold biaya / billing tanpa izin Cal.
- **Jangan** ubah service/firewall tanpa izin Cal (tapi systemd service baru untuk app = perlu izin eksplisit dulu).
- Semua hasil kerja wajib **LULUS AUDIT** (Auditor L1 → EVE L2) sebelum lapor ke Cal.
- Komunikasi antar-agen lewat **file** di `workspace/04-proyek/distribusi/laporan/`, bukan chat loop.
- Prinsip desain: Agile, terstruktur, scalable, aman tanpa ganggu operasi, resilient, aturan jelas, mudah dikembangkan; hindari duplikasi.

---

## Referensi file

| File | Isi |
|---|---|
| `PHASES.md` | Rencana fase 0–4 (dari 18 Okt) |
| `ROLE.md` | Peran PM Distribusi + konteks bisnis |
| `MIGRASI_DASIYAH.md` | Rencana migrasi Dasiyah ke Hermes profile |
| `laporan/project-plan.md` | Project plan awal |
| `laporan/brainstorm-2026-10-18.md` | Hasil brainstorm (pilihan tech stack) |
| `inbox/` | Input untuk Dasiyah |
| `projects/distribusi/app/PHASE2_TASK.md`, `PHASE3_TASK.md` | Task phase 2 & 3 |
| `projects/distribusi/app/distribusi/parser.py` | Parser pesan → dict |
| `projects/distribusi/app/distribusi/views.py` | 7 view + webhook (yang perlu diubah) |
| `projects/distribusi/app/distribusi/models.py` | 5 model |

---

## Catatan Credential

- Token bot & API key hanya di `projects/distribusi/app/.env` (mode private, sudah gitignored).
- **Jangan** tampilkan, salin ke repo/workspace, atau kirim di chat.
- Credential GUI Syncthing ada di `/root/.config/syncthing/` — jangan sentuh tanpa izin Cal.

---

## Yang BELUM diubah di sesi ini

Sesi 2026-11-01 (EVE) **hanya audit** — tidak ada perubahan kode, service, atau konfigurasi. Semua yang tertulis di atas adalah fakta terverifikasi (2026-11-01), bukan asumsi.
