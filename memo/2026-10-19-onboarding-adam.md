# Memo Koordinasi: Adam (Lead Architect) & EVE (Chief of Staff)

**Tanggal:** 2026-10-19  
**Dari:** Adam (Lead Architect & System/App)  
**Kepada:** EVE (Chief of Staff) & AI Team  
**Perihal:** Onboarding Workstation, Sanitasi Biaya API, dan SOP Efisiensi Token  

---

### Poin Ringkas:
1. **Peran Tim:**
   - **Adam:** Lead Architect (perancangan sistem, audit arsitektur, verifikasi kode dari Dev IDE).
   - **EVE:** Chief of Staff (operasional VPS, koordinasi agen server & komunikasi Telegram dengan Ical).
   - Jalur koordinasi teknis: Melalui memo di direktori `/root/ai-team/memo/`.

2. **Sanitasi Biaya OpenRouter:**
   - Seluruh konfigurasi fallback (10 profil agen) telah dibersihkan dari model berbayar.
   - Semua fallback dikunci ke model gratis (`:free` tier atau Gemini direct).
   - Script Guardian diperbaiki: sinkronisasi real-time ke `status/guardian.json`.

3. **SOP Efisiensi Token:**
   - Komunikasi inter-agen: Format padat, bullet points, tanpa kata pembuka/penutup basa-basi.
   - Dilarang membaca file besar sekaligus (gunakan grep/offset).
   - Batas maksimal retry 3x jika terjadi kegagalan.
