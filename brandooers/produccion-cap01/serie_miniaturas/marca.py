"""Shared SkillUp Brandooers visual system for the series thumbnails and the channel art: brandooers.com tokens (#0b0918 base,
cyan -> violet -> pink gradient, Space Grotesk / Inter / Caveat) plus the approved thumbnail family (Anton blocks, solid
#EC4899 / #00D4FF), the real two-eye logo, Marc's cutout, and the headless-Chrome renderer (one Chrome, >= 1.4 GB free RAM,
closed after). All text is HTML; nothing is drawn by AI."""
import html, os, subprocess, time
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, 'assets')
FOTO = os.path.join(ASSETS, 'marc_recorte.png')

EYES = ('<svg class="beyes" viewBox="0 0 100 58" aria-hidden="true"><defs>'
        '<linearGradient id="bg1" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#8B5CF6"/><stop offset="100%" stop-color="#0891B2"/></linearGradient>'
        '<linearGradient id="bg2" x1="0" y1="0" x2="1" y2="1"><stop offset="0%" stop-color="#0891B2"/><stop offset="100%" stop-color="#E4A900"/></linearGradient>'
        '<radialGradient id="ir1"><stop offset="0%" stop-color="#A78BFA"/><stop offset="100%" stop-color="#6D28D9"/></radialGradient>'
        '<radialGradient id="ir2"><stop offset="0%" stop-color="#67E8F9"/><stop offset="100%" stop-color="#0891B2"/></radialGradient></defs>'
        '<g><ellipse cx="25" cy="36" rx="18" ry="18" fill="none" stroke="url(#bg1)" stroke-width="3"/><circle cx="25" cy="36" r="7.5" fill="url(#ir1)"/>'
        '<circle cx="25" cy="36" r="3.4" fill="#0a0a12"/><circle cx="28" cy="33" r="1.8" fill="#fff"/></g>'
        '<g><ellipse cx="73" cy="36" rx="18" ry="18" fill="none" stroke="url(#bg2)" stroke-width="3"/><circle cx="73" cy="36" r="7.5" fill="url(#ir2)"/>'
        '<circle cx="73" cy="36" r="3.4" fill="#0a0a12"/><circle cx="76" cy="33" r="1.8" fill="#fff"/></g></svg>')
# «SkillUp Brandooers»: SkillUp in Caveat, then the wordmark with the eyes as the «oo»
LOGO = f'<span class="logo"><span class="ide">SkillUp</span>Brand{EYES}ers</span>'


def css(fonts='assets'):
    return f"""
@font-face{{font-family:"Anton";src:url("{fonts}/Anton.ttf")}}
@font-face{{font-family:"Inter";src:url("{fonts}/Inter.ttf");font-weight:100 900}}
@font-face{{font-family:"Caveat";src:url("{fonts}/Caveat.ttf");font-weight:400 700}}
@font-face{{font-family:"Space Grotesk";src:url("{fonts}/SpaceGroteskBD.ttf");font-weight:700}}
:root{{--k:#0b0918;--k2:#12102a;--w:#fff;--p:#EC4899;--c:#00D4FF;--v:#8B5CF6;--m:#b9b0d6;
  --grad:linear-gradient(120deg,#00D4FF,#8B5CF6,#EC4899)}}
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{overflow:hidden;background:var(--k)}}
.stage{{position:absolute;inset:0;overflow:hidden;background:var(--k)}}
.ph{{position:absolute;display:block}}
.logo{{display:inline-flex;align-items:center;gap:.1em;font-family:"Inter";font-weight:900;line-height:1;letter-spacing:-.02em;color:#fff;white-space:nowrap}}
.logo .beyes{{width:1.269em;height:auto;margin:0 .02em;overflow:visible}}
.logo .ide{{font-family:"Caveat";font-weight:700;font-size:1.05em;color:#67E8F9;margin-right:.22em;transform:translateY(.04em)}}
.dark .logo{{color:#0b0918}} .dark .logo .ide{{color:#0891B2}}
.blk{{display:inline-block;font-family:"Anton";line-height:1.04;white-space:nowrap;padding:.06em .14em 0}}
.p{{background:var(--p);color:var(--k)}} .c{{background:var(--c);color:var(--k)}} .w{{background:#fff;color:var(--k)}}
.cav{{font-family:"Caveat";font-weight:700;color:var(--w)}}
.sg{{font-family:"Space Grotesk";font-weight:700;letter-spacing:-.02em}}
.gtxt{{background:var(--grad);-webkit-background-clip:text;background-clip:text;color:transparent}}
"""


# Shrinks every [data-fit] element until it fits its own box. Sets window.__fitted when done.
FIT_JS = """<script>
document.fonts.ready.then(() => {
  for (const el of document.querySelectorAll('[data-fit]')) {
    let s = parseFloat(el.dataset.fit), min = parseFloat(el.dataset.min || 10);
    el.style.fontSize = s + 'px';
    while (s > min && (el.scrollWidth > el.clientWidth + 1 || el.scrollHeight > el.clientHeight + 1)) { s -= 2; el.style.fontSize = s + 'px'; }
    el.dataset.final = s;
  }
  window.__fitted = true;
});
</script>"""


def page(title, w, h, style, body, fonts='assets'):
    return (f'<!doctype html>\n<html lang="es"><head><meta charset="utf-8"><title>{html.escape(title)}</title>\n'
            f'<style>{css(fonts)}html,body{{width:{w}px;height:{h}px}}{style}</style></head>\n<body>\n{body}\n{FIT_JS}\n</body></html>\n')


def cabeza(path):
    """Head top (y) and head centre (x), normalised, from the cutout's alpha: first opaque row, mean x of the top 12 %."""
    a = np.asarray(Image.open(path).getchannel('A').reduce(4), np.float32) / 255
    rows = np.where((a > .5).sum(1) > a.shape[1] * .02)[0]
    top = rows[0]
    band = a[top:top + int(a.shape[0] * .12)]
    xs = np.nonzero(band > .5)[1]
    return top / a.shape[0], xs.mean() / a.shape[1]


def foto(path, cx, top, size, fade=0.16, fade_bottom=0, extra=''):
    """<img> of the square cutout, `size` px wide, with the head centre at x=cx and the head top at y=top (canvas px).
    `fade` softens the cutout's left edge (the photo is cut at the shoulder) into the background."""
    ht, hx = cabeza(path)
    left, y = cx - hx * size, top - ht * size
    layers = [f'linear-gradient(90deg,transparent 0,#000 {fade*100:.0f}%)'] if fade else []
    if fade_bottom:
        layers.append(f'linear-gradient(0deg,transparent 0,#000 {fade_bottom*100:.0f}%)')
    mask = (f'-webkit-mask-image:{",".join(layers)};-webkit-mask-composite:source-in;') if layers else ''
    return (f'<img class="ph" src="{rel(path)}" alt="" style="left:{left:.1f}px;top:{y:.1f}px;width:{size:.1f}px;'
            f'height:auto;{mask}{extra}">')


def mascota(name):
    return os.path.join(ASSETS, f'mascota_{name}.jpg')


def figura(path, box, pos='50% 50%', fade_l=.25, fade_v=0.0, fade_r=0.0):
    """<img> of a Brandooers mascot render (no face of Marc: memory rule 29-oct) filling `box` = (left, top, w, h) with
    object-fit cover; its left edge (and top/bottom with fade_v) melts into the dark background."""
    left, top, w, h = box
    layers = [f'linear-gradient(90deg,transparent 0,#000 {fade_l*100:.0f}%,#000 {100-fade_r*100:.0f}%,{"transparent" if fade_r else "#000"} 100%)']
    if fade_v:
        layers.append(f'linear-gradient(0deg,transparent 0,#000 {fade_v*100:.0f}%,#000 {100-fade_v*100:.0f}%,transparent 100%)')
    return (f'<img class="ph" src="{rel(path)}" alt="" style="left:{left}px;top:{top}px;width:{w}px;height:{h}px;object-fit:cover;'
            f'object-position:{pos};-webkit-mask-image:{",".join(layers)};-webkit-mask-composite:source-in">')


_REL_BASE = [HERE]


def rel(path):
    return os.path.relpath(path, _REL_BASE[0]).replace('\\', '/')


def free_mb():
    r = subprocess.run(['powershell', '-NoProfile', '-Command', '(Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory'],
                       capture_output=True, text=True)
    return int(r.stdout.strip()) / 1024


def render(jobs):
    """jobs = [(html_path, png_path, w, h, scale)]: one Chrome for all, launched only with >= 1.4 GB free, closed at the end."""
    while (f := free_mb()) < 1400:
        print(f'  waiting for RAM: {f:.0f} MB free < 1400', flush=True)
        time.sleep(20)
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        b = p.chromium.launch(channel='chrome', headless=True,
                              args=['--allow-file-access-from-files', '--disable-gpu', '--disable-extensions', '--renderer-process-limit=1'])
        try:
            for src, png, w, h, scale in jobs:
                pg = b.new_page(viewport={'width': w, 'height': h}, device_scale_factor=scale)
                pg.goto('file:///' + src.replace('\\', '/'))
                pg.wait_for_function('window.__fitted === true', timeout=60000)
                pg.wait_for_function('[...document.images].every(i => i.complete)', timeout=60000)
                pg.wait_for_timeout(300)
                fits = pg.eval_on_selector_all('[data-fit]', 'els => els.map(e => [e.dataset.fit, e.dataset.final])')
                pg.screenshot(path=png, clip={'x': 0, 'y': 0, 'width': w, 'height': h}, omit_background=png.endswith('_transparente.png'))
                pg.close()
                print('rendered', os.path.basename(png), f'{w*scale}x{h*scale}', 'fit:', fits, flush=True)
        finally:
            b.close()
