# Rencana pilot 1 pekan (R0)

Dibuat 2026-11-02 dari jawaban user: ujian pertama **dalam 1 pekan** (sekitar 9 November 2026, tanggal pasti belum disebut), sekolah mitra
**"Sekolah asrama A"** (nama resmi belum disebut), isian singkat diketik guru, biaya jangka panjang ditanggung sekolah.
Status: **usulan PM, menunggu persetujuan user di Gerbang 2**.

## Penilaian jujur
Satu pekan untuk aplikasi mobile + backend + pembacaan foto adalah **sangat ketat**, dan bagian paling berisiko (akurasi pada foto nyata) belum terbukti:
spike 01 hanya sintetis. Karena itu pilot ini dirancang sebagai **pilot dampingan**, bukan peluncuran: aplikasi dipakai berdampingan dengan koreksi manual
yang tetap dipegang guru. Saya tidak menjanjikan semua fitur R1 selesai; yang dijanjikan adalah urutan kerja yang menjaga agar ada hasil yang bisa dipakai di hari ujian.

## Cakupan R0 (dipotong dari R1)
| Masuk | Ditunda |
|---|---|
| Masuk guru (F-AKUN-01) | Isian singkat (F-ISI-*) dan Telaah Soal (R2) |
| Siswa hanya **kode peserta** + kelas (F-DATA-01, F-DATA-02) | Ekspor XLSX (CSV saja) |
| Ujian pilihan ganda + kunci + kebijakan nilai tetap (F-UJI-01, 03) | Koreksi nilai setelah final (F-NIL-03) dan pembekuan versi kunci (F-UJI-05): cukup catatan sederhana |
| LJK PDF dari template (F-UJI-04) | Antrean offline, saran AI, iOS |
| Foto, baca, tolak foto buruk (F-LJK-01, 02, 04) | |
| Antrean cek ulang satu ketukan (F-LJK-03), **juga berfungsi sebagai input manual** | |
| Kenali peserta dari kode (F-LJK-05) | |
| Skor + rekap + ekspor CSV (F-NIL-01, 02) | |

## Keputusan yang saya sarankan (butuh persetujuan Anda)
1. **Distribusi: web app responsif yang bisa dipasang (PWA) untuk pilot, bukan aplikasi Android yang dibangun dan ditandatangani.** Alasan: Google Play menuntut
   uji tertutup 12 penguji x 14 hari berturut-turut untuk akun pribadi baru (sumber di `findings.md`), jadi toko tidak mungkin dalam 1 pekan; APK langsung butuh
   membangun, menandatangani, dan memasang di tiap ponsel. PWA dibuka lewat Chrome, kamera tersedia, pembaruan instan. Ini menyimpang dari kata "mobile"
   di Gerbang 1 dan **perlu persetujuan Anda**. Aplikasi native tetap jalur R3.
2. **Data siswa untuk pilot: hanya kode peserta, tanpa nama.** Nama tetap di daftar milik sekolah. Telaah hukum data anak (UU PDP) tidak mungkin selesai dalam 1 pekan,
   jadi pilot meminimalkan data. Sekolah tetap perlu mengonfirmasi izin memakai foto lembar jawaban siswa.
3. **Pembacaan di perangkat (browser) lebih dulu**, bukan server, karena tidak perlu menjalankan layanan gambar tambahan. Keputusan final setelah spike 02.
4. **Pilot paralel:** ujian pertama tetap dikoreksi manual oleh guru. Aplikasi dibandingkan: 100% soal yang ditandai ragu/ganda diperiksa, ditambah sampel acak 10% lembar.
   Selisih dicatat sebagai data akurasi nyata pertama.

## Jadwal kerja (H = hari ujian; tanggal tergantung hari ujian sebenarnya)
| Hari | Pekerjaan | Keluaran | Titik putus |
|---|---|---|---|
| H-7 (Sel 3 Nov) | Konfirmasi detail sekolah (di bawah); cetak template uji; mulai **spike 02** (30 lembar nyata, minimal 2 ponsel, cahaya kelas) | Daftar jawaban benar per lembar | |
| H-6 | Selesaikan spike 02; Gerbang 2 (arsitektur + kontrak API dibekukan) | Hasil akurasi pada foto nyata | **Gerbang spike:** bila salah baca tak ditandai > 0,5% atau foto ditolak > 25%, pakai **mode input manual** untuk pilot (pembaca ditunda) |
| H-5 s.d. H-4 | Backend + skema + akun + impor kode peserta + buat ujian + PDF LJK | Alur sampai cetak LJK | |
| H-4 s.d. H-2 | Kamera + pembaca + antrean cek ulang | Alur sampai nilai | |
| H-2 s.d. H-1 | Rekap, ekspor CSV, uji ujung ke ujung dengan lembar nyata, simulasi ujian | Daftar bug P0/P1 | Bila alur tidak utuh, **tahan rilis**; guru koreksi manual seperti biasa |
| H | Ujian pilot dampingan (koreksi manual paralel) | Data akurasi nyata | |
| H+1 | Retrospektif, putuskan R1 | | |

## Yang saya butuhkan dari sekolah (paling lambat H-6)
1. Tanggal dan jam ujian pasti; mata pelajaran dan kelas yang dipakai.
2. Jumlah siswa dan jumlah soal pilihan ganda (spike memakai 40 soal, opsi A-E).
3. Jenis ponsel yang akan dipakai guru (merek, kira-kira tahun) dan apakah ada Chrome.
4. Siapa guru pendamping, dan apakah sekolah mengizinkan memotret lembar jawaban siswa.
5. Printer dan kertas A4 yang tersedia (LJK harus dicetak 100% skala, tidak "fit to page").
6. Berapa lama sekolah mau menyimpan foto (usulan: hapus 30 hari setelah nilai final).

## Risiko utama pilot
1. Foto nyata ternyata jauh lebih buruk dari simulasi (silau, kertas melengkung, bayangan tangan). Mitigasi: spike 02 di H-7 dan titik putus H-6.
2. Proyek Supabase Free dijeda setelah 7 hari tanpa aktivitas; pilot berlangsung 1 pekan, tetapi proyek harus aktif dipakai tiap hari sampai ujian.
3. Pergeseran satu bulatan (kelemahan template dari spike 01): kode lembar non-periodik wajib ada di template sebelum dicetak.
4. Kapasitas kerja: satu pekan untuk seluruh jalur kritis menyisakan hampir tidak ada ruang untuk perubahan cakupan di tengah jalan. Perubahan cakupan setelah Gerbang 2 harus berarti sesuatu dibuang.
