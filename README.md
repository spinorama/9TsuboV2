# 9TsuboV2 — 4-Mode WebXR Architectural Experience

- **Live Demo:** [https://spinorama.github.io/9TsuboV2/](https://spinorama.github.io/9TsuboV2/)
- **Changelog:** [CHANGELOG.md](./CHANGELOG.md) (current version: **`v0.4.0`**)

Interactive 3D / WebVR / WebAR architectural walkthrough of the **9-Tsubo House (*Sumire Aoi House*, 1999 by Makoto Koizumi / Koizumi Studio)**, built with Three.js (`r170`) and WebXR for **Desktop**, **Android Chrome (Pixel 10 Pro)**, and **Meta Quest Browser (Quest 3 & Quest Pro)**.

---

## 4 Viewing Modes (`index.html`)

1. **Mode 1 — Browser 3D View (`🖥️ 1 · 3D View`)**
   - **Phone / Mobile Touch:** True **1-finger 360° orbit**, **2-finger pinch-to-zoom**, and **2-finger pan** around each viewpoint's focal pivot.
   - **Desktop Mouse & Keyboard:** Left-click drag to look (`360°`), Right-click / Middle-click / `Shift`+drag to pan, Scroll wheel to zoom, **`WASD` / Arrow Keys** to walk, **`E`/`Space`** & **`Q`/`C`** to move up/down, and **`Shift`** to sprint.
   - Smooth transitions between all **13 preset cameras/viewpoints** (`01 · Ext Three-Quarter`, `02 · Ext Front & Sakura`, `03 · Ext Front Elevation`, `04 · Sakura Engawa Deck`, `05 · Living & Kitchen`, `06 · Dining & Patio View`, `07 · 1F Tatami Room`, `08 · 1F Bathroom Suite`, `09 · 2F Loft & Columns`, `10 · 2F Loft Lounge`, `11 · 2F Bed → Kitty Win`, `12 · Tuxedo Kitty Close`, `13 · Aerial Overview`).
   - Quick header toggles for **`🏠 Roof`** (`Roof_Group`), **`🌳 Context`** (`Context_Group`), **`✏️ Lines`** (Subtle Hidden-Line CAD render mode, hotkey **`[L]`**), **`📐 Style`** (German **DIN 1451** technical E-Ink paper vs. **Star Trek LCARS** telemetry UI, hotkey **`[T]`**), and **`📋 v0.4`** (in-app Changelog viewer).

2. **Mode 2 — Full VR (`🥽 2 · Quest VR`)**
   - `immersive-vr` session using `local-floor` reference space with `renderer.xr.setFoveation(1.0)`.
   - **Floor Point-and-Teleport:** Aim your controller laser at any floor, tatami, engawa deck, stair tread, or 2F loft surface to show the glowing cyan target reticle (`vrTeleportReticle`), then pull **Trigger** or **Grip** to teleport directly there.
   - **Thumbstick Locomotion:** Left stick walks/strafes smoothly; Right stick snap-turns `45°`.
   - **Room Cycling & 3D VR HUD:** Press **`A`/`X`** or **`B`/`Y`** on Quest controllers (or click the floating 3D HUD panel with the laser pointer) to jump between rooms or toggle the roof cutaway.

3. **Mode 3 — 1:1 Scale AR Walkthrough (`📱 3 · 1:1 AR Walk` — Pixel 10 Pro)**
   - `immersive-ar` at true `1:1` scale (`scale(1, 1, 1)`) using `local` reference space and WebXR `dom-overlay`.
   - Anchors the active room's eye position directly to your phone's real-world pose on frame 1 so you can physically walk around the room at 1:1 scale, tap **`📍 Anchor / Place`** to recenter, or tap any room pill at the bottom to jump between rooms.

4. **Mode 4 — Tabletop AR (`🏡 4 · Tabletop AR` — Pixel 10 Pro & Quest Passthrough)**
   - Displays the **entire model including the neighborhood `Context_Group` and `Roof_Group`**, automatically scaled on launch so the full `33m × 32.3m` site extents fit inside your phone screen (`~0.85m` in front of you).
   - **Simple 2-Finger Pinch Zoom** smoothly scales the model smaller or larger (`0.2%` to `100%`) around its center; **1-finger drag** rotates the model in place.
   - Uses WebXR `hit-test` (green surface reticle) so tapping a detected real-world table/floor (or tapping **`📍 Anchor / Place`**) snaps the model onto that surface.

---

## Version History Summary

See **[CHANGELOG.md](./CHANGELOG.md)** for full details:

- **`v0.4.0` (2026-11-08):** Phone 1-finger orbit / 2-finger pinch zoom & pan; Tabletop AR full-model + context extent auto-scaling and reliable WebXR DOM-overlay pinch scaling; subtle Hidden-Line CAD render mode (`✏️ Lines` / `[L]`); GitHub `CHANGELOG.md` and in-app `📋 v0.4` modal.
- **`v0.3.0` (2026-11-04):** Dual-Engine Graphic Design System — German DIN 1451 E-Ink technical specification UI (default) and Star Trek LCARS mode (`[T]`) with procedural Web Audio synthesizer sound effects.
- **`v0.2.1` (2026-11-04):** Docked instruction toast banner with auto-fade timer.
- **`v0.2.0` (2026-11-04):** Updated `9_tsubo_house.glb` with 2F sliding window (`Bed_SlidingWin_*`), non-symmetrical tuxedo cat (`Ctx_Kitty_*`), and cherry blossom tree (`Ctx_Sakura_*`); verified all 13 preset cameras, VR floor teleportation, and mobile AR UI.
- **`v0.1.0` (2026-11-02):** Initial 9-Tsubo House 4-Mode WebXR experience and Blender GLB export.

---

## Scene Hierarchy (`9_tsubo_house.glb`)
- `Roof_Group` — Roof & ceiling lining (toggleable for dollhouse cutaway)
- `Context_Group` — Surrounding Japanese neighborhood houses, streets, utility poles, cherry blossom tree (`Ctx_Sakura_*`), and neighbor's window non-symmetrical tuxedo cat (`Ctx_Kitty_*`)
- `House_Group` — 9-Tsubo House structure, 1F/2F interiors, furniture, tatami room, 3-zone bathroom, 2F bedroom sliding window (`Bed_SlidingWin_*`), and timber engawa deck
- `Waypoints_Group` — Named `WP_01`–`WP_09` Empty nodes
- `Cameras_Group` — Exported Blender reference cameras (`Cam_01`–`Cam_14`)
