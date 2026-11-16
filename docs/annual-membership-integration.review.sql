-- PACP ANNUAL MEMBERSHIP INTEGRATION -- REVIEW ONLY, DO NOT DEPLOY.
-- Depends on existing public.members(id), public.membership_renewal_requests(id,member_id).
-- Run ONLY in a fresh isolated disposable PostgreSQL environment until sign-off.
BEGIN;
CREATE TABLE public.membership_periods (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  member_id uuid NOT NULL REFERENCES public.members(id) ON DELETE RESTRICT,
  membership_year integer NOT NULL CHECK (membership_year BETWEEN 2020 AND 2100),
  starts_at timestamptz NOT NULL,
  ends_at timestamptz NOT NULL,
  status text NOT NULL DEFAULT 'pending' CHECK(status IN ('pending','active','expired','cancelled')),
  activated_at timestamptz,
  fee_decision text NOT NULL DEFAULT 'pending' CHECK(fee_decision IN ('pending','settled','waived')),
  fee_evidence_reference text,
  suspended_at timestamptz,
  revoked_at timestamptz,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  UNIQUE(member_id,membership_year),
  CHECK(starts_at = make_timestamptz(membership_year,1,1,0,0,0,'Asia/Hebron')),
  CHECK(ends_at = make_timestamptz(membership_year+1,1,1,0,0,0,'Asia/Hebron')),
  CHECK(ends_at>starts_at),
  CHECK(activated_at IS NULL OR (starts_at<=activated_at AND activated_at<ends_at)),
  CHECK(status<>'active' OR
      (activated_at IS NOT NULL AND fee_decision IN ('settled','waived')
       AND nullif(btrim(fee_evidence_reference),'') IS NOT NULL))
);
CREATE INDEX membership_periods_member_year_idx ON public.membership_periods(member_id,membership_year DESC);
ALTER TABLE public.membership_periods ENABLE ROW LEVEL SECURITY;
REVOKE ALL ON public.membership_periods FROM PUBLIC,anon,authenticated;

-- Preserve existing renewal records and their documented state.
-- NULL target year is a backfill/review blocker, not a default year inferred from requested_at.
ALTER TABLE public.membership_renewal_requests ADD COLUMN target_membership_year integer;
ALTER TABLE public.membership_renewal_requests
 ADD CONSTRAINT renewal_target_year_range CHECK(target_membership_year IS NULL OR target_membership_year BETWEEN 2020 AND 2100);
CREATE INDEX renewal_member_target_year_idx
 ON public.membership_renewal_requests(member_id,target_membership_year);
-- Do not backfill existing renewal requests without an authorized historical decision.
-- Before enabling writes, add a trusted transaction that creates/links period rows only
-- after approval + independently verified fee settlement/waiver and an audit log.
-- No client grants, public functions, payment processing, QR or activation included.
COMMIT;
