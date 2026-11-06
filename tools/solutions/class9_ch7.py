#!/usr/bin/env python3
"""Class 9 Maths, Chapter 7 (त्रिभुज): Exercises 7.1, 7.2 and 7.3, Hindi medium.
Rationalised book (2023-24 onward, iemh107 'Reprint 2025-26'): 7.1 (8 questions), 7.2 (8), 7.3 (5) are kept unchanged
(same question numbers and figure numbers 7.16-7.23, 7.30-7.34, 7.39-7.40); old exercises 7.4 (inequalities) and
7.5 (optional) were removed.  Question text and figures copied from NCERT Hindi PDF ihmh107 (archive.org, 2021-22 print).
Style as chapter 6: every side/angle has one colour in the solution figure and the same colour in the working;
equal sides carry the same number of ticks, equal angles the same number of arcs.
Run from repo root: python3 tools/solutions/class9_ch7.py
"""
import sys, pathlib, math
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from common import *  # noqa
from mixed_cells import *  # noqa

BASE = "/hi/class-09/maths/chapter-07/"
CH = "त्रिभुज"
BOARDS9 = ("यह हल <b>MP Board (MPBSE)</b> कक्षा 9 गणित की पाठ्यपुस्तक के अध्याय 7 ‘त्रिभुज’ के अनुसार है।")
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
        self.id, self.W, self.H, self.bg, self.el, self.top, self.marks = f"f7{Fig.n}", W, H, [], [], [], {}

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


def geo(W, H, P, segs, labels, marks, cap, fills=(), extra=None, sol=True):
    """Generic figure.  P: name -> (x, y).  segs: 'AB' or ('AB', colour, width, dash).
    marks: ('t','AB',n,col) ticks · ('q','AB',col) square mark · ('a','BAC',n,col,r) angle arcs at the middle letter ·
           ('r','ADB',col) right-angle box at D · ('l','BAC',text,col,r) angle label.
    In the textbook version (sol=False) every mark is drawn in INK and no fills/colours are used."""
    f = Fig(W, H)
    for nm in labels:
        x_, y_ = P[nm]
        assert 14 < x_ < W - 14 and 14 < y_ < H - 14, ("point near/outside canvas", cap, nm, P[nm])
    if sol:
        for pts, col in fills:
            f.poly([P[x] for x in pts], col)
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
        f.lab(P[nm], nm, deg, d)
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


# =====================================================================
# Exercise 7.1
# =====================================================================
E1 = []

# ---------- Q1 (आकृति 7.16) ----------
P1 = {"A": (55, 150), "B": (305, 150)}
P1["C"] = (190, 45)
P1["D"] = (190, 255)
assert all(15 < x < 345 and 15 < y < 285 for x, y in P1.values())
close1(dist(P1["A"], P1["C"]), dist(P1["A"], P1["D"]), 1e-6)
close1(angle_at(P1["A"], P1["C"], P1["B"]), angle_at(P1["A"], P1["D"], P1["B"]), 1e-6)


def fig716(sol, cap):
    mk = [("t", "AC", 1, RED), ("t", "AD", 1, RED), ("a", "CAB", 1, BLU, 24), ("a", "BAD", 1, BLU, 24)]
    if sol:
        mk += [("t", "BC", 2, ORG), ("t", "BD", 2, ORG)]
    segs = [("AC", RED, 3), ("AD", RED, 3), ("AB", GRN, 3.4), ("CB", ORG, 3, "7 4"), ("DB", ORG, 3, "7 4")] if sol else ["AC", "AD", "AB", "CB", "DB"]
    return geo(360, 300, P1, segs, {"A": (180, 16), "B": (0, 16), "C": (90, 15), "D": (270, 15)}, mk, cap,
               fills=(("ABC", BLU), ("ABD", ORG)), sol=sol)


s = given("चतुर्भुज " + m("ACBD") + " में<br>" + m(sd("AC", RED) + " = " + sd("AD", RED)) + "<br>"
          + m("AB") + ", " + m("\\angle A") + " को समद्विभाजित करता है, अर्थात् " + m(ang("CAB", BLU) + " = " + ang("DAB", BLU)),
          "(i) सिद्ध करना है: " + m("\\triangle ABC \\cong \\triangle ABD") + "<br>(ii) " + m(sd("BC", ORG)) + " और " + m(sd("BD", ORG)) + " का संबंध")
s += figs(fig716, "आकृति 7.16", "बराबर भुजाएँ लाल (एक निशान), बराबर कोण नीले, उभयनिष्ठ भुजा AB हरी")
s += key((RED, "AC = AD"), (BLU, "∠CAB = ∠DAB"), (GRN, "AB उभयनिष्ठ"), (ORG, "BC, BD (सिद्ध करना है)"))
s += kh("(i) " + m("\\triangle ABC \\cong \\triangle ABD"))
s += num(1, SAS)
s += kk(m("\\triangle ABC") + " और " + m("\\triangle ABD") + " में,",
        [(sd("AC", RED) + " = " + sd("AD", RED) + " \\quad (1)", "दिया है", "S", RED),
         (ang("CAB", BLU) + " = " + ang("DAB", BLU) + " \\quad (2)", "AB, ∠A को समद्विभाजित करता है", "A", BLU),
         (sd("AB", GRN) + " = " + sd("AB", GRN) + " \\quad (3)", "उभयनिष्ठ भुजा", "S", GRN)],
        ("\\triangle ABC \\cong \\triangle ABD", "(1), (2), (3) से, SAS सर्वांगसमता नियम द्वारा"),
        [("A", "A"), ("B", "B"), ("C", "D")])
s += tp("ध्यान दें: कोण " + m(ang("CAB", BLU)) + " भुजाओं " + m(sd("AC", RED)) + " और " + m(sd("AB", GRN)) + " के बीच का (अंतर्गत) कोण है, और "
        + m(ang("DAB", BLU)) + " भुजाओं " + m(sd("AD", RED)) + " और " + m(sd("AB", GRN)) + " के बीच का कोण है।")
s += kh("(ii) " + m(sd("BC", ORG)) + " और " + m(sd("BD", ORG)) + " के बारे में")
s += num(2, CPCT)
s += kk("", [(sd("BC", ORG) + " = " + sd("BD", ORG), "CPCT (शीर्ष C ↔ D, इसलिए भुजा BC ↔ BD)")])
s += ans("(i) " + m("\\triangle ABC \\cong \\triangle ABD") + " (SAS) (ii) " + m(sd("BC", ORG) + " = " + sd("BD", ORG)) + ", अर्थात् BC और BD बराबर हैं।")
E1.append(("चतुर्भुज " + m("ACBD") + " में, " + m("AC = AD") + " है और " + m("AB") + " कोण " + m("A") + " को समद्विभाजित करता है (देखिए आकृति 7.16)। दर्शाइए कि "
           + m("\\triangle ABC \\cong \\triangle ABD") + " है। " + m("BC") + " और " + m("BD") + " के बारे में आप क्या कह सकते हैं?", s))

# ---------- Q2 (आकृति 7.17) ----------
th2, L2 = 104, 150
A2, B2 = (130, 42), (82, 192)
dAB = Fig.dir(A2, B2)
D2 = Fig.pol(A2, dAB + th2, L2)
C2 = Fig.pol(B2, Fig.dir(B2, A2) - th2, L2)
P2 = {"A": A2, "B": B2, "C": C2, "D": D2}
close1(dist(A2, D2), dist(B2, C2), 1e-6)
close1(angle_at(A2, D2, B2), angle_at(B2, C2, A2), 1e-6)


def fig717(sol, cap):
    mk = [("t", "AD", 1, RED), ("t", "BC", 1, RED), ("a", "DAB", 1, BLU, 24), ("a", "CBA", 1, BLU, 24)]
    if sol:
        mk += [("t", "BD", 2, ORG, .62), ("t", "AC", 2, ORG, .62), ("a", "ABD", 2, PUR, 40), ("a", "BAC", 2, PUR, 40)]
    segs = ([("AD", RED, 3), ("BC", RED, 3), ("AB", GRN, 3.4), ("BD", ORG, 2.6), ("AC", ORG, 2.6), ("DC", None)] if sol
            else ["AD", "BC", "AB", "BD", "AC", "DC"])
    return geo(360, 305, P2, segs, {"A": (110, 16), "B": (190, 16), "C": (270, 16), "D": (20, 16)}, mk, cap,
               fills=(("ABD", BLU), ("BAC", ORG)), sol=sol)


s = given("चतुर्भुज " + m("ABCD") + " में<br>" + m(sd("AD", RED) + " = " + sd("BC", RED)) + "<br>" + m(ang("DAB", BLU) + " = " + ang("CBA", BLU)),
          "सिद्ध करना है:<br>(i) " + m("\\triangle ABD \\cong \\triangle BAC") + "<br>(ii) " + m(sd("BD", ORG) + " = " + sd("AC", ORG))
          + "<br>(iii) " + m(ang("ABD", PUR) + " = " + ang("BAC", PUR)))
s += figs(fig717, "आकृति 7.17", "AD = BC लाल, ∠DAB = ∠CBA नीले, AB हरी (उभयनिष्ठ)")
s += key((RED, "AD = BC"), (BLU, "∠DAB = ∠CBA"), (GRN, "AB उभयनिष्ठ"), (ORG, "BD, AC"), (PUR, "∠ABD, ∠BAC"))
s += kh("(i) " + m("\\triangle ABD \\cong \\triangle BAC"))
s += num(1, SAS)
s += kk(m("\\triangle ABD") + " और " + m("\\triangle BAC") + " में,",
        [(sd("AD", RED) + " = " + sd("BC", RED) + " \\quad (1)", "दिया है", "S", RED),
         (ang("DAB", BLU) + " = " + ang("CBA", BLU) + " \\quad (2)", "दिया है", "A", BLU),
         (sd("AB", GRN) + " = " + sd("BA", GRN) + " \\quad (3)", "उभयनिष्ठ भुजा", "S", GRN)],
        ("\\triangle ABD \\cong \\triangle BAC", "(1), (2), (3) से, SAS सर्वांगसमता नियम द्वारा"),
        [("A", "B"), ("B", "A"), ("D", "C")])
s += num(2, CPCT)
s += kh("(ii) " + m(sd("BD", ORG) + " = " + sd("AC", ORG)))
s += kk("", [(sd("BD", ORG) + " = " + sd("AC", ORG), "CPCT (B ↔ A, D ↔ C, इसलिए BD ↔ AC)")])
s += kh("(iii) " + m(ang("ABD", PUR) + " = " + ang("BAC", PUR)))
s += kk("", [(ang("ABD", PUR) + " = " + ang("BAC", PUR), "CPCT (शीर्ष B पर का कोण ↔ शीर्ष A पर का कोण)")])
s += ans("(i) " + m("\\triangle ABD \\cong \\triangle BAC") + " (SAS) (ii) " + m(sd("BD", ORG) + " = " + sd("AC", ORG)) + " (iii) "
         + m(ang("ABD", PUR) + " = " + ang("BAC", PUR)) + " — तीनों सिद्ध हुए।")
E1.append(("ABCD एक चतुर्भुज है, जिसमें " + m("AD = BC") + " और " + m("\\angle DAB = \\angle CBA") + " है (देखिए आकृति 7.17)। सिद्ध कीजिए कि "
           + "(i) " + m("\\triangle ABD \\cong \\triangle BAC") + " (ii) " + m("BD = AC") + " (iii) " + m("\\angle ABD = \\angle BAC") + "।", s))

# ---------- Q3 (आकृति 7.18) ----------
P3 = {"B": (200, 40), "C": (325, 40), "A": (200, 220), "D": (75, 220)}
P3["O"] = inter(P3["C"], P3["D"], P3["A"], P3["B"])
close1(dist(P3["O"], P3["A"]), dist(P3["O"], P3["B"]), 1e-6)


def fig718(sol, cap):
    mk = [("t", "BC", 1, RED), ("t", "AD", 1, RED), ("r", "ABC", PUR), ("r", "DAB", PUR)]
    if sol:
        mk += [("a", "BOC", 1, BLU, 22), ("a", "AOD", 1, BLU, 22), ("t", "OB", 2, ORG), ("t", "OA", 2, ORG)]
    segs = ([("BC", RED, 3), ("AD", RED, 3), ("OB", ORG, 3), ("OA", ORG, 3), "CD"] if sol else ["BC", "AD", "AB", "CD"])
    return geo(400, 260, P3, segs, {"A": (300, 16), "B": (110, 16), "C": (0, 16), "D": (180, 16), "O": (5, 18)}, mk, cap,
               fills=(("BOC", BLU), ("AOD", ORG)), sol=sol)


s = given(m("AD \\perp AB") + ", " + m("BC \\perp AB") + "<br>" + m(sd("AD", RED) + " = " + sd("BC", RED)) + "<br>" + m("CD") + ", " + m("AB") + " को " + m("O") + " पर काटता है।",
          "सिद्ध करना है: " + m(sd("OA", ORG) + " = " + sd("OB", ORG)) + " (अर्थात् CD, AB को समद्विभाजित करता है)")
s += figs(fig718, "आकृति 7.18", "समकोण बैंगनी, शीर्षाभिमुख कोण नीले, AD = BC लाल")
s += key((RED, "AD = BC"), (PUR, "समकोण"), (BLU, "∠BOC = ∠AOD"), (ORG, "OB, OA"))
s += num(1, VOPP)
s += kk("पहले कोणों के युग्म:", [
    (ang("CBO", PUR) + " = " + dg(90, PUR), "BC ⊥ AB"),
    (ang("DAO", PUR) + " = " + dg(90, PUR), "AD ⊥ AB"),
    (ang("CBO", PUR) + " = " + ang("DAO", PUR) + " \\quad (1)", "दोनों 90° के बराबर हैं"),
    (ang("BOC", BLU) + " = " + ang("AOD", BLU) + " \\quad (2)", "शीर्षाभिमुख कोण — रेखाएँ AB और CD, O पर प्रतिच्छेद करती हैं")])
s += num(2, AAS)
s += kk(m("\\triangle BOC") + " और " + m("\\triangle AOD") + " में,",
        [(ang("CBO", PUR) + " = " + ang("DAO", PUR), "(1) से", "A", PUR),
         (ang("BOC", BLU) + " = " + ang("AOD", BLU), "(2) से", "A", BLU),
         (sd("BC", RED) + " = " + sd("AD", RED), "दिया है", "S", RED)],
        ("\\triangle BOC \\cong \\triangle AOD", "AAS सर्वांगसमता नियम द्वारा"),
        [("B", "A"), ("O", "O"), ("C", "D")])
s += tp("AAS में भुजा, बराबर कोणों की संगत भुजा होनी चाहिए: " + m(sd("BC", RED)) + " कोण " + m(ang("BOC", BLU)) + " के सामने है और "
        + m(sd("AD", RED)) + " कोण " + m(ang("AOD", BLU)) + " के सामने है ✔")
s += num(3, CPCT)
s += kk("", [(sd("OB", ORG) + " = " + sd("OA", ORG), "CPCT (B ↔ A, इसलिए OB ↔ OA)")])
s += p("अतः " + m("O") + ", रेखाखंड " + m("AB") + " का मध्य-बिंदु है, अर्थात् " + m("CD") + ", " + m("AB") + " को समद्विभाजित करता है।")
s += ans(m(sd("OA", ORG) + " = " + sd("OB", ORG)) + ", इसलिए CD, रेखाखंड AB को समद्विभाजित करता है। सिद्ध हुआ।")
E1.append(("एक रेखाखंड " + m("AB") + " पर " + m("AD") + " और " + m("BC") + " दो बराबर लंब रेखाखंड हैं (देखिए आकृति 7.18)। दर्शाइए कि " + m("CD")
           + ", रेखाखंड " + m("AB") + " को समद्विभाजित करता है।", s))

# ---------- Q4 (आकृति 7.19) ----------
yl, ym, sx = 75, 175, 0.57
P4 = {"A": (140, yl), "D": (262, yl)}
P4["B"] = (P4["A"][0] - sx * (ym - yl), ym)
P4["C"] = (P4["D"][0] - sx * (ym - yl), ym)
close1(dist(P4["A"], P4["B"]), dist(P4["D"], P4["C"]), 1e-6)


def fig719(sol, cap):
    def ext(f, sol_):
        cl = (lambda c: c) if sol_ else (lambda c: INK)
        f.line((22, yl), (352, yl), cl(INK) if not sol_ else "#64748b", 2, True, True)
        f.line((22, ym), (352, ym), cl(INK) if not sol_ else "#64748b", 2, True, True)
        for X, Y_ in (("A", "B"), ("D", "C")):
            p_, q_ = P4[X], P4[Y_]
            dd = Fig.dir(q_, p_)
            f.line(Fig.pol(q_, dd + 180, 42), Fig.pol(p_, dd, 52), "#64748b" if sol_ else INK, 2, True, True)
        f.text(362, yl, "l", INK, 16, True)
        f.text(362, ym, "m", INK, 16, True)
        tp_ = Fig.pol(P4["A"], Fig.dir(P4["B"], P4["A"]), 62)
        tq_ = Fig.pol(P4["D"], Fig.dir(P4["C"], P4["D"]), 62)
        f.text(tp_[0] + 8, tp_[1], "p", INK, 16, True)
        f.text(tq_[0] + 8, tq_[1], "q", INK, 16, True)
    mk = []
    if sol:
        mk = [("a", "BAC", 1, BLU, 30), ("a", "DCA", 1, BLU, 30), ("a", "BCA", 2, ORG, 24), ("a", "DAC", 2, ORG, 24)]
    segs = [("AC", GRN, 3.4)] if sol else ["AC"]
    return geo(380, 250, P4, segs, {"A": (150, 18), "D": (60, 18), "B": (150, 19), "C": (320, 19)}, mk, cap,
               fills=(("ABC", BLU), ("CDA", ORG)), extra=ext, sol=sol)


s = given(m("l \\parallel m") + " (रेखा AD ∥ रेखा BC)<br>" + m("p \\parallel q") + " (रेखा AB ∥ रेखा DC)", "सिद्ध करना है: " + m("\\triangle ABC \\cong \\triangle CDA"))
s += figs(fig719, "आकृति 7.19", "एकांतर कोण-युग्म नीला (एक चाप) और नारंगी (दो चाप), AC हरी (उभयनिष्ठ)")
s += key((BLU, "∠BAC = ∠DCA"), (ORG, "∠BCA = ∠DAC"), (GRN, "AC उभयनिष्ठ"))
s += num(1, ALT)
s += kk("कोणों के युग्म:", [
    (ang("BAC", BLU) + " = " + ang("DCA", BLU) + " \\quad (1)", "p ∥ q, तिर्यक रेखा AC — एकांतर अंतः कोण"),
    (ang("BCA", ORG) + " = " + ang("DAC", ORG) + " \\quad (2)", "l ∥ m, तिर्यक रेखा AC — एकांतर अंतः कोण")])
s += num(2, ASA)
s += kk(m("\\triangle ABC") + " और " + m("\\triangle CDA") + " में,",
        [(ang("BAC", BLU) + " = " + ang("DCA", BLU), "(1) से", "A", BLU),
         (sd("AC", GRN) + " = " + sd("CA", GRN), "उभयनिष्ठ भुजा", "S", GRN),
         (ang("BCA", ORG) + " = " + ang("DAC", ORG), "(2) से", "A", ORG)],
        ("\\triangle ABC \\cong \\triangle CDA", "ASA सर्वांगसमता नियम द्वारा"),
        [("A", "C"), ("B", "D"), ("C", "A")])
s += tp("भुजा " + m(sd("AC", GRN)) + " दोनों कोणों " + m(ang("BAC", BLU)) + " और " + m(ang("BCA", ORG)) + " के बीच की (अंतर्गत) भुजा है, इसलिए ASA लगता है।")
s += ans(m("\\triangle ABC \\cong \\triangle CDA") + " (ASA नियम से) सिद्ध हुआ।")
E1.append((m("l") + " और " + m("m") + " दो समांतर रेखाएँ हैं जिन्हें समांतर रेखाओं " + m("p") + " और " + m("q") + " का एक अन्य युग्म प्रतिच्छेदित करता है (देखिए आकृति 7.19)। दर्शाइए कि "
           + m("\\triangle ABC \\cong \\triangle CDA") + " है।", s))

# ---------- Q5 (आकृति 7.20) ----------
al5 = 21
A5 = (40, 215)
B5 = Fig.pol(A5, al5, 190)
P5_ = (B5[0], A5[1])
Q5_ = foot(B5, A5, Fig.pol(A5, 2 * al5, 100))
P5 = {"A": A5, "B": B5, "P": P5_, "Q": Q5_}
close1(dist(B5, P5_), dist(B5, Q5_), 1e-6)


def fig720(sol, cap):
    def ext(f, sol_):
        c_ = "#64748b" if sol_ else INK
        f.line(A5, (352, A5[1]), c_, 2, False, True)
        f.line(A5, Fig.pol(A5, 2 * al5, 290), c_, 2, False, True)
        f.line(A5, Fig.pol(A5, al5, 295), c_, 2, False, True)
        e_ = Fig.pol(A5, al5, 300)
        f.text(e_[0] + 8, e_[1] - 6, "l", INK, 16, True)
    mk = [("r", "APB", PUR), ("r", "AQB", PUR), ("a", "PAB", 1, BLU, 44), ("a", "BAQ", 1, BLU, 44)]
    if sol:
        mk += [("t", "BP", 2, ORG), ("t", "BQ", 2, ORG)]
    segs = [("AB", GRN, 3.4), ("BP", ORG, 3), ("BQ", ORG, 3)] if sol else ["BP", "BQ"]
    return geo(380, 250, P5, segs, {"A": (225, 17), "B": (330, 17), "P": (300, 16), "Q": (125, 17)}, mk, cap,
               fills=(("APB", BLU), ("AQB", ORG)), extra=ext, sol=sol)


s = given("रेखा " + m("l") + ", " + m("\\angle A") + " को समद्विभाजित करती है: " + m(ang("PAB", BLU) + " = " + ang("QAB", BLU)) + "<br>"
          + m("B") + " रेखा " + m("l") + " पर है<br>" + m("BP \\perp AP") + ", " + m("BQ \\perp AQ"),
          "सिद्ध करना है:<br>(i) " + m("\\triangle APB \\cong \\triangle AQB") + "<br>(ii) " + m(sd("BP", ORG) + " = " + sd("BQ", ORG)))
s += figs(fig720, "आकृति 7.20", "समकोण बैंगनी, बराबर कोण नीले, AB हरी (उभयनिष्ठ)")
s += key((PUR, "समकोण ∠APB, ∠AQB"), (BLU, "∠PAB = ∠QAB"), (GRN, "AB उभयनिष्ठ"), (ORG, "BP, BQ"))
s += kh("(i) " + m("\\triangle APB \\cong \\triangle AQB"))
s += num(1, AAS)
s += kk(m("\\triangle APB") + " और " + m("\\triangle AQB") + " में,",
        [(ang("APB", PUR) + " = " + dg(90, PUR), "BP ⊥ AP"),
         (ang("AQB", PUR) + " = " + dg(90, PUR), "BQ ⊥ AQ"),
         (ang("APB", PUR) + " = " + ang("AQB", PUR) + " \\quad (1)", "दोनों 90° हैं", "A", PUR),
         (ang("PAB", BLU) + " = " + ang("QAB", BLU) + " \\quad (2)", "रेखा l, ∠A को समद्विभाजित करती है", "A", BLU),
         (sd("AB", GRN) + " = " + sd("AB", GRN) + " \\quad (3)", "उभयनिष्ठ भुजा", "S", GRN)],
        ("\\triangle APB \\cong \\triangle AQB", "(1), (2), (3) से, AAS सर्वांगसमता नियम द्वारा"),
        [("A", "A"), ("P", "Q"), ("B", "B")])
s += kh("(ii) " + m(sd("BP", ORG) + " = " + sd("BQ", ORG)))
s += num(2, CPCT)
s += kk("", [(sd("BP", ORG) + " = " + sd("BQ", ORG), "CPCT (P ↔ Q, इसलिए BP ↔ BQ)")])
s += p("BP और BQ, बिंदु B की कोण की दोनों भुजाओं से (लंब) दूरियाँ हैं; ये बराबर हैं, इसलिए B कोण की भुजाओं से समदूरस्थ है।")
s += ans("(i) " + m("\\triangle APB \\cong \\triangle AQB") + " (AAS) (ii) " + m(sd("BP", ORG) + " = " + sd("BQ", ORG)) + ", अर्थात् B कोण A की भुजाओं से समदूरस्थ है।")
E1.append(("रेखा " + m("l") + " कोण " + m("A") + " को समद्विभाजित करती है और " + m("B") + " रेखा " + m("l") + " पर स्थित कोई बिंदु है। " + m("BP") + " और " + m("BQ")
           + " कोण " + m("A") + " की भुजाओं पर " + m("B") + " से डाले गए लम्ब हैं (देखिए आकृति 7.20)। दर्शाइए कि (i) " + m("\\triangle APB \\cong \\triangle AQB")
           + " (ii) " + m("BP = BQ") + " है, अर्थात् बिंदु " + m("B") + " कोण की भुजाओं से समदूरस्थ है", s))

# ---------- Q6 (आकृति 7.21) ----------
A6 = (140, 92)
B6 = (46, 246)
D6 = (2 * A6[0] - B6[0], B6[1])
C6 = (296, 246)
rot6 = (Fig.dir(A6, D6) - Fig.dir(A6, B6)) % 360          # ∠BAD, measured anticlockwise from AB to AD
E6 = Fig.pol(A6, Fig.dir(A6, C6) + rot6, dist(A6, C6))
P6 = {"A": A6, "B": B6, "C": C6, "D": D6, "E": E6}
close1(dist(A6, B6), dist(A6, D6), 1e-6)
close1(dist(A6, C6), dist(A6, E6), 1e-6)
close1(angle_at(A6, B6, D6), angle_at(A6, E6, C6), 1e-6)
assert 15 < E6[0] < 365 and 15 < E6[1], E6
close1(dist(B6, C6), dist(D6, E6), 1e-6)


def fig721(sol, cap):
    mk = [("t", "AB", 1, RED), ("t", "AD", 1, RED, .55), ("t", "AC", 2, ORG, .62), ("t", "AE", 2, ORG), ("a", "BAD", 1, BLU, 20), ("a", "EAC", 1, BLU, 20)]
    if sol:
        mk += [("a", "DAC", 1, TEA, 30), ("ad", "BAC", PUR, 46), ("ad", "DAE", PUR, 56), ("t", "BC", 3, GRN, .3), ("t", "DE", 3, GRN, .62)]
    segs = ([("AB", RED, 3), ("AD", RED, 3), ("AC", ORG, 3), ("AE", ORG, 3), ("BC", GRN, 3), ("DE", GRN, 3), "EC"] if sol
            else ["AB", "AD", "AC", "AE", "BC", "DE", "EC"])
    return geo(380, 280, P6, segs, {"A": (115, 18), "B": (220, 16), "C": (300, 16), "D": (260, 18), "E": (150, 16)}, mk, cap,
               fills=(("ABC", BLU), ("ADE", ORG)), sol=sol)


s = given(m(sd("AC", ORG) + " = " + sd("AE", ORG)) + "<br>" + m(sd("AB", RED) + " = " + sd("AD", RED)) + "<br>" + m(ang("BAD", BLU) + " = " + ang("EAC", BLU)),
          "सिद्ध करना है: " + m(sd("BC", GRN) + " = " + sd("DE", GRN)))
s += figs(fig721, "आकृति 7.21", "AB = AD लाल (एक निशान), AC = AE नारंगी (दो निशान); बैंगनी बिंदुदार चाप ∠BAC और ∠DAE")
s += key((RED, "AB = AD"), (ORG, "AC = AE"), (BLU, "∠BAD = ∠EAC"), (TEA, "∠DAC"), (PUR, "∠BAC, ∠DAE"), (GRN, "BC, DE"))
s += kh("चरण 1: " + m(ang("BAC", PUR) + " = " + ang("DAE", PUR)) + " दिखाना")
s += num(1, EQ_ADD)
s += chain((ang("BAD", BLU), ang("EAC", BLU) + " \\qquad \\ldots(1)", "दिया है"))
s += chain((ang("BAD", BLU) + " + " + ang("DAC", TEA), ang("EAC", BLU) + " + " + ang("DAC", TEA), "(1) के दोनों पक्षों में ∠DAC जोड़ने पर"), small=True)
s += chain((ang("BAD", BLU) + " + " + ang("DAC", TEA), ang("BAC", PUR), "किरण AD, ∠BAC के अंदर है"))
s += chain((ang("EAC", BLU) + " + " + ang("DAC", TEA), ang("DAE", PUR), "किरण AC, ∠DAE के अंदर है"))
s += chain((ang("BAC", PUR), ang("DAE", PUR) + " \\qquad \\ldots(2)", "ऊपर के तीनों कथनों से"))
s += kh("चरण 2: सर्वांगसमता")
s += num(2, SAS)
s += kk(m("\\triangle ABC") + " और " + m("\\triangle ADE") + " में,",
        [(sd("AB", RED) + " = " + sd("AD", RED), "दिया है", "S", RED),
         (ang("BAC", PUR) + " = " + ang("DAE", PUR), "(2) से", "A", PUR),
         (sd("AC", ORG) + " = " + sd("AE", ORG), "दिया है", "S", ORG)],
        ("\\triangle ABC \\cong \\triangle ADE", "SAS सर्वांगसमता नियम द्वारा"),
        [("A", "A"), ("B", "D"), ("C", "E")])
s += num(3, CPCT)
s += kk("", [(sd("BC", GRN) + " = " + sd("DE", GRN), "CPCT (B ↔ D, C ↔ E, इसलिए BC ↔ DE)")])
s += ans(m(sd("BC", GRN) + " = " + sd("DE", GRN)) + " सिद्ध हुआ।")
E1.append(("आकृति 7.21 में, " + m("AC = AE") + ", " + m("AB = AD") + " और " + m("\\angle BAD = \\angle EAC") + " है। दर्शाइए कि " + m("BC = DE") + " है।", s))

# ---------- Q7 (आकृति 7.22) ----------
al7, be7 = 36, 62
A7, B7 = (40, 200), (330, 200)
P7_ = mid(A7, B7)
D7 = inter(A7, Fig.pol(A7, al7, 100), P7_, Fig.pol(P7_, be7, 100))
E7 = inter(B7, Fig.pol(B7, 180 - al7, 100), P7_, Fig.pol(P7_, 180 - be7, 100))
P7 = {"A": A7, "B": B7, "P": P7_, "D": D7, "E": E7}
close1(dist(A7, D7), dist(B7, E7), 1e-6)
assert 20 < D7[1] and 20 < E7[1]


def fig722(sol, cap):
    mk = [("a", "BAD", 1, BLU, 34), ("a", "ABE", 1, BLU, 34), ("a", "EPA", 2, ORG, 26), ("a", "DPB", 2, ORG, 26)]
    if sol:
        mk += [("a", "EPD", 1, TEA, 18), ("ad", "DPA", PUR, 46), ("ad", "EPB", PUR, 56), ("t", "AP", 1, RED), ("t", "PB", 1, RED),
               ("t", "AD", 2, GRN, .35), ("t", "BE", 2, GRN, .35)]
    segs = ([("AP", RED, 3), ("PB", RED, 3), ("AD", GRN, 3), ("BE", GRN, 3), "PE", "PD"] if sol else ["AB", "AD", "BE", "PE", "PD"])
    return geo(370, 250, P7, segs, {"A": (180, 17), "B": (0, 17), "P": (270, 18), "D": (60, 16), "E": (120, 16)}, mk, cap,
               fills=(("DAP", BLU), ("EBP", ORG)), sol=sol)


s = given(m("P") + ", " + m("AB") + " का मध्य-बिंदु है: " + m(sd("AP", RED) + " = " + sd("BP", RED)) + "<br>" + m(ang("BAD", BLU) + " = " + ang("ABE", BLU)) + "<br>"
          + m(ang("EPA", ORG) + " = " + ang("DPB", ORG)),
          "सिद्ध करना है:<br>(i) " + m("\\triangle DAP \\cong \\triangle EBP") + "<br>(ii) " + m(sd("AD", GRN) + " = " + sd("BE", GRN)))
s += figs(fig722, "आकृति 7.22", "AP = BP लाल, ∠A = ∠B नीले, P पर दिए कोण नारंगी; बैंगनी बिंदुदार चाप ∠DPA और ∠EPB")
s += key((RED, "AP = BP"), (BLU, "∠BAD = ∠ABE"), (ORG, "∠EPA = ∠DPB"), (TEA, "∠EPD"), (PUR, "∠DPA, ∠EPB"), (GRN, "AD, BE"))
s += kh("चरण 1: " + m(ang("DPA", PUR) + " = " + ang("EPB", PUR)) + " दिखाना")
s += num(1, EQ_ADD)
s += chain((ang("EPA", ORG), ang("DPB", ORG) + " \\qquad \\ldots(1)", "दिया है"))
s += chain((ang("EPA", ORG) + " + " + ang("DPE", TEA), ang("DPB", ORG) + " + " + ang("DPE", TEA), "(1) के दोनों पक्षों में ∠DPE जोड़ने पर"), small=True)
s += chain((ang("EPA", ORG) + " + " + ang("DPE", TEA), ang("DPA", PUR), "किरण PE, ∠DPA के अंदर है"))
s += chain((ang("DPB", ORG) + " + " + ang("DPE", TEA), ang("EPB", PUR), "किरण PD, ∠EPB के अंदर है"))
s += chain((ang("DPA", PUR), ang("EPB", PUR) + " \\qquad \\ldots(2)", "ऊपर के तीनों कथनों से"))
s += kh("(i) " + m("\\triangle DAP \\cong \\triangle EBP"))
s += num(2, ASA)
s += kk(m("\\triangle DAP") + " और " + m("\\triangle EBP") + " में,",
        [(ang("DAP", BLU) + " = " + ang("EBP", BLU), "दिया है (∠BAD = ∠ABE)", "A", BLU),
         (sd("AP", RED) + " = " + sd("BP", RED), "P, AB का मध्य-बिंदु है", "S", RED),
         (ang("DPA", PUR) + " = " + ang("EPB", PUR), "(2) से", "A", PUR)],
        ("\\triangle DAP \\cong \\triangle EBP", "ASA सर्वांगसमता नियम द्वारा"),
        [("D", "E"), ("A", "B"), ("P", "P")])
s += kh("(ii) " + m(sd("AD", GRN) + " = " + sd("BE", GRN)))
s += num(3, CPCT)
s += kk("", [(sd("AD", GRN) + " = " + sd("BE", GRN), "CPCT (D ↔ E, A ↔ B, इसलिए AD ↔ BE)")])
s += ans("(i) " + m("\\triangle DAP \\cong \\triangle EBP") + " (ASA) (ii) " + m(sd("AD", GRN) + " = " + sd("BE", GRN)) + " — सिद्ध हुआ।")
E1.append((m("AB") + " एक रेखाखंड है और " + m("P") + " इसका मध्य-बिंदु है। " + m("D") + " और " + m("E") + " रेखाखंड " + m("AB") + " के एक ही ओर स्थित दो बिंदु इस प्रकार हैं कि "
           + m("\\angle BAD = \\angle ABE") + " और " + m("\\angle EPA = \\angle DPB") + " है। (देखिए आकृति 7.22)। दर्शाइए कि (i) " + m("\\triangle DAP \\cong \\triangle EBP")
           + " (ii) " + m("AD = BE"), s))

# ---------- Q8 (आकृति 7.23) ----------
P8 = {"D": (70, 40), "A": (300, 40), "B": (70, 210), "C": (300, 210)}
P8["M"] = mid(P8["A"], P8["B"])
close1(dist(P8["M"], P8["C"]), dist(P8["M"], P8["D"]), 1e-6)


def fig723(sol, cap):
    mk = []
    if sol:
        mk = [("t", "AM", 1, RED), ("t", "MB", 1, RED), ("t", "CM", 2, ORG), ("t", "MD", 2, ORG), ("a", "AMC", 1, BLU, 18), ("a", "BMD", 1, BLU, 18),
              ("a", "ACM", 2, TEA, 30), ("a", "BDM", 2, TEA, 30), ("r", "ACB", PUR), ("r", "DBC", PUR), ("t", "AC", 3, BROWN), ("t", "DB", 3, BROWN)]
    segs = ([("AM", RED, 3), ("MB", RED, 3), ("CM", ORG, 3), ("MD", ORG, 3), ("AC", BROWN, 3), ("DB", BROWN, 3), ("BC", GRN, 3)] if sol
            else ["DB", "BC", "CA", "AB", "DC"])
    return geo(370, 250, P8, segs, {"D": (135, 16), "A": (45, 16), "B": (225, 16), "C": (315, 16), "M": (270, 20)}, mk, cap,
               fills=(("AMC", BLU), ("BMD", ORG)), sol=sol)


s = given(m("\\triangle ABC") + " में " + m(ang("ACB", PUR) + " = " + dg(90, PUR)) + "<br>" + m("M") + ", कर्ण " + m("AB") + " का मध्य-बिंदु: " + m(sd("AM", RED) + " = " + sd("BM", RED))
          + "<br>" + m(sd("DM", ORG) + " = " + sd("CM", ORG)),
          "सिद्ध करना है:<br>(i) " + m("\\triangle AMC \\cong \\triangle BMD") + "<br>(ii) " + m(ang("DBC", PUR) + " = 90^\\circ") + "<br>(iii) "
          + m("\\triangle DBC \\cong \\triangle ACB") + "<br>(iv) " + m(sd("CM", ORG) + " = \\dfrac{1}{2}AB"))
s += figs(fig723, "आकृति 7.23", "AM = BM लाल, CM = DM नारंगी, शीर्षाभिमुख कोण नीले, AC = DB भूरी, BC हरी")
s += key((RED, "AM = BM"), (ORG, "CM = DM"), (BLU, "∠AMC = ∠BMD"), (TEA, "∠ACM = ∠BDM"), (BROWN, "AC = DB"), (PUR, "समकोण"), (GRN, "BC उभयनिष्ठ"))
s += kh("(i) " + m("\\triangle AMC \\cong \\triangle BMD"))
s += num(1, VOPP)
s += num(2, SAS)
s += kk(m("\\triangle AMC") + " और " + m("\\triangle BMD") + " में,",
        [(sd("AM", RED) + " = " + sd("BM", RED), "M, AB का मध्य-बिंदु है", "S", RED),
         (ang("AMC", BLU) + " = " + ang("BMD", BLU), "शीर्षाभिमुख कोण", "A", BLU),
         (sd("CM", ORG) + " = " + sd("DM", ORG), "दिया है", "S", ORG)],
        ("\\triangle AMC \\cong \\triangle BMD", "SAS सर्वांगसमता नियम द्वारा"),
        [("A", "B"), ("M", "M"), ("C", "D")])
s += kh("(ii) " + m(ang("DBC", PUR) + " = 90^\\circ"))
s += num(3, CPCT)
s += kk("(i) से CPCT द्वारा:", [
    (ang("ACM", TEA) + " = " + ang("BDM", TEA) + " \\quad (1)", "CPCT (C ↔ D)"),
    (sd("AC", BROWN) + " = " + sd("DB", BROWN) + " \\quad (2)", "CPCT (A ↔ B, C ↔ D)")])
s += num(4, ALT_C)
s += stmt("AC \\parallel DB", "तिर्यक रेखा CD, रेखाओं AC और DB के साथ एकांतर अंतः कोण ∠ACD और ∠BDC बनाती है और (1) से ये बराबर हैं")
s += num(5, INT)
s += chain((ang("DBC", PUR) + " + " + ang("ACB", PUR), "180" + DEG, "AC ∥ DB, तिर्यक रेखा BC — एक ही ओर के अंतः कोण"),
           (ang("DBC", PUR) + " + 90" + DEG, "180" + DEG, "∠ACB = 90° रखने पर"))
s += chain((ang("DBC", PUR), "180" + DEG + " - 90" + DEG, "+90° को पक्षांतर करने पर −90° हो जाता है"),
           ("", dg(90, PUR), "180 − 90 = 90"))
s += p("अतः " + m("\\angle DBC") + " एक समकोण है।")
s += kh("(iii) " + m("\\triangle DBC \\cong \\triangle ACB"))
s += num(6, SAS)
s += kk(m("\\triangle DBC") + " और " + m("\\triangle ACB") + " में,",
        [(sd("DB", BROWN) + " = " + sd("AC", BROWN), "(2) से", "S", BROWN),
         (ang("DBC", PUR) + " = " + ang("ACB", PUR), "दोनों 90° हैं [(ii) से और दिया है]", "A", PUR),
         (sd("BC", GRN) + " = " + sd("CB", GRN), "उभयनिष्ठ भुजा", "S", GRN)],
        ("\\triangle DBC \\cong \\triangle ACB", "SAS सर्वांगसमता नियम द्वारा"),
        [("D", "A"), ("B", "C"), ("C", "B")])
s += kh("(iv) " + m(sd("CM", ORG) + " = \\dfrac{1}{2}AB"))
s += kk("", [("DC = AB \\quad (3)", "(iii) से CPCT (D ↔ A, C ↔ B, इसलिए DC ↔ AB)")])
s += chain(("DC", sd("DM", ORG) + " + " + sd("CM", ORG), "M, रेखाखंड DC पर है"),
           ("", sd("CM", ORG) + " + " + sd("CM", ORG), "DM = CM (दिया है) रखने पर"),
           ("", "2\\," + sd("CM", ORG), "CM + CM = 2CM"))
s += chain(("2\\," + sd("CM", ORG), "DC", "पक्ष बदलकर लिखने पर"))
s += chain((sd("CM", ORG), "\\dfrac{1}{2}DC", "2 को पक्षांतर करने पर (गुणा → भाग)"),
           ("", "\\dfrac{1}{2}AB", "(3) से DC = AB रखने पर"))
s += ans("(i) " + m("\\triangle AMC \\cong \\triangle BMD") + " (SAS) (ii) " + m("\\angle DBC = 90^\\circ") + " (iii) " + m("\\triangle DBC \\cong \\triangle ACB")
         + " (SAS) (iv) " + m("CM = \\dfrac{1}{2}AB") + " — चारों सिद्ध हुए।")
E1.append(("एक समकोण त्रिभुज " + m("ABC") + " में, जिसमें कोण " + m("C") + " समकोण है, " + m("M") + " कर्ण " + m("AB") + " का मध्य-बिंदु है। " + m("C") + " को " + m("M")
           + " से मिलाकर " + m("D") + " तक इस प्रकार बढ़ाया गया है कि " + m("DM = CM") + " है। बिंदु " + m("D") + " को बिंदु " + m("B") + " से मिला दिया जाता है (देखिए आकृति 7.23)। दर्शाइए कि "
           + "(i) " + m("\\triangle AMC \\cong \\triangle BMD") + " (ii) " + m("\\angle DBC") + " एक समकोण है (iii) " + m("\\triangle DBC \\cong \\triangle ACB") + " (iv) "
           + m("CM = \\dfrac{1}{2}AB"), s))

# =====================================================================
# Exercise 7.2
# =====================================================================
E2 = []
NOFIG = "<div class='nofig'>(पुस्तक में इस प्रश्न की आकृति नहीं दी है; नीचे हल के लिए आकृति बनाई गई है।)</div>"


def solo(f):
    return f"<div style='max-width:430px;margin:0 auto'>{f}</div>"


# ---------- Q1 (no figure in book) ----------
P21 = {"A": (180, 35), "B": (60, 235), "C": (300, 235)}
hB = angle_at(P21["B"], P21["A"], P21["C"]) / 2
P21["O"] = inter(P21["B"], Fig.pol(P21["B"], hB, 100), P21["C"], Fig.pol(P21["C"], 180 - hB, 100))


def fig72_1(sol, cap):
    mk = [("t", "AB", 1, RED), ("t", "AC", 1, RED), ("a", "ABO", 1, BLU, 40), ("a", "OBC", 1, BLU, 32), ("a", "ACO", 1, BLU, 40), ("a", "OCB", 1, BLU, 32),
          ("t", "OB", 2, ORG), ("t", "OC", 2, ORG), ("a", "BAO", 2, PUR, 34), ("a", "OAC", 2, PUR, 34)]
    segs = [("AB", RED, 3), ("AC", RED, 3), "BC", ("OB", ORG, 3), ("OC", ORG, 3), ("AO", GRN, 3)]
    return geo(360, 270, P21, segs, {"A": (90, 15), "B": (200, 16), "C": (340, 16), "O": (270, 18)}, mk, cap,
               fills=(("ABO", BLU), ("ACO", ORG)), sol=sol)


s = given(m("\\triangle ABC") + " में " + m(sd("AB", RED) + " = " + sd("AC", RED)) + "<br>" + m("BO") + ", " + m("\\angle B") + " का और " + m("CO") + ", " + m("\\angle C") + " का समद्विभाजक है",
          "सिद्ध करना है:<br>(i) " + m(sd("OB", ORG) + " = " + sd("OC", ORG)) + "<br>(ii) " + m("AO") + ", " + m("\\angle A") + " को समद्विभाजित करता है: " + m(ang("BAO", PUR) + " = " + ang("CAO", PUR)))
s += NOFIG + solo(fig72_1(True, "हल की आकृति: AB = AC लाल, चारों आधे कोण नीले, OB = OC नारंगी"))
s += key((RED, "AB = AC"), (BLU, "∠B और ∠C के आधे"), (ORG, "OB = OC"), (GRN, "AO उभयनिष्ठ"), (PUR, "∠BAO, ∠CAO"))
s += kh("चरण 1: आधे कोण बराबर हैं")
s += num(1, TH72)
s += chain(("\\angle ABC", "\\angle ACB \\qquad \\ldots(1)", "AB = AC, बराबर भुजाओं के सम्मुख कोण (प्रमेय 7.2)"))
s += num(2, EQ_HALF)
s += chain((ang("OBC", BLU), "\\dfrac{1}{2}\\angle ABC", "BO, ∠B का समद्विभाजक है"),
           ("", "\\dfrac{1}{2}\\angle ACB", "(1) से ∠ABC = ∠ACB रखने पर"),
           ("", ang("OCB", BLU) + " \\qquad \\ldots(2)", "CO, ∠C का समद्विभाजक है"))
s += chain((ang("ABO", BLU), ang("ACO", BLU) + " \\qquad \\ldots(3)", "इसी प्रकार ∠B का आधा = ∠C का आधा"))
s += kh("(i) " + m(sd("OB", ORG) + " = " + sd("OC", ORG)))
s += num(3, TH73)
s += kk(m("\\triangle OBC") + " में,", [(ang("OBC", BLU) + " = " + ang("OCB", BLU), "(2) से"),
                                     (sd("OC", ORG) + " = " + sd("OB", ORG) + " \\quad (4)", "बराबर कोणों की सम्मुख भुजाएँ (प्रमेय 7.3): ∠OBC के सामने OC, ∠OCB के सामने OB")])
s += kh("(ii) " + m("AO") + ", " + m("\\angle A") + " को समद्विभाजित करता है")
s += num(4, SAS)
s += kk(m("\\triangle AOB") + " और " + m("\\triangle AOC") + " में,",
        [(sd("AB", RED) + " = " + sd("AC", RED), "दिया है", "S", RED),
         (ang("ABO", BLU) + " = " + ang("ACO", BLU), "(3) से", "A", BLU),
         (sd("OB", ORG) + " = " + sd("OC", ORG), "(4) से", "S", ORG)],
        ("\\triangle AOB \\cong \\triangle AOC", "SAS सर्वांगसमता नियम द्वारा"),
        [("A", "A"), ("O", "O"), ("B", "C")])
s += num(5, CPCT)
s += kk("", [(ang("BAO", PUR) + " = " + ang("CAO", PUR), "CPCT (B ↔ C)")])
s += p("अतः " + m("AO") + ", " + m("\\angle A") + " को समद्विभाजित करता है।")
s += ans("(i) " + m(sd("OB", ORG) + " = " + sd("OC", ORG)) + " (ii) " + m(ang("BAO", PUR) + " = " + ang("CAO", PUR)) + ", अर्थात् AO कोण A को समद्विभाजित करता है।")
E2.append(("एक समद्विबाहु त्रिभुज " + m("ABC") + " में जिसमें " + m("AB = AC") + " है, " + m("\\angle B") + " और " + m("\\angle C") + " के समद्विभाजक परस्पर बिंदु " + m("O")
           + " पर प्रतिच्छेद करते हैं। " + m("A") + " और " + m("O") + " को जोड़िए। दर्शाइए कि (i) " + m("OB = OC") + " (ii) " + m("AO") + " कोण " + m("A") + " को समद्विभाजित करता है", s))

# ---------- Q2 (आकृति 7.30) ----------
P22 = {"A": (180, 35), "B": (55, 230), "C": (305, 230)}
P22["D"] = mid(P22["B"], P22["C"])


def fig730(sol, cap):
    mk = [("r", "ADC", PUR)]
    if sol:
        mk += [("t", "BD", 1, RED), ("t", "DC", 1, RED), ("t", "AB", 2, ORG), ("t", "AC", 2, ORG), ("r", "ADB", PUR)]
    segs = [("BD", RED, 3), ("DC", RED, 3), ("AD", GRN, 3.4), ("AB", ORG, 3), ("AC", ORG, 3)] if sol else ["AB", "AC", "BC", "AD"]
    return geo(360, 265, P22, segs, {"A": (90, 15), "B": (200, 15), "C": (340, 15), "D": (270, 17)}, mk, cap,
               fills=(("ADB", BLU), ("ADC", ORG)), sol=sol)


s = given(m("AD") + ", भुजा " + m("BC") + " का लम्ब समद्विभाजक है:<br>" + m(sd("BD", RED) + " = " + sd("DC", RED)) + " और " + m("AD \\perp BC"),
          "सिद्ध करना है: " + m(sd("AB", ORG) + " = " + sd("AC", ORG)) + " (त्रिभुज समद्विबाहु है)")
s += figs(fig730, "आकृति 7.30", "BD = DC लाल, समकोण बैंगनी, AD हरी (उभयनिष्ठ)")
s += key((RED, "BD = DC"), (PUR, "समकोण ∠ADB, ∠ADC"), (GRN, "AD उभयनिष्ठ"), (ORG, "AB, AC"))
s += num(1, SAS)
s += kk(m("\\triangle ADB") + " और " + m("\\triangle ADC") + " में,",
        [(sd("BD", RED) + " = " + sd("CD", RED), "AD, BC को समद्विभाजित करता है", "S", RED),
         (ang("ADB", PUR) + " = " + ang("ADC", PUR), "दोनों 90° हैं (AD ⊥ BC)", "A", PUR),
         (sd("AD", GRN) + " = " + sd("AD", GRN), "उभयनिष्ठ भुजा", "S", GRN)],
        ("\\triangle ADB \\cong \\triangle ADC", "SAS सर्वांगसमता नियम द्वारा"),
        [("A", "A"), ("D", "D"), ("B", "C")])
s += num(2, CPCT)
s += kk("", [(sd("AB", ORG) + " = " + sd("AC", ORG), "CPCT (B ↔ C, इसलिए AB ↔ AC)")])
s += ans(m(sd("AB", ORG) + " = " + sd("AC", ORG)) + ", अतः " + m("\\triangle ABC") + " एक समद्विबाहु त्रिभुज है। सिद्ध हुआ।")
E2.append((m("\\triangle ABC") + " में " + m("AD") + " भुजा " + m("BC") + " का लम्ब समद्विभाजक है (देखिए आकृति 7.30)। दर्शाइए कि " + m("\\triangle ABC")
           + " एक समद्विबाहु त्रिभुज है, जिसमें " + m("AB = AC") + " है।", s))


# ---------- Q3, Q4 (आकृति 7.31, 7.32) ----------
def alt_pts(A, B, C):
    P = {"A": A, "B": B, "C": C}
    P["E"] = foot(B, A, C)
    P["F"] = foot(C, A, B)
    return P


P23 = alt_pts((180, 30), (40, 235), (320, 235))
P24 = alt_pts((185, 32), (35, 235), (335, 235))
close1(dist(P23["B"], P23["E"]), dist(P23["C"], P23["F"]), 1e-6)
close1(dist(P24["B"], P24["E"]), dist(P24["C"], P24["F"]), 1e-6)


def alt_fig(P, sol, cap, given_be):
    mk = [("r", "AFC", PUR), ("r", "AEB", PUR)]
    if given_be:
        mk += []
    if sol:
        mk += [("a", "BAC", 1, BLU, 30), ("t", "BE", 2, ORG, .4), ("t", "CF", 2, ORG, .4), ("t", "AB", 1, RED, .3), ("t", "AC", 1, RED, .3)]
    segs = ([("AB", RED, 3), ("AC", RED, 3), "BC", ("BE", ORG, 3), ("CF", ORG, 3)] if sol else ["AB", "AC", "BC", "BE", "CF"])
    return geo(360, 265, P, segs, {"A": (90, 15), "B": (200, 15), "C": (340, 15), "E": (20, 15), "F": (160, 15)}, mk, cap,
               fills=(("ABE", BLU), ("ACF", ORG)), sol=sol)


s = given(m("\\triangle ABC") + " में " + m(sd("AB", RED) + " = " + sd("AC", RED)) + "<br>" + m("BE \\perp AC") + ", " + m("CF \\perp AB"),
          "सिद्ध करना है: " + m(sd("BE", ORG) + " = " + sd("CF", ORG)))
s += figs(lambda sol, cap: alt_fig(P23, sol, cap, False), "आकृति 7.31", "AB = AC लाल, उभयनिष्ठ ∠A नीला, समकोण बैंगनी")
s += key((RED, "AB = AC"), (BLU, "∠A उभयनिष्ठ"), (PUR, "समकोण ∠AEB, ∠AFC"), (ORG, "BE, CF"))
s += num(1, AAS)
s += kk(m("\\triangle ABE") + " और " + m("\\triangle ACF") + " में,",
        [(ang("AEB", PUR) + " = " + ang("AFC", PUR), "दोनों 90° हैं (BE ⊥ AC, CF ⊥ AB)", "A", PUR),
         (ang("BAE", BLU) + " = " + ang("CAF", BLU), "उभयनिष्ठ कोण ∠A", "A", BLU),
         (sd("AB", RED) + " = " + sd("AC", RED), "दिया है", "S", RED)],
        ("\\triangle ABE \\cong \\triangle ACF", "AAS सर्वांगसमता नियम द्वारा"),
        [("A", "A"), ("B", "C"), ("E", "F")])
s += tp("भुजा " + m(sd("AB", RED)) + " समकोण " + m(ang("AEB", PUR)) + " के सामने है और " + m(sd("AC", RED)) + " समकोण " + m(ang("AFC", PUR)) + " के सामने — ये संगत भुजाएँ हैं ✔")
s += num(2, CPCT)
s += kk("", [(sd("BE", ORG) + " = " + sd("CF", ORG), "CPCT (B ↔ C, E ↔ F)")])
s += ans("शीर्षलम्ब " + m(sd("BE", ORG) + " = " + sd("CF", ORG)) + ", अर्थात् ये बराबर हैं। सिद्ध हुआ।")
E2.append(("ABC एक समद्विबाहु त्रिभुज है, जिसमें बराबर भुजाओं " + m("AC") + " और " + m("AB") + " पर क्रमशः शीर्षलम्ब " + m("BE") + " और " + m("CF")
           + " खींचे गए हैं (देखिए आकृति 7.31)। दर्शाइए कि ये शीर्षलम्ब बराबर हैं।", s))

s = given(m("\\triangle ABC") + " में " + m("BE \\perp AC") + ", " + m("CF \\perp AB") + "<br>" + m(sd("BE", ORG) + " = " + sd("CF", ORG)),
          "सिद्ध करना है:<br>(i) " + m("\\triangle ABE \\cong \\triangle ACF") + "<br>(ii) " + m(sd("AB", RED) + " = " + sd("AC", RED)))
s += figs(lambda sol, cap: alt_fig(P24, sol, cap, True), "आकृति 7.32", "BE = CF नारंगी, उभयनिष्ठ ∠A नीला, समकोण बैंगनी")
s += key((ORG, "BE = CF"), (BLU, "∠A उभयनिष्ठ"), (PUR, "समकोण ∠AEB, ∠AFC"), (RED, "AB, AC"))
s += kh("(i) " + m("\\triangle ABE \\cong \\triangle ACF"))
s += num(1, AAS)
s += kk(m("\\triangle ABE") + " और " + m("\\triangle ACF") + " में,",
        [(ang("AEB", PUR) + " = " + ang("AFC", PUR), "दोनों 90° हैं", "A", PUR),
         (ang("BAE", BLU) + " = " + ang("CAF", BLU), "उभयनिष्ठ कोण ∠A", "A", BLU),
         (sd("BE", ORG) + " = " + sd("CF", ORG), "दिया है", "S", ORG)],
        ("\\triangle ABE \\cong \\triangle ACF", "AAS सर्वांगसमता नियम द्वारा"),
        [("A", "A"), ("B", "C"), ("E", "F")])
s += tp("भुजा " + m(sd("BE", ORG)) + " कोण " + m(ang("A", BLU)) + " के सामने है और " + m(sd("CF", ORG)) + " भी कोण " + m(ang("A", BLU)) + " के सामने — ये संगत भुजाएँ हैं ✔")
s += kh("(ii) " + m(sd("AB", RED) + " = " + sd("AC", RED)))
s += num(2, CPCT)
s += kk("", [(sd("AB", RED) + " = " + sd("AC", RED), "CPCT (B ↔ C, इसलिए AB ↔ AC)")])
s += ans("(i) " + m("\\triangle ABE \\cong \\triangle ACF") + " (AAS) (ii) " + m(sd("AB", RED) + " = " + sd("AC", RED)) + ", अर्थात् " + m("\\triangle ABC") + " समद्विबाहु त्रिभुज है।")
E2.append(("ABC एक त्रिभुज है जिसमें " + m("AC") + " और " + m("AB") + " पर खींचे गए शीर्षलम्ब " + m("BE") + " और " + m("CF") + " बराबर हैं (देखिए आकृति 7.32)। दर्शाइए कि (i) "
           + m("\\triangle ABE \\cong \\triangle ACF") + " (ii) " + m("AB = AC") + ", अर्थात् " + m("\\triangle ABC") + " एक समद्विबाहु त्रिभुज है।", s))

# ---------- Q5 (आकृति 7.33) ----------
P25 = {"A": (180, 30), "B": (75, 175), "C": (285, 175), "D": (180, 260)}


def fig733(sol, cap):
    mk = [("t", "AB", 1, RED), ("t", "AC", 1, RED), ("t", "BD", 2, ORG), ("t", "DC", 2, ORG)]
    if sol:
        mk += [("a", "ABC", 1, BLU, 30), ("a", "ACB", 1, BLU, 30), ("a", "CBD", 2, TEA, 30), ("a", "BCD", 2, TEA, 30), ("ad", "ABD", PUR, 46), ("ad", "ACD", PUR, 46)]
    else:
        mk += [("a", "ABD", 1, INK, 22), ("a", "ACD", 1, INK, 22)]
    segs = [("AB", RED, 3), ("AC", RED, 3), ("BD", ORG, 3), ("DC", ORG, 3), "BC"] if sol else ["AB", "AC", "BD", "DC", "BC"]
    return geo(360, 290, P25, segs, {"A": (90, 15), "B": (180, 16), "C": (0, 16), "D": (270, 15)}, mk, cap, sol=sol)


s = given(m("\\triangle ABC") + " में " + m(sd("AB", RED) + " = " + sd("AC", RED)) + "<br>" + m("\\triangle DBC") + " में " + m(sd("DB", ORG) + " = " + sd("DC", ORG)) + "<br>(दोनों का आधार BC)",
          "सिद्ध करना है: " + m(ang("ABD", PUR) + " = " + ang("ACD", PUR)))
s += figs(fig733, "आकृति 7.33", "∠ABC = ∠ACB नीले, ∠DBC = ∠DCB हरे-नीले (दो चाप), बैंगनी बिंदुदार = ∠ABD, ∠ACD")
s += key((RED, "AB = AC"), (ORG, "DB = DC"), (BLU, "∠ABC = ∠ACB"), (TEA, "∠DBC = ∠DCB"), (PUR, "∠ABD, ∠ACD"))
s += num(1, TH72)
s += chain((ang("ABC", BLU), ang("ACB", BLU) + " \\qquad \\ldots(1)", "△ABC में AB = AC, बराबर भुजाओं के सम्मुख कोण"))
s += chain((ang("DBC", TEA), ang("DCB", TEA) + " \\qquad \\ldots(2)", "△DBC में DB = DC, बराबर भुजाओं के सम्मुख कोण"))
s += num(2, EQ_ADD)
s += chain((ang("ABC", BLU) + " + " + ang("DBC", TEA), ang("ACB", BLU) + " + " + ang("DCB", TEA), "(1) और (2) को जोड़ने पर"), small=True)
s += chain((ang("ABC", BLU) + " + " + ang("DBC", TEA), ang("ABD", PUR), "किरण BC, ∠ABD के अंदर है"))
s += chain((ang("ACB", BLU) + " + " + ang("DCB", TEA), ang("ACD", PUR), "किरण CB, ∠ACD के अंदर है"))
s += chain((ang("ABD", PUR), ang("ACD", PUR), "ऊपर के तीनों कथनों से"))
s += ans(m(ang("ABD", PUR) + " = " + ang("ACD", PUR)) + " सिद्ध हुआ।")
E2.append(("ABC और DBC समान आधार " + m("BC") + " पर स्थित दो समद्विबाहु त्रिभुज हैं (देखिए आकृति 7.33)। दर्शाइए कि " + m("\\angle ABD = \\angle ACD") + " है।", s))

# ---------- Q6 (आकृति 7.34) ----------
b6 = 54
P26 = {"B": (55, 265), "C": (225, 265)}
P26["D"] = (225, 265 - 170 * math.tan(math.radians(b6)))
assert P26["D"][1] > 20
P26["A"] = mid(P26["B"], P26["D"])
close1(dist(P26["A"], P26["B"]), dist(P26["A"], P26["C"]), 1e-6)
ACD6 = 90 - b6
assert b6 + (b6 + ACD6) + ACD6 == 180


def fig734(sol, cap):
    mk = [("t", "AB", 1, RED), ("t", "AC", 1, RED), ("t", "AD", 1, RED)]
    if sol:
        mk += [("a", "ABC", 1, BLU, 30), ("a", "ACB", 1, BLU, 30), ("a", "ACD", 2, ORG, 30), ("a", "ADC", 2, ORG, 30), ("r", "BCD", PUR)]
    segs = [("AB", RED, 3), ("AC", RED, 3), ("AD", RED, 3), "BC", "CD"] if sol else ["BD", "AC", "BC", "CD"]
    return geo(300, 300, P26, segs, {"A": (150, 17), "B": (210, 16), "C": (330, 16), "D": (30, 15)}, mk, cap,
               fills=(("ABC", BLU), ("ACD", ORG)), sol=sol)


s = given(m("\\triangle ABC") + " में " + m(sd("AB", RED) + " = " + sd("AC", RED)) + "<br>" + m("BA") + " को " + m("D") + " तक बढ़ाया: " + m(sd("AD", RED) + " = " + sd("AB", RED)),
          "सिद्ध करना है: " + m(ang("BCD", PUR) + " = 90^\\circ"))
s += figs(fig734, "आकृति 7.34", "△ABC के बराबर कोण नीले, △ACD के बराबर कोण नारंगी (दो चाप)")
s += key((RED, "AB, AC, AD बराबर"), (BLU, "∠ABC = ∠ACB"), (ORG, "∠ACD = ∠ADC"), (PUR, "∠BCD"))
s += num(1, TH72)
s += kk(m("\\triangle ABC") + " में,", [(ang("ACB", BLU) + " = " + ang("ABC", BLU) + " \\quad (1)", "AB = AC, बराबर भुजाओं के सम्मुख कोण")])
s += kk(m("\\triangle ACD") + " में,", [(sd("AD", RED) + " = " + sd("AB", RED), "दिया है"),
                                     (sd("AB", RED) + " = " + sd("AC", RED), "दिया है"),
                                     (sd("AD", RED) + " = " + sd("AC", RED), "दोनों AB के बराबर हैं"),
                                     (ang("ACD", ORG) + " = " + ang("ADC", ORG) + " \\quad (2)", "AD = AC, बराबर भुजाओं के सम्मुख कोण")])
s += num(2, ASUM)
s += p(m("\\triangle BCD") + " में:")
s += chain((ang("DBC", BLU) + " + " + ang("BCD", PUR) + " + " + ang("CDB", ORG), "180" + DEG, "त्रिभुज के कोणों का योग"), small=True)
s += chain((ang("BCD", PUR), ang("ACB", BLU) + " + " + ang("ACD", ORG) + " \\qquad \\ldots(3)", "किरण CA, ∠BCD के अंदर है"))
s += chain((ang("ACB", BLU) + " + (" + ang("ACB", BLU) + " + " + ang("ACD", ORG) + ") + " + ang("ACD", ORG), "180" + DEG,
            "(1) से ∠DBC = ∠ACB, (3) से ∠BCD, (2) से ∠CDB = ∠ACD रखने पर"),
           ("2" + ang("ACB", BLU) + " + 2" + ang("ACD", ORG), "180" + DEG, "समान पद जोड़ने पर"),
           ("2(" + ang("ACB", BLU) + " + " + ang("ACD", ORG) + ")", "180" + DEG, "2 उभयनिष्ठ लेने पर"), small=True)
s += chain((ang("ACB", BLU) + " + " + ang("ACD", ORG), "\\dfrac{180^\\circ}{2}", "2 को पक्षांतर करने पर (गुणा → भाग)"),
           ("", "90" + DEG, "180 ÷ 2 = 90"))
s += chain((ang("BCD", PUR), dg(90, PUR), "(3) से ∠BCD = ∠ACB + ∠ACD"))
s += tp("जाँच (आकृति में " + m(f"\\angle B = {b6}^\\circ") + " लिया है): " + m(f"\\angle ACB = {b6}^\\circ") + ", " + m(f"\\angle ACD = {ACD6}^\\circ") + ", तो "
        + m(f"\\angle BCD = {b6}^\\circ + {ACD6}^\\circ") + ", अर्थात् " + m("90^\\circ") + " ✔")
s += ans(m(ang("BCD", PUR) + " = 90^\\circ") + ", अर्थात् " + m("\\angle BCD") + " एक समकोण है। सिद्ध हुआ।")
E2.append(("ABC एक समद्विबाहु त्रिभुज है, जिसमें " + m("AB = AC") + " है। भुजा " + m("BA") + " बिंदु " + m("D") + " तक इस प्रकार बढ़ाई गई है कि " + m("AD = AB")
           + " है (देखिए आकृति 7.34)। दर्शाइए कि " + m("\\angle BCD") + " एक समकोण है।", s))

# ---------- Q7 (no figure) ----------
B7v = (180 - 90) / 2
assert B7v == 45


def fig72_7(sol, cap):
    mk = [("r", "BAC", PUR), ("t", "AB", 1, RED), ("t", "AC", 1, RED), ("a", "ABC", 1, BLU, 34), ("a", "ACB", 1, BLU, 34),
          ("l", "ABC", "45°", BLU, 50), ("l", "ACB", "45°", BLU, 54)]
    P = {"A": (60, 240), "B": (60, 50), "C": (250, 240)}
    return geo(310, 280, P, [("AB", RED, 3), ("AC", RED, 3), "BC"], {"A": (225, 16), "B": (90, 15), "C": (0, 16)}, mk, cap, sol=sol)


s = given(m("\\triangle ABC") + " में " + m(ang("A", PUR) + " = " + dg(90, PUR)) + "<br>" + m(sd("AB", RED) + " = " + sd("AC", RED)), m(ang("B", BLU)) + " और " + m(ang("C", BLU)))
s += NOFIG + solo(fig72_7(True, "हल की आकृति: AB = AC लाल, ∠A = 90° बैंगनी, ∠B = ∠C नीले"))
s += num(1, TH72)
s += chain((ang("C", BLU), ang("B", BLU) + " \\qquad \\ldots(1)", "AB = AC; AB के सामने ∠C और AC के सामने ∠B है"))
s += num(2, ASUM)
s += chain((ang("A", PUR) + " + " + ang("B", BLU) + " + " + ang("C", BLU), "180" + DEG, "△ABC के कोणों का योग"),
           (dg(90, PUR) + " + " + ang("B", BLU) + " + " + ang("B", BLU), "180" + DEG, "∠A = 90° और (1) से ∠C = ∠B रखने पर"),
           ("90" + DEG + " + 2" + ang("B", BLU), "180" + DEG, "∠B + ∠B = 2∠B"))
s += chain(("2" + ang("B", BLU), "180" + DEG + " - 90" + DEG, "+90° को पक्षांतर करने पर −90° हो जाता है"),
           ("2" + ang("B", BLU), "90" + DEG, "180 − 90 = 90"))
s += chain((ang("B", BLU), "\\dfrac{90^\\circ}{2}", "2 को पक्षांतर करने पर (गुणा → भाग)"),
           ("", dg(45, BLU), "90 ÷ 2 = 45"))
s += chain((ang("C", BLU), ang("B", BLU), "(1) से"), ("", dg(45, BLU), "∠B = 45°"))
s += tp("जाँच: " + m("90^\\circ + 45^\\circ + 45^\\circ = 180^\\circ") + " ✔")
s += ans("(i) " + m(ang("B", BLU) + " = " + dg(45, BLU)) + " (ii) " + m(ang("C", BLU) + " = " + dg(45, BLU)))
E2.append(("ABC एक समकोण त्रिभुज है, जिसमें " + m("\\angle A = 90^\\circ") + " और " + m("AB = AC") + " है। " + m("\\angle B") + " और " + m("\\angle C") + " ज्ञात कीजिए।", s))

# ---------- Q8 (no figure) ----------
assert 180 / 3 == 60
P28 = {"A": (165, 40), "B": (55, 230.5), "C": (275, 230.5)}
close1(dist(P28["A"], P28["B"]), dist(P28["B"], P28["C"]), 0.6)


def fig72_8(sol, cap):
    mk = [("t", "AB", 1, RED), ("t", "BC", 1, RED), ("t", "CA", 1, RED), ("a", "BAC", 1, BLU, 28), ("a", "ABC", 1, BLU, 28), ("a", "ACB", 1, BLU, 28),
          ("l", "BAC", "60°", BLU, 44), ("l", "ABC", "60°", BLU, 46), ("l", "ACB", "60°", BLU, 46)]
    return geo(330, 265, P28, [("AB", RED, 3), ("BC", RED, 3), ("CA", RED, 3)], {"A": (90, 15), "B": (210, 16), "C": (330, 16)}, mk, cap, sol=sol)


s = given(m("\\triangle ABC") + " समबाहु है: " + m(sd("AB", RED) + " = " + sd("BC", RED)) + " और " + m(sd("BC", RED) + " = " + sd("CA", RED)),
          "सिद्ध करना है: " + m(ang("A", BLU)) + ", " + m(ang("B", BLU)) + ", " + m(ang("C", BLU)) + " प्रत्येक " + m("60^\\circ"))
s += NOFIG + solo(fig72_8(True, "हल की आकृति: तीनों भुजाएँ बराबर (लाल), तीनों कोण बराबर (नीले)"))
s += num(1, TH72)
s += chain((ang("C", BLU), ang("B", BLU) + " \\qquad \\ldots(1)", "AB = AC; AB के सामने ∠C और AC के सामने ∠B"))
s += chain((ang("C", BLU), ang("A", BLU) + " \\qquad \\ldots(2)", "AB = BC; AB के सामने ∠C और BC के सामने ∠A"))
s += num(2, ASUM)
s += chain((ang("A", BLU) + " + " + ang("B", BLU) + " + " + ang("C", BLU), "180" + DEG, "△ABC के कोणों का योग"),
           (ang("C", BLU) + " + " + ang("C", BLU) + " + " + ang("C", BLU), "180" + DEG, "(2) से ∠A = ∠C, (1) से ∠B = ∠C रखने पर"),
           ("3" + ang("C", BLU), "180" + DEG, "∠C + ∠C + ∠C = 3∠C"))
s += chain((ang("C", BLU), "\\dfrac{180^\\circ}{3}", "3 को पक्षांतर करने पर (गुणा → भाग)"),
           ("", dg(60, BLU), "180 ÷ 3 = 60"))
s += chain((ang("A", BLU), ang("C", BLU), "(2) से"), ("", dg(60, BLU), ""))
s += chain((ang("B", BLU), ang("C", BLU), "(1) से"), ("", dg(60, BLU), ""))
s += ans("(i) " + m(ang("A", BLU) + " = " + dg(60, BLU)) + " (ii) " + m(ang("B", BLU) + " = " + dg(60, BLU)) + " (iii) " + m(ang("C", BLU) + " = " + dg(60, BLU))
         + " — समबाहु त्रिभुज का प्रत्येक कोण 60° है।")
E2.append(("दर्शाइए कि किसी समबाहु त्रिभुज का प्रत्येक कोण " + m("60^\\circ") + " होता है।", s))

# =====================================================================
# Exercise 7.3
# =====================================================================
E3 = []

# ---------- Q1 (आकृति 7.39) ----------
P31 = {"A": (180, 30), "B": (55, 235), "C": (305, 235), "D": (180, 140)}
P31["P"] = mid(P31["B"], P31["C"])


def fig739(sol, cap):
    mk = []
    if sol:
        mk = [("t", "AB", 1, RED), ("t", "AC", 1, RED), ("t", "BD", 2, ORG), ("t", "DC", 2, ORG), ("a", "BAD", 1, BLU, 40), ("a", "DAC", 1, BLU, 40),
              ("a", "BDP", 2, TEA, 26), ("a", "PDC", 2, TEA, 26), ("t", "BP", 3, BROWN), ("t", "PC", 3, BROWN), ("r", "APC", PUR), ("r", "BPA", PUR)]
    segs = [("AB", RED, 3), ("AC", RED, 3), ("BD", ORG, 3), ("DC", ORG, 3), ("AD", GRN, 3.4), ("DP", GRN, 3.4, "6 4"), ("BP", BROWN, 3), ("PC", BROWN, 3)] if sol \
        else ["AB", "AC", "BD", "DC", "AP", "BC"]
    return geo(360, 270, P31, segs, {"A": (90, 15), "B": (200, 16), "C": (340, 16), "D": (30, 17), "P": (270, 17)}, mk, cap, sol=sol)


s = given(m("\\triangle ABC") + " में " + m(sd("AB", RED) + " = " + sd("AC", RED)) + "<br>" + m("\\triangle DBC") + " में " + m(sd("DB", ORG) + " = " + sd("DC", ORG))
          + "<br>A, D भुजा BC के एक ही ओर; AD बढ़ाने पर BC को P पर काटती है",
          "सिद्ध करना है:<br>(i) " + m("\\triangle ABD \\cong \\triangle ACD") + "<br>(ii) " + m("\\triangle ABP \\cong \\triangle ACP")
          + "<br>(iii) AP, ∠A और ∠D को समद्विभाजित करता है<br>(iv) AP, BC का लम्ब समद्विभाजक है")
s += figs(fig739, "आकृति 7.39", "AB = AC लाल (एक), DB = DC नारंगी (दो), BP = PC भूरी (तीन निशान); AD, DP हरी")
s += key((RED, "AB = AC"), (ORG, "DB = DC"), (GRN, "AD, AP, DP उभयनिष्ठ"), (BLU, "∠BAD = ∠CAD"), (TEA, "∠BDP = ∠CDP"), (BROWN, "BP = CP"), (PUR, "∠APB = ∠APC"))
s += kh("(i) " + m("\\triangle ABD \\cong \\triangle ACD"))
s += num(1, SSS)
s += kk(m("\\triangle ABD") + " और " + m("\\triangle ACD") + " में,",
        [(sd("AB", RED) + " = " + sd("AC", RED), "दिया है (△ABC समद्विबाहु)", "S", RED),
         (sd("BD", ORG) + " = " + sd("CD", ORG), "दिया है (△DBC समद्विबाहु)", "S", ORG),
         (sd("AD", GRN) + " = " + sd("AD", GRN), "उभयनिष्ठ भुजा", "S", GRN)],
        ("\\triangle ABD \\cong \\triangle ACD", "SSS सर्वांगसमता नियम द्वारा"),
        [("A", "A"), ("B", "C"), ("D", "D")])
s += num(2, CPCT)
s += kk("", [(ang("BAD", BLU) + " = " + ang("CAD", BLU) + " \\quad (1)", "CPCT (B ↔ C)")])
s += kh("(ii) " + m("\\triangle ABP \\cong \\triangle ACP"))
s += num(3, SAS)
s += kk(m("\\triangle ABP") + " और " + m("\\triangle ACP") + " में,",
        [(sd("AB", RED) + " = " + sd("AC", RED), "दिया है", "S", RED),
         (ang("BAP", BLU) + " = " + ang("CAP", BLU), "(1) से (∠BAP = ∠BAD, ∠CAP = ∠CAD)", "A", BLU),
         (sd("AP", GRN) + " = " + sd("AP", GRN), "उभयनिष्ठ भुजा", "S", GRN)],
        ("\\triangle ABP \\cong \\triangle ACP", "SAS सर्वांगसमता नियम द्वारा"),
        [("A", "A"), ("B", "C"), ("P", "P")])
s += kk("(ii) से CPCT द्वारा:", [(sd("BP", BROWN) + " = " + sd("CP", BROWN) + " \\quad (2)", "CPCT (B ↔ C)"),
                                 (ang("APB", PUR) + " = " + ang("APC", PUR) + " \\quad (3)", "CPCT (B ↔ C)")])
s += kh("(iii) AP, ∠A और ∠D दोनों को समद्विभाजित करता है")
s += p("(1) से " + m(ang("BAP", BLU) + " = " + ang("CAP", BLU)) + ", अतः AP, ∠A को समद्विभाजित करता है।")
s += kk(m("\\triangle BDP") + " और " + m("\\triangle CDP") + " में,",
        [(sd("BD", ORG) + " = " + sd("CD", ORG), "दिया है", "S", ORG),
         (sd("DP", GRN) + " = " + sd("DP", GRN), "उभयनिष्ठ भुजा", "S", GRN),
         (sd("BP", BROWN) + " = " + sd("CP", BROWN), "(2) से", "S", BROWN)],
        ("\\triangle BDP \\cong \\triangle CDP", "SSS सर्वांगसमता नियम द्वारा"),
        [("B", "C"), ("D", "D"), ("P", "P")])
s += kk("", [(ang("BDP", TEA) + " = " + ang("CDP", TEA), "CPCT (B ↔ C)")])
s += p("अतः AP (अर्थात् उसका भाग DP), ∠D (∠BDC) को समद्विभाजित करता है।")
s += kh("(iv) AP, BC का लम्ब समद्विभाजक है")
s += num(4, LINEAR)
s += chain((ang("APB", PUR) + " + " + ang("APC", PUR), "180" + DEG, "किरण PA रेखा BC पर खड़ी है (रैखिक युग्म)"),
           (ang("APB", PUR) + " + " + ang("APB", PUR), "180" + DEG, "(3) से ∠APC = ∠APB रखने पर"),
           ("2" + ang("APB", PUR), "180" + DEG, "∠APB + ∠APB = 2∠APB"))
s += chain((ang("APB", PUR), "\\dfrac{180^\\circ}{2}", "2 को पक्षांतर करने पर (गुणा → भाग)"), ("", dg(90, PUR), "180 ÷ 2 = 90"))
s += p("अतः " + m("AP \\perp BC") + " और (2) से " + m(sd("BP", BROWN) + " = " + sd("CP", BROWN)) + "; इसलिए AP, BC का लम्ब समद्विभाजक है।")
s += ans("(i) " + m("\\triangle ABD \\cong \\triangle ACD") + " (SSS) (ii) " + m("\\triangle ABP \\cong \\triangle ACP") + " (SAS) (iii) "
         + m(ang("BAP", BLU) + " = " + ang("CAP", BLU)) + " और " + m(ang("BDP", TEA) + " = " + ang("CDP", TEA)) + " (iv) " + m("AP \\perp BC") + " और "
         + m("BP = CP") + " — सभी सिद्ध हुए।")
E3.append((m("\\triangle ABC") + " और " + m("\\triangle DBC") + " एक ही आधार " + m("BC") + " पर बने दो समद्विबाहु त्रिभुज इस प्रकार हैं कि " + m("A") + " और " + m("D")
           + " भुजा " + m("BC") + " के एक ही ओर स्थित हैं (देखिए आकृति 7.39)। यदि " + m("AD") + " बढ़ाने पर " + m("BC") + " को " + m("P") + " पर प्रतिच्छेद करे, तो दर्शाइए कि "
           + "(i) " + m("\\triangle ABD \\cong \\triangle ACD") + " (ii) " + m("\\triangle ABP \\cong \\triangle ACP") + " (iii) " + m("AP") + " कोण " + m("A") + " और कोण " + m("D")
           + " दोनों को समद्विभाजित करता है। (iv) " + m("AP") + " रेखाखंड " + m("BC") + " का लम्ब समद्विभाजक है।", s))

# ---------- Q2 (no figure) ----------
P32 = {"A": (180, 35), "B": (60, 235), "C": (300, 235)}
P32["D"] = foot(P32["A"], P32["B"], P32["C"])


def fig73_2(sol, cap):
    mk = [("t", "AB", 1, RED), ("t", "AC", 1, RED), ("r", "ADC", PUR), ("r", "BDA", PUR), ("t", "BD", 2, ORG), ("t", "DC", 2, ORG),
          ("a", "BAD", 1, BLU, 40), ("a", "DAC", 1, BLU, 40)]
    return geo(360, 265, P32, [("AB", RED, 3), ("AC", RED, 3), ("AD", GRN, 3.4), ("BD", ORG, 3), ("DC", ORG, 3)],
               {"A": (90, 15), "B": (200, 15), "C": (340, 15), "D": (270, 17)}, mk, cap, fills=(("ABD", BLU), ("ACD", ORG)), sol=sol)


s = given(m("\\triangle ABC") + " में " + m(sd("AB", RED) + " = " + sd("AC", RED)) + "<br>" + m("AD") + " शीर्षलम्ब है: " + m("AD \\perp BC"),
          "सिद्ध करना है:<br>(i) " + m(sd("BD", ORG) + " = " + sd("CD", ORG)) + "<br>(ii) " + m(ang("BAD", BLU) + " = " + ang("CAD", BLU)))
s += NOFIG + solo(fig73_2(True, "हल की आकृति: कर्ण AB = AC लाल, समकोण बैंगनी, AD हरी (उभयनिष्ठ)"))
s += key((RED, "कर्ण AB = AC"), (PUR, "समकोण"), (GRN, "AD उभयनिष्ठ"), (ORG, "BD, CD"), (BLU, "∠BAD, ∠CAD"))
s += num(1, RHS)
s += kk("समकोण " + m("\\triangle ADB") + " और समकोण " + m("\\triangle ADC") + " में,",
        [(ang("ADB", PUR) + " = " + ang("ADC", PUR), "दोनों 90° हैं (AD ⊥ BC)", "R", PUR),
         (sd("AB", RED) + " = " + sd("AC", RED), "दिया है (दोनों कर्ण हैं)", "H", RED),
         (sd("AD", GRN) + " = " + sd("AD", GRN), "उभयनिष्ठ भुजा", "S", GRN)],
        ("\\triangle ADB \\cong \\triangle ADC", "RHS सर्वांगसमता नियम द्वारा"),
        [("A", "A"), ("D", "D"), ("B", "C")])
s += num(2, CPCT)
s += kh("(i)")
s += kk("", [(sd("BD", ORG) + " = " + sd("CD", ORG), "CPCT (B ↔ C)")])
s += p("अतः AD, रेखाखंड BC को समद्विभाजित करता है।")
s += kh("(ii)")
s += kk("", [(ang("BAD", BLU) + " = " + ang("CAD", BLU), "CPCT (B ↔ C)")])
s += p("अतः AD, कोण A को समद्विभाजित करता है।")
s += ans("(i) " + m(sd("BD", ORG) + " = " + sd("CD", ORG)) + ", AD रेखाखंड BC को समद्विभाजित करता है (ii) " + m(ang("BAD", BLU) + " = " + ang("CAD", BLU)) + ", AD कोण A को समद्विभाजित करता है।")
E3.append((m("AD") + " एक समद्विबाहु त्रिभुज " + m("ABC") + " का एक शीर्षलम्ब है, जिसमें " + m("AB = AC") + " है। दर्शाइए कि (i) " + m("AD") + " रेखाखंड " + m("BC")
           + " को समद्विभाजित करता है। (ii) " + m("AD") + " कोण " + m("A") + " को समद्विभाजित करता है।", s))

# ---------- Q3 (आकृति 7.40) ----------
A33, B33, C33 = (95, 40), (30, 170), (190, 190)
dx = 200
P33 = {"A": A33, "B": B33, "C": C33, "P": (A33[0] + dx, A33[1]), "Q": (B33[0] + dx, B33[1]), "R": (C33[0] + dx, C33[1])}
P33["M"] = mid(B33, C33)
P33["N"] = mid(P33["Q"], P33["R"])


def fig740(sol, cap):
    if sol:
        mk = [("t", "AB", 1, RED), ("t", "PQ", 1, RED), ("t", "BM", 2, ORG), ("t", "MC", 2, ORG), ("t", "QN", 2, ORG), ("t", "NR", 2, ORG),
              ("t", "AM", 3, TEA), ("t", "PN", 3, TEA), ("a", "ABM", 1, BLU, 26), ("a", "PQN", 1, BLU, 26)]
        segs = [("AB", RED, 3), ("PQ", RED, 3), ("BM", ORG, 3), ("MC", ORG, 3), ("QN", ORG, 3), ("NR", ORG, 3), ("AM", TEA, 3), ("PN", TEA, 3), "AC", "PR"]
    else:
        mk = [("t", "AB", 1, INK), ("t", "PQ", 1, INK), ("q", "BM", INK), ("q", "QN", INK), ("t", "AM", 2, INK), ("t", "PN", 2, INK)]
        segs = ["AB", "BC", "CA", "AM", "PQ", "QR", "RP", "PN"]
    return geo(410, 225, P33, segs, {"A": (90, 15), "B": (190, 15), "C": (0, 15), "M": (270, 17), "P": (90, 15), "Q": (190, 15), "R": (0, 15), "N": (270, 17)},
               mk, cap, fills=(("ABM", BLU), ("PQN", ORG)), sol=sol)


s = given(m(sd("AB", RED) + " = " + sd("PQ", RED)) + "<br>" + m("BC = QR") + "<br>माध्यिकाएँ " + m(sd("AM", TEA) + " = " + sd("PN", TEA))
          + "<br>(M, BC का और N, QR का मध्य-बिंदु)",
          "सिद्ध करना है:<br>(i) " + m("\\triangle ABM \\cong \\triangle PQN") + "<br>(ii) " + m("\\triangle ABC \\cong \\triangle PQR"))
s += figs(fig740, "आकृति 7.40", "AB = PQ लाल, BM = QN नारंगी (MC, NR भी उतने ही), AM = PN हरे-नीले; ∠B = ∠Q नीले")
s += key((RED, "AB = PQ"), (ORG, "BM = QN"), (TEA, "AM = PN"), (BLU, "∠B = ∠Q"))
s += kh("(i) " + m("\\triangle ABM \\cong \\triangle PQN"))
s += num(1, EQ_HALF)
s += chain(("BC", "QR \\qquad \\ldots(1)", "दिया है"))
s += chain(("\\dfrac{1}{2}BC", "\\dfrac{1}{2}QR", "(1) के दोनों पक्षों को 2 से भाग देने पर"))
s += chain((sd("BM", ORG), sd("QN", ORG) + " \\qquad \\ldots(2)", "M, BC का मध्य-बिंदु (BM = ½BC); N, QR का मध्य-बिंदु (QN = ½QR)"))
s += num(2, SSS)
s += kk(m("\\triangle ABM") + " और " + m("\\triangle PQN") + " में,",
        [(sd("AB", RED) + " = " + sd("PQ", RED), "दिया है", "S", RED),
         (sd("BM", ORG) + " = " + sd("QN", ORG), "(2) से", "S", ORG),
         (sd("AM", TEA) + " = " + sd("PN", TEA), "दिया है (माध्यिकाएँ)", "S", TEA)],
        ("\\triangle ABM \\cong \\triangle PQN", "SSS सर्वांगसमता नियम द्वारा"),
        [("A", "P"), ("B", "Q"), ("M", "N")])
s += kh("(ii) " + m("\\triangle ABC \\cong \\triangle PQR"))
s += num(3, CPCT)
s += kk("", [(ang("ABM", BLU) + " = " + ang("PQN", BLU), "(i) से CPCT (B ↔ Q)"),
             (ang("ABC", BLU) + " = " + ang("PQR", BLU) + " \\quad (3)", "∠ABM ही ∠ABC है और ∠PQN ही ∠PQR है (M, BC पर; N, QR पर)")])
s += num(4, SAS)
s += kk(m("\\triangle ABC") + " और " + m("\\triangle PQR") + " में,",
        [(sd("AB", RED) + " = " + sd("PQ", RED), "दिया है", "S", RED),
         (ang("ABC", BLU) + " = " + ang("PQR", BLU), "(3) से", "A", BLU),
         ("BC = QR", "दिया है", "S", ORG)],
        ("\\triangle ABC \\cong \\triangle PQR", "SAS सर्वांगसमता नियम द्वारा"),
        [("A", "P"), ("B", "Q"), ("C", "R")])
s += ans("(i) " + m("\\triangle ABM \\cong \\triangle PQN") + " (SSS) (ii) " + m("\\triangle ABC \\cong \\triangle PQR") + " (SAS) — दोनों सिद्ध हुए।")
E3.append(("एक त्रिभुज " + m("ABC") + " की दो भुजाएँ " + m("AB") + " और " + m("BC") + " तथा माध्यिका " + m("AM") + " क्रमशः एक दूसरे त्रिभुज की भुजाओं " + m("PQ") + " और "
           + m("QR") + " तथा माध्यिका " + m("PN") + " के बराबर हैं (देखिए आकृति 7.40)। दर्शाइए कि (i) " + m("\\triangle ABM \\cong \\triangle PQN") + " (ii) "
           + m("\\triangle ABC \\cong \\triangle PQR"), s))

# ---------- Q4 (no figure) ----------


def fig73_4(sol, cap):
    mk = [("r", "AFC", PUR), ("r", "AEB", PUR), ("t", "BE", 2, ORG, .4), ("t", "CF", 2, ORG, .4), ("a", "EBC", 1, BLU, 40), ("a", "FCB", 1, BLU, 40)]
    P = dict(P23)
    return geo(360, 265, P, [("AB", RED, 2.6), ("AC", RED, 2.6), ("BC", GRN, 3.4), ("BE", ORG, 3), ("CF", ORG, 3)],
               {"A": (90, 15), "B": (200, 15), "C": (340, 15), "E": (20, 15), "F": (160, 15)}, mk, cap, fills=(("BEC", BLU), ("CFB", ORG)), sol=sol)


s = given(m("\\triangle ABC") + " में " + m("BE \\perp AC") + ", " + m("CF \\perp AB") + "<br>" + m(sd("BE", ORG) + " = " + sd("CF", ORG)),
          "सिद्ध करना है (RHS से): " + m("\\triangle ABC") + " समद्विबाहु है, अर्थात् " + m(sd("AB", RED) + " = " + sd("AC", RED)))
s += NOFIG + solo(fig73_4(True, "हल की आकृति: BE = CF नारंगी, कर्ण BC हरी (उभयनिष्ठ), समकोण बैंगनी"))
s += key((ORG, "BE = CF"), (GRN, "कर्ण BC उभयनिष्ठ"), (PUR, "समकोण ∠BEC, ∠CFB"), (BLU, "∠ECB = ∠FBC"), (RED, "AB, AC"))
s += num(1, RHS)
s += kk("समकोण " + m("\\triangle BEC") + " और समकोण " + m("\\triangle CFB") + " में,",
        [(ang("BEC", PUR) + " = " + ang("CFB", PUR), "दोनों 90° हैं (BE ⊥ AC, CF ⊥ AB)", "R", PUR),
         (sd("BC", GRN) + " = " + sd("CB", GRN), "उभयनिष्ठ कर्ण", "H", GRN),
         (sd("BE", ORG) + " = " + sd("CF", ORG), "दिया है", "S", ORG)],
        ("\\triangle BEC \\cong \\triangle CFB", "RHS सर्वांगसमता नियम द्वारा"),
        [("B", "C"), ("E", "F"), ("C", "B")])
s += num(2, CPCT)
s += kk("", [(ang("ECB", BLU) + " = " + ang("FBC", BLU), "CPCT (C ↔ B)"),
             (ang("ACB", BLU) + " = " + ang("ABC", BLU), "∠ECB ही ∠ACB है और ∠FBC ही ∠ABC है")])
s += num(3, TH73)
s += kk("", [(sd("AB", RED) + " = " + sd("AC", RED), "बराबर कोणों की सम्मुख भुजाएँ: ∠ACB के सामने AB, ∠ABC के सामने AC")])
s += ans(m(sd("AB", RED) + " = " + sd("AC", RED)) + ", अतः " + m("\\triangle ABC") + " एक समद्विबाहु त्रिभुज है। सिद्ध हुआ।")
E3.append((m("BE") + " और " + m("CF") + " एक त्रिभुज " + m("ABC") + " के दो बराबर शीर्षलम्ब हैं। RHS सर्वांगसमता नियम का प्रयोग करके सिद्ध कीजिए कि " + m("\\triangle ABC")
           + " एक समद्विबाहु त्रिभुज है।", s))

# ---------- Q5 (no figure) ----------
P35 = {"A": (180, 35), "B": (60, 235), "C": (300, 235)}
P35["P"] = foot(P35["A"], P35["B"], P35["C"])


def fig73_5(sol, cap):
    mk = [("t", "AB", 1, RED), ("t", "AC", 1, RED), ("r", "APC", PUR), ("r", "BPA", PUR), ("a", "ABP", 1, BLU, 34), ("a", "ACP", 1, BLU, 34)]
    return geo(360, 265, P35, [("AB", RED, 3), ("AC", RED, 3), ("AP", GRN, 3.4, "7 4"), "BC"],
               {"A": (90, 15), "B": (200, 15), "C": (340, 15), "P": (270, 17)}, mk, cap, fills=(("ABP", BLU), ("ACP", ORG)), sol=sol)


s = given(m("\\triangle ABC") + " में " + m(sd("AB", RED) + " = " + sd("AC", RED)), "सिद्ध करना है: " + m(ang("B", BLU) + " = " + ang("C", BLU)))
s += NOFIG + solo(fig73_5(True, "हल की आकृति: रचना AP ⊥ BC (हरी बिंदुदार); कर्ण AB = AC लाल"))
s += key((RED, "कर्ण AB = AC"), (PUR, "समकोण"), (GRN, "AP उभयनिष्ठ"), (BLU, "∠B, ∠C"))
s += p("<b>रचना:</b> " + m("A") + " से " + m("BC") + " पर लम्ब " + m("AP") + " खींचिए।")
s += num(1, RHS)
s += kk("समकोण " + m("\\triangle APB") + " और समकोण " + m("\\triangle APC") + " में,",
        [(ang("APB", PUR) + " = " + ang("APC", PUR), "दोनों 90° हैं (रचना से AP ⊥ BC)", "R", PUR),
         (sd("AB", RED) + " = " + sd("AC", RED), "दिया है (दोनों कर्ण हैं)", "H", RED),
         (sd("AP", GRN) + " = " + sd("AP", GRN), "उभयनिष्ठ भुजा", "S", GRN)],
        ("\\triangle APB \\cong \\triangle APC", "RHS सर्वांगसमता नियम द्वारा"),
        [("A", "A"), ("P", "P"), ("B", "C")])
s += num(2, CPCT)
s += kk("", [(ang("ABP", BLU) + " = " + ang("ACP", BLU), "CPCT (B ↔ C)"),
             (ang("B", BLU) + " = " + ang("C", BLU), "∠ABP ही ∠B है और ∠ACP ही ∠C है")])
s += ans(m(ang("B", BLU) + " = " + ang("C", BLU)) + " सिद्ध हुआ।")
E3.append(("ABC एक समद्विबाहु त्रिभुज है जिसमें " + m("AB = AC") + " है। " + m("AP \\perp BC") + " खींच कर दर्शाइए कि " + m("\\angle B = \\angle C") + " है।", s))

# ---------------------------------------------------------------------
assert (len(E1), len(E2), len(E3)) == (8, 8, 5)
E1 = [(qt(a), b) for a, b in E1]
E2 = [(qt(a), b) for a, b in E2]
E3 = [(qt(a), b) for a, b in E3]
for E in (E1, E2, E3):
    check_tex(E)
SUB = "कक्षा 9 गणित · अध्याय 7: " + CH + " · {} प्रश्न"
page(BASE, 7, CH, "exercise-7-1", "प्रश्नावली 7.1", SUB.format(len(E1)), E1,
     ("/hi/class-09/maths/chapter-06/exercise-6-2/", "प्रश्नावली 6.2"), (BASE + "exercise-7-2/", "प्रश्नावली 7.2"), css=CSS + EXTRA_CSS, boards=BOARDS9)
page(BASE, 7, CH, "exercise-7-2", "प्रश्नावली 7.2", SUB.format(len(E2)), E2,
     (BASE + "exercise-7-1/", "प्रश्नावली 7.1"), (BASE + "exercise-7-3/", "प्रश्नावली 7.3"), css=CSS + EXTRA_CSS, boards=BOARDS9)
page(BASE, 7, CH, "exercise-7-3", "प्रश्नावली 7.3", SUB.format(len(E3)), E3,
     (BASE + "exercise-7-2/", "प्रश्नावली 7.2"), ("/hi/class-09/maths/chapter-08/exercise-8-1/", "प्रश्नावली 8.1"), css=CSS + EXTRA_CSS, boards=BOARDS9)
print("ok")
