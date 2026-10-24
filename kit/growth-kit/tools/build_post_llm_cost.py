"""Build images (SVG) + publish-ready HTML + meta for a post folder. Usage: python3 tools/build_post.py <post_dir>"""
import json, re, sys, pathlib, markdown
d = pathlib.Path(sys.argv[1]); slug = "llm-optimisation-cost-small-business-uk"
img = d / "images"; c = d / "content"
BG, FG, AC, MUT = "#0c0c0d", "#f5f3ee", "#ff5a1f", "#9a968e"
F = "font-family='Inter,Helvetica,Arial,sans-serif'"

# Featured 1200x630
(img / f"{slug}-featured.svg").write_text(f"""<svg xmlns='http://www.w3.org/2000/svg' width='1200' height='630'>
<rect width='1200' height='630' fill='{BG}'/><circle cx='1040' cy='120' r='260' fill='{AC}' opacity='.12'/>
<circle cx='1040' cy='120' r='150' fill='none' stroke='{AC}' stroke-width='3' opacity='.6'/>
<text x='70' y='110' {F} font-size='26' fill='{AC}' font-weight='700' letter-spacing='3'>UK PRICE GUIDE · 2026</text>
<text x='70' y='220' {F} font-size='68' fill='{FG}' font-weight='800'>How much does LLM</text>
<text x='70' y='300' {F} font-size='68' fill='{FG}' font-weight='800'>optimisation cost?</text>
<text x='70' y='370' {F} font-size='32' fill='{MUT}'>GEO &amp; AI search for small businesses, in pounds</text>
<g {F} font-size='26' font-weight='700'>
<rect x='70' y='430' width='230' height='90' rx='14' fill='#1c1c1f'/><text x='90' y='470' fill='{MUT}' font-size='18'>DIY</text><text x='90' y='505' fill='{FG}'>£0–£100</text>
<rect x='320' y='430' width='250' height='90' rx='14' fill='{AC}'/><text x='340' y='470' fill='{BG}' font-size='18'>PRODUCTISED PLAN</text><text x='340' y='505' fill='{BG}'>£89–£400</text>
<rect x='590' y='430' width='250' height='90' rx='14' fill='#1c1c1f'/><text x='610' y='470' fill='{MUT}' font-size='18'>FREELANCER</text><text x='610' y='505' fill='{FG}'>£300–£1,000</text>
<rect x='860' y='430' width='270' height='90' rx='14' fill='#1c1c1f'/><text x='880' y='470' fill='{MUT}' font-size='18'>AGENCY</text><text x='880' y='505' fill='{FG}'>£1,100–£3,800</text></g>
<text x='70' y='585' {F} font-size='22' fill='{MUT}'>contentfellow.com · per month, as of October 2026</text></svg>""")

# Range chart
rows = [("DIY with tools", 0, 100), ("Productised SEO + GEO plan", 89, 400), ("Freelancer", 300, 1000),
        ("Small-business agency", 1100, 3800), ("Mid-market agency", 3800, 11000)]
X0, W, MAX = 420, 700, 11000
def x(v): return X0 + W * (v / MAX) ** 0.5  # sqrt scale so small tiers stay visible
bars = ""
for i, (n, lo, hi) in enumerate(rows):
    y = 150 + i * 80; col = AC if i == 1 else "#3a3a40"
    bars += f"<text x='60' y='{y+28}' {F} font-size='24' fill='{FG}'>{n}</text>"
    bars += f"<rect x='{x(lo):.0f}' y='{y}' width='{max(x(hi)-x(lo),10):.0f}' height='40' rx='8' fill='{col}'/>"
    bars += f"<text x='{x(hi)+12:.0f}' y='{y+28}' {F} font-size='22' fill='{FG}' font-weight='700'>£{lo:,}–£{hi:,}</text>" if hi < 5000 else f"<text x='{x(lo)-12:.0f}' y='{y+28}' {F} font-size='22' fill='{FG}' font-weight='700' text-anchor='end'>£{lo:,}–£{hi:,}+</text>"
ticks = "".join(f"<line x1='{x(t):.0f}' y1='140' x2='{x(t):.0f}' y2='560' stroke='#2a2a2e'/><text x='{x(t):.0f}' y='590' {F} font-size='18' fill='{MUT}' text-anchor='middle'>£{t:,}</text>" for t in (0, 500, 2000, 5000, 11000))
(img / "llm-optimisation-cost-uk-chart.svg").write_text(f"""<svg xmlns='http://www.w3.org/2000/svg' width='1200' height='630'>
<rect width='1200' height='630' fill='{BG}'/>
<text x='60' y='70' {F} font-size='34' fill='{FG}' font-weight='800'>LLM optimisation cost in the UK, per month</text>
<text x='60' y='108' {F} font-size='20' fill='{MUT}'>Typical small-business ranges, Oct 2026 · sources: WebFX, Nutshell, TeamAI, Seotal</text>
{ticks}{bars}</svg>""")

# Process diagram
steps = [("1", "Technical access", "AI crawlers allowed, An llms.txt file, Fast pages"), ("2", "Structured data", "Organisation, FAQ, Service schema"),
         ("3", "Answer-first content", "Answer in sentence one, Prices and dates, Comparison tables"), ("4", "Authority + tracking", "Reviews and mentions, UK directories, AI prompt report")]
boxes = ""
for i, (n, t, s) in enumerate(steps):
    bx = 50 + i * 285
    boxes += f"<rect x='{bx}' y='200' width='255' height='260' rx='18' fill='#1c1c1f' stroke='{AC if i==3 else '#2a2a2e'}' stroke-width='2'/>"
    boxes += f"<circle cx='{bx+50}' cy='255' r='28' fill='{AC}'/><text x='{bx+50}' y='265' {F} font-size='28' font-weight='800' fill='{BG}' text-anchor='middle'>{n}</text>"
    boxes += f"<text x='{bx+24}' y='330' {F} font-size='22' font-weight='800' fill='{FG}'>{t}</text>"
    words = s.split(", "); boxes += "".join(f"<text x='{bx+24}' y='{370+j*30}' {F} font-size='19' fill='{MUT}'>{w}</text>" for j, w in enumerate(words))
    if i < 3: boxes += f"<text x='{bx+262}' y='340' {F} font-size='30' fill='{AC}'>›</text>"
(img / "llm-optimisation-process-diagram.svg").write_text(f"""<svg xmlns='http://www.w3.org/2000/svg' width='1200' height='630'>
<rect width='1200' height='630' fill='{BG}'/>
<text x='50' y='90' {F} font-size='36' fill='{FG}' font-weight='800'>The four layers of LLM optimisation</text>
<text x='50' y='132' {F} font-size='22' fill='{MUT}'>What any GEO plan should include, whatever it costs</text>
{boxes}<text x='50' y='560' {F} font-size='20' fill='{MUT}'>contentfellow.com</text></svg>""")

alts = {f"{slug}-featured.png": "UK LLM optimisation cost guide 2026: DIY £0–£100, plan £89–£400, freelancer, agency £1,100–£3,800",
        "llm-optimisation-cost-uk-chart.png": "Bar chart of UK LLM optimisation cost per month by option, from DIY to agency, 2026",
        "llm-optimisation-process-diagram.png": "Diagram of the four layers of LLM optimisation: technical, structured data, content, authority"}

# HTML
md = (c / "article.md").read_text(); fm, body = re.match(r"---\n(.*?)\n---\n(.*)", md, re.S).groups()
for f, a in alts.items(): body = re.sub(rf"!\[[^\]]*\]\({re.escape(f)}\)", f"![{a}]({f})", body)
html_body = markdown.markdown(body, extensions=["tables", "fenced_code"])
html_body = re.sub(r'<img alt="([^"]*)" src="([^"]*)" />', r'<img src="\2" alt="\1" width="1200" height="630" loading="lazy">', html_body)
faqs = re.findall(r"### (.+?\?)\n(.+?)\n", body.split("## Frequently asked questions")[1])
url = f"https://contentfellow.com/blog/{slug}/"
title = "How Much Does LLM Optimisation Cost? UK Prices 2026"
desc = "UK LLM optimisation (GEO) costs £0–£100/mo DIY, £89–£400 on a plan, £1,100–£3,800 with an agency. See what each tier includes and what to budget."
ld = [{"@context": "https://schema.org", "@type": "Article", "headline": "How Much Does LLM Optimisation Cost for Small Businesses? (UK Prices, 2026)",
       "description": desc, "image": url + f"{slug}-featured.png", "datePublished": "2026-10-16", "dateModified": "2026-10-16", "inLanguage": "en-GB",
       "author": {"@type": "Organization", "name": "ContentFellow Search Team", "url": "https://contentfellow.com"},
       "publisher": {"@type": "Organization", "name": "ContentFellow", "logo": {"@type": "ImageObject", "url": "https://contentfellow.com/f.webp"}},
       "mainEntityOfPage": url, "about": ["Generative engine optimisation", "LLM optimisation", "AI search optimisation"]},
      {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]},
      {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
          {"@type": "ListItem", "position": 1, "name": "ContentFellow", "item": "https://contentfellow.com/"},
          {"@type": "ListItem", "position": 2, "name": "Blog", "item": "https://contentfellow.com/blog/"},
          {"@type": "ListItem", "position": 3, "name": "LLM optimisation cost", "item": url}]}]
page = f"""<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title><meta name="description" content="{desc}"><link rel="canonical" href="{url}"><link rel="alternate" hreflang="en-GB" href="{url}">
<meta name="robots" content="index,follow,max-image-preview:large"><meta property="og:type" content="article"><meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}"><meta property="og:url" content="{url}"><meta property="og:image" content="{url}{slug}-featured.png">
<meta property="og:locale" content="en_GB"><meta name="twitter:card" content="summary_large_image"><link rel="icon" href="https://contentfellow.com/f.webp">
{''.join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld)}
<style>:root{{--bg:#0c0c0d;--fg:#f5f3ee;--mut:#9a968e;--ac:#ff5a1f;--card:#1c1c1f}}body{{margin:0;background:var(--bg);color:var(--fg);font:18px/1.7 Inter,Helvetica,Arial,sans-serif}}
header,main,footer{{max-width:760px;margin:auto;padding:0 20px}}header{{padding:24px 20px}}header a{{color:var(--fg);font-weight:800;text-decoration:none}}
h1{{font-size:clamp(30px,5vw,46px);line-height:1.15}}h2{{margin-top:2.2em;line-height:1.25}}a{{color:var(--ac)}}blockquote{{margin:0;background:var(--card);border-left:4px solid var(--ac);padding:4px 20px;border-radius:8px}}
img{{max-width:100%;height:auto;border-radius:12px}}table{{width:100%;border-collapse:collapse;font-size:15px;display:block;overflow-x:auto}}th,td{{border-bottom:1px solid #2a2a2e;padding:10px;text-align:left;vertical-align:top}}th{{color:var(--mut)}}
code{{background:var(--card);padding:2px 6px;border-radius:4px}}footer{{color:var(--mut);padding:40px 20px}}</style></head>
<body><header><a href="https://contentfellow.com/">ContentFellow</a> · <a href="https://contentfellow.com/blog/" style="font-weight:400;color:var(--mut)">Blog</a></header>
<main><article>{html_body}</article></main><footer>© 2026 ContentFellow · Production · Editing · Social · Web · SEO &amp; GEO</footer></body></html>"""
(c / "article.html").write_text(page)
kw = ["llm optimisation cost", "geo optimisation cost", "generative engine optimisation pricing uk", "ai search optimisation cost", "aeo pricing", "how much does geo cost"]
(c / "meta.json").write_text(json.dumps({"title": "How Much Does LLM Optimisation Cost for Small Businesses? (UK Prices, 2026)", "meta_title": title,
    "meta_description": desc, "slug": slug, "url": url, "market": "en-GB", "primary_keyword": kw[0], "keywords": kw,
    "faq": [{"q": q, "a": a} for q, a in faqs], "images": [{"file": f, "alt": a} for f, a in alts.items()],
    "category": "SEO & GEO", "tags": ["GEO", "LLM optimisation", "AI search", "SEO pricing", "UK small business"], "cta": "Search Fellow £89/mo"}, indent=2, ensure_ascii=False))
print("faqs", len(faqs), "words", len(re.sub(r"[#*|>\[\]()!-]", " ", body).split()), "meta_title", len(title), "desc", len(desc))
