#!/usr/bin/env python3
"""Regenerate the site from source in one command (run from anywhere).

  python3 tools/make.py                  menus + all solution pages
  python3 tools/make.py menus            only the menu/item pages from catalog.json (tools/build.py)
  python3 tools/make.py solutions        only the solution pages (every tools/solutions/classNN_chM.py)
  python3 tools/make.py solutions 10 12  only Class 10 chapters 10 and 12

Output goes to site/. Deploying is a separate, explicit step:
  python3 tools/deploy_cloudflare.py site   (applies brand.py + seo.py, then uploads)
"""
import pathlib, re, subprocess, sys

TOOLS = pathlib.Path(__file__).resolve().parent
ROOT = TOOLS.parent
SOLUTIONS = TOOLS / "solutions"


def chapter_scripts(only=None):
    """Solution generators sorted by (class, chapter); `only` filters by chapter number."""
    found = []
    for f in SOLUTIONS.glob("class*_ch*.py"):
        m = re.fullmatch(r"class(\d+)_ch(\d+)\.py", f.name)
        if m and (not only or int(m.group(2)) in only):
            found.append(((int(m.group(1)), int(m.group(2))), f))
    return [f for _, f in sorted(found)]


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


def main(argv):
    cmd = argv[0] if argv else "all"
    if cmd == "all" and len(argv) <= 1:
        menus()
        solutions()
    elif cmd == "menus" and len(argv) == 1:
        menus()
    elif cmd == "solutions":
        solutions({int(a) for a in argv[1:]} or None)
    else:
        sys.exit(__doc__)
    print("done. Next: python3 tools/check.py")


if __name__ == "__main__":
    main(sys.argv[1:])
