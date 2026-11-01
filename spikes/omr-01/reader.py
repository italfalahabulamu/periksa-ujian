"""Spike 01 (disposable): pembaca OMR berbasis marka sudut + homografi + rasio isi gelembung.

Ambang T_LO dan REG_MIN diturunkan dari set kalibrasi (seed 1) dan diuji sekali di set uji terpisah (seed 2).
"""
import itertools

import cv2
import numpy as np

from synth import BUB_D, COL_X, MARKERS, MM, N_Q, OPT_DX, ROW0, ROW_DY, ROWS

T_HI = 0.45   # rasio isi >= T_HI : bulatan dianggap terisi
T_LO = 0.12   # 0,12 <= rasio < T_HI : ragu (di atas semua bulatan kosong di set kalibrasi, maks 0,09)
TEMPLATE_PTS = np.float32([[MARKERS[k][0], MARKERS[k][1]] for k in ("TL", "TR", "BR", "BL")])


def find_markers(gray):
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    bw = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 61, 12)
    # RETR_CCOMP + parent == -1: semua batas luar komponen, termasuk yang berada di dalam lubang komponen lain
    # (pita tepi kertas bisa melingkupi marka; RETR_EXTERNAL melewatkannya)
    cnts, hier = cv2.findContours(bw, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    cnts = [c for c, h in zip(cnts, hier[0]) if h[3] == -1]
    cands = []
    for c in cnts:
        a = cv2.contourArea(c)
        if not 1200 < a < 40000:
            continue
        peri = cv2.arcLength(c, True)
        ap = cv2.approxPolyDP(c, 0.06 * peri, True)
        if len(ap) != 4 or not cv2.isContourConvex(ap):
            continue
        (_, _), (w, h), _ = cv2.minAreaRect(c)
        if min(w, h) < 1 or not 0.7 < w / h < 1.43 or a / (w * h) < 0.8:
            continue
        m = cv2.moments(c)
        cands.append((a, np.array([m["m10"] / m["m00"], m["m01"] / m["m00"]], np.float32)))
    if len(cands) < 4:
        return None
    cands = sorted(cands, key=lambda t: -t[0])[:8]
    scored = []
    for combo in itertools.combinations(cands, 4):
        areas = [c[0] for c in combo]
        big = max(areas)
        rest = sorted(areas)[:3]
        # sisanya harus mirip satu sama lain (3 marka kecil), dan yang terbesar kira-kira 1,6-3,6x lebih besar
        if max(rest) / min(rest) > 1.6 or not 1.6 < big / np.mean(rest) < 3.6:
            continue
        pts = np.array([c[1] for c in combo], np.float32)
        quad = cv2.contourArea(cv2.convexHull(pts))
        if quad >= 0.15 * gray.shape[0] * gray.shape[1]:
            scored.append((quad, combo))
    out = []
    for _, combo in sorted(scored, key=lambda t: -t[0]):
        best = sorted(combo, key=lambda t: -t[0])
        tl, rest = best[0][1], [b[1] for b in best[1:]]
        ctr = np.mean([tl] + rest, axis=0)
        ang = lambda p: np.arctan2(p[1] - ctr[1], p[0] - ctr[0])
        a0 = ang(tl)
        rest = sorted(rest, key=lambda p: (ang(p) - a0) % (2 * np.pi))
        areas_by_pt = {tuple(np.round(b[1], 1)): b[0] for b in best}
        pts = np.float32([tl] + rest)  # TL, TR, BR, BL searah jarum jam
        out.append((pts, [areas_by_pt[tuple(np.round(p, 1))] for p in pts]))
    return out or None


def sample(gray, pts):
    h, w = gray.shape
    x = np.clip(pts[:, 0], 0, w - 1.001)
    y = np.clip(pts[:, 1], 0, h - 1.001)
    x0, y0 = np.floor(x).astype(int), np.floor(y).astype(int)
    fx, fy = x - x0, y - y0
    g = gray.astype(np.float32)
    return (g[y0, x0] * (1 - fx) * (1 - fy) + g[y0, x0 + 1] * fx * (1 - fy)
            + g[y0 + 1, x0] * (1 - fx) * fy + g[y0 + 1, x0 + 1] * fx * fy)


def disc_points(cx, cy, r0, r1, n=14, rings=3):
    pts = []
    for rr in np.linspace(r0, r1, rings):
        for a in np.linspace(0, 2 * np.pi, n, endpoint=False):
            pts.append((cx + rr * np.cos(a), cy + rr * np.sin(a)))
    return np.float32(pts)


REG_MIN = 0.30  # gerbang pendaftaran (lembar baik di set kalibrasi: min 0,49)


def sizes_consistent(H, areas, lo=0.5, hi=1.9):
    """Luas kontur tiap marka harus cocok dengan luas yang diprediksi homografi (menolak blob palsu)."""
    for (cx, cy, size), a in zip((MARKERS[k] for k in ("TL", "TR", "BR", "BL")), areas):
        p = lambda x, y: cv2.perspectiveTransform(np.float32([[[x, y]]]), H)[0, 0]
        o, ex, ey = p(cx, cy), p(cx + 1, cy), p(cx, cy + 1)
        pred = abs((ex - o)[0] * (ey - o)[1] - (ex - o)[1] * (ey - o)[0]) * size * size
        if not lo < a / pred < hi:
            return False
    return True


def registration_score(gray, proj, K):
    """Median kontras garis tepi bulatan pada posisi yang diharapkan. Mendekati 0 bila homografi salah."""
    r = BUB_D / 2
    vals = []
    for q in range(N_Q):
        for o in range(5):
            bx, by = COL_X[q // ROWS] + o * OPT_DX, ROW0 + (q % ROWS) * ROW_DY
            P = float(np.median(sample(gray, proj(disc_points(bx, by, 1.45 * r, 1.6 * r, n=16, rings=2)))))
            ring = min(float(sample(gray, proj(disc_points(bx, by, f * r, f * r, n=16, rings=1))).mean())
                       for f in (0.85, 0.93, 1.0, 1.07, 1.15))
            vals.append((P - ring) / max(P - K, 20.0))
    return float(np.median(vals))


def read_sheet(gray, reg_min=None):
    """Kembalikan dict: status sheet, dan per soal {status, answer, fills}."""
    reg_min = REG_MIN if reg_min is None else reg_min
    sets = find_markers(gray)
    if sets is None:
        return {"ok": False, "reason": "marka sudut tidak ditemukan"}
    best = None
    for mk, areas in sets[:6]:
        H = cv2.getPerspectiveTransform(TEMPLATE_PTS, mk)
        if not sizes_consistent(H, areas):
            continue
        proj = lambda p, H=H: cv2.perspectiveTransform(np.float32(p).reshape(-1, 1, 2), H).reshape(-1, 2)
        blacks = [np.median(sample(gray, proj(disc_points(*TEMPLATE_PTS[i], 0.0, 1.8, n=8, rings=3)))) for i in (1, 2, 3)]
        K = float(np.median(blacks))
        score = registration_score(gray, proj, K)
        if best is None:
            best = (score, H, proj, K)  # kandidat dengan geometri terbaik dipakai lebih dulu
        if reg_min is None or score >= reg_min:
            best = (score, H, proj, K)
            break
    if best is None:
        return {"ok": False, "reason": "marka tidak konsisten dengan template"}
    score, H, proj, K = best
    if reg_min is not None and score < reg_min:
        return {"ok": False, "reason": "pendaftaran gambar gagal (foto ulang)", "reg": score}
    r = BUB_D / 2
    out = []
    for q in range(N_Q):
        fills = []
        for o in range(5):
            bx, by = COL_X[q // ROWS] + o * OPT_DX, ROW0 + (q % ROWS) * ROW_DY
            inner = sample(gray, proj(disc_points(bx, by, 0.0, 0.6 * r)))
            ring = sample(gray, proj(disc_points(bx, by, 1.35 * r, 1.55 * r, n=16, rings=2)))
            P = float(np.median(ring))
            denom = max(P - K, 20.0)
            fills.append(float(np.clip((P - inner.mean()) / denom, 0, 1)))
        marked = [i for i, f in enumerate(fills) if f >= T_HI]
        vague = [i for i, f in enumerate(fills) if T_LO <= f < T_HI]
        if len(marked) >= 2:
            st, ans = "multiple", None
        elif len(marked) == 1 and not vague:
            st, ans = "detected", marked[0]
        elif len(marked) == 0 and not vague:
            st, ans = "blank", None
        else:
            st, ans = "ambiguous", (marked[0] if marked else None)
        out.append({"status": st, "answer": ans, "fills": fills})
    return {"ok": True, "reg": score, "questions": out}
