#!/usr/bin/env python3
"""Static course tab and membership text checks; does not replace a browser audit."""
import unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
class AccessibilityRegression(unittest.TestCase):
 def test_course_tabs_keyboard_support(self):
  s=(R/'PACP-Reference-Design-Cloudflare-v9/design/pages/course-registration-preview.html').read_text()
  for token in ('role="tablist"','role="tab"','role="tabpanel"','aria-selected','aria-controls','ArrowLeft','ArrowRight','Home','End','tabIndex'):
   self.assertIn(token,s)
  for name in ('public','register','admin'):
   self.assertIn('id="tab-'+name+'"',s)
   self.assertIn('aria-labelledby="tab-'+name+'"',s)
 def test_membership_legibility(self):
  s=(R/'PACP-Reference-Design-Cloudflare-v9/design/pages/membership-application-preview.html').read_text()
  self.assertIn('font-size:1rem',s)
  self.assertIn('min-height:44px',s)
  self.assertIn('prefers-reduced-motion',s)
if __name__=='__main__':unittest.main(verbosity=2)
