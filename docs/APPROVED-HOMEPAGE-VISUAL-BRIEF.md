# PACP — FINAL APPROVED HOMEPAGE VISUAL IMPLEMENTATION BRIEF
**Status:** Binding design target; implementation NOT yet accepted. **Branch:** `rebuild/platform-foundation`.

## Approved reference
The owner-supplied **1648 × 928** desktop reference image in this conversation (2026-11-15) is the sole visual source of truth. Do not replace it with current Chromium screenshots. Store a reviewed copy in design documentation when image bytes are available for repository ingestion, and record its checksum. Until then verify side by side against the user-supplied image.

### Exact composition to reproduce
1. **Header:** horizontal desktop header; PACP original emblem at top-right beside bilingual identity, nav central, white/login/language controls and red join button at left. Clean high-contrast Arabic Alexandria typography.
2. **Hero:** continuous panoramic triptych across screen. LEFT = **oversized luminous cyan-green brain** with psychology/service floating translucent icons and stage/plinth; CENTER = compact eyebrow, large bold headline “نحو مجتمع نفسي / واعٍ وداعم”, supportive text, two action buttons; RIGHT = **large sweeping arched Jerusalem golden dome panorama**. No large detached white gaps. Three elements must read as ONE composition.
3. **Identity wave:** bold layered red/white/green flowing Palestinian ribbon across lower hero; connective sweep to Jerusalem, not a narrow isolated stripe.
4. **Services:** **FIVE** evenly sized frosted-glass service tiles in a single desktop row, matching the reference's icon weight, positioning and rhythm. No arbitrary 4-card substitute; clarify the duplicated practice label from reference before publishing final content.
5. **Membership:** two premium translucent **glass cards**, front and back side by side, visibly dimensional, strong cyan rim glow, reflection and soft shadow, raised showcase plinth. Treat mock member/QR as DEMO only; never issue or suggest validity.
6. **Bottom bar:** continuous deep-green rounded 4-column member/CPD/courses/PACP navigation band.
7. **Background:** pale cool white/blue glass aesthetic; subtle layered sweeping backdrop and fine highlights. Avoid excessive blank space below fold.

### Mobile-specific design
The approved reference is a DESKTOP image; mobile must be a faithful adaptation, not a shrink-to-fit replica. Logo and menu usable; headline readable; brain and Jerusalem both visible without clipping; service tiles in 2 columns then single column on very small screens; two glass membership cards readable and not overflowing; no horizontal scroll; tab/navigation works.

### Concrete visual sign-off
Capture output at desktop 1648×928 (reference matched), 1440×900, 768×1024, 390×844 and compare side-by-side (identical browser font state).
- BLOCKER: original PACP logo absent, brain/Jerusalem missing, hero columns reordered, failed images/HTTP requests, absent Palestinian ribbon, demo QR presented as real.
- MAJOR: service tile count ≠5 at desktop; non-glass cards, major mismatch in imagery scale, arc/crop, prominent text hierarchy, heavy vertical gaps, broken mobile nav.
- MINOR: shadows, gradients, fine spacing within approved tolerance after visual review.
- Technical pass does NOT imply visual match. Owner review of actual screenshots is mandatory.

### Existing code context (not a new design)
- Root `index.html` is the most similar current implemented hero layout but visually NOT APPROVED.
- `PACP-Reference-Design-Cloudflare-v9/` contains original logo and supporting imagery/pages.
- `scripts/build_public_preview.py` builds the public-safe export; never deploy the alternative nested homepage.
- `scripts/capture_visual_evidence.py` captures real-browser screenshots and checks image loads/layout; these do not yet measure fidelity to the reference.
- Membership, admin, course auth workflows remain separately staged and must not be exposed as complete in public site.

### Release rule
Do not publish to `main`, Cloudflare production or `www.pacp.ps` until the owner has reviewed screenshot evidence and live functional/security acceptance is documented. Keep rollback deployment ID and protect DNS/email.
