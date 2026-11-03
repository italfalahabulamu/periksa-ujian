"""Buat set foto sintetis + kebenaran dasar + keluaran reader.py (untuk uji paritas pembaca JS).
Pemakaian: python3 make_set.py <seed> <lembar_per_kondisi> <folder_keluar>"""
import json, sys
from pathlib import Path
import cv2, numpy as np
import synth
from reader import read_sheet
seed, n, out = int(sys.argv[1]), int(sys.argv[2]), Path(sys.argv[3]); out.mkdir(parents=True, exist_ok=True)
blank = synth.render_blank(); rng = np.random.default_rng(seed); meta = []
for cond in synth.COND:
    for i in range(n):
        sheet, truth = synth.make_sheet(blank, rng)
        img, _ = synth.photo(sheet, cond, rng)
        name = f"{cond}_{i:02d}.jpg"; cv2.imwrite(str(out / name), img, [cv2.IMWRITE_JPEG_QUALITY, 90])
        r = read_sheet(img)
        meta.append({"file": name, "cond": cond, "truth": truth, "py": None if not r["ok"] else
            [{"status": q["status"], "answer": q["answer"]} for q in r["questions"]], "py_ok": r["ok"], "py_reason": r.get("reason")})
json.dump(meta, open(out / "meta.json", "w"))
print(len(meta), "foto ->", out)
