-- PACP platform foundation schema (design draft; review before production)
-- PostgreSQL / Supabase-compatible. No production credentials or personal data belong here.
create extension if not exists pgcrypto;

create type public.membership_status as enum ('draft','submitted','under_review','approved','rejected','suspended','expired');
create type public.application_status as enum ('submitted','under_review','needs_changes','approved','rejected','withdrawn');
create type public.activity_status as enum ('draft','in_review','published','registration_open','registration_closed','in_progress','completed','cancelled','archived');
create type public.registration_status as enum ('submitted','under_review','accepted','waitlisted','rejected','withdrawn','confirmed','attended','absent','completed','not_completed');
create type public.payment_status as enum ('not_required','pending','under_review','paid','failed','refunded','partially_refunded','waived');
create type public.accreditation_status as enum ('draft','proposed','pending_verification','verified','expired','suspended','revoked');

create table public.profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  role text not null default 'member' check (role in ('member','membership_officer','training_manager','finance_officer','attendance_officer','accreditation_officer','auditor','admin')),
  display_name text,
  preferred_language text not null default 'ar' check (preferred_language in ('ar','en')),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table public.members (
  id uuid primary key default gen_random_uuid(),
  user_id uuid unique references auth.users(id) on delete set null,
  membership_code text unique,
  national_id_encrypted text,
  name_ar_first text not null,
  name_ar_father text not null,
  name_ar_grandfather text not null,
  name_ar_family text not null,
  name_en_first text not null,
  name_en_father text not null,
  name_en_grandfather text not null,
  name_en_family text not null,
  email text not null,
  phone text,
  date_of_birth date,
  residence text,
  has_moh_practice_license boolean,
  academic_level text,
  specialty text,
  graduation_year integer check (graduation_year is null or graduation_year between 1950 and 2100),
  workplace text,
  experience_years numeric(4,1) check (experience_years is null or experience_years >= 0),
  portrait_storage_path text,
  membership_type text,
  status public.membership_status not null default 'draft',
  annual_fee numeric(10,2) not null default 100 check (annual_fee >= 0),
  approved_at timestamptz,
  approved_by uuid references auth.users(id) on delete set null,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);
create unique index members_membership_code_unique_nonnull on public.members(membership_code) where membership_code is not null;

create table public.membership_applications (
  id uuid primary key default gen_random_uuid(),
  applicant_user_id uuid references auth.users(id) on delete set null,
  submitted_data jsonb not null,
  status public.application_status not null default 'submitted',
  reviewer_id uuid references auth.users(id) on delete set null,
  review_notes text,
  submitted_at timestamptz not null default now(),
  reviewed_at timestamptz,
  created_member_id uuid references public.members(id) on delete set null
);

create table public.activities (
  id uuid primary key default gen_random_uuid(),
  slug text unique,
  title_ar text not null,
  title_en text,
  description_ar text,
  description_en text,
  activity_type text not null check (activity_type in ('course','workshop','practical_training','webinar','conference','seminar','supervision','other')),
  delivery_mode text not null default 'in_person' check (delivery_mode in ('in_person','online','hybrid')),
  organizer text,
  instructors jsonb not null default '[]'::jsonb,
  venue text,
  online_url text,
  starts_at timestamptz,
  ends_at timestamptz,
  duration_hours numeric(7,2) check (duration_hours is null or duration_hours >= 0),
  capacity integer check (capacity is null or capacity >= 0),
  fee_amount numeric(10,2) not null default 0 check (fee_amount >= 0),
  fee_currency char(3) not null default 'ILS',
  status public.activity_status not null default 'draft',
  registration_opens_at timestamptz,
  registration_closes_at timestamptz,
  completion_requirements jsonb not null default '{}'::jsonb,
  published_at timestamptz,
  created_by uuid references auth.users(id) on delete set null,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table public.activity_accreditations (
  id uuid primary key default gen_random_uuid(),
  activity_id uuid not null references public.activities(id) on delete cascade,
  accrediting_body text not null,
  accreditation_reference text,
  points_proposed numeric(8,2) check (points_proposed is null or points_proposed >= 0),
  points_approved numeric(8,2) check (points_approved is null or points_approved >= 0),
  status public.accreditation_status not null default 'draft',
  issued_at date,
  expires_at date,
  evidence_storage_path text,
  verified_by uuid references auth.users(id) on delete set null,
  verified_at timestamptz,
  verification_notes text,
  created_at timestamptz not null default now(),
  unique(activity_id, accrediting_body, accreditation_reference)
);

create table public.registrations (
  id uuid primary key default gen_random_uuid(),
  activity_id uuid not null references public.activities(id) on delete restrict,
  member_id uuid references public.members(id) on delete set null,
  applicant_user_id uuid references auth.users(id) on delete set null,
  name_ar text not null,
  name_en text not null,
  email text not null,
  phone text,
  registration_status public.registration_status not null default 'submitted',
  payment_status public.payment_status not null default 'not_required',
  accessibility_notes text,
  attendance_hours numeric(7,2) check (attendance_hours is null or attendance_hours >= 0),
  completion_verified boolean not null default false,
  completion_verified_by uuid references auth.users(id) on delete set null,
  completed_at timestamptz,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique(activity_id, applicant_user_id)
);

create table public.payment_records (
  id uuid primary key default gen_random_uuid(),
  registration_id uuid not null references public.registrations(id) on delete restrict,
  provider text,
  provider_transaction_id text,
  amount numeric(10,2) not null check (amount >= 0),
  currency char(3) not null,
  status public.payment_status not null default 'pending',
  payment_method_label text,
  paid_at timestamptz,
  reconciled_by uuid references auth.users(id) on delete set null,
  reconciliation_note text,
  created_at timestamptz not null default now(),
  unique(provider, provider_transaction_id)
);

create table public.certificates (
  id uuid primary key default gen_random_uuid(),
  registration_id uuid not null unique references public.registrations(id) on delete restrict,
  certificate_number text not null unique,
  issued_at timestamptz not null default now(),
  issued_by uuid references auth.users(id) on delete set null,
  revoked_at timestamptz,
  revocation_reason text,
  pdf_storage_path text
);

create table public.member_cpd_ledger (
  id uuid primary key default gen_random_uuid(),
  member_id uuid not null references public.members(id) on delete restrict,
  activity_id uuid not null references public.activities(id) on delete restrict,
  registration_id uuid not null unique references public.registrations(id) on delete restrict,
  accreditation_id uuid references public.activity_accreditations(id) on delete restrict,
  points numeric(8,2) not null check (points >= 0),
  awarded_at timestamptz not null default now(),
  awarded_by uuid references auth.users(id) on delete set null,
  status text not null default 'awarded' check (status in ('awarded','under_review','reversed')),
  reversal_reason text,
  created_at timestamptz not null default now()
);

create table public.audit_log (
  id bigint generated always as identity primary key,
  actor_user_id uuid references auth.users(id) on delete set null,
  action text not null,
  entity_table text not null,
  entity_id text not null,
  reason text,
  before_data jsonb,
  after_data jsonb,
  created_at timestamptz not null default now()
);

create index members_status_idx on public.members(status);
create index activities_status_dates_idx on public.activities(status, starts_at);
create index registrations_activity_status_idx on public.registrations(activity_id, registration_status);
create index cpd_member_awarded_idx on public.member_cpd_ledger(member_id, awarded_at desc);

-- IMPORTANT:
-- 1) Enable RLS on every table before production.
-- 2) Add reviewed, role-specific policies. Do not rely on client-side hiding.
-- 3) Store national IDs and portrait/evidence files in restricted storage; never public buckets.
-- 4) Membership codes must be generated server-side only after approval, using a transaction and uniqueness retry.
-- 5) Payment webhooks must be verified server-side; never trust browser redirects as payment proof.
-- 6) Do not deploy this draft until migrations, RLS policies, validation, backups, and tests are complete.
