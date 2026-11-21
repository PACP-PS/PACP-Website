#!/usr/bin/env python3
"""Isolated PACP staging UI structural and JavaScript syntax preflight; no deployment."""
from html.parser import HTMLParser
from pathlib import Path
from tempfile import TemporaryDirectory
import re
import subprocess
import sys

SOURCE = Path("PACP-Reference-Design-Cloudflare-v9/design/pages/pacp-staging-integration.html")
class Elements(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            assert attrs["id"] not in self.ids, f"duplicate id: {attrs['id']}"
            self.ids.add(attrs["id"])

def main():
    page = SOURCE.read_text(encoding="utf8")
    el = Elements()
    el.feed(page)
    scripts = re.findall(r'<script[^>]*>(.*?)</script>', page, flags=re.S|re.I)
    assert len(scripts) == 1, "expected one JS module"
    js = scripts[0]
    used = set(re.findall(r"el\('([^']+)'\)", js))
    assert not (used-el.ids), f"missing HTML elements: {sorted(used-el.ids)}"
    mandatory = ["pacp_my_staff_roles", "pacp_admin_list_applications",
                 "pacp_review_application", "pacp_record_cash",
                 "pacp_issue_card", "pacp_my_card_status", "db.auth.getUser",
                 "pacp_applications", "staffArea", "notificationArea"]
    assert all(x in page for x in mandatory), "missing staging integration component"
    assert 'name="robots" content="noindex,nofollow"' in page
    assert "sb_secret_" not in page and "service_role" not in page
    assert "p_amount:Number" in page
    assert "el('cash').disabled=!roles.has('finance')" in js
    with TemporaryDirectory() as tmp:
        path = Path(tmp)/"staging.mjs"
        path.write_text(js, encoding="utf8")
        subprocess.run(["node", "--check", str(path)], check=True)
    print(f"PASS: staged PACP UI markup, {len(el.ids)} unique controls, all JS bindings, role gating, JS syntax.")

if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise
