# PACP — Database security advisor findings and release decision

Date: 2026-11-15. Scope: Supabase project **PACP-Development** only.

## Observed live security advisor output
- **7 WARN**: signed-in users can call seven SECURITY DEFINER functions in public:
  `can_review_membership`, `has_staff_role`, `membership_review_queue`,
  `my_membership_applications`, `my_membership_summary`,
  `pacp_report_members`, `process_membership_application`.
  This is a warning requiring review, **not proof of exploitation**.
- **5 INFO**: RLS enabled with no policies on `activity_accreditations`,
  `audit_log`, `contact_inquiries`, `payment_records`,
  `staff_role_assignments`. Deny-all for exposed clients may be intentional.
- **Read-only verification**: 17/17 public tables have RLS; submission RPC missing;
  the deployed approval RPC still lacks the action/authorization guard before row lookup.
- Public application insert grants/policies must be reconciled with the future submission RPC;
  otherwise direct insertion can circumvent the RPC email-check/duplicate-request constraints.
- Avoid blanket `REVOKE` on the seven RPCs; some are intended authenticated APIs.
  Review each RPC's authorization, safe search_path, least privilege, dependencies,
  and surface area before making grant decisions.

## Corrective order — do not skip
1. Set up isolated Supabase test environment with synthetic identities and no production data.
2. Snapshot relevant function definitions and grants; check current schemas, constraints,
   storage policies, schema exposure, expected clients and rollback.
3. Correct `process_membership_application` to authorize prior to row lookup.
4. Restrict direct application insert after installing and securing validated submission RPC;
   ensure verified email/consent, uniqueness (including concurrent calls), and role-based workflow.
5. Run live synthetic JWT tests for unprivileged member, reviewer, approver, anon and
   cross-account ownership. Exercise both valid transitions and denied transitions.
6. Re-run Supabase Security Advisor; record before/after notices and manual decision.
7. Complete private documents, card verification, actual CPD/course/certificate integration,
   privacy/retention, backup restore and authorized governance sign-off.
8. Leave `security/release-evidence.json` blocked until independent evidence is available.

### References
- https://supabase.com/docs/guides/database/database-linter?lint=0029_authenticated_security_definer_function_executable
- https://supabase.com/docs/guides/database/database-linter?lint=0008_rls_enabled_no_policy
- https://supabase.com/docs/guides/database/postgres/row-level-security

**Verdict:** development environment is not certified for production. No database
changes were made in this review.
