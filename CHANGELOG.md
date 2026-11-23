# Changelog — 9TsuboV2 (9-Tsubo House WebXR, Apple USDZ & BIM Project)

All notable versions, milestones, Blender refinements, and WebXR/AR/BIM updates for the **9-Tsubo House (*Sumire Aoi House*, 1999 by Makoto Koizumi / Koizumi Studio)**.

- **Repository:** [https://github.com/spinorama/9TsuboV2](https://github.com/spinorama/9TsuboV2)
- **Live WebXR App:** [https://spinorama.github.io/9TsuboV2/](https://spinorama.github.io/9TsuboV2/)
- **Apple USDZ & Android AR Launcher:** [https://spinorama.github.io/9TsuboV2/ar.html](https://spinorama.github.io/9TsuboV2/ar.html)

---

## [v0.5.0] — 2026-11-22 (Tier 1: Lighting & PBR Refinement, Modeled Fixtures, Cleanup & Apple USDZ AR)
### Added
- **36 Modeled Koizumi Architectural Light Fixtures (`9_tsubo_house.blend` & `9_tsubo_house.glb`):**
  - Modeled low-poly, architecturally authentic Japanese lighting fixtures directly under `House_Group` (adding only `1,796` triangles, keeping `House_Group + Roof_Group` at `10,130 tris` and the full neighborhood scene at `56,538 tris`, strictly under the `60,000-tri` mobile/AR performance cap):
    - **`L-01A / L-01B` Dining & Living Cord Pendants** (`Fixture_Dining_Pendant_*`, `Fixture_Living_Pendant_*`) with sloped-ceiling canopies, matte cords, spun enamel conical shades, and frosted warm 2700K bulbs.
    - **`L-02` Kitchen Ceiling Duct Rail + 3 Directional Track Spots** (`Fixture_Kitchen_TrackRail`, `Fixture_Kitchen_Spot_1..3`).
    - **`L-03 / L-04` Tatami Room Hinoki-Framed Opal Shoji Ceiling Fixture & Linear Cove LED Bar** (`Fixture_Tatami_Ceiling*`, `Fixture_Tatami_Cove*`).
    - **`L-05` 2F Loft Ridge-Beam Duct Rail + 3 Directional Spots** (`Fixture_Loft_RidgeTrack`, `Fixture_Loft_Spot_1..3`).
    - **`L-06` 2F Bedroom Brass & Opal Wall Sconce** (`Fixture_Bed_Sconce*`).
    - **`L-07 / L-08` Bathroom Linear Vanity Opal Bar & 3 Wet-Rated Recessed Downlights** (`Fixture_Bath_VanityBar*`, `Fixture_Bath_*_Downlight*`).
    - **`L-09` Exterior Weatherproof Entrance Porch Sconce** (`Fixture_Entry_PorchSconce*`) mounted beneath `Entrance_Canopy`.
- **Native Apple iOS / iPadOS / visionOS AR Quick Look Support (`USDZ` + `ar.html`):**
  - Exported uncompressed Apple-compliant native `.usdz` packages straight from Blender 5.2 LTS (`Y`-up, `-Z` forward, `metersPerUnit=1.0`, `export_lights=False`):
    - [`assets/9_tsubo_house_1to1.usdz`](./assets/9_tsubo_house_1to1.usdz) (`278 KB`, `House_Group + Roof_Group` at true `1:1` real-world walk-in scale).
    - [`assets/9_tsubo_house_tabletop.usdz`](./assets/9_tsubo_house_tabletop.usdz) (`2.1 MB`, full site + neighborhood context pre-scaled to `1:50` architectural tabletop model `0.66m × 0.65m`).
  - Wired automatic Apple iOS/iPadOS Quick Look detection into Modes 3 (`1:1 AR`) and 4 (`Tabletop AR`) in `index.html`, and added dedicated cross-platform [`ar.html`](./ar.html) (`<model-viewer>` supporting WebXR, Google Scene Viewer, and Apple Quick Look with `1:50` / `1:1` toggle).
- **Lighting Mode Switcher (`💡 Light: Day / Warm / Soft`, Hotkey `[F]`):**
  - Anchored Three.js interior point lights to the exact modeled Blender fixture coordinates (capped to 3 active lights on mobile GPUs) and added automatic calibrated AR passthrough exposure (`0.76`) so real-world AR never blows out whites or birch plywood.
- **Verification Renders & Repository Hygiene:**
  - Added updated Cycles verification renders under [`renders/`](./renders/) (`01`–`04`), poster thumbnail [`assets/poster.png`](./assets/poster.png), root [`9_tsubo_house.blend`](./9_tsubo_house.blend), and `.gitignore`.

### Fixed & Refined
- **Eliminated Blown-Out AR & Interior Exposure:**
  - Physically calibrated 35 Blender PBR material albedos & roughness values (bringing near-1.0 clipping whites/plywood into realistic `0.50–0.79` linear reflectance and reducing `Shoji_Warm_Glow` emission from `2.4` down to `0.22`).
  - Recalibrated Blender interior lights (`12W–72W` inside modeled fixtures instead of floating `140W–320W` orbs) and disabled raw punctual light export in GLB/USDZ to prevent AR environment double-lighting.
  - Tuned Three.js `ACESFilmicToneMapping` exposure from `1.08` down to `0.88` (3D/VR) and `0.76` (AR passthrough), and balanced hemisphere/sun/fill intensities (`0.58 / 1.25 / 0.24`).
- **Geometry & Coplanar Z-Fighting Cleanup:**
  - Resolved coplanar mesh overlaps on `Bath_Wall_West_Vanity`, `Bed_Frame_Base`, `WinReveal_Wood_*`, `WinFrame_Outer_*`, `WinFrame_Center_Mullion`, `Bed_SlidingWin_ExtFrame_*`, `Loft_Rail_Top_*`, `Loft_Fascia_Beam_Rear`, and `Genkan_Shoe_*`.
  - Positioned all 9 `Waypoints_Group` empties (`WP_01`–`WP_09`) accurately at their corresponding room coordinates.

---

## [v0.4.0] — 2026-11-08 (`e7f9c1c`)
### Added
- **Subtle Hidden-Line CAD Render Mode (`✏️ Lines` / `[L]` Hotkey):**
  - Added architectural hidden-line rendering toggle in the top bar (and `[L]` keyboard shortcut on desktop).
  - Lazily constructs `THREE.EdgesGeometry` (`24°` crease threshold) with subtle graphite ink lines (`opacity: 0.42`) and depth-occluded warm-paper surface shading (`polygonOffset` enabled to prevent z-fighting while hiding back-edges behind walls, floors, and roofs; window glass remains translucent).
- **Version Changelog Tracking (`CHANGELOG.md` & In-App `📋 v0.4` Modal):**
  - Added `CHANGELOG.md` in GitHub documenting all versions of the 9-Tsubo House V2 effort.
  - Added a `📋` button in the top bar opening an interactive version history modal styled in both DIN 1451 and Star Trek LCARS themes.

### Changed & Fixed
- **Phone 3D Navigation (Mode 1 — Single-Finger Orbit / Pinch-Zoom / Two-Finger Pan):**
  - Replaced first-person head-rotation on mobile touch screens with a true **1-finger 360° orbit**, **2-finger pinch-to-zoom**, and **2-finger pan** controller orbiting each preset viewpoint's focal pivot (`orbitTarget` / `orbitDist`).
- **Tabletop AR Overhaul (Mode 4 — Full Model + Context Extents & Pinch Scaling):**
  - Enabled both `Context_Group` and `Roof_Group` by default in Mode 4 so the entire neighborhood site and house are visible, with automatic full-extent viewport fitting and smooth WebXR DOM-overlay 2-finger pinch zoom.

---

## [v0.3.0] — 2026-11-04 (`6e7d113`)
### Added
- **Dual-Engine Graphic Design System (DIN 1451 vs. Star Trek LCARS):**
  - Default German **DIN 1451** E-Ink technical specification UI toggleable with 24th-century **Star Trek LCARS** telemetry (`📐 Style` / `[T]`) and procedural Web Audio tactile sound effects.

---

## [v0.2.1] — 2026-11-04 (`2f81f26`)
### Changed
- Docked instruction toast banner under the top header bar with automatic 3-second fade-out (streamlined out in v0.3.0).

---

## [v0.2.0] — 2026-11-04 (`37d86d8`, `ff13989`)
### Added & Fixed
- Updated `9_tsubo_house.glb` with 2F sliding bedroom window (`Bed_SlidingWin_*`), non-symmetrical tuxedo cat (`Ctx_Kitty_*`), and cherry blossom tree (`Ctx_Sakura_*`).
- Added Quest VR floor point-and-teleport reticle (`vrTeleportReticle`), verified all 13 preset cameras, and added responsive `2×2` mobile mode grid.

---

## [v0.1.0] — 2026-11-02 (`ade8b05`)
### Added
- Initial release of the **9-Tsubo House (Koizumi Studio, 1999)** 3D Blender architectural model (`9_tsubo_house.glb`) and 4-Mode WebXR experience (`index.html`).
