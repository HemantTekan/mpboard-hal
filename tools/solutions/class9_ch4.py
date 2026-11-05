#!/usr/bin/env python3
"""Class 9 Maths, Chapter 4 (दो चरों वाले रैखिक समीकरण): Exercises 4.1 and 4.2, Hindi medium.
Rationalised book keeps exercises 4.1 and 4.2 (the old 4.3 graphs and 4.4 were removed).
Question text checked against the NCERT Hindi PDF ihmh104 (archive.org copy, 2021-22 print).
User rules: every smallest step shown (class 9 level); transposition step by step; maths in LaTeX.
Run from repo root: python3 tools/solutions/class9_ch4.py
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from common import *  # noqa
from mixed_cells import *  # noqa

BASE = "/hi/class-09/maths/chapter-04/"
CH = "दो चरों वाले रैखिक समीकरण"
BOARDS9 = ("यह हल <b>MP Board (MPBSE)</b> कक्षा 9 गणित की पाठ्यपुस्तक के अध्याय 4 ‘दो चरों वाले रैखिक समीकरण’ के अनुसार है।")
EXTRA_CSS = """
.tw{overflow-x:auto;-webkit-overflow-scrolling:touch;max-width:100%;margin:8px 0 10px}
.st{border-collapse:collapse;font-variant-numeric:tabular-nums;background:#fff;font-size:15px}
.st th,.st td{border:1px solid #d5dbe8;padding:4px 8px;text-align:center}
.st th{background:var(--l);font-weight:700}
.tp{background:#fff4ec;border-left:4px solid #e8711a;border-radius:8px;padding:5px 10px;margin:6px 0;font-size:.95em}
.why{font-size:.95em;color:#36405a;margin:2px 0 6px}
.ans .al{margin:10px 0}
"""


def tp(t):
    return f"<div class='tp'>{t}</div>"


def why(t):
    return f"<p class='why'>{t}</p>"


def table(head, rows):
    h = "".join(f"<th>{x}</th>" for x in head)
    b = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f"<div class='tw'><table class='st'><tr>{h}</tr>{b}</table></div>"


STD = formula("मानक रूप", "दो चरों वाले रैखिक समीकरण का मानक रूप " + m("ax + by + c = 0") + " है, जहाँ " + m("a, b, c") + " वास्तविक संख्याएँ हैं और "
              + m("a") + " तथा " + m("b") + " दोनों शून्य नहीं हैं। " + m("a") + " = " + m("x") + " का गुणांक, " + m("b") + " = " + m("y") + " का गुणांक, " + m("c") + " = अचर पद।")

# =====================================================================
# Exercise 4.1
# =====================================================================
E1 = []
s = p("मान लीजिए एक नोटबुक की कीमत " + m("x") + " रु है और एक कलम की कीमत " + m("y") + " रु है।")
s += p("कथन: नोटबुक की कीमत = 2 × कलम की कीमत")
s += eqs(("x", "2 \\times y"))
s += lines("x", "2y")
s += p("सभी पदों को बाएँ पक्ष में लाने के लिए दोनों पक्षों में से " + m("2y") + " घटाते हैं:")
s += lines("x - 2y", "2y - 2y", "0")
s += STD
s += p(m("x - 2y = 0") + " को मानक रूप में लिखने पर:")
s += eqs(("1 \\cdot x + (-2) \\cdot y + 0", "0"))
s += tp("जाँच: मान लीजिए कलम की कीमत " + m("y = 10") + " रु है, तो नोटबुक की कीमत " + m("x = 2 \\times 10 = 20") + " रु होगी।")
s += lines("x - 2y", "20 - 2 \\times 10", "20 - 20", "0")
s += ok("बायाँ पक्ष = 0 = दायाँ पक्ष, अतः समीकरण सही है।")
s += ans(m("x - 2y = 0") + " (जहाँ " + m("x") + " = नोटबुक की कीमत रु में, " + m("y") + " = कलम की कीमत रु में)")
E1.append(("एक नोटबुक की कीमत एक कलम की कीमत से दो गुनी है। इस कथन को निरूपित करने के लिए दो चरों वाला एक रैखिक समीकरण लिखिए। "
           "(संकेत: मान लीजिए, नोटबुक की कीमत " + m("x") + " रु है और कलम की कीमत " + m("y") + " रु है।)", s))


def abc(a, b, c):
    return table([m("a"), m("b"), m("c")], [[m(a), m(b), m(c)]])


s = STD
# (i)
s += part("(i) " + m("2x + 3y = 9.35"),
          p("दाएँ पक्ष का " + m("9.35") + " बाएँ पक्ष में लाने के लिए दोनों पक्षों में से " + m("9.35") + " घटाते हैं:")
          + lines("2x + 3y - 9.35", "9.35 - 9.35", "0")
          + p(m("ax + by + c = 0") + " से मिलान करने पर:")
          + eqs(("2x + 3y + (-9.35)", "0"))
          + abc("2", "3", "-9.35")
          + ans(m("2x + 3y - 9.35 = 0") + "; " + m("a = 2,\\ b = 3,\\ c = -9.35")))
# (ii)
s += part("(ii) " + m("x - \\dfrac{y}{5} - 10 = 0"),
          p("समीकरण पहले से ही " + m("(\\ldots) = 0") + " रूप में है। हर पद को " + m("+") + " चिह्न के साथ लिखते हैं:")
          + eqs(("x - \\dfrac{y}{5} - 10", "0"))
          + p(m("\\dfrac{y}{5} = \\dfrac{1}{5} \\times y") + ", इसलिए " + m("-\\dfrac{y}{5} = \\left(-\\dfrac{1}{5}\\right) y") + ":")
          + eqs(("1 \\cdot x + \\left(-\\dfrac{1}{5}\\right) y + (-10)", "0"))
          + abc("1", "-\\dfrac{1}{5}", "-10")
          + ans(m("x - \\dfrac{1}{5}y - 10 = 0") + "; " + m("a = 1,\\ b = -\\dfrac{1}{5},\\ c = -10")))
# (iii)
s += part("(iii) " + m("-2x + 3y = 6"),
          p("दोनों पक्षों में से " + m("6") + " घटाते हैं:")
          + lines("-2x + 3y - 6", "6 - 6", "0")
          + eqs(("(-2) x + 3y + (-6)", "0"))
          + abc("-2", "3", "-6")
          + ans(m("-2x + 3y - 6 = 0") + "; " + m("a = -2,\\ b = 3,\\ c = -6")))
# (iv)
s += part("(iv) " + m("x = 3y"),
          p("दोनों पक्षों में से " + m("3y") + " घटाते हैं:")
          + lines("x - 3y", "3y - 3y", "0")
          + p("इसमें कोई अचर पद नहीं है, इसलिए अचर पद " + m("0") + " लिखते हैं:")
          + eqs(("1 \\cdot x + (-3) y + 0", "0"))
          + abc("1", "-3", "0")
          + ans(m("x - 3y + 0 = 0") + "; " + m("a = 1,\\ b = -3,\\ c = 0")))
# (v)
s += part("(v) " + m("2x = -5y"),
          p("दोनों पक्षों में " + m("5y") + " जोड़ते हैं:")
          + lines("2x + 5y", "-5y + 5y", "0")
          + eqs(("2x + 5y + 0", "0"))
          + abc("2", "5", "0")
          + ans(m("2x + 5y + 0 = 0") + "; " + m("a = 2,\\ b = 5,\\ c = 0")))
# (vi)
s += part("(vi) " + m("3x + 2 = 0"),
          p("इसमें " + m("y") + " वाला पद नहीं है, इसलिए " + m("y") + " का गुणांक " + m("0") + " है (" + m("0 \\cdot y = 0") + "):")
          + eqs(("3x + 0 \\cdot y + 2", "0"))
          + abc("3", "0", "2")
          + ans(m("3x + 0 \\cdot y + 2 = 0") + "; " + m("a = 3,\\ b = 0,\\ c = 2")))
# (vii)
s += part("(vii) " + m("y - 2 = 0"),
          p("इसमें " + m("x") + " वाला पद नहीं है, इसलिए " + m("x") + " का गुणांक " + m("0") + " है। " + m("y = 1 \\cdot y") + ":")
          + eqs(("0 \\cdot x + 1 \\cdot y + (-2)", "0"))
          + abc("0", "1", "-2")
          + ans(m("0 \\cdot x + 1 \\cdot y - 2 = 0") + "; " + m("a = 0,\\ b = 1,\\ c = -2")))
# (viii)
s += part("(viii) " + m("5 = 2x"),
          p("दोनों पक्षों में से " + m("2x") + " घटाते हैं:")
          + lines("5 - 2x", "2x - 2x", "0")
          + p(m("x") + " वाला पद पहले लिखते हैं और " + m("y") + " का गुणांक " + m("0") + " लेते हैं:")
          + eqs(("-2x + 0 \\cdot y + 5", "0"))
          + abc("-2", "0", "5")
          + ans(m("-2x + 0 \\cdot y + 5 = 0") + "; " + m("a = -2,\\ b = 0,\\ c = 5")))
s += table(["समीकरण", "मानक रूप", m("a"), m("b"), m("c")],
           [["(i)", m("2x + 3y - 9.35 = 0"), m("2"), m("3"), m("-9.35")],
            ["(ii)", m("x - \\frac{1}{5}y - 10 = 0"), m("1"), m("-\\frac{1}{5}"), m("-10")],
            ["(iii)", m("-2x + 3y - 6 = 0"), m("-2"), m("3"), m("-6")],
            ["(iv)", m("x - 3y + 0 = 0"), m("1"), m("-3"), m("0")],
            ["(v)", m("2x + 5y + 0 = 0"), m("2"), m("5"), m("0")],
            ["(vi)", m("3x + 0 \\cdot y + 2 = 0"), m("3"), m("0"), m("2")],
            ["(vii)", m("0 \\cdot x + y - 2 = 0"), m("0"), m("1"), m("-2")],
            ["(viii)", m("-2x + 0 \\cdot y + 5 = 0"), m("-2"), m("0"), m("5")]])
E1.append((qt("निम्नलिखित रैखिक समीकरणों को " + m("ax + by + c = 0") + " के रूप में व्यक्त कीजिए और प्रत्येक स्थिति में " + m("a, b") + " और " + m("c")
              + " के मान बताइए: (i) " + m("2x + 3y = 9.35") + " (ii) " + m("x - \\dfrac{y}{5} - 10 = 0") + " (iii) " + m("-2x + 3y = 6")
              + " (iv) " + m("x = 3y") + " (v) " + m("2x = -5y") + " (vi) " + m("3x + 2 = 0") + " (vii) " + m("y - 2 = 0") + " (viii) " + m("5 = 2x")), s))

# =====================================================================
# Exercise 4.2
# =====================================================================
E2 = []
s = p("समीकरण " + m("y = 3x + 5") + " में " + m("x") + " का कोई भी मान रखने पर " + m("y") + " का एक मान मिलता है। कुछ मान रखकर देखते हैं:")
for xv in (0, 1, 2, -1):
    xs = f"({xv})" if xv < 0 else str(xv)
    yv = 3 * xv + 5
    s += lines("y", f"3 \\times {xs} + 5", f"{3 * xv} + 5", str(yv))
    s += tp(m(f"x = {xv}") + " पर " + m(f"y = {yv}") + ", अतः " + m(f"({xv}, {yv})") + " एक हल है।")
s += p(m("x") + " के मान अपरिमित (अनगिनत) हैं और हर मान के लिए " + m("y") + " का एक मान मिलता है। इसलिए इस समीकरण के हल भी अपरिमित रूप से अनेक हैं।")
s += why("दो चरों वाले हर रैखिक समीकरण के अपरिमित रूप से अनेक हल होते हैं, इसलिए (i) अद्वितीय हल और (ii) केवल दो हल गलत हैं।")
s += ans("विकल्प (iii) सत्य है: " + m("y = 3x + 5") + " के अपरिमित रूप से अनेक हल हैं।")
E2.append(("निम्नलिखित विकल्पों में कौन-सा विकल्प सत्य है, और क्यों? " + m("y = 3x + 5") + " का "
           "<span style='display:block;margin-top:4px'>(i) एक अद्वितीय हल है</span><span style='display:block'>(ii) केवल दो हल हैं</span>"
           "<span style='display:block'>(iii) अपरिमित रूप से अनेक हल हैं</span>", s))

# Q2
s = tp("विधि: एक चर को दूसरे चर के रूप में लिखें, फिर एक चर के अलग-अलग मान रखकर दूसरे चर का मान निकालें।")
# (i)
b = p("दोनों पक्षों में से " + m("2x") + " घटाकर " + m("y") + " अलग करते हैं:")
b += lines("2x + y - 2x", "7 - 2x")
b += lines("y", "7 - 2x")
rows = []
for xv in (0, 1, 2, 3):
    yv = 7 - 2 * xv
    b += lines(f"x = {xv}:\\quad y", f"7 - 2 \\times {xv}", f"7 - {2 * xv}", str(yv))
    rows.append([m(str(xv)), m(str(yv)), m(f"({xv}, {yv})")])
b += table([m("x"), m("y"), "हल"], rows)
b += tp("जाँच " + m("(3, 1)") + " के लिए: " + m("2 \\times 3 + 1 = 6 + 1 = 7") + " ✓")
b += ans(m("(0, 7),\\ (1, 5),\\ (2, 3),\\ (3, 1)"))
s += part("(i) " + m("2x + y = 7"), b)
# (ii)
b = p("दोनों पक्षों में से " + m("\\pi x") + " घटाकर " + m("y") + " अलग करते हैं:")
b += lines("\\pi x + y - \\pi x", "9 - \\pi x")
b += lines("y", "9 - \\pi x")
b += lines("x = 0:\\quad y", "9 - \\pi \\times 0", "9 - 0", "9")
b += lines("x = 1:\\quad y", "9 - \\pi \\times 1", "9 - \\pi")
b += lines("x = 2:\\quad y", "9 - \\pi \\times 2", "9 - 2\\pi")
b += lines("x = -1:\\quad y", "9 - \\pi \\times (-1)", "9 + \\pi")
b += table([m("x"), m("y"), "हल"], [[m("0"), m("9"), m("(0, 9)")], [m("1"), m("9 - \\pi"), m("(1, 9 - \\pi)")],
                                    [m("2"), m("9 - 2\\pi"), m("(2, 9 - 2\\pi)")], [m("-1"), m("9 + \\pi"), m("(-1, 9 + \\pi)")]])
b += tp("जाँच " + m("(2, 9 - 2\\pi)") + " के लिए: " + m("\\pi \\times 2 + (9 - 2\\pi) = 2\\pi + 9 - 2\\pi = 9") + " ✓")
b += ans(m("(0, 9),\\ (1, 9 - \\pi),\\ (2, 9 - 2\\pi),\\ (-1, 9 + \\pi)"))
s += part("(ii) " + m("\\pi x + y = 9"), b)
# (iii)
b = p("यहाँ " + m("x") + " पहले से " + m("y") + " के रूप में लिखा है: " + m("x = 4y") + "। " + m("y") + " के मान रखते हैं:")
rows = []
for yv in (0, 1, 2, -1):
    ys = f"({yv})" if yv < 0 else str(yv)
    b += lines(f"y = {yv}:\\quad x", f"4 \\times {ys}", str(4 * yv))
    rows.append([m(str(yv)), m(str(4 * yv)), m(f"({4 * yv}, {yv})")])
b += table([m("y"), m("x"), "हल " + m("(x, y)")], rows)
b += why("ध्यान दें: हल हमेशा " + m("(x, y)") + " क्रम में लिखते हैं, पहले " + m("x") + " फिर " + m("y") + "।")
b += ans(m("(0, 0),\\ (4, 1),\\ (8, 2),\\ (-4, -1)"))
s += part("(iii) " + m("x = 4y"), b)
E2.append((qt("निम्नलिखित समीकरणों में से प्रत्येक समीकरण के चार हल लिखिए: (i) " + m("2x + y = 7") + " (ii) " + m("\\pi x + y = 9") + " (iii) " + m("x = 4y")), s))

# Q3
s = formula("हल की जाँच", m("(x, y)") + " को समीकरण में रखें। यदि बायाँ पक्ष = दायाँ पक्ष, तो वह हल है; नहीं तो हल नहीं है।")
s += p("समीकरण: " + m("x - 2y = 4") + " (दायाँ पक्ष = 4)")


def chk(lab, pt, stepsl, val, yes):
    b = p(m(pt) + " में " + m("x") + " और " + m("y") + " के मान रखने पर बायाँ पक्ष:")
    b += lines("x - 2y", *stepsl)
    if yes:
        b += ok("बायाँ पक्ष " + m(f"= {val} =") + " दायाँ पक्ष")
        b += ans(m(pt) + " हल है।")
    else:
        b += p("बायाँ पक्ष " + m(f"= {val} \\neq 4") + " = दायाँ पक्ष")
        b += ans(m(pt) + " हल नहीं है।")
    return part(lab + " " + m(pt), b)


s += chk("(i)", "(0, 2)", ["0 - 2 \\times 2", "0 - 4", "-4"], "-4", False)
s += chk("(ii)", "(2, 0)", ["2 - 2 \\times 0", "2 - 0", "2"], "2", False)
s += chk("(iii)", "(4, 0)", ["4 - 2 \\times 0", "4 - 0", "4"], "4", True)
s += chk("(iv)", "(\\sqrt{2}, 4\\sqrt{2})", ["\\sqrt{2} - 2 \\times 4\\sqrt{2}", "\\sqrt{2} - 8\\sqrt{2}", "(1 - 8)\\sqrt{2}", "-7\\sqrt{2}"], "-7\\sqrt{2}", False)
s += chk("(v)", "(1, 1)", ["1 - 2 \\times 1", "1 - 2", "-1"], "-1", False)
s += table(["बिंदु", m("x - 2y"), "हल?"], [[m("(0, 2)"), m("-4"), "नहीं"], [m("(2, 0)"), m("2"), "नहीं"], [m("(4, 0)"), m("4"), "हाँ"],
                                         [m("(\\sqrt{2}, 4\\sqrt{2})"), m("-7\\sqrt{2}"), "नहीं"], [m("(1, 1)"), m("-1"), "नहीं"]])
s += ans("केवल " + m("(4, 0)") + " हल है। " + m("(0, 2),\\ (2, 0),\\ (\\sqrt{2}, 4\\sqrt{2})") + " और " + m("(1, 1)") + " हल नहीं हैं।")
E2.append((qt("बताइए कि निम्नलिखित हलों में कौन-कौन समीकरण " + m("x - 2y = 4") + " के हल हैं और कौन-कौन हल नहीं हैं: (i) " + m("(0, 2)") + " (ii) " + m("(2, 0)")
              + " (iii) " + m("(4, 0)") + " (iv) " + m("(\\sqrt{2}, 4\\sqrt{2})") + " (v) " + m("(1, 1)")), s))

# Q4
s = p(m("x = 2,\\ y = 1") + " समीकरण का हल है, इसलिए इन्हें रखने पर समीकरण संतुष्ट होगा।")
s += lines("2x + 3y", "k")
s += lines("2 \\times 2 + 3 \\times 1", "k")
s += lines("4 + 3", "k")
s += lines("7", "k")
s += p("पक्ष बदलकर लिखने पर:")
s += eqs(("k", "7"))
s += tp("जाँच: " + m("2 \\times 2 + 3 \\times 1 = 4 + 3 = 7 = k") + " ✓")
s += ans(m("k = 7"))
E2.append((m("k") + " का मान ज्ञात कीजिए जबकि " + m("x = 2,\\ y = 1") + " समीकरण " + m("2x + 3y = k") + " का एक हल हो।", s))

import re as _re
ALL = [("exercise-4-1", "प्रश्नावली 4.1", "रैखिक समीकरण का मानक रूप", E1), ("exercise-4-2", "प्रश्नावली 4.2", "रैखिक समीकरण के हल", E2)]
for _, _, _, E in ALL:
    for _q, _sol in E:
        for _t in _re.findall(r"\\\((.+?)\\\)", _q + _sol):
            assert not _re.search(r"[\u0900-\u097F]", _t), ("Devanagari in TeX", _t)
for i, (slug, title, topic, E) in enumerate(ALL):
    prev = (BASE + ALL[i - 1][0] + "/", ALL[i - 1][1]) if i else ("/hi/class-09/maths/chapter-03/exercise-3-2/", "प्रश्नावली 3.2")
    nxt = (BASE + ALL[i + 1][0] + "/", ALL[i + 1][1]) if i + 1 < len(ALL) else (BASE, "अध्याय 4")
    page(BASE, 4, CH, slug, title, f"कक्षा 9 गणित · अध्याय 4: {CH} · {len(E)} प्रश्न ({topic})", E,
         prev, nxt, css=CSS + EXTRA_CSS, boards=BOARDS9)
print("ok")
