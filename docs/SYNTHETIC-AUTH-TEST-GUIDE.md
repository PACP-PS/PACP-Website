# PACP synthetic-account authorization smoke test

**Manual, read-only, development only. Not part of CI**, as test JWTs are short-lived secrets.

## Preconditions
- Obtain two **synthetic**, nonstaff, independently authenticated Supabase test accounts A and B.
- Ensure each account already owns a distinct synthetic application through a separately approved test setup.
- Do not use actual members, documents, payment data, or production tokens.
- Prepare a secure private terminal with `PACP_SUPABASE_URL`, `PACP_PUBLISHABLE_KEY`,
  `PACP_TEST_A_JWT`, and `PACP_TEST_B_JWT`. Never commit or print these values.
- Run `python3 scripts/test_member_auth_live_readonly.py` from repository root.

## Pass conditions
1. Both tokens identify different authenticated users.
2. Each retrieves its own application list from `my_membership_applications`.
3. Both application lists are non-empty and their application IDs do not overlap.
4. Both nonstaff tokens receive a denied response from `membership_review_queue`.

## Interpretation
- A pass proves only this narrow sampled read-only behavior.
- A failure or empty dataset is NOT a pass; fix the account fixture before testing again.
- This does **not** test directly querying another person's row by ID, admin authorization,
  issuing memberships, authenticated email flows, private storage, or mutations.
- The test itself performs no writes. Provisioning synthetic fixtures requires separate review.
- Do not enable the submission page or merge to production based solely on this result.
