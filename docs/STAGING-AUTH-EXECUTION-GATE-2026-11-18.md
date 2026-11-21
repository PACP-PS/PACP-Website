# PACP Staging Authorization — Execution Gate (18 November 2026)

## Completed in this session
- Reviewed GitHub Actions run 44336092990: five supporting sandbox workflows passed; prelaunch guardrails failed at accessibility integration because the test expected literal "التشخيص" while preview copy contained "تشخيص".
- Corrected this assertion on development branch (commit 40052d4530698c8712ac953ef7abdae194e0c52f). **New workflow result remains unverified.**
- Verified Staging has two finance role records, one membership approver and one superadmin assignment. Role counts do not establish which permissions are effectively available to separate signed-in users.
- Reviewed `scripts/test_staging_roles_live_readonly.py`: secure, staging-only, read-only smoke checks for three distinct authenticated sessions.
- No JWTs, passwords, auth sessions, role assignments or production resources modified.

## Secure test execution checklist
1. Obtain *independent synthetic sessions* for member, finance-only, and approver-only; verify no unintended overlap in role assignments.
2. Supply `PACP_STAGING_URL`, `PACP_STAGING_PUBLISHABLE_KEY`, and three `PACP_STAGING_{MEMBER,FINANCE,APPROVER}_JWT` variables in a trusted local process, not chat/repository or long-lived GitHub Actions secrets unless strictly controlled.
3. Run `python3 scripts/test_staging_roles_live_readonly.py` locally; capture only sanitized PASS/FAIL, dates and tested commit. Remove temporary credentials after testing.
4. If any identity or role cannot be verified, stop as INCONCLUSIVE; do not claim permission tests passed.
5. Future test scope: cross-member ownership, read/write separation, financial approval and card issuance; use isolated test data with cleanup plan.

## Immediate blockers
- A confirmed post-fix CI PASS on the final commit.
- Three role-separated synthetic JWTs in an approved secure runtime.
- Browser-based manual accessibility tests at 200% and 400% zoom, RTL keyboard, VoiceOver/NVDA, and screen reader/form errors.
- Production release requires explicit owner approval and security signoff.
