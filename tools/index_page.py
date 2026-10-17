"""Build the phone page the owner taps each day to request Google indexing.
Reads outputs/_tracker/indexing.csv (latest row per URL wins), writes outputs/index-today/index.html.
Usage: python3 tools/index_page.py"""
import csv, html, pathlib, re, datetime
SITE = pathlib.Path("outputs/_site"); OUT = pathlib.Path("outputs/index-today/index.html")
DAILY = 10  # Google allows roughly 10 manual "Request indexing" clicks a day
rows, asked = {}, {}
for r in csv.DictReader(open("outputs/_tracker/indexing.csv")):
    if r["google_status"].startswith("Indexing requested"): asked[r["url"]] = r["date"]  # owner tapped it
    else: rows[r["url"]] = {**rows.get(r["url"], {}), **r} if r.get("inspect_link") else {**r, "inspect_link": rows.get(r["url"], {}).get("inspect_link", "")}
WAIT = (datetime.date.today() - datetime.timedelta(days=7)).isoformat()  # give Google a week before asking again
def title(url):
    f = SITE / url.split("contentfellow.com/", 1)[1] / "index.html"
    m = re.search(r"<title>(.*?)</title>", f.read_text(), re.S) if f.exists() else None
    return html.unescape(m.group(1).split(" | ")[0].strip()) if m else url
done = [r for r in rows.values() if r["google_status"].startswith("Submitted and indexed") or r["google_status"].startswith("Indexed")]
waiting = [r for r in rows.values() if r not in done and asked.get(r["url"], "") >= WAIT]
todo = [r for r in rows.values() if r not in done and r not in waiting and r.get("inspect_link")]
todo = sorted(todo, key=lambda r: ("/services/" not in r["url"]))  # money pages first, then log order
today, rest = todo[:DAILY], todo[DAILY:]
cards = "".join(f'''<li class="card" data-u="{html.escape(r['url'])}"><div><b>{html.escape(title(r['url']))}</b><small>{html.escape(r['url'].replace('https://', ''))} · {html.escape(r['google_status'])}</small></div>
<a class="go" href="{html.escape(r['inspect_link'])}" target="_blank" rel="noopener">Open in Google</a><label><input type="checkbox"> Requested</label></li>''' for r in today)
upd = datetime.date.today().strftime("%-d %b %Y")
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(f'''<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Google Indexing Today</title><style>
:root{{--bg:#f6f4f1;--card:#fff;--ink:#1b1b1b;--mut:#6b6b6b;--line:#e4e0da;--acc:#e8641c;--ok:#1f8a4c}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#121212;--card:#1d1d1d;--ink:#f1f1f1;--mut:#a3a3a3;--line:#2e2e2e;--acc:#ff7a2f;--ok:#3ccf7b}}}}
:root[data-theme="dark"]{{--bg:#121212;--card:#1d1d1d;--ink:#f1f1f1;--mut:#a3a3a3;--line:#2e2e2e;--acc:#ff7a2f;--ok:#3ccf7b}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:16px/1.45 system-ui,-apple-system,Segoe UI,Roboto,sans-serif}}
main{{max-width:560px;margin:0 auto;padding:20px 16px 48px}}h1{{font-size:24px;margin:0 0 4px}}.sub{{color:var(--mut);margin:0 0 16px}}
.stat{{display:flex;gap:10px;margin:0 0 16px}}.stat div{{flex:1;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:12px}}
.stat b{{display:block;font-size:26px}}.stat span{{color:var(--mut);font-size:13px}}
ol.how{{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:12px 12px 12px 32px;margin:0 0 18px}}ol.how li{{margin:4px 0}}
ul{{list-style:none;padding:0;margin:0;display:grid;gap:10px}}.card{{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px;display:grid;gap:10px}}
.card small{{display:block;color:var(--mut);font-size:12.5px;word-break:break-all;margin-top:2px}}
.go{{display:block;text-align:center;background:var(--acc);color:#fff;text-decoration:none;font-weight:700;padding:13px;border-radius:11px}}
label{{color:var(--mut);font-size:14px;display:flex;gap:8px;align-items:center}}.card.done{{opacity:.5}}.card.done .go{{background:var(--ok)}}
.empty{{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:18px;text-align:center}}p.note{{color:var(--mut);font-size:13px;margin-top:18px}}
</style></head><body><main>
<h1>Google indexing: this evening</h1><p class="sub">ContentFellow · updated {upd}</p>
<div class="stat"><div><b>{len(done)}</b><span>pages in Google</span></div><div><b>{len(waiting)}</b><span>requested, Google checking</span></div><div><b>{len(today)}</b><span>to tap today</span></div></div>
<div class="card all"><div><b>Step 1 · All pages in one go</b><small>Send Google the sitemap again. One submit covers every page, with no daily limit. Skip this once the robot does it for you (GOOGLE_SA_JSON set).</small></div>
<a class="go" href="https://search.google.com/search-console/sitemaps?resource_id=sc-domain%3Acontentfellow.com" target="_blank" rel="noopener">Open Sitemaps in Google</a><small>Type <b>sitemap.xml</b> in "Add a new sitemap" and tap <b>SUBMIT</b>.</small></div>
<h2 style="font-size:18px;margin:20px 0 6px">Step 2 · Fast lane (up to {DAILY} pages)</h2>
<ol class="how"><li>Tap <b>Open in Google</b>.</li><li>Wait for the check to load, then tap <b>REQUEST INDEXING</b>.</li><li>Come back and tick <b>Requested</b>. Then do the next one.</li></ol>
{f"<ul>{cards}</ul>" if today else '<div class="empty"><b>Nothing to do today 🎉</b><br>Every checked page is already in Google.</div>'}
<p class="note">Google allows about {DAILY} requests a day, so this list shows the {DAILY} most important pages. {len(rest)} more will show up tomorrow. Pages you already requested stay off the list for a week while Google checks them. Pages Google has already indexed drop off this list on their own. Open the links while signed in to the Google account that owns Search Console.</p>
</main><script>
document.querySelectorAll('.card[data-u]').forEach(c=>{{const k='idx:'+c.dataset.u+':{upd}',b=c.querySelector('input');
try{{if(localStorage.getItem(k)){{b.checked=true;c.classList.add('done')}}}}catch(e){{}}
const mark=()=>{{c.classList.toggle('done',b.checked);try{{b.checked?localStorage.setItem(k,1):localStorage.removeItem(k)}}catch(e){{}}}};
b.addEventListener('change',mark);c.querySelector('.go').addEventListener('click',()=>{{b.checked=true;mark()}});}});
</script></body></html>''')
print(f"in google: {len(done)}  waiting: {len(todo)}  today: {len(today)}")
