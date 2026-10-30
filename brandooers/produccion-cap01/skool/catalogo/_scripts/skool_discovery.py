"""Read public Skool Discovery search pages (no login) and save the groups shown.

Usage: python -I skool_discovery.py OUT_DIR "query 1" "query 2" ...
Writes OUT_DIR/skool_discovery.json with name, members, price, language, description per group.
"""
import json
import re
import sys
import time
import urllib.parse
import urllib.request

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/130 Safari/537.36"


def fetch(q):
    url = "https://www.skool.com/discovery?q=" + urllib.parse.quote(q) + "&lang=spanish"
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "es-ES,es;q=0.9"})
    html = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", "replace")
    m = re.search(r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>', html, re.S)
    return url, json.loads(m.group(1))["props"]["pageProps"]


def pick(g):
    md = g.get("metadata") or {}
    out = {
        "name": g.get("name"),
        "url": "https://www.skool.com/" + str(g.get("name")),
        "display": md.get("displayName") or g.get("displayName"),
        "members": md.get("totalMembers"),
        "description": (md.get("description") or "")[:240],
    }
    for k in ("privacy", "lang", "language", "locale"):
        if k in md:
            out[k] = md[k]
    # price fields vary; keep anything that looks like price/plan
    for k, v in md.items():
        if re.search(r"price|plan|amount|currency|freemium|paid|membership|review", k, re.I) and not isinstance(v, (dict, list)):
            out[k] = v
    return out


def main():
    out_dir, queries = sys.argv[1], sys.argv[2:]
    res = {"fuente": "https://www.skool.com/discovery?q=… (página pública, sin login)", "fecha": time.strftime("%Y-%m-%d"), "busquedas": {}}
    for q in queries:
        try:
            url, pp = fetch(q)
            res["busquedas"][q] = {"url": url, "numGroups": pp.get("numGroups"), "lang": pp.get("languageParam"), "groups": [pick(x["group"]) for x in pp.get("groups", [])]}
        except Exception as e:  # keep going on one failed query
            res["busquedas"][q] = {"error": repr(e)}
        time.sleep(1.5)
    with open(out_dir + "/skool_discovery.json", "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=1)
    if len(sys.argv) > 2 and queries:
        first = next(iter(res["busquedas"].values()))
        if first.get("groups"):
            print(json.dumps(first["groups"][0], ensure_ascii=False))


if __name__ == "__main__":
    main()
