# PACP Identity Registry — Staging implementation evidence (2026-11-18)

## Confirmed
- All six GitHub sandbox and prelaunch workflows at commit `260e2406c8f350e349440d76c88e66b7cb644819` completed successfully, including prelaunch guardrails run https://github.com/PACP-PS/PACP-Website/actions/runs/44356465509.
- Supabase Staging `aweebuukeovcekctclws`: migration `create_private_identity_registry_staging` applied.
- Private schema `pacp_identity_private` contains `member_identity_registry`, with document type, keyed identity fingerprint placeholder, unique (document type,fingerprint), optional unique member_user_id and verified_at.
- Row-level security enabled. `anon` has no SELECT, `authenticated` has no SELECT or INSERT. Table not in public exposed schema.
- Synthetic duplicate insert tested inside an exception-handled subtransaction: unique constraint rejected duplicate; subsequent count 0. No personal identity or test record retained.
- Existing public membership application(s) untouched; no user identity linkage, raw ID collection, staff role alteration or production deployment.

## Privacy and release gate
- The registry contains **no HMAC secret and no generator yet**; do not send raw ID to the browser-available database API.
- Trusted server/edge integration must normalize document types/numbers, generate HMAC-SHA256 using a protected secret, and limit authorization to restricted identity-verification workflow.
- Confirm retention, legitimate purpose, access audits, collision handling, verified record merge and account recovery before enabling submission.
- Member UUID remains the internal reference; email secondary contact.
- Live JWT role tests, actual accessibility browser assessment, production approval remain outstanding.

**Outcome: staging schema + constraint test PASSED; operational identity registration NOT LIVE.**
