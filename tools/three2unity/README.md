# three2unity

Developer tool: snapshot a **running** Three.js page into a Unity `Assets/ThreeImport` folder.

It does not translate code. It opens the page in a headless Chrome/Edge, finds the `THREE.Scene` the page renders, and writes:

| Output | What it is |
|---|---|
| `scene.glb` | The whole scene graph: meshes, materials, textures (canvas textures included), hierarchy, transforms |
| `scene.json` | What glTF can't carry: lights, camera, fog, background, which nodes start hidden, and an optional recorded motion clip |
| `Editor/ImportThreeScene.cs` | Unity menu **Three2Unity > Build Scene**: instantiates the glb, adds lights / camera / fog, builds an `AnimationClip` + Animator from the recording |
| `REPORT.md` | Object counts, what was left out, warnings |

## Use

```bash
cd tools/three2unity && npm install          # once (puppeteer-core only; uses your installed Chrome or Edge)
node cli.mjs "../../Blaze vs Bedrock.html" --out ../../MyUnityProject \
  --eval "document.getElementById('modeBtn').click(); document.getElementById('modeBtn').click(); document.getElementById('startBtn').click()" \
  --wait 5000 --record 3 --scale 0.03
node check.mjs ../../MyUnityProject/Assets/ThreeImport     # optional sanity check of the output
```

`--eval` gets the page into the state you want captured (start the match, pick the 3D mode). `--scale 0.03` turns this game's 60-unit players into 1.8 m. Options: `node cli.mjs` with no arguments.

In Unity: install **glTFast** (Package Manager > + > Add package by name > `com.unity.cloud.gltfast`), let `scene.glb` import, then run **Three2Unity > Build Scene**. Everything lands under `ThreeSceneRoot`; run it again to rebuild.

## See the output without Unity

```bash
node preview.mjs ../../MyUnityProject/Assets/ThreeImport      # opens http://127.0.0.1:8770/
```

A plain three.js page that loads `scene.glb` and `scene.json`, applies the lights, fog and camera, and replays the recorded motion (button: free camera). It shows what the exporter captured, not how Unity will shade it. `.glb` also opens in Blender (free) or the Windows 3D Viewer, and imports directly into Godot 4 (free, open source) if you'd rather not use Unity.

## How it finds the scene

Pages that load three as an ES module (importmap or a CDN URL): the tool serves a copy of `three.module.js` with a small hook appended, so no change to your game is needed. Pages that use a classic `<script src=three.js>`: it hooks `window.THREE`. Bundled builds (webpack, vite) can't be hooked; set `window.__t2u = { T: THREE, scene, camera }` yourself before the tool captures.

## What converts and what doesn't

Converts: meshes, groups, materials (as glTF PBR / unlit), textures, hierarchy, instanced meshes, directional / point / spot / hemisphere / ambient lights, perspective and orthographic camera, linear and exp2 fog, solid background colour, initial visibility, and (with `--record`) local position / rotation / scale / visibility of every node that moves plus the camera's transform and FOV.

Left out, and listed in `REPORT.md`: sprites, inverted-hull outlines (BackSide meshes would z-fight their own model in Unity; use an outline shader), texture backgrounds and skyboxes. Toon and custom shader materials arrive as plain materials. Lines and points may not render.

Not converted, by design: game logic, input, audio, UI, post-processing, and procedural animation as *code* (it's captured only as the recording). This is the scene and one take of its motion, not a port of the game.

## Known limits

- **Not tested inside Unity.** The exporter and glb were verified (glb structure, every sidecar path resolves, the scene re-renders in three), and the handedness maths is unit-checked (`check.mjs`), but `ImportThreeScene.cs` has not been compiled or run in a Unity editor. Expect to fix small API details on first use.
- **Mirrored result?** The glTFast importer mirrors X. If your importer mirrors Z instead, re-run with `--flip z`.
- Recording runs in real time on a software renderer, so a heavy scene records at a few frames per second. Time is real seconds; a GPU-backed browser (or `--record` on a lighter scene) gives smoother clips.
- Node names are made unique per parent (`Group`, `Group_2`, ...) so Unity paths are stable; unnamed objects get their type as a name.
