#!/usr/bin/env python3
"""PACP final release safety checks (offline, read-only).

Run: python3 scripts/test_final_release_paths.py
This is a repository contract test, NOT proof of deployed security or human UAT.
"""
from pathlib import Path
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]
def read(path):
    return (ROOT / path).read_text(encoding="utf-8")

class ReleasePaths(unittest.TestCase):
    def test_public_website_keeps_sensitive_services_disabled(self):
        build = read("scripts/build_public_preview.py")
        self.assertIn('"membership-review-staging.html":"membership.html"', build)
        self.assertIn('"auth.html":"membership.html"', build)
        self.assertIn('"digital-card-staging.html":"membership.html"', build)
        self.assertIn('"course-registration-preview.html":"training.html"', build)
        self.assertIn('"-preview","staging","auth.html"', build)
        self.assertIn("غير مفعّلة حاليًا", build)

    def test_private_release_gate_requires_manual_approval(self):
        gate = read("scripts/check_release_evidence.py")
        self.assertIn('data.get("production_approval") is not True', gate)
        for check in ("synthetic_account_isolation","reviewer_role_denial",
                      "approver_role_denial","approval_transition_rollback",
                      "private_storage_isolation","backup_restore_rehearsal",
                      "mobile_accessibility_review","membership_governance_signoff"):
            self.assertIn(check, gate)

    def test_staging_submit_is_not_live(self):
        page = read("PACP-Reference-Design-Cloudflare-v9/design/pages/membership-submit-staging.html")
        self.assertIn("const enabled=false", page)

    def test_prelaunch_ci_has_no_automatic_production_deploy(self):
        workflow = read(".github/workflows/prelaunch-guardrails.yml")
        self.assertNotIn("wrangler pages deploy", workflow)
        self.assertNotIn("cloudflare/pages-action", workflow)
        self.assertIn("test_release_gate.py", workflow)

if __name__ == "__main__":
    unittest.main(verbosity=2)
