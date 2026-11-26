# PACP — Preview deployment runbook (NO PRODUCTION CUTOVER)

**Source of truth:** `PACP-Reference-Design-Cloudflare-v9/` in branch `rebuild/platform-foundation`.

## Intended static preview setup
- Cloudflare Pages project should use **non-production preview deployment** of branch `rebuild/platform-foundation`.
- Build command: none (static HTML).
- Build output directory: `PACP-Reference-Design-Cloudflare-v9`.
- Entry point: `/index.html`; preview center `/design/preview-center.html`.
- A branch preview URL must be taken from **actual Cloudflare Pages deployment details**. Do not guess or announce a URL from the GitHub repository name.
- Do **not** map `www.pacp.ps`, `pacp.ps` or `staging.pacp.ps` until DNS/SSL review and explicit approval.
- No MX/TXT/SPF/DKIM/DMARC, DNS registrar, custom domain or production branch changes.

## Mandatory controls
- Preview uses synthetic content only; real member records and documents must not be submitted.
- Authentication functions in `design/pages/auth.html` connect to Supabase Development. Do not encourage open public enrollment on a public preview before access and redirect settings have been audited.
- `membership-submit-staging.html` is disabled; the server submission RPC is not deployed.
- `central-admin-dashboard-preview.html` is a design preview, not an authorized live dashboard.
- `digital-card-staging.html` is a nonofficial preview and does not issue valid QR credentials.
- Before external distribution, confirm robots/noindex for all testing pages, avoid relying on robots to protect private data, and gate sensitive staging through Cloudflare Access if available.
- Check browser load, broken relative URLs, original logo, 3D hero performance, language switch, mobile menu, keyboard navigation, and Supabase Auth redirect allowlist.

## Manual UAT after a URL is obtained
1. Open preview in private browser; check original homepage layout and logo.
2. Navigate About, Membership, Training, News, Resources and Contact from the original navigation.
3. Open authentication with a synthetic account; verify logged-out and unauthorized states.
4. Confirm all preview-only actions cannot submit official applications, approve members or initiate payment.
5. Check mobile and slow-network layout, keyboard focus, console errors and network requests.
6. Compare screenshot with original approved PACP design references.
7. Document actual deployment URL, build SHA and dated evidence; do not mark launch complete.

## Current status (2026-11-15)
- Verified GitHub CI at `b0039c0f`: both static prelaunch and migration preflight **SUCCESS**.
- No verified publicly hosted preview URL from this workflow.
- Official website and registrar remain untouched.
