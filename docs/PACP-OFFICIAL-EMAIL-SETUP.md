# PACP — Official administration and requests email

**Approved address:** info@pacp.ps

## Purpose
- Official contact address for general correspondence, membership applications and renewals, admin coordination and finance-related inquiries.
- Display as contact email on public site and on staging membership interface.
- Staff can use separate accounts for authorization; owning this mailbox does **not** grant superadmin privileges.

## Supabase staging mail configuration — required before real auth testing
1. Ensure the PACP owner actually receives messages at info@pacp.ps; send and reply to a mailbox test.
2. In Supabase Dashboard → PACP-Staging → Authentication → SMTP Settings, set custom SMTP server parameters using the authorized email provider's host, port, username and password/token. Set sender name `PACP | الجمعية الفلسطينية لاختصاصيي علم النفس العيادي` and sender email `info@pacp.ps`. Do not guess SMTP host or share credentials in GitHub.
3. Verify SPF, DKIM, DMARC and the provider's From-domain authorization **without changing existing MX/TXT/DNS unless explicitly agreed with the registrar**.
4. Configure staging Auth URL Settings site URL and allowed redirect URLs **only to confirmed PACP staging host** (not pacp.ps production).
5. Test signup confirmation, recovery, notification delivery, spam handling and bounce prevention using dedicated test inboxes.
6. For admin invitations, implement trusted server-side role invites and audit logging. Never derive staff authority from email address or user_metadata.

**Status:** Address displayed on staging interface. SMTP, outbound transactional mail, incoming mail processing, request notification triggers and administrator mailbox verification are **not configured or verified**.
