"""Schedule the redone launch pieces (rehecho/MANIFIESTO.json): «ya está» posts on Mon 2-nov 17:00 Madrid (the announced
premiere), stories spread out, and the Wed 4-nov carousel C1 + story H4 recreated with the new media (old scheduled posts
deleted). Marc's standing approval to publish (30-oct). Modes: upload | validate | schedule | poll. Log: rehecho/publicado.json"""
import json, os, sys, time, urllib.request, uuid
HERE = os.path.dirname(os.path.abspath(__file__))
L01 = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, os.path.join(L01, "_zernio_tools"))
from zapi import call

RE = os.path.join(HERE, "..", "rehecho")
LOG = os.path.join(RE, "publicado.json")
ACC = {"instagram": "6ae2dd79f681a077b3f325cb", "facebook": "6ae2dfbb81cdbb682c9f2766",
       "linkedin": "6ae2e281307878009bccc784", "tiktok": "6ae2de19064494d9f3f1b5bf"}
FB_PAGE, LI_ORG = "1468362009686872", "urn:li:organization:107968246"
WHEN = {"C01-FB-P1": "2026-11-02T16:00:00.000Z", "C01-LI-P1": "2026-11-02T16:00:00.000Z",
        "C01-IG-P1": "2026-11-02T16:00:00.000Z", "C01-TT-P1": "2026-11-02T16:05:00.000Z",
        "C01-IG-H3": "2026-11-02T16:10:00.000Z", "C01-IG-H5": "2026-11-03T12:00:00.000Z",
        "C01-IG-C1": "2026-11-04T10:00:00.000Z", "C01-IG-H4": "2026-11-04T12:00:00.000Z"}
OLD = {"C01-IG-C1": "6ae323b3af3ce686a185e37d", "C01-IG-H4": "6ae3241d5a8b63605bebacca"}

M = {p["id"]: p for p in json.load(open(os.path.join(RE, "MANIFIESTO.json"), encoding="utf-8"))["piezas"]}
log = json.load(open(LOG, encoding="utf-8")) if os.path.exists(LOG) else {"media": {}, "pieces": {}}


def body(pid):
    p, media = M[pid], log["media"]
    items = [{"type": "image", "url": media[path], **({"altText": p["alt"][i]} if i < len(p["alt"]) else {})}
             for i, path in enumerate(p["images"])]
    plat = p["platform"].split()[0]
    b = {"content": p["text"], "scheduledFor": WHEN[pid], "timezone": "Europe/Madrid"}
    if items:
        b["mediaItems"] = items
    if plat == "facebook":
        b["platforms"] = [{"platform": "facebook", "accountId": ACC["facebook"], "platformSpecificData": {"pageId": FB_PAGE}}]
    elif plat == "linkedin":
        b["platforms"] = [{"platform": "linkedin", "accountId": ACC["linkedin"],
                           "platformSpecificData": {"organizationUrn": LI_ORG, "firstComment": p["firstComment"]}}]
    elif plat == "instagram":
        psd = {"isAiGenerated": bool(p["isAiGenerated"])}
        if "story" in p["platform"]:
            psd["contentType"] = "story"
        b["platforms"] = [{"platform": "instagram", "accountId": ACC["instagram"], "platformSpecificData": psd}]
    elif plat == "tiktok":
        b["platforms"] = [{"platform": "tiktok", "accountId": ACC["tiktok"]}]
        b["tiktokSettings"] = {"privacy_level": "PUBLIC_TO_EVERYONE", "allow_comment": True, "media_type": "photo",
                               "photo_cover_index": 0, "description": p["tiktokDescription"],
                               "content_preview_confirmed": True, "express_consent_given": True}
    txt = json.dumps(b, ensure_ascii=False)
    assert "Brandooers SkillUp" not in txt and "boomatik" not in txt.lower() and "€" not in txt, pid
    return b


mode = sys.argv[1]
if mode == "upload":
    for p in M.values():
        for path in p["images"]:
            if path in log["media"]:
                continue
            size = os.path.getsize(path)
            s, r = call("POST", "/media/presign", {"filename": os.path.basename(path), "contentType": "image/png", "size": size})
            assert s == 200, (s, r)
            with open(path, "rb") as f:
                req = urllib.request.Request(r["uploadUrl"], data=f, method="PUT",
                                             headers={"Content-Type": "image/png", "Content-Length": str(size)})
                urllib.request.urlopen(req, timeout=600).close()
            log["media"][path] = r["publicUrl"]
            print("up", os.path.basename(path))
else:
    for pid in (sys.argv[2:] or WHEN):
        e = log["pieces"].setdefault(pid, {})
        if mode == "validate":
            s, r = call("POST", "/tools/validate/post", body(pid))
            e["validate"] = {"http": s, "response": r}
            print(pid, "validate", s, json.dumps(r, ensure_ascii=False)[:300])
        elif mode == "schedule":
            if e.get("postId"):
                print(pid, "already", e["postId"]); continue
            if pid in OLD and not e.get("oldDeleted"):
                s, r = call("DELETE", f"/posts/{OLD[pid]}")
                assert s == 200, (pid, s, r)
                e["oldDeleted"] = OLD[pid]
            b, idem = body(pid), str(uuid.uuid4())
            s, r = call("POST", "/posts", b, headers={"Idempotency-Key": idem})
            post = r.get("post", {})
            e.update({"createHttp": s, "postId": post.get("_id"), "status": post.get("status"), "scheduledFor": WHEN[pid],
                      "fieldsSent": b, "error": None if post else r})
            print(pid, "schedule", s, post.get("_id"), post.get("status"), "" if post else json.dumps(r, ensure_ascii=False)[:500])
        elif mode == "poll" and e.get("postId"):
            s, r = call("GET", f"/posts/{e['postId']}")
            post = r.get("post", r); plat = (post.get("platforms") or [{}])[0]
            e.update({"status": post.get("status"), "url": plat.get("platformPostUrl"), "errorMessage": plat.get("errorMessage")})
            print(pid, post.get("status"), plat.get("status"), plat.get("platformPostUrl") or "", plat.get("errorMessage") or "")
json.dump(log, open(LOG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
