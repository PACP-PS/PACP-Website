-- PACP DEV ONLY — REVIEW BEFORE EXECUTION; never apply to production.
-- Least-privilege reconciliation based on live metadata inspected 2026-11-15.
-- This file is intentionally NOT an auto-deployed migration.
begin;
-- Remove high-risk table-level capabilities that should not be browser-accessible.
revoke truncate, trigger, references on all tables in schema public from anon, authenticated;
-- Remove browser write grants where no current RLS write policy exists.
revoke insert, update, delete on public.activities, public.activity_accreditations,
 public.audit_log, public.certificates, public.member_cpd_ledger, public.members,
 public.membership_application_events, public.membership_documents,
 public.membership_renewal_requests, public.membership_status_history,
 public.payment_records, public.profiles, public.registrations,
 public.site_content_entries, public.contact_inquiries,
 public.staff_role_assignments
from anon, authenticated;
-- Membership submissions: authenticated INSERT is allowed by specific ownership policy.
revoke insert, update, delete on public.membership_applications from anon;
revoke update, delete on public.membership_applications from authenticated;
-- Preserve SELECT where policies currently provide it, and preserve authenticated INSERT
-- on membership_applications. New writes require separate reviewed grants + RLS.
commit;
-- After execution verify grants, application submission, approval RPC and security advisors.
