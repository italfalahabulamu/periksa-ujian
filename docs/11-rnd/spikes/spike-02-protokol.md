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
