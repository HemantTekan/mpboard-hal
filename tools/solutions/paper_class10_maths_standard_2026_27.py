#!/usr/bin/env python3
"""Class 10 Maths (Standard): MPBSE official model / sample paper 2026-27 (High School Exam 2027), full Hindi-medium solutions.
Run from repo root: python3 tools/solutions/paper_class10_maths_standard_2026_27.py
Writes site/hi/papers/class-10-maths-standard-model-2026-27/index.html
"""
import sys, pathlib, math
from fractions import Fraction as F
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from common import *  # noqa
from mixed_cells import *  # noqa  (mc, lines, eqs for mixed Hindi/TeX cells)
from geometry import pf  # noqa

SLUG = "class-10-maths-standard-model-2026-27"
TITLE = "कक्षा 10 गणित (स्टैंडर्ड) — माशिमं आधिकारिक मॉडल प्रश्नपत्र 2026-27 का हल"

EXTRA_CSS = """
.src{background:#fff8e1;border:1px solid #f4d27a;border-radius:12px;padding:10px 12px;margin:0 0 14px;font-size:15px}
.sh{margin:22px 0 12px;padding:10px 14px;border-radius:12px;background:#1d2433;color:#fff;font-size:19px;line-height:1.35}
.sh small{display:block;font-weight:400;font-size:14px;opacity:.85}
.mk{display:inline-block;background:#fff;color:var(--c);border:1.5px solid var(--c);border-radius:999px;padding:0 9px;font-size:13.5px;font-weight:700;margin-left:6px;vertical-align:middle}
.qtx{font-weight:600;margin:0 0 8px}
.opts{display:flex;flex-direction:column;gap:3px;margin:4px 0 8px}
.opts>span{padding:3px 10px;border-radius:8px;background:#f5f6fa;border:1px solid #e3e7f3}
.opts>span.cr{background:#e6f7ee;border-color:#6cc596;font-weight:700;color:#0f6b43}
.or{margin:20px 0 12px;text-align:center;font-weight:800;color:#c2410c;letter-spacing:.5px}
.or::before,.or::after{content:"";display:inline-block;width:28%;height:2px;background:#f3b877;vertical-align:middle;margin:0 10px}
.oq{font-weight:600;background:var(--l);border-radius:10px;padding:8px 12px;margin:0 0 10px}
.tw{overflow-x:auto;-webkit-overflow-scrolling:touch;max-width:100%;margin:8px 0 10px}
.st{border-collapse:collapse;font-variant-numeric:tabular-nums;background:#fff;font-size:15px}
.st th,.st td{border:1px solid #d5dbe8;padding:4px 6px;text-align:center;white-space:nowrap}
.st th{background:var(--l);font-weight:700;line-height:1.35;vertical-align:middle;white-space:normal}
.st tr.sum td{font-weight:700;background:#eef2f9}
.st tr.hl td{background:#fff3c4}
.mt{border-collapse:collapse;margin:6px 0;font-size:15.5px}.mt td{border-bottom:1px dashed #d5dbe8;padding:5px 6px;vertical-align:middle}
"""
CSS_P = CSS + EXTRA_CSS
PI = "\\dfrac{22}{7}"


def C(t, col="#c2185b"):
    return "\\textcolor{" + col + "}{" + t + "}"


def opts(items, correct):
    return "<div class='opts'>" + "".join(f"<span class='{'cr' if k == correct else ''}'>({k}) {v}{' ✔' if k == correct else ''}</span>"
                                          for k, v in items) + "</div>"


def sub(label, text, body):
    return part(label, f"<div class='qtx'>{text}</div>{body}")


def orq(text, body):
    return f"<div class='or'>अथवा / OR</div><div class='oq'>{text}</div>{body}"


def tbl(head, rows, sum_row=None, hl=None):
    th = "<thead><tr>" + "".join(f"<th>{h}</th>" for h in head) + "</tr></thead>"
    body = "".join(f"<tr class='{'hl' if hl == i else ''}'>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for i, r in enumerate(rows))
    if sum_row:
        body += "<tr class='sum'>" + "".join(f"<td>{c}</td>" for c in sum_row) + "</tr>"
    return f"<div class='tw'><table class='st'>{th}<tbody>{body}</tbody></table></div>"


# ------------------------------------------------------------------ SVG figure helpers
def _ln(a, b, col="#1d3a8a", w=2, dash=False):
    d = " stroke-dasharray='5 4'" if dash else ""
    return f"<line x1='{a[0]:.1f}' y1='{a[1]:.1f}' x2='{b[0]:.1f}' y2='{b[1]:.1f}' stroke='{col}' stroke-width='{w}'{d}/>"


def _tx(x, y, t, size=15, col="#111", bold=True, anchor="middle"):
    fw = " font-weight='700'" if bold else ""
    return f"<text x='{x:.1f}' y='{y:.1f}' font-size='{size}'{fw} fill='{col}' text-anchor='{anchor}'>{t}</text>"


def _dot(p, col="#1d3a8a"):
    return f"<circle cx='{p[0]:.1f}' cy='{p[1]:.1f}' r='2.6' fill='{col}'/>"


def _arc(V, P1, P2, r, label=None, lr=None, col="#c2410c", size=13):
    a1 = math.atan2(P1[1] - V[1], P1[0] - V[0])
    a2 = math.atan2(P2[1] - V[1], P2[0] - V[0])
    d = (a2 - a1 + math.pi) % (2 * math.pi) - math.pi
    s = (V[0] + r * math.cos(a1), V[1] + r * math.sin(a1))
    e_ = (V[0] + r * math.cos(a1 + d), V[1] + r * math.sin(a1 + d))
    out = f"<path d='M{s[0]:.1f},{s[1]:.1f} A{r},{r} 0 0 {1 if d > 0 else 0} {e_[0]:.1f},{e_[1]:.1f}' fill='none' stroke='{col}' stroke-width='1.6'/>"
    if label:
        lr = lr or r + 13
        am = a1 + d / 2
        out += _tx(V[0] + lr * math.cos(am), V[1] + lr * math.sin(am) + 4.5, label, size, col)
    return out


def _rt(V, P1, P2, s=10, col="#1d3a8a"):
    def u(P):
        dx, dy = P[0] - V[0], P[1] - V[1]
        L = math.hypot(dx, dy)
        return dx / L * s, dy / L * s
    (ax, ay), (bx, by) = u(P1), u(P2)
    return (f"<path d='M{V[0] + ax:.1f},{V[1] + ay:.1f} L{V[0] + ax + bx:.1f},{V[1] + ay + by:.1f} L{V[0] + bx:.1f},{V[1] + by:.1f}' "
            f"fill='none' stroke='{col}' stroke-width='1.4'/>")


def svg(W, H, parts, caption=""):
    g = (f"<svg class='graph' viewBox='0 0 {W} {H}' role='img' aria-label='{caption or 'आकृति'}' style='max-width:{min(W, 340)}px'>"
         + "".join(parts) + "</svg>")
    cap = f"<div style='font-size:.85em;color:#5a6275;margin-top:2px'>{caption}</div>" if caption else ""
    return "<div style='margin:8px 0'>" + g + cap + "</div>"


QS = []   # (num, marks label, question text, body)

# ================================================================== Q1  MCQ
P = []
assert F(7 + 5, 2) == 6
s = opts([("a", "1"), ("b", "12"), ("c", "6"), ("d", "35")], "c")
s += formula("समांतर माध्य", "दो संख्याओं " + m("a") + " और " + m("b") + " का समांतर माध्य " + m("=\\dfrac{a+b}{2}"))
s += lines("\\text{समांतर माध्य}", "\\dfrac{7+5}{2}", "\\dfrac{12}{2}", "6")
s += ans("(c) 6")
P.append(sub("(i)", "7 और 5 का समांतर माध्य है :", s))

s = opts([("a", "0"), ("b", "2"), ("c", "-2"), ("d", "-1")], "a")
s += formula("त्रिकोणमितीय मान", m("\\tan 45^\\circ=1"))
s += lines("\\dfrac{1-\\tan^2 45^\\circ}{1+\\tan^2 45^\\circ}", "\\dfrac{1-(1)^2}{1+(1)^2}", "\\dfrac{1-1}{1+1}", "\\dfrac{0}{2}", "0")
s += ans("(a) 0")
P.append(sub("(ii)", m("\\dfrac{1-\\tan^2 45^\\circ}{1+\\tan^2 45^\\circ}="), s))

s = opts([("a", "प्रतिच्छेदी है।"), ("b", "समांतर है।"), ("c", "संपाती है।"), ("d", "लंबवत है।")], "c")
s += formula("संपाती रेखाएँ", m("\\dfrac{a_1}{a_2}=\\dfrac{b_1}{b_2}=\\dfrac{c_1}{c_2}") + " हो तो रेखाएँ संपाती होती हैं।")
s += p("पहला समीकरण: " + m("2x-3y-5=0") + " (5 का पक्षांतर करके), दूसरा: " + m("6x-9y-15=0"))
s += lines("\\dfrac{a_1}{a_2}", "\\dfrac{2}{6}", "\\dfrac{1}{3}")
s += lines("\\dfrac{b_1}{b_2}", "\\dfrac{-3}{-9}", "\\dfrac{1}{3}")
s += lines("\\dfrac{c_1}{c_2}", "\\dfrac{-5}{-15}", "\\dfrac{1}{3}")
assert F(2, 6) == F(-3, -9) == F(-5, -15)
s += p("तीनों अनुपात बराबर हैं, इसलिए रेखाएँ संपाती हैं।") + ans("(c) संपाती है।")
P.append(sub("(iii)", "रैखिक समीकरणों के एक युग्म " + m("2x-3y=5") + " और " + m("6x-9y-15=0") + " द्वारा निरूपित रेखाएँ परस्पर :", s))

s = opts([("a", "25"), ("b", "-25"), ("c", "7"), ("d", "-7")], "d")
s += formula("विविक्तकर", m("D=b^2-4ac"))
s += p(m("a=1,\\ b=-3,\\ c=4"))
s += lines("D", "(-3)^2-4\\times1\\times4", "9-16", "-7")
assert (-3) ** 2 - 4 * 1 * 4 == -7
s += ans("(d) -7")
P.append(sub("(iv)", "द्विघात समीकरण " + m("x^2-3x+4=0") + " का विविक्तकर है :", s))

s = opts([("a", "1"), ("b", "4"), ("c", "अनंत"), ("d", "2")], "d")
s += p("वृत्त के बाहर स्थित किसी बिंदु से वृत्त पर ठीक दो स्पर्श रेखाएँ खींची जा सकती हैं।") + ans("(d) 2")
P.append(sub("(v)", "एक बाह्य बिंदु से एक वृत्त पर अधिकतम कितनी स्पर्श रेखाएँ खींचीं जा सकती हैं?", s))

s = opts([("a", m("4\\pi r^2")), ("b", m("\\dfrac{1}{4}\\pi r^2")), ("c", m("2\\pi r^2")), ("d", m("\\dfrac{3}{4}\\pi r^2"))], "b")
s += p("चतुर्थांश = वृत्त का चौथाई भाग (केंद्र पर कोण 90°)।")
s += lines("\\text{चतुर्थांश का क्षेत्रफल}", "\\dfrac{90^\\circ}{360^\\circ}\\times\\pi r^2", "\\dfrac{1}{4}\\pi r^2")
s += ans("(b) " + m("\\dfrac{1}{4}\\pi r^2"))
P.append(sub("(vi)", "त्रिज्या " + m("r") + " वाले वृत्त के चतुर्थांश का क्षेत्रफल है :", s))
QS.append((1, "1×6 = 6", "सही विकल्प चुनकर लिखिए :", "".join(P)))

# ================================================================== Q2  fill blanks
P = []
s = formula("त्रिकोणमितीय मान", m("\\cot 30^\\circ=\\sqrt{3}"))
s += lines("\\cot^2 30^\\circ", "(\\sqrt{3})^2", "3") + ans("3")
P.append(sub("(i)", m("\\cot^2 30^\\circ=") + " ……………", s))
P.append(sub("(ii)", "घात तीन के बहुपद को …………… बहुपद कहते हैं।", p("जिस बहुपद की घात 3 हो, जैसे " + m("x^3-2x+1") + ", वह त्रिघात बहुपद है।") + ans("त्रिघात")))
P.append(sub("(iii)", "वह घटना जिसका केवल एक ही परिणाम हो एक …………… घटना कहलाती है।", p("केवल एक परिणाम वाली घटना को प्रारंभिक (प्राथमिक) घटना कहते हैं।") + ans("प्रारंभिक")))
P.append(sub("(iv)", "द्विघात समीकरण का मानक रूप …………… है।", ans(m("ax^2+bx+c=0") + ", जहाँ " + m("a\\neq0"))))
P.append(sub("(v)", "समरूप त्रिभुजों की संगत भुजाएँ …………… होती हैं।", p("समरूप त्रिभुजों के संगत कोण बराबर और संगत भुजाएँ एक ही अनुपात में होती हैं।") + ans("समानुपाती (एक ही अनुपात में)")))
P.append(sub("(vi)", "वृत्त की स्पर्श रेखा स्पर्श बिंदु से जाने वाली त्रिज्या पर …………… होती है।", ans("लंब (लंबवत)")))
QS.append((2, "1×6 = 6", "रिक्त स्थानों की पूर्ति कीजिए :", "".join(P)))

# ================================================================== Q3  true / false
P = []
P.append(sub("(i)", "किसी वृत्त के लघु त्रिज्यखंड का क्षेत्रफल उसके संगत लघु वृत्तखंड के क्षेत्रफल से अधिक होता है।",
             lines("\\text{लघु त्रिज्यखंड}", "\\text{लघु वृत्तखंड}+\\text{त्रिभुज}") + p("इसलिए त्रिज्यखंड का क्षेत्रफल वृत्तखंड से अधिक होता है।") + ans("सत्य")))
P.append(sub("(ii)", "द्विघात बहुपद का ग्राफ एक परवलय होता है।", p(m("y=ax^2+bx+c") + " का ग्राफ ऊपर या नीचे खुलने वाला वक्र (परवलय) होता है।") + ans("सत्य")))
P.append(sub("(iii)", "दो चरों वाले रैखिक समीकरणों के आश्रित युग्म का एक अद्वितीय हल होता है।", p("आश्रित युग्म की रेखाएँ संपाती होती हैं, इसलिए अपरिमित रूप से अनेक हल होते हैं।") + ans("असत्य")))
P.append(sub("(iv)", "किसी वृत्त के किसी व्यास के सिरों पर खींची गई स्पर्श रेखाएँ लंबवत होती हैं।", p("दोनों स्पर्श रेखाएँ उसी व्यास पर लंब होती हैं, इसलिए वे परस्पर समांतर होती हैं, लंबवत नहीं।") + ans("असत्य")))
P.append(sub("(v)", "केन्द्रीय प्रवृत्ति के तीनों मापकों में आनुभविक संबंध “3 माध्यक =2 माध्य + बहुलक” होता है।", lines("3\\times\\text{माध्यक}", "\\text{बहुलक}+2\\times\\text{माध्य}") + ans("सत्य")))
P.append(sub("(vi)", "एक निश्चित घटना की प्रायिकता 1 होती है।", ans("सत्य")))
QS.append((3, "1×6 = 6", "निम्नलिखित में सत्य/असत्य लिखिए :", "".join(P)))

# ================================================================== Q4  match
colB = [("a", m("\\dfrac{1}{3}\\pi r^2 h")), ("b", m("\\dfrac{2}{3}\\pi r^3")), ("c", "7"), ("d", "2"), ("e", "1"), ("f", "5")]
colA = ["बिन्दु (-5, -7) की X-अक्ष से दूरी", m("\\sec 60^\\circ ="), "समांतर श्रेढ़ी (AP): 3, 8, 13, . . . का सार्व अंतर",
        "दो सहअभाज्य संख्याओं का HCF", "अर्धगोले का आयतन", "शंकु का आयतन"]
mt = ("<table class='mt'><tr><td><b>स्तम्भ “A”</b></td><td><b>स्तम्भ “B”</b></td></tr>"
      + "".join(f"<tr><td>({l}) {a}</td><td>({k}) {b}</td></tr>" for l, a, (k, b) in zip(["i", "ii", "iii", "iv", "v", "vi"], colA, colB)) + "</table>")
P = []
P.append(sub("(i)", colA[0], p("किसी बिंदु की X-अक्ष से दूरी = उसके y-निर्देशांक का संख्यात्मक मान।") + lines("\\text{दूरी}", "|-7|", "7") + ans("(i) → (c) 7")))
P.append(sub("(ii)", colA[1], formula("प्रयुक्त", m("\\sec\\theta=\\dfrac{1}{\\cos\\theta}")) + lines("\\sec 60^\\circ", "\\dfrac{1}{\\cos 60^\\circ}", "\\dfrac{1}{\\frac{1}{2}}", "2") + ans("(ii) → (d) 2")))
P.append(sub("(iii)", colA[2], lines("d", "8-3", "5") + ans("(iii) → (f) 5")))
P.append(sub("(iv)", colA[3], p("सहअभाज्य संख्याओं का 1 के अतिरिक्त कोई उभयनिष्ठ गुणनखंड नहीं होता।") + ans("(iv) → (e) 1")))
P.append(sub("(v)", colA[4], ans("(v) → (b) " + m("\\dfrac{2}{3}\\pi r^3"))))
P.append(sub("(vi)", colA[5], ans("(vi) → (a) " + m("\\dfrac{1}{3}\\pi r^2 h"))))
s = mt + "".join(P) + ans("(i) → (c) (ii) → (d) (iii) → (f) (iv) → (e) (v) → (b) (vi) → (a)")
QS.append((4, "1×6 = 6", "सही जोड़ी बनाइए :", s))

# ================================================================== Q5  one word
P = []
s = formula("विविक्तकर", m("D=b^2-4ac") + "; " + m("D=0") + " हो तो दो बराबर वास्तविक मूल")
s += p(m("a=1,\\ b=2,\\ c=1")) + lines("D", "(2)^2-4\\times1\\times1", "4-4", "0") + ans("दो बराबर (समान) वास्तविक मूल")
P.append(sub("(i)", "द्विघात समीकरण " + m("x^2+2x+1=0") + " के मूलों की प्रकृति लिखिए।", s))
s = p(m("-1") + " शून्यक है, इसलिए " + m("p(-1)=0"))
s += eqs(("(-1)^2-2\\times(-1)+3k", "0"), ("1+2+3k", "0"), ("3+3k", "0"), ("3k", "0-3"), ("3k", "-3"), ("k", "\\dfrac{-3}{3}"), ("k", "-1"))
assert (-1) ** 2 - 2 * (-1) + 3 * (-1) == 0
s += ans(m("k=-1"))
P.append(sub("(ii)", "यदि द्विघात बहुपद " + m("x^2-2x+3k") + " का एक शून्यक -1 है, तो " + m("k") + " का मान लिखिए।", s))
P.append(sub("(iii)", "यदि दो चरों वाले रैखिक समीकरणों के एक युग्म द्वारा प्रदर्शित रेखाएं संपाती हैं, तो उनके हलों की संख्या लिखिए।",
             p("संपाती रेखाओं का हर बिंदु उभयनिष्ठ होता है।") + ans("अपरिमित रूप से अनेक (अनंत) हल")))
s = p("मिनट की सुई 60 मिनट में 360° घूमती है।") + lines("\\text{1 मिनट में कोण}", "\\dfrac{360^\\circ}{60}", "6^\\circ") + lines("\\text{10 मिनट में कोण}", "10\\times6^\\circ", "60^\\circ") + ans("60°")
P.append(sub("(iv)", "किसी घड़ी के मिनट की सुई द्वारा 10 मिनट में बनाए गए कोण का मान लिखिए।", s))
s = lines("d", "1.7-0.6", "1.1") + lines("\\text{अगला पद}", "3.9+1.1", "5.0") + ans("5.0")
assert abs(3.9 + (1.7 - 0.6) - 5.0) < 1e-9
P.append(sub("(v)", "समांतर श्रेढ़ी (AP): 0.6, 1.7, 2.8, 3.9, . . . का अगला पद लिखिए।", s))
P.append(sub("(vi)", "दृष्टि-रेखा को परिभाषित कीजिए।", ans("प्रेक्षक की आँख को, प्रेक्षक द्वारा देखी जा रही वस्तु के बिंदु से मिलाने वाली रेखा को दृष्टि-रेखा कहते हैं।")))
QS.append((5, "1×6 = 6", "एक शब्द/वाक्य में उत्तर लिखिए :", "".join(P)))

# ================================================================== Q6  LCM
s = given("संख्याएँ 6, 72 और 120", "अभाज्य गुणनखंड विधि से LCM")
s += ladders(6, 72, 120)
s += p("LCM = प्रत्येक अभाज्य गुणनखंड की सबसे बड़ी घात का गुणनफल (2 तीन बार, 3 दो बार, 5 एक बार)।")
s += lines("LCM", "2\\times2\\times2\\times3\\times3\\times5", "8\\times9\\times5", "72\\times5", "360")
assert math.lcm(6, 72, 120) == 360
s += ans("LCM = 360")
QS.append((6, "2", "अभाज्य गुणनखंड विधि द्वारा 6, 72 और 120 का LCM ज्ञात कीजिए।", s))

# ================================================================== Q7  quadratic polynomial
s = given("शून्यकों का योग " + m("\\alpha+\\beta=\\dfrac{3}{4}") + "<br>शून्यकों का गुणनफल " + m("\\alpha\\beta=\\dfrac{5}{6}"), "द्विघात बहुपद")
s += formula("द्विघात बहुपद", m("p(x)=k\\left[x^2-(\\alpha+\\beta)x+\\alpha\\beta\\right]") + ", जहाँ " + m("k") + " कोई अशून्य वास्तविक संख्या है")
s += lines("p(x)", "k\\left[x^2-\\dfrac{3}{4}x+\\dfrac{5}{6}\\right]")
s += p(m("k=12") + " लेकर सभी पदों को 12 से गुणा करने पर,")
s += lines("p(x)", "12\\times x^2-12\\times\\dfrac{3}{4}x+12\\times\\dfrac{5}{6}", "12x^2-3\\times3x+2\\times5", "12x^2-9x+10")
assert F(9, 12) == F(3, 4) and F(10, 12) == F(5, 6)
s += "<div class='vt'>जाँच:</div>" + lines("\\alpha+\\beta", "-\\dfrac{b}{a}", "\\dfrac{9}{12}", "\\dfrac{3}{4}") + lines("\\alpha\\beta", "\\dfrac{c}{a}", "\\dfrac{10}{12}", "\\dfrac{5}{6}") + ok("✔")
s += ans(m("12x^2-9x+10"))
QS.append((7, "2", "एक द्विघात बहुपद ज्ञात कीजिए, जिसके शून्यकों का योग तथा गुणनफल क्रमशः " + m("\\dfrac{3}{4}") + " और " + m("\\dfrac{5}{6}") + " हैं।", s))

# ================================================================== Q8  roots
s = given("द्विघात समीकरण " + m("\\sqrt{2}x^2+7x+5\\sqrt{2}=0"), "समीकरण के मूल")
s += p("मध्य पद विभक्त करने के लिए पहले " + m("a\\times c") + " ज्ञात करते हैं:")
s += lines("a\\times c", "\\sqrt{2}\\times5\\sqrt{2}", "5\\times\\sqrt{2}\\times\\sqrt{2}", "5\\times2", "10")
s += p("ऐसी दो संख्याएँ चाहिए जिनका योग 7 और गुणनफल 10 हो: 5 और 2 " + m("(5+2=7,\\ 5\\times2=10)"))
s += lines("\\sqrt{2}x^2+7x+5\\sqrt{2}", "0")
s += lines("\\sqrt{2}x^2+5x+2x+5\\sqrt{2}", "0")
s += p(m("2x=\\sqrt{2}\\times\\sqrt{2}x") + " लिखने पर,")
s += lines("x(\\sqrt{2}x+5)+\\sqrt{2}(\\sqrt{2}x+5)", "0")
s += lines("(\\sqrt{2}x+5)(x+\\sqrt{2})", "0")
s += p("प्रत्येक गुणनखंड को अलग-अलग शून्य रखने पर,")
s += eqs(("\\sqrt{2}x+5", "0"), ("\\sqrt{2}x", "-5"), ("x", "\\dfrac{-5}{\\sqrt{2}}"), ("x", "\\dfrac{-5}{\\sqrt{2}}\\times\\dfrac{\\sqrt{2}}{\\sqrt{2}}"), ("x", "-\\dfrac{5\\sqrt{2}}{2}"))
s += eqs(("x+\\sqrt{2}", "0"), ("x", "-\\sqrt{2}"))
r2 = math.sqrt(2)
for xx in (-5 / r2, -r2):
    assert abs(r2 * xx * xx + 7 * xx + 5 * r2) < 1e-9
s += ans("मूल " + m("-\\dfrac{5\\sqrt{2}}{2}") + " और " + m("-\\sqrt{2}") + " हैं।")
QS.append((8, "2", "वर्ग समीकरण " + m("\\sqrt{2}x^2+7x+5\\sqrt{2}=0") + " के मूल ज्ञात कीजिए।", s))

# ================================================================== Q9  AP term
s = given("AP: 3, 8, 13, 18, …<br>" + m("a=3") + ", " + m("a_n=78"), m("n") + " (पद की स्थिति)")
s += formula("n वाँ पद", m("a_n=a+(n-1)d"))
s += lines("d", "8-3", "5")
s += eqs(("a+(n-1)d", "a_n"), ("3+(n-1)\\times5", "78"), ("(n-1)\\times5", "78-3"), ("(n-1)\\times5", "75"),
         ("n-1", "\\dfrac{75}{5}"), ("n-1", "15"), ("n", "15+1"), ("n", "16"))
assert 3 + 15 * 5 == 78
s += ans("78, दी गई AP का 16वाँ पद है।")
QS.append((9, "2", "समांतर श्रेढ़ी (AP) : 3, 8, 13, 18, . . . का कौन सा पद 78 है?", s))

# ================================================================== Q10  BPT
A_, B_, C_ = (150, 22), (30, 205), (295, 205)
D_ = (A_[0] + (B_[0] - A_[0]) * 0.4, A_[1] + (B_[1] - A_[1]) * 0.4)
E_ = (A_[0] + (C_[0] - A_[0]) * 0.4, A_[1] + (C_[1] - A_[1]) * 0.4)
f10 = svg(330, 230, [_ln(A_, B_), _ln(B_, C_), _ln(C_, A_), _ln(D_, E_, "#c2410c"),
                     _dot(A_), _dot(B_), _dot(C_), _dot(D_), _dot(E_),
                     _tx(A_[0], A_[1] - 6, "A"), _tx(B_[0] - 10, B_[1] + 16, "B"), _tx(C_[0] + 10, C_[1] + 16, "C"),
                     _tx(D_[0] - 13, D_[1] + 5, "D"), _tx(E_[0] + 13, E_[1] + 5, "E"),
                     _tx(105, 58, "2 cm", 12.5, "#b4232a", False, "end"), _tx(52, 155, "3 cm", 12.5, "#b4232a", False, "end"),
                     _tx(197, 58, "4 cm", 12.5, "#b4232a", False, "start"), _tx(266, 155, "EC = ?", 12.5, "#b4232a", False, "start")],
          "ΔABC में DE ∥ BC")
s = given("ΔABC में DE ∥ BC<br>AD = 2 cm, DB = 3 cm, AE = 4 cm", "EC")
s += f10 + formula("आधारभूत समानुपातिकता प्रमेय", "त्रिभुज में DE ∥ BC हो तो " + m("\\dfrac{AD}{DB}=\\dfrac{AE}{EC}"))
s += eqs(("\\dfrac{AD}{DB}", "\\dfrac{AE}{EC}"), ("\\dfrac{2}{3}", "\\dfrac{4}{EC}"))
s += p("वज्र-गुणन (cross-multiplication) करने पर,")
s += eqs(("2\\times EC", "3\\times4"), ("2\\times EC", "12"), ("EC", "\\dfrac{12}{2}"), ("EC", "6\\ \\text{cm}"))
assert F(2, 3) == F(4, 6)
s += ans("EC = 6 cm")
QS.append((10, "2", "किसी ΔABC की भुजाओं AB और AC पर क्रमशः बिंदु D और E इस प्रकार स्थित हैं कि DE ∥ BC एवं AD=2 cm, DB=3 cm, AE=4 cm, तो EC ज्ञात कीजिए।", s))

# ================================================================== Q11  trig identity
s = given("LHS = " + m("(\\sec\\theta+\\tan\\theta)(1-\\sin\\theta)"), "LHS = RHS = " + m("\\cos\\theta"))
s += formula("प्रयुक्त", "", [m("\\sec\\theta=\\dfrac{1}{\\cos\\theta}"), m("\\tan\\theta=\\dfrac{\\sin\\theta}{\\cos\\theta}"),
                               m("\\sin^2\\theta+\\cos^2\\theta=1") + " ⇒ " + m("1-\\sin^2\\theta=\\cos^2\\theta")])
s += lines("\\text{LHS}", "(\\sec\\theta+\\tan\\theta)(1-\\sin\\theta)",
           "\\left(\\dfrac{1}{\\cos\\theta}+\\dfrac{\\sin\\theta}{\\cos\\theta}\\right)(1-\\sin\\theta)",
           "\\dfrac{1+\\sin\\theta}{\\cos\\theta}\\times(1-\\sin\\theta)",
           "\\dfrac{(1+\\sin\\theta)(1-\\sin\\theta)}{\\cos\\theta}",
           "\\dfrac{1-\\sin\\theta+\\sin\\theta-\\sin^2\\theta}{\\cos\\theta}",
           "\\dfrac{1-\\sin^2\\theta}{\\cos\\theta}",
           "\\dfrac{\\cos^2\\theta}{\\cos\\theta}",
           "\\cos\\theta", "\\text{RHS}")
for th in (0.3, 0.9, 1.2):
    close((1 / math.cos(th) + math.tan(th)) * (1 - math.sin(th)), math.cos(th))
s += ok("इति सिद्धम्") + ans("LHS = RHS, अतः " + m("(\\sec\\theta+\\tan\\theta)(1-\\sin\\theta)=\\cos\\theta") + " सिद्ध हुआ।")
QS.append((11, "2", "सिद्ध कीजिए " + m("(\\sec\\theta+\\tan\\theta)(1-\\sin\\theta)=\\cos\\theta"), s))

# ================================================================== Q12  tangent length
O, Aa = (105, 130), (265, 130)
R = 90
Pp = (O[0] + R * 0.6, O[1] - R * 0.8)
f12 = svg(310, 235, [f"<circle cx='{O[0]}' cy='{O[1]}' r='{R}' fill='none' stroke='#1d3a8a' stroke-width='2'/>",
                     _ln(O, Aa), _ln(O, Pp, "#0f7a4c"), _ln(Pp, Aa, "#c2410c"), _rt(Pp, O, Aa, 10),
                     _dot(O), _dot(Aa), _dot(Pp),
                     _tx(O[0] - 4, O[1] + 18, "O"), _tx(Aa[0] + 12, Aa[1] + 5, "A"), _tx(Pp[0] + 2, Pp[1] - 9, "P"),
                     _tx(125, 98, "r", 14, "#0f7a4c"), _tx(222, 82, "4 cm", 12.5, "#b4232a", False, "start"),
                     _tx(232, 150, "5 cm", 12.5, "#b4232a", False)],
          "केंद्र O, स्पर्श रेखा AP, ∠OPA = 90°")
s = given("OA = 5 cm (केंद्र से बिंदु A की दूरी)<br>AP = 4 cm (स्पर्श रेखा की लंबाई)", "त्रिज्या OP = r")
s += f12 + formula("प्रयुक्त", "स्पर्श बिंदु पर त्रिज्या स्पर्श रेखा पर लंब होती है, अतः " + m("\\angle OPA=90^\\circ"), [
    "पाइथागोरस प्रमेय: " + m("(\\text{कर्ण})^2=(\\text{लंब})^2+(\\text{आधार})^2").replace("\\text{कर्ण}", "OA").replace("\\text{लंब}", "OP").replace("\\text{आधार}", "AP")])
s += p("समकोण ΔOPA में,")
s += eqs(("OA^2", "OP^2+AP^2"), ("5^2", "r^2+4^2"), ("25", "r^2+16"), ("25-16", "r^2"), ("r^2", "9"))
s += lines("r", "\\sqrt{9}", "\\sqrt{\\underline{3\\times3}}", "3\\ \\text{cm}")
assert 3 ** 2 + 4 ** 2 == 5 ** 2
s += ans("वृत्त की त्रिज्या 3 cm है।")
QS.append((12, "2", "एक बिंदु A से, जो एक वृत्त के केंद्र से 5 cm दूरी पर है, वृत्त पर स्पर्श रेखा की लंबाई 4 cm है। वृत्त की त्रिज्या ज्ञात कीजिए।", s))

# ================================================================== Q13  equidistant point
s = given("A(2, −5) और B(−2, 9)<br>बिंदु P, X-अक्ष पर है, अतः P(" + m("x") + ", 0)", "P जिसके लिए PA = PB")
s += formula("प्रयुक्त", "", ["दूरी सूत्र: " + m("d^2=(x_2-x_1)^2+(y_2-y_1)^2"), m("(a-b)^2=a^2-2ab+b^2"), m("(a+b)^2=a^2+2ab+b^2")])
s += p("PA = PB है, इसलिए " + m("PA^2=PB^2") + "।")
s += lines("PA^2", "(x-2)^2+(0-(-5))^2", "(x-2)^2+(5)^2", "x^2-2\\times x\\times2+2^2+25", "x^2-4x+4+25", "x^2-4x+29")
s += lines("PB^2", "(x-(-2))^2+(0-9)^2", "(x+2)^2+(-9)^2", "x^2+2\\times x\\times2+2^2+81", "x^2+4x+4+81", "x^2+4x+85")
s += eqs(("PA^2", "PB^2"), ("x^2-4x+29", "x^2+4x+85"))
s += p("दोनों पक्षों से " + m("x^2") + " कटने पर, फिर " + m("4x") + " को बाएँ और 29 को दाएँ पक्षांतर करने पर,")
s += eqs(("x^2-4x-x^2-4x", "85-29"), ("-4x-4x", "85-29"), ("-8x", "56"), ("x", "\\dfrac{56}{-8}"), ("x", "-7"))
assert (-7 - 2) ** 2 + 25 == (-7 + 2) ** 2 + 81 == 106
s += ans("X-अक्ष पर अभीष्ट बिंदु (−7, 0) है।")
QS.append((13, "2", "X-अक्ष पर वह बिंदु ज्ञात कीजिए जो (2, -5) और (-2, 9) से समदूरस्थ है।", s))

# ================================================================== Q14  probability
sqs = [k * k for k in range(1, 10)]
assert len([n for n in range(1, 91) if int(math.isqrt(n)) ** 2 == n]) == 9
s = given("डिस्क 1 से 90 तक, कुल 90", "P(पूर्ण वर्ग संख्या)")
s += formula("प्रायिकता", m("P(E)=\\dfrac{\\text{अनुकूल परिणामों की संख्या}}{\\text{कुल परिणामों की संख्या}}").replace("\\text{अनुकूल परिणामों की संख्या}", "n(E)").replace("\\text{कुल परिणामों की संख्या}", "n(S)"))
s += lines("n(S)", "90")
s += p("1 से 90 तक पूर्ण वर्ग संख्याएँ: " + ", ".join(f"{k}² = {k*k}" for k in range(1, 10)) + " (10² = 100 > 90)")
s += lines("n(E)", "9")
s += lines("P(E)", "\\dfrac{9}{90}", "\\dfrac{1}{10}")
s += ans(m("\\dfrac{1}{10}"))
QS.append((14, "2", "एक पेटी में 90 डिस्क हैं, जिन पर 1 से 90 तक संख्याएँ अंकित हैं। यदि पेटी में से एक डिस्क यादृच्छया निकाली जाती है तो डिस्क पर अंकित संख्या के पूर्ण वर्ग संख्या होने की प्रायिकता ज्ञात कीजिए।", s))

# ================================================================== Q15  section formula
s = given("A(−3, 10), B(6, −8)<br>बिंदु P(−1, 6), रेखाखंड AB पर", "अनुपात " + m("m_1:m_2"))
s += formula("विभाजन सूत्र", m("x=\\dfrac{m_1x_2+m_2x_1}{m_1+m_2}") + ", " + m("y=\\dfrac{m_1y_2+m_2y_1}{m_1+m_2}"))
s += p(m("x_1=-3,\\ y_1=10,\\ x_2=6,\\ y_2=-8,\\ x=-1"))
s += eqs(("\\dfrac{m_1\\times6+m_2\\times(-3)}{m_1+m_2}", "-1"), ("\\dfrac{6m_1-3m_2}{m_1+m_2}", "-1"))
s += p("वज्र-गुणन करने पर,")
s += eqs(("6m_1-3m_2", "-1\\times(m_1+m_2)"), ("6m_1-3m_2", "-m_1-m_2"))
s += p("पक्षांतर करने पर (" + m("-m_1") + " बाएँ, " + m("-3m_2") + " दाएँ),")
s += eqs(("6m_1+m_1", "-m_2+3m_2"), ("7m_1", "2m_2"), ("\\dfrac{m_1}{m_2}", "\\dfrac{2}{7}"))
s += "<div class='vt'>जाँच (y-निर्देशांक से):</div>" + lines("y", "\\dfrac{2\\times(-8)+7\\times10}{2+7}", "\\dfrac{-16+70}{9}", "\\dfrac{54}{9}", "6") + ok("✔ y = 6 मिला")
assert F(2 * 6 + 7 * -3, 9) == -1 and F(2 * -8 + 7 * 10, 9) == 6
s += ans("बिंदु (−1, 6) रेखाखंड को 2 : 7 के अनुपात में (अंतः) विभाजित करता है।")
QS.append((15, "2", "वह अनुपात ज्ञात कीजिए जिसमें बिंदुओं (-3, 10) और (6, -8) को मिलाने वाले रेखाखण्ड को बिंदु (-1, 6) विभाजित करता है।", s))

# ================================================================== Q16  similar triangles (figure as in paper)
P16, Q16, R16, S16 = (55, 80), (55, 165), (285, 35), (285, 230)


def _ix(a, b, c, d):
    x1, y1 = a; x2, y2 = b; x3, y3 = c; x4, y4 = d
    den = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / den
    return (x1 + t * (x2 - x1), y1 + t * (y2 - y1))


O16 = _ix(P16, S16, Q16, R16)


def fig16(marks=False):
    el = [_ln(P16, Q16), _ln(R16, S16), _ln(P16, S16), _ln(Q16, R16)]
    if marks:
        el += [_arc(P16, Q16, O16, 16, col="#c2410c"), _arc(S16, R16, O16, 16, col="#c2410c"),
               _arc(Q16, P16, O16, 14, col="#0f7a4c"), _arc(Q16, P16, O16, 19, col="#0f7a4c"),
               _arc(R16, S16, O16, 14, col="#0f7a4c"), _arc(R16, S16, O16, 19, col="#0f7a4c"),
               _arc(O16, P16, Q16, 14, col="#7b3fe4"), _arc(O16, S16, R16, 14, col="#7b3fe4")]
    el += [_dot(p_) for p_ in (P16, Q16, R16, S16, O16)]
    el += [_tx(P16[0] - 4, P16[1] - 9, "P"), _tx(Q16[0] - 4, Q16[1] + 19, "Q"), _tx(R16[0], R16[1] - 8, "R"),
           _tx(S16[0], S16[1] + 18, "S"), _tx(O16[0] + 2, O16[1] + 22, "O")]
    return svg(330, 255, el, "PQ ∥ RS" + ("; बराबर कोण एक जैसे चिह्नों से दिखाए गए हैं" if marks else ""))


s = given("PQ ∥ RS; PS और QR बिंदु O पर काटती हैं", "ΔPOQ ~ ΔSOR")
s += fig16(True) + formula("AA समरूपता कसौटी", "यदि एक त्रिभुज के दो कोण दूसरे त्रिभुज के दो कोणों के बराबर हों, तो दोनों त्रिभुज समरूप होते हैं।")
s += pf(("PQ ∥ RS और PS तिर्यक रेखा है, इसलिए " + m("\\angle QPO=\\angle RSO") + " …(1)", "एकांतर कोण"),
        ("PQ ∥ RS और QR तिर्यक रेखा है, इसलिए " + m("\\angle PQO=\\angle SRO") + " …(2)", "एकांतर कोण"),
        (m("\\angle POQ=\\angle SOR") + " …(3)", "शीर्षाभिमुख कोण"),
        ("(1), (2) और (3) से ΔPOQ और ΔSOR के संगत कोण बराबर हैं, इसलिए " + m("\\triangle POQ\\sim\\triangle SOR"), "AA (AAA) समरूपता कसौटी"))
s += ok("इति सिद्धम्") + ans("ΔPOQ ~ ΔSOR (AA समरूपता से)")
QS.append((16, "2", "दी गई आकृति में, यदि PQ ∥ RS, तो सिद्ध कीजिए कि ΔPOQ ~ ΔSOR है।" + fig16(False), s))

# ================================================================== Q17  two coins
s = given("दो भिन्न-भिन्न सिक्के एक साथ उछाले गए", "P(कम से कम एक चित)")
s += p("चित = H, पट = T")
s += lines("S", "\\{HH,\\ HT,\\ TH,\\ TT\\}") + lines("n(S)", "4")
s += p("कम से कम एक चित वाले परिणाम: HH, HT, TH")
s += lines("n(E)", "3") + formula("प्रायिकता", m("P(E)=\\dfrac{n(E)}{n(S)}")) + lines("P(E)", "\\dfrac{3}{4}")
s += ans(m("\\dfrac{3}{4}"))
QS.append((17, "2", "हरप्रीत दो भिन्न-भिन्न सिक्कों को एक साथ उछालती है। इसकी क्या प्रायिकता है कि वह कम से कम एक चित प्राप्त करेगी?", s))

# ================================================================== Q18  sector / quadrant
Oc, Rc = (150, 125), 95
Ap = (Oc[0] + Rc, Oc[1])
Bp = (Oc[0] + Rc * math.cos(math.radians(-60)), Oc[1] + Rc * math.sin(math.radians(-60)))
f18 = svg(300, 240, [f"<circle cx='{Oc[0]}' cy='{Oc[1]}' r='{Rc}' fill='none' stroke='#1d3a8a' stroke-width='2'/>",
                     f"<path d='M{Oc[0]},{Oc[1]} L{Ap[0]},{Ap[1]} A{Rc},{Rc} 0 0 0 {Bp[0]:.1f},{Bp[1]:.1f} Z' fill='#fde2c4' stroke='#c2410c' stroke-width='2'/>",
                     _arc(Oc, Ap, Bp, 22, "60°", 38), _dot(Oc), _dot(Ap), _dot(Bp),
                     _tx(Oc[0] - 12, Oc[1] + 6, "O"), _tx(Ap[0] + 12, Ap[1] + 5, "A"), _tx(Bp[0] + 8, Bp[1] - 8, "B"),
                     _tx(195, 142, "6 cm", 12.5, "#b4232a", False)], "त्रिज्यखंड OAB, θ = 60°")
s = given(m("r=6\\ \\text{cm}") + ", " + m("\\theta=60^\\circ") + ", " + m("\\pi=" + PI), "त्रिज्यखंड का क्षेत्रफल")
s += f18 + formula("त्रिज्यखंड का क्षेत्रफल", m("\\dfrac{\\theta}{360^\\circ}\\times\\pi r^2"))
s += lines("\\text{क्षेत्रफल}", "\\dfrac{60}{360}\\times\\dfrac{22}{7}\\times6\\times6", "\\dfrac{1}{6}\\times\\dfrac{22}{7}\\times36",
           "\\dfrac{22}{7}\\times6", "\\dfrac{132}{7}", "18.86\\ \\text{cm}^2")
assert F(60, 360) * F(22, 7) * 36 == F(132, 7)
s += ans(m("\\dfrac{132}{7}\\ \\text{cm}^2=18\\tfrac{6}{7}\\ \\text{cm}^2") + " ≈ 18.86 cm²")
Bq = (Oc[0], Oc[1] - Rc)
f18b = svg(300, 240, [f"<circle cx='{Oc[0]}' cy='{Oc[1]}' r='{Rc}' fill='none' stroke='#1d3a8a' stroke-width='2'/>",
                      f"<path d='M{Oc[0]},{Oc[1]} L{Ap[0]},{Ap[1]} A{Rc},{Rc} 0 0 0 {Bq[0]},{Bq[1]} Z' fill='#d6f0e3' stroke='#0f7a4c' stroke-width='2'/>",
                      _rt(Oc, Ap, Bq, 12), _dot(Oc), _tx(Oc[0] - 12, Oc[1] + 6, "O"), _tx(195, 142, "r", 14, "#b4232a")],
           "चतुर्थांश (केंद्र पर 90°)")
s2 = given("परिधि " + m("2\\pi r=22\\ \\text{cm}") + ", " + m("\\pi=" + PI), "चतुर्थांश का क्षेत्रफल")
s2 += f18b + formula("प्रयुक्त", "", ["परिधि " + m("=2\\pi r"), "चतुर्थांश का क्षेत्रफल " + m("=\\dfrac{1}{4}\\pi r^2")])
s2 += eqs(("2\\pi r", "22"), ("2\\times\\dfrac{22}{7}\\times r", "22"), ("\\dfrac{44}{7}\\times r", "22"), ("r", "22\\times\\dfrac{7}{44}"), ("r", "\\dfrac{154}{44}"),
          ("r", "\\dfrac{7}{2}"), ("r", "3.5\\ \\text{cm}"))
s2 += lines("\\text{क्षेत्रफल}", "\\dfrac{1}{4}\\times\\dfrac{22}{7}\\times\\dfrac{7}{2}\\times\\dfrac{7}{2}", "\\dfrac{1}{4}\\times\\dfrac{22\\times7}{2\\times2}",
            "\\dfrac{1}{4}\\times\\dfrac{154}{4}", "\\dfrac{154}{16}", "\\dfrac{77}{8}", "9.625\\ \\text{cm}^2")
assert F(1, 4) * F(22, 7) * F(7, 2) ** 2 == F(77, 8)
s2 += ans(m("\\dfrac{77}{8}\\ \\text{cm}^2=9.625\\ \\text{cm}^2"))
s += orq("एक वृत्त के चतुर्थांश का क्षेत्रफल ज्ञात कीजिए, जिसकी परिधि 22 cm है।", s2)
QS.append((18, "3", "6 cm त्रिज्या वाले एक वृत्त के त्रिज्यखंड का क्षेत्रफल ज्ञात कीजिए, जो केंद्र पर 60° का कोण अंतरित करता है।", s))

# ================================================================== Q19  √3 irrational / 6^n
s = given(m("\\sqrt{3}"), m("\\sqrt{3}") + " अपरिमेय है")
s += formula("प्रमेय", "यदि अभाज्य संख्या " + m("p") + ", " + m("a^2") + " को विभाजित करे, तो " + m("p") + ", " + m("a") + " को भी विभाजित करती है।")
s += p("माना " + m("\\sqrt{3}") + " परिमेय है (विरोधाभास विधि)। तब ऐसे सहअभाज्य पूर्णांक " + m("a") + " और " + m("b\\ (b\\neq0)") + " होंगे कि")
s += eqs(("\\sqrt{3}", "\\dfrac{a}{b}"), ("\\sqrt{3}\\,b", "a"))
s += p("दोनों पक्षों का वर्ग करने पर,")
s += eqs(("(\\sqrt{3}\\,b)^2", "a^2"), ("3b^2", "a^2"))
s += p("अतः " + m("a^2") + ", 3 से विभाज्य है, इसलिए प्रमेय से " + m("a") + " भी 3 से विभाज्य है। माना " + m("a=3c") + "।")
s += eqs(("3b^2", "(3c)^2"), ("3b^2", "9c^2"), ("b^2", "\\dfrac{9c^2}{3}"), ("b^2", "3c^2"))
s += p("अतः " + m("b^2") + ", 3 से विभाज्य है, इसलिए " + m("b") + " भी 3 से विभाज्य है।")
s += p("इस प्रकार " + m("a") + " और " + m("b") + " दोनों का एक उभयनिष्ठ गुणनखंड 3 है। यह हमारी मान्यता (" + m("a") + " और " + m("b") + " सहअभाज्य हैं) का विरोधाभास है।")
s += ok("अतः हमारी मान्यता गलत है, और " + m("\\sqrt{3}") + " एक अपरिमेय संख्या है। इति सिद्धम्")
s += ans(m("\\sqrt{3}") + " अपरिमेय संख्या है।")
s2 = given("संख्या " + m("6^n") + ", " + m("n") + " प्राकृत संख्या", "क्या " + m("6^n") + " का अंतिम अंक 0 हो सकता है?")
s2 += formula("अंकगणित की आधारभूत प्रमेय", "प्रत्येक भाज्य संख्या को अभाज्य संख्याओं के गुणनफल के रूप में केवल एक ही प्रकार (अद्वितीय रूप) से व्यक्त किया जा सकता है।")
s2 += p("यदि कोई संख्या अंक 0 पर समाप्त हो, तो वह 10 से विभाज्य होगी। ") + lines("10", "2\\times5")
s2 += p("अर्थात् उसके अभाज्य गुणनखंडों में 2 और 5 दोनों होने चाहिए।")
s2 += lines("6", "2\\times3") + lines("6^n", "(2\\times3)^n", "2^n\\times3^n")
s2 += p(m("6^n") + " के अभाज्य गुणनखंडों में केवल 2 और 3 हैं, अभाज्य संख्या 5 नहीं है। आधारभूत प्रमेय (अद्वितीयता) से इसमें 5 कभी नहीं आ सकता।")
assert all(pow(6, n, 10) == 6 for n in range(1, 30))
s2 += ok("अतः किसी भी प्राकृत संख्या n के लिए " + m("6^n") + " अंक 0 पर समाप्त नहीं हो सकती।")
s2 += ans("नहीं, " + m("6^n") + " किसी भी प्राकृत संख्या " + m("n") + " के लिए अंक 0 पर समाप्त नहीं होती।")
s += orq("जाँच कीजिए कि क्या किसी प्राकृत संख्या " + m("n") + " के लिए, संख्या " + m("6^n") + " अंक 0 पर समाप्त हो सकती है।", s2)
QS.append((19, "3", "सिद्ध कीजिए कि " + m("\\sqrt{3}") + " एक अपरिमेय संख्या है।", s))

# ================================================================== Q20  cube + hemisphere / toy
# cube (oblique) with hemisphere on top face
x0, y0, a, dx, dy = 50, 105, 140, 45, -32
F1, F2, F3, F4 = (x0, y0), (x0 + a, y0), (x0 + a, y0 + a), (x0, y0 + a)
B1, B2, B3 = (x0 + dx, y0 + dy), (x0 + a + dx, y0 + dy), (x0 + a + dx, y0 + a + dy)
cx, cy = x0 + a / 2 + dx / 2, y0 + dy / 2
rx, ry = a / 2, 16
dome = f"<path d='M{cx - rx},{cy} A{rx},{rx * 0.95} 0 0 1 {cx + rx},{cy}' fill='#d6e6fb' stroke='#1d3a8a' stroke-width='2'/>"
base = f"<ellipse cx='{cx}' cy='{cy}' rx='{rx}' ry='{ry}' fill='#eef4fd' stroke='#1d3a8a' stroke-width='1.4' stroke-dasharray='5 4'/>"
f20 = svg(300, 270, [f"<polygon points='{F1[0]},{F1[1]} {B1[0]},{B1[1]} {B2[0]},{B2[1]} {F2[0]},{F2[1]}' fill='#eef4fd' stroke='#1d3a8a' stroke-width='2'/>",
                     f"<polygon points='{F2[0]},{F2[1]} {B2[0]},{B2[1]} {B3[0]},{B3[1]} {F3[0]},{F3[1]}' fill='#dfe9f8' stroke='#1d3a8a' stroke-width='2'/>",
                     f"<rect x='{x0}' y='{y0}' width='{a}' height='{a}' fill='#f7faff' stroke='#1d3a8a' stroke-width='2'/>",
                     base, dome, _ln((cx, cy), (cx + rx, cy), "#c2410c", 1.6),
                     _tx(cx + rx / 2, cy - 5, "r", 13, "#c2410c"),
                     _tx(x0 + a / 2, y0 + a + 18, "7 cm", 12.5, "#b4232a", False), _tx(x0 - 6, y0 + a / 2 + 4, "7 cm", 12.5, "#b4232a", False, "end"),
                     _tx(B3[0] + 6, (B2[1] + B3[1]) / 2 + 30, "7 cm", 12.5, "#b4232a", False, "start")],
          "7 cm भुजा का घन, ऊपर अर्धगोला")
s = given("घन की भुजा " + m("a=7\\ \\text{cm}") + ", " + m("\\pi=" + PI), "(i) अर्धगोले का अधिकतम व्यास (ii) ठोस का पृष्ठीय क्षेत्रफल")
s += f20 + p("अर्धगोला घन के ऊपरी फलक (7 cm × 7 cm) पर रखा है, इसलिए उसका व्यास घन की भुजा से बड़ा नहीं हो सकता।")
s += lines("\\text{अधिकतम व्यास}", "7\\ \\text{cm}") + lines("r", "\\dfrac{7}{2}\\ \\text{cm}")
s += formula("प्रयुक्त", "", ["घन का कुल पृष्ठीय क्षेत्रफल " + m("=6a^2"), "वृत्त का क्षेत्रफल " + m("=\\pi r^2"), "अर्धगोले का वक्र पृष्ठीय क्षेत्रफल " + m("=2\\pi r^2")])
s += p("ठोस का पृष्ठ = घन का पृष्ठ − अर्धगोले के नीचे ढका वृत्त + अर्धगोले का वक्र पृष्ठ")
s += lines("\\text{पृष्ठीय क्षेत्रफल}", "6a^2-\\pi r^2+2\\pi r^2", "6a^2+\\pi r^2")
s += lines("6a^2", "6\\times7\\times7", "6\\times49", "294\\ \\text{cm}^2")
s += lines("\\pi r^2", "\\dfrac{22}{7}\\times\\dfrac{7}{2}\\times\\dfrac{7}{2}", "\\dfrac{22\\times7}{2\\times2}", "\\dfrac{154}{4}", "38.5\\ \\text{cm}^2")
s += lines("\\text{पृष्ठीय क्षेत्रफल}", "294+38.5", "332.5\\ \\text{cm}^2")
assert 6 * 49 + F(22, 7) * F(49, 4) == F(665, 2)
s += ans("(i) अधिकतम व्यास = 7 cm (ii) ठोस का पृष्ठीय क्षेत्रफल = 332.5 cm²")
# toy
tc, tr = (150, 120), 75
toy = [f"<path d='M{tc[0] - tr},{tc[1]} A{tr},{tr} 0 0 0 {tc[0] + tr},{tc[1]} Z' fill='#d6f0e3' stroke='#0f7a4c' stroke-width='2'/>",
       f"<polygon points='{tc[0] - tr},{tc[1]} {tc[0]},{tc[1] - tr} {tc[0] + tr},{tc[1]}' fill='#fde2c4' stroke='#c2410c' stroke-width='2'/>",
       f"<ellipse cx='{tc[0]}' cy='{tc[1]}' rx='{tr}' ry='12' fill='none' stroke='#1d3a8a' stroke-width='1.4' stroke-dasharray='5 4'/>",
       _ln(tc, (tc[0], tc[1] - tr), "#1d3a8a", 1.6, True), _ln(tc, (tc[0] + tr, tc[1]), "#1d3a8a", 1.6),
       _rt(tc, (tc[0], 0), (300, tc[1]), 9), _dot(tc),
       _tx(tc[0] + 7, tc[1] - 30, "h", 14, "#b4232a", True, "start"), _tx(tc[0] + 38, tc[1] + 30, "r", 14, "#b4232a"),
       _tx(tc[0], tc[1] + 50, "अर्धगोला", 12, "#0f7a4c", False), _tx(tc[0] + 52, tc[1] - 46, "शंकु", 12, "#c2410c", False, "start")]
f20b = svg(300, 215, toy, "खिलौना: अर्धगोले पर शंकु (h = 2 cm, r = 2 cm)")
s2 = given("शंकु की ऊँचाई " + m("h=2\\ \\text{cm}") + "<br>आधार का व्यास 4 cm, " + m("\\pi=" + PI), "खिलौने का आयतन")
s2 += f20b + lines("r", "\\dfrac{4}{2}", "2\\ \\text{cm}") + p("(अर्धगोले की त्रिज्या भी 2 cm)")
s2 += formula("प्रयुक्त", "", ["अर्धगोले का आयतन " + m("=\\dfrac{2}{3}\\pi r^3"), "शंकु का आयतन " + m("=\\dfrac{1}{3}\\pi r^2h")])
s2 += lines("\\text{अर्धगोले का आयतन}", "\\dfrac{2}{3}\\times\\dfrac{22}{7}\\times2\\times2\\times2", "\\dfrac{2}{3}\\times\\dfrac{22}{7}\\times8", "\\dfrac{2\\times22\\times8}{3\\times7}", "\\dfrac{352}{21}\\ \\text{cm}^3")
s2 += lines("\\text{शंकु का आयतन}", "\\dfrac{1}{3}\\times\\dfrac{22}{7}\\times2\\times2\\times2", "\\dfrac{1}{3}\\times\\dfrac{22}{7}\\times8", "\\dfrac{22\\times8}{3\\times7}", "\\dfrac{176}{21}\\ \\text{cm}^3")
s2 += lines("\\text{खिलौने का आयतन}", "\\dfrac{352}{21}+\\dfrac{176}{21}", "\\dfrac{528}{21}", "\\dfrac{176}{7}", "25.14\\ \\text{cm}^3")
assert F(2, 3) * F(22, 7) * 8 + F(1, 3) * F(22, 7) * 8 == F(176, 7)
s2 += ans(m("\\dfrac{176}{7}\\ \\text{cm}^3") + " ≈ 25.14 cm³")
s += orq("एक ठोस खिलौना एक अर्धगोले के आकार का है जिस पर एक लंब वृत्तीय शंकु अध्यारोपित है। इस शंकु की ऊँचाई 2 cm और आधार का व्यास 4 cm है। इस खिलौने का आयतन ज्ञात कीजिए।", s2)
QS.append((20, "3", "7 cm भुजा वाले एक घनाकार ब्लॉक के ऊपर एक अर्धगोला रखा हुआ है। अर्धगोले का अधिकतम व्यास क्या हो सकता है ? इस प्रकार बने ठोस का पृष्ठीय क्षेत्रफल ज्ञात कीजिए।", s))

# ================================================================== Q21  heights & distances
P21, B21 = (40, 275), (175, 275)
C21 = (175, 275 - 135)            # building top (45°)
D21 = (175, 275 - 135 * math.sqrt(3))  # tower top (60°)
f21 = svg(300, 300, [_ln((15, 275), (285, 275), "#6b7280", 2),
                     f"<rect x='175' y='{C21[1]}' width='42' height='135' fill='#eef4fd' stroke='#1d3a8a' stroke-width='2'/>",
                     _ln(C21, D21, "#1d3a8a", 4), _ln(P21, C21, "#c2410c", 1.8), _ln(P21, D21, "#0f7a4c", 1.8),
                     _rt(B21, P21, C21, 10), _arc(P21, B21, C21, 30, "45°", 46, "#c2410c", 12), _arc(P21, B21, D21, 62, None, None, "#0f7a4c") + _tx(P21[0] + 62 * math.cos(math.radians(-66)) - 8, P21[1] + 62 * math.sin(math.radians(-66)) - 4, "60°", 12, "#0f7a4c"),
                     _dot(P21), _dot(B21), _dot(C21), _dot(D21),
                     _tx(P21[0] - 4, P21[1] + 18, "P"), _tx(B21[0] - 2, B21[1] + 18, "B"), _tx(C21[0] - 12, C21[1] + 2, "C"), _tx(D21[0] - 11, D21[1] + 4, "D"),
                     _tx(228, 212, "20 m", 12.5, "#b4232a", False, "start"), _tx(185, (C21[1] + D21[1]) / 2 + 4, "h (मीनार)", 12.5, "#b4232a", False, "start"),
                     _tx(118, 293, "x", 13, "#b4232a")],
          "BC = भवन, CD = मीनार, P = भूमि पर बिंदु")
s = given("भवन BC = 20 m, मीनार CD = h<br>" + m("\\angle BPC=45^\\circ") + ", " + m("\\angle BPD=60^\\circ"), "मीनार की ऊँचाई h")
s += f21 + formula("प्रयुक्त", "", [m("\\tan\\theta=\\dfrac{\\text{लंब}}{\\text{आधार}}").replace("\\text{लंब}", "P").replace("\\text{आधार}", "B") + " (लंब / आधार)",
                           m("\\tan45^\\circ=1") + ", " + m("\\tan60^\\circ=\\sqrt{3}")])
s += p("माना PB = " + m("x") + " m। समकोण ΔPBC में,")
s += eqs(("\\tan45^\\circ", "\\dfrac{BC}{PB}"), ("1", "\\dfrac{20}{x}"), ("x", "20\\ \\text{m}"))
s += p("समकोण ΔPBD में, BD = BC + CD = 20 + h")
s += eqs(("\\tan60^\\circ", "\\dfrac{BD}{PB}"), ("\\sqrt{3}", "\\dfrac{20+h}{20}"))
s += p("वज्र-गुणन करने पर,")
s += eqs(("20\\sqrt{3}", "20+h"), ("h", "20\\sqrt{3}-20"))
s += lines("h", "20(\\sqrt{3}-1)", "20\\times(1.732-1)", "20\\times0.732", "14.64\\ \\text{m}")
close(math.tan(math.radians(60)) * 20 - 20, 20 * (math.sqrt(3) - 1))
s += ans("मीनार की ऊँचाई " + m("20(\\sqrt{3}-1)") + " m ≈ 14.64 m")
# OR: two poles
G = 205
Lb, Pt, Rb = (30, G), (90, G), (270, G)
hpx = 60 * math.sqrt(3)
La, Ra = (30, G - hpx), (270, G - hpx)
f21b = svg(310, 250, [_ln((10, G), (295, G), "#6b7280", 2), _ln(Lb, La, "#1d3a8a", 4), _ln(Rb, Ra, "#1d3a8a", 4),
                      _ln(Pt, La, "#c2410c", 1.8), _ln(Pt, Ra, "#0f7a4c", 1.8),
                      _rt(Lb, La, Pt, 9), _rt(Rb, Ra, Pt, 9),
                      _arc(Pt, Lb, La, 24, "60°", 38, "#c2410c", 12), _arc(Pt, Rb, Ra, 30, "30°", 47, "#0f7a4c", 12),
                      _dot(Lb), _dot(Pt), _dot(Rb), _dot(La), _dot(Ra),
                      _tx(Lb[0] - 4, G + 18, "B"), _tx(Pt[0], G + 18, "P"), _tx(Rb[0] + 4, G + 18, "D"), _tx(La[0] - 2, La[1] - 8, "A"), _tx(Ra[0] + 2, Ra[1] - 8, "C"),
                      _tx(22, (G + La[1]) / 2 + 4, "h", 14, "#b4232a", True, "end"), _tx(283, (G + Ra[1]) / 2 + 4, "h", 14, "#b4232a", True, "start"),
                      _tx(60, G + 18, "x", 13, "#b4232a"), _tx(180, G + 18, "80 − x", 12.5, "#b4232a", False),
                      _tx(150, G + 40, "सड़क की चौड़ाई BD = 80 m", 12.5, "#1d3a8a", False)],
           "खंभे AB और CD, सड़क पर बिंदु P")
s2 = given("AB = CD = h (खंभे), BD = 80 m<br>" + m("\\angle APB=60^\\circ") + ", " + m("\\angle CPD=30^\\circ"), "h, BP और PD")
s2 += f21b + formula("प्रयुक्त", "", [m("\\tan60^\\circ=\\sqrt{3}"), m("\\tan30^\\circ=\\dfrac{1}{\\sqrt{3}}")])
s2 += p("माना BP = " + m("x") + " m, तब PD = " + m("(80-x)") + " m")
s2 += p("समकोण ΔABP में,")
s2 += eqs(("\\tan60^\\circ", "\\dfrac{AB}{BP}"), ("\\sqrt{3}", "\\dfrac{h}{x}"), ("h", "\\sqrt{3}\\,x\\quad\\ldots(1)"))
s2 += p("समकोण ΔCDP में,")
s2 += eqs(("\\tan30^\\circ", "\\dfrac{CD}{PD}"), ("\\dfrac{1}{\\sqrt{3}}", "\\dfrac{h}{80-x}"))
s2 += p("वज्र-गुणन करने पर,")
s2 += eqs(("\\sqrt{3}\\,h", "80-x"))
s2 += p("(1) से " + m("h=\\sqrt{3}\\,x") + " रखने पर,")
s2 += eqs(("\\sqrt{3}\\times\\sqrt{3}\\,x", "80-x"), ("3x", "80-x"), ("3x+x", "80"), ("4x", "80"), ("x", "\\dfrac{80}{4}"), ("x", "20"))
s2 += lines("h", "\\sqrt{3}\\times20", "20\\sqrt{3}", "20\\times1.732", "34.64\\ \\text{m}")
s2 += lines("PD", "80-20", "60\\ \\text{m}")
close(20 * math.sqrt(3) / 20, math.tan(math.radians(60)))
close(20 * math.sqrt(3) / 60, math.tan(math.radians(30)))
s2 += ans("(i) खंभों की ऊँचाई = " + m("20\\sqrt{3}") + " m ≈ 34.64 m (ii) 60° वाले खंभे से बिंदु की दूरी = 20 m (iii) 30° वाले खंभे से बिंदु की दूरी = 60 m")
s += orq("एक 80 m चौड़ी सड़क के दोनों ओर आमने-सामने समान लंबाई वाले दो खंभे लगे हुए हैं। इन दोनों खंभों के बीच सड़क के एक बिंदु से खंभों के शिखर के उन्नयन कोण क्रमशः 60° और 30° हैं। खंभों की ऊँचाई और खंभों से बिंदु की दूरियाँ ज्ञात कीजिए।", s2)
QS.append((21, "4", "भूमि के एक बिंदु से एक 20 m ऊँचे भवन के शिखर पर लगी एक संचार मीनार के तल और शिखर के उन्नयन कोण क्रमशः 45° और 60° हैं। मीनार की ऊँचाई ज्ञात कीजिए।", s))

# ================================================================== Q22  linear equations
s = given("अंश और हर में 2 जोड़ने पर भिन्न " + m("\\dfrac{9}{11}") + "<br>अंश और हर में 3 जोड़ने पर भिन्न " + m("\\dfrac{5}{6}"), "भिन्न")
s += p("माना भिन्न " + m("\\dfrac{x}{y}") + " है।")
s += p("पहली शर्त से:")
s += eqs(("\\dfrac{x+2}{y+2}", "\\dfrac{9}{11}"))
s += p("वज्र-गुणन करने पर,")
s += eqs(("11(x+2)", "9(y+2)"), ("11x+22", "9y+18"), ("11x-9y", "18-22"), ("11x-9y", "-4\\quad\\ldots(1)"))
s += p("दूसरी शर्त से:")
s += eqs(("\\dfrac{x+3}{y+3}", "\\dfrac{5}{6}"))
s += p("वज्र-गुणन करने पर,")
s += eqs(("6(x+3)", "5(y+3)"), ("6x+18", "5y+15"), ("6x-5y", "15-18"), ("6x-5y", "-3\\quad\\ldots(2)"))
s += p("विलोपन विधि: समीकरण (1) को 5 से और (2) को 9 से गुणा करने पर,")
s += eqs(("5\\times(11x-9y)", "5\\times(-4)"), ("55x-45y", "-20\\quad\\ldots(3)"))
s += eqs(("9\\times(6x-5y)", "9\\times(-3)"), ("54x-45y", "-27\\quad\\ldots(4)"))
s += p("(3) में से (4) घटाने पर,")
s += eqs(("55x-54x-45y+45y", "-20-(-27)"), ("x", "-20+27"), ("x", "7"))
s += p(m("x=7") + " को (2) में रखने पर,")
s += eqs(("6\\times7-5y", "-3"), ("42-5y", "-3"), ("-5y", "-3-42"), ("-5y", "-45"), ("y", "\\dfrac{-45}{-5}"), ("y", "9"))
assert F(7 + 2, 9 + 2) == F(9, 11) and F(7 + 3, 9 + 3) == F(5, 6)
s += "<div class='vt'>जाँच:</div>" + lines("\\dfrac{7+2}{9+2}", "\\dfrac{9}{11}") + lines("\\dfrac{7+3}{9+3}", "\\dfrac{10}{12}", "\\dfrac{5}{6}") + ok("✔")
s += ans("अभीष्ट भिन्न " + m("\\dfrac{7}{9}") + " है।")
s2 = given("अंकों का योग 12<br>7 × संख्या = 4 × (अंक पलटने से बनी संख्या)", "दो अंकों की संख्या")
s2 += p("माना दहाई का अंक " + m("x") + " और इकाई का अंक " + m("y") + " है।")
s2 += lines("\\text{संख्या}", "10x+y") + lines("\\text{अंक पलटने पर संख्या}", "10y+x")
s2 += p("पहली शर्त से:") + eqs(("x+y", "12\\quad\\ldots(1)"))
s2 += p("दूसरी शर्त से:")
s2 += eqs(("7(10x+y)", "4(10y+x)"), ("70x+7y", "40y+4x"), ("70x-4x", "40y-7y"), ("66x", "33y"), ("y", "\\dfrac{66x}{33}"), ("y", "2x\\quad\\ldots(2)"))
s2 += p("(2) को (1) में रखने पर,")
s2 += eqs(("x+2x", "12"), ("3x", "12"), ("x", "\\dfrac{12}{3}"), ("x", "4"))
s2 += lines("y", "2\\times4", "8") + lines("\\text{संख्या}", "10\\times4+8", "40+8", "48")
assert 7 * 48 == 4 * 84 and 4 + 8 == 12
s2 += "<div class='vt'>जाँच:</div>" + lines("7\\times48", "336") + lines("4\\times84", "336") + ok("✔")
s2 += ans("अभीष्ट संख्या 48 है।")
s += orq("दो अंकों की संख्या के अंकों का योग 12 है। इस संख्या का सात गुना, संख्या के अंकों को पलटने से बनी संख्या का चार गुना है। वह संख्या ज्ञात कीजिए।", s2)
QS.append((22, "4", "यदि किसी भिन्न के अंश और हर दोनों में 2 जोड़ दिया जाए, तो वह 9/11 हो जाती है। यदि अंश और हर दोनों में 3 जोड़ दिया जाए, तो वह 5/6 हो जाती है। वह भिन्न ज्ञात कीजिए।", s))

# ================================================================== Q23  mean / median
cls = [(45, 55), (55, 65), (65, 75), (75, 85), (85, 95)]
fq = [3, 10, 11, 8, 3]
qtab = tbl(["साक्षरता दर (% में)"] + [f"{a}-{b}" for a, b in cls], [["नगरों की संख्या"] + fq])
rows, sfx, mids = [], 0, []
for (lo, hi), f in zip(cls, fq):
    xm = (lo + hi) // 2
    sfx += f * xm
    rows.append([f"{lo}-{hi}", f, xm, m(f"{f}\\times{xm}={f * xm}")])
    mids.append(lines(f"x_{len(mids) + 1}", f"\\dfrac{{{lo}+{hi}}}{{2}}", f"\\dfrac{{{lo + hi}}}{{2}}", str(xm)))
s = given("5 वर्ग अंतराल और उनकी बारंबारता (कुल 35 नगर)", "माध्य साक्षरता दर")
s += formula("माध्य (प्रत्यक्ष विधि)", m("\\bar{x}=\\dfrac{\\sum f_ix_i}{\\sum f_i}") + ", जहाँ " + m("x_i=\\dfrac{\\text{निम्न सीमा}+\\text{उच्च सीमा}}{2}").replace("\\text{निम्न सीमा}", "l_1").replace("\\text{उच्च सीमा}", "l_2") + " (वर्ग चिह्न)")
s += p("वर्ग चिह्न:") + "<div class='lads'>" + "".join(mids) + "</div>"
s += tbl(["साक्षरता दर (%)", m("f_i"), m("x_i"), m("f_ix_i")], rows, ["योग", m("\\sum f_i=35"), "", m("\\sum f_ix_i=" + str(sfx))])
s += lines("\\sum f_ix_i", "150+600+770+640+270", "2430")
s += lines("\\bar{x}", "\\dfrac{2430}{35}", "\\dfrac{486}{7}", "69.43")
assert sfx == 2430 and sum(fq) == 35 and F(2430, 35) == F(486, 7)
s += ans("माध्य साक्षरता दर ≈ 69.43%")
wc = [(40, 45), (45, 50), (50, 55), (55, 60), (60, 65), (65, 70), (70, 75)]
wf = [2, 3, 8, 6, 6, 3, 2]
cf, c = [], 0
for f in wf:
    c += f
    cf.append(c)
otab = tbl(["भार (किलोग्राम में)", "विद्यार्थियों की संख्या"], [[f"{a}-{b}", f] for (a, b), f in zip(wc, wf)])
cfrows = []
prev = 0
for (lo, hi), f, cc in zip(wc, wf, cf):
    cfrows.append([f"{lo}-{hi}", f, m(f"{prev}+{f}={cc}") if prev else str(cc)])
    prev = cc
s2 = given("7 वर्ग अंतराल, कुल 30 विद्यार्थी", "माध्यक भार")
s2 += formula("माध्यक", m("\\text{Median}=l+\\left(\\dfrac{\\frac{n}{2}-cf}{f}\\right)\\times h").replace("\\text{Median}", "M"),
              [m("l") + " = माध्यक वर्ग की निम्न सीमा", m("cf") + " = माध्यक वर्ग से पहले वाले वर्ग की संचयी बारंबारता",
               m("f") + " = माध्यक वर्ग की बारंबारता", m("h") + " = वर्ग माप"])
s2 += tbl(["भार (kg)", "बारंबारता " + m("f"), "संचयी बारंबारता " + m("cf")], cfrows, hl=3)
s2 += lines("n", "30") + lines("\\dfrac{n}{2}", "\\dfrac{30}{2}", "15")
s2 += p("संचयी बारंबारता 15 से ठीक बड़ी 19 है, जो वर्ग 55-60 की है। अतः माध्यक वर्ग = 55-60")
s2 += p(m("l=55,\\ cf=13,\\ f=6,\\ h=5"))
s2 += lines("M", "55+\\left(\\dfrac{15-13}{6}\\right)\\times5", "55+\\dfrac{2}{6}\\times5", "55+\\dfrac{10}{6}", "55+1.67", "56.67\\ \\text{kg}")
assert cf == [2, 5, 13, 19, 25, 28, 30]
close(55 + F(15 - 13, 6) * 5, 55 + 10 / 6)
s2 += ans("माध्यक भार ≈ 56.67 kg")
s = s + orq("नीचे दिया हुआ बंटन एक कक्षा के 30 विद्यार्थियों के भार को दर्शा रहा है। विद्यार्थियों का माध्यक भार ज्ञात कीजिए।" + otab, s2)
QS.append((23, "4", "निम्नलिखित सारणी 35 नगरों की साक्षरता दर (प्रतिशत में) दर्शाती है। माध्य साक्षरता दर ज्ञात कीजिए।" + qtab, s))

# ================================================================== page
SECTIONS = {1: ("खंड अ — वस्तुनिष्ठ प्रश्न", "प्रश्न 1 से 5 · प्रत्येक उपप्रश्न 1 अंक · 30 अंक"),
            6: ("खंड ब — 2 अंक वाले प्रश्न", "प्रश्न 6 से 17 · प्रत्येक 2 अंक · 24 अंक"),
            18: ("खंड स — 3 अंक वाले प्रश्न", "प्रश्न 18 से 20 · प्रत्येक 3 अंक · 9 अंक (आंतरिक विकल्प सहित)"),
            21: ("खंड द — 4 अंक वाले प्रश्न", "प्रश्न 21 से 23 · प्रत्येक 4 अंक · 12 अंक (आंतरिक विकल्प सहित)")}


def build():
    body = ""
    for num, mk, text, b in QS:
        if num in SECTIONS:
            h, sm = SECTIONS[num]
            body += f"<h2 class='sh'>{h}<small>{sm}</small></h2>"
        mlab = f"({mk})" if "×" in mk else f"[{mk} अंक]"
        badge = f" <span class='mk'>{mlab}</span>"
        t = text.replace("<div", badge + "<div", 1) if "<div" in text else qt(text) + badge
        body += q(num, t, b, (num - 1) % 6)
    jump = "".join(f"<a href='#q{n}'>प्र. {n}</a>" for n, *_ in QS)
    src = ("<div class='src'><b>प्रश्नपत्र स्रोत:</b> माध्यमिक शिक्षा मंडल, मध्यप्रदेश (mpbse.nic.in) का आधिकारिक नमूना प्रश्नपत्र 2026-27; हल educationdew.com द्वारा।"
           "<br>हाई स्कूल परीक्षा 2027 · विषय: गणित (स्टैंडर्ड) · कुल प्रश्न 23 · पूर्णांक 75 · समय 3 घंटे</div>")
    title = TITLE
    doc = f"""<!doctype html>
<html lang="hi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)} | MP Board हल</title>
<meta name="description" content="माध्यमिक शिक्षा मंडल मध्यप्रदेश (MPBSE) के कक्षा 10 गणित (स्टैंडर्ड) आधिकारिक मॉडल/नमूना प्रश्नपत्र 2026-27 (हाई स्कूल परीक्षा 2027) के सभी 23 प्रश्नों के चरणबद्ध हल, अथवा प्रश्नों सहित — हिंदी माध्यम।">
<meta name="keywords" content="MP Board, MPBSE, कक्षा 10, गणित स्टैंडर्ड, मॉडल प्रश्नपत्र 2026-27, नमूना प्रश्नपत्र, हल, हिंदी माध्यम">
<link rel="stylesheet" href="/assets/katex/katex.min.css"><style>{CSS_P}</style></head><body>
<header class="top"><a class="brand" href="/hi/">MP Board हल</a><a class="sw" href="/en/">English Medium</a></header>
<main><nav class="crumbs"><a href="/hi/">होम</a> › <a href="/hi/papers/">प्रश्नपत्र</a> › <span>कक्षा 10 गणित (स्टैंडर्ड) मॉडल प्रश्नपत्र 2026-27</span></nav>
<div class="hero"><h1>{e(title)}</h1><p>सभी 23 प्रश्न, हर उपप्रश्न और हर “अथवा” प्रश्न का चरणबद्ध हल — चित्र सहित, हिंदी माध्यम</p></div>
{src}
<div class="jump">{jump}</div>
{body}
<p class="boards" style="font-size:14px;color:#555;margin:18px 0">यह हल <b>MP Board (MPBSE)</b> कक्षा 10 गणित (स्टैंडर्ड) की हाई स्कूल परीक्षा 2027 की तैयारी के लिए है। प्रश्न NCERT पाठ्यपुस्तक पर आधारित हैं, इसलिए NCERT/CBSE के विद्यार्थियों के लिए भी उपयोगी।</p>
</main><footer>© educationdew.com · MP Board, NCERT और CBSE पाठ्यपुस्तकों के चरणबद्ध हल</footer></body></html>
"""
    out = ROOT / "site" / "hi" / "papers" / SLUG / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render_math(doc), encoding="utf-8")
    return out


if __name__ == "__main__":
    print(build())
