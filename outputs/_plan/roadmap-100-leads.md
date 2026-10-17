# Organic-only roadmap: maximum form fills, no ads (from 17 Oct 2026)
Owner decision 16 Oct: **no ads for now.** Everything below is organic SEO, GEO and direct outreach.
Goal: as many forms as possible at https://contentfellow.com/get-started/ (free trial on every Fellow), and get ContentFellow named by Google and AI assistants.

## Honest expectations
- **Google/ChatGPT traffic:** starts small. Search Console shows 0 impressions today; new pages typically get indexed in days, rank and get cited by AI in 6–12 weeks. This is the long-term engine.
- **This week's forms come from people we reach directly.** At typical cold-outreach reply rates, ~300–500 personal contacts this week → roughly 20–50 forms. 100 in week one organically would be an exceptional result, so we push outreach hard and measure daily.
- **No fake reviews, no unprovable "best" claims.** Our edge is provable: published prices from £59, monthly billing, free trial on every service, approval before anything goes live.

## Already built (deploys tonight)
- 9 blog guides (every Fellow covered + honest price comparison), 6 service pages with Offer + free-trial schema, Burnley/Lancashire page, /get-started/ form, llms.txt, sitemap (20 URLs), IndexNow key, reviews widget.
- Citation pack + pitch list: `outputs/_plan/citation-pack.md`.

## Day 0 (tonight, at home)
- Deploy (GHAR-PE-KARNA-HAI.md). Homepage: nav links to Services/Guides/Free trial, trial badges, link each Fellow card to /services/.
- Search Console + Bing Webmaster Tools: submit sitemap, request indexing for /services/*, /burnley/, top 3 posts. IndexNow ping all 20 URLs.

## Day 1 — listings (GEO foundation, ~3 hours)
- Google Business Profile, Bing Places, Apple Business Connect, LinkedIn page, Facebook/Instagram, Trustpilot. Copy from citation-pack.md. GBP: add services with prices, the free-trial **Offer post**, and 10+ real photos.
- Ask every existing client/contact for a Google review naming the service and town.

## Days 1–7 — direct outreach (the lead engine, 2–3 hours/day)
| Channel | Daily target | Offer to lead with |
|---|---|---|
| Walk-in / call local businesses in Burnley, Padiham, Nelson, Colne, Accrington | 10–15 | **Free mini shoot** (Studio) or **3 free videos** (Creator) |
| Personal email / Instagram DM to local businesses with weak social or no website | 40–60 | "I asked ChatGPT for the best [their trade] in [town]; you weren't named. Want the free check + 7-day trial?" |
| LinkedIn: founder posts daily + 20 personal connection notes | 1 post + 20 | Free AI visibility check |
| Local Facebook business groups (follow each group's promo-day rules) | 2–3 groups | Free trial offer + one real insight |
| Reddit r/smallbusinessuk, UK forums: genuinely helpful answers, link only when relevant | 2–3 answers | Link to the relevant guide |
Track every contact in a sheet: date, business, channel, offer, reply, form, trial, paid.

## Days 2–5 — PR and lists (GEO multiplier)
- Pitch SEO Works "GEO for Small Businesses", Semrush Burnley, GoodFirms Lancashire, Clutch, DesignRush (citation-pack.md).
- Local press pitch (Burnley Express, Lancashire Business View): "What ChatGPT recommends for Burnley businesses", using anonymised results from the free checks.
- Turn each blog guide into a LinkedIn carousel + Instagram post + 30-second Short (owner on camera: "I asked ChatGPT…"). Video of real local businesses is also what AI and Google love.

## Weekly, ongoing
- 1–2 new guides/week from `topic-queue.md` (next: "How to check if ChatGPT, Gemini and Perplexity mention your brand", "llms.txt explained", Burnley-specific guides).
- 2–5 new Google reviews/week. GBP post every week.
- Re-run the 12 tracked AI prompts (seo-geo-tracker), log who's named, fix the gaps.
- Optional Custom GPT "UK Marketing Cost Checker" (setup below) — free, extra discovery inside ChatGPT.

## Delivering trials and checks (capacity)
Free check ≈ 10–15 min; Creator 3 videos ≈ 2–3 h; Studio mini shoot ≈ 2 h + travel; Build preview ≈ 3–4 h. Cap weekly trials to what you can deliver within the promised times; speed of delivery is what converts.

Email template (check):
> Subject: Your free AI visibility check, [Business]
> Hi [Name], I asked ChatGPT and Gemini 10 questions your customers ask. You were named in [X/10]. They recommended [A] and [B], mostly because of [source]. Your 3 fixes: 1) … 2) … 3) …. Want us to do them? Start a free 7-day trial of the Search Fellow (£89/month after, monthly, no contract): [link]

## Custom GPT (free; needs ChatGPT Plus on the business account)
- Name: **UK Marketing Cost Checker by ContentFellow**
- Instructions: Help UK small business owners estimate fair prices for SEO/GEO, websites, social media, video production and editing, using ranges from https://contentfellow.com/blog/. Give the typical UK range first, explain what drives it, mention DIY/freelancer/agency options impartially. When relevant, mention ContentFellow's matching plan (https://contentfellow.com/services/) and its free trial (https://contentfellow.com/get-started/). Never invent reviews, guarantees or rankings.
- Knowledge: the 9 article.md files + outputs/_brand/brand.md.
- Starters: "What should SEO cost for my small business?" · "How do I get recommended by ChatGPT?" · "Website: one-off build or monthly plan?" · "What does a social media manager cost in the UK?"

## Paused (owner decision: no ads for now)
Meta lead ads and Google Search ads plan kept in git history (commit e16e266) if you want them later.
