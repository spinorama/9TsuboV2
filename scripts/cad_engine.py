"""
9-Tsubo House — BIMCraft-Style 3D-to-2D CAD Projection, Slicing & Vector SVG Drafting Engine
Runs inside Blender 5.2 LTS (bpy, bmesh, mathutils).
Produces ARCH D / ISO A1 (1920x1280) monochrome + technical-accent vector architectural sheets
genuinely derived from the 3D Blender BIM model (slice + hidden-face orthographic projection)
augmented with parametric LOD-400 construction assembly detailing.
"""
import bpy
import bmesh
import math
from xml.sax.saxutils import escape
from mathutils import Vector

# =========================================================================
# 1. SVG SHEET FRAMEWORK & ARCHITECTURAL CAD HATCH PATTERNS
# =========================================================================
SVG_DEFS = """  <defs>
    <!-- Exterior Wall Cut Poché (Dense 45° Timber/Insulated Wall) -->
    <pattern id="hatch-wall-cut" width="6" height="6" patternTransform="rotate(45 0 0)" patternUnits="userSpaceOnUse">
      <rect width="6" height="6" fill="#e2e8f0"/>
      <line x1="0" y1="0" x2="0" y2="6" stroke="#1e293b" stroke-width="1.35"/>
    </pattern>
    <!-- Interior Partition Cut Poché (Lighter 45°) -->
    <pattern id="hatch-part-cut" width="8" height="8" patternTransform="rotate(-45 0 0)" patternUnits="userSpaceOnUse">
      <rect width="8" height="8" fill="#f1f5f9"/>
      <line x1="0" y1="0" x2="0" y2="8" stroke="#475569" stroke-width="0.95"/>
    </pattern>
    <!-- Reinforced Concrete Stipple + Aggregate Triangles -->
    <pattern id="hatch-concrete" width="22" height="22" patternUnits="userSpaceOnUse">
      <rect width="22" height="22" fill="#e5e7eb"/>
      <polygon points="4,5 8,4 6,8" fill="none" stroke="#334155" stroke-width="0.75"/>
      <polygon points="15,14 19,15 16,19" fill="none" stroke="#334155" stroke-width="0.75"/>
      <polygon points="5,18 9,16 8,20" fill="#64748b"/>
      <circle cx="14" cy="6" r="0.85" fill="#334155"/>
      <circle cx="19" cy="9" r="0.65" fill="#475569"/>
      <circle cx="9" cy="12" r="0.7" fill="#334155"/>
      <circle cx="2" cy="13" r="0.6" fill="#475569"/>
    </pattern>
    <!-- Undisturbed Earth / Grade Hatch (Standard ANSI/JIS Triple Diagonal) -->
    <pattern id="hatch-earth" width="24" height="24" patternUnits="userSpaceOnUse">
      <rect width="24" height="24" fill="#f5f3ee"/>
      <line x1="0" y1="8" x2="8" y2="0" stroke="#64748b" stroke-width="0.75"/>
      <line x1="0" y1="13" x2="13" y2="0" stroke="#64748b" stroke-width="0.75"/>
      <line x1="0" y1="18" x2="18" y2="0" stroke="#64748b" stroke-width="0.75"/>
      <line x1="12" y1="12" x2="20" y2="20" stroke="#64748b" stroke-width="0.75"/>
      <line x1="15" y1="9" x2="23" y2="17" stroke="#64748b" stroke-width="0.75"/>
      <line x1="9" y1="15" x2="17" y2="23" stroke="#64748b" stroke-width="0.75"/>
    </pattern>
    <!-- Crushed Gravel Capillary Drainage Sub-Base -->
    <pattern id="hatch-gravel" width="18" height="14" patternUnits="userSpaceOnUse">
      <rect width="18" height="14" fill="#eef0f2"/>
      <ellipse cx="4" cy="4" rx="2.4" ry="1.5" fill="none" stroke="#475569" stroke-width="0.75"/>
      <ellipse cx="12" cy="5" rx="2.8" ry="1.7" fill="none" stroke="#475569" stroke-width="0.75"/>
      <ellipse cx="8" cy="10" rx="2.5" ry="1.6" fill="none" stroke="#475569" stroke-width="0.75"/>
      <ellipse cx="15" cy="11" rx="2.0" ry="1.3" fill="none" stroke="#475569" stroke-width="0.75"/>
    </pattern>
    <!-- Rigid XPS Foam Insulation Cross-Hatch -->
    <pattern id="hatch-xps" width="10" height="10" patternUnits="userSpaceOnUse">
      <rect width="10" height="10" fill="#fefce8"/>
      <line x1="0" y1="0" x2="10" y2="10" stroke="#92400e" stroke-width="0.65"/>
      <line x1="10" y1="0" x2="0" y2="10" stroke="#92400e" stroke-width="0.65"/>
    </pattern>
    <!-- Steel / Metal Cross-Section Hatch -->
    <pattern id="hatch-steel" width="8" height="8" patternTransform="rotate(45 0 0)" patternUnits="userSpaceOnUse">
      <rect width="8" height="8" fill="#cbd5e1"/>
      <line x1="0" y1="0" x2="0" y2="8" stroke="#0f172a" stroke-width="1.0"/>
      <line x1="2.5" y1="0" x2="2.5" y2="8" stroke="#0f172a" stroke-width="0.6"/>
    </pattern>
    <!-- Plywood Multi-Ply Laminate -->
    <pattern id="hatch-plywood" width="12" height="6" patternUnits="userSpaceOnUse">
      <rect width="12" height="6" fill="#f7efe2"/>
      <line x1="0" y1="2" x2="12" y2="2" stroke="#78350f" stroke-width="0.5"/>
      <line x1="0" y1="4.5" x2="12" y2="4.5" stroke="#78350f" stroke-width="0.5"/>
      <line x1="3" y1="2" x2="5" y2="4.5" stroke="#92400e" stroke-width="0.45"/>
      <line x1="9" y1="2" x2="11" y2="4.5" stroke="#92400e" stroke-width="0.45"/>
    </pattern>
    <!-- Timber Grain (Longitudinal) -->
    <pattern id="hatch-wood" width="16" height="8" patternUnits="userSpaceOnUse">
      <rect width="16" height="8" fill="#f6ead8"/>
      <path d="M 0 2 Q 8 1 16 2 M 0 6 Q 8 7 16 6" fill="none" stroke="#92400e" stroke-width="0.55" stroke-opacity="0.55"/>
    </pattern>
    <!-- Tatami Igusa Rush Fine Weave -->
    <pattern id="hatch-tatami" width="6" height="6" patternUnits="userSpaceOnUse">
      <rect width="6" height="6" fill="#f4f1df"/>
      <line x1="0" y1="3" x2="6" y2="3" stroke="#a39e7a" stroke-width="0.5"/>
    </pattern>
    <!-- Ceramic Tile Grid -->
    <pattern id="hatch-tile" width="10" height="10" patternUnits="userSpaceOnUse">
      <rect width="10" height="10" fill="#f8fafc"/>
      <path d="M 10 0 L 0 0 0 10" fill="none" stroke="#94a3b8" stroke-width="0.55"/>
    </pattern>
    <!-- Subtle Background Drafting Grid -->
    <pattern id="draft-grid" width="40" height="40" patternUnits="userSpaceOnUse">
      <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#ebe9e1" stroke-width="0.55"/>
    </pattern>
    <!-- Arrowhead Markers -->
    <marker id="arr-dark" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 9 5 L 0 8.5 z" fill="#0f172a"/>
    </marker>
    <marker id="arr-blue" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 9 5 L 0 8.5 z" fill="#1d4ed8"/>
    </marker>
    <marker id="dot-dark" viewBox="0 0 8 8" refX="4" refY="4" markerWidth="5" markerHeight="5">
      <circle cx="4" cy="4" r="2.6" fill="#0f172a"/>
    </marker>
    <style>
      text { font-family: 'Bahnschrift', 'DIN Alternate', 'Roboto Condensed', 'Consolas', sans-serif; fill: #0f172a; }
      .mono { font-family: 'JetBrains Mono', 'Consolas', 'Courier New', monospace; }
      .tb-brand { font-size: 15px; font-weight: 800; fill: #f8fafc; letter-spacing: 1.8px; }
      .tb-sub { font-size: 9.5px; font-weight: 600; fill: #cbd5e1; letter-spacing: 0.9px; }
      .tb-hdr { font-size: 10.5px; font-weight: 700; fill: #0f172a; letter-spacing: 0.9px; }
      .tb-lbl { font-size: 8.5px; font-weight: 700; fill: #64748b; letter-spacing: 0.7px; }
      .tb-val { font-size: 11px; font-weight: 700; fill: #0f172a; }
      .sheet-num { font-size: 36px; font-weight: 800; fill: #0f172a; letter-spacing: 1.5px; }
      .vp-title { font-size: 13.5px; font-weight: 800; fill: #0f172a; letter-spacing: 0.8px; }
      .vp-scale { font-size: 10px; font-weight: 700; fill: #475569; letter-spacing: 0.5px; }
      .dim-txt { font-size: 9.5px; font-weight: 700; fill: #0f172a; text-anchor: middle; }
      .dim-sub { font-size: 8px; font-weight: 600; fill: #64748b; text-anchor: middle; }
      .grid-txt { font-size: 11px; font-weight: 800; fill: #0f172a; text-anchor: middle; }
      .room-num { font-size: 8.5px; font-weight: 700; fill: #475569; text-anchor: middle; }
      .room-name { font-size: 10px; font-weight: 800; fill: #0f172a; text-anchor: middle; letter-spacing: 0.4px; }
      .room-area { font-size: 8.5px; font-weight: 600; fill: #334155; text-anchor: middle; }
      .note-txt { font-size: 9.5px; font-weight: 600; fill: #1e293b; }
      .note-bold { font-size: 9.8px; font-weight: 800; fill: #0f172a; }
      .datum-txt { font-size: 9.2px; font-weight: 700; fill: #1d4ed8; }
      .tag-txt { font-size: 8.5px; font-weight: 800; fill: #0f172a; text-anchor: middle; }
    </style>
  </defs>"""


class SvgSheet:
    """ARCH D / ISO A1 Architectural Sheet (1920x1280) with DIN / ISO 19650 Title Block."""
    def __init__(self, sheet_id, sheet_title, scale_str, iso_code, discipline="ARCHITECTURE", total_sheets=12):
        self.sheet_id = sheet_id
        self.sheet_title = sheet_title
        self.scale_str = scale_str
        self.iso_code = iso_code
        self.discipline = discipline
        self.total_sheets = total_sheets
        self.body = []
        self.clip_counter = 0

    def add(self, svg_str):
        self.body.append(svg_str)

    def start_clip(self, x, y, w, h):
        self.clip_counter += 1
        cid = f"clip_{self.sheet_id.replace('-', '_')}_{self.clip_counter}"
        self.add(f'<clipPath id="{cid}"><rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}"/></clipPath>')
        self.add(f'<g clip-path="url(#{cid})">')
        return cid

    def end_clip(self):
        self.add('</g>')

    def viewport_title(self, x, y, num, title, scale_label, width=440):
        self.add(f'<g class="vp-header">')
        self.add(f'  <circle cx="{x + 15:.1f}" cy="{y:.1f}" r="14" fill="#0f172a"/>')
        self.add(f'  <text x="{x + 15:.1f}" y="{y + 4.5:.1f}" text-anchor="middle" style="font-size:12px;font-weight:800;fill:#ffffff;">{escape(str(num))}</text>')
        self.add(f'  <text x="{x + 37:.1f}" y="{y - 2:.1f}" class="vp-title">{escape(title.upper())}</text>')
        self.add(f'  <text x="{x + 37:.1f}" y="{y + 12:.1f}" class="vp-scale">SCALE {escape(scale_label)}</text>')
        self.add(f'  <line x1="{x + 30:.1f}" y1="{y + 1.5:.1f}" x2="{x + width:.1f}" y2="{y + 1.5:.1f}" stroke="#0f172a" stroke-width="1.6"/>')
        self.add(f'</g>')

    def scale_bar(self, x, y, px_per_m, meters_list=(0, 1, 2, 3, 5)):
        self.add(f'<g class="scale-bar">')
        max_m = meters_list[-1]
        bar_h = 6
        for i in range(len(meters_list) - 1):
            x0 = x + meters_list[i] * px_per_m
            x1 = x + meters_list[i + 1] * px_per_m
            fill = "#0f172a" if i % 2 == 0 else "#ffffff"
            self.add(f'  <rect x="{x0:.1f}" y="{y:.1f}" width="{x1 - x0:.1f}" height="{bar_h}" fill="{fill}" stroke="#0f172a" stroke-width="0.9"/>')
        for m in meters_list:
            xm = x + m * px_per_m
            lbl = f"{m}m" if m == max_m else f"{m}"
            self.add(f'  <text x="{xm:.1f}" y="{y - 3:.1f}" text-anchor="middle" style="font-size:8.5px;font-weight:700;fill:#334155;">{lbl}</text>')
        self.add(f'</g>')

    def grid_line_v(self, x, y_top, y_bot, label, top_bubble=True, bot_bubble=False):
        self.add(f'<line x1="{x:.1f}" y1="{y_top:.1f}" x2="{x:.1f}" y2="{y_bot:.1f}" stroke="#94a3b8" stroke-width="0.8" stroke-dasharray="14,4,2,4"/>')
        if top_bubble:
            cy = y_top - 15
            self.add(f'<circle cx="{x:.1f}" cy="{cy:.1f}" r="12" fill="#ffffff" stroke="#0f172a" stroke-width="1.4"/>')
            self.add(f'<text x="{x:.1f}" y="{cy + 4:.1f}" class="grid-txt">{escape(label)}</text>')
        if bot_bubble:
            cy = y_bot + 15
            self.add(f'<circle cx="{x:.1f}" cy="{cy:.1f}" r="12" fill="#ffffff" stroke="#0f172a" stroke-width="1.4"/>')
            self.add(f'<text x="{x:.1f}" y="{cy + 4:.1f}" class="grid-txt">{escape(label)}</text>')

    def grid_line_h(self, y, x_left, x_right, label, left_bubble=True, right_bubble=False):
        self.add(f'<line x1="{x_left:.1f}" y1="{y:.1f}" x2="{x_right:.1f}" y2="{y:.1f}" stroke="#94a3b8" stroke-width="0.8" stroke-dasharray="14,4,2,4"/>')
        if left_bubble:
            cx = x_left - 15
            self.add(f'<circle cx="{cx:.1f}" cy="{y:.1f}" r="12" fill="#ffffff" stroke="#0f172a" stroke-width="1.4"/>')
            self.add(f'<text x="{cx:.1f}" y="{y + 4:.1f}" class="grid-txt">{escape(label)}</text>')
        if right_bubble:
            cx = x_right + 15
            self.add(f'<circle cx="{cx:.1f}" cy="{y:.1f}" r="12" fill="#ffffff" stroke="#0f172a" stroke-width="1.4"/>')
            self.add(f'<text x="{cx:.1f}" y="{y + 4:.1f}" class="grid-txt">{escape(label)}</text>')

    def dim_h(self, x1, x2, y, label, ext_y=None, color="#0f172a"):
        if abs(x2 - x1) < 2: return
        self.add('<g class="dim-h">')
        if ext_y is not None:
            dy = 5 if y > ext_y else -5
            self.add(f'  <line x1="{x1:.1f}" y1="{ext_y:.1f}" x2="{x1:.1f}" y2="{y + dy:.1f}" stroke="#64748b" stroke-width="0.65"/>')
            self.add(f'  <line x1="{x2:.1f}" y1="{ext_y:.1f}" x2="{x2:.1f}" y2="{y + dy:.1f}" stroke="#64748b" stroke-width="0.65"/>')
        self.add(f'  <line x1="{x1 - 4:.1f}" y1="{y:.1f}" x2="{x2 + 4:.1f}" y2="{y:.1f}" stroke="{color}" stroke-width="0.9"/>')
        # 45° architectural slashes
        for xp in (x1, x2):
            self.add(f'  <line x1="{xp - 4:.1f}" y1="{y + 4:.1f}" x2="{xp + 4:.1f}" y2="{y - 4:.1f}" stroke="{color}" stroke-width="1.6"/>')
        xm = 0.5 * (x1 + x2)
        tw = max(32, len(label) * 5.8 + 8)
        self.add(f'  <rect x="{xm - tw/2:.1f}" y="{y - 12.5:.1f}" width="{tw:.1f}" height="11" fill="#fdfcf8" fill-opacity="0.92"/>')
        self.add(f'  <text x="{xm:.1f}" y="{y - 3.5:.1f}" class="dim-txt" style="fill:{color};">{escape(label)}</text>')
        self.add('</g>')

    def dim_v(self, x, y1, y2, label, ext_x=None, color="#0f172a"):
        if abs(y2 - y1) < 2: return
        self.add('<g class="dim-v">')
        if ext_x is not None:
            dx = 5 if x > ext_x else -5
            self.add(f'  <line x1="{ext_x:.1f}" y1="{y1:.1f}" x2="{x + dx:.1f}" y2="{y1:.1f}" stroke="#64748b" stroke-width="0.65"/>')
            self.add(f'  <line x1="{ext_x:.1f}" y1="{y2:.1f}" x2="{x + dx:.1f}" y2="{y2:.1f}" stroke="#64748b" stroke-width="0.65"/>')
        self.add(f'  <line x1="{x:.1f}" y1="{y1 - 4:.1f}" x2="{x:.1f}" y2="{y2 + 4:.1f}" stroke="{color}" stroke-width="0.9"/>')
        for yp in (y1, y2):
            self.add(f'  <line x1="{x - 4:.1f}" y1="{yp + 4:.1f}" x2="{x + 4:.1f}" y2="{yp - 4:.1f}" stroke="{color}" stroke-width="1.6"/>')
        ym = 0.5 * (y1 + y2)
        tw = max(32, len(label) * 5.8 + 8)
        self.add(f'  <g transform="translate({x - 4:.1f},{ym:.1f}) rotate(-90)">')
        self.add(f'    <rect x="{-tw/2:.1f}" y="-10" width="{tw:.1f}" height="11" fill="#fdfcf8" fill-opacity="0.92"/>')
        self.add(f'    <text x="0" y="-1" class="dim-txt" style="fill:{color};">{escape(label)}</text>')
        self.add('  </g>')
        self.add('</g>')

    def datum_level(self, x_line_start, x_line_end, y, code, elev_text, label_side="right"):
        self.add('<g class="datum">')
        self.add(f'  <line x1="{x_line_start:.1f}" y1="{y:.1f}" x2="{x_line_end:.1f}" y2="{y:.1f}" stroke="#1d4ed8" stroke-width="0.75" stroke-dasharray="10,4,2,4"/>')
        cx = x_line_end + 10 if label_side == "right" else x_line_start - 10
        r = 6.5
        self.add(f'  <circle cx="{cx:.1f}" cy="{y:.1f}" r="{r}" fill="#ffffff" stroke="#1d4ed8" stroke-width="1.1"/>')
        self.add(f'  <path d="M {cx:.1f} {y - r:.1f} A {r} {r} 0 0 1 {cx + r:.1f} {y:.1f} L {cx:.1f} {y:.1f} Z" fill="#1d4ed8"/>')
        self.add(f'  <path d="M {cx:.1f} {y + r:.1f} A {r} {r} 0 0 1 {cx - r:.1f} {y:.1f} L {cx:.1f} {y:.1f} Z" fill="#1d4ed8"/>')
        if label_side == "right":
            tx = cx + 11
            self.add(f'  <text x="{tx:.1f}" y="{y - 2:.1f}" class="datum-txt">{escape(code)}</text>')
            self.add(f'  <text x="{tx:.1f}" y="{y + 9:.1f}" style="font-size:8.5px;font-weight:700;fill:#334155;">{escape(elev_text)}</text>')
        else:
            tx = cx - 11
            self.add(f'  <text x="{tx:.1f}" y="{y - 2:.1f}" text-anchor="end" class="datum-txt">{escape(code)}</text>')
            self.add(f'  <text x="{tx:.1f}" y="{y + 9:.1f}" text-anchor="end" style="font-size:8.5px;font-weight:700;fill:#334155;">{escape(elev_text)}</text>')
        self.add('</g>')

    def section_cut_line(self, x1, y1, x2, y2, sec_letter, sheet_ref, look="up"):
        self.add('<g class="section-flag">')
        self.add(f'  <line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#1d4ed8" stroke-width="1.6" stroke-dasharray="16,5,3,5"/>')
        for (px, py) in ((x1, y1), (x2, y2)):
            # Pointer triangle indicating viewing direction
            if look == "up":
                pts = f"{px - 11:.1f},{py:.1f} {px + 11:.1f},{py:.1f} {px:.1f},{py - 19:.1f}"
            elif look == "down":
                pts = f"{px - 11:.1f},{py:.1f} {px + 11:.1f},{py:.1f} {px:.1f},{py + 19:.1f}"
            elif look == "right":
                pts = f"{px:.1f},{py - 11:.1f} {px:.1f},{py + 11:.1f} {px + 19:.1f},{py:.1f}"
            else:
                pts = f"{px:.1f},{py - 11:.1f} {px:.1f},{py + 11:.1f} {px - 19:.1f},{py:.1f}"
            self.add(f'  <polygon points="{pts}" fill="#1d4ed8"/>')
            self.add(f'  <circle cx="{px:.1f}" cy="{py:.1f}" r="12" fill="#ffffff" stroke="#1d4ed8" stroke-width="1.6"/>')
            self.add(f'  <line x1="{px - 12:.1f}" y1="{py:.1f}" x2="{px + 12:.1f}" y2="{py:.1f}" stroke="#1d4ed8" stroke-width="1.0"/>')
            self.add(f'  <text x="{px:.1f}" y="{py - 2.5:.1f}" text-anchor="middle" style="font-size:9px;font-weight:800;fill:#1d4ed8;">{escape(sec_letter)}</text>')
            self.add(f'  <text x="{px:.1f}" y="{py + 8.5:.1f}" text-anchor="middle" style="font-size:7.5px;font-weight:700;fill:#1d4ed8;">{escape(sheet_ref)}</text>')
        self.add('</g>')

    def detail_callout(self, cx, cy, r, det_num, sheet_ref, bx, by):
        self.add('<g class="detail-callout">')
        self.add(f'  <circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="none" stroke="#b91c1c" stroke-width="1.2" stroke-dasharray="5,3"/>')
        dx, dy = bx - cx, by - cy
        d = max(1.0, math.hypot(dx, dy))
        sx, sy = cx + dx / d * r, cy + dy / d * r
        ex, ey = bx - dx / d * 14, by - dy / d * 14
        self.add(f'  <line x1="{sx:.1f}" y1="{sy:.1f}" x2="{ex:.1f}" y2="{ey:.1f}" stroke="#b91c1c" stroke-width="1.1"/>')
        self.add(f'  <circle cx="{bx:.1f}" cy="{by:.1f}" r="14" fill="#ffffff" stroke="#b91c1c" stroke-width="1.5"/>')
        self.add(f'  <line x1="{bx - 14:.1f}" y1="{by:.1f}" x2="{bx + 14:.1f}" y2="{by:.1f}" stroke="#b91c1c" stroke-width="1.0"/>')
        self.add(f'  <text x="{bx:.1f}" y="{by - 3:.1f}" text-anchor="middle" style="font-size:9.5px;font-weight:800;fill:#b91c1c;">{escape(str(det_num))}</text>')
        self.add(f'  <text x="{bx:.1f}" y="{by + 9.5:.1f}" text-anchor="middle" style="font-size:7.8px;font-weight:700;fill:#b91c1c;">{escape(sheet_ref)}</text>')
        self.add('</g>')

    def room_tag(self, x, y, num, name, area_str):
        w = max(86, max(len(name), len(area_str)) * 5.6 + 14)
        self.add(f'<g class="room-tag">')
        self.add(f'  <rect x="{x - w/2:.1f}" y="{y - 18:.1f}" width="{w:.1f}" height="34" fill="#fdfcf8" fill-opacity="0.93" stroke="#0f172a" stroke-width="0.9"/>')
        self.add(f'  <line x1="{x - w/2:.1f}" y1="{y - 6:.1f}" x2="{x + w/2:.1f}" y2="{y - 6:.1f}" stroke="#cbd5e1" stroke-width="0.6"/>')
        self.add(f'  <text x="{x:.1f}" y="{y - 9:.1f}" class="room-num">{escape(num)}</text>')
        self.add(f'  <text x="{x:.1f}" y="{y + 3.5:.1f}" class="room-name">{escape(name)}</text>')
        self.add(f'  <text x="{x:.1f}" y="{y + 13:.1f}" class="room-area">{escape(area_str)}</text>')
        self.add(f'</g>')

    def tag_badge(self, x, y, code, shape="hex", stroke="#0f172a"):
        self.add('<g class="tag-badge">')
        if shape == "hex":
            pts = f"{x-15:.1f},{y:.1f} {x-9:.1f},{y-8:.1f} {x+9:.1f},{y-8:.1f} {x+15:.1f},{y:.1f} {x+9:.1f},{y+8:.1f} {x-9:.1f},{y+8:.1f}"
            self.add(f'  <polygon points="{pts}" fill="#ffffff" stroke="{stroke}" stroke-width="1.1"/>')
        elif shape == "pill":
            self.add(f'  <rect x="{x-15:.1f}" y="{y-8:.1f}" width="30" height="16" rx="8" fill="#ffffff" stroke="{stroke}" stroke-width="1.1"/>')
        else:
            self.add(f'  <rect x="{x-16:.1f}" y="{y-8:.1f}" width="32" height="16" fill="#ffffff" stroke="{stroke}" stroke-width="1.1"/>')
        self.add(f'  <text x="{x:.1f}" y="{y + 3:.1f}" class="tag-txt" style="fill:{stroke};">{escape(code)}</text>')
        self.add('</g>')

    def leader_note(self, px, py, tx, ty, lines, align="auto", color="#0f172a"):
        if isinstance(lines, str):
            lines = [lines]
        if align == "auto":
            align = "left" if tx >= px else "right"
        self.add('<g class="leader-note">')
        if align == "left":
            elbow_x = tx - 12
            text_x = tx + 4
            anchor = "start"
        else:
            elbow_x = tx + 12
            text_x = tx - 4
            anchor = "end"
        self.add(f'  <polyline points="{px:.1f},{py:.1f} {elbow_x:.1f},{ty:.1f} {tx:.1f},{ty:.1f}" fill="none" stroke="{color}" stroke-width="0.95" marker-start="url(#dot-dark)"/>')
        # Add subtle opaque vellum backing behind multi-line callout text so lines never clash with text
        max_chars = max(len(l) for l in lines)
        box_w = max_chars * 5.4 + 8
        box_h = len(lines) * 12 + 4
        bx = text_x - 3 if anchor == "start" else text_x - box_w + 3
        self.add(f'  <rect x="{bx:.1f}" y="{ty - 8:.1f}" width="{box_w:.1f}" height="{box_h:.1f}" fill="#fdfcf8" fill-opacity="0.88"/>')
        for idx, line in enumerate(lines):
            cls = "note-bold" if idx == 0 else "note-txt"
            self.add(f'  <text x="{text_x:.1f}" y="{ty + 3 + idx * 12:.1f}" text-anchor="{anchor}" class="{cls}">{escape(line)}</text>')
        self.add('</g>')

    def batt_insulation(self, x, y, w, h, vertical=True, cycles=None):
        """Draws true architectural sinusoidal/looped mineral-wool batt insulation inside (x,y,w,h)."""
        pts = []
        if vertical:
            if cycles is None:
                cycles = max(4, int(h / max(6.0, w * 0.55)))
            step = h / cycles
            x_l, x_r = x + 1.5, x + w - 1.5
            xm = 0.5 * (x_l + x_r)
            d = [f"M {xm:.1f} {y:.1f}"]
            for i in range(cycles):
                y0 = y + i * step
                y1 = y0 + step * 0.5
                y2 = y0 + step
                d.append(f"C {x_r:.1f} {y0:.1f}, {x_r:.1f} {y1:.1f}, {xm:.1f} {y1:.1f}")
                d.append(f"C {x_l:.1f} {y1:.1f}, {x_l:.1f} {y2:.1f}, {xm:.1f} {y2:.1f}")
            self.add(f'<path d="{" ".join(d)}" fill="none" stroke="#92400e" stroke-width="0.85" stroke-opacity="0.8"/>')
        else:
            if cycles is None:
                cycles = max(4, int(w / max(6.0, h * 0.55)))
            step = w / cycles
            y_t, y_b = y + 1.5, y + h - 1.5
            ym = 0.5 * (y_t + y_b)
            d = [f"M {x:.1f} {ym:.1f}"]
            for i in range(cycles):
                x0 = x + i * step
                x1 = x0 + step * 0.5
                x2 = x0 + step
                d.append(f"C {x0:.1f} {y_t:.1f}, {x1:.1f} {y_t:.1f}, {x1:.1f} {ym:.1f}")
                d.append(f"C {x1:.1f} {y_b:.1f}, {x2:.1f} {y_b:.1f}, {x2:.1f} {ym:.1f}")
            self.add(f'<path d="{" ".join(d)}" fill="none" stroke="#92400e" stroke-width="0.85" stroke-opacity="0.8"/>')

    def timber_section(self, x, y, w, h, stroke="#0f172a"):
        """Standard architectural cut-timber cross-section (rectangle with crisp internal X)."""
        self.add(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="#f6ead8" stroke="{stroke}" stroke-width="1.3"/>')
        self.add(f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{x+w:.1f}" y2="{y+h:.1f}" stroke="{stroke}" stroke-width="0.7"/>')
        self.add(f'<line x1="{x+w:.1f}" y1="{y:.1f}" x2="{x:.1f}" y2="{y+h:.1f}" stroke="{stroke}" stroke-width="0.7"/>')

    def _title_block(self):
        return f"""  <!-- RIGHT-HAND ISO 19650 / DIN / AIA ARCHITECTURAL TITLE BLOCK (x = 1620..1902) -->
  <g transform="translate(1620, 26)">
    <rect x="0" y="0" width="282" height="1228" fill="#fafaf7" stroke="#0f172a" stroke-width="1.8"/>
    <rect x="0" y="0" width="282" height="84" fill="#0f172a"/>
    <text x="141" y="28" text-anchor="middle" class="tb-brand">9-TSUBO HOUSE</text>
    <text x="141" y="47" text-anchor="middle" class="tb-sub">SUMIRE AOI HOUSE · MAKOTO KOIZUMI (1999)</text>
    <text x="141" y="65" text-anchor="middle" style="font-size:9px;font-weight:700;fill:#38bdf8;letter-spacing:1.1px;">MODEL-DERIVED BIM CONSTRUCTION SET</text>

    <!-- Project Identification -->
    <text x="12" y="102" class="tb-lbl">PROTOTYPE / ARCHITECTURAL SYSTEM</text>
    <text x="12" y="117" class="tb-val">3×3 KEN (5,460 × 5,460mm) · 9 TSUBO</text>
    <text x="12" y="132" style="font-size:9.5px;fill:#334155;">AFTER MASUZAWA MINIMUM HOUSE (1952)</text>
    <text x="12" y="150" class="tb-lbl">DIGITAL TWIN / REPOSITORY</text>
    <text x="12" y="164" class="mono" style="font-size:9.5px;font-weight:700;fill:#0f172a;">github.com/spinorama/9TsuboV2</text>
    <line x1="0" y1="176" x2="282" y2="176" stroke="#0f172a" stroke-width="1.2"/>

    <!-- ISO 19650 Information Container -->
    <rect x="0" y="176" width="282" height="22" fill="#e2e8f0" stroke="#0f172a" stroke-width="1.0"/>
    <text x="141" y="191" text-anchor="middle" class="tb-hdr">ISO 19650-2 / IFC4 BIM REGISTER</text>
    <text x="12" y="214" class="tb-lbl">INFORMATION CONTAINER ID</text>
    <text x="12" y="229" class="mono" style="font-size:11px;font-weight:800;fill:#1d4ed8;">{escape(self.iso_code)}</text>
    <text x="12" y="248" class="tb-lbl">SUITABILITY / REVISION</text>
    <text x="12" y="262" class="tb-val">S4 CONSTRUCTION · REV P05.0</text>
    <text x="12" y="282" class="tb-lbl">SCHEMA / LOD STRATEGY</text>
    <text x="12" y="296" class="tb-val">IFC4 ADD2 · 3D LOD300 / 2D LOD400</text>
    <text x="12" y="316" class="tb-lbl">DISCIPLINE</text>
    <text x="12" y="330" class="tb-val">{escape(self.discipline)}</text>
    <text x="150" y="316" class="tb-lbl">UNITS / DATUM</text>
    <text x="150" y="330" class="tb-val">mm / EL ±0.000 GL</text>
    <line x1="0" y1="344" x2="282" y2="344" stroke="#0f172a" stroke-width="1.2"/>

    <!-- Revision Schedule -->
    <rect x="0" y="344" width="282" height="22" fill="#e2e8f0" stroke="#0f172a" stroke-width="1.0"/>
    <text x="141" y="359" text-anchor="middle" class="tb-hdr">ISSUE &amp; REVISION LOG</text>
    <text x="10" y="378" class="tb-lbl">REV</text>
    <text x="52" y="378" class="tb-lbl">DATE</text>
    <text x="122" y="378" class="tb-lbl">DESCRIPTION</text>
    <line x1="0" y1="384" x2="282" y2="384" stroke="#94a3b8" stroke-width="0.8"/>
    <text x="10" y="399" style="font-size:9px;font-weight:700;">P01.0</text>
    <text x="52" y="399" style="font-size:9px;">2026-11-02</text>
    <text x="122" y="399" style="font-size:9px;">INITIAL 3D / WEBXR ISSUE</text>
    <text x="10" y="414" style="font-size:9px;font-weight:700;">P04.0</text>
    <text x="52" y="414" style="font-size:9px;">2026-11-08</text>
    <text x="122" y="414" style="font-size:9px;">TABLETOP AR &amp; HIDDEN LINE</text>
    <text x="10" y="429" style="font-size:9px;font-weight:700;">P04.5</text>
    <text x="52" y="429" style="font-size:9px;">2026-11-22</text>
    <text x="122" y="429" style="font-size:9px;">FIXTURES + APPLE USDZ AR</text>
    <rect x="2" y="435" width="278" height="17" fill="#eff6ff"/>
    <text x="10" y="447" style="font-size:9px;font-weight:800;fill:#1d4ed8;">P05.0</text>
    <text x="52" y="447" style="font-size:9px;font-weight:700;fill:#1d4ed8;">2026-11-22</text>
    <text x="122" y="447" style="font-size:9px;font-weight:800;fill:#1d4ed8;">FULL BIM CD SET (12 SHEETS)</text>
    <line x1="0" y1="456" x2="282" y2="456" stroke="#0f172a" stroke-width="1.2"/>

    <!-- Modular 9-Tsubo Key Plan Diagram -->
    <text x="141" y="474" text-anchor="middle" class="tb-lbl">KEY PLAN · 3×3 KEN STRUCTURAL MODULE</text>
    <g transform="translate(46, 486)">
      <rect x="0" y="0" width="190" height="150" fill="#f8fafc" stroke="#0f172a" stroke-width="1.0"/>
      <!-- Road at South (bottom) -->
      <rect x="0" y="122" width="190" height="28" fill="#e2e8f0"/>
      <text x="95" y="139" text-anchor="middle" style="font-size:8px;font-weight:700;fill:#475569;">SOUTH STREET FRONTAGE</text>
      <!-- 9-Tsubo square house -->
      <rect x="52" y="28" width="86" height="84" fill="#ffffff" stroke="#0f172a" stroke-width="1.8"/>
      <!-- 3x3 grid inside house -->
      <line x1="80.7" y1="28" x2="80.7" y2="112" stroke="#94a3b8" stroke-width="0.6" stroke-dasharray="3,2"/>
      <line x1="109.3" y1="28" x2="109.3" y2="112" stroke="#94a3b8" stroke-width="0.6" stroke-dasharray="3,2"/>
      <line x1="52" y1="56" x2="138" y2="56" stroke="#94a3b8" stroke-width="0.6" stroke-dasharray="3,2"/>
      <line x1="52" y1="84" x2="138" y2="84" stroke="#94a3b8" stroke-width="0.6" stroke-dasharray="3,2"/>
      <!-- Engawa deck -->
      <rect x="54" y="112" width="66" height="10" fill="#f6ead8" stroke="#0f172a" stroke-width="0.9"/>
      <!-- Entry pavers West -->
      <rect x="16" y="42" width="36" height="62" fill="#f1f5f9" stroke="#64748b" stroke-width="0.7"/>
      <text x="95" y="73" text-anchor="middle" style="font-size:8.5px;font-weight:800;fill:#0f172a;">9 TSUBO</text>
      <text x="95" y="84" text-anchor="middle" style="font-size:7.5px;font-weight:600;fill:#475569;">29.81 m²</text>
    </g>

    <!-- North Arrow & Scale Block -->
    <line x1="0" y1="652" x2="282" y2="652" stroke="#0f172a" stroke-width="1.2"/>
    <g transform="translate(232, 700)">
      <circle cx="0" cy="0" r="22" fill="#ffffff" stroke="#0f172a" stroke-width="1.5"/>
      <polygon points="0,-20 -6,8 0,2 6,8" fill="#0f172a"/>
      <text x="0" y="-25" text-anchor="middle" style="font-size:11px;font-weight:800;">N</text>
    </g>
    <text x="14" y="676" class="tb-lbl">PRIMARY DRAWING SCALE</text>
    <text x="14" y="698" style="font-size:14px;font-weight:800;fill:#0f172a;">{escape(self.scale_str)}</text>
    <text x="14" y="716" style="font-size:9px;fill:#475569;">1 KEN = 1,820mm · 1 SHAKU = 303mm</text>
    <text x="14" y="730" style="font-size:9px;fill:#475569;">9 TSUBO = 18 TATAMI = 29.81 m²</text>
    <line x1="0" y1="744" x2="282" y2="744" stroke="#0f172a" stroke-width="1.2"/>

    <!-- BIM Generation Notes & Performance Cap -->
    <rect x="0" y="744" width="282" height="22" fill="#e2e8f0" stroke="#0f172a" stroke-width="1.0"/>
    <text x="141" y="759" text-anchor="middle" class="tb-hdr">BIM-TO-CAD DERIVATION NOTES</text>
    <text x="12" y="782" style="font-size:8.8px;fill:#334155;">1. Plans, elevations &amp; sections are</text>
    <text x="12" y="795" style="font-size:8.8px;fill:#334155;">   automatically sliced &amp; projected from</text>
    <text x="12" y="808" style="font-size:8.8px;font-weight:700;fill:#0f172a;">   9_tsubo_house.blend (893 IFC4 objs).</text>
    <text x="12" y="826" style="font-size:8.8px;fill:#334155;">2. 3D model capped ≤ 60k tris (10.1k</text>
    <text x="12" y="839" style="font-size:8.8px;fill:#334155;">   house) for mobile WebXR &amp; Apple USDZ.</text>
    <text x="12" y="857" style="font-size:8.8px;fill:#334155;">3. Framing, flashing, rebar &amp; cavity</text>
    <text x="12" y="870" style="font-size:8.8px;fill:#334155;">   assemblies derived parametrically</text>
    <text x="12" y="883" style="font-size:8.8px;fill:#334155;">   at 2D LOD-400 (BIMCraft paradigm).</text>
    <text x="12" y="901" style="font-size:8.8px;fill:#334155;">4. All dimensions in millimeters (mm)</text>
    <text x="12" y="914" style="font-size:8.8px;fill:#334155;">   unless noted. Verify all on site.</text>
    <line x1="0" y1="932" x2="282" y2="932" stroke="#0f172a" stroke-width="1.2"/>

    <!-- Stamp -->
    <g transform="translate(141, 986)">
      <rect x="-118" y="-32" width="236" height="64" fill="#ffffff" stroke="#0f172a" stroke-width="1.5"/>
      <text x="0" y="-11" text-anchor="middle" style="font-size:10px;font-weight:800;letter-spacing:1.1px;">ISSUED FOR CONSTRUCTION STUDY</text>
      <text x="0" y="6" text-anchor="middle" style="font-size:8.8px;font-weight:700;fill:#1d4ed8;">MODEL-SYNCED · BLENDER 5.2 + IFC4</text>
      <text x="0" y="21" text-anchor="middle" style="font-size:8.2px;fill:#475569;">AUTO-GENERATED · ZERO MANUAL TRACE</text>
    </g>

    <!-- Sheet Title & Sheet Number -->
    <line x1="0" y1="1040" x2="282" y2="1040" stroke="#0f172a" stroke-width="1.8"/>
    <text x="12" y="1058" class="tb-lbl">SHEET TITLE</text>
    <text x="12" y="1084" style="font-size:{11.4 if len(self.sheet_title) > 27 else 14.0}px;font-weight:800;fill:#0f172a;letter-spacing:0.3px;">{escape(self.sheet_title)}</text>
    <text x="12" y="1104" style="font-size:9.5px;font-weight:600;fill:#475569;">9-TSUBO HOUSE (KOIZUMI STUDIO, 1999)</text>
    <line x1="0" y1="1124" x2="282" y2="1124" stroke="#0f172a" stroke-width="1.8"/>
    <rect x="0" y="1124" width="282" height="104" fill="#f1f5f9"/>
    <text x="12" y="1146" class="tb-lbl">SHEET NUMBER</text>
    <text x="141" y="1196" text-anchor="middle" class="sheet-num">{escape(self.sheet_id)}</text>
    <text x="270" y="1218" text-anchor="end" style="font-size:9.5px;font-weight:700;fill:#475569;">OF {self.total_sheets} SHEETS</text>
  </g>"""

    def render(self):
        lines = [
            '<?xml version="1.0" encoding="UTF-8"?>',
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1280" width="1920" height="1280">',
            SVG_DEFS,
            '  <!-- Archival Drafting Vellum -->',
            '  <rect x="0" y="0" width="1920" height="1280" fill="#fdfcf8"/>',
            '  <rect x="26" y="26" width="1594" height="1228" fill="url(#draft-grid)"/>',
            '  <!-- Double CAD Sheet Border -->',
            '  <rect x="16" y="16" width="1888" height="1248" fill="none" stroke="#0f172a" stroke-width="2.8"/>',
            '  <rect x="26" y="26" width="1594" height="1228" fill="none" stroke="#0f172a" stroke-width="1.4"/>',
            self._title_block(),
            '  <!-- MAIN DRAWING FIELD (x = 26..1620, y = 26..1254) -->',
            '  <g id="drawing-content">',
        ]
        lines.extend(self.body)
        lines.append('  </g>')
        lines.append('</svg>')
        return "\n".join(lines)

    def save(self, filepath):
        import re
        xml_str = self.render()
        # Guarantee valid XML: escape any bare '&' not already an entity
        xml_str = re.sub(r'&(?!amp;|lt;|gt;|quot;|apos;|#)', '&amp;', xml_str)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(xml_str)


# =========================================================================
# 2. TRUE 3D BLENDER MESH SLICING & HIDDEN-FACE ORTHOGRAPHIC PROJECTION
# =========================================================================
def get_group_meshes(root_names, exclude_substrs=()):
    res = []
    for o in bpy.data.objects:
        if o.type != "MESH" or not o.data:
            continue
        p = o
        while p.parent:
            p = p.parent
        if p.name not in root_names:
            continue
        nl = o.name.lower()
        if any(s in nl for s in exclude_substrs):
            continue
        res.append(o)
    return res

def material_fill_and_stroke(obj):
    """Subtle monochrome architectural paper tint + lineweight hierarchy derived from BIM object class."""
    n = obj.name.lower()
    mat = obj.data.materials[0].name.lower() if (obj.data.materials and obj.data.materials[0]) else ""

    if any(k in n for k in ("seam", "slot", "grout")):
        return (None, "#94a3b8", 0.45)
    if "glass" in n or "glass" in mat:
        return ("#e0f2fe", "#0284c7", 0.75)
    if "shoji_paper" in n or "shoji_warm" in n or "jimado_shoji" in n:
        return ("#faf8f0", "#64748b", 0.55)
    if "tatami_mat" in n:
        return ("url(#hatch-tatami)", "#475569", 0.70)
    if "tatami_border" in n:
        return ("#d6d1b8", "#334155", 0.55)
    if "shower_floor_tile" in n:
        return ("#f1f5f9", "#94a3b8", 0.45)
    if "roof" in n and "gutter" not in n and "downspout" not in n:
        return ("#cbd5e1", "#0f172a", 1.35)
    if "foundation" in n or "concrete" in n or "footing" in n or "mortar" in n:
        return ("#e5e7eb", "#1e293b", 1.05)
    if "deck_plank" in n or "deck_subframe" in n:
        return ("#f6ead8", "#475569", 0.65)
    if "column" in n or "beam" in n or "ridge" in n or "stair_" in n:
        return ("#f5e8d4", "#0f172a", 1.15)
    if "wall_" in n or "plywall" in n:
        return ("#ffffff", "#0f172a", 1.15)
    if "fixture_" in n:
        return ("#fef3c7", "#0f172a", 0.85)
    if "winframe" in n or "sash_" in n or "slidingwin" in n or "canopy" in n or "gutter" in n or "downspout" in n:
        return ("#e2e8f0", "#1e293b", 0.85)
    if "kit" in n or "bath" in n or "vanity" in n or "wc_" in n or "shower_" in n:
        return ("#f8fafc", "#334155", 0.75)
    if "ctx_road" in n or "asphalt" in mat:
        return ("#e2e8f0", "#64748b", 0.60)
    if "sakura" in n:
        return ("#fce7f3", "#9d174d", 0.55)
    if "tree" in n or "shrub" in n or "hedge" in n or "leaf" in n:
        return ("#dcfce7", "#166534", 0.55)
    if "ctx_" in n:
        return ("#f1f5f9", "#64748b", 0.65)
    return ("#faf7f2", "#334155", 0.70)

def cut_hatch_for_obj(obj):
    n = obj.name.lower()
    if "foundation" in n or "concrete" in n or "footing" in n or "plinth" in n:
        return ("url(#hatch-concrete)", 2.2)
    if "column" in n or "beam" in n or "ridge" in n or "stair" in n:
        return ("#e6cfa8", 2.0)
    if "house_roof" in n:
        return ("url(#hatch-steel)", 2.2)
    if any(k in n for k in ("bath_wall", "wc_wall", "shower_wall")):
        return ("url(#hatch-part-cut)", 1.9)
    if any(k in n for k in ("wall_", "plywall", "interior_loft_rear", "interior_loft_right", "interior_floor_1f")):
        return ("url(#hatch-wall-cut)", 2.3)
    if any(k in n for k in ("winframe", "sash_", "slidingwin", "door")):
        return ("#cbd5e1", 1.5)
    return ("#e2e8f0", 1.4)

def _chain_segments_into_loops(segments, tol=1e-3):
    """Chains unordered 2D line segments [(p0, p1), ...] into closed polygons / polylines."""
    if not segments:
        return []
    def key(p):
        return (round(p[0] / tol), round(p[1] / tol))

    adj = {}
    used = [False] * len(segments)
    for idx, (a, b) in enumerate(segments):
        ka, kb = key(a), key(b)
        if ka == kb:
            used[idx] = True
            continue
        adj.setdefault(ka, []).append((idx, b, kb))
        adj.setdefault(kb, []).append((idx, a, ka))

    loops = []
    for i in range(len(segments)):
        if used[i]:
            continue
        used[i] = True
        a, b = segments[i]
        chain = [a, b]
        cur_k = key(b)
        start_k = key(a)
        while True:
            nxt = None
            for idx, pt, nk in adj.get(cur_k, []):
                if not used[idx]:
                    used[idx] = True
                    nxt = (pt, nk)
                    break
            if nxt is None:
                break
            chain.append(nxt[0])
            cur_k = nxt[1]
            if cur_k == start_k:
                break
        is_closed = (cur_k == start_k and len(chain) >= 4)
        if is_closed:
            chain = chain[:-1]
        loops.append((is_closed, chain))
    return loops

def slice_objects_at_plane(objs, plane_co, plane_no, u_axis, v_axis, to_svg_fn):
    """
    True 3D bmesh.ops.bisect_plane cross-section slicer!
    Returns list of SVG elements for cut polygons (with architectural poché) and cut lines.
    """
    pco = Vector(plane_co)
    pno = Vector(plane_no).normalized()
    ua = Vector(u_axis).normalized()
    va = Vector(v_axis).normalized()

    out = []
    for obj in objs:
        # Fast world bbox rejection against cut plane
        wpts = [obj.matrix_world @ Vector(c) for c in obj.bound_box]
        dists = [(p - pco).dot(pno) for p in wpts]
        if min(dists) > 1e-4 or max(dists) < -1e-4:
            continue

        bm = bmesh.new()
        bm.from_mesh(obj.data)
        bm.transform(obj.matrix_world)
        geom = list(bm.verts) + list(bm.edges) + list(bm.faces)
        res = bmesh.ops.bisect_plane(
            bm, geom=geom, dist=1e-4,
            plane_co=pco, plane_no=pno,
            use_snap_center=False, clear_outer=False, clear_inner=False
        )
        cut_edges = [g for g in res["geom_cut"] if isinstance(g, bmesh.types.BMEdge)]
        segs = []
        for e in cut_edges:
            v0, v1 = e.verts[0].co, e.verts[1].co
            p0 = (v0.dot(ua), v0.dot(va))
            p1 = (v1.dot(ua), v1.dot(va))
            if math.hypot(p1[0] - p0[0], p1[1] - p0[1]) > 1e-4:
                segs.append((p0, p1))
        bm.free()

        if not segs:
            continue

        fill_hatch, sw = cut_hatch_for_obj(obj)
        loops = _chain_segments_into_loops(segs, tol=2e-3)
        for is_closed, pts in loops:
            spts = [to_svg_fn(u, v) for (u, v) in pts]
            pstr = " ".join(f"{sx:.1f},{sy:.1f}" for sx, sy in spts)
            if is_closed:
                out.append(f'<polygon points="{pstr}" fill="{fill_hatch}" stroke="#0a0a0a" stroke-width="{sw:.2f}" stroke-linejoin="miter"/>')
            else:
                out.append(f'<polyline points="{pstr}" fill="none" stroke="#0a0a0a" stroke-width="{sw:.2f}" stroke-linecap="square"/>')
    return out

def project_orthographic_view(
    objs,
    view_dir,
    u_axis,
    v_axis,
    to_svg_fn,
    clip_plane=None,
    depth_clip_range=None,
    override_style=None,
    skip_seams=False
):
    """
    True 3D Orthographic Hidden-Face Projection directly from Blender meshes!
    - view_dir: unit vector pointing FROM the model TOWARD the orthographic camera.
    - clip_plane: optional (plane_co, plane_no) where geometry on the +plane_no side is sliced off (clear_outer=True).
    - depth_clip_range: optional (min_depth, max_depth) along view_dir to limit depth of field.
    - Depth-sorts all front-facing polygons back-to-front (painter's order) so opaque walls
      accurately occlude interior/back geometry, producing clean CAD elevation/plan/section projections!
    """
    vd = Vector(view_dir).normalized()
    ua = Vector(u_axis).normalized()
    va = Vector(v_axis).normalized()

    draw_items = []  # (depth_key, priority, svg_poly_str)

    for obj in objs:
        if skip_seams and ("seam" in obj.name.lower() or "slot" in obj.name.lower()):
            continue

        # Fast reject via world bbox if clipped or outside depth range
        wpts = [obj.matrix_world @ Vector(c) for c in obj.bound_box]
        if clip_plane is not None:
            pco, pno = Vector(clip_plane[0]), Vector(clip_plane[1]).normalized()
            dists = [(p - pco).dot(pno) for p in wpts]
            if min(dists) > 1e-4:
                continue  # entirely on cut-away side
            needs_bisect = (max(dists) > -1e-4)
        else:
            needs_bisect = False

        if depth_clip_range is not None:
            dvals = [p.dot(vd) for p in wpts]
            if max(dvals) < depth_clip_range[0] or min(dvals) > depth_clip_range[1]:
                continue

        bm = bmesh.new()
        bm.from_mesh(obj.data)
        bm.transform(obj.matrix_world)

        if needs_bisect:
            geom = list(bm.verts) + list(bm.edges) + list(bm.faces)
            bmesh.ops.bisect_plane(
                bm, geom=geom, dist=1e-4,
                plane_co=pco, plane_no=pno,
                clear_outer=True, clear_inner=False
            )
            bm.normal_update()

        if override_style:
            fill_col, stroke_col, sw = override_style
        else:
            fill_col, stroke_col, sw = material_fill_and_stroke(obj)

        is_glass = ("glass" in obj.name.lower()) or (obj.data.materials and obj.data.materials[0] and "glass" in obj.data.materials[0].name.lower())
        is_seam = ("seam" in obj.name.lower() or "slot" in obj.name.lower())

        for f in bm.faces:
            if len(f.verts) < 3:
                continue
            no = f.normal
            nd = no.dot(vd)
            # Keep front-facing faces (allow slightly negative for double-sided thin planes like shoji/glass/seams)
            if nd <= 0.02:
                if is_seam or is_glass or "plywall" in obj.name.lower() or "lining" in obj.name.lower():
                    if abs(nd) <= 0.02:
                        continue
                else:
                    continue

            verts_3d = [v.co for v in f.verts]
            depths = [v.dot(vd) for v in verts_3d]
            avg_d = sum(depths) / len(depths)
            max_d = max(depths)
            if depth_clip_range is not None:
                if max_d < depth_clip_range[0] or min(depths) > depth_clip_range[1]:
                    continue

            pts_2d = [to_svg_fn(v.dot(ua), v.dot(va)) for v in verts_3d]
            # Compute 2D projected area to drop degenerate edge-on slivers
            area2 = 0.0
            for k in range(len(pts_2d)):
                x0, y0 = pts_2d[k]
                x1, y1 = pts_2d[(k + 1) % len(pts_2d)]
                area2 += x0 * y1 - x1 * y0
            if abs(area2) * 0.5 < 0.8 and not is_seam:
                continue

            pstr = " ".join(f"{sx:.1f},{sy:.1f}" for sx, sy in pts_2d)
            # Slight directional shading nuance for angled roofs/slopes while staying pure CAD monochrome
            actual_fill = fill_col if fill_col is not None else "none"
            opacity_attr = ' fill-opacity="0.38"' if is_glass else ""
            if is_seam:
                # Draw thin crisp architectural panel joint line
                el = f'<polygon points="{pstr}" fill="none" stroke="{stroke_col}" stroke-width="{sw:.2f}"/>'
            else:
                el = f'<polygon points="{pstr}" fill="{actual_fill}"{opacity_attr} stroke="{stroke_col}" stroke-width="{sw:.2f}" stroke-linejoin="round"/>'
            # Sort key: average depth along view_dir (smallest = farthest back, largest = closest to camera)
            bias = 0.015 if is_seam else (0.005 if "fixture_" in obj.name.lower() else 0.0)
            draw_items.append((avg_d + bias, max_d, el))

        bm.free()

    draw_items.sort(key=lambda t: (t[0], t[1]))
    return [item[2] for item in draw_items]
