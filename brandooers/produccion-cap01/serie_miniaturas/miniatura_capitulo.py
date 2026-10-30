"""YouTube thumbnail for each chapter of «Tu tienda vende más» (SkillUp Brandooers). Text left, the focal figure right
(default: the Brandooers eyes mascot, since Marc's face never goes on still images — memory rule 29-oct; --foto renders the
photo alternative into con_foto/), never text over it; series badge + «CAPÍTULO N» always in the same corner.

Layouts (see PRINCIPIOS.md):  A  leader model (Sabrina Ramonov): cutout on a brand stage, 2-4 huge words, one colour block
                              B  Colin and Samir «tell a story»: hook + the 4-step chain with the break (--pasos)
                              C  Ali Abdaal «calm authority»: clean, low saturation, brand font, gradient key word
Hook markup: *word* = highlighted word (default: the last word), | = forced line break.

Writes in serie_miniaturas/:  capNN_miniatura[_B|_C]_1280x720.jpg (<= 2 MB, YouTube upload), ..._3840x2160.png (master),
                              pequenas/capNN_miniatura[_B|_C]_168x94.png and _320x180.png (small-size check), and the .html.
Usage: python -I miniatura_capitulo.py 1 "¿POR QUÉ NO VENDE?" "Los 4 pasos donde se rompe la venta"
       [--layout A|B|C|todas] [--mascota search] [--foto foto.png] [--zoom 1.0] [--pasos "ENCONTRAR,ENTENDER,COMPRAR,PAGAR"]
--mascota: render in assets/mascota_<name>.jpg (search, hero, idea, welcome; copied from brandooers/public/images).
--foto: a portrait instead of the mascot, written to con_foto/; without transparency it is cut out first (recorte.py).
--zoom: calibration knob for photos framed tighter or looser than the default one."""
import argparse, html, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import marca
from PIL import Image

W, H, SCALE = 1280, 720, 3


def gancho_html(g, cls):
    """'¿POR QUÉ NO *VENDE?*' -> spans; without *...* the last word is highlighted; '|' forces a line break."""
    g = g.strip()
    if '*' not in g:
        g = re.sub(r'(\S+)$', r'*\1*', g)
    out = html.escape(g).replace('|', '<br>')
    return re.sub(r'\*(.+?)\*', rf'<span class="{cls}">\1</span>', out)


def top_row(n, variant):
    if variant == 'C':
        return (f'<div class="top sg"><i class="bar"></i><span>CAPÍTULO {n}</span><span class="dot">·</span>'
                f'<span class="ser">TU TIENDA VENDE MÁS</span></div>')
    return (f'<div class="top"><span class="serie sg">TU TIENDA VENDE MÁS</span>'
            f'<span class="blk {"p" if variant == "A" else "c"} cap">CAPÍTULO {n}</span></div>')


BASE = """
.glow{position:absolute;inset:0;background:
  radial-gradient(520px 520px at 965px 330px,rgba(139,92,246,.55),transparent 70%),
  radial-gradient(420px 420px at 1240px 700px,rgba(236,72,153,.35),transparent 70%),
  radial-gradient(460px 460px at 760px 40px,rgba(0,212,255,.22),transparent 70%)}
.top{position:absolute;left:56px;top:44px;display:flex;align-items:center;gap:16px}
.serie{font-size:25px;color:#fff;padding:10px 18px 9px;border-radius:999px;background:var(--grad);letter-spacing:.01em}
.cap{font-size:44px}
.hook{position:absolute;left:56px;font-family:"Anton";color:#fff;text-transform:uppercase;line-height:1.05;text-wrap:balance}
.lockup{position:absolute;left:56px;bottom:40px;font-size:30px;display:flex;align-items:center;gap:16px}
.firma{width:84px;height:84px;border-radius:50%;padding:4px;background:var(--grad);flex:none}
.firma img{width:100%;height:100%;border-radius:50%;object-fit:cover;object-position:44% 22%;transform:scale(1.35);transform-origin:44% 30%;display:block}
.firma i{display:block;width:100%;height:100%;border-radius:50%;overflow:hidden;background:#0b0a1a}
.sub{position:absolute;left:56px}
"""

LAYOUTS = {
    'A': dict(photo=(975, 36, 800), box=(600, 0, 680, 720), css="""
.hook{top:140px;width:610px;height:350px}
.hl{background:var(--c);color:var(--k);padding:0 .12em;display:inline-block;line-height:1.08;margin-top:.04em}
.sub{top:520px;width:600px;font-size:44px;line-height:1.05}
.sub span{border-bottom:5px solid var(--p);padding-bottom:2px}
""", hook_fit=(170, 90), hl='hl'),
    'B': dict(photo=(1000, 14, 900), box=(580, 0, 700, 720), css="""
.glow{background:radial-gradient(560px 560px at 990px 360px,rgba(236,72,153,.45),transparent 70%),
  radial-gradient(460px 460px at 760px 60px,rgba(139,92,246,.35),transparent 70%)}
.hook{top:130px;width:620px;height:300px}
.hl{background:var(--p);color:var(--k);padding:0 .12em;display:inline-block;line-height:1;margin-top:.04em}
.sub{top:452px;width:610px;font:600 24px/1.2 "Inter";color:var(--m)}
.chain{position:absolute;left:56px;top:500px;width:600px;height:110px}
.chain .st{position:absolute;top:0;width:126px;text-align:center}
.chain .n{display:block;margin:0 auto 10px;width:62px;height:62px;border-radius:50%;background:#fff;color:var(--k);
  font:400 40px/62px "Anton"}
.chain .t{font:700 17px/1 "Space Grotesk";color:#fff;letter-spacing:.02em}
.chain .ln{position:absolute;top:29px;height:5px;background:#fff}
.chain svg{position:absolute;left:222px;top:-6px}
""", hook_fit=(160, 90), hl='hl'),
    'C': dict(photo=(985, 52, 820), box=(630, 0, 650, 720), css="""
.stage{background:#100e22}
.glow{background:radial-gradient(600px 600px at 990px 380px,rgba(139,92,246,.30),transparent 72%)}
.top{gap:12px;font-size:24px;color:var(--m);letter-spacing:.06em;top:52px}
.top .bar{display:inline-block;width:46px;height:6px;border-radius:3px;background:var(--grad);margin-right:6px}
.top .ser{color:#fff}
.hook{top:150px;width:600px;height:330px;font-family:"Space Grotesk";font-weight:700;letter-spacing:-.035em;line-height:1.06}
.gk{background:var(--grad);-webkit-background-clip:text;background-clip:text;color:transparent;padding-right:.04em}
.sub{top:510px;width:560px;font:500 30px/1.25 "Inter";color:var(--m)}
.ph{filter:saturate(.88)}
""", hook_fit=(150, 80), hl='gk'),
}


def chain_html(pasos):
    xs = [0, 158, 316, 474]
    parts = []
    for i, (x, t) in enumerate(zip(xs, pasos)):
        parts.append(f'<div class="st" style="left:{x}px"><span class="n">{i + 1}</span><span class="t">{html.escape(t)}</span></div>')
    for a, b in ((63, 221), (379, 537)):                       # intact links 1-2 and 3-4
        parts.append(f'<i class="ln" style="left:{a + 31}px;width:{b - a - 62}px"></i>')
    # broken link between 2 and 3: two stubs and a pink jagged crack
    parts.append('<i class="ln" style="left:252px;width:26px"></i><i class="ln" style="left:322px;width:26px"></i>')
    parts.append('<svg width="150" height="76" viewBox="0 0 150 76"><path d="M62 4 L84 30 L66 40 L90 72" fill="none" '
                 'stroke="#EC4899" stroke-width="9" stroke-linejoin="miter" stroke-linecap="square"/></svg>')
    return f'<div class="chain">{"".join(parts)}</div>'


def thumb(v, n, gancho, sub, foto, zoom, pasos, mascota='search', firma=True):
    L = LAYOUTS[v]
    # small round face badge next to the logo (Marc 29-oct: «mi cara en algún sitio pequeña»); off when the big photo is used
    firma_html = (f'<span class="firma"><i><img src="{marca.rel(marca.FOTO)}" alt=""></i></span>'
                  if firma and not foto else '')
    cx, top, size = L['photo']
    fig = marca.foto(foto, cx, top, size * zoom) if foto else marca.figura(marca.mascota(mascota), L['box'], '50% 35%')
    fit, mn = L['hook_fit']
    sub_html = f'<span>{html.escape(sub)}</span>' if sub else ''
    sub_cls = 'sub cav' if v == 'A' else 'sub'
    body = f"""<div class="stage">
<div class="glow"></div>
{fig}
{top_row(n, v)}
<div class="hook" data-fit="{fit}" data-min="{mn}">{gancho_html(gancho, L['hl'])}</div>
{f'<div class="{sub_cls}">{sub_html}</div>' if sub else ''}
{chain_html(pasos) if v == 'B' and pasos else ''}
<div class="lockup">{firma_html}{marca.LOGO}</div>
</div>"""
    return marca.page(f'Capítulo {n} · miniatura {v}', W, H, BASE + L['css'], body, marca.rel(marca.ASSETS))


def ensure_cutout(path):
    im = Image.open(path)
    if im.mode == 'RGBA' and im.getchannel('A').getextrema()[0] < 250:
        return os.path.abspath(path)
    out = os.path.join(marca.ASSETS, os.path.splitext(os.path.basename(path))[0] + '_recorte')
    if not os.path.exists(out + '.png'):
        import recorte
        recorte.cut(path, out)
    return out + '.png'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('numero', type=int)
    ap.add_argument('gancho')
    ap.add_argument('subtitulo', nargs='?', default='')
    ap.add_argument('--layout', default='A', choices=('A', 'B', 'C', 'todas'))
    ap.add_argument('--mascota', default='search')
    ap.add_argument('--foto', help='portrait instead of the mascot (rendered into con_foto/)')
    ap.add_argument('--zoom', type=float, default=1.0)
    ap.add_argument('--pasos', default='ENCONTRAR,ENTENDER,COMPRAR,PAGAR', help='4 steps for layout B (empty = no chain)')
    a = ap.parse_args()
    if a.foto and not os.path.isfile(a.foto):
        ap.error(f'--foto not found: {a.foto}')
    if not os.path.isfile(marca.mascota(a.mascota)):
        ap.error(f'mascot not found: {marca.mascota(a.mascota)}')
    foto = ensure_cutout(a.foto) if a.foto else None
    out = os.path.join(marca.HERE, 'con_foto') if foto else marca.HERE
    marca._REL_BASE[0] = out
    pasos = [p.strip() for p in a.pasos.split(',') if p.strip()][:4]
    if pasos and len(pasos) != 4:
        ap.error('--pasos needs exactly 4 comma-separated steps')
    vs = ('A', 'B', 'C') if a.layout == 'todas' else (a.layout,)
    os.makedirs(os.path.join(out, 'pequenas'), exist_ok=True)
    jobs, names = [], []
    for v in vs:
        name = f'cap{a.numero:02d}_miniatura' + ('' if v == 'A' else f'_{v}')
        src = os.path.join(out, name + '.html')
        open(src, 'w', encoding='utf-8').write(thumb(v, a.numero, a.gancho, a.subtitulo, foto, a.zoom, pasos, a.mascota))
        jobs.append((src, os.path.join(out, name + '_3840x2160.png'), W, H, SCALE))
        names.append(name)
    marca.render(jobs)
    for name in names:
        master = Image.open(os.path.join(out, name + '_3840x2160.png')).convert('RGB')
        jpg = os.path.join(out, name + '_1280x720.jpg')
        q = 92
        while True:                                            # YouTube's 2 MB limit
            master.resize((W, H), Image.LANCZOS).save(jpg, quality=q, optimize=True, progressive=True)
            if os.path.getsize(jpg) <= 2_000_000 or q <= 60:
                break
            q -= 6
        for w, h in ((168, 94), (320, 180)):
            master.resize((w, h), Image.LANCZOS).save(os.path.join(out, 'pequenas', f'{name}_{w}x{h}.png'))
        print('wrote', name, f'jpg {os.path.getsize(jpg) / 1e6:.2f} MB (q{q})')


if __name__ == '__main__':
    main()
