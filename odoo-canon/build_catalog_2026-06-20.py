"""Construye CATALOG.json con clasificación semántica de cada imagen de la
biblioteca Odoo. Determinístico, sin LLM, coste 0€.

Lee:
- screenshots/INVENTORY.json (391 raw-images embedded de odoocdn.com)
- screenshots/page-shots/*.png (40 capturas full-page de odoo.com)
- scrape-modules/<module>/*.webp (1300 imágenes scrape modular)

Produce:
- CATALOG.json con un entry por imagen con campos:
    path           ruta relativa desde odoo-canon/
    cdn            URL CDN público
    module         crm/point-of-sale/inventory/.../null
    feature        kanban/dashboard/hero/bill/payment-terminal/mobile/.../null
    kind           ui/hero/persona/avatar-partner/flag/logo-store/icon/partner-logo
    format         landscape/portrait/square
    width          int
    height         int
    aspect_ratio   float
    best_for       ["cover", "inline", "icon", "skip"]
    source_url     URL original
    alt            sugerencia de alt-text en ES
    score          int 0-100 idoneidad para composición de blog
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from urllib.parse import unquote

from PIL import Image

CANON = Path(__file__).resolve().parent
SHOTS = CANON / "screenshots"
PAGE_SHOTS = SHOTS / "page-shots"
RAW_IMAGES = SHOTS / "raw-images"
SCRAPE = CANON / "scrape-modules"
INVENTORY = SHOTS / "INVENTORY.json"
OUTPUT = CANON / "CATALOG.json"
CDN_BASE = "https://cdn.jsdelivr.net/gh/supportboo/boomatik-assets/odoo-canon"

# ---- Reglas de clasificación por URL fuente -----------------------------------

# Bypass: estas URLs son obvias y se etiquetan sin más
URL_PATTERNS: list[tuple[re.Pattern[str], dict]] = [
    (re.compile(r"/country_flags/"), {"kind": "flag", "best_for": "skip"}),
    (re.compile(r"/snippets/s_wd_persona/"), {"kind": "persona", "best_for": "skip"}),
    (re.compile(r"/snippets/s_wd_testimonials/avatar/"), {"kind": "testimonial-avatar", "best_for": "skip"}),
    (re.compile(r"logo_google_play|logo_app_store"), {"kind": "store-logo", "best_for": "skip"}),
    (re.compile(r"/web/image/res\.lang/"), {"kind": "flag", "best_for": "skip"}),
    (re.compile(r"/web/image/res\.partner/"), {"kind": "partner-logo", "best_for": "skip"}),
    (re.compile(r"/illustration/doodle/"), {"kind": "illustration-doodle", "best_for": "skip"}),
    (re.compile(r"/static/src/img/snippets/.*hero", re.I), {"kind": "hero", "best_for": "cover"}),
    (re.compile(r"/static/src/img/apps/(?P<module>[a-z\-]+)/hero_image", re.I), {"kind": "hero-app", "best_for": "cover"}),
]

# Tags por palabra clave en el slug del filename original
SLUG_TAG_RULES: list[tuple[str, dict]] = [
    # Features universales
    ("hero", {"kind": "hero", "best_for": "cover"}),
    ("interface", {"feature": "ui-main", "best_for": "inline"}),
    ("dashboard", {"feature": "dashboard", "best_for": "cover"}),
    ("kanban", {"feature": "kanban", "best_for": "inline"}),
    ("calendar", {"feature": "calendar", "best_for": "inline"}),
    ("gantt", {"feature": "gantt", "best_for": "inline"}),
    ("reporting", {"feature": "reporting", "best_for": "inline"}),
    ("report", {"feature": "reporting", "best_for": "inline"}),
    ("mobile", {"format": "portrait", "feature": "mobile-app", "best_for": "inline"}),
    ("device", {"feature": "device", "best_for": "inline"}),
    # POS / Retail
    ("pos", {"module": "point-of-sale"}),
    ("payment_terminal", {"feature": "payment-terminal", "best_for": "inline"}),
    ("payment-terminal", {"feature": "payment-terminal", "best_for": "inline"}),
    ("payments", {"feature": "payments", "best_for": "inline"}),
    ("self_service", {"feature": "self-service-kiosk", "best_for": "inline"}),
    ("scanner", {"feature": "scanner", "best_for": "inline"}),
    ("shop", {"module": "point-of-sale", "feature": "shop"}),
    # Invoicing / Accounting
    ("bill", {"module": "invoicing", "feature": "bill"}),
    ("invoice", {"module": "invoicing", "feature": "invoice"}),
    ("invoicing", {"module": "invoicing"}),
    ("accounting", {"module": "accounting"}),
    ("vendor_bill", {"module": "invoicing", "feature": "vendor-bill"}),
    ("verifactu", {"module": "invoicing", "feature": "verifactu"}),
    ("ticketbai", {"module": "invoicing", "feature": "ticketbai"}),
    ("ai-powered", {"feature": "ai", "best_for": "cover"}),
    # CRM / Sales
    ("crm", {"module": "crm"}),
    ("quotation", {"module": "sales", "feature": "quotation"}),
    ("quote", {"module": "sales", "feature": "quotation"}),
    ("lead", {"module": "crm", "feature": "lead"}),
    ("pipeline", {"module": "crm", "feature": "pipeline"}),
    ("communications", {"feature": "communications"}),
    # Inventory / Logistics
    ("inventory", {"module": "inventory"}),
    ("warehouse", {"module": "inventory", "feature": "warehouse"}),
    ("vendor", {"feature": "vendor"}),
    ("automate", {"feature": "automation", "best_for": "inline"}),
    # eCommerce / Website
    ("ecommerce", {"module": "ecommerce"}),
    ("product", {"feature": "product"}),
    ("cart", {"module": "ecommerce", "feature": "cart"}),
    ("storefront", {"module": "ecommerce", "feature": "storefront"}),
    ("checkout", {"module": "ecommerce", "feature": "checkout"}),
    # Sign / Documents
    ("sign", {"module": "sign", "feature": "signature"}),
    ("documents", {"module": "documents"}),
    # Manufacturing / Project
    ("manufacturing", {"module": "manufacturing"}),
    ("mrp", {"module": "manufacturing"}),
    ("production", {"module": "manufacturing", "feature": "production"}),
    ("project", {"module": "project"}),
    ("task", {"module": "project", "feature": "task"}),
    # HR / Helpdesk
    ("helpdesk", {"module": "helpdesk"}),
    ("ticket", {"module": "helpdesk", "feature": "ticket"}),
    ("payroll", {"module": "human-resources", "feature": "payroll"}),
    ("recruitment", {"module": "recruitment"}),
    ("candidate", {"module": "recruitment", "feature": "candidate"}),
    ("employee", {"module": "human-resources", "feature": "employee"}),
    # Marketing / Comms
    ("marketing", {"module": "marketing-automation"}),
    ("campaign", {"feature": "campaign"}),
    ("email", {"module": "email-marketing"}),
    ("newsletter", {"module": "email-marketing", "feature": "newsletter"}),
    # Iconos
    ("icon", {"kind": "icon", "best_for": "icon"}),
    # Speed / feature illustrations
    ("speed", {"kind": "illustration", "best_for": "skip"}),
]

# Mapa nombre módulo a feature ES (para alt-text)
MODULE_ES: dict[str, str] = {
    "crm": "CRM",
    "sales": "Ventas",
    "subscriptions": "Suscripciones",
    "accounting": "Contabilidad",
    "invoicing": "Facturación",
    "expenses": "Gastos",
    "inventory": "Inventario",
    "purchase": "Compras",
    "manufacturing": "Fabricación",
    "plm": "Gestión del ciclo de vida del producto",
    "quality": "Calidad",
    "maintenance": "Mantenimiento",
    "point-of-sale": "Punto de venta TPV",
    "ecommerce": "eCommerce",
    "website": "Sitio web",
    "marketing-automation": "Automatización de marketing",
    "email-marketing": "Email marketing",
    "social-marketing": "Redes sociales",
    "project": "Proyectos",
    "helpdesk": "Helpdesk",
    "field-service": "Servicio en campo",
    "recruitment": "Selección de personal",
    "time-off": "Ausencias",
    "fleet": "Flota",
    "studio": "Studio",
    "documents": "Documentos",
    "spreadsheet": "Hoja de cálculo",
    "sign": "Firma electrónica",
    "discuss": "Mensajería interna",
    "rental": "Alquileres",
    "events": "Eventos",
    "elearning": "Formación online",
    "survey": "Encuestas",
    "live-chat": "Chat en directo",
    "human-resources": "Recursos humanos",
}


def slug_words(url_or_name: str) -> list[str]:
    """Extrae palabras significativas del slug del nombre/URL."""
    if "://" in url_or_name:
        slug = url_or_name.split("/")[-1].split("?")[0]
    else:
        slug = url_or_name
    slug = unquote(slug).lower()
    base = slug.rsplit(".", 1)[0]
    base = re.sub(r"[_\-\.\s]+", "-", base)
    return [w for w in base.split("-") if w and not w.isdigit() and len(w) > 1]


def detect_module_from_url(url: str) -> str | None:
    m = re.search(r"/static/src/img/apps/([a-z\-]+)/", url, re.I)
    if m:
        return m.group(1).lower()
    return None


def classify(path: Path, source_url: str = "", description: str = "") -> dict:
    tags: dict = {
        "module": None,
        "feature": None,
        "kind": "ui",
        "format": None,
        "best_for": None,
        "tags": [],
    }
    # Reglas por URL pattern
    for rx, hint in URL_PATTERNS:
        if rx.search(source_url):
            tags.update({k: v for k, v in hint.items() if v is not None})
            m = rx.search(source_url)
            if m and "module" in (m.groupdict() or {}):
                tags["module"] = m.group("module")
            break

    # Módulo desde URL path
    if not tags.get("module"):
        m = detect_module_from_url(source_url)
        if m:
            tags["module"] = m
    # Módulo desde nombre de carpeta (scrape-modules/<module>/)
    if not tags.get("module"):
        try:
            rel = path.resolve().relative_to(SCRAPE.resolve())
            tags["module"] = rel.parts[0]
        except (ValueError, OSError):
            pass

    # Tags y feature desde slug
    words = slug_words(source_url or path.name)
    for kw, hint in SLUG_TAG_RULES:
        if any(kw == w or kw in w for w in words):
            for k, v in hint.items():
                if k == "module" and tags.get("module"):
                    continue  # ya teníamos módulo más fiable
                tags[k] = v
            tags["tags"].append(kw)
            # No break: acumulamos múltiples tags

    # Aspecto y dimensiones
    try:
        with Image.open(path) as im:
            w, h = im.size
    except Exception:
        w, h = 0, 0
    tags["width"] = w
    tags["height"] = h
    tags["aspect_ratio"] = round(w / h, 2) if h > 0 else 0
    if w == 0 or h == 0:
        tags["format"] = None
    elif w / h > 1.4:
        tags["format"] = "landscape"
    elif w / h < 0.75:
        tags["format"] = "portrait"
    else:
        tags["format"] = "square"
    # Override mobile a portrait si el slug indicaba mobile
    if "mobile-app" in (tags.get("feature") or "") and tags.get("format") == "landscape":
        tags["format"] = "portrait"

    # best_for fallback por aspecto/tamaño
    if not tags["best_for"]:
        if max(w, h) < 200:
            tags["best_for"] = "icon"
        elif tags["format"] == "landscape" and w >= 1000:
            tags["best_for"] = "cover"
        elif tags["format"] == "landscape" and w >= 600:
            tags["best_for"] = "inline"
        elif tags["format"] == "portrait" and h >= 600:
            tags["best_for"] = "inline"
        else:
            tags["best_for"] = "skip"

    # Persona / flag / icon: forzar skip
    if tags["kind"] in ("persona", "flag", "store-logo", "testimonial-avatar"):
        tags["best_for"] = "skip"

    # Score 0-100 idoneidad para composición de blog
    score = 0
    if tags["best_for"] == "cover":
        score += 50
    elif tags["best_for"] == "inline":
        score += 40
    elif tags["best_for"] == "icon":
        score += 5
    if tags["module"]:
        score += 15
    if tags["feature"]:
        score += 15
    if tags["kind"] == "hero" or tags["kind"] == "hero-app":
        score += 20
    if tags["kind"] == "ui":
        score += 10
    if tags["format"] == "landscape" and tags.get("width", 0) > 1000:
        score += 10
    if tags["best_for"] == "skip":
        score = max(0, score - 30)
    tags["score"] = min(100, score)

    # Alt-text ES sugerido
    module_es = MODULE_ES.get(tags["module"] or "", tags["module"] or "Odoo")
    if tags.get("feature"):
        feat = tags["feature"].replace("-", " ")
        alt = f"{module_es} en Odoo · {feat}"
    elif tags["kind"] == "hero":
        alt = f"{module_es} en Odoo · hero"
    elif tags["kind"] == "ui":
        alt = f"Interfaz de {module_es} en Odoo"
    else:
        alt = description or f"Captura de {module_es} en Odoo"
    tags["alt"] = alt
    return tags


def main() -> None:
    inventory = {}
    if INVENTORY.exists():
        inventory = json.load(open(INVENTORY, encoding="utf-8"))
    inv_by_filename: dict[str, dict] = {}
    for k, v in inventory.items():
        if v.get("path"):
            inv_by_filename[Path(v["path"]).name] = v

    catalog: list[dict] = []

    def walk(folder: Path, section: str) -> None:
        if not folder.exists():
            return
        for p in sorted(folder.rglob("*")):
            if not p.is_file():
                continue
            if p.suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg"}:
                continue
            meta = inv_by_filename.get(p.name, {})
            source_url = meta.get("source_url", "")
            description = meta.get("description", "")
            tags = classify(p, source_url, description)
            rel = p.resolve().relative_to(CANON.resolve()).as_posix()
            entry = {
                "section": section,
                "path": rel,
                "cdn": f"{CDN_BASE}/{rel}",
                "size_kb": p.stat().st_size // 1024,
                "source_url": source_url,
                "description": description,
                **tags,
            }
            catalog.append(entry)

    walk(PAGE_SHOTS, "page-shots")
    walk(RAW_IMAGES, "raw-images")
    walk(SCRAPE, "scrape-modules")

    OUTPUT.write_text(
        json.dumps(catalog, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"OK · CATALOG.json escrito en {OUTPUT}")
    print(f"Total entries: {len(catalog)}")

    # Resumen
    from collections import Counter
    by_module = Counter(e.get("module") or "(sin módulo)" for e in catalog)
    by_best = Counter(e.get("best_for") for e in catalog)
    by_feature = Counter(e.get("feature") or "(sin feature)" for e in catalog)
    by_kind = Counter(e.get("kind") for e in catalog)
    print("\n=== Por módulo (top 20) ===")
    for k, c in by_module.most_common(20):
        print(f"  {c:>4} · {k}")
    print("\n=== Por best_for ===")
    for k, c in by_best.most_common():
        print(f"  {c:>4} · {k}")
    print("\n=== Por feature (top 25) ===")
    for k, c in by_feature.most_common(25):
        print(f"  {c:>4} · {k}")
    print("\n=== Por kind ===")
    for k, c in by_kind.most_common():
        print(f"  {c:>4} · {k}")


if __name__ == "__main__":
    main()
