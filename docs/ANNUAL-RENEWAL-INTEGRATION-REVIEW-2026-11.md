# PACP annual renewal integration review — 2026-11
**Status:** engineering review only; no production database migration, no activation, no payments.

## Findings confirmed by read-only inspection of PACP-Development
- `public.members` has `id uuid`, `user_id uuid`, and `status public.membership_status`.
- `public.membership_renewal_requests` ALREADY EXISTS, with `id uuid`, `member_id uuid`, `status text`, `fee_amount numeric`, `payment_status public.payment_status`.
- `public.payment_records` exists, with `status public.payment_status`.
- The existing `members.status` enum does not define `active` or `revoked`.
- The proposed annual `membership_periods_sandbox` is a test fixture, **not** a live table.
- The existing renewal-request table **must be preserved**, not independently recreated under a competing name.

## Correct integration architecture
1. A renewal request is a **workflow** (submitted, reviewed, approved/rejected); a membership period is the **entitlement** for one calendar year. These are distinct; approval of a request alone must not activate benefits.
2. Extend the existing `membership_renewal_requests` with a reviewed target-year link to an annual membership period, rather than introducing a second renewal workflow table. Check existing indexes and keys before designing changes.
3. Introduce a separate, unique `(member_id,membership_year)` annual periods relation after formal schema review. Carry effective year dates as UTC timestamps computed from Palestinian local calendar boundaries.
4. Reconcile existing approval-driven membership number generation before migration. Existing numbers must not be silently replaced or reused on annual renewal.
5. Only trusted staff/payment verification may authorize fee settlement or waiver. **Do not** infer settlement from client-supplied flags, request `approved`, or payment-record existence alone.
6. Card visibility must remain denied until a server-owned, current-year membership period is valid; the January late-renewal window must never extend an expired card automatically.
7. Implement a **member-scoped, read-only API** returning year, period end, non-sensitive payment/renewal status and a server-evaluated eligibility result. Never accept arbitrary member IDs from browser calls.
8. Use carefully reviewed grants/RLS; avoid privileged functions in the exposed `public` schema unless necessary, audited, and explicitly EXECUTE-restricted.
9. Keep `www.pacp.ps`, `main`, production DNS, member data and mail unchanged until approved.

## Pre-migration checklist
- Compare exact `membership_renewal_requests` columns, constraints, ownership, RLS policies and existing write RPCs.
- Test migration against a disposable database seeded with *synthetic* old-schema applications and renewals, including rollback.
- Exercise A/B access through actual Supabase Auth JWTs; current PostgreSQL role impersonation is not equivalent.
- Test reviewer-versus-approver roles and financial-signoff separation, including revocation and year boundary.
- Approve PACP bylaws-based annual validity, fee exemptions, late renewal, statutory standing and appeals.
- Re-run security advisors after schema and API changes, then stage UI integration and full UAT.

## Release gate
**BLOCKED:** Live activation/renewal/payment/official card QR must remain disabled until the above tests and approvals are complete.
