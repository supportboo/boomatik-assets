"""Cut a portrait out of a near-white background: rembg (u2net_human_seg) for the matte, then white de-fringing so no light
halo shows on the dark brand background. Writes <out>.png (RGBA, same size) and <out>_check.jpg (cutout on #0b0918).
Usage: python -I recorte.py <photo> <out_without_ext>"""
import sys
import numpy as np
from PIL import Image, ImageFilter


def cut(src, out):
    from rembg import new_session, remove
    im = Image.open(src).convert('RGB')
    mask = remove(im, session=new_session('u2net_human_seg'), only_mask=True)      # L, soft matte
    a = np.asarray(mask.filter(ImageFilter.GaussianBlur(1.2)), np.float32) / 255
    a = np.clip((a - .04) / .92, 0, 1)                                              # drop faint haze, keep edge softness
    c = np.asarray(im, np.float32)
    bg = np.median(c[a < .01], axis=0) if (a < .01).any() else np.array([248, 248, 250], np.float32)
    # C = a*F + (1-a)*BG  ->  F = (C - (1-a)*BG) / a : removes the white fringe in hair and along the shirt
    f = (c - (1 - a[..., None]) * bg) / np.maximum(a[..., None], .08)
    f = np.where(a[..., None] > .97, c, np.clip(f, 0, 255))
    rgba = np.dstack([f, a * 255]).astype(np.uint8)
    Image.fromarray(rgba, 'RGBA').save(out + '.png', optimize=True)
    chk = Image.new('RGB', im.size, (11, 9, 24))
    chk.paste(Image.fromarray(rgba, 'RGBA'), mask=Image.fromarray((a * 255).astype(np.uint8)))
    chk.resize((im.width // 2, im.height // 2), Image.LANCZOS).save(out + '_check.jpg', quality=85)
    print('bg', bg.round(), 'wrote', out + '.png')


if __name__ == '__main__':
    cut(sys.argv[1], sys.argv[2])
