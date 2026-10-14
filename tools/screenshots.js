// Takes the app screenshots for the README and the stores from the real app, with demo data.
//   node tools/screenshots.js [outDir]
// Needs: npm install (playwright). In CI the browser comes from `npx playwright install chromium`.
// Locally set CHROMIUM=/path/to/chromium if Playwright cannot download one.
// If map/region.json and map/region/ exist (the build creates them), the map screenshots show the real basemap.
const fs = require("fs"), path = require("path"), http = require("http");
const { chromium } = require("playwright");
const { execFileSync } = require("child_process");

const ROOT = path.join(__dirname, "..");
const OUT = path.resolve(process.argv[2] || path.join(ROOT, "docs", "screenshots", "raw"));
fs.mkdirSync(OUT, { recursive: true });
const DEMO = JSON.parse(execFileSync("node", [path.join(__dirname, "demo-state.js")], { encoding: "utf8", maxBuffer: 1 << 26 }));

const MIME = { ".html": "text/html", ".js": "text/javascript", ".css": "text/css", ".woff2": "font/woff2", ".json": "application/json", ".pbf": "application/x-protobuf", ".png": "image/png", ".pmtiles": "application/octet-stream" };
const server = http.createServer((req, res) => {
  const p = path.join(ROOT, decodeURIComponent(req.url.split("?")[0]).replace(/\/$/, "/index.html"));
  if (!p.startsWith(ROOT) || !fs.existsSync(p) || fs.statSync(p).isDirectory()) { res.writeHead(404); return res.end(); }
  const buf = fs.readFileSync(p), range = req.headers.range;
  const h = { "Content-Type": MIME[path.extname(p)] || "application/octet-stream", "Accept-Ranges": "bytes" };
  if (range) { const m = /bytes=(\d*)-(\d*)/.exec(range), s = +m[1] || 0, e = m[2] ? +m[2] : buf.length - 1; res.writeHead(206, { ...h, "Content-Range": `bytes ${s}-${e}/${buf.length}`, "Content-Length": e - s + 1 }); return res.end(buf.subarray(s, e + 1)); }
  res.writeHead(200, { ...h, "Content-Length": buf.length }); res.end(buf);
});


// Fake GPS and a fast clock, so that a run of a kilometer or two can be "recorded" in about 20 seconds.
const FAKE = () => {
  const realNow = Date.now.bind(Date); let base = realNow(), vbase = base, k = 1;
  Date.now = () => vbase + (realNow() - base) * k;
  window.__warp = f => { vbase = Date.now(); base = realNow(); k = f; };
  let cb = null;
  navigator.geolocation.watchPosition = c => { cb = c; return 1; };
  navigator.geolocation.clearWatch = () => {};
  navigator.geolocation.getCurrentPosition = c => c({ coords: { latitude: 52.4745, longitude: 13.4015, accuracy: 6, speed: null }, timestamp: Date.now() });
  window.__fix = (lat, lon, acc, speed) => { if (cb) cb({ coords: { latitude: lat, longitude: lon, accuracy: acc, speed }, timestamp: Date.now() }); };
};

const W = 390, H = 845, DPR = 3;   // 1170 x 2535, the same 1 : 2.17 as a current phone (and as the old map screens)
const hasMap = fs.existsSync(path.join(ROOT, "map", "region.json"));

async function newPage(browser, { state, dark, lang, geo, fake }) {
  const ctx = await browser.newContext({
    viewport: { width: W, height: H }, deviceScaleFactor: DPR, isMobile: true, hasTouch: true,
    colorScheme: dark ? "dark" : "light", locale: lang === "de" ? "de-DE" : "en-US",
    timezoneId: "Europe/Berlin", geolocation: geo || { latitude: 52.4745, longitude: 13.4015, accuracy: 8 }, permissions: ["geolocation"]
  });
  const page = await ctx.newPage();
  if (fake) await page.addInitScript(FAKE);
  page.on("pageerror", e => console.log("pageerror:", e.message));
  if (state) await page.addInitScript(s => { try { localStorage.setItem("localfit-state", s); } catch (e) {} }, JSON.stringify(Object.assign({}, state, lang ? { profile: Object.assign({}, state.profile, { lang }) } : {})));
  await page.goto(`http://127.0.0.1:${PORT}/index.html`);
  await page.waitForTimeout(700);
  return { page, ctx };
}
const snap = async (page, name) => { await page.waitForTimeout(500); await page.screenshot({ path: path.join(OUT, name + ".png") }); console.log("shot", name); };
const click = async (page, sel) => { await page.click(sel); await page.waitForTimeout(350); };
let PORT;

(async () => {
  await new Promise(r => server.listen(0, "127.0.0.1", r)); PORT = server.address().port;
  const browser = await chromium.launch({
    executablePath: process.env.CHROMIUM || undefined,
    args: ["--use-gl=angle", "--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist", "--enable-webgl"]
  });
  const only = process.env.ONLY ? process.env.ONLY.split(",") : null;
  const want = n => !only || only.includes(n);

  // 1 setup (first start)
  if (want("01-setup")) { const { page, ctx } = await newPage(browser, {}); await snap(page, "01-setup"); await ctx.close(); }
  // 2 setup, week step
  if (want("02-setup-week")) {
    const { page, ctx } = await newPage(browser, {});
    await click(page, '[data-wgoal="10k"]'); await click(page, '[data-wlevel="some"]'); await click(page, "[data-wnext]");
    await click(page, '[data-wcount="4"]'); await snap(page, "02-setup-week"); await ctx.close();
  }
  // 3 the plan, this week
  if (want("03-week")) {
    const { page, ctx } = await newPage(browser, { state: DEMO });
    await page.evaluate(() => { const o = document.querySelector('#thisweek [aria-expanded="true"]'); if (o) o.click(); });
    await page.waitForTimeout(300);
    await page.evaluate(() => { const y = document.querySelector("#thisweek .sess-head").getBoundingClientRect().top + scrollY - 84; scrollTo(0, y); });
    await snap(page, "03-week"); await ctx.close();
  }
  // 4 a finished run with its route
  if (want("04-run")) {
    const { page, ctx } = await newPage(browser, { state: DEMO });
    const id = Object.keys(DEMO.logs).filter(k => DEMO.logs[k].trk).sort((a, b) => DEMO.logs[b].km - DEMO.logs[a].km)[0];
    const wk = id.match(/^w(\d+)-/)[1];
    await page.evaluate(w => { const d = document.querySelector(`details[data-week="${w}"]`); d.querySelector("summary").click(); }, wk);
    await page.waitForTimeout(400);
    await page.evaluate(i => document.querySelector(`[data-toggle="${i}"]`).click(), id);
    await page.waitForTimeout(600);
    // the fold button of this session's route section
    await page.evaluate(i => {
      const head = document.querySelector(`[data-toggle="${i}"]`);
      let box = head.parentElement;
      const btn = [...box.querySelectorAll("*")].find(e => e.children.length === 0 && /^Route and kilometers$/.test(e.textContent.trim()));
      (btn.closest("button") || btn).click();
    }, id);
    await page.waitForTimeout(1800);
    await page.evaluate(i => {
      const box = document.querySelector(`[data-toggle="${i}"]`).parentElement;
      const el = [...box.querySelectorAll("*")].find(e => e.children.length === 0 && /^Route and kilometers$/.test(e.textContent.trim()));
      scrollTo(0, el.getBoundingClientRect().top + scrollY - 84);
    }, id);
    await snap(page, "04-run"); await ctx.close();
  }
  // 5 stats
  if (want("05-stats")) { const { page, ctx } = await newPage(browser, { state: DEMO }); await click(page, '[data-tab="stats"]'); await snap(page, "05-stats"); await ctx.close(); }
  // 5b all routes on one map
  if (want("05b-routes")) {
    const { page, ctx } = await newPage(browser, { state: DEMO });
    await click(page, '[data-tab="stats"]');
    await page.waitForTimeout(1500);
    await page.evaluate(() => { const h = [...document.querySelectorAll("h3")].find(e => /Your routes/.test(e.textContent)); scrollTo(0, h.getBoundingClientRect().top + scrollY - 84); });
    await snap(page, "05b-routes"); await ctx.close();
  }
  // 6 habits
  if (want("06-habits")) { const { page, ctx } = await newPage(browser, { state: DEMO }); await click(page, '[data-tab="habits"]'); await snap(page, "06-habits"); await ctx.close(); }
  // 7 dark
  if (want("07-dark")) { const { page, ctx } = await newPage(browser, { state: DEMO, dark: true }); await snap(page, "07-dark"); await ctx.close(); }
  // 8 German
  if (want("08-german")) { const { page, ctx } = await newPage(browser, { state: DEMO, lang: "de" }); await snap(page, "08-german"); await ctx.close(); }
  // 9 live recording (with the live map if a basemap is bundled)
  if (want("09-live")) {
    const { page, ctx } = await newPage(browser, { state: DEMO, fake: true });
    const id = Object.keys(DEMO.logs).filter(k => DEMO.logs[k].trk).sort((a, b) => DEMO.logs[b].km - DEMO.logs[a].km)[0];
    const pts = await page.evaluate(r => HMTrk.decode(r), DEMO.logs[id].trk.route[0]);
    // today's or the next planned run
    const sid = await page.evaluate(() => { const b = [...document.querySelectorAll("[data-toggle]")].map(e => e.dataset.toggle); return b; });
    const next = (await page.evaluate(() => { const c = document.querySelector("[data-gps]"); return c ? c.dataset.gps : null; })) || sid[0];
    await page.evaluate(i => { const el = document.querySelector(`[data-toggle="${i}"]`); if (el && el.getAttribute("aria-expanded") !== "true") el.click(); }, next);
    await page.waitForTimeout(300);
    await page.evaluate(i => document.querySelector(`[data-gps="${i}"]`).click(), next);
    await page.waitForTimeout(500);
    await page.evaluate(() => document.querySelector("[data-rstart]").click());
    await page.waitForTimeout(800);
    await page.evaluate(() => __warp(30));
    // walk along the route at about 5:40 min/km: one fix per 4.5 simulated seconds, 150 ms real time
    const stepM = 2.95 * 4.5; let carry = 0, seg = 0, done = 0;
    const R = 6371000, rad = Math.PI / 180, dist = (a, b) => 2 * R * Math.asin(Math.sqrt(Math.sin((b[0] - a[0]) * rad / 2) ** 2 + Math.cos(a[0] * rad) * Math.cos(b[0] * rad) * Math.sin((b[1] - a[1]) * rad / 2) ** 2));
    const targetM = 1650; let cur = pts[0], travelled = 0, idx = 1;
    while (travelled < targetM && idx < pts.length) {
      let need = stepM;
      while (need > 0 && idx < pts.length) {
        const d = dist(cur, pts[idx]);
        if (d <= need) { need -= d; cur = pts[idx]; idx++; }
        else { const f = need / d; cur = [cur[0] + (pts[idx][0] - cur[0]) * f, cur[1] + (pts[idx][1] - cur[1]) * f]; need = 0; }
      }
      travelled += stepM;
      await page.evaluate(([la, lo]) => __fix(la, lo, 5, 2.95), cur);
      await page.waitForTimeout(150);
    }
    await page.evaluate(() => __warp(1));
    await page.waitForTimeout(1500);
    await snap(page, "09-live"); await ctx.close();
  }
  console.log("map bundled:", hasMap);
  await browser.close(); server.close();
})().catch(e => { console.error(e); process.exit(1); });
