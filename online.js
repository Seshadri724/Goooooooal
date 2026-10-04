// Online 1v1 for Blaze vs Bedrock.
// The HOST runs the real game and streams its canvas + audio to the GUEST over WebRTC. The guest sends keys and menu
// picks back and plays the right-hand fighter. The room server (server/) pairs players and relays signaling + input.
(() => {
  const B = window.BVB; if (!B) return;
  const { ON, jin, keepers, cv } = B;
  const $ = id => document.getElementById(id);
  const SERVER = new URLSearchParams(location.search).get('server') ||
    (!location.hostname || /^(localhost|127\.)/.test(location.hostname) ? 'ws://localhost:8080' : 'wss://blaze-duel.fly.dev');
  const ICE = [{ urls: 'stun:stun.l.google.com:19302' }]; // ponytail: STUN only; add a TURN server for the ~10-15% of NATs that block direct links
  const ASK_TIMEOUT = 20000; // a silent guest gets the AI's pick instead of freezing the match

  // Tap the game's audio: everything connects to AC.destination, so hand out a gain node that feeds both the speakers and a stream.
  let tapStream = null;
  const ACP = window.BaseAudioContext ? BaseAudioContext.prototype : AudioContext.prototype; // `destination` lives on the base class
  const destGet = Object.getOwnPropertyDescriptor(ACP, 'destination').get;
  Object.defineProperty(ACP, 'destination', {
    configurable: true,
    get() {
      if (!this._tap) { const g = this.createGain(), s = this.createMediaStreamDestination(); g.connect(destGet.call(this)); g.connect(s); this._tap = g; tapStream = s.stream; }
      return this._tap;
    },
  });

  let ws = null, role = null, pc = null, sigQ = Promise.resolve(), video = null, begun = false, menuId = 0;
  const rin = { x: 0, y: 0, act: false }; // host side: the guest's latest input
  const pending = new Map(); let askId = 0;
  const send = o => { if (ws && ws.readyState === 1) ws.send(JSON.stringify(o)); };
  const clamp1 = v => Math.max(-1, Math.min(1, +v || 0));

  // ---------- lobby dialog ----------
  document.head.insertAdjacentHTML('beforeend', '<style>#onDlg{position:fixed;inset:0;display:none;place-items:center;background:rgba(5,8,18,.82);z-index:60}' +
    '#onDlg .card{background:var(--panel);border:1px solid var(--gale);border-radius:12px;padding:20px;width:min(380px,92vw);text-align:center;color:#eef1f8}' +
    '#onDlg h3{margin:0 0 8px}#onDlg p{margin:8px 0;min-height:2.6em}#onDlg .row{display:flex;gap:8px;justify-content:center;align-items:center;margin:10px 0;flex-wrap:wrap}' +
    '#onCode{width:5.5em;text-align:center;font:700 20px monospace;text-transform:uppercase;padding:6px;border-radius:8px;border:1px solid var(--gale);background:#0a1020;color:#eef1f8}' +
    '#onOver{position:absolute;inset:0;display:grid;place-items:center;text-align:center;background:rgba(5,8,18,.7);color:#eef1f8;z-index:25}' +
    '#onHint{position:absolute;left:0;right:0;bottom:6px;text-align:center;font-size:12px;color:#ffe14d;z-index:22;text-shadow:0 1px 2px #000;pointer-events:none}</style>');
  document.body.insertAdjacentHTML('beforeend', '<div id="onDlg" role="dialog" aria-label="Online 1v1"><div class="card"><h3>Online 1v1</h3><p id="onMsg"></p>' +
    '<div class="row"><button type="button" class="btn" id="onCreate">Create room</button></div>' +
    '<div class="row"><input id="onCode" maxlength="4" placeholder="CODE" aria-label="Room code" autocomplete="off"><button type="button" class="btn" id="onJoin">Join</button></div>' +
    '<button type="button" class="btn" id="onClose">Close</button></div></div>');
  $('startBtn').insertAdjacentHTML('afterend', '<button type="button" class="btn" id="onBtn" style="margin-top:8px">Play online 1v1</button>');

  const setMsg = t => { $('onMsg').textContent = t; };
  const showDlg = on => { $('onDlg').style.display = on ? 'grid' : 'none'; };
  const lobbyBusy = on => { for (const id of ['onCreate', 'onJoin', 'onCode']) $(id).disabled = on; };
  const ERR = { 'no-room': 'No room with that code.', 'room-full': 'That room already has two players.', full: 'Server is full, try again soon.' };

  $('onBtn').onclick = () => { setMsg('Create a room and share the code, or enter a friend’s code. You play the left fighter as host; your friend plays the right one.'); lobbyBusy(false); showDlg(true); };
  $('onClose').onclick = () => { teardown(''); showDlg(false); $('startBtn').focus({ preventScroll: true }); };
  $('onCreate').onclick = () => start('create');
  $('onJoin').onclick = () => { const c = $('onCode').value.trim().toUpperCase(); if (c.length === 4) start('join', c); else setMsg('Enter the 4-letter code.'); };

  function start(kind, code) {
    B.initAudio(); lobbyBusy(true); setMsg('Connecting to server…');
    ws = new WebSocket(SERVER);
    ws.onopen = () => send(kind === 'create' ? { t: 'create' } : { t: 'join', code });
    ws.onerror = () => { teardown('Cannot reach the game server.'); };
    ws.onmessage = e => { let m; try { m = JSON.parse(e.data); } catch { return; } onMsg(m); };
    ws.onclose = () => { if (role || ws) teardown('Connection to the server was lost.'); };
  }

  function onMsg(m) {
    switch (m.t) {
      case 'created': setMsg(`Room ${m.code}. Share this code with your friend, then wait here.`); break;
      case 'error': teardown(ERR[m.e] || 'Server error.'); break;
      case 'ready': role = m.role; if (role === 'host') hostStart(); else guestStart(); break;
      case 'sig': sigQ = sigQ.then(() => handleSig(m.d)).catch(e => console.warn('signaling', e)); break;
      case 'left': teardown(role === 'host' ? 'Opponent left. AI took over.' : 'The host left the match.'); break;
      case 'in': rin.x = clamp1(m.x); rin.y = clamp1(m.y); if (m.act) rin.act = true; break;
      case 'pick': { const e = pending.get(m.id), o = e && e.opts[m.i]; if (o && o.tp <= e.p.tp + 1e-6) e.done(o); break; }
      case 'menu': showMenu(m); break;
      case 'over': showOver(m.title, m.sub); break;
      case 'again': $('onOver')?.remove(); break;
    }
  }

  async function handleSig(d) {
    if (!pc || !d) return;
    if (d.sdp) {
      await pc.setRemoteDescription(d.sdp);
      if (d.sdp.type === 'offer') { await pc.setLocalDescription(await pc.createAnswer()); send({ t: 'sig', d: { sdp: pc.localDescription } }); }
    } else if (d.ice) await pc.addIceCandidate(d.ice);
  }
  function makePc() {
    pc = new RTCPeerConnection({ iceServers: ICE });
    pc.onicecandidate = e => { if (e.candidate) send({ t: 'sig', d: { ice: e.candidate } }); };
    pc.onconnectionstatechange = () => {
      if (pc && pc.connectionState === 'connected' && role === 'host') beginHostMatch();
      if (pc && pc.connectionState === 'failed') teardown('Video link failed: your networks block a direct connection (a TURN server is needed).');
    };
  }

  // ---------- host ----------
  async function hostStart() {
    setMsg('Friend joined. Connecting video…');
    const cap = document.createElement('canvas'); cap.width = 1280; cap.height = 720; const c = cap.getContext('2d');
    ON.tick = () => { const r3 = B.r3; if (r3 && !r3.canvas.hidden) c.drawImage(r3.canvas, 0, 0, 1280, 720); c.drawImage(cv, 0, 0, 1280, 720); }; // 3D scene sits under the 2D overlay
    ON.take = () => { const r = { x: rin.x, y: rin.y, act: rin.act }; rin.act = false; return r; };
    ON.ask = hostAsk;
    ON.over = (title, sub) => send({ t: 'over', title, sub });
    ON.again = () => send({ t: 'again' });
    ON.quit = () => teardown('');
    const stream = cap.captureStream(30);
    if (tapStream) tapStream.getAudioTracks().forEach(t => stream.addTrack(t));
    makePc(); stream.getTracks().forEach(t => pc.addTrack(t, stream));
    await pc.setLocalDescription(await pc.createOffer());
    send({ t: 'sig', d: { sdp: pc.localDescription } });
  }
  function beginHostMatch() {
    if (begun) return; begun = true;
    jin.remote = keepers[1].remote = true;
    showDlg(false); B.startMatch();
  }
  function hostAsk(p, sub, opts, fallback) { // ask the guest to pick a move; their pick is validated against the host's own TP
    return new Promise(res => {
      const id = ++askId;
      const done = v => { if (!pending.has(id)) return; pending.delete(id); clearTimeout(t); res(v); };
      const t = setTimeout(() => { send({ t: 'menu', id, close: 1 }); done(fallback()); }, ASK_TIMEOUT);
      pending.set(id, { p, opts, done, fallback });
      B.addText(B.CX, B.CY - 30, 'WAITING FOR OPPONENT', '#ffe14d');
      send({ t: 'menu', id, title: p.ch.name, sub, opts: opts.map(o => ({ name: o.name, tp: o.tp, power: o.power, c: (B.ELEM[o.elem] || {}).c, ok: o.tp <= p.tp + 1e-6 })) });
    });
  }

  // ---------- guest ----------
  function guestStart() {
    setMsg('Connecting video…'); makePc();
    pc.ontrack = e => { if (!video) showGuestView(); video.srcObject = e.streams[0]; video.play().catch(() => { }); };
  }
  const gk = new Set();
  let jx = 0, jy = 0, stickId = null; // touch stick vector (the game itself draws the knob)
  function guestVec() {
    const kx = (gk.has('KeyD') || gk.has('ArrowRight') ? 1 : 0) - (gk.has('KeyA') || gk.has('ArrowLeft') ? 1 : 0),
          ky = (gk.has('KeyS') || gk.has('ArrowDown') ? 1 : 0) - (gk.has('KeyW') || gk.has('ArrowUp') ? 1 : 0);
    return kx || ky ? [kx, ky] : [jx, jy];
  }
  let lastIn = ''; // send input only when it changes (rounded), so a held stick or key costs nothing and a hidden tab can't starve it
  function pushIn(act) {
    let [x, y] = guestVec(); x = Math.round(x * 20) / 20; y = Math.round(y * 20) / 20;
    const k = x + ',' + y; if (k === lastIn && !act) return;
    lastIn = k; send(act ? { t: 'in', x, y, act: 1 } : { t: 'in', x, y });
  }
  const stick = $('stick');
  function readStick(e) {
    const r = stick.getBoundingClientRect(); let dx = e.clientX - (r.left + r.width / 2), dy = e.clientY - (r.top + r.height / 2);
    const max = r.width / 2 - 20, d = Math.hypot(dx, dy); if (d > max) { dx *= max / d; dy *= max / d; }
    jx = dx / max; jy = dy / max; if (Math.hypot(jx, jy) < 0.15) jx = jy = 0;
    pushIn();
  }
  stick.addEventListener('pointerdown', e => { if (role === 'guest') { stickId = e.pointerId; readStick(e); } });
  stick.addEventListener('pointermove', e => { if (role === 'guest' && e.pointerId === stickId) readStick(e); });
  const endStick = e => { if (e.pointerId === stickId) { stickId = null; jx = jy = 0; pushIn(); } };
  stick.addEventListener('pointerup', endStick); stick.addEventListener('pointercancel', endStick);
  $('actBtn').addEventListener('pointerdown', e => { // capture: keep the game's own handler from starting a local match
    if (role !== 'guest') return; e.stopImmediatePropagation(); e.preventDefault();
    if (video && !menuId) pushIn(true);
  }, true);
  function guestKey(e) {
    if (role !== 'guest' || !video) return;
    const c = e.code, down = e.type === 'keydown';
    const dm = /^(?:Digit|Numpad)([0-9])$/.exec(c);
    if (dm && down && menuId) { stop(e); pick(+dm[1] === 0 ? 9 : +dm[1] - 1); return; }
    if (['KeyW', 'KeyA', 'KeyS', 'KeyD', 'ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight'].includes(c)) { stop(e); down ? gk.add(c) : gk.delete(c); pushIn(); return; }
    if (c === 'Space' || c === 'KeyJ' || c === 'Enter') { stop(e); if (down && !e.repeat && !menuId) pushIn(true); }
  }
  const stop = e => { e.preventDefault(); e.stopImmediatePropagation(); };
  window.addEventListener('keydown', guestKey, true); window.addEventListener('keyup', guestKey, true);
  window.addEventListener('blur', () => { gk.clear(); if (role === 'guest') pushIn(); });

  function showGuestView() {
    showDlg(false); $('titleScreen').hidden = true;
    video = document.createElement('video'); video.autoplay = true; video.playsInline = true;
    video.style.cssText = 'position:absolute;inset:0;width:100%;height:100%;object-fit:contain;background:#000;z-index:20';
    $('stage').append(video);
    $('stage').insertAdjacentHTML('beforeend', '<div id="onHint">You are the right-hand fighter · stick or WASD moves · button or Space shoots/dashes · tap or press 1-9 to pick a move</div>');
    lastIn = '';
  }
  function showMenu(m) {
    const cmd = $('cmd'), L = $('cmdList');
    if (m.close) { cmd.hidden = true; menuId = 0; return; }
    menuId = m.id; $('cmdTitle').textContent = m.title; $('cmdSub').textContent = m.sub; $('cmdInfo').textContent = ''; L.innerHTML = '';
    m.opts.forEach((o, i) => {
      const b = document.createElement('button'); b.type = 'button'; b.className = 'mv' + (o.tp ? ' sp' : ''); b.style.setProperty('--ec', o.c || '#9aa6b8');
      for (const [cls, txt] of [['k', i < 9 ? i + 1 : i === 9 ? 0 : '–'], ['nm', o.name], ['tp', o.tp ? o.tp + ' TP' : 'Free']]) { const s = document.createElement('span'); s.className = cls; s.textContent = txt; b.append(s); }
      if (!o.ok) { b.setAttribute('aria-disabled', 'true'); b.style.opacity = .45; }
      b.onclick = () => { if (o.ok) pick(i); };
      L.append(b);
    });
    cmd.hidden = false;
  }
  function pick(i) { send({ t: 'pick', id: menuId, i }); menuId = 0; $('cmd').hidden = true; }
  function showOver(title, sub) {
    $('onOver')?.remove();
    const d = document.createElement('div'); d.id = 'onOver';
    const h = document.createElement('div'); const a = document.createElement('h2'), b = document.createElement('p'), c = document.createElement('p');
    a.textContent = title; b.textContent = sub; c.textContent = 'Waiting for the host to start a rematch…'; h.append(a, b, c); d.append(h); $('stage').append(d);
  }

  // ---------- teardown ----------
  function teardown(msg) {
    const wasGuest = role === 'guest', wasHost = role === 'host';
    if (pc) { pc.onconnectionstatechange = null; pc.close(); pc = null; }
    if (ws) { const w = ws; ws = null; w.onclose = null; w.close(); }
    for (const e of [...pending.values()]) e.done(e.fallback());
    jin.remote = keepers[1].remote = false;
    ON.tick = ON.take = ON.ask = ON.over = ON.again = ON.quit = null;
    rin.x = rin.y = 0; rin.act = false; gk.clear(); jx = jy = 0; stickId = null; role = null; begun = false; menuId = 0;
    if (video) { video.remove(); video = null; $('onHint')?.remove(); $('onOver')?.remove(); $('cmd').hidden = true; }
    if (wasGuest) $('titleScreen').hidden = false;
    if (!msg) return;
    if (wasHost && $('onDlg').style.display !== 'grid') B.addText(B.CX, B.CY - 30, msg, '#ffe14d');
    else { setMsg(msg); lobbyBusy(false); showDlg(true); }
  }
})();
