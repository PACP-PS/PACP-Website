#!/usr/bin/env python3
"""PACP fail-closed staging contract tests. Offline, no accounts or secrets."""
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/"PACP-Reference-Design-Cloudflare-v9"/"design"/"pages"
class StagingSafety(unittest.TestCase):
    def test_submit_stays_disabled(self):
        page=(BASE/"membership-submit-staging.html").read_text()
        self.assertIn("const enabled=false",page)
        self.assertIn('id="submit" disabled',page)
        self.assertIn("if(!enabled||!user)",page)
        self.assertNotIn("const enabled=true",page)
    def test_review_uses_server_authorization(self):
        page=(BASE/"membership-review-staging.html").read_text()
        self.assertIn("client.auth.getUser()",page)
        self.assertIn("membership_review_queue",page)
        self.assertIn("textContent",page)
        self.assertNotIn("innerHTML",page)
        self.assertNotIn("process_membership_application",page)
    def test_rpc_is_review_only(self):
        sql=(ROOT/"security"/"submit-membership-rpc-REVIEW-ONLY.sql").read_text()
        self.assertIn("auth.uid()",sql)
        self.assertIn("membership_payload_shape_errors",sql)
        self.assertIn("grant execute",sql.lower())
        self.assertIn("revoke all",sql.lower())
        self.assertIn("applicant_user_id",sql)
        self.assertIn("status in ('submitted','under_review','needs_changes')",sql)
    def test_original_brand_and_noindex(self):
        for name in ("membership-review-staging.html","membership-submit-staging.html"):
            page=(BASE/name).read_text()
            self.assertIn("pacp-logo-original.png",page)
            self.assertIn("noindex,nofollow",page)
if __name__=="__main__":
    unittest.main(verbosity=2)
