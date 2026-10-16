# Test Plan dan Acceptance Criteria

## 1. Jenis pengujian

- Unit test: formula nilai, validasi skor, status ujian, aturan respons.
- Integration test: database, RLS, upload storage, worker OMR.
- End-to-end test: buat ujian → upload scan → review → nilai esai → finalisasi → laporan.
- Security test: role boundaries, akses file, manipulasi request, akses lintas ujian.
- Usability test: admin, guru, dan pemeriksa menjalankan tugas umum.
- Pilot OMR: scan nyata dari perangkat dan kondisi yang akan digunakan sekolah.

## 2. Acceptance criteria per alur

### AC-01 — Hak akses
- Pengguna tanpa sesi tidak dapat membuka data ujian.
- Guru tidak dapat mengakses ujian yang tidak ditugaskan melalui URL/API langsung.
- Pimpinan tidak dapat mengubah nilai jika hanya diberi izin baca.
- Operator scan tidak dapat membuka data yang tidak diperlukan untuk tugasnya.
- Pengujian RLS membuktikan aturan berlaku pada query langsung.

### AC-02 — Setup ujian
- Ujian tidak dapat ditandai siap jika peserta, soal/kunci yang diperlukan, template, atau formula belum lengkap.
- Sistem menolak nomor soal duplikat.
- Kunci dan rubrik yang telah digunakan tidak bisa diubah tanpa versi/audit yang benar.

### AC-03 — Upload scan
- File tidak valid ditolak dengan pesan yang jelas.
- Upload ulang yang sama tidak menciptakan duplikasi tanpa peringatan/aturan.
- File tersimpan di bucket privat.
- Pengguna melihat status upload dan pemrosesan.

### AC-04 — OMR
- Sistem menyimpan status per respons.
- Respons ambigu/ganda/tidak terbaca tidak difinalisasi otomatis.
- Hasil dapat dibandingkan dengan scan asli.
- Koreksi manual menyimpan pengguna, waktu, nilai sebelumnya, nilai baru, dan alasan bila diwajibkan.
- Reprocessing tidak menimpa koreksi manual secara diam-diam.

### AC-05 — Esai
- Guru memasukkan skor per kriteria.
- Sistem menolak skor di bawah 0 atau di atas skor maksimum.
- Esai yang belum dinilai mencegah finalisasi jika komponen esai wajib.
- Tidak ada penilaian esai otomatis oleh AI.

### AC-06 — Nilai dan finalisasi
- Formula yang disimpan menghasilkan nilai yang sama dengan perhitungan uji.
- Bobot PG dan esai berjumlah 1 bila kedua komponen aktif.
- Finalisasi menyimpan snapshot formula, versi kunci/rubrik, pengguna, dan waktu.
- Pembukaan ulang membutuhkan izin dan alasan.
- Perubahan setelah finalisasi dapat ditelusuri.

### AC-07 — Laporan
- Nilai per siswa konsisten dengan hasil ujian.
- Filter kelas/mapel/ujian tidak membocorkan data lintas cakupan akses.
- Ekspor CSV sama dengan data yang terlihat dan sesuai filter.

## 3. Uji formula contoh

PG: skor diperoleh 36 dari maksimum 40 → nilai PG 90.
Esai: skor diperoleh 24 dari maksimum 30 → nilai esai 80.
Bobot PG 70%, esai 30%:
`Nilai akhir = (90 × 0,70) + (80 × 0,30) = 87`.

Kasus uji wajib mencakup:
- ujian PG saja;
- ujian esai saja;
- bobot nol/invalid;
- jawaban kosong;
- jawaban ganda;
- nilai esai belum lengkap;
- peserta tidak hadir;
- ujian dibuka ulang setelah finalisasi.

## 4. Gate sebelum pilot

- [ ] Data siswa/kelas uji sudah disiapkan.
- [ ] Template lembar jawaban ditetapkan.
- [ ] Dataset scan pilot disetujui.
- [ ] Kriteria akurasi OMR dan batas review manual disepakati.
- [ ] Formula nilai disetujui pimpinan akademik.
- [ ] RLS dan storage privat diuji.
- [ ] Backup dan rollback tersedia.
- [ ] Guru dan operator menerima panduan singkat.
