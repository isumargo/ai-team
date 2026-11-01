# Proyek: Perbaikan AI Agent

Tujuan: merapikan arsitektur, SOP, state, dan operasional tim AI agar sumber kebenaran jelas, mudah dirawat, dan konteks kerja bisa di-handoff antar sesi.

**Lokasi kanonis:** `/root/ai-team/workspace/04-proyek/ai-agent-improvement/` (folder ini ikut tersinkron ke PC melalui Syncthing). Tidak ada salinan kedua di `projects/`.

## Dokumen proyek

- `HANDOFF.md` — konteks terkini untuk sesi/agen berikutnya. **Baca pertama.**
- `STATUS.md` — ringkasan progres satu halaman.
- `DECISIONS.md` — keputusan yang sudah disetujui; jangan menebak keputusan baru.
- `PLAN.md` — fase dan ruang lingkup kerja.
- `SESSION-LOG.md` — riwayat kronologis, bukan sumber status terbaru.
- `SOURCE-OF-TRUTH.md` — peta file ke canonical ke owner.
- `architecture/` — big picture (markdown canonical; `.excalidraw` dan `.html` adalah artefak export).
- `backlog/` — temuan dan tugas yang belum dikerjakan.
- `status-audit/` — arsip snapshot status lama (bukan status live).

## Aturan pemeliharaan konteks

1. Awal sesi: baca `HANDOFF.md`, lalu `STATUS.md`, lalu `DECISIONS.md`.
2. Sebelum mengakhiri sesi: perbarui `HANDOFF.md` dan `STATUS.md`, tambah satu entri ringkas ke `SESSION-LOG.md`.
3. Catat fakta terverifikasi sebagai fakta, dugaan sebagai dugaan, serta waktu pemeriksaan.
4. Jangan simpan secrets, token, password, credential, atau dump percakapan.
5. Jangan mengubah runtime, menghapus data, membuka firewall, atau mengubah billing tanpa izin eksplisit Ical.
6. Perubahan yang bersentuhan dengan konfigurasi aktif harus memiliki backup/rollback dan langkah verifikasi.
7. Repo ini sumber kerja tim; jangan push tanpa memeriksa perubahan lain yang belum disetujui.
8. Prinsip desain: Agile, terstruktur, scalable, aman tanpa mengganggu operasional, resilient, aturan jelas, mudah dikembangkan.
