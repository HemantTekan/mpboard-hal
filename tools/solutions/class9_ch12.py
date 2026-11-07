#!/usr/bin/env python3
"""Class 9 Maths, Chapter 12 (सांख्यिकी): Exercise 12.1, Hindi medium.
Rationalised book (2023-24 onward; NCERT iemh112 / ihmh112 'Rationalised Textbooks 2022-23', reprint 2025-26) = old chapter 14:
  collection / presentation of data, measures of central tendency and old प्रश्नावली 14.1, 14.2, 14.4 removed;
  the chapter now has only 12.1 'आंकड़ों का आलेखीय निरूपण' and प्रश्नावली 12.1 = old 14.3 (9 Q), numbers and values unchanged.
  The exercise questions have no figures of their own.
Question text copied from NCERT Hindi PDF ihmh112 (rationalised Ganit, reprint 2025-26); checked against old ihmh114 (2020-21).
  Note: the Hindi book prints no hint in Q4 (the English book has "[Hint: First make the class intervals continuous]");
  the Hindi text is kept as printed, the classes are still made continuous in the solution.
User rules: ज्ञात है / ज्ञात करना है first; one '=' per line; no step skipped; formula boxes where a rule is used;
tables for every step (heights, continuous classes, class marks, adjusted frequencies); graphs to scale on a graph-paper
grid with the scale stated, axis titles and a kink when an axis does not start at 0; the same colour in the table and the
graph; units everywhere; no जाँच boxes. Answers are checked privately with asserts.
Run from repo root: python3 tools/solutions/class9_ch12.py
"""
import sys, pathlib, re, zlib
from fractions import Fraction as F
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from common import *  # noqa
from mixed_cells import *  # noqa

BASE = "/hi/class-09/maths/chapter-12/"
CH = "सांख्यिकी"
BOARDS12 = "यह हल <b>MP Board (MPBSE)</b> कक्षा 9 गणित की पाठ्यपुस्तक के अध्याय 12 ‘सांख्यिकी’ के अनुसार है।"
EXTRA_CSS = """
.fig{margin:10px 0;text-align:center}.fig svg{width:100%;height:auto;border:1px solid #cfdcf0;border-radius:10px;background:#fff}
.fig .cap{font-size:.85em;color:#5a6275;margin-top:4px}
.scale{display:inline-block;background:#fffbea;border:1px solid #f1d27a;border-radius:8px;padding:4px 10px;font-size:.88em;margin:8px 0 2px;line-height:1.5;text-align:left}
.kh{font-weight:700;color:#1d3a8a;margin:14px 0 2px}
.tw{overflow-x:auto;-webkit-overflow-scrolling:touch;max-width:100%;margin:8px 0 10px}
.st{border-collapse:collapse;font-variant-numeric:tabular-nums;background:#fff;font-size:15px}
.st th,.st td{border:1px solid #d5dbe8;padding:4px 8px;text-align:center;white-space:nowrap;vertical-align:middle}
.st th{background:var(--l);font-weight:700;line-height:1.35;white-space:normal;min-width:4.2em}
.st th.w,.st td.w{white-space:normal;min-width:5.5em;text-align:left}
.st tr.sum td{font-weight:700;background:#eef2f9}
.st tr.hl td{background:#fff3c4}
.st i.sw{display:inline-block;width:12px;height:12px;border-radius:3px;margin-right:6px;vertical-align:-1px}
.qh .tw{margin:8px 0 4px}.qh .st{font-weight:500;font-size:14.5px}
.qh p.qx{margin:6px 0 0}.qh .sp{display:block;font-weight:500;margin-top:4px}
.st .katex{font-size:1em}
.ans .al{margin:8px 0}
ul.cn{margin:6px 0;padding-left:1.3em}ul.cn li{margin:4px 0}
@media (max-width:560px){.st{font-size:13.5px}.st th,.st td{padding:3px 4px}}
"""

INK = "#1d2433"
RED, BLU, GRN, ORG, PUR, TEA, PNK, BRN = "#d62839", "#1769c2", "#0f8a4c", "#e06a00", "#7c3aed", "#0b8aa8", "#d6336c", "#8d5524"
PAL = [RED, BLU, GRN, ORG, PUR, TEA, PNK, BRN]
ANS = {}


def C(col, t):
    return "\\textcolor{" + col + "}{" + t + "}"


def kh(t):
    return f"<div class='kh'>{t}</div>"


def sw(col):
    return f"<i class='sw' style='background:{col}'></i>"


def tab(head, rows, sums=None, hl=None, wcols=()):
    h = "".join(f"<th{' class=w' if i in wcols else ''}>{c}</th>" for i, c in enumerate(head))
    body = ""
    for k, r in enumerate(rows):
        cls = " class='hl'" if hl is not None and k in (hl if isinstance(hl, (list, tuple, set)) else [hl]) else ""
        body += f"<tr{cls}>" + "".join(f"<td{' class=w' if i in wcols else ''}>{c}</td>" for i, c in enumerate(r)) + "</tr>"
    if sums:
        body += "<tr class='sum'>" + "".join(f"<td>{c}</td>" for c in sums) + "</tr>"
    return f"<div class='tw'><table class='st'><thead><tr>{h}</tr></thead><tbody>{body}</tbody></table></div>"


def al(*rows):
    """Steps inside a table cell: first row 'LHS = RHS', every further row '= ...' (one '=' per row)."""
    out = rows[0] + " &= " + rows[1]
    for r_ in rows[2:]:
        out += " \\\\ &= " + r_
    return m("\\begin{aligned}" + out + "\\end{aligned}")


def nf(x):
    """Number without trailing zeros (exact)."""
    x = F(x)
    if x.denominator == 1:
        return str(x.numerator)
    s = f"{float(x):.6f}".rstrip("0").rstrip(".")
    assert F(s) == x, x
    return s


def check_tex(E):
    for _q, _sol in E:
        for _t in re.findall(r"\\\((.+?)\\\)", _q + _sol):
            assert not re.search(r"[\u0900-\u097F]", _t), ("Devanagari in TeX", _t)


def scale(*lines_):
    return "<div class='scale'><b>पैमाना:</b><br>" + "<br>".join(lines_) + "</div>"


# ---------------- graph paper ----------------
class G:
    """Graph on graph paper. Coordinates in cm (1 cm = P px); origin O at (0, 0)."""

    def __init__(self, xr, yr, P=28, kx=False, ky=False, xt="", yt="", L=50, B=50, T=16, R=24):
        self.xa, self.xb = xr
        self.ya, self.yb = yr
        self.P, self.kx, self.ky, self.xt, self.yt = P, kx, ky, xt, yt
        self.L, self.B, self.T, self.R = L, B, T, R
        self.W = L + (self.xb - self.xa) * P + R
        self.H = T + (self.yb - self.ya) * P + B
        self.bg, self.el, self.top = [], [], []

    def X(self, c):
        return self.L + (c - self.xa) * self.P

    def Y(self, c):
        return self.T + (self.yb - c) * self.P

    def text(self, x, y, t, col=INK, size=11, anchor="middle", bold=False, rot=None, halo=True):
        tr = f" transform='rotate({rot} {x:.1f} {y:.1f})'" if rot is not None else ""
        hl = " stroke='#ffffff' stroke-width='3.5' stroke-linejoin='round' paint-order='stroke'" if halo else ""
        self.top.append(f"<text x='{x:.1f}' y='{y:.1f}' font-size='{size}' font-weight='{700 if bold else 500}' fill='{col}' "
                        f"text-anchor='{anchor}' dominant-baseline='central'{hl}{tr}>{t}</text>")

    def rect(self, x1, x2, h, col, op=.55, label=None, lsize=10.5):
        X1, X2, Y0, Y1 = self.X(x1), self.X(x2), self.Y(0), self.Y(h)
        self.el.append(f"<rect x='{X1:.1f}' y='{Y1:.1f}' width='{X2 - X1:.1f}' height='{Y0 - Y1:.1f}' fill='{col}' fill-opacity='{op}' "
                       f"stroke='{col}' stroke-width='1.6'/>")
        if label is not None:
            self.text((X1 + X2) / 2, Y1 - 8, label, col, lsize, bold=True)

    def poly(self, pts, col, w=2.2, dash=None, dots=True, names=None, noff=None):
        d = " ".join(f"{self.X(a):.1f},{self.Y(b):.1f}" for a, b in pts)
        da = f" stroke-dasharray='{dash}'" if dash else ""
        self.el.append(f"<polyline points='{d}' fill='none' stroke='{col}' stroke-width='{w}' stroke-linejoin='round'{da}/>")
        if dots:
            for k, (a, b) in enumerate(pts):
                self.top.insert(0, f"<circle cx='{self.X(a):.1f}' cy='{self.Y(b):.1f}' r='3.2' fill='{col}'/>")
        if names:
            for k, ((a, b), nm) in enumerate(zip(pts, names)):
                dx, dy = (noff[k] if noff else (0, -11))
                self.text(self.X(a) + dx, self.Y(b) + dy, nm, col, 11, bold=True)

    def line(self, p, q, col, w=1.6, dash=None):
        da = f" stroke-dasharray='{dash}'" if dash else ""
        self.el.append(f"<line x1='{self.X(p[0]):.1f}' y1='{self.Y(p[1]):.1f}' x2='{self.X(q[0]):.1f}' y2='{self.Y(q[1]):.1f}' "
                       f"stroke='{col}' stroke-width='{w}'{da}/>")

    def svg(self, cap, xticks=(), yticks=(), xlab_dy=13, olab=None):
        P, g = self.P, []
        x0, x1, y0, y1 = self.X(self.xa), self.X(self.xb), self.Y(self.ya), self.Y(self.yb)
        g.append(f"<rect x='{x0:.1f}' y='{y1:.1f}' width='{x1 - x0:.1f}' height='{y0 - y1:.1f}' fill='#fbfdff'/>")
        n = round((self.xb - self.xa) * 5)
        for k in range(n + 1):
            c = self.xa + k / 5
            major = k % 5 == 0
            g.append(f"<line x1='{self.X(c):.1f}' y1='{y0:.1f}' x2='{self.X(c):.1f}' y2='{y1:.1f}' stroke='{'#a9c2e6' if major else '#e2eaf7'}' stroke-width='{0.9 if major else 0.6}'/>")
        n = round((self.yb - self.ya) * 5)
        for k in range(n + 1):
            c = self.ya + k / 5
            major = k % 5 == 0
            g.append(f"<line x1='{x0:.1f}' y1='{self.Y(c):.1f}' x2='{x1:.1f}' y2='{self.Y(c):.1f}' stroke='{'#a9c2e6' if major else '#e2eaf7'}' stroke-width='{0.9 if major else 0.6}'/>")
        # axes (with kinks)
        ox, oy = self.X(0), self.Y(0)
        ax = []
        mk = ("<marker id='{id}' viewBox='0 0 10 10' refX='9' refY='5' markerWidth='9' markerHeight='9' markerUnits='userSpaceOnUse' orient='auto'>"
              "<path d='M0,0 L10,5 L0,10 z' fill='#222'/></marker>")
        mid = f"ar{zlib.crc32(cap.encode()) % 10 ** 6}"
        z = 4.5
        if self.kx:
            a, b = ox + .28 * P, ox + .72 * P
            ax.append(f"<line x1='{x0:.1f}' y1='{oy:.1f}' x2='{a:.1f}' y2='{oy:.1f}' stroke='#222' stroke-width='1.6'/>")
            pts = [(a, oy), (a + (b - a) * .2, oy - z), (a + (b - a) * .45, oy + z), (a + (b - a) * .7, oy - z), (a + (b - a) * .85, oy), (b, oy)]
            ax.append("<polyline points='" + " ".join(f"{u:.1f},{v:.1f}" for u, v in pts) + "' fill='none' stroke='#222' stroke-width='1.6'/>")
            ax.append(f"<line x1='{b:.1f}' y1='{oy:.1f}' x2='{x1 + 12:.1f}' y2='{oy:.1f}' stroke='#222' stroke-width='1.6' marker-end='url(#{mid})'/>")
        else:
            ax.append(f"<line x1='{x0 - (8 if self.xa < 0 else 0):.1f}' y1='{oy:.1f}' x2='{x1 + 12:.1f}' y2='{oy:.1f}' stroke='#222' stroke-width='1.6' marker-end='url(#{mid})'/>")
        if self.ky:
            a, b = oy - .28 * P, oy - .72 * P
            ax.append(f"<line x1='{ox:.1f}' y1='{oy:.1f}' x2='{ox:.1f}' y2='{a:.1f}' stroke='#222' stroke-width='1.6'/>")
            pts = [(ox, a), (ox + z, a + (b - a) * .2), (ox - z, a + (b - a) * .45), (ox + z, a + (b - a) * .7), (ox, a + (b - a) * .85), (ox, b)]
            ax.append("<polyline points='" + " ".join(f"{u:.1f},{v:.1f}" for u, v in pts) + "' fill='none' stroke='#222' stroke-width='1.6'/>")
            ax.append(f"<line x1='{ox:.1f}' y1='{b:.1f}' x2='{ox:.1f}' y2='{y1 - 12:.1f}' stroke='#222' stroke-width='1.6' marker-end='url(#{mid})'/>")
        else:
            ax.append(f"<line x1='{ox:.1f}' y1='{oy:.1f}' x2='{ox:.1f}' y2='{y1 - 12:.1f}' stroke='#222' stroke-width='1.6' marker-end='url(#{mid})'/>")
        t = []
        if olab:
            t.append(f"<text x='{ox + olab[0]:.1f}' y='{oy + olab[1]:.1f}' font-size='11' font-weight='700' text-anchor='{olab[2]}' font-style='italic' fill='#222' stroke='#fff' stroke-width='3' paint-order='stroke'>O</text>")
        elif self.xa < 0:
            t.append(f"<text x='{ox + 3:.1f}' y='{oy + 12:.1f}' font-size='11' font-weight='700' text-anchor='start' font-style='italic' fill='#222'>O</text>")
        else:
            t.append(f"<text x='{ox - 6:.1f}' y='{oy + 12:.1f}' font-size='11' font-weight='700' text-anchor='end' font-style='italic' fill='#222'>O</text>")
        for c, lab in xticks:
            X = self.X(c)
            t.append(f"<line x1='{X:.1f}' y1='{oy - 3:.1f}' x2='{X:.1f}' y2='{oy + 3:.1f}' stroke='#222' stroke-width='1.2'/>")
            if lab != "":
                t.append(f"<text x='{X:.1f}' y='{oy + xlab_dy:.1f}' font-size='10.5' text-anchor='middle' dominant-baseline='central' fill='#222'>{lab}</text>")
        for c, lab in yticks:
            Y = self.Y(c)
            t.append(f"<line x1='{ox - 3:.1f}' y1='{Y:.1f}' x2='{ox + 3:.1f}' y2='{Y:.1f}' stroke='#222' stroke-width='1.2'/>")
            t.append(f"<text x='{ox - 6:.1f}' y='{Y:.1f}' font-size='10.5' text-anchor='end' dominant-baseline='central' fill='#222'>{lab}</text>")
        # axis titles
        cx = (max(self.X(0), x0) + x1) / 2
        t.append(f"<text x='{cx:.1f}' y='{oy + xlab_dy + 19:.1f}' font-size='12' font-weight='700' text-anchor='middle' dominant-baseline='central' fill='#1d3a8a'>{self.xt} →</text>")
        cy = (self.Y(0) + y1) / 2
        t.append(f"<text x='13' y='{cy:.1f}' font-size='12' font-weight='700' text-anchor='middle' dominant-baseline='central' fill='#1d3a8a' "
                 f"transform='rotate(-90 13 {cy:.1f})'>{self.yt} →</text>")
        body = ("<defs>" + mk.format(id=mid) + "</defs>" + "".join(g) + "".join(self.bg) + "".join(self.el) + "".join(ax) + "".join(t) + "".join(self.top))
        return (f"<div class='fig'><svg viewBox='0 0 {self.W:.0f} {self.H:.0f}' role='img' aria-label='{cap}' style='max-width:{max(self.W, 380):.0f}px' "
                f"font-family=\"Noto Sans, 'Noto Sans Devanagari', sans-serif\">{body}</svg><div class='cap'>{cap}</div></div>")


def Qx(intro, table, parts=(), after=""):
    """Question text with its data table; sub-parts (i), (ii)... each on its own line."""
    s = f"{intro}</p>{table}<p class='qx'>"
    if after:
        s += after
    s += "".join(f"<span class='sp'>{x}</span>" for x in parts)
    return s


# formulas used in several questions
F_BAR = formula("छड़ की ऊँचाई", "छड़ की ऊँचाई (cm) = मान ÷ (1 cm से दर्शाया गया मान)")
F_CM = formula("वर्ग-चिह्न", "वर्ग-चिह्न = (उच्च सीमा + निम्न सीमा) ÷ 2 &nbsp;= " + m("\\dfrac{U + L}{2}") + " &nbsp;(U = उच्च सीमा, L = निम्न सीमा)")
F_ADJ = formula("असमान वर्ग-माप वाला आयतचित्र",
                "समायोजित बारंबारता = " + m("\\dfrac{\\text{a}}{\\text{b}}").replace("\\text{a}", "a").replace("\\text{b}", "b")
                + " × बारंबारता, &nbsp;जहाँ a = न्यूनतम वर्ग-माप, b = उस वर्ग की माप।<br>अर्थात् समायोजित बारंबारता = (न्यूनतम वर्ग-माप ÷ उस वर्ग की माप) × बारंबारता")
F_SIZE = formula("वर्ग-माप", "वर्ग-माप = उच्च सीमा − निम्न सीमा")
F_CONT = formula("वर्गों को संतत बनाना",
                 "समायोजन = (अगले वर्ग की निम्न सीमा − पिछले वर्ग की उच्च सीमा) ÷ 2;<br>हर वर्ग की निम्न सीमा में से समायोजन घटाएँ और उच्च सीमा में समायोजन जोड़ें।")
POLY_RULE = formula("बारंबारता बहुभुज", "बिंदु (वर्ग-चिह्न, बारंबारता) अंकित करके रेखाखंडों से मिलाएँ; पहले वर्ग से ठीक पहले और अंतिम वर्ग के ठीक बाद "
                    "शून्य बारंबारता वाले एक-एक काल्पनिक वर्ग के वर्ग-चिह्न भी लें, ताकि बहुभुज x-अक्ष पर बंद हो।")

# =====================================================================
# Exercise 12.1
# =====================================================================
E = []

# ---- Q1 ----
causes = ["जनन स्वास्थ्य अवस्था", "तंत्रिका मनोविकारी अवस्था", "क्षति", "हृदय वाहिका अवस्था", "श्वसन अवस्था", "अन्य कारण"]
rate = [F("31.8"), F("25.4"), F("12.4"), F("4.3"), F("4.1"), F("22.0")]
assert sum(rate) == 100
qtab = tab(["क्र. सं.", "कारण", "महिला मृत्यु दर (%)"], [[f"{k + 1}.", c, "22.0" if k == 5 else nf(v)] for k, (c, v) in enumerate(zip(causes, rate))], wcols=(1,))
s = given("6 कारण और उनकी महिला मृत्यु दर (%) — तालिका में", "(i) आँकड़ों का आलेखीय निरूपण (दंड आलेख)<br>(ii) सबसे बड़ा कारण<br>(iii) उस कारण के दो प्रमुख कारक")
b = p("आँकड़े अलग-अलग कारणों (वर्गों) के हैं, अंतराल नहीं; इसलिए इन्हें <b>दंड आलेख (bar graph)</b> से दिखाएँगे — सभी छड़ें समान चौड़ाई (1 cm) की और उनके बीच समान दूरी (1 cm)।")
b += p("सबसे बड़ा मान 31.8% है, इसलिए y-अक्ष पर पैमाना 1 cm = 5% लेते हैं (35% तक 7 cm)।") + F_BAR
rows = []
for k, (c, v) in enumerate(zip(causes, rate)):
    h = v / 5
    rows.append([f"{sw(PAL[k])}{k + 1}", c, nf(v) + "%", al(nf(v) + "\\div 5", nf(h) + "\\ \\text{cm}")])
b += tab(["छड़", "कारण", "मृत्यु दर", "छड़ की ऊँचाई"], rows, wcols=(1,))
g = G((0, 13), (0, 7.4), P=27, xt="कारण (क्र. सं.)", yt="महिला मृत्यु दर (%)")
for k, v in enumerate(rate):
    g.rect(1 + 2 * k, 2 + 2 * k, float(v / 5), PAL[k], label=nf(v) if k != 5 else "22.0")
b += scale("x-अक्ष पर: हर छड़ की चौड़ाई 1 cm, दो छड़ों के बीच 1 cm", "y-अक्ष पर: 1 cm = 5% (मृत्यु दर)")
b += g.svg("दंड आलेख: कारण के अनुसार महिला मृत्यु दर (छड़ के नीचे क्रमांक, रंग तालिका के अनुसार)",
           xticks=[(1.5 + 2 * k, str(k + 1)) for k in range(6)], yticks=[(k, str(5 * k)) for k in range(1, 8)])
s += part("(i) आलेखीय निरूपण (दंड आलेख)", b)
mx = max(rate)
assert mx == rate[0]
b = p("दंड आलेख में सबसे ऊँची छड़ (" + sw(RED) + "क्र. 1, ऊँचाई 6.36 cm) जनन स्वास्थ्य अवस्था की है, जिसकी मृत्यु दर 31.8% है।")
s += part("(ii) सबसे बड़ा कारण", b)
b = "<ul class='cn'><li><b>गर्भावस्था और प्रसव के समय उचित चिकित्सा देखभाल की कमी:</b> गाँवों और गरीब क्षेत्रों में अस्पताल, प्रशिक्षित डॉक्टर/दाई, नियमित जाँच और टीकाकरण की सुविधा पर्याप्त नहीं है।</li>" \
    "<li><b>कुपोषण और जागरूकता/शिक्षा की कमी:</b> कम उम्र में विवाह, बार-बार गर्भधारण, खून की कमी (एनीमिया) और स्वास्थ्य संबंधी जानकारी के अभाव से जनन स्वास्थ्य बिगड़ता है।</li></ul>"
s += part("(iii) दो प्रमुख कारक", b)
s += ans("(i) ऊपर दंड आलेख बनाया गया है। (ii) <b>जनन स्वास्थ्य अवस्था</b> (31.8%) महिलाओं के खराब स्वास्थ्य और मृत्यु का सबसे बड़ा कारण है। "
         "(iii) गर्भावस्था/प्रसव के समय उचित चिकित्सा सुविधा की कमी, तथा कुपोषण और जागरूकता/शिक्षा की कमी।")
ANS["Q1"] = "bar graph; जनन स्वास्थ्य अवस्था 31.8%"
E.append((Qx("एक संगठन ने पूरे विश्व में 15-44 (वर्षों में) की आयु वाली महिलाओं में बीमारी और मृत्यु के कारणों का पता लगाने के लिए किए गए सर्वेक्षण से निम्नलिखित आंकड़े (% में) प्राप्त किए:",
             qtab, ["(i) ऊपर दी गई सूचनाओं को आलेखीय रूप में निरूपित कीजिए।", "(ii) कौन-सी अवस्था पूरे विश्व की महिलाओं के खराब स्वास्थ्य और मृत्यु का बड़ा कारण है?",
                    "(iii) अपनी अध्यापिका की सहायता से ऐसे दो कारणों का पता लगाने का प्रयास कीजिए जिनकी ऊपर (ii) में मुख्य भूमिका रही हो।"]), s))

# ---- Q2 ----
secs = ["अनुसूचित जाति", "अनुसूचित जनजाति", "गैर अनुसूचित जाति/जनजाति", "पिछड़े जिले", "गैर पिछड़े जिले", "ग्रामीण", "शहरी"]
gv = [940, 970, 920, 950, 920, 930, 910]
qtab = tab(["क्षेत्र", "प्रति हजार लड़कों पर लड़कियों की संख्या"], [[a, v] for a, v in zip(secs, gv)], wcols=(0,))
s = given("7 क्षेत्र और प्रति हजार लड़कों पर लड़कियों की संख्या — तालिका में", "(i) दंड आलेख<br>(ii) आलेख से निष्कर्ष")
b = p("सबसे छोटा मान 910 और सबसे बड़ा 970 है। 0 से 900 तक का भाग खाली रहेगा, इसलिए y-अक्ष पर 0 के बाद <b>टूटा हुआ निशान (kink)</b> लगाकर 900 से अंक लिखते हैं।")
b += p("पैमाना: y-अक्ष पर 1 cm = 10 लड़कियाँ; 900 का चिह्न मूल बिंदु O से 1 cm ऊपर है।")
b += formula("900 के चिह्न से छड़ की ऊँचाई", "ऊँचाई (cm) = (मान − 900) ÷ 10")
rows = []
for k, (a, v) in enumerate(zip(secs, gv)):
    rows.append([f"{sw(PAL[k])}{k + 1}", a, v, al(f"({v}-900)\\div 10", f"{v - 900}\\div 10", nf(F(v - 900, 10)) + "\\ \\text{cm}")])
b += tab(["छड़", "क्षेत्र", "लड़कियाँ", "900 के चिह्न से ऊँचाई"], rows, wcols=(1,))
g = G((0, 11.6), (0, 8.6), P=28, ky=True, xt="क्षेत्र (क्र. सं.)", yt="प्रति हजार लड़कों पर लड़कियाँ")
for k, v in enumerate(gv):
    g.rect(0.8 + 1.5 * k, 1.6 + 1.5 * k, 1 + (v - 900) / 10, PAL[k % 8], label=str(v))
b += scale("x-अक्ष पर: हर छड़ की चौड़ाई 0.8 cm, दो छड़ों के बीच 0.7 cm", "y-अक्ष पर: 1 cm = 10 लड़कियाँ (900 से आरंभ, 0 और 900 के बीच kink)")
b += g.svg("दंड आलेख: प्रति हजार लड़कों पर लड़कियों की संख्या (छड़ के नीचे क्रमांक, रंग तालिका के अनुसार)",
           xticks=[(1.2 + 1.5 * k, str(k + 1)) for k in range(7)], yticks=[(1 + k, str(900 + 10 * k)) for k in range(0, 8)])
s += part("(i) दंड आलेख", b)
assert max(gv) == 970 and min(gv) == 910 and all(v < 1000 for v in gv)
b = "<ul class='cn'>" \
    "<li>हर क्षेत्र में प्रति हजार लड़कों पर लड़कियाँ 1000 से कम हैं, अर्थात् समाज के सभी वर्गों में लड़कियों की संख्या लड़कों से कम है।</li>" \
    f"<li>सबसे ऊँची छड़ {sw(BLU)}<b>अनुसूचित जनजाति</b> (970) की है — वहाँ लिंगानुपात सबसे अच्छा है।</li>" \
    f"<li>सबसे छोटी छड़ {sw(PNK)}<b>शहरी</b> क्षेत्र (910) की है — वहाँ लिंगानुपात सबसे कम है।</li>" \
    "<li>ग्रामीण क्षेत्र (930) शहरी क्षेत्र (910) से आगे है, और पिछड़े जिले (950) गैर पिछड़े जिलों (920) से आगे हैं।</li>" \
    "<li>अनुसूचित जाति (940) और अनुसूचित जनजाति (970) में यह संख्या गैर अनुसूचित जाति/जनजाति (920) से अधिक है।</li>" \
    "<li>अतः लड़कियों के प्रति भेदभाव (जैसे भ्रूण-लिंग जाँच) रोकने और जागरूकता बढ़ाने की आवश्यकता है, विशेषकर शहरी और विकसित क्षेत्रों में।</li></ul>"
s += part("(ii) आलेख से निष्कर्ष", b)
s += ans("(i) ऊपर दंड आलेख बनाया गया है। (ii) सभी क्षेत्रों में लड़कियाँ लड़कों से कम हैं; अनुसूचित जनजाति में सबसे अधिक (970) और शहरी क्षेत्र में सबसे कम (910); "
         "ग्रामीण, पिछड़े जिलों तथा SC/ST वर्गों में स्थिति अपेक्षाकृत बेहतर है।")
ANS["Q2"] = "bar graph kink at 900; ST 970 max, Urban 910 min"
E.append((Qx("भारतीय समाज के विभिन्न क्षेत्रों में प्रति हजार लड़कों पर लड़कियों की (निकटतम दस तक की) संख्या के आंकड़े नीचे दिए गए हैं:",
             qtab, ["(i) ऊपर दी गई सूचनाओं को एक दंड आलेख द्वारा निरूपित कीजिए।", "(ii) कक्षा में चर्चा करके, बताइए कि आप इस आलेख से कौन-कौन से निष्कर्ष निकाल सकते हैं।"]), s))

# ---- Q3 ----
parties = list("ABCDEF")
seats = [75, 55, 37, 29, 10, 37]
qtab = ("<div class='tw'><table class='st'><tbody><tr><th>राजनैतिक पार्टी</th>" + "".join(f"<td>{x}</td>" for x in parties) + "</tr>"
        "<tr><th>जीती गई सीटें</th>" + "".join(f"<td>{x}</td>" for x in seats) + "</tr></tbody></table></div>")
s = given("6 पार्टियाँ A से F और उनकी जीती गई सीटें — तालिका में", "(i) दंड आलेख<br>(ii) अधिकतम सीटें जीतने वाली पार्टी")
b = p("सबसे बड़ा मान 75 सीटें है, इसलिए y-अक्ष पर पैमाना 1 cm = 10 सीटें लेते हैं (80 सीटों तक 8 cm)।") + F_BAR
rows = [[f"{sw(PAL[k])}{x}", v, al(f"{v}\\div 10", nf(F(v, 10)) + "\\ \\text{cm}")] for k, (x, v) in enumerate(zip(parties, seats))]
b += tab(["पार्टी", "जीती गई सीटें", "छड़ की ऊँचाई"], rows)
g = G((0, 13), (0, 8.4), P=27, xt="राजनैतिक पार्टी", yt="जीती गई सीटें")
for k, v in enumerate(seats):
    g.rect(1 + 2 * k, 2 + 2 * k, v / 10, PAL[k], label=str(v))
b += scale("x-अक्ष पर: हर छड़ की चौड़ाई 1 cm, दो छड़ों के बीच 1 cm", "y-अक्ष पर: 1 cm = 10 सीटें")
b += g.svg("दंड आलेख: पार्टियों द्वारा जीती गई सीटें", xticks=[(1.5 + 2 * k, x) for k, x in enumerate(parties)], yticks=[(k, str(10 * k)) for k in range(1, 9)])
s += part("(i) दंड आलेख", b)
assert max(seats) == 75 and seats.index(75) == 0
b = p("सबसे ऊँची छड़ (" + sw(RED) + "7.5 cm) पार्टी A की है, जिसने 75 सीटें जीतीं।")
s += part("(ii) अधिकतम सीटें", b)
s += ans("(i) ऊपर दंड आलेख बनाया गया है। (ii) पार्टी <b>A</b> ने अधिकतम <b>75 सीटें</b> जीतीं।")
ANS["Q3"] = "A, 75 seats"
E.append((Qx("एक राज्य के विधान सभा के चुनाव में विभिन्न राजनैतिक पार्टियों द्वारा जीती गई सीटों के परिणाम नीचे दिए गए हैं:", qtab,
             ["(i) मतदान के परिणामों को निरूपित करने वाला एक दंड आलेख खींचिए।", "(ii) किस राजनैतिक पार्टी ने अधिकतम सीटें जीती हैं?"]), s))


# ---- helpers for continuous classes / class marks ----
def cont_block(cls, freq, fcol, ftitle, unit, gap_pair):
    """Show the adjustment and the continuous-class table; returns (html, new classes)."""
    (u1, l2) = gap_pair
    gap = F(l2 - u1)
    adj = gap / 2
    b = p("दिए गए वर्ग संतत नहीं हैं: एक वर्ग की उच्च सीमा और अगले वर्ग की निम्न सीमा के बीच अंतर है। आयतचित्र/बहुभुज के लिए पहले वर्गों को संतत बनाते हैं।") + F_CONT
    b += lines("\\text{अंतर}", f"{l2}-{u1}", nf(gap))
    b += lines("\\text{समायोजन}", f"\\dfrac{{{nf(gap)}}}{{2}}", nf(adj))
    new, rows = [], []
    for (lo, hi), f in zip(cls, freq):
        a, c = F(lo) - adj, F(hi) + adj
        new.append((a, c))
        rows.append([f"{lo} − {hi}", al(f"{lo}-{nf(adj)}", nf(a)), al(f"{hi}+{nf(adj)}", nf(c)),
                     f"<b style='color:{fcol}'>{f}</b>"])
    for (a, c), (a2, c2) in zip(new, new[1:]):
        assert c == a2
    b += tab(["दिया वर्ग", "नई निम्न सीमा", "नई उच्च सीमा", ftitle], rows)
    return b, new


def cm_rows(cls):
    out = []
    for a, c in cls:
        mk = (F(a) + F(c)) / 2
        A_ = f"({nf(a)})" if F(a) < 0 else nf(a)
        out.append((mk, al(f"\\dfrac{{{nf(c)}+{A_}}}{{2}}", f"\\dfrac{{{nf(F(a) + F(c))}}}{{2}}", nf(mk))))
    return out


# ---- Q4 ----
cls4 = [(118, 126), (127, 135), (136, 144), (145, 153), (154, 162), (163, 171), (172, 180)]
f4 = [3, 5, 9, 12, 5, 4, 2]
assert sum(f4) == 40
qtab = tab(["लंबाई (मिलीमीटर में)", "पत्तियों की संख्या"], [[f"{a} - {c}", f] for (a, c), f in zip(cls4, f4)])
s = given("40 पत्तियों की लंबाई (mm) का बंटन — 7 वर्ग, तालिका में", "(i) आयतचित्र<br>(ii) अन्य उपयुक्त आलेख<br>(iii) क्या 153 mm लंबी पत्तियाँ सबसे अधिक हैं?")
b, new4 = cont_block(cls4, f4, BLU, "पत्तियों की संख्या", "mm", (126, 127))
b += p("अब हर वर्ग-माप = 126.5 − 117.5 = 9 mm (सभी वर्ग समान)। इसलिए आयतों की ऊँचाई सीधे बारंबारता के अनुपात में होगी।")
b += p("x-अक्ष पर 117.5 से आरंभ है (0 से नहीं), इसलिए x-अक्ष पर O के पास kink लगाते हैं। सबसे बड़ी बारंबारता 12 है, इसलिए y-अक्ष पर 1 cm = 2 पत्तियाँ।")
b += formula("आयत की ऊँचाई", "आयत की ऊँचाई (cm) = बारंबारता ÷ 2")
rows = [[f"{nf(a)} − {nf(c)}", f"<b style='color:{BLU}'>{f}</b>", al(f"{f}\\div 2", nf(F(f, 2)) + "\\ \\text{cm}")] for (a, c), f in zip(new4, f4)]
b += tab(["संतत वर्ग (mm)", "पत्तियाँ", "आयत की ऊँचाई"], rows, hl=3)
g = G((0, 8.6), (0, 6.8), P=34, kx=True, xt="लंबाई (mm में)", yt="पत्तियों की संख्या")
for k, f in enumerate(f4):
    g.rect(1 + k, 2 + k, f / 2, BLU, op=.45 if k != 3 else .7, label=str(f))
b += scale("x-अक्ष पर: 1 cm = 9 mm (एक वर्ग-माप), 117.5 से आरंभ (kink)", "y-अक्ष पर: 1 cm = 2 पत्तियाँ")
b += g.svg("आयतचित्र: 40 पत्तियों की लंबाई", xticks=[(1 + k, nf(new4[k][0]) if k < 7 else "") for k in range(7)] + [(8, nf(new4[6][1]))],
           yticks=[(k, str(2 * k)) for k in range(1, 7)])
s += part("(i) आयतचित्र", b)
# (ii) frequency polygon
b = p("हाँ। इन्हीं आँकड़ों को <b>बारंबारता बहुभुज (frequency polygon)</b> से भी दिखाया जा सकता है। आयतचित्र के आयतों की ऊपरी भुजाओं के मध्य-बिंदु (वर्ग-चिह्न) मिलाने से यह बनता है।")
b += F_CM + POLY_RULE
ext4 = [(F("108.5"), F("117.5"))] + new4 + [(F("180.5"), F("189.5"))]
ff4 = [0] + f4 + [0]
names4 = list("ABCDEFGHI")
rows = []
for k, ((a, c), (mk, cell), f) in enumerate(zip(ext4, cm_rows(ext4), ff4)):
    tag = "*" if k in (0, 8) else ""
    rows.append([f"{nf(a)} − {nf(c)}{tag}", f"<span style='color:{RED}'>{cell}</span>", f, f"<b style='color:{RED}'>{names4[k]}</b>({nf(mk)}, {f})"])
b += tab(["वर्ग (mm)", "वर्ग-चिह्न (mm)", "बारंबारता", "बिंदु"], rows) + "<div class='muted' style='margin:-4px 0 8px'>* काल्पनिक वर्ग (बारंबारता 0)</div>"
mk4 = [(F(a) + F(c)) / 2 for a, c in ext4]
assert mk4[1] == 122 and mk4[-1] == 185 and mk4[0] == 113
g = G((0, 10.6), (0, 6.8), P=31, kx=True, xt="लंबाई (mm में)", yt="पत्तियों की संख्या")
for k, f in enumerate(f4):
    g.rect(2 + k, 3 + k, f / 2, BLU, op=.25)
pts = [(1.5 + k, ff4[k] / 2) for k in range(9)]
offs = [(0, -11), (-9, -9), (-9, -9), (-9, -9), (0, -12), (9, -9), (9, -9), (9, -9), (0, -11)]
g.poly(pts, RED, names=names4, noff=offs)
b += scale("x-अक्ष पर: 1 cm = 9 mm, 108.5 से आरंभ (kink)", "y-अक्ष पर: 1 cm = 2 पत्तियाँ")
b += g.svg("आयतचित्र (नीला) पर बना बारंबारता बहुभुज ABCDEFGHI (लाल)",
           xticks=[(1 + k, nf(ext4[k][0])) for k in range(9)] + [(10, nf(ext4[8][1]))], yticks=[(k, str(2 * k)) for k in range(1, 7)])
b += p("A(113, 0) और I(185, 0) काल्पनिक वर्गों 108.5 − 117.5 और 180.5 − 189.5 (बारंबारता 0) के वर्ग-चिह्न हैं।")
s += part("(ii) अन्य उपयुक्त आलेख", b)
b = p("नहीं, यह निष्कर्ष सही नहीं है।")
b += p("सबसे अधिक पत्तियाँ (12) वर्ग <b>145 − 153</b> में हैं, जिसका संतत रूप <b>144.5 mm − 153.5 mm</b> है। इसका अर्थ है कि इन 12 पत्तियों की लंबाई 144.5 mm और 153.5 mm के बीच कुछ भी हो सकती है; "
       "153 तो केवल इस वर्ग की उच्च सीमा है। सारणी से यह पता नहीं चलता कि कितनी पत्तियाँ ठीक 153 mm लंबी हैं।")
s += part("(iii) क्या 153 mm लंबी पत्तियाँ सबसे अधिक हैं?", b)
s += ans("(i) संतत वर्गों 117.5 − 126.5, …, 171.5 − 180.5 पर आयतचित्र ऊपर बनाया गया है। (ii) हाँ, बारंबारता बहुभुज। "
         "(iii) नहीं; अधिकतम पत्तियाँ (12) 144.5 mm − 153.5 mm वर्ग में हैं, उनकी लंबाई ठीक 153 mm होना आवश्यक नहीं।")
ANS["Q4"] = "continuous 117.5-180.5; freq polygon; no (144.5-153.5)"
E.append((Qx("एक पौधे की 40 पत्तियों की लंबाइयाँ एक मिलीमीटर तक शुद्ध मापी गई हैं और प्राप्त आंकड़ों को निम्नलिखित सारणी में निरूपित किया गया है:", qtab,
             ["(i) दिए हुए आंकड़ों को निरूपित करने वाला एक आयतचित्र खींचिए।", "(ii) क्या इन्हीं आंकड़ों को निरूपित करने वाला कोई अन्य उपयुक्त आलेख है?",
              "(iii) क्या यह सही निष्कर्ष है कि 153 मिलीमीटर लम्बाई वाली पत्तियों की संख्या सबसे अधिक है? क्यों?"]), s))

# ---- Q5 ----
cls5 = [(300 + 100 * k, 400 + 100 * k) for k in range(7)]
f5 = [14, 56, 60, 86, 74, 62, 48]
assert sum(f5) == 400
qtab = tab(["जीवन काल (घंटों में)", "लैम्पों की संख्या"], [[f"{a} - {c}", f] for (a, c), f in zip(cls5, f5)])
s = given("400 नियॉन लैम्पों के जीवन काल (घंटे) का बंटन — 7 संतत वर्ग, तालिका में", "(i) आयतचित्र<br>(ii) 700 घंटे से अधिक जीवन काल वाले लैम्प")
b = p("वर्ग पहले से संतत हैं और सबकी माप समान है:") + F_SIZE + lines("\\text{वर्ग-माप}", "400-300", "100\\ \\text{h}")
b += p("x-अक्ष 300 से आरंभ है, इसलिए O के पास kink लगाते हैं; पैमाना 1 cm = 100 घंटे। सबसे बड़ी बारंबारता 86 है, इसलिए y-अक्ष पर 1 cm = 10 लैम्प।")
b += formula("आयत की ऊँचाई", "आयत की ऊँचाई (cm) = बारंबारता ÷ 10")
rows = [[f"{a} − {c}", f"<b style='color:{GRN}'>{f}</b>", al(f"{f}\\div 10", nf(F(f, 10)) + "\\ \\text{cm}")] for (a, c), f in zip(cls5, f5)]
b += tab(["जीवन काल (घंटे)", "लैम्प", "आयत की ऊँचाई"], rows, hl=[4, 5, 6])
g = G((0, 8.6), (0, 9.4), P=30, kx=True, xt="जीवन काल (घंटों में)", yt="लैम्पों की संख्या")
for k, f in enumerate(f5):
    g.rect(1 + k, 2 + k, f / 10, GRN, op=.4 if k < 4 else .7, label=str(f))
b += scale("x-अक्ष पर: 1 cm = 100 घंटे, 300 से आरंभ (kink)", "y-अक्ष पर: 1 cm = 10 लैम्प")
b += g.svg("आयतचित्र: 400 नियॉन लैम्पों का जीवन काल (गहरे आयत: 700 घंटे से अधिक)", xticks=[(1 + k, str(300 + 100 * k)) for k in range(8)],
           yticks=[(k, str(10 * k)) for k in range(1, 10)])
s += part("(i) आयतचित्र", b)
n700 = sum(f5[4:])
assert n700 == 184
b = p("700 घंटे से अधिक जीवन काल वाले वर्ग: 700 − 800, 800 − 900 और 900 − 1000 (आलेख में गहरे हरे आयत)।")
b += lines("\\text{700 घंटे से अधिक जीवन काल वाले लैम्प}", "74+62+48", "136+48", "184")
s += part("(ii) 700 घंटे से अधिक जीवन काल वाले लैम्प", b)
s += ans("(i) आयतचित्र ऊपर बनाया गया है। (ii) <b>184 लैम्पों</b> का जीवन काल 700 घंटे से अधिक है।")
ANS["Q5"] = "184 lamps"
E.append((Qx("नीचे की सारणी में 400 नियॉन लैम्पों के जीवन काल दिए गए हैं:", qtab,
             ["(i) एक आयतचित्र की सहायता से दी हुई सूचनाओं को निरूपित कीजिए।", "(ii) कितने लैम्पों के जीवन काल 700 घंटों से अधिक हैं?"]), s))

# ---- Q6 ----
cls6 = [(10 * k, 10 * k + 10) for k in range(5)]
fA, fB = [3, 9, 17, 12, 9], [5, 19, 15, 10, 1]
assert sum(fA) == 50 and sum(fB) == 50
qtab = ("<div class='tw'><table class='st'><thead><tr><th colspan='2'>सेक्शन A</th><th colspan='2'>सेक्शन B</th></tr>"
        "<tr><th>अंक</th><th>बारंबारता</th><th>अंक</th><th>बारंबारता</th></tr></thead><tbody>"
        + "".join(f"<tr><td>{a} - {c}</td><td>{x}</td><td>{a} - {c}</td><td>{y}</td></tr>" for (a, c), x, y in zip(cls6, fA, fB)) + "</tbody></table></div>")
s = given("दोनों सेक्शनों के अंकों का बंटन (वर्ग 0 − 10, …, 40 − 50)", "एक ही आलेख पर दोनों सेक्शनों के बारंबारता बहुभुज और निष्पादन की तुलना")
b = F_CM
b += kh("उदाहरण: वर्ग 0 − 10 का वर्ग-चिह्न") + lines("\\text{वर्ग-चिह्न}", "\\dfrac{10+0}{2}", "\\dfrac{10}{2}", "5")
b += POLY_RULE
b += p("पहला वर्ग 0 − 10 है, इसलिए उससे पहले का काल्पनिक वर्ग (−10) − 0 है, जिसका वर्ग-चिह्न −5 है। पाठ्यपुस्तक (उदाहरण 4) की तरह x-अक्ष को ऋणात्मक दिशा में बढ़ाकर पहले बिंदु को (−5, 0) से मिलाते हैं; "
       "यह रेखाखंड y-अक्ष को जिस बिंदु पर काटता है, बहुभुज वहीं से आरंभ होता है (अंक ऋणात्मक नहीं हो सकते)। अंतिम वर्ग के बाद काल्पनिक वर्ग 50 − 60 का वर्ग-चिह्न 55 है।")
ext6 = [(-10, 0)] + cls6 + [(50, 60)]
rows = []
for k, ((a, c), (mk, cell)) in enumerate(zip(ext6, cm_rows(ext6))):
    fa = ([0] + fA + [0])[k]
    fb = ([0] + fB + [0])[k]
    tag = "*" if k in (0, 6) else ""
    rows.append([f"{str(a).replace('-', '−')} − {c}{tag}", cell, f"<b style='color:{BLU}'>{fa}</b>", f"<b style='color:{RED}'>{fb}</b>"])
b += tab(["वर्ग (अंक)", "वर्ग-चिह्न", f"{sw(BLU)}सेक्शन A", f"{sw(RED)}सेक्शन B"], rows) + "<div class='muted' style='margin:-4px 0 8px'>* काल्पनिक वर्ग (बारंबारता 0)</div>"
g = G((-1.4, 6.4), (0, 10.4), P=31, xt="अंक", yt="विद्यार्थियों की संख्या", L=52)
pa = [(-0.5, 0)] + [(0.5 + k, fA[k] / 2) for k in range(5)] + [(5.5, 0)]
pb = [(-0.5, 0)] + [(0.5 + k, fB[k] / 2) for k in range(5)] + [(5.5, 0)]
for pp, col in ((pa, BLU), (pb, RED)):
    y0 = pp[1][1] * 0.5  # where (−0.5, 0) → (0.5, y) meets x = 0
    g.line(pp[0], (0, y0), col, 1.6, "4 3")
    g.poly([(0, y0)] + pp[1:], col, dots=False)
    for a_, b_ in pp[1:]:
        g.top.insert(0, f"<circle cx='{g.X(a_):.1f}' cy='{g.Y(b_):.1f}' r='3.3' fill='{col}'/>")
    g.top.insert(0, f"<circle cx='{g.X(-0.5):.1f}' cy='{g.Y(0):.1f}' r='3' fill='#fff' stroke='{col}' stroke-width='1.5'/>")
g.text(g.X(2.5) + 4, g.Y(8.5) - 12, "A", BLU, 12, bold=True)
g.text(g.X(1.5) - 2, g.Y(9.5) - 12, "B", RED, 12, bold=True)
b += scale("x-अक्ष पर: 1 cm = 10 अंक (वर्ग-चिह्न −5, 5, 15, …, 55)", "y-अक्ष पर: 1 cm = 2 विद्यार्थी")
b += g.svg("बारंबारता बहुभुज: सेक्शन A (नीला) और सेक्शन B (लाल); बिंदीदार भाग काल्पनिक वर्ग (−10) − 0 तक",
           xticks=[(k - 0.5, str(10 * k - 5).replace("-", "−")) for k in range(7)],
           yticks=[(k, str(2 * k)) for k in range(1, 11)])
s += part("बारंबारता बहुभुज", b)
hiA, hiB, loA, loB = fA[3] + fA[4], fB[3] + fB[4], fA[0] + fA[1], fB[0] + fB[1]
assert (hiA, hiB, loA, loB) == (21, 11, 12, 24)
b = p("दोनों सेक्शनों में 50-50 विद्यार्थी हैं, इसलिए सीधे तुलना कर सकते हैं।")
b += lines("\\text{सेक्शन A में 30 या अधिक अंक वाले}", "12+9", "21")
b += lines("\\text{सेक्शन B में 30 या अधिक अंक वाले}", "10+1", "11")
b += lines("\\text{सेक्शन A में 20 से कम अंक वाले}", "3+9", "12")
b += lines("\\text{सेक्शन B में 20 से कम अंक वाले}", "5+19", "24")
b += "<ul class='cn'>" \
     f"<li>{sw(BLU)}सेक्शन A का बहुभुज अपने शिखर पर वर्ग-चिह्न 25 (वर्ग 20 − 30, 17 विद्यार्थी) पर है, जबकि {sw(RED)}सेक्शन B का शिखर वर्ग-चिह्न 15 (वर्ग 10 − 20, 19 विद्यार्थी) पर है।</li>" \
     "<li>ऊँचे अंकों (30 − 50) वाले भाग में A का बहुभुज B से ऊपर है और कम अंकों (0 − 20) वाले भाग में B का बहुभुज A से ऊपर है।</li></ul>"
s += part("दोनों सेक्शनों के निष्पादन की तुलना", b)
s += ans("बहुभुज ऊपर बने हैं। सेक्शन A में 30 या अधिक अंक पाने वाले 21 विद्यार्थी हैं, जबकि सेक्शन B में केवल 11; और 20 से कम अंक वाले A में 12, B में 24। "
         "अतः <b>सेक्शन A का निष्पादन सेक्शन B से बेहतर है</b>।")
ANS["Q6"] = "A better (≥30: 21 vs 11)"
E.append((Qx("नीचे की दो सारणियों में प्राप्त किए गए अंकों के अनुसार दो सेक्शनों के विद्यार्थियों का बंटन दिया गया है:", qtab, [],
             "दो बारंबारता बहुभुजों की सहायता से एक ही आलेख पर दोनों सेक्शनों के विद्यार्थियों के प्राप्तांक निरूपित कीजिए। दोनों बहुभुजों का अध्ययन करके दोनों सेक्शनों के निष्पादनों की तुलना कीजिए।"), s))

# ---- Q7 ----
cls7 = [(6 * k + 1, 6 * k + 6) for k in range(10)]
tA = [2, 1, 8, 9, 4, 5, 6, 10, 6, 2]
tB = [5, 6, 2, 10, 5, 6, 3, 4, 8, 10]
assert sum(tA) == 53 and sum(tB) == 59
qtab = tab(["गेदों की संख्या", "टीम A", "टीम B"], [[f"{a} - {c}", x, y] for (a, c), x, y in zip(cls7, tA, tB)])
s = given("पहली 60 गेंदों के 10 वर्ग (1 − 6, …, 55 − 60) और टीम A तथा टीम B के रन", "एक ही आलेख पर दोनों टीमों के बारंबारता बहुभुज")
cb, new7 = cont_block(cls7, tA, BLU, "टीम A के रन", "गेंदें", (6, 7))
cb = cb.replace("<th>टीम A के रन</th>", "<th>" + sw(BLU) + "टीम A</th>")
# add team B column to the continuous table
rows = []
for (lo, hi), (a, c), x, y in zip(cls7, new7, tA, tB):
    rows.append([f"{lo} − {hi}", al(f"{lo}-0.5", nf(a)), al(f"{hi}+0.5", nf(c))])
cb = cb[:cb.index("<div class='tw'>")] + tab(["दिया वर्ग", "नई निम्न सीमा", "नई उच्च सीमा"], rows)
b = cb + F_CM
b += kh("उदाहरण: वर्ग 0.5 − 6.5 का वर्ग-चिह्न") + lines("\\text{वर्ग-चिह्न}", "\\dfrac{6.5+0.5}{2}", "\\dfrac{7}{2}", "3.5")
b += POLY_RULE
b += p("पहले वर्ग 0.5 − 6.5 से पहले का काल्पनिक वर्ग (−5.5) − 0.5 है, जिसका वर्ग-चिह्न −2.5 है। पाठ्यपुस्तक (उदाहरण 4) की तरह पहले बिंदु को (−2.5, 0) से मिलाते हैं और बहुभुज वहाँ से आरंभ करते हैं "
       "जहाँ यह रेखाखंड y-अक्ष को काटता है (गेंदों की संख्या ऋणात्मक नहीं हो सकती)। अंतिम वर्ग के बाद काल्पनिक वर्ग 60.5 − 66.5 का वर्ग-चिह्न 63.5 है।")
ext7 = [(F("-5.5"), F("0.5"))] + new7 + [(F("60.5"), F("66.5"))]
rows = []
for k, ((a, c), (mk, cell)) in enumerate(zip(ext7, cm_rows(ext7))):
    x = ([0] + tA + [0])[k]
    y = ([0] + tB + [0])[k]
    tag = "*" if k in (0, 11) else ""
    rows.append([f"{nf(a).replace('-', '−')} − {nf(c)}{tag}", cell, f"<b style='color:{BLU}'>{x}</b>", f"<b style='color:{RED}'>{y}</b>"])
b += tab(["संतत वर्ग (गेंदें)", "वर्ग-चिह्न", f"{sw(BLU)}टीम A के रन", f"{sw(RED)}टीम B के रन"], rows) + "<div class='muted' style='margin:-4px 0 8px'>* काल्पनिक वर्ग (बारंबारता 0)</div>"
mk7 = [(a + c) / 2 for a, c in ext7]
assert mk7[1] == F("3.5") and mk7[-1] == F("63.5") and mk7[0] == F("-2.5")
g = G((-0.9, 11.4), (0, 10.4), P=29, xt="गेंदों की संख्या", yt="रन", L=50, B=56)
X7 = lambda v: float(v) / 6
for ff, col in ((tA, BLU), (tB, RED)):
    pts = [(X7(mk7[k + 1]), ff[k]) for k in range(10)] + [(X7(mk7[11]), 0)]
    st = (X7(mk7[0]), 0)
    # intersection with x = 0 of segment st -> pts[0]
    t_ = (0 - st[0]) / (pts[0][0] - st[0])
    y0 = pts[0][1] * t_
    g.line(st, (0, y0), col, 1.6, "4 3")
    g.poly([(0, y0)] + pts, col, dots=False)
    for a_, b_ in pts:
        g.top.insert(0, f"<circle cx='{g.X(a_):.1f}' cy='{g.Y(b_):.1f}' r='3' fill='{col}'/>")
    g.top.insert(0, f"<circle cx='{g.X(st[0]):.1f}' cy='{g.Y(0):.1f}' r='2.8' fill='#fff' stroke='{col}' stroke-width='1.5'/>")
xt7 = [(X7(v), nf(v).replace("-", "−")) for v in mk7]
b += scale("x-अक्ष पर: 1 cm = 6 गेंदें (अंकित मान वर्ग-चिह्न हैं)", "y-अक्ष पर: 1 cm = 1 रन")
b += g.svg("बारंबारता बहुभुज: टीम A (नीला) और टीम B (लाल); बिंदीदार भाग काल्पनिक वर्ग (−5.5) − 0.5 तक", xticks=[(c, l) for c, l in xt7],
           yticks=[(k, str(k)) for k in range(1, 11)], xlab_dy=13, olab=(-4, -9, "end"))
b = b.replace("font-size='10.5' text-anchor='middle' dominant-baseline='central' fill='#222'>", "font-size='9.5' text-anchor='middle' dominant-baseline='central' fill='#222'>")
s += part("बारंबारता बहुभुज", b)
s += ans("संतत वर्ग 0.5 − 6.5, 6.5 − 12.5, …, 54.5 − 60.5 बनाकर, वर्ग-चिह्नों 3.5, 9.5, …, 57.5 पर दोनों टीमों के रन अंकित करके एक ही आलेख पर दोनों बारंबारता बहुभुज ऊपर बनाए गए हैं "
         "(टीम A नीला, टीम B लाल)।")
ANS["Q7"] = "two polygons, marks 3.5..57.5"
E.append((Qx("एक क्रिकेट मैच में दो टीमों A और B द्वारा प्रथम 60 गेंदों मे बनाए गए रन नीचे दिए गए हैं:", qtab, [],
             "बारंबारता बहुभुजों की सहायता से एक ही आलेख पर दोनों टीमों के आंकड़े निरूपित कीजिए। (<b>संकेत :</b> पहले वर्ग अंतरालों को संतत बनाइए)"), s))


# ---- unequal-width histograms (Q8, Q9) ----
def adj_block(cls, freq, unit, yunit, col):
    sizes = [c - a for a, c in cls]
    mn = min(sizes)
    b = p("वर्गों की माप (चौड़ाई) समान नहीं है। आयतचित्र में आयत का <b>क्षेत्रफल</b> बारंबारता के अनुपात में होना चाहिए, इसलिए आयतों की लंबाई (ऊँचाई) "
          "न्यूनतम वर्ग-माप के अनुसार समायोजित करते हैं।") + F_SIZE
    rows = [[f"{a} − {c}", al(f"{c}-{a}", f"{c - a}")] for a, c in cls]
    b += tab([f"वर्ग ({unit})", f"वर्ग-माप ({unit})"], rows)
    b += p(f"न्यूनतम वर्ग-माप = <b>{mn} {unit}</b>") + F_ADJ
    rows, adj = [], []
    for (a, c), f, w in zip(cls, freq, sizes):
        v = F(mn, w) * f
        adj.append(v)
        steps = [f"\\dfrac{{{mn}}}{{{w}}}\\times {f}"]
        if w != mn and (mn * f) % w == 0 and mn != 1:
            steps.append(f"\\dfrac{{{mn * f}}}{{{w}}}")
        elif w != mn and mn == 1:
            steps.append(f"\\dfrac{{{f}}}{{{w}}}")
        steps.append(nf(v))
        rows.append([f"{a} − {c}", f, w, f"<span style='color:{col};font-weight:700'>{al(*steps)}</span>"])
    b += tab([f"वर्ग ({unit})", "बारंबारता", "वर्ग-माप", "समायोजित बारंबारता"], rows)
    return b, adj, mn


# ---- Q8 ----
cls8 = [(1, 2), (2, 3), (3, 5), (5, 7), (7, 10), (10, 15), (15, 17)]
f8 = [5, 3, 6, 12, 9, 10, 4]
qtab = tab(["आयु (वर्षों में)", "बच्चों की संख्या"], [[f"{a} - {c}", f] for (a, c), f in zip(cls8, f8)])
s = given("पार्क में खेल रहे बच्चों की आयु (वर्ष) का बंटन — 7 वर्ग, माप असमान", "आयतचित्र")
b, adj8, mn8 = adj_block(cls8, f8, "वर्ष", "बच्चे", PUR)
assert mn8 == 1 and adj8 == [5, 3, 3, 6, F(3), 2, 2]
b += p("अब x-अक्ष पर आयु (1 cm = 1 वर्ष) और y-अक्ष पर समायोजित बारंबारता, अर्थात् <b>प्रति 1 वर्ष के अंतराल पर बच्चों की संख्या</b> (1 cm = 1 बच्चा) लेते हैं। "
       "हर आयत की चौड़ाई = उसकी वर्ग-माप और ऊँचाई = समायोजित बारंबारता।")
rows = [[f"{a} − {c}", al(f"{c - a}\\div 1", f"{c - a}\\ \\text{{cm}}"), al(f"{nf(v)}\\div 1", f"{nf(v)}\\ \\text{{cm}}")] for (a, c), v in zip(cls8, adj8)]
b += tab(["वर्ग (वर्ष)", "आयत की चौड़ाई", "आयत की ऊँचाई"], rows)
g = G((0, 17.6), (0, 6.8), P=20, xt="आयु (वर्षों में)", yt="बच्चे (प्रति 1 वर्ष)", B=50)
for k, ((a, c), v) in enumerate(zip(cls8, adj8)):
    g.rect(a, c, float(v), PUR, op=.3 + .08 * k, label=nf(v))
b += scale("x-अक्ष पर: 1 cm = 1 वर्ष", "y-अक्ष पर: 1 cm = 1 बच्चा (प्रति 1 वर्ष के अंतराल पर)")
b += g.svg("आयतचित्र (असमान वर्ग-माप): पार्क में बच्चों की आयु", xticks=[(k, str(k)) for k in range(1, 18)], yticks=[(k, str(k)) for k in range(1, 7)])
s += b
s += ans("समायोजित बारंबारताएँ 5, 3, 3, 6, 3, 2, 2 (प्रति 1 वर्ष) लेकर, वर्ग-माप के बराबर चौड़ाई वाले आयतों से आयतचित्र ऊपर बनाया गया है।")
ANS["Q8"] = "adjusted 5,3,3,6,3,2,2"
E.append((Qx("एक पार्क में खेल रहे विभिन्न आयु वर्गों के बच्चों की संख्या का एक यादृच्छिक सर्वेक्षण (random survey) करने पर निम्नलिखित आंकड़े प्राप्त हुए :", qtab, [],
             "ऊपर दिए आंकड़ों को निरूपित करने वाला एक आयतचित्र खींचिए।"), s))

# ---- Q9 ----
cls9 = [(1, 4), (4, 6), (6, 8), (8, 12), (12, 20)]
f9 = [6, 30, 44, 16, 4]
assert sum(f9) == 100
qtab = tab(["वर्णमाला के अक्षरों की संख्या", "कुलनामों की संख्या"], [[f"{a} - {c}", f] for (a, c), f in zip(cls9, f9)])
s = given("100 कुलनामों में अक्षरों की संख्या का बंटन — 5 वर्ग, माप असमान", "(i) आयतचित्र<br>(ii) अधिकतम कुलनाम वाला वर्ग अंतराल")
b, adj9, mn9 = adj_block(cls9, f9, "अक्षर", "कुलनाम", ORG)
assert mn9 == 2 and adj9 == [4, 30, 44, 8, 1]
b += p("x-अक्ष पर अक्षरों की संख्या (1 cm = 2 अक्षर) और y-अक्ष पर समायोजित बारंबारता, अर्थात् <b>प्रति 2 अक्षरों के अंतराल पर कुलनामों की संख्या</b> (1 cm = 5 कुलनाम) लेते हैं।")
b += formula("आयत की चौड़ाई और ऊँचाई", "चौड़ाई (cm) = वर्ग-माप ÷ 2; &nbsp;ऊँचाई (cm) = समायोजित बारंबारता ÷ 5")
rows = [[f"{a} − {c}", al(f"{c - a}\\div 2", nf(F(c - a, 2)) + "\\ \\text{cm}"), al(f"{nf(v)}\\div 5", nf(v / 5) + "\\ \\text{cm}")] for (a, c), v in zip(cls9, adj9)]
b += tab(["वर्ग (अक्षर)", "आयत की चौड़ाई", "आयत की ऊँचाई"], rows, hl=2)
g = G((0, 10.6), (0, 9.4), P=30, xt="अक्षरों की संख्या", yt="प्रति 2 अक्षर कुलनामों की संख्या")
for k, ((a, c), v) in enumerate(zip(cls9, adj9)):
    g.rect(a / 2, c / 2, float(v / 5), ORG, op=.35 if k != 2 else .75, label=nf(v))
b += scale("x-अक्ष पर: 1 cm = 2 अक्षर", "y-अक्ष पर: 1 cm = 5 कुलनाम (प्रति 2 अक्षरों के अंतराल पर)")
b += g.svg("आयतचित्र (असमान वर्ग-माप): कुलनामों में अक्षरों की संख्या", xticks=[(k / 2, str(k)) for k in range(4, 21, 2)] + [(1, ""), (0.5, "1")],
           yticks=[(k, str(5 * k)) for k in range(1, 10)])
s += part("(i) आयतचित्र", b)
assert max(f9) == 44 and f9.index(44) == 2
b = p("सबसे अधिक बारंबारता 44 है (आलेख में सबसे ऊँचा, गहरा नारंगी आयत), जो वर्ग 6 − 8 की है।")
s += part("(ii) अधिकतम कुलनाम वाला वर्ग", b)
s += ans("(i) समायोजित बारंबारताएँ 4, 30, 44, 8, 1 (प्रति 2 अक्षर) लेकर आयतचित्र ऊपर बनाया गया है। (ii) वर्ग अंतराल <b>6 − 8</b> में अधिकतम (44) कुलनाम हैं।")
ANS["Q9"] = "adjusted 4,30,44,8,1; 6-8"
E.append((Qx("एक स्थानीय टेलीफोन निर्देशिका से 100 कुलनाम (surname) यदृच्छया लिए गए और उनसें अंग्रेजी वर्णमाला के अक्षरों की संख्या का निम्न बारंबारता बंटन प्राप्त किया गया :", qtab,
             ["(i) दी हुई सूचनाओं को निरूपित करने वाला एक आयतचित्र खींचिए।", "(ii) वह वर्ग अंतराल बताइए जिसमें अधिकतम संख्या में कुलनाम हैं।"]), s))
assert len(E) == 9

# ---------------------------------------------------------------------
check_tex(E)
SUB = "कक्षा 9 गणित · अध्याय 12: " + CH + " (आंकड़ों का आलेखीय निरूपण) · {} प्रश्न"
page(BASE, 12, CH, "exercise-12-1", "प्रश्नावली 12.1", SUB.format(len(E)), E,
     ("/hi/class-09/maths/chapter-11/exercise-11-4/", "प्रश्नावली 11.4"), (BASE, "अध्याय 12"), css=CSS + EXTRA_CSS, boards=BOARDS12)
for k_, v_ in ANS.items():
    print(k_, v_)
print("ok")
