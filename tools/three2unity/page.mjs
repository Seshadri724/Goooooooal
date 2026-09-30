// Functions that run INSIDE the page being converted. cli.mjs serialises them with Function.prototype.toString, so each one
// must be self-contained (no imports, no closures over module scope).

// Patches Object3D.prototype.updateMatrixWorld so the page tells us which scene and camera it renders. Renderer.render()
// updates the scene and then the camera, so a camera is paired with the scene updated just before it.
// Installed two ways: appended to three's ES module (importmap pages), or when a classic <script> assigns window.THREE.
export function install(T) {
  const S = (globalThis.__t2u ??= { scenes: new Map(), cams: new Map(), last: null });
  if (S.T === T) return;
  S.T = T;
  const P = T.Object3D.prototype, orig = P.updateMatrixWorld;
  P.updateMatrixWorld = function (f) {
    if (this.isScene) { S.scenes.set(this, (S.scenes.get(this) || 0) + 1); S.last = this; }
    else if (this.isCamera && S.last) S.cams.set(this, S.last);
    return orig.call(this, f);
  };
}

// One-shot snapshot: exports the scene as a GLB and describes everything glTF can't carry (lights, camera, fog, background).
// Returns { glb: base64, info }.
export async function capture(opts) {
  const S = globalThis.__t2u;
  if (!S || !S.T) throw new Error('three.js was never loaded through the patched module (bundled build? set window.__t2u = { T: THREE, scene, camera } yourself)');
  const T = S.T;
  let scene = S.scene, best = -1;
  if (!scene) for (const s of S.scenes.keys()) { let n = 0; s.traverse(() => n++); if (n > best) { best = n; scene = s; } } // the busiest scene is the world
  if (!scene) throw new Error('no THREE.Scene has been rendered yet; use --eval / --wait to get the game into a scene first');
  let camera = S.camera;
  if (!camera) for (const [c, s] of S.cams) if (s === scene && (!camera || c.isPerspectiveCamera)) camera = c;
  scene.updateMatrixWorld(true);

  let GLTFExporter;
  try { ({ GLTFExporter } = await import('three/addons/exporters/GLTFExporter.js')); }
  catch (e) { ({ GLTFExporter } = await import(`https://cdn.jsdelivr.net/npm/three@0.${T.REVISION}.0/examples/jsm/exporters/GLTFExporter.js`)); }

  const hex = c => '#' + c.getHexString();
  const v3 = new T.Vector3(), q4 = new T.Quaternion(), sc = new T.Vector3(), tg = new T.Vector3();
  const report = { objects: {}, dropped: {}, warnings: [] };
  const lights = [], detached = [];
  const drop = (o, why) => { detached.push([o, o.parent, o.parent.children.indexOf(o)]); report.dropped[why] = (report.dropped[why] || 0) + 1; };

  // Lights, cameras and inverted-hull outlines (BackSide) don't survive glTF; lights and camera go to the sidecar instead.
  scene.traverse(o => {
    if (o === scene) return;
    report.objects[o.type] = (report.objects[o.type] || 0) + 1;
    const m = o.material, mats = Array.isArray(m) ? m : m ? [m] : [];
    if (o.isLight) {
      o.getWorldPosition(v3);
      const L = { name: o.name, type: o.type, color: hex(o.color), intensity: o.intensity, shadow: !!o.castShadow, pos: v3.toArray() };
      if (o.isDirectionalLight || o.isSpotLight) { o.target.updateWorldMatrix(true, false); o.target.getWorldPosition(tg); L.dir = tg.sub(v3).normalize().toArray(); }
      if (o.isPointLight || o.isSpotLight) { L.distance = o.distance; }
      if (o.isSpotLight) { L.angle = o.angle * 180 / Math.PI; L.penumbra = o.penumbra; }
      if (o.isHemisphereLight) L.ground = hex(o.groundColor);
      lights.push(L); drop(o, 'lights (to sidecar)');
    } else if (o.isCamera) drop(o, 'cameras (main one to sidecar)');
    else if (o.isSprite) drop(o, 'sprites');
    else if (mats.some(x => x.side === T.BackSide)) drop(o, 'inverted-hull outlines (rebuild as a Unity outline shader)');
    else {
      if (mats.some(x => x.isShaderMaterial)) report.warnings.push(`ShaderMaterial on "${o.name || o.type}" exports as a plain material`);
      if (o.isPoints || o.isLine) report.warnings.push(`${o.type} "${o.name}" may not render in Unity`);
    }
  });
  for (const [o, p] of detached.slice().reverse()) p.remove(o);

  // Unique sibling names so every node has a stable Unity path (Transform.Find takes the first match).
  const nodes = [], names = new Map();
  const walk = (parent, prefix) => {
    const seen = new Map();
    for (const c of parent.children) {
      let n = (c.name || c.type).replace(/[\/\\]/g, '_'), k = seen.get(n) || 0; seen.set(n, k + 1);
      if (k) n += '_' + (k + 1);
      names.set(c, c.name); c.name = n;
      const path = prefix ? prefix + '/' + n : n;
      nodes.push({ o: c, path }); walk(c, path);
    }
  };
  walk(scene, '');

  let buf;
  try {
    buf = await new GLTFExporter().parseAsync(scene, { binary: true, onlyVisible: false, trs: true, maxTextureSize: opts.maxTexture || 2048 });
  } finally {
    for (const [o, n] of names) o.name = n;
    for (const [o, p, i] of detached) { p.children.splice(i, 0, o); o.parent = p; } // ascending index per parent puts each back where it was
  }
  S.nodes = nodes; S.scene = scene; S.camera = camera;

  const u8 = new Uint8Array(buf); let bin = '';
  for (let i = 0; i < u8.length; i += 0x8000) bin += String.fromCharCode.apply(null, u8.subarray(i, i + 0x8000));

  const info = { lights, hidden: nodes.filter(n => !n.o.visible).map(n => n.path), report, nodeCount: nodes.length, revision: T.REVISION };
  const f = scene.fog;
  info.fog = f ? { on: true, exp: !!f.isFogExp2, color: hex(f.color), near: f.near || 0, far: f.far || 0, density: f.density || 0 } : { on: false };
  info.background = scene.background && scene.background.isColor ? hex(scene.background) : '';
  if (scene.background && !scene.background.isColor) report.warnings.push('scene.background is a texture/cube map; set a skybox in Unity');
  if (camera) {
    camera.updateMatrixWorld(true); camera.matrixWorld.decompose(v3, q4, sc);
    info.camera = { on: true, ortho: !!camera.isOrthographicCamera, fov: camera.fov || 0, near: camera.near, far: camera.far, pos: v3.toArray(), rot: q4.toArray(),
      size: camera.isOrthographicCamera ? (camera.top - camera.bottom) / 2 / camera.zoom : 0 };
  } else info.camera = { on: false };
  return { glb: btoa(bin), info };
}

// Samples every exported node's local transform and visibility (plus the camera) for `seconds`, then keeps only what moved.
// Times are real seconds; quaternions are sign-continuous so Unity doesn't slerp the long way round.
export async function record({ seconds, fps }) {
  const S = globalThis.__t2u, nodes = S.nodes, cam = S.camera, T = S.T, N = nodes.length, W = 11;
  const times = [], rows = [], cams = [], q = new T.Quaternion(), p = new T.Vector3(), s = new T.Vector3();
  await new Promise(done => {
    const t0 = performance.now(); let last = -1;
    const tick = now => {
      const e = (now - t0) / 1000;
      if (last < 0 || e - last >= 1 / fps - 0.002) {
        last = e; times.push(e);
        const r = new Float32Array(N * W);
        nodes.forEach(({ o }, i) => { r.set([o.position.x, o.position.y, o.position.z, o.quaternion.x, o.quaternion.y, o.quaternion.z, o.quaternion.w, o.scale.x, o.scale.y, o.scale.z, o.visible ? 1 : 0], i * W); });
        rows.push(r);
        if (cam) { cam.updateMatrixWorld(true); cam.matrixWorld.decompose(p, q, s); cams.push([...p.toArray(), ...q.toArray(), cam.fov || 0]); }
      }
      if (e < seconds) requestAnimationFrame(tick); else done();
    };
    requestAnimationFrame(tick);
  });
  const rd = v => Math.round(v * 1e4) / 1e4, moved = (a, b, n) => { for (let k = 0; k < n; k++) if (Math.abs(a[k] - b[k]) > 1e-4) return true; return false; };
  const tracks = [];
  const flip = (arr, from) => { for (let i = 1; i < arr.length; i++) { let d = 0; for (let k = 0; k < 4; k++) d += arr[i][from + k] * arr[i - 1][from + k]; if (d < 0) for (let k = 0; k < 4; k++) arr[i][from + k] *= -1; } };
  nodes.forEach(({ path }, i) => {
    const seq = rows.map(r => r.subarray(i * W, i * W + W)), a = seq[0], any = k => seq.some(x => x[k] !== a[k]);
    const mp = seq.some(x => moved(x.subarray(0, 3), a.subarray(0, 3), 3)), mr = seq.some(x => moved(x.subarray(3, 7), a.subarray(3, 7), 4)),
      ms = seq.some(x => moved(x.subarray(7, 10), a.subarray(7, 10), 3)), mv = any(10);
    if (!(mp || mr || ms || mv)) return;
    const copy = seq.map(x => Array.from(x));
    if (mr) flip(copy, 3);
    const pick = (from, n) => copy.flatMap(x => x.slice(from, from + n).map(rd));
    tracks.push({ path, p: mp ? pick(0, 3) : [], r: mr ? pick(3, 4) : [], s: ms ? pick(7, 3) : [], v: mv ? copy.map(x => x[10]) : [] });
  });
  let camera = { on: false };
  if (cam) {
    flip(cams, 3);
    camera = { on: true, p: cams.flatMap(c => c.slice(0, 3).map(rd)), r: cams.flatMap(c => c.slice(3, 7).map(rd)), fov: cams.map(c => rd(c[7])) };
  }
  return { times: times.map(rd), tracks, camera };
}
