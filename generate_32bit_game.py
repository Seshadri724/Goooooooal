import sys

# Read the original backup
with open(r"c:\SESHU\PROJECTS\OTHER PROJECTS\FOOTBALL\Blaze vs Bedrock.backup.html", "r", encoding="utf-8") as f:
    text = f.read()

# 1. Update font link to include Press Start 2P alongside Dela Gothic One, Zen Kaku Gothic New, and Azeret Mono
text = text.replace(
    '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Dela+Gothic+One&family=Zen+Kaku+Gothic+New:wght@400;500;700&family=Azeret+Mono:wght@500;700&display=swap">',
    '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Dela+Gothic+One&family=Zen+Kaku+Gothic+New:wght@400;500;700&family=Azeret+Mono:wght@500;700&display=swap">'
)

# 2. Update CSS variables to include both 32-bit and 12-bit tokens
css_root_old = """:root{
  color-scheme: dark;
  --night:#0b1020; --panel:#141c33; --panel2:#1a2442; --line:#28335a; --ink:#eef1f8; --mute:#98a3c2;
  --tension:#ffe14d; --flame:#ff5a36; --gale:#35d6c0; --stone:#e0a93f; --basic:#9aa6b8;
  --display:"Dela Gothic One","Arial Black",Impact,sans-serif;
  --body:"Zen Kaku Gothic New",system-ui,-apple-system,"Segoe UI",sans-serif;
  --mono:"Azeret Mono",ui-monospace,"SFMono-Regular",Menlo,monospace;
}"""

css_root_new = """:root{
  color-scheme: dark;
  --night:#080c18; --panel:#141c33; --panel2:#1a2442; --line:#28335a; --line-glow:rgba(53,214,192,.3); --ink:#eef1f8; --mute:#98a3c2;
  --tension:#ffe14d; --flame:#ff5a36; --flame-glow:rgba(255,90,54,.45); --gale:#35d6c0; --gale-glow:rgba(53,214,192,.45); --stone:#e0a93f; --stone-glow:rgba(224,169,63,.45); --basic:#9aa6b8;
  --display:"Dela Gothic One","Arial Black",Impact,sans-serif;
  --body:"Zen Kaku Gothic New",system-ui,-apple-system,"Segoe UI",sans-serif;
  --mono:"Azeret Mono",ui-monospace,"SFMono-Regular",Menlo,monospace;
  --pixel:"Press Start 2P",monospace;
}
/* 12-bit mode theme override */
body.mode-12bit {
  --night:#012; --panel:#123; --panel2:#124; --line:#235; --ink:#def; --mute:#89a;
  --tension:#fe3; --flame:#f62; --gale:#3db; --stone:#b83; --basic:#89a;
  --display:"Press Start 2P",monospace;
}
body.mode-12bit .stage { border-radius:0!important; background:#000!important; box-shadow:0 0 0 2px var(--line)!important; }
body.mode-12bit .stage canvas { image-rendering:pixelated!important; }
body.mode-12bit .screen { border-radius:0!important; background:rgba(0,17,34,.94)!important; border:2px solid var(--line)!important; }
body.mode-12bit .cmd { border-radius:0!important; border:2px solid var(--line)!important; backdrop-filter:none!important; }
body.mode-12bit .mv { border-radius:0!important; border:2px solid var(--line)!important; }
body.mode-12bit .btn { border-radius:0!important; border:2px solid var(--line)!important; font-family:var(--pixel)!important; font-size:10px!important; }
body.mode-12bit .primary { border-radius:0!important; transform:none!important; box-shadow:0 4px 0 #971!important; font-family:var(--pixel)!important; font-size:12px!important; }
body.mode-12bit .primary span { transform:none!important; }
body.mode-12bit .card { border-radius:0!important; border:2px solid var(--line)!important; }
body.mode-12bit .pf { border-radius:0!important; border:2px solid var(--line)!important; image-rendering:pixelated!important; }
body.mode-12bit .stick { border-radius:0!important; border:2px solid var(--line)!important; background:#012!important; }
body.mode-12bit .knob { border-radius:0!important; border:2px solid var(--mute)!important; }
body.mode-12bit .act { border-radius:0!important; border:2px solid var(--line)!important; font-family:var(--pixel)!important; font-size:11px!important; }
"""

assert css_root_old in text, "css_root_old not found"
text = text.replace(css_root_old, css_root_new)

# 3. Enhance stage styling with subtle 32-bit glow and support centering
old_stage = """.stage{position:relative;width:100%;max-width:100%;aspect-ratio:16/9;border-radius:12px;overflow:hidden;background:#0a0f1d;box-shadow:0 0 0 1px var(--line),0 40px 80px -40px rgba(0,0,0,.9);outline:none}
.stage canvas{display:block;width:100%;height:100%}"""

new_stage = """.stage{position:relative;width:100%;max-width:100%;aspect-ratio:16/9;border-radius:12px;overflow:hidden;background:#080c18;box-shadow:0 0 0 1px var(--line),0 30px 60px -20px rgba(0,0,0,.85),0 0 40px -10px var(--line-glow);outline:none;display:flex;align-items:center;justify-content:center}
.stage canvas{display:block;width:100%;height:100%;image-rendering:auto}"""

assert old_stage in text, "old_stage not found"
text = text.replace(old_stage, new_stage)

# 4. Header Tools: Add Mode Toggle Button (32-Bit Arcade / 12-Bit Amiga) + 12-Bit Palette & Mock Buttons
old_tools = """    <div class="tools">
      <button type="button" class="btn" id="muteBtn" aria-pressed="false">Sound: on</button>
      <button type="button" class="btn" id="restartBtn">Restart match</button>
    </div>"""

new_tools = """    <div class="tools">
      <button type="button" class="btn" id="modeBtn" style="color:var(--tension);border-color:var(--tension);font-weight:700" title="Switch between 32-Bit Arcade and 12-Bit Amiga Mode">Mode: 32-Bit Arcade</button>
      <button type="button" class="btn" id="muteBtn" aria-pressed="false">Sound: on</button>
      <button type="button" class="btn" id="restartBtn">Restart match</button>
      <button type="button" class="btn" id="palBtn" style="display:none" title="Audit on-screen palette (32 colors max)">Palette: 32c [P]</button>
      <button type="button" class="btn" id="mockBtn" style="display:none" title="Toggle 320x180 mock scene">Mock: 320x180 [M]</button>
    </div>"""

assert old_tools in text, "old_tools not found"
text = text.replace(old_tools, new_tools)

# 5. Header kicker update
text = text.replace(
    '<p class="kicker">1v1 duel prototype · mini-pitch</p>',
    '<p class="kicker" id="kickerTag">32-Bit Arcade Edition · 1v1 duel prototype</p>'
)

# 6. JavaScript engine replacement
# Let's inspect from `const W = 960, H = 540;` to the end of the script tag!
idx_script_start = text.find("const W = 960, H = 540;")
idx_script_end = text.find("})();\n</script>")
assert idx_script_start != -1 and idx_script_end != -1, "Script boundaries not found"

js_code = """// ============================================================================
// DUAL-PIPELINE ENGINE: 32-BIT ARCADE (DEFAULT) & 12-BIT AMIGA RETRO
// ============================================================================
let engineMode = '32bit'; // '32bit' (default) or '12bit'
let mockMode = false;

// 32-Bit TrueColor Master Constants (Native 960x540 Arcade Space)
const W = 960, H = 540;
const F = { x0: 60, y0: 62, x1: 900, y1: 506 };
const CX = (F.x0 + F.x1) / 2, CY = (F.y0 + F.y1) / 2;
const GY0 = CY - 60, GY1 = CY + 60;
const GOALS_TO_WIN = 3;
const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;

// 12-Bit Amiga Pipeline Constants (320x180 internal, 1/3 scale)
const LW = 320, LH = 180;
const PALETTE_32 = [
  '#000', '#012', '#123', '#235', '#456', '#89a', '#def', '#fff',
  '#fe3', '#ca1',
  '#f21', '#f62', '#fa4',
  '#076', '#3db', '#bfd',
  '#641', '#b83', '#ec7',
  '#152', '#173', '#bea', '#042',
  '#942', '#c32', '#347',
  '#fba', '#d97', '#eb9', '#611', '#4b6', '#76d'
];

// Elements in 32-Bit TrueColor & 12-Bit Hex
const ELEM = {
  flame: { name: 'Flame', c: '#ff5a36', g: '#ffc163', d: '#3a0d08', c12: '#f62', g12: '#fa4', d12: '#410' },
  gale:  { name: 'Gale',  c: '#35d6c0', g: '#c9fff6', d: '#062a2a', c12: '#3db', g12: '#bfd', d12: '#033' },
  stone: { name: 'Stone', c: '#e0a93f', g: '#fff1c9', d: '#2b1d07', c12: '#b83', g12: '#ec7', d12: '#320' },
  none:  { name: 'Basic', c: '#9aa6b8', g: '#ffffff', d: '#141a2a', c12: '#89a', g12: '#fff', d12: '#123' },
};
const BEATS = { flame: 'gale', gale: 'stone', stone: 'flame' };
const KIND = { shot: 'Shot', dribble: 'Dribble', block: 'Block' };
const BASIC = {
  shot:    { name: 'Power Shot',   kind: 'shot',    elem: 'none', power: 18, tp: 0 },
  dribble: { name: 'Push Through', kind: 'dribble', elem: 'none', power: 15, tp: 0 },
  block:   { name: 'Tackle',       kind: 'block',   elem: 'none', power: 15, tp: 0 },
};
const HARU = {
  id: 'haru', name: 'Haru Kagari', short: 'HARU', team: 'Akebono FC', role: 'Striker', elem: 'flame', num: 9,
  jersey: '#f2f4f8', trim: '#e0402a', hair: '#c41f2e', hairHi: '#ff7a52', brow: '#6e0e17', skin: '#f3caa4', eye: '#f6b92f',
  stats: { kick: 80, dribble: 70, block: 56, speed: 74 }, maxTP: 120,
  bio: 'Akebono’s first-year striker. Huge shots, thin defence. Gale Sweep and Tempest Drive are his only answers to Stone.',
  moves: [
    { name: 'Crimson Meteor', kind: 'shot',    elem: 'flame', power: 62, tp: 45 },
    { name: 'Tempest Drive',  kind: 'shot',    elem: 'gale',  power: 44, tp: 26 },
    { name: 'Blaze Step',     kind: 'dribble', elem: 'flame', power: 38, tp: 18 },
    { name: 'Gale Sweep',     kind: 'block',   elem: 'gale',  power: 36, tp: 20 },
  ],
};
const JIN = {
  id: 'jin', name: 'Jin Kurogane', short: 'JIN', team: 'Tetsuzan Academy', role: 'Libero', elem: 'stone', num: 5,
  jersey: '#252a35', trim: '#e0a93f', hair: '#b3bcc9', hairHi: '#eef2f7', brow: '#5d6573', skin: '#e6b890', eye: '#e8962a',
  stats: { kick: 76, dribble: 64, block: 76, speed: 68 }, maxTP: 120,
  bio: 'Tetsuzan’s captain. Reads dribbles early and walls off the shooting lane. Granite Guard shuts down Flame.',
  moves: [
    { name: 'Tectonic Hammer', kind: 'shot',    elem: 'stone', power: 60, tp: 45 },
    { name: 'Shard Spiral',    kind: 'shot',    elem: 'gale',  power: 44, tp: 26 },
    { name: 'Granite Guard',   kind: 'block',   elem: 'stone', power: 40, tp: 20 },
    { name: 'Mirage Feint',    kind: 'dribble', elem: 'gale',  power: 36, tp: 18 },
  ],
};

const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
const lerp = (a, b, t) => a + (b - a) * t;
const easeOut = t => 1 - Math.pow(1 - t, 3);
const easeBack = t => { const c1 = 1.70158, c3 = c1 + 1; return 1 + c3 * Math.pow(t - 1, 3) + c1 * Math.pow(t - 1, 2); };
const sr = n => { const x = Math.sin(n * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); };
const elemMod = (a, b) => (a !== 'none' && b !== 'none' && BEATS[a] === b) ? 1.2 : 1;
const sig = (m, ch) => (m.elem !== 'none' && m.elem === ch.elem) ? 1.1 : 1;
const roll = (stat, m, ch) => (stat * 0.5 + m.power + Math.random() * 24) * sig(m, ch);
const hintFor = (m, ch) => m.elem === 'none' ? 'Neutral' : ('Beats ' + ELEM[BEATS[m.elem]].name + (m.elem === ch.elem ? ' · +10% signature' : ''));

// ---------- DOM & Dual Rendering Surfaces ----------
const $ = id => document.getElementById(id);
const stage = $('stage'), cv = $('cv'), vg = cv.getContext('2d');
// 12-Bit Offscreen Surface (320x180)
const lowCv = document.createElement('canvas');
lowCv.width = LW; lowCv.height = LH;
const g12 = lowCv.getContext('2d', { willReadFrequently: true });
g12.imageSmoothingEnabled = false;

const titleScreen = $('titleScreen'), overScreen = $('overScreen');
const cmd = $('cmd'), cmdTitle = $('cmdTitle'), cmdSub = $('cmdSub'), cmdList = $('cmdList');

// ---------- state ----------
function mkPlayer(ch, team, human) { return { ch, team, human, x: 0, y: 0, vx: 0, vy: 0, fx: team === 0 ? 1 : -1, fy: 0, stun: 0, tp: 60, dash: 0, dashCd: 0 }; }
const haru = mkPlayer(HARU, 0, true), jin = mkPlayer(JIN, 1, false);
const players = [haru, jin];
const keepers = [
  { team: 0, name: 'AKEBONO GK', x: F.x0 + 14, y: CY, rating: 60, color: '#4dd684', dive: 0, dd: 1 },
  { team: 1, name: 'TETSUZAN GK', x: F.x1 - 14, y: CY, rating: 60, color: '#7b6dff', dive: 0, dd: 1 },
];
const ball = { x: CX, y: CY, vx: 0, vy: 0, owner: null, shot: null, spin: 0, noPick: null };
let trail = [], keeperHold = null, score = [0, 0], mode = 'title', duelCd = 0, matchId = 0;
let ov = {}, skipFn = null, shakeT = 0, texts = [], parts = [], rings = [];
let aiT = 0, aiDir = { x: 0, y: 0 }, aiShotCd = 1, aiShoot = false, actionPressed = false;
const keys = new Set(); let joy = { x: 0, y: 0 };
let menuResolve = null, menuOpts = [], menuP = null, menuCancel = false;
const other = p => p === haru ? jin : haru;

// ---------- 32-Bit Arcade Audio System ----------
let AC = null, muted = false, noiseBuf = null;
function initAudio() {
  if (AC) { if (AC.state === 'suspended') AC.resume(); return; }
  try {
    AC = new (window.AudioContext || window.webkitAudioContext)();
    const n = AC.sampleRate; noiseBuf = AC.createBuffer(1, n, AC.sampleRate);
    const d = noiseBuf.getChannelData(0); for (let i = 0; i < n; i++) d[i] = Math.random() * 2 - 1;
  } catch (e) { AC = null; }
}
function tone(type, f0, f1, dur, vol, delay = 0) {
  const t = AC.currentTime + delay, o = AC.createOscillator(), gn = AC.createGain();
  o.type = type; o.frequency.setValueAtTime(f0, t); if (f1) o.frequency.exponentialRampToValueAtTime(f1, t + dur);
  gn.gain.setValueAtTime(vol, t); gn.gain.exponentialRampToValueAtTime(0.0001, t + dur);
  o.connect(gn).connect(AC.destination); o.start(t); o.stop(t + dur + 0.02);
}
function noise(dur, vol, freq, delay = 0) {
  const t = AC.currentTime + delay, s = AC.createBufferSource(), f = AC.createBiquadFilter(), gn = AC.createGain();
  s.buffer = noiseBuf; f.type = 'lowpass'; f.frequency.value = freq;
  gn.gain.setValueAtTime(vol, t); gn.gain.exponentialRampToValueAtTime(0.0001, t + dur);
  s.connect(f).connect(gn).connect(AC.destination); s.start(t); s.stop(t + dur + 0.02);
}
function sfx(k) {
  if (!AC || muted) return;
  try {
    if (engineMode === '32bit') {
      switch (k) {
        case 'kick': tone('sine', 200, 45, .16, .6); tone('triangle', 320, 90, .08, .3); noise(.06, .35, 2800); break;
        case 'touch': tone('triangle', 280, 140, .07, .2); break;
        case 'whistle': tone('sine', 2400, 2200, .18, .06); tone('sine', 2400, 2200, .32, .06, .22); break;
        case 'blip': tone('triangle', 880, 440, .06, .14); break;
        case 'charge': tone('sawtooth', 110, 990, 1.2, .05); tone('triangle', 220, 1320, 1.2, .035); break;
        case 'impact': tone('sine', 110, 28, .6, .7); tone('triangle', 220, 40, .35, .4); noise(.5, .55, 950); break;
        case 'clash': noise(.22, .32, 3500); tone('sawtooth', 440, 160, .16, .08); tone('triangle', 220, 110, .18, .12); break;
        case 'goal': [523, 659, 784, 1047, 1318].forEach((f, i) => tone('triangle', f, 0, .38, .16, i * .08)); noise(1.4, .09, 1500, .12); break;
        case 'catch': tone('sine', 180, 80, .12, .4); noise(.05, .2, 1800); break;
        case 'dash': noise(.14, .16, 2000); tone('sine', 380, 120, .12, .15); break;
      }
    } else {
      switch (k) {
        case 'kick': tone('square', 180, 50, .12, .45); noise(.04, .25, 2500); break;
        case 'touch': tone('triangle', 240, 120, .05, .15); break;
        case 'whistle': tone('square', 2300, 2150, .14, .045); tone('square', 2300, 2150, .25, .045, .18); break;
        case 'blip': tone('triangle', 700, 0, .04, .1); break;
        case 'charge': tone('sawtooth', 110, 880, 1.1, .045); break;
        case 'impact': tone('square', 95, 32, .4, .5); noise(.35, .45, 900); break;
        case 'clash': noise(.15, .25, 3200); tone('square', 320, 150, .12, .06); break;
        case 'goal': [523, 659, 784, 1047].forEach((f, i) => tone('triangle', f, 0, .28, .13, i * .08)); noise(1.0, .07, 1400, .1); break;
        case 'catch': tone('triangle', 150, 90, .08, .35); break;
        case 'dash': noise(.1, .12, 1800); break;
      }
    }
  } catch (e) {}
}

// ---------- flow helpers ----------
function timed(key, data, ms) {
  return new Promise(res => {
    const o = Object.assign({}, data, { t0: performance.now(), dur: ms });
    ov[key] = o; let done = false, to = 0;
    const fin = () => { if (done) return; done = true; clearTimeout(to); if (ov[key] === o) delete ov[key]; if (skipFn === fin) skipFn = null; res(); };
    to = setTimeout(fin, ms); skipFn = fin;
  });
}
const playCut = (p, m) => { sfx('charge'); return timed('cut', { p, m, boom: false }, 2300); };
const showClash = c => { sfx('clash'); return timed('clash', c, c.quick ? 1300 : 1750); };
function shake(v) { shakeT = Math.max(shakeT, v); }
function addText(x, y, text, color) { texts.push({ x, y, text, color, t: 0, life: 1.4 }); }
function hexA(hex, a) { const n = parseInt(hex.slice(1), 16); return `rgba(${n >> 16},${(n >> 8) & 255},${n & 255},${a})`; }
function ring(x, y, color, r1, life) { rings.push({ x, y, color, r1, life, t: 0 }); }
function burst(x, y, elem, n, speed, life) {
  const E = ELEM[elem];
  for (let i = 0; i < n; i++) {
    const a = Math.random() * Math.PI * 2, v = speed * (.3 + Math.random() * .7);
    const kind = elem === 'stone' ? (i % 2 ? 'rock' : 'dust') : elem === 'gale' ? 'wisp' : elem === 'flame' ? 'ember' : 'spark';
    parts.push({ x, y, vx: Math.cos(a) * v, vy: Math.sin(a) * v, t: 0, life: life * (.6 + Math.random() * .6), size: 2 + Math.random() * 3.5,
      color: Math.random() < .5 ? E.c : E.g, kind, rot: Math.random() * 6, drag: 3, rise: elem === 'flame' ? -30 : 0 });
  }
}
function emitShot(dt) {
  const s = ball.shot, special = s.move.tp > 0, sp = Math.hypot(ball.vx, ball.vy) || 1;
  const bx = -ball.vx / sp, by = -ball.vy / sp, px = -by, py = bx;
  s.acc = (s.acc || 0) + (special ? 110 : 24) * dt;
  while (s.acc >= 1) {
    s.acc -= 1;
    const j = Math.random() - .5, sv = Math.random() - .5;
    const p = { x: ball.x + px * j * 10, y: ball.y + py * j * 10, t: 0, rot: Math.random() * 6, drag: 3, rise: 0 };
    if (!special || s.elem === 'none') Object.assign(p, { kind: 'spark', color: '#ffffff', size: 1.5, life: .25, vx: bx * 80 + px * sv * 40, vy: by * 80 + py * sv * 40 });
    else if (s.elem === 'flame') { const v = 60 + Math.random() * 110; Object.assign(p, { kind: 'ember', color: ['#ffd28a', '#ff9a3c', '#ff5a36'][Math.floor(Math.random() * 3)], size: 2 + Math.random() * 3, life: .35 + Math.random() * .3, vx: bx * v + px * sv * 70, vy: by * v + py * sv * 70, rise: -40 }); }
    else if (s.elem === 'gale') Object.assign(p, { kind: 'wisp', color: '#c9fff6', size: 2, life: .3 + Math.random() * .25, vx: bx * 140 + px * sv * 150, vy: by * 140 + py * sv * 150, drag: 2 });
    else if (Math.random() < .45) Object.assign(p, { kind: 'rock', color: Math.random() < .5 ? '#c98f2c' : '#8a5f1a', size: 1.8 + Math.random() * 2.6, life: .5 + Math.random() * .35, vx: bx * 70 + px * sv * 110, vy: by * 70 + py * sv * 110, drag: 4 });
    else Object.assign(p, { kind: 'dust', color: '#e8cf9a', size: 3 + Math.random() * 4, life: .45, vx: bx * 40 + px * sv * 40, vy: by * 40 + py * sv * 40 });
    parts.push(p);
  }
}
function updateParts(dt) {
  for (const p of parts) { p.t += dt; const f = Math.exp(-p.drag * dt); p.vx *= f; p.vy *= f; p.x += p.vx * dt; p.y += (p.vy + p.rise) * dt; p.rot += dt * 6; }
  parts = parts.filter(p => p.t < p.life); if (parts.length > 700) parts.splice(0, parts.length - 700);
  for (const r of rings) r.t += dt; rings = rings.filter(r => r.t < r.life);
}

function askMenu(title, sub, opts, p, cancel) {
  return new Promise(res => {
    cmdTitle.textContent = title; cmdSub.textContent = sub; cmdList.innerHTML = '';
    const btns = [];
    opts.forEach((m, i) => {
      const b = document.createElement('button'); b.type = 'button'; b.className = 'mv'; b.disabled = m.tp > p.tp + 1e-6;
      b.innerHTML = `<span class="k">${i + 1}</span><span class="nm">${m.name}</span><span class="tp">${m.tp ? m.tp + ' TP' : 'Free'}</span>` +
        `<span class="meta"><span class="chip ${m.elem}">${ELEM[m.elem].name}</span><span>PWR ${m.power}</span><span>${hintFor(m, p.ch)}</span></span>`;
      b.addEventListener('click', () => closeMenu(m));
      cmdList.appendChild(b); btns.push(b);
    });
    if (cancel) {
      const b = document.createElement('button'); b.type = 'button'; b.className = 'mv ghost';
      b.innerHTML = `<span class="k">Esc</span><span class="nm">${cancel}</span>`;
      b.addEventListener('click', () => closeMenu(null)); cmdList.appendChild(b);
    }
    menuOpts = opts; menuP = p; menuCancel = !!cancel; menuResolve = res; cmd.hidden = false;
    const first = btns.find(b => !b.disabled) || cmdList.querySelector('button');
    if (first) first.focus({ preventScroll: true });
    sfx('blip');
  });
}
function closeMenu(m) {
  if (!menuResolve) return;
  const r = menuResolve; menuResolve = null; cmd.hidden = true; cmdList.innerHTML = '';
  if (m) sfx('blip');
  stage.focus({ preventScroll: true });
  r(m);
}
function aiPick(p, opts, kind, info = {}) {
  const afford = opts.filter(m => m.tp > 0 && m.tp <= p.tp), basic = opts[0];
  if (!afford.length) return basic;
  if (kind === 'shot') {
    const big = afford.find(m => m.tp >= 40), mid = afford.find(m => m.tp < 40);
    if (big && info.dist < 360 && Math.random() < 0.7) return big;
    if (mid && Math.random() < 0.5) return mid;
    return basic;
  }
  if (kind === 'shotblock') return Math.random() < (info.power > 75 ? 0.85 : 0.45) ? afford[0] : basic;
  if (kind === 'block') return Math.random() < 0.5 ? afford[0] : basic;
  if (kind === 'dribble') { const m = afford[0]; if (p.tp - m.tp < 45 && Math.random() < 0.5) return basic; return Math.random() < 0.55 ? m : basic; }
  return basic;
}
function sidesOf(a, b) {
  const mk = o => ({
    name: o.name || o.ent.ch.short, move: o.move, score: o.score, mod: o.mod || 1, sig: o.sig || 1,
    team: o.ent ? o.ent.team : o.team,
    color: o.move.elem === 'none' ? (o.color || (o.ent ? ELEM[o.ent.ch.elem].c : '#9aa6b8')) : ELEM[o.move.elem].c,
  });
  const A = mk(a), B = mk(b); return A.team === 0 ? [A, B] : [B, A];
}

// ---------- match flow ----------
function placeKickoff(team) {
  for (const p of players) { p.vx = p.vy = 0; p.stun = 0; p.dash = 0; }
  ball.shot = null; keeperHold = null; trail = []; ball.vx = ball.vy = 0; ball.noPick = null; parts = []; rings = [];
  keepers.forEach(k => { k.y = CY; k.dive = 0; });
  if (team === 0) { haru.x = CX - 6; haru.y = CY; haru.fx = 1; haru.fy = 0; jin.x = CX + 96; jin.y = CY; jin.fx = -1; jin.fy = 0; ball.owner = haru; }
  else { jin.x = CX + 6; jin.y = CY; jin.fx = -1; jin.fy = 0; haru.x = CX - 96; haru.y = CY; haru.fx = 1; haru.fy = 0; ball.owner = jin; }
  ball.x = ball.owner.x + ball.owner.fx * 15; ball.y = CY;
}
async function kickoff(team) {
  const id = matchId; placeKickoff(team); mode = 'freeze'; sfx('whistle');
  await timed('banner', { text: 'KICK OFF', sub: team === 0 ? 'Akebono ball' : 'Tetsuzan ball', color: '#ffe14d', big: false }, 1000);
  if (id !== matchId) return;
  duelCd = 1; aiShotCd = 1.2; mode = 'play';
}
function startMatch(data) {
  matchId++;
  if (skipFn) skipFn();
  if (menuResolve) closeMenu(null);
  ov = {}; texts = []; score = (data && Array.isArray(data.score)) ? data.score.slice(0, 2) : [0, 0];
  haru.tp = 60; jin.tp = 60;
  titleScreen.hidden = true; overScreen.hidden = true;
  initAudio(); stage.focus({ preventScroll: true });
  kickoff(0);
}
function endMatch(team) {
  mode = 'over';
  $('overTitle').innerHTML = team === 0 ? '<span class="a">Haru</span> wins' : '<span class="b">Jin</span> wins';
  $('overSub').textContent = `${score[0]} – ${score[1]}. ` + (team === 0 ? 'Akebono’s Flame broke the wall.' : 'Tetsuzan’s Stone held firm. Try baiting Granite Guard before you shoot.');
  overScreen.hidden = false; sfx('whistle');
  $('againBtn').focus({ preventScroll: true });
}

async function duel(att, def) {
  const id = matchId; mode = 'freeze'; sfx('clash');
  const aOpts = [BASIC.dribble, ...att.ch.moves.filter(m => m.kind === 'dribble')];
  const dOpts = [BASIC.block, ...def.ch.moves.filter(m => m.kind === 'block')];
  ov.vs = { label: 'DRIBBLE DUEL', t0: performance.now() };
  let am, dm;
  if (att.human) {
    const aP = askMenu(`${att.ch.name} (Ball)`, 'Choose your dribble move', aOpts, att);
    const dP = Promise.resolve(aiPick(def, dOpts, 'dribble', {}));
    [am, dm] = await Promise.all([aP, dP]);
  } else {
    const dP = askMenu(`${def.ch.name} (Defence)`, 'Choose your block move', dOpts, def);
    const aP = Promise.resolve(aiPick(att, aOpts, 'dribble', {}));
    [am, dm] = await Promise.all([aP, dP]);
  }
  if (id !== matchId) return;
  delete ov.vs;
  if (!am) am = BASIC.dribble; if (!dm) dm = BASIC.block;
  att.tp = Math.max(0, att.tp - am.tp); def.tp = Math.max(0, def.tp - dm.tp);
  if (am.tp > 0) await playCut(att, am);
  if (id !== matchId) return;
  if (dm.tp > 0) await playCut(def, dm);
  if (id !== matchId) return;
  const aMod = elemMod(am.elem, dm.elem), dMod = elemMod(dm.elem, am.elem);
  const aSig = sig(am, att.ch), dSig = sig(dm, def.ch);
  const aScore = (att.ch.stats.dribble * 0.5 + am.power + Math.random() * 24) * aSig * aMod;
  const dScore = (def.ch.stats.block * 0.5 + dm.power + Math.random() * 24) * dSig * dMod;
  const attWins = aScore >= dScore;
  const sides = sidesOf({ ent: att, move: am, score: aScore, mod: aMod, sig: aSig }, { ent: def, move: dm, score: dScore, mod: dMod, sig: dSig });
  await showClash({ title: 'DRIBBLE DUEL', sides, verdict: attWins ? `${att.ch.short} BREAKS THROUGH!` : `${def.ch.short} WINS THE BALL!`, winTeam: attWins ? att.team : def.team });
  if (id !== matchId) return;
  if (attWins) {
    sfx('touch');
    const fwd = att.team === 0 ? 1 : -1;
    att.vx = fwd * 260; att.vy = (Math.random() - 0.5) * 60;
    def.stun = 0.9; def.vx = -fwd * 140;
    addText(att.x, att.y - 30, 'BREAK THROUGH!', ELEM[am.elem].c);
  } else {
    sfx('touch');
    ball.owner = def;
    const fwd = def.team === 0 ? 1 : -1;
    def.vx = fwd * 180;
    att.stun = 1.0; att.vx = -fwd * 120;
    addText(def.x, def.y - 30, 'BALL WON!', ELEM[dm.elem].c);
  }
  duelCd = 1.2; mode = 'play';
}

async function shoot(p) {
  const id = matchId; mode = 'freeze';
  const opts = [BASIC.shot, ...p.ch.moves.filter(m => m.kind === 'shot')];
  let m;
  if (p.human) {
    ov.aim = { p };
    m = await askMenu(`${p.ch.name} · SHOOT`, 'Choose your strike', opts, p, 'Cancel');
    delete ov.aim;
  } else {
    const dist = Math.hypot(p.x - (p.team === 0 ? F.x1 : F.x0), p.y - CY);
    m = aiPick(p, opts, 'shot', { dist });
  }
  if (id !== matchId) return;
  if (!m) { mode = 'play'; return; }
  p.tp = Math.max(0, p.tp - m.tp);
  if (m.tp > 0) await playCut(p, m);
  if (id !== matchId) return;

  const targetX = p.team === 0 ? F.x1 : F.x0;
  const targetY = clamp(CY + (Math.random() - 0.5) * 90, GY0 + 10, GY1 - 10);
  const dx = targetX - ball.x, dy = targetY - ball.y, dist = Math.hypot(dx, dy) || 1;
  const distK = clamp(lerp(1.08, 0.45, (dist - 140) / 600), 0.45, 1.08);
  const rawPwr = (p.ch.stats.kick * 0.5 + m.power + Math.random() * 24) * sig(m, p.ch);
  const pwr = rawPwr * distK;
  ball.owner = null;
  ball.vx = (dx / dist) * Math.min(880, Math.max(420, pwr * 9));
  ball.vy = (dy / dist) * Math.min(880, Math.max(420, pwr * 9));
  ball.shot = { p, move: m, elem: m.elem, power: pwr, targetY, cracked: false, distK };
  ball.noPick = { p, t: 0.6 };
  sfx('kick');
  burst(ball.x, ball.y, m.elem, m.tp > 0 ? 32 : 14, 240, 0.7);
  shake(m.tp > 0 ? 0.35 : 0.16);
  ring(ball.x, ball.y, ELEM[m.elem].c, 46, 0.45);
  addText(p.x, p.y - 30, `${m.name.toUpperCase()}!`, ELEM[m.elem].c);
  duelCd = 0.8; mode = 'play';

  const def = other(p);
  if (def.stun <= 0 && Math.abs(def.y - ball.y) < 65) {
    const fwd = p.team === 0 ? 1 : -1;
    const inPath = (def.x - p.x) * fwd > 40 && (targetX - def.x) * fwd > 60;
    if (inPath) {
      setTimeout(() => tryShotBlock(def), 120);
    }
  }
}

async function tryShotBlock(def) {
  if (!ball.shot || mode !== 'play') return;
  const s = ball.shot, id = matchId;
  const dOpts = [BASIC.block, ...def.ch.moves.filter(m => m.kind === 'block')];
  mode = 'freeze'; sfx('clash');
  let dm;
  if (def.human) {
    dm = await askMenu(`${def.ch.name} (Shot incoming!)`, 'Choose your block', dOpts, def);
  } else {
    dm = aiPick(def, dOpts, 'shotblock', { power: s.power });
  }
  if (id !== matchId) return;
  if (!dm) dm = BASIC.block;
  def.tp = Math.max(0, def.tp - dm.tp);
  if (dm.tp > 0) await playCut(def, dm);
  if (id !== matchId) return;

  const sMod = elemMod(s.elem, dm.elem), dMod = elemMod(dm.elem, s.elem);
  const dSig = sig(dm, def.ch);
  const dScore = (def.ch.stats.block * 0.5 + dm.power + Math.random() * 24) * dSig * dMod;
  const shotScore = s.power * sMod;
  const blocked = dScore >= shotScore;
  const sides = sidesOf({ name: s.p.ch.short, move: s.move, score: shotScore, mod: sMod, sig: 1, team: s.p.team, color: ELEM[s.elem].c },
    { ent: def, move: dm, score: dScore, mod: dMod, sig: dSig });
  await showClash({ title: 'SHOT BLOCK', sides, verdict: blocked ? `${def.ch.short} BLOCKS THE SHOT!` : `${s.p.ch.short} POWER BREAKS THROUGH!`, winTeam: blocked ? def.team : s.p.team, quick: true });
  if (id !== matchId) return;

  if (blocked) {
    sfx('touch');
    ball.shot = null;
    const fwd = def.team === 0 ? 1 : -1;
    ball.vx = fwd * (180 + Math.random() * 120);
    ball.vy = (Math.random() - 0.5) * 220;
    def.vx = fwd * 80;
    addText(def.x, def.y - 30, 'DEFLECTED!', ELEM[dm.elem].c);
  } else {
    s.power = Math.max(20, s.power - dScore * 0.55);
    s.cracked = true;
    def.stun = 1.1; def.vx = (def.team === 0 ? -1 : 1) * 220;
    sfx('impact');
    shake(0.3);
    addText(def.x, def.y - 30, 'BROKEN THROUGH!', ELEM[s.elem].c);
  }
  duelCd = 1.0; mode = 'play';
}

function steer(p, ix, iy, dt) {
  if (p.stun > 0) { p.stun = Math.max(0, p.stun - dt); p.vx *= 0.88; p.vy *= 0.88; p.x += p.vx * dt; p.y += p.vy * dt; return; }
  const topSp = (p.ch.stats.speed / 100) * 190 * (p.dash > 0 ? 1.85 : 1);
  const acc = p.dash > 0 ? 2200 : 1300;
  if (ix || iy) {
    const len = Math.hypot(ix, iy) || 1;
    const tx = (ix / len) * topSp, ty = (iy / len) * topSp;
    p.vx += (tx - p.vx) * Math.min(1, acc * dt / topSp);
    p.vy += (ty - p.vy) * Math.min(1, acc * dt / topSp);
    p.fx = ix / len; p.fy = iy / len;
  } else {
    p.vx *= Math.exp(-6 * dt); p.vy *= Math.exp(-6 * dt);
  }
  p.x += p.vx * dt; p.y += p.vy * dt;
  p.x = clamp(p.x, F.x0 + 16, F.x1 - 16); p.y = clamp(p.y, F.y0 + 16, F.y1 - 16);
  if (p.dash > 0) p.dash = Math.max(0, p.dash - dt);
  if (p.dashCd > 0) p.dashCd = Math.max(0, p.dashCd - dt);
  p.tp = Math.min(p.ch.maxTP, p.tp + 3.2 * dt);
}

function aiThink() {
  const me = jin, targetX = F.x0, myGoalX = F.x1;
  const dBall = Math.hypot(me.x - ball.x, me.y - ball.y);
  if (ball.owner === me) {
    const toGoalX = targetX - me.x, toGoalY = CY - me.y, dGoal = Math.hypot(toGoalX, toGoalY);
    if (dGoal < 360 && aiShotCd <= 0) { aiShoot = true; aiShotCd = 2.5; return; }
    aiDir = { x: toGoalX / dGoal, y: toGoalY / dGoal };
  } else if (ball.owner === haru) {
    const blockX = haru.x + (myGoalX - haru.x) * 0.45, blockY = haru.y + (CY - haru.y) * 0.35;
    const dx = blockX - me.x, dy = blockY - me.y, d = Math.hypot(dx, dy) || 1;
    aiDir = { x: dx / d, y: dy / d };
  } else {
    const dx = ball.x - me.x, dy = ball.y - me.y, d = Math.hypot(dx, dy) || 1;
    aiDir = { x: dx / d, y: dy / d };
  }
}

function updateBall(dt) {
  if (ball.owner) {
    const p = ball.owner;
    ball.x = p.x + p.fx * 15; ball.y = p.y + p.fy * 15;
    ball.vx = p.vx; ball.vy = p.vy;
    ball.spin += (Math.hypot(p.vx, p.vy) * 0.04) * dt;
    return false;
  }
  if (ball.noPick) { ball.noPick.t -= dt; if (ball.noPick.t <= 0) ball.noPick = null; }
  trail.push({ x: ball.x, y: ball.y }); if (trail.length > 22) trail.shift();
  ball.x += ball.vx * dt; ball.y += ball.vy * dt;
  ball.spin += (Math.hypot(ball.vx, ball.vy) * 0.03) * dt;
  if (ball.shot) emitShot(dt);

  // Goal check
  if (ball.y >= GY0 && ball.y <= GY1) {
    if (ball.x <= F.x0 - 12) { goalScored(1); return true; }
    if (ball.x >= F.x1 + 12) { goalScored(0); return true; }
  }
  // Sideline bounce
  if (ball.y < F.y0 + 6) { ball.y = F.y0 + 6; ball.vy *= -0.75; sfx('touch'); }
  if (ball.y > F.y1 - 6) { ball.y = F.y1 - 6; ball.vy *= -0.75; sfx('touch'); }
  // Backline bounce outside goal
  if (ball.x < F.x0 && (ball.y < GY0 || ball.y > GY1)) { ball.x = F.x0; ball.vx *= -0.7; sfx('touch'); }
  if (ball.x > F.x1 && (ball.y < GY0 || ball.y > GY1)) { ball.x = F.x1; ball.vx *= -0.7; sfx('touch'); }
  // Friction
  const fr = ball.shot ? 0.992 : 0.965;
  ball.vx *= Math.pow(fr, dt * 60); ball.vy *= Math.pow(fr, dt * 60);
  if (!ball.shot && Math.hypot(ball.vx, ball.vy) < 8) { ball.vx = ball.vy = 0; }
  return false;
}

function updateKeepers(dt) {
  for (const k of keepers) {
    const oppTeam = k.team === 0 ? 1 : 0;
    const attacking = ball.owner ? ball.owner.team === oppTeam : (ball.shot ? ball.shot.p.team === oppTeam : (k.team === 0 ? ball.vx < -40 : ball.vx > 40));
    let ty = CY;
    if (attacking) ty = clamp(ball.y, GY0 + 12, GY1 - 12);
    k.y += (ty - k.y) * Math.min(1, 6 * dt);
    k.y = clamp(k.y, GY0 + 8, GY1 - 8);
    if (k.dive > 0) k.dive = Math.max(0, k.dive - dt);

    if (ball.shot && ball.shot.p.team === oppTeam && Math.abs(ball.x - k.x) < 32 && Math.abs(ball.y - k.y) < 42) {
      keeperSave(k, ball.shot);
      break;
    }
  }
}

async function keeperSave(k, shot) {
  const id = matchId; mode = 'freeze';
  k.dive = 0.6; k.dd = ball.y > k.y ? 1 : -1;
  const gkScore = (30 + 34 + Math.random() * 24);
  const saved = gkScore >= shot.power;
  await timed('save', { k, saved }, 650);
  if (id !== matchId) return;

  if (saved) {
    sfx('catch');
    ball.shot = null; ball.owner = null;
    ball.vx = (k.team === 0 ? 1 : -1) * (140 + Math.random() * 80);
    ball.vy = (Math.random() - 0.5) * 160;
    ball.noPick = { p: null, t: 0.5 };
    addText(k.x, k.y - 24, `${k.name} SAVES!`, '#ffe14d');
  } else {
    sfx('goal');
    shake(0.45);
    burst(ball.x, ball.y, shot.elem, 42, 340, 0.9);
    addText(k.x, k.y - 24, 'GOAL!', '#ffe14d');
  }
  mode = 'play';
}

async function goalScored(scoringTeam) {
  mode = 'freeze'; sfx('goal'); shake(0.5);
  score[scoringTeam]++;
  const ch = scoringTeam === 0 ? HARU : JIN;
  burst(ball.x, ball.y, ch.elem, 48, 380, 1.1);
  await timed('banner', { text: 'GOAL!!', sub: `${ch.name.toUpperCase()} SCORES!`, color: ELEM[ch.elem].c, big: true }, 1800);
  if (score[0] >= GOALS_TO_WIN || score[1] >= GOALS_TO_WIN) {
    endMatch(score[0] >= GOALS_TO_WIN ? 0 : 1);
  } else {
    kickoff(scoringTeam === 0 ? 1 : 0);
  }
}

function update(dt) {
  if (mode !== 'play') return;
  duelCd = Math.max(0, duelCd - dt);
  aiShotCd = Math.max(0, aiShotCd - dt);
  let ix = joy.x, iy = joy.y;
  if (!ix && !iy) {
    if (keys.has('KeyW') || keys.has('ArrowUp')) iy -= 1;
    if (keys.has('KeyS') || keys.has('ArrowDown')) iy += 1;
    if (keys.has('KeyA') || keys.has('ArrowLeft')) ix -= 1;
    if (keys.has('KeyD') || keys.has('ArrowRight')) ix += 1;
  }
  if (actionPressed) {
    actionPressed = false;
    if (ball.owner === haru && haru.stun <= 0) { shoot(haru); return; }
    if (haru.dashCd <= 0 && haru.stun <= 0) { haru.dash = 0.22; haru.dashCd = 0.9; sfx('dash'); }
  }
  steer(haru, ix, iy, dt);
  aiT -= dt; if (aiT <= 0) { aiT = 0.1; aiThink(); }
  if (aiShoot) { aiShoot = false; if (ball.owner === jin && jin.stun <= 0) { shoot(jin); return; } }
  steer(jin, aiDir.x * 0.94, aiDir.y * 0.94, dt);
  if (!ball.owner) {
    const dx = jin.x - haru.x, dy = jin.y - haru.y, d = Math.hypot(dx, dy);
    if (d > 0 && d < 24) { const push = (24 - d) / 2; haru.x -= dx / d * push; haru.y -= dy / d * push; jin.x += dx / d * push; jin.y += dy / d * push; }
  }
  updateKeepers(dt);
  if (updateBall(dt)) return;
  if (!ball.owner && !keeperHold && !ball.shot) {
    for (const p of players) {
      if (p.stun > 0 || (ball.noPick && ball.noPick.p === p)) continue;
      if (Math.hypot(p.x - ball.x, p.y - ball.y) < 18) { ball.owner = p; sfx('touch'); break; }
    }
  }
  if (ball.owner && duelCd <= 0) {
    const o = other(ball.owner);
    if (o.stun <= 0 && ball.owner.stun <= 0 && Math.hypot(o.x - ball.owner.x, o.y - ball.owner.y) < 26) { duel(ball.owner, o); return; }
  }
}

// ============================================================================
// 32-BIT ARCADE PIPELINE RENDERING
// ============================================================================
const bg32 = document.createElement('canvas'); bg32.width = W * 2; bg32.height = H * 2;
function drawStatic32() {
  const c = bg32.getContext('2d'); c.setTransform(2, 0, 0, 2, 0, 0);
  c.fillStyle = '#080c18'; c.fillRect(0, 0, W, H);
  const crowd = ['#2a3558', '#1e2744', '#3a4570', '#5b4a3a', '#6a2d2d', '#2d4d5a', '#44506f'];
  for (let i = 0; i < 1400; i++) {
    const zone = sr(i * 9.3); let x, y;
    if (zone < 0.55) { x = sr(i * 1.3) * W; y = 4 + sr(i * 2.7) * (F.y0 - 20); }
    else if (zone < 0.8) { x = sr(i * 1.3) * W; y = F.y1 + 10 + sr(i * 2.7) * (H - F.y1 - 14); }
    else { x = sr(i * 1.3) < 0.5 ? sr(i * 4.1) * (F.x0 - 34) : F.x1 + 34 + sr(i * 4.1) * (W - F.x1 - 36); y = F.y0 + sr(i * 2.7) * (F.y1 - F.y0); }
    c.fillStyle = crowd[Math.floor(sr(i * 5.1) * crowd.length)]; c.fillRect(x, y, 3, 3);
  }
  // Ad boards
  for (let i = 0; i < 24; i++) { c.fillStyle = i % 2 ? 'rgba(224,64,42,.35)' : 'rgba(224,169,63,.3)'; c.fillRect(F.x0 + i * 35, F.y0 - 12, 33, 5); c.fillRect(F.x0 + i * 35, F.y1 + 7, 33, 5); }
  // 14 alternating turf stripes
  const n = 14, sw = (F.x1 - F.x0) / n;
  for (let i = 0; i < n; i++) { c.fillStyle = i % 2 ? '#1f6343' : '#1b5a3c'; c.fillRect(F.x0 + i * sw, F.y0, sw + 0.5, F.y1 - F.y0); }
  // Stadium corner floodlight cones (32-Bit TrueColor Radial Lighting)
  for (const [lx, ly] of [[F.x0, F.y0], [F.x1, F.y0], [F.x0, F.y1], [F.x1, F.y1]]) {
    const gr = c.createRadialGradient(lx, ly, 0, lx, ly, 460); gr.addColorStop(0, 'rgba(230,255,240,.12)'); gr.addColorStop(1, 'rgba(230,255,240,0)');
    c.fillStyle = gr; c.fillRect(F.x0, F.y0, F.x1 - F.x0, F.y1 - F.y0);
  }
  // Soft stadium center vignette
  const vg32 = c.createRadialGradient(CX, CY, 200, CX, CY, 620); vg32.addColorStop(0, 'rgba(0,0,0,0)'); vg32.addColorStop(1, 'rgba(0,0,0,.38)');
  c.fillStyle = vg32; c.fillRect(F.x0, F.y0, F.x1 - F.x0, F.y1 - F.y0);
  // Nets
  for (const side of [0, 1]) {
    const nx = side === 0 ? F.x0 - 26 : F.x1;
    c.fillStyle = 'rgba(255,255,255,.07)'; c.fillRect(nx, GY0, 26, GY1 - GY0);
    c.strokeStyle = 'rgba(255,255,255,.18)'; c.lineWidth = 1;
    for (let yy = GY0; yy <= GY1; yy += 8) { c.beginPath(); c.moveTo(nx, yy); c.lineTo(nx + 26, yy); c.stroke(); }
    for (let xx = nx; xx <= nx + 26; xx += 8) { c.beginPath(); c.moveTo(xx, GY0); c.lineTo(xx, GY1); c.stroke(); }
    c.strokeStyle = 'rgba(255,255,255,.5)'; c.lineWidth = 2; c.strokeRect(nx, GY0, 26, GY1 - GY0);
  }
  // Field lines
  c.strokeStyle = 'rgba(236,255,244,.78)'; c.lineWidth = 2.5;
  c.strokeRect(F.x0, F.y0, F.x1 - F.x0, F.y1 - F.y0);
  c.beginPath(); c.moveTo(CX, F.y0); c.lineTo(CX, F.y1); c.stroke();
  c.beginPath(); c.arc(CX, CY, 64, 0, Math.PI * 2); c.stroke();
  c.fillStyle = 'rgba(236,255,244,.85)'; c.beginPath(); c.arc(CX, CY, 3.5, 0, Math.PI * 2); c.fill();
  for (const side of [0, 1]) {
    const dir = side === 0 ? 1 : -1, gx = side === 0 ? F.x0 : F.x1;
    c.strokeRect(side === 0 ? gx : gx - 116, CY - 124, 116, 248);
    c.strokeRect(side === 0 ? gx : gx - 40, GY0 - 24, 40, GY1 - GY0 + 48);
    c.beginPath(); c.arc(gx + dir * 84, CY, 3, 0, Math.PI * 2); c.fill();
    c.beginPath(); c.arc(gx + dir * 84, CY, 52, side === 0 ? -0.93 : Math.PI - 0.93, side === 0 ? 0.93 : Math.PI + 0.93); c.stroke();
  }
  c.fillStyle = '#ffffff';
  for (const [px, py] of [[F.x0, GY0], [F.x0, GY1], [F.x1, GY0], [F.x1, GY1]]) { c.beginPath(); c.arc(px, py, 4.5, 0, Math.PI * 2); c.fill(); }
  c.lineWidth = 4; c.strokeStyle = '#ffffff';
  c.beginPath(); c.moveTo(F.x0, GY0); c.lineTo(F.x0, GY1); c.moveTo(F.x1, GY0); c.lineTo(F.x1, GY1); c.stroke();
  for (const [ax, ay, a0] of [[F.x0, F.y0, 0], [F.x1, F.y0, Math.PI / 2], [F.x1, F.y1, Math.PI], [F.x0, F.y1, Math.PI * 1.5]]) {
    c.lineWidth = 2; c.strokeStyle = 'rgba(236,255,244,.7)'; c.beginPath(); c.arc(ax, ay, 12, a0, a0 + Math.PI / 2); c.stroke();
  }
}

function rr(c, x, y, w, h, r) { c.beginPath(); c.moveTo(x + r, y); c.arcTo(x + w, y, x + w, y + h, r); c.arcTo(x + w, y + h, x, y + h, r); c.arcTo(x, y + h, x, y, r); c.arcTo(x, y, x + w, y, r); c.closePath(); }
function circle(c, x, y, r) { c.beginPath(); c.arc(x, y, r, 0, Math.PI * 2); }

function drawPlayer32(p, now) {
  const ch = p.ch, moving = Math.hypot(p.vx, p.vy) > 20, bob = moving ? Math.sin(now / 55) * 1.3 : 0;
  const x = p.x, y = p.y + bob;
  vg.fillStyle = 'rgba(0,0,0,.38)'; vg.beginPath(); vg.ellipse(p.x + 2, p.y + 11, 14, 5.5, 0, 0, Math.PI * 2); vg.fill();
  if (p.human) {
    vg.strokeStyle = '#ffe14d'; vg.lineWidth = 2; vg.beginPath(); vg.ellipse(p.x, p.y + 9, 19 + Math.sin(now / 90) * 1.5, 8 + Math.sin(now / 90) * 0.7, 0, 0, Math.PI * 2); vg.stroke();
  }
  if (p.dash > 0) { vg.globalAlpha = .38; vg.fillStyle = ELEM[ch.elem].c; circle(vg, x - p.vx * 0.04, y - p.vy * 0.04, 13); vg.fill(); vg.globalAlpha = 1; }
  vg.lineWidth = 2.5; vg.strokeStyle = '#0b0e1a';
  vg.fillStyle = ch.jersey; circle(vg, x, y, 12); vg.fill(); vg.stroke();
  vg.fillStyle = ch.trim; vg.font = '700 8.5px "Dela Gothic One", sans-serif'; vg.textAlign = 'center'; vg.textBaseline = 'middle'; vg.fillText(String(ch.num), x, y + 6.5);
  const hx = x + p.fx * 2.5, hy = y - 7 + p.fy * 1.5;
  vg.fillStyle = ch.hair;
  const back = Math.atan2(-p.fy, -p.fx);
  const spikes = ch.id === 'haru' ? 5 : 3;
  for (let i = 0; i < spikes; i++) {
    const a = back + (i - (spikes - 1) / 2) * (ch.id === 'haru' ? 0.5 : 0.7), len = ch.id === 'haru' ? 14 : 12.5;
    vg.beginPath(); vg.moveTo(hx + Math.cos(a - 0.35) * 7, hy + Math.sin(a - 0.35) * 7); vg.lineTo(hx + Math.cos(a) * len, hy + Math.sin(a) * len); vg.lineTo(hx + Math.cos(a + 0.35) * 7, hy + Math.sin(a + 0.35) * 7); vg.closePath(); vg.fill(); vg.stroke();
  }
  circle(vg, hx, hy, 8.5); vg.fill(); vg.stroke();
  vg.save(); circle(vg, hx, hy, 8.5); vg.clip(); vg.fillStyle = ch.skin; circle(vg, hx + p.fx * 4.5, hy + p.fy * 3 + 2.5, 5.8); vg.fill(); vg.restore();
  vg.font = '700 10px "Azeret Mono", monospace'; const label = ch.short, tw = vg.measureText(label).width;
  vg.fillStyle = 'rgba(8,11,22,.88)'; rr(vg, p.x - tw / 2 - 5, p.y - 38, tw + 10, 14, 4); vg.fill();
  vg.strokeStyle = 'rgba(40,51,90,.8)'; vg.lineWidth = 1; vg.stroke();
  vg.fillStyle = p.human ? '#ffe14d' : ELEM[ch.elem].c; vg.fillText(label, p.x, p.y - 30.5);
  if (p.stun > 0) {
    vg.fillStyle = '#ffe14d';
    for (let i = 0; i < 3; i++) { const a = now / 150 + i * 2.1; const sx = hx + Math.cos(a) * 12, sy = hy - 12 + Math.sin(a) * 4; circle(vg, sx, sy, 2.2); vg.fill(); }
  }
  vg.textBaseline = 'alphabetic';
}

function drawKeeper32(k) {
  const d = k.dive > 0 ? Math.sin(clamp((0.6 - k.dive) / 0.2, 0, 1) * Math.PI / 2) : 0;
  const x = k.x, y = k.y + k.dd * d * 14;
  vg.fillStyle = 'rgba(0,0,0,.38)'; vg.beginPath(); vg.ellipse(x + 2, y + 10, 13, 5, 0, 0, Math.PI * 2); vg.fill();
  vg.save(); vg.translate(x, y); vg.rotate(k.dd * d * 0.9 * (k.team === 0 ? 1 : -1));
  vg.lineWidth = 2.5; vg.strokeStyle = '#0b0e1a';
  vg.fillStyle = k.color; vg.beginPath(); vg.ellipse(0, 0, 11, 12, 0, 0, Math.PI * 2); vg.fill(); vg.stroke();
  vg.fillStyle = '#ffffff'; const gx = k.team === 0 ? 8 : -8;
  circle(vg, gx, -11 - d * 6, 3.8); vg.fill(); vg.stroke(); circle(vg, gx, 11 + d * 6, 3.8); vg.fill(); vg.stroke();
  vg.fillStyle = '#1b1f2a'; circle(vg, 0, -6, 7.5); vg.fill(); vg.stroke();
  vg.restore();
}

function ribbon(c, pts, hx, hy, w) {
  const all = pts.concat([{ x: hx, y: hy }]), n = all.length; if (n < 3) return false;
  const L = [], R = [];
  for (let i = 0; i < n; i++) {
    const a = all[Math.max(0, i - 1)], b = all[Math.min(n - 1, i + 1)];
    let dx = b.x - a.x, dy = b.y - a.y; const d = Math.hypot(dx, dy) || 1; dx /= d; dy /= d;
    const ww = w * (i / (n - 1));
    L.push([all[i].x - dy * ww, all[i].y + dx * ww]); R.push([all[i].x + dy * ww, all[i].y - dx * ww]);
  }
  c.beginPath(); L.forEach(([x, y], i) => i ? c.lineTo(x, y) : c.moveTo(x, y));
  for (let i = R.length - 1; i >= 0; i--) c.lineTo(R[i][0], R[i][1]);
  c.closePath(); return true;
}

function rock32(c, x, y, sz, rot, col) {
  c.save(); c.translate(x, y); c.rotate(rot);
  c.beginPath(); c.moveTo(-sz, -sz * .3); c.lineTo(0, -sz); c.lineTo(sz, -sz * .2); c.lineTo(sz * .5, sz * .8); c.lineTo(-sz * .7, sz * .5); c.closePath();
  c.fillStyle = col; c.fill(); c.strokeStyle = '#2b1d07'; c.lineWidth = 1.2; c.stroke(); c.restore();
}

function drawShotFx32(s, now) {
  const E = ELEM[s.elem], special = s.move.tp > 0;
  const pw = clamp(s.power / 90, 0.5, 1.4) * (s.cracked ? 0.8 : 1);
  const sp = Math.hypot(ball.vx, ball.vy) || 1, ux = ball.vx / sp, uy = ball.vy / sp, px = -uy, py = ux;
  const flick = s.cracked ? (Math.sin(now / 25) > 0 ? 1 : 0.55) : 1;
  vg.save(); vg.globalCompositeOperation = 'lighter';
  const layers = special ? [[E.c, 13 * pw, .5], [E.g, 6 * pw, .75], ['#ffffff', 2.2, .85]] : [['#ffffff', 4.5, .35]];
  for (const [col, w, al] of layers) if (ribbon(vg, trail, ball.x, ball.y, w)) { vg.fillStyle = col; vg.globalAlpha = al * flick; vg.fill(); }
  if (!special) { vg.restore(); return; }
  const R = 24 * pw + Math.sin(now / 45) * 3;
  const gr = vg.createRadialGradient(ball.x, ball.y, 2, ball.x, ball.y, R);
  gr.addColorStop(0, hexA(E.g, .95)); gr.addColorStop(.45, hexA(E.c, .55)); gr.addColorStop(1, hexA(E.c, 0));
  vg.globalAlpha = flick; vg.fillStyle = gr; circle(vg, ball.x, ball.y, R); vg.fill();
  if (s.elem === 'flame') {
    const L = (46 + Math.sin(now / 30) * 8 + Math.sin(now / 17) * 5) * pw, wob = Math.sin(now / 40) * 4;
    for (const [col, wm, lm] of [['#ff5a36', 1, 1], ['#ffb347', .7, .75], ['#fff0c2', .4, .5]]) {
      const w = 10 * pw * wm, l = L * lm;
      vg.fillStyle = col; vg.beginPath();
      vg.moveTo(ball.x + px * w, ball.y + py * w);
      vg.quadraticCurveTo(ball.x - ux * l * .5 + px * w * 1.2, ball.y - uy * l * .5 + py * w * 1.2, ball.x - ux * l + px * wob, ball.y - uy * l + py * wob);
      vg.quadraticCurveTo(ball.x - ux * l * .5 - px * w * 1.2, ball.y - uy * l * .5 - py * w * 1.2, ball.x - px * w, ball.y - py * w);
      vg.quadraticCurveTo(ball.x + ux * w * 1.4, ball.y + uy * w * 1.4, ball.x + px * w, ball.y + py * w);
      vg.closePath(); vg.fill();
    }
  } else if (s.elem === 'gale') {
    vg.strokeStyle = E.g; vg.lineCap = 'round';
    for (let i = 0; i < 3; i++) { vg.lineWidth = 2.6 - i * .5; vg.beginPath(); vg.arc(ball.x, ball.y, (12 + i * 4) * pw, now / 55 + i * 2.1, now / 55 + i * 2.1 + 1.7); vg.stroke(); }
    vg.lineWidth = 2; vg.strokeStyle = hexA(E.g, .8);
    for (const ph of [0, Math.PI]) {
      vg.beginPath();
      trail.forEach((p, i) => { const k = i / trail.length, off = Math.sin(i * 0.9 - now / 35 + ph) * 11 * pw * k; const x = p.x + px * off, y = p.y + py * off; i ? vg.lineTo(x, y) : vg.moveTo(x, y); });
      vg.lineTo(ball.x, ball.y); vg.stroke();
    }
  } else if (s.elem === 'stone') {
    vg.globalCompositeOperation = 'source-over';
    for (let i = 0; i < 4; i++) { const a = now / 80 + i * Math.PI / 2, r = 16 * pw; rock32(vg, ball.x + Math.cos(a) * r, ball.y + Math.sin(a) * r * .8, (4 + (i % 2) * 2) * Math.min(1.2, pw), a * 2, i % 2 ? '#c98f2c' : '#8a5f1a'); }
  }
  vg.restore();
}

function drawBall32(now) {
  const s = ball.shot, special = !!(s && s.move.tp > 0), E = s ? ELEM[s.elem] : ELEM.none;
  if (s) drawShotFx32(s, now);
  const r = special ? 7.5 : 6;
  vg.fillStyle = 'rgba(0,0,0,.35)'; vg.beginPath(); vg.ellipse(ball.x + 2, ball.y + 5, r, 2.6, 0, 0, Math.PI * 2); vg.fill();
  const body = !special ? '#fbfbf7' : s.elem === 'flame' ? '#fff3d2' : s.elem === 'gale' ? '#effffc' : s.elem === 'stone' ? '#d8a24a' : '#fbfbf7';
  vg.fillStyle = body; vg.strokeStyle = special ? (s.elem === 'stone' ? '#2b1d07' : E.c) : '#0b0e1a'; vg.lineWidth = special ? 2.2 : 1.6;
  circle(vg, ball.x, ball.y, r); vg.fill(); vg.stroke();
  vg.save(); circle(vg, ball.x, ball.y, r); vg.clip();
  if (special && s.elem === 'stone') {
    vg.strokeStyle = '#2b1d07'; vg.lineWidth = 1.3;
    for (let i = 0; i < 3; i++) { const a = ball.spin + i * 2.094; vg.beginPath(); vg.moveTo(ball.x, ball.y); vg.lineTo(ball.x + Math.cos(a) * r, ball.y + Math.sin(a) * r); vg.lineTo(ball.x + Math.cos(a + .5) * r * 1.2, ball.y + Math.sin(a + .5) * r * 1.2); vg.stroke(); }
  } else {
    vg.fillStyle = special ? E.c : '#20242e';
    for (let i = 0; i < 3; i++) { const a = ball.spin + i * 2.094; circle(vg, ball.x + Math.cos(a) * r * .6, ball.y + Math.sin(a) * r * .6, r * .32); vg.fill(); }
  }
  vg.restore();
  if (s) {
    const txt = special ? `${s.move.name.toUpperCase()} ${Math.round(s.power)}` : `SHOT ${Math.round(s.power)}`;
    vg.font = '700 9px "Azeret Mono", monospace'; const tw = vg.measureText(txt).width;
    const lx = clamp(ball.x, F.x0 + tw / 2, F.x1 - tw / 2), ly = Math.max(F.y0 + 10, ball.y - 26);
    vg.fillStyle = 'rgba(8,11,22,.85)'; rr(vg, lx - tw / 2 - 5, ly - 7, tw + 10, 13, 3); vg.fill();
    vg.fillStyle = special ? E.c : '#eef1f8'; vg.textAlign = 'center'; vg.textBaseline = 'middle'; vg.fillText(txt, lx, ly - 0.5); vg.textBaseline = 'alphabetic';
  }
}

function drawParts32() {
  vg.save();
  for (const p of parts) {
    const a = 1 - p.t / p.life;
    if (p.kind === 'ember' || p.kind === 'spark') { vg.globalCompositeOperation = 'lighter'; vg.globalAlpha = a; vg.fillStyle = p.color; circle(vg, p.x, p.y, p.size * (0.4 + 0.6 * a)); vg.fill(); }
    else if (p.kind === 'wisp') {
      vg.globalCompositeOperation = 'lighter'; vg.globalAlpha = a; vg.strokeStyle = p.color; vg.lineWidth = 1.6;
      const v = Math.hypot(p.vx, p.vy) || 1, l = v * 0.06 + 4; vg.beginPath(); vg.moveTo(p.x, p.y); vg.lineTo(p.x - p.vx / v * l, p.y - p.vy / v * l); vg.stroke();
    }
    else if (p.kind === 'dust') { vg.globalCompositeOperation = 'source-over'; vg.globalAlpha = a * .35; vg.fillStyle = p.color; circle(vg, p.x, p.y, p.size * (1 + p.t / p.life)); vg.fill(); }
    else if (p.kind === 'rock') { vg.globalCompositeOperation = 'source-over'; vg.globalAlpha = Math.min(1, a * 1.5); rock32(vg, p.x, p.y, p.size, p.rot, p.color); }
  }
  vg.globalCompositeOperation = 'source-over';
  for (const r of rings) { const u = r.t / r.life; vg.globalAlpha = 1 - u; vg.strokeStyle = r.color; vg.lineWidth = 4 * (1 - u) + 1; circle(vg, r.x, r.y, 4 + r.r1 * easeOut(u)); vg.stroke(); }
  vg.restore();
}

function drawTexts32() {
  vg.textAlign = 'center'; vg.font = '700 12px "Azeret Mono", monospace';
  for (const t of texts) {
    const a = 1 - t.t / t.life; vg.globalAlpha = clamp(a * 1.4, 0, 1);
    const y = t.y - t.t * 22; vg.lineWidth = 4; vg.strokeStyle = '#0b0e1a'; vg.strokeText(t.text, t.x, y); vg.fillStyle = t.color; vg.fillText(t.text, t.x, y);
  }
  vg.globalAlpha = 1;
}

function tpBar32(p, x, y, right) {
  const w = 190, h = 9, x0 = right ? x - w : x;
  vg.font = '700 11px "Azeret Mono", monospace'; vg.textAlign = right ? 'right' : 'left'; vg.textBaseline = 'alphabetic';
  vg.fillStyle = '#98a3c2'; vg.fillText(`TP ${Math.floor(p.tp)} / ${p.ch.maxTP}`, x, y + 8);
  vg.fillStyle = '#141c33'; rr(vg, x0, y + 15, w, h, 4); vg.fill();
  const fw = w * p.tp / p.ch.maxTP;
  vg.fillStyle = '#ffe14d'; if (fw > 1) { rr(vg, right ? x - fw : x0, y + 15, fw, h, 4); vg.fill(); }
  vg.fillStyle = 'rgba(11,16,32,.9)';
  for (const m of p.ch.moves) { const tx = right ? x - w * m.tp / p.ch.maxTP : x0 + w * m.tp / p.ch.maxTP; vg.fillRect(tx - 1, y + 15, 2, h); }
}

function drawHUD32() {
  const w = 236, h = 40, x = W / 2 - w / 2, y = 9;
  vg.fillStyle = 'rgba(8,11,22,.94)'; rr(vg, x, y, w, h, 8); vg.fill(); vg.strokeStyle = '#28335a'; vg.lineWidth = 1; vg.stroke();
  vg.fillStyle = HARU.trim; vg.fillRect(x + 10, y + 12, 4, 16); vg.fillStyle = JIN.trim; vg.fillRect(x + w - 14, y + 12, 4, 16);
  vg.textBaseline = 'middle'; vg.font = '700 13px "Azeret Mono", monospace'; vg.fillStyle = '#eef1f8';
  vg.textAlign = 'left'; vg.fillText('HARU', x + 22, y + h / 2 + 1); vg.textAlign = 'right'; vg.fillText('JIN', x + w - 22, y + h / 2 + 1);
  vg.textAlign = 'center'; vg.font = '24px "Dela Gothic One", sans-serif';
  vg.fillText(String(score[0]), W / 2 - 22, y + h / 2 + 1); vg.fillText(String(score[1]), W / 2 + 22, y + h / 2 + 1);
  vg.fillStyle = '#98a3c2'; vg.fillText('–', W / 2, y + h / 2);
  vg.textBaseline = 'alphabetic';
  tpBar32(haru, 22, 12, false); tpBar32(jin, W - 22, 12, true);
}

function drawAim32(p) {
  const gx = p.team === 0 ? F.x1 : F.x0;
  vg.save(); vg.setLineDash([8, 8]); vg.lineWidth = 2; vg.strokeStyle = 'rgba(255,225,77,.85)';
  vg.beginPath(); vg.moveTo(ball.x, ball.y); vg.lineTo(gx, CY); vg.stroke(); vg.setLineDash([]);
  vg.lineWidth = 5; vg.strokeStyle = 'rgba(255,225,77,.9)'; vg.beginPath(); vg.moveTo(gx, GY0); vg.lineTo(gx, GY1); vg.stroke();
  vg.restore();
}

function drawVs32(v, now) {
  const t = (now - v.t0) / 1000, k = easeOut(clamp(t / 0.3, 0, 1));
  vg.fillStyle = 'rgba(6,8,18,.82)'; vg.fillRect(0, 0, W, H);
  const L = players[0], R = players[1];
  vg.save(); vg.globalAlpha = .5;
  let gr = vg.createLinearGradient(0, 0, 520, 0); gr.addColorStop(0, ELEM[L.ch.elem].c); gr.addColorStop(1, 'rgba(0,0,0,0)');
  vg.fillStyle = gr; vg.beginPath(); vg.moveTo(0, 0); vg.lineTo(520, 0); vg.lineTo(440, H); vg.lineTo(0, H); vg.closePath(); vg.fill();
  gr = vg.createLinearGradient(W, 0, 440, 0); gr.addColorStop(0, ELEM[R.ch.elem].c); gr.addColorStop(1, 'rgba(0,0,0,0)');
  vg.fillStyle = gr; vg.beginPath(); vg.moveTo(520, 0); vg.lineTo(W, 0); vg.lineTo(W, H); vg.lineTo(440, H); vg.closePath(); vg.fill();
  vg.restore();
  vg.strokeStyle = 'rgba(255,255,255,.8)'; vg.lineWidth = 3; vg.beginPath(); vg.moveTo(520, 0); vg.lineTo(440, H); vg.stroke();
  bust(vg, L.ch, lerp(-140, 230, k), 338, 1.05);
  bust(vg, R.ch, lerp(W + 140, 730, k), 338, 1.05, { flip: true });
  vg.textBaseline = 'alphabetic';
  vg.font = '700 13px "Azeret Mono", monospace'; vg.textAlign = 'center'; vg.fillStyle = '#ffe14d'; vg.fillText(v.label, 480, 90);
  vg.save(); vg.translate(480, 238); vg.scale(1 + (1 - k) * 0.8, 1 + (1 - k) * 0.8); vg.transform(1, 0, -0.2, 1, 0, 0);
  vg.font = '72px "Dela Gothic One", sans-serif'; vg.lineWidth = 10; vg.lineJoin = 'round'; vg.strokeStyle = '#0b0e1a'; vg.strokeText('VS', 0, 0); vg.fillStyle = '#ffffff'; vg.fillText('VS', 0, 0); vg.restore();
  vg.font = '22px "Dela Gothic One", sans-serif'; vg.textAlign = 'left'; vg.fillStyle = '#ffffff'; vg.fillText(L.ch.name, 40, 118);
  vg.textAlign = 'right'; vg.fillText(R.ch.name, W - 40, 118);
  vg.font = '700 11px "Azeret Mono", monospace';
  vg.textAlign = 'left'; vg.fillStyle = ELEM[L.ch.elem].c; vg.fillText(`${ELEM[L.ch.elem].name.toUpperCase()} · TP ${Math.floor(L.tp)}`, 40, 138);
  vg.textAlign = 'right'; vg.fillStyle = ELEM[R.ch.elem].c; vg.fillText(`TP ${Math.floor(R.tp)} · ${ELEM[R.ch.elem].name.toUpperCase()}`, W - 40, 138);
}

function para32(c, x0, x1, y, h, sk) { c.beginPath(); c.moveTo(x0 + sk, y - h / 2); c.lineTo(x1 + sk, y - h / 2); c.lineTo(x1 - sk, y + h / 2); c.lineTo(x0 - sk, y + h / 2); c.closePath(); }
function drawClash32(c, now) {
  const t = (now - c.t0) / 1000, [L, R] = c.sides;
  vg.fillStyle = 'rgba(6,8,18,.84)'; vg.fillRect(0, 0, W, H);
  const grow = easeOut(clamp(t / 0.5, 0, 1)), push = easeOut(clamp((t - 0.5) / 0.45, 0, 1));
  const tot = (L.score + R.score) || 1, split = 480 + ((L.score - R.score) / tot) * 700 * push;
  const y = 282, h = 48, x0 = 90, x1 = 870;
  const le = lerp(x0, split, grow), re = lerp(x1, split, grow);
  vg.textBaseline = 'alphabetic';
  vg.font = '700 13px "Azeret Mono", monospace'; vg.textAlign = 'center'; vg.fillStyle = '#ffe14d'; vg.fillText(c.title, 480, 150);
  vg.fillStyle = L.color; para32(vg, x0, le, y, h, 8); vg.fill();
  vg.fillStyle = R.color; para32(vg, re, x1, y, h, 8); vg.fill();
  vg.strokeStyle = '#0b0e1a'; vg.lineWidth = 3; para32(vg, x0, le, y, h, 8); vg.stroke(); para32(vg, re, x1, y, h, 8); vg.stroke();
  if (grow >= 0.99) {
    vg.save(); vg.translate(split, y); vg.fillStyle = '#ffffff';
    for (let i = 0; i < 12; i++) { const a = i / 12 * Math.PI * 2 + t * 3, r = 26 + sr(i + Math.floor(t * 12)) * 30; vg.beginPath(); vg.moveTo(Math.cos(a - 0.12) * 8, Math.sin(a - 0.12) * 8); vg.lineTo(Math.cos(a) * r, Math.sin(a) * r); vg.lineTo(Math.cos(a + 0.12) * 8, Math.sin(a + 0.12) * 8); vg.closePath(); vg.fill(); }
    vg.restore();
  }
  vg.font = '34px "Dela Gothic One", sans-serif'; vg.lineWidth = 6; vg.lineJoin = 'round'; vg.strokeStyle = '#0b0e1a'; vg.fillStyle = '#ffffff';
  vg.textAlign = 'left'; vg.strokeText(String(Math.round(L.score * grow)), x0 + 12, y + 12); vg.fillText(String(Math.round(L.score * grow)), x0 + 12, y + 12);
  vg.textAlign = 'right'; vg.strokeText(String(Math.round(R.score * grow)), x1 - 12, y + 12); vg.fillText(String(Math.round(R.score * grow)), x1 - 12, y + 12);
  vg.font = '22px "Dela Gothic One", sans-serif';
  vg.textAlign = 'left'; vg.fillText(L.name, x0, y - 44); vg.textAlign = 'right'; vg.fillText(R.name, x1, y - 44);
  const modTxt = s => [s.sig > 1 ? '×1.1 signature' : '', s.mod > 1 ? '×1.2 element edge' : ''].filter(Boolean).join('  ');
  vg.font = '700 12px "Azeret Mono", monospace';
  vg.textAlign = 'left'; vg.fillStyle = L.color; vg.fillText(`${L.move.name} · ${ELEM[L.move.elem].name}`, x0, y + 50);
  vg.fillStyle = '#ffe14d'; vg.fillText(modTxt(L), x0, y + 70);
  vg.textAlign = 'right'; vg.fillStyle = R.color; vg.fillText(`${R.move.name} · ${ELEM[R.move.elem].name}`, x1, y + 50);
  vg.fillStyle = '#ffe14d'; vg.fillText(modTxt(R), x1, y + 70);
  if (t > 0.95) {
    const win = c.winTeam === 0 ? L : R, k = easeBack(clamp((t - 0.95) / 0.25, 0, 1));
    vg.save(); vg.translate(480, 400); vg.scale(k, k); vg.transform(1, 0, -0.15, 1, 0, 0);
    vg.font = '36px "Dela Gothic One", sans-serif'; vg.textAlign = 'center'; vg.lineWidth = 8; vg.strokeStyle = '#0b0e1a'; vg.strokeText(c.verdict, 0, 0);
    vg.fillStyle = win.color; vg.fillText(c.verdict, 0, 0); vg.restore();
  }
}

function drawBanner32(b, now) {
  const t = (now - b.t0) / 1000, D = b.dur / 1000;
  const k = easeBack(clamp(t / 0.3, 0, 1)), out = t > D - 0.25 ? clamp((t - (D - 0.25)) / 0.25, 0, 1) : 0;
  vg.save(); vg.globalAlpha = 1 - out;
  vg.fillStyle = 'rgba(6,8,18,.7)'; vg.beginPath(); vg.moveTo(0, 214); vg.lineTo(W, 196); vg.lineTo(W, 356); vg.lineTo(0, 374); vg.closePath(); vg.fill();
  vg.save(); vg.translate(480, 292); vg.scale(k, k); vg.transform(1, 0, -0.16, 1, 0, 0);
  vg.font = `${b.big ? 112 : 64}px "Dela Gothic One", sans-serif`; vg.textAlign = 'center'; vg.textBaseline = 'middle'; vg.lineJoin = 'round';
  vg.lineWidth = 14; vg.strokeStyle = '#0b0e1a'; vg.strokeText(b.text, 0, 0);
  vg.fillStyle = '#ffffff'; vg.fillText(b.text, 6, 6); vg.fillStyle = b.color; vg.fillText(b.text, 0, 0);
  vg.restore();
  vg.font = '700 14px "Azeret Mono", monospace'; vg.textAlign = 'center'; vg.textBaseline = 'alphabetic'; vg.fillStyle = '#eef1f8';
  vg.fillText(b.sub, 480, b.big ? 372 - 30 : 350);
  vg.restore();
}

function bigBall32(x, y, r, E, white) {
  if (!white) { const gr = vg.createRadialGradient(x, y, r * 0.5, x, y, r * 3); gr.addColorStop(0, E.g); gr.addColorStop(1, 'rgba(0,0,0,0)'); vg.fillStyle = gr; circle(vg, x, y, r * 3); vg.fill(); }
  vg.fillStyle = '#ffffff'; vg.strokeStyle = white ? '#ffffff' : '#0b0e1a'; vg.lineWidth = 4; circle(vg, x, y, r); vg.fill(); vg.stroke();
  if (!white) { vg.save(); circle(vg, x, y, r); vg.clip(); vg.fillStyle = '#20242e'; for (let i = 0; i < 3; i++) { const a = performance.now() / 60 + i * 2.094; circle(vg, x + Math.cos(a) * r * 0.6, y + Math.sin(a) * r * 0.6, r * 0.32); vg.fill(); } vg.restore(); }
}

function fxBack32(el, t, ts, fr, cx, cy) {
  if (el === 'flame') {
    const cols = ['rgba(255,70,40,.55)', 'rgba(255,150,60,.6)', 'rgba(255,225,150,.55)'];
    for (let L = 0; L < 3; L++) {
      const R = 190 - L * 45, n = 16; vg.beginPath();
      for (let i = 0; i <= n * 2; i++) {
        const a = -Math.PI / 2 + (i / (n * 2)) * Math.PI * 2;
        const sp = i % 2 === 0 ? R + 50 + Math.sin(ts * 9 + i * 1.7 + L) * 30 : R * 0.8;
        const x = cx + Math.cos(a) * sp * 0.9, y = cy - 70 + Math.sin(a) * sp * 1.15 - (i % 2 === 0 ? Math.max(0, -Math.sin(a)) * 50 : 0);
        i ? vg.lineTo(x, y) : vg.moveTo(x, y);
      }
      vg.closePath(); vg.fillStyle = cols[L]; vg.fill();
    }
    vg.fillStyle = '#ffd28a';
    for (let i = 0; i < 46; i++) { const x = sr(i * 3.1) * W, y = H + 20 - ((t * (140 + sr(i) * 160) + sr(i * 9.7) * H) % (H + 40)); const s = 2 + sr(i * 1.9) * 4; vg.globalAlpha = 0.5 + sr(i * 2.3) * 0.5; vg.fillRect(x, y, s, s); }
    vg.globalAlpha = 1;
  } else if (el === 'gale') {
    for (let i = 0; i < 5; i++) {
      vg.save(); vg.translate(cx, cy - 50); vg.rotate(ts * 2.2 + i * 1.2); vg.scale(1, 0.38);
      vg.beginPath(); vg.arc(0, 0, 150 + i * 30, 0.2, 0.2 + Math.PI * 1.2); vg.lineWidth = 7 - i; vg.strokeStyle = 'rgba(210,255,248,.6)'; vg.stroke(); vg.restore();
    }
    vg.strokeStyle = 'rgba(220,255,250,.4)'; vg.lineWidth = 2;
    for (let i = 0; i < 26; i++) { const y = sr(i * 4.4) * H, x = ((t * 1400 + sr(i + 3) * 1300) % 1400) - 250; vg.beginPath(); vg.moveTo(x, y); vg.lineTo(x + 90 + sr(i) * 80, y); vg.stroke(); }
  } else if (el === 'stone') {
    vg.strokeStyle = 'rgba(40,24,6,.7)'; vg.lineWidth = 4;
    for (let i = 0; i < 9; i++) {
      let x = cx + 60 + (i - 4) * 70, y = H; vg.beginPath(); vg.moveTo(x, y);
      for (let j = 0; j < 5; j++) { x += (sr(i * 10 + j) - 0.5) * 60; y -= 30 + sr(i * 7 + j) * 30; vg.lineTo(x, y); }
      vg.stroke();
    }
    for (let i = 0; i < 14; i++) {
      const a = i / 14 * Math.PI * 2 + ts * 0.9, r = 210 + sr(i) * 70;
      const x = cx + Math.cos(a) * r, y = cy - 70 + Math.sin(a) * r * 0.55 - ((t * 40) % 20), s = 14 + sr(i * 3) * 22;
      vg.save(); vg.translate(x, y); vg.rotate(ts * 2 + i);
      vg.beginPath(); vg.moveTo(-s, -s * 0.3); vg.lineTo(-s * 0.2, -s); vg.lineTo(s, -s * 0.4); vg.lineTo(s * 0.6, s * 0.8); vg.lineTo(-s * 0.7, s * 0.6); vg.closePath();
      vg.fillStyle = i % 2 ? '#c98f2c' : '#9a6a1c'; vg.fill(); vg.strokeStyle = '#2b1d07'; vg.lineWidth = 3; vg.stroke(); vg.restore();
    }
  }
}

function fxTrail32(el, sx, sy, x, y, t) {
  const n = 10;
  for (let i = 1; i < n; i++) {
    const u = i / n, px = lerp(sx, x, u), py = lerp(sy, y, u);
    if (el === 'flame') { vg.fillStyle = i % 2 ? '#ffd28a' : '#ff5a36'; vg.beginPath(); vg.moveTo(px - 20, py - 30); vg.lineTo(px + 30, py - 70 - sr(i + t * 12) * 40); vg.lineTo(px + 26, py - 20); vg.closePath(); vg.fill(); }
    else if (el === 'gale') { vg.strokeStyle = 'rgba(230,255,252,.8)'; vg.lineWidth = 4; vg.beginPath(); vg.ellipse(px, py, 16, 52, -0.3, 0, Math.PI * 2); vg.stroke(); }
    else if (el === 'stone') { vg.fillStyle = i % 2 ? '#c98f2c' : '#6d4a12'; const s = 10 + sr(i * 3) * 12; vg.fillRect(px - s / 2 + (sr(i) - .5) * 60, py - s / 2 + (sr(i * 2) - .5) * 70, s, s); }
  }
}

function barrier32(el, u, t, fr) {
  if (el === 'flame') {
    for (let i = 0; i < 10; i++) {
      const x = 590 + i * 20, hh = u * (360 + sr(i + fr) * 90);
      for (const [col, sc] of [['#ff5a36', 1], ['#ffb347', 0.75], ['#fff0c2', 0.45]]) { vg.fillStyle = col; vg.beginPath(); vg.moveTo(x - 24 * sc, H); vg.quadraticCurveTo(x - 10 * sc, H - hh * sc * 0.6, x + (sr(i * 2 + fr) - .5) * 20, H - hh * sc); vg.quadraticCurveTo(x + 14 * sc, H - hh * sc * 0.5, x + 24 * sc, H); vg.closePath(); vg.fill(); }
    }
  } else if (el === 'gale') {
    vg.save(); vg.translate(690, 290); vg.globalAlpha = u;
    for (let i = 0; i < 8; i++) { vg.save(); vg.rotate(t * 6 + i * 0.8); vg.beginPath(); vg.ellipse(0, 0, 40 + i * 14, 150 + i * 12, 0, 0.3, Math.PI * 1.5); vg.strokeStyle = i % 2 ? '#c9fff6' : '#35d6c0'; vg.lineWidth = 6; vg.stroke(); vg.restore(); }
    vg.restore();
  } else if (el === 'stone') {
    const top = H - u * 450;
    const gr = vg.createLinearGradient(0, top, 0, H); gr.addColorStop(0, '#e0b25a'); gr.addColorStop(1, '#6d4a12');
    vg.fillStyle = gr; vg.beginPath(); vg.moveTo(600, H); vg.lineTo(610, top + 20); vg.lineTo(650, top); vg.lineTo(740, top + 10); vg.lineTo(770, H); vg.closePath(); vg.fill();
    vg.strokeStyle = '#2b1d07'; vg.lineWidth = 4; vg.stroke();
    vg.lineWidth = 3; vg.beginPath(); vg.moveTo(660, top + 30); vg.lineTo(690, top + 110); vg.lineTo(670, top + 180); vg.moveTo(690, top + 110); vg.lineTo(730, top + 150); vg.stroke();
  }
}

function drawCut32(o, now) {
  const t = (now - o.t0) / 1000, D = o.dur / 1000, fr = Math.floor(t * 12), ts = fr / 12;
  const m = o.m, E = ELEM[m.elem], ch = o.p.ch;
  const impact = !reduced && t >= 1.22 && t < 1.36;
  if (!o.boom && t >= 1.22) { o.boom = true; sfx('impact'); }
  vg.save();
  if (!reduced && t > 1.36 && t < 1.8) { const a = (1.8 - t) * 18; vg.translate((sr(fr * 3.3) - .5) * a, (sr(fr * 7.1) - .5) * a); }
  if (impact) vg.fillStyle = '#000000';
  else { const gr = vg.createRadialGradient(640, 280, 10, 640, 280, 720); gr.addColorStop(0, E.g); gr.addColorStop(.3, E.c); gr.addColorStop(1, E.d); vg.fillStyle = gr; }
  vg.fillRect(-30, -30, W + 60, H + 60);
  vg.save(); vg.translate(600, 300); vg.fillStyle = impact ? '#ffffff' : 'rgba(255,255,255,.28)';
  for (let i = 0; i < 70; i++) {
    const a = sr(i * 13.1 + fr * 97.3) * Math.PI * 2, r0 = 120 + sr(i * 7.7 + fr * 31.1) * 160, w = 0.004 + sr(i * 3.3 + fr * 11.9) * 0.014;
    vg.beginPath(); vg.moveTo(Math.cos(a) * r0, Math.sin(a) * r0); vg.lineTo(Math.cos(a - w) * 1000, Math.sin(a - w) * 1000); vg.lineTo(Math.cos(a + w) * 1000, Math.sin(a + w) * 1000); vg.closePath(); vg.fill();
  }
  vg.restore();
  const slide = easeBack(clamp(ts / 0.42, 0, 1));
  let bx = -280 + slide * 530; const by = 340 + Math.sin(ts * 5) * 4;
  const fin = clamp((t - 1.36) / 0.5, 0, 1);
  if (!impact) fxBack32(m.elem, t, ts, fr, bx, by);
  if (m.kind === 'dribble' && t >= 1.36) {
    const e = easeOut(fin);
    for (let i = 4; i >= 1; i--) { vg.globalAlpha = 0.5 - i * 0.1; bust(vg, ch, bx + e * 760 - i * 80, by, 2.1, { sil: E.c }); }
    vg.globalAlpha = 1; bx += e * 760;
  }
  bust(vg, ch, bx, by, 2.1, { sil: impact ? '#ffffff' : null });
  if (t > 0.45 && t < 1.36 && !impact) {
    vg.fillStyle = E.g;
    for (let i = 0; i < 30; i++) { const a = sr(i * 5.3) * Math.PI * 2 + t * 1.5, r = (1 - ((t * 1.6 + sr(i * 2.2)) % 1)) * 300; const px = 560 + Math.cos(a) * r, py = 380 + Math.sin(a) * r * 0.7; vg.fillRect(px - 2.5, py - 2.5, 5, 5); }
  }
  if (m.kind === 'shot' && t < 1.36) bigBall32(560, 380, 22 + (impact ? 0 : Math.sin(t * 30) * 1.5), E, impact);
  if (t >= 1.36) {
    if (m.kind === 'shot') {
      const e = fin * fin, sx = 560, sy = 380, x = lerp(sx, 1180, e), y = lerp(sy, 190, e);
      vg.save(); vg.lineCap = 'round'; const cols = [E.d, E.c, E.g, '#ffffff'];
      for (let i = 0; i < 4; i++) { vg.strokeStyle = cols[i]; vg.lineWidth = 78 - i * 18; vg.beginPath(); vg.moveTo(sx - 60, sy + 20); vg.lineTo(x, y); vg.stroke(); }
      vg.restore();
      fxTrail32(m.elem, sx, sy, x, y, t);
      bigBall32(x, y, 24, E, false);
    } else if (m.kind === 'block') barrier32(m.elem, easeOut(fin), t, fr);
  }
  if (t > 0.3) {
    const k = Math.max(0, 1 - (t - 0.3) / 0.14), sc = 1 + k * 1.8;
    vg.save(); vg.translate(640, 138);
    vg.font = '64px "Dela Gothic One", "Arial Black", sans-serif';
    const tw = vg.measureText(m.name).width, fit = Math.min(1, 560 / tw);
    vg.scale(sc * fit, sc * fit); vg.transform(1, 0, -0.2, 1, 0, 0);
    vg.textAlign = 'center'; vg.textBaseline = 'middle'; vg.lineJoin = 'round';
    vg.lineWidth = 12; vg.strokeStyle = impact ? '#ffffff' : '#0b0e1a'; vg.strokeText(m.name, 0, 0);
    if (!impact) { vg.fillStyle = E.c; vg.fillText(m.name, 5, 5); }
    vg.fillStyle = impact ? '#000000' : '#ffffff'; vg.fillText(m.name, 0, 0);
    vg.restore();
    vg.font = '700 15px "Azeret Mono", monospace'; vg.textAlign = 'center'; vg.textBaseline = 'alphabetic';
    vg.fillStyle = impact ? '#ffffff' : 'rgba(255,255,255,.92)';
    vg.fillText(`${ch.name.toUpperCase()}  ·  ${E.name.toUpperCase()} ${KIND[m.kind].toUpperCase()}`, 640, 200);
  }
  const lb = Math.min(1, t / 0.16) * 56;
  vg.fillStyle = '#05070e'; vg.fillRect(-30, -30, W + 60, lb + 30); vg.fillRect(-30, H - lb, W + 60, lb + 30);
  if (lb >= 56) {
    vg.font = '700 12px "Azeret Mono", monospace'; vg.textBaseline = 'middle';
    vg.textAlign = 'left'; vg.fillStyle = E.c; vg.fillText(`${KIND[m.kind].toUpperCase()}  ·  ${E.name.toUpperCase()}  ·  PWR ${m.power}  ·  ${m.tp} TP`, 24, H - 28);
    vg.textAlign = 'right'; vg.fillStyle = '#98a3c2'; vg.fillText('Space or tap to skip', W - 24, H - 28);
    vg.textBaseline = 'alphabetic';
  }
  if (t > D - 0.22) { vg.fillStyle = `rgba(5,7,14,${clamp((t - (D - 0.22)) / 0.22, 0, 1)})`; vg.fillRect(-30, -30, W + 60, H + 60); }
  vg.restore();
}

// ---------- characters (shared bust art) ----------
function eye(c, ch, ex, ey, right) {
  c.save(); c.translate(ex, ey); if (!right) c.scale(-1, 1);
  c.beginPath(); c.moveTo(-8, 2); c.quadraticCurveTo(0, -7, 11, -3); c.quadraticCurveTo(4, 5, -8, 2); c.closePath();
  c.fillStyle = '#ffffff'; c.fill();
  c.save(); c.clip();
  c.beginPath(); c.arc(1.5, -1, 5, 0, Math.PI * 2); c.fillStyle = ch.eye; c.fill();
  c.beginPath(); c.arc(1.5, -1, 2.4, 0, Math.PI * 2); c.fillStyle = '#111318'; c.fill();
  c.beginPath(); c.arc(3.2, -3, 1.3, 0, Math.PI * 2); c.fillStyle = '#ffffff'; c.fill();
  c.restore();
  c.beginPath(); c.moveTo(-9, 2); c.quadraticCurveTo(0, -8, 12, -3.5); c.lineWidth = 2.6; c.strokeStyle = '#0b0e1a'; c.stroke();
  c.beginPath(); c.moveTo(-9, -9); c.lineTo(12, -15); c.lineTo(13, -11.5); c.lineTo(-8, -5.5); c.closePath(); c.fillStyle = ch.brow; c.fill();
  c.restore();
}
function hair(c, ch, sil) {
  const poly = pts => { c.beginPath(); pts.forEach(([x, y], i) => i ? c.lineTo(x, y) : c.moveTo(x, y)); c.closePath(); };
  if (ch.id === 'haru') {
    poly([[-37, -62], [-54, -84], [-40, -90], [-58, -120], [-28, -106], [-24, -144], [-4, -114], [12, -150], [20, -112], [44, -134], [38, -100], [64, -104], [42, -78], [37, -62], [30, -80], [22, -66], [16, -86], [6, -70], [-2, -90], [-12, -70], [-18, -88], [-27, -68]]);
    c.fillStyle = sil || ch.hair; c.fill(); c.stroke();
    if (!sil) {
      c.fillStyle = ch.hairHi;
      poly([[-22, -104], [-10, -132], [-6, -108]]); c.fill();
      poly([[16, -108], [34, -126], [28, -102]]); c.fill();
      poly([[-44, -94], [-50, -112], [-34, -102]]); c.fill();
    }
  } else {
    poly([[-42, -36], [-46, -80], [-36, -106], [-12, -120], [16, -118], [40, -102], [48, -74], [44, -30], [50, -4], [36, -12], [33, -50], [27, -76], [14, -86], [6, -72], [-2, -84], [-8, -60], [-15, -40], [-23, -28], [-31, -42], [-36, -18]]);
    c.fillStyle = sil || ch.hair; c.fill(); c.stroke();
    if (!sil) {
      c.strokeStyle = ch.hairHi; c.lineWidth = 3;
      c.beginPath(); c.moveTo(-20, -110); c.quadraticCurveTo(-32, -80, -26, -48); c.stroke();
      c.beginPath(); c.moveTo(20, -110); c.quadraticCurveTo(38, -86, 41, -40); c.stroke();
      c.beginPath(); c.moveTo(0, -116); c.quadraticCurveTo(-4, -100, -3, -86); c.stroke();
    }
  }
}
function bust(c, ch, x, y, s, o = {}) {
  const sil = o.sil || null, O = '#0b0e1a';
  const fill = col => { c.fillStyle = sil || col; };
  c.save(); c.translate(x, y); c.scale(o.flip ? -s : s, s);
  c.lineJoin = 'round'; c.lineCap = 'round'; c.lineWidth = 3; c.strokeStyle = sil || O;
  c.beginPath(); c.moveTo(-100, 140); c.lineTo(-92, 62); c.quadraticCurveTo(-84, 18, -38, 8); c.lineTo(38, 8); c.quadraticCurveTo(84, 18, 92, 62); c.lineTo(100, 140); c.closePath();
  fill(ch.jersey); c.fill(); c.stroke();
  if (!sil) {
    c.fillStyle = ch.trim;
    c.beginPath(); c.moveTo(-28, 8); c.lineTo(0, 42); c.lineTo(28, 8); c.lineTo(17, 8); c.lineTo(0, 27); c.lineTo(-17, 8); c.closePath(); c.fill();
    for (const sd of [-1, 1]) { c.beginPath(); c.moveTo(sd * 92, 64); c.quadraticCurveTo(sd * 84, 22, sd * 46, 11); c.lineTo(sd * 42, 21); c.quadraticCurveTo(sd * 72, 32, sd * 79, 66); c.closePath(); c.fill(); }
    c.save(); if (o.flip) c.scale(-1, 1);
    c.font = '34px "Dela Gothic One", "Arial Black", sans-serif'; c.textAlign = 'center'; c.textBaseline = 'alphabetic'; c.fillStyle = ch.trim;
    c.fillText(String(ch.num), o.flip ? -48 : 48, 106); c.restore();
  }
  c.beginPath(); c.rect(-13, -28, 26, 38); fill(ch.skin); c.fill(); c.stroke();
  if (!sil) { c.fillStyle = 'rgba(60,20,10,.22)'; c.beginPath(); c.moveTo(-13, -22); c.quadraticCurveTo(0, -8, 13, -22); c.lineTo(13, -10); c.quadraticCurveTo(0, 0, -13, -10); c.closePath(); c.fill(); }
  for (const sd of [-1, 1]) { c.beginPath(); c.ellipse(sd * 33, -56, 6, 10, 0, 0, Math.PI * 2); fill(ch.skin); c.fill(); c.stroke(); }
  c.beginPath(); c.moveTo(-33, -80); c.quadraticCurveTo(-35, -42, -19, -26); c.quadraticCurveTo(0, -10, 19, -26); c.quadraticCurveTo(35, -42, 33, -80); c.quadraticCurveTo(0, -114, -33, -80); c.closePath();
  fill(ch.skin); c.fill(); c.stroke();
  if (!sil) {
    eye(c, ch, -14, -57, false); eye(c, ch, 14, -57, true);
    c.strokeStyle = 'rgba(90,40,25,.55)'; c.lineWidth = 1.8; c.beginPath(); c.moveTo(1, -50); c.lineTo(-2, -41); c.lineTo(3, -41); c.stroke();
    c.strokeStyle = O; c.lineWidth = 2.4; c.beginPath(); c.moveTo(-8, -32); c.quadraticCurveTo(1, -29, 9, -34); c.stroke();
  }
  c.lineWidth = 3; c.strokeStyle = sil || O;
  hair(c, ch, sil);
  c.restore();
}

// ============================================================================
// 12-BIT AMIGA RETRO PIPELINE RENDERING
// ============================================================================
const bg12 = document.createElement('canvas'); bg12.width = LW; bg12.height = LH;
function drawStatic12() {
  const c = bg12.getContext('2d');
  c.imageSmoothingEnabled = false;
  c.fillStyle = '#012'; c.fillRect(0, 0, LW, LH);
  const crowd = ['#235', '#123', '#347', '#641', '#c32', '#076', '#456'];
  for (let i = 0; i < 420; i++) {
    const zone = sr(i * 9.3); let x, y;
    if (zone < 0.55) { x = Math.round(sr(i * 1.3) * LW); y = Math.round(2 + sr(i * 2.7) * (F.y0 / 3 - 6)); }
    else if (zone < 0.8) { x = Math.round(sr(i * 1.3) * LW); y = Math.round(F.y1 / 3 + 3 + sr(i * 2.7) * (LH - F.y1 / 3 - 5)); }
    else { x = Math.round(sr(i * 1.3) < 0.5 ? sr(i * 4.1) * (F.x0 / 3 - 10) : (F.x1 / 3 + 10 + sr(i * 4.1) * (LW - F.x1 / 3 - 11))); y = Math.round(F.y0 / 3 + sr(i * 2.7) * ((F.y1 - F.y0) / 3)); }
    c.fillStyle = crowd[Math.floor(sr(i * 5.1) * crowd.length)]; c.fillRect(x, y, 1, 1);
  }
  const fx0 = Math.round(F.x0 / 3), fy0 = Math.round(F.y0 / 3);
  const fx1 = Math.round(F.x1 / 3), fy1 = Math.round(F.y1 / 3);
  const cx = Math.round(CX / 3), cy = Math.round(CY / 3);
  const gy0 = Math.round(GY0 / 3), gy1 = Math.round(GY1 / 3);
  for (let i = 0; i < 24; i++) {
    c.fillStyle = i % 2 ? '#c32' : '#942';
    c.fillRect(fx0 + i * 12, fy0 - 4, 11, 2);
    c.fillRect(fx0 + i * 12, fy1 + 2, 11, 2);
  }
  const n = 14, sw = (fx1 - fx0) / n;
  for (let i = 0; i < n; i++) {
    const x = Math.round(fx0 + i * sw), w = Math.round(fx0 + (i + 1) * sw) - x;
    c.fillStyle = i % 2 ? '#173' : '#152';
    c.fillRect(x, fy0, w, fy1 - fy0);
  }
  for (const side of [0, 1]) {
    const nx = side === 0 ? fx0 - 9 : fx1;
    c.fillStyle = '#123'; c.fillRect(nx, gy0, 9, gy1 - gy0);
    c.fillStyle = '#235';
    for (let yy = gy0; yy <= gy1; yy += 3) c.fillRect(nx, yy, 9, 1);
    for (let xx = nx; xx <= nx + 9; xx += 3) c.fillRect(xx, gy0, 1, gy1 - gy0);
    c.strokeStyle = '#def'; c.lineWidth = 1; c.strokeRect(nx, gy0, 9, gy1 - gy0);
  }
  c.fillStyle = '#bea'; c.strokeStyle = '#bea'; c.lineWidth = 1;
  c.strokeRect(fx0, fy0, fx1 - fx0, fy1 - fy0);
  c.beginPath(); c.moveTo(cx, fy0); c.lineTo(cx, fy1); c.stroke();
  c.beginPath(); c.arc(cx, cy, 21, 0, Math.PI * 2); c.stroke();
  c.fillRect(cx - 1, cy - 1, 2, 2);
  for (const side of [0, 1]) {
    const dir = side === 0 ? 1 : -1, gx = side === 0 ? fx0 : fx1;
    const px = side === 0 ? gx : gx - 39;
    c.strokeRect(px, cy - 41, 39, 83);
    const bx = side === 0 ? gx : gx - 13;
    c.strokeRect(bx, gy0 - 8, 13, gy1 - gy0 + 16);
    c.fillRect(gx + dir * 28 - 1, cy - 1, 2, 2);
    c.beginPath();
    c.arc(gx + dir * 28, cy, 17, side === 0 ? -0.93 : Math.PI - 0.93, side === 0 ? 0.93 : Math.PI + 0.93);
    c.stroke();
  }
  for (const [ax, ay, a0] of [[fx0, fy0, 0], [fx1, fy0, Math.PI / 2], [fx1, fy1, Math.PI], [fx0, fy1, Math.PI * 1.5]]) {
    c.beginPath(); c.arc(ax, ay, 4, a0, a0 + Math.PI / 2); c.stroke();
  }
  c.fillStyle = '#fff';
  for (const [px, py] of [[fx0, gy0], [fx0, gy1], [fx1, gy0], [fx1, gy1]]) {
    c.fillRect(px - 1, py - 1, 3, 3);
  }
  c.beginPath();
  c.moveTo(fx0, gy0); c.lineTo(fx0, gy1);
  c.moveTo(fx1, gy0); c.lineTo(fx1, gy1);
  c.stroke();
}

function drawPlayer12(p, now) {
  const ch = p.ch, moving = Math.hypot(p.vx, p.vy) > 20;
  const bob = moving ? (Math.floor(now / 110) % 2) : 0;
  const rx = Math.round(p.x / 3);
  const ry = Math.round(p.y / 3) + bob;
  g12.fillStyle = '#012'; g12.fillRect(rx - 4, ry + 4, 9, 2);
  if (p.human) { g12.fillStyle = '#fe3'; g12.fillRect(rx - 1, ry - 14, 3, 2); g12.fillRect(rx, ry - 12, 1, 1); }
  if (p.dash > 0) {
    const gx = Math.round((p.x - p.vx * 0.04) / 3), gy = Math.round((p.y - p.vy * 0.04) / 3);
    g12.fillStyle = ELEM[ch.elem].c12; circle(g12, gx, gy, 4); g12.fill();
  }
  g12.lineWidth = 1; g12.strokeStyle = '#012';
  g12.fillStyle = ch.jersey; circle(g12, rx, ry, 4.5); g12.fill(); g12.stroke();
  g12.fillStyle = ch.trim; g12.fillRect(rx - 1, ry + 1, 2, 2);
  const hx = rx + Math.round(p.fx * 1.5), hy = ry - 3 + Math.round(p.fy * 0.8);
  g12.fillStyle = ch.hair;
  const back = Math.atan2(-p.fy, -p.fx);
  const spikes = ch.id === 'haru' ? 5 : 3;
  for (let i = 0; i < spikes; i++) {
    const a = back + (i - (spikes - 1) / 2) * (ch.id === 'haru' ? 0.5 : 0.7);
    const len = ch.id === 'haru' ? 5 : 4.5;
    g12.beginPath();
    g12.moveTo(hx + Math.round(Math.cos(a - 0.35) * 2.5), hy + Math.round(Math.sin(a - 0.35) * 2.5));
    g12.lineTo(hx + Math.round(Math.cos(a) * len), hy + Math.round(Math.sin(a) * len));
    g12.lineTo(hx + Math.round(Math.cos(a + 0.35) * 2.5), hy + Math.round(Math.sin(a + 0.35) * 2.5));
    g12.closePath(); g12.fill(); g12.stroke();
  }
  circle(g12, hx, hy, 3); g12.fill(); g12.stroke();
  g12.save(); circle(g12, hx, hy, 3); g12.clip();
  g12.fillStyle = ch.skin; circle(g12, hx + Math.round(p.fx * 1.5), hy + Math.round(p.fy + 1), 2); g12.fill();
  g12.restore();
  g12.font = '6px "Press Start 2P", monospace';
  g12.textAlign = 'center'; g12.textBaseline = 'middle';
  g12.fillStyle = '#012'; g12.fillRect(rx - 11, ry - 10, 22, 6);
  g12.strokeStyle = '#235'; g12.strokeRect(rx - 11, ry - 10, 22, 6);
  g12.fillStyle = p.human ? '#fe3' : ELEM[ch.elem].c12;
  g12.fillText(ch.short, rx, ry - 7);
  if (p.stun > 0) {
    g12.fillStyle = '#fe3';
    for (let i = 0; i < 3; i++) {
      const a = now / 150 + i * 2.094;
      const sx = hx + Math.round(Math.cos(a) * 5), sy = hy - 4 + Math.round(Math.sin(a) * 2);
      g12.fillRect(sx, sy, 1, 1);
    }
  }
  g12.textBaseline = 'alphabetic';
}

function drawKeeper12(k) {
  const d = k.dive > 0 ? Math.sin(clamp((0.6 - k.dive) / 0.2, 0, 1) * Math.PI / 2) : 0;
  const rx = Math.round(k.x / 3);
  const ry = Math.round((k.y + k.dd * d * 14) / 3);
  g12.fillStyle = '#012'; g12.fillRect(rx - 4, ry + 4, 9, 2);
  g12.save(); g12.translate(rx, ry);
  g12.rotate(k.dd * d * 0.9 * (k.team === 0 ? 1 : -1));
  g12.lineWidth = 1; g12.strokeStyle = '#012';
  g12.fillStyle = k.team === 0 ? '#4b6' : '#76d';
  g12.beginPath(); g12.ellipse(0, 0, 4, 4.5, 0, 0, Math.PI * 2); g12.fill(); g12.stroke();
  g12.fillStyle = '#fff';
  const gx = k.team === 0 ? 3 : -3;
  circle(g12, gx, -4 - Math.round(d * 2), 1.5); g12.fill(); g12.stroke();
  circle(g12, gx, 4 + Math.round(d * 2), 1.5); g12.fill(); g12.stroke();
  g12.fillStyle = '#123'; circle(g12, 0, -2, 2.5); g12.fill(); g12.stroke();
  g12.restore();
}

function drawBall12(now) {
  const s = ball.shot, special = !!(s && s.move.tp > 0), E = s ? ELEM[s.elem] : ELEM.none;
  const bx = Math.round(ball.x / 3), by = Math.round(ball.y / 3);
  if (s) {
    for (let i = 0; i < trail.length; i++) {
      const tx = Math.round(trail[i].x / 3), ty = Math.round(trail[i].y / 3);
      g12.fillStyle = special ? (i % 2 === 0 ? E.c12 : E.g12) : '#fff';
      g12.fillRect(tx, ty, 1, 1);
    }
    if (special) {
      g12.strokeStyle = E.g12; g12.lineWidth = 1; circle(g12, bx, by, 6); g12.stroke();
      g12.strokeStyle = E.c12; circle(g12, bx, by, 9); g12.stroke();
    }
  }
  g12.fillStyle = '#012'; g12.fillRect(bx - 2, by + 4, 5, 1);
  const body = !special ? '#fff' : (s.elem === 'flame' ? '#fa4' : (s.elem === 'gale' ? '#bfd' : (s.elem === 'stone' ? '#ec7' : '#fff')));
  g12.fillStyle = '#012'; g12.fillRect(bx - 3, by - 3, 6, 6);
  g12.fillStyle = body; g12.fillRect(bx - 2, by - 3, 4, 6); g12.fillRect(bx - 3, by - 2, 6, 4);
  g12.fillStyle = special ? E.c12 : '#123';
  for (let i = 0; i < 3; i++) {
    const a = ball.spin + i * 2.094;
    g12.fillRect(bx + Math.round(Math.cos(a) * 1.5), by + Math.round(Math.sin(a) * 1.5), 1, 1);
  }
  if (s) {
    const txt = special ? `${s.move.name.toUpperCase()} ${Math.round(s.power)}` : `SHOT ${Math.round(s.power)}`;
    g12.font = '6px "Press Start 2P", monospace';
    const tw = g12.measureText(txt).width;
    const lx = clamp(bx, 20 + tw / 2, LW - 20 - tw / 2), ly = Math.max(14, by - 9);
    g12.fillStyle = '#012'; g12.fillRect(lx - tw / 2 - 2, ly - 4, tw + 4, 8);
    g12.strokeStyle = '#235'; g12.lineWidth = 1; g12.strokeRect(lx - tw / 2 - 2, ly - 4, tw + 4, 8);
    g12.fillStyle = special ? E.c12 : '#def';
    g12.textAlign = 'center'; g12.textBaseline = 'middle'; g12.fillText(txt, lx, ly); g12.textBaseline = 'alphabetic';
  }
}

function drawHUD12() {
  const w = 92, h = 15, x = 160 - w / 2, y = 3;
  g12.fillStyle = '#012'; g12.fillRect(x, y, w, h);
  g12.strokeStyle = '#235'; g12.lineWidth = 1; g12.strokeRect(x, y, w, h);
  g12.fillStyle = HARU.trim; g12.fillRect(x + 3, y + 3, 2, 9);
  g12.fillStyle = JIN.trim; g12.fillRect(x + w - 5, y + 3, 2, 9);
  g12.textBaseline = 'middle';
  g12.font = '7px "Press Start 2P", monospace';
  g12.fillStyle = '#def';
  g12.textAlign = 'left'; g12.fillText('H', x + 8, y + h / 2);
  g12.textAlign = 'right'; g12.fillText('J', x + w - 8, y + h / 2);
  g12.textAlign = 'center'; g12.fillStyle = '#fe3';
  g12.fillText(`${score[0]}-${score[1]}`, 160, y + h / 2);
  g12.textBaseline = 'alphabetic';
  const drawTP12 = (p, tx, ty, right) => {
    const bw = 60, bh = 5, bx = right ? tx - bw : tx;
    g12.font = '6px "Press Start 2P", monospace'; g12.textAlign = right ? 'right' : 'left'; g12.fillStyle = '#89a';
    g12.fillText(`TP ${Math.floor(p.tp)}`, tx, ty + 5);
    g12.fillStyle = '#123'; g12.fillRect(bx, ty + 7, bw, bh);
    g12.strokeStyle = '#235'; g12.lineWidth = 1; g12.strokeRect(bx, ty + 7, bw, bh);
    const active = Math.floor((p.tp / p.ch.maxTP) * 12);
    for (let i = 0; i < 12; i++) {
      if (i < active) {
        g12.fillStyle = '#fe3';
        const sx = right ? (tx - (i + 1) * 5) : (bx + i * 5);
        g12.fillRect(sx + 1, ty + 8, 4, bh - 2);
      }
    }
  };
  drawTP12(haru, 6, 2, false);
  drawTP12(jin, LW - 6, 2, true);
}

// Phase 2 Canonical 320x180 Mock Scene
function renderMockFrame() {
  g12.setTransform(1, 0, 0, 1, 0, 0);
  g12.drawImage(bg12, 0, 0, LW, LH);
  keepers.forEach(drawKeeper12);
  const mockHaru = Object.assign({}, haru, { x: CX - 60, y: CY, fx: 1, fy: 0, vx: 0, vy: 0, dash: 0, stun: 0 });
  const mockJin = Object.assign({}, jin, { x: CX + 60, y: CY, fx: -1, fy: 0, vx: 0, vy: 0, dash: 0, stun: 0 });
  drawPlayer12(mockHaru, 0);
  drawPlayer12(mockJin, 0);
  g12.fillStyle = '#012'; g12.fillRect(160 - 2, 90 + 4, 5, 1);
  g12.fillRect(160 - 3, 90 - 3, 6, 6);
  g12.fillStyle = '#fff'; g12.fillRect(160 - 2, 90 - 3, 4, 6); g12.fillRect(160 - 3, 90 - 2, 6, 4);
  g12.fillStyle = '#123';
  g12.fillRect(160 - 1, 90 - 1, 1, 1); g12.fillRect(160 + 1, 90, 1, 1); g12.fillRect(160 - 1, 90 + 1, 1, 1);
  drawHUD12();
  g12.font = '6px "Press Start 2P", monospace';
  g12.fillStyle = '#012'; g12.fillRect(90, LH - 14, 140, 10);
  g12.strokeStyle = '#fe3'; g12.lineWidth = 1; g12.strokeRect(90, LH - 14, 140, 10);
  g12.fillStyle = '#fe3'; g12.textAlign = 'center';
  g12.fillText('PHASE 2 MOCKUP: 320x180', 160, LH - 7);
}

// 12-Bit Automated Palette Check
function checkPalette() {
  const imgData = g12.getImageData(0, 0, LW, LH);
  const data = imgData.data;
  const found = new Set();
  const paletteSet = new Set(PALETTE_32.map(c => c.toLowerCase()));
  let non12bit = 0;
  for (let i = 0; i < data.length; i += 4) {
    const r = data[i], gVal = data[i + 1], b = data[i + 2], a = data[i + 3];
    if (a < 128) continue;
    const r4 = Math.round(r / 17), g4 = Math.round(gVal / 17), b4 = Math.round(b / 17);
    const hex = ('#' + r4.toString(16) + g4.toString(16) + b4.toString(16)).toLowerCase();
    found.add(hex);
    if (r % 17 !== 0 || gVal % 17 !== 0 || b % 17 !== 0) non12bit++;
  }
  const count = found.size;
  const pass = count <= 32;
  const msg = `12-BIT PALETTE: ${count}/32 COLOURS [${pass ? 'PASS' : 'EXCEEDED'}]`;
  console.log(`[Palette Check] ${msg}`);
  console.log(`[Palette Check] Active 12-bit colors (${count}):`, [...found].join(', '));
  addText(CX, CY - 40, msg, pass ? '#fe3' : '#f62');
  return { count, pass, colors: [...found] };
}

// ============================================================================
// MAIN RENDER LOOP & MODE SWITCHING
// ============================================================================
function draw(now) {
  if (engineMode === '32bit') {
    // 32-Bit TrueColor Direct Rendering (960x540)
    vg.setTransform(cv.width / W, 0, 0, cv.height / H, 0, 0);
    vg.save();
    if (shakeT > 0 && !reduced) { const a = shakeT * 18; vg.translate((Math.random() - .5) * a, (Math.random() - .5) * a); }
    vg.drawImage(bg32, 0, 0, W, H);
    keepers.forEach(drawKeeper32);
    const ents = [...players].sort((a, b) => a.y - b.y);
    ents.forEach(p => drawPlayer32(p, now));
    drawParts32();
    drawBall32(now);
    if (ov.aim) drawAim32(ov.aim.p);
    drawTexts32();
    vg.restore();
    if (ov.vs) drawVs32(ov.vs, now);
    drawHUD32();
    if (ov.clash) drawClash32(ov.clash, now);
    if (ov.banner) drawBanner32(ov.banner, now);
    if (ov.cut) drawCut32(ov.cut, now);
  } else {
    // 12-Bit Amiga Pipeline Rendering (320x180 scaled to cv)
    if (mockMode) {
      renderMockFrame();
    } else {
      g12.setTransform(1, 0, 0, 1, 0, 0);
      g12.clearRect(0, 0, LW, LH);
      g12.save();
      if (shakeT > 0 && !reduced) {
        const s = Math.min(3, Math.max(1, Math.round(shakeT * 3)));
        const sx = (Math.random() < 0.5 ? -1 : 1) * Math.floor(Math.random() * s + 0.5);
        const sy = (Math.random() < 0.5 ? -1 : 1) * Math.floor(Math.random() * s + 0.5);
        g12.translate(sx, sy);
      }
      g12.drawImage(bg12, 0, 0, LW, LH);
      keepers.forEach(drawKeeper12);
      const ents = [...players].sort((a, b) => a.y - b.y);
      ents.forEach(p => drawPlayer12(p, now));
      drawBall12(now);
      drawTexts32();
      g12.restore();
      drawHUD12();
      if (ov.banner) {
        g12.fillStyle = '#012'; g12.fillRect(0, 68, LW, 46);
        g12.strokeStyle = '#235'; g12.lineWidth = 1; g12.strokeRect(0, 68, LW, 46);
        g12.font = '14px "Press Start 2P", monospace'; g12.textAlign = 'center'; g12.fillStyle = ov.banner.color;
        g12.fillText(ov.banner.text, 160, 90);
        g12.font = '7px "Press Start 2P", monospace'; g12.fillStyle = '#def';
        g12.fillText(ov.banner.sub, 160, 106);
      }
    }
    vg.imageSmoothingEnabled = false;
    vg.drawImage(lowCv, 0, 0, cv.width, cv.height);
  }
}

let last = performance.now();
function frame(now) {
  const dt = Math.min(0.05, (now - last) / 1000); last = now;
  if (!mockMode || engineMode === '32bit') {
    update(dt);
    for (const t of texts) t.t += dt; texts = texts.filter(t => t.t < t.life);
    updateParts(dt);
    shakeT = Math.max(0, shakeT - dt);
  }
  draw(now);
  requestAnimationFrame(frame);
}

function resize() {
  const r = stage.getBoundingClientRect();
  if (engineMode === '32bit') {
    const dpr = Math.min(2, window.devicePixelRatio || 1);
    const w = Math.max(320, Math.round(r.width * dpr));
    cv.width = w; cv.height = Math.round(w * 9 / 16);
    cv.style.width = '100%'; cv.style.height = '100%';
    vg.imageSmoothingEnabled = true;
  } else {
    const scale = Math.max(1, Math.floor(Math.min(r.width / LW, r.height / LH)));
    const dpr = Math.max(1, Math.floor(window.devicePixelRatio || 1));
    cv.width = LW * scale * dpr; cv.height = LH * scale * dpr;
    cv.style.width = (LW * scale) + 'px'; cv.style.height = (LH * scale) + 'px';
    vg.imageSmoothingEnabled = false;
    g12.imageSmoothingEnabled = false;
  }
}

function setEngineMode(m) {
  engineMode = m;
  const is32 = m === '32bit';
  document.body.classList.toggle('mode-12bit', !is32);
  $('modeBtn').textContent = is32 ? 'Mode: 32-Bit Arcade' : 'Mode: 12-Bit Amiga';
  $('modeBtn').style.color = is32 ? 'var(--tension)' : 'var(--flame)';
  $('modeBtn').style.borderColor = is32 ? 'var(--tension)' : 'var(--flame)';
  $('palBtn').style.display = is32 ? 'none' : 'inline-block';
  $('mockBtn').style.display = is32 ? 'inline-block' : 'none';
  $('kickerTag').textContent = is32 ? '32-Bit Arcade Edition · 1v1 duel prototype' : '12-Bit Amiga Retro Edition · 1v1 duel prototype';
  resize();
  paintPortraits();
  addText(CX, CY - 30, is32 ? '32-BIT ARCADE TRUECOLOR' : '12-BIT AMIGA RETRO', is32 ? '#35d6c0' : '#ffe14d');
}

// ---------- input ----------
const MOVE_KEYS = ['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'KeyW', 'KeyA', 'KeyS', 'KeyD'];
window.addEventListener('keydown', e => {
  const c = e.code;
  if (c === 'KeyT') { e.preventDefault(); setEngineMode(engineMode === '32bit' ? '12bit' : '32bit'); return; }
  if (c === 'KeyP' && engineMode === '12bit') { e.preventDefault(); checkPalette(); return; }
  if (c === 'KeyM' && engineMode === '12bit') { e.preventDefault(); mockMode = !mockMode; $('mockBtn').textContent = mockMode ? 'Mock: ON [M]' : 'Mock: 320x180 [M]'; return; }
  if (menuResolve) {
    const mm = /^(?:Digit|Numpad)([1-9])$/.exec(c);
    if (mm) { const o = menuOpts[+mm[1] - 1]; if (o && o.tp <= menuP.tp + 1e-6) { e.preventDefault(); closeMenu(o); } return; }
    if (c === 'Escape' && menuCancel) { e.preventDefault(); closeMenu(null); return; }
    if (c.startsWith('Arrow')) {
      e.preventDefault();
      const bs = [...cmdList.querySelectorAll('button:not(:disabled)')]; if (!bs.length) return;
      let i = bs.indexOf(document.activeElement);
      i = (c === 'ArrowUp' || c === 'ArrowLeft') ? (i <= 0 ? bs.length - 1 : i - 1) : (i + 1) % bs.length;
      bs[i].focus(); return;
    }
    if (MOVE_KEYS.includes(c)) keys.add(c);
    return;
  }
  const inGame = mode === 'play' || mode === 'freeze';
  if (!inGame) { if (mode === 'title' && c === 'Enter' && document.activeElement === stage) { e.preventDefault(); startMatch(); } return; }
  if (e.target && e.target.closest && e.target.closest('button') && (c === 'Space' || c === 'Enter')) return;
  if (skipFn && (c === 'Space' || c === 'Enter' || c === 'KeyJ')) { e.preventDefault(); skipFn(); return; }
  if (MOVE_KEYS.includes(c)) { keys.add(c); e.preventDefault(); }
  if (c === 'Space' || c === 'KeyJ') { e.preventDefault(); if (mode === 'play' && !e.repeat) actionPressed = true; }
});
window.addEventListener('keyup', e => keys.delete(e.code));
window.addEventListener('blur', () => keys.clear());
stage.addEventListener('pointerdown', e => { if (e.target.closest('button')) return; initAudio(); if (skipFn) skipFn(); });
$('startBtn').addEventListener('click', () => startMatch());
$('againBtn').addEventListener('click', () => startMatch());
$('restartBtn').addEventListener('click', () => { startMatch(); });
$('modeBtn').addEventListener('click', () => setEngineMode(engineMode === '32bit' ? '12bit' : '32bit'));
$('palBtn').addEventListener('click', () => checkPalette());
$('mockBtn').addEventListener('click', () => { mockMode = !mockMode; $('mockBtn').textContent = mockMode ? 'Mock: ON [M]' : 'Mock: 320x180 [M]'; });
$('muteBtn').addEventListener('click', e => { muted = !muted; e.currentTarget.textContent = muted ? 'Sound: off' : 'Sound: on'; e.currentTarget.setAttribute('aria-pressed', String(muted)); if (mode === 'play' || mode === 'freeze') stage.focus({ preventScroll: true }); });

const stick = $('stick'), knob = $('knob'); let stickId = null;
function moveStick(e) {
  const r = stick.getBoundingClientRect(); let dx = e.clientX - (r.left + r.width / 2), dy = e.clientY - (r.top + r.height / 2);
  const max = r.width / 2 - 20, d = Math.hypot(dx, dy); if (d > max) { dx *= max / d; dy *= max / d; }
  knob.style.transform = `translate(${dx}px,${dy}px)`; joy = { x: dx / max, y: dy / max };
  if (Math.hypot(joy.x, joy.y) < 0.15) joy = { x: 0, y: 0 };
}
stick.addEventListener('pointerdown', e => { e.preventDefault(); try { stick.setPointerCapture(e.pointerId); } catch (_) {} stickId = e.pointerId; initAudio(); moveStick(e); });
stick.addEventListener('pointermove', e => { if (e.pointerId === stickId) moveStick(e); });
const endStick = e => { if (e.pointerId !== stickId) return; stickId = null; joy = { x: 0, y: 0 }; knob.style.transform = ''; };
stick.addEventListener('pointerup', endStick); stick.addEventListener('pointercancel', endStick);
$('actBtn').addEventListener('pointerdown', e => {
  e.preventDefault(); initAudio();
  if (skipFn) { skipFn(); return; }
  if (mode === 'title') { startMatch(); return; }
  if (mode === 'play') actionPressed = true;
});

// ---------- roster cards ----------
function renderCards() {
  $('roster').innerHTML = [HARU, JIN].map(ch => {
    const st = [['Kick', ch.stats.kick], ['Dribble', ch.stats.dribble], ['Block', ch.stats.block], ['Speed', ch.stats.speed]];
    return `<article class="card">
      <header class="c-head"><canvas class="pf" width="168" height="168" data-p="${ch.id}" aria-hidden="true"></canvas>
        <div><p class="c-team">${ch.team} · No. ${ch.num} · ${ch.role}</p><h3>${ch.name}</h3><span class="chip ${ch.elem}">${ELEM[ch.elem].name}</span></div></header>
      <p class="c-bio">${ch.bio}</p>
      <dl class="stats">${st.map(([k, v]) => `<dt>${k}</dt><dd class="bar"><i style="width:${v}%;background:${ELEM[ch.elem].c}"></i></dd><dd class="val">${v}</dd>`).join('')}</dl>
      <div class="tbl"><table class="moves"><thead><tr><th>Special move</th><th>Use</th><th>Element</th><th class="n">PWR</th><th class="n">TP</th></tr></thead>
      <tbody>${ch.moves.map(m => `<tr><td>${m.name}</td><td>${KIND[m.kind]}</td><td><span class="chip ${m.elem}">${ELEM[m.elem].name}</span></td><td class="n">${m.power}</td><td class="n">${m.tp}</td></tr>`).join('')}</tbody></table></div>
    </article>`;
  }).join('');
  paintPortraits();
}
function paintPortraits() {
  document.querySelectorAll('canvas.pf').forEach(cn => {
    const ch = cn.dataset.p === 'haru' ? HARU : JIN, c = cn.getContext('2d'), E = ELEM[ch.elem];
    c.setTransform(1, 0, 0, 1, 0, 0);
    if (engineMode === '32bit') {
      const gr = c.createLinearGradient(0, 0, 168, 168); gr.addColorStop(0, E.c); gr.addColorStop(1, E.d);
      c.fillStyle = gr; c.fillRect(0, 0, 168, 168);
      c.fillStyle = 'rgba(255,255,255,.14)';
      for (let i = 0; i < 16; i++) { const a = i / 16 * Math.PI * 2; c.beginPath(); c.moveTo(84, 60); c.lineTo(84 + Math.cos(a - 0.05) * 200, 60 + Math.sin(a - 0.05) * 200); c.lineTo(84 + Math.cos(a + 0.05) * 200, 60 + Math.sin(a + 0.05) * 200); c.closePath(); c.fill(); }
      bust(c, ch, 84, 150, 0.95);
    } else {
      c.imageSmoothingEnabled = false;
      c.fillStyle = E.d12; c.fillRect(0, 0, cn.width, cn.height);
      c.fillStyle = E.c12;
      for (let i = 0; i < 16; i++) {
        const a = i / 16 * Math.PI * 2;
        c.beginPath(); c.moveTo(cn.width / 2, Math.round(cn.height * 0.35));
        c.lineTo(cn.width / 2 + Math.round(Math.cos(a - 0.05) * 120), Math.round(cn.height * 0.35 + Math.sin(a - 0.05) * 120));
        c.lineTo(cn.width / 2 + Math.round(Math.cos(a + 0.05) * 120), Math.round(cn.height * 0.35 + Math.sin(a + 0.05) * 120));
        c.closePath(); c.fill();
      }
      bust(c, ch, cn.width / 2, Math.round(cn.height * 0.88), cn.width / 180);
    }
  });
}

// ---------- boot ----------
function start(data) {
  drawStatic32();
  drawStatic12();
  renderCards();
  resize();
  new ResizeObserver(resize).observe(stage);
  placeKickoff(0);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(paintPortraits);
  if (data && data.inMatch && Array.isArray(data.score)) startMatch({ score: data.score });
  requestAnimationFrame(t => { last = t; frame(t); });
}
try { window.claude?.hot?.snapshot?.(() => ({ score: score.slice(), inMatch: mode === 'play' || mode === 'freeze' })); } catch (e) {}
if (window.claude?.hot?.ready) window.claude.hot.ready(start); else start(window.claude?.hot?.data ?? {});
"""

text = text[:idx_script_start] + js_code + text[idx_script_end + len("})();\n</script>"):]

with open(r"c:\SESHU\PROJECTS\OTHER PROJECTS\FOOTBALL\Blaze vs Bedrock.html", "w", encoding="utf-8") as f:
    f.write(text)

print("SUCCESS: 32-bit Arcade & 12-bit Amiga dual-engine built and saved!")
