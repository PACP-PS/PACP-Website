#!/usr/bin/env python3
"""Fail public release if local HTML references are broken or unsafe."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import sys

ROOT = Path("pacp-public-preview").resolve()
class Links(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.refs=[]
    def handle_starttag(self, tag, attrs):
        data=dict(attrs)
        for key in ("href","src","poster"):
            if key in data and data[key]:
                self.refs.append((tag,key,data[key]))
errors=[]
pages=sorted(ROOT.rglob("*.html"))
if len(pages)!=7:
    errors.append(f"Expected 7 informational pages; found {len(pages)}")
for page in pages:
    html=page.read_text(encoding="utf-8")
    parser=Links();parser.feed(html)
    for tag,attr,value in parser.refs:
        if value.startswith(("#","mailto:","tel:","data:","javascript:")):
            if value.startswith("javascript:"):errors.append(f"{page}: unsafe javascript: URL")
            continue
        parsed=urlsplit(value)
        if parsed.scheme or parsed.netloc:continue
        path=unquote(parsed.path)
        if not path:continue
        target=(ROOT/path.lstrip("/") if path.startswith("/") else page.parent/path).resolve()
        if target.is_dir():target=target/"index.html"
        if not target.is_relative_to(ROOT):
            errors.append(f"{page.relative_to(ROOT)}: outside published root: {value}")
        elif not target.is_file():
            errors.append(f"{page.relative_to(ROOT)}: missing {attr}={value}")
for error in errors:print("ERROR:",error)
if errors:sys.exit(1)
print(f"PASS: checked local references and release isolation in {len(pages)} pages")
