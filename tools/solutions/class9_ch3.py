#!/usr/bin/env python3
"""Class 9 Maths, Chapter 3 (निर्देशांक ज्यामिति): Exercises 3.1 and 3.2, Hindi medium.
Rationalised book (reprint 2025-26): the old exercise 3.1 (lamp / street plan) was removed, so the old 3.2 is 3.1
and the old 3.3 is 3.2. Figure 3.14 redrawn from the textbook.
User rules: every smallest step shown (class 9 level); figures exact and high quality; maths in LaTeX.
Run from repo root: python3 tools/solutions/class9_ch3.py
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from common import *  # noqa
from mixed_cells import *  # noqa

BASE = "/hi/class-09/maths/chapter-03/"
CH = "निर्देशांक ज्यामिति"
BOARDS9 = ("यह हल <b>MP Board (MPBSE)</b> कक्षा 9 गणित की पाठ्यपुस्तक के अध्याय 3 ‘निर्देशांक ज्यामिति’ "
           "(NCERT पाठ्यपुस्तक, पुनर्मुद्रण 2025-26) के अनुसार है।")
EXTRA_CSS = """
.tw{overflow-x:auto;-webkit-overflow-scrolling:touch;max-width:100%;margin:8px 0 10px}
.st{border-collapse:collapse;font-variant-numeric:tabular-nums;background:#fff;font-size:15px}
.st th,.st td{border:1px solid #d5dbe8;padding:4px 8px;text-align:center}
.st th{background:var(--l);font-weight:700}
.fig{margin:10px 0;text-align:center}.fig svg{width:100%;height:auto;background:#fbfcff;border:1px solid #e3e8f4;border-radius:12px}
.fig .cap{font-size:.85em;color:#5a6275;margin-top:4px}
.tp{background:#fff4ec;border-left:4px solid #e8711a;border-radius:8px;padding:5px 10px;margin:6px 0;font-size:.95em}
.why{font-size:.95em;color:#36405a;margin:2px 0 6px}
.ans .al{margin:10px 0}
"""
INK, RED, GRN, ORG, BLU = "#1d3a8a", "#b4232a", "#0f7a4c", "#c2410c", "#1769c2"


def tp(t):
    return f"<div class='tp'>{t}</div>"


def why(t):
    return f"<p class='why'>{t}</p>"


def table(head, rows):
    h = "".join(f"<th>{x}</th>" for x in head)
    b = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f"<div class='tw'><table class='st'><tr>{h}</tr>{b}</table></div>"


def mn(v):
    """number for SVG text with a true minus sign"""
    s = f"{v:g}"
    return s.replace("-", "−")


def plane(xr, yr, u, pts, cap, quads=False, drops=True, ylab_every=1):
    """Cartesian plane. pts: (x, y, name, dx, dy, colour). Dashed perpendiculars from each point to both axes."""
    pad = 34
    W = int((xr[1] - xr[0]) * u + 2 * pad)
    H = int((yr[1] - yr[0]) * u + 2 * pad)
    sx = lambda x: pad + (x - xr[0]) * u
    sy = lambda y: pad + (yr[1] - y) * u
    g = []
    for k in range(xr[0], xr[1] + 1):
        g.append(f"<line x1='{sx(k):.1f}' y1='{sy(yr[0]):.1f}' x2='{sx(k):.1f}' y2='{sy(yr[1]):.1f}' stroke='#dbe6f5' stroke-width='1'/>")
    for k in range(yr[0], yr[1] + 1):
        g.append(f"<line x1='{sx(xr[0]):.1f}' y1='{sy(k):.1f}' x2='{sx(xr[1]):.1f}' y2='{sy(k):.1f}' stroke='#dbe6f5' stroke-width='1'/>")
    mk = ("<defs><marker id='ar' viewBox='0 0 10 10' refX='8' refY='5' markerWidth='10' markerHeight='10' markerUnits='userSpaceOnUse' orient='auto-start-reverse'>"
          "<path d='M0,0 L10,5 L0,10 z' fill='#222'/></marker></defs>")
    ax = (f"<line x1='{sx(xr[0]) - 14:.1f}' y1='{sy(0):.1f}' x2='{sx(xr[1]) + 14:.1f}' y2='{sy(0):.1f}' stroke='#222' stroke-width='1.6' marker-start='url(#ar)' marker-end='url(#ar)'/>"
          f"<line x1='{sx(0):.1f}' y1='{sy(yr[0]) + 14:.1f}' x2='{sx(0):.1f}' y2='{sy(yr[1]) - 14:.1f}' stroke='#222' stroke-width='1.6' marker-start='url(#ar)' marker-end='url(#ar)'/>")
    t = []
    t.append(f"<text x='{sx(xr[1]) + 14:.1f}' y='{sy(0) - 8:.1f}' font-size='14' font-weight='700' text-anchor='end' font-style='italic'>X</text>")
    t.append(f"<text x='{sx(xr[0]) - 14:.1f}' y='{sy(0) - 8:.1f}' font-size='14' font-weight='700' font-style='italic'>X′</text>")
    t.append(f"<text x='{sx(0) + 8:.1f}' y='{sy(yr[1]) - 8:.1f}' font-size='14' font-weight='700' font-style='italic'>Y</text>")
    t.append(f"<text x='{sx(0) + 8:.1f}' y='{sy(yr[0]) + 18:.1f}' font-size='14' font-weight='700' font-style='italic'>Y′</text>")
    t.append(f"<text x='{sx(0) - 5:.1f}' y='{sy(0) + 15:.1f}' font-size='12' font-weight='700' text-anchor='end' font-style='italic'>O</text>")
    for k in range(xr[0], xr[1] + 1):
        if k:
            t.append(f"<line x1='{sx(k):.1f}' y1='{sy(0) - 3:.1f}' x2='{sx(k):.1f}' y2='{sy(0) + 3:.1f}' stroke='#222'/>")
            t.append(f"<text x='{sx(k):.1f}' y='{sy(0) + 15:.1f}' font-size='11' text-anchor='middle' fill='#333' stroke='#fbfcff' stroke-width='4' paint-order='stroke'>{mn(k)}</text>")
    for k in range(yr[0], yr[1] + 1):
        if k and k % ylab_every == 0:
            t.append(f"<line x1='{sx(0) - 3:.1f}' y1='{sy(k):.1f}' x2='{sx(0) + 3:.1f}' y2='{sy(k):.1f}' stroke='#222'/>")
            t.append(f"<text x='{sx(0) - 6:.1f}' y='{sy(k) + 4:.1f}' font-size='11' text-anchor='end' fill='#333' stroke='#fbfcff' stroke-width='4' paint-order='stroke'>{mn(k)}</text>")
    q = []
    if quads:
        for (qx, qy, nm, sg) in ((0.5, 0.5, "I चतुर्थांश", "(+, +)"), (-0.5, 0.5, "II चतुर्थांश", "(−, +)"),
                                 (-0.5, -0.5, "III चतुर्थांश", "(−, −)"), (0.5, -0.5, "IV चतुर्थांश", "(+, −)")):
            cx = sx(0) + qx * (xr[1] - xr[0]) * u * 0.5
            cy = sy(0) - qy * (yr[1] - yr[0]) * u * 0.5
            q.append(f"<text x='{cx:.1f}' y='{cy - 4:.1f}' font-size='14' font-weight='700' text-anchor='middle' fill='{ORG}'>{nm}</text>"
                     f"<text x='{cx:.1f}' y='{cy + 15:.1f}' font-size='13' text-anchor='middle' fill='{ORG}'>{sg}</text>")
    P = []
    for x, y, nm, dx, dy, col in pts:
        if drops and x != 0 and y != 0:
            P.append(f"<line x1='{sx(x):.1f}' y1='{sy(y):.1f}' x2='{sx(x):.1f}' y2='{sy(0):.1f}' stroke='{col}' stroke-width='1.4' stroke-dasharray='5 4'/>")
            P.append(f"<line x1='{sx(x):.1f}' y1='{sy(y):.1f}' x2='{sx(0):.1f}' y2='{sy(y):.1f}' stroke='{col}' stroke-width='1.4' stroke-dasharray='5 4'/>")
    for x, y, nm, dx, dy, col in pts:
        P.append(f"<circle cx='{sx(x):.1f}' cy='{sy(y):.1f}' r='4' fill='{col}'/>")
        P.append(f"<text x='{sx(x) + dx:.1f}' y='{sy(y) + dy:.1f}' font-size='13' font-weight='700' fill='{col}' text-anchor='middle'>{nm}</text>")
    drops_ = [x for x in P if "<line" in x]
    rest = [x for x in P if "<line" not in x]
    body = mk + "".join(g) + "".join(q) + "".join(drops_) + ax + "".join(t) + "".join(rest)
    return (f"<div class='fig'><svg viewBox='0 0 {W} {H}' role='img' aria-label='{cap}' style='max-width:{max(W, 420)}px' "
            f"font-family='Noto Sans, Noto Sans Devanagari, sans-serif'>{body}</svg><div class='cap'>{cap}</div></div>")


QUAD = table(["चतुर्थांश", "भुज " + m("x"), "कोटि " + m("y"), "उदाहरण"],
             [["I", "+", "+", m("(2, 3)")], ["II", "−", "+", m("(-2, 3)")], ["III", "−", "−", m("(-2, -3)")], ["IV", "+", "−", m("(2, -3)")]])
AXES = table(["बिंदु कहाँ", "पहचान"], [["x-अक्ष पर", "कोटि " + m("y = 0") + ", जैसे " + m("(4, 0)")], ["y-अक्ष पर", "भुज " + m("x = 0") + ", जैसे " + m("(0, 4)")],
                                      ["मूल बिंदु", m("(0, 0)")]])

# =====================================================================
# Exercise 3.1
# =====================================================================
E1 = []
s = part("(i) क्षैतिज और ऊर्ध्वाधर रेखाओं के नाम",
         p("कार्तीय तल में किसी बिंदु की स्थिति दो परस्पर लंब संख्या रेखाओं से तय होती है:")
         + table(["रेखा", "नाम"], [["क्षैतिज रेखा " + m("X'OX"), m("x") + "-अक्ष"], ["ऊर्ध्वाधर रेखा " + m("Y'OY"), m("y") + "-अक्ष"]])
         + ans("क्षैतिज रेखा: " + m("x") + "-अक्ष; ऊर्ध्वाधर रेखा: " + m("y") + "-अक्ष"))
s += part("(ii) तल के प्रत्येक भाग के नाम",
          p("दोनों अक्ष तल को चार भागों में बाँटते हैं। हर भाग को <b>चतुर्थांश</b> कहते हैं। " + m("OX") + " से वामावर्त (घड़ी की सुई की उलटी दिशा में) गिनते हैं:")
          + plane((-5, 5), (-4, 4), 34, [], "चित्र 1: चार चतुर्थांश और उनमें निर्देशांकों के चिह्न", quads=True)
          + QUAD + ans("प्रथम (I), द्वितीय (II), तृतीय (III) और चतुर्थ (IV) चतुर्थांश"))
s += part("(iii) दोनों रेखाओं का प्रतिच्छेद बिंदु",
          p("दोनों अक्ष बिंदु O पर काटते हैं। वहाँ " + m("x = 0") + " और " + m("y = 0") + " होता है।") + ans("मूल बिंदु O, जिसके निर्देशांक " + m("(0, 0)") + " हैं"))
s += ans("(i) " + m("x") + "-अक्ष और " + m("y") + "-अक्ष (ii) चार चतुर्थांश: I, II, III, IV (iii) मूल बिंदु " + m("O(0, 0)"))
E1.append((qt("निम्नलिखित प्रश्नों में से प्रत्येक प्रश्न का उत्तर दीजिए: (i) कार्तीय तल में किसी बिंदु की स्थिति निर्धारित करने वाली क्षैतिज और ऊर्ध्वाधर रेखाओं के क्या नाम हैं? "
              "(ii) इन दो रेखाओं से बने तल के प्रत्येक भाग के नाम बताइए। (iii) उस बिंदु का नाम बताइए जहाँ ये दो रेखाएँ प्रतिच्छेदित होती हैं।"), s))

F314 = [(-5, 2, "B", -10, -6, BLU), (6, 2, "D", 11, -5, BLU), (0, 5, "L", 11, 4, GRN), (-3, 0, "M", -2, -10, GRN), (-5, -3, "H", -11, 12, RED),
        (2, -4, "G", 11, 12, RED), (-3, -5, "E", -11, 12, ORG), (5, -5, "C", 11, 12, ORG)]
fig314 = plane((-6, 7), (-6, 6), 28, F314, "आकृति 3.14 (पाठ्यपुस्तक से पुनः बनाई गई)")
RULE = formula("निर्देशांक पढ़ना", "बिंदु से " + m("x") + "-अक्ष पर लंब डालें — जहाँ मिले वह <b>भुज</b> (" + m("x") + ")। बिंदु से " + m("y")
               + "-अक्ष पर लंब डालें — जहाँ मिले वह <b>कोटि</b> (" + m("y") + ")। निर्देशांक = " + m("(\\text{x}, \\text{y})").replace("\\text{x}", "x").replace("\\text{y}", "y") + " = (भुज, कोटि)।")


def read(nm, x, y):
    side = "दाईं" if x > 0 else "बाईं"
    up = "ऊपर" if y > 0 else "नीचे"
    h = p(f"बिंदु {nm} से " + m("x") + f"-अक्ष पर लंब (बिंदुदार रेखा) डालने पर वह " + m(str(x)) + f" पर मिलता है (O से {side} ओर {abs(x)} एकक)।")
    h += eqs(("\\text{भुज}".replace("\\text{भुज}", "x"), str(x)))
    h += p(f"बिंदु {nm} से " + m("y") + f"-अक्ष पर लंब डालने पर वह " + m(str(y)) + f" पर मिलता है (O से {up} {abs(y)} एकक)।")
    h += eqs(("y", str(y)))
    h += lines(f"{nm}", f"(x, y)", f"({x}, {y})")
    return h


s = RULE + fig314
s += part("(i) B के निर्देशांक", read("B", -5, 2) + ans(m("B(-5, 2)")))
s += part("(ii) C के निर्देशांक", read("C", 5, -5) + ans(m("C(5, -5)")))
s += part("(iii) निर्देशांक " + m("(-3, -5)") + " वाला बिंदु",
          p(m("x = -3") + ": O से " + m("x") + "-अक्ष पर बाईं ओर 3 एकक चलें।") + p(m("y = -5") + ": वहाँ से नीचे 5 एकक चलें।")
          + p("इस स्थान पर आकृति में बिंदु E है।") + ans("बिंदु E"))
s += part("(iv) निर्देशांक " + m("(2, -4)") + " वाला बिंदु",
          p(m("x = 2") + ": O से " + m("x") + "-अक्ष पर दाईं ओर 2 एकक चलें।") + p(m("y = -4") + ": वहाँ से नीचे 4 एकक चलें।")
          + p("इस स्थान पर आकृति में बिंदु G है।") + ans("बिंदु G"))
s += part("(v) D का भुज", p("बिंदु D से " + m("x") + "-अक्ष पर लंब डालने पर वह " + m("6") + " पर मिलता है।") + ans("D का भुज = 6"))
s += part("(vi) बिंदु H की कोटि", p("बिंदु H से " + m("y") + "-अक्ष पर लंब डालने पर वह " + m("-3") + " पर मिलता है।") + ans("H की कोटि = −3"))
s += part("(vii) बिंदु L के निर्देशांक", p("बिंदु L, " + m("y") + "-अक्ष पर है, इसलिए उसका भुज " + m("x = 0") + " है। वह O से ऊपर 5 एकक पर है, अतः " + m("y = 5") + "।")
          + lines("L", "(x, y)", "(0, 5)") + ans(m("L(0, 5)")))
s += part("(viii) बिंदु M के निर्देशांक", p("बिंदु M, " + m("x") + "-अक्ष पर है, इसलिए उसकी कोटि " + m("y = 0") + " है। वह O से बाईं ओर 3 एकक पर है, अतः " + m("x = -3") + "।")
          + lines("M", "(x, y)", "(-3, 0)") + ans(m("M(-3, 0)")))
s += ans("(i) " + m("(-5, 2)") + " (ii) " + m("(5, -5)") + " (iii) E (iv) G (v) 6 (vi) −3 (vii) " + m("(0, 5)") + " (viii) " + m("(-3, 0)"))
E1.append((qt("आकृति 3.14 देखकर निम्नलिखित को लिखिए: (i) B के निर्देशांक (ii) C के निर्देशांक (iii) निर्देशांक " + m("(-3, -5)") + " द्वारा पहचाना गया बिंदु "
              "(iv) निर्देशांक " + m("(2, -4)") + " द्वारा पहचाना गया बिंदु (v) D का भुज (vi) बिंदु H की कोटि (vii) बिंदु L के निर्देशांक (viii) बिंदु M के निर्देशांक"), s))

# =====================================================================
# Exercise 3.2
# =====================================================================
E2 = []
P1 = [(-2, 4, "A", 0, -10, BLU), (3, -1, "B", 12, 14, RED), (-1, 0, "C", 0, -10, GRN), (1, 2, "D", 11, -6, BLU), (-3, -5, "E", -12, 13, ORG)]
s = formula("चतुर्थांश पहचानना", "भुज और कोटि के चिह्न देखें:") + QUAD + AXES
rows = []
for (x, y, nm, *_), where in zip(P1, ["II चतुर्थांश", "IV चतुर्थांश", "ऋणात्मक " + m("x") + "-अक्ष", "I चतुर्थांश", "III चतुर्थांश"]):
    sx_ = "+" if x > 0 else ("−" if x < 0 else "0")
    sy_ = "+" if y > 0 else ("−" if y < 0 else "0")
    rows.append([f"{nm}" + m(f"({x}, {y})"), m(str(x)) + f" ({sx_})", m(str(y)) + f" ({sy_})", where])
s += p("हर बिंदु के भुज और कोटि का चिह्न देखकर:")
s += table(["बिंदु", "भुज x", "कोटि y", "स्थान"], rows)
s += p("<b>आलेखन से सत्यापन</b> (हर बिंदु के लिए: पहले भुज के अनुसार " + m("x") + "-अक्ष पर चलें, फिर कोटि के अनुसार ऊपर/नीचे):")
for x, y, nm, *_ in P1:
    mv1 = "दाईं" if x > 0 else "बाईं"
    mv2 = "ऊपर" if y > 0 else "नीचे"
    t1 = f"O से " + m("x") + f"-अक्ष पर {mv1} ओर {abs(x)} एकक"
    t2 = (f", फिर {mv2} {abs(y)} एकक" if y else ", ऊपर-नीचे नहीं चलना (" + m("y = 0") + ")")
    s += tp(f"{nm}" + m(f"({x}, {y})") + ": " + t1 + t2 + "।")
s += plane((-5, 5), (-6, 5), 30, P1, "चित्र 2: बिंदु A, B, C, D, E का आलेखन")
s += ans(m("(-2, 4)") + ": II चतुर्थांश; " + m("(3, -1)") + ": IV चतुर्थांश; " + m("(-1, 0)") + ": ऋणात्मक " + m("x") + "-अक्ष पर; " + m("(1, 2)") + ": I चतुर्थांश; " + m("(-3, -5)") + ": III चतुर्थांश")
E2.append(("किस चतुर्थांश में या किस अक्ष पर बिंदु " + m("(-2, 4),\\ (3, -1),\\ (-1, 0),\\ (1, 2)") + " और " + m("(-3, -5)") + " स्थित हैं? कार्तीय तल पर इनका स्थान निर्धारण करके अपने उत्तर सत्यापित कीजिए।", s))

T2 = [(-2, 8, "P", -11, -4, BLU), (-1, 7, "Q", -11, -4, GRN), (0, -1.25, "R", 12, 14, RED), (1, 3, "S", 11, -6, ORG), (3, -1, "T", 11, 14, BLU)]
s = p("पैमाना: दोनों अक्षों पर <b>1 सेमी = 1 एकक</b> (" + m("y") + " का सबसे बड़ा मान 8 है, इसलिए " + m("y") + "-अक्ष पर 8 तक अंकित करते हैं)।")
s += table([m("x"), "−2", "−1", "0", "1", "3"], [[m("y"), "8", "7", "−1.25", "3", "−1"]])
s += p("सारणी से बिंदु (क्रमित युग्म) बनाते हैं और हर बिंदु का स्थान तय करते हैं:")
rows = []
for x, y, nm, *_ in T2:
    yv = f"{y:g}"
    mv1 = "—" if x == 0 else (f"दाईं ओर {abs(x)}" if x > 0 else f"बाईं ओर {abs(x)}")
    mv2 = f"ऊपर {abs(y):g}" if y > 0 else f"नीचे {abs(y):g}"
    rows.append([nm, m(f"({x}, {yv})"), mv1, mv2])
s += table(["बिंदु", "निर्देशांक", "x-अक्ष पर", "फिर"], rows)
s += why("R" + m("(0, -1.25)") + " का भुज 0 है, इसलिए यह " + m("y") + "-अक्ष पर ही, O से नीचे 1.25 एकक (" + m("-1") + " और " + m("-2") + " के बीच, " + m("-1") + " से एक-चौथाई नीचे) पर है।")
s += plane((-4, 4), (-3, 9), 30, T2, "चित्र 3: सारणी के बिंदुओं P, Q, R, S, T का आलेखन")
s += ans("बिंदु " + m("P(-2, 8),\\ Q(-1, 7),\\ R(0, -1.25),\\ S(1, 3),\\ T(3, -1)") + " आलेख में दिखाए गए हैं।")
E2.append(("अक्षों पर दूरी का उपयुक्त एकक लेकर नीचे सारणी में दिए गए बिंदुओं को तल पर आलेखित कीजिए:"
           + table([m("x"), "−2", "−1", "0", "1", "3"], [[m("y"), "8", "7", "−1.25", "3", "−1"]]), s))

import re as _re
ALL = [("exercise-3-1", "प्रश्नावली 3.1", "कार्तीय पद्धति", E1), ("exercise-3-2", "प्रश्नावली 3.2", "बिंदु आलेखित करना", E2)]
for _, _, _, E in ALL:
    for _q, _sol in E:
        for _t in _re.findall(r"\\\((.+?)\\\)", _q + _sol):
            assert not _re.search(r"[\u0900-\u097F]", _t), ("Devanagari in TeX", _t)
for i, (slug, title, topic, E) in enumerate(ALL):
    prev = (BASE + ALL[i - 1][0] + "/", ALL[i - 1][1]) if i else ("/hi/class-09/maths/chapter-02/exercise-2-4/", "प्रश्नावली 2.4")
    nxt = (BASE + ALL[i + 1][0] + "/", ALL[i + 1][1]) if i + 1 < len(ALL) else ("/hi/class-09/maths/chapter-04/exercise-4-1/", "प्रश्नावली 4.1")
    page(BASE, 3, CH, slug, title, f"कक्षा 9 गणित · अध्याय 3: निर्देशांक ज्यामिति · {len(E)} प्रश्न ({topic})", E,
         prev, nxt, css=CSS + EXTRA_CSS, boards=BOARDS9)
print("ok")
