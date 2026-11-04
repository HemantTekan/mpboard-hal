import { json, error, QUIZ_ID } from "../lib/http.js";

// Teacher-only endpoints. Auth: "Authorization: Bearer <ADMIN_KEY>" (Worker secret, never in git).
async function authorized(request, env) {
  const key = env.ADMIN_KEY || "";
  const got = (request.headers.get("authorization") || "").replace(/^Bearer\s+/i, "");
  if (!key || !got) return false;
  const enc = new TextEncoder();
  const [a, b] = await Promise.all([crypto.subtle.digest("SHA-256", enc.encode(key)), crypto.subtle.digest("SHA-256", enc.encode(got))]);
  return crypto.subtle.timingSafeEqual(a, b);
}
const guard = (fn) => async (request, env, c) => (await authorized(request, env)) ? fn(request, env, c) : error(401, "unauthorized");
const nocache = { "cache-control": "private, no-store" };

// GET /api/admin/overview -> one row per quiz
export const overview = guard(async (request, env) => {
  const { results } = await env.DB.prepare(
    `SELECT quiz_id AS quiz, COUNT(*) AS attempts,
            SUM(created_at >= unixepoch() - 7 * 86400) AS last7,
            ROUND(AVG(score * 100.0 / total), 1) AS avg_pct,
            MAX(created_at) AS last_at
       FROM quiz_attempts GROUP BY quiz_id ORDER BY last_at DESC`
  ).all();
  return json({ ok: true, quizzes: results }, 200, nocache);
});

// GET /api/admin/quiz?quiz=...&days=30 -> question-wise mistakes + recent attempts + score spread
export const quizDetail = guard(async (request, env, { url }) => {
  const quiz = url.searchParams.get("quiz") || "";
  if (!QUIZ_ID.test(quiz)) return error(400, "bad_quiz");
  const days = Math.min(Math.max(parseInt(url.searchParams.get("days") || "30", 10) || 30, 1), 3650);
  const since = "unixepoch() - ?2 * 86400";
  const [sum, missed, spread, recent] = await env.DB.batch([
    env.DB.prepare(`SELECT COUNT(*) AS attempts, ROUND(AVG(score * 100.0 / total), 1) AS avg_pct, ROUND(AVG(seconds)) AS avg_seconds
                      FROM quiz_attempts WHERE quiz_id = ?1 AND created_at >= ${since}`).bind(quiz, days),
    env.DB.prepare(`SELECT CAST(j.value AS INTEGER) AS question, COUNT(*) AS wrong
                      FROM quiz_attempts a, json_each(a.wrong) j
                     WHERE a.quiz_id = ?1 AND a.created_at >= ${since} GROUP BY question ORDER BY wrong DESC`).bind(quiz, days),
    env.DB.prepare(`SELECT CASE WHEN score * 100 >= total * 80 THEN '80-100' WHEN score * 100 >= total * 60 THEN '60-79'
                                WHEN score * 100 >= total * 40 THEN '40-59' ELSE '0-39' END AS band, COUNT(*) AS n
                      FROM quiz_attempts WHERE quiz_id = ?1 AND created_at >= ${since} GROUP BY band`).bind(quiz, days),
    env.DB.prepare(`SELECT id, nickname AS name, score, total, seconds, created_at AS at
                      FROM quiz_attempts WHERE quiz_id = ?1 AND created_at >= ${since} ORDER BY id DESC LIMIT 50`).bind(quiz, days),
  ]);
  return json({ ok: true, quiz, days, ...sum.results[0], missed: missed.results, spread: spread.results, recent: recent.results }, 200, nocache);
});

// POST /api/admin/attempts/delete {id} -> remove one attempt (e.g. a student asks to remove their name, or junk)
export const deleteAttempt = guard(async (request, env) => {
  let b; try { b = await request.json(); } catch { return error(400, "bad_json"); }
  const id = Number(b && b.id);
  if (!Number.isInteger(id) || id < 1) return error(400, "bad_id");
  const r = await env.DB.prepare("DELETE FROM quiz_attempts WHERE id = ?1").bind(id).run();
  return json({ ok: true, deleted: r.meta.changes }, 200, nocache);
});
