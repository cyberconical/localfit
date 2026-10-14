// Builds a demo data set (a 10 km plan, a few weeks in) with the app's own plan generator, for screenshots.
// node tools/demo-state.js > demo-state.json
const path = require("path");
const { load } = require("./harness");
const { w } = load(path.join(__dirname, "..", "index.html"));
const t = w.__t, H = w.HMTrk;
t.setLang("en", true);

const today = t.todayNow();
const day = d => (d.getDay() + 6) % 7;
const monday = t.addDays(today, -day(today));
// plan of 14 weeks that started ten weeks ago: today lies in week 11, race day is a Sunday three weeks ahead
const raceKey = t.dayKey(t.addDays(monday, 3 * 7 + 6));
const P = Object.assign({}, t.state.profile, {
  setup: true, planType: "generated", goal: "10k", level: "some", weeks: 14, raceDate: raceKey,
  goalSec: 3000, problem: "Knee", lang: "en",
  days: ["Kraft", "Lauf", "Aus", "Lauf", "Bouldern", "Aus", "Lauf"]
});
t.state.profile = P;
t.applyProfile();
const S = t.sessions();

// A loop around a large open field (no streets to cross), about 6 km, with a little GPS wobble.
function loop(n, seed, k) {
  const pts = []; let s = seed;
  const rnd = () => (s = (s * 1664525 + 1013904223) % 4294967296) / 4294967296 - 0.5;
  const c = [52.4745, 13.4015], a = 0.0112 * (k || 1), b = 0.0095 * (k || 1);   // lat/lon half axes
  for (let i = 0; i <= n; i++) {
    const th = (i / n) * 2 * Math.PI - Math.PI / 2;
    // a rounded rectangle-like shape (superellipse)
    const ex = 2.6, x = Math.sign(Math.cos(th)) * Math.pow(Math.abs(Math.cos(th)), 2 / ex), y = Math.sign(Math.sin(th)) * Math.pow(Math.abs(Math.sin(th)), 2 / ex);
    const m = 1 + 0.10 * Math.sin(2 * th + 1) + 0.07 * Math.sin(3 * th + 0.4);
    pts.push([c[0] + a * y * m + rnd() * 0.00004, c[1] + b * x * m + rnd() * 0.00005]);
  }
  return pts;
}
const enc = pts => (H.encode ? H.encode(pts) : null);

const logs = {}, strength = {};
let last = null;
for (const s of S) {
  if (s.date >= today) continue;
  if (s.kind === "run") {
    const secPerKm = 355 + (s.week % 3) * 8 - s.week * 2;   // getting faster
    const km = Math.round((s.min * 60 / secPerKm) * 10) / 10;
    const sec = Math.round(km * secPerKm);
    logs[s.id] = { km, sec, feel: [3, 4, 3, 5, 4][(s.week + s.date.getDate()) % 5], knee: "gut", shoe: s.week % 2 ? "normal" : "barfuss", tod: ["morgen", "abend", "morgen"][s.week % 3], ts: +s.date + 36e5 * 8 };
    last = s.id;
  } else strength[s.id] = true;
}
// the five most recent runs get a recorded route around the same open field; long runs are several laps of a loop of up to 6.4 km
const len = pp => pp.slice(1).reduce((s, q, i) => s + H.hav(pp[i], q), 0);
const base = len(loop(120, 7, 1));
const routed = Object.keys(logs).filter(k => logs[k].km >= 3).sort((x, y) => logs[y].ts - logs[x].ts).slice(0, 5);
routed.forEach((id, n) => {
  const l = logs[id], laps = Math.max(1, Math.ceil(l.km / 6.4));
  let pts = [];
  for (let k = 0; k < laps; k++) pts = pts.concat(loop(120, 7 + n * 13 + k * 5, (l.km * 1000 / laps) / base));
  pts = pts.map(p => [p[0] + (n % 3 - 1) * 0.0005, p[1] + ((n + 1) % 3 - 1) * 0.0007]);
  const sp = []; for (let i = 0; i < Math.floor(l.km); i++) sp.push(Math.round(l.sec / l.km + (i % 3 - 1) * 6 + (i > 3 ? -4 : 0)));
  l.trk = { iv: [], sp, tail: [Math.round((l.km % 1) * 1000), Math.round((l.km % 1) * l.sec / l.km)], route: [enc(pts)] };
});
const dk = d => t.dayKey(d);
const habits = [
  { id: "h1", name: "Stretching", type: "check", unit: "", created: +t.addDays(today, -40) },
  { id: "h2", name: "Sleep (hours)", type: "number", unit: "h", created: +t.addDays(today, -40) },
  { id: "h3", name: "No sugar", type: "check", unit: "", created: +t.addDays(today, -40) }
];
const habitLog = { h1: {}, h2: {}, h3: {} };
for (let i = 1; i <= 21; i++) {
  const k = dk(t.addDays(today, -i));
  habitLog.h1[k] = i % 4 === 0 ? "o" : "x";
  habitLog.h2[k] = [7, 7.5, 6.5, 8, 7][i % 5];
  habitLog.h3[k] = i % 3 === 0 ? "o" : "x";
}
const state = {
  logs, strength, alt: {}, habits, habitLog,
  learnings: [
    { id: "l1", date: dk(t.addDays(today, -9)), ts: +t.addDays(today, -9), text: "Easy runs feel better when I start slower than I think I should.", type: "insight", tag: "Tempo", solved: false },
    { id: "l2", date: dk(t.addDays(today, -4)), ts: +t.addDays(today, -4), text: "Left knee twinges after hills. Shorter strides, more calf raises.", type: "issue", tag: "Knie", solved: false }
  ],
  profile: P,
  records: [{ id: "r1", sport: "lauf", key: "5k", name: "5 km", value: "26:40", date: dk(t.addDays(today, -60)), former: false, ts: 1 }],
  goals: [{ id: "g1", sport: "lauf", text: "10 km under 50 minutes", due: raceKey, done: false, ts: 1 }],
  workouts: [], dur: {}, edits: {}, gps: { zone: 300, save: true, test: false, voice: 0 }, updatedAt: Date.now()
};
process.stdout.write(JSON.stringify(state));
