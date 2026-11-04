# mpboard-hal

NCERT and MP Board textbook solutions, Class 1 to 12, Hindi and English medium. Quizzes and previous-year question paper solutions.

© educationdew.com. All rights reserved.

## Structure

```
catalog.json              every class, subject, chapter and item (notes / exercise / quiz), papers and PDFs,
                          with Hindi and English titles
site/                     the published website (generated pages + hand-made content, committed)
tools/make.py             one command: regenerates menus and all solution pages into site/
tools/build.py            menu, chapter, item, PDF and info pages from catalog.json
tools/solutions/
  common.py               page template, CSS, KaTeX pre-rendering, shared helpers
                          (lines, eqs, given, ans, q, part, formula, p, ok, qt, close, ...)
  mixed_cells.py          lines / eqs whose cells mix Hindi \text{...} with TeX (chapters 5+)
  geometry.py             दिया है / सिद्ध करना है boxes, उपपत्ति rows, r / T / A symbols, SVG fig()
  class10_chN.py          one file per chapter: only its questions, answers and chapter-specific figures
tools/katex_render.js     server-side KaTeX (node + tools/vendor/katex.min.js); pages ship no maths JS
tools/check.py            link / KaTeX / <title> checks over site/
tools/brand.py, seo.py    post-processing applied at deploy time (brand header, canonical, JSON-LD,
                          sitemap.xml, robots.txt); both idempotent
tools/deploy_cloudflare.py  deploy command (runs tools/deploy_worker.py)
worker/, migrations/, wrangler.jsonc   Cloudflare Worker API + D1 database (quiz scores); see worker/README.md
```

URL pattern: `/hi/class-10/maths/chapter-04/exercise-4-1/` and `/en/...` (same path, other medium).

## Build

```
python3 tools/make.py                  # menus + all solution pages
python3 tools/make.py menus            # only pages from catalog.json
python3 tools/make.py solutions 12     # only chapter 12 solutions
```

Needs Python 3 and `node` (for KaTeX). Output is deterministic; review `git diff site/` before committing.
A deploy runs `brand.py` + `seo.py` on `site/` in place, so pages committed after a deploy can carry that post-processing;
regenerating rewrites them without it, which is expected (the next deploy applies it again).

## Check

```
python3 tools/check.py        # exit code 1 if anything is wrong
```

Reports broken internal links (href/src to local paths that do not exist, including absolute links to educationdew.com), KaTeX errors or unrendered `\( ... \)`, and pages without a `<title>`.

## Add a new chapter (solutions)

1. Create `tools/solutions/class10_chN.py`. Start from an existing chapter of the same kind:

   ```python
   import sys, pathlib, math
   sys.path.insert(0, str(pathlib.Path(__file__).parent))
   from common import *        # page, lines, eqs, given, ans, part, formula, m, p, ok, qt, ...
   from mixed_cells import *   # if equation cells contain Hindi \text{...}
   from geometry import *      # if the chapter has proofs or figures (gp, pf, fig, T, A, r)

   BASE = "/hi/class-10/maths/chapter-NN/"
   CH = "अध्याय का नाम"

   EX1 = []
   EX1.append((qt("प्रश्न का पाठ ..."), given("...", "...") + lines("x", "2+3", "5") + ans("x = 5")))

   page(BASE, N, CH, "exercise-N-1", "प्रश्नावली N.1", "कक्षा 10 गणित · अध्याय N: ... · 1 प्रश्न", EX1,
        (BASE, "अध्याय N"), ("/hi/class-10/maths/", "सभी अध्याय"))
   ```

   Keep only content and chapter-specific figure helpers in the chapter file; anything two chapters need goes into `common.py`, `mixed_cells.py` or `geometry.py`.
2. Add the exercise items to the chapter in `catalog.json` (classes → subjects → chapters → items):

   ```json
   {"slug": "exercise-N-1", "type": "exercise",
    "title": {"hi": "प्रश्नावली N.1", "en": "Exercise N.1"},
    "hi": {"href": "/hi/class-10/maths/chapter-NN/exercise-N-1/"}}
   ```
3. `python3 tools/make.py && python3 tools/check.py`, then review the pages locally (`python3 -m http.server -d site`).

## Add a PDF to the /hi/pdf/ section

1. Add an entry to the `pdfs` list in `catalog.json`:

   ```json
   {"slug": "class-10-ch12-sutra-sarni", "class": 10, "subject": "maths", "chapter": 12,
    "title": {"hi": "कक्षा 10 · अध्याय 12 — सूत्र-सारणी", "en": "Formula Sheet"},
    "hi": {"pdf": "sutra-sarni.pdf", "summary": ["पहला बिंदु", "दूसरा बिंदु"]}}
   ```
2. Put the file at `site/hi/pdf/<slug>/<hi.pdf>` (e.g. `site/hi/pdf/class-10-ch12-sutra-sarni/sutra-sarni.pdf`).
3. `python3 tools/make.py menus && python3 tools/check.py`.

## Deploy

Deploys `site/` to the Cloudflare Worker `educationdew` (static assets + API, D1 migrations), serving educationdew.com:

```
pip install --user blake3 cairosvg
python3 tools/deploy_cloudflare.py site
```

The deploy step applies `brand.py` and `seo.py` to `site/` in place before uploading; building never uploads anything.
