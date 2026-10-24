---
name: blog-writer-seo-aeo-geo
description: Writes the full blog post from the brief, keywords, competitor gaps and brand file — optimised for Google (SEO), answer boxes/voice (AEO) and ChatGPT, Claude, Gemini, Perplexity citations (GEO). Outputs article.md, meta.json and a publish-ready article.html with JSON-LD.
---
# Blog Writer (SEO + AEO + GEO)
## Required parts
- Title (H1) containing the primary keyword; meta title ≤ 60 chars; meta description 140–155 chars; slug.
- **Answer-first TL;DR** (40–60 words) directly under H1: the exact answer an LLM can quote.
- Question-shaped H2s that mirror real prompts ("How much does…", "Is it worth…", "What's included…").
- A comparison table with concrete numbers and the market/currency stated.
- Named entities + dated facts ("as of October 2026"), sources cited inline with links.
- FAQ section (5–8 Qs, 2–3 sentence answers) → `FAQPage` JSON-LD.
- `Article` JSON-LD (author, datePublished, dateModified, publisher ContentFellow), `BreadcrumbList`.
- 3+ internal links (from brand.md) and 1 clear CTA to the relevant Fellow plan.
- British English for UK/EU. 1,500–2,200 words. No filler, no invented stats.
## Files
`content/article.md` (with front matter), `content/meta.json` (title, meta, slug, keywords, faq, images+alt), `content/article.html` (standalone, semantic HTML, OG/Twitter tags, canonical, hreflang en-GB, JSON-LD).
