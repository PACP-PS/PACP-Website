#!/usr/bin/env python3
"""Static authorization ordering tests. Never touches a database."""
import unittest
from pathlib import Path
SQL=(Path(__file__).resolve().parents[1]/"supabase/migrations/0003_membership_approval_engine_review_draft.sql").read_text()
class AuthorizationOrder(unittest.TestCase):
    def test_authorization_before_lookup(self):
        start=SQL.index("create or replace function public.process_membership_application")
        body=SQL[start:]
        lookup=body.index("select * into v_app")
        self.assertLess(body.index("if p_action is null or p_action not in"),lookup)
        self.assertLess(body.index("and not public.can_review_membership()"),lookup)
        self.assertLess(body.index("and not public.has_staff_role('membership_approver')"),lookup)
    def test_draft_only(self):
        self.assertIn("REVIEW DRAFT ONLY",SQL)
    def test_approval_needs_role(self):
        self.assertIn("public.has_staff_role('membership_approver')",SQL)
if __name__=="__main__": unittest.main(verbosity=2)
