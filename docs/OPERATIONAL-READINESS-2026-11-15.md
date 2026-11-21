# PACP staging — operational readiness and access-control audit

**Audit date:** 2026-11-15  
**Branch:** `rebuild/platform-foundation`  
**Scope:** Read-only Supabase and GitHub review; no production or DNS changes.

## Verified facts

1. Supabase project `PACP-Development` (project ref `lofvxgubetdslvaczvjp`) currently returns **INACTIVE** from `list_projects`.
2. A read-only `select current_database(), current_timestamp` failed with `Database is possibly not accessible at the moment`. Therefore *live schema, policy, role, migration and API functionality are NOT verified*.
3. The browser authentication page at `PACP-Reference-Design-Cloudflare-v9/design/pages/auth.html` imports the Supabase client module `design/assets/pacp-supabase-auth.mjs`. This exposes only a **publishable** browser key and initializes `supabase-js` with PKCE. It provides sign-up, sign-in, password reset/change, logout and two member-scoped RPC calls.
4. The beautifully styled `design/pages/member-portal-preview.html`, `design/pages/course-registration-preview.html` and `design/admin/central-admin-dashboard-preview.html` are **demonstration interfaces**, not live data-connected member/admin/course portals. Their navigation and simulated tab flows work client-side; this does not establish database authorization.
5. The repository contains nine `supabase/migrations/0000–0008_*_review_draft.sql` SQL drafts. Their own headers say **review draft / not deployed**; GitHub presence does not demonstrate deployment.
6. `0004_staff_rbac_rls_review_draft.sql` sketches separate staff roles and a privileged `has_staff_role()` function. `0005_private_member_api_review_draft.sql` sketches column-minimal `my_membership_summary()`, `my_membership_applications()` and a membership review queue. All require database-side verification and privilege review.
7. Existing preview labels warn that data submission, approvals and payments are not operational; preserve these labels until real permission-tested workflows replace them.

## Current readiness matrix

| Capability | Verified now | Release gate |
| --- | --- | --- |
| Homepage and visual identity | Staging preview previously inspected | Phone and desktop regression test |
| Member portal visual navigation | Demonstration UI inspected | Live auth + ownership-scoped API |
| Sign up / login / recovery UI | Source code present, untested | Supabase becomes ACTIVE; dedicated test accounts |
| Member summary / my applications | Client RPC calls exist | RPC existence, grants, RLS and safe column projection |
| Membership application submissions | Preview only | Authenticated server workflow, validation, private documents |
| Admin and role separation | Preview only + SQL draft | Staff role provisioning; staff/nonstaff, cross-user tests |
| Course registration/attendance/CPD | Preview only | Real endpoints with policies and transaction tests |
| Email, payments and certificates | Not confirmed | Provider validation, secrets management, audited issuance |

## Mandatory next tasks — in safe order

1. **Restore/verify the development Supabase project** via its account dashboard. Determine whether paused, inactive, deleted, or access-restricted before any activation. Do not restore or change billing silently.
2. **Reconcile actual database state** with migration drafts (they may diverge). Read `pg_policies`, table ownership, `information_schema.role_table_grants`, `pg_proc` EXECUTE privileges, and Supabase security advisors. Never execute the drafts wholesale.
3. **RLS and data minimization**: prove all browser-reachable tables have appropriate RLS plus grants. Ownership-based policies must include `auth.uid()`; do not trust client-supplied role or `user_metadata`.
4. **SECURITY DEFINER review**: inspect each function owner, role checks, `search_path`, function grants and data returned. Revoke blanket `EXECUTE FROM PUBLIC` where necessary. Review internal notes, IDs and private storage paths for accidental exposure.
5. **Least-privilege test accounts**: unauthenticated, applicant A, applicant B, approved member, membership officer, approver, training manager, administrator. Test cross-user reads/writes, staff revocation, direct REST access, privileged RPC and storage objects.
6. **Stage member portal integration** with an authenticated, server-authorized member dashboard; do not present hardcoded demo data as live. Use publishable client key only.
7. **Stage admin module** behind verified role checks at the database/API boundary; a hidden tab or route is not authorization. Apply workflow and audit-log tests before enabling decisions.
8. **Stage course and CPD operations** with actual registration status transitions, attendance recording, award approvals, certificate issuance and rollback tests.
9. **Regression and release**: desktop/mobile checks, no production branch deployment, confirm `pacp.ps` and mail records unchanged until explicit approval.

### SQL read-only probes to run once development database is available

```sql
select schemaname, tablename, rowsecurity
from pg_tables where schemaname = 'public' order by tablename;

select schemaname, tablename, policyname, roles, cmd, qual, with_check
from pg_policies where schemaname = 'public' order by tablename, policyname;

select routine_schema, routine_name, security_type
from information_schema.routines
where routine_schema = 'public' order by routine_name;

select table_name, grantee, privilege_type
from information_schema.role_table_grants
where table_schema = 'public' and grantee in ('anon','authenticated')
order by table_name, grantee, privilege_type;
```

**Do not run migrations, grant permissions, touch real member data, or claim launch readiness until the inactive database is restored and these tests succeed.**

Related documentation: [Securing your Supabase API](https://supabase.com/docs/guides/api/securing-your-api).
