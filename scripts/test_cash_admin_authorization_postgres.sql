\set ON_ERROR_STOP on
CREATE ROLE anon NOLOGIN;
CREATE ROLE authenticated NOLOGIN;
CREATE SCHEMA pacp_private;
CREATE TABLE pacp_private.staff_roles(user_id uuid NOT NULL, role text NOT NULL,
 revoked_at timestamptz,PRIMARY KEY(user_id,role));
CREATE TABLE pacp_private.cash_receipts(
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
 member_id uuid NOT NULL,
 receipt_number text NOT NULL UNIQUE,
 amount numeric(12,2) NOT NULL CHECK(amount>0),
 method text NOT NULL DEFAULT 'cash' CHECK(method='cash'),
 verified_by uuid NOT NULL,
 verified_at timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE pacp_private.membership_approvals(
 member_id uuid PRIMARY KEY, approved_by uuid NOT NULL);
INSERT INTO pacp_private.staff_roles(user_id,role) VALUES
 ('aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa','finance'),
 ('bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb','membership_approver');
-- Executable only by authenticated callers; membership and finance verification are separate.
CREATE FUNCTION pacp_private.record_cash_receipt(p_member uuid,p_receipt text,p_amount numeric,p_method text)
RETURNS uuid LANGUAGE plpgsql SECURITY DEFINER SET search_path=''
AS $fn$
DECLARE caller uuid;rid uuid;
BEGIN
 caller:=nullif(pg_catalog.current_setting('request.jwt.claim.sub',true),'')::uuid;
 IF caller IS NULL OR NOT EXISTS (
  SELECT 1 FROM pacp_private.staff_roles r WHERE r.user_id=caller
  AND r.role='finance' AND r.revoked_at IS NULL
 ) THEN RAISE EXCEPTION 'not authorized' USING ERRCODE='42501'; END IF;
 IF p_method <> 'cash' OR p_method IS NULL THEN
  RAISE EXCEPTION 'bank transfer disabled' USING ERRCODE='22023'; END IF;
 IF p_receipt IS NULL OR pg_catalog.length(pg_catalog.btrim(p_receipt))<3 OR p_amount<=0 OR p_amount IS NULL
 THEN RAISE EXCEPTION 'invalid receipt' USING ERRCODE='22023'; END IF;
 INSERT INTO pacp_private.cash_receipts(member_id,receipt_number,amount,method,verified_by)
 VALUES (p_member,p_receipt,p_amount,'cash',caller) RETURNING id INTO rid;
 RETURN rid;
END $fn$;
REVOKE ALL ON SCHEMA pacp_private FROM PUBLIC,anon,authenticated;
REVOKE ALL ON ALL TABLES IN SCHEMA pacp_private FROM PUBLIC,anon,authenticated;
REVOKE ALL ON FUNCTION pacp_private.record_cash_receipt(uuid,text,numeric,text) FROM PUBLIC,anon;
GRANT USAGE ON SCHEMA pacp_private TO authenticated;
GRANT EXECUTE ON FUNCTION pacp_private.record_cash_receipt(uuid,text,numeric,text) TO authenticated;
DO $$
DECLARE n integer;
BEGIN
 PERFORM pg_catalog.set_config('request.jwt.claim.sub','bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb',true);
 EXECUTE 'SET LOCAL ROLE authenticated';
 BEGIN
  PERFORM pacp_private.record_cash_receipt('11111111-1111-4111-8111-111111111111','NOT-FINANCE',10,'cash');
  RAISE EXCEPTION 'approver created cash receipt';
 EXCEPTION WHEN insufficient_privilege THEN NULL; END;
 PERFORM pg_catalog.set_config('request.jwt.claim.sub','aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa',true);
 BEGIN
  PERFORM pacp_private.record_cash_receipt('11111111-1111-4111-8111-111111111111','BANK-REF',10,'bank_transfer');
  RAISE EXCEPTION 'bank transfer accepted';
 EXCEPTION WHEN invalid_parameter_value THEN NULL; END;
 PERFORM pacp_private.record_cash_receipt('11111111-1111-4111-8111-111111111111','PACP-CASH-0001',25,'cash');
 BEGIN
  PERFORM pacp_private.record_cash_receipt('11111111-1111-4111-8111-111111111111','PACP-CASH-0001',25,'cash');
  RAISE EXCEPTION 'duplicate receipt accepted';
 EXCEPTION WHEN unique_violation THEN NULL; END;
 PERFORM pg_catalog.set_config('request.jwt.claim.sub','',true);
 BEGIN
  PERFORM pacp_private.record_cash_receipt('11111111-1111-4111-8111-111111111111','NO-AUTH',25,'cash');
  RAISE EXCEPTION 'unauthenticated caller accepted';
 EXCEPTION WHEN insufficient_privilege THEN NULL; END;
 EXECUTE 'RESET ROLE';
 SELECT count(*) INTO n FROM pacp_private.cash_receipts;
 IF n<>1 THEN RAISE EXCEPTION 'expected exactly one verified cash receipt, got %',n; END IF;
 IF has_function_privilege('anon','pacp_private.record_cash_receipt(uuid,text,numeric,text)','EXECUTE')
 THEN RAISE EXCEPTION 'anon can execute cashier endpoint';END IF;
END $$;
SELECT 'PASS: finance-only cash, bank disabled, duplicate blocked, approver denied' AS result;

-- Invite-only role administration: no self-promotion and no browser-granted roles.
INSERT INTO pacp_private.staff_roles(user_id,role)
VALUES ('cccccccc-cccc-4ccc-8ccc-cccccccccccc','superadmin');
CREATE TABLE pacp_private.staff_invitations(
 email text NOT NULL, role text NOT NULL, requested_by uuid NOT NULL,
 invitation_state text NOT NULL DEFAULT 'pending' CHECK(invitation_state IN ('pending','accepted','revoked')),
 created_at timestamptz NOT NULL DEFAULT now(),
 UNIQUE(email,role,invitation_state),
 CHECK(role IN ('membership_officer','membership_approver','finance','courses_editor','content_editor','read_only_auditor'))
);
CREATE FUNCTION pacp_private.create_staff_invite(p_email text,p_role text)
RETURNS void LANGUAGE plpgsql SECURITY DEFINER SET search_path=''
AS $invite$
DECLARE caller uuid;
BEGIN
 caller:=nullif(pg_catalog.current_setting('request.jwt.claim.sub',true),'')::uuid;
 IF caller IS NULL OR NOT EXISTS
  (SELECT 1 FROM pacp_private.staff_roles WHERE user_id=caller AND role='superadmin' AND revoked_at IS NULL)
 THEN RAISE EXCEPTION 'superadmin required' USING ERRCODE='42501'; END IF;
 IF p_role NOT IN ('membership_officer','membership_approver','finance','courses_editor','content_editor','read_only_auditor')
 OR p_email IS NULL OR pg_catalog.position('@' in p_email)<2
 THEN RAISE EXCEPTION 'invalid invite role/email' USING ERRCODE='22023'; END IF;
 INSERT INTO pacp_private.staff_invitations(email,role,requested_by)
 VALUES(pg_catalog.lower(pg_catalog.btrim(p_email)),p_role,caller);
END $invite$;
REVOKE ALL ON FUNCTION pacp_private.create_staff_invite(text,text) FROM PUBLIC,anon;
GRANT EXECUTE ON FUNCTION pacp_private.create_staff_invite(text,text) TO authenticated;
DO $$
DECLARE n integer;
BEGIN
 PERFORM pg_catalog.set_config('request.jwt.claim.sub','aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa',true);
 EXECUTE 'SET LOCAL ROLE authenticated';
 BEGIN
  PERFORM pacp_private.create_staff_invite('staff@example.invalid','finance');
  RAISE EXCEPTION 'finance user invited a staff user';
 EXCEPTION WHEN insufficient_privilege THEN NULL; END;
 PERFORM pg_catalog.set_config('request.jwt.claim.sub','cccccccc-cccc-4ccc-8ccc-cccccccccccc',true);
 BEGIN
  PERFORM pacp_private.create_staff_invite('self@example.invalid','superadmin');
  RAISE EXCEPTION 'superadmin escalation accepted';
 EXCEPTION WHEN invalid_parameter_value THEN NULL; END;
 PERFORM pacp_private.create_staff_invite('staff@example.invalid','membership_officer');
 PERFORM pg_catalog.set_config('request.jwt.claim.sub','',true);
 BEGIN
  PERFORM pacp_private.create_staff_invite('anon@example.invalid','finance');
  RAISE EXCEPTION 'anonymous invitation accepted';
 EXCEPTION WHEN insufficient_privilege THEN NULL; END;
 EXECUTE 'RESET ROLE';
 SELECT count(*) INTO n FROM pacp_private.staff_invitations;
 IF n<>1 THEN RAISE EXCEPTION 'wrong number of authorized invitations'; END IF;
 IF has_function_privilege('anon','pacp_private.create_staff_invite(text,text)','EXECUTE')
 THEN RAISE EXCEPTION 'anonymous invite function access'; END IF;
END $$;
SELECT 'PASS: invite only by superadmin, no admin self-grants and no anonymous grants' AS result;
