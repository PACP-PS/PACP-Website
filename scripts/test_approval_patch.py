#!/usr/bin/env python3
"""Verify review-only approval patch is guarded before any row lookup. Offline."""
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
class PatchSafety(unittest.TestCase):
    def test_authorization_precedes_lookup(self):
        s=(ROOT/"security/approval-auth-before-lookup-dev-PATCH-NOT-APPLIED.sql").read_text()
        lookup=s.index("select * into v_app")
        for x in ("if p_action is null or p_action not in", "and not public.can_review_membership()", "and not public.has_staff_role('membership_approver')"):
            self.assertLess(s.index(x),lookup)
    def test_no_automatic_deployment(self):
        s=(ROOT/"security/approval-auth-before-lookup-dev-PATCH-NOT-APPLIED.sql").read_text()
        self.assertIn("NOT APPLIED",s)
        self.assertIn("security definer",s.lower())
if __name__=="__main__":unittest.main(verbosity=2)
