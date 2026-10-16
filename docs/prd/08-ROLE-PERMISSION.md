# Role dan Hak Akses

Matriks ini adalah baseline; finalisasi mengikuti struktur organisasi dan praktik HRIS.

| Kemampuan | Admin akademik | Guru | Pemeriksa | Pimpinan | Operator scan |
|---|---:|---:|---:|---:|---:|
| Melihat dashboard | Ya | Ya, terbatas | Ya, terbatas | Ya | Ya, terbatas |
| Mengelola tahun ajaran/kelas/siswa | Ya | Tidak* | Tidak | Baca sesuai izin | Tidak |
| Membuat ujian | Ya | Ya, jika ditugaskan | Tidak | Tidak | Tidak |
| Mengubah soal/kunci | Ya | Ya, sebelum dikunci | Tidak | Tidak | Tidak |
| Mengubah rubrik | Ya | Ya, sebelum dikunci | Tidak | Tidak | Tidak |
| Mengunggah scan | Ya | Ya, jika ditugaskan | Ya, jika ditugaskan | Tidak | Ya |
| Memvalidasi OMR | Ya | Ya, jika ditugaskan | Ya, jika ditugaskan | Tidak | Tidak |
| Menilai esai | Ya* | Ya, jika ditugaskan | Ya, jika ditugaskan | Tidak | Tidak |
| Finalisasi nilai | Izin khusus | Izin khusus | Tidak secara default | Tidak secara default | Tidak |
| Membuka ulang nilai final | Izin khusus + alasan | Izin khusus + alasan | Tidak | Tidak | Tidak |
| Melihat laporan | Ya | Kelas/mapel terkait | Pemeriksaan terkait | Sesuai cakupan | Status proses saja |
| Melihat audit trail | Ya, terbatas | Tindakan sendiri/yang relevan | Tindakan sendiri/yang relevan | Baca jika diizinkan | Tidak |

`*` Hak dapat diubah sesuai keputusan sekolah. Hak istimewa harus diberikan secara eksplisit dan diuji.

## Prinsip otorisasi

- Default deny: jika tidak ada izin eksplisit, akses ditolak.
- Role tidak boleh menjadi satu-satunya pembatas; cek juga penugasan guru, kelas, dan ujian.
- Pimpinan tidak otomatis memiliki izin mengubah nilai.
- Operator scan tidak dapat membaca nilai esai atau kunci jika tidak diperlukan.
- Perubahan nilai final selalu memerlukan izin khusus, alasan, dan audit.
- Pengujian RLS harus mencakup akses langsung ke API dan storage, bukan hanya UI.
