# periksa-ujian — Sistem Pemeriksaan Ujian SMP

Aplikasi pemeriksaan ujian SMP Pesantren Modern Al-Falah Abu Lam U: pilihan ganda dibaca dengan OMR dari
lembar jawaban hasil pindai/foto, esai dinilai guru dengan rubrik digital, nilai dihitung dan difinalisasi
dengan jejak audit.

> **Status: Fase 0 (perencanaan).** Belum ada kode aplikasi. Yang ada baru dokumen dasar dan PRD v0.1.
> Kode ditulis setelah PRD (Gerbang 1) dan arsitektur (Gerbang 2) disetujui.

## Baca dulu (urutan)

1. `docs/orchestrator/STATE.md` — posisi proyek, keputusan terkunci, apa yang ditunggu.
2. `docs/PRD.md` — indeks produk; sumber lengkapnya di `docs/prd/` (mulai dari `01-PRD.md` dan `02-SCOPE-MVP.md`).
3. `AGENTS.md` — aturan kerja dan aturan keras untuk agent dan pengembang.
4. `docs/orchestrator/adr/0001-stack-dari-hris.md` — alasan stack.
5. `docs/hris-adoption-map.md` — bagian HRIS/FTS yang diadopsi dan yang tidak.
6. `docs/prd/11-OPEN-DECISIONS.md` — keputusan yang wajib dijawab sebelum implementasi.
7. `docs/data/` — template data yang harus disiapkan (kelas, siswa).

## Lingkup singkat

Dalam lingkup: data akademik, ujian, soal PG + kunci berversi, rubrik esai, unggah scan ke storage privat,
OMR dengan antrean validasi manual, penilaian esai oleh guru, nilai akhir, finalisasi terkendali, audit, laporan CSV.

Di luar lingkup: penilaian esai oleh AI, ujian daring/proctoring, aplikasi mobile native, OMR layout bebas, SSO HRIS.

## Stack (diusulkan)

HTML + JavaScript murni (ES modules) · Supabase (Postgres, Auth, RLS, RPC, Storage privat, Edge Function) ·
Cloudflare Workers static assets · Vitest + tes database + E2E. Pemrosesan OMR: belum diputuskan (prototipe dulu).

## Rahasia

Jangan commit kunci apa pun. Salin `.env.example` ke `.env`. `service_role` key tidak boleh ada di frontend.
Jangan menempel token atau kunci di chat, issue, atau commit.
