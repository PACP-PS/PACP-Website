# PACP staging final authorization readiness — 2026-11-18

## CI: verified pass
GitHub commit `3f17c120d0a852d70f52d32228e6b0136ff6c67f`; all six workflows completed successfully. Prelaunch guardrails: https://github.com/PACP-PS/PACP-Website/actions/runs/44352112222
Includes WG-SS and accessibility source-contract tests. These are not interactive browser WCAG tests.

## Read-only database access matrix finding
PACP-Staging `aweebuukeovcekctclws`, aggregated without identifiers:
- 2 staff identities; 1 finance-only identity.
- 0 membership_approver-only identities.
- 1 identity with overlapping finance + membership_approver privileges.
- 1 superadmin identity (may overlap other roles).
- Public PACP RPCs are not executable by anon. Seven are executable by authenticated and depend on internal role guards.
**Impact:** the intended three-role *independent* live test cannot run faithfully with current role distribution. Do not weaken guards or repurpose real accounts silently.

## Minimal security-gated next actions
1. Create an additional synthetic Auth identity **through approved secure admin workflow**, or redesign role distribution after owner signoff, to obtain a dedicated membership-approver-only test identity; use synthetic email and credentials. Do not paste credentials into ChatGPT.
2. Verify the three distinct test identities' assigned effective roles and ensure the ordinary member has none, the finance user has finance only, and the approver has membership_approver only. Test superadmin separately.
3. Use `scripts/test_staging_roles_live_readonly.py` with secure per-account JWTs in a private test runner (never committed), and record only HTTP status and PASS/FAIL.
4. Test direct object-level ownership for two synthetic member applications, and negative write-paths in isolated test database with cleanup and rollback; read-only script does not cover these.
5. Independently run NVDA/VoiceOver, keyboard-only and 200%/400% zoom against rendered site. Maintain no-go for full platform launch until verified.

## Overall decision
**CI source guardrails: PASS. Staging role-separation live UAT: BLOCKED by missing approver-only identity and securely supplied sessions. WCAG conformance: not demonstrated. Full production launch: NO-GO.**
No DNS, production deployment, mail, roles, credentials or user data modified by this audit.
