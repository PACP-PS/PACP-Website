#!/usr/bin/env python3
"""Structural audit for optional Washington Group form fields (not WCAG certification)."""
from pathlib import Path
import unittest
R=Path(__file__).resolve().parents[1]
P=['PACP-Reference-Design-Cloudflare-v9/design/pages/membership-application-preview.html','PACP-Reference-Design-Cloudflare-v9/design/pages/member-portal-preview.html']
class WG(unittest.TestCase):
 def test_six_domains_four_choices_each(self):
  for p in P:
   s=(R/p).read_text(encoding='utf8')
   self.assertEqual(s.count('class="wg-question"'),6)
   for i in range(1,7):
    self.assertEqual(s.count('name="wg_ss_'+str(i)+'"'),4)
   self.assertIn('اختياري بالكامل',s)
   self.assertIn('لا يتم إرسال الإجابات أو حفظها',s)
 def test_no_automatic_collection(self):
  for p in P:
   s=(R/p).read_text(encoding='utf8')
   self.assertIn('wg-ss-section',s)
   self.assertNotIn('localStorage.setItem("wg_ss',s)
if __name__=='__main__':unittest.main(verbosity=2)
