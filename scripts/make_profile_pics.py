from PIL import Image, ImageDraw, ImageFilter
import numpy as np
import os

BG      = (11, 12, 16)   # --bg
BG2     = (16, 18, 24)   # --bg-2
ACCENT  = (255, 84, 54)
ACCENT2 = (255, 154, 60)

BR = "branding/logo png-uri culori site/"
OUT_DIR = "branding/poze de profil/"
os.makedirs(OUT_DIR, exist_ok=True)

icon_only = Image.open(BR + "icon culori site.png").convert("RGBA")
word_only = Image.open(BR + "nume vizuroiu culori site.png").convert("RGBA")

def radial_glow(size, color, radius_frac=0.78, alpha=110, blur_frac=0.09):
    g = Image.new("RGBA", size, (0, 0, 0, 0))
    gd = ImageDraw.Draw(g)
    cx, cy = size[0] // 2, size[1] // 2
    r = int(size[0] * radius_frac / 2)
    # offset slightly top-right, like the site's hero::before glow
    off = int(size[0] * 0.06)
    gd.ellipse([cx - r + off, cy - r - off, cx + r + off, cy + r - off], fill=color + (alpha,))
    return g.filter(ImageFilter.GaussianBlur(int(size[0] * blur_frac)))

def base_bg(size):
    """Site-style background: solid --bg + soft accent radial glow, like hero::before."""
    canvas = Image.new("RGBA", (size, size), BG + (255,))
    glow = radial_glow((size, size), ACCENT, radius_frac=0.85, alpha=100, blur_frac=0.10)
    canvas = Image.alpha_composite(canvas, glow)
    glow2 = radial_glow((size, size), ACCENT2, radius_frac=0.5, alpha=60, blur_frac=0.14)
    canvas = Image.alpha_composite(canvas, glow2)
    return canvas

def paste_centered(canvas, art, target_w):
    ar = art.resize((target_w, int(target_w * art.height / art.width)), Image.LANCZOS)
    x = (canvas.width - ar.width) // 2
    y = (canvas.height - ar.height) // 2
    canvas.alpha_composite(ar, (x, y))
    return canvas

def make_icon_profile(size, out_name):
    canvas = base_bg(size)
    canvas = paste_centered(canvas, icon_only, int(size * 0.64))
    canvas.convert("RGB").save(OUT_DIR + out_name, "PNG")
    print("saved", out_name)

def make_wordmark_profile(size, out_name):
    canvas = base_bg(size)
    canvas = paste_centered(canvas, word_only, int(size * 0.72))
    canvas.convert("RGB").save(OUT_DIR + out_name, "PNG")
    print("saved", out_name)

def make_combo_profile(size, out_name):
    canvas = base_bg(size)
    # stack icon above wordmark, sized to survive a circular crop
    icon_w = int(size * 0.46)
    ir = icon_only.resize((icon_w, int(icon_w * icon_only.height / icon_only.width)), Image.LANCZOS)
    word_w = int(size * 0.56)
    wr = word_only.resize((word_w, int(word_w * word_only.height / word_only.width)), Image.LANCZOS)

    gap = int(size * 0.045)
    block_h = ir.height + gap + wr.height
    top = (size - block_h) // 2

    canvas.alpha_composite(ir, ((size - ir.width) // 2, top))
    canvas.alpha_composite(wr, ((size - wr.width) // 2, top + ir.height + gap))

    canvas.convert("RGB").save(OUT_DIR + out_name, "PNG")
    print("saved", out_name)

SIZES = [1000, 500, 200]

for s in SIZES:
    make_icon_profile(s, f"poza-profil-logo-{s}x{s}.png")
for s in SIZES:
    make_wordmark_profile(s, f"poza-profil-nume-{s}x{s}.png")
for s in SIZES:
    make_combo_profile(s, f"poza-profil-logo-si-nume-{s}x{s}.png")
