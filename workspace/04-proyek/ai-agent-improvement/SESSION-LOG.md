# Session log

## 2026-10-28
- Audit awal: Hermes gateway aktif, 10 profile; dua aplikasi web mati; disk/RAM sehat.
- Bikin `docs/truth-map.md`, `.excalidraw`, HTML editor dan uploader/share link; diagram terenkripsi di Excalidraw dan round-trip diverifikasi.
- Workspace VPS dibuat: `workspace/`; struktur dan file awal di-commit/push (`316d25d`, backlog memo/status berikutnya di `302c46d`).
- Pairing Syncthing selesai dengan device PC `CEPY5LX-...`; koneksi TCP direct, TLS 1.3, folder workspace idle dan 100% tersinkron.
- File uji VPS → PC muncul di Windows. Sync otomatis real-time saat dua device aktif (watcher 2s + rescan 1 jam).
- PC→VPS belum dites; menunggu file `00-inbox/uji-sync-dari-pc.txt`.
- Peta sumber kebenaran selesai sebagai **usulan**: `SOURCE-OF-TRUTH.md`; ringkasan sudah di workspace. Belum ada runtime file/policy lama dipindah atau dihapus.
- Rencana diperbarui: mulai Fase 1 `AGENTS.md` (diff dua dokumen + inventaris consumers → backup → satu canonical/mekanisme kompatibel → verifikasi). Belum mulai edit policy.
- Tunggu arahan Cal untuk lanjut urutan Fase 1; jangan melanjutkan ke USER/ROLE/status sebelum policy aman dan terdokumentasi.

## 2026-10-29 (lanjutan)
- Ical setuju gabung SOP Syncera; canonical policy dibuat `workspace/01-organisasi/policy/TEAM-POLICY.md` + generator `sync_policy_v2.py`; salinan generated `/root/AGENTS.md` dan `~/.hermes/AGENTS.md`; hash semua cocok; effective prompt test lulus.
- Fase 2 USER selesai: file aktif `~/.hermes/memories/USER.md` dikonsolidasi (satu entri 968/1375 char, 0 duplikat, aturan approval/LULUS/model tetap dimuat, lulus format_for_system_prompt).
- `/root/.hermes/USER.md` legacy snapshot direname ke `~/.hermes/USER.md.legacy-snapshot`; isi lama tidak diubah, tapi perubahan ini reversibel. Backup runtime dibuat di `~/.hermes/backups/USER.md.20261029T062415Z.bak`.
- Workspace sebelumnya punya salinan lama `01-organisasi/USER.md`; salinan stale dihapus dari workspace (canonical di `memories/USER.md`), lalu salinan aktif yang read-only-minded `USER-PROFILE-AKTIF.md` disalin untuk dibaca di PC. Workspace file bukan runtime source.

## 2026-10-29 (lanjutan 2)
- Developer profile: canonical `workspace/01-organisasi/policy/DEVELOPER-INSTRUCTIONS.md` dibuat; runtime copy `/root/.hermes/profiles/developer/AGENTS.md` digenerate (`sync_policy.py`), klaim model lama hilang dari prompt; `developer/ROLE.md` jadi metadata + pointer.
- ROLE agen lain kini punya pointer ke persona runtime + policy umum (isi SOP domain masih di ROLE; standardisasi lanjutan menyusul).
- Fase 4 mulai: hanya `check_usage.py` yang menulis `status/guardian.json`; tidak ditemukan consumer lain. Snapshot basi 5 JSON diarsipkan ke `workspace/04-proyek/ai-agent-improvement/status-audit/archive-2026-10-29/` lalu dihapus dari `status/` aktif.
- 7 SOUL non-Guardian diedit agar berhenti menyuruh agen menulis status JSON manual (backup sebelum edit di `/root/.hermes/backups/agent-soul-pre-status-cleanup/`).
- Guardian SOUL masih menyebut path status — dibiarkan karena Guardian memang penulis status biaya; pertimbangkan pembersihan terpisah.

- 2026-10-29 — Semua output laporan agen dipindah ke workspace (SOUL + ROLE + Developer canonical/runtime diperbarui). Guardian usage/status/cooldown scripts dialihkan ke workspace; cron jobs tetap aktif dan kini memakai shim di `~/.hermes/scripts/guardian-*.py` ke script kanonis repo. Jadwal/delivery tidak berubah. Backup sebelum migrasi: `/root/.hermes/backups/output-path-migration-20261029/`.
- Verifikasi: Python compile lulus; session-monitor smoke test exit 0/no alert; backup cron shim sukses menghasilkan backup 29.3MB dan retention tetap <200MB; hash policy sync lulus; old output directories kosong/removed. `git diff --check` lulus.
- Perubahan belum di-commit/push. `guardian/syncthing_auth.py` dan beberapa Guardian report changes belum dipilah; jangan `git add -A`.
- Tidak ada perubahan logic Guardian (threshold/alert behavior/session monitor thresholds) atau konfigurasi service/firewall.
- File uji dari PC `workspace/00-inbox/uji-sync-dari-pc.txt` terlihat di VPS; Syncthing state idle, tidak ada item tertunda, koneksi PC aktif. Uji dua arah tuntas; probe dipertahankan.
- Ditambahkan penjelasan eksplisit ke `projects/distribusi/ROLE.md` bahwa profile Hermes `pm-distribusi` menjalankan agen; ROLE hanya menjelaskan tugas proyek. Mirror diperbarui di `workspace/04-proyek/distribusi/ROLE.md`.
- Cal meminta review Guardian dan perbaikan Django Distribusi/Ruang 3D ditunda; arah: web monitoring penjualan dan Ruang sebagai Mission Control. Belum ada perubahan job atau service.
- Handoff dan mirror workspace diperbarui; `git diff --check` lulus. Belum commit/push.


## 2026-10-29 (konsolidasi struktur)
- Prinsip desain dicatat di DECISIONS.md: Agile, terstruktur, scalable, aman tanpa mengganggu operasional, resilient, aturan jelas, mudah dikembangkan.
- Semua dokumen kanonis dikonsolidasi ke `workspace/` (policy, memo, ROLE, proyek AI, dokumen distribusi). Repo sekarang hanya kode + job.
- `sync_policy.py` ditulis ulang dengan canonical di `workspace/01-organisasi/policy/`; target generated: `/root/AGENTS.md`, `~/.hermes/AGENTS.md`, `workspace/01-organisasi/AGENTS.md`, `~/.hermes/profiles/developer/AGENTS.md`. Hash-check lulus.
- Folder repo `projects/ai-agent-improvement/`, `memo/`, `policy/` dihapus (duplikat). Backup: `/root/.hermes/backups/ai-team-docs-preconsolidation-20261029/`.
- Folder output runtime dipertahankan: `agents/*/reports`, `auditor/reports`, `guardian/reports`, `projects/distribusi/reports|inbox`, `status/` (Guardian menulis `status/guardian.json`).
- Scan duplikasi akhir: hanya `__init__.py` Django yang sama nama (fungsi berbeda, bukan duplikat).
- SOURCE-OF-TRUTH.md ditulis ulang mengikuti struktur final.


## Handoff sesi — 2026-10-29
- Cal minta context diringkas untuk sesi selanjutnya.
- Handoff diringkas pada bagian `Struktur kanonis`, `Hasil migrasi output terbaru`, `Pending`, dan `Keputusan dan batas`; sumber utama tetap file ini di workspace.
- STATUS diselaraskan dengan output-path migration yang selesai; Guardian logic review tetap ditunda.
- Belum ada commit/push.

## 2026-11-01 — Commit selektif + status tim live
- Cal menyetujui: kerjakan yang terbaik, dokumentasikan.
- **Audit repo** (sebelum commit): 54 file untracked, ~50 changed/deleted, repo tertinggal di `302c46d` sejak 23 Okt. Secret scan 54 file baru: bersih.
- **Bug ditemukan di `.gitignore`**: hanya path runtime LAMA yang dilindungi (`status/`, `guardian/reports/`, `agents/*/reports/`). Output Guardian sudah pindah ke `workspace/` sejak 29 Okt, jadi file runtime baru (`usage-log.json`, `usage-alert.md`, `alert-state.json`, `session-alert-cooldown.json`, `05-status/guardian.json`) tidak terlindungi. `usage-log.json` nambah tiap 30 menit → working tree akan dirty terus. Diperbaiki di commit `a5ef833`; `workspace/00-inbox/` juga di-ignore (probe Syncthing, jangan dihapus tanpa izin Cal).
- **Cek `mermaid.min.js` (3.5MB)**: contrary to dugaan awal (duplikat), file ini adalah **sumber** yang di-inline oleh `sync_map.py` ke `truth-map.html` (konfirmasi: `MERMAID_JS` dibaca lalu masuk ke `<script>__MERMAID_JS__</script>`). Dipertahankan.
- **5 commit selektif** (bukan `git add -A`): `a5ef833` gitignore → `a15c7ae` konsolidasi dokumen (67 file) → `3584ce1` Guardian path-only → `a136e43` status tim live → `507a08b` syncthing_auth. Push ke `origin/main` sukses (`302c46d..507a08b`).
- **Verifikasi Guardian path-only**: diff `check_usage.py` = 3 baris (REPORT_DIR, status_file, mkdir parents); `session_monitor.py` = 1 baris (COOLDOWN_FILE). Tidak ada perubahan threshold/limit/alert behavior. Review logika Guardian **tidak** ikut terbawa — sesuai penundaan Cal.
- **Status tim live dibangun** (sebelumnya tidak ada sama sekali; folder `status/` lama berisi 5 dari 9 agen dan semuanya basi 17 Okt, sudah diarsipkan 29 Okt):
  - `guardian/team_status.py` — writer tunggal, script Python tanpa LLM (nol token), atomic write ke `workspace/05-status/team.json`. Sumber: `state.db` utama + 9 `profiles/*/state.db`, `cron/executions.db`, `cron/jobs.json`, `05-status/guardian.json`, `/proc`+`free`+`df`.
  - `guardian/dashboard/index.html` + `guardian/serve_status.py` (loopback:9200) + systemd `team-status.service`.
  - Cron `guardian-team-status` (id `f962e5af8ce3`), every 10m, `no_agent=true`, shim `~/.hermes/scripts/guardian-team-status.py`.
  - URL: `https://hermes.raminesia.com/team-status/` (basic auth, htpasswd-mc; TLS dari vhost Hermes yang sudah ada). Subdomain baru tidak dipakai karena DNS `status.raminesia.com` belum ada.
  - Verifikasi: `/`→200, `/team.json`→200, path lain→404, `/../etc/passwd`→404, tanpa kredensial→401, dengan kredensial→200 (user uji sementara, lalu dihapus). Dashboard Hermes lama tetap 302→/login.
- **Bug auth Syncthing ditemukan**: `config.xml` sudah punya `user="ical"` + password + `authMode="static"` + `address="127.0.0.1:8384"`, tapi `GET /` tanpa kredensial tetap HTTP 200. Penyebab bukan "password belum diset" tapi Syncthing v1.29.5 tidak menegakkan basic auth pada path GUI. Dampak terbatas (loopback, 8384 tidak dibuka publik). `guardian/syncthing_auth.py` diberi guard `--apply` (default dry-run) tapi **tidak dijalankan** — restart Syncthing tidak memperbaiki masalah ini.
- **Catatan teknis**: modul `crypt` Python dihapus di Python 3.14.9 (VPS ini) → verifikasi hash htpasswd di Python butuh dependency tambahan; auth dashboard diserahkan ke nginx (`auth_basic`) seperti vhost `distro`/`mission-control`. `state.db` utama tidak memisahkan session per-agen (`profile_name` selalu `default`); data per-agen ada di `profiles/*/state.db`. Endpoint `/rest/db/status` & `/rest/folder/status` 404 di Syncthing v1.29.5; yang benar `/rest/db/completion?folder=workspace` (completion 100%, needItems 0).
- **Backup**: `/root/.hermes/backups/pre-selective-commit-20261101T193138Z/` (git bundle + tar workspace).
- Working tree bersih. Tidak ada perubahan service/firewall untuk Django Distribusi atau Ruang 3D. Logika Guardian, threshold, dan billing tidak diubah.
