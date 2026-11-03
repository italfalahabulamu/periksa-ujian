# PWA Periksa Ujian

Dibangun dari `app/mock/index.html` oleh `build.py`: menyisipkan manifest, service worker (offline), ikon, dan **pembaca foto `omr.js`**. Bila `omr.js` ada, layar Pindai memakai pembaca nyata (kamera `capture`, galeri, tolak foto buruk); tanpa itu (mockup/APK) tetap simulasi.

- Bangun: `python3 app/pwa/build.py <folder_keluar>` lalu sajikan lewat HTTPS (pemasangan PWA dan kamera butuh HTTPS).
- Uji PWA offline: `python3 app/pwa/test_pwa.py <folder>` (8 uji).
- Uji pembaca pada set sintetis: `python3 spikes/omr-01/make_set.py 3 12 /tmp/omrset && python3 app/pwa/test_omr.py /tmp/omrset`.
- Uji ujung ke ujung (LJK cetak aplikasi -> foto sintetis -> unggah lewat UI): `python3 app/pwa/test_scan_e2e.py <folder>` (15 uji).
- `app/mock/test_ui.py` berlaku untuk mockup (simulasi). Pada build PWA tiga uji bagian Pindai sengaja berbeda karena pembaca nyata menggantikan simulasi; jangan dijalankan pada PWA.

## Batas (BELUM TERVERIFIKASI)
Semua uji memakai foto sintetis. Akurasi pada foto nyata, kecepatan di ponsel kelas menengah, dan perilaku kamera di Chrome Android sungguhan belum diuji. Pembacaan berjalan di thread utama (layar bisa terasa tertahan beberapa detik di ponsel lambat). Spike 02 menentukan apakah pembaca dipakai di pilot.
