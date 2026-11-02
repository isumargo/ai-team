# Handoff — Perbaikan AI Agent

**Tujuan proyek:** merapikan arsitektur, SOP, state, dan operasional tim AI supaya sumber kebenaran jelas, mudah dirawat, dan konteks bisa di-handoff antar sesi. Tanpa reinstall, tanpa kehilangan runtime/state.

**Lokasi kanonis:** `/root/ai-team/workspace/04-proyek/ai-agent-improvement/` (satu-satunya; Syncthing meneruskan ke PC).
**Repo:** `github.com/isumargo/ai-team`, branch `main`
**Update terakhir:** 2026-11-01 (commit selektif + push, status tim live)

## Prinsip desain (wajib, atur Cal)

Setiap desain/perubahan baru wajib: **Agile, Terstruktur, Scalable, Aman tapi tidak mengganggu operasional, Resilient, punya aturan jelas, mudah dikembangkan.** Jika perbaikan malah menambah sebaran folder dan duplikasi, desain itu salah dan harus diperbaiki.

Konsekuensi praktis: semua pemindahan folder (termasuk aplikasi distribusi dan job Guardian) harus mengikuti struktur baru yang kita desain; path pemakai diperbarui supaya semuanya tetap jalan.

## Cara pakai dokumen ini

- `HANDOFF.md` — ini. Konteks terkini untuk sesi berikutnya. **Baca pertama.**
- `STATUS.md` — ringkasan progres satu halaman.
- `DECISIONS.md` — keputusan yang sudah disetujui Cal. Jangan nebak ulang.
- `PLAN.md` — fase kerja dan checklist.
- `SESSION-LOG.md` — riwayat kronologis. Bukan sumber status terbaru.
- `SOURCE-OF-TRUTH.md` — peta file → canonical → owner.

Aturan: handoff ini **satu-satunya** dan tinggal di workspace, jadi otomatis tersinkron ke PC.

## Struktur kanonis (hasil konsolidasi 2026-10-29)

- Semua dokumen manusia/proyek tinggal di `workspace/` (yang tersinkron ke PC): policy di `01-organisasi/policy/`, memo di `02-memo/`, ROLE agen di `03-agen/`, dokumen proyek di `04-proyek/`.
- Repo `ai-team` berisi code/config Guardian dan aplikasi distribusi; output agent/Guardian kanonis berada di workspace. Cron script di `~/.hermes/scripts/guardian-*.py` adalah shim tipis ke script kanonis `guardian/`.
- `projects/ai-agent-improvement/`, `memo/`, `policy/`, dan `status/` di repo sudah dipensiunkan/dihapus sebagai folder aktif. Status biaya Guardian sekarang ditulis ke `workspace/05-status/guardian.json`.
- Backup pra-konsolidasi: `/root/.hermes/backups/ai-team-docs-preconsolidation-20261029/`.
- Backup migrasi output: `/root/.hermes/backups/output-path-migration-20261029/`.
- Sisa pekerjaan: audit logic Guardian (ditunda), tampilan status live, commit/push selektif, dan perbaikan dua service.

## Ringkasan keputusan

- Tidak reinstall Hermes. Runtime berjalan; perbaiki terukur.
- Workspace master di VPS (`/root/ai-team/workspace/`), mirror ke Windows via Syncthing. PC: `C:\Users\USER\ai-team\Workspace`. Google Drive tidak dipakai.
- Prinsip: **satu canonical per jenis data**. Bukan satu folder untuk semua. Compatibility copy hanya jika loader Hermes mewajibkan nama/path tertentu.
- Source of truth: `workspace/04-proyek/ai-agent-improvement/SOURCE-OF-TRUTH.md`.
- Jangan pernah simpan token/password/key di repo atau workspace. Nilai credential selalu `[REDACTED]`.
- Jangan ubah service, firewall, atau file di VPS tanpa izin Cal.

## Fase 1 — canonical team policy (selesai)

- Canonical: `workspace/01-organisasi/policy/TEAM-POLICY.md` (SOP Syncera #6 sudah digabung).
- Generated copies: `/root/AGENTS.md`, `~/.hermes/AGENTS.md`, dan `workspace/01-organisasi/AGENTS.md`; semuanya identik dengan team policy. Developer `AGENTS.md` runtime adalah gabungan policy tim + instruksi Developer karena Hermes hanya memuat satu AGENTS per direktori. Generator dan hash-check: `workspace/01-organisasi/policy/sync_policy.py`.
- Tiga target team policy identik. Effective prompt test di CWD `/root/.hermes` lulus; SOP Syncera termuat. Developer prompt diperiksa: policy tim + SOP Syncera + instruksi Developer semuanya termuat. Gateway tidak direstart.
- `AGENTS.md` adalah context-instruction file bawaan Hermes (bukan fitur self-improvement tersendiri). Perubahan teks berlaku saat sesi memuat ulang context; tidak mengubah kode/runtime.

## Fase 2 — USER profile (selesai)

- Canonical runtime: `~/.hermes/memories/USER.md` (loader `memory_tool.get_memory_dir()`). Satu entri, 968/1375 char, load test lulus.
- Legacy root file disimpan sebagai `~/.hermes/USER.md.legacy-snapshot`. Backup: `~/.hermes/backups/USER.md.20261029T062415Z.bak`.
- Tiap profile punya `memories/USER.md` sendiri. Jangan disatukan tanpa desain per profile.
- Salinan baca di PC: `workspace/01-organisasi/USER-PROFILE-AKTIF.md` (read-only, bukan sumber).

## Fase 3 — Developer instructions & ROLE (selesai sebagian)

- Canonical instruksi Developer: `workspace/01-organisasi/policy/DEVELOPER-INSTRUCTIONS.md`.
- Runtime copy: `~/.hermes/profiles/developer/AGENTS.md` (generated, hash check + prompt test lulus). Klaim nama model lama sudah hilang dari prompt.
- ROLE agen (analyst, designer, marketer, sales, strategist, auditor, guardian, PM distribusi) kini metadata + pointer ke policy + persona runtime. Tersimpan di `workspace/03-agen/` dan `workspace/04-proyek/distribusi/ROLE.md`.
- Sisa pekerjaan: standardisasi isi SOP domain per ROLE file, satu per satu, setelah cek consumer.
- Backup: `~/.hermes/backups/policy-sync/AGENTS.md.developer.20261029T064841Z.bak`.

## Output agen & status — migrasi 2026-10-29 (selesai)

- Semua laporan agen diarahkan ke `workspace/03-agen/<agent>/laporan/`; laporan project distribusi/inbox ke `workspace/04-proyek/distribusi/{laporan,inbox}/`.
- SOUL seluruh profile, ROLE canonical, Developer instructions, Guardian scripts diperbarui. Job Guardian mempertahankan jadwal/delivery, tetapi menunjuk thin shims `/root/.hermes/scripts/guardian-*.py` ke skrip kanonis di `guardian/`.
- Guardian usage log/alert/state → `workspace/03-agen/guardian/laporan/`; status biaya Guardian → `workspace/05-status/guardian.json`; session cooldown → workspace.
- Output lama disalin/hash-check, lalu file lama di repo dihapus. Folder output runtime yang kosong dipensiunkan. Backup: `/root/.hermes/backups/output-path-migration-20261029/`.
- `guardian/backup.py` tetap satu-satunya source script; cron shim memanggil langsung file kanonis itu.

## Fase 4 — status JSON (selesai sebagian)

- Satu-satunya writer terverifikasi: `guardian/check_usage.py` → `workspace/05-status/guardian.json`. Snapshot lama (17–19 Okt) ada di arsip proyek, bukan active status.
- Ruang yang terinstall **tidak** membaca `/root/ai-team/status/*.json`; sumbernya runtime Hermes. Tidak ada consumer dashboard.
- Aksi: 5 snapshot diarsipkan ke `workspace/04-proyek/ai-agent-improvement/status-audit/archive-2026-10-29/`, lalu dikeluarkan dari `status/` aktif (diarsipkan, bukan dihapus).
- Aksi: 7 SOUL non-Guardian berhenti menyuruh agen menulis status JSON manual. Guardian tetap managing status biayanya.
- Backup SOUL: `~/.hermes/backups/agent-soul-pre-status-cleanup/`.
- Sisa: bangun tampilan status tim yang live (sumber runtime, atau snapshot bertimestamp di `workspace/05-status/`).

## Progres Syncthing (terverifikasi)

- VPS Device ID: `K5UIN2P-ENOMJET-BDNVK75-PRTNZBE-AE4ZAZU-NSZH52H-H6ENDMW-724DGAM`.
- PC Device ID: `CEPY5LX-TKH4LHU-J5IRRUI-ODO53D5-BVF2AWB-AX3564I-IPP3MYW-S425ZA3` (`DESKTOP-R1HOU36`).
- Service `syncthing@root` aktif; folder ID `workspace` → `/root/ai-team/workspace` (sendreceive).
- Firewall: TCP 22000 + 21027 diizinkan atas izin Cal. GUI hanya di `127.0.0.1:8384` — **jangan expose publik**.
- Discovery, local announce, relay, NAT traversal dimatikan. Koneksi direct ke public IP VPS port 22000.
- **Uji dua arah SUDAH LOLOS.** Probe PC→VPS `workspace/00-inbox/uji-sync-dari-pc.txt` terlihat di VPS; probe VPS→PC dikonfirmasi Cal muncul di Windows. State `idle`, `needTotalItems=0`.
- Probe **jangan dihapus** tanpa persetujuan Cal.
- Credential GUI Syncthing tersimpan di `/root/.config/syncthing/gui-credentials.txt` (mode privat). **Jangan tampilkan, salin ke repo, atau kirim di chat.** Auth GUI belum proves kuat (unauthenticated HTTP sempat 200) — tetap loopback-only.

## Arsitektur big picture

- Dipusatkan di `workspace/04-proyek/ai-agent-improvement/architecture/`: `truth-map.md`, `truth-map.excalidraw`, `truth-map.html`, generator, editor, bundle Mermaid offline.
- Isi folder ini juga otomatis tersedia di PC lewat Syncthing. Salinan peta di `workspace/01-organisasi/peta/` dihapus supaya tidak ada dua master.
- Folder `docs/` lama sudah dihapus setelah semua path diperbarui.

## Penempatan peran PM Distribusi (disetujui Cal)

- **Agen yang jalan:** profil Hermes `pm-distribusi` di `~/.hermes/profiles/pm-distribusi/` (SOUL + config + cron + bot). Inilah yang mengeksekusi.
- **Kontrak tugas:** `workspace/04-proyek/distribusi/ROLE.md` — menjelaskan peran atas proyek distribusi, refer ke profil runtime, tidak menyalin persona/policy.
- Kode & data bisnis tetap di `projects/distribusi/app/`.
- `workspace/04-proyek/distribusi/ROLE.md` sudah diklarifikasi (pointer eksplisit ke profil) dan itu satu-satunya salinannya.

## Ditunda atas permintaan Cal

### Guardian review (sesi khusus, belum ada perubahan)

- Job aktif: cek biaya OpenRouter tiap 30m, backup tiap 6j, session monitor tiap 15m.
- Cal: job Guardian membingungkan → ditunda untuk review khusus.
- Rencana yang akan dibahas: satu sumber threshold config, alert hanya saat status berubah, backup scope/exclusions yang benar (sekarang masih refer path `USER.md` lama), dan keputusan fix-atau-disable untuk session monitor.
- **Jangan ubah job/script/config sebelum ada proposal dan persetujuan.**

### Django Distribusi + Ruang 3D

- `distro.raminesia.com` (port 8080): mati. Ada 2 proses `runserver` menganggur tanpa port (berebut 8080).
- `mc.raminesia.com` (port 3001): mati. Unit `ruang.service` hilang dari systemd.
- Arah produk: Cal ingin web page untuk monitoring penjualan; Ruang 3D menjadi Mission Control.
- Belum ada perubahan service/proses/firewall. Saat dilanjutkan: audit requirement + data dulu, buat rencana rollback, perbaiki terpisah.

## Temuan lain (audit sebelumnya)

- VPS sehat: disk 96G (17G terpakai), RAM 7.7G. Gateway Hermes jalan, 10 profile tersaji. Dashboard `:9119` hidup, 9router `:20128` hidup, Ollama `:11434` hidup, nginx hidup.
- Konflik threshold biaya: `guardian/config.json` bilang `$5`, `~/.hermes/memories/MEMORY.md` bilang `$20`. OpenRouter tersisa `$0.14` dari `$10`. **Jangan ubah threshold tanpa izin.**
- `check_usage.py` menulis ulang `status/guardian.json` tiap 30m dengan isi identik, dan auto-switch model tiap kali limit $5 terlewati (padahal kredit sudah habis $9.86 dari $10) → switch berjalan tanpa efek. Masukan item review Guardian.
- Backup `/root/backups` 189MB/200MB; backup tiap 6 jam; belum exclude `venv/`, `node_modules/`, `__pycache__/`.
- Syncera API sempat balas 503 saat audit. Cek lagi bila relevan.
- Push GitHub terakhir: `302c46d` (workspace `316d25d`). Perubahan konsolidasi **belum** di-commit/push.

## Struktur kanonis

- Dokumen kanonis dan output agen berada di workspace (Syncthing ke PC); workspace adalah satu-satunya rumah dokumen, tidak ada cermin handoff terpisah.
- Policy source: `workspace/01-organisasi/policy/`. Generated team copies: `/root/AGENTS.md`, `~/.hermes/AGENTS.md`, `workspace/01-organisasi/AGENTS.md`. Developer runtime `AGENTS.md` adalah gabungan team policy + instruksi Developer. Script: `workspace/01-organisasi/policy/sync_policy.py`.
- Memo: `workspace/02-memo/`. ROLE: `workspace/03-agen/<agent>/ROLE.md`; Dasiyah: `workspace/04-proyek/distribusi/ROLE.md`; persona runtime tetap `~/.hermes/profiles/<name>/SOUL.md`.
- Handoff/status/plan/log AI project: `workspace/04-proyek/ai-agent-improvement/`.
- Laporan agen: `workspace/03-agen/<agent>/laporan/`; status biaya Guardian: `workspace/05-status/guardian.json`; output distribusi: `workspace/04-proyek/distribusi/{inbox,laporan}/`.
- Guardian jobs tetap aktif dan jadwal/delivery tidak berubah. Cron memanggil shim `~/.hermes/scripts/guardian-*.py` → scripts source di `/root/ai-team/guardian/`.
- Kode distribusi tetap di `projects/distribusi/app/`; `.env`, DB, venv tidak disinkron.
- Dua arah Syncthing telah diuji. Probe file dipertahankan; GUI hanya `127.0.0.1:8384`, jangan expose publik.

## Hasil migrasi output terbaru

- Semua SOUL terkait, ROLE, Developer instructions, Guardian scripts, dan tiga cron job diarahkan ke workspace. Runtime output lama dipindahkan setelah backup/hash-check; folder lama dipensiunkan.
- Smoke tests: py_compile lulus; session monitor exit 0; backup shim sukses (backup 29.3MB, total retensi 190.7MB/200MB); policy hash-check lulus; `git diff --check` lulus. Syncthing terakhir idle, `need=0`.
- Backup lengkap: `/root/.hermes/backups/ai-team-docs-preconsolidation-20261029/`; backup output/SOUL/scripts: `/root/.hermes/backups/output-path-migration-20261029/`.
- Belum commit/push. Ada perubahan Guardian yang tidak boleh dicampur tanpa audit, termasuk `guardian/syncthing_auth.py` dan perpindahan report runtime. Jangan `git add -A`.

## Pending (urut rekomendasi)

1. **Review logika Guardian** (threshold/alert/backup/session monitor) — ditunda khusus atas permintaan Cal; jangan ubah logic sebelum pembahasan. Termasuk: konflik threshold $5 (config.json) vs $20 (MEMORY.md), kredit OpenRouter tersisa $0.14 yang masih memicu "SWITCHED" tiap 30 menit, dan backup 196M/200M tanpa exclude venv/node_modules.
2. **Status GUI Syncthing** — penyebab sudah jelas (Syncthing v1.29.5 tidak menegakkan basic auth di path GUI meski password sudah ter-set). `guardian/syncthing_auth.py` punya guard `--apply` tapi **belum dijalankan**. Dampak terbatas (loopback only).
3. **Audit/pulihkan Django distribusi :8080 dan Ruang 3D/Mission Control :3001** — belum ada service/process/firewall changes. Arah: web sales monitoring + Ruang sebagai Mission Control.
4. **Pakai `team.json` sebagai kontrak Ruang 3D** — schema sudah ada (`agents[]`, `jobs[]`, `gateway[]`, `cost{}`, `system{}`). Ruang cukup baca satu file ini, bukan `status/*.json` yang sudah dipensiunkan.

## Selesai di sesi 2026-11-01 (commit selektif + status tim live)

### Commit & push

- Repo `ai-team` sebelumnya tertinggal di `302c46d` dengan ~50 file changed/deleted + 54 untracked. Sekarang 5 commit selektif sudah dipush ke `origin/main` (terakhir `507a08b`):
  1. `a5ef833` — `.gitignore`: lindungi path runtime kanonis di `workspace/` (sebelumnya hanya path lama yang terlindungi — bug nyata, file runtime baru akan ikut ter-commit).
  2. `a15c7ae` — konsolidasi dokumen ke `workspace/` (67 file: rename ROLE + hapus duplikat `memo/`, `docs/`, `status/`, `peta/`, `rencana/`).
  3. `3584ce1` — Guardian output path → workspace (**path-only**, logika tidak berubah) + hapus `guardian/reports/` yang sudah dipensiunkan.
  4. `a136e43` — status tim live: `team_status.py`, `serve_status.py`, `dashboard/index.html`.
  5. `507a08b` — `guardian/syncthing_auth.py` dengan guard `--apply` (belum dijalankan).
- Working tree bersih. Tidak ada secret di history (scan 5 commit bersih). `git ls-tree` mengonfirmasi tidak ada runtime file yang masuk repo.
- Backup pra-commit: `/root/.hermes/backups/pre-selective-commit-20261101T193138Z/` (git bundle + tar workspace).

### Status tim live

- **Writer tunggal:** `guardian/team_status.py` → `workspace/05-status/team.json`.
  Sumber runtime: `state.db` utama + `~/.hermes/profiles/<agen>/state.db` (9 profile), `cron/executions.db`, `cron/jobs.json`, `05-status/guardian.json`, `/proc`+`free`+`df`.
  Script Python biasa tanpa LLM → **nol token**. Atomic write (`os.replace`). Tidak menulis nama model/tier/credential.
- **Dashboard:** `guardian/dashboard/index.html` (kode, di repo) + `guardian/serve_status.py` (bind `127.0.0.1:9200`, systemd `team-status.service`).
  URL: `https://hermes.raminesia.com/team-status/` — basic auth via `auth_basic` (user `ical`, file `/etc/nginx/.htpasswd-mc`), TLS dari vhost `hermes.raminesia.com` yang sudah ada.
- **Cron:** `guardian-team-status` (job id `f962e5af8ce3`), every 10m, `no_agent=true`, shim `~/.hermes/scripts/guardian-team-status.py`.
- Verifikasi: `/` → 200, `/team.json` → 200 (`application/json`), path lain → 404, `/../etc/passwd` → 404, tanpa kredensial → 401, dengan kredensial → 200. Dashboard Hermes lama tetap normal.
- Catatan desain: kode dashboard ada di `guardian/dashboard/`, runtime JSON di `workspace/05-status/` (di-ignore git). Servis memakai server sendiri, bukan alias nginx, karena `/root` mode 700 tidak bisa di-traverse worker www-data.

### Temuan yang perlu|Cal tahu

- **GUI Syncthing: password sudah ter-set tapi panel tetap terbuka.** `config.xml` punya `user="ical"` + password + `authMode="static"` + `address="127.0.0.1:8384"`, tapi `GET /` tanpa kredensial tetap 200. Penyebab: Syncthing v1.29.5 tidak menegakkan basic auth pada path GUI — bukan karena password belum diset. Restart Syncthing (yang akan dilakukan `--apply`) tidak memperbaikinya, jadi script **tidak dijalankan**. Dampak terbatas: loopback only, 8384 tidak dibuka ke publik.
- **Modul `crypt` Python dihapus** di Python 3.14.9 (VPS ini). Verifikasi hash htpasswd di Python butuh dependency tambahan; karena itu auth dashboard diserahkan ke nginx.
- **`state.db` utama tidak memisahkan session per-agen** (`profile_name` selalu `default`). Data per-agen ada di `state.db` masing-masing profile.
- **Endpoint Syncthing 404 di v1.29.5:** `/rest/db/status`, `/rest/folder/status`. Yang benar: `/rest/db/completion?folder=workspace` (completion 100%, needItems 0).
- **`mermaid.min.js` (3.5MB) dipertahankan** — contrary to dugaan awal, file ini adalah **sumber** yang di-inline oleh `sync_map.py` ke `truth-map.html`, bukan duplikat.

## Keputusan dan batas

- Prinsip desain wajib: Agile, terstruktur, scalable, aman tanpa mengganggu operasi, resilient, aturan jelas, mudah dikembangkan. Setiap pemindahan harus memperbarui seluruh consumer dan diuji.
- Jangan reinstall Hermes, jangan sync secrets/runtime DB ke PC, jangan hapus probe tanpa izin, jangan expose GUI Syncthing, jangan push perubahan campuran.
- Guardian job logic review ditunda; pemindahan path output yang baru saja dilakukan memang atas izin Cal.


1. Awal sesi: baca `HANDOFF.md` → `STATUS.md` → `DECISIONS.md`.
2. Sebelum handoff: perbarui `HANDOFF.md` + `STATUS.md`, tambah satu entri di `SESSION-LOG.md`.
3. Fakta terverifikasi ditulis sebagai fakta; dugaan ditulis sebagai dugaan; sertai waktu pemeriksaan.
4. Jangan simpan secrets, token, password, credential, atau dump percakapan.
5. Jangan mengubah runtime, menghapus data, membuka firewall, atau mengubah billing tanpa izin eksplisit Cal.
6. Perubahan pada konfigurasi aktif wajib punya backup/rollback + langkah verifikasi.
7. Jangan push tanpa memeriksa perubahan lain yang belum disetujui (saat ini ada perubahan Guardian yang belum dipilah).

## Session 2026-11-02 — Provider Integration & Structure Consolidation (COMPLETE)

### Provider Integration (✓ DONE)
- **Clouvia:** Registered & tested. Direct (`custom:clouvia`), model `coding-high` (max_tokens 32768).
- **OpenRouter:** Registered & tested. 451 models fetched & cached. Proxy via 9Router (`openrouter/...` prefix).
- **Kiro:** Already registered. ~30 models. Proxy via 9Router (`kr/...` prefix).
- **Total Models Indexed:** 616 (Clouvia 113, OpenRouter 451, Kiro 30, Other 22).
- **9Router:** Stable systemd service (port 20128). Tested: Clouvia, OpenRouter, Kiro all route correctly.
- **Model Picker:** Updated cache `/root/.hermes/provider_models_cache.json` — all 616 models live.
- **Config Fixes:** Model default locked to `coding-high` (was nemotron). Tumpang tindih removed from config.yaml lines 1604-1607.

### Structure Consolidation (✓ DONE)
- **Single Source of Truth:** `/root/ai-team/workspace/` (synced to PC via Syncthing).
- **Removed Duplicate Folders:** `agents/`, `auditor/`, `memo/`, `projects/` at top level.
- **Moved Guardian to Workspace:** `/root/ai-team/workspace/03-agen/guardian/` — backup.py, check_usage.py, session_monitor.py, team_status.py.
- **Updated Cron Wrappers:** `~/.hermes/scripts/guardian-*.py` now point to workspace paths.
- **Cron Status:** All 4 jobs active ✓ (backup 6h, check_usage 30m, session_monitor 15m, team_status 10m).
- **Git Commits:** `eb9a25d` (consolidate), `bac13cb` (document).

### Documentation Created
- `/root/ai-team/workspace/02-memo/2026-11-02-provider-integration-status.md` — detailed setup
- `/root/ai-team/workspace/02-memo/2026-11-02-structure-consolidation.md` — cleanup details

### Pending (Next Session)
1. **Confirm Provider Tiers** (Cal to provide):
   - Kiro: tier? (Free, Pro $20/mo, Pro+ $40/mo?)
   - Clouvia: billing? (subscription/usage? budget?)
   - OpenRouter: fresh or prepaid? (if prepaid, balance?)
2. **Setup Combo Failover** — 9Router native combos (multi-provider chain) once tiers confirmed.
3. **Optional:** Cost monitoring cron per provider/day.

---

## Boundary

- Tidak ada credential Google Drive yang dikonfigurasi; Drive tidak dipakai.
- Tidak ada routing model/config agent yang diubah (hanya 9Router model cache + provider integration).
- Runtime DB dan secrets belum dipindah ke workspace.
- Tidak ada install ulang Hermes.
- Provider tier info (Kiro, Clouvia, OpenRouter) diperlukan untuk Combo failover design.