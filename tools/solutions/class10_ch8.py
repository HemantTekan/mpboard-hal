#!/usr/bin/env python3
"""Class 10 Maths, Chapter 8 (त्रिकोणमिति का परिचय): Exercise 8.1, 8.2, 8.3 (rationalised), Hindi medium.
Run from repo root: python3 tools/solutions/class10_ch8.py
"""
import sys, pathlib, re as _re
from fractions import Fraction as F
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from common import *  # noqa
from common import _LAB

BASE = "/hi/class-10/maths/chapter-08/"
CH = "त्रिकोणमिति का परिचय"
_DEV = _re.compile(r"[\u0900-\u097F]")


def mc(c):
    c = str(c)
    if not _DEV.search(c):
        return mcell(c)
    out = []
    for i, piece in enumerate(_re.split(r"\\text\{([^}]*)\}", c)):
        if i % 2:
            out.append(piece)
        elif piece.strip().strip("\\").strip():
            out.append("\\(" + piece.strip().rstrip("\\").strip() + "\\)")
    return " ".join(out)


def lines(head, *rest):
    head, rest = mc(head), [mc(r) for r in rest]
    out = f"<span class='l'>{head}</span><span class='s'>=</span><span class='r'>{rest[0]}</span>"
    out += "".join(f"<span class='l'></span><span class='s'>=</span><span class='r'>{r}</span>" for r in rest[1:])
    return "<div class='eq'>" + out + "</div>"


def eqs(*pairs):
    rows = "".join(f"<span class='l'>{mc(a)}</span><span class='s'>=</span><span class='r'>{mc(b)}</span>" for a, b in pairs)
    return "<div class='eq'>" + rows + "</div>"


def p(t):
    return f"<p>{t}</p>"


def ok(t):
    return f"<p class='ok'>{t}</p>"


def qt(t):
    marks = [mm.start() for mm in _LAB.finditer(t)]
    if len(marks) < 2:
        return t
    pre = t[:marks[0]].strip()
    segs = [t[x:y].strip() for x, y in zip(marks, marks[1:] + [len(t)])]
    return pre + "".join(f"<span style='display:block;font-weight:500;margin-top:4px'>{x}</span>" for x in segs)


def gp(dia, sid, extra=None):
    """दिया है / सिद्ध करना है boxes."""
    h = (f"<div class='gv'><div class='box k'><b>दिया है</b><div>{dia}</div></div>"
         f"<div class='box f'><b>{'सिद्ध करना है' if extra is None else extra}</b><div>{sid}</div></div></div>")
    return h


def pf(*rows):
    """उपपत्ति: each row is (statement, reason); the reason sits on its own small line."""
    out = "<div class='vt'>उपपत्ति:</div><div style='margin:6px 0 4px'>"
    for st, rs in rows:
        out += ("<div style='padding:6px 0;border-bottom:1px dashed #e3e7f3'>"
                f"<div>{st}</div>" + (f"<div style='font-size:.88em;color:#5a6275'>({rs})</div>" if rs else "") + "</div>")
    return out + "</div>"


def r(a, b):
    return m(f"\\dfrac{{{a}}}{{{b}}}")


def T(x):
    return m("\\triangle " + x)


def A(x):
    return m("\\angle " + x)


def fig(W, H, pts, segs, dashed=(), labels=(), extra="", caption=""):
    """Small geometry figure. pts: name -> (x, y, dx, dy) where (dx, dy) shifts the letter."""
    g = [f"<svg class='graph' viewBox='0 0 {W} {H}' role='img' aria-label='{caption or 'आकृति'}' style='max-width:{min(W, 340)}px'>"]
    for a, b in segs:
        (x1, y1, *_), (x2, y2, *_) = pts[a], pts[b]
        g.append(f"<line x1='{x1}' y1='{y1}' x2='{x2}' y2='{y2}' stroke='#1d3a8a' stroke-width='2'/>")
    for a, b in dashed:
        (x1, y1, *_), (x2, y2, *_) = pts[a], pts[b]
        g.append(f"<line x1='{x1}' y1='{y1}' x2='{x2}' y2='{y2}' stroke='#c2410c' stroke-width='1.8' stroke-dasharray='5 4'/>")
    g.append(extra)
    for n, (x, y, dx, dy) in pts.items():
        g.append(f"<circle cx='{x}' cy='{y}' r='2.6' fill='#1d3a8a'/><text x='{x + dx}' y='{y + dy}' font-size='15' font-weight='700' fill='#111' text-anchor='middle'>{n}</text>")
    for x, y, t in labels:
        g.append(f"<text x='{x}' y='{y}' font-size='12.5' fill='#b4232a' text-anchor='middle'>{t}</text>")
    g.append("</svg>")
    cap = f"<div style='font-size:.85em;color:#5a6275;margin-top:2px'>{caption}</div>" if caption else ""
    return "<div style='margin:8px 0'>" + "".join(g) + cap + "</div>"


import math
from fractions import Fraction as F
S3, S2 = math.sqrt(3), math.sqrt(2)
rad = math.radians


def close(a, b):
    assert abs(a - b) < 1e-9, (a, b)


def rt(top, corner, right, lab_v="", lab_h="", lab_hyp="", cap=""):
    """Right triangle: right angle at `corner` (bottom-left), `top` above it, `right` to its right."""
    pts = {top: (40, 30, -12, 4), corner: (40, 170, -12, 14), right: (250, 170, 12, 14)}
    sq = "<polyline points='40,156 54,156 54,170' fill='none' stroke='#1d3a8a' stroke-width='1.4'/>"
    labs = []
    if lab_v: labs.append((20, 104, lab_v))
    if lab_h: labs.append((145, 190, lab_h))
    if lab_hyp: labs.append((160, 90, lab_hyp))
    return fig(290, 200, pts, [(top, corner), (corner, right), (right, top)], labels=labs, extra=sq, caption=cap)


RAT = formula("त्रिकोणमितीय अनुपात", "समकोण त्रिभुज में कोण A के लिए:",
              [m("\\sin A=\\dfrac{\\text{लंब}}{\\text{कर्ण}}"), m("\\cos A=\\dfrac{\\text{आधार}}{\\text{कर्ण}}"), m("\\tan A=\\dfrac{\\text{लंब}}{\\text{आधार}}"),
               m("\\operatorname{cosec} A=\\dfrac1{\\sin A},\\ \\sec A=\\dfrac1{\\cos A},\\ \\cot A=\\dfrac1{\\tan A}")])
PYT = formula("पाइथागोरस प्रमेय", m("(\\text{कर्ण})^2=(\\text{लंब})^2+(\\text{आधार})^2"))
TBL = formula("विशिष्ट कोणों के मान", "",
              [m("\\sin30^\\circ=\\cos60^\\circ=\\tfrac12,\\ \\sin60^\\circ=\\cos30^\\circ=\\tfrac{\\sqrt3}{2}"),
               m("\\sin45^\\circ=\\cos45^\\circ=\\tfrac1{\\sqrt2},\\ \\tan45^\\circ=\\cot45^\\circ=1"),
               m("\\tan30^\\circ=\\tfrac1{\\sqrt3},\\ \\tan60^\\circ=\\sqrt3,\\ \\sec30^\\circ=\\tfrac2{\\sqrt3},\\ \\operatorname{cosec}60^\\circ=\\tfrac2{\\sqrt3}"),
               m("\\sin0^\\circ=0,\\ \\cos0^\\circ=1,\\ \\tan0^\\circ=0")])
IDN = formula("त्रिकोणमितीय सर्वसमिकाएँ", "",
              [m("\\sin^2A+\\cos^2A=1"), m("\\sec^2A-\\tan^2A=1"), m("\\operatorname{cosec}^2A-\\cot^2A=1")])

# =====================================================================  Exercise 8.1
EX81 = []
s = rt("A", "B", "C", "24 cm", "7 cm", "", "ΔABC, ∠B = 90°, AB = 24 cm, BC = 7 cm") + PYT
s += lines("AC^2", "AB^2+BC^2", "24^2+7^2", "576+49", "625") + eqs(("AC", "25\\ \\text{cm}")) + RAT
s += part("(i) कोण A के लिए (लंब BC, आधार AB)", lines("\\sin A", "\\dfrac{BC}{AC}", "\\dfrac{7}{25}") + lines("\\cos A", "\\dfrac{AB}{AC}", "\\dfrac{24}{25}"))
s += part("(ii) कोण C के लिए (लंब AB, आधार BC)", lines("\\sin C", "\\dfrac{AB}{AC}", "\\dfrac{24}{25}") + lines("\\cos C", "\\dfrac{BC}{AC}", "\\dfrac{7}{25}"))
assert 24**2 + 7**2 == 25**2
s += "<div class='vt'>जाँच:</div>" + p(m("\\sin^2A+\\cos^2A=\\dfrac{49}{625}+\\dfrac{576}{625}=1") + " ✔")
s += ans("(i) sin A = 7/25, cos A = 24/25 (ii) sin C = 24/25, cos C = 7/25")
EX81.append(("ΔABC में, जिसका कोण B समकोण है, AB = 24 cm और BC = 7 cm है। निम्नलिखित का मान ज्ञात कीजिए: (i) sin A, cos A (ii) sin C, cos C", s))

s = rt("P", "Q", "R", "12 cm", "", "13 cm", "ΔPQR, ∠Q = 90°, PQ = 12 cm, PR = 13 cm") + PYT
s += lines("QR^2", "PR^2-PQ^2", "13^2-12^2", "169-144", "25") + eqs(("QR", "5\\ \\text{cm}"))
s += lines("\\tan P", "\\dfrac{QR}{PQ}", "\\dfrac{5}{12}") + lines("\\cot R", "\\dfrac{QR}{PQ}", "\\dfrac{5}{12}")
s += lines("\\tan P-\\cot R", "\\dfrac5{12}-\\dfrac5{12}", "0") + ans("tan P − cot R = 0")
EX81.append(("आकृति में (ΔPQR, ∠Q = 90°, PQ = 12 cm, PR = 13 cm), tan P − cot R का मान ज्ञात कीजिए।", s))

close(math.cos(math.asin(.75)), math.sqrt(7) / 4)
s = rt("C", "B", "A", "3k", "√7 k", "4k", "ΔABC, ∠B = 90°") + p(m("\\sin A=\\dfrac34=\\dfrac{BC}{AC}") + ", इसलिए BC = 3k, AC = 4k (k धनात्मक)") + PYT
s += lines("AB^2", "AC^2-BC^2", "16k^2-9k^2", "7k^2") + eqs(("AB", "\\sqrt7\\,k"))
s += lines("\\cos A", "\\dfrac{AB}{AC}", "\\dfrac{\\sqrt7\\,k}{4k}", "\\dfrac{\\sqrt7}{4}") + lines("\\tan A", "\\dfrac{BC}{AB}", "\\dfrac{3k}{\\sqrt7\\,k}", "\\dfrac{3}{\\sqrt7}")
s += "<div class='vt'>जाँच:</div>" + p(m("\\sin^2A+\\cos^2A=\\dfrac9{16}+\\dfrac7{16}=1") + " ✔") + ans("(i) cos A = √7/4 (ii) tan A = 3/√7")
EX81.append(("यदि sin A = 3/4 तो cos A और tan A का मान परिकलित कीजिए।", s))

s = rt("C", "B", "A", "15k", "8k", "17k", "ΔABC, ∠B = 90°") + eqs(("15\\cot A", "8"), ("\\cot A", "\\dfrac8{15}"))
s += p(m("\\cot A=\\dfrac{AB}{BC}") + ", इसलिए AB = 8k, BC = 15k") + PYT + lines("AC^2", "(8k)^2+(15k)^2", "64k^2+225k^2", "289k^2") + eqs(("AC", "17k"))
s += lines("\\sin A", "\\dfrac{BC}{AC}", "\\dfrac{15}{17}") + lines("\\sec A", "\\dfrac{AC}{AB}", "\\dfrac{17}{8}")
s += ans("(i) sin A = 15/17 (ii) sec A = 17/8")
EX81.append(("यदि 15 cot A = 8 दिया गया हो तो sin A और sec A का मान ज्ञात कीजिए।", s))

s = rt("C", "B", "A", "5k", "12k", "13k", "ΔABC, ∠B = 90°, ∠A = θ") + p(m("\\sec\\theta=\\dfrac{13}{12}=\\dfrac{\\text{कर्ण}}{\\text{आधार}}") + ", इसलिए AC = 13k, AB = 12k") + PYT
s += lines("BC^2", "(13k)^2-(12k)^2", "169k^2-144k^2", "25k^2") + eqs(("BC", "5k"))
for nm, v in (("\\sin\\theta", "\\dfrac{5}{13}"), ("\\cos\\theta", "\\dfrac{12}{13}"), ("\\tan\\theta", "\\dfrac{5}{12}"), ("\\cot\\theta", "\\dfrac{12}{5}"), ("\\operatorname{cosec}\\theta", "\\dfrac{13}{5}")):
    s += lines(nm, v)
s += ans("(i) sin θ = 5/13 (ii) cos θ = 12/13 (iii) tan θ = 5/12 (iv) cot θ = 12/5 (v) cosec θ = 13/5")
EX81.append(("यदि sec θ = 13/12, तो अन्य सभी त्रिकोणमितीय अनुपात परिकलित कीजिए।", s))

s = gp("∠A और ∠B न्यूनकोण हैं तथा cos A = cos B", "∠A = ∠B")
s += p("दो समकोण त्रिभुज ACD और BCD लीजिए जिनमें CD ⊥ AB है (D पर समकोण)।")
s += pf(("cos A = AD/AC और cos B = BD/BC", "कोज्या की परिभाषा"),
        ("AD/AC = BD/BC, अर्थात् AD/BD = AC/BC = k (मान लीजिए)", "cos A = cos B (दिया है)"),
        ("AD = k·BD और AC = k·BC", ""),
        ("CD² = AC² − AD² = k²BC² − k²BD² = k²(BC² − BD²)", "पाइथागोरस प्रमेय"),
        ("CD² = BC² − BD²", "ΔBCD में पाइथागोरस प्रमेय"),
        ("दोनों से k² = 1, अर्थात् k = 1", "CD² ≠ 0"),
        ("AC = BC", "k = 1"),
        ("∠A = ∠B", "बराबर भुजाओं के सम्मुख कोण बराबर होते हैं"))
s += ok("अतः ∠A = ∠B (इति सिद्धम्)")
EX81.append(("यदि ∠A और ∠B न्यूनकोण हों, जहाँ cos A = cos B, तो दिखाइए कि ∠A = ∠B.", s))

th = math.atan2(8, 7)
close((1 + math.sin(th)) * (1 - math.sin(th)) / ((1 + math.cos(th)) * (1 - math.cos(th))), 49 / 64)
s = rt("C", "B", "A", "8k", "7k", "√113 k", "∠A = θ, cot θ = 7/8") + lines("AC", "\\sqrt{(7k)^2+(8k)^2}", "\\sqrt{113}\\,k")
s += lines("\\sin\\theta", "\\dfrac{8}{\\sqrt{113}}") + lines("\\cos\\theta", "\\dfrac{7}{\\sqrt{113}}")
s += part("(i)", lines("\\dfrac{(1+\\sin\\theta)(1-\\sin\\theta)}{(1+\\cos\\theta)(1-\\cos\\theta)}", "\\dfrac{1-\\sin^2\\theta}{1-\\cos^2\\theta}", "\\dfrac{1-\\frac{64}{113}}{1-\\frac{49}{113}}", "\\dfrac{49/113}{64/113}", "\\dfrac{49}{64}"))
s += part("(ii)", lines("\\cot^2\\theta", "\\left(\\dfrac78\\right)^2", "\\dfrac{49}{64}"))
s += ans("(i) 49/64 (ii) 49/64")
EX81.append(("यदि cot θ = 7/8 तो (i) (1 + sin θ)(1 − sin θ) / ((1 + cos θ)(1 − cos θ)) (ii) cot²θ का मान निकालिए।", s))

s = eqs(("3\\cot A", "4"), ("\\cot A", "\\dfrac43")) + rt("C", "B", "A", "3k", "4k", "5k", "AB = 4k, BC = 3k, AC = 5k")
s += p(m("\\tan A=\\dfrac34,\\ \\sin A=\\dfrac35,\\ \\cos A=\\dfrac45"))
s += lines("\\text{बायाँ पक्ष}", "\\dfrac{1-\\tan^2A}{1+\\tan^2A}", "\\dfrac{1-\\frac9{16}}{1+\\frac9{16}}", "\\dfrac{7/16}{25/16}", "\\dfrac{7}{25}")
s += lines("\\text{दायाँ पक्ष}", "\\cos^2A-\\sin^2A", "\\dfrac{16}{25}-\\dfrac9{25}", "\\dfrac{7}{25}")
s += ok("बायाँ पक्ष = दायाँ पक्ष") + ans("हाँ, (1 − tan²A)/(1 + tan²A) = cos²A − sin²A (दोनों 7/25)")
EX81.append(("यदि 3 cot A = 4, तो जाँच कीजिए कि (1 − tan²A)/(1 + tan²A) = cos²A − sin²A है या नहीं।", s))

s = rt("C", "B", "A", "k", "√3 k", "2k", "ΔABC, ∠B = 90°, tan A = 1/√3") + lines("AC", "\\sqrt{(\\sqrt3k)^2+k^2}", "\\sqrt{4k^2}", "2k")
s += p(m("\\sin A=\\dfrac12,\\ \\cos A=\\dfrac{\\sqrt3}2,\\ \\sin C=\\dfrac{\\sqrt3}2,\\ \\cos C=\\dfrac12"))
s += part("(i)", lines("\\sin A\\cos C+\\cos A\\sin C", "\\dfrac12\\cdot\\dfrac12+\\dfrac{\\sqrt3}2\\cdot\\dfrac{\\sqrt3}2", "\\dfrac14+\\dfrac34", "1"))
s += part("(ii)", lines("\\cos A\\cos C-\\sin A\\sin C", "\\dfrac{\\sqrt3}2\\cdot\\dfrac12-\\dfrac12\\cdot\\dfrac{\\sqrt3}2", "0"))
s += ans("(i) 1 (ii) 0")
EX81.append(("त्रिभुज ABC में, जिसका कोण B समकोण है, यदि tan A = 1/√3 तो निम्नलिखित के मान ज्ञात कीजिए: (i) sin A cos C + cos A sin C (ii) cos A cos C − sin A sin C", s))

assert (25 - 12) ** 2 == 25 + 144
s = rt("P", "Q", "R", "5 cm", "x cm", "(25 − x) cm", "ΔPQR, ∠Q = 90°") + p("मान लीजिए QR = x cm, तब PR = (25 − x) cm") + PYT
s += eqs(("(25-x)^2", "5^2+x^2"), ("625-50x+x^2", "25+x^2"), ("-50x", "-600"), ("x", "12"))
s += p("अतः QR = 12 cm और PR = 25 − 12 = 13 cm")
s += lines("\\sin P", "\\dfrac{QR}{PR}", "\\dfrac{12}{13}") + lines("\\cos P", "\\dfrac{PQ}{PR}", "\\dfrac{5}{13}") + lines("\\tan P", "\\dfrac{QR}{PQ}", "\\dfrac{12}{5}")
s += "<div class='vt'>जाँच:</div>" + p(m("5^2+12^2=169=13^2") + " और 13 + 12 = 25 ✔") + ans("(i) sin P = 12/13 (ii) cos P = 5/13 (iii) tan P = 12/5")
EX81.append(("ΔPQR में, जिसका कोण Q समकोण है, PR + QR = 25 cm और PQ = 5 cm है। sin P, cos P और tan P के मान ज्ञात कीजिए।", s))

s = part("(i) असत्य", p("उदाहरण: " + m("\\tan60^\\circ=\\sqrt3>1") + "।"))
s += part("(ii) सत्य", p(m("\\sec A=\\dfrac{\\text{कर्ण}}{\\text{आधार}}\\ge1") + "; कर्ण 12 और आधार 5 वाला समकोण त्रिभुज बन सकता है।"))
s += part("(iii) असत्य", p("cos A, कोण A की कोज्या (cosine) का संक्षिप्त रूप है, cosecant का संक्षिप्त रूप cosec A है।"))
s += part("(iv) असत्य", p("cot A एक ही संकेत है, cot और A का गुणनफल नहीं; A के बिना cot का कोई अर्थ नहीं।"))
s += part("(v) असत्य", p(m("\\sin\\theta=\\dfrac{\\text{लंब}}{\\text{कर्ण}}\\le1") + ", जबकि " + m("\\dfrac43>1") + "।"))
s += ans("(i) असत्य (ii) सत्य (iii) असत्य (iv) असत्य (v) असत्य")
EX81.append(("बताइए कि निम्नलिखित कथन सत्य हैं या असत्य। कारण सहित अपने उत्तर की पुष्टि कीजिए। (i) tan A का मान सदैव 1 से कम होता है। (ii) कोण A के किसी मान के लिए sec A = 12/5 (iii) cos A, कोण A के cosecant के लिए प्रयुक्त एक संक्षिप्त रूप है। (iv) cot A, cot और A का गुणनफल होता है। (v) किसी भी कोण θ के लिए sin θ = 4/3", s))

# =====================================================================  Exercise 8.2
EX82 = []
v3 = math.cos(rad(45)) / (1 / math.cos(rad(30)) + 1 / math.sin(rad(30)))
close(v3, (3 * S2 - math.sqrt(6)) / 8)
v4 = (0.5 + 1 - 2 / S3) / (2 / S3 + 0.5 + 1)
close(v4, (43 - 24 * S3) / 11)
P = []
P.append(("(i)", lines("\\sin60^\\circ\\cos30^\\circ+\\sin30^\\circ\\cos60^\\circ", "\\dfrac{\\sqrt3}2\\cdot\\dfrac{\\sqrt3}2+\\dfrac12\\cdot\\dfrac12", "\\dfrac34+\\dfrac14", "1"), "1"))
P.append(("(ii)", lines("2\\tan^245^\\circ+\\cos^230^\\circ-\\sin^260^\\circ", "2(1)^2+\\left(\\dfrac{\\sqrt3}2\\right)^2-\\left(\\dfrac{\\sqrt3}2\\right)^2", "2+\\dfrac34-\\dfrac34", "2"), "2"))
P.append(("(iii)", lines("\\dfrac{\\cos45^\\circ}{\\sec30^\\circ+\\operatorname{cosec}30^\\circ}", "\\dfrac{\\frac1{\\sqrt2}}{\\frac2{\\sqrt3}+2}", "\\dfrac{\\frac1{\\sqrt2}}{\\frac{2+2\\sqrt3}{\\sqrt3}}", "\\dfrac{\\sqrt3}{2\\sqrt2(\\sqrt3+1)}",
                          "\\dfrac{\\sqrt3(\\sqrt3-1)}{2\\sqrt2(\\sqrt3+1)(\\sqrt3-1)}", "\\dfrac{3-\\sqrt3}{4\\sqrt2}", "\\dfrac{(3-\\sqrt3)\\sqrt2}{8}", "\\dfrac{3\\sqrt2-\\sqrt6}{8}"), "(3√2 − √6)/8"))
P.append(("(iv)", lines("\\dfrac{\\sin30^\\circ+\\tan45^\\circ-\\operatorname{cosec}60^\\circ}{\\sec30^\\circ+\\cos60^\\circ+\\cot45^\\circ}", "\\dfrac{\\frac12+1-\\frac2{\\sqrt3}}{\\frac2{\\sqrt3}+\\frac12+1}") +
          p("अंश और हर दोनों के सभी पदों को " + m("2\\sqrt3") + " से गुणा करने पर") +
          lines("", "\\dfrac{\\sqrt3+2\\sqrt3-4}{4+\\sqrt3+2\\sqrt3}", "\\dfrac{3\\sqrt3-4}{3\\sqrt3+4}", "\\dfrac{(3\\sqrt3-4)^2}{(3\\sqrt3)^2-4^2}", "\\dfrac{27-24\\sqrt3+16}{27-16}", "\\dfrac{43-24\\sqrt3}{11}"), "(43 − 24√3)/11"))
P.append(("(v)", lines("\\dfrac{5\\cos^260^\\circ+4\\sec^230^\\circ-\\tan^245^\\circ}{\\sin^230^\\circ+\\cos^230^\\circ}", "\\dfrac{5\\cdot\\frac14+4\\cdot\\frac43-1}{\\frac14+\\frac34}", "\\dfrac54+\\dfrac{16}3-1", "\\dfrac{15+64-12}{12}", "\\dfrac{67}{12}"), "67/12"))
close((5 * .25 + 4 * 4 / 3 - 1) / 1, 67 / 12)
s = TBL + "".join(part(l, x) for l, x, _ in P) + ans(" ".join(f"{l} {a}" for l, _, a in P))
EX82.append(("निम्नलिखित के मान निकालिए: (i) sin 60° cos 30° + sin 30° cos 60° (ii) 2 tan²45° + cos²30° − sin²60° (iii) cos 45° / (sec 30° + cosec 30°) (iv) (sin 30° + tan 45° − cosec 60°) / (sec 30° + cos 60° + cot 45°) (v) (5 cos²60° + 4 sec²30° − tan²45°) / (sin²30° + cos²30°)", s))

P = []
P.append(("(i)", lines("\\dfrac{2\\tan30^\\circ}{1+\\tan^230^\\circ}", "\\dfrac{\\frac2{\\sqrt3}}{1+\\frac13}", "\\dfrac{2}{\\sqrt3}\\times\\dfrac34", "\\dfrac{\\sqrt3}{2}", "\\sin60^\\circ"), "(A) sin 60°"))
P.append(("(ii)", lines("\\dfrac{1-\\tan^245^\\circ}{1+\\tan^245^\\circ}", "\\dfrac{1-1}{1+1}", "0"), "(D) 0"))
P.append(("(iii)", p("A = 0° रखने पर: " + m("\\sin0^\\circ=0") + " और " + m("2\\sin0^\\circ=0") + ", दोनों बराबर। A = 30° पर " + m("\\sin60^\\circ=\\tfrac{\\sqrt3}2\\ne1=2\\sin30^\\circ") + "।"), "(A) 0°"))
P.append(("(iv)", lines("\\dfrac{2\\tan30^\\circ}{1-\\tan^230^\\circ}", "\\dfrac{\\frac2{\\sqrt3}}{1-\\frac13}", "\\dfrac2{\\sqrt3}\\times\\dfrac32", "\\sqrt3", "\\tan60^\\circ"), "(C) tan 60°"))
s = TBL + "".join(part(l, x) for l, x, _ in P) + ans(" ".join(f"{l} {a}" for l, _, a in P))
EX82.append(("सही विकल्प चुनिए और अपने विकल्प का औचित्य दीजिए: (i) 2 tan 30° / (1 + tan²30°) = (A) sin 60° (B) cos 60° (C) tan 60° (D) sin 30° (ii) (1 − tan²45°)/(1 + tan²45°) = (A) tan 90° (B) 1 (C) sin 45° (D) 0 (iii) sin 2A = 2 sin A तब सत्य होता है, जबकि A बराबर है: (A) 0° (B) 30° (C) 45° (D) 60° (iv) 2 tan 30° / (1 − tan²30°) = (A) cos 60° (B) sin 60° (C) tan 60° (D) sin 30°", s))

close(math.tan(rad(60)), S3); close(math.tan(rad(30)), 1 / S3)
s = TBL + eqs(("\\tan(A+B)", "\\sqrt3=\\tan60^\\circ"), ("A+B", "60^\\circ\\quad\\cdots(1)")) + eqs(("\\tan(A-B)", "\\dfrac1{\\sqrt3}=\\tan30^\\circ"), ("A-B", "30^\\circ\\quad\\cdots(2)"))
s += p("(1) और (2) को जोड़ने पर") + eqs(("2A", "90^\\circ"), ("A", "45^\\circ")) + p("(1) में रखने पर") + eqs(("B", "60^\\circ-45^\\circ=15^\\circ"))
s += "<div class='vt'>जाँच:</div>" + p(m("\\tan60^\\circ=\\sqrt3") + " ✔ और " + m("\\tan30^\\circ=\\tfrac1{\\sqrt3}") + " ✔") + ans("(i) A = 45° (ii) B = 15°")
EX82.append(("यदि tan (A + B) = √3 और tan (A − B) = 1/√3; 0° < A + B ≤ 90°; A > B तो A और B का मान ज्ञात कीजिए।", s))

s = part("(i) असत्य", p("A = 30°, B = 60° लेने पर: " + m("\\sin90^\\circ=1") + " जबकि " + m("\\sin30^\\circ+\\sin60^\\circ=\\tfrac{1+\\sqrt3}2\\ne1") + "।"))
s += part("(ii) सत्य", p("0° से 90° तक sin का मान 0 से 1 तक बढ़ता है: " + m("0,\\tfrac12,\\tfrac1{\\sqrt2},\\tfrac{\\sqrt3}2,1") + "।"))
s += part("(iii) असत्य", p("cos का मान 1 से 0 तक घटता है: " + m("1,\\tfrac{\\sqrt3}2,\\tfrac1{\\sqrt2},\\tfrac12,0") + "।"))
s += part("(iv) असत्य", p("केवल θ = 45° पर sin θ = cos θ; जैसे " + m("\\sin30^\\circ=\\tfrac12\\ne\\tfrac{\\sqrt3}2=\\cos30^\\circ") + "।"))
s += part("(v) सत्य", p(m("\\cot0^\\circ=\\dfrac{\\cos0^\\circ}{\\sin0^\\circ}=\\dfrac10") + ", जो परिभाषित नहीं है।"))
s += ans("(i) असत्य (ii) सत्य (iii) असत्य (iv) असत्य (v) सत्य")
EX82.append(("बताइए कि निम्नलिखित सत्य हैं या असत्य। कारण सहित उत्तर की पुष्टि कीजिए। (i) sin (A + B) = sin A + sin B (ii) θ में वृद्धि होने के साथ sin θ के मान में भी वृद्धि होती है। (iii) θ में वृद्धि होने के साथ cos θ के मान में भी वृद्धि होती है। (iv) θ के सभी मानों पर sin θ = cos θ (v) A = 0° पर cot A परिभाषित नहीं है।", s))

# =====================================================================  Exercise 8.3
EX83 = []
a = rad(37)
cot = 1 / math.tan(a)
close(math.sin(a), 1 / math.sqrt(1 + cot**2)); close(1 / math.cos(a), math.sqrt(1 + cot**2) / cot)
s = IDN + part("sin A", lines("\\operatorname{cosec}^2A", "1+\\cot^2A") + lines("\\dfrac1{\\sin^2A}", "1+\\cot^2A") + lines("\\sin A", "\\dfrac{1}{\\sqrt{1+\\cot^2A}}"))
s += part("tan A", lines("\\tan A", "\\dfrac{1}{\\cot A}"))
s += part("sec A", lines("\\sec^2A", "1+\\tan^2A", "1+\\dfrac1{\\cot^2A}", "\\dfrac{\\cot^2A+1}{\\cot^2A}") + lines("\\sec A", "\\dfrac{\\sqrt{1+\\cot^2A}}{\\cot A}"))
s += ans("(i) sin A = 1/√(1 + cot²A) (ii) sec A = √(1 + cot²A)/cot A (iii) tan A = 1/cot A")
EX83.append(("त्रिकोणमितीय अनुपातों sin A, sec A और tan A को cot A के पदों में व्यक्त कीजिए।", s))

sec = 1 / math.cos(a)
close(math.sin(a), math.sqrt(sec**2 - 1) / sec); close(1 / math.sin(a), sec / math.sqrt(sec**2 - 1))
s = IDN + lines("\\cos A", "\\dfrac1{\\sec A}") + lines("\\tan A", "\\sqrt{\\sec^2A-1}") + lines("\\sin A", "\\tan A\\cdot\\cos A", "\\dfrac{\\sqrt{\\sec^2A-1}}{\\sec A}")
s += lines("\\cot A", "\\dfrac1{\\tan A}", "\\dfrac1{\\sqrt{\\sec^2A-1}}") + lines("\\operatorname{cosec} A", "\\dfrac1{\\sin A}", "\\dfrac{\\sec A}{\\sqrt{\\sec^2A-1}}")
s += ans("(i) cos A = 1/sec A (ii) sin A = √(sec²A − 1)/sec A (iii) tan A = √(sec²A − 1) (iv) cot A = 1/√(sec²A − 1) (v) cosec A = sec A/√(sec²A − 1)")
EX83.append(("कोण A के अन्य सभी त्रिकोणमितीय अनुपातों को sec A के पदों में लिखिए।", s))

t = a
close((1 + math.tan(t) + 1 / math.cos(t)) * (1 + 1 / math.tan(t) - 1 / math.sin(t)), 2)
close((1 / math.cos(t) + math.tan(t)) * (1 - math.sin(t)), math.cos(t))
P = []
P.append(("(i)", lines("9\\sec^2A-9\\tan^2A", "9(\\sec^2A-\\tan^2A)", "9\\times1", "9"), "(B) 9"))
P.append(("(ii)", lines("1+\\tan\\theta+\\sec\\theta", "\\dfrac{\\sin\\theta+\\cos\\theta+1}{\\cos\\theta}") + lines("1+\\cot\\theta-\\operatorname{cosec}\\theta", "\\dfrac{\\sin\\theta+\\cos\\theta-1}{\\sin\\theta}") +
          lines("\\text{गुणनफल}", "\\dfrac{(\\sin\\theta+\\cos\\theta)^2-1^2}{\\sin\\theta\\cos\\theta}", "\\dfrac{1+2\\sin\\theta\\cos\\theta-1}{\\sin\\theta\\cos\\theta}", "2"), "(C) 2"))
P.append(("(iii)", lines("\\sec A+\\tan A", "\\dfrac{1+\\sin A}{\\cos A}") + lines("\\text{गुणनफल}", "\\dfrac{1-\\sin^2A}{\\cos A}", "\\dfrac{\\cos^2A}{\\cos A}", "\\cos A"), "(D) cos A"))
P.append(("(iv)", lines("\\dfrac{1+\\tan^2A}{1+\\cot^2A}", "\\dfrac{\\sec^2A}{\\operatorname{cosec}^2A}", "\\dfrac{\\sin^2A}{\\cos^2A}", "\\tan^2A"), "(D) tan²A"))
s = IDN + "".join(part(l, x) for l, x, _ in P) + ans(" ".join(f"{l} {a_}" for l, _, a_ in P))
EX83.append(("सही विकल्प चुनिए और अपने विकल्प का औचित्य दीजिए: (i) 9 sec²A − 9 tan²A बराबर है: (A) 1 (B) 9 (C) 8 (D) 0 (ii) (1 + tan θ + sec θ)(1 + cot θ − cosec θ) बराबर है: (A) 0 (B) 1 (C) 2 (D) −1 (iii) (sec A + tan A)(1 − sin A) बराबर है: (A) sec A (B) sin A (C) cosec A (D) cos A (iv) (1 + tan²A)/(1 + cot²A) बराबर है: (A) sec²A (B) −1 (C) cot²A (D) tan²A", s))

# Q4 identities: numeric check of each at a sample acute angle
x = rad(37)
sn, cs = math.sin(x), math.cos(x)
tn, ct, sc, cc = sn / cs, cs / sn, 1 / cs, 1 / sn
checks = [((cc - ct) ** 2, (1 - cs) / (1 + cs)), (cs / (1 + sn) + (1 + sn) / cs, 2 * sc), (tn / (1 - ct) + ct / (1 - tn), 1 + sc * cc), ((1 + sc) / sc, sn**2 / (1 - cs)),
          ((cs - sn + 1) / (cs + sn - 1), cc + ct), (math.sqrt((1 + sn) / (1 - sn)), sc + tn), ((sn - 2 * sn**3) / (2 * cs**3 - cs), tn), ((sn + cc) ** 2 + (cs + sc) ** 2, 7 + tn**2 + ct**2),
          ((cc - sn) * (sc - cs), 1 / (tn + ct)), ((1 + tn**2) / (1 + ct**2), tn**2), (((1 - tn) / (1 - ct)) ** 2, tn**2)]
for l_, r_ in checks:
    close(l_, r_)

L = "\\text{बायाँ पक्ष}"
P = []
P.append(("(i)", lines(L, "(\\operatorname{cosec}\\theta-\\cot\\theta)^2", "\\left(\\dfrac1{\\sin\\theta}-\\dfrac{\\cos\\theta}{\\sin\\theta}\\right)^2", "\\dfrac{(1-\\cos\\theta)^2}{\\sin^2\\theta}", "\\dfrac{(1-\\cos\\theta)^2}{1-\\cos^2\\theta}",
                       "\\dfrac{(1-\\cos\\theta)^2}{(1-\\cos\\theta)(1+\\cos\\theta)}", "\\dfrac{1-\\cos\\theta}{1+\\cos\\theta}")))
P.append(("(ii)", lines(L, "\\dfrac{\\cos A}{1+\\sin A}+\\dfrac{1+\\sin A}{\\cos A}", "\\dfrac{\\cos^2A+(1+\\sin A)^2}{(1+\\sin A)\\cos A}", "\\dfrac{\\cos^2A+1+2\\sin A+\\sin^2A}{(1+\\sin A)\\cos A}",
                        "\\dfrac{2+2\\sin A}{(1+\\sin A)\\cos A}", "\\dfrac{2(1+\\sin A)}{(1+\\sin A)\\cos A}", "\\dfrac{2}{\\cos A}", "2\\sec A")))
P.append(("(iii)", p(m("\\tan\\theta=t") + " लिखने पर " + m("\\cot\\theta=\\dfrac1t")) +
          lines(L, "\\dfrac{t}{1-\\frac1t}+\\dfrac{\\frac1t}{1-t}", "\\dfrac{t^2}{t-1}-\\dfrac{1}{t(t-1)}", "\\dfrac{t^3-1}{t(t-1)}", "\\dfrac{(t-1)(t^2+t+1)}{t(t-1)}", "\\dfrac{t^2+t+1}{t}", "t+1+\\dfrac1t") +
          lines("t+\\dfrac1t", "\\dfrac{\\sin\\theta}{\\cos\\theta}+\\dfrac{\\cos\\theta}{\\sin\\theta}", "\\dfrac{\\sin^2\\theta+\\cos^2\\theta}{\\sin\\theta\\cos\\theta}", "\\sec\\theta\\operatorname{cosec}\\theta") +
          p("अतः बायाँ पक्ष = " + m("1+\\sec\\theta\\operatorname{cosec}\\theta") + " = दायाँ पक्ष")))
P.append(("(iv)", lines(L, "\\dfrac{1+\\sec A}{\\sec A}", "\\dfrac{1+\\frac1{\\cos A}}{\\frac1{\\cos A}}", "\\cos A+1") +
          lines("\\text{दायाँ पक्ष}", "\\dfrac{\\sin^2A}{1-\\cos A}", "\\dfrac{1-\\cos^2A}{1-\\cos A}", "\\dfrac{(1-\\cos A)(1+\\cos A)}{1-\\cos A}", "1+\\cos A")))
P.append(("(v)", p("अंश और हर दोनों के सभी पदों को " + m("\\sin A") + " से भाग देने पर") +
          lines(L, "\\dfrac{\\cot A-1+\\operatorname{cosec} A}{\\cot A+1-\\operatorname{cosec} A}") + p("अंश में " + m("1=\\operatorname{cosec}^2A-\\cot^2A") + " रखने पर:") +
          lines("\\text{अंश}", "(\\operatorname{cosec} A+\\cot A)-1", "(\\operatorname{cosec} A+\\cot A)-(\\operatorname{cosec}^2A-\\cot^2A)", "(\\operatorname{cosec} A+\\cot A)\\big[1-(\\operatorname{cosec} A-\\cot A)\\big]", "(\\operatorname{cosec} A+\\cot A)(1-\\operatorname{cosec} A+\\cot A)") +
          p("हर = " + m("\\cot A+1-\\operatorname{cosec} A") + ", जो अंश के दूसरे गुणनखंड के बराबर है।") + lines(L, "\\operatorname{cosec} A+\\cot A")))
P.append(("(vi)", lines(L, "\\sqrt{\\dfrac{1+\\sin A}{1-\\sin A}}", "\\sqrt{\\dfrac{(1+\\sin A)(1+\\sin A)}{(1-\\sin A)(1+\\sin A)}}", "\\sqrt{\\dfrac{(1+\\sin A)^2}{\\cos^2A}}", "\\dfrac{1+\\sin A}{\\cos A}", "\\sec A+\\tan A")))
P.append(("(vii)", lines(L, "\\dfrac{\\sin\\theta-2\\sin^3\\theta}{2\\cos^3\\theta-\\cos\\theta}", "\\dfrac{\\sin\\theta(1-2\\sin^2\\theta)}{\\cos\\theta(2\\cos^2\\theta-1)}", "\\dfrac{\\sin\\theta(1-2(1-\\cos^2\\theta))}{\\cos\\theta(2\\cos^2\\theta-1)}",
                         "\\dfrac{\\sin\\theta(2\\cos^2\\theta-1)}{\\cos\\theta(2\\cos^2\\theta-1)}", "\\tan\\theta")))
P.append(("(viii)", lines("(\\sin A+\\operatorname{cosec} A)^2", "\\sin^2A+\\operatorname{cosec}^2A+2") + lines("(\\cos A+\\sec A)^2", "\\cos^2A+\\sec^2A+2") +
          p("(" + m("\\sin A\\cdot\\operatorname{cosec} A=1,\\ \\cos A\\sec A=1") + ")") +
          p("जोड़ने पर, " + m("\\sin^2A+\\cos^2A=1") + " से:") + lines(L, "1+\\operatorname{cosec}^2A+\\sec^2A+4", "1+(1+\\cot^2A)+(1+\\tan^2A)+4", "7+\\tan^2A+\\cot^2A")))
P.append(("(ix)", lines(L, "(\\operatorname{cosec} A-\\sin A)(\\sec A-\\cos A)", "\\dfrac{1-\\sin^2A}{\\sin A}\\cdot\\dfrac{1-\\cos^2A}{\\cos A}", "\\dfrac{\\cos^2A\\sin^2A}{\\sin A\\cos A}", "\\sin A\\cos A") +
          lines("\\text{दायाँ पक्ष}", "\\dfrac1{\\tan A+\\cot A}", "\\dfrac1{\\frac{\\sin^2A+\\cos^2A}{\\sin A\\cos A}}", "\\sin A\\cos A")))
P.append(("(x)", lines("\\dfrac{1+\\tan^2A}{1+\\cot^2A}", "\\dfrac{\\sec^2A}{\\operatorname{cosec}^2A}", "\\tan^2A") +
          lines("\\left(\\dfrac{1-\\tan A}{1-\\cot A}\\right)^2", "\\left(\\dfrac{1-\\tan A}{1-\\frac1{\\tan A}}\\right)^2", "\\left(\\dfrac{(1-\\tan A)\\tan A}{\\tan A-1}\\right)^2", "(-\\tan A)^2", "\\tan^2A") +
          p("तीनों बराबर हैं।")))
s = IDN + "".join(part(l, x_ + ok("बायाँ पक्ष = दायाँ पक्ष (इति सिद्धम्)")) for l, x_ in P)
s += ans("सभी दस सर्वसमिकाएँ सिद्ध हुईं।")
EX83.append(("निम्नलिखित सर्वसमिकाएँ सिद्ध कीजिए, जहाँ वे कोण, जिनके लिए व्यंजक परिभाषित है, न्यूनकोण है: (i) (cosec θ − cot θ)² = (1 − cos θ)/(1 + cos θ) (ii) cos A/(1 + sin A) + (1 + sin A)/cos A = 2 sec A (iii) tan θ/(1 − cot θ) + cot θ/(1 − tan θ) = 1 + sec θ cosec θ (iv) (1 + sec A)/sec A = sin²A/(1 − cos A) (v) (cos A − sin A + 1)/(cos A + sin A − 1) = cosec A + cot A, सर्वसमिका cosec²A = 1 + cot²A का प्रयोग करके (vi) √((1 + sin A)/(1 − sin A)) = sec A + tan A (vii) (sin θ − 2 sin³θ)/(2 cos³θ − cos θ) = tan θ (viii) (sin A + cosec A)² + (cos A + sec A)² = 7 + tan²A + cot²A (ix) (cosec A − sin A)(sec A − cos A) = 1/(tan A + cot A) (x) (1 + tan²A)/(1 + cot²A) = ((1 − tan A)/(1 − cot A))² = tan²A", s))

EX81, EX82, EX83 = ([(qt(t_), b_) for t_, b_ in L_] for L_ in (EX81, EX82, EX83))
page(BASE, 8, CH, "exercise-8-1", "प्रश्नावली 8.1", "कक्षा 10 गणित · अध्याय 8: त्रिकोणमिति का परिचय · 11 प्रश्न (त्रिकोणमितीय अनुपात)", EX81, (BASE, "अध्याय 8"), (BASE + "exercise-8-2/", "प्रश्नावली 8.2"))
page(BASE, 8, CH, "exercise-8-2", "प्रश्नावली 8.2", "कक्षा 10 गणित · अध्याय 8: त्रिकोणमिति का परिचय · 4 प्रश्न (विशिष्ट कोणों के अनुपात)", EX82, (BASE + "exercise-8-1/", "प्रश्नावली 8.1"), (BASE + "exercise-8-3/", "प्रश्नावली 8.3"))
page(BASE, 8, CH, "exercise-8-3", "प्रश्नावली 8.3", "कक्षा 10 गणित · अध्याय 8: त्रिकोणमिति का परिचय · 4 प्रश्न (त्रिकोणमितीय सर्वसमिकाएँ)", EX83, (BASE + "exercise-8-2/", "प्रश्नावली 8.2"), (BASE, "अध्याय 8"))
print("ok")
