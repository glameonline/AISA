"""One-off website & app development packages page -> outputs/_site/services/development/. Run: python3 tools/build_dev_page.py"""
import sys, re, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).parent))
from build_pages import page, cta_box, SITE, BASE
WEB = [("Launch", 349, "Up to 7 pages, mobile-friendly design, contact form, Google Maps, basic SEO and structured data, 2 rounds of revisions"),
       ("Grow", 749, "Up to 15 pages, blog, booking or quote form, Google Analytics and Search Console, SEO and GEO setup for Google and AI search"),
       ("Shop", 1499, "Online shop with up to 100 products, card payments, delivery rules, product structured data, stock and order emails")]
APP = [("App Starter", 1249, "Web app that installs on any phone from the browser, up to 5 screens, login, forms and a simple admin"),
       ("App Pro", 3499, "iPhone and Android app, up to 10 screens, published to the App Store and Google Play"),
       ("App Custom", 6499, "Full app with backend, payments, admin panel and notifications, scoped with you before we start")]
FAQ = [("How much does a website cost with ContentFellow?", "One-off website builds start at £349 for Launch (up to 7 pages), £749 for Grow (up to 15 pages with blog and booking) and £1,499 for an online shop."),
       ("How much does an app cost?", "Apps start at £1,249 for a web app, £3,499 for an iPhone and Android app with up to 10 screens, and from £6,499 for a custom app with backend and payments."),
       ("How do I pay?", "Half when we start and half when your website or app goes live. The price is fixed before we begin."),
       ("What happens after launch?", "You own the build. For hosting, security and changes, join the Build Fellow at £69 a month, or app care for apps."),
       ("How long does it take?", "Launch sites usually go live in 1 to 2 weeks, Grow and Shop in 2 to 4 weeks, and apps in 3 to 8 weeks depending on the plan.")]
def card(n, p, inc, kind):
    return f'<div class="card" style="background:var(--card);border-radius:12px;padding:16px 20px;margin:12px 0"><h3 style="margin:0">{n}</h3><p class="price">£{p:,} <small>one-off</small></p><p>{inc}</p><p><a class="btn" href="/get-started/?service=dev-{kind}-{n.lower().replace(" ","-")}">Get a fixed quote →</a></p></div>'
offers = [{"@type": "Offer", "name": f"{n} ({'website' if k=='web' else 'app'} development)", "price": str(p), "priceCurrency": "GBP", "description": inc,
           "itemOffered": {"@type": "Service", "name": n, "provider": {"@id": f"{BASE}/#org"}}} for k, L in (("web", WEB), ("app", APP)) for n, p, inc in L]
ld = [{"@context": "https://schema.org", "@type": "Service", "name": "Website and app development", "serviceType": "Website and mobile app development",
       "provider": {"@type": "Organization", "@id": f"{BASE}/#org", "name": "ContentFellow", "url": f"{BASE}/"}, "areaServed": "GB", "url": f"{BASE}/services/development/",
       "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Development packages", "itemListElement": offers}},
      {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
      {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "ContentFellow", "item": f"{BASE}/"},
       {"@type": "ListItem", "position": 2, "name": "Services", "item": f"{BASE}/services/"}, {"@type": "ListItem", "position": 3, "name": "Website & app development", "item": f"{BASE}/services/development/"}]}]
body = ('<h1>Website and app development, fixed prices</h1>'
        '<p class="lead"><strong>Quick answer:</strong> ContentFellow builds websites from <strong>£349</strong> and apps from <strong>£1,249</strong>, one-off and fixed price. '
        'Pay half to start and half at launch. After launch, keep it running with the <a href="/services/build-fellow/">Build Fellow</a> at £69 a month.</p>'
        '<h2>Websites</h2>' + "".join(card(n, p, i, "web") for n, p, i in WEB) +
        '<h2>Apps</h2>' + "".join(card(n, p, i, "app") for n, p, i in APP) +
        '<h2>How this compares in the UK</h2><p>UK freelancers typically charge £500–£3,000 for a small business website and agencies £3,000–£10,000. '
        'A simple iPhone and Android app usually costs £8,000–£40,000. See our guide to <a href="/blog/small-business-website-cost-uk/">small business website costs</a>.</p>'
        '<h2>Frequently asked questions</h2>' + "".join(f"<h3>{q}</h3><p>{a}</p>" for q, a in FAQ) + cta_box("development"))
page("services/development", "Website & App Development UK | From £349 | ContentFellow",
     "Fixed-price websites from £349 and apps from £1,249. Launch, Grow and Shop sites; App Starter, App Pro and App Custom. Pay half to start, half at launch.", body, ld)
# link from services hub, sitemap, llms.txt
hub = SITE / "services/index.html"; h = hub.read_text()
if "/services/development/" not in h:
    h = h.replace("</main>", '<h2><a href="/services/development/">Website &amp; app development</a></h2><p>Fixed-price builds: websites from £349, apps from £1,249.</p></main>', 1); hub.write_text(h)
sm = SITE / "sitemap.xml"; s = sm.read_text()
if "/services/development/" not in s:
    s = s.replace("</urlset>", f"<url><loc>{BASE}/services/development/</loc><lastmod>2026-10-17</lastmod></url>\n</urlset>"); sm.write_text(s)
ll = SITE / "llms.txt"; l = ll.read_text()
if "Development (one-off)" not in l:
    l = l.replace("## Guides", "## Development (one-off, fixed price)\n- Websites: Launch £349 (up to 7 pages), Grow £749 (up to 15 pages, blog, booking), Shop £1,499 (up to 100 products)\n- Apps: App Starter £1,249 (web app), App Pro £3,499 (iPhone + Android, 10 screens), App Custom from £6,499\n- Details: https://contentfellow.com/services/development/\n\n## Guides", 1); ll.write_text(l)
print("ok")
