\set ON_ERROR_STOP on
CREATE ROLE anon NOLOGIN;
CREATE ROLE authenticated NOLOGIN;
CREATE TABLE public.members(id uuid PRIMARY KEY);
CREATE TABLE public.membership_renewal_requests(
 id uuid PRIMARY KEY, member_id uuid NOT NULL REFERENCES public.members(id),
 status text NOT NULL,requested_at timestamptz NOT NULL DEFAULT now()
);
INSERT INTO public.members VALUES('11111111-1111-4111-8111-111111111111');
INSERT INTO public.membership_renewal_requests(id,member_id,status)
 VALUES('33333333-3333-4333-8333-333333333333','11111111-1111-4111-8111-111111111111','submitted');
\i docs/annual-membership-integration.review.sql
DO $$
DECLARE m uuid:='11111111-1111-4111-8111-111111111111';
BEGIN
 IF (SELECT count(*) FROM public.membership_renewal_requests WHERE status='submitted' AND target_membership_year IS NULL)<>1 THEN
  RAISE EXCEPTION 'Existing renewal record was not preserved';
 END IF;
 UPDATE public.membership_renewal_requests SET target_membership_year=2028;
 INSERT INTO public.membership_periods(member_id,membership_year,starts_at,ends_at,status,activated_at,fee_decision,fee_evidence_reference)
 VALUES(m,2028,make_timestamptz(2028,1,1,0,0,0,'Asia/Hebron'),make_timestamptz(2029,1,1,0,0,0,'Asia/Hebron'),
 'active',make_timestamptz(2028,1,1,0,0,0,'Asia/Hebron'),'waived','TEST-WAIVER');
 BEGIN
  INSERT INTO public.membership_periods(member_id,membership_year,starts_at,ends_at)
  VALUES(m,2028,make_timestamptz(2028,1,1,0,0,0,'Asia/Hebron'),make_timestamptz(2029,1,1,0,0,0,'Asia/Hebron'));
  RAISE EXCEPTION 'Duplicate period not blocked';
 EXCEPTION WHEN unique_violation THEN NULL; END;
 BEGIN
  INSERT INTO public.membership_periods(member_id,membership_year,starts_at,ends_at,status,activated_at)
  VALUES(m,2029,make_timestamptz(2029,1,1,0,0,0,'Asia/Hebron'),make_timestamptz(2030,1,1,0,0,0,'Asia/Hebron'),
  'active',make_timestamptz(2029,1,1,0,0,0,'Asia/Hebron'));
  RAISE EXCEPTION 'Unpaid period activated';
 EXCEPTION WHEN check_violation THEN NULL; END;
 IF has_table_privilege('anon','public.membership_periods','SELECT')
 OR has_table_privilege('authenticated','public.membership_periods','SELECT') THEN
  RAISE EXCEPTION 'Read grant too broad';
 END IF;
END $$;
SELECT 'PASS: existing renewal preserved, year binding, strict membership validity and deny default' AS result;
