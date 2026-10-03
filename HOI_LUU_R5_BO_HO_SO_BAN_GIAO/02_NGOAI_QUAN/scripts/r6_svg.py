"""Minimal SVG writer + projection helpers shared by the R6 drawings."""
import math

FONT = "Segoe UI, Arial, sans-serif"


class Svg:
    def __init__(self, w, h, bg="#ffffff"):
        self.w, self.h, self.els, self.defs = w, h, [], []
        if bg:
            self.els.append('<rect width="%d" height="%d" fill="%s"/>' % (w, h, bg))

    def poly(self, pts, stroke="#333", w=1.0, fill="none", op=1.0, dash=None, cap="round", extra=""):
        if len(pts) < 2:
            return
        d = " ".join("%.1f,%.1f" % p for p in pts)
        da = ' stroke-dasharray="%s"' % dash if dash else ""
        self.els.append('<polyline points="%s" fill="%s" stroke="%s" stroke-width="%.2f" opacity="%.2f" '
                        'stroke-linejoin="round" stroke-linecap="%s"%s%s/>' % (d, fill, stroke, w, op, cap, da, extra))

    def polygon(self, pts, fill, op=1.0, stroke="none", w=0.0, extra=""):
        if len(pts) < 3:
            return
        d = " ".join("%.1f,%.1f" % p for p in pts)
        self.els.append('<polygon points="%s" fill="%s" fill-opacity="%.2f" stroke="%s" stroke-width="%.2f"%s/>'
                        % (d, fill, op, stroke, w, extra))

    def line(self, x1, y1, x2, y2, stroke="#bbb", w=0.6, dash=None, op=1.0):
        da = ' stroke-dasharray="%s"' % dash if dash else ""
        self.els.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%.2f" opacity="%.2f"%s/>'
                        % (x1, y1, x2, y2, stroke, w, op, da))

    def rect(self, x, y, w, h, fill, op=1.0, stroke="none", sw=0.0):
        self.els.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s" fill-opacity="%.2f" stroke="%s" stroke-width="%.2f"/>'
                        % (x, y, w, h, fill, op, stroke, sw))

    def text(self, x, y, s, size=11, anchor="start", color="#222", weight="normal", italic=False):
        st = ' font-style="italic"' if italic else ""
        s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        self.els.append('<text x="%.1f" y="%.1f" font-size="%d" text-anchor="%s" fill="%s" font-weight="%s" font-family="%s"%s>%s</text>'
                        % (x, y, size, anchor, color, weight, FONT, st, s))

    def raw(self, s):
        self.els.append(s)

    def clip_start(self, cid, x, y, w, h):
        self.defs.append('<clipPath id="%s"><rect x="%.1f" y="%.1f" width="%.1f" height="%.1f"/></clipPath>' % (cid, x, y, w, h))
        self.els.append('<g clip-path="url(#%s)">' % cid)

    def group_start(self, attrs=""):
        self.els.append("<g %s>" % attrs)

    def group_end(self):
        self.els.append("</g>")

    def title_block(self, code, title, note):
        self.text(28, 34, title, 18, weight="bold")
        self.text(28, self.h - 18, code + "  ·  " + note, 10, color="#5a6973")

    def save(self, path):
        defs = "<defs>%s</defs>" % "".join(self.defs) if self.defs else ""
        s = ('<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">%s%s</svg>'
             % (self.w, self.h, self.w, self.h, defs, "\n".join(self.els)))
        with open(path, "w", encoding="utf-8") as f:
            f.write(s)
        return s


def view_axes(beta_deg):
    """Viewer looks along d=(cos b, sin b); returns (right, d)."""
    b = math.radians(beta_deg)
    d = (math.cos(b), math.sin(b))
    right = (d[1], -d[0])
    return right, d


def proj(p, right):
    return p[0] * right[0] + p[1] * right[1]


def depth(p, d):
    return p[0] * d[0] + p[1] * d[1]
