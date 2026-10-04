#!/usr/bin/env node
// three2unity: snapshot a running Three.js page into a Unity `Assets/ThreeImport` folder. See README.md.
import fs from 'node:fs';
import http from 'node:http';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import puppeteer from 'puppeteer-core';
import { install, capture, record } from './page.mjs';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const USAGE = `usage: three2unity <page.html | http(s) url> --out <unity project dir> [options]
  --eval <js>          run in the page before capturing (repeatable): click "start", pick a mode, ...
  --wait <ms>          extra time after the scene appears (default 3000)
  --record <seconds>   also record node + camera motion into an AnimationClip (default 0 = snapshot only)
  --fps <n>            recording sample rate (default 30)
  --clip <name>        name of the recorded clip (default Recording)
  --scale <n>          Unity scale of the whole scene, e.g. 0.03 to turn 60-unit players into 1.8 m (default 1)
  --flip x|z           which axis the Unity glTF importer mirrors (default x, glTFast's convention)
  --max-texture <px>   downscale textures larger than this (default 2048)
  --browser <path>     Chrome / Edge executable (auto-detected otherwise)`;

const args = process.argv.slice(2), opt = { eval: [], wait: 3000, record: 0, fps: 30, clip: 'Recording', scale: 1, flip: 'x', maxTexture: 2048 };
let target = '';
const NUM = new Set(['wait', 'record', 'fps', 'scale', 'max-texture']);
for (let i = 0; i < args.length; i++) {
  const a = args[i];
  if (!a.startsWith('--')) { target = a; continue; }
  const k = a.slice(2), v = args[++i];
  if (v === undefined) fail(`missing value for ${a}`);
  if (k === 'eval') opt.eval.push(v);
  else if (NUM.has(k)) opt[k === 'max-texture' ? 'maxTexture' : k] = Number(v);
  else opt[k] = v;
}
if (!target || !opt.out) fail(USAGE);
if (!['x', 'z'].includes(opt.flip)) fail('--flip must be x or z');

function fail(msg) { console.error(msg); process.exit(1); }

function findBrowser() {
  const c = [opt.browser, process.env.CHROME_PATH,
    'C:/Program Files/Google/Chrome/Application/chrome.exe', 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe',
    'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe', 'C:/Program Files/Microsoft/Edge/Application/msedge.exe',
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',
    '/usr/bin/google-chrome', '/usr/bin/chromium', '/usr/bin/chromium-browser', '/usr/bin/microsoft-edge'];
  return c.find(p => p && fs.existsSync(p)) ?? fail('no Chrome/Edge found; pass --browser <path>');
}

// A local file is served over http from its own folder, since module imports and fetch() don't work from file://.
function serve(file) {
  const root = path.dirname(path.resolve(file)), TYPES = { '.html': 'text/html', '.js': 'text/javascript', '.mjs': 'text/javascript', '.json': 'application/json', '.png': 'image/png', '.jpg': 'image/jpeg', '.glb': 'model/gltf-binary', '.fbx': 'application/octet-stream', '.css': 'text/css' };
  const srv = http.createServer((req, res) => {
    const p = path.join(root, decodeURIComponent(new URL(req.url, 'http://x').pathname));
    if (!p.startsWith(root) || !fs.existsSync(p) || fs.statSync(p).isDirectory()) { res.writeHead(404).end(); return; }
    res.writeHead(200, { 'content-type': TYPES[path.extname(p)] || 'application/octet-stream' }); fs.createReadStream(p).pipe(res);
  });
  return new Promise(r => srv.listen(0, '127.0.0.1', () => r({ srv, url: `http://127.0.0.1:${srv.address().port}/${encodeURIComponent(path.basename(file))}` })));
}

const local = !/^https?:\/\//.test(target), served = local ? await serve(target) : null, url = served ? served.url : target;
const browser = await puppeteer.launch({ executablePath: findBrowser(), headless: true, defaultViewport: { width: 1280, height: 720 },
  args: ['--no-sandbox', '--ignore-gpu-blocklist', '--enable-unsafe-swiftshader', '--use-angle=swiftshader', '--autoplay-policy=no-user-gesture-required'] });
try {
  const page = await browser.newPage();
  page.on('pageerror', e => console.error('[page]', e.message));
  page.on('console', m => { if (m.type() === 'error') console.error('[page]', m.text()); });

  // Classic <script src=three.js>: hook when window.THREE is assigned. ES-module three: append the hook to the module source.
  await page.evaluateOnNewDocument(src => {
    let v; Object.defineProperty(window, 'THREE', { configurable: true, get: () => v, set(x) { v = x; try { (0, eval)(`(${src})`)(x); } catch (e) { /* CSP */ } } });
  }, install.toString());
  await page.setRequestInterception(true);
  page.on('request', async req => {
    const u = req.url();
    if (!/\/three(\.module)?(\.min)?\.js(\?.*)?$/.test(u)) return req.continue();
    try {
      const body = await (await fetch(u)).text();
      req.respond({ status: 200, contentType: 'text/javascript', headers: { 'access-control-allow-origin': '*' },
        body: `${body}\n;import * as __t2u_ns from ${JSON.stringify(u)};\n(${install.toString()})(__t2u_ns);\n` });
    } catch (e) { req.continue(); }
  });

  console.log('open', url);
  await page.goto(url, { waitUntil: 'load', timeout: 60000 });
  for (const js of opt.eval) await page.evaluate(js);
  await page.waitForFunction(() => globalThis.__t2u && (globalThis.__t2u.scene || globalThis.__t2u.scenes.size > 0), { timeout: 60000 })
    .catch(() => fail('no THREE.Scene was rendered within 60 s (see the [page] errors above; pages that bundle three need window.__t2u set by hand)'));
  await new Promise(r => setTimeout(r, opt.wait));

  console.log('capture');
  const { glb, info } = await page.evaluate(capture, { maxTexture: opt.maxTexture });
  const data = { flip: opt.flip, scale: opt.scale, hidden: info.hidden, fog: info.fog, background: info.background, camera: info.camera, lights: info.lights, clips: [] };
  if (opt.record > 0) {
    console.log(`record ${opt.record}s @ ${opt.fps} fps`);
    const rec = await page.evaluate(record, { seconds: opt.record, fps: opt.fps });
    data.clips.push({ name: opt.clip, ...rec });
    console.log(`  ${rec.times.length} frames, ${rec.tracks.length} moving nodes${rec.camera.on ? ', camera' : ''}`);
  }

  const dir = path.join(opt.out, 'Assets', 'ThreeImport');
  fs.mkdirSync(path.join(dir, 'Editor'), { recursive: true });
  fs.writeFileSync(path.join(dir, 'scene.glb'), Buffer.from(glb, 'base64'));
  fs.writeFileSync(path.join(dir, 'scene.json'), JSON.stringify(data));
  fs.copyFileSync(path.join(HERE, 'ImportThreeScene.cs'), path.join(dir, 'Editor', 'ImportThreeScene.cs'));
  fs.writeFileSync(path.join(dir, 'REPORT.md'), report(info, data));
  console.log(`wrote ${dir}  (${(glb.length * 0.75 / 1048576).toFixed(1)} MB glb, ${info.nodeCount} nodes, ${info.lights.length} lights)`);
  console.log('next: open the Unity project, install glTFast (com.unity.cloud.gltfast), then menu Three2Unity > Build Scene');
} finally {
  await browser.close();
  served?.srv.close();
}

function report(info, data) {
  const r = info.report, list = o => Object.entries(o).map(([k, v]) => `- ${k}: ${v}`).join('\n') || '- none';
  return `# three2unity report

three.js r${info.revision} · ${info.nodeCount} nodes exported · ${info.lights.length} lights · camera ${info.camera.on ? 'yes' : 'NOT FOUND'} · fog ${info.fog.on ? 'yes' : 'no'} · ${data.clips.length} recorded clip(s)

## Objects in the scene
${list(r.objects)}

## Left out of the glb
${list(r.dropped)}

## Warnings
${r.warnings.length ? [...new Set(r.warnings)].slice(0, 40).map(w => '- ' + w).join('\n') : '- none'}

## Not converted (by design)
- Game logic and input: this is a scene snapshot, not a code translator. Rebuild behaviour in C#.
- Procedural animation is only captured as a recorded clip (--record); it is not re-created as rigs or state machines.
- Custom shaders, post-processing and toon materials arrive as plain glTF materials; rebuild the look with URP / Shader Graph.
`;
}
