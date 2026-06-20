# Plan flujo demo MotoStore v9 — paso a paso + factores WOW

Fecha: 2026-06-21 · Cliente target: gerente pyme española sin perfil técnico

---

## Orden de trabajo (cambio de paradigma)

1. **FASE 1** · Definir flujo (este documento)
2. **FASE 2** · Grabar screencast siguiendo el flujo, sin audio
3. **FASE 3** · Anotar timestamps reales del vídeo grabado
4. **FASE 4** · Escribir guion narrativo que encaje en esos timestamps
5. **FASE 5** · Generar audio Marc con duración alineada
6. **FASE 6** · Mux audio + vídeo + subs sincronizados

Resultado: sincronización 100 % porque el audio se diseña PARA el vídeo, no al revés.

---

## Coreografía del cursor (regla maestra)

El cursor se comporta como una persona enseñando:

- **No se queda quieto** · siempre va hacia el siguiente punto de interés
- **Señala antes de hablar** · hover 0,5 s sobre el elemento antes del click
- **Movimiento curvo** · Bezier easing, no líneas rectas (parece teleport)
- **Pausa visual tras click** · 0,8 s para que el ojo registre la acción
- **Ripple violeta** centrado en la punta del cursor
- **Lentitud calculada** · 600 ms entre destinos · velocidad de comprensión

---

## Flujo paso a paso · 7 actos · 30 acciones

### ACTO 1 · CONTEXTO FRONTEND (12 s)

**Pantalla**: `outletcascos.com/`

| # | Acción cursor | Pantalla | Tiempo | Factor WOW |
|---|---|---|---|---|
| 1 | Aparece en (700, 400), apuntando al hero | Home con casco grande | 0–2 s | Visual: tienda real moderna |
| 2 | Scroll suave hasta y=600, cursor baja con el scroll | Grid de productos | 2–7 s | Funcional: catálogo con precios y stock en vivo |
| 3 | Hover sobre el primer producto sin click | Casco destacado | 7–10 s | Emocional: tienda como las grandes, hecha por una pyme |
| 4 | Cursor se mueve hacia esquina sup-dcha "Mi cesta" | Indicación "compra" | 10–12 s | Setup del momento "el cliente compra" |

### ACTO 2 · PIVOTE AL BACKEND (8 s)

**Pantalla**: transición a `demo.odoo.com/odoo`

| # | Acción cursor | Pantalla | Tiempo | Factor WOW |
|---|---|---|---|---|
| 5 | Goto demo.odoo.com (transición visible) | Carga escritorio Odoo | 12–14 s | Reveal: "todo esto pasa detrás" |
| 6 | Cursor barre los iconos de izquierda a derecha | Apps visibles | 14–18 s | Visual: 30+ apps todas conectadas |
| 7 | Cursor se posa sobre el icono CRM | Highlight CRM | 18–20 s | Setup acto 3 |

### ACTO 3 · CRM (35 s)

**Pantalla**: navegación al CRM, pipeline, ficha de oportunidad

| # | Acción cursor | Pantalla | Tiempo | Factor WOW |
|---|---|---|---|---|
| 8 | Click en CRM con ripple violeta | Carga app CRM | 20–24 s | Acción "abro CRM" |
| 9 | Cursor pasea por el pipeline kanban | Vista kanban pipeline | 24–28 s | Funcional: 4 etapas claras (Nueva, Cualificada, Propuesta, Ganada) |
| 10 | Hover sobre la columna "Ganada" 1 s | Énfasis en revenue | 28–30 s | **WOW EMOCIONAL**: "Ves de un vistazo qué hay cerca de cerrar y cuánto facturas este mes" |
| 11 | Cursor baja a una tarjeta de Propuesta | Tarjeta detallada | 30–33 s | Funcional: cada tarjeta = cliente + importe + etapa |
| 12 | Click en la tarjeta con ripple | Ficha de oportunidad | 33–37 s | Acción "entro al detalle" |
| 13 | Cursor recorre los campos: cliente, productos, presupuesto, próxima acción | Datos completos | 37–43 s | **WOW EMOCIONAL**: "Toda la info del cliente en un sitio · adiós a Excel + WhatsApp + email" |
| 14 | Cursor sube al botón "Mark Won" | Botón conversión | 43–45 s | Setup del momento "se gana" |
| 15 | Hover sobre Mark Won (no click) | Énfasis acción | 45–47 s | Funcional + WOW: "Un click la convierte automáticamente en pedido de venta" |
| 16 | Cursor sube al breadcrumb para volver al home | Salir del CRM | 47–55 s | Transición |

### ACTO 4 · VENTAS (28 s)

**Pantalla**: `/odoo` home → click Sales → lista pedidos → detalle pedido

| # | Acción cursor | Pantalla | Tiempo | Factor WOW |
|---|---|---|---|---|
| 17 | Click en Sales con ripple | Lista de pedidos | 55–60 s | Acción "voy a Ventas" |
| 18 | Cursor barre las columnas de la lista | Vista listado | 60–64 s | Funcional: número, cliente, fecha, total |
| 19 | Hover sobre el primer pedido | Énfasis | 64–66 s | **WOW EMOCIONAL**: "Los pedidos llegan ya con el cliente correcto y los productos confirmados · cero teclear" |
| 20 | Click en la fila con ripple | Detalle pedido | 66–70 s | Acción "veo detalle" |
| 21 | Cursor recorre las líneas de producto | Tabla líneas | 70–78 s | Funcional: cada línea = producto + cantidad + precio + descuento |
| 22 | Hover sobre botón "Confirmar" | Acción conversión | 78–83 s | **WOW EMOCIONAL**: "Al confirmar, Odoo crea automáticamente la transferencia del almacén · no hace falta que nadie copie nada" |

### ACTO 5 · INVENTARIO (28 s)

**Pantalla**: home → click Inventory → dashboard transferencias → detalle

| # | Acción cursor | Pantalla | Tiempo | Factor WOW |
|---|---|---|---|---|
| 23 | Click en Inventory con ripple | Dashboard | 83–88 s | Acción "voy a Inventario" |
| 24 | Cursor barre las tarjetas de operaciones | Vista dashboard | 88–93 s | Funcional: recepciones, salidas, transferencias internas |
| 25 | Hover sobre tarjeta "Salidas pendientes" | Énfasis | 93–95 s | Funcional: aquí están los envíos que vienen del CRM |
| 26 | Click en la tarjeta con ripple | Lista transferencias | 95–100 s | Acción "veo qué hay que enviar" |
| 27 | Cursor pasea por las filas | Pedidos por preparar | 100–108 s | Funcional: cliente, productos, fecha prevista |
| 28 | Hover sobre cantidad de stock | Énfasis stock | 108–111 s | **WOW EMOCIONAL**: "El stock baja en tiempo real cuando se confirma la salida · adiós a roturas por información desfasada" |

### ACTO 6 · CONTABILIDAD (32 s)

**Pantalla**: home → click Accounting → dashboard → facturas → asiento

| # | Acción cursor | Pantalla | Tiempo | Factor WOW |
|---|---|---|---|---|
| 29 | Click en Accounting con ripple | Dashboard contable | 111–116 s | Acción "voy a Contabilidad" |
| 30 | Cursor barre los journals: facturas clientes, proveedor, banco, caja | Vista journals | 116–121 s | Funcional: contabilidad española estándar |
| 31 | Hover sobre tarjeta "Customer Invoices" | Énfasis facturas | 121–124 s | Setup |
| 32 | Click en Customer Invoices con ripple | Lista facturas | 124–128 s | Acción "veo facturas" |
| 33 | Cursor recorre las facturas | Lista | 128–133 s | Funcional: número, cliente, fecha, importe, estado |
| 34 | Click en una factura con ripple | Detalle factura | 133–137 s | Acción "abro factura" |
| 35 | Cursor señala el botón "Ver asiento contable" | Énfasis | 137–141 s | **WOW EMOCIONAL**: "El asiento se hace solo: ingreso por venta, IVA repercutido y cliente pendiente · tu gestoría recibe los datos listos cada mes" |
| 36 | Cursor recorre las líneas del asiento | Tabla asiento | 141–143 s | Funcional: debe/haber/cuenta |

### ACTO 7 · MONEY MOMENT + CTA (22 s)

**Pantalla**: home Odoo → wide → outletcascos → end card Nextdoo

| # | Acción cursor | Pantalla | Tiempo | Factor WOW |
|---|---|---|---|---|
| 37 | Goto home Odoo | Vista wide apps | 143–146 s | Recapitulación visual |
| 38 | Cursor barre rápidamente CRM → Sales → Inventory → Accounting | Las 4 apps recorridas | 146–151 s | **WOW MAYOR**: "Una sola plataforma · sin re-introducir datos · del clic del cliente al asiento contable" |
| 39 | Goto outletcascos.com/ (cierre del círculo) | Tienda otra vez | 151–155 s | Cierre narrativo: vuelta al inicio |
| 40 | Goto nextdoo.cloud/contactus | Página contacto Nextdoo | 155–161 s | CTA visual |
| 41 | Cursor se posa sobre formulario | Formulario destacado | 161–165 s | CTA final: contacta con Nextdoo |

**Duración total estimada del vídeo: 165 s · 2 min 45 s**

---

## Factores WOW por acto (lo que vende emocionalmente)

| Acto | Factor WOW principal | Por qué vende |
|---|---|---|
| 1 Frontend | Tienda real moderna hecha por una pyme | "Esto lo puedo tener yo" |
| 2 Backend reveal | 30+ apps conectadas en una plataforma | "Cubre toda mi empresa, no solo un trozo" |
| 3 CRM | Pipeline visual + ficha completa | "Adiós a Excel + WhatsApp + email" |
| 4 Ventas | Cero re-teclear, automatización pedido→almacén | "Mi equipo deja de duplicar trabajo" |
| 5 Inventario | Stock en tiempo real | "Adiós a vender lo que no tengo" |
| 6 Contabilidad | Asiento automático para gestoría | "Mi gestoría está contenta y yo no me preocupo" |
| 7 Cierre | Una plataforma, todo conectado | "Esto sí es rentable" |

---

## Estilo voz Marc en cada bloque

| Acto | Tono | Ejemplo de frase |
|---|---|---|
| 1 Frontend | Cercano, acogedor | "Esto es Outlet Cascos, una tienda real con catálogo en vivo." |
| 2 Backend reveal | Sorpresa controlada | "Detrás de cada compra pasa todo esto." |
| 3 CRM | Confidente | "Aquí ves de un vistazo qué hay cerca de cerrar." |
| 4 Ventas | Directo | "El pedido del cliente llega ya con todo confirmado." |
| 5 Inventario | Práctico | "Adiós a vender lo que no tienes." |
| 6 Contabilidad | Tranquilizador | "Tu gestoría recibe la información lista cada mes." |
| 7 Cierre | Cierre fuerte | "Esto es Odoo de verdad. Contacta con Nextdoo." |

---

## Plan operativo

1. **Tú validas este flujo** (o me dices qué cambiar)
2. Genero `record_demo_v9.py` que SOLO graba el screencast siguiendo el flujo
3. Lo lanzo (tarda ~3 min con el ritmo correcto + clicks reales)
4. Anoto los timestamps reales de las 41 acciones
5. Escribo el script narrativo basado en lo que se ve en cada momento
6. Genero audio Marc segmento a segmento, cada uno con duración alineada al hueco que tiene
7. Mux + subs ASS
8. Push CDN

Tiempo total estimado: ~15 min después de tu OK.

---

## Decisión

- **"OK flujo, graba"** → arranco con la grabación del screencast
- **"Cambia X"** → ajusto X y vuelvo a presentar
- **"Añade Y"** → meto Y y vuelvo a presentar

Una vez OK, no se modifica el flujo a mitad de camino. Si quieres cambios, los acumulamos para v10.
