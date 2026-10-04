// Room + relay server for Blaze vs Bedrock online 1v1.
// The host browser runs the game and streams video over WebRTC; this server only pairs two players by room code,
// relays signaling / input / menu picks between them, and exposes /healthz and /metrics for ops.
import http from 'node:http';
import { fileURLToPath } from 'node:url';
import { WebSocketServer } from 'ws';

const ALPHABET = 'ABCDEFGHJKLMNPQRSTUVWXYZ'; // no I/O: harder to misread when shared aloud
const VERSION = process.env.RENDER_GIT_COMMIT || process.env.GIT_SHA || 'dev'; // CI waits for /healthz to report the commit it deployed
const RELAY = new Set(['sig', 'in', 'menu', 'pick', 'over', 'again']); // the only message types forwarded to the peer

export function createServer({
  port = 8080,
  maxRooms = 500,
  maxMsgBytes = 8192,
  msgsPerSec = 120, // ponytail: fixed 1s window per socket; token bucket if bursts matter
  origins = (process.env.ALLOWED_ORIGINS || '').split(',').filter(Boolean),
} = {}) {
  const rooms = new Map(); // code -> { host, guest }
  const m = { created: 0, joined: 0, relayed: 0, dropped: 0, bytes: 0, rejected: 0 };
  const started = Date.now();

  const metrics = () => [
    ['blaze_ws_connections', 'gauge', wss.clients.size],
    ['blaze_rooms_active', 'gauge', rooms.size],
    ['blaze_rooms_created_total', 'counter', m.created],
    ['blaze_rooms_joined_total', 'counter', m.joined],
    ['blaze_messages_relayed_total', 'counter', m.relayed],
    ['blaze_messages_dropped_total', 'counter', m.dropped],
    ['blaze_connections_rejected_total', 'counter', m.rejected],
    ['blaze_relay_bytes_total', 'counter', m.bytes],
    ['blaze_uptime_seconds', 'gauge', Math.round((Date.now() - started) / 1000)],
  ].map(([n, t, v]) => `# TYPE ${n} ${t}\n${n} ${v}`).join('\n') + '\n';

  const server = http.createServer((req, res) => {
    if (req.url === '/healthz') { res.writeHead(200, { 'content-type': 'application/json' }); return res.end(JSON.stringify({ ok: true, rooms: rooms.size, version: VERSION })); }
    if (req.url === '/metrics') { res.writeHead(200, { 'content-type': 'text/plain; version=0.0.4' }); return res.end(metrics()); }
    res.writeHead(404); res.end();
  });
  const wss = new WebSocketServer({ server, maxPayload: maxMsgBytes });

  const send = (ws, o) => { if (ws && ws.readyState === 1) ws.send(JSON.stringify(o)); };
  const newCode = () => { for (;;) { let c = ''; for (let i = 0; i < 4; i++) c += ALPHABET[Math.floor(Math.random() * ALPHABET.length)]; if (!rooms.has(c)) return c; } };
  const leave = ws => {
    const r = rooms.get(ws.code); if (!r) return;
    const peer = r.host === ws ? r.guest : r.host;
    send(peer, { t: 'left' }); if (peer) peer.code = null; rooms.delete(ws.code); ws.code = null;
  };

  wss.on('connection', (ws, req) => {
    if (origins.length && !origins.includes(req.headers.origin)) { m.rejected++; return ws.close(1008, 'origin'); }
    ws.isAlive = true; ws.on('pong', () => { ws.isAlive = true; });
    let winStart = Date.now(), winCount = 0;
    ws.on('message', (raw, isBinary) => {
      const now = Date.now(); if (now - winStart > 1000) { winStart = now; winCount = 0; }
      if (isBinary || ++winCount > msgsPerSec) { m.dropped++; return; }
      let msg; try { msg = JSON.parse(raw); } catch { m.dropped++; return; }
      if (!msg || typeof msg.t !== 'string') { m.dropped++; return; }
      if (msg.t === 'create') {
        if (ws.code) leave(ws);
        if (rooms.size >= maxRooms) return send(ws, { t: 'error', e: 'full' });
        const code = newCode(); rooms.set(code, { host: ws, guest: null }); ws.code = code; m.created++;
        return send(ws, { t: 'created', code });
      }
      if (msg.t === 'join') {
        const code = String(msg.code || '').toUpperCase(), r = rooms.get(code);
        if (!r) return send(ws, { t: 'error', e: 'no-room' });
        if (r.guest) return send(ws, { t: 'error', e: 'room-full' });
        if (ws.code) leave(ws);
        r.guest = ws; ws.code = code; m.joined++;
        send(r.host, { t: 'ready', role: 'host' }); return send(ws, { t: 'ready', role: 'guest' });
      }
      if (!RELAY.has(msg.t)) { m.dropped++; return; }
      const r = rooms.get(ws.code); if (!r) return;
      const peer = r.host === ws ? r.guest : r.host; if (!peer) return;
      m.relayed++; m.bytes += raw.length; peer.send(raw.toString());
    });
    ws.on('close', () => leave(ws));
    ws.on('error', () => { });
  });

  const beat = setInterval(() => { for (const ws of wss.clients) { if (!ws.isAlive) { ws.terminate(); continue; } ws.isAlive = false; ws.ping(); } }, 20000);
  beat.unref();

  return new Promise(resolve => server.listen(port, () => resolve({
    port: server.address().port, rooms, metrics: m,
    close: () => new Promise(r => { clearInterval(beat); for (const c of wss.clients) c.terminate(); wss.close(); server.close(r); }),
  })));
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  const s = await createServer({ port: +process.env.PORT || 8080 });
  console.log(`blaze-duel-server listening on :${s.port}`);
  const stop = () => s.close().then(() => process.exit(0)); // clean shutdown on container stop
  process.on('SIGTERM', stop); process.on('SIGINT', stop);
}
