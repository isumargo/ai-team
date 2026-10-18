# Developer — OpenCode CLI

## Cara Panggil
```bash
export $(grep -v '^#' /root/.hermes/.env | grep '=' | xargs) 2>/dev/null
opencode run "TASK" --model openrouter/deepseek/deepseek-v4.1-flash
```

## Model Routing (Auto-Switch)

### Default: `deepseek/deepseek-v4.1-flash` ($0.065/M)
- CRUD sederhana, scaffolding, konfigurasi, admin panel
- Bug fix minor, refactor ringan
- Semua task yang ga masuk kategori kompleks

### Auto-Switch: `deepseek/deepseek-v4-pro` (~$2/M)
Switch ke v4-pro jika task mengandung salah satu:
- Parser/NLP (regex kompleks, parsing laporan tidak terstruktur)
- Algoritma / business logic berat (heatmap, coverage gap, anomaly detection)
- Multi-step workflow (auto-reply, notification chain, state machine)
- Integrasi eksternal (Telegram Bot API, webhook handler)
- Database migration kompleks / query optimization

**Aturan:** EVE yang tentuin model pas delegasi. Default flash, sebutin explicit kalo perlu pro.

## Output
Semua hasil kerja ke /root/ai-team/agents/developer/reports/

## Rules
1. Satu task = satu opencode run
2. Test kode sebelum commit
3. Retry maks 3x
4. Output ringkas, to-the-point
5. Kalau task terbukti terlalu kompleks buat flash → restart dengan v4-pro
