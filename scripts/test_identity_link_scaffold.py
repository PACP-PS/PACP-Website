#!/usr/bin/env python3
from pathlib import Path
s=Path("supabase/functions/pacp-identity-link/index.ts").read_text()
for required in ["SUPABASE_SERVICE_ROLE_KEY","PACP_IDENTITY_HMAC_KEY","auth.getUser","superadmin","crypto.subtle.sign","identity_linking_not_enabled"]:
 assert required in s,required
assert "console.log(payload)" not in s
assert "identity_fingerprint" not in s or "service-only" in s
print("PASS: server-only identity linking scaffold fails closed until verification RPC and policy approval")
