"""Spike 01 (disposable): template LJK, lembar terisi sintetis, dan simulasi foto ponsel.

Semua ukuran template dalam milimeter. Render lembar 10 px/mm (A4 = 2100 x 2970 px).
"""
import cv2
import numpy as np

MM = 10  # px per mm pada render lembar
PAGE_W, PAGE_H = 210, 297
N_Q, ROWS, OPTS = 40, 20, "ABCDE"
# cx, cy, sisi (mm). TL sengaja lebih besar sebagai penanda orientasi.
MARKERS = {"TL": (18, 18, 16), "TR": (192, 18, 10), "BR": (192, 279, 10), "BL": (18, 279, 10)}
BUB_D = 7.0
COL_X = [34.0, 119.0]
OPT_DX, ROW0, ROW_DY = 11.0, 60.0, 10.5


def bubble_center(q, o):
    return COL_X[q // ROWS] + o * OPT_DX, ROW0 + (q % ROWS) * ROW_DY


def render_blank():
    img = np.full((PAGE_H * MM, PAGE_W * MM), 255, np.uint8)
    for cx, cy, s in MARKERS.values():
        x0, y0 = int((cx - s / 2) * MM), int((cy - s / 2) * MM)
        img[y0:y0 + int(s * MM), x0:x0 + int(s * MM)] = 0
    cv2.putText(img, "LEMBAR JAWABAN (SPIKE)", (62 * MM, 24 * MM), cv2.FONT_HERSHEY_SIMPLEX, 2.2, 0, 4)
    for col in range(2):
        for o, ch in enumerate(OPTS):
            cv2.putText(img, ch, (int((COL_X[col] + o * OPT_DX - 1.8) * MM), int((ROW0 - 8) * MM)),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.4, 0, 3)
    r = int(BUB_D / 2 * MM)
    for q in range(N_Q):
        cx, cy = bubble_center(q, 0)
        cv2.putText(img, str(q + 1), (int((cx - 13) * MM), int((cy + 1.5) * MM)), cv2.FONT_HERSHEY_SIMPLEX, 1.2, 0, 3)
        for o in range(5):
            bx, by = bubble_center(q, o)
            cv2.circle(img, (int(bx * MM), int(by * MM)), r, 0, 3, cv2.LINE_AA)
    return img


# jenis tanda: (rentang abu-abu, pakai half-plane untuk isian sebagian)
KINDS = {
    "strong": ((25, 70), False),   # pulpen / pensil tebal
    "medium": ((80, 125), False),  # pensil biasa
    "faint": ((165, 195), False),  # pensil sangat tipis
    "partial": ((30, 90), True),    # hanya sebagian bulatan terisi
    "ghost": ((205, 225), False),  # bekas hapusan
}


def draw_mark(img, q, o, kind, rng, log=None):
    if log is not None:
        log.append((int(o), kind))
    (g0, g1), partial = KINDS[kind]
    bx, by = bubble_center(q, o)
    r = BUB_D / 2 * MM
    cx, cy = bx * MM + rng.uniform(-3, 3), by * MM + rng.uniform(-3, 3)
    h = int(r * 1.5)
    x0, y0 = int(cx) - h, int(cy) - h
    yy, xx = np.mgrid[-h:h, -h:h].astype(np.float32)
    xx += x0 + h - cx + 0.0
    yy += y0 + h - cy + 0.0
    rad = r * rng.uniform(0.95, 1.1)
    mask = ((xx / rad) ** 2 + (yy / (rad * rng.uniform(0.9, 1.05))) ** 2 <= 1).astype(np.float32)
    if partial:
        ang = rng.uniform(0, 2 * np.pi)
        t = rng.uniform(-0.15, 0.35) * rad
        mask *= ((xx * np.cos(ang) + yy * np.sin(ang)) < t).astype(np.float32)
    mask = cv2.GaussianBlur(mask, (0, 0), 1.2)
    gray = rng.uniform(g0, g1) + rng.normal(0, 8, mask.shape)
    patch = img[y0:y0 + 2 * h, x0:x0 + 2 * h].astype(np.float32)
    blended = patch * (1 - mask) + gray * mask
    img[y0:y0 + 2 * h, x0:x0 + 2 * h] = np.clip(np.minimum(patch, blended), 0, 255).astype(np.uint8)


# kategori -> (peluang, jawaban yang diterima untuk keluaran pembaca)
CATS = ["clean", "clean_ghost", "blank", "double", "partial", "faint"]
CAT_P = [0.78, 0.04, 0.05, 0.05, 0.05, 0.03]


def make_sheet(blank, rng):
    img = blank.copy()
    truth = []
    for q in range(N_Q):
        cat = rng.choice(CATS, p=CAT_P)
        marks = []
        o = int(rng.integers(5))
        others = [x for x in range(5) if x != o]
        if cat == "clean":
            draw_mark(img, q, o, str(rng.choice(["strong", "medium"], p=[0.6, 0.4])), rng, marks)
        elif cat == "clean_ghost":
            draw_mark(img, q, o, "strong", rng, marks)
            draw_mark(img, q, int(rng.choice(others)), "ghost", rng, marks)
        elif cat == "blank":
            if rng.random() < 0.3:
                draw_mark(img, q, o, "ghost", rng, marks)
            o = None
        elif cat == "double":
            o2 = int(rng.choice(others))
            draw_mark(img, q, o, "strong", rng, marks)
            draw_mark(img, q, o2, "strong", rng, marks)
        elif cat == "partial":
            draw_mark(img, q, o, "partial", rng, marks)
        elif cat == "faint":
            draw_mark(img, q, o, "faint", rng, marks)
        truth.append({"cat": str(cat), "intended": o, "marks": marks})
    return img, truth


COND = {
    "A_mudah": dict(scale=0.86, rot=4, persp=0.008, light="even", blur=0.8, noise=3, q=85, flip=0.0),
    "B_sedang": dict(scale=0.80, rot=8, persp=0.02, light="gradient", blur=1.6, noise=5, q=75, flip=0.1),
    "C_berat": dict(scale=0.76, rot=12, persp=0.04, light="dim", blur=2.6, noise=8, q=65, flip=0.1),
}
CW, CH = 1800, 2400


def photo(sheet, cond, rng):
    p = COND[cond]
    if rng.random() < p["flip"]:
        sheet = cv2.rotate(sheet, cv2.ROTATE_180)
    sheet = cv2.GaussianBlur(sheet, (0, 0), 0.7)
    Hp, Wp = sheet.shape
    for attempt in range(25):
        pw = p["scale"] * CW * (0.97 ** attempt)
        ph = pw * Hp / Wp
        cx = CW / 2 + rng.uniform(-0.04, 0.04) * CW
        cy = CH / 2 + rng.uniform(-0.04, 0.04) * CH
        th = np.deg2rad(rng.uniform(-p["rot"], p["rot"]))
        R = np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])
        corners = np.array([[-pw / 2, -ph / 2], [pw / 2, -ph / 2], [pw / 2, ph / 2], [-pw / 2, ph / 2]])
        dst = corners @ R.T + [cx, cy] + rng.normal(0, p["persp"] * pw, (4, 2))
        if dst.min() > 10 and dst[:, 0].max() < CW - 10 and dst[:, 1].max() < CH - 10:
            break
    src = np.float32([[0, 0], [Wp, 0], [Wp, Hp], [0, Hp]])
    M = cv2.getPerspectiveTransform(src, dst.astype(np.float32))
    warped = cv2.warpPerspective(sheet.astype(np.float32) * 0.92, M, (CW, CH), flags=cv2.INTER_LINEAR)
    mask = cv2.warpPerspective(np.ones_like(sheet, np.float32), M, (CW, CH), flags=cv2.INTER_LINEAR)
    bg = cv2.GaussianBlur(rng.normal(0, 18, (CH, CW)).astype(np.float32), (0, 0), 25) + rng.uniform(90, 140)
    img = bg * (1 - mask) + warped * mask
    yy, xx = np.mgrid[0:CH, 0:CW].astype(np.float32)
    if p["light"] == "even":
        field = np.full((CH, CW), 1.0 + rng.normal(0, 0.02), np.float32)
    else:
        a = rng.uniform(0, 2 * np.pi)
        t = (xx * np.cos(a) + yy * np.sin(a))
        t = (t - t.min()) / (t.max() - t.min())
        lo = rng.uniform(0.62, 0.72) if p["light"] == "gradient" else rng.uniform(0.60, 0.70)
        field = lo + (1.05 - lo) * t
        if p["light"] == "dim":
            field *= rng.uniform(0.55, 0.7)
            b = rng.uniform(0, 2 * np.pi)
            s = (xx - CW / 2) * np.cos(b) + (yy - CH / 2) * np.sin(b)
            shadow = 1 - 0.45 / (1 + np.exp(-(s - rng.uniform(-300, 300)) / 40))
            field *= shadow
    img = cv2.GaussianBlur(img * field, (0, 0), p["blur"])
    img = img + rng.normal(0, p["noise"], img.shape)
    img = np.clip(img, 0, 255).astype(np.uint8)
    ok, buf = cv2.imencode(".jpg", img, [cv2.IMWRITE_JPEG_QUALITY, int(p["q"])])
    return cv2.imdecode(buf, cv2.IMREAD_GRAYSCALE), len(buf)
