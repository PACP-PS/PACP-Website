#!/usr/bin/env python3
"""Verify primary site navigation resolves to real files in original PACP bundle."""
from pathlib import Path
from html.parser import HTMLParser
import unittest
ROOT=Path(__file__).resolve().parents[1]/"PACP-Reference-Design-Cloudflare-v9"
class Links(HTMLParser):
 def __init__(self):super().__init__();self.links=[]
 def handle_starttag(self,tag,attrs):
  if tag=="a":
   href=dict(attrs).get("href")
   if href:self.links.append(href)
class Navigation(unittest.TestCase):
 def test_primary_links_resolve(self):
  source=(ROOT/"index.html").read_text(encoding="utf8")
  parser=Links();parser.feed(source)
  for href in parser.links:
   if href.startswith("/"):
    self.assertTrue((ROOT/href.lstrip("/")).is_file(),href)
  self.assertIn('/design/pages/auth.html',parser.links)
  self.assertIn('/design/pages/membership.html',parser.links)
  self.assertNotIn('/design/pages/member-portal-preview.html',parser.links)
 def test_original_logo_and_3d_preserved(self):
  html=(ROOT/"index.html").read_text(encoding="utf8")
  self.assertIn('/assets/pacp-logo-original.png',html)
  self.assertIn('/design/assets/brain-3d.mjs',html)
if __name__=="__main__":unittest.main(verbosity=2)
