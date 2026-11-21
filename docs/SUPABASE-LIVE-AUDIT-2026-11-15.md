# PACP Supabase live-access audit update — 2026-11-15

Project: `PACP-Development` (`lofvxgubetdslvaczvjp`)  
Branch: `rebuild/platform-foundation`  
Audit mode: **read-only**. No data, schema, roles, billing, DNS or production changes.

## Current state

- Supabase project progressed through `COMING_UP` to `ACTIVE_HEALTHY` during this review.
- Read-only SQL now succeeds. Public schema contains **17 tables, 14 RLS policies and 8 functions**.
- **All 17 public tables have RLS enabled**. Five have **no policies**, namely `activity_accreditations`, `audit_log`, `contact_inquiries`, `payment_records`, and `staff_role_assignments`. This is not inherently a vulnerability if those tables are intentionally unavailable to client roles.
- Database security advisor reports **7 SECURITY DEFINER functions executable by `authenticated`**. These include role checks, private member summary and applications, membership review queue, reporting, and membership application processing. This is a **review-required warning**, not proof of exploitation. Verify functions' internal permission gates, execution owners, grants, search_path and data-return minimization.
- Grant metadata shows very broad table privileges including `INSERT`, `UPDATE`, `DELETE`, `TRUNCATE` and `TRIGGER` assigned to `anon` and `authenticated` on numerous public tables. RLS may block row-level operations, but grants should still be minimized. **Priority security remediation** is to reduce unnecessary privileges only after a complete impact analysis and test accounts are available.
- Source inspection confirms `my_membership_summary()` selects rows by authenticated `auth.uid()` and returns limited summary fields, and `my_membership_applications()` filters by `applicant_user_id = auth.uid()`. This is a positive code-level finding, **not** an end-to-end cross-user proof.
- Source inspection confirms `pacp_report_members()` checks specific trusted staff roles. `process_membership_application()` checks reviewer/approver roles at action boundaries; thorough integration tests are still required.

## New staged implementation

Created `design/pages/member-dashboard-staging.html`:
- Read-only authenticated member workspace using the existing publishable Supabase client.
- Session gate via `client.auth.getUser()` and server RPCs `my_membership_summary()` and `my_membership_applications()`.
- Fields shown are restricted to member name, membership code, status, approval date, and applicant status/date metadata. Data is inserted via `textContent`, not unsanitized HTML.
- When unauthenticated, it displays a login gate and no personal member information.
- Explicitly labels development-only status and gracefully reports database/API availability errors.
- It provides no approval, editing, payment or administrative operations.
- Added a link to this page from the existing `auth.html` account section, retaining its pre-existing auth logic.

A read-only browser check confirmed the new staging page loads, displays the original PACP logo, and gates the signed-out view without showing private data. **Authenticated end-to-end tests with test accounts have not occurred.**

## Release blockers

1. Dedicated synthetic test identities for anonymous, applicant A, applicant B, member, officer, approver and admin, with independently verified role assignment.
2. Cross-user and direct REST/API tests proving the effective combination of grants and RLS.
3. Review and tighter grants for all 17 public tables; special attention to non-SELECT privileges.
4. Review of all seven callable SECURITY DEFINER functions for privilege escalation and inadvertent data exposure.
5. Verified email redirect and recovery flows.
6. Live integration of admin, membership workflow, courses, CPD and certificates remains undone; design previews are not live applications.
7. Dedicated mobile and desktop accessibility test, followed by explicit approval before production.

**Do not announce live readiness, enable acceptance of real member data, run schema migrations, or widen access until these checks pass.**

Supabase reference: https://supabase.com/docs/guides/api/securing-your-api
Security advisor references:
- https://supabase.com/docs/guides/database/database-linter?lint=0008_rls_enabled_no_policy
- https://supabase.com/docs/guides/database/database-linter?lint=0029_authenticated_security_definer_function_executable
