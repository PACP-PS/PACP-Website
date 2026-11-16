#!/usr/bin/env python3
"""Offline, static review of annual membership sandbox SQL. NOT a SQL runtime test."""
from pathlib import Path
p=Path(__file__).resolve().parents[1] / "docs/annual-membership-sandbox-schema.review.sql"
s=p.read_text(encoding="utf-8").lower()
# Comments must not be interpreted as executable DDL.
executable="\n".join(line.split("--",1)[0] for line in s.splitlines())
requirements={
    "explicit sandbox notice": "do not execute against pacp-development" in s,
    "separate annual period table": "create table public.membership_periods_sandbox" in s,
    "one period per member and year": "unique (member_id, membership_year)" in s,
    "calendar-year palestine time zone": s.count("'asia/hebron'") >= 2,
    "row level security": "enable row level security" in s,
    "revoke browser-facing grants": "revoke all on table public.membership_periods_sandbox from public, anon, authenticated" in s,
    "no permissive policy": "create policy" not in s,
    "active requires fee approval": "fee_decision in ('settled','waived')" in s,
    "active requires activation timestamp": "activated_at is not null" in s,
    "no deployed rpc": "security definer" not in executable and "create function" not in executable and "create or replace function" not in executable,
}
for name,ok in requirements.items():
    print(("PASS" if ok else "FAIL"),name)
if not all(requirements.values()):
    raise SystemExit(1)
print("Static contract passed; SQL has NOT been executed and is NOT production approved.")
