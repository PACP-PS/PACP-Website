# PACP database grants audit and hardening proposal — 2026-11-15

**Scope:** Development database only; read-only live inspection completed; no SQL mutation performed.  
**Proposed patch:** `security/development-grants-proposal.sql` (manual review required).

## Verified live state
- All 17 public tables have RLS enabled, with 14 policies observed.
- Both `anon` and `authenticated` currently have broad table-level privileges on many public tables, including TRUNCATE, TRIGGER, REFERENCES, and UPDATE/DELETE.
- 7 SECURITY DEFINER functions are executable by `authenticated`, **none** by `anon` in observed results.
- Each inspected privileged function specifies a `search_path`. `pacp_report_members` has `search_path=""`; source inspection must verify fully qualified object identifiers.
- Existing RLS policies permit application submission by its own applicant; no direct update/delete policy observed.
- A table with RLS and no policy is denied for row operations under the ordinary client role. Keep audit/payment/staff assignments private.

## Proposed changes
Revoke unneeded browser table write/DDL-like grants while preserving existing policy-allowed reads and applicant INSERT. Never introduce new access merely to resolve an API error. This is a proposal, not a claim that the SQL has run.

## Before applying to development
1. Take a verified development backup and identify rollback owner.
2. Inspect **all** invoker dependencies of views, triggers and RPCs that may rely on caller privileges.
3. Create synthetic applicant A/B, reviewer, approved member and admin.
4. Confirm direct REST access matrix and documented expected results.
5. Check security-definer source and explicit auth gating function by function.
6. Review and approve the grant proposal; only then apply in development in a controlled session.
7. Run two-sided positive/negative regression tests, advisors and rollback rehearsal.

## Required regression tests
- Anonymous may read published activities but not private member/application data.
- Applicant A cannot read or mutate applicant B application, profile, document or registration.
- An applicant cannot set staff roles, assign self a membership ID or change approval status.
- Only designated staff can view review queue and execute valid state transitions.
- Staff-role revocation takes effect without trusting editable user metadata.
- A privileged function cannot leak any internal notes, ID documents or other members' records.
- Direct REST calls for DELETE/UPDATE/INSERT outside documented RLS must fail.
- Recovery and password redirects remain bound to allowlisted staging routes.
- Courses, CPD, certificates and fees remain disabled until backend and governance tests pass.

## Release verdict
**NOT READY.** Source and backend audit provide evidence for review only. Do not accept live submissions, approve real members or switch the official domain.
