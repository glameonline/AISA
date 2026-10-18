"""Outreach send queue for the daily auto-send (owner approved 30/day on 18 Oct).
Usage: python3 tools/email_queue.py next 30  -> prints JSON list of unsent {to,subject,body}
       python3 tools/email_queue.py mark a@b.com [c@d.com ...]  -> logs as sent"""
import csv, glob, json, sys, pathlib, datetime
sys.path.insert(0, str(pathlib.Path(__file__).parent))
import agency_send_page as A, b2b_send_page as B
LOG = pathlib.Path("outputs/_plan/outreach/sent-log.csv")
def queue():
    q, seen = [], set()
    for r in csv.DictReader(open("outputs/_plan/outreach/agency-prospects.csv")):
        q.append((r, A.email))
    rows = [r for f in sorted(glob.glob("outputs/_plan/outreach/b2b-prospects-*.csv")) for r in csv.DictReader(open(f))]
    rows.sort(key=lambda r: r.get("ring") or "9")
    q += [(r, B.email) for r in rows]
    out = []
    for r, fn in q:
        e = r.get("email", "").strip().lower()
        if not e or e in seen: continue
        seen.add(e); s, b = fn(r); out.append({"to": e, "subject": s, "body": b})
    return out
sent = {l.split(",")[1] for l in LOG.read_text().splitlines()[1:]} if LOG.exists() else set()
if sys.argv[1] == "next":
    print(json.dumps([m for m in queue() if m["to"] not in sent][:int(sys.argv[2])]))
else:
    new = not LOG.exists()
    with LOG.open("a") as f:
        if new: f.write("date,email\n")
        for e in sys.argv[2:]: f.write(f"{datetime.date.today()},{e.lower()}\n")
