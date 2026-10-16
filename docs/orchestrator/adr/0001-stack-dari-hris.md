# ADR 0001: Stack periksa-ujian mengikuti pola HRIS/FTS (Supabase + JavaScript statis + Cloudflare)

- Status: **diusulkan** (final di Gerbang 2)
- Tanggal: 2026-10-17

## Konteks

PRD (`docs/prd/05-ARSITEKTUR-TEKNIS.md`) meminta aplikasi mengikuti arsitektur HRIS yang sudah ada, dengan
stack terkonfirmasi GitHub, Cloudflare, dan Supabase, dan **melarang menebak framework** sebelum repository
diaudit. FTS (`italfalahabulamu/FTS`) adalah aplikasi turunan HRIS yang sudah dibangun dan dipakai: HTML +
JavaScript murni (ES modules, tanpa framework), Supabase (Postgres, Auth, RLS, RPC, Storage, Edge Function),
Cloudflare Workers static assets, Vitest, tes database ke Postgres sungguhan, dan GitHub Actions. Pemilik
proyek meminta struktur awal repo ini mengikuti FTS.

## Opsi yang dipertimbangkan

1. **Pola FTS/HRIS: JavaScript statis + Supabase + Cloudflare Workers assets.**
   - (+) Sudah terbukti di institusi yang sama; build, header keamanan, pola RLS, dan pola tes sudah ada;
     satu pola teknis untuk dipelihara tim.
   - (−) Logika kritis harus ditulis sebagai SQL/PLpgSQL; tanpa framework butuh disiplin modul; viewer scan
     dan antarmuka validasi yang kaya perlu dibangun sendiri; Supabase Free punya batas dan tanpa email.
2. **Framework frontend baru (React/Svelte/dll).**
   - (+) Ekosistem komponen untuk viewer gambar dan tabel besar.
   - (−) Menambah pola teknis kedua; bertentangan dengan prinsip PRD untuk mengikuti HRIS; tanpa alasan
     terdokumentasi yang kuat saat ini.

## Keputusan (usulan)

Memakai opsi 1. Otoritas bisnis tetap di sisi server: **database adalah backend** (RPC `security definer`,
constraint, trigger, RLS). JavaScript klien mengurus tampilan. Frontend dipecah per modul ES.

**Di luar keputusan ini:** runtime dan library OMR. Itu diputuskan di ADR-0002 setelah prototipe pada scan
nyata, karena Cloudflare Workers belum tentu cocok untuk pemrosesan gambar berat dan pilihan (di browser,
worker terpisah, atau layanan lain) harus berdasar uji.

## Konsekuensi

- Positif: konsisten dengan HRIS/FTS; cepat memulai; aset dan tes penjaga dapat diadopsi.
- Negatif: kualitas bergantung pada tes database; risiko kebocoran data nilai/scan bila RLS atau policy
  storage salah. Mitigasi: tes "harus ditolak" per tabel dan per bucket, termasuk akses langsung ke API.
- Dipantau: batas Supabase Free (basis data, penyimpanan scan, egress) — scan menambah beban penyimpanan
  dan perlu dihitung dari D-12 dan D-14 sebelum rilis; periksa dokumentasi terbaru.
- Jalan keluar: bila beban melampaui Supabase Free, naik paket tanpa mengubah kode; bila pemrosesan OMR tidak
  cocok di runtime ini, pindahkan ke worker terpisah tanpa mengubah kontrak data.
- Syarat penutupan: audit repository HRIS langsung (A-01) tidak menemukan bukti yang bertentangan.
