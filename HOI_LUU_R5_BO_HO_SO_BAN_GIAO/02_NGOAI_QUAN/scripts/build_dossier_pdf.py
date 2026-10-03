"""Render 01_HO_SO/HOI_LUU_R5_HO_SO_BAN_GIAO.md to PDF (A4 portrait text, A4 landscape plates for figures).

Requires a Chromium browser (Edge/Chrome) for printing; set BROWSER env var if not at the default Edge path.
Usage: python build_dossier_pdf.py
"""
import html, os, re, subprocess, shutil, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(os.path.dirname(HERE))
MD = os.path.join(PKG, "01_HO_SO", "HOI_LUU_R5_HO_SO_BAN_GIAO.md")
PDF = os.path.join(PKG, "01_HO_SO", "HOI_LUU_R5_HO_SO_BAN_GIAO.pdf")
BROWSER = os.environ.get("BROWSER", r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")

CSS = """
@page { size: A4 portrait; margin: 16mm 15mm 16mm 15mm; }
@page plate { size: A4 landscape; margin: 10mm 12mm; }
body { font-family: 'Segoe UI', Arial, sans-serif; font-size: 9.6pt; line-height: 1.42; color: #1d282d; }
h1 { font-size: 19pt; margin: 0 0 4mm; color: #1f3036; }
h2 { font-size: 13.5pt; margin: 7mm 0 2.5mm; color: #1f3036; border-bottom: 0.6pt solid #b9c4c7; padding-bottom: 1mm; break-after: avoid; }
h2.chapter { break-before: page; margin-top: 0; }
h3 { font-size: 11pt; margin: 4mm 0 2mm; break-after: avoid; }
p { margin: 1.6mm 0; text-align: left; }
table { border-collapse: collapse; width: 100%; margin: 2mm 0 3mm; font-size: 8.6pt; break-inside: auto; }
tr { break-inside: avoid; }
th, td { border: 0.5pt solid #c3cccf; padding: 1.2mm 1.8mm; vertical-align: top; text-align: left; }
th { background: #eaf0f1; }
blockquote { margin: 2mm 0; padding: 2mm 4mm; background: #eef3f4; border-left: 2pt solid #5f7c85; }
code { font-family: Consolas, monospace; font-size: 8.4pt; background: #f1f3f3; padding: 0 1mm; }
ul { margin: 1.5mm 0 1.5mm 5mm; padding-left: 3mm; }
li { margin: 0.6mm 0; }
.plate { page: plate; break-before: page; break-after: page; display: flex; flex-direction: column; height: 186mm; }
.plate h3 { margin: 0 0 2mm; font-size: 12pt; }
.plate .img { flex: 1; display: flex; align-items: center; justify-content: center; min-height: 0; }
.plate img { max-width: 100%; max-height: 166mm; }
.plate p { font-size: 8.8pt; color: #3d4b51; margin: 2mm 0 0; }
.cover { font-size: 10pt; }
"""


def inline(s, base):
    s = html.escape(s, quote=False)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', s)
    return s


def convert(md_text, base):
    lines = md_text.splitlines()
    out, i, first_h2 = [], 0, True
    while i < len(lines):
        ln = lines[i]
        if not ln.strip():
            i += 1
            continue
        if ln.startswith("### ") and i + 2 < len(lines) and any(lines[j].startswith("![") for j in range(i + 1, min(i + 3, len(lines)))):
            title = ln[4:].strip()
            j = i + 1
            while not lines[j].startswith("!["):
                j += 1
            m = re.match(r"!\[([^\]]*)\]\(([^)]+)\)", lines[j])
            src = "file:///" + os.path.normpath(os.path.join(base, m.group(2))).replace("\\", "/")
            k = j + 1
            cap = []
            while k < len(lines) and not lines[k].strip():
                k += 1
            while k < len(lines) and lines[k].strip() and not lines[k].startswith("#"):
                cap.append(lines[k].strip())
                k += 1
            out.append('<div class="plate"><h3>%s</h3><div class="img"><img src="%s" alt="%s"></div><p>%s</p></div>'
                       % (inline(title, base), src, html.escape(m.group(1)), inline(" ".join(cap), base)))
            i = k
            continue
        if ln.startswith("# "):
            out.append("<h1>%s</h1>" % inline(ln[2:], base))
        elif ln.startswith("## "):
            cls = "" if first_h2 else ' class="chapter"'
            first_h2 = False
            out.append("<h2%s>%s</h2>" % (cls, inline(ln[3:], base)))
        elif ln.startswith("### "):
            out.append("<h3>%s</h3>" % inline(ln[4:], base))
        elif ln.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            head, body = rows[0], [r for r in rows[1:] if not all(re.fullmatch(r":?-{3,}:?", c) for c in r)]
            t = "<table><tr>%s</tr>%s</table>" % ("".join("<th>%s</th>" % inline(c, base) for c in head),
                                                  "".join("<tr>%s</tr>" % "".join("<td>%s</td>" % inline(c, base) for c in r) for r in body))
            out.append(t)
            continue
        elif ln.startswith("> "):
            buf = []
            while i < len(lines) and lines[i].startswith(">"):
                buf.append(lines[i][1:].strip())
                i += 1
            out.append("<blockquote>%s</blockquote>" % inline(" ".join(buf), base))
            continue
        elif ln.startswith("- "):
            items = []
            while i < len(lines) and lines[i].startswith("- "):
                items.append(lines[i][2:])
                i += 1
            out.append("<ul>%s</ul>" % "".join("<li>%s</li>" % inline(x, base) for x in items))
            continue
        elif ln.startswith("```"):
            i += 1
            buf = []
            while i < len(lines) and not lines[i].startswith("```"):
                buf.append(lines[i])
                i += 1
            out.append("<pre>%s</pre>" % html.escape("\n".join(buf)))
        else:
            buf = [ln]
            while i + 1 < len(lines) and lines[i + 1].strip() and not re.match(r"(#|\||- |> |!\[|```)", lines[i + 1]):
                i += 1
                buf.append(lines[i])
            out.append("<p>%s</p>" % inline(" ".join(buf), base))
        i += 1
    return "\n".join(out)


def build():
    base = os.path.dirname(MD)
    body = convert(open(MD, encoding="utf-8").read(), base)
    page = '<!doctype html><html lang="vi"><head><meta charset="utf-8"><title>HỘI LƯU · Hồ sơ bàn giao đánh giá ngoại quan (R5 + R6-CROWN)</title><style>%s</style></head><body>%s</body></html>' % (CSS, body)
    tmp = tempfile.mkdtemp(prefix="hl_pdf_")
    src = os.path.join(tmp, "dossier.html")
    open(src, "w", encoding="utf-8").write(page)
    ud = os.path.join(tmp, "profile")
    subprocess.run([BROWSER, "--headless=new", "--disable-gpu", "--user-data-dir=" + ud, "--no-pdf-header-footer",
                    "--print-to-pdf-no-header", "--generate-pdf-document-outline", "--print-to-pdf=" + PDF,
                    "file:///" + src.replace("\\", "/")], timeout=300, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    shutil.rmtree(tmp, ignore_errors=True)
    data = open(PDF, "rb").read()
    pages = len(re.findall(rb"/Type\s*/Page[^s]", data))
    return PDF, pages, len(data)


if __name__ == "__main__":
    print(build())
