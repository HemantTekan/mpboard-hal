#!/usr/bin/env python3
"""Class 10 Maths, Chapter 2 (बहुपद): Exercise 2.1 and 2.2 (rationalised NCERT), Hindi medium.
Run from repo root: python3 tools/solutions/class10_ch2.py
"""
import sys, pathlib
from fractions import Fraction as F
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from common import *  # noqa

BASE = "/hi/class-10/maths/chapter-02/"
CH = "बहुपद"


def eqs(*pairs):
    """Separate equations, one per row, aligned at '='."""
    rows = "".join(f"<span class='l'>{mcell(a)}</span><span class='s'>=</span><span class='r'>{mcell(b)}</span>" for a, b in pairs)
    return "<div class='eq'>" + rows + "</div>"


def therefore(t):
    return f"<p class='ok'>{t}</p>"


# ---------------- graphs for Exercise 2.1 ----------------
def svg(f, zeros, label):
    W, H, xr, yr = 300, 220, (-5, 5), (-5, 5)
    sx = lambda x: (x - xr[0]) / (xr[1] - xr[0]) * W
    sy = lambda y: H - (y - yr[0]) / (yr[1] - yr[0]) * H
    pts, path = [], []
    for i in range(401):
        x = xr[0] + (xr[1] - xr[0]) * i / 400
        y = f(x)
        if yr[0] - 1 < y < yr[1] + 1:
            pts.append(f"{sx(x):.1f},{sy(y):.1f}")
        elif pts:
            path.append(pts); pts = []
    if pts:
        path.append(pts)
    poly = "".join(f"<polyline points='{' '.join(p)}' fill='none' stroke='#1f5aa6' stroke-width='2.6'/>" for p in path)
    grid = "".join(f"<line x1='{sx(i):.1f}' y1='0' x2='{sx(i):.1f}' y2='{H}' stroke='#eef1f7'/>" for i in range(-5, 6))
    grid += "".join(f"<line x1='0' y1='{sy(i):.1f}' x2='{W}' y2='{sy(i):.1f}' stroke='#eef1f7'/>" for i in range(-5, 6))
    axes = (f"<line x1='0' y1='{sy(0):.1f}' x2='{W}' y2='{sy(0):.1f}' stroke='#333' stroke-width='1.4'/>"
            f"<line x1='{sx(0):.1f}' y1='0' x2='{sx(0):.1f}' y2='{H}' stroke='#333' stroke-width='1.4'/>"
            f"<text x='{W - 12}' y='{sy(0) - 6:.1f}' font-size='13'>X</text><text x='{sx(0) + 6:.1f}' y='14' font-size='13'>Y</text>"
            f"<text x='{sx(0) + 4:.1f}' y='{sy(0) + 14:.1f}' font-size='11'>O</text>")
    dots = "".join(f"<circle cx='{sx(z):.1f}' cy='{sy(0):.1f}' r='5' fill='#d6336c'/>" for z in zeros)
    return (f"<svg class='graph' viewBox='0 0 {W} {H}' role='img' aria-label='{label}'>{grid}{axes}{poly}{dots}"
            f"<text x='8' y='{H - 8}' font-size='12' fill='#555'>y = p(x)</text></svg>")


GRAPHS = [
    ("(i)", lambda x: 3, [], 0, "आलेख x-अक्ष के समांतर एक सरल रेखा है, जो x-अक्ष को कहीं नहीं काटती।"),
    ("(ii)", lambda x: 0.8 * x + 1.6, [-2], 1, "आलेख x-अक्ष को केवल एक बिंदु पर काटता है।"),
    ("(iii)", lambda x: 0.12 * x * (x - 3) * (x + 3), [-3, 0, 3], 3, "आलेख x-अक्ष को तीन बिंदुओं पर काटता है।"),
    ("(iv)", lambda x: 0.5 * (x * x - 4), [-2, 2], 2, "आलेख x-अक्ष को दो बिंदुओं पर काटता है।"),
    ("(v)", lambda x: 0.12 * (x * x - 1) * (x * x - 9), [-3, -1, 1, 3], 4, "आलेख x-अक्ष को चार बिंदुओं पर काटता है।"),
    ("(vi)", lambda x: 0.12 * (x + 3) * x * (x - 2) ** 2, [-3, 0, 2], 3, "आलेख x-अक्ष को तीन बिंदुओं पर काटता/स्पर्श करता है।"),
]

EX21 = []
b = given("कुछ बहुपदों p(x) के आलेख y = p(x)", "प्रत्येक स्थिति में p(x) के शून्यकों की संख्या")
b += formula("नियम", "बहुपद p(x) के शून्यकों की संख्या = आलेख y = p(x) द्वारा x-अक्ष को काटने (या स्पर्श करने) वाले बिंदुओं की संख्या")
b += "<p class='muted'>नीचे के आलेख पाठ्यपुस्तक की आकृति 2.10 जैसे बनाए गए हैं; लाल बिंदु वे स्थान हैं जहाँ आलेख x-अक्ष से मिलता है।</p>"
for lab, f, z, n, why in GRAPHS:
    for zz in z:
        assert abs(f(zz)) < 1e-9
    b += part(lab, svg(f, z, f"आलेख {lab}") + f"<p>{why}</p>" + therefore(f"अतः शून्यकों की संख्या = {n}"))
b += ans("(i) 0 (ii) 1 (iii) 3 (iv) 2 (v) 4 (vi) 3")
EX21.append(("नीचे दी गई आकृति में किन्हीं बहुपदों p(x) के आलेख y = p(x) दिए गए हैं। प्रत्येक स्थिति में p(x) के शून्यकों की संख्या ज्ञात कीजिए।", b))

# ---------------- Exercise 2.2 ----------------
SUMF = formula("शून्यक और गुणांकों में संबंध", m("ax^2+bx+c") + " के शून्यक " + m("\\alpha") + " और " + m("\\beta") + " हों, तो "
               + m("\\alpha+\\beta=-\\dfrac{b}{a}") + " और " + m("\\alpha\\beta=\\dfrac{c}{a}"))


def check(poly, coeffs, z1, z2):
    a, bb, c = coeffs
    for z in (z1, z2):
        if isinstance(z, F):
            assert a * z * z + bb * z + c == 0, (poly, z)
    return True


def verify(var, a, b_, c, zs, sum_steps, prod_steps, sum_val, prod_val):
    s = "<div class='vt'>शून्यकों और गुणांकों के बीच संबंध की जाँच:</div>"
    s += f"<p>यहाँ {m('a=' + a)}, {m('b=' + b_)}, {m('c=' + c)} तथा {m('\\alpha=' + zs[0])}, {m('\\beta=' + zs[1])}</p>"
    s += lines("\\alpha+\\beta", *sum_steps)
    bb = f"({b_})" if b_.startswith("-") else b_
    s += lines("-\\dfrac{b}{a}", f"-\\dfrac{{{bb}}}{{{a}}}", sum_val)
    s += therefore("अतः " + m("\\alpha+\\beta=-\\dfrac{b}{a}") + " ✔")
    s += lines("\\alpha\\beta", *prod_steps)
    s += lines("\\dfrac{c}{a}", prod_val) if f"\\dfrac{{{c}}}{{{a}}}" == prod_val else lines("\\dfrac{c}{a}", f"\\dfrac{{{c}}}{{{a}}}", prod_val)
    s += therefore("अतः " + m("\\alpha\\beta=\\dfrac{c}{a}") + " ✔")
    return s


def zero_from(factor_eqs):
    """factor_eqs: list of [(lhs, '0'), (var, value)] blocks."""
    return "".join(eqs(*blk) for blk in factor_eqs)


P = []
# (i) x^2 - 2x - 8
check("i", (1, -2, -8), F(4), F(-2))
p = given(m("p(x)=x^2-2x-8"), "शून्यक, तथा शून्यकों और गुणांकों के बीच संबंध की सत्यता")
p += f"<p>मध्य पद विभाजन: {m('a\\times c=1\\times(-8)=-8')}; ऐसी दो संख्याएँ जिनका गुणनफल −8 और योग −2 हो: −4 और 2</p>"
p += lines("x^2-2x-8", "x^2-4x+2x-8", "x(x-4)+2(x-4)", "(x-4)(x+2)")
p += "<p>शून्यक के लिए p(x) = 0 रखने पर " + m("(x-4)(x+2)=0") + "</p>"
p += zero_from([[("x-4", "0"), ("x", "4")], [("x+2", "0"), ("x", "-2")]])
p += therefore("अतः शून्यक 4 और −2 हैं।")
p += verify("x", "1", "-2", "-8", ("4", "-2"), ["4+(-2)", "2"], ["4\\times(-2)", "-8"], "2", "-8")
P.append(("(i) " + m("x^2-2x-8"), p))

# (ii) 4s^2 - 4s + 1
check("ii", (4, -4, 1), F(1, 2), F(1, 2))
p = given(m("p(s)=4s^2-4s+1"), "शून्यक तथा संबंध की सत्यता")
p += f"<p>मध्य पद विभाजन: {m('a\\times c=4\\times 1=4')}; गुणनफल 4 और योग −4 वाली संख्याएँ: −2 और −2</p>"
p += lines("4s^2-4s+1", "4s^2-2s-2s+1", "2s(2s-1)-1(2s-1)", "(2s-1)(2s-1)")
p += "<p>p(s) = 0 रखने पर " + m("(2s-1)(2s-1)=0") + "</p>"
p += zero_from([[("2s-1", "0"), ("2s", "1"), ("s", "\\dfrac{1}{2}")]])
p += therefore("अतः दोनों शून्यक " + m("\\dfrac{1}{2}") + " और " + m("\\dfrac{1}{2}") + " हैं।")
p += verify("s", "4", "-4", "1", ("\\dfrac{1}{2}", "\\dfrac{1}{2}"), ["\\dfrac{1}{2}+\\dfrac{1}{2}", "\\dfrac{2}{2}", "1"],
            ["\\dfrac{1}{2}\\times\\dfrac{1}{2}", "\\dfrac{1}{4}"], "1", "\\dfrac{1}{4}")
P.append(("(ii) " + m("4s^2-4s+1"), p))

# (iii) 6x^2 - 3 - 7x
check("iii", (6, -7, -3), F(3, 2), F(-1, 3))
p = given(m("p(x)=6x^2-3-7x"), "शून्यक तथा संबंध की सत्यता")
p += "<p>मानक रूप में लिखने पर</p>" + lines("p(x)", "6x^2-7x-3")
p += f"<p>मध्य पद विभाजन: {m('a\\times c=6\\times(-3)=-18')}; गुणनफल −18 और योग −7 वाली संख्याएँ: −9 और 2</p>"
p += lines("6x^2-7x-3", "6x^2-9x+2x-3", "3x(2x-3)+1(2x-3)", "(2x-3)(3x+1)")
p += "<p>p(x) = 0 रखने पर " + m("(2x-3)(3x+1)=0") + "</p>"
p += zero_from([[("2x-3", "0"), ("2x", "3"), ("x", "\\dfrac{3}{2}")], [("3x+1", "0"), ("3x", "-1"), ("x", "-\\dfrac{1}{3}")]])
p += therefore("अतः शून्यक " + m("\\dfrac{3}{2}") + " और " + m("-\\dfrac{1}{3}") + " हैं।")
p += verify("x", "6", "-7", "-3", ("\\dfrac{3}{2}", "-\\dfrac{1}{3}"),
            ["\\dfrac{3}{2}+\\left(-\\dfrac{1}{3}\\right)", "\\dfrac{9-2}{6}", "\\dfrac{7}{6}"],
            ["\\dfrac{3}{2}\\times\\left(-\\dfrac{1}{3}\\right)", "-\\dfrac{3}{6}", "-\\dfrac{1}{2}"], "\\dfrac{7}{6}", "-\\dfrac{1}{2}")
P.append(("(iii) " + m("6x^2-3-7x"), p))

# (iv) 4u^2 + 8u
check("iv", (4, 8, 0), F(0), F(-2))
p = given(m("p(u)=4u^2+8u"), "शून्यक तथा संबंध की सत्यता")
p += "<p>यहाँ अचर पद नहीं है (c = 0), इसलिए उभयनिष्ठ गुणनखंड 4u बाहर निकालेंगे।</p>"
p += lines("4u^2+8u", "4u(u+2)")
p += "<p>p(u) = 0 रखने पर " + m("4u(u+2)=0") + "</p>"
p += zero_from([[("4u", "0"), ("u", "0")], [("u+2", "0"), ("u", "-2")]])
p += therefore("अतः शून्यक 0 और −2 हैं।")
p += verify("u", "4", "8", "0", ("0", "-2"), ["0+(-2)", "-2"], ["0\\times(-2)", "0"], "-2", "0")
P.append(("(iv) " + m("4u^2+8u"), p))

# (v) t^2 - 15
p = given(m("p(t)=t^2-15"), "शून्यक तथा संबंध की सत्यता")
p += formula("सर्वसमिका", m("a^2-b^2=(a-b)(a+b)"))
p += "<p>15 पूर्ण वर्ग नहीं है, इसलिए " + m("15=(\\sqrt{15})^2") + " लिखेंगे।</p>"
p += lines("t^2-15", "t^2-(\\sqrt{15})^2", "(t-\\sqrt{15})(t+\\sqrt{15})")
p += "<p>p(t) = 0 रखने पर " + m("(t-\\sqrt{15})(t+\\sqrt{15})=0") + "</p>"
p += zero_from([[("t-\\sqrt{15}", "0"), ("t", "\\sqrt{15}")], [("t+\\sqrt{15}", "0"), ("t", "-\\sqrt{15}")]])
p += therefore("अतः शून्यक " + m("\\sqrt{15}") + " और " + m("-\\sqrt{15}") + " हैं।")
p += verify("t", "1", "0", "-15", ("\\sqrt{15}", "-\\sqrt{15}"), ["\\sqrt{15}+(-\\sqrt{15})", "0"],
            ["\\sqrt{15}\\times(-\\sqrt{15})", "-(\\sqrt{15})^2", "-15"], "0", "-15")
P.append(("(v) " + m("t^2-15"), p))

# (vi) 3x^2 - x - 4
check("vi", (3, -1, -4), F(4, 3), F(-1))
p = given(m("p(x)=3x^2-x-4"), "शून्यक तथा संबंध की सत्यता")
p += f"<p>मध्य पद विभाजन: {m('a\\times c=3\\times(-4)=-12')}; गुणनफल −12 और योग −1 वाली संख्याएँ: −4 और 3</p>"
p += lines("3x^2-x-4", "3x^2-4x+3x-4", "x(3x-4)+1(3x-4)", "(3x-4)(x+1)")
p += "<p>p(x) = 0 रखने पर " + m("(3x-4)(x+1)=0") + "</p>"
p += zero_from([[("3x-4", "0"), ("3x", "4"), ("x", "\\dfrac{4}{3}")], [("x+1", "0"), ("x", "-1")]])
p += therefore("अतः शून्यक " + m("\\dfrac{4}{3}") + " और −1 हैं।")
p += verify("x", "3", "-1", "-4", ("\\dfrac{4}{3}", "-1"), ["\\dfrac{4}{3}+(-1)", "\\dfrac{4-3}{3}", "\\dfrac{1}{3}"],
            ["\\dfrac{4}{3}\\times(-1)", "-\\dfrac{4}{3}"], "\\dfrac{1}{3}", "-\\dfrac{4}{3}")
P.append(("(vi) " + m("3x^2-x-4"), p))

b = SUMF + "".join(part(lab, body) for lab, body in P)
b += ans("(i) 4, −2 (ii) " + m("\\tfrac12, \\tfrac12") + " (iii) " + m("\\tfrac32, -\\tfrac13") + " (iv) 0, −2 (v) "
         + m("\\sqrt{15}, -\\sqrt{15}") + " (vi) " + m("\\tfrac43") + ", −1")
EX22 = [("निम्न द्विघात बहुपदों के शून्यक ज्ञात कीजिए और शून्यकों तथा गुणांकों के बीच के संबंध की सत्यता की जाँच कीजिए: "
         "(i) " + m("x^2-2x-8") + " (ii) " + m("4s^2-4s+1") + " (iii) " + m("6x^2-3-7x") + " (iv) " + m("4u^2+8u")
         + " (v) " + m("t^2-15") + " (vi) " + m("3x^2-x-4"), b)]

# Q2
QF = formula("द्विघात बहुपद बनाना", "यदि शून्यकों का योग S और गुणनफल P हो, तो " + m("p(x)=k\\left[x^2-Sx+P\\right]") + ", जहाँ k शून्येतर अचर है।")
R = []


def q2(lab, S, Pp, steps, k, final):
    body = given("शून्यकों का योग " + m("S=" + S) + ", गुणनफल " + m("P=" + Pp), "द्विघात बहुपद")
    body += lines("p(x)", *steps)
    if k:
        body += f"<p>भिन्न हटाने के लिए k = {k} लेने पर</p>"
    body += lines("p(x)", final)
    body += therefore("अतः अभीष्ट द्विघात बहुपद " + m(final) + " है।")
    R.append((lab, body, final))


q2("(i)", "\\dfrac{1}{4}", "-1", ["x^2-\\left(\\dfrac{1}{4}\\right)x+(-1)", "x^2-\\dfrac{x}{4}-1", "\\dfrac{4x^2-x-4}{4}"], 4, "4x^2-x-4")
q2("(ii)", "\\sqrt{2}", "\\dfrac{1}{3}", ["x^2-\\sqrt{2}\\,x+\\dfrac{1}{3}", "\\dfrac{3x^2-3\\sqrt{2}\\,x+1}{3}"], 3, "3x^2-3\\sqrt{2}\\,x+1")
q2("(iii)", "0", "\\sqrt{5}", ["x^2-0\\cdot x+\\sqrt{5}"], None, "x^2+\\sqrt{5}")
q2("(iv)", "1", "1", ["x^2-1\\cdot x+1"], None, "x^2-x+1")
q2("(v)", "-\\dfrac{1}{4}", "\\dfrac{1}{4}", ["x^2-\\left(-\\dfrac{1}{4}\\right)x+\\dfrac{1}{4}", "x^2+\\dfrac{x}{4}+\\dfrac{1}{4}", "\\dfrac{4x^2+x+1}{4}"], 4, "4x^2+x+1")
q2("(vi)", "4", "1", ["x^2-4x+1"], None, "x^2-4x+1")
b = QF + "".join(part(lab, body) for lab, body, _ in R)
b += ans(", ".join(f"{lab} {m(fin)}" for lab, _, fin in R))
EX22.append(("एक द्विघात बहुपद ज्ञात कीजिए, जिसके शून्यकों के योग तथा गुणनफल क्रमशः दी गई संख्याएँ हैं: (i) "
              + m("\\tfrac14, -1") + " (ii) " + m("\\sqrt2, \\tfrac13") + " (iii) " + m("0, \\sqrt5") + " (iv) 1, 1 (v) "
              + m("-\\tfrac14, \\tfrac14") + " (vi) 4, 1", b))

page(BASE, 2, CH, "exercise-2-1", "प्रश्नावली 2.1", "कक्षा 10 गणित · अध्याय 2: बहुपद · 1 प्रश्न (6 आलेख)", EX21,
     (BASE, "अध्याय 2"), (BASE + "exercise-2-2/", "प्रश्नावली 2.2"))
page(BASE, 2, CH, "exercise-2-2", "प्रश्नावली 2.2", "कक्षा 10 गणित · अध्याय 2: बहुपद · 2 प्रश्न", EX22,
     (BASE + "exercise-2-1/", "प्रश्नावली 2.1"), (BASE, "अध्याय 2"))
print("ok")
