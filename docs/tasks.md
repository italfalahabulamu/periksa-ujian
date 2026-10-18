# Rencana kerja (usulan)

Menyusun ulang `docs/prd/12-IMPLEMENTATION-BACKLOG.md` (Epic A–G) menjadi modul berurutan dengan dependensi,
gerbang, dan jalur kritis. Ukuran adalah **usaha relatif**, bukan janji tanggal: S ≈ sampai 2 hari, M ≈ 3–5 hari,
L ≈ 1–2 minggu untuk satu pengembang. Roadmap PRD (`docs/prd/10-ROADMAP.md`) memperkirakan ±7–9 minggu total; urutan
di bawah tidak mengubah itu secara material, kecuali paralelisasi spike OMR yang dapat menghemat sekitar satu minggu
**bila D-05..D-07 dijawab lebih awal**. Kapasitas tim dan tanggal ujian (D-16) belum diketahui.

## 0. Jalur pilot ramping (ujian pertama < 1 bulan)

Berdasar jawaban pemilik 2026-10-18: ±150 siswa, PG + esai, foto ponsel, Supabase Free (`decisions.md` §0).
Prinsip: **pangkas luasnya fitur, bukan keamanan dan audit.**

**Masuk pilot:** login dan 4 peran (admin, guru, pemeriksa, operator); data akademik minimal dengan impor CSV
sederhana untuk ±150 siswa; ujian, peserta + kode bercek-digit, soal PG dengan kunci beku, rubrik esai beku,
`grading_config`; template **mode ponsel**; unggah foto yang diperkecil + hash + pengukuran OMR + klasifikasi di DB;
**UI review (sekaligus mode input manual cadangan)**; penilaian esai di layar; hitung nilai; finalisasi dan `reopen_exam`;
audit dan snapshot; ekspor CSV; purge scan terjadwal; RLS dengan tes T-01..T-20 penuh; `keepalive`; cadangan data.

**Ditunda:** XLSX resmi, rekap lanjutan/antarkelas, analisis butir, `amend_final_score` (sementara lewat reopen),
QR per siswa, esai buta, ujian susulan, penugasan per kelompok soal, dashboard lanjutan, mode dua perangkat.

**Tidak boleh dipangkas:** tes "harus ditolak" RLS, audit append-only, versi beku kunci/rubrik/konfigurasi, tes formula,
telaah keamanan sebelum data nyata, dan telaah hukum D-17 sebelum data siswa nyata. Sampai itu selesai pilot memakai data fiktif.

**Urutan yang diubah:** UI review dibangun **sebelum** OMR produksi (M5 mendahului M4), sehingga bila OMR ponsel
tidak lulus, operator tetap bisa memeriksa dengan input manual (`omr-spike-plan.md` §7).

| Minggu (indikatif) | Isi | Titik keputusan |
|---|---|---|
| 1 | Penegasan G1/G2; audit FTS/HRIS ringkas (A-01); M0; **spike S1 jalur ponsel** (cetak template uji, kumpulkan lembar fiktif, generator sintetis, pengukuran JS) | Akhir hari ke-4 spike: gate ponsel (lulus / scanner / input manual) |
| 2 | M1 minimal; M2 (ujian, kunci beku, rubrik, `mark_exam_ready`); M3 (unggah + perkecil + hash + kebijakan storage) | — |
| 3 | M5 (UI review/input manual); M4 (OMR produksi bila lulus); M6 (esai) | Bila M5/M6 tertinggal: pemotongan darurat harus Anda setujui (mis. skor esai per soal, bukan per kriteria) |
| 4 | M7 (hitung, finalisasi, ekspor); M8 (tes RLS penuh, review keamanan, latihan restore, uji coba kering dengan data fiktif, panduan singkat) | **Go/no-go** pemakaian pada ujian pertama |

**Kejujuran jadwal:** rencana 4 minggu ini tanpa cadangan waktu, mengandaikan pengembangan berkelanjutan dan
keputusan cepat; kapasitas tim belum diketahui. Risiko terbesar: OMR dari foto ponsel dan penyiapan Supabase.
Karena itu tetapkan **tanggal cadangan**: bila go/no-go minggu ke-4 gagal, ujian pertama diperiksa dengan cara
sekarang dan aplikasi dipakai untuk ujian berikutnya. Keputusan ini tidak mengurangi kewajiban kualitas di atas.

## 1. Gerbang

| Gerbang | Isi | Keluaran | Status |
|---|---|---|---|
| G1 | PRD dan lingkup MVP | `decisions.md` §C | menunggu |
| A-01 | Audit repo HRIS/FTS | `HRIS-ARCHITECTURE-NOTES.md` | belum |
| G2 | Arsitektur, data, izin, RPC, ancaman, tes | `decisions.md` §D | usulan sudah disusun, menunggu G1 |
| S1 | Spike OMR | `omr-spike-report.md`, ADR-0002 final | menunggu D-05..D-07 |
| G3 | Foundation (M0) | tes hijau, CI, staging | belum |

## 2. Modul

| Modul | Cakupan (backlog) | Bergantung pada | Ukuran | Keluaran utama / kriteria keluar |
|---|---|---|---|---|
| **M0 Foundation** | A-03, A-04, G-01 (dasar) | G2 | L | Build + CSP + SW; CI; harness tes DB; migrasi dasar; `profiles`/role + trigger penjaga; `audit_logs`; Edge Function buat-akun/reset-sandi; `keepalive`; login. **Keluar:** T-01, T-03, T-16, T-17 hijau |
| **M1 Data akademik** | B-01..B-05 | M0 | L | Tahun ajaran, kelas, siswa, mapel, penugasan; impor CSV berpratinjau dan validasi. **Keluar:** role berbeda hanya melihat data yang diizinkan |
| **M2 Ujian & konfigurasi** | C-01..C-07 | M1 | L | Ujian, peserta + kode bercek-digit, soal PG, kunci berversi, rubrik berversi, `grading_config`, registri template & profil OMR, `transition_exam`, `mark_exam_ready`. **Keluar:** ujian dapat disiapkan dan dibekukan tanpa scan |
| **S1 Spike OMR** | D-04, D-05 (prototipe), D-10 | D-05..D-07, perangkat (D-20) | M (≈ 5 hari) | Laporan + ADR-0002 final + `omr_profiles` v1. **Dapat berjalan paralel dengan M0–M2** |
| **M3 Intake & storage** | D-01..D-03 | M2 | M | Bucket privat + policy, `register_sheet_pages` idempoten, UI unggah, status/antrean, batas kuota, rancangan purge (D-14). **Keluar:** T-07..T-09, T-20, AC-03 |
| **M4 OMR produksi** | D-05, D-09 | S1, M3 | L | Modul pengukuran terbukti (versi S1), `submit_omr_measurements`, klasifikasi DB, `reclassify_exam`, pencocokan peserta. **Keluar:** metrik pilot tercatat; AC-04 |
| **M5 Review OMR** | D-06..D-08 | M4 | L | Antrean, viewer berdampingan (zoom/putar/halaman), pintasan papan ketik, riwayat koreksi, prefetch. **Keluar:** pemeriksa dapat menyelesaikan satu kelas tanpa mouse berlebih (uji pengguna) |
| **M6 Esai** | E-01..E-06 | M2, M3 (scan tersedia) | M | Antrean esai, viewer scan + rubrik, skor per kriteria, draf/selesai. **Paralel dengan M4–M5.** **Keluar:** AC-05 |
| **M7 Nilai, finalisasi, laporan** | F-01..F-08 | M5, M6 | L | `compute_exam_results`, guard finalisasi, `finalize/reopen/amend`, `result_snapshots`, laporan, CSV+XLSX. **Keluar:** AC-06, AC-07; semua kasus formula §test-strategy hijau |
| **M8 Keamanan, pilot, rilis** | G-02..G-08 | M7 | L | Matriks RLS lengkap (T-01..T-20), review keamanan independen, latihan restore, e2e, pilot satu ujian, panduan, purge terjadwal, keputusan go-live. **Keluar:** gate pilot `09-TEST-PLAN.md` §4 |

Dependensi (ringkas):

```mermaid
flowchart LR
  G1 --> A01["A-01 audit"] --> G2 --> M0 --> M1 --> M2
  D567["D-05..D-07"] --> S1
  M2 --> M3 --> M4
  S1 --> M4 --> M5 --> M7
  M2 --> M6 --> M7
  M7 --> M8
```

**Jalur kritis:** D-05..D-07 → S1 → M4 → M5 → M7 → M8. Risiko jadwal terbesar ada di S1 dan M4 (OMR); hasilnya
tidak bisa dijanjikan sebelum diuji.

## 3. Urutan kerja yang disarankan

1. Jawab keputusan di `decisions.md` §A (terutama D-12, D-16, D-03, D-05..D-07).
2. Setujui G1; jalankan A-01 (audit FTS/HRIS) dan G2.
3. Mulai M0; **bersamaan** siapkan bahan S1 (cetak template uji, kumpulkan lembar, siapkan perangkat) dan jalankan S1
   segera setelah D-05..D-07 siap, tanpa menunggu M1/M2.
4. Setiap modul: mini-plan → tes dulu → review kode → review keamanan (wajib untuk M0, M3, M7, M8) → e2e →
   verifikasi → laporan modul (SHIP / NEEDS WORK / BLOCKED), `STATE.md` diperbarui.
5. Pilot terbatas hanya setelah M8 dan telaah hukum D-17 untuk data nyata.

## 4. Definition of Ready (per issue)

Tujuan pengguna; konteks dan dependensi; acceptance criteria teruji (rujuk AC-xx / T-xx); kontrak data/RPC bila ada;
dampak keamanan dan RLS; definisi selesai. (Dari `12-IMPLEMENTATION-BACKLOG.md`.)

## 5. Setelah MVP (P1, tidak dibangun sebelum disetujui)

- Cetak lembar jawaban dari aplikasi dengan QR per siswa (D-07 tahap 2) memakai `jsqr.js`.
- Analisis butir soal: tingkat kesukaran `P = benar/peserta`; daya pembeda `D = (B_atas − B_bawah) / n_kelompok` dengan
  kelompok atas/bawah 27% menurut skor total. **Metodologi harus disetujui akademik sebelum dibangun** (PRD).
- Penilaian esai buta (D-18), peserta susulan (D-19), notifikasi, penugasan pemeriksa per kelompok soal,
  perbandingan antarkelas, mode foto ponsel bila gate terpisah lulus.
