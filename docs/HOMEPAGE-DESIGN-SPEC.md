# PACP Homepage — Visual Design Specification

Status: Direction approved by the association representative based on the supplied homepage reference image. This document describes the target design; it is not yet an implemented or deployed webpage.

## 1. Design intent
Create a polished, institutional, bilingual homepage for the Palestinian Association of Clinical Psychologists. Match the supplied reference's visual hierarchy and Palestinian identity while ensuring that the website is responsive, accessible, fast, and genuinely interactive.

## 2. Brand system
- Use the official PACP emblem supplied by the association as the source of truth. Preserve aspect ratio, clear space and original colors; do not recreate or distort it.
- Core palette: deep association green, supporting leaf green, Palestinian red, near-black, white and pale neutral backgrounds. Exact tokens should be sampled from the official logo asset during implementation.
- Typography: Arabic-first readable typeface with strong screen legibility; pair with a compatible English family. Load optimized local/web font files where licensing permits.
- Tagline: “نحو مجتمع نفسي واعٍ وداعم” / “Towards a mentally aware and supportive society”.
- Institutional tone: credible, calm, welcoming, professional; avoid clinical-treatment claims or crisis-service positioning.

## 3. Desktop composition (reference-led)
1. Slim deep-green utility bar:
   - location label, official email and phone
   - approved social media links
   - short tagline / identity note
2. Main header:
   - official emblem and bilingual association name
   - primary navigation
   - search field
   - language switch
3. Hero section:
   - wide scenic composition inspired by the reference
   - right/center: Arabic association name, tagline and concise mission statement
   - left: symbolic 3D mental-wellbeing artwork (brain/leaf/heart motif) with tasteful Palestinian identity accents
   - optional Jerusalem / Palestine visual context only where imagery is accurate, licensed and appropriate
   - primary CTA: “تعرّف على الجمعية”
   - secondary CTA: “انتسب إلى الجمعية”
   - accessible carousel controls only if multiple approved hero messages exist; otherwise use a single stable hero
4. Six priority/service tiles:
   - professional standards
   - support for specialists
   - research
   - training and continuing development
   - partnerships
   - mental-health awareness
5. Three-column content band:
   - latest news
   - association statement / mission highlight
   - upcoming events
6. Further sections:
   - membership invitation
   - featured training / resources
   - partners (only confirmed)
7. Footer:
   - official contact details, address, registration number, social links, legal links

## 4. Three-dimensional visual language
- Build depth through layered compositions, soft elevation, translucent surfaces used sparingly, parallax depth, subtle hover tilt and ambient lighting.
- Use a genuine 3D asset only for the hero focal object where it adds value; the rest should use CSS depth, SVG illustrations and layered imagery.
- Respect reduced-motion preferences; disable parallax/tilt for reduced-motion users.
- Never make text part of a raster hero image. All headings, labels, CTAs and navigation must remain live HTML text, selectable, translatable and accessible.
- Do not use a full-page screenshot as the website implementation.
- Keep 3D optional and progressively enhanced: meaningful static fallback for low-power devices and mobile.

## 5. Responsive behavior
- Desktop: full utility bar, horizontal nav, wide hero, multi-column cards.
- Tablet: compact navigation, reorganized hero, 2–3-column tiles.
- Mobile: accessible menu, stacked hero, single-column cards, large touch targets, no horizontal overflow, compressed/nonessential 3D.
- Arabic RTL and English LTR must both be tested at each breakpoint.

## 6. Content and interaction rules
- Do not invent Board or committee names, event dates, news, partners, numbers or testimonials. Empty sections should be hidden or use neutral calls to action until real content is entered.
- Board, committees, news, events, training, and partner sections must be CMS-editable.
- Membership fees and rights are controlled by approved configuration, not hard-coded into UI.
- The current 100 NIS basic/full membership fee may be shown once finance and approval details are confirmed; online payment remains inactive pending provider verification and contracting.
- All links and controls must work; no decorative nonfunctional buttons.

## 7. Accessibility, performance and SEO
- Semantic landmarks and heading order; keyboard navigation and visible focus.
- Sufficient color contrast; accessible names for icon-only controls.
- Alt text for meaningful imagery; decorative artwork hidden from assistive technologies.
- Reduced-motion support.
- Optimized responsive images, lazy loading below the fold, compressed 3D assets, performance budgets and graceful fallbacks.
- Arabic and English metadata, canonical URLs, sitemap, robots policy, Open Graph images and structured data appropriate to an association.

## 8. Homepage acceptance checklist
- Looks recognizably aligned with the supplied reference without copying its screenshot as a flat image.
- Official logo is used accurately.
- Every visible navigation item and CTA leads to a real page/section.
- No sample news/events or invented people are displayed.
- RTL/LTR, desktop/tablet/mobile layouts pass review.
- 3D effects are subtle, performant and reduced-motion aware.
- All public copy is editable and bilingual.
