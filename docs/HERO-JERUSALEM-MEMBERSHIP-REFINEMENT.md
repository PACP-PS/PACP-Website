# PACP — Direct implementation instructions (2026-11-16)

Target: `rebuild/platform-foundation/index.html` exclusively. Do not edit alternative homepages or touch production.

**Requested changes and implementation:**
1. Center hero copy: on desktop use headline 40–54px, description 11–14px, max description width 365px, balanced button sizes and spacing; keep Arabic line breaks and RTL legibility; mobile scales 30–39px.
2. Jerusalem hero: use softer elliptical clipping, left-side background fade, subtle depth/drop shadow, and attached layered Palestinian-color ribbon; image remains recognizable.
3. Reverse membership card: move small Jerusalem oval to upper-left of reverse face (image itself must not compete with text), reserve headline block beside it, improve Arabic/English text grid, soften curved stripe, inset frosted barcode/logo panel. Preserve prominent demo/nonvalid notice and original PACP logo.

**Acceptance:**
- Desktop 1648×928 and 1440×900: no overlap among brain, center copy and Jerusalem.
- Mobile 390×844: both hero images visible, text readable, no horizontal overflow.
- Back card: no text collision, neat Jerusalem oval, frosted panel, visible demo notice; front card unchanged.
- Both images loaded; source remains PACP root index; 5 service tiles retained.
- Chromium screenshot comparison against owner reference is required; automated pass is not visual sign-off.
- Production site, DNS, mail and main branch unchanged.

**Implementation commit:** `b4e87a9d7f002340ac0d768560efddb3114f9e09`.
