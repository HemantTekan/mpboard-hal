#!/usr/bin/env python3
"""Class 9 Maths, Chapter 9 (वृत्त): Exercises 9.1, 9.2 and 9.3, Hindi medium.
Rationalised book (2023-24 onward; NCERT iemh109 'Rationalised 2022-23', print 2024-25) = old chapter 10 (वृत्त):
  old 10.1 (terms, fill-ups), old 10.3 (circle through three points) and old 10.6 (optional) removed;
  9.1 = old 10.2 (2 Q), 9.2 = old 10.4 (6 Q), 9.3 = old 10.5 (12 Q) -- question numbers unchanged.
  Figures renumbered like the current book: old 10.25 -> 9.12; old 10.36, 10.37, 10.38, 10.39, 10.40 -> 9.23 ... 9.27.
  Theorems: old 10.5 (unique circle through three points) removed, so old 10.1-10.4 = 9.1-9.4 and
  old 10.6-10.12 = 9.5-9.11 (9.7 angle at centre = 2 x angle at circle, 9.8 same segment, 9.10/9.11 cyclic quadrilateral).
Question text and figures copied from NCERT Hindi PDF ihmh110 (archive.org ncert-ihmh1, chapter 10 of the 2020-21 print).
Style as chapters 6-8: every side/angle/arc has one colour in the solution figure and the same colour in the working;
equal chords/radii carry matching coloured ticks, equal angles matching arcs, right angles squares.
Every circle is a true circle; every point on it is computed from the centre, radius and angle.
Run from repo root: python3 tools/solutions/class9_ch9.py
"""
import sys, pathlib, math
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from common import *  # noqa
from mixed_cells import *  # noqa

BASE = "/hi/class-09/maths/chapter-09/"
CH = "वृत्त"
BOARDS9 = ("यह हल <b>MP Board (MPBSE)</b> कक्षा 9 गणित की पाठ्यपुस्तक के अध्याय 9 ‘वृत्त’ के अनुसार है।")
EXTRA_CSS = """
.fig{margin:10px 0;text-align:center}.fig svg{width:100%;height:auto;background:#fbfcff;border:1px solid #e3e8f4;border-radius:12px}
.fig .cap{font-size:.85em;color:#5a6275;margin-top:4px}
.figs{display:grid;grid-template-columns:1fr 1fr;gap:10px}.figs .fig{margin:6px 0}
@media (max-width:640px){.figs{grid-template-columns:1fr}}
.tp{background:#fff4ec;border-left:4px solid #e8711a;border-radius:8px;padding:5px 10px;margin:6px 0;font-size:.95em}
.ax{background:#f4ecff;border-left:4px solid #8a3ffc;border-radius:8px;padding:7px 12px;margin:10px 0 6px;font-size:.96em}
.ax b{color:#5b21b6}
.eq.kk{width:auto;grid-template-columns:max-content max-content minmax(0,1fr)}
.kk .rs{grid-column:1/-1;font-size:.86em;color:#5a6275;margin:-2px 0 6px;text-align:left;white-space:normal}
.kk .rs:last-child{margin-bottom:0}
.kh{font-weight:700;color:#1d3a8a;margin:12px 0 2px}
.ans .al{margin:10px 0}
.key{display:flex;flex-wrap:wrap;gap:6px 14px;font-size:.9em;margin:4px 0 8px}
.key span{display:inline-flex;align-items:center;gap:5px}.key i{display:inline-block;width:14px;height:14px;border-radius:4px}
.pfw{overflow-x:auto;margin:4px 0 8px}
table.pft{width:100%;border-collapse:separate;border-spacing:0;background:#f7f8fc;border-radius:10px;overflow:hidden}
.pft th{background:#e6ecfa;color:#1d3a8a;font-size:.84em;padding:5px 8px;text-align:left}
.pft td{padding:7px 8px;border-top:1px solid #e3e8f4;vertical-align:middle}
.pft td.st{white-space:nowrap}.pft td.rs{font-size:.86em;color:#4d5568}
.pft td.tg{width:1%;padding-right:2px}
.pft tr.cc td{background:#e9f8ef;font-weight:600}
.tgb{display:inline-block;color:#fff;font-size:.72em;border-radius:6px;padding:1px 6px;font-weight:700;white-space:nowrap}
.corr{background:#eef4ff;border:1px dashed #8db7ef;border-radius:8px;padding:5px 10px;margin:2px 0 10px;font-size:.93em}
.nofig{font-size:.85em;color:#5a6275;margin:2px 0 6px}
"""

# ---------------- colours (same in figures and in the working) ----------------
INK, GRID = "#1d3a8a", "#94a3b8"
DISP = {"Z": "O′"}   # point keys must be one letter; Z is drawn as O′
CIR = "#0b7bc4"   # circle outline (book figures are drawn in this blue)
RED, BLU, GRN, ORG, PUR, TEA = "#d62839", "#1769c2", "#0f8a4c", "#e06a00", "#7c3aed", "#0e8a9a"
BROWN = "#9a5b13"
FONT = "font-family=\"Noto Sans, 'Noto Sans Devanagari', sans-serif\""


def C(col, t):
    return "\\textcolor{" + col + "}{" + t + "}"


def ang(name, col=None):
    t = "\\angle " + name
    return C(col, t) if col else t


def sd(name, col=None):
    return C(col, name) if col else name


def tri(name, col=None):
    t = "\\triangle " + name
    return C(col, t) if col else t


DEG = "^\\circ"


def dg(v, col=None):
    t = f"{v}^\\circ"
    return C(col, t) if col else t


def ax(title, text):
    return f"<div class='ax'><b>{title}:</b> {text}</div>"


def kh(t):
    return f"<div class='kh'>{t}</div>"


def tp(t):
    return f"<div class='tp'>{t}</div>"


def chain(*rows, small=False):
    """Statement rows aligned at the relation sign; each row may carry its reason (कारण) below it."""
    out = ""
    for r_ in rows:
        lhs, rhs, why_ = r_[:3]
        sym = r_[3] if len(r_) > 3 else "="
        out += (f"<span class='l'>{mc(lhs) if lhs else ''}</span><span class='s'>{m(sym) if sym else ''}</span>"
                f"<span class='r'>{mc(rhs)}</span>")
        if why_:
            out += f"<span class='rs'>({why_})</span>"
    return "<div class='eq kk'" + (" style='font-size:.9em'" if small else "") + ">" + out + "</div>"


def stmt(t, why_=None):
    w = f"<div style='font-size:.86em;color:#5a6275'>({why_})</div>" if why_ else ""
    return f"<div class='eq' style='display:block'>{m(t)}{w}</div>"


def key(*items):
    return "<div class='key'>" + "".join(f"<span><i style='background:{c}'></i>{t}</span>" for c, t in items) + "</div>"


TAGS = {"S": "भुजा", "A": "कोण", "R": "समकोण", "H": "कर्ण"}


def kk(head, rows, concl=None, corr=None):
    """उपपत्ति table: कथन | कारण.  rows: (tex, reason) or (tex, reason, tag, colour).
    tag S/A/R/H marks which part of the congruence rule the row gives (badge in the pair's colour)."""
    tagged = any(len(r_) > 2 and r_[2] for r_ in rows)
    th = ("<th></th>" if tagged else "") + "<th>कथन</th><th>कारण</th>"
    body = ""
    for r_ in rows:
        tex, why_ = r_[0], r_[1]
        tg = ""
        if tagged:
            if len(r_) > 2 and r_[2]:
                tg = f"<span class='tgb' style='background:{r_[3]}'>{TAGS[r_[2]]}</span>"
            tg = f"<td class='tg'>{tg}</td>"
        body += f"<tr>{tg}<td class='st'>{m(tex)}</td><td class='rs'>{why_}</td></tr>"
    if concl:
        sp = "<td class='tg'></td>" if tagged else ""
        body += f"<tr class='cc'>{sp}<td class='st'>{m(concl[0])}</td><td class='rs'>{concl[1]}</td></tr>"
    h = f"<div class='kh'>{head}</div>" if head else ""
    out = h + f"<div class='pfw'><table class='pft'><tr>{th}</tr>{body}</table></div>"
    if corr:
        out += "<div class='corr'><b>संगत शीर्ष:</b> " + ", ".join(m(a + " \\leftrightarrow " + b) for a, b in corr) + "</div>"
    return out


def num(i, a):
    return a.replace("<b>", f"<b>({i}) ", 1)


def check_tex(E):
    import re as _re
    for _q, _sol in E:
        for _t in _re.findall(r"\\\((.+?)\\\)", _q + _sol):
            assert not _re.search(r"[\u0900-\u097F]", _t), ("Devanagari in TeX", _t)


# ---------------- theorems as stated in the book ----------------
SAS = ax("अभिगृहीत 7.1 (SAS सर्वांगसमता नियम)", "दो त्रिभुज सर्वांगसम होते हैं, यदि एक त्रिभुज की दो भुजाएँ और उनका अंतर्गत कोण दूसरे त्रिभुज की दो भुजाओं और उनके अंतर्गत कोण के बराबर हों।")
ASA = ax("प्रमेय 7.1 (ASA सर्वांगसमता नियम)", "दो त्रिभुज सर्वांगसम होते हैं, यदि एक त्रिभुज के दो कोण और उनकी अंतर्गत भुजा दूसरे त्रिभुज के दो कोणों और उनकी अंतर्गत भुजा के बराबर हों।")
AAS = ax("AAS सर्वांगसमता नियम", "दो त्रिभुज सर्वांगसम होते हैं, यदि इन त्रिभुजों के दो कोणों के युग्म बराबर हों और संगत भुजाओं का एक युग्म बराबर हो।")
TH72 = ax("प्रमेय 7.2", "एक समद्विबाहु त्रिभुज की बराबर भुजाओं के सम्मुख कोण बराबर होते हैं।")
TH73 = ax("प्रमेय 7.3", "किसी त्रिभुज के बराबर कोणों की सम्मुख भुजाएँ बराबर होती हैं।")
SSS = ax("प्रमेय 7.4 (SSS सर्वांगसमता नियम)", "यदि एक त्रिभुज की तीनों भुजाएँ एक अन्य त्रिभुज की तीनों भुजाओं के बराबर हों, तो दोनों त्रिभुज सर्वांगसम होते हैं।")
RHS = ax("प्रमेय 7.5 (RHS सर्वांगसमता नियम)", "यदि दो समकोण त्रिभुजों में, एक त्रिभुज का कर्ण और एक भुजा क्रमशः दूसरे त्रिभुज के कर्ण और एक भुजा के बराबर हों, तो दोनों त्रिभुज सर्वांगसम होते हैं।")
CPCT = ax("CPCT (सर्वांगसम त्रिभुजों के संगत भाग)", "दो त्रिभुज सर्वांगसम हों, तो उनके संगत भाग (संगत भुजाएँ और संगत कोण) बराबर होते हैं।")
VOPP = ax("प्रमेय 6.1 (शीर्षाभिमुख कोण)", "यदि दो रेखाएँ परस्पर प्रतिच्छेद करती हैं, तो शीर्षाभिमुख कोण बराबर होते हैं।")
LINEAR = ax("रैखिक युग्म अभिगृहीत (अभिगृहीत 6.1)", "यदि एक किरण एक रेखा पर खड़ी हो, तो इस प्रकार बने दोनों आसन्न कोणों का योग " + m("180^\\circ") + " होता है।")
ALT = ax("एकांतर अंतः कोण", "यदि एक तिर्यक रेखा दो समांतर रेखाओं को प्रतिच्छेद करे, तो एकांतर अंतः कोणों का प्रत्येक युग्म बराबर होता है।")
ALT_C = ax("एकांतर अंतः कोणों का विलोम", "यदि एक तिर्यक रेखा दो रेखाओं को इस प्रकार प्रतिच्छेद करे कि एकांतर अंतः कोणों का एक युग्म बराबर है, तो दोनों रेखाएँ परस्पर समांतर होती हैं।")
INT = ax("तिर्यक रेखा के एक ही ओर के अंतः कोण", "यदि एक तिर्यक रेखा दो समांतर रेखाओं को प्रतिच्छेद करे, तो तिर्यक रेखा के एक ही ओर के अंतः कोणों का प्रत्येक युग्म संपूरक होता है (योग " + m("180^\\circ") + ")।")
ASUM = ax("त्रिभुज के कोणों का योग गुण", "त्रिभुज के तीनों कोणों का योग " + m("180^\\circ") + " होता है।")
EQ_HALF = ax("बराबरों के आधे", "बराबर राशियों के आधे भी बराबर होते हैं।")
EQ_ADD = ax("यूक्लिड की अभिधारणा", "यदि बराबरों को बराबरों में जोड़ा जाए, तो पूर्ण भी बराबर होते हैं।")


# ---------------- SVG figure kit ----------------
class Fig:
    n = 0

    def __init__(self, W, H):
        Fig.n += 1
        self.id, self.W, self.H, self.bg, self.el, self.top, self.marks = f"f9{Fig.n}", W, H, [], [], [], {}

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


def pair(a, b):
    return f"<div class='figs'>{a}{b}</div>"


def geo(W, H, P, segs, labels, marks, cap, fills=(), extra=None, sol=True, circ=()):
    """Generic figure.  P: name -> (x, y).  segs: 'AB' or ('AB', colour, width, dash).
    marks: ('t','AB',n,col) ticks · ('p','AB',n,col) parallel arrow-heads · ('q','AB',col) square mark · ('a','BAC',n,col,r) angle arcs at the middle letter ·
           ('r','ADB',col) right-angle box at D · ('l','BAC',text,col,r) angle label.
    In the textbook version (sol=False) every mark is drawn in INK and no fills/colours are used."""
    f = Fig(W, H)
    for nm in labels:
        x_, y_ = P[nm]
        assert 14 < x_ < W - 14 and 14 < y_ < H - 14, ("point near/outside canvas", cap, nm, P[nm])
    if sol:
        for pts, col in fills:
            f.poly([P[x] for x in pts], col)
    for c_ in circ:    # (centre name, radius[, colour, width, dash]) -- a true circle
        o_, rr = P[c_[0]], c_[1]
        assert 4 < o_[0] - rr and o_[0] + rr < W - 4 and 4 < o_[1] - rr and o_[1] + rr < H - 4, ("circle outside canvas", cap, c_)
        col = c_[2] if (sol and len(c_) > 2 and c_[2]) else CIR
        w = c_[3] if len(c_) > 3 and c_[3] else 2.2
        d_ = f" stroke-dasharray='{c_[4]}'" if len(c_) > 4 and c_[4] else ""
        f.el.insert(0, f"<circle cx='{o_[0]:.1f}' cy='{o_[1]:.1f}' r='{rr:.1f}' fill='none' stroke='{col}' stroke-width='{w}'{d_}/>")
    if extra:
        extra(f, sol)
    for s_ in segs:
        if isinstance(s_, str):
            s_ = (s_,)
        nm = s_[0]
        col = s_[1] if (sol and len(s_) > 1 and s_[1]) else INK
        w = s_[2] if (sol and len(s_) > 2 and s_[2]) else 2.2
        dash = s_[3] if len(s_) > 3 else None
        f.line(P[nm[0]], P[nm[1]], col, w, dash=dash)
    for mk in marks:
        k = mk[0]
        if k == "t":
            f.ticks(P[mk[1][0]], P[mk[1][1]], mk[2], mk[3] if sol else INK, *(mk[4:] or ()))
        elif k == "p":    # parallel arrow-heads
            f.par(P[mk[1][0]], P[mk[1][1]], mk[2], mk[3] if sol else INK, *(mk[4:] or ()))
        elif k == "q":
            f.sqm(P[mk[1][0]], P[mk[1][1]], mk[2] if sol else INK)
        elif k == "a":
            a, v, b = mk[1]
            r = mk[4] if len(mk) > 4 else 22
            f.arcp(P[v], P[a], P[b], r, mk[3] if sol else INK, mk[2], fill=sol, trim=4)
        elif k == "ad":    # dashed outline arc (no fill), for a sum angle
            a, v, b = mk[1]
            f.arcp(P[v], P[a], P[b], mk[3], mk[2], fill=False, dash="5 4", w=1.8)
        elif k == "r":
            a, v, b = mk[1]
            f.rightp(P[v], P[a], P[b], 11, mk[2] if sol else INK)
        elif k == "l" and sol:
            a, v, b = mk[1]
            f.alabp(P[v], P[a], P[b], mk[4], mk[2], mk[3], mk[5] if len(mk) > 5 else 12)
    for nm, (deg, d) in labels.items():
        f.dot(P[nm])
        f.lab(P[nm], DISP.get(nm, nm), deg, d)
    return f.svg(cap)


def figs(fn, book_cap, sol_cap):
    return pair(fn(False, book_cap), fn(True, "हल की आकृति: " + sol_cap))


def foot(p, a, b):
    ax_, ay = b[0] - a[0], b[1] - a[1]
    t = ((p[0] - a[0]) * ax_ + (p[1] - a[1]) * ay) / (ax_ * ax_ + ay * ay)
    return (a[0] + t * ax_, a[1] + t * ay)


def inter(p1, p2, p3, p4):
    x1, y1 = p1; x2, y2 = p2; x3, y3 = p3; x4, y4 = p4
    den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
    return (x1 + t * (x2 - x1), y1 + t * (y2 - y1))


def mid(a, b):
    return ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)


def dist(a, b):
    return math.dist(a, b)


def angle_at(v, a, b):
    d = abs(Fig.dir(v, a) - Fig.dir(v, b)) % 360
    return min(d, 360 - d)


def close1(a, b, tol=0.5):
    assert abs(a - b) < tol, (a, b)


# ---------------- more theorems as stated in the book ----------------
CORR = ax("संगत कोण अभिगृहीत", "यदि एक तिर्यक रेखा दो समांतर रेखाओं को प्रतिच्छेद करे, तो संगत कोणों का प्रत्येक युग्म बराबर होता है।")
TH82 = ax("प्रमेय 8.2", "एक समांतर चतुर्भुज में सम्मुख भुजाएँ बराबर होती हैं।")
TH84 = ax("प्रमेय 8.4", "एक समांतर चतुर्भुज में सम्मुख कोण बराबर होते हैं।")
D_RECT = ax("आयत", "आयत वह समांतर चतुर्भुज है जिसका एक कोण समकोण हो।")
NOFIG = "<div class='nofig'>(पुस्तक में इस प्रश्न की आकृति नहीं दी है; नीचे हल के लिए आकृति बनाई गई है।)</div>"
HALF = "\\dfrac{1}{2}"


def solo(f):
    return f"<div style='max-width:430px;margin:0 auto'>{f}</div>"


def par_(a, b, c, d, tol=1e-6):
    """assert segment ab is parallel to cd (cross product 0)"""
    v1, v2 = (b[0] - a[0], b[1] - a[1]), (d[0] - c[0], d[1] - c[1])
    assert abs(v1[0] * v2[1] - v1[1] * v2[0]) < tol * (math.hypot(*v1) * math.hypot(*v2)), (a, b, c, d)


def perp_(a, b, c, d, tol=1e-6):
    v1, v2 = (b[0] - a[0], b[1] - a[1]), (d[0] - c[0], d[1] - c[1])
    assert abs(v1[0] * v2[0] + v1[1] * v2[1]) < tol * (math.hypot(*v1) * math.hypot(*v2)), (a, b, c, d)


def on_seg(p, a, b):
    t = ((p[0] - a[0]) * (b[0] - a[0]) + (p[1] - a[1]) * (b[1] - a[1])) / dist(a, b) ** 2
    assert 0.02 < t < 0.98, (p, a, b, t)
    close1(dist(a, p) + dist(p, b), dist(a, b), 1e-6)


def pgram(P, a, b, c, d):
    par_(P[a], P[b], P[d], P[c])
    par_(P[a], P[d], P[b], P[c])


def ray(f, sol, a, b, ext, col=None):
    """ray from a through b, extended ext px beyond b, with an arrow-head"""
    d = Fig.dir(a, b)
    f.line(a, Fig.pol(b, d, ext), (col or "#64748b") if sol else INK, 2, False, True)



# ---------------- circle helpers ----------------
def on(O, R, deg):
    """point on the circle (centre O, radius R) at angle deg (maths convention, anticlockwise from +x)"""
    return Fig.pol(O, deg, R)


def oncirc(P, o, R, names, tol=1e-6):
    for n_ in names:
        close1(dist(P[o], P[n_]), R, tol)


def rl(P, o, names, d=16, extra=None):
    """labels pushed radially outwards from centre o"""
    out = {n_: (Fig.dir(P[o], P[n_]), d) for n_ in names}
    out.update(extra or {})
    return out


def carc(f, o, d1, d2, R, col, w=4.6):
    """thick coloured arc ON the circle from angle d1 anticlockwise to d2"""
    f.arc(o, d1, d2, R, col, fill=False, n=1, w=w)


def bl(f, P, abc, t, r, col=INK, size=12):
    """angle label at the middle letter of abc"""
    a, v, b = abc
    f.alabp(P[v], P[a], P[b], r, t, col, size)


def line_circ(p, d, o, R):
    """the two points where the line through p with direction angle d meets circle (o, R): (behind, ahead)"""
    ux, uy = math.cos(math.radians(d)), -math.sin(math.radians(d))
    fx, fy = p[0] - o[0], p[1] - o[1]
    b = fx * ux + fy * uy
    c = fx * fx + fy * fy - R * R
    disc = math.sqrt(b * b - c)
    t1, t2 = -b - disc, -b + disc
    return (p[0] + t1 * ux, p[1] + t1 * uy), (p[0] + t2 * ux, p[1] + t2 * uy)


def second(p, q, o, R):
    """second intersection (other than p, which is on the circle) of line pq with circle (o, R)"""
    a, b = line_circ(p, Fig.dir(p, q), o, R)
    return a if dist(a, p) > dist(b, p) else b


def circ2(o1, r1, o2, r2):
    """intersection points of two circles: (upper, lower) on screen"""
    d = dist(o1, o2)
    a = (r1 * r1 - r2 * r2 + d * d) / (2 * d)
    h = math.sqrt(r1 * r1 - a * a)
    mx, my = o1[0] + a * (o2[0] - o1[0]) / d, o1[1] + a * (o2[1] - o1[1]) / d
    p1 = (mx + h * (o2[1] - o1[1]) / d, my - h * (o2[0] - o1[0]) / d)
    p2 = (mx - h * (o2[1] - o1[1]) / d, my + h * (o2[0] - o1[0]) / d)
    return (p1, p2) if p1[1] < p2[1] else (p2, p1)


def circum(a, b, c):
    ax_, ay = a; bx, by = b; cx, cy = c
    d = 2 * (ax_ * (by - cy) + bx * (cy - ay) + cx * (ay - by))
    ux = ((ax_ ** 2 + ay ** 2) * (by - cy) + (bx ** 2 + by ** 2) * (cy - ay) + (cx ** 2 + cy ** 2) * (ay - by)) / d
    uy = ((ax_ ** 2 + ay ** 2) * (cx - bx) + (bx ** 2 + by ** 2) * (ax_ - cx) + (cx ** 2 + cy ** 2) * (bx - ax_)) / d
    return (ux, uy)


# ---------------- theorems as stated in the book (current numbering) ----------------
TH91 = ax("प्रमेय 9.1", "वृत्त की बराबर जीवाएँ केन्द्र पर बराबर कोण अंतरित करती हैं।")
TH92 = ax("प्रमेय 9.2", "यदि एक वृत्त की जीवाओं द्वारा केन्द्र पर अंतरित कोण बराबर हों, तो वे जीवाएँ बराबर होती हैं।")
TH93 = ax("प्रमेय 9.3", "एक वृत्त के केन्द्र से एक जीवा पर डाला गया लम्ब जीवा को समद्विभाजित करता है।")
TH95 = ax("प्रमेय 9.5", "एक वृत्त की (या सर्वांगसम वृत्तों की) बराबर जीवाएँ केन्द्र से (या केन्द्रों से) समान दूरी पर होती हैं।")
TH97 = ax("प्रमेय 9.7", "एक चाप द्वारा केन्द्र पर अंतरित कोण वृत्त के शेष भाग के किसी बिन्दु पर अंतरित कोण का दुगुना होता है।")
TH98 = ax("प्रमेय 9.8", "एक ही वृत्तखंड के कोण बराबर होते हैं।")
TH99 = ax("प्रमेय 9.9", "यदि दो बिन्दुओं को मिलाने वाला रेखाखंड, उसको अंतर्विष्ट करने वाली रेखा के एक ही ओर स्थित दो अन्य बिन्दुओं पर समान कोण अंतरित करे, "
          "तो चारों बिन्दु एक वृत्त पर स्थित होते हैं (अर्थात् वे चक्रीय होते हैं)।")
TH910 = ax("प्रमेय 9.10", "चक्रीय चतुर्भुज के सम्मुख कोणों के प्रत्येक युग्म का योग " + m("180^\\circ") + " होता है।")
TH911 = ax("प्रमेय 9.11", "यदि किसी चतुर्भुज के सम्मुख कोणों के एक युग्म का योग " + m("180^\\circ") + " हो, तो चतुर्भुज चक्रीय होता है।")
SEMI = ax("अर्धवृत्त का कोण (प्रमेय 9.7 से प्राप्त गुण)", "अर्धवृत्त का कोण समकोण होता है।")
CONG_C = ax("सर्वांगसम वृत्त", "दो वृत्त सर्वांगसम होते हैं, यदि उनकी त्रिज्याएँ बराबर हों।")
RADII = ax("त्रिज्या", "एक वृत्त की सभी त्रिज्याएँ बराबर होती हैं (वृत्त के सभी बिंदु केन्द्र से एक ही दूरी पर होते हैं)।")
PYTH = ax("पाइथागोरस प्रमेय", "समकोण त्रिभुज में, (कर्ण)² = (आधार)² + (लम्ब)²")
TH87 = ax("प्रमेय 8.7", "यदि एक चतुर्भुज के विकर्ण एक दूसरे को समद्विभाजित करें, तो वह एक समांतर चतुर्भुज होता है।")
LINEAR2 = ax("अभिगृहीत 6.2 (रैखिक युग्म अभिगृहीत का विलोम)", "यदि दो आसन्न कोणों का योग " + m("180^\\circ") + " है, तो उनकी अउभयनिष्ठ भुजाएँ एक रेखा बनाती हैं।")
EQUI = ax("समबाहु त्रिभुज (प्रश्नावली 7.2, प्रश्न 8)", "समबाहु त्रिभुज का प्रत्येक कोण " + m("60^\\circ") + " होता है।")
CORR_C = ax("संगत कोण अभिगृहीत का विलोम", "यदि एक तिर्यक रेखा दो रेखाओं को इस प्रकार प्रतिच्छेद करे कि संगत कोणों का एक युग्म बराबर है, तो दोनों रेखाएँ परस्पर समांतर होती हैं।")
SQ = "(a - b)^2 = a^2 - 2ab + b^2"
IDN = ax("सर्वसमिका", m(SQ))


# =====================================================================
# Exercise 9.1
# =====================================================================
E1 = []

R1 = 78
P11 = {"O": (100, 118), "Z": (290, 118)}
P11["A"], P11["B"] = on(P11["O"], R1, 205), on(P11["O"], R1, 325)
P11["C"], P11["D"] = on(P11["Z"], R1, 230), on(P11["Z"], R1, 350)
close1(dist(P11["A"], P11["B"]), dist(P11["C"], P11["D"]), 1e-6)          # equal chords
close1(angle_at(P11["O"], P11["A"], P11["B"]), angle_at(P11["Z"], P11["C"], P11["D"]), 1e-6)


def fig91(sol, cap, given_angle=False):
    mk = [("t", "OA", 1, RED), ("t", "ZC", 1, RED), ("t", "OB", 2, BLU), ("t", "ZD", 2, BLU),
          ("a", "AOB", 1, ORG, 24), ("a", "CZD", 1, ORG, 24)]
    if not given_angle:
        mk += [("t", "AB", 3, GRN), ("t", "CD", 3, GRN)]
    segs = [("OA", RED, 3), ("OB", BLU, 3), ("ZC", RED, 3), ("ZD", BLU, 3), ("AB", GRN, 3.2), ("CD", GRN, 3.2)]
    lab = rl(P11, "O", "AB", 15)
    lab.update(rl(P11, "Z", "CD", 15))
    lab.update({"O": (90, 15), "Z": (90, 15)})
    return geo(390, 236, P11, segs, lab, mk, cap, circ=(("O", R1), ("Z", R1)), fills=(("AOB", BLU), ("CZD", ORG)), sol=sol)


s = given("दो सर्वांगसम वृत्त: केन्द्र O और O′, त्रिज्याएँ बराबर: " + m(sd("OA", RED) + " = " + sd("OB", BLU) + " = " + sd("O'C", RED) + " = " + sd("O'D", BLU))
          + "<br>पहले वृत्त की जीवा AB, दूसरे वृत्त की जीवा CD<br>" + m(sd("AB", GRN) + " = " + sd("CD", GRN)),
          "सिद्ध करना है: " + m(ang("AOB", ORG) + " = " + ang("CO'D", ORG)))
s += NOFIG + solo(fig91(True, "हल की आकृति: बराबर त्रिज्याएँ लाल और नीली, बराबर जीवाएँ हरी, केन्द्र पर बने कोण नारंगी"))
s += key((RED, "OA = O′C"), (BLU, "OB = O′D"), (GRN, "AB = CD"), (ORG, "∠AOB, ∠CO′D"))
s += num(1, CONG_C)
s += num(2, SSS)
s += kk(m("\\triangle AOB") + " और " + m("\\triangle CO'D") + " में,",
        [(sd("OA", RED) + " = " + sd("O'C", RED) + " \\quad (1)", "सर्वांगसम वृत्तों की त्रिज्याएँ बराबर हैं", "S", RED),
         (sd("OB", BLU) + " = " + sd("O'D", BLU) + " \\quad (2)", "सर्वांगसम वृत्तों की त्रिज्याएँ बराबर हैं", "S", BLU),
         (sd("AB", GRN) + " = " + sd("CD", GRN) + " \\quad (3)", "दिया है (बराबर जीवाएँ)", "S", GRN)],
        ("\\triangle AOB \\cong \\triangle CO'D", "(1), (2), (3) से, SSS सर्वांगसमता नियम द्वारा"),
        [("A", "C"), ("O", "O'"), ("B", "D")])
s += num(3, CPCT)
s += kk("", [(ang("AOB", ORG) + " = " + ang("CO'D", ORG), "CPCT (शीर्ष O ↔ O′)")])
s += ans("सर्वांगसम वृत्तों की बराबर जीवाएँ AB और CD अपने केन्द्रों पर बराबर कोण बनाती हैं: " + m(ang("AOB", ORG) + " = " + ang("CO'D", ORG)) + "। सिद्ध हुआ।")
E1.append(("याद कीजिए कि दो वृत्त सर्वांगसम होते हैं, यदि उनकी त्रिज्याएँ बराबर हों। सिद्ध कीजिए कि सर्वांगसम वृत्तों की बराबर जीवाएँ उनके केन्द्रों पर बराबर कोण अंतरित करती हैं।", s))

s = given("दो सर्वांगसम वृत्त: केन्द्र O और O′, त्रिज्याएँ बराबर: " + m(sd("OA", RED) + " = " + sd("OB", BLU) + " = " + sd("O'C", RED) + " = " + sd("O'D", BLU))
          + "<br>जीवा AB (पहला वृत्त) और जीवा CD (दूसरा वृत्त) केन्द्रों पर बराबर कोण बनाती हैं:<br>" + m(ang("AOB", ORG) + " = " + ang("CO'D", ORG)),
          "सिद्ध करना है: " + m(sd("AB", GRN) + " = " + sd("CD", GRN)))
s += NOFIG + solo(fig91(True, "हल की आकृति: बराबर त्रिज्याएँ लाल और नीली, केन्द्र पर बराबर कोण नारंगी, जीवाएँ हरी", given_angle=True))
s += key((RED, "OA = O′C"), (BLU, "OB = O′D"), (ORG, "∠AOB = ∠CO′D"), (GRN, "AB, CD"))
s += num(1, CONG_C)
s += num(2, SAS)
s += kk(m("\\triangle AOB") + " और " + m("\\triangle CO'D") + " में,",
        [(sd("OA", RED) + " = " + sd("O'C", RED) + " \\quad (1)", "सर्वांगसम वृत्तों की त्रिज्याएँ बराबर हैं", "S", RED),
         (ang("AOB", ORG) + " = " + ang("CO'D", ORG) + " \\quad (2)", "दिया है", "A", ORG),
         (sd("OB", BLU) + " = " + sd("O'D", BLU) + " \\quad (3)", "सर्वांगसम वृत्तों की त्रिज्याएँ बराबर हैं", "S", BLU)],
        ("\\triangle AOB \\cong \\triangle CO'D", "(1), (2), (3) से, SAS सर्वांगसमता नियम द्वारा (कोण O, भुजाओं OA और OB के बीच का कोण है)"),
        [("A", "C"), ("O", "O'"), ("B", "D")])
s += num(3, CPCT)
s += kk("", [(sd("AB", GRN) + " = " + sd("CD", GRN), "CPCT (A ↔ C, B ↔ D, इसलिए AB ↔ CD)")])
s += ans("केन्द्रों पर बराबर कोण बनाने वाली जीवाएँ बराबर हैं: " + m(sd("AB", GRN) + " = " + sd("CD", GRN)) + "। सिद्ध हुआ।")
E1.append(("सिद्ध कीजिए कि यदि सर्वांगसम वृत्तों की जीवाएँ उनके केन्द्रों पर बराबर कोण अंतरित करें, तो जीवाएँ बराबर होती हैं।", s))


# =====================================================================
# Exercise 9.2
# =====================================================================
E2 = []

# ---------- Q1 (no figure): common chord of circles of radii 5 cm and 3 cm, centres 4 cm apart ----------
U = 25    # px per cm
P21 = {"O": (140, 150), "Z": (240, 150)}
P21["A"], P21["B"] = circ2(P21["O"], 5 * U, P21["Z"], 3 * U)
P21["M"] = foot(P21["O"], P21["A"], P21["B"])
close1(dist(P21["O"], P21["M"]), 4 * U, 1e-6)          # x = 4 cm: M coincides with O′
close1(dist(P21["A"], P21["B"]), 6 * U, 1e-6)          # AB = 6 cm
perp_(P21["O"], P21["Z"], P21["A"], P21["B"])
x21 = (25 - 9 + 16) / 8
assert x21 == 4 and math.isclose(2 * math.sqrt(25 - x21 ** 2), 6)


def fig92_1(sol, cap):
    mk = [("t", "OA", 1, RED, .55), ("t", "OB", 1, RED, .55), ("t", "AM", 2, ORG, .5), ("t", "MB", 2, ORG, .5), ("r", "AMO", PUR)]
    segs = [("OA", RED, 3), ("OB", RED, 3), ("ZA", BLU, 8), ("ZB", BLU, 8), ("AB", ORG, 3.2), ("OZ", GRN, 3)]   # O′A, O′B lie along AB: blue underlay

    def ex(f, sol_):
        f.text((P21["O"][0] + P21["Z"][0]) / 2, P21["O"][1] + 14, "x", GRN, 14, True)
        f.text(P21["O"][0] - 6, P21["O"][1] - 46, "5", RED, 13)
        f.text(P21["Z"][0] + 34, P21["Z"][1] - 46, "3", BLU, 13)

    lab = {"O": (180, 16), "Z": (228, 22), "M": (135, 27), "A": (75, 16), "B": (285, 16)}
    return geo(330, 300, P21, segs, lab, mk, cap, circ=(("O", 5 * U), ("Z", 3 * U)), extra=ex, sol=sol)


s = given("बड़ा वृत्त: केन्द्र O, त्रिज्या " + m(sd("OA", RED) + " = " + sd("OB", RED) + " = 5\\text{ cm}") + "<br>छोटा वृत्त: केन्द्र O′, त्रिज्या "
          + m(sd("O'A", BLU) + " = " + sd("O'B", BLU) + " = 3\\text{ cm}") + "<br>केन्द्रों के बीच की दूरी " + m(sd("OO'", GRN) + " = 4\\text{ cm}")
          + "<br>वृत्त A और B पर प्रतिच्छेद करते हैं; AB उभयनिष्ठ जीवा है, जो OO′ को M पर काटती है",
          "उभयनिष्ठ जीवा " + m(sd("AB", ORG)) + " की लम्बाई")
s += NOFIG + solo(fig92_1(True, "हल की आकृति (1 cm = 25 px): 5 cm त्रिज्याएँ लाल, 3 cm त्रिज्याएँ नीली, केन्द्र-रेखा OO′ हरी, उभयनिष्ठ जीवा नारंगी"))
s += key((RED, "OA = OB = 5 cm"), (BLU, "O′A = O′B = 3 cm"), (GRN, "OO′ = 4 cm, OM = x"), (ORG, "AM = MB"), (PUR, "∠AMO = 90°"))
s += kh("चरण 1: OO′ जीवा AB को समकोण पर समद्विभाजित करती है")
s += num(1, SSS)
s += kk(m("\\triangle OAO'") + " और " + m("\\triangle OBO'") + " में,",
        [(sd("OA", RED) + " = " + sd("OB", RED), "बड़े वृत्त की त्रिज्याएँ (5 cm)", "S", RED),
         (sd("O'A", BLU) + " = " + sd("O'B", BLU), "छोटे वृत्त की त्रिज्याएँ (3 cm)", "S", BLU),
         (sd("OO'", GRN) + " = " + sd("OO'", GRN), "उभयनिष्ठ भुजा", "S", GRN)],
        ("\\triangle OAO' \\cong \\triangle OBO'", "SSS सर्वांगसमता नियम द्वारा"),
        [("O", "O"), ("A", "B"), ("O'", "O'")])
s += kk("", [("\\angle AOM = \\angle BOM \\quad (1)", "CPCT (∠AOO′ ↔ ∠BOO′; M रेखा OO′ पर है)")])
s += num(2, SAS)
s += kk(m("\\triangle AOM") + " और " + m("\\triangle BOM") + " में,",
        [(sd("OA", RED) + " = " + sd("OB", RED), "त्रिज्याएँ", "S", RED),
         ("\\angle AOM = \\angle BOM", "(1) से", "A", INK),
         ("OM = OM", "उभयनिष्ठ भुजा", "S", GRN)],
        ("\\triangle AOM \\cong \\triangle BOM", "SAS सर्वांगसमता नियम द्वारा"),
        [("A", "B"), ("O", "O"), ("M", "M")])
s += num(3, CPCT)
s += kk("", [(sd("AM", ORG) + " = " + sd("MB", ORG) + " \\quad (2)", "CPCT"),
             (ang("AMO", PUR) + " = " + ang("BMO", PUR) + " \\quad (3)", "CPCT")])
s += num(4, LINEAR)
s += chain((ang("AMO", PUR) + " + " + ang("BMO", PUR), "180" + DEG, "AMB एक रेखा है (रैखिक युग्म)"),
           (ang("AMO", PUR) + " + " + ang("AMO", PUR), "180" + DEG, "(3) से ∠BMO = ∠AMO रखने पर"),
           ("2" + ang("AMO", PUR), "180" + DEG, "∠AMO + ∠AMO = 2∠AMO"))
s += chain((ang("AMO", PUR), "\\dfrac{180^\\circ}{2}", "2 को पक्षांतर करने पर (गुणा → भाग)"),
           ("", dg(90, PUR), "180 ÷ 2 = 90"))
s += p("अतः " + m("\\triangle OMA") + " और " + m("\\triangle O'MA") + " दोनों में M पर समकोण है।")
s += kh("चरण 2: OM = x मानकर समीकरण बनाना")
s += p("माना " + m(sd("OM", GRN) + " = x \\text{ cm}") + "। तब")
s += chain((sd("O'M", GRN), "OO' - OM", "M, रेखाखंड OO′ पर है"),
           ("", "(4 - x)\\text{ cm}", "OO′ = 4 cm, OM = x रखने पर"))
s += num(5, PYTH)
s += p(m("\\triangle OMA") + " में (कर्ण OA):")
s += chain((sd("OA", RED) + "^2", sd("OM", GRN) + "^2 + " + sd("AM", ORG) + "^2", "पाइथागोरस प्रमेय"),
           ("5^2", "x^2 + " + sd("AM", ORG) + "^2", "OA = 5, OM = x रखने पर"))
s += chain((sd("AM", ORG) + "^2", "5^2 - x^2", "x² को पक्षांतर करने पर (+ → −)"),
           ("", "25 - x^2 \\qquad \\ldots(4)", "5² = 5 × 5 = 25"))
s += p(m("\\triangle O'MA") + " में (कर्ण O′A):")
s += chain((sd("O'A", BLU) + "^2", sd("O'M", GRN) + "^2 + " + sd("AM", ORG) + "^2", "पाइथागोरस प्रमेय"),
           ("3^2", "(4 - x)^2 + " + sd("AM", ORG) + "^2", "O′A = 3, O′M = 4 − x रखने पर"))
s += chain((sd("AM", ORG) + "^2", "3^2 - (4 - x)^2", "(4 − x)² को पक्षांतर करने पर (+ → −)"),
           ("", "9 - (4 - x)^2 \\qquad \\ldots(5)", "3² = 3 × 3 = 9"))
s += kh("चरण 3: x का मान")
s += num(6, IDN)
s += chain(("25 - x^2", "9 - (4 - x)^2", "(4) और (5) दोनों AM² के बराबर हैं"),
           ("", "9 - (4^2 - 2 \\times 4 \\times x + x^2)", "सर्वसमिका (a − b)² में a = 4, b = x"),
           ("", "9 - (16 - 8x + x^2)", "4² = 16, 2 × 4 × x = 8x"),
           ("", "9 - 16 + 8x - x^2", "कोष्ठक हटाने पर, अंदर के चिह्न बदलते हैं"),
           ("", "-7 + 8x - x^2", "9 − 16 = −7"))
s += chain(("25 - x^2 + x^2", "-7 + 8x", "दोनों पक्षों में x² जोड़ने पर (−x² का पक्षांतर)"),
           ("25", "-7 + 8x", "−x² + x² = 0"))
s += chain(("25 + 7", "8x", "−7 को पक्षांतर करने पर +7"),
           ("32", "8x", "25 + 7 = 32"))
s += chain(("x", "\\dfrac{32}{8}", "8 को पक्षांतर करने पर (गुणा → भाग)"),
           ("", "4", "32 ÷ 8 = 4"))
s += tp("अर्थात् OM = 4 cm = OO′, यानी M और O′ एक ही बिंदु हैं: उभयनिष्ठ जीवा छोटे वृत्त के केन्द्र O′ से होकर जाती है (O′M = 4 − 4 = 0)।")
s += kh("चरण 4: AM और AB")
s += chain((sd("AM", ORG) + "^2", "25 - x^2", "(4) से"),
           ("", "25 - 4^2", "x = 4 रखने पर"),
           ("", "25 - 16", "4² = 4 × 4 = 16"),
           ("", "9", "25 − 16 = 9"))
s += chain((sd("AM", ORG), "\\sqrt{9}", "दोनों पक्षों का वर्गमूल"),
           ("", "\\sqrt{3 \\times 3}", "9 के अभाज्य गुणनखंड: 9 = 3 × 3"),
           ("", "3 \\text{ cm}", "3 का एक जोड़ा √ से बाहर 3 आता है"))
s += num(7, TH93)
s += chain((sd("AB", ORG), sd("AM", ORG) + " + " + sd("MB", ORG), "M, AB पर है"),
           ("", sd("AM", ORG) + " + " + sd("AM", ORG), "(2) से MB = AM"),
           ("", "2 \\times " + sd("AM", ORG), "AM + AM = 2AM"),
           ("", "2 \\times 3", "AM = 3 रखने पर"),
           ("", "6 \\text{ cm}", "2 × 3 = 6"))
s += ans("उभयनिष्ठ जीवा की लम्बाई " + m("AB = 6\\text{ cm}") + " है।")
E2.append(("5 cm तथा 3 cm त्रिज्या वाले दो वृत्त दो बिन्दुओं पर प्रतिच्छेद करते हैं तथा उनके केन्द्रों के बीच की दूरी 4 cm है। उभयनिष्ठ जीवा की लम्बाई ज्ञात कीजिए।", s))

# ---------- Q2, Q3 (no figure): two equal chords intersecting inside the circle ----------
R22 = 132
P22 = {"O": (190, 155)}
P22["E"] = on(P22["O"], 72, 205)
de = Fig.dir(P22["E"], P22["O"])
P22["B"], P22["A"] = line_circ(P22["E"], de + 38, P22["O"], R22)
P22["D"], P22["C"] = line_circ(P22["E"], de - 38, P22["O"], R22)
P22["M"] = foot(P22["O"], P22["A"], P22["B"])
P22["N"] = foot(P22["O"], P22["C"], P22["D"])
oncirc(P22, "O", R22, "ABCD")
close1(dist(P22["A"], P22["B"]), dist(P22["C"], P22["D"]), 1e-6)       # equal chords
on_seg(P22["M"], P22["A"], P22["E"])
on_seg(P22["N"], P22["C"], P22["E"])
close1(dist(P22["A"], P22["E"]), dist(P22["C"], P22["E"]), 1e-6)      # Q2 result
close1(dist(P22["E"], P22["B"]), dist(P22["E"], P22["D"]), 1e-6)
close1(angle_at(P22["E"], P22["O"], P22["A"]), angle_at(P22["E"], P22["O"], P22["C"]), 1e-6)   # Q3 result


def fig92_2(sol, cap, q3=False):
    mk = [("r", "OMA", PUR), ("r", "ONC", PUR), ("t", "OM", 1, RED), ("t", "ON", 1, RED),
          ("t", "ME", 2, ORG), ("t", "NE", 2, ORG), ("t", "AM", 3, BLU), ("t", "CN", 3, BLU)]
    if q3:
        mk += [("a", "OEM", 1, BROWN, 30), ("a", "OEN", 2, BROWN, 30)]
    else:
        mk += [("t", "EB", 1, TEA), ("t", "ED", 1, TEA)]
    segs = [("AM", BLU, 3), ("ME", ORG, 3), ("EB", TEA, 3), ("CN", BLU, 3), ("NE", ORG, 3), ("ED", TEA, 3),
            ("OM", RED, 2.6), ("ON", RED, 2.6), ("OE", GRN, 3)]
    lab = rl(P22, "O", "ABCD", 15)
    lab.update({"O": (Fig.dir(P22["E"], P22["O"]), 16), "E": (de + 180, 17),
                "M": (Fig.dir(P22["O"], P22["M"]), 16), "N": (Fig.dir(P22["O"], P22["N"]), 16)})
    return geo(380, 315, P22, segs, lab, mk, cap, circ=(("O", R22),), fills=(("OME", BLU), ("ONE", ORG)), sol=sol)


def common_22(s, q3=False):
    s += num(1, TH95)
    s += kk("जीवाएँ AB और CD बराबर हैं, इसलिए", [(sd("OM", RED) + " = " + sd("ON", RED) + " \\quad (1)", "प्रमेय 9.5 (बराबर जीवाएँ केन्द्र से समान दूरी पर)")])
    s += num(2, RHS)
    s += kk(m("\\triangle OME") + " और " + m("\\triangle ONE") + " में,",
            [(ang("OME", PUR) + " = " + ang("ONE", PUR) + " = 90^\\circ", "रचना से (OM ⊥ AB, ON ⊥ CD)", "R", PUR),
             (sd("OE", GRN) + " = " + sd("OE", GRN), "उभयनिष्ठ कर्ण", "H", GRN),
             (sd("OM", RED) + " = " + sd("ON", RED), "(1) से", "S", RED)],
            ("\\triangle OME \\cong \\triangle ONE", "RHS सर्वांगसमता नियम द्वारा"),
            [("O", "O"), ("M", "N"), ("E", "E")])
    s += num(3, CPCT)
    return s


s = given("केन्द्र O वाले वृत्त की दो बराबर जीवाएँ: " + m(sd("AB", BLU) + " = " + sd("CD", BLU)) + "<br>AB और CD वृत्त के अंदर बिंदु E पर प्रतिच्छेद करती हैं",
          "सिद्ध करना है: " + m(sd("AE", BLU) + " = " + sd("CE", BLU)) + " और " + m(sd("EB", TEA) + " = " + sd("ED", TEA)))
s += NOFIG + solo(fig92_2(True, "हल की आकृति: OM ⊥ AB, ON ⊥ CD (लाल); AM = CN नीले, ME = NE नारंगी, EB = ED हरे-नीले"))
s += p("रचना: O से " + m("OM \\perp AB") + " और " + m("ON \\perp CD") + " खींचिए; OE को मिलाइए।")
s += key((RED, "OM = ON"), (GRN, "OE (उभयनिष्ठ)"), (ORG, "ME = NE"), (BLU, "AM = CN"), (TEA, "EB = ED"), (PUR, "समकोण"))
s = common_22(s)
s += kk("", [(sd("ME", ORG) + " = " + sd("NE", ORG) + " \\quad (2)", "CPCT (M ↔ N)")])
s += num(4, TH93)
s += chain((sd("AM", BLU), HALF + sd("AB", BLU), "प्रमेय 9.3: OM ⊥ AB, इसलिए M, AB का मध्य-बिंदु है"),
           ("", HALF + sd("CD", BLU), "AB = CD (दिया है)"),
           ("", sd("CN", BLU) + " \\qquad \\ldots(3)", "प्रमेय 9.3: ON ⊥ CD, इसलिए N, CD का मध्य-बिंदु है"))
s += kh("एक जीवा के खंड = दूसरी के संगत खंड")
s += chain(("AE", sd("AM", BLU) + " + " + sd("ME", ORG), "M, A और E के बीच है"),
           ("", sd("CN", BLU) + " + " + sd("NE", ORG), "(3) और (2) से"),
           ("", "CE \\qquad \\ldots(4)", "N, C और E के बीच है"))
s += chain((sd("EB", TEA), "AB - AE", "E, AB पर है"),
           ("", "CD - CE", "AB = CD (दिया है) और (4) से AE = CE"),
           ("", sd("ED", TEA), "E, CD पर है"))
s += ans("(i) " + m("AE = CE") + " (ii) " + m("EB = ED") + " — अर्थात् एक जीवा के खंड दूसरी जीवा के संगत खंडों के बराबर हैं। सिद्ध हुआ।")
E2.append(("यदि एक वृत्त की दो समान जीवाएँ वृत्त के अन्दर प्रतिच्छेद करें, तो सिद्ध कीजिए कि एक जीवा के खंड दूसरी जीवा के संगत खंडों के बराबर हैं।", s))

s = given("केन्द्र O वाले वृत्त की दो बराबर जीवाएँ: " + m(sd("AB", BLU) + " = " + sd("CD", BLU)) + "<br>AB और CD वृत्त के अंदर बिंदु E पर प्रतिच्छेद करती हैं; OE को मिलाया गया",
          "सिद्ध करना है: OE जीवाओं से बराबर कोण बनाती है: " + m(ang("OEA", BROWN) + " = " + ang("OEC", BROWN)))
s += NOFIG + solo(fig92_2(True, "हल की आकृति: OM ⊥ AB, ON ⊥ CD (लाल); OE हरी; OE द्वारा जीवाओं से बने कोण भूरे", q3=True))
s += p("रचना: O से " + m("OM \\perp AB") + " और " + m("ON \\perp CD") + " खींचिए; OE को मिलाइए।")
s += key((RED, "OM = ON"), (GRN, "OE (उभयनिष्ठ)"), (BROWN, "∠OEM, ∠OEN"), (PUR, "समकोण"))
s = common_22(s)
s += kk("", [(ang("OEM", BROWN) + " = " + ang("OEN", BROWN) + " \\quad (2)", "CPCT (M ↔ N)")])
s += p("M, रेखाखंड EA पर है और N, रेखाखंड EC पर है, इसलिए " + m(ang("OEM", BROWN) + " = " + ang("OEA", BROWN)) + " और " + m(ang("OEN", BROWN) + " = " + ang("OEC", BROWN)) + "।")
s += chain((ang("OEA", BROWN), ang("OEM", BROWN), "M, EA पर है"),
           ("", ang("OEN", BROWN), "(2) से"),
           ("", ang("OEC", BROWN), "N, EC पर है"))
s += ans("प्रतिच्छेद बिंदु E को केन्द्र O से मिलाने वाली रेखा OE दोनों जीवाओं से बराबर कोण बनाती है: " + m(ang("OEA", BROWN) + " = " + ang("OEC", BROWN)) + "। सिद्ध हुआ।")
E2.append(("यदि एक वृत्त की दो समान जीवाएँ वृत्त के अन्दर प्रतिच्छेद करें, तो सिद्ध कीजिए कि प्रतिच्छेद बिन्दु को केन्द्र से मिलाने वाली रेखा जीवाओं से बराबर कोण बनाती है।", s))

# ---------- Q4 (आकृति 9.12): concentric circles ----------
RO, RI = 118, 66
P24 = {"O": (185, 140)}
d24 = 20
P24["M"] = Fig.pol(P24["O"], d24 - 90, 36)
P24["A"], P24["D"] = line_circ(P24["M"], d24, P24["O"], RO)
P24["B"], P24["C"] = line_circ(P24["M"], d24, P24["O"], RI)
oncirc(P24, "O", RO, "AD")
oncirc(P24, "O", RI, "BC")
close1(dist(P24["A"], P24["B"]), dist(P24["C"], P24["D"]), 1e-6)


def fig912(sol, cap):
    def ex(f, sol_):
        a0, d0 = Fig.pol(P24["A"], d24 + 180, 24), Fig.pol(P24["D"], d24, 26)
        f.line(a0, P24["A"], INK, 2.2, a1=True)
        f.line(P24["D"], d0, INK, 2.2, a2=True)
    if sol:
        mk = [("r", "OMD", PUR), ("t", "AB", 2, GRN), ("t", "CD", 2, GRN), ("t", "BM", 1, BLU), ("t", "MC", 1, BLU)]
        segs = [("AB", GRN, 3.4), ("BM", BLU, 3.4), ("MC", BLU, 3.4), ("CD", GRN, 3.4), ("OM", RED, 2.6, "6 4")]
        lab = {"A": (255, 16), "B": (250, 16), "C": (295, 16), "D": (75, 16), "O": (90, 15), "M": (d24 - 90, 17)}
        P = P24
    else:
        mk, segs = [], ["AD"]
        lab = {"A": (255, 16), "B": (250, 16), "C": (295, 16), "D": (75, 16), "O": (90, 15)}
        P = {k: v for k, v in P24.items() if k != "M"}
    return geo(370, 280, P, segs, lab, mk, cap, circ=(("O", RO), ("O", RI)), extra=ex, sol=sol)


s = given("संकेन्द्री वृत्त, केन्द्र O<br>एक रेखा बड़े वृत्त को A और D पर तथा छोटे वृत्त को B और C पर काटती है",
          "सिद्ध करना है: " + m(sd("AB", GRN) + " = " + sd("CD", GRN)))
s += figs(fig912, "आकृति 9.12", "OM ⊥ AD (लाल), BM = MC नीले, AB और CD हरे")
s += p("रचना: O से रेखा पर " + m("OM \\perp AD") + " खींचिए।")
s += key((RED, "OM ⊥ AD"), (BLU, "BM = MC"), (GRN, "AB, CD"), (PUR, "समकोण"))
s += num(1, TH93)
s += chain(("AM", "MD \\qquad \\ldots(1)", "बड़े वृत्त की जीवा AD पर केन्द्र से लम्ब OM (प्रमेय 9.3)"))
s += chain((sd("BM", BLU), sd("MC", BLU) + " \\qquad \\ldots(2)", "छोटे वृत्त की जीवा BC पर केन्द्र से लम्ब OM (प्रमेय 9.3)"))
s += chain((sd("AB", GRN), "AM - " + sd("BM", BLU), "B, A और M के बीच है"),
           ("", "MD - " + sd("MC", BLU), "(1) और (2) से"),
           ("", sd("CD", GRN), "C, M और D के बीच है"))
s += ans(m(sd("AB", GRN) + " = " + sd("CD", GRN)) + "। सिद्ध हुआ।")
E2.append(("यदि एक रेखा दो संकेन्द्री वृत्तों (एक ही केन्द्र वाले वृत्त) को, जिनका केन्द्र O है, A, B, C और D पर प्रतिच्छेद करे, तो सिद्ध कीजिए "
           + m("AB = CD") + " है (देखिए आकृति 9.12)।", s))

# ---------- Q5 (no figure): Reshma, Salma, Mandip ----------
V = 26    # px per metre
R25 = 5 * V
P25 = {"O": (180, 165)}
t25 = math.degrees(2 * math.asin(3 / 5))
P25["S"] = on(P25["O"], R25, 90)
P25["R"] = on(P25["O"], R25, 90 + t25)
P25["M"] = on(P25["O"], R25, 90 - t25)
P25["L"] = inter(P25["O"], P25["S"], P25["R"], P25["M"])
close1(dist(P25["R"], P25["S"]), 6 * V, 1e-6)
close1(dist(P25["S"], P25["M"]), 6 * V, 1e-6)
close1(dist(P25["O"], P25["L"]), 1.4 * V, 1e-6)
close1(dist(P25["R"], P25["M"]), 9.6 * V, 1e-6)
x25 = (25 + 25 - 36) / 10
assert math.isclose(x25, 1.4) and math.isclose(2 * math.sqrt(25 - x25 ** 2), 9.6)
assert 2304 == 2 ** 8 * 3 ** 2 and 100 == 2 ** 2 * 5 ** 2 and (2 ** 4 * 3) / (2 * 5) == 4.8


def fig92_5(sol, cap):
    mk = [("t", "RS", 2, ORG), ("t", "SM", 2, ORG), ("t", "OR", 1, RED), ("t", "OM", 1, RED), ("t", "RL", 3, BLU, .5), ("t", "LM", 3, BLU, .5),
          ("r", "OLR", PUR), ("a", "ROL", 1, TEA, 15), ("a", "MOL", 1, TEA, 15)]
    segs = [("RS", ORG, 3), ("SM", ORG, 3), ("OR", RED, 3), ("OM", RED, 3), ("RL", BLU, 3.2), ("LM", BLU, 3.2), ("OL", PUR, 3), ("LS", GRN, 3)]

    def ex(f, sol_):
        f.text(P25["O"][0] + 10, (P25["O"][1] + P25["L"][1]) / 2 - 4, "x", PUR, 14, True)
    lab = rl(P25, "O", "RSM", 15)
    lab.update({"O": (270, 16), "L": (45, 17)})
    return geo(360, 330, P25, segs, lab, mk, cap, circ=(("O", R25),), fills=(("ROL", BLU), ("MOL", ORG)), extra=ex, sol=sol)


s = given("वृत्त का केन्द्र O, त्रिज्या " + m(sd("OR", RED) + " = OS = " + sd("OM", RED) + " = 5\\text{ m}") + "<br>R = रेशमा, S = सलमा, M = मनदीप (वृत्त पर)<br>"
          + m(sd("RS", ORG) + " = " + sd("SM", ORG) + " = 6\\text{ m}"),
          "रेशमा और मनदीप के बीच की दूरी " + m("RM"))
s += NOFIG + solo(fig92_5(True, "हल की आकृति (1 m = 26 px): त्रिज्याएँ लाल, RS = SM नारंगी, OL = x बैंगनी, RL = LM नीले"))
s += p("रचना: O और S को मिलाइए; OS, जीवा RM को L पर काटती है।")
s += key((RED, "OR = OM = 5 m"), (ORG, "RS = SM = 6 m"), (TEA, "∠ROL = ∠MOL"), (PUR, "OL = x, समकोण"), (GRN, "LS = 5 − x"), (BLU, "RL = LM = y"))
s += kh("चरण 1: OS, जीवा RM को समकोण पर समद्विभाजित करती है")
s += num(1, SSS)
s += kk(m("\\triangle ORS") + " और " + m("\\triangle OMS") + " में,",
        [(sd("OR", RED) + " = " + sd("OM", RED), "त्रिज्याएँ (5 m)", "S", RED),
         (sd("RS", ORG) + " = " + sd("MS", ORG), "दिया है (6 m)", "S", ORG),
         ("OS = OS", "उभयनिष्ठ भुजा", "S", INK)],
        ("\\triangle ORS \\cong \\triangle OMS", "SSS सर्वांगसमता नियम द्वारा"),
        [("O", "O"), ("R", "M"), ("S", "S")])
s += kk("", [(ang("ROL", TEA) + " = " + ang("MOL", TEA) + " \\quad (1)", "CPCT (∠ROS ↔ ∠MOS; L रेखा OS पर है)")])
s += num(2, SAS)
s += kk(m("\\triangle ROL") + " और " + m("\\triangle MOL") + " में,",
        [(sd("OR", RED) + " = " + sd("OM", RED), "त्रिज्याएँ", "S", RED),
         (ang("ROL", TEA) + " = " + ang("MOL", TEA), "(1) से", "A", TEA),
         (sd("OL", PUR) + " = " + sd("OL", PUR), "उभयनिष्ठ भुजा", "S", PUR)],
        ("\\triangle ROL \\cong \\triangle MOL", "SAS सर्वांगसमता नियम द्वारा"),
        [("R", "M"), ("O", "O"), ("L", "L")])
s += num(3, CPCT)
s += kk("", [(sd("RL", BLU) + " = " + sd("LM", BLU) + " \\quad (2)", "CPCT"),
             (ang("RLO", PUR) + " = " + ang("MLO", PUR) + " \\quad (3)", "CPCT")])
s += num(4, LINEAR)
s += chain((ang("RLO", PUR) + " + " + ang("MLO", PUR), "180" + DEG, "RLM एक रेखा है (रैखिक युग्म)"),
           ("2" + ang("RLO", PUR), "180" + DEG, "(3) से ∠MLO = ∠RLO रखने पर"))
s += chain((ang("RLO", PUR), "\\dfrac{180^\\circ}{2}", "2 को पक्षांतर करने पर (गुणा → भाग)"),
           ("", dg(90, PUR), "180 ÷ 2 = 90"))
s += kh("चरण 2: OL = x और RL = y मानकर समीकरण")
s += p("माना " + m(sd("OL", PUR) + " = x \\text{ m}") + " और " + m(sd("RL", BLU) + " = y \\text{ m}") + "। तब")
s += chain((sd("LS", GRN), "OS - " + sd("OL", PUR), "L, रेखाखंड OS पर है"),
           ("", "(5 - x)\\text{ m}", "OS = 5, OL = x रखने पर"))
s += num(5, PYTH)
s += p("समकोण " + m("\\triangle RLO") + " में (कर्ण OR):")
s += chain((sd("OR", RED) + "^2", sd("OL", PUR) + "^2 + " + sd("RL", BLU) + "^2", "पाइथागोरस प्रमेय"),
           ("5^2", "x^2 + y^2", "मान रखने पर"))
s += chain(("x^2 + y^2", "25 \\qquad \\ldots(4)", "5² = 5 × 5 = 25 (पक्ष बदलकर लिखा)"))
s += p("समकोण " + m("\\triangle RLS") + " में (कर्ण RS):")
s += num(6, IDN)
s += chain((sd("RS", ORG) + "^2", sd("LS", GRN) + "^2 + " + sd("RL", BLU) + "^2", "पाइथागोरस प्रमेय"),
           ("6^2", "(5 - x)^2 + y^2", "मान रखने पर"),
           ("36", "5^2 - 2 \\times 5 \\times x + x^2 + y^2", "6² = 36; सर्वसमिका (a − b)² में a = 5, b = x"),
           ("", "25 - 10x + x^2 + y^2", "5² = 25, 2 × 5 × x = 10x"),
           ("", "25 - 10x + (x^2 + y^2)", "x² + y² को साथ रखने पर"),
           ("", "25 - 10x + 25", "(4) से x² + y² = 25 रखने पर"),
           ("", "50 - 10x", "25 + 25 = 50"))
s += kh("चरण 3: x का मान")
s += chain(("36 + 10x", "50", "36 = 50 − 10x में −10x को पक्षांतर करने पर (− → +)"))
s += chain(("10x", "50 - 36", "36 को पक्षांतर करने पर (+ → −)"),
           ("", "14", "50 − 36 = 14"))
s += chain(("x", "\\dfrac{14}{10}", "10 को पक्षांतर करने पर (गुणा → भाग)"),
           ("", "1.4", "14 ÷ 10 = 1.4"))
s += kh("चरण 4: y का मान")
s += chain(("y^2", "25 - x^2", "(4) से x² का पक्षांतर करने पर"),
           ("", "25 - (1.4)^2", "x = 1.4 रखने पर"),
           ("", "25 - 1.96", "1.4 × 1.4 = 1.96"),
           ("", "23.04", "25.00 − 1.96 = 23.04"))
s += chain(("y", "\\sqrt{23.04}", "दोनों पक्षों का वर्गमूल"),
           ("", "\\sqrt{\\dfrac{2304}{100}}", "23.04 = 2304 ÷ 100"),
           ("", "\\sqrt{\\dfrac{2 \\times 2 \\times 2 \\times 2 \\times 2 \\times 2 \\times 2 \\times 2 \\times 3 \\times 3}{2 \\times 2 \\times 5 \\times 5}}",
            "अभाज्य गुणनखंड: 2304 = 2⁸ × 3², 100 = 2² × 5²"),
           ("", "\\dfrac{2 \\times 2 \\times 2 \\times 2 \\times 3}{2 \\times 5}", "हर जोड़े में से एक संख्या √ से बाहर: ऊपर 2 के 4 जोड़े, 3 का 1 जोड़ा; नीचे 2 और 5 का 1-1 जोड़ा"),
           ("", "\\dfrac{48}{10}", "2 × 2 × 2 × 2 × 3 = 48, 2 × 5 = 10"),
           ("", "4.8", "48 ÷ 10 = 4.8"))
s += kh("चरण 5: रेशमा और मनदीप के बीच की दूरी")
s += chain(("RM", sd("RL", BLU) + " + " + sd("LM", BLU), "L, RM पर है"),
           ("", "y + y", "(2) से LM = RL = y"),
           ("", "2y", "y + y = 2y"),
           ("", "2 \\times 4.8", "y = 4.8 रखने पर"),
           ("", "9.6 \\text{ m}", "2 × 4.8 = 9.6"))
s += ans("रेशमा और मनदीप के बीच की दूरी " + m("RM = 9.6\\text{ m}") + " है।")
E2.append(("एक पार्क में बने 5 m त्रिज्या वाले वृत्त पर खड़ी तीन लड़कियाँ रेशमा, सलमा एवं मनदीप खेल रही हैं। रेशमा एक गेंद को सलमा के पास, सलमा मनदीप के पास तथा "
           "मनदीप रेशमा के पास फेंकती है। यदि रेशमा तथा सलमा के बीच और सलमा तथा मनदीप के बीच की प्रत्येक दूरी 6 m हो, तो रेशमा और मनदीप के बीच की दूरी क्या है?", s))

# ---------- Q6 (no figure): Ankur, Syed, David at equal distances on a circle of radius 20 m ----------
W26 = 6.25    # px per metre
R26 = 20 * W26
P26 = {"O": (190, 162)}
P26["A"], P26["S"], P26["D"] = on(P26["O"], R26, 90), on(P26["O"], R26, 210), on(P26["O"], R26, 330)
P26["K"] = on(P26["O"], R26, 150)
P26["L"] = mid(P26["A"], P26["S"])
on_seg(P26["L"], P26["O"], P26["K"])
perp_(P26["O"], P26["L"], P26["A"], P26["S"])
close1(dist(P26["A"], P26["K"]), R26, 1e-6)                    # ΔAOK equilateral
close1(dist(P26["O"], P26["L"]), 10 * W26, 1e-6)                # OL = 10 m
close1(dist(P26["A"], P26["S"]), 20 * math.sqrt(3) * W26, 1e-6)  # AS = 20√3 m
assert 300 == 2 * 2 * 3 * 5 * 5


def fig92_6(sol, cap):
    mk = [("t", "AS", 2, ORG), ("t", "SD", 2, ORG), ("t", "DA", 2, ORG), ("r", "OLA", PUR),
          ("a", "AOL", 1, TEA, 22), ("a", "LOS", 1, TEA, 22), ("t", "OL", 1, GRN, .5), ("t", "LK", 1, GRN, .5), ("t", "AK", 3, RED, .5)]
    segs = [("AS", ORG, 3), ("SD", ORG, 2.4), ("DA", ORG, 2.4), ("OA", RED, 3), ("OS", RED, 2.6), ("OD", RED, 2.2, "5 4"),
            ("OL", GRN, 3.2), ("LK", GRN, 3.2, "6 4"), ("AK", RED, 2.8, "6 4")]
    lab = rl(P26, "O", "ASDK", 15)
    lab.update({"O": (300, 17), "L": (195, 17)})
    return geo(380, 325, P26, segs, lab, mk, cap, circ=(("O", R26),), fills=(("AOK", BLU),), sol=sol)


s = given("वृत्ताकार पार्क: केन्द्र O, त्रिज्या " + m(sd("OA", RED) + " = OS = OD = 20\\text{ m}") + "<br>A = अंकुर, S = सैय्यद, D = डेविड (परिसीमा पर, बराबर दूरी पर)<br>"
          + m(sd("AS", ORG) + " = " + sd("SD", ORG) + " = " + sd("DA", ORG)),
          "प्रत्येक फोन की डोरी की लम्बाई " + m(sd("AS", ORG)))
s += NOFIG + solo(fig92_6(True, "हल की आकृति: बराबर डोरियाँ नारंगी, त्रिज्याएँ लाल, OL ⊥ AS; OL को बढ़ाने पर वह वृत्त को K पर मिलती है"))
s += p("रचना: O से " + m("OL \\perp AS") + " खींचिए और OL को बढ़ाइए, जो वृत्त को K पर मिले। AK को मिलाइए।")
s += key((ORG, "AS = SD = DA"), (RED, "त्रिज्याएँ OA = OK = AK"), (TEA, "∠AOL = ∠SOL"), (GRN, "OL = LK"), (PUR, "समकोण"))
s += kh("चरण 1: " + m(ang("AOS") + " = 120^\\circ"))
s += num(1, TH91)
s += chain((ang("AOS"), ang("SOD"), "AS = SD, बराबर जीवाएँ (प्रमेय 9.1)"),
           ("", ang("DOA") + " \\qquad \\ldots(1)", "SD = DA, बराबर जीवाएँ (प्रमेय 9.1)"))
s += chain((ang("AOS") + " + " + ang("SOD") + " + " + ang("DOA"), "360" + DEG, "O के चारों ओर पूरा कोण"),
           (ang("AOS") + " + " + ang("AOS") + " + " + ang("AOS"), "360" + DEG, "(1) से रखने पर"),
           ("3" + ang("AOS"), "360" + DEG, "तीन बार जोड़ = 3 गुना"))
s += chain((ang("AOS"), "\\dfrac{360^\\circ}{3}", "3 को पक्षांतर करने पर (गुणा → भाग)"),
           ("", "120^\\circ", "360 ÷ 3 = 120"))
s += kh("चरण 2: " + m(ang("AOL", TEA) + " = 60^\\circ"))
s += num(2, RHS)
s += kk(m("\\triangle OLA") + " और " + m("\\triangle OLS") + " में,",
        [(ang("OLA", PUR) + " = " + ang("OLS", PUR) + " = 90^\\circ", "रचना से (OL ⊥ AS)", "R", PUR),
         (sd("OA", RED) + " = " + sd("OS", RED), "त्रिज्याएँ (कर्ण)", "H", RED),
         (sd("OL", GRN) + " = " + sd("OL", GRN), "उभयनिष्ठ भुजा", "S", GRN)],
        ("\\triangle OLA \\cong \\triangle OLS", "RHS सर्वांगसमता नियम द्वारा"),
        [("O", "O"), ("L", "L"), ("A", "S")])
s += kk("", [(ang("AOL", TEA) + " = " + ang("SOL", TEA) + " \\quad (2)", "CPCT"),
             ("AL = LS \\quad (3)", "CPCT (यह प्रमेय 9.3 से भी मिलता है)")])
s += chain((ang("AOL", TEA) + " + " + ang("SOL", TEA), ang("AOS"), "OL, ∠AOS के अंदर है"),
           ("2" + ang("AOL", TEA), "120^\\circ", "(2) से और चरण 1 से"))
s += chain((ang("AOL", TEA), "\\dfrac{120^\\circ}{2}", "2 को पक्षांतर करने पर (गुणा → भाग)"),
           ("", dg(60, TEA), "120 ÷ 2 = 60"))
s += kh("चरण 3: " + m("\\triangle AOK") + " समबाहु है, अतः " + m(sd("AK", RED) + " = 20\\text{ m}"))
s += num(3, TH72)
s += chain((ang("OAK"), ang("OKA") + " \\qquad \\ldots(4)", "OA = OK (त्रिज्याएँ), इनके सम्मुख कोण (प्रमेय 7.2)"))
s += num(4, ASUM)
s += chain((ang("OAK") + " + " + ang("OKA") + " + " + ang("AOK", TEA), "180" + DEG, "त्रिभुज AOK के कोणों का योग"),
           (ang("OAK") + " + " + ang("OAK") + " + 60" + DEG, "180" + DEG, "(4) से, और ∠AOK = ∠AOL = 60°"),
           ("2" + ang("OAK") + " + 60" + DEG, "180" + DEG, "∠OAK + ∠OAK = 2∠OAK"))
s += chain(("2" + ang("OAK"), "180" + DEG + " - 60" + DEG, "60° को पक्षांतर करने पर (+ → −)"),
           ("2" + ang("OAK"), "120" + DEG, "180 − 60 = 120"))
s += chain((ang("OAK"), "\\dfrac{120^\\circ}{2}", "2 को पक्षांतर करने पर (गुणा → भाग)"),
           ("", "60^\\circ", "120 ÷ 2 = 60"))
s += num(5, TH73)
s += p(m(ang("AOK", TEA) + " = " + ang("OKA") + " = 60^\\circ") + " (चरण 2 और (4) से), इसलिए इनकी सम्मुख भुजाएँ बराबर हैं:")
s += chain((sd("AK", RED), sd("OA", RED), "∠AOK के सामने AK, ∠OKA के सामने OA (प्रमेय 7.3)"),
           ("", "20 \\text{ m}", "त्रिज्या"))
s += kh("चरण 4: " + m(sd("OL", GRN) + " = 10\\text{ m}"))
s += kk(m("\\triangle ALO") + " और " + m("\\triangle ALK") + " में,",
        [(ang("ALO", PUR) + " = " + ang("ALK", PUR) + " = 90^\\circ", "रचना से (AL ⊥ OK)", "R", PUR),
         (sd("AO", RED) + " = " + sd("AK", RED), "दोनों 20 m (चरण 3)", "H", RED),
         ("AL = AL", "उभयनिष्ठ भुजा", "S", BLU)],
        ("\\triangle ALO \\cong \\triangle ALK", "RHS सर्वांगसमता नियम द्वारा"),
        [("A", "A"), ("L", "L"), ("O", "K")])
s += kk("", [(sd("OL", GRN) + " = " + sd("LK", GRN) + " \\quad (5)", "CPCT")])
s += chain((sd("OL", GRN) + " + " + sd("LK", GRN), "OK", "L, OK पर है"),
           (sd("OL", GRN) + " + " + sd("OL", GRN), "20", "(5) से, और OK = 20 m (त्रिज्या)"),
           ("2 \\times " + sd("OL", GRN), "20", "OL + OL = 2OL"))
s += chain((sd("OL", GRN), "\\dfrac{20}{2}", "2 को पक्षांतर करने पर (गुणा → भाग)"),
           ("", "10 \\text{ m}", "20 ÷ 2 = 10"))
s += kh("चरण 5: AL और डोरी AS")
s += num(6, PYTH)
s += chain((sd("OA", RED) + "^2", sd("OL", GRN) + "^2 + AL^2", "समकोण △OLA में पाइथागोरस प्रमेय (कर्ण OA)"),
           ("20^2", "10^2 + AL^2", "मान रखने पर"),
           ("400", "100 + AL^2", "20 × 20 = 400, 10 × 10 = 100"))
s += chain(("AL^2", "400 - 100", "100 को पक्षांतर करने पर (+ → −)"),
           ("", "300", "400 − 100 = 300"))
s += chain(("AL", "\\sqrt{300}", "दोनों पक्षों का वर्गमूल"),
           ("", "\\sqrt{2 \\times 2 \\times 3 \\times 5 \\times 5}", "300 के अभाज्य गुणनखंड: 300 = 2 × 2 × 3 × 5 × 5"),
           ("", "2 \\times 5 \\times \\sqrt{3}", "2 का एक जोड़ा और 5 का एक जोड़ा √ से बाहर; 3 अंदर रहता है"),
           ("", "10\\sqrt{3}\\text{ m}", "2 × 5 = 10"))
s += chain((sd("AS", ORG), "AL + LS", "L, AS पर है"),
           ("", "AL + AL", "(3) से LS = AL"),
           ("", "2 \\times 10\\sqrt{3}", "AL + AL = 2AL"),
           ("", "20\\sqrt{3}\\text{ m}", "2 × 10 = 20"),
           ("", "20 \\times 1.732", "√3 ≈ 1.732 रखने पर"),
           ("", "34.64 \\text{ m}", "20 × 1.732 = 34.64 (लगभग)"))
s += ans("प्रत्येक फोन की डोरी की लम्बाई " + m("20\\sqrt{3}\\text{ m}") + " है (लगभग " + m("34.64\\text{ m}") + ")।")
E2.append(("20 m त्रिज्या का एक गोल पार्क (वृत्ताकार) एक कालोनी में स्थित है। तीन लड़के अंकुर, सैय्यद तथा डेविड इसकी परिसीमा पर बराबर दूरी पर बैठे हैं और प्रत्येक के हाथ में "
           "एक खिलौना टेलीफोन आपस में बात करने के लिए है। प्रत्येक फोन की डोरी की लम्बाई ज्ञात कीजिए।", s))


# =====================================================================
# Exercise 9.3
# =====================================================================
E3 = []

# ---------- Q1 (आकृति 9.23) ----------
R31 = 110
P31 = {"O": (180, 150)}
P31["B"], P31["C"], P31["A"], P31["D"] = (on(P31["O"], R31, d) for d in (95, 65, 155, 290))
close1(angle_at(P31["O"], P31["A"], P31["B"]), 60, 1e-6)
close1(angle_at(P31["O"], P31["B"], P31["C"]), 30, 1e-6)
close1(angle_at(P31["D"], P31["A"], P31["C"]), 45, 1e-6)


def fig923(sol, cap):
    def ex(f, sol_):
        if sol_:
            carc(f, P31["O"], 65, 155, R31, PUR, 5)
        else:
            bl(f, P31, "AOB", "60°", 30)
            bl(f, P31, "BOC", "30°", 30)
    if sol:
        mk = [("a", "AOB", 1, ORG, 26), ("a", "BOC", 1, BLU, 26), ("ad", "AOC", PUR, 68), ("a", "ADC", 1, GRN, 32),
              ("l", "AOB", "60°", ORG, 42), ("l", "BOC", "30°", BLU, 54), ("l", "ADC", "45°", GRN, 46),
              ("t", "OA", 1, RED), ("t", "OC", 1, RED)]
        segs = [("OA", RED, 2.6), ("OB", INK, 2.2), ("OC", RED, 2.6), ("AD", GRN, 3), ("CD", GRN, 3)]
    else:
        mk = [("a", "AOB", 1, INK, 20), ("a", "BOC", 1, INK, 20)]
        segs = ["OA", "OB", "OC", "AD", "CD"]
    lab = rl(P31, "O", "ABCD", 15)
    lab.update({"O": (250, 17)})
    return geo(360, 300, P31, segs, lab, mk, cap, circ=(("O", R31),), extra=ex, sol=sol)


s = given("केन्द्र O वाले वृत्त पर बिंदु A, B, C: " + m(ang("AOB", ORG) + " = 60^\\circ") + ", " + m(ang("BOC", BLU) + " = 30^\\circ")
          + "<br>D, चाप ABC के अतिरिक्त वृत्त पर एक बिंदु है", m(ang("ADC", GRN)))
s += figs(fig923, "आकृति 9.23", "चाप ABC बैंगनी; यह केन्द्र पर ∠AOC (बैंगनी रेखा-चाप) और D पर ∠ADC (हरा) बनाता है")
s += key((ORG, "∠AOB = 60°"), (BLU, "∠BOC = 30°"), (PUR, "चाप ABC, ∠AOC"), (GRN, "∠ADC"))
s += chain((ang("AOC", PUR), ang("AOB", ORG) + " + " + ang("BOC", BLU), "OB, ∠AOC के अंदर है"),
           ("", dg(60, ORG) + " + " + dg(30, BLU), "मान रखने पर"),
           ("", dg(90, PUR) + " \\qquad \\ldots(1)", "60 + 30 = 90"))
s += num(1, TH97)
s += p("चाप ABC केन्द्र O पर " + m(ang("AOC", PUR)) + " और वृत्त के शेष भाग के बिंदु D पर " + m(ang("ADC", GRN)) + " अंतरित करता है।")
s += chain((ang("AOC", PUR), "2" + ang("ADC", GRN), "प्रमेय 9.7"))
s += chain(("2" + ang("ADC", GRN), ang("AOC", PUR), "पक्ष बदलकर लिखने पर"),
           ("", dg(90, PUR), "(1) से"))
s += chain((ang("ADC", GRN), "\\dfrac{90^\\circ}{2}", "2 को पक्षांतर करने पर (गुणा → भाग)"),
           ("", dg(45, GRN), "90 ÷ 2 = 45"))
s += ans(m(ang("ADC", GRN) + " = 45^\\circ"))
E3.append(("आकृति 9.23 में, केन्द्र O वाले एक वृत्त पर तीन बिन्दु A, B और C इस प्रकार हैं कि " + m("\\angle BOC = 30^\\circ") + " तथा " + m("\\angle AOB = 60^\\circ")
           + " है। यदि चाप ABC के अतिरिक्त वृत्त पर D एक बिन्दु है, तो " + m("\\angle ADC") + " ज्ञात कीजिए।", s))

# ---------- Q2 (no figure): chord equal to the radius ----------
R32 = 115
P32 = {"O": (180, 140)}
P32["A"], P32["B"], P32["C"], P32["D"] = (on(P32["O"], R32, d) for d in (240, 300, 160, 258))
close1(dist(P32["A"], P32["B"]), R32, 1e-6)
close1(angle_at(P32["C"], P32["A"], P32["B"]), 30, 1e-6)
close1(angle_at(P32["D"], P32["A"], P32["B"]), 150, 1e-6)


def fig93_2(sol, cap):
    def ex(f, sol_):
        f.text(P32["D"][0] + 30, P32["D"][1] + 20, "150°", GRN, 12)
    mk = [("t", "OA", 1, RED), ("t", "OB", 1, RED), ("t", "AB", 1, RED), ("a", "AOB", 1, ORG, 24), ("l", "AOB", "60°", ORG, 36),
          ("a", "ACB", 1, BLU, 34), ("l", "ACB", "30°", BLU, 47), ("a", "ADB", 1, GRN, 9)]
    segs = [("OA", RED, 3), ("OB", RED, 3), ("AB", RED, 3), ("CA", BLU, 2.6), ("CB", BLU, 2.6), ("DA", GRN, 2.6), ("DB", GRN, 2.6)]
    lab = rl(P32, "O", "ABC", 15)
    lab.update({"O": (40, 16), "D": (262, 15)})
    return geo(360, 290, P32, segs, lab, mk, cap, circ=(("O", R32),), fills=(("AOB", ORG),), extra=ex, sol=sol)


s = given("केन्द्र O वाले वृत्त की जीवा AB, त्रिज्या के बराबर: " + m(sd("AB", RED) + " = " + sd("OA", RED) + " = " + sd("OB", RED))
          + "<br>C, दीर्घ चाप पर एक बिंदु; D, लघु चाप पर एक बिंदु",
          "(i) लघु चाप के बिंदु D पर अंतरित कोण " + m(ang("ADB", GRN)) + "<br>(ii) दीर्घ चाप के बिंदु C पर अंतरित कोण " + m(ang("ACB", BLU)))
s += NOFIG + solo(fig93_2(True, "हल की आकृति: OA = OB = AB लाल (समबाहु त्रिभुज), ∠AOB नारंगी, दीर्घ चाप पर ∠ACB नीला, लघु चाप पर ∠ADB हरा"))
s += key((RED, "OA = OB = AB"), (ORG, "∠AOB"), (BLU, "∠ACB (दीर्घ चाप)"), (GRN, "∠ADB (लघु चाप)"))
s += kh("चरण 1: " + m(ang("AOB", ORG) + " = 60^\\circ"))
s += num(1, EQUI)
s += p(m("\\triangle OAB") + " में " + m(sd("OA", RED) + " = " + sd("OB", RED) + " = " + sd("AB", RED)) + " (दो त्रिज्याएँ और त्रिज्या के बराबर जीवा), अतः यह समबाहु त्रिभुज है।")
s += chain((ang("AOB", ORG), dg(60, ORG) + " \\qquad \\ldots(1)", "समबाहु त्रिभुज का प्रत्येक कोण 60°"))
s += kh("(ii) दीर्घ चाप के बिंदु C पर कोण")
s += num(2, TH97)
s += p("लघु चाप AB केन्द्र पर " + m(ang("AOB", ORG)) + " और शेष भाग (दीर्घ चाप) के बिंदु C पर " + m(ang("ACB", BLU)) + " बनाता है।")
s += chain(("2" + ang("ACB", BLU), ang("AOB", ORG), "प्रमेय 9.7"),
           ("", dg(60, ORG), "(1) से"))
s += chain((ang("ACB", BLU), "\\dfrac{60^\\circ}{2}", "2 को पक्षांतर करने पर (गुणा → भाग)"),
           ("", dg(30, BLU) + " \\qquad \\ldots(2)", "60 ÷ 2 = 30"))
s += kh("(i) लघु चाप के बिंदु D पर कोण")
s += num(3, TH910)
s += p("A, C, B, D चारों वृत्त पर हैं, अतः ACBD एक चक्रीय चतुर्भुज है; इसमें ∠ACB और ∠ADB सम्मुख कोण हैं।")
s += chain((ang("ACB", BLU) + " + " + ang("ADB", GRN), "180" + DEG, "प्रमेय 9.10"),
           (dg(30, BLU) + " + " + ang("ADB", GRN), "180" + DEG, "(2) से"))
s += chain((ang("ADB", GRN), "180" + DEG + " - 30" + DEG, "30° को पक्षांतर करने पर (+ → −)"),
           ("", dg(150, GRN), "180 − 30 = 150"))
s += ans("(i) लघु चाप के किसी बिंदु पर अंतरित कोण " + m("= 150^\\circ") + " (ii) दीर्घ चाप के किसी बिंदु पर अंतरित कोण " + m("= 30^\\circ"))
E3.append(("किसी वृत्त की एक जीवा वृत्त की त्रिज्या के बराबर है। जीवा द्वारा लघु चाप के किसी बिन्दु पर अंतरित कोण ज्ञात कीजिए तथा दीर्घ चाप के किसी बिन्दु पर भी अंतरित कोण ज्ञात कीजिए।", s))

# ---------- Q3 (आकृति 9.24) ----------
R33 = 115
P33 = {"O": (180, 150)}
P33["P"], P33["R"], P33["Q"], P33["S"] = (on(P33["O"], R33, d) for d in (175, 15, 112, 270))
close1(angle_at(P33["Q"], P33["P"], P33["R"]), 100, 1e-6)
close1(angle_at(P33["S"], P33["P"], P33["R"]), 80, 1e-6)
close1(angle_at(P33["O"], P33["P"], P33["R"]), 160, 1e-6)
close1(angle_at(P33["P"], P33["O"], P33["R"]), 10, 1e-6)


def fig924(sol, cap):
    def ex(f, sol_):
        if sol_:
            f.text(P33["P"][0] + 78, P33["P"][1] + 1, "10°", PUR, 11)
    if sol:
        mk = [("a", "PQR", 1, ORG, 22), ("l", "PQR", "100°", ORG, 36), ("a", "PSR", 1, BLU, 26), ("l", "PSR", "80°", BLU, 40),
              ("a", "POR", 1, GRN, 13), ("a", "OPR", 1, PUR, 62), ("a", "ORP", 2, PUR, 62), ("t", "OP", 1, RED), ("t", "OR", 1, RED)]
        segs = ["PQ", "QR", ("PR", INK, 2), ("OP", RED, 2.8), ("OR", RED, 2.8), ("PS", BLU, 2.2, "6 4"), ("RS", BLU, 2.2, "6 4")]
        P = P33
        lab = rl(P33, "O", "PQRS", 15)
    else:
        mk = [("a", "PQR", 1, INK, 18)]
        segs = ["PQ", "QR", "PR", "OP", "OR"]
        P = {k: v for k, v in P33.items() if k != "S"}
        lab = rl(P33, "O", "PQR", 15)

        def ex(f, sol_):
            bl(f, P33, "PQR", "100°", 32)
    lab.update({"O": (270, 16)})
    return geo(360, 290, P, segs, lab, mk, cap, circ=(("O", R33),), extra=ex, sol=sol)


s = given("केन्द्र O वाले वृत्त पर बिंदु P, Q, R; " + m(ang("PQR", ORG) + " = 100^\\circ"), m(ang("OPR", PUR)))
s += figs(fig924, "आकृति 9.24", "दीर्घ चाप पर बिंदु S लिया (नीली डैश रेखाएँ); ∠POR हरा; त्रिज्याएँ OP = OR लाल")
s += p("रचना: दीर्घ चाप PR पर (Q के सामने वाले भाग पर) कोई बिंदु S लीजिए; SP और SR को मिलाइए।")
s += key((ORG, "∠PQR = 100°"), (BLU, "∠PSR"), (GRN, "∠POR"), (RED, "OP = OR"), (PUR, "∠OPR = ∠ORP"))
s += kh("चरण 1: " + m(ang("PSR", BLU)))
s += num(1, TH910)
s += chain((ang("PQR", ORG) + " + " + ang("PSR", BLU), "180" + DEG, "PQRS चक्रीय चतुर्भुज के सम्मुख कोण (प्रमेय 9.10)"),
           (dg(100, ORG) + " + " + ang("PSR", BLU), "180" + DEG, "मान रखने पर"))
s += chain((ang("PSR", BLU), "180" + DEG + " - 100" + DEG, "100° को पक्षांतर करने पर (+ → −)"),
           ("", dg(80, BLU), "180 − 100 = 80"))
s += kh("चरण 2: " + m(ang("POR", GRN)))
s += num(2, TH97)
s += chain((ang("POR", GRN), "2" + ang("PSR", BLU), "लघु चाप PR केन्द्र पर ∠POR और S पर ∠PSR बनाता है (प्रमेय 9.7)"),
           ("", "2 \\times 80^\\circ", "मान रखने पर"),
           ("", dg(160, GRN), "2 × 80 = 160"))
s += kh("चरण 3: " + m(ang("OPR", PUR)))
s += num(3, TH72)
s += chain((ang("OPR", PUR), ang("ORP", PUR) + " \\qquad \\ldots(1)", "OP = OR (त्रिज्याएँ), इनके सम्मुख कोण (प्रमेय 7.2)"))
s += num(4, ASUM)
s += chain((ang("OPR", PUR) + " + " + ang("ORP", PUR) + " + " + ang("POR", GRN), "180" + DEG, "△OPR के कोणों का योग"),
           (ang("OPR", PUR) + " + " + ang("OPR", PUR) + " + " + dg(160, GRN), "180" + DEG, "(1) से और ∠POR = 160°"),
           ("2" + ang("OPR", PUR) + " + 160" + DEG, "180" + DEG, "∠OPR + ∠OPR = 2∠OPR"))
s += chain(("2" + ang("OPR", PUR), "180" + DEG + " - 160" + DEG, "160° को पक्षांतर करने पर (+ → −)"),
           ("", "20" + DEG, "180 − 160 = 20"))
s += chain((ang("OPR", PUR), "\\dfrac{20^\\circ}{2}", "2 को पक्षांतर करने पर (गुणा → भाग)"),
           ("", dg(10, PUR), "20 ÷ 2 = 10"))
s += ans(m(ang("OPR", PUR) + " = 10^\\circ"))
E3.append(("आकृति 9.24 में, " + m("\\angle PQR = 100^\\circ") + " है, जहाँ P, Q तथा R, केन्द्र O वाले एक वृत्त पर स्थित बिन्दु हैं। " + m("\\angle OPR") + " ज्ञात कीजिए।", s))

# ---------- Q4 (आकृति 9.25) ----------
R34 = 112
P34 = {"O": (180, 150)}
P34["B"], P34["C"], P34["A"], P34["D"] = (on(P34["O"], R34, d) for d in (190, 350, 128, 75))
close1(angle_at(P34["B"], P34["A"], P34["C"]), 69, 1e-6)
close1(angle_at(P34["C"], P34["A"], P34["B"]), 31, 1e-6)
close1(angle_at(P34["D"], P34["B"], P34["C"]), 80, 1e-6)


def fig925(sol, cap):
    if sol:
        mk = [("a", "ABC", 1, ORG, 30), ("l", "ABC", "69°", ORG, 44), ("a", "ACB", 1, BLU, 40), ("l", "ACB", "31°", BLU, 56),
              ("a", "BAC", 1, GRN, 24), ("l", "BAC", "80°", GRN, 36), ("a", "BDC", 2, GRN, 26), ("l", "BDC", "80°", GRN, 42)]
        segs = [("AB", ORG, 2.6), ("AC", BLU, 2.6), ("BC", INK, 2.6), ("BD", GRN, 2.6), ("DC", GRN, 2.6)]
        ex = None
    else:
        mk = [("a", "ABC", 1, INK, 22), ("a", "ACB", 1, INK, 30)]
        segs = ["AB", "AC", "BC", "BD", "DC"]

        def ex(f, sol_):
            bl(f, P34, "ABC", "69°", 36)
            bl(f, P34, "ACB", "31°", 46)
    P = {k: v for k, v in P34.items() if k != "O"}
    return geo(360, 290, P, segs, rl(P34, "O", "ABCD", 15), mk, cap, extra=_circ34(ex), sol=sol,
               fills=(("ABC", BLU),))


def _circ34(ex):
    def f_(f, sol_):
        f.el.insert(0, f"<circle cx='{P34['O'][0]:.1f}' cy='{P34['O'][1]:.1f}' r='{R34}' fill='none' stroke='{CIR}' stroke-width='2.2'/>")
        if ex:
            ex(f, sol_)
    return f_


s = given("वृत्त पर बिंदु A, B, C, D; " + m(ang("ABC", ORG) + " = 69^\\circ") + ", " + m(ang("ACB", BLU) + " = 31^\\circ"), m(ang("BDC", GRN)))
s += figs(fig925, "आकृति 9.25", "∠ABC नारंगी, ∠ACB नीला; एक ही वृत्तखंड के कोण ∠BAC और ∠BDC हरे")
s += key((ORG, "∠ABC = 69°"), (BLU, "∠ACB = 31°"), (GRN, "∠BAC = ∠BDC"))
s += num(1, ASUM)
s += chain((ang("BAC", GRN) + " + " + ang("ABC", ORG) + " + " + ang("ACB", BLU), "180" + DEG, "△ABC के कोणों का योग"),
           (ang("BAC", GRN) + " + " + dg(69, ORG) + " + " + dg(31, BLU), "180" + DEG, "मान रखने पर"),
           (ang("BAC", GRN) + " + 100" + DEG, "180" + DEG, "69 + 31 = 100"))
s += chain((ang("BAC", GRN), "180" + DEG + " - 100" + DEG, "100° को पक्षांतर करने पर (+ → −)"),
           ("", dg(80, GRN) + " \\qquad \\ldots(1)", "180 − 100 = 80"))
s += num(2, TH98)
s += p("∠BAC और ∠BDC, दोनों जीवा BC द्वारा एक ही वृत्तखंड BADC में बने कोण हैं।")
s += chain((ang("BDC", GRN), ang("BAC", GRN), "प्रमेय 9.8"),
           ("", dg(80, GRN), "(1) से"))
s += ans(m(ang("BDC", GRN) + " = 80^\\circ"))
E3.append(("आकृति 9.25 में, " + m("\\angle ABC = 69^\\circ") + " और " + m("\\angle ACB = 31^\\circ") + " हो, तो " + m("\\angle BDC") + " ज्ञात कीजिए।", s))

# ---------- Q5 (आकृति 9.26) ----------
R35 = 150
P35 = {"O": (190, 170)}
P35["B"], P35["A"], P35["D"], P35["C"] = (on(P35["O"], R35, d) for d in (160, 122, 82, 20))
P35["E"] = inter(P35["A"], P35["C"], P35["B"], P35["D"])
close1(angle_at(P35["E"], P35["B"], P35["C"]), 130, 1e-6)
close1(angle_at(P35["C"], P35["E"], P35["D"]), 20, 1e-6)
close1(angle_at(P35["A"], P35["B"], P35["C"]), 110, 1e-6)


def fig926(sol, cap):
    if sol:
        mk = [("a", "BEC", 1, ORG, 16), ("l", "BEC", "130°", ORG, 30), ("a", "CED", 1, TEA, 14), ("l", "CED", "50°", TEA, 27, 11),
              ("a", "ECD", 1, BLU, 44), ("l", "ECD", "20°", BLU, 60), ("a", "EDC", 1, GRN, 14), ("l", "EDC", "110°", GRN, 30, 11),
              ("a", "BAC", 2, GRN, 18), ("l", "BAC", "110°", GRN, 32)]
        segs = [("BA", INK, 2.4), ("AE", INK, 2.4), ("EC", BLU, 2.8), ("BE", ORG, 2.8), ("ED", TEA, 2.8), ("DC", GRN, 2.8), ("BC", INK, 2)]
        ex = _circ35(None)
    else:
        mk = [("a", "BEC", 1, INK, 14), ("a", "ECD", 1, INK, 36)]
        segs = ["BA", "AC", "BD", "DC", "BC"]

        def ex0(f, sol_):
            bl(f, P35, "BEC", "130°", 27)
            bl(f, P35, "ECD", "20°", 50)
        ex = _circ35(ex0)
    P = {k: v for k, v in P35.items() if k != "O"}
    lab = rl(P35, "O", "ABCD", 15)
    lab["E"] = (90, 15)
    return geo(380, 345, P, segs, lab, mk, cap, extra=ex, sol=sol, fills=(("ECD", TEA),))


def _circ35(ex):
    def f_(f, sol_):
        f.el.insert(0, f"<circle cx='{P35['O'][0]:.1f}' cy='{P35['O'][1]:.1f}' r='{R35}' fill='none' stroke='{CIR}' stroke-width='2.2'/>")
        if ex:
            ex(f, sol_)
    return f_


s = given("वृत्त पर चार बिंदु A, B, C, D; AC और BD, बिंदु E पर प्रतिच्छेद करते हैं<br>" + m(ang("BEC", ORG) + " = 130^\\circ") + ", " + m(ang("ECD", BLU) + " = 20^\\circ"),
          m(ang("BAC", GRN)))
s += figs(fig926, "आकृति 9.26", "∠BEC नारंगी, ∠CED हरा-नीला, ∠ECD नीला; एक ही वृत्तखंड के कोण ∠BDC और ∠BAC हरे")
s += key((ORG, "∠BEC = 130°"), (TEA, "∠CED"), (BLU, "∠ECD = 20°"), (GRN, "∠EDC = ∠BDC = ∠BAC"))
s += kh("चरण 1: " + m(ang("CED", TEA)))
s += num(1, LINEAR)
s += chain((ang("BEC", ORG) + " + " + ang("CED", TEA), "180" + DEG, "किरण EC रेखा BD पर खड़ी है (रैखिक युग्म)"),
           (dg(130, ORG) + " + " + ang("CED", TEA), "180" + DEG, "मान रखने पर"))
s += chain((ang("CED", TEA), "180" + DEG + " - 130" + DEG, "130° को पक्षांतर करने पर (+ → −)"),
           ("", dg(50, TEA), "180 − 130 = 50"))
s += kh("चरण 2: " + m(ang("EDC", GRN)))
s += num(2, ASUM)
s += chain((ang("CED", TEA) + " + " + ang("ECD", BLU) + " + " + ang("EDC", GRN), "180" + DEG, "△ECD के कोणों का योग"),
           (dg(50, TEA) + " + " + dg(20, BLU) + " + " + ang("EDC", GRN), "180" + DEG, "मान रखने पर"),
           ("70" + DEG + " + " + ang("EDC", GRN), "180" + DEG, "50 + 20 = 70"))
s += chain((ang("EDC", GRN), "180" + DEG + " - 70" + DEG, "70° को पक्षांतर करने पर (+ → −)"),
           ("", dg(110, GRN), "180 − 70 = 110"))
s += p("E रेखाखंड BD पर है, इसलिए " + m(ang("BDC", GRN) + " = " + ang("EDC", GRN) + " = 110^\\circ") + "।")
s += kh("चरण 3: " + m(ang("BAC", GRN)))
s += num(3, TH98)
s += chain((ang("BAC", GRN), ang("BDC", GRN), "जीवा BC द्वारा एक ही वृत्तखंड में बने कोण (प्रमेय 9.8)"),
           ("", dg(110, GRN), "चरण 2 से"))
s += ans(m(ang("BAC", GRN) + " = 110^\\circ"))
E3.append(("आकृति 9.26 में, एक वृत्त पर A, B, C और D चार बिन्दु हैं। AC और BD एक बिन्दु E पर इस प्रकार प्रतिच्छेद करते हैं कि " + m("\\angle BEC = 130^\\circ")
           + " तथा " + m("\\angle ECD = 20^\\circ") + " है। " + m("\\angle BAC") + " ज्ञात कीजिए।", s))

# ---------- Q6 (no figure): cyclic quadrilateral, ∠DBC = 70°, ∠BAC = 30° ----------
R36 = 135
P36 = {"O": (190, 162)}
P36["A"], P36["B"], P36["C"], P36["D"] = (on(P36["O"], R36, d) for d in (150, 210, 270, 50))
P36["E"] = inter(P36["A"], P36["C"], P36["B"], P36["D"])
close1(angle_at(P36["B"], P36["D"], P36["C"]), 70, 1e-6)
close1(angle_at(P36["A"], P36["B"], P36["C"]), 30, 1e-6)
close1(dist(P36["A"], P36["B"]), dist(P36["B"], P36["C"]), 1e-6)
close1(angle_at(P36["C"], P36["B"], P36["D"]), 80, 1e-6)
close1(angle_at(P36["C"], P36["E"], P36["D"]), 50, 1e-6)


def fig93_6(sol, cap):
    mk = [("a", "DBC", 1, RED, 26), ("l", "DBC", "70°", RED, 40), ("a", "BAC", 1, BLU, 34), ("l", "BAC", "30°", BLU, 48),
          ("a", "BDC", 2, BLU, 34), ("l", "BDC", "30°", BLU, 48), ("a", "BCA", 3, BLU, 34), ("a", "ECD", 1, PUR, 30),
          ("ad", "BCD", ORG, 76), ("t", "AB", 1, GRN), ("t", "BC", 1, GRN)]
    segs = [("AB", GRN, 3), ("BC", GRN, 3), ("CD", INK, 2.4), ("DA", INK, 2.4), ("AC", INK, 2.2), ("BD", RED, 2.4)]

    def ex(f, sol_):
        f.el.insert(0, f"<circle cx='{P36['O'][0]:.1f}' cy='{P36['O'][1]:.1f}' r='{R36}' fill='none' stroke='{CIR}' stroke-width='2.2'/>")
        bl(f, P36, "BCA", "30°", 56, BLU, 12)
        bl(f, P36, "ECD", "50°", 52, PUR, 12)
    P = {k: v for k, v in P36.items() if k != "O"}
    lab = rl(P36, "O", "ABCD", 15)
    lab["E"] = (Fig.dir(P36["O"], P36["E"]) + 180, 15)
    return geo(380, 325, P, segs, lab, mk, cap, extra=ex, sol=sol)


s = given("ABCD एक चक्रीय चतुर्भुज है; विकर्ण AC और BD, बिंदु E पर प्रतिच्छेद करते हैं<br>" + m(ang("DBC", RED) + " = 70^\\circ") + ", " + m(ang("BAC", BLU) + " = 30^\\circ")
          + "<br>दूसरे भाग में: " + m(sd("AB", GRN) + " = " + sd("BC", GRN)),
          "(i) " + m(ang("BCD", ORG)) + "<br>(ii) " + m(sd("AB", GRN) + " = " + sd("BC", GRN)) + " हो तो " + m(ang("ECD", PUR)))
s += NOFIG + solo(fig93_6(True, "हल की आकृति: ∠DBC लाल; 30° के तीनों कोण नीले; ∠BCD नारंगी (डैश), ∠ECD बैंगनी; AB = BC हरी"))
s += key((RED, "∠DBC = 70°"), (BLU, "∠BAC = ∠BDC = ∠BCA = 30°"), (ORG, "∠BCD"), (PUR, "∠ECD"), (GRN, "AB = BC"))
s += kh("(i) " + m(ang("BCD", ORG)))
s += num(1, TH98)
s += chain((ang("BDC", BLU), ang("BAC", BLU), "जीवा BC द्वारा एक ही वृत्तखंड में बने कोण (प्रमेय 9.8)"),
           ("", dg(30, BLU) + " \\qquad \\ldots(1)", "दिया है"))
s += num(2, ASUM)
s += chain((ang("DBC", RED) + " + " + ang("BCD", ORG) + " + " + ang("BDC", BLU), "180" + DEG, "△BCD के कोणों का योग"),
           (dg(70, RED) + " + " + ang("BCD", ORG) + " + " + dg(30, BLU), "180" + DEG, "मान रखने पर ((1) से)"),
           ("100" + DEG + " + " + ang("BCD", ORG), "180" + DEG, "70 + 30 = 100"))
s += chain((ang("BCD", ORG), "180" + DEG + " - 100" + DEG, "100° को पक्षांतर करने पर (+ → −)"),
           ("", dg(80, ORG) + " \\qquad \\ldots(2)", "180 − 100 = 80"))
s += kh("(ii) " + m(sd("AB", GRN) + " = " + sd("BC", GRN)) + " हो, तो " + m(ang("ECD", PUR)))
s += num(3, TH72)
s += chain((ang("BCA", BLU), ang("BAC", BLU), "△ABC में AB = BC, इनके सम्मुख कोण (प्रमेय 7.2)"),
           ("", dg(30, BLU) + " \\qquad \\ldots(3)", "दिया है"))
s += chain((ang("ECD", PUR), ang("BCD", ORG) + " - " + ang("BCE", BLU), "CE (अर्थात् CA), ∠BCD के अंदर है"),
           ("", dg(80, ORG) + " - " + dg(30, BLU), "(2) से, और (3) से ∠BCE = ∠BCA = 30°"),
           ("", dg(50, PUR), "80 − 30 = 50"))
s += ans("(i) " + m(ang("BCD", ORG) + " = 80^\\circ") + " (ii) " + m(ang("ECD", PUR) + " = 50^\\circ"))
E3.append(("ABCD एक चक्रीय चतुर्भुज है जिसके विकर्ण एक बिन्दु E पर प्रतिच्छेद करते हैं। यदि " + m("\\angle DBC = 70^\\circ") + " और " + m("\\angle BAC = 30^\\circ")
           + " हो, तो " + m("\\angle BCD") + " ज्ञात कीजिए। पुनः यदि " + m("AB = BC") + " हो, तो " + m("\\angle ECD") + " ज्ञात कीजिए।", s))

# ---------- Q7 (no figure): diagonals are diameters -> rectangle ----------
R37 = 115
P37 = {"O": (180, 145)}
P37["A"], P37["B"], P37["C"], P37["D"] = (on(P37["O"], R37, d) for d in (140, 220, 320, 40))
for v_, a_, b_ in (("A", "D", "B"), ("B", "A", "C"), ("C", "B", "D"), ("D", "C", "A")):
    close1(angle_at(P37[v_], P37[a_], P37[b_]), 90, 1e-6)


def fig93_7(sol, cap):
    mk = [("r", "DAB", PUR), ("r", "ABC", PUR), ("r", "BCD", PUR), ("r", "CDA", PUR),
          ("t", "OA", 1, RED), ("t", "OC", 1, RED), ("t", "OB", 2, BLU), ("t", "OD", 2, BLU)]
    segs = ["AB", "BC", "CD", "DA", ("OA", RED, 3), ("OC", RED, 3), ("OB", BLU, 3), ("OD", BLU, 3)]
    lab = rl(P37, "O", "ABCD", 15)
    lab["O"] = (90, 16)
    return geo(360, 290, P37, segs, lab, mk, cap, circ=(("O", R37),), sol=sol)


s = given("ABCD एक चक्रीय चतुर्भुज है; विकर्ण AC और BD वृत्त के व्यास हैं (दोनों केन्द्र O से होकर जाते हैं)",
          "सिद्ध करना है: ABCD एक आयत है")
s += NOFIG + solo(fig93_7(True, "हल की आकृति: व्यास AC लाल (OA = OC), व्यास BD नीला (OB = OD), अर्धवृत्त के कोण बैंगनी"))
s += key((RED, "OA = OC (व्यास AC)"), (BLU, "OB = OD (व्यास BD)"), (PUR, "अर्धवृत्त के कोण 90°"))
s += kh("चरण 1: ABCD एक समांतर चतुर्भुज है")
s += num(1, RADII)
s += kk("", [(sd("OA", RED) + " = " + sd("OC", RED), "त्रिज्याएँ, अर्थात् O विकर्ण AC का मध्य-बिंदु है"),
             (sd("OB", BLU) + " = " + sd("OD", BLU), "त्रिज्याएँ, अर्थात् O विकर्ण BD का मध्य-बिंदु है")])
s += num(2, TH87)
s += p("विकर्ण AC और BD एक दूसरे को O पर समद्विभाजित करते हैं, इसलिए ABCD एक समांतर चतुर्भुज है।")
s += kh("चरण 2: एक कोण समकोण है")
s += num(3, SEMI)
s += kk("", [(ang("ABC", PUR) + " = 90^\\circ", "AC व्यास है, ∠ABC अर्धवृत्त का कोण है"),
             (ang("BAD", PUR) + " = 90^\\circ", "BD व्यास है, ∠BAD अर्धवृत्त का कोण है")])
s += p("(इसी प्रकार " + m(ang("BCD", PUR) + " = " + ang("CDA", PUR) + " = 90^\\circ") + " भी है।)")
s += num(4, D_RECT)
s += ans("ABCD एक समांतर चतुर्भुज है जिसका " + m("\\angle ABC = 90^\\circ") + " है, अतः ABCD एक आयत है। सिद्ध हुआ।")
E3.append(("यदि एक चक्रीय चतुर्भुज के विकर्ण उसके शीर्षों से जाने वाले वृत्त के व्यास हों, तो सिद्ध कीजिए कि वह एक आयत है।", s))

# ---------- Q8 (no figure): isosceles trapezium is cyclic ----------
P38 = {"A": (60, 235), "B": (300, 235), "C": (245, 95), "D": (115, 95)}
O38 = circum(P38["A"], P38["B"], P38["C"])
R38 = dist(O38, P38["A"])
close1(dist(O38, P38["D"]), R38, 1e-6)          # D lies on the circle through A, B, C
P38["M"] = foot(P38["D"], P38["A"], P38["B"])
P38["N"] = foot(P38["C"], P38["A"], P38["B"])
par_(P38["A"], P38["B"], P38["D"], P38["C"])
close1(dist(P38["A"], P38["D"]), dist(P38["B"], P38["C"]), 1e-6)
close1(angle_at(P38["B"], P38["A"], P38["C"]) + angle_at(P38["D"], P38["C"], P38["A"]), 180, 1e-6)   # ∠B + ∠D = 180


def fig93_8(sol, cap):
    mk = [("t", "AD", 1, RED), ("t", "BC", 1, RED), ("t", "DM", 2, BLU), ("t", "CN", 2, BLU), ("r", "AMD", PUR), ("r", "BNC", PUR),
          ("a", "DAB", 1, ORG, 30), ("a", "ABC", 1, ORG, 30), ("a", "ADC", 2, GRN, 24), ("p", "AB", 1, INK, .5), ("p", "DC", 1, INK, .5)]
    segs = [("AB", INK, 2.6), ("DC", INK, 2.6), ("AD", RED, 3), ("BC", RED, 3), ("DM", BLU, 2.6, "6 4"), ("CN", BLU, 2.6, "6 4")]

    def ex(f, sol_):
        f.el.insert(0, f"<circle cx='{O38[0]:.1f}' cy='{O38[1]:.1f}' r='{R38:.1f}' fill='none' stroke='{GRN}' stroke-width='1.8' stroke-dasharray='7 5'/>")
    lab = {"A": (200, 16), "B": (340, 16), "C": (40, 16), "D": (140, 16), "M": (270, 16), "N": (270, 16)}
    assert O38[1] + R38 < 340
    return geo(360, 345, P38, segs, lab, mk, cap, extra=ex, sol=sol, fills=(("AMD", BLU), ("BNC", ORG)))


s = given("ABCD एक समलंब है: " + m("AB \\parallel DC") + "<br>असमांतर भुजाएँ बराबर: " + m(sd("AD", RED) + " = " + sd("BC", RED)),
          "सिद्ध करना है: ABCD चक्रीय है")
s += NOFIG + solo(fig93_8(True, "हल की आकृति: AD = BC लाल, लम्ब DM = CN नीले, ∠A = ∠B नारंगी; हरा डैश वृत्त चारों शीर्षों से जाता है"))
s += p("रचना: D और C से AB पर लम्ब " + m("DM \\perp AB") + " और " + m("CN \\perp AB") + " खींचिए।")
s += key((RED, "AD = BC"), (BLU, "DM = CN"), (ORG, "∠A = ∠B"), (GRN, "∠D"), (PUR, "समकोण"))
s += kh("चरण 1: " + m(sd("DM", BLU) + " = " + sd("CN", BLU)))
s += num(1, CORR_C)
s += p(m(ang("DMA", PUR) + " = " + ang("CNA", PUR) + " = 90^\\circ") + " (संगत कोण), इसलिए " + m("DM \\parallel CN") + "। साथ ही " + m("DC \\parallel MN") + " (दिया है, MN रेखा AB का भाग है)।")
s += num(2, TH82)
s += kk("DMNC एक समांतर चतुर्भुज है (सम्मुख भुजाओं के दोनों युग्म समांतर), इसलिए", [(sd("DM", BLU) + " = " + sd("CN", BLU) + " \\quad (1)", "समांतर चतुर्भुज की सम्मुख भुजाएँ (प्रमेय 8.2)")])
s += kh("चरण 2: " + m(ang("A", ORG) + " = " + ang("B", ORG)))
s += num(3, RHS)
s += kk(m("\\triangle AMD") + " और " + m("\\triangle BNC") + " में,",
        [(ang("AMD", PUR) + " = " + ang("BNC", PUR) + " = 90^\\circ", "रचना से", "R", PUR),
         (sd("AD", RED) + " = " + sd("BC", RED), "दिया है (कर्ण)", "H", RED),
         (sd("DM", BLU) + " = " + sd("CN", BLU), "(1) से", "S", BLU)],
        ("\\triangle AMD \\cong \\triangle BNC", "RHS सर्वांगसमता नियम द्वारा"),
        [("A", "B"), ("M", "N"), ("D", "C")])
s += kk("", [(ang("DAB", ORG) + " = " + ang("CBA", ORG) + " \\quad (2)", "CPCT (∠DAM ↔ ∠CBN)")])
s += kh("चरण 3: " + m(ang("B", ORG) + " + " + ang("D", GRN) + " = 180^\\circ"))
s += num(4, INT)
s += chain((ang("A", ORG) + " + " + ang("D", GRN), "180" + DEG + " \\qquad \\ldots(3)", "AB ∥ DC, तिर्यक रेखा AD — एक ही ओर के अंतः कोण"))
s += chain((ang("B", ORG) + " + " + ang("D", GRN), ang("A", ORG) + " + " + ang("D", GRN), "(2) से ∠B = ∠A"),
           ("", "180" + DEG, "(3) से"))
s += num(5, TH911)
s += p("चतुर्भुज ABCD के सम्मुख कोणों के एक युग्म (∠B और ∠D) का योग " + m("180^\\circ") + " है।")
s += ans("प्रमेय 9.11 से समलंब ABCD चक्रीय है। सिद्ध हुआ।")
E3.append(("यदि एक समलंब की असमांतर भुजाएँ बराबर हों, तो सिद्ध कीजिए कि वह चक्रीय है।", s))

# ---------- Q9 (आकृति 9.27) ----------
O1, r1, O2, r2 = (132, 160), 105, (268, 150), 72
P39 = {}
P39["B"], P39["C"] = circ2(O1, r1, O2, r2)
_qa = Fig.pol(P39["B"], 14, 10)
P39["A"] = second(P39["B"], _qa, O1, r1)
P39["D"] = second(P39["B"], _qa, O2, r2)
_qp = Fig.pol(P39["B"], -38, 10)
P39["P"] = second(P39["B"], _qp, O1, r1)
P39["Q"] = second(P39["B"], _qp, O2, r2)
on_seg(P39["B"], P39["A"], P39["D"])
on_seg(P39["B"], P39["P"], P39["Q"])
close1(angle_at(P39["C"], P39["A"], P39["P"]), angle_at(P39["B"], P39["A"], P39["P"]), 1e-6)
close1(angle_at(P39["C"], P39["Q"], P39["D"]), angle_at(P39["B"], P39["Q"], P39["D"]), 1e-6)
close1(angle_at(P39["C"], P39["A"], P39["P"]), angle_at(P39["C"], P39["Q"], P39["D"]), 1e-6)


def fig927(sol, cap):
    def ex(f, sol_):
        for o_, rr in ((O1, r1), (O2, r2)):
            f.el.insert(0, f"<circle cx='{o_[0]:.1f}' cy='{o_[1]:.1f}' r='{rr}' fill='none' stroke='{CIR}' stroke-width='2.2'/>")
    if sol:
        mk = [("a", "ACP", 1, BLU, 34), ("a", "ABP", 1, BLU, 20), ("a", "QCD", 2, ORG, 34), ("a", "QBD", 2, ORG, 20)]
        segs = [("AD", TEA, 2.6), ("PQ", BROWN, 2.6), ("CA", BLU, 2.4), ("CP", BLU, 2.4), ("CQ", ORG, 2.4), ("CD", ORG, 2.4)]
    else:
        mk = [("a", "ACP", 1, INK, 26), ("a", "QCD", 1, INK, 26)]
        segs = ["AD", "PQ", "CA", "CP", "CQ", "CD"]
    lab = {"A": (Fig.dir(O1, P39["A"]), 15), "P": (Fig.dir(O1, P39["P"]), 15), "D": (Fig.dir(O2, P39["D"]), 15), "Q": (Fig.dir(O2, P39["Q"]), 15),
           "B": (100, 16), "C": (270, 16)}
    return geo(360, 290, P39, segs, lab, mk, cap, extra=ex, sol=sol)


s = given("दो वृत्त B और C पर प्रतिच्छेद करते हैं<br>B से जाने वाले रेखाखंड ABD और PBQ: A, P पहले वृत्त पर; D, Q दूसरे वृत्त पर",
          "सिद्ध करना है: " + m(ang("ACP", BLU) + " = " + ang("QCD", ORG)))
s += figs(fig927, "आकृति 9.27", "पहले वृत्त के एक ही वृत्तखंड के कोण नीले, दूसरे वृत्त के एक ही वृत्तखंड के कोण नारंगी")
s += key((BLU, "∠ACP = ∠ABP (पहला वृत्त)"), (ORG, "∠QCD = ∠QBD (दूसरा वृत्त)"), (TEA, "रेखा ABD"), (BROWN, "रेखा PBQ"))
s += num(1, TH98)
s += chain((ang("ACP", BLU), ang("ABP", BLU) + " \\qquad \\ldots(1)", "पहले वृत्त में जीवा AP द्वारा एक ही वृत्तखंड में बने कोण (प्रमेय 9.8)"))
s += chain((ang("QCD", ORG), ang("QBD", ORG) + " \\qquad \\ldots(2)", "दूसरे वृत्त में जीवा QD द्वारा एक ही वृत्तखंड में बने कोण (प्रमेय 9.8)"))
s += num(2, VOPP)
s += chain((ang("ABP", BLU), ang("QBD", ORG) + " \\qquad \\ldots(3)", "रेखाएँ AD और PQ, B पर प्रतिच्छेद करती हैं — शीर्षाभिमुख कोण"))
s += chain((ang("ACP", BLU), ang("ABP", BLU), "(1) से"),
           ("", ang("QBD", ORG), "(3) से"),
           ("", ang("QCD", ORG), "(2) से"))
s += ans(m(ang("ACP", BLU) + " = " + ang("QCD", ORG)) + "। सिद्ध हुआ।")
E3.append(("दो वृत्त दो बिन्दुओं B और C पर प्रतिच्छेद करते हैं। B से जाने वाले दो रेखाखंड ABD और PBQ वृत्तों को A, D और P, Q पर क्रमशः प्रतिच्छेद करते हुए खींचे गए हैं "
           "(देखिए आकृति 9.27)। सिद्ध कीजिए कि " + m("\\angle ACP = \\angle QCD") + " है।", s))

# ---------- Q10 (no figure): circles on two sides as diameters meet on the third side ----------
P310 = {"A": (190, 60), "B": (80, 255), "C": (330, 255)}
P310["D"] = foot(P310["A"], P310["B"], P310["C"])
M1, M2 = mid(P310["A"], P310["B"]), mid(P310["A"], P310["C"])
q1, q2 = dist(P310["A"], P310["B"]) / 2, dist(P310["A"], P310["C"]) / 2
close1(dist(M1, P310["D"]), q1, 1e-6)
close1(dist(M2, P310["D"]), q2, 1e-6)
on_seg(P310["D"], P310["B"], P310["C"])


def fig93_10(sol, cap):
    def ex(f, sol_):
        f.el.insert(0, f"<circle cx='{M1[0]:.1f}' cy='{M1[1]:.1f}' r='{q1:.1f}' fill='none' stroke='{BLU}' stroke-width='2'/>")
        f.el.insert(0, f"<circle cx='{M2[0]:.1f}' cy='{M2[1]:.1f}' r='{q2:.1f}' fill='none' stroke='{ORG}' stroke-width='2'/>")
    mk = [("r", "ADB", BLU), ("r", "ADC", ORG)]
    segs = [("AB", BLU, 3), ("AC", ORG, 3), ("BD", INK, 2.6), ("DC", INK, 2.6), ("AD", PUR, 2.6)]
    lab = {"A": (90, 15), "B": (200, 16), "C": (340, 16), "D": (270, 16)}
    assert M1[0] - q1 > 4 and M2[0] + q2 < 386 and M2[1] + q2 < 296 and M2[1] - q2 > 4 and M1[1] - q1 > 4
    return geo(390, 300, P310, segs, lab, mk, cap, extra=ex, sol=sol)


s = given(m("\\triangle ABC") + "; भुजा AB को व्यास मानकर वृत्त (नीला) और भुजा AC को व्यास मानकर वृत्त (नारंगी) खींचे गए<br>दोनों वृत्त A और D पर प्रतिच्छेद करते हैं",
          "सिद्ध करना है: D तीसरी भुजा BC पर स्थित है")
s += NOFIG + solo(fig93_10(True, "हल की आकृति: AB व्यास वाला वृत्त नीला, AC व्यास वाला वृत्त नारंगी; AD बैंगनी"))
s += p("रचना: AD को मिलाइए; BD और DC को मिलाइए।")
s += key((BLU, "AB व्यास, ∠ADB"), (ORG, "AC व्यास, ∠ADC"), (PUR, "AD"))
s += num(1, SEMI)
s += kk("", [(ang("ADB", BLU) + " = 90^\\circ \\quad (1)", "AB व्यास वाले वृत्त के अर्धवृत्त का कोण"),
             (ang("ADC", ORG) + " = 90^\\circ \\quad (2)", "AC व्यास वाले वृत्त के अर्धवृत्त का कोण")])
s += chain((ang("ADB", BLU) + " + " + ang("ADC", ORG), "90" + DEG + " + 90" + DEG, "(1) और (2) से"),
           ("", "180" + DEG, "90 + 90 = 180"))
s += num(2, LINEAR2)
s += p("∠ADB और ∠ADC आसन्न कोण हैं (उभयनिष्ठ भुजा DA) और इनका योग " + m("180^\\circ") + " है, इसलिए अउभयनिष्ठ भुजाएँ DB और DC एक ही रेखा में हैं, अर्थात् B, D, C संरेख हैं।")
s += ans("वृत्तों का प्रतिच्छेद बिंदु D तीसरी भुजा BC पर स्थित है। सिद्ध हुआ।")
E3.append(("यदि किसी त्रिभुज की दो भुजाओं को व्यास मानकर वृत्त खींचे जाएँ, तो सिद्ध कीजिए कि इन वृत्तों का प्रतिच्छेद बिन्दु तीसरी भुजा पर स्थित है।", s))

# ---------- Q11 (no figure): right triangles ABC, ADC on common hypotenuse AC ----------
R311 = 120
P311 = {"O": (190, 155)}
P311["A"], P311["C"] = on(P311["O"], R311, 180), on(P311["O"], R311, 0)
P311["B"], P311["D"] = on(P311["O"], R311, 245), on(P311["O"], R311, 68)
close1(angle_at(P311["B"], P311["A"], P311["C"]), 90, 1e-6)
close1(angle_at(P311["D"], P311["A"], P311["C"]), 90, 1e-6)
close1(angle_at(P311["A"], P311["C"], P311["D"]), angle_at(P311["B"], P311["C"], P311["D"]), 1e-6)


def fig93_11(sol, cap):
    def ex(f, sol_):
        f.el.insert(0, f"<circle cx='{P311['O'][0]:.1f}' cy='{P311['O'][1]:.1f}' r='{R311}' fill='none' stroke='{GRN}' stroke-width='1.8' stroke-dasharray='7 5'/>")
    mk = [("r", "ABC", PUR), ("r", "ADC", PUR), ("a", "CAD", 1, BLU, 40), ("a", "CBD", 1, BLU, 40)]
    segs = [("AB", INK, 2.6), ("BC", INK, 2.6), ("CD", ORG, 3), ("DA", INK, 2.6), ("AC", RED, 3), ("BD", INK, 2)]
    lab = rl(P311, "O", "ABCD", 15)
    P = {k: v for k, v in P311.items() if k != "O"}
    return geo(380, 310, P, segs, lab, mk, cap, extra=ex, sol=sol)


s = given("समकोण त्रिभुज ABC और ADC, उभयनिष्ठ कर्ण AC: " + m(ang("ABC", PUR) + " = " + ang("ADC", PUR) + " = 90^\\circ"),
          "सिद्ध करना है: " + m(ang("CAD", BLU) + " = " + ang("CBD", BLU)))
s += NOFIG + solo(fig93_11(True, "हल की आकृति: कर्ण AC लाल, समकोण बैंगनी; जीवा CD (नारंगी) द्वारा बने कोण नीले; हरा डैश वृत्त A, B, C, D से जाता है"))
s += key((RED, "उभयनिष्ठ कर्ण AC"), (PUR, "∠B = ∠D = 90°"), (ORG, "जीवा CD"), (BLU, "∠CAD = ∠CBD"))
s += kh("चरण 1: A, B, C, D एक वृत्त पर हैं")
s += chain((ang("ABC", PUR) + " + " + ang("ADC", PUR), "90" + DEG + " + 90" + DEG, "दिया है"),
           ("", "180" + DEG, "90 + 90 = 180"))
s += num(1, TH911)
s += p("चतुर्भुज ABCD (B और D, AC के विपरीत ओर) के सम्मुख कोणों ∠B और ∠D का योग " + m("180^\\circ") + " है, इसलिए ABCD चक्रीय है।")
s += tp("यदि B और D, AC के एक ही ओर हों, तो " + m("\\angle ABC = \\angle ADC = 90^\\circ") + ", अर्थात् AC दोनों बिंदुओं पर बराबर कोण बनाता है; प्रमेय 9.9 से तब भी A, B, C, D एक वृत्त पर होंगे।")
s += num(2, TH99)
s += kh("चरण 2: " + m(ang("CAD", BLU) + " = " + ang("CBD", BLU)))
s += num(3, TH98)
s += chain((ang("CAD", BLU), ang("CBD", BLU), "जीवा CD द्वारा एक ही वृत्तखंड में बने कोण (प्रमेय 9.8)"))
s += ans(m(ang("CAD", BLU) + " = " + ang("CBD", BLU)) + "। सिद्ध हुआ।")
E3.append(("उभयनिष्ठ कर्ण AC वाले दो समकोण त्रिभुज ABC और ADC हैं। सिद्ध कीजिए कि " + m("\\angle CAD = \\angle CBD") + " है।", s))

# ---------- Q12 (no figure): cyclic parallelogram is a rectangle ----------
R312 = 115
P312 = {"O": (180, 145)}
P312["A"], P312["B"], P312["C"], P312["D"] = (on(P312["O"], R312, d) for d in (215, 325, 35, 145))
pgram(P312, "A", "B", "C", "D")
close1(angle_at(P312["A"], P312["B"], P312["D"]), 90, 1e-6)


def fig93_12(sol, cap):
    mk = [("a", "DAB", 1, ORG, 22), ("a", "BCD", 1, ORG, 22), ("p", "AB", 1, INK, .5), ("p", "DC", 1, INK, .5), ("p", "AD", 2, INK, .5), ("p", "BC", 2, INK, .5)]
    segs = ["AB", "BC", "CD", "DA"]
    lab = rl(P312, "O", "ABCD", 15)
    P = {k: v for k, v in P312.items() if k != "O"}

    def ex(f, sol_):
        f.el.insert(0, f"<circle cx='{P312['O'][0]:.1f}' cy='{P312['O'][1]:.1f}' r='{R312}' fill='none' stroke='{CIR}' stroke-width='2.2'/>")
        bl(f, P312, "DAB", "∠A", 38, ORG, 12)
        bl(f, P312, "BCD", "∠C", 38, ORG, 12)
    return geo(360, 290, P, segs, lab, mk, cap, extra=ex, sol=sol, fills=(("ABCD", BLU),))


s = given("ABCD एक समांतर चतुर्भुज है जिसके चारों शीर्ष एक वृत्त पर हैं (चक्रीय समांतर चतुर्भुज)", "सिद्ध करना है: ABCD एक आयत है")
s += NOFIG + solo(fig93_12(True, "हल की आकृति: समांतर भुजाओं पर तीर-चिह्न; सम्मुख कोण ∠A और ∠C नारंगी"))
s += key((ORG, "∠A, ∠C (सम्मुख कोण)"))
s += num(1, TH84)
s += chain((ang("A", ORG), ang("C", ORG) + " \\qquad \\ldots(1)", "समांतर चतुर्भुज के सम्मुख कोण (प्रमेय 8.4)"))
s += num(2, TH910)
s += chain((ang("A", ORG) + " + " + ang("C", ORG), "180" + DEG, "चक्रीय चतुर्भुज के सम्मुख कोण (प्रमेय 9.10)"),
           (ang("A", ORG) + " + " + ang("A", ORG), "180" + DEG, "(1) से ∠C = ∠A रखने पर"),
           ("2" + ang("A", ORG), "180" + DEG, "∠A + ∠A = 2∠A"))
s += chain((ang("A", ORG), "\\dfrac{180^\\circ}{2}", "2 को पक्षांतर करने पर (गुणा → भाग)"),
           ("", dg(90, ORG), "180 ÷ 2 = 90"))
s += num(3, D_RECT)
s += ans("समांतर चतुर्भुज ABCD का " + m("\\angle A = 90^\\circ") + " है, अतः चक्रीय समांतर चतुर्भुज ABCD एक आयत है। सिद्ध हुआ।")
E3.append(("सिद्ध कीजिए कि चक्रीय समांतर चतुर्भुज आयत होता है।", s))

# ---------------------------------------------------------------------
assert (len(E1), len(E2), len(E3)) == (2, 6, 12)
E1 = [(qt(a), b) for a, b in E1]
E2 = [(qt(a), b) for a, b in E2]
E3 = [(qt(a), b) for a, b in E3]
for E in (E1, E2, E3):
    check_tex(E)
SUB = "कक्षा 9 गणित · अध्याय 9: " + CH + " · {} प्रश्न"
page(BASE, 9, CH, "exercise-9-1", "प्रश्नावली 9.1", SUB.format(len(E1)), E1,
     ("/hi/class-09/maths/chapter-08/exercise-8-2/", "प्रश्नावली 8.2"), (BASE + "exercise-9-2/", "प्रश्नावली 9.2"), css=CSS + EXTRA_CSS, boards=BOARDS9)
page(BASE, 9, CH, "exercise-9-2", "प्रश्नावली 9.2", SUB.format(len(E2)), E2,
     (BASE + "exercise-9-1/", "प्रश्नावली 9.1"), (BASE + "exercise-9-3/", "प्रश्नावली 9.3"), css=CSS + EXTRA_CSS, boards=BOARDS9)
page(BASE, 9, CH, "exercise-9-3", "प्रश्नावली 9.3", SUB.format(len(E3)), E3,
     (BASE + "exercise-9-2/", "प्रश्नावली 9.2"), (BASE, "अध्याय 9"), css=CSS + EXTRA_CSS, boards=BOARDS9)
print("ok")
