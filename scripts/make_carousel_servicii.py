from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

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

OUT_DIR = "branding/carusel-servicii"
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

f_eyebrow       = ImageFont.truetype(FP + "Poppins-Bold.ttf", 28)
f_eyebrow_brand = ImageFont.truetype(MUSEO_PATH, 28)
f_logo          = ImageFont.truetype(MUSEO_PATH, 40)
f_h1            = ImageFont.truetype(FP + "Poppins-Bold.ttf", 78)
f_h1_small      = ImageFont.truetype(FP + "Poppins-Bold.ttf", 60)
f_sub           = ImageFont.truetype(FL + "LiberationSans-Regular.ttf", 36)
f_tag           = ImageFont.truetype(FP + "Poppins-Bold.ttf", 30)
f_num           = ImageFont.truetype(FP + "Poppins-Bold.ttf", 220)
f_step_title    = ImageFont.truetype(FP + "Poppins-Bold.ttf", 64)
f_step_body     = ImageFont.truetype(FL + "LiberationSans-Regular.ttf", 38)
f_btn           = ImageFont.truetype(FP + "Poppins-Bold.ttf", 34)

TOTAL = 9

# ============================================================
# SLIDE 1 — COVER
# ============================================================
img = base_canvas()
d = ImageDraw.Draw(img, "RGBA")
eyebrow(d, "VIZUROIU • CE FACEM", f_eyebrow, f_eyebrow_brand)

ty = 300
title_lines = ["CUM TRANSFORMĂM", "IDEILE ÎN REZULTATE,", "PAS CU PAS."]
for i, line in enumerate(title_lines):
    color = ACCENT2 if i == 2 else TEXT
    d.text((PAD, ty), line, font=f_h1, fill=color)
    ty += 92

ty += 30
sub = "Fiecare afacere e diferită, așa că nu lucrăm după un șablon rigid — construim împreună un proces care ți se potrivește."
for line in wrap(d, sub, f_sub, W - 2 * PAD - 60):
    d.text((PAD, ty), line, font=f_sub, fill=MUTED)
    ty += 50

# mini step-index preview strip
ty += 40
steps_preview = ["Analiză", "Mesaj", "Coaching", "Filmare", "Montaj", "Ads", "Optimizare"]
sx = PAD
f_prev = ImageFont.truetype(FP + "Poppins-Bold.ttf", 24)
for i, s in enumerate(steps_preview):
    label = f"{i+1:02d} {s}"
    lw = text_w(d, f_prev, label)
    if sx + lw > W - PAD:
        break
    d.rounded_rectangle([sx, ty, sx + lw + 28, ty + 46], radius=23, fill=SURFACE, outline=BORDER, width=2)
    d.text((sx + 14, ty + 10), label, font=f_prev, fill=MUTED)
    sx += lw + 28 + 16

slide_footer(d, f_logo, 1, TOTAL)
img.save(f"{OUT_DIR}/slide-1-cover.png")
print("saved slide 1")

# ============================================================
# SLIDES 2-8 — THE 7 STEPS
# ============================================================
STEPS = [
    ("01", "ANALIZĂ", "Strategie de conținut",
     "Analizăm businessul, publicul și concurența, apoi conturăm direcția: ce spunem, cui și prin ce mijloace."),
    ("02", "MESAJ", "Construirea mesajului",
     "Scriem scenariile și hook-ul potrivit. Fiecare cadru și fiecare replică are un rol clar în mesajul final."),
    ("03", "COACHING", "Coaching pentru cameră",
     "Lucrăm cu tine înainte de filmare — poziție, ritm, ton, privire — până comunici natural în fața obiectivului."),
    ("04", "FILMARE", "Producție foto / video",
     "Filmăm cu echipament profesional. Gândim fiecare unghi, cadru și detaliu de decor în funcție de mesaj."),
    ("05", "MONTAJ", "Editare și post-producție",
     "Montaj, sunet și subtitrări transformă materialul brut în conținut gata de publicat, pe fiecare platformă."),
    ("06", "ADS", "Social media ads",
     "Setăm și rulăm campaniile plătite. Definim audiența și alocăm bugetul acolo unde contează."),
    ("07", "OPTIMIZARE", "Analiză și optimizare",
     "Urmărim datele după publicare — engagement, conversii, cost per rezultat — și creștem ce aduce rezultate."),
]

for i, (num, tag, title, body) in enumerate(STEPS):
    img = base_canvas()
    d = ImageDraw.Draw(img, "RGBA")
    eyebrow(d, "VIZUROIU • CUM LUCRĂM", f_eyebrow, f_eyebrow_brand)

    # big outline number, top-right, like the site's stepnum stroke style
    nb = d.textbbox((0, 0), num, font=f_num)
    nw, nh = nb[2] - nb[0], nb[3] - nb[1]
    d.text((W - PAD - nw - 10, 210 - nb[1]), num, font=f_num, fill=None, stroke_width=3, stroke_fill=ACCENT)

    ty = 300
    d.rounded_rectangle([PAD, ty, PAD + text_w(d, f_tag, tag) + 32, ty + 50], radius=25, fill=SURFACE, outline=BORDER, width=2)
    d.text((PAD + 16, ty + 11), tag, font=f_tag, fill=ACCENT2)
    ty += 100

    d.text((PAD, ty), title, font=f_step_title, fill=TEXT)
    ty += 110

    for line in wrap(d, body, f_step_body, W - 2 * PAD - 40):
        d.text((PAD, ty), line, font=f_step_body, fill=MUTED)
        ty += 52

    # progress dots
    dot_y = H - 210
    dot_gap = 26
    total_dots_w = 7 * 14 + 6 * dot_gap
    dx = PAD
    for j in range(7):
        active = j == i
        r = 7 if active else 5
        color = ACCENT if active else BORDER
        d.ellipse([dx, dot_y - r, dx + 2 * r, dot_y + r], fill=color)
        dx += 14 + dot_gap

    slide_footer(d, f_logo, i + 2, TOTAL)
    img.save(f"{OUT_DIR}/slide-{i+2}-{tag.lower().replace(' ', '-')}.png")
    print("saved slide", i + 2, tag)

# ============================================================
# SLIDE 9 — BONUS + CTA
# ============================================================
img = base_canvas()
d = ImageDraw.Draw(img, "RGBA")
eyebrow(d, "VIZUROIU • BONUS", f_eyebrow, f_eyebrow_brand)

ty = 320
d.rounded_rectangle([PAD, ty, PAD + text_w(d, f_tag, "SUPORT CONTINUU") + 32, ty + 50], radius=25, fill=SURFACE, outline=BORDER, width=2)
d.text((PAD + 16, ty + 11), "SUPORT CONTINUU", font=f_tag, fill=ACCENT2)
ty += 110

for i, line in enumerate(["PRIMUL PAS", "E GRATUIT."]):
    color = ACCENT2 if i == 1 else TEXT
    d.text((PAD, ty), line, font=f_h1, fill=color)
    ty += 92

ty += 30
body = "Suntem la un mesaj distanță pe WhatsApp pentru orice idee sau ajustare. Programăm și un call lunar de consultanță, ca să vedem ce merge și cum evoluăm strategia. Primul pas — un audit, fără niciun angajament."
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

slide_footer(d, f_logo, 9, TOTAL)
img.save(f"{OUT_DIR}/slide-9-cta.png")
print("saved slide 9")
