#!/usr/bin/env python3
"""Class 9 Maths, Chapter 1 (संख्या पद्धति): Exercises 1.1 to 1.5, Hindi medium.
Question text as in the MP Board / NCERT Hindi textbook (ihmh101, reprint 2025-26, rationalised).
User rules (2026-11-05): formula written where it is used; numbers under a root are factorised first;
transposition and cross-multiplication shown; bracket products multiplied term by term;
accurate figures with right-angle marks, arcs and non-overlapping labels.
Run from repo root: python3 tools/solutions/class9_ch1.py
"""
import sys, pathlib, math
from fractions import Fraction as F
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from common import *  # noqa
from mixed_cells import *  # noqa

BASE = "/hi/class-09/maths/chapter-01/"
CH = "संख्या पद्धति"
BOARDS9 = ("यह हल <b>MP Board (MPBSE)</b> कक्षा 9 गणित की पाठ्यपुस्तक के अध्याय 1 ‘संख्या पद्धति’ "
           "(NCERT पाठ्यपुस्तक, पुनर्मुद्रण 2025-26) के अनुसार है।")

EXTRA_CSS = """
.tw{overflow-x:auto;-webkit-overflow-scrolling:touch;max-width:100%;margin:8px 0 10px}
.st{border-collapse:collapse;font-variant-numeric:tabular-nums;background:#fff;font-size:15px}
.st th,.st td{border:1px solid #d5dbe8;padding:4px 9px;text-align:center;white-space:nowrap}
.st th{background:var(--l);font-weight:700}
.st tr.hl td{background:#fff3c4}
.tp{background:#fff4ec;border-left:4px solid #e8711a;border-radius:8px;padding:5px 10px;margin:6px 0;font-size:.95em}
.why{font-size:.95em;color:#36405a;margin:2px 0 6px}
.fig{margin:10px 0;text-align:center}.fig svg{width:100%;height:auto;background:#fbfcff;border:1px solid #e3e8f4;border-radius:12px}
.fig .cap{font-size:.85em;color:#5a6275;margin-top:4px}
.ans .al{margin:10px 0}.eq{row-gap:9px}
"""


# ---------------- helpers ----------------
def d(a, b):
    return f"\\dfrac{{{a}}}{{{b}}}"


def M(a, b):
    return m(d(a, b))


def tp(t):
    """पक्षांतर / तिरछा गुणा note, shown as its own orange line."""
    return f"<div class='tp'>{t}</div>"


def why(t):
    return f"<p class='why'>{t}</p>"


def fact_root(n, k=2):
    """Prime factorisation of n written out, grouped for a square (k=2) or cube (k=3) root."""
    fs = factors(n)
    groups, out = [], []
    from collections import Counter
    c = Counter(fs)
    inside, outside = 1, 1
    for pr in sorted(c):
        q_, r_ = divmod(c[pr], k)
        outside *= pr ** q_
        inside *= pr ** r_
    return fs, outside, inside


def root_steps(n, k=2):
    """√n or ∛n: factorise first (user rule 2), then pair/triple, then the value."""
    fs, out_, in_ = fact_root(n, k)
    rt = "\\sqrt" if k == 2 else "\\sqrt[3]"
    prod = "\\times ".join(map(str, fs))
    from collections import Counter
    c = Counter(fs)
    grp = []
    for pr in sorted(c):
        q_, r_ = divmod(c[pr], k)
        grp += [f"({'\\times '.join([str(pr)] * k)})"] * q_ + [str(pr)] * r_
    rows = [f"{rt}{{{prod}}}", f"{rt}{{{'\\times '.join(grp)}}}"]
    if in_ == 1:
        rows.append(str(out_))
    else:
        rows.append(f"{out_}{rt}{{{in_}}}" if out_ > 1 else f"{rt}{{{in_}}}")
    return ladders(n) + lines(f"{rt}{{{n}}}", *rows)


def div_table(a, b, steps, note_rep=None):
    """Long division a ÷ b shown as a table of steps: dividend, quotient digit, remainder."""
    q0, r = divmod(a, b)
    rows = [f"<tr><td>{a}</td><td>{q0}</td><td>{r}</td></tr>"]
    seen = {}
    digits = []
    for i in range(steps):
        x = r * 10
        dg, r = divmod(x, b)
        digits.append(dg)
        hl = " class='hl'" if note_rep and i in note_rep else ""
        rows.append(f"<tr{hl}><td>{x}</td><td>{dg}</td><td>{r}</td></tr>")
        if r == 0:
            break
    head = f"<tr><th>भाज्य</th><th>÷ {b} से भागफल अंक</th><th>शेषफल</th></tr>"
    return (f"<div class='tw'><table class='st'>{head}{''.join(rows)}</table></div>"
            "<p class='why'>(हर चरण में पिछले शेषफल के आगे 0 लगाकर, अर्थात 10 से गुणा करके, फिर से भाग दिया गया है।)</p>"), q0, digits


def svg(W, H, body, cap):
    return (f"<div class='fig'><svg viewBox='0 0 {W} {H}' role='img' aria-label='{cap}' "
            f"style='max-width:{W}px' font-family='Noto Sans, Noto Sans Devanagari, sans-serif'>{body}</svg>"
            f"<div class='cap'>{cap}</div></div>")


INK, RED, GRN, ORG = "#1d3a8a", "#b4232a", "#0f7a4c", "#c2410c"


def L(x1, y1, x2, y2, c=INK, w=2, dash=None):
    ds = f" stroke-dasharray='{dash}'" if dash else ""
    return f"<line x1='{x1:.1f}' y1='{y1:.1f}' x2='{x2:.1f}' y2='{y2:.1f}' stroke='{c}' stroke-width='{w}'{ds} stroke-linecap='round'/>"


def Tx(x, y, t, c="#111", s=14, w=700, a="middle"):
    return f"<text x='{x:.1f}' y='{y:.1f}' font-size='{s}' font-weight='{w}' fill='{c}' text-anchor='{a}'>{t}</text>"


def dot(x, y, c=INK):
    return f"<circle cx='{x:.1f}' cy='{y:.1f}' r='3' fill='{c}'/>"


def rmark(px, py, u1, u2, s=9):
    """Right-angle square at P between unit directions u1 and u2 (screen coordinates)."""
    a = (px + u1[0] * s, py + u1[1] * s)
    b = (px + (u1[0] + u2[0]) * s, py + (u1[1] + u2[1]) * s)
    c = (px + u2[0] * s, py + u2[1] * s)
    return (f"<polyline points='{a[0]:.1f},{a[1]:.1f} {b[0]:.1f},{b[1]:.1f} {c[0]:.1f},{c[1]:.1f}' "
            f"fill='none' stroke='{RED}' stroke-width='1.6'/>")


def arc(cx, cy, r, a1, a2, c=GRN, dash="5 4"):
    """Arc of circle (cx, cy, r) from angle a1 to a2 (degrees, maths sense: anticlockwise, y up)."""
    x1, y1 = cx + r * math.cos(math.radians(a1)), cy - r * math.sin(math.radians(a1))
    x2, y2 = cx + r * math.cos(math.radians(a2)), cy - r * math.sin(math.radians(a2))
    large = 1 if abs(a2 - a1) > 180 else 0
    sweep = 0 if a2 > a1 else 1
    return (f"<path d='M {x1:.1f} {y1:.1f} A {r:.1f} {r:.1f} 0 {large} {sweep} {x2:.1f} {y2:.1f}' "
            f"fill='none' stroke='{c}' stroke-width='1.8' stroke-dasharray='{dash}'/>")


def axis(x0, x1, y, ticks, px, labels=True):
    """Number line from x0 to x1 (pixels) with arrow heads and integer ticks."""
    g = [L(x0, y, x1, y, "#333", 1.8),
         f"<path d='M {x1:.1f} {y} l -8 -4 v 8 z' fill='#333'/><path d='M {x0:.1f} {y} l 8 -4 v 8 z' fill='#333'/>"]
    for t in ticks:
        g.append(L(px(t), y - 5, px(t), y + 5, "#333", 1.5))
        if labels:
            g.append(Tx(px(t), y + 21, str(t).replace("-", "−"), "#333", 13, 600))
    return "".join(g)


# =====================================================================
# Exercise 1.1
# =====================================================================
E1 = []
DEF = formula("परिमेय संख्या", "जिस संख्या को " + M("p", "q") + " के रूप में लिखा जा सके, जहाँ p और q पूर्णांक हैं और " + m("q \\neq 0") + ", वह परिमेय संख्या है।")

s = given("संख्या 0", "क्या 0 परिमेय है, क्या यह " + M("p", "q") + " रूप में लिखी जा सकती है")
s += DEF
s += p("0 को ऐसे लिखा जा सकता है:")
s += lines("0", d(0, 1), d(0, 2), d(0, -3), d(0, 5))
s += why("यहाँ p = 0 (एक पूर्णांक) और q = 1, 2, −3, 5 आदि (शून्येतर पूर्णांक) हैं। p = 0 लेकर q कोई भी शून्येतर पूर्णांक हो सकता है।")
s += ans("हाँ, 0 एक परिमेय संख्या है, क्योंकि " + m("0 = \\dfrac{0}{1}") + " (या " + m("\\dfrac{0}{q}") + ", जहाँ q ≠ 0 पूर्णांक है)।")
E1.append(("क्या शून्य एक परिमेय संख्या है? क्या इसे आप " + M("p", "q") + " के रूप में लिख सकते हैं, जहाँ p और q पूर्णांक हैं और " + m("q \\neq 0") + " है?", s))

# Q2: 3 and 4, multiply by (6+1)/(6+1)
assert all(F(21 + i, 7) > 3 and F(21 + i, 7) < 4 for i in range(1, 7))
s = given("दो परिमेय संख्याएँ 3 और 4", "इनके बीच छः परिमेय संख्याएँ")
s += p("छः संख्याएँ चाहिए, इसलिए 3 और 4 के अंश तथा हर को 6 + 1 = 7 से गुणा करते हैं:")
s += lines("3", d("3 \\times 7", "1 \\times 7"), d(21, 7))
s += lines("4", d("4 \\times 7", "1 \\times 7"), d(28, 7))
s += p("अब " + M(21, 7) + " और " + M(28, 7) + " के बीच, हर 7 रखकर अंश 22, 23, 24, 25, 26, 27 लेते हैं:")
s += lines("\\text{परिमेय संख्याएँ}", "\\dfrac{22}{7},\\ \\dfrac{23}{7},\\ \\dfrac{24}{7},\\ \\dfrac{25}{7},\\ \\dfrac{26}{7},\\ \\dfrac{27}{7}")
s += why("जाँच: " + m("\\dfrac{21}{7} < \\dfrac{22}{7} < \\dots < \\dfrac{27}{7} < \\dfrac{28}{7}") + ", अर्थात सभी 3 और 4 के बीच हैं ✔")
s += ans(m("\\dfrac{22}{7},\\ \\dfrac{23}{7},\\ \\dfrac{24}{7},\\ \\dfrac{25}{7},\\ \\dfrac{26}{7},\\ \\dfrac{27}{7}") + " (और भी अनेक उत्तर संभव हैं)")
E1.append(("3 और 4 के बीच में छः परिमेय संख्याएँ ज्ञात कीजिए।", s))

# Q3: 3/5 and 4/5, multiply by 6/6
assert all(F(3, 5) < F(18 + i, 30) < F(4, 5) for i in range(1, 6))
s = given("परिमेय संख्याएँ " + M(3, 5) + " और " + M(4, 5), "इनके बीच पाँच परिमेय संख्याएँ")
s += p("पाँच संख्याएँ चाहिए, इसलिए अंश और हर दोनों को 5 + 1 = 6 से गुणा करते हैं:")
s += lines(d(3, 5), d("3 \\times 6", "5 \\times 6"), d(18, 30))
s += lines(d(4, 5), d("4 \\times 6", "5 \\times 6"), d(24, 30))
s += p("अब " + M(18, 30) + " और " + M(24, 30) + " के बीच अंश 19, 20, 21, 22, 23 लेते हैं:")
s += lines("\\text{परिमेय संख्याएँ}", "\\dfrac{19}{30},\\ \\dfrac{20}{30},\\ \\dfrac{21}{30},\\ \\dfrac{22}{30},\\ \\dfrac{23}{30}")
s += why("सरल रूप में: " + m("\\dfrac{20}{30} = \\dfrac{2}{3}") + " और " + m("\\dfrac{21}{30} = \\dfrac{7}{10}") + "।")
s += ans(m("\\dfrac{19}{30},\\ \\dfrac{2}{3},\\ \\dfrac{7}{10},\\ \\dfrac{22}{30} = \\dfrac{11}{15},\\ \\dfrac{23}{30}"))
E1.append(("" + M(3, 5) + " और " + M(4, 5) + " के बीच पाँच परिमेय संख्याएँ ज्ञात कीजिए।", s))

s = p("याद रखें: प्राकृत संख्याएँ N = {1, 2, 3, …}, पूर्ण संख्याएँ W = {0, 1, 2, 3, …}, पूर्णांक Z = {…, −2, −1, 0, 1, 2, …}।")
s += part("(i)", ans("<b>सत्य</b>") + why("पूर्ण संख्याएँ = 0 और सभी प्राकृत संख्याएँ। अतः हर प्राकृत संख्या (1, 2, 3, …) पूर्ण संख्याओं में शामिल है।"))
s += part("(ii)", ans("<b>असत्य</b>") + why("ऋणात्मक पूर्णांक पूर्ण संख्या नहीं होते। उदाहरण: −3 एक पूर्णांक है, पर पूर्ण संख्या नहीं।"))
s += part("(iii)", ans("<b>असत्य</b>") + why("उदाहरण: " + m("\\dfrac{1}{2}") + " परिमेय संख्या है, पर पूर्ण संख्या नहीं।"))
s += ans("(i) सत्य (ii) असत्य (iii) असत्य")
E1.append((qt("नीचे दिए गए कथन सत्य हैं या असत्य? कारण के साथ अपने उत्तर दीजिए। "
              "(i) प्रत्येक प्राकृत संख्या एक पूर्ण संख्या होती है। (ii) प्रत्येक पूर्णांक एक पूर्ण संख्या होती है। "
              "(iii) प्रत्येक परिमेय संख्या एक पूर्ण संख्या होती है।"), s))
assert len(E1) == 4

# =====================================================================
# Exercise 1.2
# =====================================================================
E2 = []
s = p("याद रखें: वास्तविक संख्याएँ = सभी परिमेय संख्याएँ + सभी अपरिमेय संख्याएँ। संख्या रेखा का प्रत्येक बिंदु एक वास्तविक संख्या है।")
s += part("(i)", ans("<b>सत्य</b>") + why("वास्तविक संख्याओं में परिमेय और अपरिमेय दोनों आती हैं, इसलिए हर अपरिमेय संख्या वास्तविक है।"))
s += part("(ii)", ans("<b>असत्य</b>") + why("ऋणात्मक संख्याएँ किसी प्राकृत संख्या का (धनात्मक) वर्गमूल नहीं हो सकतीं। उदाहरण: संख्या रेखा का बिंदु −3 किसी " + m("\\sqrt{m}") + " के बराबर नहीं है।"))
s += part("(iii)", ans("<b>असत्य</b>") + why("उदाहरण: 2 वास्तविक संख्या है, पर परिमेय है (अपरिमेय नहीं)।"))
s += ans("(i) सत्य (ii) असत्य (iii) असत्य")
E2.append((qt("नीचे दिए गए कथन सत्य हैं या असत्य हैं। कारण के साथ अपने उत्तर दीजिए। "
              "(i) प्रत्येक अपरिमेय संख्या एक वास्तविक संख्या होती है। "
              "(ii) संख्या रेखा का प्रत्येक बिंदु " + m("\\sqrt{m}") + " के रूप का होता है, जहाँ m एक प्राकृत संख्या है। "
              "(iii) प्रत्येक वास्तविक संख्या एक अपरिमेय संख्या होती है।"), s))

s = p("नहीं। जिस धनात्मक पूर्णांक के अभाज्य गुणनखंड जोड़ों में बँट जाते हैं (पूर्ण वर्ग), उसका वर्गमूल परिमेय होता है। उदाहरण:")
s += root_steps(4) + root_steps(9)
s += why("4 और 9 पूर्ण वर्ग हैं, इसलिए इनके वर्गमूल 2 और 3 परिमेय हैं। जबकि " + m("\\sqrt{2}") + ", " + m("\\sqrt{3}") + " जैसे वर्गमूल अपरिमेय हैं।")
s += ans("नहीं, सभी धनात्मक पूर्णांकों के वर्गमूल अपरिमेय नहीं होते। उदाहरण: " + m("\\sqrt{4} = 2") + " एक परिमेय संख्या है।")
E2.append(("क्या सभी धनात्मक पूर्णांकों के वर्गमूल अपरिमेय होते हैं? यदि नहीं, तो एक ऐसी संख्या के वर्गमूल का उदाहरण दीजिए जो एक परिमेय संख्या है।", s))


def fig_sqrt5():
    U, X0, Y = 62, 70, 190
    px = lambda u: X0 + U * u
    g = axis(18, 352, Y, [-1, 0, 1, 2, 3, 4], px)
    O, A = (px(0), Y), (px(2), Y)
    B = (px(2), Y - U)
    r = math.sqrt(5) * U
    P = (px(0) + r, Y)
    g += arc(O[0], O[1], r, math.degrees(math.atan2(1, 2)), 0)
    g += L(*O, *A, INK, 3.2) + L(*A, *B, INK, 2.6) + L(*O, *B, ORG, 2.6)
    g += rmark(*A, (-1, 0), (0, -1))
    for (x, y), n in ((O, "O"), (A, "A"), (B, "B"), (P, "P")):
        g += dot(x, y, RED if n == "P" else INK)
    g += Tx(O[0] - 4, Y - 10, "O", s=15) + Tx(A[0] - 20, Y - 12, "A", s=15) + Tx(B[0] - 2, B[1] - 10, "B", s=15)
    g += Tx(P[0] + 12, Y - 9, "P", RED, 15)
    g += Tx(A[0] - 8, Y - U / 2 + 2, "1", RED, 14, 700, "end")
    nx, ny = -1 / math.sqrt(5), -2 / math.sqrt(5)
    mx, my = (O[0] + B[0]) / 2 + nx * 16, (O[1] + B[1]) / 2 + ny * 16
    g += Tx(mx, my, "√5", ORG, 15)
    g += Tx((O[0] + A[0]) / 2, Y + 42, "OA = 2 इकाई", INK, 12.5, 600)
    g += L(P[0], Y + 8, P[0], Y + 30, RED, 1.2, "3 3") + Tx(P[0] + 4, Y + 44, "P = √5", RED, 13.5, 700, "start")
    return svg(370, 245, g, "आकृति: संख्या रेखा पर √5 का निरूपण (OA = 2, AB = 1, OB = OP = √5)")


s = given("संख्या " + m("\\sqrt{5}"), "संख्या रेखा पर " + m("\\sqrt{5}") + " का निरूपण")
s += p("सबसे पहले 5 को दो वर्गों के योग के रूप में लिखते हैं:")
s += lines("5", "4 + 1", "2^2 + 1^2")
s += p("<b>रचना के चरण:</b>")
s += p("1. संख्या रेखा पर बिंदु O को 0 मानकर, O से दाईं ओर 2 इकाई पर बिंदु A अंकित कीजिए। अतः OA = 2 इकाई।")
s += p("2. A पर OA के लंबवत 1 इकाई लंबा रेखाखंड AB खींचिए। अतः " + m("\\angle OAB = 90^\\circ") + "।")
s += p("3. O और B को मिलाइए।")
s += formula("पाइथागोरस प्रमेय", "समकोण त्रिभुज में (कर्ण)² = (आधार)² + (लंब)²")
s += p("समकोण " + m("\\triangle OAB") + " में:")
s += lines("OB^2", "OA^2 + AB^2", "2^2 + 1^2", "4 + 1", "5")
s += lines("OB", "\\sqrt{5}")
s += p("4. O को केंद्र मानकर OB त्रिज्या का चाप खींचिए, जो संख्या रेखा को O के दाईं ओर बिंदु P पर काटता है।")
s += lines("OP", "OB", "\\sqrt{5}")
s += fig_sqrt5()
s += ans("संख्या रेखा पर बिंदु P, संख्या " + m("\\sqrt{5}") + " को निरूपित करता है (" + m("\\sqrt{5} \\approx 2.236") + ", यह 2 और 3 के बीच है)।")
E2.append(("दिखाइए कि संख्या रेखा पर " + m("\\sqrt{5}") + " को किस प्रकार निरूपित किया जा सकता है।", s))


def fig_spiral(n=8):
    U = 52
    pts = [(0.0, 0.0), (1.0, 0.0)]
    for k in range(1, n):
        x, y = pts[-1]
        r = math.hypot(x, y)
        pts.append((x - y / r, y + x / r))  # unit step perpendicular (anticlockwise)
    xs, ys = [q[0] for q in pts], [q[1] for q in pts]
    pad = 46
    W_ = (max(xs) - min(xs)) * U + 2 * pad; H_ = (max(ys) - min(ys)) * U + 2 * pad
    cx, cy = pad - min(xs) * U, pad + max(ys) * U
    S = lambda p_: (cx + p_[0] * U, cy - p_[1] * U)
    g = ""
    for k in range(2, n + 1):  # radii OP2..OPn
        g += L(*S(pts[0]), *S(pts[k]), ORG, 1.6, "5 4")
    g += L(*S(pts[0]), *S(pts[1]), INK, 2.6)
    for k in range(1, n):
        g += L(*S(pts[k]), *S(pts[k + 1]), INK, 2.6)
    for k in range(1, n):  # right angles at Pk between Pk->O and Pk->Pk+1
        x, y = pts[k]
        r = math.hypot(x, y)
        u1 = (-x / r, y / r)  # screen direction towards O
        nx, ny = pts[k + 1][0] - x, pts[k + 1][1] - y
        u2 = (nx, -ny)
        g += rmark(*S(pts[k]), u1, u2, 8)
    for k in range(2, n + 1):  # √k labels on radii, offset a little clockwise of the radius
        x, y = pts[k]
        r = math.hypot(x, y)
        t = 0.58
        ox, oy = y / r, -x / r  # clockwise normal (maths coords)
        lx, ly = S((x * t + ox * 0.22, y * t + oy * 0.22))
        g += Tx(lx, ly + 5, f"√{k}", ORG, 13, 700)
    for k in range(1, n):  # "1" on each unit segment, outside the spiral
        (x1, y1), (x2, y2) = pts[k], pts[k + 1]
        mx_, my_ = (x1 + x2) / 2, (y1 + y2) / 2
        r = math.hypot(mx_, my_)
        lx, ly = S((mx_ + mx_ / r * 0.22, my_ + my_ / r * 0.22))
        g += Tx(lx, ly + 5, "1", RED, 12.5, 700)
    lx, ly = S((0.5, -0.28))
    g += Tx(lx, ly + 5, "1", RED, 12.5, 700)
    for k in range(0, n + 1):
        x, y = pts[k]
        g += dot(*S(pts[k]))
        if k == 0:
            g += Tx(S(pts[0])[0] - 8, S(pts[0])[1] + 18, "O", s=15)
            continue
        r = math.hypot(x, y)
        lx, ly = S((x + x / r * 0.48, y + y / r * 0.48))
        g += Tx(lx, ly + 5, f"P<tspan font-size='10' dy='3'>{k}</tspan>", "#111", 14.5)
    return svg(int(W_), int(H_), g, "आकृति: वर्गमूल सर्पिल — OP₁ = 1, OP₂ = √2, OP₃ = √3, …, OP₈ = √8 = 2√2")


s = p("<b>रचना के चरण:</b>")
s += p("1. एक बिंदु O लीजिए और 1 इकाई लंबा रेखाखंड OP₁ खींचिए।")
s += p("2. P₁ पर OP₁ के लंबवत 1 इकाई लंबा रेखाखंड P₁P₂ खींचिए। O और P₂ को मिलाइए।")
s += p("3. P₂ पर OP₂ के लंबवत 1 इकाई का P₂P₃ खींचिए, फिर P₃ पर OP₃ के लंबवत P₃P₄, … इसी प्रकार आगे बढ़ते जाइए।")
s += formula("पाइथागोरस प्रमेय", "समकोण त्रिभुज में (कर्ण)² = (आधार)² + (लंब)²")
s += p("समकोण " + m("\\triangle OP_1P_2") + " में:")
s += lines("OP_2", "\\sqrt{OP_1^2 + P_1P_2^2}", "\\sqrt{1^2 + 1^2}", "\\sqrt{2}")
s += p("समकोण " + m("\\triangle OP_2P_3") + " में:")
s += lines("OP_3", "\\sqrt{OP_2^2 + P_2P_3^2}", "\\sqrt{(\\sqrt{2})^2 + 1^2}", "\\sqrt{2 + 1}", "\\sqrt{3}")
s += p("समकोण " + m("\\triangle OP_3P_4") + " में:")
s += lines("OP_4", "\\sqrt{(\\sqrt{3})^2 + 1^2}", "\\sqrt{4}", "\\sqrt{2 \\times 2}", "2")
s += p("इसी प्रकार हर बार 1 जुड़ता है:")
s += lines("OP_n", "\\sqrt{(\\sqrt{n-1})^2 + 1^2}", "\\sqrt{n}")
s += fig_spiral()
s += ans("बिंदुओं O, P₁, P₂, P₃, … को क्रम से मिलाने पर वर्गमूल सर्पिल बनता है, जिसमें " + m("OP_2 = \\sqrt{2},\\ OP_3 = \\sqrt{3},\\ OP_4 = 2,\\ \\dots,\\ OP_n = \\sqrt{n}") + "।")
E2.append(("कक्षा के लिए क्रियाकलाप (वर्गमूल सर्पिल की रचना): कागज़ की एक बड़ी शीट लीजिए और नीचे दी गई विधि से ‘वर्गमूल सर्पिल’ (square root spiral) की रचना कीजिए। "
           "सबसे पहले एक बिंदु O लीजिए और एकक लंबाई का रेखाखंड OP₁ खींचिए। एकक लंबाई वाले OP₁ पर लंब रेखाखंड P₁P₂ खींचिए। अब OP₂ पर लंब रेखाखंड P₂P₃ खींचिए। "
           "तब OP₃ पर लंब रेखाखंड P₃P₄ खींचिए। इस प्रक्रिया को जारी रखते हुए OPₙ₋₁ पर एकक लंबाई वाला लंब रेखाखंड खींचकर आप रेखाखंड Pₙ₋₁Pₙ प्राप्त कर सकते हैं। "
           "इस प्रकार आप बिंदु O, P₁, P₂, P₃, …, Pₙ, … प्राप्त कर लेंगे और उन्हें मिलाकर " + m("\\sqrt{2},\\ \\sqrt{3},\\ \\sqrt{4},\\ \\dots") + " को दर्शाने वाला एक सुंदर सर्पिल प्राप्त कर लेंगे।", s))
assert len(E2) == 4

# =====================================================================
# Exercise 1.3
# =====================================================================
E3 = []
TYPES = formula("दशमलव प्रसार के प्रकार", "", [
    "सांत (terminating): भाग देते-देते शेषफल 0 हो जाता है।",
    "असांत आवर्ती (non-terminating recurring): शेषफल 0 नहीं होता, अंकों का एक खंड बार-बार दोहराता है।"])
s = TYPES
ex = [("(i)", 36, 100, None), ("(ii)", 1, 11, "0.\\overline{09}"), ("(iii)", 33, 8, None),
      ("(iv)", 3, 13, "0.\\overline{230769}"), ("(v)", 2, 11, "0.\\overline{18}"), ("(vi)", 329, 400, None)]
res = []
for lab, a, b, rep in ex:
    if lab == "(iii)":
        body = lines("4\\dfrac{1}{8}", "\\dfrac{4 \\times 8 + 1}{8}", "\\dfrac{33}{8}")
    else:
        body = ""
    if b in (100,):
        body += lines(d(36, 100), "0.36")
        val, typ = "0.36", "सांत"
    elif b in (8, 400):
        k = 125 if b == 8 else 25
        dd = 1000 if b == 8 else 10000
        body += p("हर को 10 की घात बनाने के लिए अंश और हर को " + str(k) + " से गुणा करते हैं:")
        body += lines(d(a, b), d(f"{a} \\times {k}", f"{b} \\times {k}"), d(a * k, dd), f"{a * k / dd:g}")
        assert F(a, b) == F(a * k, dd)
        val, typ = f"{a * k / dd:g}", "सांत"
    else:
        tb, q0, dg = div_table(a, b, 8 if b == 11 else 7)
        body += tb
        val, typ = rep, "असांत आवर्ती"
        body += lines(d(a, b), f"0.{''.join(map(str, dg[:-1]))}\\dots", rep)
        body += why("शेषफल " + str(a) + " फिर से आ गया, इसलिए आगे वही अंक दोहराएँगे।")
    body += ans(m(val) + " — <b>" + typ + "</b> दशमलव प्रसार")
    res.append(f"{lab} {m(val)} ({typ})")
    s += part(lab + " " + (m("4\\dfrac{1}{8}") if lab == "(iii)" else M(a, b)), body)
assert F(1, 11) == F(9, 99) and F(3, 13) == F(230769, 999999) and F(2, 11) == F(18, 99)
s += ans(" ".join(res))
E3.append((qt("निम्नलिखित भिन्नों को दशमलव रूप में लिखिए और बताइए कि प्रत्येक का दशमलव प्रसार किस प्रकार का है: "
              "(i) " + M(36, 100) + " (ii) " + M(1, 11) + " (iii) " + m("4\\dfrac{1}{8}") + " (iv) " + M(3, 13) + " (v) " + M(2, 11) + " (vi) " + M(329, 400)), s))

s = given(m("\\dfrac{1}{7} = 0.\\overline{142857}"), M(2, 7) + ", " + M(3, 7) + ", " + M(4, 7) + ", " + M(5, 7) + ", " + M(6, 7) + " के दशमलव प्रसार")
s += p("हाँ, बिना लंबा भाग किए। " + M("k", 7) + " = k × " + M(1, 7) + ", अतः 0.142857… को k से गुणा करते हैं:")
outs = []
for k in range(2, 7):
    v = "".join(str(int(c)) for c in str(int(142857 * k)).zfill(6))
    assert F(int(v), 999999) == F(k, 7)
    s += lines(d(k, 7), f"{k} \\times \\dfrac{{1}}{{7}}", f"{k} \\times 0.\\overline{{142857}}", f"0.\\overline{{{v}}}")
    outs.append(f"{d(k, 7)} = 0.\\overline{{{v}}}")
s += why("ध्यान दें: हर उत्तर में वही छः अंक 1, 4, 2, 8, 5, 7 इसी चक्रीय क्रम में आते हैं, केवल शुरुआत का अंक बदलता है। 1 ÷ 7 के भाग में शेषफल 3, 2, 6, 4, 5, 1 आते हैं।")
s += ans(m(",\\ ".join(outs)))
E3.append(("आप जानते हैं कि " + m("\\dfrac{1}{7} = 0.\\overline{142857}") + " है। वास्तव में, लंबा भाग दिए बिना क्या आप यह बता सकते हैं कि "
           + M(2, 7) + ", " + M(3, 7) + ", " + M(4, 7) + ", " + M(5, 7) + ", " + M(6, 7) + " के दशमलव प्रसार क्या हैं? यदि हाँ, तो कैसे? "
           "[संकेत: " + M(1, 7) + " का मान ज्ञात करते समय शेषफलों का अध्ययन सावधानी से कीजिए।]", s))

# Q3 p/q
s = ""
b_ = p("माना")
b_ += eqs(("x", "0.\\overline{6} = 0.666\\dots"))
b_ += p("एक अंक दोहराता है, इसलिए दोनों पक्षों को 10 से गुणा करते हैं:")
b_ += eqs(("10x", "6.666\\dots"))
b_ += p("(2) में से (1) घटाने पर:")
b_ += lines("10x - x", "6.666\\dots - 0.666\\dots")
b_ += eqs(("9x", "6"))
b_ += tp("पक्षांतर: x का गुणक 9 दाएँ पक्ष में जाकर भाग बन जाता है।")
b_ += lines("x", d(6, 9), d("2 \\times 3", "3 \\times 3"), d(2, 3))
s += part("(i) " + m("0.\\overline{6}"), b_)
assert F(6, 9) == F(2, 3)
b_ = eqs(("x", "0.4\\overline{7} = 0.4777\\dots"))
b_ += p("दोनों पक्षों को 10 से गुणा करने पर:")
b_ += eqs(("10x", "4.777\\dots"))
b_ += p("फिर से 10 से गुणा करने पर (अर्थात मूल समीकरण को 100 से):")
b_ += eqs(("100x", "47.777\\dots"))
b_ += p("घटाने पर:")
b_ += lines("100x - 10x", "47.777\\dots - 4.777\\dots")
b_ += eqs(("90x", "43"))
b_ += tp("पक्षांतर: 90 दाएँ पक्ष में भाग बनकर जाता है।")
b_ += lines("x", d(43, 90))
assert F(43, 90) == F(4, 10) + F(7, 90)
s += part("(ii) " + m("0.4\\overline{7}"), b_)
b_ = eqs(("x", "0.\\overline{001} = 0.001001\\dots"))
b_ += p("तीन अंक (001) दोहराते हैं, इसलिए 1000 से गुणा करते हैं:")
b_ += eqs(("1000x", "1.001001\\dots"))
b_ += lines("1000x - x", "1.001001\\dots - 0.001001\\dots")
b_ += eqs(("999x", "1"))
b_ += tp("पक्षांतर: 999 दाएँ पक्ष में भाग बनकर जाता है।")
b_ += lines("x", d(1, 999))
s += part("(iii) " + m("0.\\overline{001}"), b_)
s += ans("(i) " + M(2, 3) + " (ii) " + M(43, 90) + " (iii) " + M(1, 999))
E3.append((qt("निम्नलिखित को " + M("p", "q") + " के रूप में व्यक्त कीजिए, जहाँ p और q पूर्णांक हैं तथा " + m("q \\neq 0") + " है: "
              "(i) " + m("0.\\overline{6}") + " (ii) " + m("0.4\\overline{7}") + " (iii) " + m("0.\\overline{001}")), s))

s = eqs(("x", "0.999\\dots"))
s += p("एक अंक (9) दोहराता है, इसलिए 10 से गुणा करते हैं:")
s += eqs(("10x", "9.999\\dots"))
s += lines("10x - x", "9.999\\dots - 0.999\\dots")
s += eqs(("9x", "9"))
s += tp("पक्षांतर: 9 दाएँ पक्ष में भाग बनकर जाता है।")
s += lines("x", d(9, 9), "1")
s += why("आश्चर्य की बात लगती है, पर 0.999… का अर्थ है अनंत तक 9 — 1 और 0.999… के बीच कोई भी संख्या नहीं बचती, इसलिए दोनों बराबर हैं। जैसे " + m("\\dfrac{1}{3} = 0.333\\dots") + " को 3 से गुणा करने पर " + m("1 = 0.999\\dots") + "।")
s += ans(m("0.999\\dots = 1 = \\dfrac{1}{1}") + " (p = 1, q = 1)")
E3.append(("0.99999… को " + M("p", "q") + " के रूप में व्यक्त कीजिए। क्या आप अपने उत्तर से आश्चर्यचकित हैं? अपने अध्यापक और कक्षा के सहयोगियों के साथ उत्तर की सार्थकता पर चर्चा कीजिए।", s))

tb, q0, dg = div_table(1, 17, 16)
rep17 = "".join(map(str, dg))
assert rep17 == "0588235294117647" and F(int(rep17), 10 ** 16 - 1) == F(1, 17)
s = p("17 से भाग देने पर शेषफल केवल 1, 2, …, 16 हो सकते हैं (0 आने पर प्रसार सांत हो जाता, जो यहाँ नहीं होगा क्योंकि 17 में केवल 2 या 5 अभाज्य गुणनखंड नहीं हैं)। "
      "अतः अधिकतम 16 चरणों के बाद कोई शेषफल दोहराएगा, इसलिए पुनरावृत्ति खंड में अधिकतम <b>16</b> अंक हो सकते हैं।")
s += p("<b>जाँच के लिए भाग:</b>")
s += tb
s += why("16वें चरण में शेषफल फिर 1 आ गया, अतः यहीं से अंक दोहराएँगे।")
s += lines(d(1, 17), "0.\\overline{0588235294117647}")
s += ans("अधिकतम 16 अंक; " + m("\\dfrac{1}{17} = 0.\\overline{0588235294117647}") + " में पुनरावृत्ति खंड पूरे 16 अंकों का है।")
E3.append(("" + M(1, 17) + " के दशमलव प्रसार में अंकों के पुनरावृत्ति खंड में अंकों की अधिकतम संख्या क्या हो सकती है? अपने उत्तर की जाँच करने के लिए विभाजन-क्रिया कीजिए।", s))

rows = []
for a, b in [(1, 2), (3, 4), (7, 8), (1, 5), (7, 25), (3, 20), (17, 40), (9, 125)]:
    v = F(a, b)
    dec = f"{a / b:.6f}".rstrip("0")
    fs = factors(b)
    assert set(fs) <= {2, 5} and math.gcd(a, b) == 1
    rows.append(f"<tr><td>{M(a, b)}</td><td>{dec}</td><td>{m(' \\times '.join(map(str, fs)))}</td></tr>")
s = p("कुछ उदाहरण (हर के अभाज्य गुणनखंड भी देखिए):")
s += "<div class='tw'><table class='st'><tr><th>परिमेय संख्या</th><th>दशमलव प्रसार</th><th>हर q के अभाज्य गुणनखंड</th></tr>" + "".join(rows) + "</table></div>"
s += p("हर उदाहरण में q के अभाज्य गुणनखंडों में केवल 2 या 5 या दोनों हैं। ऐसे में अंश-हर को 2 या 5 की उचित घात से गुणा करके हर को 10, 100, 1000, … बनाया जा सकता है, इसलिए प्रसार सांत होता है। उदाहरण:")
s += lines(d(7, 8), d(7, "2 \\times 2 \\times 2"), d("7 \\times 125", "8 \\times 125"), d(875, 1000), "0.875")
s += ans("q के अभाज्य गुणनखंडन में केवल 2 या 5 या दोनों होने चाहिए, अर्थात " + m("q = 2^m \\times 5^n") + " (m, n पूर्ण संख्याएँ)।")
E3.append(("" + M("p", "q") + " " + m("(q \\neq 0)") + " के रूप की परिमेय संख्याओं के अनेक उदाहरण लीजिए, जहाँ p और q पूर्णांक हैं, जिनका 1 के अतिरिक्त अन्य कोई उभयनिष्ठ गुणनखंड नहीं है और जिसका सांत दशमलव निरूपण (प्रसार) है। क्या आप यह अनुमान लगा सकते हैं कि q को कौन-सा गुण अवश्य संतुष्ट करना चाहिए?", s))

s = p("अनवसानी (असांत) अनावर्ती प्रसार में अंक कभी समाप्त नहीं होते और कोई खंड नियमित रूप से नहीं दोहराता। ऐसी संख्याएँ अपरिमेय होती हैं। उदाहरण:")
s += lines("\\text{पहली}", "0.10100100010000\\dots")
s += lines("\\text{दूसरी}", "0.20200200020000\\dots")
s += lines("\\text{तीसरी}", "0.003000300003\\dots")
s += why("हर संख्या में शून्यों की संख्या एक-एक करके बढ़ती है, इसलिए कोई खंड बार-बार नहीं दोहराता।")
s += ans(m("0.10100100010000\\dots,\\ 0.20200200020000\\dots,\\ 0.003000300003\\dots") + " (अन्य उदाहरण भी संभव: " + m("\\sqrt{2} = 1.41421\\dots") + ")")
E3.append(("ऐसी तीन संख्याएँ लिखिए जिनके दशमलव प्रसार अनवसानी अनावर्ती हों।", s))

tb1, _, d1 = div_table(5, 7, 7)
tb2, _, d2 = div_table(9, 11, 3)
s = given(M(5, 7) + " और " + M(9, 11), "इनके बीच तीन अपरिमेय संख्याएँ")
s += part("" + M(5, 7) + " का दशमलव प्रसार", tb1 + lines(d(5, 7), "0.714285714285\\dots", "0.\\overline{714285}"))
s += part("" + M(9, 11) + " का दशमलव प्रसार", tb2 + lines(d(9, 11), "0.8181\\dots", "0.\\overline{81}"))
assert F(714285, 999999) == F(5, 7) and F(81, 99) == F(9, 11)
s += p("0.714285… और 0.8181… के बीच अनवसानी अनावर्ती दशमलव वाली तीन संख्याएँ:")
s += lines("\\text{पहली}", "0.75075007500075000075\\dots")
s += lines("\\text{दूसरी}", "0.767076700767000767\\dots")
s += lines("\\text{तीसरी}", "0.808008000800008\\dots")
assert 0.714285 < 0.75075 < 0.7670767 < 0.808008 < 0.8181
s += ans(m("0.75075007500075000075\\dots,\\ 0.767076700767000767\\dots,\\ 0.808008000800008\\dots"))
E3.append(("परिमेय संख्याओं " + M(5, 7) + " और " + M(9, 11) + " के बीच की तीन अलग-अलग अपरिमेय संख्याएँ ज्ञात कीजिए।", s))

s = formula("पहचान", "", ["सांत या असांत आवर्ती दशमलव प्रसार → परिमेय संख्या", "असांत अनावर्ती दशमलव प्रसार → अपरिमेय संख्या",
                          "पूर्ण वर्ग न होने वाली प्राकृत संख्या का वर्गमूल → अपरिमेय"])
b_ = ladders(23) + p("23 एक अभाज्य संख्या है, इसके गुणनखंड जोड़े में नहीं बँटते, अर्थात 23 पूर्ण वर्ग नहीं है।")
b_ += lines("\\sqrt{23}", "4.795831\\dots") + ans("अपरिमेय (असांत अनावर्ती)")
s += part("(i) " + m("\\sqrt{23}"), b_)
s += part("(ii) " + m("\\sqrt{225}"), root_steps(225) + ans("परिमेय (225 पूर्ण वर्ग है, " + m("\\sqrt{225} = 15") + ")"))
s += part("(iii) 0.3796", lines("0.3796", d(3796, 10000)) + ans("परिमेय (सांत दशमलव)"))
s += part("(iv) 7.478478…", lines("7.478478\\dots", "7.\\overline{478}") + ans("परिमेय (असांत आवर्ती; " + m("= \\dfrac{7471}{999}") + ")"))
assert F(7, 1) + F(478, 999) == F(7471, 999)
s += part("(v) 1.101001000100001…", ans("अपरिमेय (असांत अनावर्ती — शून्यों की संख्या बढ़ती जाती है)"))
s += ans("(i) अपरिमेय (ii) परिमेय (iii) परिमेय (iv) परिमेय (v) अपरिमेय")
E3.append((qt("बताइए कि निम्नलिखित संख्याओं में कौन-कौन संख्याएँ परिमेय और कौन-कौन संख्याएँ अपरिमेय हैं: "
              "(i) " + m("\\sqrt{23}") + " (ii) " + m("\\sqrt{225}") + " (iii) 0.3796 (iv) 7.478478… (v) 1.101001000100001…"), s))
assert len(E3) == 9

# =====================================================================
# Exercise 1.4
# =====================================================================
E4 = []
s = formula("नियम", "", ["परिमेय ± अपरिमेय = अपरिमेय", "शून्येतर परिमेय × या ÷ अपरिमेय = अपरिमेय",
                         "दो अपरिमेय संख्याओं का योग/अंतर/गुणनफल/भागफल परिमेय भी हो सकता है और अपरिमेय भी"])
s += part("(i) " + m("2 - \\sqrt{5}"), p("2 परिमेय और " + m("\\sqrt{5}") + " अपरिमेय है (5 पूर्ण वर्ग नहीं)।") + ans("अपरिमेय (परिमेय − अपरिमेय)"))
s += part("(ii) " + m("(3 + \\sqrt{23}) - \\sqrt{23}"), lines("(3 + \\sqrt{23}) - \\sqrt{23}", "3 + \\sqrt{23} - \\sqrt{23}", "3") + ans("परिमेय"))
s += part("(iii) " + m("\\dfrac{2\\sqrt{7}}{7\\sqrt{7}}"), lines("\\dfrac{2\\sqrt{7}}{7\\sqrt{7}}", "\\dfrac{2}{7}") + why(m("\\sqrt{7}") + " अंश और हर दोनों में है, इसलिए कट जाता है।") + ans("परिमेय"))
s += part("(iv) " + m("\\dfrac{1}{\\sqrt{2}}"), p("1 परिमेय और " + m("\\sqrt{2}") + " अपरिमेय है।") + lines("\\dfrac{1}{\\sqrt{2}}", "0.7071\\dots") + ans("अपरिमेय"))
s += part("(v) " + m("2\\pi"), p("2 परिमेय और π अपरिमेय है।") + ans("अपरिमेय (शून्येतर परिमेय × अपरिमेय)"))
s += ans("(i) अपरिमेय (ii) परिमेय (iii) परिमेय (iv) अपरिमेय (v) अपरिमेय")
E4.append((qt("बताइए नीचे दी गई संख्याओं में कौन-कौन परिमेय हैं और कौन-कौन अपरिमेय हैं: "
              "(i) " + m("2 - \\sqrt{5}") + " (ii) " + m("(3 + \\sqrt{23}) - \\sqrt{23}") + " (iii) " + m("\\dfrac{2\\sqrt{7}}{7\\sqrt{7}}")
              + " (iv) " + m("\\dfrac{1}{\\sqrt{2}}") + " (v) " + m("2\\pi")), s))

s = formula("कर्णी गुणन", m("\\sqrt{a} \\times \\sqrt{b} = \\sqrt{ab}") + ",  " + m("\\sqrt{a} \\times \\sqrt{a} = a"))
b_ = p("पहले कोष्ठक के प्रत्येक पद से दूसरे कोष्ठक को गुणा करते हैं:")
b_ += lines("(3 + \\sqrt{3})(2 + \\sqrt{2})", "3(2 + \\sqrt{2}) + \\sqrt{3}(2 + \\sqrt{2})",
            "3 \\times 2 + 3 \\times \\sqrt{2} + \\sqrt{3} \\times 2 + \\sqrt{3} \\times \\sqrt{2}", "6 + 3\\sqrt{2} + 2\\sqrt{3} + \\sqrt{6}")
s += part("(i)", b_ + ans(m("6 + 3\\sqrt{2} + 2\\sqrt{3} + \\sqrt{6}")))
b_ = lines("(3 + \\sqrt{3})(3 - \\sqrt{3})", "3(3 - \\sqrt{3}) + \\sqrt{3}(3 - \\sqrt{3})",
           "3 \\times 3 - 3 \\times \\sqrt{3} + \\sqrt{3} \\times 3 - \\sqrt{3} \\times \\sqrt{3}", "9 - 3\\sqrt{3} + 3\\sqrt{3} - 3", "6")
b_ += why("सर्वसमिका " + m("(a + b)(a - b) = a^2 - b^2") + " से जाँच: " + m("3^2 - (\\sqrt{3})^2 = 9 - 3 = 6") + " ✔")
s += part("(ii)", b_ + ans("6"))
b_ = lines("(\\sqrt{5} + \\sqrt{2})^2", "(\\sqrt{5} + \\sqrt{2})(\\sqrt{5} + \\sqrt{2})", "\\sqrt{5}(\\sqrt{5} + \\sqrt{2}) + \\sqrt{2}(\\sqrt{5} + \\sqrt{2})",
           "\\sqrt{5} \\times \\sqrt{5} + \\sqrt{5} \\times \\sqrt{2} + \\sqrt{2} \\times \\sqrt{5} + \\sqrt{2} \\times \\sqrt{2}",
           "5 + \\sqrt{10} + \\sqrt{10} + 2", "7 + 2\\sqrt{10}")
b_ += why("सर्वसमिका " + m("(a + b)^2 = a^2 + 2ab + b^2") + " से जाँच: " + m("5 + 2\\sqrt{10} + 2 = 7 + 2\\sqrt{10}") + " ✔")
s += part("(iii)", b_ + ans(m("7 + 2\\sqrt{10}")))
b_ = lines("(\\sqrt{5} - \\sqrt{2})(\\sqrt{5} + \\sqrt{2})", "\\sqrt{5}(\\sqrt{5} + \\sqrt{2}) - \\sqrt{2}(\\sqrt{5} + \\sqrt{2})",
           "\\sqrt{5} \\times \\sqrt{5} + \\sqrt{5} \\times \\sqrt{2} - \\sqrt{2} \\times \\sqrt{5} - \\sqrt{2} \\times \\sqrt{2}",
           "5 + \\sqrt{10} - \\sqrt{10} - 2", "3")
b_ += why("सर्वसमिका " + m("(a - b)(a + b) = a^2 - b^2") + " से जाँच: " + m("5 - 2 = 3") + " ✔")
s += part("(iv)", b_ + ans("3"))
s += ans("(i) " + m("6 + 3\\sqrt{2} + 2\\sqrt{3} + \\sqrt{6}") + " (ii) 6 (iii) " + m("7 + 2\\sqrt{10}") + " (iv) 3")
E4.append((qt("निम्नलिखित व्यंजकों में से प्रत्येक व्यंजक को सरल कीजिए: "
              "(i) " + m("(3 + \\sqrt{3})(2 + \\sqrt{2})") + " (ii) " + m("(3 + \\sqrt{3})(3 - \\sqrt{3})")
              + " (iii) " + m("(\\sqrt{5} + \\sqrt{2})^2") + " (iv) " + m("(\\sqrt{5} - \\sqrt{2})(\\sqrt{5} + \\sqrt{2})")), s))

s = formula("π की परिभाषा", m("\\pi = \\dfrac{c}{d}") + " (c = परिधि, d = व्यास)")
s += p("यहाँ कोई अंतर्विरोध नहीं है। परिमेय संख्या के लिए " + M("p", "q") + " में p और q दोनों <b>पूर्णांक</b> होने चाहिए। "
       "किसी वृत्त में c और d दोनों एक साथ पूर्णांक नहीं हो सकते — यदि व्यास d परिमेय है तो परिधि c अपरिमेय होगी, और यदि c परिमेय है तो d अपरिमेय होगा।")
s += p("जब हम पैमाने या धागे से c और d नापते हैं, तो वे केवल <b>सन्निकट</b> (लगभग) मान होते हैं, इसलिए " + m("\\dfrac{22}{7}") + " या 3.14 भी π का सन्निकट मान ही है, सटीक मान नहीं।")
s += ans("π = c/d में c और d दोनों पूर्णांक नहीं होते (कम-से-कम एक अपरिमेय होता है), इसलिए π अपरिमेय है; नापकर मिला अनुपात केवल सन्निकट परिमेय मान है।")
E4.append(("आपको याद होगा कि π को एक वृत्त की परिधि (मान लीजिए c) और उसके व्यास (मान लीजिए d) के अनुपात से परिभाषित किया जाता है, अर्थात " + m("\\pi = \\dfrac{c}{d}") + " है। यह इस तथ्य का अंतर्विरोध करता हुआ प्रतीत होता है कि π अपरिमेय है। इस अंतर्विरोध का निराकरण आप किस प्रकार करेंगे?", s))


def fig_sqrt93():
    U, Y, X0 = 28, 190, 24
    A = (X0, Y)
    B = (X0 + 9.3 * U, Y)
    C = (B[0] + U, Y)
    O = ((A[0] + C[0]) / 2, Y)
    r = 10.3 / 2 * U
    h = math.sqrt(9.3) * U
    D = (B[0], Y - h)
    E_ = (B[0] + h, Y)
    g = L(A[0] - 10, Y, E_[0] + 34, Y, "#333", 1.8) + f"<path d='M {E_[0] + 34:.1f} {Y} l -8 -4 v 8 z' fill='#333'/>"
    g += f"<path d='M {A[0]:.1f} {Y} A {r:.1f} {r:.1f} 0 0 1 {C[0]:.1f} {Y}' fill='none' stroke='{INK}' stroke-width='1.8'/>"
    g += L(*O, *D, ORG, 1.6, "5 4")
    g += L(*B, *D, INK, 2.6)
    g += arc(B[0], B[1], h, 90, 0)
    g += rmark(*B, (0, -1), (1, 0))
    for P_, n, dx in ((A, "A", 0), (O, "O", 0), (B, "B", -9), (C, "C", 6), (E_, "E", 0)):
        g += dot(*P_, RED if n == "E" else INK) + Tx(P_[0] + dx, Y + 20, n, RED if n == "E" else "#111", 14.5)
    g += dot(*D) + Tx(D[0] - 18, D[1] - 10, "D", s=14.5)
    for x1, x2, t in ((A[0], B[0], "9.3 इकाई"), (B[0], C[0], "1")):
        g += L(x1, Y + 30, x2, Y + 30, "#666", 1.2) + L(x1, Y + 26, x1, Y + 34, "#666", 1.2) + L(x2, Y + 26, x2, Y + 34, "#666", 1.2)
        g += Tx((x1 + x2) / 2, Y + 47, t, "#444", 12.5, 600)
    g += Tx(B[0] - 7, Y - h / 2 + 4, "√9.3", INK, 13.5, 700, "end")
    g += Tx(E_[0] + 2, Y + 46, "BE = √9.3", RED, 12.5, 700)
    g += Tx((O[0] + D[0]) / 2 - 10, (O[1] + D[1]) / 2 - 6, "5.15", ORG, 12, 700, "end")
    return svg(440, 250, g, "आकृति: √9.3 का निरूपण — AB = 9.3, BC = 1, O मध्य-बिंदु, BD ⊥ AC, BD = BE = √9.3")


assert abs((5.15 ** 2 - 4.15 ** 2) - 9.3) < 1e-9
s = given("संख्या " + m("\\sqrt{9.3}"), "संख्या रेखा पर " + m("\\sqrt{9.3}") + " का निरूपण")
s += p("<b>रचना के चरण:</b>")
s += p("1. एक रेखा पर बिंदु A से AB = 9.3 इकाई अंकित कीजिए। B से आगे BC = 1 इकाई अंकित कीजिए। अतः AC = 9.3 + 1 = 10.3 इकाई।")
s += p("2. AC का मध्य-बिंदु O ज्ञात कीजिए (AC का लंब समद्विभाजक खींचकर)।")
s += lines("OA", "OC", d(10.3, 2), "5.15 \\text{ इकाई}")
s += p("3. O को केंद्र और OC (= 5.15) को त्रिज्या मानकर अर्धवृत्त खींचिए।")
s += p("4. B पर AC के लंबवत रेखा खींचिए, जो अर्धवृत्त को D पर काटती है। तब " + m("BD = \\sqrt{9.3}") + "।")
s += p("<b>सिद्ध करना कि " + m("BD = \\sqrt{9.3}") + ":</b>")
s += lines("OD", "\\text{त्रिज्या}", "5.15")
s += lines("OB", "OC - BC", "5.15 - 1", "4.15")
s += formula("पाइथागोरस प्रमेय", "समकोण " + m("\\triangle OBD") + " में " + m("OD^2 = OB^2 + BD^2"))
s += p("BD² को अकेला रखने के लिए OB² को पक्षांतर करते हैं:")
s += tp("पक्षांतर: बाएँ पक्ष का +OB² दाएँ पक्ष में −OB² बन जाता है।")
s += eqs(("BD^2", "OD^2 - OB^2"))
s += formula("सर्वसमिका", m("a^2 - b^2 = (a + b)(a - b)"))
s += lines("BD^2", "(5.15)^2 - (4.15)^2", "(5.15 + 4.15)(5.15 - 4.15)", "9.3 \\times 1", "9.3")
s += lines("BD", "\\sqrt{9.3}")
s += p("5. BC को संख्या रेखा मानें, जिसमें B = 0 और C = 1 है। B को केंद्र और BD त्रिज्या लेकर चाप खींचिए, जो संख्या रेखा को E पर काटता है।")
s += lines("BE", "BD", "\\sqrt{9.3}")
s += fig_sqrt93()
s += ans("संख्या रेखा पर बिंदु E, संख्या " + m("\\sqrt{9.3}") + " को निरूपित करता है (" + m("\\sqrt{9.3} \\approx 3.05") + ")।")
E4.append(("संख्या रेखा पर " + m("\\sqrt{9.3}") + " को निरूपित कीजिए।", s))

s = formula("हर का परिमेयकरण", "हर में " + m("\\sqrt{a}") + " हो तो " + m("\\sqrt{a}") + " से; " + m("\\sqrt{a} \\pm \\sqrt{b}") + " हो तो उसके संयुग्मी " + m("\\sqrt{a} \\mp \\sqrt{b}") + " से अंश और हर को गुणा करें।")
b_ = lines("\\dfrac{1}{\\sqrt{7}}", "\\dfrac{1}{\\sqrt{7}} \\times \\dfrac{\\sqrt{7}}{\\sqrt{7}}", "\\dfrac{\\sqrt{7}}{\\sqrt{7} \\times \\sqrt{7}}", "\\dfrac{\\sqrt{7}}{7}")
s += part("(i) " + m("\\dfrac{1}{\\sqrt{7}}"), b_ + ans(m("\\dfrac{\\sqrt{7}}{7}")))
IDN = formula("सर्वसमिका", m("(a - b)(a + b) = a^2 - b^2"))
b_ = p("हर का संयुग्मी " + m("\\sqrt{7} + \\sqrt{6}") + " है।") + IDN
b_ += lines("\\dfrac{1}{\\sqrt{7} - \\sqrt{6}}", "\\dfrac{1}{\\sqrt{7} - \\sqrt{6}} \\times \\dfrac{\\sqrt{7} + \\sqrt{6}}{\\sqrt{7} + \\sqrt{6}}",
            "\\dfrac{\\sqrt{7} + \\sqrt{6}}{(\\sqrt{7})^2 - (\\sqrt{6})^2}", "\\dfrac{\\sqrt{7} + \\sqrt{6}}{7 - 6}", "\\sqrt{7} + \\sqrt{6}")
s += part("(ii) " + m("\\dfrac{1}{\\sqrt{7} - \\sqrt{6}}"), b_ + ans(m("\\sqrt{7} + \\sqrt{6}")))
b_ = p("हर का संयुग्मी " + m("\\sqrt{5} - \\sqrt{2}") + " है।") + formula("सर्वसमिका", m("(a + b)(a - b) = a^2 - b^2"))
b_ += lines("\\dfrac{1}{\\sqrt{5} + \\sqrt{2}}", "\\dfrac{1}{\\sqrt{5} + \\sqrt{2}} \\times \\dfrac{\\sqrt{5} - \\sqrt{2}}{\\sqrt{5} - \\sqrt{2}}",
            "\\dfrac{\\sqrt{5} - \\sqrt{2}}{(\\sqrt{5})^2 - (\\sqrt{2})^2}", "\\dfrac{\\sqrt{5} - \\sqrt{2}}{5 - 2}", "\\dfrac{\\sqrt{5} - \\sqrt{2}}{3}")
s += part("(iii) " + m("\\dfrac{1}{\\sqrt{5} + \\sqrt{2}}"), b_ + ans(m("\\dfrac{\\sqrt{5} - \\sqrt{2}}{3}")))
b_ = p("हर का संयुग्मी " + m("\\sqrt{7} + 2") + " है।") + IDN
b_ += lines("\\dfrac{1}{\\sqrt{7} - 2}", "\\dfrac{1}{\\sqrt{7} - 2} \\times \\dfrac{\\sqrt{7} + 2}{\\sqrt{7} + 2}",
            "\\dfrac{\\sqrt{7} + 2}{(\\sqrt{7})^2 - 2^2}", "\\dfrac{\\sqrt{7} + 2}{7 - 4}", "\\dfrac{\\sqrt{7} + 2}{3}")
s += part("(iv) " + m("\\dfrac{1}{\\sqrt{7} - 2}"), b_ + ans(m("\\dfrac{\\sqrt{7} + 2}{3}")))
for v, w in ((1 / math.sqrt(7), math.sqrt(7) / 7), (1 / (math.sqrt(7) - math.sqrt(6)), math.sqrt(7) + math.sqrt(6)),
             (1 / (math.sqrt(5) + math.sqrt(2)), (math.sqrt(5) - math.sqrt(2)) / 3), (1 / (math.sqrt(7) - 2), (math.sqrt(7) + 2) / 3)):
    close(v, w)
s += ans("(i) " + m("\\dfrac{\\sqrt{7}}{7}") + " (ii) " + m("\\sqrt{7} + \\sqrt{6}") + " (iii) " + m("\\dfrac{\\sqrt{5} - \\sqrt{2}}{3}") + " (iv) " + m("\\dfrac{\\sqrt{7} + 2}{3}"))
E4.append((qt("निम्नलिखित के हरों का परिमेयकरण कीजिए: (i) " + m("\\dfrac{1}{\\sqrt{7}}") + " (ii) " + m("\\dfrac{1}{\\sqrt{7} - \\sqrt{6}}")
              + " (iii) " + m("\\dfrac{1}{\\sqrt{5} + \\sqrt{2}}") + " (iv) " + m("\\dfrac{1}{\\sqrt{7} - 2}")), s))
assert len(E4) == 5

# =====================================================================
# Exercise 1.5
# =====================================================================
E5 = []
POW = formula("घातांक नियम", m("(a^m)^n = a^{mn}"))
s = ""
for lab, n, base, e_, k in (("(i)", 64, 2, 6, 2), ("(ii)", 32, 2, 5, 5), ("(iii)", 125, 5, 3, 3)):
    b_ = ladders(n)
    b_ += lines(str(n), " \\times ".join([str(base)] * e_), f"{base}^{{{e_}}}")
    b_ += POW
    b_ += lines(f"{n}^{{\\frac{{1}}{{{k}}}}}", f"\\left({base}^{{{e_}}}\\right)^{{\\frac{{1}}{{{k}}}}}", f"{base}^{{{e_} \\times \\frac{{1}}{{{k}}}}}", f"{base}^{{{e_ // k}}}", str(base ** (e_ // k)))
    assert round(n ** (1 / k)) == base ** (e_ // k)
    s += part(lab + " " + m(f"{n}^{{\\frac{{1}}{{{k}}}}}"), b_)
s += ans("(i) 8 (ii) 2 (iii) 5")
E5.append((qt("ज्ञात कीजिए: (i) " + m("64^{\\frac{1}{2}}") + " (ii) " + m("32^{\\frac{1}{5}}") + " (iii) " + m("125^{\\frac{1}{3}}")), s))

s = ""
for lab, n, base, e_, num, den, val in (("(i)", 9, 3, 2, 3, 2, "27"), ("(ii)", 32, 2, 5, 2, 5, "4"), ("(iii)", 16, 2, 4, 3, 4, "8")):
    b_ = ladders(n) + lines(str(n), " \\times ".join([str(base)] * e_), f"{base}^{{{e_}}}") + POW
    pw = e_ * num // den
    b_ += lines(f"{n}^{{\\frac{{{num}}}{{{den}}}}}", f"\\left({base}^{{{e_}}}\\right)^{{\\frac{{{num}}}{{{den}}}}}",
                f"{base}^{{{e_} \\times \\frac{{{num}}}{{{den}}}}}", f"{base}^{{{pw}}}", " \\times ".join([str(base)] * pw), val)
    close(n ** (num / den), float(val))
    s += part(lab + " " + m(f"{n}^{{\\frac{{{num}}}{{{den}}}}}"), b_)
b_ = ladders(125) + lines("125", "5 \\times 5 \\times 5", "5^3") + formula("घातांक नियम", m("(a^m)^n = a^{mn}") + ",  " + m("a^{-n} = \\dfrac{1}{a^n}"))
b_ += lines("125^{-\\frac{1}{3}}", "\\left(5^3\\right)^{-\\frac{1}{3}}", "5^{3 \\times \\left(-\\frac{1}{3}\\right)}", "5^{-1}", "\\dfrac{1}{5}")
close(125 ** (-1 / 3), 0.2)
s += part("(iv) " + m("125^{-\\frac{1}{3}}"), b_)
s += ans("(i) 27 (ii) 4 (iii) 8 (iv) " + M(1, 5))
E5.append((qt("ज्ञात कीजिए: (i) " + m("9^{\\frac{3}{2}}") + " (ii) " + m("32^{\\frac{2}{5}}") + " (iii) " + m("16^{\\frac{3}{4}}") + " (iv) " + m("125^{-\\frac{1}{3}}")), s))

s = ""
b_ = formula("घातांक नियम", m("a^m \\cdot a^n = a^{m+n}"))
b_ += lines("2^{\\frac{2}{3}} \\cdot 2^{\\frac{1}{5}}", "2^{\\frac{2}{3} + \\frac{1}{5}}", "2^{\\frac{2 \\times 5 + 1 \\times 3}{15}}", "2^{\\frac{10 + 3}{15}}", "2^{\\frac{13}{15}}")
assert F(2, 3) + F(1, 5) == F(13, 15)
s += part("(i) " + m("2^{\\frac{2}{3}} \\cdot 2^{\\frac{1}{5}}"), b_)
b_ = formula("घातांक नियम", m("\\dfrac{1}{a^n} = a^{-n}") + ",  " + m("(a^m)^n = a^{mn}"))
b_ += lines("\\left(\\dfrac{1}{3^3}\\right)^7", "\\left(3^{-3}\\right)^7", "3^{-3 \\times 7}", "3^{-21}")
s += part("(ii) " + m("\\left(\\dfrac{1}{3^3}\\right)^7"), b_)
b_ = formula("घातांक नियम", m("\\dfrac{a^m}{a^n} = a^{m-n}"))
b_ += lines("\\dfrac{11^{\\frac{1}{2}}}{11^{\\frac{1}{4}}}", "11^{\\frac{1}{2} - \\frac{1}{4}}", "11^{\\frac{2 - 1}{4}}", "11^{\\frac{1}{4}}")
s += part("(iii) " + m("\\dfrac{11^{\\frac{1}{2}}}{11^{\\frac{1}{4}}}"), b_)
b_ = formula("घातांक नियम", m("a^m \\cdot b^m = (ab)^m"))
b_ += lines("7^{\\frac{1}{2}} \\cdot 8^{\\frac{1}{2}}", "(7 \\times 8)^{\\frac{1}{2}}", "56^{\\frac{1}{2}}")
b_ += p("कर्णी रूप में सरल करने के लिए 56 के गुणनखंड:") + ladders(56)
b_ += lines("56^{\\frac{1}{2}}", "\\sqrt{56}", "\\sqrt{2 \\times 2 \\times 2 \\times 7}", "\\sqrt{(2 \\times 2) \\times 14}", "2\\sqrt{14}")
close(math.sqrt(56), 2 * math.sqrt(14))
s += part("(iv) " + m("7^{\\frac{1}{2}} \\cdot 8^{\\frac{1}{2}}"), b_)
s += ans("(i) " + m("2^{\\frac{13}{15}}") + " (ii) " + m("3^{-21}") + " (iii) " + m("11^{\\frac{1}{4}}") + " (iv) " + m("56^{\\frac{1}{2}} = 2\\sqrt{14}"))
E5.append((qt("सरल कीजिए: (i) " + m("2^{\\frac{2}{3}} \\cdot 2^{\\frac{1}{5}}") + " (ii) " + m("\\left(\\dfrac{1}{3^3}\\right)^7")
              + " (iii) " + m("\\dfrac{11^{\\frac{1}{2}}}{11^{\\frac{1}{4}}}") + " (iv) " + m("7^{\\frac{1}{2}} \\cdot 8^{\\frac{1}{2}}")), s))
assert len(E5) == 3

# ---------------- checks and pages ----------------
import re as _re
ALL = [("exercise-1-1", "प्रश्नावली 1.1", "परिमेय संख्याएँ", E1), ("exercise-1-2", "प्रश्नावली 1.2", "अपरिमेय संख्याएँ", E2),
       ("exercise-1-3", "प्रश्नावली 1.3", "वास्तविक संख्याएँ और उनके दशमलव प्रसार", E3),
       ("exercise-1-4", "प्रश्नावली 1.4", "वास्तविक संख्याओं पर संक्रियाएँ", E4),
       ("exercise-1-5", "प्रश्नावली 1.5", "वास्तविक संख्याओं के लिए घातांक-नियम", E5)]
for _, _, _, E in ALL:
    for _qt, _sol in E:
        for _t in _re.findall(r"\\\((.+?)\\\)", _qt + _sol):
            assert not _re.search(r"[\u0900-\u097F]", _t), ("Devanagari in TeX", _t)
            assert _t.count("(") == _t.count(")") and _t.count("{") == _t.count("}"), ("unbalanced TeX", _t)
for i, (slug, title, topic, E) in enumerate(ALL):
    prev = (BASE + ALL[i - 1][0] + "/", ALL[i - 1][1]) if i else (BASE, "अध्याय 1")
    nxt = (BASE + ALL[i + 1][0] + "/", ALL[i + 1][1]) if i + 1 < len(ALL) else ("/hi/class-09/maths/", "सभी अध्याय")
    page(BASE, 1, CH, slug, title, f"कक्षा 9 गणित · अध्याय 1: संख्या पद्धति · {len(E)} प्रश्न ({topic})", E,
         prev, nxt, css=CSS + EXTRA_CSS, boards=BOARDS9)
print("ok")
