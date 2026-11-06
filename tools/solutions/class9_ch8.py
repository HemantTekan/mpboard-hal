#!/usr/bin/env python3
"""Class 9 Maths, Chapter 8 (चतुर्भुज): Exercises 8.1 and 8.2, Hindi medium.
Rationalised book (2023-24 onward; iemh108 'Rationalised 2023-24' = 'Reprint 2025-26'):
  8.1 keeps old questions 2, 4, 6, 8, 9, 10, 12 -> renumbered 1-7 (old 1, 3, 5, 7, 11 removed);
  8.2 keeps old questions 1-5 and 7 -> renumbered 1-6 (old 6 removed).
  Figures renumbered like the current book: old 8.19, 8.20, 8.21, 8.23 -> 8.11, 8.12, 8.13, 8.14;
  old 8.29, 8.30, 8.31 -> 8.20, 8.21, 8.22.  Theorems: old 8.8 (one pair equal and parallel) removed,
  so the mid-point theorem is now प्रमेय 8.8 and its converse प्रमेय 8.9 (not used: the removed theorem).
Question text and figures copied from NCERT Hindi PDF ihmh108 (archive.org ncert-ihmh1, 2020-21 print).
Style as chapters 6 and 7: every side/angle has one colour in the solution figure and the same colour in the working;
equal sides carry matching coloured ticks, equal angles matching arcs, parallel sides arrow-heads, right angles squares.
Run from repo root: python3 tools/solutions/class9_ch8.py
"""
import sys, pathlib, math
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from common import *  # noqa
from mixed_cells import *  # noqa

BASE = "/hi/class-09/maths/chapter-08/"
CH = "चतुर्भुज"
BOARDS9 = ("यह हल <b>MP Board (MPBSE)</b> कक्षा 9 गणित की पाठ्यपुस्तक के अध्याय 8 ‘चतुर्भुज’ के अनुसार है।")
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
        self.id, self.W, self.H, self.bg, self.el, self.top, self.marks = f"f8{Fig.n}", W, H, [], [], [], {}

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


def geo(W, H, P, segs, labels, marks, cap, fills=(), extra=None, sol=True):
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


# ---------------- more theorems as stated in the book ----------------
CORR = ax("संगत कोण अभिगृहीत", "यदि एक तिर्यक रेखा दो समांतर रेखाओं को प्रतिच्छेद करे, तो संगत कोणों का प्रत्येक युग्म बराबर होता है।")
TH66 = ax("प्रमेय 6.6", "वे रेखाएँ जो एक ही रेखा के समांतर हों, परस्पर समांतर होती हैं।")
TH82 = ax("प्रमेय 8.2", "एक समांतर चतुर्भुज में सम्मुख भुजाएँ बराबर होती हैं।")
TH83 = ax("प्रमेय 8.3", "यदि एक चतुर्भुज की सम्मुख भुजाओं का प्रत्येक युग्म बराबर हो, तो वह एक समांतर चतुर्भुज होता है।")
TH84 = ax("प्रमेय 8.4", "एक समांतर चतुर्भुज में सम्मुख कोण बराबर होते हैं।")
TH86 = ax("प्रमेय 8.6", "समांतर चतुर्भुज के विकर्ण एक दूसरे को (परस्पर) समद्विभाजित करते हैं।")
MPT = ax("प्रमेय 8.8 (मध्य-बिंदु प्रमेय)", "किसी त्रिभुज की किन्हीं दो भुजाओं के मध्य-बिंदुओं को मिलाने वाला रेखाखंड तीसरी भुजा के समांतर होता है। "
         "(पुस्तक: साथ ही यह रेखाखंड तीसरी भुजा का आधा होता है, " + m("EF = \\dfrac{1}{2}BC") + "।)")
MPT_C = ax("प्रमेय 8.9 (मध्य-बिंदु प्रमेय का विलोम)", "किसी त्रिभुज की एक भुजा के मध्य-बिंदु से दूसरी भुजा के समांतर खींची गई रेखा तीसरी भुजा को समद्विभाजित करती है।")
D_PGM = ax("समांतर चतुर्भुज", "वह चतुर्भुज जिसकी सम्मुख भुजाओं के दोनों युग्म समांतर हों, समांतर चतुर्भुज कहलाता है।")
D_RECT = ax("आयत", "आयत वह समांतर चतुर्भुज है जिसका एक कोण समकोण हो।")
D_RHOM = ax("समचतुर्भुज", "वह समांतर चतुर्भुज जिसकी सभी भुजाएँ बराबर हों, समचतुर्भुज कहलाता है।")
D_SQ = ax("वर्ग", "वह समांतर चतुर्भुज जिसका एक कोण समकोण हो और सभी भुजाएँ बराबर हों, वर्ग कहलाता है।")
EX1 = ax("उदाहरण 1 (पुस्तक)", "आयत का प्रत्येक कोण समकोण होता है।")
EX2 = ax("उदाहरण 2 (पुस्तक)", "समचतुर्भुज के विकर्ण परस्पर लम्ब होते हैं।")
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


# =====================================================================
# Exercise 8.1
# =====================================================================
E1 = []

# ---------- Q1 (no figure): parallelogram with equal diagonals is a rectangle ----------
P11 = {"A": (60, 235), "B": (300, 235), "C": (300, 50), "D": (60, 50)}
pgram(P11, "A", "B", "C", "D")
close1(dist(P11["A"], P11["C"]), dist(P11["B"], P11["D"]), 1e-6)


def fig81_1(sol, cap):
    mk = [("t", "AB", 1, RED), ("t", "DC", 1, RED), ("t", "AC", 2, ORG, .28), ("t", "BD", 2, ORG, .28),
          ("p", "AB", 1, RED, .7), ("p", "DC", 1, RED, .7), ("p", "AD", 2, INK, .72), ("p", "BC", 2, GRN, .72),
          ("r", "ABC", PUR), ("r", "DCB", PUR)]
    segs = [("AB", RED, 3), ("DC", RED, 3), ("BC", GRN, 3.4), "AD", ("AC", ORG, 2.6), ("BD", ORG, 2.6)]
    return geo(360, 280, P11, segs, {"A": (225, 17), "B": (315, 17), "C": (45, 17), "D": (135, 17)}, mk, cap,
               fills=(("ABC", BLU), ("DCB", ORG)), sol=sol)


s = given("ABCD एक समांतर चतुर्भुज है: " + m("AB \\parallel DC") + ", " + m("AD \\parallel BC") + "<br>विकर्ण " + m(sd("AC", ORG) + " = " + sd("BD", ORG)),
          "सिद्ध करना है: ABCD एक आयत है (अर्थात् इसका एक कोण " + m("90^\\circ") + " है)")
s += NOFIG + solo(fig81_1(True, "हल की आकृति: AB = DC लाल, BC हरी (उभयनिष्ठ), बराबर विकर्ण नारंगी"))
s += key((RED, "AB = DC"), (GRN, "BC उभयनिष्ठ"), (ORG, "AC = DB (विकर्ण)"), (PUR, "∠ABC, ∠DCB"))
s += num(1, TH82)
s += num(2, SSS)
s += kk(m("\\triangle ABC") + " और " + m("\\triangle DCB") + " में,",
        [(sd("AB", RED) + " = " + sd("DC", RED) + " \\quad (1)", "समांतर चतुर्भुज की सम्मुख भुजाएँ (प्रमेय 8.2)", "S", RED),
         (sd("BC", GRN) + " = " + sd("CB", GRN) + " \\quad (2)", "उभयनिष्ठ भुजा", "S", GRN),
         (sd("AC", ORG) + " = " + sd("DB", ORG) + " \\quad (3)", "दिया है (विकर्ण बराबर हैं)", "S", ORG)],
        ("\\triangle ABC \\cong \\triangle DCB", "(1), (2), (3) से, SSS सर्वांगसमता नियम द्वारा"),
        [("A", "D"), ("B", "C"), ("C", "B")])
s += num(3, CPCT)
s += kk("", [(ang("ABC", PUR) + " = " + ang("DCB", PUR) + " \\quad (4)", "CPCT (शीर्ष B ↔ C)")])
s += num(4, INT)
s += chain((ang("ABC", PUR) + " + " + ang("DCB", PUR), "180" + DEG, "AB ∥ DC, तिर्यक रेखा BC — एक ही ओर के अंतः कोण"),
           (ang("ABC", PUR) + " + " + ang("ABC", PUR), "180" + DEG, "(4) से ∠DCB = ∠ABC रखने पर"),
           ("2" + ang("ABC", PUR), "180" + DEG, "∠ABC + ∠ABC = 2∠ABC"))
s += chain((ang("ABC", PUR), "\\dfrac{180^\\circ}{2}", "2 को पक्षांतर करने पर (गुणा → भाग)"),
           ("", dg(90, PUR), "180 ÷ 2 = 90"))
s += num(5, D_RECT)
s += p("समांतर चतुर्भुज ABCD का एक कोण " + m(ang("ABC", PUR) + " = 90^\\circ") + " है, इसलिए ABCD एक आयत है।")
s += ans("समांतर चतुर्भुज ABCD में " + m("\\angle B = 90^\\circ") + ", अतः ABCD एक आयत है। सिद्ध हुआ।")
E1.append(("यदि एक समांतर चतुर्भुज के विकर्ण बराबर हों, तो दर्शाइए कि वह एक आयत है।", s))

# ---------- Q2 (no figure): diagonals of a square ----------
P12 = {"A": (70, 245), "B": (280, 245), "C": (280, 35), "D": (70, 35)}
P12["O"] = inter(P12["A"], P12["C"], P12["B"], P12["D"])
close1(dist(P12["O"], P12["A"]), dist(P12["O"], P12["C"]), 1e-6)
perp_(P12["A"], P12["C"], P12["B"], P12["D"])


def fig81_2(sol, cap):
    mk = [("t", "AB", 1, RED), ("t", "BC", 1, RED), ("t", "CD", 1, RED), ("t", "DA", 1, RED),
          ("r", "DAB", PUR), ("r", "ABC", PUR), ("r", "BCD", INK), ("r", "CDA", INK),
          ("t", "OA", 2, BLU), ("t", "OC", 2, BLU), ("t", "OB", 3, ORG), ("t", "OD", 3, ORG),
          ("r", "AOB", TEA), ("r", "AOD", TEA)]
    segs = [("AB", RED, 3), ("BC", RED, 3), ("CD", RED, 3), ("DA", RED, 3), ("OA", BLU, 3), ("OC", BLU, 3), ("OB", ORG, 3), ("OD", ORG, 3)]
    return geo(350, 280, P12, segs, {"A": (225, 17), "B": (315, 17), "C": (45, 17), "D": (135, 17), "O": (0, 19)}, mk, cap,
               fills=(("ABC", BLU), ("BAD", ORG)), sol=sol)


s = given("ABCD एक वर्ग है: " + m(sd("AB", RED) + " = " + sd("BC", RED) + " = " + sd("CD", RED) + " = " + sd("DA", RED)) + "<br>प्रत्येक कोण "
          + m("90^\\circ") + "<br>विकर्ण AC और BD, बिंदु O पर मिलते हैं",
          "सिद्ध करना है:<br>(i) " + m("AC = BD") + "<br>(ii) " + m(sd("OA", BLU) + " = " + sd("OC", BLU)) + " और " + m(sd("OB", ORG) + " = " + sd("OD", ORG))
          + "<br>(iii) " + m(ang("AOB", TEA) + " = 90^\\circ"))
s += NOFIG + solo(fig81_2(True, "हल की आकृति: चारों भुजाएँ लाल (बराबर), OA = OC नीले, OB = OD नारंगी"))
s += key((RED, "वर्ग की भुजाएँ"), (PUR, "∠ABC = ∠BAD = 90°"), (BLU, "OA = OC"), (ORG, "OB = OD"), (TEA, "∠AOB, ∠AOD"))
s += kh("(i) विकर्ण बराबर हैं: " + m("AC = BD"))
s += num(1, SAS)
s += kk(m("\\triangle ABC") + " और " + m("\\triangle BAD") + " में,",
        [(sd("AB", RED) + " = " + sd("BA", RED) + " \\quad (1)", "उभयनिष्ठ भुजा", "S", RED),
         (ang("ABC", PUR) + " = " + ang("BAD", PUR) + " \\quad (2)", "वर्ग का प्रत्येक कोण 90° है", "A", PUR),
         (sd("BC", RED) + " = " + sd("AD", RED) + " \\quad (3)", "वर्ग की सभी भुजाएँ बराबर हैं", "S", RED)],
        ("\\triangle ABC \\cong \\triangle BAD", "(1), (2), (3) से, SAS सर्वांगसमता नियम द्वारा"),
        [("A", "B"), ("B", "A"), ("C", "D")])
s += num(2, CPCT)
s += kk("", [("AC = BD", "CPCT (A ↔ B, C ↔ D, इसलिए AC ↔ BD)")])
s += kh("(ii) विकर्ण परस्पर समद्विभाजित करते हैं")
s += num(3, TH86)
s += kk("वर्ग एक समांतर चतुर्भुज है, इसलिए", [(sd("OA", BLU) + " = " + sd("OC", BLU) + " \\quad (4)", "प्रमेय 8.6"),
                                            (sd("OB", ORG) + " = " + sd("OD", ORG) + " \\quad (5)", "प्रमेय 8.6")])
s += kh("(iii) विकर्ण समकोण पर मिलते हैं")
s += kk(m("\\triangle AOB") + " और " + m("\\triangle AOD") + " में,",
        [(sd("OB", ORG) + " = " + sd("OD", ORG), "(5) से", "S", ORG),
         (sd("AB", RED) + " = " + sd("AD", RED), "वर्ग की भुजाएँ", "S", RED),
         (sd("OA", BLU) + " = " + sd("OA", BLU), "उभयनिष्ठ भुजा", "S", BLU)],
        ("\\triangle AOB \\cong \\triangle AOD", "SSS सर्वांगसमता नियम द्वारा"),
        [("A", "A"), ("O", "O"), ("B", "D")])
s += num(4, SSS)
s += kk("", [(ang("AOB", TEA) + " = " + ang("AOD", TEA) + " \\quad (6)", "CPCT (B ↔ D)")])
s += num(5, LINEAR)
s += chain((ang("AOB", TEA) + " + " + ang("AOD", TEA), "180" + DEG, "किरण OA रेखा BD पर खड़ी है (रैखिक युग्म)"),
           (ang("AOB", TEA) + " + " + ang("AOB", TEA), "180" + DEG, "(6) से ∠AOD = ∠AOB रखने पर"),
           ("2" + ang("AOB", TEA), "180" + DEG, "∠AOB + ∠AOB = 2∠AOB"))
s += chain((ang("AOB", TEA), "\\dfrac{180^\\circ}{2}", "2 को पक्षांतर करने पर (गुणा → भाग)"),
           ("", dg(90, TEA), "180 ÷ 2 = 90"))
s += ans("(i) " + m("AC = BD") + " (विकर्ण बराबर हैं) (ii) " + m("OA = OC") + " और " + m("OB = OD") + " (विकर्ण परस्पर समद्विभाजित करते हैं) (iii) "
         + m("\\angle AOB = 90^\\circ") + " (विकर्ण समकोण पर मिलते हैं) — सिद्ध हुआ।")
E1.append(("दर्शाइए कि एक वर्ग के विकर्ण बराबर होते हैं और परस्पर समकोण पर समद्विभाजित करते हैं।", s))

# ---------- Q3 (आकृति 8.11) ----------
s3, a3 = 200, 72
A3 = (50, 235)
P13 = {"A": A3, "B": (A3[0] + s3, A3[1]), "D": Fig.pol(A3, a3, s3)}
P13["C"] = (P13["D"][0] + s3, P13["D"][1])
pgram(P13, "A", "B", "C", "D")
close1(angle_at(P13["A"], P13["D"], P13["C"]), angle_at(P13["A"], P13["C"], P13["B"]), 1e-6)   # AC bisects ∠A (rhombus)


def fig811(sol, cap):
    if sol:
        mk = [("a", "CAB", 1, BLU, 44), ("a", "DCA", 1, BLU, 44), ("a", "DAC", 1, ORG, 30), ("a", "ACB", 1, ORG, 30),
              ("t", "AB", 1, RED), ("t", "BC", 1, RED), ("t", "CD", 1, RED), ("t", "DA", 1, RED),
              ("p", "AB", 1, INK, .7), ("p", "DC", 1, INK, .7), ("p", "AD", 2, INK, .7), ("p", "BC", 2, INK, .7)]
        segs = [("AB", RED, 3), ("BC", RED, 3), ("CD", RED, 3), ("DA", RED, 3), ("AC", GRN, 3.2)]
    else:
        mk = [("a", "CAB", 1, INK, 24), ("a", "DAC", 1, INK, 30)]
        segs = ["AB", "BC", "CD", "DA", "AC"]
    return geo(370, 270, P13, segs, {"A": (200, 17), "B": (330, 17), "C": (30, 17), "D": (120, 17)}, mk, cap,
               fills=(("ABC", BLU), ("ACD", ORG)), sol=sol)


s = given("ABCD एक समांतर चतुर्भुज है: " + m("AB \\parallel DC") + ", " + m("AD \\parallel BC") + "<br>AC, ∠A को समद्विभाजित करता है: "
          + m(ang("DAC", ORG) + " = " + ang("BAC", BLU)),
          "सिद्ध करना है:<br>(i) AC, ∠C को समद्विभाजित करता है: " + m(ang("DCA", BLU) + " = " + ang("BCA", ORG)) + "<br>(ii) ABCD एक समचतुर्भुज है")
s += figs(fig811, "आकृति 8.11", "एकांतर कोणों के युग्म नीले और नारंगी, विकर्ण AC हरा")
s += key((BLU, "∠BAC = ∠DCA (एकांतर)"), (ORG, "∠DAC = ∠BCA (एकांतर)"), (GRN, "विकर्ण AC"), (RED, "भुजाएँ (सिद्ध करना है कि बराबर हैं)"))
s += kh("(i) AC, ∠C को समद्विभाजित करता है")
s += num(1, ALT)
s += chain((ang("DCA", BLU), ang("BAC", BLU) + " \\qquad \\ldots(1)", "AB ∥ DC, तिर्यक रेखा AC — एकांतर कोण"))
s += chain((ang("BCA", ORG), ang("DAC", ORG) + " \\qquad \\ldots(2)", "AD ∥ BC, तिर्यक रेखा AC — एकांतर कोण"))
s += chain((ang("DAC", ORG), ang("BAC", BLU) + " \\qquad \\ldots(3)", "दिया है (AC, ∠A को समद्विभाजित करता है)"))
s += chain((ang("DCA", BLU), ang("BAC", BLU), "(1) से"),
           ("", ang("DAC", ORG), "(3) से"),
           ("", ang("BCA", ORG), "(2) से"))
s += p("अतः " + m(ang("DCA", BLU) + " = " + ang("BCA", ORG)) + ", अर्थात् AC कोण C को भी समद्विभाजित करता है।")
s += kh("(ii) ABCD एक समचतुर्भुज है")
s += chain((ang("DAC", ORG), ang("BAC", BLU), "(3) से"),
           ("", ang("DCA", BLU) + " \\qquad \\ldots(4)", "(1) से"))
s += num(2, TH73)
s += kk(m("\\triangle DAC") + " में,", [(ang("DAC", ORG) + " = " + ang("DCA", BLU), "(4) से"),
                                     (sd("DC", RED) + " = " + sd("DA", RED) + " \\quad (5)", "बराबर कोणों की सम्मुख भुजाएँ: ∠DAC के सामने DC, ∠DCA के सामने DA")])
s += num(3, TH82)
s += chain((sd("AB", RED), sd("DC", RED), "समांतर चतुर्भुज की सम्मुख भुजाएँ"),
           ("", sd("DA", RED), "(5) से"),
           ("", sd("BC", RED), "समांतर चतुर्भुज की सम्मुख भुजाएँ"))
s += num(4, D_RHOM)
s += p("समांतर चतुर्भुज ABCD की चारों भुजाएँ बराबर हैं, इसलिए ABCD एक समचतुर्भुज है।")
s += ans("(i) " + m(ang("DCA", BLU) + " = " + ang("BCA", ORG)) + ", अर्थात् AC कोण C को भी समद्विभाजित करता है (ii) " + m("AB = BC = CD = DA")
         + ", अतः ABCD एक समचतुर्भुज है।")
E1.append(("समांतर चतुर्भुज ABCD का विकर्ण AC कोण A को समद्विभाजित करता है (देखिए आकृति 8.11)। दर्शाइए कि (i) यह " + m("\\angle C")
           + " को भी समद्विभाजित करता है। (ii) ABCD एक समचतुर्भुज है।", s))

# ---------- Q4 (no figure): rectangle whose diagonal AC bisects ∠A and ∠C ----------
P14 = {"A": (70, 245), "B": (280, 245), "C": (280, 35), "D": (70, 35)}


def fig81_4(sol, cap):
    mk = [("r", "DAB", PUR), ("r", "ABC", PUR), ("r", "BCD", PUR), ("r", "CDA", PUR),
          ("a", "CAB", 1, BLU, 44), ("a", "DAC", 1, BLU, 32), ("a", "BCA", 1, BLU, 44), ("a", "ACD", 1, BLU, 32),
          ("a", "ABD", 2, ORG, 44), ("a", "DBC", 2, ORG, 32), ("a", "CDB", 2, ORG, 44), ("a", "BDA", 2, ORG, 32),
          ("t", "AB", 1, RED), ("t", "BC", 1, RED), ("t", "CD", 1, RED), ("t", "DA", 1, RED)]
    segs = [("AB", RED, 3), ("BC", RED, 3), ("CD", RED, 3), ("DA", RED, 3), ("AC", GRN, 2.6), ("BD", TEA, 2.6)]
    return geo(350, 280, P14, segs, {"A": (225, 17), "B": (315, 17), "C": (45, 17), "D": (135, 17)}, mk, cap, sol=sol)


s = given("ABCD एक आयत है (प्रत्येक कोण " + m("90^\\circ") + ")<br>AC, ∠A और ∠C को समद्विभाजित करता है:<br>"
          + m(ang("DAC", BLU) + " = " + ang("BAC", BLU)) + " और " + m(ang("DCA", BLU) + " = " + ang("BCA", BLU)),
          "सिद्ध करना है:<br>(i) ABCD एक वर्ग है<br>(ii) BD, ∠B और ∠D को समद्विभाजित करता है")
s += NOFIG + solo(fig81_4(True, "हल की आकृति: AC से बने आधे कोण नीले, BD से बने आधे कोण नारंगी, समकोण बैंगनी"))
s += key((BLU, "AC से बने कोण"), (ORG, "BD से बने कोण"), (RED, "भुजाएँ"), (PUR, "समकोण"))
s += kh("(i) ABCD एक वर्ग है")
s += num(1, ALT)
s += chain((ang("DCA", BLU), ang("BAC", BLU) + " \\qquad \\ldots(1)", "AB ∥ DC, तिर्यक रेखा AC — एकांतर कोण"))
s += chain((ang("BAC", BLU), ang("DAC", BLU) + " \\qquad \\ldots(2)", "दिया है (AC, ∠A को समद्विभाजित करता है)"))
s += chain((ang("DCA", BLU), ang("BAC", BLU), "(1) से"),
           ("", ang("DAC", BLU) + " \\qquad \\ldots(3)", "(2) से"))
s += num(2, TH73)
s += kk(m("\\triangle ADC") + " में,", [(ang("DCA", BLU) + " = " + ang("DAC", BLU), "(3) से"),
                                     (sd("DA", RED) + " = " + sd("DC", RED) + " \\quad (4)", "बराबर कोणों की सम्मुख भुजाएँ: ∠DCA के सामने DA, ∠DAC के सामने DC")])
s += num(3, TH82)
s += chain((sd("AB", RED), sd("DC", RED), "आयत की सम्मुख भुजाएँ"),
           ("", sd("DA", RED), "(4) से"),
           ("", sd("BC", RED), "आयत की सम्मुख भुजाएँ"))
s += num(4, D_SQ)
s += p("ABCD एक समांतर चतुर्भुज (आयत) है, इसका " + m(ang("A", PUR) + " = 90^\\circ") + " है और चारों भुजाएँ बराबर हैं, इसलिए ABCD एक वर्ग है।")
s += kh("(ii) BD, ∠B और ∠D को समद्विभाजित करता है")
s += num(5, TH72)
s += kk(m("\\triangle BCD") + " में,", [(sd("CB", RED) + " = " + sd("CD", RED), "(i) से (वर्ग की भुजाएँ)"),
                                     (ang("CBD", ORG) + " = " + ang("CDB", ORG) + " \\quad (5)", "बराबर भुजाओं के सम्मुख कोण: CD के सामने ∠CBD, CB के सामने ∠CDB")])
s += num(6, ALT)
s += chain((ang("CDB", ORG), ang("ABD", ORG) + " \\qquad \\ldots(6)", "AB ∥ DC, तिर्यक रेखा BD — एकांतर कोण"))
s += chain((ang("CBD", ORG), ang("CDB", ORG), "(5) से"),
           ("", ang("ABD", ORG), "(6) से"))
s += p("अतः " + m(ang("CBD", ORG) + " = " + ang("ABD", ORG)) + ", अर्थात् BD कोण B को समद्विभाजित करता है।")
s += kk(m("\\triangle BAD") + " में,", [(sd("AB", RED) + " = " + sd("AD", RED), "(i) से (वर्ग की भुजाएँ)"),
                                     (ang("ADB", ORG) + " = " + ang("ABD", ORG) + " \\quad (7)", "बराबर भुजाओं के सम्मुख कोण: AB के सामने ∠ADB, AD के सामने ∠ABD")])
s += chain((ang("ADB", ORG), ang("ABD", ORG), "(7) से"),
           ("", ang("CDB", ORG), "(6) से"))
s += p("अतः " + m(ang("ADB", ORG) + " = " + ang("CDB", ORG)) + ", अर्थात् BD कोण D को भी समद्विभाजित करता है।")
s += ans("(i) ABCD का " + m("\\angle A = 90^\\circ") + " और " + m("AB = BC = CD = DA") + ", अतः ABCD एक वर्ग है (ii) " + m(ang("CBD", ORG) + " = " + ang("ABD", ORG))
         + " और " + m(ang("ADB", ORG) + " = " + ang("CDB", ORG)) + ", अर्थात् BD कोणों B और D को समद्विभाजित करता है।")
E1.append(("ABCD एक आयत है जिसमें विकर्ण AC दोनों कोणों A और C को समद्विभाजित करता है। दर्शाइए कि (i) ABCD एक वर्ग है (ii) विकर्ण BD दोनों कोणों B और D को समद्विभाजित करता है।", s))

# ---------- Q5 (आकृति 8.12) ----------
P15 = {"A": (200, 32), "D": (352, 32), "B": (28, 222), "C": (180, 222)}
pgram(P15, "A", "B", "C", "D")
P15["P"] = (P15["B"][0] + .74 * (P15["D"][0] - P15["B"][0]), P15["B"][1] + .74 * (P15["D"][1] - P15["B"][1]))
P15["Q"] = (P15["B"][0] + .26 * (P15["D"][0] - P15["B"][0]), P15["B"][1] + .26 * (P15["D"][1] - P15["B"][1]))
close1(dist(P15["D"], P15["P"]), dist(P15["B"], P15["Q"]), 1e-6)
pgram(P15, "A", "P", "C", "Q")


def fig812(sol, cap):
    if sol:
        mk = [("t", "AD", 1, RED), ("t", "BC", 1, RED), ("t", "DP", 2, ORG), ("t", "BQ", 2, ORG),
              ("t", "AB", 3, TEA, .45), ("t", "DC", 3, TEA, .55), ("a", "ADP", 1, BLU, 30), ("a", "CBQ", 1, BLU, 30),
              ("a", "PDC", 2, PUR, 44), ("a", "ABQ", 2, PUR, 44)]
        segs = [("AD", RED, 3), ("BC", RED, 3), ("AB", TEA, 3), ("DC", TEA, 3), ("BQ", ORG, 3), ("QP", None, 2.2), ("PD", ORG, 3),
                ("AP", GRN, 2.8), ("CQ", GRN, 2.8), ("AQ", BROWN, 2.8), ("CP", BROWN, 2.8)]
    else:
        mk = []
        segs = ["AD", "BC", "AB", "DC", "BD", "AP", "CQ", "AQ", "CP"]
    return geo(380, 255, P15, segs, {"A": (100, 16), "D": (30, 16), "B": (190, 16), "C": (290, 16), "P": (10, 17), "Q": (250, 18)}, mk, cap,
               fills=(("APD", BLU), ("CQB", ORG)), sol=sol)


s = given("ABCD एक समांतर चतुर्भुज है<br>P और Q विकर्ण BD पर हैं: " + m(sd("DP", ORG) + " = " + sd("BQ", ORG)),
          "सिद्ध करना है:<br>(i) " + m("\\triangle APD \\cong \\triangle CQB") + "<br>(ii) " + m(sd("AP", GRN) + " = " + sd("CQ", GRN)) + "<br>(iii) "
          + m("\\triangle AQB \\cong \\triangle CPD") + "<br>(iv) " + m(sd("AQ", BROWN) + " = " + sd("CP", BROWN)) + "<br>(v) APCQ एक समांतर चतुर्भुज है")
s += figs(fig812, "आकृति 8.12", "AD = CB लाल, DP = BQ नारंगी, AB = CD हरे-नीले; एकांतर कोण नीले और बैंगनी")
s += key((RED, "AD = CB"), (ORG, "DP = BQ"), (BLU, "∠ADP = ∠CBQ"), (TEA, "AB = CD"), (PUR, "∠ABQ = ∠CDP"), (GRN, "AP, CQ"), (BROWN, "AQ, CP"))
s += kh("(i) " + m("\\triangle APD \\cong \\triangle CQB"))
s += num(1, TH82)
s += num(2, ALT)
s += num(3, SAS)
s += kk(m("\\triangle APD") + " और " + m("\\triangle CQB") + " में,",
        [(sd("AD", RED) + " = " + sd("CB", RED) + " \\quad (1)", "समांतर चतुर्भुज की सम्मुख भुजाएँ (प्रमेय 8.2)", "S", RED),
         (ang("ADP", BLU) + " = " + ang("CBQ", BLU) + " \\quad (2)", "AD ∥ BC, तिर्यक रेखा BD — एकांतर कोण", "A", BLU),
         (sd("DP", ORG) + " = " + sd("BQ", ORG) + " \\quad (3)", "दिया है", "S", ORG)],
        ("\\triangle APD \\cong \\triangle CQB", "(1), (2), (3) से, SAS सर्वांगसमता नियम द्वारा"),
        [("A", "C"), ("P", "Q"), ("D", "B")])
s += kh("(ii) " + m(sd("AP", GRN) + " = " + sd("CQ", GRN)))
s += num(4, CPCT)
s += kk("", [(sd("AP", GRN) + " = " + sd("CQ", GRN) + " \\quad (4)", "CPCT (A ↔ C, P ↔ Q)")])
s += kh("(iii) " + m("\\triangle AQB \\cong \\triangle CPD"))
s += kk(m("\\triangle AQB") + " और " + m("\\triangle CPD") + " में,",
        [(sd("AB", TEA) + " = " + sd("CD", TEA) + " \\quad (5)", "समांतर चतुर्भुज की सम्मुख भुजाएँ (प्रमेय 8.2)", "S", TEA),
         (ang("ABQ", PUR) + " = " + ang("CDP", PUR) + " \\quad (6)", "AB ∥ DC, तिर्यक रेखा BD — एकांतर कोण", "A", PUR),
         (sd("BQ", ORG) + " = " + sd("DP", ORG) + " \\quad (7)", "दिया है", "S", ORG)],
        ("\\triangle AQB \\cong \\triangle CPD", "(5), (6), (7) से, SAS सर्वांगसमता नियम द्वारा"),
        [("A", "C"), ("Q", "P"), ("B", "D")])
s += kh("(iv) " + m(sd("AQ", BROWN) + " = " + sd("CP", BROWN)))
s += kk("", [(sd("AQ", BROWN) + " = " + sd("CP", BROWN) + " \\quad (8)", "CPCT (A ↔ C, Q ↔ P)")])
s += kh("(v) APCQ एक समांतर चतुर्भुज है")
s += num(5, TH83)
s += kk("चतुर्भुज APCQ में,", [(sd("AP", GRN) + " = " + sd("CQ", GRN), "(4) से — सम्मुख भुजाओं का पहला युग्म"),
                            (sd("PC", BROWN) + " = " + sd("QA", BROWN), "(8) से — सम्मुख भुजाओं का दूसरा युग्म")],
        ("APCQ", "प्रमेय 8.3 से, APCQ एक समांतर चतुर्भुज है"))
s += ans("(i) " + m("\\triangle APD \\cong \\triangle CQB") + " (SAS) (ii) " + m("AP = CQ") + " (iii) " + m("\\triangle AQB \\cong \\triangle CPD") + " (SAS) (iv) "
         + m("AQ = CP") + " (v) APCQ एक समांतर चतुर्भुज है — सभी सिद्ध हुए।")
E1.append(("समांतर चतुर्भुज ABCD के विकर्ण BD पर दो बिंदु P और Q इस प्रकार स्थित हैं कि " + m("DP = BQ") + " है (देखिए आकृति 8.12)। दर्शाइए कि (i) "
           + m("\\Delta APD \\cong \\Delta CQB") + " (ii) " + m("AP = CQ") + " (iii) " + m("\\Delta AQB \\cong \\Delta CPD") + " (iv) " + m("AQ = CP")
           + " (v) APCQ एक समांतर चतुर्भुज है।", s))

# ---------- Q6 (आकृति 8.13) ----------
P16 = {"A": (40, 208), "B": (312, 208), "C": (348, 42), "D": (76, 42)}
pgram(P16, "A", "B", "C", "D")
P16["P"] = foot(P16["A"], P16["B"], P16["D"])
P16["Q"] = foot(P16["C"], P16["B"], P16["D"])
on_seg(P16["P"], P16["B"], P16["D"])
on_seg(P16["Q"], P16["B"], P16["D"])
close1(dist(P16["A"], P16["P"]), dist(P16["C"], P16["Q"]), 1e-6)


def fig813(sol, cap):
    mk = [("r", "APB", PUR if sol else INK), ("r", "CQD", PUR if sol else INK)]
    if sol:
        mk += [("a", "ABD", 1, BLU, 40), ("a", "CDB", 1, BLU, 40), ("t", "AB", 1, RED), ("t", "DC", 1, RED), ("t", "AP", 2, ORG), ("t", "CQ", 2, ORG),
               ("p", "AB", 1, RED, .7), ("p", "DC", 1, RED, .7)]
        segs = [("AB", RED, 3), ("DC", RED, 3), "AD", "BC", ("BD", GRN, 2.6), ("AP", ORG, 3, "7 4"), ("CQ", ORG, 3, "7 4")]
    else:
        segs = ["AB", "DC", "AD", "BC", "BD", ("AP", None, None, "7 5"), ("CQ", None, None, "7 5")]
    return geo(390, 245, P16, segs, {"A": (225, 16), "B": (320, 16), "C": (40, 16), "D": (135, 16), "P": (80, 17), "Q": (250, 17)}, mk, cap,
               fills=(("APB", BLU), ("CQD", ORG)), sol=sol)


s = given("ABCD एक समांतर चतुर्भुज है<br>" + m("AP \\perp BD") + " और " + m("CQ \\perp BD"),
          "सिद्ध करना है:<br>(i) " + m("\\triangle APB \\cong \\triangle CQD") + "<br>(ii) " + m(sd("AP", ORG) + " = " + sd("CQ", ORG)))
s += figs(fig813, "आकृति 8.13", "समकोण बैंगनी, एकांतर कोण नीले, AB = CD लाल")
s += key((PUR, "∠APB = ∠CQD = 90°"), (BLU, "∠ABP = ∠CDQ"), (RED, "AB = CD"), (ORG, "AP, CQ"))
s += kh("(i) " + m("\\triangle APB \\cong \\triangle CQD"))
s += num(1, ALT)
s += num(2, TH82)
s += num(3, AAS)
s += kk(m("\\triangle APB") + " और " + m("\\triangle CQD") + " में,",
        [(ang("APB", PUR) + " = " + ang("CQD", PUR) + " \\quad (1)", "दोनों 90° हैं (AP ⊥ BD, CQ ⊥ BD)", "A", PUR),
         (ang("ABP", BLU) + " = " + ang("CDQ", BLU) + " \\quad (2)", "AB ∥ DC, तिर्यक रेखा BD — एकांतर कोण", "A", BLU),
         (sd("AB", RED) + " = " + sd("CD", RED) + " \\quad (3)", "समांतर चतुर्भुज की सम्मुख भुजाएँ (प्रमेय 8.2)", "S", RED)],
        ("\\triangle APB \\cong \\triangle CQD", "(1), (2), (3) से, AAS सर्वांगसमता नियम द्वारा"),
        [("A", "C"), ("P", "Q"), ("B", "D")])
s += tp("AAS में भुजा संगत होनी चाहिए: " + m(sd("AB", RED)) + " समकोण " + m(ang("APB", PUR)) + " के सामने है और " + m(sd("CD", RED)) + " समकोण "
        + m(ang("CQD", PUR)) + " के सामने है ✔")
s += kh("(ii) " + m(sd("AP", ORG) + " = " + sd("CQ", ORG)))
s += num(4, CPCT)
s += kk("", [(sd("AP", ORG) + " = " + sd("CQ", ORG), "CPCT (A ↔ C, P ↔ Q)")])
s += ans("(i) " + m("\\triangle APB \\cong \\triangle CQD") + " (AAS) (ii) " + m("AP = CQ") + " — दोनों सिद्ध हुए।")
E1.append(("ABCD एक समांतर चतुर्भुज है तथा AP और CQ शीर्षों A और C से विकर्ण BD पर क्रमशः लम्ब हैं (देखिए आकृति 8.13)। दर्शाइए कि (i) "
           + m("\\Delta APB \\cong \\Delta CQD") + " (ii) " + m("AP = CQ"), s))

# ---------- Q7 (आकृति 8.14) ----------
P17 = {"D": (30, 200), "C": (270, 200), "A": (110, 45), "B": (190, 45)}
P17["E"] = (P17["A"][0] + P17["C"][0] - P17["D"][0], P17["A"][1])
close1(dist(P17["A"], P17["D"]), dist(P17["B"], P17["C"]), 1e-6)
par_(P17["A"], P17["B"], P17["D"], P17["C"])
par_(P17["C"], P17["E"], P17["D"], P17["A"])
close1(angle_at(P17["A"], P17["D"], P17["B"]), angle_at(P17["B"], P17["A"], P17["C"]), 1e-6)    # ∠A = ∠B


def fig814(sol, cap):
    def ext(f, sol_):
        ray(f, sol_, P17["A"], P17["E"], 34)
    if sol:
        mk = [("t", "AD", 1, RED), ("t", "BC", 1, RED), ("t", "CE", 1, RED), ("a", "CBE", 1, ORG, 34), ("a", "BEC", 1, ORG, 30),
              ("a", "DAB", 2, BLU, 26), ("a", "ABC", 2, BLU, 24), ("a", "ADC", 1, TEA, 28), ("a", "BCD", 1, TEA, 28),
              ("p", "DC", 1, GRN, .5), ("p", "AB", 1, GRN, .5), ("p", "DA", 2, PUR, .25), ("p", "CE", 2, PUR, .25)]
        segs = [("AD", RED, 3), ("BC", RED, 3), ("CE", RED, 3, "6 4"), ("AB", GRN, 3.2), ("DC", INK)]
    else:
        mk = []
        segs = ["AD", "BC", "DC", ("CE", None, None, "4 4")]
    return geo(400, 235, P17, segs, {"A": (120, 16), "B": (90, 16), "C": (315, 17), "D": (225, 17), "E": (300, 18)}, mk, cap,
               fills=(("BCE", ORG),), extra=ext, sol=sol)


s = given("ABCD एक समलंब है: " + m("AB \\parallel DC") + "<br>" + m(sd("AD", RED) + " = " + sd("BC", RED))
          + "<br>रचना: AB को E तक बढ़ाया और " + m("CE \\parallel DA") + " खींची",
          "सिद्ध करना है:<br>(i) " + m(ang("A", BLU) + " = " + ang("B", BLU)) + "<br>(ii) " + m(ang("C", TEA) + " = " + ang("D", TEA)) + "<br>(iii) "
          + m("\\triangle ABC \\cong \\triangle BAD") + "<br>(iv) विकर्ण " + m("AC = ") + "विकर्ण " + m("BD"))
s += figs(fig814, "आकृति 8.14", "AD = BC = CE लाल, △BCE के बराबर कोण नारंगी, ∠A = ∠B नीले, ∠C = ∠D हरे-नीले")
s += key((RED, "AD = BC = CE"), (ORG, "∠CBE = ∠CEB"), (BLU, "∠A, ∠B"), (TEA, "∠C, ∠D"), (GRN, "AB ∥ DC"), (PUR, "DA ∥ CE"))
s += kh("(i) " + m(ang("A", BLU) + " = " + ang("B", BLU)))
s += num(1, D_PGM)
s += p("चतुर्भुज ADCE में " + m("AE \\parallel DC") + " (AB ∥ DC और E, AB की बढ़ी हुई रेखा पर है) और " + m("CE \\parallel DA") + " (रचना से)। "
       + "अतः ADCE एक समांतर चतुर्भुज है।")
s += num(2, TH82)
s += chain((sd("CE", RED), sd("AD", RED) + " \\qquad \\ldots(1)", "समांतर चतुर्भुज ADCE की सम्मुख भुजाएँ"))
s += chain((sd("BC", RED), sd("AD", RED), "दिया है"),
           ("", sd("CE", RED) + " \\qquad \\ldots(2)", "(1) से"))
s += num(3, TH72)
s += kk(m("\\triangle BCE") + " में,", [(ang("CEB", ORG) + " = " + ang("CBE", ORG) + " \\quad (3)", "BC = CE (2); CB के सामने ∠CEB, CE के सामने ∠CBE")])
s += num(4, INT)
s += chain((ang("A", BLU) + " + " + ang("CEB", ORG), "180" + DEG + " \\qquad \\ldots(4)", "AD ∥ EC, तिर्यक रेखा AE — एक ही ओर के अंतः कोण"))
s += num(5, LINEAR)
s += chain((ang("ABC", BLU) + " + " + ang("CBE", ORG), "180" + DEG + " \\qquad \\ldots(5)", "किरण BC रेखा AE पर खड़ी है (रैखिक युग्म)"))
s += chain((ang("A", BLU) + " + " + ang("CEB", ORG), ang("ABC", BLU) + " + " + ang("CBE", ORG), "(4) और (5) से — दोनों 180° के बराबर"), small=True)
s += chain((ang("A", BLU) + " + " + ang("CBE", ORG), ang("ABC", BLU) + " + " + ang("CBE", ORG), "(3) से ∠CEB = ∠CBE रखने पर"), small=True)
s += chain((ang("A", BLU), ang("ABC", BLU) + " + " + ang("CBE", ORG) + " - " + ang("CBE", ORG), "+∠CBE को पक्षांतर करने पर −∠CBE हो जाता है"),
           ("", ang("ABC", BLU), "∠CBE − ∠CBE = 0"), small=True)
s += p("अतः " + m(ang("A", BLU) + " = " + ang("B", BLU)) + "।")
s += kh("(ii) " + m(ang("C", TEA) + " = " + ang("D", TEA)))
s += chain((ang("A", BLU) + " + " + ang("D", TEA), "180" + DEG + " \\qquad \\ldots(6)", "AB ∥ DC, तिर्यक रेखा AD — एक ही ओर के अंतः कोण"))
s += chain((ang("B", BLU) + " + " + ang("C", TEA), "180" + DEG + " \\qquad \\ldots(7)", "AB ∥ DC, तिर्यक रेखा BC — एक ही ओर के अंतः कोण"))
s += chain((ang("A", BLU) + " + " + ang("D", TEA), ang("B", BLU) + " + " + ang("C", TEA), "(6) और (7) से — दोनों 180° के बराबर"))
s += chain((ang("B", BLU) + " + " + ang("D", TEA), ang("B", BLU) + " + " + ang("C", TEA), "(i) से ∠A = ∠B रखने पर"))
s += chain((ang("D", TEA), ang("B", BLU) + " + " + ang("C", TEA) + " - " + ang("B", BLU), "+∠B को पक्षांतर करने पर −∠B हो जाता है"),
           ("", ang("C", TEA), "∠B − ∠B = 0"))
s += kh("(iii) " + m("\\triangle ABC \\cong \\triangle BAD"))
s += num(6, SAS)
s += kk(m("\\triangle ABC") + " और " + m("\\triangle BAD") + " में,",
        [(sd("BC", RED) + " = " + sd("AD", RED), "दिया है", "S", RED),
         (ang("ABC", BLU) + " = " + ang("BAD", BLU), "(i) से (∠B = ∠A)", "A", BLU),
         (sd("AB", GRN) + " = " + sd("BA", GRN), "उभयनिष्ठ भुजा", "S", GRN)],
        ("\\triangle ABC \\cong \\triangle BAD", "SAS सर्वांगसमता नियम द्वारा"),
        [("A", "B"), ("B", "A"), ("C", "D")])
s += kh("(iv) विकर्ण " + m("AC = ") + "विकर्ण " + m("BD"))
s += num(7, CPCT)
s += kk("", [("AC = BD", "CPCT (A ↔ B, C ↔ D, इसलिए AC ↔ BD)")])
s += ans("(i) " + m("\\angle A = \\angle B") + " (ii) " + m("\\angle C = \\angle D") + " (iii) " + m("\\triangle ABC \\cong \\triangle BAD") + " (SAS) (iv) विकर्ण "
         + m("AC = ") + "विकर्ण " + m("BD") + " — सभी सिद्ध हुए।")
E1.append(("ABCD एक समलंब है, जिसमें " + m("AB \\parallel DC") + " और " + m("AD = BC") + " है (देखिए आकृति 8.14)। दर्शाइए कि (i) " + m("\\angle A = \\angle B")
           + " (ii) " + m("\\angle C = \\angle D") + " (iii) " + m("\\Delta ABC \\cong \\Delta BAD") + " (iv) विकर्ण " + m("AC = ") + "विकर्ण " + m("BD") + " है। "
           + "[<b>संकेत:</b> AB को बढ़ाइए और C से होकर DA के समांतर एक रेखा खींचिए जो बढ़ी हुई भुजा AB को E पर प्रतिच्छेद करे।]", s))

# =====================================================================
# Exercise 8.2
# =====================================================================
E2 = []


def mids(P):
    P["P"], P["Q"], P["R"], P["S"] = mid(P["A"], P["B"]), mid(P["B"], P["C"]), mid(P["C"], P["D"]), mid(P["D"], P["A"])
    # mid-point theorem checks on the drawn figure
    par_(P["S"], P["R"], P["A"], P["C"]); close1(dist(P["S"], P["R"]), dist(P["A"], P["C"]) / 2, 1e-6)
    par_(P["P"], P["Q"], P["A"], P["C"]); close1(dist(P["P"], P["Q"]), dist(P["A"], P["C"]) / 2, 1e-6)
    par_(P["P"], P["S"], P["B"], P["D"]); close1(dist(P["P"], P["S"]), dist(P["B"], P["D"]) / 2, 1e-6)
    pgram(P, "P", "Q", "R", "S")
    return P


MID_MK = [("t", "AP", 1, RED), ("t", "PB", 1, RED), ("t", "BQ", 2, ORG), ("t", "QC", 2, ORG),
          ("t", "CR", 1, TEA), ("t", "RD", 1, TEA), ("t", "DS", 2, PUR), ("t", "SA", 2, PUR)]

# ---------- Q1 (आकृति 8.20) ----------
P21 = mids({"A": (40, 262), "B": (290, 262), "C": (308, 82), "D": (120, 36)})


def fig820(sol, cap):
    if sol:
        mk = MID_MK + [("p", "SR", 1, GRN, .5), ("p", "PQ", 1, GRN, .5), ("p", "AC", 1, BLU, .62), ("t", "SR", 3, GRN, .28), ("t", "PQ", 3, GRN, .28),
                       ("p", "PS", 2, BROWN, .4), ("p", "QR", 2, BROWN, .4)]
        segs = ["AP", "PB", "BQ", "QC", "CR", "RD", "DS", "SA", ("SR", GRN, 3), ("PQ", GRN, 3), ("PS", BROWN, 2.6), ("QR", BROWN, 2.6),
                ("AC", BLU, 2.4, "6 4"), ("BD", BROWN, 1.8, "3 4")]
    else:
        mk = []
        segs = ["AB", "BC", "CD", "DA", "PQ", "QR", "RS", "SP", ("AC", None, None, "4 4")]
    return geo(350, 295, P21, segs, {"A": (225, 16), "B": (315, 16), "C": (20, 17), "D": (110, 16), "P": (270, 16), "Q": (0, 17), "R": (75, 16), "S": (165, 17)},
               mk, cap, fills=(("PQRS", GRN),), sol=sol)


s = given("चतुर्भुज ABCD में P, Q, R, S क्रमशः AB, BC, CD, DA के मध्य-बिंदु:<br>" + m(sd("AP", RED) + " = " + sd("PB", RED)) + ", "
          + m(sd("BQ", ORG) + " = " + sd("QC", ORG)) + ", " + m(sd("CR", TEA) + " = " + sd("RD", TEA)) + ", " + m(sd("DS", PUR) + " = " + sd("SA", PUR))
          + "<br>AC एक विकर्ण है",
          "सिद्ध करना है:<br>(i) " + m(sd("SR", GRN) + " \\parallel " + sd("AC", BLU)) + " और " + m(sd("SR", GRN) + " = " + HALF + sd("AC", BLU)) + "<br>(ii) "
          + m(sd("PQ", GRN) + " = " + sd("SR", GRN)) + "<br>(iii) PQRS एक समांतर चतुर्भुज है")
s += figs(fig820, "आकृति 8.20", "मध्य-बिंदुओं के बराबर भाग रंगीन निशानों से; SR, PQ हरी (AC ∥), PS, QR भूरी (BD ∥)")
s += key((GRN, "SR, PQ (∥ AC)"), (BLU, "विकर्ण AC"), (BROWN, "PS, QR (∥ BD), विकर्ण BD"), (RED, "AP = PB"), (ORG, "BQ = QC"), (TEA, "CR = RD"), (PUR, "DS = SA"))
s += kh("(i) " + m(sd("SR", GRN) + " \\parallel " + sd("AC", BLU)) + " और " + m(sd("SR", GRN) + " = " + HALF + sd("AC", BLU)))
s += num(1, MPT)
s += kk(m("\\triangle ACD") + " में, S भुजा DA का और R भुजा DC का मध्य-बिंदु है, इसलिए",
        [(sd("SR", GRN) + " \\parallel " + sd("AC", BLU) + " \\quad (1)", "मध्य-बिंदु प्रमेय (प्रमेय 8.8)"),
         (sd("SR", GRN) + " = " + HALF + sd("AC", BLU) + " \\quad (2)", "मध्य-बिंदु प्रमेय")])
s += kh("(ii) " + m(sd("PQ", GRN) + " = " + sd("SR", GRN)))
s += kk(m("\\triangle ABC") + " में, P भुजा AB का और Q भुजा BC का मध्य-बिंदु है, इसलिए",
        [(sd("PQ", GRN) + " \\parallel " + sd("AC", BLU) + " \\quad (3)", "मध्य-बिंदु प्रमेय"),
         (sd("PQ", GRN) + " = " + HALF + sd("AC", BLU) + " \\quad (4)", "मध्य-बिंदु प्रमेय")])
s += chain((sd("PQ", GRN), HALF + sd("AC", BLU), "(4) से"),
           ("", sd("SR", GRN) + " \\qquad \\ldots(5)", "(2) से"))
s += kh("(iii) PQRS एक समांतर चतुर्भुज है")
s += p("B और D को मिलाइए (विकर्ण BD, भूरी बिंदुदार रेखा)।")
s += kk(m("\\triangle ABD") + " में, P और S क्रमशः AB और AD के मध्य-बिंदु हैं, इसलिए",
        [(sd("PS", BROWN) + " = " + HALF + "BD \\quad (6)", "मध्य-बिंदु प्रमेय")])
s += kk(m("\\triangle CBD") + " में, Q और R क्रमशः BC और CD के मध्य-बिंदु हैं, इसलिए",
        [(sd("QR", BROWN) + " = " + HALF + "BD \\quad (7)", "मध्य-बिंदु प्रमेय")])
s += chain((sd("PS", BROWN), HALF + "BD", "(6) से"),
           ("", sd("QR", BROWN) + " \\qquad \\ldots(8)", "(7) से"))
s += num(2, TH83)
s += kk("चतुर्भुज PQRS में,", [(sd("PQ", GRN) + " = " + sd("SR", GRN), "(5) से — सम्मुख भुजाओं का पहला युग्म"),
                            (sd("PS", BROWN) + " = " + sd("QR", BROWN), "(8) से — सम्मुख भुजाओं का दूसरा युग्म")],
        ("PQRS", "प्रमेय 8.3 से, PQRS एक समांतर चतुर्भुज है"))
s += tp("दूसरी विधि: (1) और (3) से PQ ∥ AC ∥ SR, इसलिए PQ ∥ SR (प्रमेय 6.6); इसी प्रकार PS ∥ BD ∥ QR — सम्मुख भुजाओं के दोनों युग्म समांतर हैं।")
s += ans("(i) " + m("SR \\parallel AC") + " और " + m("SR = \\dfrac{1}{2}AC") + " (ii) " + m("PQ = SR") + " (iii) PQRS एक समांतर चतुर्भुज है — सभी सिद्ध हुए।")
E2.append(("ABCD एक चतुर्भुज है जिसमें P, Q, R और S क्रमशः भुजाओं AB, BC, CD और DA के मध्य-बिंदु हैं (देखिए आकृति 8.20)। AC उसका एक विकर्ण है। दर्शाइए कि (i) "
           + m("SR \\parallel AC") + " और " + m("SR = \\dfrac{1}{2}AC") + " है। (ii) " + m("PQ = SR") + " है। (iii) PQRS एक समांतर चतुर्भुज है।", s))

# ---------- Q2 (no figure): rhombus -> PQRS rectangle ----------
P22 = mids({"A": (30, 168), "B": (190, 298), "C": (350, 168), "D": (190, 38)})
P22["O"] = inter(P22["A"], P22["C"], P22["B"], P22["D"])
P22["M"] = inter(P22["P"], P22["Q"], P22["B"], P22["D"])
P22["N"] = inter(P22["P"], P22["S"], P22["A"], P22["C"])
close1(dist(P22["A"], P22["B"]), dist(P22["B"], P22["C"]), 1e-6)
close1(dist(P22["A"], P22["B"]), dist(P22["A"], P22["D"]), 1e-6)
perp_(P22["A"], P22["C"], P22["B"], P22["D"])
on_seg(P22["M"], P22["O"], P22["B"])
on_seg(P22["N"], P22["O"], P22["A"])
perp_(P22["P"], P22["Q"], P22["P"], P22["S"])


def fig82_2(sol, cap):
    mk = MID_MK + [("p", "PQ", 1, GRN, .72), ("p", "SR", 1, GRN, .72), ("p", "AC", 1, GRN, .2), ("p", "SP", 2, BROWN, .7), ("p", "RQ", 2, BROWN, .7),
                   ("p", "DB", 2, BROWN, .2), ("r", "AOB", PUR), ("r", "NPM", PUR), ("r", "PQR", INK), ("r", "QRS", INK), ("r", "RSP", INK)]
    segs = ["AB", "BC", "CD", "DA", ("PQ", GRN, 3), ("SR", GRN, 3), ("PS", BROWN, 3), ("QR", BROWN, 3), ("AC", GRN, 2, "6 4"), ("BD", BROWN, 2, "6 4")]
    return geo(380, 320, P22, segs, {"A": (180, 16), "B": (270, 16), "C": (0, 16), "D": (90, 16), "P": (225, 17), "Q": (315, 17), "R": (45, 17), "S": (135, 17),
                                     "O": (45, 15), "M": (315, 16), "N": (135, 15)}, mk, cap, fills=(("PMON", PUR),), sol=sol)


s = given("ABCD एक समचतुर्भुज है: " + m("AB = BC = CD = DA") + "<br>P, Q, R, S क्रमशः AB, BC, CD, DA के मध्य-बिंदु<br>विकर्ण AC, BD बिंदु O पर मिलते हैं",
          "सिद्ध करना है: चतुर्भुज PQRS एक आयत है")
s += NOFIG + solo(fig82_2(True, "हल की आकृति: PQ, SR हरी (∥ AC), PS, QR भूरी (∥ BD); विकर्ण O पर समकोण बनाते हैं"))
s += key((GRN, "PQ, SR ∥ AC"), (BROWN, "PS, QR ∥ BD"), (PUR, "∠AOB = 90° और ∠QPS"), (RED, "AP = PB"), (ORG, "BQ = QC"), (TEA, "CR = RD"), (PUR, "DS = SA"))
s += kh("चरण 1: PQRS एक समांतर चतुर्भुज है")
s += num(1, MPT)
s += kk("मध्य-बिंदु प्रमेय से,", [(sd("PQ", GRN) + " \\parallel AC,\\;\\; " + sd("PQ", GRN) + " = " + HALF + "AC \\quad (1)", "△ABC में P, Q मध्य-बिंदु हैं"),
                               (sd("SR", GRN) + " \\parallel AC,\\;\\; " + sd("SR", GRN) + " = " + HALF + "AC \\quad (2)", "△ADC में S, R मध्य-बिंदु हैं"),
                               (sd("PS", BROWN) + " \\parallel BD,\\;\\; " + sd("PS", BROWN) + " = " + HALF + "BD \\quad (3)", "△ABD में P, S मध्य-बिंदु हैं"),
                               (sd("QR", BROWN) + " \\parallel BD,\\;\\; " + sd("QR", BROWN) + " = " + HALF + "BD \\quad (4)", "△CBD में Q, R मध्य-बिंदु हैं")])
s += chain((sd("PQ", GRN), sd("SR", GRN), "(1) और (2) से — दोनों ½AC हैं"))
s += chain((sd("PS", BROWN), sd("QR", BROWN), "(3) और (4) से — दोनों ½BD हैं"))
s += num(2, TH83)
s += p("सम्मुख भुजाओं के दोनों युग्म बराबर हैं, इसलिए PQRS एक समांतर चतुर्भुज है।")
s += kh("चरण 2: PQRS का एक कोण " + m("90^\\circ") + " है")
s += num(3, EX2)
s += chain((ang("AOB", PUR), dg(90, PUR) + " \\qquad \\ldots(5)", "समचतुर्भुज के विकर्ण परस्पर लम्ब हैं"))
s += p("मान लीजिए PQ, BD को M पर और PS, AC को N पर काटती है।")
s += num(4, D_PGM)
s += p("चतुर्भुज PMON में " + m("PM \\parallel NO") + " ((1) से, PQ ∥ AC) और " + m("PN \\parallel MO") + " ((3) से, PS ∥ BD)। अतः PMON एक समांतर चतुर्भुज है।")
s += num(5, TH84)
s += chain((ang("QPS", PUR), ang("MPN", PUR), "M, PQ पर और N, PS पर है — वही कोण"),
           ("", ang("MON", PUR), "समांतर चतुर्भुज PMON के सम्मुख कोण (प्रमेय 8.4)"),
           ("", ang("AOB", PUR), "M, OB पर और N, OA पर है — वही कोण"),
           ("", dg(90, PUR), "(5) से"))
s += num(6, D_RECT)
s += p("PQRS एक समांतर चतुर्भुज है जिसका एक कोण " + m(ang("QPS", PUR) + " = 90^\\circ") + " है, इसलिए PQRS एक आयत है।")
s += ans("PQRS एक समांतर चतुर्भुज है और " + m("\\angle QPS = 90^\\circ") + ", अतः चतुर्भुज PQRS एक आयत है। सिद्ध हुआ।")
E2.append(("ABCD एक समचतुर्भुज है और P, Q, R और S क्रमशः भुजाओं AB, BC, CD और DA के मध्य-बिंदु है। दर्शाइए कि चतुर्भुज PQRS एक आयत है।", s))

# ---------- Q3 (no figure): rectangle -> PQRS rhombus ----------
P23 = mids({"A": (40, 245), "B": (320, 245), "C": (320, 50), "D": (40, 50)})
close1(dist(P23["A"], P23["C"]), dist(P23["B"], P23["D"]), 1e-6)
for a_, b_ in (("P", "Q"), ("Q", "R"), ("R", "S")):
    close1(dist(P23[a_], P23[b_]), dist(P23["S"], P23["P"]), 1e-6)


def fig82_3(sol, cap):
    mk = MID_MK + [("r", "DAB", PUR), ("r", "ABC", PUR), ("r", "BCD", PUR), ("r", "CDA", PUR),
                   ("t", "PQ", 3, GRN), ("t", "QR", 3, GRN), ("t", "RS", 3, GRN), ("t", "SP", 3, GRN)]
    segs = ["AB", "BC", "CD", "DA", ("PQ", GRN, 3), ("QR", GRN, 3), ("RS", GRN, 3), ("SP", GRN, 3), ("AC", BLU, 2, "6 4"), ("BD", BROWN, 2, "6 4")]
    return geo(360, 285, P23, segs, {"A": (225, 16), "B": (315, 16), "C": (45, 16), "D": (135, 16), "P": (270, 16), "Q": (0, 16), "R": (90, 16), "S": (180, 16)},
               mk, cap, fills=(("PQRS", GRN),), sol=sol)


s = given("ABCD एक आयत है (प्रत्येक कोण " + m("90^\\circ") + ")<br>P, Q, R, S क्रमशः AB, BC, CD, DA के मध्य-बिंदु", "सिद्ध करना है: चतुर्भुज PQRS एक समचतुर्भुज है")
s += NOFIG + solo(fig82_3(True, "हल की आकृति: PQRS की चारों भुजाएँ हरी (बराबर); विकर्ण AC नीला, BD भूरा"))
s += key((GRN, "PQ, QR, RS, SP"), (BLU, "विकर्ण AC"), (BROWN, "विकर्ण BD"), (PUR, "समकोण"))
s += kh("चरण 1: आयत के विकर्ण बराबर हैं: " + m(sd("AC", BLU) + " = " + sd("BD", BROWN)))
s += num(1, SAS)
s += kk(m("\\triangle ABC") + " और " + m("\\triangle BAD") + " में,",
        [("AB = BA", "उभयनिष्ठ भुजा", "S", INK),
         (ang("ABC", PUR) + " = " + ang("BAD", PUR), "आयत का प्रत्येक कोण 90° है", "A", PUR),
         ("BC = AD", "आयत की सम्मुख भुजाएँ (प्रमेय 8.2)", "S", INK)],
        ("\\triangle ABC \\cong \\triangle BAD", "SAS सर्वांगसमता नियम द्वारा"),
        [("A", "B"), ("B", "A"), ("C", "D")])
s += kk("", [(sd("AC", BLU) + " = " + sd("BD", BROWN) + " \\quad (1)", "CPCT")])
s += kh("चरण 2: PQRS की चारों भुजाएँ बराबर हैं")
s += num(2, MPT)
s += kk("मध्य-बिंदु प्रमेय से,", [(sd("PQ", GRN) + " = " + HALF + sd("AC", BLU) + " \\quad (2)", "△ABC में P, Q मध्य-बिंदु हैं"),
                               (sd("SR", GRN) + " = " + HALF + sd("AC", BLU) + " \\quad (3)", "△ADC में S, R मध्य-बिंदु हैं"),
                               (sd("PS", GRN) + " = " + HALF + sd("BD", BROWN) + " \\quad (4)", "△ABD में P, S मध्य-बिंदु हैं"),
                               (sd("QR", GRN) + " = " + HALF + sd("BD", BROWN) + " \\quad (5)", "△CBD में Q, R मध्य-बिंदु हैं")])
s += chain((sd("PQ", GRN), HALF + sd("AC", BLU), "(2) से"),
           ("", HALF + sd("BD", BROWN), "(1) से AC = BD रखने पर"),
           ("", sd("PS", GRN), "(4) से"))
s += chain((sd("SR", GRN), HALF + sd("AC", BLU), "(3) से"),
           ("", sd("PQ", GRN), "(2) से"))
s += chain((sd("QR", GRN), HALF + sd("BD", BROWN), "(5) से"),
           ("", sd("PS", GRN), "(4) से"))
s += p("अतः " + m(sd("PQ", GRN) + " = " + sd("QR", GRN) + " = " + sd("RS", GRN) + " = " + sd("SP", GRN)) + " — चारों भुजाएँ बराबर हैं।")
s += num(3, TH83)
s += p("सम्मुख भुजाएँ बराबर हैं (PQ = SR, PS = QR), इसलिए PQRS एक समांतर चतुर्भुज है।")
s += num(4, D_RHOM)
s += p("PQRS एक समांतर चतुर्भुज है जिसकी सभी भुजाएँ बराबर हैं, इसलिए PQRS एक समचतुर्भुज है।")
s += ans(m("PQ = QR = RS = SP") + " और PQRS एक समांतर चतुर्भुज है, अतः PQRS एक समचतुर्भुज है। सिद्ध हुआ।")
E2.append(("ABCD एक आयत है, जिसमें P, Q, R और S क्रमशः भुजाओं AB, BC, CD और DA के मध्य-बिंदु हैं। दर्शाइए कि चतुर्भुज PQRS एक समचतुर्भुज है।", s))

# ---------- Q4 (आकृति 8.21) ----------
P24 = {"D": (99, 50), "C": (250, 50), "A": (38, 281), "B": (310, 281)}
P24["E"] = mid(P24["A"], P24["D"])
P24["F"] = inter(P24["E"], (P24["E"][0] + 10, P24["E"][1]), P24["B"], P24["C"])
P24["G"] = inter(P24["E"], P24["F"], P24["B"], P24["D"])
close1(dist(P24["B"], P24["F"]), dist(P24["F"], P24["C"]), 1e-6)
close1(dist(P24["B"], P24["G"]), dist(P24["G"], P24["D"]), 1e-6)
par_(P24["E"], P24["F"], P24["A"], P24["B"])


def fig821(sol, cap):
    def ext(f, sol_):
        y = P24["E"][1]
        c_ = GRN if sol_ else INK
        f.line((14, y), P24["E"], c_, 3 if sol_ else 2.2, True, False)
        f.line(P24["F"], (338, y), c_, 3 if sol_ else 2.2, False, True)
        f.line(P24["E"], P24["F"], c_, 3 if sol_ else 2.2)
    if sol:
        mk = [("t", "AE", 1, RED), ("t", "ED", 1, RED), ("t", "BG", 2, ORG), ("t", "GD", 2, ORG), ("t", "BF", 3, TEA), ("t", "FC", 3, TEA),
              ("p", "AB", 1, GRN, .5), ("p", "DC", 1, GRN, .5), ("p", "EG", 1, GRN, .5), ("p", "GF", 1, GRN, .5)]
        segs = [("AE", RED, 3), ("ED", RED, 3), ("BG", ORG, 3), ("GD", ORG, 3), ("BF", TEA, 3), ("FC", TEA, 3), ("AB", GRN, 3), ("DC", GRN, 3)]
    else:
        mk = []
        segs = ["AD", "BC", "AB", "DC", "BD"]
    lab = {"D": (135, 16), "C": (45, 16), "A": (225, 16), "B": (315, 16), "E": (215, 18), "F": (325, 18)}
    if sol:
        lab["G"] = (90, 17)
    return geo(350, 310, P24, segs, lab,
               mk, cap, extra=ext, fills=(("ABD", BLU), ("BDC", ORG)), sol=sol)


s = given("ABCD एक समलंब है: " + m("AB \\parallel DC") + "<br>BD एक विकर्ण है<br>E, AD का मध्य-बिंदु: " + m(sd("AE", RED) + " = " + sd("ED", RED))
          + "<br>E से होकर " + m("EF \\parallel AB") + ", F भुजा BC पर", "सिद्ध करना है: F भुजा BC का मध्य-बिंदु है: " + m(sd("BF", TEA) + " = " + sd("FC", TEA)))
s += figs(fig821, "आकृति 8.21", "AB, EF, DC हरी (समांतर); AE = ED लाल, BG = GD नारंगी, BF = FC हरे-नीले")
s += key((GRN, "AB ∥ EF ∥ DC"), (RED, "AE = ED"), (ORG, "BG = GD"), (TEA, "BF = FC"))
s += p("मान लीजिए EF, विकर्ण BD को G पर काटती है।")
s += kh("चरण 1: " + m("\\triangle ABD") + " में")
s += num(1, MPT_C)
s += kk(m("\\triangle ABD") + " में,", [(sd("AE", RED) + " = " + sd("ED", RED), "E, भुजा AD का मध्य-बिंदु है (दिया है)"),
                                     ("EG \\parallel AB", "EF ∥ AB (दिया है) और G, EF पर है"),
                                     (sd("BG", ORG) + " = " + sd("GD", ORG) + " \\quad (1)", "प्रमेय 8.9 से G, BD का मध्य-बिंदु है")])
s += kh("चरण 2: " + m("\\triangle BDC") + " में")
s += num(2, TH66)
s += kk("", [("EF \\parallel AB,\\;\\; AB \\parallel DC", "दिया है"),
             ("EF \\parallel DC", "एक ही रेखा AB के समांतर रेखाएँ परस्पर समांतर (प्रमेय 6.6)"),
             ("GF \\parallel DC \\quad (2)", "G और F रेखा EF पर हैं")])
s += kk(m("\\triangle BDC") + " में,", [(sd("BG", ORG) + " = " + sd("GD", ORG), "(1) से — G, भुजा BD का मध्य-बिंदु है"),
                                     ("GF \\parallel DC", "(2) से"),
                                     (sd("BF", TEA) + " = " + sd("FC", TEA), "प्रमेय 8.9 से F, BC का मध्य-बिंदु है")])
s += ans(m(sd("BF", TEA) + " = " + sd("FC", TEA)) + ", अर्थात् F भुजा BC का मध्य-बिंदु है। सिद्ध हुआ।")
E2.append(("ABCD एक समलंब है, जिसमें " + m("AB \\parallel DC") + " है। साथ ही, BD एक विकर्ण है और E भुजा AD का मध्य-बिंदु है। E से होकर एक रेखा AB के समांतर खींची गई है, जो BC को F पर प्रतिच्छेद करती है (देखिए आकृति 8.21)। दर्शाइए कि F भुजा BC का मध्य-बिंदु है।", s))

# ---------- Q5 (आकृति 8.22) ----------
P25 = {"A": (35, 288), "B": (288, 288), "C": (359, 42), "D": (106, 42)}
pgram(P25, "A", "B", "C", "D")
P25["E"] = mid(P25["A"], P25["B"])
P25["F"] = mid(P25["D"], P25["C"])
P25["P"] = inter(P25["A"], P25["F"], P25["B"], P25["D"])
P25["Q"] = inter(P25["E"], P25["C"], P25["B"], P25["D"])
_dp, _pq, _qb = dist(P25["D"], P25["P"]), dist(P25["P"], P25["Q"]), dist(P25["Q"], P25["B"])
close1(_dp, _pq, 1e-6)
close1(_pq, _qb, 1e-6)
close1(_dp + _pq + _qb, dist(P25["D"], P25["B"]), 1e-6)
par_(P25["A"], P25["F"], P25["E"], P25["C"])


def fig822(sol, cap):
    if sol:
        mk = [("t", "AE", 1, ORG), ("t", "EB", 1, ORG), ("t", "DF", 1, ORG), ("t", "FC", 1, ORG), ("t", "AD", 2, RED), ("t", "BC", 2, RED),
              ("t", "DP", 3, GRN), ("t", "PQ", 3, GRN), ("t", "QB", 3, GRN), ("a", "ADF", 1, BLU, 22), ("a", "CBE", 1, BLU, 22),
              ("p", "AP", 1, TEA, .45), ("p", "EQ", 1, TEA, .45)]
        segs = [("AE", ORG, 3), ("EB", ORG, 3), ("DF", ORG, 3), ("FC", ORG, 3), ("AD", RED, 3), ("BC", RED, 3), ("AF", TEA, 2.6), ("EC", TEA, 2.6),
                ("DP", GRN, 3.2), ("PQ", GRN, 3.2), ("QB", GRN, 3.2)]
    else:
        mk = []
        segs = ["AB", "BC", "CD", "DA", "AF", "EC", "BD"]
    return geo(395, 320, P25, segs, {"A": (200, 17), "B": (330, 16), "C": (20, 17), "D": (150, 16), "E": (270, 17), "F": (90, 16), "P": (5, 18), "Q": (5, 18)},
               mk, cap, fills=(("ADF", BLU), ("CBE", ORG)), sol=sol)


s = given("ABCD एक समांतर चतुर्भुज है<br>E, AB का मध्य-बिंदु: " + m(sd("AE", ORG) + " = " + sd("EB", ORG)) + "<br>F, CD का मध्य-बिंदु: "
          + m(sd("DF", ORG) + " = " + sd("FC", ORG)) + "<br>AF और EC, विकर्ण BD को P और Q पर काटते हैं",
          "सिद्ध करना है: AF और EC, BD को समत्रिभाजित करते हैं: " + m(sd("DP", GRN) + " = " + sd("PQ", GRN) + " = " + sd("QB", GRN)))
s += figs(fig822, "आकृति 8.22", "चारों आधी भुजाएँ AE, EB, DF, FC नारंगी (बराबर); AF ∥ EC हरे-नीले; BD के तीन बराबर भाग हरे")
s += key((ORG, "AE = EB = DF = FC"), (RED, "AD = CB"), (BLU, "∠D = ∠B"), (TEA, "AF ∥ EC"), (GRN, "DP, PQ, QB"))
s += kh("चरण 1: AECF एक समांतर चतुर्भुज है, अर्थात् " + m("AF \\parallel EC"))
s += num(1, TH82)
s += chain((sd("AE", ORG), HALF + "AB", "E, AB का मध्य-बिंदु है"),
           ("", HALF + "CD", "AB = CD (प्रमेय 8.2)"),
           ("", sd("FC", ORG) + " \\qquad \\ldots(1)", "F, CD का मध्य-बिंदु है"))
s += chain((sd("DF", ORG), HALF + "CD", "F, CD का मध्य-बिंदु है"),
           ("", HALF + "AB", "CD = AB"),
           ("", sd("BE", ORG) + " \\qquad \\ldots(2)", "E, AB का मध्य-बिंदु है"))
s += num(2, TH84)
s += num(3, SAS)
s += kk(m("\\triangle ADF") + " और " + m("\\triangle CBE") + " में,",
        [(sd("AD", RED) + " = " + sd("CB", RED), "समांतर चतुर्भुज की सम्मुख भुजाएँ (प्रमेय 8.2)", "S", RED),
         (ang("ADF", BLU) + " = " + ang("CBE", BLU), "समांतर चतुर्भुज के सम्मुख कोण ∠D = ∠B (प्रमेय 8.4)", "A", BLU),
         (sd("DF", ORG) + " = " + sd("BE", ORG), "(2) से", "S", ORG)],
        ("\\triangle ADF \\cong \\triangle CBE", "SAS सर्वांगसमता नियम द्वारा"),
        [("A", "C"), ("D", "B"), ("F", "E")])
s += num(4, CPCT)
s += kk("", [(sd("AF", TEA) + " = " + sd("CE", TEA) + " \\quad (3)", "CPCT (A ↔ C, F ↔ E)")])
s += num(5, TH83)
s += kk("चतुर्भुज AECF में,", [(sd("AE", ORG) + " = " + sd("FC", ORG), "(1) से — सम्मुख भुजाओं का पहला युग्म"),
                            (sd("AF", TEA) + " = " + sd("EC", TEA), "(3) से — सम्मुख भुजाओं का दूसरा युग्म")],
        ("AECF", "प्रमेय 8.3 से, AECF एक समांतर चतुर्भुज है"))
s += p("अतः " + m(sd("AF", TEA) + " \\parallel " + sd("EC", TEA)) + " ... (4), इसलिए " + m("PF \\parallel QC") + " और " + m("EQ \\parallel AP") + "।")
s += kh("चरण 2: " + m(sd("DP", GRN) + " = " + sd("PQ", GRN)))
s += num(6, MPT_C)
s += kk(m("\\triangle DQC") + " में,", [(sd("DF", ORG) + " = " + sd("FC", ORG), "F, भुजा DC का मध्य-बिंदु है"),
                                     ("FP \\parallel CQ", "(4) से"),
                                     (sd("DP", GRN) + " = " + sd("PQ", GRN) + " \\quad (5)", "प्रमेय 8.9 से P, DQ का मध्य-बिंदु है")])
s += kh("चरण 3: " + m(sd("PQ", GRN) + " = " + sd("QB", GRN)))
s += kk(m("\\triangle APB") + " में,", [(sd("AE", ORG) + " = " + sd("EB", ORG), "E, भुजा AB का मध्य-बिंदु है"),
                                     ("EQ \\parallel AP", "(4) से"),
                                     (sd("PQ", GRN) + " = " + sd("QB", GRN) + " \\quad (6)", "प्रमेय 8.9 से Q, PB का मध्य-बिंदु है")])
s += chain((sd("DP", GRN), sd("PQ", GRN), "(5) से"),
           ("", sd("QB", GRN), "(6) से"))
s += ans(m(sd("DP", GRN) + " = " + sd("PQ", GRN) + " = " + sd("QB", GRN)) + ", अर्थात् रेखाखंड AF और EC विकर्ण BD को तीन बराबर भागों में बाँटते (समत्रिभाजित करते) हैं। सिद्ध हुआ।")
E2.append(("एक समांतर चतुर्भुज ABCD में E और F क्रमशः भुजाओं AB और CD के मध्य-बिंदु हैं (देखिए आकृति 8.22)। दर्शाइए कि रेखाखंड AF और EC विकर्ण BD को समत्रिभाजित करते हैं।", s))

# ---------- Q6 (no figure): right triangle, line through mid-point of hypotenuse ----------
P26 = {"A": (70, 38), "C": (70, 250), "B": (330, 250)}
P26["M"] = mid(P26["A"], P26["B"])
P26["D"] = (P26["A"][0], P26["M"][1])
par_(P26["M"], P26["D"], P26["B"], P26["C"])
close1(dist(P26["A"], P26["D"]), dist(P26["D"], P26["C"]), 1e-6)
close1(dist(P26["C"], P26["M"]), dist(P26["A"], P26["B"]) / 2, 1e-6)


def fig82_6(sol, cap):
    mk = [("r", "ACB", PUR), ("r", "ADM", PUR), ("r", "MDC", PUR), ("t", "AM", 1, RED), ("t", "MB", 1, RED), ("t", "AD", 2, ORG), ("t", "DC", 2, ORG),
          ("p", "DM", 1, BLU, .55), ("p", "CB", 1, BLU, .55), ("t", "CM", 1, RED, .6)]
    segs = [("AM", RED, 3), ("MB", RED, 3), ("AD", ORG, 3), ("DC", ORG, 3), ("CB", BLU, 3), ("DM", GRN, 3.2), ("CM", RED, 2.6, "7 4")]
    return geo(380, 285, P26, segs, {"A": (90, 16), "C": (225, 17), "B": (0, 17), "M": (45, 17), "D": (180, 17)}, mk, cap,
               fills=(("AMD", BLU), ("CMD", ORG)), sol=sol)


s = given(m("\\triangle ABC") + " में " + m(ang("ACB", PUR) + " = 90^\\circ") + "<br>M, कर्ण AB का मध्य-बिंदु: " + m(sd("AM", RED) + " = " + sd("MB", RED))
          + "<br>M से " + m("MD \\parallel BC") + ", D भुजा AC पर",
          "सिद्ध करना है:<br>(i) D, AC का मध्य-बिंदु है<br>(ii) " + m("MD \\perp AC") + "<br>(iii) " + m("CM = MA = \\dfrac{1}{2}AB"))
s += NOFIG + solo(fig82_6(True, "हल की आकृति: AM = MB लाल, AD = DC नारंगी, MD ∥ BC, समकोण बैंगनी"))
s += key((RED, "AM = MB (= CM)"), (ORG, "AD = DC"), (BLU, "BC"), (GRN, "MD (उभयनिष्ठ)"), (PUR, "समकोण"))
s += kh("(i) D, AC का मध्य-बिंदु है")
s += num(1, MPT_C)
s += kk(m("\\triangle ABC") + " में,", [(sd("AM", RED) + " = " + sd("MB", RED), "M, भुजा AB का मध्य-बिंदु है (दिया है)"),
                                     ("MD \\parallel BC", "दिया है"),
                                     (sd("AD", ORG) + " = " + sd("DC", ORG) + " \\quad (1)", "प्रमेय 8.9 से D, AC का मध्य-बिंदु है")])
s += kh("(ii) " + m("MD \\perp AC"))
s += num(2, CORR)
s += chain((ang("ADM", PUR), ang("ACB", PUR), "MD ∥ BC, तिर्यक रेखा AC — संगत कोण"),
           ("", dg(90, PUR) + " \\qquad \\ldots(2)", "दिया है"))
s += p("अतः " + m("MD \\perp AC") + "।")
s += kh("(iii) " + m("CM = MA = \\dfrac{1}{2}AB"))
s += num(3, LINEAR)
s += chain((ang("ADM", PUR) + " + " + ang("MDC", PUR), "180" + DEG, "किरण DM रेखा AC पर खड़ी है (रैखिक युग्म)"),
           ("90" + DEG + " + " + ang("MDC", PUR), "180" + DEG, "(2) से ∠ADM = 90° रखने पर"))
s += chain((ang("MDC", PUR), "180" + DEG + " - 90" + DEG, "+90° को पक्षांतर करने पर −90° हो जाता है"),
           ("", dg(90, PUR) + " \\qquad \\ldots(3)", "180 − 90 = 90"))
s += num(4, SAS)
s += kk(m("\\triangle AMD") + " और " + m("\\triangle CMD") + " में,",
        [(sd("AD", ORG) + " = " + sd("CD", ORG), "(1) से", "S", ORG),
         (ang("ADM", PUR) + " = " + ang("CDM", PUR), "(2) और (3) से — दोनों 90°", "A", PUR),
         (sd("DM", GRN) + " = " + sd("DM", GRN), "उभयनिष्ठ भुजा", "S", GRN)],
        ("\\triangle AMD \\cong \\triangle CMD", "SAS सर्वांगसमता नियम द्वारा"),
        [("A", "C"), ("M", "M"), ("D", "D")])
s += num(5, CPCT)
s += kk("", [(sd("CM", RED) + " = " + sd("MA", RED) + " \\quad (4)", "CPCT (A ↔ C, इसलिए MA ↔ MC)")])
s += chain((sd("CM", RED), sd("MA", RED), "(4) से"),
           ("", HALF + "AB", "M, AB का मध्य-बिंदु है, इसलिए MA = ½AB"))
s += ans("(i) " + m("AD = DC") + ", अर्थात् D भुजा AC का मध्य-बिंदु है (ii) " + m("\\angle ADM = 90^\\circ") + ", अर्थात् " + m("MD \\perp AC") + " (iii) "
         + m("CM = MA = \\dfrac{1}{2}AB") + " — सभी सिद्ध हुए।")
E2.append(("ABC एक त्रिभुज है जिसका कोण C समकोण है। कर्ण AB के मध्य-बिंदु M से होकर BC के समांतर खींची गई रेखा AC को D पर प्रतिच्छेद करती है। दर्शाइए कि "
           + "(i) D भुजा AC का मध्य-बिंदु है। (ii) " + m("MD \\perp AC") + " है। (iii) " + m("CM = MA = \\dfrac{1}{2}AB") + " है।", s))

# ---------------------------------------------------------------------
assert (len(E1), len(E2)) == (7, 6)
E1 = [(qt(a), b) for a, b in E1]
E2 = [(qt(a), b) for a, b in E2]
for E in (E1, E2):
    check_tex(E)
SUB = "कक्षा 9 गणित · अध्याय 8: " + CH + " · {} प्रश्न"
page(BASE, 8, CH, "exercise-8-1", "प्रश्नावली 8.1", SUB.format(len(E1)), E1,
     ("/hi/class-09/maths/chapter-07/exercise-7-3/", "प्रश्नावली 7.3"), (BASE + "exercise-8-2/", "प्रश्नावली 8.2"), css=CSS + EXTRA_CSS, boards=BOARDS9)
page(BASE, 8, CH, "exercise-8-2", "प्रश्नावली 8.2", SUB.format(len(E2)), E2,
     (BASE + "exercise-8-1/", "प्रश्नावली 8.1"), (BASE, "अध्याय 8"), css=CSS + EXTRA_CSS, boards=BOARDS9)
print("ok")
