# Developer — OpenCode CLI

## Cara Panggil
```bash
export $(grep -v '^#' /root/.hermes/.env | grep '=' | xargs) 2>/dev/null
opencode run "TASK" --model openrouter/deepseek/deepseek-chat
```

## Model
- Default: deepseek/deepseek-chat (V3, $0.27/1M)
- Bisa ganti model via --model flag
- Free models: nvidia/nemotron-3-super-120b-a12b:free

## Output
Semua hasil kerja ke /root/ai-team/agents/developer/reports/

## Rules
1. Satu task = satu opencode run
2. Test kode sebelum commit
3. Retry maks 3x
4. Output ringkas, to-the-point
