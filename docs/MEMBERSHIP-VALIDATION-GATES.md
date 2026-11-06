# PACP membership submission validation gate

**Status:** review draft; not deployed or executed.

## Purpose

A syntactically valid application is not necessarily eligible for membership. Keep four independent gates:

1. **Shape:** JSON object, required bilingual four-part names, email, field types and lengths.
2. **Identity and consent:** authenticated owner, verified email, required privacy notices and consent, duplicates reviewed.
3. **Professional eligibility:** membership category, academic qualification, MOH license policy and approved bylaws.
4. **Documents and decision:** required files present in private storage, staff review status accepted, authorized approver and reason.

The new `0006_membership_payload_shape_review_draft.sql` only implements a limited **shape checker**. It does not enforce the other gates.

## Required integration work

- Map exact keys from the finalized public form to the schema; reject unknown/unsupported keys where appropriate.
- Build a trusted `submit_membership_application` endpoint that verifies `auth.uid()`, shape, and permitted state transitions.
- Prevent direct unaudited application inserts and edits from bypassing the endpoint.
- Make the approval transaction refuse to proceed until documented professional eligibility and document checks are satisfied.
- Ensure national ID handling uses reviewed encryption; never store plaintext under a misleading column name.
- Do not auto-approve based on a self-declared MOH practice-license checkbox.
- Add fabricated-data tests for missing bilingual names, invalid types, oversized payloads, duplicate applicants, document rejection, forged reviewer claims, and concurrent approval.

## Deployment and governance

Infrastructure provider reports domain points to VPS; hosting architecture must be verified before staging. No change to DNS, mail, VPS or production is part of this work.
