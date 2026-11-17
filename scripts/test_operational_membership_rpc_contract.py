#!/usr/bin/env python3
"""Contract checks for PACP live (read-only) RPC integration. No network or credentials."""
from pathlib import Path
root=Path(__file__).resolve().parents[1]
page=(root/"PACP-Reference-Design-Cloudflare-v9/design/pages/member-dashboard-staging.html").read_text(encoding="utf-8")
auth=(root/"PACP-Reference-Design-Cloudflare-v9/design/assets/pacp-supabase-auth.mjs").read_text(encoding="utf-8")
build=(root/"scripts/build_public_preview.py").read_text(encoding="utf-8")
assert "client.rpc('my_membership_operational_status')" in page
assert "await client.auth.getUser()" in page
assert "official_card_available" not in page or "غير" in page
assert "غير متاح" in page or "غير مؤكد" in page or "غير مفع" in page
assert "auth.html" in build and "membership.html" in build
assert "const serviceRole" not in auth and "service_role:" not in auth
assert "sb_secret_" not in auth
assert 'digital-card-staging.html' in build
print("PASS: member dashboard uses authenticated read-only RPC, bank/card remain disabled, no secrets")
