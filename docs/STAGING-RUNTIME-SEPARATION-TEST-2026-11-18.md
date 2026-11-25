# PACP Staging — negative finance-control runtime verification (2026-11-18)

## Test performed
- Target: PACP-Staging project `aweebuukeovcekctclws`.
- Existing approved synthetic application previously reviewed by `info@pacp.ps`.
- Executed `pacp_record_cash` in a SQL `DO` test block with locally simulated authenticated JWT subject equal to the reviewer and a distinct test receipt identifier.
- Expected exception: SQLSTATE `42501`, exact message `reviewer and cashier must be different users`.
- The test block **completed successfully only after checking the expected denial reason**. A different denial reason or unexpected success would have failed the block.
- Post-check confirmed 0 cash receipts, 0 test receipts and unchanged 1 application.
- No transaction/payment/application was created by the test.

## Interpretation
PASS: database-function negative path blocks a reviewer from cash-verifying the same application, even when that account carries both permissions. This tests the actual function with a simulated claims context. It is **not** independent JWT login UAT, positive separate-cashier success, or two-direction verification.

## Remaining
1. Separate identity JWT real-auth tests and positive path under secure test runner.
2. Reverse-order negative check (cash verifier attempts approval), preferably on fully synthetic rollback data.
3. Concurrent transaction + privileged bypass review, audit trail, and accessibility browser UAT.
4. Review production promotion only after explicit signoff.
