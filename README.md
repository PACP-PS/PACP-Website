# PACP Website & Digital Services

Official website and planned digital-services platform for the Palestinian Association of Clinical Psychologists (PACP).

## Source-of-truth and safety
- `main` is the current published-site source branch; do not deploy feature previews directly to production.
- `rebuild/platform-foundation` contains design previews and draft implementation documents.
- Design previews are not connected to authentication, database, email delivery, certificates, or payments.
- Never put real member records, national IDs, passwords, API keys, payment details, or private documents in this repository.
- Payment integrations remain on hold pending provider verification, contract review, settlement/reconciliation requirements, and sandbox testing.

## Start here
1. [Product plan](docs/PRODUCT-PLAN.md)
2. [Site map](docs/SITEMAP.md)
3. [Functional scope](docs/PLATFORM-FUNCTIONAL-SCOPE.md)
4. [Technical architecture](docs/TECHNICAL-ARCHITECTURE.md)
5. [Security and privacy requirements](docs/SECURITY-PRIVACY.md)
6. [Database schema draft](docs/DATABASE-SCHEMA-DRAFT.sql)
7. [Implementation readiness gates](docs/IMPLEMENTATION-READINESS-GATES.md)

## Design previews
- [Homepage](design/homepage-preview.html)
- [Membership application](design/pages/membership-application-preview.html)
- [Membership review dashboard](design/admin/membership-review-dashboard-preview.html)
- [Digital membership card and member profile](design/pages/digital-membership-card-profile-preview.html)
- [Central admin dashboard](design/admin/central-admin-dashboard-preview.html)
- [CPD points management](design/admin/cpd-points-management-preview.html)
- [Course registration](design/pages/course-registration-preview.html)

Open an HTML file from the repository's GitHub interface and choose **Download raw file** to preview it locally. GitHub's source-code view is not itself a rendered website preview.

## Recommended implementation order
1. Confirm the deployment environment and staging URL.
2. Approve the association's membership types, eligibility rules, approval authority, renewal rules, and appeal/complaint process against the latest bylaws.
3. Select and configure database/auth/storage with separate staging and production projects.
4. Review and version SQL migrations; implement row-level security and server-side role checks before importing personal data.
5. Build and test membership submission/review/approval and unique membership-code issuance.
6. Build member portal and secure digital card verification.
7. Add courses, registration, attendance, accredited CPD points, and certificates.
8. Add content management, events, reports, and audit logs.
9. Integrate payment providers only after verification and contracting; use hosted checkout and signed webhooks.
10. Run accessibility, Arabic/English, security, backup/restore, and user-acceptance tests; release via a reviewed pull request.

## Important limitations
A repository commit does not automatically mean the feature is deployed or operational. Before release, verify Cloudflare Pages project settings, build command/output directory, environment variables, domain, TLS, and rollback. No Cloudflare configuration has been changed by this work.
