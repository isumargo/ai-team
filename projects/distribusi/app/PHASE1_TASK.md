# Phase 1 Task: Telegram Parser & Inventory Core

Add these features to the existing Django app at /root/ai-team/projects/distribusi/app/

## WARNING
- DO NOT overwrite .env (contains TELEGRAM_BOT_TOKEN + DJANGO_SECRET_KEY)
- DO NOT delete db.sqlite3 (has 2 products + 6 resellers)
- DO NOT modify existing models (Product, Reseller, StockMovement, Transaction)
- Make migrations, DO NOT touch db.sqlite3 manually

## 1. Telegram Message Receiver (Polling-based)

Create a management command `python manage.py poll_telegram` that:
- Polls Telegram API `getUpdates` in a loop
- Processes updates with offset to avoid duplicates
- Runs indefinitely (for systemd service)

Or better: create a Django view `/webhook/<token>/` for Telegram webhook.
Since distro.raminesia.com will have HTTPS, use webhook approach:
- Add view in views.py: `telegram_webhook(request, token)`
- Add URL pattern: `webhook/<str:token>/`
- Add CSRF exemption for this view
- On startup: auto-register webhook with Telegram API

## 2. Message Parser (regex-based)

Parse incoming Telegram messages. Expected format:
```
JUAL [produk] [qty] bks [reseller] [harga opsional]
CONTOH [produk] [qty] bks [reseller]
RETUR [produk] [qty] bks [reseller]
STOK [produk]
STOK
PIUTANG [reseller]
```

Create `distribusi/parser.py`:
- `parse_message(text: str) -> dict` — returns structured data
- Handle variations: "jual", "JUAL", "Jual", "jual madju pro 100 bks ke rudi"
- Extract: action, product_name, quantity, reseller_name, price (optional)
- Return error dict if can't parse

## 3. Inventory Command Handler

Create `distribusi/commands.py`:
- `process_sales(action, product, qty, reseller, price)` — creates Transaction + StockMovement, reduces stock
- `process_sample(action, product, qty, reseller)` — creates StockMovement type=sample
- `process_return(action, product, qty, reseller)` — creates StockMovement type=return, increases stock
- `get_stock(product_name=None)` — returns stock info, format for Telegram reply
- `get_receivables(reseller_name=None)` — returns piutang info

## 4. Auto-Reply

After processing a message, reply via Telegram `sendMessage`:
- Success: "✅ Tercatat: [ringkasan transaksi]"
- Error: "❌ Format salah. Format: JUAL [produk] [qty] bks [reseller]"
- Stock query: return formatted stock list
- Receivables query: return formatted piutang

## 5. Inventory Command Center View

Add `/inventory/` page to Django:
- Real-time stock overview with color-coded alerts (red < 50 bks)
- Recent movements log (last 50)
- Quick stats: total stock, total receivables, today's sales
- Mobile-friendly, same Tailwind styling

## 6. Seed Data Generator

Management command: `python manage.py seed_test_data --days 7`
- Generates 7 days of realistic transaction data
- Mix of sales, samples, returns
- Uses existing 6 resellers and 2 products
- Properly adjusts stock levels

## 7. Update Admin

- Add list_filter for StockMovement (by type, date)
- Add list_filter for Transaction (by payment_status, date)
- Add search_fields for Transaction (reseller name)
- Add date_hierarchy for StockMovement and Transaction

## 8. Update Requirements

Add to requirements.txt:
```
requests
```

## Technology
- Pure Django, no Celery, no Redis
- SQLite
- Tailwind CSS CDN
- Bahasa Indonesia for all user-facing text
- Simple, minimal, production-ready

## Testing
After implementation, verify:
1. Bot receives messages
2. Parser handles all formats correctly
3. Stock decreases on sales
4. Dashboard shows updated numbers
5. `/inventory/` page loads
6. Seed data generates without errors