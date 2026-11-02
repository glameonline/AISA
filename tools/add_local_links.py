"""Site-wide footer links to the Burnley pages (internal links help them rank). Marker <!--cf-local-->."""
import pathlib, re
L = '<!--cf-local--><p style="font-size:14px;margin:8px 0">Local: <a href="/blog/marketing-agency-burnley/">Marketing agency Burnley</a> · <a href="/blog/social-media-management-burnley/">Social media management Burnley</a> · <a href="/blog/web-designer-burnley/">Web designer Burnley</a> · <a href="/blog/videographer-burnley-lancashire-prices/">Videographer Burnley</a> · <a href="/burnley/">Digital marketing Burnley</a> · <a href="/blog/marketing-agency-nelson/">Marketing agency Nelson</a> · <a href="/blog/marketing-agency-colne/">Marketing agency Colne</a> · <a href="/blog/cheapest-marketing-agency-burnley/">Cheapest marketing Burnley</a></p>'
n = 0
for f in pathlib.Path("outputs/_site").rglob("index.html"):
    if "/themes/" in str(f): continue
    s = f.read_text()
    if "</footer>" not in s: continue
    s2 = re.sub(r"<!--cf-local--><p[^>]*>.*?</p>", "", s, count=1)
    s2 = s2.replace("</footer>", L + "</footer>", 1)
    if s2 != s: f.write_text(s2); n += 1
print("local links added:", n)
