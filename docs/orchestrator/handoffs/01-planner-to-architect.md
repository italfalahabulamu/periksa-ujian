## HANDOFF: planner -> architect

### Context
Fase 0 selesai di tingkat dokumen: paket PRD v0.1 (13 berkas), peta adopsi HRIS/FTS, template data, STATE, dan
ADR-0001 sudah ada. Belum ada kode. Struktur awal repo mengikuti commit fondasi FTS.

### Findings
- Lingkup MVP: pemeriksaan PG lewat OMR dengan antrean validasi, esai dinilai guru tanpa AI, nilai akhir
  berformula berversi, finalisasi dan reopen terkendali, audit, laporan CSV.
- Stack diusulkan dari FTS (JS statis + Supabase + Cloudflare); belum diverifikasi lewat audit HRIS langsung.
- OMR adalah risiko terbesar: runtime, library, format lembar, dan sumber scan belum diputuskan.
- Jebakan keamanan yang harus dihindari: role dari metadata signup; fungsi `security definer` tanpa
  `set search_path`; scan di bucket publik; skor final yang dapat ditimpa tanpa histori.
- Poin kritis desain: state machine ujian di database, versi kunci/rubrik/formula, idempotensi pemrosesan scan,
  reprocessing yang tidak menimpa koreksi manual, RLS berbasis penugasan guru/kelas/ujian termasuk storage.

### Files Modified
`AGENTS.md`, `CLAUDE.md`, `README.md`, `.gitignore`, `.env.example`, `docs/PRD.md`, `docs/prd/*`,
`docs/hris-adoption-map.md`, `docs/data/*`, `docs/orchestrator/STATE.md`,
`docs/orchestrator/adr/0001-stack-dari-hris.md`

### Open Questions
D-01, D-03 sampai D-15 (lihat `docs/prd/11-OPEN-DECISIONS.md`).

### Recommendations
Di G2: tetapkan ERD final dari `docs/prd/06-DATABASE-SCHEMA.md`, definisi transisi status ujian, matriks izin per
tabel dan bucket, kontrak RPC (usulan: `mark_exam_ready`, `freeze_answer_key`, `record_omr_result`,
`correct_response`, `finalize_exam`, `reopen_exam`), strategi tes database + E2E, dan rencana prototipe OMR
berbatas waktu dengan dataset pilot (ADR-0002). Putuskan D-05 sampai D-07 sebelum prototipe dimulai.
