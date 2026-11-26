#!/usr/bin/env python3
"""Read-only public PACP post-deployment smoke test; no credentials or writes."""
import sys, urllib.request, urllib.error
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse
BASES=["https://pacp-website.pages.dev/","https://www.pacp.ps/"]
PATHS=["","PACP-Reference-Design-Cloudflare-v9/design/pages/about.html","PACP-Reference-Design-Cloudflare-v9/design/pages/membership.html","PACP-Reference-Design-Cloudflare-v9/design/pages/training.html","PACP-Reference-Design-Cloudflare-v9/design/pages/news.html","PACP-Reference-Design-Cloudflare-v9/design/pages/resources.html","PACP-Reference-Design-Cloudflare-v9/design/pages/contact.html"]
class Links(HTMLParser):
 def __init__(self):super().__init__();self.urls=[]
 def handle_starttag(self,tag,attrs):
  if tag in ("a","img","script","link"):
   d=dict(attrs)
   for k in ("href","src"):
    if d.get(k):self.urls.append((tag,d[k]))
errors=[]
for base in BASES:
 for path in PATHS:
  url=urljoin(base,path)
  try:
   req=urllib.request.Request(url,headers={"User-Agent":"PACP-release-smoke-test/1.0"})
   with urllib.request.urlopen(req,timeout=14) as res:
    raw=res.read(3_000_000)
    if res.status!=200:raise ValueError(f"HTTP {res.status}")
    if "text/html" not in res.headers.get("content-type",""):raise ValueError("not HTML")
   html=raw.decode("utf-8","replace")
   parsed=Links();parsed.feed(html)
   if not parsed.urls:raise ValueError("no page navigation or assets found")
   if "wa.me/970594090972" not in html:raise ValueError("WhatsApp missing")
   if "facebook.com/share/1KW6rSfwkF" not in html:raise ValueError("Facebook missing")
   if path.endswith("contact.html"):
    for need in ("mailto:info@pacp.ps","tel:+970594090972","<h2>واتساب الجمعية</h2>"):
     if need not in html:raise ValueError(f"contact info missing: {need}")
   if path.endswith("membership.html") or path.endswith("training.html"):
    if "غير مفعّلة حاليًا" not in html:raise ValueError("disabled services notice missing")
   print("PASS",url)
  except (urllib.error.URLError,TimeoutError,ValueError,OSError) as exc:
   errors.append(f"{url}: {type(exc).__name__}: {exc}")
for e in errors:print("FAIL",e,file=sys.stderr)
sys.exit(bool(errors))
