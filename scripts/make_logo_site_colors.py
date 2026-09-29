from PIL import Image, ImageDraw, ImageFont
import numpy as np

# exact site colors (from vizuroiu.html :root vars)
BG      = (11, 12, 16)
TEXT    = (244, 245, 247)
MUTED   = (154, 160, 176)
ACCENT  = (255, 84, 54)
ACCENT2 = (255, 154, 60)

FP = "/usr/share/fonts/truetype/google-fonts/"
FL = "/usr/share/fonts/truetype/liberation2/"

SRC = "branding/logo png-uri/"
OUT = "branding/logo png-uri culori site/"

def gradient_fill(mask_im, angle_deg=35):
    """Fill an alpha mask with an ACCENT -> ACCENT2 diagonal gradient (site's signature glow)."""
    w, h = mask_im.size
    alpha = np.array(mask_im.split()[-1], dtype=np.float32)
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    ang = np.radians(angle_deg)
    proj = xx * np.cos(ang) + yy * np.sin(ang)
    proj -= proj.min()
    proj /= max(proj.max(), 1e-6)
    c1 = np.array(ACCENT, dtype=np.float32)
    c2 = np.array(ACCENT2, dtype=np.float32)
    rgb = c1[None, None, :] + (c2 - c1)[None, None, :] * proj[:, :, None]
    out = np.dstack([rgb, alpha]).astype(np.uint8)
    return Image.fromarray(out, "RGBA")

def solid_fill(mask_im, color):
    w, h = mask_im.size
    alpha = np.array(mask_im.split()[-1], dtype=np.uint8)
    rgb = np.zeros((h, w, 3), dtype=np.uint8)
    rgb[:, :] = color
    out = np.dstack([rgb, alpha])
    return Image.fromarray(out, "RGBA")

def text_w(draw, font, s):
    b = draw.textbbox((0, 0), s, font=font)
    return b[2] - b[0]

def text_h(draw, font, s):
    b = draw.textbbox((0, 0), s, font=font)
    return b[3] - b[1]

def trim(im):
    a = np.array(im.split()[-1])
    rows = np.where(a.max(axis=1) > 5)[0]
    cols = np.where(a.max(axis=0) > 5)[0]
    if len(rows) == 0 or len(cols) == 0:
        return im
    return im.crop((cols[0], rows[0], cols[-1] + 1, rows[-1] + 1))

# ---------- 1) ICON alone, site-color gradient ----------
icon_src = Image.open(SRC + "icon alb.png").convert("RGBA")
icon_colored = gradient_fill(icon_src)
icon_colored = trim(icon_colored)
icon_colored.save(OUT + "icon culori site.png")
print("saved icon")

# ---------- 2) WORDMARK "VIZUROIU" alone, site colors (white + orange dot) ----------
W, H = 1400, 300
word = Image.new("RGBA", (W, H), (0, 0, 0, 0))
d = ImageDraw.Draw(word)
f_word = ImageFont.truetype(FP + "Poppins-Bold.ttf", 150)
name = "VIZUROIU"
nw = text_w(d, f_word, name)
nh = text_h(d, f_word, name)
x0 = 20
y0 = (H - nh) // 2 - 20
d.text((x0, y0), name, font=f_word, fill=TEXT)
dotx = x0 + nw + 8
d.text((dotx, y0), ".", font=f_word, fill=ACCENT)
word = trim(word)
word.save(OUT + "nume vizuroiu culori site.png")
print("saved wordmark")

# ---------- 3) COMBINED — horizontal lockup (icon + name + tagline) ----------
icon_h_target = 260
ir = icon_colored.resize(
    (int(icon_colored.width * icon_h_target / icon_colored.height), icon_h_target),
    Image.LANCZOS,
)

canvas_w = ir.width + 40 + word.width + 60
canvas_h = 340
combo = Image.new("RGBA", (canvas_w, canvas_h), (0, 0, 0, 0))
icon_y = (canvas_h - ir.height) // 2 - 20
combo.paste(ir, (0, icon_y), ir)

word_y = icon_y + (ir.height - word.height) // 2 - 10
combo.paste(word, (ir.width + 40, word_y), word)

# tagline
dtag = ImageDraw.Draw(combo)
f_tag = ImageFont.truetype(FL + "LiberationSans-Regular.ttf", 46)
tag = "focus pe tine"
dtag.text((ir.width + 40 + 6, word_y + word.height + 14), tag, font=f_tag, fill=MUTED)

combo = trim(combo)
# add small transparent padding
pad = 30
padded = Image.new("RGBA", (combo.width + pad * 2, combo.height + pad * 2), (0, 0, 0, 0))
padded.paste(combo, (pad, pad), combo)
padded.save(OUT + "logo orizontal culori site.png")
print("saved horizontal lockup")

# ---------- 4) COMBINED — vertical lockup ----------
icon_h_target_v = 280
irv = icon_colored.resize(
    (int(icon_colored.width * icon_h_target_v / icon_colored.height), icon_h_target_v),
    Image.LANCZOS,
)
word_h_target = 140
wrv = word.resize(
    (int(word.width * word_h_target / word.height), word_h_target), Image.LANCZOS
)

vcanvas_w = max(irv.width, wrv.width) + 80
vcanvas_h = irv.height + 30 + wrv.height + 20 + 70
vcombo = Image.new("RGBA", (vcanvas_w, vcanvas_h), (0, 0, 0, 0))
vcombo.paste(irv, ((vcanvas_w - irv.width) // 2, 0), irv)
wy = irv.height + 30
vcombo.paste(wrv, ((vcanvas_w - wrv.width) // 2, wy), wrv)

dtag2 = ImageDraw.Draw(vcombo)
f_tag2 = ImageFont.truetype(FL + "LiberationSans-Regular.ttf", 40)
tag2 = "focus pe tine"
tw2 = text_w(dtag2, f_tag2, tag2)
dtag2.text(((vcanvas_w - tw2) // 2, wy + wrv.height + 18), tag2, font=f_tag2, fill=MUTED)

vcombo = trim(vcombo)
padded_v = Image.new("RGBA", (vcombo.width + pad * 2, vcombo.height + pad * 2), (0, 0, 0, 0))
padded_v.paste(vcombo, (pad, pad), vcombo)
padded_v.save(OUT + "logo vertical culori site.png")
print("saved vertical lockup")
