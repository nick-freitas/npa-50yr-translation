#!/usr/bin/env python3
"""
D3.js organizational charts for pages 3, 5, and 21.
Each function returns an HTML string containing a container div and a script block
that calls the renderOrgChart() function defined in template.html.
"""

import json


def _chart_html(chart_id, title, chart_data):
    """Helper: wrap chart data in the standard container HTML."""
    return (
        f'<div class="org-chart-container">\n'
        f'  <div class="chart-title">{title}</div>\n'
        f'  <div id="{chart_id}"></div>\n'
        f'  <script>\n'
        f'    document.addEventListener("DOMContentLoaded", function() {{\n'
        f'      renderOrgChart("#{chart_id}", {json.dumps(chart_data)});\n'
        f'    }});\n'
        f'  </script>\n'
        f'</div>'
    )


# ============================================================================
# Page 3 — Figure 2-1: Old Police Law Organization
# ============================================================================

def get_chart_page3_en():
    """Page 3 - Figure 2-1: Organization Under the Old Police Law (English)"""

    # Spacing system
    bh = 34        # standard box height
    bh2 = 40       # two-line box height
    gap = 50       # vertical gap between boxes (room for arrow + label)
    gap_sm = 30    # small gap (no label)
    pad = 10       # internal box padding (visual only — built into dimensions)

    # Column X positions and widths
    gov_x = 10
    gov_w = 140
    nrp_x = 240
    nrp_w = 150
    # coop indicators between NRP and autonomous police
    coop_x = nrp_x + nrp_w + 10
    coop_w = 90
    # ap (autonomous police chain) after coop column
    ap_x = coop_x + coop_w + 10
    ap_w = 140
    # far-right: mayor/PSC governance
    auto_x = ap_x + ap_w + 30
    auto_w = 150

    W = auto_x + auto_w + 100  # extra space for edge labels on right

    nodes = []
    edges = []

    # --- Left Governance Column ---
    y = 15
    nodes.append({"id": "pm", "label": "Prime Minister", "x": gov_x, "y": y, "w": gov_w, "h": bh, "type": "accent"})
    y1_pm_bot = y + bh
    y += bh + gap
    nodes.append({"id": "npsc", "label": "National Public\nSafety Commission", "x": gov_x, "y": y, "w": gov_w, "h": bh2, "type": "primary"})
    edges.append({"x1": gov_x + gov_w/2, "y1": y1_pm_bot, "x2": gov_x + gov_w/2, "y2": y, "label": "Jurisdiction", "labelOffsetX": 4})
    npsc_mid_y = y + bh2/2
    y += bh2 + gap

    nodes.append({"id": "pg", "label": "Prefectural Governor", "x": gov_x, "y": y, "w": gov_w, "h": bh, "type": "accent"})
    y1_pg_bot = y + bh
    y += bh + gap
    nodes.append({"id": "ppsc", "label": "Prefectural Public\nSafety Commission", "x": gov_x, "y": y, "w": gov_w, "h": bh2, "type": "primary"})
    edges.append({"x1": gov_x + gov_w/2, "y1": y1_pg_bot, "x2": gov_x + gov_w/2, "y2": y, "label": "Jurisdiction", "labelOffsetX": 4})
    ppsc_mid_y = y + bh2/2

    # --- Center: National Rural Police vertical chain ---
    cy = 15
    nodes.append({"id": "nrp_label", "label": "● National Rural Police ●", "x": nrp_x, "y": cy, "w": nrp_w, "h": 28, "type": "branch-header"})
    cy += 28 + 12
    nodes.append({"id": "nrp_hq", "label": "NRP Headquarters", "x": nrp_x, "y": cy, "w": nrp_w, "h": bh, "type": "primary"})
    nrp_hq_mid_y = cy + bh/2
    cy_bot = cy + bh; cy += bh + gap
    edges.append({"x1": nrp_x + nrp_w/2, "y1": cy_bot, "x2": nrp_x + nrp_w/2, "y2": cy, "label": "Direction &\nSupervision", "labelOffsetX": 4})

    nodes.append({"id": "rpb", "label": "Regional Police Bureau", "x": nrp_x, "y": cy, "w": nrp_w, "h": bh, "type": "default"})
    cy_bot = cy + bh; cy += bh + gap
    edges.append({"x1": nrp_x + nrp_w/2, "y1": cy_bot, "x2": nrp_x + nrp_w/2, "y2": cy, "label": "Admin Mgmt", "labelOffsetX": 4})

    nodes.append({"id": "pnrphq", "label": "Prefectural NRP HQ", "x": nrp_x, "y": cy, "w": nrp_w, "h": bh, "type": "default"})
    pnrp_mid_y = cy + bh/2
    cy_bot = cy + bh; cy += bh + gap
    edges.append({"x1": nrp_x + nrp_w/2, "y1": cy_bot, "x2": nrp_x + nrp_w/2, "y2": cy, "label": "Direction &\nSupervision", "labelOffsetX": 4})

    nodes.append({"id": "nrp_ps", "label": "Police Stations", "x": nrp_x, "y": cy, "w": nrp_w, "h": bh, "type": "default"})
    cy_bot = cy + bh; cy += bh + gap_sm
    edges.append({"x1": nrp_x + nrp_w/2, "y1": cy_bot, "x2": nrp_x + nrp_w/2, "y2": cy, "arrow": False})

    nodes.append({"id": "nrp_sub", "label": "Substations & Posts", "x": nrp_x + 10, "y": cy, "w": nrp_w - 20, "h": 28, "type": "small"})
    cy_bot = cy + 28; cy += 28 + gap
    edges.append({"x1": nrp_x + nrp_w/2, "y1": cy_bot, "x2": nrp_x + nrp_w/2, "y2": cy, "label": "Execution", "labelOffsetX": 4})

    nodes.append({"id": "nrp_area", "label": "Other areas\n(mainly rural villages)", "x": nrp_x, "y": cy, "w": nrp_w, "h": bh2, "type": "area"})

    # --- Horizontal arrows from governance to NRP ---
    edges.append({"x1": gov_x + gov_w, "y1": npsc_mid_y, "x2": nrp_x, "y2": nrp_hq_mid_y, "label": "Direction &\nSupervision", "labelOffsetX": 0, "labelOffsetY": -22, "labelAnchor": "middle"})
    edges.append({"x1": gov_x + gov_w, "y1": ppsc_mid_y, "x2": nrp_x, "y2": pnrp_mid_y, "label": "Operational\nManagement", "labelOffsetX": 0, "labelOffsetY": -22, "labelAnchor": "middle"})



    # --- Far right: Mayor → PSC (governance for autonomous police) ---
    ry = 15
    nodes.append({"id": "mayor", "label": "Municipal Mayor", "x": auto_x, "y": ry, "w": auto_w, "h": bh, "type": "accent"})
    ry_bot = ry + bh; ry += bh + gap
    edges.append({"x1": auto_x + auto_w/2, "y1": ry_bot, "x2": auto_x + auto_w/2, "y2": ry, "label": "Jurisdiction", "labelOffsetX": 4})
    nodes.append({"id": "mpsc", "label": "Municipal Public\nSafety Commission", "x": auto_x, "y": ry, "w": auto_w, "h": bh2, "type": "primary"})
    mpsc_mid_y = ry + bh2 / 2

    # --- Center-right: Autonomous Police chain ---
    # ap_x and ap_w already defined above
    apy = 15
    nodes.append({"id": "auto_label", "label": "● Autonomous Police ●", "x": ap_x, "y": apy, "w": ap_w, "h": 28, "type": "branch-header"})
    apy += 28 + 12
    nodes.append({"id": "mp", "label": "Municipal Police", "x": ap_x, "y": apy, "w": ap_w, "h": bh, "type": "primary"})
    mp_mid_y = apy + bh / 2
    apy_bot = apy + bh; apy += bh + gap
    edges.append({"x1": ap_x + ap_w/2, "y1": apy_bot, "x2": ap_x + ap_w/2, "y2": apy, "label": "Direction &\nSupervision", "labelOffsetX": 4})
    nodes.append({"id": "auto_ps", "label": "Police Stations", "x": ap_x, "y": apy, "w": ap_w, "h": bh, "type": "default"})
    apy_bot = apy + bh; apy += bh + gap
    edges.append({"x1": ap_x + ap_w/2, "y1": apy_bot, "x2": ap_x + ap_w/2, "y2": apy, "label": "Execution", "labelOffsetX": 4})
    nodes.append({"id": "auto_area", "label": "Cities & towns\nwith pop. 5,000+", "x": ap_x, "y": apy, "w": ap_w, "h": bh2, "type": "area"})

    # --- Horizontal dashed arrow: PSC → Municipal Police (Management) ---
    edges.append({"x1": auto_x, "y1": mpsc_mid_y, "x2": ap_x + ap_w, "y2": mp_mid_y, "label": "Management", "labelOffsetX": 0, "labelOffsetY": -14, "labelAnchor": "middle", "dash": "5,3"})

    # --- Cooperation indicators — rendered as dashed lines between NRP and AP columns ---
    # Vertical dashed line between the two police chains
    nrp_center_x = nrp_x + nrp_w / 2
    ap_center_x = ap_x + ap_w / 2
    mid_x = (nrp_x + nrp_w + ap_x) / 2
    edges.append({"x1": nrp_x + nrp_w + 5, "y1": 120, "x2": ap_x - 5, "y2": 120, "dash": "4,3", "arrow": False})
    edges.append({"x1": nrp_x + nrp_w + 5, "y1": 200, "x2": ap_x - 5, "y2": 200, "dash": "4,3", "arrow": False})
    nodes.append({"id": "coop_label", "label": "× Oper./Admin Mgmt\n◇ Mutual Cooperation", "x": nrp_x + nrp_w + 8, "y": 140, "w": ap_x - nrp_x - nrp_w - 16, "h": 40, "type": "coop"})

    H = max(cy + bh2, apy + bh2) + 30

    chart_data = {
        "width": W,
        "height": H,
        "nodes": nodes,
        "edges": edges,
    }

    return _chart_html("chart-p3-en", "Figure 2-1: Organization of Police Under the Old Police Law", chart_data)


def get_chart_page3_jp():
    """Page 3 - Figure 2-1: Organization Under the Old Police Law (Japanese)"""

    # Spacing system
    bh = 34        # standard box height
    bh2 = 40       # two-line box height
    gap = 50       # vertical gap between boxes (room for arrow + label)
    gap_sm = 30    # small gap (no label)

    # Column X positions and widths
    gov_x = 10
    gov_w = 120
    nrp_x = 220
    nrp_w = 140
    coop_x = nrp_x + nrp_w + 10
    coop_w = 85
    ap_x = coop_x + coop_w + 10
    ap_w = 130
    auto_x = ap_x + ap_w + 30
    auto_w = 130

    W = auto_x + auto_w + 80  # extra space for edge labels on right

    nodes = []
    edges = []

    # --- Left Governance Column ---
    y = 15
    nodes.append({"id": "pm", "label": "\u5185\u95a3\u7dcf\u7406\u5927\u81e3", "x": gov_x, "y": y, "w": gov_w, "h": bh, "type": "accent"})
    y1_pm_bot = y + bh
    y += bh + gap
    nodes.append({"id": "npsc", "label": "\u56fd\u5bb6\u516c\u5b89\u59d4\u54e1\u4f1a", "x": gov_x, "y": y, "w": gov_w, "h": bh, "type": "primary"})
    edges.append({"x1": gov_x + gov_w/2, "y1": y1_pm_bot, "x2": gov_x + gov_w/2, "y2": y, "label": "\u6240\u8f44", "labelOffsetX": 4})
    npsc_mid_y = y + bh/2
    y += bh + gap

    nodes.append({"id": "pg", "label": "\u90fd\u9053\u5e9c\u770c\u77e5\u4e8b", "x": gov_x, "y": y, "w": gov_w, "h": bh, "type": "accent"})
    y1_pg_bot = y + bh
    y += bh + gap
    nodes.append({"id": "ppsc", "label": "\u90fd\u9053\u5e9c\u770c\n\u516c\u5b89\u59d4\u54e1\u4f1a", "x": gov_x, "y": y, "w": gov_w, "h": bh2, "type": "primary"})
    edges.append({"x1": gov_x + gov_w/2, "y1": y1_pg_bot, "x2": gov_x + gov_w/2, "y2": y, "label": "\u6240\u8f44", "labelOffsetX": 4})
    ppsc_mid_y = y + bh2/2

    # --- Center: National Rural Police vertical chain ---
    cy = 15
    nodes.append({"id": "nrp_label", "label": "\u25cf\u56fd\u5bb6\u5730\u65b9\u8b66\u5bdf\u25cf", "x": nrp_x, "y": cy, "w": nrp_w, "h": 28, "type": "branch-header"})
    cy += 28 + 12
    nodes.append({"id": "nrp_hq", "label": "\u56fd\u5bb6\u5730\u65b9\u8b66\u5bdf\u672c\u90e8", "x": nrp_x, "y": cy, "w": nrp_w, "h": bh, "type": "primary"})
    nrp_hq_mid_y = cy + bh/2
    cy_bot = cy + bh; cy += bh + gap
    edges.append({"x1": nrp_x + nrp_w/2, "y1": cy_bot, "x2": nrp_x + nrp_w/2, "y2": cy, "label": "\u6307\u63ee\u76e3\u7763", "labelOffsetX": 4})

    nodes.append({"id": "rpb", "label": "\u8b66\u5bdf\u7ba1\u533a\u672c\u90e8", "x": nrp_x, "y": cy, "w": nrp_w, "h": bh, "type": "default"})
    cy_bot = cy + bh; cy += bh + gap
    edges.append({"x1": nrp_x + nrp_w/2, "y1": cy_bot, "x2": nrp_x + nrp_w/2, "y2": cy, "label": "\u884c\u653f\u7ba1\u7406", "labelOffsetX": 4})

    nodes.append({"id": "pnrphq", "label": "\u90fd\u9053\u5e9c\u770c\n\u56fd\u5bb6\u5730\u65b9\u8b66\u5bdf\u672c\u90e8", "x": nrp_x, "y": cy, "w": nrp_w, "h": bh2, "type": "default"})
    pnrp_mid_y = cy + bh2/2
    cy_bot = cy + bh2; cy += bh2 + gap
    edges.append({"x1": nrp_x + nrp_w/2, "y1": cy_bot, "x2": nrp_x + nrp_w/2, "y2": cy, "label": "\u6307\u63ee\u76e3\u7763", "labelOffsetX": 4})

    nodes.append({"id": "nrp_ps", "label": "\u8b66\u5bdf\u7f72", "x": nrp_x, "y": cy, "w": nrp_w, "h": bh, "type": "default"})
    cy_bot = cy + bh; cy += bh + gap_sm
    edges.append({"x1": nrp_x + nrp_w/2, "y1": cy_bot, "x2": nrp_x + nrp_w/2, "y2": cy, "arrow": False})

    nodes.append({"id": "nrp_sub", "label": "\u6d3e\u51fa\u6240\u30fb\u99d0\u5728\u6240", "x": nrp_x + 10, "y": cy, "w": nrp_w - 20, "h": 28, "type": "small"})
    cy_bot = cy + 28; cy += 28 + gap
    edges.append({"x1": nrp_x + nrp_w/2, "y1": cy_bot, "x2": nrp_x + nrp_w/2, "y2": cy, "label": "\u57f7\u884c", "labelOffsetX": 4})

    nodes.append({"id": "nrp_area", "label": "\u305d\u306e\u4ed6\u306e\u5730\u57df\n\uff08\u4e3b\u3068\u3057\u3066\u6751\u843d\u90e8\uff09", "x": nrp_x, "y": cy, "w": nrp_w, "h": bh2, "type": "area"})

    # --- Horizontal arrows from governance to NRP ---
    edges.append({"x1": gov_x + gov_w, "y1": npsc_mid_y, "x2": nrp_x, "y2": nrp_hq_mid_y, "label": "\u6307\u63ee\u76e3\u7763", "labelOffsetX": 0, "labelOffsetY": -22, "labelAnchor": "middle"})
    edges.append({"x1": gov_x + gov_w, "y1": ppsc_mid_y, "x2": nrp_x, "y2": pnrp_mid_y, "label": "\u904b\u55b6\u7ba1\u7406", "labelOffsetX": 0, "labelOffsetY": -22, "labelAnchor": "middle"})

    # --- Far right: Mayor → PSC (governance for autonomous police) ---
    ry = 15
    nodes.append({"id": "mayor", "label": "市町村長", "x": auto_x, "y": ry, "w": auto_w, "h": bh, "type": "accent"})
    ry_bot = ry + bh; ry += bh + gap
    edges.append({"x1": auto_x + auto_w/2, "y1": ry_bot, "x2": auto_x + auto_w/2, "y2": ry, "label": "所轄", "labelOffsetX": 4})
    nodes.append({"id": "mpsc", "label": "市町村公安委員会", "x": auto_x, "y": ry, "w": auto_w, "h": bh, "type": "primary"})
    mpsc_mid_y = ry + bh / 2

    # --- Center-right: Autonomous Police chain ---
    # ap_x and ap_w already defined above
    apy = 15
    nodes.append({"id": "auto_label", "label": "●自治体警察●", "x": ap_x, "y": apy, "w": ap_w, "h": 28, "type": "branch-header"})
    apy += 28 + 12
    nodes.append({"id": "mp", "label": "市町村警察", "x": ap_x, "y": apy, "w": ap_w, "h": bh, "type": "primary"})
    mp_mid_y = apy + bh / 2
    apy_bot = apy + bh; apy += bh + gap
    edges.append({"x1": ap_x + ap_w/2, "y1": apy_bot, "x2": ap_x + ap_w/2, "y2": apy, "label": "指揮監督", "labelOffsetX": 4})
    nodes.append({"id": "auto_ps", "label": "警察署", "x": ap_x, "y": apy, "w": ap_w, "h": bh, "type": "default"})
    apy_bot = apy + bh; apy += bh + gap
    edges.append({"x1": ap_x + ap_w/2, "y1": apy_bot, "x2": ap_x + ap_w/2, "y2": apy, "label": "執行", "labelOffsetX": 4})
    nodes.append({"id": "auto_area", "label": "市及び人口5千人以上\nの市街的町村", "x": ap_x, "y": apy, "w": ap_w, "h": bh2, "type": "area"})

    # --- Horizontal dashed arrow: PSC → Municipal Police (Management) ---
    edges.append({"x1": auto_x, "y1": mpsc_mid_y, "x2": ap_x + ap_w, "y2": mp_mid_y, "label": "管理", "labelOffsetX": 0, "labelOffsetY": -14, "labelAnchor": "middle", "dash": "5,3"})

    # --- Cooperation indicators — dashed lines between NRP and AP columns ---
    edges.append({"x1": nrp_x + nrp_w + 5, "y1": 120, "x2": ap_x - 5, "y2": 120, "dash": "4,3", "arrow": False})
    edges.append({"x1": nrp_x + nrp_w + 5, "y1": 200, "x2": ap_x - 5, "y2": 200, "dash": "4,3", "arrow": False})
    nodes.append({"id": "coop_label", "label": "× 運営管理・行政管理\n◇ 相互協力", "x": nrp_x + nrp_w + 8, "y": 140, "w": ap_x - nrp_x - nrp_w - 16, "h": 40, "type": "coop"})

    H = max(cy + bh2, apy + bh2) + 30

    chart_data = {
        "width": W,
        "height": H,
        "nodes": nodes,
        "edges": edges,
    }

    return _chart_html("chart-p3-jp", "\u56f32-1\uff1a\u65e7\u8b66\u5bdf\u6cd5\u306b\u5b9a\u3081\u308b\u8b66\u5bdf\u306e\u7d44\u7e54", chart_data)


# ============================================================================
# Page 5 — Figure 2-2: New Police Law Organization
# ============================================================================

def get_chart_page5_en():
    """Page 5 - Figure 2-2: Organization Under the New Police Law (English)"""

    # Spacing system
    bh = 34        # standard box height
    bh2 = 40       # two-line box height
    gap = 50       # vertical gap between boxes (room for arrow + label)
    gap_sm = 30    # small gap (no label)

    # Column X positions and widths
    gov_x = 10
    gov_w = 140
    cx = 200
    cw = 150

    W = cx + cw + 20

    nodes = []
    edges = []

    # --- Center chain: PM -> NPSC -> NPA ---
    y = 15
    nodes.append({"id": "pm", "label": "Prime Minister", "x": cx, "y": y, "w": cw, "h": bh, "type": "accent"})
    y_bot = y + bh; y += bh + gap
    edges.append({"x1": cx + cw/2, "y1": y_bot, "x2": cx + cw/2, "y2": y, "label": "Jurisdiction", "labelOffsetX": 4})

    nodes.append({"id": "npsc", "label": "National Public\nSafety Commission", "x": cx - 10, "y": y, "w": cw + 20, "h": bh2, "type": "primary"})
    y_bot = y + bh2; y += bh2 + gap
    edges.append({"x1": cx + cw/2, "y1": y_bot, "x2": cx + cw/2, "y2": y, "label": "Management", "labelOffsetX": 4})

    nodes.append({"id": "npa", "label": "National Police Agency", "x": cx, "y": y, "w": cw, "h": bh, "type": "highlight"})
    y_bot = y + bh; y += bh + gap
    edges.append({"x1": cx + cw/2, "y1": y_bot, "x2": cx + cw/2, "y2": y, "label": "Direction &\nSupervision", "labelOffsetX": 4})

    # --- Prefectural Police ---
    pp_label_y = y
    nodes.append({"id": "pp_label", "label": "Prefectural Police", "x": cx - 5, "y": y, "w": cw + 10, "h": 26, "type": "branch-header"})
    y += 26 + 12

    nodes.append({"id": "pphq", "label": "Prefectural Police HQ", "x": cx, "y": y, "w": cw, "h": bh, "type": "default"})
    pphq_mid_y = y + bh/2
    y_bot = y + bh; y += bh + gap
    edges.append({"x1": cx + cw/2, "y1": y_bot, "x2": cx + cw/2, "y2": y, "label": "Direction &\nSupervision", "labelOffsetX": 4})

    nodes.append({"id": "ps", "label": "Police Stations", "x": cx, "y": y, "w": cw, "h": bh, "type": "default"})
    y_bot = y + bh; y += bh + gap_sm
    edges.append({"x1": cx + cw/2, "y1": y_bot, "x2": cx + cw/2, "y2": y, "arrow": False})

    nodes.append({"id": "sub", "label": "Substations &\nResidential Posts", "x": cx + 10, "y": y, "w": cw - 20, "h": bh2, "type": "small"})
    y_bot = y + bh2; y += bh2 + gap
    edges.append({"x1": cx + cw/2, "y1": y_bot, "x2": cx + cw/2, "y2": y, "label": "Execution", "labelOffsetX": 4})

    nodes.append({"id": "area", "label": "Each prefecture\u2019s\njurisdictional area", "x": cx, "y": y, "w": cw, "h": bh2, "type": "area"})

    # --- Left: Governor track (aligned with Prefectural Police section) ---
    gy = pp_label_y
    nodes.append({"id": "gov", "label": "Prefectural\nGovernor", "x": gov_x, "y": gy, "w": gov_w, "h": bh2, "type": "accent"})
    gy_bot = gy + bh2; gy += bh2 + gap
    edges.append({"x1": gov_x + gov_w/2, "y1": gy_bot, "x2": gov_x + gov_w/2, "y2": gy, "label": "Jurisdiction", "labelOffsetX": 4})

    nodes.append({"id": "ppsc", "label": "Prefectural Public\nSafety Commission", "x": gov_x, "y": gy, "w": gov_w, "h": bh2, "type": "primary"})
    ppsc_mid_y = gy + bh2/2

    # PPSC -> Prefectural Police HQ (Management)
    edges.append({"x1": gov_x + gov_w, "y1": ppsc_mid_y, "x2": cx, "y2": pphq_mid_y, "label": "Management", "labelOffsetX": 0, "labelOffsetY": -22, "labelAnchor": "middle"})

    H = y + bh2 + 30

    chart_data = {
        "width": W,
        "height": H,
        "nodes": nodes,
        "edges": edges,
    }

    return _chart_html("chart-p5-en", "Figure 2-2: Organization of Police Under the New Police Law", chart_data)


def get_chart_page5_jp():
    """Page 5 - Figure 2-2: Organization Under the New Police Law (Japanese)"""

    # Spacing system
    bh = 34        # standard box height
    bh2 = 40       # two-line box height
    gap = 50       # vertical gap between boxes (room for arrow + label)
    gap_sm = 30    # small gap (no label)

    # Column X positions and widths
    gov_x = 10
    gov_w = 130
    cx = 190
    cw = 140

    W = cx + cw + 20

    nodes = []
    edges = []

    # --- Center chain: PM -> NPSC -> NPA ---
    y = 15
    nodes.append({"id": "pm", "label": "\u5185\u95a3\u7dcf\u7406\u5927\u81e3", "x": cx, "y": y, "w": cw, "h": bh, "type": "accent"})
    y_bot = y + bh; y += bh + gap
    edges.append({"x1": cx + cw/2, "y1": y_bot, "x2": cx + cw/2, "y2": y, "label": "\u6240\u8f44", "labelOffsetX": 4})

    nodes.append({"id": "npsc", "label": "\u56fd\u5bb6\u516c\u5b89\u59d4\u54e1\u4f1a", "x": cx - 5, "y": y, "w": cw + 10, "h": bh, "type": "primary"})
    y_bot = y + bh; y += bh + gap
    edges.append({"x1": cx + cw/2, "y1": y_bot, "x2": cx + cw/2, "y2": y, "label": "\u7ba1\u7406", "labelOffsetX": 4})

    nodes.append({"id": "npa", "label": "\u8b66\u5bdf\u5e81", "x": cx, "y": y, "w": cw, "h": bh, "type": "highlight"})
    y_bot = y + bh; y += bh + gap
    edges.append({"x1": cx + cw/2, "y1": y_bot, "x2": cx + cw/2, "y2": y, "label": "\u6307\u63ee\u76e3\u7763", "labelOffsetX": 4})

    # --- Prefectural Police ---
    pp_label_y = y
    nodes.append({"id": "pp_label", "label": "\u25cf\u90fd\u9053\u5e9c\u770c\u8b66\u5bdf\u25cf", "x": cx - 5, "y": y, "w": cw + 10, "h": 26, "type": "branch-header"})
    y += 26 + 12

    nodes.append({"id": "pphq", "label": "\u90fd\u9053\u5e9c\u770c\u8b66\u5bdf\u672c\u90e8", "x": cx, "y": y, "w": cw, "h": bh, "type": "default"})
    pphq_mid_y = y + bh/2
    y_bot = y + bh; y += bh + gap
    edges.append({"x1": cx + cw/2, "y1": y_bot, "x2": cx + cw/2, "y2": y, "label": "\u6307\u63ee\u76e3\u7763", "labelOffsetX": 4})

    nodes.append({"id": "ps", "label": "\u8b66\u5bdf\u7f72", "x": cx, "y": y, "w": cw, "h": bh, "type": "default"})
    y_bot = y + bh; y += bh + gap_sm
    edges.append({"x1": cx + cw/2, "y1": y_bot, "x2": cx + cw/2, "y2": y, "arrow": False})

    nodes.append({"id": "sub", "label": "\u6d3e\u51fa\u6240\u30fb\u99d0\u5728\u6240", "x": cx + 10, "y": y, "w": cw - 20, "h": 28, "type": "small"})
    y_bot = y + 28; y += 28 + gap
    edges.append({"x1": cx + cw/2, "y1": y_bot, "x2": cx + cw/2, "y2": y, "label": "\u57f7\u884c", "labelOffsetX": 4})

    nodes.append({"id": "area", "label": "\u5404\u90fd\u9053\u5e9c\u770c\u306e\u533a\u57df", "x": cx, "y": y, "w": cw, "h": bh, "type": "area"})

    # --- Left: Governor track (aligned with Prefectural Police section) ---
    gy = pp_label_y
    nodes.append({"id": "gov", "label": "\u90fd\u9053\u5e9c\u770c\u77e5\u4e8b", "x": gov_x, "y": gy, "w": gov_w, "h": bh, "type": "accent"})
    gy_bot = gy + bh; gy += bh + gap
    edges.append({"x1": gov_x + gov_w/2, "y1": gy_bot, "x2": gov_x + gov_w/2, "y2": gy, "label": "\u6240\u8f44", "labelOffsetX": 4})

    nodes.append({"id": "ppsc", "label": "\u90fd\u9053\u5e9c\u770c\n\u516c\u5b89\u59d4\u54e1\u4f1a", "x": gov_x, "y": gy, "w": gov_w, "h": bh2, "type": "primary"})
    ppsc_mid_y = gy + bh2/2

    # PPSC -> Prefectural Police HQ (Management)
    edges.append({"x1": gov_x + gov_w, "y1": ppsc_mid_y, "x2": cx, "y2": pphq_mid_y, "label": "\u7ba1\u7406", "labelOffsetX": 0, "labelOffsetY": -22, "labelAnchor": "middle"})

    H = y + bh + 30

    chart_data = {
        "width": W,
        "height": H,
        "nodes": nodes,
        "edges": edges,
    }

    return _chart_html("chart-p5-jp", "\u56f32-2\uff1a\u65b0\u8b66\u5bdf\u6cd5\u306b\u5b9a\u3081\u308b\u8b66\u5bdf\u306e\u7d44\u7e54", chart_data)


# ============================================================================
# Page 21 — Two Charts: Organizational Reform + National Security
# ============================================================================

def get_chart_page21_en():
    """Page 21 - Organizational Reform + National Security Responsibility (English)"""

    # Spacing system
    gap = 40       # vertical gap between sections
    bh = 34        # standard box height
    bh2 = 40       # two-line box height

    W = 900

    nodes = []
    edges = []

    # --- Subtitle ---
    y = 0
    nodes.append({"id": "subtitle", "label": "Strengthening Organized Crime Countermeasures / Prevention of Terrorism / Strengthening Cyber Crime Countermeasures", "x": 0, "y": y, "w": W, "h": 18, "type": "subtitle"})
    y += 18 + 8

    # === Chart 1: Organizational Reform ===
    nodes.append({"id": "sec1", "label": "\u2460 Organizational Reform", "x": 0, "y": y, "w": 200, "h": 20, "type": "section-title"})
    y += 20 + 10

    # Top row: NPSC -> NPA -> Imperial Guard
    top_row_y = y
    top_h = bh
    nodes.append({"id": "npsc", "label": "National Public\nSafety Commission", "x": 20, "y": top_row_y, "w": 150, "h": top_h, "type": "primary"})
    edges.append({"x1": 170, "y1": top_row_y + top_h/2, "x2": 200, "y2": top_row_y + top_h/2, "arrow": False})
    nodes.append({"id": "npa", "label": "National Police\nAgency", "x": 200, "y": top_row_y, "w": 130, "h": top_h, "type": "highlight"})
    npa_mid_x = 200 + 130/2
    edges.append({"x1": 330, "y1": top_row_y + top_h/2, "x2": 360, "y2": top_row_y + top_h/2, "arrow": False})
    nodes.append({"id": "ig", "label": "Imperial\nGuard HQ", "x": 360, "y": top_row_y, "w": 90, "h": top_h, "type": "accent"})
    nodes.append({"id": "ig_note", "label": "Provisions for application\nof Police Duties Act revised", "x": 455, "y": top_row_y, "w": 160, "h": top_h, "type": "note"})
    y_bot = top_row_y + top_h
    y = y_bot + 18  # small gap before divisions

    # Vertical line from NPA down to divisions
    edges.append({"x1": npa_mid_x, "y1": y_bot, "x2": npa_mid_x, "y2": y, "arrow": False})

    # --- Bureau division boxes ---
    div_y = y
    div_w = 155
    div_gap = 10
    div_start_x = 10
    div_header_h = 36

    # Column 1: Commissioner's Secretariat
    x1 = div_start_x
    nodes.append({"id": "d1h", "label": "Commissioner's\nSecretariat, etc.", "x": x1, "y": div_y, "w": div_w, "h": div_header_h, "type": "div-header"})

    # Column 2: Criminal Investigation Bureau
    x2 = div_start_x + div_w + div_gap
    nodes.append({"id": "d2h", "label": "Criminal\nInvestigation Bureau", "x": x2, "y": div_y, "w": div_w, "h": div_header_h, "type": "div-header-active"})
    dby2 = div_y + div_header_h + 1
    d2b_h = 195
    nodes.append({"id": "d2b", "label": "Organized Crime Division\n\u2190 Reorg. from Anti-\nBoryokudan Div.\n\n\u2022 Anti-boryokudan measures\n\u2022 Drug & firearms countermeasures\n\u2022 Crimes by foreign nationals\n\n\u2192 Integrated promotion\n\nPlanning & Analysis\nAnti-Boryokudan\nDrug & Firearms\nInt'l Investigation Mgr.", "x": x2, "y": dby2, "w": div_w, "h": d2b_h, "type": "div-body-active"})

    # Column 3: Security Bureau
    x3 = div_start_x + 2 * (div_w + div_gap)
    nodes.append({"id": "d3h", "label": "Security\nBureau", "x": x3, "y": div_y, "w": div_w, "h": div_header_h, "type": "div-header-active"})
    dby3 = div_y + div_header_h + 1
    d3b_h = 195
    nodes.append({"id": "d3b", "label": "Foreign Affairs\nIntelligence Div.\n\u2190 Reorg. from\nSecretariat Int'l Div.\n\n\u2022 High-level negotiations\n  with foreign agencies\n\u2022 Close & rapid info\n  exchange\n\n\u2192 Strengthened intelligence\n\nForeign Affairs Div.\nInt'l Terrorism\nCountermeasures", "x": x3, "y": dby3, "w": div_w, "h": d3b_h, "type": "div-body-active"})

    # Column 4: Community Safety Bureau
    x4 = div_start_x + 3 * (div_w + div_gap)
    nodes.append({"id": "d4h", "label": "Community\nSafety Bureau", "x": x4, "y": div_y, "w": div_w, "h": div_header_h, "type": "div-header-active"})
    dby4 = div_y + div_header_h + 1
    nodes.append({"id": "d4b", "label": "IT Crime\nCountermeasures\nDivision", "x": x4, "y": dby4, "w": div_w, "h": 50, "type": "div-body-active"})

    # Column 5: Info & Comms Bureau
    x5 = div_start_x + 4 * (div_w + div_gap)
    nodes.append({"id": "d5h", "label": "Info & Comms\nBureau", "x": x5, "y": div_y, "w": div_w, "h": div_header_h, "type": "div-header-active"})
    dby5 = div_y + div_header_h + 1
    nodes.append({"id": "d5b", "label": "Prefectural Info &\nCommunications\nDepartments", "x": x5, "y": dby5, "w": div_w, "h": 50, "type": "div-body-active"})

    # Calculate bottom of tallest division column
    div_bottom = max(dby2 + d2b_h, dby3 + d3b_h)
    y = div_bottom + gap

    # === Chart 2: National Security Responsibility ===
    sec2_y = y
    nodes.append({"id": "sec2", "label": "\u2461 National Security Responsibility", "x": 0, "y": sec2_y, "w": 280, "h": 20, "type": "section-title"})
    y = sec2_y + 20 + 10

    # Top row: 4 boxes
    sr_y = y
    sr_w = 140
    sr_h = 46
    sr_gap = 8
    sr_start = 10

    nodes.append({"id": "s1", "label": "Police management\nfor major terrorism\ncases", "x": sr_start, "y": sr_y, "w": sr_w, "h": sr_h, "type": "sec-box"})
    nodes.append({"id": "s2", "label": "Handling terrorism\noverseas involving\nJapanese victims", "x": sr_start + sr_w + sr_gap, "y": sr_y, "w": sr_w, "h": sr_h, "type": "sec-box"})
    nodes.append({"id": "s3", "label": "Liaison with foreign\npolice agencies", "x": sr_start + 2*(sr_w + sr_gap), "y": sr_y, "w": sr_w, "h": sr_h, "type": "sec-box"})
    nodes.append({"id": "s4", "label": "Technical support\nfor cyber crime\ninvestigations", "x": sr_start + 3*(sr_w + sr_gap), "y": sr_y, "w": sr_w, "h": sr_h, "type": "sec-box"})
    y = sr_y + sr_h + 14

    # Middle: strengthen box
    mid_y = y
    mid_h = 36
    nodes.append({"id": "smid", "label": "Strengthen NPA initiative &\nclarify national security responsibility", "x": 60, "y": mid_y, "w": W - 120, "h": mid_h, "type": "highlight"})
    y_bot = mid_y + mid_h; y = y_bot + gap
    edges.append({"x1": W/2, "y1": y_bot, "x2": W/2, "y2": y})

    # Prefectural Police -> Response
    resp_y = y
    resp_h = 30
    nodes.append({"id": "sresp", "label": "Prefectural Police \u2192 Response", "x": 150, "y": resp_y, "w": W - 300, "h": resp_h, "type": "primary"})
    y_bot = resp_y + resp_h; y = y_bot + 18
    edges.append({"x1": W/2, "y1": y_bot, "x2": W/2, "y2": y, "arrow": False})

    # Bottom row: 4 result boxes
    br_y = y
    br_w = 140
    br_h = 36

    nodes.append({"id": "r1", "label": "Bomb / NBC\nterrorism", "x": sr_start, "y": br_y, "w": br_w, "h": br_h, "type": "sec-result"})
    nodes.append({"id": "r2", "label": "Overseas\nterrorism", "x": sr_start + br_w + sr_gap, "y": br_y, "w": br_w, "h": br_h, "type": "sec-result"})
    nodes.append({"id": "r3", "label": "International\norganized crime", "x": sr_start + 2*(br_w + sr_gap), "y": br_y, "w": br_w, "h": br_h, "type": "sec-result"})
    nodes.append({"id": "r4", "label": "Cyber crime", "x": sr_start + 3*(br_w + sr_gap), "y": br_y, "w": br_w, "h": br_h, "type": "sec-result"})

    # Adjust total height
    total_h = br_y + br_h + 16

    chart_data = {
        "width": W,
        "height": total_h,
        "nodes": nodes,
        "edges": edges,
    }

    return _chart_html(
        "chart-p21-en",
        "Overview of the Law Partially Amending the Police Act",
        chart_data,
    )


def get_chart_page21_jp():
    """Page 21 - Organizational Reform + National Security Responsibility (Japanese)"""

    # Spacing system
    gap = 40       # vertical gap between sections
    bh = 34        # standard box height

    W = 900

    nodes = []
    edges = []

    # --- Subtitle ---
    y = 0
    nodes.append({"id": "subtitle", "label": "\u7d44\u7e54\u72af\u7f6a\u5bfe\u7b56\u306e\u5f37\u5316\uff0f\u30c6\u30ed\u306e\u672a\u7136\u9632\u6b62\uff0f\u30b5\u30a4\u30d0\u30fc\u72af\u7f6a\u5bfe\u7b56\u306e\u5f37\u5316", "x": 0, "y": y, "w": W, "h": 18, "type": "subtitle"})
    y += 18 + 8

    # === Chart 1: Organizational Reform ===
    nodes.append({"id": "sec1", "label": "\u2460 \u7d44\u7e54\u6539\u6b63", "x": 0, "y": y, "w": 150, "h": 20, "type": "section-title"})
    y += 20 + 10

    # Top row: NPSC -> NPA -> Imperial Guard
    top_row_y = y
    top_h = 30
    nodes.append({"id": "npsc", "label": "\u56fd\u5bb6\u516c\u5b89\u59d4\u54e1\u4f1a", "x": 40, "y": top_row_y, "w": 130, "h": top_h, "type": "primary"})
    edges.append({"x1": 170, "y1": top_row_y + top_h/2, "x2": 210, "y2": top_row_y + top_h/2, "arrow": False})
    nodes.append({"id": "npa", "label": "\u8b66\u5bdf\u5e81", "x": 210, "y": top_row_y, "w": 100, "h": top_h, "type": "highlight"})
    npa_mid_x = 210 + 100/2
    edges.append({"x1": 310, "y1": top_row_y + top_h/2, "x2": 350, "y2": top_row_y + top_h/2, "arrow": False})
    nodes.append({"id": "ig", "label": "\u7687\u5ba4\u8b66\u5bdf\u672c\u90e8", "x": 350, "y": top_row_y, "w": 100, "h": top_h, "type": "accent"})
    nodes.append({"id": "ig_note", "label": "\u25cf \u8b66\u8077\u6cd5\u306e\u6e96\u7528\u898f\u5b9a\u3092\u6574\u5099", "x": 455, "y": top_row_y, "w": 160, "h": top_h, "type": "note"})
    y_bot = top_row_y + top_h
    y = y_bot + 18  # small gap before divisions

    # Vertical line from NPA down to divisions
    edges.append({"x1": npa_mid_x, "y1": y_bot, "x2": npa_mid_x, "y2": y, "arrow": False})

    # --- Bureau division boxes ---
    div_y = y
    div_w = 155
    div_gap = 10
    div_start_x = 10
    div_header_h = 28

    x1 = div_start_x
    nodes.append({"id": "d1h", "label": "\u9577\u5b98\u5b98\u623f\u4ed6", "x": x1, "y": div_y, "w": div_w, "h": div_header_h, "type": "div-header"})

    x2 = div_start_x + div_w + div_gap
    nodes.append({"id": "d2h", "label": "\u5211\u4e8b\u5c40", "x": x2, "y": div_y, "w": div_w, "h": div_header_h, "type": "div-header-active"})
    dby2 = div_y + div_header_h + 1
    d2b_h = 195
    nodes.append({"id": "d2b", "label": "\u7d44\u7e54\u72af\u7f6a\u5bfe\u7b56\u90e8\n\u2190 \u66b4\u529b\u56e3\u5bfe\u7b56\u90e8\u3092\u6539\u7d44\n\n\u2022 \u66b4\u529b\u56e3\u5bfe\u7b56\n\u2022 \u85ac\u7269\u30fb\u9283\u5668\u5bfe\u7b56\n\u2022 \u6765\u65e5\u5916\u56fd\u4eba\u72af\u7f6a\u5bfe\u7b56\n\n\u2192 \u4e00\u4f53\u7684\u306b\u63a8\u9032\n\n\u4f01\u753b\u5206\u6790\u8ab2\n\u66b4\u529b\u56e3\u5bfe\u7b56\u8ab2\n\u85ac\u7269\u9283\u5668\u5bfe\u7b56\u8ab2\n\u56fd\u969b\u6355\u67fb\u7ba1\u7406\u5b98", "x": x2, "y": dby2, "w": div_w, "h": d2b_h, "type": "div-body-active"})

    x3 = div_start_x + 2 * (div_w + div_gap)
    nodes.append({"id": "d3h", "label": "\u8b66\u5099\u5c40", "x": x3, "y": div_y, "w": div_w, "h": div_header_h, "type": "div-header-active"})
    dby3 = div_y + div_header_h + 1
    d3b_h = 195
    nodes.append({"id": "d3b", "label": "\u5916\u4e8b\u60c5\u5831\u90e8\n\u2190 \u5b98\u623f\u56fd\u969b\u90e8\u3092\u6539\u7d44\n\n\u2022 \u5916\u56fd\u6cbb\u5b89\u6a5f\u95a2\u3068\u306e\n  \u30cf\u30a4\u30ec\u30d9\u30eb\u306e\u6298\u885d\n\u2022 \u7dca\u5bc6\u30fb\u8fc5\u901f\u306a\n  \u60c5\u5831\u4ea4\u63db\n\n\u2192 \u60c5\u5831\u53ce\u96c6\u306e\u5f37\u5316\n\n\u5916\u4e8b\u8ab2\n\u56fd\u969b\u30c6\u30ed\u30ea\u30ba\u30e0\u5bfe\u7b56\u8ab2", "x": x3, "y": dby3, "w": div_w, "h": d3b_h, "type": "div-body-active"})

    x4 = div_start_x + 3 * (div_w + div_gap)
    nodes.append({"id": "d4h", "label": "\u751f\u6d3b\u5b89\u5168\u5c40", "x": x4, "y": div_y, "w": div_w, "h": div_header_h, "type": "div-header-active"})
    dby4 = div_y + div_header_h + 1
    nodes.append({"id": "d4b", "label": "\u60c5\u5831\u6280\u8853\u72af\u7f6a\n\u5bfe\u7b56\u8ab2", "x": x4, "y": dby4, "w": div_w, "h": 40, "type": "div-body-active"})

    x5 = div_start_x + 4 * (div_w + div_gap)
    nodes.append({"id": "d5h", "label": "\u60c5\u5831\u901a\u4fe1\u5c40", "x": x5, "y": div_y, "w": div_w, "h": div_header_h, "type": "div-header-active"})
    dby5 = div_y + div_header_h + 1
    nodes.append({"id": "d5b", "label": "\u90fd\u9053\u5e9c\u770c\n\u60c5\u5831\u901a\u4fe1\u90e8", "x": x5, "y": dby5, "w": div_w, "h": 40, "type": "div-body-active"})

    # Calculate bottom of tallest division column
    div_bottom = max(dby2 + d2b_h, dby3 + d3b_h)
    y = div_bottom + gap

    # === Chart 2: National Security Responsibility ===
    sec2_y = y
    nodes.append({"id": "sec2", "label": "\u2461 \u56fd\u306e\u6cbb\u5b89\u8cac\u4efb", "x": 0, "y": sec2_y, "w": 200, "h": 20, "type": "section-title"})
    y = sec2_y + 20 + 10

    sr_y = y
    sr_w = 140
    sr_h = 40
    sr_gap = 8
    sr_start = 10

    nodes.append({"id": "s1", "label": "\u91cd\u5927\u30c6\u30ed\u4e8b\u6848\u306b\n\u5bfe\u3059\u308b\u8b66\u5bdf\u904b\u55b6", "x": sr_start, "y": sr_y, "w": sr_w, "h": sr_h, "type": "sec-box"})
    nodes.append({"id": "s2", "label": "\u56fd\u5916\u306b\u304a\u3051\u308b\n\u65e5\u672c\u4eba\u88ab\u5bb3\u306e\n\u30c6\u30ed\u4e8b\u6848\u306e\u5bfe\u51e6", "x": sr_start + sr_w + sr_gap, "y": sr_y, "w": sr_w, "h": sr_h, "type": "sec-box"})
    nodes.append({"id": "s3", "label": "\u5916\u56fd\u306e\u8b66\u5bdf\u884c\u653f\n\u6a5f\u95a2\u7b49\u3068\u306e\u9023\u7d61", "x": sr_start + 2*(sr_w + sr_gap), "y": sr_y, "w": sr_w, "h": sr_h, "type": "sec-box"})
    nodes.append({"id": "s4", "label": "\u30b5\u30a4\u30d0\u30fc\u72af\u7f6a\n\u6355\u67fb\u3078\u306e\u6280\u8853\u652f\u63f4", "x": sr_start + 3*(sr_w + sr_gap), "y": sr_y, "w": sr_w, "h": sr_h, "type": "sec-box"})
    y = sr_y + sr_h + 14

    mid_y = y
    mid_h = 36
    nodes.append({"id": "smid", "label": "\u8b66\u5bdf\u5e81\u306e\u30a4\u30cb\u30b7\u30a2\u30c6\u30a3\u30d6\u3092\u5f37\u5316\u3057\u3001\n\u56fd\u306e\u6cbb\u5b89\u8cac\u4efb\u3092\u660e\u78ba\u5316", "x": 60, "y": mid_y, "w": W - 120, "h": mid_h, "type": "highlight"})
    y_bot = mid_y + mid_h; y = y_bot + gap
    edges.append({"x1": W/2, "y1": y_bot, "x2": W/2, "y2": y})

    resp_y = y
    resp_h = 30
    nodes.append({"id": "sresp", "label": "\u90fd\u9053\u5e9c\u770c\u8b66\u5bdf \u2192 \u5bfe\u51e6", "x": 150, "y": resp_y, "w": W - 300, "h": resp_h, "type": "primary"})
    y_bot = resp_y + resp_h; y = y_bot + 18
    edges.append({"x1": W/2, "y1": y_bot, "x2": W/2, "y2": y, "arrow": False})

    br_y = y
    br_w = 140
    br_h = 36

    nodes.append({"id": "r1", "label": "\u7206\u5f3e\u30c6\u30ed\nNBC\u30c6\u30ed", "x": sr_start, "y": br_y, "w": br_w, "h": br_h, "type": "sec-result"})
    nodes.append({"id": "r2", "label": "\u56fd\u5916\u30c6\u30ed\n\u4e8b\u6848", "x": sr_start + br_w + sr_gap, "y": br_y, "w": br_w, "h": br_h, "type": "sec-result"})
    nodes.append({"id": "r3", "label": "\u56fd\u969b\u7d44\u7e54\n\u72af\u7f6a", "x": sr_start + 2*(br_w + sr_gap), "y": br_y, "w": br_w, "h": br_h, "type": "sec-result"})
    nodes.append({"id": "r4", "label": "\u30b5\u30a4\u30d0\u30fc\n\u72af\u7f6a", "x": sr_start + 3*(br_w + sr_gap), "y": br_y, "w": br_w, "h": br_h, "type": "sec-result"})

    total_h = br_y + br_h + 16

    chart_data = {
        "width": W,
        "height": total_h,
        "nodes": nodes,
        "edges": edges,
    }

    return _chart_html(
        "chart-p21-jp",
        "\u8b66\u5bdf\u6cd5\u306e\u4e00\u90e8\u3092\u6539\u6b63\u3059\u308b\u6cd5\u5f8b\u306e\u6982\u8981",
        chart_data,
    )
