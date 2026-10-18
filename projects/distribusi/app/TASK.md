# Phase 0 Task: Django Distribution App Scaffold

Create a production-ready Django project for cigarette distribution tracking in `/root/ai-team/projects/distribusi/app/`.

## WARNING
A `.env` file already exists in this directory with TELEGRAM_BOT_TOKEN and DJANGO_SECRET_KEY. DO NOT overwrite it.

## Tech Stack
- Django 5.x + SQLite
- Tailwind CSS (CDN in base template)
- Leaflet.js (CDN)
- python-dotenv

## Models — Single Django app called "distribusi"

### Product
- name: CharField (Madju PRO SKT, Sukses Alami SKT)
- sku: CharField unique
- price_buy: DecimalField (default 7600)
- price_sell: DecimalField (default 8600)
- stock: IntegerField
- created_at: DateTimeField

### Reseller
- name: CharField
- phone: CharField blank
- address: TextField blank
- tier: CharField choices: bronze/silver/gold
- credit: DecimalField default 0 (piutang)
- active: BooleanField default True
- created_at: DateTimeField

### StockMovement
- product: FK Product
- reseller: FK Reseller (nullable)
- movement_type: CharField choices: in/out/sample/return
- quantity: IntegerField
- notes: TextField blank
- created_at: DateTimeField

### Transaction
- reseller: FK Reseller
- product: FK Product
- quantity: IntegerField
- price_per_unit: DecimalField
- total: DecimalField
- payment_status: CharField choices: paid/unpaid/partial
- notes: TextField blank
- created_at: DateTimeField

## Views/Templates
1. `/` — Dashboard: cards (total stok, revenue hari ini, top reseller, piutang)
2. `/stock/` — Tabel produk + stok
3. `/resellers/` — Tabel reseller + tier + piutang
4. Base template: Tailwind CDN + Leaflet.js CDN, mobile responsive, bahasa Indonesia

## Config
- Use python-dotenv, read from existing .env
- STATIC files configured
- DEBUG from .env

## Admin
- Register all models
- list_display, search_fields, list_filter for each

## Final Steps
- requirements.txt: django, python-dotenv
- Run makemigrations + migrate
- Create superuser: admin / admin123
- Load 6 initial resellers: Rudi, Ichsan, Tantri, Jarwo, Egi, Bu Yuli (phone/address can be placeholder)
- Load 2 initial products: Madju PRO SKT, Sukses Alami SKT

## Constraints
- NO Docker, Redis, Celery
- All code under /root/ai-team/projects/distribusi/app/
- Simple, production-ready but minimal