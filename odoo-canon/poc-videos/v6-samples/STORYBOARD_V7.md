# Storyboard V7 — Demo Odoo MotoStore · 125 segundos · paso a paso

Fecha: 2026-06-20 · Cliente target: gerente pyme española sin perfil técnico

---

## Filosofía editorial (lo que cambia respecto a v6)

1. **El tiempo es para entender, no para impresionar.** Cada navegación lleva 1,2 s de aire antes de hablar (el ojo necesita aterrizar en lo nuevo).
2. **Una idea por escena.** Frases ≤ 14 palabras. Nunca apilamos conceptos.
3. **Pausa de impacto tras money words.** 0,5 s después de "automáticamente", "sin re-introducir", "solo".
4. **El cursor llega antes que la palabra.** Pre-move 800 ms para que el espectador siga el movimiento como si fuera natural.
5. **El zoom subraya conceptos, no decora.** Solo cuando el copy lo nombra ("este precio", "esta tarjeta").
6. **Subtítulo siempre legible.** Frase completa visible, palabra activa en violeta grande, contexto en blanco pequeño.

---

## Cronología completa · 7 actos · 21 escenas

### ACTO 1 · CONTEXTO (00:00 → 00:15)

| t_in | t_out | Copy literal (palabra **trigger**) | Pantalla | Cursor / acción | Factor importante |
|---|---|---|---|---|---|
| 0,0 | 5,5 | "Te enseño cómo una **tienda** de cascos vende y procesa todo con Odoo, de principio a fin." | tab outletcascos.com home (pre-cargado) | `bring_to_front` en "tienda" (1,4 s) · scroll hero | Setup: ya tienen contexto retail |
| 5,5 | 10,5 | "Esto es **Outlet** Cascos, una tienda real con catálogo en tiempo real." | scroll suave hasta grid productos | scroll a y=600 en "Outlet" | "tiempo real" = factor |
| 10,5 | 16,5 | "Cuando un cliente compra un casco, **detrás** empieza un proceso en Odoo. Te lo enseño." | switch tab outletcascos /shop (pre-cargado) | `bring_to_front` en "detrás" · zoom 1,5x sobre `.product_price` durante "tiempo real" | "detrás" = pivote a backend |

### ACTO 2 · EL ESCRITORIO ODOO (00:15 → 00:25)

| t_in | t_out | Copy | Pantalla | Cursor / acción | Factor |
|---|---|---|---|---|---|
| 16,5 | 22,0 | "Este es el **escritorio** de Odoo, con todas las áreas de la empresa." | switch tab demo.odoo.com/odoo (pre-cargado, ya reemplazado "Demo Company"→"MotoStore España SL") | `bring_to_front` en "escritorio" · 1,5 s de aire | Visión global |
| 22,0 | 27,5 | "Cada aplicación se **conecta** con las otras. Sin duplicar datos." | mismo escritorio, cursor pasea entre iconos | cursor pre-move sobre CRM en "conecta" + hover Sales en "duplicar" | "Sin duplicar datos" = money word #1 |

### ACTO 3 · CRM (00:25 → 00:50)

| t_in | t_out | Copy | Pantalla | Cursor / acción | Factor |
|---|---|---|---|---|---|
| 27,5 | 31,5 | "Empezamos por el **CRM**, el área comercial." | escritorio | cursor pre-move sobre `.o_app:has-text("CRM")` en "Empezamos", click en "CRM" exacto + ripple en punta | Inicio del recorrido |
| 31,5 | 39,5 | "Aquí está el **pipeline** de oportunidades de venta. Cada tarjeta es un cliente con su importe y su etapa." | pipeline kanban (cargado <2s tras click) | 1,2 s de aire · zoom 1,3x sobre `.o_kanban_group` en "pipeline" · zoom-reset 6,0 s | "Cada tarjeta es un cliente" |
| 39,5 | 47,0 | "Si entramos a una **oportunidad**, vemos cliente, presupuesto y próximas acciones." | click 1ª `.o_kanban_record` | cursor pre-move en "entramos", click en "oportunidad" + ripple | Detalle del lead |
| 47,0 | 53,0 | "Cuando una oportunidad se gana, se convierte **automáticamente** en pedido de venta." | quedarse en la ficha | hover "Mark Won" o "Convertir" en "automáticamente" + pausa 0,5 s | money word #2 "automáticamente" |

### ACTO 4 · VENTAS (00:53 → 01:13)

| t_in | t_out | Copy | Pantalla | Cursor / acción | Factor |
|---|---|---|---|---|---|
| 53,0 | 57,5 | "Pasamos a **Ventas**." | back home + click Sales | cursor pre-move sobre `.o_app:has-text("Sales")` en "Pasamos", click en "Ventas" | Transición clara |
| 57,5 | 65,5 | "Aquí están todos los **pedidos** confirmados, con cliente, fecha y total." | lista pedidos cargada | 1,2 s de aire · zoom 1,25x sobre 1ª `.o_data_row` en "pedidos" · zoom-reset 4 s | Vista 360 ventas |
| 65,5 | 73,0 | "En el detalle vemos las **líneas** de producto y la cantidad pedida." | click 1ª fila | cursor pre-move en "detalle", click en "líneas" + ripple | Granularidad |

### ACTO 5 · INVENTARIO (01:13 → 01:33)

| t_in | t_out | Copy | Pantalla | Cursor / acción | Factor |
|---|---|---|---|---|---|
| 73,0 | 77,0 | "Pasamos a **Inventario**." | back home + click Inventory | cursor pre-move sobre `.o_app:has-text("Inventory")` en "Pasamos", click en "Inventario" | Transición |
| 77,0 | 85,0 | "Cada pedido confirmado genera una **transferencia** de salida del almacén." | dashboard transferencias | 1,2 s de aire · zoom 1,3x sobre `.o_kanban_record` en "transferencia" · zoom-reset 4 s | Flujo automático |
| 85,0 | 93,0 | "El **stock** se descuenta en tiempo real. Sin re-introducir datos." | mismo dashboard | pausa 0,5 s tras "stock" · sin zoom adicional | money word #3 "Sin re-introducir" |

### ACTO 6 · CONTABILIDAD (01:33 → 01:55)

| t_in | t_out | Copy | Pantalla | Cursor / acción | Factor |
|---|---|---|---|---|---|
| 93,0 | 97,5 | "Y por último, **Contabilidad**." | back home + click Accounting | cursor pre-move sobre `.o_app:has-text("Accounting")`, click en "Contabilidad" | Cierre del ciclo |
| 97,5 | 106,0 | "Aquí se prepara la **factura** del pedido con todos los datos fiscales españoles." | dashboard contabilidad | 1,2 s de aire · zoom 1,3x sobre `.o_kanban_record` "Customer Invoices" en "factura" | Cumplimiento ES |
| 106,0 | 115,0 | "Y el **asiento** contable se registra solo: ingreso, IVA y cliente pendiente." | mismo dashboard | cursor hover sobre asiento en "asiento", pausa 0,5 s tras "solo" | money word #4 "solo" |

### ACTO 7 · MONEY MOMENT + CIERRE (01:55 → 02:15)

| t_in | t_out | Copy | Pantalla | Cursor / acción | Factor |
|---|---|---|---|---|---|
| 115,0 | 122,0 | "Una **sola** plataforma. Sin re-introducir datos en ningún paso." | back home (vista wide apps) | 1,5 s aire · zoom 1,4x sobre conjunto apps en "sola" · zoom-reset en "ningún" | money word #5 + recapitulación |
| 122,0 | 127,5 | "Del **clic** del cliente en la web hasta el asiento contable de la venta." | montaje rápido: shop → pipeline → asiento (3 cortes rápidos de 1 s cada uno) | switch tabs rápido · cursor solo en el último corte | El círculo se cierra |
| 127,5 | 132,5 | "Esto es **Odoo** trabajando de verdad. Si lo quieres para tu negocio, contacta con Nextdoo." | end card estático: logo Nextdoo + URL nextdoo.cloud + "Partner Odoo Enterprise" | sin acciones, fade overlay | CTA cierre |

**TOTAL: 132,5 s · 2 min 12 s**

---

## Money words (los 5 mensajes que vende la demo)

1. **"Sin duplicar datos"** (00:25) — el dolor #1 del gerente pyme
2. **"Automáticamente"** (00:48) — la promesa de Odoo
3. **"Sin re-introducir datos"** (01:31) — repetido para reforzar
4. **"Solo"** (01:13) — refiriéndose al asiento contable que se hace solo
5. **"Una sola plataforma"** (01:55) — el cierre conceptual

Cada uno lleva pausa 0,5 s después + zoom o énfasis visual.

---

## Datos motos ES inyectados en demo.odoo.com (vía MutationObserver agresivo)

| Texto original | Texto inyectado |
|---|---|
| Demo Company | MotoStore España SL |
| Office Design | Casco Shoei NXR2 Negro Mate |
| Modern Open Space | Casco Modular Schuberth C5 |
| Global Solutions: Furnitures | Guantes Alpinestars SP-8 v3 |
| Ready Mat | Mono Dainese Mugello |
| Open Wood | Botas Dainese Torque 3 Out |
| Quote for 12 Tables | Presupuesto 4 cascos integral |
| Quote for 600 Chairs | Pedido 10 monos pista |
| Erik N. French | Jorge Morales |
| McEncroe | Cascos Albacete SL |
| Acme Corporation | Distribuciones Moto Levante |
| Customers | Clientes |
| Sales Orders | Pedidos de venta |
| Quotations | Presupuestos |
| Invoices | Facturas |
| Vendor Bills | Facturas de proveedor |
| Won | Ganada |
| Qualified | Cualificada |
| Proposition | Propuesta |
| New | Nueva |
| $ 80,000.00 | 74.000 € |
| $ 3,800.00 | 3.500 € |

Aplicado con `MutationObserver(document, {childList:true, subtree:true, characterData:true})` que reescribe en TODO el árbol al cargar y en cada mutación SPA.

---

## Especificaciones técnicas v7

### Pre-load (Fase A, no se graba)

```python
ctx = await browser.new_context(record_video_dir=str(VIDEO), ...)
tabs = await asyncio.gather(
    ctx.new_page(),  # outletcascos.com/
    ctx.new_page(),  # outletcascos.com/shop
    ctx.new_page(),  # demo.odoo.com/odoo (escritorio)
    ctx.new_page(),  # demo.odoo.com/odoo (otra instancia para SPA backend)
)
await asyncio.gather(*[t.goto(url) for t, url in zip(tabs, URLS)])
await asyncio.gather(*[t.evaluate(INJECT_V7) for t in tabs])
# Verificar que reemplazos motos ES están aplicados
assert "MotoStore España SL" in await tabs[2].text_content("body")
```

### Producción (Fase B, sí se graba)

- Cronómetro `time.monotonic()` parte en t=0
- Para cada palabra trigger, ejecutar la acción ANTES (cursor pre-move) y DURANTE (click/zoom/switch)
- Switch entre tabs vía `tab.bring_to_front()` (instantáneo)
- Clicks con `no_wait_after=True` para no bloquear

### Post (Fase C)

- Mux audio + vídeo SIN `-shortest` (preservar duración completa)
- Subs ASS karaoke: frase completa visible, palabra activa fontsize 48, contexto fontsize 32
- (Opcional) Overlay HeyGen 150 px inf-dcha cuando llegue API key

### Voz Marc

- `eleven_multilingual_v2` + speed 1.0 + similarity 0.88 + language "es" + stability 0.62
- Pronunciación: "Odoo" → "Odú"
- 21 escenas sintetizadas con `with-timestamps`
- Timestamps de cada palabra usados para construir el schedule absoluto

---

## QA checklist antes de publicar

- [ ] Duración total: 130-135 s
- [ ] 21 escenas todas presentes en el vídeo final (sin `-shortest`)
- [ ] Voz Marc ES España sin acento LATAM
- [ ] "MotoStore España SL" visible en el escritorio Odoo (no "Demo Company")
- [ ] Cursor visible en cada escena del backend (verificar frame por frame en t=30, 50, 70, 90, 110)
- [ ] Ripple centrado en la punta del cursor en cada click
- [ ] Subtítulos sin fondo gris, palabra activa fontsize 48 violeta
- [ ] Frase completa siempre visible (no solo la palabra activa)
- [ ] Cada palabra trigger sincronizada con su acción visual (±100 ms)
- [ ] Money words enfatizados con zoom + pausa
- [ ] CTA "contacta con Nextdoo" claro en cierre

---

## Lo que necesito de ti

**Una sola respuesta para arrancar:**

> "OK plan, ejecuta"

Y arranco. Tiempo estimado de ejecución:
- ~3 min ElevenLabs (21 audios)
- ~3 min pre-load + grabación
- ~1 min post (mux + subs)
- **Total: ~7 min**

Si quieres modificar copys, money words, orden de actos, dímelo y lo cambio antes de ejecutar.
