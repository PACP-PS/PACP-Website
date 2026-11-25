#!/usr/bin/env python3
from pathlib import Path
s=Path('PACP-Reference-Design-Cloudflare-v9/design/pages/membership-application-preview.html').read_text(encoding='utf8')
for token in ('identity_document_type','identity_document_number','المعرّف الأساسي للعضوية','contact_email','وسيلة اتصال ودخول ثانوية','لا تستخدم رقمًا حقيقيًا'):
 assert token in s,token
migration=Path('security/identity-first-membership-registry-REVIEW-ONLY.sql').read_text(encoding='utf8')
for token in ('identity_fingerprint','unique (identity_document_type, identity_fingerprint)','enable row level security','revoke all'):
 assert token in migration,token
assert 'identity_document_number text' not in migration
print('PASS: identity-first preview and non-deployed private registry draft verified')
