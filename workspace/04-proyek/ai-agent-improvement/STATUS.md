# Status — Perbaikan AI Agent

**Diperbarui:** 2026-10-29 (handoff sesi)
**Ringkasan:** Struktur dokumen dikonsolidasikan ke dalam workspace (satu sumber kanonis). Hermes tetap berjalan; tidak ada reinstall. Perubahan repo belum di-commit/push.

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

## Sedang / belum selesai

- Output path laporan agen/Guardian kini sudah dipindah ke workspace (bagian **Output agen & status** di HANDOFF). Job aktif menunjuk shim runtime.
- Tentukan desain tampilan status tim live dan sumber datanya.
- Pisahkan perubahan repo dari perubahan Guardian runtime yang tidak terkait, lalu commit/push selektif.
- Periksa status GUI Syncthing auth; GUI tetap hanya bind `127.0.0.1:8384` dan tidak boleh dibuka publik.
- Audit logic job Guardian (threshold/alert/backup/session monitor) tetap ditunda atas permintaan Cal; migrasi kali ini hanya mengubah lokasi output/path job.

## Ditunda atas permintaan Cal

- **Guardian:** review job, threshold, alert, backup scope, dan session monitor pada sesi khusus.
- **Django Distribusi (`distro.raminesia.com`, :8080):** perlu audit/perbaikan nanti; arah produk ialah web monitoring penjualan.
- **Ruang 3D (`mc.raminesia.com`, :3001):** perlu audit/perbaikan nanti; tujuannya Mission Control.
- Belum ada perubahan service, proses, atau firewall untuk dua aplikasi tersebut.

## Catatan keselamatan

- Jangan reinstall Hermes.
- Jangan simpan secrets, token, password, atau runtime DB di workspace/repo.
- Jangan hapus probe sync tanpa persetujuan Cal.
- Jangan push sebelum perubahan Guardian dipilah.
- Backup konsolidasi: `/root/.hermes/backups/ai-team-docs-preconsolidation-20261029/`.
