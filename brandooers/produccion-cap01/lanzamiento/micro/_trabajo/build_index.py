"""Writes C01-IG-C1/copy.json + cover.jpg and micro/index.html (review page). Re-run after each change."""
import html, json, os
from PIL import Image

L01 = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
LZ = os.path.join(L01, "lanzamiento")
MICRO = os.path.join(LZ, "micro")
P = {x["id"]: x for x in json.load(open(os.path.join(LZ, "primeras", "primeras.json"), encoding="utf-8"))["piezas"]}
PROG = json.load(open(os.path.join(MICRO, "programado.json"), encoding="utf-8"))["pieces"]
AI_LINE = "Vídeo con mi avatar creado con IA."

# --- C01-IG-C1 package
c1 = P["C01-IG-C1"]; d = os.path.join(MICRO, "C01-IG-C1")
json.dump({"id": "C01-IG-C1", "red": "instagram", "cuenta": "6ae2dd79f681a077b3f325cb",
           "fecha_madrid": "mié 4-nov-2026 11:00", "scheduledFor_utc": PROG["C01-IG-C1"]["scheduledFor_utc"],
           "texto": c1["texto"], "hashtags": c1["hashtags"], "alt": c1["alt"],
           "imagenes": ["../../" + i for i in c1["imagenes"]],
           "etiqueta_ia": {"instagram.isAiGenerated": True}, "postId": PROG["C01-IG-C1"].get("postId")},
          open(os.path.join(d, "copy.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
Image.open(os.path.join(LZ, c1["imagenes"][0])).convert("RGB").save(os.path.join(d, "cover.jpg"), quality=90)

# --- pending video pieces (wait for the new «limpio» master); master seconds from the plan
VIDEO = [("C01-IG-R0", "dom 1-nov 20:30", "Instagram", "0.12–21.50"),
         ("C01-YT-S0", "lun 2-nov 19:00", "YouTube Short", "0.12–21.50"),
         ("C01-YT-S1", "mar 3-nov 13:00", "YouTube Short", "77.95–86.03 · 92.74–114.65"),
         ("C01-IG-R1", "mar 3-nov 20:30", "Instagram", "77.95–86.03 · 92.74–114.65"),
         ("C01-TT-1", "mié 4-nov 20:00", "TikTok", "77.95–86.03 · 92.74–114.65"),
         ("C01-YT-S2", "jue 5-nov 13:00", "YouTube Short", "158.84–174.50 · 183.33–195.12 · 224.09–228.95"),
         ("C01-IG-R2", "jue 5-nov 20:30", "Instagram", "158.84–174.50 · 183.33–195.12 · 224.09–228.95"),
         ("C01-YT-S3", "sáb 7-nov 13:00", "YouTube Short", "237.55–249.94 · 270.05–279.72 · 308.54–312.43"),
         ("C01-IG-R3", "sáb 7-nov 20:30", "Instagram", "237.55–249.94 · 270.05–279.72 · 308.54–312.43"),
         ("C01-TT-2", "dom 8-nov 20:00", "TikTok", "237.55–249.94 · 270.05–279.72 · 308.54–312.43")]
LINK = [("C01-IG-H3", "lun 2-nov 17:15", "Historia con enlace al capítulo"),
        ("C01-FB-P1", "lun 2-nov 17:30", "Facebook, enlace al capítulo"),
        ("C01-LI-P1", "lun 2-nov 17:30", "Página de LinkedIn, enlace en el primer comentario"),
        ("C01-IG-H5", "mié 4-nov 13:05", "Historia con enlace al minuto 7:10")]

e = html.escape
YT = "https://www.youtube.com/watch?v=xOx3j_BtZZY"
NOW = {k: v["fieldsSent"] for k, v in PROG.items() if v.get("publishedNow") and not v.get("postId")}
NOW_IMG = {"C01-IG-H3": os.path.join(LZ, P["C01-IG-H3"]["imagenes"][0]), "C01-IG-H5": os.path.join(LZ, P["C01-IG-H5"]["imagenes"][0]),
           "C01-IG-P1": os.path.join(MICRO, "C01-IG-P1", "ya_esta_capitulo1_1080x1350.png"),
           "C01-TT-P1": os.path.join(MICRO, "C01-TT-P1", "ya_esta_capitulo1_1080x1920.png")}


def text(s):
    return "<p>" + e(s).replace("\n\n", "</p><p>").replace("\n", "<br>") + "</p>"


def imgs(paths, alts):
    return '<div class="strip">' + "".join(
        f'<figure><img src="../{e(p)}" alt="{e(a)}" loading="lazy"><figcaption>{e(a)}</figcaption></figure>'
        for p, a in zip(paths, alts)) + "</div>"


def copybtn(s):
    return f'<button type="button" class="copy" data-t="{e(s)}">COPIAR TEXTO</button>'


li1, li2, h2, h4 = P["C01-LI-1"], P["C01-LI-2"], P["C01-IG-H2"], P["C01-IG-H4"]
li1_full = li1["texto"] + "\n\n" + li1["hashtags"]
li2_full = li2["texto"] + "\n\n" + li2["hashtags"]
c1_full = c1["texto"] + "\n\n" + c1["hashtags"]
prog = PROG["C01-IG-C1"]

page = f"""<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Microcontenidos capítulo 1</title>
<style>
:root{{--bg:#f6f5f8;--card:#fff;--ink:#17141f;--mute:#5d5868;--line:#e2dfe8;--ok:#1d7a46;--wait:#9a5b00;--acc:#6d28d9}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#121016;--card:#1c1922;--ink:#eeebf3;--mute:#a9a3b5;--line:#2e2a36;--ok:#5fd394;--wait:#f0b45a;--acc:#b49cff}}}}
:root[data-theme="dark"]{{--bg:#121016;--card:#1c1922;--ink:#eeebf3;--mute:#a9a3b5;--line:#2e2a36;--ok:#5fd394;--wait:#f0b45a;--acc:#b49cff}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--bg);color:var(--ink);font:16px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif}}
main{{max-width:980px;margin:0 auto;padding:24px 16px 64px}}h1{{font-size:1.6rem;margin:0 0 4px}}h2{{font-size:1.15rem;margin:36px 0 12px}}
.sub{{color:var(--mute);margin:0 0 8px}}.card{{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px;margin:12px 0}}
.head{{display:flex;flex-wrap:wrap;gap:8px 16px;align-items:baseline}}.id{{font-weight:700}}.when{{color:var(--mute)}}
.tag{{font-size:.8rem;font-weight:700;letter-spacing:.04em;padding:2px 8px;border-radius:99px;border:1px solid currentColor}}
.ok{{color:var(--ok)}}.wait{{color:var(--wait)}}.strip{{display:flex;gap:10px;overflow-x:auto;padding:8px 0}}
figure{{margin:0;flex:0 0 160px}}figure img{{width:160px;height:auto;border-radius:8px;border:1px solid var(--line);display:block}}
figcaption{{font-size:.75rem;color:var(--mute);margin-top:4px}}.copy{{background:var(--acc);color:#fff;border:0;border-radius:8px;padding:8px 14px;font-weight:700;letter-spacing:.04em;cursor:pointer}}
table{{width:100%;border-collapse:collapse;font-size:.92rem}}td,th{{text-align:left;padding:8px 6px;border-bottom:1px solid var(--line);vertical-align:top}}
.tw{{overflow-x:auto}}code{{font-size:.85em}}a{{color:var(--acc)}}
</style></head><body><main>
<h1>Capítulo 1 · microcontenidos</h1>
<p class="sub">Brandooers SkillUp · «Tu tienda vende más» · estreno lunes 2-nov-2026, 17:00 (Madrid). Horas en hora de Madrid.</p>

<h2>Listo para publicar ya (validado, sin publicar)</h2>
<p class="sub">Capítulo público desde el 29-oct: {e(YT)}. Zernio los ha validado; la publicación está pendiente de permiso.</p>
{''.join(f'<div class="card"><div class="head"><span class="id">{pid}</span><span class="tag wait">PENDIENTE</span></div>' + (f'<img src="{e(os.path.relpath(NOW_IMG[pid], MICRO).replace(chr(92), "/"))}" alt="" style="max-width:220px;border-radius:8px">' if pid in NOW_IMG else '') + text(NOW[pid]["content"] or "(historia: solo imagen, sin adhesivos)") + (text("Primer comentario: " + NOW[pid]["platforms"][0]["platformSpecificData"].get("firstComment","")) if pid=="C01-LI-P1" else "") + (text(NOW[pid]["tiktokSettings"]["description"]) if "tiktokSettings" in NOW[pid] else "") + '</div>' for pid in NOW)}
<h2>Programado en Zernio</h2>
<div class="card"><div class="head"><span class="id">C01-IG-C1</span><span class="when">Instagram · carrusel de 8 · mié 4-nov 11:00</span>
<span class="tag ok">PROGRAMADO</span></div>
<p class="sub">Post <code>{e(prog.get('postId') or '')}</code> · estado «{e(prog.get('status') or '')}» · {e(prog.get('scheduledFor_returned') or '')} UTC · etiqueta de IA de Instagram activada</p>
{imgs(c1['imagenes'], c1['alt'])}{text(c1_full)}</div>

<h2>Para Marc, a mano en su perfil de LinkedIn</h2>
<div class="card"><div class="head"><span class="id">C01-LI-1</span><span class="when">mar 3-nov 08:30 · texto + imagen 4:5</span><span class="tag wait">A MANO</span></div>
{imgs(li1['imagenes'], li1['alt'])}{text(li1_full)}
<p class="sub">Primer comentario: {e(li1['primer_comentario'])} (cuando el capítulo esté subido).</p>{copybtn(li1_full)}</div>
<div class="card"><div class="head"><span class="id">C01-LI-2</span><span class="when">jue 5-nov 08:30 · documento PDF de 8 páginas</span><span class="tag wait">A MANO</span></div>
<p><a href="../{e(li2['pdf'])}">Descargar el PDF del documento</a> · título sugerido del documento: «4 pruebas de 10 minutos: dónde se rompe tu tienda».</p>
{imgs(li2['imagenes'], li2['alt'])}{text(li2_full)}{copybtn(li2_full)}</div>

<h2>Historias como imagen, sin adhesivos</h2>
<p class="sub">Sin cuenta atrás ni test: la API no pone adhesivos. Programadas en Zernio como imagen sola.</p>
<div class="card"><div class="head"><span class="id">C01-IG-H2</span><span class="when">dom 1-nov 21:00 · historia</span><span class="tag wait">A ANULAR</span></div>
<p class="sub">Post <code>{e(PROG["C01-IG-H2"]["postId"])}</code> · {e(PROG["C01-IG-H2"]["scheduledFor_returned"])} UTC</p>
{imgs(h2['imagenes'], h2['alt'])}</div>
<div class="card"><div class="head"><span class="id">C01-IG-H4</span><span class="when">mié 4-nov 13:00 · historia</span><span class="tag ok">PROGRAMADO</span></div>
<p class="sub">Post <code>{e(PROG["C01-IG-H4"]["postId"])}</code> · {e(PROG["C01-IG-H4"]["scheduledFor_returned"])} UTC</p>
{imgs(h4['imagenes'], h4['alt'])}</div>

<h2>Esperan el enlace del capítulo en YouTube</h2>
<div class="card tw"><table><tr><th>Pieza</th><th>Cuándo</th><th>Qué es</th></tr>
{''.join(f'<tr><td>{a}</td><td>{b}</td><td>{e(c)}</td></tr>' for a, b, c in LINK)}</table></div>

<h2>Vídeos: esperan el nuevo máster</h2>
<p class="sub">Se cortarán del render «limpio» (sin subtítulos) del nuevo máster. Línea de IA donde la red no tenga casilla: «{e(AI_LINE)}»</p>
<div class="card tw"><table><tr><th>Pieza</th><th>Cuándo</th><th>Red</th><th>Tramos del capítulo (s)</th></tr>
{''.join(f'<tr><td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td></tr>' for a, b, c, d in VIDEO)}</table></div>
</main>
<script>document.querySelectorAll('.copy').forEach(b=>b.onclick=()=>{{navigator.clipboard.writeText(b.dataset.t).then(()=>{{b.textContent='COPIADO';setTimeout(()=>b.textContent='COPIAR TEXTO',1500)}}).catch(()=>{{}})}})</script>
</body></html>"""
open(os.path.join(MICRO, "index.html"), "w", encoding="utf-8").write(page)
print("ok", len(page))
