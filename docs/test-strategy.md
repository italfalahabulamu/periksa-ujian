# Strategi tes (usulan untuk Gerbang 2)

Melengkapi `docs/prd/09-TEST-PLAN.md` (AC-01..AC-07). Prinsip: **tes ke Postgres sungguhan**, tes dulu
(RED→GREEN→REFACTOR), tidak ada klaim lulus tanpa keluaran nyata, tidak ada data siswa nyata di repo.

## 1. Lapisan

| Lapisan | Alat | Isi | Target |
|---|---|---|---|
| Unit (JS) | Vitest | Pengukuran OMR pada gambar sintetis, geometri/homografi, validasi form, format/ekspor, pembersih sel ekspor | ≥ 80% logika bisnis |
| Database | Postgres 16 lokal + skrip `test-db.sh` (pola FTS) | Klasifikasi respons, skor, formula nilai, transisi status, guard finalisasi, trigger penjaga, RLS (T-01..T-20), append-only | semua jalur kritis |
| Integrasi | Vitest + Supabase lokal/staging | RPC end-to-end, storage + signed URL, idempotensi unggah | alur utama |
| E2E | Playwright (bila terpasang di lingkungan; bila tidak, dilaporkan jujur) | Buat ujian → unggah sintetis → review → esai → finalisasi → laporan; per peran | AC-01..AC-07 |
| Keamanan | Tes T-xx + review independen + scan secret | Matriks `permissions-rls.md`, `threat-model.md` | sebelum pilot |
| Kinerja | Skrip ukur | Waktu/lembar, memori puncak, kueri antrean/laporan dengan data sintetis 600 siswa × 50 soal | ukur, bukan klaim |
| Pilot OMR | Scan nyata | Metrik di `omr-spike-plan.md` | gate pilot |
| Guru/operator | Sesi uji pengguna | Tugas umum dengan data fiktif | sebelum rilis |

## 2. Aset tes yang dibangun lebih dulu

1. **Generator lembar sintetis** (dari `sheet_templates.layout`): menghasilkan gambar dengan isian acak yang
   kebenarannya diketahui, dengan derau, rotasi, skala, kontras, **perspektif, bayangan bergradasi, blur, distorsi lensa ringan (mode ponsel)**,
   dan cacat (penanda terpotong, isian ganda,
   hapusan). Dipakai oleh tes unit OMR, tes lintas-browser, dan E2E (tanpa data nyata).
2. **Fixture akademik fiktif**: 1 tahun ajaran, 3 kelas, 90 siswa, 3 mapel, 5 pengguna per peran.
3. **Tabel kasus formula** (lihat §3) sebagai data uji bersama untuk tes DB dan tes UI.
4. **Matriks RLS** yang dibangkitkan dari `permissions-rls.md` §2 sehingga tabel/role baru memaksa kasus baru.

## 3. Kasus formula nilai (wajib)

Rumus PRD: `nilai_pg = skor_pg/maks_pg×100`, `nilai_esai = skor_esai/maks_esai×100`,
`akhir = nilai_pg×w_pg + nilai_esai×w_esai`, bobot total 1.

| Kasus | Masukan | Hasil |
|---|---|---|
| PRD contoh | PG 36/40, esai 24/30, bobot 0,7/0,3 | 87,00 |
| PG saja | PG 36/40, `w_pg=1` | 90,00 |
| Esai saja | esai 24/30, `w_esai=1` | 80,00 |
| Pembulatan | PG 1/3 (33,333…), esai 2/3 (66,666…), 0,5/0,5 | 50,00 (bulatkan sekali di akhir) |
| Pembulatan batas | akhir 84,005 | 84,01 (setengah menjauhi nol). Float biner memberi 84,00 (diverifikasi di Python), itulah alasan memakai `numeric` |
| Bobot tak valid | 0,6/0,3; negatif; > 1 | ditolak (CHECK) |
| Bobot nol | `w_esai=0` tetapi ada soal esai | ditolak atau esai dinonaktifkan eksplisit |
| Kosong | 5 kosong dari 40, `blank_policy=zero` | skor butir 0, tidak mengurangi |
| Ganda terkonfirmasi | `multiple_policy=zero` | 0 |
| Esai belum lengkap | satu kriteria `draft` | finalisasi diblokir |
| Peserta tidak hadir | status `absent` | tanpa nilai; tidak memblokir finalisasi |
| Reopen setelah final | `reopen_exam` → ubah → `finalize_exam` | snapshot revisi bertambah, lama tetap |
| Kunci diubah di tengah | versi 2 dibekukan | skor dihitung ulang; skor menyimpan versi kunci |

## 4. Tes properti dan invarian

- Skor PG ∈ [0, maks_pg]; nilai akhir ∈ [0,100]; monotonik terhadap skor mentah.
- Mengubah ambang tidak mengubah baris `locked_by_review`.
- Mengirim pengukuran yang sama dua kali tidak menambah baris respons (idempotensi).
- Transisi status tidak sah (mis. `draft → finalized`) selalu ditolak, apa pun peran.
- Jumlah `result_snapshots` per peserta non-menurun; tidak ada UPDATE/DELETE yang berhasil.

## 5. Gerbang CI

`lint`, `test` (unit), `test:db` (RLS + RPC), pemeriksaan guard (tanpa inline handler, CSP, tanpa `service_role`
di bundel, fungsi definer punya `search_path`, tanpa `console.log`), scan secret, build. `test:e2e` dijalankan di
staging atau lokal sesuai ketersediaan. Merge hanya bila hijau.

## 6. Larangan

- Tidak memakai scan/nilai siswa nyata di fixture, log, atau CI.
- Tidak memakai mock database untuk menyatakan RLS aman (pelajaran HRIS/SAF).
- Tidak menyatakan angka akurasi/kinerja OMR sebelum S1 dan pilot menghasilkannya.
