-- PACP annual membership: ISOLATED SANDBOX REVIEW DRAFT ONLY.
-- DO NOT EXECUTE against PACP-Development, production or existing user data.
-- Assumes existing public.members and auth.users, and pgcrypto/gen_random_uuid().
-- This draft is intentionally OUTSIDE supabase/migrations; it is not a deployment migration.
-- The board-approved bylaws, fee/exemption authority, and rollback strategy are prerequisites.
begin;

create table public.membership_periods_sandbox (
    id uuid primary key default gen_random_uuid(),
    member_id uuid not null references public.members(id) on delete restrict,
    membership_year integer not null check (membership_year between 2020 and 2100),
    period_start timestamptz not null,
    period_end timestamptz not null,
    period_status text not null default 'pending'
        check (period_status in ('pending','active','expired','cancelled')),
    activated_at timestamptz,
    fee_decision text not null default 'pending'
        check (fee_decision in ('pending','settled','waived')),
    fee_decision_reference text,
    suspension_at timestamptz,
    revoked_at timestamptz,
    created_at timestamptz not null default now(),
    updated_at timestamptz not null default now(),
    constraint periods_sandbox_year_unique unique (member_id, membership_year),
    constraint periods_sandbox_positive_length check (period_end > period_start),
    constraint periods_sandbox_activation_check check (
        activated_at is null or (activated_at >= period_start and activated_at < period_end)
    ),
    constraint periods_sandbox_active_requirements check (
        period_status <> 'active' or (
            activated_at is not null
            and fee_decision in ('settled','waived')
            and fee_decision_reference is not null
            and btrim(fee_decision_reference) <> ''
        )
    ),
    constraint periods_sandbox_calendar_bounds check (
        period_start = (make_timestamptz(membership_year,1,1,0,0,0,'Asia/Hebron'))
        and period_end = (make_timestamptz(membership_year + 1,1,1,0,0,0,'Asia/Hebron'))
    )
);
create index membership_periods_sandbox_member_year_idx
    on public.membership_periods_sandbox(member_id,membership_year desc);
alter table public.membership_periods_sandbox enable row level security;
revoke all on table public.membership_periods_sandbox from public, anon, authenticated;
-- No member-facing table policies, no SECURITY DEFINER functions, no QR issuance.
-- This table is not a replacement for statutory member standing or real payments.
-- The boolean eligibility expression is documented below but must be moved to a
-- reviewed, authenticated, owner-scoped server API before any production use.
--
-- eligible :=
--     period_status = 'active'
--     AND fee_decision IN ('settled','waived')
--     AND activated_at <= now()
--     AND period_start <= now() AND now() < period_end
--     AND suspension_at IS NULL AND revoked_at IS NULL
--     AND member is not suspended/revoked
--     AND permanent membership code exists
--
-- In a disposable test project: insert only synthetic accounts and periods;
-- test year boundaries, duplicate year, role privilege denial, suspension,
-- revoked, no settlement, and no membership code.
commit;
