# PACP live CI and staging authorization verification — 2026-11-18

## Verified GitHub workflow run
Commit: `15fb320ccddc1470852d0e640d6f4059ac3cd757`
Workflow run: https://github.com/PACP-PS/PACP-Website/actions/runs/44331630547

- Prelaunch guardrails: **SUCCESS**, including new distinct public/private release-path check (step 6), canonical 3D source (step 4), static checks, simulated membership/card/course/revocation test (step 14), and deployment isolation (step 18).
- Five other sandbox/preflight workflows for that commit completed successfully.
- Scope: offline/CI contracts and isolated simulations; **not** a real-token role authorization test, real-browser visual acceptance, or a production deployment.

## Read-only staging database checks
- Public functions reviewed: `pacp_admin_list_applications`, `pacp_review_application`, `pacp_record_cash`, `pacp_issue_card`. Each uses `SECURITY DEFINER` with an explicit role-check guard and empty search_path; this decreases risk but is not independently verified against adversarial authenticated requests.
- `pacp_cash_receipts` enforces unique `application_id` and `receipt_number`, positive amount, verified-by user foreign key.
- `pacp_cards` enforces unique application, member code and verification token hash, with valid date checks.
- Four role records across two distinct staff accounts: finance role recorded for two, membership_approver for one and superadmin for one. Because finance overlaps with at least one other role, role separation requires transaction-level checks, not role labels alone.
- Card issue RPC checks distinct reviewer and cash verifier. Test separate approver and cashier identities with synthetic account tokens before release.
- Current remaining advisor findings and password protection setting are documented in `docs/STAGING-PRELAUNCH-AUDIT-2026-11-18.md`.

## Decision
- **CI contract gate: PASS.**
- **Staging real-auth negative testing: NOT VERIFIED.**
- **Desktop/mobile/RTL actual visual testing: NOT VERIFIED.**
- **Platform production release: BLOCKED.**
- **Informational-only site: release candidate subject to browser + legal + domain + explicit owner signoff.**

No data, schema, roles, Cloudflare deployment, DNS, mail or production branch changes were made during this verification.
