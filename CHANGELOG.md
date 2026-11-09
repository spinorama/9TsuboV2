# Changelog — 9TsuboV2 (9-Tsubo House WebXR Project)

All notable versions, milestones, and UI/WebXR updates for the **9-Tsubo House (*Sumire Aoi House*, 1999 by Makoto Koizumi / Koizumi Studio)** 4-Mode WebXR architectural experience.

- **Repository:** [https://github.com/spinorama/9TsuboV2](https://github.com/spinorama/9TsuboV2)
- **Live WebXR App:** [https://spinorama.github.io/9TsuboV2/](https://spinorama.github.io/9TsuboV2/)

---

## [v0.4.0] — 2026-11-08
### Added
- **Subtle Hidden-Line CAD Render Mode (`✏️ Lines` / `[L]` Hotkey):**
  - Added architectural hidden-line rendering toggle in the top bar (and `[L]` keyboard shortcut on desktop).
  - Lazily constructs `THREE.EdgesGeometry` (`24°` crease threshold) with subtle graphite ink lines (`opacity: 0.42`) and depth-occluded warm-paper surface shading (`polygonOffset` enabled to prevent z-fighting while hiding back-edges behind walls, floors, and roofs; window glass remains translucent).
- **Version Changelog Tracking (`CHANGELOG.md` & In-App `📋 v0.4` Modal):**
  - Added `CHANGELOG.md` in GitHub documenting all versions of the 9-Tsubo House V2 effort.
  - Added a `📋 v0.4` button in the top bar opening an interactive version history modal styled in both DIN 1451 and Star Trek LCARS themes.

### Changed & Fixed
- **Phone 3D Navigation (Mode 1 — Single-Finger Orbit / Pinch-Zoom / Two-Finger Pan):**
  - Replaced first-person head-rotation on mobile touch screens with a true **1-finger 360° orbit**, **2-finger pinch-to-zoom**, and **2-finger pan** controller orbiting each preset viewpoint's focal pivot (`orbitTarget` / `orbitDist`).
  - Preserved Desktop browser mouse/keyboard controls (Left-drag look, Right-drag pan, Scroll wheel zoom, `WASD` / Arrow walk, `E`/`Q` elevation) unchanged.
- **Tabletop AR Overhaul (Mode 4 — Full Model + Context Extents & Pinch Scaling):**
  - Enabled both `Context_Group` and `Roof_Group` by default in Mode 4 so the entire neighborhood site and house are visible.
  - Fixed WebXR first-frame camera pose bug where `xrCam` was read prior to `renderer.render()` (which previously placed the model 8+ meters away). Mode 4 now reads `frame.getViewerPose(refSpace)` directly and computes `computeFitTabletopScale()` from the full `33.0m × 32.3m` bounding box so the entire model + context fits inside the phone viewport immediately on launch.
  - Added a dedicated `#ar-touch-surface` inside the WebXR `dom-overlay` with `beforexrselect` interception so **2-finger pinch zoom smoothly scales the model** (`0.2%` to `100%`) around its tabletop center and **1-finger drag rotates** it in place.
- **Preserved Mode 2 (VR) & Mode 3 (1:1 AR Walk):**
  - Kept Mode 3 (`📱 3 · 1:1 AR Walk`) and Mode 2 (`🥽 2 · Quest VR`) untouched.

---

## [v0.3.0] — 2026-11-04 (`6e7d113`)
### Added
- **Dual-Engine Graphic Design System (DIN 1451 vs. Star Trek LCARS):**
  - **Default Theme (`data-style="din"`):** German **DIN 1451** technical E-Ink paper specification UI with high-contrast `#050505` / `#ffffff` drafting borders and hard offset shadows.
  - **Alternate Theme (`data-style="lcars"`):** 24th-century **Star Trek LCARS** Okuda telemetry interface (`📐 Style` button or `[T]` hotkey) with swept elbow bars, pill terminals, and `#ff9900` / `#cc99cc` / `#5588ee` color coding.
  - **Procedural Web Audio Synthesizer:** Zero-dependency Web Audio API tactile feedback producing a mechanical typewriter click in DIN mode and a dual-frequency Starfleet chirp in LCARS mode.

### Changed
- Removed the floating instruction toast banner for an unobstructed viewport.
- Added initial multi-touch pinch-zoom and two-finger pan handlers.

---

## [v0.2.1] — 2026-11-04 (`2f81f26`)
### Changed
- Docked the instruction toast banner neatly underneath the top header bar and added an automatic 3-second fade-out timer.

---

## [v0.2.0] — 2026-11-04 (`37d86d8`, `ff13989`)
### Added
- **Updated Blender Architectural Model (`9_tsubo_house.glb`):**
  - Added 2F bedroom sliding window assembly (`Bed_SlidingWin_Frame`, `Bed_SlidingWin_SashL`, `Bed_SlidingWin_SashR`, `Bed_SlidingWin_Glass*`).
  - Added non-symmetrical tuxedo cat (`Ctx_Kitty_*`) perched on the neighboring house windowsill across from the 2F bedroom window.
  - Added exterior Japanese cherry blossom tree (`Ctx_Sakura_*`) alongside the front timber engawa deck.
  - Added preset cameras `Cam_13_Int_BedWindow_To_Kitty` and `Cam_14_Ext_RearWindow_And_Kitty`.
- **Quest VR Floor Point-and-Teleport (`vrTeleportReticle`):**
  - Added raycast floor intersection against all walkable surfaces (floors, tatami mats, engawa deck, stair treads, 2F loft, and street/ground) with a glowing cyan target ring reticle.

### Fixed
- Verified and calibrated all **13 preset camera world-space positions and `YXZ` Euler orientations** so the viewer never spawns inside geometry.
- Fixed mobile WebGL loading by disabling heavy 2048×2048 shadow maps on mobile GPUs and clamping device pixel ratio.
- Responsive `2×2` mode selector grid on mobile screens so all 4 WebXR modes (`3D View`, `Quest VR`, `1:1 AR Walk`, `Tabletop AR`) remain visible without horizontal scrolling.

---

## [v0.1.0] — 2026-11-02 (`ade8b05`)
### Added
- Initial release of the **9-Tsubo House (Koizumi Studio, 1999)** 3D Blender architectural model (`9_tsubo_house.glb`) organized into `House_Group`, `Roof_Group`, `Context_Group`, `Waypoints_Group`, and `Cameras_Group`.
- Initial single-file Three.js (`r170`) + WebXR application (`index.html`) supporting 4 viewing modes and live GitHub Pages deployment.
