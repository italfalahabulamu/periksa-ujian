# Izin, RLS, dan akses storage (usulan untuk Gerbang 2)

Dasar: `docs/prd/08-ROLE-PERMISSION.md`. Prinsip: **default deny**; role bukan satu-satunya pembatas, cek juga
penugasan (guru→kelas/mapel, `exam_staff`→ujian). Pimpinan tidak otomatis boleh mengubah nilai.

## 1. Fungsi bantu (semua `security definer`, `set search_path = public, pg_temp`, `stable`)

| Fungsi | Arti |
|---|---|
| `app_role()` | role pengguna aktif dari `profiles` (bukan dari JWT/metadata klien); NULL bila `is_active=false` |
| `has_permission(p text, exam uuid default null)` | ada baris `user_permissions` aktif untuk `p` pada ujian itu atau global |
| `is_exam_staff(exam uuid, duty text)` | ada `exam_staff` dengan duty tsb |
| `teaches_exam(exam uuid)` | guru punya `teaching_assignments` yang cocok (mapel + salah satu kelas peserta + tahun ajaran) |
| `can_view_exam(exam)` | admin, atau `teaches_exam`, atau staf ujian apa pun, atau pimpinan (hanya data hasil) |
| `can_edit_config(exam)` | (admin atau guru pemilik/pengampu) **dan** `status in (draft)`; pengecualian kunci: lihat RPC |
| `can_upload(exam)` | admin, guru pemilik, staf duty `scanner`/`grader`; ujian status `ready`/`processing` |
| `can_review(exam)` | admin, guru pemilik, staf duty `grader` |
| `can_view_scan(exam)` | admin, guru pemilik/pengampu, staf `grader`/`scanner`(hanya untuk batch sendiri); **bukan pimpinan** (D-15) |

## 2. Matriks tabel (SELECT via RLS; tulis hampir semuanya via RPC)

`R` = policy SELECT, `RPC` = hanya lewat fungsi, `—` = tidak ada akses. Tabel tanpa policy INSERT/UPDATE/DELETE
berarti klien tidak dapat menulis langsung.

| Tabel | admin | guru | pemeriksa | pimpinan | operator |
|---|---|---|---|---|---|
| `profiles` | R semua | R diri sendiri | R diri | R diri | R diri |
| `academic_years/classes/students/class_enrollments/subjects` | CRUD (policy + trigger) | R sesuai penugasan | R sesuai ujian ditugaskan | R | — |
| `teaching_assignments`, `exam_staff`, `user_permissions` | RPC | R diri | R diri | — | R diri |
| `exams`, `exam_participants`, `questions` | R + RPC | R (ujian terkait) + RPC | R (ujian ditugaskan) | R (ringkasan) | R status ujian ditugaskan |
| `answer_key_versions`, `answer_keys` | R + RPC | R + RPC | **—** | — | — |
| `rubric_versions`, `rubric_criteria` | R + RPC | R + RPC | R (ujian ditugaskan) | — | — |
| `sheet_templates`, `omr_profiles` | R + RPC | R | R | — | R (template saja) |
| `scan_batches`, `exam_sheets`, `sheet_pages` | R + RPC | R (ujian terkait) + RPC | R (ditugaskan) | — | R **status/kode gagal** batch sendiri |
| `sheet_measurements` | R | R | — | — | — |
| `student_responses`, `response_reviews` | R + RPC | R + RPC | R + RPC (ditugaskan) | — | — |
| `essay_scores` | R + RPC | R + RPC | R + RPC (ditugaskan) | — | — |
| `exam_results` | R | R (ujian terkait) | R progres saja (tanpa nilai akhir)* | R sesuai cakupan | — |
| `result_snapshots` | R | R (ujian terkait) | — | R jika `view_audit_all` | — |
| `audit_logs` | R terbatas | R aksi sendiri/ujiannya | R aksi sendiri | R jika `view_audit_all` | — |

\* Pemeriksa melihat jumlah selesai/belum, bukan nilai. Bila sekolah memutuskan lain, ubah policy (keputusan D-15).

## 3. Storage

- Bucket `scans`: **privat**, batas ukuran dan MIME (pdf/jpeg/png) di level bucket + validasi di RPC.
- Path wajib `{exam_id}/{sheet_id}/{page_no}.{ext}`.
- INSERT objek: hanya bila `can_upload(exam_id)` **dan** ada baris `sheet_pages` terdaftar dengan path itu (mencegah
  unggah liar). Tidak ada policy UPDATE/DELETE untuk klien; purge dilakukan job terjadwal dengan `service_role`.
- SELECT objek: `can_view_scan(exam_id)`. Tampilan lewat **signed URL berumur pendek (≤ 5 menit)**, dibuat saat halaman
  dibuka; antrean review melakukan prefetch satu halaman ke depan.
- Nama berkas tidak memuat nama siswa. Tidak ada URL publik, tidak ada hotlink.
- Verifikasi sintaks fungsi/kebijakan Storage terhadap dokumentasi Supabase terbaru saat implementasi.

## 4. Tes "harus ditolak" (wajib, dijalankan ke Postgres sungguhan sebagai peran berbeda)

| # | Skenario | Hasil yang diharapkan |
|---|---|---|
| T-01 | Anonim `select` dari tabel apa pun | 0 baris / ditolak |
| T-02 | Guru A membaca ujian guru B (tidak mengampu) lewat API langsung | 0 baris |
| T-03 | Guru mengubah `exams.status`, `profiles.role`, `grading_config` setelah `ready` | ditolak (trigger/RLS) |
| T-04 | Pemeriksa membaca `answer_keys` | 0 baris |
| T-05 | Operator membaca `student_responses`, `essay_scores`, `exam_results` | 0 baris |
| T-06 | Pimpinan memanggil `finalize_exam`/`review_response`/`save_essay_score` | ditolak |
| T-07 | Pimpinan membuat signed URL scan | ditolak |
| T-08 | Pengguna A membuat signed URL objek ujian B | ditolak |
| T-09 | Unggah objek tanpa `sheet_pages` terdaftar / ke path ujian lain | ditolak |
| T-10 | `insert/update/delete` langsung pada `audit_logs`, `result_snapshots`, `response_reviews`, `sheet_measurements` | ditolak |
| T-11 | Klien mengirim `reviewed_by`/`graded_by`/`created_by` palsu | diabaikan; diisi `auth.uid()` |
| T-12 | Ubah `answer_keys` pada versi `frozen` | ditolak |
| T-13 | `finalize_exam` tanpa izin `finalize` | ditolak |
| T-14 | `reopen_exam` tanpa izin atau tanpa alasan | ditolak |
| T-15 | `submit_omr_measurements` ke sheet ujian lain / template tidak cocok | ditolak |
| T-16 | Pengguna `is_active=false` memanggil RPC apa pun | ditolak |
| T-17 | Meniru role lewat `raw_user_meta_data` saat sign-up | role tetap terendah, tanpa akses |
| T-18 | Guru mengambil sheet siswa di luar ujiannya lewat tebakan UUID | 0 baris |
| T-19 | Pemeriksa A menilai esai pada ujian yang tidak ditugaskan | ditolak |
| T-20 | Operator mengunggah ke ujian berstatus `draft`/`finalized` | ditolak |

Tes dibuat table-driven dari matriks §2 supaya penambahan tabel/role memaksa penambahan kasus.
