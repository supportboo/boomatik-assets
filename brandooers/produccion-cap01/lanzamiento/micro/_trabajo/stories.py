"""C01-IG-H2 / C01-IG-H4 plain-image stories (no stickers): upload | validate | create | poll. Scheduled only."""
import json, os, sys, time, uuid, urllib.request
L01 = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, os.path.join(L01, "_zernio_tools"))
from zapi import call

LZ = os.path.join(L01, "lanzamiento")
MICRO = os.path.join(LZ, "micro")
LOG = os.path.join(MICRO, "programado.json")
IG = "6ae2dd79f681a077b3f325cb"  # BRANDOOERS profile only
BOOMATIK = {"6add01b6b63f43d5d66d1850"}
WHEN = {"C01-IG-H2": ("2026-11-01T20:00:00.000Z", "dom 1-nov-2026 21:00"),  # plan D-1, allowed before D0
        "C01-IG-H4": ("2026-11-04T12:00:00.000Z", "mié 4-nov-2026 13:00")}
P = {x["id"]: x for x in json.load(open(os.path.join(LZ, "primeras", "primeras.json"), encoding="utf-8"))["piezas"]}


def body(pid, url):
    return {"content": "", "mediaItems": [{"type": "image", "url": url}],
            "platforms": [{"platform": "instagram", "accountId": IG,
                           "platformSpecificData": {"contentType": "story", "isAiGenerated": bool(P[pid]["etiqueta_ia"])}}],
            "scheduledFor": WHEN[pid][0]}


def guard(b, pid):
    assert len(b["platforms"]) == 1 and b["platforms"][0]["accountId"] == IG not in BOOMATIK
    assert "publishNow" not in b and b["scheduledFor"] == WHEN[pid][0]


mode = sys.argv[1]
log = json.load(open(LOG, encoding="utf-8"))
for pid in WHEN:
    d = os.path.join(MICRO, pid); os.makedirs(d, exist_ok=True)
    e = log["pieces"].setdefault(pid, {})
    if mode == "upload":
        path = os.path.join(LZ, P[pid]["imagenes"][0]); size = os.path.getsize(path)
        s, p = call("POST", "/media/presign", {"filename": os.path.basename(path), "contentType": "image/png", "size": size})
        assert s == 200, (s, p)
        with open(path, "rb") as f:
            req = urllib.request.Request(p["uploadUrl"], data=f, method="PUT",
                                         headers={"Content-Type": "image/png", "Content-Length": str(size)})
            with urllib.request.urlopen(req, timeout=600) as r:
                print(pid, "PUT", r.status, size)
        e["mediaUrl"] = p["publicUrl"]
        json.dump({"id": pid, "red": "instagram · historia", "fecha_madrid": WHEN[pid][1], "scheduledFor_utc": WHEN[pid][0],
                   "imagen": "../../" + P[pid]["imagenes"][0], "alt": P[pid]["alt"], "adhesivos": "ninguno (imagen sola)",
                   "etiqueta_ia": {"instagram.isAiGenerated": bool(P[pid]["etiqueta_ia"])}},
                  open(os.path.join(d, "copy.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    else:
        b = body(pid, e["mediaUrl"]); guard(b, pid)
        e.update({"scheduledFor_utc": WHEN[pid][0], "madrid": WHEN[pid][1], "accountId": IG,
                  "nota": "historia como imagen, sin adhesivos", "fieldsSent": b})
        if mode == "validate":
            s, r = call("POST", "/tools/validate/post", b)
            e["validate"] = {"http": s, "response": r}; print(pid, "validate", s, json.dumps(r, ensure_ascii=False))
        elif mode == "create":
            if e.get("postId"):
                print(pid, "already", e["postId"]); continue
            idem = str(uuid.uuid4())
            s, r = call("POST", "/posts", b, headers={"Idempotency-Key": idem})
            post = r.get("post", {})
            e.update({"idempotencyKey": idem, "createHttp": s, "postId": post.get("_id"), "status": post.get("status"),
                      "scheduledFor_returned": post.get("scheduledFor"), "createResponse": r})
            print(pid, "create", s, post.get("_id"), post.get("status"), post.get("scheduledFor"),
                  "" if post else json.dumps(r, ensure_ascii=False)[:1500])
        elif mode == "poll":
            s, r = call("GET", f"/posts/{e['postId']}")
            post = r.get("post", r)
            e.update({"status": post.get("status"), "scheduledFor_returned": post.get("scheduledFor"),
                      "polledAt": time.strftime("%Y-%m-%dT%H:%M:%S")})
            print(pid, "poll", s, post.get("status"), post.get("scheduledFor"), [p.get("status") for p in post.get("platforms", [])])
    json.dump(log, open(LOG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
