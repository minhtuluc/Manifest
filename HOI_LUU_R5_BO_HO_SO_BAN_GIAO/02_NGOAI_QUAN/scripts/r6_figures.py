"""R6-CROWN drawings F01..F07 (SVG), built only from source coordinates + R6 rules."""
import math, os
import r6_geom as G
import r6_render as RR
from r6_svg import Svg, view_axes, proj, depth

OUT = os.path.join(G.PKG, "02_NGOAI_QUAN", "drawings", "CROWN_R6")
NOTE = "R6-CROWN · hình từ tọa độ R2/R3 + quy tắc R6; gân/fin là đường biểu đạt, chưa phải tiết diện; màu minh họa"
GLOW = '<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="3"/></filter>'


def levels(svg, x0, x1, Y, items, color="#8a969b"):
    for z, lab in items:
        svg.line(x0, Y(z), x1, Y(z), "#c9d0d3", 0.6, dash="3,3")
        svg.text(x0 - 4, Y(z) + 3.5, lab, 9, "end", color)


def compare_rim(svg, t, beta, X, Y):
    right, d = view_axes(beta)
    g5 = G.crown_grid(t, "R5")
    top = g5[-1] + [g5[-1][0]]
    for side, run in RR.split_by_side(top, d):
        if side:
            svg.poly([(X(proj(p, right)), Y(p[2])) for p in run], RR.COL["r5"], 1.1, dash="5,3")


# ------------------------------------------------------------------ F01 crown A
def f01():
    s = Svg(1560, 980)
    s.defs.append(GLOW)
    s.title_block("R6-F01", "A · Crown \"Hội lưu\": 8 gân hội tụ theo cặp về 4 rãnh, đỉnh +520", NOTE + " · nét cam đứt: vành crown R5")
    sc, ztop, zbot = 6.0, 526.0, 404.0
    for i, (beta, lab) in enumerate(((90, "Mặt đứng hướng −Y (nhìn theo +Y)"), (45, "Mặt đứng chéo 45° (từ góc −X−Y)"))):
        ox = 110 + i * 470
        X = lambda x, ox=ox: ox + 190 + x * sc
        Y = lambda z: 90 + (ztop - z) * sc
        s.text(ox, 76, lab, 13, weight="bold")
        levels(s, ox + 8, ox + 380, Y, [(410.40, "+410,40 A90"), (452.40, "+452,40 mái"), (480.0, "+480,00"), (520.0, "+520,00")])
        s.clip_start("cA%d" % i, ox, Y(ztop), 390, (ztop - zbot) * sc)
        RR.draw_body(s, "A", beta, X, Y, sc, "R6", zmin=zbot)
        RR.draw_crown(s, "A", "R6", beta, X, Y, sc)
        compare_rim(s, "A", beta, X, Y)
        s.group_end()
    # plan
    ox, oy, psc = 1070, 150, 7.0
    X = lambda x: ox + 215 + x * psc
    Y = lambda y: oy + 200 - y * psc
    s.text(ox, 76, "Mặt bằng crown (nhìn từ trên)", 13, weight="bold")
    RR.draw_plan_crown(s, "A", X, Y, psc)
    s.text(X(0), Y(0) + 4, "lõi mái / BMU", 9, "middle", "#7a6f5a")
    for k, lab in enumerate(("rãnh +X", "rãnh +Y", "rãnh −X", "rãnh −Y")):
        a = k * math.pi / 2
        s.text(X(31 * math.cos(a)), Y(31 * math.sin(a)) + 4, lab, 9, "middle", "#555")
    mA = G.metrics("A")
    notes = [
        "Mái +452,40 và toàn bộ sàn giữ nguyên; không có sàn khai thác trong crown.",
        "Vành: %s; góc thấp +480,00, trục rãnh +520,00 (envelope)." % G.SPEC["R6"]["A"]["ztop_text"],
        "Co XY 30%% theo smoothstep + tiếp tuyến Hermite R1; vòng đỉnh ≈ %.1f × %.1f m." % (mA["top_ring_W"], mA["top_ring_H"]),
        "Gân chính: φ(u) = θrãnh + (θgân − θrãnh)(1 − 0,85·s(u)); đầu gân +%.2f; khe đỉnh ≈ %.1f m." % (mA["rib_tip_max_z"], mA["apex_slot_width"]),
        "32 fin đặt đúng nút lưới panel; 16 fin trong lòng mũi nhọn dừng trên gân (vân hội tụ).",
        "Lớp che thiết bị lùi 1,5 m, bám theo co của crown, đỉnh +470,00.",
        "Vùng chuyển A90–A98: gân 1,05 → 1,40 m, nhô 0,75 → 1,50 m; fin 0,18 → 0,60 m.",
    ]
    for i, n in enumerate(notes):
        s.text(1030, 610 + i * 19, "• " + n, 10.5, color="#333")
    s.save(os.path.join(OUT, "R6-F01-crown-A.svg"))


# ------------------------------------------------------------------ F03 crown D
def f03():
    s = Svg(1560, 820)
    s.title_block("R6-F03", "D · Crown nghiêng về A: một mũi nhọn ở mặt −X, đỉnh +310", NOTE + " · nét cam đứt: vành crown R5")
    sc, ztop, zbot = 6.0, 314.0, 234.0
    for i, (beta, lab) in enumerate(((90, "Mặt đứng hướng −Y (A ở bên trái)"), (0, "Mặt −X, mặt đối diện A (nhìn theo +X)"))):
        ox = 110 + i * 470
        X = lambda x, ox=ox: ox + 190 + x * sc
        Y = lambda z: 90 + (ztop - z) * sc
        s.text(ox, 76, lab, 13, weight="bold")
        levels(s, ox + 8, ox + 380, Y, [(240.85, "+240,85 D56"), (269.45, "+269,45 mái"), (286.0, "+286,00"), (310.0, "+310,00")])
        s.clip_start("cD%d" % i, ox, Y(ztop), 390, (ztop - zbot) * sc)
        RR.draw_body(s, "D", beta, X, Y, sc, "R6", zmin=zbot)
        RR.draw_crown(s, "D", "R6", beta, X, Y, sc)
        compare_rim(s, "D", beta, X, Y)
        s.group_end()
    ox, oy, psc = 1070, 150, 7.0
    X = lambda x: ox + 215 + x * psc
    Y = lambda y: oy + 150 - y * psc
    s.text(ox, 76, "Mặt bằng crown", 13, weight="bold")
    RR.draw_plan_crown(s, "D", X, Y, psc)
    s.text(X(-33), Y(0) + 4, "← A", 11, "end", "#8a4b12", weight="bold")
    mD = G.metrics("D")
    notes = [
        "Mái +269,45 và sàn giữ nguyên; D35 kính lùi 3 m giữ nguyên.",
        "Vành: %s." % G.SPEC["R6"]["D"]["ztop_text"],
        "Đỉnh +310 ở mặt −X hướng về A; thấp +286 ở phía xa; co XY 15%%; vòng đỉnh ≈ %.1f × %.1f m." % (mD["top_ring_W"], mD["top_ring_H"]),
        "Hai gân 157,5°/202,5° hội tụ về 180°; khe đỉnh ≈ %.1f m; 6 gân còn lại đi thẳng lên vành." % mD["apex_slot_width"],
        "23 fin crown nằm đúng pier khách sạn (mỗi 4 nút; bỏ pier trùng gân ±1 nút và pier giữa khe đỉnh).",
        "Lớp che thiết bị lùi 1,2 m, đỉnh +282,00 (12,55 m trên mái).",
        "Vùng chuyển D56–D62: gân 0,52 → 0,80 m, nhô 0,38 → 0,80 m; pier 0,30 → 0,60 m.",
    ]
    for i, n in enumerate(notes):
        s.text(1070, 470 + i * 19, "• " + n, 10.5, color="#333")
    s.save(os.path.join(OUT, "R6-F03-crown-D.svg"))


# ------------------------------------------------------------------ F02 elevations
def f02():
    s = Svg(1560, 1000)
    s.title_block("R6-F02", "A/D · Mặt đứng kiểm soát cùng tỷ lệ: vùng chuyển, dải kỹ thuật cùng tông kính, crown R6", NOTE)
    sc, ztop = 1.6, 530.0
    Y = lambda z: 70 + (ztop - z) * sc
    views = [("A", 90, "A · hướng −Y"), ("A", 0, "A · hướng −X"), ("D", 90, "D · hướng −Y"), ("D", 0, "D · hướng −X (mặt đối diện A)")]
    for i, (t, beta, lab) in enumerate(views):
        ox = 90 + i * 360
        X = lambda x, ox=ox: ox + 150 + x * sc
        s.text(ox + 40, 62, lab, 12, weight="bold")
        RR.draw_body(s, t, beta, X, Y, sc, "R6", mullions=False)
        RR.draw_crown(s, t, "R6", beta, X, Y, sc, back=False)
        compare_rim(s, t, beta, X, Y)
        tr = G.TRANSITION[t]
        s.line(ox + 95, Y(tr["z0"]), ox + 95, Y(tr["z1"]), "#c0782c", 1.6)
        s.text(ox + 90, (Y(tr["z0"]) + Y(tr["z1"])) / 2, "vùng chuyển " + tr["floors"], 9, "end", "#8a4b12")
    for z, lab in ((0, "±0,00"), (34, "+34,00"), (269.45, "+269,45"), (310, "+310,00"), (452.4, "+452,40"), (480, "+480,00 (R5)"), (520, "+520,00")):
        s.line(60, Y(z), 1500, Y(z), "#e3e7e9", 0.5)
        s.text(56, Y(z) + 3, lab, 9, "end", "#6b777c")
    s.text(90, 950, "Dải kỹ thuật A31/55/79/98, D20/34/48/62: lam cùng tông và độ phản xạ với kính, gân chạy liền. "
           "Sky lobby A32/56/80 kính trong. D35 kính lùi là dải bóng chủ đích duy nhất.", 10, color="#333")
    s.save(os.path.join(OUT, "R6-F02-elevations-AD.svg"))


# ------------------------------------------------------------------ F04 B/C top zone
def bc_floor(z):
    for f in G.BC["floor_schedule"]:
        if f["z"] - 1e-6 <= z < f["top"] - 1e-6:
            return f
    return None


def draw_bc_top(s, ox, oy, sc, rev):
    zt, zb = 162.0, 118.0
    X = lambda u: ox + u * sc
    Y = lambda z: oy + (zt - z) * sc
    grids = G.BC["control_grid"]
    feats = G.BC["source_features"]
    s.clip_start("bc" + rev, X(-4), Y(zt), 68 * sc, (zt - zb) * sc)
    s.rect(X(0), Y(154.2), 60 * sc, (154.2 - zb) * sc, RR.COL["bcglass"], 1.0)
    for f in G.BC["floor_schedule"]:
        if f["top"] < zb or f["z"] > 154.2:
            continue
        z0, z1 = f["z"], f["top"]
        if f["floor"] == 40:
            col = "#8f9a97" if rev == "R5" else "#a9bcc0"
            s.rect(X(0), Y(z1), 60 * sc, (z1 - z0) * sc, col, 0.9)
            if rev == "R6":
                zz = z0 + 0.3
                while zz < z1:
                    s.line(X(0), Y(zz), X(60), Y(zz), "#95aab0", 0.5)
                    zz += 0.35
            continue
        kind = "penthouse" if f["floor"] >= 36 else "typical"
        for edge, du in ((0, 0.0), (2, 32.0)):
            segs = grids[kind][str(edge)]
            for sg in segs:
                a, b = du + sg["a"], du + sg["b"]
                typ = sg["type"]
                if typ == "loggia":
                    s.rect(X(a), Y(z1), (b - a) * sc, (z1 - z0) * sc, "#2f4650", 0.95)
                    s.line(X(a), Y(z0 + 1.1), X(b), Y(z0 + 1.1), "#9fb7bf", 0.6)
                elif typ == "living":
                    s.rect(X(a), Y(z1), (b - a) * sc, (z1 - z0) * sc, "#b9d3da", 0.9)
                s.line(X(a), Y(z0), X(a), Y(z1), "#d7e0e2", 0.5)
            # slab lines except across living voids on upper floors
            for sg in segs:
                a, b = du + sg["a"], du + sg["b"]
                if f["upper"] and sg["type"] == "living":
                    continue
                s.line(X(a), Y(z0), X(b), Y(z0), "#7e9398", 0.6)
        if rev == "R6" and kind == "penthouse" and not f["upper"]:
            for edge, du in ((0, 0.0), (2, 32.0)):
                for ft in feats["penthouse"][str(edge)]:
                    if ft["type"] == "loggia":
                        a, b = du + ft["span"][0], du + ft["span"][1]
                        s.rect(X(a) - 0.45 * sc, Y(z0 + 7.2) - 0.3 * sc, (b - a + 0.9) * sc, 7.2 * sc + 0.3 * sc,
                               "none", 1.0, RR.COL["bcmetal"], 0.45 * sc)
    # corner ribs at u=0, 32, 60
    for u in (0.0, 32.0, 60.0):
        zz = zb
        while zz < (158.7 if rev == "R5" else 159.9) - 1e-6:
            z2 = min(zz + 1.0, 158.7 if rev == "R5" else 159.9)
            face = 0.28
            if rev == "R6" and zz >= 135.6:
                face = 0.28 + 0.12 * (zz - 135.6) / (159.9 - 135.6)
            s.line(X(u), Y(zz), X(u), Y(z2), "#ece8dc", max(1.2, face * sc))
            zz = z2
    # crown
    if rev == "R5":
        tz = G.BC["crown"]["top_corner_z_m"]
        s.polygon([(X(0), Y(154.2)), (X(0), Y(tz[0])), (X(32), Y(tz[1])), (X(32), Y(tz[2])), (X(60), Y(tz[3])), (X(60), Y(154.2))],
                  "#c7cfcc", 1.0, "#9aa5a3", 0.6)
    else:
        for edge, du in ((0, 0.0), (2, 32.0)):
            for sg in grids["typical"][str(edge)]:
                for a in (sg["a"],):
                    s.line(X(du + a), Y(154.2), X(du + a), Y(159.3), "#b8b2a2", max(1.0, 0.1 * sc))
        s.rect(X(0), Y(159.9), 60 * sc, 0.6 * sc, RR.COL["bcmetal"], 1.0, "#b8b2a2", 0.6)
        s.line(X(0), Y(156.0), X(60), Y(156.0), "#d9dcd6", 0.6, dash="2,3")
    s.group_end()
    for z, lab in ((135.6, "+135,60 L36"), (150.0, "+150,00 L40"), (154.2, "+154,20 mái"),
                   (158.7 if rev == "R5" else 159.9, "+158,70" if rev == "R5" else "+159,90"), (160.0, "H02 +160,00")):
        h02 = z == 160.0
        s.line(X(-3), Y(z), X(63), Y(z), "#c07a2c" if h02 else "#c9d0d3", 0.6, dash="3,3")
        if h02:
            s.text(X(64), Y(z) + 3, lab, 9, "start", "#8a4b12")
        else:
            s.text(X(-4), Y(z) + 3, lab, 9, "end", "#6b777c")


def f04():
    s = Svg(1560, 620)
    s.title_block("R6-F04", "B/C · Vùng kết thúc L36 → crown: khung mở tới +159,90, gân góc sâu dần, khung loggia penthouse", NOTE)
    sc = 9.0
    s.text(170, 70, "R5 · dải crown đặc, cao độ góc lệch 0,6 m", 12, weight="bold")
    draw_bc_top(s, 170, 90, sc, "R5")
    s.text(900, 70, "R6 · crown khung mở (mặt local −v, hai cánh lệch)", 12, weight="bold")
    draw_bc_top(s, 900, 90, sc, "R6")
    s.text(900, 520, "• Giữ H02 (40 tầng, ≤ 160 m): đỉnh +159,90, 8 gân góc cùng cao độ; không thêm tầng hay căn.", 10.5, color="#333")
    s.text(900, 539, "• Fin 55 mm, sâu 0,45 m tại mọi mullion lưới điển hình; dầm đỉnh +159,30..159,90; không còn dải đặc.", 10.5, color="#333")
    s.text(900, 558, "• Gân góc từ L36: mặt 0,28 → 0,40 m, nhô 0,32 → 0,60 m. Khung viền loggia penthouse sâu 0,45 m, ôm hai tầng.", 10.5, color="#333")
    s.text(900, 577, "• L06/L23/L40: lam cùng tông kính. Loggia vẫn có sàn ở cả hai tầng duplex (vạch sàn giữa hốc tối).", 10.5, color="#333")
    s.save(os.path.join(OUT, "R6-F04-crown-BC.svg"))


# ------------------------------------------------------------------ skyline helpers
def bc_extent(t, right):
    xs = [p[0] * right[0] + p[1] * right[1] for p in G.bc_outline_world(t)]
    return min(xs), max(xs)


def skyline(s, beta, X, Y, sc, rev="R6", night=False, compare=True, order=None):
    right, d = view_axes(beta)
    towers = ["A", "D", "B", "C"]
    dep = {}
    for t in towers:
        c = G.CENTER[t] if t in G.CENTER else ((124, 120) if t == "B" else (164, 35))
        dep[t] = depth(c, d)
    for t in sorted(towers, key=lambda t: -dep[t]):
        if t in ("A", "D"):
            c = G.CENTER[t]
            base = proj(c, right)
            Xt = lambda x, base=base: X(base + x)
            RR.draw_body(s, t, beta, Xt, Y, sc, rev, mullions=False, night=night)
            RR.draw_crown(s, t, rev, beta, Xt, Y, sc, night=night, back=False, wmul=1.0)
            if compare and rev == "R6":
                compare_rim(s, t, beta, Xt, Y)
        else:
            x0, x1 = bc_extent(t, right)
            top = 154.2
            body = "#b3c3c5" if not night else "#26363f"
            s.rect(X(x0), Y(top), (x1 - x0) * sc, top * sc, body, 1.0, "#7d8b8b" if not night else "#34444c", 0.6)
            ct = 159.9 if rev == "R6" else 158.7
            if rev == "R6":
                s.rect(X(x0), Y(ct), (x1 - x0) * sc, (ct - top) * sc, "none", 1.0, "#e7e3d6" if not night else "#e9c890", 0.8)
                if night:
                    s.rect(X(x0), Y(ct), (x1 - x0) * sc, (ct - top) * sc, "#e9c890", 0.25)
            else:
                s.rect(X(x0), Y(ct), (x1 - x0) * sc, (ct - top) * sc, "#c7cfcc", 1.0)


def f05():
    s = Svg(1600, 900)
    s.title_block("R6-F05", "Gia đình bốn tháp R6: A +520 / D +310 / B–C +159,9, skyline hạ dần từ A về D", NOTE + " · nét cam đứt: vành crown R5")
    sc, ztop = 1.38, 540.0
    Y = lambda z: 90 + (ztop - z) * sc
    s.text(60, 74, "Skyline hướng −Y (trục ngang X)", 12, weight="bold")
    for z, lab in ((520, "+520"), (480, "+480 (R5)"), (310, "+310"), (285, "+285 (R5)"), (159.9, "+159,9")):
        s.line(96, Y(z), 830, Y(z), "#e2e6e8", 0.5, dash="2,3")
        s.text(92, Y(z) + 3, lab, 9, "end", "#6b777c")
    X1 = lambda x: 110 + x * sc
    skyline(s, 90, X1, Y, sc)
    s.line(X1(0), Y(0), X1(300), Y(0), "#888", 0.8)
    s.line(X1(53), Y(519.5), X1(238 - 25), Y(310), "#c0782c", 0.9, dash="5,4")
    s.text(590, 74, "Skyline hướng −X (trục ngang −Y)", 12, weight="bold")
    X2 = lambda x: 600 + (x + 160) * sc
    skyline(s, 0, X2, Y, sc)
    s.line(X2(-160), Y(0), X2(5), Y(0), "#888", 0.8)
    # plan
    ox, oy, ps = 900, 120, 2.25
    PX = lambda x: ox + x * ps
    PY = lambda y: oy + (155 - y) * ps
    s.text(ox, 100, "Tổng mặt bằng: vòng mái và crown R6", 12, weight="bold")
    s.rect(PX(0), PY(155), 295 * ps, 155 * ps, "#f1f1ec", 1.0, "#9aa39f", 0.8)
    plaza = [(80, 70), (112, 79), (167, 78), (208, 82), (229, 93)]
    s.poly([(PX(x), PY(y)) for x, y in plaza], "#e3dccb", 24 * ps, op=0.9)
    for t in ("B", "C"):
        s.polygon([(PX(x), PY(y)) for x, y in G.bc_outline_world(t)], "#b7c6c6", 1.0, "#7d8b8b", 0.8)
        cx = sum(p[0] for p in G.bc_outline_world(t)) / 8
        cy = sum(p[1] for p in G.bc_outline_world(t)) / 8
        s.text(PX(cx), PY(cy) + 4, t, 13, "middle", "#2c3e44", weight="bold")
    for t in ("A", "D"):
        cx, cy = G.CENTER[t]
        roof = G.RINGS[t][-1]
        s.polygon([(PX(cx + p[0]), PY(cy + p[1])) for p in roof], "#9fb6bd" if t == "A" else "#b2b8b0", 1.0, "#6d7f86", 0.8)
        grid, ribs, fins, rims = RR.crown_members(t, "R6")
        for pts in ribs:
            s.poly([(PX(cx + p[0]), PY(cy + p[1])) for p in pts], RR.COL["rib" + t], 1.3)
        for seg in rims:
            s.poly([(PX(cx + p[0]), PY(cy + p[1])) for p in seg], RR.COL["rib" + t], 1.0)
        s.text(PX(cx), PY(cy) + 4, t, 13, "middle", "#1f3036", weight="bold")
    s.line(PX(238 - 26), PY(104), PX(80), PY(58), "#c0782c", 1.0, dash="5,4")
    s.text(PX(150), PY(86) - 2, "đỉnh D (+310) quay về A", 10, "middle", "#8a4b12")
    vn = lambda v, dp=2: ("%.*f" % (dp, v)).replace(".", ",")
    rows = [("Tháp", "Mái", "Đỉnh R5", "Đỉnh R6", "Crown R6", "Vùng kết thúc R6")]
    for t, zlab in (("A", "A90"), ("D", "D56")):
        m5, m6 = G.metrics(t, "R5"), G.metrics(t, "R6")
        rows.append((t, vn(m6["roof_z"]), vn(m5["architectural_top_z"]), vn(m6["architectural_top_z"]) + "*",
                     "%s m (%s%%)" % (vn(m6["crown_height_max"], 1), vn(100 * m6["crown_share_of_height"], 1)),
                     "%s → đỉnh, %s m (%s%%)" % (zlab, vn(m6["top_zone_height"], 1), vn(100 * m6["top_zone_share"], 0))))
    bz = G.BC_R6["top_zone"]
    rows.append(("B/C", "154,20", "158,70", "159,90", "5,7 m + L36–L40",
                 "L36 → đỉnh, %s m (%s%%)" % (vn(bz["z1"] - bz["z0"], 1), vn(100 * (bz["z1"] - bz["z0"]) / 159.9, 0))))
    for i, r in enumerate(rows):
        for j, c in enumerate(r):
            s.text(ox + [0, 50, 120, 190, 270, 400][j], 520 + i * 20, c, 10.5, color="#222", weight="bold" if i == 0 else "normal")
    s.text(ox, 610, "* đầu gân tính toán; envelope giới hạn +520,00 / +310,00. Không thêm tầng hoặc GFA.", 9.5, color="#555")
    ratio = G.metrics("D")["architectural_top_z"] / G.metrics("A")["architectural_top_z"]
    s.text(ox, 628, "Tỷ lệ D/A giữ %s (R5 0,594). B/C giữ đầu bài H02 ≤ 160 m." % vn(ratio, 3), 9.5, color="#555")
    s.save(os.path.join(OUT, "R6-F05-ensemble.svg"))


def f06():
    s = Svg(1600, 960)
    s.defs.append(GLOW)
    s.title_block("R6-F06", "Ban ngày / ban đêm: crown là đèn lồng nhiều lớp, không media, không kẻ viền tầng", NOTE)
    sc, ztop = 1.35, 540.0
    Y = lambda z: 90 + (ztop - z) * sc
    s.text(60, 70, "Ban ngày · kính trung tính, kim loại bạc ấm / champagne", 12, weight="bold")
    X1 = lambda x: 120 + x * sc
    skyline(s, 90, X1, Y, sc, compare=False)
    s.rect(800, 50, 780, 790, RR.COL["night_bg"], 1.0)
    s.text(820, 76, "Ban đêm · A 3500 K / D 3000 K / B–C 3000 K, thứ bậc sáng 1 : 0,6 : 0,3", 12, color="#e8edf0", weight="bold")
    X2 = lambda x: 880 + x * sc
    skyline(s, 90, X2, Y, sc, night=True, compare=False)
    notes = ["Lớp 1: lớp che thiết bị hắt sáng đều, fin ngoài đọc thành bóng.",
             "Lớp 2: gân chính grazing sáng dần qua vùng chuyển A90–A98 / D56–D62.",
             "Lớp 3: khe đỉnh 4 mũi A và mũi D là điểm sáng nhất.",
             "Sky lobby A32/56/80 sáng từ trong; B/C chỉ sáng khung crown và sảnh."]
    for i, n in enumerate(notes):
        s.text(820 + (i % 2) * 380, 868 + (i // 2) * 18, "• " + n, 10, color="#333")
    s.save(os.path.join(OUT, "R6-F06-day-night.svg"))


# ------------------------------------------------------------------ F07 axonometric
def f07():
    s = Svg(1600, 1150)
    s.title_block("R6-F07", "Phối cảnh chiếu song song từ tọa độ: cụm bốn tháp với crown R6", NOTE + " · đế A/D giản lược theo biên sàn A01–A06/D01–D06")
    k, sx0, sy0 = 1.62, 626.0, 1080.0
    VR, VD = view_axes(68.0)  # viewer looks along VD (from the -X/-Y side), right = VR
    tilt = 0.30

    def P(x, y, z):
        # parallel view looking down ~17 deg: farther points (larger depth) sit higher on the sheet
        return (sx0 + (x * VR[0] + y * VR[1]) * k, sy0 - z * k - (x * VD[0] + y * VD[1]) * k * tilt)

    def faces_viewer(nx, ny):
        return nx * VD[0] + ny * VD[1] < 0

    def dep(x, y):
        return x * VD[0] + y * VD[1]

    light = (-0.55, -0.75, 0.37)

    def shade(base, n):
        l = max(0.0, n[0] * light[0] + n[1] * light[1] + n[2] * light[2])
        f = 0.62 + 0.38 * l
        r, g, b = int(base[1:3], 16), int(base[3:5], 16), int(base[5:7], 16)
        return "#%02x%02x%02x" % (int(r * f), int(g * f), int(b * f))

    view = (1.0, 1.0)  # faces with n.x + n.y < 0 face the viewer at -X-Y

    def prism(pts2d, z0, z1, base):
        n = len(pts2d)
        faces = []
        for i in range(n):
            a, b = pts2d[i], pts2d[(i + 1) % n]
            ex, ey = b[0] - a[0], b[1] - a[1]
            nx, ny = ey, -ex
            L = math.hypot(nx, ny) or 1
            nx, ny = nx / L, ny / L
            area = sum(p[0] * q[1] - q[0] * p[1] for p, q in zip(pts2d, pts2d[1:] + pts2d[:1]))
            if area < 0:
                nx, ny = -nx, -ny
            if faces_viewer(nx, ny):
                faces.append((dep((a[0] + b[0]) / 2, (a[1] + b[1]) / 2),
                              [P(a[0], a[1], z0), P(b[0], b[1], z0), P(b[0], b[1], z1), P(a[0], a[1], z1)], shade(base, (nx, ny, 0))))
        for dep_, poly, col in sorted(faces, key=lambda f: -f[0]):
            s.polygon(poly, col, 1.0, col, 0.3)
        s.polygon([P(p[0], p[1], z1) for p in pts2d], shade(base, (0, 0, 1)), 1.0, "#8a9599", 0.4)

    def tower_AD(t):
        cx, cy = G.CENTER[t]
        for fl in range(1, 7):
            pts = [(p[0], p[1]) for p in RR.PODIUM[(t, fl)]][::4]
            f = G.FLOORS[(t, fl)]
            prism(pts, f["z"], f["top"], "#ddd6c6")
        R = G.RINGS[t]
        rings = R[::3] + ([R[-1]] if (len(R) - 1) % 3 else [])
        base = RR.COL["glass" + t]
        faces = []
        for r0, r1 in zip(rings, rings[1:]):
            n = len(r0)
            for i in range(0, n, 2):
                j = (i + 2) % n
                a0, b0, a1, b1 = r0[i], r0[j], r1[i], r1[j]
                ex, ey = b0[0] - a0[0], b0[1] - a0[1]
                nx, ny = ey, -ex
                L = math.hypot(nx, ny) or 1
                nx, ny = nx / L, ny / L
                if faces_viewer(nx, ny):
                    poly = [P(cx + a0[0], cy + a0[1], a0[2]), P(cx + b0[0], cy + b0[1], b0[2]),
                            P(cx + b1[0], cy + b1[1], b1[2]), P(cx + a1[0], cy + a1[1], a1[2])]
                    faces.append((dep(a0[0], a0[1]), poly, shade(base, (nx, ny, 0.05))))
        for _, poly, col in sorted(faces, key=lambda f: -f[0]):
            s.polygon(poly, col, 1.0, col, 0.4)
        # roof cap (seen from above)
        s.polygon([P(cx + p[0], cy + p[1], p[2]) for p in R[-1]], shade(base, (0, 0, 1)), 1.0)
        # body ribs front
        for nn in G.RIB_NODES[t]:
            p0 = R[0][nn]
            if dep(p0[0], p0[1]) >= 0:
                continue
            for a, b in zip(R, R[1:]):
                face, _ = G.rib_face_projection(t, a[nn][2])
                s.poly([P(cx + a[nn][0], cy + a[nn][1], a[nn][2]), P(cx + b[nn][0], cy + b[nn][1], b[nn][2])],
                       RR.COL["bodyrib" + t], max(0.8, face * k), cap="butt")
        z0 = G.TRANSITION[t]["z0"]
        for nn in G.FIN_NODES[t]:
            if dep(R[-1][nn][0], R[-1][nn][1]) >= 0:
                continue
            pts = [P(cx + r[nn][0], cy + r[nn][1], r[nn][2]) for r in R if r[nn][2] >= z0 - 1e-6]
            s.poly(pts, RR.COL["fin" + t], 0.7)
        # crown
        grid, ribs, fins, rims = RR.crown_members(t, "R6")
        sr = RR.screen_rings(t, "R6", grid)
        Q = lambda p: P(cx + p[0], cy + p[1], p[2])
        for pts in fins + rims + ribs:  # back members first
            for side, run in RR.split_by_side(pts, VD):
                if not side:
                    s.poly([Q(p) for p in run], "#aeb4b4", 0.6, op=0.6)
        sf = []
        for r0, r1 in zip(sr, sr[1:]):
            n = len(r0)
            for i in range(0, n, 2):
                j = (i + 2) % n
                ex, ey = r0[j][0] - r0[i][0], r0[j][1] - r0[i][1]
                if faces_viewer(ey, -ex):
                    sf.append((dep(r0[i][0], r0[i][1]), [Q(r0[i]), Q(r0[j]), Q(r1[j]), Q(r1[i])]))
        for _, poly in sorted(sf, key=lambda f: -f[0]):
            s.polygon(poly, RR.COL["screen" + t], 1.0, RR.COL["screen" + t], 0.3)
        s.polygon([Q(p) for p in sr[-1]], "#d9cfb8", 1.0)
        rf0, rf1, ff, rw = RR.CREST[(t, "R6")]
        for pts in fins:
            for side, run in RR.split_by_side(pts, VD):
                if side:
                    s.poly([Q(p) for p in run], RR.COL["fin" + t], max(0.8, ff * k * 4))
        for seg in rims:
            for side, run in RR.split_by_side(seg, VD):
                if side:
                    s.poly([Q(p) for p in run], RR.COL["rib" + t], 1.2)
        for pts in ribs:
            for side, run in RR.split_by_side(pts, VD):
                if side:
                    s.poly([Q(p) for p in run], RR.COL["rib" + t], max(1.4, rf0 * k), cap="butt")

    def tower_BC(t):
        pts = G.bc_outline_world(t)
        prism(pts, 0, 154.2, "#b3c3c5")
        # open crown frame: posts at corners + top beam
        for p in pts:
            s.poly([P(p[0], p[1], 154.2), P(p[0], p[1], 159.9)], "#e7e3d6", 1.6)
        s.poly([P(p[0], p[1], 159.9) for p in pts + pts[:1]], "#e7e3d6", 1.6)

    s.polygon([P(0, 0, 0), P(295, 0, 0), P(295, 155, 0), P(0, 155, 0)], "#eceee9", 1.0, "#a9b0ac", 0.8)
    plaza = [(80, 70), (112, 79), (167, 78), (208, 82), (229, 93)]
    s.poly([P(x, y, 0) for x, y in plaza], "#e0d9c7", 12 * k, op=0.9)
    cen = {"A": (53, 49), "D": (238, 104), "B": (124, 120), "C": (164, 35)}
    tops = {"A": 527.0, "D": 316.0, "B": 166.0, "C": 166.0}
    for t in sorted(cen, key=lambda t: -dep(*cen[t])):
        (tower_AD if t in ("A", "D") else tower_BC)(t)
    for t, (x, y) in cen.items():
        px, py = P(x, y, tops[t])
        s.text(px, py, t, 15, "middle", "#1f3036", weight="bold")
    s.save(os.path.join(OUT, "R6-F07-axo.svg"))


def build_all():
    os.makedirs(OUT, exist_ok=True)
    for f in (f01, f02, f03, f04, f05, f06, f07):
        f()
    return sorted(os.listdir(OUT))


if __name__ == "__main__":
    print(build_all())
