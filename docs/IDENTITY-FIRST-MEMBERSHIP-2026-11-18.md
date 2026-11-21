# PACP Membership identity-first model — 2026-11-18

## Decision
**A person's verified official identity document (document type + number) is the primary *real-world uniqueness criterion*.** The internal database primary key remains a random UUID. Email is secondary, editable contact/login credential, never the underlying person identity.

### Implementation completed
- Updated membership-application preview to explicitly request document *type* and document number as required primary person identifiers, with proper accessible labels and no-real-ID warning.
- Email is clearly labeled as secondary, and a change of verified email does not create a new membership.
- Kept demo form non-operational, and did not add raw identity numbers to existing public tables.

### Data security design (review required before database rollout)
- Do **not** use email as a deduplication key.
- Normalize and verify identity kind and number in a trusted backend, using issuer-specific validation and exceptions for non-Palestinian IDs.
- Use a keyed HMAC-SHA256 fingerprint, secret managed outside browser/source control, to enforce uniqueness on (document type, fingerprint). Plain SHA256 of an ID number is unsafe against guessing.
- Store any scans/raw identity documents only if legally necessary, encrypted in private storage with restricted staff roles, retention/deletion rules and audit trails.
- Keep random UUID as relational PK and opaque member code as public identifier. Never display raw identity number in certificate, card, QR, URL, exported member list or analytics.
- Allow account recovery/email changes only with identity verification and documented manual review; avoid merging records solely because numbers match before confirmation.
- Prevent an applicant from claiming an already registered identifier; respond in a privacy-preserving way and route to manual resolution instead of exposing ownership.
- On verified renewal, link to same identity/person record rather than create a second member.
- Washington Group answers and accommodation requests stay separately protected and must not affect identity uniqueness or membership acceptance.

### Migration status
`security/identity-first-membership-registry-REVIEW-ONLY.sql` is a non-executed design proposal. The live PACP-Staging schema remains unchanged pending approval, secret management, data migration analysis and privacy assessment.

### Authorization continuation
Separate approver/finance separation checks were already demonstrated on the denied same-actor path. Reverse-order, independent real-token UAT and concurrency tests remain open.
