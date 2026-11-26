# PACP disposable Supabase staging setup

**Purpose:** isolated test-only database for membership lifecycle, RBAC, privacy and concurrency.
**Current status:** instructions only; no Supabase project has been provisioned.

## Environment separation

- Production `pacp.ps` and Cloudflare production remain unchanged.
- Use a separate Supabase project with a distinct project ID and keys; never reuse production credentials.
- Disable real outbound email/payment integrations. All identities, files and transactions must be synthetic.
- Do not use a production database backup or real national identity numbers.
- Do not commit `.env`, database passwords, service role keys or JWTs to GitHub.

## Provisioning

1. Create a disposable Supabase project or local Supabase development stack under an association-controlled account.
2. Record the test project reference securely, without credentials in the repository.
3. Review `0000_foundation_review_draft.sql` through `0005_private_member_api_review_draft.sql` before execution. These are drafts, not approved migrations.
4. Validate compatibility and execute only in the disposable environment.
5. Create fabricated Auth users for applicant A, applicant B, officer, approver, technical admin and revoked approver.
6. Provision staff roles through a trusted administrator using a documented audit trail, not browser-controlled `profiles.role`.
7. Exercise the test matrix in `docs/SECURITY-TEST-PLAN.md`.
8. Preserve logs and results in a security test report without credentials or personal data.

## Preflight

Run from repository root:

```bash
python3 scripts/check_migrations.py
```

This checks file presence and selected static security constructs. It does not execute SQL.

## Known blockers before SQL execution

- The base schema depends on `auth.users` and must run only in a compatible Supabase environment.
- `0003` uses authorization helpers defined by `0004`. Function creation and invocation order must be validated.
- Application payload JSON schema, document checks and statutory eligibility are not enforced comprehensively.
- Private Storage bucket policies and staff role provisioning are incomplete.
- Membership approval function and curated RPCs require a privileged function-owner and GRANT review.
- The payment policy and membership category rules remain subject to association approval.

## Exit criteria

A clean database can apply reviewed migrations without error, synthetic users can perform allowed actions, all cross-user and unauthorized actions are blocked, concurrent approvals cannot create duplicate memberships, and private files remain inaccessible to unrelated users.

**No-go** for live collection or production deployment until security tests pass and association governance approves the workflow.
