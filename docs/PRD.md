# PRD — Sistem Pemeriksaan Ujian SMP (indeks)

- **Versi:** 0.1 — draft baseline, **belum disetujui (Gerbang 1 menunggu)**
- **Pemilik produk:** Pesantren Modern Al-Falah Abu Lam U
- **Sumber:** paket dokumen `prd-sistem-pemeriksaan-ujian-smp` (13 berkas), disalin apa adanya ke `docs/prd/`

Berkas di `docs/prd/` adalah sumber kebenaran isi produk. Dokumen ini hanya indeks dan ringkasan agar
mudah dibaca bersama `STATE.md`. Bila ada perbedaan, `docs/prd/` yang berlaku sampai PRD diubah lewat gerbang.

## Ringkasan

Pilihan ganda diperiksa dengan OMR dari scan/foto berbasis template standar; hasil yang kosong, ganda,
ambigu, atau gagal masuk antrean validasi manusia. Esai dinilai guru per kriteria rubrik, **tanpa AI**.
Nilai akhir = (nilai PG × bobot PG) + (nilai esai × bobot esai), bobot disimpan per ujian dan berjumlah 1.
Kunci, rubrik, dan formula dibekukan sebagai versi; finalisasi dan perubahan sesudahnya diaudit.

## Peta dokumen

| Berkas | Isi |
|---|---|
| `docs/prd/01-PRD.md` | Requirements produk (FR-01..FR-13), aturan bisnis, formula nilai, metrik, kriteria rilis, risiko |
| `docs/prd/02-SCOPE-MVP.md` | Prioritas P0/P1/P2, di luar cakupan, asumsi, Definition of Done |
| `docs/prd/03-SITEMAP-USER-FLOW.md` | Sitemap, alur utama, state machine ujian |
| `docs/prd/04-UI-WIREFRAME.md` | Wireframe teks dashboard, antrean OMR, validasi OMR, esai, finalisasi |
| `docs/prd/05-ARSITEKTUR-TEKNIS.md` | Arsitektur konseptual, batas data HRIS, checklist audit repo |
| `docs/prd/06-DATABASE-SCHEMA.md` | 22 entitas inti, kolom penting, relasi, kebijakan RLS |
| `docs/prd/07-OMR-SPEC.md` | Alur pemrosesan, status respons, aturan keselamatan, dataset pilot, template |
| `docs/prd/08-ROLE-PERMISSION.md` | Matriks peran dan prinsip otorisasi |
| `docs/prd/09-TEST-PLAN.md` | Strategi tes, acceptance criteria AC-01..AC-07, gate sebelum pilot |
| `docs/prd/10-ROADMAP.md` | Tahap 0–5 dan risiko jadwal |
| `docs/prd/11-OPEN-DECISIONS.md` | Keputusan terbuka D-01..D-15 |
| `docs/prd/12-IMPLEMENTATION-BACKLOG.md` | Backlog Epic A–G siap dijadikan GitHub Issues |

## Yang harus diputuskan sebelum Gerbang 1 ditutup

Lihat `docs/prd/11-OPEN-DECISIONS.md`. Yang paling menentukan arsitektur: D-02 (repo terpisah atau monorepo;
repo ini sudah terpisah), D-03 (Supabase project sama atau terpisah dari HRIS), D-05 sampai D-07 (format
lembar, sumber scan, identifikasi peserta), D-08 dan D-09 (kebijakan jawaban ganda dan formula nilai).
