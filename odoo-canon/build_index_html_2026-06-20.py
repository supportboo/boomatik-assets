"""Genera un INDEX.html navegable con TODA la biblioteca Odoo screenshots.

Cubre:
- identity/odoo-canon/odoo-logo-official.png + polo-references/
- identity/odoo-canon/screenshots/page-shots/ (40 full-page de odoo.com)
- identity/odoo-canon/screenshots/raw-images/ (391 embedded de odoocdn.com)
- assets/odoo-screenshots/raw/<module>/ (1300 scrape módulos prioritarios)

Output: identity/odoo-canon/INDEX.html
Estilo: dark Nextdoo · grid responsive · buscador en vivo · contador por sección.
"""
from __future__ import annotations

import html
import json
import re
from datetime import datetime
from pathlib import Path

BRAIN = Path("C:/Users/march/boomatik-brain")
CANON = BRAIN / "identity" / "odoo-canon"
PAGE_SHOTS = CANON / "screenshots" / "page-shots"
RAW_IMAGES = CANON / "screenshots" / "raw-images"
INVENTORY = CANON / "screenshots" / "INVENTORY.json"
ASSETS_RAW = BRAIN / "assets" / "odoo-screenshots" / "raw"
OUTPUT = CANON / "INDEX.html"

VALID_EXT = {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg"}


def list_imgs(folder: Path) -> list[Path]:
    if not folder.exists():
        return []
    return sorted([p for p in folder.iterdir() if p.is_file() and p.suffix.lower() in VALID_EXT])


def kb(p: Path) -> int:
    try:
        return p.stat().st_size // 1024
    except Exception:
        return 0


USE_RELATIVE = True  # True: rutas relativas (sirve en CDN/local), False: file:///


def card(p: Path, meta: dict | None = None) -> str:
    abs_path = str(p.resolve()).replace("\\", "/")
    name = p.name
    if USE_RELATIVE:
        # Calcula la ruta relativa desde OUTPUT (que vive en CANON) al archivo.
        try:
            rel = p.resolve().relative_to(CANON.resolve()).as_posix()
            src = rel
        except ValueError:
            src = f"file:///{abs_path}"
    else:
        src = f"file:///{abs_path}"
    size = kb(p)
    label_extra = ""
    if meta:
        if meta.get("source_url"):
            label_extra += f'<div class="src">{html.escape(meta["source_url"])}</div>'
        if meta.get("description"):
            label_extra += f'<div class="desc">{html.escape(meta["description"])}</div>'
    return f'''<figure class="card" data-name="{html.escape(name.lower())}" data-size="{size}">
  <a href="{src}" target="_blank"><img src="{src}" loading="lazy" alt="{html.escape(name)}"/></a>
  <figcaption>
    <div class="name">{html.escape(name)}</div>
    <div class="meta">{size} KB · {p.suffix.lstrip(".")}</div>
    {label_extra}
  </figcaption>
</figure>'''


def section(title: str, cards: list[str], anchor: str, total_label: str = "") -> str:
    return f'''<section id="{anchor}" class="sec">
  <header class="sec-head">
    <h2>{html.escape(title)}</h2>
    <div class="count">{len(cards)} imágenes{total_label}</div>
  </header>
  <div class="grid">{''.join(cards)}</div>
</section>'''


def main() -> None:
    inv: dict = {}
    if INVENTORY.exists():
        inv = json.load(open(INVENTORY, encoding="utf-8"))
    inv_by_path: dict[str, dict] = {Path(v["path"]).name: v for v in inv.values() if v.get("path")}

    # --- 1. Logo + polo-references (identity raíz) ---
    raiz_cards: list[str] = []
    for p in [CANON / "odoo-logo-official.png"]:
        if p.exists():
            raiz_cards.append(card(p))
    polo = CANON / "polo-references"
    for p in list_imgs(polo):
        raiz_cards.append(card(p))

    # --- 2. Page-shots (full-page odoo.com) ---
    page_cards: list[str] = []
    for p in list_imgs(PAGE_SHOTS):
        meta = inv_by_path.get(p.name, {})
        page_cards.append(card(p, meta))

    # --- 3. Raw-images (embedded de odoocdn.com) ---
    raw_cards: list[str] = []
    for p in list_imgs(RAW_IMAGES):
        meta = inv_by_path.get(p.name, {})
        raw_cards.append(card(p, meta))

    # --- 4. Scrape por módulo ---
    # Solo se incluye si está dentro de CANON (modo publicable CDN). En modo
    # local pasa file:/// y funciona.
    module_sections: list[str] = []
    scrape_in_canon = CANON / "scrape-modules"
    scrape_source = scrape_in_canon if scrape_in_canon.exists() else (
        ASSETS_RAW if not USE_RELATIVE else None
    )
    if scrape_source and scrape_source.exists():
        modules = sorted([d for d in scrape_source.iterdir() if d.is_dir()])
        for mdir in modules:
            cards = [card(p) for p in list_imgs(mdir)]
            if cards:
                module_sections.append(section(
                    f"Módulo · {mdir.name}",
                    cards,
                    f"mod-{mdir.name}",
                ))

    extra = 0
    nav_modules = ""
    if scrape_source and scrape_source.exists():
        extra = sum(len(list_imgs(d)) for d in scrape_source.iterdir() if d.is_dir())
        nav_modules = "".join(
            f'<a href="#mod-{d.name}">{d.name}</a>'
            for d in sorted(scrape_source.iterdir()) if d.is_dir()
        )
    total_imgs = len(raiz_cards) + len(page_cards) + len(raw_cards) + extra

    css = """
:root { --bg:#0A0A0E; --bg-2:#101018; --fg:#F5F5FA; --muted:#A0A0AF; --accent:#A855F7; --pink:#EC4899; --border:rgba(255,255,255,0.08); }
* { box-sizing:border-box; }
body { margin:0; font-family:'Plus Jakarta Sans',-apple-system,Segoe UI,Inter,sans-serif; background:var(--bg); color:var(--fg); }
header.top { padding:32px 40px 20px; border-bottom:1px solid var(--border); background:linear-gradient(180deg,var(--bg) 0%,var(--bg-2) 100%); position:sticky; top:0; z-index:10; }
header.top h1 { margin:0; font-size:28px; letter-spacing:-0.02em; }
header.top .sub { color:var(--muted); margin-top:6px; font-size:13px; }
.toolbar { display:flex; gap:12px; margin-top:18px; flex-wrap:wrap; align-items:center; }
.toolbar input { background:var(--bg-2); border:1px solid var(--border); color:var(--fg); padding:8px 14px; border-radius:8px; min-width:280px; font-size:14px; }
.toolbar a { color:var(--muted); text-decoration:none; font-size:12px; padding:4px 10px; border:1px solid var(--border); border-radius:999px; }
.toolbar a:hover { color:var(--accent); border-color:var(--accent); }
.nav { padding:10px 40px; background:var(--bg-2); border-bottom:1px solid var(--border); display:flex; gap:8px; flex-wrap:wrap; font-size:12px; }
.nav a { color:var(--muted); text-decoration:none; padding:3px 8px; border-radius:6px; }
.nav a:hover { color:var(--accent); background:rgba(168,85,247,0.08); }
section.sec { padding:32px 40px; border-bottom:1px solid var(--border); }
section.sec .sec-head { display:flex; justify-content:space-between; align-items:baseline; margin-bottom:20px; }
section.sec h2 { margin:0; font-size:20px; letter-spacing:-0.01em; }
section.sec .count { color:var(--accent); font-size:13px; font-weight:600; }
.grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(220px,1fr)); gap:16px; }
.card { margin:0; background:var(--bg-2); border:1px solid var(--border); border-radius:12px; overflow:hidden; transition:border-color 0.2s,transform 0.2s; }
.card:hover { border-color:var(--accent); transform:translateY(-2px); }
.card a { display:block; }
.card img { width:100%; aspect-ratio:16/10; object-fit:contain; background:#000; display:block; }
.card figcaption { padding:10px 12px; font-size:11px; }
.card .name { font-weight:600; color:var(--fg); white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.card .meta { color:var(--muted); margin-top:2px; }
.card .src { color:var(--muted); margin-top:4px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; font-size:10px; }
.card .desc { color:var(--muted); margin-top:2px; font-size:10px; }
.card.hidden { display:none; }
.empty-msg { color:var(--muted); padding:40px; text-align:center; font-size:14px; }
"""

    js = """
const input = document.getElementById('q');
input.addEventListener('input', () => {
  const q = input.value.toLowerCase().trim();
  document.querySelectorAll('.card').forEach(c => {
    if (!q) { c.classList.remove('hidden'); return; }
    const name = c.dataset.name || '';
    const match = name.includes(q) || (c.innerText || '').toLowerCase().includes(q);
    c.classList.toggle('hidden', !match);
  });
  document.querySelectorAll('section.sec').forEach(s => {
    const visible = s.querySelectorAll('.card:not(.hidden)').length;
    s.style.display = visible ? '' : 'none';
  });
});
"""

    nav_top = (
        '<a href="#identity">Identity</a>'
        '<a href="#page-shots">Page-shots</a>'
        '<a href="#raw-images">Raw-images</a>'
        + nav_modules
    )

    sections = []
    if raiz_cards:
        sections.append(section("Identity · logo + referencias polo", raiz_cards, "identity"))
    if page_cards:
        sections.append(section("Page-shots · capturas full-page odoo.com", page_cards, "page-shots", " · alta resolución 1-2.4 MB"))
    if raw_cards:
        sections.append(section("Raw-images · assets embebidos odoocdn.com", raw_cards, "raw-images"))
    sections.extend(module_sections)

    html_doc = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Biblioteca Odoo screenshots · boomatik-brain</title>
<style>{css}</style>
</head>
<body>
<header class="top">
  <h1>Biblioteca Odoo screenshots · Nextdoo · Partner Odoo Enterprise</h1>
  <div class="sub">Catálogo navegable de pantallazos reales de Odoo · {total_imgs} imágenes · generado {datetime.now().strftime('%Y-%m-%d %H:%M')}</div>
  <div class="toolbar">
    <input id="q" type="search" placeholder="Buscar por nombre, módulo o URL (ej. crm, point-of-sale, hero)…"/>
    <a href="file:///{str(CANON.resolve()).replace(chr(92),'/')}/screenshots/INVENTORY.json" target="_blank">INVENTORY.json</a>
    <a href="file:///{str(ASSETS_RAW.parent.resolve()).replace(chr(92),'/')}/index.json" target="_blank">scrape index</a>
  </div>
</header>
<nav class="nav">{nav_top}</nav>
{''.join(sections)}
<script>{js}</script>
</body>
</html>"""

    OUTPUT.write_text(html_doc, encoding="utf-8")
    print(f"OK · INDEX.html generado en {OUTPUT}")
    print(f"Total imágenes catalogadas: {total_imgs}")


if __name__ == "__main__":
    main()
