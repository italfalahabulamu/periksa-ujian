"""Uji pembaca JS pada set foto sintetis (make_set.py). Pemakaian: python3 test_omr.py <folder_set>"""
import base64, json, pathlib, sys, time
from collections import Counter, defaultdict
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "spikes" / "omr-01"))
from run_spike import acceptable
from playwright.sync_api import sync_playwright
d = pathlib.Path(sys.argv[1]); meta = json.load(open(d / "meta.json"))
JS = (pathlib.Path(__file__).parent / "omr.js").read_text()
st = defaultdict(Counter); par = Counter(); times = []
with sync_playwright() as pw:
    b = pw.chromium.launch(); pg = b.new_page(); pg.set_content("<canvas id=c></canvas>"); pg.add_script_tag(content=JS)
    for m in meta:
        b64 = base64.b64encode((d / m["file"]).read_bytes()).decode()
        t0 = time.time()
        r = pg.evaluate("""async b64 => { const im = new Image(); im.src = 'data:image/jpeg;base64,' + b64; await im.decode();
            const c = document.getElementById('c'); c.width = im.width; c.height = im.height; const x = c.getContext('2d'); x.drawImage(im, 0, 0);
            const id = x.getImageData(0, 0, im.width, im.height); return OMR.readSheet(OMR.toGray(id.data, im.width, im.height)); }""", b64)
        times.append(time.time() - t0); s = st[m["cond"]]; s["sheets"] += 1
        if not r["ok"]:
            s["unreadable"] += 1; par["py_ok_js_fail" if m["py_ok"] else "both_fail"] += 1; print("  tak terbaca", m["file"], r["reason"]); continue
        for q, t in zip(r["questions"], m["truth"]):
            s["q"] += 1; s[acceptable(t["cat"], t["intended"], q["status"], q["answer"])] += 1
        if m["py_ok"]:
            same = sum(a["status"] == q["status"] and a["answer"] == q["answer"] for a, q in zip(m["py"], r["questions"]))
            par["q_sama"] += same; par["q_total"] += 40
        else: par["js_ok_py_fail"] += 1
    b.close()
for c, s in st.items():
    nq = s["q"]; print(f"[{c}] lembar={s['sheets']} tak_terbaca={s['unreadable']} soal={nq} ok={s['ok']} ditandai={s['flag']} SALAH_TAK_DITANDAI={s['silent']}")
print("paritas dengan reader.py:", dict(par)); print(f"waktu per foto (termasuk decode): rata2 {sum(times)/len(times):.1f}s maks {max(times):.1f}s (Chromium headless di server, BUKAN ponsel)")
