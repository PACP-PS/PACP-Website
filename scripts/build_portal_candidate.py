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
d=d.replace("التقديم الإلكتروني والدفع غير مفعّلين بعد. لن نعرض نموذجًا يوحي بإرسال طلب فعلي قبل ربطه بنظام آمن ومختبر.","التقديم الإلكتروني متاح بدعوة من الجمعية في هذه المرحلة. الدفع يتم نقدًا أو بالإيداع أو التحويل، وترفع العضوة أو العضو صورة الوصل في البوابة ليتحقق منه أمين الصندوق.")
d=d.replace("تعرض هذه الصفحة خطوات الانتساب إلى الجمعية. سيُعلن عن فتح تقديم طلبات الانتساب وإتاحة البطاقات المعتمدة عبر قنوات الجمعية الرسمية.","بعد الدخول بدعوة من الجمعية يمكنك تقديم طلب الانتساب ورفع وصل الدفع ومتابعة حالة الطلب، وتظهر بطاقة العضوية في بوابتك بعد اعتماد الطلب.")
d=d.replace("هذه معلومات تمهيدية؛ تقديم طلب الدفع وإرسال إثبات التحويل غير مفعّلين حتى اكتمال ربط النظام الآمن.","ارفعي وصل الدفع من بوابة الانتساب بعد تقديم الطلب. لا تُفعَّل العضوية إلا بعد تحقق أمين الصندوق واعتماد المسؤول المخوّل.")
big=('<section aria-label="الدخول إلى بوابة الانتساب" style="margin:22px 0;padding:26px;border-radius:18px;background:linear-gradient(135deg,#075b36,#0b7a4b);color:#fff;text-align:center">'
 '<h2 style="margin:0 0 8px;color:#fff">بوابة الانتساب الإلكترونية</h2>'
 '<p style="margin:0 0 16px;opacity:.92">للأعضاء المدعوّين: سجّلي الدخول لتقديم طلب الانتساب ورفع وصل الدفع ومتابعة حالة طلبك وبطاقتك.</p>'
 '<a href="auth.html" style="display:inline-block;background:#fff;color:#075b36;font-weight:800;font-size:18px;padding:14px 34px;border-radius:999px;text-decoration:none">ادخل إلى بوابة الانتساب ←</a>'
 '<p style="margin:14px 0 0;font-size:13px;opacity:.85">لا تملكين دعوة؟ راسلينا على info@pacp.ps</p></section>')
d=d.replace("<h2 class='section-title'>آلية الانتساب</h2>",big+"<h2 class='section-title'>آلية الانتساب</h2>",1)
m.write_text(d,encoding="utf8")
ix=DEST/"index.html";h=ix.read_text(encoding="utf8")
h=h.replace('<a class="btn" href="/PACP-Reference-Design-Cloudflare-v9/design/pages/about.html">','<a class="btn" style="background:#075b36;color:#fff;font-weight:800" href="/PACP-Reference-Design-Cloudflare-v9/design/pages/auth.html">ادخل إلى بوابة الانتساب ←</a><a class="btn" href="/PACP-Reference-Design-Cloudflare-v9/design/pages/about.html">',1)
ix.write_text(h,encoding="utf8")

# --- Member card page: reuse the approved glass front/back card from the home page, filled with real data ---
_h=ix.read_text(encoding="utf8")
_styles="".join(re.findall(r"<style[^>]*>.*?</style>",_h,flags=re.S))
_sec=re.search(r'<section class="membership-display".*?</section>',_h,flags=re.S).group(0)
for a_,b_ in (("عضو افتراضي",'<span id="cName"></span>'),("Sample Member",'<span id="cNameEn"></span>'),("PACP-DEMO-0001",'<span class="cCode"></span>'),("01 / 01 / 2025",'<span id="cFrom"></span>'),("31 / 12 / 2025",'<span id="cUntil"></span>')):
    _sec=_sec.replace(a_,b_)
_sec=re.sub(r'<div class="sample-watermark">.*?</div>','',_sec,flags=re.S)
_sec=re.sub(r'<span class="reverse-demo">.*?</span>','',_sec,flags=re.S)
_sec=_sec.replace("Demonstration design for a PACP membership card. Not proof of registered membership.","Official PACP membership card. Valid only while the membership status is active.")
_sec=_sec.replace("نموذج توضيحي لتصميم بطاقة عضوية الجمعية الفلسطينية لاختصاصيي علم النفس العيادي، وليس إثباتاً لعضوية فعلية.","بطاقة عضوية الجمعية الفلسطينية لاختصاصيي علم النفس العيادي، وتكون سارية ما دامت العضوية فعّالة.")
_sec=_sec.replace("نموذج بطاقة العضوية","بطاقة العضوية").replace("التجريبي","")
_card=('<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>بطاقة العضوية</title>'
 +_styles+'<style>html,body{background:transparent!important;margin:0}.site,.container{all:unset}.cards-pair .card-front .card-dates{background:#ffffffee;box-shadow:0 1px 4px #0a5c4630}.cards-pair .card-front .card-dates small{font-size:8px;color:#16453a}.cards-pair .card-front .card-dates b{font-size:10.5px;color:#073c2e}.cards-pair .card-front .sample-person>strong{font-size:14px;color:#062e24}.cards-pair .card-front .sample-person>b{font-size:10px}.cards-pair .card-front .member-no b{font-size:10px}.cards-pair .card-front .member-no small{font-size:7.5px}.cards-pair .card-front .avatar{box-shadow:0 3px 10px #0a5c4640;border-color:#0f6b48}.cards-pair .card-front .card-label span{font-size:7px}.cards-pair .card-front .card-brand strong{font-size:9.5px}.cards-pair .card-front .card-brand small{font-size:7.5px}.cards-pair .card-front .card-label{gap:2px;padding-left:6px}.cards-pair .card-front .card-label strong{font-size:12px;position:relative;z-index:6;line-height:1.2}.cards-pair .card-front .flag-bottom{height:26px;bottom:-16px;opacity:.75}.member-card:after{opacity:.45}.card-back-v3 .reverse-foot{grid-template-columns:1fr 1.25fr;padding:1.6cqw 2.6cqw}.card-back-v3 .reverse-identity{display:flex;align-items:center;gap:2.2cqw;direction:ltr;min-width:0;justify-content:flex-end}.card-back-v3 .reverse-identity img{width:9.5cqw;height:auto;max-height:11cqw;object-fit:contain;flex:none}.card-back-v3 .reverse-identity>div{display:flex;flex-direction:column;align-items:center;text-align:center;direction:rtl;gap:0}.card-back-v3 .reverse-identity b{font-size:2.9cqw;line-height:1.3;color:#0a4d38;white-space:nowrap}.card-back-v3 .reverse-identity small{font-size:2.3cqw;line-height:1.3;color:#0a4d38;width:100%;padding-bottom:.6cqw;margin-bottom:.6cqw;border-bottom:1px solid #0a5c4650;white-space:nowrap}.card-back-v3 .reverse-identity em{font-style:normal;font-size:2cqw;line-height:1.25;text-align:center;color:#a8182c;font-weight:700}.cards-pair .card-front .card-brand>div{text-align:center;align-items:center;gap:0;padding-inline:2px}.cards-pair .card-front .card-brand strong{font-size:11.5px;line-height:1.3;color:#0a4d38}.cards-pair .card-front .card-brand small{font-size:8.8px;line-height:1.3;color:#0a4d38;padding-bottom:3px;border-bottom:1px solid #0a5c4650;margin-bottom:3px;width:100%}.cards-pair .card-front .card-brand span{text-align:center;font-size:7.4px;line-height:1.25;letter-spacing:.1px;color:#a8182c}.cards-pair .card-front .card-brand{gap:7px;align-items:center}.cards-pair .card-front .card-brand img{width:52px;height:58px}.cards-pair .card-front .card-brand strong{font-size:11px;line-height:1.25}.cards-pair .card-front .card-brand small{font-size:8.6px;line-height:1.25}.cards-pair .card-front .card-brand span{font-size:7.6px;line-height:1.2}.cards-pair .card-front .card-brand>div{gap:2px}.cards-pair .card-front .front-heading{margin-top:9px}.cards-pair .card-front .corner-flag{width:34%;opacity:.85}.card-back-v3 .reverse-foot{margin-bottom:5cqw}.card-back-v3 .reverse-barcode b{position:relative;z-index:6;font-size:3cqw}.card-back-v3 .reverse-barcode span{height:6.5cqw}.card-back-v3 .reverse-foot{margin-bottom:6.5cqw}.card-back-v3 .reverse-identity img{width:8cqw;max-height:9cqw}.card-back-v3 .reverse-identity b{font-size:3cqw}.card-back-v3 .reverse-identity small{font-size:2.3cqw}.card-back-v3 .reverse-identity em{font-size:1.9cqw}.card-brand strong,.card-brand small,.card-label strong,.sample-person>strong,.reverse-identity b,.reverse-identity small,.reverse-heading strong{font-family:Amiri,serif!important;font-weight:700}.card-brand span,.card-label span,.sample-person>b,.reverse-identity em,.reverse-heading span{font-family:Cormorant Garamond,Georgia,serif!important;font-weight:700;letter-spacing:.2px}.cards-pair .card-front .card-brand strong{font-size:13px}.cards-pair .card-front .card-brand small{font-size:10px}.cards-pair .card-front .card-brand span{font-size:9px}.cards-pair .card-front .sample-person>strong{font-size:17px}.cards-pair .card-front .sample-person>b{font-size:12px}.cards-pair .card-front .card-label strong{font-size:14px}.card-back-v3 .reverse-identity b{font-size:3.4cqw}.card-back-v3 .reverse-identity small{font-size:2.7cqw}.card-back-v3 .reverse-identity em{font-size:2.3cqw}.card-back-v3 .reverse-foot{margin-bottom:9cqw;position:relative;z-index:5}.card-back-v3 .reverse-barcode span{height:4.6cqw}.card-back-v3 .reverse-barcode b{font-size:2.6cqw;display:block;margin-top:.6cqw}.card-back-v3 .reverse-identity em{line-height:1.1}.card-back-v3 .reverse-body{padding-bottom:0;margin-bottom:-1cqw}.card-back-v3{grid-template-rows:34% 4% 27% 35%!important}.card-back-v3 .reverse-foot{margin:0 3cqw 5cqw!important;align-self:center}.card-back-v3 .reverse-barcode span{height:5.5cqw}</style><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Amiri:wght@400;700&family=Cormorant+Garamond:wght@600;700&display=swap" rel="stylesheet"></head><body>'+_sec+
 '<script>const q=new URLSearchParams(location.search);const set=(i,v)=>{const e=document.getElementById(i);if(e)e.textContent=v||""};'
 'set("cName",q.get("n"));set("cNameEn",q.get("e"));set("cFrom",q.get("f"));set("cUntil",q.get("u"));'
 'if(q.get("p")){const av=document.querySelector(".avatar");if(av){av.innerHTML="";const im=document.createElement("img");im.src=q.get("p");im.alt="";im.style.cssText="width:100%;height:100%;object-fit:cover;display:block";av.appendChild(im)}}document.querySelectorAll(".cCode").forEach(x=>x.textContent=q.get("c")||"");'
 'const ps=()=>parent.postMessage({pacpCardH:document.documentElement.scrollHeight+8},location.origin);addEventListener("load",ps);addEventListener("resize",ps);setTimeout(ps,400);if(q.get("v")==="0")document.querySelectorAll(".member-card").forEach(x=>x.style.opacity=".5");</script></body></html>')
(DEST/INNER/"design/pages/card.html").write_text(_card,encoding="utf8")
a=DEST/INNER/"design/pages/auth.html";t=a.read_text(encoding="utf8")
t=t.replace("بوابة الحساب | PACP Development","بوابة الحساب | الجمعية الفلسطينية لاختصاصيي علم النفس العيادي")
a.write_text(t,encoding="utf8")
assert "lofvxgubetdslvaczvjp" not in "".join(p.read_text(encoding="utf8",errors="ignore") for p in DEST.rglob("*") if p.suffix in (".html",".mjs",".js"))
assert "aweebuukeovcekctclws" not in "".join(p.read_text(encoding="utf8",errors="ignore") for p in DEST.rglob("*") if p.suffix in (".html",".mjs",".js"))
print("built",DEST)
