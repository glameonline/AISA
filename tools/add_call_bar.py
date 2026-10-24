"""Adds a floating tap-to-call + WhatsApp button to every site page (owner request, 24 Oct). Idempotent. Run by build_zip.py."""
import pathlib
MARK = "<!--cf-call-->"
BAR = MARK + ('<style>.cfcall{position:fixed;right:14px;bottom:14px;z-index:99;display:flex;gap:8px}'
 '.cfcall a{display:flex;align-items:center;gap:6px;font:800 15px Inter,Arial,sans-serif;text-decoration:none;padding:12px 16px;border-radius:999px;box-shadow:0 10px 28px -8px #000}'
 '.cfcall .c{background:#ff5a1f;color:#0c0c0d}.cfcall .w{background:#25d366;color:#0c0c0d}</style>'
 '<div class="cfcall"><a class="w" href="https://wa.me/447535677302" aria-label="WhatsApp">💬</a>'
 '<a class="c" href="tel:+447535677302">📞 Call 07535 677302</a></div>')
for p in pathlib.Path("outputs/_site").rglob("*.html"):
    if "themes" in p.parts or "pay-monthly-websites" in p.parts: continue
    s = p.read_text()
    if MARK in s or "</body>" not in s: continue
    p.write_text(s.replace("</body>", BAR + "</body>", 1))
