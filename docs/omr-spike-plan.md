# Rencana spike S1: bukti kelayakan OMR

Tujuan: memutuskan ADR-0002 (JS murni vs OpenCV.js vs worker Python) dengan **data**, dan mengkalibrasi
`omr_profiles` awal. Batas waktu usulan: **5 hari kerja**, setelah D-05 sampai D-07 terjawab dan sampel kertas/scan
tersedia. Spike menghasilkan kode prototipe di cabang terpisah dan laporan; kode spike bukan kode produksi.

## 1. Prasyarat

- D-05 (format), D-06 (sumber scan), D-07 (identifikasi peserta) terjawab.
- Cetakan template uji (§ `omr-template-spec.md`) dan akses ke scanner sekolah yang akan dipakai.
- Relawan mengisi lembar (guru/siswa dengan persetujuan, **tanpa data pribadi nyata**: kode peserta fiktif).
- Perangkat acuan: 1 laptop operator tipikal sekolah + 1 tablet bila dipakai (D-20).

## 2. Dataset

| Kelompok | Jumlah minimum | Isi |
|---|---:|---|
| Scanner, isian wajar | **60 lembar** (≈ 3.000 respons bila 50 soal) | variasi pensil 2B/HB, pulpen, isian tipis/tebal |
| Scanner, kasus sulit | 30 lembar | hapusan tidak bersih, ganda, coretan, kosong, arsir kasar, tanda silang, lipatan/noda ringan |
| Scanner, kondisi teknis | 20 lembar | miring ≤ 5°, resolusi 100/150/200/300 dpi, kontras berbeda |
| Foto ponsel (opsional, terpisah) | 60 lembar | cahaya tak merata, perspektif, blur ringan |
| Sintetis | 300+ | dibangkitkan program dari `layout` (derau, rotasi, skala, isian acak dengan kebenaran diketahui) |

**Kebenaran dasar (ground truth):** dua orang membaca setiap lembar nyata secara independen; selisih diputuskan
orang ketiga. Dataset nyata disimpan di luar git (`tests/fixtures/real/` sudah di `.gitignore`); hanya sintetis yang
boleh masuk repo.

Alasan 60 lembar: tanpa satu pun kesalahan "yakin tetapi salah" pada n respons, batas atas 95% tingkat kesalahan
≈ 3/n (aturan tiga). Dengan n ≈ 3.000, batas atas ≈ 0,1%. Jumlah lebih kecil tidak dapat membuktikan target seketat itu.

## 3. Langkah

| # | Langkah | Keluaran |
|---|---|---|
| S1-1 | Generator template + lembar sintetis (JS, dipakai juga sebagai fixture tes) | `tools/synth/` |
| S1-2 | Deteksi penanda sudut + homografi (JS murni) | modul + tes pada sintetis |
| S1-3 | Pengukuran `fill_ratio` + metrik kualitas | modul + tes |
| S1-4 | Dekode PDF (pdf.js) dan gambar dalam Web Worker; batas memori | uji pada halaman 150/300 dpi |
| S1-5 | Jalankan pada dataset nyata; simpan pengukuran mentah | tabel hasil |
| S1-6 | Kalibrasi ambang (`min_fill`, `dominance_ratio`, `ambiguous_band`, `min_quality`) pada **separuh** data (pelatihan), uji pada separuh lainnya | profil kandidat + kurva |
| S1-7 | Bila gate gagal: ulangi dengan OpenCV.js (build kustom; catat ukuran `.wasm` dan lisensi); bila gagal lagi: rancang worker Python | catatan perbandingan |
| S1-8 | Uji lintas-browser dan lintas-perangkat; ukur waktu P50/P95 per lembar dan memori puncak | laporan kinerja |
| S1-9 | Laporan + draf ADR-0002 final + usulan `omr_profiles` v1 | `docs/omr-spike-report.md` |

## 4. Metrik (definisi tetap sebelum mengukur)

- **Akurasi per respons** = respons dengan status otomatis `detected` yang nilainya sama dengan kebenaran dasar ÷ semua `detected`.
- **False acceptance (FA)** = `detected` dengan nilai ≠ kebenaran dasar ÷ semua respons yang kebenaran dasarnya bukan ambigu. *Metrik paling penting*: kesalahan yang lolos tanpa review.
- **Tingkat review** = respons ber-status `ambiguous/multiple/unreadable` ÷ semua respons (beban kerja manusia).
- **False rejection** = respons jelas yang malah masuk review ÷ semua respons jelas (biaya, bukan bahaya).
- **Kegagalan lembar** = lembar `failed` ÷ semua lembar.
- **Salah kait peserta** = lembar yang kode pesertanya salah dibaca namun lolos cek-digit ÷ semua lembar.
- **Waktu per lembar** P50/P95 pada perangkat acuan, termasuk dekode.

## 5. Gate (hipotesis awal untuk dibahas; keputusan akhir di D-13)

| Metrik | Jalur scanner | Jalur foto ponsel (bila diuji) |
|---|---|---|
| FA | ≤ 0,1% (batas atas 95%, n ≥ 3.000) | ≤ 0,3% |
| Tingkat review | ≤ 10% | ≤ 20% |
| Kegagalan lembar | ≤ 2% | ≤ 8% |
| Salah kait peserta | 0 dari 60 | 0 dari 60 |
| Waktu per lembar P95 | ≤ 5 detik pada laptop acuan | ≤ 8 detik |

Angka-angka ini **usulan awal**, bukan standar. Pemilik proyek dan tim akademik menetapkan toleransi risiko
(PRD OMR §7). Jika scanner lulus tetapi foto ponsel gagal, MVP dirilis dengan scanner saja.

## 6. Keluaran keputusan

1. Pilih tahap implementasi P1/P2/P3 (ADR-0002) berdasar gate.
2. Tetapkan `omr_profiles` v1 + dokumen kalibrasi (dataset, tanggal, perangkat).
3. Perbarui `omr-template-spec.md` dengan geometri yang terbukti.
4. Daftar risiko sisa dan syarat pilot terbatas (satu ujian, jumlah peserta yang ditetapkan di D-12).
