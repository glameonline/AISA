"""Adds a website offer box (live demos, prices, call/email, promo GhostFellow7) to website-related blog posts. Idempotent. Run by build_zip.py."""
import pathlib, datetime
MARK = "<!--cf-offer-->"
SLUGS = ["booking-website-cost-uk", "how-long-to-build-a-website-uk", "marketing-agency-burnley", "online-shop-website-cost-uk",
         "pay-monthly-website-uk-comparison", "restaurant-website-cost-uk", "small-business-website-cost-uk", "tradesperson-website-cost-uk",
         "web-designer-burnley", "website-cost-ireland", "website-maintenance-cost-uk", "website-subscription-vs-one-off-build"]
sale = datetime.date.today() <= datetime.date(2026, 10, 31)
BOX = (MARK + '<aside style="margin:32px 0;padding:22px;border-radius:18px;background:linear-gradient(135deg,#1a0b2e,#3b0d4f 55%,#ff6a00);color:#fff">'
       '<strong style="font-size:22px">' + ("🎃 Halloween: 20% off websites until 31 Oct. " if sale else "") + 'See your website live first</strong>'
       '<p style="margin:8px 0 14px">Our <a href="/pay-monthly-websites/" style="color:#ffb27a">pay monthly websites</a>: built from £225 (Basic), £520 (Standard) or £1,099 (Premium), '
       'then monthly plans from £49. Open 3 live demos for your industry. Code <b>GhostFellow7</b> = 25% off.</p>'
       '<a href="/pay-monthly-websites/" style="display:inline-block;background:#ff5a1f;color:#0c0c0d;font-weight:800;padding:12px 18px;border-radius:999px;text-decoration:none;margin:0 8px 8px 0">See live demos</a>'
       '<a href="tel:+447535677302" style="display:inline-block;background:#fff;color:#0c0c0d;font-weight:800;padding:12px 18px;border-radius:999px;text-decoration:none;margin:0 8px 8px 0">📞 07535 677302</a>'
       '<a href="mailto:info@contentfellow.com?subject=Website%20-%20GhostFellow7" style="color:#fff">✉️ info@contentfellow.com</a></aside>')
for slug in SLUGS:
    p = pathlib.Path("outputs/_site/blog") / slug / "index.html"
    if not p.exists(): continue
    s = p.read_text()
    if MARK in s:  # refresh (sale text expires)
        a = s.index(MARK); b = s.index("</aside>", a) + 8; s = s[:a] + s[b:]
    s = s.replace("</article>", BOX + "</article>", 1) if "</article>" in s else s.replace("</main>", BOX + "</main>", 1)
    p.write_text(s)
