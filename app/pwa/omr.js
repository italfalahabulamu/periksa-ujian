/* Pembaca LJK (JS murni, tanpa OpenCV). Port dari spikes/omr-01/reader.py.
   Masukan: {data: Uint8Array gray, w, h}. Keluaran: {ok, reg, questions:[{status,answer,fills}]} atau {ok:false, reason}.
   Semua ukuran template dalam mm. STATUS: teruji hanya pada foto sintetis (lihat docs/11-rnd). */
(function (root) {
  const TPL = { N_Q: 40, ROWS: 20, BUB_D: 7.0, COL_X: [34.0, 119.0], OPT_DX: 11.0, ROW0: 60.0, ROW_DY: 10.5,
    MARKERS: { TL: [18, 18, 16], TR: [192, 18, 10], BR: [192, 279, 10], BL: [18, 279, 10] } };
  const T_HI = 0.45, T_LO = 0.12, REG_MIN = 0.30;
  const ORDER = ['TL', 'TR', 'BR', 'BL'];

  function blur5(g, w, h) {
    const k = [1, 4, 6, 4, 1], t = new Float32Array(w * h), o = new Float32Array(w * h);
    for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
      let s = 0; for (let i = -2; i <= 2; i++) { const xx = Math.min(w - 1, Math.max(0, x + i)); s += k[i + 2] * g[y * w + xx]; }
      t[y * w + x] = s / 16; }
    for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
      let s = 0; for (let i = -2; i <= 2; i++) { const yy = Math.min(h - 1, Math.max(0, y + i)); s += k[i + 2] * t[yy * w + x]; }
      o[y * w + x] = s / 16; }
    return o;
  }
  function inkMask(b, w, h, win = 61, C = 12) {
    const W = w + 1, I = new Float64Array(W * (h + 1));
    for (let y = 0; y < h; y++) { let r = 0; for (let x = 0; x < w; x++) { r += b[y * w + x]; I[(y + 1) * W + x + 1] = I[y * W + x + 1] + r; } }
    const m = new Uint8Array(w * h), hw = (win - 1) >> 1;
    for (let y = 0; y < h; y++) {
      const y0 = Math.max(0, y - hw), y1 = Math.min(h - 1, y + hw);
      for (let x = 0; x < w; x++) {
        const x0 = Math.max(0, x - hw), x1 = Math.min(w - 1, x + hw);
        const s = I[(y1 + 1) * W + x1 + 1] - I[y0 * W + x1 + 1] - I[(y1 + 1) * W + x0] + I[y0 * W + x0];
        const mean = s / ((x1 - x0 + 1) * (y1 - y0 + 1));
        m[y * w + x] = b[y * w + x] <= mean - C ? 1 : 0;
      }
    }
    return m;
  }
  function components(m, w, h) {
    const lab = new Int32Array(w * h), par = [0];
    const find = a => { while (par[a] !== a) { par[a] = par[par[a]]; a = par[a]; } return a; };
    for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
      const i = y * w + x; if (!m[i]) continue;
      let best = 0;
      const nb = [x > 0 ? lab[i - 1] : 0, y > 0 ? lab[i - w] : 0, (y > 0 && x > 0) ? lab[i - w - 1] : 0, (y > 0 && x < w - 1) ? lab[i - w + 1] : 0];
      for (const l of nb) if (l) { if (!best) best = find(l); else { const r = find(l); if (r !== best) par[r] = best; } }
      if (!best) { best = par.length; par.push(best); }
      lab[i] = best;
    }
    const stats = new Map();
    for (let i = 0; i < w * h; i++) if (lab[i]) {
      const r = find(lab[i]); lab[i] = r; let s = stats.get(r);
      if (!s) { s = { n: 0, x0: w, y0: h, x1: 0, y1: 0, sx: 0, sy: 0 }; stats.set(r, s); }
      const x = i % w, y = (i / w) | 0; s.n++; s.sx += x; s.sy += y;
      if (x < s.x0) s.x0 = x; if (x > s.x1) s.x1 = x; if (y < s.y0) s.y0 = y; if (y > s.y1) s.y1 = y;
    }
    return { lab, stats };
  }
  function squareFit(pix) { // minAreaRect kasar: putar 0..87 derajat langkah 3
    let best = null;
    for (let a = 0; a < 90; a += 3) {
      const c = Math.cos(a * Math.PI / 180), s = Math.sin(a * Math.PI / 180);
      let u0 = 1e9, u1 = -1e9, v0 = 1e9, v1 = -1e9;
      for (let i = 0; i < pix.length; i += 2) { const u = pix[i] * c + pix[i + 1] * s, v = -pix[i] * s + pix[i + 1] * c;
        if (u < u0) u0 = u; if (u > u1) u1 = u; if (v < v0) v0 = v; if (v > v1) v1 = v; }
      const rw = u1 - u0 + 1, rh = v1 - v0 + 1;
      if (!best || rw * rh < best.area) best = { area: rw * rh, rw, rh };
    }
    return best;
  }
  function findMarkers(g, w, h) {
    const b = blur5(g, w, h), m = inkMask(b, w, h), { lab, stats } = components(m, w, h);
    // Marka besar berlubang di tengah setelah ambang adaptif (jendela 61 px), jadi isi dengan rentang baris:
    // luas = luas kontur luar, seperti contourArea pada kontur terluar di versi Python.
    const want = new Map();
    for (const [id, s] of stats) {
      const bw = s.x1 - s.x0 + 1, bh = s.y1 - s.y0 + 1;
      if (s.n < 600 || bw < 25 || bh < 25 || bw > 400 || bh > 400 || bw / bh > 2 || bh / bw > 2) continue;
      want.set(id, { mn: new Int32Array(bh).fill(1 << 30), mx: new Int32Array(bh).fill(-1) });
    }
    for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
      const l = lab[y * w + x]; if (!l) continue; const r = want.get(l); if (!r) continue;
      const k = y - stats.get(l).y0; if (x < r.mn[k]) r.mn[k] = x; if (x > r.mx[k]) r.mx[k] = x;
    }
    const cands = [];
    for (const [id, r] of want) {
      const s = stats.get(id); let area = 0, sx = 0, sy = 0; const pix = [];
      for (let k = 0; k < r.mn.length; k++) if (r.mx[k] >= 0) { const n = r.mx[k] - r.mn[k] + 1, y = s.y0 + k;
        area += n; sx += (r.mn[k] + r.mx[k]) / 2 * n; sy += y * n; pix.push(r.mn[k], y, r.mx[k], y); }
      if (!(area > 1200 && area < 40000)) continue;
      const fit = squareFit(pix);
      if (fit.area <= 0 || area / fit.area < 0.8) continue;
      const q = fit.rw / fit.rh; if (!(q > 0.7 && q < 1.43)) continue;
      cands.push({ a: area, p: [sx / area, sy / area] });
    }
    if (cands.length < 4) return null;
    cands.sort((x, y) => y.a - x.a); const top = cands.slice(0, 8), scored = [];
    for (let i = 0; i < top.length; i++) for (let j = i + 1; j < top.length; j++) for (let k = j + 1; k < top.length; k++) for (let l = k + 1; l < top.length; l++) {
      const combo = [top[i], top[j], top[k], top[l]], areas = combo.map(c => c.a), big = Math.max(...areas);
      const rest = areas.slice().sort((x, y) => x - y).slice(0, 3), mean = rest.reduce((x, y) => x + y) / 3;
      if (Math.max(...rest) / Math.min(...rest) > 1.6 || !(big / mean > 1.6 && big / mean < 3.6)) continue;
      const quad = hullArea(combo.map(c => c.p));
      if (quad >= 0.15 * w * h) scored.push({ quad, combo });
    }
    scored.sort((x, y) => y.quad - x.quad);
    return scored.map(({ combo }) => {
      const best = combo.slice().sort((x, y) => y.a - x.a), tl = best[0], rest = best.slice(1);
      const ctr = [0, 1].map(d => (tl.p[d] + rest.reduce((s, r) => s + r.p[d], 0)) / 4);
      const ang = p => Math.atan2(p[1] - ctr[1], p[0] - ctr[0]), a0 = ang(tl.p), T = 2 * Math.PI;
      rest.sort((x, y) => ((ang(x.p) - a0) % T + T) % T - ((ang(y.p) - a0) % T + T) % T);
      const seq = [tl, ...rest]; return { pts: seq.map(c => c.p), areas: seq.map(c => c.a) };
    });
  }
  function hullArea(P) { // area poligon konveks 4 titik: urutkan menurut sudut
    const c = [0, 1].map(d => P.reduce((s, p) => s + p[d], 0) / P.length);
    const S = P.slice().sort((a, b) => Math.atan2(a[1] - c[1], a[0] - c[0]) - Math.atan2(b[1] - c[1], b[0] - c[0]));
    let a = 0; for (let i = 0; i < S.length; i++) { const p = S[i], q = S[(i + 1) % S.length]; a += p[0] * q[1] - q[0] * p[1]; }
    return Math.abs(a) / 2;
  }
  function homography(src, dst) { // 8x8 Gauss
    const A = [], B = [];
    for (let i = 0; i < 4; i++) { const [x, y] = src[i], [u, v] = dst[i];
      A.push([x, y, 1, 0, 0, 0, -u * x, -u * y]); B.push(u); A.push([0, 0, 0, x, y, 1, -v * x, -v * y]); B.push(v); }
    const n = 8; for (let i = 0; i < n; i++) A[i].push(B[i]);
    for (let c = 0; c < n; c++) { let p = c; for (let r = c + 1; r < n; r++) if (Math.abs(A[r][c]) > Math.abs(A[p][c])) p = r;
      if (Math.abs(A[p][c]) < 1e-12) return null; [A[c], A[p]] = [A[p], A[c]];
      for (let r = 0; r < n; r++) if (r !== c) { const f = A[r][c] / A[c][c]; for (let k = c; k <= n; k++) A[r][k] -= f * A[c][k]; } }
    const h = A.map((r, i) => r[n] / r[i]); return [...h, 1];
  }
  const apply = (H, x, y) => { const d = H[6] * x + H[7] * y + H[8]; return [(H[0] * x + H[1] * y + H[2]) / d, (H[3] * x + H[4] * y + H[5]) / d]; };
  function sample(g, w, h, x, y) {
    x = Math.min(Math.max(x, 0), w - 1.001); y = Math.min(Math.max(y, 0), h - 1.001);
    const x0 = Math.floor(x), y0 = Math.floor(y), fx = x - x0, fy = y - y0, i = y0 * w + x0;
    return g[i] * (1 - fx) * (1 - fy) + g[i + 1] * fx * (1 - fy) + g[i + w] * (1 - fx) * fy + g[i + w + 1] * fx * fy;
  }
  function disc(cx, cy, r0, r1, n = 14, rings = 3) {
    const out = []; for (let k = 0; k < rings; k++) { const rr = rings === 1 ? r0 : r0 + (r1 - r0) * k / (rings - 1);
      for (let j = 0; j < n; j++) { const a = 2 * Math.PI * j / n; out.push([cx + rr * Math.cos(a), cy + rr * Math.sin(a)]); } }
    return out;
  }
  const median = a => { const s = a.slice().sort((x, y) => x - y), m = s.length >> 1; return s.length % 2 ? s[m] : (s[m - 1] + s[m]) / 2; };
  function bubble(q, o) { return [TPL.COL_X[(q / TPL.ROWS) | 0] + o * TPL.OPT_DX, TPL.ROW0 + (q % TPL.ROWS) * TPL.ROW_DY]; }

  function sizesConsistent(H, areas) {
    for (let i = 0; i < 4; i++) { const [cx, cy, size] = TPL.MARKERS[ORDER[i]];
      const o = apply(H, cx, cy), ex = apply(H, cx + 1, cy), ey = apply(H, cx, cy + 1);
      const pred = Math.abs((ex[0] - o[0]) * (ey[1] - o[1]) - (ex[1] - o[1]) * (ey[0] - o[0])) * size * size, r = areas[i] / pred;
      if (!(r > 0.5 && r < 1.9)) return false; }
    return true;
  }
  function registrationScore(g, w, h, H, K, nq) {
    const r = TPL.BUB_D / 2, vals = [];
    for (let q = 0; q < nq; q++) for (let o = 0; o < 5; o++) {
      const [bx, by] = bubble(q, o), S = (pts) => pts.map(p => { const t = apply(H, p[0], p[1]); return sample(g, w, h, t[0], t[1]); });
      const P = median(S(disc(bx, by, 1.45 * r, 1.6 * r, 16, 2)));
      let ring = 1e9; for (const f of [0.85, 0.93, 1.0, 1.07, 1.15]) { const v = S(disc(bx, by, f * r, f * r, 16, 1)), mu = v.reduce((a, b) => a + b) / v.length; if (mu < ring) ring = mu; }
      vals.push((P - ring) / Math.max(P - K, 20));
    }
    return median(vals);
  }

  function readSheet(img, opts = {}) {
    const { data: g, w, h } = img, nq = Math.min(TPL.N_Q, Math.max(1, opts.n || TPL.N_Q)), regMin = opts.regMin == null ? REG_MIN : opts.regMin;
    const sets = findMarkers(g, w, h);
    if (!sets) return { ok: false, reason: 'marka sudut tidak ditemukan' };
    const tpl = ORDER.map(k => [TPL.MARKERS[k][0], TPL.MARKERS[k][1]]);
    let best = null;
    for (const { pts, areas } of sets.slice(0, 6)) {
      const H = homography(tpl, pts); if (!H || !sizesConsistent(H, areas)) continue;
      const blacks = [1, 2, 3].map(i => median(disc(tpl[i][0], tpl[i][1], 0, 1.8, 8, 3).map(p => { const t = apply(H, p[0], p[1]); return sample(g, w, h, t[0], t[1]); })));
      const K = median(blacks), score = registrationScore(g, w, h, H, K, nq);
      if (!best) best = { score, H, K };
      if (score >= regMin) { best = { score, H, K }; break; }
    }
    if (!best) return { ok: false, reason: 'marka tidak konsisten dengan template' };
    if (best.score < regMin) return { ok: false, reason: 'pendaftaran gambar gagal (foto ulang)', reg: best.score };
    const { H, K } = best, r = TPL.BUB_D / 2, S = pts => pts.map(p => { const t = apply(H, p[0], p[1]); return sample(g, w, h, t[0], t[1]); });
    const questions = [];
    for (let q = 0; q < nq; q++) {
      const fills = [];
      for (let o = 0; o < 5; o++) {
        const [bx, by] = bubble(q, o), inner = S(disc(bx, by, 0, 0.6 * r)), P = median(S(disc(bx, by, 1.35 * r, 1.55 * r, 16, 2)));
        const mi = inner.reduce((a, b) => a + b) / inner.length, den = Math.max(P - K, 20);
        fills.push(Math.min(1, Math.max(0, (P - mi) / den)));
      }
      const marked = [], vague = [];
      fills.forEach((f, i) => { if (f >= T_HI) marked.push(i); else if (f >= T_LO) vague.push(i); });
      let status, answer = null;
      if (marked.length >= 2) status = 'multiple';
      else if (marked.length === 1 && !vague.length) { status = 'detected'; answer = marked[0]; }
      else if (!marked.length && !vague.length) status = 'blank';
      else { status = 'ambiguous'; answer = marked.length ? marked[0] : null; }
      questions.push({ status, answer, fills });
    }
    return { ok: true, reg: best.score, questions };
  }
  function toGray(rgba, w, h, maxSide = 2400) { // ImageData -> gray, kecilkan bila terlalu besar
    const sc = Math.min(1, maxSide / Math.max(w, h)), W = Math.round(w * sc), H = Math.round(h * sc), g = new Uint8Array(W * H);
    for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) { const i = 4 * (Math.min(h - 1, Math.round(y / sc)) * w + Math.min(w - 1, Math.round(x / sc)));
      g[y * W + x] = (rgba[i] * 299 + rgba[i + 1] * 587 + rgba[i + 2] * 114) / 1000; }
    return { data: g, w: W, h: H };
  }
  root.OMR = { readSheet, toGray, TPL, T_HI, T_LO, REG_MIN };
})(typeof window !== 'undefined' ? window : globalThis);
