-- PACP DEVELOPMENT ONLY — SECURITY REVIEW DRAFT, NOT DEPLOYED.
-- Submission through an authenticated SECURITY DEFINER RPC with caller-derived identity.
-- Do not run until role-boundary and application validation tests pass.
begin;
create or replace function public.submit_my_membership_application(p_data jsonb)
returns jsonb language plpgsql volatile security definer
set search_path = ''
as $$
declare
  v_user uuid := auth.uid();
  v_id uuid;
  v_errors jsonb;
  v_email text;
begin
  if v_user is null then
    raise exception 'Authentication required' using errcode='28000';
  end if;
  v_errors := public.membership_payload_shape_errors(p_data);
  if jsonb_array_length(v_errors) > 0 then
    raise exception 'Invalid application payload' using errcode='22023';
  end if;
  select email into v_email from auth.users where id=v_user;
  if v_email is null or lower(btrim(v_email)) <> lower(btrim(p_data->>'email')) then
    raise exception 'Email must match authenticated account' using errcode='22023';
  end if;
  -- Avoid multiple pending applications for the same user. Concurrent calls require a
  -- unique partial index or an advisory lock; this lock serializes per user for now.
  perform pg_catalog.pg_advisory_xact_lock(pg_catalog.hashtextextended(v_user::text, 0));
  if exists(select 1 from public.membership_applications
      where applicant_user_id=v_user and status in ('submitted','under_review','needs_changes')) then
    raise exception 'An open application already exists' using errcode='23505';
  end if;
  insert into public.membership_applications(applicant_user_id,submitted_data,status)
  values (v_user,p_data,'submitted') returning id into v_id;
  return pg_catalog.jsonb_build_object('application_id',v_id,'status','submitted');
end;
$$;
revoke all on function public.submit_my_membership_application(jsonb) from public, anon;
grant execute on function public.submit_my_membership_application(jsonb) to authenticated;
commit;
-- STOP SHIP: security-definer ownership, immutable validator, policy/privilege
-- review; signed-in actual REST tests; account verification, consent, quotas and
-- storage checks; business governance approval. No official membership is created.
