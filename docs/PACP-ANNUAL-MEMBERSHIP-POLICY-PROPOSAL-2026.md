# PACP — Proposed Annual Membership Policy / السياسة المقترحة للعضوية السنوية
**Version:** draft 1.0 — 2026-11-16. **Status:** proposed for Board/legal/bylaws review; NOT adopted or effective.

## الأساس المرجعي
- قانون الجمعيات الفلسطيني رقم (1) لسنة 2000، المادة 5 بشأن شروط وأنواع العضوية والاشتراكات وأسباب انتهائها، والمادة 23 بشأن الجمعية العمومية والأعضاء الموفين بالتزاماتهم: https://mjr.ogb.gov.ps/MergedLegislations/ViewText/61/
- اللائحة التنفيذية الصادرة بقرار مجلس الوزراء رقم (9) لسنة 2003: https://mjr.ogb.gov.ps/Decrees/ViewText/26488/
- Canadian Psychological Association membership renewal: https://cpa.ca/membership/renewal/
- CPA categories: https://cpa.ca/membership/becomeamemberofcpa/membershiptypes/

This policy adapts general professional-association practices; it is **not** a claim that foreign associations impose these exact grace periods, categories, or fees. PACP's actual registered bylaws have not been provided or reviewed here. In case of conflict, the registered bylaws and Palestinian law control.

## المادة 1 — السنة المالية للعضوية
1. العضوية السنوية من الساعة 00:00 يوم 1 يناير حتى الساعة 23:59:59 يوم 31 ديسمبر من السنة نفسها، بحسب منطقة `Asia/Hebron` (Palestinian local time), with authoritative timestamps stored in UTC.
2. A new applicant approved during the year receives a validity period ending December 31 of that year only *after* separate activation. Fee proration for new applicants requires a Board-approved tariff; no assumed prorating in checkout.
3. Renewal opens December 1 for the following membership year. One paid annual period does not extend beyond its defined year.
4. Renewals paid in advance extend the next annual membership year; do not shorten an existing valid period.

## المادة 2 — الفئات والأهلية
1. `full` / **عضو عامل**: academic and practice eligibility defined by PACP's registered bylaws, with credentials assessed by authorized reviewers. Voting/nomination only if authorized by bylaws and law.
2. `associate` / **عضو منتسب**: psychology-related professionals not satisfying full statutory requirements, subject to approved category description. No implied independent practice rights.
3. `honorary` / **عضو شرف**: exceptional contribution by formally documented competent body decision; dues policy and voting rights require explicit bylaws approval.
4. `student` / **عضو طالب**: OPTIONAL only if PACP bylaws permit, for verified students, without implied clinical licensure or professional membership.
No automatic mapping of proposed UI labels to legal types. Professional practice licence is separately verified where applicable; PACP membership is not a regulatory licence.

## المادة 3 — الطلب والموافقة والتفعيل
- Application received `submitted` -> `under_review` -> `approved_pending_activation` (or `needs_changes` / `rejected`).
- Formal approver decision, identity/qualification checks and accepted Code of Ethics & privacy terms required.
- A separate trusted server-side activation requires proof of settled dues or a documented authorized exemption, as applicable; only then `active`.
- A permanent membership number is assigned once on first activation. Membership year and card issue version are separate from that permanent number.
- The current database generates a PACPxxxx number at approval; that implementation MUST be reconciled before launch. Design specification favors `PACP-YYYY-NNNN` at first activation. Never renumber an already issued identifier casually.

## المادة 4 — التجديد السنوي
- December 1: next-year renewal is available.
- Automated reminders: 60, 30 and 7 days before December 31, then 1 and 15 days after expiration (subject to lawful communications settings).
- Member verifies professional details, updates contact information, reaffirms ethical obligations, updates required licensing evidence when applicable, and pays annual dues or presents documented exemption.
- Routine renewal should not require full reapplication unless a materially changed eligibility or disciplinary/ethical restriction warrants formal review.
- January 1–31 is a **30/31-day administrative late-renewal window**, not extension of membership validity. Effective rights and QR credential expire at the end of December 31 until renewal activates. No fine unless separately authorized by Board and bylaws.
- After Jan 31 a lapsed member can request `reinstatement` through a defined review, preserving historic membership number if allowed, rather than silently creating a new full member.
- No automatic charges or recurring-payment mandates without specific consent, provider contracts and legal/financial review.

## المادة 5 — حالة العضو وحقوقه
- `approved_pending_activation`: accepted but not activated; no valid credential or member-only rights.
- `active`: activated for the current year, not suspended or revoked, before the effective `valid_until`.
- `expired`: annual end elapsed without effective next-year renewal; no valid QR/card or voting eligibility pending policy-based restoration.
- `suspended`: restrictions decided by authorized committee under documented grounds, notice, right to respond/appeal, start/end and reason; card invalid immediately.
- `revoked` or `terminated`: formal resolution, documented notice and appeal route; card revoked and number not reused.
- `rejected` refers to the application, not a formerly active membership; maintain separate application state from membership state.
- Do NOT assert suspension/expiration automatically terminates statutory association membership. Legal status and ability to exercise rights depend on registered bylaws and due process. System must distinguish `annual_benefit_eligibility` from legal membership termination.

## المادة 6 — الرسوم والإعفاءات
- Fee schedule by category and year in ILS is set by competent body, published before renewal opens; values remain TBD.
- Member can see fee, exemption basis, receipt and payment status. No service role credentials on client and no live collection prior to provider verification.
- Consider hardship accommodations and reduced fees for student/retired members ONLY if adopted by authorized body; no unapproved discrimination.
- Cancellation, refund and non-refundable exclusions must be approved in writing and comply with applicable law. No claim PACP automatically adopts the Canadian no-refund policy.

## المادة 7 — البطاقة والتحقق والخصوصية
- Credential issuance only on server after eligibility `active` AND date validity AND no suspension/revocation AND a verified settled fee/exemption.
- Current card prototype is DEMO, never a valid official credential.
- QR contains high-entropy opaque verification token / signed URL; not national ID, phone, email or member primary key. Token can be rotated/revoked. Rate-limit public verification.
- Public verification reveals only approved minimum fields (e.g. name, member number, membership category, effective validity). No documents, birthdate, national ID, address, professional licence number, or private photo by default.
- Membership ID persists; card number/version and token rotate per renewal if implemented.
- Store payment and status changes in append-only auditable history, roles held in trusted staff tables (never user_metadata).

## Implementation decision: NON-OPERATIONAL UNTIL APPROVED
Existing Supabase enum lacks `active` and `revoked`, and public.members lacks `activated_at`/`valid_until`. Existing approval generates member numbers at approval. These are release blockers.

Proposed technical fields:
`members.activated_at` (timestamptz), `members.valid_until` (timestamptz), `members.suspended_at`, `members.revoked_at`, `members.reinstated_at` (optional), plus server-owned annual `membership_periods` with year, payment/exemption evidence, activation and expiry. Prefer period rows to overwrite-only validity.
Legal/statutory membership standing separate from annual validity; controlled states and check constraints only after legal review.
Server function `my_card_eligibility()` returns strict boolean and limited reasons; authoritative verification always evaluates state/current time and revocation.
Use a disposable Supabase test environment, synthetic distinct JWTs and approval/renewal/expiration/revocation cases, then review migration and UAT before applying.

## Approval checklist
- Confirm PACP registered bylaws and exact legal categories/rights, membership termination process and appeals.
- Ratify calendar-year cycle, late-renewal window, effective cutoff and first-year joining policy.
- Approve fee amounts, discount/waiver authority and refunds.
- Ratify activation criterion and whether code assigned on activation or earlier.
- Confirm legal treatment of expired annual dues versus statutory membership and voting.
- Security review and tests required before production.
