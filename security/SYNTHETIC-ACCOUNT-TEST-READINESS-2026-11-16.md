# PACP — synthetic account test readiness, 2026-11-16

## Read-only inventory result
Direct read-only checks in Supabase PACP-Development (`lofvxgubetdslvaczvjp`) returned:
- `auth.users`: **0**
- `public.membership_applications`: **0**
- `public.staff_role_assignments`: **0**

**Consequence:** A real two-account authentication, row isolation, and staff permissions end-to-end test is currently impossible in this database. Never report it as passed; only the static CI checks and previous SQL/JWT claim simulation passed.

## Implemented in branch
`scripts/test_member_auth_live_readonly.py` uses the real Auth User endpoint to resolve two different privately supplied JWTs, checks each user's membership summary and own applications, denies the nonstaff review queue, and verifies that direct `public.members` table reads are forbidden. It fails as inconclusive unless each identity has at least one different synthetic application. Credentials must only be supplied as private runtime environment variables; never in GitHub or CI logs.

## Required controlled fixture, separate approval before any database mutation
- Create two **synthetic** nonstaff Auth accounts A and B using Supabase Auth, not hand-crafted JWT strings. Use valid verified test emails and separate passwords via controlled test setup, never real member information.
- Each must have one different synthetic membership application. Ensure fixture teardown plan, no real personal identifiers, and no payment or credential issuance.
- Create a separate test reviewer and test approver role only after the role-provisioning process is reviewed. Roles must be provisioned through trusted administration; never through self-assignable metadata.
- Test A cannot see B's application, B cannot see A's, nonstaff cannot read the review queue or full member table, reviewer cannot approve, approver can only perform allowed workflow transitions; verify logs and rollback.
- Do **not** run against production accounts and do not change currently empty PACP-Development merely to make CI green.
- Re-run Supabase security advisors and authorization tests before any activation, QR issuance or public deployment.

## Current release gate
BLOCKED: true cross-account and staff tests; credential/QR issuance disabled.
