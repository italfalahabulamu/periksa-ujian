# Implementation Backlog

Backlog awal untuk dipindahkan ke GitHub Issues. Estimasi dan prioritas perlu disesuaikan setelah audit repository HRIS.

## Epic A — Audit dan fondasi

- [ ] **A-01 Audit repository HRIS**  
  Catat framework, routing, UI, auth, Supabase, Cloudflare, CI/CD, dan conventions.  
  **Acceptance:** `HRIS-ARCHITECTURE-NOTES.md` disetujui.

- [ ] **A-02 Putuskan strategi repository dan environment**  
  **Acceptance:** keputusan repo, staging, production, dan rollback terdokumentasi.

- [ ] **A-03 Setup aplikasi mengikuti HRIS**  
  **Acceptance:** aplikasi berjalan di local/preview menggunakan konvensi yang sama.

- [ ] **A-04 Setup migration dan RLS**  
  **Acceptance:** migration dapat dijalankan di staging; pengujian role dasar lulus.

## Epic B — Data akademik

- [ ] **B-01 Tahun ajaran dan kelas**
- [ ] **B-02 Data siswa dan keanggotaan kelas**
- [ ] **B-03 Mata pelajaran dan penugasan guru**
- [ ] **B-04 Import CSV dengan preview dan validasi**
- [ ] **B-05 Pengelolaan role dan assignment**

**Acceptance epic:** data dapat dikelola dan akses lintas kelas/role dibatasi.

## Epic C — Ujian dan kunci

- [ ] **C-01 CRUD ujian dan status**
- [ ] **C-02 Peserta ujian dan kode peserta**
- [ ] **C-03 CRUD soal pilihan ganda**
- [ ] **C-04 Kunci jawaban dan versi**
- [ ] **C-05 Rubrik esai dan versi**
- [ ] **C-06 Formula nilai dan validasi kesiapan**
- [ ] **C-07 Template lembar jawaban**

**Acceptance epic:** ujian siap diproses hanya jika konfigurasi wajib lengkap.

## Epic D — Upload dan OMR

- [ ] **D-01 Upload scan ke storage privat**
- [ ] **D-02 Batch processing dan status**
- [ ] **D-03 Validasi tipe/ukuran file dan deduplikasi**
- [ ] **D-04 Prototipe alignment template**
- [ ] **D-05 Deteksi tanda dan status respons**
- [ ] **D-06 Antrean respons ambigu**
- [ ] **D-07 UI validasi OMR**
- [ ] **D-08 Simpan histori koreksi**
- [ ] **D-09 Reprocessing idempotent**
- [ ] **D-10 Uji dataset pilot**

**Acceptance epic:** OMR menghasilkan respons sementara dan tidak memfinalisasi kasus meragukan.

## Epic E — Penilaian esai

- [ ] **E-01 Daftar antrean esai**
- [ ] **E-02 Viewer scan/crop jawaban**
- [ ] **E-03 Input skor per kriteria**
- [ ] **E-04 Validasi skor dan komentar**
- [ ] **E-05 Status draft/selesai dan audit**
- [ ] **E-06 Kontrol akses penilaian**

**Acceptance epic:** nilai esai sepenuhnya ditentukan guru sesuai rubrik.

## Epic F — Nilai dan laporan

- [ ] **F-01 Perhitungan nilai PG**
- [ ] **F-02 Perhitungan nilai esai**
- [ ] **F-03 Nilai akhir dan pembulatan**
- [ ] **F-04 Pemeriksaan kelengkapan sebelum finalisasi**
- [ ] **F-05 Finalisasi dan reopen terkendali**
- [ ] **F-06 Laporan nilai siswa**
- [ ] **F-07 Rekap kelas dan filter**
- [ ] **F-08 Ekspor CSV**
- [ ] **F-09 Analisis butir soal (P1)**

## Epic G — Keamanan dan rilis

- [ ] **G-01 Audit log untuk aksi sensitif**
- [ ] **G-02 Test RLS lintas role**
- [ ] **G-03 Test storage privat**
- [ ] **G-04 Backup dan prosedur rollback**
- [ ] **G-05 End-to-end test**
- [ ] **G-06 Pilot dengan ujian nyata**
- [ ] **G-07 Panduan admin/guru/operator**
- [ ] **G-08 Persetujuan rilis**

## Definition of Ready untuk issue

Setiap issue harus memiliki:
- tujuan pengguna;
- konteks dan dependensi;
- acceptance criteria yang dapat diuji;
- desain/data contract jika diperlukan;
- dampak keamanan dan RLS;
- definisi selesai.
