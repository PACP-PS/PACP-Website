# PACP — Security, Privacy & Operations Checklist

## Before collecting real personal data
- [ ] Association approves privacy notice, terms, retention schedule, and data-controller contact.
- [ ] Define lawful purpose and minimum required fields for each workflow.
- [ ] Confirm who may view identity documents, finance data, complaints, and reviewer materials.
- [ ] Confirm hosting region, subprocessors, backups, and cross-border data handling.
- [ ] Set retention and secure deletion rules.
- [ ] Establish access request, correction, export, and deletion request process.

## Authentication and authorization
- [ ] Email verification and secure recovery.
- [ ] MFA mandatory for privileged staff.
- [ ] Role-based permissions and object-level authorization.
- [ ] Session expiration, secure cookies, rate limiting, brute-force controls.
- [ ] No shared administrator accounts.

## Files
- [ ] Private storage by default.
- [ ] File type and size allowlist.
- [ ] Malware scanning where available.
- [ ] Short-lived signed URLs after authorization.
- [ ] No public URLs for identity documents or confidential submissions.

## Payments
- [ ] Merchant agreement and provider approval confirmed.
- [ ] Hosted checkout/tokenization; no card PAN/CVV storage.
- [ ] Signed webhook verification and idempotency.
- [ ] Server-side transaction status; browser redirects are not authoritative.
- [ ] Refund, dispute, reconciliation, receipts, and finance reporting tested.
- [ ] Test mode and production credentials separated.

## Operations
- [ ] Separate staging and production.
- [ ] Automated build, type, lint, and security checks.
- [ ] Monitoring and error reporting without sensitive payloads.
- [ ] Encrypted backups and restore test.
- [ ] Incident response and credential rotation procedure.
- [ ] Release checklist and rollback procedure.
- [ ] Accessibility and performance testing, including reduced-motion mode.

## Scope exclusions
The platform is not a clinical record system, therapy platform, crisis line, emergency service, or patient portal. Do not collect patient health records or clinical case details.
