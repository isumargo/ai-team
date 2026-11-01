# Arsitektur & Big Picture Hermes VPS

Peta sistem hasil audit awal; menggambarkan runtime, alur kerja, sumber data, repo, service VPS, dan temuan kondisi. Detail status layanan/kuota adalah snapshot saat dibuat dan perlu diverifikasi ulang sebelum tindakan.

## File dalam folder ini

- `truth-map.md` — sumber teks utama (canonical).
- `truth-map.excalidraw` — diagram untuk diedit di excalidraw.com.
- `truth-map.html` — viewer/editor Mermaid offline.
- `build_excalidraw.py` — generator diagram Excalidraw.
- `sync_map.py` — generator HTML dan pembaca hasil edit.
- `mermaid/` — bundle Mermaid offline.
- `gen_truth_map.py` — generator lama, dipertahankan untuk rujukan.

## Alur perubahan

1. Ubah `truth-map.md` untuk edit fakta/dokumentasi.
2. Jalankan `python3 sync_map.py html` untuk regenerate `truth-map.html`.
3. Edit `truth-map.excalidraw` secara visual; kirim file export ke EVE untuk dibaca dan disinkronkan.
4. Jalankan `python3 build_excalidraw.py` untuk regenerate diagram dari definisi generator.

> `build_excalidraw.py` menggambar struktur terkurasi, tidak otomatis mengonversi semua teks Mermaid dari `truth-map.md`.
