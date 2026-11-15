# PACP — manual Cloudflare Pages preview

This workflow is **not automatically deployed** and is **not a change to production**.

1. Configure an existing Cloudflare Pages project named `pacp-website` with permission to create **preview deployments**, and review the project settings to ensure `rebuild-platform-foundation` is **not its production branch**.
2. In the GitHub repository set secrets `CLOUDFLARE_API_TOKEN_PREVIEW` (limited to Pages edit on the appropriate account) and `CLOUDFLARE_ACCOUNT_ID`. Never put them in code or chat.
3. Configure a GitHub environment `pacp-preview` with required reviewers/approvals.
4. In Actions select **PACP preview deployment (manual approval only)** on branch `rebuild/platform-foundation`; enter `PACP-PREVIEW-APPROVED`.
5. The workflow checks original page paths then runs a **preview branch** Pages deployment with the exact existing static directory, no build.
6. Copy the URL that Cloudflare actually returns from the Actions job. Check that it is a Pages preview URL and inspect homepage, membership, courses, assets and mobile before sharing.
7. This preview is public unless restricted by Cloudflare Access. Do not submit real members' data. Configure access protection before real testers use authenticated flows.

No workflow job runs unless manually invoked with the explicit approval string. No DNS / MX / website domain changes should be made. The official site and main branch stay untouched. This workflow has not been triggered or tested against Cloudflare yet.
