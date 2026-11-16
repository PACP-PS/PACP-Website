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


-- Synthetic cross-account RLS test. No production function or Auth users.
ALTER TABLE public.members ADD COLUMN user_id uuid;
UPDATE public.members SET user_id='aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa';
INSERT INTO public.members(id,user_id) VALUES
('22222222-2222-4222-8222-222222222222','bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb');
INSERT INTO public.membership_periods_sandbox(
 member_id,membership_year,period_start,period_end,period_status,
 activated_at,fee_decision,fee_decision_reference)
VALUES (
 '22222222-2222-4222-8222-222222222222',2028,
 make_timestamptz(2028,1,1,0,0,0,'Asia/Hebron'),
 make_timestamptz(2029,1,1,0,0,0,'Asia/Hebron'),
 'active',make_timestamptz(2028,1,1,0,0,0,'Asia/Hebron'),
 'settled','SYNTHETIC-B');
ALTER TABLE public.members ENABLE ROW LEVEL SECURITY;
GRANT SELECT ON public.members TO authenticated;
GRANT SELECT ON public.membership_periods_sandbox TO authenticated;
CREATE POLICY sandbox_own_member ON public.members FOR SELECT TO authenticated
USING (user_id = nullif(current_setting('request.jwt.claim.sub',true),'')::uuid);
CREATE POLICY sandbox_own_period ON public.membership_periods_sandbox FOR SELECT TO authenticated
USING (member_id IN (
 SELECT id FROM public.members WHERE user_id = nullif(current_setting('request.jwt.claim.sub',true),'')::uuid
));
DO $$
DECLARE visible_rows integer;
BEGIN
 PERFORM set_config('request.jwt.claim.sub','aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa',true);
 EXECUTE 'SET LOCAL ROLE authenticated';
 SELECT count(*) INTO visible_rows FROM public.membership_periods_sandbox;
 IF visible_rows<>2 THEN RAISE EXCEPTION 'Account A RLS mismatch %',visible_rows; END IF;
 PERFORM set_config('request.jwt.claim.sub','bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb',true);
 SELECT count(*) INTO visible_rows FROM public.membership_periods_sandbox;
 IF visible_rows<>1 THEN RAISE EXCEPTION 'Account B isolation mismatch %',visible_rows; END IF;
 PERFORM set_config('request.jwt.claim.sub','',true);
 SELECT count(*) INTO visible_rows FROM public.membership_periods_sandbox;
 IF visible_rows<>0 THEN RAISE EXCEPTION 'Anonymous identity leakage'; END IF;
 EXECUTE 'RESET ROLE';
END $$;
SELECT 'PASS: isolated two-account membership period RLS' AS result;

-- Server-side eligibility prototype: invoker-only, caller owns every row through RLS.
-- SQL exists ONLY in this disposable CI database, not Supabase.
ALTER TABLE public.members ADD COLUMN membership_code text;
UPDATE public.members SET membership_code='SYNTHETIC-A' WHERE user_id='aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa';
UPDATE public.members SET membership_code='SYNTHETIC-B' WHERE user_id='bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb';
CREATE SCHEMA sandbox_private;
CREATE FUNCTION sandbox_private.my_card_eligible(p_at timestamptz)
RETURNS boolean LANGUAGE sql STABLE SECURITY INVOKER SET search_path = ''
AS $eligibility$
 SELECT EXISTS (
   SELECT 1 FROM public.membership_periods_sandbox p
   JOIN public.members m ON m.id = p.member_id
   WHERE m.user_id = nullif(current_setting('request.jwt.claim.sub', true),'')::uuid
     AND nullif(btrim(m.membership_code),'') IS NOT NULL
     AND p.period_status = 'active'
     AND p.fee_decision IN ('settled','waived')
     AND nullif(btrim(p.fee_decision_reference),'') IS NOT NULL
     AND p.activated_at <= p_at AND p.period_start <= p_at AND p_at < p.period_end
     AND p.suspension_at IS NULL AND p.revoked_at IS NULL
 )
$eligibility$;
REVOKE ALL ON FUNCTION sandbox_private.my_card_eligible(timestamptz) FROM PUBLIC;
GRANT USAGE ON SCHEMA sandbox_private TO authenticated;
GRANT EXECUTE ON FUNCTION sandbox_private.my_card_eligible(timestamptz) TO authenticated;
DO $$
BEGIN
 PERFORM set_config('request.jwt.claim.sub','aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa',true);
 EXECUTE 'SET LOCAL ROLE authenticated';
 IF NOT sandbox_private.my_card_eligible(make_timestamptz(2027,6,1,0,0,0,'Asia/Hebron')) THEN
   RAISE EXCEPTION 'Account A eligibility denied';
 END IF;
 IF sandbox_private.my_card_eligible(make_timestamptz(2028,1,1,0,0,0,'Asia/Hebron')) THEN
   RAISE EXCEPTION 'Account A revoked renewal was accepted';
 END IF;
 PERFORM set_config('request.jwt.claim.sub','bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb',true);
 IF NOT sandbox_private.my_card_eligible(make_timestamptz(2028,6,1,0,0,0,'Asia/Hebron')) THEN
   RAISE EXCEPTION 'Account B eligible record not returned';
 END IF;
 IF sandbox_private.my_card_eligible(make_timestamptz(2027,6,1,0,0,0,'Asia/Hebron')) THEN
   RAISE EXCEPTION 'Account B received account A period';
 END IF;
 PERFORM set_config('request.jwt.claim.sub','',true);
 IF sandbox_private.my_card_eligible(now()) THEN RAISE EXCEPTION 'Anonymous session eligible'; END IF;
 EXECUTE 'RESET ROLE';
 IF has_function_privilege('anon','sandbox_private.my_card_eligible(timestamptz)','EXECUTE') THEN
   RAISE EXCEPTION 'Anonymous role can execute private function';
 END IF;
END $$;
SELECT 'PASS: authenticated invoker eligibility and cross-account rejection' AS result;

-- Read-only annual renewal summary, scoped to caller by RLS (sandbox only).
CREATE FUNCTION sandbox_private.my_renewal_status(p_at timestamptz)
RETURNS TABLE(membership_year integer, period_end timestamptz, period_status text,
              fee_decision text, renewal_eligible boolean)
LANGUAGE sql STABLE SECURITY INVOKER SET search_path=''
AS $renewal$
 SELECT p.membership_year,p.period_end,p.period_status,p.fee_decision,
   (p.period_status IN ('active','expired') AND p.revoked_at IS NULL
     AND p.suspension_at IS NULL) AS renewal_eligible
 FROM public.membership_periods_sandbox p
 JOIN public.members m ON m.id=p.member_id
 WHERE m.user_id=nullif(current_setting('request.jwt.claim.sub',true),'')::uuid
 ORDER BY p.membership_year DESC
 LIMIT 1
$renewal$;
REVOKE ALL ON FUNCTION sandbox_private.my_renewal_status(timestamptz) FROM PUBLIC;
GRANT EXECUTE ON FUNCTION sandbox_private.my_renewal_status(timestamptz) TO authenticated;
DO $$
DECLARE n integer; y integer;
BEGIN
 PERFORM set_config('request.jwt.claim.sub','aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa',true);
 EXECUTE 'SET LOCAL ROLE authenticated';
 SELECT count(*),max(membership_year) INTO n,y
 FROM sandbox_private.my_renewal_status(make_timestamptz(2028,6,1,0,0,0,'Asia/Hebron'));
 IF n<>1 OR y<>2028 THEN RAISE EXCEPTION 'A summary incorrect'; END IF;
 PERFORM set_config('request.jwt.claim.sub','bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb',true);
 SELECT count(*),max(membership_year) INTO n,y
 FROM sandbox_private.my_renewal_status(make_timestamptz(2028,6,1,0,0,0,'Asia/Hebron'));
 IF n<>1 OR y<>2028 THEN RAISE EXCEPTION 'B summary incorrect'; END IF;
 PERFORM set_config('request.jwt.claim.sub','',true);
 SELECT count(*) INTO n FROM sandbox_private.my_renewal_status(now());
 IF n<>0 THEN RAISE EXCEPTION 'Missing identity disclosed a period'; END IF;
 EXECUTE 'RESET ROLE';
 IF has_function_privilege('anon','sandbox_private.my_renewal_status(timestamptz)','EXECUTE') THEN
   RAISE EXCEPTION 'Anonymous read execute grant found'; END IF;
END $$;
SELECT 'PASS: invoker renewal status is caller-scoped and denied to anon' AS result;
