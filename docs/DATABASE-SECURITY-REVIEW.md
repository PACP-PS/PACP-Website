# Database security review notes — PACP

## Critical findings in the initial schema draft
1. `profiles.role` is a single text field. It must not be user-editable, and staff roles need a trusted assignment process with audit history. A multi-role model may be required as the association grows.
2. `national_id_encrypted` is only a column name; it does not encrypt data by itself. Use authenticated server-side encryption or a carefully scoped database encryption design, and never return the field to ordinary clients.
3. `membership_applications.submitted_data` stores flexible JSON. Server-side schema validation, size limits, allowed keys, and retention controls are required to prevent unreviewed sensitive fields from accumulating.
4. Direct access to tables can expose fields that a public or member UI does not intend to show. Prefer curated views or server endpoints for public cards, activity listings, and verification.
5. A unique constraint on membership codes prevents duplicates but does not itself implement safe code issuance. Generation must happen in a trusted server-side transaction after approval.
6. The draft schema does not by itself implement authorization, workflow transitions, transactional email, payment webhooks, or immutable audit controls.

## Included baseline migration
`supabase/migrations/0001_rls_baseline_review_draft.sql` enables RLS and adds deliberately restrictive self-service policies for a limited subset of read operations. It intentionally does not enable staff workflows, direct financial access, or client-side writes to registrations/CPD records.

## Important limitation
This is a review draft, not a validated production migration. The exact Supabase grants, RLS behavior, view ownership, function privileges, and query patterns must be tested in a disposable project. Applying it as-is would leave some desired operations unavailable; that is safer than prematurely granting broad access but is not a complete application authorization model.
