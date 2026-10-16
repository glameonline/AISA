# Ghar pe karna hai (deploy checklist, 16 Oct 2026)
Full technical steps: `outputs/_deploy/GO-LIVE.md` · Upload: `outputs/_deploy/contentfellow-site-2026-10-16.zip`

## Owner se chahiye (pehle 10 minute)
- [ ] Desktop access (Desktop Commander) + cPanel login
- [ ] Leads kis email par aayein? (abhi `contentfellow1@gmail.com`, `get-started/submit.php` mein `$TO`)
- [ ] Trial capacity: har hafte kitne free trials le sakte hain? (videos aur shoots mein waqt lagta hai)
- [ ] Studio mini shoot: Burnley se 20 miles theek hai? Time-based trials 7 din (data) ya 3 din (owner)? `tools/build_pages.py` → `TRIAL_DAYS`
- [ ] Ads budget is hafte (plan: ~£980) + Meta Business aur Google Ads account access
- [ ] Google Business Profile hai? Reviews hain? Place ID + Places API key (reviews widget)

## Live karna (order)
1. [ ] Backup public_html (index.html, .htaccess, robots, sitemap, llms)
2. [ ] Zip upload + extract: blog (8 posts), /services/ (6 pages + free trial each), /get-started/ form + thanks
3. [ ] `.htaccess` fixes (www → non-www, /hello-world/ 410, test .html 301)
4. [ ] Homepage `index.html`:
   - [ ] og:image absolute URL
   - [ ] Nav: "Services", "Guides", "Free trial" links
   - [ ] Hero button: "Start free →" → `/get-started/`
   - [ ] Har Fellow card par trial badge + link `/services/<fellow>/`:
     Search "Free 7-day trial" · Social "Free 7-day trial" · Build "Free homepage preview" · Studio "Free mini shoot" · Creator "3 free videos" · Growth "Free 7-day trial"
   - [ ] Har card ke neeche `<div class="cf-reviews" data-service="…" hidden></div>` + reviews CSS/JS
5. [ ] Reviews widget: `/reviews/` upload + config outside public_html (`outputs/_site-fixes/reviews/README.md`)
6. [ ] Test form → email aaya? `cf-leads.csv` mein row? thanks page?
7. [ ] Verify table in GO-LIVE.md (sab URLs 200, www 301, old pages 410)
8. [ ] GA4: `generate_lead` key event · Search Console + Bing: sitemap submit, request indexing · IndexNow

## Free trials (har service)
| Fellow | Trial | Owner ka kaam per trial |
|---|---|---|
| Search £89 | 7 din free: AI check + Bing + AI crawlers + GBP tidy | ~1–2 h |
| Social £59/£129 | 7 din free: plan + 5 posts, 1 platform | ~2 h |
| Build £69 | Free homepage preview, 3 working days | ~3–4 h |
| Studio £149 | Free 30-min mini shoot (20 miles of Burnley): 5 photos + 1 short video | ~2 h + travel |
| Creator £119 | 3 free short videos from client's footage | ~2–3 h |
| Growth £389 | 7 din: AI check, 2 videos, 1 week posts, homepage preview, strategy call | ~6–8 h |
Terms on every page: no card, one per business, UK only, limited trials each week.
Why not 3 days everywhere: 7-day trials convert best (24% median vs 19% for 14 days; decisions peak on days 3–4), and SEO/social show nothing in 3 days. Video and web trials are deliverables ("first video free, keep it"), which is how video agencies win clients.

## Is hafte ke ads (roadmap-100-leads.md)
- [ ] Meta lead ads: trial wale ads (neeche) + free check ad
- [ ] Google Search ads: landing = matching /services/ page
- [ ] Custom GPT "UK Marketing Cost Checker" publish
- [ ] Outreach: 60 businesses/din
