const fs=require('fs');
const {JSDOM,VirtualConsole}=require('jsdom');

const INJECT = `
window.__t={
  get state(){return state}, set state(v){state=v},
  buildGenerated, planParams, applyProfile, normalize, render, wizOpen, GOALS, LEVELS, DAYSETS, DAYTOKENS, GOALORDER,
  sessions:()=>SESSIONS, runs:()=>RUNS, phases:()=>PHASES, start:()=>START, race:()=>RACE, nw:()=>NW, weeks:()=>GENWEEKS,
  setLang, todayNow, dayKey, fromKey, addDays, tr, pick, parseGoalFor, goalDist, hasGoalTime, wz:()=>WZ
};`;

function load(file, opts={}){
  let html=fs.readFileSync(file,'utf8');
  const re=/\}\)\(\);\n<\/script>\n<\/body>/;
  if(!re.test(html)) throw new Error('inject point not found');
  html=html.replace(re, (opts.inject||INJECT)+"\n})();\n</script>\n</body>");
  const vc=new VirtualConsole(); const errors=[];
  vc.on('jsdomError',e=>errors.push('jsdomError: '+(e.detail&&e.detail.stack||e.message)));
  vc.on('error',e=>errors.push('console.error: '+e));
  const dom=new JSDOM(html,{runScripts:'dangerously',url:'http://localhost/',pretendToBeVisual:true,virtualConsole:vc,
    beforeParse(w){
      w.matchMedia=w.matchMedia||(()=>({matches:false,addEventListener(){},removeEventListener(){},addListener(){},removeListener(){}}));
      w.scrollTo=()=>{}; w.Element.prototype.scrollTo=()=>{}; w.Element.prototype.scrollIntoView=()=>{};
      w.confirm=()=>true;
      if(opts.storage) for(const k in opts.storage) w.localStorage.setItem(k,typeof opts.storage[k]==='string'?opts.storage[k]:JSON.stringify(opts.storage[k]));
    }});
  return {w:dom.window, errors, dom};
}
module.exports={load};
