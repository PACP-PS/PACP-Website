# PACP Infrastructure Update — 2026-11-03

## Owner-provided information (not independently verified)
- Association email is hosted on a server.
- A website and its related subdomain/site were created.
- Cloudflare was connected and DNS records were configured.
- Earlier provider statement described a VPS.

**Important:** Cloudflare DNS/proxy use does not itself establish Cloudflare Pages hosting. The web origin and mail origin may be separate. Do not change any existing DNS, proxy, mail or production settings.

## Read-only inventory required before deployment
Ask the administrator to confirm, without credentials:
1. Cloudflare zone and whether nameservers are active; screenshot/redacted list of DNS record *types, names, targets and proxy status* for apex, www and intended staging host.
2. Website origin (VPS IP/hostname, web server and document root) and whether the site is already live.
3. Mail provider and existing MX, SPF, DKIM and DMARC records; confirm mail delivery is functioning.
4. SSL/TLS mode and certificate at origin, HTTP→HTTPS behavior, and backup/restore policy.
5. Whether a separate `staging.pacp.ps` hostname and isolated document root can be provisioned without modifying the existing mail or production records.
6. Whether staging is static-only or needs a backend runtime, and who authorizes changes.

## Proposed staged delivery (requires owner approval)
**Stage A — static preview:** publish the design preview to an isolated staging hostname, with access restrictions if needed. No personal data or real forms. Use an isolated deployment directory; no changes to production site.
**Stage B — application integration:** separately provision authentication, database and storage, review RLS and migration drafts on a disposable environment, complete security tests, then connect staging.
**Stage C — production:** only after acceptance tests, backups, rollback plan and explicit approval. Preserve email configuration.

## Cloudflare-specific precautions
- Keep existing MX/TXT (SPF/DKIM/DMARC) records intact.
- Mail-related DNS hostnames should not be accidentally proxied as HTTP.
- Confirm whether the Cloudflare proxy is enabled for web hostnames and whether origin TLS is valid; avoid changing SSL mode blindly.
- Cloudflare is not a substitute for origin backups, access control or secure application configuration.
- Do not commit API keys, service-role secrets, email credentials or VPS access details to GitHub.

## Current repository state
The `rebuild/platform-foundation` branch contains design previews and review-draft Supabase migrations. The previews are not live services; database migrations have not been applied or verified against production.