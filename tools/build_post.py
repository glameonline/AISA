"""Generic post builder. Usage: python3 tools/build_post.py <post_dir>
Reads <post_dir>/content/post.json + article.md, writes images/*.svg, content/article.html, content/meta.json.
post.json: slug, title, meta_title, meta_description, eyebrow, subtitle, stats [[label,value]x<=4],
           points_title, points_subtitle, points [[title,"line1|line2|line3"]x4], keywords[], tags[], category, cta, date"""
import json, re, sys, pathlib, html as H, markdown
d = pathlib.Path(sys.argv[1]); c = d / "content"; img = d / "images"; img.mkdir(exist_ok=True)
P = json.loads((c / "post.json").read_text()); slug = P["slug"]
BG, FG, AC, MUT, CARD = "#0c0c0d", "#f5f3ee", "#ff5a1f", "#9a968e", "#1c1c1f"
F = "font-family='Inter,Helvetica,Arial,sans-serif'"
e = lambda s: H.escape(s, quote=True)

def wrap(text, n):
    out, line = [], ""
    for w in text.split():
        if len(line) + len(w) + 1 > n: out.append(line); line = w
        else: line = (line + " " + w).strip()
    return out + [line]

# featured 1200x630
tl = wrap(P["title_short"] if "title_short" in P else P["meta_title"], 22)[:3]
t = "".join(f"<text x='70' y='{200+i*80}' {F} font-size='66' fill='{FG}' font-weight='800'>{e(x)}</text>" for i, x in enumerate(tl))
sy = 200 + len(tl) * 80 - 10
stats = P.get("stats", [])[:4]; w = 1060 // max(len(stats), 1)
boxes = "".join(f"<rect x='{70+i*w}' y='{sy+60}' width='{w-20}' height='90' rx='14' fill='{AC if i==P.get('highlight',1) else CARD}'/>"
                f"<text x='{90+i*w}' y='{sy+100}' {F} font-size='18' font-weight='700' fill='{BG if i==P.get('highlight',1) else MUT}'>{e(a.upper())}</text>"
                f"<text x='{90+i*w}' y='{sy+135}' {F} font-size='26' font-weight='700' fill='{BG if i==P.get('highlight',1) else FG}'>{e(b)}</text>" for i, (a, b) in enumerate(stats))
(img / f"{slug}-featured.svg").write_text(f"""<svg xmlns='http://www.w3.org/2000/svg' width='1200' height='630'><rect width='1200' height='630' fill='{BG}'/>
<circle cx='1040' cy='120' r='260' fill='{AC}' opacity='.12'/><circle cx='1040' cy='120' r='150' fill='none' stroke='{AC}' stroke-width='3' opacity='.6'/>
<text x='70' y='110' {F} font-size='26' fill='{AC}' font-weight='700' letter-spacing='3'>{e(P['eyebrow'].upper())}</text>{t}
<text x='70' y='{sy+30}' {F} font-size='28' fill='{MUT}'>{e(P['subtitle'])}</text>{boxes}
<text x='70' y='600' {F} font-size='20' fill='{MUT}'>contentfellow.com</text></svg>""")

# points diagram 1200x630
pts = P["points"][:4]; b = ""
for i, (tt, s) in enumerate(pts):
    x = 50 + i * 285
    b += f"<rect x='{x}' y='200' width='255' height='270' rx='18' fill='{CARD}' stroke='{AC if i==len(pts)-1 else '#2a2a2e'}' stroke-width='2'/>"
    b += f"<circle cx='{x+50}' cy='255' r='28' fill='{AC}'/><text x='{x+50}' y='265' {F} font-size='28' font-weight='800' fill='{BG}' text-anchor='middle'>{i+1}</text>"
    b += "".join(f"<text x='{x+24}' y='{330+j*28}' {F} font-size='22' font-weight='800' fill='{FG}'>{e(l)}</text>" for j, l in enumerate(wrap(tt, 19)[:2]))
    b += "".join(f"<text x='{x+24}' y='{400+j*28}' {F} font-size='18' fill='{MUT}'>{e(l)}</text>" for j, l in enumerate(s.split("|")[:3]))
(img / f"{slug}-diagram.svg").write_text(f"""<svg xmlns='http://www.w3.org/2000/svg' width='1200' height='630'><rect width='1200' height='630' fill='{BG}'/>
<text x='50' y='90' {F} font-size='36' fill='{FG}' font-weight='800'>{e(P['points_title'])}</text>
<text x='50' y='132' {F} font-size='22' fill='{MUT}'>{e(P['points_subtitle'])}</text>{b}<text x='50' y='560' {F} font-size='20' fill='{MUT}'>contentfellow.com</text></svg>""")

alts = {f"{slug}-featured.png": P["featured_alt"], f"{slug}-diagram.png": P["diagram_alt"]}
md = (c / "article.md").read_text(); body = re.match(r"---\n.*?\n---\n(.*)", md, re.S).group(1)
for f, a in alts.items(): body = re.sub(rf"!\[[^\]]*\]\({re.escape(f)}\)", f"![{a}]({f})", body)
hb = markdown.markdown(body, extensions=["tables"])
hb = re.sub(r'<img alt="([^"]*)" src="([^"]*)" />', r'<img src="\2" alt="\1" width="1200" height="630" loading="lazy">', hb)
faqs = re.findall(r"### (.+?\?)\n(.+?)\n", body.split("## Frequently asked questions")[1]) if "## Frequently asked questions" in body else []
url = f"https://contentfellow.com/blog/{slug}/"; date = P["date"]
ld = [{"@context": "https://schema.org", "@type": "Article", "headline": P["title"], "description": P["meta_description"], "image": "https://contentfellow.com/studio.jpg",
       "datePublished": date, "dateModified": date, "inLanguage": "en-GB",
       "author": {"@type": "Organization", "name": "ContentFellow Search Team", "url": "https://contentfellow.com"},
       "publisher": {"@type": "Organization", "name": "ContentFellow", "logo": {"@type": "ImageObject", "url": "https://contentfellow.com/f.webp"}}, "mainEntityOfPage": url},
      {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
          {"@type": "ListItem", "position": 1, "name": "ContentFellow", "item": "https://contentfellow.com/"},
          {"@type": "ListItem", "position": 2, "name": "Blog", "item": "https://contentfellow.com/blog/"},
          {"@type": "ListItem", "position": 3, "name": P["meta_title"], "item": url}]}]
if faqs: ld.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]})
tmpl = pathlib.Path(__file__).with_name("post_template.html").read_text()
page = (tmpl.replace("{{TITLE}}", e(P["meta_title"])).replace("{{DESC}}", e(P["meta_description"])).replace("{{URL}}", url)
        .replace("{{LD}}", "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld)).replace("{{BODY}}", hb))
(c / "article.html").write_text(page)
(c / "meta.json").write_text(json.dumps({**{k: P[k] for k in ("title", "meta_title", "meta_description", "slug", "keywords", "tags", "category", "cta")},
    "url": url, "faq": [{"q": q, "a": a} for q, a in faqs], "images": [{"file": f, "alt": a} for f, a in alts.items()]}, indent=2, ensure_ascii=False))
print("ok", slug, "faqs", len(faqs), "words", len(re.sub(r"[#*|>\[\]()!-]", " ", body).split()), "meta_title", len(P["meta_title"]), "desc", len(P["meta_description"]))
