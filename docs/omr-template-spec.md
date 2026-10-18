# Spesifikasi template lembar jawaban dan SOP pemindaian (usulan)

Status: **usulan awal untuk spike S1**. Semua angka geometri adalah titik awal yang harus diuji pada kertas dan
scanner sekolah; format final menunggu D-05 sampai D-07. Template disimpan sebagai data (`sheet_templates.layout`),
bukan konstanta di kode, dan **tidak boleh diubah setelah dipakai ujian** (revisi = versi baru).

## 1. Prinsip

- Template terkendali (PRD §4): satu layout per format ujian; bukan pengenalan layout bebas.
- Posisi diukur **relatif terhadap penanda sudut**, bukan terhadap tepi kertas, supaya tahan geser/rotasi/skala kecil.
- Pengukuran hanya di area gelembung (tidak perlu me-*warp* seluruh gambar).
- Identitas lembar harus mengurangi risiko tertukar; nama saja tidak cukup (PRD OMR §8).

## 2. Geometri (A4 portrait, satuan mm)

| Elemen | Usulan | Alasan/catatan |
|---|---|---|
| Penanda sudut | 4 persegi hitam solid 10×10, pusat 12 mm dari tiap tepi | Di luar area tak-tercetak printer (biasanya ±4–5 mm) |
| Penanda orientasi | 1 batang hitam 3×20 di samping penanda kiri-atas | Membedakan rotasi 180°/mirror |
| Gelembung | lingkaran Ø 4,5 (garis tipis abu-abu); area ukur = cakram dalam ≤ 60% jari-jari | Garis tepi tidak ikut terukur |
| Jarak | antar-opsi 7 horizontal; antar-baris 6,5 vertikal | Disesuaikan agar 50 soal muat 2 kolom × 25 baris |
| Kolom soal | maks 50 soal per halaman, opsi A–E (4/5 per ujian via `option_count`) | Opsi E diabaikan bila `option_count=4` |
| Blok kode peserta | N kolom digit × 10 baris (0–9), N = panjang kode (D-07); digit terakhir = pemeriksa (Luhn) | Salah baca satu digit terdeteksi |
| Blok kode ujian | 3 digit | Silang-cek: lembar ujian salah masuk batch |
| Blok kode halaman | 1 digit/batang untuk nomor halaman (PG=1, esai 2..n) | Menghindari halaman tertukar |
| Area esai | persegi panjang per soal esai (di `layout.essay_regions`) berbingkai tipis | Tampil sebagai tujuan lompat di UI |

Koordinat dalam `layout` memakai ruang template (mm dari pusat penanda kiri-atas, sumbu ke kanan/bawah) dan
dipetakan ke gambar lewat homografi dari 4 pusat penanda.

```jsonc
// bentuk layout (ilustrasi, bukan final)
{
  "page": {"size": "A4", "markers": [[12,12],[198,12],[12,285],[198,285]]},
  "orientation_bar": {"near": 0, "rect": [16,9,20,3]},
  "bubble": {"radius_mm": 2.25, "measure_radius_ratio": 0.6},
  "id_block":   {"origin": [30,30], "cols": 8, "pitch": [7,6.5], "digits": 10, "check": "luhn"},
  "exam_block": {"origin": [100,30], "cols": 3, "pitch": [7,6.5], "digits": 10},
  "page_block": {"origin": [140,30], "cols": 1, "pitch": [7,6.5], "digits": 10},
  "answer_cols": [{"origin": [30,80], "rows": 25, "options": 5, "pitch": [7,6.5], "q_start": 1},
                  {"origin": [110,80], "rows": 25, "options": 5, "pitch": [7,6.5], "q_start": 26}],
  "essay_regions": []
}
```

## 3. Ukuran yang dikirim klien (per soal)

Untuk tiap gelembung: `fill_ratio` ∈ [0,1] = (kegelapan rata-rata cakram dalam − kegelapan latar sekitar cincin
luar) dinormalisasi oleh rentang kegelapan lembar itu sendiri. Dengan begitu pensil tipis dan cetakan pudar
tidak memakai ambang mutlak yang sama. Metrik kualitas per halaman: `marker_residual_px`, `skew_deg`,
`sharpness`, `contrast`, `bubble_baseline_spread`. Rumus final ditetapkan di S1 dan dicatat di `algorithm_version`.

## 4. SOP pencetakan dan pengisian

- Cetak pada **100% (Actual size)**, bukan "fit to page"; hitam putih/abu-abu; kertas ≥ 70 gsm.
- Penanda dan blok kode tidak boleh terpotong; cek cetakan uji sebelum perbanyak.
- Peserta: pensil 2B atau pulpen hitam, isi gelembung penuh, hapus bersih bila mengganti, tidak mencoret di luar
  gelembung, jangan melipat/menodai lembar. Isi kode peserta di blok yang disediakan.
- Lembar kosong untuk kalibrasi dicetak dari batch yang sama.

## 5. SOP pemindaian (scanner)

| Pengaturan | Nilai | Mengapa |
|---|---|---|
| Mode | **Grayscale 8-bit** (bukan 1-bit B/W) | Tingkat abu-abu dibutuhkan untuk membedakan isian tipis |
| Resolusi | 150–200 dpi (uji S1; naik hanya bila perlu) | Menjaga ukuran berkas dan storage |
| Format | PDF multi-halaman atau JPEG kualitas sedang | Ukur ukuran nyata di S1 |
| Perbaikan otomatis | **Matikan** kontras otomatis, "hapus latar", "tajamkan", penghilang bercak | Bisa menghapus isian pensil tipis |
| Pelurusan otomatis | boleh mati; aplikasi menangani kemiringan | Hindari transformasi ganda |
| Penamaan | bebas; sistem memakai hash | Tidak memuat nama siswa |

Pemilik proyek memilih **foto ponsel** sebagai sumber utama (2026-10-18); scanner menjadi cadangan. Ketentuan
khusus ponsel (template, pemotretan, ukuran berkas) ada di §8, dan harus lulus gate ponsel di
`omr-spike-plan.md` sebelum dipakai untuk data nyata.

## 6. Kegagalan yang harus dikenali (`failure_code`)

`no_markers` (penanda < 4 ditemukan), `marker_geometry` (rasio sisi di luar toleransi → halaman terpotong/terlipat),
`low_quality` (tajam/kontras di bawah ambang), `template_mismatch` (kode ujian/halaman/versi tidak cocok),
`file_unreadable`, `id_unreadable` (cek-digit gagal atau kolom ganda). Setiap kegagalan memberi saran tindakan di UI
(scan ulang, atur manual, cocokkan peserta).

## 7. Versi dan kompatibilitas

`sheet_templates(code, version)` unik. Perubahan geometri, jumlah soal, atau blok kode = versi baru. `omr_profiles`
mengacu ke template yang dikalibrasi. Ujian menyimpan kedua ID; pengukuran menyimpan keduanya plus `algorithm_version`.

## 8. Mode foto ponsel (pilihan pemilik; berisiko lebih tinggi dari scanner)

Foto ponsel menambah perspektif, bayangan, blur, distorsi lensa, dan variasi cahaya. Karena itu template punya
varian **mode ponsel** (ditandai pada kode template) dengan elemen lebih besar. Semua angka adalah titik awal yang
harus dibuktikan pada cetakan uji; bila tidak muat, turunkan jumlah soal per halaman.

### 8.1 Geometri varian ponsel (usulan)

| Elemen | Mode scanner (§2) | Mode ponsel |
|---|---|---|
| Penanda sudut | 10×10 mm, pusat 12 mm dari tepi | **15×15 mm**, pusat 14 mm dari tepi; margin putih ≥ 5 mm di sekelilingnya |
| Gelembung | Ø 4,5 mm | **Ø 6 mm** (area ukur tetap ≤ 60% jari-jari) |
| Jarak gelembung | 7 × 6,5 mm | **9 × 8 mm** |
| Soal per halaman | ≤ 50 | **≤ 40** (2 kolom × 20 baris); lebih dari itu → halaman PG kedua dengan kode halaman |
| Blok kode peserta/ujian | Ø 4,5 mm | Ø 6 mm, jarak 9 × 6,5 mm |

### 8.2 SOP pemotretan (wajib, dicetak dan ditempel di meja pemotretan)

- **Meja pemotretan standar:** penyangga/tripod ponsel ±30–40 cm di atas kertas, alas gelap polos, cahaya merata dari atas atau dua sisi,
  tanpa bayangan tangan/ponsel, **tanpa flash** (pantulan). Satu pengaturan tetap jauh lebih dapat diuji daripada pemotretan bebas.
- Kamera tegak lurus; keempat penanda dan margin ≥ 5% tampak penuh; tunggu fokus tajam; satu halaman = satu foto.
- Matikan HDR, filter kecantikan, dan "peningkatan dokumen" otomatis (bisa menghapus isian pensil tipis); mode foto biasa, resolusi 12 MP atau lebih.
- **Format JPEG.** iPhone menyimpan HEIC secara bawaan dan browser desktop umumnya tidak membukanya: atur kamera ke
  format paling kompatibel (JPEG). Verifikasi pada perangkat nyata di S1.
- Pindahkan ke laptop dengan kabel atau penyimpanan awan; **hindari aplikasi pesan yang mengompres foto** (kirim sebagai
  berkas/dokumen). Kompresi tambahan menurunkan akurasi dan tidak dapat dibatalkan.
- Perkiraan beban kerja (hitungan kasar, belum diukur): 150 siswa × 3–4 foto ≈ 450–600 foto ≈ 2–3,3 jam pada 15–20 detik per foto.

### 8.3 Pengolahan di klien

1. Dekode foto resolusi penuh (perhatikan orientasi EXIF) di Web Worker; **ukur dari resolusi penuh**.
2. Umpan balik instan: foto buram, penanda tidak lengkap, atau kontras rendah ditolak saat itu juga dengan alasan
   (`failure_code`), agar dipotret ulang selagi kertas masih di meja.
3. Setelah pengukuran sukses, buat **salinan bukti**: sisi panjang ≤ 2.000 px, JPEG kualitas ±80 (target ≤ 0,5 MB,
   diukur di S1). **Yang diunggah ke storage adalah salinan ini.** Foto mentah 12 MP (±3–5 MB) akan memakai 1,35–3 GB
   per ujian pada skala 150 siswa × 3–4 halaman, melebihi 1 GB storage Free.
4. Catat `file_hash` foto asli dan hash salinan; foto asli tetap berada di perangkat operator sampai nilai difinalisasi (SOP).
   Ini penyimpangan terkontrol dari "simpan gambar asli" (PRD OMR §5) demi kuota; menunggu persetujuan (D-23).
5. Mode dua perangkat (ponsel hanya mengunggah, laptop mengukur antrean `uploaded`) didukung kontrak RPC tetapi
   **tidak masuk pilot**.
