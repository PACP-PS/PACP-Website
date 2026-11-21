# PACP — Two-stage official publication decision (2026-11-18)

## Recommendation
**Publish the informational site first, only after an explicit go-live approval and a reproducible prelaunch check.** Never deploy all of `rebuild/platform-foundation` as-is: it contains admin/staging/demo and identity service scaffolding.

### Stage A: public informational release
- Build from canonical approved `index.html` with `python3 scripts/build_public_preview.py`.
- Cloudflare Pages artifact: **`build/pacp-public-preview` only**. Do not point Pages at repo root and do not merge 300+ development commits to production without a content review.
- Confirm build has only about, membership information, training information, news, resources and contact; no real login/application/payment/card/staging paths.
- Review brand/logo, Arabic RTL, accessible text/keyboard/reduced motion, all navigation links, links to privacy/contact, desktop/mobile screenshots, legal copy.
- Record existing live version and rollback instructions. Confirm registrar DNS and `info@pacp.ps` unchanged.
- Ask designated PACP approver to explicitly sign off on informational scope and timing. Do not treat general desire to launch as approval to change Cloudflare or DNS.

### Stage B: member platform
- Separate source/output and deployment from Stage A.
- Role-separated real JWT UAT, document/privacy controls, identity verifier approved and online, secure HMAC storage and rotating keys, staff MFA, backup/restore, acceptance of accessibility tests all required before enabling applications, course payment, membership cards or identity collection.
- Do not expose `supabase/functions/pacp-identity-link/index.ts` in production yet. It is intentionally fail-closed with HTTP 503 until private service-only RPC, legal/identity normalization and safe account recovery are completed.

## What is actually verified
- Source contract and multiple offline CI sandboxes passed at prior branch commit `260e2406c8f350e349440d76c88e66b7cb644819`.
- New identity-link scaffold was added on development branch and CI step created. Its **new** workflow result must be checked before assuming pass.
- PACP-Staging already has an empty, private RLS-protected identity registry; no actual ID numbers stored.
- Live website accessibility/HTTPS from available browser fetch was not confirmed; do not infer outage from a failed tool fetch.

## Next acceptance action
Use an isolated Cloudflare Pages preview build and confirm every public page, then owner approval, then promote **informational artifact only** with rollback retained. Later make controlled revisions as needed.
