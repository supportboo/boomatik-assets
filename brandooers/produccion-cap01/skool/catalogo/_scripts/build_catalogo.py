"""Single source of truth for the Skool course catalogue of SkillUp Brandooers (I+D+E).

Run:  python -I build_catalogo.py
Reads the measured data in ../_datos/ (DataForSEO, YouTube, Skool Discovery) and writes
../catalogo_cursos.json and ../CATALOGO_CURSOS.md. Edit the data below, never the outputs.
"""
import json
import os
import statistics as st

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(HERE)
DAT = os.path.join(BASE, "_datos")
FECHA = "2026-10-29"

SV = {r["k"]: r["v"] for r in json.load(open(os.path.join(DAT, "sv_2724_es.json"), encoding="utf-8"))["filas"]}
IDEAS = {r["k"]: r["v"] for r in json.load(open(os.path.join(DAT, "ideas_2724_es.json"), encoding="utf-8"))["filas"]}
YT = json.load(open(os.path.join(DAT, "youtube_raw", "youtube_busquedas.json"), encoding="utf-8"))["busquedas"]
SK = json.load(open(os.path.join(DAT, "skool_raw", "skool_discovery.json"), encoding="utf-8"))["busquedas"]

COSTE_DATAFORSEO = {
    "total_usd": 0.191,
    "detalle": [
        ["google_ads/search_volume/live · 415 palabras", 0.09],
        ["google_ads/keywords_for_keywords/live · 20 semillas, 3.804 ideas", 0.09],
        ["google_trends/explore/live · 5 términos, 12 meses", 0.011],
    ],
    "metodo": "Saldo de la cuenta antes (10,888 USD) y después (10,697 USD), /v3/appendix/user_data",
}

SRC_SV = "DataForSEO · Google Ads search_volume, España (2724), español, leído el 29-10-2026; media mensual de 12 meses"
SRC_YT = "YouTube, página pública de resultados (hl=es, gl=ES), leída el 29-10-2026; mediana de visualizaciones de los ~20 primeros vídeos"
SRC_SK = "Skool Discovery, búsqueda pública con filtro de idioma español (lang=spanish), leída el 29-10-2026"


def kw(k):
    v = SV.get(k)
    if v is None:
        v = IDEAS.get(k)
    return {"keyword": k, "busquedas_mes": v, "certeza": "HECHO" if v is not None else "SIN DATOS", "fuente": SRC_SV}


def yt(q):
    b = YT[q]
    vs = [v["vistas_n"] for v in b.get("videos", []) if v.get("vistas_n")]
    top = max(b.get("videos", []), key=lambda v: v.get("vistas_n") or 0)
    return {"busqueda": q, "url": b["url"], "mediana_vistas_top20": int(st.median(vs)) if vs else None,
            "video_mas_visto": {"titulo": top["titulo"], "canal": top["canal"], "vistas": top["vistas_n"], "publicado": top["publicado"]},
            "certeza": "HECHO (cifras visibles en la página) · INFERENCIA (que reflejen demanda en España: la lista mezcla vídeos de otros países y en inglés)",
            "fuente": SRC_YT}


def sk(q):
    b = SK[q]
    paid = []
    for g in b["groups"]:
        try:
            p = json.loads(g.get("displayPrice") or "{}")
        except ValueError:
            p = {}
        if p.get("recurring_interval") == "month" and p.get("amount") and p["amount"] <= 100_00:
            paid.append(p["amount"] / 100)
    top = sorted(b["groups"], key=lambda g: -(g.get("members") or 0))[:3]
    return {"busqueda": q, "url": b["url"], "grupos_en_espanol": b["numGroups"],
            "mediana_precio_mensual_usd_30_primeros": st.median(paid) if paid else None,
            "mayores": [{"nombre": g["display"], "miembros": g["members"], "url": g["url"]} for g in top],
            "certeza": "HECHO (lo que muestra Skool) · INFERENCIA (precio = el que enseña la tarjeta; en grupos freemium puede ser el del plan de pago)",
            "fuente": SRC_SK}


# ---------------------------------------------------------------- catalogue data
# indice: [[modulo, [lecciones]]]; the first lesson of every course is «Introducción» (text in intro).
# puntos: demanda, encaje con el público, experiencia real, camino al pago (1-5 each).

BLOQUES = [
    {"id": "0", "nombre": "Empieza aquí", "letra": "Entrada",
     "para_que": "La puerta de la comunidad: qué es I+D+E, el mapa de cursos y tu primera semana. Gratis para todos."},
    {"id": "A", "nombre": "Tu tienda vende más", "letra": "Ruta e-commerce",
     "para_que": "La primera serie: los cuatro pasos en los que se rompe la venta online (encontrar, entender, comprar y pagar), más medir y temporadas."},
    {"id": "B", "nombre": "Desarrollo con IA", "letra": "D de I+D+E",
     "para_que": "Trabajar con la IA como socia: método, agentes, vídeo e imágenes."},
    {"id": "C", "nombre": "Visibilidad y captación", "letra": "Ruta marketing",
     "para_que": "Que te encuentren y te elijan: buscadores e IA, ficha de Google, anuncios, redes, correo y LinkedIn."},
    {"id": "D", "nombre": "Estrategia", "letra": "E de I+D+E",
     "para_que": "Poner orden: a quién vendes, a qué precio, con qué datos y en qué mercado."},
    {"id": "E", "nombre": "Innovación", "letra": "I de I+D+E",
     "para_que": "Aprender de los mejores, probar rápido y construir tus propias herramientas."},
]

INTRO_GENERAL = (
    "Te doy la bienvenida a I+D+E: Innovación, Desarrollo con IA y Estrategia. Soy Marc Herrero y esta es la parte "
    "práctica de SkillUp Brandooers. En YouTube y en brandooers.com cuento el porqué y el qué; aquí hacemos el cómo, "
    "con tu negocio delante.\n\n"
    "Esta comunidad es para ti si tienes una pyme o una tienda online, o si trabajas por tu cuenta, y quieres crecer "
    "usando la inteligencia artificial con cabeza y una estrategia que quepa en una página. No hace falta saber "
    "programar ni ser experto en marketing. Hacen falta ganas de probar una cosa cada semana y medirla.\n\n"
    "El aula está ordenada en cinco bloques. «Tu tienda vende más» es para quien vende online: encontrar, entender, "
    "comprar y pagar. «Desarrollo con IA» te enseña a trabajar con la IA como con una socia: método, agentes, vídeo e "
    "imágenes. «Visibilidad y captación» va de que te encuentren y te elijan: buscadores, ficha de Google, anuncios, "
    "redes y correo. «Estrategia» pone orden: cliente, precio, datos y mercado. E «Innovación» te da el método para "
    "aprender de los mejores, probar rápido y construir tus propias herramientas.\n\n"
    "Verás cursos abiertos y cursos con candado. Los del candado están en preparación: en este mismo curso tienes de "
    "qué irá cada uno y su índice, para que sepas lo que viene. Se irán abriendo a lo largo de los meses.\n\n"
    "Mi consejo: termina esta lección, haz el test del módulo 2 para saber qué curso te toca primero y publica tu "
    "presentación en el muro. A partir de ahí, una prueba por semana."
)

CURSOS = [
    # ------------------------------------------------------------------ bloque 0
    {"bloque": "0", "slug": "empieza-aqui", "titulo": "Empieza aquí: el mapa de I+D+E",
     "gancho": "EMPIEZA *AQUÍ*", "mascota": "dos ojos con luz (marca)",
     "promesa": "En veinte minutos sabes qué curso te toca primero y sales con tu primera prueba apuntada.",
     "para_quien": "Todos los miembros, gratis y desde el primer día.",
     "estado": "disponible", "ola": 1, "orden": 1, "acceso": "Abierto",
     "capitulos_youtube": [1], "material_base": ["capítulo 1", "hoja de los 4 pasos", "calculadora", "10 prompts"],
     "puntos": None,
     "indice": [
         ["Bienvenida", ["Introducción: qué es I+D+E y cómo se usa", "Cómo funciona la comunidad: muro, directos y niveles", "Las normas y lo que aquí no hacemos"]],
         ["El mapa de cursos", ["Los cinco bloques y su orden", "Test: qué curso te toca primero", "Calendario de aperturas"]],
         ["Tu primera semana", ["Si tienes tienda: encuentra tu paso roto (los 4 pasos y la calculadora)", "Si no: elige tu primera prueba", "Publica tu presentación"]],
         ["Lo que viene", ["Bloque «Tu tienda vende más»: de qué irá cada curso", "Bloque «Desarrollo con IA»", "Bloque «Visibilidad y captación»", "Bloque «Estrategia»", "Bloque «Innovación»"]],
     ],
     "intro": INTRO_GENERAL,
     "keywords": [], "youtube": None, "skool": None},

    {"bloque": "0", "slug": "biblioteca", "titulo": "Biblioteca de plantillas",
     "gancho": "TUS *PLANTILLAS*", "mascota": "lupa",
     "promesa": "Todas las hojas, plantillas, listas y prompts de la comunidad, ordenados por bloque y listos para usar.",
     "para_quien": "Miembros que ya se han presentado (se abre en el nivel 2).",
     "estado": "disponible", "ola": 1, "orden": 2, "acceso": "Por nivel: nivel 2 (5 puntos)",
     "capitulos_youtube": [1, 3, 4, 5, 6], "material_base": ["hoja de los 4 pasos", "calculadora", "biblioteca «Prompts para tu tienda»"],
     "puntos": None,
     "indice": [
         ["Cómo usar la biblioteca", ["Introducción", "Cómo pedir una plantilla nueva"]],
         ["Tienda", ["Hoja de los 4 pasos", "Las 7 comprobaciones antes de una campaña", "Prompts para tu tienda (enlace a la web)"]],
         ["IA", ["Ficha de tu negocio para la IA", "Plantilla de agente"]],
         ["Estrategia y datos", ["Estrategia en una página", "Hoja de precios y márgenes", "Cuadro semanal"]],
         ["Captación", ["Plantilla de imán", "Calendario de contenidos"]],
     ],
     "intro": (
         "Aquí está, ordenado por bloques, todo el material práctico de la comunidad: hojas, plantillas, listas de "
         "comprobación y prompts. Lo que ya está publicado gratis en brandooers.com no se copia aquí: se enlaza, para que "
         "siempre tengas la versión al día. Cada vez que se abre un curso, sus plantillas aparecen en su carpeta. "
         "Úsalas tal cual o adáptalas a tu negocio, y si echas en falta alguna, pídela en el muro con la etiqueta de su "
         "bloque. Las que más se pidan son las primeras que preparo. Esta biblioteca se abre en el nivel 2, que se "
         "consigue con cinco «me gusta» en tus publicaciones o comentarios: basta con presentarte y comentar la "
         "prueba de otra persona."
     ),
     "keywords": [], "youtube": None, "skool": None},

    # ------------------------------------------------------------------ bloque A
    {"bloque": "A", "slug": "que-te-encuentren", "titulo": "Que te encuentren",
     "gancho": "QUE TE *ENCUENTREN*", "mascota": "lupa",
     "promesa": "Tus productos aparecen en Google, en ChatGPT y en el buscador de tu tienda con las palabras que usa tu cliente.",
     "para_quien": "Dueños de tienda online con catálogo publicado, en cualquier plataforma.",
     "estado": "disponible", "ola": 1, "orden": 3, "acceso": "Privado + plan de pago",
     "capitulos_youtube": [1, 2], "material_base": ["capítulo 1 (paso 1)", "plan de lecciones del curso 1 en SKOOL_PLAN"],
     "puntos": {"demanda": 3, "encaje": 5, "experiencia": 5, "pago": 5},
     "indice": [
         ["Cómo te busca tu cliente", ["Introducción", "Las palabras de tu cliente: 20 términos de reseñas, preguntas y buscador", "Las preguntas que le hace a ChatGPT"]],
         ["Nombres y categorías", ["Renombra tus 10 más vendidos", "Categorías que se recorren en tres toques", "Fichas que responden la pregunta, para Google y para la IA"]],
         ["El buscador de tu tienda", ["Las búsquedas que no dan resultados", "Sinónimos y errores frecuentes"]],
         ["Fuera de tu tienda", ["Google Shopping y tu catálogo: lo básico", "Qué miran los asistentes de IA para recomendarte"]],
         ["Mide y compara", ["Visitas a ficha, semana contra semana", "Publica tu victoria con su cifra"]],
     ],
     "intro": (
         "Si tu tienda tiene buenos productos y poca gente llega a verlos, el problema suele estar en el primer paso: que "
         "te encuentren. En este curso trabajamos ese paso con tu tienda delante. Primero averiguamos cómo busca de verdad "
         "tu cliente, con sus palabras y no con las tuyas: las que usa en Google, las que escribe en el buscador de tu "
         "tienda y las preguntas que le hace a ChatGPT. Después renombras tus productos más vendidos, ordenas las "
         "categorías para que se llegue a cualquier ficha en tres toques y arreglas las búsquedas internas que hoy no "
         "devuelven nada. Al final vemos qué necesitan Google Shopping y los asistentes de IA para poder recomendarte. Es "
         "para ti si ya tienes una tienda online funcionando, sea cual sea la plataforma. Cada lección acaba con una "
         "práctica de menos de una hora. Cuando termines tendrás tu lista de palabras del cliente, tus diez fichas "
         "principales renombradas, un mapa de categorías claro y una cifra para comparar cada semana con la anterior."
     ),
     "keywords": ["google shopping", "google merchant center", "search console", "palabras clave", "seo ecommerce", "seo para tiendas online"],
     "youtube": "cómo vender más en tu tienda online", "skool": "tienda online"},

    {"bloque": "A", "slug": "ficha-en-5-segundos", "titulo": "La ficha que se entiende en 5 segundos",
     "gancho": "TU FICHA EN *5 SEGUNDOS*", "mascota": "lupa",
     "promesa": "Tu ficha responde qué es, para quién, cuánto mide y cuándo llega antes de que el cliente se vaya.",
     "para_quien": "Tiendas online cuyas visitas llegan a la ficha pero no añaden al carrito.",
     "estado": "disponible", "ola": 1, "orden": 7, "acceso": "Privado + plan de pago",
     "capitulos_youtube": [6, 7, 11], "material_base": ["prompt «La primera pantalla de tu ficha»"],
     "puntos": {"demanda": 2, "encaje": 5, "experiencia": 5, "pago": 5},
     "indice": [
         ["La primera pantalla", ["Introducción", "Qué decide el cliente en la primera pantalla del móvil", "La prueba del desconocido en tu ficha"]],
         ["Texto que vende sin sonar a IA", ["La descripción en cuatro bloques", "El prompt «La primera pantalla de tu ficha»", "Cómo quitarle el tono de IA"]],
         ["Fotos que responden", ["Las seis fotos que necesita cada ficha, con tu móvil", "Dónde ayuda la IA y dónde engaña"]],
         ["Dudas resueltas en la ficha", ["Las preguntas de tu cliente antes de comprar", "Preguntas frecuentes por ficha (plantilla)", "Opiniones: cómo pedirlas y mostrarlas"]],
         ["Mide y compara", ["Añadidos al carrito por ficha", "Publica tu antes y después"]],
     ],
     "intro": (
         "Tu cliente llega a la ficha y en unos segundos decide si sigue o se va. En ese rato tiene que entender qué es, "
         "si es para él, cuánto mide o qué incluye y cuándo le llega. En este curso rehacemos tus fichas para que "
         "respondan a eso a la primera. Empezamos por la primera pantalla del móvil, que es la que de verdad se ve. Luego "
         "escribes la descripción en cuatro bloques con ayuda de la IA, pero sin que suene a IA, y preparas las seis fotos "
         "que necesita cada producto con tu propio móvil. Después llevamos a la ficha las preguntas que hoy te hacen por "
         "correo o por WhatsApp, para que el cliente no tenga que hacerlas. Es para ti si vendes online y tus visitas "
         "llegan a las fichas pero no añaden al carrito. Saldrás con tus fichas principales rehechas, una plantilla para "
         "el resto del catálogo y la cifra de añadidos al carrito para compararla cada semana."
     ),
     "keywords": ["copywriting", "fichas de producto", "fotos de producto", "descripcion de producto"],
     "youtube": "cómo vender más en tu tienda online", "skool": "ecommerce"},

    {"bloque": "A", "slug": "carrito-sin-sustos", "titulo": "El carrito sin sustos",
     "gancho": "CARRITO SIN *SUSTOS*", "mascota": "lupa",
     "promesa": "El cliente ve el total, con envío y plazos, antes de darte ningún dato.",
     "para_quien": "Tiendas con carritos que se llenan y no llegan al pago.",
     "estado": "disponible", "ola": 1, "orden": 12, "acceso": "Privado + plan de pago",
     "capitulos_youtube": [5, 8], "material_base": ["prompt «El aviso de envío gratis»", "plantilla de devoluciones (pendiente de revisión legal)"],
     "puntos": {"demanda": 2, "encaje": 5, "experiencia": 4, "pago": 5},
     "indice": [
         ["Dónde se asusta el cliente", ["Introducción", "Recorre tu carrito como un desconocido", "Las sorpresas más comunes"]],
         ["Envío y plazos claros", ["¿Envío gratis? Las cuentas antes de decidir", "El aviso de envío gratis que sube el carrito", "Plazos de entrega que se entienden"]],
         ["Devoluciones que dan confianza", ["La política en lenguaje claro (plantilla)", "Dónde mostrarla"]],
         ["Menos pasos", ["Comprar sin registrarse", "Lo que sobra en tu carrito"]],
         ["Mide y compara", ["Carritos que pasan a pago", "Publica tu victoria"]],
     ],
     "intro": (
         "Muchas ventas se pierden en el carrito, cuando el cliente ya ha decidido comprar. Casi siempre por una sorpresa: "
         "un gasto de envío que no esperaba, un plazo que no se entiende, una política de devoluciones que asusta o un "
         "formulario que pide demasiado. En este curso recorres tu carrito como lo haría un desconocido y quitas esas "
         "sorpresas una a una. Hacemos las cuentas del envío gratis antes de decidir nada, para que no regales el margen, "
         "y escribimos el aviso que anima a sumar un producto más. Reescribes tu política de devoluciones en lenguaje "
         "claro, con una plantilla, y la colocas donde da confianza. Por último, quitamos los pasos que sobran. Es para ti "
         "si en tu tienda se llenan carritos que no llegan al pago. Terminarás con un carrito sin sorpresas, tus cuentas "
         "del envío en una hoja y la cifra de carritos que pasan a pago para seguirla cada semana."
     ),
     "keywords": ["politica de devoluciones", "carrito abandonado", "envio gratis tienda online"],
     "youtube": "por qué mi tienda online no vende", "skool": "ecommerce"},

    {"bloque": "A", "slug": "pagar-desde-el-movil", "titulo": "Pagar desde el móvil",
     "gancho": "PAGA DESDE EL *MÓVIL*", "mascota": "lupa",
     "promesa": "Compras de prueba desde el móvil sin atascos y un correo que recupera carritos sin perseguir a nadie.",
     "para_quien": "Tiendas con pedidos que se empiezan y no se pagan.",
     "estado": "proximamente", "ola": 2, "orden": 19, "acceso": "Privado + plan de pago",
     "capitulos_youtube": [4, 9], "material_base": ["prompt «Las sorpresas del pago»", "tres plantillas de correo de carrito (capítulo 9)"],
     "puntos": {"demanda": 1, "encaje": 5, "experiencia": 4, "pago": 4},
     "indice": [
         ["La compra de prueba", ["Introducción", "Haz una compra de prueba desde el móvil", "Las sorpresas del pago (prompt)"]],
         ["Formas de pago", ["Las que espera tu cliente", "Errores de pago y mensajes que se entienden"]],
         ["Recuperar sin perseguir", ["Tres correos de carrito (plantillas)", "Cuándo y cuántas veces, con permiso"]],
         ["Mide y compara", ["Pedidos pagados frente a iniciados", "Publica tu victoria"]],
     ],
     "intro": (
         "El último paso es el más caro de perder: el cliente ya quiere pagar y algo se lo impide. Suele pasar en el "
         "móvil, con un formulario incómodo, un método de pago que no está o un error que nadie entiende. En este curso "
         "haces compras de prueba desde tu propio móvil, como cualquier cliente, y apuntas cada tropiezo. Revisamos qué "
         "formas de pago espera tu público, cómo explicar los errores para que la gente no abandone y qué cambiar primero. "
         "Después preparamos tres correos de carrito abandonado que recuerdan sin agobiar, con la frecuencia justa y el "
         "permiso adecuado. Es para ti si tienes pedidos que se empiezan y no se pagan. Saldrás con tu lista de arreglos "
         "del pago ordenada por importancia, tus tres correos listos para tu herramienta de correo y la cifra de pedidos "
         "pagados frente a iniciados para compararla cada semana."
     ),
     "keywords": ["recuperar carritos abandonados", "carrito abandonado"],
     "youtube": "por qué mi tienda online no vende", "skool": "ecommerce"},

    {"bloque": "A", "slug": "tus-cinco-numeros", "titulo": "Medir y repetir: tus cinco números",
     "gancho": "TUS 5 *NÚMEROS*", "mascota": "lupa",
     "promesa": "Un cuadro semanal de cinco números para saber en qué paso pierdes la venta y si tu cambio funcionó.",
     "para_quien": "Tiendas que hacen cambios y no saben si funcionan.",
     "estado": "proximamente", "ola": 2, "orden": 18, "acceso": "Privado + plan de pago",
     "capitulos_youtube": [3, 13], "material_base": ["calculadora del paso que se rompe (brandooers.com/calculadora/)"],
     "no_repetir": "Solo los cinco números de una tienda y su ciclo semanal. Las herramientas (Analytics, Search Console, Clarity) se enseñan en «Decide con datos» y aquí se enlazan.",
     "puntos": {"demanda": 3, "encaje": 5, "experiencia": 5, "pago": 4},
     "indice": [
         ["Tus cinco números", ["Introducción", "Dónde sale cada número en tus estadísticas", "La calculadora del paso que se rompe"]],
         ["Compararte contigo", ["Semana contra semana", "Cuántos datos hacen falta para fiarte"]],
         ["El ciclo semanal", ["Una prueba por semana", "El diario de pruebas (plantilla)"]],
         ["Tu plan de 90 días", ["El plan en una página con los cuatro pasos", "Publica tu plan"]],
     ],
     "intro": (
         "Cambiar cosas en la tienda sin medir es ir a ciegas. En este curso montas un cuadro sencillo con cinco números "
         "que ya tienes en tus estadísticas, y con ellos sabes en qué paso pierdes la venta: encontrar, entender, comprar o "
         "pagar. Usamos la calculadora del paso que se rompe y aprendes a comparar tu tienda consigo misma, semana contra "
         "semana, en vez de con cifras de otros que no sabes de dónde salen. También vemos cuántos datos hacen falta para "
         "fiarte de un cambio y cuándo es pura casualidad. Con eso entras en el ciclo semanal: una prueba, una medida y una "
         "decisión. Al final lo juntas todo en un plan de 90 días en una sola página. Es para ti si haces cambios en tu "
         "tienda y no sabes si funcionan. Terminarás con tu cuadro semanal, tu diario de pruebas y tu plan de 90 días "
         "publicado en la comunidad."
     ),
     "keywords": ["kpi", "google analytics 4", "tasa de conversion ecommerce"],
     "youtube": "por qué mi tienda online no vende", "skool": "tienda online"},

    {"bloque": "A", "slug": "temporadas", "titulo": "Temporadas sin regalar el margen",
     "gancho": "REBAJAS SIN *REGALAR*", "mascota": "lupa",
     "promesa": "Preparas Black Friday, Navidad y rebajas con seis semanas de antelación y con las cuentas hechas.",
     "para_quien": "Tiendas a las que las campañas siempre pillan con prisas.",
     "estado": "proximamente", "ola": 2, "orden": 17, "acceso": "Privado + plan de pago",
     "capitulos_youtube": [4, 7, 10], "material_base": ["lista de las 7 comprobaciones", "hoja de margen en rebajas (capítulo 10, revisión legal del precio anterior)"],
     "puntos": {"demanda": 2, "encaje": 5, "experiencia": 4, "pago": 4},
     "indice": [
         ["Tu calendario", ["Introducción", "Las fechas que mueven tu sector", "Qué preparar seis semanas antes"]],
         ["Antes de lanzar", ["Las siete comprobaciones", "Productos que sí venden y hay en stock"]],
         ["Descuentos con cuentas", ["Hasta dónde puedes bajar (hoja de margen)", "El precio anterior en rebajas: lo que dice la norma"]],
         ["Navidad", ["Lo que pregunta el cliente antes de regalar", "Plazos y devoluciones de regalos"]],
         ["Después de la campaña", ["Medir y apuntar para el año que viene"]],
     ],
     "intro": (
         "Las campañas de temporada pueden salvarte el trimestre o comerse el margen. La diferencia casi siempre está en "
         "prepararlas con tiempo y con números. En este curso montas tu calendario de fechas, eliges qué productos empujar "
         "según lo que de verdad vendes y tienes en stock, y repasas las siete comprobaciones que conviene hacer antes de "
         "lanzar nada. Hacemos las cuentas del descuento en una hoja para saber hasta dónde puedes bajar, y vemos qué dice "
         "la norma sobre el precio anterior en rebajas para que no te metas en líos. Preparamos también lo que pregunta el "
         "cliente en Navidad: plazos, regalos y devoluciones. Y cuando acaba la campaña, la medimos y dejamos apuntado lo "
         "aprendido para el año siguiente. Es para ti si vendes online y las campañas te pillan siempre con prisas. "
         "Saldrás con tu calendario, tu hoja de márgenes y tu lista de comprobación."
     ),
     "keywords": ["descuentos", "cupones descuento", "campañas black friday", "rebajas tienda online"],
     "youtube": None, "skool": "ecommerce"},

    # ------------------------------------------------------------------ bloque B
    {"bloque": "B", "slug": "la-ia-como-socia", "titulo": "La IA como socia",
     "gancho": "LA IA COMO *SOCIA*", "mascota": "dos ojos con luz",
     "promesa": "Usas ChatGPT, Claude o Gemini con método: le das contexto, compruebas lo que dice y lo aplicas a tu negocio.",
     "para_quien": "Dueños de pyme y de tienda, autónomos y profesionales sin perfil técnico.",
     "estado": "disponible", "ola": 1, "orden": 3.5, "acceso": "Privado + plan de pago",
     "capitulos_youtube": [12], "material_base": ["10 prompts de brandooers.com", "pack «Seis preguntas antes de gastar» (capítulo 12)"],
     "puntos": {"demanda": 5, "encaje": 5, "experiencia": 4, "pago": 5},
     "indice": [
         ["Cómo trabaja la IA", ["Introducción", "Qué hace bien y en qué se equivoca", "Qué asistente para qué tarea"]],
         ["Pedir bien", ["El encargo en cinco partes: contexto, tarea, ejemplos, formato y límites", "La ficha de tu negocio para la IA", "Tu biblioteca de prompts"]],
         ["Comprobar antes de usar", ["Hecho, suposición o sin datos", "Cómo pedir fuentes y comprobarlas"]],
         ["Lo de cada semana", ["Textos y correos con tu voz", "Reseñas y preguntas de clientes", "Seis preguntas a la IA antes de gastar un euro"]],
         ["Con cabeza", ["Los datos que nunca le das", "Cuánto cuesta y cómo controlarlo"]],
     ],
     "intro": (
         "La IA no es magia ni es un juguete: es una socia que trabaja muy rápido, que a veces se equivoca con mucha "
         "seguridad y que rinde según lo bien que le expliques las cosas. En este curso aprendes a trabajar con ella con "
         "método. Primero vemos qué hace bien, en qué falla y qué asistente conviene para cada tarea. Después aprendes a "
         "hacer un buen encargo, con contexto, ejemplos, formato y límites, y preparas una ficha de tu negocio para que la "
         "IA hable con tu voz y conozca a tu cliente. Te enseño a comprobar lo que te dice antes de usarlo, separando lo "
         "que es un hecho de lo que es una suposición. Y lo aplicamos a lo de cada semana: textos, correos, reseñas, "
         "preguntas de clientes y decisiones de gasto. Es para ti si usas la IA de vez en cuando y quieres que te ahorre "
         "horas de verdad. Saldrás con tu ficha de negocio, tu biblioteca de prompts y una forma de trabajar que no "
         "depende de ninguna herramienta concreta."
     ),
     "keywords": ["curso ia", "cursos de ia", "curso inteligencia artificial", "prompts chatgpt", "prompt engineering", "chatgpt", "claude ai", "notebooklm"],
     "youtube": "chatgpt para negocios", "skool": "inteligencia artificial"},

    {"bloque": "B", "slug": "tu-equipo-de-agentes", "titulo": "Tu equipo de agentes",
     "gancho": "TU EQUIPO DE *AGENTES*", "mascota": "dos ojos con luz",
     "promesa": "Delegas tareas repetitivas en agentes de IA y automatizaciones sin programar, con límites y control de gasto.",
     "para_quien": "Negocios pequeños y autónomos a los que el día se les va en tareas repetitivas.",
     "estado": "disponible", "ola": 1, "orden": 8, "acceso": "Privado + plan de pago",
     "capitulos_youtube": [], "material_base": [],
     "puntos": {"demanda": 5, "encaje": 4, "experiencia": 5, "pago": 5},
     "indice": [
         ["Qué es un agente", ["Introducción", "Agente, automatización y asistente: en qué se diferencian", "Qué tareas delegar y cuáles no"]],
         ["Tu primer agente", ["La ficha del agente: papel, conocimiento y límites", "Darle tus documentos", "Probarlo antes de fiarte"]],
         ["Automatizaciones", ["Disparador, pasos y resultado", "Conectar correo, hojas y formularios", "Que no duplique ni se dispare solo"]],
         ["Un equipo que se coordina", ["Repartir el trabajo entre varios agentes", "Elegir el modelo según la tarea y el coste"]],
         ["Bajo control", ["Topes de gasto y registro", "Aprender de cada corrección"]],
     ],
     "intro": (
         "Hay tareas que repites cada semana y que una máquina puede hacer por ti: contestar lo de siempre, ordenar "
         "pedidos o contactos, preparar un informe o resumir correos. En este curso aprendes a delegarlas en agentes de IA "
         "y automatizaciones, sin programar. Empezamos por entender qué es un agente y qué tareas conviene delegar y "
         "cuáles no. Luego creas tu primer agente con su ficha: qué papel tiene, qué sabe de tu negocio y qué no puede "
         "hacer nunca. Después montamos automatizaciones que conectan tu correo, tus hojas y tus formularios, con cuidado "
         "para que no dupliquen nada ni se disparen solas. Y cuando tengas varios, te enseño a coordinarlos y a elegir el "
         "modelo adecuado para cada tarea según lo que cuesta. Es para ti si tu día se te va en tareas repetitivas. "
         "Terminarás con un agente funcionando, una automatización probada y un tope de gasto que no se pasa."
     ),
     "keywords": ["n8n", "zapier", "agentes ia", "agentes de ia", "automatizacion de procesos", "curso n8n"],
     "youtube": "agentes de ia tutorial español", "skool": "agentes ia"},

    {"bloque": "B", "slug": "tu-avatar-y-tu-voz", "titulo": "Vídeo con IA: tu avatar y tu voz",
     "gancho": "TU AVATAR *HABLA*", "mascota": "dos ojos con luz",
     "promesa": "Produces vídeos con tu avatar y tu voz clonada, con permiso, calidad y etiqueta de IA, sin grabarte cada semana.",
     "para_quien": "Quien quiere hacer vídeo para su negocio y no tiene tiempo de grabarse.",
     "estado": "disponible", "ola": 1, "orden": 13, "acceso": "Privado + plan de pago",
     "capitulos_youtube": [], "material_base": ["el propio capítulo 1 (avatar + voz)"],
     "puntos": {"demanda": 5, "encaje": 4, "experiencia": 5, "pago": 4},
     "indice": [
         ["Antes de empezar", ["Introducción", "Qué se puede hacer hoy y qué no", "Consentimiento, derechos y etiqueta de IA"]],
         ["Tu voz", ["Clonar tu voz bien", "Escribir para que suene natural: pausas y ritmo"]],
         ["Tu avatar", ["Grabar la toma base", "Encuadres, fondos y escenas"]],
         ["Guion y montaje", ["Gancho, capítulo y cierre", "Cortes, subtítulos y recursos sin tapar la cara"]],
         ["Calidad y publicación", ["Revisar sincronía, sonido y cortes antes de publicar", "Formatos para YouTube, Shorts y reels"]],
     ],
     "intro": (
         "Grabarte cada semana cuesta tiempo, luz, sitio y ganas. Con un avatar y tu voz clonada puedes publicar con "
         "constancia sin ponerte delante de la cámara cada vez. Así hago yo los capítulos de este canal, y en este curso te "
         "enseño a hacerlo bien. Empezamos por lo que no se negocia: tu consentimiento, los derechos de imagen y de voz, y "
         "cómo avisar de que el vídeo está hecho con IA. Después clonamos tu voz y aprendes a escribir para que suene "
         "natural, con pausas y ritmo de conversación. Grabas la toma base de tu avatar, eliges encuadres y escenas, y "
         "montamos un capítulo con gancho, cuerpo y cierre, con subtítulos y recursos que nunca tapan la cara. Antes de "
         "publicar revisamos la sincronía de la boca, el sonido y los cortes, porque un fallo pequeño se nota mucho. Es "
         "para ti si quieres hacer vídeo para tu negocio y no tienes tiempo de grabarte. Saldrás con tu voz, tu avatar y "
         "tu primer vídeo revisado."
     ),
     "keywords": ["elevenlabs", "heygen", "higgsfield", "crear videos con ia", "generar videos con ia", "video ia", "voz ia", "clonar voz", "avatar ia"],
     "youtube": "crear videos con ia", "skool": "videos con ia"},

    {"bloque": "B", "slug": "imagenes-con-ia", "titulo": "Imágenes con IA que no se notan",
     "gancho": "IA QUE *NO SE NOTA*", "mascota": "lupa",
     "promesa": "Creas imágenes de producto y de ambiente con IA fieles al producto real y sin aspecto artificial.",
     "para_quien": "Tiendas y negocios que hacen sus propias fotos y quieren más variedad.",
     "estado": "proximamente", "ola": 2, "orden": 21, "acceso": "Privado + plan de pago",
     "capitulos_youtube": [11], "material_base": [],
     "puntos": {"demanda": 4, "encaje": 4, "experiencia": 4, "pago": 3},
     "indice": [
         ["Antes de generar", ["Introducción", "El producto real primero: fotos de referencia", "Cuándo IA y cuándo el móvil"]],
         ["Pedir la imagen", ["El prompt con medidas, no con adjetivos", "Producto en contexto y fondos"]],
         ["Que no parezca IA", ["Los fallos que delatan una imagen", "Revisión antes de publicar"]],
         ["Texto e imagen", ["Por qué el texto no lo dibuja la IA", "Portadas y banners con plantilla"]],
         ["Coste y derechos", ["Cuánto cuesta cada imagen", "Licencias y uso comercial"]],
     ],
     "intro": (
         "La IA puede darte fotos de ambiente, fondos y variantes de producto que antes costaban una sesión de fotos. Pero "
         "si la imagen no se parece al producto real, o se nota que es artificial, pierdes la confianza del cliente. En "
         "este curso aprendes a generar imágenes que respetan tu producto y no delatan la IA. Partimos siempre del "
         "producto real: sus fotos, colores y detalles. Después aprendes a pedir la imagen con medidas y no con adjetivos, "
         "a colocar el producto en un contexto creíble y a revisar los fallos típicos antes de publicar: manos, reflejos, "
         "letras deformadas o piezas que no existen. Verás por qué el texto de una portada se compone aparte con una "
         "plantilla y no lo dibuja la IA. Y cerramos con lo práctico: cuánto cuesta cada imagen y qué licencias necesitas. "
         "Es para ti si haces tus propias fotos y quieres más variedad sin perder realismo. Saldrás con tu método de "
         "prompt, tu lista de revisión y tus primeras imágenes listas para la ficha."
     ),
     "keywords": ["nano banana", "midjourney", "crear imagenes con ia", "imagenes con ia", "fotos de producto"],
     "youtube": None, "skool": "inteligencia artificial"},

    # ------------------------------------------------------------------ bloque C
    {"bloque": "C", "slug": "que-la-ia-te-recomiende", "titulo": "Que Google y ChatGPT te recomienden",
     "gancho": "QUE LA IA TE *RECOMIENDE*", "mascota": "lupa",
     "promesa": "Tu web responde lo que pregunta tu cliente para que Google y los asistentes de IA la muestren y la citen.",
     "para_quien": "Negocios con web o tienda a los que casi nadie llega desde los buscadores.",
     "estado": "disponible", "ola": 1, "orden": 4, "acceso": "Privado + plan de pago",
     "capitulos_youtube": [2], "material_base": [],
     "puntos": {"demanda": 5, "encaje": 5, "experiencia": 5, "pago": 4},
     "indice": [
         ["Cómo se busca ahora", ["Introducción", "Google, las respuestas con IA y los asistentes: qué cambia", "Cómo saber si hoy te citan"]],
         ["Las preguntas de tu cliente", ["Palabras clave a partir de lo que vendes", "Qué quiere la persona detrás de cada búsqueda"]],
         ["Páginas que responden", ["Respuesta arriba y secciones que se entienden solas", "Quién firma y por qué fiarse", "Datos con fuente"]],
         ["Lo técnico imprescindible", ["Search Console paso a paso", "Indexación, velocidad y móvil"]],
         ["Medir", ["Clics, posiciones y citas", "Qué tocar cada mes"]],
     ],
     "intro": (
         "Cada vez más gente pregunta a ChatGPT o lee la respuesta de Google antes de entrar en ninguna web. Si tu página "
         "no responde bien a esas preguntas, ni te ven ni te citan. En este curso trabajamos el posicionamiento tal y como "
         "funciona hoy. Empezamos por ver cómo buscan tus clientes y cómo comprobar si los buscadores y los asistentes de "
         "IA te mencionan. Después sacamos las palabras clave a partir de lo que de verdad vendes, no de listas genéricas, "
         "y entendemos qué quiere la persona detrás de cada búsqueda. Rehacemos tus páginas para que respondan arriba, con "
         "secciones que se entienden por sí solas, firma real y datos con fuente. Te enseño a usar Search Console paso a "
         "paso y a revisar lo técnico imprescindible sin volverte loco. Es para ti si tienes web o tienda y casi nadie "
         "llega desde los buscadores. Saldrás con tu lista de preguntas del cliente, tus páginas clave rehechas y una "
         "revisión mensual que cabe en una hora."
     ),
     "keywords": ["google search console", "seo", "posicionamiento seo", "posicionamiento web", "curso seo", "ai overviews", "geo seo", "seo ia"],
     "youtube": "seo 2026 tutorial", "skool": "seo",
     "youtube_extra": "aparecer en chatgpt seo"},

    {"bloque": "C", "slug": "tu-ficha-de-google", "titulo": "Tu ficha de Google trae clientes",
     "gancho": "TU FICHA DE *GOOGLE*", "mascota": "lupa",
     "promesa": "Tu ficha de Google completa, con reseñas y publicaciones, para que te elija quien busca cerca.",
     "para_quien": "Negocios con local o que atienden en una zona concreta.",
     "estado": "proximamente", "ola": 2, "orden": 20, "acceso": "Privado + plan de pago",
     "capitulos_youtube": [], "material_base": [],
     "puntos": {"demanda": 4, "encaje": 4, "experiencia": 4, "pago": 3},
     "indice": [
         ["La ficha completa", ["Introducción", "Nombre, categorías y horarios sin errores", "Fotos reales que ayudan"]],
         ["Reseñas", ["Cómo pedirlas con enlace o código QR", "Cómo responderlas, también las malas"]],
         ["Publicaciones", ["Qué publicar cada semana", "Ofertas y eventos"]],
         ["Todo coherente", ["Nombre, dirección y teléfono iguales en todas partes", "Cambios que propone Google y suspensiones"]],
         ["Medir", ["Llamadas, rutas y visitas desde la ficha"]],
     ],
     "intro": (
         "Si tu negocio tiene local o trabajas en una zona concreta, tu ficha de Google puede traerte más clientes que tu "
         "web. Es lo primero que ve quien busca cerca, y muchas veces decide ahí mismo si te llama. En este curso la dejas "
         "completa y viva. Revisamos nombre, categorías, horarios y fotos para que no haya errores que te resten. Aprendes "
         "a pedir reseñas de forma natural, con un enlace o un código QR, y a responderlas todas, también las malas, sin "
         "meterte en problemas. Preparamos publicaciones sencillas para cada semana con tus novedades, ofertas o eventos. "
         "Comprobamos que tu nombre, tu dirección y tu teléfono son iguales en todas partes, y vemos qué hacer cuando "
         "Google cambia algo de tu ficha sin avisar. Es para ti si tienes un negocio local o de servicios por zona. Saldrás "
         "con tu ficha al día, tu sistema para conseguir reseñas y la cifra de llamadas y rutas que te trae cada mes."
     ),
     "keywords": ["google business profile", "reseñas google", "google mi negocio", "seo local", "ficha de google"],
     "youtube": "ficha de google business profile", "skool": "pymes"},

    {"bloque": "C", "slug": "anuncios-con-cuentas", "titulo": "Anuncios con las cuentas claras",
     "gancho": "ANUNCIOS CON *CUENTAS*", "mascota": "lupa",
     "promesa": "Lanzas anuncios en Meta y Google sabiendo cuánto puedes pagar por cliente y midiendo bien cada venta.",
     "para_quien": "Quien quiere anunciarse, o ya lo hace sin saber si le compensa.",
     "estado": "disponible", "ola": 1, "orden": 9, "acceso": "Privado + plan de pago",
     "capitulos_youtube": [], "material_base": [],
     "puntos": {"demanda": 5, "encaje": 4, "experiencia": 4, "pago": 4},
     "indice": [
         ["Antes de gastar", ["Introducción", "Cuánto puedes pagar por un cliente", "Medición lista antes del primer euro: conversiones y consentimiento"]],
         ["Meta: Instagram y Facebook", ["Una estructura sencilla", "Leer los resultados sin engañarte"]],
         ["Google", ["Búsquedas con intención clara", "Shopping si tienes tienda", "Palabras negativas"]],
         ["Creatividades", ["Ángulos y ganchos: una matriz de pruebas", "Cuándo una creatividad se cansa"]],
         ["Presupuesto y decisiones", ["Topes diarios y mensuales", "Subir, mantener o cortar"]],
     ],
     "intro": (
         "Los anuncios pueden acelerar un negocio o quemar dinero muy deprisa. La diferencia está en hacer las cuentas "
         "antes y en medir bien después. En este curso no empezamos por la plataforma, sino por tus números: cuánto puedes "
         "pagar por conseguir un cliente sin perder dinero. Después dejamos la medición lista antes de gastar el primer "
         "euro, con las conversiones bien registradas y el consentimiento en orden. Montamos campañas sencillas en Meta, "
         "para Instagram y Facebook, y en Google, con búsquedas de intención clara y Shopping si tienes tienda. Trabajamos "
         "las creatividades con ángulos y ganchos distintos para saber qué funciona con tu público, y aprendes a leer los "
         "resultados sin dejarte engañar por las cifras bonitas. Al final fijas topes de gasto y una regla para decidir "
         "cuándo subir, mantener o cortar. Es para ti si quieres anunciarte o ya lo haces sin tener claro si te compensa. "
         "Saldrás con tus cuentas, tu medición comprobada y tu primera campaña con tope."
     ),
     "keywords": ["google ads", "meta ads", "roas", "facebook ads", "tiktok ads", "curso google ads", "curso meta ads"],
     "youtube": "meta ads 2026 tutorial", "skool": "meta ads"},

    {"bloque": "C", "slug": "redes-con-metodo", "titulo": "Redes con método: un vídeo, muchas piezas",
     "gancho": "REDES CON *MÉTODO*", "mascota": "dos ojos con luz",
     "promesa": "Conviertes una pieza larga a la semana en cortos, carruseles y publicaciones para cada red, con un calendario que puedes mantener.",
     "para_quien": "Negocios y profesionales que saben que tienen que estar en redes y no saben cómo sostenerlo.",
     "estado": "proximamente", "ola": 2, "orden": 22, "acceso": "Privado + plan de pago",
     "capitulos_youtube": [], "material_base": ["plan de micropiezas por capítulo", "mecánica comentario a mensaje"],
     "condicion": "Se abre cuando la propia serie tenga 8 semanas medidas frente a su mediana (regla «solo lo probado»).",
     "puntos": {"demanda": 4, "encaje": 4, "experiencia": 3, "pago": 4},
     "indice": [
         ["El sistema", ["Introducción", "Lo corto da alcance, lo largo da autoridad y el correo da control", "En qué redes estar según tu cliente"]],
         ["La pieza de la semana", ["El tema desde las preguntas del cliente", "Guion con gancho"]],
         ["De una pieza a muchas", ["Cortes para Shorts, reels y TikTok", "Carruseles y documentos de LinkedIn", "Un texto para cada red"]],
         ["Comentarios que abren conversación", ["Una palabra clave por pieza", "Responder con permiso y sin agobiar"]],
         ["Calendario y medida", ["Un calendario que puedes mantener", "Comparar cada pieza con lo que suelen darte las tuyas"]],
     ],
     "intro": (
         "Publicar en todas las redes cada día agota a cualquiera. La alternativa es trabajar con un sistema: una pieza "
         "larga a la semana y, a partir de ella, todo lo demás. En este curso te enseño ese método, el mismo que aplico con "
         "este canal. Primero decidimos en qué redes estar según dónde está tu cliente, no según la moda. Luego eliges el "
         "tema de la semana a partir de las preguntas reales de tus clientes y escribes un guion con gancho. De esa pieza "
         "sacamos cortos para Shorts, reels y TikTok, carruseles, documentos para LinkedIn y un texto adaptado a cada red. "
         "Aprendes a convertir los comentarios en conversaciones, con una palabra clave por pieza y siempre con permiso. Y "
         "lo ordenamos todo en un calendario que puedas mantener, midiendo cada pieza frente a lo que suelen darte las "
         "tuyas. Es para ti si sabes que tienes que estar en redes y no sabes cómo sostenerlo. Saldrás con tu sistema "
         "semanal y tu calendario del mes."
     ),
     "keywords": ["youtube shorts", "community manager", "reels instagram", "marca personal", "carrusel instagram", "curso community manager", "calendario de contenidos"],
     "youtube": "crear un canal de youtube con ia", "skool": "redes sociales"},

    {"bloque": "C", "slug": "tu-lista-de-correo", "titulo": "Correo que vende: imanes, boletín y secuencias",
     "gancho": "TU LISTA DE *CORREO*", "mascota": "dos ojos con luz",
     "promesa": "Construyes tu propia lista con un recurso útil y un boletín que la gente quiere abrir, con permiso y sin depender de ninguna red.",
     "para_quien": "Negocios que dependen de las redes o de los anuncios para que les encuentren.",
     "estado": "disponible", "ola": 1, "orden": 14, "acceso": "Privado + plan de pago",
     "capitulos_youtube": [9], "material_base": ["boletín de Substack con bienvenida automática", "hoja de los 4 pasos como imán"],
     "puntos": {"demanda": 4, "encaje": 4, "experiencia": 4, "pago": 4},
     "indice": [
         ["Por qué el correo", ["Introducción", "Lo que no controlas en redes y sí en tu lista"]],
         ["El imán", ["Un recurso que tu cliente quiere de verdad", "Hojas, plantillas y calculadoras"]],
         ["Permiso y ley", ["Consentimiento con prueba y doble confirmación", "Baja en un clic"]],
         ["Boletín y secuencias", ["El correo de bienvenida", "Una carta por semana", "Secuencias antes y después de la compra"]],
         ["Medir", ["Altas, aperturas, clics y bajas", "Qué cambiar cuando no se abre"]],
     ],
     "intro": (
         "Las redes te prestan la audiencia; tu lista de correo es tuya. Si mañana cambia un algoritmo, tus suscriptores "
         "siguen ahí. En este curso construyes esa lista paso a paso. Empezamos por el imán: un recurso que tu cliente "
         "quiere de verdad, como una hoja, una plantilla o una calculadora, y no un PDF genérico. Lo hacemos con el permiso "
         "en regla, con casilla sin marcar, doble confirmación y baja en un clic, para cumplir la ley y para que tus "
         "correos lleguen. Después escribimos el correo de bienvenida, montamos una carta semanal que se lee con gusto y "
         "preparamos secuencias que acompañan al cliente antes y después de comprar. Y aprendemos a medir altas, "
         "aperturas, clics y bajas para mejorar cada mes. Es para ti si dependes de las redes o de los anuncios para que "
         "te encuentren. Saldrás con tu imán publicado, tu bienvenida automática y tu primera carta enviada."
     ),
     "keywords": ["substack", "email marketing", "newsletter", "funnel de ventas", "lead magnet", "embudo de ventas"],
     "youtube": "email marketing tutorial", "skool": "marketing digital"},

    {"bloque": "C", "slug": "linkedin-sin-agobiar", "titulo": "LinkedIn para vender sin parecer vendedor",
     "gancho": "LINKEDIN SIN *AGOBIAR*", "mascota": "dos ojos con luz",
     "promesa": "Conviertes tu perfil y tus publicaciones de LinkedIn en conversaciones con clientes, a mano y sin automatismos prohibidos.",
     "para_quien": "Autónomos, consultores y quien vende a otras empresas.",
     "estado": "proximamente", "ola": 3, "orden": 24, "acceso": "Privado + plan de pago",
     "capitulos_youtube": [], "material_base": [],
     "puntos": {"demanda": 2, "encaje": 3, "experiencia": 3, "pago": 3},
     "indice": [
         ["El perfil", ["Introducción", "El perfil como página de aterrizaje", "Titular y extracto que dicen a quién ayudas"]],
         ["Publicar", ["Publicaciones que hacen pensar, no que informan", "Documentos y carruseles"]],
         ["Conversar", ["Comentarios con valor", "Invitaciones personales", "Del mensaje a la llamada, con permiso"]],
         ["Ritmo y medida", ["Una rutina de veinte minutos al día", "Qué medir: conversaciones, no «me gusta»"]],
     ],
     "intro": (
         "Si vendes servicios o trabajas con otras empresas, LinkedIn es el sitio donde están tus clientes. Pero casi todo "
         "el mundo lo usa mal: publica noticias que nadie comenta o manda mensajes de venta a desconocidos. En este curso "
         "aprendes a usarlo para tener conversaciones de verdad. Convertimos tu perfil en una página que dice en segundos a "
         "quién ayudas y cómo. Escribes publicaciones en primera persona que hacen pensar en vez de informar, y aprendes a "
         "comentar con criterio en las publicaciones de tus posibles clientes. Después vemos cómo invitar a contactos con "
         "un mensaje personal y cómo pasar de un intercambio a una llamada, siempre con permiso y sin herramientas que "
         "LinkedIn prohíbe. Todo cabe en una rutina de veinte minutos al día. Es para ti si eres autónomo, consultor o "
         "vendes a empresas. Saldrás con tu perfil rehecho, tu rutina diaria y tus primeras conversaciones abiertas."
     ),
     "keywords": ["linkedin ads", "curso linkedin", "linkedin para empresas", "perfil de linkedin", "social selling"],
     "youtube": "marca personal linkedin", "skool": "marca personal"},

    # ------------------------------------------------------------------ bloque D
    {"bloque": "D", "slug": "estrategia-en-una-pagina", "titulo": "Tu estrategia en una página",
     "gancho": "ESTRATEGIA EN *1 PÁGINA*", "mascota": "dos ojos con luz",
     "promesa": "Decides a quién vendes, por qué te eligen y qué haces los próximos 90 días, todo en una página.",
     "para_quien": "Dueños de pyme y autónomos que sienten que van apagando fuegos sin rumbo.",
     "estado": "disponible", "ola": 1, "orden": 10, "acceso": "Privado + plan de pago",
     "capitulos_youtube": [13], "material_base": ["plan de 90 días en una página (capítulo 13)"],
     "puntos": {"demanda": 4, "encaje": 5, "experiencia": 4, "pago": 4},
     "indice": [
         ["Dónde juegas", ["Introducción", "Tu cliente ideal, con sus palabras", "Frente a qué alternativas compites de verdad"]],
         ["Por qué te eligen", ["Tu propuesta de valor", "Lo que solo tú puedes demostrar"]],
         ["Tu modelo en una hoja", ["El lienzo del modelo de negocio, sin rellenar por rellenar", "Lo que dejas de hacer"]],
         ["Plan de 90 días", ["Tres objetivos medibles", "Pruebas semanales y revisión mensual"]],
     ],
     "intro": (
         "Muchos negocios hacen muchas cosas a la vez y ninguna del todo bien. No por falta de ganas, sino porque nadie ha "
         "decidido con claridad para quién trabajan y por qué les tendrían que elegir. En este curso tomamos esas "
         "decisiones y las dejamos en una sola página. Empezamos por tu cliente ideal, descrito con sus propias palabras y "
         "no con una ficha inventada. Vemos frente a qué alternativas compites de verdad, que a veces no es la competencia "
         "que crees, y escribimos tu propuesta de valor con lo que puedes demostrar. Repasamos tu modelo de negocio en una "
         "hoja y, lo más difícil, decidimos qué dejas de hacer. Con todo eso montamos un plan de 90 días con tres "
         "objetivos medibles, pruebas semanales y una revisión al mes. Es para ti si tienes la sensación de ir apagando "
         "fuegos sin rumbo. Saldrás con tu estrategia en una página, lista para colgarla en la pared y revisarla cada mes."
     ),
     "keywords": ["modelo canvas", "buyer persona", "propuesta de valor", "plan de marketing", "modelo de negocio", "plan de negocio", "estrategia de marketing"],
     "youtube": "modelo de negocio canvas explicado", "skool": "estrategia"},

    {"bloque": "D", "slug": "precios-con-margen", "titulo": "Precios que dejan margen",
     "gancho": "PRECIOS CON *MARGEN*", "mascota": "lupa",
     "promesa": "Calculas tu precio desde tus costes, tu valor y tu competencia, y sabes cuánto puedes descontar sin perder dinero.",
     "para_quien": "Quien trabaja mucho y tiene la sensación de ganar poco.",
     "estado": "disponible", "ola": 1, "orden": 15, "acceso": "Privado + plan de pago",
     "capitulos_youtube": [5, 10], "material_base": ["hoja de margen en rebajas (capítulo 10)"],
     "puntos": {"demanda": 3, "encaje": 5, "experiencia": 4, "pago": 4},
     "indice": [
         ["Tus números", ["Introducción", "El coste real de lo que vendes, también tu tiempo", "Margen y punto muerto"]],
         ["Poner precio", ["Desde el coste, el valor y la competencia", "Tres niveles: entrada, recomendado y completo"]],
         ["Descuentos y envíos", ["Cuánto puedes descontar", "Envío gratis: cuándo sale a cuenta"]],
         ["Subir precios", ["Cuándo y cómo anunciarlo", "Qué pasa con los clientes que ya tienes"]],
         ["La caja", ["El flujo de caja en una hoja"]],
     ],
     "intro": (
         "El precio es la decisión que más dinero mueve y la que menos se piensa. Muchas veces se copia el de la "
         "competencia o se pone a ojo, y luego los descuentos se comen lo poco que queda. En este curso calculas tus "
         "precios con números. Primero sacamos el coste real de lo que vendes, incluido tu tiempo, y vemos cuánto tienes "
         "que vender para no perder dinero. Después ponemos precio desde tres miradas: lo que te cuesta, lo que vale para "
         "tu cliente y lo que cobran otros. Aprendes a ofrecer niveles, uno de entrada, uno recomendado y uno completo, "
         "para que cada cliente elija. Hacemos las cuentas de descuentos y envíos gratis antes de lanzarlos y vemos cómo "
         "subir precios sin perder a quien ya te compra. Cerramos con una hoja de caja sencilla para saber cómo vas cada "
         "mes. Es para ti si trabajas mucho y tienes la sensación de ganar poco. Saldrás con tu hoja de precios y márgenes "
         "y tus reglas de descuento."
     ),
     "keywords": ["rentabilidad", "flujo de caja", "margen de beneficio", "calcular margen", "estrategia de precios", "como poner precio a un producto"],
     "youtube": "cómo fijar el precio de tu producto", "skool": "emprendedores"},

    {"bloque": "D", "slug": "decide-con-datos", "titulo": "Decide con datos",
     "gancho": "DECIDE CON *DATOS*", "mascota": "lupa",
     "promesa": "Montas tu cuadro de mando con Analytics, Search Console y Clarity y separas lo que es un hecho de lo que es una suposición.",
     "para_quien": "Negocios que tienen datos y no saben qué hacer con ellos.",
     "estado": "disponible", "ola": 1, "orden": 6, "acceso": "Privado + plan de pago",
     "capitulos_youtube": [3], "material_base": [],
     "no_repetir": "Herramientas y cuadro general para cualquier negocio. Los cinco números de una tienda van en «Medir y repetir».",
     "puntos": {"demanda": 5, "encaje": 4, "experiencia": 5, "pago": 4},
     "indice": [
         ["Qué medir", ["Introducción", "De la decisión a la cifra", "Hecho, suposición o sin datos"]],
         ["Tus fuentes", ["Google Analytics 4 sin perderte", "Search Console", "Clarity: ver dónde se atasca la gente"]],
         ["Tu cuadro", ["Un cuadro de mando en una pantalla", "Que se actualice solo"]],
         ["Leer bien", ["Compararte contigo, no con medias ajenas", "Coincidencia no es causa", "Cuándo un cambio es real"]],
         ["La rutina", ["Quince minutos a la semana y una hora al mes"]],
     ],
     "intro": (
         "Casi todos los negocios tienen datos y casi ninguno decide con ellos. O se miran demasiadas cifras, o se miran "
         "las que no importan, o se sacan conclusiones de dos días de visitas. En este curso montas un cuadro de mando que "
         "se entiende de un vistazo y te ayuda a decidir. Empezamos al revés de lo habitual: primero la decisión que "
         "quieres tomar y después la cifra que la responde. Te enseño una costumbre que cambia mucho: marcar cada dato "
         "como hecho, suposición o sin datos. Después aprendes a sacar lo importante de Google Analytics, de Search Console "
         "y de Clarity, que te deja ver dónde se atasca la gente en tu web. Lo juntamos en una sola pantalla que se "
         "actualiza sola y aprendes a leerla bien: comparar tu negocio consigo mismo, no confundir coincidencia con causa "
         "y saber cuándo un cambio es real. Es para ti si tienes datos y no sabes qué hacer con ellos. Saldrás con tu "
         "cuadro de mando y tu rutina semanal de quince minutos."
     ),
     "keywords": ["google analytics", "search console", "kpi", "dashboard", "looker studio", "google analytics 4", "microsoft clarity", "cuadro de mando"],
     "youtube": None, "skool": "marketing digital"},

    {"bloque": "D", "slug": "hay-demanda", "titulo": "¿Hay demanda? Investiga tu mercado con datos",
     "gancho": "¿HAY *DEMANDA*?", "mascota": "lupa",
     "promesa": "Antes de lanzar algo, mides cuánta gente lo busca, quién compite y qué dicen los clientes, con fuentes que puedes citar.",
     "para_quien": "Quien va a tomar una decisión importante y no quiere hacerlo a ciegas.",
     "estado": "proximamente", "ola": 2, "orden": 23, "acceso": "Privado + plan de pago",
     "capitulos_youtube": [], "material_base": ["este mismo estudio de catálogo como ejemplo"],
     "puntos": {"demanda": 3, "encaje": 4, "experiencia": 5, "pago": 3},
     "indice": [
         ["La pregunta", ["Introducción", "De una idea a una pregunta que se puede responder"]],
         ["Demanda", ["Volúmenes de búsqueda y tendencias", "Estadística oficial para dimensionar"]],
         ["Competencia", ["Quién compite de verdad: búsqueda, anuncios y oferta", "Precios y mensajes"]],
         ["La voz del cliente", ["Reseñas, foros y preguntas reales", "Sus palabras para tus textos"]],
         ["Decidir", ["El informe de una página, con certeza por dato"]],
     ],
     "intro": (
         "Antes de lanzar un producto, abrir una línea nueva o invertir en una campaña, conviene saber si hay gente que lo "
         "quiere. Y eso se puede averiguar con datos, sin encuestas caras ni corazonadas. En este curso aprendes a "
         "investigar tu mercado como lo hemos hecho para preparar el aula de esta comunidad. Primero conviertes la idea en "
         "una pregunta concreta. Después mides la demanda con volúmenes de búsqueda y tendencias, y la dimensionas con "
         "estadística oficial. Analizas quién compite de verdad, qué ofrece, a qué precio y con qué mensajes. Y escuchas al "
         "cliente donde habla sin filtro, en reseñas, foros y preguntas reales, apuntando sus palabras para usarlas luego "
         "en tus textos. Todo termina en un informe de una página en el que cada dato lleva su fuente y su grado de "
         "certeza. Es para ti si vas a tomar una decisión importante y no quieres hacerlo a ciegas. Saldrás con tu "
         "método, tus fuentes y tu primer informe."
     ),
     "keywords": ["google trends", "buyer persona", "estudio de mercado", "palabras clave", "analisis de la competencia", "como hacer un estudio de mercado"],
     "youtube": None, "skool": "estrategia"},

    {"bloque": "D", "slug": "marketing-sin-multas", "titulo": "Marketing sin multas",
     "gancho": "MARKETING SIN *MULTAS*", "mascota": "lupa",
     "promesa": "Sabes qué exige la ley a tus correos, cookies, anuncios, reseñas y contenidos con IA, y cuándo llamar a tu asesoría.",
     "para_quien": "Quien hace marketing por su cuenta y quiere evitar sustos legales.",
     "estado": "proximamente", "ola": 3, "orden": 25, "acceso": "Privado + plan de pago",
     "capitulos_youtube": [8, 10], "material_base": [],
     "condicion": "Cada lección pasa por la revisión de los agentes legales y, antes de abrir, por la asesoría de Marc.",
     "puntos": {"demanda": 3, "encaje": 4, "experiencia": 3, "pago": 2},
     "indice": [
         ["Lo básico", ["Introducción", "Las normas que te afectan: protección de datos, comercio electrónico y consumo", "Lo que este curso no sustituye"]],
         ["Datos y correos", ["Base legal y consentimiento", "Comunicaciones comerciales y bajas"]],
         ["Tu web", ["Cookies y aviso legal", "Accesibilidad"]],
         ["Publicidad", ["Precios, rebajas y precio anterior", "Reseñas, testimonios y colaboraciones con creadores"]],
         ["IA", ["Cuándo etiquetar contenido hecho con IA", "Voces y caras: consentimiento"]],
     ],
     "intro": (
         "Una campaña puede salir muy bien y aun así meterte en un lío: un correo enviado sin permiso, unas cookies que se "
         "cargan antes de aceptar, un precio tachado que no cumple o un vídeo con IA sin avisar. En este curso repasamos "
         "lo que la ley española y europea exige a lo que haces cada día en marketing, explicado en llano. Vemos cuándo "
         "puedes escribir a alguien y cómo guardar la prueba de su permiso, qué tiene que llevar tu web, qué reglas hay "
         "para precios, rebajas, reseñas y colaboraciones con creadores, y qué cambia con la normativa europea de "
         "inteligencia artificial cuando usas avatares, voces o imágenes generadas. No soy abogado y este curso no "
         "sustituye a uno: te ayuda a detectar los riesgos a tiempo y a saber qué preguntar a tu asesoría. Es para ti si "
         "haces marketing por tu cuenta y quieres trabajar tranquilo. Saldrás con tu lista de comprobación legal y tus "
         "textos básicos revisados."
     ),
     "keywords": ["lssi", "ley de inteligencia artificial", "proteccion de datos empresa", "politica de cookies", "aviso legal web"],
     "youtube": None, "skool": None},

    # ------------------------------------------------------------------ bloque E
    {"bloque": "E", "slug": "radar-de-innovacion", "titulo": "Radar de innovación: aprende de los mejores",
     "gancho": "APRENDE DE LOS *MEJORES*", "mascota": "dos ojos con luz",
     "promesa": "Detectas qué hacen los mejores de tu sector y de otros, lo adaptas a tu negocio y mides si funciona.",
     "para_quien": "Dueños de pyme que sienten que el mundo va más rápido que su negocio.",
     "estado": "disponible", "ola": 1, "orden": 11, "acceso": "Privado + plan de pago",
     "capitulos_youtube": [], "material_base": ["circuito líder → paquete de conocimiento → prueba → medida"],
     "puntos": {"demanda": 2, "encaje": 4, "experiencia": 5, "pago": 4},
     "indice": [
         ["El método", ["Introducción", "Ir a la fuente, nunca al resumen del resumen", "Copiar la estructura, nunca el material"]],
         ["Tu radar", ["A quién seguir y dónde mirar", "Una hora a la semana de radar"]],
         ["El giro propio", ["De idea ajena a prueba tuya", "Lo que no encaja con tu marca"]],
         ["Medir y decidir", ["Funciona, empeora o todavía no se sabe", "Tu archivo de aprendizajes"]],
     ],
     "intro": (
         "Innovar en una pyme no va de inventar algo que nadie ha hecho. Va de fijarte en quién lo está haciendo bien, "
         "entender por qué le funciona y adaptarlo a tu negocio antes que los demás. En este curso te enseño el método con "
         "el que trabajo cada semana. Primero aprendes a ir a la fuente: lo que dice y hace el referente, no el resumen de "
         "alguien que lo resumió. Después montas tu radar: a quién seguir, en tu sector y fuera de él, y cómo revisarlo en "
         "una hora a la semana. Lo importante viene luego: copiar la estructura y no el material, darle tu giro y "
         "convertirlo en una prueba pequeña en tu negocio. Por último mides el resultado y lo clasificas en tres cajones: "
         "funciona, empeora o todavía no se sabe. Lo que funciona se queda y lo que empeora se retira. Es para ti si "
         "sientes que el mundo va más rápido que tu negocio. Saldrás con tu radar montado y tu primera prueba en marcha."
     ),
     "keywords": ["google trends", "design thinking", "lean startup", "innovacion empresarial", "tendencias marketing"],
     "youtube": None, "skool": "innovacion"},

    {"bloque": "E", "slug": "experimentos-de-una-semana", "titulo": "Experimentos de una semana",
     "gancho": "PRUEBA, MIDE, *DECIDE*", "mascota": "lupa",
     "promesa": "Conviertes cada idea en una prueba pequeña con fecha, cifra y decisión, y dejas de cambiar cosas a ciegas.",
     "para_quien": "Quien tiene muchas ideas y poco tiempo para saber cuáles valen.",
     "estado": "disponible", "ola": 1, "orden": 16, "acceso": "Privado + plan de pago",
     "capitulos_youtube": [], "material_base": [],
     "no_repetir": "Método general de experimentos para cualquier negocio. El ciclo semanal propio de una tienda está en «Medir y repetir».",
     "puntos": {"demanda": 1, "encaje": 4, "experiencia": 4, "pago": 3},
     "indice": [
         ["La prueba pequeña", ["Introducción", "De idea a hipótesis", "La prueba más pequeña que responde"]],
         ["Diseñar", ["Una sola cosa cada vez", "Cuánto tiempo y cuántos datos"]],
         ["Pruebas A/B sin trampas", ["Cuándo merece la pena", "Errores que dan resultados falsos"]],
         ["Decidir y aprender", ["Mantener, revertir o repetir", "Tu registro de pruebas"]],
     ],
     "intro": (
         "La mayoría de los cambios en un negocio se hacen a ojo: se cambia la web, el precio o el anuncio y nadie sabe si "
         "fue a mejor. En este curso aprendes a convertir cada idea en una prueba pequeña con fecha, cifra y decisión. "
         "Empezamos por pasar de una idea vaga a una hipótesis clara y por diseñar la prueba más pequeña que puede "
         "responderla. Aprendes a cambiar una sola cosa cada vez, a decidir cuánto tiempo dejarla correr y cuántos datos "
         "necesitas antes de fiarte. Vemos cuándo merece la pena una prueba A/B y qué errores dan resultados falsos aunque "
         "los números parezcan claros. Y cerramos el ciclo: mantener, revertir o repetir, con un registro donde queda lo "
         "aprendido para no volver a probar lo mismo. Es para ti si tienes muchas ideas y poco tiempo para saber cuáles "
         "valen. Saldrás con tu plantilla de prueba y tu primer experimento en marcha."
     ),
     "keywords": ["growth hacking", "growth marketing", "lean startup"],
     "youtube": None, "skool": "innovacion"},

    {"bloque": "E", "slug": "crea-sin-programar", "titulo": "Crea tus herramientas con IA sin programar",
     "gancho": "CREA SIN *PROGRAMAR*", "mascota": "dos ojos con luz",
     "promesa": "Construyes con IA una calculadora, un panel interno o una pequeña aplicación para tu negocio sin saber programar.",
     "para_quien": "Quien tiene en la cabeza una herramienta que le ahorraría horas y nadie se la hace.",
     "estado": "disponible", "ola": 1, "orden": 5, "acceso": "Privado + plan de pago",
     "capitulos_youtube": [], "material_base": ["la calculadora del paso que se rompe como caso"],
     "limite": "Herramientas para tu negocio (calculadoras, paneles, pequeñas apps). No es un curso de diseño de webs.",
     "puntos": {"demanda": 5, "encaje": 4, "experiencia": 5, "pago": 5},
     "indice": [
         ["Qué puedes construir", ["Introducción", "Lo que ya hacen personas sin perfil técnico", "Lo que no conviene construir tú"]],
         ["Pedir bien a la IA programadora", ["Describir la herramienta antes de pedirla", "Construir por pasos pequeños"]],
         ["Tu primera herramienta", ["Una calculadora para tus clientes", "Un panel interno"]],
         ["Probar y cuidar", ["Probar con datos reales", "Seguridad básica: claves y datos de clientes"]],
         ["Ponerla en marcha", ["Publicarla", "Arreglarla cuando algo falla"]],
     ],
     "intro": (
         "No soy programador y buena parte de las herramientas con las que trabajo las he construido dando instrucciones a "
         "la IA; la calculadora del paso que se rompe de brandooers.com, por ejemplo. En este curso aprendes a hacerlo tú, "
         "empezando por cosas pequeñas y útiles para tu negocio. Vemos qué tiene sentido construir y qué es mejor no tocar. "
         "Aprendes a describir la herramienta antes de pedirla y a construirla por pasos pequeños, comprobando cada uno. "
         "Haces tu primera herramienta, una calculadora para tus clientes o un panel interno, y la pruebas con datos "
         "reales. Repasamos la seguridad básica, porque una clave mal guardada o unos datos de clientes a la vista son un "
         "problema serio. Y aprendes a ponerla en marcha y a arreglarla cuando algo falla. Es para ti si tienes en la "
         "cabeza una herramienta que te ahorraría horas y nadie te la hace. Saldrás con tu primera herramienta "
         "funcionando y un método para la siguiente."
     ),
     "keywords": ["claude code", "lovable", "vibe coding", "cursor ia", "crear app con ia", "programar con ia"],
     "youtube": "inteligencia artificial para empresas", "skool": "automatizacion"},

    {"bloque": "E", "slug": "monta-tu-escuela", "titulo": "Monta tu escuela: de un vídeo semanal a una comunidad",
     "gancho": "TU SABER, *TU ESCUELA*", "mascota": "dos ojos con luz",
     "promesa": "Conviertes lo que sabes en una serie semanal, un boletín y una comunidad, paso a paso y midiendo cada fase.",
     "para_quien": "Expertos y profesionales que quieren convertir lo que saben en audiencia.",
     "estado": "proximamente", "ola": 3, "orden": 26, "acceso": "Privado + plan de pago",
     "capitulos_youtube": [], "material_base": ["el propio embudo de Brandooers"],
     "condicion": "Se abre cuando cada fase del embudo propio tenga resultados medidos (regla «solo lo probado»).",
     "puntos": {"demanda": 4, "encaje": 3, "experiencia": 2, "pago": 3},
     "indice": [
         ["El embudo", ["Introducción", "Lo corto, lo largo y el correo", "Qué va gratis y qué de pago"]],
         ["La serie", ["El capítulo semanal, con avatar o con cámara", "Una página por capítulo"]],
         ["Audio y boletín", ["El pódcast sin grabar de nuevo", "La carta semanal"]],
         ["La comunidad", ["Aula y muro", "Niveles, directos y permanencia"]],
         ["Medir", ["Cada fase con su cifra"]],
     ],
     "intro": (
         "Si sabes hacer algo bien, puedes enseñarlo, y enseñar es una de las mejores formas de que te conozcan. En este "
         "curso te cuento paso a paso cómo estoy montando esta escuela: un capítulo semanal en vídeo, una página por "
         "capítulo, un pódcast sacado de los mismos vídeos, un boletín por correo y esta comunidad. Vemos el embudo "
         "completo, qué va gratis y qué de pago, cómo producir la serie con avatar o con cámara, cómo sacar el audio sin "
         "grabar de nuevo y cómo montar el aula, el muro, los niveles y los directos para que la gente se quede. Abriré "
         "este curso cuando tenga resultados medidos de cada fase, porque solo enseño lo que he comprobado. Es para ti si "
         "eres experto en algo y quieres convertirlo en audiencia. Saldrás con tu embudo dibujado, tu serie planificada y "
         "tu comunidad lista para abrir."
     ),
     "keywords": ["podcast", "substack", "skool", "como hacer un podcast", "vender cursos online", "crear curso online"],
     "youtube": None, "skool": None},
]

DECISION_MARC = [
    {"tema": "Tu tienda con Odoo (montar y llevar una tienda online sobre Odoo)",
     "demanda": ["odoo", "odoo erp", "odoo tutorial", "curso odoo", "odoo ecommerce"],
     "por_que_fuera": "Marc trabaja dentro de Odoo: no puede vender servicios ni hablar como Odoo. Solo cabría como material de aprendizaje con la oferta oficial y con el visto bueno previo de Odoo."},
    {"tema": "Verifactu y factura electrónica para autónomos y pymes",
     "demanda": ["verifactu", "facturacion electronica"],
     "por_que_fuera": "Mucha demanda, pero es terreno de software de gestión y facturación (donde está Odoo) y fiscal; riesgo de parecer consultoría y de error normativo."},
    {"tema": "Cómo elegir un ERP o un CRM para tu pyme",
     "demanda": ["erp", "que es un erp", "crm", "que es un crm", "erp para pymes", "software de gestion"],
     "por_que_fuera": "Cualquier comparativa pone a Odoo frente a sus competidores; choca con la norma de no recomendar herramientas que compitan con la oferta oficial de Odoo."},
    {"tema": "Crea tu web o tu landing con IA",
     "demanda": ["crear pagina web", "diseño web", "landing page", "crear web con ia", "diseño web con ia"],
     "por_que_fuera": "Hacer webs es el negocio de otra marca de Marc, que no aparece en Brandooers. «Crea sin programar» se limita a herramientas internas para no pisarlo."},
]

FUERA_POR_NORMA = [
    {"tema": "Cursos de plataforma: Shopify, WooCommerce, PrestaShop", "demanda": ["shopify", "woocommerce", "prestashop"],
     "motivo": "Compiten con la oferta de comercio electrónico de Odoo. La ruta «Tu tienda vende más» es válida para cualquier plataforma sin enseñar ninguna."},
    {"tema": "Dropshipping", "demanda": ["dropshipping"], "motivo": "No es experiencia nuestra (no se enseña lo no probado) y en Skool en español está saturado."},
    {"tema": "FUNDAE y formación bonificada", "demanda": ["fundae", "curso fundae", "formacion bonificada"],
     "motivo": "Es el escalón 3 (SkillUp para empresas), no la comunidad de pago para personas."},
]


# ---------------------------------------------------------------- build
def num(x):
    """Spanish number format: 33.0 -> 33, 25.5 -> 25,5, 1000 -> 1.000."""
    if x is None:
        return "SIN DATOS"
    if float(x).is_integer():
        return f"{int(x):,}".replace(",", ".")
    return f"{x:.1f}".replace(".", ",")


def total(p):
    return sum(p.values()) if p else None


def build():
    cursos = []
    for c in CURSOS:
        d = dict(c)
        d["bloque_nombre"] = next(b["nombre"] for b in BLOQUES if b["id"] == c["bloque"])
        d["puntuacion"] = total(c["puntos"])
        d["demanda"] = {
            "busquedas_google_es": [kw(k) for k in c["keywords"]],
            "youtube": yt(c["youtube"]) if c.get("youtube") else None,
            "youtube_extra": yt(c["youtube_extra"]) if c.get("youtube_extra") else None,
            "skool_espanol": sk(c["skool"]) if c.get("skool") else None,
        }
        for k in ("keywords", "youtube", "skool", "youtube_extra"):
            d.pop(k, None)
        d["intro_palabras"] = len(c["intro"].split())
        cursos.append(d)
    cursos.sort(key=lambda x: x["orden"])
    for i, c in enumerate(cursos, 1):
        c["orden"] = i
    return cursos


def main():
    cursos = build()
    out = {
        "meta": {
            "fecha": FECHA, "marca": "SkillUp Brandooers", "comunidad": "I+D+E · Innovación, Desarrollo IA y Estrategia (Skool, freemium)",
            "autor": "Marc Herrero",
            "certeza": {"HECHO": "dato leído en su fuente, con enlace", "INFERENCIA": "conclusión razonada a partir de hechos", "SIN DATOS": "no se pudo medir"},
            "estado": {"disponible": "se graba antes de abrir y se abre el día de la apertura (ola 1). Hoy ningún curso está grabado en Skool.",
                       "proximamente": "visible en el aula con candado; se abre en la ola 2 o 3"},
            "gancho": "Texto de la portada: MAYÚSCULAS, 5 palabras como máximo; *palabra* = resaltada; | = salto de línea (motor serie_miniaturas/miniatura_capitulo.py). Figura: mascota de los ojos, nunca la cara de Marc.",
            "puntos": "demanda, encaje con el público, experiencia real y camino al pago, de 1 a 5 cada uno (máximo 20). INFERENCIA: lo puntúa este estudio a partir de los datos citados.",
            "coste_dataforseo": COSTE_DATAFORSEO,
            "fuentes_datos": {"busquedas": "_datos/sv_2724_es.json y _datos/ideas_2724_es.json", "youtube": "_datos/youtube_raw/youtube_busquedas.json",
                              "skool": "_datos/skool_raw/skool_discovery.json", "skool_ayuda": "_datos/skool_help_img/ (capturas de la ayuda oficial)"},
        },
        "bloques": BLOQUES,
        "cursos": cursos,
        "decision_marc": [dict(x, demanda=[kw(k) for k in x["demanda"]]) for x in DECISION_MARC],
        "fuera_por_norma": [dict(x, demanda=[kw(k) for k in x["demanda"]]) for x in FUERA_POR_NORMA],
        "skool_proximamente": SKOOL_METODO,
    }
    with open(os.path.join(BASE, "catalogo_cursos.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    with open(os.path.join(BASE, "CATALOGO_CURSOS.md"), "w", encoding="utf-8") as f:
        f.write(md(out))
    # self-checks: intro length, one intro per course, order unique, ola-1 rule (>=3 per content block)
    for c in cursos:
        assert c["indice"][0][1][0].startswith("Introducción"), c["slug"]
        assert 100 <= c["intro_palabras"] <= 270, (c["slug"], c["intro_palabras"])
        assert "Boomatik" not in c["intro"] and "Odoo" not in c["intro"], c["slug"]
    for b in "ABCDE":
        assert sum(1 for c in cursos if c["bloque"] == b and c["ola"] == 1) >= 3, b
    print(len(cursos), "cursos ·", sum(c["ola"] == 1 for c in cursos), "en la ola 1")


# ---------------------------------------------------------------- Skool «próximamente» (verified 29-10-2026)
SKOOL_METODO = {
    "hechos": [
        {"dato": "Cinco formas de acceso por curso: Abierto, Por nivel, Compra suelta, Por días desde el alta y Privado. Con Privado aparece el acceso por plan (Tier) y se combinan «nivel O plan», «compra O plan» y «días O plan».",
         "fuente": "https://help.skool.com/article/23-how-to-set-permissions-for-a-course", "certeza": "HECHO"},
        {"dato": "Un curso por nivel sigue apareciendo en la lista del aula de los miembros que aún no lo tienen: tarjeta con la portada atenuada en gris, candado y el aviso «Course unlocks at Level 2»; el título y la descripción se leen debajo.",
         "fuente": "https://help.skool.com/article/145-how-does-level-locked-courses-work (texto y captura)", "certeza": "HECHO"},
        {"dato": "Un curso sin acceso (privado o de pago) se ve igual, con el aviso «You don't have access to this course».",
         "fuente": "https://help.skool.com/article/101-how-to-unlock-a-locked-course-or-an-event (captura)", "certeza": "HECHO"},
        {"dato": "Los cursos se publican por defecto; si se pasan a borrador, desaparecen para los miembros. Un borrador NO sirve para enseñar un curso con candado.",
         "fuente": "https://help.skool.com/article/143-how-to-publish-a-course", "certeza": "HECHO"},
        {"dato": "Cada página (lección) tiene su interruptor de publicada: solo se ve cuando está publicada. Las páginas se agrupan en carpetas (módulos).",
         "fuente": "https://help.skool.com/article/166-what-is-classroom", "certeza": "HECHO"},
        {"dato": "Goteo por página: una lección se abre X días después del alta; el miembro ve el título y el aviso «Module unlocks in 14 days».",
         "fuente": "https://help.skool.com/article/53-how-to-drip-the-content (texto y captura)", "certeza": "HECHO"},
        {"dato": "Tamaño de portada de curso: la ayuda oficial no lo da. Una documentación no oficial indica 1460 × 752 px en JPG; Skool convierte PNG y WebP a JPG, rechaza SVG y acepta hasta unos 10 MB.",
         "fuente": "https://skool-api.cristiantala.com/docs/files/", "certeza": "INFERENCIA (fuente no oficial, medida empírica)"},
        {"dato": "Texto del aviso de candado con la interfaz en español y límite de caracteres de la descripción del curso.", "fuente": "—", "certeza": "SIN DATOS"},
        {"dato": "Cómo ve un miembro del plan gratis un curso Privado sin plan asignado dentro de un grupo freemium.", "fuente": "—", "certeza": "SIN DATOS (se comprueba con una cuenta de prueba antes de abrir)"},
    ],
    "recomendacion": [
        "Curso «Empieza aquí» el primero del aula, en Abierto. Lleva la introducción general (el «doc de introducción» con portada llamativa) y un módulo «Lo que viene» con una lección por bloque: de qué irá cada curso y su índice completo. Así todo el mundo lee lo que viene aunque el curso tenga candado.",
        "Cada curso «próximamente»: se crea publicado (nunca en borrador), con su portada, su título y una descripción que empieza por «Próximamente ·» y sigue con la promesa. Acceso: Privado, sin plan y sin nadie asignado. Sale con candado para todos y solo lo ven por dentro los administradores.",
        "Dentro del curso «próximamente» se van montando las lecciones como páginas no publicadas. La primera, «Introducción», con el texto de este catálogo.",
        "El día que se abre: se publican las páginas y se cambia el acceso. Si es de pago, Privado + plan de pago (y, si se quiere regalar una muestra, «nivel O plan»). Si es gratis, Abierto. Se quita «Próximamente ·» de la descripción y se anuncia en el muro.",
        "No usar Por nivel 9 ni Por días para simular «próximamente»: el aviso diría «se abre en el nivel 9» o «en N días», que no es verdad. No usar Borrador: esconde el curso.",
        "Alternativa si Marc quiere que cada curso se pueda abrir para leer su propia introducción: curso en Abierto con solo «Introducción» publicada y el resto de páginas sin publicar, y «Próximamente ·» en la descripción. No lleva candado, y cuando pase a Privado + plan de pago los del plan gratis dejarán de ver esa introducción, por eso también está en «Empieza aquí».",
        "Antes de abrir: en el grupo privado, entrar con una cuenta de prueba del plan gratis y otra del plan de pago, y hacer captura de cómo se ve cada tipo de curso.",
    ],
    "portada": [
        "Diseñar a 1460 × 752 px (INFERENCIA, ver arriba) y exportar en JPG de calidad 85-90 % y menos de 10 MB.",
        "Con candado, Skool tapa la portada con gris y pone el candado y el aviso en el centro: la portada casi no se lee. Lo que vende un curso cerrado es el título y la descripción; la portada luce cuando se abre.",
        "Mismo sistema que las miniaturas de la serie (serie_miniaturas/miniatura_capitulo.py): gancho en mayúsculas, como mucho cinco palabras, una palabra resaltada, mascota de los ojos a la derecha y nunca la cara de Marc. Color de acento por bloque para que el aula se lea por bloques.",
    ],
}


def md(o):
    L = []
    w = L.append
    cursos = o["cursos"]
    w("# Catálogo de cursos de I+D+E (Skool) · SkillUp Brandooers\n")
    w(f"Borrador para Marc · {FECHA} · Nada está creado ni publicado en Skool. Fuente única: `_scripts/build_catalogo.py`; este documento y `catalogo_cursos.json` salen de ahí.\n")
    w("**Cómo leer las cifras.** HECHO = leído en su fuente, con enlace. INFERENCIA = conclusión nuestra a partir de hechos. SIN DATOS = no se pudo medir. Las búsquedas son la media mensual en Google España (DataForSEO, 29-10-2026).\n")
    w("## 1. En cinco líneas\n")
    n1 = sum(c["ola"] == 1 for c in cursos)
    w(f"- **{len(cursos)} cursos en 6 bloques**: «Empieza aquí» (gratis), «Tu tienda vende más», «Desarrollo con IA», «Visibilidad y captación», «Estrategia» e «Innovación».")
    w(f"- **Ola 1 (apertura): {n1} cursos**: los dos de entrada y tres por bloque, como pidió Marc el 29-10. El resto se ve en el aula con candado y se abre en las olas 2 y 3.")
    w("- **Donde más se busca: la IA aplicada.** «curso ia» 3.600 búsquedas al mes, «n8n» 49.500, «claude code» 74.000, «elevenlabs» 90.500, «google search console» 90.500 (HECHO). Lo que busca el dueño de tienda con sus palabras casi no aparece en Google («carrito abandonado» 70): ese público llega por YouTube, donde «cómo vender más en tu tienda online» tiene una mediana de 182.539 visualizaciones en los primeros resultados (HECHO).")
    w("- **En Skool en español hay mucha oferta de IA y casi nada para pymes españolas**: 484 grupos sobre «inteligencia artificial» y 638 sobre «IA para negocios», frente a 30 para «pymes» (HECHO). La mayoría de los grandes apuntan a ganar dinero con IA o con redes (INFERENCIA por sus descripciones). Hueco: pyme y tienda española, con método y sin promesas.")
    w("- **Cómo se hace el «próximamente» en Skool**: curso publicado, acceso Privado sin plan ni miembros, descripción que empieza por «Próximamente ·», y su introducción e índice dentro del curso abierto «Empieza aquí» (detalle en el punto 6).\n")

    w("## 2. El mapa\n")
    for b in o["bloques"]:
        cs = [c for c in cursos if c["bloque"] == b["id"]]
        w(f"### {b['id']} · {b['nombre']} ({b['letra']})\n")
        w(b["para_que"] + "\n")
        w("| Orden | Curso | Estado | Ola | Acceso al abrirse | Capítulos que lo alimentan |")
        w("|---|---|---|---|---|---|")
        for c in cs:
            caps = ", ".join(str(x) for x in c["capitulos_youtube"]) or "ninguno aún (pide serie propia)"
            w(f"| {c['orden']} | **{c['titulo']}** | {'disponible' if c['estado'] == 'disponible' else 'próximamente'} | {c['ola']} | {c['acceso']} | {caps} |")
        w("")
    w("«Disponible» quiere decir que se graba antes de abrir y se abre ese día. Hoy no hay ningún curso grabado en Skool. Capítulos = los 13 de «Tu tienda vende más» del plan de 13 semanas (`serie.json`).\n")

    w("## 3. Por qué este orden\n")
    w("Cada curso se puntúa de 1 a 5 en cuatro cosas (INFERENCIA, con los datos del punto 4): **demanda** medida, **encaje** con el público (pyme, tienda, autónomo), **experiencia real** nuestra (lo que hacemos cada semana, no lo que hemos leído) y **camino al pago** (si lleva de forma natural al plan de pago). Máximo 20.\n")
    w("Reglas que mandan sobre la puntuación: la ruta de tiendas abre primero porque la serie gratis ya la alimenta; cada bloque abre con tres cursos (regla de Marc del 29-10); lo que aún no hemos comprobado nosotros (redes, montar una escuela) espera a tener resultados propios medidos.\n")
    w("| Orden | Curso | Demanda | Encaje | Experiencia | Pago | Total | Ola |")
    w("|---|---|---|---|---|---|---|---|")
    for c in cursos:
        p = c["puntos"]
        if p:
            w(f"| {c['orden']} | {c['titulo']} | {p['demanda']} | {p['encaje']} | {p['experiencia']} | {p['pago']} | **{c['puntuacion']}** | {c['ola']} |")
        else:
            w(f"| {c['orden']} | {c['titulo']} | — | — | — | — | puerta | {c['ola']} |")
    w("")

    w("## 4. La demanda, curso a curso\n")
    w("Búsquedas al mes en Google España (HECHO, DataForSEO). YouTube: mediana de visualizaciones de los ~20 primeros vídeos de esa búsqueda en español (HECHO lo que muestra la página; INFERENCIA que sea demanda española, porque la lista mezcla otros países y algún vídeo en inglés). Skool: grupos en español que salen al buscar el tema y mediana del precio mensual que enseñan los 30 primeros (HECHO lo que muestra Skool).\n")
    w("| Curso | Búsquedas (Google España) | YouTube | Skool en español |")
    w("|---|---|---|---|")
    for c in cursos:
        d = c["demanda"]
        if not d["busquedas_google_es"]:
            continue
        ks = sorted(d["busquedas_google_es"], key=lambda x: -(x["busquedas_mes"] or 0))
        kt = "; ".join(f"«{x['keyword']}» {x['busquedas_mes']:,}".replace(",", ".") if x["busquedas_mes"] is not None else f"«{x['keyword']}» SIN DATOS" for x in ks[:5])
        y = d["youtube"]
        yt_t = f"«{y['busqueda']}»: {y['mediana_vistas_top20']:,}".replace(",", ".") if y else "—"
        if d.get("youtube_extra"):
            ye = d["youtube_extra"]
            yt_t += f"; «{ye['busqueda']}»: {ye['mediana_vistas_top20']:,}".replace(",", ".")
        s = d["skool_espanol"]
        sk_t = f"«{s['busqueda']}»: {num(s['grupos_en_espanol'])} grupos, mediana {num(s['mediana_precio_mensual_usd_30_primeros'])} $/mes" if s else "—"
        w(f"| {c['titulo']} | {kt} | {yt_t} | {sk_t} |")
    w("")
    w("Lecturas (INFERENCIA):\n")
    w("- La IA es lo que más se busca y donde más compite Skool en español, con medianas de 25,5 a 37 $/mes en «inteligencia artificial», «automatización» y «agentes IA». Lo que nos diferencia no es el tema, sino el enfoque: pyme y tienda española, método, comprobación y sin promesas de ingresos.")
    w("- «Aparecer en ChatGPT» casi no tiene vídeos con audiencia (mediana de 1.007 visualizaciones) mientras «google search console» tiene 90.500 búsquedas: hay hueco para «Que Google y ChatGPT te recomienden».")
    w("- Los cursos de tienda tienen poca búsqueda directa en Google, pero su público ve vídeos de «vender más» por cientos de miles. Se alimentan desde YouTube, no desde el buscador.")
    w("- Google Trends, últimos 12 meses en España (HECHO, DataForSEO): «curso ia» media 65 sobre 100, con su máximo en mayo de 2026; «curso marketing digital» 8; «curso seo» 2; «ecommerce curso» y «curso n8n» por debajo de 1 en la misma escala.")
    w("- Ojo con un dato: Google Ads da 3.600 búsquedas a «ecommerce curso», pero agrupa variantes y Trends lo deja por debajo de 1; usamos «curso ecommerce», 480.\n")

    w("## 5. Qué hay en Skool en español\n")
    w("Búsqueda pública de Skool Discovery con el filtro de idioma español, 29-10-2026 (HECHO). Los mayores grupos de cada tema:\n")
    w("| Tema buscado | Grupos | Mediana $/mes (30 primeros) | Los tres mayores (miembros) |")
    w("|---|---|---|---|")
    seen = set()
    for c in cursos:
        s = c["demanda"]["skool_espanol"]
        if not s or s["busqueda"] in seen:
            continue
        seen.add(s["busqueda"])
        top = "; ".join(f"{g['nombre'].strip()} ({g['miembros']:,})".replace(",", ".") for g in s["mayores"])
        w(f"| {s['busqueda']} | {num(s['grupos_en_espanol'])} | {num(s['mediana_precio_mensual_usd_30_primeros'])} | {top} |")
    w("")
    w("Skool limita la búsqueda a 1.000 resultados («estrategia» llega al tope). El precio es el que enseña la tarjeta; en un grupo freemium puede ser el del plan de pago (INFERENCIA). No es una recomendación de precio: el precio lo decide Marc y no se publica.\n")

    w("## 6. «Próximamente» en Skool: qué está comprobado y cómo hacerlo\n")
    sm = o["skool_proximamente"]
    w("**Comprobado en la ayuda oficial de Skool (29-10-2026):**\n")
    for h in sm["hechos"]:
        w(f"- {h['dato']} {h['certeza']}. Fuente: {h['fuente']}")
    w("\n**Cómo hacerlo («visible con introducción, el resto cerrado»):**\n")
    for i, r in enumerate(sm["recomendacion"], 1):
        w(f"{i}. {r}")
    w("\n**Portadas:**\n")
    for r in sm["portada"]:
        w(f"- {r}")
    w("")
    w("| Curso | Gancho de portada | Figura |")
    w("|---|---|---|")
    for c in cursos:
        w(f"| {c['titulo']} | `{c['gancho']}` | {c['mascota']} |")
    w("")

    w("## 7. La introducción general (el documento de entrada)\n")
    w("Va como primera lección de «Empieza aquí». Portada llamativa del curso: `EMPIEZA *AQUÍ*`, mascota de los dos ojos con luz.\n")
    for p in INTRO_GENERAL.split("\n\n"):
        w("> " + p + "\n>")
    L[-1] = L[-1].rstrip(">").rstrip()
    w("")

    w("## 8. Fichas de curso\n")
    for c in cursos:
        w(f"### {c['orden']}. {c['titulo']}\n")
        w(f"- **Bloque:** {c['bloque_nombre']} · **Estado:** {'disponible' if c['estado'] == 'disponible' else 'próximamente'} (ola {c['ola']}) · **Acceso:** {c['acceso']}")
        w(f"- **Promesa:** {c['promesa']}")
        w(f"- **Para quién:** {c['para_quien']}")
        w(f"- **Portada:** `{c['gancho']}`")
        caps = ", ".join(str(x) for x in c["capitulos_youtube"]) or "ninguno todavía"
        w(f"- **Capítulos gratis que lo alimentan:** {caps}")
        if c.get("material_base"):
            w(f"- **Material que ya existe:** {', '.join(c['material_base'])}")
        for k, lab in (("condicion", "Condición para abrir"), ("no_repetir", "Para no repetir"), ("limite", "Límite")):
            if c.get(k):
                w(f"- **{lab}:** {c[k]}")
        w("\n**Índice**\n")
        for i, (mod, lecs) in enumerate(c["indice"], 1):
            w(f"{i}. **{mod}**")
            for j, l in enumerate(lecs, 1):
                w(f"   {i}.{j}. {l}")
        if c["slug"] != "empieza-aqui":
            w(f"\n**Introducción** ({c['intro_palabras']} palabras)\n")
            w("> " + c["intro"].replace("\n\n", "\n>\n> "))
        else:
            w("\n**Introducción:** la del punto 7.")
        w("")

    w("## 9. Decisión de Marc: temas con demanda que no entran en el catálogo\n")
    w("| Tema | Demanda (Google España) | Por qué está fuera |")
    w("|---|---|---|")
    for x in o["decision_marc"]:
        kt = "; ".join(f"«{k['keyword']}» {k['busquedas_mes']:,}".replace(",", ".") for k in x["demanda"] if k["busquedas_mes"])
        w(f"| {x['tema']} | {kt} | {x['por_que_fuera']} |")
    w("")
    w("**Fuera por norma (no se proponen):**\n")
    for x in o["fuera_por_norma"]:
        kt = "; ".join(f"«{k['keyword']}» {k['busquedas_mes']:,}".replace(",", ".") for k in x["demanda"] if k["busquedas_mes"])
        w(f"- **{x['tema']}** ({kt}). {x['motivo']}")
    w("")

    w("## 10. Lo que falta o hay que decidir\n")
    o1 = [c for c in cursos if c["ola"] == 1 and c["bloque"] != "0"]
    nl = sum(len(l) for c in o1 for _, l in c["indice"])
    w(f"- **Carga de la ola 1.** Tres cursos por bloque son {len(o1)} cursos con {nl} lecciones antes de abrir (más las de entrada). Es mucho. Alternativa (decisión de Marc): abrir con «Empieza aquí» y los bloques A, B y D, y dejar C y E visibles con candado; o abrir cada curso de la ola 1 con sus dos primeros módulos y gotear el resto.")
    w("- **Series gratis que faltan.** «Tu equipo de agentes», «Vídeo con IA», «Anuncios con las cuentas claras», «Radar de innovación», «Crea sin programar» y «Experimentos de una semana» no tienen ningún capítulo de YouTube que los alimente. Cada uno necesita al menos un capítulo gancho propio.")
    w("- **Revisión legal antes de publicar:** plantilla de devoluciones, hoja de rebajas (precio anterior), «Correo que vende» y todo «Marketing sin multas».")
    w("- **SIN DATOS:** texto del candado en la interfaz en español, límite de caracteres de la descripción del curso, cómo ve un miembro gratis un curso Privado sin plan en un grupo freemium y tamaño oficial de la portada. Se comprueba en el grupo privado con cuentas de prueba.")
    w("- **Encaje con el plan de Skool del 29-10.** «Empieza aquí» fusiona el módulo 0A de `SKOOL_PLAN_2026-10-29.md` con el mapa general, porque I+D+E ya no es solo para tiendas; la biblioteca es el 0B; los cursos 1 a 6 de aquel plan son el bloque A con los mismos temas.")
    w("- **Tiempo de cada curso:** SIN DATOS hasta grabar el primero; se mide con «Que te encuentren» y se ajusta el calendario.\n")

    w("## 11. Fuentes y coste\n")
    cd = o["meta"]["coste_dataforseo"]
    es = lambda x: str(x).replace(".", ",")  # noqa: E731
    w(f"- **DataForSEO: {es(cd['total_usd'])} USD en total** ({'; '.join(f'{a}: {es(b)} USD' for a, b in cd['detalle'])}). {cd['metodo']}.")
    w("- Búsquedas en Google: `_datos/sv_2724_es.json` (415 palabras) e `_datos/ideas_2724_es.json` (3.804 ideas).")
    w("- YouTube: `_datos/youtube_raw/youtube_busquedas.json` (20 búsquedas, páginas públicas, sin iniciar sesión).")
    w("- Skool Discovery: `_datos/skool_raw/skool_discovery.json` (19 búsquedas con filtro de español, sin iniciar sesión).")
    w("- Ayuda de Skool: artículos 23, 53, 101, 143, 144, 145, 166, 168 y 215 de https://help.skool.com, y capturas en `_datos/skool_help_img/`.")
    w("- Conocimiento propio: `boomatik-brain` (playbooks, skills y catálogo de agentes), `SKOOL_PLAN_2026-10-29.md`, `MODELO_TRES_ESCALONES_2026-10-29.md`, `serie.json` y `embudo_y_distribucion.json`.")
    return "\n".join(L) + "\n"


if __name__ == "__main__":
    main()
