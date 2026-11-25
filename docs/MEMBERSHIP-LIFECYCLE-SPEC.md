# PACP Membership Lifecycle — Workflow & Acceptance Specification

**Status:** implementation specification / pre-production review.  
**Applies to:** applicants, members, membership officers, authorized approvers, auditors.  
**Production status:** not deployed. No live member data should be entered into previews.

## 1. Design principles

1. The association's latest registered bylaws and formally approved resolutions are the authority for eligibility, membership classes, rights, fees, voting, nomination, renewal and termination.
2. The platform must not infer eligibility or legal rights from a display label. Store the statutory membership category separately from its Arabic/English public label.
3. Every decision is attributable to an authenticated staff identity, timestamped, reasoned and retained in an append-only event history.
4. Applicants can see their own application status and applicant-visible messages only. Internal deliberations and documents remain staff-restricted.
5. Membership number issuance occurs only after the authorized final approval decision, in a trusted server-side transaction.
6. Payment is not a condition in the software until the association formally confirms fee policy and the provider/payment workflow is contracted and tested.

## 2. Lifecycle state model

| State | Meaning | Permitted next states | Applicant visibility |
|---|---|---|---|
| draft | Applicant has not submitted | submitted, withdrawn | Draft |
| submitted | Application received | under_review, withdrawn | Received |
| under_review | Assigned officer is reviewing | needs_changes, approved, rejected | Under review |
| needs_changes | Applicant action required | submitted (resubmission) | Action required + curated note |
| approved | Final authorized approval recorded | — | Approved; membership record/card becomes eligible for issuance |
| rejected | Final decision recorded | — | Rejected + approved applicant-facing reason |
| withdrawn | Applicant withdrew | — | Withdrawn |

A rejected application is not silently reopened. Any appeal/reapplication process must be separately approved and configured under the bylaws.

## 3. Application data and document handling

- Identity and contact data, four-part Arabic and English names, date of birth and residence.
- Professional data: MOH practice-license response, academic level, specialty, graduation year, workplace and years of experience.
- Portrait image and only those supporting documents explicitly required by the current bylaws or approved application policy.
- Each uploaded object is private; store only object metadata in the relational record. Use file type/size allowlists, malware scanning where available, and short-lived authorized download links.
- National identity number is highly restricted. Column naming does not encrypt it; use a reviewed encryption design and never expose it in member-facing views.
- Do not accept clinical records, patient data, therapy notes or case details.

## 4. Review and decision workflow

1. Applicant verifies email/account and submits a validated application.
2. Server creates an application ID and an initial `submitted` event.
3. Membership officer claims/assigns the case; assignment is audited.
4. Officer checks required fields and documents against the currently approved criteria.
5. Officer may request specific corrections; only an applicant-visible note is sent to the applicant.
6. Applicant resubmits; the system records a new event and retains prior decision history.
7. Authorized approver records approve/reject with a reason and timestamp.
8. On approval, a single server transaction creates or links the member record, sets approved status, allocates the unique membership code and writes the status-history/audit events. If any step fails, the entire transaction rolls back.
9. Applicant receives a notification that does not include sensitive documents or national ID.

## 5. Membership number and digital card

- Format: `PACPXXXX` is a display format only; the actual sequence length and starting value require association approval.
- Allocate number only in the approval transaction using a database sequence or equivalent concurrency-safe allocator; never generate in browser JavaScript.
- Enforce a unique database constraint and retry safely on collision.
- Never reuse a number after suspension, expiry, resignation or revocation.
- Card is issued only after approval. It displays the minimum approved fields: name, membership code, category label, status and validity dates if applicable.
- QR contains an opaque, non-guessable verification token or URL; do not encode national ID, date of birth, email, phone, or internal database IDs.
- Public verification returns only the minimum fields authorized for public disclosure. Revocation/suspension/expiry must be reflected promptly.

## 6. Renewal, suspension and expiry

- Renewal is a separate request linked to the existing member record.
- Renewal decision, fee assessment and payment status are separate facts; a browser payment redirect is never proof of payment.
- Suspension and expiry require an authorized reason, effective date and status-history event.
- Reinstatement must be a new authorized transition, not deletion of historical status.
- The exact term, grace period, reminders, renewal fee and consequences of non-renewal remain configurable pending formal approval.

## 7. Roles and separation of duties

| Role | Minimum intended access |
|---|---|
| Applicant | Create and view own application; upload own required documents; see curated messages |
| Member | View own profile, membership, renewals, courses and certificates |
| Membership officer | Review applications/documents; request changes; prepare recommendations |
| Authorized approver | Record final membership decisions as delegated by the association |
| Finance officer | View fee/payment and reconciliation fields only where needed; no access to identity documents by default |
| Auditor | Read permitted audit/history records; no editing |
| System administrator | Technical administration; no automatic authority to decide membership |

The final role map and delegation must be approved by the association. Do not assume that a technical admin role grants statutory decision authority.

## 8. Notifications

Required event templates: submission receipt, review started (optional), changes requested, resubmission received, decision issued, renewal reminder, renewal decision, card available. Notifications should contain a secure sign-in link and minimal status text, not identity documents or sensitive data.

## 9. Minimum acceptance tests

- Applicant A cannot read or modify Applicant B's application, documents, membership or renewals.
- A member cannot access another member's profile/card/CPD history by changing an identifier.
- A public verifier cannot enumerate member numbers or retrieve private fields.
- A staff user without membership permissions cannot access membership documents.
- A reviewer cannot silently alter a final decision or erase prior events.
- Duplicate/parallel approvals cannot allocate duplicate membership codes or create duplicate member records.
- Rejected/withdrawn applications do not create active memberships or cards.
- A member status change immediately affects the verification result.
- File uploads reject disallowed types, oversize files and unauthorized object paths.
- Audit events record actor, action, target, time and decision reason without copying unnecessary sensitive payloads.
- No production payment or email is triggered from a preview environment.

## 10. Open governance decisions before implementation

1. Confirm the latest registered bylaws version/date and exact eligibility clauses.
2. Confirm legal membership category names and approved bilingual display labels.
3. Confirm who has delegated authority to recommend and who has authority to approve/reject.
4. Confirm whether membership approval is conditional on annual fee payment, and when payment is due.
5. Confirm membership term, renewal window, grace period, suspension and reinstatement rules.
6. Confirm required documents and whether MOH license is mandatory, optional or category-dependent.
7. Confirm retention period and process for rejected/withdrawn applications and identity documents.
8. Confirm the membership number sequence length, initial number and card validity model.

## 11. Technical implementation boundary

The accompanying SQL migration is a review draft adding application event history, private document metadata, membership status history and renewal requests. It deliberately contains no permissive client policies, no membership approval function, no sequence allocator and no payment integration. These must be designed, reviewed and tested separately before deployment.

**Release gate:** no migration execution, real personal-data collection, Cloudflare production change or merge to `main` is authorized by this specification.
