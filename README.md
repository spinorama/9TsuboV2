# 9TsuboV2 — WebXR, Apple USDZ, ISO 19650 BIM & 12-Sheet Model-Derived Architectural Drawing Set

Complete architectural digital twin of the **9-Tsubo House (*Sumire Aoi House*, 1999 by Makoto Koizumi / Koizumi Studio — after Makoto Masuzawa's 1952 Minimum House)** featuring a calibrated **4-Mode WebXR Experience**, **Native Apple iOS USDZ & Android AR**, an **ISO 19650 / IFC4 BIM Coordination Viewer**, and a **12-Sheet Model-Derived Construction Drawing Set (`A-000`–`A-601`)** automatically sliced and projected from Blender (`v1.0.0`).

---

## 🚀 Live Interactive Deliverables

| Deliverable | Live URL / Path | Key Capabilities |
| :--- | :--- | :--- |
| **1. 4-Mode WebXR Experience** | [**`index.html`**](https://spinorama.github.io/9TsuboV2/) · [**🌸 Anime Mode**](https://spinorama.github.io/9TsuboV2/?anime=1) | Desktop 3D (`WASD`+mouse), Mobile 1-finger orbit/pinch, Quest VR teleport + 3D HUD, Android 1:1 & Tabletop WebXR, Apple iOS Quick Look USDZ auto-launch, **🌸 Japanese Summer Anime Mode (`[V]`)**, `💡 Light` (`[F]`), Hidden-Line (`[L]`), `DIN 1451 / LCARS` (`[T]`) |
| **2. ISO 19650 / IFC4 BIM Viewer** | [**`bim.html`**](https://spinorama.github.io/9TsuboV2/bim.html) | `893` IFC4 elements (`9_tsubo_bim_metadata.json`) · CSI MasterFormat 2020 trade filters · 6-Plane Section Box · Laser Tape Measure (`mm` / `ft-in` / `ken`) · **LOD-400 Multi-Layer Assembly Inspector** · Live `.IFC` & `.CSV` BOQ export |
| **3. 12-Sheet Construction Drawing Binder** | [**`drawings/index.html`**](https://spinorama.github.io/9TsuboV2/drawings/index.html) | Interactive pan/zoom/print-to-PDF binder for **12 Vector SVG Architectural Sheets (`A-000`–`A-601`)** automatically derived from `9_tsubo_house.blend` via `bmesh` slicing & orthographic projection |
| **4. Dedicated Apple & Android AR Launcher** | [**`ar.html`**](https://spinorama.github.io/9TsuboV2/ar.html) | Cross-platform `<model-viewer>` AR page with `1:50` Tabletop & `1:1` Walk-In toggle, native Apple `.usdz` Quick Look links & Android ARCore Scene Viewer fallback |
| **5. Automated BIM-to-CAD Scripts** | [`scripts/`](./scripts/) | Reproducible Blender 5.2 LTS Python pipeline ([`extract_bim_metadata.py`](./scripts/extract_bim_metadata.py), [`cad_engine.py`](./scripts/cad_engine.py), [`generate_sheets_part1.py`](./scripts/generate_sheets_part1.py), [`generate_sheets_part2.py`](./scripts/generate_sheets_part2.py)) |

---

## ⚡ Hybrid Mobile/AR Performance Budget (`LOD-300 3D → LOD-400 2D`)

Following the **BIMCraft** automated model-to-drawing philosophy, 3D geometry stays strictly capped for instant mobile & AR performance (`≤ 60,000` triangles total), while structural framing, flashing, rebar, cavity insulation, and joinery assemblies are driven parametrically from the BIM model into crisp 2D LOD-400 construction drawings:

| Asset | Scope | Triangles | File Size | Platform |
| :--- | :--- | ---: | ---: | :--- |
| [`9_tsubo_house.glb`](./9_tsubo_house.glb) | Full House + Roof + 36 Modeled Fixtures + Neighborhood Context | `56,538 tris` | `2.33 MB` | Desktop 3D, Quest VR, Android WebXR, BIM Viewer |
| [`assets/9_tsubo_house_1to1.usdz`](./assets/9_tsubo_house_1to1.usdz) | House + Roof + Fixtures (`1:1` True Walk-In Scale) | `10,130 tris` | `278 KB` | Apple iPhone / iPad / Vision Pro Quick Look (`1:1`) |
| [`assets/9_tsubo_house_tabletop.usdz`](./assets/9_tsubo_house_tabletop.usdz) | Full Site + Context (`1:50` Architectural Tabletop `0.66m × 0.65m`) | `56,538 tris` | `2.11 MB` | Apple iPhone / iPad / Vision Pro Quick Look (Tabletop) |
| [`assets/9_tsubo_house_1to1.glb`](./assets/9_tsubo_house_1to1.glb) | House + Roof + Fixtures (`1:1` Scale) | `10,130 tris` | `792 KB` | Android `<model-viewer>` / ARCore Scene Viewer |
| [`assets/9_tsubo_house_tabletop.glb`](./assets/9_tsubo_house_tabletop.glb) | Full Site + Context (`1:50` Tabletop) | `56,538 tris` | `2.32 MB` | Android `<model-viewer>` / ARCore Scene Viewer |

---

## 📐 12-Sheet Model-Derived Construction Drawing Set ([`drawings/`](./drawings/index.html))

1. **[`A-000_Cover_Index.svg`](./drawings/A-000_Cover_Index.svg)** — Cover Sheet, Drawing Index, Model-Projected Axonometric, Project Data & Hybrid LOD-300/400 Pipeline Spec
2. **[`A-100_Site_Context_Plan.svg`](./drawings/A-100_Site_Context_Plan.svg)** — Site & Neighborhood Context Plan (`1:100`, parcel setbacks, Sakura tree & Tuxedo Kitty sightline)
3. **[`A-101_First_Floor_Plan.svg`](./drawings/A-101_First_Floor_Plan.svg)** — First Floor Plan (`1:50`, `bmesh` cut @ `EL +1.250m`, `3×3 ken` grid, 3-tier dimensions, room/door/window tags)
4. **[`A-102_Second_Floor_Loft_Plan.svg`](./drawings/A-102_Second_Floor_Loft_Plan.svg)** — Second Floor Loft & Mezzanine Plan (`1:50`, `bmesh` cut @ `EL +3.550m`, double-height void & `W-02` sliding window)
5. **[`A-103_Roof_Structural_Framing_Plan.svg`](./drawings/A-103_Roof_Structural_Framing_Plan.svg)** — Roof Drainage Plan & *Zairai-koho* Structural Timber Framing Plan (`1:50`)
6. **[`A-104_Reflected_Ceiling_Lighting_Plan.svg`](./drawings/A-104_Reflected_Ceiling_Lighting_Plan.svg)** — 1F & 2F Reflected Ceiling & Architectural Lighting Plan (`1:50`, all 36 modeled fixtures `L-01`–`L-09` & luminaire schedule)
7. **[`A-201_Exterior_Elevations.svg`](./drawings/A-201_Exterior_Elevations.svg)** — Exterior Elevations (`1:50`, South, West, North & East true orthographic 3D projections)
8. **[`A-301_Building_Sections.svg`](./drawings/A-301_Building_Sections.svg)** — Building Sections A-A (E–W) & B-B (N–S) (`1:50`, `bmesh` cuts + below-grade RC footings + detail callouts)
9. **[`A-401_Enlarged_Interior_Plans_Elevations.svg`](./drawings/A-401_Enlarged_Interior_Plans_Elevations.svg)** — Enlarged `1:25` Kitchen, 3-Zone Bathroom Suite & Tatami Plans + Interior Elevations
10. **[`A-501_Wall_Section_Envelope_Details.svg`](./drawings/A-501_Wall_Section_Envelope_Details.svg)** — Typical Full-Height Wall Section (`1:15`) & Foundation Plinth/Engawa Pier, Vented Eave/Gutter & Ridge Beam/Column Cap Details (`1:10`)
11. **[`A-502_Glazing_Stair_Guardrail_Details.svg`](./drawings/A-502_Glazing_Stair_Guardrail_Details.svg)** — 2-Story Shoji Curtain Wall (`1:8`), `W-02` Sliding Window Flashing (`1:5`), Open-Riser Stair Stringer (`1:10`) & Cable Guardrail (`1:10`) Details
12. **[`A-601_Schedules_BIM_QTO.svg`](./drawings/A-601_Schedules_BIM_QTO.svg)** — Door, Window/Shoji & Room Finish Schedules + IFC4 Performance Cap Audit & CSI MasterFormat 2020 Quantity Take-Off

---

## 📸 All-Camera Render Gallery — Architectural PBR vs. Japanese Summer Anime

All **12 perspective cameras** rendered at `1280×720` in both **Architectural PBR** (`Cycles GPU / OPTIX`, AgX, calibrated modeled fixtures — [`renders/current/`](./renders/current/)) and **Japanese Summer Anime Style** (`EEVEE` + 3-pass Freestyle ink + Mist/Fog-Glow compositor, sculpted foliage & Sakura, terracotta *kawara* roofs, towering summer cumulus sky — [`renders/anime/`](./renders/anime/)).

### Exterior & Neighborhood Context
| Camera | Architectural PBR (`Cycles`) | Japanese Summer Anime (`EEVEE + Freestyle`) |
| :--- | :---: | :---: |
| **01. Three-Quarter Street** (`Cam_01`) | ![Cam 01 PBR](./renders/current/01_Cam_01_Ext_ThreeQuarter.png) | ![Cam 01 Anime](./renders/anime/01_Cam_01_Ext_ThreeQuarter.png) |
| **02. Front Low-Angle & Deck** (`Cam_02`) | ![Cam 02 PBR](./renders/current/02_Cam_02_Ext_FrontLowAngle.png) | ![Cam 02 Anime](./renders/anime/02_Cam_02_Ext_FrontLowAngle.png) |
| **04. South Elevation & Sakura** (`Cam_04`) | ![Cam 04 PBR](./renders/current/04_Cam_04_Ext_FrontElevation.png) | ![Cam 04 Anime](./renders/anime/04_Cam_04_Ext_FrontElevation.png) |
| **10. Aerial Context Overview** (`Cam_12`) | ![Cam 12 PBR](./renders/current/10_Cam_12_Context_Overview.png) | ![Cam 12 Anime](./renders/anime/10_Cam_12_Context_Overview.png) |

### Interior Architecture & Fixtures
| Camera | Architectural PBR (`Cycles`) | Japanese Summer Anime (`EEVEE + Freestyle`) |
| :--- | :---: | :---: |
| **03. Kitchen, Pendant & Loft** (`Cam_03`) | ![Cam 03 PBR](./renders/current/03_Cam_03_Int_KitchenAndLoft.png) | ![Cam 03 Anime](./renders/anime/03_Cam_03_Int_KitchenAndLoft.png) |
| **05. 2F Loft Lounge & Bed** (`Cam_05`) | ![Cam 05 PBR](./renders/current/05_Cam_05_Int_LoftLoungeAndBed.png) | ![Cam 05 Anime](./renders/anime/05_Cam_05_Int_LoftLoungeAndBed.png) |
| **06. High-Angle Dining & Deck** (`Cam_06`) | ![Cam 06 PBR](./renders/current/06_Cam_06_Int_HighAngleDiningKitchen.png) | ![Cam 06 Anime](./renders/anime/06_Cam_06_Int_HighAngleDiningKitchen.png) |
| **07. Loft to Bed & Stairs** (`Cam_07`) | ![Cam 07 PBR](./renders/current/07_Cam_07_Int_LoftToBedAndStairs.png) | ![Cam 07 Anime](./renders/anime/07_Cam_07_Int_LoftToBedAndStairs.png) |
| **08. 1F Tatami Room** (`Cam_08`) | ![Cam 08 PBR](./renders/current/08_Cam_08_Int_TatamiRoom.png) | ![Cam 08 Anime](./renders/anime/08_Cam_08_Int_TatamiRoom.png) |
| **09. Bathroom Suite** (`Cam_09`) | ![Cam 09 PBR](./renders/current/09_Cam_09_Int_Bathroom.png) | ![Cam 09 Anime](./renders/anime/09_Cam_09_Int_Bathroom.png) |

### Neighbor's Tuxedo Kitty Sightlines
| Camera | Architectural PBR (`Cycles`) | Japanese Summer Anime (`EEVEE + Freestyle`) |
| :--- | :---: | :---: |
| **11. Bed Window to Kitty** (`Cam_13`) | ![Cam 13 PBR](./renders/current/11_Cam_13_Int_BedWindow_To_Kitty.png) | ![Cam 13 Anime](./renders/anime/11_Cam_13_Int_BedWindow_To_Kitty.png) |
| **12. Exterior Kitty Close-Up** (`Cam_14`) | ![Cam 14 PBR](./renders/current/12_Cam_14_Ext_RearWindow_And_Kitty.png) | ![Cam 14 Anime](./renders/anime/12_Cam_14_Ext_RearWindow_And_Kitty.png) |
