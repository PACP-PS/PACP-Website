# PACP Membership Authorization — Read-only Audit (2026-11-16)

**Scope:** Supabase PACP-Development, project `lofvxgubetdslvaczvjp`. This is a limited audit, **not** a security certification, and **not** approval for live issuance.

## Read-only simulated-account checks executed
Transactions used `BEGIN READ ONLY`, `SET LOCAL ROLE authenticated`, and an unused synthetic JWT subject `00000000-0000-4000-8000-000000000001`, then `ROLLBACK`. No user, member, membership request, token, or role record was created or altered.

1. `my_membership_summary()` returned SQL NULL for the synthetic unregistered user: **PASS**.
2. `my_membership_applications()` returned empty JSON array: **PASS**.
3. `membership_review_queue(5)` raised `insufficient_privilege` for this synthetic nonstaff user: **PASS**.

**Limitations:** SQL role/JWT simulation is NOT equivalent to two different signed-in Supabase Auth sessions. It cannot prove against cross-account data leakage, forged tokens, JWT session behavior, Storage access or role escalation. Execute `scripts/test_member_auth_live_readonly.py` using two *distinct synthetic account JWTs and distinct application records* held in private environment variables, without logging credentials. Test actual staff/nonstaff and other-account denial before enablement.

## Security advisor findings
Security advisors yielded 7 `authenticated_security_definer_function_executable` WARN findings:
- `can_review_membership()`
- `has_staff_role(text)`
- `membership_review_queue(integer)`
- `my_membership_applications()`
- `my_membership_summary()`
- `pacp_report_members(integer)`
- `process_membership_application(uuid,text,text,text)`

These findings report broad API callability to authenticated users, **not proven exploitable behavior**. Review each function's authorization, grants, and search_path before deciding whether to revoke EXECUTE, move to private schema, or refactor. Any change must preserve needed member reads and administrator workflows.

Five RLS-enabled tables have no policies: `activity_accreditations`, `audit_log`, `contact_inquiries`, `payment_records`, `staff_role_assignments`. No-policy normally denies row access, but check table grants/expected uses, especially privileged functions; do not create permissive policies just to silence the linter.

Advisor reference: https://supabase.com/docs/guides/database/database-linter?lint=0029_authenticated_security_definer_function_executable

## Release blockers / next work
- Complete a full audit of `has_staff_role`, `process_membership_application`, `pacp_report_members`, privileged functions and object grants; record proposed hardening in a reviewed migration.
- Two real synthetic JWT sessions, BOLA/RLS denial matrix, admin/non-admin tests and private document Storage tests.
- Confirm server-authoritative active/expired/revoked membership state; only then build production digital card and opaque-QR verification endpoint.
- Security and user visual approval before staging/production. No deployment, DNS, mail or production membership changes performed.
