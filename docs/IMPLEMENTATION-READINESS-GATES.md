# PACP implementation readiness gates

This document separates design completion from production readiness. Passing a gate requires evidence, not a visual mockup.

## Gate 0 — Governance and product decisions
- [ ] Verify the latest approved bylaws and any applicable membership regulations.
- [ ] Approve Arabic/English labels for membership classes and eligibility criteria.
- [ ] Approve who can review, request changes, approve/reject, suspend, renew, and revoke membership.
- [ ] Approve annual fee (currently planned at ILS 100), exemptions, renewals, refunds, and accounting treatment.
- [ ] Approve privacy notice, retention/deletion schedule, member consent, and directory opt-in.
- [ ] Approve CPD credit rules, evidence requirements, appeal/reversal rules, and authorized approvers.

## Gate 1 — Deployment and technical environment
- [ ] Confirm Cloudflare Pages project and whether Pages Functions/Workers are available.
- [ ] Confirm staging hostname, production hostname, DNS/TLS, build command, output directory, and rollback procedure.
- [ ] Confirm database/auth/storage provider and regional/data-protection requirements.
- [ ] Create separate development/staging/production environments and credentials.
- [ ] Store secrets only in environment settings; never commit them.
- [ ] Confirm automated preview builds and required checks.

## Gate 2 — Database and security
- [ ] Convert schema draft into ordered, reviewed migrations.
- [ ] Enable RLS on every table exposed through the database API.
- [ ] Add explicit least-privilege policies for member, officer, finance, accreditation, auditor, and administrator roles.
- [ ] Ensure role assignment cannot be self-escalated by a member.
- [ ] Ensure national IDs, portraits, and supporting documents use private storage and authorized access.
- [ ] Add server-side validation, rate limiting, anti-automation, audit events, and idempotency for sensitive actions.
- [ ] Test cross-member access denial and role-boundary denial.
- [ ] Test backup and restore.

## Gate 3 — Membership workflow
- [ ] Submit application without generating an active membership code.
- [ ] Review and request missing information.
- [ ] Record decision, decision-maker, timestamp, and reason.
- [ ] Generate unique PACP membership code server-side only after final approval; enforce uniqueness in the database.
- [ ] Apply the approved ILS 100 fee rule, exceptions, and payment state only after policy approval.
- [ ] Issue a card only for an approved/active member.
- [ ] Test suspension, expiration, renewal, revocation, and reissue.
- [ ] Public verification reveals only approved minimal fields; no national ID, birth date, address, contact details, or document URLs.

## Gate 4 — Courses, CPD, and certificates
- [ ] Publish only approved activities.
- [ ] Validate registration limits, waitlists, cancellation, attendance, and completion.
- [ ] Record proposed versus verified CPD points separately.
- [ ] Grant points only through an authorized, auditable operation.
- [ ] Issue certificates only when approved completion conditions are met.
- [ ] Support certificate verification and revocation.

## Gate 5 — Payments (currently on hold)
- [ ] Verify local and international providers' legal availability for the association and settlement to its bank/account.
- [ ] Review fees, currencies, settlement time, refunds, chargebacks, support, and contractual terms.
- [ ] Confirm hosted checkout and signed server-side webhook support.
- [ ] Test in provider sandbox, including duplicate callbacks and failed/late payments.
- [ ] Reconcile provider transactions with bank settlement.
- [ ] Never store card PAN/CVV; never treat a browser return page as proof of payment.
- [ ] Obtain written approval before enabling production payments.

## Gate 6 — Launch approval
- [ ] Test responsive layout, keyboard navigation, contrast, screen readers, Arabic RTL and English LTR.
- [ ] Test email delivery, error states, and all form validation.
- [ ] Run dependency/security checks and manual authorization tests.
- [ ] Confirm legal copy, contact information, policies, and content ownership.
- [ ] Obtain association acceptance and sign-off.
- [ ] Merge reviewed pull request and deploy to staging first.
- [ ] Validate production deployment and rollback plan before switching the domain.

## Current known state
Design previews and draft specifications exist on `rebuild/platform-foundation`. The draft SQL explicitly still requires reviewed row-level security policies. The member portal, live authentication, transactional email, official card issuance, and payment integration are not operational. Production deployment configuration has not been verified or changed by this work.
