#!/usr/bin/env python3
"""Check that staging card is auth-scoped, never official."""
import unittest
from pathlib import Path
FILE=Path(__file__).resolve().parents[1]/"PACP-Reference-Design-Cloudflare-v9/design/pages/digital-card-staging.html"
class DigitalCardContract(unittest.TestCase):
 def test_card_gated_by_auth(self):
  text=FILE.read_text()
  for token in ("client.auth.getUser()","mySummary()","membership_code","data.status","SIGNED_OUT","textContent"):self.assertIn(token,text)
 def test_no_official_issue_or_untrusted_html(self):
  text=FILE.read_text()
  self.assertIn("NOT VALID",text)
  self.assertIn("noindex,nofollow",text)
  self.assertNotIn("innerHTML",text)
  self.assertNotIn("createObjectURL",text)
  self.assertNotIn("client.from(",text)
if __name__=="__main__":unittest.main(verbosity=2)
