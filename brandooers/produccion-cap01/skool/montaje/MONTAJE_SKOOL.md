# Montaje de Skool · I+D+E · Innovación, Desarrollo IA y Estrategia

Kit para configurar la comunidad de pago de SkillUp Brandooers en Skool, pantalla a pantalla, en cuanto Marc cree el grupo con el plan Pro. 29-10-2026. No se ha entrado en Skool ni se ha creado, comprado o publicado nada. Las mismas instrucciones, en datos, están en `montaje_skool.json` (ambos salen de `_build_montaje.py`).

**Cómo leerlo.** Cada casilla es un paso. «HECHO» = función o límite leído en el centro de ayuda de Skool (número de artículo de help.skool.com). **«comprobar en pantalla»** = no consta en ninguna fuente oficial: se mira al montarlo. Rutas de ficheros relativas a `.claude/scratch/l01/`.

**Orden recomendado:** General → Precios → Plugins → Categorías → Niveles → Aula → Acerca de → Publicaciones fijadas → Zapier. Lo último, abrir la entrada.


## 1. Ajustes › General

- [ ] **Nombre del grupo:** I+D+E · Innovación, Desarrollo IA y Estrategia · **comprobar en pantalla**
  - Límite de caracteres sin datos. Si lo corta, alternativa: «I+D+E · SkillUp Brandooers». · Fuente: SKOOL_PLAN §7 (decisión de Marc)
- [ ] **Dirección (URL):** skool.com/skillup-brandooers (alternativa: skool.com/ide-brandooers) · **comprobar en pantalla**
  - Comprobar que está libre. Elegir bien a la primera. · Fuente: help 121 y 176: dirección propia solo en Pro; los cambios después del primero se pagan
- [ ] **Descripción:** Para pymes, tiendas online y autónomos: cada semana una prueba en tu negocio, con IA y estrategia, y una cifra para saber si funcionó. · **comprobar en pantalla**
  - 134 caracteres; límite sin datos. · Fuente: help 153 (Discovery pide descripción)
- [ ] **Icono del grupo:** serie_miniaturas/banners/perfil_1080x1080.png (los ojos de Brandooers) · **comprobar en pantalla**
  - Cuadrado. Comprobar el recorte circular en pantalla. · Fuente: help 120: se cambia en General › CHANGE; no da medidas
- [ ] **Portada del grupo:** serie_miniaturas/banners/facebook_portada_1640x624.jpg (provisional) · **comprobar en pantalla**
  - Si el recorte corta el logotipo o el lema, se rehace a la medida que pida el cargador con la misma plantilla (facebook_portada_1640x624.html). Nunca la cara de Marc. · Fuente: help 120 no da medidas; help 153 y 245 (Discovery y anuncios usan la portada)
- [ ] **Privacidad del grupo:** Privado (el contenido solo lo ven los miembros) · **comprobar en pantalla**

## 2. Ajustes › Precios (el único sitio con precios)

- [ ] **Tipo de cobro:** Freemium: un plan gratis y un plan de pago
  - Fuente: help 215
- [ ] **Plan gratis:** Activo. Incluye el muro, «Empieza aquí» y la biblioteca por nivel 2.
  - Fuente: help 215, 23
- [ ] **Plan de pago · precio mensual:** 9 (primer tramo: 10 miembros; Marc confirma la moneda)
  - Escalera para nuevos (decisión de Marc): 9 hasta 10 altas de pago, 29 hasta 25, 49 hasta 50, 79 hasta 100. Quien ya paga conserva su precio (help 86). El cambio es a mano: el Manager crea la tarea al llegar a 10, 25, 50 y 100. · Fuente: help 86: Skool cobra en dólares y suma el IVA en la caja
- [ ] **Plan de pago · precio anual:** 90 (10 veces el mes) o sin plan anual: decide Marc
  - Quien elige anual conserva ese precio. · Fuente: help 215 e interfaz: el anual tiene que ser mayor que el mensual
- [ ] **Prueba gratis de 7 días:** Desactivada
  - Recomendación: el plan gratis ya deja ver la comunidad y así las plazas cuentan altas de pago reales. · Fuente: help 215
- [ ] **Growth Boost:** Se deja como viene (activado)
  - En freemium Skool no hace anuncios; no cuesta nada mientras no traiga a nadie de pago. Se revisa a los 90 días. · Fuente: help 226 y 245

## 3. Ajustes › Plugins › Preguntas de entrada (3, el máximo)

- [ ] **Pregunta 1 · Texto:** ¿A qué te dedicas y qué quieres mejorar con IA y estrategia?
  - Decisión de Marc del 29-10 (SKOOL_PLAN §7): la comunidad ya no es solo de tiendas. Sirve para aceptar a mano y para que Marc salude con contexto. · Fuente: help 57: máximo 3; tipos texto, opción múltiple y correo (uno solo); hay que contestarlas todas
- [ ] **Pregunta 2 · Opción múltiple:** ¿Por dónde quieres empezar?  Opciones: Que mi tienda online venda más | Trabajar con la IA en mi negocio | Que me encuentren y me elijan | Ordenar mi estrategia y mis números | Probar ideas nuevas en mi negocio
  - Cada opción es un bloque del aula (A, B, C, D, E). Dice qué curso recomendar en la bienvenida y qué bloque producir antes. Número máximo de opciones: comprobar en pantalla. · Fuente: help 57: máximo 3; tipos texto, opción múltiple y correo (uno solo); hay que contestarlas todas
- [ ] **Pregunta 3 · Correo electrónico:** Tu correo, para avisarte cuando se abra un curso nuevo. Lo usa solo SkillUp Brandooers, no se cede a nadie y puedes pedir la baja cuando quieras. Tienes la política de privacidad en brandooers.com.
  - Skool solo admite una pregunta de correo. Se activa SOLO después de que legal-rgpd-proteccion-datos revise el texto y la base legal; hasta entonces, se deja fuera y quedan 2 preguntas. · Fuente: help 57: máximo 3; tipos texto, opción múltiple y correo (uno solo); hay que contestarlas todas

Aceptación: a mano. Se acepta a quien conteste con un negocio o un proyecto real. Al resto, rechazo amable sin enlace (no hay mensaje automático al rechazar).

## 4. Ajustes › Plugins (bienvenida, aprobación, enlaces, chat)

- [ ] **AutoDM:** Hola, #NAME#. Te doy la bienvenida a #GROUPNAME#. Para empezar, una pregunta: ¿a qué te dedicas y qué quieres que sea distinto dentro de un mes? Contéstame aquí mismo y lo leo yo. Las dudas de los cursos, mejor en la categoría Pregunta a Marc del muro: así la respuesta sirve también a los demás. Y el primer paso, el curso Empieza aquí: veinte minutos y sales con tu primera prueba apuntada. Marc
  - Texto fijo escrito por Marc, no lo genera una IA. Remitente: Marc. Revisar con PREVIEW y encender. · Fuente: help 64: un mensaje, 1 a 5 min tras el alta, variables #NAME# y #GROUPNAME#; no se envía si ya hay conversación
- [ ] **Vídeo de bienvenida:** Vacío hasta tenerlo: avatar de Marc con su voz V4, 4K, coste en euros y OK de Marc antes de generar
  - Fuente: help 176 (Pro)
- [ ] **Aprobación automática:** Apagada. Se acepta a mano a quien conteste con un negocio o proyecto real; se rechaza el spam.
  - Fuente: help 176, 184
- [ ] **Enlaces del grupo (hasta 3):** 1) Capítulos gratis: https://brandooers.com/tu-tienda-vende-mas/?utm_source=skool&utm_medium=referral&utm_campaign=bdo-comunidad  2) Política de privacidad de brandooers.com  3) Libre (chat de ayuda cuando exista) · **comprobar en pantalla**
  - Es la única vía de enlace fuera de las lecciones, porque los de «Acerca de» no funcionan. Dónde se ven: comprobar. · Fuente: help 76 (Pro, hasta 3)
- [ ] **Vídeo de baja:** Más adelante: recuerda, sin presión, que quien se va y vuelve paga el precio de ese día
  - Fuente: help 170, 244
- [ ] **Chat por nivel:** Nivel 1 (todos pueden escribir a Marc). Subir a nivel 2 si entra spam.
  - Fuente: help 176, 184
- [ ] **Publicar por nivel:** Nivel 1
  - Fuente: help 176

## 5. Ajustes › Notificaciones

- [ ] **Aviso por cada publicación nueva:** Activado, al correo de la cuenta de Marc
  - El Manager lee ese aviso para preparar el borrador; Marc contesta a mano. Qué trae el correo: comprobar. · Fuente: help 95

## 6. Muro › Categorías (en este orden)

| # | Nombre | Quién publica | Para qué |
|---|---|---|---|
| 1 | Avisos | Solo administradores | Aperturas de cursos, vídeos de respuesta y cambios de la comunidad. |
| 2 | Preséntate | Todos | La primera publicación de cada miembro, con la plantilla fijada. |
| 3 | Pregunta a Marc | Todos | Dudas de los cursos. Marc contesta en el hilo; la respuesta sirve a todos. |
| 4 | Tu tienda vende más | Todos | Bloque A: pruebas y dudas de tiendas online. |
| 5 | Desarrollo con IA | Todos | Bloque B. |
| 6 | Visibilidad y captación | Todos | Bloque C. |
| 7 | Estrategia | Todos | Bloque D. |
| 8 | Innovación | Todos | Bloque E. |
| 9 | Victorias | Todos | Un cambio medido: antes, después y la cifra de la propia tienda o negocio. |
| 10 | (libre) | — | Para la próxima ruta |

HECHO: hasta 10 categorías de 30 caracteres, con quién publica (help 67). Orden del muro: «Nuevo».

## 7. Ajustes › Niveles

| Nivel | Puntos (Skool) | Nombre | Qué abre |
|---|---|---|---|
| 1 | 0 | Recién llegado | El muro, publicar, el chat con Marc y el curso «Empieza aquí». |
| 2 | 5 | Primera prueba | El curso «Biblioteca de plantillas» (acceso por nivel 2, como dice el catálogo). |
| 3 | 20 | Con método | Nada extra: el nivel se ve en el perfil y en la clasificación. |
| 4 | 65 | Mide cada semana | Nada extra. |
| 5 | 155 | Ayuda a otros | El curso «Que te encuentren» con acceso «nivel 5 O plan de pago» (desde que se abra). Que esto anime a pagar es suposición: se mide a los 28 días. |
| 6 | 515 | Referente | Nada extra. |
| 7 | 2.015 | Motor de la comunidad | Nada extra. |
| 8 | 8.015 | Veterano I+D+E | Nada extra. |
| 9 | 33.015 | Leyenda I+D+E | Nada extra. |

HECHO: umbrales y 1 punto por «me gusta» recibido (help 31); cursos por nivel (help 145). **Comprobar en pantalla** dónde se renombran los niveles: la ayuda solo dice que la clasificación enseña «los nombres de nivel propios de cada grupo». Nada de pedir «me gusta» a cambio de «me gusta»: Skool prohíbe cultivar puntos (help 179).

## 8. Ajustes › Afiliados

- [ ] **Afiliados de miembros:** Apagado al abrir. Al llegar a 25 altas de pago, decide Marc el porcentaje.
  - Sin datos de rango mínimo y máximo ni de lo que usan comunidades parecidas: por eso no se recomienda una cifra. · Fuente: help 192, 187, 219 (Pro; cambiar el % afecta a todos; bajarlo daña la reputación)

## 9. Ajustes › Plugins › Zapier (integración con BOO Manager)

- [ ] **Clave de Zapier:** Copiarla en Zapier. No se guarda en ningún documento. Cambiarla rompe los Zaps.
  - Fuente: help 56
- [ ] **Zap 1:** Disparador Skool «New Paid Member» → Webhooks by Zapier POST → <URL_WEBHOOK_MANAGER_EDUCACION>, cabecera x-webhook-secret: <SECRETO_EN_ENV_LOCAL>. Campos: event=skool.new_paid_member, fecha, id de transacción.
  - Mínimo de datos: para contar la escalera bastan fecha e id. Nombre y correo solo con revisión de legal-rgpd-proteccion-datos. El punto de entrada del Manager aún no existe. Plan de Zapier con webhooks: sin datos. · Fuente: help 56, 162; zapier.com/apps/skool/integrations
- [ ] **Zap 2:** Disparador «Answered Membership Questions» → el mismo webhook con event=skool.membership_answers
  - Solo después de la revisión legal. Las invitaciones por correo o CSV no cuentan como altas de pago. · Fuente: help 59

## 10. Página «Acerca de»

**Titular (primera línea):** Aquí no se viene a ver vídeos. Se viene a probar una cosa cada semana en tu negocio y a medir si ha funcionado.

```text
Aquí no se viene a ver vídeos. Se viene a probar una cosa cada semana en tu negocio y a medir si ha funcionado.

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

En los vídeos, Marc aparece con un avatar y una voz generados con IA a partir de su imagen y su voz reales.
```

- [ ] Sin un solo enlace: Skool no los activa en «Acerca de» (help 123). Los enlaces van en el plugin de enlaces y en las lecciones.
- [ ] **Imágenes y vídeo (en este orden)** · **comprobar en pantalla** (medidas y número máximo sin datos): 1) Vídeo de bienvenida cuando exista  2) serie_miniaturas/banners/youtube_banner_2560x1440.jpg  3) catalogo/portadas/01_empieza-aqui_1460x752.jpg  4) catalogo/portadas/03_que-te-encuentren_1460x752.jpg  5) catalogo/portadas/04_la-ia-como-socia_1460x752.jpg  6) catalogo/portadas/07_decide-con-datos_1460x752.jpg

## 11. Aula (Classroom) · 27 cursos

Método «próximamente» (CATALOGO_CURSOS.md §6, HECHO en help 23, 143, 145, 166): todos los cursos **publicados, nunca en borrador**. Los cerrados van en **Privado, sin plan y sin nadie asignado**: salen con candado para todos y con título y descripción legibles. Las lecciones se montan como páginas sin publicar. **El día que se abre cada uno:** se publican las páginas, se cambia el acceso a la columna «Al abrir», se quita «Próximamente · » de la descripción y se avisa en «Avisos». Nunca «Por nivel 9» ni «Por días» para fingir un «próximamente».

**Ajuste en «Empieza aquí» (curso 01):** la lección 1.2 del índice dice «muro, directos y niveles»; ponerla como «Cómo funciona la comunidad: muro, ayuda y niveles», porque no hay directos. Y la 2.3 «Calendario de aperturas» se cuenta por olas, sin fechas que no estén decididas.

| # | Curso | Bloque | Descripción al montar | Portada | Acceso al montar | Acceso al abrir | Ola |
|---|---|---|---|---|---|---|---|
| 01 | Empieza aquí: el mapa de I+D+E | Empieza aquí | En veinte minutos sabes qué curso te toca primero y sales con tu primera prueba apuntada. | `01_empieza-aqui_1460x752.jpg` | Abierto | Abierto | 1 |
| 02 | Biblioteca de plantillas | Empieza aquí | Todas las hojas, plantillas, listas y prompts de la comunidad, ordenados por bloque y listos para usar. | `02_biblioteca_1460x752.jpg` | Por nivel: nivel 2 | Por nivel: nivel 2 | 1 |
| 03 | Que te encuentren | Tu tienda vende más | Próximamente · Tus productos aparecen en Google, en ChatGPT y en el buscador de tu tienda con las palabras que usa tu cliente. | `03_que-te-encuentren_1460x752.jpg` | Privado, sin plan y sin miembros asignados (candado para todos) | Privado + plan de pago O nivel 5 | 1 |
| 04 | La IA como socia | Desarrollo con IA | Próximamente · Usas ChatGPT, Claude o Gemini con método: le das contexto, compruebas lo que dice y lo aplicas a tu negocio. | `04_la-ia-como-socia_1460x752.jpg` | Privado, sin plan y sin miembros asignados (candado para todos) | Privado + plan de pago | 1 |
| 05 | Que Google y ChatGPT te recomienden | Visibilidad y captación | Próximamente · Tu web responde lo que pregunta tu cliente para que Google y los asistentes de IA la muestren y la citen. | `05_que-la-ia-te-recomiende_1460x752.jpg` | Privado, sin plan y sin miembros asignados (candado para todos) | Privado + plan de pago | 1 |
| 06 | Crea tus herramientas con IA sin programar | Innovación | Próximamente · Construyes con IA una calculadora, un panel interno o una pequeña aplicación para tu negocio sin saber programar. | `06_crea-sin-programar_1460x752.jpg` | Privado, sin plan y sin miembros asignados (candado para todos) | Privado + plan de pago | 1 |
| 07 | Decide con datos | Estrategia | Próximamente · Montas tu cuadro de mando con Analytics, Search Console y Clarity y separas lo que es un hecho de lo que es una suposición. | `07_decide-con-datos_1460x752.jpg` | Privado, sin plan y sin miembros asignados (candado para todos) | Privado + plan de pago | 1 |
| 08 | La ficha que se entiende en 5 segundos | Tu tienda vende más | Próximamente · Tu ficha responde qué es, para quién, cuánto mide y cuándo llega antes de que el cliente se vaya. | `08_ficha-en-5-segundos_1460x752.jpg` | Privado, sin plan y sin miembros asignados (candado para todos) | Privado + plan de pago | 1 |
| 09 | Tu equipo de agentes | Desarrollo con IA | Próximamente · Delegas tareas repetitivas en agentes de IA y automatizaciones sin programar, con límites y control de gasto. | `09_tu-equipo-de-agentes_1460x752.jpg` | Privado, sin plan y sin miembros asignados (candado para todos) | Privado + plan de pago | 1 |
| 10 | Anuncios con las cuentas claras | Visibilidad y captación | Próximamente · Lanzas anuncios en Meta y Google sabiendo cuánto puedes pagar por cliente y midiendo bien cada venta. | `10_anuncios-con-cuentas_1460x752.jpg` | Privado, sin plan y sin miembros asignados (candado para todos) | Privado + plan de pago | 1 |
| 11 | Tu estrategia en una página | Estrategia | Próximamente · Decides a quién vendes, por qué te eligen y qué haces los próximos 90 días, todo en una página. | `11_estrategia-en-una-pagina_1460x752.jpg` | Privado, sin plan y sin miembros asignados (candado para todos) | Privado + plan de pago | 1 |
| 12 | Radar de innovación: aprende de los mejores | Innovación | Próximamente · Detectas qué hacen los mejores de tu sector y de otros, lo adaptas a tu negocio y mides si funciona. | `12_radar-de-innovacion_1460x752.jpg` | Privado, sin plan y sin miembros asignados (candado para todos) | Privado + plan de pago | 1 |
| 13 | El carrito sin sustos | Tu tienda vende más | Próximamente · El cliente ve el total, con envío y plazos, antes de darte ningún dato. | `13_carrito-sin-sustos_1460x752.jpg` | Privado, sin plan y sin miembros asignados (candado para todos) | Privado + plan de pago | 1 |
| 14 | Vídeo con IA: tu avatar y tu voz | Desarrollo con IA | Próximamente · Produces vídeos con tu avatar y tu voz clonada, con permiso, calidad y etiqueta de IA, sin grabarte cada semana. | `14_tu-avatar-y-tu-voz_1460x752.jpg` | Privado, sin plan y sin miembros asignados (candado para todos) | Privado + plan de pago | 1 |
| 15 | Correo que vende: imanes, boletín y secuencias | Visibilidad y captación | Próximamente · Construyes tu propia lista con un recurso útil y un boletín que la gente quiere abrir, con permiso y sin depender de ninguna red. | `15_tu-lista-de-correo_1460x752.jpg` | Privado, sin plan y sin miembros asignados (candado para todos) | Privado + plan de pago | 1 |
| 16 | Precios que dejan margen | Estrategia | Próximamente · Calculas tu precio desde tus costes, tu valor y tu competencia, y sabes cuánto puedes descontar sin perder dinero. | `16_precios-con-margen_1460x752.jpg` | Privado, sin plan y sin miembros asignados (candado para todos) | Privado + plan de pago | 1 |
| 17 | Experimentos de una semana | Innovación | Próximamente · Conviertes cada idea en una prueba pequeña con fecha, cifra y decisión, y dejas de cambiar cosas a ciegas. | `17_experimentos-de-una-semana_1460x752.jpg` | Privado, sin plan y sin miembros asignados (candado para todos) | Privado + plan de pago | 1 |
| 18 | Temporadas sin regalar el margen | Tu tienda vende más | Próximamente · Preparas Black Friday, Navidad y rebajas con seis semanas de antelación y con las cuentas hechas. | `18_temporadas_1460x752.jpg` | Privado, sin plan y sin miembros asignados (candado para todos) | Privado + plan de pago | 2 |
| 19 | Medir y repetir: tus cinco números | Tu tienda vende más | Próximamente · Un cuadro semanal de cinco números para saber en qué paso pierdes la venta y si tu cambio funcionó. | `19_tus-cinco-numeros_1460x752.jpg` | Privado, sin plan y sin miembros asignados (candado para todos) | Privado + plan de pago | 2 |
| 20 | Pagar desde el móvil | Tu tienda vende más | Próximamente · Compras de prueba desde el móvil sin atascos y un correo que recupera carritos sin perseguir a nadie. | `20_pagar-desde-el-movil_1460x752.jpg` | Privado, sin plan y sin miembros asignados (candado para todos) | Privado + plan de pago | 2 |
| 21 | Tu ficha de Google trae clientes | Visibilidad y captación | Próximamente · Tu ficha de Google completa, con reseñas y publicaciones, para que te elija quien busca cerca. | `21_tu-ficha-de-google_1460x752.jpg` | Privado, sin plan y sin miembros asignados (candado para todos) | Privado + plan de pago | 2 |
| 22 | Imágenes con IA que no se notan | Desarrollo con IA | Próximamente · Creas imágenes de producto y de ambiente con IA fieles al producto real y sin aspecto artificial. | `22_imagenes-con-ia_1460x752.jpg` | Privado, sin plan y sin miembros asignados (candado para todos) | Privado + plan de pago | 2 |
| 23 | Redes con método: un vídeo, muchas piezas | Visibilidad y captación | Próximamente · Conviertes una pieza larga a la semana en cortos, carruseles y publicaciones para cada red, con un calendario que puedes mantener. | `23_redes-con-metodo_1460x752.jpg` | Privado, sin plan y sin miembros asignados (candado para todos) | Privado + plan de pago | 2 |
| 24 | ¿Hay demanda? Investiga tu mercado con datos | Estrategia | Próximamente · Antes de lanzar algo, mides cuánta gente lo busca, quién compite y qué dicen los clientes, con fuentes que puedes citar. | `24_hay-demanda_1460x752.jpg` | Privado, sin plan y sin miembros asignados (candado para todos) | Privado + plan de pago | 2 |
| 25 | LinkedIn para vender sin parecer vendedor | Visibilidad y captación | Próximamente · Conviertes tu perfil y tus publicaciones de LinkedIn en conversaciones con clientes, a mano y sin automatismos prohibidos. | `25_linkedin-sin-agobiar_1460x752.jpg` | Privado, sin plan y sin miembros asignados (candado para todos) | Privado + plan de pago | 3 |
| 26 | Marketing sin multas | Estrategia | Próximamente · Sabes qué exige la ley a tus correos, cookies, anuncios, reseñas y contenidos con IA, y cuándo llamar a tu asesoría. | `26_marketing-sin-multas_1460x752.jpg` | Privado, sin plan y sin miembros asignados (candado para todos) | Privado + plan de pago | 3 |
| 27 | Monta tu escuela: de un vídeo semanal a una comunidad | Innovación | Próximamente · Conviertes lo que sabes en una serie semanal, un boletín y una comunidad, paso a paso y midiendo cada fase. | `27_monta-tu-escuela_1460x752.jpg` | Privado, sin plan y sin miembros asignados (candado para todos) | Privado + plan de pago | 3 |

- **Lección 1 de cada curso, «Introducción»:** texto en `catalogo_cursos.json` → `cursos[orden=N].intro` (en el catálogo, §8, ficha N). Publicada en los cursos 01 y 02; sin publicar en el resto hasta su apertura.
- **Índice:** carpetas y páginas según `cursos[].indice`, todas sin publicar hasta que la lección exista.
- **Portadas:** carpeta `skool/catalogo/portadas/` (1460 × 752 JPG, medida no oficial; **comprobar en pantalla** el recorte).
- **Comprobar en pantalla:** límite de caracteres del título (el más largo, el 27, tiene 54) y de la descripción (la más larga, 145); texto del candado con la interfaz en español; cómo ve un miembro gratis un curso Privado sin plan en un grupo freemium (cuenta de prueba gratis y otra de pago, con captura, antes de abrir).

## 12. Calendario

- [ ] Ninguno por ahora: no hay directo semanal (decisión de Marc del 29-10). Si algún día hace falta, Skool Call está en los dos planes (help 210).

## 13. Publicaciones fijadas (3, el máximo)

HECHO: hasta 3 fijadas en el muro (help 38); correo a todos como mucho una vez cada 72 horas (interfaz de Skool).

### Fijada 1 · categoría Avisos

```text
Empieza aquí: tu primera semana

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

En claro: una prueba por semana, medida contra ti mismo. ¿Cuál es la tuya?
```
- Al abrir, enviarla por correo a todos (como mucho una vez cada 72 horas).

### Fijada 2 · categoría Pregunta a Marc

```text
Cómo pedir ayuda (y que sirva)

Una pregunta bien hecha se contesta a la primera. Publícala en «Pregunta a Marc» con estas cinco líneas:

1. A qué te dedicas: qué vendes o qué haces, y para quién.
2. Qué querías conseguir.
3. Qué has probado, en qué curso y en qué lección.
4. Qué ha pasado, con una cifra si la tienes (tuya, de antes y de después).
5. Qué necesitas saber exactamente.

Si añades una captura, que no salgan datos de tus clientes, contraseñas ni nada privado.

Te contesto en el hilo, en público, para que la respuesta sirva también a quien venga detrás. Si una duda se repite, la convierto en un vídeo de respuesta y lo aviso en «Avisos».

Lo que no va en el muro: cobros, planes, facturas y bajas. Eso escríbelo a info@brandooers.com y lo vemos en privado.

Y una cosa que no hago: revisar negocios uno a uno. Si haces la prueba de la lección y me cuentas qué te ha salido, te ayudo a leerlo.
```
- Correo de cobros y bajas: comprobar con Marc que es info@brandooers.com.

### Fijada 3 · categoría Preséntate

```text
Preséntate: copia esta plantilla

Copia estas líneas en una publicación nueva de la categoría «Preséntate» y rellénalas:

Me llamo:
A qué me dedico (qué vendo o qué hago, y para quién):
Lo que quiero que sea distinto dentro de un mes:
Por dónde empiezo (bloque del aula):
Mi primera prueba y el día en que la mido:

Cuando la publiques, comenta la presentación de alguien que esté en lo mismo que tú. Así empieza esto: probando y contándolo.
```

## 14. Antes de abrir la entrada

- [ ] Cuenta de prueba en el plan gratis y otra en el de pago: captura de cómo se ve cada tipo de curso.
- [ ] Revisión de legal-rgpd-proteccion-datos de la pregunta 3 y del Zap 1 con nombre y correo; de legal-publicidad-consumo del aviso de la escalera de precios en brandooers.com (precio final con IVA).
- [ ] brand-separation-gate en verde: en ninguna pantalla sale otra marca de Marc ni su empresa, solo SkillUp Brandooers.
- [ ] Ninguna extensión de terceros con la sesión de la cuenta dueña (condiciones de Skool, help 179 y 186).

## Decisiones de Marc (3)

1. Moneda (dólares) y si se abre ya el plan anual a 10 veces el mes.
2. Dirección del grupo: skillup-brandooers o ide-brandooers (solo el primer cambio es gratis).
3. Recompensa del nivel 5: abrir «Que te encuentren» con «nivel 5 O plan de pago», o ninguna.
