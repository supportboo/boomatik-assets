# Odoo Canon — Biblioteca canónica de pantallazos reales de Odoo

Catálogo de imágenes oficiales de Odoo descargadas desde `odoo.com` y `github.com/odoo/odoo`. Material para composiciones visuales en blog, landings y materiales comerciales del ecosistema BOO sin necesidad de inventar UI.

Norma vinculante: cualquier imagen del ecosistema que muestre Odoo SIEMPRE usa material de esta biblioteca. Nada de UI inventada con Nano Banana / Imagen 4.0. Ver `feedback_odoo_real_screenshots_only.md` en la memoria global Claude.

## Inventario

| Carpeta | Cantidad | Tamaño | Descripción |
|---|---|---|---|
| `odoo-logo-official.png` | 1 | 3 KB | Logo oficial Odoo press kit |
| `screenshots/page-shots/` | 40 | ~50 MB | Capturas full-page de odoo.com (apps + pages comerciales) |
| `screenshots/raw-images/` | 391 | ~470 MB | Assets embebidos referenciados en odoocdn.com |
| `screenshots/INVENTORY.json` | 1 | 90 KB | Metadata estructurada (path, description, source_url, kind, last_updated) por imagen |

**Total: 432 imágenes oficiales · ~520 MB.**

Biblioteca complementaria de scrape modular en `boomatik-brain/assets/odoo-screenshots/raw/` con 1.300 imágenes adicionales agrupadas en 34 módulos (`crm`, `point-of-sale`, `accounting`, `inventory`, etc.). El catálogo combinado supera las 1.700 imágenes Odoo reales.

## INDEX.html (navegador visual)

`INDEX.html` es un catálogo navegable con buscador en vivo y agrupación por sección. Abre en local con doble clic. Tamaño 1.1 MB.

URL pública vía jsDelivr (CDN GitHub):
```
https://cdn.jsdelivr.net/gh/supportboo/boomatik-brain/identity/odoo-canon/INDEX.html
```

## Uso desde código

```python
from pathlib import Path
import json

CANON = Path.home() / "boomatik-brain" / "identity" / "odoo-canon"
PAGE_SHOTS = CANON / "screenshots" / "page-shots"
RAW_IMAGES = CANON / "screenshots" / "raw-images"
INVENTORY = json.load(open(CANON / "screenshots" / "INVENTORY.json", encoding="utf-8"))

# Ejemplo: localizar la captura full-page de la app CRM
for key, meta in INVENTORY.items():
    if meta["kind"] == "page_shot" and "crm" in meta["source_url"]:
        print(meta["path"])
```

Compositor canónico que tira de esta biblioteca para generar imágenes con backplate brand + UI Odoo real:
```
boomatik-automation/odoo_nextdoo/pipeline/real_screenshots.py
```

## Mantenimiento

- Refrescar catálogo: `python build_index_html_2026-06-20.py` regenera `INDEX.html` con el estado actual de carpetas.
- Refrescar scrape modular: `boomatik-brain/assets/odoo-screenshots/scrape_odoo_assets_2026-06-20.py`.
- Verificar nuevos page-shots después de cada release Odoo mayor (cada 6 meses aprox).

## Acceso CDN para apps BOO

Para usar desde una app sin tener el repo clonado, jsDelivr sirve cualquier fichero del repo a velocidad de CDN:

```
https://cdn.jsdelivr.net/gh/supportboo/boomatik-brain/identity/odoo-canon/screenshots/page-shots/app-crm.png
https://cdn.jsdelivr.net/gh/supportboo/boomatik-brain/identity/odoo-canon/screenshots/page-shots/app-point-of-sale-shop.png
https://cdn.jsdelivr.net/gh/supportboo/boomatik-brain/identity/odoo-canon/odoo-logo-official.png
```

Patrón: `cdn.jsdelivr.net/gh/<user>/<repo>@<branch>/<path>`. Por defecto sirve `HEAD` del branch principal.
