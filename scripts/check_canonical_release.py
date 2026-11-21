#!/usr/bin/env python3
"""Assert that the release hero is the approved brain-left / copy-center / Jerusalem-right design."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
PAGE=ROOT/"index.html"
SRC=ROOT/"PACP-Reference-Design-Cloudflare-v9"
def main():
 s=PAGE.read_text(encoding="utf8")
 must=("class=\"hero-art brain-hero\"","class=\"hero-copy\"","class=\"jerusalem-hero\"",
 "assets/brain-scene-v2.webp","jerusalem-panorama-v6.webp","pacp-logo-original.png")
 failed=[item for item in must if item not in s]
 files=(ROOT/"assets/brain-scene-v2.webp",SRC/"design/assets/jerusalem-panorama-v6.webp",SRC/"assets/pacp-logo-original.png")
 failed += [str(p) for p in files if not p.is_file()]
 if failed:
  print("FAIL: approved original hero is incomplete",failed);return 1
 print("PASS: approved brain-left / center-copy / Jerusalem-right homepage source")
 print("NOTE: browser-based screenshot comparison is still required")
 return 0
if __name__=="__main__":sys.exit(main())
