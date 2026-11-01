# PRD: periksa-ujian (draf v0.1)

Status: **usulan, menunggu Gerbang 2**. Mode A. Masukan: `docs/11-rnd/findings.md`, `docs/11-rnd/spikes/spike-01-hasil.md`,
`docs/12-finance/opex-model.md`, `docs/13-business/business-brief.md`, keputusan Gerbang 1 (sekolah, template dari aplikasi, gratis).

## 1. Masalah dan pengguna
Guru sekolah mengoreksi ujian pilihan ganda dan isian singkat secara manual: lama, rawan salah hitung, dan hasilnya jarang dipakai
untuk memperbaiki soal. Cara sekarang (asumsi, belum diwawancara): koreksi dengan kunci di kertas, spreadsheet, atau pemindai LJK gratis
yang sudah ada. Aplikasi ini memeriksa jawaban dari foto lembar jawaban (LJK) dan memberi tahu soal mana yang bermasalah, gratis untuk sekolah.

## 2. Persona
| Persona | Tujuan | Kekhawatiran |
|---|---|---|
| **Guru mata pelajaran** (pengguna utama) | Koreksi cepat satu kelas, nilai tepat, tahu soal yang buruk | Salah baca diam-diam, foto ditolak berulang, aplikasi rumit |
| **Admin sekolah / operator** | Kelola kelas dan siswa, ekspor nilai ke rapor | Data siswa bocor, salah impor |
| **Kepala sekolah / wali kelas** (pembaca) | Melihat rekap per kelas | Angka tidak bisa dipercaya |
Siswa dan orang tua tidak memakai aplikasi pada rilis ini.

## 3. Rilis
| Rilis | Isi | Alasan urutan |
|---|---|---|
| **R1 (MVP)** | Satu alur utuh pilihan ganda: data kelas, buat ujian, cetak LJK, foto, cek ulang, nilai, ekspor | Risiko terbesar (pembacaan foto) harus terbukti lebih dulu |
| **R2** | Isian singkat dan Telaah Soal | Telaah soal butuh hasil ujian nyata dari R1 |
| **R3** | Penyempurnaan (offline, saran AI, iOS) | Bergantung data pakai |

## 4. Peta fitur
Prioritas MoSCoW untuk rilis yang tertulis. Must hanya yang membuat produk tidak bermakna tanpanya.

| ID | Domain | Fitur | Prioritas | Rilis | Bergantung pada |
|---|---|---|---|---|---|
| F-AKUN-01 | Akun | Masuk guru/admin dengan email dan sandi | Must | R1 | |
| F-DATA-01 | Data | Kelas dan daftar siswa (impor CSV), kode peserta | Must | R1 | F-AKUN-01 |
| F-DATA-02 | Data | Privasi siswa: minimalisasi data, retensi foto, akses terbatas | Must | R1 | F-DATA-01 |
| F-UJI-01 | Ujian | Buat ujian pilihan ganda dan kunci jawaban | Must | R1 | F-DATA-01 |
| F-UJI-03 | Ujian | Bobot dan kebijakan nilai (kosong, ganda) per ujian | Must | R1 | F-UJI-01 |
| F-UJI-04 | Ujian | Hasilkan LJK PDF dari template aplikasi | Must | R1 | F-UJI-01 |
| F-UJI-05 | Ujian | Kunci dibekukan sebagai versi saat pemeriksaan mulai | Should | R1 | F-UJI-01 |
| F-LJK-01 | Koreksi | Foto LJK dengan panduan bingkai dan cek mutu di kamera | Must | R1 | F-UJI-04 |
| F-LJK-02 | Koreksi | Baca jawaban per soal dengan status (terdeteksi, kosong, ganda, ragu) | Must | R1 | F-LJK-01 |
| F-LJK-03 | Koreksi | Antrean cek ulang: guru memutuskan soal ragu/ganda dengan satu ketukan | Must | R1 | F-LJK-02 |
| F-LJK-04 | Koreksi | Tolak foto yang tidak terbaca dengan alasan dan minta foto ulang | Must | R1 | F-LJK-01 |
| F-LJK-05 | Koreksi | Kenali lembar dan peserta dari kode pada LJK | Must | R1 | F-DATA-01 |
| F-NIL-01 | Nilai | Hitung skor dan rekap per siswa dan per kelas | Must | R1 | F-LJK-03, F-UJI-03 |
| F-NIL-02 | Nilai | Ekspor CSV/XLSX | Must | R1 | F-NIL-01 |
| F-NIL-03 | Nilai | Koreksi manual nilai dengan alasan dan jejak audit | Should | R1 | F-NIL-01 |
| F-ISI-01 | Isian | Soal isian dengan daftar jawaban yang diterima | Should | R2 | F-UJI-01 |
| F-ISI-02 | Isian | Masukkan jawaban isian siswa dan nilai otomatis (normalisasi teks) | Should | R2 | F-ISI-01 |
| F-ISI-03 | Isian | Guru menimpa penilaian isian dengan alasan | Should | R2 | F-ISI-02 |
| F-TEL-01 | Telaah | Analisis butir: tingkat kesulitan, daya beda, efektivitas pengecoh | Should | R2 | F-NIL-01 |
| F-TEL-02 | Telaah | Pemeriksaan kunci dan soal sebelum ujian (aturan, bukan AI) | Should | R2 | F-UJI-01 |
| F-TEL-03 | Telaah | Saran AI untuk soal ambigu, berkuota, hanya saran | Could | R3 | F-TEL-02 |
| F-OFF-01 | Umum | Antrean unggah saat tidak ada sinyal | Could | R3 | F-LJK-02 |
| F-PLT-01 | Umum | iOS | Won't | R3+ | |

Hitungan: 13 Must dari 23 fitur (57%) bila seluruh rilis dihitung bersama; per rilis, R1 memang hampir semuanya Must karena alurnya harus utuh.
Fitur yang tampak sama dicek: F-LJK-03 (cek ulang soal ragu) dan F-NIL-03 (koreksi nilai setelah final) sengaja terpisah: yang pertama sebelum nilai
dihitung, yang kedua sesudah.

## 5. Cerita pengguna dan kriteria penerimaan (fitur Must)

**F-AKUN-01** Sebagai guru saya ingin masuk agar data saya terlindungi.
- Given akun valid, When masuk, Then melihat daftar ujian milik saya saja.
- Kasus gagal: sandi salah lima kali berturut-turut, Then percobaan berikutnya tertunda dan tidak ada petunjuk akun ada atau tidak.

**F-DATA-01** Sebagai admin saya ingin mengimpor kelas dan siswa dari CSV.
- Given CSV valid (kode peserta unik, nama, kelas), When impor, Then jumlah baris diterima dan ditolak ditampilkan beserta alasan.
- Kasus gagal: kode peserta ganda atau kolom hilang, Then tidak ada baris yang masuk sebagian tanpa ringkasan; berkas ditolak atau baris bermasalah dilewati dengan daftar jelas.

**F-DATA-02** Sebagai admin saya ingin data siswa seminimal mungkin agar kewajiban pelindungan data terpenuhi.
- Given siswa tersimpan, Then yang disimpan hanya kode peserta, nama, kelas; tidak ada data lain.
- Given foto LJK, When melewati masa simpan yang diatur sekolah, Then foto dihapus otomatis dan nilai tetap ada.
- Given guru lain di sekolah yang sama, When membuka ujian bukan miliknya, Then ditolak (diuji langsung ke API, bukan hanya lewat layar).
- Kasus gagal: gangguan keamanan terdeteksi, Then ada prosedur pemberitahuan tertulis 3x24 jam (UU PDP Pasal 46, perlu konfirmasi hukum).

**F-UJI-01** Sebagai guru saya ingin membuat ujian dan kunci agar bisa dikoreksi.
- Given jumlah soal 1-40 dan opsi A-E, When menyimpan, Then ujian tercatat dan kunci bisa dilihat ulang.
- Kasus gagal: soal tanpa kunci, Then ujian tidak bisa dicetak atau dikoreksi.

**F-UJI-03** Sebagai guru saya ingin aturan nilai jelas.
- Given kebijakan kosong = 0, ganda = ditandai cek ulang, tanpa nilai negatif, When ujian dibuat, Then aturan tampil dan tersimpan di ujian itu.
- Kasus gagal: bobot total nol atau negatif ditolak.

**F-UJI-04** Sebagai guru saya ingin mencetak LJK dari aplikasi.
- Given ujian valid, When membuat LJK, Then PDF A4 berisi marka sudut, bulatan jawaban, dan kode lembar/peserta yang bisa dibaca pembaca yang sama.
- Kasus gagal: dicetak di skala tidak 100%, Then pembaca tetap bisa membaca karena memakai marka (diuji), atau memberi tahu bila tidak bisa.

**F-LJK-01** Sebagai guru saya ingin memotret LJK dengan panduan agar fotonya layak.
- Given kamera terbuka, When LJK masuk bingkai dengan keempat marka terlihat, Then aplikasi memberi tanda siap dan mengambil foto.
- Kasus gagal: gelap, kabur, atau marka terpotong, Then pesan spesifik dan foto tidak diambil.

**F-LJK-02** Sebagai guru saya ingin jawaban terbaca otomatis dengan status per soal.
- Given foto layak, When diproses, Then tiap soal berstatus terdeteksi, kosong, ganda, atau ragu.
- Target mutu (usulan, harus dibuktikan pada foto nyata): salah baca tak ditandai ≤ 0,5% soal; ragu pada soal bersih ≤ 5%.
- Kasus gagal: jawaban pasti salah **tidak boleh** muncul tanpa tanda; diukur di spike 02 dan pilot.

**F-LJK-03** Sebagai guru saya ingin memutuskan soal yang ragu dengan cepat.
- Given soal ragu/ganda, When saya membuka antrean, Then melihat potongan gambar soal itu dan memilih jawaban atau kosong dengan satu ketukan.
- Kasus gagal: nilai tidak bisa difinalkan selama masih ada soal ragu.

**F-LJK-04** Sebagai guru saya ingin foto buruk ditolak dengan alasan jelas.
- Given marka tidak ditemukan atau tidak konsisten, When diproses, Then lembar ditandai "foto ulang" dan tidak dibaca sama sekali.

**F-LJK-05** Sebagai guru saya ingin lembar dikenali otomatis agar tidak tertukar.
- Given kode peserta terbaca valid, Then lembar terhubung ke siswa tersebut.
- Kasus gagal: kode tidak terbaca atau ganda, Then guru memilih siswa manual; dua lembar dengan peserta sama ditandai konflik.
- Catatan: pergeseran satu bulatan harus terdeteksi lewat fitur non-periodik (kode lembar) karena grid bulatan periodik (lihat hasil spike 01).

**F-NIL-01** Sebagai guru saya ingin skor dan rekap otomatis.
- Given semua soal sudah diputuskan, Then skor dihitung sesuai kebijakan F-UJI-03 dan rekap per kelas tersedia.
- Kasus gagal: nilai yang belum lengkap tidak ditampilkan sebagai final.

**F-NIL-02** Sebagai admin saya ingin mengekspor nilai.
- Given rekap final, When ekspor, Then berkas CSV/XLSX terbuka benar di Excel berlokal Indonesia dan tidak mengeksekusi rumus dari teks nama.

## 6. Di luar cakupan (rilis ini)
Esai dan tulisan tangan (OCR), siswa atau orang tua login, ujian daring/proctoring, aplikasi iOS, integrasi LMS/rapor, pembuatan soal otomatis oleh AI,
LJK format bebas dari institusi (diputuskan: hanya template aplikasi).

## 7. Metrik keberhasilan (target angka ditetapkan setelah pilot)
| Metrik | Definisi | Sumber |
|---|---|---|
| Aktivasi | Guru yang menyelesaikan satu ujian sampai rekap tanpa bantuan pengembang | Log + survei |
| Akurasi baca | Persen soal salah tak ditandai; persen soal bersih yang diragukan | Hasil cek ulang guru dan uji foto nyata |
| Waktu koreksi | Menit per kelas dibanding cara lama | Survei guru (baseline diukur di pilot) |
| Foto ditolak | Persen foto yang harus diulang | Log |
Pemakaian Telaah Soal (R2): persen ujian yang analisisnya dibuka.

## 8. Non-fungsional
- Bahasa antarmuka Bahasa Indonesia. Android dahulu; versi minimum dan kamera minimum **belum ditetapkan**, diukur di spike 02.
- Pembacaan butuh waktu yang wajar; belum ada target waktu (spike 01 hanya mengukur di Python, bukan ponsel). Target ditetapkan setelah pilihan perangkat/server.
- Koneksi: R1 butuh internet untuk menyimpan hasil; antrean offline di R3.
- Keamanan: RLS di semua tabel, bucket foto privat, tidak ada data siswa di log atau URL, `service_role` tidak di aplikasi klien, backup (Free tidak mencantumkan cadangan harian; dirancang DevOps).
- Biaya: bertahan di batas gratis untuk pilot; batas pemakaian per guru agar biaya tidak tak terbatas (lihat opex-model).

## 9. Risiko dan pertanyaan terbuka
| # | Pertanyaan/risiko | Siapa yang bisa menjawab |
|---|---|---|
| 1 | **Isian singkat bagaimana dimasukkan?** Tanpa OCR tulisan tangan, pilihan: (a) guru mengetik jawaban siswa di layar cepat lalu dinilai otomatis, atau (b) jawaban angka lewat grid bulatan di LJK. Rekomendasi: (a) untuk R2, (b) bila jawaban hanya angka | User (Gerbang 2) |
| 2 | **Tenggat dan distribusi.** Bila ujian pertama masih sebelum ± 18 November 2026 (angka dari catatan repo lama, belum dikonfirmasi), uji tertutup Google Play (12 penguji x 14 hari berturut-turut) tidak muat; opsi distribusi APK langsung | User |
| 3 | Sekolah mitra pilot siapa, dan berapa guru/ujian? | User |
| 4 | Siapa pengendali data (sekolah atau kita) dan cara persetujuan orang tua | Penasihat hukum |
| 5 | Lama simpan foto LJK (usulan 30 hari setelah final, keputusan sekolah) | Sekolah + hukum |
| 6 | Akurasi pada foto nyata belum terbukti; spike 02 wajib sebelum R1 dikunci | R&D |
| 7 | Siapa menanggung biaya jangka panjang dan tujuan akhirnya (gratis) | User |
| 8 | Jumlah soal tipikal per ujian (spike memakai 40 soal, A-E) | Guru mitra |
| 9 | Proyek Supabase Free dijeda 7 hari tanpa aktivitas; perlu aktivitas terjadwal atau Pro menjelang ujian | DevOps |

## 10. Asumsi (belum dikonfirmasi)
Android lebih dulu; guru memakai ponselnya sendiri; hampir semua LJK dicetak oleh sekolah dari PDF aplikasi; satu template A4 dengan 40 soal dan opsi A-E cukup
untuk R1; angka kebijakan nilai (kosong = 0, tanpa nilai negatif) sesuai keinginan guru; ambang analisis butir dari studi pendidikan kedokteran perlu disetujui
guru atau ahli evaluasi pendidikan sebelum dipakai di sekolah.
