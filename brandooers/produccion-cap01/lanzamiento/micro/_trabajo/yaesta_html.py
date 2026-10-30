"""«Ya está: capítulo 1» 4:5 and 9:16 from the published teaser HTML (same photo, logo, fonts)."""
import os
LZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
os.makedirs(os.path.join(LZ, "micro", "_trabajo", "html"), exist_ok=True)
for a, b in [("teaser_4x5", "yaesta_4x5"), ("teaser_9x16", "yaesta_9x16")]:
    s = open(os.path.join(LZ, "_trabajo", "html", a + ".html"), encoding="utf-8").read()
    s = s.replace(">EL LUNES,<", ">YA ESTÁ:<").replace(">Tu tienda vende más<", ">Tu tienda vende más · en YouTube<")
    assert "YA ESTÁ:" in s and "en YouTube" in s
    open(os.path.join(LZ, "micro", "_trabajo", "html", b + ".html"), "w", encoding="utf-8").write(s)
print("ok")
