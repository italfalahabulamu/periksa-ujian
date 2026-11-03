# Spike 02: akurasi baca pada foto nyata

Protokol lengkap: `docs/11-rnd/spikes/spike-02-protokol.md`.

## Alat
- `make_kit.py <jumlah> <seed> <keluar>` : `ljk.pdf` (cetak 100%, A4), `instruksi.pdf` (daftar isian per lembar untuk pengisi), `kunci.csv` (kebenaran dasar).
- `evaluate.py <folder_kunci> <folder_foto> [laporan.md]` : jalankan pembaca JS (`app/pwa/omr.js`) pada foto bernama `lembar-NN_<ponsel>_<baik|sulit>.jpg`, tulis laporan dan keputusan titik putus.
- `sim_photos.py` : HANYA simulasi, untuk menguji alat sebelum foto nyata ada.

## Alur lapangan
1. Cetak `ljk.pdf` 100% skala (pilih "ukuran sebenarnya", bukan "fit to page"). Cetak `instruksi.pdf` terpisah.
2. Pengisi mengisi tiap LJK mengikuti halaman instruksi dengan nomor yang sama.
3. Foto tiap lembar: kondisi baik dan sulit (bayangan tangan, miring sekitar 15 derajat), minimal 2 ponsel.
4. Taruh foto di satu folder (jangan commit; `tests/fixtures/real/` diabaikan git), jalankan `evaluate.py`.

## Batas
- Uji alat memakai foto simulasi; hasil "LULUS" pada simulasi tidak berarti apa-apa untuk foto nyata.
- Template belum punya kode lembar non-periodik; pembaca mengandalkan gerbang ukuran marka dan skor pendaftaran. Nomor lembar hanya dicetak sebagai teks.
