# Go-live runbook: contentfellow.com (Namecheap cPanel, LiteSpeed)
Package: `outputs/_deploy/contentfellow-site-2026-10-16.zip` (= `outputs/_site/`).

## 1. Back up (2 min)
cPanel → File Manager → public_html → select `index.html`, `.htaccess`, `robots.txt`, `sitemap.xml`, `llms.txt` → Compress → `backup-2026-10-16.zip`.

## 2. Upload the blog
Upload the zip into public_html → Extract → overwrite `robots.txt`, `sitemap.xml`, `llms.txt`. It adds `/blog/`. It does NOT touch `index.html`.

## 3. .htaccess
Paste `outputs/_site-fixes/htaccess-add-at-top.txt` at the top of `public_html/.htaccess`.

## 4. Homepage
Apply `outputs/_site-fixes/homepage-changes.md` (absolute og:image, "Guides" link to /blog/).

## 4b. Live reviews under each service (needs Google Place ID + API key)
Follow `outputs/_site-fixes/reviews/README.md`: upload `reviews/`, add config outside public_html, add the CSS/JS lines and one `<div class="cf-reviews" data-service="…">` under each service. Real reviews only.

## 4c. Lead form
Confirm the inbox in `public_html/get-started/submit.php` (`$TO`). Submit one test form: email arrives, row appears in `/home/<user>/cf-leads.csv`, browser lands on /get-started/thanks/. In GA4 mark `generate_lead` as a key event.
Add a "Free check" button to the homepage hero and nav linking to `/get-started/`, and link each homepage Fellow card to its `/services/<fellow>/` page.

## 5. Verify (each must pass)
| URL | Expect |
|---|---|
| https://contentfellow.com/ | 200, unchanged homepage, Guides link |
| https://contentfellow.com/blog/ | 200, lists 2 posts |
| /blog/geo-vs-seo-uk-small-business/ | 200, 2 images load |
| /blog/llm-optimisation-cost-small-business-uk/ | 200, 3 images load |
| /blog/get-business-recommended-by-chatgpt-uk/ and the 5 service guides (social, website, video production, video editing, outsourced team) | 200, 2 images each |
| /services/ + 6 service pages, /get-started/ | 200; form submits to /get-started/thanks/ |
| /burnley/, /5ba1ed0245094aa65dacdb4a3ec88d27.txt (IndexNow key) | 200 |
| /about/, /faq/, /llms-full.txt | 200 |
| /sitemap.xml, /robots.txt, /llms.txt | 200, new versions (25 URLs in sitemap) |
| https://www.contentfellow.com/ | 301 → https://contentfellow.com/ |
| /hello-world/ , /hugo-portfolio-hero-image/ | 410 |
Also: Rich Results Test on all 8 posts (Article, FAQPage, Breadcrumb).

## 6. Tell the search engines
- Search Console: Sitemaps → submit `sitemap.xml`; URL Inspection → Request indexing for /blog/ and all 8 posts.
- IndexNow (Bing/ChatGPT search): OpenSEO `submit_indexnow_urls` with the 9 blog URLs (/blog/ + 8 posts).
- Tracker: tick `outputs/_plan/publish-queue.md`, log in `outputs/_tracker/`.

## Rollback
Extract `backup-2026-10-16.zip` over public_html and delete `/blog/`.
