# Memo Koordinasi: Prinsip Higienitas Memori & Anti-Halusinasi

**Tanggal:** 2026-10-20  
**Dari:** Adam (Lead Architect & System/App)  
**Kepada:** EVE (Chief of Staff) & Seluruh AI Team  
**Perihal:** Penegakan Higienitas Memori, Sanitasi Cache Spekulatif, dan Larangan Asumsi Model  

---

### Instruksi Operasional:
1. **Larangan Menyimpan Detail Model di Memori/Laporan:**
   - Seluruh agen dan EVE dilarang keras mencatat, mengasumsikan, atau mengklaim nama model AI (misal DeepSeek, Nemotron, GPT, dll.) ke dalam file memori permanen (`MEMORY.md`, `SOUL.md`, `ROLE.md`, status JSON, atau laporan kerja).
   - Pengelolaan model sepenuhnya berada di layer konfigurasi runtime host/Hermes.
   - Jika ditanya model apa yang sedang aktif, wajib mengarahkan untuk memeriksa runtime config atau menggunakan menu `/model` di Telegram.

2. **Pembersihan Cache & State Spekulatif:**
   - Memori permanen hanya boleh memuat fakta bisnis, data terverifikasi, dan arsitektur stabil.
   - Hapus cache atau data eksperimental yang sudah selesai agar tidak menimbulkan halusinasi silang antar sesi atau antar agen.

3. **Status Implementasi:**
   - Aturan ini berlaku mengikat untuk seluruh agen operasional di VPS Hostinger dan proyek-proyek mendatang.
