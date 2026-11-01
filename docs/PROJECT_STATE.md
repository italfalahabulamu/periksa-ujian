# Status Proyek: pemeriksa-ujian

Dibuat: 2026-11-01
Mode: A  (A = dari nol, B = duplikasi, C = perbaiki/tingkatkan)
Fase saat ini: 2 - Produk (PRD draf v0.1 selesai, menunggu Gerbang 2)
Gerbang terakhir lolos: Gerbang 1 (keputusan user 2026-11-01); Gerbang 2 menunggu

## Ide inti
Aplikasi mobile untuk sekolah: (A) Koreksi Jawaban (pilihan ganda via foto LJK + isian singkat) dan (B) Telaah Soal (kunci, analisis butir). Stack: mobile + backend + Supabase. Nama proyek sementara: pemeriksa-ujian.

## Keputusan
- Mode A (dari nol).
- Gerbang 1 (user, 2026-11-01): pengguna awal = sekolah; LJK = template buatan aplikasi; harga = gratis.
- Repo `italfalahabulamu/periksa-ujian` dipakai sebagai tempat simpan. Dokumen proyek lama (SMP pesantren, web JS) dihapus; riwayatnya di tag `archive/pre-reset` (user, 2026-11-01).
- Rilis: R1 = alur utuh pilihan ganda; R2 = isian singkat + Telaah Soal; R3 = offline, saran AI, iOS (usulan PM, menunggu Gerbang 2).
- Cakupan MVP: pilihan ganda + isian singkat; esai dan tulisan tangan ditunda.

## Asumsi yang belum dikonfirmasi
- Target akurasi pindai (usulan di spike-01): salah baca tak ditandai <= 0,5%, ragu <= 5%.
- Platform pertama Android; iOS ditunda.
- Batas Supabase Free berasal dari sumber pihak ketiga, belum dicek ke halaman resmi.
- Siapa yang menanggung biaya jangka panjang (harga gratis) belum dijawab user.
- Spike 01 hanya pada data sintetis; akurasi pada foto nyata belum terbukti (lihat docs/11-rnd/spikes/spike-01-hasil.md).
- Tenggat ujian pertama dan sekolah mitra pilot belum dikonfirmasi (angka ± 18 Nov 2026 hanya dari catatan repo lama).

## Versi kontrak
belum dibekukan

## Bug/temuan terbuka
QA: P0=0 P1=0 P2=0 | Security: Critical=0 High=0

## Putaran rework aktif
-

## Langkah berikutnya
- Gerbang 2: user menjawab pertanyaan terbuka di docs/01-product/PRD.md bagian 9 (terutama isian singkat, tenggat, sekolah mitra, biaya jangka panjang).
- Spike 02 dengan foto nyata (docs/11-rnd/spikes/spike-01-hasil.md bagian akhir) sebelum R1 dikunci.
- Setelah Gerbang 2: Architect (ADR, kontrak openapi.yaml), Desainer, Database.
- Dokumen: docs/11-rnd/, docs/12-finance/, docs/13-business/, docs/01-product/PRD.md
