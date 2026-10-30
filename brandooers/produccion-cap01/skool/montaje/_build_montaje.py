# Builds MONTAJE_SKOOL.md and montaje_skool.json from one source, so both stay in sync.
# Run: python _build_montaje.py  (reads ../catalogo/catalogo_cursos.json)
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
CAT = HERE.parent / "catalogo"
BANNERS = HERE.parent.parent / "serie_miniaturas" / "banners"
cat = json.loads((CAT / "catalogo_cursos.json").read_text(encoding="utf-8"))

OK = "HECHO"
CHK = "comprobar en pantalla"

# ---------------------------------------------------------------- texts
NOMBRE = "I+D+E · Innovación, Desarrollo IA y Estrategia"
DESCRIPCION = ("Para pymes, tiendas online y autónomos: cada semana una prueba en tu negocio, "
               "con IA y estrategia, y una cifra para saber si funcionó.")

AUTODM = ("Hola, #NAME#. Te doy la bienvenida a #GROUPNAME#. Para empezar, una pregunta: "
          "¿a qué te dedicas y qué quieres que sea distinto dentro de un mes? Contéstame aquí mismo y lo leo yo. "
          "Las dudas de los cursos, mejor en la categoría Pregunta a Marc del muro: así la respuesta sirve también a los demás. "
          "Y el primer paso, el curso Empieza aquí: veinte minutos y sales con tu primera prueba apuntada. Marc")

PREGUNTAS = [
    {"n": 1, "tipo": "Texto", "texto": "¿A qué te dedicas y qué quieres mejorar con IA y estrategia?",
     "por_que": "Decisión de Marc del 29-10 (SKOOL_PLAN §7): la comunidad ya no es solo de tiendas. Sirve para aceptar a mano y para que Marc salude con contexto."},
    {"n": 2, "tipo": "Opción múltiple",
     "texto": "¿Por dónde quieres empezar?",
     "opciones": ["Que mi tienda online venda más", "Trabajar con la IA en mi negocio",
                  "Que me encuentren y me elijan", "Ordenar mi estrategia y mis números",
                  "Probar ideas nuevas en mi negocio"],
     "por_que": "Cada opción es un bloque del aula (A, B, C, D, E). Dice qué curso recomendar en la bienvenida y qué bloque producir antes."},
    {"n": 3, "tipo": "Correo electrónico",
     "texto": ("Tu correo, para avisarte cuando se abra un curso nuevo. Lo usa solo SkillUp Brandooers, "
               "no se cede a nadie y puedes pedir la baja cuando quieras. Tienes la política de privacidad en brandooers.com."),
     "por_que": "Skool solo admite una pregunta de correo. Se activa SOLO después de que legal-rgpd-proteccion-datos revise el texto y la base legal; hasta entonces, se deja fuera y quedan 2 preguntas."},
]

CATEGORIAS = [
    ("Avisos", "Solo administradores", "Aperturas de cursos, vídeos de respuesta y cambios de la comunidad."),
    ("Preséntate", "Todos", "La primera publicación de cada miembro, con la plantilla fijada."),
    ("Pregunta a Marc", "Todos", "Dudas de los cursos. Marc contesta en el hilo; la respuesta sirve a todos."),
    ("Tu tienda vende más", "Todos", "Bloque A: pruebas y dudas de tiendas online."),
    ("Desarrollo con IA", "Todos", "Bloque B."),
    ("Visibilidad y captación", "Todos", "Bloque C."),
    ("Estrategia", "Todos", "Bloque D."),
    ("Innovación", "Todos", "Bloque E."),
    ("Victorias", "Todos", "Un cambio medido: antes, después y la cifra de la propia tienda o negocio."),
]

NIVELES = [
    (1, 0, "Recién llegado", "El muro, publicar, el chat con Marc y el curso «Empieza aquí»."),
    (2, 5, "Primera prueba", "El curso «Biblioteca de plantillas» (acceso por nivel 2, como dice el catálogo)."),
    (3, 20, "Con método", "Nada extra: el nivel se ve en el perfil y en la clasificación."),
    (4, 65, "Mide cada semana", "Nada extra."),
    (5, 155, "Ayuda a otros", "El curso «Que te encuentren» con acceso «nivel 5 O plan de pago» (desde que se abra). Que esto anime a pagar es suposición: se mide a los 28 días."),
    (6, 515, "Referente", "Nada extra."),
    (7, 2015, "Motor de la comunidad", "Nada extra."),
    (8, 8015, "Veterano I+D+E", "Nada extra."),
    (9, 33015, "Leyenda I+D+E", "Nada extra."),
]

ACERCA_TITULAR = "Aquí no se viene a ver vídeos. Se viene a probar una cosa cada semana en tu negocio y a medir si ha funcionado."
ACERCA = f"""{ACERCA_TITULAR}

Soy Marc Herrero. En YouTube y en el pódcast de SkillUp Brandooers cuento el porqué y el qué. Esta comunidad es la parte práctica: el cómo, con tu negocio delante.

Es para ti si tienes una pyme o una tienda online, o trabajas por tu cuenta, y quieres usar la inteligencia artificial con cabeza y una estrategia que quepa en una página. No hace falta saber programar ni ser experto en marketing. Hacen falta ganas de probar una cosa por semana.

Con la entrada gratis tienes:
- El curso «Empieza aquí»: el mapa de cursos y tu primera prueba apuntada en veinte minutos.
- El muro, para presentarte, preguntar y contar lo que has probado.
- «Pregunta a Marc»: dejas tu duda en el muro y te contesto yo, en público, para que la respuesta sirva a todos.
- La biblioteca de plantillas, que se abre en cuanto empiezas a participar.

Con el plan de pago, además:
- Los cursos de los cinco bloques: «Tu tienda vende más», «Desarrollo con IA», «Visibilidad y captación», «Estrategia» e «Innovación».
- Una práctica en cada lección, sobre tu propio negocio, y una lección de cierre para medir el cambio.
- Vídeos de respuesta con las dudas que más se repiten.
- Cursos nuevos a lo largo de los meses. Ves lo que viene desde el primer día.

Lo que no hacemos: no revisamos negocios uno a uno, no montamos webs ni tiendas y no vendemos servicios. Aquí aprendes a hacerlo tú, con método y con gente que está en lo mismo.

No hay promesas de ingresos. Hay una prueba por semana y una cifra para compararte contigo mismo.

En los vídeos, Marc aparece con un avatar y una voz generados con IA a partir de su imagen y su voz reales."""

POST_EMPIEZA = """Empieza aquí: tu primera semana

Hola. Esto es I+D+E, la parte práctica de SkillUp Brandooers. Tres cosas para esta semana:

1. Haz el curso «Empieza aquí» del aula. Son veinte minutos y sales con tu primera prueba apuntada.
2. Preséntate en la categoría «Preséntate» con la plantilla fijada. Qué haces, qué quieres mejorar y cuál es tu primera prueba.
3. Comenta la presentación de alguien que esté en lo mismo que tú. Una pregunta concreta vale más que un «me gusta».

Cómo funciona esto:
- El muro tiene una categoría por bloque. Publica tu prueba en la de su bloque y, cuando la midas, cuéntalo en «Victorias» con el antes y el después.
- Las dudas van en «Pregunta a Marc». Te contesto en el hilo.
- Verás cursos abiertos y cursos con candado. Los del candado están en preparación: en «Empieza aquí» tienes de qué irá cada uno y su índice.

Cuatro normas:
- Cifras tuyas, nunca datos de tus clientes.
- Aquí no se venden servicios ni se ponen enlaces de afiliado.
- Se critica la prueba, no a la persona.
- Una victoria lleva antes, después y la cifra.

En claro: una prueba por semana, medida contra ti mismo. ¿Cuál es la tuya?"""

POST_AYUDA = """Cómo pedir ayuda (y que sirva)

Una pregunta bien hecha se contesta a la primera. Publícala en «Pregunta a Marc» con estas cinco líneas:

1. A qué te dedicas: qué vendes o qué haces, y para quién.
2. Qué querías conseguir.
3. Qué has probado, en qué curso y en qué lección.
4. Qué ha pasado, con una cifra si la tienes (tuya, de antes y de después).
5. Qué necesitas saber exactamente.

Si añades una captura, que no salgan datos de tus clientes, contraseñas ni nada privado.

Te contesto en el hilo, en público, para que la respuesta sirva también a quien venga detrás. Si una duda se repite, la convierto en un vídeo de respuesta y lo aviso en «Avisos».

Lo que no va en el muro: cobros, planes, facturas y bajas. Eso escríbelo a info@brandooers.com y lo vemos en privado.

Y una cosa que no hago: revisar negocios uno a uno. Si haces la prueba de la lección y me cuentas qué te ha salido, te ayudo a leerlo."""

POST_PRESENTATE = """Preséntate: copia esta plantilla

Copia estas líneas en una publicación nueva de la categoría «Preséntate» y rellénalas:

Me llamo:
A qué me dedico (qué vendo o qué hago, y para quién):
Lo que quiero que sea distinto dentro de un mes:
Por dónde empiezo (bloque del aula):
Mi primera prueba y el día en que la mido:

Cuando la publiques, comenta la presentación de alguien que esté en lo mismo que tú. Así empieza esto: probando y contándolo."""

# ---------------------------------------------------------------- courses
cursos = sorted(cat["cursos"], key=lambda c: c["orden"])
assert len(cursos) == 27


def acceso_al_abrir(c):
    if c["orden"] == 1:
        return "Abierto"
    if c["orden"] == 2:
        return "Por nivel: nivel 2"
    if c["orden"] == 3:
        return "Privado + plan de pago O nivel 5"
    return "Privado + plan de pago"


def acceso_al_montar(c):
    if c["orden"] in (1, 2):
        return acceso_al_abrir(c)
    return "Privado, sin plan y sin miembros asignados (candado para todos)"


aula = []
for c in cursos:
    portada = f"{c['orden']:02d}_{c['slug']}_1460x752.jpg"
    assert (CAT / "portadas" / portada).exists(), portada
    prox = c["orden"] > 2
    aula.append({
        "orden": c["orden"],
        "bloque": c["bloque_nombre"],
        "titulo": c["titulo"],
        "estado_catalogo": c["estado"],
        "ola": c["ola"],
        "descripcion_al_montar": ("Próximamente · " if prox else "") + c["promesa"],
        "descripcion_al_abrir": c["promesa"],
        "portada": f"catalogo/portadas/{portada}",
        "acceso_al_montar": acceso_al_montar(c),
        "acceso_al_abrir": acceso_al_abrir(c),
        "publicado": "Sí (nunca en borrador: el borrador esconde el curso)",
        "leccion_introduccion": (f"Página 1 «Introducción»: texto de catalogo_cursos.json, cursos[orden={c['orden']}].intro "
                                 f"(CATALOGO_CURSOS.md §8, ficha {c['orden']}). "
                                 + ("Publicada." if not prox else "Sin publicar hasta el día de apertura.")),
        "indice": "Carpetas y páginas según cursos[].indice; páginas sin publicar hasta tener la lección.",
    })
    for k in ("descripcion_al_montar", "descripcion_al_abrir"):
        assert len(aula[-1][k]) <= 200, (c["orden"], k)

for nombre, _, _ in CATEGORIAS:
    assert len(nombre) <= 30, nombre
assert len(CATEGORIAS) <= 10
for t in (AUTODM,):
    assert "«" not in t and "»" not in t and "—" not in t and "…" not in t  # short chat copy: no angle quotes
for t in (AUTODM, ACERCA, POST_EMPIEZA, POST_AYUDA, POST_PRESENTATE, DESCRIPCION):
    low = t.lower()
    assert "boomatik" not in low and "odoo" not in low and "$" not in t and "€" not in t, t[:40]
for f in ("perfil_1080x1080.png", "facebook_portada_1640x624.jpg", "youtube_banner_2560x1440.jpg"):
    assert (BANNERS / f).exists(), f

# ---------------------------------------------------------------- structured steps
pasos = []


def paso(pantalla, campo, valor, verificado, fuente="", nota=""):
    pasos.append({"paso": len(pasos) + 1, "pantalla": pantalla, "campo": campo, "valor": valor,
                  "verificado": verificado, "fuente": fuente, "nota": nota})


G = "Ajustes › General"
paso(G, "Nombre del grupo", NOMBRE, CHK, "SKOOL_PLAN §7 (decisión de Marc)",
     "Límite de caracteres sin datos. Si lo corta, alternativa: «I+D+E · SkillUp Brandooers».")
paso(G, "Dirección (URL)", "skool.com/skillup-brandooers (alternativa: skool.com/ide-brandooers)", CHK,
     "help 121 y 176: dirección propia solo en Pro; los cambios después del primero se pagan",
     "Comprobar que está libre. Elegir bien a la primera.")
paso(G, "Descripción", DESCRIPCION, CHK, "help 153 (Discovery pide descripción)", f"{len(DESCRIPCION)} caracteres; límite sin datos.")
paso(G, "Icono del grupo", "serie_miniaturas/banners/perfil_1080x1080.png (los ojos de Brandooers)", CHK,
     "help 120: se cambia en General › CHANGE; no da medidas", "Cuadrado. Comprobar el recorte circular en pantalla.")
paso(G, "Portada del grupo", "serie_miniaturas/banners/facebook_portada_1640x624.jpg (provisional)", CHK,
     "help 120 no da medidas; help 153 y 245 (Discovery y anuncios usan la portada)",
     "Si el recorte corta el logotipo o el lema, se rehace a la medida que pida el cargador con la misma plantilla (facebook_portada_1640x624.html). Nunca la cara de Marc.")
paso(G, "Privacidad del grupo", "Privado (el contenido solo lo ven los miembros)", CHK, "", "")

P = "Ajustes › Precios"
paso(P, "Tipo de cobro", "Freemium: un plan gratis y un plan de pago", OK, "help 215")
paso(P, "Plan gratis", "Activo. Incluye el muro, «Empieza aquí» y la biblioteca por nivel 2.", OK, "help 215, 23")
paso(P, "Plan de pago · precio mensual", "9 (primer tramo: 10 miembros; Marc confirma la moneda)", OK,
     "help 86: Skool cobra en dólares y suma el IVA en la caja",
     "Escalera para nuevos (decisión de Marc): 9 hasta 10 altas de pago, 29 hasta 25, 49 hasta 50, 79 hasta 100. Quien ya paga conserva su precio (help 86). El cambio es a mano: el Manager crea la tarea al llegar a 10, 25, 50 y 100.")
paso(P, "Plan de pago · precio anual", "90 (10 veces el mes) o sin plan anual: decide Marc", OK,
     "help 215 e interfaz: el anual tiene que ser mayor que el mensual", "Quien elige anual conserva ese precio.")
paso(P, "Prueba gratis de 7 días", "Desactivada", OK, "help 215", "Recomendación: el plan gratis ya deja ver la comunidad y así las plazas cuentan altas de pago reales.")
paso(P, "Growth Boost", "Se deja como viene (activado)", OK, "help 226 y 245",
     "En freemium Skool no hace anuncios; no cuesta nada mientras no traiga a nadie de pago. Se revisa a los 90 días.")

Q = "Ajustes › Plugins › Preguntas de entrada"
for q in PREGUNTAS:
    paso(Q, f"Pregunta {q['n']} · {q['tipo']}", q["texto"] + (("  Opciones: " + " | ".join(q["opciones"])) if "opciones" in q else ""),
         OK, "help 57: máximo 3; tipos texto, opción múltiple y correo (uno solo); hay que contestarlas todas",
         q["por_que"] + (" Número máximo de opciones: comprobar en pantalla." if "opciones" in q else ""))

PL = "Ajustes › Plugins"
paso(PL, "AutoDM", AUTODM, OK, "help 64: un mensaje, 1 a 5 min tras el alta, variables #NAME# y #GROUPNAME#; no se envía si ya hay conversación",
     "Texto fijo escrito por Marc, no lo genera una IA. Remitente: Marc. Revisar con PREVIEW y encender.")
paso(PL, "Vídeo de bienvenida", "Vacío hasta tenerlo: avatar de Marc con su voz V4, 4K, coste en euros y OK de Marc antes de generar", OK, "help 176 (Pro)", "")
paso(PL, "Aprobación automática", "Apagada. Se acepta a mano a quien conteste con un negocio o proyecto real; se rechaza el spam.", OK, "help 176, 184", "")
paso(PL, "Enlaces del grupo (hasta 3)", "1) Capítulos gratis: https://brandooers.com/tu-tienda-vende-mas/?utm_source=skool&utm_medium=referral&utm_campaign=bdo-comunidad  2) Política de privacidad de brandooers.com  3) Libre (chat de ayuda cuando exista)",
     CHK, "help 76 (Pro, hasta 3)", "Es la única vía de enlace fuera de las lecciones, porque los de «Acerca de» no funcionan. Dónde se ven: comprobar.")
paso(PL, "Vídeo de baja", "Más adelante: recuerda, sin presión, que quien se va y vuelve paga el precio de ese día", OK, "help 170, 244", "")
paso(PL, "Chat por nivel", "Nivel 1 (todos pueden escribir a Marc). Subir a nivel 2 si entra spam.", OK, "help 176, 184", "")
paso(PL, "Publicar por nivel", "Nivel 1", OK, "help 176", "")

N = "Ajustes › Notificaciones (cuenta de Marc)"
paso(N, "Aviso por cada publicación nueva", "Activado, al correo de la cuenta de Marc", OK, "help 95",
     "El Manager lee ese aviso para preparar el borrador; Marc contesta a mano. Qué trae el correo: comprobar.")

C = "Muro › Categorías"
for i, (nombre, quien, uso) in enumerate(CATEGORIAS, 1):
    paso(C, f"Categoría {i}", nombre, OK, "help 67: hasta 10, 30 caracteres, quién publica", f"Publica: {quien}. {uso}")
paso(C, "Hueco 10", "Libre para la próxima ruta", OK, "help 67", "")

L = "Ajustes › Niveles"
for n, pts, nombre, abre in NIVELES:
    paso(L, f"Nivel {n} ({pts} puntos)", nombre, OK, "help 31 (umbrales), 145 (cursos por nivel)",
         f"Abre: {abre} Dónde se renombran los niveles: comprobar en pantalla.")

A = "Ajustes › Afiliados"
paso(A, "Afiliados de miembros", "Apagado al abrir. Al llegar a 25 altas de pago, decide Marc el porcentaje.", OK,
     "help 192, 187, 219 (Pro; cambiar el % afecta a todos; bajarlo daña la reputación)",
     "Sin datos de rango mínimo y máximo ni de lo que usan comunidades parecidas: por eso no se recomienda una cifra.")

Z = "Ajustes › Plugins › Zapier"
paso(Z, "Clave de Zapier", "Copiarla en Zapier. No se guarda en ningún documento. Cambiarla rompe los Zaps.", OK, "help 56", "")
paso(Z, "Zap 1", "Disparador Skool «New Paid Member» → Webhooks by Zapier POST → <URL_WEBHOOK_MANAGER_EDUCACION>, cabecera x-webhook-secret: <SECRETO_EN_ENV_LOCAL>. Campos: event=skool.new_paid_member, fecha, id de transacción.",
     OK, "help 56, 162; zapier.com/apps/skool/integrations",
     "Mínimo de datos: para contar la escalera bastan fecha e id. Nombre y correo solo con revisión de legal-rgpd-proteccion-datos. El punto de entrada del Manager aún no existe. Plan de Zapier con webhooks: sin datos.")
paso(Z, "Zap 2", "Disparador «Answered Membership Questions» → el mismo webhook con event=skool.membership_answers",
     OK, "help 59", "Solo después de la revisión legal. Las invitaciones por correo o CSV no cuentan como altas de pago.")

AB = "Página «Acerca de»"
paso(AB, "Texto", ACERCA, OK, "help 123: los enlaces del texto no funcionan; se suben imágenes y vídeos", "Sin enlaces, sin precios.")
paso(AB, "Imágenes y vídeo (en este orden)",
     "1) Vídeo de bienvenida cuando exista  2) serie_miniaturas/banners/youtube_banner_2560x1440.jpg  3) catalogo/portadas/01_empieza-aqui_1460x752.jpg  4) catalogo/portadas/03_que-te-encuentren_1460x752.jpg  5) catalogo/portadas/04_la-ia-como-socia_1460x752.jpg  6) catalogo/portadas/07_decide-con-datos_1460x752.jpg",
     CHK, "help 123 no da medidas ni número máximo", "Cuando haya lecciones grabadas, se añaden capturas reales de lecciones.")

AU = "Aula (Classroom)"
for c in aula:
    paso(AU, f"Curso {c['orden']:02d} · {c['titulo']}", c, OK if c["orden"] <= 2 else CHK,
         "help 23, 143, 145, 166 y CATALOGO_CURSOS.md §6",
         "Límite de caracteres de título y descripción y tamaño oficial de portada: sin datos (1460 × 752 es medida no oficial).")

paso("Calendario", "Eventos", "Ninguno por ahora: no hay directo semanal (decisión de Marc del 29-10)", OK,
     "memory: project_brandooers_skool_precio_escalera_soporte", "Si algún día hace falta, Skool Call está en los dos planes (help 210).")

F = "Muro › Publicaciones fijadas (máximo 3)"
paso(F, "Fijada 1 · categoría Avisos", POST_EMPIEZA, OK, "help 38", "Al abrir, enviarla por correo a todos (como mucho una vez cada 72 horas).")
paso(F, "Fijada 2 · categoría Pregunta a Marc", POST_AYUDA, OK, "help 38", "Correo de cobros y bajas: comprobar con Marc que es info@brandooers.com.")
paso(F, "Fijada 3 · categoría Preséntate", POST_PRESENTATE, OK, "help 38", "")

out = {
    "meta": {"fecha": "2026-10-29", "comunidad": NOMBRE, "plan_creador": "Pro",
             "estado": "Kit para pegar. No se ha entrado en Skool ni se ha creado, comprado o publicado nada.",
             "verificado": {"HECHO": "función o límite leído en help.skool.com (artículo citado)",
                            "comprobar en pantalla": "no consta en fuente oficial; se mira al montar"},
             "rutas_base": "relativas a .claude/scratch/l01/"},
    "pasos": pasos,
    "aula": aula,
    "decisiones_marc": [
        "Moneda (dólares) y si se abre ya el plan anual a 10 veces el mes.",
        "Dirección del grupo: skillup-brandooers o ide-brandooers (solo el primer cambio es gratis).",
        "Recompensa del nivel 5: abrir «Que te encuentren» con «nivel 5 O plan de pago», o ninguna.",
    ],
}
(HERE / "montaje_skool.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- markdown
md = []
w = md.append
w(f"# Montaje de Skool · {NOMBRE}\n")
w("Kit para configurar la comunidad de pago de SkillUp Brandooers en Skool, pantalla a pantalla, en cuanto Marc cree el grupo con el plan Pro. "
  "29-10-2026. No se ha entrado en Skool ni se ha creado, comprado o publicado nada. "
  "Las mismas instrucciones, en datos, están en `montaje_skool.json` (ambos salen de `_build_montaje.py`).\n")
w("**Cómo leerlo.** Cada casilla es un paso. «HECHO» = función o límite leído en el centro de ayuda de Skool (número de artículo de help.skool.com). "
  "**«comprobar en pantalla»** = no consta en ninguna fuente oficial: se mira al montarlo. Rutas de ficheros relativas a `.claude/scratch/l01/`.\n")
w("**Orden recomendado:** General → Precios → Plugins → Categorías → Niveles → Aula → Acerca de → Publicaciones fijadas → Zapier. Lo último, abrir la entrada.\n")


def bloque(titulo, filtro):
    w(f"\n## {titulo}\n")
    for p in pasos:
        if p["pantalla"] != filtro:
            continue
        v = p["valor"]
        multi = isinstance(v, str) and "\n" in v
        marca = "" if p["verificado"] == OK else " · **comprobar en pantalla**"
        if multi:
            w(f"- [ ] **{p['campo']}**{marca}\n")
            w("```text\n" + v + "\n```")
        else:
            w(f"- [ ] **{p['campo']}:** {v}{marca}")
        extra = " · ".join(x for x in (p["nota"], ("Fuente: " + p["fuente"]) if p["fuente"] else "") if x)
        if extra:
            w(f"  - {extra}")


bloque("1. Ajustes › General", G)
bloque("2. Ajustes › Precios (el único sitio con precios)", P)
bloque("3. Ajustes › Plugins › Preguntas de entrada (3, el máximo)", Q)
w("\nAceptación: a mano. Se acepta a quien conteste con un negocio o un proyecto real. Al resto, rechazo amable sin enlace (no hay mensaje automático al rechazar).")
bloque("4. Ajustes › Plugins (bienvenida, aprobación, enlaces, chat)", PL)
bloque("5. Ajustes › Notificaciones", N)
w("\n## 6. Muro › Categorías (en este orden)\n")
w("| # | Nombre | Quién publica | Para qué |\n|---|---|---|---|")
for i, (nombre, quien, uso) in enumerate(CATEGORIAS, 1):
    w(f"| {i} | {nombre} | {quien} | {uso} |")
w("| 10 | (libre) | — | Para la próxima ruta |")
w("\nHECHO: hasta 10 categorías de 30 caracteres, con quién publica (help 67). Orden del muro: «Nuevo».")
w("\n## 7. Ajustes › Niveles\n")
w("| Nivel | Puntos (Skool) | Nombre | Qué abre |\n|---|---|---|---|")
for n, pts, nombre, abre in NIVELES:
    w(f"| {n} | {pts:,}".replace(",", ".") + f" | {nombre} | {abre} |")
w("\nHECHO: umbrales y 1 punto por «me gusta» recibido (help 31); cursos por nivel (help 145). **Comprobar en pantalla** dónde se renombran los niveles: la ayuda solo dice que la clasificación enseña «los nombres de nivel propios de cada grupo». "
  "Nada de pedir «me gusta» a cambio de «me gusta»: Skool prohíbe cultivar puntos (help 179).")
bloque("8. Ajustes › Afiliados", A)
bloque("9. Ajustes › Plugins › Zapier (integración con BOO Manager)", Z)
w("\n## 10. Página «Acerca de»\n")
w(f"**Titular (primera línea):** {ACERCA_TITULAR}\n")
for p in pasos:
    if p["pantalla"] == AB and p["campo"] == "Texto":
        w("```text\n" + p["valor"] + "\n```")
w("\n- [ ] Sin un solo enlace: Skool no los activa en «Acerca de» (help 123). Los enlaces van en el plugin de enlaces y en las lecciones.")
for p in pasos:
    if p["pantalla"] == AB and p["campo"] != "Texto":
        w(f"- [ ] **{p['campo']}** · **comprobar en pantalla** (medidas y número máximo sin datos): {p['valor']}")
w("\n## 11. Aula (Classroom) · 27 cursos\n")
w("Método «próximamente» (CATALOGO_CURSOS.md §6, HECHO en help 23, 143, 145, 166): todos los cursos **publicados, nunca en borrador**. "
  "Los cerrados van en **Privado, sin plan y sin nadie asignado**: salen con candado para todos y con título y descripción legibles. "
  "Las lecciones se montan como páginas sin publicar. **El día que se abre cada uno:** se publican las páginas, se cambia el acceso a la columna «Al abrir», se quita «Próximamente · » de la descripción y se avisa en «Avisos». "
  "Nunca «Por nivel 9» ni «Por días» para fingir un «próximamente».\n")
w("**Ajuste en «Empieza aquí» (curso 01):** la lección 1.2 del índice dice «muro, directos y niveles»; ponerla como «Cómo funciona la comunidad: muro, ayuda y niveles», porque no hay directos. Y la 2.3 «Calendario de aperturas» se cuenta por olas, sin fechas que no estén decididas.\n")
w("| # | Curso | Bloque | Descripción al montar | Portada | Acceso al montar | Acceso al abrir | Ola |\n|---|---|---|---|---|---|---|---|")
for c in aula:
    w(f"| {c['orden']:02d} | {c['titulo']} | {c['bloque']} | {c['descripcion_al_montar']} | `{c['portada'].split('/')[-1]}` | {c['acceso_al_montar']} | {c['acceso_al_abrir']} | {c['ola']} |")
w("\n- **Lección 1 de cada curso, «Introducción»:** texto en `catalogo_cursos.json` → `cursos[orden=N].intro` (en el catálogo, §8, ficha N). Publicada en los cursos 01 y 02; sin publicar en el resto hasta su apertura.")
w("- **Índice:** carpetas y páginas según `cursos[].indice`, todas sin publicar hasta que la lección exista.")
w("- **Portadas:** carpeta `skool/catalogo/portadas/` (1460 × 752 JPG, medida no oficial; **comprobar en pantalla** el recorte).")
w("- **Comprobar en pantalla:** límite de caracteres del título (el más largo, el 27, tiene 54) y de la descripción (la más larga, 145); texto del candado con la interfaz en español; cómo ve un miembro gratis un curso Privado sin plan en un grupo freemium (cuenta de prueba gratis y otra de pago, con captura, antes de abrir).")
w("\n## 12. Calendario\n")
for p in pasos:
    if p["pantalla"] == "Calendario":
        w(f"- [ ] {p['valor']}. {p['nota']}")
w("\n## 13. Publicaciones fijadas (3, el máximo)\n")
w("HECHO: hasta 3 fijadas en el muro (help 38); correo a todos como mucho una vez cada 72 horas (interfaz de Skool).\n")
for p in pasos:
    if p["pantalla"] == F:
        w(f"### {p['campo']}\n")
        w("```text\n" + p["valor"] + "\n```")
        if p["nota"]:
            w(f"- {p['nota']}\n")
w("\n## 14. Antes de abrir la entrada\n")
w("- [ ] Cuenta de prueba en el plan gratis y otra en el de pago: captura de cómo se ve cada tipo de curso.")
w("- [ ] Revisión de legal-rgpd-proteccion-datos de la pregunta 3 y del Zap 1 con nombre y correo; de legal-publicidad-consumo del aviso de la escalera de precios en brandooers.com (precio final con IVA).")
w("- [ ] brand-separation-gate en verde: en ninguna pantalla sale otra marca de Marc ni su empresa, solo SkillUp Brandooers.")
w("- [ ] Ninguna extensión de terceros con la sesión de la cuenta dueña (condiciones de Skool, help 179 y 186).")
w("\n## Decisiones de Marc (3)\n")
for i, d in enumerate(out["decisiones_marc"], 1):
    w(f"{i}. {d}")
(HERE / "MONTAJE_SKOOL.md").write_text("\n".join(md) + "\n", encoding="utf-8")
print(f"OK · {len(pasos)} pasos · {len(aula)} cursos")
