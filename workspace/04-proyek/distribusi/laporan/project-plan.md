# Project Plan: Distribusi Rokok Alami Pacitan

## 1. Analisis Awal

| Item | Nilai |
|------|-------|
| Modal per bungkus | Rp 7.600 |
| Harga ke reseller | Rp 8.600 |
| Margin Ical per bungkus | Rp 1.000 |
| Harga jual akhir (reseller → konsumen) | Rp 10.000 - 11.000 |
| Margin reseller per bungkus | Rp 1.400 - 2.400 |
| Stok saat ini | 2.000 bungkus (Madju PRO SKT 800 + Sukses Alami SKT 800 + Sample Madju PRO 200 + Sample Sukses Alami 200) |
| Modal total | Rp 15.200.000 |
| Profit maksimal (jual semua ke reseller) | Rp 2.000.000 |
| Volume break-even (revenue = modal) | 1.768 bungkus (≈ 88% stok) |

## 2. Milestone 3 Tahap

### Tahap 1: Optimasi Batch Ini (2.000 bks)
- Implementasi tracking setiap unit yang keluar (reseller, jumlah, tanggal, harga)
- Strategi sample: hanya untuk promocional, catat distribusi ke influencer/warung pilihan
- Identifikasi reseller terbaik: pilih 5 mitra dengan potensi volume tinggi, beri insentif kecil jika target tercapai

### Tahap 2: Scale-up Batch Selanjutnya
- Cari reseller tetap (kontrak bulanan) dengan sistem order teratur
- Fokus pada warung/toko di sekitar sekolah, kantor, dan pasar tradisional
- Bangun database reseller dan segmentasikan berdasarkan wilayah dan volume potensi

### Tahap 3: Sistem Dropship & Otomatisasi
- Siapkan dropship melalui platform e-commerce (Tokopedia, Shopee) untuk konsumen akhir
- Otomatisasi order: integrasi WhatsApp/Telegram bot untuk pencatatan pesanan
- Laporan otomatis mingguan (volume, pendapatan, kas) ke Ical

## 3. Rekomendasi Konkret untuk Ical
- Buat spreadsheet tracking: kolom tanggal, nama reseller, jumlah (bungkus), jenis produk, harga per bungkus, total, catatan
- Pisahkan stok sample dan karton: sample tidak boleh dijual; catat penggunaan sample untuk uji coba dan promosi
- Lakukan survey harga ke reseller setiap minggu untuk memastikan HET tetap Rp 10.000-11.000
- Siapkan mekanisme pembayaran cepat (transfer bank atau e-wallet) dalam 24 jam setelah penyerahan
- Jadwalkan pertemuan koordinasi bulanan dengan top 5 reseller untuk evaluasi dan penyesuaian
- Buat kode voucher khusus untuk reseller yang mencapai target volume bulanan (misal: diskon Rp 200/bungkus untuk 3 bulan ke depan)

## 4. Tugas untuk Agent Fungsional

### Analyst
- Hitung margin dan sensitivitas harga (simulasi perubahan +/- 10% harga jual)
- Buat forecast permintaan bulanan berdasarkan data penjualan awal 2 minggu
- Identifikasi wilayah dengan konsentrasi warung tinggi untuk prioritas ekspansi
- Hitung titik kembali modal (break-even) dengan berbagai skenario harga reseller

### Developer
- Bangun aplikasi tracking sederhana (Google Sheet + Apps Script atau web mini) untuk mencatat stok, penjualan, dan komisi
- Integrasikan dengan WhatsApp API untuk notifikasi pesanan baru dan konfirmasi pembayaran
- Buat dashboard visualisasi penjualan harian, mingguan, dan bulanan (grafik garis dan pie)
- Siapkan otomatis kirim laporan mingguan ke email Ical via script

### Strategist
- Rencana roadmap 6 bulan: target jumlah reseller aktif, volume distribusi, dan pendapatan
- Evaluasi peluang dropship: risiko, keuntungan, dan mitra logistik untuk pengiriman langsung ke konsumen
- Definisikan KPI utama: volume terjual per bulan, rata-rata waktu pembayaran reseller, tingkat kepuasan reseller (survey)
- Buat matriks SWOT untuk bisnis distribusi saat ini dan rekomendasi strategi pertumbuhan