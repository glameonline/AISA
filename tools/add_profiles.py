"""Link ContentFellow's Google Maps and Yell profiles from every page in outputs/_site (idempotent).
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
    if f.parent.name in LOCAL and 'class="cf-find"' not in s: s = s.replace("</main>", BOX + "</main>", 1)
    if s != o: f.write_text(s); n += 1
print("pages updated:", n)
