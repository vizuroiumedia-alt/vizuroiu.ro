from PIL import Image, ImageDraw, ImageFont, ImageFilter

BG        = (11, 12, 16)
BORDER    = (36, 40, 55)
TEXT      = (244, 245, 247)
MUTED     = (170, 176, 190)
ACCENT    = (255, 84, 54)
ACCENT2   = (255, 154, 60)

FP = "/usr/share/fonts/truetype/google-fonts/"
FL = "/usr/share/fonts/truetype/liberation2/"
PHOTO = "img/fondatori-vizuroiu-media.jpg"

HIGHLIGHT_WORDS = {"ALEGI"}

LIST_ITEMS = [
    ("01", "PORTOFOLIU REAL"),
    ("02", "STUDII DE CAZ"),
    ("03", "PROCES ÎN 7 PAȘI"),
    ("04", "CIFRE CONCRETE"),
    ("05", "ACOPERIRE REGIONALĂ"),
    ("06", "AUDIT GRATUIT"),
]

def radial_glow(size, color, alpha_center):
    g = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    gd = ImageDraw.Draw(g)
    cx = cy = size / 2
    for r in range(int(size/2), 0, -2):
        t = r / (size/2)
        a = int(alpha_center * (1 - t) ** 2)
        gd.ellipse([cx-r, cy-r, cx+r, cy+r], fill=color + (a,))
    return g.filter(ImageFilter.GaussianBlur(size*0.06))

def text_w(draw, font, s):
    bbox = draw.textbbox((0, 0), s, font=font)
    return bbox[2] - bbox[0]

def wrap(draw, text, font, max_width):
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if text_w(draw, font, trial) <= max_width:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines

def wrap_words(draw, text, font, max_width):
    """Wrap into lines of individual words (for mixed-color rendering)."""
    words = text.split(" ")
    space_w = text_w(draw, font, " ")
    lines, cur, cur_w = [], [], 0
    for w in words:
        ww = text_w(draw, font, w)
        add = ww + (space_w if cur else 0)
        if cur_w + add <= max_width:
            cur.append(w)
            cur_w += add
        else:
            lines.append(cur)
            cur = [w]
            cur_w = ww
    if cur:
        lines.append(cur)
    return lines

def draw_title_mixed(draw, xy, text, font, max_width, line_h, color=TEXT, hl_color=ACCENT2):
    lines = wrap_words(draw, text, font, max_width)
    x0, y = xy
    space_w = text_w(draw, font, " ")
    for line in lines:
        x = x0
        for w in line:
            c = hl_color if w.upper().strip(",.") in HIGHLIGHT_WORDS else color
            draw.text((x, y), w, font=font, fill=c)
            x += text_w(draw, font, w) + space_w
        y += line_h
    return y

def fit_cover(im, target_w, target_h):
    src_w, src_h = im.size
    src_ratio = src_w / src_h
    tgt_ratio = target_w / target_h
    if src_ratio > tgt_ratio:
        new_h = target_h
        new_w = int(src_ratio * new_h)
    else:
        new_w = target_w
        new_h = int(new_w / src_ratio)
    im = im.resize((new_w, new_h), Image.LANCZOS)
    left = (new_w - target_w) // 2
    top = (new_h - target_h) // 2
    return im.crop((left, top, left+target_w, top+target_h))

def draw_logo(draw, x, y, font_logo, dot_color=ACCENT, text_color=TEXT):
    draw.text((x, y), "VIZUROIU", font=font_logo, fill=text_color)
    lw = text_w(draw, font_logo, "VIZUROIU")
    draw.text((x+lw+4, y), ".", font=font_logo, fill=dot_color)
    return lw

TITLE = "6 MOTIVE PENTRU CARE SĂ ALEGI VIZUROIU"
SUBTITLE = "DOI FRAȚI, O SINGURĂ VIZIUNE: CONTENT CARE ADUCE REZULTATE REALE AFACERII TALE."

# ============================================================
# HORIZONTAL 2560x1440
# ============================================================
W, H = 2560, 1440
f_eyebrow = ImageFont.truetype(FP + "Poppins-Bold.ttf", 30)
f_title   = ImageFont.truetype(FP + "Poppins-Bold.ttf", 78)
f_sub     = ImageFont.truetype(FL + "LiberationSans-Bold.ttf", 34)
f_logo    = ImageFont.truetype(FP + "Poppins-Bold.ttf", 44)
f_list_n  = ImageFont.truetype(FP + "Poppins-Bold.ttf", 34)
f_list_t  = ImageFont.truetype(FL + "LiberationSans-Bold.ttf", 30)

img = Image.new("RGB", (W, H), BG)
rgba = img.convert("RGBA")
glow1 = radial_glow(1400, ACCENT, 55)
rgba.alpha_composite(glow1, (-500, -450))
img = rgba.convert("RGB")

PAD = 110
photo_w = 1080
photo = Image.open(PHOTO).convert("RGB")
photo = fit_cover(photo, photo_w, H)
img.paste(photo, (W-photo_w, 0))

fade_w = 220
fade = Image.new("L", (fade_w, H), 0)
fd = ImageDraw.Draw(fade)
for i in range(fade_w):
    a = int(255 * (i/fade_w))
    fd.line([(i, 0), (i, H)], fill=a)
bg_strip = Image.new("RGB", (fade_w, H), BG)
img.paste(bg_strip, (W-photo_w, 0), Image.eval(fade, lambda p: 255-p))

draw = ImageDraw.Draw(img, "RGBA")

ex, ey = PAD, 84
draw.rectangle([ex, ey+15, ex+56, ey+19], fill=ACCENT)
draw.text((ex+72, ey), "VIZUROIU  •  CINE SUNTEM", font=f_eyebrow, fill=ACCENT)

max_text_w = W - photo_w - PAD - 160
ty = 210
ty = draw_title_mixed(draw, (PAD, ty), TITLE, f_title, max_text_w, 92)

ty += 18
draw.rectangle([PAD, ty, PAD+90, ty+6], fill=ACCENT)
ty += 42
sub_lines = wrap(draw, SUBTITLE, f_sub, max_text_w)
for sl in sub_lines:
    draw.text((PAD, ty), sl, font=f_sub, fill=MUTED)
    ty += 48

# --- fill the remaining space: preview list of the 6 points ---
ty += 56
list_top = ty
col_w = max_text_w // 2
row_h = 96
for i, (num, label) in enumerate(LIST_ITEMS):
    col = i % 2
    row = i // 2
    lx = PAD + col*col_w
    ly = list_top + row*row_h
    draw.text((lx, ly), num, font=f_list_n, fill=None, stroke_width=2, stroke_fill=ACCENT)
    label_lines = wrap(draw, label, f_list_t, col_w - 90)
    lyy = ly + 4
    for ll in label_lines:
        draw.text((lx+68, lyy), ll, font=f_list_t, fill=TEXT)
        lyy += 36

foot_y = H - 110
draw.line([(PAD, foot_y), (W-photo_w-90, foot_y)], fill=BORDER, width=2)
draw_logo(draw, PAD, foot_y+26, f_logo)
tag = "VIZUROIU.RO"
tw = text_w(draw, f_logo, tag)
draw.text((W-photo_w-90-tw, foot_y+26), tag, font=f_logo, fill=MUTED)

img.save("vizuroiu-cover-00-6-motive.png", "PNG")
print("saved horizontal intro")

# ============================================================
# VERTICAL 1080x1920
# ============================================================
W2, H2 = 1080, 1920
f_eyebrow_v = ImageFont.truetype(FP + "Poppins-Bold.ttf", 26)
f_title_v   = ImageFont.truetype(FP + "Poppins-Bold.ttf", 58)
f_sub_v     = ImageFont.truetype(FL + "LiberationSans-Bold.ttf", 28)
f_logo_v    = ImageFont.truetype(FP + "Poppins-Bold.ttf", 36)
f_list_n_v  = ImageFont.truetype(FP + "Poppins-Bold.ttf", 30)
f_list_t_v  = ImageFont.truetype(FL + "LiberationSans-Bold.ttf", 27)

img2 = Image.new("RGB", (W2, H2), BG)
photo2 = Image.open(PHOTO).convert("RGB")
photo_h = 1120
photo2 = fit_cover(photo2, W2, photo_h)
img2.paste(photo2, (0, 0))

scrim = Image.new("L", (W2, photo_h), 0)
sd = ImageDraw.Draw(scrim)
fade_h = 420
for i in range(fade_h):
    a = int(255 * (i/fade_h))
    y = photo_h - fade_h + i
    sd.line([(0, y), (W2, y)], fill=a)
bg_layer = Image.new("RGB", (W2, photo_h), BG)
img2.paste(bg_layer, (0, 0), scrim)

rgba2 = img2.convert("RGBA")
glow2 = radial_glow(1100, ACCENT2, 40)
rgba2.alpha_composite(glow2, (-450, H2-650))
img2 = rgba2.convert("RGB")

draw2 = ImageDraw.Draw(img2, "RGBA")

PAD2 = 76
ex2, ey2 = PAD2, 68
draw2.rectangle([ex2, ey2+13, ex2+44, ey2+16], fill=ACCENT)
draw2.text((ex2+58, ey2), "VIZUROIU  •  CINE SUNTEM", font=f_eyebrow_v, fill=ACCENT)

max_text_w2 = W2 - 2*PAD2
ty2 = photo_h - 240
ty2 = draw_title_mixed(draw2, (PAD2, ty2), TITLE, f_title_v, max_text_w2, 68)

ty2 += 18
draw2.rectangle([PAD2, ty2, PAD2+80, ty2+6], fill=ACCENT)
ty2 += 36
sub_lines2 = wrap(draw2, SUBTITLE, f_sub_v, max_text_w2)
for sl in sub_lines2:
    draw2.text((PAD2, ty2), sl, font=f_sub_v, fill=MUTED)
    ty2 += 40

# --- fill remaining space: preview list of the 6 points, 2 columns ---
ty2 += 100
list_top2 = ty2
col_w2 = max_text_w2 // 2
row_h2 = 118
for i, (num, label) in enumerate(LIST_ITEMS):
    col = i % 2
    row = i // 2
    lx = PAD2 + col*col_w2
    ly = list_top2 + row*row_h2
    draw2.text((lx, ly), num, font=f_list_n_v, fill=None, stroke_width=2, stroke_fill=ACCENT)
    label_lines = wrap(draw2, label, f_list_t_v, col_w2 - 78)
    lyy = ly + 2
    for ll in label_lines:
        draw2.text((lx+60, lyy), ll, font=f_list_t_v, fill=TEXT)
        lyy += 32

foot_y2 = H2 - 130
draw2.line([(PAD2, foot_y2), (W2-PAD2, foot_y2)], fill=BORDER, width=2)
draw_logo(draw2, PAD2, foot_y2+30, f_logo_v)
tag2 = "VIZUROIU.RO"
tw2 = text_w(draw2, f_logo_v, tag2)
draw2.text((W2-PAD2-tw2, foot_y2+30), tag2, font=f_logo_v, fill=MUTED)

img2.save("vizuroiu-cover-vert-00-6-motive.png", "PNG")
print("saved vertical intro")
