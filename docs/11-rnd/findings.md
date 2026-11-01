# Temuan R&D (Fase 1)

Tanggal akses semua sumber: 2026-11-01. Penanda: **[SUMBER]** = dibaca dari halaman, **[KESIMPULAN]** = penalaran kami, **[BELUM TERVERIFIKASI]** = belum dicek ke sumber primer.

## Pertanyaan riset (urut menurut risiko)
1. Apakah foto LJK dari ponsel bisa dibaca cukup akurat dengan teknologi yang sudah ada?
2. Apakah batas gratis Supabase cukup untuk sekolah, dan apa jebakannya?
3. Apa yang sudah ada di pasar, dan celah mana yang tersisa?
4. Aturan data siswa (anak) apa yang mengikat desain sejak awal?
5. Ambang apa yang dipakai untuk menafsirkan analisis butir soal?

## 1. Pembacaan LJK (OMR)
- **[SUMBER]** OMRChecker (Python + OpenCV, lisensi MIT) membaca lembar OMR dari pemindai dan foto ponsel, memakai `template.json`. Proyek ini mengklaim hampir 100% akurat pada hasil pindai bagus dan sekitar 90% pada foto ponsel. Ia menyebut dirinya masih di tahap "hanya developer yang bisa memakai", dan fitur `--autoAlign` ditandai usang karena kurang bagus pada lembar umum. Sumber: https://github.com/Udayraj123/OMRChecker
- **[KESIMPULAN]** Angka 90% pada foto ponsel tidak cukup untuk menilai siswa. Karena kita memakai template buatan aplikasi (keputusan Gerbang 1), kita bisa menaruh marka sudut dan menandai bulatan ambigu sebagai "perlu dicek guru" alih-alih menebak. Itu cara paling murah menaikkan keandalan.
- **[SUMBER]** Beberapa skripsi/jurnal Indonesia sudah membahas koreksi LJK dengan OpenCV di Android (mis. repositori Telkom University, jurnal CORE UNUJA). Ini menunjukkan pendekatannya layak, tetapi belum kami baca isinya, jadi tidak dipakai sebagai bukti akurasi.
- **[KESIMPULAN, perlu spike]** Supabase Edge Functions memakai runtime Deno, sedangkan OpenCV paling matang di Python/C++/mobile. Pilihannya: (a) baca di perangkat dengan OpenCV mobile, atau (b) layanan Python terpisah. Ini keputusan Architect setelah spike, bukan sekarang.

## 2. Supabase (batas gratis)
Sumber: artikel pihak ketiga https://www.jetadmin.io/blog/supabase-pricing-2026-guide-to-plans-limits-and-real-world-costs/ (menyatakan diverifikasi ke halaman harga Supabase pada 16 Juli 2026). Halaman resmi supabase.com/pricing tidak bisa dibuka dari sesi ini, jadi **[BELUM TERVERIFIKASI ke sumber primer]**.
- Free: database 500 MB, penyimpanan berkas 1 GB, egress 5 GB (tak ter-cache) + 5 GB (ter-cache), 50.000 MAU, 500.000 pemanggilan Edge Function, dua proyek aktif per akun.
- **Proyek gratis dijeda setelah 7 hari tanpa aktivitas** dan harus diaktifkan manual. **[KESIMPULAN]** Ini jebakan terbesar untuk sekolah: ujian terjadi per semester, jadi proyek bisa terjeda di antara ujian. Perlu rancangan (aktivitas berkala, atau naik ke Pro).
- Pro: $25 per bulan per organisasi, database 8 GB, penyimpanan 100 GB, cadangan harian 7 hari. Free tidak tercantum punya cadangan harian, jadi cadangan sendiri perlu dirancang (DevOps).

## 3. Pasar dan pesaing
- **[SUMBER]** EvalBee: aplikasi gratis di Google Play, memindai LJK lewat kamera, pilihan A-E, benar/salah, matriks dan numerik, maksimal 240 soal, ringkasan nilai diekspor ke Excel. Artikel bertanggal 9 September 2023, jadi fitur dan harga sekarang **[BELUM TERVERIFIKASI]**. Sumber: https://guruinovatif.id/artikel/cara-membuat-soal-ljk-dan-scan-otomatis-dengan-aplikasi-gratis-evalbee
- Artikel itu tidak menyebut analisis butir atau telaah kualitas soal. **Ini bukan bukti bahwa EvalBee tidak punya fitur itu**; perlu dicek langsung.
- **[KESIMPULAN]** Pemindai LJK gratis sudah ada. Pembeda yang masuk akal untuk kita adalah modul Telaah Soal (analisis butir + pemeriksaan kunci) yang terhubung ke hasil ujian nyata. Perlu diuji ke guru apakah itu benar-benar dibutuhkan.

## 4. Data siswa dan hukum (UU PDP No. 27 Tahun 2022)
Sumber: https://pasal.id/peraturan/uu/uu-no-27-tahun-2022 (halaman memotong sebagian pasal; naskah resmi ada di peraturan.go.id).
- Data anak termasuk data pribadi spesifik (Pasal 4 ayat 2). Pemrosesannya "diselenggarakan secara khusus" dan perlu persetujuan orang tua/wali (Pasal 25).
- Pengendali wajib menjaga keamanan data (Pasal 35-39), mencatat kegiatan pemrosesan (Pasal 31), dan memberi tahu kegagalan pelindungan data tertulis paling lambat 3x24 jam (Pasal 46).
- Berlaku sejak 17 Oktober 2022; masa penyesuaian dua tahun berakhir 17 Oktober 2024. Jadi aturan ini sudah sepenuhnya berlaku.
- **[KESIMPULAN]** Siapa "pengendali data" (sekolah atau kita) dan bagaimana persetujuan orang tua dikumpulkan adalah pertanyaan hukum. Ditandai untuk penasihat hukum, bukan diputuskan di sini. Desain yang aman tanpa menunggu: minimalkan data siswa (nomor induk atau kode, bukan data lengkap), hapus foto LJK setelah masa verifikasi, enkripsi, RLS ketat.

## 5. Ambang analisis butir soal
Sumber: tabel dalam studi BMC Medical Education, "Item analysis: the impact of distractor efficiency on the difficulty index and discrimination power of multiple-choice items". https://bmcmededuc.biomedcentral.com/articles/10.1186/s12909-024-05433-y/tables/1 dan /tables/2
- Indeks kesulitan (persen benar): 76-100 mudah, 26-75 dapat diterima, 0-25 sulit.
- Daya beda: ≤0,20 tidak membedakan, 0,21-0,24 dapat diterima, 0,25-0,34 baik, ≥0,35 sangat baik.
- Ambang efisiensi pengecoh tidak terbaca dari halaman itu. **[BELUM TERVERIFIKASI]**: definisi "pengecoh fungsional" (lazimnya dipilih oleh persentase kecil siswa tertentu) perlu dicari dari sumber lain sebelum dipakai.
- Ambang ini dari konteks pendidikan kedokteran. Apakah cocok untuk ujian sekolah perlu disetujui guru atau ahli evaluasi pendidikan.

## Radar teknologi (sementara)
| Teknologi | Status | Alasan |
|---|---|---|
| OpenCV (inti pembacaan bulatan) | Coba (spike) | Dipakai luas, MIT/Apache; akurasi foto ponsel harus diukur sendiri |
| OMRChecker | Coba (spike) | MIT, bisa jadi dasar template/logika; tidak dijadikan fondasi produksi tanpa persetujuan Tech Lead |
| Supabase (Postgres, Auth, Storage, RLS) | Pakai | Sesuai keputusan stack; waspadai penjedaan proyek gratis |
| Edge Functions untuk pemrosesan gambar | Tunda | Runtime Deno; keputusan setelah spike |
| LLM untuk menelaah soal ambigu | Coba | Hanya saran; biaya per panggilan belum diverifikasi |

## Ketidakpastian yang tersisa
1. Akurasi nyata pada foto dari ponsel murah dan cahaya kelas (spike 01).
2. Fitur EvalBee dan pesaing lain saat ini.
3. Harga resmi Supabase dan biaya LLM.
4. Status hukum peran kita terhadap data siswa.
