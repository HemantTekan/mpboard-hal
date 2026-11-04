// educationdew Worker: static site is served by the assets layer; only /api/* reaches this code
// (assets.config.run_worker_first = ["/api/*"]). Add a feature = add a file in ./routes and one line in ROUTES.
import * as quiz from "./routes/quiz.js";
import { json, error } from "./lib/http.js";

const ROUTES = [
  ["GET", /^\/api\/health$/, async (req, env) => {
    const r = await env.DB.prepare("SELECT 1 AS ok").first();
    return json({ ok: r && r.ok === 1, service: "educationdew", time: new Date().toISOString() });
  }],
  ["POST", /^\/api\/quiz\/attempts$/, quiz.createAttempt],
  ["GET", /^\/api\/quiz\/leaderboard$/, quiz.leaderboard],
  ["GET", /^\/api\/quiz\/stats$/, quiz.stats],
];

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    if (!url.pathname.startsWith("/api/")) return env.ASSETS.fetch(request);
    if (request.method === "OPTIONS") return new Response(null, { status: 204 });
    for (const [method, re, handler] of ROUTES) {
      const m = url.pathname.match(re);
      if (!m) continue;
      if (request.method !== method) continue;
      try {
        return await handler(request, env, { url, params: m.slice(1), ctx });
      } catch (e) {
        console.error(e && e.stack || e);
        return error(500, "server_error");
      }
    }
    return error(404, "not_found");
  },
};
