# PACP parallel frontend and database integration contract

**Status:** design + security drafts, not deployed.

## Public pages and navigation
- `design/website-integrated-preview.html`: interactive homepage.
- `design/pages/about-preview.html`: bilingual About page, editable institutional copy.
- `design/pages/membership-application-preview.html`: applicant experience.
- `design/pages/member-portal-preview.html`: member dashboard.
- `design/pages/course-registration-preview.html`: training experience.
- Verification preview link must not be treated as a working public verification endpoint.

## Backend boundaries
- Public site content: approved CMS content only; no fabricated association statistics.
- Membership form: authenticated server-validated submission, then staff review.
- Private documents: private bucket; upload and access controlled by application ownership.
- Membership approval: trusted staff role, eligibility checks, audit log and transaction.
- Digital card: server-issued after approval, public verification exposes minimum status only.
- Payments: no production integration pending governance and provider contracts.

## Design quality gate
- Bilingual Arabic/English with full RTL/LTR, including labels and screen-reader descriptions.
- Responsive desktop/tablet/mobile and reduced-motion fallback for 3D visual effects.
- Clear distinction between clickable design prototypes and functioning electronic services.
- Association's official approved logo, legal text and bylaws replace provisional copy before release.
- Preserve `pacp.ps` VPS, DNS and existing email configuration until infrastructure inventory.

## Database quality gate
- All migration files execute cleanly on disposable Supabase.
- No untrusted user can read another person's documents or application data.
- No approver can grant their own role.
- Validation and file verification are server-enforced, not browser-only.
- No production personal data used during testing.
