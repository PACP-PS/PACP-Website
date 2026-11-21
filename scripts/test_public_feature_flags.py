#!/usr/bin/env python3
"""Validate informational-only public export; no real member workflow is bundled."""
from pathlib import Path
import subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
subprocess.run([sys.executable,str(ROOT/'scripts/build_public_preview.py')],check=True)
out=ROOT/'build/pacp-public-preview'
assert (out/'index.html').exists()
htmls=list(out.rglob('*.html'))
assert htmls
for file in htmls:
    content=file.read_text(encoding='utf8')
    assert 'service_role' not in content
    assert 'sb_secret_' not in content
    assert not file.name.endswith('-staging.html')
    assert not file.name.endswith('-preview.html')
    assert file.name != 'auth.html'
for name in ('membership','training'):
    page=(out/f'PACP-Reference-Design-Cloudflare-v9/design/pages/{name}.html').read_text(encoding='utf8')
    assert 'غير مفعّلة حاليًا' in page
    assert 'تجديد العضوية' in page
print('PASS: public website is informational-only, deferred services are explicit')
