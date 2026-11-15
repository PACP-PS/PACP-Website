#!/usr/bin/env python3
"""Build a public-safe PACP preview from the canonical 3D site; omit staging/admin demos."""
from pathlib import Path
import shutil,sys
SRC=Path(__file__).resolve().parents[1]/"PACP-Reference-Design-Cloudflare-v9"
DEST=Path(__file__).resolve().parents[1]/"build/pacp-public-preview"
FILES=[
"index.html","favicon.png","_headers",
"assets/pacp-logo-original.png","assets/pacp-logo.svg",
"design/assets/brain-3d.mjs","design/assets/jerusalem-panorama-v6.webp",
"design/assets/reference-brain-scene.webp","design/assets/reference-jerusalem.webp",
"design/assets/reference-membership-card.webp","design/assets/pacp-hero-illustration.svg",
"design/assets/pacp-shared-theme.css","design/assets/pacp-experience.css",
"design/assets/pacp-portal-admin-v4.css",
"design/pages/about.html","design/pages/membership.html","design/pages/training.html",
"design/pages/news.html","design/pages/resources.html","design/pages/contact.html",
]
def main():
 if not all((SRC/p).is_file() for p in FILES):
  missing=[p for p in FILES if not (SRC/p).is_file()]
  print("Cannot package; missing required assets:",missing,file=sys.stderr);return 1
 if DEST.exists():shutil.rmtree(DEST)
 for rel in FILES:
  target=DEST/rel;target.parent.mkdir(parents=True,exist_ok=True)
  shutil.copy2(SRC/rel,target)
 # The canonical homepage may link to nonpublic previews; rewrite only these
 # specific calls to action into the public membership information page.
 home=DEST/"index.html"
 s=home.read_text(encoding="utf8")
 s=s.replace('href="/design/pages/auth.html"','href="/design/pages/membership.html"')
 s=s.replace('href="/design/pages/membership-application-preview.html"','href="/design/pages/membership.html"')
 s=s.replace('href="/design/pages/member-dashboard-staging.html"','href="/design/pages/membership.html"')
 s=s.replace('href="/design/preview-center.html"','href="/design/pages/about.html"')
 home.write_text(s,encoding="utf8")
 # Explicitly prevent preview/demo administration and private auth from public artifacts.
 forbidden=["design/admin/central-admin-dashboard-preview.html","design/pages/auth.html","design/pages/member-dashboard-staging.html","design/pages/membership-submit-staging.html"]
 for rel in forbidden:
  if (DEST/rel).exists():raise RuntimeError("Forbidden public artifact: "+rel)
 print("SAFE PREVIEW READY:",DEST,"files",len(FILES))
 return 0
if __name__=="__main__":sys.exit(main())
