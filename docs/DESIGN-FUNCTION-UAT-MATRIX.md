# PACP — Design and Functional Acceptance Matrix

**Target branch:** `rebuild/platform-foundation`  
**Canonical source:** `PACP-Reference-Design-Cloudflare-v9/`  
**Exported public build:** `build/pacp-public-preview/`  
**Baseline:** approved PACP homepage screenshots and original association logo (compare against owner's approved references, not legacy root index).  
**Current release decision:** HOLD — no approved visual diff, live role tests, or hosted staging URL.

| ID | Area | Expected acceptance result | How to test | Status |
|---|---|---|---|---|
| V01 | Homepage hero | Matches approved reference layout and the two-part hero | Side-by-side screenshot at 1440px | NOT TESTED |
| V02 | Logo | Original PACP logo, correct proportions and colors | Compare image source and screenshot | CODE SOURCE CHECKED / VISUAL PENDING |
| V03 | 3D brain | Loads, animates, no console errors; graceful static fallback | Chromium network + console + slow connection | NOT TESTED |
| V04 | Arabic typography | Alexandria rendered where specified, no unintentional fallback; readable line heights | Chrome Computed > Rendered fonts | NOT TESTED |
| V05 | RTL | Correct alignment and keyboard focus order | Manual Arabic reading and Tab navigation | NOT TESTED |
| V06 | Images | All displayed images load and are not stretched/cropped | Automated exported asset audit and browser screenshots | PENDING CI |
| V07 | Navigation | Public pages accessible without broken links | Automated exported asset audit + manual clickthrough | PENDING CI |
| V08 | Responsive | 390px, 768px, 1440px; no horizontal overflow | Browser screenshots and scroll test | NOT TESTED |
| V09 | Accessibility | Images have alt; visible focus; adequate contrast; reduced-motion behavior | axe/keyboard/manual | NOT TESTED |
| F01 | Sign-in | Development test accounts authenticate, failures do not leak detail | Supabase Dev browser test | NOT TESTED |
| F02 | Membership submission | Authenticated member can submit exactly as authorized | RPC and audit/log tests | BLOCKED — submission RPC not deployed |
| F03 | Membership approval | Only approved admin role may approve/reject | Negative permission tests | NOT TESTED — review SECURITY DEFINER patches |
| F04 | Member card | Approved member only; valid verification and revocation | End-to-end sandbox test | NOT TESTED live |
| F05 | Courses | Registration, capacity, CPD award and certificate policy | E2E authorized test | NOT TESTED live |
| F06 | Public preview isolation | Staging/admin/auth pages not distributed in public ZIP | Build audit | PENDING CI |
| R01 | Infrastructure | Actual staging URL, TLS, cache headers, no credentials in repo | Hosting and browser inspection | NOT TESTED |
| R02 | Production readiness | Backup/restore, legal notices, privacy, admin audit, owner signoff | Release evidence review | BLOCKED |

**Pass criteria:** all critical V01–V08 and F01–F06 pass or are deliberately removed from launch scope. All FAIL/BLOCKED items need assigned owner, fix commit and dated retest evidence. Never mark a row PASS solely because an HTML link exists or a CI job ran.

## Verified automated rendering evidence (2026-11-16)
- GitHub Actions [run 43935906609](https://github.com/PACP-PS/PACP-Website/actions/runs/43935906609) completed **successfully** at commit `fa851d0b`.
- The `PACP-visual-evidence` artifact exists (ID 14260930004); the public-site archive exists (ID 14258684896).
- Chromium check passed image loading, console errors, viewport overflow, five service tiles, glass treatment and measured central headline bounds at desktop/tablet/mobile/reference widths. These are **automated structural checks, NOT owner's visual sign-off**.
- The exact visual acceptance of the owner-approved homepage and membership reverse remains OPEN; Cloudflare HTTPS preview remains UNVERIFIED.
- Freeze accepted headline text `نحو مجتمع نفسي داعم وواعٍ` pending further owner feedback. Do not rework accepted public layout merely to satisfy a screenshot metric.

## Visual diff procedure
1. Capture approved reference image and a screenshot of *the same page* at 1440×900, 768×1024, 390×844 at 100% zoom.
2. Match viewport, device pixel ratio, font-loading state and browser.
3. Compare hero layout, logo size, card proportions, gradients, imagery, navigation, spacing, typography and RTL line wraps.
4. Log differences: expected vs observed, screenshot pair, severity (blocking/major/minor), GitHub issue, resolved commit.
5. Re-capture after fix, with reviewer approval. No automatic pixel metric alone can certify the intended design.

## Practical browser checks
Chrome/Edge DevTools → Network → Disable cache → reload → filter Img/Font/JS → zero failed asset requests. Elements → Computed → Rendered Fonts: inspect Arabic and Latin samples. Console: zero uncaught errors. Performance: inspect layout shifts and 3D animation on a phone. Test Tab/Shift+Tab, keyboard menus and 200% zoom.

## Release policy
Static public pages can be previewed before member/admin features. **Do not activate real credentials, application submissions, membership QR issuance, approvals, payments or certificates until corresponding live-development permission and security tests pass**. Do not publish to `main` or `www.pacp.ps` without approved reference comparison and signed release evidence.
