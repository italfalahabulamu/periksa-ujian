# Sistem Pemeriksaan Ujian SMP — Dokumentasi Produk

Dokumentasi awal untuk membangun aplikasi pemeriksaan ujian SMP berbasis lembar jawaban hasil pindai/foto, dengan pemeriksaan pilihan ganda berbantuan OMR dan pemeriksaan esai oleh guru menggunakan rubrik digital.

## Prinsip utama

- Mengikuti arsitektur dan pola implementasi HRIS Al-Falah yang sudah ada.
- Teknologi yang sudah terkonfirmasi dari konteks: GitHub, Cloudflare, dan Supabase.
- Framework frontend, struktur repository, strategi deployment, dan konvensi coding **harus diverifikasi dari repository HRIS** sebelum implementasi. Jangan mengasumsikan Next.js, Vite, atau framework lain sebelum audit.
- Pemeriksaan esai dilakukan guru; **tidak menggunakan AI untuk memberi nilai esai**.
- Hasil OMR yang meragukan harus masuk antrean validasi manual, bukan otomatis dianggap salah.
- Data akademik aplikasi ujian dipisahkan dari data HRIS. Integrasi akun/SSO hanya dilakukan jika disetujui dan dirancang secara eksplisit.

## Isi dokumentasi

| File | Isi |
|---|---|
| `01-PRD.md` | Product Requirements Document |
| `02-SCOPE-MVP.md` | Ruang lingkup, prioritas, dan kriteria MVP |
| `03-SITEMAP-USER-FLOW.md` | Sitemap dan alur pengguna |
| `04-UI-WIREFRAME.md` | Wireframe teks untuk dashboard dan halaman utama |
| `05-ARSITEKTUR-TEKNIS.md` | Arsitektur sistem dan keputusan teknologi |
| `06-DATABASE-SCHEMA.md` | Model data dan rancangan skema awal |
| `07-OMR-SPEC.md` | Spesifikasi pemindaian dan pembacaan OMR |
| `08-ROLE-PERMISSION.md` | Peran dan matriks hak akses |
| `09-TEST-PLAN.md` | Strategi pengujian dan acceptance criteria |
| `10-ROADMAP.md` | Tahapan pengembangan |
| `11-OPEN-DECISIONS.md` | Keputusan yang wajib dikonfirmasi |
| `12-IMPLEMENTATION-BACKLOG.md` | Backlog awal yang bisa dijadikan issue GitHub |

## Status dokumen

Dokumen ini adalah **baseline PRD dan rancangan awal**, belum dianggap spesifikasi final untuk produksi. Beberapa keputusan teknis—khususnya framework HRIS, format lembar jawaban, metode pemindaian, dan kebijakan penilaian—harus dikonfirmasi sebelum coding.

## Cara menggunakan

1. Audit repository HRIS dan catat framework, pola routing, UI components, autentikasi, konfigurasi Cloudflare, dan Supabase.
2. Lengkapi `11-OPEN-DECISIONS.md`.
3. Sepakati `01-PRD.md` dan `02-SCOPE-MVP.md`.
4. Pecah backlog di `12-IMPLEMENTATION-BACKLOG.md` menjadi GitHub Issues.
5. Implementasikan secara bertahap; jangan langsung mengaktifkan penilaian massal sebelum pilot OMR lolos uji.
