#!/usr/bin/env python3
"""Fail-closed static prelaunch checks. Does not contact production or process private data."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
required = [
    "index.html",
    "assets/pacp-logo.svg",
    "PACP-Reference-Design-Cloudflare-v9/assets/pacp-logo-original.png",
    "PACP-Reference-Design-Cloudflare-v9/design/pages/auth.html",
    "PACP-Reference-Design-Cloudflare-v9/design/pages/member-dashboard-staging.html",
    "supabase/migrations/0000_foundation_review_draft.sql",
    "docs/IMPLEMENTATION-READINESS-GATES.md",
]
errors = []
for name in required:
    if not (ROOT / name).is_file():
        errors.append(f"Missing required project file: {name}")

# Scan only small text assets. Never echo a suspected secret.
patterns = {
    "Supabase service-role key": re.compile(r'(?i)(?:service_role|supabase_service_role_key)\s*[:=]\s*["\']eyJ[A-Za-z0-9_.-]{30,}'),
    "Cloudflare API token assignment": re.compile(r'(?i)(?:CLOUDFLARE_API_TOKEN|CF_API_TOKEN)\s*[:=]\s*["\']?[A-Za-z0-9_-]{25,}'),
    "private key header": re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),
}
for path in list(ROOT.rglob("*.html")) + list(ROOT.rglob("*.mjs")) + list(ROOT.rglob("*.js")):
    if ".git" in path.parts or path.stat().st_size > 300_000:
        continue
    content = path.read_text(encoding="utf-8", errors="replace")
    for label, pattern in patterns.items():
        if pattern.search(content):
            errors.append(f"Potential {label} in {path.relative_to(ROOT)} (redacted)")

if errors:
    print("PRELAUNCH STATIC CHECK: FAILED")
    for error in errors:
        print(" - " + error)
    sys.exit(1)
print("PRELAUNCH STATIC CHECK: PASSED (files and limited secret patterns only)")
print("NOT VERIFIED: live RLS, role boundaries, login, payments, approvals, visual QA, deployments.")
