# Spike 02: akurasi baca pada foto nyata (protokol lapangan)

Tujuan: mengukur salah baca tak ditandai dan foto ditolak pada lembar nyata. Ambang dari spike 01: salah baca tak ditandai <= 0,5%, foto ditolak <= 25% (titik putus pilot).

## Bahan
- 30 LJK dari template aplikasi (40 soal, A-E), dicetak A4 **100% skala** (bukan "fit to page").
- Pulpen/pensil seperti dipakai siswa. Diisi oleh orang nyata, bukan disimulasikan.
- Minimal 2 jenis ponsel, cahaya kelas biasa.

## Prosedur
1. Tiap lembar diisi dengan jawaban acak yang **dicatat di lembar kunci terpisah** (kebenaran dasar). Sertakan: 5 lembar dengan hapusan, 5 dengan dua bulatan terisi, 5 isian tipis, 5 kertas agak melengkung/terlipat.
2. Foto tiap lembar 2 kali per ponsel: kondisi baik, dan kondisi sulit (bayangan tangan, miring sekitar 15 derajat).
3. Beri nama berkas `lembar-NN_ponselX_baik|sulit.jpg`. Foto asli **tidak masuk git** (`tests/fixtures/real/` sudah diabaikan).
4. Jalankan pembaca; bandingkan dengan kunci.

## Yang dilaporkan
- Jumlah soal dibaca benar, salah baca tak ditandai, ditandai ragu, ditolak; per ponsel dan per kondisi.
- Keputusan: ambang lulus -> pembaca dipakai di pilot; gagal -> mode input manual.

## Batasan
- Bergantung pada izin sekolah memotret lembar siswa; gunakan lembar uji yang diisi guru/relawan, bukan lembar ujian siswa, bila izin belum ada.
- Pembaca sebenarnya di browser belum ditulis; sementara dipakai `reader.py` pada foto yang sama.

## Catatan 2026-11-04: pembaca JS (app/pwa/omr.js)
Port JavaScript murni dari reader.py sudah ada dan diuji pada set sintetis baru (seed 3, 36 foto, 1.320 soal; `spikes/omr-01/make_set.py` + `app/pwa/test_omr.py`):
- Salah baca tak ditandai: 0 dari 1.320 soal; ditandai ragu/ganda: 144 (sekitar 11%); 1 lembar kondisi berat ditolak.
- Paritas dengan reader.py: 1.319 dari 1.320 soal sama. Waktu rata-rata 0,5 detik per foto di Chromium server.
- **BELUM TERVERIFIKASI**: foto nyata, kecepatan di ponsel kelas menengah, dan integrasi ke antarmuka PWA (kamera + template LJK aplikasi memakai geometri yang sama dengan TPL di omr.js). Tanpa nol salah baca pada foto nyata, hasil ini hanya bukti bahwa port setara dengan versi Python.
