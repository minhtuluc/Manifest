"""Tower / crown elevation and plan renderers for the R6 drawings."""
import csv, json, math, os
import r6_geom as G
from r6_svg import view_axes, proj, depth

COL = dict(
    glassA="#8fa9b2", glassD="#a5ada6", ribA="#6b7477", ribD="#8a7550", finA="#8d9496", finD="#ab946b",
    bodyribA="#d5d3c9", bodyribD="#cdb98f", screenA="#e9e0cb", screenD="#efe3c8", r5="#c0782c",
    band="#a9bcc2", skylobby="#cddde2", accent="#44575c", bcglass="#9fb2b5", bcmetal="#e7e3d6",
    podium="#dcd6c8", night_bg="#14222b", night_body="#22333c",
)

CREST = {  # crown rib face at roof -> tip (m), fin face (m), rim (m)
    ("A", "R6"): (1.40, 0.90, 0.12, 0.30), ("A", "R5"): (0.65, 0.65, 0.08, 0.18),
    ("D", "R6"): (0.80, 0.55, 0.10, 0.24), ("D", "R5"): (0.36, 0.36, 0.06, 0.12),
}

AD_R3 = json.load(open(os.path.join(G.DATA, "facade-ad-r3.json"), encoding="utf-8"))


def load_podium():
    out = {}
    with open(os.path.join(G.DATA, "outline-vertices-AD-R2.csv"), encoding="utf-8-sig") as f:
        for x in csv.DictReader(f):
            fl = int(x["floor"])
            if fl <= 6:
                out.setdefault((x["tower"], fl), []).append((float(x["X_m"]), float(x["Y_m"]), float(x["z_m"])))
    return out


PODIUM = load_podium()


def ring_extent(ring, right):
    xs = [proj(p, right) for p in ring]
    return min(xs), max(xs)


def extent_at(t, z, right):
    R = G.RINGS[t]
    if z <= R[0][0][2]:
        return ring_extent(R[0], right)
    for a, b in zip(R, R[1:]):
        za, zb = a[0][2], b[0][2]
        if za <= z <= zb:
            s = (z - za) / (zb - za) if zb > za else 0.0
            l0, r0 = ring_extent(a, right)
            l1, r1 = ring_extent(b, right)
            return l0 + s * (l1 - l0), r0 + s * (r1 - r0)
    return ring_extent(R[-1], right)


def screen_rings(t, rev, grid, steps=6):
    sp = G.SPEC[rev][t]
    roof, top, nu = sp["roof"], sp["screen_top"], len(grid) - 1
    rings = []
    for k in range(steps + 1):
        z = roof + (top - roof) * k / steps
        ring = []
        for n in range(len(grid[0])):
            H = grid[-1][n][2] - roof
            u = min(1.0, (z - roof) / H) if H > 0 else 0.0
            f = u * nu
            k0 = min(int(f), nu - 1)
            s = f - k0
            p = [grid[k0][n][j] + s * (grid[k0 + 1][n][j] - grid[k0][n][j]) for j in range(3)]
            r = math.hypot(p[0], p[1])
            sc = max(0.0, 1 - sp["screen_inset"] / r)
            ring.append((p[0] * sc, p[1] * sc, z))
        rings.append(ring)
    return rings


def split_by_side(pts, d, off=(0.0, 0.0)):
    """Split a 3D polyline into runs of front (True) / back (False) segments."""
    runs = []
    for a, b in zip(pts, pts[1:]):
        mid = ((a[0] + b[0]) / 2 + off[0], (a[1] + b[1]) / 2 + off[1])
        side = depth(mid, d) < 0
        if runs and runs[-1][0] == side:
            runs[-1][1].append(b)
        else:
            runs.append([side, [a, b]])
    return runs


def r5_fins(t, grid):
    key = "crown_secondary_angles_deg"
    angs = AD_R3[t][key]
    return [[G.on_row(row, math.radians(a)) for row in grid] for a in angs]


def crown_members(t, rev):
    grid = G.crown_grid(t, rev)
    ribs = [G.rib_path(t, n, grid, rev) for n in G.RIB_NODES[t]]
    if rev == "R6":
        fins = [G.fin_path(t, n, grid, rev)[0] for n in G.FIN_NODES[t]]
        rims = G.rim_segments(t, grid, rev)
    else:
        fins = r5_fins(t, grid)
        rims = [grid[-1] + [grid[-1][0]]]
    return grid, ribs, fins, rims


def draw_crown(svg, t, rev, beta, X, Y, sc, night=False, back=True, screen=True, wmul=1.0, off=(0.0, 0.0)):
    """Draw crown in an elevation. X() takes horizontal metres (local, already projected), Y() takes Z."""
    right, d = view_axes(beta)
    grid, ribs, fins, rims = crown_members(t, rev)
    rf0, rf1, ff, rim_w = CREST[(t, rev)]
    ribc = COL["rib" + t] if not night else ("#ffe6b3" if t == "A" else "#ffd9a0")
    finc = COL["fin" + t] if not night else ("#f1d7a2" if t == "A" else "#ebc98f")
    backc = "#b9bebe" if not night else "#5d6a70"
    P = lambda p: (X(proj(p, right)), Y(p[2]))
    fronts, backs = [], []
    nu = len(grid) - 1
    for pts in fins:
        for side, run in split_by_side(pts, d, off):
            (fronts if side else backs).append(([P(p) for p in run], finc, max(0.7, ff * sc) * wmul, 0.95))
    for seg in rims:
        for side, run in split_by_side(seg, d, off):
            (fronts if side else backs).append(([P(p) for p in run], ribc, max(0.9, rim_w * sc) * wmul, 1.0))
    rib_front = []
    for pts in ribs:
        for i, (a, b) in enumerate(zip(pts, pts[1:])):
            u = (i + 0.5) / nu
            w = (rf0 + (rf1 - rf0) * u) * sc * wmul
            mid = ((a[0] + b[0]) / 2 + off[0], (a[1] + b[1]) / 2 + off[1])
            if depth(mid, d) < 0:
                rib_front.append(([P(a), P(b)], ribc, max(1.0, w), 1.0))
            else:
                backs.append(([P(a), P(b)], backc, max(0.8, w * 0.6), 0.8))
    if back:
        for pts, c, w, op in backs:
            svg.poly(pts, backc, max(0.5, w * 0.7), op=0.55 if not night else 0.5)
    if screen:
        sr = screen_rings(t, rev, grid)
        left = [(X(ring_extent(r, right)[0]), Y(r[0][2])) for r in sr]
        rgt = [(X(ring_extent(r, right)[1]), Y(r[0][2])) for r in sr]
        if night:
            svg.polygon(left + rgt[::-1], "#ffd79a" if t == "A" else "#ffcf8a", 0.42, extra=' filter="url(#glow)"')
        else:
            svg.polygon(left + rgt[::-1], COL["screen" + t] if rev == "R6" else "#c3c9ca", 0.9, "#b7ad97", 0.4)
    for pts, c, w, op in fronts:
        svg.poly(pts, c, w, op=op)
    for pts, c, w, op in rib_front:
        svg.poly(pts, c, w, op=op, cap="butt")
    if night and rev == "R6":
        # apex slots: brightest element
        for n, (th, axis) in G.rib_axes(t, rev).items():
            pass
        tops = {}
        for n, pts in zip(G.RIB_NODES[t], ribs):
            th, axis = G.rib_axes(t, rev)[n]
            if axis is not None:
                tops.setdefault(round(axis, 5), []).append(pts)
        for ax, pair in tops.items():
            if len(pair) == 2:
                k0 = int(nu * 0.78)
                mid_top = [((pair[0][k][0] + pair[1][k][0]) / 2, (pair[0][k][1] + pair[1][k][1]) / 2, (pair[0][k][2] + pair[1][k][2]) / 2)
                           for k in range(k0, nu + 1)]
                m = mid_top[-1]
                if depth((m[0] + off[0], m[1] + off[1]), d) < 0:
                    svg.poly([P(p) for p in mid_top], "#fff4d6", max(2.0, 1.2 * sc) * wmul, op=0.95, extra=' filter="url(#glow)"')
    return grid


def draw_body(svg, t, beta, X, Y, sc, rev="R6", zmin=0.0, mullions=True, night=False, podium=True, off=(0.0, 0.0)):
    right, d = view_axes(beta)
    R = [r for r in G.RINGS[t] if r[0][2] >= zmin - 8]
    glass = COL["glass" + t] if not night else COL["night_body"]
    if podium and zmin < 34:
        for fl in range(1, 7):
            pts = PODIUM[(t, fl)]
            cx, cy = G.CENTER[t]
            xs = [proj((p[0] - cx, p[1] - cy), right) for p in pts]
            z0 = pts[0][2]
            h = G.FLOORS[(t, fl)]["h"]
            svg.rect(X(min(xs)), Y(z0 + h), (max(xs) - min(xs)) * sc, h * sc,
                     COL["podium"] if not night else "#2c3b42", 1.0, "#b9b2a2" if not night else "#3a4a52", 0.5)
            if night and fl == 1:
                svg.rect(X(min(xs)), Y(z0 + h), (max(xs) - min(xs)) * sc, h * sc, "#ffd9a0", 0.35)
    left = [(X(ring_extent(r, right)[0]), Y(r[0][2])) for r in R]
    rgt = [(X(ring_extent(r, right)[1]), Y(r[0][2])) for r in R]
    svg.polygon(left + rgt[::-1], glass, 0.95)
    # bands
    for kind in ("technical", "skylobby"):
        for fl in G.BANDS[t][kind]:
            f = G.FLOORS[(t, fl)]
            if f["top"] < zmin:
                continue
            l0, r0 = extent_at(t, f["z"], right)
            l1, r1 = extent_at(t, f["top"], right)
            poly = [(X(l0), Y(f["z"])), (X(r0), Y(f["z"])), (X(r1), Y(f["top"])), (X(l1), Y(f["top"]))]
            if night:
                if kind == "skylobby":
                    svg.polygon(poly, "#ffd9a0", 0.22)
                continue
            if t == "D" and fl == 35:
                # D35 inset glass: retained as the one intended shadow band
                svg.polygon(poly, COL["accent"], 0.95)
            elif rev == "R5":
                svg.polygon(poly, "#6f858c" if kind == "technical" else "#7d9197", 0.75)
            else:
                svg.polygon(poly, COL["band"] if kind == "technical" else COL["skylobby"], 0.55)
    # mullions (front half only)
    N = len(R[-1])
    if mullions:
        step = 1 if sc >= 4 else 2
        for n in range(0, N, step):
            pts = [(X(proj(r[n], right)), Y(r[n][2])) for r in R
                   if depth((r[n][0] + off[0], r[n][1] + off[1]), d) < 0]
            if len(pts) > 1:
                svg.poly(pts, "#b9cbd0" if not night else "#2d4049", 0.35, op=0.8)
    # transition fins (R6)
    if rev == "R6":
        z0 = G.TRANSITION[t]["z0"]
        for n in G.FIN_NODES[t]:
            pts = [(X(proj(r[n], right)), Y(r[n][2])) for r in R
                   if r[n][2] >= z0 - 1e-6 and depth((r[n][0] + off[0], r[n][1] + off[1]), d) < 0]
            if len(pts) > 1:
                svg.poly(pts, COL["fin" + t] if not night else "#d9bd86", max(0.8, 0.10 * sc), op=0.9 if not night else 0.6)
    # major ribs
    for n in G.RIB_NODES[t]:
        for a, b in zip(R, R[1:]):
            pa, pb = a[n], b[n]
            if depth(((pa[0] + pb[0]) / 2 + off[0], (pa[1] + pb[1]) / 2 + off[1]), d) >= 0:
                continue
            face, projm = G.rib_face_projection(t, (pa[2] + pb[2]) / 2, rev)
            col = COL["bodyrib" + t]
            opc = 1.0
            if night:
                zt = G.TRANSITION[t]["z0"] if rev == "R6" else G.SPEC[rev][t]["roof"] - 20
                s = max(0.0, min(1.0, ((pa[2] + pb[2]) / 2 - zt) / (G.SPEC[rev][t]["roof"] - zt)))
                if s <= 0:
                    col, opc = "#3a4d56", 0.8
                else:
                    col, opc = "#ffe2a8", 0.25 + 0.7 * s
            svg.poly([(X(proj(pa, right)), Y(pa[2])), (X(proj(pb, right)), Y(pb[2]))], col, max(0.9, face * sc), op=opc, cap="butt")
    return right, d


def draw_plan_crown(svg, t, X, Y, sc, rev="R6", compare=True):
    grid, ribs, fins, rims = crown_members(t, rev)
    P = lambda p: (X(p[0]), Y(p[1]))
    roof = G.RINGS[t][-1]
    svg.polygon([P(p) for p in roof], COL["glass" + t], 0.35, "#6d7f86", 0.8)
    sr = screen_rings(t, rev, grid)
    svg.polygon([P(p) for p in sr[-1]], COL["screen" + t], 0.8, "#b7ad97", 0.6)
    for pts in fins:
        svg.poly([P(p) for p in pts], COL["fin" + t], 0.9)
    for seg in rims:
        svg.poly([P(p) for p in seg], COL["rib" + t], 1.4)
    rf0, rf1, ff, rim_w = CREST[(t, rev)]
    for pts in ribs:
        svg.poly([P(p) for p in pts], COL["rib" + t], max(1.5, rf0 * sc * 0.6))
    if compare:
        g5 = G.crown_grid(t, "R5")
        svg.poly([P(p) for p in g5[-1] + [g5[-1][0]]], COL["r5"], 1.0, dash="4,3")
    return grid
