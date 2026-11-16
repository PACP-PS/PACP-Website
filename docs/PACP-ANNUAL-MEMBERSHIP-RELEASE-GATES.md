# PACP Annual Membership — Technical release gate (2026-11-17)
**Current disposition: HOLD / NOT RELEASED.** This is a developer-to-Board handoff, not a production launch approval.

## Implemented and versioned on branch `rebuild/platform-foundation`
1. Draft annual policy (calendar year Jan 1 to Dec 31, late renewal window, fixed member ID).
2. Separate annual period model and negative SQL constraint tests in isolated GitHub Actions PostgreSQL.
3. Existing renewal request table compatibility review and review-only SQL `docs/annual-membership-integration.review.sql`: periods plus nullable target year, no historical rewriting.
4. Synthetic role/JWT claim tests for own-period visibility, read-only eligibility and renewal summary in disposable SQL.
5. Staging dashboard read-only; renewal/payment buttons disabled and demo cards non-valid.

## Live PACP-Development findings (read-only)
- `membership_renewal_requests` already exists: do NOT recreate. Its status constrained to submitted/under_review/needs_changes/approved/rejected/withdrawn. `member_id` references `members(id)`; `reviewer_id` references `auth.users`; fee and payment status present.
- RLS: `members_select_self` selects records for `auth.uid()`. Renewal requests have *staff-only* SELECT policy using `can_review_membership()`. No member self-SELECT. `payment_records` has no RLS SELECT policies.
- Original live `members.status` enum lacks `active`. Current data model does NOT have a live authoritative year/activation/expiry contract. Do NOT infer validity from `approved`.
- Historically 0 Auth users / 0 membership applications / 0 staff role assignments on development. Re-check inventory before UAT.

## Minimum backend release implementation — needs implementation/approval
- Board/legal approval of membership categories, calendar cutoffs, renewal rights, dues, waivers, appeals, and payment settlement authority.
- Stage and review annual periods DB migration against full actual schema and historical data. Add controlled backfill only with reviewed archival evidence; retain the existing application and renewal tables.
- Implement trusted transaction for activation and renewal: verify approved workflow; verify payment or waiver independently; enforce unique annual period, immutable annual history, role separation and idempotency.
- Design member-only read API: choose policy-safe RLS + SECURITY INVOKER or a separately audited scoped definer with restricted grants; never expose direct `members` bulk read or financial data.
- Link existing `membership_renewal_requests` to annual period by member/year; prevent multiple simultaneous open renewal requests for the same year according to approved rules.
- Implement authoritative current-time membership eligibility, not client state; QR token issue, rotation and revocation, minimal public verification, rate limits and audit events.
- Integrate private payment provider after merchant onboarding, reconciliation, errors/refunds and receipt audits. No auto-activation from front-end receipts.
- Create two independent synthetic Supabase Auth members plus reviewer/approver/finance test roles in a **separate isolated Supabase staging project**; verify positive and negative access via actual JWT requests including stale tokens, row ID tampering, privilege escalation, revocation, suspension and race conditions.
- Run security advisors, CI and end-to-end UAT; require explicit change approval, rollback script and backed-up schema before any deployment.

## Staging protocol
- Branch: `rebuild/platform-foundation`; production `main`, DNS, Cloudflare Pages publication and email records unchanged.
- SQL in `docs/*.review.sql` is intentionally outside migration runner. It must be copied into a reviewed migration only after stage QA.
- Deploy gate remains **closed** until: bylaws signoff; real Auth isolation; secure activation/renewal; payment reconciliation; authoritative QR/revocation; security review; authorized release.

## Common confusion to avoid
- Passing GitHub Actions SQL simulation != passing genuine Supabase Auth end-to-end.
- `approved` != `active`, and late renewal administrative grace != credential validity.
- Association membership != statutory practice licence.
- The web card mockup and public QR demonstration never constitute valid credentials.
