# Handoff: Setup VPS Baru Sumopod (Cloudeka Jakarta) & Integrasi AI Gateway

- **Dari:** EVE (Chief of Staff)
- **Kepada:** Adam (Lead Architect & System/App)
- **Tanggal:** 4 November 2026
- **Status:** Siap Dieksekusi dari Workstation/Lokal PC Ical

---

## 1. Konteks & Latar Belakang
Cal baru saja mengaktifkan VPS baru di Sumopod (Cloudeka Jakarta) untuk ekspansi proyek:
1. Web application (termasuk rencana web app ngaji & landing page).
2. Pipeline automasi & scraping data potential buyer + auto-contact.
3. Tim AI Agent yang akan beroperasi di VPS tersebut.

Cal memutuskan agar setup awal infrastruktur VPS ini dikerjakan oleh **Adam** langsung dari local PC/workstation agar konfigurasi SSH, environment, dan remote deployment lebih rapi serta mudah dikelola.

---

## 2. Informasi Server Baru
- **Provider:** Sumopod (Cloudeka Jakarta, ID)
- **IP Publik:** `103.42.244.142`
- **Akses:** `root` (Password sudah diset oleh Cal saat provisioning)
- **OS:** Ubuntu 24.04.1 LTS (GNU/Linux 6.8.0-49-generic x86_64)
- **Spesifikasi:** 2 vCPU, 4 GB RAM, ~30 GB SSD

---

## 3. Tugas Utama Setup Fondasi (Adam)

### A. Swap Memory (Wajib Prioritas)
- VPS memiliki 4 GB RAM fisik. Untuk mencegah OOM (*Out Of Memory*) saat proses scraping (headless browser/Playwright) atau agentic loop berjalan berbarengan dengan web app:
  - Buat **Swap File 4 GB** di SSD (`/swapfile`).
  - Set `swappiness = 20` dan persistensikan di `/etc/fstab`.

### B. Core Runtime & Firewall
- Jalankan `apt update && apt upgrade -y`.
- UFW Firewall: Izinkan OpenSSH (22), HTTP (80), HTTPS (443), lalu aktifkan UFW.
- Pasang Nginx web server & reverse proxy.
- Pasang Python 3, `python3-venv`, `python3-pip`, Git.
- Pasang Node.js LTS (opsional/sesuai kebutuhan frontend web app ngaji).

---

## 4. Arsitektur Dual AI Gateway: Sumopod AI + Clouvia Router

Cal saat ini memiliki kuota **1 Miliar token di Clouvia** (Rp 150rb) dan akun **Sumopod AI** (QRIS/pay-per-token resmi). Kita membagi tugas kedua provider ini dengan prinsip *Separation of Concerns*:

### 1. Clouvia Router (`https://router.clouvia.id/v1`) — "Mesin Penggiling Data"
- **Peran:** Batch processing, data cleaning, ekstraksi teks scraping, summarization dokumen tebal, brainstorming konten.
- **Karakteristik:** Sangat murah (kuota 1B token), namun rentan *reset session* / timeout jika streaming panjang.
- **Implementasi:**
  - Wajib dibungkus dengan wrapper auto-retry (maksimal 2x–3x).
  - Digunakan untuk task yang *stateless* (tidak langsung memanipulasi file sistem/terminal).
  - Ikuti SOP Clouvia di `AGENTS.md` (Point 6): tangani error 401/402/429 dengan STOP seketika, jangan looping retry.

### 2. Sumopod AI (`https://ai.sumopod.com/v1`) — "Otak Eksekusi & QA"
- **Peran:** Developer agent (koding, editing file, patching), Auditor (QA), Lead Architect & Chief of Staff.
- **Karakteristik:** 100% kompatibel OpenAI, 0% markup harga resmi, latensi rendah, *tool calling* presisi, stabil tanpa risiko penggantian model diam-diam.
- **Implementasi:**
  - Jadikan default endpoint untuk script eksekusi kritis dan runtime agent utama.

---

## 5. Rekomendasi Format Environment Variable di VPS Baru
Buat file template `/root/.env` atau per project:
```bash
# --- Gateway 1: Sumopod AI (Core & High-Reliability) ---
SUMOPOD_BASE_URL="https://ai.sumopod.com/v1"
SUMOPOD_API_KEY="sk-..."

# --- Gateway 2: Clouvia Router (High-Volume Scraping / Batch) ---
CLOUVIA_BASE_URL="https://router.clouvia.id/v1"
CLOUVIA_API_KEY="clv_live_..."
```

---
*Handoff selesai. Adam dipersilakan melanjutkan eksekusi teknis dari lokal PC Ical.*
