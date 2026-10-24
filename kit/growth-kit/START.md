# Website Growth Kit (copy of the ContentFellow system)

Paste this into a new project's first message:

> Repo glameonline/aisa (branch claude/seo-geo-content-agents) se `kit/growth-kit/` copy karo is project mein. skills/ ko .claude/skills/ mein daalo, tools/ ko tools/ mein. Phir yeh setup karo meri website **Throne Solutions** (<website URL>) ke liyaa.

## What the new session must do (in order)
1. Copy skills to `.claude/skills/`, tools to `tools/`, workflow yml to `.github/workflows/`.
2. Run the `website-brand-scraper` skill on the new site → `outputs/_brand/brand.md` (services, prices, voice). Replace every "ContentFellow"/contentfellow.com/Burnley reference in tools and skills with the new brand, domain and city.
3. Make `outputs/_plan/prompts-100.md` (100 buyer prompts), `topic-queue.md`, `backlinks.md`.
4. Daily loop (content-agent-orchestrator): 2 articles → seo_audit → 5 backlinks → build_zip + deploy → indexing check → tracker + dashboard.
5. Outreach (optional, only with owner approval): build prospects CSV → build_fit.py → email_queue.py, max 20/day, opt-out line, generic business emails only.
6. Create scheduled tasks: morning run (LIGHT), weekday email send, evening indexing check.

## Owner rules (always)
- Usage cap: keep each day under ~40-50% of the daily limit; do less, put the rest in "pending kal" and report in Roman Urdu.
- Never ask for passwords/keys/JSON in chat; secrets go only in GitHub/environment secrets.
- No fake reviews/stats, no spam backlinks, no publishing the owner's home address/phone.
- Outreach only with owner approval; honour STOP / "no thanks".

## Owner must connect in the new project
GitHub repo for the new site, Gmail, OpenSEO project for the new domain, hosting (cPanel) secrets in GitHub.
