# STATE: periksa-ujian — Sistem Pemeriksaan Ujian SMP

**Terakhir diperbarui:** 2026-10-17
**Fase aktif:** F1 (Plan & Architecture) — usulan Gerbang 2 sudah disusun   **Modul aktif:** -   **Mode:** perencanaan
**Menunggu:** jawaban pemilik proyek atas `docs/decisions.md` §A, lalu persetujuan Gerbang 1; setelah itu audit FTS/HRIS (A-01) dan Gerbang 2

## Keputusan terkunci
| # | Keputusan | Tanggal | Sumber |
|---|---|---|---|
| 1 | Repo aplikasi terpisah: `italfalahabulamu/periksa-ujian` | 2026-10-17 | Permintaan pengguna |
| 2 | Struktur berkas awal mengikuti commit fondasi FTS | 2026-10-17 | Permintaan pengguna |
| 3 | Baseline produk = paket PRD v0.1 (`docs/prd/`) | 2026-10-17 | Berkas dari pengguna |
| 4 | Riset dan perencanaan Fase 1 dilakukan (dokumen saja, tanpa kode) | 2026-10-17 | Permintaan pengguna |

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
Urutan jawab: D-12 + D-16 → D-03 → D-05/D-06/D-07 → D-14 → D-08/D-09 → D-17.
Lainnya: D-01, D-04, D-10, D-11, D-13, D-15, D-18..D-22. D-02 terjawab oleh keputusan #1.

## Risiko terbuka
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
1. Pemilik proyek menjawab `decisions.md` §A dan menyetujui/mengubah PRD (Gerbang 1).
2. Audit FTS/HRIS (A-01) dan penutupan Gerbang 2.
3. Siapkan bahan S1 (cetak template uji, lembar isian fiktif, perangkat) lalu jalankan spike; mulai M0 secara paralel.
