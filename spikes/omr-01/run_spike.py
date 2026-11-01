"""Spike 01 (disposable): jalankan evaluasi dan tulis hasil.

Pemakaian: python3 run_spike.py <seed> <sheets_per_condition> <out_dir> [--samples]
"""
import json
import sys
import time
from collections import Counter, defaultdict
from math import sqrt
from pathlib import Path

import cv2
import numpy as np

import synth
from reader import read_sheet

CLEAN = ("clean", "clean_ghost")


def acceptable(cat, intended, st, ans):
    """Kembalikan 'ok', 'flag' (diminta dicek manusia), atau 'silent' (salah baca tak ditandai)."""
    if st in ("multiple", "ambiguous"):
        if cat == "double" and st == "multiple":
            return "ok"
        return "flag"
    if cat in CLEAN or cat in ("partial", "faint"):
        return "ok" if (st == "detected" and ans == intended) else "silent"
    if cat == "blank":
        return "ok" if st == "blank" else "silent"
    if cat == "double":
        return "silent"
    raise ValueError(cat)


def wilson_upper(k, n, z=1.96):
    if n == 0:
        return float("nan")
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    m = z * sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (c + m) / d


def main():
    seed, n_sheets, out_dir = int(sys.argv[1]), int(sys.argv[2]), Path(sys.argv[3])
    samples = "--samples" in sys.argv
    out_dir.mkdir(parents=True, exist_ok=True)
    blank = synth.render_blank()
    rng = np.random.default_rng(seed)
    res = {}
    for cond in synth.COND:
        stats = Counter()
        bycat = defaultdict(Counter)
        sizes, times = [], []
        silent_examples = []
        for i in range(n_sheets):
            sheet, truth = synth.make_sheet(blank, rng)
            img, nbytes = synth.photo(sheet, cond, rng)
            sizes.append(nbytes)
            if samples and i == 0:
                small = cv2.resize(img, (600, 800), interpolation=cv2.INTER_AREA)
                cv2.imwrite(str(out_dir / f"sample_{cond}.jpg"), small, [cv2.IMWRITE_JPEG_QUALITY, 80])
            t0 = time.time()
            r = read_sheet(img)
            times.append(time.time() - t0)
            stats["sheets"] += 1
            if not r["ok"]:
                stats["sheets_unreadable"] += 1
                continue
            for q, (t, o) in enumerate(zip(truth, r["questions"])):
                v = acceptable(t["cat"], t["intended"], o["status"], o["answer"])
                stats["questions"] += 1
                stats[v] += 1
                bycat[t["cat"]][v] += 1
                if t["cat"] in CLEAN:
                    stats["clean_q"] += 1
                    stats["clean_flag"] += v == "flag"
                if v == "silent" and len(silent_examples) < 5:
                    silent_examples.append({"sheet": i, "q": q + 1, "cat": t["cat"], "truth": t["intended"],
                                            "got": [o["status"], o["answer"]],
                                            "fills": [round(f, 2) for f in o["fills"]]})
        res[cond] = {"stats": dict(stats), "bycat": {k: dict(v) for k, v in bycat.items()},
                     "silent_examples": silent_examples,
                     "jpeg_kb_mean": round(float(np.mean(sizes)) / 1024),
                     "read_ms_mean": round(float(np.mean(times)) * 1000)}
    json.dump(res, open(out_dir / f"results_seed{seed}.json", "w"), indent=1, default=int)

    print(f"seed={seed} sheets/condition={n_sheets}")
    for cond, r in res.items():
        s = r["stats"]
        nq = s.get("questions", 0)
        sil = s.get("silent", 0)
        print(f"\n[{cond}] sheets={s['sheets']} unreadable={s.get('sheets_unreadable', 0)} questions={nq} "
              f"jpeg~{r['jpeg_kb_mean']}KB read~{r['read_ms_mean']}ms")
        if nq:
            print(f"  silent errors: {sil}/{nq} = {100*sil/nq:.2f}%  (95% upper bound {100*wilson_upper(sil, nq):.2f}%)")
            cq = s.get("clean_q", 0)
            print(f"  flag on clean answers (false alarm): {s.get('clean_flag', 0)}/{cq} = {100*s.get('clean_flag', 0)/max(cq, 1):.2f}%")
            print(f"  flagged overall: {s.get('flag', 0)}/{nq} = {100*s.get('flag', 0)/nq:.2f}%")
            for cat, c in sorted(r["bycat"].items()):
                print(f"    {cat:12s} {dict(c)}")
        for e in r["silent_examples"]:
            print("   silent ex:", e)


if __name__ == "__main__":
    main()
