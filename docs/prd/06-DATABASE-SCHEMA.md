# Rancangan Database

Rancangan ini bersifat konseptual. Nama kolom, tipe data, strategi multi-tenant, dan relasi pengguna harus diselaraskan dengan schema dan konvensi Supabase HRIS setelah audit.

## 1. Prinsip

- Gunakan UUID sebagai primary key jika itu sejalan dengan pola HRIS.
- Tambahkan `created_at`, `updated_at`, dan `created_by` untuk entitas yang relevan.
- Gunakan foreign key dan unique constraint.
- Gunakan soft delete hanya jika ada kebutuhan bisnis; jangan mengandalkannya sebagai kontrol keamanan.
- Simpan snapshot versi kunci, rubrik, dan formula yang dipakai ketika pemeriksaan dimulai/finalisasi.
- Jangan menyimpan scan siswa di bucket publik.
- Jangan menyimpan skor final hanya sebagai angka yang bisa diubah tanpa histori.

## 2. Entitas inti

| Tabel | Fungsi |
|---|---|
| `academic_years` | Tahun ajaran dan semester |
| `classes` | Rombel/kelas |
| `students` | Data siswa minimum yang dibutuhkan |
| `class_enrollments` | Keanggotaan siswa di kelas per tahun ajaran |
| `subjects` | Mata pelajaran |
| `teaching_assignments` | Penugasan guru ke kelas/mapel |
| `exams` | Konfigurasi ujian |
| `exam_participants` | Peserta ujian yang dibekukan untuk ujian tersebut |
| `questions` | Soal dan jenis soal |
| `question_options` | Opsi untuk soal pilihan ganda |
| `answer_key_versions` | Versi kunci jawaban |
| `answer_keys` | Kunci per nomor pada versi tertentu |
| `rubric_versions` | Versi rubrik esai |
| `rubric_criteria` | Kriteria dan skor maksimum |
| `exam_sheet_templates` | Definisi template lembar jawaban |
| `scan_batches` | Batch upload scan |
| `exam_sheets` | Berkas/lembar untuk seorang peserta |
| `student_responses` | Respons siswa per soal |
| `response_reviews` | Riwayat validasi/koreksi respons |
| `essay_scores` | Skor esai per peserta/soal/kriteria |
| `exam_results` | Ringkasan hasil komponen dan nilai akhir |
| `audit_logs` | Jejak tindakan penting |

## 3. Kolom penting (konseptual)

### `exams`
- `id`
- `name`
- `academic_year_id`
- `class_id` atau relasi ke peserta/kelas yang lebih fleksibel
- `subject_id`
- `exam_date`
- `status` — draft, ready, processing, review, ready_to_finalize, finalized, reopened, cancelled
- `pg_weight` dan `essay_weight` (misalnya numeric, total 1 jika kedua komponen dipakai)
- `grading_config` jika memang diperlukan, dengan validasi ketat
- `created_by`, timestamps

### `exam_participants`
- `id`, `exam_id`, `student_id`
- `participant_code` yang digunakan untuk mencocokkan lembar
- `status` — active, absent, withdrawn, replacement
- unique constraint yang sesuai untuk mencegah peserta ganda

### `questions`
- `id`, `exam_id`, `question_number`
- `question_type` — `multiple_choice` atau `essay`
- `prompt` atau referensi aset soal
- `max_score`
- `is_active`
- unique `(exam_id, question_number)` kecuali desain versi mengharuskan model lain

### `answer_key_versions` / `answer_keys`
- Versi kunci memiliki nomor versi, status, pembuat, dan waktu.
- Kunci per soal menyimpan jawaban benar dan/atau skor.
- Kunci yang telah dipakai pemeriksaan tidak diedit diam-diam; buat versi baru dan catat dampaknya.

### `rubric_versions` / `rubric_criteria`
- Rubrik memiliki versi dan status.
- Kriteria memiliki urutan, deskripsi, skor maksimum, dan bobot bila diperlukan.
- Simpan snapshot versi rubrik yang digunakan pada proses pemeriksaan.

### `exam_sheets`
- `id`, `exam_id`, `participant_id`, `scan_batch_id`
- `storage_path` (bukan public URL permanen)
- `template_version_id`
- `processing_status`
- `page_count`, `file_hash`, `uploaded_by`, timestamps
- unique/idempotency strategy agar upload ulang tidak menggandakan lembar tanpa sengaja

### `student_responses`
- `id`, `exam_sheet_id`, `question_id`
- `detected_answer`
- `final_answer`
- `response_status` — detected, blank, multiple, ambiguous, unreadable, manually_corrected
- `confidence` (nullable, jika algoritma mendukung pengukuran yang bermakna)
- `score`, `review_status`
- unique `(exam_sheet_id, question_id)`

### `response_reviews`
- `id`, `student_response_id`
- `previous_value`, `new_value`, `reason`
- `reviewed_by`, `reviewed_at`
- setiap koreksi menjadi event baru, bukan menimpa sejarah

### `essay_scores`
- `id`, `exam_id`, `participant_id`, `question_id`, `rubric_criterion_id`
- `score`, `comment`, `graded_by`, `graded_at`, `status`
- constraint skor tidak boleh kurang dari 0 atau melebihi skor maksimum kriteria

### `exam_results`
- `exam_id`, `participant_id`
- `pg_raw_score`, `pg_normalized_score`
- `essay_raw_score`, `essay_normalized_score`
- `final_score`
- `status`, `finalized_by`, `finalized_at`
- snapshot bobot, formula, dan versi kunci/rubrik yang dipakai

### `audit_logs`
- `id`, `actor_user_id`, `action`, `entity_type`, `entity_id`
- `before_data`, `after_data` (JSONB bila sesuai)
- `reason`, `created_at`, `request_id` bila tersedia
- batasi akses baca dan hindari menyimpan data pribadi berlebihan

## 4. Relasi ringkas

```text
academic_years ──< classes
students ──< class_enrollments >── classes
subjects ──< teaching_assignments
exams ──< exam_participants >── students
exams ──< questions ──< question_options
exams ──< answer_key_versions ──< answer_keys
exams ──< rubric_versions ──< rubric_criteria
exams ──< scan_batches ──< exam_sheets
exam_sheets ──< student_responses ──< response_reviews
exam_participants ──< essay_scores
exam_participants ──< exam_results
```

## 5. Kebijakan RLS yang harus dirancang

- Admin akademik dapat mengelola data akademik sesuai cakupan sekolah.
- Guru hanya dapat mengakses ujian/kelas yang ditugaskan kepadanya, kecuali ada izin tambahan.
- Pemeriksa hanya dapat memeriksa batch/ujian yang ditugaskan.
- Pimpinan dapat melihat laporan sesuai cakupan, tanpa hak mengubah nilai secara default.
- Perubahan nilai final memerlukan izin khusus dan alasan.
- Storage scan harus menggunakan kebijakan akses yang setara dengan izin data ujian.
- Jangan menganggap role yang dikirim dari browser dapat dipercaya tanpa verifikasi server/database.

## 6. Migration dan validasi

Semua perubahan schema harus:
- dibuat sebagai migration yang dapat dijalankan ulang sesuai toolchain;
- diuji di staging;
- menyertakan constraint/index yang diperlukan;
- disertai pengujian RLS;
- tidak mengubah atau menghapus data HRIS.
