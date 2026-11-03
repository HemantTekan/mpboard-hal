#!/usr/bin/env python3
"""Shared helpers for Hindi solution pages (colourful, responsive, KaTeX pre-rendered)."""
import pathlib, html

ROOT = pathlib.Path(__file__).resolve().parents[2]
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


def mcell(c):
    """A cell with no Hindi text is typeset wholly in TeX, so letters, powers and roots match."""
    import re
    c = str(c)
    if not c or re.search(r"[\u0900-\u097F]", c):
        return c
    t = tex(c).replace("²", "^2").replace("<sup>", "^{").replace("</sup>", "}")
    return "\\(" + t + "\\)"


def lines(head, *rest):
    """First line 'LHS = RHS', then each further '= ...' aligned under the first '='."""
    head, rest = mcell(head), [mcell(r) for r in rest]
    if not rest:
        return f"<div class='eq'><span class='l'>{head}</span></div>"
    out = f"<span class='l'>{head}</span><span class='s'>=</span><span class='r'>{rest[0]}</span>"
    out += "".join(f"<span class='l'></span><span class='s'>=</span><span class='r'>{r}</span>" for r in rest[1:])
    return "<div class='eq'>" + out + "</div>"


def tex(s):
    return str(s).replace("\\(", "").replace("\\)", "").replace("−", "-").replace("×", "\\times ")


def sq(x):
    return f"\\(\\sqrt{{{x}}}\\)"


def fr(a, b):
    return f"\\(\\dfrac{{{tex(a)}}}{{{tex(b)}}}\\)"


def render_math(doc):
    """Pre-render every \\( ... \\) with KaTeX (server side, no JS on the page)."""
    import re, json, subprocess
    parts = re.findall(r"\\\((.+?)\\\)", doc)
    if not parts:
        return doc
    out = subprocess.run(["node", str(ROOT / "tools" / "katex_render.js")], input=json.dumps(parts),
                         capture_output=True, text=True, check=True).stdout
    it = iter(json.loads(out))
    return re.sub(r"\\\((.+?)\\\)", lambda m: next(it), doc)


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



def m(t):
    """Inline TeX."""
    return "\\(" + t + "\\)"


def formula(name, t):
    return f"<div class='frm'><b>सूत्र ({name}):</b> {t}</div>"


def note(t):
    return f"<p>{t}</p>"


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
.muted{color:var(--muted);font-size:15px}
.frm{background:#fff8e1;border-left:4px solid #f4b400;border-radius:8px;padding:8px 12px;margin:8px 0}
.graph{max-width:340px;width:100%;height:auto;background:#fff;border:1px solid #e3e7f3;border-radius:12px}
.katex{font-size:1.12em}
.fr{display:inline-flex;flex-direction:column;vertical-align:middle;text-align:center;line-height:1.15;margin:0 3px}
.fr span:first-child{border-bottom:1.5px solid currentColor;padding:0 3px}
.btns{display:flex;justify-content:space-between;gap:10px;margin:22px 0 6px}
.btns a{background:var(--pri);color:#fff;text-decoration:none;padding:10px 16px;border-radius:10px;font-weight:600}
footer{position:relative;z-index:1;text-align:center;color:var(--muted);font-size:13px;padding:22px 16px 30px}
@media (max-width:560px){body{font-size:16px}.gv{grid-template-columns:1fr}.hero h1{font-size:22px}.eq{column-gap:6px}.qb{padding:10px 12px 14px}}
@media print{.top,.jump,.btns{display:none}body{background:#fff}.q{box-shadow:none;break-inside:avoid}}
"""



def page(BASE, chnum, chname, slug, title, sub, qs, prev, nxt):
    body = "".join(q(i + 1, t, b, i % 6) for i, (t, b) in enumerate(qs))
    jump = "".join(f"<a href='#q{i + 1}'>प्र. {i + 1}</a>" for i in range(len(qs)))
    pv = f"<a href='{prev[0]}'>← {e(prev[1])}</a>" if prev else "<span></span>"
    nx = f"<a href='{nxt[0]}'>{e(nxt[1])} →</a>" if nxt else "<span></span>"
    doc = f"""<!doctype html>
<html lang="hi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>कक्षा 10 गणित {e(title)} हल | MP Board हल</title>
<meta name="description" content="कक्षा 10 गणित अध्याय {chnum} {e(chname)}, {e(title)} के सभी प्रश्नों के चरणबद्ध हल।">
<link rel="stylesheet" href="/assets/katex/katex.min.css"><style>{CSS}</style></head><body>
<header class="top"><a class="brand" href="/hi/">MP Board हल</a><a class="sw" href="/en{BASE[3:]}">English Medium</a></header>
<main><nav class="crumbs"><a href="/hi/">होम</a> › <a href="/hi/class-10/">कक्षा 10</a> › <a href="/hi/class-10/maths/">गणित</a> › <a href="{BASE}">अध्याय {chnum}</a> › <span>{e(title)}</span></nav>
<div class="hero"><h1>{e(title)} के हल</h1><p>{e(sub)}</p></div>
<div class="jump">{jump}</div>
{body}
<div class="btns">{pv}{nx}</div>
</main><footer>© हेमंत कुमार टेकन · MP Board और NCERT पाठ्यपुस्तकों के चरणबद्ध हल</footer></body></html>
"""
    out = ROOT / "site" / BASE.strip("/") / slug / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(render_math(doc), encoding="utf-8")


