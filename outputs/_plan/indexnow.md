# IndexNow
Key file: https://contentfellow.com/5ba1ed0245094aa65dacdb4a3ec88d27.txt (in outputs/_site, deploys with the zip).
After go-live, ping Bing/Yandex (feeds ChatGPT search) with every URL in sitemap.xml:
curl -s -X POST https://api.indexnow.org/indexnow -H 'Content-Type: application/json' -d '{"host":"contentfellow.com","key":"5ba1ed0245094aa65dacdb4a3ec88d27","keyLocation":"https://contentfellow.com/5ba1ed0245094aa65dacdb4a3ec88d27.txt","urlList":[...sitemap URLs...]}'
Or OpenSEO submit_indexnow_urls. Re-ping whenever a page is added or changed.
OpenSEO IndexNow key: https://contentfellow.com/2d842ffcbfa64f9d854bb35f99d36dff.txt (use OpenSEO submit_indexnow_urls, project bb835b3c-4112-463f-838f-251dcdc12f30).
