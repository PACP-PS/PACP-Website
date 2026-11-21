\set ON_ERROR_STOP on
CREATE ROLE anon NOLOGIN;
CREATE ROLE authenticated NOLOGIN;
CREATE SCHEMA pacp_private;
CREATE TABLE pacp_private.staff_roles (user_id uuid,role text,revoked_at timestamptz,PRIMARY KEY(user_id,role));
CREATE TABLE pacp_private.memberships (
 member_id uuid PRIMARY KEY,member_user_id uuid NOT NULL,member_code text NOT NULL UNIQUE,
 approved_at timestamptz,approved_by uuid,fee_verified_at timestamptz,fee_verified_by uuid,
 year integer NOT NULL,starts_at timestamptz NOT NULL,ends_at timestamptz NOT NULL,
 activated_at timestamptz,revoked_at timestamptz,suspended_at timestamptz,
 CHECK(ends_at=make_timestamptz(year+1,1,1,0,0,0,'Asia/Hebron')),
 CHECK(starts_at=make_timestamptz(year,1,1,0,0,0,'Asia/Hebron'))
);
CREATE TABLE pacp_private.card_tokens (
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(),member_id uuid NOT NULL REFERENCES pacp_private.memberships(member_id),
 token_hash text NOT NULL UNIQUE,issued_at timestamptz NOT NULL DEFAULT now(),revoked_at timestamptz);
INSERT INTO pacp_private.staff_roles VALUES
 ('aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa','finance',NULL),
 ('bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb','membership_approver',NULL);
INSERT INTO pacp_private.memberships VALUES(
 '11111111-1111-4111-8111-111111111111','dddddddd-dddd-4ddd-8ddd-dddddddddddd','PACP-TEST-0001',
 make_timestamptz(2028,1,1,0,0,0,'Asia/Hebron'),'bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb',
 make_timestamptz(2028,1,1,0,0,0,'Asia/Hebron'),'aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa',
 2028,make_timestamptz(2028,1,1,0,0,0,'Asia/Hebron'),make_timestamptz(2029,1,1,0,0,0,'Asia/Hebron'),
 NULL,NULL,NULL);
CREATE FUNCTION pacp_private.activate_member(p_member uuid,p_when timestamptz)
RETURNS boolean LANGUAGE plpgsql SECURITY DEFINER SET search_path=''
AS $fn$
DECLARE caller uuid;
BEGIN
 caller:=nullif(pg_catalog.current_setting('request.jwt.claim.sub',true),'')::uuid;
 IF caller IS NULL OR NOT EXISTS (SELECT 1 FROM pacp_private.staff_roles WHERE user_id=caller AND role='membership_approver' AND revoked_at IS NULL)
 THEN RAISE EXCEPTION 'not approver' USING ERRCODE='42501';END IF;
 UPDATE pacp_private.memberships SET activated_at=p_when
 WHERE member_id=p_member AND activated_at IS NULL
 AND p_when>=starts_at AND p_when<ends_at AND approved_at IS NOT NULL
 AND fee_verified_at IS NOT NULL AND approved_by<>fee_verified_by
 AND revoked_at IS NULL AND suspended_at IS NULL;
 RETURN FOUND;
END $fn$;
CREATE FUNCTION pacp_private.card_valid(p_hash text,p_at timestamptz)
RETURNS boolean LANGUAGE sql STABLE SECURITY INVOKER SET search_path=''
AS $fn$
 SELECT EXISTS(
 SELECT 1 FROM pacp_private.card_tokens t JOIN pacp_private.memberships m ON m.member_id=t.member_id
 WHERE t.token_hash=p_hash AND t.revoked_at IS NULL AND m.activated_at IS NOT NULL
 AND m.approved_at IS NOT NULL AND m.fee_verified_at IS NOT NULL
 AND m.revoked_at IS NULL AND m.suspended_at IS NULL
 AND p_at>=m.starts_at AND p_at<m.ends_at)
$fn$;
REVOKE ALL ON SCHEMA pacp_private FROM PUBLIC,anon,authenticated;
REVOKE ALL ON ALL TABLES IN SCHEMA pacp_private FROM PUBLIC,anon,authenticated;
REVOKE ALL ON FUNCTION pacp_private.activate_member(uuid,timestamptz) FROM PUBLIC,anon;
GRANT USAGE ON SCHEMA pacp_private TO authenticated;
GRANT EXECUTE ON FUNCTION pacp_private.activate_member(uuid,timestamptz) TO authenticated;
DO $$
DECLARE ok boolean; m uuid:='11111111-1111-4111-8111-111111111111';
BEGIN
 PERFORM pg_catalog.set_config('request.jwt.claim.sub','aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa',true);
 EXECUTE 'SET LOCAL ROLE authenticated';
 BEGIN
  PERFORM pacp_private.activate_member(m,make_timestamptz(2028,1,2,0,0,0,'Asia/Hebron'));
  RAISE EXCEPTION 'finance activated card';
 EXCEPTION WHEN insufficient_privilege THEN NULL; END;
 PERFORM pg_catalog.set_config('request.jwt.claim.sub','bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb',true);
 SELECT pacp_private.activate_member(m,make_timestamptz(2028,1,2,0,0,0,'Asia/Hebron')) INTO ok;
 IF NOT ok THEN RAISE EXCEPTION 'valid approval denied';END IF;
 EXECUTE 'RESET ROLE';
 INSERT INTO pacp_private.card_tokens(member_id,token_hash) VALUES(m,'TEST_HASH_NOT_A_REAL_QR');
 IF NOT pacp_private.card_valid('TEST_HASH_NOT_A_REAL_QR',make_timestamptz(2028,6,1,0,0,0,'Asia/Hebron'))
 THEN RAISE EXCEPTION 'valid test token rejected';END IF;
 IF pacp_private.card_valid('TEST_HASH_NOT_A_REAL_QR',make_timestamptz(2029,1,1,0,0,0,'Asia/Hebron'))
 THEN RAISE EXCEPTION 'expired card accepted';END IF;
 UPDATE pacp_private.memberships SET suspended_at=now() WHERE member_id=m;
 IF pacp_private.card_valid('TEST_HASH_NOT_A_REAL_QR',make_timestamptz(2028,6,1,0,0,0,'Asia/Hebron'))
 THEN RAISE EXCEPTION 'suspended card accepted';END IF;
 UPDATE pacp_private.memberships SET suspended_at=NULL WHERE member_id=m;
 UPDATE pacp_private.card_tokens SET revoked_at=now();
 IF pacp_private.card_valid('TEST_HASH_NOT_A_REAL_QR',make_timestamptz(2028,6,1,0,0,0,'Asia/Hebron'))
 THEN RAISE EXCEPTION 'revoked QR accepted';END IF;
END $$;
SELECT 'PASS: segregated activation, annual expiry, suspension, QR revocation' AS result;

-- Security regression: no public read access to private membership and token metadata.
DO $$
BEGIN
 IF has_table_privilege('anon','pacp_private.memberships','SELECT')
 OR has_table_privilege('authenticated','pacp_private.memberships','SELECT')
 OR has_table_privilege('anon','pacp_private.card_tokens','SELECT')
 OR has_table_privilege('authenticated','pacp_private.card_tokens','SELECT') THEN
   RAISE EXCEPTION 'private membership or QR token metadata exposed'; END IF;
 IF has_function_privilege('anon','pacp_private.activate_member(uuid,timestamptz)','EXECUTE') THEN
   RAISE EXCEPTION 'anonymous user can activate membership'; END IF;
END $$;
-- Separate finance and approver identities remain necessary; a single person cannot perform both.
UPDATE pacp_private.memberships SET
 activated_at=NULL,approved_by='aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa',
 fee_verified_by='aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa',
 suspended_at=NULL,revoked_at=NULL;
DO $$
DECLARE worked boolean;
BEGIN
 PERFORM pg_catalog.set_config('request.jwt.claim.sub','bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb',true);
 EXECUTE 'SET LOCAL ROLE authenticated';
 SELECT pacp_private.activate_member(
 '11111111-1111-4111-8111-111111111111',
 make_timestamptz(2028,1,2,0,0,0,'Asia/Hebron')) INTO worked;
 IF worked THEN RAISE EXCEPTION 'self-verified approval unexpectedly activated'; END IF;
 EXECUTE 'RESET ROLE';
END $$;
SELECT 'PASS: private metadata not public and split approval/payment mandatory' AS result;

-- Extra deny-by-default cases: expired period cannot be newly activated,
-- a revoked membership fails validation even with an unrevoked token.
DO $$
DECLARE m uuid:='11111111-1111-4111-8111-111111111111'; worked boolean;
BEGIN
 UPDATE pacp_private.memberships
 SET approved_by='bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb',
 fee_verified_by='aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa',
 activated_at=NULL,suspended_at=NULL,revoked_at=NULL WHERE member_id=m;
 PERFORM pg_catalog.set_config('request.jwt.claim.sub','bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb',true);
 EXECUTE 'SET LOCAL ROLE authenticated';
 SELECT pacp_private.activate_member(m,make_timestamptz(2029,1,1,0,0,0,'Asia/Hebron')) INTO worked;
 IF worked THEN RAISE EXCEPTION 'new activation of expired period accepted';END IF;
 SELECT pacp_private.activate_member(m,make_timestamptz(2028,2,1,0,0,0,'Asia/Hebron')) INTO worked;
 IF NOT worked THEN RAISE EXCEPTION 'approved and paid membership not activated';END IF;
 EXECUTE 'RESET ROLE';
 UPDATE pacp_private.card_tokens SET revoked_at=NULL WHERE member_id=m;
 UPDATE pacp_private.memberships SET revoked_at=now() WHERE member_id=m;
 IF pacp_private.card_valid('TEST_HASH_NOT_A_REAL_QR',make_timestamptz(2028,6,1,0,0,0,'Asia/Hebron'))
 THEN RAISE EXCEPTION 'revoked membership validates token';END IF;
END $$;
SELECT 'PASS: no expired activation and revoked membership always fails QR validation' AS result;
