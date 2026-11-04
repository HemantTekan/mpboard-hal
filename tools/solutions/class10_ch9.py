#!/usr/bin/env python3
"""Class 10 Maths, Chapter 9 (त्रिकोणमिति के कुछ अनुप्रयोग): Exercise 9.1 (rationalised), Hindi medium.
Run from repo root: python3 tools/solutions/class10_ch9.py
"""
import sys, pathlib, re as _re
from fractions import Fraction as F
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from common import *  # noqa
from common import _LAB

BASE = "/hi/class-10/maths/chapter-09/"
CH = "त्रिकोणमिति के कुछ अनुप्रयोग"
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
S3 = math.sqrt(3)
rad = math.radians


def close(a, b):
    assert abs(a - b) < 1e-9, (a, b)


def sq_at(x, y, sx=-1):
    """small right-angle mark at (x, y): sx=-1 opens left, +1 right."""
    return f"<polyline points='{x + sx * 12},{y} {x + sx * 12},{y - 12} {x},{y - 12}' fill='none' stroke='#1d3a8a' stroke-width='1.3'/>"


def ground(x1=15, x2=325, y=180):
    return f"<line x1='{x1}' y1='{y}' x2='{x2}' y2='{y}' stroke='#7a8499' stroke-width='1.2'/>"


TRIG = formula("उपयोगी मान", "", [m("\\sin30^\\circ=\\tfrac12,\\ \\sin60^\\circ=\\tfrac{\\sqrt3}2,\\ \\cos30^\\circ=\\tfrac{\\sqrt3}2"),
                                   m("\\tan30^\\circ=\\tfrac1{\\sqrt3},\\ \\tan45^\\circ=1,\\ \\tan60^\\circ=\\sqrt3")])
EX = []


def Q(text, body):
    EX.append((text, body))


# ---- Q1
close(10 / math.sin(rad(30)), 20)
f = fig(340, 200, {"A": (260, 40, 12, 4), "B": (260, 180, 12, 14), "C": (40, 180, -6, 16)}, [("A", "B"), ("C", "A")],
        labels=[(80, 172, "30°"), (140, 100, "20 m")], extra=ground() + sq_at(260, 180), caption="AB खंभा, AC रस्सी")
s = f + p("मान लीजिए खंभा AB = h m, रस्सी AC = 20 m, ∠ACB = 30°") + TRIG
s += lines("\\sin30^\\circ", "\\dfrac{AB}{AC}") + eqs(("\\dfrac12", "\\dfrac{h}{20}"), ("h", "10"))
s += "<div class='vt'>जाँच:</div>" + p(m("\\dfrac{10}{20}=\\dfrac12=\\sin30^\\circ") + " ✔") + ans("खंभे की ऊँचाई 10 m है।")
Q("सर्कस का एक कलाकार एक 20 m लंबी डोर पर चढ़ रहा है जो अच्छी तरह से तनी हुई है और भूमि पर सीधे लगे खंभे के शिखर से बँधा हुआ है। यदि भूमि स्तर के साथ डोर द्वारा बनाया गया कोण 30° का हो तो खंभे की ऊँचाई ज्ञात कीजिए।", s)

# ---- Q2
bc, bd = 8 / S3, 16 / S3
close(bc + bd, 8 * S3); close(math.hypot(8, bc), bd)
f = fig(340, 200, {"B": (260, 100, 14, 0), "C": (260, 180, 12, 14), "D": (60, 180, -6, 16)}, [("B", "C"), ("D", "B")],
        labels=[(100, 172, "30°"), (160, 196, "8 m")], extra=ground() + sq_at(260, 180), caption="BC: खड़ा भाग, BD: टूटा भाग")
s = f + p("मान लीजिए पेड़ B पर टूटा, खड़ा भाग BC और टूटा भाग BD है, CD = 8 m, ∠BDC = 30°।") + TRIG
s += lines("\\tan30^\\circ", "\\dfrac{BC}{CD}") + eqs(("\\dfrac1{\\sqrt3}", "\\dfrac{BC}{8}"), ("BC", "\\dfrac{8}{\\sqrt3}\\ \\text{m}"))
s += lines("\\cos30^\\circ", "\\dfrac{CD}{BD}") + eqs(("\\dfrac{\\sqrt3}{2}", "\\dfrac{8}{BD}"), ("BD", "\\dfrac{16}{\\sqrt3}\\ \\text{m}"))
s += lines("\\text{पेड़ की ऊँचाई}", "BC+BD", "\\dfrac{8}{\\sqrt3}+\\dfrac{16}{\\sqrt3}", "\\dfrac{24}{\\sqrt3}", "\\dfrac{24\\sqrt3}{3}", "8\\sqrt3\\ \\text{m}")
s += "<div class='vt'>जाँच (पाइथागोरस):</div>" + p(m("BC^2+CD^2=\\dfrac{64}{3}+64=\\dfrac{256}{3}=BD^2") + " ✔") + ans("पेड़ की ऊँचाई 8√3 m (≈ 13.86 m) है।")
Q("आँधी आने से एक पेड़ टूट जाता है और टूटा हुआ भाग इस तरह मुड़ जाता है कि पेड़ का शिखर ज़मीन को छूने लगता है और इसके साथ 30° का कोण बनाता है। पेड़ के पाद-बिंदु की दूरी, जहाँ पेड़ का शिखर ज़मीन को छूता है, 8 m है। पेड़ की ऊँचाई ज्ञात कीजिए।", s)

# ---- Q3
close(1.5 / math.sin(rad(30)), 3); close(3 / math.sin(rad(60)), 2 * S3)
s = TRIG + part("(i) छोटे बच्चों की फिसलनपट्टी", p("ऊँचाई AB = 1.5 m, लंबाई AC = x m, ∠C = 30°") + lines("\\sin30^\\circ", "\\dfrac{AB}{AC}") + eqs(("\\dfrac12", "\\dfrac{1.5}{x}"), ("x", "3")))
s += part("(ii) बड़े बच्चों की फिसलनपट्टी", p("ऊँचाई PQ = 3 m, लंबाई PR = y m, ∠R = 60°") + lines("\\sin60^\\circ", "\\dfrac{PQ}{PR}") +
          eqs(("\\dfrac{\\sqrt3}2", "\\dfrac{3}{y}"), ("y", "\\dfrac{6}{\\sqrt3}"), ("y", "2\\sqrt3")))
s += "<div class='vt'>जाँच:</div>" + p(m("3\\times\\tfrac12=1.5") + " ✔ और " + m("2\\sqrt3\\times\\tfrac{\\sqrt3}2=3") + " ✔")
s += ans("(i) 3 m (ii) 2√3 m (≈ 3.46 m)")
Q("एक ठेकेदार बच्चों को खेलने के लिए एक पार्क में दो फिसलनपट्टी लगाना चाहती है। 5 वर्ष से कम उम्र के बच्चों के लिए वह एक ऐसी फिसलनपट्टी लगाना चाहती है जिसका शिखर 1.5 m की ऊँचाई पर हो और भूमि के साथ 30° के कोण पर झुका हुआ हो, जबकि इससे अधिक उम्र के बच्चों के लिए वह 3 m की ऊँचाई पर एक अधिक ढाल की फिसलनपट्टी लगाना चाहती है, जो भूमि के साथ 60° का कोण बनाती हो। प्रत्येक स्थिति में फिसलनपट्टी की लंबाई क्या होनी चाहिए?", s)

# ---- Q4
close(30 * math.tan(rad(30)), 10 * S3)
f = fig(340, 200, {"A": (270, 50, 12, 4), "B": (270, 180, 12, 14), "C": (50, 180, -6, 16)}, [("A", "B")], dashed=[("C", "A")],
        labels=[(92, 172, "30°"), (160, 196, "30 m")], extra=ground() + sq_at(270, 180), caption="AB मीनार, C प्रेक्षण बिंदु")
s = f + p("मान लीजिए मीनार AB = h m, BC = 30 m, ∠ACB = 30°") + TRIG + lines("\\tan30^\\circ", "\\dfrac{AB}{BC}") + eqs(("\\dfrac1{\\sqrt3}", "\\dfrac{h}{30}"), ("h", "\\dfrac{30}{\\sqrt3}"), ("h", "10\\sqrt3"))
s += "<div class='vt'>जाँच:</div>" + p(m("\\dfrac{10\\sqrt3}{30}=\\dfrac{1}{\\sqrt3}=\\tan30^\\circ") + " ✔") + ans("मीनार की ऊँचाई 10√3 m (≈ 17.32 m) है।")
Q("भूमि के एक बिंदु से, जो मीनार के पाद-बिंदु से 30 m की दूरी पर है, मीनार के शिखर का उन्नयन कोण 30° है। मीनार की ऊँचाई ज्ञात कीजिए।", s)

# ---- Q5
close(60 / math.sin(rad(60)), 40 * S3)
f = fig(340, 200, {"A": (250, 40, 12, 4), "B": (250, 180, 12, 14), "C": (130, 180, -6, 16)}, [("C", "A")], dashed=[("A", "B")],
        labels=[(152, 170, "60°"), (275, 112, "60 m")], extra=ground() + sq_at(250, 180), caption="A पतंग, AC डोरी")
s = f + p("पतंग A की ऊँचाई AB = 60 m, डोरी AC = l m, ∠ACB = 60°") + TRIG + lines("\\sin60^\\circ", "\\dfrac{AB}{AC}")
s += eqs(("\\dfrac{\\sqrt3}2", "\\dfrac{60}{l}"), ("l", "\\dfrac{120}{\\sqrt3}"), ("l", "40\\sqrt3"))
s += "<div class='vt'>जाँच:</div>" + p(m("40\\sqrt3\\times\\dfrac{\\sqrt3}2=60") + " ✔") + ans("डोरी की लंबाई 40√3 m (≈ 69.28 m) है।")
Q("भूमि से 60 m की ऊँचाई पर एक पतंग उड़ रही है। पतंग में लगी डोरी को अस्थायी रूप से भूमि के एक बिंदु से बाँध दिया गया है। भूमि के साथ डोरी का झुकाव 60° है। यह मानकर कि डोरी में कोई ढील नहीं है, डोरी की लंबाई ज्ञात कीजिए।", s)

# ---- Q6
h = 28.5
close(h / math.tan(rad(30)) - h / math.tan(rad(60)), 19 * S3)
f = fig(340, 200, {"A": (300, 30, 12, 4), "E": (300, 160, 14, 4), "P": (40, 160, -6, -8), "Q": (170, 160, 0, -8)}, [("A", "E")], dashed=[("P", "A"), ("Q", "A")],
        labels=[(75, 154, "30°"), (192, 154, "60°"), (318, 100, "28.5")],
        extra=ground() + "<line x1='40' y1='160' x2='300' y2='160' stroke='#94a3b8' stroke-dasharray='3 3'/><line x1='40' y1='160' x2='40' y2='180' stroke='#1d3a8a' stroke-width='3'/><line x1='170' y1='160' x2='170' y2='180' stroke='#1d3a8a' stroke-width='3'/><line x1='300' y1='180' x2='300' y2='160' stroke='#1d3a8a' stroke-width='2'/>",
        caption="लड़का P से Q तक चलता है; आँख की ऊँचाई 1.5 m")
s = f + p("भवन 30 m, लड़के की आँख की ऊँचाई 1.5 m, इसलिए आँख के स्तर से भवन की ऊँचाई") + lines("AE", "30-1.5", "28.5\\ \\text{m}") + TRIG
s += p("ΔAPE में:") + lines("\\tan30^\\circ", "\\dfrac{AE}{PE}") + eqs(("PE", "28.5\\sqrt3\\ \\text{m}"))
s += p("ΔAQE में:") + lines("\\tan60^\\circ", "\\dfrac{AE}{QE}") + eqs(("QE", "\\dfrac{28.5}{\\sqrt3}\\ \\text{m}"))
s += lines("PQ", "PE-QE", "28.5\\sqrt3-\\dfrac{28.5}{\\sqrt3}", "\\dfrac{28.5\\times3-28.5}{\\sqrt3}", "\\dfrac{57}{\\sqrt3}", "19\\sqrt3\\ \\text{m}")
s += "<div class='vt'>जाँच:</div>" + p(m("PE\\approx49.36,\\ QE\\approx16.45") + ", अंतर " + m("\\approx32.91") + " = " + m("19\\sqrt3") + " ✔")
s += ans("लड़का भवन की ओर 19√3 m (≈ 32.91 m) चला।")
Q("1.5 m लंबा एक लड़का 30 m ऊँचे एक भवन से कुछ दूरी पर खड़ा है। जब वह ऊँचे भवन की ओर जाता है तब उसकी आँख से भवन के शिखर का उन्नयन कोण 30° से 60° हो जाता है। बताइए कि वह भवन की ओर कितनी दूरी तक चलकर गया है।", s)

# ---- Q7
d = 20
close(d * math.tan(rad(60)) - 20, 20 * (S3 - 1))
f = fig(340, 210, {"D": (280, 20, 14, 4), "C": (280, 100, 14, 4), "B": (280, 180, 12, 14), "P": (60, 180, -6, 16)}, [("D", "C"), ("C", "B")], dashed=[("P", "C"), ("P", "D")],
        labels=[(110, 172, "45°"), (98, 150, "60°"), (300, 145, "20 m")], extra=ground() + sq_at(280, 180), caption="BC भवन, CD मीनार")
s = f + p("मान लीजिए भवन BC = 20 m, मीनार CD = h m, P प्रेक्षण बिंदु, PB = x m") + TRIG
s += p("ΔPBC में:") + lines("\\tan45^\\circ", "\\dfrac{BC}{PB}") + eqs(("1", "\\dfrac{20}{x}"), ("x", "20"))
s += p("ΔPBD में:") + lines("\\tan60^\\circ", "\\dfrac{BD}{PB}") + eqs(("\\sqrt3", "\\dfrac{20+h}{20}"), ("20+h", "20\\sqrt3"), ("h", "20(\\sqrt3-1)"))
s += "<div class='vt'>जाँच:</div>" + p(m("\\dfrac{20+20\\sqrt3-20}{20}=\\sqrt3=\\tan60^\\circ") + " ✔") + ans("मीनार की ऊँचाई 20(√3 − 1) m (≈ 14.64 m) है।")
Q("भूमि के एक बिंदु से एक 20 m ऊँचे भवन के शिखर पर लगी एक संचार मीनार के तल और शिखर के उन्नयन कोण क्रमशः 45° और 60° हैं। मीनार की ऊँचाई ज्ञात कीजिए।", s)

# ---- Q8
hp = 0.8 * (S3 + 1)
close((hp + 1.6) / hp, S3)
f = fig(340, 210, {"D": (280, 20, 14, 4), "C": (280, 100, 14, 4), "B": (280, 180, 12, 14), "P": (100, 180, -6, 16)}, [("D", "C"), ("C", "B")], dashed=[("P", "C"), ("P", "D")],
        labels=[(148, 172, "45°"), (130, 148, "60°"), (304, 62, "1.6 m")], extra=ground() + sq_at(280, 180), caption="BC पेडस्टल, CD मूर्ति")
s = f + p("मान लीजिए पेडस्टल BC = h m, मूर्ति CD = 1.6 m, PB = x m") + TRIG
s += p("ΔPBC में:") + lines("\\tan45^\\circ", "\\dfrac{h}{x}") + eqs(("x", "h"))
s += p("ΔPBD में:") + lines("\\tan60^\\circ", "\\dfrac{h+1.6}{x}") + eqs(("\\sqrt3h", "h+1.6"), ("h(\\sqrt3-1)", "1.6"), ("h", "\\dfrac{1.6}{\\sqrt3-1}"), ("h", "\\dfrac{1.6(\\sqrt3+1)}{3-1}"), ("h", "0.8(\\sqrt3+1)"))
s += "<div class='vt'>जाँच:</div>" + p(m("h\\approx2.186,\\ \\dfrac{h+1.6}{h}\\approx\\dfrac{3.786}{2.186}\\approx1.732=\\sqrt3") + " ✔")
s += ans("पेडस्टल की ऊँचाई 0.8(√3 + 1) m (≈ 2.19 m) है।")
Q("एक पेडस्टल के शिखर पर एक 1.6 m ऊँची मूर्ति लगी है। भूमि के एक बिंदु से मूर्ति के शिखर का उन्नयन कोण 60° है और उसी बिंदु से पेडस्टल के शिखर का उन्नयन कोण 45° है। पेडस्टल की ऊँचाई ज्ञात कीजिए।", s)

# ---- Q9
dd = 50 / S3
close(dd * math.tan(rad(30)), 50 / 3)
f = fig(340, 210, {"A": (60, 30, -10, 4), "B": (60, 180, -10, 14), "D": (280, 120, 12, 4), "C": (280, 180, 12, 14)}, [("A", "B"), ("D", "C")], dashed=[("B", "D"), ("C", "A")],
        labels=[(240, 172, "60°"), (98, 172, "30°"), (36, 108, "50 m")], extra=ground(), caption="AB मीनार, CD भवन")
s = f + p("मान लीजिए मीनार AB = 50 m, भवन CD = h m, BC = x m") + TRIG
s += p("ΔABC में (भवन के पाद C से मीनार का शिखर):") + lines("\\tan60^\\circ", "\\dfrac{AB}{BC}") + eqs(("\\sqrt3", "\\dfrac{50}{x}"), ("x", "\\dfrac{50}{\\sqrt3}"))
s += p("ΔDCB में (मीनार के पाद B से भवन का शिखर):") + lines("\\tan30^\\circ", "\\dfrac{CD}{BC}") + eqs(("\\dfrac1{\\sqrt3}", "\\dfrac{h}{50/\\sqrt3}"), ("h", "\\dfrac{50}{3}"), ("h", "16\\tfrac23"))
s += "<div class='vt'>जाँच:</div>" + p(m("x\\approx28.87,\\ \\dfrac{16.67}{28.87}\\approx0.577=\\tan30^\\circ") + " ✔") + ans("भवन की ऊँचाई 50/3 m = 16⅔ m है।")
Q("एक मीनार के पाद-बिंदु से एक भवन के शिखर का उन्नयन कोण 30° है और भवन के पाद-बिंदु से मीनार के शिखर का उन्नयन कोण 60° है। यदि मीनार 50 m ऊँची हो, तो भवन की ऊँचाई ज्ञात कीजिए।", s)

# ---- Q10
x = 20; hh = x * S3
close(hh / (80 - x), math.tan(rad(30)))
f = fig(340, 210, {"A": (30, 50, -10, 4), "B": (30, 180, -10, 14), "D": (310, 50, 12, 4), "C": (310, 180, 12, 14), "P": (100, 180, 0, 16)},
        [("A", "B"), ("D", "C")], dashed=[("P", "A"), ("P", "D")], labels=[(80, 172, "60°"), (140, 172, "30°"), (170, 200, "80 m")], extra=ground(), caption="AB और CD खंभे, P सड़क पर बिंदु")
s = f + p("मान लीजिए दोनों खंभे h m ऊँचे हैं, BP = x m, तब PC = (80 − x) m") + TRIG
s += p("ΔABP में:") + lines("\\tan60^\\circ", "\\dfrac{h}{x}") + eqs(("h", "\\sqrt3x\\quad\\cdots(1)"))
s += p("ΔDCP में:") + lines("\\tan30^\\circ", "\\dfrac{h}{80-x}") + eqs(("h", "\\dfrac{80-x}{\\sqrt3}\\quad\\cdots(2)"))
s += p("(1) और (2) से, दोनों पक्षों को " + m("\\sqrt3") + " से गुणा करने पर") + eqs(("3x", "80-x"), ("4x", "80"), ("x", "20")) + lines("h", "20\\sqrt3\\ \\text{m}")
s += "<div class='vt'>जाँच:</div>" + p(m("\\dfrac{20\\sqrt3}{60}=\\dfrac{1}{\\sqrt3}=\\tan30^\\circ") + " ✔")
s += ans("(i) प्रत्येक खंभे की ऊँचाई 20√3 m (≈ 34.64 m) (ii) बिंदु की खंभों से दूरियाँ 20 m और 60 m")
Q("एक 80 m चौड़ी सड़क के दोनों ओर आमने-सामने समान लंबाई वाले दो खंभे लगे हुए हैं। इन दोनों खंभों के बीच सड़क के एक बिंदु से खंभों के शिखर के उन्नयन कोण क्रमशः 60° और 30° हैं। खंभों की ऊँचाई और खंभों से बिंदु की दूरी ज्ञात कीजिए।", s)

# ---- Q11
w = 10
close(w * S3 / (w + 20), math.tan(rad(30)))
f = fig(340, 210, {"A": (300, 40, 12, 4), "B": (300, 180, 12, 14), "C": (190, 180, 0, 16), "D": (40, 180, -6, 16)}, [("A", "B")], dashed=[("C", "A"), ("D", "A")],
        labels=[(212, 172, "60°"), (80, 172, "30°"), (115, 200, "20 m"), (245, 200, "चौड़ाई")], extra=ground() + sq_at(300, 180), caption="AB टीवी टॉवर, BC नहर की चौड़ाई")
s = f + p("मान लीजिए टॉवर AB = h m, नहर की चौड़ाई BC = x m, CD = 20 m") + TRIG
s += p("ΔABC में:") + lines("\\tan60^\\circ", "\\dfrac{h}{x}") + eqs(("h", "\\sqrt3x\\quad\\cdots(1)"))
s += p("ΔABD में:") + lines("\\tan30^\\circ", "\\dfrac{h}{x+20}") + eqs(("h", "\\dfrac{x+20}{\\sqrt3}\\quad\\cdots(2)"))
s += p("(1) और (2) से, दोनों पक्षों को " + m("\\sqrt3") + " से गुणा करने पर") + eqs(("3x", "x+20"), ("2x", "20"), ("x", "10")) + lines("h", "10\\sqrt3\\ \\text{m}")
s += "<div class='vt'>जाँच:</div>" + p(m("\\dfrac{10\\sqrt3}{30}=\\dfrac1{\\sqrt3}=\\tan30^\\circ") + " ✔")
s += ans("(i) टॉवर की ऊँचाई 10√3 m (≈ 17.32 m) (ii) नहर की चौड़ाई 10 m")
Q("एक नहर के एक तट पर एक टीवी टॉवर ऊर्ध्वाधरतः खड़ा है। टॉवर के ठीक सामने दूसरे तट के एक अन्य बिंदु से टॉवर के शिखर का उन्नयन कोण 60° है। इसी तट पर इस बिंदु से 20 m दूर और इस बिंदु को मीनार के पाद से मिलाने वाली रेखा पर स्थित एक अन्य बिंदु से टॉवर के शिखर का उन्नयन कोण 30° है। टॉवर की ऊँचाई और नहर की चौड़ाई ज्ञात कीजिए।", s)

# ---- Q12
close(7 + 7 * math.tan(rad(60)), 7 * (S3 + 1))
f = fig(340, 210, {"A": (50, 130, -10, 4), "B": (50, 180, -10, 14), "D": (280, 20, 12, 4), "E": (280, 130, 14, 4), "C": (280, 180, 12, 14)},
        [("A", "B"), ("D", "E"), ("E", "C")], dashed=[("A", "D"), ("A", "C"), ("A", "E")], labels=[(96, 118, "60°"), (96, 146, "45°"), (30, 160, "7 m")], extra=ground(),
        caption="AB भवन, CD केबल टॉवर")
s = f + p("मान लीजिए भवन AB = 7 m, टॉवर CD = H m, AE ∥ BC, तब EC = 7 m और AE = BC = x m") + TRIG
s += p("ΔAEC में (अवनमन कोण 45°):") + lines("\\tan45^\\circ", "\\dfrac{EC}{AE}") + eqs(("1", "\\dfrac{7}{x}"), ("x", "7"))
s += p("ΔAED में (उन्नयन कोण 60°):") + lines("\\tan60^\\circ", "\\dfrac{DE}{AE}") + eqs(("DE", "7\\sqrt3"))
s += lines("CD", "DE+EC", "7\\sqrt3+7", "7(\\sqrt3+1)\\ \\text{m}")
s += "<div class='vt'>जाँच:</div>" + p(m("\\dfrac{7\\sqrt3}{7}=\\sqrt3=\\tan60^\\circ") + " ✔") + ans("टॉवर की ऊँचाई 7(√3 + 1) m (≈ 19.12 m) है।")
Q("एक 7 m ऊँचे भवन के शिखर से एक केबल टॉवर के शिखर का उन्नयन कोण 60° है और इसके पाद का अवनमन कोण 45° है। टॉवर की ऊँचाई ज्ञात कीजिए।", s)

# ---- Q13
close(75 / math.tan(rad(30)) - 75, 75 * (S3 - 1))
f = fig(340, 210, {"A": (300, 40, 12, 4), "B": (300, 180, 12, 14), "C": (200, 180, 0, 16), "D": (60, 180, -6, 16)}, [("A", "B")], dashed=[("A", "C"), ("A", "D")],
        labels=[(320, 112, "75 m"), (228, 172, "45°"), (100, 172, "30°")], extra=ground() + sq_at(300, 180), caption="AB प्रकाश-स्तंभ, C और D जहाज़")
s = f + p("प्रकाश-स्तंभ AB = 75 m। अवनमन कोण, संगत उन्नयन कोण के बराबर होता है (एकांतर कोण), इसलिए ∠ACB = 45°, ∠ADB = 30°।") + TRIG
s += p("ΔABC में:") + lines("\\tan45^\\circ", "\\dfrac{75}{BC}") + eqs(("BC", "75\\ \\text{m}"))
s += p("ΔABD में:") + lines("\\tan30^\\circ", "\\dfrac{75}{BD}") + eqs(("BD", "75\\sqrt3\\ \\text{m}"))
s += lines("CD", "BD-BC", "75\\sqrt3-75", "75(\\sqrt3-1)\\ \\text{m}")
s += "<div class='vt'>जाँच:</div>" + p(m("BD\\approx129.90,\\ BC=75") + ", अंतर " + m("\\approx54.90") + " ✔") + ans("दोनों जहाज़ों के बीच की दूरी 75(√3 − 1) m (≈ 54.9 m) है।")
Q("समुद्र-तल से 75 m ऊँचे प्रकाश-स्तंभ के शिखर से देखने पर दो समुद्री जहाज़ों के अवनमन कोण 30° और 45° हैं। यदि प्रकाश-स्तंभ के एक ही ओर एक जहाज़ दूसरे जहाज़ के ठीक पीछे हो तो दोनों जहाज़ों के बीच की दूरी ज्ञात कीजिए।", s)

# ---- Q14
hb = 87
close(hb / math.tan(rad(30)) - hb / math.tan(rad(60)), 58 * S3)
f = fig(340, 210, {"A": (100, 30, 0, -6), "B": (280, 30, 0, -6), "P": (40, 160, -8, 4), "C": (100, 160, 0, 16), "D": (280, 160, 0, 16)},
        [("A", "B")], dashed=[("P", "A"), ("P", "B"), ("A", "C"), ("B", "D")], labels=[(62, 140, "60°"), (86, 158, "30°"), (300, 100, "87 m")],
        extra=ground() + "<line x1='40' y1='160' x2='300' y2='160' stroke='#94a3b8' stroke-dasharray='3 3'/><line x1='40' y1='160' x2='40' y2='180' stroke='#1d3a8a' stroke-width='3'/>",
        caption="A और B गुब्बारे की दो स्थितियाँ; P लड़की की आँख")
s = f + p("गुब्बारे की आँख के स्तर से ऊँचाई") + lines("AC=BD", "88.2-1.2", "87\\ \\text{m}") + TRIG
s += p("ΔACP में:") + lines("\\tan60^\\circ", "\\dfrac{87}{PC}") + eqs(("PC", "\\dfrac{87}{\\sqrt3}"), ("PC", "29\\sqrt3\\ \\text{m}"))
s += p("ΔBDP में:") + lines("\\tan30^\\circ", "\\dfrac{87}{PD}") + eqs(("PD", "87\\sqrt3\\ \\text{m}"))
s += lines("AB=CD", "PD-PC", "87\\sqrt3-29\\sqrt3", "58\\sqrt3\\ \\text{m}")
s += "<div class='vt'>जाँच:</div>" + p(m("PD\\approx150.69,\\ PC\\approx50.23") + ", अंतर " + m("\\approx100.46\\approx58\\sqrt3") + " ✔") + ans("गुब्बारे द्वारा तय की गई दूरी 58√3 m (≈ 100.46 m) है।")
Q("1.2 m लंबी एक लड़की भूमि से 88.2 m की ऊँचाई पर एक क्षैतिज रेखा में हवा में उड़ रहे गुब्बारे को देखती है। किसी भी क्षण लड़की की आँख से गुब्बारे का उन्नयन कोण 60° है। कुछ समय बाद उन्नयन कोण घटकर 30° हो जाता है। इस अंतराल के दौरान गुब्बारे द्वारा तय की गई दूरी ज्ञात कीजिए।", s)

# ---- Q15
hT = 1.0
close((hT * S3 - hT / S3) / 6, (hT / S3) / 3)
f = fig(340, 210, {"A": (300, 40, 12, 4), "B": (300, 180, 12, 14), "C": (210, 180, 0, 16), "D": (40, 180, -6, 16)}, [("A", "B")], dashed=[("A", "C"), ("A", "D")],
        labels=[(232, 172, "60°"), (82, 172, "30°"), (125, 200, "6 सेकंड")], extra=ground() + sq_at(300, 180), caption="AB मीनार; कार D से C तक 6 s में")
s = f + p("मान लीजिए मीनार AB = h m। कार पहले D पर (अवनमन कोण 30°) और 6 s बाद C पर (अवनमन कोण 60°) है। एकांतर कोणों से ∠ADB = 30°, ∠ACB = 60°।") + TRIG
s += p("ΔABD में:") + lines("\\tan30^\\circ", "\\dfrac{h}{BD}") + eqs(("BD", "\\sqrt3h"))
s += p("ΔABC में:") + lines("\\tan60^\\circ", "\\dfrac{h}{BC}") + eqs(("BC", "\\dfrac{h}{\\sqrt3}"))
s += lines("DC", "BD-BC", "\\sqrt3h-\\dfrac{h}{\\sqrt3}", "\\dfrac{3h-h}{\\sqrt3}", "\\dfrac{2h}{\\sqrt3}")
s += p("मान लीजिए कार की एकसमान चाल v m/s है:") + lines("v", "\\dfrac{2h/\\sqrt3}{6}", "\\dfrac{h}{3\\sqrt3}\\ \\text{m/s}")
s += lines("\\text{शेष समय}", "\\dfrac{BC}{v}", "\\dfrac{h/\\sqrt3}{h/(3\\sqrt3)}", "3\\ \\text{s}")
s += "<div class='vt'>जाँच:</div>" + p("BC, DC का आधा है " + m("\\left(\\tfrac{h}{\\sqrt3}=\\tfrac12\\cdot\\tfrac{2h}{\\sqrt3}\\right)") + ", इसलिए समय भी 6 s का आधा = 3 s ✔")
s += ans("कार को मीनार के पाद तक पहुँचने में 3 सेकंड और लगेंगे।")
Q("एक सीधा राजमार्ग एक मीनार के पाद तक जाता है। मीनार के शिखर पर खड़ा एक आदमी एक कार को 30° के अवनमन कोण पर देखता है जो कि मीनार के पाद की ओर एक समान चाल से जाता है। छः सेकंड बाद कार का अवनमन कोण 60° हो गया। इस बिंदु से मीनार के पाद तक पहुँचने में कार द्वारा लिया गया समय ज्ञात कीजिए।", s)

EX = [(qt(t_), b_) for t_, b_ in EX]
page(BASE, 9, CH, "exercise-9-1", "प्रश्नावली 9.1", "कक्षा 10 गणित · अध्याय 9: त्रिकोणमिति के कुछ अनुप्रयोग · 15 प्रश्न (ऊँचाइयाँ और दूरियाँ)", EX, (BASE, "अध्याय 9"), ("/hi/class-10/maths/", "सभी अध्याय"))
print("ok")
