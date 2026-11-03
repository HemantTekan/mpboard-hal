import os,sys,json,base64,mimetypes,subprocess,blake3,pathlib,urllib.request
A="1f56a0aa6f2d247a2e9c0c1cfc73c2e7";P="mpboard-hal";SITE=pathlib.Path(sys.argv[1])
subprocess.run([sys.executable, str(pathlib.Path(__file__).with_name("seo.py")), sys.argv[1]], check=True)
def jwt():
    r=subprocess.run(["curl","-s",f"https://api.cloudflare.com/client/v4/accounts/{A}/pages/projects/{P}/upload-token"],capture_output=True,text=True)
    return json.loads(r.stdout)["result"]["jwt"]
J=jwt()
noproxy=urllib.request.build_opener(urllib.request.ProxyHandler({}))
def direct(path,body):
    req=urllib.request.Request("https://api.cloudflare.com/client/v4"+path,data=json.dumps(body).encode(),method="POST",headers={"Authorization":"Bearer "+J,"Content-Type":"application/json"})
    return json.loads(noproxy.open(req,timeout=120).read())
files={};manifest={}
for f in sorted(SITE.rglob("*")):
    if not f.is_file(): continue
    b64=base64.b64encode(f.read_bytes()).decode()
    h=blake3.blake3((b64+f.suffix.lstrip(".")).encode()).hexdigest()[:32]
    rel="/"+str(f.relative_to(SITE))
    manifest[rel]=h; files[h]=(b64,mimetypes.guess_type(f.name)[0] or "application/octet-stream")
r=direct("/pages/assets/check-missing",{"hashes":list(files)}); missing=r["result"]
print("files",len(files),"missing",len(missing))
batch=[];size=0
def flush():
    global batch,size
    if batch:
        r=direct("/pages/assets/upload",batch); assert r["success"],r
    batch=[];size=0
for h in missing:
    b64,ct=files[h]
    if size+len(b64)>40_000_000: flush()
    batch.append({"key":h,"value":b64,"metadata":{"contentType":ct},"base64":True}); size+=len(b64)
flush()
r=direct("/pages/assets/upsert-hashes",{"hashes":list(files)}); print("upsert",r["success"])
json.dump(manifest,open("/tmp/manifest.json","w"))
r=subprocess.run(["curl","-s","-X","POST",f"https://api.cloudflare.com/client/v4/accounts/{A}/pages/projects/{P}/deployments",
  "-F","manifest=</tmp/manifest.json","-F","branch=main"],capture_output=True,text=True)
d=json.loads(r.stdout); print(d["success"],d["errors"],(d.get("result") or {}).get("url"),(d.get("result") or {}).get("latest_stage"))
