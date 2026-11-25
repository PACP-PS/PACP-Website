# PACP — release-candidate handoff and non-production gate (2026-11-15)

**Current source:** `rebuild/platform-foundation` · **Production source:** `main`.  
**Status:** NOT APPROVED FOR LAUNCH. This document is a release checklist, not an operational certification.

## Confirmed read-only (15 November 2026)
- GitHub repository and feature branch exist; original logo, 3D visual assets and HTML previews are present.
- Development Supabase project `PACP-Development` is `ACTIVE_HEALTHY`; 17/17 public tables have RLS enabled.
- Security advisors still report 5 tables with RLS but no policy, and 7 callable SECURITY DEFINER functions. Neither finding alone proves a leak; both require specific role and grants review.
- Member-dashboard staging is wired to authenticated read-only RPCs in source. Full account login, email recovery and multi-user isolation have **not** been exercised with test identities.
- Admin, application, course, CPD, payment and certificate previews are not proof of functional backend integration.

## Non-negotiable restrictions
1. Do not edit `main`, DNS, `pacp.ps`, `www.pacp.ps`, mail MX/SPF/DKIM/DMARC, Cloudflare production project or live member records.
2. Do not accept real membership submissions, publish live credentials, issue official cards, or collect payments through a demonstration UI.
3. Keep publishable Supabase key only in the browser; no service-role or payment-secret tokens in source.
4. Do not merge/deploy until the designated association owner signs the acceptance record.

## Verification matrix (all must pass before production)
| Gate | Owner/evidence | Status |
| --- | --- | --- |
| Ratified bylaws, membership categories, dues/CPD and privacy policy | PACP leadership decision | BLOCKED |
| Development/staging/prod isolation and rollback rehearsed | Hosting admin logs | BLOCKED |
| Public table grants and RLS for anon/applicant A/applicant B/member/staff/admin | SQL + direct REST test report | BLOCKED |
| SECURITY DEFINER function-by-function caller, EXECUTE, search_path, owner and output review | Security review | BLOCKED |
| Authentication: signup, verification, login, reset, logout, redirect allowlist | Synthetic accounts and screenshots | BLOCKED |
| Membership upload, request changes, rejection, approval, ID generation, expiry | Integration tests | BLOCKED |
| Staff RBAC cannot self-escalate; audit trails and role revocation | Negative test evidence | BLOCKED |
| Course capacity/waitlist/attendance/CPD/certificates and revocation | Test transactions | BLOCKED |
| Payments and settlement | Contract, sandbox callbacks, financial signoff | ON HOLD |
| Arabic RTL/English LTR, keyboard, mobile, reduced motion and 3D fallback | Device/browser QA | BLOCKED |
| Privacy retention, accessibility, contact details, content and final design approval | Editorial and legal signoff | BLOCKED |
| Deployment pipeline, TLS, redirects, cache, backup/restore and rollback | Staging rehearsal | BLOCKED |

## Security review probes (READ ONLY; use authenticated tester roles separately)
```sql
select schemaname, tablename, rowsecurity from pg_tables
where schemaname='public' order by tablename;
select schemaname, tablename, policyname, roles, cmd, qual, with_check
from pg_policies where schemaname='public' order by tablename, policyname;
select table_name, grantee, privilege_type
from information_schema.role_table_grants
where table_schema='public' and grantee in ('anon','authenticated')
order by table_name,grantee,privilege_type;
select n.nspname, p.proname, p.prosecdef, p.proconfig, 
       has_function_privilege('authenticated',p.oid,'EXECUTE') as authenticated_execute
from pg_proc p join pg_namespace n on n.oid=p.pronamespace
where n.nspname='public' order by p.proname;
```

## UAT record (fill only with verified outcomes)
- Tested build commit:
- Staging URL (not production):
- Synthetic accounts and role matrix (store identifiers privately):
- Tests passed / failed:
- Security findings and remediation:
- Accessibility and responsive evidence:
- Restoration/rollback test result:
- PACP authorized approver and date:
- Explicit release approval: **NO**

## Cutover plan — DO NOT EXECUTE WITHOUT APPROVAL
1. Freeze reviewed candidate commit; retain stable production rollback commit.
2. Deploy to isolated preview/staging (no production domain modification).
3. Complete and sign UAT/security/backup/rollback acceptance.
4. Only after written approval: schedule production release, preserve email records, inspect TLS/redirects/health, and retain rollback path.
5. Record post-release monitoring and incident owner.

Automated GitHub prelaunch checks verify only source-file presence, selected secret patterns and draft migration structure; they do not certify secure operations or successful production deployment.
