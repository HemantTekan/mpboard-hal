export function json(data, status = 200, headers = {}) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store", ...headers },
  });
}
export const error = (status, code, extra = {}) => json({ ok: false, error: code, ...extra }, status);

// Only accept writes from our own pages (simple CSRF/abuse guard).
const ORIGINS = ["https://educationdew.com", "https://www.educationdew.com", "https://educationdew.hemanttekan.workers.dev"];
export function sameSite(request) {
  const o = request.headers.get("origin");
  return !o || ORIGINS.includes(o);
}

export async function readJson(request, maxBytes = 8192) {
  const len = Number(request.headers.get("content-length") || 0);
  if (len > maxBytes) return null;
  const text = await request.text();
  if (text.length > maxBytes) return null;
  try { return JSON.parse(text); } catch { return null; }
}

// Nickname: trim, collapse spaces, strip control/markup chars, max 24 chars.
export function cleanName(s) {
  if (typeof s !== "string") return "";
  return s.replace(/[\u0000-\u001f<>"'`\\]/g, "").replace(/\s+/g, " ").trim().slice(0, 24);
}

// Quiz ids are site paths like "hi/class-09/maths/chapter-03".
export const QUIZ_ID = /^[a-z]{2}\/class-\d{2}\/[a-z-]+\/chapter-\d{2}(\/[a-z0-9-]+)?$/;
