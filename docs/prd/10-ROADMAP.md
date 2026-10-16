# Roadmap Pengembangan

Estimasi waktu adalah indikatif dan bergantung pada kondisi repository HRIS, kemampuan tim, dan hasil pilot OMR.

## Tahap 0 — Audit dan keputusan (3–5 hari kerja)

- Audit repository HRIS, framework, komponen UI, autentikasi, Supabase, Cloudflare, CI/CD.
- Sepakati apakah aplikasi berada di repo terpisah atau monorepo.
- Konfirmasi template lembar, jumlah soal, jenis scan, formula nilai, dan role.
- Buat architecture decision records (ADR) untuk keputusan penting.

**Exit criteria:** tidak ada asumsi teknologi inti yang belum terverifikasi.

## Tahap 1 — Fondasi aplikasi (minggu 1)

- Setup repo dan environment sesuai HRIS.
- Login, role, layout, navigasi, dan design system.
- Data tahun ajaran, kelas, siswa, mapel, penugasan.
- Migration dan RLS awal.
- Import CSV dengan validasi dasar.

**Exit criteria:** role yang berbeda hanya dapat melihat data yang diizinkan.

## Tahap 2 — Setup ujian dan rubrik (minggu 2)

- CRUD ujian dan peserta.
- Input/import soal PG dan kunci.
- Rubrik esai.
- Versi kunci/rubrik.
- Formula nilai dan validasi kesiapan ujian.

**Exit criteria:** ujian dapat disiapkan dan dibekukan tanpa proses scan.

## Tahap 3 — Upload dan OMR pilot (minggu 3–4 atau lebih)

- Storage privat dan batch upload.
- Definisi template.
- Prototipe alignment dan deteksi bubble.
- Status respons dan antrean validasi.
- Antarmuka review berdampingan.
- Uji dengan scan nyata dan iterasi.

**Exit criteria:** hasil pilot memenuhi kriteria yang disepakati; kasus ambigu tidak difinalisasi otomatis.

## Tahap 4 — Esai, nilai, dan laporan (minggu 4–5 atau lebih)

- Antarmuka penilaian esai per kriteria.
- Perhitungan nilai.
- Finalisasi dan pembukaan ulang terkendali.
- Audit trail.
- Laporan dan ekspor CSV.

**Exit criteria:** end-to-end test lulus.

## Tahap 5 — Pilot terbatas dan rilis (1–2 minggu)

- Pilot pada satu ujian dan jumlah peserta yang ditentukan.
- Bandingkan hasil OMR dengan pemeriksaan manual.
- Perbaiki UX, performa, dan kebijakan validasi.
- Pelatihan pengguna.
- Rilis bertahap dan monitoring.

**Exit criteria:** persetujuan pemilik produk dan tim akademik.

## Risiko jadwal

OMR dapat menjadi komponen dengan ketidakpastian tertinggi. Jangan menjanjikan akurasi atau tanggal rilis OMR massal sebelum uji scan nyata. Estimasi di atas tidak menggantikan penilaian kapasitas developer dan kondisi repository.
