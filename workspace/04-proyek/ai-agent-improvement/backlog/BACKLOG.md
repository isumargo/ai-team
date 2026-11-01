# Backlog — tugas berikutnya

## Syncthing
- [ ] Validasi auth GUI (kredensial tersimpan, tapi cek HTTP unauth masih 200).
- [ ] Pair device Windows dengan direct address `tcp://<IP-VPS>:22000`.
- [ ] Share folder `workspace` ke device Windows; set type sendreceive dua arah.
- [ ] Windows installer hanya dari `syncthing.net`; jangan mirror tak dikenal.
- [ ] Uji sync dua arah dengan file dummy; hapus dummy setelah Ical konfirmasi.
- [ ] Buat `.stignore` kecil (secrets, dumps, temp) bila Ical setuju.

## Layanan mati (Fase 2)
- [ ] Django distro: bunuh proses zombie 8080, start ulang service, uji domain.
- [ ] Ruang 3D: hidupkan `ruang.service`; systemd user bus bermasalah (DBUS).
- [ ] Health check mingguan ke Guardian: distro, ruang, dashboard, gateway.

## Konsistensi dokumen
- [ ] Rekonsiliasi threshold biaya $5 vs $20 (butuh keputusan Ical).
- [ ] Samakan AGENTS.md: `/root/AGENTS.md` vs `~/.hermes/AGENTS.md` (SOP #6 Syncera hanya di satu versi).
- [ ] ROLE.md per agen -> pointer ke `~/.hermes/profiles/<nama>/SOUL.md`.
- [ ] status/*.json: 5 dari 9 agen; pertimbangkan generate otomatis dari state.

## Pembersihan (butuh persetujuan)
- [ ] `profiles/developer/config.yaml` 109KB -> override ringkas saja.
- [ ] Backup 189MB/200MB -> exclude `venv/`, `node_modules/` sebelum membesar.
- [ ] Nama model bocor di beberapa file → sanitasi bertahap, tanpa menyentuh `config.yaml`.