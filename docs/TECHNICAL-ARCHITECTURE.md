# PACP — Technical Architecture & Repository Plan

## Target repository layout

```
apps/
  web/                 # Public website and authenticated member/admin portal
packages/
  ui/                  # Shared accessible design system
  i18n/                # Arabic/English dictionaries and locale helpers
  config/              # Shared lint/type/build configuration
  domain/              # Shared domain types and validation schemas
  payments/            # Provider-neutral payment contracts and adapters
  notifications/       # Email/SMS provider abstractions
  security/            # Authorization helpers and audit utilities
supabase/
  migrations/          # Versioned SQL schema and policies
  functions/           # Server-side functions / webhooks (if Supabase selected)
docs/
  PRODUCT-PLAN.md
  SERVICE-REQUIREMENTS.md
  TECHNICAL-ARCHITECTURE.md
  SECURITY-PRIVACY.md
  OPERATIONS-RUNBOOK.md
  CONTENT-INVENTORY.md
```

## Application boundaries

1. Public content is readable without authentication, except drafts and restricted materials.
2. Member operations require an authenticated member identity and object-level authorization.
3. Staff operations require explicit role and permission checks server-side.
4. Payment operations run server-side and use verified provider callbacks.
5. File access uses private storage and short-lived authorized URLs.
6. Administrative and financial changes create immutable audit events.

## Proposed entities

- User, Profile, Role, Permission, UserRole
- MembershipApplication, Membership, MembershipDocument, MembershipRenewal
- Course, CourseSession, Instructor, CourseRegistration, Attendance, Evaluation
- Event, EventRegistration, AbstractSubmission, ReviewerAssignment, Review
- Invoice, PaymentIntent, PaymentTransaction, ProviderWebhookEvent, Refund
- Certificate, CertificateRevocation
- Page, NewsPost, Resource, Announcement
- ProfessionalDirectoryProfile, DirectoryConsent
- SupervisionRequest, VolunteerApplication, Complaint, Inquiry
- Notification, NotificationDelivery, AuditEvent

## Payment abstraction

Define a provider-neutral interface:
- create hosted checkout session
- verify webhook signature
- parse provider event into normalized event
- query transaction status
- initiate refund (where supported)
- reconcile settlement records

Persist provider, external transaction ID, currency, amount, status, idempotency key, timestamps, and reconciliation state. Never persist card PAN/CVV. A browser return URL is not proof of payment.

## Security baseline

- Database RLS / server authorization for every protected resource.
- Separate service credentials from public client keys.
- MFA for staff and super administrators.
- Rate limiting and bot protection on public forms and authentication.
- File allowlists, size limits, malware scanning where available, private buckets.
- Secrets only in managed environment variables; never commit credentials.
- CSP and security headers tailored to actual dependencies.
- Audit trail and backup/restore drills.
- Automated dependency and secret scanning.

## Deployment model

- GitHub feature branch → automated checks → preview deployment → review → pull request → approved merge → production deployment.
- Do not bind a new production deployment to the current domain until Cloudflare project, DNS, TLS, build settings, environment variables, and rollback are verified.
- Maintain separate development/staging/production environments and separate credentials/data.
