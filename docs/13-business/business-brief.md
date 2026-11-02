# Ringkasan Bisnis (Fase 1)

## Keputusan Gerbang 1 dari user
1. Pengguna awal: **sekolah**
2. LJK: **template buatan aplikasi**
3. Harga: **gratis**

## Pelanggan dan masalah
- **Pengguna:** guru mata pelajaran. **Pembayar:** tidak ada (gratis), tetapi **penentu adopsi** adalah guru dan kepala sekolah.
- Masalah: mengoreksi pilihan ganda dan isian singkat secara manual memakan waktu, rentan salah hitung, dan hasilnya jarang dianalisis untuk memperbaiki soal.
- Cara sekarang (asumsi, belum diwawancara): koreksi manual dengan kunci, spreadsheet, atau pemindai gratis seperti EvalBee. **[BELUM TERVERIFIKASI dengan guru nyata]**

## Pesaing dan pengganti
- EvalBee (gratis di Google Play, pindai LJK dengan kamera, ekspor Excel, maksimal 240 soal; informasi bertanggal September 2023). Sumber: https://guruinovatif.id/artikel/cara-membuat-soal-ljk-dan-scan-otomatis-dengan-aplikasi-gratis-evalbee
- Pengganti: koreksi manual dan spreadsheet.
- Pesaing lain di Indonesia belum ditelusuri; tugas lanjutan sebelum Gerbang 2.

## Proposisi nilai (hipotesis)
"Untuk guru sekolah yang sudah mengoreksi LJK, aplikasi ini bukan hanya menghitung nilai tetapi juga memberi tahu soal mana yang bermasalah (kunci keliru, pengecoh tidak berfungsi, terlalu sulit atau mudah), sehingga ujian berikutnya lebih baik." Pembeda adalah modul Telaah Soal; ini **hipotesis** yang perlu diuji ke 5-10 guru sebelum dibangun penuh.

## Model bisnis dan keberlanjutan
- Pendapatan dari guru: tidak ada (keputusan Gerbang 1: gratis). **Biaya jangka panjang ditanggung sekolah** (jawaban user 2026-11-02), jadi sekolah adalah pembayar infrastruktur dan guru adalah pengguna. Ini membedakan pengguna dan pembayar (lihat bagian Pelanggan).
- Konsekuensi: sekolah perlu tahu perkiraan biayanya (Supabase Pro sekitar $25/bulan per organisasi bila Free tidak cukup; angka dari sumber pihak ketiga, **belum diverifikasi** ke halaman resmi) dan siapa yang memegang akun layanan (kepemilikan akun, cadangan, dan akses jika pengembang berhenti). Perlu batas pemakaian agar biaya tidak membengkak. Belum ada perjanjian layanan; perlu dibuat sebelum R1.
- Tujuan akhir proyek bagi pemilik (dampak, portofolio, atau layanan berbayar nanti) belum dinyatakan.
- Jalur masa depan yang tidak mengubah keputusan sekarang: paket institusi untuk dinas atau yayasan, atau fitur berkuota yang lebih tinggi.

## Go-to-market (pilot)
1. Satu atau dua sekolah mitra dengan satu guru pendamping sebagai pengguna pertama.
2. Satu ujian nyata per semester sebagai pilot, bukan peluncuran luas.
3. Kriteria lanjut: guru menyelesaikan satu siklus ujian (cetak LJK, pindai, rekap, telaah) tanpa bantuan pengembang, dan waktu koreksi turun dibanding cara lama.
4. Kriteria berhenti atau ubah arah: salah baca tak ditandai melewati ambang spike, atau guru tidak memakai modul Telaah Soal.

## KPI usulan (definisi dan target dibahas di Gerbang 2)
| KPI | Definisi | Sumber data |
|---|---|---|
| Aktivasi | Guru yang menyelesaikan satu ujian sampai rekap nilai | Log aplikasi |
| Akurasi pindai | Persen bulatan benar dan persen ditandai ragu | Hasil koreksi guru |
| Waktu koreksi | Menit per kelas dibanding cara lama | Survei guru |
| Pemakaian Telaah Soal | Persen ujian yang dibuka analisisnya | Log aplikasi |
Target angka belum ditetapkan karena belum ada dasar data.

## Tanda hukum dan kepatuhan (diserahkan ke penasihat hukum)
- Data siswa adalah data anak, termasuk data pribadi spesifik; persetujuan orang tua/wali dan keamanan data diatur UU PDP No. 27/2022 (Pasal 4, 25, 35-39, 46). Peran hukum kita (pengendali atau prosesor) dan cara persetujuan dikumpulkan lewat sekolah belum diputuskan.
- Syarat dan ketentuan serta kebijakan privasi diperlukan sebelum pilot.

## Risiko bisnis
1. Pesaing gratis sudah ada; pembeda harus nyata di mata guru.
2. Ketergantungan pada satu penyedia (Supabase) dan kebijakan toko aplikasi (uji tertutup 12 penguji x 14 hari).
3. Adopsi lambat: sekolah butuh izin kepala sekolah dan kesiapan cetak LJK.
4. Biaya tanpa pendapatan (lihat model biaya).
