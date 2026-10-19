// Render the 1200x600 outreach email graphics. Usage: node tools/outreach_images.js
const { chromium } = require('playwright'); const fs = require('fs');
const O = '#f26a1b', BG = '#0c0c0d', CARD = '#1b1d22', T = '#ffffff', M = '#a7adb8';
const wrap = (title, sub, art) => `<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="600" viewBox="0 0 1200 600" font-family="Arial,Helvetica,sans-serif">
<rect width="1200" height="600" fill="${BG}"/><rect x="0" y="0" width="1200" height="8" fill="${O}"/>
<text x="60" y="80" fill="${O}" font-size="24" font-weight="700" letter-spacing="2">CONTENTFELLOW</text>
<text x="60" y="190" fill="${T}" font-size="54" font-weight="700">${title[0]}</text><text x="60" y="255" fill="${T}" font-size="54" font-weight="700">${title[1]}</text>
<text x="60" y="320" fill="${M}" font-size="26">${sub}</text>
<rect x="60" y="440" width="330" height="76" rx="38" fill="${O}"/><text x="225" y="489" fill="#fff" font-size="28" font-weight="700" text-anchor="middle">Claim free trial →</text>
<text x="60" y="560" fill="${M}" font-size="20">7 days free · no card · cancel any time</text>${art}</svg>`;
const chat = `<rect x="690" y="90" width="460" height="420" rx="24" fill="${CARD}"/>
<rect x="730" y="130" width="380" height="60" rx="16" fill="#2a2d34"/><text x="750" y="168" fill="${T}" font-size="20">Who's the best firm near me?</text>
<text x="730" y="235" fill="${M}" font-size="18">AI answer:</text>
${[['1. Competitor A', 0], ['2. Competitor B', 1], ['3. You?', 2]].map(([s, i]) => `<rect x="730" y="${255 + i * 70}" width="380" height="54" rx="12" fill="${i == 2 ? O : '#2a2d34'}"/><text x="750" y="${290 + i * 70}" fill="#fff" font-size="22" font-weight="700">${s}</text>`).join('')}`;
const reel = `${[0, 1, 2].map(i => `<rect x="${700 + i * 160}" y="${110 + (i % 2) * 40}" width="140" height="250" rx="18" fill="${CARD}" stroke="${i == 1 ? O : '#333'}" stroke-width="3"/><polygon points="${755 + i * 160},${205 + (i % 2) * 40} ${755 + i * 160},${265 + (i % 2) * 40} ${800 + i * 160},${235 + (i % 2) * 40}" fill="${O}"/>`).join('')}
<rect x="700" y="430" width="440" height="14" rx="7" fill="#2a2d34"/><rect x="700" y="430" width="290" height="14" rx="7" fill="${O}"/><text x="700" y="480" fill="${M}" font-size="20">8 short videos + 1 motion graphic a month</text>`;
const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'];
const cal = `<rect x="680" y="100" width="470" height="400" rx="24" fill="${CARD}"/>${days.map((d, i) => `<text x="${720 + i * 88}" y="150" fill="${M}" font-size="18">${d}</text>${[0, 1, 2].map(j => `<rect x="${710 + i * 88}" y="${170 + j * 105}" width="74" height="90" rx="12" fill="${(i + j) % 2 ? O : '#2a2d34'}"/><text x="${747 + i * 88}" y="${222 + j * 105}" fill="#fff" font-size="16" text-anchor="middle">${['Post', 'Reel', 'Story'][(i + j) % 3]}</text>`).join('')}`).join('')}`;
const cam = `<rect x="700" y="170" width="420" height="270" rx="30" fill="${CARD}" stroke="${O}" stroke-width="4"/><rect x="800" y="130" width="140" height="50" rx="12" fill="${CARD}" stroke="${O}" stroke-width="4"/>
<circle cx="910" cy="305" r="95" fill="#2a2d34" stroke="${O}" stroke-width="8"/><circle cx="910" cy="305" r="45" fill="${BG}"/><circle cx="1070" cy="215" r="12" fill="${O}"/>
<text x="700" y="490" fill="${M}" font-size="20">1 on-site shoot · 20 edited photos · 4K video</text>`;
const wl = `<rect x="690" y="110" width="200" height="300" rx="20" fill="${CARD}"/><text x="790" y="250" fill="${M}" font-size="22" text-anchor="middle">We edit</text>
<text x="925" y="270" fill="${O}" font-size="60" text-anchor="middle">→</text>
<rect x="960" y="110" width="200" height="300" rx="20" fill="${O}"/><text x="1060" y="240" fill="#fff" font-size="22" font-weight="700" text-anchor="middle">Your brand</text><text x="1060" y="275" fill="#fff" font-size="18" text-anchor="middle">your price</text>
<text x="690" y="470" fill="${M}" font-size="20">30 videos £249/mo · no ContentFellow branding</text>`;
const S = {
  search: wrap(['Does ChatGPT', 'recommend you?'], 'Search Fellow: SEO + GEO · £89/month', chat),
  creator: wrap(['Turn visitors', 'into enquiries'], 'Creator Fellow: short videos · £119/month', reel),
  social: wrap(['Look active,', 'every weekday'], 'Social Fellow: managed social · from £59/month', cal),
  studio: wrap(['Show your best', 'work properly'], 'Studio Fellow: photo + video shoot · £149/month', cam),
  partner: wrap(['White-label', 'video for agencies'], 'Ready-edited Reels, TikToks & podcasts', wl),
};
(async () => {
  const b = await chromium.launch(); const p = await b.newPage(); await p.setViewportSize({ width: 1200, height: 600 });
  for (const [k, svg] of Object.entries(S)) { await p.setContent(`<body style="margin:0">${svg}</body>`); await p.screenshot({ path: `outputs/_site/img/outreach/${k}.png` }); }
  await b.close();
})();
