#!/usr/bin/env python3
"""Class 10 Maths, Chapter 13 (सांख्यिकी): Exercise 13.1, 13.2, 13.3 (rationalised), Hindi medium.
Question data as in the NCERT Hindi textbook (jhmh113, reprint 2026-27).
Run from repo root: python3 tools/solutions/class10_ch13.py
"""
import sys, pathlib
from fractions import Fraction as F
from decimal import Decimal, ROUND_HALF_UP
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from common import *  # noqa
from mixed_cells import *  # noqa  (mc, lines, eqs for mixed Hindi/TeX cells)

BASE = "/hi/class-10/maths/chapter-13/"
CH = "सांख्यिकी"

EXTRA_CSS = """
.tw{overflow-x:auto;-webkit-overflow-scrolling:touch;max-width:100%;margin:8px 0 10px}
.st{border-collapse:collapse;font-variant-numeric:tabular-nums;background:#fff;font-size:15px}
.st th,.st td{border:1px solid #d5dbe8;padding:4px 8px;text-align:center;white-space:nowrap}
.st th{background:var(--l);font-weight:700;line-height:1.35;vertical-align:middle}
.qh .st th{white-space:normal;min-width:6em;max-width:12em}
.st td.lb,.st th.lb{white-space:normal;min-width:7.5em;max-width:11em;text-align:left;font-weight:600;background:var(--l)}
.st tr.sum td{font-weight:700;background:#eef2f9}
.st tr.hl td{background:#fff3c4}
.qh .tw{margin:8px 0 4px}.qh .st{font-weight:500;font-size:14.5px}
.qh p.qx{margin:6px 0 0}
.meth{display:inline-block;background:#e9f7f1;border:1px solid #9fd8bf;color:#0b6b48;border-radius:8px;padding:2px 10px;font-weight:700;margin:2px 0 6px}
.st .katex{font-size:1em}
@media (max-width:560px){.st{font-size:14px}.st th,.st td{padding:3px 7px}}
"""

MINUS = "−"


# ---------------- number helpers ----------------
def dec(x, nd=2):
    """Fraction -> exact decimal string when it terminates (<= 4 places), else rounded to nd places."""
    x = F(x)
    for k in range(0, 5):
        if (x * 10 ** k).denominator == 1:
            s = format(Decimal((x * 10 ** k).numerator).scaleb(-k), "f")
            return s
    q = Decimal(x.numerator) / Decimal(x.denominator)
    return str(q.quantize(Decimal(1).scaleb(-nd), rounding=ROUND_HALF_UP))


def exact(x):
    x = F(x)
    return any((x * 10 ** k).denominator == 1 for k in range(5))


def t(x, nd=2):
    """Table text with a real minus sign."""
    s = dec(x, nd)
    return MINUS + s[1:] if s.startswith("-") else s


def tx(x, nd=2):
    """TeX number (minus handled by TeX)."""
    return dec(x, nd)


def P(x):
    """TeX number, parenthesised when negative."""
    s = tx(x)
    return f"({s})" if s.startswith("-") else s


# ---------------- tables ----------------
def hd(a, b):
    """Two-line header: symbol on top, its definition below."""
    return m(a) + "<br>" + m(b)


def sm(a, v):
    """Σ cell on two lines."""
    return m(a) + "<br>" + m("=" + v)


def tab(head, rows, sums=None, hl=None):
    """Working table: head = list of header cells (HTML/TeX), rows = list of lists, sums = Σ row, hl = row index to highlight."""
    h = "".join(f"<th>{c}</th>" for c in head)
    body = ""
    for i, r in enumerate(rows):
        cls = " class='hl'" if hl is not None and i == hl else ""
        body += f"<tr{cls}>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>"
    if sums:
        body += "<tr class='sum'>" + "".join(f"<td>{c}</td>" for c in sums) + "</tr>"
    return f"<div class='tw'><table class='st'><thead><tr>{h}</tr></thead><tbody>{body}</tbody></table></div>"


def dtab(h1, h2, cls, fr, vertical=True):
    vertical = True  # phone readers: two columns always fit; values exactly as in the book
    """Question data table as in the book: horizontal (two rows) or vertical (two columns)."""
    if vertical:
        rows = "".join(f"<tr><td>{c}</td><td>{f}</td></tr>" for c, f in zip(cls, fr))
        return f"<div class='tw'><table class='st'><thead><tr><th>{h1}</th><th>{h2}</th></tr></thead><tbody>{rows}</tbody></table></div>"
    r1 = f"<tr><td class='lb'>{h1}</td>" + "".join(f"<td>{c}</td>" for c in cls) + "</tr>"
    r2 = f"<tr><td class='lb'>{h2}</td>" + "".join(f"<td>{f}</td>" for f in fr) + "</tr>"
    return f"<div class='tw'><table class='st'><tbody>{r1}{r2}</tbody></table></div>"


def Q(text, table, after=""):
    """Question text + its data table (+ a closing sentence). q() wraps the text in <p>...</p>."""
    s = f"{text}</p>{table}"
    return s + (f"<p class='qx'>{after}" if after else "<p class='qx' style='display:none'>")


def cl(lo, hi):
    return f"{lo} {MINUS} {hi}"


def meth(name):
    return f"<div class='meth'>विधि: {name}</div>"


def chk(t_):
    return "<div class='vt'>जाँच:</div>" + p(t_)


H_CI = "वर्ग अंतराल"
FI, XI, DI, UI = m("f_i"), m("x_i"), m("d_i"), m("u_i")

FM_DIRECT = m("\\bar{x}=\\dfrac{\\Sigma f_ix_i}{\\Sigma f_i}")
FM_ASSUMED = m("\\bar{x}=a+\\dfrac{\\Sigma f_id_i}{\\Sigma f_i}")
FM_STEP = m("\\bar{x}=a+h\\times\\dfrac{\\Sigma f_iu_i}{\\Sigma f_i}")
FM_MODE = "बहुलक " + m("=l+\\left(\\dfrac{f_1-f_0}{2f_1-f_0-f_2}\\right)\\times h")
FM_MEDIAN = "माध्यक " + m("=l+\\left(\\dfrac{\\frac{n}{2}-cf}{f}\\right)\\times h")
FM_XI = "वर्ग चिह्न " + XI + " = (उपरि वर्ग सीमा + निचली वर्ग सीमा) ÷ 2"


def formulas(*items):
    """Numbered formula box: सूत्र (1) ..., (2) ..."""
    return formula("", "", list(items)).replace("<b>सूत्र ():</b> ", "<b>सूत्र:</b>")


# ---------------- mean ----------------
def mean_block(classes, fs, method, a=None, h=None, unit="", nd=2, fnum=1, show_formula=True):
    """classes: list of (lo, hi) strings. Returns (html, mean Fraction)."""
    xs = [(F(lo) + F(hi)) / 2 for lo, hi in classes]
    fsF = [F(f) for f in fs]
    N = sum(fsF)
    ci = [cl(lo, hi) for lo, hi in classes]
    out = ""
    if method == "direct":
        fx = [f * x for f, x in zip(fsF, xs)]
        S = sum(fx)
        out += meth("प्रत्यक्ष विधि")
        if show_formula:
            out += formulas(FM_DIRECT)
        out += p(FM_XI)
        out += tab([H_CI, FI, XI, m("f_ix_i")], [[c, t(f), t(x), t(v)] for c, f, x, v in zip(ci, fsF, xs, fx)],
                   ["योग", sm("\\Sigma f_i", tx(N)), "", sm("\\Sigma f_ix_i", tx(S))])
        mean = S / N
        out += f"सूत्र ({fnum}) में मान रखने पर:"
        steps = ["\\dfrac{\\Sigma f_ix_i}{\\Sigma f_i}", f"\\dfrac{{{tx(S)}}}{{{tx(N)}}}"]
        steps.append(tx(mean, nd) + ("" if exact(mean) else "\\ \\text{(लगभग)}"))
        out += lines("\\bar{x}", *steps)
    elif method == "assumed":
        ds = [x - a for x in xs]
        fd = [f * d for f, d in zip(fsF, ds)]
        S = sum(fd)
        out += meth("कल्पित माध्य विधि")
        if show_formula:
            out += formulas(FM_ASSUMED)
        out += p(FM_XI) + p(f"कल्पित माध्य {m('a=' + tx(a))} लिया (बीच का वर्ग चिह्न), तब {m('d_i=x_i-' + tx(a))}")
        out += tab([H_CI, FI, XI, hd("d_i", "=x_i-" + tx(a)), m("f_id_i")],
                   [[c, t(f), t(x), t(d), t(v)] for c, f, x, d, v in zip(ci, fsF, xs, ds, fd)],
                   ["योग", sm("\\Sigma f_i", tx(N)), "", "", sm("\\Sigma f_id_i", tx(S))])
        mean = a + S / N
        out += f"सूत्र ({fnum}) में मान रखने पर:"
        steps = ["a+\\dfrac{\\Sigma f_id_i}{\\Sigma f_i}", f"{tx(a)}+\\left(\\dfrac{{{tx(S)}}}{{{tx(N)}}}\\right)"]
        corr = S / N
        steps.append(f"{tx(a)}{'+' if corr >= 0 else '-'}{tx(abs(corr), nd)}")
        steps.append(tx(mean, nd) + ("" if exact(mean) else "\\ \\text{(लगभग)}"))
        out += lines("\\bar{x}", *steps)
    else:  # step deviation
        ds = [x - a for x in xs]
        us = [d / h for d in ds]
        assert all(u.denominator == 1 for u in us), us
        fu = [f * u for f, u in zip(fsF, us)]
        S = sum(fu)
        out += meth("पग-विचलन विधि")
        if show_formula:
            out += formulas(FM_STEP)
        out += p(FM_XI) + p(f"कल्पित माध्य {m('a=' + tx(a))}, वर्ग माप {m('h=' + tx(h))} लिया, तब "
                            f"{m('d_i=x_i-' + tx(a))} और {m('u_i=\\dfrac{d_i}{h}')}")
        out += tab([H_CI, FI, XI, hd("d_i", "=x_i-" + tx(a)), hd("u_i", "=\\frac{d_i}{" + tx(h) + "}"), m("f_iu_i")],
                   [[c, t(f), t(x), t(d), t(u), t(v)] for c, f, x, d, u, v in zip(ci, fsF, xs, ds, us, fu)],
                   ["योग", sm("\\Sigma f_i", tx(N)), "", "", "", sm("\\Sigma f_iu_i", tx(S))])
        mean = a + h * S / N
        out += f"सूत्र ({fnum}) में मान रखने पर:"
        corr = h * S / N
        steps = ["a+h\\times\\dfrac{\\Sigma f_iu_i}{\\Sigma f_i}",
                 f"{tx(a)}+{tx(h)}\\times\\left(\\dfrac{{{tx(S)}}}{{{tx(N)}}}\\right)"]
        hs = h * S
        if h != 1 and hs.denominator == 1:
            steps.append(f"{tx(a)}{'+' if hs >= 0 else '-'}\\dfrac{{{tx(abs(hs))}}}{{{tx(N)}}}")
        steps.append(f"{tx(a)}{'+' if corr >= 0 else '-'}{tx(abs(corr), nd)}")
        steps.append(tx(mean, nd) + ("" if exact(mean) else "\\ \\text{(लगभग)}"))
        out += lines("\\bar{x}", *steps)
    return out, mean


# ---------------- mode ----------------
def mode_block(classes, fs, fnum=1, show_formula=True, nd=2):
    fsF = [F(f) for f in fs]
    k = max(range(len(fs)), key=lambda i: fsF[i])
    assert sum(1 for f in fsF if f == fsF[k]) == 1
    lo, hi = F(classes[k][0]), F(classes[k][1])
    h = hi - lo
    f1, f0 = fsF[k], (fsF[k - 1] if k > 0 else F(0))
    f2 = fsF[k + 1] if k + 1 < len(fs) else F(0)
    num, den = f1 - f0, 2 * f1 - f0 - f2
    mode = lo + num / den * h
    out = ""
    if show_formula:
        out += formulas(FM_MODE)
    out += tab([H_CI, "बारंबारता " + FI], [[cl(a, b), t(f)] for (a, b), f in zip(classes, fsF)], hl=k)
    out += p(f"अधिकतम बारंबारता {t(f1)} है, जो वर्ग {cl(*classes[k])} की है।")
    out += eqs(("\\text{बहुलक वर्ग}", f"\\text{{{tx(lo)} – {tx(hi)}}}"))
    out += eqs(("\\text{निम्न सीमा } l", tx(lo)),
               ("\\text{वर्ग माप } h", tx(h)),
               ("\\text{बहुलक वर्ग की बारंबारता } f_1", tx(f1)),
               ("\\text{ठीक पहले वाले वर्ग की बारंबारता } f_0", tx(f0)),
               ("\\text{ठीक बाद वाले वर्ग की बारंबारता } f_2", tx(f2)))
    out += f"सूत्र ({fnum}) में मान रखने पर:"
    steps = ["l+\\left(\\dfrac{f_1-f_0}{2f_1-f_0-f_2}\\right)\\times h",
             f"{tx(lo)}+\\left(\\dfrac{{{tx(f1)}-{tx(f0)}}}{{2\\times{tx(f1)}-{tx(f0)}-{tx(f2)}}}\\right)\\times{tx(h)}",
             f"{tx(lo)}+\\dfrac{{{tx(num)}}}{{{tx(den)}}}\\times{tx(h)}",
             f"{tx(lo)}+\\dfrac{{{tx(num * h)}}}{{{tx(den)}}}"]
    corr = num * h / den
    steps.append(f"{tx(lo)}+{tx(corr, nd)}")
    steps.append(tx(mode, nd) + ("" if exact(mode) else "\\ \\text{(लगभग)}"))
    out += lines("\\text{बहुलक}", *steps)
    return out, mode


# ---------------- median ----------------
def median_block(classes, fs, fnum=1, show_formula=True, nd=2, shown=None, fcol=None):
    """classes: (lo, hi) strings used in the formula (continuous). shown: display labels for the class column."""
    fsF = [F(f) for f in fs]
    cf, run = [], F(0)
    for f in fsF:
        run += f
        cf.append(run)
    n = cf[-1]
    k = next(i for i, c in enumerate(cf) if c > n / 2)
    if k > 0:
        assert cf[k - 1] < n / 2 or cf[k - 1] == n / 2
    lo, hi = F(classes[k][0]), F(classes[k][1])
    h = hi - lo
    cfp = cf[k - 1] if k > 0 else F(0)
    f = fsF[k]
    med = lo + (n / 2 - cfp) / f * h
    labels = shown or [cl(a, b) for a, b in classes]
    out = ""
    if show_formula:
        out += formulas(FM_MEDIAN)
    fcells = fcol or [t(x) for x in fsF]
    out += tab([H_CI, "बारंबारता " + FI, "संचयी बारंबारता " + m("cf")],
               [[c, fc, t(x)] for c, fc, x in zip(labels, fcells, cf)],
               ["योग", m("n=" + tx(n)), ""], hl=k)
    out += eqs(("n", tx(n)))
    out += lines("\\dfrac{n}{2}", f"\\dfrac{{{tx(n)}}}{{2}}", tx(n / 2))
    out += p(f"{tx(n / 2)} से अधिक और उसकी निकटतम संचयी बारंबारता {t(cf[k])} है, जो वर्ग {cl(*classes[k])} की है।")
    out += eqs(("\\text{माध्यक वर्ग}", f"\\text{{{tx(lo)} – {tx(hi)}}}"))
    out += eqs(("\\text{निम्न सीमा } l", tx(lo)),
               ("\\text{पिछले वर्ग की संचयी बारंबारता } cf", tx(cfp)),
               ("\\text{माध्यक वर्ग की बारंबारता } f", tx(f)),
               ("\\text{वर्ग माप } h", tx(h)))
    out += f"सूत्र ({fnum}) में मान रखने पर:"
    num = n / 2 - cfp
    steps = ["l+\\left(\\dfrac{\\frac{n}{2}-cf}{f}\\right)\\times h",
             f"{tx(lo)}+\\left(\\dfrac{{{tx(n / 2)}-{tx(cfp)}}}{{{tx(f)}}}\\right)\\times{tx(h)}",
             f"{tx(lo)}+\\dfrac{{{tx(num)}}}{{{tx(f)}}}\\times{tx(h)}",
             f"{tx(lo)}+\\dfrac{{{tx(num * h)}}}{{{tx(f)}}}"]
    corr = num * h / f
    steps.append(f"{tx(lo)}+{tx(corr, nd)}")
    steps.append(tx(med, nd) + ("" if exact(med) else "\\ \\text{(लगभग)}"))
    # drop a duplicate step when the division is trivial
    out += lines("\\text{माध्यक}", *steps)
    return out, med


def close2(v, target, tol=0.006):
    assert abs(float(v) - target) < tol, (float(v), target)


R = "₹"
SO2 = "SO<sub>2</sub>"

# =====================================================================
# 13.1 — माध्य
# =====================================================================
E1 = []

# Q1
C = [("0", "2"), ("2", "4"), ("4", "6"), ("6", "8"), ("8", "10"), ("10", "12"), ("12", "14")]
Fq = [1, 2, 1, 5, 6, 2, 3]
s, v = mean_block(C, Fq, "direct")
close2(v, 8.1)
s += p("प्रत्यक्ष विधि इसलिए चुनी, क्योंकि " + XI + " और " + FI + " दोनों के मान छोटे हैं, इसलिए " + m("f_ix_i") + " सीधे आसानी से निकल जाते हैं।")
s += chk("माध्य 8.1 वर्ग 8 − 10 में है, जहाँ सबसे अधिक (6) घर हैं; उत्तर उचित है ✔")
s += ans("(i) प्रति घर माध्य पौधों की संख्या = 8.1 (ii) विधि: प्रत्यक्ष विधि, क्योंकि xᵢ और fᵢ के मान छोटे हैं।")
E1.append((Q("विद्यार्थियों के एक समूह द्वारा अपने पर्यावरण संचेतना अभियान के अंतर्गत एक सर्वेक्षण किया गया, जिसमें उन्होंने एक मोहल्ले के 20 घरों में लगे हुए पौधों से संबंधित निम्नलिखित आँकड़े एकत्रित किए। प्रति घर माध्य पौधों की संख्या ज्ञात कीजिए।",
              dtab("पौधों की संख्या", "घरों की संख्या", [cl(*c) for c in C], Fq),
              "माध्य ज्ञात करने के लिए आपने किस विधि का प्रयोग किया और क्यों?"), s))

# Q2
C = [("500", "520"), ("520", "540"), ("540", "560"), ("560", "580"), ("580", "600")]
Fq = [12, 14, 8, 6, 10]
s, v = mean_block(C, Fq, "assumed", a=F(550))
close2(v, 545.2)
s += chk(m("\\Sigma f_ix_i=" + tx(sum(F(f) * (F(a) + F(b)) / 2 for (a, b), f in zip(C, Fq)))) + " और "
         + m("\\dfrac{27260}{50}=545.2") + " (प्रत्यक्ष विधि से भी वही) ✔")
assert sum(F(f) * (F(a) + F(b)) / 2 for (a, b), f in zip(C, Fq)) == 27260
s += ans("श्रमिकों की माध्य दैनिक मज़दूरी ₹545.20")
E1.append((Q("किसी फैक्टरी के 50 श्रमिकों की दैनिक मज़दूरी के निम्नलिखित बंटन पर विचार कीजिए:",
              dtab(f"दैनिक मज़दूरी (रुपयों में)", "श्रमिकों की संख्या", [cl(*c) for c in C], Fq),
              "एक उपयुक्त विधि का प्रयोग करते हुए, इस फैक्टरी के श्रमिकों की माध्य दैनिक मज़दूरी ज्ञात कीजिए।"), s))

# Q3 — unknown frequency f
C = [("11", "13"), ("13", "15"), ("15", "17"), ("17", "19"), ("19", "21"), ("21", "23"), ("23", "25")]
Fk = [7, 6, 9, 13, None, 5, 4]
xs = [(F(a) + F(b)) / 2 for a, b in C]
known_fx = sum(F(f) * x for f, x in zip(Fk, xs) if f is not None)
known_f = sum(f for f in Fk if f is not None)
assert known_fx == 752 and known_f == 44
fv = (18 * 44 - 752) / F(20 - 18)
assert fv == 20
rows = []
for (a, b), f, x in zip(C, Fk, xs):
    rows.append([cl(a, b), m("f") if f is None else t(f), t(x), m("20f") if f is None else t(f * x)])
s = meth("प्रत्यक्ष विधि") + formulas(FM_DIRECT) + p(FM_XI)
s += tab([H_CI, FI, XI, m("f_ix_i")], rows, ["योग", sm("\\Sigma f_i", "44+f"), "", sm("\\Sigma f_ix_i", "752+20f")])
s += p("दिया है: माध्य " + m("\\bar{x}=18") + "। सूत्र (1) में मान रखने पर:")
s += eqs(("18", "\\dfrac{752+20f}{44+f}"))
s += p("दोनों पक्षों को " + m("(44+f)") + " से गुणा करने पर:")
s += eqs(("18(44+f)", "752+20f"), ("792+18f", "752+20f"), ("18f-20f", "752-792"), ("-2f", "-40"), ("f", "\\dfrac{-40}{-2}"), ("f", "20"))
s += chk("f = 20 रखने पर " + m("\\Sigma f_i=64") + ", " + m("\\Sigma f_ix_i=752+400=1152") + " और "
         + m("\\dfrac{1152}{64}=18") + " = दिया हुआ माध्य ✔")
assert F(1152, 64) == 18
s += ans("लुप्त बारंबारता f = 20")
E1.append((Q("निम्नलिखित बंटन एक मोहल्ले के बच्चों के दैनिक जेबखर्च दर्शाता है। माध्य जेबखर्च ₹18 है। लुप्त बारंबारता " + m("f") + " ज्ञात कीजिए:",
              dtab("दैनिक जेब भत्ता (रुपयों में)", "बच्चों की संख्या", [cl(*c) for c in C], [m("f") if f is None else f for f in Fk])), s))

# Q4
C = [("65", "68"), ("68", "71"), ("71", "74"), ("74", "77"), ("77", "80"), ("80", "83"), ("83", "86")]
Fq = [2, 4, 3, 8, 7, 4, 2]
s, v = mean_block(C, Fq, "assumed", a=F("75.5"))
close2(v, 75.9)
s += chk("प्रत्यक्ष विधि से " + m("\\Sigma f_ix_i=2277") + " और " + m("\\dfrac{2277}{30}=75.9") + " ✔")
assert sum(F(f) * (F(a) + F(b)) / 2 for (a, b), f in zip(C, Fq)) == 2277
s += ans("महिलाओं के हृदय स्पंदन की प्रति मिनट माध्य संख्या = 75.9")
E1.append((Q("किसी अस्पताल में, एक डॉक्टर द्वारा 30 महिलाओं की जाँच की गई और उनके हृदय स्पंदन (beat) की प्रति मिनट संख्या नोट करके नीचे दर्शाए अनुसार संक्षिप्त रूप में लिखी गई। एक उपयुक्त विधि चुनते हुए, इन महिलाओं के हृदय स्पंदन की प्रति मिनट माध्य संख्या ज्ञात कीजिए:",
              dtab("हृदय स्पंदन की प्रति मिनट संख्या", "महिलाओं की संख्या", [cl(*c) for c in C], Fq)), s))

# Q5
C = [("50", "52"), ("53", "55"), ("56", "58"), ("59", "61"), ("62", "64")]
Fq = [15, 110, 135, 115, 25]
s = p("वर्ग अंतराल सतत नहीं हैं, पर माध्य के लिए केवल वर्ग चिह्न चाहिए (जैसे " + m("\\dfrac{50+52}{2}=51") + "), इसलिए वर्गों को बदलने की आवश्यकता नहीं है।")
b, v = mean_block(C, Fq, "assumed", a=F(57))
s += b
close2(v, 57.19)
s += p(FI + " के मान बड़े (110, 135, 115) हैं, इसलिए कल्पित माध्य विधि चुनी, जिससे गुणा छोटी संख्याओं से हो।")
s += chk("प्रत्यक्ष विधि से " + m("\\Sigma f_ix_i=22875") + " और " + m("\\dfrac{22875}{400}=57.1875") + " ✔")
assert sum(F(f) * (F(a) + F(b)) / 2 for (a, b), f in zip(C, Fq)) == 22875
s += ans("(i) एक पेटी में आमों की माध्य संख्या = 57.19 (लगभग) (ii) विधि: कल्पित माध्य विधि, क्योंकि fᵢ के मान बड़े हैं।")
E1.append((Q("किसी फुटकर बाज़ार में, फल विक्रेता पेटियों में रखे आम बेच रहे थे। इन पेटियों में आमों की संख्याएँ भिन्न-भिन्न थीं। पेटियों की संख्या के अनुसार, आमों का बंटन निम्नलिखित था:",
              dtab("आमों की संख्या", "पेटियों की संख्या", [cl(*c) for c in C], Fq),
              "एक पेटी में रखे आमों की माध्य संख्या ज्ञात कीजिए। आपने माध्य ज्ञात करने की किस विधि का प्रयोग किया है?"), s))

# Q6
C = [("100", "150"), ("150", "200"), ("200", "250"), ("250", "300"), ("300", "350")]
Fq = [4, 5, 12, 2, 2]
s, v = mean_block(C, Fq, "step", a=F(225), h=F(50))
assert v == 211
s += chk("प्रत्यक्ष विधि से " + m("\\Sigma f_ix_i=5275") + " और " + m("\\dfrac{5275}{25}=211") + " ✔")
assert sum(F(f) * (F(a) + F(b)) / 2 for (a, b), f in zip(C, Fq)) == 5275
s += ans("भोजन पर हुआ माध्य दैनिक व्यय ₹211")
E1.append((Q("निम्नलिखित सारणी किसी मोहल्ले के 25 परिवारों में भोजन पर हुए दैनिक व्यय को दर्शाती है:",
              dtab("दैनिक व्यय (रुपयों में)", "परिवारों की संख्या", [cl(*c) for c in C], Fq),
              "एक उपयुक्त विधि द्वारा भोजन पर हुआ माध्य व्यय ज्ञात कीजिए।"), s))

# Q7
C = [("0.00", "0.04"), ("0.04", "0.08"), ("0.08", "0.12"), ("0.12", "0.16"), ("0.16", "0.20"), ("0.20", "0.24")]
Fq = [4, 9, 9, 2, 4, 2]
s, v = mean_block(C, Fq, "step", a=F("0.10"), h=F("0.04"), nd=4)
close2(v, 0.099, 0.0005)
s += chk("प्रत्यक्ष विधि से " + m("\\Sigma f_ix_i=2.96") + " और " + m("\\dfrac{2.96}{30}=0.0987") + " (लगभग) ✔")
assert sum(F(f) * (F(a) + F(b)) / 2 for (a, b), f in zip(C, Fq)) == F("2.96")
s += ans("वायु में SO₂ की माध्य सांद्रता ≈ 0.099 ppm (भाग प्रति मिलियन)")
E1.append((Q(f"वायु में सल्फर डाई-ऑक्साइड ({SO2}) की सांद्रता (भाग प्रति मिलियन में) को ज्ञात करने के लिए, एक नगर के 30 मोहल्लों से आँकड़े एकत्रित किए गए, जिन्हें नीचे प्रस्तुत किया गया है:",
              dtab(f"{SO2} की सांद्रता", "बारंबारता", [cl(*c) for c in C], Fq, vertical=True),
              f"वायु में {SO2} की सांद्रता का माध्य ज्ञात कीजिए।"), s))

# Q8 — unequal class widths
C = [("0", "6"), ("6", "10"), ("10", "14"), ("14", "20"), ("20", "28"), ("28", "38"), ("38", "40")]
Fq = [11, 10, 7, 4, 4, 3, 1]
s = p("वर्ग माप असमान हैं (6, 4, 4, 6, 8, 10, 2), इसलिए पग-विचलन विधि सुविधाजनक नहीं; कल्पित माध्य विधि लेते हैं।")
b, v = mean_block(C, Fq, "assumed", a=F(17))
s += b
close2(v, 12.475, 1e-9)
s += chk("प्रत्यक्ष विधि से " + m("\\Sigma f_ix_i=499") + " और " + m("\\dfrac{499}{40}=12.475") + " ✔")
assert sum(F(f) * (F(a) + F(b)) / 2 for (a, b), f in zip(C, Fq)) == 499
s += ans("एक विद्यार्थी के अनुपस्थित रहने के दिनों का माध्य = 12.475 ≈ 12.48 दिन")
E1.append((Q("किसी कक्षा अध्यापिका ने पूरे सत्र के लिए अपनी कक्षा के 40 विद्यार्थियों की अनुपस्थिति निम्नलिखित रूप में रिकॉर्ड (record) की। एक विद्यार्थी जितने दिन अनुपस्थित रहा उनका माध्य ज्ञात कीजिए:",
              dtab("दिनों की संख्या", "विद्यार्थियों की संख्या", [cl(*c) for c in C], Fq)), s))

# Q9
C = [("45", "55"), ("55", "65"), ("65", "75"), ("75", "85"), ("85", "95")]
Fq = [3, 10, 11, 8, 3]
s, v = mean_block(C, Fq, "step", a=F(70), h=F(10))
close2(v, 69.43)
s += chk("प्रत्यक्ष विधि से " + m("\\Sigma f_ix_i=2430") + " और " + m("\\dfrac{2430}{35}=69.43") + " (लगभग) ✔")
assert sum(F(f) * (F(a) + F(b)) / 2 for (a, b), f in zip(C, Fq)) == 2430
s += ans("माध्य साक्षरता दर = 69.43% (लगभग)")
E1.append((Q("निम्नलिखित सारणी 35 नगरों की साक्षरता दर (प्रतिशत में) दर्शाती है। माध्य साक्षरता दर ज्ञात कीजिए:",
              dtab("साक्षरता दर (% में)", "नगरों की संख्या", [cl(*c) for c in C], Fq)), s))

# =====================================================================
# 13.2 — बहुलक
# =====================================================================
E2 = []

# Q1
C = [("5", "15"), ("15", "25"), ("25", "35"), ("35", "45"), ("45", "55"), ("55", "65")]
Fq = [6, 11, 21, 23, 14, 5]
s = formulas(FM_MODE, FM_DIRECT)
s += part("(i) बहुलक", mode_block(C, Fq, 1, False)[0])
mo = mode_block(C, Fq)[1]
b, mean = mean_block(C, Fq, "direct", fnum=2, show_formula=False)
s += part("(ii) माध्य", b)
close2(mo, 36.82); close2(mean, 35.38)
s += part("(iii) तुलना और व्याख्या", p("बहुलक (36.82 वर्ष) > माध्य (35.38 वर्ष)।")
          + p("अर्थात् अस्पताल में भर्ती होने वाले रोगियों में सबसे अधिक रोगी लगभग 36.8 वर्ष आयु के हैं, जबकि भर्ती हुए रोगियों की औसत आयु लगभग 35.4 वर्ष है।"))
s += ans("(i) बहुलक = 36.82 वर्ष (लगभग) (ii) माध्य = 35.38 वर्ष (लगभग) (iii) अधिकतम रोगी लगभग 36.8 वर्ष के हैं; औसत आयु लगभग 35.4 वर्ष है।")
E2.append((Q("निम्नलिखित सारणी किसी अस्पताल में एक विशेष वर्ष में भर्ती हुए रोगियों की आयु को दर्शाती है:",
              dtab("आयु (वर्षों में)", "रोगियों की संख्या", [cl(*c) for c in C], Fq),
              "उपरोक्त आँकड़ों के बहुलक और माध्य ज्ञात कीजिए। दोनों केंद्रीय प्रवृत्ति की मापों की तुलना कीजिए और उनकी व्याख्या कीजिए।"), s))

# Q2
C = [("0", "20"), ("20", "40"), ("40", "60"), ("60", "80"), ("80", "100"), ("100", "120")]
Fq = [10, 35, 52, 61, 38, 29]
s, mo = mode_block(C, Fq)
close2(mo, 65.625, 1e-9)
s += ans("उपकरणों का बहुलक जीवनकाल = 65.625 घंटे (≈ 65.63 घंटे)")
E2.append((Q("निम्नलिखित आँकड़े, 225 बिजली उपकरणों के प्रेक्षित जीवन काल (घंटों में) की सूचना देते हैं:",
              dtab("जीवनकाल (घंटों में)", "बारंबारता", [cl(*c) for c in C], Fq),
              "उपकरणों का बहुलक जीवनकाल ज्ञात कीजिए।"), s))

# Q3
C = [("1000", "1500"), ("1500", "2000"), ("2000", "2500"), ("2500", "3000"), ("3000", "3500"), ("3500", "4000"), ("4000", "4500"), ("4500", "5000")]
Fq = [24, 40, 33, 28, 30, 22, 16, 7]
s = formulas(FM_MODE, FM_STEP)
b, mo = mode_block(C, Fq, 1, False)
s += part("(i) बहुलक मासिक व्यय", b)
b, mean = mean_block(C, Fq, "step", a=F(2750), h=F(500), fnum=2, show_formula=False)
s += part("(ii) माध्य मासिक व्यय", b)
close2(mo, 1847.83); assert mean == F("2662.5")
s += ans("(i) बहुलक मासिक व्यय = ₹1847.83 (लगभग) (ii) माध्य मासिक व्यय = ₹2662.50")
E2.append((Q("निम्नलिखित आँकड़े किसी गाँव के 200 परिवारों के कुल मासिक घरेलू व्यय के बंटन को दर्शाते हैं। इन परिवारों का बहुलक मासिक व्यय ज्ञात कीजिए। साथ ही, माध्य मासिक व्यय भी ज्ञात कीजिए।",
              dtab("व्यय (रुपयों में)", "परिवारों की संख्या", [cl(*c) for c in C], Fq, vertical=True)), s))

# Q4
C = [("15", "20"), ("20", "25"), ("25", "30"), ("30", "35"), ("35", "40"), ("40", "45"), ("45", "50"), ("50", "55")]
Fq = [3, 8, 9, 10, 3, 0, 0, 2]
s = formulas(FM_MODE, FM_STEP)
b, mo = mode_block(C, Fq, 1, False, nd=3)
s += part("(i) बहुलक", b)
b, mean = mean_block(C, Fq, "step", a=F("32.5"), h=F(5), fnum=2, show_formula=False)
s += part("(ii) माध्य", b)
close2(mo, 30.625, 1e-9); close2(mean, 29.21)
s += part("(iii) व्याख्या", p("बहुलक 30.6 का अर्थ: अधिकतर राज्यों/संघीय क्षेत्रों में प्रति शिक्षक लगभग 30.6 विद्यार्थी हैं।")
          + p("माध्य 29.2 का अर्थ: औसतन प्रति शिक्षक लगभग 29.2 विद्यार्थी हैं।"))
s += ans("(i) बहुलक = 30.625 ≈ 30.6 (ii) माध्य = 29.21 ≈ 29.2 (लगभग) (iii) अधिकतर राज्यों में प्रति शिक्षक लगभग 30.6 विद्यार्थी हैं; औसतन प्रति शिक्षक लगभग 29.2 विद्यार्थी हैं।")
E2.append((Q("निम्नलिखित बंटन भारत के उच्चतर माध्यमिक स्कूलों में, राज्यों के अनुसार, शिक्षक-विद्यार्थी अनुपात को दर्शाता है। इन आँकड़ों के बहुलक और माध्य ज्ञात कीजिए। दोनों मापकों की व्याख्या कीजिए।",
              dtab("प्रति शिक्षक विद्यार्थियों की संख्या", "राज्य/संघीय क्षेत्रों की संख्या", [cl(*c) for c in C], Fq, vertical=True)), s))

# Q5
C = [("3000", "4000"), ("4000", "5000"), ("5000", "6000"), ("6000", "7000"), ("7000", "8000"), ("8000", "9000"), ("9000", "10000"), ("10000", "11000")]
CL5 = ["3000 − 4000", "4000 − 5000", "5000 − 6000", "6000 − 7000", "7000 − 8000", "8000 − 9000", "9000 − 10,000", "10,000 − 11,000"]
Fq = [4, 18, 9, 7, 6, 3, 1, 1]
s, mo = mode_block(C, Fq)
close2(mo, 4608.7, 0.01)
s += ans("बनाए गए रनों का बहुलक = 4608.7 रन (लगभग)")
E2.append((Q("दिया हुआ बंटन विश्व के कुछ श्रेष्ठतम बल्लेबाज़ों द्वारा एकदिवसीय अंतर्राष्ट्रीय क्रिकेट मैचों में बनाए गए रनों को दर्शाता है:",
              dtab("बनाए गए रन", "बल्लेबाज़ों की संख्या", CL5, Fq, vertical=True),
              "इन आँकड़ों का बहुलक ज्ञात कीजिए।"), s))

# Q6
C = [("0", "10"), ("10", "20"), ("20", "30"), ("30", "40"), ("40", "50"), ("50", "60"), ("60", "70"), ("70", "80")]
Fq = [7, 14, 13, 12, 20, 11, 15, 8]
s, mo = mode_block(C, Fq)
close2(mo, 44.7, 0.01)
s += ans("कारों की संख्या का बहुलक = 44.7 (लगभग)")
E2.append((Q("एक विद्यार्थी ने एक सड़क के किसी स्थान से होकर जाती हुई कारों की संख्याएँ नोट कीं और उन्हें नीचे दी हुई सारणी के रूप में व्यक्त किया। सारणी में दिया प्रत्येक प्रेक्षण 3 मिनट के अंतराल में उस स्थान से होकर जाने वाली कारों की संख्याओं से संबंधित है। ऐसे 100 अंतरालों पर प्रेक्षण लिए गए। इन आँकड़ों का बहुलक ज्ञात कीजिए।",
              dtab("कारों की संख्या", "बारंबारता", [cl(*c) for c in C], Fq)), s))

# =====================================================================
# 13.3 — माध्यक
# =====================================================================
E3 = []

# Q1
C = [("65", "85"), ("85", "105"), ("105", "125"), ("125", "145"), ("145", "165"), ("165", "185"), ("185", "205")]
Fq = [4, 5, 13, 20, 14, 8, 4]
s = formulas(FM_MEDIAN, FM_STEP, FM_MODE)
b, med = median_block(C, Fq, 1, False)
s += part("(i) माध्यक", b)
b, mean = mean_block(C, Fq, "step", a=F(135), h=F(20), fnum=2, show_formula=False)
s += part("(ii) माध्य", b)
b, mo = mode_block(C, Fq, 3, False)
s += part("(iii) बहुलक", b)
assert med == 137; close2(mean, 137.06); close2(mo, 135.77)
s += part("(iv) तुलना", p("माध्यक = 137 इकाई, माध्य ≈ 137.06 इकाई, बहुलक ≈ 135.77 इकाई — तीनों लगभग बराबर हैं।")
          + p("अर्थात् अधिकतर उपभोक्ता लगभग 135.8 इकाई बिजली खर्च करते हैं, आधे उपभोक्ता 137 इकाई से कम खर्च करते हैं और औसत खपत लगभग 137 इकाई है।"))
s += ans("(i) माध्यक = 137 इकाई (ii) माध्य = 137.06 इकाई (लगभग) (iii) बहुलक = 135.77 इकाई (लगभग) (iv) तीनों माप लगभग बराबर हैं।")
E3.append((Q("निम्नलिखित बारंबारता बंटन किसी मोहल्ले के 68 उपभोक्ताओं की बिजली की मासिक खपत दर्शाता है। इन आँकड़ों के माध्यक, माध्य और बहुलक ज्ञात कीजिए। इनकी तुलना कीजिए।",
              dtab("मासिक खपत (इकाइयों में)", "उपभोक्ताओं की संख्या", [cl(*c) for c in C], Fq, vertical=True)), s))

# Q2 — unknowns x, y
C = [("0", "10"), ("10", "20"), ("20", "30"), ("30", "40"), ("40", "50"), ("50", "60")]
s = formulas(FM_MEDIAN)
s += tab([H_CI, "बारंबारता " + FI, "संचयी बारंबारता " + m("cf")],
         [[cl(*C[0]), "5", "5"], [cl(*C[1]), m("x"), m("5+x")], [cl(*C[2]), "20", m("25+x")],
          [cl(*C[3]), "15", m("40+x")], [cl(*C[4]), m("y"), m("40+x+y")], [cl(*C[5]), "5", m("45+x+y")]],
         ["योग", m("n=60"), ""], hl=2)
s += p("कुल बारंबारता " + m("n=60") + " है:")
s += eqs(("45+x+y", "60"), ("x+y", "60-45"), ("x+y", "15\\quad\\cdots(2)"))
s += p("माध्यक 28.5 है, जो वर्ग 20 − 30 में है, इसलिए माध्यक वर्ग = 20 − 30:")
s += eqs(("l", "20"), ("\\dfrac{n}{2}", "30"), ("cf", "5+x"), ("f", "20"), ("h", "10"))
s += p("सूत्र (1) में मान रखने पर:")
s += eqs(("28.5", "20+\\left(\\dfrac{30-(5+x)}{20}\\right)\\times10"),
         ("28.5", "20+\\dfrac{25-x}{2}"),
         ("28.5-20", "\\dfrac{25-x}{2}"),
         ("8.5", "\\dfrac{25-x}{2}"))
s += p("दोनों पक्षों को 2 से गुणा करने पर:")
s += eqs(("17", "25-x"), ("x", "25-17"), ("x", "8"))
s += p("समीकरण (2) में x = 8 रखने पर:")
s += eqs(("8+y", "15"), ("y", "15-8"), ("y", "7"))
x_, y_ = 8, 7
med = median_block(C, [5, x_, 20, 15, y_, 5], show_formula=False)[1]
assert med == F("28.5") and 5 + x_ + 20 + 15 + y_ + 5 == 60
s += chk("x = 8, y = 7 रखने पर कुल बारंबारता " + m("5+8+20+15+7+5=60") + " ✔; "
         + m("cf=13") + " और माध्यक " + m("=20+\\dfrac{30-13}{20}\\times10=20+8.5=28.5") + " ✔")
s += ans("(i) x = 8 (ii) y = 7")
E3.append((Q("यदि नीचे दिए हुए बंटन का माध्यक 28.5 हो तो " + m("x") + " और " + m("y") + " के मान ज्ञात कीजिए:",
              dtab("वर्ग अंतराल", "बारंबारता", [cl(*c) for c in C] + ["<b>योग</b>"], ["5", m("x"), "20", "15", m("y"), "5", "<b>60</b>"], vertical=True)), s))

# Q3 — less-than cumulative table
up = [20, 25, 30, 35, 40, 45, 50, 55, 60]
cum = [2, 6, 24, 45, 78, 89, 92, 98, 100]
fr3 = [cum[0]] + [cum[i] - cum[i - 1] for i in range(1, len(cum))]
assert fr3 == [2, 4, 18, 21, 33, 11, 3, 6, 2]
C = [("15", "20")] + [(str(a), str(a + 5)) for a in up[:-1]]
shown = ["18 − 20 (20 से कम)"] + [cl(*c) for c in C[1:]]
fcol = ["2"] + [f"{cum[i]} {MINUS} {cum[i - 1]} = {fr3[i]}" for i in range(1, len(cum))]
s = formulas(FM_MEDIAN)
s += p("दिया गया बंटन ‘से कम’ प्रकार का है। उपरि सीमाएँ 20, 25, …, 60 हैं, इसलिए वर्ग 20 − 25, 25 − 30, …, 55 − 60 बनते हैं। पॉलिसी 18 वर्ष या उससे अधिक आयु पर मिलती है, इसलिए पहला वर्ग 18 − 20 है (‘20 से कम’)। "
       "प्रत्येक वर्ग की बारंबारता = उसकी संचयी बारंबारता − पिछली संचयी बारंबारता:")
b, med = median_block(C, fr3, 1, False, shown=shown, fcol=fcol)
s += b
close2(med, 35.76)
s += p("(पहले वर्ग की निचली सीमा 15 या 18 कुछ भी हो, माध्यक पर कोई प्रभाव नहीं, क्योंकि माध्यक वर्ग 35 − 40 है।)")
s += ans("माध्यक आयु = 35.76 वर्ष (लगभग)")
E3.append((Q("एक जीवन बीमा एजेंट 100 पॉलिसी धारकों की आयु के बंटन के निम्नलिखित आँकड़े ज्ञात करता है। माध्यक आयु परिकलित कीजिए, यदि पॉलिसी केवल उन्हीं व्यक्तियों को दी जाती है, जिनकी आयु 18 वर्ष या उससे अधिक हो, परंतु 60 वर्ष से कम हो।",
              dtab("आयु (वर्षों में)", "पॉलिसी धारकों की संख्या", [f"{u} से कम" for u in up], cum, vertical=True)), s))

# Q4 — inclusive classes -> continuous
orig = [("118", "126"), ("127", "135"), ("136", "144"), ("145", "153"), ("154", "162"), ("163", "171"), ("172", "180")]
Fq = [3, 5, 9, 12, 5, 4, 2]
C = [(dec(F(a) - F(1, 2)), dec(F(b) + F(1, 2))) for a, b in orig]
s = formulas(FM_MEDIAN)
s += p("वर्ग सतत नहीं हैं। एक वर्ग की उपरि सीमा और अगले वर्ग की निचली सीमा का अंतर 1 है, इसलिए प्रत्येक निचली सीमा में से "
       + m("\\dfrac12=0.5") + " घटाकर और प्रत्येक उपरि सीमा में 0.5 जोड़कर वर्गों को सतत बनाया:")
s += tab(["दिया गया वर्ग", "सतत वर्ग"], [[cl(*o), cl(*c)] for o, c in zip(orig, C)])
b, med = median_block(C, Fq, 1, False)
s += b
assert med == F("146.75")
s += ans("पत्तियों की माध्यक लंबाई = 146.75 mm")
E3.append((Q("एक पौधे की 40 पत्तियों की लंबाइयाँ निकटतम मिलीमीटरों में मापी जाती हैं तथा प्राप्त आँकड़ों को निम्नलिखित सारणी के रूप में निरूपित किया जाता है:",
              dtab("लंबाई (mm में)", "पत्तियों की संख्या", [cl(*c) for c in orig], Fq, vertical=True),
              "पत्तियों की माध्यक लंबाई ज्ञात कीजिए।<br><b>संकेत:</b> माध्यक ज्ञात करने के लिए, आँकड़ों को सतत वर्ग अंतरालों में बदलना पड़ेगा, क्योंकि सूत्र में वर्ग अंतरालों को सतत माना गया है। तब ये वर्ग 117.5 − 126.5, 126.5 − 135.5, …, 171.5 − 180.5 में बदल जाते हैं।"), s))

# Q5
C = [("1500", "2000"), ("2000", "2500"), ("2500", "3000"), ("3000", "3500"), ("3500", "4000"), ("4000", "4500"), ("4500", "5000")]
Fq = [14, 56, 60, 86, 74, 62, 48]
s, med = median_block(C, Fq)
close2(med, 3406.98)
s += ans("एक लैंप का माध्यक जीवन काल = 3406.98 घंटे (लगभग)")
E3.append((Q("निम्नलिखित सारणी 400 नियॉन लैंपों के जीवन कालों (life time) को प्रदर्शित करती है:",
              dtab("जीवन काल (घंटों में)", "लैंपों की संख्या", [cl(*c) for c in C], Fq, vertical=True),
              "एक लैंप का माध्यक जीवन काल ज्ञात कीजिए।"), s))

# Q6
C = [("1", "4"), ("4", "7"), ("7", "10"), ("10", "13"), ("13", "16"), ("16", "19")]
Fq = [6, 30, 40, 16, 4, 4]
assert sum(Fq) == 100
s = formulas(FM_MEDIAN, FM_DIRECT, FM_MODE)
b, med = median_block(C, Fq, 1, False)
s += part("(i) माध्यक", b)
b, mean = mean_block(C, Fq, "direct", fnum=2, show_formula=False)
s += part("(ii) माध्य", b)
b, mo = mode_block(C, Fq, 3, False)
s += part("(iii) बहुलक", b)
assert med == F("8.05") and mean == F("8.32"); close2(mo, 7.88)
s += ans("(i) माध्यक अक्षरों की संख्या = 8.05 (ii) माध्य अक्षरों की संख्या = 8.32 (iii) बहुलक = 7.88 (लगभग)")
E3.append((Q("एक स्थानीय टेलीफ़ोन निर्देशिका से 100 कुलनाम (surnames) लिए गए और उनमें प्रयुक्त अंग्रेज़ी वर्णमाला के अक्षरों की संख्या का निम्नलिखित बारंबारता बंटन प्राप्त हुआ:",
              dtab("अक्षरों की संख्या", "कुलनामों की संख्या", [cl(*c) for c in C], Fq),
              "कुलनामों में माध्यक अक्षरों की संख्या ज्ञात कीजिए। कुलनामों में माध्य अक्षरों की संख्या ज्ञात कीजिए। साथ ही, कुलनामों का बहुलक ज्ञात कीजिए।"), s))

# Q7
C = [("40", "45"), ("45", "50"), ("50", "55"), ("55", "60"), ("60", "65"), ("65", "70"), ("70", "75")]
Fq = [2, 3, 8, 6, 6, 3, 2]
s, med = median_block(C, Fq)
close2(med, 56.67)
s += ans("विद्यार्थियों का माध्यक भार = 56.67 kg (लगभग)")
E3.append((Q("नीचे दिया हुआ बंटन एक कक्षा के 30 विद्यार्थियों के भार दर्शा रहा है। विद्यार्थियों का माध्यक भार ज्ञात कीजिए।",
              dtab("भार (किलोग्राम में)", "विद्यार्थियों की संख्या", [cl(*c) for c in C], Fq)), s))

assert (len(E1), len(E2), len(E3)) == (9, 6, 7)
CSS13 = CSS + EXTRA_CSS
page(BASE, 13, CH, "exercise-13-1", "प्रश्नावली 13.1", "कक्षा 10 गणित · अध्याय 13: सांख्यिकी · 9 प्रश्न (वर्गीकृत आँकड़ों का माध्य)", E1,
     (BASE, "अध्याय 13"), (BASE + "exercise-13-2/", "प्रश्नावली 13.2"), css=CSS13)
page(BASE, 13, CH, "exercise-13-2", "प्रश्नावली 13.2", "कक्षा 10 गणित · अध्याय 13: सांख्यिकी · 6 प्रश्न (वर्गीकृत आँकड़ों का बहुलक)", E2,
     (BASE + "exercise-13-1/", "प्रश्नावली 13.1"), (BASE + "exercise-13-3/", "प्रश्नावली 13.3"), css=CSS13)
page(BASE, 13, CH, "exercise-13-3", "प्रश्नावली 13.3", "कक्षा 10 गणित · अध्याय 13: सांख्यिकी · 7 प्रश्न (वर्गीकृत आँकड़ों का माध्यक)", E3,
     (BASE + "exercise-13-2/", "प्रश्नावली 13.2"), (BASE, "अध्याय 13"), css=CSS13)
print("ok")
