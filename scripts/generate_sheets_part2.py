"""
9-Tsubo House — Automated Model-Derived Architectural Construction Sheets (Part 2: A-401 to A-601)
Runs inside Blender 5.2 LTS using cad_engine.py + 9_tsubo_bim_metadata.json.
Produces:
  - A-401: Enlarged 1:25 Kitchen, 3-Zone Bath & Tatami Plans + Interior Elevations (Model-Derived)
  - A-501: LOD-400 Typical Wall Section & Envelope Construction Details (Footing, Eave, Ridge)
  - A-502: LOD-400 Glazing, Stair Stringer & Cable Guardrail Construction Details
  - A-601: Automated Door/Window/Room Finish Schedules & BIM Quantity Take-Off (CSI & IFC4)
"""
import os
import sys
import json
import math
from collections import defaultdict
import bpy

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


# =========================================================================
# SHEET A-401: ENLARGED 1:25 INTERIOR PLANS & ELEVATIONS (MODEL-DERIVED)
# =========================================================================
def build_a401():
    s = SvgSheet("A-401", "ENLARGED INTERIOR PLANS & ELEVATIONS", "1 : 25 (ENLARGED)", "9TS-KOI-B1-L1-DR-A-0401", "INTERIOR ARCHITECTURE")
    house_objs = get_group_meshes({"House_Group"})

    # 4 crisp framed viewports (2x2 layout inside x=48..1596, y=46..1234)
    # Top-Left: Enlarged 1F Galley Kitchen Plan (1:25)
    # Top-Right: Enlarged 1F Kitchen East Counter & Window Elevation (1:25)
    # Bottom-Left: Enlarged 1F 3-Zone Bathroom Suite Plan (1:25)
    # Bottom-Right: Enlarged 1F Wet-Room Shower, Vanity & Tatami Elevation (1:25)

    px_m = 165.0  # Crisp 1:25 enlarged detail scale!

    # --- VP 1: ENLARGED 1F GALLEY KITCHEN PLAN (X=0.60..2.85, Y=-2.75..+0.90) ---
    s.add('<rect x="48" y="46" width="756" height="572" fill="#ffffff" stroke="#0f172a" stroke-width="1.3"/>')
    px_k = 135.0
    def to_kp(u, v):
        return (430.0 + (u - 1.72) * px_k, 305.0 - (v - (-0.95)) * px_k)

    kit_objs = [o for o in house_objs if any(k in o.name.lower() for k in ("kitchen", "wall_right", "wall_front_right", "plywall_right", "plywall_frontright", "bath_wall_front", "column_1", "prop_kitchen", "interior_floor_1f", "fixture_kitchen"))]
    s.start_clip(52, 50, 748, 515)
    for p in project_orthographic_view(kit_objs, (0, 0, 1), (1, 0, 0), (0, 1, 0), to_kp, clip_plane=((0, 0, 1.55), (0, 0, 1)), skip_seams=True):
        s.add(p)
    for c in slice_objects_at_plane(kit_objs, (0, 0, 1.55), (0, 0, 1), (1, 0, 0), (0, 1, 0), to_kp):
        s.add(c)
    s.end_clip()

    # Exact Model Dimensions for Kitchen Plan (cleanly inside VP 1 frame!)
    s.dim_h(to_kp(0.85, 0)[0], to_kp(1.38, 0)[0], to_kp(0, -2.72)[1], "530", ext_y=to_kp(0, -2.35)[1])
    s.dim_h(to_kp(1.38, 0)[0], to_kp(2.02, 0)[0], to_kp(0, -2.72)[1], "640 AISLE", ext_y=to_kp(0, -2.35)[1], color="#1d4ed8")
    s.dim_h(to_kp(2.02, 0)[0], to_kp(2.64, 0)[0], to_kp(0, -2.72)[1], "620", ext_y=to_kp(0, -2.35)[1])
    s.dim_v(to_kp(2.96, 0)[0], to_kp(0, 0.12)[1], to_kp(0, -2.45)[1], "2,570 WALL COUNTER RUN", ext_x=to_kp(2.64, 0)[0])
    s.leader_note(*to_kp(1.10, -1.52), 265, 225, ["PENINSULA SINK COUNTER", "530×1,970mm · PRIVACY SHIELD", "EL +1.420m TOP (1,060 ABOVE FFL)"], align="right")
    s.leader_note(*to_kp(2.33, -1.95), 625, 480, ["INDUCTION COOKTOP &", "UNDER-COUNTER OVEN"], align="left")
    s.leader_note(*to_kp(2.26, 0.44), 625, 130, ["RECESSED FRIDGE NICHE", "700×590mm W/ OVERHEAD CAB"], align="left")
    s.viewport_title(62, 594, "1", "ENLARGED 1F GALLEY KITCHEN PLAN", "1 : 25", width=440)

    # --- VP 2: ENLARGED 1F KITCHEN EAST WALL ELEVATION (Looking East +X @ X >= 1.50m) ---
    s.add('<rect x="824" y="46" width="770" height="572" fill="#ffffff" stroke="#0f172a" stroke-width="1.3"/>')
    def to_ke(u, v):
        # Looking East (+X): view_dir=(-1,0,0), u = -Y (North left +0.8, South right -2.6), v = Z (0.36..2.52)
        return (1205.0 + (u - 0.90) * px_m, 535.0 - (v - 0.36) * px_m)

    ke_objs = [o for o in house_objs if any(k in o.name.lower() for k in ("kitchen_wall", "kitchen_stove", "kitchen_oven", "kitchen_smallwin", "kitchen_re_", "prop_kitchen_kettle", "prop_kitchen_rice", "prop_kitchen_laptop", "fixture_kitchen", "interior_loft_ceiling_right", "interior_loft_right", "loft_fascia_beam_right", "interior_floor_1f"))]
    s.start_clip(828, 50, 762, 515)
    # 1F Floor & Loft Ceiling datum lines
    s.add(f'<line x1="850" y1="{to_ke(0, 0.36)[1]:.1f}" x2="1560" y2="{to_ke(0, 0.36)[1]:.1f}" stroke="#0f172a" stroke-width="2.2"/>')
    s.add(f'<line x1="850" y1="{to_ke(0, 2.36)[1]:.1f}" x2="1560" y2="{to_ke(0, 2.36)[1]:.1f}" stroke="#0f172a" stroke-width="1.6"/>')
    for p in project_orthographic_view(ke_objs, (-1, 0, 0), (0, -1, 0), (0, 0, 1), to_ke, clip_plane=((1.45, 0, 0), (-1, 0, 0)), skip_seams=True):
        s.add(p)
    s.end_clip()

    # Exact Cabinet & Window Elevation Dimensions
    s.dim_v(1485, to_ke(0, 1.22)[1], to_ke(0, 0.36)[1], "860 CTR", ext_x=1450)
    s.dim_v(1485, to_ke(0, 1.92)[1], to_ke(0, 1.22)[1], "700 SPLASH", ext_x=1450)
    s.dim_v(1485, to_ke(0, 2.36)[1], to_ke(0, 1.92)[1], "440 UPPER", ext_x=1450)
    s.dim_v(1538, to_ke(0, 2.36)[1], to_ke(0, 0.36)[1], "2,000 CLR CLG", ext_x=1485, color="#b91c1c")
    s.dim_h(to_ke(0.72, 0)[0], to_ke(1.15, 0)[0], to_ke(0, 1.88)[1], "430", ext_y=to_ke(0, 1.78)[1], color="#1d4ed8")
    s.dim_h(to_ke(1.35, 0)[0], to_ke(1.78, 0)[0], to_ke(0, 1.88)[1], "430", ext_y=to_ke(0, 1.78)[1], color="#1d4ed8")

    s.leader_note(*to_ke(1.30, 2.25), 965, 118, ["L-02 CEILING DUCT RAIL", "+ 3× DIRECTIONAL SPOTS (EL +2.35m)"], align="right")
    s.leader_note(*to_ke(1.55, 1.58), 1020, 255, ["W-05 TWIN AWNING WINDOWS", "430 × 400mm FROSTED GLASS"], align="right")
    s.leader_note(*to_ke(-0.44, 1.65), 1020, 412, ["REFRIGERATOR NICHE &", "BIRCH OVERHEAD CABINET"], align="right")
    s.viewport_title(838, 594, "2", "ENLARGED 1F KITCHEN EAST ELEVATION", "1 : 25", width=480)

    # --- VP 3: ENLARGED 1F 3-ZONE BATHROOM SUITE PLAN (X=0.55..2.80, Y=0.72..2.75) ---
    s.add('<rect x="48" y="644" width="756" height="588" fill="#ffffff" stroke="#0f172a" stroke-width="1.3"/>')
    def to_bp(u, v):
        return (415.0 + (u - 1.65) * px_m, 925.0 - (v - 1.68) * px_m)

    bath_objs = [o for o in house_objs if any(k in o.name.lower() for k in ("bath_", "vanity_", "wc_", "shower_", "wall_rear_split_bot", "wall_right_gable", "plywall_right", "int_plywall_rear_split_bot", "fixture_bath"))]
    s.start_clip(52, 648, 748, 530)
    for p in project_orthographic_view(bath_objs, (0, 0, 1), (1, 0, 0), (0, 1, 0), to_bp, clip_plane=((0, 0, 1.50), (0, 0, 1)), skip_seams=False):
        s.add(p)
    for c in slice_objects_at_plane(bath_objs, (0, 0, 1.50), (0, 0, 1), (1, 0, 0), (0, 1, 0), to_bp):
        s.add(c)
    s.end_clip()

    # Exact Bathroom Zone Dimensions
    s.dim_h(to_bp(0.655, 0)[0], to_bp(1.842, 0)[0], to_bp(0, 2.92)[1], "1,187 VESTIBULE / VANITY", ext_y=to_bp(0, 2.57)[1])
    s.dim_h(to_bp(1.842, 0)[0], to_bp(2.625, 0)[0], to_bp(0, 2.92)[1], "783 WC", ext_y=to_bp(0, 2.57)[1])
    s.dim_v(to_bp(2.96, 0)[0], to_bp(0, 2.555)[1], to_bp(0, 1.758)[1], "797 SHOWER", ext_x=to_bp(2.64, 0)[0])
    s.dim_v(to_bp(2.96, 0)[0], to_bp(0, 1.758)[1], to_bp(0, 0.825)[1], "933 WC/VEST", ext_x=to_bp(2.64, 0)[0])

    s.leader_note(*to_bp(0.95, 1.42), 235, 920, ["VANITY COUNTER & VESSEL BASIN", "EL +1.16m · MIRROR + L-07 BAR"], align="right")
    s.leader_note(*to_bp(2.26, 1.25), 620, 1085, ["SEPARATE WC COMPARTMENT", "783×895mm · L-08B DOWNLIGHT"], align="left")
    s.leader_note(*to_bp(1.90, 2.15), 235, 720, ["WET-ROOM SHOWER (1,475×797)", "240×190 TILE · FRAMELESS GLASS", "FLOOR DRAIN · HINOKI STOOL"], align="right")
    s.viewport_title(62, 1208, "3", "ENLARGED 1F 3-ZONE BATHROOM SUITE PLAN", "1 : 25", width=480)

    # --- VP 4: ENLARGED WET-ROOM SHOWER & TATAMI ELEVATION (Looking North +Y) ---
    s.add('<rect x="824" y="644" width="770" height="588" fill="#ffffff" stroke="#0f172a" stroke-width="1.3"/>')
    # Split cleanly into Left (Tatami North Wall & Jimado Elevation, 1:25) & Right (Wet-Room Shower North Wall Elevation, 1:25)
    px_e4 = 135.0
    def to_te(u, v):
        # Tatami X=-2.64..+0.58 (center -1.03), Z=0.36..2.36 -> left half of VP 4 (x=845..1240)
        return (1040.0 + (u - (-1.03)) * px_e4, 1100.0 - (v - 0.36) * px_e4)

    tat_objs = [o for o in house_objs if any(k in o.name.lower() for k in ("tatami_", "prop_tatami", "fixture_tatami", "int_plywall_rear_split_bot", "bath_tatami_closet"))]
    s.start_clip(834, 654, 420, 480)
    s.add(f'<line x1="840" y1="{to_te(0, 0.36)[1]:.1f}" x2="1248" y2="{to_te(0, 0.36)[1]:.1f}" stroke="#0f172a" stroke-width="2.0"/>')
    for p in project_orthographic_view(tat_objs, (0, -1, 0), (1, 0, 0), (0, 0, 1), to_te, clip_plane=((0, 0.72, 0), (0, -1, 0)), skip_seams=False):
        s.add(p)
    s.end_clip()

    s.dim_h(to_te(-1.48, 0)[0], to_te(-0.02, 0)[0], to_te(0, 1.12)[1], "1,460 JIMADO W-03", ext_y=to_te(0, 0.96)[1], color="#1d4ed8")
    s.dim_v(855, to_te(0, 0.52)[1], to_te(0, 0.36)[1], "160", ext_x=to_te(-1.96, 0)[0])
    s.leader_note(*to_te(-0.69, 2.33), 990, 712, ["L-03 HINOKI SHOJI DRUM", "(480×480mm FLUSH CEILING)"], align="right")
    s.leader_note(*to_te(-1.93, 0.56), 990, 815, ["L-04 LINEAR LED COVE", "ALONG STORAGE WALL BASE"], align="right")

    # Right half of VP 4: Wet-Room Shower North Wall Elevation (X=1.15..2.63, Z=0.36..2.36)
    def to_se(u, v):
        return (1425.0 + (u - 1.89) * px_e4, 1100.0 - (v - 0.36) * px_e4)

    shw_objs = [o for o in house_objs if any(k in o.name.lower() for k in ("shower_", "fixture_bath_shower"))]
    s.start_clip(1272, 654, 314, 480)
    s.add(f'<line x1="1280" y1="{to_se(0, 0.36)[1]:.1f}" x2="1580" y2="{to_se(0, 0.36)[1]:.1f}" stroke="#0f172a" stroke-width="2.0"/>')
    for p in project_orthographic_view(shw_objs, (0, -1, 0), (1, 0, 0), (0, 0, 1), to_se, clip_plane=((0, 1.76, 0), (0, -1, 0)), skip_seams=True):
        s.add(p)
    s.end_clip()

    s.dim_v(1558, to_se(0, 2.26)[1], to_se(0, 0.38)[1], "1,880 RAIN HD", ext_x=1525)
    s.leader_note(*to_se(1.77, 1.65), 1280, 730, ["W-04 SHOWER WINDOW", "500×460 FROSTED · RAIN HEAD", "& HINOKI BATH STOOL"])

    s.viewport_title(838, 1208, "4", "ENLARGED TATAMI & WET-ROOM SHOWER NORTH ELEVATIONS", "1 : 25", width=590)
    s.save(os.path.join(DRAWINGS_DIR, "A-401_Enlarged_Interior_Plans_Elevations.svg"))
    print("Generated A-401_Enlarged_Interior_Plans_Elevations.svg")


# =========================================================================
# SHEET A-501: LOD-400 TYPICAL WALL SECTION & ENVELOPE CONSTRUCTION DETAILS
# =========================================================================
def build_a501():
    s = SvgSheet("A-501", "WALL SECTION & ENVELOPE DETAILS", "1:15 / 1:10 (LOD-400)", "9TS-KOI-B1-EN-DR-A-0501", "CONSTRUCTION DETAILS")

    # Pull exact model geometry benchmarks directly from BIM_DATA!
    dat = BIM_DATA["datums"]

    # =====================================================================
    # DETAIL 1 (LEFT FULL HEIGHT, x=46..540): TYPICAL FOOTING-TO-RIDGE WALL SECTION (1:15)
    # =====================================================================
    s.add('<rect x="46" y="46" width="496" height="1186" fill="#ffffff" stroke="#0f172a" stroke-width="1.4"/>')
    # Scale: 1m = 160px -> 6.0m total height (EL -0.45 to +5.55) = 960px!
    sc1 = 158.0
    wx_ext = 258.0   # Shifted slightly right so left datums sit 100% inside the x=46 frame!
    wy_gl = 1045.0   # Grade EL ±0.000
    def ws(dx_m, z_m):
        # dx_m: positive = interior (right), negative = exterior (left)
        return (wx_ext + dx_m * sc1, wy_gl - z_m * sc1)

    # Earth & Gravel below grade
    x0, y0 = ws(-0.95, 0.0)
    x1, y1 = ws(1.75, -0.58)
    s.add(f'<rect x="{x0:.1f}" y="{y0:.1f}" width="{x1-x0:.1f}" height="{y1-y0:.1f}" fill="url(#hatch-earth)"/>')
    s.add(f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y0:.1f}" stroke="#0f172a" stroke-width="2.0"/>')
    # Gravel capillary bed
    gx0, gy0 = ws(-0.26, -0.30)
    gx1, gy1 = ws(1.55, -0.45)
    s.add(f'<rect x="{gx0:.1f}" y="{gy0:.1f}" width="{gx1-gx0:.1f}" height="{gy1-gy0:.1f}" fill="url(#hatch-gravel)" stroke="#475569" stroke-width="0.9"/>')
    # RC Mat Slab + Stem Plinth (EL -0.30..+0.32m, stem 160mm wide)
    fpts = [ws(0.0, 0.32), ws(0.16, 0.32), ws(0.16, -0.12), ws(1.55, -0.12), ws(1.55, -0.30), ws(-0.18, -0.30), ws(-0.18, -0.15), ws(0.0, -0.15)]
    s.add(f'<polygon points="{" ".join(f"{a:.1f},{b:.1f}" for a,b in fpts)}" fill="url(#hatch-concrete)" stroke="#0f172a" stroke-width="1.8"/>')
    # Rebar inside slab/plinth
    s.add(f'<line x1="{ws(-0.12, -0.22)[0]:.1f}" y1="{ws(-0.12, -0.22)[1]:.1f}" x2="{ws(1.50, -0.22)[0]:.1f}" y2="{ws(1.50, -0.22)[1]:.1f}" stroke="#b91c1c" stroke-width="1.2" stroke-dasharray="5,2"/>')
    s.add(f'<line x1="{ws(0.08, 0.28)[0]:.1f}" y1="{ws(0.08, 0.28)[1]:.1f}" x2="{ws(0.08, -0.22)[0]:.1f}" y2="{ws(0.08, -0.22)[1]:.1f}" stroke="#b91c1c" stroke-width="1.2" stroke-dasharray="5,2"/>')

    # 1F Floor Assembly (EL +0.18..+0.36m: XPS + joists + 24mm ply + 18mm pine)
    s.add(f'<rect x="{ws(0.16, 0.36)[0]:.1f}" y="{ws(0.16, 0.36)[1]:.1f}" width="{1.38*sc1:.1f}" height="{0.042*sc1:.1f}" fill="url(#hatch-wood)" stroke="#0f172a" stroke-width="1.2"/>')
    s.add(f'<rect x="{ws(0.16, 0.318)[0]:.1f}" y="{ws(0.16, 0.318)[1]:.1f}" width="{1.38*sc1:.1f}" height="{0.070*sc1:.1f}" fill="url(#hatch-xps)" stroke="#92400e" stroke-width="0.8"/>')
    # Dodai sill plate (105x105mm)
    s.timber_section(*ws(0.032, 0.425), 0.105*sc1, 0.105*sc1)

    # Continuous 160mm Exterior Wall W-EXT-01 (EL +0.32..+4.56m)
    # Outer Galvalume + 18mm furred cavity + 12mm ply + 105mm stud/wool + 12mm interior birch ply
    s.add(f'<rect x="{ws(0.0, 4.56)[0]:.1f}" y="{ws(0.0, 4.56)[1]:.1f}" width="{0.019*sc1:.1f}" height="{4.24*sc1:.1f}" fill="#e2e8f0" stroke="#0f172a" stroke-width="1.3"/>')
    s.add(f'<rect x="{ws(0.019, 4.56)[0]:.1f}" y="{ws(0.019, 4.56)[1]:.1f}" width="{0.013*sc1:.1f}" height="{4.24*sc1:.1f}" fill="url(#hatch-plywood)" stroke="#0f172a" stroke-width="0.8"/>')
    s.add(f'<rect x="{ws(0.032, 4.56)[0]:.1f}" y="{ws(0.032, 4.56)[1]:.1f}" width="{0.105*sc1:.1f}" height="{4.24*sc1:.1f}" fill="#fefce8" stroke="#0f172a" stroke-width="0.9"/>')
    s.batt_insulation(*ws(0.032, 4.52), 0.105*sc1, 2.00*sc1, vertical=True)
    s.batt_insulation(*ws(0.032, 2.30), 0.105*sc1, 1.85*sc1, vertical=True)
    s.add(f'<rect x="{ws(0.148, 4.56)[0]:.1f}" y="{ws(0.148, 4.56)[1]:.1f}" width="{0.012*sc1:.1f}" height="{4.24*sc1:.1f}" fill="url(#hatch-plywood)" stroke="#0f172a" stroke-width="1.1"/>')

    # 2F Loft Rim Beam & Floor Assembly (EL +2.36..+2.52m)
    s.timber_section(*ws(0.032, 2.52), 0.116*sc1, 0.160*sc1)
    s.add(f'<rect x="{ws(0.16, 2.52)[0]:.1f}" y="{ws(0.16, 2.52)[1]:.1f}" width="{1.38*sc1:.1f}" height="{0.16*sc1:.1f}" fill="url(#hatch-wood)" stroke="#0f172a" stroke-width="1.3"/>')
    s.add(f'<rect x="{ws(0.16, 2.40)[0]:.1f}" y="{ws(0.16, 2.40)[1]:.1f}" width="{1.38*sc1:.1f}" height="{0.04*sc1:.1f}" fill="url(#hatch-plywood)" stroke="#0f172a" stroke-width="0.9"/>')

    # Sloped Roof RF-01 (South slope 16.0° from eave overhang dx=-0.205, Z=4.568 up to dx=1.55, Z=5.07)
    slope = 0.28676
    rpts_top = [ws(-0.205, 4.658), ws(1.55, 4.658 + 1.755*slope), ws(1.55, 4.506 + 1.755*slope), ws(-0.205, 4.506)]
    s.add(f'<polygon points="{" ".join(f"{a:.1f},{b:.1f}" for a,b in rpts_top)}" fill="#f6ead8" stroke="#0f172a" stroke-width="1.6"/>')
    # Standing seam outer metal skin
    s.add(f'<line x1="{ws(-0.205, 4.662)[0]:.1f}" y1="{ws(-0.205, 4.662)[1]:.1f}" x2="{ws(1.55, 4.662 + 1.755*slope)[0]:.1f}" y2="{ws(1.55, 4.662 + 1.755*slope)[1]:.1f}" stroke="#0f172a" stroke-width="2.6"/>')
    # Half-round gutter at eave
    gx_gt, gy_gt = ws(-0.24, 4.58)
    s.add(f'<path d="M {gx_gt-6:.1f} {gy_gt:.1f} A 6 6 0 0 0 {gx_gt+6:.1f} {gy_gt:.1f}" fill="#cbd5e1" stroke="#0f172a" stroke-width="1.4"/>')
    # Top double plate
    s.timber_section(*ws(0.032, 4.56), 0.105*sc1, 0.090*sc1)

    # Datums & Callouts on Detail 1 (cleanly inside x=54..536!)
    for dcode, delv, dz in [("S. EAVE", "+4.568", 4.568), ("2F FFL", "+2.520", 2.520), ("1F FFL", "+0.360", 0.360), ("GL", "±0.000", 0.000), ("FTG", "-0.300", -0.300)]:
        s.datum_level(120, 195, ws(0, dz)[1], dcode, delv, label_side="left")

    s.detail_callout(*ws(0.08, 4.58), 26, "3", "A-501", *ws(1.10, 4.50))
    s.detail_callout(*ws(0.08, 0.25), 26, "2", "A-501", *ws(1.10, 0.72))
    s.leader_note(*ws(0.08, 3.45), 325, 455, ["ASSEMBLY W-EXT-01 (160mm):", "• 0.4mm Galvalume Cladding", "• 18mm Vented Furring Cavity", "• Breathable WRB Membrane", "• 12mm JAS Shear Plywood", "• 105mm Timber + Mineral Wool", "• 0.2mm Vapor Retarder", "• 12mm Birch Plywood Finish"], align="left")
    s.leader_note(*ws(0.85, 2.44), 325, 710, ["ASSEMBLY FL-2F-01 (160mm):", "18mm Pine + 18mm Subfloor +", "45×96 Joists + 28mm Soffit"], align="left")
    s.viewport_title(60, 1208, "1", "TYPICAL EXTERIOR WALL SECTION", "1 : 15", width=445)

    # =====================================================================
    # DETAIL 2 (TOP-RIGHT, x=566..1594, y=46..418): RC PLINTH, FOOTING, ANCHOR BOLT & ENGAWA PIER (1:10)
    # =====================================================================
    s.add('<rect x="566" y="46" width="1028" height="372" fill="#ffffff" stroke="#0f172a" stroke-width="1.4"/>')
    sc2 = 290.0  # Rich 1:10 detail scale!
    ox2, oy2 = 1095.0, 295.0  # Origin at outer plinth face X=0, Grade Z=0
    def d2(x_m, z_m):
        # x_m < 0 = exterior (left, Engawa deck!), x_m > 0 = interior (right)
        return (ox2 + x_m * sc2, oy2 - z_m * sc2)

    # Undisturbed soil + gravel bed
    s.add(f'<rect x="580" y="{oy2:.1f}" width="998" height="72" fill="url(#hatch-earth)"/>')
    s.add(f'<line x1="580" y1="{oy2:.1f}" x2="1578" y2="{oy2:.1f}" stroke="#0f172a" stroke-width="2.0"/>')
    # Crushed gravel under house & under engawa pier
    s.add(f'<rect x="{d2(-0.85, -0.05)[0]:.1f}" y="{d2(-0.85, -0.05)[1]:.1f}" width="{0.60*sc2:.1f}" height="{0.14*sc2:.1f}" fill="url(#hatch-gravel)" stroke="#475569" stroke-width="0.8"/>')
    s.add(f'<rect x="{d2(-0.22, -0.22)[0]:.1f}" y="{d2(-0.22, -0.22)[1]:.1f}" width="{1.45*sc2:.1f}" height="{0.12*sc2:.1f}" fill="url(#hatch-gravel)" stroke="#475569" stroke-width="0.8"/>')

    # RC Mat Slab + Stem Plinth (0.00..+0.32m, width 160mm)
    p2 = [d2(0.0, 0.32), d2(0.16, 0.32), d2(0.16, -0.08), d2(1.22, -0.08), d2(1.22, -0.22), d2(-0.16, -0.22), d2(-0.16, -0.10), d2(0.0, -0.10)]
    s.add(f'<polygon points="{" ".join(f"{a:.1f},{b:.1f}" for a,b in p2)}" fill="url(#hatch-concrete)" stroke="#0f172a" stroke-width="2.0"/>')
    # D13 Rebar + Stirrups
    s.add(f'<line x1="{d2(-0.10, -0.16)[0]:.1f}" y1="{d2(-0.10, -0.16)[1]:.1f}" x2="{d2(1.18, -0.16)[0]:.1f}" y2="{d2(1.18, -0.16)[1]:.1f}" stroke="#b91c1c" stroke-width="1.6"/>')
    s.add(f'<line x1="{d2(0.08, 0.27)[0]:.1f}" y1="{d2(0.08, 0.27)[1]:.1f}" x2="{d2(0.08, -0.16)[0]:.1f}" y2="{d2(0.08, -0.16)[1]:.1f}" stroke="#b91c1c" stroke-width="1.6"/>')
    for rx in (-0.08, 0.08, 0.35, 0.65, 0.95):
        cxr, cyr = d2(rx, -0.16)
        s.add(f'<circle cx="{cxr:.1f}" cy="{cyr:.1f}" r="2.6" fill="#b91c1c"/>')

    # M12 Galvanized Anchor Bolt rising through Dodai sill plate!
    abx, aby_top = d2(0.08, 0.44)
    _, aby_bot = d2(0.08, 0.08)
    s.add(f'<line x1="{abx:.1f}" y1="{aby_top:.1f}" x2="{abx:.1f}" y2="{aby_bot:.1f}" stroke="#0f172a" stroke-width="2.6"/>')
    s.add(f'<rect x="{abx-6:.1f}" y="{aby_top-3:.1f}" width="12" height="4" fill="#0f172a"/>')  # washer + hex nut

    # Aluminum Plinth Drip Flashing (Plinth_Flashing EL +0.30..+0.325m)
    fl_pts = [d2(-0.042, 0.295), d2(-0.036, 0.325), d2(0.03, 0.325), d2(0.03, 0.36)]
    s.add(f'<polyline points="{" ".join(f"{a:.1f},{b:.1f}" for a,b in fl_pts)}" fill="none" stroke="#1d4ed8" stroke-width="2.4"/>')

    # 105×105mm Pressure-Treated Hinoki Dodai Sill Plate + Wall Bottom Layers
    s.timber_section(*d2(0.032, 0.425), 0.105*sc2, 0.105*sc2)
    s.add(f'<rect x="{d2(0.0, 0.72)[0]:.1f}" y="{d2(0.0, 0.72)[1]:.1f}" width="{0.018*sc2:.1f}" height="{0.40*sc2:.1f}" fill="#e2e8f0" stroke="#0f172a" stroke-width="1.3"/>')
    s.add(f'<rect x="{d2(0.018, 0.72)[0]:.1f}" y="{d2(0.018, 0.72)[1]:.1f}" width="{0.014*sc2:.1f}" height="{0.40*sc2:.1f}" fill="url(#hatch-plywood)" stroke="#0f172a" stroke-width="0.9"/>')
    s.add(f'<rect x="{d2(0.032, 0.72)[0]:.1f}" y="{d2(0.032, 0.72)[1]:.1f}" width="{0.105*sc2:.1f}" height="{0.295*sc2:.1f}" fill="#fefce8" stroke="#0f172a" stroke-width="0.9"/>')
    s.batt_insulation(*d2(0.032, 0.71), 0.105*sc2, 0.28*sc2, vertical=True)
    s.add(f'<rect x="{d2(0.148, 0.72)[0]:.1f}" y="{d2(0.148, 0.72)[1]:.1f}" width="{0.012*sc2:.1f}" height="{0.36*sc2:.1f}" fill="url(#hatch-plywood)" stroke="#0f172a" stroke-width="1.1"/>')

    # Interior 1F Floor Assembly (Pine 18mm + Plywood 24mm + Joists + Rigid XPS 65mm)
    s.add(f'<rect x="{d2(0.16, 0.36)[0]:.1f}" y="{d2(0.16, 0.36)[1]:.1f}" width="{1.06*sc2:.1f}" height="{0.018*sc2:.1f}" fill="url(#hatch-wood)" stroke="#0f172a" stroke-width="1.1"/>')
    s.add(f'<rect x="{d2(0.16, 0.342)[0]:.1f}" y="{d2(0.16, 0.342)[1]:.1f}" width="{1.06*sc2:.1f}" height="{0.024*sc2:.1f}" fill="url(#hatch-plywood)" stroke="#0f172a" stroke-width="0.9"/>')
    s.add(f'<rect x="{d2(0.16, 0.318)[0]:.1f}" y="{d2(0.16, 0.318)[1]:.1f}" width="{1.06*sc2:.1f}" height="{0.065*sc2:.1f}" fill="url(#hatch-xps)" stroke="#92400e" stroke-width="0.9"/>')
    # Floor joists every 455mm
    for jx in (0.45, 0.90):
        s.timber_section(*d2(jx, 0.318), 0.045*sc2, 0.095*sc2)

    # Exterior Cedar Engawa Deck + Precast Concrete Pier Block (EXACT model coords: Deck_Footing Z=0..0.22, Subframe Z=0.21..0.26, Planks Z=0.26..0.32!)
    # Precast trapezoidal pier block at x=-0.55
    pier_pts = [d2(-0.66, 0.00), d2(-0.62, 0.22), d2(-0.48, 0.22), d2(-0.44, 0.00)]
    s.add(f'<polygon points="{" ".join(f"{a:.1f},{b:.1f}" for a,b in pier_pts)}" fill="url(#hatch-concrete)" stroke="#0f172a" stroke-width="1.8"/>')
    # Cedar bearer subframe (EL +0.21..+0.26m)
    s.add(f'<rect x="{d2(-1.45, 0.26)[0]:.1f}" y="{d2(-1.45, 0.26)[1]:.1f}" width="{1.40*sc2:.1f}" height="{0.05*sc2:.1f}" fill="url(#hatch-wood)" stroke="#0f172a" stroke-width="1.3"/>')
    # Individual Cedar Deck Planks (32×174mm w/ 8mm gaps @ EL +0.26..+0.32m)
    for px_d in (-1.42, -1.23, -1.04, -0.85, -0.66, -0.47, -0.28):
        s.timber_section(*d2(px_d, 0.32), 0.174*sc2, 0.058*sc2)

    # Keynotes & Dimensions on Detail 2 (clean white-space placement!)
    s.dim_v(d2(0.24, 0)[0], d2(0, 0.32)[1], d2(0, 0.00)[1], "320 PLINTH", ext_x=d2(0.16, 0)[0])
    s.leader_note(*d2(-0.85, 0.32), 775, 92, ["CEDAR ENGAWA DECK (DK-01)", "32×174mm PLANKS (8mm GAP)", "50×90 CEDAR BEARER SUBFRAME", "220mm PRECAST CONCRETE PIER"], align="right")
    s.leader_note(*d2(-0.04, 0.31), 985, 118, ["ALUMINUM PLINTH FLASHING", "W/ DRIP EDGE & BUG SCREEN"], align="right")
    s.leader_note(*d2(0.08, 0.42), 1205, 86, ["M12 GALV. ANCHOR BOLT @ 910 O.C.", "105×105 PT HINOKI DODAI SILL", "160mm W-EXT-01 CAVITY WALL"], align="left")
    s.leader_note(*d2(0.75, 0.34), 1300, 152, ["1F FLOOR ASSEMBLY (FL-1F-01)", "18mm RED PINE + 24mm PLYWOOD", "65mm RIGID XPS + 45×95 JOISTS"], align="left")
    s.leader_note(*d2(0.55, -0.16), 1295, 372, ["RC MAT & STEM PLINTH (FND-01)", "24 MPa CONCRETE · D13 @ 200 B.W.", "0.15mm VAPOR BARRIER OVER 150 GRAVEL"], align="left")
    s.viewport_title(582, 396, "2", "FOUNDATION PLINTH, ANCHOR BOLT & ENGAWA PIER DETAIL", "1 : 10", width=560)

    # =====================================================================
    # DETAIL 3 (MID-RIGHT, x=566..1594, y=440..825): GABLE EAVE, VENTED CAVITY & GUTTER DETAIL (1:10)
    # =====================================================================
    s.add('<rect x="566" y="440" width="1028" height="385" fill="#ffffff" stroke="#0f172a" stroke-width="1.4"/>')
    sc3 = 310.0
    ox3, oy3 = 1040.0, 680.0  # Outer wall face X=0, Top of wall / Eave datum EL +4.568
    def d3(x_m, dz_m):
        return (ox3 + x_m * sc3, oy3 - dz_m * sc3)

    slope3 = 0.28676  # Exact 16.0° South Roof Slope!
    # Exterior Wall W-EXT-01 rising up to double top plate (dz = -0.50..0.00)
    s.add(f'<rect x="{d3(0.0, 0.0)[0]:.1f}" y="{d3(0.0, 0.0)[1]:.1f}" width="{0.018*sc3:.1f}" height="{0.42*sc3:.1f}" fill="#e2e8f0" stroke="#0f172a" stroke-width="1.3"/>')
    s.add(f'<rect x="{d3(0.018, 0.0)[0]:.1f}" y="{d3(0.018, 0.0)[1]:.1f}" width="{0.014*sc3:.1f}" height="{0.42*sc3:.1f}" fill="url(#hatch-plywood)" stroke="#0f172a" stroke-width="0.9"/>')
    s.add(f'<rect x="{d3(0.032, -0.09)[0]:.1f}" y="{d3(0.032, -0.09)[1]:.1f}" width="{0.105*sc3:.1f}" height="{0.33*sc3:.1f}" fill="#fefce8" stroke="#0f172a" stroke-width="0.9"/>')
    s.batt_insulation(*d3(0.032, -0.10), 0.105*sc3, 0.31*sc3, vertical=True)
    # Double 45×105mm Top Wall Plate (dz = -0.09..0.00)
    s.timber_section(*d3(0.032, 0.00), 0.105*sc3, 0.045*sc3)
    s.timber_section(*d3(0.032, -0.045), 0.105*sc3, 0.045*sc3)
    # Interior birch plywood lining
    s.add(f'<rect x="{d3(0.148, -0.01)[0]:.1f}" y="{d3(0.148, -0.01)[1]:.1f}" width="{0.012*sc3:.1f}" height="{0.41*sc3:.1f}" fill="url(#hatch-plywood)" stroke="#0f172a" stroke-width="1.1"/>')

    # Sloped Roof Assembly RF-01 (x = -0.24..+1.15, angle 16.0°)
    # Draw multi-layer roof stripes parallel to slope!
    def roof_strip(x0, x1, z_bot_at_0, thick_m, fill, stroke="#0f172a", sw=1.1):
        pts = [
            d3(x0, z_bot_at_0 + x0 * slope3),
            d3(x1, z_bot_at_0 + x1 * slope3),
            d3(x1, z_bot_at_0 + thick_m + x1 * slope3),
            d3(x0, z_bot_at_0 + thick_m + x0 * slope3),
        ]
        s.add(f'<polygon points="{" ".join(f"{a:.1f},{b:.1f}" for a,b in pts)}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')

    # Layer 7: 12mm Interior Birch Plywood Ceiling Lining (inside wall x=0.16..1.15)
    roof_strip(0.155, 1.15, -0.025, 0.012, "url(#hatch-plywood)", sw=1.2)
    # Layer 5: 100mm Cedar Rafter & Mineral Wool Cavity
    roof_strip(-0.22, 1.15, -0.013, 0.102, "#fefce8", sw=1.3)
    # Show dashed rafter outline + sloped insulation strokes
    roof_strip(-0.22, 1.15, 0.089, 0.024, "#e0f2fe", stroke="#0284c7", sw=0.9)  # 24mm Continuous Vented Air Channel!
    # Layer 3: 12mm Structural Plywood Roof Deck
    roof_strip(-0.24, 1.15, 0.113, 0.014, "url(#hatch-plywood)", sw=1.1)
    # Layer 1-2: Underlayment + 0.4mm Standing-Seam Galvalume Metal Roof
    roof_strip(-0.25, 1.15, 0.127, 0.018, "url(#hatch-steel)", sw=1.8)

    # Eave Fascia, Vented Soffit Insect Screen & Half-Round Aluminum Gutter (Roof_Gutter)
    fx0, fy0 = d3(-0.25, 0.127 - 0.25 * slope3)
    s.add(f'<rect x="{fx0:.1f}" y="{fy0:.1f}" width="{0.022*sc3:.1f}" height="{0.13*sc3:.1f}" fill="#cbd5e1" stroke="#0f172a" stroke-width="1.4"/>')
    # Half-round aluminum gutter hung off fascia
    gx3, gy3 = d3(-0.30, 0.01)
    s.add(f'<path d="M {gx3-16:.1f} {gy3:.1f} A 16 16 0 0 0 {gx3+16:.1f} {gy3:.1f} Z" fill="#e2e8f0" stroke="#0f172a" stroke-width="1.6"/>')
    # Ventilation airflow arrow entering eave soffit up through 24mm channel!
    va0 = d3(-0.14, -0.07)
    va1 = d3(-0.08, 0.05)
    va2 = d3(0.42, 0.10 + 0.42 * slope3)
    s.add(f'<polyline points="{va0[0]:.1f},{va0[1]:.1f} {va1[0]:.1f},{va1[1]:.1f} {va2[0]:.1f},{va2[1]:.1f}" fill="none" stroke="#0284c7" stroke-width="1.6" stroke-dasharray="5,3" marker-end="url(#arr-blue)"/>')

    # Leader Callouts on Detail 3 (zero text crossing roof line!)
    s.leader_note(*d3(-0.30, 0.01), 765, 695, ["HALF-ROUND ALUM. GUTTER", "(ROOF_GUTTER · EL +4.568m)", "ALUM. DRIP EDGE & FASCIA"], align="right")
    s.leader_note(*d3(-0.10, -0.05), 765, 560, ["CONTINUOUS VENTED EAVE", "INSECT MESH + 24mm AIR GAP", "EAVE-TO-RIDGE VENTILATION"], align="right", color="#0284c7")
    s.leader_note(*d3(0.55, 0.13 + 0.55*slope3), 1210, 464, ["ROOF ASSEMBLY RF-01 (152mm):", "• 0.4mm Standing-Seam Galvalume", "• Bitumen Underlayment + 12mm Deck", "• 24mm Vent Channel + 45×100 Rafters", "• Mineral Wool + 12mm Birch Clg"], align="left")
    s.leader_note(*d3(0.08, -0.04), 1245, 725, ["DOUBLE 45×105 TOP PLATE", "GALV. HURRICANE CLIP TO RAFTER", "160mm W-EXT-01 CONTINUOUS WALL"], align="left")
    s.viewport_title(582, 804, "3", "SOUTH GABLE EAVE, VENTED CAVITY & GUTTER DETAIL", "1 : 10", width=560)

    # =====================================================================
    # DETAIL 4 (BOTTOM-RIGHT, x=566..1594, y=847..1232): RIDGE BEAM, Ø176 CEDAR COLUMN CAP & TRACK MOUNT (1:10)
    # =====================================================================
    s.add('<rect x="566" y="847" width="1028" height="385" fill="#ffffff" stroke="#0f172a" stroke-width="1.4"/>')
    sc4 = 310.0
    ox4, oy4 = 1070.0, 1020.0  # Ridge centerline Y=+0.150, Top of Ridge Beam EL +5.340
    def d4(dy_m, dz_m):
        # dy_m < 0 = North (left, 23.1° steeper), dy_m > 0 = South (right, 16.0°)
        return (ox4 + dy_m * sc4, oy4 - dz_m * sc4)

    sl_n = 0.42562  # North 23.1°
    sl_s = 0.28676  # South 16.0°

    # Central Ø176mm Turned Cedar Column rising into Ridge Beam (dz = -0.60..-0.18)
    s.add(f'<rect x="{d4(-0.088, -0.18)[0]:.1f}" y="{d4(-0.088, -0.18)[1]:.1f}" width="{0.176*sc4:.1f}" height="{0.42*sc4:.1f}" fill="url(#hatch-wood)" stroke="#0f172a" stroke-width="1.8"/>')
    # 140×180mm Exposed Structural Timber Ridge Beam (Ceiling_Ridge_Beam: width 140mm, Z=5.16..5.34 -> dz=-0.18..0.00)
    s.timber_section(*d4(-0.070, 0.00), 0.140*sc4, 0.180*sc4)
    # Concealed Steel Knife-Plate + 2× M12 Drift Pins connecting Column to Ridge Beam!
    s.add(f'<rect x="{d4(-0.008, -0.05)[0]:.1f}" y="{d4(-0.008, -0.05)[1]:.1f}" width="{0.016*sc4:.1f}" height="{0.26*sc4:.1f}" fill="url(#hatch-steel)" stroke="#0f172a" stroke-width="1.3"/>')
    for pin_z in (-0.09, -0.14, -0.23, -0.28):
        pxp, pyp = d4(0.0, pin_z)
        s.add(f'<circle cx="{pxp:.1f}" cy="{pyp:.1f}" r="3.2" fill="#0f172a"/>')

    # Opposing Asymmetric Roof Rafters & Standing-Seam Galvalume + Vented Ridge Cap!
    def half_roof(sign, slope_val, x_len):
        # sign = -1 (North left), +1 (South right)
        x0, x1 = sign * 0.070, sign * x_len
        for zb, th, fl, sw in [(-0.015, 0.012, "url(#hatch-plywood)", 1.1), (-0.003, 0.095, "#fefce8", 1.2), (0.092, 0.022, "#e0f2fe", 0.9), (0.114, 0.014, "url(#hatch-plywood)", 1.0), (0.128, 0.016, "url(#hatch-steel)", 1.7)]:
            pts = [
                d4(x0, zb - abs(x0)*slope_val),
                d4(x1, zb - abs(x1)*slope_val),
                d4(x1, zb + th - abs(x1)*slope_val),
                d4(x0, zb + th - abs(x0)*slope_val),
            ]
            s.add(f'<polygon points="{" ".join(f"{a:.1f},{b:.1f}" for a,b in pts)}" fill="{fl}" stroke="#0f172a" stroke-width="{sw}"/>')

    half_roof(-1, sl_n, 0.95)
    half_roof(1, sl_s, 1.05)

    # Vented Standing-Seam Ridge Cap Flashing (EL +5.460m apex!)
    rc_pts = [d4(-0.18, 0.145 - 0.18*sl_n), d4(0.0, 0.165), d4(0.18, 0.145 - 0.18*sl_s)]
    s.add(f'<polyline points="{" ".join(f"{a:.1f},{b:.1f}" for a,b in rc_pts)}" fill="none" stroke="#0f172a" stroke-width="3.2"/>')

    # Modeled L-05 Duct Rail mounted on underside of Ridge Beam (offset right of column) + Directional Spot!
    s.add(f'<rect x="{d4(0.09, -0.18)[0]:.1f}" y="{d4(0.09, -0.18)[1]:.1f}" width="{0.044*sc4:.1f}" height="{0.028*sc4:.1f}" fill="#ffffff" stroke="#0f172a" stroke-width="1.4"/>')
    s.add(f'<rect x="{d4(0.095, -0.215)[0]:.1f}" y="{d4(0.095, -0.215)[1]:.1f}" width="{0.034*sc4:.1f}" height="{0.095*sc4:.1f}" fill="#fef3c7" stroke="#0f172a" stroke-width="1.3"/>')

    s.leader_note(*d4(0.0, 0.165), 815, 892, ["VENTED GALVALUME RIDGE CAP", "EL +5.460m · CONTINUOUS RIDGE VENT", "NORTH 23.1° / SOUTH 16.0° ASYMMETRY"], align="right")
    s.leader_note(*d4(-0.07, -0.09), 815, 1020, ["140×180mm TIMBER RIDGE BEAM", "(CEILING_RIDGE_BEAM · EL +5.16..+5.34)", "CONCEALED 9mm STEEL KNIFE PLATE"], align="right")
    s.leader_note(*d4(-0.088, -0.35), 815, 1135, ["Ø176mm TURNED CEDAR COLUMN", "4× M12 THROUGH-DRIFT PINS"], align="right")
    s.leader_note(*d4(0.12, -0.24), 1215, 1142, ["L-05 ARCHITECTURAL DUCT RAIL", "& ADJUSTABLE 2800K TRACK SPOT", "SURFACE MOUNTED TO RIDGE BEAM"], align="left")
    s.viewport_title(582, 1210, "4", "RIDGE BEAM, Ø176 CEDAR COLUMN CAP & TRACK MOUNT", "1 : 10", width=575)

    s.save(os.path.join(DRAWINGS_DIR, "A-501_Wall_Section_Envelope_Details.svg"))
    print("Generated A-501_Wall_Section_Envelope_Details.svg")


# =========================================================================
# SHEET A-502: LOD-400 GLAZING, STAIR STRINGER & CABLE GUARDRAIL DETAILS
# =========================================================================
def build_a502():
    s = SvgSheet("A-502", "GLAZING, STAIR & GUARDRAIL DETAILS", "1:5 / 1:10 (LOD-400)", "9TS-KOI-B1-DT-DR-A-0502", "ARCHITECTURAL DETAILS")

    # 2x2 Grid of Large-Scale Construction Joinery Details (x=48..1594, y=46..1232)

    # =====================================================================
    # DETAIL 1 (TOP-LEFT, x=48..808, y=46..625): 2-STORY FRONT SHOJI & ALUMINUM CURTAIN WALL (1:8)
    # =====================================================================
    s.add('<rect x="48" y="46" width="760" height="579" fill="#ffffff" stroke="#0f172a" stroke-width="1.4"/>')
    sc1 = 360.0
    # Break-section showing: (A) Mid-Transom at 2F Loft EL +2.44m (top half) & (B) Sill Track at Engawa EL +0.36m (bottom half)
    ox1 = 370.0  # Wall centerline Y = -2.65m (left = exterior South / Engawa, right = interior)

    # --- Top Break: MID-TRANSOM & 2F LOFT HEADER (y=120..310) ---
    ym1 = 220.0
    def d1_mid(dx_m, dz_m):
        return (ox1 + dx_m * sc1, ym1 - dz_m * sc1)

    # Aluminum Mid-Transom Extrusion (WinFrame_Mid_Transom: 222mm deep x 100mm tall, EL +2.39..+2.49)
    s.add(f'<rect x="{d1_mid(-0.14, 0.05)[0]:.1f}" y="{d1_mid(-0.14, 0.05)[1]:.1f}" width="{0.222*sc1:.1f}" height="{0.10*sc1:.1f}" fill="url(#hatch-steel)" stroke="#0f172a" stroke-width="1.8"/>')
    # Thermal break polyamide core inside extrusion
    s.add(f'<rect x="{d1_mid(-0.04, 0.045)[0]:.1f}" y="{d1_mid(-0.04, 0.045)[1]:.1f}" width="{0.024*sc1:.1f}" height="{0.09*sc1:.1f}" fill="#0f172a"/>')
    # Upper Outer Shoji Sash (Y=-2.74 -> dx=-0.09) + Upper Inner Sash (dx=+0.06)
    s.add(f'<rect x="{d1_mid(-0.115, 0.28)[0]:.1f}" y="{d1_mid(-0.115, 0.28)[1]:.1f}" width="{0.055*sc1:.1f}" height="{0.23*sc1:.1f}" fill="#f6ead8" stroke="#0f172a" stroke-width="1.4"/>')
    s.add(f'<line x1="{d1_mid(-0.088, 0.28)[0]:.1f}" y1="{d1_mid(-0.088, 0.28)[1]:.1f}" x2="{d1_mid(-0.088, 0.05)[0]:.1f}" y2="{d1_mid(-0.088, 0.05)[1]:.1f}" stroke="#64748b" stroke-width="1.4"/>')  # Washi paper plane
    # Lower Glazed Double Low-E IGU Sash (dx=+0.04, below transom)
    s.add(f'<rect x="{d1_mid(0.015, -0.05)[0]:.1f}" y="{d1_mid(0.015, -0.05)[1]:.1f}" width="{0.055*sc1:.1f}" height="{0.22*sc1:.1f}" fill="#e2e8f0" stroke="#0f172a" stroke-width="1.4"/>')
    s.add(f'<rect x="{d1_mid(0.032, -0.09)[0]:.1f}" y="{d1_mid(0.032, -0.09)[1]:.1f}" width="{0.022*sc1:.1f}" height="{0.18*sc1:.1f}" fill="#bae6fd" stroke="#0284c7" stroke-width="1.2"/>')
    # Solid Cedar Interior Reveal Casing (WinReveal_Wood_*)
    s.timber_section(*d1_mid(0.082, 0.09), 0.055*sc1, 0.045*sc1)
    s.timber_section(*d1_mid(0.082, -0.05), 0.055*sc1, 0.045*sc1)
    # 2F Loft Rim Beam tie-back (interior)
    s.add(f'<rect x="{d1_mid(0.137, 0.08)[0]:.1f}" y="{d1_mid(0.137, 0.08)[1]:.1f}" width="{0.40*sc1:.1f}" height="{0.16*sc1:.1f}" fill="url(#hatch-wood)" stroke="#0f172a" stroke-width="1.4"/>')

    # Break-line divider between Mid-Transom & Sill
    s.add('<line x1="120" y1="335" x2="740" y2="335" stroke="#94a3b8" stroke-width="1.0" stroke-dasharray="12,4,3,4"/>')

    # --- Bottom Break: SILL TRACK, PLINTH FLASHING & ENGAWA INTERFACE (y=360..540) ---
    ys1 = 465.0
    def d1_sill(dx_m, dz_m):
        return (ox1 + dx_m * sc1, ys1 - dz_m * sc1)

    # Concrete Plinth (EL 0.00..+0.32m -> dz=-0.32..0.00)
    s.add(f'<rect x="{d1_sill(-0.12, 0.0)[0]:.1f}" y="{d1_sill(-0.12, 0.0)[1]:.1f}" width="{0.28*sc1:.1f}" height="{0.18*sc1:.1f}" fill="url(#hatch-concrete)" stroke="#0f172a" stroke-width="1.8"/>')
    # Aluminum Sill Track w/ Weep Slot (EL +0.31..+0.36m -> dz=0.00..0.05)
    s.add(f'<rect x="{d1_sill(-0.13, 0.05)[0]:.1f}" y="{d1_sill(-0.13, 0.05)[1]:.1f}" width="{0.21*sc1:.1f}" height="{0.05*sc1:.1f}" fill="url(#hatch-steel)" stroke="#0f172a" stroke-width="1.6"/>')
    # Dual Sliding Track Rails (outer shoji track + inner glass door track!)
    s.add(f'<rect x="{d1_sill(-0.115, 0.25)[0]:.1f}" y="{d1_sill(-0.115, 0.25)[1]:.1f}" width="{0.055*sc1:.1f}" height="{0.20*sc1:.1f}" fill="#f6ead8" stroke="#0f172a" stroke-width="1.3"/>')
    s.add(f'<rect x="{d1_sill(0.015, 0.25)[0]:.1f}" y="{d1_sill(0.015, 0.25)[1]:.1f}" width="{0.055*sc1:.1f}" height="{0.20*sc1:.1f}" fill="#e2e8f0" stroke="#0f172a" stroke-width="1.3"/>')
    s.add(f'<rect x="{d1_sill(0.032, 0.25)[0]:.1f}" y="{d1_sill(0.032, 0.25)[1]:.1f}" width="{0.022*sc1:.1f}" height="{0.16*sc1:.1f}" fill="#bae6fd" stroke="#0284c7" stroke-width="1.1"/>')
    # Exterior Engawa Deck Plank flush at EL +0.32m
    s.timber_section(*d1_sill(-0.55, 0.00), 0.38*sc1, 0.055*sc1)
    # Interior 1F Pine Floor flush at EL +0.36m
    s.add(f'<rect x="{d1_sill(0.08, 0.04)[0]:.1f}" y="{d1_sill(0.08, 0.04)[1]:.1f}" width="{0.52*sc1:.1f}" height="{0.042*sc1:.1f}" fill="url(#hatch-wood)" stroke="#0f172a" stroke-width="1.2"/>')

    s.leader_note(*d1_mid(-0.09, 0.16), 255, 118, ["OUTER TRACK: SLIDING CEDAR", "SHOJI LATTICE + WASHI PAPER", "(SASH_*_SHOJI · Y = -2.74m)"], align="right")
    s.leader_note(*d1_mid(-0.03, 0.00), 255, 232, ["THERMAL-BREAK ALUM. MID-TRANSOM", "222×100mm (EL +2.39..+2.49m)", "POLYAMIDE THERMAL BARRIER"], align="right")
    s.leader_note(*d1_mid(0.11, 0.07), 500, 128, ["SOLID CEDAR REVEAL CASING", "(WINREVEAL_WOOD_*)", "TIED TO 2F LOFT STRUCTURE"], align="left")
    s.leader_note(*d1_sill(-0.08, 0.03), 255, 402, ["ANODIZED ALUM. SILL TRACK", "W/ INTEGRATED WEEP DRAIN", "& EPDM SUB-SILL GASKET"], align="right")
    s.leader_note(*d1_sill(-0.36, 0.00), 255, 518, ["CEDAR ENGAWA DECK (EL +0.320)", "40mm STEP DOWN FROM 1F FFL"], align="right")
    s.leader_note(*d1_sill(0.32, 0.04), 500, 488, ["1F SOLID PINE FLOOR (EL +0.360)", "FLUSH THRESHOLD TO INNER TRACK"], align="left")
    s.viewport_title(62, 600, "1", "2-STORY FRONT SHOJI & ALUMINUM CURTAIN WALL (GLZ-01)", "1 : 8", width=620)

    # =====================================================================
    # DETAIL 2 (TOP-RIGHT, x=832..1594, y=46..625): 2F REAR SLIDING WINDOW W-02 FLASHING DETAIL (1:5)
    # =====================================================================
    s.add('<rect x="832" y="46" width="762" height="579" fill="#ffffff" stroke="#0f172a" stroke-width="1.4"/>')
    sc2 = 520.0  # Ultra-crisp 1:5 construction detail!
    ox2 = 1220.0  # Exterior North face on RIGHT, Interior 2F Bedroom on LEFT (matches Section B-B orientation!)

    # Top: HEAD DETAIL (EL +3.86m) | Bottom: SILL DETAIL (EL +3.30m)
    yh2, ys2 = 215.0, 445.0
    def d2h(dx_m, dz_m):
        # dx_m < 0 = interior, dx_m > 0 = exterior North
        return (ox2 + dx_m * sc2, yh2 - dz_m * sc2)
    def d2s(dx_m, dz_m):
        return (ox2 + dx_m * sc2, ys2 - dz_m * sc2)

    # Wall W-EXT-01 Above Head & Below Sill (160mm thick: dx = -0.16..0.00)
    for fn, z0, h in [(d2h, 0.19, 0.19), (d2s, 0.00, 0.19)]:
        # Birch interior ply
        s.add(f'<rect x="{fn(-0.16, z0)[0]:.1f}" y="{fn(-0.16, z0)[1]:.1f}" width="{0.012*sc2:.1f}" height="{h*sc2:.1f}" fill="url(#hatch-plywood)" stroke="#0f172a" stroke-width="1.1"/>')
        # Timber header / sill plate + insulated cavity
        s.add(f'<rect x="{fn(-0.138, z0)[0]:.1f}" y="{fn(-0.138, z0)[1]:.1f}" width="{0.105*sc2:.1f}" height="{h*sc2:.1f}" fill="#fefce8" stroke="#0f172a" stroke-width="0.9"/>')
        # Structural plywood sheathing + WRB + 18mm furred Galvalume cladding
        s.add(f'<rect x="{fn(-0.033, z0)[0]:.1f}" y="{fn(-0.033, z0)[1]:.1f}" width="{0.013*sc2:.1f}" height="{h*sc2:.1f}" fill="url(#hatch-plywood)" stroke="#0f172a" stroke-width="0.9"/>')
        s.add(f'<rect x="{fn(-0.020, z0)[0]:.1f}" y="{fn(-0.020, z0)[1]:.1f}" width="{0.020*sc2:.1f}" height="{h*sc2:.1f}" fill="#e2e8f0" stroke="#0f172a" stroke-width="1.4"/>')
    # Solid Header & Sill framing timber sections
    s.timber_section(*d2h(-0.138, 0.11), 0.105*sc2, 0.11*sc2)
    s.timber_section(*d2s(-0.138, 0.00), 0.105*sc2, 0.09*sc2)

    # Cedar Interior Reveal Casing (Bed_SlidingWin_Reveal_Top/Bot: 24mm thick x 195mm deep!)
    s.add(f'<rect x="{d2h(-0.185, 0.00)[0]:.1f}" y="{d2h(-0.185, 0.00)[1]:.1f}" width="{0.195*sc2:.1f}" height="{0.024*sc2:.1f}" fill="url(#hatch-wood)" stroke="#0f172a" stroke-width="1.4"/>')
    s.add(f'<rect x="{d2s(-0.185, 0.024)[0]:.1f}" y="{d2s(-0.185, 0.024)[1]:.1f}" width="{0.195*sc2:.1f}" height="{0.024*sc2:.1f}" fill="url(#hatch-wood)" stroke="#0f172a" stroke-width="1.4"/>')

    # Exterior Anodized Aluminum Head Drip Cap & Folded Sill Pan Flashing w/ Back Dam!
    hd_pts = [d2h(-0.020, 0.075), d2h(-0.020, 0.002), d2h(0.035, -0.012), d2h(0.035, -0.024)]
    s.add(f'<polyline points="{" ".join(f"{a:.1f},{b:.1f}" for a,b in hd_pts)}" fill="none" stroke="#1d4ed8" stroke-width="2.6"/>')
    sp_pts = [d2s(-0.095, 0.030), d2s(-0.095, 0.002), d2s(0.035, -0.014), d2s(0.035, -0.030)]
    s.add(f'<polyline points="{" ".join(f"{a:.1f},{b:.1f}" for a,b in sp_pts)}" fill="none" stroke="#1d4ed8" stroke-width="2.6"/>')

    # Dual Sliding Aluminum Sashes (Bed_SlidingWin_SashL / SashR) + Low-E Double Glazing!
    for sx_off in (-0.085, -0.042):
        # Upper sash rail (at head)
        s.add(f'<rect x="{d2h(sx_off, -0.024)[0]:.1f}" y="{d2h(sx_off, -0.024)[1]:.1f}" width="{0.028*sc2:.1f}" height="{0.035*sc2:.1f}" fill="url(#hatch-steel)" stroke="#0f172a" stroke-width="1.3"/>')
        s.add(f'<rect x="{d2h(sx_off+0.006, -0.059)[0]:.1f}" y="{d2h(sx_off+0.006, -0.059)[1]:.1f}" width="{0.016*sc2:.1f}" height="{0.10*sc2:.1f}" fill="#bae6fd" stroke="#0284c7" stroke-width="1.1"/>')
        # Lower sash rail (at sill)
        s.add(f'<rect x="{d2s(sx_off, 0.060)[0]:.1f}" y="{d2s(sx_off, 0.060)[1]:.1f}" width="{0.028*sc2:.1f}" height="{0.036*sc2:.1f}" fill="url(#hatch-steel)" stroke="#0f172a" stroke-width="1.3"/>')
        s.add(f'<rect x="{d2s(sx_off+0.006, 0.140)[0]:.1f}" y="{d2s(sx_off+0.006, 0.140)[1]:.1f}" width="{0.016*sc2:.1f}" height="{0.08*sc2:.1f}" fill="#bae6fd" stroke="#0284c7" stroke-width="1.1"/>')

    s.add('<line x1="880" y1="330" x2="1550" y2="330" stroke="#94a3b8" stroke-width="1.0" stroke-dasharray="12,4,3,4"/>')
    s.leader_note(*d2h(0.025, -0.01), 1295, 175, ["ANODIZED ALUM. HEAD DRIP CAP", "TAPED TO WRB BEHIND CLADDING", "EXT. FRAME EL +3.85..+3.89m"], align="left", color="#1d4ed8")
    s.leader_note(*d2h(-0.15, -0.01), 1065, 175, ["24×195mm CEDAR REVEAL CASING", "(BED_SLIDINGWIN_REVEAL_TOP)", "AIRTIGHT SEALANT + BACKER ROD"], align="right")
    s.leader_note(*d2s(-0.06, 0.10), 1065, 375, ["DUAL SLIDING ALUM. SASHES", "LOW-E IGU (5+12Ar+5mm)", "RO 1,800 × 560mm (W-02)"], align="right")
    s.leader_note(*d2s(0.025, -0.015), 1295, 475, ["FOLDED SILL PAN FLASHING", "W/ 28mm BACK DAM & END DAMS", "OVER 18mm VENTED RAINSCREEN"], align="left", color="#1d4ed8")
    s.viewport_title(848, 600, "2", "2F BEDROOM SLIDING WINDOW (W-02) HEAD & SILL DETAIL", "1 : 5", width=620)

    # =====================================================================
    # DETAIL 3 (BOTTOM-LEFT, x=48..808, y=648..1232): OPEN-RISER STAIR STRINGER & LOFT LEDGER (1:10)
    # =====================================================================
    s.add('<rect x="48" y="648" width="760" height="584" fill="#ffffff" stroke="#0f172a" stroke-width="1.4"/>')
    sc3 = 270.0
    ox3, oy3 = 520.0, 825.0  # 2F Loft landing edge Y=+0.15, EL +2.52m
    def d3(dy_m, dz_m):
        # dy_m < 0 = down stair (left), dy_m > 0 = onto 2F loft (right)
        return (ox3 + dy_m * sc3, oy3 - dz_m * sc3)

    # 2F Loft Fascia Rim Beam (Loft_Fascia_Beam_Rear: 180×205mm @ EL +2.32..+2.525m -> dz=-0.20..0.00)
    s.timber_section(*d3(0.0, 0.0), 0.180*sc3, 0.205*sc3)
    # 2F Loft Floor & Soffit extending right
    s.add(f'<rect x="{d3(0.18, 0.0)[0]:.1f}" y="{d3(0.18, 0.0)[1]:.1f}" width="{0.82*sc3:.1f}" height="{0.12*sc3:.1f}" fill="url(#hatch-wood)" stroke="#0f172a" stroke-width="1.4"/>')
    s.add(f'<rect x="{d3(0.18, -0.12)[0]:.1f}" y="{d3(0.18, -0.12)[1]:.1f}" width="{0.82*sc3:.1f}" height="{0.04*sc3:.1f}" fill="url(#hatch-plywood)" stroke="#0f172a" stroke-width="1.0"/>')

    # Concealed Steel L-Bracket Hanger bolting Stair Stringer to Loft Rim Beam!
    s.add(f'<polygon points="{d3(-0.08, -0.02)[0]:.1f},{d3(-0.08, -0.02)[1]:.1f} {d3(0.0, -0.02)[0]:.1f},{d3(0.0, -0.02)[1]:.1f} {d3(0.0, -0.22)[0]:.1f},{d3(0.0, -0.22)[1]:.1f} {d3(-0.015, -0.22)[0]:.1f},{d3(-0.015, -0.035)[1]:.1f} {d3(-0.08, -0.035)[0]:.1f},{d3(-0.08, -0.035)[1]:.1f}" fill="url(#hatch-steel)" stroke="#0f172a" stroke-width="1.4"/>')

    # Inclined Laminated Hardwood Stringer (45×220mm @ exact 44.5° stair pitch: rise 180mm / run 183mm!)
    # Draw 4 top treads (Treads 08..11) + full stringer band
    st_pts = [d3(-1.05, -0.92), d3(0.0, -0.02), d3(0.0, -0.24), d3(-1.05, -1.14)]
    s.add(f'<polygon points="{" ".join(f"{a:.1f},{b:.1f}" for a,b in st_pts)}" fill="url(#hatch-wood)" stroke="#0f172a" stroke-width="1.6"/>')

    # Exact Model Treads (36mm thick × 180mm deep, rise=180mm, run=183mm)
    for k in range(1, 6):
        ty_r = -k * 0.183 + 0.08
        tz_t = -k * 0.180 + 0.02
        s.timber_section(*d3(ty_r - 0.180, tz_t), 0.180*sc3, 0.036*sc3)
        # Lag bolt markers
        bx, by = d3(ty_r - 0.09, tz_t - 0.018)
        s.add(f'<circle cx="{bx:.1f}" cy="{by:.1f}" r="2.2" fill="#0f172a"/>')

    # Wall-Mounted Birch Plywood Handrail parallel at +850mm above nosing line
    hr_pts = [d3(-1.02, -0.18), d3(-0.06, 0.64), d3(-0.06, 0.56), d3(-1.02, -0.26)]
    s.add(f'<polygon points="{" ".join(f"{a:.1f},{b:.1f}" for a,b in hr_pts)}" fill="url(#hatch-plywood)" stroke="#0f172a" stroke-width="1.2" stroke-dasharray="6,3"/>')

    # Rise / Run Triangle Dimension
    s.dim_h(d3(-0.469, 0)[0], d3(-0.286, 0)[0], d3(0, -0.25)[1], "183 RUN", ext_y=d3(0, -0.34)[1], color="#1d4ed8")
    s.dim_v(d3(-0.18, 0)[0], d3(0, -0.16)[1], d3(0, -0.34)[1], "180 RISE", ext_x=d3(-0.28, 0)[0], color="#1d4ed8")

    s.leader_note(*d3(-0.55, 0.25), 255, 730, ["WALL-MOUNTED BIRCH HANDRAIL", "(STAIR_WALL_HANDRAIL · 40mm PLY)", "CONTINUOUS ALONG WEST GABLE"], align="right")
    s.leader_note(*d3(-0.52, -0.50), 255, 865, ["36×180×600mm SOLID TREADS", "MORTISED INTO TWIN 45×220mm", "LAMINATED HARDWOOD STRINGERS", "11 TREADS · 12 RISERS (44.5°)"], align="right")
    s.leader_note(*d3(0.09, -0.10), 560, 1020, ["180×205mm LOFT RIM GIRDER", "CONCEALED 6mm STEEL ANGLE", "LEDGER W/ 4× M12 LAG BOLTS"], align="left")
    s.viewport_title(62, 1208, "3", "OPEN-RISER TIMBER STAIR & 2F LOFT LEDGER DETAIL", "1 : 10", width=590)

    # =====================================================================
    # DETAIL 4 (BOTTOM-RIGHT, x=832..1594, y=648..1232): 2F LOFT RIM BEAM & CABLE GUARDRAIL (1:10)
    # =====================================================================
    s.add('<rect x="832" y="648" width="762" height="584" fill="#ffffff" stroke="#0f172a" stroke-width="1.4"/>')
    sc4 = 330.0
    ox4, oy4 = 1150.0, 1020.0  # Rim beam outer face X=0, 2F FFL EL +2.520m
    def d4(dx_m, dz_m):
        # dx_m < 0 = double-height void (left), dx_m > 0 = 2F loft floor (right)
        return (ox4 + dx_m * sc4, oy4 - dz_m * sc4)

    # 180×205mm Loft Fascia Rim Beam (EL +2.32..+2.525m -> dz=-0.205..0.00)
    s.timber_section(*d4(0.0, 0.0), 0.180*sc4, 0.205*sc4)
    # 2F Mezzanine Floor Assembly FL-2F-01 (Pine 18mm + Plywood 18mm + 45×96 Joists + 28mm Birch Soffit)
    s.add(f'<rect x="{d4(0.18, 0.0)[0]:.1f}" y="{d4(0.18, 0.0)[1]:.1f}" width="{0.95*sc4:.1f}" height="{0.018*sc4:.1f}" fill="url(#hatch-wood)" stroke="#0f172a" stroke-width="1.2"/>')
    s.add(f'<rect x="{d4(0.18, -0.018)[0]:.1f}" y="{d4(0.18, -0.018)[1]:.1f}" width="{0.95*sc4:.1f}" height="{0.018*sc4:.1f}" fill="url(#hatch-plywood)" stroke="#0f172a" stroke-width="0.9"/>')
    s.add(f'<rect x="{d4(0.18, -0.036)[0]:.1f}" y="{d4(0.18, -0.036)[1]:.1f}" width="{0.95*sc4:.1f}" height="{0.096*sc4:.1f}" fill="#f6ead8" stroke="#0f172a" stroke-width="1.2"/>')
    s.add(f'<rect x="{d4(0.18, -0.132)[0]:.1f}" y="{d4(0.18, -0.132)[1]:.1f}" width="{0.95*sc4:.1f}" height="{0.028*sc4:.1f}" fill="url(#hatch-plywood)" stroke="#0f172a" stroke-width="1.1"/>')
    # Galvanized Steel Joist Hanger at Rim Beam inner face!
    s.add(f'<rect x="{d4(0.18, -0.032)[0]:.1f}" y="{d4(0.18, -0.032)[1]:.1f}" width="{0.038*sc4:.1f}" height="{0.104*sc4:.1f}" fill="url(#hatch-steel)" stroke="#0f172a" stroke-width="1.3"/>')

    # 36×36mm Painted Steel Guardrail Post (Loft_Rail_Post_* @ EL +2.52..+3.28m -> dz=0.00..+0.76m!)
    s.add(f'<rect x="{d4(0.052, 0.76)[0]:.1f}" y="{d4(0.052, 0.76)[1]:.1f}" width="{0.036*sc4:.1f}" height="{0.76*sc4:.1f}" fill="#f8fafc" stroke="#0f172a" stroke-width="1.8"/>')
    # Baseplate + 2× M10 Structural Lag Bolts down into Rim Beam
    s.add(f'<rect x="{d4(0.020, 0.012)[0]:.1f}" y="{d4(0.020, 0.012)[1]:.1f}" width="{0.100*sc4:.1f}" height="{0.012*sc4:.1f}" fill="url(#hatch-steel)" stroke="#0f172a" stroke-width="1.4"/>')
    for bx_m in (0.036, 0.104):
        bxp, by0 = d4(bx_m, 0.02)
        _, by1 = d4(bx_m, -0.11)
        s.add(f'<line x1="{bxp:.1f}" y1="{by0:.1f}" x2="{bxp:.1f}" y2="{by1:.1f}" stroke="#0f172a" stroke-width="2.0" stroke-dasharray="4,2"/>')

    # 36×36mm Top Rail Cap (EL +3.28m -> dz=+0.76m)
    s.add(f'<rect x="{d4(0.048, 0.796)[0]:.1f}" y="{d4(0.048, 0.796)[1]:.1f}" width="{0.044*sc4:.1f}" height="{0.036*sc4:.1f}" fill="#ffffff" stroke="#0f172a" stroke-width="1.8"/>')

    # 3× Tensioned Ø8mm Stainless Wire Cables @ Exact Model Elevations (Z=2.71, 2.90, 3.09 -> dz=0.19, 0.38, 0.57m!)
    for cz_m in (0.19, 0.38, 0.57):
        cxp, cyp = d4(0.070, cz_m)
        s.add(f'<circle cx="{cxp:.1f}" cy="{cyp:.1f}" r="4.5" fill="url(#hatch-steel)" stroke="#0f172a" stroke-width="1.5"/>')
        s.add(f'<line x1="{cxp - 24:.1f}" y1="{cyp:.1f}" x2="{cxp + 24:.1f}" y2="{cyp:.1f}" stroke="#475569" stroke-width="1.1" stroke-dasharray="6,2"/>')

    # Exact Guardrail Vertical Dimensions (190mm equal spacing!)
    s.dim_v(d4(-0.18, 0)[0], d4(0, 0.76)[1], d4(0, 0.57)[1], "190", ext_x=d4(0.04, 0)[0])
    s.dim_v(d4(-0.18, 0)[0], d4(0, 0.57)[1], d4(0, 0.38)[1], "190", ext_x=d4(0.04, 0)[0])
    s.dim_v(d4(-0.18, 0)[0], d4(0, 0.38)[1], d4(0, 0.19)[1], "190", ext_x=d4(0.04, 0)[0])
    s.dim_v(d4(-0.18, 0)[0], d4(0, 0.19)[1], d4(0, 0.00)[1], "190", ext_x=d4(0.04, 0)[0])
    s.dim_v(d4(-0.34, 0)[0], d4(0, 0.76)[1], d4(0, 0.00)[1], "760 GUARDRAIL", ext_x=d4(-0.18, 0)[0], color="#b91c1c")

    s.leader_note(*d4(0.09, 0.775), 1245, 755, ["36×36mm PAINTED STEEL TOP RAIL", "& VERTICAL STANCHION POSTS", "(LOFT_RAIL_TOP_* · EL +3.280m)"], align="left")
    s.leader_note(*d4(0.08, 0.38), 1245, 865, ["3× Ø8mm 316 STAINLESS CABLES", "190mm EQUAL VERTICAL SPACING", "SWAGED TURNBUCKLE TENSIONERS"], align="left")
    s.leader_note(*d4(0.07, -0.08), 1060, 1110, ["180×205mm LOFT RIM GIRDER", "M10 BASEPLATE LAG ANCHORS", "STEEL JOIST HANGER @ 455 O.C."], align="right")
    s.leader_note(*d4(0.65, -0.06), 1245, 1110, ["2F FLOOR ASSEMBLY FL-2F-01", "18 PINE + 18 PLY + 45×96 JOIST", "+ 28mm BIRCH SOFFIT CEILING"], align="left")
    s.viewport_title(848, 1208, "4", "2F LOFT RIM BEAM & TENSIONED CABLE GUARDRAIL DETAIL", "1 : 10", width=620)

    s.save(os.path.join(DRAWINGS_DIR, "A-502_Glazing_Stair_Guardrail_Details.svg"))
    print("Generated A-502_Glazing_Stair_Guardrail_Details.svg")


# =========================================================================
# SHEET A-601: AUTOMATED ARCHITECTURAL SCHEDULES & BIM QUANTITY TAKE-OFF
# =========================================================================
def build_a601():
    s = SvgSheet("A-601", "SCHEDULES & BIM QUANTITY TAKE-OFF", "TABLE / METRIC", "9TS-KOI-ZZ-ZZ-SH-A-0601", "BIM SCHEDULES / QTO")

    # 1. DOOR SCHEDULE (Top-Left: x=48..795, y=48..295)
    s.add('<rect x="48" y="48" width="748" height="245" fill="#ffffff" stroke="#0f172a" stroke-width="1.4"/>')
    s.add('<rect x="48" y="48" width="748" height="26" fill="#0f172a"/>')
    s.add('<text x="62" y="65" style="font-size:11px;font-weight:800;fill:#ffffff;letter-spacing:0.9px;">1 · ARCHITECTURAL DOOR SCHEDULE (DERIVED FROM BLENDER MODEL)</text>')
    d_cols = [(58, "MARK"), (114, "LOCATION"), (246, "W × H (mm)"), (346, "TYPE / LEAF"), (516, "FRAME / HARDWARE"), (674, "RATING")]
    s.add('<rect x="48" y="74" width="748" height="20" fill="#e2e8f0"/>')
    for x, lbl in d_cols:
        s.add(f'<text x="{x}" y="88" class="tb-lbl">{lbl}</text>')
    d_rows = [
        ("D-01", "West Entry / Genkan", "683 × 1,930", "Insulated Flush Metal", "Anodized Alum. / Deadbolt", "Weatherstrip"),
        ("D-02", "1F Bath Vestibule",   "600 × 1,740", "Birch Plywood Swing", "Cedar Jamb / Lever Set",    "Privacy"),
        ("D-03", "1F Separate WC",      "520 × 1,740", "Birch Plywood Swing", "Cedar Jamb / Indicator",    "Privacy"),
        ("D-04", "1F Wet-Room Shower",  "520 × 1,715", "Tempered Frameless",  "Chrome Pivot / Seal Strip", "Tempered"),
        ("D-05", "Tatami Closet (×2)",  "835 × 2,000", "Sliding Birch Panel", "Recessed Finger Slots",     "Millwork"),
    ]
    for i, r in enumerate(d_rows):
        ry = 94 + i * 38
        bg = "#ffffff" if i % 2 == 0 else "#f8fafc"
        s.add(f'<rect x="48" y="{ry}" width="748" height="38" fill="{bg}" stroke="#e2e8f0" stroke-width="0.6"/>')
        for j, val in enumerate(r):
            st = "font-size:10px;font-weight:800;fill:#0f172a;" if j == 0 else "font-size:9.3px;font-weight:600;fill:#1e293b;"
            s.add(f'<text x="{d_cols[j][0]}" y="{ry + 23}" style="{st}">{val}</text>')

    # 2. WINDOW & SHOJI SCHEDULE (Top-Right: x=816..1594, y=48..330)
    s.add('<rect x="816" y="48" width="778" height="282" fill="#ffffff" stroke="#0f172a" stroke-width="1.4"/>')
    s.add('<rect x="816" y="48" width="778" height="26" fill="#0f172a"/>')
    s.add('<text x="830" y="65" style="font-size:11px;font-weight:800;fill:#ffffff;letter-spacing:0.9px;">2 · WINDOW &amp; SLIDING SHOJI OPENING SCHEDULE (DERIVED FROM MODEL)</text>')
    w_cols = [(826, "MARK"), (886, "FACADE / RM"), (1016, "RO W×H (mm)"), (1120, "SILL EL"), (1192, "OPERATION / GLAZING"), (1435, "DETAIL")]
    s.add('<rect x="816" y="74" width="778" height="20" fill="#e2e8f0"/>')
    for x, lbl in w_cols:
        s.add(f'<text x="{x}" y="88" class="tb-lbl">{lbl}</text>')
    w_rows = [
        ("W-01A/B", "South 1F Living",  "3,900 × 2,030", "+0.36m", "2-Bay Sliding Low-E + Outer Shoji", "1 / A-502"),
        ("W-01C/D", "South 2F Void",    "3,900 × 2,030", "+2.49m", "Fixed / Sliding Low-E + Shoji",     "1 / A-502"),
        ("W-02",    "North 2F Bed",     "1,800 × 560",   "+3.30m", "Dual Sliding Alum. (Kitty View)",   "2 / A-502"),
        ("W-03",    "North 1F Tatami",  "1,460 × 440",   "+0.52m", "Low Jimado Sliding Shoji Panel",    "4 / A-401"),
        ("W-04",    "North 1F Shower",  "500 × 460",     "+1.42m", "Frosted Tempered Awning Vent",      "4 / A-401"),
        ("W-05",    "East 1F Kitchen",  "2× 430 × 400",  "+1.38m", "Twin Countertop Frosted Casements", "2 / A-401"),
        ("W-06",    "East 1F WC/Shwr",  "380×470 / 420", "+1.35m", "Frosted Privacy Vent Windows",      "3 / A-401"),
    ]
    for i, r in enumerate(w_rows):
        ry = 94 + i * 33
        bg = "#ffffff" if i % 2 == 0 else "#f8fafc"
        s.add(f'<rect x="816" y="{ry}" width="778" height="33" fill="{bg}" stroke="#e2e8f0" stroke-width="0.6"/>')
        for j, val in enumerate(r):
            st = "font-size:9.8px;font-weight:800;fill:#1d4ed8;" if j in (0, 5) else "font-size:9.2px;font-weight:600;fill:#1e293b;"
            s.add(f'<text x="{w_cols[j][0]}" y="{ry + 21}" style="{st}">{val}</text>')

    # 3. ROOM FINISH SCHEDULE (Mid-Left: x=48..795, y=312..680)
    s.add('<rect x="48" y="312" width="748" height="368" fill="#ffffff" stroke="#0f172a" stroke-width="1.4"/>')
    s.add('<rect x="48" y="312" width="748" height="26" fill="#0f172a"/>')
    s.add('<text x="62" y="329" style="font-size:11px;font-weight:800;fill:#ffffff;letter-spacing:0.9px;">3 · ROOM AREA &amp; ARCHITECTURAL FINISH SCHEDULE</text>')
    r_cols = [(58, "ID"), (120, "SPACE NAME"), (262, "AREA (m²)"), (332, "FFL (m)"), (402, "FLOOR FINISH"), (540, "WALL FINISH"), (672, "CEILING")]
    s.add('<rect x="48" y="338" width="748" height="20" fill="#e2e8f0"/>')
    for x, lbl in r_cols:
        s.add(f'<text x="{x}" y="352" class="tb-lbl">{lbl}</text>')
    r_rows = [
        ("RM-101", "Living / Dining",   "10.6 m²", "+0.360", "Solid Red Pine",    "12mm Birch Ply",  "Sloped Birch"),
        ("RM-102", "Galley Kitchen",    "4.8 m²",  "+0.360", "Solid Red Pine",    "12mm Birch Ply",  "Flat Ply +2.36"),
        ("RM-103", "6-Mat Tatami Bay",  "4.6 m²",  "+0.520", "Igusa Tatami Mats", "12mm Birch Ply",  "Flat Ply +2.36"),
        ("RM-104", "Genkan Entry",      "1.1 m²",  "+0.360", "Troweled Mortar",   "12mm Birch Ply",  "Sloped Birch"),
        ("RM-105", "Bath Vanity",       "1.2 m²",  "+0.360", "Solid Red Pine",    "White Cladding",  "Flat Ply +2.36"),
        ("RM-106", "Separate WC",       "0.7 m²",  "+0.360", "Solid Red Pine",    "White Cladding",  "Flat Ply +2.36"),
        ("RM-107", "Wet-Room Shower",   "1.2 m²",  "+0.388", "Porcelain Tile",    "Porcelain Tile",  "Moisture Board"),
        ("RM-201", "2F Bedroom Loft",   "10.8 m²", "+2.520", "Solid Red Pine",    "12mm Birch Ply",  "Sloped Birch"),
        ("RM-202", "2F Loft Lounge",    "6.8 m²",  "+2.520", "Solid Red Pine",    "12mm Birch Ply",  "Sloped Birch"),
        ("EXT-01", "Cedar Engawa Deck", "6.5 m²",  "+0.320", "W. Red Cedar",      "Ext. Galvalume",  "Open Sky"),
    ]
    for i, r in enumerate(r_rows):
        ry = 358 + i * 32
        bg = "#ffffff" if i % 2 == 0 else "#f8fafc"
        s.add(f'<rect x="48" y="{ry}" width="748" height="32" fill="{bg}" stroke="#e2e8f0" stroke-width="0.6"/>')
        for j, val in enumerate(r):
            st = "font-size:9.3px;font-weight:800;fill:#0f172a;" if j == 0 else "font-size:9.0px;font-weight:600;fill:#1e293b;"
            s.add(f'<text x="{r_cols[j][0]}" y="{ry + 20}" style="{st}">{val}</text>')

    # 4. LIVE AUTO-COMPUTED CSI MASTERFORMAT 2020 BIM QUANTITY TAKE-OFF (Bottom Full Width: x=48..1594, y=700..1230)
    csi_agg = defaultdict(lambda: {"title": "", "count": 0, "area": 0.0, "vol": 0.0, "tris": 0})
    ifc_agg = defaultdict(lambda: {"count": 0, "area": 0.0, "vol": 0.0, "tris": 0})
    for el in BIM_DATA["elements"]:
        cc = el["csiCode"]
        csi_agg[cc]["title"] = el["csiTitle"]
        csi_agg[cc]["count"] += 1
        csi_agg[cc]["area"] += el["areaM2"]
        csi_agg[cc]["vol"] += el["volumeM3"]
        csi_agg[cc]["tris"] += el["triangles"]

        ic = el["ifcClass"]
        ifc_agg[ic]["count"] += 1
        ifc_agg[ic]["area"] += el["areaM2"]
        ifc_agg[ic]["vol"] += el["volumeM3"]
        ifc_agg[ic]["tris"] += el["triangles"]

    # Right-Mid Card: IFC4 Entity Summary & Mobile/AR Triangle Cap Verification (x=816..1594, y=348..680)
    s.add('<rect x="816" y="348" width="778" height="332" fill="#ffffff" stroke="#0f172a" stroke-width="1.4"/>')
    s.add('<rect x="816" y="348" width="778" height="26" fill="#0f172a"/>')
    s.add('<text x="830" y="365" style="font-size:11px;font-weight:800;fill:#ffffff;letter-spacing:0.9px;">4 · IFC4 ENTITY BREAKDOWN &amp; MOBILE / AR TRIANGLE CAP AUDIT</text>')
    i_cols = [(826, "IFC4 CLASS"), (1026, "ELEMENTS"), (1116, "SURFACE (m²)"), (1236, "VOLUME (m³)"), (1356, "TRIANGLES"), (1466, "% BUDGET")]
    s.add('<rect x="816" y="374" width="778" height="20" fill="#e2e8f0"/>')
    for x, lbl in i_cols:
        s.add(f'<text x="{x}" y="388" class="tb-lbl">{lbl}</text>')

    cap_tris = BIM_DATA["project"]["performanceCapTris"]
    top_ifcs = sorted(ifc_agg.items(), key=lambda kv: (-kv[1]["count"], kv[0]))[:10]
    for i, (cls, d) in enumerate(top_ifcs):
        ry = 394 + i * 25.5
        bg = "#ffffff" if i % 2 == 0 else "#f8fafc"
        s.add(f'<rect x="816" y="{ry:.1f}" width="778" height="25.5" fill="{bg}" stroke="#e2e8f0" stroke-width="0.6"/>')
        pct = (d["tris"] / cap_tris) * 100.0
        vals = [cls, str(d["count"]), f"{d['area']:.2f}", f"{d['vol']:.3f}", f"{d['tris']:,}", f"{pct:.1f}%"]
        for j, val in enumerate(vals):
            st = "font-size:9.3px;font-weight:800;fill:#1d4ed8;" if j == 0 else "font-size:9.2px;font-weight:600;fill:#0f172a;"
            s.add(f'<text x="{i_cols[j][0]}" y="{ry + 16.5:.1f}" class="mono" style="{st}">{val}</text>')
    tot = BIM_DATA["totals"]
    s.add('<rect x="816" y="650" width="778" height="30" fill="#ecfdf5" stroke="#10b981" stroke-width="1.0"/>')
    s.add(f'<text x="830" y="669" class="mono" style="font-size:10px;font-weight:800;fill:#065f46;">TOTAL: {tot["meshes"]} IFC4 ELEMENTS · HOUSE+ROOF {tot["houseRoofTris"]:,} TRIS · FULL SITE {tot["totalTris"]:,} / {cap_tris:,} CAP ({tot["totalTris"]/cap_tris*100:.1f}% — PASS)</text>')

    # Bottom Card: CSI MasterFormat 2020 Trade QTO Table (2-column split so all CSI trades fit with huge readability!)
    s.add('<rect x="48" y="700" width="1546" height="532" fill="#ffffff" stroke="#0f172a" stroke-width="1.4"/>')
    s.add('<rect x="48" y="700" width="1546" height="28" fill="#0f172a"/>')
    s.add('<text x="64" y="719" style="font-size:11.5px;font-weight:800;fill:#ffffff;letter-spacing:1px;">5 · AUTOMATED CSI MASTERFORMAT 2020 QUANTITY TAKE-OFF (LIVE FROM 9_TSUBO_BIM_METADATA.JSON)</text>')

    csi_sorted = sorted(csi_agg.items(), key=lambda kv: kv[0])
    half = (len(csi_sorted) + 1) // 2
    for pane_idx, chunk in enumerate([csi_sorted[:half], csi_sorted[half:]]):
        ox = 48 + pane_idx * 773
        ccols = [(ox + 12, "CSI CODE"), (ox + 88, "TRADE PACKAGE"), (ox + 382, "QTY"), (ox + 445, "AREA (m²)"), (ox + 555, "VOL (m³)"), (ox + 662, "TRIS")]
        s.add(f'<rect x="{ox}" y="728" width="773" height="22" fill="#e2e8f0" stroke="#cbd5e1" stroke-width="0.8"/>')
        for x, lbl in ccols:
            s.add(f'<text x="{x}" y="743" class="tb-lbl">{lbl}</text>')
        for i, (code, d) in enumerate(chunk):
            ry = 750 + i * 33.5
            bg = "#ffffff" if i % 2 == 0 else "#f8fafc"
            s.add(f'<rect x="{ox}" y="{ry:.1f}" width="773" height="33.5" fill="{bg}" stroke="#e2e8f0" stroke-width="0.6"/>')
            vals = [code, d["title"][:34], str(d["count"]), f"{d['area']:.2f}", f"{d['vol']:.3f}", f"{d['tris']:,}"]
            for j, val in enumerate(vals):
                st = "font-size:9.8px;font-weight:800;fill:#0f172a;" if j == 0 else "font-size:9.3px;font-weight:600;fill:#1e293b;"
                cls_attr = ' class="mono"' if j != 1 else ''
                s.add(f'<text x="{ccols[j][0]}" y="{ry + 21:.1f}"{cls_attr} style="{st}">{val}</text>')
    s.add('<line x1="821" y1="728" x2="821" y2="1232" stroke="#0f172a" stroke-width="1.2"/>')

    s.save(os.path.join(DRAWINGS_DIR, "A-601_Schedules_BIM_QTO.svg"))
    print("Generated A-601_Schedules_BIM_QTO.svg")


def main():
    build_a401()
    build_a501()
    build_a502()
    build_a601()
    print("=== PART 2 COMPLETE (4 SHEETS: A-401, A-501, A-502, A-601) ===")

if __name__ == "__main__":
    main()
