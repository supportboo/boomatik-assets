"""Read public YouTube search result pages (no login, hl=es, gl=ES) and save top videos.

Usage: python -I youtube_search.py OUT_DIR "query 1" "query 2" ...
Writes OUT_DIR/youtube_busquedas.json: per query, first ~20 videos with title, channel, views text, published text.
"""
import json
import re
import sys
import time
import urllib.parse
import urllib.request

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/130 Safari/537.36"


def runs(o):
    if not o:
        return None
    if "simpleText" in o:
        return o["simpleText"]
    return "".join(r.get("text", "") for r in o.get("runs", []))


def walk(o, acc):
    if isinstance(o, dict):
        if "videoRenderer" in o:
            v = o["videoRenderer"]
            acc.append({
                "id": v.get("videoId"),
                "titulo": runs(v.get("title")),
                "canal": runs(v.get("ownerText")),
                "vistas": runs(v.get("viewCountText")),
                "publicado": runs(v.get("publishedTimeText")),
                "duracion": runs(v.get("lengthText")),
            })
            return
        for x in o.values():
            walk(x, acc)
    elif isinstance(o, list):
        for x in o:
            walk(x, acc)


def views_num(s):
    if not s:
        return None
    s = s.replace("\xa0", " ")
    m = re.search(r"([\d.,]+)\s*(mill|M|k|K|mil)?", s)
    if not m:
        return None
    n = float(m.group(1).replace(".", "").replace(",", "."))
    unit = (m.group(2) or "").lower()
    return int(n * (1_000_000 if unit.startswith("mill") or unit == "m" else 1000 if unit in ("k", "mil") else 1))


def main():
    out_dir, queries = sys.argv[1], sys.argv[2:]
    res = {"fuente": "https://www.youtube.com/results?search_query=…&hl=es&gl=ES (página pública)", "fecha": time.strftime("%Y-%m-%d"), "busquedas": {}}
    for q in queries:
        url = "https://www.youtube.com/results?search_query=" + urllib.parse.quote(q) + "&hl=es&gl=ES"
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "es-ES,es;q=0.9"})
            html = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace")
            m = re.search(r"var ytInitialData = (\{.*?\});</script>", html, re.S)
            acc = []
            walk(json.loads(m.group(1)), acc)
            for v in acc:
                v["vistas_n"] = views_num(v["vistas"])
            res["busquedas"][q] = {"url": url, "videos": acc[:20]}
        except Exception as e:  # keep going on one failed query
            res["busquedas"][q] = {"url": url, "error": repr(e)}
        time.sleep(1.5)
    with open(out_dir + "/youtube_busquedas.json", "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
