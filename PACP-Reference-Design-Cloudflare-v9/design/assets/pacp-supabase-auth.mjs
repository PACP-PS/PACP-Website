import {createClient} from 'https://esm.sh/@supabase/supabase-js@2';
// Public client key only. NEVER put a service_role or SMTP credential in this file.
const supabaseUrl='https://lofvxgubetdslvaczvjp.supabase.co';
const publishableKey='sb_publishable_S6H6prb6Pr16VWGTLjwgOQ_cF5BrlGf';
export const client=createClient(supabaseUrl,publishableKey,{auth:{persistSession:true,autoRefreshToken:true,detectSessionInUrl:true,flowType:'pkce'}});
export async function register(email,password){return client.auth.signUp({email,password,options:{emailRedirectTo:new URL('./auth.html',location.href).href}})}
export async function login(email,password){return client.auth.signInWithPassword({email,password})}
export async function logout(){return client.auth.signOut()}
export async function sendReset(email){return client.auth.resetPasswordForEmail(email,{redirectTo:new URL('./auth.html?pacp_recovery=1',location.href).href})}
export async function changePassword(password){return client.auth.updateUser({password})}
export async function mySummary(){return client.rpc('my_membership_summary')}
export async function myApplications(){return client.rpc('my_membership_applications')}
