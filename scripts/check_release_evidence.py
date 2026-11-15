#!/usr/bin/env python3
"""Non-destructive release gate reporter. FAILS closed until manual evidence is recorded.
No passwords, tokens, member identifiers, or real member data belong in evidence.
"""
import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PATH=ROOT/"security/release-evidence.json"
REQUIRED=("synthetic_account_isolation","reviewer_role_denial","approver_role_denial","approval_transition_rollback","private_storage_isolation","password_reset_redirects","membership_governance_signoff","backup_restore_rehearsal","mobile_accessibility_review")
def main():
    data=json.loads(PATH.read_text(encoding="utf-8"))
    checks=data.get("checks",{})
    missing=[key for key in REQUIRED if checks.get(key,{}).get("status")!="passed" or not checks.get(key,{}).get("evidence")]
    if data.get("production_approval") is not True:missing.append("production_approval")
    if missing:
        print("BLOCKED: production release conditions not met")
        for item in missing:print(" - "+item)
        return 1
    print("Evidence checklist complete. Independent human release review still mandatory.")
    return 0
if __name__=="__main__":sys.exit(main())
