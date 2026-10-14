const {load}=require('./harness');
const NEW=require('path').join(__dirname,'..','index.html');
let fails=0; const ok=(c,m)=>{ if(!c){ fails++; console.log('FAIL:',m); } else console.log('ok:',m); };

// ---- T1: first start shows the wizard
{
  const {w,errors}=load(NEW);
  const wiz=w.document.getElementById('wiz');
  ok(!wiz.hidden,'wizard is open on first start');
  ok(/Welcome/.test(wiz.textContent),'welcome text visible');
  ok(/No account, no tracking, no cloud/.test(wiz.textContent),'privacy line visible');
  ok(errors.length===0,'no script errors on boot '+errors.slice(0,2).join(' | '));
  const t=w.__t;
  ok(t.state.profile.setup===false,'profile.setup false before wizard');
}

// ---- T2: click through the wizard
{
  const {w,errors}=load(NEW);
  const d=w.document, click=el=>el.dispatchEvent(new w.MouseEvent('click',{bubbles:true}));
  const q=s=>d.querySelector(s);
  click(q('[data-wgoal="10k"]'));
  ok(q('[data-wgoal="10k"]').getAttribute('aria-pressed')==='true','10k selected');
  click(q('[data-wlevel="some"]'));
  click(q('[data-wnext]'));
  ok(/Your week/.test(d.getElementById('wiz').textContent),'step 2 shown');
  click(q('[data-wcount="4"]'));
  // change Wednesday to Yoga
  const sel=q('[data-wday="2"]'); sel.value='Yoga'; sel.dispatchEvent(new w.Event('change',{bubbles:true}));
  click(q('[data-wnext]'));
  ok(/Your plan/.test(d.getElementById('wiz').textContent),'step 3 summary shown');
  console.log('   summary:', d.getElementById('wiz').textContent.replace(/\s+/g,' ').slice(0,300));
  click(q('[data-wfinish]'));
  const t=w.__t, P=t.state.profile;
  ok(d.getElementById('wiz').hidden,'wizard closed after finish');
  ok(P.setup===true && P.planType==='generated' && P.goal==='10k' && P.level==='some','profile written');
  ok(P.days[2]==='Yoga','Yoga on Wednesday');
  ok(t.sessions().length>0,'sessions created: '+t.sessions().length);
  ok(t.sessions().some(s=>s.race),'race session exists');
  ok(/Week 1|Week \d/.test(d.getElementById('thisweek').textContent),'week view rendered');
  const saved=JSON.parse(w.localStorage.getItem('localfit-state'));
  ok(saved.profile.setup===true,'saved to localStorage');
  ok(errors.length===0,'no script errors in flow '+errors.slice(0,2).join(' | '));
  // settings page
  t.render();
  w.document.getElementById('settingsBtn').dispatchEvent(new w.MouseEvent('click',{bubbles:true}));
  const st=d.getElementById('settings').textContent.replace(/\s+/g,' ');
  ok(/Your plan/.test(st)&&/sessions per week/.test(st),'settings shows plan summary');
  console.log('   ',st.slice(0,260));
}

// ---- T2b: fit goal with no running, German
{
  const {w,errors}=load(NEW);
  const d=w.document, click=el=>el.dispatchEvent(new w.MouseEvent('click',{bubbles:true})), q=s=>d.querySelector(s);
  click(q('[data-wlang="de"]'));
  ok(/Willkommen/.test(d.getElementById('wiz').textContent),'German wizard');
  click(q('[data-wgoal="fit"]'));
  click(q('[data-wnext]'));
  for(let i=0;i<7;i++){ const s=q('[data-wday="'+i+'"]'); s.value=['Kraft','Aus','Yoga','Aus','Bouldern','Aus','Aus'][i]; s.dispatchEvent(new w.Event('change',{bubbles:true})); }
  click(q('[data-wnext]'));
  click(q('[data-wfinish]'));
  const t=w.__t;
  ok(t.runs().length===0,'no runs in plan');
  ok(t.sessions().length===12*3,'36 sessions in 12 weeks, got '+t.sessions().length);
  ok(d.getElementById('wiz').hidden,'closed');
  ok(/Sitzung|Einheit|Woche/.test(d.getElementById('stats').textContent),'hero stats without runs: '+d.getElementById('stats').textContent.replace(/\s+/g,' '));
  w.document.querySelector('[data-tab="stats"]').dispatchEvent(new w.MouseEvent('click',{bubbles:true}));
  ok(errors.length===0,'no errors '+errors.slice(0,3).join(' | '));
}
console.log(fails? ('\n'+fails+' FAILED'):'\nALL OK');
process.exit(fails?1:0);
