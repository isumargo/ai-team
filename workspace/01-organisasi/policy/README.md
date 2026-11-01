# Policy canonical

Policy tim dan instruksi khusus Developer bersumber dari file di folder ini. **Edit hanya file sumber di sini.**

## Sumber kanonis

- `TEAM-POLICY.md` — aturan umum tim.
- `DEVELOPER-INSTRUCTIONS.md` — instruksi tambahan Developer.

## Salinan otomatis

Jalankan dari VPS:

```bash
python3 /root/ai-team/workspace/01-organisasi/policy/sync_policy.py --sync
python3 /root/ai-team/workspace/01-organisasi/policy/sync_policy.py --check
```

Script membuat salinan runtime:

- Team policy → `/root/AGENTS.md`, `~/.hermes/AGENTS.md`, dan `workspace/01-organisasi/AGENTS.md`.
- Developer profile → `~/.hermes/profiles/developer/AGENTS.md`, yang berisi gabungan team policy + instruksi Developer. Hermes hanya memuat satu AGENTS per direktori; file profil ini perlu gabungan agar Developer menerima keduanya.

Salinan runtime jangan diedit manual. `--check` hanya verifikasi dan tidak menulis. `--sync` membuat backup privat sebelum menimpa.
