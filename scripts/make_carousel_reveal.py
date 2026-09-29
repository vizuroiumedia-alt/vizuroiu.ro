from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random, os

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

OUT_DIR = "branding/carusel-dupa-lansare"
os.makedirs(OUT_DIR, exist_ok=True)

W = H = 1600
PAD = 90
random.seed(3)

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

def draw_logo(draw, x, y, font_logo, dot_color=ACCENT, text_color=TEXT):
    draw.text((x, y), "VIZUROIU", font=font_logo, fill=text_color)
    lw = text_w(draw, font_logo, "VIZUROIU")
    draw.text((x+lw+4, y), ".", font=font_logo, fill=dot_color)
    return lw

def base_canvas():
    img = Image.new("RGB", (W, H), BG)
    rgba = img.convert("RGBA")
    g1 = radial_glow(1100, ACCENT, 60)
    rgba.alpha_composite(g1, (W-750, -380))
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
    bar_x0, bar_x1 = int(w*0.32), int(w*0.68)
    f_url = ImageFont.truetype(FL + "LiberationSans-Regular.ttf", int(chrome_h*0.36))
    d.rounded_rectangle([bar_x0, int(chrome_h*0.24), bar_x1, int(chrome_h*0.76)], radius=chrome_h//3, fill=SURFACE)
    url = "vizuroiu.ro"
    uw = d.textbbox((0,0), url, font=f_url)[2]
    d.text(((bar_x0+bar_x1-uw)//2, int(chrome_h*0.3)), url, font=f_url, fill=MUTED)
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
    ty = y + int(hero_h*0.10)
    d.rounded_rectangle([padx, ty, padx+180, ty+28], radius=7, fill=ACCENT+(210,))
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
    # real founders photo inside the mockup hero
    photo = Image.open(PHOTO).convert("RGB")
    ph_w = int(w*0.34)
    ph_h = int(hero_h*0.60)
    photo = fit_cover(photo, ph_w, ph_h)
    im.paste(photo, (w-int(w*0.04)-ph_w, y+int(hero_h*0.28)))
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

f_eyebrow = ImageFont.truetype(FP + "Poppins-Bold.ttf", 28)
f_eyebrow_brand = ImageFont.truetype(MUSEO_PATH, 28)
f_logo = ImageFont.truetype(MUSEO_PATH, 40)
f_h1 = ImageFont.truetype(FP + "Poppins-Bold.ttf", 92)
f_sub = ImageFont.truetype(FL + "LiberationSans-Regular.ttf", 34)
f_stat_num = ImageFont.truetype(FP + "Poppins-Bold.ttf", 108)
f_stat_lbl = ImageFont.truetype(FL + "LiberationSans-Regular.ttf", 26)
f_quote = ImageFont.truetype(FP + "Poppins-Bold.ttf", 52)
f_btn = ImageFont.truetype(FP + "Poppins-Bold.ttf", 34)

# ============================================================
# SLIDE 1 — E LIVE (reveal, unblurred mockup)
# ============================================================
mock = build_site_mockup(W, H)
img = mock.copy()
scrim = Image.new("RGBA", (W, H), (11,12,16,120))
img = Image.alpha_composite(img.convert("RGBA"), scrim).convert("RGB")
draw = ImageDraw.Draw(img, "RGBA")
eyebrow(draw, "VIZUROIU  •  LIVE ACUM", f_eyebrow, f_eyebrow_brand)

ty = 660
draw.text((PAD, ty), "E LIVE.", font=f_h1, fill=ACCENT2)
ty += 106 + 20
sub_lines = wrap(draw, "Site-ul nostru nou e gata de vizitat.", f_sub, W-2*PAD)
for l in sub_lines:
    draw.text((PAD, ty), l, font=f_sub, fill=MUTED)
    ty += 44
ty += 30
tag = "VIZUROIU.RO"
f_tag = ImageFont.truetype(MUSEO_PATH, 44)
draw.text((PAD, ty), tag, font=f_tag, fill=TEXT)

slide_footer(draw, f_logo, 1, 5)
img.save(f"{OUT_DIR}/slide-1-e-live.png", "PNG")
print("saved slide 1")

# ============================================================
# SLIDE 2 — fondatori / cine suntem (poza reala)
# ============================================================
img = Image.new("RGB", (W, H), BG)
photo = Image.open(PHOTO).convert("RGB")
photo_h = int(H*0.62)
photo_r = fit_cover(photo, W, photo_h)
img.paste(photo_r, (0, 0))

scrim = Image.new("L", (W, photo_h), 0)
sd = ImageDraw.Draw(scrim)
fade_h = int(photo_h*0.42)
for i in range(fade_h):
    a = int(255*(i/fade_h))
    y = photo_h-fade_h+i
    sd.line([(0,y),(W,y)], fill=a)
bgL = Image.new("RGB", (W, photo_h), BG)
img.paste(bgL, (0,0), scrim)

rgba = img.convert("RGBA")
glow = radial_glow(1000, ACCENT2, 40)
rgba.alpha_composite(glow, (-380, H-620))
img = rgba.convert("RGB")

draw = ImageDraw.Draw(img, "RGBA")
eyebrow(draw, "VIZUROIU  •  CINE SUNTEM", f_eyebrow, f_eyebrow_brand)

ty = photo_h - 90
q_lines = wrap(draw, "Doi frați, o singură viziune.", f_quote, W-2*PAD)
for l in q_lines:
    draw.text((PAD, ty), l, font=f_quote, fill=TEXT)
    ty += 64
ty += 20
sub_lines = wrap(draw, "Fă mereu ce-ți place, ca munca să devină o plăcere.", f_sub, W-2*PAD)
for l in sub_lines:
    draw.text((PAD, ty), l, font=f_sub, fill=MUTED)
    ty += 44

slide_footer(draw, f_logo, 2, 5)
img.save(f"{OUT_DIR}/slide-2-cine-suntem.png", "PNG")
print("saved slide 2")

# ============================================================
# SLIDE 3 — portofoliu real (reveal, carduri colorate)
# ============================================================
img = base_canvas()
draw = ImageDraw.Draw(img, "RGBA")
eyebrow(draw, "VIZUROIU  •  PORTOFOLIU", f_eyebrow, f_eyebrow_brand)

ty = 560
for tl in ["PESTE 20 DE", "BRANDURI REALE."]:
    draw.text((PAD, ty), tl, font=f_h1, fill=TEXT)
    ty += 106
ty += 55
sub_lines = wrap(draw, "AG Tiny House, Pizzeria Arena, CONAF, Brăila Imobiliare și alții.", f_sub, W-2*PAD)
for l in sub_lines:
    draw.text((PAD, ty), l, font=f_sub, fill=MUTED)
    ty += 44

cards_y = ty + 60
card_w, card_h_, gap = 300, 220, 28
total_w = card_w*3 + gap*2
cx0 = (W-total_w)//2
labels = ["AG TINY HOUSE", "CONAF", "+ 18 ALTELE"]

# real AG Tiny House logo, recolored white, rasterized from the site's svg
ag_svg_path = "img/ag-tiny-house.svg"
ag_logo_img = None
try:
    import cairosvg
    with open(ag_svg_path, "r", encoding="utf-8") as f:
        svg_text = f.read()
    svg_text_white = svg_text.replace("#1a5c3a", "#F4F5F7")
    png_bytes = cairosvg.svg2png(bytestring=svg_text_white.encode("utf-8"), output_width=300, output_height=300)
    import io
    ag_logo_img = Image.open(io.BytesIO(png_bytes)).convert("RGBA")
except Exception as e:
    print("AG logo render failed:", e)

# real CONAF logo (cropped to emblem+wordmark, on a white badge for contrast)
conaf_logo_img = None
try:
    conaf_full = Image.open("youtube-covers/logos/conaf.webp").convert("RGBA")
    conaf_logo_img = conaf_full.crop((0, 0, conaf_full.width, 51))
except Exception as e:
    print("CONAF logo load failed:", e)

for i in range(3):
    cx = cx0 + i*(card_w+gap)
    draw.rounded_rectangle([cx, cards_y, cx+card_w, cards_y+card_h_], radius=20, fill=SURFACE, outline=BORDER, width=2)
    if i == 0 and ag_logo_img is not None:
        icon_size = 96
        icon_r = ag_logo_img.resize((icon_size, icon_size), Image.LANCZOS)
        img.paste(icon_r, (cx+(card_w-icon_size)//2, cards_y+24), icon_r)
    elif i == 1 and conaf_logo_img is not None:
        badge_w, badge_h = 190, 74
        badge = Image.new("RGBA", (badge_w, badge_h), (0,0,0,0))
        bd = ImageDraw.Draw(badge)
        bd.rounded_rectangle([0, 0, badge_w, badge_h], radius=14, fill=(244,245,247,255))
        logo_target_w = badge_w - 28
        logo_r = conaf_logo_img.resize((logo_target_w, int(logo_target_w*conaf_logo_img.height/conaf_logo_img.width)), Image.LANCZOS)
        badge.paste(logo_r, ((badge_w-logo_r.width)//2, (badge_h-logo_r.height)//2), logo_r)
        img.paste(badge, (cx+(card_w-badge_w)//2, cards_y+34), badge)
    elif i == 2:
        # "+" plus icon for "more brands"
        plus_cx, plus_cy = cx+card_w//2, cards_y+68
        arm, thick = 34, 10
        draw.rounded_rectangle([plus_cx-arm, plus_cy-thick//2, plus_cx+arm, plus_cy+thick//2], radius=thick//2, fill=ACCENT2)
        draw.rounded_rectangle([plus_cx-thick//2, plus_cy-arm, plus_cx+thick//2, plus_cy+arm], radius=thick//2, fill=ACCENT2)
    else:
        draw.ellipse([cx+card_w//2-28, cards_y+40, cx+card_w//2+28, cards_y+96], outline=ACCENT2, width=4)
    lbl = labels[i]
    f_lbl = ImageFont.truetype(FL + "LiberationSans-Bold.ttf", 24)
    lw_ = text_w(draw, f_lbl, lbl)
    draw.text((cx+(card_w-lw_)//2, cards_y+card_h_-60), lbl, font=f_lbl, fill=MUTED)

slide_footer(draw, f_logo, 3, 5)
img.save(f"{OUT_DIR}/slide-3-portofoliu.png", "PNG")
print("saved slide 3")

# ============================================================
# SLIDE 4 — cifre complete
# ============================================================
img = base_canvas()
draw = ImageDraw.Draw(img, "RGBA")
eyebrow(draw, "VIZUROIU  •  REZULTATE", f_eyebrow, f_eyebrow_brand)

ty = 480
for tl in ["CIFRE COMPLETE,", "NU VORBE."]:
    draw.text((PAD, ty), tl, font=f_h1, fill=TEXT)
    ty += 106

stats = [("37%", "creștere medie a vânzărilor"), ("583+", "clienți potențiali generați"), ("81%", "rezultate mai bune ca înainte")]
sy = ty + 100
for num, label in stats:
    nw = text_w(draw, f_stat_num, num)
    draw.text((PAD, sy), num, font=f_stat_num, fill=None, stroke_width=4, stroke_fill=ACCENT)
    label_lines = wrap(draw, label, f_stat_lbl, W-2*PAD-nw-40)
    lyy = sy + 58 - (len(label_lines)-1)*18
    for ll in label_lines:
        draw.text((PAD+nw+30, lyy), ll, font=f_stat_lbl, fill=MUTED)
        lyy += 36
    sy += 160

slide_footer(draw, f_logo, 4, 5)
img.save(f"{OUT_DIR}/slide-4-cifre.png", "PNG")
print("saved slide 4")

# ============================================================
# SLIDE 5 — CTA audit gratuit
# ============================================================
img = base_canvas()
draw = ImageDraw.Draw(img, "RGBA")
eyebrow(draw, "VIZUROIU  •  HAI SĂ DISCUTĂM", f_eyebrow, f_eyebrow_brand)

ty = 620
for tl in ["PRIMUL PAS E", "GRATUIT."]:
    color = ACCENT2 if tl == "GRATUIT." else TEXT
    draw.text((PAD, ty), tl, font=f_h1, fill=color)
    ty += 106
ty += 20
sub_lines = wrap(draw, "Beneficiezi de un audit gratuit, fără niciun angajament.", f_sub, W-2*PAD)
for l in sub_lines:
    draw.text((PAD, ty), l, font=f_sub, fill=MUTED)
    ty += 44

ty += 50
btn_w, btn_h = 420, 90
draw.rounded_rectangle([PAD, ty, PAD+btn_w, ty+btn_h], radius=btn_h//2, fill=ACCENT)
btxt = "Audit gratuit"
bw_ = text_w(draw, f_btn, btxt)
draw.text((PAD+(btn_w-bw_)//2, ty+(btn_h-38)//2), btxt, font=f_btn, fill=BG)

ty += btn_h + 50
tag = "VIZUROIU.RO"
f_tag = ImageFont.truetype(MUSEO_PATH, 40)
draw.text((PAD, ty), tag, font=f_tag, fill=MUTED)

slide_footer(draw, f_logo, 5, 5)
img.save(f"{OUT_DIR}/slide-5-cta.png", "PNG")
print("saved slide 5")
