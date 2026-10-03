# Generates a before/after crown comparison SVG from R3 panel-grid rings (A/D) and R2 outlines.
# Crown formulas follow source-r1/docs/07-mat-dung-crown.md (current) and the REV proposals (after).
import csv, math, os
from collections import defaultdict

BASE = r"c:\Users\tumin\Downloads\HOI_LUU_R5_BO_HO_SO_BAN_GIAO\HOI_LUU_R5_BO_HO_SO_BAN_GIAO\03_DU_LIEU_KIEM_SOAT"
OUT = r"c:\Users\tumin\Downloads\HOI_LUU_R5_BO_HO_SO_BAN_GIAO\danh_gia_crown\\REV-C_crown_truoc_sau.svg"

rings = defaultdict(dict)
with open(os.path.join(BASE, "panel-grid-AD-R3.csv"), encoding="utf-8-sig") as f:
    for x in csv.DictReader(f):
        rings[(x["tower"], int(x["ring_index"]))][int(x["panel_node_index"])] = (
            float(x["u_local_m"]), float(x["v_local_m"]), float(x["z_m"]))

def ring_list(t):
    idx = sorted(k[1] for k in rings if k[0] == t)
    return [[rings[(t, i)][n] for n in sorted(rings[(t, i)])] for i in idx]

RA, RD = ring_list("A"), ring_list("D")
RIB_NODES = {"A": [9, 31, 49, 71, 89, 111, 129, 151], "D": [7, 22, 34, 49, 63, 78, 90, 105]}

def ang(p):
    return math.atan2(p[1], p[0]) % (2 * math.pi)

def crown_surface(R, ztop_fn, c, nu=24):
    """Return grid[u_i][node] = (x, y, z) using S(u) contraction + Hermite tangent term."""
    roof, prev = R[-1], R[-2]
    z0 = roof[0][2]
    dz = z0 - prev[0][2]
    grid = []
    for k in range(nu + 1):
        u = k / nu
        S = 1 - c * (3 * u * u - 2 * u ** 3)
        h = u ** 3 - 2 * u * u + u
        row = []
        for p, q in zip(roof, prev):
            th = ang(p)
            H = ztop_fn(th) - z0
            Tx, Ty = (p[0] - q[0]) / dz, (p[1] - q[1]) / dz
            row.append((S * p[0] + h * H * Tx, S * p[1] + h * H * Ty, z0 + u * H))
        grid.append(row)
    return grid

def interp_on_row(row, phi):
    """Point on a crown row at polar angle phi (linear between nodes)."""
    n = len(row)
    angs = [ang(p) for p in row]
    for i in range(n):
        a0, a1 = angs[i], angs[(i + 1) % n]
        span = (a1 - a0) % (2 * math.pi)
        d = (phi - a0) % (2 * math.pi)
        if d <= span + 1e-9:
            t = d / span if span else 0
            p, q = row[i], row[(i + 1) % n]
            return tuple(p[j] + t * (q[j] - p[j]) for j in range(3))
    return row[0]

# ---------- crown definitions ----------
A_now = dict(z=lambda th: 478.5 + 1.5 * math.cos(4 * th), c=0.12)
A_new = dict(z=lambda th: 466.0 + 14.0 * abs(math.cos(2 * th)) ** 1.5, c=0.22)
TH_A = math.atan2(49 - 104, 53 - 238)  # direction D -> A, ~196.6 deg
D_now = dict(z=lambda th: 281.5 + 3.5 * math.cos(th), c=0.035)
D_new = dict(z=lambda th: 280.5 + 4.5 * math.cos(th - TH_A), c=0.10)

# ---------- SVG helpers ----------
els = []
def poly(pts, stroke="#333", w=1.0, fill="none", op=1.0, dash=None):
    d = " ".join("%.1f,%.1f" % p for p in pts)
    extra = ' stroke-dasharray="%s"' % dash if dash else ""
    els.append('<polyline points="%s" fill="%s" stroke="%s" stroke-width="%.2f" opacity="%.2f"%s stroke-linejoin="round"/>' % (d, fill, stroke, w, op, extra))
def polygon(pts, fill, op=1.0, stroke="none", w=0):
    d = " ".join("%.1f,%.1f" % p for p in pts)
    els.append('<polygon points="%s" fill="%s" opacity="%.2f" stroke="%s" stroke-width="%.2f"/>' % (d, fill, op, stroke, w))
def text(x, y, s, size=12, anchor="start", color="#222", weight="normal"):
    els.append('<text x="%.1f" y="%.1f" font-size="%d" text-anchor="%s" fill="%s" font-weight="%s" font-family="Segoe UI, Arial, sans-serif">%s</text>' % (x, y, size, anchor, color, weight, s))
def line(x1, y1, x2, y2, stroke="#bbb", w=0.6, dash=None):
    extra = ' stroke-dasharray="%s"' % dash if dash else ""
    els.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%.2f"%s/>' % (x1, y1, x2, y2, stroke, w, extra))

def panel_A(ox, oy, spec, title, proposed):
    sc = 5.2  # px per m
    zmin, zmax = 400.0, 484.0
    X = lambda x: ox + 175 + x * sc
    Y = lambda z: oy + (zmax - z) * sc
    text(ox, oy - 14, title, 14, weight="bold")
    for zz in (410.4, 452.4, 466, 480):
        line(ox + 10, Y(zz), ox + 345, Y(zz), dash="3,3")
        text(ox + 6, Y(zz) + 4, "+%.1f" % zz, 10, "end", "#666")
    # body: rings z>=zmin, silhouette + glass fill
    body = [r for r in RA if r[0][2] >= zmin - 5]
    left = [(X(min(p[0] for p in r)), Y(r[0][2])) for r in body]
    right = [(X(max(p[0] for p in r)), Y(r[0][2])) for r in body]
    polygon(left + right[::-1], "#8aa7b0", 0.85)
    # body ribs (front half: v<0)
    for n in RIB_NODES["A"]:
        pts = [(X(r[n][0]), Y(r[n][2])) for r in body if r[n][1] < 0]
        if len(pts) > 1:
            w = 0.65 * sc if not proposed else [0.65 * sc, 1.9 * sc]
            if proposed:
                # rib deepens/widens through transition zone A90-A98
                seg = [(X(r[n][0]), Y(r[n][2]), r[n][2]) for r in body if r[n][1] < 0]
                for a, b in zip(seg, seg[1:]):
                    t = max(0.0, min(1.0, (a[2] - 410.4) / (452.4 - 410.4)))
                    poly([(a[0], a[1]), (b[0], b[1])], "#d8d2c2", 0.65 * sc + t * 1.25 * sc)
            else:
                poly(pts, "#e3e6e6", w)
    # proposed: secondary fins emerge from A90 on every 5th node (continuous with crown fins)
    if proposed:
        for n in range(4, 160, 5):
            seg = [(X(r[n][0]), Y(r[n][2])) for r in body if r[n][1] < 0 and r[n][2] >= 410.4]
            if len(seg) > 1:
                poly(seg, "#f4f6f6", 1.1, op=0.9)
    grid = crown_surface(RA, spec["z"], spec["c"])
    # crown back half fill (lantern glow)
    top = grid[-1]
    xs_rows = [(min(p[0] for p in row), max(p[0] for p in row), row[0]) for row in grid]
    # silhouette via per-node max z vs x: sample columns
    sil = []
    for k in range(-34, 35):
        xk = k * 1.0
        best = None
        for row in grid:
            for p in row:
                if abs(p[0] - xk) < 1.05:
                    best = p[2] if best is None else max(best, p[2])
        if best is not None:
            sil.append((X(xk), Y(best)))
    base_l = (X(min(p[0] for p in grid[0])), Y(452.4))
    base_r = (X(max(p[0] for p in grid[0])), Y(452.4))
    polygon([base_l] + sil + [base_r], "#f3efe6" if proposed else "#eceeee", 0.9, "#9aa3a6", 0.8)
    # inner equipment screen (inset) as darker band
    scr_top = 462.0 if proposed else 474.0
    polygon([(X(-20), Y(452.4)), (X(-20), Y(scr_top)), (X(20), Y(scr_top)), (X(20), Y(452.4))], "#b8c0c2" if not proposed else "#e9d9b0", 0.55)
    # rim front + back
    rim_front = sorted([p for p in top if p[1] < 0], key=lambda p: p[0])
    rim_back = sorted([p for p in top if p[1] >= 0], key=lambda p: p[0])
    poly([(X(p[0]), Y(p[2])) for p in rim_back], "#9aa3a6", 0.8, op=0.6, dash="2,2")
    poly([(X(p[0]), Y(p[2])) for p in rim_front], "#6d777a", 1.4)
    # crown fins
    if proposed:
        fin_nodes = list(range(4, 160, 5))
        for n in fin_nodes:
            pts = [row[n] for row in grid]
            if pts[0][1] < 0:
                poly([(X(p[0]), Y(p[2])) for p in pts], "#8c8f86", 0.9, op=0.9)
    else:
        for k in range(32):
            phi = math.radians(5.625 + 11.25 * k)
            pts = [interp_on_row(row, phi) for row in grid]
            if pts[0][1] < 0:
                poly([(X(p[0]), Y(p[2])) for p in pts], "#a4abad", 0.6)
    # major ribs in crown
    for n in RIB_NODES["A"]:
        th = ang(RA[-1][n])
        if proposed:
            g = round(th / (math.pi / 2)) * (math.pi / 2)
            pts = []
            nu = len(grid) - 1
            for k, row in enumerate(grid):
                u = k / nu
                s = 3 * u * u - 2 * u ** 3
                phi = g + (th - g) * (1 - 0.85 * s)
                pts.append(interp_on_row(row, phi % (2 * math.pi)))
        else:
            pts = [row[n] for row in grid]
        if pts[0][1] < 0:
            poly([(X(p[0]), Y(p[2])) for p in pts], "#5f6a6d" if proposed else "#c9cdcd", 3.4 * (1.9 if proposed else 0.65), op=0.95)
    return X, Y

def panel_D(ox, oy, spec, title, proposed):
    sc = 5.2
    zmin, zmax = 236.0, 288.0
    X = lambda x: ox + 170 + x * sc
    Y = lambda z: oy + (zmax - z) * sc
    text(ox, oy - 14, title, 14, weight="bold")
    for zz in (269.45, 276, 278, 285):
        line(ox + 10, Y(zz), ox + 330, Y(zz), dash="3,3")
        text(ox + 6, Y(zz) + 4, "+%.2f" % zz if zz == 269.45 else "+%d" % zz, 10, "end", "#666")
    body = [r for r in RD if r[0][2] >= zmin]
    left = [(X(min(p[0] for p in r)), Y(r[0][2])) for r in body]
    right = [(X(max(p[0] for p in r)), Y(r[0][2])) for r in body]
    polygon(left + right[::-1], "#a3aaa2", 0.85)
    # hotel piers every 4 nodes (front)
    for n in range(0, 112, 4):
        pts = [(X(r[n][0]), Y(r[n][2])) for r in body if r[n][1] < 0]
        if len(pts) > 1:
            poly(pts, "#cdb996", 1.0, op=0.8)
    grid = crown_surface(RD, spec["z"], spec["c"])
    sil = []
    for k in range(-30, 31):
        xk = k * 1.0
        best = None
        for row in grid:
            for p in row:
                if abs(p[0] - xk) < 1.05:
                    best = p[2] if best is None else max(best, p[2])
        if best is not None:
            sil.append((X(xk), Y(best)))
    base_l = (X(min(p[0] for p in grid[0])), Y(269.45))
    base_r = (X(max(p[0] for p in grid[0])), Y(269.45))
    polygon([base_l] + sil + [base_r], "#f1e7d2" if proposed else "#ecebe6", 0.9, "#b09a74", 0.8)
    top = grid[-1]
    poly([(X(p[0]), Y(p[2])) for p in sorted([p for p in top if p[1] >= 0], key=lambda p: p[0])], "#b09a74", 0.8, op=0.6, dash="2,2")
    poly([(X(p[0]), Y(p[2])) for p in sorted([p for p in top if p[1] < 0], key=lambda p: p[0])], "#8a7550", 1.4)
    if proposed:
        for n in range(0, 112, 4):
            pts = [row[n] for row in grid]
            if pts[0][1] < 0:
                poly([(X(p[0]), Y(p[2])) for p in pts], "#b39a6a", 1.0)
    else:
        for k in range(16):
            phi = math.radians(11.25 + 22.5 * k)
            pts = [interp_on_row(row, phi) for row in grid]
            if pts[0][1] < 0:
                poly([(X(p[0]), Y(p[2])) for p in pts], "#c2b08c", 0.6)
    for n in RIB_NODES["D"]:
        pts = [row[n] for row in grid]
        if pts[0][1] < 0:
            poly([(X(p[0]), Y(p[2])) for p in pts], "#8a7550" if proposed else "#c9b99a", 2.0 if proposed else 1.4)
    # arrow toward A
    ax = X(-30) - 6
    text(ax, Y(287) , "← phía A (−X)", 10, "start", "#555")

def skyline(ox, oy, specA, specD, title, proposed):
    sc = 0.92
    X = lambda x: ox + x * sc
    Y = lambda z: oy + (490 - z) * sc
    text(ox, oy - 12, title, 14, weight="bold")
    line(X(0), Y(0), X(300), Y(0), "#888", 0.8)
    for t, R, spec, cx, col in (("A", RA, specA, 53, "#8aa7b0"), ("D", RD, specD, 238, "#a3aaa2")):
        left = [(X(cx + min(p[0] for p in r)), Y(r[0][2])) for r in R]
        right = [(X(cx + max(p[0] for p in r)), Y(r[0][2])) for r in R]
        polygon(left + right[::-1], col, 0.9)
        grid = crown_surface(R, spec["z"], spec["c"], nu=12)
        sil = []
        span = 36 if t == "A" else 31
        for k in range(-span, span + 1):
            best = None
            for row in grid:
                for p in row:
                    if abs(p[0] - k) < 1.05:
                        best = p[2] if best is None else max(best, p[2])
            if best is not None:
                sil.append((X(cx + k), Y(best)))
        z0 = R[-1][0][2]
        polygon([(X(cx + min(p[0] for p in grid[0])), Y(z0))] + sil + [(X(cx + max(p[0] for p in grid[0])), Y(z0))], "#e9e2cf" if proposed else "#e6e8e8", 1.0, "#777", 0.6)
    for x0, x1 in ((94, 154), (134, 194)):
        polygon([(X(x0), Y(0)), (X(x0), Y(158.7)), (X(x1), Y(158.7)), (X(x1), Y(0))], "#b7c4c4", 0.55, "#7d8b8b", 0.6)
    for z, lab in ((480, "480"), (285, "285"), (158.7, "158,7")):
        text(X(300) + 4, Y(z) + 4, lab, 10, "start", "#666")
    # descending envelope A-apex -> D-high
    if proposed:
        line(X(53), Y(480), X(238 - 25), Y(285), "#c07a2c", 0.9, "5,4")

W, H = 1500, 1080
text(24, 34, "HỘI LƯU · Crown A/D trước và sau đề xuất (REV-C01…C05), dựng từ lưới R3 và công thức crown", 18, weight="bold")
text(24, 56, "Nhìn theo trục local −Y, cùng tỷ lệ 5,2 px/m cho crown. Silhouette tính từ vòng panel nguồn; gân/màu là sơ đồ, không phải tiết diện hoặc vật liệu.", 11, color="#555")
panel_A(60, 110, A_now, "A · hiện trạng R3  (Z = 478,5 + 1,5·cos4θ, co 12%)", False)
panel_A(430, 110, A_new, "A · đề xuất 'Hội lưu'  (Z = 466 + 14·|cos2θ|^1,5, co 22%)", True)
panel_D(830, 110, D_now, "D · hiện trạng  (281,5 + 3,5·cosθ, co 3,5%)", False)
panel_D(830, 440, D_new, "D · đề xuất  (280,5 + 4,5·cos(θ − θA), co 10%)", True)
skyline(60, 620, A_now, D_now, "Skyline trục X · hiện trạng", False)
skyline(430, 620, A_new, D_new, "Skyline trục X · đề xuất", True)
notes = [
    "Giữ nguyên: số tầng, biên sàn, mái A +452,40 / D +269,45, đỉnh 480 / 285, GFA.",
    "A: 8 gân chính hội tụ theo cặp về trục 4 rãnh; đỉnh 480 tại rãnh, góc hạ về +466; khe mở ~2,2 m ở đỉnh.",
    "A: vùng chuyển A90–A98 (+410,4 → +452,4): gân chính tăng bề rộng biểu kiến 0,65 → 1,9 m; gân phụ mỗi 5 nút lưới nổi dần.",
    "Gân phụ crown đặt theo chỉ số nút lưới (A mỗi 5 nút, D theo pier 4 nút) thay vì góc polar cố định.",
    "D: đỉnh cao quay về phía A (θA ≈ 196,6°), thấp +276 ở phía xa; co 10% cho đọc cùng họ với A.",
    "Nét cam: đường bao skyline hạ dần từ đỉnh A xuống đỉnh cao D.",
]
for i, s in enumerate(notes):
    text(830, 800 + i * 20, "• " + s, 11, color="#333")
svg = '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d"><rect width="100%%" height="100%%" fill="#ffffff"/>%s</svg>' % (W, H, W, H, "\n".join(els))
open(OUT, "w", encoding="utf-8").write(svg)
print("ok", len(svg))

