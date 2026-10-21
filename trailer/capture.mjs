// Records live gameplay of "Blaze vs Bedrock.html" frame by frame on a virtual clock, so every frame is a full-quality
// 1920x1080 render no matter how slow the capture is. The page's clock (performance.now, Date.now, rAF, timers) only moves
// when __step() is called; an autopilot plays the left fighter and picks a different special shot each time.
//   node capture.mjs <scenario|all>        (game served at GAME_URL, default http://localhost:8765)
// Writes public/raw/<scenario>.mp4 (30 fps, no audio) and public/raw/<scenario>.json (menu picks + mode/camera changes).
import fs from 'node:fs';
import { spawn } from 'node:child_process';
import puppeteer from '../tools/three2unity/node_modules/puppeteer-core/lib/esm/puppeteer/puppeteer-core.js';

const URL = (process.env.GAME_URL || 'http://localhost:8765') + '/Blaze%20vs%20Bedrock.html';
const EDGE = 'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe';
const FPS = 30, SUB = 2; // the game steps at 60 Hz (its auto-quality drops HD above 20 ms a frame); every 2nd frame is kept

// mode: 12bit | 32bit | 64bit | hd. cams: [second, camera id] (ids from CAMS in the game). modes: [second, mode] mid-match.
const SCENARIOS = {
  main: { a: 'haru', b: 'jin', mode: 'hd', secs: 100, cams: [[0, 'tv'], [40, 'cinematic']] },
  sari: { a: 'aoi', b: 'fubuki', mode: 'hd', secs: 50, cams: [[0, 'follow']] },
  cams: { a: 'raijin', b: 'haru', mode: 'hd', secs: 66, cams: ['tv', 'cinematic', 'follow', 'ots', 'orbit', 'fpp', 'helmet', 'cockpit', 'fixed', 'iso', 'top', 'cctv'].map((c, i) => [i * 5.5, c]) },
  modes: { a: 'haru', b: 'jin', mode: '12bit', secs: 36, cams: [[0, 'tv']], modes: [[12, '32bit'], [24, 'hd']] },
  // full TP every frame, so each shot menu can fire a different special (the montage); a recording aid, not gameplay
  specials: { a: 'haru', b: 'jin', mode: 'hd', secs: 120, cams: [[0, 'tv'], [60, 'cinematic']], fullTP: true },
};

// Runs in the page before any of its scripts: a clock that only advances in __step(ms).
function virtualClock() {
  let t = 0, rid = 0, tid = 0; const T0 = Date.now(), raf = new Map(), timers = new Map();
  performance.now = () => t; Date.now = () => T0 + t;
  window.requestAnimationFrame = cb => { raf.set(++rid, cb); return rid; };
  window.cancelAnimationFrame = id => raf.delete(id);
  const add = (cb, ms, rep, a) => { const id = ++tid; ms = Math.max(0, +ms || 0); timers.set(id, { at: t + ms, cb, rep: rep ? Math.max(1, ms) : 0, a }); return id; };
  window.setTimeout = (cb, ms, ...a) => add(cb, ms, false, a);
  window.setInterval = (cb, ms, ...a) => add(cb, ms, true, a);
  window.clearTimeout = window.clearInterval = id => timers.delete(id);
  window.__step = async ms => {
    const end = t + ms;
    for (;;) { // due timers in order, letting promise chains settle after each (timed() banners chain into the next beat)
      let id = 0, o = null;
      for (const [k, v] of timers) if (v.at <= end && (!o || v.at < o.at)) { id = k; o = v; }
      if (!o) break;
      t = Math.max(t, o.at); if (o.rep) o.at += o.rep; else timers.delete(id);
      try { typeof o.cb === 'function' ? o.cb(...o.a) : (0, eval)(o.cb); } catch (e) { console.error(e); }
      await new Promise(r => queueMicrotask(r));
    }
    t = end;
    const cbs = [...raf.values()]; raf.clear();
    for (const cb of cbs) try { cb(t); } catch (e) { console.error(e); }
    await new Promise(r => queueMicrotask(r));
  };
}

// Reads what the autopilot needs (runs in the page).
function look() {
  const B = window.BVB, cmd = document.getElementById('cmd');
  const opts = cmd.hidden ? [] : [...document.querySelectorAll('#cmdList .mv')].filter(b => !b.getAttribute('aria-disabled'))
    .map(b => ({ k: b.querySelector('.k').textContent, name: b.querySelector('.nm').textContent, tp: b.querySelector('.tp').textContent }));
  return { menu: !cmd.hidden, title: document.getElementById('cmdTitle').textContent, opts, over: !document.getElementById('overScreen').hidden,
    hx: B.haru.x, hy: B.haru.y, jx: B.jin.x, jy: B.jin.y, CX: B.CX, CY: B.CY, cam: document.getElementById('camBtn').textContent };
}

async function record(name) {
  const S = SCENARIOS[name];
  fs.mkdirSync('public/raw', { recursive: true });
  const browser = await puppeteer.launch({ executablePath: EDGE, headless: true,
    args: ['--use-angle=d3d11', '--enable-gpu', '--ignore-gpu-blocklist', '--autoplay-policy=no-user-gesture-required', '--mute-audio'],
    defaultViewport: { width: 1280, height: 720, deviceScaleFactor: 1.875 } });
  const page = await browser.newPage();
  page.on('console', m => { if (m.type() === 'error' || m.type() === 'warn') console.log(`  [page ${m.type()}]`, m.text()); });
  page.on('pageerror', e => console.log('  [pageerror]', e.message));
  await page.evaluateOnNewDocument(virtualClock);
  await page.goto(URL, { waitUntil: 'load' });
  const step = (n = 1) => page.evaluate(async (n, ms) => { for (let i = 0; i < n; i++) await window.__step(ms); }, n, 1000 / 60);
  const realWait = ms => new Promise(r => setTimeout(r, ms));
  const key = async (type, code) => page.evaluate((type, code) => window.dispatchEvent(new KeyboardEvent(type, { code, key: code, bubbles: true })), type, code);
  const press = async code => { await key('keydown', code); await key('keyup', code); };

  // lineup, mode, then wait (real time, the clock creeping) until three.js and the fighters' GLB are in
  await step(30);
  await page.evaluate((a, b) => { document.querySelector(`#pickA [data-id=${a}]`).click(); document.querySelector(`#pickB [data-id=${b}]`).click(); }, S.a, S.b);
  const setMode = m => page.evaluate(want => { const label = { '12bit': '12-Bit', '32bit': '32-Bit', '64bit': '64-Bit', hd: 'HD' }[want], b = document.getElementById('modeBtn');
    for (let i = 0; i < 4 && !b.textContent.includes(label); i++) b.click(); return b.textContent; }, m);
  // load 3D first even for a 2D start, so a mid-scenario switch to HD has its models
  console.log(' ', await setMode('hd'));
  for (let i = 0; i < 600; i++) {
    await step(2); await realWait(20);
    if (await page.evaluate(() => { const r = window.BVB.r3; return !!(r && [...r.rigs.values()].every(C => C.glb)); })) break;
  }
  console.log(' ', await setMode(S.mode));
  await page.evaluate(() => document.getElementById('startBtn').click());
  const setCam = id => page.evaluate(id => { // cycle the camera button until its label is this id's name
    const names = { tv: 'Broadcast', cinematic: 'Cinematic', follow: 'Follow', ots: 'Over-the', orbit: 'Orbit', fpp: 'First', helmet: 'Helmet', cockpit: 'Cockpit', fixed: 'Fixed', iso: 'Isometric', top: 'Top', cctv: 'CCTV' };
    const b = document.getElementById('camBtn'); for (let i = 0; i < 14 && !b.textContent.includes(names[id]); i++) b.click(); return b.textContent;
  }, id);

  const stage = await page.evaluate(() => { const r = document.getElementById('stage').getBoundingClientRect(); return { x: r.x, y: r.y, width: r.width, height: r.height }; });
  const out = `public/raw/${name}.mp4`;
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'mjpeg', '-i', '-',
    '-vf', 'scale=1920:1080:flags=lanczos', '-c:v', 'libx264', '-preset', 'medium', '-crf', '15', '-pix_fmt', 'yuv420p', out], { stdio: ['pipe', 'inherit', 'inherit'] });
  const cdp = await page.createCDPSession();
  const log = { name, lineup: [S.a, S.b], fps: FPS, events: [] };
  const cams = [...(S.cams || [])], modes = [...(S.modes || [])], used = new Map();
  const N = Math.round((+process.env.SECS || S.secs) * FPS), t0 = Date.now();
  let hold = new Set(), lastShoot = -9, menuFrames = 0;
  for (let f = 0; f < N; f++) {
    const sec = f / FPS;
    while (cams.length && cams[0][0] <= sec) { const [, id] = cams.shift(); log.events.push({ t: sec, cam: await setCam(id) }); }
    while (modes.length && modes[0][0] <= sec) { const [, m] = modes.shift(); log.events.push({ t: sec, mode: await setMode(m) }); }
    if (S.fullTP) await page.evaluate(() => { const h = window.BVB.haru; h.tp = h.ch.maxTP; });
    const s = await page.evaluate(look);
    if (s.over) { log.events.push({ t: sec, over: true }); await page.evaluate(() => document.getElementById('againBtn').click()); }
    else if (s.menu && s.opts.length) {
      // specials first, the one used least so far (variety on screen); otherwise the strongest free move
      const sp = s.opts.filter(o => o.tp !== 'Free');
      const pick = sp.length ? sp.reduce((a, b) => ((used.get(a.name) || 0) <= (used.get(b.name) || 0) ? a : b)) : s.opts[s.opts.length - 1];
      if (++menuFrames >= 14) { // let the menu read on screen for about half a second first
        menuFrames = 0; used.set(pick.name, (used.get(pick.name) || 0) + 1);
        log.events.push({ t: sec, menu: s.title, pick: pick.name, special: pick.tp !== 'Free' });
        await press(/^\d$/.test(pick.k) ? 'Digit' + pick.k : 'Digit1');
      }
    } else {
      // attack right; chase the rival when he's between us and our goal; weave; shoot near goal
      const want = new Set();
      const chase = s.jx < s.hx - 10;
      const tx = chase ? s.jx : s.CX + 400, ty = chase ? s.jy : s.CY + Math.sin(sec * 1.3) * 60;
      if (tx > s.hx + 6) want.add('KeyD'); if (tx < s.hx - 6) want.add('KeyA');
      if (ty > s.hy + 6) want.add('KeyS'); if (ty < s.hy - 6) want.add('KeyW');
      for (const k of hold) if (!want.has(k)) await key('keyup', k);
      for (const k of want) if (!hold.has(k)) await key('keydown', k);
      hold = want;
      if (!chase && s.hx > s.CX + 200 && sec - lastShoot > 1.2) { lastShoot = sec; await press('Space'); }
      if (sec - lastShoot > 6 && f % 90 === 0) await press('Space'); // skip a banner that's waiting on input
    }
    await step(SUB - 1);
    await step(1);
    const { data } = await cdp.send('Page.captureScreenshot', { format: 'jpeg', quality: 92, clip: { ...stage, scale: 1 }, captureBeyondViewport: false });
    if (!ff.stdin.write(Buffer.from(data, 'base64'))) await new Promise(r => ff.stdin.once('drain', r));
    if (f % 150 === 0) console.log(`  ${name} ${sec.toFixed(0)}/${S.secs}s  (${((Date.now() - t0) / 1000).toFixed(0)}s real)`);
  }
  ff.stdin.end(); await new Promise(r => ff.on('close', r));
  fs.writeFileSync(`public/raw/${name}.json`, JSON.stringify(log, null, 1));
  await browser.close();
  console.log(`  wrote ${out}`);
}

const which = process.argv[2] || 'all';
for (const n of which === 'all' ? Object.keys(SCENARIOS) : which.split(',')) { console.log(n); await record(n); }
