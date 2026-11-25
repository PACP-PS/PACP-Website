# PACP Disability Inclusion & Accessibility Specification — November 2026

Target: WCAG 2.2 AA (not yet certified). Reference: https://www.w3.org/TR/WCAG22/

## Implemented in development branch
- Shared keyboard-operable reading preferences: text enlargement, high-contrast mode, reduced motion, persistent device-only settings, skip-to-content.
- Defer-loaded script and styling connected to canonical homepage, membership application preview and course registration preview.
- Public static builder now copies the two accessibility assets.
- Optional accommodation section in the two *preview* forms; explicit notice that no information is saved or sent.

## Release-blocking inclusive service design requirements
1. **Non-discrimination:** do not make diagnosis, disability category, or medical documentation mandatory for membership or course eligibility. Request functional accommodations, not disability proof.
2. **Accommodation workflow:** user can request captions, transcripts, sign-language interpretation, readable files, step-free venues, accessible toilets/seating, breaks, additional time or remote participation. Provide response timing, contact channel and appeal route.
3. **Privacy:** avoid storing free-text medical details by default. Design separate restricted accommodation records with least-privilege access, limited retention, consent/notice, withdrawal and deletion; never include them in financial reports, public profiles or QR verification.
4. **Membership form:** semantic labels; step validation and summary with focus; error identification; review before submission; no time limit without extension; accessible attachments and optional non-digital submission.
5. **Training/course registration:** list accommodation availability before enrolling; downloadable accessible content; captioned and transcribed videos; material in advance; non-audio attendance alternatives; accessible exams and evaluations.
6. **Website:** Arabic RTL and English LTR, valid language switching, meaningful alt text, keyboard and screen-reader navigation, visible focus, 200% and 400% zoom/reflow, contrast ≥4.5:1 for normal text, ≥3:1 for large text, touch targets minimum 24×24 CSS px with exceptions, no keyboard traps, reduced motion, captions/transcripts and accessible PDF.
7. **Review:** automated axe/Lighthouse tests plus manual NVDA/VoiceOver, keyboard-only, mobile zoom and low-bandwidth testing; involve actual users with disabilities (hearing, mobility, vision, cognitive), with consent.
8. **Alternative channels:** accessible email and text messaging for assistance; do not require telephone-only communications.

## Known limitations
- Current enhancement controls do not, by themselves, prove WCAG compliance.
- Text scale relies partly on page authors' use of relative units; several existing components use fixed px. Full 200%/400% reflow testing remains mandatory.
- Contrast toggle is a user preference, not a substitute for adequate baseline color contrast.
- Accommodation fields added to *design previews only*. No database persistence, notifications, admin workflow or consent collection has been activated.
- The public informational build does not include the private preview forms.
- Real user acceptance and independently tested login/permissions remain pending.

## Login & access rights — staging test matrix
| Caller | Own application | Admin listing | Approve | Record cash | Issue card |
|---|---|---|---|---|---|
| anon | denied | denied | denied | denied | denied |
| ordinary member | own only | denied | denied | denied | denied |
| finance-only | explicit scope only | denied | denied | allowed if valid | denied |
| membership approver-only | explicit scope only | allowed | allowed | denied | conditional |
| superadmin | documented scope | allowed | check documented grants | check documented grants | check documented grants |
Test *both* role denial and cross-user object ID attacks; never rely only on visible navigation.

Read-only SQL inspection verified `anon` lacks EXECUTE for the public `pacp_*` functions; most authenticated accounts can invoke role-guarded RPCs. This is not evidence that member/finance/approver real-token tests have passed.

Before activating protected functions, perform negative POST tests using distinct synthetic user JWTs held only in secure test execution environment, never in source control or chat logs.
