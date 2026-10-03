"""HOI LUU R6-CROWN - geometry kernel.

Reads the R3 panel rings (03_DU_LIEU_KIEM_SOAT/panel-grid-AD-R3.csv) and the R4 B/C facade JSON,
builds the R6 crown surfaces, ribs and fins for A/D, and the R6 B/C crown frame parameters.
Slab outlines, floor levels, roofs and GFA are NOT modified. Units m, Z-up, site X/Y.
"""
import csv, json, math, os

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(os.path.dirname(HERE))
DATA = os.path.join(PKG, "03_DU_LIEU_KIEM_SOAT")
TAU = 2 * math.pi


def smooth(u):
    return 3 * u * u - 2 * u ** 3


def ang(p):
    return math.atan2(p[1], p[0]) % TAU


def wrap(a):
    """Wrap angle to (-pi, pi]."""
    a = (a + math.pi) % TAU - math.pi
    return a


# --------------------------------------------------------------- source rings
def load_rings():
    rings = {}
    with open(os.path.join(DATA, "panel-grid-AD-R3.csv"), encoding="utf-8-sig") as f:
        for x in csv.DictReader(f):
            key = (x["tower"], int(x["ring_index"]))
            rings.setdefault(key, {})[int(x["panel_node_index"])] = (
                float(x["u_local_m"]), float(x["v_local_m"]), float(x["z_m"]))
    out = {}
    for t in ("A", "D"):
        idx = sorted(k[1] for k in rings if k[0] == t)
        out[t] = [[rings[(t, i)][n] for n in sorted(rings[(t, i)])] for i in idx]
    return out


def load_floors():
    fl = {}
    with open(os.path.join(DATA, "floor-schedule-AD-R2.csv"), encoding="utf-8-sig") as f:
        for x in csv.DictReader(f):
            fl[(x["tower"], int(x["floor"]))] = dict(z=float(x["z_m"]), h=float(x["height_m"]),
                                                     top=float(x["top_m"]), kind=x["kind"], program=x["program"])
    return fl


def load_bc():
    return json.load(open(os.path.join(DATA, "facade-bc-r4.json"), encoding="utf-8"))


RINGS = load_rings()
FLOORS = load_floors()
BC = load_bc()

SECTOR_COUNTS = {"A": [9, 11, 11, 9] * 4, "D": [7, 8, 7, 6, 6, 7, 8, 7] * 2}
CENTER = {"A": (53.0, 49.0), "D": (238.0, 104.0)}


def sector_starts(t):
    s, out = 0, []
    for n in SECTOR_COUNTS[t]:
        out.append((s, n))
        s += n
    return out


RIB_NODES = {t: [s for i, (s, n) in enumerate(sector_starts(t)) if i % 2 == 1] for t in ("A", "D")}


def a_fin_nodes():
    nodes = []
    for s, n in sector_starts("A"):
        nodes += [s + round(n / 4), s + round(3 * n / 4)]
    return nodes


D_SLOT_AXIS, D_SLOT_HALF = math.pi, math.radians(22.5 * (1 - 0.85))  # open apex slot on the -X face


def d_fin_nodes():
    """Hotel piers every 4 nodes; drop piers within 1 node of a rib and any pier standing in the open apex slot."""
    ribs = RIB_NODES["D"]
    roof = RINGS["D"][-1]
    out = []
    for k in range(0, 112, 4):
        if min(abs(k - r) for r in ribs) <= 1:
            continue
        if abs(wrap(ang(roof[k]) - D_SLOT_AXIS)) < D_SLOT_HALF:
            continue
        out.append(k)
    return out


FIN_NODES = {"A": a_fin_nodes(), "D": d_fin_nodes()}
D_PIER_NODES = list(range(0, 112, 4))

# --------------------------------------------------------------- crown specs
SPEC = {
    "R6": {
        "A": dict(roof=452.40, c=0.30, conv=0.85, screen_inset=1.5, screen_top=470.0,
                  ztop=lambda th: 480.0 + 40.0 * abs(math.cos(2 * th)) ** 1.5,
                  ztop_text="Z_top(θ) = 480,00 + 40,00·|cos 2θ|^1,5",
                  converge={n: None for n in RIB_NODES["A"]}),  # None -> nearest k*90deg axis
        "D": dict(roof=269.45, c=0.15, conv=0.85, screen_inset=1.2, screen_top=282.0,
                  ztop=lambda th: 286.0 + 24.0 * ((1 + math.cos(th - math.pi)) / 2) ** 2,
                  ztop_text="Z_top(θ) = 286,00 + 24,00·((1 + cos(θ − 180°))/2)²",
                  converge={49: math.pi, 63: math.pi}),
    },
    "R5": {
        "A": dict(roof=452.40, c=0.12, conv=0.0, screen_inset=1.5, screen_top=474.0,
                  ztop=lambda th: 478.5 + 1.5 * math.cos(4 * th),
                  ztop_text="Z_top(θ) = 478,50 + 1,50·cos 4θ", converge={}),
        "D": dict(roof=269.45, c=0.035, conv=0.0, screen_inset=1.2, screen_top=276.0,
                  ztop=lambda th: 281.5 + 3.5 * math.cos(th),
                  ztop_text="Z_top(θ) = 281,50 + 3,50·cos θ", converge={}),
    },
}
NU = 24  # crown u-steps


def crown_grid(t, rev="R6", nu=NU):
    """grid[k][node] = (u_local, v_local, z) following the R1 Hermite rule with R6 parameters."""
    sp = SPEC[rev][t]
    R = RINGS[t]
    roof, prev = R[-1], R[-2]
    z0 = roof[0][2]
    dz = z0 - prev[0][2]
    grid = []
    for k in range(nu + 1):
        u = k / nu
        S = 1 - sp["c"] * smooth(u)
        h = u ** 3 - 2 * u * u + u
        row = []
        for p, q in zip(roof, prev):
            H = sp["ztop"](ang(p)) - z0
            Tx, Ty = (p[0] - q[0]) / dz, (p[1] - q[1]) / dz
            row.append((S * p[0] + h * H * Tx, S * p[1] + h * H * Ty, z0 + u * H))
        grid.append(row)
    return grid


def on_row(row, phi):
    """Point on a crown row at polar angle phi (linear between nodes)."""
    n = len(row)
    angs = [ang(p) for p in row]
    for i in range(n):
        a0, a1 = angs[i], angs[(i + 1) % n]
        span = (a1 - a0) % TAU
        d = (phi - a0) % TAU
        if d <= span + 1e-12:
            s = d / span if span else 0.0
            p, q = row[i], row[(i + 1) % n]
            return tuple(p[j] + s * (q[j] - p[j]) for j in range(3))
    return row[0]


def rib_axes(t, rev="R6"):
    """Return {rib_node: (theta_r, theta_axis or None)}."""
    sp = SPEC[rev][t]
    roof = RINGS[t][-1]
    out = {}
    for n in RIB_NODES[t]:
        th = ang(roof[n])
        axis = None
        if n in sp["converge"]:
            axis = sp["converge"][n]
            if axis is None:
                axis = (round(th / (math.pi / 2)) * (math.pi / 2)) % TAU
        out[n] = (th, axis)
    return out


def rib_path(t, n, grid, rev="R6"):
    sp = SPEC[rev][t]
    th, axis = rib_axes(t, rev)[n]
    if axis is None:
        return [row[n] for row in grid]
    d = wrap(th - axis)
    pts = []
    nu = len(grid) - 1
    for k, row in enumerate(grid):
        phi = axis + d * (1 - sp["conv"] * smooth(k / nu))
        pts.append(on_row(row, phi % TAU))
    return pts


def inv_smooth(s):
    lo, hi = 0.0, 1.0
    for _ in range(60):
        m = (lo + hi) / 2
        if smooth(m) < s:
            lo = m
        else:
            hi = m
    return (lo + hi) / 2


def fin_path(t, n, grid, rev="R6"):
    """Fin follows its node column; if it lies inside a converging lancet it stops on the rib."""
    sp = SPEC[rev][t]
    roof = RINGS[t][-1]
    thf = ang(roof[n])
    u_stop, rib_hit = 1.0, None
    for rn, (th, axis) in rib_axes(t, rev).items():
        if axis is None:
            continue
        d = wrap(th - axis)
        df = wrap(thf - axis)
        if d == 0 or df * d <= 0:
            continue
        ratio = df / d
        if 0 < ratio < 1:
            s_need = (1 - ratio) / sp["conv"]
            if s_need < 1:
                u = inv_smooth(s_need)
                if u < u_stop:
                    u_stop, rib_hit = u, rn
    nu = len(grid) - 1
    pts = []
    for k, row in enumerate(grid):
        if k / nu <= u_stop + 1e-9:
            pts.append(row[n])
    if u_stop < 1.0:
        # close onto the rib at u_stop (interpolated)
        k0 = int(u_stop * nu)
        k1 = min(k0 + 1, nu)
        rp = rib_path(t, rib_hit, grid, rev)
        s = u_stop * nu - k0
        pts.append(tuple(rp[k0][j] + s * (rp[k1][j] - rp[k0][j]) for j in range(3)))
    return pts, u_stop


def rim_segments(t, grid, rev="R6"):
    """Top rim polyline(s) excluding the open apex slot between converging rib pairs."""
    sp = SPEC[rev][t]
    top = grid[-1]
    slots = []
    for rn, (th, axis) in rib_axes(t, rev).items():
        if axis is None:
            continue
        half = abs(wrap(th - axis)) * (1 - sp["conv"])
        slots.append((axis, half))
    keep = []
    for i, p in enumerate(top):
        a = ang(p)
        inside = any(abs(wrap(a - ax)) < half for ax, half in slots)
        keep.append(not inside)
    segs, cur = [], []
    n = len(top)
    start = keep.index(False) if False in keep else 0
    for j in range(n + 1):
        i = (start + j) % n
        if keep[i]:
            cur.append(top[i])
        else:
            if len(cur) > 1:
                segs.append(cur)
            cur = []
    if len(cur) > 1:
        segs.append(cur)
    return segs


def to_world(t, p):
    cx, cy = CENTER[t]
    return (cx + p[0], cy + p[1], p[2])


# --------------------------------------------------------------- body facade rules (R6)
def rib_face_projection(t, z, rev="R6"):
    """Major rib face width / projection vs Z for the tower body (m)."""
    if t == "A":
        z_base, z_roof = 34.0, 452.40
        if rev == "R5":
            s = (z - z_base) / (z_roof - z_base)
            return 1.05 - 0.40 * s, 0.75 - 0.30 * s
        zt = FLOORS[("A", 90)]["z"]
        if z <= zt:
            return 1.05, 0.75
        s = (z - zt) / (z_roof - zt)
        return 1.05 + 0.35 * s, 0.75 + 0.75 * s
    z_base, z_roof = 34.0, 269.45
    if rev == "R5":
        s = (z - z_base) / (z_roof - z_base)
        return 0.52 - 0.16 * s, 0.38 - 0.13 * s
    zt = FLOORS[("D", 56)]["z"]
    if z <= zt:
        return 0.52, 0.38
    s = (z - zt) / (z_roof - zt)
    return 0.52 + 0.28 * s, 0.38 + 0.42 * s


TRANSITION = {
    "A": dict(floors="A90–A98", z0=FLOORS[("A", 90)]["z"], z1=452.40),
    "D": dict(floors="D56–D62", z0=FLOORS[("D", 56)]["z"], z1=269.45),
}

BANDS = {
    "A": dict(technical=[31, 55, 79, 98], skylobby=[32, 56, 80]),
    "D": dict(technical=[20, 34, 48, 62], skylobby=[35]),
}


# --------------------------------------------------------------- metrics
def polyline_len_xy(pts):
    return sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pts, pts[1:]))


def metrics(t, rev="R6"):
    sp = SPEC[rev][t]
    g = crown_grid(t, rev)
    top = g[-1]
    zs = [p[2] for row in g for p in row]
    ribs = {n: rib_path(t, n, g, rev) for n in RIB_NODES[t]}
    rib_tip = max(p[-1][2] for p in ribs.values())
    rims = rim_segments(t, g, rev)
    rim_z = [p[2] for seg in rims for p in seg]
    fin_z = [q[2] for n in (FIN_NODES[t] if rev == "R6" else []) for q in fin_path(t, n, g, rev)[0]]
    m = dict(
        roof_z=sp["roof"],
        envelope_top_z=max(zs),
        rim_min_z=min(rim_z),
        rim_max_z=max(rim_z),
        rib_tip_max_z=rib_tip,
        architectural_top_z=max(rim_z + fin_z + [rib_tip]),
        top_ring_W=max(p[0] for p in top) - min(p[0] for p in top),
        top_ring_H=max(p[1] for p in top) - min(p[1] for p in top),
        roof_W=max(p[0] for p in g[0]) - min(p[0] for p in g[0]),
        roof_H=max(p[1] for p in g[0]) - min(p[1] for p in g[0]),
    )
    m["crown_height_max"] = m["architectural_top_z"] - sp["roof"]
    m["crown_height_min"] = m["rim_min_z"] - sp["roof"]
    m["crown_share_of_height"] = m["crown_height_max"] / m["architectural_top_z"]
    occ_top = FLOORS[(t, 97)]["top"] if t == "A" else FLOORS[(t, 61)]["top"]
    m["highest_occupiable_top_z"] = occ_top
    m["vanity_height"] = m["architectural_top_z"] - occ_top
    m["vanity_share"] = m["vanity_height"] / m["architectural_top_z"]
    tz = TRANSITION[t]["z0"]
    m["top_zone_height"] = m["architectural_top_z"] - tz if rev == "R6" else m["crown_height_max"]
    m["top_zone_share"] = m["top_zone_height"] / m["architectural_top_z"]
    # slot width and lean for converging pairs
    pairs = {}
    for n, (th, axis) in rib_axes(t, rev).items():
        if axis is not None:
            pairs.setdefault(round(axis, 6), []).append(n)
    slots, leans = [], []
    for ax, ns in pairs.items():
        if len(ns) == 2:
            a, b = ribs[ns[0]][-1], ribs[ns[1]][-1]
            slots.append(math.dist(a[:2], b[:2]))
        for n in ns:
            p = ribs[n]
            leans.append(math.degrees(math.atan2(polyline_len_xy(p), p[-1][2] - p[0][2])))
    m["apex_slot_width"] = min(slots) if slots else None
    m["rib_mean_lean_deg"] = sum(leans) / len(leans) if leans else 0.0
    # fins
    fins = [fin_path(t, n, g, rev) for n in FIN_NODES[t]] if rev == "R6" else []
    m["fins_total"] = len(fins)
    m["fins_terminating_on_ribs"] = sum(1 for _, u in fins if u < 1.0)
    return m


def fin_offset_check(t):
    """Max distance between R6 crown fins and body mullion nodes at roof ring (should be 0)."""
    roof = RINGS[t][-1]
    g = crown_grid(t)
    return max(math.dist(roof[n][:2], g[0][n][:2]) for n in FIN_NODES[t])


def frit_share_A():
    """Share of A97 perimeter occupied by the graded-frit flank panels (1 panel each side of 8 ribs)."""
    fl = FLOORS[("A", 97)]["z"]
    R = RINGS["A"]
    ring = min(R, key=lambda r: abs(r[0][2] - fl))
    n = len(ring)
    per = sum(math.dist(ring[i][:2], ring[(i + 1) % n][:2]) for i in range(n))
    flank = 0.0
    for r in RIB_NODES["A"]:
        flank += math.dist(ring[r - 1][:2], ring[r][:2]) + math.dist(ring[r][:2], ring[(r + 1) % n][:2])
    return per, flank, flank / per


# --------------------------------------------------------------- B/C R6
BC_R6 = dict(
    roof_z=154.20,
    crown_top_z=159.90,
    brief_limit_z=160.00,
    corner_rib_top_z=[159.90] * 8,
    frame=dict(fin_face_m=0.055, fin_depth_m=0.45, fin_positions="every mullion of the R4 typical control grid (124/tower)",
               top_beam_z=[159.30, 159.90], solid_band="none - open frame; plant screened by inner louvre line on L40 roof"),
    top_zone=dict(floors="L36–L40 + crown", z0=135.60, z1=159.90,
                  corner_rib_face_m=[0.28, 0.40], corner_rib_projection_m=[0.32, 0.60],
                  penthouse_loggia_surround_reveal_m=0.45),
    bands=dict(L06="glass-tone louvre, ribs continuous", L23="glass-tone louvre, ribs continuous",
               L40="glass-tone louvre, reads as base of crown frame"),
)


def bc_outline_world(t):
    pts = BC["footprint_outline_local_m"]
    if t == "B":
        return [(94 + u, 102 + v) for u, v in pts]
    return [(194 - u, 53 - v) for u, v in pts]
