# periksa-ujian

Aplikasi mobile untuk sekolah dengan dua fungsi: **Koreksi Jawaban** (foto LJK pilihan ganda dan isian singkat) dan
**Telaah Soal** (pemeriksaan kunci dan analisis butir). Gratis untuk sekolah. Dibangun dengan Fd.co Team (mode A, dari nol).

> Status: lihat `docs/PROJECT_STATE.md`. Riwayat perencanaan sebelumnya diarsipkan di tag `archive/pre-reset`
> (`git show archive/pre-reset:README.md`). Dokumen lama tidak lagi berlaku.

## Isi repo
- `docs/PROJECT_STATE.md`: posisi proyek, keputusan, asumsi, langkah berikutnya.
- `docs/11-rnd/`: temuan riset dan spike. `docs/12-finance/`: model biaya. `docs/13-business/`: ringkasan bisnis.
- `docs/01-product/`: PRD (Fase 2).
- `spikes/`: kode prototipe sekali pakai (bukan fondasi produksi).

## Rahasia
Jangan commit kunci apa pun. Salin `.env.example` ke `.env`. `service_role` tidak boleh ada di aplikasi klien.
Jangan menempel token di chat, issue, atau commit.
