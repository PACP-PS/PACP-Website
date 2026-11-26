# PACP Supabase live integration status — 2026-11-17

## Verified (read-only inspection)
- Single available Supabase project: **PACP-Development** (`lofvxgubetdslvaczvjp`). No separate isolated staging project available.
- Current counts in this project: **zero** `auth.users`, **zero** `public.members`, **zero** `public.staff_role_assignments`.
- `public.my_membership_operational_status()` exists and is callable by `authenticated`, not `anon`. Calling without a valid user identity rejects the request.
- Dashboard on `rebuild/platform-foundation` calls that read-only RPC. This page is **not in the public release artifact**.
- The bank-transfer option remains disabled. No actual cash settlement, card, staff invite or annual activation endpoint has been applied to this project.
- Supabase Security Advisor identifies 8 exposed `SECURITY DEFINER` RPCs executable by authenticated users, including the operational status RPC, and 5 RLS-enabled tables with no policies. Security review is REQUIRED before enabling registration and financial or administrator actions.

## Testing that is still required (not performed)
1. A separate test Supabase project, or explicit authorization to use the current development environment for synthetic Auth accounts and schema tests.
2. Two independent Supabase Auth accounts with verified email (member A/member B), plus superadmin/reviewer/approver/finance roles.
3. Negative JWT requests: own-vs-other row, anonymous, lost permission after revocation, object ID tampering.
4. Tested server endpoints for cash receipt/reconciliation, reviewed membership activation, invitations, QR verification/revocation.
5. Authoritative production configuration and legal/association approval: cash amount, official receipts, approved status and membership calendar.

## Release policy
Do not mistake PostgreSQL-only synthetic role impersonation for real Supabase Auth end-to-end testing.
Keep payment, bank transfer, renewal activation and official cards disabled until reviewed end-to-end completion.
No production website, DNS, mail or real-member records have been modified in this step.

Reference: https://supabase.com/docs/guides/database/database-linter?lint=0029_authenticated_security_definer_function_executable
