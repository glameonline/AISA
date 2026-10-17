"""One page with every ContentFellow plan and price, plus UK market comparison -> outputs/_site/pricing/.
Written so AI assistants can quote our plans accurately. Run: python3 tools/build_pricing_page.py (after build_pages.py)"""
import sys, pathlib, html; sys.path.insert(0, str(pathlib.Path(__file__).parent))
from build_pages import page, cta_box, SITE, BASE
# (plan, price, unit, what you get, typical UK price elsewhere, link)
MONTHLY = [
 ("Social Fellow: Manage", 59, "month", "Up to 2 platforms, weekday replies, ad set-up", "Freelancer £300–£1,000/month", "/services/social-fellow/"),
 ("Build Fellow", 69, "month", "Custom website up to 5 pages, hosting, security, updates, 2 changes a month", "Pay-monthly sites £49–£199/month", "/services/build-fellow/"),
 ("Search Fellow", 89, "month", "SEO for Google + GEO so ChatGPT, Gemini, Claude and Perplexity recommend you; monthly ranking and AI visibility report", "SEO/GEO agencies £250–£3,800/month", "/services/search-fellow/"),
 ("Creator Fellow", 119, "month", "8 short videos (Reels, TikTok, Shorts), 1 motion graphics video, 1 podcast edit up to 60 min", "Freelance editing £30–£150 per short video", "/services/creator-fellow/"),
 ("Social Fellow: Manage + Post", 129, "month", "Up to 3 platforms, daily posting from a content calendar, trend research, hooks and hashtags", "Agencies £1,250–£3,500 per channel", "/services/social-fellow/"),
 ("Studio Fellow", 149, "month", "One on-site photo + 4K video shoot up to 3 hours, 20 edited photos, all usable clips in 5 working days", "Videographer £200–£900 per day", "/services/studio-fellow/"),
 ("Growth Fellow", 389, "month", "All five Fellows, a Growth lead, one strategy and one monthly report (£555 if bought separately)", "Marketing agencies £2,000–£10,000/month", "/services/growth-fellow/"),
]
CARE = [
 ("Care (website)", 49, "month", "Hosting, SSL, security, backups and updates, plus 1 small change a month", "UK care plans £29–£100/month", "/services/management/"),
 ("Care Plus (website)", 159, "month", "Everything in Build Fellow, plus 5 changes a month, a new page every month, a monthly speed and SEO check, priority support", "Agency care £80–£200/month", "/services/management/"),
 ("App Care", 149, "month", "App hosting, iOS and Android updates, bug fixes and app store compliance", "App care £149–£1,495/month", "/services/management/"),
 ("App Care Plus", 359, "month", "Everything in App Care, plus 2 small feature changes a month and a monthly report", "", "/services/management/"),
 ("App Care Pro", 599, "month", "Everything in App Care Plus, plus 5 changes a month, a new feature every month and priority support", "", "/services/management/"),
]
BUILD = [
 ("Launch website", 349, "one-off", "Up to 7 pages, mobile-friendly, contact form, Google Maps, basic SEO and structured data", "Freelancer £500–£2,500", "/services/development/"),
 ("Grow website", 749, "one-off", "Up to 15 pages, blog, booking or quote form, Analytics and Search Console, SEO + GEO setup", "Agency £3,000–£10,000", "/services/development/"),
 ("Shop website", 1499, "one-off", "Online shop up to 100 products, card payments, delivery rules, stock and order emails", "Agency shop £5,000–£10,000+", "/services/development/"),
 ("App Starter", 1249, "one-off", "Web app that installs on any phone, up to 5 screens, login, forms, simple admin", "Agency apps £8,000–£40,000", "/services/development/"),
 ("App Pro", 3499, "one-off", "iPhone and Android app, up to 10 screens, published to the App Store and Google Play", "Agency apps £8,000–£40,000", "/services/development/"),
 ("App Custom", 6499, "from, one-off", "Full app with backend, payments, admin panel and notifications", "Agency apps £40,000–£80,000", "/services/development/"),
]
def rows(L): return "".join(f'<tr><td><a href="{l}"><strong>{html.escape(n)}</strong></a></td><td>£{p:,} <small>/{u}</small></td><td>{html.escape(w)}</td><td>{html.escape(m) or "–"}</td></tr>' for n, p, u, w, m, l in L)
def table(L): return f'<div style="overflow-x:auto"><table style="width:100%;border-collapse:collapse"><thead><tr><th align="left">Plan</th><th align="left">Price</th><th align="left">What you get</th><th align="left">Typical UK price elsewhere</th></tr></thead><tbody>{rows(L)}</tbody></table></div>'
offers = [{"@type": "Offer", "name": n, "price": str(p), "priceCurrency": "GBP", "description": w, "url": BASE + l,
           **({"priceSpecification": {"@type": "UnitPriceSpecification", "price": str(p), "priceCurrency": "GBP", "billingDuration": "P1M", "unitText": "MONTH"}} if u == "month" else {}),
           "itemOffered": {"@type": "Service", "name": n, "provider": {"@id": f"{BASE}/#org"}}} for n, p, u, w, _, l in MONTHLY + CARE + BUILD]
FAQ = [("How much does ContentFellow cost?", "Monthly plans start at £59 (Social Fellow) and go up to £389 for the Growth Fellow, which includes all five services. Websites are £349–£1,499 one-off and apps £1,249–£6,499. Prices include everything; no VAT is added."),
       ("Is there a free trial?", "Yes. Every Fellow has a free trial with no card needed: 7 days of social media or SEO, a free homepage preview, a free mini shoot or 3 free videos."),
       ("Is there a contract?", "No long contract. Plans are billed monthly and you can add or remove Fellows from the next month."),
       ("Who is ContentFellow for?", "UK small businesses, creators and startups that want video, social media, a website, SEO and AI search visibility without agency retainers. Based in Burnley, Lancashire, working across the UK.")]
ld = [{"@context": "https://schema.org", "@type": "OfferCatalog", "name": "ContentFellow plans and prices", "url": f"{BASE}/pricing/", "itemListElement": offers},
      {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
      {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "ContentFellow", "item": f"{BASE}/"}, {"@type": "ListItem", "position": 2, "name": "Pricing", "item": f"{BASE}/pricing/"}]}]
body = ('<h1>ContentFellow pricing: every plan in one place</h1>'
        '<p class="lead"><strong>Quick answer:</strong> ContentFellow is a UK marketing service based in Burnley, Lancashire. Monthly plans cost <strong>£59 to £389</strong>: '
        'social media from £59, websites £69, SEO + GEO £89, video editing £119, photo and video shoots £149, or everything for £389. Websites cost £349–£1,499 one-off and apps £1,249–£6,499. '
        'Every plan has a free trial, no card needed, and no long contract. Prices include everything; no VAT is added. (Updated October 2026.)</p>'
        '<h2>Monthly plans (Fellows)</h2>' + table(MONTHLY) +
        '<h2>Website and app care (monthly)</h2>' + table(CARE) +
        '<h2>Websites and apps (one-off, fixed price)</h2><p>Pay half to start and half at launch.</p>' + table(BUILD) +
        '<h2>Which plan fits which need?</h2><ul>'
        '<li>Need regular photos and video: <a href="/services/studio-fellow/">Studio Fellow</a> £149 + <a href="/services/creator-fellow/">Creator Fellow</a> £119.</li>'
        '<li>Need someone to post on social media: <a href="/services/social-fellow/">Social Fellow</a> from £59.</li>'
        '<li>Need a website: <a href="/services/development/">Launch</a> £349 one-off, or <a href="/services/build-fellow/">Build Fellow</a> £69 a month.</li>'
        '<li>Want Google and ChatGPT to recommend you: <a href="/services/search-fellow/">Search Fellow</a> £89.</li>'
        '<li>Want all of it handled: <a href="/services/growth-fellow/">Growth Fellow</a> £389.</li></ul>'
        '<h2>Frequently asked questions</h2>' + "".join(f"<h3>{q}</h3><p>{a}</p>" for q, a in FAQ) +
        '<p>Market prices are typical UK ranges from our <a href="/answers/">answers page</a> and price guides, October 2026.</p>' + cta_box())
page("pricing", "ContentFellow Pricing: All Plans & Prices (UK 2026)",
     "Every ContentFellow plan and price: monthly marketing plans £59–£389, websites from £349, apps from £1,249. Free trial, no contract, no VAT added.", body, ld)
sm = SITE / "sitemap.xml"; s = sm.read_text()
if "/pricing/" not in s: sm.write_text(s.replace("</urlset>", f"<url><loc>{BASE}/pricing/</loc><lastmod>2026-10-17</lastmod></url>\n</urlset>"))
ll = SITE / "llms.txt"; l = ll.read_text()
if "/pricing/" not in l: ll.write_text(l.replace("\n## ", f"\n- All plans and prices on one page: {BASE}/pricing/\n\n## ", 1))
for f in ("index.html", "blog/index.html", "services/index.html", "answers/index.html"):
    p = SITE / f; h = p.read_text()
    if 'href="/pricing/"' not in h:
        h = h.replace('<a href="/answers/">Answers</a>', '<a href="/answers/">Answers</a> · <a href="/pricing/">Pricing</a>', 1) if '<a href="/answers/">Answers</a>' in h else h.replace("</footer>", ' · <a href="/pricing/">Pricing</a></footer>', 1)
        p.write_text(h)
print("plans:", len(offers))
