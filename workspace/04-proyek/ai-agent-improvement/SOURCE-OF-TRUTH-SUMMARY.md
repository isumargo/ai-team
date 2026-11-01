# Audit sumber data — executive summary

Rujuk detail dan target di `SOURCE-OF-TRUTH.md`.

| Domain | Lokasi canonical saat ini / usulan | Tingkat risiko | Belum dilakukan |
|---|---|---:|---|
| Hermes config/secrets/state | `~/.hermes/` runtime | Sangat tinggi | Tidak dipindah/salin ke workspace |
| Policy umum | Belum satu: `/root/AGENTS.md` dan `~/.hermes/AGENTS.md` | Tinggi | Merge + cek loader sebelum ubah |
| User profile | Belum jelas: `~/.hermes/USER.md` vs `memories/USER.md` | Tinggi | Cek loader dan efek prompt |
| Persona agent | Profile `SOUL.md`; repo `ROLE.md` kemungkinan duplikasi | Tinggi | Cek apakah automation membaca ROLE |
| Memo | `memo/` repo + salinan workspace | Sedang | Putuskan workspace sebagai master, ubah memo lama jadi pointer/arsip |
| Project docs | `workspace/04-proyek/ai-agent-improvement/` + mirror workspace | Sedang | Pilih satu master, pindahkan satu kali setelah persetujuan |
| Status agen | `status/*.json` stale/incomplete | Sedang | Cari consumer, pilih runtime status source |
| Reports | tersebar di agents/auditor/guardian/projects | Sedang | Bedakan laporan audit dari metrics operasional Guardian |
| Big picture | `workspace/04-proyek/ai-agent-improvement/architecture/` + workspace mirror | Rendah | Sudah dipusatkan; Markdown adalah source teks |
| Workspace PC | `/root/ai-team/workspace/` ↔ Windows Syncthing | Rendah | Mirror, bukan runtime source atau pengganti Git |

**Saran:** satu canonical per domain, bukan memaksa semua hal dalam satu folder. Sebelum migrasi file aktif, periksa semua consumer dan cara Hermes memuat instruksi. Rencana lengkap ada di `SOURCE-OF-TRUTH.md`.
