## HANDOFF: architect -> pemilik proyek (usulan Gerbang 2)

### Context
Riset dan perencanaan Fase 1 selesai di tingkat dokumen pada 2026-10-17. Tidak ada kode. Seluruh isi berstatus
**diusulkan** dan menunggu Gerbang 1 (PRD) serta keputusan di `docs/decisions.md`.

### Findings
- Workers Free (10 ms CPU) dan Edge Function (2 detik CPU, 256 MB) tidak dapat memproses gambar halaman penuh.
  Usulan: **ukur di browser (Web Worker), klasifikasi di Postgres** (ADR-0002), sehingga tidak butuh server komputasi
  dan ambang dapat dikalibrasi ulang tanpa memindai ulang.
- **Storage 1 GB Supabase Free tidak cukup untuk satu periode ujian penuh dengan esai** (model: 180–720 MB per ujian
  300 siswa). Perlu kebijakan purge scan (D-14) dan/atau Pro (D-03). Proyek Free juga dijeda setelah 1 minggu idle.
- Batas 2 proyek aktif di Free mungkin sudah terpakai HRIS + FTS; jumlah proyek yang ada belum diketahui.
- OMRChecker bukan dependensi: lisensi upstream belum terverifikasi (satu salinan menyebut GPLv3), Python, klaim
  akurasi milik pengembangnya.
- Rancangan database PRD diperkuat (ADR-0003): sheet multi-halaman, snapshot hasil append-only, versi beku
  kunci/rubrik/konfigurasi, state machine di DB, `numeric` (float biner membulatkan 84,005 menjadi 84,0).
- Pihak yang belum diverifikasi: ketentuan UU PDP untuk data anak (D-17), harga/status Cloudflare Containers,
  ukuran OpenCV.js yang dibutuhkan.

### Files Modified
Baru: `docs/research/riset-2026-10-17.md`, `docs/architecture.md`, `docs/data-model.md`, `docs/permissions-rls.md`,
`docs/rpc-contracts.md`, `docs/omr-template-spec.md`, `docs/omr-spike-plan.md`, `docs/threat-model.md`,
`docs/test-strategy.md`, `docs/decisions.md`, `docs/tasks.md`,
`docs/orchestrator/adr/0002-runtime-omr.md`, `docs/orchestrator/adr/0003-model-data-versi-dan-audit.md`.
Diubah: `README.md`, `AGENTS.md`, `docs/PRD.md`, `docs/hris-adoption-map.md`, `docs/orchestrator/STATE.md`.

### Open Questions
Lihat `docs/decisions.md` §A: D-12, D-16, D-03, D-05..D-07, D-14, D-08/D-09, D-17; plus D-20.

### Recommendations
1. Jawab keputusan §A, lalu setujui G1.
2. Jalankan audit FTS/HRIS (A-01) dan tutup G2.
3. Jadwalkan spike S1 segera setelah D-05..D-07 dan perangkat (D-20) siap; ia memotong risiko terbesar proyek.
4. Pindahkan penyiapan akses GitHub ke konektor resmi dan **cabut token yang pernah ditempel di chat**.
