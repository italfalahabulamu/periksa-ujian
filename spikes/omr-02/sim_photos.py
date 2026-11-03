"""SIMULASI saja: isi LJK kit sesuai kunci.csv dan buat 'foto' sintetis bernama sesuai konvensi lapangan.
Dipakai hanya untuk menguji alat evaluasi sebelum foto nyata ada. Pemakaian: python3 sim_photos.py <kit> <jumlah_lembar> <folder_foto>"""
import csv, sys
from pathlib import Path
import cv2, numpy as np
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "omr-01"))
import synth
from make_kit import blank_with_number
kit, n, out = Path(sys.argv[1]), int(sys.argv[2]), Path(sys.argv[3]); out.mkdir(parents=True, exist_ok=True)
rows = list(csv.DictReader(open(kit / "kunci.csv"))); rng = np.random.default_rng(99); blank = synth.render_blank()
for i in range(1, n + 1):
    img = blank_with_number(blank, i)
    for r in (x for x in rows if int(x["lembar"]) == i):
        q, k = int(r["soal"]) - 1, r["jenis"]; a = "ABCDE".find(r["jawaban_akhir"]); b = "ABCDE".find(r["opsi_lain"])
        if k == "clean": synth.draw_mark(img, q, a, str(rng.choice(["strong", "medium"])), rng)
        elif k == "double": synth.draw_mark(img, q, a, "strong", rng); synth.draw_mark(img, q, b, "strong", rng)
        elif k == "faint": synth.draw_mark(img, q, a, "faint", rng)
        elif k == "erase": synth.draw_mark(img, q, b, "ghost", rng); synth.draw_mark(img, q, a, "strong", rng)
    for ph, cond in (("ponselX", "A_mudah"), ("ponselY", "B_sedang")):
        for kond, c in (("baik", cond), ("sulit", "C_berat")):
            photo, _ = synth.photo(img, c, rng); cv2.imwrite(str(out / f"lembar-{i:02d}_{ph}_{kond}.jpg"), photo, [cv2.IMWRITE_JPEG_QUALITY, 85])
print("foto simulasi ->", out)
