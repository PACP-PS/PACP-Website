# PACP Staging — direct-table access and separation validation (2026-11-18)

## Read-only verified
- `public.pacp_applications`: RLS enabled; authenticated INSERT allowed subject to own-user and submitted-only RLS; authenticated UPDATE revoked. Anonymous UPDATE revoked.
- `public.pacp_cash_receipts`: RLS enabled; authenticated INSERT/UPDATE revoked. Anonymous UPDATE revoked.
- Existing Staging records: 1 membership application, 0 cash receipts, 0 cards; zero reviewer/cashier collisions observed. This last result is **vacuous** because there are no receipts.
- Review and record-cash RPCs each contain guards that reject using the same account for both acts. Card issuance additionally requires distinct reviewer and cashier.

## Critical testing distinction
No real authenticated user session was supplied, and no test payment, card or application was created. Thus **no end-to-end authorization or rollback test was performed**. Direct SQL privilege inspection and function-body inspection do not establish actual runtime success for role-specific or concurrent transactions.

## Remaining checks before platform launch
1. Secure independent member, finance-only and approver-only sessions; validate denial and allowed operations with synthetic applications.
2. Test same-actor denial in both orders, with rollback/cleanup; test role revocation and cross-account object identifiers.
3. Review concurrency/race conditions and privileged bypasses; consider database-side invariant enforced by a well-reviewed trigger, not merely RPC checks.
4. Verify privileged service keys are never exposed; complete staff MFA/password protection and accessibility browser UAT.
5. Promote to production only with explicit approval and rollback plan.

No schema mutation or payment during this inspection.
