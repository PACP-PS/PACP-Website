# PACP Public Content & Contact — Implementation Contract

**Status:** development drafts; no production deployment.

## News and events
- CMS table `site_content_entries` contains bilingual content with `draft`, `review`, `published`, `archived` states.
- Only published content whose publish timestamp is in the past may be public.
- The news/events preview currently displays clearly labeled templates, not live announcements.
- Future editor/approver permissions, image uploads, revision history and publication audits require implementation.
- Events use start/end timestamps; show times with the local time zone only after it is set and verified.

## Contact
- Current contact preview uses `mailto:` and does not submit to a backend.
- The `contact_inquiries` table is a future-only structure with no public insert/read permission.
- Before connecting a web form: privacy notice, consent, anti-spam, throttling, staff routing, retention and no clinical/patient data collection.
- Preserve existing `info@pacp.ps` mailbox and MX/DNS settings.

## Integration
- Public UI fetches only published CMS records through a reviewed read-only API.
- No service-role key or SMTP credentials may be embedded in browser JS.
- All user-entered content is rendered as text, not injected HTML.
- Provide empty/loading/error states and accessible filters.
- Preview environment must be separate from the live VPS-hosted domain until approved.
