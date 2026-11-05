#!/usr/bin/env python3
"""SEO pass over the built site: canonical, Open Graph, JSON-LD, robots meta, footer links,
sitemap.xml and robots.txt. Idempotent: replaces its own <!--seo--> block on every run.
Part of the build: tools/make.py runs it after brand.py.

  python3 tools/seo.py [site]        (standalone; normally use tools/make.py)

As a module: page_seo(text, rel, lastmod) -> (text, sitemap entry or None); run(site) -> indexable pages.

Dates (JSON-LD dateModified and sitemap <lastmod>) come from git, but only from commits that changed what the
page renders to: each committed version of site/<rel> is normalised (brand + this SEO pass with a fixed date)
and compared with the page being built.
  - page differs from the committed HEAD version (or is new/untracked) -> today's date (UTC)
  - otherwise -> UTC date of the oldest commit since which the rendered page has been unchanged
So a commit that only regenerates or re-post-processes pages (same rendered output) never moves a date, and
the date written before committing a real change equals the date after committing it (if committed the same
UTC day). SOURCE_DATE_EPOCH overrides "today". Without git, every page gets today.
"""
import datetime, html, json, os, pathlib, re, subprocess, sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import brand

BASE = "https://educationdew.com"
SITE_NAME = "MP Board हल"
AUTHOR = "educationdew.com"
AUTHOR_DESC = "MP Board, NCERT और CBSE कक्षा 9–10 गणित के चरणबद्ध हल"
START, END = "<!--seo-->", "<!--/seo-->"

DEFAULT_SITE = pathlib.Path(__file__).resolve().parents[1] / "site"


def text_of(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s))).strip()


def url_for(rel):
    if rel == "index.html":
        return BASE + "/"
    if rel.endswith("/index.html"):
        return BASE + "/" + rel[:-len("index.html")]
    return BASE + "/" + rel


def page_seo(s, rel, lastmod):
    """Pure transform of one page. rel = path relative to site/ (posix); lastmod() -> "YYYY-MM-DD", called only
    for indexable pages. Returns (new text, (url, lastmod) for the sitemap or None)."""
    s = re.sub(re.escape(START) + r".*?" + re.escape(END), "", s, flags=re.S)
    url = url_for(rel)
    title_m = re.search(r"<title>(.*?)</title>", s, re.S)
    title = text_of(title_m.group(1)) if title_m else SITE_NAME
    desc_m = re.search(r'<meta name="description" content="([^"]*)"', s)
    desc = html.unescape(desc_m.group(1)) if desc_m else ""
    main_m = re.search(r"<main.*?</main>", s, re.S)
    main_txt = text_of(re.sub(r'<p class="boards".*?</p>', "", main_m.group(0), flags=re.S)) if main_m else ""

    # thin / placeholder pages: keep out of the index until real content exists
    entry = None
    thin = (rel == "404.html" or rel.startswith("en/") or rel.startswith("teacher/")
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
        if "/exercise-" in rel or "/notes/" in rel or "/formulas/" in rel or "/pdf/" in rel or "/papers/" in rel and rel.count("/") > 2 or "/quiz/" in rel and rel.count("/") > 2:
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
                "author": {"@type": "Organization", "name": AUTHOR, "url": BASE + "/"},
                "keywords": "MP Board, MPBSE, NCERT, CBSE, गणित, हल",
                "publisher": {"@type": "Organization", "name": SITE_NAME, "url": BASE + "/", "logo": {"@type": "ImageObject", "url": BASE + "/assets/icon-512.png"}},
                "dateModified": lastmod(),
            }
            ld.append(lr)
        if rel in ("index.html", "hi/index.html"):
            ld.append({"@context": "https://schema.org", "@type": "Organization", "name": "educationdew", "alternateName": SITE_NAME,
                       "url": BASE + "/", "logo": BASE + "/assets/icon-512.png"})
        if rel == "hi/index.html":
            ld.append({"@context": "https://schema.org", "@type": "WebSite", "name": SITE_NAME, "url": BASE + "/hi/",
                       "inLanguage": "hi", "description": AUTHOR_DESC, "author": {"@type": "Organization", "name": AUTHOR, "url": BASE + "/"}})
        for obj in ld:
            head.append('<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False) + "</script>")
        entry = (url, lastmod())

    block = START + "".join(head) + END
    s = s.replace("</title>", "</title>" + block, 1) if "</title>" in s else s.replace("</head>", block + "</head>", 1)
    # accessible names for graphs/figures that have no label yet
    s = re.sub(r"<svg(?![^>]*aria-label)(?![^>]*aria-hidden)([^>]*class='graph')", r"<svg role='img' aria-label='आलेख'\1", s)
    s = re.sub(r"<!--foot-->.*?<!--/foot-->", "", s, flags=re.S)
    links = ('<!--foot--><nav class="footlinks" style="display:block;margin-bottom:6px;font-size:13px;line-height:2"><a href="/hi/about/">हमारे बारे में</a> · <a href="/hi/author/">लेखक</a> · '
             '<a href="/hi/contact/">संपर्क</a> · <a href="/hi/privacy/">गोपनीयता नीति</a> · <a href="/hi/disclaimer/">अस्वीकरण</a> · '
             '<a href="/hi/terms/">उपयोग की शर्तें</a></nav><!--/foot-->')
    s = re.sub(r"(<footer[^>]*>)", lambda m: m.group(1) + links, s, count=1)
    return s, entry


def today():
    epoch = os.environ.get("SOURCE_DATE_EPOCH")
    t = datetime.datetime.fromtimestamp(int(epoch), datetime.timezone.utc) if epoch else datetime.datetime.now(datetime.timezone.utc)
    return t.date().isoformat()


def rendered(s, rel):
    """What a version of a page renders to after the post-processing passes, independent of dates."""
    b = brand.brand_html(s, rel)
    return page_seo(b if b is not None else s, rel, lambda: "0000-00-00")[0]


class GitDates:
    def __init__(self, site):
        self.site = pathlib.Path(site).resolve()
        self.repo = None
        r = subprocess.run(["git", "-C", str(self.site), "rev-parse", "--show-toplevel"], capture_output=True, text=True)
        if r.returncode == 0:
            self.repo = pathlib.Path(r.stdout.strip())
        self.cache = {}

    def _git(self, *args):
        r = subprocess.run(["git", "-C", str(self.repo), *args], capture_output=True)
        return r.stdout if r.returncode == 0 else None

    def lastmod(self, rel, current):
        if rel not in self.cache:
            self.cache[rel] = self._lastmod(rel, current)
        return self.cache[rel]

    def _lastmod(self, rel, current):
        """current = the page as it will be published (already branded); see module docstring."""
        if self.repo is None:
            return today()
        path = (self.site / rel).relative_to(self.repo).as_posix()
        log = (self._git("log", "--format=%H %ct", "--", path) or b"").decode().split()
        commits = list(zip(log[0::2], log[1::2]))  # newest first
        cur = rendered(current, rel)
        when = None
        for sha, ct in commits:
            old = self._git("show", f"{sha}:{path}")
            if old is None:
                break  # file deleted in this commit
            if rendered(old.decode("utf-8"), rel) != cur:
                break
            when = ct
        if when is None:
            return today()
        return datetime.datetime.fromtimestamp(int(when), datetime.timezone.utc).date().isoformat()


def run(site=DEFAULT_SITE):
    site = pathlib.Path(site)
    dates = GitDates(site)
    entries = []
    for p in sorted(site.rglob("*.html")):
        rel = p.relative_to(site).as_posix()
        s = p.read_text(encoding="utf-8")
        out, entry = page_seo(s, rel, lambda: dates.lastmod(rel, s))
        if entry:
            entries.append(entry)
        if out != s:
            p.write_text(out, encoding="utf-8")
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u, d in entries:
        sm.append(f"<url><loc>{u}</loc><lastmod>{d}</lastmod></url>")
    sm.append("</urlset>")
    (site / "sitemap.xml").write_text("\n".join(sm) + "\n", encoding="utf-8")
    (site / "robots.txt").write_text(f"User-agent: *\nAllow: /\nDisallow: /teacher/\nDisallow: /api/\n\nSitemap: {BASE}/sitemap.xml\n", encoding="utf-8")
    return len(entries)


if __name__ == "__main__":
    print(f"seo: {run(sys.argv[1] if len(sys.argv) > 1 else DEFAULT_SITE)} indexable pages in sitemap")
