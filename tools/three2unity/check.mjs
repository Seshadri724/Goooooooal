// Self-check, no dependencies:  node check.mjs [path/to/Assets/ThreeImport]
// 1. the handedness maths that ImportThreeScene.cs repeats in C# (positions, rotations, the camera rig) holds for both flip axes;
// 2. with a folder: scene.glb is a valid glb and every path in scene.json (hidden nodes, animated nodes) exists in it.
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';

const mul = (a, b) => [a[3] * b[0] + a[0] * b[3] + a[1] * b[2] - a[2] * b[1], a[3] * b[1] - a[0] * b[2] + a[1] * b[3] + a[2] * b[0],
  a[3] * b[2] + a[0] * b[1] - a[1] * b[0] + a[2] * b[3], a[3] * b[3] - a[0] * b[0] - a[1] * b[1] - a[2] * b[2]];
const rot = (q, v) => { const r = mul(mul(q, [...v, 0]), [-q[0], -q[1], -q[2], q[3]]); return [r[0], r[1], r[2]]; };
const near = (a, b) => a.forEach((x, i) => assert.ok(Math.abs(x - b[i]) < 1e-9, `${a} != ${b}`));
const rnd = () => Math.random() * 2 - 1;

for (const flip of ['x', 'z']) {
  const V = ([x, y, z]) => flip === 'z' ? [x, y, -z] : [-x, y, z];
  const Q = ([x, y, z, w]) => flip === 'z' ? [-x, -y, z, w] : [x, -y, -z, w];
  for (let n = 0; n < 200; n++) {
    let q = [rnd(), rnd(), rnd(), rnd()]; const l = Math.hypot(...q); q = q.map(x => x / l);
    const v = [rnd(), rnd(), rnd()];
    near(rot(Q(q), V(v)), V(rot(q, v)));                       // rotating then mirroring = mirroring then rotating
    const cam = flip === 'z' ? Q(q) : mul(Q(q), [0, 1, 0, 0]);  // camera rig rotation (* Euler(0,180,0) when X is mirrored)
    near(rot(cam, [0, 0, 1]), V(rot(q, [0, 0, -1])));           // Unity camera forward (+Z) = three view direction (-Z)
    near(rot(cam, [0, 1, 0]), V(rot(q, [0, 1, 0])));            // and it stays upright
  }
}
console.log('handedness maths ok (flip x and z)');

const dir = process.argv[2];
if (dir) {
  const b = fs.readFileSync(path.join(dir, 'scene.glb'));
  assert.equal(b.toString('utf8', 0, 4), 'glTF'); assert.equal(b.readUInt32LE(8), b.length, 'glb length header');
  const g = JSON.parse(b.toString('utf8', 20, 20 + b.readUInt32LE(12))), paths = new Set();
  const walk = (i, pre) => { const n = g.nodes[i], p = pre ? pre + '/' + n.name : n.name; assert.ok(!paths.has(p), 'duplicate path ' + p); paths.add(p); (n.children || []).forEach(c => walk(c, p)); };
  g.scenes[g.scene || 0].nodes.forEach(i => walk(i, ''));
  const d = JSON.parse(fs.readFileSync(path.join(dir, 'scene.json'), 'utf8'));
  const want = [...d.hidden, ...d.clips.flatMap(c => c.tracks.map(t => t.path))], miss = want.filter(p => !paths.has(p));
  assert.equal(miss.length, 0, `paths in scene.json missing from the glb: ${miss.slice(0, 5)}`);
  for (const c of d.clips) for (const t of c.tracks) for (const [k, stride] of [['p', 3], ['r', 4], ['s', 3], ['v', 1]]) assert.ok(!t[k].length || t[k].length === c.times.length * stride, `${t.path}.${k} length`);
  console.log(`${dir}: ${g.nodes.length} nodes, ${want.length} sidecar paths, all resolve`);
}
