-- PACP public content and inquiries — REVIEW DRAFT ONLY
-- No production deployment; no public insert policies for contact inquiries.
begin;
create table if not exists public.site_content_entries (
 id uuid primary key default gen_random_uuid(),
 slug text not null unique check (slug ~ '^[a-z0-9]+(-[a-z0-9]+)*$'),
 content_type text not null check(content_type in ('news','event','resource','page')),
 title_ar text not null check(length(btrim(title_ar)) between 3 and 250),
 title_en text,
 summary_ar text,
 summary_en text,
 body_ar text,
 body_en text,
 status text not null default 'draft' check(status in ('draft','review','published','archived')),
 published_at timestamptz,
 event_starts_at timestamptz,
 event_ends_at timestamptz,
 created_by uuid references auth.users(id) on delete set null,
 updated_by uuid references auth.users(id) on delete set null,
 created_at timestamptz not null default now(),
 updated_at timestamptz not null default now(),
 constraint valid_event_window check(event_ends_at is null or event_starts_at is null or event_ends_at>=event_starts_at),
 constraint published_requires_timestamp check(status <> 'published' or published_at is not null)
);
create index if not exists site_content_public_idx on public.site_content_entries(content_type,published_at desc) where status='published';
alter table public.site_content_entries enable row level security;
create policy site_content_public_published_read
 on public.site_content_entries for select to anon,authenticated
 using (status='published' and published_at <= now());
-- No direct client INSERT/UPDATE/DELETE. Admin publishing requires a
-- separately audited, permissioned workflow.
create table if not exists public.contact_inquiries (
 id uuid primary key default gen_random_uuid(),
 topic text not null check(topic in ('membership','training','partnership','general')),
 sender_name text,
 sender_email text,
 message text not null check(length(btrim(message)) between 10 and 2000),
 status text not null default 'new' check(status in ('new','in_progress','resolved','closed')),
 created_at timestamptz not null default now(),
 assigned_to uuid references auth.users(id) on delete set null
);
alter table public.contact_inquiries enable row level security;
-- NO PUBLIC INSERT: contact form currently opens mailto only.
-- Future server endpoint must add rate limits, abuse prevention, consent,
-- retention and restricted staff access before enabling stored inquiries.
revoke all on public.contact_inquiries from anon,authenticated;
commit;
-- Verify migration compatibility, privileges, function owners, and privacy
-- on a disposable Supabase project before any deployment.
