# PACP — Staging Acceptance Test Plan
Version: 1.0
Status: Review checklist; not evidence that tests have passed
Target: Cloudflare Pages preview deployments from `rebuild/platform-foundation`
Production safety: Do not merge to `main`, alter production DNS, or enable payments during these tests.

## 1. Test boundary
This checklist separates visual-preview review from functional acceptance. A rendered prototype is not proof of authentication, persistence, authorization, email delivery, payment processing, or certificate verification. Record each item as Pass, Fail, Blocked, or Not implemented, with the tested preview URL, date, device/browser, and evidence.

## 2. Visual and responsive checks
- [ ] Homepage loads on mobile without horizontal overflow.
- [ ] Arabic pages use correct RTL direction, alignment, punctuation, and keyboard order.
- [ ] English pages use LTR direction and correct layout.
- [ ] Language switch preserves the current page where possible and does not lose entered form data.
- [ ] Text contrast, focus indicators, labels, and touch targets are usable.
- [ ] Layout is usable at 320–390 px mobile widths, tablet width, and desktop.
- [ ] Official association logo and approved identity are used; no placeholder identity is presented as official.
- [ ] No invented statistics, sample people, fabricated approvals, or misleading live status indicators are shown.

## 3. Public website
- [ ] Navigation links work and have no dead ends.
- [ ] Contact details and registration number match approved source material.
- [ ] Content is editable through the agreed publishing workflow rather than requiring unsafe production edits.
- [ ] Privacy notice, terms, accessibility/contact route, and membership rules are available before collecting personal data.
- [ ] Public pages do not expose private member data, unpublished content, internal notes, or admin routes.

## 4. Membership application — functional acceptance
Do not collect real applicant data during preview testing. Use synthetic test records only.
- [ ] Required fields and field-level error messages are clear in Arabic and English.
- [ ] Full four-part name is supported in both scripts where applicable.
- [ ] Ministry of Health professional-practice question and academic/work-history fields follow approved wording.
- [ ] Uploads enforce permitted file types, size limits, and private access.
- [ ] Duplicate submissions are handled safely and applicants receive a reference number.
- [ ] Application status transitions are server-side and auditable.
- [ ] Applicant can view only their own application and permitted documents.
- [ ] Membership number in format PACPXXXX is issued only after final authorized approval; it cannot be chosen by the applicant or generated solely in browser code.
- [ ] Rejected or returned applications record the authorized decision and permitted explanation.
- [ ] National ID is minimized, protected at rest and in transit, excluded from URLs/logs, and not displayed in ordinary list views.

## 5. Member portal and digital card
- [ ] Sign-in and account recovery work using a verified, supported identity flow.
- [ ] Member sees only their own profile, applications, renewals, certificates, and card.
- [ ] Card is generated only for an approved, active membership.
- [ ] QR code resolves to a stable verification page and reveals only minimal public verification data.
- [ ] Invalid, revoked, expired, or fabricated identifiers do not verify as active.
- [ ] Print/PDF output is readable and includes Arabic/English fields as approved.
- [ ] Card preview/sample is clearly marked as a demo until real issuance is implemented.

## 6. Courses, CPD and certificates
- [ ] Course listing, dates, capacity, fees, language, and accessibility details are accurate.
- [ ] Registration prevents overbooking and handles duplicate registrations.
- [ ] Attendance is recorded only by authorized staff and changes are auditable.
- [ ] CPD points are calculated from approved course rules and cannot be edited by the participant.
- [ ] Certificate is issued only after approved attendance/completion conditions.
- [ ] Certificate verification page does not expose unnecessary participant data.
- [ ] Cancellation, refund, waitlist, and failed-registration states are defined before launch.

## 7. Administration and access control
- [ ] Admin routes require authenticated staff access.
- [ ] Authorization is enforced on the server/database, not only by hiding UI buttons.
- [ ] Membership reviewers cannot access unrelated finance settings unless explicitly authorized.
- [ ] Finance users cannot access private identity documents unless necessary and approved.
- [ ] Content editors cannot grant roles or change security settings.
- [ ] Role assignment is restricted to a trusted, audited process.
- [ ] High-impact actions require confirmation and create an audit event.
- [ ] Exports are role-scoped, logged, and minimize personal information.
- [ ] No shared default admin password or public demo credential exists.

## 8. Data protection and operations
- [ ] RLS/security policies are tested against anonymous, applicant, member, reviewer, admin, and finance roles.
- [ ] Database migration is reviewed and tested in a non-production project before execution.
- [ ] Secrets are stored only in protected environment variables; none are committed to Git.
- [ ] File storage is private by default and uses short-lived authorized access.
- [ ] Backups, restore procedure, retention schedule, deletion/correction requests, and incident response are documented.
- [ ] Logs exclude passwords, tokens, full national IDs, uploaded document contents, and payment secrets.
- [ ] No patient clinical records or clinical case data are collected by this association platform.

## 9. Payments — launch blocked until approved
- [ ] Association verifies legal entity, merchant eligibility, fees, settlement currency, refunds, chargebacks, and Palestine availability with the provider.
- [ ] Payment provider is selected and contract/account is approved by the association.
- [ ] Checkout and provider webhooks run server-side; webhook signatures and idempotency are verified.
- [ ] Browser return/redirect alone never marks an invoice as paid.
- [ ] Failed, pending, duplicate, refunded, and disputed transactions are reconciled.
- [ ] Test/sandbox transactions pass before any live payment.
- [ ] No live payment keys or real card data are used in previews.

## 10. Go-live gates
Production release requires all of the following:
1. Product owner signs off on content, membership rules, role matrix, and fee schedule.
2. Technical reviewer approves schema, migrations, RLS, storage, auth, and recovery procedures.
3. Functional and security checks pass in staging, with failures documented and resolved.
4. Payment provider is approved and tested, if payments are included in launch.
5. Association authorizes the exact release commit and rollback plan in writing.
6. Production deployment and post-deploy smoke test are completed by an authorized operator.

## Test report template
- Preview URL:
- Commit:
- Date / tester:
- Device / browser:
- Test case:
- Result: Pass / Fail / Blocked / Not implemented
- Evidence:
- Severity and remediation owner:
