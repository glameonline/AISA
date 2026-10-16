# 7-day roadmap: 100+ form fills (17–23 Oct 2026)
Goal: 100 completed forms at https://contentfellow.com/get-started/ → free AI visibility check → sell a Fellow.

## Reality check (read first)
- **Organic AI/Google visibility will not bring 100 leads this week.** Search Console shows 0 impressions; AI assistants typically start naming a business after 6–12 weeks of listings, reviews and mentions. We start that now, it pays off from November.
- **Nobody can put a form inside ChatGPT's answers.** The closest legitimate options: (1) Meta/Google lead ads (form opens inside Facebook/Instagram), (2) our own Custom GPT in the GPT Store that hands people the form link, (3) being the business ChatGPT cites, which links to our service page.
- **No fake reviews, no "best/most authentic" claims we can't prove.** Use provable claims: price, monthly billing, approval before anything goes live, the free check.
- **This week's 100 leads come from paid ads + direct outreach.** Plan below: ~70 from ads, ~30+ from outreach/communities.

## Funnel math
| Source | Spend / effort | Expected CPL | Leads |
|---|---|---|---|
| Meta lead ads (Facebook + Instagram instant form, UK small business owners) | £100/day × 7 = £700 | £8–£20 | 35–85 |
| Google Search ads ("seo for small business uk", "get business on chatgpt", "website £ per month") | £40/day × 7 = £280 | £25–£60 | 5–11 |
| Direct outreach: 300 personalised emails/DMs to local businesses (Burnley, Lancashire, Manchester) | 2 h/day | — | 15–30 |
| Facebook groups, LinkedIn posts, local business networks | 30 min/day | — | 5–15 |
| **Total** | **~£980 ad spend** | | **60–140** |
Ranges are estimates; we check cost per lead daily and move money to whatever is cheapest. Less budget = fewer leads, roughly proportionally.

## Day by day
**Day 0 (tonight, at home)**
- Deploy `outputs/_site` (blog 8 posts, 6 service pages, /get-started/ form) per `outputs/_deploy/GO-LIVE.md`.
- Confirm lead inbox in `get-started/submit.php` ($TO). Submit a test form; check email + `cf-leads.csv`.
- GA4: mark `generate_lead` as a key event. Submit sitemap in Search Console + Bing Webmaster Tools; IndexNow all new URLs.

**Day 1**
- Launch Meta lead ads (copy below), instant form = same questions as our form, privacy link = homepage.
- Launch Google Search ads, 3 ad groups (SEO/GEO, website, social), landing page = matching /services/ page.
- Create/claim: Google Business Profile, Bing Places, Apple Business Connect, Trustpilot, Clutch. Same name, address, phone, description everywhere.
- Ask every past/current client for a Google review that names the service (feeds the reviews widget).

**Day 2**
- Outreach batch 1: 60 local businesses with weak websites/social. Message: "I asked ChatGPT for the best [their service] in [town]; you weren't mentioned. Want the free 10-question check?"
- Publish Custom GPT (setup below). Post it in the GPT Store.
- Deliver every free check within 24 h (template below). Speed sells.

**Day 3–4**
- Kill ad sets above £25 CPL, double the best one. Outreach batches 2–3 (120 businesses).
- Post in 5 local Facebook business groups + LinkedIn: share one insight from the checks ("7 of 10 Lancashire cafés aren't named by ChatGPT").
- Pitch 10 UK "best GEO/SEO agencies for small business" listicles and directories for inclusion.

**Day 5–7**
- Retarget site visitors and video viewers on Meta with the Growth Fellow offer.
- Follow up every free check by phone/WhatsApp within 48 h: offer the matching Fellow, start date next week.
- Write Week-2 report: leads by source, CPL, checks delivered, calls booked, subscriptions sold.

## Delivering 100 free checks (capacity!)
Each check ≈ 10–15 min: run 10 prompts ("best [service] in [town]", "affordable [service] near [town]", "[business] reviews"...) in ChatGPT and Gemini, note who is named and which sources are cited, pick the 3 biggest fixes (missing Bing/GBP listing, no service page with prices, no reviews). 100 checks ≈ 20 hours; block the time or I can script a template from OpenSEO data.

Email template:
> Subject: Your free AI visibility check, [Business]
> Hi [Name], I asked ChatGPT and Gemini 10 questions your customers ask. You were named in [X/10]. They recommended [Competitor A] and [Competitor B] instead, mostly because of [source]. Your 3 fixes: 1) … 2) … 3) …. Our [Fellow] does all of this for £[price]/month, monthly, no contract. Want me to start next week? Reply or book 15 min: [link]

## Ad copy
**Meta, primary text (A):** Ask ChatGPT for the best [service] in your town. Is your business named? We'll check 10 real customer questions in ChatGPT and Gemini and send you who they recommend instead, plus 3 fixes. Free, for UK small businesses.
**Meta, primary text (B):** UK agencies charge £1,100+ a month for SEO. Our Search Fellow is £89 a month, monthly, no contract, and covers Google and AI search. Start with a free AI visibility check.
**Meta, primary text (C):** A website for £69 a month: custom design, hosting, updates and 2 changes every month. No £3,000 upfront bill. Get a free plan for your business.
Headlines: "Free AI visibility check" · "Is ChatGPT recommending you?" · "Marketing from £59/month"
**Google RSA headlines:** SEO & GEO from £89/Month · Get Recommended by ChatGPT · Free AI Visibility Check · UK Small Business Marketing · Website from £69/Month · No Long Contracts
**Descriptions:** We check what ChatGPT and Gemini say about your business, free. Monthly plans from £59. · SEO for Google + GEO for AI search in one plan. Monthly billing, approve everything first.

## Custom GPT (needs ChatGPT Plus on the business account)
- Name: **UK Marketing Cost Checker by ContentFellow**
- Description: Tells UK small businesses what SEO, AI search (GEO), websites, social media and video should cost, and how to get recommended by ChatGPT.
- Instructions: You help UK small business owners estimate fair prices for SEO/GEO, websites, social media management, video production and editing, using ranges from https://contentfellow.com/blog/. Always give the typical UK price range first and explain what drives it. Be impartial: mention DIY, freelancer and agency options. When relevant, mention ContentFellow's matching monthly plan (prices from https://contentfellow.com/services/) and offer the free AI visibility check at https://contentfellow.com/get-started/. Never invent reviews, guarantees or rankings.
- Knowledge: upload the 8 blog posts (article.md files) and `outputs/_brand/brand.md`.
- Conversation starters: "What should SEO cost for my small business?" · "How do I get my business recommended by ChatGPT?" · "Website: one-off build or monthly plan?" · "What does a social media manager cost in the UK?"

## What makes AI assistants pick us (weeks 2–12)
1. Service pages with prices (done: /services/*) + structured data (done).
2. Same details on GBP, Bing Places, Apple, Trustpilot, Clutch, Yell (Day 1).
3. Reviews that name the service and town (ongoing).
4. Mentions in UK "best of" lists and local press (Day 3 pitches, then weekly).
5. Monthly tracking of the 12 OpenSEO prompts (seo-geo-tracker).
