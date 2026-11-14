-- PACP security baseline migration (REVIEW DRAFT; do not run against production)
-- Assumes the schema in docs/DATABASE-SCHEMA-DRAFT.sql has already been applied
-- to a disposable development database. This file intentionally does not grant
-- administrative permissions until a trusted role-assignment mechanism is reviewed.

begin;

-- Protect all application tables against accidental exposure through the API.
alter table public.profiles enable row level security;
alter table public.members enable row level security;
alter table public.membership_applications enable row level security;
alter table public.activities enable row level security;
alter table public.activity_accreditations enable row level security;
alter table public.registrations enable row level security;
alter table public.payment_records enable row level security;
alter table public.certificates enable row level security;
alter table public.member_cpd_ledger enable row level security;
alter table public.audit_log enable row level security;

-- Profiles: a signed-in user may read their own profile only.
-- Deliberately no client update/insert/delete policy. In particular, users must
-- never be able to change their own role field.
create policy profiles_select_self
  on public.profiles for select to authenticated
  using (id = (select auth.uid()));

-- Members: a member may read only the record linked to their own auth identity.
-- Do not expose national ID, DOB, residence, portrait path, or other fields
-- through a public verification endpoint; implement a dedicated minimal view
-- or server endpoint for public verification after security review.
create policy members_select_self
  on public.members for select to authenticated
  using (user_id = (select auth.uid()));

-- Applications: applicants may see their own submissions.
create policy applications_select_self
  on public.membership_applications for select to authenticated
  using (applicant_user_id = (select auth.uid()));

-- An authenticated applicant may submit an application only for themselves.
-- Staff review/update and anonymous public application submission are not
-- enabled by this baseline; add server-validated workflow functions later.
create policy applications_insert_self
  on public.membership_applications for insert to authenticated
  with check (
    applicant_user_id = (select auth.uid())
    and status = 'submitted'
    and reviewer_id is null
    and reviewed_at is null
    and created_member_id is null
  );

-- Published activities are readable by any visitor. Drafts remain staff-only
-- until explicit staff policies are added.
create policy activities_select_published
  on public.activities for select to anon, authenticated
  using (status in ('published','registration_open','registration_closed','in_progress','completed'));

-- Verified accreditation metadata may be read only when attached to a
-- publicly visible activity. Evidence paths and administrative notes remain
-- in the same row, so production should expose a curated public view instead
-- of granting direct table access. Therefore no direct policy is added here.

-- A signed-in user may read only their own registrations.
create policy registrations_select_self
  on public.registrations for select to authenticated
  using (applicant_user_id = (select auth.uid()));

-- No direct registration insert/update policy in this baseline: the workflow
-- must validate capacity, registration windows, duplicate requests, payment
-- requirements, and member linkage server-side.

-- Payment records are financial data: no direct client policies.
-- Certificates: allow a user to read certificates for their own registrations.
create policy certificates_select_own
  on public.certificates for select to authenticated
  using (
    exists (
      select 1
      from public.registrations r
      where r.id = certificates.registration_id
        and r.applicant_user_id = (select auth.uid())
    )
  );

-- CPD ledger: a member can read only ledger entries attached to their member
-- record. No member-facing write policy: points must be awarded/reversed by a
-- trusted, audited server-side action.
create policy cpd_select_own
  on public.member_cpd_ledger for select to authenticated
  using (
    exists (
      select 1
      from public.members m
      where m.id = member_cpd_ledger.member_id
        and m.user_id = (select auth.uid())
    )
  );

-- Audit log: no direct client access.
-- Staff/admin policies are intentionally omitted pending secure role mapping,
-- privilege separation, and explicit approval of decision authority.

commit;

-- Required before deployment:
-- 1) Test every policy using at least two distinct users and each staff role.
-- 2) Confirm anon/authenticated grants and database default privileges.
-- 3) Confirm no SECURITY DEFINER function is callable by untrusted users.
-- 4) Add curated public views for activities, accreditation and membership verification.
-- 5) Add server-side workflows for application review, code generation, registrations,
--    attendance, point award/reversal, certificates, payments, and audit logging.
-- 6) Never treat this draft as complete authorization: test on a disposable project.
