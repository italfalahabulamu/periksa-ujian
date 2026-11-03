# ADR-001: PWA, pembacaan foto di perangkat, data minimal

Status: **usulan** (2026-11-03). Persetujuan PWA dari user sudah ada; sisanya menunggu hasil spike 02.

## Konteks
Ujian pilot dalam sekitar 1 pekan. Toko aplikasi tidak mungkin (akun pribadi baru butuh uji tertutup 12 penguji x 14 hari, lihat findings.md). Data siswa adalah data anak (UU PDP). Akurasi baca foto nyata belum terbukti.

## Keputusan
1. **PWA** (hosting HTTPS statis), bukan APK, untuk pilot. Native tetap R3.
2. **Pembaca OMR berjalan di perangkat** (browser), foto tidak dikirim ke server pada R0. Alasan: tidak ada layanan gambar untuk dijalankan, foto siswa tidak keluar dari ponsel guru.
3. **R0 tanpa backend wajib**: data di perangkat (sudah dibuktikan di mockup) plus ekspor CSV dan cadangan. Supabase masuk R1 untuk akun, sinkron, dan multi-perangkat.
4. **Data siswa hanya kode peserta**; nama tetap di daftar sekolah.
5. **Mode input manual selalu tersedia** (antrean cek ulang), sebagai jalur aman bila pembaca gagal.

## Konsekuensi dan risiko
- Pembaca harus ditulis ulang di JavaScript (referensi: `spikes/omr-01/reader.py`, OpenCV). Pilihan: OpenCV.js (besar, ~8 MB) atau implementasi kecil sendiri. Diputuskan setelah spike 02. BELUM TERVERIFIKASI untuk kecepatan pada ponsel kelas menengah.
- Data di perangkat hilang bila data peramban dihapus atau ponsel hilang: wajib ada cadangan CSV/berkas sebelum R1.
- Template LJK perlu kode lembar non-periodik sebelum dicetak (kelemahan dari spike 01).
- Tanpa akun, tidak ada kontrol akses selain kunci ponsel; cukup untuk pilot dampingan, tidak untuk R1.

## Alternatif ditolak
- APK langsung: butuh penandatanganan dan pemasangan per ponsel, peringatan Play Protect.
- Pembaca di server: butuh layanan gambar dan unggah foto siswa; ditunda.
