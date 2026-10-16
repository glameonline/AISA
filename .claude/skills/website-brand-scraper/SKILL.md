---
name: website-brand-scraper
description: Reads contentfellow.com (or any own site) to capture brand voice, services, prices, FAQs and internal link targets, saved to outputs/_brand/brand.md so every post sounds on-brand and links correctly.
---
# Website Brand Scraper
1. If `outputs/_brand/brand.md` exists and is < 7 days old, use it and stop.
2. `firecrawl_scrape` the homepage (`formats: ["markdown","links"]`, `onlyMainContent: false`). Direct curl may be blocked by the sandbox proxy; Firecrawl works.
3. Extract into brand.md: one-line positioning; voice rules (tone, spelling = British English, sentence length);
   every service with price + deliverables; FAQ answers (reusable as citations); internal link targets (anchors/URLs) with suggested anchor text; CTAs.
4. Never invent prices or claims. Quote the site.
