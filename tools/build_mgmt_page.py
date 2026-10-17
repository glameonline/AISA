"""Monthly website & app management plans page -> outputs/_site/services/management/. Run: python3 tools/build_mgmt_page.py"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).parent))
from build_pages import page, cta_box, SITE, BASE
WEB = [("Care", 49, "Hosting, SSL certificate, security, backups and updates, plus 1 small change a month", None),
       ("Build Fellow", 69, "A custom website of up to 5 pages, with hosting, security and updates, plus 2 change requests a month", "/services/build-fellow/"),
       ("Care Plus", 159, "Everything in Build Fellow, plus 5 changes a month, a new page every month, a monthly speed and SEO check, and priority support within 24 hours", None)]
APP = [("App Care", 149, "App hosting, iOS and Android updates, bug fixes and app store compliance", None),
       ("App Care Plus", 359, "Everything in App Care, plus 2 small feature changes a month and a monthly report", None),
       ("App Care Pro", 599, "Everything in App Care Plus, plus 5 changes a month, a new feature every month and priority support", None)]
FAQ = [("How much does website management cost?", "Website management starts at £49 a month for Care, £69 a month for the Build Fellow (including a 5-page custom site) and £159 a month for Care Plus."),
       ("How much does app maintenance cost?", "App management starts at £149 a month for App Care, £359 for App Care Plus and £599 for App Care Pro."),
       ("Is there a contract?", "Plans are billed monthly. You can move up or down a plan from the next month."),
       ("Can you look after a website or app you didn't build?", "Yes. We check it first, then take it onto the plan that fits."),
       ("Do I need a plan after a development build?", "We recommend one so your website or app stays secure, fast and up to date. New builds start on the plan you choose at launch.")]
def card(n, p, inc, link, kind):
    more = f' <a href="{link}">Details</a>' if link else ""
    return f'<div class="card" style="background:var(--card);border-radius:12px;padding:16px 20px;margin:12px 0"><h3 style="margin:0">{n}</h3><p class="price">£{p} <small>per month</small></p><p>{inc}{more}</p><p><a class="btn" href="/get-started/?service=care-{kind}-{n.lower().replace(" ","-")}">Start this plan →</a></p></div>'
offers = [{"@type": "Offer", "name": n, "price": str(p), "priceCurrency": "GBP", "description": inc,
           "priceSpecification": {"@type": "UnitPriceSpecification", "price": str(p), "priceCurrency": "GBP", "unitText": "MONTH"},
           "itemOffered": {"@type": "Service", "name": n, "provider": {"@id": f"{BASE}/#org"}}} for L in (WEB, APP) for n, p, inc, _ in L]
ld = [{"@context": "https://schema.org", "@type": "Service", "name": "Website and app management", "serviceType": "Website maintenance and app maintenance",
       "provider": {"@type": "Organization", "@id": f"{BASE}/#org", "name": "ContentFellow", "url": f"{BASE}/"}, "areaServed": "GB", "url": f"{BASE}/services/management/",
       "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Management plans", "itemListElement": offers}},
      {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
      {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "ContentFellow", "item": f"{BASE}/"},
       {"@type": "ListItem", "position": 2, "name": "Services", "item": f"{BASE}/services/"}, {"@type": "ListItem", "position": 3, "name": "Website & app management", "item": f"{BASE}/services/management/"}]}]
body = ('<h1>Website and app management plans</h1>'
        '<p class="lead"><strong>Quick answer:</strong> ContentFellow looks after websites from <strong>£49 a month</strong> and apps from <strong>£149 a month</strong>: '
        'hosting, security, updates and changes on one monthly plan. Need something built first? See <a href="/services/development/">website and app development</a>.</p>'
        '<h2>Website plans</h2>' + "".join(card(n, p, i, l, "web") for n, p, i, l in WEB) +
        '<h2>App plans</h2>' + "".join(card(n, p, i, l, "app") for n, p, i, l in APP) +
        '<h2>How this compares in the UK</h2><p>UK agencies typically charge from £50 to £150 a month for website care, and specialist app studios charge £675 to £1,495 a month for app maintenance.</p>'
        '<h2>Frequently asked questions</h2>' + "".join(f"<h3>{q}</h3><p>{a}</p>" for q, a in FAQ) + cta_box("management"))
page("services/management", "Website & App Management UK | From £49/month | ContentFellow",
     "Monthly website care from £49, Build Fellow £69 and Care Plus £159. App care from £149, App Care Plus £359 and App Care Pro £599. UK, monthly billing.", body, ld)
hub = SITE / "services/index.html"; h = hub.read_text()
if "/services/management/" not in h:
    h = h.replace("</main>", '<h2><a href="/services/management/">Website &amp; app management</a></h2><p>Monthly care: websites from £49, apps from £149.</p></main>', 1); hub.write_text(h)
sm = SITE / "sitemap.xml"; s = sm.read_text()
if "/services/management/" not in s:
    s = s.replace("</urlset>", f"<url><loc>{BASE}/services/management/</loc><lastmod>2026-10-17</lastmod></url>\n</urlset>"); sm.write_text(s)
ll = SITE / "llms.txt"; l = ll.read_text()
if "Management (monthly)" not in l:
    l = l.replace("## Development (one-off", "## Management (monthly)\n- Websites: Care £49, Build Fellow £69 (includes 5-page custom site), Care Plus £159\n- Apps: App Care £149, App Care Plus £359, App Care Pro £599\n- Details: https://contentfellow.com/services/management/\n\n## Development (one-off", 1); ll.write_text(l)
print("ok")
