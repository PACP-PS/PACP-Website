# PACP practical accessibility & staging authorization audit — 2026-11-18

## Scope and status
**Partial audit — not WCAG certification, not complete login UAT.** GitHub branch `rebuild/platform-foundation`; Supabase PACP-Staging. No production, DNS, email or real member data changed.

## Confirmed changes
- WG-SS (six functional domains, four options each) added to application and member portal *preview* pages, optional; no data submission/storage implemented.
- Arabic source: Washington Group translation dated 2020-01-22: https://www.washingtongroup-disability.com/fileadmin/uploads/wg/Documents/Short_Set_Translations/WG-Short-Set-Arabic-translation-v2020-Jan-22.pdf
- CI structural test `scripts/test_wg_ss_inclusion.py` added to `prelaunch-guardrails.yml`. Latest workflow on the new commit has not yet been confirmed.
- Shared accessibility controls (text, contrast, motion, skip) connected to homepage; note typography still uses numerous fixed pixel sizes.

## Practical audit findings (inspection of actual source)
| Check | Result | Required remediation |
|---|---|---|
| Arabic `lang` and RTL on reviewed application | PASS (source) | Validate English switching once implemented |
| WG-SS completeness | PASS (source) | Test rendered page and mobile screen reader |
| Voluntary disclosure | PASS (source) | Never gate eligibility on responses |
| Functional accommodation workflow | PARTIAL | Preview fields only; no securely isolated storage or staff routing |
| Text scaling 200% and 400% reflow | NOT VERIFIED | Fixed 9–12px fonts across previews; refactor to relative sizes and browser-test |
| Keyboard focus and reduced-motion settings | PARTIAL | Shared enhancement present; manually test tab order, focus return and full page |
| Course tabs semantics | FAIL source review | Buttons alter content with JS but lack complete ARIA tabs/tabpanel keyboard contract; use accessible tab semantics or simpler heading/sections |
| WG optional responses privacy | PARTIAL | No storage currently; future restricted schema, privacy notice, independent consent/retention required |
| Color contrast | NOT VERIFIED | Verify all text and states with automated+manual contrast testing |
| Screen reader Arabic | NOT VERIFIED | NVDA/VoiceOver and actual mobile/browser tests needed |
| Audio/video captions and transcripts | NOT VERIFIED | Required before training-content activation |
| Browser visual parity approved design | NOT VERIFIED | Screenshot comparison needed |
| WG-SS version | REVIEW | Version is preliminary Arabic 2020; confirm current validated localization before official data collection |

## Authorization test evidence
- Supabase security advisor: four RLS-no-policy info notices; seven signed-in-executable SECURITY DEFINER warnings; leaked password protection disabled.
- Prior SQL inspection showed `anon` cannot execute PACP public RPCs; callability alone is not an authorization bypass.
- Role records exist but **test identity JWTs/session access were not available**. No claim that member-versus-finance-versus-approver token-based endpoint requests passed.
- Existing `scripts/test_member_auth_live_readonly.py` is for the *Development* schema's membership RPCs; it must not be misrepresented as a valid test of Staging's different `pacp_*` schema.
- Need nonstaff and separate-role synthetic JWTs obtained securely, not pasted in chat/committed into GitHub. Run negative access tests and save only pass/fail evidence.

## Release verdict
**NO-GO for production.** The privacy architecture, token-level authorization, manual WCAG audit and acceptance tests remain incomplete. Informational-only release is independently assessable.
