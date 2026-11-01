# Source of Truth — Struktur Environment AI

**Diperbarui:** 2026-11-01
**Status:** struktur kanonis aktif; repo GitHub sudah sinkron (push `507a08b`); status tim live berjalan.

## Prinsip

Satu sumber kanonis per jenis data. Compatibility copy hanya ada bila loader membutuhkannya, dihasilkan otomatis dan dicek. Jangan mencampur dokumen PC-sync dengan data runtime/rahasia.

## Peta canonical saat ini

| Domain | Sumber kanonis | Runtime/consumer | Aturan |
|---|---|---|---|
| Dokumen organisasi/policy | `/root/ai-team/workspace/01-organisasi/` | Workspace ke PC via Syncthing | Edit di workspace, jangan edit salinan AGENTS runtime |
| Policy tim | `workspace/01-organisasi/policy/TEAM-POLICY.md` | `/root/AGENTS.md`, `~/.hermes/AGENTS.md`, `workspace/01-organisasi/AGENTS.md` | Generated oleh `workspace/01-organisasi/policy/sync_policy.py`; hash-check |
| Developer instructions | `workspace/01-organisasi/policy/DEVELOPER-INSTRUCTIONS.md` | `~/.hermes/profiles/developer/AGENTS.md` | Generated oleh script sync yang sama |
| ROLE metadata | `workspace/03-agen/<agent>/ROLE.md`; PM role di `workspace/04-proyek/distribusi/ROLE.md` | Hermes profiles memuat SOUL/config | ROLE dokumen, bukan activator; output runtime masih mengarah ke folder laporan lama |
| Persona | `~/.hermes/profiles/<profile>/SOUL.md` | Hermes runtime | Jangan pindah/sinkron |
| User memory | `~/.hermes/memories/USER.md` | Hermes runtime | Stable memory; jangan jadikan progress log |
| Session state/secrets/config | `~/.hermes/` | Hermes runtime | Private; jangan sync ke PC |
| Handoff/status/plan/decision proyek AI | `workspace/04-proyek/ai-agent-improvement/` | Dibaca EVE/Cal; Syncthing PC | Satu-satunya canonical; tidak ada `projects/ai-agent-improvement/` kedua |
| Memo | `workspace/02-memo/` | Agen/manusia via file | Satu-satunya canonical; direktori root `memo/` sudah dipensiunkan |
| Distribusi: dokumen bisnis | `workspace/04-proyek/distribusi/` | Dibaca Cal/Dasiyah | Kode aplikasi tidak berada di sini |
| Distribusi: aplikasi | `/root/ai-team/projects/distribusi/app/` | Django runtime/deployment | Tetap di lokasi operasional; `.env`, DB, venv tidak masuk workspace |
| Guardian code/config | `/root/ai-team/guardian/` | Hermes cron jobs | Code/config stays. Guardian runtime output goes to workspace `03-agen/guardian/laporan/` and `05-status/` via canonical scripts; cron uses thin Hermes script shims.
| Status historis | `workspace/04-proyek/ai-agent-improvement/status-audit/archive-2026-10-29/` | Arsip audit | Bukan status live; jangan mengedit |
| Status Guardian | `/root/ai-team/workspace/05-status/guardian.json` (dibuat Guardian) | Check usage cron script | Output ditulis ke workspace canonical; jangan edit manual |
| **Status tim live** | `/root/ai-team/workspace/05-status/team.json` (dibuat `guardian/team_status.py`) | Dashboard `guardian/dashboard/index.html`, Ruang 3D (nanti) | **Satu writer**: `guardian/team_status.py`. Tidak boleh ada agen lain yang menulis file ini. Runtime, di-ignore git |
| **Kode dashboard status** | `/root/ai-team/guardian/dashboard/index.html` + `guardian/serve_status.py` | systemd `team-status.service` (loopback:9200), nginx vhost `hermes.raminesia.com` → `/team-status/` | Kode ada di repo; file runtime JSON tidak |
| Laporan agen | `/root/ai-team/workspace/03-agen/<agent>/laporan/` | SOUL + ROLE | Semua agen dan auditor menulis ke satu workspace kanonis; folder repo lama dipensiunkan |
| Git | `/root/ai-team` | GitHub remote | Version history; working tree bersih per 2026-11-01 |

## Ruang lingkup sinkronisasi

- Syncthing hanya menyinkronkan `/root/ai-team/workspace/` ke PC.
- Workspace berisi dokumen yang memang perlu diakses di PC. Tidak menaruh `.env`, credential, runtime DB, venv, atau live state.
- Generated `/root/ai-team/workspace/01-organisasi/AGENTS.md` adalah compatibility copy di dalam workspace yang perlu disync ke PC; jangan diedit manual.

## Batasan dan sisa pekerjaan

1. Output laporan agen telah diarahkan ke `workspace/03-agen/<agent>/laporan/`; SOUL, Developer instructions, Guardian scripts, dan cron script path diperbarui. Old repo output directories removed after copy/hash check.
2. Guardian scripts aktif dan tidak dipindah. Jangan ubah hingga audit job/consumer/threshold/backup selesai dan Cal menyetujui rencana. **Status tim live (`team_status.py`) juga bagian Guardian — hanya writer tambahan, tidak mengubah logika job yang ada.**
3. Django Distribusi code/runtime tetap di `projects/distribusi/app/`; repair nanti harus memperbarui deployment path secara lengkap atau mempertahankan path ini.
4. PC-sync dua arah telah diuji. Jangan hapus probe tanpa izin.
5. Workspace cermin dari PC adalah working copy pada folder yang sama melalui Syncthing, bukan direktori terpisah.
6. Before commit/push, pisahkan perubahan terkait dari Guardian runtime output yang tidak terkait dan audit secret scan. **Selesai 2026-11-01** — 5 commit selektif, push `507a08b`. Peringatan: jangan pakai `git add -A`; `.gitignore` hanya melindungi path yang dikomentari eksplisit, dan path runtime kanonis ada di `workspace/`.

## Validasi

- Policy `--check` lulus untuk tiga target team policy dan satu Developer runtime target.
- Handoff/status/plan/docs proyek AI memiliki satu salinan kanonis di `workspace/04-proyek/ai-agent-improvement/`.
- Tidak ada folder repo `projects/ai-agent-improvement/` lagi.
- `memo/` root tidak ada; memo kanonis di `workspace/02-memo/`.
- **2026-11-01**: `git check-ignore` mengonfirmasi 6 file runtime tertosol; `git ls-tree origin/main` mengonfirmasi tidak ada runtime file di repo. Secret scan 5 commit bersih. Working tree bersih.
- **2026-11-01**: `team_status.py` menghasilkan 10 agen + 3 job; `team.json` valid JSON dan tidak memuat nama model/tier/credential. Dashboard: `/`→200, `/team.json`→200, path lain→404, traversal→404, tanpa kredensial→401, dengan kredensial→200.
