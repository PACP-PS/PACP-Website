# PACP Membership — Design Review and Implementation Decisions

## 1. Purpose and current status
This document reviews the membership information architecture and the non-submitting application-form prototype. It is a product-design and implementation reference, not a legal opinion. The prototype is not connected to a database, email service, identity verification, document storage, or payment provider.

## 2. Membership categories: legal label vs public display label
Keep two separate fields in the database and administration interface:
- `statutory_category`: the exact category stated in the currently verified registered bylaws.
- `display_label_ar` / `display_label_en`: the member-friendly label approved by the association.

Proposed public labels for discussion:
| Exact bylaw category | Proposed Arabic display label | Proposed English display label |
|---|---|---|
| العضو العامل | العضو الأساسي | Full Member |
| العضو المؤازر | العضو المساند | Supporting Member |
| عضو الشرف | العضو الفخري | Honorary Member |

Do not replace the statutory category in legal records, minutes, official notices, receipts, or exports. Labels remain configurable until formally approved.

## 3. Rules supported by the supplied bylaw copy
The supplied 12-page document indicates:
- Membership is personal and is not transferable by representation or inheritance (Article 7).
- Article 8 describes eligibility for a legally competent natural or legal person subject to the statutory conditions.
- Article 9 lists application data: full four-part name, address, date of birth, profession, identity number and nationality, plus an undertaking to comply with the bylaws and Board decisions.
- The Board decides acceptance or rejection; an applicant may object to rejection at the next General Assembly meeting.
- Article 10 states minimum age 18 and a specified conviction exclusion.
- Article 11 states a 100 NIS membership fee, with the amount set by the Board subject to General Assembly approval.
- Member rights described in the supplied text include personal participation and voting at General Assembly meetings, and election to / standing for the Board. Do not assume these rights apply identically to all three categories; category-specific rights require confirmation.
- Article 12 requires due process for specified termination grounds, including written warning, reasonable opportunity to correct, and opportunity to present a defence.
- Article 13 describes formal written/personal or registered-mail notices. Digital notices should be supplementary until formally approved as legally sufficient.

**Important:** The supplied bylaw copy does not explicitly impose a clinical psychology degree or professional licence as a universal eligibility requirement. Do not add this as an automatic rejection rule without an approved legal basis.

## 4. Proposed application workflow
1. Applicant selects a statutory category (with public-facing label shown).
2. Applicant reviews eligibility information and privacy notice.
3. Applicant submits minimum required personal data and any approved supporting documents.
4. System issues a reference number and records timestamp.
5. Membership officer checks completeness; may request missing information.
6. Authorized Board decision-maker records accept / reject / return-for-information, decision date, rationale and supporting minute/reference.
7. If approved, finance officer records dues assessment and payment status.
8. Membership activates only after all required approvals and financial conditions are met.
9. System issues a member number and digital membership card with a verifiable identifier.
10. Member can access account, renewal status, receipts and approved member services.

No automated acceptance, rejection, suspension or expulsion based solely on a payment flag.

## 5. Suggested status model
`draft` → `submitted` → `under_review` → `information_requested` → `approved_pending_dues` → `payment_pending` → `active`

Alternative terminal / exception statuses: `rejected`, `withdrawn`, `expired`, `renewal_pending`, `suspended_pending_due_process`.

Every status change must record actor, timestamp, reason, and associated decision/document. Restrict sensitive reason details to authorized roles.

## 6. Operational roles (proposed; Board approval required)
- Applicant: submit and track own application.
- Membership officer / Secretary: completeness review and member-register administration.
- Board approver: record the decision within the Board's statutory authority.
- Treasurer / finance officer: assess and reconcile dues; cannot independently approve membership unless authorized.
- System administrator: technical administration only; no automatic right to read confidential membership documents.
- Auditor: read-only access to defined audit and financial records.

These are platform permissions, not new statutory offices.

## 7. Privacy and security requirements
- Collect only fields required by the verified legal process.
- Identity numbers and supporting documents must be encrypted in transit and at rest, stored privately, and visible only to authorized roles.
- Never place identity numbers, documents, or membership decisions in public URLs, analytics, logs, or public directory records.
- Public directory is opt-in and limited to fields the member has approved.
- Define retention, correction, access, deletion and breach-response procedures before launch.
- Provide a clear privacy notice and consent record at submission.
- Do not collect patient records or clinical case information.

## 8. Items requiring formal confirmation before production
1. Confirm that the supplied bylaw copy is the latest registered and amended version.
2. Confirm the current approved membership fee and effective date. The user's instruction is 100 NIS; the product setting should remain inactive until the approval record is documented.
3. Confirm eligibility for each category and whether professional qualifications are required.
4. Confirm category-specific voting, election, nomination, service and renewal rights.
5. Confirm whether legal persons may be members in practice and how an authorized representative is recorded.
6. Confirm the authorized body and delegation rules for decisions, appeals and notices.
7. Confirm whether digital notices and electronic signatures are accepted for formal statutory purposes.
8. Approve the exact public Arabic and English labels.
9. Approve the fields, documents, retention periods and privacy notice.
10. Approve card format, membership number format, renewal cycle and fee receipt workflow.

## 9. Prototype acceptance review
- The current application page is a visual interaction prototype only.
- It must display a persistent notice that it does not submit or save information.
- File upload remains disabled.
- No payment fields or live checkout are shown.
- Before production, add server-side validation, abuse protection, secure authentication, private document storage, audit trail, email receipts and role-based access checks.
- Test Arabic/English labels, RTL/LTR layout, keyboard navigation, mobile display and screen-reader labels.
