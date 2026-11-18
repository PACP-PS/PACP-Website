#!/usr/bin/env python3
"""Isolated Staging-only member login artifact. NEVER use as production output."""
from pathlib import Path
import shutil
root=Path(__file__).resolve().parents[1]
source=root/"PACP-Reference-Design-Cloudflare-v9/design/pages/staging-member-login.html"
dest=root/"build/pacp-phase2-staging"
dest.mkdir(parents=True,exist_ok=True)
shutil.copyfile(source,dest/"index.html")
page=(dest/"index.html").read_text(encoding="utf8")
assert 'aweebuukeovcekctclws.supabase.co' in page
assert 'lofvxgubetdslvaczvjp.supabase.co' not in page
assert 'persistSession:false' in page and 'pacp_my_card_status' in page
assert 'noindex,nofollow' in page and 'type="password"' in page
assert 'service_role' not in page and 'sb_secret_' not in page
assert len(list(dest.rglob("*.html")))==1
print("PASS: isolated Staging member login artifact:",dest)
