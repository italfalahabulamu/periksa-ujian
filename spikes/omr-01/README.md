# Spike 01 (sekali pakai): pembacaan LJK dari foto, data sintetis

Kode prototipe untuk menjawab pertanyaan di `docs/11-rnd/spikes/spike-01-omr-akurasi.md`. **Bukan fondasi produksi**
(aturan Mode A: spike dibuang setelah dipakai belajar, kecuali Technical Lead menyetujui).

- `synth.py`: template LJK (A4, 40 soal, A-E, 4 marka sudut dengan TL lebih besar), pembuat tanda (kuat, sedang, tipis,
  sebagian, bekas hapusan), dan simulasi foto ponsel (perspektif, rotasi, 180 derajat, cahaya tidak rata, bayangan, blur, noise, JPEG).
- `reader.py`: deteksi marka, homografi, rasio isi per bulatan, klasifikasi per soal, gerbang kualitas.
- `run_spike.py`: evaluasi. Contoh: `python3 run_spike.py 2 40 out --samples`.
- `out/`: hasil mentah dan 3 contoh foto kecil. Hasil dan tafsirnya ada di `docs/11-rnd/spikes/spike-01-hasil.md`.

Dependensi: Python 3, numpy, opencv (cv2).
