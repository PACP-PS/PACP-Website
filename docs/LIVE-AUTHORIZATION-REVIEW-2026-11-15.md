# PACP — live database authorization audit 2026-11-15

Environment: PACP-Development only. This is NOT certification for launch.

## Observed read-only findings
- Under authenticated database role **without a user JWT**, `has_staff_role('membership_officer')`, `has_staff_role('membership_approver')`, and `can_review_membership()` returned `false`.
- `my_membership_summary()` raised `28000 Authentication required` with no user identity.
- Function source confirms `has_staff_role` checks the authenticated user identity and non-revoked rows in `public.staff_role_assignments`.
- `membership_review_queue` checks both `auth.uid()` and reviewer role before returning limited application metadata.
- `process_membership_application` checks role before state-changing actions, but it currently looks up the requested application *before* action-specific authorization. For a nonstaff caller, this can distinguish nonexistent application IDs from existing ones via error behavior. Reorder authorization before row lookup as a defense-in-depth improvement.
- No actual staff or test applicant JWT was used, and no membership records were changed.

## Required security refinements before enabling RPC
1. Reject unsupported `p_action` and check authorization **before** fetching application rows.
2. Make `SECURITY DEFINER` functions use `SET search_path = ''` and schema-qualify all references if dependencies permit; preserve trusted helper calls.
3. Ensure private submission documents and portraits use separate storage policies.
4. Restrict direct write table grants (proposed in `security/development-grants-proposal.sql`) after dependency review.
5. Test two synthetic applicant JWTs plus reviewer and approver JWTs; verify direct REST cross-user reads/writes.
6. Validate that the applicant's authenticated email is verified and consistent with submission data. Obtain consent to collect personal records.
7. Confirm procedural and statutory approval requirements before issuing membership code and certificates.

## Safe read-only probe
```sql
begin;
set local role authenticated;
select public.has_staff_role('membership_officer') as officer,
       public.has_staff_role('membership_approver') as approver,
       public.can_review_membership() as can_review;
rollback;
```

Expected: three `false` values **only when no JWT identity is present**.
Never treat this as equivalent to a multi-user RLS test.

## Release gate
Status: **BLOCKED**. No production deployment, no real applications and no official card issuance.
