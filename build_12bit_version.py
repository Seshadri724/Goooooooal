import re

with open(r"c:\SESHU\PROJECTS\OTHER PROJECTS\FOOTBALL\Blaze vs Bedrock.backup.html", "r", encoding="utf-8") as f:
    text = f.read()

# 1. Update font link
text = text.replace(
    '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Dela+Gothic+One&family=Zen+Kaku+Gothic+New:wght@400;500;700&family=Azeret+Mono:wght@500;700&display=swap">',
    '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Press+Start+2P&family=Dela+Gothic+One&family=Zen+Kaku+Gothic+New:wght@400;500;700&family=Azeret+Mono:wght@500;700&display=swap">'
)

# 2. Update CSS in :root
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
  --night:#012; --panel:#123; --panel2:#124; --line:#235; --ink:#def; --mute:#89a;
  --tension:#fe3; --flame:#f62; --gale:#3db; --stone:#b83; --basic:#89a;
  --display:"Press Start 2P","Dela Gothic One",sans-serif;
  --body:"Zen Kaku Gothic New",system-ui,-apple-system,"Segoe UI",sans-serif;
  --mono:"Press Start 2P","Azeret Mono",ui-monospace,monospace;
}"""
assert css_root_old in text, "css_root_old not found"
text = text.replace(css_root_old, css_root_new)

# 3. Update .stage, .stage canvas, .screen, .btn
old_stage_block = """.btn{font:500 12px/1 var(--mono);letter-spacing:.04em;color:var(--ink);background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:10px 12px;cursor:pointer;}
.btn:hover{border-color:var(--mute)}
button:focus-visible,.stage:focus-visible{outline:2px solid var(--tension);outline-offset:2px}
.stage-wrap{position:relative}
.stage{position:relative;width:100%;max-width:100%;aspect-ratio:16/9;border-radius:12px;overflow:hidden;background:#0a0f1d;box-shadow:0 0 0 1px var(--line),0 40px 80px -40px rgba(0,0,0,.9);outline:none}
.stage canvas{display:block;width:100%;height:100%}
.screen{position:absolute;inset:0;display:grid;place-items:center;padding:16px;background:radial-gradient(ellipse at center,rgba(8,11,22,.5),rgba(8,11,22,.9));}"""

new_stage_block = """.btn{font:500 10px/1 var(--mono);letter-spacing:.04em;color:var(--ink);background:var(--panel);border:2px solid var(--line);border-radius:0;padding:8px 10px;cursor:pointer;}
.btn:hover{border-color:var(--tension)}
button:focus-visible,.stage:focus-visible{outline:2px solid var(--tension);outline-offset:2px}
.stage-wrap{position:relative}
.stage{position:relative;width:100%;max-width:100%;aspect-ratio:16/9;border-radius:0;overflow:hidden;background:#000;box-shadow:0 0 0 2px var(--line);outline:none;display:flex;align-items:center;justify-content:center}
.stage canvas{display:block;image-rendering:-moz-crisp-edges;image-rendering:-webkit-crisp-edges;image-rendering:pixelated;image-rendering:crisp-edges;}
.screen{position:absolute;inset:0;display:grid;place-items:center;padding:16px;background:rgba(0,17,34,.94);border:2px solid var(--line);}"""
assert old_stage_block in text, "old_stage_block not found"
text = text.replace(old_stage_block, new_stage_block)

# 4. Update primary button and cmd blur
old_cmd_block = """.primary{font-family:var(--display);font-size:18px;color:#1d1600;background:var(--tension);border:0;border-radius:6px;padding:13px 30px;cursor:pointer;transform:skewX(-10deg);box-shadow:0 6px 0 #b39a1f;transition:transform .12s, box-shadow .12s;}
.primary span{display:inline-block;transform:skewX(10deg)}
.primary:hover{transform:skewX(-10deg) translateY(-2px);box-shadow:0 8px 0 #b39a1f}
.primary:active{transform:skewX(-10deg) translateY(3px);box-shadow:0 3px 0 #b39a1f}
@media (max-width:620px){ .lede,.keys{display:none} .screen-card{gap:8px} .primary{font-size:15px;padding:10px 22px} .screen h2{font-size:30px} }
.cmd{margin-top:10px;background:rgba(12,17,33,.96);border:1px solid var(--line);border-radius:12px;padding:12px;display:grid;gap:10px;}
@media (min-width:760px){ .cmd{position:absolute;left:14px;right:14px;bottom:14px;margin:0;backdrop-filter:blur(6px);} }
.cmd-head{display:flex;flex-wrap:wrap;align-items:baseline;gap:4px 12px}
.cmd-head strong{font-family:var(--display);font-weight:400;font-size:17px;letter-spacing:.02em}
.cmd-head span{color:var(--mute);font-size:13px}
.cmd-list{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:8px}
.mv{display:grid;grid-template-columns:auto 1fr auto;align-items:center;gap:6px 10px;text-align:left;background:var(--panel2);color:var(--ink);border:1px solid var(--line);border-radius:9px;padding:10px 12px;cursor:pointer;font-family:var(--body);transition:border-color .12s,transform .12s,background .12s}
.mv:hover:not(:disabled),.mv:focus-visible{border-color:var(--tension);transform:translateY(-1px);background:#202c52;outline:none}
.mv:disabled{opacity:.42;cursor:not-allowed}
.mv .k{font:700 11px/1 var(--mono);color:var(--night);background:var(--mute);border-radius:4px;padding:4px 6px}
.mv .nm{font-weight:700;font-size:14.5px;line-height:1.25}
.mv .tp{font:700 12px/1 var(--mono);color:var(--tension);font-variant-numeric:tabular-nums;white-space:nowrap}
.mv .meta{grid-column:2 / 4;display:flex;flex-wrap:wrap;align-items:center;gap:4px 8px;font:500 11px/1.4 var(--mono);color:var(--mute)}
.mv.ghost{grid-template-columns:auto 1fr;background:transparent}
.chip{display:inline-block;font:700 10.5px/1 var(--mono);letter-spacing:.08em;text-transform:uppercase;border:1px solid currentColor;border-radius:4px;padding:3px 6px}
.chip.flame{color:var(--flame)} .chip.gale{color:var(--gale)} .chip.stone{color:var(--stone)} .chip.none{color:var(--basic)}
.touchpad{display:none}
@media (pointer:coarse){ .touchpad{display:flex;justify-content:space-between;align-items:center;gap:16px;margin-top:12px;user-select:none;-webkit-user-select:none} }
.stick{position:relative;width:136px;height:136px;border-radius:50%;border:2px solid var(--line);background:radial-gradient(circle,#18223f,#0f1629);touch-action:none;flex:none}
.knob{position:absolute;left:50%;top:50%;width:56px;height:56px;margin:-28px 0 0 -28px;border-radius:50%;background:var(--panel2);border:2px solid var(--mute);pointer-events:none}
.act{width:112px;height:112px;border-radius:50%;border:0;background:var(--flame);color:#fff;font-family:var(--display);font-size:18px;touch-action:none;display:grid;place-content:center;gap:2px;box-shadow:0 6px 0 #9b2a14;flex:none}
.act small{font:500 10px/1.2 var(--mono);opacity:.9}
.pad-note{font:500 11px/1.5 var(--mono);color:var(--mute);text-align:center;margin:0}

.roster{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,320px),1fr));gap:16px}
.card{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:18px;display:grid;gap:14px;align-content:start}
.c-head{display:flex;gap:14px;align-items:center}
.pf{width:84px;height:84px;border-radius:10px;flex:none}"""

new_cmd_block = """.primary{font-family:var(--display);font-size:12px;color:#123;background:var(--tension);border:0;border-radius:0;padding:12px 24px;cursor:pointer;box-shadow:0 4px 0 #971;transition:none;}
.primary span{display:inline-block;transform:none}
.primary:hover{transform:translateY(-2px);box-shadow:0 6px 0 #971}
.primary:active{transform:translateY(2px);box-shadow:0 2px 0 #971}
@media (max-width:620px){ .lede,.keys{display:none} .screen-card{gap:8px} .primary{font-size:10px;padding:10px 18px} .screen h2{font-size:22px} }
.cmd{margin-top:10px;background:var(--panel);border:2px solid var(--line);border-radius:0;padding:12px;display:grid;gap:10px;}
@media (min-width:760px){ .cmd{position:absolute;left:14px;right:14px;bottom:14px;margin:0;} }
.cmd-head{display:flex;flex-wrap:wrap;align-items:baseline;gap:4px 12px}
.cmd-head strong{font-family:var(--display);font-weight:400;font-size:13px;letter-spacing:.02em}
.cmd-head span{color:var(--mute);font-size:11px}
.cmd-list{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:8px}
.mv{display:grid;grid-template-columns:auto 1fr auto;align-items:center;gap:6px 10px;text-align:left;background:var(--panel2);color:var(--ink);border:2px solid var(--line);border-radius:0;padding:10px 12px;cursor:pointer;font-family:var(--body);transition:border-color .12s,background .12s}
.mv:hover:not(:disabled),.mv:focus-visible{border-color:var(--tension);background:#1a2542;outline:none}
.mv:disabled{opacity:.42;cursor:not-allowed}
.mv .k{font:700 9px/1 var(--mono);color:var(--night);background:var(--mute);border-radius:0;padding:4px 6px}
.mv .nm{font-weight:700;font-size:13px;line-height:1.25}
.mv .tp{font:700 10px/1 var(--mono);color:var(--tension);font-variant-numeric:tabular-nums;white-space:nowrap}
.mv .meta{grid-column:2 / 4;display:flex;flex-wrap:wrap;align-items:center;gap:4px 8px;font:500 9px/1.4 var(--mono);color:var(--mute)}
.mv.ghost{grid-template-columns:auto 1fr;background:transparent}
.chip{display:inline-block;font:700 9px/1 var(--mono);letter-spacing:.08em;text-transform:uppercase;border:1px solid currentColor;border-radius:0;padding:3px 6px}
.chip.flame{color:var(--flame)} .chip.gale{color:var(--gale)} .chip.stone{color:var(--stone)} .chip.none{color:var(--basic)}
.touchpad{display:none}
@media (pointer:coarse){ .touchpad{display:flex;justify-content:space-between;align-items:center;gap:16px;margin-top:12px;user-select:none;-webkit-user-select:none} }
.stick{position:relative;width:120px;height:120px;border-radius:0;border:2px solid var(--line);background:#012;touch-action:none;flex:none}
.knob{position:absolute;left:50%;top:50%;width:48px;height:48px;margin:-24px 0 0 -24px;border-radius:0;background:var(--panel2);border:2px solid var(--mute);pointer-events:none}
.act{width:96px;height:96px;border-radius:0;border:2px solid var(--line);background:var(--flame);color:#fff;font-family:var(--display);font-size:11px;touch-action:none;display:grid;place-content:center;gap:2px;box-shadow:0 4px 0 #921;flex:none}
.act small{font:500 8px/1.2 var(--mono);opacity:.9}
.pad-note{font:500 9px/1.5 var(--mono);color:var(--mute);text-align:center;margin:0}

.roster{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,320px),1fr));gap:16px}
.card{background:var(--panel);border:2px solid var(--line);border-radius:0;padding:18px;display:grid;gap:14px;align-content:start}
.c-head{display:flex;gap:14px;align-items:center}
.pf{width:84px;height:84px;border-radius:0;border:2px solid var(--line);image-rendering:pixelated;flex:none}"""
assert old_cmd_block in text, "old_cmd_block not found"
text = text.replace(old_cmd_block, new_cmd_block)

# 5. Header buttons (Palette check and Mockup toggle)
old_tools = """    <div class="tools">
      <button type="button" class="btn" id="muteBtn" aria-pressed="false">Sound: on</button>
      <button type="button" class="btn" id="restartBtn">Restart match</button>
    </div>"""

new_tools = """    <div class="tools">
      <button type="button" class="btn" id="muteBtn" aria-pressed="false">Sound: on</button>
      <button type="button" class="btn" id="restartBtn">Restart match</button>
      <button type="button" class="btn" id="palBtn">Palette: 32c [P]</button>
      <button type="button" class="btn" id="mockBtn">Mock: 320x180 [M]</button>
    </div>"""
assert old_tools in text, "old_tools not found"
text = text.replace(old_tools, new_tools)

# 6. JavaScript setup (lines 193-264)
old_js_setup = """(() => {
'use strict';
const W = 960, H = 540;
const F = { x0: 60, y0: 62, x1: 900, y1: 506 };
const CX = (F.x0 + F.x1) / 2, CY = (F.y0 + F.y1) / 2;
const GY0 = CY - 60, GY1 = CY + 60;
const GOALS_TO_WIN = 3;
const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;

const ELEM = {
  flame: { name: 'Flame', c: '#ff5a36', g: '#ffc163', d: '#3a0d08' },
  gale:  { name: 'Gale',  c: '#35d6c0', g: '#c9fff6', d: '#062a2a' },
  stone: { name: 'Stone', c: '#e0a93f', g: '#fff1c9', d: '#2b1d07' },
  none:  { name: 'Basic', c: '#9aa6b8', g: '#ffffff', d: '#141a2a' },
};
const BEATS = { flame: 'gale', gale: 'stone', stone: 'flame' };
const KIND = { shot: 'Shot', dribble: 'Dribble', block: 'Block' };
const BASIC = {
  shot:    { name: 'Power Shot',   kind: 'shot',    elem: 'none', power: 18, tp: 0 },
  dribble: { name: 'Push Through', kind: 'dribble', elem: 'none', power: 15, tp: 0 },
  block:   { name: 'Tackle',       kind: 'block',   elem: 'none', power: 15, tp: 0 },
};
const HARU = {
  id: 'haru', name: 'Nuem', short: 'NUEM', team: 'Akebono FC', role: 'Striker', elem: 'flame', num: 9,
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
  id: 'jin', name: 'Some', short: 'SOME', team: 'Tetsuzan Academy', role: 'Libero', elem: 'stone', num: 5,
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

// ---------- DOM ----------
const $ = id => document.getElementById(id);
const stage = $('stage'), cv = $('cv'), g = cv.getContext('2d');
const titleScreen = $('titleScreen'), overScreen = $('overScreen');
const cmd = $('cmd'), cmdTitle = $('cmdTitle'), cmdSub = $('cmdSub'), cmdList = $('cmdList');

// ---------- state ----------
function mkPlayer(ch, team, human) { return { ch, team, human, x: 0, y: 0, vx: 0, vy: 0, fx: team === 0 ? 1 : -1, fy: 0, stun: 0, tp: 60, dash: 0, dashCd: 0 }; }
const haru = mkPlayer(HARU, 0, true), jin = mkPlayer(JIN, 1, false);
const players = [haru, jin];
const keepers = [
  { team: 0, name: 'AKEBONO GK', x: F.x0 + 14, y: CY, rating: 60, color: '#7fd18b', dive: 0, dd: 1 },
  { team: 1, name: 'TETSUZAN GK', x: F.x1 - 14, y: CY, rating: 60, color: '#8b7bff', dive: 0, dd: 1 },
];"""

new_js_setup = """(() => {
'use strict';
// 12-Bit Amiga Pipeline Constants:
// Internal resolution: 320x180 (16:9, exactly 1/3 of 960x540 game space).
// Game logic coordinates remain untouched in 960x540, divided by 3 only during rendering.
const LW = 320, LH = 180;
const W = 960, H = 540;
const F = { x0: 60, y0: 62, x1: 900, y1: 506 };
const CX = (F.x0 + F.x1) / 2, CY = (F.y0 + F.y1) / 2;
const GY0 = CY - 60, GY1 = CY + 60;
const GOALS_TO_WIN = 3;
const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;

// 32-Colour 12-Bit Master Palette (#RGB format, 4 bits per channel)
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

const ELEM = {
  flame: { name: 'Flame', c: '#f62', g: '#fa4', d: '#410' },
  gale:  { name: 'Gale',  c: '#3db', g: '#bfd', d: '#033' },
  stone: { name: 'Stone', c: '#b83', g: '#ec7', d: '#320' },
  none:  { name: 'Basic', c: '#89a', g: '#fff', d: '#123' },
};
const BEATS = { flame: 'gale', gale: 'stone', stone: 'flame' };
const KIND = { shot: 'Shot', dribble: 'Dribble', block: 'Block' };
const BASIC = {
  shot:    { name: 'Power Shot',   kind: 'shot',    elem: 'none', power: 18, tp: 0 },
  dribble: { name: 'Push Through', kind: 'dribble', elem: 'none', power: 15, tp: 0 },
  block:   { name: 'Tackle',       kind: 'block',   elem: 'none', power: 15, tp: 0 },
};
const HARU = {
  id: 'haru', name: 'Nuem', short: 'NUEM', team: 'Akebono FC', role: 'Striker', elem: 'flame', num: 9,
  jersey: '#def', trim: '#e42', hair: '#c22', hairHi: '#f75', brow: '#611', skin: '#fba', eye: '#fb3',
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
  id: 'jin', name: 'Some', short: 'SOME', team: 'Tetsuzan Academy', role: 'Libero', elem: 'stone', num: 5,
  jersey: '#233', trim: '#b83', hair: '#789', hairHi: '#cdf', brow: '#456', skin: '#eb9', eye: '#e92',
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

// ---------- DOM & 12-Bit Canvas Surface ----------
const $ = id => document.getElementById(id);
const stage = $('stage'), cv = $('cv'), vg = cv.getContext('2d');
// Low-resolution drawing surface: 320x180 offscreen canvas
const lowCv = document.createElement('canvas');
lowCv.width = LW; lowCv.height = LH;
const g = lowCv.getContext('2d', { willReadFrequently: true });
g.imageSmoothingEnabled = false;
vg.imageSmoothingEnabled = false;

const titleScreen = $('titleScreen'), overScreen = $('overScreen');
const cmd = $('cmd'), cmdTitle = $('cmdTitle'), cmdSub = $('cmdSub'), cmdList = $('cmdList');

// ---------- state ----------
function mkPlayer(ch, team, human) { return { ch, team, human, x: 0, y: 0, vx: 0, vy: 0, fx: team === 0 ? 1 : -1, fy: 0, stun: 0, tp: 60, dash: 0, dashCd: 0 }; }
const haru = mkPlayer(HARU, 0, true), jin = mkPlayer(JIN, 1, false);
const players = [haru, jin];
const keepers = [
  { team: 0, name: 'AKEBONO GK', x: F.x0 + 14, y: CY, rating: 60, color: '#4b6', dive: 0, dd: 1 },
  { team: 1, name: 'TETSUZAN GK', x: F.x1 - 14, y: CY, rating: 60, color: '#76d', dive: 0, dd: 1 },
];"""
assert old_js_setup in text, "old_js_setup not found"
text = text.replace(old_js_setup, new_js_setup)

# 7. Update sfx to chiptune (square & triangle waves with shorter envelopes)
old_sfx = """    switch (k) {
      case 'kick': tone('sine', 180, 50, .14, .5); noise(.05, .25, 2500); break;
      case 'touch': tone('sine', 240, 120, .06, .15); break;
      case 'whistle': tone('square', 2300, 2150, .16, .045); tone('square', 2300, 2150, .3, .045, .2); break;
      case 'blip': tone('triangle', 700, 0, .05, .1); break;
      case 'charge': tone('sawtooth', 110, 880, 1.15, .045); break;
      case 'impact': tone('sine', 95, 32, .55, .6); noise(.45, .45, 900); break;
      case 'clash': noise(.18, .25, 3200); tone('square', 320, 150, .14, .06); break;
      case 'goal': [523, 659, 784, 1047].forEach((f, i) => tone('triangle', f, 0, .32, .13, i * .09)); noise(1.2, .07, 1400, .1); break;
      case 'catch': tone('sine', 150, 90, .1, .35); break;
      case 'dash': noise(.12, .12, 1800); break;
    }"""

new_sfx = """    switch (k) {
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
    }"""
assert old_sfx in text, "old_sfx not found"
text = text.replace(old_sfx, new_sfx)

# 8. Particle colors in 12-bit hex
old_emit = """    else if (s.elem === 'flame') { const v = 60 + Math.random() * 110; Object.assign(p, { kind: 'ember', color: ['#ffd28a', '#ff9a3c', '#ff5a36'][Math.floor(Math.random() * 3)], size: 2 + Math.random() * 3, life: .35 + Math.random() * .3, vx: bx * v + px * sv * 70, vy: by * v + py * sv * 70, rise: -40 }); }
    else if (s.elem === 'gale') Object.assign(p, { kind: 'wisp', color: '#c9fff6', size: 2, life: .3 + Math.random() * .25, vx: bx * 140 + px * sv * 150, vy: by * 140 + py * sv * 150, drag: 2 });
    else if (Math.random() < .45) Object.assign(p, { kind: 'rock', color: Math.random() < .5 ? '#c98f2c' : '#8a5f1a', size: 1.8 + Math.random() * 2.6, life: .5 + Math.random() * .35, vx: bx * 70 + px * sv * 110, vy: by * 70 + py * sv * 110, drag: 4 });
    else Object.assign(p, { kind: 'dust', color: '#e8cf9a', size: 3 + Math.random() * 4, life: .45, vx: bx * 40 + px * sv * 40, vy: by * 40 + py * sv * 40 });"""

new_emit = """    else if (s.elem === 'flame') { const v = 60 + Math.random() * 110; Object.assign(p, { kind: 'ember', color: ['#fa4', '#f62', '#f21'][Math.floor(Math.random() * 3)], size: 2 + Math.random() * 3, life: .35 + Math.random() * .3, vx: bx * v + px * sv * 70, vy: by * v + py * sv * 70, rise: -40 }); }
    else if (s.elem === 'gale') Object.assign(p, { kind: 'wisp', color: '#bfd', size: 2, life: .3 + Math.random() * .25, vx: bx * 140 + px * sv * 150, vy: by * 140 + py * sv * 150, drag: 2 });
    else if (Math.random() < .45) Object.assign(p, { kind: 'rock', color: Math.random() < .5 ? '#b83' : '#641', size: 1.8 + Math.random() * 2.6, life: .5 + Math.random() * .35, vx: bx * 70 + px * sv * 110, vy: by * 70 + py * sv * 110, drag: 4 });
    else Object.assign(p, { kind: 'dust', color: '#ec7', size: 3 + Math.random() * 4, life: .45, vx: bx * 40 + px * sv * 40, vy: by * 40 + py * sv * 40 });"""
assert old_emit in text, "old_emit not found"
text = text.replace(old_emit, new_emit)

# 9. Complete Drawing Pipeline replacement: from `// ---------- static pitch ----------` to `// ---------- input ----------`
idx_start = text.find("// ---------- static pitch ----------")
idx_end = text.find("// ---------- input ----------")
assert idx_start != -1 and idx_end != -1, "Drawing block not found"

new_drawing_pipeline = """// ---------- static pitch (320x180 whole-pixel surface, no smooth effects) ----------
const bg = document.createElement('canvas'); bg.width = LW; bg.height = LH;
function drawStatic() {
  const c = bg.getContext('2d');
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
  // ad boards
  for (let i = 0; i < 24; i++) {
    c.fillStyle = i % 2 ? '#c32' : '#942';
    c.fillRect(fx0 + i * 12, fy0 - 4, 11, 2);
    c.fillRect(fx0 + i * 12, fy1 + 2, 11, 2);
  }
  // grass stripes (two-tone 12-bit green bands, zero radial gradients)
  const n = 14, sw = (fx1 - fx0) / n;
  for (let i = 0; i < n; i++) {
    const x = Math.round(fx0 + i * sw), w = Math.round(fx0 + (i + 1) * sw) - x;
    c.fillStyle = i % 2 ? '#173' : '#152';
    c.fillRect(x, fy0, w, fy1 - fy0);
  }
  // nets (flat color grid)
  for (const side of [0, 1]) {
    const nx = side === 0 ? fx0 - 9 : fx1;
    c.fillStyle = '#123'; c.fillRect(nx, gy0, 9, gy1 - gy0);
    c.fillStyle = '#235';
    for (let yy = gy0; yy <= gy1; yy += 3) c.fillRect(nx, yy, 9, 1);
    for (let xx = nx; xx <= nx + 9; xx += 3) c.fillRect(xx, gy0, 1, gy1 - gy0);
    c.strokeStyle = '#def'; c.lineWidth = 1; c.strokeRect(nx, gy0, 9, gy1 - gy0);
  }
  // pitch lines (1px crisp lines)
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

// ---------- characters (bust art in 12-bit whole-pixel) ----------
function eye(c, ch, ex, ey, right) {
  c.save(); c.translate(ex, ey); if (!right) c.scale(-1, 1);
  c.beginPath(); c.moveTo(-8, 2); c.quadraticCurveTo(0, -7, 11, -3); c.quadraticCurveTo(4, 5, -8, 2); c.closePath();
  c.fillStyle = '#fff'; c.fill();
  c.save(); c.clip();
  c.beginPath(); c.arc(1.5, -1, 5, 0, Math.PI * 2); c.fillStyle = ch.eye; c.fill();
  c.beginPath(); c.arc(1.5, -1, 2.4, 0, Math.PI * 2); c.fillStyle = '#012'; c.fill();
  c.beginPath(); c.arc(3.2, -3, 1.3, 0, Math.PI * 2); c.fillStyle = '#fff'; c.fill();
  c.restore();
  c.beginPath(); c.moveTo(-9, 2); c.quadraticCurveTo(0, -8, 12, -3.5); c.lineWidth = 2.4; c.strokeStyle = '#012'; c.stroke();
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
  const sil = o.sil || null, O = '#012';
  const fill = col => { c.fillStyle = sil || col; };
  c.save(); c.translate(Math.round(x), Math.round(y)); c.scale(o.flip ? -s : s, s);
  c.lineJoin = 'miter'; c.lineCap = 'square'; c.lineWidth = 2.5; c.strokeStyle = sil || O;
  c.beginPath(); c.moveTo(-100, 140); c.lineTo(-92, 62); c.quadraticCurveTo(-84, 18, -38, 8); c.lineTo(38, 8); c.quadraticCurveTo(84, 18, 92, 62); c.lineTo(100, 140); c.closePath();
  fill(ch.jersey); c.fill(); c.stroke();
  if (!sil) {
    c.fillStyle = ch.trim;
    c.beginPath(); c.moveTo(-28, 8); c.lineTo(0, 42); c.lineTo(28, 8); c.lineTo(17, 8); c.lineTo(0, 27); c.lineTo(-17, 8); c.closePath(); c.fill();
    for (const sd of [-1, 1]) { c.beginPath(); c.moveTo(sd * 92, 64); c.quadraticCurveTo(sd * 84, 22, sd * 46, 11); c.lineTo(sd * 42, 21); c.quadraticCurveTo(sd * 72, 32, sd * 79, 66); c.closePath(); c.fill(); }
    c.save(); if (o.flip) c.scale(-1, 1);
    c.font = '28px "Press Start 2P", monospace'; c.textAlign = 'center'; c.textBaseline = 'alphabetic'; c.fillStyle = ch.trim;
    c.fillText(String(ch.num), o.flip ? -48 : 48, 106); c.restore();
  }
  c.beginPath(); c.rect(-13, -28, 26, 38); fill(ch.skin); c.fill(); c.stroke();
  if (!sil) { c.fillStyle = '#611'; c.beginPath(); c.moveTo(-13, -22); c.quadraticCurveTo(0, -8, 13, -22); c.lineTo(13, -10); c.quadraticCurveTo(0, 0, -13, -10); c.closePath(); c.fill(); }
  for (const sd of [-1, 1]) { c.beginPath(); c.ellipse(sd * 33, -56, 6, 10, 0, 0, Math.PI * 2); fill(ch.skin); c.fill(); c.stroke(); }
  c.beginPath(); c.moveTo(-33, -80); c.quadraticCurveTo(-35, -42, -19, -26); c.quadraticCurveTo(0, -10, 19, -26); c.quadraticCurveTo(35, -42, 33, -80); c.quadraticCurveTo(0, -114, -33, -80); c.closePath();
  fill(ch.skin); c.fill(); c.stroke();
  if (!sil) {
    eye(c, ch, -14, -57, false); eye(c, ch, 14, -57, true);
    c.strokeStyle = '#611'; c.lineWidth = 1.8; c.beginPath(); c.moveTo(1, -50); c.lineTo(-2, -41); c.lineTo(3, -41); c.stroke();
    c.strokeStyle = O; c.lineWidth = 2.4; c.beginPath(); c.moveTo(-8, -32); c.quadraticCurveTo(1, -29, 9, -34); c.stroke();
  }
  c.lineWidth = 2.5; c.strokeStyle = sil || O;
  hair(c, ch, sil);
  c.restore();
}

// ---------- field drawing (Whole-pixel 320x180) ----------
function rr(x, y, w, h, r) { g.beginPath(); g.moveTo(x + r, y); g.arcTo(x + w, y, x + w, y + h, r); g.arcTo(x + w, y + h, x, y + h, r); g.arcTo(x, y + h, x, y, r); g.arcTo(x, y, x + w, y, r); g.closePath(); }
function circle(x, y, r) { g.beginPath(); g.arc(x, y, r, 0, Math.PI * 2); }

function drawPlayer(p, now) {
  const ch = p.ch, moving = Math.hypot(p.vx, p.vy) > 20;
  const bob = moving ? (Math.floor(now / 110) % 2) : 0;
  const rx = Math.round(p.x / 3);
  const ry = Math.round(p.y / 3) + bob;
  // 1-pixel shadow
  g.fillStyle = '#012';
  g.fillRect(rx - 4, ry + 4, 9, 2);
  // Human indicator
  if (p.human) {
    g.fillStyle = '#fe3';
    g.fillRect(rx - 1, ry - 14, 3, 2);
    g.fillRect(rx, ry - 12, 1, 1);
  }
  // Dash ghost
  if (p.dash > 0) {
    const gx = Math.round((p.x - p.vx * 0.04) / 3), gy = Math.round((p.y - p.vy * 0.04) / 3);
    g.fillStyle = ELEM[ch.elem].c;
    circle(gx, gy, 4); g.fill();
  }
  // Body (radius 4.5, diameter 9)
  g.lineWidth = 1; g.strokeStyle = '#012';
  g.fillStyle = ch.jersey; circle(rx, ry, 4.5); g.fill(); g.stroke();
  g.fillStyle = ch.trim; g.fillRect(rx - 1, ry + 1, 2, 2);
  // Head & Hair
  const hx = rx + Math.round(p.fx * 1.5), hy = ry - 3 + Math.round(p.fy * 0.8);
  g.fillStyle = ch.hair;
  const back = Math.atan2(-p.fy, -p.fx);
  const spikes = ch.id === 'haru' ? 5 : 3;
  for (let i = 0; i < spikes; i++) {
    const a = back + (i - (spikes - 1) / 2) * (ch.id === 'haru' ? 0.5 : 0.7);
    const len = ch.id === 'haru' ? 5 : 4.5;
    g.beginPath();
    g.moveTo(hx + Math.round(Math.cos(a - 0.35) * 2.5), hy + Math.round(Math.sin(a - 0.35) * 2.5));
    g.lineTo(hx + Math.round(Math.cos(a) * len), hy + Math.round(Math.sin(a) * len));
    g.lineTo(hx + Math.round(Math.cos(a + 0.35) * 2.5), hy + Math.round(Math.sin(a + 0.35) * 2.5));
    g.closePath(); g.fill(); g.stroke();
  }
  circle(hx, hy, 3); g.fill(); g.stroke();
  g.save(); circle(hx, hy, 3); g.clip();
  g.fillStyle = ch.skin; circle(hx + Math.round(p.fx * 1.5), hy + Math.round(p.fy + 1), 2); g.fill();
  g.restore();
  // Overhead name tag in pixel font
  g.font = '6px "Press Start 2P", monospace';
  g.textAlign = 'center'; g.textBaseline = 'middle';
  g.fillStyle = '#012'; g.fillRect(rx - 11, ry - 10, 22, 6);
  g.strokeStyle = '#235'; g.strokeRect(rx - 11, ry - 10, 22, 6);
  g.fillStyle = p.human ? '#fe3' : ELEM[ch.elem].c;
  g.fillText(ch.short, rx, ry - 7);
  // Stun stars orbiting in whole pixels
  if (p.stun > 0) {
    g.fillStyle = '#fe3';
    for (let i = 0; i < 3; i++) {
      const a = now / 150 + i * 2.094;
      const sx = hx + Math.round(Math.cos(a) * 5), sy = hy - 4 + Math.round(Math.sin(a) * 2);
      g.fillRect(sx, sy, 1, 1);
    }
  }
  g.textBaseline = 'alphabetic';
}

function drawKeeper(k) {
  const d = k.dive > 0 ? Math.sin(clamp((0.6 - k.dive) / 0.2, 0, 1) * Math.PI / 2) : 0;
  const rx = Math.round(k.x / 3);
  const ry = Math.round((k.y + k.dd * d * 14) / 3);
  g.fillStyle = '#012'; g.fillRect(rx - 4, ry + 4, 9, 2);
  g.save(); g.translate(rx, ry);
  g.rotate(k.dd * d * 0.9 * (k.team === 0 ? 1 : -1));
  g.lineWidth = 1; g.strokeStyle = '#012';
  g.fillStyle = k.color;
  g.beginPath(); g.ellipse(0, 0, 4, 4.5, 0, 0, Math.PI * 2); g.fill(); g.stroke();
  g.fillStyle = '#fff';
  const gx = k.team === 0 ? 3 : -3;
  circle(gx, -4 - Math.round(d * 2), 1.5); g.fill(); g.stroke();
  circle(gx, 4 + Math.round(d * 2), 1.5); g.fill(); g.stroke();
  g.fillStyle = '#123'; circle(0, -2, 2.5); g.fill(); g.stroke();
  g.restore();
}

function rock(x, y, sz, rot, col) {
  g.save(); g.translate(Math.round(x), Math.round(y)); g.rotate(rot);
  g.fillStyle = col; g.fillRect(-sz, -sz, sz * 2, sz * 2);
  g.strokeStyle = '#320'; g.lineWidth = 1; g.strokeRect(-sz, -sz, sz * 2, sz * 2);
  g.restore();
}

function drawShotFx(s, now) {
  const E = ELEM[s.elem], special = s.move.tp > 0;
  const bx = Math.round(ball.x / 3), by = Math.round(ball.y / 3);
  // Stepped trail dots in palette colors
  for (let i = 0; i < trail.length; i++) {
    const tx = Math.round(trail[i].x / 3), ty = Math.round(trail[i].y / 3);
    g.fillStyle = special ? (i % 2 === 0 ? E.c : E.g) : '#fff';
    g.fillRect(tx, ty, 1, 1);
  }
  if (!special) return;
  // Flat stepped aura rings (no radial gradient!)
  g.strokeStyle = E.g; g.lineWidth = 1;
  circle(bx, by, 6); g.stroke();
  g.strokeStyle = E.c;
  circle(bx, by, 9); g.stroke();
  if (s.elem === 'flame') {
    g.fillStyle = '#f62';
    for (let i = 0; i < 4; i++) {
      const a = now / 70 + i * 1.57;
      g.fillRect(bx + Math.round(Math.cos(a) * 8), by + Math.round(Math.sin(a) * 8), 2, 2);
    }
  } else if (s.elem === 'gale') {
    g.strokeStyle = '#bfd'; g.lineWidth = 1;
    for (let i = 0; i < 2; i++) {
      g.beginPath();
      g.arc(bx, by, 8 + i * 3, now / 60 + i * Math.PI, now / 60 + i * Math.PI + 1.6);
      g.stroke();
    }
  } else if (s.elem === 'stone') {
    g.fillStyle = '#b83';
    for (let i = 0; i < 3; i++) {
      const a = now / 90 + i * 2.094;
      g.fillRect(bx + Math.round(Math.cos(a) * 7) - 1, by + Math.round(Math.sin(a) * 7) - 1, 2, 2);
    }
  }
}

function drawParts() {
  g.save();
  for (const p of parts) {
    const rx = Math.round(p.x / 3);
    const ry = Math.round(p.y / 3);
    const sz = p.size >= 4 ? 2 : 1;
    g.fillStyle = p.color;
    g.fillRect(rx, ry, sz, sz);
  }
  for (const r of rings) {
    const rx = Math.round(r.x / 3);
    const ry = Math.round(r.y / 3);
    const rad = Math.max(1, Math.round((4 + r.r1 * easeOut(r.t / r.life)) / 3));
    g.strokeStyle = r.color; g.lineWidth = 1;
    g.strokeRect(rx - rad, ry - rad, rad * 2, rad * 2);
  }
  g.restore();
}

function drawBall(now) {
  const s = ball.shot, special = !!(s && s.move.tp > 0), E = s ? ELEM[s.elem] : ELEM.none;
  if (s) drawShotFx(s, now);
  const bx = Math.round(ball.x / 3), by = Math.round(ball.y / 3);
  // 1-pixel shadow underneath
  g.fillStyle = '#012';
  g.fillRect(bx - 2, by + 4, 5, 1);
  // 6x6 chunky ball
  const body = !special ? '#fff' : (s.elem === 'flame' ? '#fa4' : (s.elem === 'gale' ? '#bfd' : (s.elem === 'stone' ? '#ec7' : '#fff')));
  g.fillStyle = '#012';
  g.fillRect(bx - 3, by - 3, 6, 6);
  g.fillStyle = body;
  g.fillRect(bx - 2, by - 3, 4, 6);
  g.fillRect(bx - 3, by - 2, 6, 4);
  // Spinning dots
  g.fillStyle = special ? E.c : '#123';
  for (let i = 0; i < 3; i++) {
    const a = ball.spin + i * 2.094;
    g.fillRect(bx + Math.round(Math.cos(a) * 1.5), by + Math.round(Math.sin(a) * 1.5), 1, 1);
  }
  // Overhead shot banner
  if (s) {
    const txt = special ? `${s.move.name.toUpperCase()} ${Math.round(s.power)}` : `SHOT ${Math.round(s.power)}`;
    g.font = '6px "Press Start 2P", monospace';
    const tw = g.measureText(txt).width;
    const lx = clamp(bx, 20 + tw / 2, LW - 20 - tw / 2), ly = Math.max(14, by - 9);
    g.fillStyle = '#012'; g.fillRect(lx - tw / 2 - 2, ly - 4, tw + 4, 8);
    g.strokeStyle = '#235'; g.lineWidth = 1; g.strokeRect(lx - tw / 2 - 2, ly - 4, tw + 4, 8);
    g.fillStyle = special ? E.c : '#def';
    g.textAlign = 'center'; g.textBaseline = 'middle';
    g.fillText(txt, lx, ly);
    g.textBaseline = 'alphabetic';
  }
}

function drawTexts() {
  g.textAlign = 'center';
  g.font = '8px "Press Start 2P", monospace';
  for (const t of texts) {
    const tx = Math.round(t.x / 3);
    const ty = Math.round((t.y - t.t * 22) / 3);
    g.fillStyle = '#012';
    g.fillText(t.text, tx + 1, ty + 1);
    g.fillStyle = t.color;
    g.fillText(t.text, tx, ty);
  }
}

function tpBar(p, x, y, right) {
  const w = 60, h = 5, x0 = right ? x - w : x;
  g.font = '6px "Press Start 2P", monospace';
  g.textAlign = right ? 'right' : 'left';
  g.textBaseline = 'alphabetic';
  g.fillStyle = '#89a';
  g.fillText(`TP ${Math.floor(p.tp)}`, x, y + 5);
  g.fillStyle = '#123';
  g.fillRect(x0, y + 7, w, h);
  g.strokeStyle = '#235'; g.lineWidth = 1;
  g.strokeRect(x0, y + 7, w, h);
  const numSegs = 12;
  const activeSegs = Math.floor((p.tp / p.ch.maxTP) * numSegs);
  for (let i = 0; i < numSegs; i++) {
    if (i < activeSegs) {
      g.fillStyle = '#fe3';
      const sx = right ? (x - (i + 1) * 5) : (x0 + i * 5);
      g.fillRect(sx + 1, y + 8, 4, h - 2);
    }
  }
  g.fillStyle = '#456';
  for (const m of p.ch.moves) {
    const tx = Math.round(right ? (x - w * m.tp / p.ch.maxTP) : (x0 + w * m.tp / p.ch.maxTP));
    g.fillRect(tx, y + 6, 1, h + 2);
  }
}

function drawHUD() {
  const w = 92, h = 15, x = 160 - w / 2, y = 3;
  g.fillStyle = '#012'; g.fillRect(x, y, w, h);
  g.strokeStyle = '#235'; g.lineWidth = 1; g.strokeRect(x, y, w, h);
  g.fillStyle = HARU.trim; g.fillRect(x + 3, y + 3, 2, 9);
  g.fillStyle = JIN.trim; g.fillRect(x + w - 5, y + 3, 2, 9);
  g.textBaseline = 'middle';
  g.font = '7px "Press Start 2P", monospace';
  g.fillStyle = '#def';
  g.textAlign = 'left'; g.fillText('H', x + 8, y + h / 2);
  g.textAlign = 'right'; g.fillText('J', x + w - 8, y + h / 2);
  g.textAlign = 'center';
  g.fillStyle = '#fe3';
  g.fillText(`${score[0]}-${score[1]}`, 160, y + h / 2);
  g.textBaseline = 'alphabetic';
  tpBar(haru, 6, 2, false);
  tpBar(jin, LW - 6, 2, true);
}

function drawAim(p) {
  const gx = p.team === 0 ? Math.round(F.x1 / 3) : Math.round(F.x0 / 3);
  const bx = Math.round(ball.x / 3), by = Math.round(ball.y / 3);
  const cy = Math.round(CY / 3), gy0 = Math.round(GY0 / 3), gy1 = Math.round(GY1 / 3);
  g.save();
  g.strokeStyle = '#fe3'; g.lineWidth = 1;
  g.setLineDash([3, 3]);
  g.beginPath(); g.moveTo(bx, by); g.lineTo(gx, cy); g.stroke();
  g.setLineDash([]);
  g.lineWidth = 2;
  g.beginPath(); g.moveTo(gx, gy0); g.lineTo(gx, gy1); g.stroke();
  g.restore();
}

// ---------- overlays (320x180 whole-pixel) ----------
function drawVs(v, now) {
  const t = (now - v.t0) / 1000, k = easeOut(clamp(t / 0.3, 0, 1));
  g.fillStyle = '#012'; g.fillRect(0, 0, LW, LH);
  const L = players[0], R = players[1];
  g.save();
  // Solid diagonal panels in element colors (no linear gradients!)
  g.fillStyle = ELEM[L.ch.elem].d;
  g.beginPath(); g.moveTo(0, 0); g.lineTo(175, 0); g.lineTo(145, LH); g.lineTo(0, LH); g.closePath(); g.fill();
  g.fillStyle = ELEM[R.ch.elem].d;
  g.beginPath(); g.moveTo(175, 0); g.lineTo(LW, 0); g.lineTo(LW, LH); g.lineTo(145, LH); g.closePath(); g.fill();
  g.strokeStyle = '#def'; g.lineWidth = 1;
  g.beginPath(); g.moveTo(175, 0); g.lineTo(145, LH); g.stroke();
  g.restore();
  bust(g, L.ch, Math.round(lerp(-50, 75, k)), 115, 0.35);
  bust(g, R.ch, Math.round(lerp(LW + 50, 245, k)), 115, 0.35, { flip: true });
  g.font = '8px "Press Start 2P", monospace'; g.textAlign = 'center';
  g.fillStyle = '#fe3'; g.fillText(v.label, 160, 24);
  g.font = '24px "Press Start 2P", monospace';
  g.fillStyle = '#012'; g.fillText('VS', 160 + 1, 80 + 1);
  g.fillStyle = '#fff'; g.fillText('VS', 160, 80);
  g.font = '8px "Press Start 2P", monospace';
  g.textAlign = 'left'; g.fillStyle = '#fff'; g.fillText(L.ch.name, 12, 38);
  g.textAlign = 'right'; g.fillStyle = '#fff'; g.fillText(R.ch.name, LW - 12, 38);
  g.font = '6px "Press Start 2P", monospace';
  g.textAlign = 'left'; g.fillStyle = ELEM[L.ch.elem].c; g.fillText(`${ELEM[L.ch.elem].name} TP ${Math.floor(L.tp)}`, 12, 48);
  g.textAlign = 'right'; g.fillStyle = ELEM[R.ch.elem].c; g.fillText(`TP ${Math.floor(R.tp)} ${ELEM[R.ch.elem].name}`, LW - 12, 48);
}

function para(x0, x1, y, h, sk) { g.beginPath(); g.moveTo(x0 + sk, y - h / 2); g.lineTo(x1 + sk, y - h / 2); g.lineTo(x1 - sk, y + h / 2); g.lineTo(x0 - sk, y + h / 2); g.closePath(); }
function drawClash(c, now) {
  const t = (now - c.t0) / 1000, [L, R] = c.sides;
  g.fillStyle = '#012'; g.fillRect(0, 0, LW, LH);
  const grow = easeOut(clamp(t / 0.5, 0, 1)), push = easeOut(clamp((t - 0.5) / 0.45, 0, 1));
  const tot = (L.score + R.score) || 1, split = 160 + ((L.score - R.score) / tot) * 230 * push;
  const y = 94, h = 16, x0 = 30, x1 = 290;
  const le = lerp(x0, split, grow), re = lerp(x1, split, grow);
  g.font = '8px "Press Start 2P", monospace'; g.textAlign = 'center'; g.fillStyle = '#fe3';
  g.fillText(c.title, 160, 48);
  g.fillStyle = L.color; para(x0, le, y, h, 3); g.fill();
  g.fillStyle = R.color; para(re, x1, y, h, 3); g.fill();
  g.strokeStyle = '#012'; g.lineWidth = 1; para(x0, le, y, h, 3); g.stroke(); para(re, x1, y, h, 3); g.stroke();
  if (grow >= 0.99) {
    g.fillStyle = '#fff';
    for (let i = 0; i < 8; i++) {
      const a = i / 8 * Math.PI * 2 + t * 3, r = 8 + sr(i + Math.floor(t * 12)) * 10;
      g.fillRect(Math.round(split + Math.cos(a) * r), Math.round(y + Math.sin(a) * r), 2, 2);
    }
  }
  g.font = '10px "Press Start 2P", monospace';
  g.fillStyle = '#fff';
  g.textAlign = 'left'; g.fillText(String(Math.round(L.score * grow)), x0 + 4, y + 4);
  g.textAlign = 'right'; g.fillText(String(Math.round(R.score * grow)), x1 - 4, y + 4);
  g.font = '8px "Press Start 2P", monospace';
  g.textAlign = 'left'; g.fillText(L.name, x0, y - 14);
  g.textAlign = 'right'; g.fillText(R.name, x1, y - 14);
  g.font = '6px "Press Start 2P", monospace';
  g.textAlign = 'left'; g.fillStyle = L.color; g.fillText(`${L.move.name} (${ELEM[L.move.elem].name})`, x0, y + 18);
  g.textAlign = 'right'; g.fillStyle = R.color; g.fillText(`${R.move.name} (${ELEM[R.move.elem].name})`, x1, y + 18);
  if (t > 0.95) {
    const win = c.winTeam === 0 ? L : R;
    g.font = '12px "Press Start 2P", monospace'; g.textAlign = 'center';
    g.fillStyle = '#012'; g.fillText(c.verdict, 160 + 1, 136 + 1);
    g.fillStyle = win.color; g.fillText(c.verdict, 160, 136);
  }
}

function drawBanner(b, now) {
  const t = (now - b.t0) / 1000, D = b.dur / 1000;
  const k = easeBack(clamp(t / 0.3, 0, 1)), out = t > D - 0.25 ? clamp((t - (D - 0.25)) / 0.25, 0, 1) : 0;
  g.save();
  g.fillStyle = '#012';
  g.fillRect(0, 68, LW, 46);
  g.strokeStyle = '#235'; g.lineWidth = 1;
  g.strokeRect(0, 68, LW, 46);
  g.save(); g.translate(160, 88); g.scale(k, k);
  g.font = `${b.big ? 18 : 12}px "Press Start 2P", monospace`;
  g.textAlign = 'center'; g.textBaseline = 'middle';
  g.fillStyle = '#012'; g.fillText(b.text, 1, 1);
  g.fillStyle = b.color; g.fillText(b.text, 0, 0);
  g.restore();
  g.font = '7px "Press Start 2P", monospace'; g.textAlign = 'center'; g.textBaseline = 'alphabetic'; g.fillStyle = '#def';
  g.fillText(b.sub, 160, 106);
  g.restore();
}

function bigBall(x, y, r, E, white) {
  g.fillStyle = white ? '#fff' : E.g;
  g.beginPath(); circle(x, y, r); g.fill();
  g.strokeStyle = '#012'; g.lineWidth = 1; g.stroke();
  if (!white) {
    g.save(); circle(x, y, r); g.clip();
    g.fillStyle = '#123';
    for (let i = 0; i < 3; i++) {
      const a = performance.now() / 60 + i * 2.094;
      circle(x + Math.round(Math.cos(a) * r * 0.6), y + Math.round(Math.sin(a) * r * 0.6), r * 0.32);
      g.fill();
    }
    g.restore();
  }
}

function fxBack(el, t, ts, fr, cx, cy) {
  if (el === 'flame') {
    const cols = ['#f21', '#f62', '#fa4'];
    for (let L = 0; L < 3; L++) {
      const R = 64 - L * 15, n = 12; g.beginPath();
      for (let i = 0; i <= n * 2; i++) {
        const a = -Math.PI / 2 + (i / (n * 2)) * Math.PI * 2;
        const sp = i % 2 === 0 ? R + 16 + Math.sin(ts * 9 + i * 1.7 + L) * 10 : R * 0.8;
        const x = cx + Math.round(Math.cos(a) * sp * 0.9), y = cy - 24 + Math.round(Math.sin(a) * sp * 1.15);
        i ? g.lineTo(x, y) : g.moveTo(x, y);
      }
      g.closePath(); g.fillStyle = cols[L]; g.fill();
    }
    g.fillStyle = '#fa4';
    for (let i = 0; i < 20; i++) {
      const x = Math.round(sr(i * 3.1) * LW), y = LH - Math.round(((t * 120 + sr(i * 9.7) * LH) % LH));
      g.fillRect(x, y, 2, 2);
    }
  } else if (el === 'gale') {
    g.strokeStyle = '#bfd'; g.lineWidth = 1;
    for (let i = 0; i < 3; i++) {
      g.save(); g.translate(cx, cy - 20); g.rotate(ts * 2.2 + i * 1.2); g.scale(1, 0.4);
      g.beginPath(); g.arc(0, 0, 50 + i * 10, 0.2, 0.2 + Math.PI * 1.2); g.stroke(); g.restore();
    }
    g.fillStyle = '#3db';
    for (let i = 0; i < 15; i++) {
      const y = Math.round(sr(i * 4.4) * LH), x = Math.round(((t * 500 + sr(i + 3) * 400) % (LW + 100)) - 50);
      g.fillRect(x, y, 8, 1);
    }
  } else if (el === 'stone') {
    g.fillStyle = '#641';
    for (let i = 0; i < 6; i++) {
      const a = i / 6 * Math.PI * 2 + ts * 0.9, r = 70 + sr(i) * 20;
      const x = cx + Math.round(Math.cos(a) * r), y = cy - 20 + Math.round(Math.sin(a) * r * 0.55);
      g.fillRect(x - 4, y - 4, 8, 8);
    }
  }
}

function fxTrail(el, sx, sy, x, y, t) {
  const n = 8;
  for (let i = 1; i < n; i++) {
    const u = i / n, px = Math.round(lerp(sx, x, u)), py = Math.round(lerp(sy, y, u));
    g.fillStyle = el === 'flame' ? (i % 2 ? '#fa4' : '#f21') : (el === 'gale' ? '#3db' : '#b83');
    g.fillRect(px - 1, py - 1, 3, 3);
  }
}

function barrier(el, u, t, fr) {
  if (el === 'flame') {
    g.fillStyle = '#f62';
    for (let i = 0; i < 8; i++) {
      const x = 200 + i * 8, hh = Math.round(u * (120 + sr(i + fr) * 30));
      g.fillRect(x, LH - hh, 6, hh);
    }
  } else if (el === 'gale') {
    g.strokeStyle = '#3db'; g.lineWidth = 2;
    for (let i = 0; i < 4; i++) {
      circle(230, 100, Math.round(20 + i * 8 * u)); g.stroke();
    }
  } else if (el === 'stone') {
    const top = LH - Math.round(u * 150);
    g.fillStyle = '#b83';
    g.fillRect(200, top, 60, LH - top);
    g.strokeStyle = '#320'; g.lineWidth = 1;
    g.strokeRect(200, top, 60, LH - top);
    // crack lines
    g.beginPath();
    g.moveTo(220, top + 10); g.lineTo(230, top + 40); g.lineTo(225, top + 70);
    g.moveTo(230, top + 40); g.lineTo(245, top + 55);
    g.stroke();
  }
}

function drawCut(o, now) {
  const t = (now - o.t0) / 1000, D = o.dur / 1000, fr = Math.floor(t * 12), ts = fr / 12;
  const m = o.m, E = ELEM[m.elem], ch = o.p.ch;
  const impact = !reduced && t >= 1.22 && t < 1.36;
  if (!o.boom && t >= 1.22) { o.boom = true; sfx('impact'); }
  g.save();
  // Screen shake on cut
  if (!reduced && t > 1.36 && t < 1.8) {
    const a = Math.round((1.8 - t) * 6);
    g.translate((sr(fr * 3.3) > 0.5 ? 1 : -1) * (a % 3), (sr(fr * 7.1) > 0.5 ? 1 : -1) * (a % 3));
  }
  // Background
  g.fillStyle = impact ? '#fff' : E.d;
  g.fillRect(0, 0, LW, LH);
  // Speed lines
  if (!impact) {
    g.fillStyle = E.c;
    for (let i = 0; i < 18; i++) {
      const y = (i * 10 + fr * 13) % LH;
      const len = 30 + ((i * 37) % 90);
      const x = ((fr * 47 + i * 83) % (LW + 80)) - 40;
      g.fillRect(x, y, len, 1);
    }
  }
  const slide = easeBack(clamp(ts / 0.42, 0, 1));
  let bx = Math.round(-90 + slide * 175); const by = Math.round(112 + Math.sin(ts * 5) * 2);
  const fin = clamp((t - 1.36) / 0.5, 0, 1);
  if (!impact) fxBack(m.elem, t, ts, fr, bx, by);
  if (m.kind === 'dribble' && t >= 1.36) {
    const e = easeOut(fin);
    for (let i = 3; i >= 1; i--) {
      bust(g, ch, bx + Math.round(e * 250 - i * 26), by, 0.7, { sil: E.c });
    }
    bx += Math.round(e * 250);
  }
  bust(g, ch, bx, by, 0.7, { sil: impact ? '#000' : null });
  // Shot ball
  if (m.kind === 'shot' && t < 1.36) {
    bigBall(187, 126, 8, E, impact);
  }
  if (t >= 1.36) {
    if (m.kind === 'shot') {
      const e = fin * fin, sx = 187, sy = 126, x = Math.round(lerp(sx, 380, e)), y = Math.round(lerp(sy, 60, e));
      g.strokeStyle = E.c; g.lineWidth = 14;
      g.beginPath(); g.moveTo(sx - 20, sy + 6); g.lineTo(x, y); g.stroke();
      fxTrail(m.elem, sx, sy, x, y, t);
      bigBall(x, y, 8, E, false);
    } else if (m.kind === 'block') {
      barrier(m.elem, easeOut(fin), t, fr);
    }
  }
  // Move title banner
  if (t > 0.3) {
    g.font = '10px "Press Start 2P", monospace'; g.textAlign = 'center';
    g.fillStyle = '#012'; g.fillText(m.name, 213 + 1, 46 + 1);
    g.fillStyle = impact ? '#000' : '#fff'; g.fillText(m.name, 213, 46);
    g.font = '6px "Press Start 2P", monospace';
    g.fillStyle = E.g; g.fillText(`${ch.name.toUpperCase()} · ${E.name.toUpperCase()} ${KIND[m.kind].toUpperCase()}`, 213, 64);
  }
  // Letterbox borders
  const lb = Math.min(1, t / 0.16) * 18;
  g.fillStyle = '#012'; g.fillRect(0, 0, LW, lb); g.fillRect(0, LH - lb, LW, lb);
  if (lb >= 18) {
    g.strokeStyle = E.c; g.lineWidth = 1;
    g.beginPath(); g.moveTo(0, 18); g.lineTo(LW, 18); g.moveTo(0, LH - 18); g.lineTo(LW, LH - 18); g.stroke();
    g.font = '6px "Press Start 2P", monospace'; g.textBaseline = 'middle';
    g.textAlign = 'left'; g.fillStyle = E.c; g.fillText(`${KIND[m.kind].toUpperCase()} · PWR ${m.power} · ${m.tp} TP`, 8, LH - 9);
    g.textAlign = 'right'; g.fillStyle = '#89a'; g.fillText('Space: skip', LW - 8, LH - 9);
    g.textBaseline = 'alphabetic';
  }
  g.restore();
}

// ---------- render loop (320x180 low-res pipeline) ----------
let mockMode = false;
function draw(now) {
  if (mockMode) {
    renderMockFrame();
    vg.imageSmoothingEnabled = false;
    vg.drawImage(lowCv, 0, 0, cv.width, cv.height);
    return;
  }
  g.setTransform(1, 0, 0, 1, 0, 0);
  g.clearRect(0, 0, LW, LH);
  g.save();
  // Screen shake in whole pixels: 1-3 pixels at a time, never fractions
  if (shakeT > 0 && !reduced) {
    const s = Math.min(3, Math.max(1, Math.round(shakeT * 3)));
    const sx = (Math.random() < 0.5 ? -1 : 1) * Math.floor(Math.random() * s + 0.5);
    const sy = (Math.random() < 0.5 ? -1 : 1) * Math.floor(Math.random() * s + 0.5);
    g.translate(sx, sy);
  }
  g.drawImage(bg, 0, 0, LW, LH);
  keepers.forEach(drawKeeper);
  const ents = [...players].sort((a, b) => a.y - b.y);
  ents.forEach(p => drawPlayer(p, now));
  drawParts();
  drawBall(now);
  if (ov.aim) drawAim(ov.aim.p);
  drawTexts();
  g.restore();
  if (ov.vs) drawVs(ov.vs, now);
  drawHUD();
  if (ov.clash) drawClash(ov.clash, now);
  if (ov.banner) drawBanner(ov.banner, now);
  if (ov.cut) drawCut(ov.cut, now);

  // Scaled up onto visible canvas cv with crisp pixel scaling
  vg.imageSmoothingEnabled = false;
  vg.drawImage(lowCv, 0, 0, cv.width, cv.height);
}

let last = performance.now();
function frame(now) {
  const dt = Math.min(0.05, (now - last) / 1000); last = now;
  if (!mockMode) {
    update(dt);
    for (const t of texts) t.t += dt; texts = texts.filter(t => t.t < t.life);
    updateParts(dt);
    shakeT = Math.max(0, shakeT - dt);
  }
  draw(now);
  requestAnimationFrame(frame);
}

// Whole-number scaling: only x2, x3, x4, etc., with black bars filling leftover space
function resize() {
  const r = stage.getBoundingClientRect();
  const scale = Math.max(1, Math.floor(Math.min(r.width / LW, r.height / LH)));
  const dpr = Math.max(1, Math.floor(window.devicePixelRatio || 1));
  cv.width = LW * scale * dpr;
  cv.height = LH * scale * dpr;
  cv.style.width = (LW * scale) + 'px';
  cv.style.height = (LH * scale) + 'px';
  vg.imageSmoothingEnabled = false;
  g.imageSmoothingEnabled = false;
}

// Automated 12-Bit Palette Check (Reads back frame, checks <= 32 colors)
function checkPalette() {
  const imgData = g.getImageData(0, 0, LW, LH);
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
  console.log(`[Palette Check] Unique 12-bit colors on screen:`, [...found].join(', '));
  addText(CX, CY - 40, msg, pass ? '#fe3' : '#f62');
  return { count, pass, colors: [...found], non12bit };
}

// Phase 2 Canonical 320x180 Mock Screenshot (pitch, 2 players, ball, HUD)
function renderMockFrame() {
  g.setTransform(1, 0, 0, 1, 0, 0);
  g.drawImage(bg, 0, 0, LW, LH);
  keepers.forEach(drawKeeper);
  const mockHaru = Object.assign({}, haru, { x: CX - 60, y: CY, fx: 1, fy: 0, vx: 0, vy: 0, dash: 0, stun: 0 });
  const mockJin = Object.assign({}, jin, { x: CX + 60, y: CY, fx: -1, fy: 0, vx: 0, vy: 0, dash: 0, stun: 0 });
  drawPlayer(mockHaru, 0);
  drawPlayer(mockJin, 0);
  // 1-pixel shadow underneath ball
  g.fillStyle = '#012'; g.fillRect(160 - 2, 90 + 4, 5, 1);
  // 6x6 ball
  g.fillStyle = '#012'; g.fillRect(160 - 3, 90 - 3, 6, 6);
  g.fillStyle = '#fff'; g.fillRect(160 - 2, 90 - 3, 4, 6); g.fillRect(160 - 3, 90 - 2, 6, 4);
  g.fillStyle = '#123';
  g.fillRect(160 - 1, 90 - 1, 1, 1); g.fillRect(160 + 1, 90, 1, 1); g.fillRect(160 - 1, 90 + 1, 1, 1);
  drawHUD();
  // Phase 2 Mockup banner
  g.font = '6px "Press Start 2P", monospace';
  g.fillStyle = '#012'; g.fillRect(90, LH - 14, 140, 10);
  g.strokeStyle = '#fe3'; g.lineWidth = 1; g.strokeRect(90, LH - 14, 140, 10);
  g.fillStyle = '#fe3'; g.textAlign = 'center';
  g.fillText('PHASE 2 MOCKUP: 320x180', 160, LH - 7);
}

function toggleMock() {
  mockMode = !mockMode;
  $('mockBtn').textContent = mockMode ? 'Mock: ON [M]' : 'Mock: 320x180 [M]';
  $('mockBtn').style.borderColor = mockMode ? 'var(--tension)' : 'var(--line)';
  addText(CX, CY - 20, mockMode ? 'MOCKUP MODE' : 'LIVE MATCH', '#fe3');
}

"""

text = text[:idx_start] + new_drawing_pipeline + text[idx_end:]

# 10. Update key listener for 'KeyP' and 'KeyM'
old_key_check = "if (skipFn && (c === 'Space' || c === 'Enter' || c === 'KeyJ')) { e.preventDefault(); skipFn(); return; }"
new_key_check = """if (c === 'KeyP') { e.preventDefault(); checkPalette(); return; }
  if (c === 'KeyM') { e.preventDefault(); toggleMock(); return; }
  if (skipFn && (c === 'Space' || c === 'Enter' || c === 'KeyJ')) { e.preventDefault(); skipFn(); return; }"""
assert old_key_check in text, "old_key_check not found"
text = text.replace(old_key_check, new_key_check, 1)

# 11. Add event listeners for palBtn and mockBtn
old_btns = "$('restartBtn').addEventListener('click', () => { startMatch(); });"
new_btns = """$('restartBtn').addEventListener('click', () => { startMatch(); });
$('palBtn').addEventListener('click', () => checkPalette());
$('mockBtn').addEventListener('click', () => toggleMock());"""
assert old_btns in text, "old_btns not found"
text = text.replace(old_btns, new_btns)

# 12. Update paintPortraits (remove createLinearGradient, use 12-bit flat / rays)
old_paint_portraits = """function paintPortraits() {
  document.querySelectorAll('canvas.pf').forEach(cn => {
    const ch = cn.dataset.p === 'haru' ? HARU : JIN, c = cn.getContext('2d'), E = ELEM[ch.elem];
    c.setTransform(1, 0, 0, 1, 0, 0);
    const gr = c.createLinearGradient(0, 0, 168, 168); gr.addColorStop(0, E.c); gr.addColorStop(1, E.d);
    c.fillStyle = gr; c.fillRect(0, 0, 168, 168);
    c.fillStyle = 'rgba(255,255,255,.12)';
    for (let i = 0; i < 16; i++) { const a = i / 16 * Math.PI * 2; c.beginPath(); c.moveTo(84, 60); c.lineTo(84 + Math.cos(a - 0.05) * 200, 60 + Math.sin(a - 0.05) * 200); c.lineTo(84 + Math.cos(a + 0.05) * 200, 60 + Math.sin(a + 0.05) * 200); c.closePath(); c.fill(); }
    bust(c, ch, 84, 150, 0.95);
  });
}"""

new_paint_portraits = """function paintPortraits() {
  document.querySelectorAll('canvas.pf').forEach(cn => {
    const ch = cn.dataset.p === 'haru' ? HARU : JIN, c = cn.getContext('2d'), E = ELEM[ch.elem];
    c.imageSmoothingEnabled = false;
    c.setTransform(1, 0, 0, 1, 0, 0);
    c.fillStyle = E.d; c.fillRect(0, 0, cn.width, cn.height);
    c.fillStyle = E.c;
    for (let i = 0; i < 16; i++) {
      const a = i / 16 * Math.PI * 2;
      c.beginPath();
      c.moveTo(cn.width / 2, Math.round(cn.height * 0.35));
      c.lineTo(cn.width / 2 + Math.round(Math.cos(a - 0.05) * 120), Math.round(cn.height * 0.35 + Math.sin(a - 0.05) * 120));
      c.lineTo(cn.width / 2 + Math.round(Math.cos(a + 0.05) * 120), Math.round(cn.height * 0.35 + Math.sin(a + 0.05) * 120));
      c.closePath(); c.fill();
    }
    bust(c, ch, cn.width / 2, Math.round(cn.height * 0.88), cn.width / 180);
  });
}"""
assert old_paint_portraits in text, "old_paint_portraits not found"
text = text.replace(old_paint_portraits, new_paint_portraits)

with open(r"c:\SESHU\PROJECTS\OTHER PROJECTS\FOOTBALL\Blaze vs Bedrock.html", "w", encoding="utf-8") as f:
    f.write(text)

print("Conversion complete! Output written to Blaze vs Bedrock.html")
