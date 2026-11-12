"""Make a short local landing page. Usage: make_local_page.py <slug> <Town> <kind:marketing|web> <miles> <ai_img>"""
import json, os, sys
S, T, kind, miles, img = sys.argv[1:6]
base = json.load(open('outputs/seo-agency-nelson/content/post.json')); bm = json.load(open('outputs/seo-agency-nelson/content/meta.json'))
if kind == "web":
    title = f"Web Designer in {T}, Lancashire: Prices From £225 (2026)"
    mt = f"Web Designer {T} | Websites From £225, Live in 2 Weeks"[:60]
    desc = f"Web designer for {T} small businesses: websites from £225, then £49/mo hosting and care. Code GhostFellow7 = 25% off. Call 07535 677302."
    q = f"How much does a web designer in {T} cost?"
    ans = f"A small business website from a web designer in {T} usually costs £300–£3,000. ContentFellow, a <a href=\"/blog/marketing-agency-burnley/\">Burnley marketing agency</a> about {miles} miles from {T}, builds sites from £225 (Basic), £520 (Standard) or £1,099 (Premium), then hosting and care from £49 a month. Use code GhostFellow7 for 25% off. Call 07535 677302."
    kw = [f"web designer {T.lower()}", f"website design {T.lower()}"]
else:
    title = f"Marketing Agency in {T}, Lancashire: Prices From £59/mo (2026)"
    mt = f"Marketing Agency {T} | Social, SEO & Web From £59/mo"[:60]
    desc = f"Marketing agency for {T} small businesses: social media £59/mo, SEO & AI Search £89/mo, websites from £225. No contract. Call 07535 677302."
    q = f"How much does a marketing agency in {T} cost?"
    ans = f"Most Lancashire marketing agencies charge £300–£1,000+ a month. ContentFellow, a <a href=\"/blog/marketing-agency-burnley/\">Burnley marketing agency</a> about {miles} miles from {T}, offers social media from £59 a month, SEO & AI Search for £89 a month and websites from £225. Call 07535 677302."
    kw = [f"marketing agency {T.lower()}", f"digital marketing {T.lower()}"]
d = f'outputs/{S}/content'; os.makedirs(d, exist_ok=True)
md = f'''---
title: "{title}"
slug: {S}
date: 2026-11-12
author: ContentFellow Team
market: en-GB
---

# {title}

## {q}

> **Quick answer:** {ans} *(Updated November 2026.)*

**TL;DR:** Fixed prices, no contract, no VAT, free 7-day trial. Covering {T} and the rest of Lancashire.

## Prices in {T} (2026)

| Service | ContentFellow | Typical Lancashire agency |
|---|---|---|
| Website | from £225, then £49/month | £1,000–£5,000 |
| Social Media Management | £59–£129/month | £300–£800/month |
| SEO & AI Search | £89/month | £300–£1,000/month |
| Photo & Video Shoots | £149/month | £390–£650 per half day |
| Full Marketing Team | £389/month | £1,500+/month |

See <a href="/pay-monthly-websites/">pay monthly websites</a> and our <a href="/blog/seo-geo-case-study-uk/">SEO & GEO case study</a>.

## What is included

- Mobile-first website or social posts set up for {T}
- Google Business Profile and local SEO
- Click-to-call and WhatsApp buttons
- Monthly report: clicks, calls and rankings
- No long contract, cancel any month

## Get started

Call or WhatsApp **07535 677302** or email **info@contentfellow.com**. Website builds: code **GhostFellow7** = 25% off.

## Frequently asked questions

### How much does it cost in {T}?
Websites start at £225, social media at £59 a month and SEO & AI Search at £89 a month, with no contract and no VAT.

### Do you work in {T}?
Yes. We are based in Burnley, about {miles} miles from {T}, and work across Lancashire.

### Is there a free trial?
Yes. Monthly plans start with a free 7-day trial, no card needed.

### Is there a discount on websites?
Yes. Use code GhostFellow7 for 25% off any website build.

### How do I contact you?
Call or WhatsApp 07535 677302 or email info@contentfellow.com.
'''
open(f'{d}/article.md', 'w').write(md)
p = dict(base); p.update(slug=S, title=title, title_short=title.split(':')[0], meta_title=mt, meta_description=desc, eyebrow=f"Local · {T}", subtitle=f"{T} prices",
  stats=[["Website", "from £225"], ["Social", "£59/mo"], ["SEO + AI", "£89/mo"], ["Contract", "None"]], points_title=f"What {T} businesses get", points_subtitle=title.split(':')[0],
  points=[["Website", "Fast|Mobile"], ["Google", "Maps|SEO"], ["AI", "ChatGPT"], ["Calls", "Call|WhatsApp"]], featured_alt=title.split(':')[0], diagram_alt=f"Services for {T} businesses", keywords=kw, tags=["Local", T], date="2026-11-12")
json.dump(p, open(f'{d}/post.json', 'w'), ensure_ascii=False)
m = dict(bm); m.update(title=title, meta_title=mt, meta_description=desc, slug=S, url=f"https://contentfellow.com/blog/{S}/", keywords=kw, tags=p['tags'],
  images=[{"file": f"{S}-featured.png", "alt": p['featured_alt']}, {"file": f"{S}-diagram.png", "alt": p['diagram_alt']}])
json.dump(m, open(f'{d}/meta.json', 'w'), indent=2, ensure_ascii=False)
import pathlib
a = pathlib.Path('tools/add_ai_images.py'); s = a.read_text()
if f'"blog/{S}"' not in s: a.write_text(s.replace('"burnley": "restaurant-burnley",', f'"blog/{S}": "{img}",\n "burnley": "restaurant-burnley",', 1))
l = pathlib.Path('outputs/_site/llms.txt'); s = l.read_text(); u = f"https://contentfellow.com/blog/{S}/"
if u not in s:
    i = s.find("\n- ["); s = s[:i+1] + f"- [{title.split(':')[0]}]({u}): {desc}\n" + s[i+1:]; l.write_text(s)
print("made", S)
