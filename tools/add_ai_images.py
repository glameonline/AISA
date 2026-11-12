"""Owner-approved (8 Nov 2026) AI-search illustration + call button on target pages. Marker <!--cf-aiimg-->."""
import pathlib, re
MAP = {
 "blog/restaurant-website-cost-uk": "restaurant-burnley", "blog/tradesperson-website-cost-uk": "plumber-burnley",
 "blog/marketing-agency-burnley": "cafe-burnley", "blog/social-media-management-burnley": "gym-burnley",
 "blog/web-designer-burnley": "plumber-burnley", "blog/cheapest-marketing-agency-burnley": "accountant-burnley",
 "blog/marketing-agency-nelson": "barber-nelson", "blog/social-media-management-nelson": "barber-nelson", "blog/web-designer-nelson": "barber-nelson",
 "blog/marketing-agency-colne": "salon-colne", "blog/social-media-management-colne": "salon-colne", "blog/web-designer-colne": "salon-colne",
 "blog/seo-geo-case-study-uk": "cafe-burnley", "blog/get-business-recommended-by-chatgpt-uk": "cafe-burnley",
 "blog/rank-on-google-maps-uk": "restaurant-burnley", "blog/marketing-for-cafes-restaurants-burnley": "cafe-burnley", "blog/marketing-for-barbers-salons-burnley": "barber-nelson",
 "blog/marketing-for-plumbers-trades-burnley": "plumber-burnley", "blog/marketing-for-gyms-burnley": "gym-burnley", "blog/marketing-for-accountants-burnley": "accountant-burnley",
 "blog/seo-agency-nelson": "barber-nelson", "blog/seo-agency-colne": "salon-colne",
 "blog/videographer-nelson": "barber-nelson", "blog/videographer-colne": "salon-colne",
 "blog/marketing-agency-accrington": "cafe-burnley", "blog/affordable-social-media-management-lancashire": "gym-burnley",
 "blog/web-designer-accrington": "plumber-burnley",
 "blog/marketing-agency-blackburn": "cafe-burnley",
 "burnley": "restaurant-burnley",
}
NOUN = lambda s: s.split("-")[0]
n = 0
for page, img in MAP.items():
    f = pathlib.Path("outputs/_site") / page / "index.html"
    if not f.exists(): continue
    s = f.read_text()
    s = re.sub(r"<!--cf-aiimg-->.*?<!--/cf-aiimg-->", "", s, flags=re.S)
    town = img.split("-")[1].title()
    blk = (f'<!--cf-aiimg--><figure style="margin:24px auto;max-width:420px;text-align:center">'
           f'<a href="tel:07535677302"><img src="/img/ai/ai-search-{img}.png" alt="Illustration: how an AI assistant lists the best {NOUN(img)}s in {town}" width="414" height="750" loading="lazy" style="width:100%;height:auto;border-radius:16px;border:1px solid #ddd"></a>'
           f'<figcaption style="font-size:14px;margin:8px 0">Illustration. Want your {NOUN(img)} business named when locals ask AI?</figcaption>'
           f'<a href="tel:07535677302" style="display:inline-block;background:#f5b942;color:#111;font-weight:700;padding:12px 22px;border-radius:10px;text-decoration:none">📞 Call 07535 677302</a></figure><!--/cf-aiimg-->')
    m = re.search(r"Quick answer.*?</p>", s, flags=re.S) or re.search(r"</h1>", s)
    if not m: continue
    s = s[:m.end()] + blk + s[m.end():]
    f.write_text(s); n += 1
print("ai images placed:", n)
