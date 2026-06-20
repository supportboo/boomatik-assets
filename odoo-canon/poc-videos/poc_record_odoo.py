"""POC vídeo demo Odoo · Playwright graba + Edge TTS narra + ffmpeg compone.

Demo: navega por el catálogo Odoo Apps (es la marketing page pública,
no requiere login) mientras la voz en off explica cada paso.

Output: poc_demo_odoo.mp4 (HD 1280×720, voz ES, subtítulos quemados)
"""
from __future__ import annotations

import asyncio
import json
import subprocess
from pathlib import Path

from playwright.async_api import async_playwright
import edge_tts

OUT = Path(__file__).resolve().parent
VOICE = "es-ES-AlvaroNeural"  # voz masculina ES España
UA_REAL = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"

# POC: navegamos el frontend de Nextdoo (nuestra instancia Odoo 19 viva).
# Mostramos el blog optimizado + alguna landing. Sin login. Demuestra el stack.
SCRIPT = [
    {
        "say": "Esta es Nextdoo, partner Odoo Enterprise. Te enseño un recorrido por el sitio.",
        "url": "https://www.nextdoo.cloud/",
        "wait": 4500,
    },
    {
        "say": "La página principal explica los servicios sobre Odoo para pymes españolas.",
        "scroll_to": 800,
        "wait": 4000,
    },
    {
        "say": "El blog tiene más de sesenta artículos optimizados sobre Odoo: contabilidad, TPV, ecommerce y casos prácticos.",
        "goto": "https://www.nextdoo.cloud/blog",
        "wait": 5000,
    },
    {
        "say": "Cada post lleva pantallazos reales de Odoo y disclaimer legal de JLM Business Solutions.",
        "goto": "https://www.nextdoo.cloud/blog/nextdoo-blog-3/zoho-vs-odoo-en-tarragona-cuando-conviene-cada-uno-y-por-que-odoo-gana-en-pyme-integral-262",
        "wait": 4500,
    },
    {
        "say": "Bajamos para ver la comparativa y el resumen ejecutivo.",
        "scroll_to": 900,
        "wait": 4500,
    },
    {
        "say": "Y cerramos el recorrido con el contacto comercial para pedir presupuesto.",
        "goto": "https://www.nextdoo.cloud/contactus",
        "wait": 4000,
    },
]


async def synth_voice(text: str, out_mp3: Path) -> float:
    """Genera audio MP3 + devuelve duración en segundos."""
    com = edge_tts.Communicate(text, VOICE, rate="+0%")
    await com.save(str(out_mp3))
    # duración con ffprobe
    r = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(out_mp3)],
        capture_output=True, text=True,
    )
    return float(r.stdout.strip() or 0)


def srt_from_steps(steps: list[dict]) -> str:
    """Construye SRT a partir de start/end de cada paso."""
    def fmt(t: float) -> str:
        h = int(t // 3600); m = int((t % 3600) // 60); s = int(t % 60); ms = int((t - int(t)) * 1000)
        return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"
    lines = []
    for i, s in enumerate(steps, 1):
        lines.append(str(i))
        lines.append(f"{fmt(s['start_s'])} --> {fmt(s['end_s'])}")
        lines.append(s["say"])
        lines.append("")
    return "\n".join(lines)


async def record_video(steps: list[dict]) -> Path:
    """Graba la sesión Playwright en webm y devuelve la ruta."""
    OUT.mkdir(exist_ok=True)
    video_dir = OUT / "video_raw"
    video_dir.mkdir(exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        ctx = await browser.new_context(
            viewport={"width": 1280, "height": 720},
            record_video_dir=str(video_dir),
            record_video_size={"width": 1280, "height": 720},
            user_agent=UA_REAL,
            locale="es-ES",
        )
        page = await ctx.new_page()
        for s in steps:
            if "url" in s:
                await page.goto(s["url"], wait_until="domcontentloaded", timeout=45000)
            elif "goto" in s:
                await page.goto(s["goto"], wait_until="domcontentloaded", timeout=45000)
            if "scroll_to" in s:
                await page.evaluate(f"window.scrollTo({{top: {s['scroll_to']}, behavior:'smooth'}})")
            await page.wait_for_timeout(s.get("wait", 3000))
        await ctx.close()
        await browser.close()

    # Encontrar el .webm que Playwright generó
    webms = sorted(video_dir.glob("*.webm"))
    if not webms:
        raise RuntimeError("Playwright no generó video.")
    return webms[-1]


async def main():
    print("[1/4] Generando narración Edge TTS por paso…")
    audio_dir = OUT / "audio_raw"; audio_dir.mkdir(exist_ok=True)
    cum = 0.0
    for i, s in enumerate(SCRIPT):
        mp3 = audio_dir / f"step_{i:02d}.mp3"
        dur = await synth_voice(s["say"], mp3)
        s["audio"] = mp3
        s["audio_dur"] = dur
        s["start_s"] = cum
        # El paso dura: max(audio, wait_durante_grabacion)
        nav_dur = s.get("wait", 3000) / 1000
        s["end_s"] = cum + max(dur, nav_dur)
        cum = s["end_s"]
        print(f"  · paso {i+1}: audio {dur:.1f}s · nav {nav_dur:.1f}s")
    total_dur = cum

    print(f"[2/4] Grabando navegación con Playwright (~{total_dur:.0f}s)…")
    # Ajustar waits de navegación para que coincidan con duración audio
    for i, s in enumerate(SCRIPT):
        # Si el audio es más largo que el wait, ampliamos el wait
        needed_ms = int(max(s["audio_dur"], s.get("wait", 3000) / 1000) * 1000)
        s["wait"] = needed_ms
    webm = await record_video(SCRIPT)
    print(f"  · webm: {webm}")

    print("[3/4] Concatenando audio (con offsets) y mezclando con vídeo…")
    # Crear lista de concatenación de audios con silencios entre ellos si hace falta.
    # Aquí: cada paso ya tiene audio_dur ≈ wait, así que concatenamos secuencialmente.
    concat_file = OUT / "audio_concat.txt"
    with open(concat_file, "w", encoding="utf-8") as f:
        for s in SCRIPT:
            f.write(f"file '{s['audio'].as_posix()}'\n")
    audio_mix = OUT / "audio_mix.mp3"
    subprocess.run(
        ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_file),
         "-c", "copy", str(audio_mix)],
        check=True, capture_output=True,
    )

    # Convertir webm a mp4 + añadir audio + (subtítulos quemados en pasada 2)
    srt_path = OUT / "subs.srt"
    srt_path.write_text(srt_from_steps(SCRIPT), encoding="utf-8")

    raw_mp4 = OUT / "poc_demo_odoo_raw.mp4"
    subprocess.run(
        ["ffmpeg", "-y", "-i", str(webm), "-i", str(audio_mix),
         "-map", "0:v:0", "-map", "1:a:0",
         "-c:v", "libx264", "-preset", "fast", "-crf", "22",
         "-c:a", "aac", "-b:a", "128k",
         "-shortest", str(raw_mp4)],
        check=True, capture_output=True,
    )

    final = OUT / "poc_demo_odoo.mp4"
    # Quemamos subtítulos. ffmpeg subtitles= necesita ruta con forward slash y escape
    srt_for_ffmpeg = str(srt_path).replace("\\", "/").replace(":", "\\:")
    sub_filter = (
        f"subtitles='{srt_for_ffmpeg}'"
        ":force_style='Fontname=Inter,Fontsize=22,PrimaryColour=&HFFFFFF&,"
        "OutlineColour=&H000000&,BorderStyle=3,Outline=2,Shadow=0,"
        "MarginV=40,Alignment=2,Bold=1'"
    )
    print("[4/4] Quemando subtítulos…")
    subprocess.run(
        ["ffmpeg", "-y", "-i", str(raw_mp4),
         "-vf", sub_filter,
         "-c:v", "libx264", "-preset", "fast", "-crf", "22",
         "-c:a", "copy", str(final)],
        check=True, capture_output=True,
    )
    print(f"\nOK · vídeo final: {final}")
    size_kb = final.stat().st_size // 1024
    print(f"Tamaño: {size_kb} KB · Duración total: {total_dur:.1f}s")


if __name__ == "__main__":
    asyncio.run(main())
