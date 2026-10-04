# ⚽ Blaze vs Bedrock

> **High-Octane Retro Anime Soccer Duel Engine with Triple-Pipeline Rendering**  
> *Captain Tsubasa* & *Inazuma Eleven* meets *Street Fighter* and *Mario Strikers* in a pure, zero-dependency HTML5/JavaScript experience.

---

## 📖 Overview

**Blaze vs Bedrock** is an arcade soccer duel game that blends real-time pitch control with tactical, time-stop anime showdowns. When players collide, time freezes, initiating a mind-game duel where element advantages, stats, and Tension Points (TP) determine who blasts the ball toward the net.

The project features a **Triple-Pipeline Graphics Engine**, allowing instant switching between retro Amiga pixel aesthetics, 960x540 Neo-Geo arcade sprites, and real-time 64-bit 3D WebGL action.

---

## ⚡ Key Features

* **Tactical Time-Stop Duels**: Running into an opponent or keeper halts the action to pick Dribble, Block, Shot, or Save moves.
* **Elemental Rock-Paper-Scissors**:
  * 🔥 **Flame** beats 🌪️ **Gale**
  * 🌪️ **Gale** beats 🪨 **Stone**
  * 🪨 **Stone** beats 🔥 **Flame**
  * Advantage grants a **+20% power boost**, while matching a move to the character's innate element yields an extra **+10% signature bonus**.
* **Triple-Pipeline Rendering Engine**:
  * **12-Bit Amiga Pipeline**: 320x180 internal canvas scaled up with authentic 32-color palette quantization, raster dithering, and `Press Start 2P` pixel typography.
  * **32-Bit Arcade Pipeline**: Native 960x540 canvas with multi-layered motion trails, particle sparks, gradient auras, and dynamic HUD.
  * **64-Bit 3D WebGL Pipeline**: Built-in Three.js pitch, 3D stadium lights, player billboard meshes, dynamic action camera tracking, and dramatic 3D cutscenes.
* **Signature Special Shots**:
  * **Crimson Meteor**: Devastating Flame blast with high power.
  * **Phantom Barrage**: Splits into 5 phantom balls, reducing the goalkeeper's save chance by 10%.
  * **Photon Laser**: Ultra-high-velocity linear beam that moves too fast to block.
  * **Hellfire Missile**: Homing curve strike with zero distance falloff.
  * **Thunderbolt Barrage** (Thunder): the ball turns into lightning that strikes the keeper instantly. Unblockable, keeper −12%, can't be held.
  * **Gatling Volley** (Steel): the ball turns into a burst of brass slugs. Unblockable, keeper −8%, can't be held.
  * **Avalanche Snowball** (Frost): a slow, heavy snowball that shoves the keeper back. Keeper −15%, can't be held.
  * **Hydro Cannon** (Water): a pressurised water jet with the ball inside a bubble. Soaks the keeper, keeper −10%, can't be held.
  * **Imperial Dragon** (Dragon): a dragon carries the ball in its jaws, its body following the ball's trail. Keeper −18%, can't be held.
  * **Colossus Lion** (Beast): a giant lion gallops in with the ball in its jaws and roars at the keeper. Keeper −16%, can't be held.
  * **Sword Storm** (Blade): a fan of swords and knives launches round the ball, opening mid-flight and closing on the keeper. Unblockable, keeper −14%, can't be held.
  * **Verdant Tempest** (Nature): a helix of glowing magic leaves swirls round the ball. Keeper −10%, can't be held, and it restores 12 TP to the kicker.
  * **Zigzag Comet** (Gale): a curve shot that swings from side to side in straight legs and sharp turns (a flash and blip at each turn), weaves past the defender and comes in on the keeper. Unblockable, keeper −8%.
  * **Special-shot UI**: move cards carry the element colour and an animated power bar; the cutscene title card has a wiping slash banner, a line saying what the move does to the keeper, and a power meter that fills and counts up.
  * **Release cameras**: after the strike each cutscene follows its shot with its own camera: `low` (the default low follow), `high` (a crane that lifts up and back for a bird's-eye view), `push` (a close side chase that starts on a wide lens and tightens) and `dutch` (a steeper bank).
  * **Choreography (3D)**: every special shot has its own cutscene opening camera, charge weather, ground marks in flight and keeper reaction (burn, spin, riddle, shock, freeze). See `CHOREO` in the game file.
  * **Tectonic Hammer**: Massive seismic shockwave shot.
* **Procedural Web Audio Engine**:
  * Custom synth built on Web Audio API (zero external sound files needed).
  * Custom square, saw, noise-snare, and kick oscillators for dynamic chiptune/arcade effects, whistles, crowds, and impact explosions.
* **UI Motion (GSAP, optional)**: the title card, fighter chips, duel menu, win screen and roster cards (ScrollTrigger reveal, stat bars filling) are animated with GSAP from cdnjs. If the CDN is unreachable or the player prefers reduced motion, the UI is simply static. HD 3D also has a cinematic grade pass (vignette, S-curve contrast, night/golden tint, light film grain) that drops with the other HD effects when quality steps down.
* **Full Mobile & Desktop Support**:
  * Keyboard & mouse controls on desktop.
  * Responsive virtual joystick and action button on touch devices.

---

## 👥 Roster

### Field Players

| Player | Team | Role | Element | Stats (Kick/Dribble/Block/Spd) | Signature Moves |
| :--- | :--- | :--- | :---: | :---: | :--- |
| **Haru Kagari** | Akebono FC | Striker (#9) | 🔥 Flame | 80 / 70 / 56 / 74 | *Crimson Meteor*, *Tempest Drive*, *Blaze Step*, *Gale Sweep*, *Phantom Barrage*, *Photon Laser*, *Hellfire Missile*, *Thunderbolt Barrage*, *Gatling Volley*, *Avalanche Snowball*, *Hydro Cannon*, *Imperial Dragon*, *Colossus Lion*, *Sword Storm*, *Verdant Tempest*, *Zigzag Comet* |
| **Jin Kurogane** | Tetsuzan Academy | Libero (#5) | 🪨 Stone | 76 / 64 / 76 / 68 | *Tectonic Hammer*, *Shard Spiral*, *Granite Guard*, *Mirage Feint* |
| **Raijin Ikazuchi** | Raikou Tech | Winger (#11) | ⚡ Thunder | 74 / 78 / 50 / 88 | *Volt Strike*, *Static Dash*, *Shock Wall*, *Thunderbolt Barrage*, *Zigzag Comet*, *Gatling Volley* |
| **Fubuki Shirayuki** | Tetsuzan Academy | Midfielder (#8) | ❄️ Frost | 70 / 72 / 74 / 66 | *Glacier Lance*, *Ice Slide*, *Frost Wall*, *Avalanche Snowball*, *Sword Storm*, *Zigzag Comet* |
| **Aoi Minato** | Akebono FC | Playmaker (#10) | 💧 Water | 72 / 82 / 62 / 72 | *Tidal Burst*, *Current Glide*, *Undertow*, *Hydro Cannon*, *Imperial Dragon*, *Verdant Tempest* |

Pick your fighter and your rival on the title screen (picking the rival's fighter swaps the two). The keepers belong to the left and right side, so they stay Kaito (you) and Genta (AI) whoever plays.

### Goalkeepers

| Keeper | Team | Role | Element | Catch Stat | Signature Save |
| :--- | :--- | :--- | :---: | :---: | :--- |
| **Kaito Minase** | Akebono FC | Goalkeeper (#1) | 🌪️ Gale | 60 | *Tornado Wall* (Power: 52, TP: 30), *Iron Bulwark* (giant iron shield, Power: 58, TP: 34), *Titan Hands* (two giant hands, Power: 56, TP: 32) |
| **Genta Iwaki** | Tetsuzan Academy | Goalkeeper (#1) | 🪨 Stone | 60 | *Bedrock Fortress* (Power: 54, TP: 32), *Iron Bulwark*, *Titan Hands* |

---

## 🎮 Controls

### Desktop Keyboard & Mouse
* **Move**: `W` `A` `S` `D` or `Arrow Keys`
* **Shoot / Dash**: `Space` or `J`
  * *With ball*: Prepares and releases a shot toward the goal.
  * *Without ball*: Performs a high-speed dash tackle.
* **Duel Selection**: `1`, `2`, `3`, `4` or direct mouse click on move cards.
* **Skip Cutscenes**: `Space` or mouse click.
* **Engine Switching**: `T` (cycles between 32-Bit Arcade ➔ 64-Bit 3D ➔ HD 3D ➔ 12-Bit Amiga).
* **HD Lighting**: `G` (HD 3D only) switches between a night match and golden hour.
* **Camera views**: `C` / `Shift+C` (3D modes only) cycles Broadcast, Cinematic, Follow, Over-the-shoulder, Orbit (drag, `Q`/`E`, wheel), First-person, Helmet HUD, Cockpit, Fixed angles, Isometric, Top-down, CCTV and Photo mode. Photo mode freezes the match: `WASD` to fly, `Q`/`E` to go down/up, drag to look, wheel to zoom, `Space` to save a PNG. In the views that sit behind or inside Haru, movement keys follow the camera.
* **Debug Tools**:
  * `F`: FPS meter (in HD it also shows the auto-quality level, which drops a step whenever the game runs under 50 FPS for 2s).
  * `P`: Audit on-screen palette (12-bit mode).
  * `M`: Toggle 320x180 mock scene.

### Mobile & Touchpad
* **Movement**: Virtual analog stick on the left.
* **Action**: Big action button on the right (Tap to Shoot / Dash).
* **Landscape Mode**: Recommended for optimal touch play.

---

## 🧮 Duel Mechanics

When players collide or when a shot reaches a defender/keeper, a duel sequence triggers:

$$\text{Duel Score} = (\text{Stat} \times 0.5 + \text{Move Power} + \text{Roll}(0 \dots 24)) \times \text{Signature Bonus} \times \text{Element Advantage}$$

* **Signature Bonus**: $\times 1.10$ if the move matches the player's innate element.
* **Element Advantage**: $\times 1.20$ if the move's element counters the opponent's move.
* **Shot Distance Falloff**: Normal shots lose power over distance ($\times 1.08$ at point-blank down to $\times 0.45$ from the defensive half). *Hellfire Missile* ignores distance falloff.

---

## 🚀 Getting Started

No build tools, `npm install`, or bundlers required. Everything runs directly in the browser!

### Quick Launch
1. Double-click [Blaze vs Bedrock.html](file:///c:/SESHU/PROJECTS/OTHER%20PROJECTS/FOOTBALL/Blaze%20vs%20Bedrock.html) in your file explorer to open it in Chrome, Edge, Firefox, or Safari.
2. Hit **Kick off** and enjoy!

### Local Development Server (Optional)
To run with an HTTP server for development:
```bash
# Using Python
python -m http.server 8000

# Using Node (npx)
npx serve .
```
Then navigate to `http://localhost:8000/Blaze%20vs%20Bedrock.html`.

---

## 🌐 Online 1v1

The host runs the real game and streams its canvas and audio to the guest over WebRTC. The guest sends keys and move picks back and plays the right-hand fighter. `server/` only pairs players by room code and relays signaling, input and menu picks.

```
Host browser ──WebRTC video+audio──► Guest browser
     ▲  └──────── WebSocket ────────┐     │
     └─ input + menu picks ◄── room server (server/) ◄┘   /healthz  /metrics
```

Run it locally (two terminals, then open the game in two tabs and use **Play online 1v1**):

```bash
cd server && npm ci && npm start
```

```bash
python -m http.server 8000
```

* **Config:** `?server=wss://host` overrides the server URL; `SERVER` and the STUN list sit at the top of `online.js`. On the server, `PORT` and `ALLOWED_ORIGINS` (comma-separated) are env vars.
* **Ops:** `GET /healthz`, Prometheus text at `GET /metrics` (rooms, connections, relayed/dropped messages, bytes). Per-socket rate limit, 8 KB message cap, origin allow-list, ping/pong reaping of dead sockets.
* **CI/CD:** `.github/workflows/ci.yml` runs tests and `npm audit`, builds the image, scans it with Trivy, smoke-tests the container, pushes to GHCR on `main`, and deploys to Fly.io when repository variable `DEPLOY_FLY=true` and secret `FLY_API_TOKEN` are set.
* **Known limits:** STUN only (some networks need a TURN server); rooms live in one process's memory; the guest feels host round-trip lag and the host could cheat, which is fine for friends.

---

## 📁 Repository Structure

```
FOOTBALL/
├── Blaze vs Bedrock.html       # Primary complete single-file game bundle
├── Blaze vs Bedrock.backup.html# Baseline reference backup
├── build_12bit_version.py      # Build script for 12-bit Amiga retro quantization pipeline
├── generate_32bit_game.py      # Generator script uniting 32-bit, 12-bit, and 64-bit engines
├── check_file.py               # Quick validation and inspection utility
├── assets/gk-*.json            # Baked Mixamo goalkeeper clips: catch, dive, sidestep, dropkick (limb directions per frame)
├── trailer/                    # Remotion project for the trailer (src/Trailer.tsx). Needs public/gameplay.mp4 = a copy of blaze-demo.v2-720p.mp4; `npm i && npx remotion studio`, render with `npx remotion render Trailer out/blaze-trailer.mp4`
├── tools/bake-clip.mjs         # Bakes a Mixamo FBX into one of those jsons (see its header for usage)
├── tools/three2unity/          # Developer tool: snapshot a running Three.js page into a Unity project folder (see its README)
└── README.md                   # Project documentation and specifications
```

---

## 🗺️ Roadmap & Commercial Expansion

* [ ] **Clash Minigame**: Split-screen button mash/timing clash on tied rolls.
* [x] **Roster Expansion**: Thunder (⚡), Water (💧) and Frost (❄️) fighters (Raijin, Aoi, Fubuki) with a title-screen fighter select.
* [ ] **Roguelite Tournament Mode**: Single-player cup with artifact drafts and skill unlocks (*Balatro* x *Soccer*).
* [x] **Online 1v1**: room codes, host-streamed WebRTC play and a Node room server (see *Online 1v1* below). The guest can use the keyboard or the on-screen touch stick.
* [ ] **Gamepad Support**: Standard Gamepad API integration for Xbox, PlayStation, and 8BitDo controllers.
* [ ] **Steam & Portal Release**: Exporting for Poki / CrazyGames web portals and packaging for Steam via Tauri / Electron.
