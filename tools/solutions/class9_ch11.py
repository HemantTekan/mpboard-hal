#!/usr/bin/env python3
"""Class 9 Maths, Chapter 11 (पृष्ठीय क्षेत्रफल और आयतन): Exercises 11.1, 11.2, 11.3 and 11.4, Hindi medium.
Rationalised book (2023-24 onward; NCERT iemh111 'Rationalised Textbooks 2022-23', print 2024-25) = old chapter 13:
  cuboid / cylinder sections and old प्रश्नावली 13.1, 13.2, 13.5, 13.6 and 13.9 (ऐच्छिक) removed;
  11.1 = old 13.3 (8 Q, cone surface area), 11.2 = old 13.4 (9 Q, sphere surface area),
  11.3 = old 13.7 (9 Q, cone volume), 11.4 = old 13.8 (10 Q, sphere volume); question numbers unchanged.
  Figure renumbered like the current book: old 13.22 (cylinder enclosing a sphere) -> 11.10.
  One change in the rationalised book: 11.4 Q8 white-washing cost ₹4989.60 at ₹20 per m² (old print: ₹498.96 at ₹2);
  the area (249.48 m²) and the answers are the same. The current numbers are used here.
Question text copied from NCERT Hindi PDF ihmh113 (archive.org ncert-ihmh1, chapter 13 of the 2020-21 print).
User rules: ज्ञात है / ज्ञात करना है first; one '=' per line, aligned; no step skipped; formula boxes; prime factors and
pairs under every square root; π = 22/7 unless the question says otherwise; units everywhere; figures to true
proportions, colour-coded (r red, h blue, l green, d orange, outer radius purple) with the same colours in the working;
no जाँच boxes and no extra 'लगभग' values unless the question asks. Answers are checked privately with asserts.
Run from repo root: python3 tools/solutions/class9_ch11.py
"""
import sys, pathlib, math, re
from fractions import Fraction as F
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from common import *  # noqa
from mixed_cells import *  # noqa

BASE = "/hi/class-09/maths/chapter-11/"
CH = "पृष्ठीय क्षेत्रफल और आयतन"
BOARDS11 = ("यह हल <b>MP Board (MPBSE)</b> कक्षा 9 गणित की पाठ्यपुस्तक के अध्याय 11 ‘पृष्ठीय क्षेत्रफल और आयतन’ के अनुसार है।")
EXTRA_CSS = """
.fig{margin:10px 0;text-align:center}.fig svg{width:100%;height:auto;background:#fbfcff;border:1px solid #e3e8f4;border-radius:12px}
.fig .cap{font-size:.85em;color:#5a6275;margin-top:4px}
.figs{display:grid;grid-template-columns:1fr 1fr;gap:10px}.figs .fig{margin:6px 0}
@media (max-width:640px){.figs{grid-template-columns:1fr}}
.tp{background:#fff4ec;border-left:4px solid #e8711a;border-radius:8px;padding:5px 10px;margin:6px 0;font-size:.95em}
.kh{font-weight:700;color:#1d3a8a;margin:14px 0 2px}
.ans .al{margin:10px 0}
.key{display:flex;flex-wrap:wrap;gap:6px 14px;font-size:.9em;margin:4px 0 8px}
.key span{display:inline-flex;align-items:center;gap:5px}.key i{display:inline-block;width:14px;height:14px;border-radius:4px}
.nofig{font-size:.85em;color:#5a6275;margin:2px 0 6px}
.frm{font-size:.97em}.frm .katex{font-size:1.05em}
.eq .l{white-space:nowrap}
.lads{gap:10px 12px}.lad{padding:6px 10px}.lad .lt{font-size:13.5px}.lad .ladder td{padding:1px 8px}.lad .fl{font-size:15px}
@media (max-width:420px){.part .eq{padding:8px 8px}.eq .katex{font-size:.95em}}
.pin{background:#eef4ff;border:1px dashed #8db7ef;border-radius:10px;padding:6px 12px;margin:0 0 14px;font-size:.95em}
"""

# ---------------- colours (same in figures and in the working) ----------------
INK = "#1d3a8a"
RED, BLU, GRN, ORG, PUR, TEA = "#d62839", "#1769c2", "#0f8a4c", "#e06a00", "#7c3aed", "#0e8a9a"
FONT = "font-family=\"Noto Sans, 'Noto Sans Devanagari', sans-serif\""
FILL = "#cfe6fb"


def C(col, t):
    return "\\textcolor{" + col + "}{" + t + "}"


def r_(t="r"):
    return C(RED, t)


def h_(t="h"):
    return C(BLU, t)


def l_(t="l"):
    return C(GRN, t)


def d_(t="d"):
    return C(ORG, t)


def R_(t="R"):
    return C(PUR, t)


def kh(t):
    return f"<div class='kh'>{t}</div>"


def tp(t):
    return f"<div class='tp'>{t}</div>"


def key(*items):
    return "<div class='key'>" + "".join(f"<span><i style='background:{c}'></i>{t}</span>" for c, t in items) + "</div>"


def check_tex(E):
    import re as _re
    for _q, _sol in E:
        for _t in _re.findall(r"\\\((.+?)\\\)", _q + _sol):
            assert not _re.search(r"[\u0900-\u097F]", _t), ("Devanagari in TeX", _t)


NOFIG = "<div class='nofig'>(पुस्तक में इस प्रश्न की आकृति नहीं दी है; नीचे हल के लिए आकृति बनाई गई है।)</div>"


def solo(f):
    return f"<div style='max-width:400px;margin:0 auto'>{f}</div>"


def pair(a, b):
    return f"<div class='figs'>{a}{b}</div>"


# ---------------- numbers ----------------
def dec(v):
    """Fraction -> TeX: integer, terminating decimal, or a fraction."""
    v = F(v)
    if v.denominator == 1:
        return str(v.numerator)
    q = v.denominator
    while q % 2 == 0:
        q //= 2
    while q % 5 == 0:
        q //= 5
    if q == 1:
        s = f"{float(v):.10f}".rstrip("0").rstrip(".")
        assert F(s) == v
        return s
    return f"\\dfrac{{{v.numerator}}}{{{v.denominator}}}"


def mixed(v):
    v = F(v)
    a, b = divmod(v.numerator, v.denominator)
    return f"{a}\\tfrac{{{b}}}{{{v.denominator}}}" if a else f"\\dfrac{{{b}}}{{{v.denominator}}}"


def U(u, p=1):
    if not u:
        return ""
    return f"\\ \\text{{{u}}}" + (f"^{p}" if p > 1 else "")


def frac_tex(v):
    v = F(v)
    return str(v.numerator) if v.denominator == 1 else f"\\dfrac{{{v.numerator}}}{{{v.denominator}}}"


def chain(lhs, factors, unit="", p=1, want=None, tail=None, conv=True, mix=False, pre=()):
    """lhs = product of factors, step by step (one '=' per row).
    factors: list of (tex shown, Fraction value).  Rows: substitution; decimals as fractions; one fraction;
    common factors cancelled; the value (terminating decimal / fraction / mixed number).  Asserts value == want."""
    u = U(unit, p)
    val = math.prod((F(v) for _, v in factors), start=F(1))
    if want is not None:
        assert val == F(want), (lhs, val, want)
    rows = list(pre) + ["\\times ".join(t for t, _ in factors) + u]
    nums = [F(v).numerator for _, v in factors]
    dens = [F(v).denominator for _, v in factors if F(v).denominator != 1]
    has_dec = any(F(v).denominator != 1 and "frac" not in t for t, v in factors)
    if has_dec and conv:
        rows.append("\\times ".join(frac_tex(v) for _, v in factors) + u)
    if dens:
        if len(factors) > 1:
            rows.append(f"\\dfrac{{{'\\times '.join(map(str, nums))}}}{{{'\\times '.join(map(str, dens))}}}" + u)
        n2, d2 = nums[:], dens[:]
        for i in range(len(n2)):
            for j in range(len(d2)):
                g = math.gcd(n2[i], d2[j])
                n2[i] //= g
                d2[j] //= g
        n3 = [x for x in n2 if x != 1] or [1]
        d3 = [x for x in d2 if x != 1]
        if (n3, d3) != ([x for x in nums if x != 1] or [1], [x for x in dens if x != 1]):
            if d3:
                rows.append(f"\\dfrac{{{'\\times '.join(map(str, n3))}}}{{{'\\times '.join(map(str, d3))}}}" + u)
            else:
                rows.append("\\times ".join(map(str, n3)) + u)
        N, D = math.prod(n3), math.prod(d3)
        assert F(N, D) == val
        if D > 1 and (len(n3) > 1 or len(d3) > 1):
            rows.append(f"\\dfrac{{{N}}}{{{D}}}" + u)
        elif D == 1 and len(n3) > 1:
            rows.append(str(N) + u)
        if D > 1 and "frac" not in dec(val):
            rows.append(dec(val) + u)
        elif D > 1 and mix and val > 1:
            rows.append(mixed(val) + u)
    elif len(factors) > 1:
        rows.append(str(val) + u)
    if tail:
        rows += [t + u for t in tail]
    return lines(lhs, *rows), val


def pairs_tex(ps):
    """(p×p)×(q×q)...; four or more pairs go on two rows so the line fits a phone."""
    g = [f"({a}\\times {a})" for a in ps]
    if len(g) < 4:
        return "\\times ".join(g)
    h = (len(g) + 1) // 2
    return "\\begin{array}{l}" + "\\times ".join(g[:h]) + "\\\\ \\times " + "\\times ".join(g[h:]) + "\\end{array}"


def sq_rows(v, unit="", col=None):
    """√v for a perfect-square Fraction v: factorisation, pairs, root. Returns rows (after '√v')."""
    v = F(v)
    n, d = v.numerator, v.denominator
    u = U(unit)
    if d == 1 and "." not in str(v):
        fs = factors(n)
        assert math.isqrt(n) ** 2 == n
        rows = [f"\\sqrt{{{'\\times '.join(map(str, fs))}}}" + u,
                f"\\sqrt{{{pairs_tex(fs[::2])}}}" + u,
                ("\\times ".join(map(str, fs[::2])) + u) if len(fs) > 2 else None,
                str(math.isqrt(n)) + u]
        return [r for r in rows if r]
    # decimal: write as N/100 etc (keep the printed decimal's power of ten)
    s = dec(v)
    k = len(s.split(".")[1]) if "." in s else 0
    N, D = int(v * 10 ** k), 10 ** k
    assert F(N, D) == v and math.isqrt(N) ** 2 == N and math.isqrt(D) ** 2 == D
    fN, fD = factors(N), factors(D)
    rN, rD = math.isqrt(N), math.isqrt(D)
    rows = [f"\\sqrt{{\\dfrac{{{N}}}{{{D}}}}}" + u,
            f"\\sqrt{{\\dfrac{{{'\\times '.join(map(str, fN))}}}{{{'\\times '.join(map(str, fD))}}}}}" + u,
            f"\\sqrt{{\\dfrac{{{'\\times '.join(f'({a}\\times {a})' for a in fN[::2])}}}{{{'\\times '.join(f'({a}\\times {a})' for a in fD[::2])}}}}}" + u,
            f"\\dfrac{{{'\\times '.join(map(str, fN[::2]))}}}{{{'\\times '.join(map(str, fD[::2]))}}}" + u,
            f"\\dfrac{{{rN}}}{{{rD}}}" + u,
            dec(F(rN, rD)) + u]
    return rows


def pyth(lhs_t, a, at, acol, b, bt, bcol, unit, mode="+"):
    """lhs = √(a² ± b²) with numbers, then factor pairs and the root.  Returns (html, value)."""
    a, b = F(a), F(b)
    s = a * a + b * b if mode == "+" else a * a - b * b
    rt = F(math.isqrt(int(s * 10000)), 100)
    assert rt * rt == s
    op = "+" if mode == "+" else "-"
    rows = [f"\\sqrt{{{C(acol, at)}^2{op}{C(bcol, bt)}^2}}" + U(unit),
            f"\\sqrt{{{dec(a * a)}{op}{dec(b * b)}}}" + U(unit),
            f"\\sqrt{{{dec(s)}}}" + U(unit)]
    rows += sq_rows(s, unit)
    return rows, rt


def lad_for(v):
    v = F(v)
    s = dec(v)
    k = len(s.split(".")[1]) if "." in s else 0
    N = int(v * 10 ** k)
    out = [N] + ([10 ** k] if k else [])
    return p("अभाज्य गुणनखंड (भाग-विधि से):") + ladders(*out)


# ---------------- formula boxes ----------------
def f_csa():
    return formula("शंकु का वक्र पृष्ठीय क्षेत्रफल", "वक्र पृष्ठीय क्षेत्रफल " + m(f"= \\pi {r_()} {l_()}") +
                   ", जहाँ " + m(r_()) + " = आधार की त्रिज्या, " + m(l_()) + " = तिर्यक ऊँचाई")


def f_tsa():
    return formula("शंकु का कुल पृष्ठीय क्षेत्रफल", "कुल पृष्ठीय क्षेत्रफल " + m(f"= \\pi {r_()} {l_()} + \\pi {r_()}^2 = \\pi {r_()}({l_()} + {r_()})"))


def f_l():
    return formula("तिर्यक ऊँचाई", m(f"{l_()} = \\sqrt{{{h_()}^2 + {r_()}^2}}") + " (क्योंकि " +
                   m(f"{l_()}^2 = {h_()}^2 + {r_()}^2") + ", पाइथागोरस प्रमेय)")


def f_sph():
    return formula("गोले का पृष्ठीय क्षेत्रफल", "पृष्ठीय क्षेत्रफल " + m(f"= 4\\pi {r_()}^2"))


def f_hcsa(col=RED, t="r"):
    return formula("अर्धगोले का वक्र पृष्ठीय क्षेत्रफल", "वक्र पृष्ठीय क्षेत्रफल " + m(f"= 2\\pi {C(col, t)}^2"))


def f_htsa():
    return formula("अर्धगोले का कुल पृष्ठीय क्षेत्रफल", "कुल पृष्ठीय क्षेत्रफल " + m(f"= 2\\pi {r_()}^2 + \\pi {r_()}^2 = 3\\pi {r_()}^2"))


def f_vcone():
    return formula("शंकु का आयतन", "आयतन " + m(f"= \\dfrac{{1}}{{3}}\\pi {r_()}^2 {h_()}"))


def f_vsph():
    return formula("गोले का आयतन", "आयतन " + m(f"= \\dfrac{{4}}{{3}}\\pi {r_()}^3"))


def f_vhem():
    return formula("अर्धगोले का आयतन", "आयतन " + m(f"= \\dfrac{{2}}{{3}}\\pi {r_()}^3"))


def eqsu(u, *pairs):
    """eqs with the unit written on every RHS that has none (u like 'cm^2'); r^2 rows get the squared unit,
    a row whose LHS is r, h or d gets the plain unit."""
    base, _, pw = u.partition("^")
    out = []
    for a, b in pairs:
        if "\\text{" in b:
            out.append((a, b))
            continue
        a0 = re.sub(r"\\textcolor\{[^}]*\}\{([^}]*)\}", r"\1", a).strip()
        if a0 in ("r", "h", "d"):
            uu = f"\\ \\text{{{base}}}"
        elif a0 in ("r^2", "h^2"):
            uu = f"\\ \\text{{{base}}}^2"
        else:
            uu = f"\\ \\text{{{base}}}" + (f"^{pw}" if pw else "")
        out.append((a, b + uu))
    return eqs(*out)


PI = ("\\dfrac{22}{7}", F(22, 7))
PI314 = ("3.14", F(314, 100))


# ---------------- SVG figure kit ----------------
class Fig:
    n = 0

    def __init__(self, W, H):
        Fig.n += 1
        self.id, self.W, self.H, self.bg, self.el, self.top, self.marks = f"f11{Fig.n}", W, H, [], [], [], {}

    def _mk(self, col):
        if col not in self.marks:
            self.marks[col] = f"{self.id}m{len(self.marks)}"
        return self.marks[col]

    def line(self, p, q, col=INK, w=2.2, dash=None, a1=False, a2=False):
        d = f" stroke-dasharray='{dash}'" if dash else ""
        ms = f" marker-start='url(#{self._mk(col)})'" if a1 else ""
        me = f" marker-end='url(#{self._mk(col)})'" if a2 else ""
        self.el.append(f"<line x1='{p[0]:.1f}' y1='{p[1]:.1f}' x2='{q[0]:.1f}' y2='{q[1]:.1f}' stroke='{col}' stroke-width='{w}' "
                       f"stroke-linecap='round'{d}{ms}{me}/>")

    def path(self, d, col=INK, w=2.2, fill="none", op=1, dash=None, layer="el"):
        ds = f" stroke-dasharray='{dash}'" if dash else ""
        getattr(self, layer).append(f"<path d='{d}' fill='{fill}' fill-opacity='{op}' stroke='{col}' stroke-width='{w}' "
                                    f"stroke-linejoin='round'{ds}/>")

    def text(self, x, y, t, col=INK, size=14, bold=True, anchor="middle", italic=False):
        st = " font-style='italic'" if italic else ""
        self.top.append(f"<text x='{x:.1f}' y='{y:.1f}' font-size='{size}' font-weight='{700 if bold else 500}' fill='{col}' "
                        f"text-anchor='{anchor}' dominant-baseline='central'{st} stroke='#fbfcff' stroke-width='4' "
                        f"stroke-linejoin='round' paint-order='stroke'>{t}</text>")

    def dot(self, p, col=INK, r=3):
        self.top.insert(0, f"<circle cx='{p[0]:.1f}' cy='{p[1]:.1f}' r='{r}' fill='{col}'/>")

    def right(self, o, ux, uy, vx, vy, s=9, col=INK):
        p1 = (o[0] + ux * s, o[1] + uy * s)
        p3 = (o[0] + vx * s, o[1] + vy * s)
        p2 = (p1[0] + vx * s, p1[1] + vy * s)
        self.el.append(f"<path d='M{p1[0]:.1f},{p1[1]:.1f} L{p2[0]:.1f},{p2[1]:.1f} L{p3[0]:.1f},{p3[1]:.1f}' fill='none' stroke='{col}' stroke-width='1.6'/>")

    def svg(self, cap, maxw=None):
        defs = "".join(f"<marker id='{mid}' viewBox='0 0 10 10' refX='8.5' refY='5' markerWidth='10' markerHeight='10' "
                       f"markerUnits='userSpaceOnUse' orient='auto-start-reverse'><path d='M0,0.5 L10,5 L0,9.5 L2.6,5 z' fill='{col}'/></marker>"
                       for col, mid in self.marks.items())
        grad = (f"<radialGradient id='{self.id}g' cx='38%' cy='34%' r='70%'><stop offset='0' stop-color='#ffffff'/>"
                f"<stop offset='.55' stop-color='#8fd0f5'/><stop offset='1' stop-color='#1e88d0'/></radialGradient>")
        mw = maxw or max(self.W, 300)
        return (f"<div class='fig'><svg viewBox='0 0 {self.W} {self.H}' role='img' aria-label='{cap}' style='max-width:{mw}px' {FONT}>"
                f"<defs>{defs}{grad}</defs>{''.join(self.bg)}{''.join(self.el)}{''.join(self.top)}</svg><div class='cap'>{cap}</div></div>")


def ell(cx, cy, rx, ry, half="full"):
    """SVG path of an ellipse (full), its front (lower) half or back (upper) half."""
    if half == "full":
        return f"M{cx - rx:.1f},{cy:.1f} A{rx:.1f},{ry:.1f} 0 1 0 {cx + rx:.1f},{cy:.1f} A{rx:.1f},{ry:.1f} 0 1 0 {cx - rx:.1f},{cy:.1f}"
    if half == "front":
        return f"M{cx - rx:.1f},{cy:.1f} A{rx:.1f},{ry:.1f} 0 0 0 {cx + rx:.1f},{cy:.1f}"
    return f"M{cx - rx:.1f},{cy:.1f} A{rx:.1f},{ry:.1f} 0 0 1 {cx + rx:.1f},{cy:.1f}"


def cone_fig(r, h, cap, labs, W=300, H=230, unit="cm", tri=None, maxw=None):
    """Right circular cone drawn to scale (radius r, height h in the same unit).
    labs: dict with any of 'r', 'h', 'l', 'd' -> label text; the segment is drawn in its colour.
    The right edge (apex to rim end) has true length k·l in the drawing."""
    mt, mb = (44 if tri else 22), 14
    lw = 0 if "l" not in labs else 0.55 * 13 * len(labs["l"]) * 0.7 + 14
    mx = max(22, lw)
    k = min((W - 2 * mx) / (2 * float(r)), (H - mt - mb - 30) / float(h))
    rx = k * float(r)
    ry = max(5.0, min(0.22 * rx, 18))
    bot = 22 if ("r" in labs or "d" in labs) else 0
    H = int(mt + k * float(h) + ry + bot + mb + 6)
    cx = W / 2
    cy = H - mb - ry - bot
    A = (cx, cy - k * float(h))
    L, R = (cx - rx, cy), (cx + rx, cy)
    close(math.dist(A, R), k * math.sqrt(float(r) ** 2 + float(h) ** 2))
    f = Fig(W, H)
    f.path(f"M{A[0]:.1f},{A[1]:.1f} L{L[0]:.1f},{L[1]:.1f} " + ell(cx, cy, rx, ry, "front")[ell(cx, cy, rx, ry, "front").index("A"):] +
           " Z", "none", 0, FILL, .8, layer="bg")
    f.path(ell(cx, cy, rx, ry, "back"), INK, 1.4, dash="5 4")
    f.path(ell(cx, cy, rx, ry, "front"), INK, 2.2)
    f.line(A, L, INK, 2.2)
    f.line(A, R, GRN if "l" in labs else INK, 3.2 if "l" in labs else 2.2)
    O = (cx, cy)
    if "h" in labs:
        f.line(A, O, BLU, 2.4, dash="6 4")
        f.right(O, 1, 0, 0, -1, 8, BLU)
        f.text(cx - 6, (A[1] + cy) / 2, labs["h"], BLU, 13, anchor="end")
    if "r" in labs:
        f.line(O, R, RED, 2.8)
        wr = 0.55 * 13 * len(labs["r"]) / 2
        f.text(min(max((cx + R[0]) / 2, cx + wr - 4), W - wr - 4), cy + ry + 12, labs["r"], RED, 13)
    if "d" in labs:
        f.line(L, R, ORG, 2.8, a1=True, a2=True)
        f.text(cx, cy + ry + 12, labs["d"], ORG, 13)
    if "l" in labs:
        mxp, myp = (A[0] + R[0]) / 2, (A[1] + R[1]) / 2
        dx, dy = R[0] - A[0], R[1] - A[1]
        LL = math.hypot(dx, dy)
        nx, ny = dy / LL, -dx / LL
        w = 0.55 * 13 * len(labs["l"])
        off = 9 + abs(nx) * w / 2 + abs(ny) * 8
        f.text(mxp + nx * off, myp + ny * off, labs["l"], GRN, 13)
    f.dot(O, INK, 2.6)
    if tri:
        # right triangle that is turned: apex A, centre O (right angle), rim point R
        f.path(f"M{A[0]:.1f},{A[1]:.1f} L{O[0]:.1f},{O[1]:.1f} L{R[0]:.1f},{R[1]:.1f} Z", "none", 0, "#f4b400", .35, layer="bg")
        for nm, pt, dx_, dy_ in zip(tri, (A, O, R), (13, -12, 12), (-4, 12, 0)):
            f.text(pt[0] + dx_, pt[1] + dy_, nm, INK, 14)
        f.line((cx, A[1]), (cx, A[1] - 34), PUR, 1.6, dash="4 3")
        f.el.append(f"<path d='M{cx - 18:.1f},{A[1] - 22:.1f} A18,6 0 1 0 {cx + 18:.1f},{A[1] - 22:.1f}' fill='none' stroke='{PUR}' "
                    f"stroke-width='1.8' marker-end='url(#{f._mk(PUR)})'/>")
    for pt in (A, L, R):
        assert 4 < pt[0] < W - 4 and 4 < pt[1] < H - 4, (cap, pt)
    return f.svg(cap, maxw)


def sphere_fig(r_px, cap, lab=None, dlab=None, W=260, H=230, maxw=None, cx=None, cy=None, f=None, ret=False):
    f = f or Fig(W, H)
    cx = W / 2 if cx is None else cx
    cy = H / 2 if cy is None else cy
    f.bg.append(f"<circle cx='{cx:.1f}' cy='{cy:.1f}' r='{r_px:.1f}' fill='{FILL}' fill-opacity='.85' stroke='{INK}' stroke-width='2.2'/>")
    ry = 0.26 * r_px
    f.path(ell(cx, cy, r_px, ry, "back"), INK, 1.3, dash="5 4")
    f.path(ell(cx, cy, r_px, ry, "front"), INK, 1.6)
    O = (cx, cy)
    f.dot(O)
    if lab:
        f.line(O, (cx + r_px, cy), RED, 2.8)
        f.text(cx + r_px / 2, cy - ry - 10, lab, RED, 13)
    if dlab:
        f.line((cx - r_px, cy), (cx + r_px, cy), ORG, 2.8, a1=True, a2=True)
        f.text(cx, cy - ry - 10, dlab, ORG, 13)
    f.text(cx - 8, cy + 10, "O", INK, 13)
    if ret:
        return f
    return f.svg(cap, maxw)


def hemi_fig(r, cap, lab=None, dlab=None, R=None, Rlab=None, dome=False, solid=False, W=300, H=190, maxw=None, tnote=None,
             draw_R=None):
    """Hemisphere.  dome=False: bowl (open face up); dome=True: dome (curved face up) on its circular base.
    R: outer radius (thickness R - r) drawn as given by draw_R (true unless the thickness is too thin to see)."""
    f = Fig(W, H)
    Rr = draw_R or R or r
    k = min((W - 70) / (2 * float(Rr)), (H - 50) / float(Rr) / 1.05)
    rp, Rp = k * float(r), k * float(Rr)
    cx = W / 2
    ryR, ry = 0.25 * Rp, 0.25 * rp
    if not dome:
        cy = 26 + ryR
        outer = f"M{cx - Rp:.1f},{cy:.1f} A{Rp:.1f},{Rp:.1f} 0 0 0 {cx + Rp:.1f},{cy:.1f}"
        f.path(outer + " " + f"A{Rp:.1f},{ryR:.1f} 0 0 0 {cx - Rp:.1f},{cy:.1f}", "none", 0, FILL, .85, layer="bg")
        f.path(ell(cx, cy, rp, ry, "full"), INK, 1.8, fill="#eef7ff", op=1)
        f.path(f"M{cx - rp:.1f},{cy:.1f} A{rp:.1f},{rp:.1f} 0 0 0 {cx + rp:.1f},{cy:.1f}", INK, 1.3, dash="5 4")
        f.path(outer, INK, 2.2)
        if R:
            f.path(ell(cx, cy, Rp, ryR, "full"), INK, 2)
    else:
        cy = H - 22 - ryR
        outer = f"M{cx - Rp:.1f},{cy:.1f} A{Rp:.1f},{Rp:.1f} 0 0 1 {cx + Rp:.1f},{cy:.1f}"
        f.path(outer + f" A{Rp:.1f},{ryR:.1f} 0 0 1 {cx - Rp:.1f},{cy:.1f}", "none", 0, FILL, .85, layer="bg")
        if solid:
            f.path(ell(cx, cy, Rp, ryR, "full"), INK, 1.8, fill="#9fd0f2", op=.6)
        else:
            f.path(ell(cx, cy, Rp, ryR, "back"), INK, 1.3, dash="5 4")
            f.path(ell(cx, cy, Rp, ryR, "front"), INK, 2)
        f.path(outer, INK, 2.2)
    O = (cx, cy)
    f.dot(O)
    if lab:
        f.line(O, (cx + rp, cy), RED, 2.8)
        f.text(cx + rp / 2, cy + (13 if not dome else -12), lab, RED, 13)
    if dlab:
        f.line((cx - rp, cy), (cx + rp, cy), ORG, 2.8, a1=True, a2=True)
        f.text(cx, cy - 12 if not dome else cy - 12, dlab, ORG, 13)
    if R and Rlab:
        ang = math.radians(-50)
        P = (cx + Rp * math.cos(ang), cy - Rp * math.sin(ang))
        f.line(O, P, PUR, 2.4)
        f.text(P[0] + 8, P[1] + 10, Rlab, PUR, 13, anchor="start")
    if tnote:
        f.text(cx, H - 9, tnote, "#5a6275", 11, bold=False)
    return f.svg(cap, maxw)


def cyl_sphere_fig(cap, sol=False, W=230, H=250):
    """Fig. 11.10: a right circular cylinder just enclosing a sphere (cylinder radius r, height 2r)."""
    f = Fig(W, H)
    rp = 78
    cx, cy = W / 2, H / 2 + 2
    ry = 18
    top, bot = cy - rp, cy + rp
    f.bg.append(f"<rect x='{cx - rp:.1f}' y='{top:.1f}' width='{2 * rp}' height='{2 * rp}' fill='#f3f8ff'/>")
    f.path(ell(cx, bot, rp, ry, "back"), INK, 1.3, dash="5 4")
    f.top.insert(0, f"<circle cx='{cx:.1f}' cy='{cy:.1f}' r='{rp}' fill='url(#{f.id}g)' stroke='#1e88d0' stroke-width='1.2'/>")
    f.path(ell(cx, bot, rp, ry, "front"), INK, 2)
    f.path(ell(cx, top, rp, ry, "full"), INK, 1.6, dash="5 4" if not sol else None)
    f.line((cx - rp, top), (cx - rp, bot), INK, 2)
    f.line((cx + rp, top), (cx + rp, bot), INK, 2)
    if sol:
        O = (cx, cy)
        f.top.append(f"<circle cx='{cx}' cy='{cy}' r='3' fill='{INK}'/>")
        f.top.append(f"<line x1='{cx}' y1='{cy}' x2='{cx + rp}' y2='{cy}' stroke='{RED}' stroke-width='2.8'/>")
        f.text(cx + rp / 2, cy - 11, "r", RED, 15, italic=True)
        f.text(cx - 8, cy + 11, "O", INK, 13)
        x = cx + rp + 16
        f.line((x, top), (x, bot), BLU, 2, a1=True, a2=True)
        f.text(x + 4, cy + 34, "2r", BLU, 14, anchor="start", italic=True)
        f.line((cx - rp, bot + ry + 12), (cx + rp, bot + ry + 12), ORG, 2, a1=True, a2=True)
        f.text(cx, bot + ry + 24, "2r", ORG, 14, italic=True)
        del O
    return f.svg(cap, 260)


def two_spheres(cap, ratio, labs, names, cols=(BLU, RED), W=320, H=190):
    """Two spheres whose radii are in the true ratio `ratio` (big : small)."""
    f = Fig(W, H)
    R = 70
    rs = R / ratio
    cy = H / 2 + 6
    c1, c2 = 20 + R, W - 30 - max(rs, 22)
    f = sphere_fig(R, cap, None, None, W, H, cx=c1, cy=cy, f=f, ret=True)
    f = sphere_fig(rs, cap, None, None, W, H, cx=c2, cy=cy + R - rs, f=f, ret=True)
    f.line((c1, cy), (c1 + R, cy), cols[0], 2.8)
    f.text(c1 + R / 2, cy - 12, labs[0], cols[0], 13)
    f.line((c2, cy + R - rs), (c2 + rs, cy + R - rs), cols[1], 2.6)
    f.text(c2, cy + R - 2 * rs - 14, labs[1], cols[1], 13)
    f.text(c1, cy - R - 10, names[0], INK, 13)
    f.text(c2, cy + R - 2 * rs - 34, names[1], INK, 13)
    return f.svg(cap)


# ======================= helpers for the working =======================
def r_from_d(dv, unit, col=ORG):
    """r = d/2 rows."""
    dv = F(dv)
    return lines(r_(), f"\\dfrac{{{d_()}}}{{2}}", f"\\dfrac{{{C(col, dec(dv))}}}{{2}}" + U(unit), r_(dec(dv / 2)) + U(unit))


def ans_(t):
    return ans(t)


def q_(t):
    return qt(t)


cm2, m2 = m("\\text{cm}^2"), m("\\text{m}^2")
cm3, m3 = m("\\text{cm}^3"), m("\\text{m}^3")


T_CSA = "\\text{वक्र पृष्ठीय क्षेत्रफल}"
T_TSA = "\\text{कुल पृष्ठीय क्षेत्रफल}"
T_SA = "\\text{पृष्ठीय क्षेत्रफल}"
T_V = "\\text{आयतन}"
PIR_L = f"\\pi {r_()} {l_()}"
ANS = {}


def pi_r_l(rv, rt, lv, lt, unit, want, pi=PI, mix=False):
    return chain(T_CSA, [pi, (r_(rt), rv), (l_(lt), lv)], unit, 2, want, pre=[PIR_L], mix=mix)


def sph_sa(rv, rt, unit, want, lhs=T_SA, col=RED):
    return chain(lhs, [("4", 4), PI, (C(col, rt), rv), (C(col, rt), rv)], unit, 2, want,
                 pre=[f"4\\pi {C(col, 'r')}^2"])


def cone_v(rv, rt, hv, ht, unit, want, mix=False, lhs=T_V):
    return chain(lhs, [("\\dfrac{1}{3}", F(1, 3)), PI, (r_(rt), rv), (r_(rt), rv), (h_(ht), hv)], unit, 3, want,
                 pre=[f"\\dfrac{{1}}{{3}}\\pi {r_()}^2 {h_()}"], mix=mix)


def sph_v(rv, rt, unit, want, mix=False, lhs=T_V, frac=("\\dfrac{4}{3}", F(4, 3)), sym="\\dfrac{4}{3}"):
    return chain(lhs, [frac, PI, (r_(rt), rv), (r_(rt), rv), (r_(rt), rv)], unit, 3, want,
                 pre=[f"{sym}\\pi {r_()}^3"], mix=mix)


# ======================= प्रश्नावली 11.1 (शंकु का पृष्ठीय क्षेत्रफल) =======================
E1 = []

# ---- Q1 ----
s = given("शंकु के आधार का व्यास " + m(f"{d_()} = 10.5\\ \\text{{cm}}") + "<br>तिर्यक ऊँचाई " + m(f"{l_()} = 10\\ \\text{{cm}}"),
          "शंकु का वक्र पृष्ठीय क्षेत्रफल")
s += NOFIG + solo(cone_fig(F(21, 4), math.sqrt(100 - 5.25 ** 2), "हल की आकृति: शंकु (पैमाने पर); व्यास d नारंगी, तिर्यक ऊँचाई l हरी",
                           {"d": "d = 10.5 cm", "l": "l = 10 cm"}))
s += kh("आधार की त्रिज्या " + m(r_()) + " ज्ञात करना") + r_from_d(F(21, 2), "cm")
s += f_csa()
w, v = pi_r_l(F(21, 4), "5.25", 10, "10", "cm", 165)
s += w
s += ans("शंकु का वक्र पृष्ठीय क्षेत्रफल " + m("= 165\\ \\text{cm}^2") + " है।")
ANS["11.1 Q1"] = "165 cm²"
E1.append(("एक शंकु के आधार का व्यास 10.5 cm है और इसकी तिर्यक ऊँचाई 10 cm है। इसका वक्र पृष्ठीय क्षेत्रफल ज्ञात कीजिए।", s))

# ---- Q2 ----
s = given("तिर्यक ऊँचाई " + m(f"{l_()} = 21\\ \\text{{m}}") + "<br>आधार का व्यास " + m(f"{d_()} = 24\\ \\text{{m}}"),
          "शंकु का कुल पृष्ठीय क्षेत्रफल")
s += NOFIG + solo(cone_fig(12, math.sqrt(21 ** 2 - 12 ** 2), "हल की आकृति: शंकु (पैमाने पर); व्यास d नारंगी, तिर्यक ऊँचाई l हरी",
                           {"d": "d = 24 m", "l": "l = 21 m"}, unit="m"))
s += kh("आधार की त्रिज्या " + m(r_()) + " ज्ञात करना") + r_from_d(24, "m")
s += f_tsa()
w, v = chain(T_TSA, [PI, (r_("12"), 12), ("33", 33)], "m", 2, F(8712, 7), mix=True,
             pre=[f"\\pi {r_()}({l_()}+{r_()})", f"\\dfrac{{22}}{{7}}\\times {r_('12')}\\times ({l_('21')}+{r_('12')})\\ \\text{{m}}^2"])
s += w
s += ans("शंकु का कुल पृष्ठीय क्षेत्रफल " + m("= 1244\\tfrac{4}{7}\\ \\text{m}^2") + " है।")
ANS["11.1 Q2"] = "8712/7 = 1244 4/7 m²"
E1.append(("एक शंकु का कुल पृष्ठीय क्षेत्रफल ज्ञात कीजिए, जिसकी तिर्यक ऊँचाई 21 m है और आधार का व्यास 24 m है।", s))

# ---- Q3 ----
s = given("वक्र पृष्ठीय क्षेत्रफल " + m("= 308\\ \\text{cm}^2") + "<br>तिर्यक ऊँचाई " + m(f"{l_()} = 14\\ \\text{{cm}}"),
          "(i) आधार की त्रिज्या " + m(r_()) + "<br>(ii) शंकु का कुल पृष्ठीय क्षेत्रफल")
s += NOFIG + solo(cone_fig(7, math.sqrt(14 ** 2 - 7 ** 2), "हल की आकृति: शंकु (पैमाने पर); त्रिज्या r लाल, तिर्यक ऊँचाई l हरी",
                           {"r": "r = ?", "l": "l = 14 cm"}))
b = f_csa()
b += eqsu("cm^2", (PIR_L, "308"), (f"\\dfrac{{22}}{{7}}\\times {r_()}\\times {l_('14')}", "308"), (f"22\\times {r_()}\\times 2", "308"),
         (f"44{r_()}", "308"), (r_(), "\\dfrac{308}{44}"), (r_(), r_("7") + "\\ \\text{cm}"))
assert F(308, 44) == 7 and F(22, 7) * 7 * 14 == 308
s += part("(i) आधार की त्रिज्या", b)
b = f_tsa()
w1, v1 = chain(f"\\pi {r_()}^2", [PI, (r_("7"), 7), (r_("7"), 7)], "cm", 2, 154)
b += p("पहले आधार का क्षेत्रफल " + m(f"\\pi {r_()}^2") + " ज्ञात करते हैं:") + w1
b += lines(T_TSA, f"\\pi {r_()} {l_()} + \\pi {r_()}^2", "308 + 154\\ \\text{cm}^2", "462\\ \\text{cm}^2")
assert 308 + 154 == 462
s += part("(ii) कुल पृष्ठीय क्षेत्रफल", b)
s += ans("(i) आधार की त्रिज्या " + m("= 7\\ \\text{cm}") + " (ii) कुल पृष्ठीय क्षेत्रफल " + m("= 462\\ \\text{cm}^2"))
ANS["11.1 Q3"] = "r = 7 cm; TSA 462 cm²"
E1.append(("एक शंकु का वक्र पृष्ठीय क्षेत्रफल 308 " + cm2 + " है और इसकी तिर्यक ऊँचाई 14 cm है। ज्ञात कीजिए : (i) आधार की त्रिज्या (ii) शंकु का कुल पृष्ठीय क्षेत्रफल", s))

# ---- Q4 ----
s = given("तंबू (शंकु) की ऊँचाई " + m(f"{h_()} = 10\\ \\text{{m}}") + "<br>आधार की त्रिज्या " + m(f"{r_()} = 24\\ \\text{{m}}") +
          "<br>1 " + m2 + " केनवास की लागत = ₹70",
          "(i) तंबू की तिर्यक ऊँचाई " + m(l_()) + "<br>(ii) तंबू में लगे केनवास की लागत")
s += NOFIG + solo(cone_fig(24, 10, "हल की आकृति: तंबू (पैमाने पर); r लाल, h नीली, l हरी",
                           {"r": "r = 24 m", "h": "h = 10 m", "l": "l = ?"}, W=320, H=170, unit="m"))
rows, lv = pyth("l", 10, "10", BLU, 24, "24", RED, "m")
assert lv == 26
s += part("(i) तिर्यक ऊँचाई", f_l() + lad_for(676) + lines(l_(), f"\\sqrt{{{h_()}^2+{r_()}^2}}", *rows))
b = p("तंबू में लगा केनवास = तंबू का वक्र पृष्ठीय क्षेत्रफल") + f_csa()
w, v = pi_r_l(24, "24", 26, "26", "m", F(13728, 7))
b += w
b += kh("केनवास की लागत")
b += lines("\\text{लागत}", "\\text{क्षेत्रफल}\\times \\text{दर}", "\\dfrac{13728}{7}\\times 70\\text{ रुपये}", "13728\\times 10\\text{ रुपये}",
           "137280\\text{ रुपये}")
assert F(13728, 7) * 70 == 137280
s += part("(ii) केनवास की लागत", b)
s += ans("(i) तंबू की तिर्यक ऊँचाई " + m("= 26\\ \\text{m}") + " (ii) केनवास की लागत <b>₹1,37,280</b>")
ANS["11.1 Q4"] = "l = 26 m; CSA 13728/7 m²; cost ₹137280"
E1.append(("शंकु के आकार का एक तंबू 10 m ऊँचा है और उसके आधार की त्रिज्या 24 m है। ज्ञात कीजिए : (i) तंबू की तिर्यक ऊँचाई (ii) तंबू में लगे केनवास (canvas) की लागत, यदि 1 " + m2 + " केनवास की लागत 70 रुपए है।", s))

# ---- Q5 ----
s = given("तंबू (शंकु) की ऊँचाई " + m(f"{h_()} = 8\\ \\text{{m}}") + ", आधार की त्रिज्या " + m(f"{r_()} = 6\\ \\text{{m}}") +
          "<br>तिरपाल की चौड़ाई = 3 m<br>सिलाई और कटाई के लिए अतिरिक्त तिरपाल = 20 cm<br>" + m("\\pi = 3.14"),
          "तिरपाल की कुल लंबाई")
s += NOFIG + solo(cone_fig(6, 8, "हल की आकृति: तंबू (पैमाने पर); r लाल, h नीली, l हरी",
                           {"r": "r = 6 m", "h": "h = 8 m", "l": "l = ?"}, unit="m"))
rows, lv = pyth("l", 8, "8", BLU, 6, "6", RED, "m")
assert lv == 10
s += kh("तिर्यक ऊँचाई " + m(l_()) + " ज्ञात करना") + f_l() + lad_for(100) + lines(l_(), f"\\sqrt{{{h_()}^2+{r_()}^2}}", *rows)
s += kh("तंबू का वक्र पृष्ठीय क्षेत्रफल (" + m("\\pi = 3.14") + ")") + f_csa()
w, v = pi_r_l(6, "6", 10, "10", "m", F(1884, 10), pi=PI314)
s += w
s += kh("तिरपाल की लंबाई")
s += p("तिरपाल का क्षेत्रफल = तंबू का वक्र पृष्ठीय क्षेत्रफल, और तिरपाल आयताकार है:")
s += formula("आयत का क्षेत्रफल", "क्षेत्रफल = लंबाई × चौड़ाई")
s += eqs(("\\text{लंबाई}\\times 3\\ \\text{m}", "188.4\\ \\text{m}^2"), ("\\text{लंबाई}", "\\dfrac{188.4}{3}\\ \\text{m}"), ("\\text{लंबाई}", "62.8\\ \\text{m}"))
assert F(1884, 10) / 3 == F(628, 10)
s += p("अतिरिक्त तिरपाल = 20 cm = " + m("\\dfrac{20}{100}") + " m = 0.2 m")
s += lines("\\text{कुल लंबाई}", "62.8 + 0.2\\ \\text{m}", "63\\ \\text{m}")
s += ans("3 m चौड़े तिरपाल की <b>63 m</b> लंबाई लगेगी।")
ANS["11.1 Q5"] = "l=10 m, CSA 188.4 m², length 62.8 + 0.2 = 63 m"
E1.append(("8 m ऊँचाई और आधार की त्रिज्या 6 m वाले एक शंकु के आकार का तंबू बनाने में 3 m चौड़े तिरपाल की कितनी लंबाई लगेगी? यह मान कर चलिए कि इसकी सिलाई और कटाई में 20 cm तिरपाल अतिरिक्त लगेगा। (" + m("\\pi = 3.14") + " का प्रयोग कीजिए।)", s))

# ---- Q6 ----
s = given("गुंबज (शंकु) की तिर्यक ऊँचाई " + m(f"{l_()} = 25\\ \\text{{m}}") + "<br>आधार का व्यास " + m(f"{d_()} = 14\\ \\text{{m}}") +
          "<br>सफेदी की दर = ₹210 प्रति 100 " + m2, "वक्र पृष्ठ पर सफेदी कराने का व्यय")
s += NOFIG + solo(cone_fig(7, 24, "हल की आकृति: गुंबज (पैमाने पर); व्यास d नारंगी, तिर्यक ऊँचाई l हरी",
                           {"d": "d = 14 m", "l": "l = 25 m"}, unit="m"))
s += kh("आधार की त्रिज्या " + m(r_()) + " ज्ञात करना") + r_from_d(14, "m")
s += f_csa()
w, v = pi_r_l(7, "7", 25, "25", "m", 550)
s += w
s += kh("सफेदी का व्यय")
s += lines("100\\ \\mathrm{m}^2\\text{ का व्यय}", "210\\text{ रुपये}")
s += lines("1\\ \\mathrm{m}^2\\text{ का व्यय}", "\\dfrac{210}{100}\\text{ रुपये}")
s += lines("550\\ \\mathrm{m}^2\\text{ का व्यय}", "\\dfrac{210}{100}\\times 550\\text{ रुपये}", "\\dfrac{210\\times 550}{100}\\text{ रुपये}",
           "21\\times 55\\text{ रुपये}", "1155\\text{ रुपये}")
assert F(210, 100) * 550 == 1155
s += ans("वक्र पृष्ठ पर सफेदी कराने का व्यय <b>₹1155</b> है।")
ANS["11.1 Q6"] = "CSA 550 m², ₹1155"
E1.append(("शंकु के आधार की एक गुंबज की तिर्यक ऊँचाई और आधार व्यास क्रमश: 25 m और 14 m हैं। इसकी वक्र पृष्ठ पर ₹ 210 प्रति 100 " + m2 + " की दर से सफेदी कराने का व्यय ज्ञात कीजिए।", s))

# ---- Q7 ----
s = given("टोपी (शंकु) के आधार की त्रिज्या " + m(f"{r_()} = 7\\ \\text{{cm}}") + "<br>ऊँचाई " + m(f"{h_()} = 24\\ \\text{{cm}}") +
          "<br>टोपियों की संख्या = 10", "10 टोपियों के लिए आवश्यक गत्ते का क्षेत्रफल")
s += NOFIG + solo(cone_fig(7, 24, "हल की आकृति: टोपी (पैमाने पर); r लाल, h नीली, l हरी",
                           {"r": "r = 7 cm", "h": "h = 24 cm", "l": "l = ?"}, H=250))
rows, lv = pyth("l", 24, "24", BLU, 7, "7", RED, "cm")
assert lv == 25
s += kh("तिर्यक ऊँचाई " + m(l_()) + " ज्ञात करना") + f_l() + lad_for(625) + lines(l_(), f"\\sqrt{{{h_()}^2+{r_()}^2}}", *rows)
s += kh("एक टोपी के लिए गत्ता = टोपी का वक्र पृष्ठीय क्षेत्रफल") + f_csa()
w, v = pi_r_l(7, "7", 25, "25", "cm", 550)
s += w
s += lines("\\text{10 टोपियों के लिए गत्ता}", "10\\times 550\\ \\text{cm}^2", "5500\\ \\text{cm}^2")
s += ans("10 टोपियाँ बनाने के लिए " + m("5500\\ \\text{cm}^2") + " गत्ते की आवश्यकता होगी।")
ANS["11.1 Q7"] = "l = 25 cm, 550 cm² each, 5500 cm²"
E1.append(("एक जोकर की टोपी एक शंकु के आकार की है, जिसके आधार की त्रिज्या 7 cm और ऊँचाई 24 cm है। इसी प्रकार की 10 टोपियाँ बनाने के लिए आवश्यक गत्ते का क्षेत्रफल ज्ञात कीजिए।", s))

# ---- Q8 ----
s = given("शंकुओं की संख्या = 50<br>प्रत्येक शंकु के आधार का व्यास " + m(f"{d_()} = 40\\ \\text{{cm}}") + ", ऊँचाई " + m(f"{h_()} = 1\\ \\text{{m}}") +
          "<br>पेंट की दर = ₹12 प्रति " + m2 + "<br>" + m("\\pi = 3.14,\\ \\sqrt{1.04} = 1.02"),
          "सभी शंकुओं के बाहरी पृष्ठों को पेंट कराने की लागत")
s += NOFIG + solo(cone_fig(F(1, 5), 1, "हल की आकृति: एक शंकु (पैमाने पर); d नारंगी, h नीली, l हरी",
                           {"d": "d = 40 cm", "h": "h = 1 m", "l": "l = ?"}, W=300, H=260, unit="m"))
s += kh("त्रिज्या " + m(r_()) + " (मीटर में)")
s += lines(r_(), f"\\dfrac{{{d_()}}}{{2}}", f"\\dfrac{{{d_('40')}}}{{2}}\\ \\text{{cm}}", r_("20") + "\\ \\text{cm}",
           "\\dfrac{20}{100}\\ \\text{m}", r_("0.2") + "\\ \\text{m}")
s += kh("तिर्यक ऊँचाई " + m(l_())) + f_l()
s += lines(l_(), f"\\sqrt{{{h_()}^2+{r_()}^2}}", f"\\sqrt{{{h_('1')}^2+{r_('0.2')}^2}}\\ \\text{{m}}", "\\sqrt{1+0.04}\\ \\text{m}",
           "\\sqrt{1.04}\\ \\text{m}", l_("1.02") + "\\ \\text{m}")
s += p("(प्रश्न में दिया है: " + m("\\sqrt{1.04} = 1.02") + ")")
s += kh("एक शंकु का बाहरी (वक्र) पृष्ठ (" + m("\\pi = 3.14") + ")") + f_csa()
w, v = pi_r_l(F(1, 5), "0.2", F(102, 100), "1.02", "m", F(64056, 100000), pi=PI314)
s += w
s += lines("\\text{50 शंकुओं का पृष्ठ}", "50\\times 0.64056\\ \\text{m}^2", "32.028\\ \\text{m}^2")
assert 50 * F(64056, 100000) == F(32028, 1000)
s += kh("पेंट कराने की लागत")
s += lines("\\text{लागत}", "32.028\\times 12\\text{ रुपये}", "384.336\\text{ रुपये}", "384.34\\text{ रुपये (पैसे तक)}")
assert F(32028, 1000) * 12 == F(384336, 1000)
s += ans("सभी 50 शंकुओं को पेंट कराने की लागत <b>₹384.34</b> (₹384.336, पैसे तक) होगी।")
ANS["11.1 Q8"] = "CSA 0.64056 m², 50 → 32.028 m², ₹384.336 ≈ ₹384.34"
E1.append(("किसी बस स्टाप को पुराने गत्ते से बने 50 खोखले शंकुओं द्वारा सड़क से अलग किया हुआ है। प्रत्येक शंकु के आधार का व्यास 40 cm है और ऊँचाई 1 m है। यदि इन शंकुओं की बाहरी पृष्ठों को पेंट करवाना है और पेंट की दर ₹ 12 प्रति " + m2 + " है, तो इनको पेंट कराने में कितनी लागत आएगी? (" + m("\\pi = 3.14") + " और " + m("\\sqrt{1.04} = 1.02") + " का प्रयोग कीजिए।)", s))
assert len(E1) == 8

# ======================= प्रश्नावली 11.2 (गोले का पृष्ठीय क्षेत्रफल) =======================
E2 = []

# ---- Q1 ----
s = given("गोले की त्रिज्या " + m(r_()) + ": (i) 10.5 cm (ii) 5.6 cm (iii) 14 cm", "प्रत्येक गोले का पृष्ठीय क्षेत्रफल")
s += NOFIG + solo(sphere_fig(80, "हल की आकृति: गोला, केंद्र O; त्रिज्या r लाल", "r", W=240, H=200))
s += f_sph()
for lab, rv, rt, want in (("(i)", F(21, 2), "10.5", F(1386)), ("(ii)", F(28, 5), "5.6", F(39424, 100)), ("(iii)", 14, "14", 2464)):
    w, v = sph_sa(rv, rt, "cm", want)
    s += part(f"{lab} " + m(f"{r_()} = {rt}\\ \\text{{cm}}"), w)
s += ans("(i) " + m("1386\\ \\text{cm}^2") + " (ii) " + m("394.24\\ \\text{cm}^2") + " (iii) " + m("2464\\ \\text{cm}^2"))
ANS["11.2 Q1"] = "1386, 394.24, 2464 cm²"
E2.append(("निम्न त्रिज्या वाले गोले का पृष्ठीय क्षेत्रफल ज्ञात कीजिए : (i) 10.5 cm (ii) 5.6 cm (iii) 14 cm", s))

# ---- Q2 ----
s = given("गोले का व्यास " + m(d_()) + ": (i) 14 cm (ii) 21 cm (iii) 3.5 m", "प्रत्येक गोले का पृष्ठीय क्षेत्रफल")
s += NOFIG + solo(sphere_fig(80, "हल की आकृति: गोला, केंद्र O; व्यास d नारंगी", None, "d", W=240, H=200))
s += f_sph()
for lab, dv, dt, unit, want in (("(i)", 14, "14", "cm", 616), ("(ii)", 21, "21", "cm", 1386), ("(iii)", F(7, 2), "3.5", "m", F(385, 10))):
    rv = F(dv) / 2
    w, v = sph_sa(rv, dec(rv), unit, want)
    s += part(f"{lab} " + m(f"{d_()} = {dt}\\ \\text{{{unit}}}"), r_from_d(dv, unit) + w)
s += ans("(i) " + m("616\\ \\text{cm}^2") + " (ii) " + m("1386\\ \\text{cm}^2") + " (iii) " + m("38.5\\ \\text{m}^2"))
ANS["11.2 Q2"] = "616 cm², 1386 cm², 38.5 m²"
E2.append(("निम्न व्यास वाले गोले का पृष्ठीय क्षेत्रफल ज्ञात कीजिए : (i) 14 cm (ii) 21 cm (iii) 3.5 m", s))

# ---- Q3 ----
s = given("अर्धगोले की त्रिज्या " + m(f"{r_()} = 10\\ \\text{{cm}}") + ", " + m("\\pi = 3.14"), "अर्धगोले का कुल पृष्ठीय क्षेत्रफल")
s += NOFIG + solo(hemi_fig(10, "हल की आकृति: ठोस अर्धगोला; वक्र पृष्ठ + वृत्ताकार आधार; त्रिज्या r लाल", "r = 10 cm", dome=True, solid=True))
s += p("ठोस अर्धगोले के कुल पृष्ठ में उसका वक्र पृष्ठ " + m(f"2\\pi {r_()}^2") + " और वृत्ताकार आधार " + m(f"\\pi {r_()}^2") + " दोनों आते हैं।")
s += f_htsa()
w, v = chain(T_TSA, [("3", 3), PI314, (r_("10"), 10), (r_("10"), 10)], "cm", 2, 942, pre=[f"3\\pi {r_()}^2"], conv=False)
s += w
s += ans("अर्धगोले का कुल पृष्ठीय क्षेत्रफल " + m("= 942\\ \\text{cm}^2") + " है।")
ANS["11.2 Q3"] = "942 cm²"
E2.append(("10 cm त्रिज्या वाले एक अर्धगोले का कुल पृष्ठीय क्षेत्रफल ज्ञात कीजिए। (" + m("\\pi = 3.14") + " लीजिए।)", s))

# ---- Q4 ----
s = given("गुब्बारे की त्रिज्या: पहले " + m(f"{r_('r_1')} = 7\\ \\text{{cm}}") + ", हवा भरने के बाद " + m(f"{C(BLU, 'r_2')} = 14\\ \\text{{cm}}"),
          "दोनों स्थितियों में पृष्ठीय क्षेत्रफलों का अनुपात")
s += NOFIG + solo(two_spheres("हल की आकृति: गुब्बारा पहले (लाल त्रिज्या) और बाद में (नीली त्रिज्या); त्रिज्याएँ 7 : 14 (पैमाने पर)", 2,
                              ("r₂ = 14 cm", "r₁ = 7 cm"), ("बाद में", "पहले")))
s += f_sph()
s += p("माना पहली स्थिति में पृष्ठीय क्षेत्रफल " + m("S_1") + " और दूसरी स्थिति में " + m("S_2") + " है।")
s += lines("\\dfrac{S_1}{S_2}", f"\\dfrac{{4\\pi {r_('r_1')}^2}}{{4\\pi {C(BLU, 'r_2')}^2}}",
           f"\\dfrac{{4\\pi\\times {r_('7')}\\times {r_('7')}}}{{4\\pi\\times {C(BLU, '14')}\\times {C(BLU, '14')}}}",
           "\\dfrac{7\\times 7}{14\\times 14}", "\\dfrac{7\\times 7}{(2\\times 7)\\times (2\\times 7)}", "\\dfrac{1}{2\\times 2}", "\\dfrac{1}{4}")
assert F(49, 196) == F(1, 4)
s += ans("पृष्ठीय क्षेत्रफलों का अनुपात <b>1 : 4</b> है।")
ANS["11.2 Q4"] = "1 : 4"
E2.append(("एक गोलाकार गुब्बारे में हवा भरने पर, उसकी त्रिज्या 7 cm से 14 cm हो जाती है। इन दोनों स्थितियों में, गुब्बारे के पृष्ठीय क्षेत्रफलों का अनुपात ज्ञात कीजिए।", s))

# ---- Q5 ----
s = given("अर्धगोलाकार कटोरे का आंतरिक व्यास " + m(f"{d_()} = 10.5\\ \\text{{cm}}") + "<br>कलई की दर = ₹16 प्रति 100 " + cm2,
          "आंतरिक पृष्ठ पर कलई कराने का व्यय")
s += NOFIG + solo(hemi_fig(F(21, 4), "हल की आकृति: अर्धगोलाकार कटोरा; आंतरिक व्यास d नारंगी", None, "d = 10.5 cm"))
s += kh("आंतरिक त्रिज्या " + m(r_())) + r_from_d(F(21, 2), "cm")
s += f_hcsa()
w, v = chain(T_CSA, [("2", 2), PI, (r_("5.25"), F(21, 4)), (r_("5.25"), F(21, 4))], "cm", 2, F(17325, 100), pre=[f"2\\pi {r_()}^2"])
s += w
s += kh("कलई का व्यय")
s += lines("100\\ \\mathrm{cm}^2\\text{ का व्यय}", "16\\text{ रुपये}")
s += lines("173.25\\ \\mathrm{cm}^2\\text{ का व्यय}", "\\dfrac{16}{100}\\times 173.25\\text{ रुपये}", "0.16\\times 173.25\\text{ रुपये}",
           "27.72\\text{ रुपये}")
assert F(16, 100) * F(17325, 100) == F(2772, 100)
s += ans("आंतरिक पृष्ठ पर कलई कराने का व्यय <b>₹27.72</b> है।")
ANS["11.2 Q5"] = "173.25 cm², ₹27.72"
E2.append(("पीतल से बने एक अर्धगोलाकार कटोरे का आंतरिक व्यास 10.5 cm है। ₹16 प्रति 100 " + cm2 + " की दर से इसके आंतरिक पृष्ठ पर कलई कराने का व्यय ज्ञात कीजिए।", s))


def r_from_sa154():
    """4πr² = 154 -> r = 3.5 cm (used in 11.2 Q6 and 11.4 Q7)."""
    o = f_sph()
    o += eqsu("cm^2", (f"4\\pi {r_()}^2", "154"), (f"4\\times \\dfrac{{22}}{{7}}\\times {r_()}^2", "154"), (f"\\dfrac{{88}}{{7}}{r_()}^2", "154"),
             (f"{r_()}^2", "\\dfrac{154\\times 7}{88}"), (f"{r_()}^2", "\\dfrac{1078}{88}"), (f"{r_()}^2", "12.25"))
    assert F(154 * 7, 88) == F(1225, 100)
    o += lad_for(F(1225, 100))
    o += lines(r_(), "\\sqrt{12.25}\\ \\text{cm}", *sq_rows(F(1225, 100), "cm")[:-1], r_("3.5") + "\\ \\text{cm}")
    return o


# ---- Q6 ----
s = given("गोले का पृष्ठीय क्षेत्रफल " + m("= 154\\ \\text{cm}^2"), "गोले की त्रिज्या " + m(r_()))
s += NOFIG + solo(sphere_fig(70, "हल की आकृति: गोला, केंद्र O; त्रिज्या r लाल", "r = ?", W=220, H=180))
s += r_from_sa154()
s += ans("गोले की त्रिज्या " + m("= 3.5\\ \\text{cm}") + " है।")
ANS["11.2 Q6"] = "3.5 cm"
E2.append(("उस गोले की त्रिज्या ज्ञात कीजिए जिसका पृष्ठीय क्षेत्रफल 154 " + cm2 + " है।", s))

# ---- Q7 ----
s = given("चंद्रमा का व्यास = पृथ्वी के व्यास का " + m("\\dfrac{1}{4}") + " (लगभग)", "चंद्रमा और पृथ्वी के पृष्ठीय क्षेत्रफलों का अनुपात")
s += NOFIG + solo(two_spheres("हल की आकृति: पृथ्वी (त्रिज्या R नीली) और चंद्रमा (त्रिज्या r लाल); r = R/4 (पैमाने पर)", 4,
                              ("R", "r"), ("पृथ्वी", "चंद्रमा")))
s += p("माना पृथ्वी का व्यास " + m(C(BLU, "2R")) + " है, तो उसकी त्रिज्या " + m(C(BLU, "R")) + " होगी।")
s += lines("\\text{चंद्रमा का व्यास}", f"\\dfrac{{1}}{{4}}\\times {C(BLU, '2R')}", "\\dfrac{R}{2}")
s += lines(f"\\text{{चंद्रमा की त्रिज्या }}{r_()}", "\\dfrac{1}{2}\\times \\dfrac{R}{2}", r_("\\dfrac{R}{4}"))
s += f_sph()
s += p("माना चंद्रमा का पृष्ठीय क्षेत्रफल " + m("S_1") + " और पृथ्वी का " + m("S_2") + " है।")
s += lines("\\dfrac{S_1}{S_2}", f"\\dfrac{{4\\pi {r_()}^2}}{{4\\pi {C(BLU, 'R')}^2}}",
           f"\\dfrac{{{r_()}^2}}{{{C(BLU, 'R')}^2}}", f"\\dfrac{{\\left({r_('\\dfrac{R}{4}')}\\right)^2}}{{R^2}}", "\\dfrac{R^2}{16}\\times \\dfrac{1}{R^2}",
           "\\dfrac{1}{16}")
s += ans("चंद्रमा और पृथ्वी के पृष्ठीय क्षेत्रफलों का अनुपात <b>1 : 16</b> है।")
ANS["11.2 Q7"] = "1 : 16"
E2.append(("चन्द्रमा का व्यास पृथ्वी के व्यास का लगभग एक-चौथाई है। इन दोनों के पृष्ठीय क्षेत्रफलों का अनुपात ज्ञात कीजिए।", s))

# ---- Q8 ----
s = given("कटोरे की आंतरिक त्रिज्या " + m(f"{r_()} = 5\\ \\text{{cm}}") + "<br>स्टील की मोटाई = 0.25 cm", "कटोरे का बाहरी वक्र पृष्ठीय क्षेत्रफल")
s += NOFIG + solo(hemi_fig(5, "हल की आकृति: अर्धगोलाकार कटोरा (पैमाने पर); आंतरिक त्रिज्या r लाल, बाहरी त्रिज्या R बैंगनी", "r = 5 cm",
                           R=F(21, 4), Rlab="R = ?"))
s += kh("बाहरी त्रिज्या " + m(R_()))
s += lines(R_(), f"{r_()} + \\text{{मोटाई}}", f"{r_('5')} + 0.25\\ \\text{{cm}}", R_("5.25") + "\\ \\text{cm}")
s += f_hcsa(PUR, "R")
w, v = chain(T_CSA, [("2", 2), PI, (R_("5.25"), F(21, 4)), (R_("5.25"), F(21, 4))], "cm", 2, F(17325, 100), pre=[f"2\\pi {R_()}^2"])
s += w
s += ans("कटोरे का बाहरी वक्र पृष्ठीय क्षेत्रफल " + m("= 173.25\\ \\text{cm}^2") + " है।")
ANS["11.2 Q8"] = "R = 5.25 cm, 173.25 cm²"
E2.append(("एक अर्धगोलाकार कटोरा 0.25 cm मोटी स्टील से बना है। इस कटोरे की आंतरिक त्रिज्या 5 cm है। कटोरे का बाहरी वक्र पृष्ठीय क्षेत्रफल ज्ञात कीजिए।", s))

# ---- Q9 ----
s = given("गोले की त्रिज्या " + m(r_()) + "; लंब वृत्तीय बेलन गोले को पूर्णतया घेरे हुए है",
          "(i) गोले का पृष्ठीय क्षेत्रफल<br>(ii) बेलन का वक्र पृष्ठीय क्षेत्रफल<br>(iii) दोनों क्षेत्रफलों का अनुपात")
s += pair(cyl_sphere_fig("आकृति 11.10"),
          cyl_sphere_fig("हल की आकृति: बेलन की त्रिज्या = r (लाल), ऊँचाई = व्यास = 2r (नीली)", sol=True))
s += part("(i) गोले का पृष्ठीय क्षेत्रफल", f_sph() + lines(T_SA, f"4\\pi {r_()}^2"))
b = p("बेलन गोले को पूर्णतया घेरे हुए है, इसलिए:")
b += lines("\\text{बेलन की त्रिज्या}", "\\text{गोले की त्रिज्या}", r_())
b += lines(f"\\text{{बेलन की ऊँचाई }}{h_()}", "\\text{गोले का व्यास}", h_("2r"))
b += formula("बेलन का वक्र पृष्ठीय क्षेत्रफल", "वक्र पृष्ठीय क्षेत्रफल " + m(f"= 2\\pi {r_()} {h_()}"))
b += lines(T_CSA, f"2\\pi {r_()} {h_()}", f"2\\pi\\times {r_()}\\times {h_('2r')}", f"4\\pi {r_()}^2")
s += part("(ii) बेलन का वक्र पृष्ठीय क्षेत्रफल", b)
s += part("(iii) अनुपात", p("माना (i) का क्षेत्रफल " + m("S_1") + " और (ii) का " + m("S_2") + " है।") + lines("\\dfrac{S_1}{S_2}", f"\\dfrac{{4\\pi {r_()}^2}}{{4\\pi {r_()}^2}}", "\\dfrac{1}{1}"))
s += ans("(i) " + m(f"4\\pi r^2") + " (ii) " + m("4\\pi r^2") + " (iii) अनुपात <b>1 : 1</b>")
ANS["11.2 Q9"] = "4πr², 4πr², 1:1"
E2.append(("एक लंब वृत्तीय बेलन त्रिज्या " + m("r") + " वाले एक गोले को पूर्णतया घेरे हुए है (देखिए आकृति 11.10)। ज्ञात कीजिए: (i) गोले का पृष्ठीय क्षेत्रफल (ii) बेलन का वक्र पृष्ठीय क्षेत्रफल (iii) ऊपर (i) और (ii) में प्राप्त क्षेत्रफलों का अनुपात", s))
assert len(E2) == 9

# ======================= प्रश्नावली 11.3 (शंकु का आयतन) =======================
E3 = []

# ---- Q1 ----
s = given("(i) " + m(f"{r_()} = 6\\ \\text{{cm}},\\ {h_()} = 7\\ \\text{{cm}}") + "<br>(ii) " + m(f"{r_()} = 3.5\\ \\text{{cm}},\\ {h_()} = 12\\ \\text{{cm}}"),
          "प्रत्येक लंब वृत्तीय शंकु का आयतन")
s += NOFIG + pair(cone_fig(6, 7, "हल की आकृति (i): r = 6 cm, h = 7 cm (पैमाने पर)", {"r": "r = 6 cm", "h": "h = 7 cm"}, W=260, H=210),
                  cone_fig(F(7, 2), 12, "हल की आकृति (ii): r = 3.5 cm, h = 12 cm (पैमाने पर)", {"r": "r = 3.5 cm", "h": "h = 12 cm"}, W=260, H=210))
s += f_vcone()
w, v = cone_v(6, "6", 7, "7", "cm", 264)
s += part("(i) " + m(f"{r_()} = 6\\ \\text{{cm}},\\ {h_()} = 7\\ \\text{{cm}}"), w)
w, v = cone_v(F(7, 2), "3.5", 12, "12", "cm", 154)
s += part("(ii) " + m(f"{r_()} = 3.5\\ \\text{{cm}},\\ {h_()} = 12\\ \\text{{cm}}"), w)
s += ans("(i) आयतन " + m("= 264\\ \\text{cm}^3") + " (ii) आयतन " + m("= 154\\ \\text{cm}^3"))
ANS["11.3 Q1"] = "264 cm³, 154 cm³"
E3.append(("उस लंब वृत्तीय शंकु का आयतन ज्ञात कीजिए, जिसकी (i) त्रिज्या 6 cm और ऊँचाई 7 cm है। (ii) त्रिज्या 3.5 cm और ऊँचाई 12 cm है।", s))

# ---- Q2 ----
s = given("(i) " + m(f"{r_()} = 7\\ \\text{{cm}},\\ {l_()} = 25\\ \\text{{cm}}") + "<br>(ii) " + m(f"{h_()} = 12\\ \\text{{cm}},\\ {l_()} = 13\\ \\text{{cm}}"),
          "प्रत्येक शंकु के आकार के बर्तन की धारिता (लीटरों में)")
s += NOFIG + pair(cone_fig(7, 24, "हल की आकृति (i): r = 7 cm, l = 25 cm (पैमाने पर)", {"r": "r = 7 cm", "l": "l = 25 cm", "h": "h = ?"}, W=260, H=230),
                  cone_fig(5, 12, "हल की आकृति (ii): h = 12 cm, l = 13 cm (पैमाने पर)", {"r": "r = ?", "l": "l = 13 cm", "h": "h = 12 cm"}, W=260, H=230))
s += tp("धारिता = बर्तन का आयतन; " + m("1000\\ \\text{cm}^3 = 1") + " लीटर")
b = kh("ऊँचाई " + m(h_()) + " ज्ञात करना") + p("क्योंकि " + m(f"{l_()}^2 = {h_()}^2 + {r_()}^2") + ", इसलिए " + m(f"{h_()}^2 = {l_()}^2 - {r_()}^2"))
rows, hv = pyth("h", 25, "25", GRN, 7, "7", RED, "cm", "-")
assert hv == 24
b += lad_for(576) + lines(h_(), f"\\sqrt{{{l_()}^2-{r_()}^2}}", *rows)
b += f_vcone()
w, v = cone_v(7, "7", 24, "24", "cm", 1232)
b += w
b += lines("\\text{धारिता}", "\\dfrac{1232}{1000}\\text{ लीटर}", "1.232\\text{ लीटर}")
s += part("(i) " + m(f"{r_()} = 7\\ \\text{{cm}},\\ {l_()} = 25\\ \\text{{cm}}"), b)
b = kh("त्रिज्या " + m(r_()) + " ज्ञात करना") + p("क्योंकि " + m(f"{l_()}^2 = {h_()}^2 + {r_()}^2") + ", इसलिए " + m(f"{r_()}^2 = {l_()}^2 - {h_()}^2"))
rows, rv = pyth("r", 13, "13", GRN, 12, "12", BLU, "cm", "-")
assert rv == 5
b += lines(r_(), f"\\sqrt{{{l_()}^2-{h_()}^2}}", *rows)
b += f_vcone()
w, v = cone_v(5, "5", 12, "12", "cm", F(2200, 7))
b += w
b += lines("\\text{धारिता}", "\\dfrac{2200}{7}\\div 1000\\text{ लीटर}", "\\dfrac{2200}{7\\times 1000}\\text{ लीटर}", "\\dfrac{22}{70}\\text{ लीटर}",
           "\\dfrac{11}{35}\\text{ लीटर}")
assert F(2200, 7000) == F(11, 35)
s += part("(ii) " + m(f"{h_()} = 12\\ \\text{{cm}},\\ {l_()} = 13\\ \\text{{cm}}"), b)
s += ans("(i) धारिता = 1.232 लीटर (ii) धारिता = " + m("\\dfrac{11}{35}") + " लीटर")
ANS["11.3 Q2"] = "h=24, 1232 cm³ = 1.232 L; r=5, 2200/7 cm³ = 11/35 L"
E3.append(("शंकु के आकार के उस बर्तन की लीटरों में धारिता ज्ञात कीजिए जिसकी (i) त्रिज्या 7 cm और तिर्यक ऊँचाई 25 cm है। (ii) ऊँचाई 12 cm और तिर्यक ऊँचाई 13 cm है।", s))

# ---- Q3 ----
s = given("शंकु की ऊँचाई " + m(f"{h_()} = 15\\ \\text{{cm}}") + "<br>आयतन " + m("= 1570\\ \\text{cm}^3") + ", " + m("\\pi = 3.14"),
          "आधार की त्रिज्या " + m(r_()))
s += NOFIG + solo(cone_fig(10, 15, "हल की आकृति: शंकु (पैमाने पर); h नीली, r लाल", {"r": "r = ?", "h": "h = 15 cm"}, W=280, H=220))
s += f_vcone()
s += eqsu("cm^3", (f"\\dfrac{{1}}{{3}}\\pi {r_()}^2 {h_()}", "1570"), (f"\\dfrac{{1}}{{3}}\\times 3.14\\times {r_()}^2\\times {h_('15')}", "1570"),
         (f"3.14\\times {r_()}^2\\times 5", "1570"), (f"15.7{r_()}^2", "1570"), (f"{r_()}^2", "\\dfrac{1570}{15.7}"),
         (f"{r_()}^2", "\\dfrac{15700}{157}"), (f"{r_()}^2", "100"))
assert F(314, 100) * 5 == F(157, 10) and F(1570) / F(157, 10) == 100
s += lad_for(100) + lines(r_(), "\\sqrt{100}\\ \\text{cm}", *sq_rows(100, "cm")[:-1], r_("10") + "\\ \\text{cm}")
s += ans("आधार की त्रिज्या " + m("= 10\\ \\text{cm}") + " है।")
ANS["11.3 Q3"] = "10 cm"
E3.append(("एक शंकु की ऊँचाई 15 cm है। यदि इसका आयतन 1570 " + cm3 + " है, तो इसके आधार की त्रिज्या ज्ञात कीजिए। (" + m("\\pi = 3.14") + " प्रयोग कीजिए।)", s))

# ---- Q4 ----
s = given("शंकु की ऊँचाई " + m(f"{h_()} = 9\\ \\text{{cm}}") + "<br>आयतन " + m("= 48\\pi\\ \\text{cm}^3"), "आधार का व्यास " + m(d_()))
s += NOFIG + solo(cone_fig(4, 9, "हल की आकृति: शंकु (पैमाने पर); h नीली, व्यास d नारंगी", {"d": "d = ?", "h": "h = 9 cm"}, W=260, H=220))
s += f_vcone()
s += eqsu("cm^3", (f"\\dfrac{{1}}{{3}}\\pi {r_()}^2 {h_()}", "48\\pi"), (f"\\dfrac{{1}}{{3}}\\times \\pi\\times {r_()}^2\\times {h_('9')}", "48\\pi"),
         (f"3\\pi {r_()}^2", "48\\pi"), (f"{r_()}^2", "\\dfrac{48\\pi}{3\\pi}"), (f"{r_()}^2", "16"))
s += lines(r_(), "\\sqrt{16}\\ \\text{cm}", *sq_rows(16, "cm")[:-1], r_("4") + "\\ \\text{cm}")
s += lines(d_(), f"2\\times {r_()}", f"2\\times {r_('4')}\\ \\text{{cm}}", d_("8") + "\\ \\text{cm}")
s += ans("आधार का व्यास " + m("= 8\\ \\text{cm}") + " है।")
ANS["11.3 Q4"] = "r = 4, d = 8 cm"
E3.append(("यदि 9 cm ऊँचाई वाले एक लंब वृत्तीय शंकु का आयतन " + m("48\\pi\\ \\text{cm}^3") + " है, तो इसके आधार का व्यास ज्ञात कीजिए।", s))

# ---- Q5 ----
s = given("शंक्वाकार गड्ढे का ऊपरी व्यास " + m(f"{d_()} = 3.5\\ \\text{{m}}") + "<br>गहराई (ऊँचाई) " + m(f"{h_()} = 12\\ \\text{{m}}"),
          "गड्ढे की धारिता (किलोलीटर में)")
s += NOFIG + solo(cone_fig(F(7, 4), 12, "हल की आकृति: गड्ढे का आकार (शंकु, पैमाने पर; गड्ढे में शीर्ष नीचे और व्यास ऊपर होता है)",
                           {"d": "d = 3.5 m", "h": "h = 12 m"}, W=260, H=250, unit="m"))
s += kh("त्रिज्या " + m(r_())) + r_from_d(F(7, 2), "m")
s += f_vcone()
w, v = cone_v(F(7, 4), "1.75", 12, "12", "m", F(385, 10))
s += w
s += tp(m("1\\ \\text{m}^3 = 1000") + " लीटर = 1 किलोलीटर")
s += lines("\\text{धारिता}", "38.5\\text{ किलोलीटर}")
s += ans("गड्ढे की धारिता <b>38.5 किलोलीटर</b> है।")
ANS["11.3 Q5"] = "38.5 m³ = 38.5 kL"
E3.append(("ऊपरी व्यास 3.5 m वाले शंकु के आकार का एक गड्ढा 12 m गहरा है। इसकी धारिता किलोलीटरों में कितनी है?", s))

# ---- Q6 ----
s = given("शंकु का आयतन " + m("= 9856\\ \\text{cm}^3") + "<br>आधार का व्यास " + m(f"{d_()} = 28\\ \\text{{cm}}"),
          "(i) ऊँचाई " + m(h_()) + "<br>(ii) तिर्यक ऊँचाई " + m(l_()) + "<br>(iii) वक्र पृष्ठीय क्षेत्रफल")
s += NOFIG + solo(cone_fig(14, 48, "हल की आकृति: शंकु (पैमाने पर); d नारंगी, h नीली, l हरी", {"d": "d = 28 cm", "h": "h = ?", "l": "l = ?"},
                           W=260, H=260))
s += kh("त्रिज्या " + m(r_())) + r_from_d(28, "cm")
b = f_vcone()
b += eqsu("cm^3", (f"\\dfrac{{1}}{{3}}\\pi {r_()}^2 {h_()}", "9856"), (f"\\dfrac{{1}}{{3}}\\times \\dfrac{{22}}{{7}}\\times {r_('14')}\\times {r_('14')}\\times {h_()}", "9856"),
         (f"\\dfrac{{22\\times 14\\times 14}}{{3\\times 7}}{h_()}", "9856"), (f"\\dfrac{{22\\times 2\\times 14}}{{3}}{h_()}", "9856"),
         (f"\\dfrac{{616}}{{3}}{h_()}", "9856"), (h_(), "\\dfrac{9856\\times 3}{616}"), (h_(), "16\\times 3"), (h_(), h_("48") + "\\ \\text{cm}"))
assert F(9856, 616) == 16 and F(1, 3) * F(22, 7) * 196 * 48 == 9856
s += part("(i) शंकु की ऊँचाई", b)
rows, lv = pyth("l", 48, "48", BLU, 14, "14", RED, "cm")
assert lv == 50
s += part("(ii) तिर्यक ऊँचाई", f_l() + lad_for(2500) + lines(l_(), f"\\sqrt{{{h_()}^2+{r_()}^2}}", *rows))
w, v = pi_r_l(14, "14", 50, "50", "cm", 2200)
s += part("(iii) वक्र पृष्ठीय क्षेत्रफल", f_csa() + w)
s += ans("(i) ऊँचाई " + m("= 48\\ \\text{cm}") + " (ii) तिर्यक ऊँचाई " + m("= 50\\ \\text{cm}") + " (iii) वक्र पृष्ठीय क्षेत्रफल " + m("= 2200\\ \\text{cm}^2"))
ANS["11.3 Q6"] = "h 48 cm, l 50 cm, CSA 2200 cm²"
E3.append(("एक लंब वृत्तीय शंकु का आयतन 9856 " + cm3 + " है। यदि इसके आधार का व्यास 28 cm है, तो ज्ञात कीजिए : (i) शंकु की ऊँचाई (ii) शंकु की तिर्यक ऊँचाई (iii) शंकु का वक्र पृष्ठीय क्षेत्रफल", s))

# ---- Q7 ----
s = given("समकोण △ABC: AB = 12 cm, BC = 5 cm, AC = 13 cm (समकोण B पर)<br>त्रिभुज को भुजा AB = 12 cm के परित घुमाया जाता है",
          "प्राप्त ठोस (शंकु) का आयतन")
s += NOFIG + solo(cone_fig(5, 12, "हल की आकृति: △ABC को AB के परित घुमाने पर शंकु; h = AB नीली, r = BC लाल, l = AC हरी (पैमाने पर)",
                           {"r": "5 cm", "h": "12 cm", "l": "13 cm"}, W=280, H=250, tri="ABC"))
s += p("भुजा AB के परित घुमाने पर AB शंकु की ऊँचाई, BC आधार की त्रिज्या और AC तिर्यक ऊँचाई बनती है:")
s += eqs((h_(), "AB = 12\\ \\text{cm}"), (r_(), "BC = 5\\ \\text{cm}"))
s += f_vcone()
def vol_pi(rv, hv, want):
    """V = 1/3 π r² h kept in terms of π (11.3 Q7, Q8)."""
    assert F(rv * rv * hv, 3) == want
    return lines(T_V, f"\\dfrac{{1}}{{3}}\\pi {r_()}^2 {h_()}", f"\\dfrac{{1}}{{3}}\\times \\pi\\times {r_(str(rv))}\\times {r_(str(rv))}\\times {h_(str(hv))}\\ \\text{{cm}}^3",
                 f"\\dfrac{{{rv}\\times {rv}\\times {hv}}}{{3}}\\pi\\ \\text{{cm}}^3",
                 (f"{rv}\\times {rv}\\times {hv // 3}\\pi\\ \\text{{cm}}^3" if hv % 3 == 0 else f"{rv // 3}\\times {rv}\\times {hv}\\pi\\ \\text{{cm}}^3"),
                 f"{want}\\pi\\ \\text{{cm}}^3")


s += vol_pi(5, 12, 100)
s += p(m("\\pi = \\dfrac{22}{7}") + " रखने पर:")
w, v = chain(T_V, [("100", 100), PI], "cm", 3, F(2200, 7), mix=True)
s += w
s += ans("प्राप्त ठोस का आयतन " + m("= 100\\pi\\ \\text{cm}^3 = 314\\tfrac{2}{7}\\ \\text{cm}^3") + " है।")
ANS["11.3 Q7"] = "100π = 2200/7 = 314 2/7 cm³"
E3.append(("भुजाओं 5 cm, 12 cm और 13 cm वाले एक समकोण त्रिभुज ABC को भुजा 12 cm के परित घुमाया जाता है। इस प्रकार प्राप्त ठोस का आयतन ज्ञात कीजिए।", s))

# ---- Q8 ----
s = given("प्रश्न 7 का समकोण △ABC (AB = 12 cm, BC = 5 cm, AC = 13 cm)<br>इसे भुजा BC = 5 cm के परित घुमाया जाता है",
          "प्राप्त ठोस का आयतन; प्रश्न 7 और 8 के ठोसों के आयतनों का अनुपात")
s += NOFIG + solo(cone_fig(12, 5, "हल की आकृति: △ABC को BC के परित घुमाने पर शंकु; h = BC नीली, r = AB लाल, l = AC हरी (पैमाने पर)",
                           {"r": "12 cm", "h": "5 cm", "l": "13 cm"}, W=320, H=180, tri="CBA"))
s += p("भुजा BC के परित घुमाने पर BC शंकु की ऊँचाई, AB आधार की त्रिज्या और AC तिर्यक ऊँचाई बनती है:")
s += eqs((h_(), "BC = 5\\ \\text{cm}"), (r_(), "AB = 12\\ \\text{cm}"))
s += f_vcone() + vol_pi(12, 5, 240)
s += p(m("\\pi = \\dfrac{22}{7}") + " रखने पर:")
w, v = chain(T_V, [("240", 240), PI], "cm", 3, F(5280, 7), mix=True)
s += w
s += kh("दोनों ठोसों के आयतनों का अनुपात")
s += p("माना प्रश्न 7 के ठोस का आयतन " + m("V_1") + " और प्रश्न 8 के ठोस का आयतन " + m("V_2") + " है।")
s += lines("\\dfrac{V_1}{V_2}", "\\dfrac{100\\pi}{240\\pi}", "\\dfrac{100}{240}", "\\dfrac{5\\times 20}{12\\times 20}", "\\dfrac{5}{12}")
assert F(100, 240) == F(5, 12)
s += ans("प्राप्त ठोस का आयतन " + m("= 240\\pi\\ \\text{cm}^3 = 754\\tfrac{2}{7}\\ \\text{cm}^3") + "; दोनों ठोसों के आयतनों का अनुपात <b>5 : 12</b> है।")
ANS["11.3 Q8"] = "240π = 5280/7 = 754 2/7 cm³; 5:12"
E3.append(("यदि प्रश्न 7 के त्रिभुज ABC को यदि भुजा 5 cm के परित घुमाया जाए, तो इस प्रकार प्राप्त ठोस का आयतन ज्ञात कीजिए। प्रश्नों 7 और 8 में प्राप्त किए गए दोनों ठोसों के आयतनों का अनुपात भी ज्ञात कीजिए।", s))

# ---- Q9 ----
s = given("गेहूँ की शंक्वाकार ढेरी का व्यास " + m(f"{d_()} = 10.5\\ \\text{{m}}") + "<br>ऊँचाई " + m(f"{h_()} = 3\\ \\text{{m}}"),
          "(1) ढेरी का आयतन<br>(2) ढकने के लिए केनवास का क्षेत्रफल (= वक्र पृष्ठीय क्षेत्रफल)")
s += NOFIG + solo(cone_fig(F(21, 4), 3, "हल की आकृति: गेहूँ की ढेरी (पैमाने पर); d नारंगी, h नीली, l हरी",
                           {"d": "d = 10.5 m", "h": "h = 3 m", "l": "l = ?"}, W=320, H=170, unit="m"))
s += kh("त्रिज्या " + m(r_())) + r_from_d(F(21, 2), "m")
b = f_vcone()
w, v = cone_v(F(21, 4), "5.25", 3, "3", "m", F(86625, 1000))
b += w
s += part("ढेरी का आयतन", b)
b = f_l()
b += lines(l_(), f"\\sqrt{{{h_()}^2+{r_()}^2}}", f"\\sqrt{{{h_('3')}^2+{r_('5.25')}^2}}\\ \\text{{m}}", "\\sqrt{9+27.5625}\\ \\text{m}",
           "\\sqrt{36.5625}\\ \\text{m}", "\\sqrt{\\dfrac{585}{16}}\\ \\text{m}")
assert 9 + F(275625, 10000) == F(585, 16)
b += p("गुणनखंड: " + m("585 = 3\\times 3\\times 5\\times 13") + " और " + m("16 = 2\\times 2\\times 2\\times 2"))
b += lines(l_(), "\\sqrt{\\dfrac{3\\times 3\\times 5\\times 13}{2\\times 2\\times 2\\times 2}}\\ \\text{m}",
           "\\sqrt{\\dfrac{(3\\times 3)\\times 65}{(2\\times 2)\\times (2\\times 2)}}\\ \\text{m}", "\\dfrac{3\\sqrt{65}}{2\\times 2}\\ \\text{m}",
           "\\dfrac{3\\sqrt{65}}{4}\\ \\text{m}")
b += p("65 पूर्ण वर्ग नहीं है; " + m("\\sqrt{65} = 8.062") + " (तीन दशमलव स्थान तक) लेने पर:")
b += lines(l_(), "\\dfrac{3\\times 8.062}{4}\\ \\text{m}", "\\dfrac{24.186}{4}\\ \\text{m}", "6.0465\\ \\text{m}", l_("6.05") + "\\ \\text{m (दो दशमलव स्थान तक)}")
assert abs(math.sqrt(585 / 16) - 6.0467) < 1e-3 and abs(3 * 8.062 / 4 - 6.0465) < 1e-9
b += f_csa()
w, v = pi_r_l(F(21, 4), "5.25", F(605, 100), "6.05", "m", F(99825, 1000))
b += w
s += part("केनवास का क्षेत्रफल", b)
s += ans("ढेरी का आयतन " + m("= 86.625\\ \\text{m}^3") + "; वाँछित केनवास का क्षेत्रफल " + m("= 99.825\\ \\text{m}^2") +
         " (" + m("l = 6.05\\ \\text{m}") + " लेने पर)")
ANS["11.3 Q9"] = "V 86.625 m³; l = 3√65/4 ≈ 6.05 m; canvas 99.825 m²"
E3.append(("गेहूँ की एक ढेरी 10.5 m व्यास और ऊँचाई 3 m वाले एक शंकु के आकार की है। इसका आयतन ज्ञात कीजिए। इस ढेरी को वर्षा से बचाने के लिए केनवास से ढका जाना है। वाँछित केनवास का क्षेत्रफल ज्ञात कीजिए।", s))
assert len(E3) == 9

# ======================= प्रश्नावली 11.4 (गोले का आयतन) =======================
E4 = []

# ---- Q1 ----
s = given("गोले की त्रिज्या " + m(r_()) + ": (i) 7 cm (ii) 0.63 m", "प्रत्येक गोले का आयतन")
s += NOFIG + solo(sphere_fig(70, "हल की आकृति: गोला, केंद्र O; त्रिज्या r लाल", "r", W=220, H=180))
s += f_vsph()
w, v = sph_v(7, "7", "cm", F(4312, 3), mix=True)
s += part("(i) " + m(f"{r_()} = 7\\ \\text{{cm}}"), w)
w, v = sph_v(F(63, 100), "0.63", "m", F(1047816, 1000000))
s += part("(ii) " + m(f"{r_()} = 0.63\\ \\text{{m}}"), w)
s += ans("(i) आयतन " + m("= 1437\\tfrac{1}{3}\\ \\text{cm}^3") + " (ii) आयतन " + m("= 1.047816\\ \\text{m}^3"))
ANS["11.4 Q1"] = "4312/3 = 1437 1/3 cm³; 1.047816 m³"
E4.append(("उस गोले का आयतन ज्ञात कीजिए जिसकी त्रिज्या निम्न है : (i) 7 cm (ii) 0.63 m", s))

# ---- Q2 ----
s = given("ठोस गोलाकार गेंद का व्यास " + m(d_()) + ": (i) 28 cm (ii) 0.21 m", "गेंद द्वारा हटाए गए (विस्थापित) पानी का आयतन")
s += NOFIG + solo(sphere_fig(70, "हल की आकृति: गेंद (गोला); व्यास d नारंगी", None, "d", W=220, H=180))
s += tp("हटाए गए पानी का आयतन = गेंद का आयतन")
s += f_vsph()
w, v = sph_v(14, "14", "cm", F(34496, 3), mix=True)
s += part("(i) " + m(f"{d_()} = 28\\ \\text{{cm}}"), r_from_d(28, "cm") + w)
w, v = sph_v(F(105, 1000), "0.105", "m", F(4851, 1000000))
s += part("(ii) " + m(f"{d_()} = 0.21\\ \\text{{m}}"), r_from_d(F(21, 100), "m") + w)
s += ans("(i) " + m("11498\\tfrac{2}{3}\\ \\text{cm}^3") + " (ii) " + m("0.004851\\ \\text{m}^3"))
ANS["11.4 Q2"] = "34496/3 = 11498 2/3 cm³; 0.004851 m³"
E4.append(("उस ठोस गोलाकार गेंद द्वारा हटाए गए (विस्थापित) पानी का आयतन ज्ञात कीजिए, जिसका व्यास निम्न है : (i) 28 cm (ii) 0.21 m", s))

# ---- Q3 ----
s = given("धातु की गेंद का व्यास " + m(f"{d_()} = 4.2\\ \\text{{cm}}") + "<br>धातु का घनत्व = 8.9 ग्राम प्रति " + cm3, "गेंद का द्रव्यमान")
s += NOFIG + solo(sphere_fig(70, "हल की आकृति: धातु की गेंद; व्यास d नारंगी", None, "d = 4.2 cm", W=220, H=180))
s += kh("त्रिज्या " + m(r_())) + r_from_d(F(21, 5), "cm")
s += f_vsph()
w, v = sph_v(F(21, 10), "2.1", "cm", F(38808, 1000))
s += w
s += formula("द्रव्यमान", "द्रव्यमान = घनत्व × आयतन")
s += lines("\\text{द्रव्यमान}", "8.9\\times 38.808\\text{ ग्राम}", "345.3912\\text{ ग्राम}")
assert F(89, 10) * F(38808, 1000) == F(3453912, 10000)
s += ans("गेंद का द्रव्यमान <b>345.3912 ग्राम</b> है।")
ANS["11.4 Q3"] = "V 38.808 cm³; 345.3912 g"
E4.append(("धातु की एक गेंद का व्यास 4.2 cm है। यदि इस धातु का घनत्व 8.9 ग्राम प्रति " + cm3 + " है, तो इस गेंद का द्रव्यमान ज्ञात कीजिए।", s))

# ---- Q4 ----
s = given("चंद्रमा का व्यास = पृथ्वी के व्यास का " + m("\\dfrac{1}{4}") + " (लगभग)", "चंद्रमा का आयतन पृथ्वी के आयतन की कौन-सी भिन्न है")
s += NOFIG + solo(two_spheres("हल की आकृति: पृथ्वी (त्रिज्या R नीली) और चंद्रमा (त्रिज्या r लाल); r = R/4 (पैमाने पर)", 4,
                              ("R", "r"), ("पृथ्वी", "चंद्रमा")))
s += p("माना पृथ्वी की त्रिज्या " + m(C(BLU, "R")) + " है। व्यास एक-चौथाई है, तो त्रिज्या भी एक-चौथाई होगी:")
s += lines(f"\\text{{चंद्रमा की त्रिज्या }}{r_()}", r_("\\dfrac{R}{4}"))
s += f_vsph()
s += p("माना चंद्रमा का आयतन " + m("V_1") + " और पृथ्वी का आयतन " + m("V_2") + " है।")
s += lines("\\dfrac{V_1}{V_2}", f"\\dfrac{{\\dfrac{{4}}{{3}}\\pi {r_()}^3}}{{\\dfrac{{4}}{{3}}\\pi {C(BLU, 'R')}^3}}",
           f"\\dfrac{{{r_()}^3}}{{{C(BLU, 'R')}^3}}", f"\\dfrac{{\\left({r_('\\dfrac{R}{4}')}\\right)^3}}{{R^3}}", "\\dfrac{R^3}{64}\\times \\dfrac{1}{R^3}",
           "\\dfrac{1}{64}")
s += ans("चंद्रमा का आयतन पृथ्वी के आयतन का " + m("\\dfrac{1}{64}") + " भाग है।")
ANS["11.4 Q4"] = "1/64"
E4.append(("चंद्रमा का व्यास पृथ्वी के व्यास का लगभग एक-चौथाई है। चंद्रमा का आयतन पृथ्वी के आयतन की कौन-सी भिन्न है?", s))

# ---- Q5 ----
s = given("अर्धगोलाकार कटोरे का व्यास " + m(f"{d_()} = 10.5\\ \\text{{cm}}"), "कटोरे में आने वाला दूध (लीटर में)")
s += NOFIG + solo(hemi_fig(F(21, 4), "हल की आकृति: अर्धगोलाकार कटोरा; व्यास d नारंगी", None, "d = 10.5 cm"))
s += kh("त्रिज्या " + m(r_())) + r_from_d(F(21, 2), "cm")
s += f_vhem()
w, v = sph_v(F(21, 4), "5.25", "cm", F(3031875, 10000), frac=("\\dfrac{2}{3}", F(2, 3)), sym="\\dfrac{2}{3}")
s += w
s += tp(m("1000\\ \\text{cm}^3 = 1") + " लीटर")
s += lines("\\text{दूध}", "\\dfrac{303.1875}{1000}\\text{ लीटर}", "0.3031875\\text{ लीटर}")
s += ans("कटोरे में <b>0.3031875 लीटर</b> दूध आ सकता है।")
ANS["11.4 Q5"] = "303.1875 cm³ = 0.3031875 L"
E4.append(("व्यास 10.5 cm वाले एक अर्धगोलाकार कटोरे में कितने लीटर दूध आ सकता है?", s))

# ---- Q6 ----
s = given("अर्धगोलाकार टंकी की आंतरिक त्रिज्या " + m(f"{r_()} = 1\\ \\text{{m}}") + "<br>लोहे की चादर की मोटाई = 1 cm",
          "टंकी बनाने में लगे लोहे का आयतन")
s += NOFIG + solo(hemi_fig(1, "हल की आकृति: अर्धगोलाकार टंकी; आंतरिक त्रिज्या r लाल, बाहरी त्रिज्या R बैंगनी", "r = 1 m", R=F(101, 100),
                           Rlab="R", draw_R=F(109, 100), tnote="(1 cm की मोटाई स्पष्टता के लिए बड़ी दिखाई गई है)", H=200))
s += kh("बाहरी त्रिज्या " + m(R_()))
s += lines(R_(), f"{r_()} + \\text{{मोटाई}}", "1\\ \\text{m} + 1\\ \\text{cm}", "1\\ \\text{m} + 0.01\\ \\text{m}", R_("1.01") + "\\ \\text{m}")
s += f_vhem()
s += p("लोहे का आयतन = बाहरी अर्धगोले का आयतन − भीतरी अर्धगोले का आयतन")
s += lines("\\text{लोहे का आयतन}", f"\\dfrac{{2}}{{3}}\\pi {R_()}^3 - \\dfrac{{2}}{{3}}\\pi {r_()}^3", f"\\dfrac{{2}}{{3}}\\pi\\left({R_()}^3 - {r_()}^3\\right)",
           f"\\dfrac{{2}}{{3}}\\times \\dfrac{{22}}{{7}}\\times \\left({R_('1.01')}^3 - {r_('1')}^3\\right)\\ \\text{{m}}^3",
           "\\dfrac{2}{3}\\times \\dfrac{22}{7}\\times (1.030301 - 1)\\ \\text{m}^3", "\\dfrac{2}{3}\\times \\dfrac{22}{7}\\times 0.030301\\ \\text{m}^3",
           "\\dfrac{44\\times 0.030301}{21}\\ \\text{m}^3", "\\dfrac{1.333244}{21}\\ \\text{m}^3", "0.06349\\ \\text{m}^3\\text{ (लगभग)}")
iron = F(2, 3) * F(22, 7) * (F(101, 100) ** 3 - 1)
assert F(101, 100) ** 3 == F(1030301, 1000000) and iron == F(1333244, 21 * 1000000) and abs(float(iron) - 0.06349) < 5e-6
s += ans("टंकी बनाने में लगे लोहे का आयतन " + m("= 0.06349\\ \\text{m}^3") + " (लगभग, पाँच दशमलव स्थान तक) है।")
ANS["11.4 Q6"] = "1.333244/21 = 0.063488 ≈ 0.06349 m³"
E4.append(("एक अर्धगोलाकार टंकी 1 cm मोटी एक लोहे की चादर (sheet) से बनी है। यदि इसकी आंतरिक त्रिज्या 1 m है, तो इस टंकी के बनाने में लगे लोहे का आयतन ज्ञात कीजिए।", s))

# ---- Q7 ----
s = given("गोले का पृष्ठीय क्षेत्रफल " + m("= 154\\ \\text{cm}^2"), "गोले का आयतन")
s += NOFIG + solo(sphere_fig(70, "हल की आकृति: गोला, केंद्र O; त्रिज्या r लाल", "r = ?", W=220, H=180))
s += kh("त्रिज्या " + m(r_()) + " ज्ञात करना") + r_from_sa154()
s += kh("आयतन") + f_vsph()
w, v = sph_v(F(7, 2), "3.5", "cm", F(539, 3), mix=True)
s += w
s += ans("गोले का आयतन " + m("= 179\\tfrac{2}{3}\\ \\text{cm}^3") + " है।")
ANS["11.4 Q7"] = "r 3.5 cm, 539/3 = 179 2/3 cm³"
E4.append(("उस गोले का आयतन ज्ञात कीजिए जिसका पृष्ठीय क्षेत्रफल 154 " + cm2 + " है।", s))

# ---- Q8 ----
s = given("गुंबद अर्धगोलाकार है<br>अंदर सफेदी का कुल व्यय = ₹4989.60<br>सफेदी की दर = ₹20 प्रति वर्ग मीटर",
          "(i) गुंबद का आंतरिक वक्र पृष्ठीय क्षेत्रफल<br>(ii) गुंबद के अंदर की हवा का आयतन")
s += NOFIG + solo(hemi_fig(F(63, 10), "हल की आकृति: अर्धगोलाकार गुंबद; आंतरिक त्रिज्या r लाल", "r = ?", dome=True))
b = lines("\\text{आंतरिक वक्र पृष्ठीय क्षेत्रफल}", "\\text{कुल व्यय} \\div \\text{दर}", "\\dfrac{4989.60}{20}\\ \\text{m}^2", "249.48\\ \\text{m}^2")
assert F(498960, 100) / 20 == F(24948, 100)
s += part("(i) आंतरिक वक्र पृष्ठीय क्षेत्रफल", b)
b = kh("आंतरिक त्रिज्या " + m(r_())) + f_hcsa()
b += eqsu("m^2", (f"2\\pi {r_()}^2", "249.48"), (f"2\\times \\dfrac{{22}}{{7}}\\times {r_()}^2", "249.48"), (f"\\dfrac{{44}}{{7}}{r_()}^2", "249.48"),
         (f"{r_()}^2", "\\dfrac{249.48\\times 7}{44}"), (f"{r_()}^2", "5.67\\times 7"), (f"{r_()}^2", "39.69"))
assert F(24948, 100) * 7 / 44 == F(3969, 100) and F(24948, 100) / 44 == F(567, 100)
b += lad_for(F(3969, 100))
b += lines(r_(), "\\sqrt{39.69}\\ \\text{m}", *sq_rows(F(3969, 100), "m")[:-1], r_("6.3") + "\\ \\text{m}")
b += kh("हवा का आयतन = अर्धगोले का आयतन") + f_vhem()
w, v = sph_v(F(63, 10), "6.3", "m", F(523908, 1000), frac=("\\dfrac{2}{3}", F(2, 3)), sym="\\dfrac{2}{3}")
b += w
s += part("(ii) गुंबद के अंदर की हवा का आयतन", b)
s += ans("(i) आंतरिक वक्र पृष्ठीय क्षेत्रफल " + m("= 249.48\\ \\text{m}^2") + " (ii) हवा का आयतन " + m("= 523.908\\ \\text{m}^3"))
ANS["11.4 Q8"] = "249.48 m², r 6.3 m, 523.908 m³"
E4.append(("किसी भवन का गुंबद एक अर्धगोले के आकार का है। अंदर से, इसमें सफेदी कराने में ₹4989.60 व्यय हुए। यदि सफेदी कराने की दर ₹20 प्रति वर्ग मीटर है, तो ज्ञात कीजिए: (i) गुंबद का आंतरिक वक्र पृष्ठीय क्षेत्रफल (ii) गुंबद के अंदर की हवा का आयतन", s))

# ---- Q9 ----
RP = C(PUR, "r'")
s = given("27 ठोस गोले, प्रत्येक की त्रिज्या " + m(r_()) + " और पृष्ठीय क्षेत्रफल S<br>इन्हें पिघलाकर बने नए गोले की त्रिज्या " +
          m(C(PUR, "r'")) + " और पृष्ठीय क्षेत्रफल S′", "(i) नए गोले की त्रिज्या " + m(C(PUR, "r'")) + "<br>(ii) S और S′ का अनुपात")
s += p("पिघलाकर नया गोला बनाने पर धातु का आयतन नहीं बदलता।") + f_vsph()
b = lines("\\text{नए गोले का आयतन}", "27\\times \\text{एक छोटे गोले का आयतन}")
b += eqs((f"\\dfrac{{4}}{{3}}\\pi {RP}^3", f"27\\times \\dfrac{{4}}{{3}}\\pi {r_()}^3"), (f"{RP}^3", f"27{r_()}^3"),
         (f"{RP}^3", f"3\\times 3\\times 3\\times {r_()}\\times {r_()}\\times {r_()}"), (f"{RP}^3", f"(3{r_()})^3"),
         (C(PUR, "r'"), C(PUR, f"3{r_()}")))
s += part("(i) नए गोले की त्रिज्या", b)
b = f_sph()
b += lines("S", f"4\\pi {r_()}^2")
b += lines("S'", f"4\\pi {RP}^2", f"4\\pi (3{r_()})^2", f"4\\pi\\times 9{r_()}^2", f"36\\pi {r_()}^2")
b += lines("\\dfrac{S}{S'}", f"\\dfrac{{4\\pi {r_()}^2}}{{36\\pi {r_()}^2}}", "\\dfrac{4}{36}", "\\dfrac{1}{9}")
s += part("(ii) S और S′ का अनुपात", b)
s += ans("(i) " + m("r' = 3r") + " (ii) S : S′ = <b>1 : 9</b>")
ANS["11.4 Q9"] = "r' = 3r, 1:9"
E4.append(("लोहे के सत्ताइस ठोस गोलों को पिघलाकर, जिनमें से प्रत्येक की त्रिज्या " + m("r") + " है और पृष्ठीय क्षेत्रफल S है, एक बड़ा गोला बनाया जाता है जिसका पृष्ठीय क्षेत्रफल S′ है। ज्ञात कीजिए: (i) नए गोले की त्रिज्या " + m("r'") + " (ii) S और S′ का अनुपात", s))

# ---- Q10 ----
s = given("कैपसूल (गोला) का व्यास " + m(f"{d_()} = 3.5\\ \\text{{mm}}"), "कैपसूल भरने के लिए आवश्यक दवाई (" + m("\\text{mm}^3") + " में)")
s += NOFIG + solo(sphere_fig(60, "हल की आकृति: गोलाकार कैपसूल; व्यास d नारंगी", None, "d = 3.5 mm", W=220, H=160))
s += kh("त्रिज्या " + m(r_())) + r_from_d(F(7, 2), "mm")
s += f_vsph()
w, v = sph_v(F(7, 4), "1.75", "mm", F(539, 24), mix=True)
s += w
s += ans("कैपसूल भरने के लिए " + m("22\\tfrac{11}{24}\\ \\text{mm}^3") + " दवाई की आवश्यकता होगी।")
ANS["11.4 Q10"] = "539/24 = 22 11/24 mm³ (≈22.46)"
E4.append(("दवाई का एक कैपसूल (capsule) 3.5 mm व्यास का एक गोला (गोली) है। इस कैपसूल को भरने के लिए कितनी दवाई (" + m("\\text{mm}^3") + " में) की आवश्यकता होगी?", s))
assert len(E4) == 10

# ---------------------------------------------------------------------
PIN = "<div class='pin'>जब तक अन्यथा न कहा जाए, " + m("\\pi = \\dfrac{22}{7}") + " लीजिए।</div>"
SUB = "कक्षा 9 गणित · अध्याय 11: " + CH + " · {} प्रश्न"
EXS = [("11-1", "11.1", E1), ("11-2", "11.2", E2), ("11-3", "11.3", E3), ("11-4", "11.4", E4)]
for i, (sl, nm, E) in enumerate(EXS):
    E = [(qt(a), b) for a, b in E]
    E[0] = (E[0][0], PIN + E[0][1])
    check_tex(E)
    prev = (BASE + f"exercise-{EXS[i - 1][0]}/", "प्रश्नावली " + EXS[i - 1][1]) if i else ("/hi/class-09/maths/chapter-10/exercise-10-1/", "प्रश्नावली 10.1")
    nxt = (BASE + f"exercise-{EXS[i + 1][0]}/", "प्रश्नावली " + EXS[i + 1][1]) if i < 3 else ("/hi/class-09/maths/chapter-12/exercise-12-1/", "प्रश्नावली 12.1")
    page(BASE, 11, CH, f"exercise-{sl}", f"प्रश्नावली {nm}", SUB.format(len(E)), E, prev, nxt, css=CSS + EXTRA_CSS, boards=BOARDS11)
for k_, v_ in ANS.items():
    print(k_, v_)
print("ok")
