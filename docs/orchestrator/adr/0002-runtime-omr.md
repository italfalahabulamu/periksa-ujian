# ADR 0002: Runtime OMR — pengukuran di browser, klasifikasi di database

- Status: **diusulkan** (final setelah spike S1 lulus dan disetujui di Gerbang 2)
- Tanggal: 2026-10-17
- Terkait: `docs/research/riset-2026-10-17.md`, `docs/omr-template-spec.md`, `docs/omr-spike-plan.md`

## Konteks

PRD mensyaratkan OMR yang idempoten, berversi, tidak menimpa koreksi manual, dan tidak memfinalisasi kasus
meragukan. Stack yang dipakai (Cloudflare + Supabase Free) membatasi komputasi: Workers Free hanya 10 ms CPU,
Edge Function 2 detik CPU dan 256 MB (R1, R2). Pemrosesan halaman A4 penuh tidak muat di sana.

Aturan keras `AGENTS.md` #9: logika kritis berada di Postgres. Ini tampak bertentangan dengan pemrosesan gambar
di klien, kecuali pekerjaan dibelah dua: **mengukur** piksel (butuh gambar) dan **memutuskan** arti ukuran itu
(tidak butuh gambar).

## Keputusan (usulan)

Pembelahan dua tahap:

1. **Pengukuran (klien, Web Worker).** Browser operator memuat halaman (gambar atau PDF lewat pdf.js), mencari
   penanda sudut, menghitung pemetaan template→gambar, dan mengukur **rasio isi tiap gelembung** serta metrik
   kualitas. Keluarannya data mentah, bukan jawaban:
   `{template_version, algorithm_version, quality, id_bubbles[], bubbles[q][opt] = fill_ratio}`.
2. **Klasifikasi (database).** Fungsi Postgres deterministik mengubah ukuran menjadi status per soal
   (`detected`, `blank`, `multiple`, `ambiguous`, `unreadable`) memakai ambang dari `omr_profiles` (hasil
   kalibrasi pilot). Fungsi yang sama dipakai ulang bila ambang diubah, **tanpa memproses ulang gambar**.

Konsekuensi desain:
- Ambang confidence menjadi **data konfigurasi berversi**, bukan konstanta di kode klien (aturan #6).
- Perubahan ambang → klasifikasi ulang di DB; baris dengan `locked_by_review = true` (sudah dikoreksi manusia)
  **tidak disentuh**. Ini memenuhi "reprocessing tidak menimpa koreksi manual".
- Klien tidak pernah mengirim "jawaban akhir", hanya ukuran. Perubahan jawaban oleh manusia hanya lewat
  `review_response` yang menulis `response_reviews` dan audit.
- Idempotensi: kunci `(exam_sheet_id, algorithm_version, template_version)`; kiriman ulang dengan nilai sama
  adalah no-op; dengan nilai berbeda membuat revisi pengukuran baru, bukan menimpa.

## Implementasi bertahap (dipilih lewat spike S1)

| Tahap | Pendekatan | Dipakai bila |
|---|---|---|
| P1 | **JavaScript murni**: deteksi penanda sudut dengan analisis komponen terhubung pada ImageData, homografi 4 titik, sampling hanya di area gelembung (tidak perlu me-*warp* seluruh gambar) | Default; lulus gate S1 |
| P2 | **OpenCV.js** (build kustom, `.wasm` terpisah) | P1 gagal pada foto ponsel/pencahayaan; ukuran dan lisensi dicek (lisensi OpenCV modern diperkirakan Apache 2.0, **belum diverifikasi** dalam sesi riset ini) |
| P3 | **Worker Python/OpenCV** di mesin sekolah atau VPS, mengambil antrean dari Supabase | P1 dan P2 gagal, atau volume melebihi kemampuan browser |

Antarmuka data ke database **sama untuk ketiganya** (`submit_omr_measurements`), sehingga berganti tahap tidak
mengubah skema, RLS, atau UI validasi.

## Opsi yang ditolak

- **Edge Function / Workers memproses gambar:** melanggar batas CPU/memori (R1, R2).
- **Cloudflare Containers:** status dan harga belum terverifikasi (R7), tambahan biaya dan kompleksitas; ditinjau
  ulang hanya bila P1–P3 tidak memadai.
- **OMRChecker sebagai dependensi:** lisensi belum pasti, Python, klaim akurasi tidak berlaku untuk template kita (R4, R5).
- **Model visi/AI untuk membaca gelembung:** tidak deterministik, tidak dapat diaudit, dan membawa data siswa
  ke pihak ketiga. Bertentangan dengan semangat PRD (kasus ambigu harus ke manusia dengan alasan yang dapat dipahami).
- **Klien mengirim jawaban jadi:** melanggar aturan #9 dan menyulitkan kalibrasi ulang.

## Konsekuensi

- Positif: tanpa server komputasi; skala mengikuti jumlah operator; ambang dapat dikalibrasi ulang tanpa scan ulang;
  logika keputusan teruji di tes database; metrik OMR (false acceptance, review rate) dapat dihitung ulang dari data tersimpan.
- Negatif: kecepatan bergantung perangkat operator; hasil bisa berbeda antar-browser bila pustaka gambar berbeda
  (mitigasi: `algorithm_version` + `client_info` disimpan, dan tes lintas-browser di S1); data pengukuran yang
  dikirim klien bisa dipalsukan oleh pengguna yang sah (lihat risiko di bawah).
- Dipantau: memori dekode (R §2), dukungan `OffscreenCanvas`, ukuran bundel.

## Risiko yang diterima dan mitigasinya

| Risiko | Mitigasi |
|---|---|
| Pengguna berwenang mengirim ukuran palsu untuk mengubah jawaban | Setiap kiriman memuat `submitted_by`; gambar asli tersimpan dan `file_hash` dicatat; sampling pemeriksaan ulang oleh orang kedua (P0: laporan "selisih pengukuran vs koreksi"); koreksi manual juga bisa dilakukan sah oleh pengguna yang sama, sehingga kontrol utamanya adalah audit, bukan menutup jalur ini |
| Ukuran dikirim ke lembar yang salah | RPC memeriksa kepemilikan sheet, status ujian, dan `template_version` cocok dengan ujian |
| Hasil berbeda antar perangkat | Fixture sintetis wajib lulus identik di semua browser target; selisih > toleransi menggagalkan CI |

## Syarat penutupan (menjadikan status "diterima")

1. Spike S1 lulus gate di `docs/omr-spike-plan.md` untuk jalur scanner (dan terpisah untuk foto ponsel bila diinginkan).
2. Lisensi pustaka apa pun yang ditambahkan diverifikasi dan dicatat.
3. Pemilik proyek menyetujui ambang awal `omr_profiles`.
