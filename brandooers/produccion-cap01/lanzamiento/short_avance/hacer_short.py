"""YouTube Short teaser: the 9:16 launch image with a slow push-in and the podcast intro cue, 9.5 s, -14 LUFS."""
import pathlib, subprocess

HERE = pathlib.Path(__file__).parent
L01 = HERE.parents[1]
IMG = L01 / 'lanzamiento' / 'primeras' / 'teaser_lunes_capitulo1_1080x1920.png'
AUD = L01 / 'microcontenidos' / 'podcast' / 'identidad' / 'intro_v1.wav'
OUT = HERE / 'short_avance_capitulo1.mp4'
DUR = 9.5
FR = 30
frames = int(DUR * FR)

# push-in from 100 % to 106 % over the whole clip, rendered at 2x to avoid zoompan jitter
vf = (f"scale=2160:3840:flags=lanczos,zoompan=z='1+0.06*on/{frames}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
      f":d={frames}:s=1080x1920:fps={FR},format=yuv420p,fade=t=out:st={DUR - 0.4}:d=0.4")
af = f"atrim=0:{DUR},afade=t=out:st={DUR - 0.6}:d=0.6,loudnorm=I=-14:TP=-1.5:LRA=7"
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-loop', '1', '-i', str(IMG), '-i', str(AUD),
                '-vf', vf, '-af', af, '-t', str(DUR), '-c:v', 'libx264', '-crf', '16', '-preset', 'slow',
                '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709',
                '-c:a', 'aac', '-b:a', '256k', '-ar', '48000', '-movflags', '+faststart', str(OUT)], check=True)
r = subprocess.run(['ffmpeg', '-hide_banner', '-i', str(OUT), '-af', 'ebur128=peak=true', '-f', 'null', '-'],
                   capture_output=True, text=True)
tail = [l.strip() for l in r.stderr.splitlines() if l.strip().startswith(('I:', 'Peak:'))]
print(OUT.name, OUT.stat().st_size, tail[-2:])
