#!/usr/bin/env python3
"""PACP migration preflight: static checks only; no database connection."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
MIG = ROOT / "supabase" / "migrations"
EXPECTED = [f"000{i}_" for i in range(0, 9)]
issues = []
files = sorted(MIG.glob("*.sql"))
for prefix in EXPECTED:
    matches = [p for p in files if p.name.startswith(prefix)]
    if len(matches) != 1:
        issues.append(f"Expected one migration starting {prefix}, found {len(matches)}")
if issues:
    print("\n".join(issues))
    sys.exit(1)

sources = {p.name[:4]: p.read_text(encoding="utf-8") for p in files if p.name[:4] in {"0000","0001","0002","0003","0004","0005","0006","0007","0008"}}
base = (ROOT / "docs" / "DATABASE-SCHEMA-DRAFT.sql").read_text(encoding="utf-8")
checks = [
    ("baseline defines membership application", "create table public.membership_applications" in base.lower()),
    ("versioned baseline defines membership application", "create table public.membership_applications" in sources["0000"].lower()),
    ("versioned baseline contains original schema", base.strip() in sources["0000"]),
    ("baseline defines members", "create table public.members (" in base.lower()),
    ("0001 enables RLS", "enable row level security" in sources["0001"].lower()),
    ("0002 has application events", "create table if not exists public.membership_application_events" in sources["0002"].lower()),
    ("0003 has atomic approval function", "create or replace function public.process_membership_application" in sources["0003"].lower()),
    ("0003 checks trusted approver role", "public.has_staff_role('membership_approver')" in sources["0003"]),
    ("0003 does not authorize technical admin as approver", "v_role not in ('membership_approver','admin')" not in sources["0003"]),
    ("0004 defines trusted role assignments", "create table if not exists public.staff_role_assignments" in sources["0004"].lower()),
    ("0004 defines authorization helper", "create or replace function public.has_staff_role" in sources["0004"].lower()),
    ("0005 revokes base member reads", "revoke select on public.members from anon, authenticated" in sources["0005"].lower()),
    ("0005 limits review queue", "p_limit > 100" in sources["0005"]),
    ("0005 scopes member summary to auth user", "where m.user_id=v_user" in sources["0005"]),
    ("0006 validates membership payload", "membership_payload_shape_errors" in sources["0006"]),
    ("0007 limits document bucket", "membership-private" in sources["0007"]),
    ("0008 defines published site content", "site_content_entries" in sources["0008"]),
    ("0008 restricts contact inquiries", "revoke all on public.contact_inquiries" in sources["0008"].lower()),
]
for label, passed in checks:
    print(("PASS" if passed else "FAIL") + " " + label)
if not all(passed for _, passed in checks):
    sys.exit(1)
print("\nStatic preflight passed. This does NOT prove SQL executes, RLS is secure, or workflows are production-ready.")
