# Kontrak RPC (usulan untuk Gerbang 2)

Semua fungsi: `security definer`, `set search_path = public, pg_temp`; aktor dari `auth.uid()`; menolak bila
`app_role()` NULL; menulis `audit_logs` untuk aksi bertanda **[A]**; mengembalikan kode galat stabil (mis. `E_STATE`,
`E_PERM`, `E_VALIDATION`, `E_CONFLICT`) tanpa membocorkan detail internal. **Idempoten** berarti pemanggilan ulang
dengan argumen sama tidak mengubah hasil.

## 1. Setup ujian

| RPC | Izin | Prasyarat | Efek | Idempoten |
|---|---|---|---|---|
| `create_exam(...)` **[A]** | admin; guru yang mengampu | tahun ajaran, mapel ada | buat ujian `draft` | tidak (membuat baru) |
| `update_exam_config(exam, patch)` **[A]** | `can_edit_config` | status `draft`; bobot valid (jumlah = 1 bila dua komponen) | ubah nama/tanggal/`grading_config` | ya |
| `set_exam_participants(exam, student_ids[])` **[A]** | `can_edit_config` | `draft`; siswa aktif | isi `exam_participants` + `participant_code` bercek-digit | ya |
| `upsert_question(exam, number, type, option_count, max_score)` | `can_edit_config` | `draft`; nomor unik | ubah daftar soal | ya |
| `save_answer_key_draft(exam, rows[])` | admin/guru | versi `draft` | simpan kunci draf | ya |
| `freeze_answer_key(exam, reason)` **[A]** | admin/guru pemilik | semua soal PG aktif punya kunci | buat versi `frozen` baru, set aktif; bila `processing/review` → hitung ulang skor | tidak (versi baru) |
| `freeze_rubric(exam, reason)` **[A]** | admin/guru pemilik | tiap soal esai punya kriteria; total skor kriteria = `max_score` | versi rubrik `frozen` | tidak |
| `mark_exam_ready(exam)` **[A]** | admin/guru pemilik | peserta ≥ 1; kunci beku; rubrik beku bila ada esai; template & profil OMR terpilih; bobot valid | `draft → ready`; bekukan peserta & konfigurasi | ya |
| `cancel_exam(exam, reason)` **[A]** | admin | status bukan `finalized` | `cancelled` | ya |

## 2. Intake dan OMR

| RPC | Izin | Prasyarat | Efek | Idempoten |
|---|---|---|---|---|
| `create_scan_batch(exam, label)` | `can_upload` | `ready`/`processing` | buat batch | tidak |
| `register_sheet_pages(batch, pages[{page_no, file_hash, mime, bytes}])` | `can_upload` | tipe/ukuran sah | buat/ambil `exam_sheets` + `sheet_pages`; ujian `ready → processing` | **ya** (hash+page sama → sheet yang sama; hash sudah ada di sheet lain → `E_CONFLICT` dengan petunjuk duplikat) |
| `submit_omr_measurements(sheet, template, algo_version, quality, id_bubbles, bubbles, client_info)` | `can_upload` | sheet milik ujian itu; template cocok dengan ujian | simpan `sheet_measurements` revisi baru, klasifikasi → `student_responses`; cocokkan peserta dari kode; status sheet `ready`/`needs_review`/`failed` | **ya** (isi identik = no-op; beda = revisi baru, revisi lama `superseded`) |
| `report_sheet_failure(sheet, code, detail)` | `can_upload` | — | status `failed` + kode (`no_markers`, `low_quality`, `template_mismatch`, `file_unreadable`) | ya |
| `request_reprocess(sheet, reason)` **[A]** | `can_review` | sheet bukan `superseded` | tandai agar klien mengukur ulang; **tidak** menyentuh respons `locked_by_review` | ya |
| `reclassify_exam(exam, omr_profile)` **[A]** | admin/guru pemilik | profil `approved`; ujian bukan `finalized` | klasifikasi ulang semua pengukuran tanpa gambar; lewati `locked_by_review` | ya |
| `match_sheet_participant(sheet, participant, reason)` **[A]** | `can_review` | peserta belum punya sheet aktif | set `participant_id`, `match_source=manual` | ya |
| `close_intake(exam)` **[A]** | admin/guru pemilik | tidak ada sheet `uploaded` yang belum terukur (atau ditandai gagal) | `processing → review` | ya |

## 3. Review dan esai

| RPC | Izin | Prasyarat | Efek | Idempoten |
|---|---|---|---|---|
| `review_response(response, new_value, reason)` **[A]** | `can_review` | ujian `processing/review/reopened`; `new_value` ∈ A–E/kosong/ganda; alasan wajib bila beda dari terdeteksi | tulis `response_reviews`, set `final_answer`, `manually_corrected`, `locked_by_review=true`, hitung skor butir | ya (nilai sama = no-op) |
| `save_essay_score(participant, criterion, score, comment)` | `can_review` | ujian `review/processing/reopened`; `0 ≤ score ≤ max` | upsert `essay_scores` `draft` | ya |
| `complete_essay_grading(participant, question)` **[A]** | `can_review` | semua kriteria soal terisi | status `completed` | ya |

## 4. Hasil, finalisasi, koreksi

| RPC | Izin | Prasyarat | Efek | Idempoten |
|---|---|---|---|---|
| `compute_exam_results(exam)` | internal + admin/guru pemilik | — | hitung ulang `exam_results` per peserta (set-based, satu transaksi); status `provisional/complete` | ya |
| `mark_ready_to_finalize(exam)` **[A]** | admin/guru pemilik/`finalize` | **guard di bawah** | `review → ready_to_finalize` | ya |
| `finalize_exam(exam, exceptions jsonb)` **[A]** | `has_permission('finalize')` | `ready_to_finalize`; `exceptions` hanya untuk peserta `absent/withdrawn` atau pengecualian formal beralasan | tulis `result_snapshots` (event `finalize`), kunci hasil, `finalized` | **ya** (sudah final = no-op) |
| `reopen_exam(exam, reason)` **[A]** | `has_permission('reopen')` | `finalized`; alasan ≥ 10 karakter | snapshot `reopen`, `finalized → reopened → review` | ya |
| `amend_final_score(exam, participant, patch, reason)` **[A]** | `has_permission('amend_final')` | `finalized`; alasan ≥ 10 karakter | revisi baru di `result_snapshots` (event `amend`); nilai sebelum/sesudah di audit | tidak (revisi baru) |
| `export_scores(exam, filters)` | sesuai cakupan | hasil `finalized` untuk ekspor resmi | baris ekspor (CSV/XLSX disusun klien; sel diawali `'` bila diawali `= + - @` untuk cegah formula injection) | ya |

### Guard `mark_ready_to_finalize`

1. Tidak ada `exam_sheets` berstatus `uploaded`, `needs_review`, atau `failed` yang belum diselesaikan/dikecualikan.
2. Tidak ada `student_responses` dengan `review_status = 'pending'`.
3. Semua sheet punya `participant_id` (atau ditandai pengecualian).
4. Setiap peserta `active` yang punya soal esai: semua kriteria `completed`.
5. Peserta `active` tanpa sheet: harus ditandai `absent` atau dikecualikan beralasan.
6. `compute_exam_results` sudah dijalankan setelah perubahan terakhir (versi kunci/rubrik sesuai).
7. Bobot dan konfigurasi tidak berubah sejak `ready`.

## 4b. Fungsi internal (tidak dipanggil klien langsung)

| Fungsi | Dipanggil oleh | Tugas |
|---|---|---|
| `transition_exam(exam, to_status, reason)` | semua RPC yang mengubah status ujian | Satu-satunya jalan mengubah `exams.status`: memeriksa tabel transisi sah (lihat `architecture.md` §3), menjalankan guard, menulis audit. Kolom `status` dijaga trigger terhadap UPDATE langsung |
| `classify_response(fills numeric[], profile omr_profiles)` | `submit_omr_measurements`, `reclassify_exam` | Fungsi murni deterministik di §5 |
| `score_response(response, answer_key_version)` | `review_response`, `compute_exam_results` | Skor butir dari kunci versi aktif dan kebijakan kosong/ganda |
| `write_audit(action, entity, before, after, reason)` | semua RPC bertanda **[A]** | Menulis `audit_logs`; aktor dari `auth.uid()` |

## 5. Klasifikasi respons (fungsi murni `classify_response`, dites di DB)

Masukan: nilai `fill` tiap opsi pada satu soal, urut menurun `f1 ≥ f2 ≥ …`, dan ambang dari `omr_profiles`
(`min_fill`, `ambiguous_band`, `dominance_ratio`, `min_quality`). Nilai ambang = **hipotesis awal**, dikalibrasi di S1.
Aturan dievaluasi berurutan; yang pertama cocok menang:

1. Kualitas halaman `< min_quality` atau pengukuran soal tidak tersedia → `unreadable`.
2. `f1 < min_fill − ambiguous_band` → `blank`.
3. `f1 < min_fill` (tanda samar di dalam pita) → `ambiguous`.
4. `f1 ≥ min_fill`, dan `f2 ≥ min_fill` serta `f2 ≥ dominance_ratio × f1` → `multiple`.
5. `f1 ≥ min_fill`, dan `f2 ≥ min_fill − ambiguous_band` serta `f2 ≥ dominance_ratio × f1` (opsi kedua samar tetapi
   cukup kuat) → `ambiguous`.
6. Selain itu → `detected` (opsi dengan `f1`).

Skor butir: `detected` → cocok kunci ? skor kunci : 0. `blank` → 0 (kebijakan `blank_policy`). `multiple`/`ambiguous`/
`unreadable` → **tanpa skor sampai diputuskan manusia**; setelah dikonfirmasi `multiple` → `multiple_policy` (default 0).
Tes: kombinasi di atas + nilai batas tepat pada ambang (inklusif/eksklusif didokumentasikan) + monotonisitas
(menaikkan fill satu opsi tidak boleh mengubah hasil dari `detected` ke `blank`).
