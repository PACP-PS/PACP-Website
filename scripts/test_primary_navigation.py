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
 def test_membership_and_training_integration(self):
  for name,expected in (
   ("membership.html",("auth.html","member-dashboard-staging.html","membership-application-preview.html")),
   ("training.html",("course-registration-preview.html","../admin/course-management-preview.html"))):
   source=(ROOT/"design/pages"/name).read_text(encoding="utf8")
   parser=Links();parser.feed(source)
   for href in expected:
    self.assertIn(href,parser.links)
    self.assertTrue((ROOT/"design/pages"/href).resolve().is_file(),href)
 def test_member_admin_original_site_links(self):
  pages=(("design/pages/member-dashboard-staging.html",("../../index.html","digital-card-staging.html","auth.html")),("design/admin/central-admin-dashboard-preview.html",("../../index.html","../pages/membership-review-staging.html","../pages/auth.html")))
  for path,expected in pages:
   html=(ROOT/path).read_text(encoding="utf8")
   parser=Links();parser.feed(html)
   for href in expected:
    self.assertIn(href,parser.links)
    self.assertTrue((ROOT/path).parent.joinpath(href).resolve().is_file(),href)
 def test_original_logo_and_3d_preserved(self):
  html=(ROOT/"index.html").read_text(encoding="utf8")
  self.assertIn('/assets/pacp-logo-original.png',html)
  self.assertIn('/design/assets/brain-3d.mjs',html)
if __name__=="__main__":unittest.main(verbosity=2)
