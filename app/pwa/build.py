"""Bangun PWA dari app/mock/index.html: sisipkan manifest + pendaftaran service worker, tulis manifest, sw.js, ikon."""
import hashlib, json, pathlib, sys
from PIL import Image, ImageDraw
src = pathlib.Path(__file__).resolve().parent.parent / "mock" / "index.html"
out = pathlib.Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
html = src.read_text(encoding="utf-8")
html = html.replace('<meta name="theme-color" content="#0f766e">',
    '<meta name="theme-color" content="#0f766e">\n<link rel="manifest" href="manifest.webmanifest">\n<link rel="icon" href="icon-192.png">', 1)
reg = "<script>if('serviceWorker' in navigator){addEventListener('load',()=>navigator.serviceWorker.register('sw.js').catch(()=>{}));}</script>\n</body>"
assert html.count("</body>") == 1
html = html.replace("</body>", reg, 1)
(out / "index.html").write_text(html, encoding="utf-8")
for n in (192, 512):
    im = Image.new("RGB", (n, n), "#0f766e"); d = ImageDraw.Draw(im)
    d.rounded_rectangle([n*.22, n*.18, n*.78, n*.82], n*.05, fill="white")
    for i in range(4):
        y = n*(.3+i*.13); d.ellipse([n*.3, y, n*.3+n*.07, y+n*.07], outline="#0f766e", width=max(2, n//64))
        d.line([n*.43, y+n*.035, n*.68, y+n*.035], fill="#0f766e", width=max(2, n//64))
    im.save(out / f"icon-{n}.png")
(out / "manifest.webmanifest").write_text(json.dumps({
    "name": "Periksa Ujian (Mock)", "short_name": "Periksa", "start_url": "./index.html", "scope": "./",
    "display": "standalone", "background_color": "#ffffff", "theme_color": "#0f766e", "lang": "id",
    "icons": [{"src": "icon-192.png", "sizes": "192x192", "type": "image/png"},
              {"src": "icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any maskable"}]}, indent=1))
ver = hashlib.sha256(html.encode()).hexdigest()[:12]
(out / "sw.js").write_text(f"""const V='pu-{ver}';
const FILES=['./','index.html','manifest.webmanifest','icon-192.png','icon-512.png'];
self.addEventListener('install',e=>{{e.waitUntil(caches.open(V).then(c=>c.addAll(FILES)).then(()=>self.skipWaiting()));}});
self.addEventListener('activate',e=>{{e.waitUntil(caches.keys().then(k=>Promise.all(k.filter(x=>x!==V).map(x=>caches.delete(x)))).then(()=>self.clients.claim()));}});
self.addEventListener('fetch',e=>{{if(e.request.method!=='GET')return;e.respondWith(caches.match(e.request,{{ignoreSearch:true}}).then(r=>r||fetch(e.request)));}});
""")
print("PWA ->", out, "versi cache", ver)
