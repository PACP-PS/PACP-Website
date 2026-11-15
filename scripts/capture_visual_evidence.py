#!/usr/bin/env python3
"""Render PACP canonical build in Chromium; fail for missing visible hero images."""
from pathlib import Path
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from functools import partial
from threading import Thread
from playwright.sync_api import sync_playwright
import json
ROOT=Path(__file__).resolve().parents[1]
SITE=ROOT/"build/pacp-public-preview"
OUT=ROOT/"build/visual-evidence"
OUT.mkdir(parents=True,exist_ok=True)
server=ThreadingHTTPServer(("127.0.0.1",0),partial(SimpleHTTPRequestHandler,directory=str(SITE)))
Thread(target=server.serve_forever,daemon=True).start()
base=f"http://127.0.0.1:{server.server_port}"
report={}
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(headless=True)
  for label,width,height in (("desktop",1440,900),("tablet",768,1024),("mobile",390,844)):
   page=browser.new_page(viewport={"width":width,"height":height},device_scale_factor=1)
   errors=[]
   page.on("pageerror",lambda exc:errors.append(str(exc)))
   page.goto(base+"/",wait_until="networkidle",timeout=60000)
   page.screenshot(path=str(OUT/f"PACP-{label}.png"),full_page=True)
   imgs=page.locator("img").evaluate_all("(images)=>images.map(i=>({src:i.getAttribute('src'),loaded:i.complete&&i.naturalWidth>0}))")
   overflow=page.evaluate("document.documentElement.scrollWidth > window.innerWidth + 3")
   visual=page.evaluate("""() => {
     const rect=sel=>{const e=document.querySelector(sel);if(!e)return null;const r=e.getBoundingClientRect();return {x:r.x,y:r.y,width:r.width,height:r.height}}
     const card=document.querySelector('.member-card');
     const style=card?getComputedStyle(card):null;
     return {brain:rect('.brain-hero'),copy:rect('.hero-copy'),jerusalem:rect('.jerusalem-hero'),
       cards:document.querySelectorAll('.member-card').length,services:document.querySelectorAll('.services .service').length,
       glassBlur:style?style.backdropFilter:null,
       font:getComputedStyle(document.querySelector('h1')).fontFamily}
   }""")
   report[label]={"images":imgs,"horizontalOverflow":overflow,"scriptErrors":errors,"visual":visual}
   assert visual["cards"]>=2,f"{label}: missing membership card faces"
   if label=="desktop":assert visual["services"]==5,f"Approved screenshot requires 5 tiles; found {visual['services']}"
   assert visual["brain"] and visual["copy"] and visual["jerusalem"],f"{label}: incomplete hero"
   if label=="desktop":
    assert visual["brain"]["x"] < visual["copy"]["x"] < visual["jerusalem"]["x"],f"Wrong approved desktop hero ordering: {visual}"
    assert visual["glassBlur"] and visual["glassBlur"]!="none",f"Missing membership glass treatment: {visual}"

   assert all(i["loaded"] for i in imgs),f"{label}: broken image(s): {imgs}"
   assert not overflow,f"{label}: horizontal overflow"
   assert not errors,f"{label}: JavaScript errors: {errors}"
   page.close()
  browser.close()
finally:
 server.shutdown()
(OUT/"render-report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf8")
print("PASS: actual Chromium rendered image, no script error or horizontal overflow at 3 widths")
