#!/usr/bin/env python3
"""SEO pass over the built site: canonical, Open Graph, JSON-LD, robots meta,
sitemap.xml and robots.txt. Idempotent: replaces its own block on every run.
Usage: python3 tools/seo.py site
"""
import html, json, pathlib, re, subprocess, sys, datetime

BASE = "https://educationdew.com"
SITE_NAME = "MP Board हल"
AUTHOR = "हेमंत कुमार टेकन"
AUTHOR_DESC = "गणित शिक्षक, MP Board कक्षा 9 और 10"
START, END = "<!--seo-->", "<!--/seo-->"

root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "site")
repo = root.resolve().parent


def lastmod(p):
    try:
        out = subprocess.run(["git", "-C", str(repo), "log", "-1", "--format=%cs", "--", str(p.resolve())],
                             capture_output=True, text=True).stdout.strip()
        if out:
            return out
    except Exception:
        pass
    return datetime.date.today().isoformat()


def text_of(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s))).strip()


def url_for(p):
    rel = p.relative_to(root).as_posix()
    if rel == "index.html":
        return BASE + "/"
    if rel.endswith("/index.html"):
        return BASE + "/" + rel[:-len("index.html")]
    return BASE + "/" + rel


entries = []
for p in sorted(root.rglob("*.html")):
    s = p.read_text(encoding="utf-8")
    s = re.sub(re.escape(START) + r".*?" + re.escape(END), "", s, flags=re.S)
    rel = p.relative_to(root).as_posix()
    url = url_for(p)
    title_m = re.search(r"<title>(.*?)</title>", s, re.S)
    title = text_of(title_m.group(1)) if title_m else SITE_NAME
    desc_m = re.search(r'<meta name="description" content="([^"]*)"', s)
    desc = html.unescape(desc_m.group(1)) if desc_m else ""
    main_m = re.search(r"<main.*?</main>", s, re.S)
    main_txt = text_of(main_m.group(0)) if main_m else ""

    # thin / placeholder pages: keep out of the index until real content exists
    thin = (rel == "404.html" or rel.startswith("en/")
            or ("जल्द आ रहे हैं" in main_txt and len(main_txt) < 300))

    head = []
    if thin:
        head.append('<meta name="robots" content="noindex,follow">')
    else:
        head.append(f'<link rel="canonical" href="{url}">')
        head.append('<meta name="robots" content="index,follow,max-image-preview:large">')
    head.append(f'<meta name="author" content="{AUTHOR}">')
    head += [
        '<meta property="og:type" content="website">',
        f'<meta property="og:site_name" content="{SITE_NAME}">',
        f'<meta property="og:title" content="{html.escape(title, quote=True)}">',
        f'<meta property="og:description" content="{html.escape(desc, quote=True)}">',
        f'<meta property="og:url" content="{url}">',
        '<meta property="og:locale" content="hi_IN">',
        f'<meta property="og:image" content="{BASE}/assets/og.png">',
        '<meta name="twitter:card" content="summary_large_image">',
    ]

    if not thin:
        ld = []
        cr = re.search(r'<nav class="crumbs">(.*?)</nav>', s, re.S)
        if cr:
            items = []
            for i, m in enumerate(re.finditer(r'<a href="([^"]+)">(.*?)</a>|<span>(.*?)</span>', cr.group(1))):
                name = text_of(m.group(2) or m.group(3))
                it = {"@type": "ListItem", "position": i + 1, "name": name}
                it["item"] = BASE + m.group(1) if m.group(1) else url
                items.append(it)
            if items:
                ld.append({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items})
        if "/exercise-" in rel or "/notes/" in rel or "/formulas/" in rel or "/papers/" in rel and rel.count("/") > 2 or "/quiz/" in rel and rel.count("/") > 2:
            cls = re.search(r"class-(\d+)", rel)
            lr = {
                "@context": "https://schema.org",
                "@type": "Quiz" if "/quiz/" in rel else "LearningResource",
                "name": title.split(" | ")[0],
                "description": desc,
                "url": url,
                "inLanguage": "hi",
                "isAccessibleForFree": True,
                "educationalLevel": f"कक्षा {int(cls.group(1))}" if cls else "माध्यमिक",
                "educationalUse": "practice" if "/quiz/" in rel else "study",
                "learningResourceType": ("Quiz" if "/quiz/" in rel else "Notes" if "/notes/" in rel else
                                         "Formula sheet" if "/formulas/" in rel else
                                         "Practice paper" if "/papers/" in rel else "Step-by-step solutions"),
                "about": {"@type": "Thing", "name": "गणित"},
                "author": {"@type": "Person", "name": AUTHOR, "description": AUTHOR_DESC},
                "publisher": {"@type": "Organization", "name": SITE_NAME, "url": BASE + "/"},
                "dateModified": lastmod(p),
            }
            ld.append(lr)
        if rel == "hi/index.html":
            ld.append({"@context": "https://schema.org", "@type": "WebSite", "name": SITE_NAME, "url": BASE + "/hi/",
                       "inLanguage": "hi", "author": {"@type": "Person", "name": AUTHOR, "description": AUTHOR_DESC}})
        for obj in ld:
            head.append('<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False) + "</script>")
        entries.append((url, lastmod(p)))

    block = START + "".join(head) + END
    s = s.replace("</title>", "</title>" + block, 1) if "</title>" in s else s.replace("</head>", block + "</head>", 1)
    # accessible names for graphs/figures that have no label yet
    s = re.sub(r"<svg(?![^>]*aria-label)(?![^>]*aria-hidden)([^>]*class='graph')", r"<svg role='img' aria-label='आलेख'\1", s)
    p.write_text(s, encoding="utf-8")

sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for u, d in entries:
    sm.append(f"<url><loc>{u}</loc><lastmod>{d}</lastmod></url>")
sm.append("</urlset>")
(root / "sitemap.xml").write_text("\n".join(sm) + "\n", encoding="utf-8")
(root / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {BASE}/sitemap.xml\n", encoding="utf-8")
print(f"seo: {len(entries)} indexable pages in sitemap")
