"""Site-wide footer links to the Burnley pages (internal links help them rank). Marker <!--cf-local-->."""
import pathlib
L = '<!--cf-local--><p style="font-size:14px;margin:8px 0">Local: <a href="/blog/marketing-agency-burnley/">Marketing agency Burnley</a> · <a href="/blog/social-media-management-burnley/">Social media management Burnley</a> · <a href="/blog/web-designer-burnley/">Web designer Burnley</a> · <a href="/blog/videographer-burnley-lancashire-prices/">Videographer Burnley</a> · <a href="/burnley/">Digital marketing Burnley</a></p>'
n = 0
for f in pathlib.Path("outputs/_site").rglob("index.html"):
    if "/themes/" in str(f): continue
    s = f.read_text()
    if "<!--cf-local-->" in s or "</footer>" not in s: continue
    f.write_text(s.replace("</footer>", L + "</footer>", 1)); n += 1
print("local links added:", n)
