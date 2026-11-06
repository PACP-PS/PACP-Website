-- PACP staff authorization & restrictive RLS — REVIEW DRAFT, NOT DEPLOYED
-- Dependency: baseline schema, 0001, 0002 and 0003.
-- SECURITY NOTE: Do not run against production without independent review and tests.
begin;

create table if not exists public.staff_role_assignments (
 id uuid primary key default gen_random_uuid(),
 user_id uuid not null references auth.users(id) on delete cascade,
 role_name text not null check (role_name in (
  'membership_officer','membership_approver','training_manager',
  'finance_officer','attendance_officer','accreditation_officer','auditor','admin'
 )),
 granted_by uuid references auth.users(id) on delete set null,
 granted_at timestamptz not null default now(),
 revoked_at timestamptz,
 revocation_reason text,
 constraint staff_role_revocation_time check (revoked_at is null or revoked_at >= granted_at)
);
create unique index if not exists staff_active_role_unique
 on public.staff_role_assignments(user_id,role_name) where revoked_at is null;
create index if not exists staff_roles_user_idx on public.staff_role_assignments(user_id);
alter table public.staff_role_assignments enable row level security;
-- No client SELECT/INSERT/UPDATE/DELETE policies: trusted administrative
-- provisioning only, with a separate out-of-band audit and approval process.
revoke all on public.staff_role_assignments from anon, authenticated;

create or replace function public.has_staff_role(p_role text)
returns boolean language sql stable security definer
set search_path = pg_catalog, public
as $$
 select (select auth.uid()) is not null
   and exists (
     select 1 from public.staff_role_assignments s
     where s.user_id = (select auth.uid())
       and s.role_name = p_role
       and s.revoked_at is null
   );
$$;
revoke all on function public.has_staff_role(text) from public, anon;
grant execute on function public.has_staff_role(text) to authenticated;

create or replace function public.can_review_membership()
returns boolean language sql stable security definer
set search_path = pg_catalog, public
as $$
 select public.has_staff_role('membership_officer')
     or public.has_staff_role('membership_approver');
$$;
revoke all on function public.can_review_membership() from public, anon;
grant execute on function public.can_review_membership() to authenticated;

-- Staff read is limited to membership review staff. No direct client updates:
-- changes must pass through a validated workflow function.
create policy membership_applications_staff_read
 on public.membership_applications for select to authenticated
 using ((select public.can_review_membership()));

create policy membership_documents_staff_read
 on public.membership_documents for select to authenticated
 using ((select public.can_review_membership()));

-- Do NOT give applicants direct access to this table: it contains internal_note
-- and reasons. Applicant-facing history requires a curated server endpoint/view.
create policy membership_events_staff_read
 on public.membership_application_events for select to authenticated
 using ((select public.can_review_membership()));

create policy membership_status_history_staff_read
 on public.membership_status_history for select to authenticated
 using ((select public.can_review_membership()));

create policy membership_renewals_staff_read
 on public.membership_renewal_requests for select to authenticated
 using ((select public.can_review_membership()));

-- Important: existing members_select_self policy exposes the whole member row
-- to its owner, including national_id_encrypted (ciphertext) and internal fields.
-- Production must use column-restricted API views/endpoints, with direct base-table
-- grants revoked. RLS alone is row-level, not column-level.
-- Similarly, existing applications_select_self exposes review_notes:
-- must replace with a curated applicant API before production.

commit;

-- Mandatory checks before applying:
-- * confirm SECURITY DEFINER owner cannot be controlled by an app user;
-- * grant staff roles only through an independently authenticated trusted process;
-- * ensure no self-assignment via profiles.role, JWT custom claims or user metadata;
-- * confirm RLS and SQL privileges on every table and object-storage bucket;
-- * test officer/approver/admin separation, cross-user access, revocation and audits;
-- * test API read column exposure, not only row policies;
-- * verify no workflow function exposes internal_note or national identity data;
-- * do not expose service_role key to browsers or Cloudflare Pages client assets.
