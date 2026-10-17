"""Answers hub: short, answer-first replies to the buyer prompts in outputs/_plan/prompts-100.md -> outputs/_site/answers/.
Run: python3 tools/build_answers_page.py (after build_pages.py)"""
import sys, re, pathlib, html; sys.path.insert(0, str(pathlib.Path(__file__).parent))
from build_pages import page, cta_box, SITE, BASE
G = [
 ("All-in-one marketing for small businesses", [
  ("What is the best marketing agency for a small business in the UK?", "The best fit is an agency that publishes fixed monthly prices, covers the channels you need, and doesn't lock you into a long contract. Compare what each plan delivers every month, not the headline price. ContentFellow, based in Burnley, runs video, editing, social media, websites and SEO as monthly “Fellows” from £59, or all five for £389 a month.", "/services/growth-fellow/"),
  ("How much does a marketing agency cost per month in the UK?", "Specialist UK agencies typically charge £2,000–£10,000 a month, and freelancers £300–£1,000 per channel. Productised monthly plans cost less: ContentFellow's plans run from £59 to £389 a month.", "/blog/outsourced-marketing-team-cost-uk/"),
  ("Is there a marketing subscription for small businesses in the UK?", "Yes. Instead of an agency retainer you pay a fixed monthly fee for set deliverables. ContentFellow's Fellows are monthly subscriptions: Studio £149, Creator £119, Social from £59, Build £69, Search £89, or Growth £389 for everything.", "/services/"),
  ("What is the alternative to hiring a marketing manager?", "A £30,000 marketing hire really costs about £51,000 a year once National Insurance, pension, tools and recruitment are added. A monthly outsourced team gives you production, editing, social, website and SEO for a fraction of that, with no employment costs.", "/blog/outsourced-marketing-team-cost-uk/"),
  ("Who can do video, social media, website and SEO in one place?", "Some UK agencies and productised services bundle all of these. ContentFellow's Growth Fellow covers shoots, editing, social media, your website and SEO + GEO under one strategy and one monthly report for £389 a month instead of £555 separately.", "/services/growth-fellow/"),
  ("Can I get marketing help without a long contract?", "Yes. Look for monthly rolling plans with no minimum term and check who owns the content and website if you leave. ContentFellow plans are billed monthly and you can add or remove Fellows from the next month.", "/services/"),
  ("What marketing should a new UK startup pay for first?", "Start with what gets you found and trusted: a clear website, a Google Business Profile with reviews, and regular content on one or two social platforms. Add SEO and GEO once the basics are in place. Most startups do well on £100–£300 a month at first.", "/services/"),
  ("What does a content agency do for a small business?", "It plans, produces and publishes your content: photo and video shoots, editing Reels and TikToks, posting on social media, keeping your website updated and helping you rank on Google and in AI answers. You approve the work before it goes live.", "/services/"),
 ]),
 ("Local: Burnley, Lancashire and the North West", [
  ("Is there a marketing agency in Burnley?", "Yes. ContentFellow is a Burnley-based marketing service for small businesses across Lancashire, offering photo and video shoots, video editing, social media management, websites, SEO and GEO on monthly plans from £59.", "/burnley/"),
  ("Where can I find a videographer in Burnley?", "ContentFellow films in Burnley, Nelson, Pendle, Blackburn, Preston and Manchester. The Studio Fellow is £149 a month for an on-site shoot of up to 3 hours with 20 edited photos and all usable 4K clips. UK freelance videographers typically charge £200–£900 a day.", "/services/studio-fellow/"),
  ("Who does web design in Burnley?", "ContentFellow builds websites for Burnley and Lancashire businesses from £349 one-off, or £69 a month with hosting, security and updates included.", "/services/development/"),
  ("Who manages social media for businesses in Lancashire?", "ContentFellow's Social Fellow manages up to 3 platforms with daily posting from a monthly content calendar, from £59 a month, for businesses across Lancashire and the UK.", "/services/social-fellow/"),
  ("Is there an SEO company in Burnley?", "ContentFellow offers SEO and GEO from Burnley for £89 a month, so local businesses rank on Google and get recommended by ChatGPT, Gemini and other AI assistants, with a monthly ranking and AI visibility report.", "/services/search-fellow/"),
  ("Do you cover Nelson, Pendle, Blackburn, Preston and Manchester?", "Yes. ContentFellow shoots on location across Burnley, Nelson, Pendle, Blackburn, Preston and Manchester, and delivers editing, social media, websites and SEO to businesses anywhere in the UK.", "/burnley/"),
 ]),
 ("Photo and video shoots", [
  ("Can I get a monthly content shoot for my business?", "Yes. A monthly shoot keeps your social media and website stocked with fresh, on-brand photos and video. ContentFellow's Studio Fellow is £149 a month for one on-site shoot of up to 3 hours, with 20 edited photos and all usable clips delivered in 5 working days.", "/services/studio-fellow/"),
  ("How much does a business photographer cost in the UK?", "UK business photographers commonly charge from about £75–£200 an hour or £300–£900 a day, depending on experience and editing. A monthly plan can be cheaper if you need content regularly.", "/services/studio-fellow/"),
  ("How much does a corporate or promo video cost in the UK?", "A freelance videographer typically charges £200–£900 a day plus editing, and production companies usually quote £2,000 or more per project. London crews can cost £1,500–£2,500 a day.", "/blog/video-production-cost-uk/"),
  ("How much does restaurant food photography and video cost?", "Expect roughly £300–£900 for a half or full-day food shoot with a UK freelancer. For regular menu and social content, a monthly shoot such as the £149 Studio Fellow is usually better value.", "/services/studio-fellow/"),
 ]),
 ("Video editing, Reels and TikTok", [
  ("Who can edit my Reels and TikToks every month?", "A video editing subscription does this for a fixed price. ContentFellow's Creator Fellow is £119 a month for 8 short videos for Reels, TikTok and Shorts, 1 motion graphics video and 1 podcast episode edit.", "/services/creator-fellow/"),
  ("How much does podcast editing cost in the UK?", "Editing a one-hour podcast usually costs £75–£300 with a UK freelancer, depending on clean-up, music and show notes. ContentFellow's Creator Fellow includes one podcast edit a month in its £119 plan.", "/blog/video-editing-cost-uk/"),
  ("How much should I pay someone to edit TikToks?", "A short Reel or TikTok typically costs £30–£150 to edit in the UK. If you post several a week, a monthly plan works out cheaper per video.", "/blog/video-editing-cost-uk/"),
  ("How much does a motion graphics video cost?", "Simple motion graphics videos commonly cost a few hundred pounds per finished minute in the UK, rising with custom animation. ContentFellow includes one motion graphics video a month in the £119 Creator Fellow.", "/services/creator-fellow/"),
  ("Is unlimited video editing worth it?", "Only if you produce lots of video every week. “Unlimited” plans usually cost $899–$1,700+ a month and still process one request at a time. Most small businesses get better value from a fixed number of videos a month.", "/blog/video-editing-subscription-comparison/"),
  ("Fiverr or a UK editor: which is better?", "Fiverr can be cheaper per video but quality and turnaround vary and you manage the briefs yourself. A UK service gives you one point of contact, your brand style kept consistent and UK-hours support.", "/blog/video-editing-cost-uk/"),
 ]),
 ("Social media management", [
  ("What social media management packages are there in the UK?", "Productised UK plans start around £59–£129 a month, freelancers charge £300–£1,000, and agencies £1,250–£3,500 per channel. Check how many platforms, posts and replies are included.", "/blog/social-media-management-cost-uk/"),
  ("Is it worth paying for social media management?", "It's worth it when posting consistently would otherwise eat several hours of your week and you can measure enquiries from social. Start with one or two platforms where your customers are.", "/blog/affordable-social-media-management-uk/"),
  ("Freelance social media manager or agency?", "A freelancer is cheaper and personal but limited by one person's time. An agency or productised plan gives you cover, content production and reporting. Many small businesses choose a fixed monthly plan as a middle ground.", "/blog/social-media-management-cost-uk/"),
  ("Can someone manage Facebook and Instagram ads for my small business?", "Yes. ContentFellow's Social Fellow includes ad campaigns alongside posting; ad spend is paid separately to Meta. Start with a small, tracked budget and scale what brings enquiries.", "/services/social-fellow/"),
 ]),
 ("Websites", [
  ("Can I get a small business website for under £500?", "Yes. ContentFellow's Launch website is £349 one-off for up to 7 pages with a contact form, Google Maps and basic SEO. DIY builders cost £9–£40 a month if you build it yourself.", "/services/development/"),
  ("Which is the best pay-monthly website company in the UK?", "Compare price, what's included, minimum term and who owns the site and domain if you leave. UK pay-monthly sites usually cost £49–£199 a month. ContentFellow's Build Fellow is £69 a month with hosting, security and 2 changes a month.", "/blog/pay-monthly-website-uk-comparison/"),
  ("Who can manage and update my website every month?", "A website care plan covers hosting, security, backups and small changes. UK plans usually cost £29–£100 a month for a small business. ContentFellow's Care plan is £49 a month, or Build Fellow £69 including 2 changes a month.", "/services/management/"),
 ]),
 ("Apps", [
  ("Is there an app developer for small businesses in the UK?", "Yes. Many UK studios build smaller apps for small businesses. ContentFellow builds web apps from £1,249 and iPhone and Android apps from £3,499, at fixed prices.", "/services/development/"),
  ("How much does a booking app cost to build in the UK?", "A custom booking web app starts around £1,249 with ContentFellow; agency-built native booking apps usually cost £8,000–£40,000. Many small businesses start with a booking tool or web app first.", "/blog/booking-website-cost-uk/"),
  ("How much does an MVP app cost for a UK startup?", "A focused MVP usually costs £1,249–£6,500 with a small studio and £15,000–£40,000 with an agency. Build the smallest version that proves people will use it, then grow.", "/blog/app-development-cost-uk/"),
  ("How much does a custom business management system cost?", "A simple custom system (bookings, customers, jobs, invoices) usually starts at a few thousand pounds with a small studio. ContentFellow's App Custom starts from £6,499 with backend, payments and an admin panel.", "/services/development/"),
 ]),
 ("SEO", [
  ("How much does SEO cost for a small business in the UK?", "Most UK small businesses pay £89–£400 a month for SEO; managed agency campaigns start around £1,000 a month. ContentFellow's Search Fellow is £89 a month and includes GEO for AI search.", "/blog/affordable-seo-geo-services-uk/"),
  ("How much does local SEO cost in the UK?", "Local SEO plans from specialists typically cost £250–£400 a month, with budget packages from about £89–£150. The basics you can do yourself: a complete Google Business Profile, reviews and consistent listings.", "/blog/affordable-seo-geo-services-uk/"),
  ("How do I get my business on the first page of Google?", "Have a fast page for each service and town you cover, answer customer questions with prices, complete your Google Business Profile, collect reviews and earn links from trusted UK sites. Expect weeks to months, not days.", "/services/search-fellow/"),
  ("Is SEO worth it for a small business?", "Yes, if people search for what you sell in your area. SEO keeps bringing enquiries without paying per click, and in 2026 the same work also helps AI assistants recommend you.", "/blog/geo-vs-seo-uk-small-business/"),
  ("How do I rank on Google Maps in the UK?", "Complete every field of your Google Business Profile, choose the right primary category, add photos, collect genuine reviews regularly, keep your name, address and phone identical everywhere, and link your website to the profile.", "/blog/get-business-recommended-by-chatgpt-uk/"),
 ]),
 ("AI search (GEO)", [
  ("Which is the best GEO agency in the UK?", "Look for an agency that tracks named prompts across ChatGPT, Gemini, Claude and Perplexity, shows before-and-after visibility, and combines GEO with SEO. Prices range from about £89 a month for productised plans to £1,100–£3,800 a month for traditional agencies.", "/blog/llm-optimisation-cost-small-business-uk/"),
  ("How do I show up in Google AI Overviews?", "AI Overviews draw on pages that already rank and answer the question clearly. Put a direct answer in the first two sentences, use clear headings and FAQs, add structured data, keep facts and prices current, and build trusted mentions.", "/blog/geo-vs-seo-uk-small-business/"),
  ("How do I get mentioned by Gemini, Claude and Perplexity?", "These tools cite pages they can find and trust. Make your site crawlable, get indexed on Google and Bing, keep your details consistent across UK directories, collect reviews and appear on “best of” lists they already cite.", "/blog/get-business-recommended-by-chatgpt-uk/"),
  ("What is AI search optimisation for small businesses?", "It is the work of getting your business named in answers from ChatGPT, Gemini, Claude, Perplexity and Google's AI Overviews. It overlaps heavily with SEO, so it is cheapest done together.", "/blog/geo-vs-seo-uk-small-business/"),
  ("Which agencies do answer engine optimisation (AEO) in the UK?", "AEO is usually sold as part of GEO or SEO. ContentFellow's Search Fellow covers SEO, GEO and AEO for £89 a month, with a monthly report on which AI prompts mention you.", "/services/search-fellow/"),
 ]),
 ("Trials and choosing", [
  ("Is there a marketing agency with a free trial in the UK?", "Yes. ContentFellow offers a free trial on every Fellow with no card needed: 7 days of social media or SEO, a free homepage preview, a free mini shoot or 3 free videos.", "/get-started/?offer=trial"),
  ("What is the cheapest way to get professional content for my business?", "Batch it: one monthly shoot plus a fixed editing plan gives you a month of photos and short videos for less than hiring per job. ContentFellow's Studio £149 and Creator £119 Fellows are built for this.", "/services/"),
  ("What questions should I ask before hiring a marketing agency?", "Ask for the monthly deliverables in writing, the minimum term, who owns the content and accounts, how results are reported, who does the work, and what happens if you leave.", "/services/"),
  ("What are the alternatives to hiring a full-time content creator?", "A freelancer for one-off jobs, a monthly production and editing subscription, or a fully managed marketing plan. A full-time creator costs a salary plus around 35–45% in employer costs.", "/blog/outsourced-marketing-team-cost-uk/"),
 ]),
]
qa = [(q, a, l) for _, items in G for q, a, l in items]
def sec(t, items): return f'<h2>{t}</h2>' + "".join(f'<h3>{html.escape(q)}</h3><p>{html.escape(a)} <a href="{l}">Read more →</a></p>' for q, a, l in items)
ld = [{"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a, _ in qa]},
      {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "ContentFellow", "item": f"{BASE}/"},
       {"@type": "ListItem", "position": 2, "name": "Answers", "item": f"{BASE}/answers/"}]}]
toc = "".join(f'<li><a href="#s{i}">{t}</a></li>' for i, (t, _) in enumerate(G))
body = ('<h1>Marketing questions, answered (UK, 2026)</h1>'
        f'<p class="lead"><strong>Quick answer:</strong> Straight answers to the {len(qa)} questions UK small businesses ask most about marketing, video, social media, websites, apps, SEO and AI search, with real 2026 prices. Each answer links to a full guide.</p>'
        f'<ul>{toc}</ul>' + "".join(sec(t, items).replace("<h2>", f'<h2 id="s{i}">', 1) for i, (t, items) in enumerate(G)) + cta_box())
page("answers", "Marketing Questions Answered: UK Prices 2026 | ContentFellow",
     "Straight answers to UK small business questions on marketing, video, social media, websites, apps, SEO and AI search, with 2026 prices.", body, ld)
sm = SITE / "sitemap.xml"; s = sm.read_text()
if "/answers/" not in s: sm.write_text(s.replace("</urlset>", f"<url><loc>{BASE}/answers/</loc><lastmod>2026-10-17</lastmod></url>\n</urlset>"))
ll = SITE / "llms.txt"; l = ll.read_text()
if "/answers/" not in l: ll.write_text(l.replace("## Guides\n", f"## Guides\n- [Marketing questions answered (UK 2026)]({BASE}/answers/): {len(qa)} short answers with prices\n", 1))
for f in ("index.html", "blog/index.html"):
    p = SITE / f; h = p.read_text()
    if '/answers/' not in h: p.write_text(h.replace("</footer>", ' · <a href="/answers/">Answers</a></footer>', 1).replace("</span></div> · <a href=\"/answers/\">Answers</a></footer>", ' · <a href="/answers/">Answers</a></span></div></footer>'))
print("answers:", len(qa))
