# 9TsuboV2 — 4-Mode WebXR Experience

**Live Demo:** https://spinorama.github.io/9TsuboV2/

Interactive 3D / WebVR / WebAR architectural walkthrough of the **9-Tsubo House (*Sumire Aoi House*, 1999 by Makoto Koizumi / Koizumi Studio)**, built with Three.js (`r170`) and WebXR for **Desktop**, **Android Chrome (Pixel 10 Pro)**, and **Meta Quest Browser (Quest 3 & Quest Pro)**.

## 4 Viewing Modes (`index.html`)

1. **Mode 1 — Browser 3D Walk (`🖥️ 1 · 3D Walk`)**
   - Smooth first-person 360° mouse/touch look + **`WASD` / Arrow Keys** to walk, **`E`/`Space`** & **`Q`/`C`** to move up/down, **`Shift`** to sprint, and an on-screen **`🕹️ Move` Walk Pad** for mobile touch.
   - Smooth transitions between all **13 preset cameras/viewpoints** (`01 · Ext Three-Quarter`, `02 · Ext Front & Sakura`, `03 · Ext Front Elevation`, `04 · Sakura Engawa Deck`, `05 · Living & Kitchen`, `06 · Dining & Patio View`, `07 · 1F Tatami Room`, `08 · 1F Bathroom Suite`, `09 · 2F Loft & Columns`, `10 · 2F Loft Lounge`, `11 · 2F Bed → Kitty Win`, `12 · Tuxedo Kitty Close`, `13 · Aerial Overview`).
   - Quick toggle buttons for **`🏠 Roof`** (`Roof_Group`) and **`🌳 Context`** (`Context_Group`).

2. **Mode 2 — Full VR (`🥽 2 · Quest VR`)**
   - `immersive-vr` session using `local-floor` reference space with `renderer.xr.setFoveation(1.0)`.
   - **Floor Point-and-Teleport:** Aim your controller laser at any floor, tatami, engawa deck, stair tread, or 2F loft surface to show the glowing cyan target reticle (`vrTeleportReticle`), then pull **Trigger** or **Grip** to teleport directly there.
   - **Thumbstick Locomotion:** Left stick walks/strafes smoothly; Right stick snap-turns `45°`.
   - **Room Cycling & 3D VR HUD:** Press **`A`/`X`** or **`B`/`Y`** on Quest controllers (or click the floating 3D HUD panel with the laser pointer) to jump between rooms or toggle the roof cutaway.

3. **Mode 3 — 1:1 Scale AR Walkthrough (`📱 3 · 1:1 AR Walk` — Pixel 10 Pro)**
   - `immersive-ar` at true `1:1` scale (`scale(1, 1, 1)`) using `local` reference space and WebXR `dom-overlay`.
   - Anchors the active room's eye position directly to your phone's real-world pose on frame 1 so you can physically walk around the room at 1:1 scale, tap **`📍 Anchor / Place Here`** to recenter, or tap any room pill at the bottom to jump between rooms.

4. **Mode 4 — Tabletop Dollhouse AR (`🏡 4 · Tabletop AR` — Pixel 10 Pro & Quest Passthrough)**
   - `immersive-ar` architectural miniature model (`6%` default scale, adjustable with **`➖ Smaller`**, **`➕ Larger`**, and **`🔄 Rotate 45°`**).
   - Automatically hides `Roof_Group` and `Context_Group` so you can peer straight inside the 1F and 2F rooms.
   - Places the miniature house `0.75m` in front of you immediately on startup and uses WebXR `hit-test` (green surface reticle) so tapping any real-world table or floor snaps the dollhouse onto that surface.

## Scene Hierarchy (`9_tsubo_house.glb`)
- `Roof_Group` — Roof & ceiling lining (toggleable for dollhouse cutaway)
- `Context_Group` — Surrounding Japanese neighborhood houses, streets, utility poles, cherry blossom tree (`Ctx_Sakura_*`), and neighbor's window non-symmetrical tuxedo cat (`Ctx_Kitty_*`)
- `House_Group` — 9-Tsubo House structure, 1F/2F interiors, furniture, tatami room, 3-zone bathroom, 2F bedroom sliding window (`Bed_SlidingWin_*`), and timber engawa deck
- `Waypoints_Group` — Named `WP_01`–`WP_09` Empty nodes
- `Cameras_Group` — Exported Blender reference cameras (`Cam_01`–`Cam_14`)
