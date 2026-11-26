# PACP — member authentication and card integration gate

Status: implementation checklist, not production approval. Branch: `rebuild/platform-foundation`.

## Verified baseline (2026-11-16)
- Supabase project: PACP-Development. Public schema contains profiles, members, membership_applications, staff_role_assignments, membership_documents and related activity/certificate tables; RLS enabled on those tables.
- Read-only policy inspection: profiles_select_self restricts profiles to auth.uid(); members_select_self restricts members by user_id; applications_insert_self requires applicant ownership, status submitted, and unset reviewer/member fields; applications_select_self restricts to applicant; staff read policies depend on can_review_membership().
- This inspection alone **does not prove authorization is safe**. All policies, functions, GRANTs, Storage and negative tests must pass before UI authentication is connected.
- The public homepage and preview card are demos and must not infer membership validity. No real QR token, approval or card issuance is enabled.

## Execution order and acceptance gates

### Gate 1: verify backend security (blocking)
1. Review the complete definitions and grants of `can_review_membership()` and any other privileged functions; inspect SECURITY DEFINER and schema search_path protections.
2. Inspect all policies and column privileges for profiles, members, applications, documents, role assignments, activity enrolments and certificate tables; check for unapproved anon access and unexpected table writes.
3. Confirm ownership relation of `profiles.id`, `members.user_id`, and `membership_applications.applicant_user_id` to `auth.users.id`.
4. Inspect private Storage bucket policies for sensitive documents/photos; never expose file URLs in public QR verification.
5. Run role-based positive and negative tests: anonymous, applicant A, applicant B, active member, reviewer and admin. Verify users cannot read, edit or enumerate others' documents or membership data.
6. Establish audit logging and a reviewed server-only transition for approval/rejection/activation; do not let the browser set activation or membership number.

### Gate 2: member authentication
- Implement controlled sign-in/out and password recovery with Supabase Auth. Client uses publishable key only. Never expose service_role or privileged SQL.
- Fetch current user's member/application data through RLS; handle pending, rejected, approved-but-not-activated, active, suspended, expired and revoked states distinctly.
- No access to member dashboard based on editable user_metadata; check server-authoritative role assignments.

### Gate 3: official credential issue and verification
- Assign annual membership number transactionally only on approved activation after Board policy sign-off. Ensure unique constraint and an auditable history.
- Issue opaque random verification token server-side; store only a digest when practical, with revoke/rotate lifecycle and anti-enumeration protections.
- Public verification displays only approved minimal fields and current status, with privacy review and rate limiting. No national ID, email, phone, address, private photo or supporting documents.
- Embed QR only after real endpoint and tests exist. Mark every other preview DEMO/NOT VALID.
- Generate PDF from the same approved card fields; test Arabic/English glyph shaping, mobile/print sizing, accessibility and revocation.

### Gate 4: CI and stage review
- Run visual captures at 1648x928, 1440x900, 768x1024, 390x844; do not call technical pass visual approval.
- Run tests including RLS denial cases, QR forgery/guessability, revocation, unauthorized access and cross-account data leakage.
- Owner reviews screenshots and security/UAT report before any Cloudflare staging deployment; production remains unchanged until separate explicit approval.

## Design alignment
- Homepage design authority remains root `index.html`. Maintain large Jerusalem on right, brain on left and compact non-crowded center headline.
- Membership card preview uses original PACP emblem, Jerusalem panoramic identity, DEMO watermark and deliberately non-functional verification indicator.
- On phones <=520px the homepage mock front/back cards are stacked for readability; still requires browser screenshots and owner visual acceptance.

## No-go items
No public release, DNS/mail changes, privileged keys in browser/repository, actual member data in demo, real credential issuance, or payment enablement without separate review and approval.
