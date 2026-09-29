from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os, io

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
MUSEO_PATH = "branding/fonts/MuseoModerno-800.ttf"
PHOTO = "img/fondatori-vizuroiu-media.jpg"

OUT_DIR = "branding/carusel-ce-ofera"
os.makedirs(OUT_DIR, exist_ok=True)

W = H = 1600
PAD = 90

def text_w(draw, font, s):
    b = draw.textbbox((0, 0), s, font=font)
    return b[2] - b[0]

def radial_glow(size, color, alpha_center):
    g = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    gd = ImageDraw.Draw(g)
    cx = cy = size / 2
    for r in range(int(size / 2), 0, -2):
        t = r / (size / 2)
        a = int(alpha_center * (1 - t) ** 2)
        gd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color + (a,))
    return g.filter(ImageFilter.GaussianBlur(size * 0.06))

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
    return im.crop((left, top, left + target_w, top + target_h))

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
    draw.text((x + lw + 4, y), ".", font=font_logo, fill=dot_color)
    return lw

def base_canvas():
    img = Image.new("RGB", (W, H), BG)
    rgba = img.convert("RGBA")
    g1 = radial_glow(1100, ACCENT, 55)
    rgba.alpha_composite(g1, (W - 750, -380))
    g2 = radial_glow(1000, ACCENT2, 34)
    rgba.alpha_composite(g2, (-400, H - 620))
    return rgba.convert("RGB")

def slide_footer(draw, f_logo, index, total):
    foot_y = H - 96
    draw.line([(PAD, foot_y), (W - PAD, foot_y)], fill=BORDER, width=2)
    draw_logo(draw, PAD, foot_y + 22, f_logo)
    ind = f"{index}/{total}"
    f_ind = ImageFont.truetype(FP + "Poppins-Bold.ttf", 26)
    iw = text_w(draw, f_ind, ind)
    draw.text((W - PAD - iw, foot_y + 26), ind, font=f_ind, fill=MUTED)

def eyebrow(draw, label, f_eyebrow, f_eyebrow_brand):
    ex, ey = PAD, 74
    draw.rectangle([ex, ey + 15, ex + 50, ey + 19], fill=ACCENT)
    x = ex + 66
    if "VIZUROIU" in label.upper():
        parts = label.split(" ", 1)
        draw.text((x, ey), parts[0], font=f_eyebrow_brand, fill=ACCENT)
        x += text_w(draw, f_eyebrow_brand, parts[0])
        if len(parts) > 1:
            draw.text((x, ey), " " + parts[1], font=f_eyebrow, fill=ACCENT)
    else:
        draw.text((x, ey), label, font=f_eyebrow, fill=ACCENT)

def section_tag(draw, x, y, label, f_tag):
    tw = text_w(draw, f_tag, label)
    draw.rounded_rectangle([x, y, x + tw + 32, y + 50], radius=25, fill=SURFACE, outline=BORDER, width=2)
    draw.text((x + 16, y + 11), label, font=f_tag, fill=ACCENT2)
    return y + 50

f_eyebrow       = ImageFont.truetype(FP + "Poppins-Bold.ttf", 28)
f_eyebrow_brand = ImageFont.truetype(MUSEO_PATH, 28)
f_logo          = ImageFont.truetype(MUSEO_PATH, 40)
f_h1            = ImageFont.truetype(FP + "Poppins-Bold.ttf", 78)
f_h1_mid        = ImageFont.truetype(FP + "Poppins-Bold.ttf", 66)
f_sub           = ImageFont.truetype(FL + "LiberationSans-Regular.ttf", 36)
f_tag           = ImageFont.truetype(FP + "Poppins-Bold.ttf", 30)
f_quote         = ImageFont.truetype(FP + "Poppins-Bold.ttf", 42)
f_quote_by      = ImageFont.truetype(FL + "LiberationSans-Italic.ttf", 26)
f_stat_num      = ImageFont.truetype(FP + "Poppins-Bold.ttf", 96)
f_stat_lbl      = ImageFont.truetype(FL + "LiberationSans-Regular.ttf", 26)
f_step_mini     = ImageFont.truetype(FP + "Poppins-Bold.ttf", 24)
f_card_lbl      = ImageFont.truetype(FL + "LiberationSans-Bold.ttf", 24)
f_btn           = ImageFont.truetype(FP + "Poppins-Bold.ttf", 34)

TOTAL = 6

# ============================================================
# SLIDE 1 — COVER
# ============================================================
img = base_canvas()
d = ImageDraw.Draw(img, "RGBA")
eyebrow(d, "VIZUROIU • TUR SITE", f_eyebrow, f_eyebrow_brand)

ty = 300
for i, line in enumerate(["CE OFERĂ", "VIZUROIU.RO"]):
    color = ACCENT2 if i == 1 else TEXT
    d.text((PAD, ty), line, font=f_h1, fill=color)
    ty += 92

ty += 30
sub = "Un tur rapid prin site — cine suntem, cum lucrăm, ce rezultate obținem și cu cine am colaborat până acum."
for line in wrap(d, sub, f_sub, W - 2 * PAD - 60):
    d.text((PAD, ty), line, font=f_sub, fill=MUTED)
    ty += 50

ty += 40
nav_preview = ["Despre noi", "Cei 7 pași", "Rezultate", "Portofoliu", "Contact"]
sx = PAD
for label in nav_preview:
    lw = text_w(d, f_step_mini, label)
    if sx + lw > W - PAD:
        break
    d.rounded_rectangle([sx, ty, sx + lw + 28, ty + 46], radius=23, fill=SURFACE, outline=BORDER, width=2)
    d.text((sx + 14, ty + 10), label, font=f_step_mini, fill=MUTED)
    sx += lw + 28 + 16

slide_footer(d, f_logo, 1, TOTAL)
img.save(f"{OUT_DIR}/slide-1-cover.png")
print("saved slide 1")

# ============================================================
# SLIDE 2 — DESPRE NOI
# ============================================================
img = base_canvas()
d = ImageDraw.Draw(img, "RGBA")
eyebrow(d, "VIZUROIU • DESPRE NOI", f_eyebrow, f_eyebrow_brand)

ty = 300
ty = section_tag(d, PAD, ty, "POVESTEA NOASTRĂ", f_tag) + 50

d.text((PAD, ty), "Doi frați,", font=f_h1_mid, fill=TEXT)
ty += 78
d.text((PAD, ty), "o singură viziune.", font=f_h1_mid, fill=ACCENT2)
ty += 100

body = "Am pornit de la o pasiune comună pentru imagine, comunicare și tehnologie — investind puținele resurse pe care le aveam în echipamente profesionale."
for line in wrap(d, body, f_sub, W - 2 * PAD - 620):
    d.text((PAD, ty), line, font=f_sub, fill=MUTED)
    ty += 50

# photo card, bottom-right
card_w, card_h = 560, 640
cx0, cy0 = W - PAD - card_w, H - 96 - 40 - card_h
photo = Image.open(PHOTO).convert("RGB")
ph = fit_cover(photo, card_w - 32, 340)
img.paste(ph, (cx0 + 16, cy0 + 16))
d.rounded_rectangle([cx0, cy0, cx0 + card_w, cy0 + card_h], radius=22, outline=BORDER, width=2)

qy = cy0 + 16 + 340 + 26
quote = '„Fă mereu ce-ți place,\nca munca să devină\no plăcere."'
for line in quote.split("\n"):
    d.text((cx0 + 24, qy), line, font=f_quote, fill=TEXT)
    qy += 50
qy += 10
d.text((cx0 + 24, qy), "— sfatul tatălui nostru", font=f_quote_by, fill=MUTED)

slide_footer(d, f_logo, 2, TOTAL)
img.save(f"{OUT_DIR}/slide-2-despre-noi.png")
print("saved slide 2")

# ============================================================
# SLIDE 3 — CEI 7 PAȘI
# ============================================================
img = base_canvas()
d = ImageDraw.Draw(img, "RGBA")
eyebrow(d, "VIZUROIU • CUM LUCRĂM", f_eyebrow, f_eyebrow_brand)

ty = 300
ty = section_tag(d, PAD, ty, "PROCES", f_tag) + 50
d.text((PAD, ty), "Un proces clar,", font=f_h1_mid, fill=TEXT)
ty += 78
d.text((PAD, ty), "în 7 pași.", font=f_h1_mid, fill=ACCENT2)
ty += 100

body = "Nu lucrăm după un șablon rigid. Construim împreună un proces care ți se potrivește — de la strategie, până la analiza rezultatelor."
for line in wrap(d, body, f_sub, W - 2 * PAD - 40):
    d.text((PAD, ty), line, font=f_sub, fill=MUTED)
    ty += 50

ty += 60
steps = ["Analiză", "Mesaj", "Coaching", "Filmare", "Montaj", "Ads", "Optimizare"]
col_w = (W - 2 * PAD - 3 * 24) // 4
row_h = 130
for i, s in enumerate(steps):
    col = i % 4
    row = i // 4
    cx = PAD + col * (col_w + 24)
    cy = ty + row * (row_h + 24)
    d.rounded_rectangle([cx, cy, cx + col_w, cy + row_h], radius=16, fill=SURFACE, outline=BORDER, width=2)
    num = f"{i+1:02d}"
    d.text((cx + 20, cy + 16), num, font=None if False else ImageFont.truetype(FP + "Poppins-Bold.ttf", 34), fill=None, stroke_width=2, stroke_fill=ACCENT)
    d.text((cx + 20, cy + 78), s, font=f_card_lbl, fill=TEXT)

slide_footer(d, f_logo, 3, TOTAL)
img.save(f"{OUT_DIR}/slide-3-proces.png")
print("saved slide 3")

# ============================================================
# SLIDE 4 — REZULTATE
# ============================================================
img = base_canvas()
d = ImageDraw.Draw(img, "RGBA")
eyebrow(d, "VIZUROIU • REZULTATE", f_eyebrow, f_eyebrow_brand)

ty = 300
ty = section_tag(d, PAD, ty, "CIFRE, NU PROMISIUNI", f_tag) + 50
d.text((PAD, ty), "Rezultate", font=f_h1_mid, fill=TEXT)
ty += 78
d.text((PAD, ty), "măsurabile.", font=f_h1_mid, fill=ACCENT2)
ty += 120

stats = [
    ("37%", "creștere medie a vânzărilor pentru clienții noștri"),
    ("100%", "echipă certificată Google și Facebook"),
    ("81%", "rezultate îmbunătățite față de agențiile anterioare"),
    ("583+", "clienți potențiali generați până acum"),
]
col_w = (W - 2 * PAD - 40) // 2
row_h = 220
for i, (num, label) in enumerate(stats):
    col = i % 2
    row = i // 2
    cx = PAD + col * (col_w + 40)
    cy = ty + row * (row_h + 20)
    d.rounded_rectangle([cx, cy, cx + col_w, cy + row_h - 20], radius=18, fill=SURFACE, outline=BORDER, width=2)
    d.text((cx + 28, cy + 20), num, font=f_stat_num, fill=None, stroke_width=3, stroke_fill=ACCENT)
    label_lines = wrap(d, label, f_stat_lbl, col_w - 56)
    ly = cy + 140
    for ll in label_lines:
        d.text((cx + 28, ly), ll, font=f_stat_lbl, fill=MUTED)
        ly += 32

slide_footer(d, f_logo, 4, TOTAL)
img.save(f"{OUT_DIR}/slide-4-rezultate.png")
print("saved slide 4")

# ============================================================
# SLIDE 5 — PORTOFOLIU
# ============================================================
img = base_canvas()
d = ImageDraw.Draw(img, "RGBA")
eyebrow(d, "VIZUROIU • PORTOFOLIU", f_eyebrow, f_eyebrow_brand)

ty = 300
ty = section_tag(d, PAD, ty, "PESTE 20 DE BRANDURI", f_tag) + 50
d.text((PAD, ty), "Clienți reali,", font=f_h1_mid, fill=TEXT)
ty += 78
d.text((PAD, ty), "rezultate reale.", font=f_h1_mid, fill=ACCENT2)
ty += 110

body = "AG Tiny House, CONAF, Pizzeria Arena, Brăila Imobiliare, Metalift, Tabiet Good Food și alții — fiecare cu pagină dedicată pe site."
for line in wrap(d, body, f_sub, W - 2 * PAD - 40):
    d.text((PAD, ty), line, font=f_sub, fill=MUTED)
    ty += 50
ty += 40

# real logos
ag_logo_img = None
try:
    import cairosvg
    with open("img/ag-tiny-house.svg", "r", encoding="utf-8") as f:
        svg_text = f.read().replace("#1a5c3a", "#F4F5F7")
    png_bytes = cairosvg.svg2png(bytestring=svg_text.encode("utf-8"), output_width=300, output_height=300)
    ag_logo_img = Image.open(io.BytesIO(png_bytes)).convert("RGBA")
except Exception as e:
    print("AG logo render failed:", e)

conaf_logo_img = None
try:
    conaf_full = Image.open("youtube-covers/logos/conaf.webp").convert("RGBA")
    conaf_logo_img = conaf_full.crop((0, 0, conaf_full.width, 51))
except Exception as e:
    print("CONAF logo load failed:", e)

grid_labels = ["AG TINY HOUSE", "CONAF", "PIZZERIA ARENA", "METALIFT", "BRĂILA IMOB.", "+ 15 ALTELE"]
cols, rows = 3, 2
gap = 24
cell_w = (W - 2 * PAD - (cols - 1) * gap) // cols
cell_h = 200
for i, label in enumerate(grid_labels):
    col = i % cols
    row = i // cols
    cx = PAD + col * (cell_w + gap)
    cy = ty + row * (cell_h + gap)
    d.rounded_rectangle([cx, cy, cx + cell_w, cy + cell_h], radius=18, fill=SURFACE, outline=BORDER, width=2)
    if i == 0 and ag_logo_img is not None:
        sz = 84
        ic = ag_logo_img.resize((sz, sz), Image.LANCZOS)
        img.paste(ic, (cx + (cell_w - sz) // 2, cy + 22), ic)
    elif i == 1 and conaf_logo_img is not None:
        bw, bh = cell_w - 60, 66
        badge = Image.new("RGBA", (bw, bh), (0, 0, 0, 0))
        bd = ImageDraw.Draw(badge)
        bd.rounded_rectangle([0, 0, bw, bh], radius=12, fill=(244, 245, 247, 255))
        lw_target = bw - 24
        logo_r = conaf_logo_img.resize((lw_target, int(lw_target * conaf_logo_img.height / conaf_logo_img.width)), Image.LANCZOS)
        badge.paste(logo_r, ((bw - logo_r.width) // 2, (bh - logo_r.height) // 2), logo_r)
        img.paste(badge, (cx + 30, cy + 26), badge)
    elif i == 5:
        plus_cx, plus_cy = cx + cell_w // 2, cy + 60
        arm, thick = 26, 8
        d.rounded_rectangle([plus_cx - arm, plus_cy - thick // 2, plus_cx + arm, plus_cy + thick // 2], radius=thick // 2, fill=ACCENT2)
        d.rounded_rectangle([plus_cx - thick // 2, plus_cy - arm, plus_cx + thick // 2, plus_cy + arm], radius=thick // 2, fill=ACCENT2)
    else:
        d.ellipse([cx + cell_w // 2 - 22, cy + 34, cx + cell_w // 2 + 22, cy + 78], outline=ACCENT, width=3)

    lbl_w = text_w(d, f_card_lbl, label)
    d.text((cx + (cell_w - lbl_w) // 2, cy + cell_h - 46), label, font=f_card_lbl, fill=MUTED)

slide_footer(d, f_logo, 5, TOTAL)
img.save(f"{OUT_DIR}/slide-5-portofoliu.png")
print("saved slide 5")

# ============================================================
# SLIDE 6 — CONTACT / CTA
# ============================================================
img = base_canvas()
d = ImageDraw.Draw(img, "RGBA")
eyebrow(d, "VIZUROIU • CONTACT", f_eyebrow, f_eyebrow_brand)

ty = 320
ty = section_tag(d, PAD, ty, "AUDIT GRATUIT", f_tag) + 60

for i, line in enumerate(["PRIMUL PAS", "E GRATUIT."]):
    color = ACCENT2 if i == 1 else TEXT
    d.text((PAD, ty), line, font=f_h1, fill=color)
    ty += 92

ty += 30
body = "Un audit rapid al prezenței tale online, fără niciun angajament. Vedem împreună ce se poate face — și dacă ni se potrivim."
for line in wrap(d, body, f_sub, W - 2 * PAD - 60):
    d.text((PAD, ty), line, font=f_sub, fill=MUTED)
    ty += 50

ty += 50
btn_text = "AUDIT GRATUIT"
bw = text_w(d, f_btn, btn_text) + 80
bh = 96
d.rounded_rectangle([PAD, ty, PAD + bw, ty + bh], radius=bh // 2, fill=ACCENT)
d.text((PAD + 40, ty + 28), btn_text, font=f_btn, fill=(255, 255, 255))

tag_text = "VIZUROIU.RO"
tw = text_w(d, f_btn, tag_text)
d.text((W - PAD - tw, ty + 28), tag_text, font=f_btn, fill=ACCENT2)

slide_footer(d, f_logo, 6, TOTAL)
img.save(f"{OUT_DIR}/slide-6-contact.png")
print("saved slide 6")
