# ADR 0003: Model data — versi beku, snapshot hasil, numerik, dan state machine di database

- Status: **diusulkan** (final di Gerbang 2)
- Tanggal: 2026-10-17
- Terkait: `docs/data-model.md`, `docs/rpc-contracts.md`, `docs/prd/06-DATABASE-SCHEMA.md`

## Konteks

PRD meminta: kunci/rubrik/formula berversi, nilai final tidak dapat berubah tanpa jejak, transisi status
divalidasi di backend, dan skor tidak disimpan sebagai angka yang bisa ditimpa tanpa histori. Rancangan PRD
(`06-DATABASE-SCHEMA.md`) bersifat konseptual dan memiliki beberapa celah yang perlu ditutup sebelum migrasi.

## Keputusan (usulan)

1. **Versi beku, bukan edit di tempat.**
   - `answer_key_versions` dan `rubric_versions` berstatus `draft` → `frozen`. Versi `frozen` tidak dapat diubah
     (trigger menolak UPDATE/DELETE pada baris anaknya).
   - `freeze_answer_key` membuat nomor versi berikutnya. Ujian menunjuk `active_answer_key_version_id`.
   - Perubahan kunci setelah pemeriksaan dimulai: versi baru + alasan + audit + **hitung ulang skor** (kunci tidak
     memengaruhi status OMR, hanya skor). Skor menyimpan `answer_key_version_id` yang dipakai.
2. **Konfigurasi penilaian dibekukan pada `ready`.** `exams.grading_config` (bobot PG/esai, kebijakan kosong/
   ganda, pembulatan) hanya dapat diubah selama `draft`. Setelah `ready`, perubahan hanya lewat `reopen`.
3. **Snapshot hasil append-only.** `exam_results` adalah keadaan kerja (boleh dihitung ulang sampai finalisasi).
   Saat `finalize_exam`, `amend_final_score`, atau `reopen_exam`, sistem menulis baris di `result_snapshots`
   (revisi bertambah, tidak pernah diubah/dihapus) berisi nilai, bobot, versi kunci/rubrik, pelaku, alasan.
4. **Numerik.** Skor dan nilai memakai `numeric` (bukan `float`): skor butir `numeric(7,2)`, nilai komponen dan
   akhir `numeric(6,2)`. Pembulatan dilakukan **sekali**, pada nilai akhir, dengan `round(numeric, 2)` (setengah
   menjauhi nol; untuk nilai non-negatif sama dengan setengah ke atas). Komponen tidak dibulatkan sebelum digabung.
5. **State machine ujian** (`draft → ready → processing → review → ready_to_finalize → finalized → reopened → review`;
   `cancelled` dari status non-final): satu fungsi `transition_exam(exam_id, to_status, reason)` dengan tabel
   transisi sah dan *guard* per transisi. Tidak ada `UPDATE exams SET status` dari klien (kolom dijaga trigger).
6. **State machine lembar** (`uploaded → measured → ready | needs_review | failed`; `superseded` untuk
   pengukuran lama): ditulis hanya oleh RPC intake.
7. **Lembar multi-halaman.** Tabel `sheet_pages` (halaman per lembar) — PRD hanya `storage_path` di `exam_sheets`,
   padahal satu siswa bisa punya halaman PG dan halaman esai.
8. **Lembar belum cocok dengan peserta.** `exam_sheets.participant_id` boleh `NULL` (kode peserta tidak terbaca/
   tidak cocok). Lembar tanpa peserta menghalangi `ready_to_finalize`, kecuali dikecualikan formal.
9. **Enum status memakai huruf kecil snake_case** (selaras `06-DATABASE-SCHEMA.md`); huruf besar hanya dalam
   diagram dan label UI. (Menyimpang dari FTS yang memakai huruf besar; alasan: ikut PRD proyek ini.)
10. **Penghapusan.** FK `ON DELETE RESTRICT`; tidak ada hard delete data akademik/hasil. Purge scan
    (retensi D-14) adalah satu-satunya penghapusan terjadwal, hanya objek storage + baris `sheet_pages` ditandai
    `purged_at`; hasil, respons, dan audit tetap.
11. **Aktor dan waktu** diisi trigger dari `auth.uid()` dan `now()`; klien tidak mengirimnya.

## Konsekuensi

- Positif: sejarah nilai dan kunci dapat direkonstruksi; finalisasi dan koreksi dapat dibuktikan; perubahan ambang
  OMR tidak merusak koreksi manusia; model mudah diuji (fungsi murni di DB).
- Negatif: lebih banyak tabel dan fungsi daripada rancangan PRD; hitung ulang skor perlu dioptimalkan (set-based,
  satu ujian per transaksi); butuh tes database yang disiplin.
- Dipantau: ukuran `audit_logs` dan `result_snapshots` (kecil dibanding scan); indeks untuk laporan.

## Penyimpangan dari rancangan PRD (disengaja)

| PRD | Usulan | Alasan |
|---|---|---|
| `exams.class_id` tunggal | Peserta lewat `exam_participants`; kelas opsional lewat `exam_classes` | Ujian bisa lintas kelas/paralel |
| `exam_sheets.storage_path` | `sheet_pages` per halaman | PG + esai multi-halaman |
| `exam_results` sebagai satu-satunya hasil | `exam_results` (kerja) + `result_snapshots` (bukti) | Histori finalisasi/koreksi |
| `student_responses.confidence` | `measurements jsonb` + status; `confidence` diturunkan bila bermakna | Klasifikasi ulang tanpa gambar |
| `question_options` wajib | Opsional di MVP (hanya `option_count`) | D-21: teks soal tidak disimpan di MVP |
