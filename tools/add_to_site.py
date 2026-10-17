"""Add built posts to outputs/_site (folder, blog index, sitemap, llms.txt). Usage: python3 tools/add_to_site.py <slug>:<tag> ..."""
import json, pathlib, shutil, sys, datetime
SITE = pathlib.Path("outputs/_site"); B = "https://contentfellow.com"; today = datetime.date.today().isoformat()
idx = SITE / "blog/index.html"; h = idx.read_text(); sm = SITE / "sitemap.xml"; s = sm.read_text(); ll = SITE / "llms.txt"; l = ll.read_text(); new = ""
for arg in sys.argv[1:]:
    slug, tag = arg.split(":", 1); src = pathlib.Path("outputs") / slug; meta = json.loads((src / "content/meta.json").read_text())
    d = SITE / "blog" / slug; d.mkdir(parents=True, exist_ok=True); shutil.copy(src / "content/article.html", d / "index.html")
    for png in (src / "images").glob("*.png"): shutil.copy(png, d / png.name)
    if f"/blog/{slug}/" not in h: new += f'<article><p class="tag">{tag}</p><h2><a href="/blog/{slug}/">{meta["title"]}</a></h2><p>{meta["meta_description"]}</p></article>'
    if f"/blog/{slug}/" not in s: s = s.replace("</urlset>", f"<url><loc>{B}/blog/{slug}/</loc><lastmod>{today}</lastmod></url>\n</urlset>")
    if f"/blog/{slug}/" not in l: l = l.replace("## Guides\n", f"## Guides\n- [{meta['title']}]({B}/blog/{slug}/): {meta['meta_description']}\n", 1)
idx.write_text(h.replace("<article>", new + "<article>", 1)); sm.write_text(s); ll.write_text(l)
print("posts:", (h + new).count("<article>"), "sitemap urls:", s.count("<url>"))
