#!/usr/bin/env python3
"""Class 10 Maths, Chapter 11 (वृत्तों से संबंधित क्षेत्रफल): Exercise 11.1 (rationalised), Hindi medium.
Run from repo root: python3 tools/solutions/class10_ch11.py
"""
import sys, pathlib, math
from fractions import Fraction as F
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from common import *  # noqa
from mixed_cells import *  # noqa  (mc, lines, eqs for mixed Hindi/TeX cells)
from geometry import *  # noqa

BASE = "/hi/class-10/maths/chapter-11/"
CH = "वृत्तों से संबंधित क्षेत्रफल"


def close(a, b, t=1e-9):
    assert abs(float(a) - float(b)) < t, (a, b)


def secfig(theta, rlab, shade="sector", caption="", extra_lab=None):
    """circle with a shaded sector or segment of angle theta at centre O."""
    cx, cy, R = 170, 110, 80
    a1 = 90 - theta / 2; a2 = 90 + theta / 2
    A = (cx + R * math.cos(math.radians(a1)), cy - R * math.sin(math.radians(a1)))
    B = (cx + R * math.cos(math.radians(a2)), cy - R * math.sin(math.radians(a2)))
    large = 1 if theta > 180 else 0
    arc = f"A {R} {R} 0 {large} 0 {B[0]:.1f} {B[1]:.1f}"
    if shade == "sector":
        path = f"M {cx} {cy} L {A[0]:.1f} {A[1]:.1f} {arc} Z"
    else:
        path = f"M {A[0]:.1f} {A[1]:.1f} {arc} Z"
    ex = (f"<circle cx='{cx}' cy='{cy}' r='{R}' fill='none' stroke='#0f766e' stroke-width='2'/>"
          f"<path d='{path}' fill='#99f6e4' fill-opacity='.65' stroke='#0f766e' stroke-width='1.5'/>")
    pts = {"O": (cx, cy, 0, 18), "A": (round(A[0], 1), round(A[1], 1), 10, -2), "B": (round(B[0], 1), round(B[1], 1), -10, -2)}
    labs = [(cx, cy - 16, f"{theta}°"), ((cx + A[0]) / 2 + 12, (cy + A[1]) / 2 + 10, rlab)]
    if extra_lab:
        labs += extra_lab
    return fig(340, 210, pts, [("O", "A"), ("O", "B")], dashed=[("A", "B")] if shade == "segment" else [], labels=labs, extra=ex, caption=caption)


SEC = formula("सूत्र", "", [m("\\text{त्रिज्यखंड का क्षेत्रफल}=\\dfrac{\\theta}{360^\\circ}\\times\\pi r^2"),
                            m("\\text{चाप की लंबाई}=\\dfrac{\\theta}{360^\\circ}\\times2\\pi r"),
                            m("\\text{वृत्तखंड का क्षेत्रफल}=\\text{त्रिज्यखंड}-\\triangle OAB")])
EX = []
P7 = F(22, 7)
P3 = F(314, 100)

# Q1
a = F(60, 360) * P7 * 36
assert a == F(132, 7)
s = secfig(60, "6 cm", caption="त्रिज्यखंड OAB") + SEC + p("r = 6 cm, θ = 60°")
s += lines("\\text{क्षेत्रफल}", "\\dfrac{60}{360}\\times\\dfrac{22}{7}\\times6\\times6", "\\dfrac{1}{6}\\times\\dfrac{22}{7}\\times36", "\\dfrac{132}{7}", "18\\tfrac{6}{7}\\ \\text{cm}^2")
s += "<div class='vt'>जाँच:</div>" + p("पूरा वृत्त " + m("\\tfrac{22}{7}\\times36=\\tfrac{792}{7}") + "; उसका छठा भाग " + m("\\tfrac{132}{7}") + " ✔") + ans("त्रिज्यखंड का क्षेत्रफल 132/7 cm² (≈ 18.86 cm²)")
EX.append(("6 cm त्रिज्या वाले एक वृत्त के एक त्रिज्यखंड का क्षेत्रफल ज्ञात कीजिए, जिसका कोण 60° है।", s))

# Q2
r = F(22) / (2 * P7)
assert r == F(7, 2)
a = F(1, 4) * P7 * r * r
assert a == F(77, 8)
s = SEC + p("परिधि = 2πr = 22 cm:") + eqs(("2\\times\\dfrac{22}{7}\\times r", "22"), ("r", "\\dfrac{22\\times7}{44}"), ("r", "\\dfrac{7}{2}\\ \\text{cm}"))
s += p("चतुर्थांश = 90° का त्रिज्यखंड:") + lines("\\text{क्षेत्रफल}", "\\dfrac{90}{360}\\times\\dfrac{22}{7}\\times\\dfrac72\\times\\dfrac72", "\\dfrac14\\times\\dfrac{77}{2}", "\\dfrac{77}{8}\\ \\text{cm}^2")
s += "<div class='vt'>जाँच:</div>" + p(m("2\\times\\tfrac{22}{7}\\times\\tfrac72=22") + " ✔") + ans("चतुर्थांश का क्षेत्रफल 77/8 cm² = 9.625 cm²")
EX.append(("एक वृत्त के चतुर्थांश (quadrant) का क्षेत्रफल ज्ञात कीजिए, जिसकी परिधि 22 cm है।", s))

# Q3
a = F(30, 360) * P7 * 196
assert a == F(154, 3)
s = SEC + p("मिनट की सुई 60 मिनट में 360° घूमती है, इसलिए 5 मिनट में") + lines("\\theta", "\\dfrac{360^\\circ}{60}\\times5", "30^\\circ")
s += secfig(30, "14 cm", caption="5 मिनट में सुई द्वारा रचित त्रिज्यखंड")
s += lines("\\text{क्षेत्रफल}", "\\dfrac{30}{360}\\times\\dfrac{22}{7}\\times14\\times14", "\\dfrac{1}{12}\\times616", "\\dfrac{154}{3}", "51\\tfrac13\\ \\text{cm}^2")
s += "<div class='vt'>जाँच:</div>" + p("पूरे घंटे में " + m("\\tfrac{22}{7}\\times196=616") + "; 5 मिनट = 1/12 भाग = " + m("\\tfrac{616}{12}=\\tfrac{154}{3}") + " ✔") + ans("5 मिनट में रचित क्षेत्रफल 154/3 cm² (≈ 51.33 cm²)")
EX.append(("एक घड़ी की मिनट की सुई जिसकी लंबाई 14 cm है। इस सुई द्वारा 5 मिनट में रचित क्षेत्रफल ज्ञात कीजिए।", s))

# Q4
sec = F(90, 360) * P3 * 100; tri = F(1, 2) * 100
assert sec == F(785, 10) and sec - tri == F(285, 10) and P3 * 100 - sec == F(2355, 10)
s = secfig(90, "10 cm", "segment", caption="छायांकित: लघु वृत्तखंड") + SEC + p("r = 10 cm, θ = 90°, π = 3.14")
s += lines("\\text{लघु त्रिज्यखंड}", "\\dfrac{90}{360}\\times3.14\\times10\\times10", "78.5\\ \\text{cm}^2")
s += lines("\\triangle OAB", "\\dfrac12\\times OA\\times OB", "\\dfrac12\\times10\\times10", "50\\ \\text{cm}^2")
s += part("(i) लघु वृत्तखंड", lines("\\text{क्षेत्रफल}", "78.5-50", "28.5\\ \\text{cm}^2"))
s += part("(ii) दीर्घ त्रिज्यखंड", lines("\\text{क्षेत्रफल}", "\\pi r^2-\\text{लघु त्रिज्यखंड}", "314-78.5", "235.5\\ \\text{cm}^2"))
s += "<div class='vt'>जाँच:</div>" + p(m("78.5+235.5=314=3.14\\times100") + " ✔") + ans("(i) लघु वृत्तखंड 28.5 cm² (ii) दीर्घ त्रिज्यखंड 235.5 cm²")
EX.append(("10 cm त्रिज्या वाले एक वृत्त की कोई जीवा केंद्र पर एक समकोण अंतरित करती है। निम्नलिखित के क्षेत्रफल ज्ञात कीजिए: (i) संगत लघु वृत्तखंड (ii) संगत दीर्घ त्रिज्यखंड (π = 3.14 का प्रयोग कीजिए)", s))

# Q5
arc = F(60, 360) * 2 * P7 * 21; sec = F(60, 360) * P7 * 441
assert arc == 22 and sec == 231
s = secfig(60, "21 cm", "segment", caption="ΔOAB समबाहु (OA = OB, ∠O = 60°)") + SEC + p("r = 21 cm, θ = 60°")
s += part("(i) चाप की लंबाई", lines("l", "\\dfrac{60}{360}\\times2\\times\\dfrac{22}{7}\\times21", "\\dfrac16\\times132", "22\\ \\text{cm}"))
s += part("(ii) त्रिज्यखंड का क्षेत्रफल", lines("\\text{क्षेत्रफल}", "\\dfrac{60}{360}\\times\\dfrac{22}{7}\\times21\\times21", "\\dfrac16\\times1386", "231\\ \\text{cm}^2"))
s += part("(iii) वृत्तखंड का क्षेत्रफल", p("OA = OB और ∠AOB = 60°, इसलिए ∠OAB = ∠OBA = 60°, अर्थात् ΔOAB समबाहु है:") +
          lines("\\triangle OAB", "\\dfrac{\\sqrt3}{4}\\times21^2", "\\dfrac{441\\sqrt3}{4}\\ \\text{cm}^2") +
          lines("\\text{वृत्तखंड}", "\\left(231-\\dfrac{441\\sqrt3}{4}\\right)\\ \\text{cm}^2"))
s += "<div class='vt'>जाँच:</div>" + p("√3 ≈ 1.732 लेने पर " + m("231-190.96\\approx40.04") + " cm² (धनात्मक और त्रिज्यखंड से छोटा) ✔")
s += ans("(i) 22 cm (ii) 231 cm² (iii) (231 − 441√3/4) cm²")
EX.append(("21 cm त्रिज्या वाले एक वृत्त का एक चाप केंद्र पर 60° का कोण अंतरित करता है। ज्ञात कीजिए: (i) चाप की लंबाई (ii) चाप द्वारा बनाए गए त्रिज्यखंड का क्षेत्रफल (iii) संगत जीवा द्वारा बनाए गए वृत्तखंड का क्षेत्रफल", s))

# Q6
S3 = F(173, 100)
sec = F(60, 360) * P3 * 225; tri = S3 / 4 * 225
minor = sec - tri; major = P3 * 225 - minor
assert sec == F(11775, 100) and tri == F(973125, 10000) and minor == F(204375, 10000) and major == F(6860625, 10000)
s = secfig(60, "15 cm", "segment", caption="छायांकित: लघु वृत्तखंड") + SEC + p("r = 15 cm, θ = 60°, π = 3.14, √3 = 1.73")
s += lines("\\text{त्रिज्यखंड}", "\\dfrac{60}{360}\\times3.14\\times15\\times15", "\\dfrac{706.5}{6}", "117.75\\ \\text{cm}^2")
s += p("ΔOAB समबाहु है (OA = OB, ∠O = 60°):") + lines("\\triangle OAB", "\\dfrac{\\sqrt3}{4}\\times15^2", "\\dfrac{1.73\\times225}{4}", "97.3125\\ \\text{cm}^2")
s += part("(i) लघु वृत्तखंड", lines("\\text{क्षेत्रफल}", "117.75-97.3125", "20.4375\\ \\text{cm}^2"))
s += part("(ii) दीर्घ वृत्तखंड", lines("\\text{क्षेत्रफल}", "\\pi r^2-\\text{लघु वृत्तखंड}", "706.5-20.4375", "686.0625\\ \\text{cm}^2"))
s += "<div class='vt'>जाँच:</div>" + p(m("20.4375+686.0625=706.5=3.14\\times225") + " ✔") + ans("लघु वृत्तखंड 20.4375 cm², दीर्घ वृत्तखंड 686.0625 cm²")
EX.append(("15 cm त्रिज्या वाले एक वृत्त की कोई जीवा केंद्र पर 60° का कोण अंतरित करती है। जीवा द्वारा बनाए गए संगत लघु और दीर्घ वृत्तखंडों के क्षेत्रफल ज्ञात कीजिए। (π = 3.14 और √3 = 1.73 का प्रयोग कीजिए)", s))

# Q7
sec = F(120, 360) * P3 * 144; tri = 36 * S3
assert sec == F(15072, 100) and tri == F(6228, 100) and sec - tri == F(8844, 100)
close(0.5 * 144 * math.sin(math.radians(120)), 36 * math.sqrt(3))
s = secfig(120, "12 cm", "segment", caption="OM ⊥ AB") + SEC + p("r = 12 cm, θ = 120°, π = 3.14, √3 = 1.73")
s += lines("\\text{त्रिज्यखंड}", "\\dfrac{120}{360}\\times3.14\\times12\\times12", "\\dfrac{452.16}{3}", "150.72\\ \\text{cm}^2")
s += p("O से AB पर लंब OM डालिए। ∠AOM = 60°, इसलिए:") + eqs(("OM", "12\\cos60^\\circ=6\\ \\text{cm}"), ("AM", "12\\sin60^\\circ=6\\sqrt3\\ \\text{cm}"), ("AB", "2AM=12\\sqrt3\\ \\text{cm}"))
s += lines("\\triangle OAB", "\\dfrac12\\times AB\\times OM", "\\dfrac12\\times12\\sqrt3\\times6", "36\\sqrt3", "36\\times1.73", "62.28\\ \\text{cm}^2")
s += lines("\\text{वृत्तखंड}", "150.72-62.28", "88.44\\ \\text{cm}^2")
s += "<div class='vt'>जाँच:</div>" + p(m("\\tfrac12\\cdot12\\cdot12\\cdot\\sin120^\\circ=72\\cdot\\tfrac{\\sqrt3}{2}=36\\sqrt3") + " ✔") + ans("वृत्तखंड का क्षेत्रफल 88.44 cm²")
EX.append(("12 cm त्रिज्या वाले एक वृत्त की कोई जीवा केंद्र पर 120° का कोण अंतरित करती है। संगत वृत्तखंड का क्षेत्रफल ज्ञात कीजिए। (π = 3.14 और √3 = 1.73 का प्रयोग कीजिए)", s))

# Q8
a1 = F(1, 4) * P3 * 25; a2 = F(1, 4) * P3 * 100
assert a1 == F(19625, 1000) and a2 - a1 == F(58875, 1000)
ex = ("<rect x='60' y='30' width='160' height='160' fill='none' stroke='#1d3a8a' stroke-width='2'/>"
      "<path d='M 60 190 L 60 136.7 A 53.3 53.3 0 0 1 113.3 190 Z' fill='#bbf7d0' stroke='#15803d'/>"
      "<path d='M 60 136.7 L 60 83.3 A 106.7 106.7 0 0 1 166.7 190 L 113.3 190 A 53.3 53.3 0 0 0 60 136.7 Z' fill='#fde68a' fill-opacity='.7' stroke='#b45309'/>")
f = fig(340, 210, {"P": (60, 190, -10, 14)}, [], labels=[(90, 178, "5 m"), (150, 110, "10 m"), (140, 22, "15 m")], extra=ex,
        caption="हरा: 5 m रस्सी; पीला: रस्सी 10 m करने पर बढ़ा भाग")
s = f + SEC + p("खूँटा वर्ग के कोने पर है, इसलिए घोड़ा 90° के त्रिज्यखंड (चतुर्थांश) में चर सकता है। π = 3.14")
s += part("(i) रस्सी 5 m", lines("\\text{क्षेत्रफल}", "\\dfrac{90}{360}\\times3.14\\times5\\times5", "\\dfrac{78.5}{4}", "19.625\\ \\text{m}^2"))
s += part("(ii) रस्सी 10 m", lines("\\text{क्षेत्रफल}", "\\dfrac14\\times3.14\\times10\\times10", "78.5\\ \\text{m}^2") + lines("\\text{वृद्धि}", "78.5-19.625", "58.875\\ \\text{m}^2"))
s += "<div class='vt'>जाँच:</div>" + p("रस्सी दुगुनी तो क्षेत्रफल 4 गुना: " + m("4\\times19.625=78.5") + " ✔; दोनों रस्सियाँ 15 m भुजा से छोटी, इसलिए चतुर्थांश पूरा मैदान में ✔")
s += ans("(i) 19.625 m² (ii) चरने के क्षेत्रफल में वृद्धि 58.875 m²")
EX.append(("15 m भुजा वाले एक वर्गाकार घास के मैदान के एक कोने पर लगे खूँटे से एक घोड़े को 5 m लंबी रस्सी से बाँध दिया गया है। ज्ञात कीजिए: (i) मैदान के उस भाग का क्षेत्रफल जहाँ घोड़ा घास चर सकता है। (ii) चरे जा सकने वाले क्षेत्रफल में वृद्धि, यदि घोड़े को 5 m लंबी रस्सी के स्थान पर 10 m लंबी रस्सी से बाँध दिया जाए। (π = 3.14 का प्रयोग कीजिए)", s))

# Q9
circ = P7 * 35; tot = circ + 5 * 35; each = P7 * F(35, 2) ** 2 / 10
assert circ == 110 and tot == 285 and each == F(385, 4)
ln = "".join(f"<line x1='{170 + 80 * math.cos(math.radians(k * 36)):.1f}' y1='{110 - 80 * math.sin(math.radians(k * 36)):.1f}' x2='{170 - 80 * math.cos(math.radians(k * 36)):.1f}' y2='{110 + 80 * math.sin(math.radians(k * 36)):.1f}' stroke='#94a3b8' stroke-width='1.6'/>" for k in range(5))
f = fig(340, 210, {}, [], labels=[(170, 205, "व्यास 35 mm")], extra=ln + "<circle cx='170' cy='110' r='80' fill='none' stroke='#94a3b8' stroke-width='2.4'/>", caption="5 व्यास, 10 बराबर त्रिज्यखंड")
s = f + SEC + p("व्यास = 35 mm, r = 35/2 mm")
s += part("(i) तार की कुल लंबाई", lines("\\text{परिधि}", "\\pi d", "\\dfrac{22}{7}\\times35", "110\\ \\text{mm}") + lines("5\\ \\text{व्यास}", "5\\times35", "175\\ \\text{mm}") + lines("\\text{कुल}", "110+175", "285\\ \\text{mm}"))
s += part("(ii) प्रत्येक त्रिज्यखंड", p("10 बराबर त्रिज्यखंड, इसलिए प्रत्येक का कोण 36°:") +
          lines("\\text{क्षेत्रफल}", "\\dfrac{36}{360}\\times\\dfrac{22}{7}\\times\\dfrac{35}{2}\\times\\dfrac{35}{2}", "\\dfrac{1}{10}\\times\\dfrac{1925}{2}", "\\dfrac{385}{4}\\ \\text{mm}^2"))
s += "<div class='vt'>जाँच:</div>" + p(m("10\\times\\tfrac{385}{4}=962.5=\\tfrac{22}{7}\\times(17.5)^2") + " ✔") + ans("(i) 285 mm (ii) प्रत्येक त्रिज्यखंड 385/4 mm² = 96.25 mm²")
EX.append(("एक ब्रूच (brooch) को चाँदी के तार से बनाया जाता है, जो 35 mm व्यास वाले एक वृत्त के रूप में है। तार को वृत्त के 5 व्यासों को बनाने में भी प्रयुक्त किया गया है, जो उसे 10 बराबर त्रिज्यखंडों में विभाजित करता है। ज्ञात कीजिए: (i) कुल वांछित चाँदी के तार की लंबाई (ii) ब्रूच के प्रत्येक त्रिज्यखंड का क्षेत्रफल", s))

# Q10
a = F(45, 360) * P7 * 2025
assert a == F(22275, 28)
s = SEC + p("8 तानें बराबर दूरी पर हैं, इसलिए दो क्रमागत तानों के बीच का कोण") + lines("\\theta", "\\dfrac{360^\\circ}{8}", "45^\\circ")
s += secfig(45, "45 cm", caption="दो क्रमागत तानों के बीच का भाग")
s += lines("\\text{क्षेत्रफल}", "\\dfrac{45}{360}\\times\\dfrac{22}{7}\\times45\\times45", "\\dfrac18\\times\\dfrac{44550}{7}", "\\dfrac{22275}{28}\\ \\text{cm}^2")
s += "<div class='vt'>जाँच:</div>" + p(m("8\\times\\tfrac{22275}{28}=\\tfrac{44550}{7}=\\tfrac{22}{7}\\times2025") + " ✔") + ans("दो क्रमागत तानों के बीच का क्षेत्रफल 22275/28 cm² (≈ 795.54 cm²)")
EX.append(("एक छतरी में 8 ताने हैं, जो बराबर दूरी पर लगे हुए हैं। छतरी को 45 cm त्रिज्या वाला एक सपाट वृत्त मानते हुए, इसकी दो क्रमागत तानों के बीच का क्षेत्रफल ज्ञात कीजिए।", s))

# Q11
one = F(115, 360) * P7 * 625
assert 2 * one == F(158125, 126)
s = secfig(115, "25 cm", caption="एक वाइपर द्वारा साफ़ भाग") + SEC + p("r = 25 cm, θ = 115°। वाइपर एक-दूसरे पर नहीं चढ़ते, इसलिए कुल = 2 × एक त्रिज्यखंड।")
s += lines("\\text{एक वाइपर}", "\\dfrac{115}{360}\\times\\dfrac{22}{7}\\times25\\times25", "\\dfrac{23}{72}\\times\\dfrac{13750}{7}", "\\dfrac{158125}{252}\\ \\text{cm}^2")
s += lines("\\text{कुल}", "2\\times\\dfrac{158125}{252}", "\\dfrac{158125}{126}\\ \\text{cm}^2")
s += "<div class='vt'>जाँच:</div>" + p(m("\\tfrac{158125}{126}\\approx1254.96") + " cm², जो दो पूरे वृत्तों " + m("(2\\times1964.29)") + " के 115/360 भाग के बराबर है ✔")
s += ans("प्रत्येक बुहार में साफ़ क्षेत्रफल 158125/126 cm² (≈ 1254.96 cm²)")
EX.append(("किसी कार के दो वाइपर (wipers) हैं, जो परस्पर कभी आच्छादित नहीं होते हैं। प्रत्येक वाइपर की पत्ती की लंबाई 25 cm है और 115° के कोण तक घूम कर सफ़ाई कर सकता है। पत्तियों की प्रत्येक बुहार के साथ जितना क्षेत्रफल साफ़ हो जाता है, वह ज्ञात कीजिए।", s))

# Q12
a = F(80, 360) * P3 * F(165, 10) ** 2
close(a, 189.97, 0.001)
s = secfig(80, "16.5 km", caption="लाल प्रकाश से ढका समुद्री भाग") + SEC + p("r = 16.5 km, θ = 80°, π = 3.14")
s += lines("\\text{क्षेत्रफल}", "\\dfrac{80}{360}\\times3.14\\times16.5\\times16.5", "\\dfrac29\\times854.865", "189.97\\ \\text{km}^2")
s += "<div class='vt'>जाँच:</div>" + p(m("854.865\\times2=1709.73,\\ 1709.73\\div9=189.97") + " ✔") + ans("समुद्र का 189.97 km² (लगभग) क्षेत्रफल चेतावनी के अंतर्गत है।")
EX.append(("समुद्री जहाजों को पानी के नीचे स्थित चट्टानों की चेतावनी देने के लिए, एक लाइट हाउस (light house) 80° कोण वाले एक त्रिज्यखंड में 16.5 km की दूरी तक लाल रंग का प्रकाश फैलाता है। समुद्र के उस भाग का क्षेत्रफल ज्ञात कीजिए जिसमें जहाजों को चेतावनी दी जा सके। (π = 3.14 का प्रयोग कीजिए)", s))

# Q13
S17 = F(17, 10)
sec = F(60, 360) * P7 * 784; tri = S17 / 4 * 784; seg = sec - tri
assert 6 * seg == F(4648, 10) and 6 * seg * F(35, 100) == F(16268, 100)
hexs = [(170 + 80 * math.cos(math.radians(90 + 60 * k)), 110 - 80 * math.sin(math.radians(90 + 60 * k))) for k in range(6)]
ex = "<circle cx='170' cy='110' r='80' fill='#99f6e4' fill-opacity='.65' stroke='#0f766e' stroke-width='2'/>"
ex += "<polygon points='" + " ".join(f"{x:.1f},{y:.1f}" for x, y in hexs) + "' fill='#fff' stroke='#1d3a8a' stroke-width='1.8'/>"
f = fig(340, 210, {"O": (170, 110, 0, 18)}, [], labels=[(214, 104, "28 cm")], extra=ex + "<line x1='170' y1='110' x2='239.3' y2='70' stroke='#1d3a8a' stroke-width='1.4'/>",
        caption="छायांकित: 6 बराबर डिज़ाइन (वृत्तखंड)")
s = f + SEC + p("6 बराबर डिज़ाइन, प्रत्येक वृत्तखंड का केंद्रीय कोण 360°/6 = 60°, r = 28 cm, √3 = 1.7")
s += lines("\\text{एक त्रिज्यखंड}", "\\dfrac{60}{360}\\times\\dfrac{22}{7}\\times28\\times28", "\\dfrac{1232}{3}\\ \\text{cm}^2")
s += p("ΔOAB समबाहु है:") + lines("\\triangle OAB", "\\dfrac{\\sqrt3}{4}\\times28^2", "1.7\\times196", "333.2\\ \\text{cm}^2")
s += lines("\\text{एक डिज़ाइन}", "\\dfrac{1232}{3}-333.2", "\\dfrac{1232-999.6}{3}", "\\dfrac{232.4}{3}\\ \\text{cm}^2")
s += lines("\\text{6 डिज़ाइन}", "6\\times\\dfrac{232.4}{3}", "464.8\\ \\text{cm}^2")
s += lines("\\text{लागत}", "464.8\\times0.35", "162.68\\ \\text{रुपये}")
s += "<div class='vt'>जाँच:</div>" + p("वृत्त " + m("\\approx2464") + " − षट्भुज " + m("(6\\times333.2=1999.2)") + " = 464.8 cm² ✔") + ans("डिज़ाइन बनाने की लागत ₹162.68")
EX.append(("एक गोल मेज़पोश पर छः समान डिज़ाइन बने हुए हैं। यदि मेज़पोश की त्रिज्या 28 cm है, तो ₹0.35 प्रति वर्ग सेंटीमीटर की दर से इन डिज़ाइनों को बनाने की लागत ज्ञात कीजिए। (√3 = 1.7 का प्रयोग कीजिए)", s))

# Q14
s = SEC + lines("\\text{क्षेत्रफल}", "\\dfrac{p}{360}\\times\\pi R^2", "\\dfrac{p}{720}\\times2\\pi R^2")
s += p("(A), (C) में 2πR (परिधि) है जो लंबाई देता है, क्षेत्रफल नहीं; (B) में 180 है जो दुगुना मान देगा।")
s += "<div class='vt'>जाँच (p = 360° पर):</div>" + p(m("\\dfrac{360}{720}\\times2\\pi R^2=\\pi R^2") + " (पूरा वृत्त) ✔") + ans("(D) p/720 × 2πR²")
EX.append(("सही उत्तर चुनिए: R त्रिज्या वाले उस त्रिज्यखंड का क्षेत्रफल जिसका कोण p° है, निम्नलिखित है: (A) p/180 × 2πR (B) p/180 × πR² (C) p/360 × 2πR (D) p/720 × 2πR²", s))

EX = [(qt(t_), b_) for t_, b_ in EX]
page(BASE, 11, CH, "exercise-11-1", "प्रश्नावली 11.1", "कक्षा 10 गणित · अध्याय 11: वृत्तों से संबंधित क्षेत्रफल · 14 प्रश्न (त्रिज्यखंड और वृत्तखंड)", EX,
     (BASE, "अध्याय 11"), ("/hi/class-10/maths/", "सभी अध्याय"))
print("ok")
