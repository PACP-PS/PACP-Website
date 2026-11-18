#!/usr/bin/env python3
"""Offline PACP inclusion integration tests: not an accessibility conformance audit."""
from pathlib import Path
import unittest
R=Path(__file__).resolve().parents[1]
class Inclusion(unittest.TestCase):
 def test_accessibility_assets_in_build(self):
  s=(R/'scripts/build_public_preview.py').read_text()
  self.assertIn('assets/pacp-accessibility.css',s)
  self.assertIn('assets/pacp-accessibility.js',s)
 def test_page_integration(self):
  for p in ['index.html','PACP-Reference-Design-Cloudflare-v9/design/pages/membership-application-preview.html','PACP-Reference-Design-Cloudflare-v9/design/pages/course-registration-preview.html']:
   s=(R/p).read_text()
   self.assertIn('pacp-accessibility.css',s)
   self.assertIn('pacp-accessibility.js',s)
 def test_optional_accommodation(self):
  for p in ['PACP-Reference-Design-Cloudflare-v9/design/pages/membership-application-preview.html','PACP-Reference-Design-Cloudflare-v9/design/pages/course-registration-preview.html']:
   s=(R/p).read_text()
   for v in ['pacp_accommodation_request','captions','screen_reader','accessible_venue','التشخيص']:
    self.assertIn(v,s)
 def test_keyboard_motion_preferences(self):
  s=(R/'assets/pacp-accessibility.js').read_text()
  for v in ['aria-expanded','aria-pressed','Escape','pacp-main','localStorage']:
   self.assertIn(v,s)
  css=(R/'assets/pacp-accessibility.css').read_text()
  self.assertIn('prefers-reduced-motion',css)
  self.assertIn(':focus-visible',css)
if __name__=='__main__':unittest.main(verbosity=2)
