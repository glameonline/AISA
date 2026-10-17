#!/usr/bin/env bash
# Deploy outputs/_site to contentfellow.com via the cPanel API. Run on YOUR computer (Mac/Linux terminal):
#   bash <(curl -fsSL https://raw.githubusercontent.com/glameonline/AISA/claude/seo-geo-content-agents/tools/deploy_cpanel.sh)
# It asks for a cPanel API token (cPanel > Security > Manage API Tokens). The token is never stored.
set -euo pipefail
CP_USER="contwfah"
HOST="https://server247.web-hosting.com:2083"
DOC="/home/$CP_USER/public_html"
BR="claude/seo-geo-content-agents"
RAW="https://raw.githubusercontent.com/glameonline/AISA/$BR"
ZIP="contentfellow-site-2026-10-16.zip"

read -rsp "cPanel API token: " TOKEN; echo
AUTH="Authorization: cpanel $CP_USER:$TOKEN"
BK="$HOME/contentfellow-backup-$(date +%Y%m%d-%H%M)"; mkdir -p "$BK"; cd "$BK"
api() { curl -fsS -H "$AUTH" "$@"; }
ok() { grep -q '"status":1\|"result":1\|"result" : 1' "$1"; }

echo "1/6 Checking login..."
api -G "$HOST/execute/Fileman/list_files" --data-urlencode "dir=$DOC" -o list.json
ok list.json || { echo "Login failed. Check the token."; cat list.json; exit 1; }

echo "2/6 Backing up index.html and .htaccess to $BK ..."
for f in index.html .htaccess; do
  api -G "$HOST/execute/Fileman/get_file_content" --data-urlencode "dir=$DOC" --data-urlencode "file=$f" -o "backup-$f.json"
  ok "backup-$f.json" || { echo "Backup of $f failed, stopping (nothing changed)."; cat "backup-$f.json"; exit 1; }
done

echo "3/6 Downloading the site package from GitHub..."
curl -fsSL "https://github.com/glameonline/AISA/raw/$BR/outputs/_deploy/$ZIP" -o "$ZIP"
curl -fsSL "$RAW/outputs/_site-fixes/htaccess-add-at-top.txt" -o htaccess-add.txt

echo "4/6 Uploading and extracting into public_html..."
api -F "dir=$DOC" -F "overwrite=1" -F "file-1=@$ZIP" "$HOST/execute/Fileman/upload_files" -o up.json
ok up.json || { echo "Upload failed."; cat up.json; exit 1; }
api -G "$HOST/json-api/cpanel" --data-urlencode "cpanel_jsonapi_user=$CP_USER" --data-urlencode "cpanel_jsonapi_apiversion=2" \
  --data-urlencode "cpanel_jsonapi_module=Fileman" --data-urlencode "cpanel_jsonapi_func=fileop" --data-urlencode "op=extract" \
  --data-urlencode "sourcefiles=$DOC/$ZIP" --data-urlencode "destfiles=$DOC" -o ex.json
ok ex.json || { echo "Extract failed. In cPanel File Manager: right-click $ZIP > Extract."; cat ex.json; }
api -G "$HOST/json-api/cpanel" --data-urlencode "cpanel_jsonapi_user=$CP_USER" --data-urlencode "cpanel_jsonapi_apiversion=2" \
  --data-urlencode "cpanel_jsonapi_module=Fileman" --data-urlencode "cpanel_jsonapi_func=fileop" --data-urlencode "op=unlink" \
  --data-urlencode "sourcefiles=$DOC/$ZIP" -o rm.json || true

echo "5/6 Adding SEO rules to the top of .htaccess..."
if command -v python3 >/dev/null 2>&1; then
  python3 - <<'PY'
import json
old=json.load(open("backup-.htaccess.json"))["data"]["content"] or ""
add=open("htaccess-add.txt").read()
open("htaccess-new.txt","w").write(old if "ContentFellow SEO fixes" in old else add+"\n"+old)
PY
  api -F "dir=$DOC" -F "file=.htaccess" -F "content=<htaccess-new.txt" "$HOST/execute/Fileman/save_file_content" -o ht.json
  ok ht.json && echo "   .htaccess updated." || { echo "   .htaccess not updated; paste htaccess-add.txt at the top manually."; cat ht.json; }
else
  echo "   python3 not found: paste $BK/htaccess-add.txt at the top of .htaccess in File Manager."
fi

echo "6/6 Checking pages..."
for p in "" blog/ services/ services/search-fellow/ get-started/ burnley/ about/ faq/ privacy/ sitemap.xml llms.txt llms-full.txt; do
  printf "  %-28s %s\n" "/$p" "$(curl -s -o /dev/null -w '%{http_code}' "https://contentfellow.com/$p")"
done
printf "  %-28s %s\n" "www -> non-www" "$(curl -s -o /dev/null -w '%{http_code} %{redirect_url}' https://www.contentfellow.com/)"
echo "Done. Backup kept in $BK. Tell Claude: 'script chal gayi' and paste this output."
