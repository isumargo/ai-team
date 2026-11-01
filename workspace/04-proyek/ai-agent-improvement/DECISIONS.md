# Keputusan proyek

| Tanggal | Keputusan | Status |
|---|---|---|
| 2026-11-01 | **Commit selektif, bukan `git add -A`.** 5 commit terpisah (gitignore → dokumen → Guardian path → status tim → syncthing_auth), lalu push. Alasannya: `.gitignore` hanya melindungi path runtime LAMA, sedangkan output Guardian sudah pindah ke `workspace/` — file runtime baru akan ikut ter-commit dan membuat working tree dirty terus | Diterapkan; push `507a08b`, working tree bersih |
| 2026-11-01 | **Runtime JSON tidak masuk repo.** `workspace/05-status/`, `workspace/03-agen/guardian/laporan/*.json|md` runtime, dan `workspace/00-inbox/` di-ignore. File statis (laporan, SOP, arsip) tetap masuk repo | Diterapkan; diverifikasi `git check-ignore` + `git ls-tree` |
| 2026-11-01 | **Status tim live dibangun dengan satu writer.** `guardian/team_status.py` (script, nol token) → satu file `workspace/05-status/team.json`. Tidak ada lagi agent yang menulis status manual. Dashboard web membaca file yang sama | Diterapkan; cron `guardian-team-status` every 10m |
| 2026-11-01 | **Dashboard status tim disajikan di `https://hermes.raminesia.com/team-status/`** (path di vhost Hermes yang sudah ada + TLS), auth basic via `auth_basic` seperti vhost `distro`/`mission-control`. Tidak menambah subdomain baru karena DNS `status.raminesia.com` belum ada | Diterapkan; 401 tanpa kredensial, 200 dengan kredensial |
| 2026-11-01 | **Kode dashboard di repo, runtime JSON di workspace.** `guardian/dashboard/index.html` (kode, ter-track) vs `workspace/05-status/team.json` (runtime, di-ignore). Server statis kecil (`guardian/serve_status.py`, loopback:9200, systemd `team-status.service`) karena `/root` mode 700 tidak bisa di-traverse worker www-data | Diterapkan; worker www-data tidak bisa traverse `/root` mode 700 |
| 2026-11-01 | **`guardian/syncthing_auth.py` default dry-run**, ubah config + restart Syncthing hanya dengan `--apply` eksplisit | Diterapkan; **belum dijalankan** — restart tidak memperbaiki masalah auth GUI Syncthing |
| 2026-11-01 | **Logika Guardian tidak diubah.** Commit `3584ce1` hanya memindahkan path output (REPORT_DIR, status_file, COOLDOWN_FILE). Threshold $5, alert behavior, session monitor tetap apa adanya | Diterapkan; review logika tetap ditunda atas permintaan Cal |
| 2026-10-29 | Big-picture peta VPS/Hermes dimiliki proyek `workspace/04-proyek/ai-agent-improvement/architecture/`; workspace PC memuat salinannya | Sudah dipindahkan; file `docs/` lama dibersihkan |
| 2026-10-29 | **Prinsip desain lingkungan AI:** Agile, terstruktur, scalable, aman tanpa mengganggu operasional, resilient, aturan jelas, mudah dikembangkan; hindari duplikasi folder/path dan perbarui semua consumer saat memindahkan sesuatu | Disetujui Ical; berlaku untuk semua perubahan desain |
| 2026-10-29 | Dokumen/ROLE/laporan kanonis dipusatkan di workspace; output path agent & Guardian diarahkan ke workspace. Kode/job tetap di lokasi aman, cron memakai shim ke source script kanonis | Diterapkan dan path diuji |
| 2026-10-28 | Workspace file di VPS, dicermin ke Windows via Syncthing (PC kadang mati) | Disetujui Ical |
| 2026-10-28 | Folder Windows target: `C:\Users\USER\ai-team\Workspace` | Disetujui Ical |
| 2026-10-28 | Google Drive tidak dipakai untuk tahap awal | Rancangan saja; bukan keputusan eksplisit, boleh ditinjau |
| 2026-10-28 | Syncthing discovery/relay/NAT mati; direct connection lebih privat | Konfigurasi aktif, perlu evaluasi kemudahan pairing |
| 2026-10-28 | Jangan buka GUI Syncthing (8384) ke publik | Keputusan keamanan |
| 2026-10-28 | `workspace/` disimpan di repo GitHub agar PC bisa mengambil master via Git juga | Implementasi saat ini, perlu tinjau apakah tetap perlu setelah Syncthing aktif |
