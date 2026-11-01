# Spike 01: Akurasi pembacaan LJK dari foto ponsel

**Status:** dijalankan sebagian pada data sintetis (2026-11-01). Hasil: `spike-01-hasil.md`. Foto nyata belum. Hasil spike ini dibuang setelah dipakai belajar; bukan fondasi produksi kecuali Technical Lead menyetujui.

## Pertanyaan
Dengan template LJK buatan kita (marka sudut + bulatan jawaban), seberapa akurat foto ponsel biasa dibaca, dan seberapa sering sistem harus meminta guru memeriksa ulang?

## Rancangan
1. Buat satu template LJK (misalnya 40 soal, pilihan A-E) dengan marka sudut.
2. Isi minimal 30 lembar dengan variasi nyata: pensil dan pulpen, bulatan terisi penuh, setengah, dihapus sebagian, dan dicoret.
3. Foto tiap lembar dengan berbagai ponsel (termasuk kelas menengah ke bawah), tiga kondisi cahaya, dan kemiringan wajar. Catat jawaban sebenarnya per lembar (kebenaran dasar).
4. Bandingkan dua pendekatan: (a) OMRChecker dengan template kita, (b) pipeline OpenCV sederhana berbasis marka sudut.
5. Ukur: akurasi per bulatan, jumlah bulatan yang ditandai "ragu", jumlah salah baca yang tidak ditandai (paling berbahaya), waktu proses per lembar.

## Kriteria sukses (USULAN, perlu disetujui user di Gerbang 1)
- Salah baca yang tidak ditandai: ≤ 0,5% dari bulatan.
- Bulatan yang ditandai "ragu": ≤ 5%, dan semua bisa dikoreksi guru dalam satu ketukan.
- Bila gagal: opsi (1) templat lebih sederhana (bulatan lebih besar, jarak lebih longgar), (2) foto dengan panduan bingkai di kamera, (3) beralih ke pemindai/foto dengan kontrol cahaya.

## Batas
Maksimal 3 hari kerja. Tidak ada data siswa nyata; lembar diisi relawan atau dibuat sintetis.

## Keputusan yang bergantung pada hasil
Pembacaan di perangkat atau di server; apakah Edge Functions cukup atau perlu layanan Python.
