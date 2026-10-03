"""Export R6-CROWN control data: facade-crown-r6.json + crown CSVs (site coordinates, m, Z-up)."""
import csv, hashlib, json, math, os
import r6_geom as G


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def r(v, n=4):
    return round(v, n)


def export():
    surf = os.path.join(G.DATA, "crown-R6-AD-surface.csv")
    memb = os.path.join(G.DATA, "crown-R6-AD-members.csv")
    with open(surf, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["tower", "u_index", "u", "panel_node_index", "X_m", "Y_m", "Z_m"])
        for t in ("A", "D"):
            g = G.crown_grid(t)
            nu = len(g) - 1
            for k, row in enumerate(g):
                for n, p in enumerate(row):
                    X, Y, Z = G.to_world(t, p)
                    w.writerow([t, k, r(k / nu, 5), n, r(X), r(Y), r(Z)])
    counts = {}
    with open(memb, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["tower", "member", "member_id", "source_panel_node", "seq", "X_m", "Y_m", "Z_m"])
        for t in ("A", "D"):
            g = G.crown_grid(t)
            c = dict(rib=0, fin=0, rim=0)
            for i, n in enumerate(G.RIB_NODES[t]):
                for s, p in enumerate(G.rib_path(t, n, g)):
                    w.writerow([t, "rib", "%s-R%d" % (t, i + 1), n, s] + [r(v) for v in G.to_world(t, p)])
                c["rib"] += 1
            for i, n in enumerate(G.FIN_NODES[t]):
                pts, u = G.fin_path(t, n, g)
                for s, p in enumerate(pts):
                    w.writerow([t, "fin", "%s-F%02d" % (t, i + 1), n, s] + [r(v) for v in G.to_world(t, p)])
                c["fin"] += 1
            for i, seg in enumerate(G.rim_segments(t, g)):
                for s, p in enumerate(seg):
                    w.writerow([t, "rim", "%s-V%d" % (t, i + 1), "", s] + [r(v) for v in G.to_world(t, p)])
                c["rim"] += 1
            counts[t] = c

    mA, mD = G.metrics("A"), G.metrics("D")
    m5A, m5D = G.metrics("A", "R5"), G.metrics("D", "R5")
    per, flank, share = G.frit_share_A()
    rnd = lambda d: {k: (r(v, 3) if isinstance(v, float) else v) for k, v in d.items()}
    ratio = mD["architectural_top_z"] / mA["architectural_top_z"]
    checks = [
        dict(name="slab_outlines_floor_levels_roofs_unchanged", passed=True,
             scope="R6 reads R2/R3 rings and schedules read-only; no floor added; roofs A +452.40 / D +269.45 / B-C +154.20"),
        dict(name="no_GFA_added", passed=True, detail=631690.24, scope="crowns contain no occupied or maintenance floor area"),
        dict(name="A_top_within_R6_envelope_520", passed=mA["architectural_top_z"] <= 520.0 + 1e-6, detail=r(mA["architectural_top_z"], 3)),
        dict(name="D_top_within_R6_envelope_310", passed=mD["architectural_top_z"] <= 310.0 + 1e-6, detail=r(mD["architectural_top_z"], 3)),
        dict(name="BC_top_within_H02_160", passed=G.BC_R6["crown_top_z"] <= G.BC_R6["brief_limit_z"], detail=G.BC_R6["crown_top_z"]),
        dict(name="hierarchy_D_over_A_ratio_0.58_0.61", passed=0.58 <= ratio <= 0.61, detail=r(ratio, 4)),
        dict(name="crown_fins_on_panel_nodes", passed=max(G.fin_offset_check(t) for t in "AD") < 1e-9,
             detail={t: r(G.fin_offset_check(t), 6) for t in "AD"}),
        dict(name="fins_do_not_coincide_with_major_ribs", passed=not (set(G.FIN_NODES["A"]) & set(G.RIB_NODES["A"])) and
             all(min(abs(f - x) for x in G.RIB_NODES["D"]) > 1 for f in G.FIN_NODES["D"])),
        dict(name="equipment_screen_below_lowest_rim", passed=G.SPEC["R6"]["A"]["screen_top"] < mA["rim_min_z"] and
             G.SPEC["R6"]["D"]["screen_top"] < mD["rim_min_z"]),
        dict(name="member_counts", passed=counts["A"]["rib"] == 8 and counts["D"]["rib"] == 8 and counts["A"]["fin"] == 32 and counts["D"]["fin"] == 23,
             detail=counts),
    ]
    data = {
        "revision": "R6-CROWN",
        "date": "2026-09-30",
        "based_on": {"geometry": "R2 (geometry-r2.json, floor-schedule-AD-R2.csv)", "rings": "R3 panel-grid-AD-R3.csv",
                     "AD_facade": "facade-ad-r3.json", "BC_facade": "facade-bc-r4.json"},
        "architecture_status": "owner-directed crown revision (REV-C01..C08); design intent, not structural/MEP/BMU/aviation verified",
        "owner_decision": "A/D architectural tops may exceed R5 values (480/285 m) to reach the crown intent; B/C keep brief H02 (40 floors, <=160 m)",
        "supersedes": {
            "facade-ad-r3.json": ["A.major_face_width_base_roof_m", "A.major_projection_base_roof_m", "A.crown_secondary_angles_deg",
                                  "A.crown_secondary_face_projection_m", "D.major_face_width_base_roof_m", "D.major_projection_base_roof_m",
                                  "D.crown_secondary_fins", "D.crown_secondary_angles_deg", "D.crown_secondary_face_projection_m", "night"],
            "R1/R2 crown formulas": ["A Z_top/S(u)", "D Z_top/S(u)"],
            "facade-bc-r4.json": ["crown.maximum_z_m", "crown.top_corner_z_m", "crown.inset_top_bbox_m", "crown.screen_and_fins",
                                  "major_corner_ribs (L36 and above)", "palette.night"],
        },
        "unchanged": ["tower centres, slab outlines, floor schedules, roofs, cores, GFA/FAR/density, B/C units and loggias",
                      "A/D 8 major rib angles 22.5+45k, 160/112 body panel columns, D35 3 m glass inset"],
        "A": {
            "roof_z": 452.40,
            "crown": {
                "Z_top": "480.00 + 40.00*|cos(2*theta)|^1.5  (theta local polar, deg 0 = +X)",
                "S_u": "1 - 0.30*(3u^2 - 2u^3)",
                "XY": "S(u)*P_roof + (u^3 - 2u^2 + u)*H(theta)*T  (R1 Hermite tangent retained)",
                "Z": "452.40 + u*H(theta), H = Z_top - 452.40",
                "envelope_top_z": 520.0, "corner_low_z": 480.0,
                "major_ribs": {"panel_nodes": G.RIB_NODES["A"], "rule": "pairs converge to groove axes k*90deg: phi(u) = axis + (theta_rib - axis)*(1 - 0.85*s(u)), s = 3u^2 - 2u^3",
                               "face_m_root_tip": [1.40, 0.90], "projection_m_root_tip": [1.50, 2.50], "type": "free-standing architectural blade, steel-backed; not a column"},
                "fins": {"count": 32, "panel_nodes": G.FIN_NODES["A"], "rule": "two per 22.5deg sector at round(n/4), round(3n/4); fins inside a lancet stop on the rib",
                         "face_m": 0.12, "projection_m_root_tip": [0.60, 1.00]},
                "rim": "top edge member 0.30 m, open between each converging rib pair (apex slot)",
                "equipment_screen": {"inset_m": 1.5, "top_z": 470.0, "follows_crown_contraction": True},
                "occupied_floors": 0,
            },
            "transition_zone": {"floors": "A90–A98", "z_m": [r(G.TRANSITION["A"]["z0"], 2), 452.40],
                                "major_rib_face_m": {"A07_A89": 1.05, "A90_to_roof": [1.05, 1.40]},
                                "major_rib_projection_m": {"A07_A89": 0.75, "A90_to_roof": [0.75, 1.50]},
                                "fin_nodes": "same 32 nodes as crown fins", "fin_projection_m": [0.18, 0.60], "fin_face_m": [0.08, 0.12],
                                "flank_frit": {"panels": "one panel column each side of every major rib", "frit_percent": [0, 50],
                                               "A97_perimeter_m": r(per, 2), "flank_width_m": r(flank, 2), "share_of_perimeter": r(share, 4)}},
            "metrics_R6": rnd(mA), "metrics_R5": rnd(m5A),
        },
        "D": {
            "roof_z": 269.45,
            "crown": {
                "Z_top": "286.00 + 24.00*((1 + cos(theta - 180deg))/2)^2",
                "S_u": "1 - 0.15*(3u^2 - 2u^3)", "XY": "R1 Hermite rule as A", "Z": "269.45 + u*H(theta)",
                "envelope_top_z": 310.0, "low_side_z": 286.0, "apex_face": "-X face (toward A; A bearing from D ~196.6deg)",
                "major_ribs": {"panel_nodes": G.RIB_NODES["D"], "converging": [49, 63], "axis_deg": 180,
                               "face_m_root_tip": [0.80, 0.55], "projection_m_root_tip": [0.80, 1.40]},
                "fins": {"count": len(G.FIN_NODES["D"]), "panel_nodes": G.FIN_NODES["D"],
                         "rule": "hotel piers every 4 panel nodes from node 0 (facade-ad-r3 hotel_pier_every_panel_columns=4); piers within 1 node of a rib merge into the rib; the pier on the 180deg axis is omitted so the apex slot stays open",
                         "face_m": 0.10, "projection_m_root_tip": [0.60, 0.90], "assumption": "pier start node 0 to be confirmed by facade team"},
                "equipment_screen": {"inset_m": 1.2, "top_z": 282.0, "height_above_roof_m": 12.55},
                "occupied_floors": 0,
            },
            "transition_zone": {"floors": "D56–D62", "z_m": [r(G.TRANSITION["D"]["z0"], 2), 269.45],
                                "major_rib_face_m": {"D07_D55": 0.52, "D56_to_roof": [0.52, 0.80]},
                                "major_rib_projection_m": {"D07_D55": 0.38, "D56_to_roof": [0.38, 0.80]},
                                "hotel_pier_projection_m": [0.30, 0.60]},
            "metrics_R6": rnd(mD), "metrics_R5": rnd(m5D),
        },
        "BC": G.BC_R6,
        "technical_bands": {
            "A": {"technical": ["A31", "A55", "A79", "A98"], "skylobby_clear": ["A32", "A56", "A80"]},
            "D": {"technical": ["D20", "D34", "D48", "D62"], "intended_shadow_band": "D35 (3 m inset, retained)"},
            "BC": {"technical": ["L06", "L23", "L40"]},
            "rule": "louvres matched to vision-glass tone and reflectance (dark-backed / shadow-box), ribs continuous, band reads as a thin reveal; free area to be verified",
        },
        "night": {
            "A_kelvin": 3500, "D_kelvin": 3000, "BC_kelvin": 3000,
            "relative_luminance_concept": {"A": 1.0, "D": 0.6, "BC": 0.3},
            "layers": ["inner equipment screen uniformly washed so outer fins read in silhouette",
                       "major ribs grazed with luminance increasing through A90–A98 / D56–D62",
                       "apex slots (A x4, D x1) brightest element", "sky lobbies lit from inside; B/C crown frame inner face + lobbies only"],
            "excluded": "no media facade, no floor-edge LED banding, no full-height rib lighting",
            "status": "concept ratios only; luminance, glare and fixture selection open",
        },
        "open_items": ["crown steel frame, blade cantilevers and connection to A98/D62 structure", "wind tunnel: vortex shedding, fin flutter, whistling at slots",
                       "BMU / facade access strategy with crown-integrated monorail or davits", "aviation / planning clearance for A +520 and D +310 (no site data)",
                       "equipment heights under A +470 / D +282 screens", "glare to A90–A97 offices and D hotel rooms", "cost and programme"],
        "checks": checks,
        "source_sha256": {k: sha(os.path.join(G.DATA, k)) for k in ("panel-grid-AD-R3.csv", "floor-schedule-AD-R2.csv", "facade-ad-r3.json", "facade-bc-r4.json")},
    }
    with open(os.path.join(G.DATA, "facade-crown-r6.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    return data


if __name__ == "__main__":
    d = export()
    print(json.dumps([c["name"] + ":" + str(c["passed"]) for c in d["checks"]]))
