#!/usr/bin/env python3
"""Staging-platform release checks. No tokens, writes or deployments."""
from pathlib import Path
import json
BASE=Path("PACP-Reference-Design-Cloudflare-v9/design")
release=Path("security/platform-phase2-acceptance.json")
data=json.loads(release.read_text(encoding="utf-8"))
assert data["environment"]=="PACP-Staging"
assert data["production_write_enabled"] is False
for target in (
 "pages/member-portal-preview.html",
 "pages/membership-application-preview.html",
 "pages/course-registration-preview.html",
 "admin/central-admin-dashboard-preview.html",
):
 p=BASE/target
 html=p.read_text(encoding="utf8")
 assert "preview" in target and "<html" in html.lower(),target
 assert "https://wa.me/" not in html or "wa.me/" in html
assert all(v["status"]=="pending" for v in data["gates"].values())
assert "identity_linking_not_enabled" in Path("supabase/functions/pacp-identity-link/index.ts").read_text()
print("PASS: phase-two pages and authorization gates still isolated from public launch")
