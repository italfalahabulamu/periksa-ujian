# Spike 01: hasil (data sintetis)

Tanggal: 2026-11-01. Kode: `spikes/omr-01/`. Status spike: **dijalankan sebagian**. Tidak ada foto nyata dari ponsel.

## Yang dilakukan dan yang belum
| Rencana (spike-01-omr-akurasi.md) | Status |
|---|---|
| Template LJK dengan marka sudut | Dilakukan (A4, 40 soal, A-E) |
| Lembar terisi dengan variasi tanda | Dilakukan, **sintetis**: kuat, sedang, tipis, sebagian, bekas hapusan, ganda, kosong |
| Foto dengan berbagai ponsel dan cahaya | **Belum.** Diganti simulasi: perspektif, rotasi (termasuk 180 derajat), cahaya tidak rata, bayangan, blur, noise, JPEG |
| Bandingkan OMRChecker dan pipeline OpenCV sendiri | **Belum.** Hanya pipeline OpenCV sendiri |
| Ukur ukuran foto dan waktu proses | Sebagian (lihat bawah) |

## Cara uji
Dua set terpisah dengan seed berbeda. Set kalibrasi (seed 1, 20 lembar per kondisi) dipakai untuk memperbaiki bug dan
menetapkan dua ambang. Set uji (seed 2, 40 lembar per kondisi) dijalankan **sekali** setelah itu, tanpa penyetelan lagi.
Tiga kondisi: A mudah (cahaya rata, blur kecil), B sedang (gradien cahaya, rotasi sampai 8 derajat, 10% lembar terbalik 180 derajat),
C berat (redup + bayangan, perspektif kuat, blur besar, 10% terbalik).

Satuan penilaian adalah satu soal. **Salah baca tak ditandai** = sistem melaporkan jawaban pasti yang salah (atau kosong)
padahal seharusnya jawaban lain atau perlu dicek. Soal dengan tanda ganda yang dilaporkan "ganda" dianggap benar.
"Ragu" = sistem meminta guru memeriksa.

## Hasil set uji (seed 2)
| Kondisi | Lembar | Tidak terbaca | Soal | Salah baca tak ditandai | Batas atas 95% | Ragu pada jawaban bersih* | Ukuran foto |
|---|---:|---:|---:|---:|---:|---:|---:|
| A mudah | 40 | 0 | 1600 | 0 | 0,24% | 3,7% | ± 526 KB |
| B sedang | 40 | 0 | 1600 | 0 | 0,24% | 4,3% | ± 454 KB |
| C berat | 40 | 5 (12,5%) | 1400 | 0 | 0,27% | 4,4% | ± 467 KB |
| Gabungan | 120 | 5 | 4600 | 0 | 0,08% | | |

*Hampir seluruhnya soal yang punya bekas hapusan di pilihan lain (diminta dicek karena memang ada coretan). Soal bersih
tanpa bekas: 1 dari 3.714 yang diragukan (kondisi C).

Lembar "tidak terbaca" tidak dibaca sama sekali dan diminta difoto ulang; ini perilaku yang diinginkan, bukan salah baca.
Waktu baca ± 2,2-2,9 detik per lembar di Python pada mesin sesi ini (bukan ukuran untuk ponsel atau browser).

## Perjalanan dan bug yang ditemukan (penting untuk desain)
1. **Pita tepi kertas melingkupi marka.** Pada foto dengan latar abu-abu, `RETR_EXTERNAL` melewatkan semua marka. Diperbaiki dengan
   `RETR_CCOMP`.
2. **Grid bulatan itu periodik.** Sebuah homografi yang bergeser tepat satu jarak bulatan tetap menghasilkan skor "garis tepi cocok"
   yang tinggi, tetapi seluruh jawaban terbaca salah (skor bahkan lebih tinggi daripada lembar benar). Karena itu skor pendaftaran
   **tidak boleh** dipakai untuk memilih antar kandidat. Pemilihan memakai geometri marka, dan dua pemeriksaan independen dipakai
   sebagai gerbang: ukuran marka harus cocok dengan homografi, dan kontras garis tepi bulatan harus di atas batas.
   Pelajaran untuk produksi: tambahkan fitur non-periodik (mis. kode lembar atau marka tambahan di sisi) agar pergeseran satu bulatan terdeteksi.
3. **Salah arah sendiri:** sempat mengetatkan filter bentuk marka sehingga marka yang kabur ikut gugur (kondisi C hampir semua gagal).
   Dikembalikan.
4. **Isian sebagian yang tipis dibaca kosong.** Pada lintasan pertama (10 lembar per kondisi, ambang ragu 0,22) ada 8 salah baca tak ditandai
   dari 1.160 soal (0,69%), semuanya isian sebagian dengan rasio isi 0,14-0,20. Ambang ragu diturunkan ke 0,12, tepat di atas semua
   bulatan kosong di set kalibrasi (maks 0,09). Konsekuensinya: bekas hapusan (0,12-0,23) ikut ditandai. Ini keputusan kebijakan:
   lebih baik guru memeriksa bekas hapusan daripada jawaban hilang diam-diam.

## Batas kesimpulan (baca sebelum memakai angka di atas)
- **Data sintetis buatan saya.** Ambang diturunkan dari sebaran generator yang sama, jadi angka di atas hampir pasti terlalu optimis.
  Yang valid: **jalur kode bekerja**, dan **jenis kegagalan** (marka tersaring, pergeseran satu bulatan, tanda tipis) nyata dan akan muncul pada foto asli.
  Yang belum terbukti: akurasi pada ponsel, pensil dan pulpen asli, silau, kertas melengkung, bayangan tangan, warna.
- 0 salah baca dari 4.600 soal hanya membuktikan batas atas 0,08% **pada data sintetis ini**.
- 12,5% lembar tidak terbaca pada kondisi berat menunjukkan foto yang buruk harus ditolak dengan panduan jelas di aplikasi, bukan dipaksa dibaca.
- Isian (jawaban singkat), kode peserta, dan nilai tidak diuji di spike ini.

## Keputusan yang bisa diambil sekarang dan yang tidak
- Bisa: pendekatan marka sudut + homografi + rasio isi + gerbang kualitas **layak dilanjutkan** ke spike foto nyata.
- Bisa: template perlu fitur non-periodik (kode lembar) dan panduan bingkai di kamera.
- Belum bisa: memilih pembacaan di perangkat atau di server. Spike berikutnya harus mengukur waktu dan akurasi di ponsel nyata.
- Belum bisa: menyatakan target akurasi tercapai. Target usulan (salah baca tak ditandai ≤ 0,5%, ragu pada jawaban bersih ≤ 5%) hanya diuji di data sintetis.

## Spike 02 (usulan): foto nyata
Cetak 30 lembar template, isi dengan pensil/pulpen oleh relawan, foto dengan 3 ponsel (termasuk kelas menengah ke bawah) pada 3 kondisi cahaya,
catat kebenaran dasar per soal, jalankan pembaca yang sama tanpa mengubah ambang, lalu bandingkan dengan tabel di atas.
