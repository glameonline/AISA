---
name: backlink-builder
description: Builds backlinks and brand mentions for contentfellow.com (UK first): directory/citation listings, "best UK agency" listicle pitches, journalist/expert quotes, guest posts and partner links. Works rows from outputs/_plan/backlinks.md, drafts outreach in outputs/_plan/outreach/, logs status. Use for "backlinks", "link building", "get mentioned", "citations".
---
# Backlink Builder
Why: AI assistants and Google trust brands mentioned on trusted UK sites. Listicles ("best GEO agencies UK") are what ChatGPT/Gemini cite most.
## Rules
- Real, relevant sites only. No paid link farms, PBNs, comment spam, forum/profile spam, auto-generated guest posts, link exchanges or fake reviews. Mass low-quality links break Google's spam policy and can get the site penalised; volume never justifies breaking this rule.
- Keep at least 30 `todo` targets in outputs/_plan/backlinks.md: each run, research new ones (UK directories by sector, Lancashire/Burnley business sites, UK small-business blogs and podcasts, "best GEO/SEO/video agency UK" listicles, journalist requests, unlinked brand mentions, competitor backlinks via OpenSEO get_backlinks_profile).
- Same NAP everywhere: ContentFellow · Burnley, Lancashire, UK · https://contentfellow.com · contentfellow1@gmail.com. Never publish the owner's home address or phone without approval; use "Burnley, Lancashire".
- Anchor text: mostly brand ("ContentFellow") or URL; at most 1 in 5 keyword anchors.
## Daily: 15 rows per run, 30 a day (owner asked for maximum volume; quality rules above still win)
1. Take the top rows with status `todo` in outputs/_plan/backlinks.md.
2. Directory: write the listing copy (name, 150 and 750-character descriptions, categories, services with £ prices from outputs/_brand/brand.md) into outputs/_plan/outreach/<site>.md and mark the row `ready-to-submit` (submission needs the owner's login or email verification).
3. Listicle/journalist/guest post: find the editor/contact page with firecrawl_search/scrape, draft a short personal pitch (why ContentFellow fits: UK, £ prices, GEO, Burnley) in outputs/_plan/outreach/<site>.md and mark `drafted`. Never send email without the owner's go-ahead.
4. Log the date and next step in the row. Count live links in the tracker report.
