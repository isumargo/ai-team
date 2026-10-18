# Phase 2 Task: Dashboard & CRM

Add these features to the Django distribusi app at /root/ai-team/projects/distribusi/app/

## WARNING
- DO NOT overwrite .env or db.sqlite3
- DO NOT modify existing models (Product, Reseller, StockMovement, Transaction)
- DO NOT delete existing templates/views
- Keep using Tailwind CSS CDN + Leaflet.js CDN
- Bahasa Indonesia for all user-facing text

## 1. Enhanced Sales Dashboard (upgrade `/`)

Add to existing dashboard view:
- **Revenue chart**: weekly revenue trend as a simple bar chart (pure CSS/HTML bars, no chart library)
- **Top products**: ranked list with quantities sold
- **Top resellers**: ranked by total purchase value
- **Recent transactions**: already exists, expand to last 10 with status badges
- **Quick stats cards**: already exists, add week-over-week comparison arrow (↑↓)

## 2. Reseller Detail Page (NEW `/reseller/<id>/`)

Clicking a reseller in the list goes to detail page:
- **Profile card**: name, phone, address, tier (bronze/silver/gold badge with color), active status
- **Transaction history**: table of all transactions, sorted by date desc, with payment status badges
- **Receivables tracker**: total piutang, list of unpaid transactions
- **Stock movement log**: samples taken, returns made
- **Stats**: total purchased, total spent, average order size
- **Tier logic**: 
  - Bronze: default (0-1000 bks total)
  - Silver: 1000-3000 bks
  - Gold: >3000 bks
  - Auto-calculate from transaction history

Add to reseller_list template: make reseller names clickable → detail page

## 3. Distribution Map (NEW at `/map/`)

Full-page Leaflet.js map showing reseller locations:
- **Markers**: each reseller as a pin on the map, color-coded by tier (bronze/silver/gold)
- **Popups**: click pin → reseller name, total purchase, last transaction date, link to detail
- **Heatmap layer**: use Leaflet.heat plugin (CDN) showing transaction density
- **Coverage visualization**: color-coded areas based on reseller activity

Since resellers don't have lat/lng yet, add these coordinates:
- Rudi: -8.1939, 111.1029 (Pacitan)
- Ichsan: -8.2047, 111.1352
- Tantri: -8.1871, 111.1184
- Jarwo: -8.2106, 111.0917
- Egi: -8.1998, 111.1103
- Bu Yuli: -8.1754, 111.1276
- Store lat/lng as JSONField on Reseller model (or add FloatField lat, lng via migration)

Better: add lat/lng to Reseller model via migration (FloatField, nullable). Seed these coordinates.

## 4. Mobile-Friendly Layout

All pages must work on mobile:
- Responsive Tailwind classes (grid-cols-1 sm:grid-cols-2 lg:grid-cols-4)
- Stack cards vertically on small screens
- Map takes full width on mobile
- Tables become scrollable horizontally on mobile (overflow-x-auto)
- Nav menu collapses to hamburger on mobile (pure CSS, no JS framework)

## 5. Template Updates

- **dashboard.html**: add revenue bars, top products, top resellers sections
- **NEW reseller_detail.html**: full detail page
- **reseller_list.html**: make names clickable, add tier badges
- **NEW map.html**: Leaflet.js full page
- **base.html**: add Map link to nav

## 6. URL Patterns (update urls.py)

```
/                  → dashboard (enhanced)
/reseller/<id>/    → reseller_detail
/map/              → distribution_map
```

## 7. No New Dependencies

- NO chart.js, NO apexcharts — use pure CSS bars
- Leaflet.js + Leaflet.heat from CDN
- Tailwind CSS CDN
- All existing deps stay

## Verification
1. Dashboard loads with revenue bars
2. Click reseller → detail page with history
3. Map loads with 6 colored pins
4. Mobile view: hamburger menu, stacked cards, horizontal-scroll tables