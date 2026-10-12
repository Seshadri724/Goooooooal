import test from 'node:test';
import assert from 'node:assert/strict';
import { WebSocket } from 'ws';
import { createServer } from './server.js';

const open = (port) => new Promise(res => {
  const ws = new WebSocket(`ws://127.0.0.1:${port}`); ws.q = []; ws.w = [];
  ws.on('message', d => { const o = JSON.parse(d); const w = ws.w.shift(); w ? w(o) : ws.q.push(o); });
  ws.on('open', () => res(ws));
});
const next = ws => new Promise(res => (ws.q.length ? res(ws.q.shift()) : ws.w.push(res)));
const J = o => JSON.stringify(o);

test('create, join, relay, leave, metrics, limits', async () => {
  const s = await createServer({ port: 0, msgsPerSec: 5, metricsToken: '' });
  const host = await open(s.port), guest = await open(s.port);

  host.send(J({ t: 'create' }));
  const { code } = await next(host); assert.match(code, /^[A-Z]{4}$/);

  guest.send(J({ t: 'join', code: 'ZZZZ' }));
  assert.equal((await next(guest)).e, 'no-room');

  guest.send(J({ t: 'join', code: code.toLowerCase() }));
  assert.deepEqual(await next(host), { t: 'ready', role: 'host' });
  assert.deepEqual(await next(guest), { t: 'ready', role: 'guest' });

  const third = await open(s.port);
  third.send(J({ t: 'join', code })); assert.equal((await next(third)).e, 'room-full');

  guest.send(J({ t: 'in', x: 1, y: 0 }));
  assert.deepEqual(await next(host), { t: 'in', x: 1, y: 0 });
  host.send(J({ t: 'bogus' })); host.send('not json'); // dropped, never forwarded
  host.send(J({ t: 'sig', d: 'x' })); assert.equal((await next(guest)).t, 'sig');

  await new Promise(r => setTimeout(r, 1100)); // fresh rate-limit window
  const before = s.metrics.dropped;
  for (let i = 0; i < 20; i++) guest.send(J({ t: 'in', x: 0, y: 0 })); // flood: over the 5/s limit
  await new Promise(r => setTimeout(r, 150));
  assert.ok(s.metrics.dropped - before >= 14, 'rate limit drops the flood');

  const txt = await (await fetch(`http://127.0.0.1:${s.port}/metrics`)).text();
  assert.match(txt, /blaze_rooms_active 1/); assert.match(txt, /blaze_rooms_created_total 1/);
  const h = await fetch(`http://127.0.0.1:${s.port}/healthz`);
  assert.equal(h.status, 200); assert.equal((await h.json()).version, process.env.RENDER_GIT_COMMIT || process.env.GIT_SHA || 'dev');

  guest.close();
  let last; do { last = await next(host); } while (last.t === 'in'); // skip the flood messages that got under the limit
  assert.deepEqual(last, { t: 'left' });
  await new Promise(r => setTimeout(r, 50)); assert.equal(s.rooms.size, 0);
  await s.close();
});

test('/metrics needs the bearer token when one is set; /healthz stays public', async () => {
  const s = await createServer({ port: 0, metricsToken: 's3cret' });
  const get = (path, auth) => fetch(`http://127.0.0.1:${s.port}${path}`, auth ? { headers: { authorization: auth } } : {});
  assert.equal((await get('/metrics')).status, 401);
  assert.equal((await get('/metrics', 'Bearer wrong')).status, 401);
  assert.equal((await get('/metrics', 's3cret')).status, 401); // scheme required
  const ok = await get('/metrics', 'Bearer s3cret');
  assert.equal(ok.status, 200); assert.match(await ok.text(), /blaze_rooms_active 0/);
  assert.equal((await get('/healthz')).status, 200);
  await s.close();
});
