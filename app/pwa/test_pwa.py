"""Uji PWA: manifest valid, service worker aktif, jalan offline, data bertahan. Pemakaian: python3 test_pwa.py <folder_pwa>"""
import http.server, json, pathlib, sys, threading, functools
from playwright.sync_api import sync_playwright
root = pathlib.Path(sys.argv[1]).resolve()
H = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(root))
H.log_message = lambda *a, **k: None
srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), H); threading.Thread(target=srv.serve_forever, daemon=True).start()
URL = f"http://127.0.0.1:{srv.server_address[1]}/index.html"
f, p = [], 0
def ck(n, c, d=""):
    global p
    if c: p += 1; print("  ok  ", n)
    else: f.append(n); print("  GAGAL", n, d)
m = json.loads((root / "manifest.webmanifest").read_text())
ck("manifest: standalone + ikon 192 & 512", m["display"] == "standalone" and {i["sizes"] for i in m["icons"]} == {"192x192", "512x512"})
ck("manifest: start_url ada", (root / m["start_url"].lstrip("./")).exists())
with sync_playwright() as pw:
    b = pw.chromium.launch(); ctx = b.new_context(viewport={"width": 390, "height": 800}); pg = ctx.new_page()
    errs = []; pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.goto(URL); pg.wait_for_function("navigator.serviceWorker.ready.then(()=>true)", timeout=15000)
    pg.wait_for_function("caches.keys().then(k=>k.length>0)")
    ck("service worker aktif", pg.evaluate("navigator.serviceWorker.ready.then(r=>!!r.active)"))
    cached = pg.evaluate("caches.keys().then(async k=>(await (await caches.open(k[0])).keys()).map(r=>new URL(r.url).pathname))")
    ck("cache berisi index + manifest + ikon", all(x in cached for x in ["/index.html", "/manifest.webmanifest", "/icon-192.png", "/icon-512.png"]), cached)
    pg.reload(); pg.wait_for_load_state()
    pg.evaluate("localStorage.setItem('probe','1')")
    ctx.set_offline(True)
    pg.reload(); pg.wait_for_load_state()
    ck("offline: halaman tetap termuat", pg.title().startswith("Periksa Ujian"), pg.title())
    ck("offline: UI tampil", pg.locator("button").count() > 0)
    ck("offline: data lokal bertahan", pg.evaluate("localStorage.getItem('probe')") == "1")
    ctx.set_offline(False)
    ck("tanpa galat JS", not errs, errs)
    b.close()
print(f"\n{p} lulus, {len(f)} gagal"); sys.exit(1 if f else 0)
