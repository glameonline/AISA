"""GA4 events for call / WhatsApp / email clicks + sticky mobile call bar on blog posts. Marker <!--cf-track-->."""
import pathlib
JS = ('<!--cf-track--><script>document.addEventListener("click",function(e){var a=e.target.closest&&e.target.closest("a");if(!a||!window.gtag)return;var h=a.getAttribute("href")||"";'
      'var t=h.indexOf("tel:")==0?"call_click":h.indexOf("mailto:")==0?"email_click":/wa\\.me|whatsapp/.test(h)?"whatsapp_click":"";'
      'if(t)gtag("event",t,{link_url:h,page_path:location.pathname})});</script>')
BAR = ('<div style="position:fixed;left:0;right:0;bottom:0;z-index:99;display:flex;gap:8px;padding:10px;background:#0c0c0d;border-top:1px solid #333" class="cf-mbar">'
       '<a href="tel:+447535677302" style="flex:1;text-align:center;padding:12px;border-radius:999px;background:#ff5a1f;color:#000;font-weight:700;text-decoration:none">📞 Call now</a>'
       '<a href="https://wa.me/447535677302" style="flex:1;text-align:center;padding:12px;border-radius:999px;background:#25d366;color:#000;font-weight:700;text-decoration:none">WhatsApp</a>'
       '<a href="mailto:info@contentfellow.com" style="flex:1;text-align:center;padding:12px;border-radius:999px;background:#fff;color:#000;font-weight:700;text-decoration:none">Email</a></div>'
       '<style>@media(min-width:800px){.cf-mbar{display:none!important}}body{padding-bottom:70px}</style>')
n = 0
for f in pathlib.Path("outputs/_site").rglob("index.html"):
    p = str(f)
    if "/themes/" in p: continue
    s = f.read_text()
    if "<!--cf-track-->" in s or "</body>" not in s: continue
    add = JS + (BAR if "/blog/" in p and not p.endswith("blog/index.html") and "<!--cf-call-->" not in s else "")
    f.write_text(s.replace("</body>", add + "</body>", 1)); n += 1
print("tracking added:", n)
