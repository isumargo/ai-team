# Workspace AI — dokumen kanonis tim

Folder ini adalah **satu-satunya rumah dokumen** tim AI. Isinya tersinkron ke PC lewat Syncthing (`C:\Users\USER\ai-team\Workspace`) sehingga bisa dibaca dan diedit dari Windows.

## Struktur

| Folder | Isi | Siapa yang edit |
|---|---|---|
| `00-inbox/` | Masukan dan file uji sinkronisasi | EVE, Cal |
| `01-organisasi/` | Policy tim, peta arsitektur, profil pengguna | EVE/Adam |
| `01-organisasi/policy/` | **Canonical policy** + generator salinan runtime | EVE |
| `02-memo/` | Memo dan korespondensi antar-agen | EVE, Adam |
| `03-agen/<agent>/` | ROLE tiap agen (metadata peran, bukan persona) | EVE |
| `04-proyek/<project>/` | Handoff, status, plan, dokumen bisnis | EVE, Cal |
| `05-status/` | Snapshot status ber-timestamp (jika dipakai) | generator, bukan diedit manual |
| `99-arsip/` | Arsip lama dengan retensi jelas | EVE |

## Aturan

1. **Satu sumber kanonis per jenis data.** Jangan membuat file yang sama di dua folder. Kalau ada compatibility copy (misalnya `AGENTS.md` runtime), itu hasil generate dan wajib dicek.
2. EditPolicy hanya di `01-organisasi/policy/`, lalu jalankan:
   ```bash
   python3 /root/ai-team/workspace/01-organisasi/policy/sync_policy.py --sync
   python3 /root/ai-team/workspace/01-organisasi/policy/sync_policy.py --check
   ```
3. **Tidak ada rahasia di sini.** Jangan masukkan `.env`, token, password, database runtime, venv, atau state Hermes. Folder `projects/distribusi/app/` (kode + DB) tetap di VPS, tidak ikut sinkron.
4. Folder output runtime (`agents/*/reports`, `guardian/reports`, `status/`) sengaja tetap di repo karena script dan job menunjuk ke sana. Jangan dihapus sebelum path-nya dimigrasikan.
5. Edit dari PC dan VPS jangan bersamaan untuk file yang sama. Git dan Syncthing bukan pengganti satu sama lain: Git untuk riwayat, Syncthing untuk akses file.
6. Prinsip desain: Agile, terstruktur, scalable, aman tanpa mengganggu operasional, resilient, aturan jelas, mudah dikembangkan.
