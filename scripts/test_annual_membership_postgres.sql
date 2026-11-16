-- Executes only in temporary GitHub Actions PostgreSQL service.
\set ON_ERROR_STOP on
CREATE ROLE anon NOLOGIN;
CREATE ROLE authenticated NOLOGIN;
CREATE TABLE public.members(id uuid PRIMARY KEY);
INSERT INTO public.members(id) VALUES ('11111111-1111-4111-8111-111111111111');
\i docs/annual-membership-sandbox-schema.review.sql
DO $$
DECLARE m uuid := '11111111-1111-4111-8111-111111111111';
BEGIN
  INSERT INTO public.membership_periods_sandbox(
    member_id,membership_year,period_start,period_end,period_status,activated_at,fee_decision,fee_decision_reference)
  VALUES (m,2027,make_timestamptz(2027,1,1,0,0,0,'Asia/Hebron'),
             make_timestamptz(2028,1,1,0,0,0,'Asia/Hebron'),
             'active',make_timestamptz(2027,1,1,0,0,0,'Asia/Hebron'),'settled','SYNTHETIC-TEST');
  IF (SELECT count(*) FROM public.membership_periods_sandbox)<>1 THEN RAISE EXCEPTION 'insert failed'; END IF;
  BEGIN
    INSERT INTO public.membership_periods_sandbox(member_id,membership_year,period_start,period_end)
    VALUES(m,2027,make_timestamptz(2027,1,1,0,0,0,'Asia/Hebron'),make_timestamptz(2028,1,1,0,0,0,'Asia/Hebron'));
    RAISE EXCEPTION 'duplicate year accepted';
  EXCEPTION WHEN unique_violation THEN NULL; END;
  BEGIN
    INSERT INTO public.membership_periods_sandbox(member_id,membership_year,period_start,period_end,period_status,activated_at)
    VALUES(m,2028,make_timestamptz(2028,1,1,0,0,0,'Asia/Hebron'),make_timestamptz(2029,1,1,0,0,0,'Asia/Hebron'),
    'active',make_timestamptz(2028,1,1,0,0,0,'Asia/Hebron'));
    RAISE EXCEPTION 'unpaid activation accepted';
  EXCEPTION WHEN check_violation THEN NULL; END;
  IF has_table_privilege('authenticated','public.membership_periods_sandbox','SELECT')
     OR has_table_privilege('anon','public.membership_periods_sandbox','SELECT') THEN
    RAISE EXCEPTION 'member table leaked'; END IF;
END $$;
SELECT 'PASS: sandbox SQL executes; duplicate, unpaid activation and access denied' AS result;
