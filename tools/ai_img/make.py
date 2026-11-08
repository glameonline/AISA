"""Builds 'how AI answers local searches' illustration images (owner-approved design, 8 Nov 2026)."""
import subprocess, pathlib, json, os
OUT = pathlib.Path("outputs/_site/img/ai")
B = [  # slug, query, title, icon, color set, three descriptors
 ("cafe-burnley","Best cafe in Burnley","Top cafés in Burnley","☕","cafés",["Best overall for brunch","Best for atmosphere","Best for coffee"],"Café"),
 ("restaurant-burnley","Best restaurant in Burnley","Top restaurants in Burnley","🍽️","restaurants",["Best for date night","Best for families","Best value"],"Restaurant"),
 ("barber-nelson","Best barber in Nelson","Top barbers in Nelson","💈","barbers",["Best for fades","Best for beards","Walk-ins welcome"],"Barber"),
 ("salon-colne","Best hair salon in Colne","Top hair salons in Colne","💇","salons",["Best for colour","Best for cuts","Best for weddings"],"Salon"),
 ("plumber-burnley","Best plumber in Burnley","Top plumbers in Burnley","🔧","plumbers",["Best for emergencies","Best for boilers","Best reviewed"],"Plumber"),
 ("gym-burnley","Best gym in Burnley","Top gyms in Burnley","🏋️","gyms",["Best overall","Best for beginners","Best classes"],"Gym"),
 ("accountant-burnley","Best accountant in Burnley","Top accountants in Burnley","📊","accountants",["Best for small business","Best for tax returns","Best value"],"Accountant"),
]
COL=["#e9d7c0","#cfe0d6","#d6d9ea"]
def html(q,t,ic,ds,noun):
    cards="".join(f'<div style="display:flex;gap:28px;margin-top:44px;border-bottom:1px solid #eee;padding-bottom:40px"><div style="width:262px;height:262px;border-radius:30px;background:{COL[i]};flex:none;display:flex;align-items:center;justify-content:center;font-size:90px">{ic}</div><div><div style="font-size:37px;font-weight:700">{i+1}. {"Your "+noun if i==0 else noun+" "+"BC"[i-1]}</div><div style="font-size:27px;color:#777;margin-top:10px">{ds[i]}</div><div style="font-size:33px;margin-top:12px">★ {["4.9","4.7","4.6"][i]}</div></div></div>' for i in range(3))
    return f'''<html><body style="margin:0;background:#fff;font-family:-apple-system,Helvetica,Arial"><div style="width:828px;height:1500px;box-sizing:border-box;padding:60px 36px;color:#111;position:relative">
<div style="font-size:22px;color:#c58a00;font-weight:700;text-align:center">ILLUSTRATION · how AI answers local searches</div>
<div style="display:flex;justify-content:flex-end;margin-top:50px"><div style="background:#f1f1f1;border-radius:36px;padding:28px 36px;font-size:34px">{q}</div></div>
<div style="font-size:31px;color:#888;margin-top:50px">Thought for a few seconds ›</div>
<div style="font-size:40px;font-weight:700;margin-top:40px">{t}</div>{cards}
<div style="position:absolute;left:36px;right:36px;bottom:50px;background:#111;color:#fff;border-radius:30px;padding:34px;font-size:32px;line-height:1.4"><b style="color:#f5b942">Want your business here?</b><br>SEO &amp; AI Search from £89/mo · ContentFellow<br>Call/WhatsApp 07535 677302</div></div></body></html>'''
tmp=pathlib.Path(os.environ.get("TMPD","/tmp"))
for s,q,t,ic,_,ds,noun in B:
    f=tmp/f"{s}.html"; f.write_text(html(q,t,ic,ds,noun))
js="const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:828,height:1500}});for(const s of %s){await p.goto('file://%s/'+s+'.html');await p.screenshot({path:'%s/ai-search-'+s+'.png'});}await b.close()})()"%(json.dumps([b[0] for b in B]),tmp,OUT.resolve())
subprocess.run(["node","-e",js],check=True); print("made",len(B))
