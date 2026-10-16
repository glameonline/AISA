---
name: wordpress-publisher
description: Publishes a finished post. WordPress mode creates a draft via REST API (title, content, featured image, Yoast/RankMath meta, tags, categories). Static mode (contentfellow.com today) builds a deployable /blog package — HTML page, images, sitemap, llms.txt, robots — and deploys it if hosting access is configured.
---
# Publisher
## Mode A — WordPress (needs env `WP_URL`, `WP_USER`, `WP_APP_PASSWORD`)
1. Upload images: `POST $WP_URL/wp-json/wp/v2/media` (Basic auth with application password) → media ids; set `alt_text`.
2. `POST /wp-json/wp/v2/posts` with `status: "draft"`, title, content (article HTML body), excerpt, slug, `featured_media`, categories, tags.
3. SEO meta: Yoast `yoast_head_json` is read-only — set via `meta: {_yoast_wpseo_title, _yoast_wpseo_metadesc}` (requires the field registered for REST) or RankMath equivalent.
4. Log the draft URL to `publish/publish-log.md`. Never set `publish` without owner approval unless `AUTO_PUBLISH=true`.
## Mode B — Static site (contentfellow.com is a custom static one-pager, not WordPress)
1. Copy `content/article.html` → `publish/blog/<slug>/index.html`, images → `publish/blog/<slug>/`.
2. Update `publish/blog/index.html`, `publish/sitemap.xml`, `publish/llms.txt`, `publish/robots.txt` (allow GPTBot, ClaudeBot, PerplexityBot, Google-Extended).
3. Deploy: if the site's git repo is attached → commit to `/blog` and push; if Netlify/Vercel token present → deploy; otherwise hand the package to the owner.
4. After going live: submit URL via OpenSEO `submit_indexnow_urls` (Bing/Yandex → feeds ChatGPT/Copilot search) and request indexing in Search Console.
