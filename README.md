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
  * **Tectonic Hammer**: Massive seismic shockwave shot.
* **Procedural Web Audio Engine**:
  * Custom synth built on Web Audio API (zero external sound files needed).
  * Custom square, saw, noise-snare, and kick oscillators for dynamic chiptune/arcade effects, whistles, crowds, and impact explosions.
* **Full Mobile & Desktop Support**:
  * Keyboard & mouse controls on desktop.
  * Responsive virtual joystick and action button on touch devices.

---

## 👥 Roster

### Field Players

| Player | Team | Role | Element | Stats (Kick/Dribble/Block/Spd) | Signature Moves |
| :--- | :--- | :--- | :---: | :---: | :--- |
| **Haru Kagari** | Akebono FC | Striker (#9) | 🔥 Flame | 80 / 70 / 56 / 74 | *Crimson Meteor*, *Tempest Drive*, *Blaze Step*, *Gale Sweep*, *Phantom Barrage*, *Photon Laser*, *Hellfire Missile* |
| **Jin Kurogane** | Tetsuzan Academy | Libero (#5) | 🪨 Stone | 76 / 64 / 76 / 68 | *Tectonic Hammer*, *Shard Spiral*, *Granite Guard*, *Mirage Feint* |

### Goalkeepers

| Keeper | Team | Role | Element | Catch Stat | Signature Save |
| :--- | :--- | :--- | :---: | :---: | :--- |
| **Kaito Minase** | Akebono FC | Goalkeeper (#1) | 🌪️ Gale | 60 | *Tornado Wall* (Power: 52, TP: 30) |
| **Genta Iwaki** | Tetsuzan Academy | Goalkeeper (#1) | 🪨 Stone | 60 | *Bedrock Fortress* (Power: 54, TP: 32) |

---

## 🎮 Controls

### Desktop Keyboard & Mouse
* **Move**: `W` `A` `S` `D` or `Arrow Keys`
* **Shoot / Dash**: `Space` or `J`
  * *With ball*: Prepares and releases a shot toward the goal.
  * *Without ball*: Performs a high-speed dash tackle.
* **Duel Selection**: `1`, `2`, `3`, `4` or direct mouse click on move cards.
* **Skip Cutscenes**: `Space` or mouse click.
* **Engine Switching**: `T` (cycles between 32-Bit Arcade ➔ 64-Bit 3D ➔ 12-Bit Amiga).
* **Debug Tools**:
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

## 📁 Repository Structure

```
FOOTBALL/
├── Blaze vs Bedrock.html       # Primary complete single-file game bundle
├── Blaze vs Bedrock.backup.html# Baseline reference backup
├── build_12bit_version.py      # Build script for 12-bit Amiga retro quantization pipeline
├── generate_32bit_game.py      # Generator script uniting 32-bit, 12-bit, and 64-bit engines
├── check_file.py               # Quick validation and inspection utility
└── README.md                   # Project documentation and specifications
```

---

## 🗺️ Roadmap & Commercial Expansion

* [ ] **Clash Minigame**: Split-screen button mash/timing clash on tied rolls.
* [ ] **Roster Expansion**: Adding Thunder (⚡) and Frost (❄️) characters (Aoi, Raijin, Fubuki).
* [ ] **Roguelite Tournament Mode**: Single-player cup with artifact drafts and skill unlocks (*Balatro* x *Soccer*).
* [ ] **WebRTC Multiplayer**: 1-click room codes for instant peer-to-peer friend matches via WebRTC (PeerJS).
* [ ] **Gamepad Support**: Standard Gamepad API integration for Xbox, PlayStation, and 8BitDo controllers.
* [ ] **Steam & Portal Release**: Exporting for Poki / CrazyGames web portals and packaging for Steam via Tauri / Electron.
