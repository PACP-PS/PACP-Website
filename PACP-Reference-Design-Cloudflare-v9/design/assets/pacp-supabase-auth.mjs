import {createClient} from 'https://esm.sh/@supabase/supabase-js@2';
// Public client key only. Never place any private server credential in this file.
const supabaseUrl='https://nwbiazllkpiggbrwhpmh.supabase.co';
const publishableKey='sb_publishable_zbEonvbjAL5rGqBBnSW95Q_VrwUNxrh';
export const client=createClient(supabaseUrl,publishableKey,{auth:{persistSession:true,autoRefreshToken:true,detectSessionInUrl:true,flowType:'pkce'}});
export async function register(email,password,captchaToken){return client.auth.signUp({email,password,options:{emailRedirectTo:new URL('./auth.html',location.href).href,captchaToken}})}
export async function login(email,password,captchaToken){return client.auth.signInWithPassword({email,password,options:{captchaToken}})}
export async function logout(){return client.auth.signOut()}
export async function sendReset(email,captchaToken){return client.auth.resetPasswordForEmail(email,{redirectTo:new URL('./auth.html?pacp_recovery=1',location.href).href,captchaToken})}
export async function changePassword(password){return client.auth.updateUser({password})}
export async function mySummary(){return client.rpc('my_membership_summary')}
export async function myApplications(){return client.rpc('my_membership_applications')}
export async function submitApplication(data){return client.rpc('submit_my_membership_application',{p_data:data})}
export async function myCard(){return client.rpc('my_membership_card_status')}
export async function myStaffRoles(){return client.rpc('my_staff_roles')}
export async function staffQueue(){return client.rpc('staff_membership_queue',{p_limit:100})}
export async function recordCash(id,receipt,amount){return client.rpc('record_membership_cash',{p_application_id:id,p_receipt:receipt,p_amount:amount})}
export async function processApplication(id,action,reason,note){return client.rpc('process_membership_application',{p_application_id:id,p_action:action,p_reason:reason,p_applicant_note:note||null})}
export async function issueCard(id,tokenHash,year){return client.rpc('issue_membership_card',{p_application_id:id,p_token_hash:tokenHash,p_year:year})}
export async function uploadReceipt(userId,applicationId,file){
  const ext=(file.name.split('.').pop()||'bin').toLowerCase().replace(/[^a-z0-9]/g,'').slice(0,5)||'bin';
  const path=`${userId}/${applicationId}/${Date.now()}.${ext}`;
  const up=await client.storage.from('membership-receipts').upload(path,file,{contentType:file.type,upsert:false});
  if(up.error)return {error:up.error};
  return client.rpc('attach_payment_receipt',{p_application_id:applicationId,p_path:path,p_filename:file.name,p_mime:file.type,p_size:file.size});
}
export async function staffNationalId(id){return client.rpc('staff_get_national_id',{p_application_id:id})}
export async function uploadPortrait(userId,blob){
  const path=`${userId}/portrait.jpg`;
  const up=await client.storage.from('membership-portraits').upload(path,blob,{contentType:'image/jpeg',upsert:true});
  if(up.error)return {error:up.error};
  return client.rpc('set_my_portrait',{p_path:path});
}
export async function portraitUrl(userId){
  const l=await client.storage.from('membership-portraits').list(userId,{limit:5});
  if(l.error||!(l.data||[]).some(x=>x.name==='portrait.jpg'))return null;
  const s=await client.storage.from('membership-portraits').createSignedUrl(`${userId}/portrait.jpg`,3600);
  return s.data?s.data.signedUrl:null;
}
export async function receiptUrl(path){return client.storage.from('membership-receipts').createSignedUrl(path,300)}

export async function verifyCard(code){return client.rpc('verify_membership_card',{p_code:code})}
