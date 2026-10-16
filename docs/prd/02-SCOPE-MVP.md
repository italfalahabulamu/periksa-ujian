# Ruang Lingkup MVP

## 1. Tujuan MVP

Membuktikan bahwa alur inti—mengatur ujian, memindai lembar jawaban PG, memvalidasi OMR, memberi nilai esai secara manual, dan menerbitkan laporan—dapat dilakukan dengan aman dan dapat diaudit.

## 2. Prioritas fitur

### P0 — Wajib untuk pilot
- Login dan role-based access control.
- Data tahun ajaran, kelas, siswa, mata pelajaran.
- Impor siswa/kelas melalui CSV dengan validasi.
- Pembuatan ujian.
- Soal PG, opsi, kunci jawaban, bobot, dan versi kunci.
- Rubrik esai dan versi rubrik.
- Template lembar jawaban standar.
- Upload PDF/JPG/PNG ke storage privat.
- Antrean pemrosesan dan status setiap berkas.
- OMR untuk template yang disetujui.
- Status respons: terbaca, kosong, ganda, ambigu, gagal.
- Validasi manual OMR dengan gambar dan respons berdampingan.
- Penilaian esai oleh guru tanpa AI.
- Perhitungan nilai akhir.
- Finalisasi, pembukaan ulang terkendali, audit trail.
- Laporan nilai dasar dan ekspor CSV.
- RLS dan pengujian akses.

### P1 — Setelah pilot stabil
- Analisis butir soal (tingkat kesukaran dan daya pembeda setelah metodologi disetujui).
- Ekspor XLSX dengan format resmi sekolah.
- Cetak lembar jawaban dari aplikasi.
- Penjadwalan pemeriksaan dan notifikasi.
- Penugasan pemeriksa per kelas atau kelompok soal.
- Perbandingan hasil antarkelas/ujian.

### P2 — Tidak untuk MVP
- Penilaian esai otomatis/AI.
- Ujian daring dan proctoring.
- Aplikasi mobile native.
- Pengakuan layout OMR bebas tanpa template.
- Integrasi dengan LMS atau sistem eksternal sebelum kontrak integrasi jelas.
- SSO HRIS tanpa desain dan persetujuan terpisah.

## 3. Di luar cakupan

- Sistem manajemen pembelajaran lengkap.
- Bank soal lintas sekolah.
- Pembayaran atau PSB.
- Penilaian karakter dan rapor komprehensif.
- Otomatisasi keputusan kenaikan kelas.

## 4. Asumsi MVP

- Sekolah menggunakan satu template lembar jawaban per format ujian.
- Kualitas scan dapat dikendalikan dan resolusi minimum ditetapkan saat pilot.
- Daftar peserta dan kelas tersedia dalam format yang dapat diimpor.
- Guru memiliki perangkat untuk meninjau scan esai.
- Formula nilai akhir ditetapkan sebelum ujian diproses.

## 5. Definition of Done

Satu fitur dianggap selesai jika:
1. Kriteria penerimaan dipenuhi.
2. Validasi frontend dan server tersedia.
3. Hak akses diuji pada role yang relevan.
4. Error/loading/empty states tersedia.
5. Perubahan skema database dan migrasi terdokumentasi.
6. Audit trail tersedia untuk operasi sensitif.
7. Pengujian otomatis atau checklist pengujian manual ditambahkan.
8. Dokumentasi penggunaan diperbarui.
