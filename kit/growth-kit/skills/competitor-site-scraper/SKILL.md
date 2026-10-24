---
name: competitor-site-scraper
description: Finds and reads the pages currently ranking (Google UK) and being cited by AI for a topic — their headings, prices, FAQs, schema — and lists what they miss. Output research/competitors.md.
---
# Competitor Site Scraper
1. `firecrawl_search` the topic + a commercial variant, `location: "United Kingdom"`, limit 8, `sources: ["web"]`. Excerpts usually suffice; scrape at most the 2 strongest pages.
2. Optionally `OpenSEO find_serp_competitors` / `Semrush organic_research` when credits allow.
3. Write a table: URL · angle · price ranges quoted · currency/market · FAQs · schema/freshness.
4. **Gaps** section: what no competitor covers (e.g. UK £ pricing, small-business budgets, named UK plans, AI-citation-ready answer blocks). The gaps become the article's angle.
5. Also record which competitor brands an AI answer recommends (feeds the tracker).
