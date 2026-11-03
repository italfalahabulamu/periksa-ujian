"""Evaluasi spike 02: jalankan pembaca JS (app/pwa/omr.js) pada foto nyata dan bandingkan dengan kunci.csv.
Nama foto: lembar-NN_<ponsel>_<baik|sulit>.jpg. Pemakaian: python3 evaluate.py <kit_dengan_kunci.csv> <folder_foto> [laporan.md]"""
import base64, csv, re, sys
from collections import Counter, defaultdict
from math import sqrt
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "omr-01"))
from run_spike import acceptable
from playwright.sync_api import sync_playwright
OMR = Path(__file__).resolve().parents[2] / "app" / "pwa" / "omr.js"
CAT = {"clean": "clean", "blank": "blank", "double": "double", "faint": "faint", "erase": "clean_ghost"}
def wilson(k, n, z=1.96):
    if not n: return float("nan")
    p = k / n; d = 1 + z * z / n; return (p + z * z / (2 * n) + z * sqrt(p * (1 - p) / n + z * z / (4 * n * n))) / d
kit, photos = Path(sys.argv[1]), Path(sys.argv[2]); rep = Path(sys.argv[3]) if len(sys.argv) > 3 else None
key = defaultdict(dict)
for r in csv.DictReader(open(kit / "kunci.csv")): key[int(r["lembar"])][int(r["soal"])] = r
st = defaultdict(Counter); silent = []
with sync_playwright() as pw:
    b = pw.chromium.launch(); pg = b.new_page(); pg.set_content("<canvas id=c></canvas>"); pg.add_script_tag(content=OMR.read_text())
    for f in sorted(photos.glob("lembar-*.jpg")):
        m = re.match(r"lembar-(\d+)_(.+)_(baik|sulit)\.jpg$", f.name)
        if not m: print("nama tidak sesuai konvensi, dilewati:", f.name); continue
        sheet, phone, cond = int(m[1]), m[2], m[3]; s = st[(phone, cond)]; s["foto"] += 1
        if sheet not in key: print("tidak ada di kunci:", f.name); continue
        r = pg.evaluate("""async b64 => { const im = new Image(); im.src = 'data:image/jpeg;base64,' + b64; await im.decode();
            const c = document.getElementById('c'); c.width = im.width; c.height = im.height; const x = c.getContext('2d'); x.drawImage(im, 0, 0);
            const id = x.getImageData(0, 0, im.width, im.height); return OMR.readSheet(OMR.toGray(id.data, im.width, im.height)); }""", base64.b64encode(f.read_bytes()).decode())
        if not r["ok"]: s["ditolak"] += 1; continue
        for q, res in enumerate(r["questions"], 1):
            k = key[sheet][q]; intended = "ABCDE".find(k["jawaban_akhir"]); intended = None if intended < 0 else intended
            v = acceptable(CAT[k["jenis"]], intended, res["status"], res["answer"]); s["soal"] += 1; s[v] += 1
            if v == "silent": silent.append((f.name, q, k["jenis"], k["jawaban_akhir"] or "-", res["status"], "ABCDE"[res["answer"]] if res["answer"] is not None else "-"))
    b.close()
L = ["# Laporan spike 02", "", "| Ponsel | Kondisi | Foto | Ditolak | Soal | Benar | Ditandai | Salah tak ditandai | Batas atas 95% |", "|---|---|---|---|---|---|---|---|---|"]
tot = Counter()
for (ph, c), s in sorted(st.items()):
    L.append(f"| {ph} | {c} | {s['foto']} | {s['ditolak']} | {s['soal']} | {s['ok']} | {s['flag']} | {s['silent']} | {100*wilson(s['silent'], s['soal']):.2f}% |"); tot.update(s)
rej = tot["ditolak"] / max(tot["foto"], 1); sil = tot["silent"] / max(tot["soal"], 1)
L += ["", f"Total: foto {tot['foto']}, ditolak {100*rej:.1f}%, salah tak ditandai {tot['silent']} dari {tot['soal']} soal ({100*sil:.2f}%, batas atas 95% {100*wilson(tot['silent'], tot['soal']):.2f}%).",
      f"Keputusan titik putus (ditolak <= 25% dan salah tak ditandai <= 0,5%): **{'LULUS, pembaca dipakai di pilot' if rej <= .25 and sil <= .005 else 'GAGAL, pilot memakai input manual'}**.", ""]
if silent: L += ["Salah baca tak ditandai (periksa foto):", ""] + [f"- {a} soal {q} jenis={j} kunci={t} dibaca={s}/{d}" for a, q, j, t, s, d in silent]
print("\n".join(L)); rep and rep.write_text("\n".join(L), encoding="utf-8")
