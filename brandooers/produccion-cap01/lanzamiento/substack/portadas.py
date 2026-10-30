# Substack social previews without faces (29-oct-2026). Reuses the launch kit's fonts/CSS/logo (gen.py definitions only).
import pathlib
GEN = pathlib.Path(r'C:/Users/march/boo-manager/.claude/worktrees/social-growth/.claude/scratch/l01/lanzamiento/_trabajo/gen.py')
src = GEN.read_text(encoding='utf-8'); ns = {'__file__': str(GEN)}
exec(src.split('renders = []')[0], ns)   # definitions only: CSS, DEFS, logo(), mascot(), page()
page, logo, mascot = ns['page'], ns['logo'], ns['mascot']
OUT = pathlib.Path(__file__).parent
W, H = 1200, 630
EXTRA = '.strike{position:absolute;height:14px;background:var(--p);transform:rotate(-6deg)}'

a = (f'<div class="glow"></div>'
     f'<div class="chip c" style="left:64px;top:70px">CAPÍTULO 1 · LUNES 17:00</div>'
     f'<div class="txt" style="left:64px;top:150px;font-size:150px;color:#fff">EL LUNES</div>'
     f'<div class="blk p" style="left:58px;top:300px;font-size:150px">EMPIEZA</div>'
     f'<div class="cav" style="left:72px;top:478px;color:var(--ide)">Tu tienda vende más</div>'
     + mascot('position:absolute;left:760px;top:150px;width:380px')
     + f'<div class="lp" style="right:60px;bottom:48px">{logo(30)}</div>')

b = ('<div style="position:absolute;inset:0;background:var(--c)"></div>'
     '<div class="txt" style="left:60px;top:56px;font-size:120px;color:var(--k)">¿MÁS VISITAS?</div>'
     '<div class="strike" style="left:48px;top:118px;width:700px"></div>'
     '<div class="blk k" style="left:54px;top:200px;font-size:210px">NO</div>'
     '<div class="cav" style="left:66px;top:430px;color:var(--k);font-size:60px">arregla el paso que se rompe</div>'
     '<div class="chip w" style="left:820px;top:90px">ENCONTRAR</div>'
     '<div class="chip w" style="left:820px;top:165px">ENTENDER</div>'
     '<div class="chip w" style="left:820px;top:240px">COMPRAR</div>'
     '<div class="chip p" style="left:850px;top:330px;transform:rotate(4deg)">PAGAR</div>'
     + f'<div class="lp" style="left:60px;bottom:40px">{logo(30)}</div>'
     + mascot('position:absolute;left:930px;top:440px;width:200px'))

for name, body in (('substack_empezamos_1200x630', a), ('substack_carta1_1200x630', b)):
    (OUT / f'{name}.html').write_text(page(name, W, H, body, EXTRA), encoding='utf-8')

from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    br = p.chromium.launch(channel='chrome')
    for name in ('substack_empezamos_1200x630', 'substack_carta1_1200x630'):
        pg = br.new_page(viewport={'width': W, 'height': H})
        pg.goto((OUT / f'{name}.html').as_uri()); pg.evaluate('document.fonts.ready')
        off = pg.evaluate('[...document.querySelectorAll(".txt,.blk,.cav,.chip,.lp")].filter(e=>{const b=e.getBoundingClientRect();return b.right>innerWidth+1||b.bottom>innerHeight+1||b.left<-1||b.top<-1}).map(e=>e.textContent.trim())')
        assert not off, f'{name} off canvas: {off}'
        pg.screenshot(path=str(OUT / f'{name}.png')); pg.close()
    br.close()
print('ok')
