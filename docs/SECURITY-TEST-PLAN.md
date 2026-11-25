# PACP security test plan — executable scenarios for staging

**Status:** test design only. No live database connection or automated execution has been performed.

## Test setup
- Provision disposable Supabase project with fake identities: applicant A, applicant B, membership officer, membership approver, technical admin, revoked approver, anonymous.
- Apply schema and migrations in sequence after correcting all migration compatibility issues.
- Use only fabricated identity details and dummy documents.
- Exercise RPCs using real JWTs for each test identity; do not simulate roles by trusting browser-controlled claims.
- Inspect PostgREST table endpoints, RPCs, storage endpoints, and direct SQL grants.

## Required assertions

| Case | Action | Expected |
|---|---|---|
| S01 | Anonymous calls `my_membership_summary` | 401/permission denied |
| S02 | Applicant A calls `my_membership_applications` | Only A's records, no `submitted_data` or `review_notes` |
| S03 | Applicant A requests B's application via REST | Denied; no row/column leakage |
| S04 | Applicant A reads `members` via REST | No access to base table |
| S05 | Applicant A reads `membership_documents` via REST | No access |
| S06 | Officer calls `membership_review_queue(25)` | Minimal metadata only |
| S07 | Applicant calls `membership_review_queue(25)` | Permission denied |
| S08 | Approver calls `process_membership_application` for complete under-review application | One member, one code, audit entries |
| S09 | Officer calls approval action | Permission denied |
| S10 | Technical admin without approver role calls approval | Permission denied |
| S11 | Approver role revoked before action | Permission denied |
| S12 | Two parallel approvals of same application | One success at most; no duplicate membership |
| S13 | Approval with malformed/missing mandatory fields | Rejected, no partial member |
| S14 | Attempt to upload/read private file using another user's path | Denied by storage policy |
| S15 | Public verifier requests unissued/revoked code | No sensitive data; safe generic result |
| S16 | Browser calls staff role table write | Denied |
| S17 | User changes `profiles.role` or JWT metadata | Cannot gain decision authority |
| S18 | Expired or suspended member tries to use QR | Verification reflects current status |
| S19 | Rejected application tries to issue card | Denied |
| S20 | Untrusted user invokes any SECURITY DEFINER function | Only explicitly granted, authorized actions |

## Release blocking gaps

1. **Schema compatibility:** `0003` references JSON field keys that must be matched to the final form, and does not yet enforce all eligibility/document requirements.
2. **Data privacy:** baseline table reads and other endpoints need complete privilege review. `0005` addresses only member/application direct reads.
3. **Storage:** private buckets and `storage.objects` policies are not implemented.
4. **Authority:** independent staff-role provisioning and two-person approval of approver grants remain to be designed.
5. **Tests:** no test runner, disposable database, or CI job has been connected.
6. **Payment:** no live payment integration; fees remain a governance decision.

## Acceptance criteria

Zero unauthorized reads/writes; correct role revocation; no duplicate codes; no partial approval; private files inaccessible cross-user; audit trail immutable for application users; no patient information stored; all critical tests pass in disposable staging. A security review and governance sign-off are required before production.
