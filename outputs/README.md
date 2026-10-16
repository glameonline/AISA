# ContentFellow SEO/GEO Agent Team

## Which skill runs in what order
```
Topic (or "daily run" → next row of outputs/_plan/topic-queue.md)
  │
  ▼  content-agent-orchestrator  (manager)
1. Research + keywords ........ Firecrawl search (UK) + Keyword Tool UK  → research/brief.md, keywords.md
2. Competitor check ........... competitor-site-scraper                   → research/competitors.md
3. Brand voice + links ........ website-brand-scraper                     → _brand/brand.md (cached 7 days)
4. Write ...................... blog-writer-seo-aeo-geo                   → content/article.md, meta.json, article.html
5. Images ..................... blog-image-generator (tools/build_post.py + tools/render.js) → images/*.png
6. Save ....................... outputs/<topic>/{research,content,images,publish,screenshots}
7. Publish .................... wordpress-publisher (WP draft via REST, or static /blog package) → publish/
8. Track ...................... seo-geo-tracker (OpenSEO AI visibility + GA4/GSC) → _tracker/ + dashboard/
```
Skills live in `.claude/skills/<name>/SKILL.md` (where Claude Code loads them for this repo).
The brief said `/mnt/skills/user/`, but that folder is wiped with each cloud container.

## Test topic result: "How Much Does LLM Optimization Cost for Small Businesses?"
| Check | Status | Where |
|---|---|---|
| Researched the topic | ✅ | research/brief.md |
| Checked competitors | ✅ | research/competitors.md |
| Found keywords | ✅ | research/keywords.md |
| Full SEO+AEO+GEO article | ✅ 1,540 words, 7 FAQs, Article/FAQPage/Breadcrumb JSON-LD | content/ |
| ≥2 images | ✅ 3 (featured, chart, diagram) + alt text | images/ |
| Saved in folders | ✅ | outputs/how-much-does-llm-optimization-cost-small-businesses/ |
| WordPress draft / live | ⚠️ contentfellow.com isn't WordPress; static package built, deploy access needed | publish/ |

Screenshot: `screenshots/article-full.png`. Dashboard: `outputs/dashboard/index.html`.

## To make it fully automatic
- Deploy access: GitHub repo of contentfellow.com (add to the Claude session), or a Netlify/Vercel token, or WordPress `WP_URL` / `WP_USER` / `WP_APP_PASSWORD` as environment secrets.
- Network: allow `contentfellow.com` in the environment's network policy (Firecrawl works meanwhile).
- OpenSEO credits: one AI-visibility check (12 prompts × 5 engines) = 3,468 credits ≈ $3.47; daily ≈ $104/month. Weekly ≈ $15/month.
- Connect GA4 + Search Console inside OpenSEO for views and the queries that bring visitors.
