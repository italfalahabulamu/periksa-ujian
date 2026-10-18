# STATE: periksa-ujian — Sistem Pemeriksaan Ujian SMP

**Terakhir diperbarui:** 2026-10-17
**Fase aktif:** F1 (Plan & Architecture) — usulan Gerbang 2 sudah disusun   **Modul aktif:** -   **Mode:** perencanaan
**Menunggu:** penegasan resmi Gerbang 1 dan 2 dari pemilik proyek (keputusan inti sudah dijawab 2026-10-18, lihat `docs/decisions.md` §0); lalu audit FTS/HRIS (A-01) dan spike OMR S1 (jalur foto ponsel)

## Keputusan terkunci
| # | Keputusan | Tanggal | Sumber |
|---|---|---|---|
| 1 | Repo aplikasi terpisah: `italfalahabulamu/periksa-ujian` | 2026-10-17 | Permintaan pengguna |
| 2 | Struktur berkas awal mengikuti commit fondasi FTS | 2026-10-17 | Permintaan pengguna |
| 3 | Baseline produk = paket PRD v0.1 (`docs/prd/`) | 2026-10-17 | Berkas dari pengguna |
| 4 | Riset dan perencanaan Fase 1 dilakukan (dokumen saja, tanpa kode) | 2026-10-17 | Permintaan pengguna |
| 5 | Skala: ±150 siswa per ujian; PG + esai (2–3 halaman esai); soal per siswa > 10 (jumlah pasti belum diketahui) | 2026-10-18 | Jawaban pemilik |
| 6 | Ujian pertama < 1 bulan → **pilot ramping + OMR** (cakupan dipotong; `tasks.md` §0) | 2026-10-18 | Jawaban pemilik |
| 7 | Supabase: proyek baru terpisah, **tetap Free** (slot belum diverifikasi) | 2026-10-18 | Jawaban pemilik |
| 8 | Template baru dari aplikasi; kode peserta berdigit pemeriksa; operator memakai laptop Chrome/Edge | 2026-10-18 | Jawaban pemilik |
| 9 | Sumber scan: **foto ponsel** (menyimpang dari rekomendasi scanner; scanner = cadangan) | 2026-10-18 | Jawaban pemilik |
| 10 | Kebijakan nilai sesuai rekomendasi D-08/D-09; scan dihapus 90 hari setelah final | 2026-10-18 | Jawaban pemilik |

## Baseline PRD (berlaku sebagai usulan sampai G1 disetujui)
- Esai dinilai guru; tidak ada penilaian esai oleh AI.
- Hasil OMR yang kosong/ganda/ambigu/gagal masuk antrean validasi manusia, tidak difinalisasi otomatis.
- Kunci, rubrik, dan formula dibekukan sebagai versi; finalisasi dan perubahan sesudahnya diaudit.
- Data akademik ujian dipisah dari data HRIS; SSO HRIS tidak otomatis.

## Hasil riset yang mengubah rencana (detail: `docs/research/riset-2026-10-17.md`)
1. Workers Free (10 ms CPU) dan Edge Function (2 detik CPU) tidak cocok untuk memproses gambar → pengukuran OMR di browser, klasifikasi di Postgres (ADR-0002, diusulkan).
2. Storage 1 GB Supabase Free tidak cukup untuk satu periode ujian penuh dengan esai → perlu purge scan dan/atau Pro (D-14, D-03).
3. Proyek Free dijeda setelah 1 minggu idle dan dibatasi 2 proyek aktif → `keepalive`, kemungkinan proyek terpisah di Pro.
4. OMRChecker tidak dijadikan dependensi (lisensi belum terverifikasi, klaim akurasi bukan milik kita).

## Status gerbang
| Gerbang | Isi | Status | Tanggal |
|---|---|---|---|
| G1 | PRD dan lingkup MVP | **menunggu** (`decisions.md` §C) | |
| A-01 | Audit repo HRIS/FTS → `HRIS-ARCHITECTURE-NOTES.md` | belum | |
| G2 | Arsitektur dan stack (ADR-0001..0003, ERD, matriks izin, kontrak RPC, ancaman, tes) | **usulan disusun**, menunggu G1 dan keputusan (`decisions.md` §D) | |
| S1 | Spike OMR (`omr-spike-plan.md`) | menunggu D-05..D-07, D-20 | |
| G3 | Foundation (M0) | belum | |

## Status modul (rencana di `docs/tasks.md`)
| Modul | Status | Coverage | Temuan terbuka | Rekomendasi |
|---|---|---|---|---|
| M0 Foundation | belum mulai | | | |
| M1 Data akademik | belum mulai | | | |
| M2 Ujian & konfigurasi | belum mulai | | | |
| S1 Spike OMR | belum mulai | | | |
| M3 Intake & storage | belum mulai | | | |
| M4 OMR produksi | belum mulai | | | |
| M5 Review OMR | belum mulai | | | |
| M6 Esai | belum mulai | | | |
| M7 Nilai, finalisasi, laporan | belum mulai | | | |
| M8 Keamanan, pilot, rilis | belum mulai | | | |

## Keputusan terbuka (lihat `docs/decisions.md`; rekomendasi sudah ada di setiap baris)
Sudah dijawab 2026-10-18: D-03, D-05, D-06, D-07, D-08, D-09, D-12, D-14, D-16, D-20 (dan D-02 oleh keputusan #1).
Belum: D-01 (default: ikut FTS), D-04, D-10, D-11, D-13 (gate S1 sebagai titik awal), D-15, D-17 (telaah hukum), D-18, D-19, D-21, D-22.
Data yang masih dibutuhkan: jumlah soal pasti, jumlah mapel + tanggal ujian pertama, jenis ponsel, panjang kode peserta,
konfirmasi slot Supabase Free.

## Risiko terbuka
- **Tiga pilihan pemilik saling menekan:** tenggat < 1 bulan + OMR dari foto ponsel (belum terbukti) + Supabase Free
  (1 GB). Mitigasi: titik putus keputusan di akhir spike dan mode input manual cadangan (`tasks.md` §0,
  `omr-spike-plan.md` §7); foto diperkecil sebelum diunggah; pilot hanya 1–2 ujian di Free.
- Foto ponsel iPhone berformat HEIC umumnya tidak terbaca browser desktop; foto yang dikirim lewat aplikasi pesan
  bisa terkompresi. SOP pemotretan wajib (`omr-template-spec.md` §8).
- Pilot dengan data siswa nyata sebelum telaah hukum (D-17) berisiko; gunakan data fiktif sampai jelas.
- OMR adalah komponen paling tidak pasti; akurasi dan estimasi tidak boleh dijanjikan sebelum S1 dan pilot.
- Kapasitas storage Free; model kapasitas belum diukur dengan scan nyata (S1).
- Jumlah proyek Supabase di organisasi belum diketahui; bisa memaksa Pro.
- Ketentuan UU PDP untuk data anak belum ditelaah resmi (D-17).
- Stack diusulkan dari FTS; audit HRIS langsung (A-01) belum dilakukan.
- Lisensi OMRChecker dan OpenCV, status Cloudflare Containers belum terverifikasi (tidak menghalangi rencana).
- Token GitHub pernah ditempel di chat pada 2026-10-17; harus dicabut dan diganti (gunakan konektor GitHub).

## Asumsi belum terkonfirmasi
- Supabase Free dipakai seperti FTS; rekomendasi berubah ke Pro bila D-12/D-14 menuntut.
- Satu template lembar jawaban per format ujian pada MVP.
- Pilot pada satu ujian dengan jumlah peserta terbatas (angka di D-12).
- Ukuran berkas scan per halaman (0,2–0,8 MB) adalah asumsi; diukur di S1.

## Langkah berikutnya
1. Pemilik proyek menegaskan Gerbang 1 (cakupan pilot ramping) dan Gerbang 2 (arsitektur), serta menyerahkan data yang masih dibutuhkan.
2. Audit FTS/HRIS (A-01) versi ringkas.
3. Siapkan bahan S1 jalur ponsel (cetak template uji mode ponsel, meja pemotretan, 50–150 lembar isian fiktif) lalu jalankan spike;
   mulai M0 dan UI review (yang juga menjadi mode input manual) secara paralel.
