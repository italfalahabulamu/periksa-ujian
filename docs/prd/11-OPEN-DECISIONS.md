# Keputusan Terbuka

Semua pertanyaan berikut perlu dijawab sebelum implementasi penuh. Catat keputusan, pemilik keputusan, dan tanggalnya.

| ID | Pertanyaan | Opsi/pertimbangan | Pemilik | Status |
|---|---|---|---|---|
| D-01 | Framework frontend HRIS yang harus diikuti? | Verifikasi repository, jangan menebak | Tim IT | Belum |
| D-02 | Repo aplikasi ujian terpisah atau monorepo? | Pisah untuk isolasi; monorepo jika pola HRIS mendukung | Tim IT | Belum |
| D-03 | Supabase project sama atau terpisah dari HRIS? | Project sama perlu batas schema/RLS ketat; terpisah memudahkan isolasi | Pimpinan + IT | Belum |
| D-04 | Apakah login/SSO HRIS akan digunakan? | Tidak otomatis; evaluasi kebutuhan dan risiko | Pimpinan + IT | Belum |
| D-05 | Format lembar jawaban? | A4, jumlah soal, opsi A–D/E, marker | Akademik + IT | Belum |
| D-06 | Sumber scan? | Scanner flatbed/ADF atau kamera ponsel | Operator | Belum |
| D-07 | Identifikasi peserta pada lembar? | Barcode/QR, kode peserta, atau ID cetak | Akademik + IT | Belum |
| D-08 | Skor jawaban ganda? | Nol, review wajib, atau aturan lain | Akademik | Belum |
| D-09 | Formula PG/esai? | Bobot, skala, pembulatan, pengecualian | Pimpinan akademik | Belum |
| D-10 | Apakah nilai final dapat diubah? | Hanya dengan izin khusus, alasan, dan audit | Pimpinan | Usulan |
| D-11 | Ekspor yang wajib? | CSV dulu; XLSX jika dibutuhkan | Akademik | Belum |
| D-12 | Target jumlah siswa/lembar per batch? | Tentukan volume pilot dan puncak | Akademik + IT | Belum |
| D-13 | Target akurasi OMR dan toleransi review? | Tetapkan setelah dataset pilot | Akademik + IT | Belum |
| D-14 | Retensi scan dan data nilai? | Kebijakan arsip sekolah | Pimpinan | Belum |
| D-15 | Siapa yang boleh melihat jawaban/scan? | Sesuai penugasan dan prinsip least privilege | Pimpinan + IT | Belum |

## Rekomendasi urutan keputusan

1. Audit HRIS (D-01 sampai D-04).
2. Sepakati template dan perangkat scan (D-05 sampai D-07).
3. Sepakati kebijakan nilai dan otorisasi (D-08 sampai D-10).
4. Tentukan volume pilot, akurasi, ekspor, dan retensi (D-11 sampai D-15).
