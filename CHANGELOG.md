# Changelog — 9TsuboV2 (9-Tsubo House WebXR, Apple USDZ, IFC4 BIM & Construction Drawings)

All notable versions, Blender refinements, WebXR/AR/USDZ releases, and BIM drawing milestones for the **9-Tsubo House (*Sumire Aoi House*, 1999 by Makoto Koizumi / Koizumi Studio)**.

- **Repository:** [https://github.com/spinorama/9TsuboV2](https://github.com/spinorama/9TsuboV2)
- **Live 4-Mode WebXR App (Anime Default):** [https://spinorama.github.io/9TsuboV2/](https://spinorama.github.io/9TsuboV2/) ([🏛️ PBR Mode](https://spinorama.github.io/9TsuboV2/?pbr=1) · [🏡 Tabletop Diorama](https://spinorama.github.io/9TsuboV2/?tabletop=1))
- **ISO 19650 / IFC4 BIM Viewer:** [https://spinorama.github.io/9TsuboV2/bim.html](https://spinorama.github.io/9TsuboV2/bim.html)
- **12-Sheet Construction Drawing Binder:** [https://spinorama.github.io/9TsuboV2/drawings/index.html](https://spinorama.github.io/9TsuboV2/drawings/index.html)
- **Apple USDZ & Android AR Launcher:** [https://spinorama.github.io/9TsuboV2/ar.html](https://spinorama.github.io/9TsuboV2/ar.html)

---

## [v1.2.0] — 2026-11-23 (Anime Default, Non-AR Tabletop Diorama, Mobile Orbit/Walk Toggle & Overhauled VR/AR Locomotion)
### Changed & Added
- **Japanese Summer Anime Default & Clean DIN 1451 UI:**
  - Japanese Summer Anime Mode (cel-shading, architectural + organic ink outlines, and procedural cumulus sky) is now **ON by default** on initial load (toggle back to Architectural PBR with `🌸 Anime` / `[V]` or `?pbr=1` / `?anime=0`).
  - Completely removed the legacy LCARS UI option, CSS theme, `[T]` hotkey, and audio chirp; standardized on clean German **DIN 1451** Technical E-Ink Paper styling.
- **Contextual Non-AR Tabletop Diorama Toggle (`🏡 Tabletop` / Hotkey `[M]` & VR 3D HUD button):**
  - Keeps the 4-Mode selector strictly 4 views while offering a contextual exhibition-plinth maquette toggle inside **Desktop 3D**, **Mobile 3D**, and **Meta Quest VR** (auto-hidden in AR Modes 3 & 4).
  - Features a stepped architectural plinth dynamically fitted to either the **Full Site** (`33m × 32m`) or **House Maquette** (`~9m × 8.5m`), turntable **Auto-Spin**, **Cutaway Roof**, **Full Site / House Only** toggle, pitch-clamped exhibition orbit, and waist-high interactive VR miniature manipulation.
- **Mobile & Desktop Orbit ↔ First-Person Walk Toggle (`🔄 Nav: Orbit` ↔ `🚶 Nav: Walk` / Hotkey `[N]`):**
  - Mobile/touch users can now switch seamlessly between **360° Orbit** and **First-Person Walk** featuring a tactile bottom-left analog virtual joystick (independent multi-touch ID so you can walk with your left thumb and drag-look with your right thumb simultaneously) plus a bottom-right `▲ UP / ▼ DN / ↺ 30° / ↻ 30°` elevation & turn pad.
  - Desktop users also gain true Orbit vs. First-Person Walk mouse/wheel switching.
- **Overhauled Meta Quest VR & Android WebXR AR Interactive Movement:**
  - **Non-Escapable Quest VR 3D HUD:** Moved from `rig` into world-space with an expanded 2-row × 4-button DIN 1451 command panel, live 3D laser cursor dot & button hover states, **Auto-Follow Guard** (smoothly glides back into view when walking or turning away), and instant summon/re-center via **`Y`/`B`** or **Thumbstick Click**.
  - **Parabolic Teleport Arc & Step-Following:** Upgraded VR teleport to a 24-segment gravity parabola colliding against all visible opaque meshes (excluding hidden roof/context groups), with headset XZ offset compensation so your physical feet land directly on the reticle, multi-runtime thumbstick auto-detection (`axes[2,3]` vs `axes[0,1]`), smooth deck/stair step-climbing raycast, and head-centered `30°` snap turning.
  - **1:1 AR Walk (`Mode 3`):** Added on-screen touch virtual joystick, `▲/▼` elevation climbing, head-aligned room anchoring (faces the chosen viewpoint immediately), and viewer-centered turning.
  - **Tabletop AR (`Mode 4`):** Eliminated accidental WebXR `selectstart` model jumps, added **2-finger spatial pan/lift** alongside 1-finger spin & 2-finger pinch scale, plus explicit `⬆️ Raise` / `⬇️ Lower` / `📍 Place on Surface` controls.

---

## [v1.1.0] — 2026-11-22 (Real-Time WebXR Japanese Summer Anime Mode & 24-View Render Gallery)
### Added
- **Live WebXR Japanese Summer Anime Toggle (`index.html` — `🌸 Anime` button, Hotkey `[V]`, Quest VR 3D HUD button & `?anime=1` URL parameter):**
  - Works seamlessly across all 4 WebXR modes: **Desktop 3D**, **Meta Quest VR**, **1:1 AR Walk**, and **Tabletop Dollhouse AR** (including live Tabletop rotation/scale-synced sun & procedural shaders, plus automatic sky-dome hiding for transparent AR passthrough).
  - **Studio-Calibrated 85-Material Cel Shader Suite:** Exact warm pastel cream vs. cool cerulean shadow palettes matching the finalized Blender v2.1 anime renders, smooth painterly wood & white interiors (zero point-light bullseyes), smooth-normal Makoto Shinkai pastel Sakura & lush summer foliage, procedural terracotta *kawara* clay roof ribs, and turquoise windows with diagonal glare slashes.
  - **Dual-System Real-Time Ink Outlines:** Crisp `#141d2b` architectural edge lines + subtle `#3a5575` paver/panel seams + watertight inverted-hull organic ink silhouettes on the Sakura tree, foliage canopies, Tuxedo Kitty, and bedside opal sconce globe.
  - **Procedural Makoto Shinkai Summer Sky Dome:** Electric cyan summer sky gradient with gently drifting 3-step cel-shaded towering cumulus clouds and distant misty turquoise horizon mountains.
- **24-View Architectural PBR vs. Japanese Summer Anime Render Gallery (`renders/current/`, `renders/anime/`, `README.md`):**
  - All 12 perspective cameras rendered at `1280×720` in both Cycles GPU (`OPTIX`, AgX) and EEVEE + 3-Pass Freestyle Ink + Mist/Glare Compositor.

---

## [v1.0.0] — 2026-11-22 (Tier 2: BIMCraft-Style Automated Drawing Pipeline, 12-Sheet CAD Set & IFC4 BIM Viewer)
### Added
- **BIMCraft-Style Automated Model-to-Drawing Pipeline (`scripts/`):**
  - [`scripts/extract_bim_metadata.py`](./scripts/extract_bim_metadata.py) — Extracts exact world-space geometry, areas, volumes, triangle counts, deterministic IFC4 `GlobalId`s, CSI MasterFormat 2020 trades, Uniformat II, Uniclass 2015, and multi-layer **LOD-400 Construction Assemblies** (`W-EXT-01`, `W-INT-01`, `RF-01`, `FND-01`, `FL-1F-01`, `FL-2F-01`, `GLZ-01`, `DK-01`, `STR-01`, `LGT-01`) for all `893` mesh elements into [`9_tsubo_bim_metadata.json`](./9_tsubo_bim_metadata.json).
  - [`scripts/cad_engine.py`](./scripts/cad_engine.py) — Core 3D-to-2D architectural vector engine implementing true `bmesh.ops.bisect_plane` cross-section slicing with closed poché loops + depth-sorted orthographic hidden-face projection + architectural CAD hatch library (`hatch-concrete`, `hatch-gravel`, `hatch-earth`, `hatch-wall-cut`, `hatch-xps`, `hatch-plywood`, `hatch-wood`, `hatch-steel`, `hatch-tatami`) and sinusoidal mineral-wool batt insulation generator.
  - [`scripts/generate_sheets_part1.py`](./scripts/generate_sheets_part1.py) & [`scripts/generate_sheets_part2.py`](./scripts/generate_sheets_part2.py) — Automatically generate all **12 ARCH D / ISO A1 (`1920×1280`) Vector SVG Construction Sheets** (`A-000`–`A-601`) directly from `9_tsubo_house.blend`, honoring the `≤ 60,000`-triangle mobile/AR 3D cap while automatically detailing full LOD-400 assemblies in 2D.
- **12-Sheet Model-Derived Architectural Construction Drawing Set ([`drawings/index.html`](./drawings/index.html)):**
  - `A-000` Cover Sheet, Drawing Index, Model-Projected Axonometric & Hybrid LOD-300/400 Pipeline Spec
  - `A-100` Site & Neighborhood Context Plan (`1:100`, parcel setbacks, Sakura tree & Tuxedo Kitty sightline)
  - `A-101` First Floor Plan (`1:50`, `bmesh` cut @ `EL +1.250m`, 3-tier dimensions, `1820mm` ken grid, room/door/window tags)
  - `A-102` Second Floor Loft & Mezzanine Plan (`1:50`, `bmesh` cut @ `EL +3.550m`, open-to-below void, `W-02` sliding window)
  - `A-103` Roof Drainage Plan & *Zairai-koho* Structural Timber Framing Plan (`1:50`, `105×105` Hinoki posts, `Ø176` cedar columns, girders, ridge beam & joists)
  - `A-104` 1F & 2F Reflected Ceiling & Architectural Lighting Plan (`1:50`, all 36 modeled fixtures `L-01`–`L-09`, switch legs & luminaire schedule)
  - `A-201` All 4 Exterior Elevations (`1:50`, South, West, North & East true orthographic 3D projections w/ datums & roof pitch triangles)
  - `A-301` Building Sections A-A (East–West) & B-B (North–South) (`1:50`, true `bmesh` cuts + below-grade RC footings + detail bubbles)
  - `A-401` Enlarged `1:25` Kitchen, 3-Zone Bathroom Suite & Tatami Plans + Interior Elevations
  - `A-501` LOD-400 Wall Section (`1:15`) & Envelope Construction Details (`1:10`: RC Plinth/Footing/Anchor Bolt/Engawa Pier, Vented South Eave & Gutter, Ridge Beam/Cedar Column Steel Knife-Plate Cap & Track Mount)
  - `A-502` LOD-400 Glazing, Stair & Guardrail Details (`1:8` 2-Story Shoji & Aluminum Curtain Wall, `1:5` `W-02` Sliding Window Head/Sill Flashing, `1:10` Open-Riser Timber Stair & Loft Ledger, `1:10` Loft Rim Beam & Tensioned Stainless Cable Guardrail)
  - `A-601` Automated Architectural Schedules (Door, Window/Shoji, Room Finish) + IFC4 Performance Cap Audit & CSI MasterFormat 2020 Quantity Take-Off
- **Dedicated ISO 19650-2 / IFC4 BIM Coordination Viewer ([`bim.html`](./bim.html)):**
  - Interactive 3D federation viewer with calibrated lighting, Spatial Tree (`BLDG-01`, `SITE-01`, `CTX-01`), Storeys (`L00`–`L03`), IFC4 & CSI MasterFormat filters, 6 federation color modes, 6-plane Section Box (`1F Plan`, `2F Plan`, `Section A-A`, `Section B-B`), 3D Laser Tape Measure (`mm` / `ft-in` / Japanese `ken`), Right-Docked IFC4 + **LOD-400 Construction Assembly Inspector**, instant 2D CAD Sheet preview modal, searchable BOQ spreadsheet, and `.IFC` / `.CSV` exports.

---

## [v0.5.0] — 2026-11-22 (`cbb53a6` — Tier 1: Lighting & PBR Refinement, Modeled Fixtures, Cleanup & Apple USDZ AR)
### Added & Fixed
- **36 Modeled Koizumi Architectural Light Fixtures** (`1,796 tris`, keeping `House_Group + Roof_Group` at `10,130 tris` and full scene at `56,538 tris ≤ 60k cap`).
- **Eliminated Blown-Out AR & 3D Lighting:** Calibrated all 35 Blender PBR material albedos & emissives (`Shoji_Warm_Glow` `2.4 → 0.22`), anchored Three.js point lights to actual fixture coordinates, added `💡 Light: Day / Warm / Soft` (`[F]`) and calibrated WebXR AR passthrough exposure (`0.76`).
- **Geometry Cleanup:** Resolved coplanar Z-fighting overlaps across bath walls, bed frame, front window reveals/frames, loft rails, and stairs; calibrated `WP_01`–`WP_09` waypoint positions.
- **Native Apple iOS / iPadOS / visionOS USDZ Support:** Exported `assets/9_tsubo_house_1to1.usdz` (`278 KB`) and `assets/9_tsubo_house_tabletop.usdz` (`2.11 MB`), integrated Apple Quick Look into Modes 3 & 4, and added cross-platform [`ar.html`](./ar.html).

---

## [v0.4.0] — 2026-11-08 (`e7f9c1c`)
- Phone 1-finger 360° orbit / 2-finger pinch zoom & pan; Tabletop AR full-extent auto-scaling & pinch scaling; subtle Hidden-Line CAD render mode (`✏️ Lines` / `[L]`); `CHANGELOG.md`.

## [v0.3.0] — 2026-11-04 (`6e7d113`)
- Dual-Engine Graphic Design System: German **DIN 1451** E-Ink paper (default) toggleable with **Star Trek LCARS** (`[T]`) + Web Audio synthesizer.

## [v0.2.0] — 2026-11-04 (`37d86d8`)
- Added 2F bedroom sliding window (`Bed_SlidingWin_*`), non-symmetrical tuxedo cat (`Ctx_Kitty_*`), cherry blossom tree (`Ctx_Sakura_*`), and Quest VR floor teleportation reticle.

## [v0.1.0] — 2026-11-02 (`ade8b05`)
- Initial 9-Tsubo House Blender model and 4-Mode WebXR experience.
