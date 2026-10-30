"""Skool course covers (1460x752) for every course in l01/skool/catalogo/catalogo_cursos.json, on layout A of the chapter
thumbnail (mascot + Marc's small face badge next to the logo). Top row: block pill + «CURSO» or «PRÓXIMAMENTE».
Usage: python -I cursos_portadas.py [slug ...]      (no slug = all courses)
Writes l01/skool/catalogo/portadas/NN_<slug>_1460x752.jpg (+ _2920x1504.png master) and index.html."""
import html, json, os, re, sys, unicodedata
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import marca
import miniatura_capitulo as mc
from PIL import Image

W, H, SCALE = 1460, 752, 2
CAT = os.path.join(marca.HERE, '..', 'skool', 'catalogo', 'catalogo_cursos.json')
OUT = os.path.join(marca.HERE, '..', 'skool', 'catalogo', 'portadas')
# per block: mascot render + highlight colour, so 27 covers don't look alike
BLOQUE = {'0': ('welcome', '#00D4FF'), 'A': ('search', '#00D4FF'), 'B': ('hero', '#EC4899'),
          'C': ('welcome', '#A78BFA'), 'D': ('search', '#EC4899'), 'E': ('idea', '#A78BFA')}
EXTRA = """
.stage{width:1460px;height:752px}
.pro{background:var(--p);color:var(--k)}
.cur{background:var(--c);color:var(--k)}
"""


def stems(s):
    s = unicodedata.normalize('NFD', s.replace('*', '').replace('|', ' '))
    s = re.sub(r'[^a-z ]', ' ', ''.join(ch for ch in s if unicodedata.category(ch) != 'Mn').lower())
    return {w[:4] for w in s.split() if len(w) > 2}


# unlock level per course (Marc 30-oct: courses open by level; tasks are a MUST to level up)
NIVEL = {1: 1, 2: 2, 3: 2, 4: 2, 5: 2, 6: 2, 7: 2, 8: 3, 9: 3, 10: 3, 11: 3, 12: 3, 13: 4, 14: 4, 15: 4, 16: 4, 17: 4,
         18: 5, 19: 5, 20: 5, 21: 5, 22: 5, 23: 5, 24: 5, 25: 6, 26: 6, 27: 6}


def top(c):
    n = NIVEL[c['orden']]
    tag = ('<span class="blk cur cap">ABIERTO</span>' if n == 1
           else f'<span class="blk {"cur" if n <= 3 else "pro"} cap">NIVEL {n}</span>')
    return f'<div class="top"><span class="serie sg">{html.escape(c["bloque_nombre"].upper())}</span>{tag}</div>'


def cover(c):
    mc.W, mc.H = W, H
    mc.LAYOUTS['A']['box'] = (700, 0, 760, 752)
    mc.top_row = lambda n, v: top(c)
    t, g = stems(c['titulo']), stems(c['gancho'])
    sub = c['titulo'] if len(t - g) >= max(2, len(t) // 2) else ''     # skip a subtitle that repeats the hook
    m, col = BLOQUE.get(c['bloque'], ('search', '#00D4FF'))
    page = mc.thumb('A', c['orden'], c['gancho'], sub, None, 1.0, [], m)
    return page.replace('</style>', EXTRA + f'.hl{{background:{col}}}</style>', 1)


def main():
    cursos = sorted(json.load(open(CAT, encoding='utf-8'))['cursos'], key=lambda c: c['orden'])
    if sys.argv[1:]:
        cursos = [c for c in cursos if c['slug'] in sys.argv[1:]]
    os.makedirs(OUT, exist_ok=True)
    marca._REL_BASE[0] = OUT
    jobs = []
    for c in cursos:
        name = f'{c["orden"]:02d}_{c["slug"]}'
        src = os.path.join(OUT, name + '.html')
        open(src, 'w', encoding='utf-8').write(cover(c))
        jobs.append((src, os.path.join(OUT, name + f'_{W * SCALE}x{H * SCALE}.png'), W, H, SCALE))
    marca.render(jobs)
    for _, png, *_ in jobs:
        jpg = png.replace(f'_{W * SCALE}x{H * SCALE}.png', f'_{W}x{H}.jpg')
        Image.open(png).convert('RGB').resize((W, H), Image.LANCZOS).save(jpg, quality=90, optimize=True, progressive=True)
        print('wrote', os.path.basename(jpg), f'{os.path.getsize(jpg) / 1e6:.2f} MB')
    allc = sorted(json.load(open(CAT, encoding='utf-8'))['cursos'], key=lambda c: c['orden'])
    cards = ''.join(f'<figure><img src="{c["orden"]:02d}_{c["slug"]}_{W}x{H}.jpg" alt=""><figcaption>{c["orden"]} · '
                    f'{html.escape(c["titulo"])} · {c["estado"]}</figcaption></figure>' for c in allc)
    open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(
        '<!doctype html><meta charset="utf-8"><title>Portadas de cursos</title><style>body{background:#0b0a1a;color:#ddd;'
        'font:14px system-ui;margin:24px}main{display:grid;grid-template-columns:repeat(auto-fill,minmax(360px,1fr));gap:20px}'
        'img{width:100%;border-radius:10px}</style><h1>Portadas de cursos · Skool</h1><main>' + cards + '</main>')


if __name__ == '__main__':
    main()
