"""MANIFIESTO.json + contact sheet for micro/rehecho/. Texts come from the validated bodies in programado.json (fieldsSent),
fixed only where the 29-oct rules require it. Touches no network."""
import json, os, re
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
LZ = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(LZ, "micro", "rehecho")
LOG = json.load(open(os.path.join(LZ, "micro", "programado.json"), encoding="utf-8"))["pieces"]
P = {x["id"]: x for x in json.load(open(os.path.join(LZ, "primeras", "primeras.json"), encoding="utf-8"))["piezas"]}
AI_IMAGE = "\n\nLa imagen es mi avatar creado con IA."
png = lambda pid, name: os.path.join(OUT, f"{pid}_{name}.png")
fs = lambda pid: LOG[pid]["fieldsSent"]

c1_alt = list(P["C01-IG-C1"]["alt"])
c1_alt[0] = ("Portada sobre fondo cian: ¿Dónde se rompe? Encontrar, entender, comprar y pagar, con pagar torcido. "
             "4 pruebas de 10 minutos. Abajo, la mascota de los ojos de SkillUp Brandooers mira con una lupa.")
tt = fs("C01-TT-P1")["tiktokSettings"]["description"]
assert tt.endswith(AI_IMAGE)

pieces = [
    dict(id="C01-FB-P1", platform="facebook", action="create now", text=fs("C01-FB-P1")["content"], isAiGenerated=None,
         images=[], alt=[], note="Link post, no media; the preview is the YouTube thumbnail (mascot + small badge). "
                                 "The «Vídeo con mi avatar creado con IA.» line stays: it describes the linked video."),
    dict(id="C01-LI-P1", platform="linkedin", action="create now", text=fs("C01-LI-P1")["content"], isAiGenerated=None,
         images=[], alt=[], firstComment=fs("C01-LI-P1")["platforms"][0]["platformSpecificData"]["firstComment"],
         note="Text post, no media; AI line describes the linked video. Unchanged."),
    dict(id="C01-IG-H3", platform="instagram (story)", action="create now", text="", isAiGenerated=False,
         images=[png("C01-IG-H3", "historia_h3_mas_visitas_no_1080x1920")],
         alt=["Fondo oscuro. Texto: ¿Más visitas? No. Arregla el paso que se rompe. La mascota de los ojos de SkillUp "
              "Brandooers mira con una lupa. Logo de SkillUp Brandooers."],
         note="Marc's photo replaced by the mascot; logo renamed; isAiGenerated true -> false."),
    dict(id="C01-IG-H5", platform="instagram (story)", action="create now", text="", isAiGenerated=False,
         images=[png("C01-IG-H5", "historia_h5_pagar_de_15_a_3_1080x1920")], alt=P["C01-IG-H5"]["alt"],
         note="No face before; only the logo order changed to «SkillUp Brandooers»."),
    dict(id="C01-IG-P1", platform="instagram (feed)", action="create now", text=fs("C01-IG-P1")["content"], isAiGenerated=False,
         images=[png("C01-IG-P1", "ya_esta_capitulo1_1080x1350")],
         alt=["La mascota de los ojos de SkillUp Brandooers, con una lupa, sobre fondo oscuro. Texto: Ya está: capítulo 1. "
              "Tu tienda vende más, en YouTube. Logo de SkillUp Brandooers."],
         note="Marc's photo replaced by the mascot; logo renamed; alt no longer says «Marc mira a cámara»; isAiGenerated true -> false."),
    dict(id="C01-TT-P1", platform="tiktok (photo)", action="create now", text=fs("C01-TT-P1")["content"],
         tiktokDescription=tt[: -len(AI_IMAGE)], isAiGenerated=False,
         images=[png("C01-TT-P1", "ya_esta_capitulo1_1080x1920")], alt=[],
         note="Marc's photo replaced by the mascot; «La imagen es mi avatar creado con IA.» removed from the description."),
    dict(id="C01-IG-C1", platform="instagram (feed carousel)", action=f"replace media of scheduled post {LOG['C01-IG-C1']['postId']}",
         scheduledFor_utc=LOG["C01-IG-C1"]["scheduledFor_utc"], text=fs("C01-IG-C1")["content"], isAiGenerated=False,
         images=[png("C01-IG-C1", f"carrusel_4_pasos_{i}de8_1080x1350") for i in range(1, 9)], alt=c1_alt,
         note="Slide 1: Marc's photo -> mascot. All 8 slides: logo «Brandooers SkillUp» -> «SkillUp Brandooers»; slide 8 "
              "line «YouTube: Brandooers SkillUp.» -> «YouTube: SkillUp Brandooers.». Post scheduled with isAiGenerated true -> set false."),
    dict(id="C01-IG-H4", platform="instagram (story)", action=f"replace media of scheduled post {LOG['C01-IG-H4']['postId']}",
         scheduledFor_utc=LOG["C01-IG-H4"]["scheduledFor_utc"], text="", isAiGenerated=False,
         images=[png("C01-IG-H4", "historia_h4_donde_esta_el_salto_1080x1920")], alt=P["C01-IG-H4"]["alt"],
         note="No face before; only the logo order changed."),
]

# rule checks on everything that will be published
for p in pieces:
    blob = json.dumps({k: v for k, v in p.items() if k != "note"}, ensure_ascii=False)  # what gets published
    assert "Brandooers SkillUp" not in blob and "€" not in blob, p["id"]
    assert not re.search("[\U0001F300-\U0001FAFF☀-➿]", blob), p["id"]
    for f in p["images"]:
        assert os.path.isfile(f), f
    if p["isAiGenerated"] is False:
        assert "avatar creado con IA" not in (p["text"] + p.get("tiktokDescription", "")), p["id"]

json.dump({"generado": "2026-10-30", "regla": "memory feedback_marc_no_graba_heygen_educador (29-oct)", "piezas": pieces},
          open(os.path.join(OUT, "MANIFIESTO.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# contact sheet: every final image at 270 px wide, labelled
tiles = [(p["id"] + (f" {i + 1}/{len(p['images'])}" if len(p["images"]) > 1 else ""), f)
         for p in pieces for i, f in enumerate(p["images"])]
TW, TH, COLS = 270, 480 + 28, 7
sheet = Image.new("RGB", (TW * COLS + 8 * (COLS + 1), (TH + 8) * -(-len(tiles) // COLS) + 8), (24, 22, 40))
d = ImageDraw.Draw(sheet)
for k, (label, f) in enumerate(tiles):
    im = Image.open(f).convert("RGB")
    im = im.resize((TW, round(im.height * TW / im.width)), Image.LANCZOS)
    x, y = 8 + (k % COLS) * (TW + 8), 8 + (k // COLS) * (TH + 8)
    sheet.paste(im, (x, y)); d.text((x + 4, y + 482), label, fill=(255, 255, 255))
sheet.save(os.path.join(OUT, "hoja_contactos.jpg"), quality=88)
print("ok", len(pieces), "pieces,", len(tiles), "images")
