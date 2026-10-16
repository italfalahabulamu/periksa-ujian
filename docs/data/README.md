# Data dasar yang harus disiapkan

Berkas di folder ini adalah **template kosong**. Isi dengan data sekolah, lalu impor lewat fitur impor CSV
(backlog B-04) setelah fiturnya ada. **Jangan commit data siswa nyata ke repo ini**; simpan berkas terisi di
luar git atau di Supabase Storage privat.

Format kolom di bawah adalah usulan awal. Final setelah D-12 (volume) dan B-04 (impor CSV) diputuskan.

| Berkas | Isi | Kolom |
|---|---|---|
| `classes.template.csv` | Daftar kelas/rombel per tahun ajaran | `academic_year`, `semester`, `class_name`, `grade_level` |
| `students.template.csv` | Siswa dan keanggotaan kelas | `student_code`, `full_name`, `class_name`, `academic_year` |

## Aturan

- `student_code` unik per siswa dan dipakai untuk kode peserta pada lembar jawaban (lihat D-07).
- Satu siswa hanya boleh punya satu kelas aktif per tahun ajaran.
- Data pribadi seminimal mungkin: tidak perlu NIK, alamat, atau kontak orang tua.
- Validasi impor: tolak baris dengan kode ganda, kelas tidak dikenal, atau nama kosong; tampilkan preview sebelum menyimpan.
