#!/usr/bin/env python3
"""Class 10 Maths, Chapter 1 (वास्तविक संख्याएँ): Exercise 1.1 and 1.2, Hindi medium.
Writes colourful, responsive, self-contained HTML pages into site/.
Run from repo root: python3 tools/solutions/class10_ch1.py
"""
import pathlib, html

ROOT = pathlib.Path(__file__).resolve().parents[2]
BASE = "/hi/class-10/maths/chapter-01/"
X = " × "


def e(s):
    return html.escape(str(s))


def factors(n):
    out, d = [], 2
    while n > 1:
        while n % d == 0:
            out.append(d)
            n //= d
        d += 1
    return out


def ladder(n):
    """Division ladder as an HTML table, plus the one-line factorisation."""
    rows, m = [], n
    for p in factors(n):
        rows.append(f"<tr><td class='d'>{p}</td><td>{m}</td></tr>")
        m //= p
    rows.append("<tr><td class='d'></td><td>1</td></tr>")
    return (f"<div class='lad'><div class='lt'>{n} के अभाज्य गुणनखंड:</div>"
            f"<table class='ladder'>{''.join(rows)}</table>"
            f"<div class='fl'>{n} = {X.join(map(str, factors(n)))}</div></div>")


def ladders(*ns):
    return "<div class='lads'>" + "".join(ladder(n) for n in ns) + "</div>"


def lines(head, *rest):
    """Head on its own line, then one '=' per line."""
    if not rest:
        return f"<div class='eq'><span class='l'>{head}</span></div>"
    out = f"<span class='l'>{head}</span><span class='s'>=</span><span class='r'>{rest[0]}</span>"
    out += "".join(f"<span class='l'></span><span class='s'>=</span><span class='r'>{r}</span>" for r in rest[1:])
    return "<div class='eq'>" + out + "</div>"


def sq(x):
    return f"√<span class='ov'>{x}</span>"


def fr(a, b):
    return f"<span class='fr'><span>{a}</span><span>{b}</span></span>"


def given(k, f):
    return (f"<div class='gv'><div class='box k'><b>ज्ञात है</b><div>{k}</div></div>"
            f"<div class='box f'><b>ज्ञात करना है</b><div>{f}</div></div></div>")


def ans(t):
    return f"<div class='ans'><b>उत्तर:</b> {t}</div>"


def q(num, text, body, color):
    return (f"<section class='q c{color}' id='q{num}'><div class='qh'><span class='qn'>प्रश्न {num}</span>"
            f"<p>{text}</p></div><div class='qb'>{body}</div></section>")


def part(label, body):
    return f"<div class='part'><div class='pl'>{label}</div>{body}</div>"


def lcm_hcf(nums, hcf_f, hcf_v, lcm_f, lcm_v, verify=False):
    b = ladders(*nums)
    import math
    from functools import reduce
    assert reduce(math.gcd, nums) == hcf_v and math.prod(hcf_f) == hcf_v
    assert reduce(lambda x, y: x * y // math.gcd(x, y), nums) == lcm_v and math.prod(lcm_f) == lcm_v
    b += lines("HCF", str(hcf_v)) if len(hcf_f) == 1 else lines("HCF", X.join(map(str, hcf_f)), str(hcf_v))
    b += lines("LCM", X.join(map(str, lcm_f)), str(lcm_v))
    if verify:
        a, c = nums
        b += "<div class='vt'>जाँच:</div>"
        b += lines("HCF × LCM", f"{hcf_v} × {lcm_v}", f"{hcf_v * lcm_v}")
        b += lines("दोनों संख्याओं का गुणनफल", f"{a} × {c}", f"{a * c}")
        assert hcf_v * lcm_v == a * c
        b += "<p class='ok'>अतः HCF × LCM = दोनों संख्याओं का गुणनफल ✔</p>"
    return b


# ---------------- Exercise 1.1 ----------------
Q = []
b = given("संख्याएँ 140, 156, 3825, 5005, 7429", "इन्हें अभाज्य गुणनखंडों के गुणनफल के रूप में व्यक्त करना")
for lab, n in zip("(i) (ii) (iii) (iv) (v)".split(), [140, 156, 3825, 5005, 7429]):
    b += part(f"{lab} {n}", ladders(n))
b += ans("140 = 2² × 5 × 7, 156 = 2² × 3 × 13, 3825 = 3² × 5² × 17, 5005 = 5 × 7 × 11 × 13, 7429 = 17 × 19 × 23")
Q.append(("निम्नलिखित संख्याओं को अभाज्य गुणनखंडों के गुणनफल के रूप में व्यक्त कीजिए: (i) 140 (ii) 156 (iii) 3825 (iv) 5005 (v) 7429", b))

b = given("पूर्णांकों के युग्म (26, 91), (510, 92), (336, 54)", "प्रत्येक युग्म का HCF और LCM, तथा जाँच कि HCF × LCM = दोनों संख्याओं का गुणनफल")
b += part("(i) 26 एवं 91", lcm_hcf((26, 91), [13], 13, [2, 7, 13], 182, True))
b += part("(ii) 510 एवं 92", lcm_hcf((510, 92), [2], 2, [2, 2, 3, 5, 17, 23], 23460, True))
b += part("(iii) 336 एवं 54", lcm_hcf((336, 54), [2, 3], 6, [2, 2, 2, 2, 3, 3, 3, 7], 3024, True))
b += ans("(i) HCF = 13, LCM = 182; (ii) HCF = 2, LCM = 23460; (iii) HCF = 6, LCM = 3024")
Q.append(("निम्नलिखित पूर्णांकों के युग्मों के HCF और LCM ज्ञात कीजिए तथा इसकी जाँच कीजिए कि दो संख्याओं का गुणनफल = HCF × LCM है: (i) 26 और 91 (ii) 510 और 92 (iii) 336 और 54", b))

b = given("पूर्णांक (12, 15, 21), (17, 23, 29), (8, 9, 25)", "अभाज्य गुणनखंडन विधि से HCF और LCM")
b += part("(i) 12, 15 एवं 21", lcm_hcf((12, 15, 21), [3], 3, [2, 2, 3, 5, 7], 420))
b += part("(ii) 17, 23 एवं 29", ladders(17, 23, 29) + "<p>तीनों संख्याएँ अभाज्य हैं, कोई उभयनिष्ठ गुणनखंड नहीं।</p>" + lines("HCF", "1") + lines("LCM", "17 × 23 × 29", "11339"))
b += part("(iii) 8, 9 एवं 25", ladders(8, 9, 25) + "<p>कोई उभयनिष्ठ अभाज्य गुणनखंड नहीं।</p>" + lines("HCF", "1") + lines("LCM", "2 × 2 × 2 × 3 × 3 × 5 × 5", "1800"))
b += ans("(i) HCF = 3, LCM = 420; (ii) HCF = 1, LCM = 11339; (iii) HCF = 1, LCM = 1800")
Q.append(("अभाज्य गुणनखंडन विधि द्वारा निम्नलिखित पूर्णांकों के HCF और LCM ज्ञात कीजिए: (i) 12, 15 और 21 (ii) 17, 23 और 29 (iii) 8, 9 और 25", b))

b = given("HCF (306, 657) = 9", "LCM (306, 657)")
b += "<p>हम जानते हैं:</p>" + lines("HCF × LCM", "दोनों संख्याओं का गुणनफल")
b += lines("LCM", fr("306 × 657", "9"), "34 × 657", "22338")
assert 306 * 657 // 9 == 22338
b += ans("LCM (306, 657) = 22338")
Q.append(("यदि HCF (306, 657) = 9 दिया है, तो LCM (306, 657) ज्ञात कीजिए।", b))

b = given("संख्या 6<sup>n</sup>, जहाँ n एक प्राकृत संख्या है", "क्या 6<sup>n</sup> अंक 0 पर समाप्त हो सकती है")
b += "<p>कोई संख्या अंक 0 पर तभी समाप्त होती है जब वह 10 से विभाज्य हो, अर्थात उसके अभाज्य गुणनखंडों में 2 और 5 दोनों हों।</p>"
b += lines("6<sup>n</sup>", "(2 × 3)<sup>n</sup>", "2<sup>n</sup> × 3<sup>n</sup>")
b += "<p>6<sup>n</sup> के अभाज्य गुणनखंडों में केवल 2 और 3 हैं, 5 नहीं है। अंकगणित की आधारभूत प्रमेय के अनुसार यह गुणनखंडन अद्वितीय है, इसलिए 6<sup>n</sup> में 5 कभी नहीं आ सकता।</p>"
b += ans("नहीं, किसी भी प्राकृत संख्या n के लिए 6<sup>n</sup> अंक 0 पर समाप्त नहीं हो सकती।")
Q.append(("जाँच कीजिए कि क्या किसी प्राकृत संख्या n के लिए, संख्या 6<sup>n</sup> अंक 0 पर समाप्त हो सकती है।", b))

b = given("7 × 11 × 13 + 13 तथा 7 × 6 × 5 × 4 × 3 × 2 × 1 + 5", "ये भाज्य (composite) संख्याएँ क्यों हैं")
b += part("पहली संख्या", lines("7 × 11 × 13 + 13", "13 × (7 × 11 + 1)", "13 × (77 + 1)", "13 × 78", "1014")
          + "<p>1014 के 1 और स्वयं के अलावा गुणनखंड 13 और 78 भी हैं, अतः यह भाज्य संख्या है।</p>")
b += part("दूसरी संख्या", lines("7 × 6 × 5 × 4 × 3 × 2 × 1 + 5", "5 × (7 × 6 × 4 × 3 × 2 × 1 + 1)", "5 × (1008 + 1)", "5 × 1009", "5045")
          + "<p>5045 के 1 और स्वयं के अलावा गुणनखंड 5 और 1009 भी हैं, अतः यह भाज्य संख्या है।</p>")
assert 7 * 11 * 13 + 13 == 1014 and 5040 + 5 == 5045
b += ans("दोनों संख्याएँ 1 और स्वयं के अलावा अन्य गुणनखंड (13 तथा 5) रखती हैं, इसलिए भाज्य हैं।")
Q.append(("व्याख्या कीजिए कि 7 × 11 × 13 + 13 और 7 × 6 × 5 × 4 × 3 × 2 × 1 + 5 भाज्य संख्याएँ क्यों हैं।", b))

b = given("सोनिया एक चक्कर 18 मिनट में, रवि 12 मिनट में लगाते हैं; दोनों एक ही स्थान और समय से एक ही दिशा में चलते हैं", "कितने मिनट बाद वे प्रारंभिक स्थान पर फिर मिलेंगे")
b += "<p>दोनों उस समय मिलेंगे जो 18 और 12 दोनों का गुणज हो, यानी LCM (18, 12)।</p>"
b += ladders(18, 12) + lines("LCM", "2 × 2 × 3 × 3", "36")
b += ans("36 मिनट बाद दोनों प्रारंभिक स्थान पर फिर मिलेंगे।")
Q.append(("किसी खेल के मैदान के चारों ओर एक वृत्ताकार पथ है। इस मैदान का एक चक्कर लगाने में सोनिया को 18 मिनट लगते हैं, जबकि इसी मैदान का एक चक्कर लगाने में रवि को 12 मिनट लगते हैं। मान लीजिए वे दोनों एक ही स्थान और एक ही समय पर चलना प्रारंभ करके एक ही दिशा में चलते हैं। कितने समय बाद वे पुनः प्रारंभिक स्थान पर मिलेंगे?", b))
EX11 = Q

# ---------------- Exercise 1.2 ----------------
Q = []
THM = "<div class='thm'>प्रमेय: यदि अभाज्य संख्या p, a² को विभाजित करती है, तो p, a को भी विभाजित करती है (a एक धनात्मक पूर्णांक)।</div>"
b = given(f"संख्या {sq(5)}", f"सिद्ध करना है कि {sq(5)} अपरिमेय है")
b += THM
b += f"<p>विरोधाभास विधि: माना {sq(5)} परिमेय है। तब ऐसे सह-अभाज्य पूर्णांक a और b (b ≠ 0) होंगे कि</p>"
b += lines(f"{sq(5)}", fr("a", "b"))
b += "<p>तिरछा गुणा करने पर</p>" + lines(f"b{sq(5)}", "a")
b += "<p>दोनों पक्षों का वर्ग करने पर</p>" + lines("5b²", "a²")
b += "<p>अतः 5, a² को विभाजित करता है, इसलिए प्रमेय से 5, a को भी विभाजित करेगा। माना a = 5c, जहाँ c एक पूर्णांक है। a का मान रखने पर</p>"
b += lines("5b²", "(5c)²", "25c²")
b += lines("b²", "5c²")
b += "<p>अतः 5, b² को विभाजित करता है, इसलिए 5, b को भी विभाजित करेगा। इस प्रकार 5, a और b दोनों का उभयनिष्ठ गुणनखंड है, जबकि a और b सह-अभाज्य हैं (1 के अलावा कोई उभयनिष्ठ गुणनखंड नहीं)। यह विरोधाभास है।</p>"
b += ans(f"हमारी कल्पना गलत थी, अतः {sq(5)} अपरिमेय है।")
Q.append((f"सिद्ध कीजिए कि {sq(5)} एक अपरिमेय संख्या है।", b))

b = given(f"संख्या 3 + 2{sq(5)}; {sq(5)} अपरिमेय है (प्रश्न 1 से)", f"सिद्ध करना है कि 3 + 2{sq(5)} अपरिमेय है")
b += f"<p>माना 3 + 2{sq(5)} परिमेय है। तब ऐसे सह-अभाज्य पूर्णांक a और b (b ≠ 0) होंगे कि</p>"
b += lines(f"3 + 2{sq(5)}", fr("a", "b"))
b += lines(f"2{sq(5)}", fr("a", "b") + " − 3", fr("a − 3b", "b"))
b += lines(f"{sq(5)}", fr("a − 3b", "2b"))
b += f"<p>a और b पूर्णांक हैं, इसलिए {fr('a − 3b', '2b')} परिमेय है, अतः {sq(5)} भी परिमेय होगा। परंतु {sq(5)} अपरिमेय है। यह विरोधाभास है।</p>"
b += ans(f"अतः 3 + 2{sq(5)} अपरिमेय है।")
Q.append((f"सिद्ध कीजिए कि 3 + 2{sq(5)} एक अपरिमेय संख्या है।", b))

b = given(f"{fr('1', sq(2))}, 7{sq(5)}, 6 + {sq(2)}; {sq(2)} और {sq(5)} अपरिमेय हैं", "सिद्ध करना है कि तीनों संख्याएँ अपरिमेय हैं")
p = f"<p>माना {fr('1', sq(2))} परिमेय है। तब सह-अभाज्य पूर्णांक a, b (b ≠ 0) होंगे कि</p>"
p += lines(fr("1", sq(2)), fr("a", "b"))
p += "<p>व्युत्क्रम लेने पर</p>" + lines(sq(2), fr("b", "a"))
p += f"<p>{fr('b', 'a')} परिमेय है, अतः {sq(2)} परिमेय होगा, जबकि {sq(2)} अपरिमेय है। विरोधाभास।</p>"
p += ans(f"{fr('1', sq(2))} अपरिमेय है।")
b += part(f"(i) {fr('1', sq(2))}", p)
p = f"<p>माना 7{sq(5)} परिमेय है। तब</p>" + lines(f"7{sq(5)}", fr("a", "b"))
p += lines(sq(5), fr("a", "7b"))
p += f"<p>{fr('a', '7b')} परिमेय है, अतः {sq(5)} परिमेय होगा, जबकि {sq(5)} अपरिमेय है। विरोधाभास।</p>"
p += ans(f"7{sq(5)} अपरिमेय है।")
b += part(f"(ii) 7{sq(5)}", p)
p = f"<p>माना 6 + {sq(2)} परिमेय है। तब</p>" + lines(f"6 + {sq(2)}", fr("a", "b"))
p += lines(sq(2), fr("a", "b") + " − 6", fr("a − 6b", "b"))
p += f"<p>{fr('a − 6b', 'b')} परिमेय है, अतः {sq(2)} परिमेय होगा, जबकि {sq(2)} अपरिमेय है। विरोधाभास।</p>"
p += ans(f"6 + {sq(2)} अपरिमेय है।")
b += part(f"(iii) 6 + {sq(2)}", p)
Q.append((f"सिद्ध कीजिए कि निम्नलिखित संख्याएँ अपरिमेय हैं: (i) {fr('1', sq(2))} (ii) 7{sq(5)} (iii) 6 + {sq(2)}", b))
EX12 = Q

CSS = """
:root{--ink:#1d2433;--muted:#5d6676;--pri:#1f5aa6}
*{box-sizing:border-box}
body{margin:0;font-family:"Noto Sans Devanagari","Mangal",system-ui,sans-serif;color:var(--ink);line-height:1.65;font-size:17px;
 background:#f4f6fb}
body::before{content:"HEMANT KUMAR TEKAN";position:fixed;top:50%;left:50%;transform:translate(-50%,-50%) rotate(-45deg);
 font:700 9vw/1 system-ui,sans-serif;color:rgba(0,0,0,.045);white-space:nowrap;pointer-events:none;z-index:0}
.top{display:flex;justify-content:space-between;align-items:center;padding:12px 16px;background:var(--pri);color:#fff;position:sticky;top:0;z-index:5}
.top a{color:#fff;text-decoration:none}.top .brand{font-weight:700;font-size:19px}
.top .sw{border:1px solid rgba(255,255,255,.7);padding:4px 10px;border-radius:999px;font-size:14px}
main{position:relative;z-index:1;max-width:900px;margin:0 auto;padding:14px}
.crumbs{font-size:14px;color:var(--muted)}.crumbs a{color:var(--pri);text-decoration:none}
.hero{background:linear-gradient(135deg,#1f5aa6,#7b3fe4 60%,#e8467c);color:#fff;border-radius:18px;padding:20px 18px;margin:10px 0 16px}
.hero h1{margin:0 0 4px;font-size:25px;line-height:1.3}.hero p{margin:0;opacity:.92}
.jump{display:flex;flex-wrap:wrap;gap:8px;margin:0 0 16px}
.jump a{background:#fff;border:1px solid #dde2ee;border-radius:999px;padding:4px 12px;text-decoration:none;color:var(--pri);font-weight:600;font-size:15px}
.q{background:#fff;border-radius:16px;margin:0 0 18px;box-shadow:0 2px 10px rgba(20,30,60,.07);overflow:hidden;border-top:6px solid var(--c)}
.c0{--c:#1f5aa6;--l:#e8f0fb}.c1{--c:#0f9d76;--l:#e4f6ef}.c2{--c:#e07b00;--l:#fdf1e2}.c3{--c:#8a3ffc;--l:#f1eafe}.c4{--c:#d6336c;--l:#fde8ef}.c5{--c:#0b8aa8;--l:#e2f4f8}
.qh{background:var(--l);padding:12px 16px}.qh p{margin:6px 0 0;font-weight:600}
.qn{display:inline-block;background:var(--c);color:#fff;border-radius:8px;padding:2px 10px;font-weight:700;font-size:15px}
.qb{padding:12px 16px 16px}
.gv{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:4px 0 12px}
.box{border-radius:12px;padding:10px 12px;border:2px solid}.box b{display:block;font-size:14px;letter-spacing:.3px}
.box.k{background:#eaf3ff;border-color:#8db7ef}.box.k b{color:#1f5aa6}
.box.f{background:#fff3e6;border-color:#f3b877}.box.f b{color:#c25e00}
.part{border-left:4px solid var(--c);padding:4px 0 4px 12px;margin:14px 0}
.pl{font-weight:700;color:var(--c);margin-bottom:6px}
.lads{display:flex;flex-wrap:wrap;gap:14px 26px;align-items:flex-start;margin:6px 0 10px}
.lad{background:#fafbff;border:1px solid #e3e7f3;border-radius:12px;padding:8px 12px}
.lt{font-size:15px;color:var(--muted);margin-bottom:4px}
.ladder{border-collapse:collapse;margin:0 0 6px 6px;font-variant-numeric:tabular-nums}
.ladder td{padding:2px 10px;border-bottom:1.5px solid #9aa3b5;text-align:left}
.ladder td.d{border-right:1.5px solid #9aa3b5;color:var(--c);font-weight:700;text-align:right}
.ladder tr:last-child td{border-bottom:0}
.fl{font-weight:600}
.eq{margin:8px 0;padding:8px 14px;background:#f7f8fc;border-radius:10px;display:grid;width:fit-content;grid-template-columns:auto auto auto;column-gap:8px;row-gap:4px;align-items:center;max-width:100%}
.eq .l{text-align:right}.eq .s{text-align:center}.eq .r{text-align:left}
.vt{font-weight:700;margin-top:8px}.ok{color:#0f7a4c;font-weight:600}
.ans{background:#e6f7ee;border:2px solid #6cc596;border-radius:12px;padding:10px 12px;margin-top:12px}.ans b{color:#0f7a4c}
.thm{background:#f4ecff;border:1px dashed #a77bf3;border-radius:10px;padding:8px 12px;margin:8px 0;font-size:15.5px}
.ov{text-decoration:overline}
.fr{display:inline-flex;flex-direction:column;vertical-align:middle;text-align:center;line-height:1.15;margin:0 3px}
.fr span:first-child{border-bottom:1.5px solid currentColor;padding:0 3px}
.btns{display:flex;justify-content:space-between;gap:10px;margin:22px 0 6px}
.btns a{background:var(--pri);color:#fff;text-decoration:none;padding:10px 16px;border-radius:10px;font-weight:600}
footer{position:relative;z-index:1;text-align:center;color:var(--muted);font-size:13px;padding:22px 16px 30px}
@media (max-width:560px){body{font-size:16px}.gv{grid-template-columns:1fr}.hero h1{font-size:22px}.eq{column-gap:6px}.qb{padding:10px 12px 14px}}
@media print{.top,.jump,.btns{display:none}body{background:#fff}.q{box-shadow:none;break-inside:avoid}}
"""


def page(slug, title, sub, qs, prev, nxt):
    body = "".join(q(i + 1, t, b, i % 6) for i, (t, b) in enumerate(qs))
    jump = "".join(f"<a href='#q{i + 1}'>प्र. {i + 1}</a>" for i in range(len(qs)))
    pv = f"<a href='{prev[0]}'>← {e(prev[1])}</a>" if prev else "<span></span>"
    nx = f"<a href='{nxt[0]}'>{e(nxt[1])} →</a>" if nxt else "<span></span>"
    doc = f"""<!doctype html>
<html lang="hi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>कक्षा 10 गणित {e(title)} हल | MP Board हल</title>
<meta name="description" content="कक्षा 10 गणित अध्याय 1 वास्तविक संख्याएँ, {e(title)} के सभी प्रश्नों के चरणबद्ध हल।">
<style>{CSS}</style></head><body>
<header class="top"><a class="brand" href="/hi/">MP Board हल</a><a class="sw" href="/en/class-10/maths/chapter-01/">English Medium</a></header>
<main><nav class="crumbs"><a href="/hi/">होम</a> › <a href="/hi/class-10/">कक्षा 10</a> › <a href="/hi/class-10/maths/">गणित</a> › <a href="{BASE}">अध्याय 1</a> › <span>{e(title)}</span></nav>
<div class="hero"><h1>{e(title)} के हल</h1><p>{e(sub)}</p></div>
<div class="jump">{jump}</div>
{body}
<div class="btns">{pv}{nx}</div>
</main><footer>© हेमंत कुमार टेकन · MP Board और NCERT पाठ्यपुस्तकों के चरणबद्ध हल</footer></body></html>
"""
    out = ROOT / "site" / BASE.strip("/") / slug / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(doc, encoding="utf-8")


page("exercise-1-1", "प्रश्नावली 1.1", "कक्षा 10 गणित · अध्याय 1: वास्तविक संख्याएँ · 7 प्रश्न", EX11,
     (BASE, "अध्याय 1"), (BASE + "exercise-1-2/", "प्रश्नावली 1.2"))
page("exercise-1-2", "प्रश्नावली 1.2", "कक्षा 10 गणित · अध्याय 1: वास्तविक संख्याएँ · 3 प्रश्न", EX12,
     (BASE + "exercise-1-1/", "प्रश्नावली 1.1"), (BASE, "अध्याय 1"))
print("ok")
