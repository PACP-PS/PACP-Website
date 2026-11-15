#!/usr/bin/env python3
"""PACP read-only, real-token authorization smoke test (manual only).
Required env: PACP_SUPABASE_URL, PACP_PUBLISHABLE_KEY, PACP_TEST_A_JWT, PACP_TEST_B_JWT.
Use synthetic accounts with DIFFERENT application records. No database writes.
Never provide these JWTs as CLI arguments or put them in CI logs.
"""
import json, os, sys, urllib.request, urllib.error
from urllib.parse import urlparse

def required(name):
    value=os.environ.get(name,"").strip()
    if not value: raise RuntimeError("Missing private test setting: "+name)
    return value

def request(base,key,token,path,method="GET",body=None):
    headers={"apikey":key,"Authorization":"Bearer "+token,
             "Accept":"application/json","Content-Type":"application/json"}
    payload=json.dumps(body).encode() if body is not None else None
    req=urllib.request.Request(base+path,data=payload,headers=headers,method=method)
    try:
        with urllib.request.urlopen(req,timeout=15) as response:
            return response.status,json.loads(response.read(131072))
    except urllib.error.HTTPError as err:
        return err.code, None

def main():
    base=required("PACP_SUPABASE_URL").rstrip("/")
    host=urlparse(base)
    if host.scheme!="https" or not host.hostname or not host.hostname.endswith(".supabase.co"):
        raise RuntimeError("Supabase HTTPS URL required")
    key=required("PACP_PUBLISHABLE_KEY")
    a,b=required("PACP_TEST_A_JWT"),required("PACP_TEST_B_JWT")
    if a==b: raise RuntimeError("Tests A and B must have different tokens")
    identities=[]
    applications=[]
    for token in (a,b):
        code, user=request(base,key,token,"/auth/v1/user")
        if code!=200 or not isinstance(user,dict) or not user.get("id"):
            raise RuntimeError("Authenticated synthetic test identity unavailable")
        identities.append(user["id"])
        code, records=request(base,key,token,"/rest/v1/rpc/my_membership_applications","POST",{})
        if code!=200 or not isinstance(records,list):
            raise RuntimeError("Own-applications RPC failed")
        applications.append({r.get("application_id") for r in records if isinstance(r,dict)})
        code,_=request(base,key,token,"/rest/v1/rpc/membership_review_queue","POST",{"p_limit":25})
        if code in (200,201): raise RuntimeError("Nonstaff account unexpectedly permitted to review queue")
    if identities[0]==identities[1]: raise RuntimeError("Different tokens resolved to same identity")
    if not applications[0] or not applications[1]:
        raise RuntimeError("INCONCLUSIVE: create at least one synthetic application for each tester beforehand")
    if applications[0]&applications[1]:
        raise RuntimeError("CROSS-USER LEAK: overlapping application IDs")
    print("PASS: independent identities, distinct own applications, nonstaff review queue denied")
    print("LIMITATION: No direct-table access / staff transitions / payment / storage tested")

if __name__=="__main__":
    try: main()
    except Exception as err:
        # Exceptions must not contain tokens, URL parameters or personal records.
        print("FAIL / INCONCLUSIVE: "+str(err),file=sys.stderr)
        sys.exit(1)
