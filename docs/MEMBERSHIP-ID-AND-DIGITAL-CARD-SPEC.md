# PACP Membership Identity and Digital Card Specification

## Membership number
- Generate the public membership number only after the membership application has been formally approved and the membership is activated.
- Format: `PACP-YYYY-NNNN` (example: `PACP-2026-0001`). `YYYY` is the activation year; `NNNN` is a sequential, zero-padded counter scoped to the year.
- The sequence must be allocated transactionally in the database with a unique constraint. Never generate it in the browser and never accept a user-supplied number.
- A rejected, withdrawn, duplicate or incomplete application does not consume an active membership number unless the Board-approved numbering policy explicitly requires it.
- Do not encode the national ID number, date of birth, phone number or other personal data into the membership number or QR payload.
- The national ID is associated with the membership record as a separately encrypted, access-controlled identity attribute, with a normalized keyed fingerprint/HMAC only if needed for duplicate detection. Do not use a reversible or visible national-ID-derived code.
- A membership number remains an internal association identifier. A public verification QR should contain a random opaque token or signed verification URL, not the national ID or the database row ID.

## Proposed data fields
### Applicant / member
- legal full name (four-part name)
- national ID / identity document number (encrypted at rest; restricted access)
- date of birth
- nationality
- residence governorate / city and detailed address
- phone and email
- statutory membership category (unaltered legal value)
- public display label (configurable Arabic and English)
- academic level (controlled vocabulary)
- latest degree's specific discipline (free text)
- graduation year
- Ministry of Health Palestinian professional-practice licence: yes / no / pending
- licence number and expiry/verification metadata only where applicable and approved
- workplace category (controlled vocabulary) and workplace name / department / job title (optional)
- years-of-experience band
- personal photo (private object storage; approved image used on card)
- application status, Board decision reference/date, activation date, renewal date and payment status

### Membership card
- membership number
- member's approved name
- approved professional specialization / academic field
- approved profile photo
- category label and membership status
- join/activation date and expiry/renewal date if applicable
- association logo and official brand assets
- opaque QR verification token
- card issue date and version/revocation status

## Digital card visibility and lifecycle
- The card is not available to the applicant while the request is pending.
- After formal approval and activation, the member account displays a prominent "View / Download Membership Card" action.
- Card status is checked server-side on every verification; revoked, expired or suspended cards must not display as active.
- The QR verification page reveals only minimum public data: member name (subject to approved policy), membership number, category label, and current status. Never reveal national ID, date of birth, private address, phone, email, licence number, or uploaded documents.
- Support print-ready PDF and mobile wallet-friendly view in a later implementation phase.
- The card preview in the current prototype is illustrative only and must never be mistaken for a real credential.

## Form UX and validation
- Academic level: dropdown; exact discipline: free text; graduation year: four-digit year with sensible bounds.
- Workplace category: dropdown with "Other" and a conditional free-text field.
- Years of experience: dropdown bands; consider a separate exact numeric field only if the association has an operational need.
- Practice licence: Yes / No / Pending. Show licence number and evidence upload only for Yes/Pending, if the Board approves collecting evidence.
- Personal photo: JPEG/PNG/WebP, recommended 2 MB maximum, private upload, image preview, clear consent and replacement/delete route.
- National ID is required only to the extent confirmed by the bylaws and legal/privacy review; collect it over HTTPS and store encrypted. Do not use it as the public membership number.
- Residence should be separated into governorate/city and detailed address.
- Date of birth should be validated against statutory minimum age at server side.
- All validation and authorization must be enforced server-side, not only in browser JavaScript.

## Governance and policy confirmations
Before production, the association must approve:
1. Exact membership-number format and whether sequence resets annually.
2. Whether the membership number is issued at approval or activation (this specification recommends activation).
3. Required identity data and verification method.
4. Whether licence possession is an eligibility requirement, a category-specific requirement, or informational only.
5. Academic qualification requirements for each statutory category.
6. Workplace and experience fields as required vs optional.
7. Photo use, retention and consent terms.
8. Which member attributes may appear on the digital card and QR verification page.
9. Card validity period, renewal, suspension and revocation process.
10. Whether electronic membership cards have formal evidentiary status under association decisions.

## Current prototype status
The design preview now includes the requested fields and a client-side sample card toggle. It does not save or transmit any data, create real member numbers, verify identity or licence, generate a real QR code, or issue valid cards. All live functions require the secure application backend and approved policies.
