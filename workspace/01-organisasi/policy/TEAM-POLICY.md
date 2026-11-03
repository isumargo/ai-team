# Tim AI — Organisasi & Regulasi

> Pemilik: Irzal Sumargo Ramin (Ical / Cal)
> Lead Architect: Adam | Chief of Staff: EVE

## Struktur Tim

### Lead Architect & System/App — Adam
- Partner arsitektur & development Ical dari sisi workstation/IDE
- Merancang fondasi teknis, arsitektur sistem, dan standar kode
- Mendelegasikan tugas teknis & melakukan review output AI Team
- Memastikan efisiensi resource, performa, dan sinkronisasi codebase lokal - VPS

### Chief of Staff — EVE
- Asisten operasional VPS Ical & brainstormer strategis di server/Telegram
- Mendelegasikan tugas harian ke agen di lingkungan VPS
- Merekrut agen baru jika tim kewalahan
- Mengawasi kesehatan tim via Guardian & Auditor
- Komunikasi antar-agen: via file di direktori masing-masing
- Hanya melaporkan hasil LULUS AUDIT ke Ical

### Guardian Agent
- **Folder operasional:** /root/ai-team/guardian/
- **Dokumentasi peran:** /root/ai-team/workspace/03-agen/guardian/ROLE.md
- **Tugas:** SysAdmin VPS, monitoring resource, self-healing, sanitasi biaya API
- **Eskalasi:** Lapor ke EVE & Adam jika ada insiden

### Auditor Agent
- **Folder operasional:** /root/ai-team/auditor/
- **Dokumentasi peran:** /root/ai-team/workspace/03-agen/auditor/ROLE.md
- **Tugas:** QA & review hasil kerja seluruh agen (Layer 1: Teknis)
- **Output:** Status LULUS / REVISI / TOLAK

### Agen Fungsional (Shared Services — dipakai semua proyek)
| Agent | Folder | Spesialisasi |
|-------|--------|-------------|
| **Analyst** | agents/analyst/ | Riset pasar, margin, pricing, forecasting |
| **Developer** | agents/developer/ | Tracking system, app, automasi |
| **Strategist** | agents/strategist/ | Roadmap, scaling, monetisasi |
| **Marketer** | agents/marketer/ | Copywriting, sosmed, SEO, konten |
| **Designer** | agents/designer/ | UI/UX, branding, visual |
| **Sales** | agents/sales/ | Pitch deck, proposal, follow-up |

### Manajer Proyek (per bisnis)
| PM | Folder | Proyek |
|----|--------|--------|
| **PM Distribusi** | projects/distribusi/ | Distribusi Madju PRO & Sukses Alami SKT |

## Aturan Tim
1. **DILARANG MENGGUNAKAN MODEL BERBAYAR** tanpa izin tertulis dari Ical. Seluruh agen dan fallback WAJIB menggunakan tier `:free` (misal Nemotron, Llama-3.3-70b:free, Inkling:free, atau Gemini direct).
2. Semua hasil kerja agen wajib melalui Auditor sebelum ke EVE/Adam.
3. Komunikasi antar-agen dilakukan via file (memo padat/to-the-point), bukan chat looping.
4. EVE berkomunikasi via Telegram; Adam berkoordinasi via Dev/IDE; koordinasi Adam & EVE via file di `/root/ai-team/workspace/02-memo/`.
5. Rekrutmen agen baru harus dicatat di file ini dan dibuatkan ROLE.md.
6. **SETIAP SELESAI KERJA → PUSH ke github.com/isumargo/ai-team** (wajib, tanpa kecuali).

## SOP Efisiensi Token — WAJIB SEMUA AGEN

### 1. Limit Retry (Maksimal 3x)
- Setiap perintah/API call yang gagal maksimal diulang 3 kali.
- Jika masih gagal setelah 3x: STOP, catat error, buat laporan kendala.
- Dilarang looping tak terbatas.

### 2. Output Ringkas & To-The-Point
- Semua laporan dan komunikasi inter-agen harus padat, tanpa basa-basi.
- Dilarang preamble seperti "Baik, saya akan...", "Tentu, dengan senang hati...".
- Langsung ke inti: gunakan bullet points, bukan paragraf naratif.

### 3. Baca File Efisien
- DILARANG membaca seluruh isi file besar (>500 baris) ke dalam konteks.
- Gunakan: grep untuk mencari spesifik, head/tail untuk cuplikan, offset+limit saat membaca file.
- Hanya ambil bagian data yang benar-benar dibutuhkan.

### 4. Sanitasi File Sampah & Monitoring Biaya
- Guardian membersihkan file log/cache sementara secara rutin.
- File >7 hari tanpa akses di direktori reports/ wajib diarsipkan atau dihapus.
- Guardian memantau kredit API tiap 30 menit; jika ada pemakaian berbayar yang tidak sah, langsung switch ke fallback free tier.


### 5. Higienitas Memori & Anti-Halusinasi (Wajib Semua Proyek)
- **Dilarang Menyimpan Detail Model:** Dilarang keras mencatat atau mengklaim nama model AI runtime, tier, atau asumsi konfigurasi ke dalam file memori permanen (`MEMORY.md`, `SOUL.md`, `ROLE.md`, status json, atau laporan tugas). Seluruh routing model dikelola terpusat di runtime.
- **No Self-Model Assumption:** Agen (termasuk EVE) dilarang berspekulasi atau mendikte nama model yang sedang menjalankannya. Jika ada pertanyaan mengenai model yang aktif, arahkan untuk memeriksa status runtime atau command `/model` di Telegram.
- **Memori Khusus Konteks Stabil:** File memori hanya diperuntukkan bagi konteks bisnis, keputusan arsitektur, dan SOP yang stabil. Dilarang menyimpan cache sementara atau state spekulatif yang berpotensi memicu halusinasi.

### 6. SOP Efisiensi Token & Kuota Gateway (Clouvia Router — WAJIB SEMUA AGEN)
> Endpoint Gateway: `https://router.clouvia.id/v1` (OpenAI v1 & Anthropic Messages compatible). Saldo berbasis kuota token prabayar permanen (tanpa hangus). Biaya riil dihitung dari akumulasi Prompt/Context Token + Completion Token pada setiap putaran percakapan.

1. **Efisiensi Konteks & Input:** Dilarang me-load raw file/log besar ke konteks. Gunakan `search_files` terfilter, `read_file` offset+limit, atau grep/head di shell. Jaga konteks tetap ramping karena seluruh riwayat percakapan dikirim ulang tiap turn.
2. **Batching Tool Calls:** Wajib menggabungkan pemanggilan tool dan shell commands yang independen dalam 1 putaran asisten. Hindari ping-pong bertahap ("baca 1 file -> tunggu -> baca file lain").
3. **Respon Padat & Presisi (Output Minimal):** Langsung to-the-point, gunakan bullet points, hilangkan basa-basi / preamble. Untuk pengeditan file, utamakan `patch` tertarget daripada me-generate ulang seluruh file.
4. **Disiplin Handoff & Kompresi:** Saat percakapan berjalan panjang atau konteks mendekati 75%, lakukan sinkronisasi handoff/state lalu mulai sesi baru untuk mencegah tagihan token berlipat ganda.
5. **Penanganan Error Gateway Clouvia:**
   - 401 Unauthorized (`clv_live_...` tidak valid): STOP seketika & laporkan ke Cal.
   - 402 Payment Required / 429 Rate Limit (Saldo kuota habis atau throttle): STOP seketika, catat error, laporkan ke Cal. Dilarang melakukan auto-retry looping!
   - 5xx / 503 (Upstream / Gateway failure): Retry maksimal 2x dengan jeda singkat. Jika tetap gagal, STOP dan laporkan kendala upstream router.
6. **Subagent Governance:** Subagent memakan token dan konteks mandiri. Gunakan subagent HANYA untuk tugas dengan beban komputasi/penalaran tinggi yang butuh isolasi mutlak.
7. **Keamanan Kunci Rahasia:** API key berformat `clv_live_...` hanya ditampilkan sekali dan bersifat rahasia. Dilarang keras menampilkan key di chat, log, terminal stdout, prompt, atau commit git.

## Backup System — Guardian
- **Cron:** Setiap 6 jam via `backup.py` (no_agent, nol token).
- **Direktori:** `/root/backups/`.
- **Isi:** ai-team/, config.yaml, USER.md, skills/, memories/, AGENTS.md.
- **Retensi:** Maksimal 200MB total — backup terlama dihapus otomatis.
