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

Foto ponsel **tidak didukung di MVP** kecuali spike terpisah lulus (pencahayaan, perspektif, blur). Bila diuji: kertas
datar di latar kontras, cahaya merata tanpa bayangan, keempat penanda terlihat, ≥ 8 MP, tegak lurus.

## 6. Kegagalan yang harus dikenali (`failure_code`)

`no_markers` (penanda < 4 ditemukan), `marker_geometry` (rasio sisi di luar toleransi → halaman terpotong/terlipat),
`low_quality` (tajam/kontras di bawah ambang), `template_mismatch` (kode ujian/halaman/versi tidak cocok),
`file_unreadable`, `id_unreadable` (cek-digit gagal atau kolom ganda). Setiap kegagalan memberi saran tindakan di UI
(scan ulang, atur manual, cocokkan peserta).

## 7. Versi dan kompatibilitas

`sheet_templates(code, version)` unik. Perubahan geometri, jumlah soal, atau blok kode = versi baru. `omr_profiles`
mengacu ke template yang dikalibrasi. Ujian menyimpan kedua ID; pengukuran menyimpan keduanya plus `algorithm_version`.
