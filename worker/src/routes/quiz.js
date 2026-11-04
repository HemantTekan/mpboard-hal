import { json, error, readJson, cleanName, sameSite, QUIZ_ID } from "../lib/http.js";

// POST /api/quiz/attempts  {quiz, name, score, total, wrong:[question numbers], seconds}
export async function createAttempt(request, env) {
  if (!sameSite(request)) return error(403, "forbidden");
  const b = await readJson(request);
  if (!b) return error(400, "bad_json");
  const quiz = String(b.quiz || "");
  const total = Number(b.total), score = Number(b.score);
  if (!QUIZ_ID.test(quiz)) return error(400, "bad_quiz");
  if (!Number.isInteger(total) || total < 1 || total > 100) return error(400, "bad_total");
  if (!Number.isInteger(score) || score < 0 || score > total) return error(400, "bad_score");
  const wrong = Array.isArray(b.wrong) ? b.wrong.filter((n) => Number.isInteger(n) && n >= 0 && n < 100).slice(0, total) : [];
  if (wrong.length !== total - score) return error(400, "bad_wrong");
  const seconds = Number.isInteger(b.seconds) && b.seconds >= 0 && b.seconds < 86400 ? b.seconds : null;
  const name = cleanName(b.name);
  const r = await env.DB.prepare(
    "INSERT INTO quiz_attempts (quiz_id, nickname, score, total, wrong, seconds) VALUES (?1, ?2, ?3, ?4, ?5, ?6)"
  ).bind(quiz, name || null, score, total, JSON.stringify(wrong), seconds).run();
  return json({ ok: true, id: r.meta.last_row_id }, 201);
}

// GET /api/quiz/leaderboard?quiz=...&days=30&limit=10  -> best score per nickname
export async function leaderboard(request, env, { url }) {
  const quiz = url.searchParams.get("quiz") || "";
  if (!QUIZ_ID.test(quiz)) return error(400, "bad_quiz");
  const days = Math.min(Math.max(parseInt(url.searchParams.get("days") || "30", 10) || 30, 1), 365);
  const limit = Math.min(Math.max(parseInt(url.searchParams.get("limit") || "10", 10) || 10, 1), 50);
  const { results } = await env.DB.prepare(
    `SELECT nickname AS name, MAX(score) AS score, total, MIN(created_at) AS at
       FROM quiz_attempts
      WHERE quiz_id = ?1 AND nickname IS NOT NULL AND created_at >= unixepoch() - ?2 * 86400
      GROUP BY nickname, total
      ORDER BY score DESC, at ASC
      LIMIT ?3`
  ).bind(quiz, days, limit).all();
  return json({ ok: true, quiz, days, rows: results }, 200, { "cache-control": "public, max-age=60" });
}

// GET /api/quiz/stats?quiz=...  -> attempts, average, most-missed questions (for the teacher)
export async function stats(request, env, { url }) {
  const quiz = url.searchParams.get("quiz") || "";
  if (!QUIZ_ID.test(quiz)) return error(400, "bad_quiz");
  const [summary, missed] = await env.DB.batch([
    env.DB.prepare("SELECT COUNT(*) AS attempts, ROUND(AVG(score * 100.0 / total), 1) AS avg_pct FROM quiz_attempts WHERE quiz_id = ?1").bind(quiz),
    env.DB.prepare(
      `SELECT CAST(j.value AS INTEGER) AS question, COUNT(*) AS wrong
         FROM quiz_attempts a, json_each(a.wrong) j
        WHERE a.quiz_id = ?1 GROUP BY question ORDER BY wrong DESC LIMIT 5`
    ).bind(quiz),
  ]);
  return json({ ok: true, quiz, ...summary.results[0], most_missed: missed.results }, 200, { "cache-control": "public, max-age=300" });
}
