# PACP Phase 2 — reverse-order separation of duties test, 2026-11-18

## Direct test: PASS (simulated JWT claims, not real login)
On Supabase PACP-Staging `aweebuukeovcekctclws`:
- Used existing synthetic auth identities and local request JWT claims for `info@pacp.ps`.
- Within a PL/pgSQL subtransaction created a synthetic submitted application and cash receipt with the admin as cashier.
- Called `public.pacp_review_application` with that same identity and checked that the expected SQLSTATE 42501 and exact `reviewer and cashier must be different users` error occurred.
- Raised a tagged internal exception to **roll back synthetic inserts**, then checked that no test receipt remained.
- Post-test independent query: 1 application, 0 receipts, 0 synthetic receipts, 0 identity records.

This confirms the reversed same-person denial in the database function, complementing previously verified reviewer→cashier denial. This is **not** proof of independent real-JWT UAT, concurrent requests, privileged SQL bypass protection, or any deployment success.

## Existing CI
All six previously available development-branch GitHub Actions workflows completed successfully at commit `8e9c7046aef845f07aaa419c914391c940d20998`.

## Next gates
- Test independent authenticated member/finance/approver/superadmin sessions, positive transition and denial paths.
- Verify Cloudflare Pages staging config without opening private preview pages publicly.
- Verify last live informational Cloudflare deployment and mobile footer/navigation interactively.
- Leave identity collection and payments disabled in production.
