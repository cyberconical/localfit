const {load}=require('./harness');
const NEW=require('path').join(__dirname,'..','index.html');
const {w}=load(NEW); const t=w.__t, H=w.HMTrk;
let fails=0, checked=0; const bad=[];
const fail=(ctx,m)=>{ fails++; if(bad.length<25) bad.push(ctx+' :: '+m); };

const day=(d)=> (d.getDay()+6)%7;
const dayPatterns=[
  ['Aus','Aus','Lauf','Aus','Aus','Aus','Lauf'],
  ['Aus','Lauf','Aus','Kraft','Aus','Aus','Lauf'],
  ['Aus','Lauf','Kraft','Aus','Lauf','Aus','Lauf'],
  ['Kraft','Lauf','Stretching','Lauf','Aus','Aus','Lauf'],
  ['Lauf','Lauf','Lauf','Lauf','Lauf','Aus','Lauf'],
  ['Lauf','Lauf','Lauf','Lauf','Lauf','Lauf','Lauf'],
  ['Aus','Aus','Aus','Aus','Aus','Aus','Lauf'],
  ['Aus','Aus','Lauf','Aus','Aus','Lauf','Aus'],
  ['Kraft','Bouldern','Aus','Yoga','Aus','Schwimmen','Rad'],  // no running at all
];
const profile=(goal,level,days,hasTime,raceKey,weeks)=>({...t.state.profile, planType:'generated', goal, level, weeks, raceDate:raceKey, goalSec:hasTime?3600*(GOALK[goal]/10):0, days});
const GOALK={ '5k':5,'10k':10,'hm':21.0975,'marathon':42.195,'fit':0 };

const today=t.todayNow();
for(const lang of ['en','de']){
 t.setLang(lang,true);
 for(const goal of t.GOALORDER) for(const level of t.LEVELS) for(const days of dayPatterns) for(const hasTime of [false,true]) for(const raceDow of [6,3,0]) for(const weeksOut of [3,9,15,28,60]){
  const g=t.GOALS[goal];
  if(g.km && !days.includes('Lauf')) continue;   // blocked by the wizard
  // race date: weeksOut weeks from now, moved to the weekday raceDow (0=Mon .. 6=Sun)
  let rk=''; if(g.km){ let d=t.addDays(today,weeksOut*7); d=t.addDays(d, raceDow-day(d)); rk=t.dayKey(d); }
  const pp=t.planParams(goal,level,rk,today);
  const ctx=`${lang}/${goal}/${level}/${days.map(x=>x[0]).join('')}/time=${hasTime}/dow=${raceDow}/out=${weeksOut}`;
  if(pp.weeks<g.min[level]||pp.weeks>g.max[level]) fail(ctx,'weeks out of range '+pp.weeks);
  if(day(pp.start)!==0) fail(ctx,'start is not a Monday');
  const P=profile(goal,level,days,hasTime&&g.km>0,pp.raceKey,pp.weeks);
  let b; try{ b=t.buildGenerated(P); }catch(e){ fail(ctx,'throws '+e.message); continue; }
  checked++;
  const N=pp.weeks, S=b.sessions, ids=new Set();
  if(+b.start!==+pp.start) fail(ctx,'start mismatch');
  if(b.weeks.length!==N) fail(ctx,'weeks length');
  for(const s of S){
    if(ids.has(s.id)) fail(ctx,'dup id '+s.id); ids.add(s.id);
    if(s.week<1||s.week>N) fail(ctx,'week range '+s.id);
    const mon=t.addDays(pp.start,(s.week-1)*7); if(!(s.date>=mon && s.date<=t.addDays(mon,6))) fail(ctx,'date outside week '+s.id);
    if(!s.t||!s.d) fail(ctx,'empty text '+s.id);
    if(/undefined|NaN|\{HMP\}|about\s+\/km|\{x\}|\[object/.test(s.t+' '+s.d)) fail(ctx,'bad text '+s.id+': '+s.t+' / '+s.d);
    if(s.kind==='run' && !(s.min>=0)) fail(ctx,'bad min '+s.id);
    if(s.kind==='run' && !s.race && s.min<15) fail(ctx,'tiny run '+s.id+' '+s.min);
    if(s.kind==='run' && s.min>240) fail(ctx,'huge run '+s.id+' '+s.min);
    if(s.kind==='run' && !days.includes('Lauf')) fail(ctx,'run without run day');
  }
  const nonAus=days.filter(x=>x!=='Aus').length;
  if(g.km){
    const races=S.filter(s=>s.race);
    if(days.includes('Lauf')||true){
      if(races.length!==1) fail(ctx,'races='+races.length);
      else {
        if(+races[0].date!==+t.fromKey(pp.raceKey)) fail(ctx,'race date');
        if(races[0].week!==N) fail(ctx,'race week');
        if(S.some(s=>s.date>races[0].date)) fail(ctx,'sessions after race');
      }
    }
  } else if(S.some(s=>s.race)) fail(ctx,'race in fit plan');
  // full weeks (not final) have one session per non-free day
  for(let wk=1; wk<N; wk++){ const c=S.filter(s=>s.week===wk).length; if(c!==nonAus) fail(ctx,`week ${wk} has ${c} sessions, expected ${nonAus}`); }
  // long runs: last run of each week
  const runsByWeek=[]; for(let wk=1;wk<=N;wk++) runsByWeek.push(S.filter(s=>s.week===wk&&s.kind==='run'&&!s.race));
  const longs=runsByWeek.map(r=>r.length?Math.max(...r.map(x=>x.min)):0);
  const peak=Math.max(...longs);
  if(g.km && peak>g.peak+5) fail(ctx,'peak '+peak+' > '+g.peak);
  if(days.includes('Lauf') && g.km && N>=g.min[level]){ /* long run should reach at least 70% of the goal peak on solid plans */ }
  // structure: parseSegments must give >=2 segments for interval-like descriptions
  for(const s of S){ if(s.kind!=='run'||s.race) continue;
    const segs=H.parseSegments(s.d,s.min);
    const structured=/×|warm-up|Min\. ein|min fast|Min\. zügig|fartlek|Tempowechsel|Tempo anziehen|last \d+ min|letzten/.test(s.d);
    if(structured && segs.length<2) fail(ctx,'no segments for "'+s.d+'"');
    if(/goal pace|Zieltempo/.test(s.d) && !segs.some(x=>x.label==='hmp')) fail(ctx,'goal pace not recognised: '+s.d+' -> '+JSON.stringify(segs.map(x=>x.label)));
    const total=segs.reduce((a,x)=>a+x.sec,0)/60; if(segs.length && total>s.min*1.35+5) fail(ctx,`segments ${total.toFixed(0)} min vs planned ${s.min}: ${s.d}`);
  }
  // weekly total ramp (non-recovery, non-taper): compare with previous week
  const tot=runsByWeek.map(r=>r.reduce((a,x)=>a+x.min,0));
  for(let wk=2; wk<=N; wk++){ const phase=b.weeks[wk-1].phase; if(phase==='taper') continue; if(tot[wk-2]>0 && tot[wk-1] > tot[wk-2]*1.6 && tot[wk-1]-tot[wk-2]>25 && !/Breathe|Durchatmen/.test(b.weeks[wk-2].title.en+b.weeks[wk-2].title.de)) fail(ctx,`ramp wk${wk}: ${tot[wk-2]} -> ${tot[wk-1]}`); }
  // phases cover all weeks contiguously
  let cov=0; for(const ph of b.phases){ if(ph.weeks[0]!==cov+1) fail(ctx,'phase gap'); cov=ph.weeks[1]; } if(cov!==N) fail(ctx,'phases do not cover '+cov+'/'+N);
  // titles
  b.weeks.forEach((x,i)=>{ const tt=t.pick(x.title); if(!tt) fail(ctx,'empty title wk'+(i+1)); });
 }
}
console.log('checked',checked,'plans; failures',fails);
bad.forEach(x=>console.log(' ',x));
process.exit(fails?1:0);
