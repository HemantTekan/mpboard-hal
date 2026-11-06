#!/usr/bin/env python3
"""The one pipeline for the site: build, check, deploy (run from anywhere).

  python3 tools/make.py                  build everything: menus + all solutions -> brand -> seo -> check
  python3 tools/make.py menus            only menu/item pages from catalog.json (tools/build.py), then brand -> seo -> check
  python3 tools/make.py solutions        only the solution pages (every tools/solutions/classNN_chM.py), then brand -> seo -> check
  python3 tools/make.py solutions 10 12  only Class 10 chapters 10 and 12, then brand -> seo -> check
  python3 tools/make.py deploy           full build -> check (abort on any problem) -> upload site/ to Cloudflare

site/ always ends up in its final, publishable form (what deploy uploads byte for byte), so commit it after building.
brand.py (header, nav, hero, icons) and seo.py (canonical, OG, JSON-LD, sitemap.xml, robots.txt) are idempotent.
"""
import pathlib, re, subprocess, sys

TOOLS = pathlib.Path(__file__).resolve().parent
ROOT = TOOLS.parent
SITE = ROOT / "site"
SOLUTIONS = TOOLS / "solutions"
sys.path.insert(0, str(TOOLS))
import brand, seo  # noqa: E402


def chapter_scripts(only=None):
    """Solution generators sorted by (class, chapter); `only` filters by chapter number."""
    found = []
    for f in SOLUTIONS.glob("class*_ch*.py"):
        m = re.fullmatch(r"class(\d+)_ch(\d+)\.py", f.name)
        if m and (not only or int(m.group(2)) in only):
            found.append(((int(m.group(1)), int(m.group(2))), f))
    out = [f for _, f in sorted(found)]
    if not only:
        out += sorted(SOLUTIONS.glob("paper_*.py"))
    return out


def run(script):
    r = subprocess.run([sys.executable, str(script)], cwd=ROOT, capture_output=True, text=True)
    if r.returncode != 0:
        sys.stderr.write(r.stdout + r.stderr)
        sys.exit(f"FAILED: {script.relative_to(ROOT)}")
    return r.stdout.strip()


def menus():
    print("menus:", run(TOOLS / "build.py"))


def solutions(only=None):
    scripts = chapter_scripts(only)
    if not scripts:
        sys.exit("no matching tools/solutions/class*_ch*.py")
    for s in scripts:
        # one process per chapter: chapter files are plain scripts with module-level content
        run(s)
        print("solutions:", s.name)


def post():
    print("brand:", brand.run(SITE), "pages")
    print("seo:", seo.run(SITE), "indexable pages in sitemap")


def check():
    r = subprocess.run([sys.executable, str(TOOLS / "check.py"), str(SITE)], cwd=ROOT, capture_output=True, text=True)
    if r.returncode != 0:
        sys.stderr.write(r.stdout + r.stderr)
        sys.exit("CHECK FAILED: see problems above")
    print("check: OK")


def build():
    menus()
    solutions()
    post()
    check()


def deploy():
    build()
    dirty = subprocess.run(["git", "-C", str(ROOT), "status", "--porcelain", "--", "site"], capture_output=True, text=True).stdout
    if dirty.strip():
        print("warning: site/ differs from the last commit; commit it so the repo matches what is live")
    import deploy_worker  # needs blake3; imported only when deploying
    deploy_worker.upload(SITE)


def main(argv):
    cmd = argv[0] if argv else "all"
    if cmd == "all" and len(argv) <= 1:
        build()
    elif cmd == "menus" and len(argv) == 1:
        menus(); post(); check()
    elif cmd == "solutions":
        solutions({int(a) for a in argv[1:]} or None); post(); check()
    elif cmd == "deploy" and len(argv) == 1:
        deploy()
    else:
        sys.exit(__doc__)
    print("done.")


if __name__ == "__main__":
    main(sys.argv[1:])
