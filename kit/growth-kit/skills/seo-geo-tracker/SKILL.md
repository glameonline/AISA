---
name: seo-geo-tracker
description: Daily tracker agent. Measures traffic/engagement, Google UK rankings and AI visibility (which prompts on ChatGPT, Claude, Gemini, Perplexity mention ContentFellow vs which competitors), logs mistakes to fix, and updates the graphical dashboard the manager shows the owner.
---
# SEO/GEO Tracker
## Data sources (use what is connected; record "n/a" otherwise — never fabricate numbers)
- AI visibility: OpenSEO `save_ai_visibility_tracker` + `set_ai_visibility_schedule` (daily) → `get_ai_visibility_results` / `get_ai_visibility_trend` / `get_ai_visibility_sources` (which domains/competitors get cited per prompt).
- Rankings: OpenSEO `create_rank_tracker` (location United Kingdom, then DE/FR/NL/IE) → `get_rank_tracker`.
- Traffic/engagement: OpenSEO `get_google_analytics_*` and `get_search_console_performance` (queries = the prompts/searches that sent visitors).
## Daily routine
1. Pull the above; append one row per day to `outputs/_tracker/daily.csv` (date, sessions, engaged_sessions, gsc_clicks, gsc_impressions, avg_position, ai_prompts_tracked, ai_mentions, ai_share_of_voice).
2. Update `outputs/_tracker/prompts.csv` (prompt, platform, market, mentioned_us, top_competitor_cited).
3. Write `outputs/_tracker/report-YYYY-MM-DD.md`: wins (new rankings/mentions), losses, **mistakes to fix** (technical + content), top 5 prompts where competitors are cited and we are not → push to `outputs/_plan/topic-queue.md`.
4. Regenerate `dashboard/index.html` data and republish the dashboard artifact.
