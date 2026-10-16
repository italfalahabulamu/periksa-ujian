# STATE: periksa-ujian — Sistem Pemeriksaan Ujian SMP

**Terakhir diperbarui:** 2026-10-17
**Fase aktif:** F0 (Discovery & Plan)   **Modul aktif:** -   **Mode:** kickoff
**Menunggu:** persetujuan Gerbang 1 (PRD dan lingkup) dan jawaban atas keputusan terbuka di bawah

## Keputusan terkunci
| # | Keputusan | Tanggal | Sumber |
|---|---|---|---|
| 1 | Repo aplikasi terpisah: `italfalahabulamu/periksa-ujian` | 2026-10-17 | Permintaan pengguna |
| 2 | Struktur berkas awal mengikuti commit fondasi FTS | 2026-10-17 | Permintaan pengguna |
| 3 | Baseline produk = paket PRD v0.1 (`docs/prd/`) | 2026-10-17 | Berkas dari pengguna |

## Baseline PRD (berlaku sebagai usulan sampai G1 disetujui)
- Esai dinilai guru; tidak ada penilaian esai oleh AI.
- Hasil OMR yang kosong/ganda/ambigu/gagal masuk antrean validasi manusia, tidak difinalisasi otomatis.
- Kunci, rubrik, dan formula dibekukan sebagai versi; finalisasi dan perubahan sesudahnya diaudit.
- Data akademik ujian dipisah dari data HRIS; SSO HRIS tidak otomatis.

## Status gerbang
| Gerbang | Isi | Status | Tanggal |
|---|---|---|---|
| G1 | PRD dan lingkup MVP | **menunggu** | |
| G2 | Arsitektur dan stack (ADR-0001, ADR-0002 OMR, ERD, matriks izin, kontrak RPC) | belum | |
| G3 | Foundation | belum | |

## Status modul
Modul akan ditetapkan di G2 dari Epic A–G di `docs/prd/12-IMPLEMENTATION-BACKLOG.md`.
Usulan awal urutan: Foundation (A) → Data akademik (B) → Ujian dan kunci (C) → Prototipe OMR (D) →
Esai (E) → Nilai dan laporan (F) → Keamanan dan rilis (G).

| Modul | Status | Coverage | Temuan terbuka | Rekomendasi |
|---|---|---|---|---|
| A Foundation | belum mulai | | | |
| B Data akademik | belum mulai | | | |
| C Ujian dan kunci | belum mulai | | | |
| D Upload dan OMR | belum mulai | | | |
| E Penilaian esai | belum mulai | | | |
| F Nilai dan laporan | belum mulai | | | |
| G Keamanan dan rilis | belum mulai | | | |

## Keputusan terbuka (lihat `docs/prd/11-OPEN-DECISIONS.md`)
D-01 framework (usulan: ikut FTS, perlu konfirmasi) · D-03 Supabase project sama/terpisah dari HRIS ·
D-04 login/SSO HRIS · D-05 format lembar jawaban · D-06 sumber scan · D-07 identifikasi peserta ·
D-08 skor jawaban ganda · D-09 formula PG/esai dan pembulatan · D-10 perubahan nilai final ·
D-11 ekspor · D-12 volume lembar · D-13 target akurasi OMR · D-14 retensi scan · D-15 akses scan.
D-02 (repo terpisah) sudah terjawab oleh keputusan #1.

## Risiko terbuka
- OMR adalah komponen paling tidak pasti; estimasi dan akurasi tidak boleh dijanjikan sebelum uji pada scan nyata.
- Runtime OMR belum diputuskan; library native belum tentu berjalan di Cloudflare tanpa uji.
- Format lembar jawaban dan sumber scan belum ditetapkan; keduanya menentukan desain OMR.
- Stack diusulkan dari FTS; audit repository HRIS langsung (A-01) belum dilakukan.
- Token GitHub pernah ditempel di chat pada 2026-10-17; harus dicabut dan diganti (gunakan konektor GitHub).

## Asumsi belum terkonfirmasi
- Supabase Free dipakai seperti FTS (tanpa email, reset sandi oleh admin); belum dikonfirmasi untuk aplikasi ini.
- Satu template lembar jawaban per format ujian pada MVP.
- Pilot dilakukan pada satu ujian dengan jumlah peserta terbatas (angka ditetapkan di D-12).

## Langkah berikutnya
1. Pengguna menyetujui/mengubah PRD (Gerbang 1) dan menjawab keputusan terbuka, mulai dari D-03 sampai D-09.
2. Audit HRIS/FTS (A-01) → `HRIS-ARCHITECTURE-NOTES.md`.
3. Fase 1: ADR final, ERD, matriks izin, kontrak RPC, rencana prototipe OMR (Gerbang 2).
