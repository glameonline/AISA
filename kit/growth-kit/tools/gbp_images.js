// Render Google Business Profile images. Usage: node tools/gbp_images.js
const { chromium } = require('playwright');
const O = '#f26a1b', BG = '#0b0b0b', CARD = '#1b1d22', T = '#ffffff', M = '#a7adb8', D = 'outputs/gbp-images';
const svg = (w, h, body) => `<svg xmlns="http://www.w3.org/2000/svg" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}" font-family="Arial,Helvetica,sans-serif"><rect width="${w}" height="${h}" fill="${BG}"/>${body}</svg>`;
const lines = (x, y, arr, size, fill = T, lh = 1.15, weight = 700) => arr.map((s, i) => `<text x="${x}" y="${y + i * size * lh}" fill="${fill}" font-size="${size}" font-weight="${weight}">${s}</text>`).join('');
const pill = (x, y, w, label) => `<rect x="${x}" y="${y}" width="${w}" height="80" rx="40" fill="${O}"/><text x="${x + w / 2}" y="${y + 52}" fill="#fff" font-size="30" font-weight="700" text-anchor="middle">${label}</text>`;
const post = (title, sub, cta, art, ctaW = 380) => svg(1200, 900, `<rect width="1200" height="10" fill="${O}"/>
<text x="70" y="100" fill="${O}" font-size="28" font-weight="700" letter-spacing="3">CONTENTFELLOW</text>
${lines(70, 230, title, 64)}${lines(70, 230 + title.length * 74 + 30, sub, 30, M, 1.35, 400)}
${pill(70, 690, ctaW, cta)}<text x="70" y="830" fill="${M}" font-size="24">contentfellow.com · Burnley, Lancashire</text>${art}`);
const chat = `<rect x="700" y="170" width="440" height="460" rx="24" fill="${CARD}"/>
<rect x="730" y="200" width="380" height="60" rx="16" fill="#2a2d34"/><text x="750" y="238" fill="${T}" font-size="20">Best agency near me?</text>
<text x="730" y="305" fill="${M}" font-size="18">AI answer:</text>
${['1. Competitor A', '2. Competitor B', '3. You?'].map((s, i) => `<rect x="730" y="${325 + i * 80}" width="380" height="60" rx="12" fill="${i == 2 ? O : '#2a2d34'}"/><text x="750" y="${363 + i * 80}" fill="#fff" font-size="22" font-weight="700">${s}</text>`).join('')}`;
const browser = `<rect x="720" y="180" width="420" height="420" rx="20" fill="${CARD}"/><rect x="720" y="180" width="420" height="44" rx="20" fill="#2a2d34"/>
${[0, 1, 2].map(i => `<circle cx="${748 + i * 24}" cy="202" r="7" fill="${i ? '#555' : O}"/>`).join('')}
<rect x="750" y="250" width="360" height="130" rx="12" fill="${O}"/><rect x="750" y="400" width="220" height="18" rx="9" fill="#3a3d44"/><rect x="750" y="432" width="300" height="18" rx="9" fill="#3a3d44"/>
<rect x="750" y="480" width="170" height="90" rx="12" fill="#2a2d34"/><rect x="940" y="480" width="170" height="90" rx="12" fill="#2a2d34"/>`;
const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'];
const cal = `<rect x="690" y="170" width="460" height="440" rx="24" fill="${CARD}"/>${days.map((d, i) => `<text x="${722 + i * 86}" y="220" fill="${M}" font-size="18">${d}</text>${[0, 1, 2].map(j => `<rect x="${715 + i * 86}" y="${240 + j * 115}" width="72" height="100" rx="12" fill="${(i + j) % 2 ? O : '#2a2d34'}"/><text x="${751 + i * 86}" y="${296 + j * 115}" fill="#fff" font-size="16" text-anchor="middle">${['Post', 'Reel', 'Story'][(i + j) % 3]}</text>`).join('')}`).join('')}`;
const cam = `<rect x="720" y="250" width="420" height="270" rx="30" fill="${CARD}" stroke="${O}" stroke-width="4"/><rect x="820" y="210" width="140" height="50" rx="12" fill="${CARD}" stroke="${O}" stroke-width="4"/>
<circle cx="930" cy="385" r="95" fill="#2a2d34" stroke="${O}" stroke-width="8"/><circle cx="930" cy="385" r="45" fill="${BG}"/><circle cx="1090" cy="295" r="12" fill="${O}"/>`;
const gift = `<rect x="740" y="240" width="380" height="330" rx="24" fill="${CARD}" stroke="${O}" stroke-width="4"/>
<text x="930" y="400" fill="${O}" font-size="150" font-weight="700" text-anchor="middle">7</text><text x="930" y="470" fill="${T}" font-size="40" font-weight="700" text-anchor="middle">DAYS FREE</text>
<text x="930" y="520" fill="${M}" font-size="22" text-anchor="middle">no card needed</text>`;
const price = (big, small) => `<rect x="720" y="230" width="420" height="340" rx="24" fill="${CARD}" stroke="${O}" stroke-width="4"/>
<text x="930" y="420" fill="${O}" font-size="120" font-weight="700" text-anchor="middle">${big}</text><text x="930" y="490" fill="${T}" font-size="34" font-weight="700" text-anchor="middle">${small}</text>`;
const S = {
  logo: [720, 720, svg(720, 720, `<rect x="60" y="60" width="600" height="600" rx="120" fill="${O}"/>
<text x="360" y="455" fill="#fff" font-size="300" font-weight="700" text-anchor="middle" letter-spacing="-10">CF</text>
<rect x="210" y="520" width="300" height="14" rx="7" fill="${BG}"/>`)],
  cover: [1024, 576, svg(1024, 576, `<rect width="1024" height="10" fill="${O}"/>
<text x="60" y="90" fill="${O}" font-size="26" font-weight="700" letter-spacing="3">CONTENTFELLOW</text>
${lines(60, 190, ['Marketing agency', 'in Burnley'], 64)}
${lines(60, 335, ['Content, websites, social &amp; Google/AI search', 'on simple monthly plans'], 28, M, 1.35, 400)}
<rect x="60" y="440" width="330" height="70" rx="35" fill="${O}"/><text x="225" y="485" fill="#fff" font-size="28" font-weight="700" text-anchor="middle">contentfellow.com</text>
<circle cx="860" cy="250" r="110" fill="none" stroke="${O}" stroke-width="16"/><text x="860" y="285" fill="#fff" font-size="100" font-weight="700" text-anchor="middle">CF</text>`)],
  'post-ai-check': [1200, 900, post(['Does ChatGPT', 'recommend your', 'business?'], ['Free AI visibility check: see if', 'ChatGPT, Claude &amp; Gemini mention you'], 'Get free check →', chat)],
  'post-search-fellow': [1200, 900, post(['Get found on', 'Google and AI'], ['Search Fellow: SEO + GEO', 'Monthly ranking + AI visibility report'], 'See Search Fellow →', price('£89', 'per month'), 420)],
  'post-websites': [1200, 900, post(['Pay-monthly', 'websites'], ['Build Fellow from £69/month', 'or a Launch website for £349', '(up to 7 pages)'], 'Get a website →', browser)],
  'post-social': [1200, 900, post(['Social media,', 'managed monthly'], ['Social Fellow from £59/month', 'Manage + Post £129/month'], 'See Social Fellow →', cal, 420)],
  'post-studio': [1200, 900, post(['Video &amp; photo', 'shoots in', 'Lancashire'], ['Studio Fellow £149/month: 1 on-site shoot,', '4K video + 20 edited photos'], 'Book a shoot →', cam)],
  'post-free-trial': [1200, 900, post(['Try us free', 'for 7 days'], ['Free AI visibility check included', 'contentfellow.com/ai-check'], 'Start free trial →', gift, 400)],
};
(async () => {
  const b = await chromium.launch(); const p = await b.newPage();
  for (const [k, [w, h, s]] of Object.entries(S)) { await p.setViewportSize({ width: w, height: h }); await p.setContent(`<body style="margin:0">${s}</body>`); await p.screenshot({ path: `${D}/${k}.png` }); }
  await b.close();
})();
