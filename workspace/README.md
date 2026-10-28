# AI Team Workspace — Panduan Singkat

Ini folder kerja bersama antara VPS dan PC kamu. Master-nya di VPS, PC hanya cermin.

## Aturan

1. **Kamu bebas membaca dan mengedit file di sini.**
2. Edit-kanmu dibalikkan ke VPS: kirim file yang sudah diubah ke chat EVE, EVE menulisnya ke VPS dan memperbarui mirror ini.
3. EVE juga menaruh hasil kerja agen di sini setelah lolos audit — biasanya di `03-agen/<nama>/laporan/` atau `04-proyek/`.
4. folder `99-arsip/` diisi otomatis; laporan lebih tua dari 7 hari dipindah Guardian ke sana.
5. File rahasia (token, password, key, database) **tidak pernah** ditaruh di folder ini.

## Struktur

| Folder | Isi | Siapa yang menulis |
|---|---|---|
| `00-inbox/` | draft mentah, belum diaudit | agen |
| `01-organisasi/` | AGENTS.md, USER.md, peta | EVE + kamu |
| `02-memo/` | koordinasi Adam ↔ EVE | EVE |
| `03-agen/*/laporan/` | hasil kerja agen | agen + EVE |
| `04-proyek/` | rencana, laporan, rilis per proyek | agen + EVE |
| `05-status/` | snapshot status harian | EVE |
| `99-arsip/` | laporan tua | Guardian |

## Nama file

Format: `YYYY-MM-DD-<agen>-<judul-pendek>.md` — contoh: `2026-10-28-analyst-margin-madju.md`.

## Sumber kebenaran

- Persona + konfigurasi agen: tetap di VPS `~/.hermes/` — tidak diduplikasi ke sini.
- Peta organisasi: `01-organisasi/peta/truth-map.md` (teks) + `truth-map.excalidraw` (visual).