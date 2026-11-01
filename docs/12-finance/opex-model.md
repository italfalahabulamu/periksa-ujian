# Model Biaya (Fase 1, versi awal)

Keputusan Gerbang 1: aplikasi **gratis untuk sekolah**. Maka biaya ditanggung pemilik proyek, dan model ini menjawab "berapa lama bisa gratis".

## Asumsi (terpisah dari hasil)
| Kode | Asumsi | Sumber/status |
|---|---|---|
| A1 | Batas Free Supabase: DB 500 MB, berkas 1 GB, egress 5+5 GB, 50.000 MAU, 500.000 invokasi, 2 proyek aktif | Artikel pihak ketiga (Juli 2026), **BELUM TERVERIFIKASI ke halaman resmi** |
| A2 | Proyek Free dijeda setelah 7 hari tanpa aktivitas | Sumber yang sama |
| A3 | Pro: $25/bulan/organisasi, DB 8 GB, berkas 100 GB | Sumber yang sama |
| A4 | Akun Google Play: $25 sekali bayar; akun pribadi baru wajib uji tertutup 12 penguji selama 14 hari berturut-turut sebelum produksi | magora-systems.com, 4 Okt 2026 (dicek 13 Okt 2026) |
| A5 | Apple Developer Program: $99/tahun | Sumber yang sama |
| A6 | Ukuran foto LJK setelah dikompres sekitar 300 KB | **ASUMSI kami, belum diukur** (diukur di spike 01) |
| A7 | Biaya layanan pemrosesan gambar dan panggilan LLM | **BELUM DIKETAHUI**, bergantung hasil spike dan pilihan penyedia |

## Biaya satu kali
- Google Play: $25 (A4). Android adalah target pertama; iOS ($99/tahun) ditunda sampai ada permintaan nyata.
- Uji tertutup Google Play butuh 12 penguji selama 14 hari: perlu direncanakan sebagai pekerjaan jadwal, bukan biaya.

## Biaya bulanan per skenario (hanya yang bisa dihitung sekarang)
| Skenario | Database | Penyimpanan foto | Catatan |
|---|---|---|---|
| 1 sekolah pilot (± 10 kelas) | Muat di Free (baris teks kecil) | 1 GB ÷ 300 KB ≈ 3.300 foto (hitungan dari A6) | Hapus foto setelah masa verifikasi supaya tidak habis |
| Beberapa sekolah | Mendekati batas 500 MB / 1 GB lebih cepat | Foto jadi batas pertama | Pertimbangkan Pro ($25/bln) atau simpan hasil tanpa foto |
| Pemrosesan gambar & LLM | belum dihitung (A7) | | Wajib dihitung setelah spike 01 |

Perhitungan 1 GB ÷ 300 KB: 1.000.000 KB ÷ 300 KB ≈ 3.333 foto. Jumlah ini hanya sah bila A6 benar.

## Risiko biaya
1. **Penjedaan proyek Free** bukan biaya uang tetapi biaya keandalan: aplikasi mati di hari ujian. Mitigasi: aktivitas terjadwal atau naik ke Pro menjelang masa ujian.
2. **Gratis tanpa sumber pendapatan** menuntut batas pemakaian (jumlah foto per bulan, panggilan LLM per guru) agar biaya tidak tak terbatas.
3. Biaya LLM untuk telaah soal bisa naik tidak linear; jadikan fitur ini berkuota.

## Sensitivitas (yang bisa dikatakan sekarang)
- Jika ukuran foto dua kali lipat (600 KB), kapasitas foto turun separuh (± 1.670 foto per GB).
- Titik di mana Free tidak cukup lagi belum bisa ditentukan sebelum A6 dan A7 terukur.

## Pelacakan biaya
Pasang peringatan penggunaan di Supabase, catat jumlah foto dan invokasi per bulan, bandingkan dengan perkiraan ini di Fase 9.

## Catatan
Ini bukan nasihat pajak atau akuntansi berlisensi. Aplikasi ini tidak menyimpan uang, jadi desain buku besar tidak berlaku.
