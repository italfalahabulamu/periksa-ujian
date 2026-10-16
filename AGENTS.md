# AGENTS.md — periksa-ujian (Sistem Pemeriksaan Ujian SMP)

Panduan untuk agent pengembang (Claude Code, Codex, dan sejenisnya) dan manusia yang
bekerja di repo ini. Baca seluruhnya sebelum mengubah apa pun.

## 1. Tentang proyek

Aplikasi web untuk memeriksa ujian SMP Pesantren Modern Al-Falah Abu Lam U dari lembar jawaban hasil
pindai/foto: pilihan ganda dibaca dengan **OMR** (Optical Mark Recognition) berbasis template standar,
esai dinilai **guru secara manual** memakai rubrik digital, lalu nilai dihitung, difinalisasi, dan dilaporkan
dengan jejak audit.

- Pengguna: admin akademik, guru mata pelajaran, pemeriksa, pimpinan, operator pemindaian (opsional).
- Sistem ini **terpisah dari HRIS** pesantren dan dari FTS (pendaftaran FITAS). Pola teknis diadopsi
  sebagian dari HRIS lewat FTS; lihat `docs/hris-adoption-map.md`.
- Data akademik ujian tidak bercampur dengan data HRIS. Integrasi akun/SSO hanya bila disetujui dan
  dirancang eksplisit (keputusan D-03, D-04).

## 2. Lingkup

**Dalam lingkup (MVP, P0):** login dan RBAC, data akademik (tahun ajaran, kelas, siswa, mapel, penugasan
guru), impor CSV, ujian, soal PG + kunci berversi, rubrik esai berversi, template lembar jawaban standar,
unggah PDF/JPG/PNG ke storage privat, antrean pemrosesan, OMR dengan status per respons, validasi manual OMR,
penilaian esai oleh guru, perhitungan nilai, finalisasi dan pembukaan ulang terkendali, audit trail,
laporan dasar dan ekspor CSV.

**Di luar lingkup (jangan dibangun tanpa persetujuan eksplisit):** penilaian esai oleh AI, ujian daring dan
proctoring, pembuatan soal otomatis oleh AI, aplikasi mobile native, OMR layout bebas tanpa template, integrasi
LMS/sistem eksternal, SSO HRIS, bank soal lintas sekolah, rapor, keputusan kenaikan kelas.

Dokumen produk lengkap: `docs/PRD.md` (indeks) dan `docs/prd/` (13 berkas sumber).
Status dan keputusan terkunci: `docs/orchestrator/STATE.md`.

## 3. Stack (diusulkan, final di Gerbang 2 — lihat ADR-0001)

- Frontend: HTML + JavaScript murni (ES modules, **tanpa framework**), responsif; desktop diutamakan untuk
  pemeriksaan massal, tablet harus dapat dipakai. Dipecah per modul, bukan satu file raksasa.
- Backend: Supabase (Postgres, Auth, RLS, RPC/fungsi SQL, Storage privat, Edge Function Deno/TypeScript).
- Hosting: Cloudflare Workers static assets (`wrangler.jsonc`); `scripts/build.js` menyuntik konfigurasi publik.
- Tes: Vitest (unit), tes database terhadap Postgres sungguhan (RLS, RPC, transisi status), E2E. CI: GitHub Actions.
- **Pemrosesan OMR: belum diputuskan.** Library, runtime, dan lokasi eksekusi (browser atau worker terpisah)
  ditentukan setelah prototipe pada scan nyata (ADR-0002, Gerbang 2). Jangan mengasumsikan library native
  berjalan di runtime Cloudflare tanpa uji kompatibilitas.

> Stack ini dipilih mengikuti FTS yang diturunkan dari HRIS. PRD meminta pola HRIS diverifikasi dari
> repository, bukan ditebak; FTS dipakai sebagai sumber verifikasi sampai audit HRIS langsung dilakukan (A-01).

## 4. Struktur repo (target; folder yang belum ada dibuat saat fasenya tiba)

```
AGENTS.md  CLAUDE.md  README.md
docs/
  PRD.md                    indeks dan ringkasan produk
  prd/                      13 berkas PRD sumber (PRD, scope, sitemap, wireframe, arsitektur, DB, OMR, role, tes, roadmap, keputusan, backlog)
  hris-adoption-map.md      bagian HRIS/FTS yang diadopsi dan yang tidak
  data/                     template data dasar (kelas, siswa)
  orchestrator/             STATE.md, handoffs/, adr/
public/                     sumber frontend statis (index.html, js/, css/, _headers, manifest, sw.js)
scripts/                    build.js dan skrip bantu
supabase/
  migrations/               SQL bernomor, satu perubahan logis per file
  functions/                Edge Function
workers/                    pemrosesan OMR bila diputuskan berjalan di luar frontend (opsional)
tests/                      unit, db, e2e, dataset pilot OMR
```

## 5. Perintah

Belum ada sampai fase Foundation selesai. Saat dibuat, perintah standar:
`npm run build`, `npm test`, `npm run test:db`, `npm run test:e2e`. Jangan mengklaim perintah lulus bila
belum dijalankan; sertakan output nyata di laporan.

## 6. Aturan keras

**Integritas nilai**
1. Skor dan nilai disimpan sebagai `numeric` dengan skala jelas, tidak pernah float biner. Aturan pembulatan
   ditetapkan di keputusan D-09 dan diuji.
2. Kunci jawaban, rubrik, bobot, dan formula **dibekukan sebagai versi/snapshot** saat pemeriksaan dimulai.
   Pengaturan global yang berubah tidak boleh mengubah ujian yang sudah berjalan.
3. Nilai final tidak boleh menjadi angka yang bisa ditimpa tanpa histori. Perubahan setelah finalisasi
   memerlukan izin khusus, alasan, dan audit (nilai sebelum dan sesudah).
4. Nilai yang belum lengkap tidak pernah disajikan sebagai final.

**OMR dan esai**
5. Jawaban kosong, ganda, ambigu, atau tidak terbaca **tidak boleh difinalisasi otomatis**; masuk antrean
   validasi manusia. Kebijakan skor kosong/ganda ditetapkan sebagai aturan ujian (D-08), bukan tebakan kode.
6. Ambang confidence berasal dari dataset pilot, bukan angka tebakan. Jangan mempublikasikan klaim akurasi
   OMR sebelum ada hasil uji nyata.
7. Gambar asli scan tidak pernah ditimpa; hasil transformasi adalah artefak turunan. Reprocessing idempoten
   dan tidak menimpa koreksi manual tanpa prosedur eksplisit.
8. **Penilaian esai sepenuhnya oleh guru.** Tidak ada skor esai yang dihasilkan AI. Skor dibatasi 0 sampai
   skor maksimum kriteria oleh constraint database.

**Otoritas ada di database**
9. Logika kritis (transisi status ujian, finalisasi, pembukaan ulang, kunci/versi, validasi skor, perhitungan
   nilai) dijalankan di Postgres: fungsi RPC `security definer` dengan `set search_path = public, pg_temp`,
   constraint, dan trigger. JavaScript klien hanya untuk tampilan.
10. RLS aktif di **semua** tabel yang dapat diakses klien, default-deny. Akses ditentukan role **dan**
    penugasan (guru, kelas, ujian). Setiap tabel baru wajib punya policy dan tes "harus ditolak", termasuk
    akses langsung ke API dan storage, bukan hanya lewat UI.
11. Role tidak pernah berasal dari input klien atau metadata signup. Kolom role/status/identitas dijaga trigger.
12. Kolom aktor (`created_by`, `reviewed_by`, `graded_by`, `finalized_by`, dan sejenisnya) diisi trigger dari
    `auth.uid()`, bukan dari kiriman klien.
13. Transisi status ujian hanya lewat fungsi terpusat (DRAFT → READY → PROCESSING → REVIEW →
    READY_TO_FINALIZE → FINALIZED → REOPENED); transisi tidak sah ditolak. Aksi bersifat idempoten.
14. FK memakai `ON DELETE RESTRICT`; "menghapus" berarti mengubah status. Aksi sensitif (ubah kunci, koreksi
    OMR, nilai esai, finalisasi, reopen) menulis `audit_logs`.

**Rahasia, data siswa, dan keamanan**
15. `service_role` key hanya di Edge Function (secret Supabase), worker, atau skrip lokal lewat environment
    variable. Tidak pernah di frontend, repo, log, atau CI frontend. `build.js` menolak kunci ber-role `service_role`.
16. Bucket Storage scan **privat**. Akses lewat signed URL berumur pendek atau policy setara izin data ujian;
    validasi tipe dan ukuran berkas di sisi server.
17. Data pribadi siswa seminimal mungkin; tidak masuk log, URL, atau pesan error. Scan dan nilai hanya dapat
    dilihat pengguna berwenang (least privilege, D-15).
18. Tanpa inline event handler (`onclick=` dan sejenisnya); CSP ketat tanpa `unsafe-inline` untuk script. Ada
    tes penjaga. Jangan menambah domain CSP tanpa alasan konkret.
19. Service worker hanya meng-cache aset statis, tidak pernah data atau scan. **Naikkan versi cache setiap
    deploy** yang mengubah aset.
20. Endpoint upload wajib dibatasi ukuran/tipe dan dilindungi rate limit sesuai kemampuan platform.

## 7. Cara kerja (orchestrator)

Proyek dijalankan dengan pola fase dan **gerbang konfirmasi** yang sama seperti FTS
(planner → architect → tdd-guide → code-reviewer → security-reviewer → e2e-runner → verification-loop).

- Tidak ada kode produksi sebelum Gerbang 1 (PRD dan lingkup) dan Gerbang 2 (arsitektur) disetujui.
- Siklus per modul: mini-plan → **tes dulu (RED→GREEN→REFACTOR)** → review kode → review keamanan (wajib untuk
  auth, RLS, storage scan, finalisasi nilai, data siswa) → E2E → verifikasi (build, lint, tes, scan secret) →
  laporan modul dengan rekomendasi SHIP / NEEDS WORK / BLOCKED.
- **OMR dikerjakan sebagai prototipe berbatas waktu lebih dulu** dan diuji pada scan nyata; jangan menjanjikan
  akurasi atau tanggal rilis OMR massal sebelum uji (lihat `docs/prd/10-ROADMAP.md`).
- Perbarui `docs/orchestrator/STATE.md` di setiap gerbang. Tulis ADR untuk keputusan arsitektur.
- Konfirmasi dulu sebelum tindakan sulit dibatalkan: dependensi baru, migrasi ke database selain lokal,
  menimpa file, memakai akun eksternal (Supabase, Cloudflare), deploy.
- Cakupan tes: minimal 80% pada logika bisnis; jalur kritis (formula nilai, transisi status, RLS, finalisasi,
  idempotensi OMR) diuji lebih dalam. Definition of Done fitur: lihat `docs/prd/02-SCOPE-MVP.md` §5.
- Jujur soal bukti: jangan menyatakan lulus tanpa output nyata; angka akurasi/kinerja hanya setelah pengujian.

## 8. Konvensi

- Dokumen dan teks antarmuka: Bahasa Indonesia. Kode, nama tabel/kolom/fungsi, commit message: Bahasa Inggris.
- Migrasi: nama berawalan timestamp, satu perubahan logis per file, header berisi keputusan dan asumsi,
  perbaikan lewat migrasi baru (jangan edit migrasi yang sudah dijalankan).
- Satu commit = satu unit kerja jelas; jangan campur perubahan skema dan UI beberapa modul.
- Nama tabel memakai bahasa Inggris, jamak, snake_case (mengikuti `docs/prd/06-DATABASE-SCHEMA.md`).
  Enum status memakai nilai dari PRD.
- Rute di `docs/prd/03-SITEMAP-USER-FLOW.md` bersifat usulan konseptual; penamaan final mengikuti pola FTS/HRIS.

## 9. Jangan salin dari HRIS / FTS

Modul HRIS (cuti, penggajian, kinerja, bagan organisasi, DMS), `app.js` monolit, `mockDataService`, dan
ratusan migrasinya **tidak** dibawa. Dari FTS jangan menyalin modul pendaftaran, order, pembayaran, atau
logika FITAS. Jangan mengambil `role` dari `raw_user_meta_data`, dan jangan menulis fungsi `security definer`
tanpa `set search_path`. Jangan memberi aplikasi ini akses ke tabel HRIS hanya karena database/projectnya sama.

## 10. Definition of Done modul

Tes lulus (output nyata), jalur kritis punya tes keamanan dan idempotensi, RLS punya tes "harus ditolak",
audit trail untuk operasi sensitif ada, state loading/empty/error/permission-denied tersedia, tidak ada
secret/`console.log` tersisa, `STATE.md` dan dokumen terkait diperbarui, laporan modul ditulis.
