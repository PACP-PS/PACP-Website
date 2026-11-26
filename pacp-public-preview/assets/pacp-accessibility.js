/* PACP accessibility preferences: local to device, not tied to member identity. */
(()=>{'use strict';
const ROOT=document.documentElement, PREF='pacp_accessibility_v1', OPTIONS=['large-text','contrast','no-motion'];
let state={};try{state=JSON.parse(localStorage.getItem(PREF)||'{}')||{}}catch(_){state={}}
const apply=()=>OPTIONS.forEach(x=>ROOT.classList.toggle('pacp-'+x,!!state[x]));
apply();
function init(){
if(document.querySelector('.pacp-access'))return;
const main=document.querySelector('main')||document.querySelector('.site')||document.querySelector('header')||document.body;
if(!main.id)main.id='pacp-main';
const skip=document.createElement('a');skip.className='pacp-skip';skip.href='#'+main.id;skip.textContent='تجاوز إلى المحتوى الرئيسي';document.body.prepend(skip);
const box=document.createElement('aside');box.className='pacp-access';box.setAttribute('aria-label','إعدادات إمكانية الوصول');
const trigger=document.createElement('button');trigger.type='button';trigger.className='pacp-access-toggle';trigger.textContent='إمكانية الوصول';trigger.setAttribute('aria-expanded','false');trigger.setAttribute('aria-controls','pacp-access-panel');
const panel=document.createElement('div');panel.className='pacp-access-panel';panel.id='pacp-access-panel';panel.hidden=true;
const field=document.createElement('fieldset'),legend=document.createElement('legend');legend.textContent='خيارات القراءة والتصفح';field.append(legend);
const actions=document.createElement('div');actions.className='pacp-access-actions';
[['large-text','تكبير النص'],['contrast','تباين مرتفع'],['no-motion','تقليل الحركة']].forEach(([key,label])=>{
const btn=document.createElement('button');btn.type='button';btn.textContent=label;btn.setAttribute('aria-pressed',String(!!state[key]));
btn.addEventListener('click',()=>{state[key]=!state[key];btn.setAttribute('aria-pressed',String(!!state[key]));apply();try{localStorage.setItem(PREF,JSON.stringify(state))}catch(_){}});
actions.append(btn)});
const reset=document.createElement('button');reset.type='button';reset.textContent='إعادة الضبط';reset.addEventListener('click',()=>{state={};apply();actions.querySelectorAll('[aria-pressed]').forEach(b=>b.setAttribute('aria-pressed','false'));try{localStorage.removeItem(PREF)}catch(_){}});
actions.append(reset);field.append(actions);panel.append(field);box.append(trigger,panel);document.body.append(box);
trigger.addEventListener('click',()=>{panel.hidden=!panel.hidden;trigger.setAttribute('aria-expanded',String(!panel.hidden));});
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&!panel.hidden){panel.hidden=true;trigger.setAttribute('aria-expanded','false');trigger.focus()}});
}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',init,{once:true});else init();
})();
