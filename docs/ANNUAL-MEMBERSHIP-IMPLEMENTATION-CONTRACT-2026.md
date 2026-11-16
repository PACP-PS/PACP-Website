# PACP — Annual Membership Implementation Contract (review only)
**Based on:** `docs/PACP-ANNUAL-MEMBERSHIP-POLICY-PROPOSAL-2026.md`
**Status:** Not deployed, not an adopted bylaws amendment. No live SQL changes.

## Source of truth
Annual membership period: 1 January 00:00 local to next 1 January 00:00 local (exclusive), based on Palestinian local time `Asia/Hebron`, timestamps persisted as UTC instants. Avoid adding 365 days (leap years and DST). Use independent yearly period rows and a permanent member identifier.

## Required database model for future reviewed migration
`public.membership_periods` (proposed, not existing):
- `id uuid PK`, `member_id uuid FK`, `year integer NOT NULL`, `status` constrained to `pending|active|expired|cancelled`, `starts_at timestamptz`, `ends_at timestamptz` exclusive, `activated_at timestamptz`, `fee_decision` ('settled'|'waived'|'pending'), `decision_reference`, `created_at`, `updated_at`.
- Unique `(member_id,year)`; server-side permissions only. A renewal shall not reset or reuse member identity or issue a new permanent membership code.
- Hold separate suspension/revocation flags or audited restrictions at member level; validity depends on both period and member standing.
- Period boundaries must be generated in Palestinian local time and converted to UTC. They must not be user-submitted.

`members` future additions `activated_at`, `suspended_at`, `revoked_at`; consider deriving current active state rather than letting client mutate enum directly. Current enum does not have active/revoked. Changes must be backward compatible and reversible with an independently reviewed release plan.

## Permission contract
- Applicant: submit and read own curated application; cannot approve or activate.
- Membership officer: inspect and request corrections; cannot approve final decision or activate.
- Membership approver: decide application according to bylaws; approval does not activate membership automatically.
- Finance officer / explicitly authorized waiver officer: certify annual fee settlement or waiver from trusted payment evidence, no client-supplied paid flag.
- Authorized activator (specific role to ratify): execute auditable activation after approval + eligibility + fee settled or waiver + no restrictions.
- Member: read only own period status/renewal eligibility; no direct grant to update period rows.
- Anonymous: never access member base records or credential issuance; only a heavily minimized rate-limited verification interface when approved.

## Card eligibility server contract
Returns *eligible* only when:
- authenticated user owns member record (for self-card),
- member state not suspended/revoked/terminated,
- there exists a period for current local year with status active,
- `now >= starts_at`, `now < ends_at`, `activated_at <= now`,
- fee settlement or valid waiver is recorded,
- a nonempty permanent membership code exists,
- no active disciplinary/legal hold prohibits credential.
Use fail-closed behavior when any required field is unknown. Treat the 1–31 January renewal window as administrative only, never a card-validity extension.

## Card / QR architecture
The member dashboard may show limited status, but an authoritative server credential must be issued via controlled API after eligibility check; never construct official PDF solely with browser state. QR token is a high-entropy, opaque, non-PII credential handle with a digest stored server-side, version and revocation on renewal/reissue. Verification must check current member and period state each time. Public endpoint returns only approved minimal data, never national identity or private contacts.

## Tests before migration or release
- Calendar year end, leap year, year rollover (including time zone), approved-not-activated, inactive/no-payment, waived fee, suspended, revoked, expired, renewed, stale QR, duplicate period, unauthorized activation, concurrent approvals.
- Two different real synthetic Supabase Auth sessions and actual staff role separation in a disposable project. RLS positive AND negative tests; private storage, grants and SECURITY DEFINER audit.
- Test current draft migration dependencies against empty disposable database and ensure rollback and archival preservation. Current existing `public.members` fields do not suffice for this feature; never claim readiness from static CI tests.

## Owner/Board sign-off required
Review the registered PACP bylaws, membership category labels, statutory termination/voting rules, category fees, first-year proration and waiver authority. Reconcile existing `PACPxxxx` numbering at approval with proposed permanent numbering at activation before writing SQL.
