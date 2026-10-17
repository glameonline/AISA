// Why ContentFellow: pure function of time. window.seek(t) paints frame t (see lib/motion.js).
// Story: the problem (0-10 s) -> what you actually need (10-16.9 s) -> what ContentFellow offers
// (drop at 16.88 s) -> end card. Scenes are timed in seconds against the VO words (vo_words.json);
// docs/shotlist.md is the plan.
import * as M from './lib/motion.js';

const { W, H, E, prog, lerp, clamp, spring, SPRING, font, layout, fitSize, glyph, text, fill, rrect, hash01, noise1, kf, mulberry32 } = M;

// Brand tokens from contentfellow.com (Firecrawl branding + screenshots). One accent: the orange.
const C = { bg: '#0C0C0D', card: '#18181A', line: 'rgba(243,243,245,0.12)', ink: '#F3F3F5', mute: '#9A9AA2', acc: '#F26A1B', dark: '#0C0C0D' };
const D = 'Display', UI = 'UI';
const X0 = 72, XW = 858;                       // 9x16 safe column (clear of the Reels buttons)

// grid (beats.json): 127.996 bpm, offset 1 ms. HITS are written in seconds and converted to beats.
const PER = 60 / 127.996, OFF = 0.001;
const HS = [
  [0.0, 'sub', { len: 0.8 }], [0.57, 'click'], [0.87, 'pop', { pitch: 'E5' }],
  [1.83, 'tok', { pitch: 'E5' }], [2.47, 'tok', { pitch: 'G5' }], [3.19, 'tok', { pitch: 'A5' }], [4.11, 'tok', { pitch: 'B5' }],
  [5.6, 'whoosh', { len: 0.4 }], [5.97, 'thud'], [6.75, 'coins'], [7.45, 'tick'], [7.73, 'thud'],
  ...[0, 1, 2, 3, 4, 5, 6].map((i) => [8.73 + i * 0.12, 'tick']),
  [10.2, 'whoosh', { len: 0.45 }], [11.72, 'click'], [12.02, 'pop', { pitch: 'B5' }],
  ...[0, 1, 2, 3].map((i) => [12.8 + i * 0.14, 'blip', { pitch: ['E6', 'F#6', 'G#6', 'B6'][i] }]),
  [13.5, 'whoosh', { len: 0.35, from: 400, to: 1500 }], [13.62, 'thud'],
  [15.04, 'whoosh', { len: 0.25, from: 2600, to: 700 }], [15.22, 'whoosh', { len: 0.25, from: 2600, to: 700 }], [15.3, 'thud'],
  [16.88, 'riser', { len: 1.3 }], [16.88, 'impact'], [17.3, 'bell', { pitch: 'E6' }],
  [17.65, 'whoosh', { len: 0.4 }], [19.1, 'tok', { pitch: 'E5' }], [19.76, 'tok', { pitch: 'F#5' }], [20.46, 'tok', { pitch: 'G#5' }],
  [21.12, 'tok', { pitch: 'A5' }], [21.76, 'tok', { pitch: 'B5' }],
  [22.2, 'whoosh', { len: 0.4 }], [22.44, 'thud'], [23.95, 'coins'], [23.95, 'bell', { pitch: 'E6' }], [24.1, 'click'],
  [24.55, 'whoosh', { len: 0.4 }], [25.05, 'whoosh', { len: 0.35, from: 400, to: 1800 }], [25.58, 'impact'],
  [26.3, 'pop', { pitch: 'G5' }], [27.64, 'click'], [27.7, 'bell', { pitch: 'B5' }], [28.0, 'blip', { pitch: 'E6' }],
  [28.3, 'whoosh', { len: 0.4 }], [28.5, 'bell', { pitch: 'E6' }], [28.7, 'thud'], [29.3, 'pop', { pitch: 'B5' }],
];
const HITS = HS.map(([s, sfx, o]) => [(s - OFF) / PER, `${sfx} @${s}s`, sfx, o || {}]);

// ---------------------------------------------------------------- helpers (time in seconds)
const S = (t, t0, cfg = SPRING.snappy) => spring(t - t0, cfg);
function skeys(t, keys, cfg = SPRING.snappy) {
  let v = keys[0][1];
  for (let i = 1; i < keys.length; i++) {
    const k = S(t, keys[i][0], cfg);
    if (k === 0) break;
    v += (keys[i][1] - keys[i - 1][1]) * k;
  }
  return v;
}
// Kinetic type: each glyph springs up out of a mask at its baseline, a touch after the last.
function typeIn(ctx, str, x, y, f, color, t, t0, { stagger = 0.022, align = 'left', track = 0, cfg = SPRING.snappy } = {}) {
  const L = layout(ctx, str, f, track);
  const x0 = align === 'center' ? x - L.width / 2 : x;
  if (t < t0) return L;
  ctx.save();
  ctx.beginPath(); ctx.rect(0, y - L.asc * 1.4, W, L.asc * 1.4 + L.desc + 14); ctx.clip();
  L.glyphs.forEach((g, j) => {
    const k = S(t, t0 + j * stagger, cfg);
    if (k > 0) glyph(ctx, g.ch, x0 + g.cx, y + (1 - k) * L.asc * 1.15, f, color);
  });
  ctx.restore();
  return L;
}
const fitD = (ctx, strs, max, w = XW, weight = 800) => Math.min(...strs.map((s) => fitSize(ctx, s, weight, D, w, max, -0.02)));
// A real screenshot as a floating card.
function card(ctx, img, cx, cy, w, { rot = 0, s = 1, a = 1, r = 22 } = {}) {
  if (!img || a <= 0.001 || s <= 0.001) return;
  const h = (w * img.height) / img.width;
  ctx.save(); ctx.globalAlpha *= a; ctx.translate(cx, cy); ctx.rotate(rot); ctx.scale(s, s);
  rrect(ctx, -w / 2 + 8, -h / 2 + 28, w, h, r); ctx.fillStyle = 'rgba(0,0,0,0.55)'; ctx.fill();
  ctx.save(); rrect(ctx, -w / 2, -h / 2, w, h, r); ctx.clip(); ctx.drawImage(img, -w / 2, -h / 2, w, h); ctx.restore();
  rrect(ctx, -w / 2, -h / 2, w, h, r); ctx.strokeStyle = 'rgba(255,255,255,0.12)'; ctx.lineWidth = 2; ctx.stroke();
  ctx.restore();
}
function pill(ctx, cx, cy, w, h, color, stroke) {
  rrect(ctx, cx - w / 2, cy - h / 2, w, h, h / 2); ctx.fillStyle = color; ctx.fill();
  if (stroke) { ctx.strokeStyle = stroke; ctx.lineWidth = 2; ctx.stroke(); }
}
function tick(ctx, x, y, s, p, color, lw = 10) {           // a hand-drawn check, p = 0..1 drawn
  const pts = [[-0.45, 0.02], [-0.12, 0.34], [0.5, -0.32]];
  const l1 = Math.hypot(0.33, 0.32), l2 = Math.hypot(0.62, 0.66), d = p * (l1 + l2);
  ctx.save(); ctx.translate(x, y); ctx.scale(s, s);
  ctx.strokeStyle = color; ctx.lineWidth = lw / s; ctx.lineCap = 'round'; ctx.lineJoin = 'round';
  ctx.beginPath(); ctx.moveTo(...pts[0]);
  if (d <= l1) ctx.lineTo(lerp(pts[0][0], pts[1][0], d / l1), lerp(pts[0][1], pts[1][1], d / l1));
  else { ctx.lineTo(...pts[1]); const q = (d - l1) / l2; ctx.lineTo(lerp(pts[1][0], pts[2][0], q), lerp(pts[1][1], pts[2][1], q)); }
  ctx.stroke(); ctx.restore();
}
// Tiny line icons for the to-do list (shape only, no fonts needed).
function icon(ctx, kind, x, y, s, color) {
  ctx.save(); ctx.translate(x, y); ctx.strokeStyle = color; ctx.fillStyle = color; ctx.lineWidth = 4; ctx.lineJoin = 'round'; ctx.lineCap = 'round';
  if (kind === 'video') { rrect(ctx, -s, -s * 0.7, s * 2, s * 1.4, 6); ctx.stroke(); ctx.beginPath(); ctx.moveTo(-s * 0.3, -s * 0.38); ctx.lineTo(s * 0.45, 0); ctx.lineTo(-s * 0.3, s * 0.38); ctx.closePath(); ctx.fill(); }
  if (kind === 'posts') { for (let i = 0; i < 4; i++) { rrect(ctx, (i % 2 ? 0.1 : -1) * s, (i > 1 ? 0.1 : -1) * s, s * 0.9, s * 0.9, 4); ctx.stroke(); } }
  if (kind === 'web') { rrect(ctx, -s, -s * 0.8, s * 2, s * 1.6, 6); ctx.stroke(); ctx.beginPath(); ctx.moveTo(-s, -s * 0.35); ctx.lineTo(s, -s * 0.35); ctx.stroke(); }
  if (kind === 'search') { ctx.beginPath(); ctx.arc(-s * 0.15, -s * 0.15, s * 0.6, 0, M.TAU); ctx.stroke(); ctx.beginPath(); ctx.moveTo(s * 0.3, s * 0.3); ctx.lineTo(s * 0.85, s * 0.85); ctx.stroke(); }
  ctx.restore();
}

// ---------------------------------------------------------------- background
function bg(ctx, t) {
  fill(ctx, C.bg);
  ctx.save(); ctx.strokeStyle = 'rgba(255,255,255,0.035)'; ctx.lineWidth = 1.5;
  const gs = 120, oy = (t * 14) % gs;
  ctx.beginPath();
  for (let x = 60; x < W; x += gs) { ctx.moveTo(x, 0); ctx.lineTo(x, H); }
  for (let y = oy - gs; y < H; y += gs) { ctx.moveTo(0, y); ctx.lineTo(W, y); }
  ctx.stroke(); ctx.restore();
  const drop = S(t, 16.88, SPRING.gentle);
  const gy = kf(t, [[0, 1650], [10, 1450], [16.8, 900], [22, 1500], [28.3, 900]]);
  const gi = 0.16 + 0.16 * drop + 0.25 * Math.exp(-Math.max(0, t - 16.88) * 3) * (t > 16.88);
  const g = ctx.createRadialGradient(W / 2, gy, 0, W / 2, gy, 1000);
  g.addColorStop(0, `rgba(242,106,27,${gi})`); g.addColorStop(1, 'rgba(242,106,27,0)');
  ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);
  for (let i = 0; i < 12; i++) {                 // soft lens bokeh, as on the site's hero
    const r = 30 + hash01(i, 11) * 90;
    const x = hash01(i, 3) * W + noise1(t * 0.2 + i * 7, 5) * 60;
    const y = ((hash01(i, 5) * (H + 400) - t * (14 + hash01(i, 9) * 30)) % (H + 400) + H + 400) % (H + 400) - 200;
    const a = (0.04 + hash01(i, 13) * 0.07) * (0.6 + 0.4 * drop);
    const b = ctx.createRadialGradient(x, y, 0, x, y, r);
    b.addColorStop(0, `rgba(255,140,60,${a})`); b.addColorStop(1, 'rgba(255,140,60,0)');
    ctx.fillStyle = b; ctx.fillRect(x - r, y - r, r * 2, r * 2);
  }
}

// ---------------------------------------------------------------- ACT 1: the problem
const JOBS = [['video', 'Videos', 1.83], ['posts', 'Posts', 2.47], ['web', 'A website', 3.19], ['search', 'Customers finding you', 4.11]];
function sceneBusiness(ctx, t) {
  const out = E.inBack(prog(t, 5.42, 5.85), 1.3) * 1500;
  ctx.save(); ctx.translate(0, -out);
  typeIn(ctx, 'Running a', X0, 470, font(60, 600, UI), C.mute, t, -0.4);
  const sz = fitD(ctx, ['small', 'business?'], 140);
  typeIn(ctx, 'small', X0, 470 + sz * 1.15, font(sz, 800, D), C.ink, t, -0.3);
  typeIn(ctx, 'business?', X0, 470 + sz * 2.3, font(sz, 800, D), C.acc, t, 0.5);
  const top = 470 + sz * 2.3 + 90;
  JOBS.forEach(([ic, label, t0], i) => {
    const k = S(t, t0 - 0.06, SPRING.bouncy);
    if (k <= 0) return;
    const y = top + i * 146, jig = t > 4.4 ? noise1(t * 6 + i * 3, 4) * 3 : 0;
    ctx.save(); ctx.translate(X0 + XW / 2 + (1 - k) * 760, y + 60 + jig); ctx.rotate((1 - k) * 0.12 + jig * 0.002);
    rrect(ctx, -XW / 2, -60, XW, 120, 24); ctx.fillStyle = C.card; ctx.fill(); ctx.strokeStyle = C.line; ctx.lineWidth = 2; ctx.stroke();
    ctx.beginPath(); ctx.arc(-XW / 2 + 64, 0, 40, 0, M.TAU); ctx.fillStyle = 'rgba(242,106,27,0.16)'; ctx.fill();
    icon(ctx, ic, -XW / 2 + 64, 0, 19, C.acc);
    text(ctx, label, -XW / 2 + 130, 20, font(56, 600, UI), C.ink);
    // an empty checkbox on the right: nobody has done it yet
    rrect(ctx, XW / 2 - 78, -22, 44, 44, 10); ctx.strokeStyle = 'rgba(243,243,245,0.35)'; ctx.lineWidth = 3; ctx.stroke();
    ctx.restore();
  });
  ctx.restore();
}

function sceneCost(ctx, t) {
  const enter = 1 - E.outCubic(prog(t, 5.55, 6.0)), exit = E.inOutCubic(prog(t, 10.1, 10.55));
  ctx.save(); ctx.translate(-exit * W, enter * 900);
  typeIn(ctx, 'Agencies', X0, 470, font(fitD(ctx, ['Agencies'], 120), 800, D), C.ink, t, 5.93);
  typeIn(ctx, 'are expensive', X0, 570, font(60, 600, UI), C.mute, t, 6.55);
  for (let i = 0; i < 5; i++) {                  // the bill keeps growing
    const k = S(t, 6.75 + i * 0.09, SPRING.bouncy);
    if (k > 0) glyph(ctx, '£', X0 + 70 + i * 150, 760 + (1 - k) * 80, font(170, 900, D), C.acc, k, k, (1 - k) * 0.5);
  }
  const dl = E.outCubic(prog(t, 7.4, 7.8));
  if (dl > 0) { ctx.fillStyle = C.line; ctx.fillRect(X0, 870, XW * dl, 3); }
  typeIn(ctx, 'Doing it yourself', X0, 1010, font(fitD(ctx, ['Doing it yourself'], 80), 800, D), C.ink, t, 7.7);
  const days = 'MTWTFSS', bw = 110, gap = (XW - bw * 7) / 6;
  for (let i = 0; i < 7; i++) {
    const k = S(t, 7.95 + i * 0.04, SPRING.snappy);
    if (k <= 0) continue;
    const x = X0 + i * (bw + gap), y = 1075 + (1 - k) * 60;
    ctx.save(); ctx.globalAlpha = k;
    rrect(ctx, x, y, bw, 150, 18); ctx.fillStyle = C.card; ctx.fill(); ctx.strokeStyle = C.line; ctx.lineWidth = 2; ctx.stroke();
    const f = E.outCubic(prog(t, 8.73 + i * 0.12, 8.95 + i * 0.12));
    if (f > 0) { ctx.save(); rrect(ctx, x, y, bw, 150, 18); ctx.clip(); ctx.fillStyle = C.acc; ctx.fillRect(x, y + 150 * (1 - f), bw, 150 * f); ctx.restore(); }
    text(ctx, days[i], x + bw / 2, y + 92, font(46, 700, UI), f > 0.5 ? C.dark : C.mute, 'center');
    ctx.restore();
  }
  typeIn(ctx, 'eats your whole week.', X0, 1340, font(64, 600, UI), C.ink, t, 8.73);
  ctx.restore();
}

// ---------------------------------------------------------------- ACT 2: what you really need
const MATCH = [['Videos', 'Video editor'], ['Posts', 'Social manager'], ['Website', 'Web developer'], ['Google', 'SEO specialist']];
function sceneNeed(ctx, t) {
  const enter = 1 - E.inOutCubic(prog(t, 10.1, 10.55));
  ctx.save(); ctx.translate(enter * W, 0);
  typeIn(ctx, 'What you really need is', X0, 440, font(60, 600, UI), C.mute, t, 10.42);
  const sz = fitD(ctx, ['the right', 'expert'], 130);
  typeIn(ctx, 'the right', X0, 440 + sz * 1.2, font(sz, 800, D), C.ink, t, 11.55);
  typeIn(ctx, 'expert', X0, 440 + sz * 2.35, font(sz, 800, D), C.acc, t, 12.0);
  const y0 = 440 + sz * 2.35;
  typeIn(ctx, 'for each job.', X0, y0 + 95, font(60, 600, UI), C.mute, t, 12.56);
  // job -> expert matching: left chips, right chips, a line drawn between each pair
  const dOut = E.inCubic(prog(t, 13.3, 13.65));
  ctx.save(); ctx.globalAlpha = 1 - dOut; ctx.translate(0, dOut * 300);
  MATCH.forEach(([job, pro], i) => {
    const y = y0 + 200 + i * 104, k = S(t, 12.6 + i * 0.06, SPRING.snappy);
    if (k <= 0) return;
    ctx.save(); ctx.globalAlpha *= k;
    pill(ctx, X0 + 130, y, 260, 76, C.card, C.line); text(ctx, job, X0 + 130, y + 16, font(40, 600, UI), C.ink, 'center');
    const lp = E.outCubic(prog(t, 12.8 + i * 0.14, 13.0 + i * 0.14));
    ctx.strokeStyle = C.acc; ctx.lineWidth = 4; ctx.setLineDash([10, 10]);
    ctx.beginPath(); ctx.moveTo(X0 + 268, y); ctx.lineTo(lerp(X0 + 268, X0 + 440, lp), y); ctx.stroke(); ctx.setLineDash([]);
    const pk = S(t, 12.8 + i * 0.14 + 0.18, SPRING.bouncy);
    if (pk > 0) {
      ctx.save(); ctx.translate(X0 + 650, y); ctx.scale(pk, pk);
      pill(ctx, 0, 0, 420, 76, 'rgba(242,106,27,0.16)', C.acc); text(ctx, pro, 0, 15, font(38, 600, UI), C.ink, 'center');
      ctx.restore();
    }
    ctx.restore();
  });
  ctx.restore();
  // "without being locked into a long contract" -> a contract with a padlock, crossed out
  const dk = S(t, 13.5, SPRING.bouncy);
  if (dk > 0) {
    const fall = E.inBack(prog(t, 15.45, 15.95), 1.4);
    const cx = 540, cy = y0 + 400 + (1 - dk) * 900 + fall * 1400, w = 420, h = 470;
    ctx.save(); ctx.translate(cx, cy); ctx.rotate(-0.05 + (1 - dk) * 0.3 + fall * 0.5);
    rrect(ctx, -w / 2 + 10, -h / 2 + 24, w, h, 22); ctx.fillStyle = 'rgba(0,0,0,0.5)'; ctx.fill();
    rrect(ctx, -w / 2, -h / 2, w, h, 22); ctx.fillStyle = C.ink; ctx.fill();
    text(ctx, '12-MONTH CONTRACT', 0, -h / 2 + 70, font(30, 700, UI), C.dark, 'center', 2);
    ctx.fillStyle = 'rgba(12,12,13,0.18)';
    for (let i = 0; i < 6; i++) ctx.fillRect(-w / 2 + 40, -h / 2 + 115 + i * 38, (w - 80) * (i === 5 ? 0.6 : 1), 12);
    // padlock
    ctx.save(); ctx.translate(0, h / 2 - 95); ctx.strokeStyle = C.dark; ctx.lineWidth = 9;
    ctx.beginPath(); ctx.arc(0, -22, 26, Math.PI, 0); ctx.stroke();
    rrect(ctx, -40, -22, 80, 62, 10); ctx.fillStyle = C.dark; ctx.fill(); ctx.restore();
    // the cross
    const a = E.outCubic(prog(t, 14.95, 15.15)), b = E.outCubic(prog(t, 15.13, 15.33));
    ctx.strokeStyle = C.acc; ctx.lineWidth = 26; ctx.lineCap = 'round';
    if (a > 0) { ctx.beginPath(); ctx.moveTo(-w / 2 - 20, -h / 2 - 20); ctx.lineTo(lerp(-w / 2 - 20, w / 2 + 20, a), lerp(-h / 2 - 20, h / 2 + 20, a)); ctx.stroke(); }
    if (b > 0) { ctx.beginPath(); ctx.moveTo(w / 2 + 20, -h / 2 - 20); ctx.lineTo(lerp(w / 2 + 20, -w / 2 - 20, b), lerp(-h / 2 - 20, h / 2 + 20, b)); ctx.stroke(); }
    ctx.restore();
  }
  // "No lock-in." lands in the pause before the brand
  const nk = S(t, 15.75, SPRING.bouncy);
  if (nk > 0) { ctx.save(); ctx.translate(540, y0 + 420); ctx.scale(0.5 + 0.5 * nk, 0.5 + 0.5 * nk); ctx.translate(-540, -(y0 + 420));
    typeIn(ctx, 'No lock-in.', 540, y0 + 420, font(fitD(ctx, ['No lock-in.'], 120), 800, D), C.acc, t, 15.75, { align: 'center' }); ctx.restore(); }
  ctx.restore();
}

// Lens iris from the problem into the brand: the frame closes into the logo's lens.
function iris(ctx, t, draw) {
  const p = E.inCubic(prog(t, 16.25, 16.88));
  const r = lerp(1300, 0, p);
  ctx.save(); ctx.beginPath(); ctx.arc(540, 820, Math.max(r, 0.1), 0, M.TAU); ctx.clip(); draw(); ctx.restore();
  if (p > 0) { ctx.beginPath(); ctx.arc(540, 820, r + 6, 0, M.TAU); ctx.strokeStyle = C.acc; ctx.lineWidth = 12; ctx.stroke(); }
}

// ---------------------------------------------------------------- ACT 3: the offer
// The logo lands on the drop, then parks above the offer as its anchor until the end card.
function logoState(t) {
  const y = skeys(t, [[16.88, 820], [17.6, 330], [28.25, 760]], SPRING.gentle);
  const w = skeys(t, [[16.88, 560], [17.6, 150], [28.25, 300]], SPRING.gentle);
  return { y, w };
}
function sceneLogo(ctx, t, IMG) {
  const k = S(t, 16.88, SPRING.bouncy), rk = S(t, 16.88, SPRING.gentle);
  const { y, w } = logoState(t);
  ctx.save(); M.shake(ctx, (t - OFF) / PER, (16.88 - OFF) / PER, 22);
  if (IMG.logo) {
    const ih = (w * IMG.logo.height) / IMG.logo.width;
    ctx.save(); ctx.translate(540, y); ctx.rotate((1 - rk) * -0.7); ctx.scale(0.25 + 0.75 * k, 0.25 + 0.75 * k);
    ctx.drawImage(IMG.logo, -w / 2, -ih / 2, w, ih); ctx.restore();
  }
  // wordmark under the lens, wiped on, then lifted away as the offer starts
  const wp = E.outQuint(prog(t, 17.25, 17.7)), wo = E.inBack(prog(t, 17.55, 17.9), 1.3);
  if (wp > 0 && wo < 1 && IMG.word) {
    const ww = 820, wh = (ww * IMG.word.height) / IMG.word.width;
    ctx.save(); ctx.beginPath(); ctx.rect(540 - ww / 2, 0, ww * wp, H); ctx.clip();
    ctx.globalAlpha = 1 - wo;
    ctx.drawImage(IMG.word, 540 - ww / 2, 1150 - wo * 900, ww, wh); ctx.restore();
  }
  ctx.restore();
}
function drawLogoParked(ctx, t, IMG) {
  const { y, w } = logoState(t);
  const ih = (w * IMG.logo.height) / IMG.logo.width;
  ctx.drawImage(IMG.logo, 540 - w / 2, y - ih / 2, w, ih);
}

const FELLOWS = [['studio', 'SHOOTING', 19.1], ['creator', 'EDITING', 19.76], ['social', 'SOCIAL', 20.46], ['build', 'WEB', 21.12], ['search', 'SEARCH', 21.76]];
function scenePick(ctx, t, IMG) {
  const out = E.inBack(prog(t, 22.08, 22.45), 1.3);
  ctx.save(); ctx.translate(0, -out * 900);
  const sz = fitD(ctx, ['Pick the Fellows'], 100);
  typeIn(ctx, 'Pick the Fellows', X0, 540, font(sz, 800, D), C.ink, t, 17.68);
  typeIn(ctx, 'you need.', X0, 540 + sz * 1.2, font(sz, 800, D), C.acc, t, 18.44);
  ctx.restore();
  const idx = skeys(t, [[17.7, -2.6], [19.05, 0], [19.72, 1], [20.42, 2], [21.08, 3], [21.72, 4]], SPRING.snappy);
  const drop = E.inBack(prog(t, 22.1, 22.5), 1.4) * 1300;
  const cy = 1220 + drop, cw = 440;
  const order = FELLOWS.map((f, i) => i).sort((a, b) => Math.abs(b - idx) - Math.abs(a - idx));
  for (const i of order) {
    const d = i - idx, ad = Math.min(1, Math.abs(d));
    card(ctx, IMG[FELLOWS[i][0]], 540 + d * 480, cy + ad * 40, cw, { s: 1 - 0.16 * ad, a: 1 - 0.55 * ad, rot: d * 0.05 });
  }
  // the job each Fellow does, on a chip that pops as the narrator names it
  const cur = FELLOWS.reduce((b, f, i) => (t >= f[2] - 0.05 ? i : b), -1);
  if (cur >= 0) {
    const pk = S(t, FELLOWS[cur][2] - 0.05, SPRING.bouncy);
    ctx.save(); ctx.translate(540, cy - 450); ctx.scale(pk, pk);
    const L = layout(ctx, FELLOWS[cur][1], font(42, 700, UI), 3);
    pill(ctx, 0, 0, L.width + 80, 78, C.acc);
    text(ctx, FELLOWS[cur][1], 0, 15, font(42, 700, UI), '#FFFFFF', 'center', 3);
    ctx.restore();
  }
}

function scenePrice(ctx, t) {
  const enter = 1 - E.outCubic(prog(t, 22.25, 22.6)), exit = E.inOutCubic(prog(t, 24.5, 24.9));
  ctx.save(); ctx.translate(-exit * W, enter * 700);
  typeIn(ctx, 'Simple', X0, 560, font(fitD(ctx, ['Monthly plans'], 110), 800, D), C.ink, t, 22.3);
  typeIn(ctx, 'monthly plans', X0, 690, font(fitD(ctx, ['Monthly plans'], 110), 800, D), C.ink, t, 22.44);
  typeIn(ctx, 'from', X0, 820, font(56, 600, UI), C.mute, t, 23.25);
  // odometer: £ then two digit wheels rolling up to 59
  const f = font(280, 900, D), base = 1130;
  const pk = S(t, 23.4, SPRING.snappy);
  if (pk > 0) {
    const L = layout(ctx, '£59', f, -8);
    const lh = 310;
    ctx.save(); ctx.beginPath(); ctx.rect(0, base - 250, W, 295); ctx.clip();
    glyph(ctx, '£', X0 + L.glyphs[0].cx, base + (1 - pk) * 300, f, C.acc);
    [5, 9].forEach((d, j) => {
      const roll = skeys(t, [[23.4, 0], [23.45 + j * 0.08, 10 + d]], { stiffness: 90, damping: 18 });
      for (let n = Math.floor(roll) - 1; n <= Math.floor(roll) + 1; n++) {
        const yy = base - (n - roll) * lh;
        glyph(ctx, String(((n % 10) + 10) % 10), X0 + L.glyphs[j + 1].cx, yy, f, C.acc);
      }
    });
    ctx.restore();
    typeIn(ctx, 'per month', X0 + 8, base + 110, font(64, 600, UI), C.ink, t, 24.05);
  }
  typeIn(ctx, 'Social Fellow · Manage plan', X0 + 8, base + 195, font(44, 500, UI), C.mute, t, 24.15);
  ctx.restore();
}

function sceneTrial(ctx, t, IMG) {
  const enter = 1 - E.inOutCubic(prog(t, 24.5, 24.9)), exit = E.inBack(prog(t, 28.15, 28.45), 1.3);
  ctx.save(); ctx.translate(enter * W, -exit * 1500);
  typeIn(ctx, 'Try any of them', X0, 500, font(58, 600, UI), C.ink, t, 24.64);
  const free = font(fitD(ctx, ['free.'], 250, XW, 900), 900, D);
  ctx.save();
  const sk = S(t, 25.58, SPRING.bouncy);
  if (sk > 0) { ctx.translate(X0, 770); ctx.scale(0.6 + 0.4 * sk, 0.6 + 0.4 * sk); ctx.translate(-X0, -770); }
  typeIn(ctx, 'free.', X0, 770, free, C.acc, t, 25.5, { stagger: 0.03 });
  ctx.restore();
  // the real "Every Fellow has a free trial" panel from the site
  const pk = S(t, 25.05, SPRING.gentle), pout = E.inBack(prog(t, 26.05, 26.4), 1.3);
  if (pk > 0 && pout < 1) card(ctx, IMG.trials, 540, 1080 + (1 - pk) * 900 + pout * 1000, 900, { rot: (1 - pk) * 0.2 + 0.03, a: 1 - pout });
  // approval: button, cursor, click, tick, LIVE
  const bk = S(t, 26.3, SPRING.bouncy);
  if (bk > 0) {
    const press = Math.exp(-Math.max(0, t - 27.64) * 10) * (t > 27.64) * 0.07;
    const on = E.outCubic(prog(t, 27.64, 27.8));
    ctx.save(); ctx.translate(540, 1050); ctx.scale(bk * (1 - press), bk * (1 - press));
    pill(ctx, 0, 0, 560, 140, on > 0 ? M.mix(C.card, C.acc, on) : C.card, on > 0.5 ? null : 'rgba(243,243,245,0.3)');
    if (on < 0.5) text(ctx, 'Approve', 0, 20, font(58, 700, UI), C.ink, 'center');
    else { tick(ctx, -150, 0, 70, E.outCubic(prog(t, 27.72, 27.95)), '#FFFFFF', 12); text(ctx, 'Approved', 40, 20, font(58, 700, UI), '#FFFFFF', 'center'); }
    ctx.restore();
    // cursor glides in and clicks
    const cp = E.inOutCubic(prog(t, 26.75, 27.55));
    const cx = lerp(930, 600, cp), cy = lerp(1560, 1075, cp) + Math.sin(cp * Math.PI) * -60;
    const cs = 1 - press * 2;
    ctx.save(); ctx.translate(cx, cy); ctx.scale(1.6 * cs, 1.6 * cs);
    ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(0, 44); ctx.lineTo(11, 33); ctx.lineTo(19, 50); ctx.lineTo(27, 46); ctx.lineTo(19, 30); ctx.lineTo(34, 30); ctx.closePath();
    ctx.fillStyle = '#FFFFFF'; ctx.fill(); ctx.strokeStyle = C.dark; ctx.lineWidth = 3; ctx.stroke(); ctx.restore();
  }
  const lk = S(t, 28.0, SPRING.bouncy);
  if (lk > 0) {
    ctx.save(); ctx.translate(540, 1215); ctx.scale(lk, lk);
    pill(ctx, 0, 0, 230, 70, C.card, C.line);
    ctx.beginPath(); ctx.arc(-62, 0, 11, 0, M.TAU); ctx.fillStyle = C.acc; ctx.fill();
    text(ctx, 'LIVE', 18, 14, font(38, 700, UI), C.ink, 'center', 4);
    ctx.restore();
  }
  typeIn(ctx, 'Nothing goes live', X0, 1350, font(56, 600, UI), C.ink, t, 26.15);
  typeIn(ctx, 'until you approve it.', X0, 1425, font(56, 600, UI), C.acc, t, 27.1);
  ctx.restore();
}

function sceneEnd(ctx, t, IMG) {
  if (IMG.word) {
    const wp = E.outQuint(prog(t, 28.5, 28.95)), ww = 760, wh = (ww * IMG.word.height) / IMG.word.width;
    ctx.save(); ctx.beginPath(); ctx.rect(540 - ww / 2, 0, ww * wp, H); ctx.clip();
    ctx.drawImage(IMG.word, 540 - ww / 2, 960, ww, wh); ctx.restore();
  }
  const sz = fitD(ctx, ['Your Content. Our Fellows.'], 68, XW, 700);
  typeIn(ctx, 'Your Content. Our Fellows.', 540, 1150, font(sz, 700, D), C.ink, t, 28.7, { align: 'center', stagger: 0.012 });
  typeIn(ctx, 'Your Success.', 540, 1150 + sz * 1.4, font(sz, 700, D), C.acc, t, 28.95, { align: 'center', stagger: 0.02 });
  const ck = S(t, 29.3, SPRING.bouncy);
  if (ck > 0) {
    ctx.save(); ctx.translate(540, 1345); ctx.scale(ck, ck);
    pill(ctx, 0, 0, 560, 110, C.acc);
    text(ctx, 'Start a free trial', 0, 17, font(48, 700, UI), '#FFFFFF', 'center');
    ctx.restore();
  }
  typeIn(ctx, 'contentfellow.com', 540, 1470, font(46, 600, UI), C.mute, t, 29.5, { align: 'center', stagger: 0.012 });
}

// ---------------------------------------------------------------- film
let NOISE = null;
M.film({
  fonts: [font(100, 700, D), font(100, 800, D), font(100, 900, D), font(40, 500, UI), font(40, 600, UI), font(40, 700, UI)],
  images: {
    logo: 'assets/logo_icon_a.png', word: 'assets/wordmark_a.png', trials: 'assets/trials.png',
    studio: 'assets/card_studio.png', creator: 'assets/card_creator.png', social: 'assets/card_social.png',
    build: 'assets/card_build.png', search: 'assets/card_search.png',
  },
  hits: HITS,
  init() {                                        // seeded film grain tile
    NOISE = document.createElement('canvas'); NOISE.width = NOISE.height = 256;
    const c = NOISE.getContext('2d'), im = c.createImageData(256, 256), r = mulberry32(7);
    for (let i = 0; i < im.data.length; i += 4) { const v = r() * 255; im.data[i] = im.data[i + 1] = im.data[i + 2] = v; im.data[i + 3] = 255; }
    c.putImageData(im, 0, 0);
  },
  draw(ctx, u, t, IMG) {
    bg(ctx, t);
    if (t < 16.88) {
      iris(ctx, t, () => {
        ctx.translate(0, 150);                    // sit the story in the middle of the phone
        if (t < 5.9) sceneBusiness(ctx, t);
        if (t > 5.5 && t < 10.6) sceneCost(ctx, t);
        if (t > 10.05) sceneNeed(ctx, t);
      });
      return;
    }
    if (t < 17.95) sceneLogo(ctx, t, IMG); else drawLogoParked(ctx, t, IMG);
    if (t > 17.55 && t < 22.6) scenePick(ctx, t, IMG);
    if (t > 22.2 && t < 24.95) scenePrice(ctx, t);
    if (t > 24.45 && t < 28.5) sceneTrial(ctx, t, IMG);
    if (t > 28.3) sceneEnd(ctx, t, IMG);
  },
  post(ctx, u, t) {
    if (!NOISE) return;
    const f = Math.floor(t * 60), r = mulberry32(f + 1);
    ctx.save(); ctx.globalAlpha = 0.05; ctx.globalCompositeOperation = 'overlay';
    ctx.fillStyle = ctx.createPattern(NOISE, 'repeat');
    ctx.translate(-r() * 256, -r() * 256); ctx.fillRect(0, 0, W + 256, H + 256);
    ctx.restore();
  },
});
