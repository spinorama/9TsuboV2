"""
9-Tsubo House — Automated Model-Derived Architectural Construction Sheets (Part 1: A-000 to A-301)
Runs inside Blender 5.2 LTS using cad_engine.py directly on 9_tsubo_house.blend.
"""
import os
import sys
import json
import math
import bpy
from mathutils import Vector

REPO_ROOT = r"C:\Users\paque\.gemini\antigravity\scratch\9TsuboHouseV2"
SCRIPTS_DIR = os.path.join(REPO_ROOT, "scripts")
DRAWINGS_DIR = os.path.join(REPO_ROOT, "drawings")
os.makedirs(DRAWINGS_DIR, exist_ok=True)
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

import importlib
import cad_engine
importlib.reload(cad_engine)
from cad_engine import (
    SvgSheet, get_group_meshes, slice_objects_at_plane, project_orthographic_view
)

with open(os.path.join(REPO_ROOT, "9_tsubo_bim_metadata.json"), encoding="utf-8") as _f:
    BIM_DATA = json.load(_f)

# Exact Structural Grid Lines (derived from 9_tsubo_house.blend wall & column centerlines)
GRID_X = [("1", -2.720), ("2", -0.780), ("3", 0.850), ("4", 2.720)]
GRID_Y = [("A", -2.650), ("B", 0.150), ("C", 2.650)]

def mm(val_m):
    return f"{int(round(val_m * 1000)):,}"

def m_dual(val_m):
    mm_val = int(round(abs(val_m) * 1000))
    total_in = abs(val_m) * 39.3701
    ft = int(total_in // 12)
    inch = int(round(total_in - ft * 12))
    if inch == 12:
        ft += 1
        inch = 0
    return f"{mm_val:,} ({ft}'-{inch}\")"

# =========================================================================
# SHEET A-000: COVER SHEET, DRAWING INDEX, CONCEPT & BIM LOD STRATEGY
# =========================================================================
def build_a000():
    s = SvgSheet("A-000", "COVER SHEET & DRAWING INDEX", "NTS / AS NOTED", "9TS-KOI-ZZ-ZZ-DR-A-0000", "GENERAL")

    # Hero Architectural Header Banner inside Drawing Field
    s.add('<rect x="52" y="50" width="1542" height="156" fill="#0f172a"/>')
    s.add('<text x="82" y="102" style="font-size:34px;font-weight:800;fill:#ffffff;letter-spacing:3px;">9-TSUBO HOUSE · SUMIRE AOI HOUSE</text>')
    s.add('<text x="82" y="132" style="font-size:14px;font-weight:700;fill:#38bdf8;letter-spacing:1.8px;">ARCHITECTURAL CONSTRUCTION DRAWING SET · ISO 19650 / IFC4 MODEL-DERIVED BIM</text>')
    s.add('<text x="82" y="160" style="font-size:11.5px;fill:#cbd5e1;letter-spacing:0.6px;">MAKOTO KOIZUMI / KOIZUMI STUDIO (1999) · AFTER MAKOTO MASUZAWA MINIMUM HOUSE (1952) · 3×3 KEN STRUCTURAL TIMBER PROTOTYPE</text>')
    s.add('<text x="82" y="182" class="mono" style="font-size:10.5px;fill:#94a3b8;">REPOSITORY: https://github.com/spinorama/9TsuboV2  |  BLENDER 5.2 LTS + BIMCRAFT-STYLE AUTOMATED SLICING &amp; LOD-400 DETAILING</text>')

    # Left Column: Complete 12-Sheet Construction Drawing Index Table
    s.add('<rect x="52" y="232" width="760" height="534" fill="#ffffff" stroke="#0f172a" stroke-width="1.5"/>')
    s.add('<rect x="52" y="232" width="760" height="32" fill="#e2e8f0" stroke="#0f172a" stroke-width="1.2"/>')
    s.add('<text x="68" y="253" style="font-size:12.5px;font-weight:800;letter-spacing:1px;">ARCHITECTURAL CONSTRUCTION DRAWING INDEX (12 SHEETS)</text>')

    # Table headers
    s.add('<rect x="52" y="264" width="760" height="24" fill="#f8fafc" stroke="#cbd5e1" stroke-width="0.8"/>')
    s.add('<text x="68" y="280" class="tb-lbl">SHEET</text>')
    s.add('<text x="148" y="280" class="tb-lbl">SHEET TITLE &amp; SCOPE</text>')
    s.add('<text x="545" y="280" class="tb-lbl">SCALE</text>')
    s.add('<text x="642" y="280" class="tb-lbl">DERIVATION METHOD</text>')

    sheet_rows = [
        ("A-000", "Cover Sheet, Drawing Index, Concept & BIM LOD Spec", "NTS", "BIM Metadata JSON"),
        ("A-100", "Site & Neighborhood Context Plan (33.0m × 32.3m)", "1 : 100", "3D Ortho Projection"),
        ("A-101", "First Floor Plan (Cut EL +1.250m · 1F & Engawa)", "1 : 50", "bmesh Slice + Proj."),
        ("A-102", "Second Floor Loft & Mezzanine Plan (Cut EL +3.550m)", "1 : 50", "bmesh Slice + Proj."),
        ("A-103", "Roof Plan & Zairai-koho Timber Framing Plan", "1 : 50", "3D Proj. + Struct."),
        ("A-104", "Reflected Ceiling & Architectural Lighting Plan", "1 : 50", "36 Modeled Fixtures"),
        ("A-201", "Exterior Elevations (South, West, North & East)", "1 : 50", "4× True 3D Ortho"),
        ("A-301", "Building Sections A-A (E–W) & B-B (N–S)", "1 : 50", "bmesh Cut + Poché"),
        ("A-401", "Enlarged Kitchen, 3-Zone Bath & Tatami Views", "1 : 25", "Sub-Volume 3D Slice"),
        ("A-501", "Typical Wall Section & Envelope Construction Details", "1:15 / 1:10", "Model-Driven LOD400"),
        ("A-502", "Glazing, Stair Stringer & Cable Guardrail Details", "1:5 / 1:10", "Model-Driven LOD400"),
        ("A-601", "Door, Window, Lighting & Room Schedules + BIM QTO", "TABLE", "Auto JSON Take-Off"),
    ]
    for i, (sid, title, sc, meth) in enumerate(sheet_rows):
        ry = 288 + i * 39
        bg = "#fdfcf8" if i % 2 == 0 else "#f8fafc"
        s.add(f'<rect x="52" y="{ry}" width="760" height="39" fill="{bg}" stroke="#e2e8f0" stroke-width="0.7"/>')
        s.add(f'<text x="68" y="{ry + 24}" class="mono" style="font-size:12px;font-weight:800;fill:#1d4ed8;">{sid}</text>')
        s.add(f'<text x="148" y="{ry + 24}" style="font-size:11px;font-weight:700;fill:#0f172a;">{title}</text>')
        s.add(f'<text x="545" y="{ry + 24}" class="mono" style="font-size:10px;font-weight:700;fill:#334155;">{sc}</text>')
        s.add(f'<text x="642" y="{ry + 24}" style="font-size:10px;font-weight:600;fill:#475569;">{meth}</text>')

    # Right Column Top: Live Model-Projected Isometric / Architectural Concept Box
    s.add('<rect x="838" y="232" width="756" height="534" fill="#ffffff" stroke="#0f172a" stroke-width="1.5"/>')
    s.add('<rect x="838" y="232" width="756" height="32" fill="#e2e8f0" stroke="#0f172a" stroke-width="1.2"/>')
    s.add('<text x="854" y="253" style="font-size:12.5px;font-weight:800;letter-spacing:1px;">MODEL-DERIVED AXONOMETRIC PROJECTION (HOUSE_GROUP + ROOF_GROUP)</text>')

    # True 3D Isometric Projection directly from Blender meshes!
    house_objs = get_group_meshes({"House_Group", "Roof_Group"})
    iso_dir = Vector((-0.62, -0.68, 0.39)).normalized()
    iso_u = Vector((0.74, -0.67, 0.0)).normalized()
    iso_v = iso_dir.cross(iso_u).normalized()
    # Make sure iso_v points up (+Z)
    if iso_v.z < 0:
        iso_v = -iso_v
    iso_scale = 74.0
    cx_iso, cy_iso = 1225.0, 625.0
    def to_iso(u, v):
        return (cx_iso + u * iso_scale, cy_iso - v * iso_scale)

    s.start_clip(842, 268, 748, 494)
    iso_polys = project_orthographic_view(house_objs, iso_dir, iso_u, iso_v, to_iso, skip_seams=False)
    for p in iso_polys:
        s.add(p)
    s.end_clip()

    # Callout overlay on axonometric
    s.leader_note(1120, 390, 1020, 315, ["ASYMMETRIC GABLE ROOF", "GALVALUME STANDING SEAM", "SOUTH 16.0° / NORTH 23.1°"], align="right")
    s.leader_note(1025, 520, 995, 495, ["WEST ENTRANCE CANOPY", "POUR-IN-PLACE STEP &", "EXTERIOR PORCH SCONCE"], align="right")
    s.leader_note(1310, 470, 1410, 355, ["2-STORY SLIDING SHOJI", "& ALUMINUM CURTAIN WALL", "(3,900mm × 4,260mm)"], align="left")
    s.leader_note(1345, 650, 1410, 675, ["CEDAR ENGAWA DECK", "24 PLANKS ON PRECAST", "CONCRETE PIER BLOCKS"], align="left")

    # Bottom Strip: 3 Structured Technical Cards (Building Data, Hybrid BIM/Mobile Cap, Architectural Legend)
    # Card 1: Project Code & Area Data
    s.add('<rect x="52" y="792" width="496" height="434" fill="#ffffff" stroke="#0f172a" stroke-width="1.5"/>')
    s.add('<rect x="52" y="792" width="496" height="30" fill="#0f172a"/>')
    s.add('<text x="68" y="812" style="font-size:11.5px;font-weight:800;fill:#ffffff;letter-spacing:0.9px;">1 · PROJECT DATA &amp; AREA SUMMARY (METRIC / JAPANESE)</text>')

    proj_lines = [
        ("FOOTPRINT MODULE", "3.0 ken × 3.0 ken = 9.0 Tsubo (18 Jo)"),
        ("EXTERIOR DIMENSIONS", "5,600mm (E–W) × 5,460mm (N–S) = 30.58 m²"),
        ("INTERIOR NET 1F AREA", "5,280mm × 5,140mm = 27.14 m² (292.1 sq ft)"),
        ("2F L-SHAPED LOFT AREA", "17.64 m² (189.9 sq ft) · Double-Height Void 9.50 m²"),
        ("TOTAL HABITABLE FLOOR", "44.78 m² (482.0 sq ft) + 6.53 m² Engawa Deck"),
        ("STRUCTURAL SYSTEM", "Zairai-koho Post & Beam · Twin Ø176mm Cedar Cols"),
        ("BUILDING HEIGHT", "EL +5.460m Ridge / +4.568m South Eave / +4.308m N"),
        ("FOUNDATION SYSTEM", "RC Mat Slab + 320mm Stem Plinth (EL 0.00..+0.32m)"),
        ("THERMAL ENVELOPE", "W-EXT-01 (160mm, U=0.34) · RF-01 (152mm, U=0.24)"),
        ("ARCHITECTURAL LIGHTING", "36 Modeled Luminaires (9 Fixture Types, 2700K LED)"),
        ("DESIGN / PROTOTYPE", "Makoto Koizumi (1999) / Makoto Masuzawa (1952)"),
    ]
    for i, (k, v) in enumerate(proj_lines):
        py = 846 + i * 33
        s.add(f'<line x1="64" y1="{py + 10}" x2="536" y2="{py + 10}" stroke="#e2e8f0" stroke-width="0.8"/>')
        s.add(f'<text x="68" y="{py}" class="tb-lbl">{k}</text>')
        s.add(f'<text x="225" y="{py}" style="font-size:10px;font-weight:700;fill:#0f172a;">{v}</text>')

    # Card 2: BIMCraft Hybrid 3D/2D Performance Architecture
    s.add('<rect x="574" y="792" width="500" height="434" fill="#ffffff" stroke="#0f172a" stroke-width="1.5"/>')
    s.add('<rect x="574" y="792" width="500" height="30" fill="#0f172a"/>')
    s.add('<text x="590" y="812" style="font-size:11.5px;font-weight:800;fill:#ffffff;letter-spacing:0.9px;">2 · HYBRID LOD-300 / LOD-400 MOBILE BIM PIPELINE</text>')

    tot = BIM_DATA["totals"]
    bim_notes = [
        ("MOBILE / AR TRIANGLE CAP", f"≤ 60,000 tris total (Actual: {tot['totalTris']:,} tris — PASS)"),
        ("HOUSE + ROOF + FIXTURES", f"{tot['houseRoofTris']:,} tris (10.1K) · 278 KB Apple 1:1 USDZ"),
        ("FULL SITE + CONTEXT", f"{tot['contextTris']:,} context tris · 2.33 MB GLB / 2.11 MB USDZ"),
        ("FEDERATED IFC4 ELEMENTS", f"{tot['meshes']} tagged meshes · ISO 19650-2 S4 Rev P05.0"),
        ("WHY HYBRID 3D + 2D?", "Studs, flashing, rebar, WRB & batt insulation would"),
        ("", "add 400k+ tris and crash mobile WebXR / Quick Look."),
        ("", "Instead, the 3D BIM model defines exact envelope"),
        ("", "boundaries & thickness (LOD-300) and stores assembly"),
        ("", "metadata (W-EXT-01, RF-01, FND-01, GLZ-01, STR-01)."),
        ("", "Our Python BIM engine slices the 3D meshes and auto-"),
        ("", "generates 2D LOD-400 details (BIMCraft workflow)."),
    ]
    for i, (k, v) in enumerate(bim_notes):
        py = 846 + i * 33
        if k:
            s.add(f'<text x="590" y="{py}" class="tb-lbl" style="fill:#1d4ed8;">{k}</text>')
            s.add(f'<text x="765" y="{py}" style="font-size:9.8px;font-weight:700;fill:#0f172a;">{v}</text>')
        else:
            s.add(f'<text x="590" y="{py}" style="font-size:10px;fill:#334155;">{v}</text>')

    # Card 3: Architectural Graphic Symbols & Material Hatch Legend
    s.add('<rect x="1100" y="792" width="494" height="434" fill="#ffffff" stroke="#0f172a" stroke-width="1.5"/>')
    s.add('<rect x="1100" y="792" width="494" height="30" fill="#0f172a"/>')
    s.add('<text x="1116" y="812" style="font-size:11.5px;font-weight:800;fill:#ffffff;letter-spacing:0.9px;">3 · MATERIAL HATCH &amp; DRAFTING SYMBOL LEGEND</text>')

    hatches = [
        ("url(#hatch-wall-cut)", "EXTERIOR INSULATED TIMBER WALL (160mm · W-EXT-01)"),
        ("url(#hatch-part-cut)", "INTERIOR PARTITION WALL (75mm · W-INT-01)"),
        ("url(#hatch-concrete)", "REINFORCED CONCRETE FOOTING &amp; PLINTH (24 MPa)"),
        ("url(#hatch-gravel)", "CRUSHED GRAVEL CAPILLARY DRAINAGE BED (150mm)"),
        ("url(#hatch-earth)", "COMPACTED GRADE / UNDISTURBED SOIL"),
        ("url(#hatch-xps)", "RIGID EXTRUDED POLYSTYRENE INSULATION (XPS)"),
        ("url(#hatch-plywood)", "JAS BIRCH / LAUAN STRUCTURAL PLYWOOD LINING"),
        ("url(#hatch-wood)", "JAPANESE CEDAR (SUGI) / RED PINE TIMBER"),
        ("url(#hatch-steel)", "GALVALUME METAL ROOFING / ANODIZED ALUMINUM"),
        ("url(#hatch-tatami)", "IGUSA RUSH TATAMI MAT (6-MAT RAISED BAY)"),
    ]
    for i, (hfill, hlbl) in enumerate(hatches):
        hy = 838 + i * 37
        s.add(f'<rect x="1118" y="{hy}" width="44" height="24" fill="{hfill}" stroke="#0f172a" stroke-width="1.2"/>')
        s.add(f'<text x="1174" y="{hy + 16}" style="font-size:9.8px;font-weight:700;fill:#0f172a;">{hlbl}</text>')

    s.save(os.path.join(DRAWINGS_DIR, "A-000_Cover_Index.svg"))
    print("Generated A-000_Cover_Index.svg")


# =========================================================================
# SHEET A-100: SITE & NEIGHBORHOOD CONTEXT PLAN (1:100)
# =========================================================================
def build_a100():
    s = SvgSheet("A-100", "SITE & CONTEXT PLAN", "1 : 100 (SITE)", "9TS-KOI-ST-00-DR-A-0100", "SITE / CIVIL")
    all_objs = get_group_meshes({"Context_Group", "House_Group", "Roof_Group"})

    # Center site (X=-16.5..+16.5, Y=-16.8..+15.5 -> 33.0m x 32.3m) into drawing field (50..1590 x 55..1180)
    # 1:100 scale ~ 33.5 px/m -> 33m = 1105px! Plenty of room for dimensions, keynotes & site metrics.
    px_m = 33.0
    cx, cy = 780.0, 600.0
    def to_svg(u, v):
        return (cx + u * px_m, cy - v * px_m)

    s.start_clip(48, 52, 1546, 1126)
    polys = project_orthographic_view(all_objs, (0, 0, 1), (1, 0, 0), (0, 1, 0), to_svg, skip_seams=True)
    for p in polys:
        s.add(p)

    # Highlight 9-Tsubo Property Parcel Boundary (approx X=-5.5..+3.5, Y=-4.8..+3.2)
    px0, py1 = to_svg(-5.45, -4.65)
    px1, py0 = to_svg(3.35, 3.15)
    s.add(f'<rect x="{px0:.1f}" y="{py0:.1f}" width="{px1 - px0:.1f}" height="{py1 - py0:.1f}" fill="none" stroke="#b91c1c" stroke-width="2.0" stroke-dasharray="14,5,3,5"/>')

    # Sightline from 2F Bedroom Window (W-02) to Neighbor's Tuxedo Kitty Window!
    kx0, ky0 = to_svg(-0.05, 2.73)
    kx1, ky1 = to_svg(-0.90, 5.20)
    s.add(f'<line x1="{kx0:.1f}" y1="{ky0:.1f}" x2="{kx1:.1f}" y2="{ky1:.1f}" stroke="#1d4ed8" stroke-width="1.5" stroke-dasharray="6,4" marker-end="url(#arr-blue)"/>')
    s.end_clip()

    # Site Boundary & House Setback Dimensions
    hx0, hy1 = to_svg(-2.80, -2.73)
    hx1, hy0 = to_svg(2.80, 2.73)
    s.dim_h(px0, hx0, py0 - 22, f"{mm(2.65)} WEST SETBACK", ext_y=py0)
    s.dim_h(hx0, hx1, py0 - 22, f"{mm(5.60)} HOUSE", ext_y=hy0)
    s.dim_h(hx1, px1, py0 - 22, f"{mm(0.55)} EAST", ext_y=py0)
    s.dim_h(px0, px1, py0 - 48, f"{mm(8.80)} PARCEL WIDTH (28'-10\")", ext_y=py0 - 20, color="#b91c1c")

    s.dim_v(px0 - 26, py0, hy0, f"{mm(0.42)}", ext_x=px0)
    s.dim_v(px0 - 26, hy0, hy1, f"{mm(5.46)} HOUSE", ext_x=hx0)
    s.dim_v(px0 - 26, hy1, py1, f"{mm(1.92)} FRONT", ext_x=px0)
    s.dim_v(px0 - 54, py0, py1, f"{mm(7.80)} PARCEL DEPTH (25'-7\")", ext_x=px0 - 24, color="#b91c1c")

    # Site Callout Leaders
    s.leader_note(*to_svg(0.0, 0.15), 1160, 420, ["9-TSUBO HOUSE (BLDG-01)", "5,600 × 5,460mm FOOTPRINT", "RIDGE EL +5.460m · 29.81 m²"], align="left")
    s.leader_note(*to_svg(-0.90, 5.20), 1160, 260, ["NEIGHBOR 2F WINDOW SIGHTLINE", "TUXEDO KITTY PERCH (CTX_KITTY)", "FRAMED FROM 2F BEDROOM W-02"], align="left", color="#1d4ed8")
    s.leader_note(*to_svg(3.0, -3.7), 1160, 760, ["SPECIMEN SAKURA (CHERRY TREE)", "FLANKING FRONT ENGAWA DECK", "CTX_SAKURA_* PRESERVED"], align="left")
    s.leader_note(*to_svg(-4.1, -0.5), 305, 505, ["WEST CONCRETE ENTRY PAVERS", "PERMEABLE GRAVEL APRON", "EL ±0.000 SITE GRADE"], align="right")
    s.leader_note(*to_svg(-0.5, -3.5), 305, 745, ["CEDAR ENGAWA DECK (EL +0.320m)", "4,352 × 1,500mm · PRECAST PIERS"], align="right")
    s.leader_note(*to_svg(0.0, -7.8), 1160, 910, ["URBAN ACCESS STREET (ASPHALT)", "UTILITY POLES & OVERHEAD LINES", "DRAINAGE TO STREET CURB"], align="left")

    # Site Metrics Legend Card (top-left)
    s.add('<rect x="52" y="56" width="290" height="175" fill="#fdfcf8" fill-opacity="0.95" stroke="#0f172a" stroke-width="1.3"/>')
    s.add('<rect x="52" y="56" width="290" height="24" fill="#0f172a"/>')
    s.add('<text x="64" y="72" style="font-size:10.5px;font-weight:800;fill:#ffffff;">SITE ZONING &amp; COVERAGE DATA</text>')
    site_stats = [
        "MODEL SITE EXTENTS: 33.0m × 32.3m",
        "PARCEL LOT AREA: ~68.6 m² (20.8 Tsubo)",
        "BUILDING FOOTPRINT: 30.58 m² (44.6% BCR)",
        "GROSS FLOOR AREA: 44.78 m² (65.3% FAR)",
        "GRADE DATUM: EL ±0.000m (STREET +0.00)",
        "ROOF DRAINAGE: SOUTH EAVE GUTTER →",
        "SE CORNER DOWNSPOUT TO GRAVEL BED",
    ]
    for i, ln in enumerate(site_stats):
        s.add(f'<text x="64" y="{98 + i * 18}" style="font-size:9.3px;font-weight:700;fill:#1e293b;">{ln}</text>')

    s.viewport_title(56, 1214, "1", "SITE & NEIGHBORHOOD CONTEXT PLAN (MODEL-DERIVED)", "1 : 100", width=560)
    s.scale_bar(660, 1212, px_m, (0, 1, 2, 5, 10))
    s.save(os.path.join(DRAWINGS_DIR, "A-100_Site_Context_Plan.svg"))
    print("Generated A-100_Site_Context_Plan.svg")


# =========================================================================
# SHEET A-101: FIRST FLOOR PLAN (1:50, TRUE bmesh SLICE @ EL +1.250m)
# =========================================================================
def build_a101():
    s = SvgSheet("A-101", "FIRST FLOOR PLAN (1F)", "1 : 50 (EL +1.250m)", "9TS-KOI-B1-L1-DR-A-0101", "ARCHITECTURE")
    # Use House_Group only (no Roof_Group), exclude 2F-only loft objects above Z=2.30m
    house_objs = get_group_meshes({"House_Group"})

    # 1:50 architectural scale on 1920x1280 -> 110 px/m makes 5.6m = 616px (super readable with 3-tier dims & notes!)
    px_m = 112.0
    cx, cy = 835.0, 565.0
    def to_svg(u, v):
        return (cx + u * px_m, cy - v * px_m)

    # 1. Structural Grid Lines (1..4, A..C)
    y_gtop = to_svg(0, 3.35)[1]
    y_gbot = to_svg(0, -4.55)[1]
    x_glft = to_svg(-4.00, 0)[0]
    x_grgt = to_svg(3.35, 0)[0]

    for lbl, gx in GRID_X:
        s.grid_line_v(to_svg(gx, 0)[0], y_gtop, y_gbot, lbl, top_bubble=True, bot_bubble=True)
    for lbl, gy in GRID_Y:
        s.grid_line_h(to_svg(0, gy)[1], x_glft, x_grgt, lbl, left_bubble=True, right_bubble=True)

    # 2. Projected 3D Floor, Furniture, Fixtures & Deck BELOW Cut Plane Z = 1.25m
    cut_z = 1.25
    plan_bg = project_orthographic_view(
        house_objs,
        view_dir=(0, 0, 1), u_axis=(1, 0, 0), v_axis=(0, 1, 0),
        to_svg_fn=to_svg,
        clip_plane=((0, 0, cut_z), (0, 0, 1)),  # removes everything ABOVE Z=1.25m!
        skip_seams=False
    )
    s.add('<g id="plan-1f-projected-below">')
    for p in plan_bg:
        s.add(p)
    s.add('</g>')

    # 3. TRUE bmesh Cross-Section Cut Polygons at Z = 1.25m (Walls, Columns, Partitions, Frames!)
    cut_els = slice_objects_at_plane(
        house_objs,
        plane_co=(0, 0, cut_z), plane_no=(0, 0, 1),
        u_axis=(1, 0, 0), v_axis=(0, 1, 0),
        to_svg_fn=to_svg
    )
    s.add('<g id="plan-1f-cut-poche">')
    for c in cut_els:
        s.add(c)
    s.add('</g>')

    # 4. Architectural Drafting Overlays Derived from Exact Model Coordinates:
    # 4a. Dashed overhead 2F Loft Mezzanine edge line (L-shaped loft overhang @ Y=0.15, X=0.85)
    lx1, ly1 = to_svg(-2.64, 0.15)
    lx2, ly2 = to_svg(0.85, 0.15)
    lx3, ly3 = to_svg(0.85, -2.57)
    s.add(f'<polyline points="{lx1:.1f},{ly1:.1f} {lx2:.1f},{ly2:.1f} {lx3:.1f},{ly3:.1f}" fill="none" stroke="#475569" stroke-width="1.3" stroke-dasharray="8,4"/>')
    s.add(f'<rect x="{to_svg(-0.62, 0.08)[0]:.1f}" y="{ly2 + 4:.1f}" width="152" height="12" fill="#fdfcf8" fill-opacity="0.88"/>')
    s.add(f'<text x="{to_svg(0.04, 0.08)[0]:.1f}" y="{ly2 + 13:.1f}" text-anchor="middle" style="font-size:8.2px;font-weight:700;fill:#475569;">2F LOFT EDGE ABOVE (+2.36m)</text>')

    # 4b. Stair Cut Break Line, Remaining Upper Treads Dashed, & UP Arrow (X=-2.58..-1.98, Y=-1.96..+0.06)
    st_x0, st_y_bot = to_svg(-2.58, -1.96)
    st_x1, st_y_top = to_svg(-1.98, 0.15)
    st_xm = 0.5 * (st_x0 + st_x1)
    _, st_y_cut = to_svg(0, -1.04)  # Tread 6 cut at Z=1.25m
    # Dashed treads above cut line (Treads 7..11)
    for ty_m in (-0.86, -0.67, -0.49, -0.31, -0.12, 0.06):
        _, sy = to_svg(0, ty_m)
        s.add(f'<line x1="{st_x0:.1f}" y1="{sy:.1f}" x2="{st_x1:.1f}" y2="{sy:.1f}" stroke="#475569" stroke-width="0.9" stroke-dasharray="4,3"/>')
    # Diagonal architectural stair cut break line
    s.add(f'<line x1="{st_x0 - 6:.1f}" y1="{st_y_cut + 10:.1f}" x2="{st_x1 + 6:.1f}" y2="{st_y_cut - 10:.1f}" stroke="#0f172a" stroke-width="1.8"/>')
    s.add(f'<line x1="{st_xm:.1f}" y1="{st_y_bot:.1f}" x2="{st_xm:.1f}" y2="{st_y_cut + 4:.1f}" stroke="#0f172a" stroke-width="1.4" marker-end="url(#arr-dark)"/>')
    s.add(f'<text x="{st_xm:.1f}" y="{st_y_bot + 14:.1f}" text-anchor="middle" style="font-size:8.5px;font-weight:800;">UP 12R (180/183)</text>')

    # 4c. Door Swing Arcs (West Entry D-01, Bath Entry D-02, WC Door D-03, Shower Glass Door D-04)
    # West Entry D-01 hinge at (-2.80, 0.00), swings outward or inward (683mm leaf)
    d1x, d1y = to_svg(-2.80, 0.00)
    r1 = 0.683 * px_m
    s.add(f'<line x1="{d1x:.1f}" y1="{d1y:.1f}" x2="{d1x - r1:.1f}" y2="{d1y:.1f}" stroke="#0f172a" stroke-width="1.5"/>')
    s.add(f'<path d="M {d1x - r1:.1f} {d1y:.1f} A {r1:.1f} {r1:.1f} 0 0 1 {d1x:.1f} {d1y - r1:.1f}" fill="none" stroke="#475569" stroke-width="0.9" stroke-dasharray="4,3"/>')
    # Front sliding door arrow (open bay X=-0.75..+1.10 @ Y=-2.65)
    sl_x0, sl_y = to_svg(-0.55, -2.66)
    sl_x1, _ = to_svg(0.85, -2.66)
    s.add(f'<line x1="{sl_x1:.1f}" y1="{sl_y:.1f}" x2="{sl_x0:.1f}" y2="{sl_y:.1f}" stroke="#1d4ed8" stroke-width="1.3" marker-end="url(#arr-blue)"/>')

    # 4d. Section Cut Flags A-A (Y=-0.50 looking North) and B-B (X=-0.40 looking East)
    _, sec_aa_y = to_svg(0, -0.50)
    s.section_cut_line(x_glft + 18, sec_aa_y, x_grgt - 18, sec_aa_y, "A", "A-301", look="up")
    sec_bb_x, _ = to_svg(-0.40, 0)
    s.section_cut_line(sec_bb_x, y_gtop + 28, sec_bb_x, y_gbot - 18, "B", "A-301", look="right")

    # 4e. Room Tags (Exact Areas Derived from Model Coordinates)
    s.room_tag(*to_svg(-0.42, -1.42), "RM-101", "LIVING / DINING", "10.6 m² · EL +0.360")
    s.room_tag(*to_svg(1.70, -1.35), "RM-102", "GALLEY KITCHEN", "4.8 m² · EL +0.360")
    s.room_tag(*to_svg(-0.68, 1.66), "RM-103", "6-MAT TATAMI", "4.6 m² (3 TSUBO) · +0.520")
    s.room_tag(*to_svg(-2.26, 0.48), "RM-104", "GENKAN", "1.1 m² · +0.360")
    s.room_tag(*to_svg(1.38, 1.25), "RM-105", "VANITY", "1.2 m² · +0.360")
    s.room_tag(*to_svg(2.26, 1.28), "RM-106", "WC", "0.7 m²")
    s.room_tag(*to_svg(1.90, 2.18), "RM-107", "WET SHOWER", "1.2 m² · +0.388")
    s.room_tag(*to_svg(-0.56, -3.50), "EXT-01", "CEDAR ENGAWA DECK", "6.5 m² · EL +0.320")

    # 4f. Door & Window Schedule Tags
    s.tag_badge(*to_svg(-3.08, 0.34), "D-01", shape="pill", stroke="#0f172a")
    s.tag_badge(*to_svg(1.50, 0.55), "D-02", shape="pill", stroke="#0f172a")
    s.tag_badge(*to_svg(1.88, 1.40), "D-03", shape="pill", stroke="#0f172a")
    s.tag_badge(*to_svg(1.50, 1.72), "D-04", shape="pill", stroke="#0f172a")
    s.tag_badge(*to_svg(-1.70, -2.92), "W-01A", shape="hex", stroke="#1d4ed8")
    s.tag_badge(*to_svg(0.20, -2.92), "W-01B", shape="hex", stroke="#1d4ed8")
    s.tag_badge(*to_svg(-0.75, 2.90), "W-03", shape="hex", stroke="#1d4ed8")
    s.tag_badge(*to_svg(2.96, -1.25), "W-05", shape="hex", stroke="#1d4ed8")
    s.tag_badge(*to_svg(2.96, 1.37), "W-06", shape="hex", stroke="#1d4ed8")
    s.tag_badge(*to_svg(1.77, 2.90), "W-04", shape="hex", stroke="#1d4ed8")

    # 5. Three-Tier Exterior Dimension Chains (North Top, South Bottom, East Right, West Left)
    # Top (North) Horizontal Chain: Grid-to-Grid & Overall
    y_dim_t1 = y_gtop - 48
    y_dim_t2 = y_gtop - 76
    gx_svgs = [to_svg(gx, 0)[0] for _, gx in GRID_X]
    s.dim_h(gx_svgs[0], gx_svgs[1], y_dim_t1, mm(1.94), ext_y=y_gtop - 26)
    s.dim_h(gx_svgs[1], gx_svgs[2], y_dim_t1, mm(1.63), ext_y=y_gtop - 26)
    s.dim_h(gx_svgs[2], gx_svgs[3], y_dim_t1, mm(1.87), ext_y=y_gtop - 26)
    s.dim_h(to_svg(-2.80, 0)[0], to_svg(2.80, 0)[0], y_dim_t2, f"5,600 OVERALL (18'-4\") · 3 KEN MODULE", ext_y=y_dim_t1, color="#b91c1c")

    # Bottom (South) Horizontal Chain: Engawa & Front Curtain Opening
    y_dim_b1 = y_gbot + 44
    s.dim_h(to_svg(-2.736, 0)[0], to_svg(1.616, 0)[0], y_dim_b1, "4,352 CEDAR ENGAWA DECK", ext_y=to_svg(0, -4.25)[1])
    s.dim_h(to_svg(1.616, 0)[0], to_svg(2.80, 0)[0], y_dim_b1, "1,184", ext_y=to_svg(0, -2.73)[1])

    # Right (East) Vertical Chain: Grid-to-Grid & Overall
    x_dim_r1 = x_grgt + 46
    x_dim_r2 = x_grgt + 76
    gy_svgs = [to_svg(0, gy)[1] for _, gy in GRID_Y]  # A (south/bottom), B (mid), C (north/top)
    s.dim_v(x_dim_r1, gy_svgs[2], gy_svgs[1], mm(2.50), ext_x=x_grgt + 24)
    s.dim_v(x_dim_r1, gy_svgs[1], gy_svgs[0], mm(2.80), ext_x=x_grgt + 24)
    s.dim_v(x_dim_r1, gy_svgs[0], to_svg(0, -4.25)[1], "1,600 DECK", ext_x=x_grgt + 24)
    s.dim_v(x_dim_r2, to_svg(0, 2.73)[1], to_svg(0, -2.73)[1], "5,460 = 3.0 KEN (17'-11\")", ext_x=x_dim_r1, color="#b91c1c")

    # Enlarged Plan Callout Boxes pointing to A-401
    ex0, ey1 = to_svg(0.55, 0.72)
    ex1, ey0 = to_svg(2.68, 2.60)
    s.add(f'<rect x="{ex0:.1f}" y="{ey0:.1f}" width="{ex1 - ex0:.1f}" height="{ey1 - ey0:.1f}" fill="none" stroke="#b91c1c" stroke-width="1.2" stroke-dasharray="6,3"/>')
    s.detail_callout(ex1 - 8, ey0, 9, "3", "A-401", ex1 + 115, ey0 - 72)

    # Keynotes Panel (Left side of sheet)
    s.add('<rect x="46" y="130" width="278" height="390" fill="#ffffff" stroke="#0f172a" stroke-width="1.3"/>')
    s.add('<rect x="46" y="130" width="278" height="24" fill="#0f172a"/>')
    s.add('<text x="58" y="146" style="font-size:10.5px;font-weight:800;fill:#ffffff;">1F CONSTRUCTION KEYNOTES</text>')
    notes_1f = [
        "1. EXTERIOR WALLS: 160mm W-EXT-01",
        "   Galvalume rainscreen + 105mm posts +",
        "   mineral wool + 12mm birch plywood.",
        "2. CENTRAL COLUMNS: Twin Ø176mm",
        "   turned cedar columns on Grid B.",
        "3. TATAMI BAY: Raised +160mm (EL +0.52)",
        "   with 6 mats + low jimado window W-03.",
        "4. BATHROOM SUITE: 3-zone Japanese",
        "   plan (Vanity / separate WC / Wet-room).",
        "5. STAIR FLIGHT: 11 open timber treads,",
        "   180mm rise / 183mm run to 2F loft.",
        "6. FRONT ENGAWA: 24 cedar planks on",
        "   8 precast concrete piers (EL +0.320).",
        "7. SEE SHEET A-401 FOR 1:25 ENLARGED",
        "   KITCHEN, BATH & TATAMI PLANS.",
    ]
    for i, ln in enumerate(notes_1f):
        s.add(f'<text x="58" y="{174 + i * 22}" style="font-size:9.3px;font-weight:600;fill:#1e293b;">{ln}</text>')

    s.viewport_title(56, 1214, "1", "FIRST FLOOR PLAN — CUT AT EL +1.250m (MODEL-SLICED)", "1 : 50", width=620)
    s.scale_bar(720, 1212, px_m, (0, 1, 2, 3, 4))
    s.save(os.path.join(DRAWINGS_DIR, "A-101_First_Floor_Plan.svg"))
    print("Generated A-101_First_Floor_Plan.svg")


# =========================================================================
# SHEET A-102: SECOND FLOOR LOFT & MEZZANINE PLAN (1:50, SLICE @ EL +3.550m)
# =========================================================================
def build_a102():
    s = SvgSheet("A-102", "SECOND FLOOR LOFT PLAN (2F)", "1 : 50 (EL +3.550m)", "9TS-KOI-B1-L2-DR-A-0102", "ARCHITECTURE")
    house_objs = get_group_meshes({"House_Group"})

    px_m = 112.0
    cx, cy = 835.0, 610.0
    def to_svg(u, v):
        return (cx + u * px_m, cy - v * px_m)

    y_gtop = to_svg(0, 3.35)[1]
    y_gbot = to_svg(0, -3.55)[1]
    x_glft = to_svg(-3.60, 0)[0]
    x_grgt = to_svg(3.35, 0)[0]

    for lbl, gx in GRID_X:
        s.grid_line_v(to_svg(gx, 0)[0], y_gtop, y_gbot, lbl, top_bubble=True, bot_bubble=True)
    for lbl, gy in GRID_Y:
        s.grid_line_h(to_svg(0, gy)[1], x_glft, x_grgt, lbl, left_bubble=True, right_bubble=True)

    cut_z = 3.55
    # 1. Ghosted lower 1F floor visible inside Double-Height Void (Z < 2.35m)
    lower_proj = project_orthographic_view(
        house_objs,
        view_dir=(0, 0, 1), u_axis=(1, 0, 0), v_axis=(0, 1, 0),
        to_svg_fn=to_svg,
        clip_plane=((0, 0, 2.34), (0, 0, 1)),
        override_style=("#fafaf7", "#cbd5e1", 0.55),
        skip_seams=True
    )
    s.add('<g id="plan-2f-below-void">')
    for p in lower_proj:
        s.add(p)
    s.add('</g>')

    # 2. Crisp 2F Loft Mezzanine Elements (Z >= 2.34m and Z <= 3.55m)
    upper_proj = project_orthographic_view(
        house_objs,
        view_dir=(0, 0, 1), u_axis=(1, 0, 0), v_axis=(0, 1, 0),
        to_svg_fn=to_svg,
        clip_plane=((0, 0, cut_z), (0, 0, 1)),
        depth_clip_range=(2.32, cut_z + 0.05),
        skip_seams=False
    )
    s.add('<g id="plan-2f-projected">')
    for p in upper_proj:
        s.add(p)
    s.add('</g>')

    # 3. TRUE bmesh Cross-Section Cut at Z = 3.55m (Cuts 2F Rear Sliding Window W-02 + Upper Shoji + Columns!)
    cut_els = slice_objects_at_plane(
        house_objs,
        plane_co=(0, 0, cut_z), plane_no=(0, 0, 1),
        u_axis=(1, 0, 0), v_axis=(0, 1, 0),
        to_svg_fn=to_svg
    )
    s.add('<g id="plan-2f-cut-poche">')
    for c in cut_els:
        s.add(c)
    s.add('</g>')

    # 4. Open-to-Below Double-Height Void X-Cross (X=-1.92..+0.85, Y=-2.57..+0.15)
    vx0, vy1 = to_svg(-1.92, -2.57)
    vx1, vy0 = to_svg(0.85, 0.15)
    s.add(f'<line x1="{vx0:.1f}" y1="{vy0:.1f}" x2="{vx1:.1f}" y2="{vy1:.1f}" stroke="#94a3b8" stroke-width="1.0" stroke-dasharray="8,5"/>')
    s.add(f'<line x1="{vx1:.1f}" y1="{vy0:.1f}" x2="{vx0:.1f}" y2="{vy1:.1f}" stroke="#94a3b8" stroke-width="1.0" stroke-dasharray="8,5"/>')
    s.room_tag(*to_svg(-0.54, -1.21), "VOID", "OPEN TO LIVING BELOW", "9.50 m² DOUBLE-HEIGHT")

    # Dashed overhead rear storage cabinet (Loft_Rear_Overhead_Cab: X=-1.15..+2.16, Y=2.19..2.57 @ Z=3.90..4.26)
    oc_x0, oc_y1 = to_svg(-1.15, 2.19)
    oc_x1, oc_y0 = to_svg(2.16, 2.57)
    s.add(f'<rect x="{oc_x0:.1f}" y="{oc_y0:.1f}" width="{oc_x1 - oc_x0:.1f}" height="{oc_y1 - oc_y0:.1f}" fill="none" stroke="#64748b" stroke-width="1.0" stroke-dasharray="5,3"/>')

    # Stair DN arrow at landing
    st_x, st_y0 = to_svg(-2.28, 0.15)
    _, st_y1 = to_svg(-2.28, -1.85)
    s.add(f'<line x1="{st_x:.1f}" y1="{st_y0:.1f}" x2="{st_x:.1f}" y2="{st_y1:.1f}" stroke="#0f172a" stroke-width="1.3" marker-end="url(#arr-dark)"/>')
    s.add(f'<text x="{st_x:.1f}" y="{st_y0 - 8:.1f}" text-anchor="middle" style="font-size:8.5px;font-weight:800;">DN 12R</text>')

    # Room Tags
    s.room_tag(*to_svg(-0.08, 1.55), "RM-201", "2F BEDROOM LOFT", "10.8 m² · EL +2.520")
    s.room_tag(*to_svg(1.52, -1.15), "RM-202", "2F LOFT LOUNGE", "6.8 m² · EL +2.520")
    s.tag_badge(*to_svg(-0.05, 2.94), "W-02", shape="hex", stroke="#1d4ed8")
    s.tag_badge(*to_svg(-1.70, -2.90), "W-01C", shape="hex", stroke="#1d4ed8")
    s.tag_badge(*to_svg(0.20, -2.90), "W-01D", shape="hex", stroke="#1d4ed8")

    # Section Cut Lines
    _, sec_aa_y = to_svg(0, -0.50)
    s.section_cut_line(x_glft + 18, sec_aa_y, x_grgt - 18, sec_aa_y, "A", "A-301", look="up")
    sec_bb_x, _ = to_svg(-0.40, 0)
    s.section_cut_line(sec_bb_x, y_gtop + 28, sec_bb_x, y_gbot - 18, "B", "A-301", look="right")

    # Detail Callout for W-02 & Cable Rail
    s.detail_callout(*to_svg(-0.05, 2.66), 24, "2", "A-502", *to_svg(1.40, 3.60))
    s.detail_callout(*to_svg(0.85, -0.80), 22, "4", "A-502", *to_svg(-0.40, -3.55))

    # Dimensions
    y_dim_t1 = y_gtop - 48
    y_dim_t2 = y_gtop - 76
    gx_svgs = [to_svg(gx, 0)[0] for _, gx in GRID_X]
    s.dim_h(gx_svgs[0], gx_svgs[1], y_dim_t1, mm(1.94), ext_y=y_gtop - 26)
    s.dim_h(gx_svgs[1], gx_svgs[2], y_dim_t1, mm(1.63), ext_y=y_gtop - 26)
    s.dim_h(gx_svgs[2], gx_svgs[3], y_dim_t1, mm(1.87), ext_y=y_gtop - 26)
    s.dim_h(to_svg(-2.80, 0)[0], to_svg(2.80, 0)[0], y_dim_t2, "5,600 OVERALL (18'-4\")", ext_y=y_dim_t1, color="#b91c1c")

    # Rear Window W-02 opening dimension
    s.dim_h(to_svg(-0.95, 0)[0], to_svg(0.85, 0)[0], to_svg(0, 3.15)[1], "1,800 RO (W-02 SLIDING)", ext_y=to_svg(0, 2.73)[1], color="#1d4ed8")

    x_dim_r1 = x_grgt + 46
    x_dim_r2 = x_grgt + 76
    gy_svgs = [to_svg(0, gy)[1] for _, gy in GRID_Y]
    s.dim_v(x_dim_r1, gy_svgs[2], gy_svgs[1], mm(2.50), ext_x=x_grgt + 24)
    s.dim_v(x_dim_r1, gy_svgs[1], gy_svgs[0], mm(2.80), ext_x=x_grgt + 24)
    s.dim_v(x_dim_r2, to_svg(0, 2.73)[1], to_svg(0, -2.73)[1], "5,460 = 3.0 KEN (17'-11\")", ext_x=x_dim_r1, color="#b91c1c")

    # Left Keynotes Panel
    s.add('<rect x="46" y="160" width="286" height="360" fill="#ffffff" stroke="#0f172a" stroke-width="1.3"/>')
    s.add('<rect x="46" y="160" width="286" height="24" fill="#0f172a"/>')
    s.add('<text x="58" y="176" style="font-size:10.5px;font-weight:800;fill:#ffffff;">2F LOFT &amp; MEZZANINE NOTES</text>')
    notes_2f = [
        "1. L-SHAPED MEZZANINE: EL +2.520m FFL",
        "   (160mm FL-2F-01 timber joist assembly).",
        "2. SAFETY GUARDRAIL: 760mm high painted",
        "   steel posts & top rail w/ 3 tensioned",
        "   Ø8mm SS wire cables (See 4/A-502).",
        "3. REAR SLIDING WINDOW (W-02): 1,800 ×",
        "   560mm dual aluminum sash, sill +3.30m,",
        "   head +3.86m, cedar interior reveal.",
        "4. EAST BUILT-IN STORAGE: Full-length",
        "   5,140 × 480 × 820mm birch cabinetry.",
        "5. OVERHEAD CABINET: Dashed above bed",
        "   at EL +3.90..+4.26m along north wall.",
        "6. SLOPED CEILING: Rises from +4.30m N",
        "   to +5.33m ridge (Grid B), +4.55m S.",
    ]
    for i, ln in enumerate(notes_2f):
        s.add(f'<text x="58" y="{204 + i * 22}" style="font-size:9.3px;font-weight:600;fill:#1e293b;">{ln}</text>')

    s.viewport_title(56, 1214, "1", "SECOND FLOOR LOFT & MEZZANINE PLAN — CUT AT EL +3.550m", "1 : 50", width=650)
    s.scale_bar(740, 1212, px_m, (0, 1, 2, 3, 4))
    s.save(os.path.join(DRAWINGS_DIR, "A-102_Second_Floor_Loft_Plan.svg"))
    print("Generated A-102_Second_Floor_Loft_Plan.svg")


# =========================================================================
# SHEET A-103: ROOF PLAN & STRUCTURAL TIMBER FRAMING PLAN (1:50)
# =========================================================================
def build_a103():
    s = SvgSheet("A-103", "ROOF & TIMBER FRAMING PLANS", "1 : 50", "9TS-KOI-B1-L3-DR-S-0103", "ARCHITECTURE / STRUCT")
    roof_objs = get_group_meshes({"Roof_Group", "House_Group"})

    px_m = 88.0

    # --- LEFT VIEWPORT: ROOF PLAN (1:50) ---
    cx1, cy1 = 440.0, 560.0
    def to_roof(u, v):
        return (cx1 + u * px_m, cy1 - v * px_m)

    for lbl, gx in GRID_X:
        s.grid_line_v(to_roof(gx, 0)[0], to_roof(0, 3.25)[1], to_roof(0, -3.55)[1], lbl, top_bubble=True)
    for lbl, gy in GRID_Y:
        s.grid_line_h(to_roof(0, gy)[1], to_roof(-3.95, 0)[0], to_roof(3.30, 0)[0], lbl, left_bubble=True)

    # Project Roof_Group + Entry Canopy + Engawa outline from top
    roof_only = [o for o in roof_objs if (o.parent and o.parent.name == "Roof_Group") or any(k in o.name.lower() for k in ("canopy", "deck_plank", "entrance_concrete"))]
    for p in project_orthographic_view(roof_only, (0, 0, 1), (1, 0, 0), (0, 1, 0), to_roof, skip_seams=True):
        s.add(p)

    # Standing-seam Galvalume roof rib lines (455mm module) derived over House_Roof (-2.845..+2.845)
    for k in range(-6, 7):
        rx = k * 0.455
        if -2.82 <= rx <= 2.82:
            x0, y0 = to_roof(rx, -2.81)
            _, y1 = to_roof(rx, 2.81)
            s.add(f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x0:.1f}" y2="{y1:.1f}" stroke="#64748b" stroke-width="0.6"/>')

    # Bold Ridge Line at Y = +0.150 (EL +5.460m)
    rx0, ry = to_roof(-2.845, 0.150)
    rx1, _ = to_roof(2.845, 0.150)
    s.add(f'<line x1="{rx0:.1f}" y1="{ry:.1f}" x2="{rx1:.1f}" y2="{ry:.1f}" stroke="#0f172a" stroke-width="2.6"/>')
    s.add(f'<text x="{0.5*(rx0+rx1):.1f}" y="{ry - 7:.1f}" text-anchor="middle" style="font-size:9.5px;font-weight:800;fill:#0f172a;">RIDGE LINE EL +5.460m (Y = +150mm)</text>')

    # Slope Arrows (North 23.1° / 5.1:12, South 16.0° / 3.4:12)
    sx, sy_n0 = to_roof(0.0, 0.55)
    _, sy_n1 = to_roof(0.0, 2.35)
    s.add(f'<line x1="{sx:.1f}" y1="{sy_n0:.1f}" x2="{sx:.1f}" y2="{sy_n1:.1f}" stroke="#1d4ed8" stroke-width="1.6" marker-end="url(#arr-blue)"/>')
    s.add(f'<text x="{sx + 8:.1f}" y="{0.5*(sy_n0+sy_n1):.1f}" class="datum-txt">SLOPE 23.1° (4.26:10)</text>')
    s.add(f'<text x="{sx + 8:.1f}" y="{0.5*(sy_n0+sy_n1) + 12:.1f}" style="font-size:8.5px;fill:#334155;">EAVE EL +4.308m</text>')

    _, sy_s0 = to_roof(0.0, -0.30)
    _, sy_s1 = to_roof(0.0, -2.35)
    s.add(f'<line x1="{sx:.1f}" y1="{sy_s0:.1f}" x2="{sx:.1f}" y2="{sy_s1:.1f}" stroke="#1d4ed8" stroke-width="1.6" marker-end="url(#arr-blue)"/>')
    s.add(f'<text x="{sx + 8:.1f}" y="{0.5*(sy_s0+sy_s1):.1f}" class="datum-txt">SLOPE 16.0° (2.87:10)</text>')
    s.add(f'<text x="{sx + 8:.1f}" y="{0.5*(sy_s0+sy_s1) + 12:.1f}" style="font-size:8.5px;fill:#334155;">EAVE EL +4.568m</text>')

    # Dashed building wall outline below roof overhangs
    bx0, by1 = to_roof(-2.80, -2.73)
    bx1, by0 = to_roof(2.80, 2.73)
    s.add(f'<rect x="{bx0:.1f}" y="{by0:.1f}" width="{bx1 - bx0:.1f}" height="{by1 - by0:.1f}" fill="none" stroke="#475569" stroke-width="1.0" stroke-dasharray="5,3"/>')

    # Roof Dimensions & Callouts
    s.dim_h(to_roof(-2.845, 0)[0], to_roof(2.845, 0)[0], to_roof(0, 3.65)[1], "5,690 ROOF OVERALL (E–W)", ext_y=to_roof(0, 2.81)[1], color="#b91c1c")
    s.dim_v(to_roof(3.45, 0)[0], to_roof(0, 2.81)[1], to_roof(0, -2.81)[1], "5,620 ROOF OVERALL (N–S)", ext_x=to_roof(2.845, 0)[0], color="#b91c1c")
    s.leader_note(*to_roof(2.82, -2.84), 600, 915, ["ALUMINUM EAVE GUTTER &", "Ø50mm DOWNSPOUT (SE CORNER)", "DISCHARGE TO GRAVEL APRON"])
    s.leader_note(*to_roof(-3.20, 0.34), 100, 880, ["CANTILEVERED ALUM. ENTRY CANOPY", "820 × 1,122mm W/ TENSION STRUTS"])
    s.viewport_title(56, 1214, "1", "ROOF DRAINAGE & CLADDING PLAN", "1 : 50", width=440)

    # --- RIGHT VIEWPORT: ZAIRAI-KOHO STRUCTURAL TIMBER FRAMING PLAN (1:50) ---
    cx2, cy2 = 1220.0, 560.0
    def to_fr(u, v):
        return (cx2 + u * px_m, cy2 - v * px_m)

    for lbl, gx in GRID_X:
        s.grid_line_v(to_fr(gx, 0)[0], to_fr(0, 3.25)[1], to_fr(0, -3.55)[1], lbl, top_bubble=True)
    for lbl, gy in GRID_Y:
        s.grid_line_h(to_fr(0, gy)[1], to_fr(-3.35, 0)[0], to_fr(3.30, 0)[0], lbl, left_bubble=True)

    # Structural perimeter wall plates / shear wall panels (derived from exact model walls)
    wx0, wy1 = to_fr(-2.80, -2.73)
    wx1, wy0 = to_fr(2.80, 2.73)
    s.add(f'<rect x="{wx0:.1f}" y="{wy0:.1f}" width="{wx1 - wx0:.1f}" height="{wy1 - wy0:.1f}" fill="#fdfcf8" stroke="#0f172a" stroke-width="1.2"/>')
    # Shear wall bold zones (West gable, East gable, North rear wall, Front-Right solid wall)
    for (x0m, y0m, x1m, y1m) in [(-2.80, -2.73, -2.64, 2.73), (2.64, -2.73, 2.80, 2.73), (-2.64, 2.57, 2.64, 2.73), (1.12, -2.73, 2.64, -2.57)]:
        sx0, sy1 = to_fr(x0m, y0m)
        sx1, sy0 = to_fr(x1m, y1m)
        s.add(f'<rect x="{sx0:.1f}" y="{sy0:.1f}" width="{sx1-sx0:.1f}" height="{sy1-sy0:.1f}" fill="url(#hatch-wall-cut)" stroke="#0f172a" stroke-width="1.6"/>')

    # Loft Floor Joists @ 455mm O.C. inside L-shaped loft (Y=0.15..2.57 and X=0.85..2.64)
    # Rear bay joists running N-S
    for jx in [round(-2.64 + i * 0.455, 3) for i in range(1, 12)]:
        if jx < 2.60:
            x0, y0 = to_fr(jx, 0.24)
            _, y1 = to_fr(jx, 2.57)
            s.add(f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x0:.1f}" y2="{y1:.1f}" stroke="#92400e" stroke-width="0.95" stroke-dasharray="6,3"/>')
    # East wing joists running E-W
    for jy in [round(-2.57 + i * 0.455, 3) for i in range(1, 6)]:
        if jy < 0.08:
            x0, y0 = to_fr(0.94, jy)
            x1, _ = to_fr(2.64, jy)
            s.add(f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y0:.1f}" stroke="#92400e" stroke-width="0.95" stroke-dasharray="6,3"/>')

    # Primary Structural Timber Beams (EXACT model coords: Loft_Fascia_Beam_Rear, Loft_Fascia_Beam_Right, Ceiling_Ridge_Beam)
    beams = [
        (-2.64, 0.09, 0.79, 0.27, "G-1: 180×205 LOFT RIM GIRDER"),
        (0.79, -2.57, 0.97, 0.27, "G-2: 180×205 LOFT RIM GIRDER"),
        (-2.64, 0.08, 2.64, 0.22, "RB-1: 140×180 RIDGE BEAM (+5.16m)"),
    ]
    for (x0m, y0m, x1m, y1m, _) in beams[:2]:
        bx0, by1 = to_fr(x0m, y0m)
        bx1, by0 = to_fr(x1m, y1m)
        s.add(f'<rect x="{bx0:.1f}" y="{by0:.1f}" width="{bx1-bx0:.1f}" height="{by1-by0:.1f}" fill="#f6ead8" stroke="#0f172a" stroke-width="1.8"/>')
    # Ridge beam dashed centerline over G-1 & east span
    r_x0, r_y = to_fr(-2.64, 0.15)
    r_x1, _ = to_fr(2.64, 0.15)
    s.add(f'<line x1="{r_x0:.1f}" y1="{r_y:.1f}" x2="{r_x1:.1f}" y2="{r_y:.1f}" stroke="#b91c1c" stroke-width="2.0" stroke-dasharray="10,4"/>')

    # Perimeter 105×105mm Hinoki/Cedar Structural Posts (at exact 910mm half-ken intervals!)
    post_coords = []
    for px in (-2.72, 2.72):
        for py in (-2.65, -1.74, -0.83, 0.15, 1.06, 1.85, 2.65):
            post_coords.append((px, py))
    for px in (-1.75, -0.78, 0.85, 1.78):
        post_coords.append((px, 2.65))
    post_coords.append((1.14, -2.65))
    post_coords.append((1.96, -2.65))
    for (px, py) in post_coords:
        sx, sy = to_fr(px, py)
        hw = 0.0525 * px_m
        s.timber_section(sx - hw, sy - hw, hw * 2, hw * 2)

    # Twin Central Turned Cedar Columns (Ø176mm @ (-0.78, 0.15) and (+0.85, 0.15))
    for idx, (cxm, cym) in enumerate([(-0.78, 0.15), (0.85, 0.15)], start=1):
        sx, sy = to_fr(cxm, cym)
        r = 0.088 * px_m
        s.add(f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="{r:.1f}" fill="#d97706" fill-opacity="0.35" stroke="#0f172a" stroke-width="2.2"/>')
        s.add(f'<circle cx="{sx:.1f}" cy="{sy:.1f}" r="2.2" fill="#0f172a"/>')
        s.tag_badge(sx, sy - 20, f"C-{idx}", shape="rect", stroke="#b91c1c")

    # Stair Structural Stringers
    for stx in (-2.60, -1.96):
        x0, y0 = to_fr(stx, -2.05)
        _, y1 = to_fr(stx, 0.15)
        s.add(f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x0:.1f}" y2="{y1:.1f}" stroke="#0f172a" stroke-width="2.0"/>')

    # Framing Callouts & Structural Legend
    s.leader_note(*to_fr(-0.78, 0.15), 955, 865, ["C-1 / C-2: Ø176mm TURNED CEDAR", "FULL HEIGHT EL +0.36 → +5.32m", "CONCEALED STEEL CAP TO RIDGE"], align="left")
    s.leader_note(*to_fr(0.88, -1.20), 1310, 885, ["G-1 / G-2: 180×205mm LOFT", "RIM GIRDERS (EL +2.32..+2.52m)", "45×96 JOISTS @ 455mm O.C."], align="left")
    s.leader_note(*to_fr(1.80, 0.15), 1310, 185, ["RB-1: 140×180mm RIDGE BEAM", "45×100 ROOF RAFTERS @ 455 O.C.", "12mm PLYWOOD DIAPHRAGM DECK"], align="left")
    s.leader_note(*to_fr(-2.72, 1.06), 920, 185, ["105×105mm HINOKI POSTS", "@ 910mm HALF-KEN MODULE", "+ 12mm JAS SHEAR SHEATHING"], align="right")

    s.viewport_title(860, 1214, "2", "ZAIRAI-KOHO TIMBER FRAMING & SHEAR PLAN", "1 : 50", width=520)
    s.scale_bar(530, 1212, px_m, (0, 1, 2, 3))
    s.save(os.path.join(DRAWINGS_DIR, "A-103_Roof_Structural_Framing_Plan.svg"))
    print("Generated A-103_Roof_Structural_Framing_Plan.svg")


# =========================================================================
# SHEET A-104: REFLECTED CEILING & ARCHITECTURAL LIGHTING PLAN (1:50)
# =========================================================================
def build_a104():
    s = SvgSheet("A-104", "REFLECTED CEILING & LIGHTING PLAN", "1 : 50", "9TS-KOI-B1-ZZ-DR-E-0104", "ARCHITECTURAL LIGHTING")
    house_objs = get_group_meshes({"House_Group"})

    px_m = 92.0

    def draw_fixture_symbol(x, y, kind, tag, radius=9, label_pos="right"):
        if kind == "pendant":
            s.add(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{radius}" fill="#fef3c7" stroke="#0f172a" stroke-width="1.5"/>')
            s.add(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.2" fill="#0f172a"/>')
        elif kind == "downlight":
            s.add(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="7" fill="#ffffff" stroke="#0f172a" stroke-width="1.4"/>')
            s.add(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.5" fill="#fef3c7" stroke="#0f172a" stroke-width="0.9"/>')
        elif kind == "drum":
            s.add(f'<rect x="{x-14:.1f}" y="{y-14:.1f}" width="28" height="28" fill="#fef3c7" stroke="#0f172a" stroke-width="1.5"/>')
            s.add(f'<rect x="{x-10:.1f}" y="{y-10:.1f}" width="20" height="20" fill="#ffffff" stroke="#64748b" stroke-width="0.8"/>')
        elif kind == "sconce":
            s.add(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="6" fill="#fef3c7" stroke="#0f172a" stroke-width="1.4"/>')
            s.add(f'<line x1="{x-9:.1f}" y1="{y:.1f}" x2="{x+9:.1f}" y2="{y:.1f}" stroke="#0f172a" stroke-width="1.4"/>')
        if label_pos == "left":
            s.add(f'<text x="{x - 13:.1f}" y="{y + 3.5:.1f}" text-anchor="end" style="font-size:8.6px;font-weight:800;fill:#b91c1c;">{tag}</text>')
        elif label_pos == "below":
            s.add(f'<text x="{x:.1f}" y="{y + 18:.1f}" text-anchor="middle" style="font-size:8.4px;font-weight:800;fill:#b91c1c;">{tag}</text>')
        else:
            s.add(f'<text x="{x + 14:.1f}" y="{y + 3.5:.1f}" style="font-size:8.6px;font-weight:800;fill:#b91c1c;">{tag}</text>')

    # --- LEFT: 1F REFLECTED CEILING PLAN ---
    cx1, cy1 = 445.0, 520.0
    def to_rcp1(u, v):
        return (cx1 + u * px_m, cy1 - v * px_m)

    for lbl, gx in GRID_X:
        s.grid_line_v(to_rcp1(gx, 0)[0], to_rcp1(0, 3.15)[1], to_rcp1(0, -3.35)[1], lbl, top_bubble=True)
    for lbl, gy in GRID_Y:
        s.grid_line_h(to_rcp1(0, gy)[1], to_rcp1(-3.35, 0)[0], to_rcp1(3.20, 0)[0], lbl, left_bubble=True)

    # Cut walls at Z=2.15m for crisp ceiling boundary
    for c in slice_objects_at_plane(house_objs, (0, 0, 2.15), (0, 0, 1), (1, 0, 0), (0, 1, 0), to_rcp1):
        s.add(c)

    # Flat Plywood Loft Underside Soffit (EL +2.360m) shaded subtly
    # Rear bay (-2.64..2.64, 0.15..2.57) and East bay (0.85..2.64, -2.57..0.15)
    p1x0, p1y1 = to_rcp1(-2.64, 0.15)
    p1x1, p1y0 = to_rcp1(2.64, 2.57)
    s.add(f'<rect x="{p1x0:.1f}" y="{p1y0:.1f}" width="{p1x1-p1x0:.1f}" height="{p1y1-p1y0:.1f}" fill="#f7efe2" fill-opacity="0.55" stroke="#0f172a" stroke-width="1.2"/>')
    p2x0, p2y1 = to_rcp1(0.85, -2.57)
    p2x1, p2y0 = to_rcp1(2.64, 0.15)
    s.add(f'<rect x="{p2x0:.1f}" y="{p2y0:.1f}" width="{p2x1-p2x0:.1f}" height="{p2y1-p2y0:.1f}" fill="#f7efe2" fill-opacity="0.55" stroke="#0f172a" stroke-width="1.2"/>')

    # Double-height sloped ceiling zone label
    s.add(f'<text x="{to_rcp1(-0.90, -1.95)[0]:.1f}" y="{to_rcp1(-0.90, -1.95)[1]:.1f}" text-anchor="middle" style="font-size:9.5px;font-weight:700;fill:#475569;">DOUBLE-HEIGHT SLOPED BIRCH PLYWOOD CEILING</text>')
    s.add(f'<text x="{to_rcp1(-0.90, -2.18)[0]:.1f}" y="{to_rcp1(-0.90, -2.18)[1]:.1f}" text-anchor="middle" style="font-size:8.5px;font-weight:600;fill:#64748b;">EL +4.550m (S) → EL +5.330m (RIDGE)</text>')

    # Plot ACTUAL modeled 1F Fixtures from Blender exact coordinates!
    draw_fixture_symbol(*to_rcp1(-0.35, -1.40), "pendant", "L-01A (2.38m)")
    draw_fixture_symbol(*to_rcp1(-1.30, -1.15), "pendant", "L-01B (3.25m)")

    # L-02 Kitchen Duct Rail + 3 Track Spots (X=1.62, Y=-2.15..-0.45 @ Z=2.345)
    kx, ky1 = to_rcp1(1.62, -2.15)
    _, ky0 = to_rcp1(1.62, -0.45)
    s.add(f'<line x1="{kx:.1f}" y1="{ky0:.1f}" x2="{kx:.1f}" y2="{ky1:.1f}" stroke="#0f172a" stroke-width="3.2"/>')
    for sy in (-1.95, -1.30, -0.65):
        tx, ty = to_rcp1(1.62, sy)
        s.add(f'<circle cx="{tx:.1f}" cy="{ty:.1f}" r="5.5" fill="#fef3c7" stroke="#0f172a" stroke-width="1.3"/>')
    s.add(f'<text x="{kx + 11:.1f}" y="{0.5*(ky0+ky1):.1f}" style="font-size:8.8px;font-weight:800;fill:#b91c1c;">L-02 (3× SPOT)</text>')

    # L-03 Tatami Shoji Drum (-0.69, 1.66) + L-04 Cove LED (-1.94, 0.96..2.36)
    draw_fixture_symbol(*to_rcp1(-0.69, 1.66), "drum", "L-03 (2.33m)")
    cv_x, cv_y1 = to_rcp1(-1.94, 0.96)
    _, cv_y0 = to_rcp1(-1.94, 2.36)
    s.add(f'<line x1="{cv_x:.1f}" y1="{cv_y0:.1f}" x2="{cv_x:.1f}" y2="{cv_y1:.1f}" stroke="#d97706" stroke-width="3.2" stroke-dasharray="5,2"/>')
    s.add(f'<text x="{cv_x + 8:.1f}" y="{cv_y0 + 14:.1f}" style="font-size:8.2px;font-weight:800;fill:#b91c1c;">L-04 COVE</text>')

    # L-07 Vanity Bar + L-08 Downlights + L-09 Porch Sconce
    vb_x, vb_y1 = to_rcp1(0.85, 0.94)
    _, vb_y0 = to_rcp1(0.85, 1.60)
    s.add(f'<line x1="{vb_x:.1f}" y1="{vb_y0:.1f}" x2="{vb_x:.1f}" y2="{vb_y1:.1f}" stroke="#d97706" stroke-width="3.4"/>')
    s.add(f'<text x="{vb_x + 7:.1f}" y="{vb_y0 + 10:.1f}" style="font-size:8px;font-weight:800;fill:#b91c1c;">L-07</text>')

    draw_fixture_symbol(*to_rcp1(1.38, 1.27), "downlight", "L-08A", label_pos="below")
    draw_fixture_symbol(*to_rcp1(2.26, 1.25), "downlight", "L-08B", label_pos="below")
    draw_fixture_symbol(*to_rcp1(1.90, 2.15), "downlight", "L-08C")
    draw_fixture_symbol(*to_rcp1(-2.85, 0.76), "sconce", "L-09", label_pos="left")

    # Curved dashed architectural switch legs (from entry switch bank at X=-2.50, Y=-0.10)
    swx, swy = to_rcp1(-2.55, -0.15)
    s.add(f'<text x="{swx + 4:.1f}" y="{swy + 4:.1f}" style="font-size:10px;font-weight:900;fill:#1d4ed8;">$d</text>')
    for target_pt in [(-1.30, -1.15), (-0.35, -1.40), (-0.69, 1.66)]:
        tx, ty = to_rcp1(*target_pt)
        mx, my = 0.5*(swx+tx) - 22, 0.5*(swy+ty) + 18
        s.add(f'<path d="M {swx:.1f} {swy:.1f} Q {mx:.1f} {my:.1f} {tx:.1f} {ty:.1f}" fill="none" stroke="#1d4ed8" stroke-width="0.9" stroke-dasharray="4,3"/>')

    s.viewport_title(56, 860, "1", "1F REFLECTED CEILING & SWITCHING PLAN", "1 : 50", width=470)

    # --- RIGHT: 2F SLOPED ROOF CEILING & RIDGE TRACK PLAN ---
    cx2, cy2 = 1220.0, 520.0
    def to_rcp2(u, v):
        return (cx2 + u * px_m, cy2 - v * px_m)

    for lbl, gx in GRID_X:
        s.grid_line_v(to_rcp2(gx, 0)[0], to_rcp2(0, 3.15)[1], to_rcp2(0, -3.35)[1], lbl, top_bubble=True)
    for lbl, gy in GRID_Y:
        s.grid_line_h(to_rcp2(0, gy)[1], to_rcp2(-3.20, 0)[0], to_rcp2(3.20, 0)[0], lbl, left_bubble=True)

    for c in slice_objects_at_plane(house_objs, (0, 0, 3.55), (0, 0, 1), (1, 0, 0), (0, 1, 0), to_rcp2):
        s.add(c)

    # Ridge beam & ceiling slope boundary
    rx0, ry = to_rcp2(-2.64, 0.15)
    rx1, _ = to_rcp2(2.64, 0.15)
    s.add(f'<rect x="{rx0:.1f}" y="{ry - 6.5:.1f}" width="{rx1 - rx0:.1f}" height="13" fill="#f6ead8" stroke="#0f172a" stroke-width="1.4"/>')
    s.add(f'<text x="{0.5*(rx0+rx1):.1f}" y="{ry - 12:.1f}" text-anchor="middle" style="font-size:8.8px;font-weight:800;fill:#0f172a;">EXPOSED RIDGE BEAM (EL +5.160m) + DUCT RAIL L-05</text>')

    # L-05 Ridge-Beam Duct Rail (X=-1.60..+1.80, Y=0.15 @ Z=5.146) + 3 Track Spots
    rt0, rty = to_rcp2(-1.60, 0.15)
    rt1, _ = to_rcp2(1.80, 0.15)
    s.add(f'<line x1="{rt0:.1f}" y1="{rty:.1f}" x2="{rt1:.1f}" y2="{rty:.1f}" stroke="#b91c1c" stroke-width="3.4"/>')
    for idx, sx_m in enumerate((-1.20, 0.05, 1.35), start=1):
        px, py = to_rcp2(sx_m, 0.15)
        s.add(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="6" fill="#fef3c7" stroke="#0f172a" stroke-width="1.4"/>')
        s.add(f'<text x="{px:.1f}" y="{py + 18:.1f}" text-anchor="middle" style="font-size:8.2px;font-weight:800;fill:#b91c1c;">L-05.{idx}</text>')

    # L-06 Bedside Brass & Opal Sconce (-1.04, 2.55, Z=3.18)
    draw_fixture_symbol(*to_rcp2(-1.04, 2.46), "sconce", "L-06 (3.18m)")
    # Show pendant canopies mounted on South sloped ceiling
    draw_fixture_symbol(*to_rcp2(-0.35, -1.40), "pendant", "L-01A CANOPY", radius=6)
    draw_fixture_symbol(*to_rcp2(-1.30, -1.15), "pendant", "L-01B CANOPY", radius=6)

    s.viewport_title(860, 860, "2", "2F SLOPED CEILING & RIDGE TRACK PLAN", "1 : 50", width=470)

    # --- BOTTOM STRIP: ARCHITECTURAL LUMINAIRE SCHEDULE (ALL 9 MODELED FIXTURE TYPES) ---
    s.add('<rect x="52" y="905" width="1542" height="320" fill="#ffffff" stroke="#0f172a" stroke-width="1.5"/>')
    s.add('<rect x="52" y="905" width="1542" height="28" fill="#0f172a"/>')
    s.add('<text x="68" y="924" style="font-size:11.5px;font-weight:800;fill:#ffffff;letter-spacing:1px;">ARCHITECTURAL LUMINAIRE SCHEDULE (36 MODELED MESHES · CALIBRATED 2700K–3000K LED · ZERO AR BLOWOUT)</text>')

    cols = [(64, "MARK"), (130, "FIXTURE TYPE & DESCRIPTION"), (480, "MOUNTING"), (630, "ELEV (Z)"), (730, "LAMP / CCT"), (870, "QTY"), (930, "BLENDER / IFC ELEMENT GROUP"), (1260, "CONTROL / LOCATION")]
    s.add('<rect x="52" y="933" width="1542" height="22" fill="#e2e8f0" stroke="#cbd5e1" stroke-width="0.8"/>')
    for cx_c, hlbl in cols:
        s.add(f'<text x="{cx_c}" y="948" class="tb-lbl">{hlbl}</text>')

    l_rows = [
        ("L-01A", "Koizumi Spun Enamel Dining Cord Pendant (Ø360mm)", "Sloped Canopy", "+2.38m", "8W LED 2700K", "1", "Fixture_Dining_Pendant_*", "Dimmer · 1F Dining"),
        ("L-01B", "Koizumi Spun Enamel Living Void Pendant (Ø280mm)", "Sloped Canopy", "+3.25m", "7W LED 2700K", "1", "Fixture_Living_Pendant_*", "Dimmer · Double-Height"),
        ("L-02",  "Ceiling Duct Rail (1,750mm) + 3× Directional Spots", "Surface Ceiling", "+2.35m", "3×6W 2800K", "3", "Fixture_Kitchen_Track / Spot_*", "Switch · 1F Kitchen"),
        ("L-03",  "Hinoki-Framed Opal Shoji Square Luminaire (480×480)", "Flush Ceiling", "+2.33m", "12W LED 2700K", "1", "Fixture_Tatami_Ceiling*", "Dimmer · 1F Tatami"),
        ("L-04",  "Anodized Aluminum Linear LED Cove Strip (1,400mm)", "Wall Base Cove", "+0.56m", "6W/m 2400K", "1", "Fixture_Tatami_Cove*", "Switch · Tatami Alcove"),
        ("L-05",  "Ridge-Beam Duct Rail (3,400mm) + 3× Cylinder Spots", "Ridge Underside", "+5.15m", "3×7W 2800K", "3", "Fixture_Loft_RidgeTrack / Spot_*", "3-Way · 2F Loft & Bed"),
        ("L-06",  "Brushed Brass & Opal Glass Globe Wall Sconce", "Wall Mounted", "+3.18m", "4W LED 2700K", "1", "Fixture_Bed_Sconce*", "Local · 2F Bedside"),
        ("L-07",  "Linear Opal Glass Architectural Vanity Bar (660mm)", "Over Mirror", "+2.27m", "9W LED 3000K", "1", "Fixture_Bath_VanityBar*", "Switch · Bath Vanity"),
        ("L-08",  "IP65 Wet-Rated Recessed Trim Downlight (Ø136mm)", "Recessed Clg", "+2.36m", "3×6W 3000K", "3", "Fixture_Bath_*_Downlight_*", "Switch · Vest/WC/Shwr"),
        ("L-09",  "Weatherproof Matte-Black Exterior Porch Sconce", "Ext Wall Hood", "+2.04m", "5W LED 2700K", "1", "Fixture_Entry_PorchSconce*", "Dusk Sensor · Entry"),
    ]
    for i, r in enumerate(l_rows):
        ry = 955 + i * 26.5
        bg = "#ffffff" if i % 2 == 0 else "#f8fafc"
        s.add(f'<rect x="52" y="{ry:.1f}" width="1542" height="26.5" fill="{bg}" stroke="#e2e8f0" stroke-width="0.6"/>')
        for j, val in enumerate(r):
            c_x = cols[j][0]
            st = "font-size:9.5px;font-weight:800;fill:#b91c1c;" if j == 0 else "font-size:9.3px;font-weight:600;fill:#0f172a;"
            s.add(f'<text x="{c_x}" y="{ry + 17:.1f}" style="{st}">{val}</text>')

    s.save(os.path.join(DRAWINGS_DIR, "A-104_Reflected_Ceiling_Lighting_Plan.svg"))
    print("Generated A-104_Reflected_Ceiling_Lighting_Plan.svg")


# =========================================================================
# SHEET A-201: ALL 4 EXTERIOR ELEVATIONS (1:50, 100% MODEL-PROJECTED!)
# =========================================================================
def build_a201():
    s = SvgSheet("A-201", "EXTERIOR ELEVATIONS", "1 : 50 (4 FACADES)", "9TS-KOI-B1-ZZ-DR-A-0201", "ARCHITECTURE")
    # Include House_Group + Roof_Group (pure architecture!)
    objs = get_group_meshes({"House_Group", "Roof_Group"})

    px_m = 74.0  # 5.6m = 414px, 5.46m height = 404px -> 2x2 grid fits 4 elevations cleanly with datums & notes!

    elev_specs = [
        ("1", "SOUTH (FRONT) ELEVATION — ENGAWA & 2-STORY SHOJI FACADE", 410.0, 515.0, (0, -1, 0), (1, 0, 0), (0, 0, 1), True),
        ("2", "WEST (ENTRANCE) ELEVATION — CANOPY & GALVALUME GABLE",    1190.0, 515.0, (-1, 0, 0), (0, -1, 0), (0, 0, 1), False),
        ("3", "NORTH (REAR) ELEVATION — 2F SLIDING WINDOW & JIMADO",      410.0, 1115.0, (0, 1, 0), (-1, 0, 0), (0, 0, 1), True),
        ("4", "EAST (SIDE) ELEVATION — KITCHEN, WC & SHOWER WINDOWS",    1190.0, 1115.0, (1, 0, 0), (0, 1, 0), (0, 0, 1), False),
    ]

    datums = [
        ("RIDGE", "EL +5.460", 5.460),
        ("S. EAVE", "EL +4.568", 4.568),
        ("N. EAVE", "EL +4.308", 4.308),
        ("2F FFL", "EL +2.520", 2.520),
        ("1F FFL", "EL +0.360", 0.360),
        ("GL", "EL ±0.000", 0.000),
    ]

    for num, title, cx, base_y, vdir, ua, va, is_ew in elev_specs:
        def to_el(u, v, _cx=cx, _by=base_y):
            return (_cx + u * px_m, _by - v * px_m)

        # Ground Grade Line & Earth Sub-grade Strip
        g_x0 = cx - 345
        g_x1 = cx + 335
        s.add(f'<rect x="{g_x0:.1f}" y="{base_y:.1f}" width="{g_x1 - g_x0:.1f}" height="14" fill="url(#hatch-earth)"/>')
        s.add(f'<line x1="{g_x0:.1f}" y1="{base_y:.1f}" x2="{g_x1:.1f}" y2="{base_y:.1f}" stroke="#0f172a" stroke-width="2.4"/>')

        # True 3D Orthographic Model Projection!
        polys = project_orthographic_view(objs, vdir, ua, va, to_el, skip_seams=False)
        s.add(f'<g id="elev-{num}">')
        for p in polys:
            s.add(p)
        s.add('</g>')

        # Datum Level Lines on right side of each elevation (avoid overlapping close eaves)
        for dcode, delv, dz in datums:
            if num == "1" and dcode == "N. EAVE":
                continue
            if num == "3" and dcode == "S. EAVE":
                continue
            if num in ("2", "4") and dcode == "N. EAVE":
                # Place North Eave datum cleanly on the left side on gable views!
                s.datum_level(cx - 275, cx - 220, base_y - dz * px_m, dcode, delv, label_side="left")
                continue
            if dcode == "1F FFL" and num == "2":
                # Keep 1F FFL clear of Engawa on West elevation
                s.datum_level(cx - 275, cx - 220, base_y - dz * px_m, dcode, delv, label_side="left")
                continue
            dy = base_y - dz * px_m
            s.datum_level(cx + 220, cx + 275, dy, dcode, delv, label_side="right")

        # Overall Width & Ridge Height Dimensions
        if is_ew:
            s.dim_h(to_el(-2.80, 0)[0], to_el(2.80, 0)[0], base_y + 34, "5,600 WALL EXTENTS (18'-4\")", ext_y=base_y + 4)
        else:
            s.dim_h(to_el(-2.73, 0)[0], to_el(2.73, 0)[0], base_y + 34, "5,460 = 3.0 KEN (17'-11\")", ext_y=base_y + 4)
        s.dim_v(cx - 235, base_y - 5.460 * px_m, base_y, "5,460 RIDGE", ext_x=cx - 208, color="#b91c1c")

        # Specific Architectural Keynotes per Facade (placed cleanly outside dim lines!)
        if num == "1":
            s.leader_note(*to_el(-1.70, 3.50), cx - 256, base_y - 315, ["2-STORY ALUMINUM", "& SHOJI CURTAIN", "W-01 (3,900×4,260)"], align="right")
            s.leader_note(*to_el(1.96, 3.10), cx + 225, base_y - 255, ["GALVALUME WHITE", "VERTICAL SIDING", "W/ 683mm MODULE"], align="left")
            s.leader_note(*to_el(-0.50, 0.28), cx - 256, base_y - 58, ["CEDAR ENGAWA DECK", "ON PRECAST PIERS"], align="right")
        elif num == "2":
            # Pitch Triangle Annotations on West Gable!
            s.add(f'<polygon points="{cx - 105:.1f},{base_y - 398:.1f} {cx - 65:.1f},{base_y - 398:.1f} {cx - 65:.1f},{base_y - 415:.1f}" fill="none" stroke="#1d4ed8" stroke-width="1.2"/>')
            s.add(f'<text x="{cx - 110:.1f}" y="{base_y - 418:.1f}" class="datum-txt">23.1° N</text>')
            s.add(f'<polygon points="{cx + 95:.1f},{base_y - 398:.1f} {cx + 55:.1f},{base_y - 398:.1f} {cx + 55:.1f},{base_y - 410:.1f}" fill="none" stroke="#1d4ed8" stroke-width="1.2"/>')
            s.add(f'<text x="{cx + 68:.1f}" y="{base_y - 418:.1f}" class="datum-txt">16.0° S</text>')
            s.leader_note(*to_el(-0.34, 2.38), cx - 256, base_y - 210, ["ENTRY CANOPY", "ALUM. + STRUTS", "+ SCONCE L-09"], align="right")
            s.leader_note(*to_el(-0.88, 1.22), cx - 256, base_y - 118, ["MAILBOX, INTERCOM", "& WALL VENTS"], align="right")
        elif num == "3":
            s.tag_badge(*to_el(0.05, 3.58), "W-02", shape="hex", stroke="#1d4ed8")
            s.tag_badge(*to_el(0.75, 0.74), "W-03", shape="hex", stroke="#1d4ed8")
            s.tag_badge(*to_el(-1.77, 1.65), "W-04", shape="hex", stroke="#1d4ed8")
            s.leader_note(*to_el(0.05, 3.58), cx - 256, base_y - 295, ["2F BEDROOM SLIDING", "WINDOW W-02 (1800×560)", "SIGHTLINE TO KITTY"], align="right")
            s.leader_note(*to_el(0.75, 0.74), cx - 256, base_y - 95, ["TATAMI LOW JIMADO", "SHOJI WINDOW W-03"], align="right")
        elif num == "4":
            s.tag_badge(*to_el(-1.25, 1.58), "W-05", shape="hex", stroke="#1d4ed8")
            s.tag_badge(*to_el(1.37, 1.58), "W-06", shape="hex", stroke="#1d4ed8")
            s.leader_note(*to_el(-2.80, 2.60), cx - 256, base_y - 220, ["ALUMINUM DOWNSPOUT", "SE EAVE TO GRAVEL"], align="right")

        s.viewport_title(cx - 345, base_y + 72, num, title, "1 : 50", width=675)

    s.scale_bar(1400, 1218, px_m, (0, 1, 2))
    s.save(os.path.join(DRAWINGS_DIR, "A-201_Exterior_Elevations.svg"))
    print("Generated A-201_Exterior_Elevations.svg")


# =========================================================================
# SHEET A-301: BUILDING SECTIONS A-A & B-B (1:50, TRUE bmesh SLICES + FOOTINGS)
# =========================================================================
def build_a301():
    s = SvgSheet("A-301", "BUILDING SECTIONS A-A & B-B", "1 : 50", "9TS-KOI-B1-ZZ-DR-A-0301", "ARCHITECTURE / STRUCT")
    objs = get_group_meshes({"House_Group", "Roof_Group"})

    px_m = 92.0

    def draw_below_grade_footings(to_sec, u_min, u_max, has_center_pier=True):
        """Parametric LOD-400 RC Mat Slab & Perimeter Spread Footings anchored directly under Foundation_Plinth."""
        # Earth grade box below Z=0.00m
        gx0, gy0 = to_sec(u_min - 1.0, 0.0)
        gx1, gy1 = to_sec(u_max + 1.0, -0.78)
        s.add(f'<rect x="{gx0:.1f}" y="{gy0:.1f}" width="{gx1 - gx0:.1f}" height="{gy1 - gy0:.1f}" fill="url(#hatch-earth)"/>')
        s.add(f'<line x1="{gx0:.1f}" y1="{gy0:.1f}" x2="{gx1:.1f}" y2="{gy0:.1f}" stroke="#0f172a" stroke-width="2.2"/>')

        # 150mm Compacted Crushed Gravel Capillary Layer (EL -0.45 to -0.30m)
        gr0, gry0 = to_sec(u_min - 0.25, -0.30)
        gr1, gry1 = to_sec(u_max + 0.25, -0.45)
        s.add(f'<rect x="{gr0:.1f}" y="{gry0:.1f}" width="{gr1 - gr0:.1f}" height="{gry1 - gry0:.1f}" fill="url(#hatch-gravel)" stroke="#475569" stroke-width="0.9"/>')

        # Continuous RC Mat Foundation Slab (EL -0.30 to -0.12m) + Perimeter Spread Footings + Plinth Stem Walls
        # Build unified concrete foundation silhouette polygon
        pts_m = [
            (u_min, 0.32), (u_min + 0.16, 0.32), (u_min + 0.16, -0.12),
            (u_max - 0.16, -0.12), (u_max - 0.16, 0.32), (u_max, 0.32),
            (u_max, -0.15), (u_max + 0.18, -0.15), (u_max + 0.18, -0.30),
            (u_min - 0.18, -0.30), (u_min - 0.18, -0.15), (u_min, -0.15)
        ]
        pstr = " ".join(f"{to_sec(u, v)[0]:.1f},{to_sec(u, v)[1]:.1f}" for u, v in pts_m)
        s.add(f'<polygon points="{pstr}" fill="url(#hatch-concrete)" stroke="#0a0a0a" stroke-width="2.0"/>')

        # Rebar dashed line inside mat slab
        rb0, rby = to_sec(u_min - 0.12, -0.22)
        rb1, _ = to_sec(u_max + 0.12, -0.22)
        s.add(f'<line x1="{rb0:.1f}" y1="{rby:.1f}" x2="{rb1:.1f}" y2="{rby:.1f}" stroke="#b91c1c" stroke-width="1.2" stroke-dasharray="6,3"/>')

    # --- LEFT VIEWPORT: SECTION A-A (East-West Cut @ Y = -0.50m, Looking North) ---
    cx1, by1 = 420.0, 935.0
    def to_sa(u, v):
        return (cx1 + u * px_m, by1 - v * px_m)

    for lbl, gx in GRID_X:
        s.grid_line_v(to_sa(gx, 0)[0], to_sa(0, 6.05)[1], to_sa(0, -0.85)[1], lbl, top_bubble=True)

    draw_below_grade_footings(to_sa, -2.77, 2.77)

    # Interior elevation BEYOND cut plane Y >= -0.50m (looking North)
    proj_sa = project_orthographic_view(
        objs, view_dir=(0, -1, 0), u_axis=(1, 0, 0), v_axis=(0, 0, 1),
        to_svg_fn=to_sa, clip_plane=((0, -0.50, 0), (0, -1, 0)), skip_seams=True
    )
    for p in proj_sa:
        s.add(p)

    # TRUE bmesh Section Cut at Y = -0.50m
    cut_sa = slice_objects_at_plane(objs, (0, -0.50, 0), (0, -1, 0), (1, 0, 0), (0, 0, 1), to_sa)
    for c in cut_sa:
        s.add(c)

    # Datum Levels & Vertical Dimensions (Section A-A — clean non-overlapping primary datums)
    for dcode, delv, dz in [("RIDGE", "+5.460", 5.460), ("2F FFL", "+2.520", 2.520), ("1F FFL", "+0.360", 0.360), ("GL", "±0.000", 0.000), ("FTG BOT", "-0.300", -0.300)]:
        s.datum_level(to_sa(2.85, 0)[0], to_sa(3.30, 0)[0], to_sa(0, dz)[1], dcode, delv, label_side="right")

    s.dim_v(to_sa(-3.45, 0)[0], to_sa(0, 2.36)[1], to_sa(0, 0.36)[1], "2,000 1F CLR", ext_x=to_sa(-2.80, 0)[0])
    s.dim_v(to_sa(-3.45, 0)[0], to_sa(0, 5.33)[1], to_sa(0, 2.52)[1], "2,810 2F MAX", ext_x=to_sa(-2.80, 0)[0])
    s.dim_v(to_sa(-3.82, 0)[0], to_sa(0, 5.46)[1], to_sa(0, 0.00)[1], "5,460 OVERALL HEIGHT", ext_x=to_sa(-3.45, 0)[0], color="#b91c1c")

    # Space Labels inside Section A-A
    s.room_tag(*to_sa(-1.10, 1.35), "1F", "LIVING / STAIR VOID", "DOUBLE-HEIGHT")
    s.room_tag(*to_sa(1.75, 1.35), "1F", "KITCHEN", "CLG 2,000mm")
    s.room_tag(*to_sa(1.50, 3.55), "2F", "LOFT LOUNGE", "EL +2.520m")
    s.room_tag(*to_sa(-0.40, 3.65), "2F", "BEDROOM BEYOND", "SLIDING WIN W-02")

    # Detail Callout Bubbles pointing to A-501 & A-502
    s.detail_callout(*to_sa(-2.72, 0.15), 22, "2", "A-501", *to_sa(-3.25, -0.60))
    s.detail_callout(*to_sa(-2.25, 1.75), 24, "3", "A-502", *to_sa(-1.45, 2.85))
    s.detail_callout(*to_sa(0.85, 2.80), 22, "4", "A-502", *to_sa(0.05, 4.55))

    s.viewport_title(56, 1214, "1", "SECTION A-A (LONGITUDINAL E–W @ Y = -500mm, LOOKING NORTH)", "1 : 50", width=675)

    # --- RIGHT VIEWPORT: SECTION B-B (North-South Cut @ X = -0.40m, Looking East) ---
    cx2, by2 = 1210.0, 935.0
    def to_sb(u, v):
        # u = -Y (North +2.73 is u=-2.73 LEFT, South -2.73 is u=+2.73 RIGHT, Engawa -4.25 is u=+4.25 FAR RIGHT!)
        return (cx2 + u * px_m, by2 - v * px_m)

    for lbl, gy in GRID_Y:
        s.grid_line_v(to_sb(-gy, 0)[0], to_sb(0, 6.05)[1], to_sb(0, -0.85)[1], lbl, top_bubble=True)

    draw_below_grade_footings(to_sb, -2.70, 2.70)

    # Interior elevation BEYOND cut plane X >= -0.40m (looking East)
    proj_sb = project_orthographic_view(
        objs, view_dir=(-1, 0, 0), u_axis=(0, -1, 0), v_axis=(0, 0, 1),
        to_svg_fn=to_sb, clip_plane=((-0.40, 0, 0), (-1, 0, 0)), skip_seams=True
    )
    for p in proj_sb:
        s.add(p)

    # TRUE bmesh Section Cut at X = -0.40m
    cut_sb = slice_objects_at_plane(objs, (-0.40, 0, 0), (-1, 0, 0), (0, -1, 0), (0, 0, 1), to_sb)
    for c in cut_sb:
        s.add(c)

    # Datum Levels on Section B-B (clean vertical spacing)
    for dcode, delv, dz in [("RIDGE", "+5.460", 5.460), ("N. EAVE", "+4.308", 4.308), ("2F FFL", "+2.520", 2.520), ("1F FFL", "+0.360", 0.360), ("GL", "±0.000", 0.000)]:
        s.datum_level(to_sb(-3.15, 0)[0], to_sb(-2.85, 0)[0], to_sb(0, dz)[1], dcode, delv, label_side="left")
    s.datum_level(to_sb(2.85, 0)[0], to_sb(3.20, 0)[0], to_sb(0, 4.568)[1], "S. EAVE", "+4.568", label_side="right")

    # Space Labels inside Section B-B
    s.room_tag(*to_sb(-1.45, 1.40), "1F", "6-MAT TATAMI", "EL +0.520m")
    s.room_tag(*to_sb(1.30, 1.45), "1F", "DINING / LIVING", "PENDANT L-01A")
    s.room_tag(*to_sb(-1.40, 3.55), "2F", "BEDROOM LOFT", "W-02 REAR WIN")
    s.room_tag(*to_sb(3.45, 0.72), "EXT", "ENGAWA", "EL +0.320")

    # Detail Callout Bubbles pointing to A-501 & A-502
    s.detail_callout(*to_sb(-0.15, 5.25), 24, "4", "A-501", *to_sb(-1.45, 5.85))
    s.detail_callout(*to_sb(2.75, 4.55), 22, "3", "A-501", *to_sb(3.55, 5.25))
    s.detail_callout(*to_sb(2.68, 2.45), 24, "1", "A-502", *to_sb(3.75, 3.15))
    s.detail_callout(*to_sb(-2.65, 3.58), 22, "2", "A-502", *to_sb(-3.40, 3.65))
    s.detail_callout(*to_sb(3.35, 0.18), 24, "2", "A-501", *to_sb(3.75, -0.55))

    s.viewport_title(855, 1214, "2", "SECTION B-B (TRANSVERSE N–S @ X = -400mm, LOOKING EAST)", "1 : 50", width=675)
    s.scale_bar(755, 1140, px_m, (0, 1, 2))
    s.save(os.path.join(DRAWINGS_DIR, "A-301_Building_Sections.svg"))
    print("Generated A-301_Building_Sections.svg")


def main():
    build_a000()
    build_a100()
    build_a101()
    build_a102()
    build_a103()
    build_a104()
    build_a201()
    build_a301()
    print("=== PART 1 COMPLETE (8 SHEETS: A-000 .. A-301) ===")

if __name__ == "__main__":
    main()
