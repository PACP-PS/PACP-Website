#!/usr/bin/env python3
"""Build public PACP website from APPROVED three-column homepage, not alternate v9 homepage."""
from pathlib import Path
import shutil,sys,re,os
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/"PACP-Reference-Design-Cloudflare-v9"
DEST=ROOT/"build/pacp-public-preview"
PAGES=("about","membership","training","news","resources","contact")
ROOT_ASSETS=("assets/pacp-accessibility.css","assets/pacp-accessibility.js","assets/brain-scene-v2.webp","assets/jerusalem-scene-v2.webp","assets/jerusalem-composite.svg")
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
  # Explicit feature flags for the publishable informational-only release.
  # No live sign-in, payment, card, application or renewal promise is made.
  if file.name in ("membership.html","training.html"):
   note=('<aside role="note" aria-label="حالة الخدمات الإلكترونية" '
     'style="direction:rtl;background:#fff8e9;color:#634b20;border-right:4px solid #bd9029;'
     'padding:14px 20px;margin:14px auto;max-width:1100px;border-radius:12px;'
     'font:600 13px/1.9 Tahoma,Arial,sans-serif">'
     'خدمات الانتساب الإلكتروني وتجديد العضوية والدفع وإصدار البطاقة والتسجيل الإلكتروني '
     'قيد الإعداد، وغير مفعّلة حاليًا. المعلومات المعروضة للتعريف بخدمات الجمعية فقط.'
     '</aside>')
   data=re.sub(r'(<body[^>]*>)',lambda m:m.group(1)+note,data,count=1,flags=re.I)
  for old,new in changes.items():data=data.replace('href="'+old+'"','href="'+new+'"').replace("href='"+old+"'","href='"+new+"'")
  # Make static export portable for Android content://, file:// and HTTP servers.
  # Convert ONLY site-local absolute asset/href URLs, not external // URLs.
  prefix=os.path.relpath(DEST,file.parent).replace("\\\\","/")
  if prefix==".":prefix=""
  data=re.sub(r'(?P<lead>(?:src|href|poster)=[\\x22\\x27])/(?P<path>(?!/)[^\\x22\\x27]+)',lambda m:m.group("lead")+(prefix+"/" if prefix else "")+m.group("path"),data)
  data=re.sub(r'url\\(\\s*(?P<quote>[\\x22\\x27]?)/(?P<path>(?!/)[^)\\x22\\x27]+)(?P=quote)\\s*\\)',lambda m:"url("+m.group("quote")+(prefix+"/" if prefix else "")+m.group("path")+m.group("quote")+")",data)
  # Public social contact shortcuts: visible on every informational page.
  # Contact-only links, never personal data submission or third-party widgets.
  social_css='''<style id="pacp-social-contact-style">
.pacp-social-links{position:fixed;inset-inline-end:16px;bottom:20px;z-index:999;display:flex;flex-direction:column;gap:9px;direction:rtl}
.pacp-social-links a{display:flex;align-items:center;justify-content:center;gap:8px;min-height:44px;padding:9px 14px;border-radius:24px;color:#fff!important;font:700 15px/1.4 Tahoma,Arial,sans-serif;text-decoration:none!important;box-shadow:0 3px 12px #0003}
.pacp-social-links a:focus-visible{outline:3px solid #222;outline-offset:3px}
.pacp-social-links .pacp-whatsapp{background:#147d45}.pacp-social-links .pacp-facebook{background:#1554a7}
@media(max-width:480px){.pacp-social-links{bottom:10px;inset-inline-end:10px}.pacp-social-links a{font-size:13px;padding:8px 10px}}
@media print{.pacp-social-links{display:none}}
</style>'''
  social_html='''<nav class="pacp-social-links" aria-label="قنوات التواصل الاجتماعي للجمعية">
<a class="pacp-whatsapp" href="https://wa.me/970594090972" target="_blank" rel="noopener noreferrer" aria-label="التواصل مع الجمعية عبر واتساب على الرقم +970594090972">واتساب <span aria-hidden="true">◉</span></a>
<a class="pacp-facebook" href="https://www.facebook.com/share/1KW6rSfwkF/" target="_blank" rel="noopener noreferrer" aria-label="زيارة صفحة الجمعية على فيسبوك">فيسبوك <span aria-hidden="true">f</span></a>
</nav>'''
  if '</head>' in data:data=data.replace('</head>',social_css+'</head>',1)
  if '</body>' in data:data=data.replace('</body>',social_html+'</body>',1)
  file.write_text(data,encoding="utf8")
 # Safety: no development-only authenticated or admin workflows in public output.
 for file in DEST.rglob("*.html"):
  if any(x in file.name for x in ("-preview","staging","auth.html")):raise RuntimeError("Development page leaked: "+str(file))
 print("PACP APPROVED 3-COLUMN HERO OUTPUT:",DEST)
 return 0
if __name__=="__main__":
 try:sys.exit(main())
 except (OSError,RuntimeError) as ex:print("BUILD FAILED:",ex,file=sys.stderr);sys.exit(1)
