# PACP phase 2 staging release handoff — 2026-11-18

## Publication boundaries
**Public site:** Cloudflare Pages project `pacp-website`, informational-only release branch `release/informational-2026-11-18`; no member registration, identity collection, fees or cards should be enabled there.
**Phase 2 staging:** Existing Cloudflare project `pacp-staging-v8` and Supabase project `PACP-Staging` (`aweebuukeovcekctclws`). Do **not** alter the staging project's build configuration or public visibility without inspecting its current configuration and securing access.

## Implemented now
- Added `.github/workflows/platform-phase2-staging.yml`, running a non-deploying suite for site/public separation, ID-first privacy, fail-closed linkage, membership/staff contracts, cash and card controls, accessibility and release-gate denial.
- This is a CI test integration, **not** a live Cloudflare or Supabase authorization connection. No production secrets were installed and no member records moved.
- The official homepage footer now contains WhatsApp and Facebook alongside Instagram and email in the release branch.

## Non-negotiable activation gates
1. **Website deployment evidence:** latest Cloudflare production deployment successful, desktop and 320/375px mobile navigation validated, footer links tested.
2. **Staging test account separation:** independent ordinary member, finance-only, membership approver, and superadmin; real JWT positive and negative access tests.
3. **Identity:** reviewer-approved ID verification, private HMAC with server-only secret, duplicate-ID handling, account recovery, consent/retention, audit.
4. **Financial:** cashier/approver separation and transaction tests, no premature real receipts or money collection.
5. **Infrastructure:** staging site access restricted or clearly preview-only, secrets isolated, monitoring and rollback.
6. **Accessibility:** keyboard and screen reader checks, accessible accommodations, no automatic membership exclusion by Washington Group answers.

## Current evidence limitations
External fetching of `www.pacp.ps` and `pacp-website.pages.dev` failed in available web and container clients. GitHub run listing API yielded no run for the latest release commit. This does not establish outage or success. Accordingly, do not represent the footer deployment or mobile visual UAT as complete.

## Release decision
**Informational source updated:** YES. **Live published deployment verified:** NO.
**Phase 2 CI gate:** CREATED. **Phase 2 live services launched:** NO.
