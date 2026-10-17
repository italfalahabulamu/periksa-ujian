# Model ancaman (usulan untuk Gerbang 2)

Aset yang dilindungi: **nilai siswa** (integritas), **scan lembar jawaban** dan data siswa (kerahasiaan; sebagian
besar anak), **kunci jawaban dan soal** (kerahasiaan sebelum ujian), **jejak audit** (keutuhan).
Pelaku: siswa atau wali yang ingin mengubah nilai, staf yang salah/curang, pihak luar, kesalahan operasional.

## 1. Ancaman dan mitigasi

| # | Ancaman | Dampak | Mitigasi | Bukti uji |
|---|---|---|---|---|
| TM-01 | Role dinaikkan lewat metadata signup / tabel `profiles` | Akses nilai/scan seluruh sekolah | Role hanya dari `profiles` diubah admin; trigger penjaga; signup publik dimatikan, akun dibuat admin | T-03, T-17 |
| TM-02 | Fungsi `security definer` tanpa `search_path` | Eskalasi hak lewat objek palsu | Lint CI: tolak fungsi definer tanpa `set search_path` | tes penjaga SQL |
| TM-03 | IDOR: menebak UUID sheet/ujian | Bocor scan/nilai | RLS berbasis penugasan di semua tabel; signed URL hanya setelah `can_view_scan` | T-02, T-08, T-18 |
| TM-04 | Scan dibuka lewat URL publik/hotlink | Bocor data anak | Bucket privat; signed URL ≤ 5 menit; tidak ada URL permanen | T-07, T-09 |
| TM-05 | Staf mengubah jawaban/nilai tanpa jejak | Nilai tak dapat dipercaya | Semua koreksi via RPC → `response_reviews` + `audit_logs` append-only; snapshot hasil; laporan selisih | T-10 |
| TM-06 | Pengukuran OMR dipalsukan klien | Jawaban diubah diam-diam | Akui risiko (ADR-0002): kontrol utama audit + gambar asli + `file_hash` + sampling pemeriksaan ulang | tes + prosedur |
| TM-07 | Lembar tertukar / masuk ujian salah | Nilai salah siswa | Kode peserta bercek-digit, kode ujian, kode halaman; ID tak cocok → review wajib | tes OMR + e2e |
| TM-08 | Unggah berkas berbahaya (PDF berskrip, bom dekompresi) | Eksekusi kode / memori habis | Batas ukuran, jumlah halaman, dimensi piksel; pdf.js dijalankan di Worker tanpa akses DOM; tolak PDF terenkripsi; CSP ketat | tes berkas sengaja rusak |
| TM-09 | Injeksi rumus lewat ekspor CSV/XLSX | Eksekusi rumus di Excel pemakai | Awali sel yang diawali `= + - @` dengan `'` | tes ekspor |
| TM-10 | Kunci/soal bocor sebelum ujian | Ujian gugur | Kunci tidak terbaca pemeriksa/operator; akses kunci hanya admin/guru terkait; audit baca opsional (P1) | T-04 |
| TM-11 | Pengguna berhenti bertugas masih punya akses | Akses tak sah | `is_active=false` menolak semua RPC/RLS; peninjauan penugasan tiap semester | T-16 |
| TM-12 | Sesi terbuka di komputer bersama | Akses oleh orang lain | Idle logout (pola FTS `idle-timeout.js`); waktu ditetapkan dengan pimpinan | e2e |
| TM-13 | Brute force / credential stuffing pada login | Pengambilalihan akun | Rate limit Auth Supabase; sandi kuat; reset oleh admin; tanpa pesan galat yang membocorkan | uji manual + konfigurasi |
| TM-14 | Unggah massal membebani kuota | Layanan terhenti (storage/egress Free) | Batas ukuran per berkas, per batch, per ujian; peringatan kapasitas; purge terjadwal | tes batas |
| TM-15 | Proyek Supabase dijeda saat ujian | Layanan tak tersedia | `keepalive.yml`; cek kesehatan sebelum hari ujian; pertimbangkan Pro | skrip cek |
| TM-16 | Kehilangan data (salah hapus, kerusakan) | Nilai hilang | Tidak ada hard delete; cadangan data berkala (pola `backup.js` FTS); latihan pemulihan sebelum rilis | latihan restore |
| TM-17 | Data pribadi masuk log/URL/pesan galat | Kebocoran data anak | Log pakai ID saja; nama siswa tidak di URL; tes penjaga `console.log`/log | review keamanan |
| TM-18 | Inline script / XSS lewat nama siswa/komentar | Pembajakan sesi | Escape keluaran; CSP tanpa `unsafe-inline`; tes penjaga handler inline | tes penjaga |
| TM-19 | Nilai dibaca pihak tak berhak lewat laporan/filter | Kebocoran lintas cakupan | Filter laporan ditegakkan di server (RLS), bukan di klien | AC-07 |
| TM-20 | Rahasia (service_role, token) bocor ke repo/chat | Pengambilalihan proyek | Hanya env/secret platform; `build.js` menolak `service_role`; scan secret di CI; token yang tampil di chat harus dicabut | CI |

## 2. Risiko sisa yang diterima secara sadar

- TM-06 (klien palsu) dan staf berwenang yang sah menyalahgunakan hak: dikendalikan dengan audit dan pemisahan
  tugas (finalisasi memerlukan izin khusus), bukan dicegah sepenuhnya.
- Perangkat operator yang terinfeksi malware: di luar kendali aplikasi; mitigasi lewat SOP perangkat.
- Foto ponsel (bila didukung nanti) menambah variasi dan risiko salah baca; hanya diaktifkan setelah gate terpisah lulus.

## 3. Pemeriksaan wajib sebelum pilot data nyata

1. Seluruh tes T-01..T-20 lulus pada Postgres sungguhan.
2. Telaah keamanan independen untuk RLS, Storage, finalisasi, dan unggah berkas.
3. Latihan pemulihan dari cadangan.
4. Telaah hukum dan keputusan persetujuan wali (D-17).
