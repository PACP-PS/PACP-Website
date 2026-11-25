# PACP Hosting Decision Record — VPS reported by technical provider

**Status:** provisional infrastructure finding; not independently verified.  
**Source:** association's technical support stated that `pacp.ps` is "مربوط جاهز في سيرفر vps".  
**Decision:** preserve current DNS, web hosting and email configuration until a read-only inventory is completed.

## What is known vs unknown

Known from provider statement: domain is reportedly connected to a VPS.

Not yet verified:
- authoritative nameservers, A/AAAA/CNAME, DNS provider, CDN/proxy configuration;
- actual web server (Nginx/Apache/Caddy), operating system, ports and SSL renewal;
- who owns/administrates VPS and deployment access;
- whether the current site is served from VPS, Cloudflare Pages or another upstream;
- whether `info@pacp.ps` mailboxes live on VPS or a separate mail service;
- MX, SPF, DKIM, DMARC and backup/restore arrangements;
- whether Node.js, Docker, PostgreSQL or reverse proxy are available.

## Deployment options to evaluate

| Option | Characteristics | Prerequisites |
|---|---|---|
| Keep public frontend on VPS | Minimal DNS disruption; operational responsibility remains with VPS owner | Web server, HTTPS, deploy/rollback, access and backups |
| VPS frontend + managed Supabase | Web UI on VPS; managed authentication/database | secure HTTPS, env configuration, CORS, region/data governance, secrets |
| Cloudflare Pages frontend + managed backend | Preview deploys possible, but DNS and mail must be planned | confirm existing Cloudflare use, DNS ownership, explicit migration approval |
| Entire backend on VPS | Single hosting vendor but highest operational burden | patching, DB security, backups, monitoring, restore drills |

**Provisional preference:** retain VPS for public website during discovery. Do not decide the application backend location until infrastructure and privacy requirements are confirmed.

## Read-only questions for hosting provider

1. Which public IPv4/IPv6 address and DNS nameservers currently serve `pacp.ps` and `www.pacp.ps`?
2. Is the website currently hosted on the VPS? What web server and OS versions are installed?
3. Does VPS include SSH/SFTP, Git-based deployment, staging subdomain, SSL auto-renewal and backup/restore?
4. Are Node.js runtime, Docker and reverse proxy permitted? Is there an application process manager?
5. Where is `info@pacp.ps` hosted? Please confirm MX/SPF/DKIM/DMARC without sending credentials.
6. Who has administrative ownership, and can a read-only inventory be provided?
7. Can staging use a separate subdomain without changing the live site's DNS or mail records?

## Non-negotiable change controls

- No edits to nameservers, A/AAAA/CNAME, MX, SPF, DKIM or DMARC without written owner approval and rollback plan.
- Never put SSH passwords, API tokens, mail passwords or database credentials in chat, commits or public files.
- Do not open firewall ports, install packages or deploy to VPS without a reviewed change request.
- Confirm HTTPS and backups before any collection of membership identity documents.
- Staging must use fictional data and isolated credentials.

## Next technical gate

Obtain a read-only infrastructure inventory from the provider. Decide whether staging belongs on VPS or separate hosting. Only then prepare deployment automation.
