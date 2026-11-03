# 9TsuboHouseV2 — 4-Mode WebXR Experience

Interactive 3D / WebVR / WebAR architectural walkthrough of the **9-Tsubo House (*Sumire Aoi House* by Makoto Koizumi)**, built with Three.js (`r170`) and WebXR for **Android Chrome (Pixel 10 Pro)** and **Meta Quest Browser (Quest 3 & Quest Pro)**.

## Viewing Modes (`index.html`)

1. **Mode 1 — Browser 3D (`1 · Browser 3D`)**
   - Standard `OrbitControls` with smooth cubic-eased camera transitions between 10 preset room viewpoints (`Exterior Front`, `Sakura Deck`, `Living & Dining`, `Kitchen`, `Tatami Room`, `Bathroom`, `2F Loft Lounge`, `2F Bedroom`, `Kitty Window`, `Neighborhood Overview`).
   - Quick toggle buttons for `Roof: On/Off` (`Roof_Group`) and `Context: On/Off` (`Context_Group`).

2. **Mode 2 — Full VR (`2 · Full VR (Quest)`)**
   - `immersive-vr` session using `local-floor` reference space.
   - Left thumbstick: smooth walking with floor/stair raycast height tracking (`walkableMeshes`).
   - Right thumbstick: 45° snap turn.
   - Controller buttons: **`A` / `X`** or **Trigger** cycles to the next room; **`B` / `Y`** cycles to the previous room.
   - Includes an in-VR 3D HUD panel (`vrHudMesh`) with laser pointer raycasting to toggle the roof cutaway.

3. **Mode 3 — 1:1 Scale AR Walkthrough (`3 · 1:1 AR Walkthrough` — Pixel 10 Pro)**
   - `immersive-ar` at true `1:1` scale (`scale(1, 1, 1)`) with `dom-overlay`.
   - Anchors the active room's floor waypoint to your real-world floor position so you can physically walk around the room holding your phone and tap the on-screen room pills to jump between rooms.

4. **Mode 4 — Dollhouse Tabletop AR (`4 · Dollhouse AR` — Pixel 10 Pro & Quest Passthrough)**
   - `immersive-ar` with `hit-test` reticle placement at `0.05×` (`1:20`) miniature scale.
   - Automatically hides `Roof_Group` and `Context_Group` so you can peer straight inside the 1F and 2F rooms like a physical architectural model.

## Scene Hierarchy (`9_tsubo_house.glb`)
- `Roof_Group` — Roof & plywood ceiling lining
- `Context_Group` — Surrounding Japanese neighborhood houses, streets, utility poles, cherry blossom tree, and neighbor's window tuxedo kitty
- `House_Group` — 9-Tsubo House structure, 1F/2F interiors, furniture, tatami room, 3-zone bathroom, and timber deck
- `Waypoints_Group` — Named `WP_01`–`WP_09` Empty nodes at `1.6m` eye height
- `Cameras_Group` — Exported Blender reference cameras (`Cam_01`–`Cam_14`)
