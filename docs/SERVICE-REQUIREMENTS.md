# PACP — Service Requirements & Workflow Register

## 1. Membership application

**Actors:** Applicant, membership officer, board/authorized approver, finance officer (where dues apply).  
**Flow:** Draft/application → submit → acknowledgement/reference number → completeness review → request for information (if needed) → eligibility/board decision → dues invoice (if applicable) → verified payment → activate membership → issue digital card.  
**Statuses:** draft, submitted, under_review, information_requested, approved_pending_dues, payment_pending, active, rejected, withdrawn, expired, renewal_pending.  
**Controls:** restricted identity/document access; decision history; no automatic approval; configurable membership classes and criteria sourced from approved bylaws.

## 2. Member account and directory

- Email/phone verification and secure account recovery.
- Member can update allowed profile fields and request corrections.
- Member controls whether their professional profile appears publicly.
- Public directory only exposes fields explicitly approved by the member and association policy.
- Member can view membership status, renewal date, receipts, certificates, and their own registrations.

## 3. Training / CPD registration

**Flow:** Published course → registration → capacity check / waitlist → fee assessment → hosted checkout or approved manual payment → server-verified payment → confirmed seat → attendance → evaluation → certificate.  
**Rules:** configurable cancellation/refund deadlines, attendance threshold, prerequisites, maximum capacity, waitlist promotion, and certificate revocation.  
**Payment:** local and international providers behind separate adapters; no activation until provider and merchant onboarding are approved.

## 4. Events and conference abstracts

- Event creation with public description, schedule, venue/online access, fee, capacity, and deadlines.
- Participant registration and confirmation.
- Abstract submission with file constraints, author declarations, and submission receipt.
- Restricted reviewer assignment, conflict declaration, scoring, decision and revision workflow.
- Do not publish reviewer identities or submissions to unauthorized users.

## 5. Certificates

- Unique, non-guessable verification identifier.
- PDF certificate with participant, event/course, date, issuing body, and authorized signatory.
- Public verification page exposes only minimum necessary validity information.
- Admin can revoke/reissue with reason and audit record.

## 6. Research and professional opportunities

- Admin-published calls, opportunities, resources, and announcements.
- Optional submission form with restricted access and defined retention.
- Clear statement that listing an opportunity does not constitute endorsement or accreditation.

## 7. Supervision / professional consultation requests

- Intake fields: requester, professional role, topic category, preferred format, availability, and consent.
- Route to authorized coordinator; track status and assignment.
- Clearly state this is an administrative/professional request channel, not therapy, clinical advice, or crisis response.
- Avoid collecting patient-identifying information or clinical records.

## 8. Volunteering and committees

- Expression of interest, skills/experience, committee preference, availability, and consent.
- Coordinator review and decision.
- Access limited to assigned coordinators.

## 9. Complaints, suggestions, and formal correspondence

- Distinct categories and routing.
- Optional confidential submission where operationally supported.
- Reference number, receipt, status, responsible role, response record, retention schedule.
- Do not promise anonymity unless the platform and workflow technically guarantee it.

## 10. Administration and reporting

- Role-specific dashboards; least privilege.
- Search and filter with access controls.
- Export permissions separated from view permissions.
- Audit logs for application decisions, member status changes, payment adjustments, certificate issuance, exports, and role changes.
- Reports: member counts by status/class, renewal pipeline, course enrollment, attendance, revenue/settlement reconciliation, certificates, event participation.

## 11. Notifications

- Email first; optional SMS/WhatsApp integration only after sender/account approval and privacy review.
- Templates bilingual and editable.
- Notifications for application receipt/status, missing documents, dues, payment result, course reminders, event changes, certificate availability, and account security.
- Delivery failures logged; notification content must not disclose sensitive data.

## 12. Common requirements

- Bilingual Arabic/English; all user-facing content translatable.
- Mobile-first, keyboard accessible, clear validation and error messages.
- Consent and privacy notice at collection points.
- Data minimization, retention schedule, export/deletion request workflow.
- No collection or processing of patient clinical data.
