"""White-label production for UK agencies (Partner Fellow) -> outputs/_site/agencies/. Run: python3 tools/build_agencies_page.py (after build_pages.py)"""
import sys, pathlib, html; sys.path.insert(0, str(pathlib.Path(__file__).parent))
from build_pages import page, SITE, BASE
PLANS = [("Partner 30", 249, 30, "3 working days", "Short videos for 2–4 client brands"),
         ("Partner 80", 599, 80, "2 working days, dedicated editor", "Agencies running content for 5–10 clients"),
         ("Partner 200", 1349, 200, "48 hours, dedicated editor, priority queue", "High-volume social and paid-ads teams")]
ADDONS = [("Shoot half day (up to 4 hours)", "£295", "Photo + 4K video for your client in Lancashire, Manchester or Yorkshire; raw clips in 2 working days"),
          ("Shoot full day (up to 8 hours)", "£495", "As above, full day on location"),
          ("White-label social posting", "£49 per client brand / month", "Up to 3 platforms, posting from your approved calendar"),
          ("Trade websites", "Launch £249 · Grow £549 · Shop £1,149", "Built under your brand; you keep the client relationship"),
          ("White-label SEO + GEO report", "£39 per client / month", "Google rankings and AI visibility, in your branding")]
FAQ = [("What is white-label video editing?", "We edit and produce videos for your clients under your agency's brand. No ContentFellow logo, no contact with your client unless you want it; you deliver the work as your own and set your own price."),
       ("How much does white-label video editing cost?", "Partner plans cost £249 a month for 30 credits, £599 for 80 credits or £1,349 for 200 credits. One credit is one short video up to 60 seconds; a 10-minute edit is 4 credits, a motion graphics video 3 and a 60-minute podcast 4. Elsewhere, white-label editing typically costs $50–$500 per video."),
       ("How do agencies send work?", "Share raw footage and a brief through a shared folder (Google Drive, Dropbox or Frame.io). Each client brand gets its own style sheet, so edits stay consistent."),
       ("Is there a contract or a trial?", "No long contract: plans are monthly and unused credits roll over one month. New agency partners get 5 free credits to test quality, no card needed."),
       ("Where are you based?", "Burnley, Lancashire. Editing is done for agencies across the UK; on-site shoots cover Lancashire, Greater Manchester and Yorkshire.")]
def tr(cells): return "<tr>" + "".join(f"<td>{c}</td>" for c in cells) + "</tr>"
offers = [{"@type": "Offer", "name": f"{n} white-label video editing ({c} credits)", "price": str(p), "priceCurrency": "GBP", "url": f"{BASE}/agencies/",
           "priceSpecification": {"@type": "UnitPriceSpecification", "price": str(p), "priceCurrency": "GBP", "billingDuration": "P1M", "unitText": "MONTH"},
           "itemOffered": {"@type": "Service", "name": f"{n}: white-label video editing for agencies", "provider": {"@id": f"{BASE}/#org"}}} for n, p, c, _, _ in PLANS]
ld = [{"@context": "https://schema.org", "@type": "Service", "name": "White-label video editing and production for agencies", "serviceType": "White-label video editing",
       "audience": {"@type": "BusinessAudience", "audienceType": "Marketing, social media and web design agencies"}, "areaServed": "GB",
       "provider": {"@type": "Organization", "@id": f"{BASE}/#org", "name": "ContentFellow", "url": f"{BASE}/"}, "url": f"{BASE}/agencies/",
       "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Partner Fellow plans", "itemListElement": offers}},
      {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]},
      {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "ContentFellow", "item": f"{BASE}/"}, {"@type": "ListItem", "position": 2, "name": "For agencies", "item": f"{BASE}/agencies/"}]}]
tbl = lambda head, rows: f'<div style="overflow-x:auto"><table style="width:100%;border-collapse:collapse"><thead>{tr(head).replace("td>", "th>")}</thead><tbody>{"".join(rows)}</tbody></table></div>'
body = ('<h1>White-label video editing and production for UK agencies</h1>'
        '<p class="lead"><strong>Quick answer:</strong> ContentFellow edits and produces videos for marketing, social media and web agencies under the agency\'s own brand. '
        'Partner plans cost <strong>£249 a month for 30 short videos</strong>, £599 for 80 or £1,349 for 200, with 2–3 day turnaround, rollover credits and no long contract. '
        'On-site shoots in Lancashire, Manchester and Yorkshire cost £295 for a half day. New partners get 5 free credits. (October 2026.)</p>'
        '<h2>How it works</h2><ol><li>You send raw footage and a brief to a shared folder.</li><li>We edit in your client\'s style, with no ContentFellow branding.</li>'
        '<li>You review, request changes, and deliver to your client at your own price. Agencies typically mark up white-label work 50–100%.</li></ol>'
        '<h2>Partner plans (monthly)</h2><p>1 credit = 1 short video up to 60 seconds (Reel, TikTok, Short). A 10-minute edit = 4 credits, motion graphics = 3, a 60-minute podcast = 4. Unused credits roll over one month.</p>' +
        tbl(["Plan", "Price", "Credits", "Per credit", "Turnaround", "Best for"], [tr([f"<strong>{n}</strong>", f"£{p:,}/month", c, f"£{p/c:.2f}", t, b]) for n, p, c, t, b in PLANS]) +
        '<h2>White-label add-ons</h2>' + tbl(["Add-on", "Price", "What you get"], [tr([f"<strong>{html.escape(a)}</strong>", html.escape(b), html.escape(c)]) for a, b, c in ADDONS]) +
        '<h2>Why agencies use a partner instead of hiring</h2><p>A UK video editor costs about £30,000–£40,000 a year plus 35–45% employer costs, and sits idle in quiet months. '
        'A partner plan scales up and down with your client list and costs from £249 a month.</p>'
        '<h2>Frequently asked questions</h2>' + "".join(f"<h3>{q}</h3><p>{a}</p>" for q, a in FAQ) +
        '<div class="cta"><h3>Try 5 free credits</h3><p>Send us one client\'s footage and see the quality before you commit. No card needed.</p>'
        '<p><a class="btn" href="/get-started/?service=partner-trial">Claim 5 free credits →</a></p></div>')
page("agencies", "White-Label Video Editing for UK Agencies | ContentFellow",
     "White-label video editing and production for UK agencies: 30 short videos for £249/month, 2–3 day turnaround, rollover credits, 5 free credits to start.", body, ld)
sm = SITE / "sitemap.xml"; s = sm.read_text()
if "/agencies/" not in s: sm.write_text(s.replace("</urlset>", f"<url><loc>{BASE}/agencies/</loc><lastmod>2026-10-17</lastmod></url>\n</urlset>"))
ll = SITE / "llms.txt"; l = ll.read_text()
if "/agencies/" not in l:
    l = l.replace("## Development (one-off", "## For agencies (white-label, monthly)\n- Partner 30 £249 (30 credits), Partner 80 £599 (80 credits), Partner 200 £1,349 (200 credits); 1 credit = 1 short video\n"
                  "- Add-ons: shoot half day £295, full day £495; white-label social posting £49/client; trade websites from £249; SEO+GEO report £39/client\n"
                  f"- Details: {BASE}/agencies/\n\n## Development (one-off", 1)
    ll.write_text(l)
for f in ("index.html", "services/index.html", "pricing/index.html"):
    p = SITE / f; h = p.read_text()
    if 'href="/agencies/"' not in h:
        h = h.replace('<a href="/pricing/">Pricing</a>', '<a href="/pricing/">Pricing</a> · <a href="/agencies/">For agencies</a>', 1) if '<a href="/pricing/">Pricing</a>' in h else h.replace("</footer>", ' · <a href="/agencies/">For agencies</a></footer>', 1)
        if f == "services/index.html": h = h.replace("</main>", '<h2><a href="/agencies/">For agencies: white-label production</a></h2><p>Bulk video editing under your brand from £249 a month (30 videos).</p></main>', 1)
        if f == "pricing/index.html": h = h.replace("<h2>Which plan fits", '<h2>For agencies (white-label)</h2><p>Partner 30 £249/month (30 short videos), Partner 80 £599, Partner 200 £1,349. Shoots from £295. <a href="/agencies/">See agency plans →</a></p><h2>Which plan fits', 1)
        p.write_text(h)
print("agencies page built")
