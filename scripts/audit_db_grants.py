#!/usr/bin/env python3
"""Read-only policy review checks against a sanitized manually supplied SQL audit JSON.
This script does not connect to Supabase and must not process personal data.
Expected JSON: {"tables":[{"name":"...", "rls":true, "grants":{"anon":["SELECT"],"authenticated":["SELECT"]}}], "functions":[{"name":"...", "security_definer":true, "anon_execute":false, "authenticated_execute":true}]}.
"""
import json
import sys
from pathlib import Path
def check(data):
    findings=[]
    if len(data.get("tables", [])) < 1: findings.append("No tables in audit")
    for t in data.get("tables", []):
        if not t.get("rls"): findings.append(f"RLS missing: {t['name']}")
        for role, privileges in t.get("grants", {}).items():
            excessive=set(privileges)&{"TRUNCATE","TRIGGER","REFERENCES"}
            if role in {"anon","authenticated"} and excessive:
                findings.append(f"Excessive table privileges: {t['name']} / {role}: {','.join(sorted(excessive))}")
    for f in data.get("functions", []):
        if f.get("security_definer") and f.get("anon_execute"):
            findings.append(f"Privileged function callable anonymously: {f['name']}")
    return findings
if __name__ == "__main__":
    if len(sys.argv)!=2:
        print("Usage: python scripts/audit_db_grants.py sanitized_audit.json")
        sys.exit(2)
    findings=check(json.loads(Path(sys.argv[1]).read_text(encoding="utf-8")))
    for item in findings: print("FINDING: "+item)
    print(f"{len(findings)} finding(s)")
    sys.exit(bool(findings))
