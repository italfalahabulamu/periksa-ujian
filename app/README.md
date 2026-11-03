# Model aplikasi (mockup) Pemeriksa Ujian

Prototipe yang bisa dipasang di Android untuk **menguji alur**, dengan data tiruan. Bukan produk jadi.

## Yang nyata dan yang disimulasikan
| Nyata | Disimulasikan / belum ada |
|---|---|
| Alur: masuk, kelas, buat ujian, kunci, cetak/lihat LJK, pindai, cek ulang, nilai, rekap | **Pembacaan foto**: hasil pindai dibangkitkan acak dari data tiruan; kamera tidak dipakai |
| Skor bilangan bulat (sen, pembulatan setengah ke atas), kebijakan nilai | Akun/backend/Supabase: semua data hanya di perangkat (localStorage) |
| Ekspor CSV (titik koma, koma desimal, BOM UTF-8, anti formula-injection) | Ekspor di APK = lembar Bagikan (teks), bukan berkas |
| Simpan lokal, cadangan, reset | Cetak LJK dari APK tidak tersedia (pakai versi HTML di peramban) |

## Isi
- `mock/index.html` : aplikasi satu berkas, jalan offline.
- `mock/test_ui.py` : 43 uji Playwright.
- `android-shell/` : cangkang WebView (smali), skrip bangun dan verifikasi.

## Memasang di Android
1. Salin `periksa-ujian-mock.apk` ke ponsel.
2. Izinkan "pasang aplikasi dari sumber tak dikenal" untuk aplikasi berkas/peramban.
3. Buka berkas, pasang. Tanda tangan = kunci debug; Play Protect bisa memberi peringatan.
Alternatif tanpa pasang: buka `mock/index.html` di Chrome.

## Menguji dan membangun
- UI: `python3 app/mock/test_ui.py` (butuh Playwright + Chromium).
- APK: `bash app/android-shell/build_apk.sh <dir-alat> <dir-keluar>` (Apktool 2.10.0, uber-apk-signer 1.3.0, tanpa Android SDK).
- Verifikasi: `bash app/android-shell/verify_shell.sh <apk> <android.jar> <dex2jar> <kerja>`.

## Hasil uji (2026-11-03)
- UI di Chromium: 43 lulus, 0 gagal (skor, klasifikasi, alur, hitung ulang independen vs tabel dan CSV, persistensi, jembatan Android tiruan).
- Statis APK: 31 referensi API cocok dengan android-33, 4 override sah, 3 kelas lolos verifier JVM; tanda tangan v2/v3 dan zipalign valid; aset di APK identik dengan sumber.
- Perilaku native: 24 uji terhadap kelas Android tiruan; uji mutasi menangkap kesalahan yang disuntikkan.

## Batas yang jujur (BELUM TERVERIFIKASI)
- **APK belum pernah dijalankan di perangkat atau emulator nyata**; sesi ini tidak punya SDK/emulator. Perilaku WebView sungguhan, pemilih berkas, dan tombol kembali baru teruji terhadap tiruan.
- Akurasi baca foto nyata belum diketahui (spike 01 hanya sintetis; butuh spike 02).
- Untuk pilot, PWA tetap disarankan (lihat `docs/01-product/pilot-1-pekan.md`), menunggu keputusan pemilik.
