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
        cands = [(d, e), (-d, -e)] if P > 0 else [(d, -e), (-d, e)]
        for m_, n_ in cands:
            if (m_, n_) in seen:
                continue
            seen.add((m_, n_))
            hl = m_ + n_ == b
            if hl and pick is None:
                pick = (m_, n_)
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
SUB = formula("बहुपद का मान", m("p(x)") + " में x के स्थान पर दी गई संख्या रखकर गणना करने से " + m("p(\\text{संख्या})").replace("\\text{संख्या}", "a") + " मिलता है।")
s = SUB + p("माना " + m("p(x) = 5x - 4x^2 + 3") + "।")
T = [(5, 1), (-4, 2), (3, 0)]
outs = []
for lab, v in (("(i)", 0), ("(ii)", -1), ("(iii)", 2)):
    st, val = subst("p", T, v)
    s += part(f"{lab} x = {v}".replace("-", "−"), st + ans(f"मान = {num(val)}".replace("-", "−")))
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

# ---------------- checks and pages ----------------
import re as _re
ALL = [("exercise-2-1", "प्रश्नावली 2.1", "एक चर वाले बहुपद", E1), ("exercise-2-2", "प्रश्नावली 2.2", "बहुपद के शून्यक", E2),
       ("exercise-2-3", "प्रश्नावली 2.3", "बहुपदों का गुणनखंडन", E3)]
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
