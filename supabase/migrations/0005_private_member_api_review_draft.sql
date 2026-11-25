-- PACP column-minimization boundary — REVIEW DRAFT / NOT DEPLOYED
-- Depends on base schema and 0001–0004. Review privilege owner and API grants.
begin;

-- RLS protects rows, not sensitive columns. Revoke direct client reads on
-- tables whose rows contain identity details, internal review notes, or private
-- storage paths. Access is through narrowly scoped SECURITY DEFINER RPCs.
revoke select on public.members from anon, authenticated;
revoke select on public.membership_applications from anon, authenticated;
revoke select on public.membership_documents from anon, authenticated;
revoke select on public.membership_application_events from anon, authenticated;
revoke select on public.membership_status_history from anon, authenticated;
revoke select on public.membership_renewal_requests from anon, authenticated;
revoke select on public.audit_log from anon, authenticated;

-- A member may read a minimal summary of their own approved record.
-- No national ID, date of birth, contact details, storage paths or approval notes.
create or replace function public.my_membership_summary()
returns jsonb language plpgsql stable security definer
set search_path = pg_catalog, public, auth
as $$
declare v_user uuid := auth.uid(); v_result jsonb;
begin
  if v_user is null then
    raise exception 'Authentication required' using errcode='28000';
  end if;
  select jsonb_build_object(
    'membership_code',m.membership_code,
    'name_ar',concat_ws(' ',m.name_ar_first,m.name_ar_father,m.name_ar_grandfather,m.name_ar_family),
    'name_en',concat_ws(' ',m.name_en_first,m.name_en_father,m.name_en_grandfather,m.name_en_family),
    'membership_type',m.membership_type,
    'status',m.status,
    'approved_at',m.approved_at
  ) into v_result
  from public.members m where m.user_id=v_user;
  return v_result;
end;
$$;
revoke all on function public.my_membership_summary() from public, anon;
grant execute on function public.my_membership_summary() to authenticated;

-- Applicant can read status and timestamps of their own application, but not
-- submitted_data, review_notes, reviewer identity, or other applicants' data.
create or replace function public.my_membership_applications()
returns jsonb language plpgsql stable security definer
set search_path = pg_catalog, public, auth
as $$
declare v_user uuid := auth.uid(); v_result jsonb;
begin
  if v_user is null then
    raise exception 'Authentication required' using errcode='28000';
  end if;
  select coalesce(jsonb_agg(jsonb_build_object(
    'application_id',a.id,
    'status',a.status,
    'submitted_at',a.submitted_at,
    'reviewed_at',a.reviewed_at
  ) order by a.submitted_at desc),'[]'::jsonb)
  into v_result
  from public.membership_applications a
  where a.applicant_user_id=v_user;
  return v_result;
end;
$$;
revoke all on function public.my_membership_applications() from public, anon;
grant execute on function public.my_membership_applications() to authenticated;

-- A reviewer may see the minimum application queue metadata. Detailed document
-- access and decision actions remain separately permissioned.
create or replace function public.membership_review_queue(p_limit integer default 25)
returns jsonb language plpgsql stable security definer
set search_path = pg_catalog, public, auth
as $$
declare v_result jsonb;
begin
  if auth.uid() is null or not public.can_review_membership() then
    raise exception 'Not authorized' using errcode='42501';
  end if;
  if p_limit is null or p_limit < 1 or p_limit > 100 then
    raise exception 'Invalid limit' using errcode='22023';
  end if;
  select coalesce(jsonb_agg(jsonb_build_object(
    'application_id',q.id,'status',q.status,'submitted_at',q.submitted_at,
    'reviewed_at',q.reviewed_at
  ) order by q.submitted_at asc),'[]'::jsonb)
  into v_result
  from (
    select id,status,submitted_at,reviewed_at
    from public.membership_applications
    order by submitted_at asc,id asc
    limit p_limit
  ) q;
  return v_result;
end;
$$;
revoke all on function public.membership_review_queue(integer) from public, anon;
grant execute on function public.membership_review_queue(integer) to authenticated;

commit;

-- STOP-SHIP CONDITIONS:
-- 1) Verify table ownership, function owners, default grants and search_path
--    in a disposable Supabase project. SECURITY DEFINER must not be owned by
--    a role that an untrusted user can assume.
-- 2) Verify that revoked SELECT privileges do not break workflow functions,
--    member portal queries, or RLS helper calls.
-- 3) Review other sensitive tables (registrations, certificates, CPD, activities)
--    for column leaks; not covered by this migration.
-- 4) Add storage.objects RLS for private uploads separately; table policies
--    do NOT protect files in object storage.
-- 5) Add pagination and rate limiting at API boundary for production queues.
-- 6) Do not expose service_role secrets to browsers or public build artifacts.
