"""Outreach send queue for the daily auto-send (owner: 50/day, image emails, one best-fit service per company, 19 Oct).
Usage: python3 tools/email_queue.py next 50  -> JSON list of unsent {to,subject,body,html}
       python3 tools/email_queue.py mark a@b.com [c@d.com ...]  -> logs as sent
       python3 tools/email_queue.py sample  -> writes outputs/_plan/outreach/sample-email.html
Fit (service + problem) comes from tools/build_fit.py -> outputs/_plan/outreach/fit.csv."""
import csv, glob, html, json, sys, pathlib, datetime
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from agency_send_page import you
import build_fit
LOG = pathlib.Path("outputs/_plan/outreach/sent-log.csv")
TRIAL = "https://contentfellow.com/get-started/?offer=trial"
IMG = "https://contentfellow.com/img/outreach/{}.png"
SVC = {  # name, price line, what you get, page
    "search": ("Search Fellow", "£89 a month", "SEO for Google plus GEO so ChatGPT, Claude and Gemini recommend you, with a monthly ranking and AI visibility report", "/services/search-fellow/"),
    "creator": ("Creator Fellow", "£119 a month", "8 short videos, 1 motion graphics video and 1 podcast edit every month", "/services/creator-fellow/"),
    "social": ("Social Fellow", "from £59 a month", "we manage your social accounts and replies (£129 adds daily posting on up to 3 platforms)", "/services/social-fellow/"),
    "studio": ("Studio Fellow", "£149 a month", "1 on-site shoot a month with photo and 4K video, 20 edited photos within 5 working days", "/services/studio-fellow/"),
    "partner": ("white-label video service", "30 videos for £249 a month", "Reels, TikToks, YouTube and podcast edits under your brand, 2-3 day turnaround, you set your own price", "/agencies/"),
}
SUBJ = {"search": "{n}: buyers asking ChatGPT may not find you", "creator": "{n}: turning more site visitors into enquiries",
        "social": "{n}: looking active on LinkedIn without the hours", "studio": "{n}: showing your projects at their best",
        "partner": "White-label video editing for {n}?"}
OPT = "If you'd rather not hear from us, just reply \"no thanks\" and we won't email again."
def make(r, f):
    n = r["name"].strip(); k = f["service"]; name, price, what, page = SVC[k]
    note = you(r.get("personal_note", ""))
    prob = f["problem"][0].upper() + f["problem"][1:]
    subj = SUBJ[k].format(n=n)
    ag = k == "partner"
    TRIAL = "https://contentfellow.com/get-started/?service=partner-trial" if ag else globals()["TRIAL"]
    offer = "with 5 free credits to test us first (no card needed)" if ag else "with a free 7-day trial first (no card needed)"
    body = (f"Hi {n} team,\n\n{note}\n\n{prob}.\n\n"
            f"That's what our {name} is for: {what}. {price}, {offer}.\n\n"
            f"{"Claim 5 free credits" if ag else "Claim your free trial"}: {TRIAL}\nHow it works: https://contentfellow.com{page}\n\n"
            f"Best,\nThe ContentFellow team\nContentFellow · Burnley, Lancashire · https://contentfellow.com\n{OPT}")
    e = html.escape
    h = f"""<!doctype html><html><body style="margin:0;padding:0;background:#f4f4f5">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:#f4f4f5"><tr><td align="center" style="padding:24px 12px">
<table role="presentation" width="600" cellpadding="0" cellspacing="0" style="max-width:600px;width:100%;background:#ffffff;border-radius:12px;overflow:hidden;font-family:Arial,Helvetica,sans-serif;color:#1f2328;font-size:16px;line-height:1.55">
<tr><td><a href="{TRIAL}"><img src="{IMG.format(k)}" width="600" alt="{e(name)} by ContentFellow, claim your free trial" style="display:block;width:100%;height:auto;border:0"></a></td></tr>
<tr><td style="padding:28px 32px 8px">
<p style="margin:0 0 14px">Hi {e(n)} team,</p>
<p style="margin:0 0 14px">{e(note)}</p>
<p style="margin:0 0 14px"><strong>{e(prob)}.</strong></p>
<p style="margin:0 0 20px">That's what our <strong>{e(name)}</strong> is for: {e(what)}. <strong>{e(price)}</strong>, {e(offer)}.</p>
<table role="presentation" cellpadding="0" cellspacing="0"><tr><td style="border-radius:28px;background:#f26a1b"><a href="{TRIAL}" style="display:inline-block;padding:14px 30px;color:#ffffff;font-weight:bold;text-decoration:none;font-size:17px">{"Claim 5 free credits" if ag else "Claim free trial"}</a></td></tr></table>
<p style="margin:20px 0 0;font-size:14px"><a href="https://contentfellow.com{page}" style="color:#b84308">How {e(name)} works</a></p>
</td></tr>
<tr><td style="padding:20px 32px 28px">
<p style="margin:0">Best,<br>The ContentFellow team<br>ContentFellow · Burnley, Lancashire · <a href="https://contentfellow.com" style="color:#1f2328">contentfellow.com</a></p>
<p style="margin:18px 0 0;font-size:12px;color:#6b7280">{e(OPT)}</p>
</td></tr></table></td></tr></table></body></html>"""
    return {"to": f["email"], "subject": subj, "body": body, "html": h}
def queue():
    fits = {f["email"]: f for f in build_fit.rows()}  # unsent only, deduped
    src = ["outputs/_plan/outreach/agency-prospects.csv"]
    b2b = sorted((r for p in sorted(glob.glob("outputs/_plan/outreach/b2b-prospects-*.csv")) for r in csv.DictReader(open(p))), key=lambda r: r.get("ring") or "9")
    rows = list(csv.DictReader(open(src[0]))) + b2b
    out, seen = [], set()
    for r in rows:
        e = r.get("email", "").strip().lower()
        if e in fits and e not in seen:
            seen.add(e); out.append(make(r, fits[e]))
    return out
if __name__ == "__main__":
    if sys.argv[1] == "next":
        print(json.dumps(queue()[:int(sys.argv[2])]))
    elif sys.argv[1] == "sample":
        m = next(x for x in queue() if "kneeshaws" in x["to"]) if any("kneeshaws" in x["to"] for x in queue()) else queue()[0]
        pathlib.Path("outputs/_plan/outreach/sample-email.html").write_text(f"<!-- To: {m['to']} | Subject: {m['subject']} -->\n" + m["html"])
        print(m["subject"]); print(m["body"])
    else:
        new = not LOG.exists()
        with LOG.open("a") as f:
            if new: f.write("date,email\n")
            for e in sys.argv[2:]: f.write(f"{datetime.date.today()},{e.lower()}\n")
