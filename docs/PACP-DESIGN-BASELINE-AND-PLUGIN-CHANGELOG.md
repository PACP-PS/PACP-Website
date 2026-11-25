# PACP — Design baseline and integration change register

Status: development-only documentation, 2026-11-17. Production remains unchanged by this document.

## Approved canonical visual identity
- Original PACP logo (source: `PACP-Reference-Design-Cloudflare-v9/assets/pacp-logo-original.png`).
- Three-column desktop hero: brain illustration on the left, association introduction in the centre, Jerusalem image on the right.
- Arabic-first RTL presentation with clear typography and five service tiles.
- Two styled membership card faces, but no issuance or payment functionality in public build.
- Public preview generated exclusively using `scripts/build_public_preview.py`, not the alternate v9 homepage.

## What is verified
- Latest design-source revision checked: `9947fae3` on `rebuild/platform-foundation`.
- GitHub visual evidence workflow renders at 1648px, 1440px, 768px, 390px; checks image loading, hero elements, text overflow, JS errors and responsive overflow. This is structural QA, not a full pixel-difference approval.
- Public production dashboard previously reported active project/domain SSL; production content was not replaced in this step.
- Some public website content remains editorially provisional; no claims of final approval.

## Design integration status
- GitHub and Cloudflare connections are available for repository/deployment inspection.
- No Figma/Adobe/other design-tool-generated file was imported into the canonical homepage as part of these updates.
- Simply enabling or connecting a design plugin does **not** alter the PACP website.
- Do not claim a design change without a concrete Git commit diff, exported assets, or a verified deployed page.

## Mandatory change register for future Figma/Adobe/plugin contributions
Record: tool/source; date; branch; changed files; before/after snapshots (desktop and mobile); logo preservation; RTL checks; impact on layout/typography/colour/animations/performance/accessibility; approval; deployment status.

## Release boundary
Do not merge or deploy design/plugin changes to production automatically. Preserve the official logo and the approved hero arrangement. Keep staging admin, applications, auth, payments and cards out of public artifact until separate authorization and end-to-end verification.
