// Bakes a Mixamo FBX clip into per-frame limb directions in the game rig's axes (+x forward, +y up, +z right), so the
// game ships a ~20 KB json instead of a 2 MB FBX and needs no FBXLoader at runtime.
//   cd tools && npm i --no-save three@0.169.0 && node bake-clip.mjs "<Goalkeeper Catch.fbx>" ../assets/gk-catch.json
// Frame layout (GK_S floats): 12 unit vectors [thighL shinL footL thighR shinR footR armL foreL armR foreR spine shoulders(R-L)],
// then the hips height as a fraction of Mixamo's standing hip height (95.65 cm). Mixamo faces +z with its left at +x; the rig maps (x,y,z) -> (z,y,-x).
import fs from 'node:fs';
import * as THREE from 'three';
import { FBXLoader } from 'three/examples/jsm/loaders/FBXLoader.js';

const [src, dst] = process.argv.slice(2);
const buf = fs.readFileSync(src);
const g = new FBXLoader().parse(buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength), '');
const clip = g.animations.find(a => a.tracks.length);
const mix = new THREE.AnimationMixer(g); mix.clipAction(clip).play();
const bone = n => g.getObjectByName('mixamorig' + n) ?? g.getObjectByName('mixamorig:' + n) ?? (() => { throw new Error('no bone ' + n); })();
const SLOTS = [['LeftUpLeg', 'LeftLeg'], ['LeftLeg', 'LeftFoot'], ['LeftFoot', 'LeftToeBase'], ['RightUpLeg', 'RightLeg'], ['RightLeg', 'RightFoot'], ['RightFoot', 'RightToeBase'],
  ['LeftArm', 'LeftForeArm'], ['LeftForeArm', 'LeftHand'], ['RightArm', 'RightForeArm'], ['RightForeArm', 'RightHand'], ['Hips', 'Neck'], ['LeftArm', 'RightArm']]
  .map(([a, b]) => [bone(a), bone(b)]);
const hips = bone('Hips'), hands = [bone('LeftHand'), bone('RightHand')];
const n = Math.ceil(clip.duration * 30) + 1, dt = clip.duration / (n - 1), a = new THREE.Vector3(), b = new THREE.Vector3(), f = [];
const STAND = 95.65;
let tc = 0, best = -1;
for (let i = 0; i < n; i++) {
  mix.setTime(i * dt); g.updateMatrixWorld(true);
  for (const [p, q] of SLOTS) {
    p.getWorldPosition(a); q.getWorldPosition(b); b.sub(a).normalize();
    f.push(b.z, b.y, -b.x);
  }
  f.push(hips.getWorldPosition(a).y / STAND);
  const h = (hands[0].getWorldPosition(a).y + hands[1].getWorldPosition(b).y) / 2; // highest hands = the catch / the dive's reach
  if (h > best) { best = h; tc = i * dt; }
}
fs.writeFileSync(dst, JSON.stringify({ n, dt, dur: clip.duration, tc, f: f.map(v => +v.toFixed(3)) }));
console.log(`${n} frames, ${clip.duration.toFixed(2)}s, catch at ${tc.toFixed(2)}s -> ${dst}`);
