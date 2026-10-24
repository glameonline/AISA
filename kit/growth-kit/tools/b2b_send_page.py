"""Phone page for the B2B GEO cold emails (IT and corporate firms), one tap each.
Reads outputs/_plan/outreach/b2b-prospects-*.csv (nearest ring first), writes outputs/b2b-outreach/index.html. Usage: python3 tools/b2b_send_page.py"""
import csv, glob, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from agency_send_page import build, you

def email(r):
    n, q = r["name"].strip(), r["buyer_prompt"].strip().strip('"')
    subj = f"Does ChatGPT recommend {n}?"
    body = (f"Hi {n} team,\n\n{you(r['personal_note'])}\n\n"
            f"More buyers now ask ChatGPT, Gemini or Google's AI Overviews questions like \"{q}\", and these tools usually name only two or three firms. "
            "Being one of them is the new page one of Google.\n\n"
            "We're ContentFellow, based in Burnley. Our Search Fellow plan does SEO and GEO (generative engine optimisation) together, so Google ranks you and AI assistants recommend you:\n\n"
            "- Free AI visibility check: we test the questions your buyers ask and show who gets named instead of you, plus the 3 fixes that matter most\n"
            "- Then a free 7-day trial, no card needed\n"
            "- £89 a month after that, cancel any time, with a monthly ranking and AI visibility report\n\n"
            "👉 Claim your free trial (2-minute form): https://contentfellow.com/get-started/?offer=trial\n"
            "How it works: https://contentfellow.com/services/search-fellow/\n\n"
            f"Would it help if we ran the check for \"{q}\" and sent you what we find?\n\n"
            "Best,\nThe ContentFellow team\nContentFellow · Burnley, Lancashire · https://contentfellow.com\n"
            "If you'd rather not hear from us, just reply \"no thanks\" and we won't email again.")
    return subj, body

if __name__ == "__main__":
    rows, seen = [], set()
    for f in sorted(glob.glob("outputs/_plan/outreach/b2b-prospects-*.csv")):
        for r in csv.DictReader(open(f)):
            key = (r.get("website") or r["name"]).lower().split("//")[-1].strip("/").removeprefix("www.")
            if key in seen or not r.get("name"): continue
            seen.add(key); rows.append(r)
    rows.sort(key=lambda r: (r.get("ring") or "9", not r.get("email", "").strip()))
    build(rows, email, pathlib.Path("outputs/b2b-outreach/index.html"), "AI Search Outreach", "AI search outreach",
          f"Search Fellow free trial · {len(rows)} IT and corporate firms, nearest to Burnley first",
          lambda r: f"{r['town']} · {r['sector']} · asks AI: “{r['buyer_prompt']}”", "b2b")
