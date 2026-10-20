import './style.css';

type Service = {id:number;name:string;url:string;environment:string;status:string};
type Incident = {id:number;service_id:number;title:string;severity:string;status:string;details:string;created_at:string};
type Dashboard = {total_services:number;operational_services:number;open_incidents:number;uptime_percent:number;services:Service[];incidents:Incident[]};
const app = document.querySelector<HTMLDivElement>('#app')!;
let data: Dashboard | null = null;
let view = 'Overview';

async function request<T>(path:string, init?:RequestInit):Promise<T>{
  const res = await fetch(path,{...init,headers:{'Content-Type':'application/json',...(init?.headers||{})}});
  if(!res.ok){const body=await res.json().catch(()=>({detail:'Request failed'}));throw new Error(body.detail||'Request failed');}
  if(res.status===204)return undefined as T;
  return res.json() as Promise<T>;
}
const safe=(s:string)=>s.replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]!));
const pill=(s:string)=>`<span class="pill ${safe(s)}"><i></i>${safe(s)}</span>`;
function render(){
  app.innerHTML=`<aside class="sidebar"><div class="brand"><span class="logo">✳</span>dev<span>pulse</span></div><p class="eyebrow">WORKSPACE</p>
  ${['Overview','Services','Incidents'].map(v=>`<button class="nav ${view===v?'selected':''}" data-view="${v}">${v==='Overview'?'◫':v==='Services'?'▤':'⚠'} <span>${v}</span></button>`).join('')}
  <div class="side-bottom"><div class="live"><i></i><div><b>Demo environment</b><small>API connection status</small></div></div><small>DEVPULSE • STATUS INTELLIGENCE</small></div></aside>
  <main><header><span>Workspace　/　<b>${view}</b></span><div><span class="connected">● Demo data</span><button id="refresh" class="secondary">↻ Refresh</button><button id="add" class="primary">＋ Add service</button></div></header>
  <section class="content"><div class="heading"><div><p class="eyebrow">SYSTEM OVERVIEW</p><h1>${view==='Overview'?'Good systems. Clear signals.':view}</h1><p class="subtitle">A clear view of service health, performance, and incidents.</p></div><span class="chip">◷ Live workspace</span></div>
  ${data?`<div class="metrics"><article><label>MONITORED SERVICES</label><strong>${String(data.total_services).padStart(2,'0')}</strong><small>${data.operational_services} currently operational</small></article><article><label>RECENT CHECK UPTIME</label><strong>${data.uptime_percent.toFixed(1)}%</strong><small>Based on recorded checks</small></article><article><label>OPEN INCIDENTS</label><strong>${String(data.open_incidents).padStart(2,'0')}</strong><small>${data.open_incidents?'Requires attention':'All clear'}</small></article></div>
  ${view!=='Incidents'?`<section class="panel"><div class="panel-head"><div><h2>Service health</h2><p>Current status of monitored endpoints</p></div><button data-view="Services" class="link">View all ↗</button></div><div class="table-head"><span>SERVICE</span><span>ENVIRONMENT</span><span>STATUS</span><span></span></div>
  ${data.services.map(s=>`<div class="service"><div class="service-name"><span class="service-icon">▤</span><div><b>${safe(s.name)}</b><small>${safe(s.url)}</small></div></div><span class="env">${safe(s.environment)}</span>${pill(s.status)}<button class="delete" data-id="${s.id}" title="Delete service">×</button></div>`).join('')||'<p class="empty">No services yet. Add one to get started.</p>'}</section>`:''}
  ${view!=='Services'?`<section class="panel"><div class="panel-head"><div><h2>Recent incidents</h2><p>Latest events across your services</p></div><button data-view="Incidents" class="link">Incident history ↗</button></div>
  ${data.incidents.map(i=>`<div class="incident"><span class="warn">⚠</span><div class="incident-copy"><b>${safe(i.title)}</b><p>${safe(i.details||'No additional details')}</p><small>${new Date(i.created_at).toLocaleString()}</small></div><div class="incident-action"><span>${safe(i.severity)}</span>${i.status==='open'?`<button class="resolve" data-incident="${i.id}">Resolve</button>`:'Resolved'}</div></div>`).join('')||'<p class="empty">No incidents recorded.</p>'}</section>`:''}`:'<div class="error">Cannot connect to API. Start the backend and click Refresh.</div>'}
  <footer>DEVPULSE　•　BUILT WITH FASTAPI + TYPESCRIPT</footer></section></main>
  <dialog id="modal"><form id="service-form"><button type="button" id="close" class="close">×</button><p class="eyebrow">CONFIGURATION</p><h2>Add a service</h2><label>Service name<input name="name" minlength="2" required placeholder="Payments API"></label><label>Service URL<input name="url" type="url" required placeholder="https://api.example.com"></label><label>Environment<select name="environment"><option>production</option><option>staging</option><option>development</option></select></label><p id="error" class="form-error"></p><button class="primary" type="submit">Add service ↗</button></form></dialog><div id="toast"></div>`;
  document.querySelectorAll<HTMLButtonElement>('[data-view]').forEach(b=>b.onclick=()=>{view=b.dataset.view!;render()});
  document.querySelector('#refresh')!.addEventListener('click',()=>void load());
  document.querySelector('#add')!.addEventListener('click',()=>document.querySelector<HTMLDialogElement>('#modal')!.showModal());
  document.querySelector('#close')!.addEventListener('click',()=>document.querySelector<HTMLDialogElement>('#modal')!.close());
  document.querySelector<HTMLFormElement>('#service-form')!.onsubmit=async e=>{e.preventDefault();const fd=new FormData(e.currentTarget as HTMLFormElement);try{await request('/api/services',{method:'POST',body:JSON.stringify({name:fd.get('name'),url:fd.get('url'),environment:fd.get('environment')})});document.querySelector<HTMLDialogElement>('#modal')!.close();await load();notify('Service added.')}catch(err){document.querySelector('#error')!.textContent=err instanceof Error?err.message:'Could not add service.'}};
  document.querySelectorAll<HTMLButtonElement>('.delete').forEach(b=>b.onclick=async()=>{if(confirm('Delete this service and its history?'))try{await request(`/api/services/${b.dataset.id}`,{method:'DELETE'});await load();notify('Service deleted.')}catch(e){notify(String(e))}});
  document.querySelectorAll<HTMLButtonElement>('.resolve').forEach(b=>b.onclick=async()=>{try{await request(`/api/incidents/${b.dataset.incident}/resolve`,{method:'PATCH'});await load();notify('Incident resolved.')}catch(e){notify(String(e))}});
}
function notify(msg:string){const t=document.querySelector<HTMLDivElement>('#toast')!;t.textContent=msg;t.classList.add('show');setTimeout(()=>t.classList.remove('show'),2500)}
async function load(){try{data=await request<Dashboard>('/api/dashboard')}catch(e){console.error(e);data=null}render()}
render();void load();
