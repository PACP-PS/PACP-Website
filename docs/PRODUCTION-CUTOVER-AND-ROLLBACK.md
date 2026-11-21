# PACP — production cutover decision and rollback plan

Status: **HOLD / NO DEPLOY** (2026-11-15). Owner-approved screenshot is the three-column root `index.html` on `rebuild/platform-foundation`: brain left, text center, Jerusalem right, translucent cards. Do not substitute nested `PACP-Reference-Design-Cloudflare-v9/index.html`.

## Verified GitHub facts
- `main`: commit `0f002f0ee3bcb596a290ea34e038cceb57006793`, only four top-level files; homepage ~241 KB.
- `rebuild/platform-foundation`: commit `9dd583565f974ca3f02dfd84fef8dae50733ee18`, larger development tree; homepage ~28 KB plus images/assets.
- The new build is `scripts/build_public_preview.py` -> `build/pacp-public-preview`. This public-only output intentionally omits live admin/auth functionality; DO NOT market it as a fully functional membership portal.
- Official domain is not deployed or modified by creating this document.

## Required launch gates (all mandatory)
1. Confirm Cloudflare Pages production project, current production branch and deployment ID; preserve a known-good rollback deployment. Record real project settings from console, do not assume.
2. Publish the **exact build output** as a separate isolated preview deployment. Test at real HTTPS URL, not `content://` or `file://`.
3. Visually compare with owner's approved screenshot at desktop 1440, tablet 768, and mobile 390. Original logo, brain and Jerusalem must load. Membership cards must have approved glass appearance. Confirm mobile navigation and five service tiles (or approved mobile transformation).
4. Network/Console: zero missing image/font/CSS/JS assets, no unhandled errors; check fonts actually rendered and not fallback; test RTL/keyboard.
5. Cross-check all existing published URLs and redirects against new build; no broken links; privacy/contact pages and social links reviewed.
6. Either complete Supabase Development live role/RLS and test-user acceptance for auth, membership, admin, courses, QR and certificates, OR explicitly restrict launch to public informational website with these functions unavailable and honestly labeled.
7. Approve privacy, security, backups, deployment ownership and rollback; confirm DNS, custom domain, email MX/TXT/SPF/DKIM/DMARC unchanged.
8. Owner reviews real preview and gives explicit final production approval.

## Controlled release
- Take before screenshots and record production deployment ID and Git SHA.
- Deploy only from reviewed release commit with verified build output dir.
- Run 15-minute smoke checks: home, images, membership, training, contact, mobile; monitor logs.
- If critical defect, immediately roll back to prior Cloudflare Pages production deployment; verify site and mail.

This document is a gate checklist, **not evidence that any gate has passed**. No production release authorized.
