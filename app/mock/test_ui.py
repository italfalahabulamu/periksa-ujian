"""Uji prototipe mock di Chromium headless (Playwright).

Pemakaian: python3 test_ui.py [index.html] [folder_screenshot]
Keluar dengan kode 1 bila ada uji gagal.
"""
import csv
import io
import json
import pathlib
import re
import sys

from playwright.sync_api import sync_playwright

HTML = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "index.html").resolve()
SHOTS = pathlib.Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else None
URL = HTML.as_uri()
PNG = bytes.fromhex("89504e470d0a1a0a0000000d49484452000000010000000108060000001f15c4890000000d49444154789c6360f8cfc0000003010100c9fe92ef0000000049454e44ae426082")
fails, passes = [], 0


def check(name, cond, detail=""):
    global passes
    if cond:
        passes += 1
        print("  ok  ", name)
    else:
        fails.append(name)
        print("  GAGAL", name, detail)


def expected_scores(S, ex, choices):
    """Hitung ulang nilai dari state mentah, independen dari kode aplikasi."""
    kl = next(k for k in S["kelas"] if k["id"] == ex["kelas"])
    out = {}
    n = len(ex["key"])
    for kode in kl["siswa"]:
        sh = ex["sheets"].get(kode)
        if sh is None:
            out[kode] = "belum dipindai"
            continue
        if sh["state"] == "ditolak":
            out[kode] = "foto ditolak"
            continue
        b = s = k = 0
        for i, q in enumerate(sh["q"]):
            fills = q["fills"]
            marked = [j for j, f in enumerate(fills) if f >= 0.45]
            vague = [j for j, f in enumerate(fills) if 0.12 <= f < 0.45]
            if len(marked) == 1 and not vague:
                a = marked[0]
            elif not marked and not vague:
                a = None
            else:
                a = choices[(kode, i)]  # harus dicek guru
            if a is None:
                k += 1
            elif a == ex["key"][i]:
                b += 1
            else:
                s += 1
        # setengah ke atas pada sen, dengan bilangan rasional (tanpa float)
        from fractions import Fraction
        cents = int(Fraction(b * 10000, n) + Fraction(1, 2) // 1) if False else (b * 20000 + n) // (2 * n)
        out[kode] = (b, s, k, f"{cents // 100},{cents % 100:02d}")
    return out


with sync_playwright() as p:
    br = p.chromium.launch()
    ctx = br.new_context(viewport={"width": 390, "height": 844}, accept_downloads=True)
    page = ctx.new_page()
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
    page.goto(URL)

    print("[1] Hitungan murni")
    r = page.evaluate("""() => { const P=window.__pu; const f=(k,a)=>{const r=P.scoreFor(k,a);return [r.benar,r.salah,r.kosong,P.fmt(r.cents)]};
      return {
       a:f([0,1,2,3,4],[0,1,null,0,4]),
       b:f([0,0,0],[0,1,1]), c:f([0,0,0],[0,0,1]),
       d:f(Array(32).fill(0),[0,...Array(31).fill(1)]),
       e:f(Array(8).fill(0),[0,...Array(7).fill(1)]),
       z:f([0,1],[1,0]), full:f([0,1],[0,1]),
       cl:[[0,0,.8,0,0],[.5,.5,0,0,0],[0,0,0,0,.1],[0,0,0,0,.12],[.46,0,0,0,.12],[0,0,0,.45,0],[.8,0,0,0,.45]].map(x=>{const c=P.classify(x);return c.status+':'+c.answer}),
       csv:[P.csvCell('=1+1'),P.csvCell('@x'),P.csvCell('a;b'),P.csvCell('8A-001')] } }""")
    check("3 benar, 1 salah, 1 kosong dari 5 = 60,00", r["a"] == [3, 1, 1, "60,00"], r["a"])
    check("1/3 = 33,33", r["b"][3] == "33,33", r["b"])
    check("2/3 = 66,67", r["c"][3] == "66,67", r["c"])
    check("1/32 = 3,13 (setengah ke atas, tanpa galat float)", r["d"][3] == "3,13", r["d"])
    check("1/8 = 12,50", r["e"][3] == "12,50", r["e"])
    check("nol benar = 0,00 dan semua benar = 100,00", r["z"][3] == "0,00" and r["full"][3] == "100,00", (r["z"], r["full"]))
    check("klasifikasi batas (0,12 / 0,45)", r["cl"] == ["detected:2", "multiple:null", "blank:null", "ambiguous:null", "ambiguous:0", "detected:3", "multiple:null"], r["cl"])
    check("CSV menetralkan rumus", r["csv"] == ["'=1+1", "'@x", '"a;b"', "8A-001"], r["csv"])

    print("[2] Alur dasar")
    check("layar masuk tampil dan ada label mockup", "Mode demo" in page.inner_text("body") and "DATA MOCKUP" in page.inner_text("body"))
    page.click("#login")
    check("beranda memuat ujian contoh", "UH Matematika Bab 3" in page.inner_text("main"))
    check("setelah masuk, riwayat tidak menumpuk (sekali kembali keluar dari beranda)", page.evaluate("history.length") <= 2, page.evaluate("history.length"))
    # polyfill replaceChildren: hapus metode aslinya lalu muat ulang layar
    ctx_old = br.new_context(viewport={"width": 390, "height": 844})
    pg_old = ctx_old.new_page()
    pg_old.add_init_script("delete Element.prototype.replaceChildren;")
    pg_old.goto(URL)
    has = pg_old.evaluate("typeof Element.prototype.replaceChildren")
    pg_old.click("#login")
    check("tetap jalan tanpa replaceChildren bawaan (WebView lama; polyfill aktif)", "UH Matematika Bab 3" in pg_old.inner_text("main") and has == "function", has)
    ctx_old.close()
    seed_json = page.evaluate("() => JSON.stringify(window.__pu.S)")
    S0 = json.loads(seed_json)
    ex0 = S0["ujian"][0]
    n_sheets = sum(1 for v in ex0["sheets"].values() if v["state"] == "terbaca")
    check("data contoh: 21 lembar terbaca, 1 ditolak, 2 belum", n_sheets == 21 and sum(1 for v in ex0["sheets"].values() if v["state"] == "ditolak") == 1)
    page.goto(URL + "#/u/u1/nilai")
    txt = page.inner_text("#st-n")
    final_before = int(txt.split("/")[0])
    pend_students = sum(1 for kode, sh in ex0["sheets"].items() if sh["state"] == "terbaca" and any(
        (len([j for j, f in enumerate(q["fills"]) if f >= .45]) != 1 or any(.12 <= f < .45 for f in q["fills"])) and not (not any(f >= .12 for f in q["fills"])) for q in sh["q"]))
    check("jumlah final awal = lembar tanpa soal ragu/ganda", final_before == n_sheets - pend_students, (final_before, n_sheets, pend_students))
    if SHOTS:
        SHOTS.mkdir(parents=True, exist_ok=True)
        page.screenshot(path=str(SHOTS / "nilai-awal.png"))

    print("[3] Antrean cek ulang sampai kosong")
    page.goto(URL + "#/u/u1/cek")
    if SHOTS:
        page.screenshot(path=str(SHOTS / "cek-ulang.png"))
    choices, steps = {}, 0
    while page.query_selector("button[data-ans]") and steps < 600:
        head = page.inner_text(".card b")  # "8A-004 · soal 7"
        m = re.match(r"(\S+) · soal (\d+)", head)
        kode, qi = m.group(1), int(m.group(2)) - 1
        pick = (qi + steps) % 6 - 1  # -1 = kosong, 0..4
        choices[(kode, qi)] = None if pick < 0 else pick
        page.click(f"button[data-ans='{pick}']")
        steps += 1
    check("antrean habis", page.query_selector("#cek-kosong") is not None, steps)
    stored_total = sum(1 for kode, sh in ex0["sheets"].items() if sh["state"] == "terbaca" for q in sh["q"] if q["status"] in ("multiple", "ambiguous"))
    check(f"jumlah soal yang dicek = jumlah soal ragu/ganda di data ({stored_total})", steps == stored_total, (steps, stored_total))

    print("[4] Nilai, CSV, dan hitungan independen")
    page.goto(URL + "#/u/u1/nilai")
    check("21 lembar final", page.inner_text("#st-n") == "21/24", page.inner_text("#st-n"))
    S1 = json.loads(page.evaluate("() => JSON.stringify(window.__pu.S)"))
    exp = expected_scores(S1, S1["ujian"][0], choices)
    ui = {}
    for tr in page.query_selector_all("#nilai-tbl tbody tr"):
        tds = [t.inner_text().strip() for t in tr.query_selector_all("td")]
        ui[tds[0]] = tuple([int(tds[1]), int(tds[2]), int(tds[3]), tds[4]]) if tds[4] else tds[5]
    check("tabel di layar = hitungan Python independen (24 baris)", all(ui[k] == (v if isinstance(v, tuple) else {"belum dipindai": "belum", "foto ditolak": "foto ulang"}[v]) for k, v in exp.items()), [(k, ui[k], v) for k, v in exp.items() if ui[k] != (v if isinstance(v, tuple) else {"belum dipindai": "belum", "foto ditolak": "foto ulang"}[v])][:3])
    with page.expect_download() as dl:
        page.click("#export")
    raw = pathlib.Path(dl.value.path()).read_bytes()
    check("CSV berawalan BOM UTF-8", raw.startswith(b"\xef\xbb\xbf"))
    rows = list(csv.reader(io.StringIO(raw.decode("utf-8-sig")), delimiter=";"))
    check("CSV: kolom benar", rows[0] == ["kode_peserta", "benar", "salah", "kosong", "skor", "status"], rows[0])
    body = {r[0]: r for r in rows[1:]}
    bad = []
    for k, v in exp.items():
        r_ = body[k]
        if isinstance(v, tuple):
            if (int(r_[1]), int(r_[2]), int(r_[3]), r_[4], r_[5]) != (v[0], v[1], v[2], v[3], "final"):
                bad.append((k, r_, v))
        elif r_[5] != v or r_[4] != "":
            bad.append((k, r_, v))
    check("CSV 24 baris = hitungan Python independen", len(body) == 24 and not bad, bad[:3])
    finals = [v for v in exp.values() if isinstance(v, tuple)]
    cents = [int(v[3].replace(",", "")) for v in finals]
    avg = (2 * sum(cents) + len(cents)) // (2 * len(cents))
    check("rata-rata, terendah, tertinggi cocok", (page.inner_text("#st-avg"), page.inner_text("#st-min"), page.inner_text("#st-max")) ==
          (f"{avg // 100},{avg % 100:02d}", f"{min(cents) // 100},{min(cents) % 100:02d}", f"{max(cents) // 100},{max(cents) % 100:02d}"),
          (page.inner_text("#st-avg"), avg))
    if SHOTS:
        page.screenshot(path=str(SHOTS / "nilai-akhir.png"), full_page=True)

    print("[5] Penyimpanan lokal")
    page.reload()
    check("setelah muat ulang, nilai tetap ada", page.inner_text("#st-n") == "21/24")

    print("[6] Pindai (simulasi)")
    page.goto(URL + "#/u/u1/pindai")
    page.click("#scan-run")
    check("tanpa foto: ditolak dengan pesan", "Pilih atau ambil foto" in page.inner_text("#scan-msg"))
    page.set_input_files("#scan-file", {"name": "x.png", "mimeType": "image/png", "buffer": PNG})
    check("pratinjau foto muncul", page.query_selector("#scan-prev img") is not None)
    before = page.inner_text("#st-n") if page.query_selector("#st-n") else None
    page.click("#scan-run")  # attempt 1 -> dibaca
    page.set_input_files("#scan-file", {"name": "x.png", "mimeType": "image/png", "buffer": PNG})
    page.click("#scan-run")  # attempt 2 -> dibaca
    page.set_input_files("#scan-file", {"name": "x.png", "mimeType": "image/png", "buffer": PNG})
    page.click("#scan-run")  # attempt 3 -> habis siswa? (3 siswa: 022 foto ulang, 023, 024)
    S2 = json.loads(page.evaluate("() => JSON.stringify(window.__pu.S)"))
    st = S2["ujian"][0]["sheets"]
    check("tiga siswa tersisa kini terbaca", all(st.get(k, {}).get("state") == "terbaca" for k in ("8A-022", "8A-023", "8A-024")), {k: st.get(k, {}).get("state") for k in ("8A-022", "8A-023", "8A-024")})
    page.goto(URL + "#/baru")
    page.fill("#new-judul", "Uji coba")
    page.select_option("#new-kelas", "8B")
    page.fill("#new-n", "4")
    page.dispatch_event("#new-n", "change")
    page.click("#new-save")
    check("kunci tidak lengkap: ujian tidak tersimpan, pesan menyebut soal", "Kunci belum lengkap: soal 1, 2, 3, 4" in page.inner_text("#new-err"), page.inner_text("#new-err"))
    for i in range(4):
        page.click(f"button[data-q='{i}'][data-o='{i}']")
    page.click("#new-save")
    page.wait_for_function("() => location.hash === '#/u/u2/ringkas' && document.querySelector('header h1').textContent === 'Uji coba'")
    check("ujian baru tersimpan dan terbuka", "4 soal" in page.inner_text("main") and "Kelas 8B" in page.inner_text("main"), page.inner_text("main")[:80])
    page.goto(URL + "#/u/u2/pindai")
    results = []
    for i in range(4):
        page.set_input_files("#scan-file", {"name": "x.png", "mimeType": "image/png", "buffer": PNG})
        page.click("#scan-run")
        results.append(page.inner_text("#scan-msg") if page.query_selector("#scan-msg") else "")
    S3 = json.loads(page.evaluate("() => JSON.stringify(window.__pu.S)"))
    states = [S3["ujian"][1]["sheets"].get(k, {}).get("state") for k in ("8B-001", "8B-002", "8B-003", "8B-004")]
    # penghitung global: tiga pindai sebelumnya = 1..3; empat percobaan di u2 = 4..7.
    # Nomor 4 (kelipatan 4) ditolak pada 8B-001, lalu 8B-001 diulang (5), 8B-002 (6), 8B-003 (7).
    check("percobaan ke-4 ditolak dengan pesan terlihat, lalu foto ulang diterima", "ditolak (simulasi)" in results[0] and "8B-001" in results[0], results)
    check("setelah foto ulang: tiga lembar terbaca, 8B-004 belum", states == ["terbaca", "terbaca", "terbaca", None], states)

    print("[7] Kelas, impor, LJK")
    page.goto(URL + "#/kelas")
    page.fill("#imp-text", "8A-025\n8A-001\nxx\n8A-026")
    page.click("#imp-run")
    msg = page.inner_text("#imp-msg")
    check("impor: 2 diterima, 2 ditolak dengan alasan", msg.startswith("2 diterima, 2 ditolak.") and "sudah ada" in msg and "format tidak valid" in msg, msg)
    page.goto(URL + "#/lembar/u1/*")
    nsheets = page.eval_on_selector_all("svg.sheet", "e=>e.length")
    check("LJK semua siswa = 26 lembar (24 + 2 hasil impor)", nsheets == 26, nsheets)
    check("tiap LJK punya 40x5 bulatan dan 4 marka", page.eval_on_selector("svg.sheet", "s=>[s.querySelectorAll('circle').length,s.querySelectorAll('rect[fill=\"#000\"]').length]") == [200, 4])
    if SHOTS:
        page.goto(URL + "#/lembar/u1/8A-001")
        page.screenshot(path=str(SHOTS / "lembar.png"))
        page.goto(URL + "#/")
        page.screenshot(path=str(SHOTS / "beranda.png"))
        page.goto(URL + "#/baru")
        page.screenshot(path=str(SHOTS / "baru.png"))

    print("[8] Cadangan dan reset")
    page.goto(URL + "#/data")
    with page.expect_download() as dl2:
        page.click("#bk-export")
    bk = json.loads(pathlib.Path(dl2.value.path()).read_text())
    check("cadangan JSON memuat 2+ ujian", len(bk["ujian"]) == 2)
    page.click("#reset")
    S4 = json.dumps(json.loads(page.evaluate("() => JSON.stringify(window.__pu.S)")), sort_keys=True)
    S0s = json.loads(seed_json)
    check("reset mengembalikan data awal yang sama persis (deterministik)", S4 == json.dumps(S0s, sort_keys=True))
    page.goto(URL + "#/data")
    page.fill("#bk-text", json.dumps(bk))
    page.click("#bk-import")
    check("pulihkan dari cadangan mengembalikan 2 ujian", len(json.loads(page.evaluate("() => JSON.stringify(window.__pu.S)"))["ujian"]) == 2)
    page.goto(URL + "#/data")
    page.fill("#bk-text", "{rusak")
    page.click("#bk-import")
    check("cadangan rusak ditolak, data tetap", len(json.loads(page.evaluate("() => JSON.stringify(window.__pu.S)"))["ujian"]) == 2)

    print("[9] Cabang Android (bridge tiruan yang mencatat panggilan)")
    ctx2 = br.new_context(viewport={"width": 390, "height": 844}, accept_downloads=True)
    pg2 = ctx2.new_page()
    err2, dls = [], []
    pg2.on("pageerror", lambda e: err2.append(str(e)))
    pg2.on("console", lambda m: err2.append(m.text) if m.type == "error" else None)
    pg2.on("download", lambda d: dls.append(d))
    pg2.add_init_script("window.__shared=[]; window.AndroidBridge={share:function(n,t){window.__shared.push([n,t]);}};")
    pg2.goto(URL)
    pg2.click("#login")
    pg2.goto(URL + "#/u/u1/nilai")
    check("tombol ekspor berlabel 'Bagikan CSV'", pg2.inner_text("#export") == "Bagikan CSV", pg2.inner_text("#export"))
    pg2.click("#export")
    pg2.wait_for_timeout(400)
    shared = pg2.evaluate("window.__shared")
    want_csv = pg2.evaluate("window.__pu.csvFor(window.__pu.S, window.__pu.S.ujian[0])")
    check("CSV lewat AndroidBridge.share dengan nama dan isi yang benar, tanpa unduhan browser",
          len(shared) == 1 and shared[0][0] == "nilai-8A-u1.csv" and shared[0][1] == want_csv and not dls and want_csv.startswith("﻿"), (shared[:1] and shared[0][0], len(dls)))
    pg2.goto(URL + "#/data")
    pg2.click("#bk-export")
    pg2.wait_for_timeout(300)
    shared = pg2.evaluate("window.__shared")
    check("cadangan JSON lewat bridge dan dapat dibaca kembali", len(shared) == 2 and shared[1][0] == "cadangan-periksa-ujian.json" and json.loads(shared[1][1])["v"] == 1, shared[-1][0] if shared else None)
    pg2.goto(URL + "#/lembar/u1/8A-001")
    check("di Android: tombol Cetak diganti petunjuk", pg2.query_selector("#print") is None and "Cetak belum tersedia" in pg2.inner_text("main"))
    check("tidak ada galat konsol di mode Android", not err2, err2[:3])
    ctx2.close()

    check("tidak ada galat di konsol", not errors, errors[:3])
    br.close()

print(f"\n{passes} lulus, {len(fails)} gagal")
if fails:
    print("GAGAL:", fails)
    sys.exit(1)
