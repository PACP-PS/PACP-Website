# PACP membership card lifecycle — confirmed schema blocker (2026-11-16)

## Directly verified on PACP-Development (read only)
- `public.members.status` uses enum `public.membership_status` with labels: `draft`, `submitted`, `under_review`, `approved`, `rejected`, `suspended`, `expired`.
- **The enum has no `active` or `revoked` value.**
- `public.members` has `approved_at` but no membership activation date or expiration/valid-until field. Therefore the current member summary RPC cannot prove current valid membership or expiry.
- The staging digital card deliberately requires `status==='active'`, so it currently fails closed and cannot present a membership card for any member. This is intentional until a server-enforced activation and validity contract exists.
- Prior GitHub Actions checks at commit `af28fa4576b424128511bf828178e0c4329e31f8` were successful; this does not establish runtime membership validity.

## Proposed policy and technical design — require Board decisions before database migration
1. Confirm legally defined activation trigger, whether approval alone grants membership, initial validity duration and whether membership expires automatically.
2. Define mutually exclusive lifecycle states (e.g. pending/approved_pending_activation/active/suspended/expired/revoked) and ensure legacy status compatibility; do not extend enum until a reviewed migration includes rollback plan and application compatibility.
3. Store authoritative `activated_at`, `valid_until`, `suspended_at`, `revoked_at` as necessary. Derive validity server-side from state AND relevant timestamps, not from client values.
4. Add minimal member-scoped read API exposing `card_eligible` only if active, not expired, not suspended, not revoked, membership code assigned and all policy requirements met. Never leak national ID, email/phone or private documents.
5. Implement a separately audited issuance process plus opaque verification token with revocation and rotation; do not treat QR or static HTML as official membership proof.
6. Test approved-but-inactive, active-unexpired, active-expired, suspended, revoked, missing code, cross-user and admin role cases using real synthetic Auth sessions in isolated staging.
7. Keep preview cards marked DEMO/NOT VALID, and all official issuance disabled until policy, security and UAT sign-off.

## Operational boundary
No SQL migration or production database changes have been applied in this step. No synthetic accounts created. No live membership cards or verification tokens issued.
