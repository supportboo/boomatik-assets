"""C01-IG-C1 carousel: upload | validate | create | poll. Scheduled, never publishNow. Log has no key."""
import json, os, sys, time, uuid, urllib.request
L01 = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, os.path.join(L01, "_zernio_tools"))
from zapi import call

LZ = os.path.join(L01, "lanzamiento")
OUT = os.path.join(LZ, "micro", "C01-IG-C1")
LOG = os.path.join(LZ, "micro", "programado.json")
MEDIA = os.path.join(OUT, "media.json")
IG = "6ae2dd79f681a077b3f325cb"  # BRANDOOERS profile, @brandooers_skillup
BOOMATIK = {"6add01b6b63f43d5d66d1850"}
WHEN = "2026-11-04T10:00:00.000Z"  # mié 4-nov-2026 11:00 Europe/Madrid (CET)
D0_UTC = "2026-11-02T16:00:00.000Z"

src = next(p for p in json.load(open(os.path.join(LZ, "primeras", "primeras.json"), encoding="utf-8"))["piezas"]
           if p["id"] == "C01-IG-C1")
assert len(src["imagenes"]) == len(src["alt"]) == 8


def body():
    urls = json.load(open(MEDIA, encoding="utf-8"))
    return {
        "content": src["texto"] + "\n\n" + src["hashtags"],
        "mediaItems": [{"type": "image", "url": urls[i], "altText": src["alt"][i]} for i in range(8)],
        "platforms": [{"platform": "instagram", "accountId": IG,
                       "platformSpecificData": {"isAiGenerated": bool(src["etiqueta_ia"])}}],
        "scheduledFor": WHEN,
    }


def guard(b):
    assert len(b["platforms"]) == 1 and b["platforms"][0]["accountId"] == IG not in BOOMATIK
    assert "publishNow" not in b and b["scheduledFor"] == WHEN >= D0_UTC
    assert len(b["content"]) <= 2200 and "boomatik" not in b["content"].lower() and "€" not in b["content"]


mode = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
if mode == "upload":
    out = []
    for rel in src["imagenes"]:
        path = os.path.join(LZ, rel); size = os.path.getsize(path)
        s, p = call("POST", "/media/presign", {"filename": os.path.basename(path), "contentType": "image/png", "size": size})
        assert s == 200, (s, p)
        with open(path, "rb") as f:
            req = urllib.request.Request(p["uploadUrl"], data=f, method="PUT",
                                         headers={"Content-Type": "image/png", "Content-Length": str(size)})
            with urllib.request.urlopen(req, timeout=600) as r:
                print(os.path.basename(path), "PUT", r.status, size)
        out.append(p["publicUrl"])
    json.dump(out, open(MEDIA, "w", encoding="utf-8"), indent=1)
    sys.exit()

b = body(); guard(b)
log = json.load(open(LOG, encoding="utf-8")) if os.path.exists(LOG) else {"profile": "BRANDOOERS", "pieces": {}}
e = log["pieces"].setdefault("C01-IG-C1", {})
e.update({"scheduledFor_utc": WHEN, "madrid": "mié 4-nov-2026 11:00", "accountId": IG, "fieldsSent": b})
if mode == "validate":
    s, r = call("POST", "/tools/validate/post", b)
    e["validate"] = {"http": s, "response": r}; print("validate", s, json.dumps(r, ensure_ascii=False))
elif mode == "create":
    if e.get("postId"):
        raise SystemExit("already created " + e["postId"])
    idem = str(uuid.uuid4())
    s, r = call("POST", "/posts", b, headers={"Idempotency-Key": idem})
    post = r.get("post", {})
    e.update({"idempotencyKey": idem, "createHttp": s, "postId": post.get("_id"), "status": post.get("status"),
              "scheduledFor_returned": post.get("scheduledFor"), "createResponse": r})
    print("create", s, post.get("_id"), post.get("status"), post.get("scheduledFor"),
          "" if post else json.dumps(r, ensure_ascii=False)[:1500])
elif mode == "poll":
    s, r = call("GET", f"/posts/{e['postId']}")
    post = r.get("post", r)
    e.update({"status": post.get("status"), "scheduledFor_returned": post.get("scheduledFor"),
              "polledAt": time.strftime("%Y-%m-%dT%H:%M:%S")})
    print("poll", s, post.get("status"), post.get("scheduledFor"), [p.get("status") for p in post.get("platforms", [])])
json.dump(log, open(LOG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
