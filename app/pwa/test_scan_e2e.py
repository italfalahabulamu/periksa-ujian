"""Uji ujung ke ujung PWA: cetak LJK dari aplikasi -> isi (sintetis) -> 'foto' -> unggah lewat layar Pindai -> bandingkan dengan kebenaran dasar.
Memastikan geometri LJK aplikasi cocok dengan pembaca. Pemakaian: python3 test_scan_e2e.py <folder_pwa>"""
import functools, http.server, io, pathlib, sys, threading
import cv2, numpy as np
from playwright.sync_api import sync_playwright
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "spikes" / "omr-01"))
import synth
root = pathlib.Path(sys.argv[1]).resolve()
H = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(root)); H.log_message = lambda *a, **k: None
srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), H); threading.Thread(target=srv.serve_forever, daemon=True).start()
URL = f"http://127.0.0.1:{srv.server_address[1]}/index.html"
f, p = [], 0
def ck(n, c, d=""):
    global p
    if c: p += 1; print("  ok  ", n)
    else: f.append(n); print("  GAGAL", n, d)
rng = np.random.default_rng(4242)
with sync_playwright() as pw:
    b = pw.chromium.launch(); page = b.new_page(viewport={"width": 1100, "height": 900}); errs = []; page.on("pageerror", lambda e: errs.append(str(e)))
    page.goto(URL); page.click("#login")
    page.goto(URL + "#/lembar/u1/8A-023"); page.wait_for_selector("svg.sheet")
    svg = page.evaluate("document.querySelector('svg.sheet').outerHTML")
    shot = b.new_page(viewport={"width": 2100, "height": 2970})
    shot.set_content(f"<body style='margin:0'><div style='width:2100px;height:2970px'>{svg.replace('<svg', '<svg width=2100 height=2970', 1)}</div></body>")
    png = shot.screenshot(clip={"x": 0, "y": 0, "width": 2100, "height": 2970})
    blank = cv2.imdecode(np.frombuffer(png, np.uint8), cv2.IMREAD_GRAYSCALE)
    ck("render LJK aplikasi 2100x2970", blank.shape == (2970, 2100), blank.shape)
    n = page.evaluate("window.__pu.S.ujian[0].n"); ck("ujian contoh 40 soal", n == 40)
    jobs = []  # (kode, kondisi, kebenaran dasar)
    for kode, cond in (("8A-023", "A_mudah"), ("8A-024", "B_sedang"), ("8A-022", "A_mudah")):
        img = blank.copy(); truth = []
        for q in range(n):
            kind = str(rng.choice(["clean", "clean", "clean", "clean", "blank", "double"])); o = int(rng.integers(5)); o2 = (o + 1 + int(rng.integers(4))) % 5
            if kind == "clean": synth.draw_mark(img, q, o, str(rng.choice(["strong", "medium"])), rng)
            elif kind == "double": synth.draw_mark(img, q, o, "strong", rng); synth.draw_mark(img, q, o2, "strong", rng)
            truth.append((kind, o if kind != "blank" else None))
        photo, _ = synth.photo(img, cond, rng); ok, buf = cv2.imencode(".jpg", photo, [cv2.IMWRITE_JPEG_QUALITY, 85]); jobs.append((kode, bytes(buf), truth))
    page.goto(URL + "#/u/u1/pindai"); page.wait_for_selector("#scan-run")
    ck("tombol kamera tersedia (capture)", page.get_attribute("#scan-cam", "capture") == "environment")
    ck("teks tidak lagi 'simulasi'", "SIMULASI" not in page.inner_text("#app"))
    for kode, jpg, truth in jobs:
        page.evaluate("(k) => { delete window.__pu.S.ujian[0].sheets[k]; }", kode)  # hindari membaca status lama
        page.goto(URL + "#/u/u1/ringkas"); page.goto(URL + "#/u/u1/pindai"); page.wait_for_selector("#scan-run")
        page.select_option("#scan-siswa", kode); page.set_input_files("#scan-file", {"name": "foto.jpg", "mimeType": "image/jpeg", "buffer": jpg})
        page.click("#scan-run"); page.wait_for_function("(k) => { const s = window.__pu.S.ujian[0].sheets[k]; return s && s.state }", arg=kode, timeout=60000)
        sh = page.evaluate("(k) => window.__pu.S.ujian[0].sheets[k]", kode)
        ck(f"{kode}: terbaca", sh["state"] == "terbaca", sh)
        if sh["state"] != "terbaca": continue
        silent = 0
        for q, (kind, o) in zip(sh["q"], truth):
            if q["status"] in ("multiple", "ambiguous"): continue
            good = (kind == "clean" and q["status"] == "detected" and q["answer"] == o) or (kind == "blank" and q["status"] == "blank")
            silent += 0 if good else 1
        ck(f"{kode}: 0 salah baca tak ditandai (40 soal)", silent == 0, silent)
        ck(f"{kode}: tanda ganda terdeteksi", all(q["status"] == "multiple" for q, (k, _) in zip(sh["q"], truth) if k == "double"))
    # foto jelek harus ditolak, bukan dibaca asal
    page.goto(URL + "#/u/u1/pindai"); page.wait_for_selector("#scan-run")
    todo = ["8A-024"]
    junk = cv2.imencode(".jpg", rng.integers(0, 255, (900, 700), dtype=np.uint8))[1].tobytes()
    if todo:
        k = todo[0]; page.evaluate("(k) => { delete window.__pu.S.ujian[0].sheets[k]; }", k); page.goto(URL + "#/u/u1/ringkas"); page.goto(URL + "#/u/u1/pindai"); page.wait_for_selector("#scan-run"); page.select_option("#scan-siswa", k); page.set_input_files("#scan-file", {"name": "noise.jpg", "mimeType": "image/jpeg", "buffer": junk})
        page.click("#scan-run"); page.wait_for_function("(k) => window.__pu.S.ujian[0].sheets[k] && window.__pu.S.ujian[0].sheets[k].state === 'ditolak'", arg=k, timeout=60000)
        ck("foto derau ditolak dengan alasan", "ditolak" in page.inner_text("#scan-msg") or page.evaluate("(k)=>window.__pu.S.ujian[0].sheets[k].alasan.length>10", k))
    ck("tanpa galat JS", not errs, errs); b.close()
print(f"\n{p} lulus, {len(f)} gagal"); sys.exit(1 if f else 0)
