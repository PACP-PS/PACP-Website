# PACP integrated preview — how to review

## Start here

Open `design/preview-center.html` from a local HTTP server or a staging web host. It presents a single navigation hub for 12 existing page previews and lets reviewers switch between desktop, tablet and mobile widths.

Example from repository root:

```bash
python3 -m http.server 8080
```

Then visit `http://localhost:8080/design/preview-center.html`.

Do **not** assume a GitHub blob link renders the HTML. GitHub's file viewer displays source code. No public preview deployment is claimed.

## Review checklist

- Branding: approved association logo, official typography and colors.
- Content: replace all provisional mission/vision copy with formally approved text.
- Accessibility: keyboard navigation, RTL/LTR, mobile width, reduced-motion behavior.
- Experience: homepage → membership → application → member portal → digital card.
- Editorial: news/events templates must not be mistaken for actual announcements.
- Administration: dashboards are design previews, not connected to privileged actions.
- Privacy: never enter real IDs or documents into a preview.
- Infrastructure: do not modify live VPS, DNS, MX, SPF, DKIM or DMARC.

## Important distinction

A visually complete prototype is not a functioning member management platform. Authentication, secure storage, eligibility review, card issuance, payment and CPD services require tested backend integration.
