# Status Proyek: pemeriksa-ujian

Dibuat: 2026-11-01
Mode: A  (A = dari nol, B = duplikasi, C = perbaiki/tingkatkan)
Fase saat ini: 1 - Riset & Bisnis (menunggu Gerbang 1)
Gerbang terakhir lolos: belum ada

## Ide inti
Aplikasi mobile untuk sekolah: (A) Koreksi Jawaban (pilihan ganda via foto LJK + isian singkat) dan (B) Telaah Soal (kunci, analisis butir). Stack: mobile + backend + Supabase. Nama proyek sementara: pemeriksa-ujian.

## Keputusan
- Mode A (dari nol).
- Gerbang 1 (user, 2026-11-01): pengguna awal = sekolah; LJK = template buatan aplikasi; harga = gratis.
- Cakupan MVP: pilihan ganda + isian singkat; esai dan tulisan tangan ditunda.

## Asumsi yang belum dikonfirmasi
- Target akurasi pindai (usulan di spike-01): salah baca tak ditandai <= 0,5%, ragu <= 5%.
- Platform pertama Android; iOS ditunda.
- Batas Supabase Free berasal dari sumber pihak ketiga, belum dicek ke halaman resmi.
- Siapa yang menanggung biaya jangka panjang (harga gratis) belum dijawab user.

## Versi kontrak
belum dibekukan

## Bug/temuan terbuka
QA: P0=0 P1=0 P2=0 | Security: Critical=0 High=0

## Putaran rework aktif
-

## Langkah berikutnya
- Gerbang 1: user menyetujui ringkasan Fase 1, lalu jalankan spike-01 (docs/11-rnd/spikes/) dan mulai Fase 2 (PM -> PRD).
- Dokumen Fase 1: docs/11-rnd/findings.md, docs/12-finance/opex-model.md, docs/13-business/business-brief.md
