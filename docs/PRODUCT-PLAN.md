# PACP Digital Platform — Product & Delivery Plan

**Status:** Foundation planning / discovery  
**Repository:** `PACP-PS/PACP-Website`  
**Production safety:** This plan is being prepared on `rebuild/platform-foundation`. The `main` branch and live deployment must remain unchanged until a reviewed release is approved.

## Product vision

Build the official bilingual digital platform of the Palestinian Association of Clinical Psychologists (PACP): a credible public website plus secure, operational services for members, trainees, event participants, researchers, and association administrators.

The platform must not be presented as a clinical service, patient portal, crisis service, or emergency response channel.

## Experience and visual direction

- Arabic-first experience with complete English parity; correct RTL/LTR behavior, typography, dates, navigation, forms, and transactional messages.
- Use the official PACP logo supplied by the association as the primary identity asset. Preserve its proportions, colors, and Arabic/English naming; do not redraw or replace it with a conceptual mark. Prepare optimized web variants (SVG if supplied, otherwise transparent PNG/WebP) while retaining the original source file.
- Palette: association green, red, black, and white; restrained neutral surfaces.
- Distinctive 3D visual signature: a performant hero scene and selected section accents using Three.js / React Three Fiber where justified; CSS depth, lighting, and motion for lighter components.
- Motion must respect `prefers-reduced-motion`; provide static fallbacks, keyboard access, adequate contrast, and mobile-friendly performance.
- The 3D scene is decorative and must never obscure navigation, content, forms, or accessibility.

## Public website

1. Home / association overview, mission, vision, objectives, and values.
2. About PACP, governance, board, committees, and bylaws (only approved content).
3. Membership information and eligibility.
4. Training and continuing professional development catalogue.
5. Events, conferences, and announcements.
6. News and publications.
7. Professional resources and research opportunities.
8. Public professional directory (opt-in, consent-based, with field-level visibility).
9. Contact, location, and official communication channels.
10. Privacy, terms, accessibility, complaints, and service limitations.

## Authenticated services

### Member services
- Account registration and secure sign-in.
- Membership application and document upload.
- Application status, requests for additional information, and decision history.
- Member profile, consent and visibility settings.
- Membership category, renewal, dues/invoices, payment receipts, and digital membership card.
- Member directory opt-in and profile controls.
- Downloadable letters/certificates where authorized.

### Training and CPD
- Course catalogue, dates, instructors, prerequisites, capacity, fees, and language.
- Registration, waitlists, cancellation rules, and attendance records.
- Local and international payment options only after merchant/provider approval.
- Refund/cancellation status, receipts, course evaluations, and certificate issuance/verification.
- Admin controls for courses, cohorts, attendance, and certificates.

### Events and conferences
- Event pages and registration.
- Abstract submission with file upload and status tracking.
- Reviewer assignment and conflict-of-interest controls if scientific review is enabled.
- Attendance, speaker management, and certificates.

### Research and publications
- Calls for papers, research opportunities, approved resources, and publication announcements.
- Optional manuscript/abstract intake workflow with restricted reviewer access.
- No claim of journal peer review or accreditation unless formally established.

### Professional engagement
- Supervision / consultation request intake (administrative routing only; no clinical emergency handling).
- Volunteering and committee interest forms.
- Career and job announcements.
- Complaints, suggestions, and formal correspondence with restricted access and tracking.

### Administration
- Role-based dashboards and audit trail.
- Manage members, applications, courses, events, news, resources, payments, refunds, certificates, and user access.
- Export reports with least-privilege controls and logged access.
- Separate roles: super administrator, association administrator, membership officer, training officer, finance officer, event/research reviewer, content editor, read-only auditor.

## Payment strategy

**Current decision: payment provider selection and onboarding are deferred to the verification and contracting workstream.** The target capability is both Palestinian/local payment methods and international card payments. Do not hard-code a gateway or advertise payment as active before all of the following are verified:
1. The provider accepts a Palestinian legal entity and the association's registration documents.
2. Merchant onboarding, settlement account, currencies, fees, refund/dispute process, and settlement schedule are confirmed in writing.
3. The provider offers a supported integration/API or hosted checkout.
4. Webhook signature verification, idempotency, reconciliation, refunds, and receipts are implemented and tested.
5. Finance and legal representatives approve terms and accounting workflow.

Use a provider-adapter architecture so local and international providers can be added independently. Never store card numbers, CVV, or raw payment credentials. Prefer provider-hosted checkout/tokenization. Payment status must be derived from verified server-side provider callbacks, not browser redirects.

## Suggested technical architecture

- Frontend: Next.js + TypeScript, accessible component system, Arabic/English localization.
- 3D: Three.js / React Three Fiber, loaded lazily; static fallback and reduced-motion mode.
- Backend: secure server-side API / server functions; never expose privileged keys in browser code.
- Data: PostgreSQL (Supabase is a candidate, subject to data-processing, region, backup, and access review).
- Authentication: managed authentication with MFA for administrators; email verification and secure recovery.
- File storage: private buckets, signed short-lived URLs, file type/size scanning and authorization checks.
- Hosting: Cloudflare Pages/Workers or another compatible deployment target after checking the current account's capabilities and architecture fit.
- Source control: GitHub is the source of truth; feature branches, pull requests, preview deployments, automated checks, and reviewed releases.
- Content: begin with a controlled admin CMS/workflow; evaluate a dedicated headless CMS only if editorial needs justify it.

## Core data domains

- identities, profiles, roles, permissions, sessions
- membership applications, membership records, renewals, documents, consent
- courses, cohorts, instructors, registrations, attendance, evaluations
- events, abstracts, submissions, reviewers, decisions
- invoices, payment attempts, provider events, refunds, receipts
- certificates, verification tokens, issuance/revocation
- news, pages, resources, announcements
- inquiries, supervision requests, volunteering, complaints
- audit events, notification preferences, outbound notifications

## Security, privacy, and governance

- Apply least privilege and deny-by-default authorization.
- Enforce row-level authorization at the database/API layer; UI hiding is not access control.
- Keep identity documents and finance records private; never expose them in public directories or logs.
- Collect only necessary personal data; define purpose, retention, deletion, and access policies.
- Require consent for public directory listings and optional profile fields.
- MFA for privileged accounts; rate limits, CSRF protections where applicable, secure cookies, input validation, output encoding, and dependency scanning.
- Audit administrative reads/exports and all sensitive state changes.
- Backups and tested restore procedure; incident response and breach escalation contacts.
- No patient clinical records or sensitive health data in this platform.
- Publish a privacy notice and terms reviewed by the association before collecting live applications or payments.

## Delivery approach

1. Discovery and audit: verify domain, Cloudflare configuration, current production status, existing content, official assets, bylaws, operational workflows, and account ownership.
2. UX and visual system: approve sitemap, design tokens, responsive layouts, 3D concept, and Arabic/English content model.
3. Platform foundation: repository structure, CI checks, preview environment, database schema, authentication, roles, logging, and privacy controls.
4. Public site and CMS: pages, news, events, resources, SEO, accessibility, and analytics with privacy safeguards.
5. Member services: applications, review workflow, member accounts, renewals, and cards.
6. Training and events: registration, abstract submissions, attendance, certificates.
7. Finance: local and international provider onboarding, checkout, reconciliation, refunds, receipts.
8. Professional engagement and research workflows.
9. Security, accessibility, performance, backup/restore, UAT, and launch readiness.
10. Controlled production cutover with rollback plan.

## Launch acceptance criteria

- Arabic and English content parity and correct RTL/LTR behavior.
- No demo/sample data in production.
- No fake login, fake payment, or nonfunctional portal controls.
- Every form has a tested submission path, confirmation, error handling, and privacy notice.
- Role and object-level authorization tests pass.
- Payment provider webhooks and refund/reconciliation tests pass before payments are enabled.
- Accessibility, mobile, performance, security, backup/restore, and cross-browser checks documented.
- Production domain, DNS, TLS, redirects, headers, monitoring, and rollback verified.
- Association sign-off on legal, membership, finance, and content workflows.
