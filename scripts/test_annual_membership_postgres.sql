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
  -- A separate renewal period is allowed and must keep the original member ID.
  INSERT INTO public.membership_periods_sandbox(
    member_id,membership_year,period_start,period_end,period_status,
    activated_at,fee_decision,fee_decision_reference)
  VALUES(m,2028,make_timestamptz(2028,1,1,0,0,0,'Asia/Hebron'),
         make_timestamptz(2029,1,1,0,0,0,'Asia/Hebron'),'active',
         make_timestamptz(2028,1,1,0,0,0,'Asia/Hebron'),
         'waived','SYNTHETIC-BOARD-WAIVER');
  IF (SELECT count(*) FROM public.membership_periods_sandbox
      WHERE member_id=m AND membership_year IN (2027,2028))<>2 THEN
    RAISE EXCEPTION 'annual renewal failed';
  END IF;
  BEGIN
    INSERT INTO public.membership_periods_sandbox(member_id,membership_year,period_start,period_end)
    VALUES(m,2029,make_timestamptz(2029,1,2,0,0,0,'Asia/Hebron'),
           make_timestamptz(2030,1,1,0,0,0,'Asia/Hebron'));
    RAISE EXCEPTION 'invalid local January boundary accepted';
  EXCEPTION WHEN check_violation THEN NULL; END;
  BEGIN
    INSERT INTO public.membership_periods_sandbox(member_id,membership_year,period_start,period_end)
    VALUES(m,2030,make_timestamptz(2031,1,1,0,0,0,'Asia/Hebron'),
           make_timestamptz(2030,1,1,0,0,0,'Asia/Hebron'));
    RAISE EXCEPTION 'reversed period accepted';
  EXCEPTION WHEN check_violation THEN NULL; END;
  BEGIN
    INSERT INTO public.membership_periods_sandbox(
      member_id,membership_year,period_start,period_end,period_status,
      activated_at,fee_decision,fee_decision_reference)
    VALUES(m,2031,make_timestamptz(2031,1,1,0,0,0,'Asia/Hebron'),
           make_timestamptz(2032,1,1,0,0,0,'Asia/Hebron'),'active',
           make_timestamptz(2031,1,1,0,0,0,'Asia/Hebron'),'settled',' ');
    RAISE EXCEPTION 'blank fee evidence accepted';
  EXCEPTION WHEN check_violation THEN NULL; END;
  IF (SELECT count(*) FROM public.membership_periods_sandbox)<>2 THEN
    RAISE EXCEPTION 'negative tests changed rows';
  END IF;
  IF has_table_privilege('authenticated','public.membership_periods_sandbox','SELECT')
     OR has_table_privilege('anon','public.membership_periods_sandbox','SELECT')
     OR has_table_privilege('authenticated','public.membership_periods_sandbox','INSERT')
     OR has_table_privilege('anon','public.membership_periods_sandbox','UPDATE') THEN
    RAISE EXCEPTION 'member table leaked'; END IF;
END $$;
SELECT 'PASS: sandbox SQL executes; renewal, duplicate, fee, calendar and browser access checks' AS result;
-- Test the authoritative date/state predicate in disposable SQL, not from browser data.
-- This is a test expression, NOT an exposed production function.
DO $$
DECLARE
  check_at timestamptz;
  n integer;
BEGIN
  check_at := make_timestamptz(2027,12,31,23,59,59,'Asia/Hebron');
  SELECT count(*) INTO n FROM public.membership_periods_sandbox p
  WHERE p.membership_year=2027 AND p.period_status='active'
    AND p.fee_decision IN ('settled','waived') AND p.fee_decision_reference IS NOT NULL
    AND p.activated_at<=check_at AND p.period_start<=check_at AND check_at<p.period_end
    AND p.suspension_at IS NULL AND p.revoked_at IS NULL;
  IF n<>1 THEN RAISE EXCEPTION '2027 final-second validity failed'; END IF;
  check_at := make_timestamptz(2028,1,1,0,0,0,'Asia/Hebron');
  SELECT count(*) INTO n FROM public.membership_periods_sandbox p
  WHERE p.membership_year=2027 AND p.period_status='active'
    AND p.activated_at<=check_at AND p.period_start<=check_at AND check_at<p.period_end;
  IF n<>0 THEN RAISE EXCEPTION 'expired 2027 still valid'; END IF;
  SELECT count(*) INTO n FROM public.membership_periods_sandbox p
  WHERE p.membership_year=2028 AND p.period_status='active'
    AND p.fee_decision='waived' AND p.activated_at<=check_at
    AND p.period_start<=check_at AND check_at<p.period_end
    AND p.suspension_at IS NULL AND p.revoked_at IS NULL;
  IF n<>1 THEN RAISE EXCEPTION 'renewed 2028 activation failed'; END IF;

  UPDATE public.membership_periods_sandbox SET suspension_at=check_at
  WHERE membership_year=2028;
  SELECT count(*) INTO n FROM public.membership_periods_sandbox p
  WHERE p.membership_year=2028 AND p.period_status='active'
    AND p.period_start<=check_at AND check_at<p.period_end
    AND p.suspension_at IS NULL AND p.revoked_at IS NULL;
  IF n<>0 THEN RAISE EXCEPTION 'suspended credential still valid'; END IF;
  UPDATE public.membership_periods_sandbox SET suspension_at=NULL,revoked_at=check_at
  WHERE membership_year=2028;
  SELECT count(*) INTO n FROM public.membership_periods_sandbox p
  WHERE p.membership_year=2028 AND p.period_status='active'
    AND p.period_start<=check_at AND check_at<p.period_end
    AND p.suspension_at IS NULL AND p.revoked_at IS NULL;
  IF n<>0 THEN RAISE EXCEPTION 'revoked credential still valid'; END IF;
END $$;
SELECT 'PASS: year rollover, waiver, suspension and revocation boundary predicates' AS result;

