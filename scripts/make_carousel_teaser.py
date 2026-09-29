from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random

BG        = (11, 12, 16)
BG2       = (16, 18, 24)
SURFACE   = (22, 25, 34)
BORDER    = (36, 40, 55)
TEXT      = (244, 245, 247)
MUTED     = (170, 176, 190)
ACCENT    = (255, 84, 54)
ACCENT2   = (255, 154, 60)

FP = "/usr/share/fonts/truetype/google-fonts/"
FL = "/usr/share/fonts/truetype/liberation2/"
MUSEO_PATH = "/sessions/gifted-exciting-ritchie/mnt/claude code vsc/branding/fonts/MuseoModerno-800.ttf"
PHOTO = "img/fondatori-vizuroiu-media.jpg"
GRADIENT_ICON = "branding/logo png-uri gradient/icon gradient.png"

OUT_DIR = "branding/carusel-teaser-lansare"

W = H = 1600
PAD = 90

random.seed(11)

def text_w(draw, font, s):
    bbox = draw.textbbox((0, 0), s, font=font)
    return bbox[2] - bbox[0]

def radial_glow(size, color, alpha_center):
    g = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    gd = ImageDraw.Draw(g)
    cx = cy = size / 2
    for r in range(int(size/2), 0, -2):
        t = r / (size/2)
        a = int(alpha_center * (1 - t) ** 2)
        gd.ellipse([cx-r, cy-r, cx+r, cy+r], fill=color + (a,))
    return g.filter(ImageFilter.GaussianBlur(size*0.06))

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

BRAND_WORDS = {"VIZUROIU"}

def draw_title_mixed(draw, xy, text, font, font_brand, max_width, line_h, color=TEXT, align_center=False, canvas_w=W):
    lines = wrap_words(draw, text, font, max_width)
    x0, y = xy
    space_w = text_w(draw, font, " ")
    for line in lines:
        if align_center:
            lw_total = 0
            for w in line:
                key = w.upper().strip(",.")
                f = font_brand if key in BRAND_WORDS else font
                lw_total += text_w(draw, f, w) + space_w
            lw_total -= space_w
            x = (canvas_w - lw_total)//2
        else:
            x = x0
        for w in line:
            key = w.upper().strip(",.")
            f = font_brand if key in BRAND_WORDS else font
            draw.text((x, y), w, font=f, fill=color)
            x += text_w(draw, f, w) + space_w
        y += line_h
    return y

def draw_logo(draw, x, y, font_logo, dot_color=ACCENT, text_color=TEXT):
    draw.text((x, y), "VIZUROIU", font=font_logo, fill=text_color)
    lw = text_w(draw, font_logo, "VIZUROIU")
    draw.text((x+lw+4, y), ".", font=font_logo, fill=dot_color)
    return lw

def base_canvas(with_glow_topright=True, with_glow_bottomleft=True):
    img = Image.new("RGB", (W, H), BG)
    rgba = img.convert("RGBA")
    if with_glow_topright:
        g1 = radial_glow(1100, ACCENT, 60)
        rgba.alpha_composite(g1, (W-750, -380))
    if with_glow_bottomleft:
        g2 = radial_glow(1000, ACCENT2, 38)
        rgba.alpha_composite(g2, (-400, H-620))
    return rgba.convert("RGB")

def build_site_mockup(w, h):
    im = Image.new("RGB", (w, h), BG)
    d = ImageDraw.Draw(im, "RGBA")
    chrome_h = int(h*0.045)
    d.rectangle([0, 0, w, chrome_h], fill=BG2)
    dotr = int(chrome_h*0.16)
    cx = int(w*0.025)
    for c in [(255,95,86),(255,189,46),(39,201,63)]:
        d.ellipse([cx, chrome_h//2-dotr, cx+2*dotr, chrome_h//2+dotr], fill=c)
        cx += int(dotr*3.2)
    y = chrome_h
    nav_h = int(h*0.065)
    d.rectangle([0, y, w, y+nav_h], fill=BG)
    d.line([(0, y+nav_h), (w, y+nav_h)], fill=BORDER, width=2)
    lx = int(w*0.04)
    d.rectangle([lx, y+nav_h//2-12, lx+120, y+nav_h//2+12], fill=TEXT)
    nxx = int(w*0.42)
    for i in range(5):
        lw = 55 + (i%3)*16
        d.rounded_rectangle([nxx, y+nav_h//2-7, nxx+lw, y+nav_h//2+7], radius=5, fill=MUTED+(140,))
        nxx += lw + 26
    btn_w = int(w*0.11)
    d.rounded_rectangle([w-int(w*0.04)-btn_w, y+nav_h//2-20, w-int(w*0.04), y+nav_h//2+20], radius=20, fill=ACCENT)
    y += nav_h
    hero_h = int(h*0.55)
    d.rectangle([0, y, w, y+hero_h], fill=BG)
    glow = Image.new("RGBA", (int(w*0.55), int(w*0.55)), (0,0,0,0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([0,0,glow.size[0],glow.size[1]], fill=ACCENT+(65,))
    glow = glow.filter(ImageFilter.GaussianBlur(70))
    im.paste(Image.alpha_composite(im.crop((w-glow.size[0], y, w, y+glow.size[1])).convert("RGBA"), glow).convert("RGB"),
             (w-glow.size[0], y))
    padx = int(w*0.04)
    ty = y + int(hero_h*0.12)
    d.rounded_rectangle([padx, ty, padx+180, ty+28], radius=7, fill=ACCENT+(200,))
    ty += 56
    for wfrac in (0.55, 0.4, 0.46):
        lww = int(w*wfrac); lh = int(h*0.042)
        d.rounded_rectangle([padx, ty, padx+lww, ty+lh], radius=8, fill=TEXT)
        ty += lh + int(h*0.014)
    ty += int(h*0.018)
    for wfrac in (0.44, 0.34):
        lww = int(w*wfrac); lh = int(h*0.015)
        d.rounded_rectangle([padx, ty, padx+lww, ty+lh], radius=5, fill=MUTED+(150,))
        ty += lh + int(h*0.01)
    y += hero_h
    strip_h = int(h*0.10)
    d.rectangle([0, y, w, y+strip_h], fill=BG2)
    d.line([(0, y), (w, y)], fill=BORDER, width=2)
    cxp = int(w*0.03)
    card_h = int(strip_h*0.5)
    while cxp < w - int(w*0.03):
        cw = random.randint(int(w*0.05), int(w*0.09))
        d.rounded_rectangle([cxp, y+(strip_h-card_h)//2, cxp+cw, y+(strip_h+card_h)//2], radius=8, fill=SURFACE, outline=BORDER, width=2)
        cxp += cw + int(w*0.02)
    y += strip_h
    rest_h = h - y
    d.rectangle([0, y, w, h], fill=BG)
    gx, gy = int(w*0.04), y+int(rest_h*0.15)
    gap = int(w*0.02)
    cell_w = (w - 2*gx - 3*gap)//4
    cell_h = int(rest_h*0.5)
    for i in range(4):
        cxx = gx + i*(cell_w+gap)
        d.rounded_rectangle([cxx, gy, cxx+cell_w, gy+cell_h], radius=12, fill=SURFACE, outline=BORDER, width=2)
    return im

def slide_footer(draw, f_logo, index, total):
    foot_y = H - 96
    draw.line([(PAD, foot_y), (W-PAD, foot_y)], fill=BORDER, width=2)
    draw_logo(draw, PAD, foot_y+22, f_logo)
    ind = f"{index}/{total}"
    f_ind = ImageFont.truetype(FP + "Poppins-Bold.ttf", 26)
    iw = text_w(draw, f_ind, ind)
    draw.text((W-PAD-iw, foot_y+26), ind, font=f_ind, fill=MUTED)

def eyebrow(draw, label, f_eyebrow, f_eyebrow_brand):
    ex, ey = PAD, 74
    draw.rectangle([ex, ey+15, ex+50, ey+19], fill=ACCENT)
    x = ex + 66
    if "VIZUROIU" in label.upper():
        parts = label.split(" ", 1)
        draw.text((x, ey), parts[0], font=f_eyebrow_brand, fill=ACCENT)
        x += text_w(draw, f_eyebrow_brand, parts[0])
        if len(parts) > 1:
            draw.text((x, ey), " " + parts[1], font=f_eyebrow, fill=ACCENT)
    else:
        draw.text((x, ey), label, font=f_eyebrow, fill=ACCENT)

# ============================================================
# fonts
# ============================================================
f_eyebrow = ImageFont.truetype(FP + "Poppins-Bold.ttf", 28)
f_eyebrow_brand = ImageFont.truetype(MUSEO_PATH, 28)
f_logo = ImageFont.truetype(MUSEO_PATH, 40)
f_h1 = ImageFont.truetype(FP + "Poppins-Bold.ttf", 92)
f_h1_brand = ImageFont.truetype(MUSEO_PATH, 92)
f_sub = ImageFont.truetype(FL + "LiberationSans-Regular.ttf", 34)
f_num_outline = ImageFont.truetype(FP + "Poppins-Bold.ttf", 220)
f_date = ImageFont.truetype(FP + "Poppins-Bold.ttf", 96)

import os
os.makedirs(OUT_DIR, exist_ok=True)

# ============================================================
# SLIDE 1 — hook / mister
# ============================================================
mock = build_site_mockup(W, H)
img = mock.filter(ImageFilter.GaussianBlur(30))
scrim = Image.new("RGBA", (W, H), (11,12,16,165))
img = Image.alpha_composite(img.convert("RGBA"), scrim).convert("RGB")
draw = ImageDraw.Draw(img, "RGBA")
eyebrow(draw, "VIZUROIU  •  ÎN CURÂND", f_eyebrow, f_eyebrow_brand)

ty = 640
draw.text((PAD, ty), "DE O LUNĂ", font=f_h1, fill=TEXT)
ty += 106
draw.text((PAD, ty), "LUCRĂM LA", font=f_h1, fill=TEXT)
ty += 106
draw.text((PAD, ty), "CEVA.", font=f_h1, fill=ACCENT2)
ty += 106 + 30
sub_lines = wrap(draw, "Nu la un client — la noi.", f_sub, W-2*PAD)
for l in sub_lines:
    draw.text((PAD, ty), l, font=f_sub, fill=MUTED)
    ty += 44
slide_footer(draw, f_logo, 1, 5)
img.save(f"{OUT_DIR}/slide-1-hook.png", "PNG")
print("saved slide 1")

# ============================================================
# SLIDE 2 — identitate vizuala noua
# ============================================================
img = base_canvas()
draw = ImageDraw.Draw(img, "RGBA")
eyebrow(draw, "VIZUROIU  •  IDENTITATE NOUĂ", f_eyebrow, f_eyebrow_brand)

icon = Image.open(GRADIENT_ICON).convert("RGBA")
icon_w = 420
icon_r = icon.resize((icon_w, int(icon_w*icon.height/icon.width)), Image.LANCZOS)
img.paste(icon_r, ((W-icon_w)//2, 380), icon_r)

ty = 380 + icon_r.height + 90
line = "UN VIZUAL NOU."
lw_ = text_w(draw, f_h1, line)
draw.text(((W-lw_)//2, ty), line, font=f_h1, fill=TEXT)
ty += 106 + 24
sub = "Brand refresh în lucru — o să vedeți."
sw_ = text_w(draw, f_sub, sub)
draw.text(((W-sw_)//2, ty), sub, font=f_sub, fill=MUTED)

slide_footer(draw, f_logo, 2, 5)
img.save(f"{OUT_DIR}/slide-2-identitate.png", "PNG")
print("saved slide 2")

# ============================================================
# SLIDE 3 — studii de caz teaser
# ============================================================
img = base_canvas()
draw = ImageDraw.Draw(img, "RGBA")
eyebrow(draw, "VIZUROIU  •  STUDII DE CAZ", f_eyebrow, f_eyebrow_brand)

ty = 560
title_lines = ["O PAGINĂ PENTRU", "FIECARE CLIENT."]
for tl in title_lines:
    draw.text((PAD, ty), tl, font=f_h1, fill=TEXT)
    ty += 106
ty += 20
sub_lines = wrap(draw, "Fiecare proiect, propria poveste.", f_sub, W-2*PAD)
for l in sub_lines:
    draw.text((PAD, ty), l, font=f_sub, fill=MUTED)
    ty += 44

# abstract blurred portfolio cards row
cards_y = ty + 60
card_w, card_h_, gap = 300, 220, 28
total_w = card_w*3 + gap*2
cx0 = (W-total_w)//2
for i in range(3):
    cx = cx0 + i*(card_w+gap)
    draw.rounded_rectangle([cx, cards_y, cx+card_w, cards_y+card_h_], radius=20, fill=SURFACE, outline=BORDER, width=2)
    draw.rounded_rectangle([cx+24, cards_y+24, cx+card_w-24, cards_y+70], radius=8, fill=BORDER)
    draw.rounded_rectangle([cx+24, cards_y+card_h_-56, cx+140, cards_y+card_h_-30], radius=6, fill=MUTED+(120,))

slide_footer(draw, f_logo, 3, 5)
img.save(f"{OUT_DIR}/slide-3-studii-caz.png", "PNG")
print("saved slide 3")

# ============================================================
# SLIDE 4 — cifra teaser
# ============================================================
img = base_canvas()
draw = ImageDraw.Draw(img, "RGBA")
eyebrow(draw, "VIZUROIU  •  REZULTATE", f_eyebrow, f_eyebrow_brand)

num = "583+"
nw = text_w(draw, f_num_outline, num)
draw.text(((W-nw)//2, 560), num, font=f_num_outline, fill=None, stroke_width=5, stroke_fill=ACCENT)

ty = 560 + 300
line = "REZULTATE, NU VORBE."
lw_ = text_w(draw, f_h1, line)
# scale down if too wide
f_h1b = f_h1
if lw_ > W - 2*PAD:
    f_h1b = ImageFont.truetype(FP + "Poppins-Bold.ttf", 70)
    lw_ = text_w(draw, f_h1b, line)
draw.text(((W-lw_)//2, ty), line, font=f_h1b, fill=TEXT)
ty += 100
sub = "Cifrele complete, pe 14 august."
sw_ = text_w(draw, f_sub, sub)
draw.text(((W-sw_)//2, ty), sub, font=f_sub, fill=MUTED)

slide_footer(draw, f_logo, 4, 5)
img.save(f"{OUT_DIR}/slide-4-cifra.png", "PNG")
print("saved slide 4")

# ============================================================
# SLIDE 5 — CTA lansare
# ============================================================
mock2 = build_site_mockup(W, H)
img = mock2.filter(ImageFilter.GaussianBlur(34))
scrim = Image.new("RGBA", (W, H), (11,12,16,175))
img = Image.alpha_composite(img.convert("RGBA"), scrim).convert("RGB")
draw = ImageDraw.Draw(img, "RGBA")
eyebrow(draw, "VIZUROIU  •  LANSARE", f_eyebrow, f_eyebrow_brand)

line1 = "LANSAREA"
w1 = text_w(draw, f_h1, line1)
draw.text(((W-w1)//2, 600), line1, font=f_h1, fill=TEXT)

line2 = "14 AUGUST"
w2 = text_w(draw, f_date, line2)
draw.text(((W-w2)//2, 600+112), line2, font=f_date, fill=None, stroke_width=4, stroke_fill=ACCENT2)

sub = "Urmărește-ne ca să nu ratezi."
sw_ = text_w(draw, f_sub, sub)
draw.text(((W-sw_)//2, 600+112+150), sub, font=f_sub, fill=MUTED)

slide_footer(draw, f_logo, 5, 5)
img.save(f"{OUT_DIR}/slide-5-cta-lansare.png", "PNG")
print("saved slide 5")
