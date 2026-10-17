# Publish queue: goes live automatically as soon as hosting access exists
Deploy = copy everything in outputs/_site/ into public_html/ (keep the existing homepage index.html).
- [x] /blog/ (index), /blog/llm-optimisation-cost-small-business-uk/ (16 Oct)
- [x] /blog/geo-vs-seo-uk-small-business/ (16 Oct)
- [x] /blog/get-business-recommended-by-chatgpt-uk/ (16 Oct)
- [x] /blog/social-media-management-cost-uk/ (16 Oct)
- [x] /blog/small-business-website-cost-uk/ (16 Oct)
- [x] /blog/video-production-cost-uk/ (16 Oct)
- [x] /blog/video-editing-cost-uk/ (16 Oct)
- [x] /blog/outsourced-marketing-team-cost-uk/ (16 Oct)
- [ ] sitemap.xml + llms.txt (updated with both posts)
- [ ] Remove manual test upload if present: /blog/llm-optimisation-cost-small-business-uk.html → 301 to folder URL

## Prepared 16 Oct evening (waiting for desktop/cPanel access)
- Hosting: Namecheap cPanel (dns1/dns2.namecheaphosting.com). Runbook: outputs/_deploy/GO-LIVE.md
- Zip rebuilt after fixes: GEO vs SEO og:image/Article image now its own featured PNG (was studio.jpg); posts cross-link each other.
- [ ] .htaccess: www→non-www 301, /hello-world/ + /hugo-portfolio-hero-image/ 410, test .html → 301 (outputs/_site-fixes/htaccess-add-at-top.txt)
- [ ] Homepage: absolute og:image + Guides link to /blog/ (outputs/_site-fixes/homepage-changes.md)
- [ ] GSC sitemap + request indexing, IndexNow

## LIVE 17 Oct 2026 01:25 (owner ran tools/deploy_cpanel.ps1)
- [x] 25 sitemap URLs 200, 25 images 200, homepage trials/nav/og:image, www→non-www 301, /hello-world/ + /hugo-portfolio-hero-image/ 410, test .html 301, IndexNow key 200, form → thanks (test lead sent)
- [x] IndexNow: 27 URLs sent direct to Bing, HTTP 202 (17 Oct)
- [x] GSC request indexing /services/ + /blog/ (owner, 17 Oct); sitemap via robots.txt
- [ ] /services/development/ (new, 17 Oct) + updated services/index.html, sitemap.xml, llms.txt
- [ ] /services/management/ (new, 17 Oct) + updated services/index.html, sitemap.xml, llms.txt
- [ ] Backlinks: work outputs/_plan/backlinks.md (skill: backlink-builder)
- [ ] 17 Oct: 4 new posts: /blog/app-development-cost-uk/, /blog/website-subscription-vs-one-off-build/, /blog/llms-txt-explained/, /blog/check-if-chatgpt-mentions-your-brand/
- [ ] 17 Oct (extra batch): /blog/website-maintenance-cost-uk/, /blog/online-shop-website-cost-uk/, /blog/app-maintenance-cost-uk/, /blog/web-app-vs-mobile-app/
- [ ] 17 Oct: SEO audit fixes (shorter titles on 9 pages, 3 descriptions) in services, about, burnley, get-started, 2 posts
