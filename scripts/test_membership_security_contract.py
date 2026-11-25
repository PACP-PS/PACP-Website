#!/usr/bin/env python3
"""Static safety checks for PACP member-facing Supabase staging code.
Run from repository root: python3 scripts/test_membership_security_contract.py
Does not connect to Supabase or validate live RLS.
"""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "PACP-Reference-Design-Cloudflare-v9/design"
AUTH = BASE / "assets/pacp-supabase-auth.mjs"
DASH = BASE / "pages/member-dashboard-staging.html"
TEST = ROOT / "scripts/test_member_auth_live_readonly.py"
CARD = BASE / "pages/digital-card-staging.html"

def main():
    for path in (AUTH, DASH, TEST, CARD):
        assert path.is_file(), f"Missing source: {path.relative_to(ROOT)}"
    auth, dash, test, card = (p.read_text(encoding="utf-8") for p in (AUTH,DASH,TEST,CARD))
    assert "sb_publishable_" in auth, "Browser must use publishable key"
    assert "flowType:'pkce'" in auth, "PKCE is required in the staging Auth client"
    assert "my_membership_summary" in auth and "my_membership_applications" in auth
    assert "mySummary" in dash and "myApplications" in dash, "Dashboard must invoke the imported member-read wrappers"
    assert "from '../assets/pacp-supabase-auth.mjs'" in dash, "Dashboard must import the approved Auth module"
    assert "DEMO ONLY" in dash, "Demo information must be prominently labeled"
    assert "PACP_TEST_A_JWT" in test and "PACP_TEST_B_JWT" in test, "Cross-user tests must exist"
    for path, data in ((AUTH, auth),(DASH,dash)):
        assert not re.search(r"(?i)(service_role|sb_secret_[A-Za-z0-9_-]+)\s*[:=]\s*['\"]", data), f"Secret-looking credential in {path}"
    assert "membership_review_queue" in test, "Negative non-staff reviewer test missing"
    assert "memberState==='approved'" in card and "memberState!=='active'" in card, "Card must block approved-but-inactive members"
    assert "STAGING • NOT VALID" in card and "mySummary" in card, "Preview must be labeled and backed by member summary"
    print("PASS: static staging auth and demo safety checks")
    print("INCONCLUSIVE: live RLS, grants, cross-account isolation, and approval remain untested")

if __name__ == "__main__":
    main()
