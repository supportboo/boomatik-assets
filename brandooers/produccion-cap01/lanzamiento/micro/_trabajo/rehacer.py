"""Rebuild the pending/scheduled chapter-1 pieces to Marc's 29-oct visual rules: no big face (photo -> Brandooers eyes mascot
render), logo «SkillUp Brandooers» (was «Brandooers SkillUp»), small round face badge next to the logo (as in the chapter
thumbnail). Patches the original HTML so the rest of each design stays identical. Renders ONE job per Chrome launch behind
marca.render's RAM gate. Writes micro/rehecho/{id}_{name}.png + html/.
Usage: python rehacer.py [job_name ...]   (no args = all jobs; already rendered PNGs are skipped unless named)"""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
LZ = os.path.abspath(os.path.join(HERE, "..", ".."))
L01 = os.path.dirname(LZ)
SM = os.path.join(L01, "serie_miniaturas")
sys.path.insert(0, SM)
import marca  # noqa: E402

OUT = os.path.join(LZ, "micro", "rehecho")
HT = os.path.join(OUT, "html")
SRC1 = os.path.join(LZ, "_trabajo", "html")
SRC2 = os.path.join(HERE, "html")
url = lambda p: "file:///" + p.replace("\\", "/")
FACE = url(marca.FOTO)

LOGO_RE = re.compile(r'Brand(<svg class="beyes".*?</svg>)ers<span class="ide">SkillUp</span>', re.S)
IDE_RE = re.compile(r'\.logo \.ide\{[^}]*\}')
PH_RE = re.compile(r'<div class="ph" data-face="[^"]*" style="left:(\d+)px;top:(\d+)px;width:(\d+)px;height:(\d+)px;[^"]*"></div>')
EXTRA_CSS = """.logo .ide{font-family:Caveat;font-weight:700;font-size:1.05em;color:var(--ide);margin-right:.22em;transform:translateY(.04em)}
.lp .firma{width:66px;height:66px;border-radius:50%;padding:3px;background:linear-gradient(120deg,#00D4FF,#8B5CF6,#EC4899);flex:none;margin:-11px 14px -11px -17px}
.firma i{display:block;width:100%;height:100%;border-radius:50%;overflow:hidden;background:#0b0a1a}
.firma img{width:100%;height:100%;border-radius:50%;object-fit:cover;object-position:44% 22%;transform:scale(1.35);transform-origin:44% 30%;display:block}
.mas{position:absolute;display:block;object-fit:cover}"""


def mascot(box, name, pos, fade_top=0, fade_bot=0):
    """<img> of the mascot render in the photo's box; optional vertical fades into the dark background."""
    l, t, w, h = box
    mask = ""
    if fade_top or fade_bot:
        mask = (f"-webkit-mask-image:linear-gradient(180deg,{'transparent 0,' if fade_top else ''}#000 {fade_top}%,"
                f"#000 {100 - fade_bot}%{',transparent 100%' if fade_bot else ''});")
    return (f'<img class="mas" src="{url(marca.mascota(name))}" alt="" '
            f'style="left:{l}px;top:{t}px;width:{w}px;height:{h}px;object-position:{pos};{mask}">')


# job: (piece id, source html, output name, w, h, mascot spec or None)
JOBS = [("C01-IG-C1", os.path.join(SRC1, f"carrusel_{i}.html"), f"carrusel_4_pasos_{i}de8_1080x1350", 1080, 1350,
         ("search", "50% 34%", 0, 0) if i == 1 else None) for i in range(1, 9)]
JOBS += [
    ("C01-IG-H3", os.path.join(SRC1, "historia_h3.html"), "historia_h3_mas_visitas_no_1080x1920", 1080, 1920, ("search", "50% 40%", 10, 10)),
    ("C01-IG-H4", os.path.join(SRC1, "historia_h4.html"), "historia_h4_donde_esta_el_salto_1080x1920", 1080, 1920, None),
    ("C01-IG-H5", os.path.join(SRC1, "historia_h5.html"), "historia_h5_pagar_de_15_a_3_1080x1920", 1080, 1920, None),
    ("C01-IG-P1", os.path.join(SRC2, "yaesta_4x5.html"), "ya_esta_capitulo1_1080x1350", 1080, 1350, ("search", "50% 30%", 0, 30)),
    ("C01-TT-P1", os.path.join(SRC2, "yaesta_9x16.html"), "ya_esta_capitulo1_1080x1920", 1080, 1920, ("search", "50% 30%", 12, 26)),
]
# full-bleed photos: shrink the mascot box so the headline sits on dark background, not over the mascot
BOX = {"C01-IG-P1": (0, 0, 1080, 900), "C01-TT-P1": (0, 160, 1080, 1120)}


def build(pid, src, name, w, h, spec):
    s = open(src, encoding="utf-8").read()
    s, n = LOGO_RE.subn(r'<span class="ide">SkillUp</span>Brand\1ers', s)
    assert n == 1, (src, "logo", n)
    s = s.replace('<span class="logo"', f'<span class="firma"><i><img src="{FACE}" alt=""></i></span><span class="logo"', 1)
    s = IDE_RE.sub("", s, 1).replace("</style>", EXTRA_CSS + "</style>", 1)
    s = s.replace("Brandooers SkillUp", "SkillUp Brandooers")
    if spec:
        m = PH_RE.search(s)
        assert m, (src, "no photo box")
        s = s.replace(m.group(0), mascot(BOX.get(pid) or tuple(map(int, m.groups())), *spec))
    assert "data-face" not in s and "/fotos/" not in s and "Brandooers SkillUp" not in s, src
    s = s.replace("</body>", marca.FIT_JS + "</body>")  # sets window.__fitted for marca.render
    hp = os.path.join(HT, f"{pid}_{name}.html")
    open(hp, "w", encoding="utf-8").write(s)
    return hp, os.path.join(OUT, f"{pid}_{name}.png")


if __name__ == "__main__":
    os.makedirs(HT, exist_ok=True)
    only = set(sys.argv[1:])
    for pid, src, name, w, h, spec in JOBS:
        hp, png = build(pid, src, name, w, h, spec)
        if (only and name not in only and pid not in only) or (not only and os.path.exists(png)):
            continue
        marca.render([(hp, png, w, h, 1)])  # one Chrome per job, RAM-gated (>= 1.4 GB free)
