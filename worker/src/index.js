// educationdew Worker: static site is served by the assets layer; this code runs first on every request
// (assets.config.run_worker_first = true). Add a feature = add a file in ./routes and one line in ROUTES.
import * as quiz from "./routes/quiz.js";
import * as admin from "./routes/admin.js";
import { json, error } from "./lib/http.js";

const ROUTES = [
  ["GET", /^\/api\/health$/, async (req, env) => {
    const r = await env.DB.prepare("SELECT 1 AS ok").first();
    return json({ ok: r && r.ok === 1, service: "educationdew", time: new Date().toISOString() });
  }],
  ["POST", /^\/api\/quiz\/attempts$/, quiz.createAttempt],
  ["GET", /^\/api\/quiz\/leaderboard$/, quiz.leaderboard],
  ["GET", /^\/api\/quiz\/stats$/, quiz.stats],
  ["GET", /^\/api\/admin\/overview$/, admin.overview],
  ["GET", /^\/api\/admin\/quiz$/, admin.quizDetail],
  ["POST", /^\/api\/admin\/attempts\/delete$/, admin.deleteAttempt],
];

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    // One canonical address for SEO: www.educationdew.com -> educationdew.com (301), API excepted.
    if (url.hostname === "www.educationdew.com" && !url.pathname.startsWith("/api/")) {
      url.hostname = "educationdew.com";
      return Response.redirect(url.toString(), 301);
    }
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
