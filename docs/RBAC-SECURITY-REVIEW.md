# PACP RBAC & RLS implementation review

**Status:** Draft security design committed to development branch. Not tested or deployed.

## Authority model

- **Identity:** Supabase Auth `auth.uid()`.
- **Authorization:** Active rows in `staff_role_assignments`, provisioned exclusively by a trusted administrative process, not `profiles.role`.
- **Decision authority:** `membership_approver` is required for final approval/rejection. Technical `admin` has no implicit membership decision authority.
- **Review authority:** `membership_officer` or `membership_approver` may start review or request changes.
- **Revocation:** `revoked_at` invalidates the role on the next authorization check.
- **Least privilege:** staff roles cannot edit application tables directly from the browser.

## Migration sequence

1. Review and apply the foundation schema in a disposable database.
2. Review `0001_rls_baseline_review_draft.sql`.
3. Review `0002_membership_lifecycle_review_draft.sql`.
4. Review `0003_membership_approval_engine_review_draft.sql`.
5. Review `0004_staff_rbac_rls_review_draft.sql`.

**Integration dependency:** `0003` must check `has_staff_role` / `can_review_membership` rather than `profiles.role`. Its implementation has been updated in the development branch to call those helpers. Do not invoke it before `0004` is installed and tested.

## Unresolved high-priority security issues

1. **Column exposure:** baseline self-read policies on `members` and `membership_applications` expose entire rows. Replace with curated, column-restricted member and applicant endpoints; RLS is not field-level protection.
2. **Documents:** `membership_documents` is metadata only. Storage policies must restrict actual files by application and reviewer role. Use signed URLs with short expiry and audit downloads.
3. **Audit integrity:** `membership_application_events`, `membership_status_history` and `audit_log` must be append-only to normal application roles; trusted workflow functions must be reviewed for execution privilege and input validation.
4. **Trusted provisioning:** design a two-person approval workflow for granting `membership_approver` and an audit log for grant/revoke actions. No public grant function is provided.
5. **Business-rule validation:** approval engine currently validates only basic names/email. Bylaws, document requirements, duplicate identity detection, consent and fees must be validated before production.
6. **Member ID privacy:** do not populate `national_id_encrypted` with plaintext; a proper encryption and key management plan is still required.
7. **Fee configuration:** the current draft schema defaults annual fee to 100 ILS; final business rules need governance approval.
8. **SQL deployment:** a draft schema in `docs/` is not a tested baseline migration. Run migrations in a disposable environment with automated tests before creating staging.

## Security test matrix

| Test | Expected |
|---|---|
| Applicant A reads Applicant B application | Denied |
| Applicant reads application event internal_note | Denied |
| Officer reviews own assigned case | Allowed after validated workflow |
| Officer final-approves application | Denied |
| Approver final-approves complete application | Allowed only after validations |
| Technical admin without approver role final-approves | Denied |
| Approver role revoked then approval attempted | Denied |
| Member reads another member record | Denied |
| Member reads private identity columns through API | Denied by curated API grants |
| Unauthenticated user queries staff roles | Denied |
| Applicant inserts/updates staff role assignment | Denied |
| Parallel approval attempts | Exactly one approved membership record |
| Invalid/missing document on approval | Denied |
| Rejected application obtains a card | Denied |

## Acceptance gate

No production deployment, personal data collection, role assignment or real membership approval until the schema, RLS, Storage rules, privileged functions and test matrix pass independent review.
