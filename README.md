# Boomatik Assets

Repositorio publico de assets de marca Boomatik. Servido via CDN gratuito **jsDelivr**.

## URL base CDN

```
https://cdn.jsdelivr.net/gh/supportboo/boomatik-assets@main/
```

## Estructura

```
logos/         -> logos oficiales BOO ghost PNG
avatars/       -> avatares cuadrados redes sociales
banners/       -> banners YouTube/LinkedIn/X
thumbnails/    -> plantillas miniaturas video
pdfs/          -> lead magnets descargables
social/        -> imagenes promocionales apps
```

## Uso

### PDF lead magnet

```
https://cdn.jsdelivr.net/gh/supportboo/boomatik-assets@main/pdfs/01_checklist_automatizar_odoo.pdf
```

### Logo en web/email

```html
<img src="https://cdn.jsdelivr.net/gh/supportboo/boomatik-assets@main/logos/boo-ghost-full.png" alt="BOO">
```

### Avatar social

```
https://cdn.jsdelivr.net/gh/supportboo/boomatik-assets@main/avatars/avatar_1080x1080.png
```

## Reglas

- Todo publico (necesario para CDN jsDelivr)
- NUNCA subir credenciales, API keys, datos clientes
- Formato PNG optimizado para logos (transparencia)
- PDFs generados desde boomatik-brain/content/lead-magnets/ con generate_pdfs.py
- Caché jsDelivr: 7 dias. Para forzar refresh usar `?purge=1` o cambiar path.

## Regenerar assets

Los scripts fuente estan en **boomatik-brain**:

- `boomatik-brain/identity/assets/generate_assets.py` -> avatares + banner + thumbnail
- `boomatik-brain/content/lead-magnets/generate_pdfs.py` -> PDFs

## Licencia

Todos los assets son propiedad de Boomatik 2026.
Uso permitido solo en contextos autorizados por Boomatik.
