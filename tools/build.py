#!/usr/bin/env python3
"""Build the static site from catalog.json into site/.

Run from repo root:  python3 tools/build.py
- Content files (PDFs, quiz HTML) live directly under site/ at their final paths.
- Every generated page carries GEN marker; old generated pages are removed first,
  hand-made pages (e.g. quizzes) are never touched.
"""
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
               tag="MP Board और NCERT पाठ्यपुस्तकों के चरणबद्ध हल, चित्र सहित",
               notes="नोट्स", quiz="क्विज़", exercises="प्रश्नावली के हल", subjects="विषय", sections="सामग्री के प्रकार",
               none_yet="अभी उपलब्ध नहीं, जल्द आ रहा है।", back_ch="← अध्याय पर लौटें"),
    "en": dict(home="Home", cls="Class", ch="Chapter", soon="Coming soon", choose_cls="Choose your class",
               choose_sub="Choose a subject", choose_ch="Choose a chapter", pdf_view="View PDF", pdf_dl="Download PDF",
               answers="Answers at a glance", q="Q", prev="← Previous", next="Next →", papers="Question papers (with solutions)",
               medium="English Medium", other="हिंदी माध्यम", inside="What's inside", open_quiz="Start quiz",
               ready="Available", items_none="Solutions for this chapter are coming soon.",
               tag="Step-by-step solutions for MP Board and NCERT textbooks, with diagrams",
               notes="Notes", quiz="Quiz", exercises="Exercise Solutions", subjects="Subjects", sections="Browse by type",
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
<link rel="stylesheet" href="/assets/style.css">
</head><body>
<header class="top"><a class="brand" href="/{lang}/">{e(site_name)}</a>
<a class="switch" href="{e(sw)}">{e(t['other'])}</a></header>
<main>{crumb_html}
<h1>{e(title)}</h1>
{body}
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


def type_buttons(lang):
    t = T[lang]
    return (f'<h2>{e(t["sections"])}</h2><div class="tiles">'
            f'<a class="tile" href="/{lang}/notes/"><b>📘 {e(t["notes"])}</b><small>{len(collect(lang, "notes"))} {e(t["ready"])}</small></a>'
            f'<a class="tile" href="/{lang}/quiz/"><b>🎯 {e(t["quiz"])}</b><small>{len(collect(lang, "quiz"))} {e(t["ready"])}</small></a>'
            f'<a class="tile" href="/{lang}/papers/"><b>📝 {e(t["papers"])}</b><small>{len([p for p in cat["papers"] if p.get(lang)])} {e(t["ready"])}</small></a>'
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
        papers = [p for p in cat["papers"] if p.get(lang)]
        body = f'<p class="lead">{e(t["tag"])}</p><h2>{e(t["choose_cls"])}</h2>' + tiles(ents) + type_buttons(lang)
        page(lang, home, f"{cat['site']['name'][lang]} — {t['medium']}", None, body)
        page(lang, f"/{lang}/notes/", f"📘 {t['notes']}", [(t["home"], home), (t["notes"], f"/{lang}/notes/")], item_list(lang, collect(lang, "notes")))
        page(lang, f"/{lang}/quiz/", f"🎯 {t['quiz']}", [(t["home"], home), (t["quiz"], f"/{lang}/quiz/")], item_list(lang, collect(lang, "quiz")))
        page(lang, f"/{lang}/papers/", f"📝 {t['papers']}", [(t["home"], home), (t["papers"], f"/{lang}/papers/")], paper_list(lang, papers))

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


if __name__ == "__main__":
    build()
    print("built", sum(1 for _ in SITE.rglob("index.html")), "pages")
