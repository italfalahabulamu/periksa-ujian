# Sitemap dan Alur Pengguna

## 1. Sitemap

```text
/login
/dashboard
├── /akademik
│   ├── /tahun-ajaran
│   ├── /kelas
│   ├── /siswa
│   ├── /mata-pelajaran
│   └── /penugasan-guru
├── /ujian
│   ├── /baru
│   └── /[examId]
│       ├── /pengaturan
│       ├── /peserta
│       ├── /soal-pg
│       ├── /rubrik-esai
│       ├── /template-lembar
│       └── /versi
├── /pemeriksaan
│   ├── /unggah
│   ├── /[batchId]
│   │   ├── /status
│   │   ├── /validasi-omr
│   │   ├── /nilai-esai
│   │   └── /finalisasi
├── /laporan
│   ├── /nilai
│   ├── /rekap-kelas
│   └── /analisis-soal
├── /pengaturan
│   ├── /pengguna
│   ├── /peran
│   └── /audit
└── /profil
```

Rute adalah usulan konseptual. Penamaan dan pola routing final harus mengikuti repository HRIS.

## 2. Alur utama: membuat ujian

1. Admin/guru membuka **Ujian → Buat Ujian**.
2. Mengisi nama ujian, tahun ajaran, kelas, mapel, tanggal, peserta, dan skema nilai.
3. Memasukkan soal PG dan kunci, atau mengimpor data sesuai format yang didukung.
4. Menetapkan rubrik untuk esai.
5. Memilih template lembar jawaban dan jumlah soal.
6. Meninjau ringkasan, lalu mengubah status menjadi **Siap Diperiksa**.
7. Setelah pemeriksaan dimulai, perubahan kunci/rubrik memerlukan versi baru atau proses koreksi terkendali.

## 3. Alur utama: memeriksa PG melalui OMR

1. Operator/guru memilih ujian dan mengunggah PDF/JPG/PNG.
2. Sistem memvalidasi file, membuat batch, dan menyimpan file di storage privat.
3. Sistem membaca identitas lembar dan posisi tanda berdasarkan template.
4. Setiap respons diberi status dan skor keyakinan.
5. Respons yang jelas masuk hasil sementara; respons ambigu, kosong, ganda, atau gagal masuk antrean review sesuai aturan.
6. Pemeriksa melihat gambar dan hasil OMR berdampingan.
7. Pemeriksa menyimpan koreksi; perubahan tercatat di audit trail.
8. Sistem menghitung skor PG sementara.
9. Setelah seluruh lembar memenuhi aturan kelengkapan, komponen PG dapat ditandai selesai.

## 4. Alur utama: menilai esai

1. Guru membuka antrean esai sesuai penugasan.
2. Sistem menampilkan scan/crop jawaban siswa dan rubrik versi ujian.
3. Guru memasukkan skor per kriteria dan komentar opsional.
4. Sistem memvalidasi skor tidak melebihi batas kriteria.
5. Guru menyimpan nilai sebagai draft.
6. Pemeriksa/guru yang berwenang menyelesaikan penilaian.
7. Nilai final baru dapat dihitung ketika komponen wajib lengkap.

## 5. Alur finalisasi

1. Sistem menampilkan jumlah peserta, lembar selesai, respons yang belum tervalidasi, esai belum dinilai, dan pengecualian.
2. Pengguna berwenang memeriksa ringkasan.
3. Sistem memblokir finalisasi jika ada pekerjaan wajib yang belum selesai, kecuali pengecualian formal diizinkan.
4. Pengguna mengonfirmasi finalisasi.
5. Sistem menyimpan snapshot formula, versi kunci/rubrik, nilai, pengguna, waktu, dan audit event.
6. Perubahan setelah finalisasi memerlukan izin khusus dan alasan.

## 6. State machine ujian

```text
DRAFT
  └── READY
       └── PROCESSING
            └── REVIEW
                 └── READY_TO_FINALIZE
                      └── FINALIZED
                           └── REOPENED (izin khusus + alasan)
```

Transisi harus divalidasi di backend/database, bukan hanya dikontrol melalui tombol UI.
