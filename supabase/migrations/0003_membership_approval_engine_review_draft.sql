-- PACP membership approval engine — SECURITY REVIEW DRAFT ONLY
-- Apply only after 0001 and 0002 have been reviewed and tested in disposable Supabase.
-- Never execute in production as part of this commit.

begin;

-- Explicit statutory decision role; technical admin is retained as emergency system role.
alter table public.profiles drop constraint if exists profiles_role_check;
alter table public.profiles add constraint profiles_role_check check (
  role in ('member','membership_officer','membership_approver','training_manager',
           'finance_officer','attendance_officer','accreditation_officer','auditor','admin')
);

create sequence if not exists public.pacp_membership_code_seq start with 1;

-- The function accepts only controlled workflow actions. Approval creates member,
-- assigns code, updates application and appends history/audit in one transaction.
create or replace function public.process_membership_application(
  p_application_id uuid,
  p_action text,
  p_reason text default null,
  p_applicant_note text default null
) returns jsonb
language plpgsql
security definer
set search_path = pg_catalog, public, auth
as $$
declare
  v_actor uuid := auth.uid();
  v_app public.membership_applications%rowtype;
  v_member_id uuid;
  v_code text;
  v_name jsonb;
  v_data jsonb;
  v_new_status public.application_status;
  v_member_status public.membership_status;
begin
  if v_actor is null then
    raise exception 'Authentication required' using errcode = '28000';
  end if;

  -- Authorization is evaluated against trusted staff_role_assignments via 0004 helpers.

  select * into v_app
  from public.membership_applications
  where id = p_application_id
  for update;

  if not found then
    raise exception 'Application not found' using errcode = 'P0002';
  end if;

  if v_app.status in ('approved','rejected','withdrawn') then
    raise exception 'Application is already in a final state' using errcode = '22023';
  end if;

  if p_action in ('start_review','request_changes') then
    if not public.can_review_membership() then
      raise exception 'Insufficient permission for review action' using errcode = '42501';
    end if;
    if p_action = 'start_review' then
      if v_app.status not in ('submitted','under_review','needs_changes') then
        raise exception 'Invalid state transition' using errcode = '22023';
      end if;
      v_new_status := 'under_review';
    else
      if v_app.status <> 'under_review' or coalesce(trim(p_applicant_note),'') = '' then
        raise exception 'Requesting changes requires under_review status and applicant note' using errcode = '22023';
      end if;
      v_new_status := 'needs_changes';
    end if;
    update public.membership_applications
      set status = v_new_status, reviewer_id = v_actor, review_notes = p_reason,
          reviewed_at = now()
      where id = p_application_id;
    insert into public.membership_application_events
      (application_id,from_status,to_status,action,actor_user_id,reason,internal_note,applicant_visible_note)
    values (p_application_id,v_app.status,v_new_status,
      case when p_action='start_review' then 'started_review' else 'requested_changes' end,
      v_actor,p_reason,p_reason,case when p_action='request_changes' then p_applicant_note else null end);
    insert into public.audit_log(actor_user_id,action,entity_table,entity_id,reason)
      values(v_actor,p_action,'membership_applications',p_application_id::text,p_reason);
    return jsonb_build_object('application_id',p_application_id,'status',v_new_status);
  end if;

  if p_action in ('approve','reject') then
    if not public.has_staff_role('membership_approver') then
      raise exception 'Only an authorized membership approver may decide' using errcode = '42501';
    end if;
    if v_app.status <> 'under_review' then
      raise exception 'Application must be under review before final decision' using errcode = '22023';
    end if;
    if coalesce(trim(p_reason),'') = '' then
      raise exception 'A decision reason is required' using errcode = '22023';
    end if;

    if p_action = 'reject' then
      update public.membership_applications
        set status='rejected', reviewer_id=v_actor, review_notes=p_reason, reviewed_at=now()
        where id=p_application_id;
      insert into public.membership_application_events
        (application_id,from_status,to_status,action,actor_user_id,reason,internal_note,applicant_visible_note)
      values(p_application_id,v_app.status,'rejected','rejected',v_actor,p_reason,p_reason,p_applicant_note);
      insert into public.audit_log(actor_user_id,action,entity_table,entity_id,reason)
        values(v_actor,'reject','membership_applications',p_application_id::text,p_reason);
      return jsonb_build_object('application_id',p_application_id,'status','rejected');
    end if;

    v_data := v_app.submitted_data;
    -- Required bilingual four-part name and email are validated server-side.
    if coalesce(trim(v_data->>'email'),'') = ''
       or coalesce(trim(v_data->>'name_ar_first'),'') = ''
       or coalesce(trim(v_data->>'name_ar_father'),'') = ''
       or coalesce(trim(v_data->>'name_ar_grandfather'),'') = ''
       or coalesce(trim(v_data->>'name_ar_family'),'') = ''
       or coalesce(trim(v_data->>'name_en_first'),'') = ''
       or coalesce(trim(v_data->>'name_en_father'),'') = ''
       or coalesce(trim(v_data->>'name_en_grandfather'),'') = ''
       or coalesce(trim(v_data->>'name_en_family'),'') = '' then
      raise exception 'Application is missing required bilingual identity fields' using errcode = '22023';
    end if;

    if v_app.created_member_id is not null then
      raise exception 'Application already linked to a member' using errcode = '23505';
    end if;

    v_code := 'PACP' || lpad(nextval('public.pacp_membership_code_seq')::text,4,'0');
    v_member_status := 'approved';

    insert into public.members(
      user_id,membership_code,
      name_ar_first,name_ar_father,name_ar_grandfather,name_ar_family,
      name_en_first,name_en_father,name_en_grandfather,name_en_family,
      email,phone,date_of_birth,residence,has_moh_practice_license,
      academic_level,specialty,graduation_year,workplace,experience_years,
      portrait_storage_path,membership_type,status,approved_at,approved_by
    ) values (
      v_app.applicant_user_id,v_code,
      v_data->>'name_ar_first',v_data->>'name_ar_father',v_data->>'name_ar_grandfather',v_data->>'name_ar_family',
      v_data->>'name_en_first',v_data->>'name_en_father',v_data->>'name_en_grandfather',v_data->>'name_en_family',
      v_data->>'email',v_data->>'phone',nullif(v_data->>'date_of_birth','')::date,v_data->>'residence',
      nullif(v_data->>'has_moh_practice_license','')::boolean,
      v_data->>'academic_level',v_data->>'specialty',nullif(v_data->>'graduation_year','')::integer,
      v_data->>'workplace',nullif(v_data->>'experience_years','')::numeric,
      v_data->>'portrait_storage_path',v_data->>'membership_type',v_member_status,now(),v_actor
    ) returning id into v_member_id;

    update public.membership_applications
      set status='approved',reviewer_id=v_actor,review_notes=p_reason,reviewed_at=now(),
          created_member_id=v_member_id
      where id=p_application_id;

    insert into public.membership_application_events
      (application_id,from_status,to_status,action,actor_user_id,reason,internal_note,applicant_visible_note)
    values(p_application_id,v_app.status,'approved','approved',v_actor,p_reason,p_reason,p_applicant_note);

    insert into public.membership_status_history(member_id,from_status,to_status,reason,actor_user_id)
      values(v_member_id,'draft','approved',p_reason,v_actor);

    insert into public.audit_log(actor_user_id,action,entity_table,entity_id,reason,after_data)
      values(v_actor,'approve','members',v_member_id::text,p_reason,
        jsonb_build_object('membership_code',v_code,'application_id',p_application_id));

    return jsonb_build_object('application_id',p_application_id,'status','approved',
      'member_id',v_member_id,'membership_code',v_code);
  end if;

  raise exception 'Unsupported action' using errcode = '22023';
end;
$$;

revoke all on function public.process_membership_application(uuid,text,text,text) from public, anon;
grant execute on function public.process_membership_application(uuid,text,text,text) to authenticated;
revoke all on sequence public.pacp_membership_code_seq from public, anon, authenticated;

commit;

-- IMPORTANT: profiles.role is still a draft source of authority. Replace with trusted\n-- staff_role_assignments and role-check helper before using this function.\n-- REQUIRED BEFORE USE:
-- 1) Validate submitted_data keys against the final application form.
-- 2) Review role assignment out-of-band; never let a user update profiles.role.
-- 3) Add and test RLS/policies for the new workflow tables.
-- 4) Confirm membership class, annual fee, statutory decision authority and ID format.
-- 5) Add explicit notification outbox and failure-safe delivery.
-- 6) Test parallel approvals, forged role claims, malformed JSON, null applicant ids,
--    duplicate applicant/member constraints, rollback, and unauthorized invocation.
-- 7) This draft is not production-ready and must not be run against production.
