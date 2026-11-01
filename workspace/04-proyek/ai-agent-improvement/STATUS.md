# Status — Perbaikan AI Agent

**Diperbarui:** 2026-11-01 (sesi commit selektif + status tim live)
**Ringkasan:** Workspace dipakai GitHub. Repo dibersihkan lewat 5 commit selektif (push `507a08b`). Status tim live dibangun: satu writer + satu dashboard web. Logika Guardian tetap tidak disentuh.

## Selesai

- Policy tim punya satu canonical di `workspace/01-organisasi/policy/TEAM-POLICY.md`; tiga copy runtime/generated hash-check lulus. Developer menerima gabungan policy + instruksi profilnya.
- Instruksi Developer dipisah ke `workspace/01-organisasi/policy/DEVELOPER-INSTRUCTIONS.md`; runtime copy diverifikasi.
- Profil USER aktif di `~/.hermes/memories/USER.md`; legacy snapshot dipertahankan.
- Dokumen proyek AI (handoff/status/plan/decisions/log) sekarang hanya ada di `workspace/04-proyek/ai-agent-improvement/`; duplikat repo dihapus.
- Memo kanonis di `workspace/02-memo/`; folder `memo/` root dipensiunkan.
- ROLE agen dan laporan kanonis berada di `workspace/03-agen/`; SOUL, Developer instructions, dan Guardian scripts/jobs diarahkan ke sana. Output repo lama dipensiunkan setelah backup + verifikasi.
- Dokumen bisnis distribusi di `workspace/04-proyek/distribusi/`; kode aplikasi tetap di `projects/distribusi/app/`.
- Snapshot status lama diarsipkan, bukan dihapus; instruksi menulis status manual diperbaiki untuk tujuh profil.
- Syncthing VPS ke PC teruji dua arah. Probe tetap ada sampai Cal menyetujui penghapusan.
- **Commit selektif + push ke GitHub** (`302c46d` → `507a08b`, 5 commit). Working tree bersih, tidak ada secret di history.
- **`.gitignore` diperbaiki**: path runtime kanonis di `workspace/` sekarang terlindungi. Sebelumnya hanya path lama yang dilindungi, sehingga file runtime baru akan ikut ter-commit.
- **Status tim live** dibangun: `guardian/team_status.py` (writer tunggal, nol token) → `workspace/05-status/team.json`; dashboard web di `https://hermes.raminesia.com/team-status/` (basic auth).

## Sedang / belum selesai

- Review logic job Guardian (threshold/alert/backup/session monitor) tetap ditunda atas permintaan Cal. Yang sudah masuk commit hanya perubahan **path** — logika tidak berubah.
- Status GUI Syncthing auth: penyebabnya sudah jelas (lihat Temuan) tetapi **belum diperbaiki**; keputusan ada di Cal.
- Kredit OpenRouter tersisa `$0.14` dari `$10`, sementara job tetap menulis "SWITCHED" tiap 30 menit. Perlu keputusan Cal (bagian review Guardian).
- Backup `/root/backups` 196M/200M — hampir penuh, belum exclude `venv/`, `node_modules/`, `__pycache__/`.
- Django Distribusi `:8080` dan Ruang 3D `:3001` masih mati; belum ada perubahan service/process/firewall.

## Ditunda atas permintaan Cal

- **Guardian:** review job, threshold, alert, backup scope, dan session monitor pada sesi khusus.
- **Django Distribusi (`distro.raminesia.com`, :8080):** perlu audit/perbaikan nanti; arah produk ialah web monitoring penjualan.
- **Ruang 3D (`mc.raminesia.com`, :3001):** perlu audit/perbaikan nanti; tujuannya Mission Control.
- Belum ada perubahan service, proses, atau firewall untuk dua aplikasi tersebut.

## Temuan baru (2026-11-01)

- **GUI Syncthing sudah punya password, tapi panel tetap terbuka.** `config.xml` memuat `user="ical"`, password ter-set, `authMode="static"`, `address="127.0.0.1:8384"` — namun `GET /` tanpa kredensial tetap membalas HTTP 200. Penyebabnya bukan "password belum di-set", melainkan Syncthing v1.29.5 tidak menegakkan basic auth pada path GUI. Dampak terbatas (loopback + 8384 tidak dibuka ke publik). `guardian/syncthing_auth.py` sudah diberi guard `--apply` (default dry-run) tapi **belum dijalankan** karena restart Syncthing tidak memperbaiki masalah ini.
- **Modul `crypt` Python dihapus** (VPS ini pakai Python 3.14.9). Verifikasi hash htpasswd tidak bisa dilakukan di Python tanpa dependency tambahan; karena itu auth dashboard diserahkan ke nginx (`auth_basic`), sesuai pola vhost `distro` dan `mission-control`.
- **Struktur session per-agen tidak ada di `state.db` utama** — `profile_name` selalu `default`. Data per-agen ada di `~/.hermes/profiles/<agen>/state.db` masing-masing. Writer `team_status.py` membaca keduanya.
- **Tiga endpoint Syncthing 404** di v1.29.5: `/rest/db/status`, `/rest/folder/status`. Yang benar: `/rest/db/completion?folder=workspace` (completion 100%, needItems 0).

## Status tim live (baru)

- **Writer tunggal:** `guardian/team_status.py` → `workspace/05-status/team.json`.
  Sumber: `state.db` (default + 9 profile), `cron/executions.db`, `cron/jobs.json`, `05-status/guardian.json`, `/proc` + `free` + `df`.
  Script Python biasa, **tanpa LLM** → nol token. Atomic write. Tidak menulis nama model/tier/credential.
- **Dashboard:** `guardian/dashboard/index.html` + `guardian/serve_status.py` (bind `127.0.0.1:9200`), systemd `team-status.service` (enabled).
  URL: `https://hermes.raminesia.com/team-status/` (basic auth, user `ical`).
- **Cron:** `guardian-team-status` (job id `f962e5af8ce3`), every 10m, `no_agent=true`.
- **Schema `team.json`:** `agents[]` (state, last_activity, sessions, messages, tokens), `jobs[]` (health), `gateway[]` (heartbeat), `cost{}` (OpenRouter), `system{}` (RAM/disk/load).
- Dashboard Hermes yang lama tetap jalan normal (302 ke `/login`).

## Catatan keselamatan

- Jangan reinstall Hermes.
- Jangan simpan secrets, token, password, atau runtime DB di workspace/repo.
- Jangan hapus probe sync tanpa persetujuan Cal.
- Jangan pakai `git add -A` di repo ini — path runtime tidak selalu bisa diprediksi dari `.gitignore` saja.
- Backup pra-commit: `/root/.hermes/backups/pre-selective-commit-20261101T193138Z/` (git bundle + tar workspace).
- Backup konsolidasi: `/root/.hermes/backups/ai-team-docs-preconsolidation-20261029/`.
