# Product Requirements Document (PRD)
## Sistem Pemeriksaan Ujian SMP

- **Versi:** 0.1 — Draft
- **Status:** Untuk review
- **Pemilik produk:** Pesantren Modern Al-Falah Abu Lam U
- **Pengguna utama:** Admin akademik, guru mata pelajaran, pemeriksa, pimpinan
- **Platform:** Web responsif, dioptimalkan untuk desktop saat pemeriksaan massal dan tetap dapat digunakan di tablet
- **Arsitektur:** Mengikuti pola HRIS yang sudah ada; rincian framework wajib diverifikasi dari repository

---

## 1. Ringkasan produk

Sistem Pemeriksaan Ujian SMP adalah aplikasi untuk mengelola ujian, memeriksa lembar jawaban hasil pindai/foto, menghitung nilai, dan menyajikan laporan hasil belajar. Pilihan ganda diperiksa menggunakan Optical Mark Recognition (OMR) berbasis template lembar jawaban. Esai diperiksa secara manual oleh guru melalui antarmuka digital dengan rubrik dan skor per kriteria.

Aplikasi harus mengurangi pekerjaan koreksi manual, mempercepat rekap nilai, meminimalkan kesalahan input, dan menyediakan jejak audit untuk setiap perubahan nilai atau kunci jawaban.

## 2. Latar belakang dan masalah

Proses pemeriksaan manual berpotensi:
- Memerlukan waktu lama saat jumlah peserta dan soal banyak.
- Menimbulkan kesalahan hitung atau pemindahan nilai.
- Menyulitkan pelacakan jawaban yang tidak terbaca atau lembar yang perlu diperiksa ulang.
- Menghabiskan waktu untuk rekap nilai dan analisis butir soal.
- Tidak memiliki satu alur terdokumentasi untuk pemeriksaan pilihan ganda dan esai.

## 3. Tujuan produk

1. Mengelola ujian berdasarkan tahun ajaran, kelas, mata pelajaran, dan peserta.
2. Memungkinkan guru menyusun soal pilihan ganda, kunci jawaban, bobot, dan rubrik esai.
3. Membaca lembar jawaban pilihan ganda dari scan/foto dengan OMR dan memberi status keyakinan hasil baca.
4. Memungkinkan validasi manual untuk jawaban kosong, ganda, tidak terbaca, atau meragukan.
5. Memungkinkan guru menilai esai secara manual berdasarkan rubrik.
6. Menghitung nilai akhir sesuai formula yang disepakati.
7. Menyediakan laporan per siswa, kelas, mata pelajaran, dan ujian, serta ekspor CSV/XLSX jika teknologi pendukung sudah dipilih.
8. Menyimpan audit trail untuk tindakan penting.

## 4. Non-goals

Tidak termasuk MVP:
- Penilaian esai otomatis menggunakan AI.
- Proctoring atau pengawasan ujian daring.
- Pembuatan soal otomatis menggunakan AI.
- Aplikasi native Android/iOS.
- Integrasi nilai ke sistem eksternal yang belum ditentukan.
- SSO lintas aplikasi sebelum kebutuhan dan kontrol akses disepakati.
- OMR untuk semua jenis layout kertas secara bebas; MVP memakai template lembar jawaban yang terstandar.

## 5. Pengguna dan kebutuhan

### 5.1 Admin akademik
- Membuat tahun ajaran, kelas, siswa, mata pelajaran, dan penugasan guru.
- Mengelola pengguna dan hak akses sesuai kewenangan.
- Memantau status seluruh proses pemeriksaan.

### 5.2 Guru mata pelajaran
- Membuat ujian, soal, opsi, kunci, bobot, dan rubrik.
- Melihat hasil pembacaan OMR.
- Memvalidasi jawaban yang ditandai meragukan.
- Menilai esai dan memfinalisasi nilai sesuai izin.
- Melihat laporan kelas dan analisis butir soal.

### 5.3 Pemeriksa
- Memeriksa antrean OMR dan/atau esai yang ditugaskan.
- Tidak dapat mengubah konfigurasi akademik atau kunci ujian jika tidak diberi izin.
- Tidak dapat memfinalisasi nilai jika bukan kewenangannya.

### 5.4 Pimpinan
- Melihat dashboard ringkasan dan laporan sesuai cakupan akses.
- Mengunduh laporan jika diberi izin.
- Tidak otomatis memiliki izin mengubah nilai.

### 5.5 Operator pemindaian (opsional)
- Mengunggah berkas scan/foto.
- Mengaitkan berkas dengan ujian dan kelas.
- Melihat kesalahan pemrosesan tanpa dapat mengubah kunci jawaban.

## 6. Ruang lingkup fungsional

### FR-01 — Autentikasi dan otorisasi
Pengguna harus masuk melalui mekanisme autentikasi yang sesuai dengan arsitektur HRIS. Hak akses ditegakkan di server/database, bukan hanya menyembunyikan menu di frontend.

### FR-02 — Data akademik
Sistem mengelola tahun ajaran, semester, kelas, siswa, mata pelajaran, dan penugasan guru. Impor data CSV dapat menjadi fitur MVP jika format sumber data disepakati.

### FR-03 — Pengelolaan ujian
Admin/guru berwenang dapat membuat ujian dengan nama, tahun ajaran, kelas, mata pelajaran, tanggal, jenis ujian, status, jumlah soal, dan skema nilai. Ujian memiliki status draft, siap, berlangsung dalam proses pemeriksaan, final, atau dibatalkan.

### FR-04 — Soal pilihan ganda
Pengguna berwenang dapat membuat nomor soal, teks/asset soal bila diperlukan, opsi jawaban, kunci, bobot, dan status aktif. Perubahan kunci setelah proses pemeriksaan dimulai harus tercatat dan dapat memicu pemeriksaan ulang terkontrol.

### FR-05 — Rubrik esai
Guru dapat menetapkan kriteria, deskripsi tingkat capaian, skor maksimum, dan bobot. Rubrik harus disimpan sebagai versi yang digunakan oleh ujian tersebut.

### FR-06 — Unggah lembar jawaban
Sistem menerima format file yang disepakati (MVP: PDF, JPG, PNG). Berkas dikaitkan dengan ujian, peserta, dan template lembar jawaban. Sistem menolak atau mengarantina berkas yang tidak valid, terlalu besar, atau tidak dapat dibaca.

### FR-07 — Pemrosesan OMR
Sistem mendeteksi area jawaban berdasarkan template, mengidentifikasi tanda pada opsi, dan mengembalikan hasil per nomor beserta status confidence/ambiguity. Pemrosesan gagal tidak boleh diam-diam menghasilkan nilai final.

### FR-08 — Validasi OMR
Pemeriksa dapat melihat gambar lembar jawaban dan hasil baca berdampingan, mengoreksi respons yang salah baca, serta menyimpan alasan/perubahan. Jawaban kosong, ganda, dan tidak terbaca memiliki status eksplisit.

### FR-09 — Pemeriksaan esai
Guru melihat jawaban esai berupa scan/crop atau gambar halaman, memilih skor untuk setiap kriteria rubrik, menambahkan catatan jika diperlukan, dan menyimpan nilai. Sistem tidak menghasilkan skor esai menggunakan AI.

### FR-10 — Perhitungan nilai
Nilai pilihan ganda dan esai dihitung sesuai konfigurasi ujian. Formula harus terlihat dan diuji. Nilai tidak boleh difinalisasi sebelum semua syarat kelengkapan terpenuhi atau pengecualian dicatat.

### FR-11 — Finalisasi dan koreksi
Nilai final dikunci untuk mencegah perubahan tidak sengaja. Perubahan setelah finalisasi membutuhkan izin khusus, alasan, dan audit trail; sistem menyimpan nilai sebelum dan sesudah perubahan.

### FR-12 — Laporan
Laporan minimal mencakup nilai siswa, rekap kelas, nilai PG, nilai esai, nilai akhir, status pemeriksaan, dan ekspor data. Analisis butir soal dapat menyusul setelah validitas perhitungannya disepakati.

### FR-13 — Audit trail
Sistem mencatat pengguna, waktu, entitas, tindakan, nilai sebelum/sesudah bila relevan, dan alasan untuk tindakan sensitif seperti perubahan kunci, koreksi OMR, dan perubahan nilai final.

## 7. Persyaratan nonfungsional

- **Keamanan:** RLS Supabase atau kontrol setara; akses file privat; prinsip least privilege.
- **Privasi:** data siswa hanya dapat dilihat oleh pengguna yang berwenang.
- **Integritas:** foreign key, constraint, validasi server, dan transaksi untuk operasi penting.
- **Auditabilitas:** perubahan nilai/kunci dan finalisasi dapat ditelusuri.
- **Keandalan:** kegagalan pemrosesan scan dapat diulang tanpa membuat duplikasi hasil.
- **Kinerja:** daftar, antrean, dan laporan harus menggunakan pagination/filter; target angka ditetapkan setelah ukuran kelas dan volume scan diketahui.
- **Kegunaan:** alur pemeriksaan mendukung keyboard dan navigasi cepat.
- **Aksesibilitas:** label jelas, kontras memadai, status tidak hanya dibedakan dengan warna.
- **Backup dan pemulihan:** kebijakan backup mengikuti kemampuan dan paket layanan yang dipilih.
- **Kompatibilitas:** browser modern; responsif untuk desktop dan tablet.

## 8. Aturan bisnis

1. Setiap ujian terkait dengan mata pelajaran, kelas/kelompok peserta, dan tahun ajaran.
2. Setiap lembar jawaban harus terhubung ke satu peserta dan satu ujian.
3. Satu peserta tidak boleh memiliki dua hasil aktif untuk ujian yang sama kecuali proses penggantian/retake secara eksplisit diaktifkan.
4. Jawaban OMR ambigu harus menunggu validasi manusia.
5. Kunci jawaban dan rubrik yang sudah dipakai harus memiliki versi atau snapshot.
6. Nilai final tidak dapat diubah tanpa otorisasi dan alasan.
7. Nilai yang belum lengkap tidak boleh disajikan sebagai final.
8. Jika ujian hanya berisi PG atau esai, sistem menghitung komponen tersebut sesuai skala yang ditentukan.
9. Formula bobot harus disimpan per ujian dan tidak berubah diam-diam ketika pengaturan global diubah.

## 9. Formula nilai (baseline yang perlu disetujui)

Untuk komponen pilihan ganda:
`Nilai PG = (total skor PG yang diperoleh / total skor maksimum PG) × 100`

Untuk komponen esai:
`Nilai esai = (total skor esai yang diperoleh / total skor maksimum esai) × 100`

Jika kedua komponen digunakan:
`Nilai akhir = (Nilai PG × bobot PG) + (Nilai esai × bobot esai)`

Bobot PG dan esai disimpan dalam bentuk proporsi dan totalnya harus 1. Contoh: PG 0,70 dan esai 0,30. Jika hanya satu komponen digunakan, nilai akhir adalah nilai komponen tersebut. Formula final perlu dikonfirmasi oleh pimpinan akademik.

## 10. Metrik keberhasilan

- Waktu dari unggah scan hingga hasil PG siap divalidasi.
- Persentase jawaban yang dibaca OMR dengan benar pada pilot.
- Persentase jawaban yang perlu validasi manual.
- Jumlah kesalahan nilai yang ditemukan setelah finalisasi.
- Waktu yang diperlukan untuk rekap nilai satu kelas.
- Persentase pemeriksaan esai yang selesai sesuai tenggat.
- Jumlah tindakan sensitif yang memiliki audit trail lengkap.

Target angka baru ditetapkan setelah pilot menggunakan lembar jawaban dan scanner/perangkat nyata.

## 11. Kriteria rilis MVP

MVP dapat dirilis untuk pilot jika:
- Pengguna dan hak akses berfungsi.
- Admin dapat membuat data dasar dan ujian.
- Kunci PG serta rubrik esai dapat dibuat dan dibekukan sebagai versi.
- Berkas scan dapat diunggah dan diproses dengan status yang jelas.
- Hasil OMR ambigu masuk antrean validasi.
- Guru dapat memberi nilai esai manual.
- Nilai akhir dapat dihitung dan diperiksa ulang.
- Finalisasi dan koreksi meninggalkan audit trail.
- Laporan dasar dapat difilter dan diekspor.
- Uji keamanan RLS dan akses berkas privat lulus.
- Pilot OMR lulus kriteria akurasi yang disepakati oleh tim.

## 12. Risiko utama

- Variasi kualitas scan/foto, rotasi, pencahayaan, dan bentuk tanda.
- Lembar jawaban tidak seragam atau tidak mengikuti template.
- Salah kait antara lembar jawaban dan siswa.
- Perubahan kunci setelah pemeriksaan dimulai.
- Kebocoran data nilai siswa melalui izin yang terlalu luas.
- Ketergantungan pada detail stack HRIS yang belum diaudit.
- Perkiraan waktu OMR terlalu optimistis sebelum uji lapangan.

Mitigasi utama: template standar, kode ujian/lembar yang jelas, validasi manual, pilot terukur, RLS, storage privat, audit trail, dan review repository sebelum implementasi.
