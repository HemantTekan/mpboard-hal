#!/usr/bin/env python3
"""Deploy site/ as a Cloudflare Worker with static assets (no script).
Usage: python3 tools/deploy_worker.py site
Runs brand.py + seo.py first. Uses the cloudflare service (api.cloudflare.com) bound to the vault token."""
import sys, json, base64, mimetypes, subprocess, pathlib, urllib.request, blake3, uuid
A = "1f56a0aa6f2d247a2e9c0c1cfc73c2e7"; NAME = "educationdew"; SITE = pathlib.Path(sys.argv[1])
API = "https://api.cloudflare.com/client/v4"
here = pathlib.Path(__file__).parent
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
meta = {"compatibility_date": "2026-11-04",
        "assets": {"jwt": done, "config": {"html_handling": "auto-trailing-slash", "not_found_handling": "404-page"}}}
body, ct = multipart({"metadata": (json.dumps(meta).encode(), "application/json", None)})
r = proxied("PUT", f"/accounts/{A}/workers/scripts/{NAME}", raw=body, ctype=ct)
print("deploy", r.get("success"), r.get("errors"))
