"""Builds the lead-gen pages into outputs/_site: /services/<fellow>/, /services/, /get-started/ (+ thanks, submit.php),
and adds a free-check CTA box to every blog post. Usage: python3 tools/build_pages.py"""
import json, pathlib, re, html as H
SITE = pathlib.Path("outputs/_site"); BASE = "https://contentfellow.com"
e = lambda s: H.escape(s, quote=True)
CSS = """:root{--bg:#0c0c0d;--fg:#f5f3ee;--mut:#9a968e;--ac:#ff5a1f;--card:#1c1c1f}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:18px/1.7 Inter,Helvetica,Arial,sans-serif}
header,main,footer{max-width:820px;margin:auto;padding:0 20px}header{padding:24px 20px;display:flex;flex-wrap:wrap;gap:4px 14px}header a{color:var(--fg);font-weight:800;text-decoration:none;white-space:nowrap}header a+a{font-weight:400;color:var(--mut)}
h1{font-size:clamp(30px,5vw,46px);line-height:1.15}h2{margin-top:2em;line-height:1.25}a{color:var(--ac)}
.lead{background:var(--card);border-left:4px solid var(--ac);padding:12px 20px;border-radius:8px}
.price{font-size:40px;font-weight:800}.price small{font-size:18px;color:var(--mut);font-weight:400}
.btn{display:inline-block;background:var(--ac);color:#0c0c0d;font-weight:800;padding:14px 24px;border-radius:10px;text-decoration:none;border:0;font-size:18px;cursor:pointer}
.grid{display:grid;gap:14px;grid-template-columns:repeat(auto-fit,minmax(230px,1fr))}.card{background:var(--card);border:1px solid #2a2a2e;border-radius:14px;padding:18px}
.card h3{margin:0 0 6px}.mut{color:var(--mut)}table{width:100%;border-collapse:collapse;font-size:15px;display:block;overflow-x:auto}th,td{border-bottom:1px solid #2a2a2e;padding:10px;text-align:left}th{color:var(--mut)}
form{display:grid;gap:14px}label{font-size:15px;color:var(--mut);display:grid;gap:6px}input,select,textarea{font:16px Inter,Helvetica,Arial,sans-serif;background:#151517;color:var(--fg);border:1px solid #3a3a40;border-radius:10px;padding:12px}
fieldset{border:1px solid #3a3a40;border-radius:10px;padding:12px}fieldset label{display:flex;gap:8px;align-items:center;color:var(--fg)}.hp{position:absolute;left:-9999px}
.cta{background:var(--card);border:1px solid var(--ac);border-radius:14px;padding:20px;margin:32px 0}.cta h3{margin-top:0}footer{color:var(--mut);padding:40px 20px}"""
GA = "<script async src=\"https://www.googletagmanager.com/gtag/js?id=G-EZMWHSK0LD\"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments)}var c=null;try{c=localStorage.getItem('cf_consent')}catch(e){}gtag('consent','default',{analytics_storage:c==='yes'?'granted':'denied',ad_storage:'denied',ad_user_data:'denied',ad_personalization:'denied'});gtag('js',new Date());gtag('config','G-EZMWHSK0LD');</script>"
OFFER = "Free AI visibility check"
OFFER_LINE = "We ask ChatGPT and Gemini 10 questions your customers ask, and email you who they recommend instead of you, plus the 3 fixes that matter most. Free, within 2 working days."

def page(path, title, desc, body, ld=None, noindex=False, extra_head=""):
    url = f"{BASE}/{path}"
    lds = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in (ld or []))
    out = (f'<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
           f'<title>{e(title)}</title><meta name="description" content="{e(desc)}"><link rel="canonical" href="{url}">'
           f'<meta name="robots" content="{"noindex" if noindex else "index,follow,max-image-preview:large"}"><meta property="og:title" content="{e(title)}">'
           f'<meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{url}"><meta property="og:image" content="{BASE}/studio.jpg">'
           f'<meta property="og:locale" content="en_GB"><link rel="icon" href="{BASE}/f.webp">{GA}{lds}{extra_head}<style>{CSS}</style></head><body>'
           f'<header><a href="{BASE}/">ContentFellow</a><a href="/services/">Services</a><a href="/blog/">Guides</a><a href="/get-started/">Free check</a></header>'
           f'<main>{body}</main><footer>© 2026 ContentFellow · Burnley, Lancashire, UK · Monthly plans, no long contracts · <a href="/get-started/">Contact</a></footer></body></html>')
    p = SITE / path; p.mkdir(parents=True, exist_ok=True); (p / "index.html").write_text(out)

def cta_box(service=""):
    q = f"?service={service}" if service else ""
    return (f'<div class="cta"><h3>{OFFER}</h3><p>{OFFER_LINE}</p>'
            f'<p><a class="btn" href="/get-started/{q}">Get my free check →</a></p></div>')

F = [  # slug, name, short, price, what, includes, who, compare (label, typical), guide, faqs
 ("search-fellow", "Search Fellow", "SEO & GEO for AI search", "£89", "Get found on Google and recommended by ChatGPT, Claude, Gemini and Perplexity.",
  ["SEO for Google: technical fixes, service pages, local SEO", "GEO so AI assistants recommend you: structured data, answer-first pages, crawler access", "Bing indexing (what ChatGPT search uses) and directory clean-up", "Monthly report: rankings plus which AI prompts name you and which name competitors"],
  "UK small businesses that want more enquiries from Google and AI search without agency retainers.",
  [("UK SEO/GEO agency", "£1,100–£3,800 a month"), ("Freelance SEO", "£300–£1,000 a month"), ("Search Fellow", "£89 a month")],
  [("llm-optimisation-cost-small-business-uk", "How much LLM optimisation costs"), ("get-business-recommended-by-chatgpt-uk", "How to get recommended by ChatGPT"), ("geo-vs-seo-uk-small-business", "GEO vs SEO")],
  [("What is GEO?", "GEO stands for generative engine optimisation. It makes your business easy for AI assistants like ChatGPT, Claude and Gemini to find, understand and recommend."),
   ("How long until I see results?", "Technical fixes reach Google and Bing within days. Rankings and AI mentions usually move over 6 to 12 weeks."),
   ("Is there a contract?", "No long contract. Billing is monthly and you can change or cancel from the next month.")]),
 ("social-fellow", "Social Fellow", "Social media management", "£59", "Consistent, on-brand social media without hiring a social media manager.",
  ["Up to 3 platforms (e.g. Instagram, Facebook, TikTok or LinkedIn)", "Daily posting with the Manage + Post plan (£129/mo)", "Trend research: formats, sounds and topics", "You approve content before it goes live"],
  "Local and service businesses that know social matters but never have time to post.",
  [("UK agency (per channel)", "£1,250–£3,500 a month"), ("Freelancer", "£300–£1,000 a month"), ("Social Fellow", "£59 or £129 a month")],
  [("social-media-management-cost-uk", "What social media management costs in the UK")],
  [("What's the difference between Manage and Manage + Post?", "Both cover up to three platforms with trend research; Manage + Post (£129 a month) includes daily posting for you."),
   ("Do I approve posts?", "Yes. Content is shared with you for approval before it goes live."),
   ("Is ad spend included?", "No. Ad spend is paid to the platform and quoted separately.")]),
 ("build-fellow", "Build Fellow", "Website design, build and hosting", "£69", "A custom website with hosting, security and updates, for one monthly fee.",
  ["Custom website up to 5 pages", "Hosting, security and software updates included", "2 change requests every month", "Built for search: fast mobile pages, structured data, sitemap"],
  "Small businesses that need a professional site without a £3,000+ upfront bill.",
  [("UK agency build", "£3,000–£10,000 upfront + care plan"), ("Freelancer", "£500–£2,500 upfront"), ("Build Fellow", "£69 a month, nothing upfront")],
  [("small-business-website-cost-uk", "What a small business website costs in the UK")],
  [("Is there an upfront fee?", "No. The Build Fellow is £69 a month including the build, hosting, security and updates."),
   ("How many pages do I get?", "Up to five custom pages, plus two change requests every month."),
   ("Will the website help with Google and ChatGPT?", "Yes, it's built with fast pages, clear service pages, structured data and a sitemap. Add the Search Fellow for ongoing SEO and GEO.")]),
 ("studio-fellow", "Studio Fellow", "Photo and video production", "£149", "A professional on-site shoot every month: photos and 4K video of your business.",
  ["1 on-site shoot a month, up to 3 hours", "Photo and 4K video", "20 edited photos within 5 working days", "Based in Burnley, Lancashire"],
  "Businesses that need fresh, real content for social, website, Google Business Profile and ads.",
  [("Freelance videographer", "£200–£900 a day + editing"), ("Production company", "£2,000+ per project"), ("Studio Fellow", "£149 a month")],
  [("video-production-cost-uk", "What video production costs for UK small businesses")],
  [("Where do you shoot?", "On-site at your business. We're based in Burnley, Lancashire; ask us about your location."),
   ("How quickly do I get the photos?", "20 edited photos within five working days of the shoot."),
   ("Can I turn the footage into Reels?", "Yes, add the Creator Fellow for short videos, motion graphics and podcast edits.")]),
 ("creator-fellow", "Creator Fellow", "Video editing and motion graphics", "£119", "Short videos, motion graphics and podcast edits every month at a fixed price.",
  ["8 short videos for Reels, TikTok or Shorts", "1 motion graphics video", "1 podcast edit up to 60 minutes", "Two rounds of revisions per video"],
  "Businesses and creators who film content but don't have time to edit it.",
  [("Freelance editor", "£30–£150 per Reel"), ("Podcast edit (freelance)", "£75–£300 each"), ("Creator Fellow", "£119 a month for all of it")],
  [("video-editing-cost-uk", "What video editing costs in the UK")],
  [("What do I need to send you?", "Your raw footage and any brand fonts, colours or examples you like."),
   ("How many revisions are included?", "Two rounds of revisions on each video."),
   ("Can you film the footage too?", "Yes, add the Studio Fellow for a monthly on-site shoot.")]),
 ("growth-fellow", "Growth Fellow", "Your full marketing team", "£389", "All five Fellows plus a Growth lead, one strategy and one monthly report.",
  ["Studio, Creator, Social, Build and Search Fellows", "A Growth lead who sets one strategy across them", "Monthly call and one combined report", "£389 a month vs £555 separately (save £166)"],
  "Small businesses that want a complete marketing team without hiring one.",
  [("One in-house hire (loaded)", "~£4,300 a month"), ("Full-service agency", "£5,000–£25,000 a month"), ("Growth Fellow", "£389 a month")],
  [("outsourced-marketing-team-cost-uk", "Outsourced team vs agency vs in-house costs")],
  [("What's included in the Growth Fellow?", "All five Fellows (production, editing, social, website and SEO & GEO), a Growth lead, a monthly call and a combined report."),
   ("How much do I save?", "£166 a month compared with buying the five Fellows separately (£555)."),
   ("Can I start with one Fellow and upgrade?", "Yes. You can add, remove or upgrade Fellows from the next month.")]),
]

# Free trial per Fellow: (badge, what you get, how long). Change TRIAL_DAYS to switch the time-based trials (owner asked 3; data says 7 converts best).
TRIAL_DAYS = 7
TRIAL = {
 "search":  (f"Free {TRIAL_DAYS}-day trial", f"For {TRIAL_DAYS} days we work on your search for free: your AI visibility check (who ChatGPT and Gemini recommend instead of you), Bing Webmaster Tools set-up, AI crawler access fixed, and your Google Business Profile tidied. You keep every fix."),
 "social":  (f"Free {TRIAL_DAYS}-day trial", f"For {TRIAL_DAYS} days we plan and post for you on one platform: a short content plan, 5 posts written and designed for your approval, and trend ideas for your industry. You keep all the content."),
 "build":   ("Free homepage preview", "We design a preview of your new homepage, with your brand, services and prices, within 3 working days. You only pay if you go ahead."),
 "studio":  ("Free mini shoot", "A free 30-minute mini shoot at your business (within 20 miles of Burnley): 5 edited photos and 1 short vertical video, delivered within 5 working days. You keep them."),
 "creator": ("3 free videos", "Send us your footage and we edit 3 short videos for Reels, TikTok or Shorts, with captions and two rounds of revisions. You keep all 3 either way."),
 "growth":  (f"Free {TRIAL_DAYS}-day trial", f"For {TRIAL_DAYS} days you get a taste of the whole team: your AI visibility check, 2 free short videos, a week of posts on one platform, a homepage preview and a 30-minute strategy call with your Growth lead."),
}
TRIAL_TERMS = "No card needed. One free trial per business, UK businesses only. We take a limited number of new trials each week so every one gets proper attention."

def trial_block(key):
    badge, what = TRIAL[key]
    return (f'<div class="cta" id="trial"><p class="mut" style="margin:0">{e(badge)}</p><h3>Try it free first</h3><p>{e(what)}</p>'
            f'<p><a class="btn" href="/get-started/?service={key}&amp;offer=trial">Start my free trial →</a></p><p class="mut" style="font-size:14px">{e(TRIAL_TERMS)}</p></div>')

def service_pages():
    cards = ""
    for slug, name, short, price, what, inc, who, comp, guides, faqs in F:
        url = f"{BASE}/services/{slug}/"
        num = re.sub(r"[^\d.]", "", price)
        ld = [{"@context": "https://schema.org", "@type": "Service", "name": f"{name}: {short}", "serviceType": short, "description": what,
               "provider": {"@type": "Organization", "@id": f"{BASE}/#org", "name": "ContentFellow", "url": f"{BASE}/"}, "areaServed": "GB", "url": url,
               "offers": {"@type": "Offer", "price": num, "priceCurrency": "GBP", "url": url,
                          "priceSpecification": {"@type": "UnitPriceSpecification", "price": num, "priceCurrency": "GBP", "unitText": "MONTH"}}},
              {"@context": "https://schema.org", "@type": "Offer", "name": f"{name}: {TRIAL[slug.split('-')[0]][0]}", "description": TRIAL[slug.split('-')[0]][1],
               "price": "0", "priceCurrency": "GBP", "url": f"{url}#trial", "eligibleRegion": "GB", "seller": {"@type": "Organization", "@id": f"{BASE}/#org"}},
              {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs + [("Is there a free trial?", TRIAL[slug.split('-')[0]][1] + " " + TRIAL_TERMS)]]},
              {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
                  {"@type": "ListItem", "position": 1, "name": "ContentFellow", "item": f"{BASE}/"},
                  {"@type": "ListItem", "position": 2, "name": "Services", "item": f"{BASE}/services/"},
                  {"@type": "ListItem", "position": 3, "name": name, "item": url}]}]
        key = slug.split("-")[0]
        body = (f'<p class="mut">ContentFellow · {e(short)} · UK</p><h1>{e(name)}: {e(short)} for UK small businesses</h1>'
                f'<p class="lead"><strong>{e(name)} costs {price} a month.</strong> {e(what)} Monthly billing, no long contract, and you approve work before it goes live.</p>'
                f'<p class="price">{price}<small> / month</small></p><p><strong style="color:var(--ac)">{e(TRIAL[key][0])}</strong> · no card needed</p>'
                f'<p><a class="btn" href="/get-started/?service={key}&amp;offer=trial">Start my free trial →</a></p>{trial_block(key)}'
                f'<h2>What\'s included</h2><ul>{"".join(f"<li>{e(x)}</li>" for x in inc)}</ul>'
                f'<h2>Who it\'s for</h2><p>{e(who)}</p>'
                f'<h2>How it compares on price</h2><table><tr><th>Option</th><th>Typical UK cost</th></tr>{"".join(f"<tr><td>{e(a)}</td><td>{e(b)}</td></tr>" for a, b in comp)}</table>'
                f'<p class="mut">Typical UK prices from our guides: {", ".join(f"<a href=\'/blog/{g}/\'>{e(t)}</a>" for g, t in guides)}.</p>'
                f'<div class="cf-reviews" data-service="{key}" hidden></div>'
                f'<h2>How it works</h2><ol><li><strong>Tell us about your business</strong> (2-minute form).</li><li><strong>Get your free trial</strong>: {e(TRIAL[key][0].lower())}, no card needed.</li><li><strong>Like it? Start monthly</strong> at {price} a month; change or cancel from the next month.</li></ol>'
                f'{cta_box(key)}<h2>Frequently asked questions</h2>{"".join(f"<h3>{e(q)}</h3><p>{e(a)}</p>" for q, a in faqs + [("Is there a free trial?", TRIAL[key][1] + " " + TRIAL_TERMS)])}'
                f'<p><a href="/services/">See all Fellows →</a></p>')
        page(f"services/{slug}", f"{name}: {short} UK | {price}/month | ContentFellow", f"{name} by ContentFellow: {what} {price} a month, monthly billing, UK.", body, ld)
        cards += (f'<a class="card" href="/services/{slug}/" style="text-decoration:none;color:inherit"><h3>{e(name)} · {price}/mo</h3><p class="mut">{e(short)}</p><p>{e(what)}</p>'
                  f'<p style="color:var(--ac);font-weight:700;margin:0">{e(TRIAL[key][0])} →</p></a>')
    ld = [{"@context": "https://schema.org", "@type": "ItemList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": f"{BASE}/services/{x[0]}/", "name": x[1]} for i, x in enumerate(F)]}]
    page("services", "ContentFellow Services & Prices: Monthly Marketing Plans from £59 (UK)",
         "Hire a Fellow: SEO & GEO £89, social media £59, websites £69, photo & video £149, editing £119, or the full team £389 a month.",
         f'<h1>Monthly marketing plans for UK small businesses</h1><p class="lead">Hire a Fellow from <strong>£59 a month</strong>: one specialist, or the whole team for £389. Monthly billing, no long contracts, and <strong>every Fellow has a free trial</strong>, no card needed.</p><div class="grid">{cards}</div>{cta_box()}', ld)

def get_started():
    opts = "".join(f'<label><input type="checkbox" name="services[]" value="{s.split("-")[0]}"> {n} ({p}/mo)</label>' for s, n, _, p, *_ in F)
    form = (f'<h1>Start free: trial or AI visibility check</h1><p class="lead"><strong>Every Fellow has a free trial</strong>: 3 free edited videos, a free mini shoot, a free homepage preview, or {TRIAL_DAYS} free days of search or social. No card needed. Or ask for the {OFFER.lower()}: {OFFER_LINE[0].lower()+OFFER_LINE[1:]}</p>'
            '<form method="post" action="/get-started/submit.php" id="cf-form">'
            '<label>I want<select name="offer" id="cf-offer"><option value="trial">A free trial of a Fellow</option><option value="check">The free AI visibility check</option><option value="call">A 15-minute call</option></select></label>'
            '<label>Your name<input name="name" required autocomplete="name"></label>'
            '<label>Business name<input name="business" required autocomplete="organization"></label>'
            '<label>Website (if you have one)<input name="website" type="url" placeholder="https://" autocomplete="url"></label>'
            '<label>Email<input name="email" type="email" required autocomplete="email"></label>'
            '<label>Phone or WhatsApp (optional)<input name="phone" type="tel" autocomplete="tel"></label>'
            '<label>Town or area you serve<input name="area" required placeholder="e.g. Burnley, Manchester, UK-wide"></label>'
            f'<fieldset><legend class="mut">What do you need help with?</legend>{opts}</fieldset>'
            '<label>Monthly budget<select name="budget"><option>Under £100</option><option>£100–£250</option><option>£250–£500</option><option>£500+</option><option>Not sure yet</option></select></label>'
            '<label>Anything else? (optional)<textarea name="message" rows="3"></textarea></label>'
            '<input class="hp" name="company_url" tabindex="-1" autocomplete="off" aria-hidden="true">'
            '<input type="hidden" name="source" id="cf-src">'
            '<label style="display:flex;gap:8px;align-items:flex-start;color:var(--fg)"><input type="checkbox" name="consent" value="yes" required> I agree ContentFellow can contact me about my free check. We never share your details.</label>'
            '<button class="btn" type="submit">Send me my free check →</button></form>'
            '<p class="mut">Prefer to talk? Reply to our email and we\'ll book a 15-minute call.</p>'
            '<script>(function(){var q=new URLSearchParams(location.search),s=q.get("service");if(s){var b=document.querySelector(\'input[value="\'+s+\'"]\');if(b)b.checked=true}if(q.get("offer")==="trial"||s)document.getElementById("cf-offer").value="trial";else document.getElementById("cf-offer").value="check";'
            'document.getElementById("cf-src").value=[q.get("utm_source")||"",q.get("utm_campaign")||"",document.referrer].join("|")})();</script>')
    page("get-started", f"{OFFER} for UK Small Businesses | ContentFellow", "See who ChatGPT and Gemini recommend instead of you, and the 3 fixes that matter most. Free, within 2 working days.", form)
    page("get-started/thanks", "Thanks: your free check is on its way | ContentFellow", "Thanks for your request.",
         '<h1>Thanks, we\'ve got it.</h1><p class="lead">We\'ll email you within 1 working day to start your free trial or send your free AI visibility check. Check your spam folder if you don\'t see it.</p>'
         '<p>While you wait: <a href="/blog/get-business-recommended-by-chatgpt-uk/">how to get your business recommended by ChatGPT</a>.</p>'
         '<script>gtag("event","generate_lead",{currency:"GBP",value:89});</script>', noindex=True)
    (SITE / "get-started/submit.php").write_text(SUBMIT)

SUBMIT = r"""<?php
// Lead form handler: emails the lead and appends it to a CSV OUTSIDE public_html. Config: set $TO below.
$TO = 'contentfellow1@gmail.com';            // <-- confirm the inbox that should receive leads
$CSV = dirname($_SERVER['DOCUMENT_ROOT']) . '/cf-leads.csv';
if ($_SERVER['REQUEST_METHOD'] !== 'POST') { header('Location: /get-started/'); exit; }
if (!empty($_POST['company_url'])) { header('Location: /get-started/thanks/'); exit; }   // honeypot: bots
$f = function ($k, $n = 300) { return trim(mb_substr(strip_tags((string)($_POST[$k] ?? '')), 0, $n)); };
$email = filter_var($f('email'), FILTER_VALIDATE_EMAIL);
if (!$email || !$f('name') || ($_POST['consent'] ?? '') !== 'yes') { header('Location: /get-started/?error=1'); exit; }
$services = implode(', ', array_map('strip_tags', (array)($_POST['services'] ?? [])));
$row = [date('c'), $f('offer'), $f('name'), $f('business'), $f('website'), $email, $f('phone'), $f('area'), $services, $f('budget'), $f('message', 1000), $f('source'), $_SERVER['REMOTE_ADDR'] ?? ''];
$new = !is_file($CSV); $fh = @fopen($CSV, 'a');
if ($fh) { if ($new) fputcsv($fh, ['time','offer','name','business','website','email','phone','area','services','budget','message','source','ip']); fputcsv($fh, $row); fclose($fh); }
$body = "New free-check request\n\n" . implode("\n", array_map(fn($k, $v) => "$k: $v", ['Wants','Name','Business','Website','Email','Phone','Area','Services','Budget','Message','Source'], array_slice($row, 1, 11)));
@mail($TO, "New lead ({$row[1]}): {$row[3]} ({$services})", $body, "From: ContentFellow <no-reply@contentfellow.com>\r\nReply-To: $email\r\nContent-Type: text/plain; charset=utf-8");
header('Location: /get-started/thanks/');
"""

def blog_ctas():
    for p in SITE.glob("blog/*/index.html"):
        s = p.read_text()
        if 'class="cf-cta"' in s: continue
        box = (f'<div class="cf-cta" style="background:#1c1c1f;border:1px solid #ff5a1f;border-radius:14px;padding:20px;margin:32px 0">'
               f'<h3 style="margin-top:0">{OFFER}</h3><p>{OFFER_LINE}</p><p><a href="/get-started/" style="display:inline-block;background:#ff5a1f;color:#0c0c0d;font-weight:800;padding:12px 22px;border-radius:10px;text-decoration:none">Get my free check →</a></p></div>')
        s = s.replace("<h2>Frequently asked questions</h2>", box + "<h2>Frequently asked questions</h2>", 1)
        p.write_text(s)

TOWNS = ["Burnley", "Padiham", "Nelson", "Brierfield", "Colne", "Accrington", "Clitheroe", "Blackburn", "Rawtenstall", "Haslingden", "Todmorden"]

def local_page():
    url = f"{BASE}/burnley/"
    rows = "".join(f'<tr><td><a href="/services/{s}/">{e(n)}</a></td><td>{e(sh)}</td><td>{p}/mo</td><td>{e(TRIAL[s.split("-")[0]][0])}</td><td>{"On-site in Burnley + 20 miles" if s.startswith("studio") else "Remote, UK-wide"}</td></tr>'
                   for s, n, sh, p, *_ in F)
    faqs = [("Do you work with businesses in Burnley?", "Yes. ContentFellow is based in Burnley, Lancashire. Shoots happen on-site at your business; editing, social, websites and SEO are done remotely."),
            ("Which areas do you cover for photo and video shoots?", f"On-site shoots cover Burnley and about 20 miles around it, including {', '.join(TOWNS[1:])}. Ask us about other locations."),
            ("How much does marketing cost for a small business in Burnley?", "ContentFellow plans start at £59 a month for social media, £69 for a website, £89 for SEO and GEO, £119 for video editing, £149 for a monthly shoot, or £389 for the full team."),
            ("Can you help my Burnley business show up on Google Maps and ChatGPT?", "Yes. The Search Fellow covers local SEO, your Google Business Profile, Bing Places and the listings and pages AI assistants use to recommend local businesses.")]
    ld = [{"@context": "https://schema.org", "@type": "ProfessionalService", "@id": f"{BASE}/#org", "name": "ContentFellow", "url": f"{BASE}/", "logo": f"{BASE}/f.webp",
           "description": "Monthly marketing plans for small businesses: photo and video shoots, video editing, social media, websites, and SEO & GEO.",
           "address": {"@type": "PostalAddress", "addressLocality": "Burnley", "addressRegion": "Lancashire", "addressCountry": "GB"},
           "areaServed": [{"@type": "City", "name": t} for t in TOWNS] + [{"@type": "Country", "name": "United Kingdom"}], "priceRange": "£59–£389 a month"},
          {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}]
    body = (f'<p class="mut">Burnley · Lancashire · UK</p><h1>Marketing, video and websites for Burnley and Lancashire businesses</h1>'
            f'<p class="lead"><strong>ContentFellow is based in Burnley.</strong> Hire a Fellow from £59 a month: on-site photo and video shoots across Burnley and East Lancashire, plus video editing, social media, websites and SEO & GEO for businesses anywhere in the UK. Monthly billing, and every Fellow has a free trial.</p>'
            f'<p><a class="btn" href="/get-started/?offer=trial">Start a free trial →</a></p>'
            f'<h2>Services and prices</h2><table><tr><th>Fellow</th><th>What it is</th><th>Price</th><th>Free trial</th><th>Where</th></tr>{rows}</table>'
            f'<h2>Areas we cover for shoots</h2><p>{", ".join(TOWNS)}, and nearby. Everything else (editing, social, websites, SEO and GEO) is delivered remotely across the UK.</p>'
            f'<h2>Why local businesses use a Fellow</h2><ul><li><strong>Real content of your business</strong>, shot on-site, not stock photos.</li><li><strong>One monthly price</strong> instead of agency retainers or a full-time hire.</li><li><strong>You approve everything</strong> before it goes live.</li><li><strong>Found on Google Maps and in AI answers</strong>: the Search Fellow handles local SEO, Google Business Profile and Bing Places.</li></ul>'
            f'<div class="cf-reviews" data-service="all" hidden></div>{cta_box()}'
            f'<h2>Frequently asked questions</h2>{"".join(f"<h3>{e(q)}</h3><p>{e(a)}</p>" for q, a in faqs)}'
            f'<p>Guides: <a href="/blog/get-business-recommended-by-chatgpt-uk/">get recommended by ChatGPT</a> · <a href="/blog/video-production-cost-uk/">video production costs</a> · <a href="/blog/small-business-website-cost-uk/">website costs</a></p>')
    page("burnley", "Marketing, Video & Websites in Burnley, Lancashire | ContentFellow", "Burnley-based ContentFellow: on-site photo and video shoots, editing, social media, websites and SEO & GEO from £59 a month. Free trial on every service.", body, ld)

def about_page():
    facts = [("Name", "ContentFellow (one word; not related to Contentful, the software company)"), ("What it is", "A UK marketing service for small businesses, sold as monthly plans called \"Fellows\""),
             ("Based in", "Burnley, Lancashire, United Kingdom"), ("Serves", "Small businesses and creators across the UK; on-site shoots within about 20 miles of Burnley"),
             ("Founded", "2026"), ("Prices", "From £59 a month; full team £389 a month"), ("Billing", "Monthly; add, remove or upgrade Fellows from the next month"),
             ("Free trial", "Every Fellow has a free trial; no card needed"), ("Website", f"{BASE}/")]
    rows = "".join(f"<tr><th>{e(a)}</th><td>{e(b)}</td></tr>" for a, b in facts)
    plans = "".join(f'<li><a href="/services/{s}/">{e(n)}</a>: {e(sh)}, {p} a month. {e(TRIAL[s.split("-")[0]][0])}.</li>' for s, n, sh, p, *_ in F)
    ld = [{"@context": "https://schema.org", "@type": "AboutPage", "url": f"{BASE}/about/", "mainEntity": {"@type": "Organization", "@id": f"{BASE}/#org", "name": "ContentFellow",
           "alternateName": ["Content Fellow", "ContentFellow UK"], "url": f"{BASE}/", "logo": f"{BASE}/f.webp", "foundingDate": "2026",
           "description": "UK marketing service for small businesses: photo and video shoots, video editing, social media, websites, and SEO & GEO on monthly plans from £59.",
           "address": {"@type": "PostalAddress", "addressLocality": "Burnley", "addressRegion": "Lancashire", "addressCountry": "GB"}, "areaServed": "GB",
           "knowsAbout": ["SEO", "Generative engine optimisation (GEO)", "AI search visibility", "Local SEO", "Social media management", "Video production", "Video editing", "Website design"],
           "makesOffer": [{"@type": "Offer", "name": n, "price": re.sub(r"[^\d.]", "", p), "priceCurrency": "GBP", "url": f"{BASE}/services/{s}/"} for s, n, sh, p, *_ in F]}}]
    body = (f'<h1>About ContentFellow</h1><p class="lead"><strong>ContentFellow is a UK marketing service for small businesses, based in Burnley, Lancashire.</strong> Instead of agency retainers, you hire "Fellows": specialists on simple monthly plans from £59, for photo and video, editing, social media, websites, and SEO & GEO (getting recommended by Google and AI assistants like ChatGPT).</p>'
            f'<h2>Key facts</h2><table>{rows}</table><h2>The Fellows</h2><ul>{plans}</ul>'
            f'<h2>How we work</h2><ul><li>Published prices, monthly billing, no long contracts.</li><li>You approve every video, post and website change before it goes live; videos include two rounds of revisions.</li><li>We publish our pricing research openly in our <a href="/blog/">guides</a>, including comparisons with other providers.</li></ul>'
            f'<h2>Not to be confused with</h2><p>ContentFellow is not Contentful (a content management software company) and is not affiliated with it.</p>{cta_box()}')
    page("about", "About ContentFellow: UK Small Business Marketing, Burnley", "ContentFellow is a Burnley-based UK marketing service: monthly plans from £59 for video, editing, social, websites and SEO & GEO. Key facts, prices and how we work.", body, ld)

FAQ_HUB = [
 ("Pricing", [("How much does ContentFellow cost?", "Plans start at £59 a month. Social Fellow £59 or £129, Build Fellow £69, Search Fellow £89, Creator Fellow £119, Studio Fellow £149, or the Growth Fellow (all five) £389 a month."),
              ("Is there a contract?", "No long contract. Billing is monthly and you can add, remove or upgrade Fellows from the next month."),
              ("Is there a free trial?", "Yes, every Fellow: 7 free days for Search, Social and Growth, 3 free videos for Creator, a free mini shoot for Studio, and a free homepage preview for Build. No card needed."),
              ("Are prices plus VAT?", "Ask us when you start; we'll confirm the exact monthly amount in writing before any billing.")]),
 ("SEO & GEO", [("Can you get my business recommended by ChatGPT?", "Nobody can guarantee it, but the Search Fellow does what AI assistants rely on: Bing indexing, structured data, answer-first service pages, consistent directory listings, reviews and tracking which prompts name you."),
                ("What is GEO?", "GEO (generative engine optimisation) makes your business easy for AI assistants like ChatGPT, Claude, Gemini and Perplexity to find, understand and recommend."),
                ("What's the most affordable SEO for a UK small business?", "Affordable UK SEO typically costs £89 to £400 a month. The Search Fellow is £89 a month and covers SEO and GEO together."),
                ("How long does SEO take?", "Technical fixes show within weeks; rankings and AI mentions usually build over 6 to 12 weeks or longer in competitive areas.")]),
 ("Websites", [("How much is a website with ContentFellow?", "The Build Fellow is £69 a month with no upfront fee: a custom site up to five pages, hosting, security, updates and two change requests a month."),
               ("Can I see my website before paying?", "Yes. We design a free homepage preview within 3 working days.")]),
 ("Social media", [("How much is social media management?", "The Social Fellow is £59 a month (Manage) or £129 a month (Manage + Post), covering up to three platforms with trend research."),
                   ("Do I approve posts?", "Yes, every post is shared with you for approval before it goes live.")]),
 ("Video & photo", [("How much is a monthly photo and video shoot?", "The Studio Fellow is £149 a month: one on-site shoot up to 3 hours, photo and 4K video, 20 edited photos within 5 working days."),
                    ("How much is video editing for Reels and TikTok?", "The Creator Fellow is £119 a month: 8 short videos, 1 motion graphics video and 1 podcast edit up to 60 minutes."),
                    ("Where do you shoot?", "On-site at your business within about 20 miles of Burnley, Lancashire (Padiham, Nelson, Colne, Accrington, Clitheroe, Blackburn and nearby). Editing and other services are UK-wide.")]),
 ("Getting started", [("How do I start?", "Fill in the 2-minute form at contentfellow.com/get-started/ and choose a free trial or the free AI visibility check. We reply within 1 working day."),
                      ("Who is ContentFellow for?", "UK small businesses and creators who want professional marketing on a small, predictable monthly budget.")]),
]

def faq_hub():
    allq = [qa for _, qs in FAQ_HUB for qa in qs]
    ld = [{"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in allq]}]
    body = "<h1>ContentFellow FAQ: prices, trials and how it works</h1><p class=\"lead\">Straight answers about ContentFellow's monthly marketing plans for UK small businesses.</p>"
    body += "".join(f"<h2>{e(sec)}</h2>" + "".join(f"<h3>{e(q)}</h3><p>{e(a)}</p>" for q, a in qs) for sec, qs in FAQ_HUB) + cta_box()
    page("faq", "ContentFellow FAQ: Prices, Free Trials, SEO, Websites, Video", "Answers about ContentFellow: prices from £59 a month, free trials on every plan, SEO & GEO, websites, social media and video.", body, ld)

def llms_full():
    """Plain-text copy of the key pages for AI crawlers (llms-full.txt convention)."""
    def text(p):
        s = (SITE / p / "index.html").read_text()
        s = re.sub(r"(?s)<head>.*?</head>|<script.*?</script>|<style.*?</style>|<header>.*?</header>|<footer>.*?</footer>", "", s)
        s = re.sub(r"<(h1|h2|h3)[^>]*>", lambda m: "\n" + "#" * int(m.group(1)[1]) + " ", s)
        s = re.sub(r"<li\b[^>]*>", "\n- ", s); s = re.sub(r"</(p|tr|table|ul|ol|div|h1|h2|h3|li)>", "\n", s); s = re.sub(r"</t[hd]>", " | ", s)
        s = H.unescape(re.sub(r"<[^>]+>", "", s)); return re.sub(r"\n{3,}", "\n\n", s).strip()
    pages = ["about", "services"] + [f"services/{x[0]}" for x in F] + ["burnley", "faq"] + sorted(str(p.parent.relative_to(SITE)) for p in SITE.glob("blog/*/index.html"))
    out = "# ContentFellow — full text for AI assistants\n> UK marketing service for small businesses, Burnley, Lancashire. Monthly plans from £59; free trial on every plan. Source: https://contentfellow.com/\n\n"
    out += "\n\n---\n\n".join(f"URL: {BASE}/{p}/\n\n{text(p)}" for p in pages)
    (SITE / "llms-full.txt").write_text(out)

if __name__ == "__main__":
    service_pages(); get_started(); local_page(); about_page(); faq_hub(); blog_ctas(); llms_full(); print("ok")
