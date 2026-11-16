# PACP — privileged membership function review (2026-11-16)

Scope: read-only inspection of live PACP-Development PostgreSQL function definitions and grants; no live authorization, membership or content changes.

## Findings

- `public.has_staff_role(p_role text)`: STABLE SECURITY DEFINER; only authenticated EXECUTE; checks `auth.uid()` against nonrevoked records in `public.staff_role_assignments`. Uses a fixed `search_path=pg_catalog,public`. Restricted function but exposed RPC; consider private-schema migration and keep explicit object qualification.
- `public.can_review_membership()`: STABLE SECURITY DEFINER; only authenticated EXECUTE; delegates to `has_staff_role('membership_officer')` OR `has_staff_role('membership_approver')`. Currently does **not** include generic admin role; verify if intended.
- `public.pacp_report_members(p_limit integer)`: SECURITY DEFINER; only authenticated EXECUTE; checks `auth.uid()` and staff roles admin/officer/approver; validates 1–500 limit. Returns full names, email, phone, status and approved_at, so keep admin-only and do not call from the public site; check download/export and audit trail. `search_path` is empty and references are qualified.
- `public.process_membership_application(...)`: SECURITY DEFINER; only authenticated EXECUTE; requires staff role for decisions, approver specifically for approve/reject, validates application state and required fields, writes events/audit/status history. **Review order:** currently `SELECT ... FOR UPDATE` loads an application before verifying any relevant staff role. This may give unauthorized authenticated callers a distinguishable “Application not found”/“insufficient permission” or “already final” response and may temporarily lock rows. Recommend validate action type and staff role *before* row access/lock in a reviewed migration; retain row-state checks after authorization and keep transaction atomic.

## Additional privacy and workflow issues for product owner

- `approve` produces membership code and a `members.status='approved'` row. This is not the same as an active/paid/renewed/valid membership. **Never show “valid” QR based only on approved.** Confirm official activation rules, duration, fees and revocation policy before issuance.
- The public role labels must match a documented role matrix: membership_officer (review), membership_approver (decide), admin (report). The approval action does not currently treat admin as approver; clarify governance intentionally rather than silently broadening rights.
- Ensure every public verification endpoint is privacy-minimized, rate-limited, opaque-token-based and independent of protected personal information.

## Proposed remediation sequence (NOT applied)

1. Design and review permission-first flow in `process_membership_application`: auth check -> validate action -> role check -> SELECT ... FOR UPDATE -> state and payload validation -> mutation/audit. This is a controlled schema migration with rollback and tests; do not change live function before testing.
2. Negative tests with two real test JWTs and different created test membership applications (unauthorized reviewer and cross-user denial), plus authorized staff role test, done outside production personal data.
3. Review 7 SECURITY DEFINER advisor warnings and move privileged helpers into a nonexposed schema where practical without breaking existing RPC entry points; verify EXECUTE grants again.
4. Verify member status handling, period of validity and rules for QR issuance; separate `approved` from `active`.

Documentation: https://supabase.com/docs/guides/database/database-linter?lint=0029_authenticated_security_definer_function_executable

## Decision gate
No schema update, production deployment, live QR issuance, or real member credentials until explicit review and test acceptance. This report reflects code inspection, not a completed penetration test.
