-- PACP DEVELOPMENT ONLY: read-only SQL preflight, no writes.
-- Expected results are evaluated by security owner; this does NOT replace JWT UAT.
select
 (select count(*) from pg_class c join pg_namespace n on n.oid=c.relnamespace where n.nspname='public' and c.relkind='r') as total_public_tables,
 (select count(*) from pg_class c join pg_namespace n on n.oid=c.relnamespace where n.nspname='public' and c.relkind='r' and c.relrowsecurity) as rls_enabled_tables,
 to_regprocedure('public.submit_my_membership_application(jsonb)') is not null as submission_rpc_installed,
 position('if p_action is null or p_action not in' in pg_get_functiondef('public.process_membership_application(uuid,text,text,text)'::regprocedure)) > 0 as approval_guard_present,
 position('if p_action is null or p_action not in' in pg_get_functiondef('public.process_membership_application(uuid,text,text,text)'::regprocedure))
  < position('select * into v_app' in pg_get_functiondef('public.process_membership_application(uuid,text,text,text)'::regprocedure))
  and position('if p_action is null or p_action not in' in pg_get_functiondef('public.process_membership_application(uuid,text,text,text)'::regprocedure)) > 0
    as approval_guard_precedes_lookup;
-- Note: Five deny-all RLS tables can be correct; ensure grants + app requirements match.
