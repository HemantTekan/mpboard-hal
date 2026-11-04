#!/usr/bin/env python3
"""Deploy the educationdew Worker: static assets from site/ + API code from worker/src + D1 migrations.
Usage: python3 tools/deploy_worker.py site
Single source of truth for names/ids/bindings: wrangler.jsonc at the repo root (wrangler-compatible).
Steps: brand.py + seo.py -> apply new migrations/*.sql to D1 (tracked in d1_migrations, same table wrangler uses)
-> upload assets -> upload modules + bindings. Uses the cloudflare service (api.cloudflare.com) bound to the vault token."""
import sys, json, base64, mimetypes, subprocess, pathlib, urllib.request, blake3, uuid, re
here = pathlib.Path(__file__).parent; ROOT = here.parent
CFG = json.loads(re.sub(r"^\s*//.*$", "", (ROOT / "wrangler.jsonc").read_text(), flags=re.M))
A = CFG["account_id"]; NAME = CFG["name"]; SITE = pathlib.Path(sys.argv[1])
API = "https://api.cloudflare.com/client/v4"
for s in ("brand.py", "seo.py"):
    subprocess.run([sys.executable, str(here / s), str(SITE)], check=True)

def proxied(method, path, body=None, ctype="application/json", raw=None):
    args = ["curl", "-s", "-X", method, API + path]
    if raw is not None:
        args += ["-H", f"Content-Type: {ctype}", "--data-binary", "@-"]
        r = subprocess.run(args, input=raw, capture_output=True)
    elif body is not None:
        args += ["-H", "Content-Type: application/json", "--data-binary", "@-"]
        r = subprocess.run(args, input=json.dumps(body).encode(), capture_output=True)
    else:
        r = subprocess.run(args, capture_output=True)
    return json.loads(r.stdout)

def d1(sql, params=None):
    db = CFG["d1_databases"][0]["database_id"]
    r = proxied("POST", f"/accounts/{A}/d1/database/{db}/query", {"sql": sql, **({"params": params} if params else {})})
    if not r.get("success"): sys.exit(f"D1 failed: {r.get('errors')} :: {sql[:80]}")
    return r["result"]

# 1) migrations
d1("CREATE TABLE IF NOT EXISTS d1_migrations (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE, applied_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP)")
done_m = {row["name"] for row in d1("SELECT name FROM d1_migrations")[0]["results"]}
for mf in sorted((ROOT / CFG["d1_databases"][0].get("migrations_dir", "migrations")).glob("*.sql")):
    if mf.name in done_m: continue
    d1(mf.read_text()); d1("INSERT INTO d1_migrations (name) VALUES (?)", [mf.name]); print("migration applied", mf.name)

noproxy = urllib.request.build_opener(urllib.request.ProxyHandler({}))
def multipart(fields):
    b = uuid.uuid4().hex; out = b""
    for name, (val, ct, fn) in fields.items():
        disp = f'form-data; name="{name}"' + (f'; filename="{fn}"' if fn else "")
        out += f"--{b}\r\nContent-Disposition: {disp}\r\nContent-Type: {ct}\r\n\r\n".encode() + val + b"\r\n"
    return out + f"--{b}--\r\n".encode(), f"multipart/form-data; boundary={b}"

manifest, files = {}, {}
for f in sorted(SITE.rglob("*")):
    if not f.is_file() or f.name.startswith(".") or f.name in ("_worker.js",): continue
    data = f.read_bytes(); b64 = base64.b64encode(data).decode()
    h = blake3.blake3((b64 + f.suffix.lstrip(".")).encode()).hexdigest()[:32]
    manifest["/" + str(f.relative_to(SITE))] = {"hash": h, "size": len(data)}
    files[h] = (b64, mimetypes.guess_type(f.name)[0] or "application/octet-stream")
r = proxied("POST", f"/accounts/{A}/workers/scripts/{NAME}/assets-upload-session", {"manifest": manifest})
if not r.get("success"): sys.exit(f"session failed: {r.get('errors')}")
jwt = r["result"]["jwt"]; buckets = r["result"].get("buckets") or []
print("files", len(manifest), "buckets", len(buckets))
done = jwt
for bucket in buckets:
    body, ct = multipart({h: (files[h][0].encode(), files[h][1], h) for h in bucket})
    req = urllib.request.Request(f"{API}/accounts/{A}/workers/assets/upload?base64=true", data=body, method="POST",
                                 headers={"Authorization": "Bearer " + jwt, "Content-Type": ct})
    res = json.loads(noproxy.open(req, timeout=180).read())
    if not res.get("success"): sys.exit(f"upload failed: {res.get('errors')}")
    if res["result"].get("jwt"): done = res["result"]["jwt"]
# 3) code + bindings
src = (ROOT / CFG["main"]).parent; main = (ROOT / CFG["main"]).relative_to(src).as_posix()
ac = CFG["assets"]
meta = {"main_module": main, "keep_bindings": ["secret_text"], "compatibility_date": CFG["compatibility_date"],
        "bindings": [{"type": "assets", "name": ac["binding"]}] +
                    [{"type": "d1", "name": d["binding"], "id": d["database_id"]} for d in CFG.get("d1_databases", [])] +
                    [{"type": "r2_bucket", "name": b["binding"], "bucket_name": b["bucket_name"]} for b in CFG.get("r2_buckets", [])],
        "assets": {"jwt": done, "config": {k: ac[k] for k in ("html_handling", "not_found_handling", "run_worker_first") if k in ac}}}
parts = {"metadata": (json.dumps(meta).encode(), "application/json", None)}
for f in sorted(src.rglob("*.js")):
    rel = f.relative_to(src).as_posix(); parts[rel] = (f.read_bytes(), "application/javascript+module", rel)
body, ct = multipart(parts)
r = proxied("PUT", f"/accounts/{A}/workers/scripts/{NAME}", raw=body, ctype=ct)
print("deploy", r.get("success"), r.get("errors"))
