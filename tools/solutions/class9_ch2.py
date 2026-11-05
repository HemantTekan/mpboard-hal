#!/usr/bin/env python3
"""Class 9 Maths, Chapter 2 (बहुपद): Exercises 2.1, 2.2, 2.3 (rationalised book: the remainder-theorem
exercise was removed, so the old 2.4 'गुणनखंडन' is 2.3 and the old 2.5 'बीजीय सर्वसमिकाएँ' is 2.4).
User rules: every smallest step shown (class 9 level), formula where used, पक्षांतर shown,
bracket products term by term, LaTeX maths.
Run from repo root: python3 tools/solutions/class9_ch2.py
"""
import sys, pathlib, math
from fractions import Fraction as F
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from common import *  # noqa
from mixed_cells import *  # noqa

BASE = "/hi/class-09/maths/chapter-02/"
CH = "बहुपद"
BOARDS9 = ("यह हल <b>MP Board (MPBSE)</b> कक्षा 9 गणित की पाठ्यपुस्तक के अध्याय 2 ‘बहुपद’ "
           "(NCERT पाठ्यपुस्तक, पुनर्मुद्रण 2025-26) के अनुसार है।")
EXTRA_CSS = """
.tw{overflow-x:auto;-webkit-overflow-scrolling:touch;max-width:100%;margin:8px 0 10px}
.st{border-collapse:collapse;font-variant-numeric:tabular-nums;background:#fff;font-size:15px}
.st th,.st td{border:1px solid #d5dbe8;padding:4px 10px;text-align:center;white-space:nowrap}
.st th{background:var(--l);font-weight:700}.st tr.hl td{background:#fff3c4;font-weight:700}
.tp{background:#fff4ec;border-left:4px solid #e8711a;border-radius:8px;padding:5px 10px;margin:6px 0;font-size:.95em}
.why{font-size:.95em;color:#36405a;margin:2px 0 6px}
.ans .al{margin:10px 0}.eq{row-gap:9px}
.eq .r,.eq .r .katex,.eq .r .katex-html{white-space:normal}.eq .r .base{margin:2px 0}.eq .r{min-width:0}.eq{grid-template-columns:auto auto minmax(0,1fr)}
"""


def tp(t):
    return f"<div class='tp'>{t}</div>"


def why(t):
    return f"<p class='why'>{t}</p>"


# ---------- number / term formatting ----------
def num(v):
    """Fraction -> TeX (no sign handling beyond a leading minus)."""
    v = F(v)
    if v.denominator == 1:
        return str(v.numerator)
    s = "-" if v < 0 else ""
    return f"{s}\\dfrac{{{abs(v.numerator)}}}{{{v.denominator}}}"


def par(v):
    """Value in brackets for substitution: (2), (-1), (\\dfrac{1}{3})."""
    return f"({num(v)})"


def chain(vals):
    """Signed numbers written as a sum: 3 - 5 + 2."""
    out = num(vals[0])
    for v in vals[1:]:
        v = F(v)
        out += f" - {num(-v)}" if v < 0 else f" + {num(v)}"
    return out


def poly(cs, x="x"):
    """Polynomial TeX from coefficient list, highest power first: [1,-2,-1,2] -> x^3 - 2x^2 - x + 2."""
    n = len(cs) - 1
    out = ""
    for i, c in enumerate(cs):
        k = n - i
        if c == 0:
            continue
        c = F(c)
        a = abs(c)
        cs_ = "" if (a == 1 and k > 0) else num(a)
        var = "" if k == 0 else (x if k == 1 else f"{x}^{{{k}}}")
        sign = ("-" if c < 0 else "") if not out else (" - " if c < 0 else " + ")
        out += sign + cs_ + var
    return out or "0"


def subst(name, terms, val, vs="x", ptex=None):
    """p(a) step by step. terms: list of (coef, power) in the book's order.
    Rows: substitute -> powers -> products -> add one pair at a time -> value."""
    rows = []
    # 1. substitute
    s = ""
    for i, (c, k) in enumerate(terms):
        c = F(c)
        a = abs(c)
        if k == 0:
            body = num(a)
        else:
            pw = par(val) + (f"^{{{k}}}" if k > 1 else "")
            body = pw if a == 1 else f"{num(a)}{pw}"
        sign = ("-" if c < 0 else "") if i == 0 else (" - " if c < 0 else " + ")
        s += sign + body
    rows.append(s)
    # 2. powers
    if any(k > 1 for _, k in terms):
        s = ""
        for i, (c, k) in enumerate(terms):
            c = F(c)
            a = abs(c)
            if k == 0:
                body = num(a)
            else:
                pv = F(val) ** k
                pt = par(pv) if (pv < 0 or pv.denominator != 1) else num(pv)
                body = pt if a == 1 else f"{num(a)} \\times {pt}"
            sign = ("-" if c < 0 else "") if i == 0 else (" - " if c < 0 else " + ")
            s += sign + body
        rows.append(s)
    # 3. products
    vals = [F(c) * F(val) ** k for c, k in terms]
    if chain(vals) != rows[-1]:
        rows.append(chain(vals))
    # 4. add one pair at a time
    while len(vals) > 1:
        vals = [vals[0] + vals[1]] + vals[2:]
        rows.append(chain(vals))
    return lines(f"{name}({num(val)})", *rows), vals[0]


# ---------- factorisation helpers ----------
def pairs_table(a, b, c):
    """All integer pairs (m, n) with m·n = a·c, their sums, the pair with sum b highlighted."""
    P = a * c
    seen, rows, pick = set(), [], None
    for d in range(1, abs(P) + 1):
        if abs(P) % d:
            continue
        e = abs(P) // d
        if d > e:
            break
        if pick:
            break
        cands = [(d, e), (-d, -e)] if P > 0 else [(d, -e), (-d, e)]
        for m_, n_ in cands:
            if (m_, n_) in seen:
                continue
            seen.add((m_, n_))
            hl = m_ + n_ == b
            if hl and pick is None:
                pick = (m_, n_)
                break
            rows.append(f"<tr{' class=hl' if hl else ''}><td>{m_}, {n_}</td><td>{m_} × {'(' + str(n_) + ')' if n_ < 0 else n_} = {m_ * n_}</td><td>{m_} + ({n_}) = {m_ + n_}</td></tr>".replace("-", "−"))
    t = ("<div class='tw'><table class='st'><tr><th>संख्याएँ</th><th>गुणनफल</th><th>योग</th></tr>"
         + "".join(rows) + "</table></div>")
    return t, pick


def split_quad(a, b, c, x="x"):
    """Middle-term splitting, every step. Returns (html, (p1, q1), (p2, q2)) factors (p x + q)."""
    h = formula("मध्य पद विभाजन", m(f"a{x}^2 + b{x} + c") + " में ऐसी दो संख्याएँ m, n ढूँढें कि " + m("m + n = b") + " और " + m("m \\times n = a \\times c") + "।")
    h += lines("a", str(a)) + lines("b", str(b)) + lines("c", str(c))
    h += lines("a \\times c", f"{a} \\times {'(' + str(c) + ')' if c < 0 else c}", str(a * c))
    h += p("ऐसी दो संख्याएँ चाहिए जिनका गुणनफल " + m(str(a * c)) + " और योग " + m(str(b)) + " हो:")
    t, (mm, nn) = pairs_table(a, b, c)
    h += t
    # order so that the second group shares the bracket
    for m_, n_ in ((mm, nn), (nn, mm)):
        g = math.gcd(a, m_) * (1 if a > 0 else -1)
        br = (a // g, m_ // g)
        if (n_ * g) % a == 0:
            k = n_ * g // a
            if k * br[1] == c:
                break
    h += p("अतः " + m(f"{m_}") + " और " + m(f"{n_}") + " लेते हैं (" + m(f"{m_} + ({n_}) = {b}") + ", " + m(f"{m_} \\times ({n_}) = {a * c}") + ")। मध्य पद " + m(poly([b, 0], x)) + " को तोड़ते हैं:")
    E = poly([a, b, c], x)
    s2 = poly([a, m_, 0], x) + (" - " if n_ < 0 else " + ") + poly([abs(n_), 0], x) + (" - " if c < 0 else " + ") + str(abs(c))
    br_t = poly(list(br), x)
    g_t = ("" if g == 1 else ("-" if g == -1 else str(g))) + x
    k_t = ("-" if k < 0 else "+") + " " + str(abs(k))
    s3 = f"{g_t}({br_t}) {k_t}({br_t})"
    s4 = f"({br_t})({poly([g, k], x)})"
    h += lines(E, s2, f"({poly([a, m_, 0], x)}) {'-' if n_ < 0 else '+'} ({poly([abs(n_), abs(c) if (n_ < 0) == (c < 0) else -abs(c)], x)})" if False else s2.replace(s2, f"({poly([a, m_, 0], x)}) + ({poly([n_, c], x)})"), s3, s4)
    h += why(f"पहले समूह से {m(g_t)} और दूसरे समूह से {m(str(k))} उभयनिष्ठ निकाला; फिर {m('(' + br_t + ')')} उभयनिष्ठ लिया।")
    # check by multiplying back term by term
    p1, q1, p2, q2 = br[0], br[1], g, k
    assert p1 * p2 == a and p1 * q2 + q1 * p2 == b and q1 * q2 == c
    return h, (p1, q1), (p2, q2)


def fac_tex(pq, x="x"):
    return "(" + poly(list(pq), x) + ")"


def cubic_split(cs, r, x="x"):
    """a x^3 + b x^2 + c x + d with root r: rewrite term by term to take (x - r) common."""
    a, b, c, d = cs
    q1 = b + a * r
    q0 = c + q1 * r
    assert d + q0 * r == 0
    fx = poly([1, -r], x)
    h = p(f"अब पदों को इस प्रकार तोड़ते हैं कि हर जोड़े में {m('(' + fx + ')')} उभयनिष्ठ निकले:")

    def t(cf, k):
        return poly([cf] + [0] * k, x)
    h += tp(m(f"{t(b, 2)} = {t(-a * r, 2)} {'+' if q1 >= 0 else '-'} {t(abs(q1), 2) if q1 else '0'}") + " और " +
            m(f"{t(c, 1)} = {t(-q1 * r, 1) if q1 * r else '0'} {'+' if q0 >= 0 else '-'} {t(abs(q0), 1) if q0 else '0'}"))
    full = poly([a, -a * r, 0, 0], x)
    mid = poly([q1, -q1 * r, 0], x)
    end = poly([q0, -q0 * r], x)
    six = [(a, 3), (-a * r, 2), (q1, 2), (-q1 * r, 1), (q0, 1), (-q0 * r, 0)]
    s1 = ""
    for i_, (cf_, k_) in enumerate(six):
        if cf_ == 0:
            continue
        tt = poly([abs(cf_)] + [0] * k_, x)
        s1 += (("-" if cf_ < 0 else "") if not s1 else (" - " if cf_ < 0 else " + ")) + tt
    grp = f"({full}) + ({mid}) + ({end})"

    def cf(v, k):
        return ("" if v == 1 else ("-" if v == -1 else str(v))) + (x if k == 1 else (f"{x}^{{{k}}}" if k > 1 else ""))
    s2 = f"{cf(a, 2)}({fx})" + (f" {'+' if q1 > 0 else '-'} {cf(abs(q1), 1)}({fx})" if q1 else "") + (f" {'+' if q0 > 0 else '-'} {abs(q0)}({fx})" if q0 else "")
    s3 = f"({fx})({poly([a, q1, q0], x)})"
    h += lines(f"p({x})", s1, grp, s2, s3)
    return h, (a, q1, q0)


def cubic_fact(name, cs, cands, x="x"):
    """Full factorisation of a cubic: find a root by trying factors of the constant term, then split."""
    a, b, c, d = cs
    h = p(f"माना {m(f'p({x}) = ' + poly(cs, x))}।")
    h += formula("गुणनखंड प्रमेय", "यदि " + m(f"p(a) = 0") + " हो, तो " + m(f"({x} - a)") + " बहुपद " + m(f"p({x})") + " का एक गुणनखंड है।")
    h += p("अचर पद " + m(str(d)) + " के गुणनखंड: " + ", ".join(m(f"\\pm {v}") for v in sorted({abs(v) for v in range(1, abs(d) + 1) if d % v == 0})) + "। इन्हें एक-एक करके रखकर देखते हैं:")
    terms = [(a, 3), (b, 2), (c, 1), (d, 0)]
    root = None
    for v in cands:
        st, val = subst("p", terms, v, x)
        h += st
        if val == 0:
            h += ok(m(f"p({num(v)}) = 0") + f", अतः {m('(' + poly([1, -v], x) + ')')} एक गुणनखंड है।")
            root = v
            break
        h += why(m(f"p({num(v)}) = {num(val)} \\neq 0") + f", अतः {m('(' + poly([1, -v], x) + ')')} गुणनखंड नहीं है।")
    s, (A, B, C) = cubic_split(cs, root, x)
    h += s
    h += p(f"अब द्विघात बहुपद {m(poly([A, B, C], x))} के गुणनखंड मध्य पद विभाजन से:")
    s, f1, f2 = split_quad(A, B, C, x)
    h += s
    fs = sorted([(1, -root), f1, f2], key=lambda t: (t[0], t[1]))
    res = "".join(fac_tex(f, x) for f in [(1, -root), f1, f2])
    h += lines(f"p({x})", f"({poly([1, -root], x)})({poly([A, B, C], x)})", res)
    return h, res


# =====================================================================
# Exercise 2.1
# =====================================================================
E1 = []
DEF = formula("एक चर में बहुपद", "जिस व्यंजक में केवल एक चर हो और चर की हर घात एक पूर्ण संख्या (0, 1, 2, 3, …) हो, वह एक चर में बहुपद है।")
s = DEF
s += part("(i) " + m("4x^2 - 3x + 7"), p("चर केवल x है। घातें: " + m("x^2") + " में 2, " + m("x = x^1") + " में 1, और " + m("7 = 7x^0") + " में 0 — सभी पूर्ण संख्याएँ।") + ans("हाँ, यह एक चर x में बहुपद है।"))
s += part("(ii) " + m("y^2 + \\sqrt{2}"), p("चर केवल y है। घातें: " + m("y^2") + " में 2 और " + m("\\sqrt{2} = \\sqrt{2}\\,y^0") + " में 0 — पूर्ण संख्याएँ।") + why(m("\\sqrt{2}") + " गुणांक (अचर) है, चर नहीं; गुणांक कोई भी वास्तविक संख्या हो सकता है।") + ans("हाँ, यह एक चर y में बहुपद है।"))
s += part("(iii) " + m("3\\sqrt{t} + t\\sqrt{2}"), lines("3\\sqrt{t}", "3t^{\\frac{1}{2}}") + p("यहाँ t की घात " + m("\\dfrac{1}{2}") + " है, जो पूर्ण संख्या नहीं है।") + ans("नहीं, यह बहुपद नहीं है।"))
s += part("(iv) " + m("y + \\dfrac{2}{y}"), lines("\\dfrac{2}{y}", "2y^{-1}") + p("यहाँ y की घात −1 है, जो पूर्ण संख्या नहीं है।") + ans("नहीं, यह बहुपद नहीं है।"))
s += part("(v) " + m("x^{10} + y^3 + t^{50}"), p("इसमें तीन चर x, y और t हैं।") + ans("नहीं, यह एक चर में बहुपद नहीं है (यह तीन चरों में बहुपद है)।"))
s += ans("(i) हाँ (ii) हाँ (iii) नहीं (iv) नहीं (v) नहीं, एक चर में नहीं")
E1.append((qt("निम्नलिखित व्यंजकों में कौन-कौन एक चर में बहुपद हैं और कौन-कौन नहीं हैं? कारण के साथ अपने उत्तर दीजिए: "
              "(i) " + m("4x^2 - 3x + 7") + " (ii) " + m("y^2 + \\sqrt{2}") + " (iii) " + m("3\\sqrt{t} + t\\sqrt{2}") + " (iv) " + m("y + \\dfrac{2}{y}") + " (v) " + m("x^{10} + y^3 + t^{50}")), s))

s = formula("गुणांक", m("x^2") + " का गुणांक वह संख्या है जो " + m("x^2") + " से गुणा हो रही है (चिह्न सहित)।")
for lab, e, rw, c in (("(i)", "2 + x^2 + x", "2 + 1 \\cdot x^2 + x", "1"), ("(ii)", "2 - x^2 + x^3", "2 + (-1) \\cdot x^2 + x^3", "-1"),
                      ("(iii)", "\\dfrac{\\pi}{2}x^2 + x", "\\dfrac{\\pi}{2} \\cdot x^2 + x", "\\dfrac{\\pi}{2}"), ("(iv)", "\\sqrt{2}x - 1", "0 \\cdot x^2 + \\sqrt{2}x - 1", "0")):
    s += part(lab + " " + m(e), lines(e, rw) + ans(m("x^2") + " का गुणांक = " + m(c)))
s += ans("(i) 1 (ii) −1 (iii) " + m("\\dfrac{\\pi}{2}") + " (iv) 0")
E1.append((qt("निम्नलिखित में से प्रत्येक में " + m("x^2") + " का गुणांक लिखिए: (i) " + m("2 + x^2 + x") + " (ii) " + m("2 - x^2 + x^3") + " (iii) " + m("\\dfrac{\\pi}{2}x^2 + x") + " (iv) " + m("\\sqrt{2}x - 1")), s))

s = formula("परिभाषाएँ", "", ["द्विपद: जिस बहुपद में दो पद हों।", "एकपदी: जिस बहुपद में केवल एक पद हो।", "घात: चर की सबसे बड़ी घात।"])
s += part("घात 35 वाला द्विपद", p("दो पद चाहिए और सबसे बड़ी घात 35 हो, जैसे " + m("x^{35}") + " और " + m("-1") + ":") + lines("\\text{द्विपद}", "x^{35} - 1"))
s += part("घात 100 वाला एकपदी", p("एक ही पद चाहिए जिसकी घात 100 हो:") + lines("\\text{एकपदी}", "y^{100}"))
s += ans("घात 35 का द्विपद: " + m("x^{35} - 1") + "; घात 100 का एकपदी: " + m("y^{100}") + " (अन्य उदाहरण भी सही हैं)")
E1.append(("घात 35 वाले द्विपद का और घात 100 वाले एकपदी का एक-एक उदाहरण दीजिए।", s))

s = formula("बहुपद की घात", "बहुपद के पदों में चर की सबसे बड़ी घात।")
for lab, e, pw, dg in (("(i)", "5x^3 + 4x^2 + 7x", "5x^3 \\to 3,\\ 4x^2 \\to 2,\\ 7x \\to 1", "3"), ("(ii)", "4 - y^2", "4 \\to 0,\\ -y^2 \\to 2", "2"),
                       ("(iii)", "5t - \\sqrt{7}", "5t \\to 1,\\ -\\sqrt{7} \\to 0", "1"), ("(iv)", "3", "3 = 3x^0 \\to 0", "0")):
    s += part(lab + " " + m(e), p("हर पद की घात: " + m(pw)) + ans("सबसे बड़ी घात " + dg + ", अतः घात = " + dg))
s += ans("(i) 3 (ii) 2 (iii) 1 (iv) 0")
E1.append((qt("निम्नलिखित बहुपदों में से प्रत्येक बहुपद की घात लिखिए: (i) " + m("5x^3 + 4x^2 + 7x") + " (ii) " + m("4 - y^2") + " (iii) " + m("5t - \\sqrt{7}") + " (iv) " + m("3")), s))

s = formula("वर्गीकरण (घात के अनुसार)", "", ["घात 1 → रैखिक बहुपद", "घात 2 → द्विघाती बहुपद", "घात 3 → त्रिघाती बहुपद"])
res = []
for lab, e, dg, k in (("(i)", "x^2 + x", 2, "द्विघाती"), ("(ii)", "x - x^3", 3, "त्रिघाती"), ("(iii)", "y + y^2 + 4", 2, "द्विघाती"), ("(iv)", "1 + x", 1, "रैखिक"),
                      ("(v)", "3t", 1, "रैखिक"), ("(vi)", "r^2", 2, "द्विघाती"), ("(vii)", "7x^3", 3, "त्रिघाती")):
    s += part(lab + " " + m(e), p(f"सबसे बड़ी घात = {dg}") + ans(k))
    res.append(f"{lab} {k}")
s += ans(" ".join(res))
E1.append((qt("निम्नलिखित को रैखिक, द्विघाती और त्रिघाती बहुपदों में वर्गीकृत कीजिए: (i) " + m("x^2 + x") + " (ii) " + m("x - x^3") + " (iii) " + m("y + y^2 + 4")
              + " (iv) " + m("1 + x") + " (v) " + m("3t") + " (vi) " + m("r^2") + " (vii) " + m("7x^3")), s))
assert len(E1) == 5

# =====================================================================
# Exercise 2.2
# =====================================================================
E2 = []
SUB = formula("बहुपद का मान", m("p(x)") + " में " + m("x") + " के स्थान पर दी गई संख्या रखकर गणना करने से " + m("p(\\text{संख्या})").replace("\\text{संख्या}", "a") + " मिलता है।")
s = SUB + p("माना " + m("p(x) = 5x - 4x^2 + 3") + "।")
T = [(5, 1), (-4, 2), (3, 0)]
outs = []
for lab, v in (("(i)", 0), ("(ii)", -1), ("(iii)", 2)):
    st, val = subst("p", T, v)
    s += part(lab + " " + m(f"x = {v}"), st + ans(f"मान = {num(val)}".replace("-", "−")))
    outs.append(f"{lab} {num(val)}".replace("-", "−"))
assert [5 * v - 4 * v * v + 3 for v in (0, -1, 2)] == [3, -6, -3]
s += ans(" ".join(outs))
E2.append((qt("निम्नलिखित पर बहुपद " + m("5x - 4x^2 + 3") + " के मान ज्ञात कीजिए: (i) " + m("x = 0") + " (ii) " + m("x = -1") + " (iii) " + m("x = 2")), s))

s = SUB
outs = []
for lab, nm, vs, T, ptx in (("(i)", "p", "y", [(1, 2), (-1, 1), (1, 0)], "y^2 - y + 1"), ("(ii)", "p", "t", [(2, 0), (1, 1), (2, 2), (-1, 3)], "2 + t + 2t^2 - t^3"),
                           ("(iii)", "p", "x", [(1, 3)], "x^3")):
    b_ = p("माना " + m(f"p({vs}) = {ptx}") + "।")
    vals = []
    for v in (0, 1, 2):
        st, val = subst("p", T, v)
        b_ += st
        vals.append(val)
    b_ += ans(f"p(0) = {num(vals[0])}, p(1) = {num(vals[1])}, p(2) = {num(vals[2])}")
    outs.append(f"{lab} {num(vals[0])}, {num(vals[1])}, {num(vals[2])}")
    s += part(lab + " " + m(f"p({vs}) = {ptx}"), b_)
b_ = p("माना " + m("p(x) = (x - 1)(x + 1)") + "। हर बार दोनों कोष्ठकों में x का मान रखेंगे:")
vals = []
for v in (0, 1, 2):
    a1, a2 = v - 1, v + 1
    b_ += lines(f"p({v})", f"({v} - 1)({v} + 1)", f"({a1})({a2})", f"{a1} \\times {a2}", str(a1 * a2))
    vals.append(a1 * a2)
b_ += ans(f"p(0) = {vals[0]}, p(1) = {vals[1]}, p(2) = {vals[2]}".replace("-", "−"))
outs.append(f"(iv) {vals[0]}, {vals[1]}, {vals[2]}".replace("-", "−"))
s += part("(iv) " + m("p(x) = (x - 1)(x + 1)"), b_)
s += ans(" ".join(outs))
E2.append((qt("निम्नलिखित बहुपदों में से प्रत्येक बहुपद के लिए p(0), p(1) और p(2) ज्ञात कीजिए: (i) " + m("p(y) = y^2 - y + 1") + " (ii) " + m("p(t) = 2 + t + 2t^2 - t^3")
              + " (iii) " + m("p(x) = x^3") + " (iv) " + m("p(x) = (x - 1)(x + 1)")), s))

ZER = formula("शून्यक", "यदि " + m("p(a) = 0") + " हो, तो संख्या a बहुपद " + m("p(x)") + " का शून्यक है।")
s = ZER
st, v = subst("p", [(3, 1), (1, 0)], F(-1, 3))
s += part("(i) " + m("p(x) = 3x + 1,\\ x = -\\dfrac{1}{3}"), lines("p\\left(-\\dfrac{1}{3}\\right)", "3\\left(-\\dfrac{1}{3}\\right) + 1", "-\\dfrac{3}{3} + 1", "-1 + 1", "0") + ans(m("-\\dfrac{1}{3}") + " शून्यक है।"))
s += part("(ii) " + m("p(x) = 5x - \\pi,\\ x = \\dfrac{4}{5}"), lines("p\\left(\\dfrac{4}{5}\\right)", "5\\left(\\dfrac{4}{5}\\right) - \\pi", "\\dfrac{20}{5} - \\pi", "4 - \\pi")
          + why("π ≈ 3.14, अतः " + m("4 - \\pi \\approx 0.86 \\neq 0") + "।") + ans(m("\\dfrac{4}{5}") + " शून्यक <b>नहीं</b> है।"))
b_ = ""
for v in (1, -1):
    st, val = subst("p", [(1, 2), (-1, 0)], v)
    b_ += st
    assert val == 0
s += part("(iii) " + m("p(x) = x^2 - 1,\\ x = 1, -1"), b_ + ans("1 और −1 दोनों शून्यक हैं।"))
b_ = ""
for v in (-1, 2):
    a1, a2 = v + 1, v - 2
    b_ += lines(f"p({v})", f"({v} + 1)({v} - 2)", f"({a1})({a2})", f"{a1} \\times ({a2})" if a2 < 0 else f"{a1} \\times {a2}", str(a1 * a2))
    assert a1 * a2 == 0
s += part("(iv) " + m("p(x) = (x + 1)(x - 2),\\ x = -1, 2"), b_ + ans("−1 और 2 दोनों शून्यक हैं।"))
st, val = subst("p", [(1, 2)], 0)
s += part("(v) " + m("p(x) = x^2,\\ x = 0"), st + ans("0 शून्यक है।"))
s += part("(vi) " + m("p(x) = lx + m,\\ x = -\\dfrac{m}{l}"), lines("p\\left(-\\dfrac{m}{l}\\right)", "l\\left(-\\dfrac{m}{l}\\right) + m", "-\\dfrac{l \\times m}{l} + m", "-m + m", "0") + why("l अंश और हर दोनों में है, कट गया।") + ans(m("-\\dfrac{m}{l}") + " शून्यक है।"))
b_ = lines("p\\left(-\\dfrac{1}{\\sqrt{3}}\\right)", "3\\left(-\\dfrac{1}{\\sqrt{3}}\\right)^2 - 1", "3 \\times \\dfrac{(-1)^2}{(\\sqrt{3})^2} - 1", "3 \\times \\dfrac{1}{3} - 1", "\\dfrac{3}{3} - 1", "1 - 1", "0")
b_ += ok(m("-\\dfrac{1}{\\sqrt{3}}") + " शून्यक है।")
b_ += lines("p\\left(\\dfrac{2}{\\sqrt{3}}\\right)", "3\\left(\\dfrac{2}{\\sqrt{3}}\\right)^2 - 1", "3 \\times \\dfrac{2^2}{(\\sqrt{3})^2} - 1", "3 \\times \\dfrac{4}{3} - 1", "\\dfrac{12}{3} - 1", "4 - 1", "3")
b_ += why(m("p\\left(\\dfrac{2}{\\sqrt{3}}\\right) = 3 \\neq 0") + "।")
s += part("(vii) " + m("p(x) = 3x^2 - 1,\\ x = -\\dfrac{1}{\\sqrt{3}}, \\dfrac{2}{\\sqrt{3}}"), b_ + ans(m("-\\dfrac{1}{\\sqrt{3}}") + " शून्यक है, पर " + m("\\dfrac{2}{\\sqrt{3}}") + " शून्यक <b>नहीं</b> है।"))
s += part("(viii) " + m("p(x) = 2x + 1,\\ x = \\dfrac{1}{2}"), lines("p\\left(\\dfrac{1}{2}\\right)", "2\\left(\\dfrac{1}{2}\\right) + 1", "\\dfrac{2}{2} + 1", "1 + 1", "2") + why(m("2 \\neq 0")) + ans(m("\\dfrac{1}{2}") + " शून्यक <b>नहीं</b> है।"))
s += ans("(i) हाँ (ii) नहीं (iii) हाँ, दोनों (iv) हाँ, दोनों (v) हाँ (vi) हाँ (vii) " + m("-\\tfrac{1}{\\sqrt{3}}") + " हाँ, " + m("\\tfrac{2}{\\sqrt{3}}") + " नहीं (viii) नहीं")
E2.append((qt("सत्यापित कीजिए कि दिखाए गए मान निम्नलिखित स्थितियों में संगत बहुपद के शून्यक हैं: "
              "(i) " + m("p(x) = 3x + 1;\\ x = -\\dfrac{1}{3}") + " (ii) " + m("p(x) = 5x - \\pi;\\ x = \\dfrac{4}{5}") + " (iii) " + m("p(x) = x^2 - 1;\\ x = 1, -1")
              + " (iv) " + m("p(x) = (x + 1)(x - 2);\\ x = -1, 2") + " (v) " + m("p(x) = x^2;\\ x = 0") + " (vi) " + m("p(x) = lx + m;\\ x = -\\dfrac{m}{l}")
              + " (vii) " + m("p(x) = 3x^2 - 1;\\ x = -\\dfrac{1}{\\sqrt{3}}, \\dfrac{2}{\\sqrt{3}}") + " (viii) " + m("p(x) = 2x + 1;\\ x = \\dfrac{1}{2}")), s))

s = formula("शून्यक ज्ञात करना", m("p(x) = 0") + " रखकर x का मान निकालें।")


def lin_zero(a, b, at=None, bt=None):
    """Zero of a x + b, every step with पक्षांतर."""
    at = at or str(a)
    bt = bt if bt is not None else str(abs(b))
    ex = (("" if at == "1" else at) + "x") + ((" + " if b > 0 else " - ") + bt if b else "")
    h = eqs(("p(x)", "0"), (ex, "0"))
    if b:
        h += tp(f"पक्षांतर: {'+' if b > 0 else '−'}{bt} दाएँ पक्ष में जाकर {'−' if b > 0 else '+'}{bt} हो जाता है।")
        h += eqs((("" if at == "1" else at) + "x", ("-" if b > 0 else "") + bt))
    if at != "1":
        h += tp(f"पक्षांतर: x का गुणक {at} दाएँ पक्ष में भाग बनकर जाता है।")
        h += eqs(("x", (("-" if b > 0 else "") + f"\\dfrac{{{bt}}}{{{at}}}") if b else f"\\dfrac{{0}}{{{at}}}"))
    return h


outs = []
for lab, a, b, txt, z in (("(i)", 1, 5, "x + 5", "-5"), ("(ii)", 1, -5, "x - 5", "5"), ("(iii)", 2, 5, "2x + 5", "-\\dfrac{5}{2}"),
                          ("(iv)", 3, -2, "3x - 2", "\\dfrac{2}{3}"), ("(v)", 3, 0, "3x", "0")):
    h = lin_zero(a, b)
    if lab == "(v)":
        h += lines("x", "0")
    s += part(lab + " " + m("p(x) = " + txt), h + ans("शून्यक " + m(z)))
    outs.append(lab + " " + m(z))
h = eqs(("p(x)", "0"), ("ax", "0")) + tp("पक्षांतर: a ≠ 0 दाएँ पक्ष में भाग बनकर जाता है।") + eqs(("x", "\\dfrac{0}{a}")) + lines("x", "0")
s += part("(vi) " + m("p(x) = ax,\\ a \\neq 0"), h + ans("शून्यक 0"))
h = eqs(("p(x)", "0"), ("cx + d", "0")) + tp("पक्षांतर: +d दाएँ पक्ष में −d हो जाता है।") + eqs(("cx", "-d")) + tp("पक्षांतर: c ≠ 0 दाएँ पक्ष में भाग बनकर जाता है।") + eqs(("x", "-\\dfrac{d}{c}"))
s += part("(vii) " + m("p(x) = cx + d,\\ c \\neq 0,\\ c, d") + " वास्तविक संख्याएँ", h + ans("शून्यक " + m("-\\dfrac{d}{c}")))
s += ans(" ".join(outs) + " (vi) 0 (vii) " + m("-\\dfrac{d}{c}"))
E2.append((qt("निम्नलिखित स्थितियों में से प्रत्येक स्थिति में बहुपद का शून्यक ज्ञात कीजिए: (i) " + m("p(x) = x + 5") + " (ii) " + m("p(x) = x - 5") + " (iii) " + m("p(x) = 2x + 5")
              + " (iv) " + m("p(x) = 3x - 2") + " (v) " + m("p(x) = 3x") + " (vi) " + m("p(x) = ax,\\ a \\neq 0") + " (vii) " + m("p(x) = cx + d,\\ c \\neq 0") + ", c, d वास्तविक संख्याएँ हैं।"), s))
assert len(E2) == 4

# =====================================================================
# Exercise 2.3 (गुणनखंडन)
# =====================================================================
E3 = []
FT = formula("गुणनखंड प्रमेय", m("(x + 1)") + " बहुपद " + m("p(x)") + " का गुणनखंड है, यदि " + m("p(-1) = 0") + " हो। (क्योंकि " + m("x + 1 = 0 \\Rightarrow x = -1") + ")")
s = FT
outs = []
for lab, cs in (("(i)", [1, 1, 1, 1]), ("(ii)", [1, 1, 1, 1, 1]), ("(iii)", [1, 3, 3, 1, 1])):
    n = len(cs) - 1
    T = [(c, n - i) for i, c in enumerate(cs)]
    st, val = subst("p", T, -1)
    verdict = "है" if val == 0 else "नहीं है"
    s += part(lab + " " + m(poly(cs)), st + ans(m(f"p(-1) = {num(val)}" + ("" if val == 0 else " \\neq 0")) + ", अतः " + m("(x + 1)") + f" गुणनखंड <b>{verdict}</b>।"))
    outs.append(f"{lab} {verdict}")
b_ = lines("p(-1)", "(-1)^3 - (-1)^2 - (2 + \\sqrt{2})(-1) + \\sqrt{2}", "-1 - 1 - (2 + \\sqrt{2})(-1) + \\sqrt{2}")
b_ += p("कोष्ठक का गुणा, हर पद से अलग-अलग:")
b_ += lines("-(2 + \\sqrt{2})(-1)", "-[2 \\times (-1) + \\sqrt{2} \\times (-1)]", "-[-2 - \\sqrt{2}]", "2 + \\sqrt{2}")
b_ += lines("p(-1)", "-1 - 1 + 2 + \\sqrt{2} + \\sqrt{2}", "-2 + 2 + 2\\sqrt{2}", "0 + 2\\sqrt{2}", "2\\sqrt{2}")
s += part("(iv) " + m("x^3 - x^2 - (2 + \\sqrt{2})x + \\sqrt{2}"), b_ + ans(m("p(-1) = 2\\sqrt{2} \\neq 0") + ", अतः " + m("(x + 1)") + " गुणनखंड <b>नहीं है</b>।"))
outs.append("(iv) नहीं है")
s += ans(" ".join(o.replace("है", "गुणनखंड है").replace("नहीं गुणनखंड है", "गुणनखंड नहीं है") for o in outs))
E3.append((qt("बताइए कि निम्नलिखित बहुपदों में से किस बहुपद का एक गुणनखंड " + m("x + 1") + " है: (i) " + m("x^3 + x^2 + x + 1") + " (ii) " + m("x^4 + x^3 + x^2 + x + 1")
              + " (iii) " + m("x^4 + 3x^3 + 3x^2 + x + 1") + " (iv) " + m("x^3 - x^2 - (2 + \\sqrt{2})x + \\sqrt{2}")), s))

s = formula("गुणनखंड प्रमेय", m("g(x) = x - a") + " बहुपद " + m("p(x)") + " का गुणनखंड है, यदि " + m("p(a) = 0") + "।")
outs = []
for lab, cs, gtx, a in (("(i)", [2, 1, -2, -1], "x + 1", -1), ("(ii)", [1, 3, 3, 1], "x + 2", -2), ("(iii)", [1, -4, 1, 6], "x - 3", 3)):
    T = [(c, 3 - i) for i, c in enumerate(cs)]
    b_ = eqs(("g(x)", "0"), (gtx, "0"))
    b_ += tp("पक्षांतर: अचर पद दाएँ पक्ष में जाकर चिह्न बदल लेता है (+ से −, − से +)।")
    b_ += eqs(("x", str(a)))
    st, val = subst("p", T, a)
    b_ += st
    v = "है" if val == 0 else "नहीं है"
    b_ += ans(m(f"p({a}) = {val}" + ("" if val == 0 else " \\neq 0")) + ", अतः " + m("g(x)") + f" गुणनखंड <b>{v}</b>।")
    s += part(lab + " " + m(f"p(x) = {poly(cs)},\\ g(x) = {gtx}"), b_)
    outs.append(f"{lab} {'हाँ' if val == 0 else 'नहीं'}")
s += ans(" ".join(outs))
E3.append((qt("गुणनखंड प्रमेय लागू करके बताइए कि निम्नलिखित स्थितियों में से प्रत्येक स्थिति में " + m("g(x)") + ", " + m("p(x)") + " का एक गुणनखंड है या नहीं: "
              "(i) " + m("p(x) = 2x^3 + x^2 - 2x - 1,\\ g(x) = x + 1") + " (ii) " + m("p(x) = x^3 + 3x^2 + 3x + 1,\\ g(x) = x + 2") + " (iii) " + m("p(x) = x^3 - 4x^2 + x + 6,\\ g(x) = x - 3")), s))

s = formula("गुणनखंड प्रमेय", m("(x - 1)") + " गुणनखंड है, तो " + m("p(1) = 0") + " होगा।")
b_ = lines("p(1)", "(1)^2 + 1 + k", "1 + 1 + k", "2 + k") + eqs(("2 + k", "0")) + tp("पक्षांतर: +2 दाएँ पक्ष में −2 हो जाता है।") + eqs(("k", "-2"))
s += part("(i) " + m("p(x) = x^2 + x + k"), b_ + ans(m("k = -2")))
b_ = lines("p(1)", "2(1)^2 + k(1) + \\sqrt{2}", "2 \\times 1 + k + \\sqrt{2}", "2 + k + \\sqrt{2}") + eqs(("2 + k + \\sqrt{2}", "0"))
b_ += tp("पक्षांतर: +2 और +√2 दाएँ पक्ष में −2 और −√2 हो जाते हैं।") + eqs(("k", "-2 - \\sqrt{2}")) + lines("k", "-(2 + \\sqrt{2})")
s += part("(ii) " + m("p(x) = 2x^2 + kx + \\sqrt{2}"), b_ + ans(m("k = -(2 + \\sqrt{2})")))
b_ = lines("p(1)", "k(1)^2 - \\sqrt{2}(1) + 1", "k \\times 1 - \\sqrt{2} + 1", "k - \\sqrt{2} + 1") + eqs(("k - \\sqrt{2} + 1", "0"))
b_ += tp("पक्षांतर: −√2 दाएँ पक्ष में +√2 और +1 दाएँ पक्ष में −1 हो जाता है।") + eqs(("k", "\\sqrt{2} - 1"))
s += part("(iii) " + m("p(x) = kx^2 - \\sqrt{2}x + 1"), b_ + ans(m("k = \\sqrt{2} - 1")))
b_ = lines("p(1)", "k(1)^2 - 3(1) + k", "k \\times 1 - 3 + k", "k - 3 + k", "2k - 3") + eqs(("2k - 3", "0"))
b_ += tp("पक्षांतर: −3 दाएँ पक्ष में +3 हो जाता है।") + eqs(("2k", "3")) + tp("पक्षांतर: k का गुणक 2 दाएँ पक्ष में भाग बनकर जाता है।") + eqs(("k", "\\dfrac{3}{2}"))
s += part("(iv) " + m("p(x) = kx^2 - 3x + k"), b_ + ans(m("k = \\dfrac{3}{2}")))
s += ans("(i) " + m("k = -2") + " (ii) " + m("k = -(2 + \\sqrt{2})") + " (iii) " + m("k = \\sqrt{2} - 1") + " (iv) " + m("k = \\dfrac{3}{2}"))
E3.append((qt("k का मान ज्ञात कीजिए जबकि निम्नलिखित स्थितियों में से प्रत्येक स्थिति में " + m("(x - 1)") + ", " + m("p(x)") + " का एक गुणनखंड हो: "
              "(i) " + m("p(x) = x^2 + x + k") + " (ii) " + m("p(x) = 2x^2 + kx + \\sqrt{2}") + " (iii) " + m("p(x) = kx^2 - \\sqrt{2}x + 1") + " (iv) " + m("p(x) = kx^2 - 3x + k")), s))

s = ""
outs = []
for lab, (a, b, c) in (("(i)", (12, -7, 1)), ("(ii)", (2, 7, 3)), ("(iii)", (6, 5, -6)), ("(iv)", (3, -1, -4))):
    h, f1, f2 = split_quad(a, b, c)
    r = fac_tex(f1) + fac_tex(f2)
    # check by multiplying back, term by term
    p1, q1 = f1
    p2, q2 = f2
    h += p("<b>जाँच</b> (हर पद से अलग-अलग गुणा):")
    h += lines(r, f"{poly([p1, 0])}{fac_tex(f2)} {'+' if q1 > 0 else '-'} {abs(q1)}{fac_tex(f2)}",
               f"{poly([p1 * p2, p1 * q2, 0])} {'+' if q1 * p2 > 0 else '-'} {poly([abs(q1 * p2), 0])} {'+' if q1 * q2 > 0 else '-'} {abs(q1 * q2)}", poly([a, b, c]))
    h += ans(m(r))
    s += part(lab + " " + m(poly([a, b, c])), h)
    outs.append(lab + " " + m(r))
s += ans(" ".join(outs))
E3.append((qt("गुणनखंड ज्ञात कीजिए: (i) " + m("12x^2 - 7x + 1") + " (ii) " + m("2x^2 + 7x + 3") + " (iii) " + m("6x^2 + 5x - 6") + " (iv) " + m("3x^2 - x - 4")), s))

s = ""
outs = []
for lab, cs, cands, vs in (("(i)", [1, -2, -1, 2], [1], "x"), ("(ii)", [1, -3, -9, -5], [1, -1], "x"), ("(iii)", [1, 13, 32, 20], [1, -1], "x"), ("(iv)", [2, 1, -2, -1], [1], "y")):
    h, r = cubic_fact("p", cs, cands, vs)
    if lab == "(ii)":
        h += lines(r, "(x + 1)^2(x - 5)")
        r = "(x + 1)^2(x - 5)"
    h += ans(m(r))
    s += part(lab + " " + m(poly(cs, vs)), h)
    outs.append(lab + " " + m(r))
s += ans(" ".join(outs))
E3.append((qt("गुणनखंड ज्ञात कीजिए: (i) " + m("x^3 - 2x^2 - x + 2") + " (ii) " + m("x^3 - 3x^2 - 9x - 5") + " (iii) " + m("x^3 + 13x^2 + 32x + 20") + " (iv) " + m("2y^3 + y^2 - 2y - 1")), s))
assert len(E3) == 5

# =====================================================================
# Exercise 2.4 (बीजीय सर्वसमिकाएँ)
# =====================================================================
class Mo:
    """Monomial: c (Fraction) × (√2)^s × variables."""
    def __init__(self, c, v=None, s=0):
        self.c, self.s, self.v = F(c), s, dict(v or {})

    def __mul__(self, o):
        if not isinstance(o, Mo):
            o = Mo(o)
        v = dict(self.v)
        for k, e_ in o.v.items():
            v[k] = v.get(k, 0) + e_
        c, s = self.c * o.c, self.s + o.s
        if s == 2:
            c, s = c * 2, 0
        return Mo(c, v, s)
    __rmul__ = __mul__

    def __neg__(self):
        return Mo(-self.c, self.v, self.s)

    def key(self):
        return (tuple(sorted(self.v.items())), self.s)

    def vt(self):
        return "".join(k if e_ == 1 else f"{k}^{{{e_}}}" for k, e_ in sorted(self.v.items()))

    def ct(self):
        """signed coefficient alone"""
        r = abs(self.c)
        body = (num(r) if (r != 1 or not self.s) else "") + ("\\sqrt{2}" if self.s else "")
        return ("-" if self.c < 0 else "") + body

    def tex(self):
        r = abs(self.c)
        vt = self.vt()
        if self.s:
            body = ("" if r == 1 else num(r)) + "\\sqrt{2}" + vt
        else:
            body = ("" if (r == 1 and vt) else num(r)) + vt
        return ("-" if self.c < 0 else "") + body


def X(v, c=1, s=0):
    return Mo(c, {v: 1}, s)


def P(t):
    """bracket a TeX piece when it starts with a minus"""
    return f"\\left({t}\\right)" if (t.startswith("-") or "dfrac" in t) else t


def B(m_):
    return f"\\left({m_.tex()}\\right)"


def sumt(ms):
    out = ""
    for m_ in ms:
        t = m_.tex()
        if not out:
            out = t
        else:
            out += (" - " + t[1:]) if t.startswith("-") else (" + " + t)
    return out


def sq_rows(A):
    R = A * A
    rows = []
    if A.vt() and (A.c != 1 or A.s):
        rows.append(f"{P(A.ct())}^2 \\times ({A.vt()})^2")
    elif not A.vt() and (A.c.denominator != 1 or A.s or A.c < 0):
        rows.append(f"{P(A.ct())} \\times {P(A.ct())}")
    rows.append(R.tex())
    return lines(f"{B(A)}^2", *rows), R


def cube_rows(A):
    R = A * A * A
    rows = []
    if A.vt():
        if A.c != 1 or A.s:
            rows.append(f"{P(A.ct())}^3 \\times ({A.vt()})^3")
            ct = P(A.ct())
            rows.append(f"{ct} \\times {ct} \\times {ct} \\times {A.vt()}^{{3}}" if len(A.v) == 1 and list(A.v.values())[0] == 1 else rows[-1])
            if rows[-1] == rows[-2]:
                rows.pop()
    else:
        ct = P(A.ct())
        if A.c != 1:
            rows.append(f"{ct} \\times {ct} \\times {ct}")
    rows.append(R.tex())
    return lines(f"{B(A)}^3", *rows), R


def prod_rows(k, Ms, head=None):
    """k × M1 × M2 ... with the coefficients first, then the result."""
    R = Mo(k)
    for M_ in Ms:
        R = R * M_
    head = head or (f"{k}" + "".join(B(M_) for M_ in Ms))
    cs = " \\times ".join([str(k)] + [P(M_.ct()) for M_ in Ms if M_.ct() not in ("1",)])
    vs = " \\times ".join(M_.vt() for M_ in Ms if M_.vt())
    rows = [cs + (f" \\times {vs}" if vs else "")]
    rows.append(R.tex())
    return lines(head, *rows), R


def split_as(expr, Ms):
    return lines(expr, " + ".join(B(M_) for M_ in Ms))


SQ3 = formula("सर्वसमिका IV", m("(a + b + c)^2 = a^2 + b^2 + c^2 + 2ab + 2bc + 2ca"))


def sq3(expr, A, B_, C):
    h = SQ3
    h += split_as(expr, [A, B_, C])
    h += eqs(("a", A.tex()), ("b", B_.tex()), ("c", C.tex()))
    h += p("सूत्र में मान रखने पर:")
    h += lines(f"\\left({expr}\\right)^2", f"{B(A)}^2 + {B(B_)}^2 + {B(C)}^2 + 2{B(A)}{B(B_)} + 2{B(B_)}{B(C)} + 2{B(C)}{B(A)}")
    h += p("अब हर पद को अलग-अलग हल करते हैं:")
    res = []
    for M_ in (A, B_, C):
        t, R = sq_rows(M_)
        h += t
        res.append(R)
    for M1, M2 in ((A, B_), (B_, C), (C, A)):
        t, R = prod_rows(2, [M1, M2])
        h += t
        res.append(R)
    out = sumt(res)
    h += p("सभी पद जोड़ने पर:")
    h += lines(f"\\left({expr}\\right)^2", out)
    return h, out


def cube(expr, A, B_, sign):
    s = "+" if sign > 0 else "-"
    nm = "VI" if sign > 0 else "VII"
    h = formula(f"सर्वसमिका {nm}", m(f"(a {s} b)^3 = a^3 {s} 3a^2b + 3ab^2 {s} b^3"))
    h += lines(expr, f"{B(A)} {s} {B(B_)}")
    h += eqs(("a", A.tex()), ("b", B_.tex()))
    h += p("सूत्र में मान रखने पर:")
    h += lines(f"\\left({expr}\\right)^3", f"{B(A)}^3 {s} 3{B(A)}^2{B(B_)} + 3{B(A)}{B(B_)}^2 {s} {B(B_)}^3")
    h += p("अब हर पद को अलग-अलग हल करते हैं:")
    t, a3 = cube_rows(A)
    h += t
    t, a2 = sq_rows(A)
    h += t
    t, b2 = sq_rows(B_)
    h += t
    t, m1 = prod_rows(3, [a2, B_], f"3{B(A)}^2{B(B_)}")
    h += t
    t, m2 = prod_rows(3, [A, b2], f"3{B(A)}{B(B_)}^2")
    h += t
    t, b3 = cube_rows(B_)
    h += t
    terms = [a3, m1 if sign > 0 else -m1, m2, b3 if sign > 0 else -b3]
    out = sumt(terms)
    h += p("सभी पद रखने पर:")
    h += lines(f"\\left({expr}\\right)^3", out)
    return h, out


def numcube(n, a, b, sign):
    s = "+" if sign > 0 else "-"
    h = formula(f"सर्वसमिका {'VI' if sign > 0 else 'VII'}", m(f"(a {s} b)^3 = a^3 {s} 3a^2b + 3ab^2 {s} b^3"))
    h += lines(f"{n}", f"{a} {s} {b}")
    h += eqs(("a", str(a)), ("b", str(b)))
    vals = [a ** 3, sign * 3 * a * a * b, 3 * a * b * b, sign * b ** 3]
    h += lines(f"{n}^3", f"({a} {s} {b})^3", f"({a})^3 {s} 3 \\times ({a})^2 \\times {b} + 3 \\times {a} \\times ({b})^2 {s} ({b})^3",
               f"{a ** 3} {s} 3 \\times {a * a} \\times {b} + 3 \\times {a} \\times {b * b} {s} {b ** 3}",
               chain(vals))
    v = vals[:]
    rows = []
    while len(v) > 1:
        v = [v[0] + v[1]] + v[2:]
        rows.append(chain(v))
    h += lines("", *rows) if False else lines(f"{n}^3", *rows)
    assert v[0] == n ** 3
    return h, v[0]


E4 = []
# Q1
s = formula("सर्वसमिकाएँ", "", [m("(x + a)(x + b) = x^2 + (a + b)x + ab") + " &nbsp;(सर्वसमिका IV)", m("(a + b)(a - b) = a^2 - b^2") + " &nbsp;(सर्वसमिका III)"])
s += part("(i) " + m("(x + 4)(x + 10)"), p("सूत्र (1) में " + m("a = 4,\\ b = 10") + ":")
          + lines("(x + 4)(x + 10)", "x^2 + (4 + 10)x + 4 \\times 10", "x^2 + 14x + 40") + ans(m("x^2 + 14x + 40")))
s += part("(ii) " + m("(x + 8)(x - 10)"), lines("(x + 8)(x - 10)", "(x + 8)(x + (-10))") + p("सूत्र (1) में " + m("a = 8,\\ b = -10") + ":")
          + lines("(x + 8)(x - 10)", "x^2 + (8 + (-10))x + 8 \\times (-10)", "x^2 + (8 - 10)x + (-80)", "x^2 + (-2)x - 80", "x^2 - 2x - 80") + ans(m("x^2 - 2x - 80")))
s += part("(iii) " + m("(3x + 4)(3x - 5)"), p("यहाँ " + m("3x") + " को सूत्र का " + m("x") + " मानते हैं, " + m("a = 4,\\ b = -5") + ":")
          + lines("(3x + 4)(3x - 5)", "(3x)^2 + (4 + (-5))(3x) + 4 \\times (-5)", "(3x)^2 + (4 - 5)(3x) - 20", "3^2 \\times x^2 + (-1)(3x) - 20", "9x^2 - 3x - 20") + ans(m("9x^2 - 3x - 20")))
s += part("(iv) " + m("\\left(y^2 + \\dfrac{3}{2}\\right)\\left(y^2 - \\dfrac{3}{2}\\right)"), p("सूत्र (2) में " + m("a = y^2,\\ b = \\dfrac{3}{2}") + ":")
          + lines("\\left(y^2 + \\dfrac{3}{2}\\right)\\left(y^2 - \\dfrac{3}{2}\\right)", "(y^2)^2 - \\left(\\dfrac{3}{2}\\right)^2", "y^{2 \\times 2} - \\dfrac{3^2}{2^2}", "y^4 - \\dfrac{9}{4}") + ans(m("y^4 - \\dfrac{9}{4}")))
s += part("(v) " + m("(3 - 2x)(3 + 2x)"), lines("(3 - 2x)(3 + 2x)", "(3 + 2x)(3 - 2x)") + p("सूत्र (2) में " + m("a = 3,\\ b = 2x") + ":")
          + lines("(3 + 2x)(3 - 2x)", "3^2 - (2x)^2", "9 - 2^2 \\times x^2", "9 - 4x^2") + ans(m("9 - 4x^2")))
s += ans("(i) " + m("x^2 + 14x + 40") + " (ii) " + m("x^2 - 2x - 80") + " (iii) " + m("9x^2 - 3x - 20") + " (iv) " + m("y^4 - \\dfrac{9}{4}") + " (v) " + m("9 - 4x^2"))
E4.append((qt("उपयुक्त सर्वसमिकाओं को प्रयोग करके निम्नलिखित गुणनफल ज्ञात कीजिए: (i) " + m("(x + 4)(x + 10)") + " (ii) " + m("(x + 8)(x - 10)") + " (iii) " + m("(3x + 4)(3x - 5)")
              + " (iv) " + m("\\left(y^2 + \\dfrac{3}{2}\\right)\\left(y^2 - \\dfrac{3}{2}\\right)") + " (v) " + m("(3 - 2x)(3 + 2x)")), s))

# Q2
s = formula("सर्वसमिकाएँ", "", [m("(x + a)(x + b) = x^2 + (a + b)x + ab"), m("(a + b)(a - b) = a^2 - b^2")])
s += part("(i) " + m("103 \\times 107"), lines("103 \\times 107", "(100 + 3)(100 + 7)") + p("सूत्र (1) में " + m("x = 100,\\ a = 3,\\ b = 7") + ":")
          + lines("103 \\times 107", "100^2 + (3 + 7) \\times 100 + 3 \\times 7", "10000 + 10 \\times 100 + 21", "10000 + 1000 + 21", "11000 + 21", "11021") + ans(m("11021")))
s += part("(ii) " + m("95 \\times 96"), lines("95 \\times 96", "(100 - 5)(100 - 4)", "(100 + (-5))(100 + (-4))") + p("सूत्र (1) में " + m("x = 100,\\ a = -5,\\ b = -4") + ":")
          + lines("95 \\times 96", "100^2 + ((-5) + (-4)) \\times 100 + (-5) \\times (-4)", "10000 + (-9) \\times 100 + 20", "10000 - 900 + 20", "9100 + 20", "9120") + ans(m("9120")))
s += part("(iii) " + m("104 \\times 96"), lines("104 \\times 96", "(100 + 4)(100 - 4)") + p("सूत्र (2) में " + m("a = 100,\\ b = 4") + ":")
          + lines("104 \\times 96", "100^2 - 4^2", "10000 - 16", "9984") + ans(m("9984")))
s += ans("(i) 11021 (ii) 9120 (iii) 9984")
E4.append((qt("सीधे गुणा किए बिना निम्नलिखित गुणनफलों के मान ज्ञात कीजिए: (i) " + m("103 \\times 107") + " (ii) " + m("95 \\times 96") + " (iii) " + m("104 \\times 96")), s))

# Q3
s = formula("सर्वसमिकाएँ", "", [m("a^2 + 2ab + b^2 = (a + b)^2"), m("a^2 - 2ab + b^2 = (a - b)^2"), m("a^2 - b^2 = (a + b)(a - b)")])
s += part("(i) " + m("9x^2 + 6xy + y^2"), lines("9x^2", "3^2 \\times x^2", "(3x)^2") + lines("6xy", "2 \\times 3x \\times y", "2(3x)(y)")
          + lines("9x^2 + 6xy + y^2", "(3x)^2 + 2(3x)(y) + (y)^2") + p("सूत्र (1) में " + m("a = 3x,\\ b = y") + ":") + lines("9x^2 + 6xy + y^2", "(3x + y)^2", "(3x + y)(3x + y)") + ans(m("(3x + y)(3x + y)")))
s += part("(ii) " + m("4y^2 - 4y + 1"), lines("4y^2", "2^2 \\times y^2", "(2y)^2") + lines("4y", "2 \\times 2y \\times 1", "2(2y)(1)") + lines("1", "1^2")
          + lines("4y^2 - 4y + 1", "(2y)^2 - 2(2y)(1) + (1)^2") + p("सूत्र (2) में " + m("a = 2y,\\ b = 1") + ":") + lines("4y^2 - 4y + 1", "(2y - 1)^2", "(2y - 1)(2y - 1)") + ans(m("(2y - 1)(2y - 1)")))
s += part("(iii) " + m("x^2 - \\dfrac{y^2}{100}"), lines("\\dfrac{y^2}{100}", "\\dfrac{y^2}{10^2}", "\\left(\\dfrac{y}{10}\\right)^2") + lines("x^2 - \\dfrac{y^2}{100}", "(x)^2 - \\left(\\dfrac{y}{10}\\right)^2")
          + p("सूत्र (3) में " + m("a = x,\\ b = \\dfrac{y}{10}") + ":") + lines("x^2 - \\dfrac{y^2}{100}", "\\left(x + \\dfrac{y}{10}\\right)\\left(x - \\dfrac{y}{10}\\right)") + ans(m("\\left(x + \\dfrac{y}{10}\\right)\\left(x - \\dfrac{y}{10}\\right)")))
s += ans("(i) " + m("(3x + y)(3x + y)") + " (ii) " + m("(2y - 1)(2y - 1)") + " (iii) " + m("\\left(x + \\dfrac{y}{10}\\right)\\left(x - \\dfrac{y}{10}\\right)"))
E4.append((qt("उपयुक्त सर्वसमिकाएँ प्रयोग करके निम्नलिखित का गुणनखंडन कीजिए: (i) " + m("9x^2 + 6xy + y^2") + " (ii) " + m("4y^2 - 4y + 1") + " (iii) " + m("x^2 - \\dfrac{y^2}{100}")), s))

# Q4
x_, y_, z_, a_, b_ = (lambda c=1: X("x", c)), (lambda c=1: X("y", c)), (lambda c=1: X("z", c)), (lambda c=1: X("a", c)), (lambda c=1: X("b", c))
Q4 = [("(i)", "x + 2y + 4z", x_(), y_(2), z_(4)), ("(ii)", "2x - y + z", x_(2), y_(-1), z_()), ("(iii)", "-2x + 3y + 2z", x_(-2), y_(3), z_(2)),
      ("(iv)", "3a - 7b - c", a_(3), b_(-7), X("c", -1)), ("(v)", "-2x + 5y - 3z", x_(-2), y_(5), z_(-3)),
      ("(vi)", "\\dfrac{1}{4}a - \\dfrac{1}{2}b + 1", a_(F(1, 4)), b_(F(-1, 2)), Mo(1))]
s = ""
outs = []
for lab, ex, A, B_, C in Q4:
    h, out = sq3(ex, A, B_, C)
    s += part(lab + " " + m(f"\\left({ex}\\right)^2"), h + ans(m(out)))
    outs.append(lab + " " + m(out))
s += ans(" ".join(outs))
E4.append((qt("उपयुक्त सर्वसमिकाओं का प्रयोग करके निम्नलिखित में से प्रत्येक का प्रसार कीजिए: " + " ".join(f"{lab} " + m(f"\\left({ex}\\right)^2") for lab, ex, *_ in Q4)), s))


# Q5
def sq3fact(given, sq_parts, cross, A, B_, C, why_sign):
    h = SQ3
    for t_, rows in sq_parts:
        h += lines(t_, *rows)
    h += p("बीच वाले पदों (" + m("2ab,\\ 2bc,\\ 2ca") + ") के चिह्न देखकर a, b, c के चिह्न तय करते हैं:")
    h += why(why_sign)
    h += eqs(("a", A.tex()), ("b", B_.tex()), ("c", C.tex()))
    h += p("जाँच (हर बीच वाला पद अलग-अलग):")
    for M1, M2 in ((A, B_), (B_, C), (C, A)):
        t, R = prod_rows(2, [M1, M2])
        h += t
    res = [A * A, B_ * B_, C * C, 2 * A * B_, 2 * B_ * C, 2 * C * A]
    h += p("माना " + m("E = " + given) + "। तब")
    h += lines("E", f"{B(A)}^2 + {B(B_)}^2 + {B(C)}^2 + 2{B(A)}{B(B_)} + 2{B(B_)}{B(C)} + 2{B(C)}{B(A)}", f"\\left({sumt([A, B_, C])}\\right)^2")
    return h, f"\\left({sumt([A, B_, C])}\\right)^2", res


s = ""
g1 = "4x^2 + 9y^2 + 16z^2 + 12xy - 24yz - 16xz"
h, r1, res = sq3fact(g1, [("4x^2", ["2^2 \\times x^2", "(2x)^2"]), ("9y^2", ["3^2 \\times y^2", "(3y)^2"]), ("16z^2", ["4^2 \\times z^2", "(4z)^2"])], None,
                     x_(2), y_(3), z_(-4), m("+12xy") + " धनात्मक है, अतः " + m("2x") + " और " + m("3y") + " का चिह्न एक-सा; " + m("-24yz") + " और " + m("-16xz") + " ऋणात्मक हैं, अतः " + m("4z") + " का चिह्न उलटा, यानी " + m("c = -4z") + "।")
assert [t.tex() for t in res] == ["4x^{2}", "9y^{2}", "16z^{2}", "12xy", "-24yz", "-16xz"], [t.tex() for t in res]
s += part("(i) " + m(g1), h + ans(m(r1) + " = " + m("(2x + 3y - 4z)(2x + 3y - 4z)")))
g2 = "2x^2 + y^2 + 8z^2 - 2\\sqrt{2}xy + 4\\sqrt{2}yz - 8xz"
h, r2, res = sq3fact(g2, [("2x^2", ["(\\sqrt{2})^2 \\times x^2", "(\\sqrt{2}x)^2"]), ("y^2", ["(y)^2"]), ("8z^2", ["4 \\times 2 \\times z^2", "2^2 \\times (\\sqrt{2})^2 \\times z^2", "(2\\sqrt{2}z)^2"])], None,
                     X("x", -1, 1), y_(), X("z", 2, 1), m("+4\\sqrt{2}yz") + " धनात्मक है, अतः " + m("y") + " और " + m("2\\sqrt{2}z") + " का चिह्न एक-सा; " + m("-2\\sqrt{2}xy") + " और " + m("-8xz") + " ऋणात्मक हैं, अतः " + m("\\sqrt{2}x") + " का चिह्न उलटा, यानी " + m("a = -\\sqrt{2}x") + "।")
assert [t.tex() for t in res] == ["2x^{2}", "y^{2}", "8z^{2}", "-2\\sqrt{2}xy", "4\\sqrt{2}yz", "-8xz"], [t.tex() for t in res]
s += part("(ii) " + m(g2), h + ans(m(r2) + " = " + m("(-\\sqrt{2}x + y + 2\\sqrt{2}z)(-\\sqrt{2}x + y + 2\\sqrt{2}z)")))
s += ans("(i) " + m("(2x + 3y - 4z)(2x + 3y - 4z)") + " (ii) " + m("(-\\sqrt{2}x + y + 2\\sqrt{2}z)(-\\sqrt{2}x + y + 2\\sqrt{2}z)"))
E4.append((qt("गुणनखंडन कीजिए: (i) " + m(g1) + " (ii) " + m(g2)), s))

# Q6
Q6 = [("(i)", "2x + 1", x_(2), Mo(1), 1), ("(ii)", "2a - 3b", a_(2), b_(3), -1), ("(iii)", "\\dfrac{3}{2}x + 1", x_(F(3, 2)), Mo(1), 1), ("(iv)", "x - \\dfrac{2}{3}y", x_(), y_(F(2, 3)), -1)]
s = ""
outs = []
for lab, ex, A, B_, sg in Q6:
    h, out = cube(ex, A, B_, sg)
    s += part(lab + " " + m(f"\\left({ex}\\right)^3"), h + ans(m(out)))
    outs.append(lab + " " + m(out))
s += ans(" ".join(outs))
E4.append((qt("निम्नलिखित घनों में से प्रत्येक का प्रसारित रूप लिखिए: " + " ".join(f"{lab} " + m(f"\\left({ex}\\right)^3") for lab, ex, *_ in Q6)), s))

# Q7
s = ""
outs = []
for lab, n, a, b, sg in (("(i)", 99, 100, 1, -1), ("(ii)", 102, 100, 2, 1), ("(iii)", 998, 1000, 2, -1)):
    h, v = numcube(n, a, b, sg)
    s += part(lab + " " + m(f"{n}^3"), h + ans(m(str(v))))
    outs.append(f"{lab} {v}")
s += ans(" ".join(outs))
E4.append((qt("उपयुक्त सर्वसमिकाओं को प्रयोग करके निम्नलिखित के मान ज्ञात कीजिए: (i) " + m("(99)^3") + " (ii) " + m("(102)^3") + " (iii) " + m("(998)^3")), s))


# Q8
def cubefact(given, A, B_, sg, cube_split):
    s_ = "+" if sg > 0 else "-"
    h = formula(f"सर्वसमिका {'VI' if sg > 0 else 'VII'}", m(f"a^3 {s_} 3a^2b + 3ab^2 {s_} b^3 = (a {s_} b)^3"))
    h += p("पहले घन वाले पद पहचानते हैं:")
    for t_, rows in cube_split:
        h += lines(t_, *rows)
    h += eqs(("a", A.tex()), ("b", B_.tex()))
    h += p("अब बीच वाले पद जाँचते हैं:")
    t, a2 = sq_rows(A)
    h += t
    t, b2 = sq_rows(B_)
    h += t
    t, m1 = prod_rows(3, [a2, B_], f"3{B(A)}^2{B(B_)}")
    h += t
    t, m2 = prod_rows(3, [A, b2], f"3{B(A)}{B(B_)}^2")
    h += t
    h += p("दोनों पद दिए गए व्यंजक में हैं। पदों को सूत्र के क्रम में लिखने पर:")
    out = f"\\left({A.tex()} {s_} {B_.tex()}\\right)^3"
    h += p("माना " + m("E = " + given) + "। तब")
    h += lines("E", f"{B(A)}^3 {s_} 3{B(A)}^2{B(B_)} + 3{B(A)}{B(B_)}^2 {s_} {B(B_)}^3", out)
    return h, out, (m1.tex(), m2.tex())


Q8 = [("(i)", "8a^3 + b^3 + 12a^2b + 6ab^2", a_(2), b_(), 1, [("8a^3", ["2 \\times 2 \\times 2 \\times a^3", "2^3 \\times a^3", "(2a)^3"]), ("b^3", ["(b)^3"])], ("12a^{2}b", "6ab^{2}")),
      ("(ii)", "8a^3 - b^3 - 12a^2b + 6ab^2", a_(2), b_(), -1, [("8a^3", ["2 \\times 2 \\times 2 \\times a^3", "(2a)^3"]), ("b^3", ["(b)^3"])], ("12a^{2}b", "6ab^{2}")),
      ("(iii)", "27 - 125a^3 - 135a + 225a^2", Mo(3), a_(5), -1, [("27", ["3 \\times 3 \\times 3", "3^3"]), ("125a^3", ["5 \\times 5 \\times 5 \\times a^3", "(5a)^3"])], ("135a", "225a^{2}")),
      ("(iv)", "64a^3 - 27b^3 - 144a^2b + 108ab^2", a_(4), b_(3), -1, [("64a^3", ["4 \\times 4 \\times 4 \\times a^3", "(4a)^3"]), ("27b^3", ["3 \\times 3 \\times 3 \\times b^3", "(3b)^3"])], ("144a^{2}b", "108ab^{2}")),
      ("(v)", "27p^3 - \\dfrac{1}{216} - \\dfrac{9}{2}p^2 + \\dfrac{1}{4}p", X("p", 3), Mo(F(1, 6)), -1,
       [("27p^3", ["3 \\times 3 \\times 3 \\times p^3", "(3p)^3"]), ("\\dfrac{1}{216}", ["\\dfrac{1}{6 \\times 6 \\times 6}", "\\left(\\dfrac{1}{6}\\right)^3"])], ("\\dfrac{9}{2}p^{2}", "\\dfrac{1}{4}p"))]
s = ""
outs = []
for lab, g, A, B_, sg, cs_, expect in Q8:
    h, out, got = cubefact(g, A, B_, sg, cs_)
    assert got == expect, (lab, got)
    long_ = f"\\left({A.tex()} {'+' if sg > 0 else '-'} {B_.tex()}\\right)" * 3
    s += part(lab + " " + m(g), h + ans(m(out) + " = " + m(long_)))
    outs.append(lab + " " + m(long_))
s += ans(" ".join(outs))
E4.append((qt("गुणनखंडन कीजिए: " + " ".join(f"{lab} " + m(g) for lab, g, *_ in Q8)), s))

# Q9
s = part("(i) " + m("x^3 + y^3 = (x + y)(x^2 - xy + y^2)"),
         p("दायाँ पक्ष लेते हैं और पहले कोष्ठक के हर पद से दूसरे कोष्ठक को अलग-अलग गुणा करते हैं:")
         + lines("\\text{RHS}", "(x + y)(x^2 - xy + y^2)", "x(x^2 - xy + y^2) + y(x^2 - xy + y^2)")
         + lines("x(x^2 - xy + y^2)", "x \\times x^2 - x \\times xy + x \\times y^2", "x^3 - x^2y + xy^2")
         + lines("y(x^2 - xy + y^2)", "y \\times x^2 - y \\times xy + y \\times y^2", "x^2y - xy^2 + y^3")
         + lines("\\text{RHS}", "x^3 - x^2y + xy^2 + x^2y - xy^2 + y^3", "x^3 + (-x^2y + x^2y) + (xy^2 - xy^2) + y^3", "x^3 + 0 + 0 + y^3", "x^3 + y^3", "\\text{LHS}")
         + ans("सत्यापित।"))
s += part("(ii) " + m("x^3 - y^3 = (x - y)(x^2 + xy + y^2)"),
          lines("\\text{RHS}", "(x - y)(x^2 + xy + y^2)", "x(x^2 + xy + y^2) - y(x^2 + xy + y^2)")
          + lines("x(x^2 + xy + y^2)", "x \\times x^2 + x \\times xy + x \\times y^2", "x^3 + x^2y + xy^2")
          + lines("y(x^2 + xy + y^2)", "y \\times x^2 + y \\times xy + y \\times y^2", "x^2y + xy^2 + y^3")
          + lines("\\text{RHS}", "x^3 + x^2y + xy^2 - (x^2y + xy^2 + y^3)", "x^3 + x^2y + xy^2 - x^2y - xy^2 - y^3", "x^3 + (x^2y - x^2y) + (xy^2 - xy^2) - y^3", "x^3 + 0 + 0 - y^3", "x^3 - y^3", "\\text{LHS}")
          + ans("सत्यापित।"))
E4.append((qt("सत्यापित कीजिए: (i) " + m("x^3 + y^3 = (x + y)(x^2 - xy + y^2)") + " (ii) " + m("x^3 - y^3 = (x - y)(x^2 + xy + y^2)")), s))

# Q10
s = formula("सर्वसमिकाएँ", "", [m("a^3 + b^3 = (a + b)(a^2 - ab + b^2)"), m("a^3 - b^3 = (a - b)(a^2 + ab + b^2)")])
s += part("(i) " + m("27y^3 + 125z^3"), lines("27y^3", "3 \\times 3 \\times 3 \\times y^3", "(3y)^3") + lines("125z^3", "5 \\times 5 \\times 5 \\times z^3", "(5z)^3")
          + p("सूत्र (1) में " + m("a = 3y,\\ b = 5z") + ":")
          + lines("27y^3 + 125z^3", "(3y)^3 + (5z)^3", "(3y + 5z)[(3y)^2 - (3y)(5z) + (5z)^2]", "(3y + 5z)[3^2 \\times y^2 - 3 \\times 5 \\times y \\times z + 5^2 \\times z^2]", "(3y + 5z)(9y^2 - 15yz + 25z^2)")
          + ans(m("(3y + 5z)(9y^2 - 15yz + 25z^2)")))
s += part("(ii) " + m("64m^3 - 343n^3"), lines("64m^3", "4 \\times 4 \\times 4 \\times m^3", "(4m)^3") + lines("343n^3", "7 \\times 7 \\times 7 \\times n^3", "(7n)^3")
          + p("सूत्र (2) में " + m("a = 4m,\\ b = 7n") + ":")
          + lines("64m^3 - 343n^3", "(4m)^3 - (7n)^3", "(4m - 7n)[(4m)^2 + (4m)(7n) + (7n)^2]", "(4m - 7n)[4^2 \\times m^2 + 4 \\times 7 \\times m \\times n + 7^2 \\times n^2]", "(4m - 7n)(16m^2 + 28mn + 49n^2)")
          + ans(m("(4m - 7n)(16m^2 + 28mn + 49n^2)")))
s += ans("(i) " + m("(3y + 5z)(9y^2 - 15yz + 25z^2)") + " (ii) " + m("(4m - 7n)(16m^2 + 28mn + 49n^2)"))
E4.append((qt("गुणनखंडन कीजिए: (i) " + m("27y^3 + 125z^3") + " (ii) " + m("64m^3 - 343n^3")), s))

# Q11
ID8 = formula("सर्वसमिका VIII", m("a^3 + b^3 + c^3 - 3abc = (a + b + c)(a^2 + b^2 + c^2 - ab - bc - ca)"))
s = ID8
s += lines("27x^3", "3 \\times 3 \\times 3 \\times x^3", "(3x)^3") + lines("9xyz", "3 \\times 3x \\times y \\times z", "3(3x)(y)(z)")
s += lines("27x^3 + y^3 + z^3 - 9xyz", "(3x)^3 + (y)^3 + (z)^3 - 3(3x)(y)(z)")
s += p("सूत्र में " + m("a = 3x,\\ b = y,\\ c = z") + ":")
s += lines("27x^3 + y^3 + z^3 - 9xyz", "(3x + y + z)[(3x)^2 + y^2 + z^2 - (3x)(y) - (y)(z) - (z)(3x)]", "(3x + y + z)(9x^2 + y^2 + z^2 - 3xy - yz - 3zx)")
s += ans(m("(3x + y + z)(9x^2 + y^2 + z^2 - 3xy - yz - 3zx)"))
E4.append(("गुणनखंडन कीजिए: " + m("27x^3 + y^3 + z^3 - 9xyz"), s))

# Q12
s = p("दायाँ पक्ष (RHS) लेते हैं। पहले बड़े कोष्ठक के तीनों वर्ग अलग-अलग:")
s += formula("सर्वसमिका II", m("(a - b)^2 = a^2 - 2ab + b^2"))
s += lines("(x - y)^2", "x^2 - 2xy + y^2") + lines("(y - z)^2", "y^2 - 2yz + z^2") + lines("(z - x)^2", "z^2 - 2zx + x^2")
s += lines("(x - y)^2 + (y - z)^2 + (z - x)^2", "x^2 - 2xy + y^2 + y^2 - 2yz + z^2 + z^2 - 2zx + x^2", "(x^2 + x^2) + (y^2 + y^2) + (z^2 + z^2) - 2xy - 2yz - 2zx",
           "2x^2 + 2y^2 + 2z^2 - 2xy - 2yz - 2zx", "2(x^2 + y^2 + z^2 - xy - yz - zx)")
s += lines("\\text{RHS}", "\\dfrac{1}{2}(x + y + z) \\times 2(x^2 + y^2 + z^2 - xy - yz - zx)", "\\dfrac{2}{2}(x + y + z)(x^2 + y^2 + z^2 - xy - yz - zx)", "(x + y + z)(x^2 + y^2 + z^2 - xy - yz - zx)")
s += p("अब पहले कोष्ठक के हर पद से दूसरे कोष्ठक को अलग-अलग गुणा करते हैं:")
s += lines("x(x^2 + y^2 + z^2 - xy - yz - zx)", "x^3 + xy^2 + xz^2 - x^2y - xyz - x^2z")
s += lines("y(x^2 + y^2 + z^2 - xy - yz - zx)", "x^2y + y^3 + yz^2 - xy^2 - y^2z - xyz")
s += lines("z(x^2 + y^2 + z^2 - xy - yz - zx)", "x^2z + y^2z + z^3 - xyz - yz^2 - xz^2")
s += p("तीनों को जोड़ते हैं। समान पद आपस में कट जाते हैं:")
s += lines("\\text{RHS}", "x^3 + y^3 + z^3 + (xy^2 - xy^2) + (xz^2 - xz^2) + (x^2y - x^2y) + (yz^2 - yz^2) + (x^2z - x^2z) + (y^2z - y^2z) - xyz - xyz - xyz",
           "x^3 + y^3 + z^3 + 0 - 3xyz", "x^3 + y^3 + z^3 - 3xyz", "\\text{LHS}")
s += ans("सत्यापित।")
E4.append(("सत्यापित कीजिए: " + m("x^3 + y^3 + z^3 - 3xyz = \\dfrac{1}{2}(x + y + z)[(x - y)^2 + (y - z)^2 + (z - x)^2]"), s))

# Q13
s = ID8.replace("a^3 + b^3 + c^3 - 3abc = (a + b + c)(a^2 + b^2 + c^2 - ab - bc - ca)", "x^3 + y^3 + z^3 - 3xyz = (x + y + z)(x^2 + y^2 + z^2 - xy - yz - zx)")
s += p("दिया है: " + m("x + y + z = 0") + "। सूत्र में रखने पर:")
s += lines("x^3 + y^3 + z^3 - 3xyz", "(0)(x^2 + y^2 + z^2 - xy - yz - zx)", "0")
s += eqs(("x^3 + y^3 + z^3 - 3xyz", "0")) + tp("पक्षांतर: −3xyz दाएँ पक्ष में +3xyz हो जाता है।".replace("−3xyz", m("-3xyz")).replace("+3xyz हो", m("+3xyz") + " हो"))
s += eqs(("x^3 + y^3 + z^3", "3xyz")) + ans("सिद्ध हुआ: " + m("x^3 + y^3 + z^3 = 3xyz"))
E4.append(("दर्शाइए कि " + m("x^3 + y^3 + z^3 = 3xyz") + " होता है, यदि " + m("x + y + z = 0") + " हो।", s))

# Q14
s = formula("प्रश्न 13 का परिणाम", "यदि " + m("a + b + c = 0") + " हो, तो " + m("a^3 + b^3 + c^3 = 3abc") + "।")
s += part("(i) " + m("(-12)^3 + (7)^3 + (5)^3"), eqs(("a", "-12"), ("b", "7"), ("c", "5")) + lines("a + b + c", "-12 + 7 + 5", "-5 + 5", "0")
          + lines("(-12)^3 + (7)^3 + (5)^3", "3 \\times (-12) \\times 7 \\times 5", "(-36) \\times 7 \\times 5", "(-252) \\times 5", "-1260") + ans(m("-1260")))
s += part("(ii) " + m("(28)^3 + (-15)^3 + (-13)^3"), eqs(("a", "28"), ("b", "-15"), ("c", "-13")) + lines("a + b + c", "28 + (-15) + (-13)", "28 - 15 - 13", "13 - 13", "0")
          + lines("(28)^3 + (-15)^3 + (-13)^3", "3 \\times 28 \\times (-15) \\times (-13)", "84 \\times (-15) \\times (-13)", "(-1260) \\times (-13)", "16380") + ans(m("16380")))
assert (-12) ** 3 + 7 ** 3 + 5 ** 3 == -1260 and 28 ** 3 - 15 ** 3 - 13 ** 3 == 16380
s += ans("(i) −1260 (ii) 16380")
E4.append((qt("वास्तव में घनों का परिकलन किए बिना निम्नलिखित में से प्रत्येक का मान ज्ञात कीजिए: (i) " + m("(-12)^3 + (7)^3 + (5)^3") + " (ii) " + m("(28)^3 + (-15)^3 + (-13)^3")), s))

# Q15
s = formula("आयत का क्षेत्रफल", m("\\text{क्षेत्रफल} = \\text{लंबाई} \\times \\text{चौड़ाई}").replace("\\text{क्षेत्रफल}", "A").replace("\\text{लंबाई}", "l").replace("\\text{चौड़ाई}", "b") + " (A = क्षेत्रफल, l = लंबाई, b = चौड़ाई)")
s += p("अतः क्षेत्रफल के व्यंजक के दो गुणनखंड ही लंबाई और चौड़ाई होंगे।")
outs = []
for lab, (a, b, c), v, L, Bd in (("(i)", (25, -35, 12), "a", "5a - 3", "5a - 4"), ("(ii)", (35, 13, -12), "y", "7y - 3", "5y + 4")):
    h, f1, f2 = split_quad(a, b, c, v)
    r = fac_tex(f1, v) + fac_tex(f2, v)
    s += part(lab + " क्षेत्रफल " + m(poly([a, b, c], v)), h + ans("लंबाई और चौड़ाई के संभव व्यंजक: " + m(f"({L})") + " और " + m(f"({Bd})")))
    assert sorted([poly(list(f1), v), poly(list(f2), v)]) == sorted([L, Bd]), (f1, f2)
    outs.append(lab + " " + m(f"({L})") + " और " + m(f"({Bd})"))
s += ans(" ".join(outs))
E4.append((qt("नीचे दिए गए आयतों, जिनमें उनके क्षेत्रफल दिए गए हैं, में से प्रत्येक की लंबाई और चौड़ाई के लिए संभव व्यंजक दीजिए: (i) क्षेत्रफल: " + m("25a^2 - 35a + 12") + " (ii) क्षेत्रफल: " + m("35y^2 + 13y - 12")), s))

# Q16
s = formula("घनाभ का आयतन", m("V = l \\times b \\times h") + " (लंबाई × चौड़ाई × ऊँचाई)")
s += p("अतः आयतन के व्यंजक के तीन गुणनखंड ही विमाएँ होंगी।")
h = lines("3x^2", "3 \\times x \\times x") + lines("12x", "3 \\times 4 \\times x") + p("दोनों पदों में " + m("3x") + " उभयनिष्ठ है:")
h += lines("3x^2 - 12x", "3x \\times x - 3x \\times 4", "3x(x - 4)", "3 \\times x \\times (x - 4)")
s += part("(i) आयतन " + m("3x^2 - 12x"), h + ans("विमाओं के संभव व्यंजक: " + m("3,\\ x") + " और " + m("(x - 4)")))
h = lines("12ky^2", "4k \\times 3y^2") + lines("8ky", "4k \\times 2y") + lines("20k", "4k \\times 5") + p("तीनों पदों में " + m("4k") + " उभयनिष्ठ है:")
h += lines("12ky^2 + 8ky - 20k", "4k \\times 3y^2 + 4k \\times 2y - 4k \\times 5", "4k(3y^2 + 2y - 5)")
h += p("अब " + m("3y^2 + 2y - 5") + " के गुणनखंड:")
t, f1, f2 = split_quad(3, 2, -5, "y")
h += t
h += lines("12ky^2 + 8ky - 20k", "4k" + fac_tex(f1, "y") + fac_tex(f2, "y"))
assert sorted([poly(list(f1), "y"), poly(list(f2), "y")]) == ["3y + 5", "y - 1"]
s += part("(ii) आयतन " + m("12ky^2 + 8ky - 20k"), h + ans("विमाओं के संभव व्यंजक: " + m("4k,\\ (3y + 5)") + " और " + m("(y - 1)")))
s += ans("(i) " + m("3,\\ x,\\ (x - 4)") + " (ii) " + m("4k,\\ (3y + 5),\\ (y - 1)"))
E4.append((qt("घनाभों, जिनके आयतन नीचे दिए गए हैं, की विमाओं के लिए संभव व्यंजक क्या हैं? (i) आयतन: " + m("3x^2 - 12x") + " (ii) आयतन: " + m("12ky^2 + 8ky - 20k")), s))
assert len(E4) == 16

try:  # optional algebra check (sympy is not needed for the build)
    import sympy as _sp
    _x, _y, _z, _a, _b, _c, _p = _sp.symbols("x y z a b c p")
    _ok = [
        _sp.expand((_x + 2*_y + 4*_z)**2) == _x**2 + 4*_y**2 + 16*_z**2 + 4*_x*_y + 16*_y*_z + 8*_x*_z,
        _sp.expand((2*_x + 3*_y - 4*_z)**2 - (4*_x**2 + 9*_y**2 + 16*_z**2 + 12*_x*_y - 24*_y*_z - 16*_x*_z)) == 0,
        _sp.expand((-_sp.sqrt(2)*_x + _y + 2*_sp.sqrt(2)*_z)**2 - (2*_x**2 + _y**2 + 8*_z**2 - 2*_sp.sqrt(2)*_x*_y + 4*_sp.sqrt(2)*_y*_z - 8*_x*_z)) == 0,
        _sp.expand((3*_p - _sp.Rational(1, 6))**3 - (27*_p**3 - _sp.Rational(1, 216) - _sp.Rational(9, 2)*_p**2 + _sp.Rational(1, 4)*_p)) == 0,
        _sp.expand((5*_a - 3)*(5*_a - 4)) == 25*_a**2 - 35*_a + 12, _sp.expand((7*_y - 3)*(5*_y + 4)) == 35*_y**2 + 13*_y - 12,
    ]
    assert all(_ok), _ok
except ImportError:
    pass


# ---------------- checks and pages ----------------
import re as _re
ALL = [("exercise-2-1", "प्रश्नावली 2.1", "एक चर वाले बहुपद", E1), ("exercise-2-2", "प्रश्नावली 2.2", "बहुपद के शून्यक", E2),
       ("exercise-2-3", "प्रश्नावली 2.3", "बहुपदों का गुणनखंडन", E3),
       ("exercise-2-4", "प्रश्नावली 2.4", "बीजीय सर्वसमिकाएँ", E4)]
for _, _, _, E in ALL:
    for _q, _sol in E:
        for _t in _re.findall(r"\\\((.+?)\\\)", _q + _sol):
            assert not _re.search(r"[\u0900-\u097F]", _t), ("Devanagari in TeX", _t)
            assert _t.count("{") == _t.count("}"), ("unbalanced TeX", _t)
for i, (slug, title, topic, E) in enumerate(ALL):
    prev = (BASE + ALL[i - 1][0] + "/", ALL[i - 1][1]) if i else ("/hi/class-09/maths/chapter-01/exercise-1-5/", "प्रश्नावली 1.5")
    nxt = (BASE + ALL[i + 1][0] + "/", ALL[i + 1][1]) if i + 1 < len(ALL) else (BASE, "अध्याय 2")
    page(BASE, 2, CH, slug, title, f"कक्षा 9 गणित · अध्याय 2: बहुपद · {len(E)} प्रश्न ({topic})", E,
         prev, nxt, css=CSS + EXTRA_CSS, boards=BOARDS9)
print("ok")
