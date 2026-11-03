# Memo: Distribusi Skill Tim (Adam ke EVE)

- **Tanggal:** 2026-11-03
- **Dari:** Adam (Lead Architect & System/App)
- **Kepada:** EVE (Chief of Staff)
- **Perihal:** Distribusi dan Penerapan Skill Baru untuk Agen di VPS
- **Lokasi Sumber:** `/root/ai-team/workspace/skills/`

---

## 1. Latar Belakang & Tujuan
Atas arahan Ical, sejumlah skill yang telah distandardisasi di lingkungan workstation didistribusikan ke VPS agar dapat diterapkan oleh agen-agen di bawah koordinasi EVE sesuai peran dan environment VPS.

Catatan: Skill `sop-hemat-token` tidak disertakan karena sudah menjadi bagian dari team policy kanonik.

---

## 2. Daftar Skill yang Didistribusikan

Berkas kanonik skill telah disinkronkan via Syncthing ke path `/root/ai-team/workspace/skills/`:

| Nama Skill | Lokasi Sumber | Deskripsi & Fungsi | Rekomendasi Target Agen di VPS |
|---|---|---|---|
| `buat-skill` | `/root/ai-team/workspace/skills/buat-skill/` | Generator dan validator pembuatan skill agen baru secara terstruktur dan portabel | EVE / Developer |
| `grill_me` | `/root/ai-team/workspace/skills/grill_me/` | Wawancara terarah & probing mendalam terhadap ide yang belum matang sebelum dieksekusi | EVE / Strategist / Analyst |
| `kritisi` | `/root/ai-team/workspace/skills/kritisi/` | Evaluasi kritis terstruktur (Verified, Assessment, Speculation) atas rencana/dokumen/karya tanpa revisi otomatis | Auditor / EVE |
| `web-extract` | `/root/ai-team/workspace/skills/web-extract/` | Ekstraksi konten web/video YouTube (metadata, transcript, source analysis) | Analyst / Marketer / Developer |

---

## 3. Permintaan Tindakan untuk EVE

1. **Inspeksi & Penyesuaian Lingkungan (Environment Adaptation):**
   - Periksa kebutuhan runtime pada environment VPS (Linux Ubuntu, Python environment Hermes, dependensi seperti `yt-dlp` atau `ffmpeg` untuk `web-extract`).
   - Khusus `web-extract`: versi workstation menggunakan forwarder PowerShell (`extract.ps1`). Jika diperlukan di VPS, sesuaikan eksekutor menggunakan script shell/bash (`extract.sh`) atau python script yang hemat resource.
2. **Pemasangan / Integrasi Skill:**
   - Pasang file skill ke direktori skill Hermes / profil agen terkait (misalnya `/root/.hermes/skills/` atau sesuai arsitektur konfigurasi skill aktif di VPS).
   - Pastikan agen terkait memahami trigger pemanggilan masing-masing skill.
3. **Verifikasi Keamanan & Higienitas:**
   - Jalankan pengecekan bersama Auditor sebelum aktivasi penuh ke alur kerja agen.
   - Tetap patuhi batasan efisiensi token, larangan pencatatan model identity di memori, dan zero external credential leak.

---
*Status: Berkas telah tersinkron ke workspace tim. Mohon EVE mengonfirmasi kesiapan penerapan di VPS setelah review.*
