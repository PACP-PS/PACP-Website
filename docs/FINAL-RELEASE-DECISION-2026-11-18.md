# PACP — Final release decision record (2026-11-18)

**Current decision: NO-GO for full interactive platform.**

This record is a controlled completion checklist. A checked source-code contract is not equivalent to real-browser, credentialed security testing, or production approval.

## Release A: Informational website (independent path)

Deployable source is the canonical repository-root homepage built exclusively with `python3 scripts/build_public_preview.py`, output `build/pacp-public-preview/`.

### Already implemented in repository
- Approved three-column homepage source: luminous brain left; Arabic title center; Jerusalem right; original logo.
- Public-only builder redirects previews, login, application, course registration, cards and admin paths to informational pages.
- Feature warning says membership, fees, digital card and registration services are not yet enabled.
- The prelaunch CI workflow has static tests; a new `scripts/test_final_release_paths.py` is included in CI.

### Release A remaining acceptance evidence
- [ ] GitHub workflow succeeds on the final source SHA; inspect Actions logs.
- [ ] Generate actual public build, inspect output for forbidden files/links, and smoke-test all local page links.
- [ ] Compare browser screenshots desktop/tablet/mobile to approved original, including Arabic RTL, original logo, contrast and reduced-motion behavior.
- [ ] Confirm real domain, HTTPS and redirect behavior using separate read-only checks.
- [ ] Confirm MX/SPF/DKIM/DMARC unchanged (no DNS edits).
- [ ] Confirm approved privacy policy, contact details, accessibility, governance and legal copy.
- [ ] Obtain explicit association owner approval for informational launch.
- [ ] Record Cloudflare Pages target branch, build output, rollback plan and backup of current deployed version. Deploy only after approval.

## Release B: Membership, admin, finance, courses, digital cards (separate authorization)

**Not releasable merely because Release A ships.**

### Connected staging evidence checked (2026-11-18)
- PACP-Staging is active; five public tables report RLS enabled.
- Three Auth identities, four staff-role records (two unique staff identities), one sample application; these counts are NOT authorization tests.
- Security advisor flagged seven callable SECURITY DEFINER RPCs and four RLS-no-policy info findings; leaked-password protection disabled.
- PACP-Development is a different schema; its member/CPD tables cannot be assumed to exist in PACP-Staging.

### Mandatory Release B acceptance
- [ ] Stage-only explicit permission matrix: ordinary member, finance, membership approver, superadmin. Confirm staff-role intersections, negative access and object-level checks.
- [ ] Inspect each SECURITY DEFINER function (including admin listing) for secure auth checks, `search_path`, ownership, role constraints, and least privilege; verify denied requests with actual tokens.
- [ ] Confirm service-only RLS tables deliberately have no public policies, not inaccessible by accident.
- [ ] Configure leaked-password protection and strong staff MFA where available.
- [ ] Two synthetic applicants with separate applications: confirm individual record isolation and no cross-user UUID access.
- [ ] Complete submission → review → finance approval → activation → card issue/verify/revoke, logging all state transitions.
- [ ] Test finance, cancellation/refund/reconciliation, uniqueness of receipt identifiers; no real payment activation before provider contracts and verified settlement.
- [ ] Validate members/courses/registrations/attendance/CPD/certificate issuance against a consistent target schema; otherwise record as not implemented.
- [ ] Verify private document storage, signed URLs, uploads, revocation, audit logs, and backup restoration.
- [ ] Validate email outbox with a non-delivery dry run, then separate safe test delivery only with approval.
- [ ] Perform security, WCAG, AR/EN and clinical/professional content review; update `security/release-evidence.json` only with real evidence and explicit human approval.

## Non-negotiable controls

- Keep `main`, `www.pacp.ps`, registrar DNS, and email DNS unchanged during testing.
- No `service_role`/secret keys in browser, repository, logs or user-facing documentation.
- No real patient/member data in staging or code.
- No claims that an offline contract test constitutes a penetration test.
- Production promotion requires a reviewed PR, owner approval and rollback readiness.

## Final handoff
- Code branch: `rebuild/platform-foundation`.
- Release A artifact: `build/pacp-public-preview/` **after** build/test.
- Release B target: PACP-Staging until mandatory permissions and operational UAT pass.
- Overall launch remains blocked pending factual tests and authorization; do not auto-promote.
