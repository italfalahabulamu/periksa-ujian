# Paket keputusan untuk Gerbang 1 dan 2

Status: baris yang tercantum di §0 sudah **dijawab pemilik pada 2026-10-18** (penegasan resmi Gerbang 1/2 masih
menunggu); baris lain menunggu. "Rekomendasi" adalah usulan dengan alasan, bukan
keputusan. Bila Anda setuju semuanya, cukup balas "setuju semua"; bila tidak, sebut ID yang berbeda.
Keputusan D-01..D-15 berasal dari `docs/prd/11-OPEN-DECISIONS.md`; D-16..D-22 ditambahkan oleh riset ini.

## 0. Jawaban pemilik proyek (2026-10-18)

| ID | Jawaban | Sesuai rekomendasi? | Dampak |
|---|---|---|---|
| D-12 | Sekitar **150 siswa** per ujian; **PG + esai (2–3 halaman esai)** → 3–4 halaman scan per siswa; soal per siswa **"> 10"** (jumlah pasti belum diketahui) | — | Model kapasitas di bawah; jumlah soal menentukan ukuran sampel uji OMR |
| D-16 | Ujian pertama **kurang dari 1 bulan** (sebelum ±18 Nov 2026) | — | MVP penuh (±7–9 minggu) tidak muat → **pilot ramping** (`tasks.md` §0) |
| Cakupan | **Pilot ramping + OMR** | Ya | Review OMR dibangun lebih dulu; mode input manual sebagai cadangan (`tasks.md` §0) |
| D-03 | **Proyek Supabase baru terpisah, tetap Free** | Tidak (rekomendasi: Pro) | Ketersediaan slot proyek aktif **belum diverifikasi**; wajib `keepalive`, purge scan, batas kapasitas |
| D-05 | **Template baru dari aplikasi** (belum punya LJK) | Ya | Kita yang menentukan geometri; cetak uji dulu |
| D-06 | **Foto ponsel** (bukan scanner) | **Tidak** (rekomendasi: scanner) | Jalur utama kini berisiko lebih tinggi; template mode ponsel, meja pemotretan, gate ponsel, cadangan (`omr-template-spec.md` §8, `omr-spike-plan.md` §7) |
| D-07 | **Kolom digit kode peserta + digit pemeriksa** | Ya | Sesuai `omr-template-spec.md` |
| D-08, D-09 | **Setuju rekomendasi** (kosong = 0; ganda/ambigu dicek manusia lalu 0 bila ganda; tanpa nilai negatif; bobot eksplisit per ujian; nilai akhir 2 desimal) | Ya | Tidak ada perubahan rancangan |
| D-14 | Scan **dihapus 90 hari setelah final** | Ya | Pada Free hanya aman bila ujian bersamaan ≤ 2–4 (lihat di bawah) |
| D-20 | Operator/guru memakai **laptop/PC dengan Chrome atau Edge** | Ya | OMR berjalan di laptop; ponsel hanya untuk memotret |

**Kapasitas dengan jawaban di atas** (150 siswa × 3–4 halaman; Free = 1.000 MB; ukuran per halaman masih asumsi):

| Halaman/siswa | MB/halaman | MB per ujian | Ujian bersamaan muat di 1 GB |
|---:|---:|---:|---:|
| 3 | 0,4 | 180 | 5,6 |
| 4 | 0,2 / 0,4 / 0,8 | 120 / 240 / 480 | 8,3 / 4,2 / 2,1 |

Dengan retensi 90 hari, semua ujian dalam jendela 90 hari menumpuk bersamaan. Untuk pilot (1–2 ujian) Free cukup;
untuk pekan ujian dengan banyak mapel PG + esai **tidak cukup** → pilihan: purge lebih cepat (mis. 14–30 hari setelah
final), kurangi halaman esai, atau naik ke Pro sebelum pekan ujian. **Foto ponsel mentah (12 MP, ±3–5 MB)** akan
memakai 1,35–3 GB per ujian, sehingga **wajib diperkecil di klien** sebelum diunggah (`omr-template-spec.md` §8).

**Masih dibutuhkan dari pemilik** (tidak menghalangi mulai, tetapi menentukan angka): jumlah soal pasti per ujian
(maksimum PG dan jumlah soal esai), jumlah mapel dan tanggal ujian pertama, jenis ponsel (Android/iPhone), panjang
kode peserta (mis. NIS berapa digit), konfirmasi slot proyek Supabase Free dari tim Supabase, dan penegasan resmi
Gerbang 1.

## A. Yang paling membuka jalan (jawab dulu)

| Urutan | ID | Mengapa menentukan |
|---|---|---|
| 1 | D-12 + D-16 | Volume dan tanggal ujian pertama menentukan paket Supabase, prioritas, dan jadwal |
| 2 | D-03 | Proyek Supabase baru kemungkinan butuh paket berbayar (batas 2 proyek aktif di Free) |
| 3 | D-05, D-06, D-07 | Format lembar, sumber scan, dan identitas peserta menentukan desain OMR; spike S1 tak bisa mulai tanpanya |
| 4 | D-14 | Retensi scan menentukan apakah 1 GB cukup |
| 5 | D-08, D-09 | Kebijakan nilai harus tetap sebelum satu ujian pun diproses |
| 6 | D-17 | Telaah hukum data anak sebelum pilot dengan data nyata |

## B. Keputusan dan rekomendasi

| ID | Pertanyaan | Rekomendasi | Alasan / konsekuensi bila berbeda |
|---|---|---|---|
| D-01 | Framework frontend | **Ikuti FTS: JS murni (ES modules), tanpa framework**, sampai audit HRIS langsung (A-01) membuktikan sebaliknya | FTS adalah turunan HRIS yang sudah berjalan; PRD melarang menebak. Framework baru = pola teknis kedua |
| D-02 | Repo terpisah/monorepo | **Terpisah** (sudah: `periksa-ujian`) | Terjawab oleh keputusan #1 di STATE |
| D-03 | Supabase proyek sama/terpisah dari HRIS | **Proyek terpisah, paket Pro ($25/bln)** bila organisasi sudah memakai 2 proyek aktif | Data anak + scan + ledakan dampak RLS; Pro juga menutup storage 1 GB, jeda 1 minggu, dan memberi cadangan (R3). Alternatif: skema terpisah di proyek lain, **tidak dianjurkan** (blast radius, dan proyek FTS direncanakan anonimisasi 31 Des 2026). Jumlah proyek saat ini perlu dicek tim Supabase |
| D-04 | Login/SSO HRIS | **Tidak di MVP.** Akun staf dibuat admin; reset sandi oleh admin | SSO menautkan domain keamanan HRIS; evaluasi terpisah |
| D-05 | Format lembar | **A4 portrait, ≤ 50 soal/halaman, opsi A–E (ujian memilih 4 atau 5), 4 penanda sudut + batang orientasi**; esai di halaman terpisah | Cocok kebiasaan LJK; detail di `omr-template-spec.md`. Format lain = template versi lain |
| D-06 | Sumber scan | **Scanner (ADF/flatbed) grayscale 150–200 dpi** untuk MVP; foto ponsel hanya setelah gate terpisah lulus. **→ Pemilik memilih foto ponsel (§0); scanner menjadi cadangan** | Variasi foto menaikkan risiko salah baca dan tingkat review |
| D-07 | Identifikasi peserta | **Blok digit kode peserta (dengan digit pemeriksa Luhn) + kode ujian + kode halaman** di MVP; **QR per siswa** saat fitur cetak lembar (P1) tersedia | Tidak perlu mencetak per-siswa untuk memulai; cek-digit menangkap salah baca. `jsqr.js` sudah ada di FTS untuk tahap QR |
| D-08 | Skor jawaban ganda/kosong | `blank_policy=zero` (tanpa pengurangan); ganda/ambigu **wajib review**; ganda yang dikonfirmasi → `multiple_policy=zero`; tanpa nilai negatif | Konsisten PRD: ganda tidak diputuskan otomatis; keduanya disimpan per ujian |
| D-09 | Formula nilai | Rumus PRD §9 dengan bobot **eksplisit per ujian** (tanpa default tersembunyi; antarmuka mengisi usulan 0,7/0,3 yang harus dikonfirmasi); PG-saja/esai-saja = bobot 1; `numeric`; bulatkan **sekali** di nilai akhir ke 2 desimal (setengah menjauhi nol) | Hindari galat float (84,005 → 84,0 di float). Pembulatan ke bilangan bulat untuk rapor ditentukan sekolah di luar sistem atau sebagai opsi tampilan |
| D-10 | Nilai final bisa diubah? | **Ya, hanya lewat `reopen_exam` (seluruh ujian) atau `amend_final_score` (satu siswa)**, izin khusus terpisah, alasan ≥ 10 karakter, snapshot append-only | PRD: izin khusus + alasan + audit |
| D-11 | Ekspor wajib | **CSV (UTF-8 BOM, pembersih rumus) + XLSX di MVP** | `export-xlsx.js`/`xlsx.js` sudah ada di FTS sehingga murah; Excel berlokal Indonesia memakai `;` sebagai pemisah daftar, CSV mentah sering salah buka |
| D-12 | Volume siswa/lembar per batch | **Perlu data dari Anda**: jumlah siswa SMP, jumlah mapel per periode, halaman per siswa, adakah esai | Dipakai pada model kapasitas (riset §2); contoh 300 siswa + esai 3 halaman = 180–720 MB per ujian |
| D-13 | Target akurasi OMR | Gate S1 sebagai titik awal: FA ≤ 0,1%, review ≤ 10%, gagal ≤ 2% (scanner) | Hanya hipotesis; tim akademik menetapkan toleransi risiko (`omr-spike-plan.md` §5) |
| D-14 | Retensi scan/nilai | **Nilai, respons, audit, snapshot: disimpan lama (sesuai arsip sekolah). Scan: dihapus N hari setelah finalisasi (usulan N = 90) kecuali ditandai ditahan**; job purge terjadwal | Tanpa purge atau Pro, 1 GB cepat habis; juga meminimalkan data anak yang disimpan. N dan jangka arsip nilai harus dari kebijakan sekolah |
| D-15 | Siapa boleh lihat scan/jawaban | Admin; guru pengampu/pemilik ujian; staf `grader`/`scanner` yang ditugaskan; **bukan pimpinan** secara default; siswa/wali tidak punya akses di MVP | Least privilege (`permissions-rls.md`) |
| D-16 | **Baru:** tanggal ujian pertama yang ingin dipakai & tanggal pilot | **Perlu data dari Anda** | Menentukan apakah spike S1 harus dimulai sekarang dan apakah cakupan perlu dipotong |
| D-17 | **Baru:** dasar hukum data anak & persetujuan wali (UU 27/2022) | **Telaah hukum sebelum pilot data nyata**; sementara pilot memakai data fiktif; minimalkan data pribadi | Sebuah ringkasan firma hukum menyebut data anak sebagai data pribadi spesifik; detail pasal belum terverifikasi (riset R8) |
| D-18 | **Baru:** penilaian esai buta (nama disembunyikan) | **Opsi per ujian, ditunda ke P1** | Mengurangi bias; tidak diperlukan untuk MVP |
| D-19 | **Baru:** peserta susulan/ujian ulang | **MVP: status `absent`, tanpa nilai; susulan = P1** memakai `attempt_no` | Aturan bisnis #3 PRD mensyaratkan mekanisme eksplisit; belum dibutuhkan untuk pilot |
| D-20 | **Baru:** perangkat operator dan scanner | **Perlu data dari Anda**: model scanner (ADF? dpi), spesifikasi laptop/tablet, browser | Uji kinerja S1 dilakukan pada perangkat ini |
| D-21 | **Baru:** simpan teks/gambar soal? | **Tidak di MVP**; hanya nomor, tipe, skor, jumlah opsi, kunci | Mengurangi cakupan dan data; analisis butir tetap bisa berjalan |
| D-22 | **Baru:** penyetuju gerbang | **Anda (pemilik proyek)** sebagai penyetuju tunggal, kecuali Anda menunjuk lain | Mengikuti pola FTS |
| D-23 | **Baru (dari pilihan ponsel):** foto asli diperkecil sebelum diunggah | **Ya**: unggah salinan ≤ 2.000 px (≈ ≤ 0,5 MB), foto mentah disimpan di perangkat operator sampai nilai final; hash keduanya dicatat | Foto mentah 12 MP memakai 1,35–3 GB per ujian (150 siswa × 3–4 hal.); menyimpang dari "simpan gambar asli" PRD, sehingga perlu persetujuan eksplisit Anda |

## C. Syarat Gerbang 1 (PRD dan lingkup)

- [ ] D-12, D-16 dijawab; lingkup MVP (`docs/prd/02-SCOPE-MVP.md` P0) disetujui atau dipotong.
- [ ] D-08, D-09, D-10 disetujui sebagai kebijakan nilai.
- [ ] D-15 disetujui sebagai kebijakan akses.
- [ ] Pemilik proyek menyetujui `docs/prd/01-PRD.md` sebagai baseline v0.1 (atau menyebut perubahan).

## D. Syarat Gerbang 2 (arsitektur)

- [ ] D-01, D-03, D-04 disetujui (ADR-0001 menjadi "diterima").
- [ ] D-05, D-06, D-07 disetujui; spike S1 dijadwalkan; ADR-0002 tetap "diusulkan" sampai S1 lulus.
- [ ] D-14, D-17 punya jalur penyelesaian (kebijakan + telaah hukum) sebelum pilot data nyata.
- [ ] `architecture.md`, `data-model.md`, `permissions-rls.md`, `rpc-contracts.md`, `threat-model.md`,
      `test-strategy.md` ditinjau dan disetujui atau direvisi.
- [ ] Audit HRIS/FTS (A-01) selesai → `HRIS-ARCHITECTURE-NOTES.md`.
