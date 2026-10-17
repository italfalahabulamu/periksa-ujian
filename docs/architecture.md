# Arsitektur (usulan untuk Gerbang 2)

Status: **diusulkan**. Mengikuti `docs/prd/05-ARSITEKTUR-TEKNIS.md`, ADR-0001 (stack), ADR-0002 (OMR), ADR-0003 (data).
Tidak ada kode yang ditulis sebelum Gerbang 1 dan 2 disetujui.

## 1. Komponen

```mermaid
flowchart LR
  subgraph Browser["Browser pengguna (desktop/tablet)"]
    UI["UI modul ES (tanpa framework)"]
    W["Web Worker OMR\n(ukur gelembung)"]
    PDF["pdf.js (render PDF)"]
  end
  subgraph CF["Cloudflare Workers (static assets)"]
    ST["public/ + _headers (CSP ketat)"]
  end
  subgraph SB["Supabase"]
    AUTH["Auth"]
    PG[("Postgres\nRLS + RPC + trigger")]
    STO[("Storage privat\nbucket scans")]
    EF["Edge Function\n(admin: buat akun, reset sandi)"]
  end
  UI --> ST
  UI -->|"RPC / query (JWT)"| PG
  UI -->|"signed URL"| STO
  UI --> W
  PDF --> W
  W -->|"submit_omr_measurements"| PG
  UI --> AUTH
  EF --> AUTH
  EF --> PG
```

- **Database adalah backend.** Semua keputusan bisnis ada di Postgres (RPC `security definer`,
  `set search_path = public, pg_temp`, constraint, trigger, RLS). Klien hanya menampilkan dan mengukur.
- **Cloudflare** hanya menyajikan aset statis. Tidak ada komputasi gambar di Workers/Edge Function (riset R1, R2).
- **Edge Function** hanya untuk tindakan admin yang butuh `service_role` (membuat akun staf, reset sandi), seperti FTS.
- **Service worker** hanya meng-cache aset statis; tidak pernah scan atau data (aturan #19).

## 2. Alur data: unggah → ukur → klasifikasi → review

```mermaid
sequenceDiagram
  actor Op as Operator scan
  participant UI as Browser (UI)
  participant W as Web Worker OMR
  participant ST as Storage privat
  participant DB as Postgres (RPC)
  Op->>UI: pilih ujian + berkas (PDF/JPG/PNG)
  UI->>UI: validasi tipe, ukuran, hitung SHA-256
  UI->>DB: register_sheet_pages(exam, batch, hash, page_no)
  DB-->>UI: sheet_id (idempoten: hash sama → sheet yang sama)
  UI->>ST: upload ke scans/{exam}/{sheet}/{page}
  UI->>W: halaman (ImageData)
  W->>W: cari penanda, homografi, ukur fill_ratio per gelembung
  W-->>UI: measurements + quality
  UI->>DB: submit_omr_measurements(sheet, template_v, algo_v, measurements)
  DB->>DB: klasifikasi deterministik (omr_profiles) → student_responses
  DB-->>UI: ringkasan: ready / needs_review / failed + alasan
  Note over DB: respons ambigu/ganda/kosong/tak terbaca → antrean review
```

Reprocessing: perubahan ambang → `reclassify_exam(exam_id)` di DB, **tanpa memuat ulang gambar**; baris
`locked_by_review = true` tidak disentuh. Kegagalan teknis (`failed`) tercatat dengan kode alasan dan dapat
diulang dari UI (`request_reprocess`).

## 3. State machine ujian

```mermaid
stateDiagram-v2
  [*] --> draft
  draft --> ready: mark_exam_ready (kelengkapan)
  ready --> processing: sheet pertama terdaftar
  processing --> review: close_intake
  review --> ready_to_finalize: mark_ready_to_finalize (tidak ada pekerjaan wajib)
  ready_to_finalize --> review: ada masalah baru / kunci diubah
  ready_to_finalize --> finalized: finalize_exam (izin finalize)
  finalized --> reopened: reopen_exam (izin reopen + alasan)
  reopened --> review
  draft --> cancelled
  ready --> cancelled
  processing --> cancelled
  review --> cancelled
```

*Guard* per transisi didefinisikan di `docs/rpc-contracts.md`. Satu fungsi pusat `transition_exam` menegakkan
tabel transisi; kolom `status` tidak dapat diubah langsung oleh klien.

## 4. State machine lembar

```mermaid
stateDiagram-v2
  [*] --> uploaded
  uploaded --> measured: submit_omr_measurements
  uploaded --> failed: gagal (penanda/kualitas/berkas)
  measured --> ready: semua respons detected/blank (sesuai kebijakan)
  measured --> needs_review: ada ambiguous/multiple/unreadable atau ID tak cocok
  needs_review --> ready: semua respons wajib terselesaikan
  failed --> uploaded: request_reprocess / unggah ulang
  ready --> superseded: pengukuran baru menggantikan
  needs_review --> superseded: idem
```

## 5. Anggaran kapasitas dan kinerja (model; diukur di spike S1)

| Sumber daya | Batas (Free) | Perkiraan per ujian 300 siswa | Catatan |
|---|---|---|---|
| Storage scan | 1 GB | 120 MB (PG saja, 0,4 MB/hal.) – 360 MB (PG+esai 3 hal.) | Perlu purge/Pro; lihat riset §2 |
| Database | 500 MB | ≈ 2 MB respons + audit | Tidak jadi kendala |
| Egress | 5 GB | ≈ 720 MB (2 kali lihat) | Cache + signed URL dipakai ulang |
| Memori dekode browser | — | 35–48 MB/halaman | Proses 1 halaman per Worker, tidak paralel tanpa batas |
| Waktu per lembar | — | **belum diukur** | Target ditetapkan setelah S1; jangan janjikan angka |

Aturan kinerja UI: semua daftar dipaginasi dan difilter di server; antrean review memuat gambar halaman
berikutnya secara *prefetch* (satu di depan) agar berpindah cepat tanpa memboroskan egress.

## 6. Lingkungan dan penyebaran

| Lingkungan | Isi | Catatan |
|---|---|---|
| Lokal | Postgres 16 sungguhan untuk tes DB/RLS, build statis | Sama seperti FTS (`scripts/test-db.sh`) |
| Staging | Proyek Supabase + deployment Cloudflare terpisah | Migrasi diuji dulu di sini; akun uji ber-sandi di-generate |
| Produksi | Proyek Supabase produksi | Rollback: migrasi maju-saja + cadangan data (`backup.js` pola FTS) sebelum rilis |

Pencegahan jeda proyek Supabase Free: workflow `keepalive.yml` (pola FTS). Keputusan paket (Free/Pro) di D-03/D-14.

## 7. Batas dengan HRIS dan FTS

- Tidak ada tabel, kunci, atau fungsi HRIS/FTS yang diakses aplikasi ini.
- Rekomendasi D-03: **proyek Supabase terpisah** (data anak, scan, blast radius RLS). Biaya: kemungkinan Pro karena
  batas 2 proyek aktif di Free (R3); jumlah proyek yang sudah ada belum diketahui.
- SSO tidak dibuat di MVP (D-04). Akun staf dibuat admin; reset sandi oleh admin bila email tidak tersedia.
