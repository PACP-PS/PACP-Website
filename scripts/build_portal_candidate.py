#!/usr/bin/env python3
"""Build the PRODUCTION-CANDIDATE site: informational site + live membership portal (Supabase Production).
Output: build/pacp-portal-candidate. Public keys only; no secrets."""
from pathlib import Path
import shutil, re, subprocess, sys
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/"PACP-Reference-Design-Cloudflare-v9"
BASE=ROOT/"build/pacp-public-preview"
DEST=ROOT/"build/pacp-portal-candidate"
INNER="PACP-Reference-Design-Cloudflare-v9"
subprocess.run([sys.executable,str(ROOT/"scripts/build_public_preview.py")],check=True)
if DEST.exists():shutil.rmtree(DEST)
shutil.copytree(BASE,DEST)
for rel in ("design/pages/auth.html","design/pages/portal.html","design/pages/staff.html","design/assets/pacp-supabase-auth.mjs"):
    t=DEST/INNER/rel;t.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(SRC/rel,t)
m=DEST/INNER/"design/pages/membership.html"
d=m.read_text(encoding="utf8")
d=re.sub(r'<aside role="note" aria-label="حالة الخدمات الإلكترونية".*?</aside>','',d,flags=re.S)
cta=('<aside role="note" aria-label="بوابة الانتساب" style="direction:rtl;background:#e9f7f1;color:#063d31;'
 'border-right:4px solid #075b36;padding:16px 20px;margin:14px auto;max-width:1100px;border-radius:12px;font:600 14px/1.9 Tahoma,Arial,sans-serif">'
 'الانتساب الإلكتروني متاح بدعوة من الجمعية في هذه المرحلة (للدعوة: info@pacp.ps): بعد الدخول قدّمي الطلب ثم ارفعي وصل الدفع ليتحقق منه الطاقم. '
 '<a href="portal.html" style="color:#075b36">افتحي بوابة الانتساب ←</a> · '
 '<a href="auth.html" style="color:#075b36">تسجيل الدخول</a></aside>')
d=re.sub(r'(<body[^>]*>)',lambda x:x.group(1)+cta,d,count=1,flags=re.I)
m.write_text(d,encoding="utf8")
a=DEST/INNER/"design/pages/auth.html";t=a.read_text(encoding="utf8")
t=t.replace("بوابة الحساب | PACP Development","بوابة الحساب | الجمعية الفلسطينية لاختصاصيي علم النفس العيادي")
a.write_text(t,encoding="utf8")
assert "lofvxgubetdslvaczvjp" not in "".join(p.read_text(encoding="utf8",errors="ignore") for p in DEST.rglob("*") if p.suffix in (".html",".mjs",".js"))
assert "aweebuukeovcekctclws" not in "".join(p.read_text(encoding="utf8",errors="ignore") for p in DEST.rglob("*") if p.suffix in (".html",".mjs",".js"))
print("built",DEST)
