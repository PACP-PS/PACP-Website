# PACP database migration compatibility audit

**Reviewed:** foundation schema plus migrations 0001–0005 on development branch.  
**Method:** source-level inspection only. **No database connection, SQL execution, or live security test.**

## Findings

| Priority | Finding | Consequence | Required action |
|---|---|---|---|
| Blocker | The base schema exists in `docs/DATABASE-SCHEMA-DRAFT.sql` rather than an executable versioned migration | Automated migration tooling cannot provision an empty project from the migration directory alone | Move reviewed baseline into `supabase/migrations/0000_...` after schema freeze and test clean installation |
| Blocker | Approval function accepts `submitted_data` JSON fields without an approved schema, eligibility and document validation | Incomplete or ineligible application may become an approved member | Define typed validation and check required document reviews before approval |
| Blocker | Applicant can insert `submitted_data` directly through the baseline insert policy | Malformed data or forged fields may enter the queue | Introduce server-validated submission RPC; restrict direct insert and enforce schema |
| Blocker | Storage bucket access rules are absent | Relational RLS does not prevent private-file access | Add private bucket policies and cross-user upload/download tests |
| Blocker | Role assignment has no trusted audited provisioning workflow | Approver privileges cannot yet be safely administered | Implement audited grant/revoke by separately authorized operators |
| High | `0003` is defined before `0004` helpers | Deployment must validate function dependency at invocation and ensure `0004` exists before use | Integrate migration order in disposable DB test |
| High | `0005` protects selected membership tables, but registrations, certificates, CPD and activities still need column-level privilege review | Potential private-field exposure | Audit grants and curated APIs for remaining modules |
| High | Member code formatting `lpad(nextval(...),4,'0')` does not enforce maximum length or final code policy | Format changes after 9999 and business rule remains undecided | Approve code policy, add issuance tests and explicit format rules |
| High | `profiles.role` remains in the schema alongside trusted `staff_role_assignments` | Confusing duplicate sources of authorization | Deprecate role as authority and prevent role-based UI from implying permission |
| High | SECURITY DEFINER ownership and function execute grants not verified | Privileged function misuse possible | Test owner, search path, grants, and impersonation attempts in disposable Supabase |
| Medium | The workflow stores `review_notes` and internal events without a fully specified retention policy | Unclear lifecycle for sensitive decision records | Approve retention and deletion rules |
| Medium | Existing static previews are not connected to an authentication/session model | UI cannot demonstrate real authorization | Build staging adapter only after database tests pass |

## Safe test order

1. Freeze and version the foundation schema.
2. Provision disposable Supabase project with fake identities.
3. Apply reviewed migrations in order; fix all execution errors.
4. Seed fictional applicants, staff and membership requests.
5. Run role separation, row/column privacy and object storage tests.
6. Run concurrent approval, rollback and duplicate-code tests.
7. Review security results and formally authorize a staging deployment.
8. Keep `main`, production Cloudflare Pages and live member data untouched until sign-off.

## Automated static preflight

Run `python3 scripts/check_migrations.py` from the repository root. It checks that the expected files and key authorization constructs exist. **Passing is not proof of runtime correctness or security.**

## Decision

**NO-GO for production or real personal-data collection.** Development and isolated testing may proceed after a disposable environment is configured.
