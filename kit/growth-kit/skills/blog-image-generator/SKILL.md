---
name: blog-image-generator
description: Creates a featured image (1200x630) and 1–2 supporting images (charts/diagrams) for a post, with SEO file names and alt text. Uses Canva generate-image when connected, otherwise renders on-brand SVG→PNG locally.
---
# Blog Image Generator
- Featured: 1200×630, title text, brand colours (ContentFellow dark #0c0c0d + accent). File: `<slug>-featured.png`.
- Supporting: a data chart of the article's key table and/or a process diagram. File: `<slug>-<what-it-shows>.png`.
- Preferred engine: local SVG → PNG via headless Chromium (deterministic, no credits, exact numbers). Canva `generate-image` for photographic heroes when wanted.
- Write alt text (≤ 125 chars, describes content + keyword naturally) into `content/meta.json` images[].
- Keep each PNG < 200 KB; also export WebP if the host supports it.
