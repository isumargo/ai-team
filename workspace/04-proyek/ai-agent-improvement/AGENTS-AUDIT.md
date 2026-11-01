> **ARSIP (audit 2026-10-29, sebelum konsolidasi struktur).** Path di bawah ini sudah tidak berlaku; current canonical ada di `SOURCE-OF-TRUTH.md`.

# Fase 1 — AGENTS.md: diff & keputusan uji

**Tanggal:** 2026-10-29
**Status:** Audit selesai, file belum diubah.

## Diff tepat

`/root/AGENTS.md` dan `~/.hermes/AGENTS.md` sama seluruhnya, kecuali `~/.hermes/AGENTS.md` punya tambahan SOP hemat request/kuota Syncera (#6), 8 aturan ringkas. SOP ini jangan hilang.

## Consumer / jalur instruksi yang ditemukan

- `guardian/backup.py` memasukkan `/root/AGENTS.md` ke backup. Tidak memasukkan `~/.hermes/AGENTS.md`.
- Hermes service unit: `WorkingDirectory=/root/.hermes`, `HERMES_HOME=/root/.hermes`.
- Hermes `agent/prompt_builder.py` mencari `AGENTS.md` via git root/cwd directory chain; berkas di cwd berpotensi termuat. Maka file di `/root/` parent tidak otomatis menjadi pengganti file di `~/.hermes/`.
- Semua profile aktif punya `SOUL.md` masing-masing. Mayoritas SOUL menyebut menulis status ke `~/ai-team/status/<agent>.json`.
- `guardian/check_usage.py` adalah writer terverifikasi untuk `status/guardian.json`.
- Ada **file ketiga** `/root/.hermes/profiles/developer/AGENTS.md`. Spesifik Developer, tetapi juga memuat klaim model runtime yang melanggar SOP higiene. Belum ada perubahan.

## Opsi pemetaan

### Opsi A — satu sumber kanonis + copy-generated untuk Hermes (disarankan)

- Canonical: `/root/ai-team/policy/AGENTS.md` (atau lokasi proyek yang dipilih Cal).
- Generate/salin secara deterministik ke `/root/.hermes/AGENTS.md` setelah tes memastikan Hermes memang perlu file di cwd.
- `/root/AGENTS.md` diubah jadi pointer singkat/compatibility stub, atau berhenti dibackup jika tak diperlukan.
- Backup script diubah eksplisit agar menyimpan canonical; generated copy juga boleh ikut untuk disaster recovery.
- CI/local check membandingkan hash canonical vs generated; beda hash membuat audit fail.

**Pro:** benar-benar satu file yang diedit; tetap memenuhi loader cwd dan backup. **Kontra:** ada output copy yang tetap terlihat di filesystem, tapi tidak diedit manual.

### Opsi B — symlink

Satu file canonical lalu `~/.hermes/AGENTS.md` symlink ke file itu.

**Belum disarankan:** tidak diuji terhadap service, backup tar, permissions, dan workspace/sync. Windows mirror juga bisa mengubah semantics. Coba hanya di staging dan rollback mudah.

## Langkah yang masih perlu sebelum eksekusi

1. Pilih lokasi canonical untuk policy (`/root/ai-team/policy/AGENTS.md` atau `workspace/01-organisasi/AGENTS.md`).
2. Pastikan isi SOP #6 boleh digabung ke policy canonical.
3. Audit `prompt_builder` runtime test/trace untuk memastikan AGENTS mana yang termuat di gateway EVE, bukan hanya membaca source code.
4. Backup 3 AGENTS + backup script; uji generator/check di staging.
5. Baru setelah Cal setuju, terapkan satu sumber + generated copy, restart tidak perlu kecuali config-loader mensyaratkan.
6. Uji effective prompt / boot gateway dan cek backup archive memuat canonical.

## Batas scope

Belum mengubah `/root/AGENTS.md`, `~/.hermes/AGENTS.md`, developer profile AGENTS, `backup.py`, profile SOUL, atau status JSON.
