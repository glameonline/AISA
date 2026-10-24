"""Audit every page in outputs/_site: title<=60, description<=155, canonical, one H1, valid JSON-LD, internal links resolve. Usage: python3 tools/seo_audit.py"""
import json, re, pathlib, html
SITE = pathlib.Path("outputs/_site"); issues = []
def exists(href):
    p = href.split("#")[0].split("?")[0]
    if not p or p == "/": return True
    p = p.replace("https://contentfellow.com", "")
    if not p.startswith("/"): return True
    t = SITE / p.lstrip("/")
    return t.is_file() or (t / "index.html").is_file()
for f in sorted(SITE.rglob("*.html")):
    s = f.read_text(); rel = str(f.relative_to(SITE))
    if 'name="robots" content="noindex' in s: continue
    t = re.search(r"<title>(.*?)</title>", s, re.S); d = re.search(r'<meta name="description" content="([^"]*)"', s)
    tt = html.unescape(t.group(1).strip()) if t else ""; dd = html.unescape(d.group(1)) if d else ""
    if not tt or len(tt) > 60: issues.append((rel, f"title {len(tt)}: {tt}"))
    if not dd or len(dd) > 155: issues.append((rel, f"description {len(dd)}"))
    if 'rel="canonical"' not in s: issues.append((rel, "no canonical"))
    h1 = len(re.findall(r"<h1[\s>]", s))
    if h1 != 1: issues.append((rel, f"{h1} H1"))
    for j in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        try: json.loads(j)
        except Exception as e: issues.append((rel, f"bad JSON-LD: {e}"))
    for href in re.findall(r'href="([^"]+)"', s):
        if (href.startswith("/") or href.startswith("https://contentfellow.com/")) and not re.search(r"\.(webp|jpg|png|css|js|xml|txt)$", href) and not exists(href):
            issues.append((rel, f"broken link {href}"))
for r, i in issues: print(f"{r}: {i}")
print(f"{len(issues)} issues")
