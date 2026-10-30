"""Channel art for SkillUp Brandooers at brand level («Innovación · Desarrollo · Estrategia»: no series, no chapter) plus the
series-level covers of each course (YouTube playlist cover 1280x720 and podcast season cover 3000x3000), all in the same system
as the chapter thumbnails (marca.py): dark brandooers.com base, cyan -> violet -> pink accents, Anton blocks, Space Grotesk /
Inter / Caveat, the two-eye logo and the eyes mascot (Marc's face never goes on still images: memory rule 29-oct), key
content inside each platform's safe area (SAFE, also drawn by index.html).
Writes into banners/: the .html of each piece and its PNG (JPG too when the platform has a weight limit), then index.html.
--foto renders the alternative with Marc's photo into con_foto/banners/ (only if Marc lifts the no-face rule).
Usage: python -I banners.py                                        brand pieces + the covers of every course in SERIES
       python -I banners.py --serie "Nuevo *curso*" --temporada 2  only the covers of one course (playlist + podcast season)
       python -I banners.py --solo youtube_banner_2560x1440 ...   |   --indice (only rebuild index.html)
Course name markup: *word* = highlighted words (default: the last word), | = forced line break."""
import argparse, glob, json, os, re, sys, unicodedata
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import marca
from miniatura_capitulo import gancho_html
from PIL import Image

OUT = os.path.join(marca.HERE, 'banners')
OUT_FOTO = os.path.join(marca.HERE, 'con_foto', 'banners')
NO_FIGURE = {'substack_wordmark_1344x256_texto-oscuro_transparente', 'substack_wordmark_1344x256_texto-blanco_transparente',
             'substack_logo_512x512'}
PROMESA = 'Formación práctica para hacer crecer tu negocio con innovación, IA y estrategia'
CRED = 'Marc Herrero · Educando innovación y estrategia'
SERIES = [('Tu tienda *vende más*', 1)]          # (course name with markup, podcast season or 0) — add each new course here

# safe area of each piece: (x, y, w, h) in the piece's pixels, with its source
SAFE = {
    'youtube_banner_2560x1440': ((507, 508, 1546, 423), 'YouTube: zona visible en todos los dispositivos 1546x423 centrada'),
    'facebook_portada_1640x624': ((266, 0, 1108, 624), 'Facebook: en móvil se ve el centro 16:9 (1108x624); en escritorio la foto de perfil tapa abajo a la izquierda'),
    'linkedin_portada_1128x191': ((200, 0, 928, 191), 'LinkedIn: el logo de la página tapa la parte izquierda'),
    'substack_wordmark_1344x256_texto-oscuro_transparente': ((0, 0, 1344, 256), 'Substack wordmark 21:4, mínimo 1344x256 (cabecera clara)'),
    'substack_wordmark_1344x256_texto-blanco_transparente': ((0, 0, 1344, 256), 'Substack wordmark 21:4, mínimo 1344x256 (cabecera oscura)'),
    'substack_banner_correo_1100x220': ((0, 0, 1100, 220), 'Substack banner del correo 1100x220'),
    'substack_logo_512x512': ((75, 75, 362, 362), 'Logo cuadrado (se ve recortado en círculo)'),
    'perfil_1080x1080': ((158, 158, 764, 764), 'Foto de perfil: se recorta en círculo'),
    'perfil_claro_1080x1080': ((158, 158, 764, 764), 'Foto de perfil: se recorta en círculo'),
    'podcast_portada_3000x3000': ((0, 0, 3000, 3000), 'Portada del pódcast (marca): debe leerse a 200x200'),
}

GLOW = ('<div style="position:absolute;inset:0;background:'
        'radial-gradient({r}px {r}px at {x1}px {y1}px,rgba(139,92,246,.50),transparent 70%),'
        'radial-gradient({r}px {r}px at {x2}px {y2}px,rgba(236,72,153,.30),transparent 70%),'
        'radial-gradient({r}px {r}px at {x3}px {y3}px,rgba(0,212,255,.22),transparent 70%)"></div>')


def glow(r, a, b, c):
    return GLOW.format(r=r, x1=a[0], y1=a[1], x2=b[0], y2=b[1], x3=c[0], y3=c[1])


FOTO_MODE = [False]


def fig(photo, mascota):
    """Right-hand figure: Marc's cutout when FOTO_MODE, else a mascot render. photo = (cx, top, size[, fade_bottom]);
    mascota = (name, (left, top, w, h), object-position, fade_left, fade_vertical)."""
    if FOTO_MODE[0]:
        cx, top, size, *fb = photo
        return marca.foto(marca.FOTO, cx, top, size, fade_bottom=fb[0] if fb else 0)
    name, box, pos, fl, fv, *fr = mascota
    return marca.figura(marca.mascota(name), box, pos, fl, fv, fr[0] if fr else 0)


def ide(size, gap=.22):
    """«Innovación · Desarrollo · Estrategia» as three Anton blocks in the brand colours."""
    return (f'<div style="display:flex;flex-wrap:wrap;gap:{gap}em;font-size:{size}px">'
            '<span class="blk w">INNOVACIÓN</span><span class="blk c">DESARROLLO</span><span class="blk p">ESTRATEGIA</span></div>')


def youtube():
    w, h = 2560, 1440
    body = f"""<div class="stage">{glow(900, (1850, 700), (2300, 1200), (700, 400))}
{fig((1870, 520, 520, .15), ('hero', (1300, 470, 900, 500), '50% 50%', .3, .3, .35))}
<div style="position:absolute;left:560px;top:536px;width:940px">
  <div style="font-size:100px">{marca.LOGO}</div>
  <div style="margin-top:28px">{ide(58)}</div>
  <div style="margin-top:24px;font:600 34px/1.25 Inter;color:#fff;width:900px">{PROMESA}</div>
  <div class="cav" style="margin-top:10px;font-size:40px;color:#67E8F9">{CRED}</div>
</div></div>"""
    return w, h, body


def facebook():
    w, h = 1640, 624
    body = f"""<div class="stage">{glow(700, (1180, 330), (1550, 620), (400, 60))}
{fig((1190, 46, 600), ('welcome', (900, 0, 560, 624), '50% 40%', .28, 0, .2))}
<div style="position:absolute;left:300px;top:100px;width:640px">
  <div style="font-size:64px">{marca.LOGO}</div>
  <div style="margin-top:24px">{ide(42)}</div>
  <div style="margin-top:22px;font:600 25px/1.3 Inter;color:#fff;width:600px">{PROMESA}</div>
  <div class="cav" style="margin-top:10px;font-size:32px;color:#67E8F9">{CRED}</div>
</div></div>"""
    return w, h, body


def linkedin():
    w, h = 1128, 191
    body = f"""<div class="stage">{glow(380, (980, 100), (1120, 190), (300, 0))}
{fig((990, 12, 250), ('hero', (840, 0, 288, 191), '55% 50%', .3, 0))}
<div style="position:absolute;left:236px;top:24px;width:640px">
  <div style="font-size:40px">{marca.LOGO}</div>
  <div style="margin-top:14px">{ide(30)}</div>
  <div style="margin-top:12px;font:600 16px/1.2 Inter;color:#fff">{PROMESA}</div>
</div></div>"""
    return w, h, body


def wordmark(blanco):
    w, h = 1344, 256
    body = f"""<div class="{'' if blanco else 'dark'}" style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center">
<div data-fit="170" data-min="60" style="width:1300px;height:230px;display:flex;align-items:center;justify-content:center">{marca.LOGO}</div></div>"""
    return w, h, body, 'html,body{background:transparent!important}'


def correo():
    w, h = 1100, 220
    body = f"""<div class="stage">{glow(420, (930, 110), (1100, 220), (200, 0))}
{fig((950, 16, 290), ('hero', (780, 0, 320, 220), '55% 50%', .3, 0))}
<div style="position:absolute;left:48px;top:30px">
  <div style="font-size:46px">{marca.LOGO}</div>
  <div style="margin-top:18px">{ide(34)}</div>
  <div class="cav" style="margin-top:10px;font-size:30px;color:#67E8F9">{CRED}</div>
</div></div>"""
    return w, h, body


def logo_cuadrado():
    w, h = 512, 512
    body = f"""<div class="stage">{glow(420, (256, 256), (470, 480), (40, 40))}
<div style="position:absolute;left:56px;top:150px;width:400px">{marca.EYES.replace('class="beyes"', 'width="400" height="232"')}</div>
</div>"""
    return w, h, body


def perfil(claro):
    w, h = 1080, 1080
    ring = ('<svg style="position:absolute;inset:0" width="1080" height="1080"><defs><linearGradient id="rg" x1="0" y1="0" x2="1" y2="1">'
            '<stop offset="0" stop-color="#00D4FF"/><stop offset=".5" stop-color="#8B5CF6"/><stop offset="1" stop-color="#EC4899"/>'
            '</linearGradient></defs><circle cx="540" cy="540" r="518" fill="none" stroke="url(#rg)" stroke-width="14" opacity=".9"/></svg>')
    bg = '<div class="stage" style="background:#f8f9fd">' if claro else f'<div class="stage">{glow(800, (560, 460), (980, 1000), (120, 120))}'
    return w, h, f'{bg}{fig((545, 110, 1000), ("hero", (0, 0, 1080, 1080), "53% 45%", 0, 0))}{ring}</div>'


def podcast():
    w, h = 3000, 3000
    body = f"""<div class="stage">{glow(1900, (2150, 1300), (2900, 2900), (300, 300))}
{fig((2130, 720, 2350), ('hero', (1450, 700, 1550, 1550), '55% 50%', .25, .12))}
<div style="position:absolute;left:170px;top:200px;font-size:170px">{marca.LOGO}</div>
<div class="cav" style="position:absolute;left:190px;top:430px;font-size:230px;transform:rotate(-4deg)">el pódcast</div>
<div style="position:absolute;left:170px;top:1060px;display:flex;flex-direction:column;gap:60px;align-items:flex-start">
  <span class="blk w" style="font-size:260px">INNOVACIÓN</span>
  <span class="blk c" style="font-size:260px">DESARROLLO</span>
  <span class="blk p" style="font-size:260px">ESTRATEGIA</span>
</div>
<div class="cav" style="position:absolute;left:176px;top:2720px;font-size:96px;color:var(--m)">{CRED}</div>
</div>"""
    return w, h, body


HOOK_CSS = """.hook{{position:absolute;left:{l}px;top:{t}px;width:{w}px;height:{h}px;font-family:Anton;color:#fff;text-transform:uppercase;
line-height:.98;text-wrap:balance}}.hl{{background:var(--c);color:var(--k);padding:0 .12em;display:inline-block;line-height:1.1;margin-top:.04em}}"""


def lista(nombre):
    """YouTube playlist cover of a course, 1280x720: the chapter-thumbnail grid with «CURSO» + course name instead of the hook."""
    w, h = 1280, 720
    body = f"""<div class="stage">{glow(560, (965, 330), (1240, 700), (760, 40))}
{fig((975, 36, 800), ('search', (600, 0, 680, 720), '50% 35%', .25, 0))}
<div style="position:absolute;left:56px;top:44px;display:flex;gap:16px;align-items:center">
  <span class="serie sg" style="font-size:25px">CURSO</span><span class="sg" style="font-size:22px;color:var(--m)">INNOVACIÓN · DESARROLLO · ESTRATEGIA</span></div>
<div class="hook" data-fit="170" data-min="80">{gancho_html(nombre, 'hl')}</div>
<div class="cav" style="position:absolute;left:56px;top:540px;font-size:46px">Todos los capítulos, en orden</div>
<div style="position:absolute;left:56px;bottom:40px;font-size:30px">{marca.LOGO}</div>
</div>"""
    return w, h, body, HOOK_CSS.format(l=56, t=130, w=610, h=380)


def temporada(nombre, n):
    """Podcast season cover 3000x3000: the brand show + «TEMPORADA N» + the course name."""
    w, h = 3000, 3000
    body = f"""<div class="stage">{glow(1900, (2150, 1300), (2900, 2900), (300, 300))}
{fig((2130, 720, 2350), ('search', (1450, 700, 1550, 1550), '50% 40%', .25, .12))}
<div style="position:absolute;left:170px;top:200px;font-size:120px">{marca.LOGO}</div>
<div class="cav" style="position:absolute;left:180px;top:360px;font-size:150px;transform:rotate(-4deg)">el pódcast</div>
<div style="position:absolute;left:170px;top:700px"><span class="blk p" style="font-size:250px">TEMPORADA {n}</span></div>
<div class="hook" data-fit="440" data-min="200">{gancho_html(nombre, 'hl')}</div>
<div class="sg" style="position:absolute;left:176px;top:2760px;font-size:76px;color:var(--m)">INNOVACIÓN · DESARROLLO · ESTRATEGIA</div>
</div>"""
    return w, h, body, HOOK_CSS.format(l=170, t=1060, w=1250, h=1560)


def slug(nombre):
    t = unicodedata.normalize('NFKD', nombre.replace('*', '').replace('|', ' ')).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', '-', t).strip('-')


def series_pieces(series):
    out = {}
    for nombre, n in series:
        s, clean = slug(nombre), nombre.replace('*', '').replace('|', ' ')
        out[f'serie_{s}_lista_1280x720'] = lambda nm=nombre: lista(nm)
        SAFE[f'serie_{s}_lista_1280x720'] = ((0, 0, 1280, 720), f'Portada de la lista de YouTube del curso «{clean}»')
        if n:
            out[f'podcast_temporada{n:02d}_{s}_3000x3000'] = lambda nm=nombre, k=n: temporada(nm, k)
            SAFE[f'podcast_temporada{n:02d}_{s}_3000x3000'] = ((0, 0, 3000, 3000), f'Portada de la temporada {n} del pódcast: debe leerse a 200x200')
            JPG[f'podcast_temporada{n:02d}_{s}_3000x3000'] = 0
    return out


EXTRA_CSS = '.serie{color:#fff;padding:.38em .7em .34em;border-radius:999px;background:var(--grad);letter-spacing:.01em}'

PIECES = {
    'youtube_banner_2560x1440': youtube,
    'facebook_portada_1640x624': facebook,
    'linkedin_portada_1128x191': linkedin,
    'substack_wordmark_1344x256_texto-oscuro_transparente': lambda: wordmark(False),
    'substack_wordmark_1344x256_texto-blanco_transparente': lambda: wordmark(True),
    'substack_banner_correo_1100x220': correo,
    'substack_logo_512x512': logo_cuadrado,
    'perfil_1080x1080': lambda: perfil(False),
    'perfil_claro_1080x1080': lambda: perfil(True),
    'podcast_portada_3000x3000': podcast,
}
JPG = {'youtube_banner_2560x1440': 6_000_000, 'facebook_portada_1640x624': 1_000_000, 'podcast_portada_3000x3000': 0}


INDEX = """<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Miniaturas y banners · SkillUp Brandooers</title>
<style>
:root{--k:#0b0918;--k2:#16132f;--w:#fff;--m:#b9b0d6;--c:#00D4FF;--p:#EC4899}
*{box-sizing:border-box}body{margin:0;background:var(--k);color:var(--w);font:16px/1.5 Inter,system-ui,sans-serif;padding:24px 16px 80px}
h1{font-size:28px;margin:0 0 4px}h2{font-size:20px;margin:48px 0 12px;border-top:1px solid #2a2550;padding-top:24px}
p{color:var(--m);margin:4px 0 16px;max-width:900px}
.row{display:flex;flex-wrap:wrap;gap:24px;align-items:flex-start;margin-bottom:28px}
.card{background:var(--k2);border-radius:14px;padding:14px;max-width:100%}
.card h3{margin:0 0 8px;font-size:16px;overflow-wrap:anywhere}.card small{color:var(--m)}
.big{width:min(640px,100%)}
.sm{display:flex;gap:16px;align-items:flex-end;flex-wrap:wrap;margin-top:10px}
.sm figure{margin:0}.sm figcaption{color:var(--m);font-size:12px}.sm img{display:block}
.frame{position:relative;display:inline-block;max-width:100%;background:repeating-conic-gradient(#ffffff10 0 25%,#0000 0 50%) 0/20px 20px}
.frame img{display:block;width:100%;height:auto}
.safe{position:absolute;border:3px dashed #00D4FF;background:#00D4FF22;pointer-events:none;display:none}
.on .safe{display:block}
.dur{position:absolute;right:1.2%;bottom:2.5%;width:9%;height:7%;background:#000c;border-radius:4px;display:none;color:#fff;font-size:11px;align-items:center;justify-content:center}
.on .dur{display:flex}
label{cursor:pointer;color:var(--m);font-size:14px;display:inline-flex;gap:6px;align-items:center;margin-top:8px}
.light{background:#fff}
</style></head><body>
<h1>SkillUp Brandooers · miniaturas, portadas de curso y banners</h1>
<p>Un solo sistema visual. El canal es de marca (Innovación · Desarrollo · Estrategia) y cada curso es una lista dentro del canal y una temporada del pódcast.
Todo el texto está compuesto en HTML y renderizado con Chrome. Cada pieza lleva un interruptor que dibuja su zona segura
(en las miniaturas, la etiqueta de duración que YouTube pone abajo a la derecha). Principios aplicados: PRINCIPIOS.md.</p>
<h2>Curso «Tu tienda vende más» · capítulo 1 · miniaturas A, B y C</h2>
<p>Grande (1280x720) y a los tamaños pequeños de YouTube (320x180 y 168x94), lado a lado.</p>
<div id="thumbs"></div>
<h2>Portadas de curso (lista de YouTube y temporada del pódcast)</h2>
<div id="series" class="row"></div>
<h2>Banners y perfiles de la marca</h2>
<div id="banners" class="row"></div>
<h2>Alternativa con la foto de Marc (en espera)</h2>
<p>La memoria dice que la cara de Marc no va en imágenes fijas (portadas, perfiles, Substack); por eso las piezas de arriba llevan
la mascota de los ojos. Estas versiones con su foto solo se usan si Marc levanta esa regla.</p>
<div id="altthumbs"></div><div id="alt" class="row"></div>
<script>
const THUMBS = __THUMBS__, SAFE = __SAFE__;
const toggle = '<label><input type="checkbox" onchange="this.closest(\\'.card\\').classList.toggle(\\'on\\',this.checked)"> ';
for (const [dir, name, label] of THUMBS) {
  const d = document.createElement('div'); d.className = 'row';
  d.innerHTML = `<div class="card"><h3>${label}</h3><div class="frame big"><img src="${dir}${name}_1280x720.jpg" alt="${label}"><div class="dur">10:01</div></div>
  ${toggle}ver la etiqueta de duración</label>
  <div class="sm"><figure><img src="${dir}pequenas/${name}_320x180.png" width="320" height="180" alt=""><figcaption>320x180</figcaption></figure>
  <figure><img src="${dir}pequenas/${name}_168x94.png" width="168" height="94" alt=""><figcaption>168x94 (móvil, lista)</figcaption></figure></div></div>`;
  document.getElementById(dir ? 'altthumbs' : 'thumbs').appendChild(d);
}
for (const [key, [rect, note, w, h, file, section]] of Object.entries(SAFE)) {
  const name = key.split('/').pop();
  const [x, y, sw, sh] = rect, c = document.createElement('div'); c.className = 'card';
  const pct = (a, b) => (a / b * 100).toFixed(3) + '%';
  const light = name.includes('texto-oscuro') ? ' light' : '';
  const width = Math.min(w, w > 1500 ? 900 : w > 700 ? 640 : 360);
  const small = w === 3000 ? `<div class="sm"><figure><img src="${file}" width="200" height="200" alt=""><figcaption>200x200 (app de pódcast)</figcaption></figure></div>` : '';
  c.innerHTML = `<h3>${name}</h3><small>${w}x${h} · ${note}</small><br>
  <div class="frame${light}" style="width:${width}px;max-width:100%"><img src="${file}" alt="${name}">
  <div class="safe" style="left:${pct(x,w)};top:${pct(y,h)};width:${pct(sw,w)};height:${pct(sh,h)}"></div></div><br>
  ${toggle}ver zona segura</label>${small}`;
  document.getElementById(section).appendChild(c);
}
</script></body></html>
"""


LAYOUT_NAME = {'A': 'Ramonov', 'B': 'Colin and Samir', 'C': 'Ali Abdaal'}


def write_index():
    thumbs = []
    for d in ('', 'con_foto/'):
        for jpg in sorted(glob.glob(os.path.join(marca.HERE, d, 'cap*_miniatura*_1280x720.jpg'))):
            name = os.path.basename(jpg)[:-len('_1280x720.jpg')]
            v = name.rsplit('_', 1)[-1] if name.endswith(('_B', '_C')) else 'A'
            thumbs.append([d, name, f'{name} · versión {v} ({LAYOUT_NAME[v]})' + (' · con foto' if d else '')])
    safe = {}
    for d, out in (('banners/', OUT), ('con_foto/banners/', OUT_FOTO)):
        for name, (rect, note) in SAFE.items():
            f = name + ('.jpg' if name in JPG else '.png')
            if os.path.exists(os.path.join(out, f)):
                w, h = Image.open(os.path.join(out, f)).size
                section = 'alt' if d.startswith('con_foto') else \
                    'series' if name.startswith(('serie_', 'podcast_temporada')) else 'banners'
                safe[d + name] = [rect, note, w, h, d + f, section]
    doc = INDEX.replace('__THUMBS__', json.dumps(thumbs, ensure_ascii=False)).replace('__SAFE__', json.dumps(safe, ensure_ascii=False))
    open(os.path.join(marca.HERE, 'index.html'), 'w', encoding='utf-8').write(doc)
    print('wrote index.html:', len(thumbs), 'thumbnails,', len(safe), 'banners/covers')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--solo', nargs='+')
    ap.add_argument('--serie', help='course name (markup *word*); renders only its playlist cover (+ season cover with --temporada)')
    ap.add_argument('--temporada', type=int, default=0)
    ap.add_argument('--indice', action='store_true', help='only rebuild index.html')
    ap.add_argument('--foto', action='store_true', help="alternative with Marc's photo, into con_foto/banners/")
    a = ap.parse_args()
    pieces = dict(PIECES, **series_pieces(SERIES))
    if a.serie:
        pieces = series_pieces([(a.serie, a.temporada)])
    if a.indice:
        return write_index()
    out = OUT
    if a.foto:
        FOTO_MODE[0], out = True, OUT_FOTO
        pieces = {k: v for k, v in pieces.items() if k not in NO_FIGURE}
    else:
        pieces.pop('perfil_claro_1080x1080', None)          # the mascot render fills the frame: no light variant
    if a.solo:
        bad = set(a.solo) - set(pieces)
        if bad:
            ap.error(f'unknown pieces: {sorted(bad)}; choose from {sorted(pieces)}')
        pieces = {k: pieces[k] for k in a.solo}
    os.makedirs(out, exist_ok=True)
    marca._REL_BASE[0] = out                                   # image paths relative to the output folder
    jobs = []
    for name, fn in pieces.items():
        r = fn()
        w, h, body = r[:3]
        src = os.path.join(out, name + '.html')
        page = marca.page(name, w, h, EXTRA_CSS + (r[3] if len(r) > 3 else ''), body, marca.rel(marca.ASSETS))
        open(src, 'w', encoding='utf-8').write(page)
        jobs.append((src, os.path.join(out, name + '.png'), w, h, 1))
    marca.render(jobs)
    for _, png, w, h, _ in jobs:
        name = os.path.basename(png)[:-4]
        if name in JPG:
            jpg = png[:-4] + '.jpg'
            Image.open(png).convert('RGB').save(jpg, quality=90, optimize=True, progressive=True)
            os.remove(png)                                     # keep disk use small: the JPG is the deliverable
            print(f'  {name}.jpg {os.path.getsize(jpg) / 1e6:.2f} MB' + (f' (limit {JPG[name] / 1e6:g} MB)' if JPG[name] else ''))
        if w == 3000:
            src = png if os.path.exists(png) else png[:-4] + '.jpg'
            Image.open(src).convert('RGB').resize((200, 200), Image.LANCZOS).save(png[:-4].replace('3000x3000', '200x200') + '.png')
    write_index()


if __name__ == '__main__':
    main()
