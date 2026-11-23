"""
9-Tsubo House (Koizumi Studio, 1999) — ISO 19650 / IFC4 BIM Metadata Extractor
Runs inside Blender 5.2 LTS on 9_tsubo_house.blend to generate 9_tsubo_bim_metadata.json.
Implements the Hybrid LOD-300 (Mobile/AR lightweight 3D) -> LOD-400 (Parametric Construction Assembly)
data bridge inspired by BIMCraft / ISO 19650-2 workflows.
"""
import bpy
import bmesh
import json
import hashlib
import os
from mathutils import Vector

REPO_ROOT = r"C:\Users\paque\.gemini\antigravity\scratch\9TsuboHouseV2"
OUT_JSON = os.path.join(REPO_ROOT, "9_tsubo_bim_metadata.json")

ISO_CONTAINER = "9TS-KOI-ZZ-ZZ-M3-A-0001"
IFC_B64 = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz_$"

def make_ifc_guid(seed: str) -> str:
    h = hashlib.sha256(f"9TsuboV2::{seed}".encode("utf-8")).digest()
    num = int.from_bytes(h[:16], "big")
    chars = []
    for _ in range(22):
        chars.append(IFC_B64[num & 63])
        num >>= 6
    return "".join(reversed(chars))

# LOD-400 Construction Assembly Dictionary (Drives both BIM Inspector & Automatic 2D Details!)
ASSEMBLIES = {
    "W-EXT-01": {
        "code": "W-EXT-01",
        "title": "Exterior Insulated Galvalume Timber-Frame Wall (160mm)",
        "totalThicknessMm": 160,
        "uValue": "0.34 W/m²·K",
        "fireRating": "30-min Residential Timber",
        "layers": [
            {"seq": 1, "material": "Pre-painted Galvalume Steel Cladding (White)", "thicknessMm": 1, "function": "Weather Cladding"},
            {"seq": 2, "material": "Vertical Cedar Furring Strips (Vented Rainscreen Cavity)", "thicknessMm": 18, "function": "Drainage / Air Gap"},
            {"seq": 3, "material": "Breathable Water-Resistive Barrier (Tyvek WRB)", "thicknessMm": 1, "function": "Air / Moisture Barrier"},
            {"seq": 4, "material": "Structural Plywood Shear Sheathing (JAS 12mm)", "thicknessMm": 12, "function": "Lateral Shear"},
            {"seq": 5, "material": "105×105mm Hinoki/Cedar Posts & Studs w/ 100mm Mineral Wool", "thicknessMm": 105, "function": "Structure + Thermal"},
            {"seq": 6, "material": "Polyethylene Vapor Retarder (0.2mm)", "thicknessMm": 1, "function": "Vapor Control"},
            {"seq": 7, "material": "Interior Acoustic Furring / Service Cavity", "thicknessMm": 10, "function": "Wiring Chase"},
            {"seq": 8, "material": "Exposed Birch / Lauan Structural Plywood Lining (12mm)", "thicknessMm": 12, "function": "Interior Finish"}
        ]
    },
    "W-INT-01": {
        "code": "W-INT-01",
        "title": "Interior Partition Wall (75mm)",
        "totalThicknessMm": 75,
        "uValue": "Interior Partition",
        "fireRating": "Non-Rated",
        "layers": [
            {"seq": 1, "material": "Painted Gypsum / Birch Plywood Facing", "thicknessMm": 12, "function": "Finish"},
            {"seq": 2, "material": "45×51mm Timber Studs @ 455mm O.C. w/ Acoustic Batt", "thicknessMm": 51, "function": "Framing / Acoustic"},
            {"seq": 3, "material": "Painted Gypsum / Birch Plywood Facing", "thicknessMm": 12, "function": "Finish"}
        ]
    },
    "RF-01": {
        "code": "RF-01",
        "title": "Asymmetric Gable Standing-Seam Galvalume Roof (152mm)",
        "totalThicknessMm": 152,
        "uValue": "0.24 W/m²·K",
        "fireRating": "Class A Non-Combustible Metal",
        "layers": [
            {"seq": 1, "material": "0.4mm Standing-Seam Charcoal Galvalume Roofing", "thicknessMm": 1, "function": "Primary Waterproofing"},
            {"seq": 2, "material": "Modified Bitumen Asphalt Roofing Underlayment", "thicknessMm": 2, "function": "Secondary Membrane"},
            {"seq": 3, "material": "12mm Structural Plywood Roof Deck", "thicknessMm": 12, "function": "Diaphragm Deck"},
            {"seq": 4, "material": "24mm Eave-to-Ridge Vented Air Channel", "thicknessMm": 24, "function": "Roof Ventilation"},
            {"seq": 5, "material": "45×100mm Cedar Rafters @ 455mm O.C. w/ High-Density Wool", "thicknessMm": 100, "function": "Structure + Thermal"},
            {"seq": 6, "material": "Vapor Retarder Membrane", "thicknessMm": 1, "function": "Vapor Control"},
            {"seq": 7, "material": "12mm Exposed Birch Plywood Sloped Ceiling Lining", "thicknessMm": 12, "function": "Interior Finish"}
        ]
    },
    "FND-01": {
        "code": "FND-01",
        "title": "Reinforced Concrete Mat & Perimeter Stem Plinth (EL 0.00..+0.32m)",
        "totalThicknessMm": 320,
        "uValue": "0.42 W/m²·K (Perimeter XPS)",
        "fireRating": "2-Hr Non-Combustible RC",
        "layers": [
            {"seq": 1, "material": "150mm Compacted Crushed Gravel Capillary Break", "thicknessMm": 150, "function": "Drainage Sub-base"},
            {"seq": 2, "material": "0.15mm Polyethylene Vapor Barrier", "thicknessMm": 1, "function": "Damp-Proofing"},
            {"seq": 3, "material": "150mm RC Mat Slab (D13 @ 200mm O.C. Both Ways, 24 MPa)", "thicknessMm": 150, "function": "Foundation Slab"},
            {"seq": 4, "material": "160×320mm RC Perimeter Stem Wall + M12 Anchor Bolts @ 910mm", "thicknessMm": 320, "function": "Plinth / Uplift"},
            {"seq": 5, "material": "Anodized Aluminum Plinth Drip Flashing (EL +0.30..+0.325m)", "thicknessMm": 2, "function": "Termite & Drip Guard"}
        ]
    },
    "FL-1F-01": {
        "code": "FL-1F-01",
        "title": "1F Solid Pine Plank Floor over Insulated Timber Joists (EL +0.36m)",
        "totalThicknessMm": 180,
        "uValue": "0.38 W/m²·K",
        "fireRating": "Residential Timber",
        "layers": [
            {"seq": 1, "material": "18mm Japanese Red Pine (Akamatsu) Tongue-and-Groove Boards", "thicknessMm": 18, "function": "Wear Surface"},
            {"seq": 2, "material": "24mm Structural Plywood Subfloor", "thicknessMm": 24, "function": "Diaphragm"},
            {"seq": 3, "material": "105×105mm Pressure-Treated Hinoki Dodai Sill & Floor Joists", "thicknessMm": 105, "function": "Structure"},
            {"seq": 4, "material": "65mm Extruded Polystyrene (XPS) Rigid Under-Floor Insulation", "thicknessMm": 65, "function": "Thermal Barrier"}
        ]
    },
    "FL-2F-01": {
        "code": "FL-2F-01",
        "title": "2F L-Shaped Loft Mezzanine Timber Floor Assembly (160mm, EL +2.36..+2.52m)",
        "totalThicknessMm": 160,
        "uValue": "Interior Assembly",
        "fireRating": "Heavy Timber",
        "layers": [
            {"seq": 1, "material": "18mm Solid Pine Loft Flooring", "thicknessMm": 18, "function": "Wear Surface"},
            {"seq": 2, "material": "18mm Structural Plywood Subfloor", "thicknessMm": 18, "function": "Diaphragm"},
            {"seq": 3, "material": "45×96mm Timber Joists @ 455mm O.C. hung to 180×205mm Rim Beams", "thicknessMm": 96, "function": "Structure"},
            {"seq": 4, "material": "28mm Exposed Birch Plywood Soffit & Concealed Wiring Chase", "thicknessMm": 28, "function": "1F Ceiling Finish"}
        ]
    },
    "GLZ-01": {
        "code": "GLZ-01",
        "title": "2-Story Front Aluminum Sliding Glazing & Inner Shoji Screen System",
        "totalThicknessMm": 220,
        "uValue": "1.90 W/m²·K (Double Low-E + Shoji)",
        "fireRating": "Tempered Safety Glass",
        "layers": [
            {"seq": 1, "material": "Anodized Silver Aluminum Thermal-Break Outer Frame & Track", "thicknessMm": 70, "function": "Structural Sash"},
            {"seq": 2, "material": "Low-E Double Insulating Glass Unit (5+12Ar+5mm)", "thicknessMm": 22, "function": "Thermal Glazing"},
            {"seq": 3, "material": "Sliding Cedar Shoji Lattice Frames w/ Translucent Washi Paper", "thicknessMm": 32, "function": "Daylight Diffusion"},
            {"seq": 4, "material": "Solid Japanese Cedar Interior Reveal Casing", "thicknessMm": 96, "function": "Architectural Trim"}
        ]
    },
    "DK-01": {
        "code": "DK-01",
        "title": "Exterior Cedar Engawa Deck on Precast Concrete Pier Blocks (EL +0.32m)",
        "totalThicknessMm": 320,
        "uValue": "Exterior",
        "fireRating": "Exterior Timber",
        "layers": [
            {"seq": 1, "material": "32×174mm Western Red Cedar Deck Planks (8mm Drainage Gap)", "thicknessMm": 60, "function": "Walking Surface"},
            {"seq": 2, "material": "50×90mm Cedar Ledger & Bearer Subframe w/ SS Screws", "thicknessMm": 50, "function": "Framing"},
            {"seq": 3, "material": "220×220×220mm Precast Concrete Kutsunugi Pier Blocks on Gravel", "thicknessMm": 220, "function": "Point Footings"}
        ]
    },
    "STR-01": {
        "code": "STR-01",
        "title": "Open-Riser Japanese Timber Stair (11 Treads, 180mm Rise / 183mm Run)",
        "totalThicknessMm": 220,
        "uValue": "Interior",
        "fireRating": "Residential Timber",
        "layers": [
            {"seq": 1, "material": "45×220mm Laminated Hardwood Twin Stringers", "thicknessMm": 45, "function": "Primary Load Path"},
            {"seq": 2, "material": "36×180×600mm Mortised Solid Hardwood Treads", "thicknessMm": 36, "function": "Tread"},
            {"seq": 3, "material": "Wall-Mounted Birch Plywood Continuous Handrail", "thicknessMm": 40, "function": "Guard / Grasp"}
        ]
    },
    "LGT-01": {
        "code": "LGT-01",
        "title": "Koizumi Studio Minimalist 2700K Architectural LED Luminaire",
        "totalThicknessMm": 50,
        "uValue": "2700K CRI 95+ LED",
        "fireRating": "UL / JIS Wet-Rated Where Applicable",
        "layers": [
            {"seq": 1, "material": "Spun Enamel / Extruded Aluminum Housing or Duct Rail", "thicknessMm": 25, "function": "Enclosure"},
            {"seq": 2, "material": "High-CRI 2700K Warm LED Engine w/ Opal Diffuser", "thicknessMm": 25, "function": "Optics / Illumination"}
        ]
    }
}

def classify_object(obj, root_name, bb_min, bb_max, mat_name):
    n = obj.name
    nl = n.lower()
    z_min, z_max = bb_min[2], bb_max[2]
    z_mid = 0.5 * (z_min + z_max)

    # 1. Building & Storey
    if root_name == "Context_Group":
        bldg = "CTX-01"
        storey = "L00"
    elif any(k in nl for k in ("site_", "deck_", "entrance_concrete", "outdoor_")):
        bldg = "SITE-01"
        storey = "L00"
    else:
        bldg = "BLDG-01"
        if root_name == "Roof_Group" or z_min >= 4.25:
            storey = "L03"
        elif z_min >= 2.34 or "loft_" in nl or "bed_" in nl:
            storey = "L02"
        elif z_max <= 0.34 or "foundation" in nl or "plinth" in nl:
            storey = "L00"
        else:
            storey = "L01"

    # 2. IFC4 Class, PredefinedType, CSI MasterFormat, Uniformat, Uniclass, Assembly, Spec
    assembly = None
    disc = "A"
    disc_name = "Architecture"

    if root_name == "Context_Group":
        if "kitty" in nl and "win" not in nl:
            return (bldg, storey, "IfcBuildingElementProxy", "USERDEFINED", "A", "Architecture",
                    "01 70 00", "Neighborhood Easter Egg (Tuxedo Kitty)", "Z10", "Pr_40_30", None,
                    "Asymmetrical tuxedo cat perched at rear neighbor 2F window — framed along sightline from 2F Bedroom sliding window W-02.")
        if any(k in nl for k in ("tree", "sakura", "shrub", "hedge", "leaf")):
            return (bldg, storey, "IfcGeographicElement", "VEGETATION", "L", "Landscape",
                    "32 90 00", "Planting & Specimen Sakura", "G2050", "Ss_45_40", None,
                    "Neighborhood vegetation including specimen Japanese Cherry Blossom (Sakura) flanking front engawa deck.")
        if any(k in nl for k in ("road", "asphalt", "paver", "curb", "manhole", "ground")):
            return (bldg, storey, "IfcGeographicElement", "TERRAIN", "C", "Civil",
                    "32 10 00", "Streets, Paving & Civil", "G2020", "Ss_30_10", None,
                    "Urban Japanese residential streetscape, asphalt carriageway, utility access, and site parcel grade.")
        if any(k in nl for k in ("pole", "power", "wire", "utility", "mirror")):
            return (bldg, storey, "IfcDistributionElement", "UTILITY", "C", "Civil",
                    "33 70 00", "Electrical & Street Utilities", "G4010", "Ss_70_10", None,
                    "Overhead neighborhood utility poles, drop lines, and street corner convex traffic mirror.")
        return (bldg, storey, "IfcBuildingElementProxy", "CONTEXT", "A", "Context",
                "01 10 00", "Adjacent Urban Context Massing", "G1010", "En_10_10", None,
                "Surrounding Tokyo/suburban Japanese residential context massing establishing setback & daylight envelope.")

    # House & Roof Elements
    if n.startswith("Fixture_"):
        return (bldg, storey, "IfcLightFixture", "POINTSOURCE", "E", "Electrical / Lighting",
                "26 51 00", "Interior & Exterior Architectural Lighting", "D5020", "Pr_70_70_48", "LGT-01",
                "Modeled Koizumi Studio minimalist 2700K architectural luminaire with calibrated warm emission (see Sheet A-104 & A-601).")

    if "foundation" in nl or "deck_footing" in nl or "plinth_flashing" in nl or "entrance_concrete" in nl:
        return (bldg, "L00", "IfcFooting", "STRIP_FOOTING" if "foundation" in nl else "PAD_FOOTING", "S", "Structural",
                "03 30 00", "Cast-in-Place & Precast Concrete", "A1010", "Ss_20_05", "FND-01",
                "24 MPa reinforced concrete foundation plinth (EL 0.00..+0.32m) with aluminum drip flashing and precast concrete engawa pier blocks.")

    if "column" in nl:
        return (bldg, "L01", "IfcColumn", "COLUMN", "S", "Structural",
                "06 13 00", "Heavy Timber Structural Columns", "B1010", "Ss_20_10_30", "FL-2F-01",
                "Continuous Ø176mm turned Japanese cedar (Sugi) structural column spanning EL +0.36m to roof ridge EL +5.32m on 1820mm ken grid.")

    if "beam" in nl or "ridge" in nl:
        return (bldg, storey, "IfcBeam", "BEAM", "S", "Structural",
                "06 13 00", "Heavy Timber Girders & Ridge Beam", "B1010", "Ss_20_10_30", "RF-01" if "ridge" in nl else "FL-2F-01",
                "Primary structural timber girder (180×205mm loft fascia rim beam or 140×180mm ridge beam) transferring floor/roof loads to Ø176mm cedar columns.")

    if "house_roof" in nl or "gutter" in nl or "downspout" in nl:
        return (bldg, "L03", "IfcRoof", "GABLE_ROOF", "A", "Architecture",
                "07 41 13", "Standing-Seam Galvalume Metal Roofing", "B3010", "Ss_30_10_30", "RF-01",
                "Asymmetric gable Galvalume metal roof (South pitch 16.0° / North pitch 23.1°, ridge EL +5.46m) with aluminum eave gutter & downspout.")

    if "ceiling_" in nl or "loft_ceiling" in nl:
        return (bldg, storey, "IfcCovering", "CEILING", "A", "Architecture",
                "09 54 00", "Exposed Birch Plywood Ceilings", "C3030", "Ss_30_25", "RF-01" if "plywood_lining" in nl else "FL-2F-01",
                "12mm JAS birch/lauan structural plywood ceiling lining cleanly expressing the asymmetric roof pitch and mezzanine underside.")

    if "stair_" in nl:
        return (bldg, "L01", "IfcStairFlight", "STRAIGHT", "A", "Architecture",
                "06 43 00", "Architectural Wood Stairs & Handrail", "C2010", "Ss_35_10", "STR-01",
                "Open-riser timber stair flight (11 solid treads @ 180mm rise / 183mm run, twin 45×220mm laminated stringers, wall-mounted plywood handrail).")

    if "loft_rail" in nl or "loft_cable" in nl:
        return (bldg, "L02", "IfcRailing", "GUARDRAIL", "A", "Architecture",
                "05 52 00", "Metal & Stainless Cable Guardrails", "C2010", "Ss_25_60", "FL-2F-01",
                "760mm loft safety guardrail with 36×36mm white steel posts/top rail and 3 tensioned Ø8mm stainless wire cables @ 190mm spacing.")

    if any(k in nl for k in ("winframe", "winreveal", "sash_", "bed_slidingwin", "smallwin", "rearwin", "sidewin", "wc_window", "jimado")):
        return (bldg, storey, "IfcWindow", "WINDOW", "A", "Architecture",
                "08 51 13", "Aluminum Windows & Sliding Shoji", "B2020", "Ss_25_30_95", "GLZ-01",
                "Anodized aluminum thermal-break sliding window / 2-story shoji curtain assembly with solid cedar interior reveal casing.")

    if any(k in nl for k in ("entrance_door", "bath_entry_door", "wc_door", "shower_glass_door", "canopy")):
        return (bldg, storey, "IfcDoor", "DOOR", "A", "Architecture",
                "08 11 00", "Exterior & Interior Doors / Entry Canopy", "B2030", "Ss_25_30_20", "W-EXT-01" if "entrance" in nl else "W-INT-01",
                "Architectural exterior insulated metal entry door under cantilevered aluminum canopy, or interior birch plywood / frameless glass door.")

    if any(k in nl for k in ("wall_", "plywall", "seam_")) and not any(k in nl for k in ("cabinet", "counter", "mirror", "tile", "handrail", "mailbox", "intercom", "vent")):
        is_ext = not any(k in nl for k in ("bath_wall", "wc_wall", "shower_wall"))
        return (bldg, storey, "IfcWall", "STANDARD", "A", "Architecture",
                "07 42 13" if is_ext else "09 21 16",
                "Exterior Insulated Galvalume Wall" if is_ext else "Interior Partition Wall",
                "B2010" if is_ext else "C1010", "Ss_25_10",
                "W-EXT-01" if is_ext else "W-INT-01",
                "160mm exterior timber-frame Galvalume rainscreen wall with 12mm birch interior lining (Assembly W-EXT-01)." if is_ext else "75mm interior framed partition wall (Assembly W-INT-01).")

    if any(k in nl for k in ("interior_floor", "interior_loft_rear", "interior_loft_right", "deck_plank", "deck_subframe", "genkan_mortar", "genkan_wood", "site_")):
        if "deck_" in nl:
            return (bldg, "L00", "IfcSlab", "LANDING", "A", "Architecture",
                    "06 15 00", "Exterior Cedar Engawa Decking", "G2030", "Ss_30_20", "DK-01",
                    "Western Red Cedar engawa deck (24 spaced planks 32×174mm on cedar subframe & precast concrete piers, EL +0.32m).")
        if "loft" in nl:
            return (bldg, "L02", "IfcSlab", "FLOOR", "S", "Structural",
                    "06 16 00", "2F Loft Mezzanine Timber Floor", "B1010", "Ss_30_20", "FL-2F-01",
                    "L-shaped 2F timber mezzanine floor assembly (EL +2.40..+2.52m, solid pine finish over plywood diaphragm & joists).")
        if "site_" in nl:
            return (bldg, "L00", "IfcSlab", "BASESLAB", "C", "Civil",
                    "32 14 00", "Site Concrete Pavers & Gravel Apron", "G2030", "Ss_30_10", "FND-01",
                    "Exterior concrete entry pavers and crushed gravel perimeter drainage apron.")
        return (bldg, "L01", "IfcSlab", "FLOOR", "A", "Architecture",
                "09 64 00", "1F Solid Pine Flooring & Genkan Mortar", "C3020", "Ss_30_20", "FL-1F-01",
                "1F solid Japanese red pine flooring (EL +0.36m) with troweled mortar genkan entry apron and timber curb.")

    if "tatami" in nl and not any(k in nl for k in ("storage", "closet", "prop", "jimado")):
        return (bldg, "L01", "IfcCovering", "FLOORING", "A", "Architecture",
                "09 68 00", "Raised 6-Mat Tatami Platform", "C3020", "Ss_30_40", "FL-1F-01",
                "Raised timber platform (+160mm above 1F FFL, EL +0.52m) fitted with 6 traditional igusa-straw tatami mats with woven heri borders.")

    if "shower_floor" in nl or "shower_walltile" in nl or "shower_door_curb" in nl:
        return (bldg, "L01", "IfcCovering", "FLOORING" if "floor" in nl else "CLADDING", "A", "Architecture",
                "09 30 00", "Wet-Room Ceramic Tile & Waterproofing", "C3020", "Ss_30_42", "W-INT-01",
                "Waterproofed Japanese wet-room bath enclosure finished in modular 240×190mm porcelain floor & wall tile.")

    if any(k in nl for k in ("wc_toilet", "vanity_washbasin", "vanity_faucet", "shower_rain", "shower_mixer", "shower_riser", "shower_top", "shower_handheld", "shower_floor_drain", "kitchen_sink", "kitchen_faucet", "outdoor_standpipe", "outdoor_drain")):
        return (bldg, storey, "IfcSanitaryTerminal", "SANITARY", "P", "Plumbing",
                "22 40 00", "Plumbing Fixtures & Wet-Room Trim", "D2010", "Pr_40_20", None,
                "Architectural chrome plumbing fixture, porcelain sanitary ware, or exterior utility standpipe/drain.")

    if any(k in nl for k in ("fridge", "oven", "stove", "ricecooker", "kettle", "laptop", "monitor")):
        return (bldg, storey, "IfcElectricAppliance", "APPLIANCE", "E", "Equipment",
                "11 30 00", "Residential Kitchen Appliances", "E1090", "Pr_40_70", None,
                "Built-in or countertop residential appliance (induction cooktop, under-counter oven, refrigerator, small electronics).")

    if any(k in nl for k in ("counter", "cab", "storage", "closet", "vanity_", "peninsula", "dresser")):
        return (bldg, storey, "IfcFurniture", "CASEWORK", "A", "Interiors / Millwork",
                "06 41 00", "Custom Birch Plywood Millwork", "C1030", "Pr_40_30_30", None,
                "Koizumi-designed bespoke birch plywood built-in cabinetry, kitchen peninsula, vanity, or storage wall with recessed finger pulls.")

    if any(k in nl for k in ("mailbox", "intercom", "vent")):
        return (bldg, "L01", "IfcBuildingElementProxy", "ACCESSORY", "A", "Architecture",
                "10 55 00", "Exterior Entry Specialties & Vents", "B2010", "Pr_40_10", None,
                "Exterior architectural mailbox, intercom terminal, or intake/exhaust wall louver.")

    return (bldg, storey, "IfcFurnishingElement", "FURNITURE", "A", "Interiors / FF&E",
            "12 50 00", "Furniture, Loose Fixtures & Props", "E2020", "Pr_40_50", None,
            "Minimalist Japanese residential furniture & interior appointments (dining table, chairs, loft bed, hinoki bath stool, props).")

def calc_mesh_quantities(obj):
    me = obj.data
    bm = bmesh.new()
    bm.from_mesh(me)
    bm.transform(obj.matrix_world)
    area = sum(f.calc_area() for f in bm.faces)
    vol = abs(bm.calc_volume())
    verts = len(bm.verts)
    tris = sum(max(0, len(f.verts) - 2) for f in bm.faces)
    xs = [v.co.x for v in bm.verts]
    ys = [v.co.y for v in bm.verts]
    zs = [v.co.z for v in bm.verts]
    bm.free()
    if not xs:
        return [0,0,0], [0,0,0], [0,0,0], 0.0, 0.0, 0, 0
    bmin = [round(min(xs), 4), round(min(ys), 4), round(min(zs), 4)]
    bmax = [round(max(xs), 4), round(max(ys), 4), round(max(zs), 4)]
    dims = [round(bmax[i] - bmin[i], 4) for i in range(3)]
    return bmin, bmax, dims, round(area, 4), round(vol, 5), verts, tris

def main():
    elements = []
    totals = {"meshes": 0, "houseRoofTris": 0, "contextTris": 0, "totalTris": 0, "totalAreaM2": 0.0, "totalVolumeM3": 0.0}

    for obj in sorted(bpy.data.objects, key=lambda o: o.name):
        if obj.type != "MESH" or not obj.data:
            continue
        root = obj
        while root.parent:
            root = root.parent
        root_name = root.name

        bmin, bmax, dims, area, vol, verts, tris = calc_mesh_quantities(obj)
        mat_name = obj.data.materials[0].name if (obj.data.materials and obj.data.materials[0]) else "Unassigned"
        bldg, storey, ifc_cls, predef, disc, disc_name, csi_code, csi_title, uniformat, uniclass, asm_code, notes = classify_object(
            obj, root_name, bmin, bmax, mat_name
        )

        rec = {
            "name": obj.name,
            "globalId": make_ifc_guid(obj.name),
            "isoContainer": ISO_CONTAINER,
            "parentGroup": root_name,
            "buildingId": bldg,
            "storeyId": storey,
            "discipline": disc,
            "disciplineName": disc_name,
            "ifcClass": ifc_cls,
            "predefinedType": predef,
            "csiCode": csi_code,
            "csiTitle": csi_title,
            "uniformat": uniformat,
            "uniclass": uniclass,
            "material": mat_name,
            "assemblyCode": asm_code,
            "bboxMin": bmin,
            "bboxMax": bmax,
            "dimensions": dims,
            "areaM2": area,
            "areaSqFt": round(area * 10.76391, 2),
            "volumeM3": vol,
            "volumeCuFt": round(vol * 35.31467, 2),
            "vertices": verts,
            "triangles": tris,
            "specNotes": notes,
        }
        elements.append(rec)
        totals["meshes"] += 1
        totals["totalTris"] += tris
        if root_name in ("House_Group", "Roof_Group"):
            totals["houseRoofTris"] += tris
        else:
            totals["contextTris"] += tris
        totals["totalAreaM2"] += area
        totals["totalVolumeM3"] += vol

    totals["totalAreaM2"] = round(totals["totalAreaM2"], 2)
    totals["totalVolumeM3"] = round(totals["totalVolumeM3"], 3)

    # Extract fixture coordinates directly from modeled Fixture_* objects for RCP & Lighting Schedule
    fixtures_summary = []
    for rec in elements:
        if rec["name"].startswith("Fixture_"):
            cx = round(0.5 * (rec["bboxMin"][0] + rec["bboxMax"][0]), 3)
            cy = round(0.5 * (rec["bboxMin"][1] + rec["bboxMax"][1]), 3)
            cz = round(0.5 * (rec["bboxMin"][2] + rec["bboxMax"][2]), 3)
            fixtures_summary.append({
                "name": rec["name"],
                "storeyId": rec["storeyId"],
                "center": [cx, cy, cz],
                "material": rec["material"],
            })

    payload = {
        "schema": "IFC4 ADD2 TC1",
        "standard": "ISO 19650-2",
        "containerId": ISO_CONTAINER,
        "suitability": "S4",
        "revision": "P05.0",
        "project": {
            "name": "9-Tsubo House (Sumire Aoi House)",
            "architect": "Makoto Koizumi / Koizumi Studio (1999)",
            "prototypeOrigin": "Makoto Masuzawa Minimum House (1952)",
            "footprintKen": "3.0 ken × 3.0 ken (5,460mm × 5,460mm = 9 Tsubo = 29.81 m²)",
            "repository": "https://github.com/spinorama/9TsuboV2",
            "performanceCapTris": 60000,
        },
        "datums": {
            "GL": 0.000,
            "PLINTH_TOP": 0.320,
            "FFL_1F": 0.360,
            "TATAMI_TOP": 0.520,
            "LOFT_SOFFIT": 2.360,
            "FFL_2F": 2.520,
            "EAVE_NORTH": 4.308,
            "EAVE_SOUTH": 4.568,
            "RIDGE_TOP": 5.460,
        },
        "totals": totals,
        "assemblies": ASSEMBLIES,
        "fixtures": fixtures_summary,
        "elements": elements,
    }

    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    print(f"Exported BIM metadata: {OUT_JSON}")
    print(f"Totals: {totals}")

if __name__ == "__main__":
    main()
