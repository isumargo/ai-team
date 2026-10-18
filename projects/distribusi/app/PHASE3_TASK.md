# Phase 3 Task: AI Agent Dasiyah — Replace Regex Parser

Replace the regex parser in the Telegram webhook with an AI agent.

## Architecture

```
Sales chat → Telegram → webhook → Agent (LLM + tools) → DB
                                    ↓
                              auto-reply via Telegram
```

## WARNING
- DO NOT overwrite .env or db.sqlite3
- Keep existing commands.py — use it as tool implementations
- Keep existing models, views, URLs
- Keep Telegram webhook endpoint at /webhook/<token>/
- Fallback chain: gemini-flash → nemotron → deepseek-chat

## 1. Session Storage (for multi-turn context)

Create model `ChatSession` in distribusi/models.py:
- chat_id: CharField (Telegram chat_id)
- messages: JSONField (list of {role, content} dicts)
- updated_at: DateTimeField (auto_now)
- is_active: BooleanField (default True)

Keep max 10 messages per session. Auto-deactivate sessions >15 min old.

Migration: `0003_chatsession`

## 2. Agent Core (NEW: distribusi/agent.py)

`class DasiyahAgent`:
- `__init__()`: loads config (model, fallback chain, system prompt)
- `process_message(chat_id: str, text: str) -> str`: main entry point
  - Load or create session from ChatSession
  - Build messages: system prompt + session history + new user message
  - Call LLM with function/tool definitions
  - If LLM returns function_call → execute tool → feed result back → loop (max 5 iterations)
  - If LLM returns final text → save to session, return reply
- Tool methods (all call existing commands.py functions):
  - `cek_stok(produk=None)` → string
  - `cari_reseller(nama)` → dict or None
  - `catat_penjualan(produk, qty_bks, reseller, harga?)` → string result
  - `catat_sample(produk, qty_bks, reseller)` → string result
  - `catat_retur(produk, qty_bks, reseller)` → string result
  - `cek_piutang(reseller=None)` → string
  - `tanya_ke_owner(pertanyaan)` → sends Telegram DM to owner's chat_id (from .env: OWNER_CHAT_ID), returns confirmation
  - `selesai()` → mark session inactive, return closing message

## 3. System Prompt — Dasiyah Persona

Bahasa: Indonesian with Javanese flair. Panggil "Mas" atau "Mbak".

```
Kamu adalah Dasiyah (Jeng Yah), admin pabrik rokok Madju PRO & Sukses Alami di Pacitan.
Persona: cekatan, ceplas-ceplos tapi sopan, paham seluk-beluk rokok, panggil semua "Mas" atau "Mbak".

Tugas:
1. Baca laporan sales di grup, catat ke database
2. Kalo ada yang kurang jelas, tanya balik
3. Konversi unit otomatis ke bungkus: 1 slop = 12 bks, 1 bal = 120 bks
4. Validasi stok sebelum catat penjualan
5. Kalo transaksi udah lengkap & valid, langsung catat tanpa konfirmasi ulang
6. Kalo nemu anomali (stok minus, piutang numpuk), sampaikan ke owner

Aturan:
- Jangan catat tanpa konfirmasi kalo data ambigu (unit gak jelas, reseller gak ketemu)
- Stok Sukses Alami & Madju PRO terpisah
- Harga default: Rp 8.600/bks (kecuali disebut lain)
- Piutang dicatat otomatis per transaksi (sales nyicil)
- Kalo transaksi berhasil, kasih ringkasan singkat
- Jangan banyak basa-basi, langsung kerja
```

Add to .env: `OWNER_CHAT_ID=<Ical's Telegram chat ID>`

## 4. LLM Call Implementation

Use direct OpenRouter API via requests (NO langchain, NO complex framework):

```python
def call_llm(messages, tools=None):
    # Model chain: gemini-flash → nemotron → deepseek-chat
    for model in ["google/gemini-3-flash-preview", "nvidia/nemotron-3-super-120b-a12b:free", "deepseek/deepseek-chat"]:
        try:
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={"Authorization": f"Bearer {token}"},
                json={"model": model, "messages": messages, "tools": tools},
                timeout=30
            )
            if response.status_code == 200:
                return response.json()
        except:
            continue
    return None
```

## 5. Modify telegram_webhook View

In views.py, replace the regex parser call with Dasiyah agent:
- Remove `from .parser import parse_message`
- Add `from .agent import DasiyahAgent`
- Replace the parse_message + action routing block with:
  ```python
  agent = DasiyahAgent()
  reply = agent.process_message(chat_id, text)
  ```
- Keep send_telegram_message as-is
- Keep CSRF exemption + token validation

## 6. Requirements

Add to requirements.txt: NO new deps needed (requests already there)

## 7. Verification

After implementation:
1. Run `python manage.py makemigrations && python manage.py migrate`
2. Verify ChatSession model created
3. Test via curl simulating Telegram message:
```bash
curl -X POST http://localhost:8080/webhook/<TOKEN>/ \
  -H "Content-Type: application/json" \
  -d '{"message":{"chat":{"id":"12345"},"text":"jual madju pro 2 slop ke rudi"}}'
```
4. Verify stock decreases, transaction created
5. Verify ambiguous message gets follow-up question
6. Push to GitHub