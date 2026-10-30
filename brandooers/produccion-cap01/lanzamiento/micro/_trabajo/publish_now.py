"""Chapter 1 is live (29-oct): publish now the link pieces + «ya está» posts. upload | validate | create | poll.
Also `cancel_h2`: removes the scheduled H2 story («Capítulo 1, mañana»), now false. Log has no key."""
import json, os, sys, time, uuid, urllib.request
L01 = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
sys.path.insert(0, os.path.join(L01, "_zernio_tools"))
from zapi import call

LZ = os.path.join(L01, "lanzamiento")
MICRO = os.path.join(LZ, "micro")
LOG = os.path.join(MICRO, "programado.json")
YT = "https://www.youtube.com/watch?v=xOx3j_BtZZY"
ACC = {"instagram": "6ae2dd79f681a077b3f325cb", "facebook": "6ae2dfbb81cdbb682c9f2766",
       "linkedin": "6ae2e281307878009bccc784", "tiktok": "6ae2de19064494d9f3f1b5bf"}
BOOMATIK = {"6add01b6b63f43d5d66d1850"}
FB_PAGE, LI_ORG = "1468362009686872", "urn:li:organization:107968246"
AI_VIDEO = "Vídeo con mi avatar creado con IA."
AI_IMAGE = "La imagen es mi avatar creado con IA."
P = {x["id"]: x for x in json.load(open(os.path.join(LZ, "primeras", "primeras.json"), encoding="utf-8"))["piezas"]}
IMG = {"C01-IG-H3": os.path.join(LZ, P["C01-IG-H3"]["imagenes"][0]),
       "C01-IG-H5": os.path.join(LZ, P["C01-IG-H5"]["imagenes"][0]),
       "C01-IG-P1": os.path.join(MICRO, "C01-IG-P1", "ya_esta_capitulo1_1080x1350.png"),
       "C01-TT-P1": os.path.join(MICRO, "C01-TT-P1", "ya_esta_capitulo1_1080x1920.png")}
ALT_YA = "Marc mira a cámara en un salón luminoso. Texto: Ya está: capítulo 1. Tu tienda vende más, en YouTube. Logo de Brandooers SkillUp."


def utm(src, pid):
    return f"{YT}&utm_source={src}&utm_medium=social&utm_campaign=tvm-cap01&utm_content={pid.lower()}"


def pieces(m):
    fb_text = P["C01-FB-P1"]["texto"].replace("<enlace del capítulo 1 en YouTube>", utm("facebook", "C01-FB-P1"))
    li = P["C01-LI-P1"]
    ig_text = ("Ya está: el capítulo 1 de «Tu tienda vende más».\n\n"
               "Va de lo que más se repite en una tienda online: hay visitas, pero no hay ventas. "
               "Los cuatro pasos por donde se escapa una venta (encontrar, entender, comprar y pagar) "
               "y una prueba de diez minutos para cada uno.\n\n"
               "El capítulo completo, en YouTube: enlace en la bio.\n\n#tiendaonline #ecommerce #ventasonline")
    tt_text = ("Ya está disponible el capítulo 1 de «Tu tienda vende más»: por qué tu tienda tiene visitas y no vende. "
               "Busca SkillUp Brandooers en YouTube.\n\n#tiendaonline #ecommerce #emprender\n\n" + AI_IMAGE)
    return {
        "C01-FB-P1": {"content": fb_text + "\n\n" + AI_VIDEO,
                      "platforms": [{"platform": "facebook", "accountId": ACC["facebook"],
                                     "platformSpecificData": {"pageId": FB_PAGE}}], "publishNow": True},
        "C01-LI-P1": {"content": li["texto"] + "\n\n" + li["hashtags"] + "\n\n" + AI_VIDEO,
                      "platforms": [{"platform": "linkedin", "accountId": ACC["linkedin"],
                                     "platformSpecificData": {"organizationUrn": LI_ORG,
                                                              "firstComment": "El capítulo completo: " + utm("linkedin", "C01-LI-P1")}}],
                      "publishNow": True},
        "C01-IG-H3": {"content": "", "mediaItems": [{"type": "image", "url": m["C01-IG-H3"]}],
                      "platforms": [{"platform": "instagram", "accountId": ACC["instagram"],
                                     "platformSpecificData": {"contentType": "story", "isAiGenerated": True}}], "publishNow": True},
        "C01-IG-H5": {"content": "", "mediaItems": [{"type": "image", "url": m["C01-IG-H5"]}],
                      "platforms": [{"platform": "instagram", "accountId": ACC["instagram"],
                                     "platformSpecificData": {"contentType": "story", "isAiGenerated": False}}], "publishNow": True},
        "C01-IG-P1": {"content": ig_text, "mediaItems": [{"type": "image", "url": m["C01-IG-P1"], "altText": ALT_YA}],
                      "platforms": [{"platform": "instagram", "accountId": ACC["instagram"],
                                     "platformSpecificData": {"isAiGenerated": True}}], "publishNow": True},
        "C01-TT-P1": {"content": "Ya está disponible el capítulo 1 de «Tu tienda vende más»",
                      "mediaItems": [{"type": "image", "url": m["C01-TT-P1"]}],
                      "platforms": [{"platform": "tiktok", "accountId": ACC["tiktok"]}],
                      "tiktokSettings": {"privacy_level": "PUBLIC_TO_EVERYONE", "allow_comment": True, "media_type": "photo",
                                         "photo_cover_index": 0, "description": tt_text,
                                         "content_preview_confirmed": True, "express_consent_given": True},
                      "publishNow": True},
    }


def guard(b):
    assert len(b["platforms"]) == 1 and b.get("publishNow") is True and "scheduledFor" not in b
    p = b["platforms"][0]
    assert ACC[p["platform"]] == p["accountId"] and p["accountId"] not in BOOMATIK
    txt = json.dumps(b, ensure_ascii=False).lower()
    assert "boomatik" not in txt and "€" not in txt and "el lunes" not in txt and "mañana" not in txt


log = json.load(open(LOG, encoding="utf-8"))
mode = sys.argv[1]
if mode == "upload":
    m = log.setdefault("media_now", {})
    for pid, path in IMG.items():
        size = os.path.getsize(path)
        s, p = call("POST", "/media/presign", {"filename": os.path.basename(path), "contentType": "image/png", "size": size})
        assert s == 200, (s, p)
        with open(path, "rb") as f:
            req = urllib.request.Request(p["uploadUrl"], data=f, method="PUT",
                                         headers={"Content-Type": "image/png", "Content-Length": str(size)})
            with urllib.request.urlopen(req, timeout=600) as r:
                print(pid, "PUT", r.status, size)
        m[pid] = p["publicUrl"]
elif mode == "cancel_h2":
    e = log["pieces"]["C01-IG-H2"]
    s, r = call("DELETE", f"/posts/{e['postId']}")
    e.update({"cancelled": {"http": s, "response": r, "at": time.strftime("%Y-%m-%dT%H:%M:%S"),
                            "why": "Chapter went public 29-oct; the story says «Capítulo 1, mañana · 17:00» and would be false on 1-nov."}})
    print("H2 delete", s, json.dumps(r, ensure_ascii=False)[:500])
else:
    only = set(sys.argv[2:])
    for pid, b in pieces(log.get("media_now", {})).items():
        if only and pid not in only:
            continue
        guard(b)
        e = log["pieces"].setdefault(pid, {})
        e["fieldsSent"] = b; e["publishedNow"] = True
        if mode == "validate":
            s, r = call("POST", "/tools/validate/post", b)
            e["validate"] = {"http": s, "response": r}; print(pid, "validate", s, json.dumps(r, ensure_ascii=False))
        elif mode == "create":
            if e.get("postId"):
                print(pid, "already", e["postId"]); continue
            idem = str(uuid.uuid4())
            s, r = call("POST", "/posts", b, headers={"Idempotency-Key": idem})
            post = r.get("post", {}); plat = (post.get("platforms") or [{}])[0]
            e.update({"idempotencyKey": idem, "createHttp": s, "postId": post.get("_id"), "status": post.get("status"),
                      "platformStatus": plat.get("status"), "url": plat.get("platformPostUrl"),
                      "errorMessage": plat.get("errorMessage"), "createResponse": r})
            print(pid, "create", s, post.get("_id"), post.get("status"), plat.get("status"), plat.get("platformPostUrl"),
                  plat.get("errorMessage") or ("" if post else json.dumps(r, ensure_ascii=False)[:1500]))
        elif mode == "poll":
            if not e.get("postId"):
                continue
            s, r = call("GET", f"/posts/{e['postId']}")
            post = r.get("post", r); plat = (post.get("platforms") or [{}])[0]
            e.update({"status": post.get("status"), "platformStatus": plat.get("status"), "url": plat.get("platformPostUrl"),
                      "errorMessage": plat.get("errorMessage"), "polledAt": time.strftime("%Y-%m-%dT%H:%M:%S")})
            print(pid, "poll", s, post.get("status"), plat.get("status"), plat.get("platformPostUrl"), plat.get("errorMessage") or "")
json.dump(log, open(LOG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
