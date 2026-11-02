# Temuan Teknis — Guardian Auto-Switch Salah Target

**Dari:** EVE (Chief of Staff)
**Ke:** Ical (Cal) — untuk keputusan
**Tanggal:** 2026-11-02
**Status:** ⏸️ Menunggu keputusan Cal (belum ada perubahan dibuat)
**Lokasi kodenya:** `guardian/check_usage.py`

---

## 1. Ringkasan

Guardian (penjaga biaya) supposed auto-alihkan model ke yang lebih murah saat biaya melewati batas. **Ternyata yang dialihkan cuma 1 dari 10 profil** — dan bukan yang paling boros.

## 2. Yang terjadi

Di `guardian/check_usage.py`, perintah switch-nya:

```python
["/root/.local/bin/hermes", "config", "set", "model.default", new_model]
```

**Tidak ada flag `-p <nama-profil>`.** Tanpa flag itu, Hermes menulis ke **config root** (= profil EVE) saja.

Jadi kalo biaya lewat batas:
- ✅ Profil **EVE** (root) → diganti ke model murah
- ❌ Profil **analyst, developer, pm-distribusi, auditor, guardian, marketer, sales, strategist, designer** → **tidak tersentuh sama sekali**

Justru profil anak itu yang paling sering mikir (kode, laporan, planning) — di situ borosnya.

## 3. Bukti

| Observasi | Nilai |
|---|---|
| Biaya OpenRouter saat sesi ini | **$9.86** dari total $10 |
| Limit di `guardian/config.json` | $5 → sudah terlampaui |
| Yang ter-switch | `model.default` di `/root/.hermes/config.yaml` (root/EVE) |
| Log Guardian | `Switched OK: ✓ Set model.default = ... in /root/.hermes/config.yaml` |

Cron Guardian (`guardian-openrouter-check`) jalan **setiap 30 menit** — jadi penulisan ulang config EVE ini terjadi rutin.

## 4. Temuan tambahan (lebih halus)

Guardian cuma cek endpoint `https://openrouter.ai/api/v1/credits`. Sementara EVE (dan sebagian alur lain) jalan lewat **provider `anthropic` → `api.syncera.id`**, yang biayanya **tidak dipantau sama sekali** sama Guardian.

Jadi ada 2 celah:
1. **Target switch** cuma 1 profil (EVE), padahal borosnya di profil anak.
2. **Cakupan monitor** cuma OpenRouter, padahal ada jalur_request lewat Syncera yang beda aturannya (paket kuota 550 request/5 jam + 5.000/minggu — bukan berbasis dollar).

## 5. Kenapa aku belum ubah

Ini menyentuh perilaku biaya & infra:
- Menambah monitor Syncera → perlu endpoint/credential & keputusan logikanya.
- Mengubah switch jadi kena semua profil → 9 profil ditulis ulang tiap 30 menit saat limit terlampaui (bisa bikin session agents kehilangan model mid-flight).

Perubahannya cukup jelas, tapi perlu tahu **niatmu** dulu: hemat maksimal, atau auto-switch per profil yang boros aja?

## 6. Keputusan yang dibutuhkan

| # | Pertanyaan | Pilihan |
|---|---|---|
| 1 | Batas biaya resmi tim | **$5** (nilai sekarang di `guardian/config.json`) atau **$20** (catatan lama)? |
| 2 | Auto-switch kena semua profil, atau per profil? | Semua / per profil |
| 3 | Pantau juga biaya Syncera (non-dollar)? | Ya / belum |

## 7. Yang sudah diperbaiki (aman, tanpa izin tambahan)

`BACKUP_MODEL` di `guardian/check_usage.py` sebelumnya menunjuk model yang sudah mati (404). Kalau tidak diganti, switch-nya jadi no-op — jadi "auto-switch" terlihat jalan di log tapi sebenarnya tidak mengubah apa-apa. Sudah diganti ke model yang hidup dan teruji.

## 8. Catatan

Nama model sengaja tidak ditulis lengkap di dokumen ini — identitasnya ada di file config runtime, sesuai aturan anti-halusinasi tim.
