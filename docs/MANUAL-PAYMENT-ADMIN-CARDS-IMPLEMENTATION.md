# PACP — Manual Payment, Membership Issuance and Admin Accounts
Status: implementation contract, **not a deployed backend**.

## Offline payment methods
- `cash`: staff cashier accepts cash and enters a unique official receipt number; finance reconciles with the daily cashier report.
- `bank_transfer`: applicant receives PACP's *verified official bank account details*. Never hard-code unverified account numbers. Applicant may quote a bank transaction reference; this is **evidence only**, not confirmation.
- Status: pending -> under_review -> paid or failed; waiver requires authorized, documented decision. Only staff with verified finance entitlement may mark funds received, with reference, method, date, and audit event.
- Recording payment evidence and confirming money received are separate authorities. Preserve the member's original unique ID and signed history.

## Secure staff account creation through website
1. Applicant can create an ordinary Supabase Auth user account.
2. Existing, authenticated *superadmin* initiates a staff invitation for an email; invite remains pending until verified ownership of the email and explicit acceptance.
3. The invite endpoint must verify superadmin authorization from the database using the authenticated identity, not `user_metadata` or user-controlled request fields. It must never accept a caller-supplied role for self-assignment.
4. First superadmin is bootstrapped **out of band** by an authorized operator with 2FA, audit trail and signed authorization; public signup cannot create any administrative privileges.
5. Grant/revoke role actions use an audited server-only transaction; two-person approval for superadmin grant and finance approval is recommended. A user's JWT may remain stale: sensitive operations re-check DB permissions.
6. Roles: `superadmin`, `membership_reviewer`, `membership_approver`, `finance`, `courses_editor`, `content_editor`, `read_only_auditor`. Define least-privilege matrix before enabling.

## Activation and digital card
- Initial application / renewal request approved by designated authority AND payment independently reconciled or signed waiver AND non-suspended standing AND valid annual entitlement.
- Activation in one idempotent transaction; store approver, financial verifier, effective dates, source requests, audit event. No browser-set `active` state.
- Official cards have stable member code and annual validity. Public QR points to a minimal verification URL with opaque rotating/revocable token, never national ID/phone/payment details.
- Card expires automatically at the calendar-year boundary, and immediately upon suspension/revocation. QR verification should be server-side and rate-limited.

## Existing schema compatibility
- Existing `public.members` and `public.membership_renewal_requests` must be reused.
- Existing `public.payment_records` tracks course registrations (`registration_id`), so do **not** repurpose it as a membership payment table without a new audited relationship/schema review.
- Existing `members.status` enum does not contain `active`; annual entitlement lives in a separate table.
- `membership_renewal_requests.payment_status` is not sufficient proof of a bank deposit absent finance reconciliation.

## Production enablement gates
- Verify association's official IBAN/bank name/account holder and exact membership fee/category decisions.
- Dedicated staging Supabase project, real test Auth users, authenticated A/B RLS and superadmin/finance negatives, approved SQL migration plus rollback, email delivery, no secrets client-side.
- Test cash receipt duplication, bank reference duplicate, refunds, concurrent approval, renewal, expiry and revocation; backup and audit.
- Only then switch public build to include protected member routes and staff panel; feature flag sensitive actions pending independent verification.

Until those gates pass, display payment methods as guidance and **do not claim online settlement or valid official cards**.
