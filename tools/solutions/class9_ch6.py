#!/usr/bin/env python3
"""Class 9 Maths, Chapter 6 (रेखाएँ और कोण): Exercises 6.1 and 6.2, Hindi medium.
Rationalised book (2023-24 onward): 6.1 has 6 questions; 6.2 keeps old Q2–Q6 (5 questions, figures 6.23–6.27);
old 6.2 Q1 and old exercise 6.3 (angle-sum of a triangle) were removed.
Question text and figures checked against NCERT Hindi PDF ihmh106 (archive.org copy, 2021-22 print)
and the rationalised English iemh106 (for which questions remain and the new figure numbers).
User rules: ज्ञात है / ज्ञात करना है boxes; every smallest step on its own line, one '=' per line;
axiom/theorem stated where used; figures drawn from the real angles, colour-coded like the working.
Run from repo root: python3 tools/solutions/class9_ch6.py
"""
import sys, pathlib, math
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from common import *  # noqa
from mixed_cells import *  # noqa

BASE = "/hi/class-09/maths/chapter-06/"
CH = "रेखाएँ और कोण"
BOARDS9 = ("यह हल <b>MP Board (MPBSE)</b> कक्षा 9 गणित की पाठ्यपुस्तक के अध्याय 6 ‘रेखाएँ और कोण’ के अनुसार है।")
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
"""

# ---------------- colours (same in figures and in the working) ----------------
INK, GRID = "#1d3a8a", "#94a3b8"
RED, BLU, GRN, ORG, PUR, TEA = "#d62839", "#1769c2", "#0f8a4c", "#e06a00", "#7c3aed", "#0e8a9a"
FONT = "font-family=\"Noto Sans, 'Noto Sans Devanagari', sans-serif\""


def C(col, t):
    return "\\textcolor{" + col + "}{" + t + "}"


def ang(name, col=None):
    t = "\\angle " + name
    return C(col, t) if col else t


DEG = "^\\circ"


def dg(v, col=None):
    t = f"{v}^\\circ"
    return C(col, t) if col else t


def ax(title, text):
    """An axiom / theorem stated exactly where it is used."""
    return f"<div class='ax'><b>{title}:</b> {text}</div>"


def kh(t):
    return f"<div class='kh'>{t}</div>"


def tp(t):
    return f"<div class='tp'>{t}</div>"


def chain(*rows, small=False):
    """Statement rows aligned at the relation sign; each row may carry its reason (कारण) below it.
    row = (lhs, rhs, reason) or (lhs, rhs, reason, sym).  lhs '' = continuation line '= ...'."""
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
    """A statement that is not an equation (e.g. AB ∥ EF) with its reason."""
    w = f"<div style='font-size:.86em;color:#5a6275'>({why_})</div>" if why_ else ""
    return f"<div class='eq' style='display:block'>{m(t)}{w}</div>"


def key(*items):
    return "<div class='key'>" + "".join(f"<span><i style='background:{c}'></i>{t}</span>" for c, t in items) + "</div>"


# ---------------- SVG figure kit (math angles: degrees, anticlockwise from →) ----------------
class Fig:
    n = 0

    def __init__(self, W, H):
        Fig.n += 1
        self.id, self.W, self.H, self.el, self.top, self.marks = f"f6{Fig.n}", W, H, [], [], {}

    @staticmethod
    def pol(o, deg, r):
        a = math.radians(deg)
        return (o[0] + r * math.cos(a), o[1] - r * math.sin(a))

    @staticmethod
    def dir(p, q):
        return math.degrees(math.atan2(-(q[1] - p[1]), q[0] - p[0])) % 360

    def _mk(self, col):
        if col not in self.marks:
            mid = f"{self.id}m{len(self.marks)}"
            self.marks[col] = mid
        return self.marks[col]

    def line(self, p, q, col=INK, w=2.2, a1=False, a2=False, dash=None):
        d = f" stroke-dasharray='{dash}'" if dash else ""
        ms = f" marker-start='url(#{self._mk(col)})'" if a1 else ""
        me = f" marker-end='url(#{self._mk(col)})'" if a2 else ""
        self.el.append(f"<line x1='{p[0]:.1f}' y1='{p[1]:.1f}' x2='{q[0]:.1f}' y2='{q[1]:.1f}' stroke='{col}' stroke-width='{w}' "
                       f"stroke-linecap='round'{d}{ms}{me}/>")

    def fline(self, p, q, col=INK, w=2.2, dash=None):
        """full line with arrowheads at both ends"""
        self.line(p, q, col, w, True, True, dash)

    def ray(self, o, deg, length, col=INK, w=2.2, arrow=True, dash=None):
        q = self.pol(o, deg, length)
        self.line(o, q, col, w, False, arrow, dash)
        return q

    def tick(self, p, deg, col=INK, h=6):
        a, b = self.pol(p, deg + 90, h), self.pol(p, deg - 90, h)
        self.line(a, b, col, 1.8)

    def mid_arrow(self, p, q, col=INK, at=0.55, size=9):
        """small arrowhead on a segment showing direction p → q"""
        d = self.dir(p, q)
        c = (p[0] + (q[0] - p[0]) * at, p[1] + (q[1] - p[1]) * at)
        a, b = self.pol(c, d + 150, size), self.pol(c, d - 150, size)
        self.el.append(f"<path d='M{a[0]:.1f},{a[1]:.1f} L{c[0]:.1f},{c[1]:.1f} L{b[0]:.1f},{b[1]:.1f}' fill='none' stroke='{col}' "
                       "stroke-width='2' stroke-linecap='round' stroke-linejoin='round'/>")

    def par(self, p, q, n=1, col=INK, at=0.5):
        """parallel-line chevrons (n of them) on line p→q"""
        d = self.dir(p, q)
        for k in range(n):
            c = self.pol((p[0] + (q[0] - p[0]) * at, p[1] + (q[1] - p[1]) * at), d, (k - (n - 1) / 2) * 8)
            a, b = self.pol(c, d + 150, 11), self.pol(c, d - 150, 11)
            self.el.append(f"<path d='M{a[0]:.1f},{a[1]:.1f} L{c[0]:.1f},{c[1]:.1f} L{b[0]:.1f},{b[1]:.1f}' fill='none' stroke='{col}' "
                           "stroke-width='2.6' stroke-linecap='round' stroke-linejoin='round'/>")

    def arc(self, o, a1, a2, r, col, fill=True, n=1, w=2, dash=None, op=.16):
        """angle from direction a1 anticlockwise to a2"""
        span = (a2 - a1) % 360
        large = 1 if span > 180 else 0
        p1, p2 = self.pol(o, a1, r), self.pol(o, a2, r)
        if fill:
            self.el.append(f"<path d='M{o[0]:.1f},{o[1]:.1f} L{p1[0]:.1f},{p1[1]:.1f} A{r},{r} 0 {large} 0 {p2[0]:.1f},{p2[1]:.1f} Z' "
                           f"fill='{col}' fill-opacity='{op}' stroke='none'/>")
        d = f" stroke-dasharray='{dash}'" if dash else ""
        for k in range(n):
            rr = r - 4 * k
            q1, q2 = self.pol(o, a1, rr), self.pol(o, a2, rr)
            self.el.append(f"<path d='M{q1[0]:.1f},{q1[1]:.1f} A{rr},{rr} 0 {large} 0 {q2[0]:.1f},{q2[1]:.1f}' fill='none' "
                           f"stroke='{col}' stroke-width='{w}'{d}/>")

    def right(self, o, a1, s=13, col=INK):
        p1 = self.pol(o, a1, s)
        p3 = self.pol(o, a1 + 90, s)
        p2 = self.pol(p1, a1 + 90, s)
        self.el.append(f"<path d='M{p1[0]:.1f},{p1[1]:.1f} L{p2[0]:.1f},{p2[1]:.1f} L{p3[0]:.1f},{p3[1]:.1f}' fill='none' stroke='{col}' stroke-width='1.8'/>")

    def text(self, x, y, t, col=INK, size=16, italic=False, bold=True, anchor="middle"):
        st = " font-style='italic'" if italic else ""
        self.top.append(f"<text x='{x:.1f}' y='{y:.1f}' font-size='{size}' font-weight='{700 if bold else 500}' fill='{col}' "
                        f"text-anchor='{anchor}' dominant-baseline='central'{st} stroke='#fbfcff' stroke-width='4.5' "
                        f"stroke-linejoin='round' paint-order='stroke'>{t}</text>")

    def lab(self, p, t, deg, d=15, col=INK, size=16, italic=False):
        """label t placed at distance d from point p, in direction deg"""
        q = self.pol(p, deg, d)
        self.text(q[0], q[1], t, col, size, italic)

    def alab(self, o, a1, a2, r, t, col, size=14, italic=False):
        """angle label on the bisector of angle a1→a2 at radius r"""
        mid = a1 + ((a2 - a1) % 360) / 2
        self.lab(o, t, mid, r, col, size, italic)

    def dot(self, p, col=INK, r=3.2):
        self.top.insert(0, f"<circle cx='{p[0]:.1f}' cy='{p[1]:.1f}' r='{r}' fill='{col}'/>")

    def hatch(self, p, q, side=1, col=INK, step=9, h=7):
        """mirror back: short slanted strokes on one side of segment p→q"""
        d = self.dir(p, q)
        L = math.dist(p, q)
        k = step / 2
        while k < L:
            c = self.pol(p, d, k)
            e = self.pol(c, d + side * 125, h)
            self.el.append(f"<line x1='{c[0]:.1f}' y1='{c[1]:.1f}' x2='{e[0]:.1f}' y2='{e[1]:.1f}' stroke='{col}' stroke-width='1.2'/>")
            k += step

    def svg(self, cap):
        defs = "".join(f"<marker id='{mid}' viewBox='0 0 10 10' refX='8.5' refY='5' markerWidth='11' markerHeight='11' "
                       f"markerUnits='userSpaceOnUse' orient='auto-start-reverse'><path d='M0,0.5 L10,5 L0,9.5 L2.6,5 z' fill='{col}'/></marker>"
                       for col, mid in self.marks.items())
        return (f"<div class='fig'><svg viewBox='0 0 {self.W} {self.H}' role='img' aria-label='{cap}' style='max-width:{max(self.W, 360)}px' {FONT}>"
                f"<defs>{defs}</defs>{''.join(self.el)}{''.join(self.top)}</svg><div class='cap'>{cap}</div></div>")


def pair(a, b):
    return f"<div class='figs'>{a}{b}</div>"


def check_tex(E):
    import re as _re
    for _q, _sol in E:
        for _t in _re.findall(r"\\\((.+?)\\\)", _q + _sol):
            assert not _re.search(r"[\u0900-\u097F]", _t), ("Devanagari in TeX", _t)


LINEAR = ax("रैखिक युग्म अभिगृहीत (अभिगृहीत 6.1)", "यदि एक किरण एक रेखा पर खड़ी हो, तो इस प्रकार बने दोनों आसन्न कोणों का योग " + m("180^\\circ") + " होता है।")
VOPP = ax("प्रमेय 6.1 (शीर्षाभिमुख कोण)", "यदि दो रेखाएँ परस्पर प्रतिच्छेद करती हैं, तो शीर्षाभिमुख कोण बराबर होते हैं।")
LINEAR2 = ax("अभिगृहीत 6.2 (रैखिक युग्म अभिगृहीत का विलोम)", "यदि दो आसन्न कोणों का योग " + m("180^\\circ") + " है, तो उनकी अउभयनिष्ठ भुजाएँ एक रेखा बनाती हैं।")
ROUND = ax("एक बिंदु के चारों ओर के कोण", "एक बिंदु के चारों ओर बने सभी कोणों का योग " + m("360^\\circ") + " होता है।")
REFLEX = ax("प्रतिवर्ती कोण", "किसी कोण का प्रतिवर्ती कोण " + m("= 360^\\circ -") + " वह कोण। (प्रतिवर्ती कोण " + m("180^\\circ") + " से बड़ा और " + m("360^\\circ") + " से छोटा होता है।)")
ALT = ax("एकांतर अंतः कोण", "यदि एक तिर्यक रेखा दो समांतर रेखाओं को प्रतिच्छेद करे, तो एकांतर अंतः कोणों का प्रत्येक युग्म बराबर होता है।")
ALT_C = ax("एकांतर अंतः कोणों का विलोम", "यदि एक तिर्यक रेखा दो रेखाओं को इस प्रकार प्रतिच्छेद करे कि एकांतर अंतः कोणों का एक युग्म बराबर है, तो दोनों रेखाएँ परस्पर समांतर होती हैं।")
CORR = ax("संगत कोण अभिगृहीत", "यदि एक तिर्यक रेखा दो समांतर रेखाओं को प्रतिच्छेद करे, तो संगत कोणों का प्रत्येक युग्म बराबर होता है।")
CORR_C = ax("संगत कोण अभिगृहीत का विलोम", "यदि एक तिर्यक रेखा दो रेखाओं को इस प्रकार प्रतिच्छेद करे कि संगत कोणों का एक युग्म बराबर है, तो दोनों रेखाएँ परस्पर समांतर होती हैं।")
INT = ax("तिर्यक रेखा के एक ही ओर के अंतः कोण", "यदि एक तिर्यक रेखा दो समांतर रेखाओं को प्रतिच्छेद करे, तो तिर्यक रेखा के एक ही ओर के अंतः कोणों का प्रत्येक युग्म संपूरक होता है (योग " + m("180^\\circ") + ")।")
TH66 = ax("प्रमेय 6.6", "वे रेखाएँ जो एक ही रेखा के समांतर हों, परस्पर समांतर होती हैं।")


def num(i, a):
    """number an axiom box (1), (2) ... inside one solution"""
    return a.replace("<b>", f"<b>({i}) ", 1)


# =====================================================================
# Exercise 6.1
# =====================================================================
E1 = []

# ---------- Q1 (आकृति 6.13) ----------
aAOC, aBOD = 40, 40
aBOE = 70 - aAOC
aCOE = 180 - aAOC - aBOE
rCOE = 360 - aCOE
assert (aBOE, aCOE, rCOE) == (30, 110, 250)
dA, dB, dC, dD, dE = 180, 0, 180 - aAOC, 360 - aBOD, aBOE


def fig613(sol):
    f = Fig(360, 250)
    O = (178, 128)
    f.fline(f.pol(O, dA, 150), f.pol(O, dB, 150))
    f.fline(f.pol(O, dC, 125), f.pol(O, dD, 125))
    f.ray(O, dE, 138)
    for d, r in ((dA, 122), (dB, 122), (dC, 100), (dD, 100), (dE, 112)):
        f.tick(f.pol(O, d, r), d)
    if not sol:
        f.arc(O, dD, 360, 30, ORG)
        f.alab(O, dD, 360, 47, "40°", ORG, 14)
    else:
        f.arc(O, dD, 360, 30, ORG)
        f.alab(O, dD, 360, 47, "40°", ORG, 13)
        f.arc(O, dC, dA, 30, RED)
        f.alab(O, dC, dA, 47, "40°", RED, 13)
        f.arc(O, 0, dE, 44, BLU)
        f.alab(O, 0, dE, 62, "30°", BLU, 13)
        f.arc(O, dE, dC, 22, GRN)
        f.alab(O, dE, dC, 38, "110°", GRN, 13)
        f.arc(O, dC, dE + 360, 72, PUR, fill=False, dash="5 4")
        f.alab(O, dC, dE + 360, 88, "250°", PUR, 13)
    f.dot(O)
    f.lab(f.pol(O, dA, 122), "A", 245, 17)
    f.lab(f.pol(O, dB, 122), "B", 295, 17)
    f.lab(f.pol(O, dC, 100), "C", 230, 17)
    f.lab(f.pol(O, dD, 100), "D", 215, 17)
    f.lab(f.pol(O, dE, 112), "E", 120, 16)
    f.lab(O, "O", 262 if not sol else 250, 18 if not sol else 30)
    return f.svg("आकृति 6.13" if not sol else "हल की आकृति: रंगीन कोण (बैंगनी बिंदुदार = प्रतिवर्ती ∠COE)")


s = given("रेखाएँ " + m("AB") + " और " + m("CD") + " बिंदु " + m("O") + " पर प्रतिच्छेद करती हैं।<br>"
          + m("\\angle AOC + \\angle BOE = 70^\\circ") + "<br>" + m(ang("BOD", ORG) + " = " + dg(40, ORG)),
          "(i) " + m(ang("BOE", BLU)) + "<br>(ii) प्रतिवर्ती " + m(ang("COE", PUR)))
s += pair(fig613(False), fig613(True))
s += key((RED, "∠AOC"), (ORG, "∠BOD"), (BLU, "∠BOE"), (GRN, "∠COE"), (PUR, "प्रतिवर्ती ∠COE"))
s += kh("चरण 1: " + m(ang("AOC", RED)) + " ज्ञात करना")
s += num(1, VOPP)
s += chain((ang("AOC", RED), ang("BOD", ORG), "रेखाएँ AB और CD प्रतिच्छेद करती हैं, ∠AOC और ∠BOD शीर्षाभिमुख कोण हैं"),
           ("", dg(40, RED), "∠BOD = 40° दिया है"))
s += kh("चरण 2: " + m(ang("BOE", BLU)) + " ज्ञात करना")
s += chain((ang("AOC", RED) + " + " + ang("BOE", BLU), "70" + DEG, "दिया है"),
           (dg(40, RED) + " + " + ang("BOE", BLU), "70" + DEG, "∠AOC = 40° रखने पर"))
s += chain((ang("BOE", BLU), "70" + DEG + " - " + dg(40, RED), "+40° को पक्षांतर करने पर −40° हो जाता है"),
           ("", dg(30, BLU), "70 − 40 = 30"))
s += kh("चरण 3: " + m(ang("COE", GRN)) + " ज्ञात करना")
s += num(2, LINEAR)
s += chain((ang("AOC", RED) + " + \\angle COB", "180" + DEG, "किरण OC रेखा AB पर खड़ी है (रैखिक युग्म)"))
s += chain(("\\angle COB", ang("COE", GRN) + " + " + ang("EOB", BLU), "किरण OE, ∠COB के अंदर है"))
s += chain((ang("AOC", RED) + " + " + ang("COE", GRN) + " + " + ang("EOB", BLU), "180" + DEG, "∠COB का मान रखने पर"),
           (dg(40, RED) + " + " + ang("COE", GRN) + " + " + dg(30, BLU), "180" + DEG, "∠AOC = 40°, ∠EOB = 30° रखने पर"),
           ("70" + DEG + " + " + ang("COE", GRN), "180" + DEG, "40 + 30 = 70"))
s += chain((ang("COE", GRN), "180" + DEG + " - 70" + DEG, "+70° को पक्षांतर करने पर"),
           ("", dg(110, GRN), "180 − 70 = 110"))
s += kh("चरण 4: प्रतिवर्ती " + m(ang("COE", PUR)) + " ज्ञात करना")
s += num(3, REFLEX)
s += chain(("\\text{प्रतिवर्ती} " + ang("COE", PUR), "360" + DEG + " - " + ang("COE", GRN), "प्रतिवर्ती कोण = 360° − कोण"),
           ("", "360" + DEG + " - " + dg(110, GRN), "∠COE = 110° रखने पर"),
           ("", dg(250, PUR), "360 − 110 = 250"))
s += ans("(i) " + m(ang("BOE", BLU) + " = " + dg(30, BLU)) + " (ii) प्रतिवर्ती " + m(ang("COE", PUR) + " = " + dg(250, PUR)))
E1.append(("आकृति 6.13 में, रेखाएँ " + m("AB") + " और " + m("CD") + " बिंदु " + m("O") + " पर प्रतिच्छेद करती हैं। यदि "
           + m("\\angle AOC + \\angle BOE = 70^\\circ") + " है और " + m("\\angle BOD = 40^\\circ") + " है, तो "
           + m("\\angle BOE") + " और प्रतिवर्ती " + m("\\angle COE") + " ज्ञात कीजिए।", s))

# ---------- Q2 (आकृति 6.14) ----------
k2 = 90 / 5
a2, b2 = 2 * k2, 3 * k2
c2 = 180 - b2
assert (k2, a2, b2, c2) == (18, 36, 54, 126) and a2 + b2 == 90
dX, dY, dP, dM = 180, 0, 90, 180 - b2
dN = dM - 180  # -54


def fig614(sol):
    f = Fig(360, 260)
    O = (178, 140)
    f.fline(f.pol(O, dX, 150), f.pol(O, dY, 150))
    f.fline(f.pol(O, dM, 125), f.pol(O, dN, 125))
    f.ray(O, dP, 118)
    for d, r in ((dX, 125), (dY, 125), (dM, 100), (dN, 100), (dP, 98)):
        f.tick(f.pol(O, d, r), d)
    f.right(O, 0, 13)
    f.arc(O, dP, dM, 40, RED)
    f.alab(O, dP, dM, 54, "a", RED, 15, True)
    f.arc(O, dM, dX, 28, BLU)
    f.alab(O, dM, dX, 44, "b", BLU, 15, True)
    f.arc(O, dX, dN + 360, 32, GRN)
    f.alab(O, dX, dN + 360, 47, "c", GRN, 15, True)
    if sol:
        f.text(O[0] + 30, O[1] - 26, "90°", INK, 12)
        for i_, (t_, c_) in enumerate((("a = 36°", RED), ("b = 54°", BLU), ("c = 126°", GRN))):
            f.text(262, 28 + 22 * i_, t_, c_, 15, False, True, "start")
    f.dot(O)
    f.lab(f.pol(O, dX, 125), "X", 260, 17)
    f.lab(f.pol(O, dY, 125), "Y", 280, 17)
    f.lab(f.pol(O, dM, 100), "M", 205, 17)
    f.lab(f.pol(O, dN, 100), "N", 220, 17)
    f.lab(f.pol(O, dP, 98), "P", 0, 14)
    f.lab(O, "O", 320, 20)
    return f.svg("आकृति 6.14" if not sol else "हल की आकृति: a लाल, b नीला, c हरा")


s = given("रेखाएँ " + m("XY") + " और " + m("MN") + " बिंदु " + m("O") + " पर प्रतिच्छेद करती हैं।<br>"
          + m("\\angle POY = 90^\\circ") + "<br>" + m(C(RED, "a") + " : " + C(BLU, "b") + " = 2 : 3"), m(C(GRN, "c")) + " का मान")
s += pair(fig614(False), fig614(True))
s += kh("चरण 1: " + m("\\angle XOP") + " ज्ञात करना")
s += num(1, LINEAR)
s += chain(("\\angle XOP + \\angle POY", "180" + DEG, "किरण OP रेखा XY पर खड़ी है (रैखिक युग्म)"),
           ("\\angle XOP + 90" + DEG, "180" + DEG, "∠POY = 90° रखने पर"))
s += chain(("\\angle XOP", "180" + DEG + " - 90" + DEG, "+90° को पक्षांतर करने पर"), ("", "90" + DEG, "180 − 90 = 90"))
s += kh("चरण 2: " + m(C(RED, "a")) + " और " + m(C(BLU, "b")) + " ज्ञात करना")
s += chain((C(RED, "a") + " + " + C(BLU, "b"), "\\angle XOP", "किरण OM, ∠XOP के अंदर है: ∠POM + ∠MOX = ∠XOP"),
           ("", "90" + DEG, "∠XOP = 90°"))
s += p(m(C(RED, "a") + " : " + C(BLU, "b") + " = 2 : 3") + " है, इसलिए माना " + m(C(RED, "a") + " = 2k") + " और " + m(C(BLU, "b") + " = 3k") + "।")
s += chain((C(RED, "2k") + " + " + C(BLU, "3k"), "90" + DEG, "a = 2k, b = 3k रखने पर"),
           ("5k", "90" + DEG, "2k + 3k = 5k"))
s += chain(("k", "\\dfrac{90^\\circ}{5}", "5 से भाग देने पर (गुणा का 5 पक्षांतर होकर भाग बन जाता है)"),
           ("", "18" + DEG, "90 ÷ 5 = 18"))
s += chain((C(RED, "a"), C(RED, "2k"), ""), ("", "2 \\times 18" + DEG, "k = 18° रखने पर"), ("", dg(36, RED), "2 × 18 = 36"))
s += chain((C(BLU, "b"), C(BLU, "3k"), ""), ("", "3 \\times 18" + DEG, "k = 18° रखने पर"), ("", dg(54, BLU), "3 × 18 = 54"))
s += kh("चरण 3: " + m(C(GRN, "c")) + " ज्ञात करना")
s += num(2, LINEAR)
s += chain((C(BLU, "b") + " + " + C(GRN, "c"), "180" + DEG, "किरण OX रेखा MN पर खड़ी है: ∠XOM + ∠XON = 180°"),
           (dg(54, BLU) + " + " + C(GRN, "c"), "180" + DEG, "b = 54° रखने पर"))
s += chain((C(GRN, "c"), "180" + DEG + " - " + dg(54, BLU), "+54° को पक्षांतर करने पर"),
           ("", dg(126, GRN), "180 − 54 = 126"))
s += ans(m(C(GRN, "c") + " = " + dg(126, GRN)) + " &nbsp;(साथ में " + m(C(RED, "a") + " = 36^\\circ") + ", " + m(C(BLU, "b") + " = 54^\\circ") + ")")
E1.append(("आकृति 6.14 में, रेखाएँ " + m("XY") + " और " + m("MN") + " बिंदु " + m("O") + " पर प्रतिच्छेद करती हैं। यदि "
           + m("\\angle POY = 90^\\circ") + " और " + m("a : b = 2 : 3") + " है, तो " + m("c") + " ज्ञात कीजिए।", s))

# ---------- Q3 (आकृति 6.15) ----------
base = 62


def fig615(sol):
    f = Fig(360, 205)
    Q, R = (105, 172), (255, 172)
    h = (R[0] - Q[0]) / 2 * math.tan(math.radians(base))
    P = ((Q[0] + R[0]) / 2, Q[1] - h)
    f.fline((15, 172), (345, 172))
    f.line(Q, P)
    f.line(P, R)
    f.tick((38, 172), 0)
    f.tick((322, 172), 0)
    dq, dr = Fig.dir(Q, P), Fig.dir(R, P)
    f.arc(Q, 0, dq, 24, RED)
    f.arc(R, dr, 180, 24, RED)
    if sol:
        f.arc(Q, dq, 180, 18, BLU, n=2)
        f.arc(R, 0, dr, 18, BLU, n=2)
        f.alab(Q, 0, dq, 50, "∠PQR", RED, 11)
        f.alab(R, dr, 180, 50, "∠PRQ", RED, 11)
        f.alab(Q, dq, 180, 46, "∠PQS", BLU, 11)
        f.alab(R, 0, dr, 46, "∠PRT", BLU, 11)
    for pnt, t, d in ((P, "P", 90), (Q, "Q", 260), (R, "R", 280)):
        f.dot(pnt)
        f.lab(pnt, t, d, 17)
    f.lab((38, 172), "S", 270, 18)
    f.lab((322, 172), "T", 270, 18)
    return f.svg("आकृति 6.15" if not sol else "हल की आकृति: लाल = अंदर के बराबर कोण, नीला = बाहर के कोण")


s = given(m("ST") + " एक रेखा है, " + m("Q") + " और " + m("R") + " उस पर हैं।<br>" + m(ang("PQR", RED) + " = " + ang("PRQ", RED)),
          "सिद्ध करना है: " + m(ang("PQS", BLU) + " = " + ang("PRT", BLU)))
s += pair(fig615(False), fig615(True))
s += num(1, LINEAR)
s += kh("उपपत्ति (कथन और कारण):")
s += chain((ang("PQS", BLU) + " + " + ang("PQR", RED), "180^\\circ \\qquad \\ldots(1)", "किरण QP रेखा ST पर खड़ी है (रैखिक युग्म अभिगृहीत)"),
           (ang("PRT", BLU) + " + " + ang("PRQ", RED), "180^\\circ \\qquad \\ldots(2)", "किरण RP रेखा ST पर खड़ी है (रैखिक युग्म अभिगृहीत)"))
s += chain((ang("PQS", BLU) + " + " + ang("PQR", RED), ang("PRT", BLU) + " + " + ang("PRQ", RED), "(1) और (2) से, दोनों 180° के बराबर हैं"))
s += chain((ang("PRQ", RED), ang("PQR", RED) + " \\qquad \\ldots(3)", "दिया है"))
s += chain((ang("PQS", BLU) + " + " + ang("PQR", RED), ang("PRT", BLU) + " + " + ang("PQR", RED), "(3) से ∠PRQ के स्थान पर ∠PQR रखने पर"))
s += chain((ang("PQS", BLU), ang("PRT", BLU) + " + " + ang("PQR", RED) + " - " + ang("PQR", RED), "+∠PQR को पक्षांतर करने पर"),
           ("", ang("PRT", BLU), "∠PQR − ∠PQR = 0"))
s += ans(m(ang("PQS", BLU) + " = " + ang("PRT", BLU)) + " सिद्ध हुआ।")
E1.append(("आकृति 6.15 में, यदि " + m("\\angle PQR = \\angle PRQ") + " है, तो सिद्ध कीजिए कि " + m("\\angle PQS = \\angle PRT") + " है।", s))

# ---------- Q4 (आकृति 6.16) ----------
dB4, dC4, dA4, dD4 = 38, 78, 218, 280
x4, y4, z4, w4 = dC4 - dB4, dA4 - dC4, dD4 - dA4, 360 - dD4 + dB4
assert x4 + y4 + z4 + w4 == 360 and x4 + y4 == z4 + w4 == 180


def fig616(sol):
    f = Fig(360, 270)
    O = (182, 132)
    for d, L, t, ld in ((dA4, 125, "A", 300), (dB4, 135, "B", 300), (dC4, 118, "C", 180), (dD4, 118, "D", 0)):
        q = f.ray(O, d, L)
        tk = f.pol(O, d, L - 18)
        f.tick(tk, d)
        f.lab(tk, t, ld if not (t == "B") else 120, 17)
    f.arc(O, dB4, dC4, 34, RED)
    f.alab(O, dB4, dC4, 50, "x", RED, 15, True)
    f.arc(O, dC4, dA4, 24, BLU)
    f.alab(O, dC4, dA4, 39, "y", BLU, 15, True)
    f.arc(O, dA4, dD4, 30, GRN)
    f.alab(O, dA4, dD4, 45, "z", GRN, 15, True)
    f.arc(O, dD4, dB4 + 360, 20, ORG)
    f.lab(O, "w", 320, 42, ORG, 15, True)
    if sol:
        f.line(f.pol(O, dB4, 150), f.pol(O, dA4, 150), PUR, 1.6, dash="6 5")
    f.dot(O)
    f.lab(O, "O", 4, 33)
    return f.svg("आकृति 6.16" if not sol else "हल की आकृति: x + y = 180° होने पर OA और OB एक सीध में (बैंगनी बिंदुदार रेखा)")


s = given("किरणें " + m("OA, OB, OC, OD") + " बिंदु " + m("O") + " से निकलती हैं।<br>"
          + m(C(RED, "x") + " + " + C(BLU, "y") + " = " + C(ORG, "w") + " + " + C(GRN, "z")),
          "सिद्ध करना है: " + m("AOB") + " एक रेखा है।")
s += pair(fig616(False), fig616(True))
s += tp("आकृति से: " + m(C(RED, "x") + " = \\angle BOC") + ", " + m(C(BLU, "y") + " = \\angle COA") + ", " + m(C(GRN, "z") + " = \\angle AOD") + ", " + m(C(ORG, "w") + " = \\angle DOB"))
s += kh("उपपत्ति (कथन और कारण):")
s += num(1, ROUND)
X4, Y4, Z4, W4 = C(RED, "x"), C(BLU, "y"), C(GRN, "z"), C(ORG, "w")
s += chain((X4 + " + " + Y4 + " + " + Z4 + " + " + W4, "360^\\circ \\qquad \\ldots(1)", "बिंदु O के चारों ओर के कोण"))
s += chain((W4 + " + " + Z4, X4 + " + " + Y4 + " \\qquad \\ldots(2)", "दिया है"))
s += chain((X4 + " + " + Y4 + " + (" + W4 + " + " + Z4 + ")", "360" + DEG, "(1) के पदों को क्रम बदलकर लिखा"),
           (X4 + " + " + Y4 + " + (" + X4 + " + " + Y4 + ")", "360" + DEG, "(2) से w + z के स्थान पर x + y रखने पर"),
           ("2(" + X4 + " + " + Y4 + ")", "360" + DEG, "(x + y) + (x + y) = 2(x + y)"))
s += chain((X4 + " + " + Y4, "\\dfrac{360^\\circ}{2}", "2 को पक्षांतर करने पर (गुणा → भाग)"), ("", "180" + DEG, "360 ÷ 2 = 180"))
s += chain(("\\angle BOC + \\angle COA", "180" + DEG, "x = ∠BOC, y = ∠COA"))
s += p(m("\\angle BOC") + " और " + m("\\angle COA") + " आसन्न कोण हैं: उभयनिष्ठ भुजा " + m("OC") + " है और अउभयनिष्ठ भुजाएँ " + m("OB") + " तथा " + m("OA") + " हैं।")
s += num(2, LINEAR2)
s += p("इसलिए अउभयनिष्ठ भुजाएँ " + m("OA") + " और " + m("OB") + " एक ही रेखा बनाती हैं (अभिगृहीत 6.2)।")
s += ans(m("AOB") + " एक रेखा है। सिद्ध हुआ।")
E1.append(("आकृति 6.16 में, यदि " + m("x + y = w + z") + " है, तो सिद्ध कीजिए कि " + m("AOB") + " एक रेखा है।", s))

# ---------- Q5 (आकृति 6.17) ----------
dS5 = 116
POS5, ROS5, QOS5 = 180 - dS5, dS5 - 90, dS5
assert ROS5 * 2 == QOS5 - POS5


def fig617(sol):
    f = Fig(360, 220)
    O = (180, 170)
    f.fline((25, 170), (335, 170))
    f.tick((52, 170), 0)
    f.tick((308, 170), 0)
    f.ray(O, 90, 135)
    f.tick(f.pol(O, 90, 118), 90)
    f.ray(O, dS5, 145)
    f.tick(f.pol(O, dS5, 128), dS5)
    f.right(O, 0, 14)
    if sol:
        f.arc(O, 90, dS5, 52, RED)
        f.alab(O, 90, dS5, 100, "∠ROS", RED, 11)
        f.arc(O, dS5, 180, 34, BLU)
        f.alab(O, dS5, 180, 66, "∠POS", BLU, 12)
        f.arc(O, 0, dS5, 84, GRN, fill=False, w=1.6, dash="6 4")
        f.alab(O, 20, 50, 98, "∠QOS", GRN, 12)
    f.dot(O)
    f.lab((52, 170), "P", 270, 18)
    f.lab((308, 170), "Q", 270, 18)
    f.lab(O, "O", 270, 20)
    f.lab(f.pol(O, 90, 118), "R", 0, 16)
    f.lab(f.pol(O, dS5, 128), "S", 205, 17)
    return f.svg("आकृति 6.17" if not sol else "हल की आकृति: ∠ROS लाल, ∠POS नीला, ∠QOS हरा")


s = given(m("POQ") + " एक रेखा है।<br>किरण " + m("OR \\perp PQ") + "<br>किरण " + m("OS") + ", किरणों " + m("OP") + " और " + m("OR") + " के बीच है।",
          "सिद्ध करना है: " + m(ang("ROS", RED) + " = \\dfrac{1}{2}(" + ang("QOS", GRN) + " - " + ang("POS", BLU) + ")"))
s += pair(fig617(False), fig617(True))
s += kh("उपपत्ति (कथन और कारण):")
s += num(1, ax("लम्ब की परिभाषा", m("OR \\perp PQ") + " का अर्थ है कि " + m("\\angle ROQ = 90^\\circ") + " और " + m("\\angle ROP = 90^\\circ") + "।"))
s += chain((ang("QOS", GRN), "\\angle QOR + " + ang("ROS", RED), "किरण OR, ∠QOS के अंदर है"),
           ("", "90^\\circ + " + ang("ROS", RED) + " \\qquad \\ldots(1)", "∠QOR = 90° रखने पर"))
s += chain((ang("POS", BLU) + " + " + ang("ROS", RED), "\\angle POR", "किरण OS, ∠POR के अंदर है"),
           ("", "90" + DEG, "∠POR = 90°"))
s += chain((ang("POS", BLU), "90^\\circ - " + ang("ROS", RED) + " \\qquad \\ldots(2)", "+∠ROS को पक्षांतर करने पर"))
s += chain((ang("QOS", GRN) + " - " + ang("POS", BLU), "(90^\\circ + " + ang("ROS", RED) + ")", "(1) में से (2) घटाने पर"),
           ("", "{} - (90^\\circ - " + ang("ROS", RED) + ")", "", ""),
           ("", "90^\\circ + " + ang("ROS", RED) + " - 90^\\circ + " + ang("ROS", RED), "कोष्ठक खोलने पर: −(−∠ROS) = +∠ROS"),
           ("", ang("ROS", RED) + " + " + ang("ROS", RED), "90° − 90° = 0"),
           ("", "2" + ang("ROS", RED), "∠ROS + ∠ROS = 2∠ROS"), small=True)
s += chain(("2" + ang("ROS", RED), ang("QOS", GRN) + " - " + ang("POS", BLU), "पक्ष बदलकर लिखने पर"))
s += chain((ang("ROS", RED), "\\dfrac{1}{2}(" + ang("QOS", GRN) + " - " + ang("POS", BLU) + ")", "2 को पक्षांतर करने पर (गुणा → भाग)"))
s += tp("जाँच (आकृति के कोणों से): " + m(f"\\angle QOS = {QOS5}^\\circ") + ", " + m(f"\\angle POS = {POS5}^\\circ") + ", तो "
        + m(f"\\tfrac{{1}}{{2}}({QOS5}^\\circ - {POS5}^\\circ) = {ROS5}^\\circ = \\angle ROS") + " ✔")
s += ans(m(ang("ROS", RED) + " = \\dfrac{1}{2}(" + ang("QOS", GRN) + " - " + ang("POS", BLU) + ")") + " सिद्ध हुआ।")
E1.append(("आकृति 6.17 में, " + m("POQ") + " एक रेखा है। किरण " + m("OR") + " रेखा " + m("PQ") + " पर लम्ब है। किरणों " + m("OP")
           + " और " + m("OR") + " के बीच में " + m("OS") + " एक अन्य किरण है। सिद्ध कीजिए: " + m("\\angle ROS = \\dfrac{1}{2}(\\angle QOS - \\angle POS)"), s))

# ---------- Q6 (drawn figure) ----------
XYZ6 = 64
ZYP6 = 180 - XYZ6
QYP6 = ZYP6 / 2
XYQ6 = XYZ6 + QYP6
rQYP6 = 360 - QYP6
assert (ZYP6, QYP6, XYQ6, rQYP6) == (116, 58, 122, 302)
dZ6, dQ6 = 180 - XYZ6, QYP6


def fig6q6(sol):
    f = Fig(360, 230)
    Y = (175, 150)
    f.ray(Y, 180, 145, arrow=False)
    f.ray(Y, 0, 150, INK, 2.2, True, "7 5")
    f.ray(Y, dZ6, 125)
    f.ray(Y, dQ6, 130, TEA)
    Xp = f.pol(Y, 180, 135)
    f.dot(Xp)
    Pp = f.pol(Y, 0, 120)
    f.dot(Pp)
    f.arc(Y, dZ6, 180, 34, RED)
    f.alab(Y, dZ6, 180, 52, "64°", RED, 13)
    if not sol:
        f.arc(Y, dQ6, dZ6, 30, BLU, n=2)
        f.arc(Y, 0, dQ6, 30, BLU, n=2)
    else:
        f.arc(Y, dQ6, dZ6, 30, BLU, n=2)
        f.alab(Y, dQ6, dZ6, 47, "58°", BLU, 13)
        f.arc(Y, 0, dQ6, 30, BLU, n=2)
        f.alab(Y, 0, dQ6, 47, "58°", BLU, 13)
        f.arc(Y, dQ6, 360, 64, PUR, fill=False, dash="5 4")
        f.alab(Y, dQ6, 360, 80, "302°", PUR, 13)
        f.arc(Y, dQ6, 180, 90, GRN, fill=False, w=1.6)
        f.alab(Y, dQ6 + 60, 180, 102, "122°", GRN, 13)
    f.dot(Y)
    f.lab(Xp, "X", 270, 17)
    f.lab(Pp, "P", 270, 17)
    f.lab(Y, "Y", 270, 18)
    f.lab(f.pol(Y, dZ6, 125), "Z", 180, 15)
    f.lab(f.pol(Y, dQ6, 130), "Q", 0, 15, TEA)
    return f.svg("प्रश्न 6 की आकृति: XY को P तक बढ़ाया (बिंदुदार), YQ ∠ZYP का समद्विभाजक" if not sol
                 else "हल की आकृति: ∠XYQ हरा चाप, प्रतिवर्ती ∠QYP बैंगनी बिंदुदार")


s = given(m(ang("XYZ", RED) + " = " + dg(64, RED)) + "<br>" + m("XY") + " को बिंदु " + m("P") + " तक बढ़ाया गया है।<br>किरण " + m("YQ") + ", "
          + m("\\angle ZYP") + " को समद्विभाजित करती है।",
          "(i) " + m(ang("XYQ", GRN)) + "<br>(ii) प्रतिवर्ती " + m(ang("QYP", PUR)))
s += p("<b>आकृति बनाना:</b> एक रेखाखंड " + m("XY") + " खींचिए। " + m("Y") + " पर " + m("64^\\circ") + " का कोण " + m("\\angle XYZ")
       + " बनाइए। " + m("XY") + " को " + m("Y") + " से आगे " + m("P") + " तक बढ़ाइए। फिर " + m("\\angle ZYP") + " का समद्विभाजक " + m("YQ") + " खींचिए।")
s += pair(fig6q6(False), fig6q6(True))
s += kh("चरण 1: " + m("\\angle ZYP") + " ज्ञात करना")
s += num(1, LINEAR)
s += chain((ang("XYZ", RED) + " + \\angle ZYP", "180" + DEG, "किरण YZ रेखा XP पर खड़ी है (रैखिक युग्म)"),
           (dg(64, RED) + " + \\angle ZYP", "180" + DEG, "∠XYZ = 64° रखने पर"))
s += chain(("\\angle ZYP", "180^\\circ - " + dg(64, RED), "+64° को पक्षांतर करने पर"), ("", "116" + DEG, "180 − 64 = 116"))
s += kh("चरण 2: " + m(ang("ZYQ", BLU)) + " और " + m(ang("QYP", BLU)) + " ज्ञात करना")
s += num(2, ax("कोण समद्विभाजक", "समद्विभाजक किरण कोण को दो बराबर भागों में बाँटती है।"))
s += chain((ang("ZYQ", BLU), ang("QYP", BLU), "YQ, ∠ZYP को समद्विभाजित करती है"),
           ("", "\\dfrac{1}{2} \\times \\angle ZYP", "बराबर आधे भाग"),
           ("", "\\dfrac{1}{2} \\times 116" + DEG, "∠ZYP = 116° रखने पर"),
           ("", dg(58, BLU), "116 ÷ 2 = 58"))
s += kh("चरण 3: " + m(ang("XYQ", GRN)) + " ज्ञात करना")
s += chain((ang("XYQ", GRN), ang("XYZ", RED) + " + " + ang("ZYQ", BLU), "किरण YZ, ∠XYQ के अंदर है"),
           ("", dg(64, RED) + " + " + dg(58, BLU), "मान रखने पर"),
           ("", dg(122, GRN), "64 + 58 = 122"))
s += kh("चरण 4: प्रतिवर्ती " + m(ang("QYP", PUR)) + " ज्ञात करना")
s += num(3, REFLEX)
s += chain(("\\text{प्रतिवर्ती} " + ang("QYP", PUR), "360^\\circ - " + ang("QYP", BLU), "प्रतिवर्ती कोण = 360° − कोण"),
           ("", "360^\\circ - " + dg(58, BLU), "∠QYP = 58° रखने पर"),
           ("", dg(302, PUR), "360 − 58 = 302"))
s += ans("(i) " + m(ang("XYQ", GRN) + " = " + dg(122, GRN)) + " (ii) प्रतिवर्ती " + m(ang("QYP", PUR) + " = " + dg(302, PUR)))
E1.append(("यह दिया है कि " + m("\\angle XYZ = 64^\\circ") + " है और " + m("XY") + " को बिंदु " + m("P") + " तक बढ़ाया गया है। दी हुई सूचना से एक आकृति खींचिए। यदि किरण "
           + m("YQ") + ", " + m("\\angle ZYP") + " को समद्विभाजित करती है, तो " + m("\\angle XYQ") + " और प्रतिवर्ती " + m("\\angle QYP") + " के मान ज्ञात कीजिए।", s))

# =====================================================================
# Exercise 6.2
# =====================================================================
E2 = []

# ---------- Q1 (आकृति 6.23) ----------
k21 = 180 / (3 + 7)
y21, z21 = 3 * k21, 7 * k21
x21 = z21
assert (k21, y21, z21, x21) == (18, 54, 126, 126)
T21 = 180 - y21   # direction of the upward part of the transversal = 126°


def fig623(sol):
    f = Fig(360, 250)
    ys = (60, 125, 190)
    names = (("A", "B"), ("C", "D"), ("E", "F"))
    xs_ = 55, 305
    for yy, (l, r_) in zip(ys, names):
        f.fline((30, yy), (330, yy))
        f.tick((xs_[0], yy), 0)
        f.tick((xs_[1], yy), 0)
        f.lab((xs_[0], yy), l, 270, 17)
        f.lab((xs_[1], yy), r_, 270, 17)
    if sol:
        for yy in ys:
            f.par((30, yy), (330, yy), 1, INK, .8)
    # transversal through (165, 125) with direction 126° upward
    Pc = (175, 125)
    cot = 1 / math.tan(math.radians(180 - T21))
    pts = [(Pc[0] + (Pc[1] - yy) * (-cot), yy) for yy in ys]   # x moves left going up
    top, bot = f.pol(pts[0], T21, 48), f.pol(pts[2], T21 + 180, 48)
    f.fline(top, bot)
    down = T21 + 180
    f.arc(pts[0], 180, down, 22, RED)
    f.alab(pts[0], 180, down, 36, "x", RED, 15, True)
    f.arc(pts[1], T21, 180, 22, BLU)
    f.alab(pts[1], T21, 180, 37, "y", BLU, 15, True)
    f.arc(pts[2], 0, T21, 22, GRN)
    f.alab(pts[2], 0, T21, 36, "z", GRN, 15, True)
    if sol:
        f.arc(pts[2], T21, 180, 26, BLU, op=.10, dash="4 3")
        f.alab(pts[2], T21, 180, 41, "1", BLU, 14)
    for q_ in pts:
        f.dot(q_)
    return f.svg("आकृति 6.23" if not sol else "हल की आकृति: ∠1, y का संगत कोण (EF पर)")


s = given(m("AB \\parallel CD") + ", " + m("CD \\parallel EF") + "<br>" + m(C(BLU, "y") + " : " + C(GRN, "z") + " = 3 : 7"), m(C(RED, "x")) + " का मान")
s += pair(fig623(False), fig623(True))
s += kh("चरण 1: " + m("AB") + " और " + m("EF") + " का संबंध")
s += num(1, TH66)
s += stmt("AB \\parallel EF", "AB ∥ CD और CD ∥ EF, अर्थात् AB और EF दोनों एक ही रेखा CD के समांतर हैं")
s += kh("चरण 2: " + m(C(BLU, "y")) + " और " + m(C(GRN, "z")) + " का संबंध")
s += p("EF पर, तिर्यक रेखा के ऊपर बाईं ओर का कोण " + m(C(BLU, "\\angle 1")) + " लीजिए (हल की आकृति)।")
s += num(2, CORR)
s += chain((C(BLU, "\\angle 1"), C(BLU, "y"), "CD ∥ EF, ∠1 और y संगत कोण हैं"))
s += num(3, LINEAR)
s += chain((C(BLU, "\\angle 1") + " + " + C(GRN, "z"), "180" + DEG, "तिर्यक रेखा का भाग रेखा EF पर खड़ा है (रैखिक युग्म)"),
           (C(BLU, "y") + " + " + C(GRN, "z"), "180" + DEG, "∠1 = y रखने पर"))
s += kh("चरण 3: अनुपात से " + m(C(BLU, "y")) + " और " + m(C(GRN, "z")))
s += p(m(C(BLU, "y") + " : " + C(GRN, "z") + " = 3 : 7") + " है, इसलिए माना " + m(C(BLU, "y") + " = 3k") + " और " + m(C(GRN, "z") + " = 7k") + "।")
s += chain((C(BLU, "3k") + " + " + C(GRN, "7k"), "180" + DEG, "y = 3k, z = 7k रखने पर"), ("10k", "180" + DEG, "3k + 7k = 10k"))
s += chain(("k", "\\dfrac{180^\\circ}{10}", "10 को पक्षांतर करने पर (गुणा → भाग)"), ("", "18" + DEG, "180 ÷ 10 = 18"))
s += chain((C(BLU, "y"), "3 \\times 18" + DEG, "y = 3k, k = 18°"), ("", dg(54, BLU), "3 × 18 = 54"))
s += chain((C(GRN, "z"), "7 \\times 18" + DEG, "z = 7k, k = 18°"), ("", dg(126, GRN), "7 × 18 = 126"))
s += kh("चरण 4: " + m(C(RED, "x")) + " ज्ञात करना")
s += num(4, ALT)
s += chain((C(RED, "x"), C(GRN, "z"), "AB ∥ EF (चरण 1), x और z एकांतर अंतः कोण हैं"),
           ("", dg(126, RED), "z = 126°"))
s += ans(m(C(RED, "x") + " = " + dg(126, RED)))
E2.append(("आकृति 6.23 में, यदि " + m("AB \\parallel CD") + ", " + m("CD \\parallel EF") + " और " + m("y : z = 3 : 7") + " है, तो " + m("x") + " का मान ज्ञात कीजिए।", s))

# ---------- Q2 (आकृति 6.24) ----------
GED = 126
AGE, GEF, FGE = GED, GED - 90, 180 - GED
assert (AGE, GEF, FGE) == (126, 36, 54)


def fig624(sol):
    f = Fig(360, 230)
    yT, yB = 55, 185
    E = (225, yB)
    F = (225, yT)
    G = (E[0] - (yB - yT) / math.tan(math.radians(180 - GED)), yT)
    f.fline((25, yT), (335, yT))
    f.fline((25, yB), (335, yB))
    f.tick((48, yT), 0)
    f.tick((312, yT), 0)
    f.tick((48, yB), 0)
    f.tick((312, yB), 0)
    f.line(G, E)
    f.line(F, E)
    f.right(E, 0, 13)
    if sol:
        f.par((25, yT), (335, yT), 1, INK, .8)
        f.par((25, yB), (335, yB), 1, INK, .8)
        f.arc(E, 0, GED, 22, ORG)
        f.text(E[0] + 26, E[1] - 30, "126°", ORG, 12)
        f.arc(E, 90, GED, 38, GRN)
        f.alab(E, 90, GED, 54, "36°", GRN, 12)
        f.arc(G, 180, GED + 180, 22, RED)
        f.alab(G, 180, GED + 180, 38, "126°", RED, 12)
        f.arc(G, GED + 180, 360, 26, BLU)
        f.alab(G, GED + 180, 360, 44, "54°", BLU, 12)
    for pnt, t, d in ((G, "G", 90), (F, "F", 90), (E, "E", 270)):
        f.dot(pnt)
        f.lab(pnt, t, d, 17)
    f.lab((48, yT), "A", 90, 17)
    f.lab((312, yT), "B", 90, 17)
    f.lab((48, yB), "C", 270, 17)
    f.lab((312, yB), "D", 270, 17)
    return f.svg("आकृति 6.24" if not sol else "हल की आकृति: ∠GED नारंगी, ∠AGE लाल, ∠GEF हरा, ∠FGE नीला")


s = given(m("AB \\parallel CD") + "<br>" + m("EF \\perp CD") + "<br>" + m(ang("GED", ORG) + " = " + dg(126, ORG)),
          "(i) " + m(ang("AGE", RED)) + "<br>(ii) " + m(ang("GEF", GRN)) + "<br>(iii) " + m(ang("FGE", BLU)))
s += pair(fig624(False), fig624(True))
s += kh("चरण 1: " + m(ang("AGE", RED)))
s += num(1, ALT)
s += chain((ang("AGE", RED), ang("GED", ORG), "AB ∥ CD, तिर्यक रेखा GE; ∠AGE और ∠GED एकांतर अंतः कोण हैं"),
           ("", dg(126, RED), "∠GED = 126° दिया है"))
s += kh("चरण 2: " + m(ang("GEF", GRN)))
s += num(2, ax("लम्ब", m("EF \\perp CD") + " है, इसलिए " + m("\\angle FED = 90^\\circ") + "।"))
s += chain((ang("GEF", GRN) + " + \\angle FED", ang("GED", ORG), "किरण EF, ∠GED के अंदर है"),
           (ang("GEF", GRN) + " + 90" + DEG, dg(126, ORG), "∠FED = 90°, ∠GED = 126° रखने पर"))
s += chain((ang("GEF", GRN), dg(126, ORG) + " - 90" + DEG, "+90° को पक्षांतर करने पर"), ("", dg(36, GRN), "126 − 90 = 36"))
s += kh("चरण 3: " + m(ang("FGE", BLU)))
s += num(3, LINEAR)
s += chain((ang("AGE", RED) + " + " + ang("FGE", BLU), "180" + DEG, "किरण GE रेखा AB पर खड़ी है (रैखिक युग्म)"),
           (dg(126, RED) + " + " + ang("FGE", BLU), "180" + DEG, "∠AGE = 126° रखने पर"))
s += chain((ang("FGE", BLU), "180^\\circ - " + dg(126, RED), "+126° को पक्षांतर करने पर"), ("", dg(54, BLU), "180 − 126 = 54"))
s += ans("(i) " + m(ang("AGE", RED) + " = " + dg(126, RED)) + " (ii) " + m(ang("GEF", GRN) + " = " + dg(36, GRN)) + " (iii) " + m(ang("FGE", BLU) + " = " + dg(54, BLU)))
E2.append(("आकृति 6.24 में, यदि " + m("AB \\parallel CD") + ", " + m("EF \\perp CD") + " और " + m("\\angle GED = 126^\\circ") + " है, तो "
           + m("\\angle AGE") + ", " + m("\\angle GEF") + " और " + m("\\angle FGE") + " ज्ञात कीजिए।", s))

# ---------- Q3 (आकृति 6.25) ----------
PQR3, RST3 = 110, 130
QRA3 = 180 - PQR3
SRB3 = 180 - RST3
QRS3 = 180 - QRA3 - SRB3
dQR = 180 + PQR3          # direction Q→R = 290°
dRS = 360 - RST3 - 180    # direction R→S = 50°
assert (QRA3, SRB3, QRS3) == (70, 50, 60)
assert (dQR - 180) - dRS == QRS3   # angle at R between RQ (110°) and RS (50°)


def fig625(sol):
    f = Fig(360, 220)
    Q = (110, 85)
    R = f.pol(Q, dQR, 95)
    S = f.pol(R, dRS, (R[1] - 52) / math.sin(math.radians(dRS)))
    f.line(Q, (20, Q[1]), INK, 2.2, False, True)
    f.line(S, (340, S[1]), INK, 2.2, False, True)
    f.line(Q, R)
    f.line(R, S)
    f.tick((48, Q[1]), 0)
    f.tick((308, S[1]), 0)
    f.arc(Q, 180, dQR, 20, RED)
    f.alab(Q, 180, dQR, 38, "110°", RED, 13)
    f.arc(S, dRS + 180, 360, 20, BLU)
    f.alab(S, dRS + 180, 360, 38, "130°", BLU, 13)
    if sol:
        f.line((22, R[1]), (338, R[1]), PUR, 1.8, True, True, "7 5")
        f.par((20, Q[1]), Q, 1, INK, .55)
        f.par(S, (340, S[1]), 1, INK, .5)
        f.par((22, R[1]), (338, R[1]), 1, PUR, .82)
        f.lab((30, R[1]), "A", 90, 14, PUR, 15)
        f.lab((330, R[1]), "B", 90, 14, PUR, 15)
        f.arc(R, dQR - 180, 180, 22, ORG)
        f.alab(R, dQR - 180, 180, 38, "70°", ORG, 12)
        f.arc(R, dRS, dQR - 180, 34, GRN)
        f.alab(R, dRS, dQR - 180, 50, "60°", GRN, 12)
        f.arc(R, 0, dRS, 22, TEA)
        f.alab(R, 0, dRS, 38, "50°", TEA, 12)
    for pnt, t, d in ((Q, "Q", 70), (R, "R", 270), (S, "S", 110)):
        f.dot(pnt)
        f.lab(pnt, t, d, 16)
    f.lab((48, Q[1]), "P", 90, 16)
    f.lab((308, S[1]), "T", 90, 16)
    return f.svg("आकृति 6.25" if not sol else "हल की आकृति: R से होकर AB ∥ ST (बैंगनी बिंदुदार)")


s = given(m("PQ \\parallel ST") + "<br>" + m(ang("PQR", RED) + " = " + dg(110, RED)) + "<br>" + m(ang("RST", BLU) + " = " + dg(130, BLU)),
          m(ang("QRS", GRN)))
s += pair(fig625(False), fig625(True))
s += p("<b>रचना:</b> बिंदु " + m("R") + " से होकर " + m("ST") + " के समांतर एक रेखा " + m("AB") + " खींचिए (संकेत के अनुसार)।")
s += kh("चरण 1: " + m("AB \\parallel PQ"))
s += num(1, TH66)
s += stmt("AB \\parallel PQ", "AB ∥ ST (रचना) और PQ ∥ ST (दिया है); दोनों एक ही रेखा ST के समांतर हैं")
s += kh("चरण 2: " + m(ang("QRA", ORG)))
s += num(2, INT)
s += chain((ang("PQR", RED) + " + " + ang("QRA", ORG), "180" + DEG, "PQ ∥ AB, तिर्यक रेखा QR के एक ही ओर (बाईं ओर) के अंतः कोण"),
           (dg(110, RED) + " + " + ang("QRA", ORG), "180" + DEG, "∠PQR = 110° रखने पर"))
s += chain((ang("QRA", ORG), "180^\\circ - " + dg(110, RED), "+110° को पक्षांतर करने पर"), ("", dg(70, ORG), "180 − 110 = 70"))
s += kh("चरण 3: " + m(ang("SRB", TEA)))
s += chain((ang("RST", BLU) + " + " + ang("SRB", TEA), "180" + DEG, "ST ∥ AB, तिर्यक रेखा RS के एक ही ओर (दाईं ओर) के अंतः कोण — गुण (2)"),
           (dg(130, BLU) + " + " + ang("SRB", TEA), "180" + DEG, "∠RST = 130° रखने पर"))
s += chain((ang("SRB", TEA), "180^\\circ - " + dg(130, BLU), "+130° को पक्षांतर करने पर"), ("", dg(50, TEA), "180 − 130 = 50"))
s += kh("चरण 4: " + m(ang("QRS", GRN)))
s += num(3, ax("रेखा पर एक बिंदु के कोण", "रेखा " + m("AB") + " पर बिंदु " + m("R") + " के एक ओर बने सभी आसन्न कोणों का योग " + m("180^\\circ") + " होता है (रैखिक युग्म अभिगृहीत से)।"))
s += chain((ang("QRA", ORG) + " + " + ang("QRS", GRN) + " + " + ang("SRB", TEA), "180" + DEG, "AB एक रेखा है"),
           (dg(70, ORG) + " + " + ang("QRS", GRN) + " + " + dg(50, TEA), "180" + DEG, "मान रखने पर"),
           ("120^\\circ + " + ang("QRS", GRN), "180" + DEG, "70 + 50 = 120"))
s += chain((ang("QRS", GRN), "180^\\circ - 120^\\circ", "+120° को पक्षांतर करने पर"), ("", dg(60, GRN), "180 − 120 = 60"))
s += ans(m(ang("QRS", GRN) + " = " + dg(60, GRN)))
E2.append(("आकृति 6.25 में, यदि " + m("PQ \\parallel ST") + ", " + m("\\angle PQR = 110^\\circ") + " और " + m("\\angle RST = 130^\\circ") + " है, तो "
           + m("\\angle QRS") + " ज्ञात कीजिए।<br>[<b>संकेत:</b> बिंदु " + m("R") + " से होकर " + m("ST") + " के समांतर एक रेखा खींचिए।]", s))

# ---------- Q4 (आकृति 6.26) ----------
APQ4, PRD4 = 50, 127
x4b = APQ4
APR4 = PRD4
y4b = APR4 - APQ4
assert (x4b, y4b) == (50, 77)
dPQ, dPR = 180 + APQ4, 180 + APR4   # 230°, 307°


def fig626(sol):
    f = Fig(360, 220)
    yT, yB = 50, 175
    P = (175, yT)
    Q = f.pol(P, dPQ, (yB - yT) / math.sin(math.radians(APQ4)))
    R = f.pol(P, dPR, (yB - yT) / math.sin(math.radians(180 - APR4)))
    f.fline((22, yT), (338, yT))
    f.fline((22, yB), (338, yB))
    for xx in (45, 315):
        f.tick((xx, yT), 0)
        f.tick((xx, yB), 0)
    f.line(P, Q)
    f.line(P, R)
    f.arc(P, 180, dPQ, 22, BLU)
    f.alab(P, 180, dPQ, 40, "50°", BLU, 13)
    f.arc(P, dPQ, dPR, 26, GRN)
    f.alab(P, dPQ, dPR, 42, "y", GRN, 15, True)
    f.arc(Q, 0, dPQ - 180, 24, RED)
    f.alab(Q, 0, dPQ - 180, 40, "x", RED, 15, True)
    f.arc(R, 0, dPR - 180, 20, ORG)
    f.alab(R, 0, dPR - 180, 38, "127°", ORG, 13)
    if sol:
        f.par((22, yT), (338, yT), 1, INK, .62)
        f.par((22, yB), (338, yB), 1, INK, .62)
        f.arc(P, 180, dPR, 50, ORG, fill=False, dash="5 4", w=1.8)
        f.lab(P, "∠APR", 268, 72, ORG, 11)
    for pnt, t, d in ((P, "P", 90), (Q, "Q", 270), (R, "R", 270)):
        f.dot(pnt)
        f.lab(pnt, t, d, 17)
    f.lab((45, yT), "A", 90, 17)
    f.lab((315, yT), "B", 90, 17)
    f.lab((45, yB), "C", 270, 17)
    f.lab((315, yB), "D", 270, 17)
    return f.svg("आकृति 6.26" if not sol else "हल की आकृति: बिंदुदार नारंगी चाप = ∠APR (= ∠PRD, एकांतर)")


s = given(m("AB \\parallel CD") + "<br>" + m(ang("APQ", BLU) + " = " + dg(50, BLU)) + "<br>" + m(ang("PRD", ORG) + " = " + dg(127, ORG)),
          m(C(RED, "x")) + " और " + m(C(GRN, "y")))
s += pair(fig626(False), fig626(True))
s += tp("आकृति से: " + m(C(RED, "x") + " = \\angle PQR") + " और " + m(C(GRN, "y") + " = \\angle QPR"))
s += kh("चरण 1: " + m(C(RED, "x")) + " ज्ञात करना")
s += num(1, ALT)
s += chain((C(RED, "x"), ang("APQ", BLU), "AB ∥ CD, तिर्यक रेखा PQ; ∠PQR और ∠APQ एकांतर अंतः कोण हैं"),
           ("", dg(50, RED), "∠APQ = 50° दिया है"))
s += kh("चरण 2: " + m("\\angle APR") + " ज्ञात करना")
s += chain(("\\angle APR", ang("PRD", ORG), "AB ∥ CD, तिर्यक रेखा PR; एकांतर अंतः कोण — गुण (1)"),
           ("", dg(127, ORG), "∠PRD = 127° दिया है"))
s += kh("चरण 3: " + m(C(GRN, "y")) + " ज्ञात करना")
s += chain((ang("APQ", BLU) + " + " + C(GRN, "y"), "\\angle APR", "किरण PQ, ∠APR के अंदर है: ∠APQ + ∠QPR = ∠APR"),
           (dg(50, BLU) + " + " + C(GRN, "y"), dg(127, ORG), "मान रखने पर"))
s += chain((C(GRN, "y"), dg(127, ORG) + " - " + dg(50, BLU), "+50° को पक्षांतर करने पर"), ("", dg(77, GRN), "127 − 50 = 77"))
s += ans("(i) " + m(C(RED, "x") + " = " + dg(50, RED)) + " (ii) " + m(C(GRN, "y") + " = " + dg(77, GRN)))
E2.append(("आकृति 6.26 में, यदि " + m("AB \\parallel CD") + ", " + m("\\angle APQ = 50^\\circ") + " और " + m("\\angle PRD = 127^\\circ") + " है, तो "
           + m("x") + " और " + m("y") + " ज्ञात कीजिए।", s))

# ---------- Q5 (आकृति 6.27) ----------
i5 = 36                   # angle of incidence used for the drawing (any value works)
ABC5, BCD5 = 2 * i5, 2 * i5
assert ABC5 == BCD5


def fig627(sol):
    f = Fig(360, 240)
    yT, yB = 50, 190
    B = (120, yT)
    C_ = (B[0] + (yB - yT) * math.tan(math.radians(i5)), yB)
    A_ = f.pol(B, 270 - i5, 85)
    D_ = f.pol(C_, 90 - i5, 90)
    f.fline((22, yT), (338, yT))
    f.fline((22, yB), (338, yB))
    f.hatch((30, yT), (330, yT), -1, INK)
    f.hatch((30, yB), (330, yB), 1, INK)
    for xx in (45, 315):
        f.tick((xx, yT), 0)
        f.tick((xx, yB), 0)
    f.line(A_, B)
    f.mid_arrow(A_, B)
    f.line(B, C_)
    f.mid_arrow(B, C_)
    f.line(C_, D_)
    f.mid_arrow(C_, D_, at=.6)
    if sol:
        M = (B[0], yT + 70)
        N = (C_[0], yB - 70)
        f.line(B, M, PUR, 1.8, dash="6 4")
        f.line(C_, N, PUR, 1.8, dash="6 4")
        f.arc(B, 270 - i5, 270, 30, RED)
        f.arc(B, 270, 270 + i5, 30, ORG, n=2)
        f.arc(C_, 90 + 0, 90 + i5, 30, BLU)
        f.arc(C_, 90 - i5, 90, 30, BLU, n=2)
        f.lab(M, "M", 270, 13, PUR, 15)
        f.lab(N, "N", 90, 13, PUR, 15)
        f.alab(B, 270 - i5, 270, 44, "1", RED, 13)
        f.alab(B, 270, 270 + i5, 44, "2", ORG, 13)
        f.alab(C_, 90, 90 + i5, 44, "3", BLU, 13)
        f.alab(C_, 90 - i5, 90, 44, "4", BLU, 13)
    for pnt, t, d in ((A_, "A", 200), (B, "B", 90), (C_, "C", 270), (D_, "D", 20)):
        f.dot(pnt)
        f.lab(pnt, t, d, 17 if t not in "BC" else 21)
    f.lab((45, yT), "P", 90, 21)
    f.lab((315, yT), "Q", 90, 21)
    f.lab((45, yB), "R", 270, 21)
    f.lab((315, yB), "S", 270, 21)
    return f.svg("आकृति 6.27" if not sol else "हल की आकृति: BM और CN अभिलंब (बैंगनी बिंदुदार); ∠1 = ∠2, ∠3 = ∠4")


def fig627b():
    f = Fig(360, 240)
    yT, yB = 50, 190
    B = (120, yT)
    C_ = (B[0] + (yB - yT) * math.tan(math.radians(i5)), yB)
    A_ = f.pol(B, 270 - i5, 85)
    D_ = f.pol(C_, 90 - i5, 90)
    f.line((22, yT), (338, yT), GRID, 1.6)
    f.line((22, yB), (338, yB), GRID, 1.6)
    # extend AB and CD as dashed lines to show they are parallel
    f.line(f.pol(B, 90 - i5, 40), f.pol(B, 270 - i5, 150), RED, 1.4, dash="5 5")
    f.line(f.pol(C_, 270 - i5, 40), f.pol(C_, 90 - i5, 150), RED, 1.4, dash="5 5")
    f.line(A_, B, RED, 2.6)
    f.line(B, C_, INK, 2.2)
    f.line(C_, D_, RED, 2.6)
    f.arc(B, 270 - i5, 270 + i5, 26, GRN)
    f.alab(B, 270 - i5, 270 + i5, 44, "∠ABC", GRN, 12)
    f.arc(C_, 90 - i5, 90 + i5, 26, GRN)
    f.alab(C_, 90 - i5, 90 + i5, 44, "∠BCD", GRN, 12)
    f.par(A_, B, 1, RED, .5)
    f.par(C_, D_, 1, RED, .45)
    for pnt, t, d in ((A_, "A", 200), (B, "B", 90), (C_, "C", 270), (D_, "D", 20)):
        f.dot(pnt)
        f.lab(pnt, t, d, 17)
    return f.svg("एकांतर कोण ∠ABC = ∠BCD (हरा) ⇒ AB ∥ CD (लाल)")


s = given("दर्पण " + m("PQ \\parallel RS") + "<br>आपतन किरण " + m("AB") + ", परावर्तित किरण " + m("BC") + ", फिर परावर्तित किरण " + m("CD"),
          "सिद्ध करना है: " + m("AB \\parallel CD"))
s += pair(fig627(False), fig627(True))
s += p("<b>रचना:</b> बिंदु " + m("B") + " पर दर्पण " + m("PQ") + " का अभिलंब " + m("BM") + " और बिंदु " + m("C") + " पर दर्पण " + m("RS") + " का अभिलंब " + m("CN") + " खींचिए।")
s += tp("आकृति में: " + m(C(RED, "\\angle 1") + " = \\angle ABM") + " (आपतन कोण), " + m(C(ORG, "\\angle 2") + " = \\angle MBC") + " (परावर्तन कोण), "
        + m(C(BLU, "\\angle 3") + " = \\angle BCN") + " (आपतन कोण), " + m(C(BLU, "\\angle 4") + " = \\angle NCD") + " (परावर्तन कोण)")
s += kh("उपपत्ति (कथन और कारण):")
s += num(1, CORR_C)
s += stmt("BM \\parallel CN", "BM ⊥ PQ और PQ ∥ RS, इसलिए BM ⊥ RS भी (संगत कोण 90°); CN ⊥ RS; RS के साथ दोनों के संगत कोण 90° = 90° हैं")
s += num(2, ALT)
s += chain((C(ORG, "\\angle 2"), C(BLU, "\\angle 3") + " \\qquad \\ldots(1)", "BM ∥ CN, तिर्यक रेखा BC; ∠MBC और ∠BCN एकांतर अंतः कोण हैं"))
s += num(3, ax("परावर्तन का नियम", "आपतन कोण = परावर्तन कोण (दोनों अभिलंब से मापे जाते हैं)।"))
s += chain((C(RED, "\\angle 1"), C(ORG, "\\angle 2") + " \\qquad \\ldots(2)", "बिंदु B पर परावर्तन"),
           (C(BLU, "\\angle 4"), C(BLU, "\\angle 3") + " \\qquad \\ldots(3)", "बिंदु C पर परावर्तन"))
s += chain(("\\angle ABC", C(RED, "\\angle 1") + " + " + C(ORG, "\\angle 2"), "किरण BM, ∠ABC के अंदर है"),
           ("", C(ORG, "\\angle 2") + " + " + C(ORG, "\\angle 2"), "(2) से ∠1 = ∠2 रखने पर"),
           ("", "2" + C(ORG, "\\angle 2") + " \\qquad \\ldots(4)", "∠2 + ∠2 = 2∠2"))
s += chain(("\\angle BCD", C(BLU, "\\angle 3") + " + " + C(BLU, "\\angle 4"), "किरण CN, ∠BCD के अंदर है"),
           ("", C(BLU, "\\angle 3") + " + " + C(BLU, "\\angle 3"), "(3) से ∠4 = ∠3 रखने पर"),
           ("", "2" + C(BLU, "\\angle 3"), "∠3 + ∠3 = 2∠3"),
           ("", "2" + C(ORG, "\\angle 2") + " \\qquad \\ldots(5)", "(1) से ∠3 = ∠2 रखने पर"))
s += chain(("\\angle ABC", "\\angle BCD", "(4) और (5) से, दोनों 2∠2 के बराबर हैं"))
s += fig627b()
s += num(4, ALT_C)
s += stmt("AB \\parallel CD", "तिर्यक रेखा BC, रेखाओं AB और CD के साथ एकांतर अंतः कोण ∠ABC और ∠BCD बनाती है और ये बराबर हैं")
s += tp("जाँच (आकृति में आपतन कोण " + m(f"{i5}^\\circ") + " लिया है): " + m(f"\\angle ABC = 2 \\times {i5}^\\circ = {ABC5}^\\circ") + " और "
        + m(f"\\angle BCD = {BCD5}^\\circ") + " ✔")
s += ans(m("AB \\parallel CD") + " सिद्ध हुआ।")
E2.append(("आकृति 6.27 में, " + m("PQ") + " और " + m("RS") + " दो दर्पण हैं जो एक दूसरे के समांतर रखे गए हैं। एक आपतन किरण (incident ray) " + m("AB")
           + ", दर्पण " + m("PQ") + " से " + m("B") + " पर टकराती है और परावर्तित किरण (reflected ray) पथ " + m("BC") + " पर चलकर दर्पण " + m("RS")
           + " से " + m("C") + " पर टकराती है तथा पुनः " + m("CD") + " के अनुदिश परावर्तित हो जाती है। सिद्ध कीजिए कि " + m("AB \\parallel CD") + " है।", s))

check_tex(E1)
check_tex(E2)
page(BASE, 6, CH, "exercise-6-1", "प्रश्नावली 6.1", f"कक्षा 9 गणित · अध्याय 6: {CH} · {len(E1)} प्रश्न", E1,
     ("/hi/class-09/maths/chapter-05/exercise-5-1/", "प्रश्नावली 5.1"), (BASE + "exercise-6-2/", "प्रश्नावली 6.2"), css=CSS + EXTRA_CSS, boards=BOARDS9)
page(BASE, 6, CH, "exercise-6-2", "प्रश्नावली 6.2", f"कक्षा 9 गणित · अध्याय 6: {CH} · {len(E2)} प्रश्न", E2,
     (BASE + "exercise-6-1/", "प्रश्नावली 6.1"), ("/hi/class-09/maths/chapter-07/exercise-7-1/", "प्रश्नावली 7.1"), css=CSS + EXTRA_CSS, boards=BOARDS9)
print("ok")
