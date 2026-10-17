"""Phone page for sending the agency cold emails one tap at a time (mailto, pre-filled).
Reads outputs/_plan/outreach/agency-prospects.csv, writes outputs/agency-outreach/index.html. Usage: python3 tools/agency_send_page.py"""
import csv, html, re, pathlib, urllib.parse
DAILY = 15
VERB = {"is": "are", "has": "have", "does": "do"}
def you(s):
    s = s.strip()
    for a, b in [(r"\bThey're\b", "You're"), (r"\bthey're\b", "you're"), (r"\bThey've\b", "You've"), (r"\bthey've\b", "you've"), (r"\bThey\b", "You"), (r"\bthey\b", "you"),
                 (r"\bTheir\b", "Your"), (r"\btheir\b", "your"), (r"\bthemselves\b", "yourselves"), (r"\bthem\b", "you")]:
        s = re.sub(a, b, s)
    s = re.sub(r"\b(you|You) (is|has|does|[a-z]+?s)\b(?= )", lambda m: f"{m.group(1)} {VERB.get(m.group(2), m.group(2)[:-2] if m.group(2).endswith(('ses', 'shes', 'ches', 'xes')) else m.group(2)[:-1])}" if m.group(2) in VERB or not m.group(2).endswith(("ss", "us", "is", "ys")) else m.group(0), s)
    return re.sub(r"\b(you|You) (also|already|now) has\b", r"\1 \2 have", s)
def email(r):
    n = r["name"].strip()
    subj = f"White-label video editing for {n}?"
    body = (f"Hi {n} team,\n\n{you(r['personal_note'])}\n\n"
            "We're ContentFellow, a video and content studio in Burnley. We edit Reels, TikToks, YouTube videos and podcasts for agencies under the agency's own brand, "
            "so you can sell more video to your clients without hiring an editor.\n\n"
            "- 30 short videos for £249 a month (80 for £599), 2-3 day turnaround\n- No ContentFellow branding; you set your own price\n"
            "- On-site shoots in Lancashire, Manchester and Yorkshire from £295\n- 5 free credits to test us, no card needed\n\n"
            "Details: https://contentfellow.com/agencies/\n\nWould it be worth sending one client's footage to try it?\n\n"
            "Best,\nThe ContentFellow team\nContentFellow · Burnley, Lancashire · https://contentfellow.com\n"
            "If you'd rather not hear from us, just reply \"no thanks\" and we won't email again.")
    return subj, body
def build(ROWS, email, OUT, TITLE, H1, SUB, META, KEY):
    cards = []
    for i, r in enumerate(ROWS):
        subj, body = email(r)
        if r["email"].strip():
            href = f"mailto:{r['email'].strip()}?subject={urllib.parse.quote(subj)}&body={urllib.parse.quote(body)}"
            action = f'<a class="go" href="{html.escape(href)}">Open email to {html.escape(r["email"].strip())}</a>'
        else:
            action = (f'<a class="go alt" href="{html.escape(r["contact_page"] or r["website"])}" target="_blank" rel="noopener">Open contact form</a>'
                      f'<button class="copy" data-t="{html.escape(body)}">Copy message</button>')
        cards.append(f'<li class="card" data-k="{i}" data-day="{1 + i // DAILY}"><div><b>{html.escape(r["name"])}</b><small>{html.escape(META(r))}</small>'
                     f'<details><summary>Preview</summary><pre>{html.escape(body)}</pre></details></div>{action}<label><input type="checkbox"> Sent</label></li>')
    n_mail = sum(1 for r in ROWS if r["email"].strip())
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(f'''<!doctype html><html lang="en-GB"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
    <title>{TITLE}</title><style>
    :root{{--bg:#f6f4f1;--card:#fff;--ink:#1b1b1b;--mut:#6b6b6b;--line:#e4e0da;--acc:#e8641c;--ok:#1f8a4c}}
    @media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#121212;--card:#1d1d1d;--ink:#f1f1f1;--mut:#a3a3a3;--line:#2e2e2e;--acc:#ff7a2f;--ok:#3ccf7b}}}}
    :root[data-theme="dark"]{{--bg:#121212;--card:#1d1d1d;--ink:#f1f1f1;--mut:#a3a3a3;--line:#2e2e2e;--acc:#ff7a2f;--ok:#3ccf7b}}
    *{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:16px/1.45 system-ui,-apple-system,Segoe UI,Roboto,sans-serif}}
    main{{max-width:560px;margin:0 auto;padding:20px 16px 48px}}h1{{font-size:24px;margin:0 0 4px}}.sub{{color:var(--mut);margin:0 0 14px}}
    .stat{{display:flex;gap:10px;margin:0 0 14px}}.stat div{{flex:1;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:12px}}.stat b{{display:block;font-size:24px}}.stat span{{color:var(--mut);font-size:13px}}
    ol.how{{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:12px 12px 12px 32px;margin:0 0 14px}}
    .tabs{{display:flex;gap:8px;flex-wrap:wrap;margin:0 0 12px}}.tabs button{{border:1px solid var(--line);background:var(--card);color:var(--ink);border-radius:999px;padding:7px 12px;font:inherit;font-size:14px}}.tabs button.on{{background:var(--acc);color:#fff;border-color:var(--acc)}}
    ul{{list-style:none;padding:0;margin:0;display:grid;gap:10px}}.card{{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:14px;display:grid;gap:10px}}
    .card small{{display:block;color:var(--mut);font-size:12.5px;margin-top:2px}}details{{margin-top:6px;font-size:13px}}pre{{white-space:pre-wrap;font:13px/1.45 system-ui,sans-serif;color:var(--mut)}}
    .go{{display:block;text-align:center;background:var(--acc);color:#fff;text-decoration:none;font-weight:700;padding:13px;border-radius:11px;word-break:break-all}}.go.alt{{background:#555}}
    .copy{{border:1px solid var(--line);background:transparent;color:var(--ink);border-radius:11px;padding:10px;font:inherit}}
    label{{color:var(--mut);font-size:14px;display:flex;gap:8px;align-items:center}}.card.done{{opacity:.5}}.card.done .go{{background:var(--ok)}}
    p.note{{color:var(--mut);font-size:13px;margin-top:18px}}
    </style></head><body><main>
    <h1>{H1}</h1><p class="sub">{SUB}</p>
    <div class="stat"><div><b>{n_mail}</b><span>with email</span></div><div><b>{len(ROWS) - n_mail}</b><span>contact form only</span></div><div><b id="sent">0</b><span>sent</span></div></div>
    <ol class="how"><li>Pick today's batch below.</li><li>Tap the orange button: Gmail opens with the email ready. Check it and tap <b>Send</b>.</li><li>Come back; it's ticked as sent. Do up to {DAILY} a day so Gmail doesn't flag you.</li></ol>
    <div class="tabs" id="tabs"></div>
    <ul id="list">{"".join(cards)}</ul>
    <p class="note">Every address was taken from the agency's own website. Each email has an opt-out line (UK PECR). Paste replies to Claude in chat for a ready answer. Follow-up after 5 days if there's no reply.</p>
    </main><script>
    const list=[...document.querySelectorAll('.card')],tabs=document.getElementById('tabs'),days=Math.max(...list.map(c=>+c.dataset.day));
    const st=k=>{{try{{return localStorage.getItem('{KEY}:'+k)}}catch(e){{return null}}}},sv=(k,v)=>{{try{{v?localStorage.setItem('{KEY}:'+k,1):localStorage.removeItem('{KEY}:'+k)}}catch(e){{}}}};
    const count=()=>document.getElementById('sent').textContent=list.filter(c=>c.classList.contains('done')).length;
    function show(d){{list.forEach(c=>c.hidden=d&&+c.dataset.day!==d);[...tabs.children].forEach(b=>b.classList.toggle('on',+b.dataset.d===d))}}
    for(let d=1;d<=days;d++){{const b=document.createElement('button');b.textContent='Day '+d;b.dataset.d=d;b.onclick=()=>show(d);tabs.appendChild(b)}}
    const all=document.createElement('button');all.textContent='All';all.dataset.d=0;all.onclick=()=>show(0);tabs.appendChild(all);
    list.forEach(c=>{{const b=c.querySelector('input'),k=c.dataset.k;if(st(k)){{b.checked=true;c.classList.add('done')}}
    const m=()=>{{c.classList.toggle('done',b.checked);sv(k,b.checked);count()}};b.onchange=m;
    c.querySelector('.go').addEventListener('click',()=>{{b.checked=true;m()}});
    const cp=c.querySelector('.copy');if(cp)cp.onclick=()=>{{navigator.clipboard&&navigator.clipboard.writeText(cp.dataset.t);cp.textContent='Copied ✓'}}}});
    count();show(1);
    </script></body></html>''')
    print(OUT, "rows:", len(ROWS), "with email:", n_mail)


if __name__ == "__main__":
    rows = list(csv.DictReader(open("outputs/_plan/outreach/agency-prospects.csv")))
    build(rows, email, pathlib.Path("outputs/agency-outreach/index.html"), "Agency Outreach Sender", "Agency outreach",
          f"White-label Partner Fellow · {len(rows)} agencies in Lancashire, Manchester and Yorkshire", lambda r: f"{r['town']} · {r['services'][:80]}", "ao")
