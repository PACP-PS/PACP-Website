# PACP — one-stop completion and handoff (2026-11-15)

## What is actually implemented
- Official identity assets (including the original PACP logo), website and three-dimensional homepage design previews.
- Supabase Development project exists with 17 RLS-enabled public tables (previous live audit).
- Authentication page and authenticated read-only member summary.
- Read-only reviewer queue page, guarded by Supabase RPC.
- Application validation and guarded submission UI, but submission is **disabled**, and its server RPC is **not deployed**.
- Staging-only digital membership card display with no official QR or public verification endpoint.
- Independent local **SQLite demonstration portal** (`PACP-Reference-Design-Cloudflare-v9/portal/app.py`) supports synthetic login, application, approval, card verification/revocation, training registration/completion; this is NOT the live Supabase backend.
- Existing tests exercise the local synthetic workflow; CI now invokes these tests along with source security checks.

## Hard blockers / must not misrepresent
- Supabase approval function currently differs from corrected draft. Proposed replacement under `security/approval-auth-before-lookup-dev-PATCH-NOT-APPLIED.sql` is **not deployed**.
- Member application submission RPC and least-privilege grant proposals are **not deployed**.
- No multi-account JWT isolation/authorization tests were completed against Supabase.
- No legal/governance approval of membership classes, finance/CPD policy, retention, consent.
- No verified hosted staging, TLS/redirect, browser accessibility, email/reset, backups/restore or actual QR verification service.
- Production payments intentionally remain **off**.
- **Do not** merge to `main`, claim launch readiness, handle real member data, alter domain/DNS/mail or publish without approval.

## Operator checklist, in order
1. Set up **separate isolated staging** with synthetic data and valid Supabase staging credentials. Review which Cloudflare Pages branch and directory are used. Production DNS/email remains unchanged.
2. Provision synthetic applicant A and B, reviewer, approver, admin. Keep test passwords/tokens outside GitHub.
3. Review privileged function source, owner, EXECUTE grants, `search_path`, RLS, private storage and table grants.
4. Review and manually apply reconciled development-only SQL. Verify rollback and security advisors. No automatic migration.
5. Test authenticated user isolation and denied reviewer/approver calls; see `docs/SYNTHETIC-AUTH-TEST-GUIDE.md`.
6. Complete and test submission, admin actions, approval/rejection, membership code uniqueness, valid/revoked verification, certificates and audited CPD. Local demo tests do NOT count as Supabase integration evidence.
7. Approve governance/privacy/courses/payment rules; run accessibility, Arabic/English, mobile, recovery, backup, incident-response and security testing.
8. Fill `security/release-evidence.json` with independently verified evidence. Independent authorized sign-off required.
9. Freeze and review release candidate; stage and rehearse rollback. **Stop before production domain switch** unless separately approved.

## Files of note
- `.github/workflows/prelaunch-guardrails.yml` — source checks and synthetic local end-to-end tests, no deployment.
- `PACP-Reference-Design-Cloudflare-v9/portal/test_workflows.py` — isolated local workflow simulation.
- `security/release-evidence.json` — currently fails closed by design.
- `docs/PRELAUNCH-HANDOFF-2026-11-15.md` — detailed release checklist.
- `docs/LIVE-AUTHORIZATION-REVIEW-2026-11-15.md` — observed DB authorization behavior.
- `security/approval-auth-before-lookup-dev-PATCH-NOT-APPLIED.sql` — review-only SQL.

## Final verdict
**Not ready for production; substantial front-end/demo implementation done, but real backend/security/UAT and governance gates remain.** The stop point requested by the user (ready for launch but not switched) requires the items above, and cannot honestly be certified by static and simulated tests alone.
