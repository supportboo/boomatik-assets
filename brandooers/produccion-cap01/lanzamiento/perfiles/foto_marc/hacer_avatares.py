"""Download the upscaled profile photo and cut the avatar of each network (plus the /enlaces/ photo)."""
import pathlib, urllib.request
from PIL import Image

HERE = pathlib.Path(__file__).parent
SRC = 'https://d8j0ntlcm91z4.cloudfront.net/user_3EK1A7UZAYUqpkNAaZJW4e4EYJI/hf_20261029_143112_4056d82b-6095-4998-97fe-14cc6ebd7171.png'
ENLACES = HERE.parents[3] / 'brandooers_public' / 'enlaces' / 'marc-herrero.webp'

big = HERE / 'marc_2k.png'
if not big.exists():
    urllib.request.urlretrieve(SRC, big)
im = Image.open(big).convert('RGB')
print('source', im.size)
for name, s in [('youtube', 800), ('instagram', 1080), ('tiktok', 720), ('facebook', 720), ('linkedin', 400), ('google', 720)]:
    im.resize((s, s), Image.LANCZOS).save(HERE / f'avatar_{name}_{s}.jpg', quality=92)
im.resize((320, 320), Image.LANCZOS).save(ENLACES, quality=88)
im.resize((600, 600), Image.LANCZOS).save(HERE / 'preview.jpg', quality=90)
print('ok', ENLACES)
