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

OUT_DIR = "branding/carusel-nevoie-agentie"
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

def section_tag(draw, x, y, label, f_tag):
    tw = text_w(draw, f_tag, label)
    draw.rounded_rectangle([x, y, x + tw + 32, y + 50], radius=25, fill=SURFACE, outline=BORDER, width=2)
    draw.text((x + 16, y + 11), label, font=f_tag, fill=ACCENT2)
    return y + 50

def progress_dots(draw, index, total):
    dot_y = H - 210
    dot_gap = 26
    dot_d = 14
    total_w = total * dot_d + (total - 1) * dot_gap
    dx = PAD
    for j in range(total):
        active = j == index
        r = 7 if active else 5
        color = ACCENT if active else BORDER
        draw.ellipse([dx, dot_y - r, dx + 2 * r, dot_y + r], fill=color)
        dx += dot_d + dot_gap

f_eyebrow       = ImageFont.truetype(FP + "Poppins-Bold.ttf", 28)
f_eyebrow_brand = ImageFont.truetype(MUSEO_PATH, 28)
f_logo          = ImageFont.truetype(MUSEO_PATH, 40)
f_tag           = ImageFont.truetype(FP + "Poppins-Bold.ttf", 30)
f_statement     = ImageFont.truetype(FP + "Poppins-Bold.ttf", 84)
f_h1_mid        = ImageFont.truetype(FP + "Poppins-Bold.ttf", 62)
f_sub           = ImageFont.truetype(FL + "LiberationSans-Regular.ttf", 38)
f_btn           = ImageFont.truetype(FP + "Poppins-Bold.ttf", 34)

TOTAL = 7

def statement_slide(idx, eyebrow_label, lines, highlight_idx, out_name):
    """lines: list of strings, wrapped manually. highlight_idx: index of line to color accent (or None)."""
    img = base_canvas()
    d = ImageDraw.Draw(img, "RGBA")
    eyebrow(d, eyebrow_label, f_eyebrow, f_eyebrow_brand)

    line_h = 96
    total_h = len(lines) * line_h
    ty = (H - total_h) // 2 - 40
    for i, line in enumerate(lines):
        color = ACCENT2 if i == highlight_idx else TEXT
        d.text((PAD, ty), line, font=f_statement, fill=color)
        ty += line_h

    progress_dots(d, idx, TOTAL)
    slide_footer(d, f_logo, idx + 1, TOTAL)
    img.save(f"{OUT_DIR}/{out_name}")
    print("saved", out_name)

def content_slide(idx, eyebrow_label, tag_label, title_lines, title_highlight, body, out_name):
    img = base_canvas()
    d = ImageDraw.Draw(img, "RGBA")
    eyebrow(d, eyebrow_label, f_eyebrow, f_eyebrow_brand)

    ty = 320
    ty = section_tag(d, PAD, ty, tag_label, f_tag) + 50

    for i, line in enumerate(title_lines):
        color = ACCENT2 if i == title_highlight else TEXT
        d.text((PAD, ty), line, font=f_h1_mid, fill=color)
        ty += 78

    ty += 30
    for line in wrap(d, body, f_sub, W - 2 * PAD - 40):
        d.text((PAD, ty), line, font=f_sub, fill=MUTED)
        ty += 50

    progress_dots(d, idx, TOTAL)
    slide_footer(d, f_logo, idx + 1, TOTAL)
    img.save(f"{OUT_DIR}/{out_name}")
    print("saved", out_name)

# ============================================================
# SLIDE 1 — HOOK
# ============================================================
statement_slide(
    0, "VIZUROIU • O ÎNTREBARE ONESTĂ",
    ["Nu mai poți crește", "doar cu postări", "făcute la întâmplare."],
    2, "slide-1-hook.png"
)

# ============================================================
# SLIDE 2 — NEVOIA DE CONȚINUT
# ============================================================
content_slide(
    1, "VIZUROIU • REALITATEA", "REALITATE",
    ["Rețelele sociale nu mai", "sunt loc de postat poze."], 1,
    "Sunt canal de vânzare. Dacă nu tratezi conținutul ca pe o investiție, pierzi teren în fața concurenței care o face.",
    "slide-2-realitate.png"
)

# ============================================================
# SLIDE 3 — NEVOIA DE O AGENȚIE
# ============================================================
content_slide(
    2, "VIZUROIU • TIMPUL TĂU", "TIMPUL TĂU",
    ["O agenție bună", "nu te încarcă,", "te eliberează."], 2,
    "Poți încerca singur — dar între filmat, montat, scris texte și rulat reclame, rămâne timp puțin pentru afacerea ta de bază.",
    "slide-3-timp.png"
)

# ============================================================
# SLIDE 4 — A DOUA ÎNTREBARE
# ============================================================
statement_slide(
    3, "VIZUROIU • ÎNTREBAREA",
    ["Dar cu ce agenție", "lucrezi?"],
    1, "slide-4-intrebare.png"
)

# ============================================================
# SLIDE 5 — MIZA ALEGERII GREȘITE
# ============================================================
content_slide(
    4, "VIZUROIU • RISCUL", "RISCUL",
    ["Alegi greșit o dată,", "pierzi bani și timp."], 1,
    'Ai văzut zeci de agenții. Toate promit "conținut de calitate" și "creștere garantată". Alegi greșit a doua oară, îți pierzi încrederea.',
    "slide-5-risc.png"
)

# ============================================================
# SLIDE 6 — REFRAME
# ============================================================
content_slide(
    5, "VIZUROIU • CE CONTEAZĂ", "CE CONTEAZĂ",
    ["Nu ai nevoie de o", "agenție care promite."], 1,
    "Ai nevoie de una care îți arată exact ce a făcut, cum lucrează și ce rezultate a obținut — înainte să semnezi ceva.",
    "slide-6-reframe.png"
)

# ============================================================
# SLIDE 7 — CTA
# ============================================================
img = base_canvas()
d = ImageDraw.Draw(img, "RGBA")
eyebrow(d, "VIZUROIU • AUDIT GRATUIT", f_eyebrow, f_eyebrow_brand)

ty = 320
ty = section_tag(d, PAD, ty, "AUDIT GRATUIT", f_tag) + 50

for i, line in enumerate(["Vezi tot,", "înainte să decizi."]):
    color = ACCENT2 if i == 1 else TEXT
    d.text((PAD, ty), line, font=f_h1_mid, fill=color)
    ty += 78

ty += 30
body = "Portofoliul real, procesul în 7 pași, cifrele — tot ce ai nevoie ca să decizi în cunoștință de cauză."
for line in wrap(d, body, f_sub, W - 2 * PAD - 40):
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

progress_dots(d, 6, TOTAL)
slide_footer(d, f_logo, 7, TOTAL)
img.save(f"{OUT_DIR}/slide-7-cta.png")
print("saved slide-7-cta.png")
