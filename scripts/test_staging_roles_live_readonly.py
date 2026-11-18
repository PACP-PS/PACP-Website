#!/usr/bin/env python3
"""READ-ONLY PACP-Staging auth smoke tests with independently obtained synthetic JWTs.
Environment: PACP_STAGING_URL, PACP_STAGING_PUBLISHABLE_KEY,
PACP_STAGING_MEMBER_JWT, PACP_STAGING_FINANCE_JWT, PACP_STAGING_APPROVER_JWT.
Never put tokens in arguments, source, CI artifacts or logs.
"""
import os, json, urllib.request, urllib.error, sys
from urllib.parse import urlparse
def env(name):
 v=os.environ.get(name,"").strip()
 if not v: raise RuntimeError("Missing securely injected env: "+name)
 return v
def call(base,key,jwt,path):
 req=urllib.request.Request(base+path,data=b"{}",method="POST",headers={"apikey":key,"Authorization":"Bearer "+jwt,"Content-Type":"application/json"})
 try:
  with urllib.request.urlopen(req,timeout=12) as rsp:return rsp.status
 except urllib.error.HTTPError as e:return e.code
def identity(base,key,jwt):
 req=urllib.request.Request(base+"/auth/v1/user",headers={"apikey":key,"Authorization":"Bearer "+jwt})
 try:
  with urllib.request.urlopen(req,timeout=12) as r:return json.load(r).get("id")
 except urllib.error.HTTPError:return None
def main():
 base=env("PACP_STAGING_URL").rstrip("/")
 if urlparse(base).hostname!="aweebuukeovcekctclws.supabase.co" or not base.startswith("https://"):raise RuntimeError("Staging project URL mismatch: refusing to run")
 key=env("PACP_STAGING_PUBLISHABLE_KEY")
 tokens=[env("PACP_STAGING_"+r+"_JWT") for r in ("MEMBER","FINANCE","APPROVER")]
 ids=[identity(base,key,t) for t in tokens]
 if not all(ids) or len(set(ids))!=3:raise RuntimeError("Three distinct signed-in synthetic identities are required")
 cases=[
  ("member cannot list applications",tokens[0],"/rest/v1/rpc/pacp_admin_list_applications",False),
  ("finance cannot list applications",tokens[1],"/rest/v1/rpc/pacp_admin_list_applications",False),
  ("approver can list applications",tokens[2],"/rest/v1/rpc/pacp_admin_list_applications",True)]
 failed=[]
 for name,jwt,path,allow in cases:
  code=call(base,key,jwt,path)
  ok=(code==200) if allow else (code in (401,403))
  print(("PASS" if ok else "FAIL")+" "+name+" (HTTP "+str(code)+")")
  if not ok:failed.append(name)
 if failed:raise RuntimeError("Authorization mismatch in "+str(len(failed))+" cases")
 print("LIMITATION: read-only list-access smoke checks only; does not verify cash, card issuance or BOLA")
if __name__=="__main__":
 try:main()
 except Exception as e:
  print("BLOCKED/FAIL: "+str(e),file=sys.stderr)
  sys.exit(1)
