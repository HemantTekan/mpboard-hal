#!/usr/bin/env python3
"""Apply the educationdew brand header, colourful navigation and home hero to every page in site/.
Idempotent; run after build/generators (deploy runs it automatically)."""
import re, sys, pathlib

SITE = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else pathlib.Path(__file__).resolve().parents[1] / "site")
L = {
    "hi": dict(name="MP Board हल", home="होम", c10="कक्षा 10", c9="कक्षा 9", notes="नोट्स", quiz="क्विज़", papers="प्रश्नपत्र", pdfs="PDF",
               tag="MP Board, NCERT और CBSE गणित के चरणबद्ध हल, चित्र और आलेख सहित — आसान हिंदी में।",
               chips=["✔ हर प्रश्न का हल", "✔ चित्र और आलेख", "✔ PDF और क्विज़"]),
    "en": dict(name="MP Board Solutions", home="Home", c10="Class 10", c9="Class 9", notes="Notes", quiz="Quiz", papers="Papers", pdfs="PDF",
               tag="Step-by-step maths solutions for MP Board, NCERT and CBSE, with diagrams and graphs.",
               chips=["✔ Every question solved", "✔ Diagrams & graphs", "✔ PDFs & quizzes"]),
}
ICONS = ('<link rel="icon" href="/favicon.ico" sizes="48x48">'
         '<link rel="icon" type="image/svg+xml" href="/favicon.svg">'
         '<link rel="icon" type="image/png" sizes="96x96" href="/assets/icon-96.png">'
         '<link rel="icon" type="image/png" sizes="192x192" href="/assets/icon-192.png">'
         '<link rel="apple-touch-icon" href="/apple-touch-icon.png"><meta name="theme-color" content="#0E7FA0">')
HEAD_RE = re.compile(r'<header class="top">.*?</header>', re.S)
SYM = "".join(f'<i style="left:{x}%;top:{y}%;font-size:{s}px">{c}</i>' for c, x, y, s in
              [("π", 4, 8, 54), ("√", 88, 10, 50), ("∑", 72, 62, 46), ("÷", 30, 70, 40), ("∞", 55, 6, 44), ("x²", 92, 70, 34), ("Δ", 16, 55, 36), ("θ", 64, 30, 30)])


def other_url(header, lang, rel):
    m = re.search(r'class="(?:switch|sw)" href="([^"]+)"', header)
    if m:
        return m.group(1)
    return "/en/" if lang == "hi" else "/hi/"


def header(lang, rel, sw):
    t = L[lang]
    hi_url, en_url = (rel, sw) if lang == "hi" else (sw, rel)
    if rel == "/":
        hi_url, en_url = "/hi/", "/en/"
    items = [("n1", "🏠 " + t["home"], f"/{lang}/"), ("n2", t["c10"], f"/{lang}/class-10/"), ("n3", t["c9"], f"/{lang}/class-09/"),
             ("n4", "📘 " + t["notes"], f"/{lang}/notes/"), ("n5", "🎯 " + t["quiz"], f"/{lang}/quiz/"), ("n6", "📝 " + t["papers"], f"/{lang}/papers/"), ("n7", "📄 " + t["pdfs"], f"/{lang}/pdf/")]
    cur = max((h for _, _, h in items if rel.startswith(h)), key=len, default=None)
    nav = "".join(f'<a class="{c}{" cur" if h == cur else ""}" href="{h}">{lab}</a>' for c, lab, h in items)
    return (f'<header class="top"><div class="bar"><a class="brand" href="/{lang}/" aria-label="educationdew {t["name"]}">'
            f'<img src="/assets/logo-mark.svg" alt="educationdew लोगो" width="34" height="40">'
            f'<span class="bt"><span class="wm">education<b>dew</b></span><small>{t["name"]}</small></span></a>'
            f'<div class="lang" role="navigation" aria-label="भाषा / Language">'
            f'<a class="{"on" if lang == "hi" else ""}" href="{hi_url}" hreflang="hi">हिंदी</a>'
            f'<a class="{"on" if lang == "en" else ""}" href="{en_url}" hreflang="en">English</a></div></div>'
            f'<nav class="mainnav" aria-label="मुख्य नेविगेशन">{nav}</nav></header>')


def hero(lang, root=False):
    t = L[lang]
    if root:
        btns = '<a class="cta" href="/hi/">हिंदी माध्यम</a><a class="cta alt" href="/en/">English Medium</a>'
        tag = L["hi"]["tag"]
    else:
        btns = f'<a class="cta" href="/{lang}/class-10/">{t["c10"]}</a><a class="cta alt" href="/{lang}/class-09/">{t["c9"]}</a>'
        tag = t["tag"]
    chips = "".join(f"<span>{c}</span>" for c in t["chips"])
    return (f'<!--hero--><section class="hero"><div class="sym" aria-hidden="true">{SYM}</div><div class="hin">'
            f'<img src="/assets/logo-mark.svg" alt="" width="86" height="100"><div>'
            f'<h2>education<b>dew</b></h2><p>{tag}</p><div class="hb">{btns}</div><div class="chips">{chips}</div>'
            f'</div></div></section><!--/hero-->')


def process(f):
    s = f.read_text(encoding="utf-8")
    m = HEAD_RE.search(s)
    if not m:
        return False
    lang_m = re.search(r'<html lang="(\w+)"', s)
    lang = lang_m.group(1) if lang_m and lang_m.group(1) in L else "hi"
    rel = "/" + str(f.relative_to(SITE).parent).replace(".", "").strip("/") + "/"
    rel = "/" if rel == "//" else rel
    old = m.group(0)
    sw = other_url(old, lang, rel) if 'class="bar"' not in old else re.findall(r'href="([^"]+)" hreflang', old)[1 if lang == "hi" else 0]
    s = s.replace(old, header(lang, rel, sw), 1)
    s = re.sub(r"<!--hero-->.*?<!--/hero-->", "", s, flags=re.S)
    if rel in ("/", "/hi/", "/en/"):
        s = s.replace("</header>", "</header>" + hero(lang, root=(rel == "/")), 1)
    s = re.sub(r'<link rel="(?:icon|apple-touch-icon)"[^>]*>|<meta name="theme-color"[^>]*>', "", s)
    if "/assets/brand.css" not in s:
        s = s.replace("</head>", '<link rel="stylesheet" href="/assets/brand.css"></head>', 1)
    s = s.replace("</head>", ICONS + "</head>", 1)
    f.write_text(s, encoding="utf-8")
    return True


if __name__ == "__main__":
    n = sum(process(f) for f in SITE.rglob("*.html"))
    print("branded", n)
