#!/usr/bin/env python3
"""One and only PACP publishable tree. No deployment and no writes to project files."""
from pathlib import Path
from html.parser import HTMLParser
import sys
ROOT=Path(__file__).resolve().parents[1]
SITE=ROOT/"PACP-Reference-Design-Cloudflare-v9"
class Refs(HTMLParser):
 def __init__(self): super().__init__();self.refs=[]
 def handle_starttag(self,tag,attrs):
  attrs=dict(attrs)
  for key in ("href","src"):
   v=attrs.get(key,"")
   if v.startswith("/") and not v.startswith("//"):self.refs.append(v.split("?")[0].split("#")[0])
def main():
 required=[SITE/"index.html", SITE/"assets/pacp-logo-original.png",SITE/"design/assets/brain-3d.mjs", SITE/"design/pages/auth.html",SITE/"design/pages/membership.html"]
 errors=[str(p) for p in required if not p.is_file()]
 home=(SITE/"index.html").read_text(encoding="utf-8")
 parser=Refs();parser.feed(home)
 for url in parser.refs:
  if not (SITE/url.lstrip("/")).is_file():errors.append("BROKEN ROOT-ASSET "+url)
 if "/design/assets/brain-3d.mjs" not in home:errors.append("Missing approved 3D scene")
 if '/assets/pacp-logo-original.png' not in home:errors.append("Missing original PACP logo")
 if "/design/pages/auth.html" not in home:errors.append("Missing real account navigation")
 if errors:
  for error in errors:print("ERROR",error)
  return 1
 print("PASS: canonical package only:",SITE.relative_to(ROOT))
 print("PASS: original logo, 3D script, auth navigation, root-relative assets")
 print("NOTE: visual sign-off and functional Supabase UAT remain separate.")
 return 0
if __name__=="__main__":sys.exit(main())
