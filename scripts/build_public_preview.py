#!/usr/bin/env python3
"""Build public PACP website from APPROVED three-column homepage, not alternate v9 homepage."""
from pathlib import Path
import shutil,sys,re,os
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"PACP-Reference-Design-Cloudflare-v9"
DEST=ROOT/"build/pacp-public-preview"
PAGES=("about","membership","training","news","resources","contact")
ROOT_ASSETS=("assets/brain-scene-v2.webp","assets/jerusalem-scene-v2.webp","assets/jerusalem-composite.svg")
INNER_ASSETS=("favicon.png","assets/pacp-logo-original.png","assets/pacp-logo.svg",
 "design/assets/jerusalem-panorama-v6.webp","design/assets/reference-brain-scene.webp",
 "design/assets/reference-jerusalem.webp","design/assets/reference-membership-card.webp",
 "design/assets/pacp-shared-theme.css","design/assets/pacp-experience.css",
 "design/assets/pacp-hero-illustration.svg")
def copy(source,target):
 if not source.is_file():raise FileNotFoundError(source)
 target.parent.mkdir(parents=True,exist_ok=True)
 shutil.copy2(source,target)
def main():
 if DEST.exists():shutil.rmtree(DEST)
 copy(ROOT/"index.html",DEST/"index.html")
 for path in ROOT_ASSETS:copy(ROOT/path,DEST/path)
 for path in INNER_ASSETS:copy(SOURCE/path,DEST/"PACP-Reference-Design-Cloudflare-v9"/path)
 for name in PAGES:copy(SOURCE/f"design/pages/{name}.html",DEST/f"PACP-Reference-Design-Cloudflare-v9/design/pages/{name}.html")
 # Disable links to demos and nonfunctional login until real auth/submission testing.
 changes={
 "/PACP-Reference-Design-Cloudflare-v9/design/pages/membership-application-preview.html":"/PACP-Reference-Design-Cloudflare-v9/design/pages/membership.html",
 "/PACP-Reference-Design-Cloudflare-v9/design/pages/member-portal-preview.html":"/PACP-Reference-Design-Cloudflare-v9/design/pages/membership.html",
 "../homepage-reference-matched.html":"../../../index.html",
 "membership-application-preview.html":"membership.html",
 "member-dashboard-staging.html":"membership.html",
 "member-portal-preview.html":"membership.html",
 "auth.html":"membership.html",
 "course-registration-preview.html":"training.html",
 "../admin/course-management-preview.html":"training.html",
 "digital-card-staging.html":"membership.html",
 "membership-review-staging.html":"membership.html",
 }
 for file in DEST.rglob("*.html"):
  data=file.read_text(encoding="utf8")
  # Public-only builds must not label an informational page as a functional sign-in.
  if file.name=="index.html":
   data=data.replace('>تسجيل الدخول</a>','>معلومات العضوية</a>')
   data=data.replace('>انتسب إلى الجمعية</a>','>شروط الانتساب</a>')
   data=data.replace('>انتسب إلى الجمعية ←</a>','>استكشف العضوية ←</a>')
  for old,new in changes.items():data=data.replace('href="'+old+'"','href="'+new+'"').replace("href='"+old+"'","href='"+new+"'")
  # Make static export portable for Android content://, file:// and HTTP servers.
  # Convert ONLY site-local absolute asset/href URLs, not external // URLs.
  prefix=os.path.relpath(DEST,file.parent).replace("\\\\","/")
  if prefix==".":prefix=""
  data=re.sub(r'(?P<lead>(?:src|href|poster)=[\\x22\\x27])/(?P<path>(?!/)[^\\x22\\x27]+)',lambda m:m.group("lead")+(prefix+"/" if prefix else "")+m.group("path"),data)
  data=re.sub(r'url\\(\\s*(?P<quote>[\\x22\\x27]?)/(?P<path>(?!/)[^)\\x22\\x27]+)(?P=quote)\\s*\\)',lambda m:"url("+m.group("quote")+(prefix+"/" if prefix else "")+m.group("path")+m.group("quote")+")",data)
  file.write_text(data,encoding="utf8")
 # Safety: no development-only authenticated or admin workflows in public output.
 for file in DEST.rglob("*.html"):
  if any(x in file.name for x in ("-preview","staging","auth.html")):raise RuntimeError("Development page leaked: "+str(file))
 print("PACP APPROVED 3-COLUMN HERO OUTPUT:",DEST)
 return 0
if __name__=="__main__":
 try:sys.exit(main())
 except (OSError,RuntimeError) as ex:print("BUILD FAILED:",ex,file=sys.stderr);sys.exit(1)
