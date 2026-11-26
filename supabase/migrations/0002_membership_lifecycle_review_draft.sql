-- PACP membership lifecycle extension — REVIEW DRAFT ONLY
-- PostgreSQL / Supabase-compatible. Do not run in production before review.
-- Depends on docs/DATABASE-SCHEMA-DRAFT.sql.
-- This migration adds auditable workflow records; it does not grant client access
-- and intentionally does not implement approval RPCs or membership-code issuance.

create table if not exists public.membership_application_events (
  id uuid primary key default gen_random_uuid(),
  application_id uuid not null references public.membership_applications(id) on delete restrict,
  from_status public.application_status,
  to_status public.application_status not null,
  action text not null check (action in (
    'submitted','assigned','started_review','requested_changes',
    'resubmitted','approved','rejected','withdrawn','note_added'
  )),
  actor_user_id uuid references auth.users(id) on delete set null,
  reason text,
  internal_note text,
  applicant_visible_note text,
  created_at timestamptz not null default now()
);

create index if not exists membership_application_events_app_idx
  on public.membership_application_events(application_id, created_at desc);

create table if not exists public.membership_documents (
  id uuid primary key default gen_random_uuid(),
  application_id uuid not null references public.membership_applications(id) on delete restrict,
  document_type text not null check (document_type in (
    'identity_document','moh_practice_license','academic_certificate',
    'professional_cv','portrait','other'
  )),
  storage_bucket text not null default 'private-membership-documents',
  storage_path text not null,
  original_filename text,
  mime_type text,
  file_size_bytes bigint check (file_size_bytes is null or file_size_bytes > 0),
  uploaded_by uuid references auth.users(id) on delete set null,
  review_status text not null default 'pending'
    check (review_status in ('pending','accepted','rejected','reupload_required')),
  reviewed_by uuid references auth.users(id) on delete set null,
  reviewed_at timestamptz,
  review_note text,
  created_at timestamptz not null default now(),
  unique(storage_bucket, storage_path)
);

create index if not exists membership_documents_app_idx
  on public.membership_documents(application_id, created_at desc);

create table if not exists public.membership_status_history (
  id uuid primary key default gen_random_uuid(),
  member_id uuid not null references public.members(id) on delete restrict,
  from_status public.membership_status,
  to_status public.membership_status not null,
  reason text,
  actor_user_id uuid references auth.users(id) on delete set null,
  effective_at timestamptz not null default now(),
  created_at timestamptz not null default now()
);

create index if not exists membership_status_history_member_idx
  on public.membership_status_history(member_id, effective_at desc);

create table if not exists public.membership_renewal_requests (
  id uuid primary key default gen_random_uuid(),
  member_id uuid not null references public.members(id) on delete restrict,
  requested_membership_type text,
  status text not null default 'submitted'
    check (status in ('submitted','under_review','needs_changes','approved','rejected','withdrawn')),
  requested_at timestamptz not null default now(),
  reviewed_at timestamptz,
  reviewer_id uuid references auth.users(id) on delete set null,
  decision_reason text,
  fee_amount numeric(10,2) check (fee_amount is null or fee_amount >= 0),
  fee_currency char(3) not null default 'ILS',
  payment_status public.payment_status not null default 'not_required',
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create index if not exists membership_renewals_member_idx
  on public.membership_renewal_requests(member_id, requested_at desc);

-- No public/member/staff policies are supplied here. RLS must be enabled and
-- tested for each new table in a disposable Supabase project before any use.
alter table public.membership_application_events enable row level security;
alter table public.membership_documents enable row level security;
alter table public.membership_status_history enable row level security;
alter table public.membership_renewal_requests enable row level security;

comment on table public.membership_application_events is
  'Append-only workflow history; applicant-visible notes must be deliberately curated.';
comment on table public.membership_documents is
  'Private object metadata only. Actual files must live in a private storage bucket.';
comment on table public.membership_status_history is
  'Auditable membership status transitions; never use this as a substitute for authorization.';
comment on table public.membership_renewal_requests is
  'Renewal workflow. Payment remains disabled until provider contracting and verification.';
