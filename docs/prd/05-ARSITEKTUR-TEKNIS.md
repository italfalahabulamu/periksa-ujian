# Arsitektur Teknis

## 1. Prinsip keputusan

Aplikasi mengikuti arsitektur dan konvensi HRIS yang sudah ada agar tim tidak memelihara dua pola teknis berbeda. Stack yang terkonfirmasi dari konteks adalah GitHub, Cloudflare, dan Supabase. Framework frontend, pipeline deployment, dan detail runtime harus dikonfirmasi dengan audit repository.

**Jangan mulai dengan mengganti framework HRIS atau membuat pola autentikasi baru tanpa alasan yang terdokumentasi.**

## 2. Arsitektur konseptual

```text
Browser
  │
  ▼
Frontend (framework/pola mengikuti repository HRIS)
  │
  ├── Supabase Auth (sesuai konfigurasi HRIS)
  │
  ├── Supabase Database / PostgreSQL
  │      ├── Data akademik dan ujian
  │      ├── Kunci/rubrik versi
  │      ├── Respons, skor, hasil
  │      └── Audit trail
  │
  ├── Supabase Storage (bucket privat untuk scan)
  │
  └── Worker pemrosesan OMR
         ├── Validasi dan normalisasi gambar
         ├── Deteksi template / alignment
         ├── Deteksi tanda
         ├── Confidence dan status ambigu
         └── Simpan hasil sementara ke database
```

## 3. Komponen

### 3.1 Frontend
- Gunakan framework, struktur folder, routing, komponen UI, pola form, dan gaya kode dari HRIS.
- Jangan membuat asumsi framework sebelum membaca `package.json`, konfigurasi build, routing, dan workflow CI/CD.
- Semua aksi sensitif harus divalidasi di backend/database, bukan hanya di UI.
- Gunakan pagination/filter untuk tabel yang dapat membesar.

### 3.2 GitHub
- Repository mengikuti konvensi HRIS.
- Gunakan branch/PR sesuai kebiasaan tim.
- Perubahan schema harus disertai migration.
- Secrets hanya melalui konfigurasi secret/environment yang aman, tidak ditulis ke repository.
- CI minimal menjalankan lint, typecheck (jika tersedia), dan test.

### 3.3 Cloudflare
- Gunakan konfigurasi deployment yang selaras dengan HRIS setelah audit.
- Verifikasi apakah HRIS memakai Cloudflare Pages, Workers, atau metode lain.
- Jangan menganggap runtime tertentu dapat menjalankan library OMR native tanpa uji kompatibilitas.
- Pemrosesan OMR dapat memerlukan worker terpisah jika runtime frontend/deployment tidak cocok untuk operasi gambar.

### 3.4 Supabase
- PostgreSQL untuk data relasional.
- Supabase Auth jika sesuai dengan pola HRIS.
- Row Level Security (RLS) untuk semua tabel yang dapat diakses klien.
- Storage untuk file scan dengan bucket privat dan akses terotorisasi.
- Gunakan migration SQL yang dapat direproduksi.
- Service role key tidak boleh berada di browser.

### 3.5 Worker OMR
OMR adalah komponen yang paling membutuhkan prototipe dan pengujian. Pilih runtime/library setelah audit deployment dan percobaan terhadap scan nyata. Worker harus:
- memproses berkas secara idempotent;
- mencatat versi algoritma/template;
- mengembalikan status per lembar dan per nomor;
- tidak mengubah nilai final secara langsung;
- dapat diulang tanpa membuat data duplikat;
- memisahkan kegagalan teknis dari jawaban kosong/ganda.

## 4. Batas data HRIS dan ujian

- Data karyawan HRIS dan data akademik ujian berada pada domain/tabel yang terpisah.
- Jangan memberi akses tabel HRIS kepada aplikasi ujian hanya karena menggunakan project/database yang sama.
- Jika menggunakan Supabase project yang sama, tentukan schema, RLS, dan batas akses secara eksplisit.
- Jika memakai project berbeda, tentukan apakah login bersama benar-benar diperlukan.
- Jangan membuat SSO atau menghubungkan tabel user secara langsung sebelum dampak keamanan dan pemeliharaannya disepakati.

## 5. Keamanan

- RLS aktif untuk setiap tabel yang diakses melalui API klien.
- Hak akses ditetapkan berdasarkan role dan assignment yang sah.
- File scan disimpan privat; gunakan URL bertanda tangan dengan masa berlaku terbatas jika diperlukan.
- Jangan menyimpan data sensitif siswa dalam log aplikasi yang tidak terkontrol.
- Audit trail untuk perubahan kunci, validasi OMR, nilai esai, finalisasi, dan pembukaan ulang.
- Validasi input dan batas ukuran/tipe file pada server.
- Rate limit dan proteksi upload mengikuti kemampuan platform.
- Rahasia dan kredensial hanya melalui environment secrets.

## 6. Alur deployment

1. Audit repository HRIS dan dokumentasikan build/deploy saat ini.
2. Tentukan apakah aplikasi ujian menjadi repository terpisah atau modul dalam monorepo.
3. Buat environment development/staging/production sesuai kemampuan yang ada.
4. Terapkan migration ke staging.
5. Uji RLS dan upload privat.
6. Deploy preview untuk review.
7. Jalankan smoke test.
8. Deploy production setelah approval.
9. Pastikan prosedur rollback dan backup tersedia.

## 7. Audit repository HRIS — checklist

- [ ] Framework dan versi dari `package.json` atau file dependency.
- [ ] Struktur direktori dan konvensi penamaan.
- [ ] Routing dan layout.
- [ ] UI component library dan design tokens.
- [ ] Pola validasi form.
- [ ] Supabase client dan lokasi konfigurasi.
- [ ] Strategi autentikasi/session.
- [ ] RLS dan pola query.
- [ ] File migration.
- [ ] Storage dan upload pattern.
- [ ] Cloudflare product/runtime yang dipakai.
- [ ] GitHub Actions/CI/CD.
- [ ] Environment variables dan secrets.
- [ ] Logging, error handling, dan testing.
- [ ] Konvensi commit, branch, dan pull request.

Hasil audit sebaiknya disimpan sebagai `HRIS-ARCHITECTURE-NOTES.md` sebelum implementasi.
