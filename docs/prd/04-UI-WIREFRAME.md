# Wireframe UI — Draft

Wireframe berikut berupa struktur teks, bukan desain visual final. Komponen, token desain, navigasi, dan pola responsif perlu mengikuti HRIS.

## 1. Dashboard

```text
┌─────────────────────────────────────────────────────────────────────┐
│ Logo / Sistem Pemeriksaan Ujian       Tahun Ajaran ▼  Profil ▼      │
├───────────────┬─────────────────────────────────────────────────────┤
│ Dashboard     │ Dashboard                                           │
│ Akademik      │ [Ujian aktif] [Lembar diproses] [Perlu validasi]    │
│ Ujian         │ [Esai belum dinilai] [Ujian siap finalisasi]        │
│ Pemeriksaan   │                                                     │
│ Laporan       │ Pemeriksaan terbaru                                │
│ Pengaturan    │ ┌────────┬────────┬──────────┬───────────┐           │
│               │ │ Ujian  │ Kelas  │ Progres  │ Status    │           │
│               │ └────────┴────────┴──────────┴───────────┘           │
│               │                                                     │
│               │ [Lanjutkan pemeriksaan] [Buat ujian]                │
└───────────────┴─────────────────────────────────────────────────────┘
```

### Prinsip dashboard
- Tampilkan pekerjaan yang perlu tindakan, bukan hanya angka statistik.
- Kartu “Perlu validasi” membuka antrean terkait.
- Semua metrik mengikuti cakupan akses pengguna.
- Jangan tampilkan data siswa sensitif kepada role yang tidak berhak.

## 2. Detail ujian

```text
Ujian: Penilaian Akhir Semester IPA Kelas VIII
Status: DRAFT

[Ringkasan] [Peserta] [Soal PG] [Rubrik Esai] [Template] [Versi]

Informasi:
- Tahun ajaran
- Kelas/kelompok
- Mata pelajaran
- Tanggal
- Jumlah peserta
- Komposisi nilai PG / esai

Checklist kesiapan:
[ ] Peserta terverifikasi
[ ] Kunci PG selesai
[ ] Rubrik esai selesai
[ ] Template lembar sesuai
[ ] Formula nilai disetujui

[Simpan Draft] [Tandai Siap]
```

## 3. Antrean OMR

```text
Pemeriksaan: Ujian IPA Kelas VIII
Batch: scan-2026-001

[Total lembar] [Sukses] [Perlu review] [Gagal]

Filter: [Status ▼] [Kelas ▼] [Cari siswa...]

┌─────────────┬─────────────┬───────────────┬──────────────┐
│ Identitas   │ Status OMR  │ Isu            │ Aksi         │
├─────────────┼─────────────┼───────────────┼──────────────┤
│ Siswa A     │ Perlu review│ Nomor 12 ganda │ Validasi     │
│ Siswa B     │ Selesai     │ -              │ Lihat        │
└─────────────┴─────────────┴───────────────┴──────────────┘
```

## 4. Validasi OMR — tampilan inti

```text
┌─────────────────────────────┬──────────────────────────────────────┐
│ Gambar lembar jawaban       │ Hasil pembacaan                      │
│                             │ No. 1  A B C D   Terbaca: B           │
│ [Zoom] [Putar] [Fit]        │ No. 2  A B C D   Ambigu: B/C          │
│                             │ No. 3  A B C D   Kosong               │
│                             │                                      │
│                             │ Pilih respons final untuk soal aktif │
│                             │ [A] [B] [C] [D] [Kosong] [Ganda]      │
│                             │ [Simpan koreksi] [Berikutnya]         │
└─────────────────────────────┴──────────────────────────────────────┘
```

- Gambar asli tidak boleh ditimpa oleh hasil koreksi.
- Perubahan respons harus dicatat.
- Keyboard shortcuts dapat ditambahkan setelah alur dasar stabil.
- Status confidence tidak boleh menjadi satu-satunya informasi; sediakan alasan/indikator yang dapat dipahami pemeriksa.

## 5. Penilaian esai

```text
Siswa: Siswa A             Soal esai: Nomor 4
┌──────────────────────────────┬─────────────────────────────────────┐
│ Scan jawaban siswa           │ Rubrik                              │
│ [Zoom] [Halaman sebelumnya]  │ Kriteria 1 (maks 4): [0..4]         │
│ [Halaman berikutnya]         │ Kriteria 2 (maks 3): [0..3]         │
│                              │ Kriteria 3 (maks 3): [0..3]         │
│                              │ Catatan guru: [...................]  │
│                              │ Total: 8/10                          │
│                              │ [Simpan Draft] [Selesai Menilai]     │
└──────────────────────────────┴─────────────────────────────────────┘
```

## 6. Finalisasi

- Ringkasan komponen PG dan esai.
- Daftar lembar yang belum selesai.
- Daftar respons OMR belum divalidasi.
- Daftar skor esai belum lengkap.
- Ringkasan formula dan bobot.
- Konfirmasi finalisasi dengan peringatan bahwa perubahan berikutnya memerlukan prosedur khusus.

## 7. Respons UI yang wajib

Semua halaman data perlu memiliki loading, empty, error, permission denied, dan success states. Operasi unggah/pemrosesan harus memperlihatkan progres dan opsi retry yang aman.
