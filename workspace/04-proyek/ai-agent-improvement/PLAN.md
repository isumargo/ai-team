# Rencana kerja — Perbaikan AI Agent Hermes

## Tujuan

Satu canonical per jenis data, tanpa menghilangkan/merusak file yang masih dipakai Hermes, cron, Dashboard, Ruang, bot, atau kerja Adam.

## Prinsip keselamatan

- `~/.hermes/` adalah runtime: `state.db`, sessions, config dan credentials tetap di sana.
- Satu domain boleh memiliki runtime file dan dokumen penjelas, tetapi dokumen jelas sebagai dokumentasi, bukan salinan operasional.
- Hapus/migrasi hanya setelah consumers diperiksa, ada backup, test berhasil, dan Ical menyetujui cleanup final.
- Workspace Windows adalah mirror Syncthing; Git menyimpan riwayat. Jangan edit file yang sama bersamaan di dua sisi.
- Jangan push perubahan Guardian/sesi lain sebagai bagian cleanup tanpa review terpisah.

## Tahapan

### Fase 0 — baseline & akses kerja
- [x] Buat proyek dan handoff lintas sesi.
- [x] Inventaris awal environment, repo, profiles, services dan data.
- [x] Setup Syncthing VPS ↔ Windows.
- [x] Buat big picture Excalidraw/Markdown.
- [x] Buat `SOURCE-OF-TRUTH.md`.
- [ ] Validasi sync arah PC→VPS.

### Fase 1 — team policy (`TEAM-POLICY.md`) — **selesai**
- [x] Canonical `/root/ai-team/workspace/01-organisasi/policy/TEAM-POLICY.md` dibuat; SOP kuota #6 digabung.
- [x] Runtime compatibility copies `/root/AGENTS.md` dan `/root/.hermes/AGENTS.md` dihasilkan dari canonical; `sync_policy.py --check` lulus.
- [x] Hermes effective prompt diuji dengan `cwd=/root/.hermes`: policy dan Syncera SOP termuat.
- [ ] Profile-specific `~/.hermes/profiles/developer/AGENTS.md` diperiksa pada tahap role/persona, termasuk klaim model lama; belum diubah.
- [ ] Backup script masih backup generated `/root/AGENTS.md`; pertimbangkan backup canonical secara eksplisit pada perubahan terpisah.

### Fase 2 — preferensi pengguna (`USER.md`) — selesai
- [x] Canonical runtime: `~/.hermes/memories/USER.md`; loader uses Hermes memory folder.
- [x] Consolidated duplicate entries into one 968/1375-char entry; active prompt test passed.
- [x] Old root file retained as `/root/.hermes/USER.md.legacy-snapshot`; backup at `/root/.hermes/backups/USER.md.20261029T062415Z.bak`.
- [x] Stale shared workspace copy replaced with `workspace/01-organisasi/USER-PROFILE-AKTIF.md` read-only mirror.
- [ ] Later: adjust backup script's obsolete root USER.md reference; current backup already includes `~/.hermes/memories/`.

### Fase 3 — instruksi profil Developer + ROLE — selesai untuk konsolidasi awal
- [x] Ditemukan `~/.hermes/profiles/developer/AGENTS.md` dimuat Hermes saat CWD = profile, dan memiliki klaim model lama.
- [x] Sumber kanonik dibuat di `workspace/01-organisasi/policy/DEVELOPER-INSTRUCTIONS.md`; file runtime `AGENTS.md` jadi generated copy lewat `workspace/01-organisasi/policy/sync_policy.py`.
- [x] Role repo Developer menjadi metadata/pointer, bukan salinan persona/policy.
- [x] Hash check + prompt tests untuk default dan Developer pass.
- [ ] Standardisasi ROLE lain secara bertahap; sekarang hanya pointer policy umum ditambah isi domain/SOP yang masih berulang.

### Fase 4 — status dan reporting — audit awal
- [x] Found current writers: only `guardian/check_usage.py` actively writes `status/guardian.json`; others are stale/manual snapshots (17–19 Oct).
- [x] Installed Ruang source did not explicitly consume `/root/ai-team/status/*.json`; it reads Hermes runtime data/commands. Legacy memos/SOULs said agents should write status JSON.
- [x] Backed up the 5 stale JSON snapshots to `workspace/04-proyek/ai-agent-improvement/status-audit/archive-2026-10-29/` and removed them from the active `status/` directory (source `.json` files were archived, not destroyed).
- [x] Updated the 7 non-Guardian agent SOULs to stop asking agents to write manual status JSON; Guardian cost status remains its own operational metric.
- [ ] Decide/implement canonical live team-status view (prefer Hermes/Ruang runtime source; if user snapshot needed, generate timestamped derived report under `workspace/05-status/`).
- [ ] Keep Guardian cost fields in its operational reports; decide separately whether `status/guardian.json` is still required by any consumer.
- [ ] Do not purge archive or change Guardian writer until an end-to-end status view is tested.

### Fase 5 — dokumen dan workspace
- [x] `/root/ai-team/workspace/` ditetapkan sebagai canonical dokumen manusia; PC Syncthing sebagai mirror. Folder `projects/ai-agent-improvement/`, `memo/`, dan `policy/` di repo dihapus setelah verifikasi.
- [ ] Pindahkan memo/laporan/project docs per domain; old paths jadi pointer/arsip.
- [ ] Kode tetap di folder project; workspace hanya release/dokumen aman.
- [ ] Exclude secrets, DB aktif, venv, Hermes state dan cache dari Syncthing.

### Fase 6 — validasi, cleanup, handoff
- [ ] Audit duplicate canonical, stale pointers, broken path refs, secrets, sync errors.
- [ ] Jalankan health checks + `git diff --check`; review Guardian changes terpisah.
- [ ] Minta approval sebelum hapus salinan lama; archive + manifest.
- [ ] Update handoff/session log; commit terpilah dan push setelah review.

## Metode tiap migrasi

1. Inventaris sumber dan semua consumers.
2. Buat backup/checksum + diff.
3. Pilih canonical dan mekanisme transisi.
4. Ubah satu domain saja; jangan campur lintas domain.
5. Test jalur nyata/runtime + rollback.
6. Setelah lolos, tandai legacy sebagai pointer/arsip; penghapusan butuh persetujuan eksplisit.

## Belum boleh dilakukan

- Menghapus/mengganti AGENTS.md, USER.md, ROLE.md, SOUL.md, status JSON.
- Memindah `state.db`, sessions, `.env`, `auth.json`, DB aktif atau laporan operasional Guardian.
- Membuat sync dua arah ke file runtime Hermes.
- Push perubahan campuran sebelum memisahkan perubahan Guardian/task lain.


## Fase 6 - konsolidasi struktur (2026-10-29)

- [x] Semua dokumen kanonis dipindah ke `workspace/`: policy, memo, ROLE agen, dokumen proyek AI, dokumen bisnis distribusi.
- [x] `sync_policy.py` ditulis ulang: canonical di `workspace/01-organisasi/policy/`, empat target generated termasuk alias workspace; `--check` lulus.
- [x] Duplikat dihapus: `projects/ai-agent-improvement/`, `memo/`, `policy/`, salinan handoff/status di `workspace/01-organisasi/`, `workspace/04-proyek/distribusi/rencana/`, salinan peta ganda, arsip status ganda.
- [x] Folder output runtime (`agents/*/reports`, `auditor/reports`, `guardian/reports`, `projects/distribusi/reports|inbox`, `status/`) dipertahankan agar SOUL, script, dan job tidak rusak.
- [x] Backup pra-konsolidasi di `/root/.hermes/backups/ai-team-docs-preconsolidation-20261029/`.
- [ ] Migrasi output path laporan agen ke workspace (perlu koordinasi dengan SOUL + job Guardian).
- [ ] Guard `.gitignore` agar `.env`, DB, venv, dan file runtime tidak pernah masuk commit.
- [ ] Commit/push selektif setelah dipisah dari perubahan Guardian runtime.
