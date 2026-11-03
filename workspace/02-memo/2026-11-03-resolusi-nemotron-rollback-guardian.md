# Resolusi Root Cause: Model Reverting ke Nemotron & Error Clouvia

**Tanggal:** 2026-11-03  
**Dari:** EVE (Chief of Staff)  
**Untuk:** Ical (Cal), Adam (Lead Architect)  
**Status:** ✓ TUNTAS & TERVERIFIKASI  

---

## 1. Gejala Masalah
- Di Hermes Desktop / Chat, model terus-menerus kembali ke `nvidia/nemotron-3.5-lightning:free`.
- Pesan error muncul:
  > `This model is not available: custom does not offer this model on your account. Choose another model, then send your message again.`
- Sebelumnya dicoba solusi manual (mengunci config dengan `chmod 444` dan menghapus cache backup), namun model tetap kembali ke Nemotron secara berkala ("back and forth").

---

## 2. Investigasi Root Cause
Setelah investigasi sistematis:
1. **Cron Job Tersembunyi:** Terdapat cron job Hermes bernama `guardian-openrouter-check` (`98c8436a58f9`) yang berjalan setiap 30 menit.
2. **Skrip Eksekusi:** Menjalankan `/root/ai-team/workspace/03-agen/guardian/check_usage.py` (via shim `guardian-check-usage.py`).
3. **Logika Auto-Switch:**
   - Skrip mengambil data penggunaan OpenRouter API (`https://openrouter.ai/api/v1/credits`).
   - Nilai `total_usage` yang tercatat adalah akumulasi riwayat akun sebesar **$9.87**.
   - Batas `COST_LIMIT` disetel ke **$5.00**.
   - Karena `$9.87 >= $5.00` selalu bernilai `True`, skrip secara otomatis menjalankan:
     ```bash
     hermes config set model.default nvidia/nemotron-3.5-lightning:free
     ```
   - Perintah ini menimpa `model.default` di `/root/.hermes/config.yaml` menjadi Nemotron **setiap 30 menit**.
4. **Konflik Provider:**
   - Provider utama runtime saat ini telah bermigrasi ke **Clouvia Router** (`provider: custom:clouvia`, `https://router.clouvia.id/v1`).
   - Clouvia Router tidak menyediakan model `nvidia/nemotron-3.5-lightning:free`.
   - Akibatnya, request gagal dengan status model not offered.

---

## 3. Tindakan Perbaikan yang Dilakukan
1. **Eliminasi Auto-Switch Sepihak:**
   - Menghapus fungsi `switch_model()` dan variabel `BACKUP_MODEL` dari `/root/ai-team/workspace/03-agen/guardian/check_usage.py`.
   - Mengubah logika Guardian menjadi **Alert-Only**: jika pemakaian melebihi batas atau ada kenaikan biaya, Guardian hanya mencatat peringatan ke file laporan/log tanpa menyentuh konfigurasi runtime.
2. **Sinkronisasi Skrip Shim:**
   - Memastikan `~/.hermes/scripts/check_usage.py` mengarah ke source of truth di `workspace/03-agen/guardian/check_usage.py`.
3. **Restorasi Konfigurasi Runtime:**
   - Menyetel kembali `model.default` ke `coding-high` di `/root/.hermes/config.yaml`.
4. **Pembaruan Memori Agen:**
   - Memperbarui memori persisten agar mencerminkan bahwa `check_usage.py` kini bersifat alert-only dan tidak melakukan auto-switch runtime model.

---

## 4. Hasil Pengujian & Verifikasi
1. **Pengujian Eksekusi Skrip Cron:**
   - Menjalankan `python3 /root/.hermes/scripts/guardian-check-usage.py`.
   - Skrip mendeteksi biaya $9.87, mencatat log secara diam (tanpa spam), dan **TIDAK MENGUBAH** konfigurasi runtime.
   - `model.default` tetap `coding-high`.
2. **Pengujian Chat Hermes:**
   - Menjalankan `hermes chat -q "halo" --max-turns 1`.
   - Berhasil merespons via Clouvia Router tanpa error.
