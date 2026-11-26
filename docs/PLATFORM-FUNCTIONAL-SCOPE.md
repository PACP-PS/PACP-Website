# PACP Platform — Functional Scope and Delivery Plan

## Product objective
Deliver one bilingual Arabic/English association platform. The public website and authenticated services share one content and identity system. GitHub remains the source of truth for code. Production deployment is not authorized by this document.

## Proposed application areas

### Public website
- Home, association profile, mission and objectives.
- Governance and committees (publish only approved names and mandates).
- Membership categories and eligibility.
- News, events, training and announcements.
- Scientific resources, publications and professional opportunities.
- Contact, policies, accessibility and privacy pages.

### Member workspace
- Account creation and secure sign-in.
- Membership application, document upload, status tracking and committee decision.
- Profile and contact details.
- Membership renewal and fee status.
- Downloadable membership card and approved letters.
- Member-only announcements and resources.

### Training and events
- Course/event catalogue with dates, venue, trainer, capacity and fees.
- Registration, cancellation and waitlist.
- Attendance and participant evaluation.
- Certificate issuance and verification.
- Conference abstract submission and review workflow, if enabled by the association.

### Administration
- Role-scoped dashboard for membership, training, events, content and applications.
- Workflow queues with approve / request changes / decline decisions.
- Search, export and reporting with privacy-aware permissions.
- Audit log for administrative actions.
- Content publishing workflow with draft, review and publish states.

## Membership configuration — provisional
- Basic member: proposed public label for the statutory category “العضو العامل”.
- Supporting member: proposed public label for “العضو المؤازر”.
- Honorary member: proposed public label for “عضو الشرف”.
- The legal/statutory category is stored separately from the display label so the association can revise labels without changing legal records.
- Eligibility criteria are configurable and must be entered from the latest registered bylaws; do not hard-code assumptions.
- Application fee: 100 NIS as instructed by the association; record approval/effective date in governance settings.
- Rights, voting eligibility, nomination rights, renewal and category-specific fees remain configurable proposals pending formal board/assembly approval.

## Payment — disabled pending verification and contracting
Design the payment layer to support local Palestinian and international methods, but do not collect or process live payments until:
1. Providers available to a Palestinian registered association are identified and eligibility is confirmed.
2. The association completes provider due diligence, merchant onboarding and contracts.
3. Settlement currency, fees, chargebacks, refunds, reconciliation and tax/accounting treatment are agreed.
4. Security, privacy and PCI responsibilities are reviewed.
5. Test transactions and refund flows pass acceptance tests.
Store provider credentials only as server-side secrets; never in browser code or Git.

## Suggested technical architecture
- Web application: Next.js + TypeScript, responsive component system, accessible RTL/LTR.
- Visual layer: CSS 3D / motion for lightweight interactions; use WebGL/Three.js only for hero elements where performance permits.
- Backend: managed PostgreSQL with authentication, object storage and row-level access policies.
- Deployment: Cloudflare Pages/Workers or an equivalent supported deployment target after compatibility and configuration review.
- Email: verified transactional email provider for application receipts and notices.
- Integrations: payment providers only after contracting; no payment secrets in client code.

## Security and privacy baseline
- Role-based access control: public, applicant, member, content editor, membership officer, training officer, finance officer, administrator and auditor.
- Row-level authorization for all member-specific records.
- Multi-factor authentication for privileged accounts where supported.
- Upload validation, file size/type limits, malware scanning and private document storage.
- Audit logs for decisions, exports, role changes and payment reconciliation.
- Data minimization, explicit consent, retention/deletion policy and secure backups.
- Do not collect or store clinical patient records; PACP is a professional association platform, not a clinical record system.

## Phased delivery under one complete roadmap
1. Identity and public website: design system, logo, homepage, all public page templates, bilingual content model.
2. Membership: bylaws-based eligibility configuration, application workflow, review queue, member workspace.
3. Training and events: catalogue, registration, attendance, evaluation and certificates.
4. Research and professional services: resource library, calls, abstract submission and directory only with opt-in consent.
5. Administration: roles, dashboard, content approval, reporting and audit.
6. Payments: provider verification, contracts, integration, testing and controlled activation.
7. Quality and launch: accessibility, security, performance, bilingual QA, backups, operational handover and launch approval.

## Acceptance criteria
- No invented people, events, research, partners or governance records.
- Every form has a defined destination, confirmation and error state; no fake submission success.
- Arabic and English are complete and independently reviewed.
- All member and admin routes enforce server-side authorization.
- Payments remain disabled until provider and contract checks are complete.
- The production branch and live deployment remain unchanged until an explicit release approval.
