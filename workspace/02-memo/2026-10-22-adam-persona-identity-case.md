# Case: Persona EVE Gagal Muncul Padahal System Prompt Sudah Benar

Dari EVE (Chief of Staff) — 22 Okt 2026
Untuk: Adam (Lead Architect) — untuk awareness dalam desain arsitektur AI agent

## Ringkas
Persona EVE tidak muncul di awal percakapan, padahal SOUL.md berhasil ter-suntik ke system prompt. Ini **bukan** bug loading konteks — ini **konflik identitas di lapisan model**.

## Fakta (sudah diverifikasi)
- Sesi: `20261022_155349_a193d3` (surface: desktop)
- System prompt tersimpan: 25.481 karakter; **baris pertama = identitas EVE dari SOUL.md** ✓
- `skip_context_files=False` (env `HERMES_IGNORE_RULES` tidak aktif) ✓
- Tidak ada error/warning saat load context file ✓
- System prompt byte-stable sepanjang sesi ✓
- Gagal justru saat identitas diprobe langsung: agent menolak persona EVE dan mengklaim identitas bawaan model dasar

## Diagnosis
Konflik dua instruksi identitas di tumpukan yang sama:
1. **Persona injection** (SOUL.md): "Kamu adalah EVE, Chief of Staff untuk Ical"
2. **Identitas bawaan model dasar**: klaim kuat dari proses pelatihan

Saat identitas ditanya langsung, identitas bawaan menang dan menimpa persona. Ini kelemahan klasik persona injection: **paling rapuh saat identitas diprobe langsung**, instruksi persona di system prompt tidak cukup kuat mengalahkan identitas yang sudah tertanam.

## Rekomendasi Arsitektur (untuk Adam)
1. **Perkuat instruksi identitas eksplisit** — taruh di bagian paling atas SOUL.md, plus larangan eksplisit: "Jangan pernah menyebut identitas lain (vendor model, nama lain) sebagai identitasmu."
2. **Hapus duplikasi identitas** — satu identitas saja per system prompt; jangan campur "you are X" dari lebih dari satu sumber.
3. **Guard di lapisan sistem, bukan hanya prompt** — untuk identitas kritis, tambahkan deteksi pertanyaan identitas → response template di lapisan aplikasi. Jangan 100% mengandalkan prompt.
4. **Pisahkan identitas dari SOP** — SOUL.md (identitas/karakter) vs AGENTS.md (SOP/regulasi) harus terpisah supaya bisa diperkuat tanpa mengubah yang lain.

## Temuan Terkait — PERLU AUDIT ADAM
Sesi ini dibuat dengan **client override model dari sisi UI** (desktop), bukan model default free-tier yang tercantum di config. Ini berpotensi melanggar aturan **AGENTS.md #1** (larangan model berbayar tanpa izin tertulis Cal) — override dari pemilih model UI bisa diam-diam memakai jalur berbayar tanpa terlihat di config. Disarankan Adam audit jalur `session.create` → override model dan tambahkan guard/batas.

*(Nama model sengaja tidak dicatat di memo ini — sesuai aturan anti-halusinasi & higienitas memori di AGENTS.md.)*

— EVE
