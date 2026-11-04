#!/usr/bin/env python3
"""Sanity checks over the generated site.

  python3 tools/check.py [site]

Reports:
  - broken internal links: href/src pointing at a local path that does not exist in site/
  - KaTeX problems: katex-error spans, "ParseError" text, or \\( ... \\) left unrendered
  - HTML pages without a non-empty <title>
Exit code 0 when clean, 1 when anything is found.
"""
import html, pathlib, re, sys
from urllib.parse import urlsplit, unquote

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = pathlib.Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else ROOT / "site"

ATTR = re.compile(r"""\b(href|src|content)\s*=\s*(?:"([^"]*)"|'([^']*)')""", re.I)
SCRIPT_STYLE = re.compile(r"<(script|style)\b.*?</\1\s*>", re.S | re.I)
COMMENT = re.compile(r"<!--.*?-->", re.S)
SKIP_SCHEMES = ("http:", "https:", "mailto:", "tel:", "data:", "javascript:", "blob:")
OWN_HOSTS = ("educationdew.com", "www.educationdew.com")  # absolute links to our own domain are checked too
WORKER_ROUTES = ("/api/",)  # served by the Worker, not by static assets (wrangler.jsonc run_worker_first)


def target_exists(path):
    """Mirror Workers static assets html_handling 'auto-trailing-slash'."""
    rel = path.lstrip("/")
    p = SITE / rel
    if path.endswith("/"):
        return (p / "index.html").is_file()
    return p.is_file() or (p / "index.html").is_file() or p.with_name(p.name + ".html").is_file()


def page_url(f):
    rel = f.relative_to(SITE).as_posix()
    return "/" + (rel[: -len("index.html")] if rel.endswith("index.html") else rel)


def check_links(f, text):
    bad = []
    base = page_url(f)
    for m in ATTR.finditer(text):
        raw = html.unescape(m.group(2) if m.group(2) is not None else m.group(3)).strip()
        own = urlsplit(raw).hostname in OWN_HOSTS if "//" in raw else False
        if m.group(1).lower() == "content" and not own:  # <meta content=...>: only our own absolute URLs
            continue
        if own:
            raw = urlsplit(raw).path or "/"
        if not raw or raw.startswith("#") or raw.startswith("//") or raw.lower().startswith(SKIP_SCHEMES):
            continue
        if any(c in raw for c in "{}+$`") or " " in raw:  # template fragments, not real URLs
            continue
        path = unquote(urlsplit(raw).path)
        if not path:
            continue
        if not path.startswith("/"):
            path = str(pathlib.PurePosixPath(base if base.endswith("/") else base.rsplit("/", 1)[0] + "/") / path)
            parts = []
            for seg in path.split("/"):
                if seg == "..":
                    parts and parts.pop()
                elif seg != ".":
                    parts.append(seg)
            path = "/".join(parts) + ("/" if raw.endswith("/") else "")
        if path.startswith(WORKER_ROUTES):
            continue
        if not target_exists(path):
            bad.append(raw)
    return bad


def check_katex(text):
    body = SCRIPT_STYLE.sub("", text)
    found = []
    if "katex-error" in body:
        found.append(f"katex-error x{body.count('katex-error')}")
    if "ParseError" in body:
        found.append("ParseError text")
    raw = re.findall(r"\\\((.{0,40})", COMMENT.sub("", body))
    if raw:
        found.append(f"unrendered \\( x{len(raw)} (first: \\({raw[0]}…)")
    return found


def main():
    if not SITE.is_dir():
        sys.exit(f"no site directory: {SITE}")
    links, katex, titles = [], [], []
    pages = sorted(SITE.rglob("*.html"))
    for f in pages:
        text = f.read_text(encoding="utf-8", errors="replace")
        rel = f.relative_to(SITE).as_posix()
        for b in check_links(f, SCRIPT_STYLE.sub("", text)):
            links.append((rel, b))
        for k in check_katex(text):
            katex.append((rel, k))
        t = re.search(r"<title[^>]*>(.*?)</title>", text, re.S | re.I)
        if not t or not t.group(1).strip():
            titles.append(rel)

    print(f"checked {len(pages)} HTML pages in {SITE}")
    print(f"\nbroken internal links: {len(links)}")
    for rel, b in links:
        print(f"  {rel}: {b}")
    print(f"\nKaTeX problems: {len(katex)}")
    for rel, k in katex:
        print(f"  {rel}: {k}")
    print(f"\npages missing <title>: {len(titles)}")
    for rel in titles:
        print(f"  {rel}")
    problems = len(links) + len(katex) + len(titles)
    print("\nOK" if not problems else f"\n{problems} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
