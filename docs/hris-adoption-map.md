# Peta adopsi HRIS Al-Falah (lewat FTS) → periksa-ujian

Sumber pola: HRIS Al-Falah (`dataku2026`) dan **FTS** (`italfalahabulamu/FTS`), aplikasi pendaftaran FITAS 2026
yang sudah diturunkan dari HRIS dan menjadi acuan struktur repo ini. Dokumen ini daftar kerja untuk fase
Foundation; **belum ada kode yang disalin** ke repo ini. Setiap butir disalin dengan adaptasi, bukan apa adanya.

Audit repository HRIS langsung (A-01 di `docs/prd/12-IMPLEMENTATION-BACKLOG.md`) tetap perlu dilakukan.
Sampai itu selesai, butir di bawah adalah **usulan** yang berasal dari FTS, bukan fakta tentang HRIS.

## Diadopsi (usulan)

| # | Sumber (FTS/HRIS) | Target periksa-ujian | Adaptasi | Fase |
|---|---|---|---|---|
| 1 | `scripts/build.js` | `scripts/build.js` | Hanya suntik `SUPABASE_URL`/`SUPABASE_ANON_KEY`; gagal keras bila kosong; tolak kunci ber-role `service_role` | Foundation |
| 2 | `wrangler.jsonc` | `wrangler.jsonc` | Ganti nama project; `assets.directory = "dist"` | Foundation |
| 3 | `public/_headers` | `public/_headers` | CSP hanya untuk domain yang dipakai; tambahkan kebutuhan viewer scan/PDF bila perlu | Foundation |
| 4 | Trigger proteksi role/status dan penanganan user baru | migrasi auth | Role default terendah; role hanya diubah admin; tidak dari metadata signup | Foundation |
| 5 | Trigger `audit_logs` | migrasi audit | Catat aksi sensitif sesuai FR-13 (ubah kunci, koreksi OMR, nilai esai, finalisasi, reopen) | Foundation |
| 6 | Pola fungsi helper RLS (`security definer`) | migrasi RLS | Tambah `set search_path = public, pg_temp`; peran: admin akademik, guru, pemeriksa, pimpinan, operator scan | Foundation |
| 7 | Edge Function pembuatan akun staf dan reset sandi | `supabase/functions/` | Admin membuat akun guru/pemeriksa dan mereset sandi (Supabase Free tanpa email) | Foundation |
| 8 | `public/sw.js`, `manifest`, registrasi service worker | sama | App-shell saja; **tidak meng-cache scan atau data**; naikkan versi cache tiap deploy | Foundation |
| 9 | `public/js/idle-timeout.js`, util escape HTML | sama | Ambil yang generik saja; data siswa sensitif, waktu idle ditetapkan dengan pimpinan | Foundation |
| 10 | Tes penjaga `no_inline_event_handlers`, CSP connect-src | `tests/` | Sesuaikan ke struktur repo ini | Foundation |
| 11 | `.github/workflows` (tes, tes database, deploy Supabase) | `.github/workflows/` | Lint, test, test:db; job staging aktif bila secret ada | Foundation |
| 12 | Tes database ke Postgres sungguhan (`scripts/test-db.sh`) | `scripts/` | Wajib untuk RLS, transisi status, perhitungan nilai | Foundation |
| 13 | Impor CSV (`public/js/lib/csv.js`) dan ekspor (`export-xlsx.js`) | `public/js/lib/` | Impor siswa/kelas dengan preview dan validasi (B-04); ekspor CSV dulu, XLSX di P1 | Akademik |
| 14 | Kompresi gambar (`image-compress.js`), unggah berkas (`proof-uploader.js`) | `public/js/lib/` | Pola validasi tipe/ukuran; **jangan** mengompres scan OMR yang menjadi bukti asli | Upload |
| 15 | `.github/workflows/keepalive.yml` | sama | Mencegah proyek Supabase Free dijeda setelah 1 minggu idle | Foundation |
| 16 | `src/vendor/pdf.js` + `pdf.worker.js` | sama | Render PDF scan di Web Worker; batasi halaman/dimensi; lisensi vendor dicatat di `THIRD_PARTY.md` | Upload |
| 17 | `src/vendor/jsqr.js` | sama | Hanya untuk tahap QR per siswa (P1, D-07) | P1 |
| 18 | `public/js/lib/backup.js` (cadangan zip) | sama | Cadangan data hasil/audit sebelum rilis dan latihan restore | Rilis |
| 19 | `scripts/test-db.sh`, `scripts/check-live.mjs` | `scripts/` | Harness tes Postgres sungguhan; pemeriksaan kesehatan sebelum hari ujian | Foundation |

## Tidak diadopsi

- `public/js/app.js` monolit HRIS dan modul HRIS: cuti, penggajian, kinerja, bagan organisasi, DMS, absensi.
- `mockDataService.js`; tes memakai Postgres sungguhan.
- Modul FTS: katalog lomba, kontingen, order, pembayaran, QR/check-in, kartu peserta, pengumuman, laporan keuangan.
- Ratusan migrasi HRIS/FTS: yang dipakai adalah **pola penulisannya** (nomor, header keputusan, perbaikan lewat migrasi baru).
- Notifikasi push dan sinkronisasi luring.

## Yang tidak ada di HRIS/FTS dan harus dirancang baru

- Pemrosesan OMR (alignment, deteksi bubble, status respons) dan runtime-nya; ditentukan lewat prototipe (ADR-0002).
- Penyimpanan dan penayangan scan privat dengan izin berbasis penugasan guru/ujian.
- Versi kunci/rubrik, snapshot formula, finalisasi dan reopen terkendali.
- Viewer scan berdampingan (zoom, rotate, antar-halaman) untuk validasi OMR dan penilaian esai.

## Pelajaran dari HRIS/FTS yang jadi aturan di `AGENTS.md`

1. Role tidak boleh diambil dari metadata signup.
2. Fungsi `security definer` wajib `set search_path`.
3. RLS harus diuji ke Postgres sungguhan; lulus tes mock bukan bukti.
4. Naikkan versi cache service worker tiap deploy.
5. Tambah header CSP hanya untuk domain yang dipakai; fitur bisa gagal diam-diam karena CSP.
6. Atribusi aktor diisi trigger, bukan klien.
