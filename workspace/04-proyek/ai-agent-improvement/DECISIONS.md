# Keputusan proyek

| Tanggal | Keputusan | Status |
|---|---|---|
| 2026-10-29 | Big-picture peta VPS/Hermes dimiliki proyek `workspace/04-proyek/ai-agent-improvement/architecture/`; workspace PC memuat salinannya | Sudah dipindahkan; file `docs/` lama dibersihkan |
| 2026-10-29 | **Prinsip desain lingkungan AI:** Agile, terstruktur, scalable, aman tanpa mengganggu operasional, resilient, aturan jelas, mudah dikembangkan; hindari duplikasi folder/path dan perbarui semua consumer saat memindahkan sesuatu | Disetujui Ical; berlaku untuk semua perubahan desain |
| 2026-10-29 | Dokumen/ROLE/laporan kanonis dipusatkan di workspace; output path agent & Guardian diarahkan ke workspace. Kode/job tetap di lokasi aman, cron memakai shim ke source script kanonis | Diterapkan dan path diuji |
| 2026-10-28 | Workspace file di VPS, dicermin ke Windows via Syncthing (PC kadang mati) | Disetujui Ical |
| 2026-10-28 | Folder Windows target: `C:\Users\USER\ai-team\Workspace` | Disetujui Ical |
| 2026-10-28 | Google Drive tidak dipakai untuk tahap awal | Rancangan saja; bukan keputusan eksplisit, boleh ditinjau |
| 2026-10-28 | Syncthing discovery/relay/NAT mati; direct connection lebih privat | Konfigurasi aktif, perlu evaluasi kemudahan pairing |
| 2026-10-28 | Jangan buka GUI Syncthing (8384) ke publik | Keputusan keamanan |
| 2026-10-28 | `workspace/` disimpan di repo GitHub agar PC bisa mengambil master via Git juga | Implementasi saat ini, perlu tinjau apakah tetap perlu setelah Syncthing aktif |
