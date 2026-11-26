-- PACP reporting RPC deployed to PACP-Development on 2026-11-08.
-- This file is a source snapshot, not an automatically applied migration.
create or replace function public.pacp_report_members(p_limit integer default 200)
returns table(member_code text,full_name text,email text,phone text,member_status text,approved_at timestamptz)
language plpgsql security definer set search_path = '' as $$
begin
 if auth.uid() is null or not (public.has_staff_role('admin') or public.has_staff_role('membership_officer') or public.has_staff_role('membership_approver')) then
  raise exception 'Access denied' using errcode='42501';
 end if;
 if p_limit < 1 or p_limit > 500 then raise exception 'Invalid limit'; end if;
 return query select m.membership_code::text,concat_ws(' ',m.name_ar_first,m.name_ar_father,m.name_ar_family)::text,m.email::text,m.phone::text,m.status::text,m.approved_at from public.members m order by m.created_at desc limit p_limit;
end $$;
revoke all on function public.pacp_report_members(integer) from public,anon;
grant execute on function public.pacp_report_members(integer) to authenticated;
-- TODO: Validate role checks using two real Auth accounts before enabling Excel export.
