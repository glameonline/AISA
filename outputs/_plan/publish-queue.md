# Publish queue: goes live automatically as soon as hosting access exists
Deploy = copy everything in outputs/_site/ into public_html/ (keep the existing homepage index.html).
- [ ] /blog/ (index), /blog/llm-optimisation-cost-small-business-uk/ (16 Oct)
- [ ] /blog/geo-vs-seo-uk-small-business/ (16 Oct)
- [ ] /blog/get-business-recommended-by-chatgpt-uk/ (16 Oct)
- [ ] /blog/social-media-management-cost-uk/ (16 Oct)
- [ ] /blog/small-business-website-cost-uk/ (16 Oct)
- [ ] /blog/video-production-cost-uk/ (16 Oct)
- [ ] /blog/video-editing-cost-uk/ (16 Oct)
- [ ] /blog/outsourced-marketing-team-cost-uk/ (16 Oct)
- [ ] sitemap.xml + llms.txt (updated with both posts)
- [ ] Remove manual test upload if present: /blog/llm-optimisation-cost-small-business-uk.html → 301 to folder URL

## Prepared 16 Oct evening (waiting for desktop/cPanel access)
- Hosting: Namecheap cPanel (dns1/dns2.namecheaphosting.com). Runbook: outputs/_deploy/GO-LIVE.md
- Zip rebuilt after fixes: GEO vs SEO og:image/Article image now its own featured PNG (was studio.jpg); posts cross-link each other.
- [ ] .htaccess: www→non-www 301, /hello-world/ + /hugo-portfolio-hero-image/ 410, test .html → 301 (outputs/_site-fixes/htaccess-add-at-top.txt)
- [ ] Homepage: absolute og:image + Guides link to /blog/ (outputs/_site-fixes/homepage-changes.md)
- [ ] GSC sitemap + request indexing, IndexNow
