#!/usr/bin/env python3
"""Build the static site from catalog.json into site/.

Run from repo root:  python3 tools/build.py
- Content files (PDFs, quiz HTML) live directly under site/ at their final paths.
- Every generated page carries GEN marker; old generated pages are removed first,
  hand-made pages (e.g. quizzes) are never touched.
"""
import re
import json, os, html, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
GEN = "<!-- generated:mpboard-hal -->"
cat = json.load(open(ROOT / "catalog.json", encoding="utf-8"))
LANGS = ["hi", "en"]

T = {
    "hi": dict(home="होम", cls="कक्षा", ch="अध्याय", soon="जल्द आ रहा है", choose_cls="अपनी कक्षा चुनिए",
               choose_sub="विषय चुनिए", choose_ch="अध्याय चुनिए", pdf_view="PDF देखें", pdf_dl="PDF डाउनलोड करें",
               answers="उत्तर एक नज़र में", q="प्रश्न", prev="← पिछला", next="अगला →", papers="प्रश्नपत्र (हल सहित)",
               medium="हिंदी माध्यम", other="English Medium", inside="इसमें क्या है", open_quiz="क्विज़ शुरू करें",
               ready="उपलब्ध", items_none="इस अध्याय के हल जल्द आ रहे हैं।",
               tag="MP Board, NCERT और CBSE पाठ्यपुस्तकों के चरणबद्ध हल, चित्र सहित",
               notes="नोट्स", quiz="क्विज़", pdfs="PDF फ़ाइलें", exercises="प्रश्नावली के हल", subjects="विषय", sections="सामग्री के प्रकार",
               none_yet="अभी उपलब्ध नहीं, जल्द आ रहा है।", back_ch="← अध्याय पर लौटें"),
    "en": dict(home="Home", cls="Class", ch="Chapter", soon="Coming soon", choose_cls="Choose your class",
               choose_sub="Choose a subject", choose_ch="Choose a chapter", pdf_view="View PDF", pdf_dl="Download PDF",
               answers="Answers at a glance", q="Q", prev="← Previous", next="Next →", papers="Question papers (with solutions)",
               medium="English Medium", other="हिंदी माध्यम", inside="What's inside", open_quiz="Start quiz",
               ready="Available", items_none="Solutions for this chapter are coming soon.",
               tag="Step-by-step solutions for MP Board and NCERT textbooks, with diagrams",
               notes="Notes", quiz="Quiz", pdfs="PDF Files", exercises="Exercise Solutions", subjects="Subjects", sections="Browse by type",
               none_yet="Not available yet, coming soon.", back_ch="← Back to chapter"),
}
ICON = {"notes": "📘", "exercise": "✏️", "quiz": "🎯", "paper": "📝"}


def e(s):
    return html.escape(str(s))


def cls_slug(n):
    return f"class-{n:02d}"


def ch_slug(n):
    return f"chapter-{n:02d}"


def item_available(item, lang):
    return bool(item.get(lang))


def chapter_has(ch, lang):
    return any(item_available(i, lang) for i in ch["items"])


def subject_has(sub, lang):
    return any(chapter_has(c, lang) for c in sub["chapters"])


def class_has(c, lang):
    return any(subject_has(s, lang) for s in c["subjects"]) or any(
        p["class"] == c["num"] and p.get(lang) for p in cat["papers"])


def boards_note(lang, path):
    m = re.search(r"/(?:class-(\d+)/maths/chapter-\d+/|papers/class-(\d+)-)", path)
    if lang != "hi" or not m:
        return ""
    n = int(m.group(1) or m.group(2))
    if n == 9:
        return ('<p class="boards" style="font-size:14px;color:#555;margin-top:18px">यह सामग्री <b>MP Board (MPBSE)</b> '
                'कक्षा 9 गणित की पाठ्यपुस्तक के अनुसार है।</p>')
    return ('<p class="boards" style="font-size:14px;color:#555;margin-top:18px">यह सामग्री <b>MP Board (MPBSE)</b>, '
            f'<b>NCERT</b> और <b>CBSE</b> — तीनों के कक्षा {n} गणित के विद्यार्थियों के लिए उपयोगी है, '
            'क्योंकि तीनों में गणित की पाठ्यपुस्तक NCERT की ही है। परीक्षा का प्रारूप बोर्ड के अनुसार अलग हो सकता है।</p>')


def page(lang, path, title, crumbs, body, switch_to=None):
    t = T[lang]
    other = "en" if lang == "hi" else "hi"
    sw = switch_to if switch_to else "/" + other + path[3:]
    crumb_html = ""
    if crumbs:
        parts = [f'<a href="{e(h)}">{e(n)}</a>' for n, h in crumbs[:-1]] + [f"<span>{e(crumbs[-1][0])}</span>"]
        crumb_html = '<nav class="crumbs">' + " › ".join(parts) + "</nav>"
    site_name = cat["site"]["name"][lang]
    doc = f"""<!doctype html>
{GEN}
<html lang="{lang}"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)} | {e(site_name)}</title>
<meta name="description" content="{e(title)} — {e(t['tag'])}">
<meta name="keywords" content="MP Board, MPBSE, NCERT, CBSE, कक्षा 9, कक्षा 10, गणित, हल, हिंदी माध्यम">
<link rel="stylesheet" href="/assets/style.css">
</head><body>
<header class="top"><a class="brand" href="/{lang}/">{e(site_name)}</a>
<a class="switch" href="{e(sw)}">{e(t['other'])}</a></header>
<main>{crumb_html}
<h1>{e(title)}</h1>
{body}{"" if T[lang]["items_none"] in body or T[lang]["soon"] in body else boards_note(lang, path)}
</main>
<footer>© {e(cat['site']['author'][lang])} · {e(t['tag'])}</footer>
</body></html>
"""
    out = SITE / path.strip("/") / "index.html"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(doc, encoding="utf-8")


def tiles(entries):
    """entries: (label, sub, href or None)"""
    out = ['<div class="tiles">']
    for label, sub, href in entries:
        if href:
            out.append(f'<a class="tile" href="{e(href)}"><b>{e(label)}</b><small>{e(sub)}</small></a>')
        else:
            out.append(f'<div class="tile off"><b>{e(label)}</b><small>{e(sub)}</small></div>')
    out.append("</div>")
    return "\n".join(out)


TYPE_KEY = {"notes": "notes", "exercise": "exercises", "quiz": "quiz"}


def collect(lang, typ, cls=None):
    """All items of a type: list of (class, subject, chapter, item, href)."""
    out = []
    for c in cat["classes"]:
        if cls is not None and c["num"] != cls:
            continue
        for s in c["subjects"]:
            for ch in s["chapters"]:
                for it in ch["items"]:
                    if it["type"] == typ and it.get(lang):
                        href = it[lang].get("href") or f"/{lang}/{cls_slug(c['num'])}/{s['slug']}/{ch_slug(ch['num'])}/{it['slug']}/"
                        out.append((c, s, ch, it, href))
    return out


def item_list(lang, rows, show_class=True):
    t = T[lang]
    if not rows:
        return f'<p class="note">{e(t["none_yet"])}</p>'
    out = ['<ul class="list">']
    for c, s, ch, it, href in rows:
        where = (f"{t['cls']} {c['num']} · " if show_class else "") + f"{s['name'][lang]} · {t['ch']} {ch['num']}: {ch['name'][lang]}"
        out.append(f'<li><a href="{e(href)}"><b>{e(it["title"][lang])}</b><small>{e(where)}</small></a></li>')
    out.append("</ul>")
    return "\n".join(out)


def paper_list(lang, papers):
    t = T[lang]
    if not papers:
        return f'<p class="note">{e(t["none_yet"])}</p>'
    return '<ul class="list">' + "".join(
        f'<li><a href="/{lang}/papers/{p["slug"]}/"><b>{e(p["title"][lang])}</b><small>{e(t["cls"])} {p["class"]}</small></a></li>'
        for p in papers) + "</ul>"


def pdf_list(lang, pdfs):
    t = T[lang]
    if not pdfs:
        return f'<p class="note">{e(t["none_yet"])}</p>'
    return '<ul class="list">' + "".join(
        f'<li><a href="/{lang}/pdf/{p["slug"]}/"><b>{e(p["title"][lang])}</b><small>{e(t["cls"])} {p["class"]}'
        + (f' · {e(t["ch"])} {p["chapter"]}' if p.get("chapter") else "") + '</small></a></li>'
        for p in pdfs) + "</ul>"


def type_buttons(lang):
    t = T[lang]
    return (f'<h2>{e(t["sections"])}</h2><div class="tiles">'
            f'<a class="tile" href="/{lang}/notes/"><b>📘 {e(t["notes"])}</b><small>{len(collect(lang, "notes"))} {e(t["ready"])}</small></a>'
            f'<a class="tile" href="/{lang}/quiz/"><b>🎯 {e(t["quiz"])}</b><small>{len(collect(lang, "quiz"))} {e(t["ready"])}</small></a>'
            f'<a class="tile" href="/{lang}/papers/"><b>📝 {e(t["papers"])}</b><small>{len([p for p in cat["papers"] if p.get(lang)])} {e(t["ready"])}</small></a>'
            f'<a class="tile" href="/{lang}/pdf/"><b>📄 {e(t["pdfs"])}</b><small>{len([p for p in cat.get("pdfs", []) if p.get(lang)])} {e(t["ready"])}</small></a>'
            '</div>')


def patch_quiz(lang):
    """Add a small site bar to hand-made quiz pages (idempotent)."""
    t = T[lang]
    for c, s, ch, it, href in collect(lang, "quiz"):
        f = SITE / href.strip("/") / "index.html"
        if not f.exists():
            continue
        txt = f.read_text(encoding="utf-8")
        if "id=\"sitebar\"" in txt:
            continue
        chpath = f"/{lang}/{cls_slug(c['num'])}/{s['slug']}/{ch_slug(ch['num'])}/"
        bar = (f'<div id="sitebar" style="background:#1f5aa6;padding:10px 14px;font:600 15px system-ui,sans-serif;display:flex;justify-content:space-between">'
               f'<a href="{chpath}" style="color:#fff;text-decoration:none">{e(t["back_ch"])}</a>'
               f'<a href="/{lang}/quiz/" style="color:#fff;text-decoration:none">{e(t["quiz"])}</a></div>')
        txt = txt.replace("<body>", "<body>" + bar, 1)
        f.write_text(txt, encoding="utf-8")


def clean():
    for p in SITE.rglob("index.html"):
        if GEN in p.read_text(encoding="utf-8", errors="ignore")[:200]:
            p.unlink()


def build():
    clean()
    for lang in LANGS:
        t = T[lang]
        home = f"/{lang}/"
        # medium home: classes
        ents = []
        for c in cat["classes"]:
            has = class_has(c, lang)
            ents.append((f"{t['cls']} {c['num']}", t["ready"] if has else t["soon"],
                         f"/{lang}/{cls_slug(c['num'])}/" if c["subjects"] else None))
        ents.sort(key=lambda x: x[2] is None or x[1] == t["soon"])  # available classes first
        papers = [p for p in cat["papers"] if p.get(lang)]
        body = f'<p class="lead">{e(t["tag"])}</p><h2>{e(t["choose_cls"])}</h2>' + tiles(ents) + type_buttons(lang)
        page(lang, home, f"{cat['site']['name'][lang]} — {t['medium']}", None, body)
        page(lang, f"/{lang}/notes/", f"📘 {t['notes']}", [(t["home"], home), (t["notes"], f"/{lang}/notes/")], item_list(lang, collect(lang, "notes")))
        page(lang, f"/{lang}/quiz/", f"🎯 {t['quiz']}", [(t["home"], home), (t["quiz"], f"/{lang}/quiz/")], item_list(lang, collect(lang, "quiz")))
        page(lang, f"/{lang}/papers/", f"📝 {t['papers']}", [(t["home"], home), (t["papers"], f"/{lang}/papers/")], paper_list(lang, papers))
        pdfs = [p for p in cat.get("pdfs", []) if p.get(lang)]
        page(lang, f"/{lang}/pdf/", f"📄 {t['pdfs']}", [(t["home"], home), (t["pdfs"], f"/{lang}/pdf/")], pdf_list(lang, pdfs))
        for p in pdfs:
            ppath = f"/{lang}/pdf/{p['slug']}/"
            d = p[lang]
            b = "<ul>" + "".join(f"<li>{e(x)}</li>" for x in d.get("summary", [])) + "</ul>"
            b += (f'<div class="btns"><a class="btn" href="{e(d["pdf"])}">{e(t["pdf_view"])}</a>'
                  f'<a class="btn ghost" href="{e(d["pdf"])}" download>{e(t["pdf_dl"])}</a></div>')
            other = "en" if lang == "hi" else "hi"
            page(lang, ppath, p["title"][lang], [(t["home"], home), (t["pdfs"], f"/{lang}/pdf/"), (p["title"][lang], ppath)], b, switch_to=f"/{other}/pdf/")

        for c in cat["classes"]:
            if not c["subjects"]:
                continue
            cname = f"{t['cls']} {c['num']}"
            cpath = f"/{lang}/{cls_slug(c['num'])}/"
            body = f"<h2>{e(t['choose_sub'])}</h2>" + tiles([
                (s["name"][lang], t["ready"] if subject_has(s, lang) else t["soon"],
                 f"{cpath}{s['slug']}/" if s["chapters"] else None) for s in c["subjects"]])
            cp = [p for p in cat["papers"] if p["class"] == c["num"] and p.get(lang)]
            body = body.replace(f"<h2>{e(t['choose_sub'])}</h2>", f"<h2>{e(t['subjects'])}</h2>", 1)
            body += f'<h2>📘 {e(t["notes"])}</h2>' + item_list(lang, collect(lang, "notes", c["num"]), False)
            body += f'<h2>🎯 {e(t["quiz"])}</h2>' + item_list(lang, collect(lang, "quiz", c["num"]), False)
            body += f'<h2>📝 {e(t["papers"])}</h2>' + paper_list(lang, cp)
            body += f'<h2>📄 {e(t["pdfs"])}</h2>' + pdf_list(lang, [p for p in cat.get("pdfs", []) if p["class"] == c["num"] and p.get(lang)])
            page(lang, cpath, cname, [(t["home"], home), (cname, cpath)], body)

            for s in c["subjects"]:
                if not s["chapters"]:
                    continue
                spath = f"{cpath}{s['slug']}/"
                rows = ['<ol class="chapters">']
                for ch in s["chapters"]:
                    has = chapter_has(ch, lang)
                    href = f"{spath}{ch_slug(ch['num'])}/"
                    badge = f'<span class="ok">{e(t["ready"])}</span>' if has else f'<span class="soon">{e(t["soon"])}</span>'
                    rows.append(f'<li><a href="{e(href)}"><span class="n">{ch["num"]}</span> {e(ch["name"][lang])}</a>{badge}</li>')
                rows.append("</ol>")
                title = f"{cname} · {s['name'][lang]}"
                page(lang, spath, title, [(t["home"], home), (cname, cpath), (s["name"][lang], spath)],
                     f"<h2>{e(t['choose_ch'])}</h2>" + "\n".join(rows))

                for ch in s["chapters"]:
                    chpath = f"{spath}{ch_slug(ch['num'])}/"
                    chname = f"{t['ch']} {ch['num']}: {ch['name'][lang]}"
                    crumbs = [(t["home"], home), (cname, cpath), (s["name"][lang], spath), (f"{t['ch']} {ch['num']}", chpath)]
                    avail = [i for i in ch["items"] if item_available(i, lang)]
                    if avail:
                        body = ""
                        for typ in ("notes", "exercise", "quiz"):
                            grp = [i for i in avail if i["type"] == typ]
                            if grp:
                                body += f"<h2>{ICON[typ]} {e(t[TYPE_KEY[typ]])}</h2>" + tiles(
                                    [(i["title"][lang], "", i[lang].get("href") or f"{chpath}{i['slug']}/") for i in grp])
                    else:
                        body = f'<p class="note">{e(t["items_none"])}</p>'
                    page(lang, chpath, chname, crumbs, body)

                    pages_items = [i for i in avail if not i[lang].get("href")]
                    for k, it in enumerate(pages_items):
                        ipath = f"{chpath}{it['slug']}/"
                        d = it[lang]
                        b = ""
                        if d.get("summary"):
                            b += f"<h2>{e(t['inside'])}</h2><ul>" + "".join(f"<li>{e(x)}</li>" for x in d["summary"]) + "</ul>"
                        if d.get("answers"):
                            b += f"<h2>{e(t['answers'])}</h2><ol class='answers'>" + "".join(
                                f"<li>{e(x)}</li>" for x in d["answers"]) + "</ol>"
                        if d.get("pdf"):
                            b += (f'<div class="btns"><a class="btn" href="{e(d["pdf"])}">{e(t["pdf_view"])}</a>'
                                  f'<a class="btn ghost" href="{e(d["pdf"])}" download>{e(t["pdf_dl"])}</a></div>')
                        nav = '<div class="pn">'
                        nav += f'<a href="{chpath}{pages_items[k-1]["slug"]}/">{e(t["prev"])}</a>' if k > 0 else "<span></span>"
                        nav += f'<a href="{chpath}{pages_items[k+1]["slug"]}/">{e(t["next"])}</a>' if k + 1 < len(pages_items) else "<span></span>"
                        b += nav + "</div>"
                        other = "en" if lang == "hi" else "hi"
                        sw = ("/" + other + ipath[3:]) if it.get(other) else ("/" + other + chpath[3:])
                        page(lang, ipath, f"{cname} {s['name'][lang]} · {it['title'][lang]}",
                             crumbs + [(it["title"][lang], ipath)], b, switch_to=sw)

        for p in cat["papers"]:
            if not p.get(lang):
                continue
            ppath = f"/{lang}/papers/{p['slug']}/"
            d = p[lang]
            b = "<ul>" + "".join(f"<li>{e(x)}</li>" for x in d.get("summary", [])) + "</ul>"
            if d.get("disclaimer"):
                b = ('<div style="background:#fff5e6;border-left:4px solid #f08c00;padding:10px 14px;border-radius:8px;margin:12px 0">'
                     f'<b>⚠️ अस्वीकरण:</b> {e(d["disclaimer"])}</div>') + b
            b += (f'<div class="btns"><a class="btn" href="{e(d["pdf"])}">{e(t["pdf_view"])}</a>'
                  f'<a class="btn ghost" href="{e(d["pdf"])}" download>{e(t["pdf_dl"])}</a></div>')
            other = "en" if lang == "hi" else "hi"
            sw = ("/" + other + ppath[3:]) if p.get(other) else f"/{other}/"
            page(lang, ppath, p["title"][lang], [(t["home"], home), (t["papers"], f"/{lang}/papers/"), (p["title"][lang], ppath)], b, switch_to=sw)

    for lang in LANGS:
        patch_quiz(lang)
    # root: choose medium
    root = f"""<!doctype html>
{GEN}
<html lang="hi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>MP Board हल | MP Board Solutions</title>
<meta name="description" content="{e(T['hi']['tag'])} | {e(T['en']['tag'])}">
<link rel="stylesheet" href="/assets/style.css"></head><body>
<header class="top"><span class="brand">MP Board हल</span></header>
<main><h1>माध्यम चुनिए <small>Choose your medium</small></h1>
<div class="tiles big"><a class="tile" href="/hi/"><b>हिंदी माध्यम</b><small>कक्षा 1–12</small></a>
<a class="tile" href="/en/"><b>English Medium</b><small>Class 1–12</small></a></div>
<p class="lead">{e(T['hi']['tag'])}</p></main>
<footer>© {e(cat['site']['author']['hi'])}</footer></body></html>
"""
    (SITE / "index.html").write_text(root, encoding="utf-8")
    nf = root.replace("माध्यम चुनिए <small>Choose your medium</small>", "पेज नहीं मिला <small>Page not found</small>")
    (SITE / "404.html").write_text(nf, encoding="utf-8")


INFO = [
    ("about", "हमारे बारे में", "MP Board हल क्या है, किसके लिए है और यहाँ की सामग्री कैसे तैयार होती है।", """
<p><b>MP Board हल</b> मध्यप्रदेश बोर्ड (MPBSE) के विद्यार्थियों के लिए एक निःशुल्क शैक्षिक वेबसाइट है। यहाँ NCERT/MP Board पाठ्यपुस्तकों पर आधारित <b>चरणबद्ध हल, नोट्स, सूत्र-सारणी, ऑनलाइन क्विज़ और अभ्यास प्रश्नपत्र</b> सरल हिंदी में दिए जाते हैं।</p>
<p>MP Board कक्षा 9 और 10 में गणित की पाठ्यपुस्तक NCERT की ही है, जो CBSE में भी पढ़ाई जाती है। इसलिए यहाँ के हल MP Board, NCERT और CBSE — तीनों के विद्यार्थियों के काम आते हैं।</p>
<h2>हमारा उद्देश्य</h2>
<p>हर विद्यार्थी, चाहे गाँव में हो या शहर में, बिना किसी शुल्क के अच्छी गुणवत्ता की अध्ययन सामग्री पा सके और हर प्रश्न को समझकर हल करना सीखे, केवल उत्तर रटना नहीं।</p>
<h2>सामग्री कैसे तैयार होती है</h2>
<ul><li>हर हल में पहले <b>“ज्ञात है”</b> और <b>“ज्ञात करना है”</b> लिखा जाता है।</li>
<li>कोई चरण नहीं छोड़ा जाता; जहाँ सूत्र या सर्वसमिका लगे, उसका नाम लिखा जाता है।</li>
<li>सामग्री एक अनुभवी गणित शिक्षक द्वारा तैयार और जाँची जाती है।</li></ul>
<h2>अभी क्या उपलब्ध है</h2>
<p>फ़िलहाल कक्षा 9 और 10 गणित की सामग्री उपलब्ध है; अन्य कक्षाएँ और विषय धीरे-धीरे जोड़े जा रहे हैं।</p>
<p><a href="/hi/author/">लेखक परिचय</a> · <a href="/hi/contact/">संपर्क</a></p>"""),
    ("author", "लेखक परिचय", "educationdew.com की सामग्री MP Board कक्षा 9 और 10 के अनुभवी गणित शिक्षक द्वारा तैयार की जाती है।", """
<p>educationdew.com की सामग्री मध्यप्रदेश के एक <b>अनुभवी गणित शिक्षक</b> द्वारा तैयार की जाती है, जो MP Board की <b>कक्षा 9 और 10</b> को गणित पढ़ाते हैं।</p>
<p>इस वेबसाइट के सभी हल, नोट्स, क्विज़ और अभ्यास प्रश्नपत्र उन्हीं के मार्गदर्शन में तैयार किए जाते हैं। कक्षा में विद्यार्थियों को जहाँ सबसे अधिक कठिनाई आती है, उन्हीं बातों को ध्यान में रखकर हर हल चरणबद्ध लिखा जाता है।</p>
<h2>लेखन के नियम</h2>
<ul><li>पाठ्यपुस्तक के प्रश्न और आकृतियाँ हूबहू।</li><li>हर पंक्ति में एक ही चरण, स्पष्ट संरेखण के साथ।</li><li>उत्तरों की गणना से जाँच।</li></ul>
<p><a href="/hi/about/">हमारे बारे में</a> · <a href="/hi/contact/">संपर्क</a></p>"""),
    ("contact", "संपर्क करें", "MP Board हल से संपर्क: सुझाव, त्रुटि की सूचना या सामग्री का अनुरोध।", """
<p>किसी हल में त्रुटि दिखे, कोई अध्याय या प्रश्नपत्र चाहिए, या कोई सुझाव देना हो, तो हमें अवश्य बताएँ। आपका हर सुझाव सामग्री को बेहतर बनाता है।</p>
<div style="background:#fff5e6;border-left:4px solid #f08c00;padding:10px 14px;border-radius:8px;margin:12px 0"><p><b>ईमेल:</b> जल्द जोड़ा जाएगा।</p></div>
<p>संदेश में कृपया कक्षा, विषय, अध्याय और प्रश्न संख्या लिखें, ताकि हम जल्दी सुधार कर सकें।</p>"""),
    ("privacy", "गोपनीयता नीति", "MP Board हल की गोपनीयता नीति: कौन-सी जानकारी ली जाती है और कैसे उपयोग होती है।", """
<p><i>अंतिम अद्यतन: 2026-11-03</i></p>
<p>MP Board हल (educationdew.com) आपकी गोपनीयता का सम्मान करता है। यह नीति बताती है कि इस वेबसाइट पर कौन-सी जानकारी ली जाती है।</p>
<h2>1. हम क्या जानकारी लेते हैं</h2>
<p>वेबसाइट पढ़ने के लिए किसी पंजीकरण या लॉगिन की आवश्यकता नहीं है। हम आपसे नाम, फ़ोन या ईमेल जैसी कोई व्यक्तिगत जानकारी नहीं माँगते।</p>
<h2>2. सर्वर लॉग</h2>
<p>वेबसाइट Cloudflare पर होस्ट है। सुरक्षा और सेवा चलाने के लिए होस्टिंग प्रदाता सामान्य तकनीकी जानकारी (जैसे IP पता, ब्राउज़र का प्रकार, देखा गया पेज और समय) अपने लॉग में रख सकता है।</p>
<h2>3. क्विज़</h2>
<p>ऑनलाइन क्विज़ के उत्तर आपके ही ब्राउज़र में जाँचे जाते हैं; वे हमारे पास नहीं भेजे जाते।</p>
<h2>4. कुकीज़ और विज्ञापन</h2>
<p>अभी यह वेबसाइट विज्ञापन या ट्रैकिंग कुकीज़ का उपयोग नहीं करती। भविष्य में विज्ञापन (जैसे Google AdSense) या विश्लेषण सेवाएँ जोड़ी गईं तो वे तीसरे पक्ष कुकीज़ का उपयोग कर सकती हैं; तब यह नीति अद्यतन की जाएगी।</p>
<h2>5. बाहरी लिंक</h2>
<p>दूसरी वेबसाइटों के लिंक पर उनकी अपनी गोपनीयता नीति लागू होती है।</p>
<h2>6. बच्चों की गोपनीयता</h2>
<p>यह वेबसाइट विद्यार्थियों के लिए है और उनसे जानबूझकर कोई व्यक्तिगत जानकारी नहीं ली जाती।</p>
<h2>7. परिवर्तन</h2>
<p>इस नीति में बदलाव होने पर इसी पेज पर नई तारीख के साथ अद्यतन किया जाएगा। प्रश्न हों तो <a href="/hi/contact/">संपर्क</a> करें।</p>"""),
    ("disclaimer", "अस्वीकरण", "MP Board हल का अस्वीकरण: यह आधिकारिक MPBSE वेबसाइट नहीं है।", """
<div style="background:#fff5e6;border-left:4px solid #f08c00;padding:10px 14px;border-radius:8px;margin:12px 0"><p><b>यह मध्यप्रदेश माध्यमिक शिक्षा मंडल (MPBSE) या NCERT की आधिकारिक वेबसाइट नहीं है।</b> आधिकारिक सूचना, परिणाम और समय-सारणी के लिए केवल <a href="https://mpbse.mp.gov.in/" rel="noopener">mpbse.mp.gov.in</a> देखें।</p></div>
<ul><li>यहाँ दिए गए हल, नोट्स और अभ्यास प्रश्नपत्र केवल अध्ययन और अभ्यास के लिए हैं। अभ्यास प्रश्नपत्र “मॉडल पेपर” हैं, बोर्ड के वास्तविक प्रश्नपत्र नहीं।</li>
<li>सामग्री को सही रखने का पूरा प्रयास किया जाता है, फिर भी त्रुटि संभव है। कोई त्रुटि दिखे तो <a href="/hi/contact/">हमें बताएँ</a>।</li>
<li>पाठ्यपुस्तकों के प्रश्न शिक्षा के उद्देश्य से उद्धृत हैं; उनका स्वत्वाधिकार संबंधित प्रकाशकों का है।</li>
<li>इस सामग्री के उपयोग से होने वाली किसी हानि के लिए वेबसाइट उत्तरदायी नहीं है।</li></ul>"""),
    ("terms", "उपयोग की शर्तें", "MP Board हल के उपयोग की शर्तें।", """
<p><i>अंतिम अद्यतन: 2026-11-03</i></p>
<ul><li>यह वेबसाइट विद्यार्थियों और शिक्षकों के निजी, गैर-व्यावसायिक अध्ययन के लिए निःशुल्क है।</li>
<li>हल, नोट्स, आलेख और प्रश्नपत्र © educationdew.com। कक्षा में पढ़ाने या विद्यार्थियों से साझा करने के लिए लिंक भेजें; सामग्री को अपनी वेबसाइट, ऐप या पुस्तक में बिना अनुमति कॉपी न करें।</li>
<li>सामग्री “जैसी है” उपलब्ध कराई जाती है; विवरण के लिए <a href="/hi/disclaimer/">अस्वीकरण</a> देखें।</li>
<li>वेबसाइट का उपयोग करने पर आप इन शर्तों और <a href="/hi/privacy/">गोपनीयता नीति</a> से सहमत होते हैं।</li></ul>"""),
]


def info_pages():
    for slug, title, desc, body in INFO:
        path = f"/hi/{slug}/"
        page("hi", path, title, [(T["hi"]["home"], "/hi/"), (title, path)], body, switch_to="/en/")
        f = SITE / "hi" / slug / "index.html"
        d = f.read_text(encoding="utf-8")
        d = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{e(desc)}">', d, 1)
        f.write_text(d, encoding="utf-8")


if __name__ == "__main__":
    build()
    info_pages()
    print("built", sum(1 for _ in SITE.rglob("index.html")), "pages")
