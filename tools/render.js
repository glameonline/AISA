// Render SVG images to PNG and screenshot the article. Usage: node tools/render.js <post_dir>
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
(async () => {
  const d = path.resolve(process.argv[2]); const b = await chromium.launch(); const p = await b.newPage();
  for (const f of fs.readdirSync(`${d}/images`).filter(f => f.endsWith('.svg'))) {
    await p.setViewportSize({ width: 1200, height: 630 });
    await p.goto('file://' + `${d}/images/${f}`);
    await p.screenshot({ path: `${d}/images/${f.replace('.svg', '.png')}` });
  }
  fs.mkdirSync(`${d}/screenshots`, { recursive: true });
  for (const f of fs.readdirSync(`${d}/images`).filter(f => f.endsWith('.png'))) fs.copyFileSync(`${d}/images/${f}`, `${d}/content/${f}`);
  await p.setViewportSize({ width: 1280, height: 900 });
  await p.goto('file://' + `${d}/content/article.html`);
  await p.screenshot({ path: `${d}/screenshots/article-full.png`, fullPage: true });
  await b.close();
})();
