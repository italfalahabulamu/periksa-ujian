"""Kit lapangan spike 02: LJK cetak (A4, 100% skala), lembar instruksi pengisian per lembar, dan kunci kebenaran dasar.
Pemakaian: python3 make_kit.py <jumlah_lembar> <seed> <folder_keluar>
Keluaran: ljk.pdf (cetak 100%, TANPA fit-to-page), instruksi.pdf (untuk pengisi), kunci.csv (rahasia dari pembaca)."""
import csv, sys
from pathlib import Path
import cv2, numpy as np
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "omr-01"))
import synth

KINDS = [("clean", 0.70), ("blank", 0.10), ("double", 0.08), ("faint", 0.06), ("erase", 0.06)]
TXT = {"clean": "isi tebal", "blank": "KOSONGKAN", "double": "isi DUA bulatan", "faint": "isi SANGAT TIPIS (pensil ringan)", "erase": "isi, hapus, lalu isi yang lain"}


def plan_for(rng):
    kinds, ps = zip(*KINDS); out = []
    for q in range(synth.N_Q):
        k = str(rng.choice(kinds, p=ps)); a = int(rng.integers(5)); b = int(rng.choice([x for x in range(5) if x != a]))
        out.append((k, a, b))
    return out


def blank_with_number(blank, n):
    img = blank.copy(); cv2.putText(img, f"No. {n:02d}", (150 * synth.MM, 31 * synth.MM), cv2.FONT_HERSHEY_SIMPLEX, 1.6, 0, 3); return img


def instruction_page(n, plan):
    W, H = 1654, 2339  # A4 200 dpi
    im = Image.new("L", (W, H), 255); d = ImageDraw.Draw(im)
    try: f, fb = ImageFont.truetype("DejaVuSans.ttf", 34), ImageFont.truetype("DejaVuSans-Bold.ttf", 48)
    except OSError: f = fb = ImageFont.load_default()
    d.text((80, 70), f"Instruksi pengisian LJK No. {n:02d}", font=fb, fill=0)
    d.text((80, 140), "Isi PERSIS sesuai daftar. Jangan beri tahu pembaca foto. Pakai pulpen/pensil biasa.", font=f, fill=0)
    for q, (k, a, b) in enumerate(plan):
        col, row = q // 20, q % 20; x, y = 80 + col * 790, 230 + row * 100
        opt = {"clean": f"{'ABCDE'[a]}", "blank": "-", "double": f"{'ABCDE'[a]} dan {'ABCDE'[b]}", "faint": f"{'ABCDE'[a]}",
               "erase": f"awal {'ABCDE'[b]}, hapus, akhir {'ABCDE'[a]}"}[k]
        d.text((x, y), f"{q+1:>2}. {opt}", font=fb, fill=0); d.text((x + 40, y + 52), TXT[k], font=f, fill=90)
    return im


def main():
    n, seed, out = int(sys.argv[1]), int(sys.argv[2]), Path(sys.argv[3]); out.mkdir(parents=True, exist_ok=True)
    blank = synth.render_blank(); rng = np.random.default_rng(seed); pages, ins, rows = [], [], []
    for i in range(1, n + 1):
        plan = plan_for(rng); pages.append(Image.fromarray(blank_with_number(blank, i))); ins.append(instruction_page(i, plan))
        for q, (k, a, b) in enumerate(plan):
            rows.append([i, q + 1, k, "ABCDE"[a] if k != "blank" else "", "ABCDE"[b] if k in ("double", "erase") else ""])
    pages[0].save(out / "ljk.pdf", save_all=True, append_images=pages[1:], resolution=254.0)  # 2100 px = 210 mm
    ins[0].save(out / "instruksi.pdf", save_all=True, append_images=ins[1:], resolution=200.0)
    with open(out / "kunci.csv", "w", newline="") as f:
        w = csv.writer(f); w.writerow(["lembar", "soal", "jenis", "jawaban_akhir", "opsi_lain"]); w.writerows(rows)
    print(n, "lembar ->", out)


if __name__ == "__main__":
    main()
