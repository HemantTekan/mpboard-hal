#!/usr/bin/env python3
"""Class 9 Maths, Chapter 10 (हीरोन का सूत्र): Exercise 10.1, Hindi medium.
Rationalised book (2023-24 onward; NCERT iemh110 'Rationalised Textbooks 2022-23', print 2024-25) = old chapter 12 (हीरोन का सूत्र):
  old 12.3 (area of quadrilaterals) and old प्रश्नावली 12.2 removed; 10.1 = old 12.1 (6 Q), question numbers unchanged.
  Figures renumbered like the current book: old 12.9 (flyover wall) -> 10.6, old 12.10 (slide wall) -> 10.7.
Question text copied from NCERT Hindi PDF ihmh112 (archive.org ncert-ihmh1, chapter 12 of the 2020-21 print).
Style as chapters 6-9: each side has one colour in the solution figure and the same colour in the working
(a red, b blue, c green, s purple; s - a red, s - b blue, s - c green). Every triangle is drawn to scale from its
three sides (law of cosines), so side lengths and angles are true.
Under every square root: prime factorisation (division ladders), then pairs, then the root.
Run from repo root: python3 tools/solutions/class9_ch10.py
"""
import sys, pathlib, math
from collections import Counter
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from common import *  # noqa
from mixed_cells import *  # noqa

BASE = "/hi/class-09/maths/chapter-10/"
CH = "हीरोन का सूत्र"
BOARDS10 = ("यह हल <b>MP Board (MPBSE)</b> कक्षा 9 गणित की पाठ्यपुस्तक के अध्याय 10 ‘हीरोन का सूत्र’ के अनुसार है।")
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
.pn{font-size:.9em;color:#4d5568;margin:2px 0 4px}
"""

# ---------------- colours (same in figures and in the working) ----------------
INK = "#1d3a8a"
RED, BLU, GRN, ORG, PUR = "#d62839", "#1769c2", "#0f8a4c", "#e06a00", "#7c3aed"
SC = (RED, BLU, GRN)          # colours of sides a, b, c (and of s - a, s - b, s - c)
FONT = "font-family=\"Noto Sans, 'Noto Sans Devanagari', sans-serif\""


def C(col, t):
    return "\\textcolor{" + col + "}{" + t + "}"


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
    return f"<div style='max-width:430px;margin:0 auto'>{f}</div>"


def pair(a, b):
    return f"<div class='figs'>{a}{b}</div>"


# ---------------- SVG figure kit (same as chapter 9) ----------------
class Fig:
    n = 0

    def __init__(self, W, H):
        Fig.n += 1
        self.id, self.W, self.H, self.bg, self.el, self.top, self.marks = f"f10{Fig.n}", W, H, [], [], [], {}

    @staticmethod
    def pol(o, deg, r):
        a = math.radians(deg)
        return (o[0] + r * math.cos(a), o[1] - r * math.sin(a))

    @staticmethod
    def dir(p, q):
        return math.degrees(math.atan2(-(q[1] - p[1]), q[0] - p[0])) % 360

    def _mk(self, col):
        if col not in self.marks:
            self.marks[col] = f"{self.id}m{len(self.marks)}"
        return self.marks[col]

    def line(self, p, q, col=INK, w=2.2, a1=False, a2=False, dash=None):
        d = f" stroke-dasharray='{dash}'" if dash else ""
        ms = f" marker-start='url(#{self._mk(col)})'" if a1 else ""
        me = f" marker-end='url(#{self._mk(col)})'" if a2 else ""
        self.el.append(f"<line x1='{p[0]:.1f}' y1='{p[1]:.1f}' x2='{q[0]:.1f}' y2='{q[1]:.1f}' stroke='{col}' stroke-width='{w}' "
                       f"stroke-linecap='round'{d}{ms}{me}/>")

    def poly(self, pts, col, op=.09):
        d = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        self.bg.append(f"<polygon points='{d}' fill='{col}' fill-opacity='{op}' stroke='none'/>")

    def ticks(self, p, q, n=1, col=INK, at=.5, h=6.5, gap=5):
        d = self.dir(p, q)
        c0 = (p[0] + (q[0] - p[0]) * at, p[1] + (q[1] - p[1]) * at)
        for k in range(n):
            c = self.pol(c0, d, (k - (n - 1) / 2) * gap)
            a, b = self.pol(c, d + 90, h), self.pol(c, d - 90, h)
            self.top.insert(0, f"<line x1='{a[0]:.1f}' y1='{a[1]:.1f}' x2='{b[0]:.1f}' y2='{b[1]:.1f}' stroke='{col}' stroke-width='2.2' stroke-linecap='round'/>")

    def par(self, p, q, n=1, col=INK, at=.5, gap=7):
        """n arrow-heads (chevrons) on segment pq pointing p -> q: the book's mark for parallel sides."""
        d = self.dir(p, q)
        c0 = (p[0] + (q[0] - p[0]) * at, p[1] + (q[1] - p[1]) * at)
        for k in range(n):
            tip = self.pol(c0, d, 3.5 + (k - (n - 1) / 2) * gap)
            w1, w2 = self.pol(tip, d + 148, 9), self.pol(tip, d - 148, 9)
            self.top.insert(0, f"<path d='M{w1[0]:.1f},{w1[1]:.1f} L{tip[0]:.1f},{tip[1]:.1f} L{w2[0]:.1f},{w2[1]:.1f}' fill='none' stroke='{col}' "
                               f"stroke-width='2.3' stroke-linecap='round' stroke-linejoin='round'/>")

    def sqm(self, p, q, col=INK, at=.5, s=3.6):
        c = (p[0] + (q[0] - p[0]) * at, p[1] + (q[1] - p[1]) * at)
        self.top.insert(0, f"<rect x='{c[0] - s:.1f}' y='{c[1] - s:.1f}' width='{2 * s}' height='{2 * s}' fill='{col}'/>")

    def arc(self, o, a1, a2, r, col, fill=True, n=1, w=2, dash=None, op=.16):
        span = (a2 - a1) % 360
        large = 1 if span > 180 else 0
        p1, p2 = self.pol(o, a1, r), self.pol(o, a2, r)
        if fill:
            self.el.append(f"<path d='M{o[0]:.1f},{o[1]:.1f} L{p1[0]:.1f},{p1[1]:.1f} A{r},{r} 0 {large} 0 {p2[0]:.1f},{p2[1]:.1f} Z' "
                           f"fill='{col}' fill-opacity='{op}' stroke='none'/>")
        d = f" stroke-dasharray='{dash}'" if dash else ""
        for k in range(n):
            rr = r - 4.5 * k
            q1, q2 = self.pol(o, a1, rr), self.pol(o, a2, rr)
            self.el.append(f"<path d='M{q1[0]:.1f},{q1[1]:.1f} A{rr},{rr} 0 {large} 0 {q2[0]:.1f},{q2[1]:.1f}' fill='none' "
                           f"stroke='{col}' stroke-width='{w}'{d}/>")

    def _span(self, V, P1, P2):
        a1, a2 = self.dir(V, P1), self.dir(V, P2)
        if (a2 - a1) % 360 > 180:
            a1, a2 = a2, a1
        return a1, a2

    def arcp(self, V, P1, P2, r, col, n=1, fill=True, dash=None, w=2, trim=0):
        a1, a2 = self._span(V, P1, P2)
        if trim and fill:
            self.arc(V, a1, a2, r, col, True, 0)
        if trim:
            span = (a2 - a1) % 360
            t = min(trim, span / 6)
            a1, a2 = a1 + t, a1 + span - t
        self.arc(V, a1, a2, r, col, fill and not trim, n, w, dash)

    def right(self, o, a1, s=12, col=INK):
        p1 = self.pol(o, a1, s)
        p3 = self.pol(o, a1 + 90, s)
        p2 = self.pol(p1, a1 + 90, s)
        self.el.append(f"<path d='M{p1[0]:.1f},{p1[1]:.1f} L{p2[0]:.1f},{p2[1]:.1f} L{p3[0]:.1f},{p3[1]:.1f}' fill='none' stroke='{col}' stroke-width='1.8'/>")

    def rightp(self, V, P1, P2, s=12, col=INK):
        a1, a2 = self._span(V, P1, P2)
        self.right(V, a1, s, col)

    def text(self, x, y, t, col=INK, size=16, italic=False, bold=True, anchor="middle"):
        st = " font-style='italic'" if italic else ""
        self.top.append(f"<text x='{x:.1f}' y='{y:.1f}' font-size='{size}' font-weight='{700 if bold else 500}' fill='{col}' "
                        f"text-anchor='{anchor}' dominant-baseline='central'{st} stroke='#fbfcff' stroke-width='4.5' "
                        f"stroke-linejoin='round' paint-order='stroke'>{t}</text>")

    def lab(self, p, t, deg, d=15, col=INK, size=16, italic=False):
        q = self.pol(p, deg, d)
        self.text(q[0], q[1], t, col, size, italic)

    def alabp(self, V, P1, P2, r, t, col, size=12):
        a1, a2 = self._span(V, P1, P2)
        self.lab(V, t, a1 + ((a2 - a1) % 360) / 2, r, col, size)

    def dot(self, p, col=INK, r=3):
        self.top.insert(0, f"<circle cx='{p[0]:.1f}' cy='{p[1]:.1f}' r='{r}' fill='{col}'/>")

    def svg(self, cap):
        defs = "".join(f"<marker id='{mid}' viewBox='0 0 10 10' refX='8.5' refY='5' markerWidth='11' markerHeight='11' "
                       f"markerUnits='userSpaceOnUse' orient='auto-start-reverse'><path d='M0,0.5 L10,5 L0,9.5 L2.6,5 z' fill='{col}'/></marker>"
                       for col, mid in self.marks.items())
        return (f"<div class='fig'><svg viewBox='0 0 {self.W} {self.H}' role='img' aria-label='{cap}' style='max-width:{max(self.W, 360)}px' {FONT}>"
                f"<defs>{defs}</defs>{''.join(self.bg)}{''.join(self.el)}{''.join(self.top)}</svg><div class='cap'>{cap}</div></div>")




# ---------------- triangle drawn to scale from its three sides ----------------
def tri_unit(a, b, c, base="a", mirror=False):
    """A, B, C (y up) with BC = a, CA = b, AB = c; side `base` horizontal, third vertex above it."""
    assert a + b > c and b + c > a and c + a > b
    P = {"A": (0.0, 0.0), "B": (float(c), 0.0)}
    x = (b * b - a * a + c * c) / (2 * c)
    P["C"] = (x, math.sqrt(b * b - x * x))
    e1, e2 = {"a": "BC", "b": "CA", "c": "AB"}[base]
    p, q = P[e1], P[e2]
    t = math.atan2(q[1] - p[1], q[0] - p[0])
    ct, st = math.cos(-t), math.sin(-t)
    R = {k: ((v[0] - p[0]) * ct - (v[1] - p[1]) * st, (v[0] - p[0]) * st + (v[1] - p[1]) * ct) for k, v in P.items()}
    apex = ({"A", "B", "C"} - {e1, e2}).pop()
    if R[apex][1] < 0:
        R = {k: (v[0], -v[1]) for k, v in R.items()}
    if mirror:
        R = {k: (-v[0], v[1]) for k, v in R.items()}
    return R


def fit(R, W, H, mx, my_top, my_bot):
    xs, ys = [v[0] for v in R.values()], [v[1] for v in R.values()]
    k = min((W - 2 * mx) / (max(xs) - min(xs)), (H - my_top - my_bot) / (max(ys) - min(ys)))
    ox = (W - k * (max(xs) - min(xs))) / 2 - k * min(xs)
    P = {n: (ox + k * v[0], H - my_bot - k * (v[1] - min(ys))) for n, v in R.items()}
    return P, k


SIDE = {"a": "BC", "b": "CA", "c": "AB"}


def side_label(f, P, nm, t, col, size=13, gap=11):
    p, q = P[SIDE[nm][0]], P[SIDE[nm][1]]
    g = ((P["A"][0] + P["B"][0] + P["C"][0]) / 3, (P["A"][1] + P["B"][1] + P["C"][1]) / 3)
    mx_, my_ = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
    dx, dy = q[0] - p[0], q[1] - p[1]
    L = math.hypot(dx, dy)
    nx, ny = -dy / L, dx / L
    if (mx_ - g[0]) * nx + (my_ - g[1]) * ny < 0:
        nx, ny = -nx, -ny
    w = 0.58 * size * len(t)
    off = gap + abs(nx) * w / 2 + abs(ny) * size * 0.55
    f.text(mx_ + nx * off, my_ + ny * off, t, col, size, bold=True)


def tri_fig(vals, sol, cap, base="a", mirror=False, W=360, H=200, unit="cm", names=None, ticks=None, right=None,
            letters=True, labs=None, cols=SC, mx=46):
    """Triangle ABC to scale.  vals = (a, b, c) = (BC, CA, AB) in `unit`.
    sol=False: book style (ink, value labels only); sol=True: sides coloured a/b/c, labels 'a = 12 cm'."""
    a, b, c = vals
    R = tri_unit(a, b, c, base, mirror)
    P, k = fit(R, W, H, mx, 30, 30)
    for nm, v in zip("abc", vals):          # true proportions
        close(math.dist(P[SIDE[nm][0]], P[SIDE[nm][1]]), k * v)
    f = Fig(W, H)
    if sol:
        f.poly([P["A"], P["B"], P["C"]], "#f4b400", .12)
    for i, nm in enumerate("abc"):
        col = cols[i] if sol else INK
        f.line(P[SIDE[nm][0]], P[SIDE[nm][1]], col, 3.2 if sol else 2.2)
        n_t = (ticks or {}).get(nm)
        if n_t:
            f.ticks(P[SIDE[nm][0]], P[SIDE[nm][1]], n_t, col if sol else INK, .3)
        if labs:
            t = labs[i]
        else:
            t = f"{fmt(vals[i])} {unit}"
            if sol:
                t = f"{(names or 'abc')[i]} = {t}"
        side_label(f, P, nm, t, col, 13)
    if right:
        o = [x for x in "ABC" if x != right]
        f.rightp(P[right], P[o[0]], P[o[1]], 11, PUR if sol else INK)
    if letters:
        g = ((P["A"][0] + P["B"][0] + P["C"][0]) / 3, (P["A"][1] + P["B"][1] + P["C"][1]) / 3)
        for n in "ABC":
            f.dot(P[n])
            d = Fig.dir(g, P[n])
            f.lab(P[n], n, d, 15)
    for n, (x, y) in P.items():
        assert 8 < x < W - 8 and 8 < y < H - 8, (cap, n, x, y)
    return f.svg(cap)


def fmt(v):
    return str(int(v)) if float(v).is_integer() else str(v)


# ---------------- working helpers ----------------
def M_(t):
    return m(t)


def heron_formula():
    return formula("हीरोन का सूत्र", "त्रिभुज का क्षेत्रफल " + m("= \\sqrt{s(s-a)(s-b)(s-c)}") +
                   ", जहाँ " + m("a, b, c") + " त्रिभुज की भुजाएँ हैं और " + m("s = \\dfrac{a+b+c}{2}") + " (अर्धपरिमाप) है।")


def s_steps(vals, unit, cols=SC, names="abc"):
    a, b, c = vals
    tot = a + b + c
    assert tot % 2 == 0
    s = tot // 2
    abc = "+".join(C(cols[i], x) for i, x in enumerate(names))
    nums = "+".join(C(cols[i], fmt(v)) for i, v in enumerate(vals))
    out = kh("अर्धपरिमाप " + m(C(PUR, "s")) + " ज्ञात करना")
    out += lines(C(PUR, "s"), f"\\dfrac{{{abc}}}{{2}}", f"\\dfrac{{{nums}}}{{2}}", f"\\dfrac{{{tot}}}{{2}}",
                 C(PUR, str(s)) + f"\\ \\text{{{unit}}}")
    uniq = [i for i, nm in enumerate(names) if nm not in names[:i]]
    out += kh(m(",\\ ".join("s-" + names[i] for i in uniq)) + " ज्ञात करना")
    if len(uniq) < 3:
        out += p("तीनों भुजाएँ बराबर हैं, इसलिए " + m("(s-" + names[0] + ")") + " तीनों गुणनखंडों में एक ही होगा:")
    for i in uniq:
        nm, v = names[i], vals[i]
        out += lines(C(PUR, "s") + "-" + C(cols[i], nm), C(PUR, str(s)) + "-" + C(cols[i], fmt(v)),
                     C(cols[i], fmt(s - v)) + f"\\ \\text{{{unit}}}")
        assert s - v > 0
    return out, s


def X_(xs):
    return "\\times ".join(map(str, xs))


def _w(t):
    """rough rendered width (px at 16px) of a TeX product"""
    import re as _r
    t2 = _r.sub(r"\\textcolor\{[^}]*\}", "", t)
    return 18 * t2.count("\\times") + 9.5 * len(_r.findall(r"\d", t2)) + 6 * (t2.count("(") + t2.count(")")) + 9 * t2.count("-")


def split_rows(groups, maxw=180, sep="\\times "):
    """groups: TeX pieces of a product; one row if it fits on a phone, else several rows (each new row starts with ×)."""
    if _w(sep.join(groups)) <= maxw or len(groups) < 2:
        return sep.join(groups)
    rows, cur = [], []
    for g in groups:
        if cur and _w(sep.join(cur + [g])) + (18 if rows else 0) > maxw:
            rows.append(cur)
            cur = []
        cur.append(g)
    rows.append(cur)
    out = [sep.join(r) for r in rows]
    return "\\begin{array}{l}" + "\\\\ ".join(("" if i == 0 else "\\times ") + r for i, r in enumerate(out)) + "\\end{array}"


def root_of_product(nums, cols, unit2, lhs):
    """√(n1 × n2 × ...) : ladders for each composite factor, prime factorisation, pairs, the root."""
    comp = [n for i, n in enumerate(nums) if n > 1 and len(factors(n)) > 1 and n not in nums[:i]]
    primes = sorted({n for n in nums if n > 1 and len(factors(n)) == 1})
    out = ""
    if comp:
        out += p("गुणनखंड (अभाज्य गुणनखंड भाग-विधि से):") + ladders(*comp)
    if primes:
        out += p(", ".join(map(str, primes)) + (" अभाज्य संख्या है।" if len(primes) == 1 else " अभाज्य संख्याएँ हैं।"))
    allp = []
    grp = []
    for n, col in zip(nums, cols):
        fs = factors(n) if n > 1 else [1]
        allp += [x for x in fs if x > 1]
        t = X_(fs)
        grp.append(C(col, f"({t})" if len(fs) > 1 else t))
    cnt = Counter(allp)
    pairs, rest, outside = [], [], 1
    for pr in sorted(cnt):
        q_, r_ = divmod(cnt[pr], 2)
        pairs += [f"({pr}\\times {pr})"] * q_
        rest += [str(pr)] * r_
        outside *= pr ** q_
    inside = math.prod(int(x) for x in rest) if rest else 1
    U = f"\\ \\text{{{unit2}}}^2"
    rows = [f"\\sqrt{{{split_rows(grp)}}}" + U,
            f"\\sqrt{{{split_rows([str(x) for x in sorted(allp)])}}}" + U,
            f"\\sqrt{{{split_rows(pairs + rest)}}}" + U]
    outs = []
    for pr in sorted(cnt):
        outs += [str(pr)] * (cnt[pr] // 2)
    rin = X_(rest)
    if inside == 1:
        rows.append(X_(outs) + U)
        val = f"{outside}"
    else:
        rows.append(X_(outs) + f"\\times\\sqrt{{{rin}}}" + U if outs else f"\\sqrt{{{rin}}}" + U)
        if len(rest) > 1:
            rows.append(X_(outs) + f"\\sqrt{{{inside}}}" + U)
        val = f"{outside}\\sqrt{{{inside}}}"
    rows.append(val + U)
    # check
    close(math.prod(nums), outside * outside * inside)
    return out, rows, outside, inside


def area_block(vals, s, unit, lhs="\\text{क्षेत्रफल}", what="त्रिभुज का क्षेत्रफल", cols=SC, names="abc"):
    """Heron substitution and the root, all in one aligned chain."""
    a, b, c = vals
    S = C(PUR, str(s))
    sub_parts = [S] + [f"({S}-{C(cols[i], fmt(v))})" for i, v in enumerate(vals)]
    nums = [s, s - a, s - b, s - c]
    cols = [PUR, *cols]
    prod = "\\times ".join(C(col, str(n)) for n, col in zip(nums, cols))
    fpre, rows, o, i = root_of_product(nums, cols, unit, lhs)
    U = f"\\ \\text{{{unit}}}^2"
    head = [f"\\sqrt{{{C(PUR, 's')}" + "".join(f"({C(PUR, 's')}-{C(cols[i + 1], names[i])})" for i in range(3)) + "}",
            f"\\sqrt{{{split_rows(sub_parts, maxw=160, sep='')}}}" + U, f"\\sqrt{{{split_rows([C(col, str(n)) for n, col in zip(nums, cols)])}}}" + U]
    out = fpre + p(f"अब हीरोन के सूत्र में मान रखने पर ({what}):")
    out += lines(lhs, *head, *rows)
    close(math.sqrt(s * (s - a) * (s - b) * (s - c)), o * math.sqrt(i))
    return out, o, i


# ---------------- textbook figures 10.6 and 10.7 ----------------
def fig10_6(cap):
    """Flyover: two triangular side walls 120 m x 22 m (right angle under the deck), true ratio 120 : 22."""
    W, H = 360, 150
    f = Fig(W, H)
    k = 1.05                       # px per metre
    y0 = 96
    L0, L1 = 22, 22 + 120 * k      # left wall: base from L0 to L1
    R1, R0 = W - 22, W - 22 - 120 * k
    h = 22 * k
    close(math.dist((L0, y0), (L1, y0 - h)), 122 * k)
    # roads under the bridge
    f.line((L1 + 8, y0 + 2), (L1 - 30, H - 6), INK, 1.6)
    f.line((R0 - 8, y0 + 2), (R0 + 30, H - 6), INK, 1.6)
    f.line(((L1 + R0) / 2, y0 + 4), ((L1 + R0) / 2, H - 6), INK, 1.6, dash="8 7")
    # walls
    for pts in (((L0, y0), (L1, y0), (L1, y0 - h)), ((R1, y0), (R0, y0), (R0, y0 - h))):
        f.poly(pts, "#9ec9ea", .35)
        f.line(pts[0], pts[1], INK, 2)
        f.line(pts[1], pts[2], INK, 2)
        f.line(pts[2], pts[0], INK, 2)
    # deck (arch) over the gap
    top = y0 - h
    f.el.append(f"<path d='M{L1:.1f},{top:.1f} Q{W / 2:.1f},{top - 30:.1f} {R0:.1f},{top:.1f}' fill='none' stroke='{INK}' stroke-width='2'/>")
    f.el.append(f"<path d='M{L1:.1f},{top + 7:.1f} Q{W / 2:.1f},{top - 21:.1f} {R0:.1f},{top + 7:.1f}' fill='none' stroke='{INK}' stroke-width='1.6'/>")
    # a bus on the deck
    bx, by = W / 2 - 17, top - 15 - 17
    f.el.append(f"<rect x='{bx:.1f}' y='{by:.1f}' width='34' height='14' rx='3' fill='#fff' stroke='{INK}' stroke-width='1.6'/>")
    for wx in (bx + 8, bx + 26):
        f.el.append(f"<circle cx='{wx:.1f}' cy='{by + 15:.1f}' r='2.6' fill='{INK}'/>")
    f.el.append(f"<rect x='{bx + 4:.1f}' y='{by + 3:.1f}' width='26' height='5' fill='none' stroke='{INK}' stroke-width='1'/>")
    # labels (left wall, as in the book)
    f.text(L0 + 34, y0 - h - 6, "122m", INK, 13, bold=False)
    f.text(L1 - 16, y0 - h - 8, "22m", INK, 13, bold=False)
    f.text((L0 + L1) / 2, y0 + 14, "120m", INK, 13, bold=False)
    return f.svg(cap)


def fig10_7(cap):
    """Slide wall: triangle 15 m, 11 m, 6 m drawn to scale; message painted on it; dashed measure arrows."""
    W, H = 360, 190
    R = tri_unit(15, 11, 6, "a", True)      # B right, C left; CA = 11 (left, long), AB = 6 (right)
    P, k = fit(R, W, H, 16, 44, 34)
    close(math.dist(P["B"], P["C"]), 15 * k)
    close(math.dist(P["C"], P["A"]), 11 * k)
    close(math.dist(P["A"], P["B"]), 6 * k)
    f = Fig(W, H)
    Bp, Cp, Ap = P["B"], P["C"], P["A"]
    tri = " ".join(f"{x:.1f},{y:.1f}" for x, y in (Cp, Bp, Ap))
    # hatched strip along the 6 m side (the slide's edge), clipped to the wall
    d = 9
    nx, ny = -(Ap[1] - Bp[1]), (Ap[0] - Bp[0])
    L = math.hypot(nx, ny); nx, ny = nx / L, ny / L
    if (Cp[0] - Bp[0]) * nx + (Cp[1] - Bp[1]) * ny < 0:
        nx, ny = -nx, -ny
    b2, a2 = (Bp[0] + nx * d * 3, Bp[1] + ny * d * 3), (Ap[0] + nx * d * 3, Ap[1] + ny * d * 3)
    band = " ".join(f"{x:.1f},{y:.1f}" for x, y in (Bp, Ap, (Ap[0] + nx * d, Ap[1] + ny * d), (Bp[0] + nx * d, Bp[1] + ny * d)))
    del b2, a2
    cid = f.id + "c"
    f.bg.append(f"<defs><clipPath id='{cid}t'><polygon points='{tri}'/></clipPath><clipPath id='{cid}b'><polygon points='{band}'/></clipPath></defs>")
    f.bg.append(f"<polygon points='{tri}' fill='#c9ebf7' stroke='none'/>")
    xs = range(int(min(Ap[0], Bp[0]) - 30), int(max(Ap[0], Bp[0]) + 5), 4)
    hat = "".join(f"<line x1='{x}' y1='{Ap[1] - 5:.1f}' x2='{x}' y2='{Bp[1] + 5:.1f}' stroke='{INK}' stroke-width='1'/>" for x in xs)
    f.bg.append(f"<g clip-path='url(#{cid}t)'><g clip-path='url(#{cid}b)'>{hat}</g></g>")
    f.line(Cp, Bp, INK, 2.2)
    f.line(Bp, Ap, INK, 2.2)
    f.line(Ap, Cp, INK, 2.2)

    def shifted(p, q, off, inward, cut=10):
        dx, dy = q[0] - p[0], q[1] - p[1]
        LL = math.hypot(dx, dy)
        ux, uy = dx / LL, dy / LL
        nx_, ny_ = -uy, ux
        g = ((Ap[0] + Bp[0] + Cp[0]) / 3, (Ap[1] + Bp[1] + Cp[1]) / 3)
        side = (g[0] - p[0]) * nx_ + (g[1] - p[1]) * ny_
        if (side > 0) != inward:
            nx_, ny_ = -nx_, -ny_
        return ((p[0] + ux * cut + nx_ * off, p[1] + uy * cut + ny_ * off),
                (q[0] - ux * cut + nx_ * off, q[1] - uy * cut + ny_ * off), (nx_, ny_))
    p1, q1, n1 = shifted(Cp, Ap, 7, True, 14)
    f.line(p1, q1, BLU, 1.6, a1=True, a2=True, dash="6 4")
    p2, q2, n2 = shifted(Ap, Bp, 10, False, 4)
    f.line(p2, q2, BLU, 1.6, a1=True, a2=True, dash="6 4")
    mA = ((Cp[0] + Ap[0]) / 2, (Cp[1] + Ap[1]) / 2)
    f.text(mA[0] - 6, mA[1] - 13, "11 m", INK, 13, bold=False)
    mB = ((Ap[0] + Bp[0]) / 2, (Ap[1] + Bp[1]) / 2)
    f.text(mB[0] + 26, mB[1] - 6, "6 m", INK, 13, bold=False)
    f.text((Cp[0] + Bp[0]) / 2, Bp[1] + 16, "15 m", INK, 13, bold=False)
    cx = Cp[0] + 0.60 * (Bp[0] - Cp[0])
    f.text(cx, Bp[1] - 31, "KEEP THE PARK", "#1d2433", 12.5, bold=False)
    f.top.append(f"<text x='{cx:.1f}' y='{Bp[1] - 13:.1f}' font-size='12.5' text-anchor='middle' dominant-baseline='central' fill='#1d2433'>"
                 f"<tspan fill='#1a9fd6' font-weight='700'>GREEN</tspan> AND CLEAN</text>")
    return f.svg(cap)


# ======================= प्रश्नावली 10.1 =======================
E1 = []
ANS = {}

# ---------- Q1 ----------
s = given("यातायात संकेत बोर्ड एक समबाहु त्रिभुज है; प्रत्येक भुजा = " + m("a") + "<br>(ii) में: बोर्ड का परिमाप = 180 cm",
          "(i) हीरोन के सूत्र से बोर्ड का क्षेत्रफल (" + m("a") + " के पदों में)<br>(ii) परिमाप 180 cm होने पर बोर्ड का क्षेत्रफल")
s += NOFIG + solo(tri_fig((60, 60, 60), True, "हल की आकृति: समबाहु त्रिभुज ABC; तीनों भुजाएँ a (लाल), बराबर भुजाओं पर एक-एक चिह्न",
                          W=300, H=250, labs=("a", "a", "a"), cols=(RED, RED, RED), ticks={"a": 1, "b": 1, "c": 1}))
s += key((RED, "भुजा a और s − a"), (PUR, "अर्धपरिमाप s"))
s += heron_formula()
A_ = C(RED, "a")
S_ = C(PUR, "s")
s += part("(i) भुजा " + m("a") + " वाले समबाहु त्रिभुज का क्षेत्रफल",
          p("यहाँ तीनों भुजाएँ BC, CA और AB बराबर हैं; प्रत्येक भुजा " + m(f"= {A_}")) +
          kh("अर्धपरिमाप " + m(S_) + " ज्ञात करना") +
          lines(S_, f"\\dfrac{{{A_}+{A_}+{A_}}}{{2}}", C(PUR, f"\\dfrac{{3a}}{{2}}")) +
          kh(m("s-a") + " ज्ञात करना") +
          p("तीनों भुजाएँ " + m("a") + " हैं, इसलिए " + m("(s-a)") + " तीनों गुणनखंडों में एक ही होगा:") +
          lines(f"{S_}-{A_}", f"{C(PUR, '\\dfrac{3a}{2}')}-{A_}", "\\dfrac{3a}{2}-\\dfrac{2a}{2}", f"\\dfrac{{3a-2a}}{{2}}", C(RED, "\\dfrac{a}{2}")) +
          p("हीरोन के सूत्र में मान रखने पर (बोर्ड का क्षेत्रफल):") +
          lines("\\text{क्षेत्रफल}",
                f"\\sqrt{{{S_}({S_}-{A_})({S_}-{A_})({S_}-{A_})}}",
                f"\\sqrt{{{C(PUR, '\\dfrac{3a}{2}')}\\times {C(RED, '\\dfrac{a}{2}')}\\times {C(RED, '\\dfrac{a}{2}')}\\times {C(RED, '\\dfrac{a}{2}')}}}",
                "\\sqrt{\\dfrac{3\\times a\\times a\\times a\\times a}{2\\times 2\\times 2\\times 2}}",
                "\\sqrt{\\dfrac{3\\times (a\\times a)\\times (a\\times a)}{(2\\times 2)\\times (2\\times 2)}}",
                "\\dfrac{a\\times a}{2\\times 2}\\sqrt{3}",
                "\\dfrac{a^2}{4}\\sqrt{3}",
                "\\dfrac{\\sqrt{3}}{4}a^2") +
          p("(" + m("a") + " cm में हो, तो क्षेत्रफल " + m("\\text{cm}^2") + " में होगा।)"))
b1 = kh("भुजा " + m("a") + " ज्ञात करना") + formula("समबाहु त्रिभुज का परिमाप", m("a + a + a = 3a") + " (तीनों भुजाएँ बराबर)")
b1 += eqs(("3" + A_, "180"), (A_, "\\dfrac{180}{3}"), (A_, C(RED, "60") + "\\ \\text{cm}"))
assert 180 % 3 == 0 and 180 // 3 == 60
st, sv = s_steps((60, 60, 60), "cm", (RED, RED, RED), "aaa")
ab, o1, i1 = area_block((60, 60, 60), sv, "cm", what="बोर्ड का क्षेत्रफल", cols=(RED, RED, RED), names="aaa")
assert (sv, o1, i1) == (90, 900, 3)
b1 += st + ab
b1 += kh("जाँच ((i) के सूत्र से)") + lines("\\dfrac{\\sqrt{3}}{4}a^2", "\\dfrac{\\sqrt{3}}{4}\\times 60^2", "\\dfrac{\\sqrt{3}}{4}\\times 3600",
                                          "\\sqrt{3}\\times 900", "900\\sqrt{3}\\ \\text{cm}^2")
close(math.sqrt(3) / 4 * 3600, 900 * math.sqrt(3))
b1 += ok("दोनों विधियों से एक ही उत्तर ✔")
s += part("(ii) परिमाप 180 cm होने पर क्षेत्रफल", b1)
assert abs(900 * 1.732 - 1558.8) < 1e-9
s += ans("(i) बोर्ड का क्षेत्रफल " + m("= \\dfrac{\\sqrt{3}}{4}a^2") + " (ii) परिमाप 180 cm होने पर क्षेत्रफल " + m("= 900\\sqrt{3}\\ \\text{cm}^2") +
         " (" + m("\\sqrt{3} = 1.732") + " लेने पर लगभग " + m("1558.8\\ \\text{cm}^2") + ")")
ANS[1] = "a²√3/4; 900√3 cm² ≈ 1558.8 cm²"
E1.append(("एक यातायात संकेत बोर्ड पर ‘आगे स्कूल है’ लिखा है और यह भुजा ‘" + m("a") + "’ वाले एक समबाहु त्रिभुज के आकार का है। हीरोन के सूत्र का प्रयोग करके इस बोर्ड का क्षेत्रफल ज्ञात कीजिए। यदि संकेत बोर्ड का परिमाप 180 cm है, तो इसका क्षेत्रफल क्या होगा?", s))

# ---------- Q2 ----------
V2 = (122, 22, 120)
assert 120 ** 2 + 22 ** 2 == 122 ** 2
s = given("त्रिभुजाकार दीवार की भुजाएँ: " + m(f"{C(RED, 'a')} = 122\\ \\text{{m}},\\ {C(BLU, 'b')} = 22\\ \\text{{m}},\\ {C(GRN, 'c')} = 120\\ \\text{{m}}") +
          "<br>किराया: ₹5000 प्रति " + m("\\text{m}^2") + " प्रति वर्ष; दीवार 3 महीने के लिए किराए पर",
          "कंपनी द्वारा दिया गया कुल किराया")
s += pair(fig10_6("आकृति 10.6"),
          tri_fig(V2, True, "हल की आकृति: दीवार △ABC (पैमाने पर); a = BC लाल, b = CA नीली, c = AB हरी", base="c", mirror=True,
                  W=360, H=150, unit="m", right="A", mx=74))
s += key((RED, "a = 122 m, s − a"), (BLU, "b = 22 m, s − b"), (GRN, "c = 120 m, s − c"), (PUR, "s"))
s += heron_formula()
st, sv = s_steps(V2, "m")
ab, o2, i2 = area_block(V2, sv, "m", what="दीवार का क्षेत्रफल")
assert (sv, o2, i2) == (132, 1320, 1)
s += st + ab
s += kh("जाँच") + p("दो छोटी भुजाओं के वर्गों का योग:") + lines("120^2+22^2", "14400+484", "14884", "122^2")
s += p("अतः पाइथागोरस प्रमेय के विलोम से दीवार एक समकोण त्रिभुज है (समकोण A पर, आधार 120 m, ऊँचाई 22 m)।")
s += lines("\\text{क्षेत्रफल}", "\\dfrac{1}{2}\\times \\text{आधार}\\times \\text{ऊँचाई}", "\\dfrac{1}{2}\\times 120\\times 22", "60\\times 22", "1320\\ \\text{m}^2")
s += ok("हीरोन के सूत्र से प्राप्त क्षेत्रफल सही है ✔")
s += kh("3 महीने का किराया")
s += p("1 वर्ष = 12 महीने। 1 " + m("\\text{m}^2") + " का 12 महीने का किराया ₹5000 है।")
s += lines("\\text{1 }\\mathrm{m}^2\\text{ का 1 महीने का किराया}", "\\dfrac{5000}{12}\\text{ रुपये}")
s += lines("\\text{1 }\\mathrm{m}^2\\text{ का 3 महीने का किराया}", "\\dfrac{5000}{12}\\times 3\\text{ रुपये}", "\\dfrac{15000}{12}\\text{ रुपये}", "1250\\text{ रुपये}")
assert 5000 * 3 % 12 == 0 and 5000 * 3 // 12 == 1250
s += lines("\\text{1320 }\\mathrm{m}^2\\text{ का 3 महीने का किराया}", "1320\\times 1250\\text{ रुपये}", "1650000\\text{ रुपये}")
assert 1320 * 1250 == 1650000
s += ans("कंपनी ने 3 महीने का कुल किराया <b>₹16,50,000</b> दिया। (दीवार का क्षेत्रफल " + m("1320\\ \\text{m}^2") + ")")
ANS[2] = "area 1320 m², rent ₹16,50,000"
E1.append(("किसी फ्लाईओवर (flyover) की त्रिभुजाकार दीवार को विज्ञापनों के लिए प्रयोग किया जाता है। दीवार की भुजाओं की लंबाइयाँ 122 m, 22 m और 120 m हैं (देखिए आकृति 10.6)। इस विज्ञापन से प्रति वर्ष ₹5000 प्रति " + m("\\text{m}^2") + " की प्राप्ति होती है। एक कम्पनी ने एक दीवार को विज्ञापन देने के लिए 3 महीने के लिए किराए पर लिया। उसने कुल कितना किराया दिया?", s))

# ---------- Q3 ----------
V3 = (15, 11, 6)
s = given("पेंट की गई त्रिभुजाकार दीवार की विमाएँ: " + m(f"{C(RED, 'a')} = 15\\ \\text{{m}},\\ {C(BLU, 'b')} = 11\\ \\text{{m}},\\ {C(GRN, 'c')} = 6\\ \\text{{m}}"),
          "रंग से पेंट हुए भाग (त्रिभुजाकार दीवार) का क्षेत्रफल")
s += pair(fig10_7("आकृति 10.7"),
          tri_fig(V3, True, "हल की आकृति: दीवार △ABC (पैमाने पर); a = BC लाल, b = CA नीली, c = AB हरी", base="a", mirror=True,
                  W=360, H=160, unit="m"))
s += key((RED, "a = 15 m, s − a"), (BLU, "b = 11 m, s − b"), (GRN, "c = 6 m, s − c"), (PUR, "s"))
s += heron_formula()
st, sv = s_steps(V3, "m")
ab, o3, i3 = area_block(V3, sv, "m", what="पेंट हुए भाग का क्षेत्रफल")
assert (sv, o3, i3) == (16, 20, 2)
s += st + ab
s += ans("रंग से पेंट हुए भाग का क्षेत्रफल " + m("= 20\\sqrt{2}\\ \\text{m}^2") + " (" + m("\\sqrt{2} = 1.414") + " लेने पर लगभग " + m("28.28\\ \\text{m}^2") + ")")
assert abs(20 * 1.414 - 28.28) < 1e-9
ANS[3] = "20√2 m² ≈ 28.28 m²"
E1.append(("किसी पार्क में एक फिसल पट्टी (slide) बनी हुई है। इसकी पार्श्वीय दीवारों (side walls) में से एक दीवार पर किसी रंग से पेंट किया गया है और उस पर “पार्क को हरा-भरा और साफ रखिए” लिखा हुआ है (देखिए आकृति 10.7)। यदि इस दीवार की विमाएँ 15 m, 11 m और 6 m हैं, तो रंग से पेंट हुए भाग का क्षेत्रफल ज्ञात कीजिए।", s))

# ---------- Q4 ----------
V4 = (18, 10, 14)
s = given("त्रिभुज की दो भुजाएँ " + m(f"{C(RED, 'a')} = 18\\ \\text{{cm}},\\ {C(BLU, 'b')} = 10\\ \\text{{cm}}") + "<br>परिमाप = 42 cm",
          "त्रिभुज का क्षेत्रफल")
s += NOFIG + solo(tri_fig(V4, True, "हल की आकृति: △ABC (पैमाने पर); a = BC लाल, b = CA नीली, तीसरी भुजा c = AB हरी", W=330, H=210))
s += key((RED, "a = 18 cm, s − a"), (BLU, "b = 10 cm, s − b"), (GRN, "c (तीसरी भुजा), s − c"), (PUR, "s"))
s += kh("तीसरी भुजा " + m(C(GRN, "c")) + " ज्ञात करना")
s += formula("त्रिभुज का परिमाप", "परिमाप " + m("= a + b + c"))
s += eqs((f"{C(RED, '18')}+{C(BLU, '10')}+{C(GRN, 'c')}", "42"), (f"28+{C(GRN, 'c')}", "42"), (C(GRN, "c"), "42-28"), (C(GRN, "c"), C(GRN, "14") + "\\ \\text{cm}"))
assert 42 - 18 - 10 == 14
s += heron_formula()
st, sv = s_steps(V4, "cm")
ab, o4, i4 = area_block(V4, sv, "cm")
assert (sv, o4, i4) == (21, 21, 11)
s += st + ab
s += ans("त्रिभुज का क्षेत्रफल " + m("= 21\\sqrt{11}\\ \\text{cm}^2") + " (" + m("\\sqrt{11} = 3.317") + " लेने पर लगभग " + m("69.66\\ \\text{cm}^2") + ")")
assert abs(round(21 * 3.317, 2) - 69.66) < 1e-9
ANS[4] = "third side 14 cm; 21√11 cm² ≈ 69.66 cm²"
E1.append(("उस त्रिभुज का क्षेत्रफल ज्ञात कीजिए जिसकी दो भुजाएँ 18 cm और 10 cm हैं तथा उसका परिमाप 42 cm है।", s))

# ---------- Q5 ----------
V5 = (120, 170, 250)
s = given("त्रिभुज की भुजाओं का अनुपात = 12 : 17 : 25<br>परिमाप = 540 cm", "भुजाएँ और त्रिभुज का क्षेत्रफल")
s += NOFIG + solo(tri_fig(V5, True, "हल की आकृति: △ABC (पैमाने पर); a = BC लाल, b = CA नीली, c = AB हरी", base="c", W=360, H=170))
s += key((RED, "a = 12x, s − a"), (BLU, "b = 17x, s − b"), (GRN, "c = 25x, s − c"), (PUR, "s"))
s += kh("भुजाएँ ज्ञात करना")
s += p("माना भुजाएँ " + m(f"{C(RED, '12x')},\\ {C(BLU, '17x')}") + " और " + m(C(GRN, "25x")) + " cm हैं।")
s += formula("त्रिभुज का परिमाप", "परिमाप " + m("= a + b + c"))
s += eqs((f"{C(RED, '12x')}+{C(BLU, '17x')}+{C(GRN, '25x')}", "540"), ("54x", "540"), ("x", "\\dfrac{540}{54}"), ("x", "10"))
assert 12 + 17 + 25 == 54 and 540 / 54 == 10
s += lines(C(RED, "a"), C(RED, "12x"), "12\\times 10", C(RED, "120") + "\\ \\text{cm}")
s += lines(C(BLU, "b"), C(BLU, "17x"), "17\\times 10", C(BLU, "170") + "\\ \\text{cm}")
s += lines(C(GRN, "c"), C(GRN, "25x"), "25\\times 10", C(GRN, "250") + "\\ \\text{cm}")
s += heron_formula()
st, sv = s_steps(V5, "cm")
ab, o5, i5 = area_block(V5, sv, "cm")
assert (sv, o5, i5) == (270, 9000, 1)
s += st + ab
s += ans("त्रिभुज की भुजाएँ 120 cm, 170 cm और 250 cm हैं तथा इसका क्षेत्रफल " + m("= 9000\\ \\text{cm}^2") + " है।")
ANS[5] = "sides 120, 170, 250 cm; 9000 cm²"
E1.append(("एक त्रिभुज की भुजाओं का अनुपात 12 : 17 : 25 है और उसका परिमाप 540 cm है। इस त्रिभुज का क्षेत्रफल ज्ञात कीजिए।", s))

# ---------- Q6 ----------
V6 = (12, 12, 6)
s = given("समद्विबाहु त्रिभुज: बराबर भुजाएँ " + m(f"{C(RED, 'a')} = {C(BLU, 'b')} = 12\\ \\text{{cm}}") + "<br>परिमाप = 30 cm",
          "त्रिभुज का क्षेत्रफल")
s += NOFIG + solo(tri_fig(V6, True, "हल की आकृति: समद्विबाहु △ABC (पैमाने पर); बराबर भुजाएँ a = BC लाल, b = CA नीली, आधार c = AB हरा",
                          base="c", W=300, H=260, ticks={"a": 1, "b": 1}))
s += key((RED, "a = 12 cm, s − a"), (BLU, "b = 12 cm, s − b"), (GRN, "c (आधार), s − c"), (PUR, "s"))
s += kh("तीसरी भुजा (आधार) " + m(C(GRN, "c")) + " ज्ञात करना")
s += formula("त्रिभुज का परिमाप", "परिमाप " + m("= a + b + c"))
s += eqs((f"{C(RED, '12')}+{C(BLU, '12')}+{C(GRN, 'c')}", "30"), (f"24+{C(GRN, 'c')}", "30"), (C(GRN, "c"), "30-24"), (C(GRN, "c"), C(GRN, "6") + "\\ \\text{cm}"))
assert 30 - 24 == 6
s += heron_formula()
st, sv = s_steps(V6, "cm")
ab, o6, i6 = area_block(V6, sv, "cm")
assert (sv, o6, i6) == (15, 9, 15)
s += st + ab
s += ans("त्रिभुज का क्षेत्रफल " + m("= 9\\sqrt{15}\\ \\text{cm}^2") + " (" + m("\\sqrt{15} = 3.873") + " लेने पर लगभग " + m("34.86\\ \\text{cm}^2") + ")")
assert abs(round(9 * 3.873, 2) - 34.86) < 1e-9
ANS[6] = "base 6 cm; 9√15 cm² ≈ 34.86 cm²"
E1.append(("एक समद्विबाहु त्रिभुज का परिमाप 30 cm है और उसकी बराबर भुजाएँ 12 cm लम्बाई की हैं। इस त्रिभुज का क्षेत्रफल ज्ञात कीजिए।", s))

# ---------------------------------------------------------------------
assert len(E1) == 6
E1 = [(qt(a), b) for a, b in E1]
check_tex(E1)
SUB = "कक्षा 9 गणित · अध्याय 10: " + CH + " · {} प्रश्न"
page(BASE, 10, CH, "exercise-10-1", "प्रश्नावली 10.1", SUB.format(len(E1)), E1,
     ("/hi/class-09/maths/chapter-09/exercise-9-3/", "प्रश्नावली 9.3"), ("/hi/class-09/maths/chapter-11/exercise-11-1/", "प्रश्नावली 11.1"), css=CSS + EXTRA_CSS, boards=BOARDS10)
for k_, v_ in ANS.items():
    print(k_, v_)
print("ok")
