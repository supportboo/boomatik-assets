# Storyboard Demo Odoo MotoStore v6 — Plan Senior

Fecha: 2026-06-20 · Autor: Claude Code Max + 6 roles · Cliente final: gerente pyme ES

---

## 1. Equipo creativo activado

| Rol | Responsabilidad | Decisión clave |
|---|---|---|
| Storyteller | Guion 3 actos · setup-conflict-resolution | Hook 4s, demo 60s, cierre 8s |
| Video Director | Planos, cortes, ritmo | 1 corte ≤ cada 6 s · zoom para "money moments" |
| Copy Impact | "Money words" que ganan al cliente | Sin re-introducir, automáticamente, tiempo real, una sola |
| UX Choreographer | Cursor y clicks reales | Cursor pointer 18 px, ripple en la PUNTA, easing natural |
| Localization ES | Lengua y ñ | Cero anglicismos, motos ES, JLM mencionable |
| QA Sync | Sync palabra-imagen | Δ desfase ≤ 80 ms entre trigger y acción |

---

## 2. Arquitectura técnica corregida (vs v5)

**Problema v5:** audio se genera, vídeo intenta seguir con `waits` aproximados. Cualquier carga de página 200 ms más lenta rompe el sync.

**Fix v6:** **schedule de tiempos absolutos** ejecutado por un timer:

1. Genero audio TODO de una pasada → obtengo timestamps por palabra de ElevenLabs.
2. Para cada escena identifico la **palabra trigger** (la que debe coincidir con la acción visual).
3. Construyo un `schedule = [(t_abs_seg, accion)]` con acciones precargadas (cursor pre-moves antes del trigger).
4. La grabación arranca un cronómetro a t=0; cada acción se ejecuta cuando el reloj llega a su t.
5. ffmpeg mux audio+vídeo SIN reajuste de timestamps (`-itsoffset 0`).

Resultado: si la voz dice "CRM" en t=18,4 s, el click ocurre en t=18,4 s (no en t≈18 s).

---

## 3. Cursor y click corregidos

**Cursor (SVG nuevo, 18 px):**
```svg
<svg viewBox="0 0 16 16" width="18" height="18">
  <path d="M0,0 L0,12 L3.5,9 L6,15 L8,14 L5.5,8.5 L10,8.5 Z"
        fill="#FFFFFF" stroke="#0A0A0E" stroke-width="1.2" stroke-linejoin="round"/>
</svg>
```
La PUNTA está en (0, 0) del SVG (esquina sup-izda) → es el punto exacto del click.

**Click ripple (centrado en la punta, no en el centro):**
- Posición: `left: cursorX - 6px; top: cursorY - 6px` (la punta del cursor está en (cursorX, cursorY) directamente, sin offset)
- Tamaño: 0 → 72 px en 600 ms
- Color: violeta `#A855F7` con outline

**Movimiento del cursor:**
- Curva Bezier suave en lugar de línea recta (`cubic-bezier(.22,.61,.36,1)`)
- Duración 380 ms entre puntos
- Ease-out: rápido al salir, lento al llegar

**Sin cursor del sistema Playwright:** apago el cursor nativo del navegador con CSS `* { cursor: none !important; }` en el body.

---

## 4. Subtítulos corregidos

| Atributo | v5 (malo) | v6 (correcto) |
|---|---|---|
| Background | gris oscuro `BackColour=&H80000000` + `BorderStyle=3` | NO HAY background. Solo outline negro 2 px |
| Fontsize | 16-22 px (demasiado pequeño) | **48 px palabra activa**, 32 px contexto antes/después |
| Color activa | Violeta `#F770FA` | Violeta `#F770FA` con outline negro grueso |
| Color contexto | Blanco apagado | Blanco `#FFFFFF` con outline negro |
| Posición | Bottom 60 | Bottom 100, alignment 2 (centrado) |
| Estilo | Como TV | TikTok karaoke clásico: palabra grande, vecinas pequeñas |

ASS spec:
```
Style: Active,Inter,48,&H00F770FA,&H00FFFFFF,&H000A0A0E,&H00000000,1,0,0,0,100,100,0,0,1,3,0,2,40,40,100,1
Style: Ctx,Inter,32,&H00FFFFFF,&H000000FF,&H000A0A0E,&H00000000,0,0,0,0,100,100,0,0,1,2,0,2,40,40,100,1
```
(Sin BorderStyle=3 = sin background sólido detrás)

---

## 5. Datos demo Odoo en español (inyección visual)

`demo.odoo.com` tiene productos de muebles ingleses ("Office Design", "Modern Open Space"). En v6 inyecto JS que **reemplaza el texto visible** sin tocar la DB, convirtiendo la pantalla en MotoStore España:

| Texto demo original | Texto inyectado motero ES |
|---|---|
| Demo Company | MotoStore España SL |
| Office Design | Casco Shoei NXR2 Negro Mate |
| Modern Open Space | Casco Modular Schuberth C5 |
| Global Solutions | Guantes Alpinestars SP-8 v3 |
| Furnitures / Furniture | Equipación moto |
| Open Wood | Botas Dainese Torque 3 Out |
| Ready Mat | Mono Dainese Mugello |
| Erik N. French | Jorge Morales (cliente) |
| McEncroe | Cascos Albacete SL |
| Acme Corp | Distribuidora Moto Levante |
| Quote for 12 Tables | Presupuesto 4 cascos |
| 600 Chairs | 10 monos pista |
| $ 80,000.00 | 4.250 € |
| $ 3,800.00 | 379 € |
| Won | Ganada |
| Qualified | Cualificada |
| Proposition | Propuesta |
| New | Nueva |

Tras cada navegación SPA o reload, se re-aplica el reemplazo con `MutationObserver`.

---

## 6. Storyboard time-coded (5 actos · 14 escenas · 72 s)

### ACTO 1 · Hook (00:00 — 00:08)

| t_start | Narración (palabra **trigger** en negrita) | Plano | Acción visual |
|---|---|---|---|
| 0,0 s | "Una **tienda** de cascos vende online y al cliente le llega su pedido al día siguiente." | OutletCascos hero | goto outletcascos.com en t=0; pre-scroll a 0 |
| 4,2 s | "Detrás hay un **proceso** que Odoo automatiza de principio a fin." | Catálogo /shop con zoom precio | goto /shop en t=4.0, zoom 1.5x en t=5.5 sobre `.product_price` |

### ACTO 2 · Setup compra cliente (00:08 — 00:18)

| 8,0 s | "El cliente **compra** un casco y termina el pedido." | Frontend casco card | scroll/click en producto · ripple en botón añadir |
| 12,5 s | "En el **backend** de Odoo, el pedido entra solo." | Pivot a demo.odoo.com | goto demo.odoo.com, inyectar overlay ES |

### ACTO 3 · Recorrido backend (00:18 — 00:58)

| 18,0 s | "Esto es el escritorio con todas las **apps**." | Apps wide | mostrar escritorio · cursor llega a CRM en 17.6 |
| 20,5 s | "Abrimos **CRM**." | Zoom out → in | click CRM en t=20.7 (palabra "CRM") |
| 23,5 s | "Aquí está el **pipeline** comercial." | CRM kanban con zoom 1.3x | zoom 1.3x sobre `.o_kanban_group` en t=24.0 |
| 28,0 s | "Cada **tarjeta** es una venta con cliente y precio." | Detalle tarjeta zoom 1.5x | zoom 1.5x sobre 1ra `.o_kanban_record` |
| 33,0 s | "Pasamos a **Ventas**." | Cambio de plano | back home, cursor a Sales en t=32.6, click en t=33.2 |
| 36,5 s | "Aquí están los **pedidos** confirmados con sus líneas." | Sales list zoom 1.25x sobre 1ra row | zoom sobre `.o_data_row:nth-child(1)` |
| 42,0 s | "**Inventario**: el almacén baja stock automáticamente." | Click Inventory | back home, click Inventory en t=42.0 |
| 47,0 s | "**Contabilidad** cierra el ciclo: factura y asiento." | Click Accounting | back home, click Accounting en t=47.0 |

### ACTO 4 · Money moment (00:58 — 01:08)

| 58,0 s | "Una **sola** plataforma." | Zoom escritorio + apps | back home con apps visibles |
| 61,5 s | "**Sin** re-introducir datos." | Énfasis con zoom | zoom 1.4x sobre conjunto de apps centrales |
| 65,0 s | "Del **clic** del cliente al **asiento** contable de la venta." | Split visual rápido | montaje: corte rápido shop → kanban → asiento |

### ACTO 5 · CTA cierre (01:08 — 01:12)

| 68,0 s | "Esto es **Odoo** trabajando en una tienda real de motos. Contacta con Nextdoo." | End card statico | overlay final con logo + URL |

**Total estimado: 72 s · 14 escenas · 5 actos.**

---

## 7. Money words (lo que vende, ZOOM aquí)

1. **"automáticamente"** → zoom sobre el campo que cambia solo
2. **"tiempo real"** → zoom sobre stock o pipeline
3. **"sin re-introducir"** → split rápido frontend ↔ backend
4. **"una sola plataforma"** → wide shot de todas las apps
5. **"del clic al asiento"** → split visual web → asiento

---

## 8. Voz Marc — canon validado

Audio referencia: `C:/Users/march/Downloads/marc-voz-CANON-OPTIMIZADO-pro.mp3` (17.6 s, 192 kbps).

Settings v6:
- `voice_id = ILNSYKWBF65GlgJYtEYk` (entrenado 9:44 min, canon CERRADO)
- `model_id = eleven_multilingual_v2` (más estable que v3 para ES, evita LATAM)
- `language_code = "es"`
- `stability = 0.62` (sube vs 0.55 para más consistencia ES España)
- `style = 0.18` (baja para evitar inflexiones LATAM)
- `similarity_boost = 0.88` (alto para fijar timbre)
- `use_speaker_boost = true`
- `speed = 1.0` (NO subir, derivaba a LATAM)
- Pronunciación: regex `\bOdoo\b → Odú`

Validación voz en cada render:
- Spectrogram diff vs canon mp3
- Si diff > umbral, retry con `stability += 0.05`

---

## 9. QA checklist antes de publish

- [ ] Cada palabra trigger sincronizada ±80 ms con su acción visual
- [ ] Cursor visible en TODAS las escenas backend (verificar frame por frame)
- [ ] Ripple centrado en la punta del cursor (no en el centro)
- [ ] Subtítulos sin fondo gris, fontsize 48
- [ ] Textos demo reemplazados a motos ES (no debe aparecer "Demo Company")
- [ ] Banner "This is a demo database" oculto
- [ ] Voz suena Marc canon (sin acento argentino)
- [ ] Money words enfatizados con zoom
- [ ] Duración entre 60-80 s

---

## 10. Pipeline ejecución

1. **Generar audio** todas las escenas con `with-timestamps`
2. **Calcular schedule** time-coded usando word timestamps reales
3. **Pre-grabar** con timer ejecutando schedule
4. **Inyectar reemplazos ES** vía MutationObserver
5. **Mux audio+vídeo** sin offset
6. **Burn subs ASS** con styles corregidos
7. **Verificar QA checklist**
8. **Push CDN** y URL al cliente

---

## 11. Si validas este plan

Te paso de inmediato:
1. Sample voz Marc nuevo con settings v6 (5 s, valídalo contra tu MP3 canon)
2. Vista preview del nuevo cursor + ripple
3. Sample subtítulo con un fragmento de 3 s (sin background, fontsize correcto)

Si las 3 muestras te encajan, lanzo grabación v6 completa.

Si algo no encaja (ej. quieres OTRO cursor estilo Apple, o cambio de plan), itero antes de gastar render completo.
