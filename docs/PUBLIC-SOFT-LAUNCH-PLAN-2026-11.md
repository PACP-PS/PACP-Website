# PACP public soft launch — proposed release checklist
**Status:** candidate / pending explicit site-owner approval. Do not deploy automatically.

## Release scope (Phase P1)
- Public official homepage: repository-root `index.html`, retaining approved original PACP logo and 3-column visual.
- Public informational pages: about, membership, training, news, resources, contact.
- Membership/training pages disclose that application, renewal, payments, card issuance and online enrollment are **not active**.
- No admin dashboard, test login, member database, staff API, renewal RPC, payment endpoint, QR or test data in public artifact.
- Existing organizational mailbox and domain DNS are out of scope.

## Release artifact
`python3 scripts/build_public_preview.py` produces **`build/pacp-public-preview/`**.
Run `python3 scripts/test_public_feature_flags.py` and
`python3 scripts/audit_public_assets.py` before any deployment.
A manual branch preview workflow exists at
`.github/workflows/manual-pages-preview.yml` and needs configured
Cloudflare credentials and the exact preview approval input.
No command here deploys or merges to production.

## Go/no-go release criteria
1. All CI checks on `rebuild/platform-foundation` pass.
2. Preview built from **root homepage**, not alternative reference homepage; verify 3-column hero, correct logo, responsive views, Arabic RTL, accessibility and mobile navigation visually.
3. Check all 6 public page routes, image paths, real contact details and legal/privacy links by browser; avoid claiming unverified contacts or events.
4. Verify public output contains no auth, admin, staging, membership credential, payment, secret or personal file. Keep external links accurate and safe.
5. Verify Cloudflare Pages build directory, custom domain binding, SSL/TLS, DNS/redirect and email/MX/TXT preservation in **read-only mode**.
6. Obtain written approval to promote candidate to `main` and publish to `www.pacp.ps`. Back up previous deployed artifact and create rollback reference.
7. Once approved, promote only the **public artifact**, never the whole dev tree. Validate HTTPS, redirects, analytics/privacy and actual live pages after release.

## Planned phased features after P1
P2: tested member Auth and application submission with genuine A/B JWT isolation
P3: staff portal permissions and review workflow, logged actions
P4: annual membership periods/renewal, verified payments and cards/QR
P5: course registration, attendance, certificates and CPD after governance approval

## Important
Approval to prepare a public launch is not authorization to modify production DNS or publish. Keep all in-progress services disabled. No official membership verification or paid service is implied by public mockups.
