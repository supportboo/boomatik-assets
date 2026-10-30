"""Builds hoy.html: the launch distribution of chapter 1 (published, scheduled, to paste, pending)."""
import html, json, pathlib

HERE = pathlib.Path(__file__).parent
L01 = HERE.parent
CORREO = L01 / 'microcontenidos' / 'correo'
prim = {p['id']: p for p in json.loads((HERE / 'primeras' / 'primeras.json').read_text(encoding='utf-8'))['piezas']}

PUBLICADO = [
    ('YouTube', 'Capítulo 1 completo · PÚBLICO', 'https://www.youtube.com/watch?v=xOx3j_BtZZY'),
    ('Web', 'Hub de la serie «Tu tienda vende más» (suscripción al boletín)', 'https://brandooers.com/tu-tienda-vende-mas/'),
    ('Web', 'Curso gratis «Los 4 pasos de una tienda que vende»', 'https://brandooers.com/curso-gratis/'),
    ('Web', 'Página de enlaces (para las biografías)', 'https://brandooers.com/enlaces/'),
    ('Web', 'Artículos de la serie', 'https://brandooers.com/tu-tienda-vende-mas/articulos/'),
    ('Web', 'Página del capítulo con transcripción','https://brandooers.com/tu-tienda-vende-mas/por-que-tu-tienda-online-no-vende/'),
    ('Web', 'La hoja de los 4 pasos (PDF)', 'https://brandooers.com/descargas/hoja-4-pasos-tu-tienda-vende-mas.pdf'),
    ('Web', 'Calculadora del paso que se rompe', 'https://brandooers.com/calculadora/'),
    ('Web', '10 prompts para tu tienda', 'https://brandooers.com/prompts-para-tu-tienda/'),
    ('Pódcast', 'Episodio 1 en audio (el RSS sale el lunes)', 'https://brandooers.com/podcast/tvm-ep01-por-que-tu-tienda-online-no-vende.mp3'),
    ('Instagram', 'Avance «El lunes, capítulo 1»', 'https://www.instagram.com/p/DfEzo9pgA38/'),
    ('Instagram', 'Historia «Visitas sí, ventas no»', 'https://www.instagram.com/stories/brandooers_skillup/4018564162979931529'),
    ('Facebook', 'Avance en la página', 'https://www.facebook.com/1468362009686872_122096100579536027'),
    ('LinkedIn', 'Avance en la página de Brandooers', 'https://www.linkedin.com/feed/update/urn:li:share:7521520311226368002/'),
    ('TikTok', 'Avance en foto', 'https://www.tiktok.com/@skillup_brandooers/video/7702036797534063905'),
]
PROGRAMADO = [
    ('dom 1-nov · 21:00', 'Instagram', 'Historia: cuenta atrás (imagen)'),
    ('lun 2-nov · 17:00', 'Pódcast', 'RSS público con el episodio 1 (Spotify, Apple, Amazon, iVoox lo leen)'),
    ('hoy y desde mañana', 'Facebook, LinkedIn, Instagram, TikTok', 'Avisos «ya está» con el enlace del capítulo y los vídeos cortos de la primera semana (preparándose)'),
    ('mié 4-nov · 11:00', 'Instagram', 'Carrusel «Los 4 pasos donde se rompe la venta» (8 láminas)'),
    ('mié 4-nov · 13:00', 'Instagram', 'Historia: pregunta (imagen)'),
]
PENDIENTE = [
    ('Vídeos cortos (Shorts, reels, TikTok)', 'Se cortan del capítulo corregido; los programa el equipo BOO Social.'),
    ('Publicaciones con el enlace del capítulo (FB, LinkedIn página, historias)', 'En cuanto el capítulo sea público el lunes.'),
    ('Spotify y Apple Podcasts', 'Alta única el lunes después de las 17:00: pegar el RSS https://brandooers.com/podcast/feed.xml (código a marc@brandooers.com).'),
    ('Substack: descripción con erratas', 'Cambia «Educacion innovación y estraetgia» por «Educando innovación y estrategia» en Ajustes de la publicación.'),
    ('Entrada musical con Suno', 'Con los prompts de rap; cuando tengas las tomas, se montan.'),
]
CUENTAS = [
    ('YouTube', 'https://www.youtube.com/@skillup.brandooers'),
    ('Instagram', 'https://www.instagram.com/brandooers_skillup/'),
    ('TikTok', 'https://www.tiktok.com/@skillup_brandooers'),
    ('Facebook', 'https://www.facebook.com/1468362009686872'),
    ('LinkedIn', 'https://www.linkedin.com/company/brandooers/'),
    ('Substack', 'https://skillupbrandooers.substack.com'),
    ('Web', 'https://brandooers.com/tu-tienda-vende-mas/por-que-tu-tienda-online-no-vende/'),
]


def e(s):
    return html.escape(s, quote=True)


def copiable(titulo, cuando, texto):
    i = abs(hash(titulo)) % 10**8
    return (f'<article class="card"><div class="row"><h3>{e(titulo)}</h3><span class="tag">{e(cuando)}</span></div>'
            f'<pre id="t{i}">{e(texto)}</pre><button onclick="copiar(\'t{i}\', this)">COPIAR TEXTO</button></article>')


def li(pid):
    p = prim.get(pid, {})
    return (p.get('texto', '') + ('\n\n' + p['hashtags'] if p.get('hashtags') else '')).strip()


pegar = [
    copiable('Substack · correo de bienvenida (Ajustes › Correo de bienvenida)', 'ya', (CORREO / '00_bienvenida.md').read_text(encoding='utf-8')),
    copiable('Substack · carta 1 «Por qué tu tienda no vende»', 'programar lun 2-nov 17:00', (CORREO / '01_carta_por-que-tu-tienda-no-vende.md').read_text(encoding='utf-8')),
    copiable('Tu LinkedIn personal · post 1 (con la imagen del kit)', 'mar 3-nov 8:30', li('C01-LI-1')),
    copiable('Tu LinkedIn personal · post 2 (documento PDF de los 4 pasos)', 'jue 5-nov 8:30', li('C01-LI-2')),
]

rows_pub = ''.join(f'<li><span class="net">{e(n)}</span><a href="{e(u)}" target="_blank" rel="noopener">{e(t)}</a></li>' for n, t, u in PUBLICADO)
rows_prog = ''.join(f'<li><span class="net">{e(d)}</span><b>{e(n)}</b> · {e(t)}</li>' for d, n, t in PROGRAMADO)
rows_pend = ''.join(f'<li><b>{e(a)}</b><br><span class="muted">{e(b)}</span></li>' for a, b in PENDIENTE)
rows_cta = ''.join(f'<a class="pill" href="{e(u)}" target="_blank" rel="noopener">{e(n)}</a>' for n, u in CUENTAS)

page = f'''<!doctype html><html lang="es-ES"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Lanzamiento capítulo 1 · Brandooers</title>
<style>
:root{{--bg:#0d0b14;--card:#17131f;--fg:#ece9f5;--muted:#b3acc6;--acc:#a78bfa;--pink:#ec4899;--cyan:#22d3ee;--line:#2a2338}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--fg);font:16px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif;padding:24px max(16px,env(safe-area-inset-left)) 48px max(16px,env(safe-area-inset-right))}}
main{{max-width:960px;margin:0 auto;display:grid;gap:28px}}h1{{font-size:clamp(1.6rem,4vw,2.4rem);margin:0;text-wrap:balance}}
h2{{font-size:1.15rem;letter-spacing:.06em;text-transform:uppercase;color:var(--acc);margin:0 0 12px}}h3{{font-size:1rem;margin:0}}
.muted{{color:var(--muted)}}ul{{list-style:none;margin:0;padding:0;display:grid;gap:8px}}
li{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px 14px;min-width:0;overflow-wrap:anywhere}}
.net{{display:inline-block;min-width:9.5em;color:var(--cyan);font-weight:600;margin-right:8px}}a{{color:var(--fg)}}
.pills{{display:flex;flex-wrap:wrap;gap:8px}}.pill{{background:var(--card);border:1px solid var(--line);border-radius:999px;padding:8px 14px;text-decoration:none}}
.card{{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px;display:grid;gap:10px;min-width:0}}
.row{{display:flex;flex-wrap:wrap;justify-content:space-between;gap:8px;align-items:center}}.tag{{background:var(--pink);color:#fff;border-radius:6px;padding:2px 8px;font-size:.85rem}}
pre{{white-space:pre-wrap;margin:0;font:14px/1.5 ui-monospace,Consolas,monospace;color:var(--muted);max-height:220px;overflow:auto}}
button{{justify-self:start;background:var(--acc);color:#fff;border:0;border-radius:8px;padding:10px 16px;font-weight:700;letter-spacing:.05em;cursor:pointer}}
.grid{{display:grid;gap:12px}}@media(min-width:760px){{.grid{{grid-template-columns:1fr 1fr}}}}
</style></head><body><main>
<header><p class="muted">Brandooers SkillUp · Tu tienda vende más</p><h1>Lanzamiento del capítulo 1</h1>
<p class="muted">Todo lo que ha salido hoy, lo programado, lo que tienes que pegar tú y lo que falta.</p></header>
<section><h2>Cuentas</h2><div class="pills">{rows_cta}</div></section>
<section><h2>Publicado hoy</h2><ul>{rows_pub}</ul></section>
<section><h2>Programado</h2><ul>{rows_prog}</ul></section>
<section><h2>Para pegar tú</h2><p class="muted">Substack y tu LinkedIn personal no permiten publicar por programa: copia y pega.</p><div class="grid">{''.join(pegar)}</div></section>
<section><h2>Pendiente</h2><ul>{rows_pend}</ul></section>
</main>
<script>
function copiar(id, b){{const t=document.getElementById(id).textContent;
navigator.clipboard.writeText(t).then(()=>{{b.textContent='COPIADO';setTimeout(()=>b.textContent='COPIAR TEXTO',1500)}}).catch(()=>{{const r=document.createRange();r.selectNodeContents(document.getElementById(id));const s=getSelection();s.removeAllRanges();s.addRange(r)}})}}
</script></body></html>'''
(HERE / 'hoy.html').write_text(page, encoding='utf-8')
print('hoy.html', len(page))
