# Brainstorm: Aplikasi Distribusi Rokok — 18 Okt 2026

## Ringkasan Keputusan
- **Pilot project** → portfolio buat ditawarin ke pabrik rokok kecil
- **6 reseller test:** Rudi (Gandul), Ichsan, Tantri, Jarwo, Egi, Bu Yuli
- **Tech stack:** Django + Tailwind + Leaflet.js + SQLite
- **Agent:** 1 PM Distribusi nangani Parser + Advisor + Report. Auditor tetap pisah.
- **Input:** Sales lapor via Telegram Group dengan format terstruktur

## Format Laporan Sales (real)
Template laporan harian dari lapangan — udah terstruktur:
- Header: Hari/Tanggal, Nama/Kode Sales, Regional, Area, Routing
- Metrik kunjungan: Call Mad, SAB, SATB, SKB, SKTB, NOO, DS, EC, AV
- Loading (stok dibawa) / Volume (terjual) / Sisa Saldo — per produk
- Total volume/omset, Setoran, BBM, Kilometer

## Istilah FMCG (confirmed)
| Kode | Arti |
|------|------|
| EC | Effective Call (kunjungan → transaksi) |
| NOO | New Open Outlet (pelanggan baru) |
| AV | Availability & Visibility (cek stok) |
| DS | Direct Selling (SPG/end user) |

SAB, SATB, SKB, SKTB → menunggu konfirmasi Ical ke sales (Agus). Kemungkinan kode segmen outlet internal.

## Modul Aplikasi (MVP)
1. Inventory Command Center — stok real-time, log masuk/keluar, alert
2. Sales Dashboard — revenue, tren, per produk/reseller/wilayah
3. Reseller CRM — profil, tier, history, piutang
4. Distribution Map — heat map, coverage gap (Leaflet.js)
5. Executive Dashboard — one screen holistic view

## Workflow Agent
```
Sales input Telegram → PM Agent parse → validasi → DB update → auto-reply
                                          ↓
                                    Auditor QC → flag anomali
                                          ↓
                                    Dashboard Owner (real-time)
```

## SOP Token Efficiency
- Simpan di ai-team-management skill ✓
- /new: history >40 rekomendasi, >80 wajib
- Delegate kerja berat ke sub-agent (model gratis)
- Output ringkas, jangan replay data user

## Next Steps
- Ical konfirmasi arti SAB/SATB/SKB/SKTB
- Lanjut spesifikasi teknis + wireframe
- Developer mulai coding setelah spec disetujui