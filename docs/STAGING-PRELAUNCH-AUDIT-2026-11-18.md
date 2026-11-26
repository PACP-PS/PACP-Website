# PACP staging prelaunch audit — 2026-11-18

Status: **HOLD — NOT APPROVED FOR PRODUCTION**. This is a read-only assessment of the connected GitHub/Supabase environments, not a penetration test or functional UAT.

## Verified configuration
- Repository: `PACP-PS/PACP-Website`; default `main`, development `rebuild/platform-foundation`. Development is ahead of `main` by 346 commits at inspection.
- Supabase `PACP-Development` (project `lofvxgubetdslvaczvjp`): active. 17 public tables, RLS enabled for all.
- Supabase `PACP-Staging` (project `aweebuukeovcekctclws`): active. Five public tables, RLS enabled for all.
- Staging: three Auth accounts, four staff-role records across two distinct staff users (two finance, one membership_approver, one superadmin); one application. **These counts do not prove login, individual role ownership, or workflow success.**
- Supabase security advisor: development has five RLS-no-policy INFO findings and eight authenticated SECURITY DEFINER warnings; staging has four RLS-no-policy INFO findings, seven authenticated SECURITY DEFINER warnings, and a leaked-password-protection warning.
- Staging's operational notification table contains records; this does **not** prove email delivery.

## Required release blockers / security review
1. Inspect all staging SECURITY DEFINER RPC bodies and authorization checks, particularly `pacp_admin_list_applications`, `pacp_record_cash`, `pacp_review_application`, and `pacp_issue_card`. A callability lint is **not** itself a confirmed vulnerability; test unauthorized roles and object-level ownership, including cross-user UUIDs.
2. Explicitly document why RLS-no-policy tables are service-only and verify no direct unintended client access. Do not add broad permissive RLS policies just to silence warnings.
3. Enable leaked-password protection in Supabase Auth if supported by the selected plan, and confirm password strength and MFA for staff.
4. Test account-by-account authorization: member must not see staff functions; finance must not approve membership; membership approver must not record cash; admin can do only documented privileged operations. Re-test after any Auth account replacement.
5. Complete staging-only end-to-end UAT: application submission → administrative review → finance verification → activation → card issuance/verification → revocation, and courses/registrations/CPD/certificates as applicable. Record pass/fail and test evidence without sharing secrets or personal data.
6. Compare the canonical root `index.html` to approved visual screenshot in a real desktop and mobile browser, including original logo and glass-effect membership card; visual parity is not yet evidenced.
7. Check branch CI, accessibility (Arabic RTL and English), backup/restore, auditability, TLS, rollback, and notification delivery separately before release approval.

## Change control
- No `main` merge, live `pacp.ps` deployment, Cloudflare DNS change, MX/SPF/DKIM/DMARC adjustment, real payment enablement, or email sending is authorized by this audit.
- Distinguish `PACP-Development` legacy schema (`members`, `profiles`, etc.) from `PACP-Staging` `pacp_*` schema. Do not assume equivalent tables or copy production/personal data between them.
- No schema mutations or access-control changes were performed in this audit.
