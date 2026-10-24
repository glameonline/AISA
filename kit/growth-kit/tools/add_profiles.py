"""Link ContentFellow's Google Maps and Yell profiles from every page in outputs/_site and add a plans box to blog posts (idempotent).
Adds footer links, sameAs on Organization/ProfessionalService JSON-LD, and a 'Find us' box on local pages.
Usage: python3 tools/add_profiles.py"""
import json, pathlib, re
SITE = pathlib.Path("outputs/_site")
GBP = "https://maps.google.com/?cid=6675954353271833173"
YELL = "https://www.yell.com/biz/content-fellow-burnley-11050665/"
LINKS = f' · <a class="cf-prof" href="{GBP}" rel="noopener" target="_blank">Google Maps &amp; reviews</a> · <a href="{YELL}" rel="noopener" target="_blank">Yell</a>'
BOX = (f'<section class="cf-find" style="max-width:760px;margin:32px auto;padding:18px 20px;border:1px solid rgba(128,128,128,.3);border-radius:14px">'
       f'<h2 style="margin:0 0 6px;font-size:20px">Find ContentFellow in Burnley</h2><p style="margin:0">See our reviews and location on '
       f'<a href="{GBP}" rel="noopener" target="_blank">Google Maps</a> and our listing on <a href="{YELL}" rel="noopener" target="_blank">Yell</a>.</p></section>')
LOCAL = {"burnley", "about", "get-started"}
PLANS = ('<aside class="cf-plans" style="margin:28px 0;padding:16px 18px;border:1px solid rgba(128,128,128,.3);border-radius:14px"><strong>ContentFellow plans:</strong> '
         'social media from £59/month, websites £69/month or from £349 one-off, SEO + GEO £89/month, video editing £119/month, shoots £149/month, everything £389/month. '
         'Apps from £1,249. Free trial, no contract. <a href="/pricing/">See all plans and prices →</a></aside>')

def same_as(m):
    d = json.loads(m.group(1)); items = d.get("@graph", [d]) if isinstance(d, dict) else d; hit = False
    for i in items:
        if i.get("@type") in ("Organization", "ProfessionalService", "LocalBusiness"):
            i["sameAs"] = sorted(set(i.get("sameAs", []) + [GBP, YELL])); hit = True
    return '<script type="application/ld+json">' + json.dumps(d, ensure_ascii=False, separators=(",", ":")) + "</script>" if hit else m.group(0)

n = 0
for f in SITE.rglob("*.html"):
    s = o = f.read_text()
    if 'class="cf-prof"' not in s and "</footer>" in s:
        s = s.replace("</span></div></footer>", LINKS + "</span></div></footer>", 1) if "</span></div></footer>" in s else s.replace("</footer>", LINKS + "</footer>", 1)
    s = re.sub(r'<script type="application/ld\+json">(.*?)</script>', same_as, s, flags=re.S)
    if f.parent.parent.name == "blog" and 'class="cf-plans"' not in s and "</article>" in s:
        s = s.replace("</article>", PLANS + "</article>", 1)
    if f.parent.name in LOCAL and 'class="cf-find"' not in s: s = s.replace("</main>", BOX + "</main>", 1)
    if s != o: f.write_text(s); n += 1
print("pages updated:", n)

# /ai-check/: same form as /get-started/ but with the ChatGPT graphic as the link preview (WhatsApp/social)
_gs = SITE / "get-started" / "index.html" if "SITE" in globals() else None
if _gs and _gs.exists():
    _h = _gs.read_text().replace("https://contentfellow.com/studio.jpg", "https://contentfellow.com/img/outreach/search.png")
    _h = _h.replace('href="https://contentfellow.com/get-started/"', 'href="https://contentfellow.com/ai-check/"')
    (SITE / "ai-check").mkdir(exist_ok=True); (SITE / "ai-check" / "index.html").write_text(_h)
