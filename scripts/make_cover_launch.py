from PIL import Image, ImageDraw, ImageFont, ImageFilter

BG        = (11, 12, 16)
BORDER    = (36, 40, 55)
TEXT      = (244, 245, 247)
MUTED     = (170, 176, 190)
ACCENT    = (255, 84, 54)
ACCENT2   = (255, 154, 60)

FP = "/usr/share/fonts/truetype/google-fonts/"
FL = "/usr/share/fonts/truetype/liberation2/"

HIGHLIGHT = {"VIZUROIU.RO"}

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
            c = hl_color if w.upper().strip(".,") in HIGHLIGHT else color
            draw.text((x, y), w, font=font, fill=c)
            x += text_w(draw, font, w) + space_w
        y += line_h
    return y

def draw_logo(draw, x, y, font_logo, dot_color=ACCENT, text_color=TEXT):
    draw.text((x, y), "VIZUROIU", font=font_logo, fill=text_color)
    lw = text_w(draw, font_logo, "VIZUROIU")
    draw.text((x+lw+4, y), ".", font=font_logo, fill=dot_color)
    return lw

TITLE = "BINE AI VENIT PE VIZUROIU.RO"

PARA_1 = ("De când am început Vizuroiu Media, ne-am dorit să arătăm cine suntem cu adevărat. "
          "Povestea noastră, procesul din spatele fiecărui proiect, rezultatele pe care le obținem, "
          "valorile în care credem și ceea ce ne diferențiază.")
PARA_2 = ("După aproape o lună de muncă, am lansat un site care reflectă exact ceea ce facem "
          "și modul în care lucrăm.")

# ============================================================
# HORIZONTAL 2560x1440
# ============================================================
W, H = 2560, 1440
f_eyebrow = ImageFont.truetype(FP + "Poppins-Bold.ttf", 30)
f_title   = ImageFont.truetype(FP + "Poppins-Bold.ttf", 82)
f_body    = ImageFont.truetype(FL + "LiberationSans-Regular.ttf", 38)
f_logo    = ImageFont.truetype(FP + "Poppins-Bold.ttf", 44)

img = Image.new("RGB", (W, H), BG)
rgba = img.convert("RGBA")
glow1 = radial_glow(1500, ACCENT, 65)
rgba.alpha_composite(glow1, (W-1150, -520))
glow2 = radial_glow(1300, ACCENT2, 40)
rgba.alpha_composite(glow2, (-550, H-780))
img = rgba.convert("RGB")

draw = ImageDraw.Draw(img, "RGBA")
PAD = 130
max_w = W - 2*PAD

ex, ey = PAD, 100
draw.rectangle([ex, ey+15, ex+56, ey+19], fill=ACCENT)
draw.text((ex+72, ey), "VIZUROIU  •  LANSARE OFICIALĂ", font=f_eyebrow, fill=ACCENT)

title_lines = wrap_words(draw, TITLE, f_title, max_w)
block_title_h = len(title_lines) * 100

p1_lines = wrap(draw, PARA_1, f_body, max_w)
p2_lines = wrap(draw, PARA_2, f_body, max_w)
body_line_h = 56
block_body_h = len(p1_lines)*body_line_h + 34 + len(p2_lines)*body_line_h

total_block = block_title_h + 26 + 46 + block_body_h
region_top, region_bottom = 260, H - 190
ty = region_top + max(0, (region_bottom - region_top - total_block)//2)

ty = draw_title_mixed(draw, (PAD, ty), TITLE, f_title, max_w, 100)
ty += 26
draw.rectangle([PAD, ty, PAD+100, ty+6], fill=ACCENT)
ty += 46

for l in p1_lines:
    draw.text((PAD, ty), l, font=f_body, fill=MUTED)
    ty += body_line_h
ty += 34
for l in p2_lines:
    draw.text((PAD, ty), l, font=f_body, fill=MUTED)
    ty += body_line_h

foot_y = H - 110
draw.line([(PAD, foot_y), (W-PAD, foot_y)], fill=BORDER, width=2)
draw_logo(draw, PAD, foot_y+26, f_logo)
tag = "VIZUROIU.RO"
tw = text_w(draw, f_logo, tag)
draw.text((W-PAD-tw, foot_y+26), tag, font=f_logo, fill=ACCENT2)

img.save("vizuroiu-cover-07-lansare.png", "PNG")
print("saved horizontal launch cover")

# ============================================================
# VERTICAL 1080x1920
# ============================================================
W2, H2 = 1080, 1920
f_eyebrow_v = ImageFont.truetype(FP + "Poppins-Bold.ttf", 26)
f_title_v   = ImageFont.truetype(FP + "Poppins-Bold.ttf", 62)
f_body_v    = ImageFont.truetype(FL + "LiberationSans-Regular.ttf", 34)
f_logo_v    = ImageFont.truetype(FP + "Poppins-Bold.ttf", 36)

img2 = Image.new("RGB", (W2, H2), BG)
rgba2 = img2.convert("RGBA")
glow1v = radial_glow(1200, ACCENT, 65)
rgba2.alpha_composite(glow1v, (-450, -420))
glow2v = radial_glow(1100, ACCENT2, 40)
rgba2.alpha_composite(glow2v, (W2-650, H2-620))
img2 = rgba2.convert("RGB")

draw2 = ImageDraw.Draw(img2, "RGBA")
PAD2 = 80
max_w2 = W2 - 2*PAD2

ex2, ey2 = PAD2, 100
draw2.rectangle([ex2, ey2+13, ex2+48, ey2+16], fill=ACCENT)
draw2.text((ex2+62, ey2), "VIZUROIU  •  LANSARE", font=f_eyebrow_v, fill=ACCENT)

title_lines2 = wrap_words(draw2, TITLE, f_title_v, max_w2)
block_title_h2 = len(title_lines2) * 76

p1_lines2 = wrap(draw2, PARA_1, f_body_v, max_w2)
p2_lines2 = wrap(draw2, PARA_2, f_body_v, max_w2)
body_line_h2 = 50
block_body_h2 = len(p1_lines2)*body_line_h2 + 32 + len(p2_lines2)*body_line_h2

total_block2 = block_title_h2 + 26 + 42 + block_body_h2
region_top2, region_bottom2 = 260, H2 - 200
ty2 = region_top2 + max(0, (region_bottom2 - region_top2 - total_block2)//2)

ty2 = draw_title_mixed(draw2, (PAD2, ty2), TITLE, f_title_v, max_w2, 76)
ty2 += 26
draw2.rectangle([PAD2, ty2, PAD2+90, ty2+6], fill=ACCENT)
ty2 += 42

for l in p1_lines2:
    draw2.text((PAD2, ty2), l, font=f_body_v, fill=MUTED)
    ty2 += body_line_h2
ty2 += 32
for l in p2_lines2:
    draw2.text((PAD2, ty2), l, font=f_body_v, fill=MUTED)
    ty2 += body_line_h2

foot_y2 = H2 - 130
draw2.line([(PAD2, foot_y2), (W2-PAD2, foot_y2)], fill=BORDER, width=2)
draw_logo(draw2, PAD2, foot_y2+30, f_logo_v)
tag2 = "VIZUROIU.RO"
tw2 = text_w(draw2, f_logo_v, tag2)
draw2.text((W2-PAD2-tw2, foot_y2+30), tag2, font=f_logo_v, fill=ACCENT2)

img2.save("vizuroiu-cover-vert-07-lansare.png", "PNG")
print("saved vertical launch cover")
