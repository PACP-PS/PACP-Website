#!/usr/bin/env python3
"""Audit generated public PACP site, not just the development source tree."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit,unquote
import re, subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
SITE=ROOT/"build/pacp-public-preview"
class Parser(HTMLParser):
 def __init__(self):super().__init__();self.links=[]
 def handle_starttag(self,tag,attrs):
  attrs=dict(attrs)
  for k in ("href","src","poster"):
   if attrs.get(k):self.links.append((tag,k,attrs[k]))
  if attrs.get("srcset"):
   for part in attrs["srcset"].split(","):self.links.append((tag,"srcset",part.strip().split(" ")[0]))
def main():
 if not SITE.exists():
  r=subprocess.run([sys.executable,str(ROOT/"scripts/build_public_preview.py")])
  if r.returncode:return r.returncode
 errors=[];warnings=[];n=0
 for html in SITE.rglob("*.html"):
  parser=Parser();parser.feed(html.read_text(encoding="utf8"))
  for tag,attr,raw in parser.links:
   url=urlsplit(raw.strip())
   if raw.strip().lower().startswith("javascript:"):errors.append(f"{html.relative_to(SITE)}: unsafe javascript link");continue
   if url.scheme in ("https","http") or raw.startswith(("#","mailto:","tel:","data:","//")):continue
   if url.scheme:continue
   target=(SITE/url.path.lstrip("/")) if raw.startswith("/") else (html.parent/unquote(url.path))
   if not target.is_file():errors.append(f"{html.relative_to(SITE)}: missing {raw}")
   n+=1
  text=html.read_text(encoding="utf8")
  if "fonts.googleapis.com" in text:warnings.append(f"{html.relative_to(SITE)}: Alexandria depends on Google Fonts availability; fallback may render differently")
  if "supabase.co" in text:warnings.append(f"{html.relative_to(SITE)}: external Supabase reference in public HTML; review")
  if re.search(r"(?i)(?:pacp-supabase-auth\\.mjs|supabase\\.co/(?:rest|auth|functions)/v1|sb_secret_|service_role)",text):errors.append(f"{html.relative_to(SITE)}: private platform API/auth reference in public export")
 for css in SITE.rglob("*.css"):
  for raw in re.findall(r'url\(\s*[\x22\x27]?([^\x22\x27)]+)',css.read_text(encoding="utf8")):
   if raw.startswith(("data:","https:","http:","//","#")):continue
   target=(SITE/raw.lstrip("/")) if raw.startswith("/") else css.parent/raw
   if not target.is_file():errors.append(f"{css.relative_to(SITE)}: missing CSS asset {raw}")
 for html in SITE.rglob("*.html"):
  if any(x in html.as_posix() for x in ("/admin/","staging","-preview.html","/auth.html")):errors.append(f"Nonpublic page exported: {html}")
 print(f"Audited {len(list(SITE.rglob('*.html')))} exported pages, {n} local references")
 for x in sorted(set(warnings)):print("WARNING:",x)
 for x in sorted(set(errors)):print("ERROR:",x)
 print("PASS" if not errors else "FAIL")
 return int(bool(errors))
if __name__=="__main__":sys.exit(main())
