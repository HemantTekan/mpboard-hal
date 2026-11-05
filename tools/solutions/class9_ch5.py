#!/usr/bin/env python3
"""Class 9 Maths, Chapter 5 (यूक्लिड की ज्यामिति का परिचय): Exercise 5.1, Hindi medium.
Rationalised book keeps only exercise 5.1 (old 5.2 removed).
Question text checked against the NCERT Hindi PDF ihmh105 (archive.org copy, 2021-22 print).
User rules: every smallest step shown; figures exact (right-angle marks, labels off lines); maths in LaTeX.
Run from repo root: python3 tools/solutions/class9_ch5.py
"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from common import *  # noqa
from mixed_cells import *  # noqa

BASE = "/hi/class-09/maths/chapter-05/"
CH = "यूक्लिड की ज्यामिति का परिचय"
BOARDS9 = ("यह हल <b>MP Board (MPBSE)</b> कक्षा 9 गणित की पाठ्यपुस्तक के अध्याय 5 ‘यूक्लिड की ज्यामिति का परिचय’ के अनुसार है।")
EXTRA_CSS = """
.tw{overflow-x:auto;-webkit-overflow-scrolling:touch;max-width:100%;margin:8px 0 10px}
.st{border-collapse:collapse;background:#fff;font-size:15px}
.st th,.st td{border:1px solid #d5dbe8;padding:5px 8px;text-align:left;vertical-align:top}
.st th{background:var(--l);font-weight:700}
.fig{margin:10px 0;text-align:center}.fig svg{width:100%;height:auto;background:#fbfcff;border:1px solid #e3e8f4;border-radius:12px}
.fig .cap{font-size:.85em;color:#5a6275;margin-top:4px}
.tp{background:#fff4ec;border-left:4px solid #e8711a;border-radius:8px;padding:5px 10px;margin:6px 0;font-size:.95em}
.why{font-size:.95em;color:#36405a;margin:2px 0 6px}
.tf{display:inline-block;font-weight:700;border-radius:6px;padding:0 7px;margin-right:4px}
.tf.y{background:#e3f6ea;color:#0f7a3c}.tf.n{background:#fde8e8;color:#b4232a}
.pf{counter-reset:s}.pf .ps{display:flex;gap:8px;margin:5px 0;align-items:baseline}
.pf .ps .n{flex:0 0 auto;font-weight:700;color:#1d3a8a}.pf .ps .r{color:#5a6275;font-size:.92em}
.ans .al{margin:10px 0}
"""
INK, RED, GRN, ORG, BLU = "#1d3a8a", "#b4232a", "#0f7a4c", "#c2410c", "#1769c2"
FONT = "font-family='Noto Sans, Noto Sans Devanagari, sans-serif'"


def tp(t):
    return f"<div class='tp'>{t}</div>"


def why(t):
    return f"<p class='why'>{t}</p>"


def table(head, rows):
    h = "".join(f"<th>{x}</th>" for x in head)
    b = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in rows)
    return f"<div class='tw'><table class='st'><tr>{h}</tr>{b}</table></div>"


def T(ok_):
    return "<span class='tf y'>सत्य</span>" if ok_ else "<span class='tf n'>असत्य</span>"


def proof(rows):
    """rows: (statement-html, reason-html)"""
    out = "".join(f"<div class='ps'><span class='n'>{i}.</span><span>{a}<br><span class='r'>कारण: {b}</span></span></div>"
                  for i, (a, b) in enumerate(rows, 1))
    return f"<div class='pf'>{out}</div>"


# ---------------- SVG helpers ----------------
def svg(w, h, body, cap):
    return (f"<div class='fig'><svg viewBox='0 0 {w} {h}' role='img' aria-label='{cap}' style='max-width:{max(w, 360)}px' {FONT}>{body}</svg>"
            f"<div class='cap'>{cap}</div></div>")


def seg(x1, y1, x2, y2, col=INK, w=2.2, dash=None):
    d = f" stroke-dasharray='{dash}'" if dash else ""
    return f"<line x1='{x1}' y1='{y1}' x2='{x2}' y2='{y2}' stroke='{col}' stroke-width='{w}' stroke-linecap='round'{d}/>"


def dot(x, y, col=INK):
    return f"<circle cx='{x}' cy='{y}' r='4' fill='{col}'/>"


def lab(x, y, t, col=INK, size=15, anchor="middle", italic=True):
    st = " font-style='italic'" if italic else ""
    return (f"<text x='{x}' y='{y}' font-size='{size}' font-weight='700' fill='{col}' text-anchor='{anchor}'{st} "
            f"stroke='#fbfcff' stroke-width='4' paint-order='stroke'>{t}</text>")


def tick(x, y, n=1, col=RED, vertical=True):
    """n small equal-length marks centred at (x, y) on a horizontal segment"""
    o = ""
    for k in range(n):
        dx = (k - (n - 1) / 2) * 6
        o += seg(x + dx, y - 7, x + dx, y + 7, col, 2)
    return o


def arrow_line(x1, y, x2, col=INK):
    mk = ("<defs><marker id='ah' viewBox='0 0 10 10' refX='8' refY='5' markerWidth='10' markerHeight='10' markerUnits='userSpaceOnUse' orient='auto-start-reverse'>"
          f"<path d='M0,0 L10,5 L0,10 z' fill='{col}'/></marker></defs>")
    return mk + f"<line x1='{x1}' y1='{y}' x2='{x2}' y2='{y}' stroke='{col}' stroke-width='2.2' marker-start='url(#ah)' marker-end='url(#ah)'/>"


# Fig 5.9: three equal segments AB, PQ, XY
f59 = ""
for i, (a, b, col) in enumerate((("A", "B", BLU), ("P", "Q", GRN), ("X", "Y", ORG))):
    y = 34 + i * 46
    f59 += seg(60, y, 300, y, col) + dot(60, y, col) + dot(300, y, col) + lab(44, y + 5, a, col) + lab(316, y + 5, b, col) + tick(180, y, i + 1 if False else 1)
FIG59 = svg(360, 150, f59, "आकृति 5.9: रेखाखंड AB, PQ और XY")

# Q1 (i): many lines through one point
q1i = ""
import math
for k, col in zip(range(6), (BLU, GRN, ORG, RED, INK, "#7c3aed")):
    ang = math.radians(k * 30)
    dx, dy = 85 * math.cos(ang), 85 * math.sin(ang)
    q1i += seg(180 - dx, 95 - dy, 180 + dx, 95 + dy, col, 1.8)
q1i += dot(180, 95, RED) + lab(210, 106, "P", RED, 14)
FIG1i = svg(360, 190, q1i, "चित्र 1: एक बिंदु P से होकर अनेक रेखाएँ")

# Q1 (ii): one line through two points
q1ii = arrow_line(30, 60, 330) + dot(110, 60, RED) + dot(250, 60, RED) + lab(110, 44, "P", RED) + lab(250, 44, "Q", RED)
FIG1ii = svg(360, 90, q1ii, "चित्र 2: दो भिन्न बिंदुओं P, Q से होकर केवल एक रेखा")

# Q1 (iii): segment extended both ways
q1iii = seg(30, 60, 120, 60, INK, 2, "6 5") + seg(240, 60, 330, 60, INK, 2, "6 5") + seg(120, 60, 240, 60, BLU, 3) + dot(120, 60, BLU) + dot(240, 60, BLU) \
    + lab(120, 44, "A", BLU) + lab(240, 44, "B", BLU) + lab(40, 84, "←", INK, 15, "middle", False) + lab(320, 84, "→", INK, 15, "middle", False)
FIG1iii = svg(360, 100, q1iii, "चित्र 3: सांत रेखा AB को दोनों ओर बढ़ाना (बिंदुदार भाग)")

# Q1 (iv): two equal circles superposed
q1iv = (f"<circle cx='110' cy='80' r='55' fill='none' stroke='{BLU}' stroke-width='2.2'/>" + dot(110, 80, BLU) + seg(110, 80, 165, 80, BLU, 2)
        + lab(98, 74, "O", BLU) + lab(138, 98, "r", BLU, 14)
        + f"<circle cx='260' cy='80' r='55' fill='none' stroke='{GRN}' stroke-width='2.2'/>" + dot(260, 80, GRN) + seg(260, 80, 315, 80, GRN, 2)
        + lab(248, 74, "O′", GRN) + lab(288, 98, "r′", GRN, 14))
FIG1iv = svg(370, 160, q1iv, "चित्र 4: दो बराबर वृत्त, त्रिज्याएँ r और r′")

# Q2 figures
q2a = arrow_line(30, 40, 330, BLU) + arrow_line(30, 100, 330, GRN) + lab(345, 45, "l", BLU) + lab(345, 105, "m", GRN)
FIG2a = svg(370, 130, q2a, "चित्र 5: समांतर रेखाएँ l ∥ m (कभी नहीं मिलतीं)")
q2b = (seg(40, 120, 320, 120, BLU) + seg(180, 20, 180, 140, GRN) + f"<path d='M180,104 L196,104 L196,120' fill='none' stroke='{RED}' stroke-width='1.8'/>"
       + dot(180, 120, RED) + lab(166, 138, "O", RED) + lab(330, 125, "l", BLU, 15, "start") + lab(190, 24, "m", GRN, 15, "start"))
FIG2b = svg(370, 160, q2b, "चित्र 6: लम्ब रेखाएँ l ⊥ m (O पर समकोण का चिह्न)")
q2c = seg(80, 50, 280, 50, BLU, 3) + dot(80, 50, BLU) + dot(280, 50, BLU) + lab(80, 34, "A", BLU) + lab(280, 34, "B", BLU)
FIG2c = svg(360, 80, q2c, "चित्र 7: रेखाखंड AB (दो अंत बिंदु)")
q2d = (f"<circle cx='180' cy='85' r='62' fill='none' stroke='{BLU}' stroke-width='2.2'/>" + dot(180, 85, RED) + seg(180, 85, 224, 41, RED, 2.2) + dot(224, 41, RED)
       + lab(166, 100, "O", RED) + lab(236, 36, "P", RED) + lab(194, 56, "r", RED, 14))
FIG2d = svg(360, 165, q2d, "चित्र 8: केंद्र O, त्रिज्या OP = r")
q2e = (f"<rect x='120' y='30' width='120' height='120' fill='none' stroke='{BLU}' stroke-width='2.2'/>"
       + "".join(f"<path d='{d}' fill='none' stroke='{RED}' stroke-width='1.6'/>" for d in
                 ("M120,44 L134,44 L134,30", "M226,30 L226,44 L240,44", "M240,136 L226,136 L226,150", "M134,150 L134,136 L120,136"))
       + lab(108, 26, "A", BLU) + lab(252, 26, "B", BLU) + lab(252, 164, "C", BLU) + lab(108, 164, "D", BLU)
       + tick(180, 30) + tick(180, 150) + "".join(seg(233, 90 + d, 247, 90 + d, RED, 2) for d in (0,)) + seg(113, 90, 127, 90, RED, 2))
FIG2e = svg(360, 180, q2e, "चित्र 9: वर्ग ABCD (चारों भुजाएँ बराबर, चारों कोण समकोण)")

# Q3 figure: C between A and B; three non-collinear points
q3 = seg(40, 50, 320, 50, BLU) + dot(70, 50, BLU) + dot(290, 50, BLU) + dot(180, 50, RED) + lab(70, 34, "A", BLU) + lab(290, 34, "B", BLU) + lab(180, 34, "C", RED)
FIG3 = svg(360, 80, q3, "चित्र 10: A और B के बीच बिंदु C")
q3b = dot(80, 130, BLU) + dot(280, 130, BLU) + dot(170, 40, RED) + lab(66, 150, "P", BLU) + lab(294, 150, "Q", BLU) + lab(170, 28, "R", RED) + seg(40, 130, 320, 130, BLU, 1.6, "6 5")
FIG3b = svg(360, 165, q3b, "चित्र 11: P, Q एक रेखा पर; R उस रेखा पर नहीं")

# Q4 figure: A — C — B, AC = BC
q4 = seg(50, 50, 310, 50, INK) + dot(50, 50, BLU) + dot(310, 50, BLU) + dot(180, 50, RED) + lab(50, 34, "A", BLU) + lab(310, 34, "B", BLU) + lab(180, 76, "C", RED) \
    + tick(115, 50) + tick(245, 50)
FIG4 = svg(360, 90, q4, "चित्र 12: AC = BC (बराबर भाग एक-एक चिह्न से)")

# Q5 figure: C and D two "midpoints"
q5 = seg(50, 50, 310, 50, INK) + dot(50, 50, BLU) + dot(310, 50, BLU) + dot(180, 50, RED) + dot(212, 50, GRN) + lab(50, 34, "A", BLU) + lab(310, 34, "B", BLU) \
    + lab(180, 76, "C", RED) + lab(212, 76, "D", GRN)
FIG5 = svg(360, 90, q5, "चित्र 13: मान लीजिए C और D दोनों मध्य-बिंदु हैं")

# Fig 5.10: A B C D on a line
f510 = seg(40, 50, 320, 50, INK) + "".join(dot(x, 50, BLU) + lab(x, 34, n, BLU) for x, n in ((60, "A"), (140, "B"), (220, "C"), (300, "D")))
f510 += f"<path d='M60,64 Q140,92 220,64' fill='none' stroke='{RED}' stroke-width='1.6'/>" + lab(140, 98, "AC", RED, 13)
f510 += f"<path d='M140,64 Q220,92 300,64' fill='none' stroke='{GRN}' stroke-width='1.6' stroke-dasharray='5 3'/>" + lab(250, 98, "BD", GRN, 13)
FIG510 = svg(360, 110, f510, "आकृति 5.10: एक रेखा पर बिंदु A, B, C, D")

AX = formula("यूक्लिड के अभिगृहीत (जो इस प्रश्नावली में काम आते हैं)", "", [
    "वे वस्तुएँ जो एक ही वस्तु के बराबर हों, एक दूसरे के बराबर होती हैं।",
    "यदि बराबरों को बराबरों में जोड़ा जाए, तो पूर्ण भी बराबर होते हैं।",
    "यदि बराबरों को बराबरों में से घटाया जाए, तो शेषफल भी बराबर होते हैं।",
    "वे वस्तुएँ जो परस्पर संपाती हों, एक दूसरे के बराबर होती हैं।",
    "पूर्ण अपने भाग से बड़ा होता है।",
    "एक ही वस्तुओं के दुगुने परस्पर बराबर होते हैं।",
    "एक ही वस्तुओं के आधे परस्पर बराबर होते हैं।"])

E = []
# ---------------- Q1 ----------------
s = ""
s += part("(i) एक बिंदु से होकर केवल एक ही रेखा खींची जा सकती है।",
          p("एक बिंदु P लीजिए। P से होकर हम किसी भी दिशा में रेखा खींच सकते हैं, और दिशाएँ अनगिनत हैं।") + FIG1i
          + ans(T(False) + " एक बिंदु से होकर असंख्य (अनगिनत) रेखाएँ खींची जा सकती हैं।"))
s += part("(ii) दो भिन्न बिंदुओं से होकर जाने वाली असंख्य रेखाएँ हैं।",
          p("<b>अभिगृहीत 5.1:</b> दिए हुए दो भिन्न बिंदुओं से होकर एक अद्वितीय (केवल एक) रेखा खींची जा सकती है।") + FIG1ii
          + ans(T(False) + " दो भिन्न बिंदुओं से होकर केवल एक ही रेखा जाती है।"))
s += part("(iii) एक सांत रेखा दोनों ओर अनिश्चित रूप से बढ़ाई जा सकती है।",
          p("<b>यूक्लिड की अभिधारणा 2:</b> एक सांत रेखा (रेखाखंड) को अनिश्चित रूप से बढ़ाया जा सकता है।") + FIG1iii
          + ans(T(True) + " यह यूक्लिड की दूसरी अभिधारणा है।"))
s += part("(iv) यदि दो वृत्त बराबर हैं, तो उनकी त्रिज्याएँ बराबर होती हैं।",
          p("दो वृत्त बराबर हैं, तो एक को दूसरे पर रखने पर वे पूरी तरह संपाती होते हैं (एक-दूसरे को पूरा ढक लेते हैं)।")
          + p("तब दोनों के केंद्र " + m("O") + " और " + m("O'") + " भी एक ही बिंदु पर आते हैं और परिधियाँ भी मिल जाती हैं।") + FIG1iv
          + p("इसलिए केंद्र से परिधि तक की दूरी, अर्थात् त्रिज्याएँ, संपाती होती हैं। अभिगृहीत 4 से:") + eqs(("r", "r'"))
          + ans(T(True) + " बराबर वृत्त संपाती होते हैं, इसलिए उनकी त्रिज्याएँ बराबर होती हैं (अभिगृहीत 4)।"))
s += part("(v) आकृति 5.9 में, यदि " + m("AB = PQ") + " और " + m("PQ = XY") + " है, तो " + m("AB = XY") + " होगा।",
          FIG59 + p("यहाँ " + m("AB") + " और " + m("XY") + " दोनों एक ही वस्तु " + m("PQ") + " के बराबर हैं।")
          + eqs(("AB", "PQ"), ("XY", "PQ")) + p("अभिगृहीत 1 (एक ही वस्तु के बराबर वस्तुएँ परस्पर बराबर) से:") + eqs(("AB", "XY"))
          + ans(T(True) + " अभिगृहीत 1 के अनुसार।"))
s += table(["कथन", "उत्तर", "कारण"], [["(i)", T(False), "एक बिंदु से असंख्य रेखाएँ"], ["(ii)", T(False), "अभिगृहीत 5.1: केवल एक रेखा"],
                                        ["(iii)", T(True), "अभिधारणा 2"], ["(iv)", T(True), "अभिगृहीत 4 (संपाती)"], ["(v)", T(True), "अभिगृहीत 1"]])
E.append((qt("निम्नलिखित कथनों में से कौन-से कथन सत्य हैं और कौन-से कथन असत्य हैं? अपने उत्तरों के लिए कारण दीजिए। "
             "(i) एक बिंदु से होकर केवल एक ही रेखा खींची जा सकती है। (ii) दो भिन्न बिंदुओं से होकर जाने वाली असंख्य रेखाएँ हैं। "
             "(iii) एक सांत रेखा दोनों ओर अनिश्चित रूप से बढ़ाई जा सकती है। (iv) यदि दो वृत्त बराबर हैं, तो उनकी त्रिज्याएँ बराबर होती हैं। "
             "(v) आकृति 5.9 में, यदि " + m("AB = PQ") + " और " + m("PQ = XY") + " है, तो " + m("AB = XY") + " होगा।"), s))

# ---------------- Q2 ----------------
s = tp("<b>अपरिभाषित पद:</b> बिंदु, रेखा और तल ज्यामिति के मूल पद हैं। इन्हें परिभाषित नहीं किया जाता, केवल समझा जाता है। बाकी परिभाषाएँ इन्हीं पर टिकी हैं।")
s += part("(i) समांतर रेखाएँ",
          p("<b>परिभाषा:</b> एक ही तल में स्थित दो रेखाएँ जो दोनों ओर कितनी भी बढ़ाने पर कभी प्रतिच्छेद नहीं करतीं (नहीं मिलतीं), समांतर रेखाएँ कहलाती हैं। लिखते हैं " + m("l \\parallel m") + "।")
          + FIG2a + why("पहले परिभाषित होने चाहिए: बिंदु, रेखा, तल (अपरिभाषित) और प्रतिच्छेद करना।"))
s += part("(ii) लम्ब रेखाएँ",
          p("<b>परिभाषा:</b> दो रेखाएँ जो एक-दूसरे को प्रतिच्छेद करें और प्रतिच्छेद बिंदु पर समकोण (" + m("90^\\circ") + ") बनाएँ, लम्ब रेखाएँ कहलाती हैं। लिखते हैं " + m("l \\perp m") + "।")
          + FIG2b + why("पहले परिभाषित होने चाहिए: रेखा, प्रतिच्छेद बिंदु, कोण और समकोण।"))
s += part("(iii) रेखाखंड",
          p("<b>परिभाषा:</b> किसी रेखा का वह भाग जिसके दो अंत बिंदु हों, रेखाखंड कहलाता है। दो अंत बिंदु " + m("A") + " और " + m("B") + " वाले रेखाखंड को " + m("\\overline{AB}") + " लिखते हैं।")
          + FIG2c + why("पहले परिभाषित होने चाहिए: बिंदु, रेखा और अंत बिंदु।"))
s += part("(iv) वृत्त की त्रिज्या",
          p("<b>परिभाषा:</b> वृत्त के केंद्र को वृत्त के किसी भी बिंदु से मिलाने वाला रेखाखंड वृत्त की त्रिज्या कहलाता है, जैसे " + m("OP") + "।")
          + FIG2d + why("पहले परिभाषित होने चाहिए: वृत्त (एक तल के वे सभी बिंदु जो एक स्थिर बिंदु से बराबर दूरी पर हों), केंद्र और रेखाखंड।"))
s += part("(v) वर्ग",
          p("<b>परिभाषा:</b> वह चतुर्भुज जिसकी चारों भुजाएँ बराबर हों और चारों कोण समकोण हों, वर्ग कहलाता है।")
          + FIG2e + why("पहले परिभाषित होने चाहिए: चतुर्भुज, भुजा, कोण और समकोण।"))
s += ans("हाँ, इन परिभाषाओं के लिए कुछ और पद परिभाषित करने पड़ते हैं, जैसे कोण, समकोण, प्रतिच्छेद, अंत बिंदु, वृत्त, केंद्र, चतुर्भुज। "
         "ये सब अंत में बिंदु, रेखा और तल पर टिके हैं, जो अपरिभाषित पद हैं।")
E.append((qt("निम्नलिखित पदों में से प्रत्येक की परिभाषा दीजिए। क्या इनके लिए कुछ ऐसे पद हैं, जिन्हें परिभाषित करने की आवश्यकता है? वे क्या हैं और आप इन्हें कैसे परिभाषित कर पाएँगे? "
             "(i) समांतर रेखाएँ (ii) लम्ब रेखाएँ (iii) रेखाखंड (iv) वृत्त की त्रिज्या (v) वर्ग"), s))

# ---------------- Q3 ----------------
s = FIG3 + FIG3b
s += part("अपरिभाषित शब्द",
          p("दोनों अभिधारणाओं में <b>बिंदु</b> और <b>रेखा</b> शब्द आए हैं। ये ज्यामिति के अपरिभाषित पद हैं।")
          + p("इनके अलावा ‘के बीच स्थित’ शब्द भी है, जिसे यूक्लिड ने परिभाषित नहीं किया है।")
          + ans("हाँ, बिंदु और रेखा अपरिभाषित शब्द हैं।"))
s += part("क्या ये अविरोधी हैं?",
          p("अभिधारणा (i) एक रेखाखंड पर बिंदुओं की बात करती है; अभिधारणा (ii) कहती है कि सभी बिंदु एक ही रेखा पर नहीं होते।")
          + p("दोनों अलग-अलग स्थितियों की बात करती हैं, इसलिए इनसे कोई ऐसा कथन नहीं बनता जो किसी अभिगृहीत या सिद्ध कथन के विरोध में हो।")
          + ans("हाँ, ये अभिधारणाएँ अविरोधी हैं।"))
s += part("क्या ये यूक्लिड की अभिधारणाओं से प्राप्त होती हैं?",
          p("यूक्लिड की पाँचों अभिधारणाओं में से कोई भी यह नहीं कहती कि दो बिंदुओं के बीच तीसरा बिंदु होता है, या तीन असंरेख बिंदु होते हैं।")
          + p("परंतु अभिगृहीत 5.1 (दो भिन्न बिंदुओं से होकर एक अद्वितीय रेखा) की सहायता से इन्हें समझा जा सकता है: " + m("A") + " और " + m("B")
              + " से होकर जाने वाली रेखा पर " + m("A") + " और " + m("B") + " के बीच बिंदु " + m("C") + " लिया जा सकता है; और उस रेखा के बाहर एक बिंदु " + m("R") + " लेने पर तीन असंरेख बिंदु मिलते हैं।")
          + ans("नहीं, ये यूक्लिड की अभिधारणाओं से प्राप्त नहीं होतीं। ये अभिगृहीत 5.1 से प्राप्त होती हैं।"))
E.append(("नीचे दी हुई दो अभिधारणाओं पर विचार कीजिए: "
          "<span style='display:block;margin-top:4px'>(i) दो भिन्न बिंदु " + m("A") + " और " + m("B") + " दिए रहने पर, एक तीसरा बिंदु " + m("C") + " ऐसा विद्यमान है जो " + m("A") + " और " + m("B") + " के बीच स्थित होता है।</span>"
          "<span style='display:block'>(ii) यहाँ कम से कम ऐसे तीन बिंदु विद्यमान हैं कि वे एक रेखा पर स्थित नहीं हैं।</span>"
          "क्या इन अभिधारणाओं में कोई अपरिभाषित शब्द हैं? क्या ये अभिधारणाएँ अविरोधी हैं? क्या ये यूक्लिड की अभिधारणाओं से प्राप्त होती हैं? स्पष्ट कीजिए।", s))

# ---------------- Q4 ----------------
s = FIG4
s += given("दिया है", "बिंदु " + m("C") + ", " + m("A") + " और " + m("B") + " के बीच है तथा " + m("AC = BC") + "।") if False else ""
s += p("<b>दिया है:</b> बिंदु " + m("C") + ", " + m("A") + " और " + m("B") + " के बीच स्थित है तथा " + m("AC = BC") + "।")
s += p("<b>सिद्ध करना है:</b> " + m("AC = \\dfrac{1}{2} AB"))
s += p("<b>उपपत्ति:</b>")
s += proof([(m("AC = BC") + " &nbsp;&nbsp;...(1)", "दिया है"),
            (m("AC + AC = BC + AC") + " &nbsp;&nbsp;...(2)", "(1) के दोनों पक्षों में " + m("AC") + " जोड़ा (अभिगृहीत 2: बराबरों में बराबर जोड़ने पर पूर्ण बराबर)"),
            (m("BC + AC = AB") + " &nbsp;&nbsp;...(3)", m("C") + ", " + m("A") + " और " + m("B") + " के बीच है, इसलिए दोनों भाग मिलकर पूरा " + m("AB") + " बनाते हैं (संपाती, अभिगृहीत 4)"),
            (m("AC + AC = AB"), "(2) और (3) से (अभिगृहीत 1: एक ही वस्तु के बराबर वस्तुएँ परस्पर बराबर)"),
            (m("2\\,AC = AB"), m("AC + AC = 2 \\times AC")),
            (m("AC = \\dfrac{1}{2} AB"), "दोनों पक्षों को 2 से भाग दिया (अभिगृहीत 7: बराबरों के आधे बराबर)")])
s += ans(m("AC = \\dfrac{1}{2} AB") + " सिद्ध हुआ।")
E.append(("यदि दो बिंदुओं " + m("A") + " और " + m("B") + " के बीच एक बिंदु " + m("C") + " ऐसा स्थित है कि " + m("AC = BC") + " है, तो सिद्ध कीजिए कि "
          + m("AC = \\dfrac{1}{2} AB") + " है। एक आकृति खींच कर इसे स्पष्ट कीजिए।", s))

# ---------------- Q5 ----------------
s = p("<b>सिद्ध करना है:</b> रेखाखंड " + m("AB") + " का एक और केवल एक मध्य-बिंदु होता है।")
s += p("<b>उपपत्ति:</b> मान लीजिए रेखाखंड " + m("AB") + " के दो मध्य-बिंदु " + m("C") + " और " + m("D") + " हैं।") + FIG5
s += proof([(m("AC = \\dfrac{1}{2} AB") + " &nbsp;&nbsp;...(1)", m("C") + " मध्य-बिंदु है (प्रश्न 4 से)"),
            (m("AD = \\dfrac{1}{2} AB") + " &nbsp;&nbsp;...(2)", m("D") + " भी मध्य-बिंदु है (प्रश्न 4 से)"),
            (m("AC = AD"), "(1) और (2) से, दोनों एक ही वस्तु " + m("\\frac{1}{2}AB") + " के बराबर हैं (अभिगृहीत 1)"),
            ("यदि " + m("D") + ", " + m("C") + " से अलग हो, तो " + m("AC") + " और " + m("AD") + " में से एक दूसरे का भाग होगा, और पूर्ण अपने भाग से बड़ा होता है, इसलिए वे बराबर नहीं हो सकते।",
             "अभिगृहीत 5"),
            (m("AC = AD") + " तभी संभव है जब " + m("C") + " और " + m("D") + " एक ही बिंदु हों, अर्थात् संपाती हों।", "ऊपर के चरण 3 और 4 से")])
s += ans("हमारी यह मान्यता गलत है कि दो अलग मध्य-बिंदु हैं। अतः रेखाखंड का एक और केवल एक ही मध्य-बिंदु होता है।")
E.append(("प्रश्न 4 में, " + m("C") + " रेखाखंड " + m("AB") + " का एक मध्य-बिंदु कहलाता है। सिद्ध कीजिए कि एक रेखाखंड का एक और केवल एक ही मध्य-बिंदु होता है।", s))

# ---------------- Q6 ----------------
s = FIG510
s += p("<b>दिया है:</b> " + m("AC = BD"))
s += p("<b>सिद्ध करना है:</b> " + m("AB = CD"))
s += p("<b>उपपत्ति:</b>")
s += proof([(m("AC = AB + BC") + " &nbsp;&nbsp;...(1)", m("B") + ", " + m("A") + " और " + m("C") + " के बीच है"),
            (m("BD = BC + CD") + " &nbsp;&nbsp;...(2)", m("C") + ", " + m("B") + " और " + m("D") + " के बीच है"),
            (m("AC = BD") + " &nbsp;&nbsp;...(3)", "दिया है"),
            (m("AB + BC = BC + CD"), "(1), (2) को (3) में रखने पर (अभिगृहीत 1)"),
            (m("AB + BC - BC = BC + CD - BC"), "दोनों पक्षों में से " + m("BC") + " घटाया (अभिगृहीत 3: बराबरों में से बराबर घटाने पर शेषफल बराबर)"),
            (m("AB = CD"), m("BC - BC = 0"))])
s += ans(m("AB = CD") + " सिद्ध हुआ।")
E.append(("आकृति 5.10 में, यदि " + m("AC = BD") + " है, तो सिद्ध कीजिए कि " + m("AB = CD") + " है।", s))

# ---------------- Q7 ----------------
s = p("<b>अभिगृहीत 5:</b> पूर्ण अपने भाग से बड़ा होता है।")
s += p("यह अभिगृहीत केवल ज्यामिति के लिए नहीं, बल्कि हर प्रकार की राशि (संख्या, लंबाई, क्षेत्रफल, भार, धन आदि) के लिए सत्य है। इसलिए इसे सर्वव्यापी सत्य माना जाता है।")
s += tp("उदाहरण 1 (संख्या): " + m("10 = 6 + 4") + "। यहाँ 10 पूर्ण है और 6 उसका एक भाग है:")
s += eqs(("10", "6 + 4")) + p(m("10 > 6") + " और " + m("10 > 4"))
s += tp("उदाहरण 2 (रेखाखंड): यदि " + m("C") + ", " + m("AB") + " पर " + m("A") + " और " + m("B") + " के बीच हो, तो " + m("AB = AC + CB") + ", इसलिए " + m("AB > AC") + "।")
s += tp("उदाहरण 3 (दैनिक जीवन): एक पूरी रोटी उसके आधे टुकड़े से बड़ी होती है।")
s += ans("क्योंकि ‘पूर्ण अपने भाग से बड़ा होता है’ हर क्षेत्र की हर प्रकार की राशि पर लागू होता है, इसलिए अभिगृहीत 5 एक सर्वव्यापी सत्य माना जाता है।")
E.append(("यूक्लिड की अभिगृहीतों की सूची में दिया हुआ अभिगृहीत 5 एक सर्वव्यापी सत्य क्यों माना जाता है? (ध्यान दीजिए कि यह प्रश्न पाँचवीं अभिधारणा से संबंधित नहीं है।)", s))

# Axioms box shown once at the start of Q1
E[0] = (E[0][0], AX + E[0][1])

import re as _re
for _q, _sol in E:
    for _t in _re.findall(r"\\\((.+?)\\\)", _q + _sol):
        assert not _re.search(r"[\u0900-\u097F]", _t), ("Devanagari in TeX", _t)
page(BASE, 5, CH, "exercise-5-1", "प्रश्नावली 5.1", f"कक्षा 9 गणित · अध्याय 5: {CH} · {len(E)} प्रश्न", E,
     ("/hi/class-09/maths/chapter-04/exercise-4-2/", "प्रश्नावली 4.2"), (BASE, "अध्याय 5"), css=CSS + EXTRA_CSS, boards=BOARDS9)
print("ok")
