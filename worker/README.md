# educationdew Worker

- Static site: `site/` (assets layer, no code runs). Only `/api/*` reaches `worker/src/index.js`.
- Config (names, ids, bindings): `wrangler.jsonc`, single source of truth.
- Database: D1 `educationdew-db`, binding `DB`. Schema change = new file `migrations/000N_name.sql` (never edit an applied one). Deploy applies new ones automatically (tracked in `d1_migrations`).
- New API feature: add `worker/src/routes/<feature>.js` and one line in `ROUTES`.
- Files later (R2): add `r2_buckets` to `wrangler.jsonc`; the deploy script binds it.
- Deploy: `pip install blake3 cairosvg && python3 tools/deploy_worker.py site`.

## API
- `GET /api/health`
- `POST /api/quiz/attempts` `{quiz, name?, score, total, wrong:[0-based q numbers], seconds?}`
- `GET /api/quiz/leaderboard?quiz=hi/class-09/maths/chapter-03&days=30&limit=10`
- `GET /api/quiz/stats?quiz=...` (attempts, avg %, 5 most-missed questions)

Quiz pages use `/assets/quiz-api.js` (`EDQuiz.submit`, `EDQuiz.board`).
