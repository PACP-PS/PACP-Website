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
   report[label]={"images":imgs,"horizontalOverflow":overflow,"scriptErrors":errors}
   assert all(i["loaded"] for i in imgs),f"{label}: broken image(s): {imgs}"
   assert not overflow,f"{label}: horizontal overflow"
   assert not errors,f"{label}: JavaScript errors: {errors}"
   page.close()
  browser.close()
finally:
 server.shutdown()
(OUT/"render-report.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf8")
print("PASS: actual Chromium rendered image, no script error or horizontal overflow at 3 widths")
