-- PACP identity-first membership registry — REVIEW ONLY, NOT DEPLOYED.
-- Preconditions: approve privacy impact assessment, design applicant verification and
-- secure trusted-server identity fingerprinting (HMAC-SHA256 with secret outside DB/frontend).
-- Do not use unsalted SHA256 for predictable ID values.
begin;
create schema if not exists pacp_identity_private;
revoke all on schema pacp_identity_private from public, anon, authenticated;
create table if not exists pacp_identity_private.member_identity_registry (
 id uuid primary key default gen_random_uuid(),
 identity_document_type text not null check (identity_document_type in ('palestinian_id','passport','other')),
 identity_fingerprint text not null check (identity_fingerprint ~ '^[0-9a-f]{64}$'),
 member_user_id uuid unique references auth.users(id),
 verified_at timestamptz,
 created_at timestamptz not null default now(),
 unique (identity_document_type, identity_fingerprint)
);
alter table pacp_identity_private.member_identity_registry enable row level security;
revoke all on pacp_identity_private.member_identity_registry from public, anon, authenticated;
comment on table pacp_identity_private.member_identity_registry is
 'Restricted mapping of trusted-server HMAC identity fingerprint to member user; never store ID plaintext or expose in Data API.';
commit;
