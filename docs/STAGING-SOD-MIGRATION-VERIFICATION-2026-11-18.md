# Staging membership-approval / finance separation — 2026-11-18

## Implemented (PACP-Staging only)
Migration `enforce_membership_finance_separation_staging` successfully applied to Supabase project `aweebuukeovcekctclws`.

- `public.pacp_record_cash`: denies a finance verification if the same user already reviewed that application.
- `public.pacp_review_application`: denies approval/rejection if the same user previously verified its cash receipt.
- Existing `public.pacp_issue_card` additionally requires that approved application's reviewer and cashier verifier are different.
- Authorization role checks, validations, SECURITY DEFINER and search_path preserved.
- Post-change SQL inspection confirmed both function bodies include the separation guard.
- No synthetic or real payment was posted, no application was approved by this session.

## Limitations / release blockers
- No session-authenticated negative tests were executed; separate test credentials were not available in a secure runner.
- These guards apply to the two public RPC paths, not necessarily privileged direct SQL modifications by operators. For absolute row-level enforcement, review triggers/permissions and operator procedures as a subsequent hardening stage.
- Staging role assignments currently include the admin with overlapping privileges. This does not bypass same-actor rule for these RPCs.
- Security advisor still flags signed-in callable SECURITY DEFINER functions. Authorization checks must be independently tested.
- Production schema was not modified. Promotion requires reviewed migration, UAT, rollback and explicit authorization.

## Recommended test cases
1. Admin approves synthetic application, admin attempts to record cash: expect SQLSTATE 42501, no receipt.
2. Finance-only user records receipt for another synthetic application, same user tries approval (if temporarily assigned approver for negative test): expect SQLSTATE 42501.
3. Admin reviews application and separate finance user verifies receipt: expect success for respective steps.
4. Unauthorized member invoking either function: expect SQLSTATE 42501.
5. Verify card issuance remains impossible without separate reviewer/cash verifier.
