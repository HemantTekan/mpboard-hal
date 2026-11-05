# mpboard-hal

NCERT and MP Board textbook solutions, Class 1 to 12, Hindi and English medium. Quizzes and previous-year question paper solutions.

© educationdew.com. All rights reserved.

## Structure

```
catalog.json              every class, subject, chapter and item (notes / exercise / quiz), papers and PDFs,
                          with Hindi and English titles
site/                     the published website (generated pages + hand-made content, committed)
tools/make.py             the pipeline: build (generators -> brand -> seo -> check) and deploy
tools/build.py            menu, chapter, item, PDF and info pages from catalog.json
tools/solutions/
  common.py               page template, CSS, KaTeX pre-rendering, shared helpers
                          (lines, eqs, given, ans, q, part, formula, p, ok, qt, close, ...)
  mixed_cells.py          lines / eqs whose cells mix Hindi \text{...} with TeX (chapters 5+)
  geometry.py             दिया है / सिद्ध करना है boxes, उपपत्ति rows, r / T / A symbols, SVG fig()
  class10_chN.py          one file per chapter: only its questions, answers and chapter-specific figures
tools/katex_render.js     server-side KaTeX (node + tools/vendor/katex.min.js); pages ship no maths JS
tools/check.py            link / KaTeX / <title> checks over site/
tools/brand.py, seo.py    build passes run by make.py after the generators (brand header, nav, hero, icons;
                          canonical, OG, JSON-LD, sitemap.xml, robots.txt); idempotent, importable
tools/deploy_worker.py    upload step only (D1 migrations, assets, Worker code); never modifies site/
tools/deploy_cloudflare.py  alias for `make.py deploy`
worker/, migrations/, wrangler.jsonc   Cloudflare Worker API + D1 database (quiz scores); see worker/README.md
```

URL pattern: `/hi/class-10/maths/chapter-04/exercise-4-1/` and `/en/...` (same path, other medium).

## Build

```
python3 tools/make.py                  # everything: menus + all solutions -> brand -> seo -> check
python3 tools/make.py menus            # only pages from catalog.json, then brand -> seo -> check
python3 tools/make.py solutions 12     # only chapter 12 solutions, then brand -> seo -> check
```

Needs Python 3, `git` and `node` (for KaTeX). Every run leaves `site/` in its final form, exactly what a deploy
uploads, and running it twice changes nothing. Review `git diff site/` and commit `site/` with the source change,
so the repository always holds what is live.

Dates (JSON-LD `dateModified`, sitemap `<lastmod>`) come from git history in `seo.py`: a page's date is the UTC
day of the commit since which its rendered output is unchanged; a page that differs from the last commit gets
today's UTC date (`SOURCE_DATE_EPOCH` overrides "today"). Commits that only regenerate pages without changing
their rendered output do not move dates.

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
3. `python3 tools/make.py` (includes the checks), then review the pages locally (`python3 -m http.server -d site`).

## Add a PDF to the /hi/pdf/ section

1. Add an entry to the `pdfs` list in `catalog.json`:

   ```json
   {"slug": "class-10-ch12-sutra-sarni", "class": 10, "subject": "maths", "chapter": 12,
    "title": {"hi": "कक्षा 10 · अध्याय 12 — सूत्र-सारणी", "en": "Formula Sheet"},
    "hi": {"pdf": "sutra-sarni.pdf", "summary": ["पहला बिंदु", "दूसरा बिंदु"]}}
   ```
2. Put the file at `site/hi/pdf/<slug>/<hi.pdf>` (e.g. `site/hi/pdf/class-10-ch12-sutra-sarni/sutra-sarni.pdf`).
3. `python3 tools/make.py menus` (includes the checks).

## Deploy

One command: full build -> check (aborts on any problem) -> upload `site/` to the Cloudflare Worker `educationdew`
(static assets + API, D1 migrations), serving educationdew.com:

```
pip install --user blake3 cairosvg
python3 tools/make.py deploy
```

The upload sends `site/` byte for byte and never modifies it. Commit the built `site/` (before or right after
deploying; the command warns if it differs from the last commit). `python3 tools/deploy_cloudflare.py site` is
an alias for the same command; `python3 tools/deploy_worker.py site` uploads without building.
