-- PACP private membership document storage — REVIEW DRAFT ONLY
-- Supabase Storage required. Does NOT create a bucket or grant public access.
-- Bucket must be created PRIVATE by a trusted operator, named membership-private.
-- This draft provides owner-scoped uploads; reviewers should obtain short-lived
-- signed URLs only from a separately audited server-side document-review endpoint.
begin;
-- NOTE: Supabase Storage owns storage.objects. Test privileges and policy syntax
-- in a disposable Supabase project before applying.
create policy "pacp_document_owner_insert_review_draft"
on storage.objects for insert to authenticated
with check (
  bucket_id = 'membership-private'
  and (storage.foldername(name))[1] = (select auth.uid())::text
  and lower(storage.extension(name)) in ('pdf','jpg','jpeg','png')
);
create policy "pacp_document_owner_read_review_draft"
on storage.objects for select to authenticated
using (
  bucket_id = 'membership-private'
  and (storage.foldername(name))[1] = (select auth.uid())::text
);
-- No update/delete policy: submitted files are immutable from the client.
-- No public read policy. No staff read policy until an audited review API exists.
commit;
-- BLOCKERS:
-- (1) Client path prefix alone is not document ownership validation; associate
-- uploaded paths to application + authenticated applicant via trusted RPC.
-- (2) Validate MIME via file signatures, size limits, malware scanning,
-- and extension on a trusted server. Extension checks are insufficient.
-- (3) Configure private bucket with allowed MIME types and file size cap.
-- (4) Prohibit uploads for other users, abandoned applications and final states.
-- (5) Add retention, signed URL expiry, reviewer audit and secure deletion.
-- (6) Test all policies and bucket privileges in disposable Supabase only.
