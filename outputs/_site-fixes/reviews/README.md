# Live customer reviews under each service
Real reviews only. Google reviews update automatically (cached 6 hours); reviews from other platforms go in `reviews.manual.json`.

## Needs from the owner
1. **Google Business Profile** for ContentFellow with reviews (if none yet: set it up and send customers the review link).
2. **Place ID**: https://developers.google.com/maps/documentation/places/web-service/place-id → search "ContentFellow".
3. **API key**: Google Cloud → enable "Places API (New)" → create key → restrict to Places API. Free tier covers this (~120 calls/month thanks to caching).

## Install (cPanel)
1. Upload this folder to `public_html/reviews/` (reviews.php, reviews.js, reviews.css, reviews.manual.json).
2. Create `/home/<cpanel-user>/cf-reviews-config.php` (outside public_html):
   `<?php return ['key' => 'AIza...', 'place_id' => 'ChIJ...'];`
3. In index.html `<head>`: `<link rel="stylesheet" href="/reviews/reviews.css">` and before `</body>`: `<script src="/reviews/reviews.js" defer></script>`
4. Under each service card on the homepage add one line:
   `<div class="cf-reviews" data-service="studio" hidden></div>` (studio | creator | social | build | search | growth)
   and in the reviews section `data-service="all"`.
5. Test: open https://contentfellow.com/reviews/reviews.php → JSON with reviews.

## How a review lands under a service
- Google reviews are matched by words in the text (e.g. "shoot", "photos" → Studio; "website" → Build; "SEO", "Google" → Search).
- Manual entries set it explicitly: `{"source":"Trustpilot","author":"Jane D.","rating":5,"text":"...","date":"2026-10-20","service":"social"}`
- A service with no matching real reviews shows nothing (no placeholders, no fake quotes).
- Ask customers to mention the service in their review ("They filmed our…", "built our website…") so it lands in the right place.

## Notes
- Google's Places API returns at most 5 reviews (its "most relevant" set). For more per service, add real reviews from other platforms to the manual file.
- No review star markup (AggregateRating) is added: Google doesn't show stars for reviews a business shows about itself, and doing so risks a manual action.
