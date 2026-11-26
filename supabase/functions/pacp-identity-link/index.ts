// PACP secure identity linkage (staging design, NOT DEPLOYED).
// Secret env: SUPABASE_URL, SUPABASE_ANON_KEY, SUPABASE_SERVICE_ROLE_KEY,
// PACP_IDENTITY_HMAC_KEY (high-entropy random secret, >=32 bytes).
// Require an authenticated superadmin, verified real-world document and explicit
// human verification before invoking; never accept identity claims from public form.
import { createClient } from "https://esm.sh/@supabase/supabase-js@2.49.8";

const response = (status: number, result: Record<string, unknown>) =>
  new Response(JSON.stringify(result), { status, headers: {
    "content-type": "application/json; charset=utf-8", "cache-control": "no-store",
    "access-control-allow-origin": "null" } });
const validType = new Set(["palestinian_id", "passport", "other"]);
const validUUID = (x: unknown) => typeof x === "string" && /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(x);
const hex = (bytes: ArrayBuffer) => Array.from(new Uint8Array(bytes)).map(x=>x.toString(16).padStart(2,"0")).join("");
Deno.serve(async req => {
  if (req.method !== "POST") return response(405, { error: "method_not_allowed" });
  const bearer = req.headers.get("authorization") || "";
  if (!/^Bearer\s+\S+$/i.test(bearer)) return response(401, { error: "unauthorized" });
  const url = Deno.env.get("SUPABASE_URL");
  const anon = Deno.env.get("SUPABASE_ANON_KEY");
  const service = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY");
  const secret = Deno.env.get("PACP_IDENTITY_HMAC_KEY");
  if (!url || !anon || !service || !secret || new TextEncoder().encode(secret).length < 32)
    return response(503,{error:"service_not_configured"});
  const signedIn = createClient(url, anon, { auth: { persistSession: false } });
  const {data:{user},error:authErr} = await signedIn.auth.getUser(bearer.replace(/^Bearer\s+/i,""));
  if(authErr || !user) return response(401,{error:"unauthorized"});
  const admin = createClient(url, service, { auth:{persistSession:false} });
  const {data:role,error:roleErr} = await admin.from("pacp_staff_roles").select("role")
    .eq("user_id",user.id).eq("role","superadmin").maybeSingle();
  if (roleErr || !role) return response(403,{error:"forbidden"});
  let payload: Record<string,unknown>;
  try { payload = await req.json(); } catch { return response(400,{error:"invalid_request"}); }
  if (!validType.has(String(payload.document_type)) || !validUUID(payload.member_user_id) ||
      payload.verification_confirmed !== true || typeof payload.document_number !== "string")
    return response(400,{error:"invalid_request"});
  // Normalization must remain issuer-specific and legally approved before deploy.
  const normalized = payload.document_number.trim().toUpperCase().replace(/[\s\-]/g,"");
  if (normalized.length < 5 || normalized.length > 32 || !/^[A-Z0-9]+$/.test(normalized))
    return response(400,{error:"invalid_request"});
  const key = await crypto.subtle.importKey("raw", new TextEncoder().encode(secret),
    {name:"HMAC",hash:"SHA-256"},false,["sign"]);
  const fingerprint = hex(await crypto.subtle.sign("HMAC",key,
    new TextEncoder().encode(String(payload.document_type)+":"+normalized)));
  // Private schema is not exposed through Data API. Do NOT enable it merely to use
  // .schema(): this endpoint requires a separate narrow, service-only RPC deployed
  // after security review. Fail closed until that RPC exists.
  return response(503,{error:"identity_linking_not_enabled"});
});
