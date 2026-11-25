# PACP staging live integration (2026-11-17)

## Project isolation
- Staging: **PACP-Staging**, ref `aweebuukeovcekctclws`, `eu-west-1`, ACTIVE_HEALTHY.
- Development: `lofvxgubetdslvaczvjp` — **not modified by staging schema migration**.
- This is **testing only**, no payments or official membership issuance.
- Browser-only staging harness: `PACP-Reference-Design-Cloudflare-v9/design/pages/pacp-staging-integration.html`; do **not** put it into the production static export.

## Live migration applied to staging
- `public.pacp_staff_roles`: registered Auth users, role and revoke timestamp; no direct public/admin assignment.
- `public.pacp_applications`: authenticated users may insert/select **own** applications via RLS; status starts at `submitted`.
- `public.pacp_cash_receipts`: finance-only confirmation RPC, unique cash receipt, exactly one per application.
- `public.pacp_cards`: approver-only issuance after distinct finance verification; annual year date bounds and revocation field.
- `pacp_private.has_role` checks roles using `auth.uid()`. Schema is not granted to browser roles.
- `public.pacp_review_application` restricted by database role checks.
- `public.pacp_record_cash` restricted by database finance role.
- `public.pacp_issue_card` restricted by database approver role and two-person approval/finance check.
- `public.pacp_my_card_status` returns own limited card status only.
- `public.rls_auto_enable()` event trigger helper RPC privileges revoked from anonymous/authenticated, while trigger function remains for DDL.

## Verified directly via staging SQL
- Four tables exist, all RLS enabled.
- Public anon EXECUTE is false for all four exposed PACP RPCs.
- Anonymous and phantom user identifiers are rejected from privileged actions.
- Zero Auth users, applications, staff assignments, receipts and cards at final inspection.
- No actual Auth sessions have been exercised; SQL-simulated identities are **not** proof of Auth integration.

## Must finish before real end-to-end completion
1. Host the *staging-only* harness under protected preview, configured with staging origin redirect URLs; do not publish on pacp.ps.
2. Create and email-verify **synthetic** test users with Supabase Auth using disposable testing mailboxes controlled by PACP.
3. Bootstrap initial superadmin **outside** public signup by authorized project owner after test user verification; then add a gated staff invite workflow. Do not grant roles via user metadata.
4. Assign separate finance and membership approver identities only in staging, and test denied and successful RPCs with actual `access_token` sessions.
5. Before issuing valid QR, implement server-generated opaque token & public verification endpoint with anti-enumeration/rate limits; current staging harness only stores a digest and does not deliver a valid official QR.
6. Check reconciliation policy and annual fee amount. Cash entry is test data only; bank transfer remains **disabled**.

### Known staging limitations
- No staff invitations from the UI yet, no email integration validation, no tested cash receipt vs approved amount, no admin queue, no printable official card, no renewal.
- Staging form does not replace PACP's production membership process.
- No production publish, domain or DNS changes.
