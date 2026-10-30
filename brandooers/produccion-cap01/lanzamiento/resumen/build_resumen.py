"""Launch review page: what is published on every platform (preview + link), what is scheduled, what is being redone
and what waits on Marc. Data comes live from Zernio (GET /posts) plus the fixed list below. Usage: python -I build_resumen.py"""
import datetime as dt, html, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
L01 = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(L01, "_zernio_tools"))
from zapi import call

BRAND_USERS = {"brandooers_skillup", "skillup.brandooers", "skillup_brandooers", "Brandooers", "Skillup.brandooers"}
TEST_VIDEOS = {"gJQuARzDLW4", "iL5YrJWVCE4"}
NAME = {"youtube": "YouTube", "instagram": "Instagram", "facebook": "Facebook", "linkedin": "LinkedIn", "tiktok": "TikTok"}
S = "../.."  # resumen/ -> scratch root is l01/lanzamiento/resumen -> ../../ = l01


def madrid(iso):
    t = dt.datetime.fromisoformat(iso.replace("Z", "+00:00")).astimezone(dt.timezone(dt.timedelta(hours=1)))
    return t.strftime("%d-%m %H:%M")


def card(platform, title, img, url, estado, cuando, nota="", tono="ok"):
    im = f'<img src="{html.escape(img)}" alt="" loading="lazy">' if img else '<div class="noimg">sin imagen</div>'
    link = f'<a href="{html.escape(url)}" target="_blank" rel="noopener">Abrir</a>' if url else ""
    return (f'<article class="c {tono}"><div class="m">{im}</div><div class="b"><div class="p">{html.escape(platform)}</div>'
            f'<h3>{html.escape(title)}</h3><div class="e">{html.escape(estado)} · {html.escape(cuando)}</div>'
            f'{f"<p>{html.escape(nota)}</p>" if nota else ""}{link}</div></article>')


def main():
    s, r = call("GET", "/posts?limit=100")
    assert s == 200, (s, r)
    pub, prog = [], []
    for p in r["posts"]:
        x = p["platforms"][0]
        if x["accountId"].get("username") not in BRAND_USERS:
            continue
        media = p.get("mediaItems") or [{}]
        img = media[0].get("thumbnail") or (media[0].get("url") if media[0].get("type") == "image" else "")
        url = x.get("platformPostUrl") or ""
        plat = NAME.get(x["platform"], x["platform"])
        text = (p.get("content") or "").split("\n")[0][:90] or "Historia"
        if p["status"] == "published":
            vid = url.rsplit("=", 1)[-1] if "youtube" in url else ""
            if vid in TEST_VIDEOS:
                pub.append(card(plat, "Vídeo de prueba (borrar en YouTube Studio)", img, url, "Publicado (oculto)",
                                madrid(x.get("publishedAt") or p.get("publishedAt") or p.get("scheduledFor") or p["createdAt"]), "Versión de prueba del capítulo 1. Hay que borrarla a mano.", "aviso"))
                continue
            if vid:
                img = f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg"
                nota = ("Capítulo 1 público. La miniatura nueva (mascota + tu sello) no se puede poner hasta que verifiques "
                        "el canal en youtube.com/verify.")
                pub.append(card(plat, "Capítulo 1 · Por qué tu tienda online no vende", img, url, "Publicado",
                                madrid(x.get("publishedAt") or p.get("publishedAt") or p.get("scheduledFor") or p["createdAt"]), nota))
            else:
                nota = "Teaser del 29-oct: hecho antes de tu norma (cara grande y nombre antiguo «Brandooers SkillUp»). Propuesta: dejarlo."
                if p.get("content") == "" and x["platform"] == "instagram":
                    nota = "Historia de 24 h (ya caducada). Hecha antes de tu norma."
                pub.append(card(plat, text, img, url, "Publicado", madrid(x.get("publishedAt") or p.get("publishedAt") or p.get("scheduledFor") or p["createdAt"]), nota, "aviso"))
        elif p["status"] == "scheduled":
            nota = "Rehecho sin tu cara grande: mascota, «SkillUp Brandooers» y tu sello pequeño."
            prog.append(card(plat, text, img, "", "Programado", madrid(p["scheduledFor"]), nota, "prog"))

    skool = [
        card("Skool", "Comunidad SkillUp Brandooers · I+D+E", f"{S}/serie_miniaturas/skool/skool_portada_2168x1152.jpg",
             "https://www.skool.com/skillup-brandooers", "Configurada", "30-10",
             "Acerca de, 2 preguntas de entrada, bienvenida automática con tu voz, 9 categorías, 4 normas y 3 enlaces."),
        card("Skool", "Empieza aquí: tu primera semana (fijada)", f"{S}/serie_miniaturas/skool/about_1_marca_1400x790.jpg",
             "https://www.skool.com/skillup-brandooers/empieza-aqui-tu-primera-semana", "Publicado y fijado", "30-10",
             "Corregidas tus frases: «promocionéis», «sino» y los candados."),
        card("Skool", "Cómo pedir ayuda (y que sirva) (fijada)", "",
             "https://www.skool.com/skillup-brandooers/como-pedir-ayuda-y-que-sirva", "Publicado y fijado", "30-10",
             "Cobros y bajas: por mensaje privado en Skool."),
        card("Skool", "Preséntate: copia esta plantilla (fijada)", "",
             "https://www.skool.com/skillup-brandooers/presentate-copia-esta-plantilla", "Publicado y fijado", "30-10"),
        card("Skool", "Aula: 27 cursos", f"{S}/skool/catalogo/portadas/_hoja_27.jpg",
             "https://www.skool.com/skillup-brandooers/classroom", "Publicado", "30-10",
             "Empieza aquí abierto (con 5 lecciones de bloques), Plantillas en nivel 2 y 25 cursos «Próximamente» con candado."),
    ]
    web = [
        card("brandooers.com", "Capítulo 1 en la web", f"{S}/serie_miniaturas/cap01_miniatura_1280x720.jpg",
             "https://brandooers.com/tu-tienda-vende-mas/por-que-tu-tienda-online-no-vende/", "Publicado", "29-10",
             "Con el vídeo, la hoja de 4 pasos y sin tu foto (los ojos)."),
        card("brandooers.com", "Página de enlaces (link in bio)", f"{S}/serie_miniaturas/banners/perfil_1080x1080.png",
             "https://brandooers.com/enlaces/", "Publicado", "30-10"),
        card("brandooers.com", "Curso gratis · Calculadora · Prompts", "", "https://brandooers.com/curso-gratis/", "Publicado", "29-10",
             "También: brandooers.com/calculadora/ y brandooers.com/prompts-para-tu-tienda/"),
        card("Pódcast", "SkillUp Brandooers: innovación, desarrollo y estrategia · T1 E1", f"{S}/serie_miniaturas/banners/podcast_portada_3000x3000.jpg",
             "https://brandooers.com/podcast/tvm-ep01-por-que-tu-tienda-online-no-vende.mp3", "Sale solo", "lun 02-11 17:00",
             "Portada nueva sin tu cara (cambiada hoy). El lunes, dar de alta el RSS en Spotify y Apple.", "prog"),
        card("Substack", "skillupbrandooers.substack.com", "", "https://skillupbrandooers.substack.com", "Sin publicar", "—",
             "No tiene API: necesito tu sesión abierta en Chrome para montarlo y publicar «Empezamos el lunes».", "aviso"),
    ]
    rehacer = ("Nada pendiente de rehacer. Los «Ya está» salen el lunes 2-nov a las 17:00, a la vez que el estreno anunciado, "
               "el pódcast y la carta. Regla nueva: todo vídeo abre con la miniatura como primer fotograma y cierra "
               "pidiendo me gusta, suscripción, comentario y seguirte en redes.")
    pendiente = ["Verificar el canal en youtube.com/verify: sin eso YouTube no deja poner la miniatura (lo he vuelto a probar hoy).", "En YouTube Studio: pantalla final con «Suscribirse» y el vídeo siguiente (la API no lo permite).", "Borrar 2 vídeos de prueba en YouTube Studio.",
                 "Abrir Substack en Chrome para que lo monte.", "Política de privacidad de brandooers.com: ¿la preparo?"]
    now = dt.datetime.now().strftime("%d-%m-%Y %H:%M")
    page = f"""<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Lanzamiento · revisión</title><style>
:root{{--bg:#0b0a1a;--card:#15132b;--fg:#ecebf7;--mut:#a7a3c7;--c:#00D4FF;--p:#EC4899;--v:#A78BFA;--ok:#34d399;--av:#fbbf24}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--fg);font:15px/1.5 Inter,system-ui,sans-serif;padding:24px max(16px,4vw)}}
h1{{font:800 30px/1.1 Anton,Impact,sans-serif;letter-spacing:.02em;margin:0 0 4px}}h2{{margin:32px 0 12px;font-size:18px;color:var(--c)}}
.sub{{color:var(--mut)}}.g{{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:16px}}
.c{{background:var(--card);border-radius:14px;overflow:hidden;border:1px solid #2a2750;display:flex;flex-direction:column}}
.c.aviso{{border-color:#5a4520}}.c.prog{{border-color:#3b2a66}}.m{{aspect-ratio:16/10;background:#000;display:flex;align-items:center;justify-content:center}}
.m img{{width:100%;height:100%;object-fit:contain}}.noimg{{color:var(--mut);font-size:13px}}.b{{padding:12px 14px 14px;display:flex;flex-direction:column;gap:4px}}
.p{{font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--v);font-weight:700}}h3{{margin:0;font-size:15px}}
.e{{font-size:13px;color:var(--ok)}}.aviso .e{{color:var(--av)}}.prog .e{{color:var(--v)}}p{{margin:4px 0 0;color:var(--mut);font-size:13px}}
a{{color:var(--c);font-weight:700;margin-top:6px;text-decoration:none}}a:hover{{text-decoration:underline}}
.box{{background:var(--card);border-radius:14px;padding:14px 18px;border:1px solid #2a2750}}li{{margin:4px 0}}
</style></head><body>
<h1>SkillUp Brandooers · lanzamiento</h1><div class="sub">Revisión de lo publicado y lo programado · datos de Zernio en directo · {now}</div>
<h2>Publicado en redes</h2><div class="g">{''.join(pub)}</div>
<h2>Skool</h2><div class="g">{''.join(skool)}</div>
<h2>Web, pódcast y boletín</h2><div class="g">{''.join(web)}</div>
<h2>Programado</h2><div class="g">{''.join(prog)}</div>
<h2>En preparación</h2><div class="box">{html.escape(rehacer)}</div>
<h2>Pendiente de ti</h2><div class="box"><ul>{''.join(f'<li>{html.escape(x)}</li>' for x in pendiente)}</ul></div>
</body></html>"""
    out = os.path.join(HERE, "index.html")
    open(out, "w", encoding="utf-8").write(page)
    print(out, len(pub), "published,", len(prog), "scheduled")


if __name__ == "__main__":
    main()
