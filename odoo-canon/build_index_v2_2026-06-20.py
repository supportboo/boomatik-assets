"""Regenera INDEX.html usando CATALOG.json con filtros facetados.

Mejora vs INDEX v1:
- Filtros en vivo por módulo, feature, best_for, kind, format
- Cards muestran tags clasificados (módulo, feature, score)
- Orden: best_for primero, luego score, luego módulo
- Mismas rutas relativas para servir en CDN y local

Output: INDEX.html (reemplaza el anterior)
"""
from __future__ import annotations

import html
import json
from datetime import datetime
from pathlib import Path

CANON = Path(__file__).resolve().parent
CATALOG = CANON / "CATALOG.json"
OUTPUT = CANON / "INDEX.html"


def main() -> None:
    if not CATALOG.exists():
        print("ERROR · CATALOG.json no encontrado. Corre build_catalog_2026-06-20.py primero.")
        return

    catalog: list[dict] = json.load(open(CATALOG, encoding="utf-8"))
    # Orden estable: best_for cover > inline > icon > skip, luego score desc
    order_best = {"cover": 0, "inline": 1, "icon": 2, "skip": 3, None: 4}
    catalog.sort(key=lambda e: (order_best.get(e.get("best_for"), 5), -e.get("score", 0), e.get("module") or "z"))

    modules = sorted({e.get("module") or "" for e in catalog if e.get("module")})
    features = sorted({e.get("feature") or "" for e in catalog if e.get("feature")})
    kinds = sorted({e.get("kind") or "" for e in catalog if e.get("kind")})
    formats = sorted({e.get("format") or "" for e in catalog if e.get("format")})

    cards_html = []
    for e in catalog:
        path = e["path"]
        size_kb = e.get("size_kb", 0)
        module = e.get("module") or ""
        feature = e.get("feature") or ""
        kind = e.get("kind") or ""
        fmt = e.get("format") or ""
        best_for = e.get("best_for") or ""
        score = e.get("score", 0)
        alt = e.get("alt", "")
        source_url = e.get("source_url", "")
        cdn = e.get("cdn", "")
        tags_str = " ".join([module, feature, kind, fmt, best_for]).lower()
        cards_html.append(f'''<figure class="card"
  data-module="{html.escape(module)}"
  data-feature="{html.escape(feature)}"
  data-kind="{html.escape(kind)}"
  data-format="{html.escape(fmt)}"
  data-best="{html.escape(best_for)}"
  data-score="{score}"
  data-text="{html.escape(tags_str)} {html.escape(path)}">
  <a href="{html.escape(path)}" target="_blank"><img src="{html.escape(path)}" loading="lazy" alt="{html.escape(alt)}"/></a>
  <figcaption>
    <div class="row1">
      <span class="best best-{html.escape(best_for or 'none')}">{html.escape(best_for or '?')}</span>
      <span class="score">{score}</span>
    </div>
    <div class="alt">{html.escape(alt)}</div>
    <div class="tags">
      {f'<span class="tag tag-module">{html.escape(module)}</span>' if module else ''}
      {f'<span class="tag tag-feature">{html.escape(feature)}</span>' if feature else ''}
      {f'<span class="tag tag-kind">{html.escape(kind)}</span>' if kind else ''}
      {f'<span class="tag tag-format">{html.escape(fmt)}</span>' if fmt else ''}
    </div>
    <div class="meta">{size_kb} KB · <a href="{html.escape(cdn)}" target="_blank">CDN</a>{f' · <a href="{html.escape(source_url)}" target="_blank">fuente</a>' if source_url else ''}</div>
  </figcaption>
</figure>''')

    css = """
:root { --bg:#0A0A0E; --bg-2:#101018; --bg-3:#181822; --fg:#F5F5FA; --muted:#A0A0AF; --accent:#A855F7; --pink:#EC4899; --emerald:#10b981; --amber:#f59e0b; --rose:#f43f5e; --border:rgba(255,255,255,0.08); }
* { box-sizing:border-box; }
body { margin:0; font-family:'Plus Jakarta Sans',-apple-system,Segoe UI,Inter,sans-serif; background:var(--bg); color:var(--fg); }
header.top { padding:24px 32px 14px; border-bottom:1px solid var(--border); background:linear-gradient(180deg,var(--bg) 0%,var(--bg-2) 100%); position:sticky; top:0; z-index:10; backdrop-filter:blur(6px); }
header.top h1 { margin:0; font-size:22px; letter-spacing:-0.02em; }
header.top .sub { color:var(--muted); margin-top:4px; font-size:12px; }
.toolbar { display:flex; gap:10px; margin-top:14px; flex-wrap:wrap; align-items:center; }
.toolbar input, .toolbar select { background:var(--bg-3); border:1px solid var(--border); color:var(--fg); padding:7px 12px; border-radius:8px; font-size:13px; font-family:inherit; }
.toolbar input { min-width:240px; }
.toolbar select { cursor:pointer; }
.toolbar .clear { color:var(--muted); cursor:pointer; padding:7px 12px; border:1px solid var(--border); border-radius:8px; font-size:12px; background:var(--bg-3); }
.toolbar .clear:hover { color:var(--accent); border-color:var(--accent); }
.stats { padding:12px 32px; background:var(--bg-2); border-bottom:1px solid var(--border); color:var(--muted); font-size:12px; }
.stats strong { color:var(--fg); }
.grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(280px,1fr)); gap:16px; padding:24px 32px; }
.card { margin:0; background:var(--bg-2); border:1px solid var(--border); border-radius:12px; overflow:hidden; transition:border-color 0.2s,transform 0.2s; }
.card:hover { border-color:var(--accent); transform:translateY(-2px); }
.card a { display:block; }
.card img { width:100%; aspect-ratio:16/10; object-fit:contain; background:#000; display:block; }
.card figcaption { padding:10px 12px; font-size:11px; }
.row1 { display:flex; justify-content:space-between; align-items:center; margin-bottom:6px; }
.best { padding:2px 8px; border-radius:6px; font-size:10px; font-weight:700; text-transform:uppercase; letter-spacing:0.04em; }
.best-cover { background:rgba(16,185,129,0.15); color:var(--emerald); }
.best-inline { background:rgba(168,85,247,0.15); color:var(--accent); }
.best-icon { background:rgba(245,158,11,0.15); color:var(--amber); }
.best-skip { background:rgba(244,63,94,0.10); color:var(--rose); opacity:0.7; }
.best-none { background:var(--bg-3); color:var(--muted); }
.score { color:var(--muted); font-weight:600; font-size:11px; }
.alt { color:var(--fg); font-size:12px; font-weight:600; margin:4px 0 6px; line-height:1.3; }
.tags { display:flex; flex-wrap:wrap; gap:4px; margin:6px 0; }
.tag { padding:2px 7px; border-radius:4px; font-size:10px; font-weight:600; }
.tag-module { background:rgba(168,85,247,0.15); color:var(--accent); }
.tag-feature { background:rgba(16,185,129,0.15); color:var(--emerald); }
.tag-kind { background:rgba(245,158,11,0.12); color:var(--amber); }
.tag-format { background:rgba(255,255,255,0.06); color:var(--muted); }
.meta { color:var(--muted); margin-top:6px; font-size:10px; }
.meta a { color:var(--muted); }
.meta a:hover { color:var(--accent); }
.card.hidden { display:none; }
.empty { padding:60px; text-align:center; color:var(--muted); display:none; }
.empty.show { display:block; }
"""

    js = """
const q = document.getElementById('q');
const fModule = document.getElementById('f-module');
const fFeature = document.getElementById('f-feature');
const fBest = document.getElementById('f-best');
const fKind = document.getElementById('f-kind');
const fFormat = document.getElementById('f-format');
const clearBtn = document.getElementById('clear');
const statsEl = document.getElementById('stats-visible');
const empty = document.getElementById('empty');

function apply() {
  const text = (q.value || '').toLowerCase().trim();
  const fmod = fModule.value;
  const ffeat = fFeature.value;
  const fbest = fBest.value;
  const fkind = fKind.value;
  const ffmt = fFormat.value;
  let visible = 0;
  document.querySelectorAll('.card').forEach(c => {
    let ok = true;
    if (fmod && c.dataset.module !== fmod) ok = false;
    if (ok && ffeat && c.dataset.feature !== ffeat) ok = false;
    if (ok && fbest && c.dataset.best !== fbest) ok = false;
    if (ok && fkind && c.dataset.kind !== fkind) ok = false;
    if (ok && ffmt && c.dataset.format !== ffmt) ok = false;
    if (ok && text && !c.dataset.text.includes(text)) ok = false;
    c.classList.toggle('hidden', !ok);
    if (ok) visible++;
  });
  statsEl.textContent = visible;
  empty.classList.toggle('show', visible === 0);
}
[q, fModule, fFeature, fBest, fKind, fFormat].forEach(el => el.addEventListener('input', apply));
clearBtn.addEventListener('click', () => {
  q.value = ''; fModule.value = ''; fFeature.value = '';
  fBest.value = ''; fKind.value = ''; fFormat.value = '';
  apply();
});
"""

    def opts(values, label):
        items = '\n'.join(f'<option value="{html.escape(v)}">{html.escape(v)}</option>' for v in values)
        return f'<select id="f-{label}"><option value="">{label} (todos)</option>{items}</select>'

    html_doc = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Catálogo Odoo screenshots · filtros facetados</title>
<style>{css}</style>
</head>
<body>
<header class="top">
  <h1>Catálogo Odoo screenshots · Nextdoo · Partner Odoo Enterprise</h1>
  <div class="sub">{len(catalog)} imágenes clasificadas por módulo, feature, formato y uso óptimo · CDN jsDelivr · actualizado {datetime.now().strftime('%Y-%m-%d %H:%M')}</div>
  <div class="toolbar">
    <input id="q" type="search" placeholder="Texto libre (path, tag, descripción)…"/>
    {opts(modules, "module")}
    {opts(features, "feature")}
    {opts(['cover','inline','icon','skip'], "best")}
    {opts(kinds, "kind")}
    {opts(formats, "format")}
    <button id="clear" class="clear" type="button">Limpiar</button>
  </div>
</header>
<div class="stats">Visible: <strong id="stats-visible">{len(catalog)}</strong> · Total <strong>{len(catalog)}</strong> · CDN base <code>cdn.jsdelivr.net/gh/supportboo/boomatik-assets/odoo-canon/</code></div>
<div class="grid">{''.join(cards_html)}</div>
<div class="empty" id="empty">Sin resultados con esos filtros.</div>
<script>{js}</script>
</body>
</html>"""

    OUTPUT.write_text(html_doc, encoding="utf-8")
    print(f"OK · INDEX.html v2 escrito en {OUTPUT}")
    print(f"  · Entries: {len(catalog)}")
    print(f"  · Modules en dropdown: {len(modules)}")
    print(f"  · Features en dropdown: {len(features)}")
    print(f"  · Tamaño: {OUTPUT.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
