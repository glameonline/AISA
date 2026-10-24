"""Pick each unsent prospect's single most-needed ContentFellow service + problem -> outputs/_plan/outreach/fit.csv.
Verified = OpenSEO get_domain_overview (19 Oct 2026, UK). Everything else is a soft observation from the prospect's own note/sector
(website crawling was blocked by the session proxy). Usage: python3 tools/build_fit.py"""
import csv, glob, re
# domain: (est. monthly organic visits, ranking keywords) from OpenSEO, 2026-10-19
SEO = {"calderit.com": (1, 3), "bandicoot.co.uk": (149, 104), "kmaccountants.co.uk": (89, 43), "kneeshaws.co.uk": (42, 9),
       "thurstons.me.uk": (19, 10), "farnworthrose.co.uk": (2203, 440), "ngasolicitors.co.uk": (214, 61), "maysonslaw.co.uk": (50, 20),
       "j700group.co.uk": (387, 253), "use-it.co.uk": (859, 342), "rraccountingsolutions.co.uk": (32, 41)}
LOG = "outputs/_plan/outreach/sent-log.csv"
def dom(u): return re.sub(r"^https?://(www\.)?", "", u.strip()).split("/")[0].lower()
def fit(r, agency):
    n, note, sec = r["name"].strip(), r.get("personal_note", "").strip(), r.get("sector", "").lower()
    if agency:
        return "partner", "you could sell more video to your clients without hiring an in-house editor", f"agency; note: {note}"
    d = dom(r.get("website", ""))
    if d in SEO:
        t, k = SEO[d]
        if t < 100:
            return "search", f"Google sends your site an estimated {t} visits a month from {k} ranking keywords, so buyers asking Google or ChatGPT \"{r['buyer_prompt'].strip(chr(34))}\" rarely find you", f"VERIFIED OpenSEO 2026-10-19: {t} visits/mo, {k} keywords"
        return "creator", f"your site already gets an estimated {t} Google visits a month, so short videos are the easiest way to turn more of those visitors into enquiries", f"VERIFIED OpenSEO 2026-10-19: {t} visits/mo, {k} keywords (visible; video is the gap)"
    if "recruit" in sec:
        return "social", "candidates and clients judge recruiters on how active they look on LinkedIn and social", f"soft: sector {sec}"
    if "architect" in sec or "surveyor" in sec or "property" in sec:
        return "studio", "finished projects and buildings sell best with professional photos and video", f"soft: sector {sec}"
    return "search", f"more buyers now ask ChatGPT or Google's AI \"{r.get('buyer_prompt','').strip().strip(chr(34))}\", and only two or three firms get named", f"soft: sector {sec}; buyer prompt"
def rows():
    sent = {l.split(",")[1].strip() for l in open(LOG).read().splitlines()[1:]}
    out, seen = [], set()
    src = [("outputs/_plan/outreach/agency-prospects.csv", True)] + [(f, False) for f in sorted(glob.glob("outputs/_plan/outreach/b2b-prospects-*.csv"))]
    for f, ag in src:
        for r in csv.DictReader(open(f)):
            e = r.get("email", "").strip().lower()
            if not e or e in seen or e in sent: continue
            seen.add(e); s, p, ev = fit(r, ag); out.append({"email": e, "service": s, "problem": p, "evidence": ev})
    return out
if __name__ == "__main__":
    o = rows()
    with open("outputs/_plan/outreach/fit.csv", "w", newline="") as f:
        w = csv.DictWriter(f, ["email", "service", "problem", "evidence"]); w.writeheader(); w.writerows(o)
    from collections import Counter
    print(len(o), Counter(x["service"] for x in o), sum(x["evidence"].startswith("VERIFIED") for x in o), "verified")
