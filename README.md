# mpboard-hal
NCERT and MP BOARD Textbook Solutions, Class 1 to 12. Both Hindi and English Medium. Quiz and Previous Year Question Paper Solutions.

© Hemant Kumar Tekan. All rights reserved.

## Structure
- `catalog.json` — every class, subject, chapter and item (notes / exercise / quiz / paper) with Hindi and English titles.
- `site/` — the published website (Cloudflare Pages output directory). PDFs and quiz pages live here at their final URLs.
- `tools/build.py` — generates all menu and solution pages from `catalog.json`. Run `python3 tools/build.py` after editing the catalog.

URL pattern: `/hi/class-09/maths/chapter-04/exercise-4-1/` and `/en/...` (same path, different medium).

## Cloudflare Pages
Framework preset: None · Build command: (empty) · Build output directory: `site`
