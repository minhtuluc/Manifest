"""Self-contained HTML viewer for R6-CROWN: inline SVG drawings, R5/R6 tables and embedded control JSON."""
import html, json, os
import r6_geom as G

DRAW = os.path.join(G.PKG, "02_NGOAI_QUAN", "drawings", "CROWN_R6")
OUT = os.path.join(G.PKG, "02_NGOAI_QUAN", "CROWN_R6.html")

FIGS = [
    ("R6-F05-ensemble.svg", "Gia đình bốn tháp",
     "Thứ bậc A520 / D310 / B–C159,9 m, tỷ lệ D/A 0,597. Nét cam đứt: vành crown R5. Mặt bằng thể hiện vòng mái, gân crown và hướng đỉnh D về A."),
    ("R6-F07-axo.svg", "Phối cảnh chiếu song song",
     "Dựng trực tiếp từ vòng panel R3 và quy tắc R6; đế A/D giản lược theo biên sàn A01–A06/D01–D06."),
    ("R6-F01-crown-A.svg", "A · crown \"Hội lưu\"",
     "8 gân chính hội tụ theo cặp về 4 rãnh; đỉnh mỗi mũi +520 (envelope), đầu gân +519,54; góc +480; khe đỉnh ~1,7 m; lớp che thiết bị +470."),
    ("R6-F03-crown-D.svg", "D · crown nghiêng về A",
     "Một mũi nhọn ở mặt −X đối diện A, đỉnh +310 (envelope), phía xa +286; 23 fin trên pier khách sạn."),
    ("R6-F02-elevations-AD.svg", "A/D · mặt đứng kiểm soát cùng tỷ lệ",
     "Vùng chuyển A90–A98 / D56–D62; dải kỹ thuật cùng tông kính; D35 là dải bóng chủ đích duy nhất."),
    ("R6-F04-crown-BC.svg", "B/C · vùng kết thúc và crown khung mở",
     "Giữ H02 ≤ 160 m: khung fin mở tới +159,90; gân góc sâu dần từ L36; khung viền loggia penthouse ôm hai tầng."),
    ("R6-F06-day-night.svg", "Ban ngày / ban đêm",
     "Crown là đèn lồng nhiều lớp: lớp che hắt sáng, gân grazing sáng dần, khe đỉnh sáng nhất. Không media, không viền tầng."),
]

CSS = """
body{font-family:'Segoe UI',Arial,sans-serif;margin:0;color:#1f2a30;background:#f6f7f5}
header{background:#1f3036;color:#eef3f4;padding:28px 40px}
header h1{margin:0 0 6px;font-size:26px} header p{margin:4px 0;color:#c9d6da;max-width:1100px}
main{padding:24px 40px;max-width:1640px}
section{background:#fff;border:1px solid #dde3e4;border-radius:6px;margin:0 0 22px;padding:18px 22px}
h2{font-size:19px;margin:0 0 10px} .cap{color:#4d5c62;font-size:13.5px;margin:8px 0 0}
table{border-collapse:collapse;font-size:13.5px;margin:6px 0} td,th{border:1px solid #d7dddf;padding:5px 9px;text-align:left}
th{background:#eef2f2} .fig svg{width:100%;height:auto;display:block}
.tag{display:inline-block;background:#e6ecee;color:#233;border-radius:3px;padding:2px 8px;margin:2px 4px 2px 0;font-size:12px}
pre{background:#f2f4f4;padding:10px;overflow:auto;max-height:420px;font-size:11.5px}
ul{margin:6px 0 6px 20px}
"""


def fmt(v, d=2):
    return ("%.*f" % (d, v)).replace(".", ",")


def build():
    data = json.load(open(os.path.join(G.DATA, "facade-crown-r6.json"), encoding="utf-8"))
    a5, a6 = data["A"]["metrics_R5"], data["A"]["metrics_R6"]
    d5, d6 = data["D"]["metrics_R5"], data["D"]["metrics_R6"]
    rows = [
        ("Đỉnh kiến trúc, m", fmt(a5["architectural_top_z"]), fmt(a6["architectural_top_z"]), fmt(d5["architectural_top_z"]), fmt(d6["architectural_top_z"])),
        ("Crown max, m (% chiều cao)", "%s (%s%%)" % (fmt(a5["crown_height_max"], 1), fmt(100 * a5["crown_share_of_height"], 1)),
         "%s (%s%%)" % (fmt(a6["crown_height_max"], 1), fmt(100 * a6["crown_share_of_height"], 1)),
         "%s (%s%%)" % (fmt(d5["crown_height_max"], 1), fmt(100 * d5["crown_share_of_height"], 1)),
         "%s (%s%%)" % (fmt(d6["crown_height_max"], 1), fmt(100 * d6["crown_share_of_height"], 1))),
        ("Vành thấp nhất, m", fmt(a5["rim_min_z"]), fmt(a6["rim_min_z"]), fmt(d5["rim_min_z"]), fmt(d6["rim_min_z"])),
        ("Vùng kết thúc đọc được, m (%)", "%s (%s%%)" % (fmt(a5["top_zone_height"], 1), fmt(100 * a5["top_zone_share"], 1)),
         "%s (%s%%)" % (fmt(a6["top_zone_height"], 1), fmt(100 * a6["top_zone_share"], 1)),
         "%s (%s%%)" % (fmt(d5["top_zone_height"], 1), fmt(100 * d5["top_zone_share"], 1)),
         "%s (%s%%)" % (fmt(d6["top_zone_height"], 1), fmt(100 * d6["top_zone_share"], 1))),
        ("Chiều cao không khai thác, m (%)", "%s (%s%%)" % (fmt(a5["vanity_height"], 1), fmt(100 * a5["vanity_share"], 1)),
         "%s (%s%%)" % (fmt(a6["vanity_height"], 1), fmt(100 * a6["vanity_share"], 1)),
         "%s (%s%%)" % (fmt(d5["vanity_height"], 1), fmt(100 * d5["vanity_share"], 1)),
         "%s (%s%%)" % (fmt(d6["vanity_height"], 1), fmt(100 * d6["vanity_share"], 1))),
        ("Vòng đỉnh, m", "%s × %s" % (fmt(a5["top_ring_W"], 1), fmt(a5["top_ring_H"], 1)), "%s × %s" % (fmt(a6["top_ring_W"], 1), fmt(a6["top_ring_H"], 1)),
         "%s × %s" % (fmt(d5["top_ring_W"], 1), fmt(d5["top_ring_H"], 1)), "%s × %s" % (fmt(d6["top_ring_W"], 1), fmt(d6["top_ring_H"], 1))),
        ("Khe đỉnh, m", "—", fmt(a6["apex_slot_width"], 1), "—", fmt(d6["apex_slot_width"], 1)),
        ("Fin crown", "32 (lệch mullion ≤ 0,44 m)", "%d trên nút lưới (%d dừng trên gân)" % (a6["fins_total"], a6["fins_terminating_on_ribs"]),
         "16 (lệch ≤ 0,56 m)", "%d trên pier" % d6["fins_total"]),
    ]
    tb = "<table><tr><th>Chỉ số</th><th>A R5</th><th>A R6</th><th>D R5</th><th>D R6</th></tr>%s</table>" % "".join(
        "<tr>%s</tr>" % "".join("<td>%s</td>" % html.escape(c) for c in r) for r in rows)
    checks = "".join('<span class="tag">%s %s</span>' % ("✔" if c["passed"] else "✘", html.escape(c["name"])) for c in data["checks"])
    figs = []
    for fn, title, cap in FIGS:
        svg = open(os.path.join(DRAW, fn), encoding="utf-8").read()
        figs.append('<section class="fig"><h2>%s</h2>%s<p class="cap">%s · <code>drawings/CROWN_R6/%s</code></p></section>'
                    % (html.escape(title), svg, html.escape(cap), fn))
    opens = "".join("<li>%s</li>" % html.escape(o) for o in data["open_items"])
    sup = "".join("<li><b>%s</b>: %s</li>" % (html.escape(k), html.escape(", ".join(v))) for k, v in data["supersedes"].items())
    page = """<!doctype html><html lang="vi"><head><meta charset="utf-8"><title>HỘI LƯU · R6-CROWN</title><style>%s</style></head><body>
<header><h1>HỘI LƯU · R6-CROWN: crown và vùng kết thúc</h1>
<p>REV-C01…C08 theo chỉ đạo chủ đầu tư. A/D được vượt cao độ đỉnh R5 để crown đạt ý đồ thị giác; B/C giữ đầu bài H02 (≤ 40 tầng, ≤ 160 m).
Sàn, mái, lõi, số căn và GFA 631.690,24 m² không đổi. Chưa phê duyệt cuối; chưa kiểm chứng kết cấu, gió, BMU, tĩnh không.</p>
<p>Ngày 30/09/2026 · đơn vị m · Z-up · tọa độ site · hình dựng từ tọa độ, không phải render/GenAI.</p></header><main>
<section><h2>Ý đồ</h2><p>Tên Hội Lưu (hợp lưu) được đọc thành hình. Bốn rãnh nông của thân A là bốn dòng chảy; mỗi cặp gân chính hai bên một rãnh
hội tụ lên trời thành một mũi nhọn, để lại khe mở ở đỉnh. D đáp lại bằng một mũi duy nhất quay về A, nên skyline hạ dần một đường liền từ A xuống D.
B/C là nền cư trú, kết thúc bằng khung mở tiết chế. Crown bắt đầu từ vùng chuyển trên thân (A90–A98, D56–D62, L36), nên không thành một chiếc mũ đặt lên mái.</p>
%s<p>%s</p></section>
%s
<section><h2>Trường bị R6 thay (supersedes)</h2><ul>%s</ul><p class="cap">Mọi trường khác của R1–R4 giữ nguyên hiệu lực.</p></section>
<section><h2>Còn mở</h2><ul>%s</ul></section>
<section><h2>Dữ liệu kiểm soát nhúng: facade-crown-r6.json</h2><p class="cap">Bản gốc: <code>03_DU_LIEU_KIEM_SOAT/facade-crown-r6.json</code>;
tọa độ crown: <code>crown-R6-AD-surface.csv</code>, <code>crown-R6-AD-members.csv</code>; tái tạo: <code>python 02_NGOAI_QUAN/scripts/build_crown_r6.py</code>.</p>
<details><summary>Xem JSON</summary><pre>%s</pre></details></section>
</main></body></html>""" % (CSS, tb, checks, "\n".join(figs), sup, opens, html.escape(json.dumps(data, ensure_ascii=False, indent=1)))
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(page)
    return OUT


if __name__ == "__main__":
    print(build())
