# Spesifikasi OMR (Optical Mark Recognition)

## 1. Tujuan

Membaca tanda jawaban pada lembar pilihan ganda dengan template tetap. OMR membantu mendeteksi respons; hasilnya tetap harus melewati aturan validasi dan tidak langsung dianggap final.

## 2. Batasan awal

- MVP menggunakan template lembar jawaban yang ditetapkan dan dikontrol.
- Ukuran kertas, jumlah soal, jumlah opsi, area identitas, marker alignment, dan resolusi scan harus ditentukan.
- Foto dari ponsel dapat menimbulkan perspektif, bayangan, blur, dan pencahayaan tidak merata; dukung hanya setelah pengujian.
- OMR bukan OCR penuh dan tidak dimaksudkan membaca layout kertas bebas.

## 3. Alur pemrosesan

1. Validasi tipe, ukuran, dan integritas file.
2. Buat hash file untuk deduplikasi yang aman.
3. Deteksi jumlah halaman dan orientasi.
4. Temukan marker/anchor template.
5. Lakukan deskew, alignment, dan normalisasi pencahayaan.
6. Petakan koordinat setiap bubble berdasarkan versi template.
7. Ukur intensitas/rasio tanda pada setiap bubble.
8. Tentukan status per soal.
9. Simpan hasil sementara dan metadata versi algoritma.
10. Kirim respons meragukan ke antrean validasi manusia.

## 4. Status respons

| Status | Arti | Tindakan |
|---|---|---|
| `detected` | Satu opsi terdeteksi dengan jelas | Bisa menjadi hasil sementara |
| `blank` | Tidak ada opsi yang terdeteksi | Tampilkan untuk kebijakan skor kosong |
| `multiple` | Lebih dari satu opsi tampak terisi | Perlu aturan ujian dan/atau review |
| `ambiguous` | Hasil tidak cukup meyakinkan | Review manual |
| `unreadable` | Area/lembar tidak dapat diproses | Scan ulang atau review |
| `manually_corrected` | Respons telah dikoreksi pemeriksa | Simpan histori koreksi |

## 5. Aturan keselamatan hasil

- Jawaban kosong tidak sama dengan jawaban salah secara teknis; kebijakan skor ditetapkan dalam aturan ujian.
- Jawaban ganda tidak boleh diputuskan otomatis tanpa kebijakan eksplisit.
- Ambang confidence ditentukan lewat dataset pilot, bukan angka tebakan.
- Jika template tidak terdeteksi, hentikan pemrosesan dan tandai gagal.
- Simpan gambar asli sebagai bukti; hasil transformasi adalah artefak turunan.
- Setiap hasil menyimpan versi template dan algoritma.
- Reprocessing tidak boleh menimpa koreksi manual tanpa prosedur yang jelas.
- Kegagalan worker harus dapat diulang dengan idempotency key.

## 6. Antarmuka review

Pemeriksa perlu:
- melihat scan dan hasil per nomor secara berdampingan;
- zoom, rotate, dan berpindah halaman;
- melihat opsi yang terdeteksi dan statusnya;
- memilih respons final atau menandai kosong/ganda sesuai kebijakan;
- menyimpan alasan jika mengubah hasil yang terdeteksi;
- berpindah ke respons berikutnya dengan cepat.

## 7. Dataset pilot dan evaluasi

Buat dataset uji yang mewakili:
- tanda pensil tipis/tebal;
- tanda silang, arsiran, dan coretan;
- penghapusan jawaban;
- jawaban ganda;
- lembar kosong;
- rotasi dan skew;
- scan beresolusi rendah;
- pencahayaan tidak merata;
- kertas terlipat atau bernoda;
- marker template yang terpotong.

Catat minimal:
- akurasi pembacaan per respons;
- tingkat false acceptance (jawaban salah dibaca sebagai pasti);
- persentase respons yang harus direview;
- tingkat kegagalan pemrosesan per lembar;
- waktu pemrosesan per lembar.

Kriteria rilis pilot ditetapkan setelah tim akademik menyetujui batas risiko dan hasil uji. Jangan mempromosikan akurasi OMR sebelum ada hasil pengujian nyata.

## 8. Template lembar jawaban

Template perlu mendefinisikan:
- kode template dan versi;
- ukuran/format halaman;
- anchor/alignment markers;
- area identitas atau barcode/QR/nomor peserta;
- koordinat bubble setiap nomor dan opsi;
- area jawaban esai atau referensi halaman;
- jumlah soal dan opsi;
- aturan versi serta tanggal berlaku.

Format identitas harus mengurangi risiko lembar tertukar. Nama saja tidak disarankan sebagai satu-satunya pengenal.
