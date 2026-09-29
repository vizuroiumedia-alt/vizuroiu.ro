from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random

BG        = (11, 12, 16)
BG2       = (16, 18, 24)
SURFACE   = (22, 25, 34)
BORDER    = (36, 40, 55)
TEXT      = (244, 245, 247)
MUTED     = (154, 160, 176)
ACCENT    = (255, 84, 54)
ACCENT2   = (255, 154, 60)

FP = "/usr/share/fonts/truetype/google-fonts/"
FL = "/usr/share/fonts/truetype/liberation2/"
PHOTO = "img/fondatori-vizuroiu-media.jpg"

random.seed(7)

def text_w(draw, font, s):
    bbox = draw.textbbox((0, 0), s, font=font)
    return bbox[2] - bbox[0]

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

def build_site_mockup(W, H):
    """Recreates a stylized mock of the vizuroiu.html hero/site (to be blurred)."""
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im, "RGBA")

    # browser chrome bar
    chrome_h = int(H*0.052)
    d.rectangle([0, 0, W, chrome_h], fill=BG2)
    dotr = int(chrome_h*0.16)
    cx = int(W*0.02)
    for i, c in enumerate([(255,95,86),(255,189,46),(39,201,63)]):
        d.ellipse([cx, chrome_h//2-dotr, cx+2*dotr, chrome_h//2+dotr], fill=c)
        cx += int(dotr*3.2)
    bar_x0 = int(W*0.34); bar_x1 = int(W*0.66)
    d.rounded_rectangle([bar_x0, int(chrome_h*0.28), bar_x1, int(chrome_h*0.72)], radius=chrome_h//3, fill=SURFACE)

    y = chrome_h
    # nav bar
    nav_h = int(H*0.075)
    d.rectangle([0, y, W, y+nav_h], fill=BG)
    d.line([(0, y+nav_h), (W, y+nav_h)], fill=BORDER, width=2)
    # logo block
    lx = int(W*0.045)
    d.rectangle([lx, y+nav_h//2-14, lx+150, y+nav_h//2+14], fill=TEXT)
    d.ellipse([lx+158, y+nav_h//2-8, lx+174, y+nav_h//2+8], fill=ACCENT)
    # nav links
    nxx = int(W*0.42)
    for i in range(5):
        lw = 70 + (i%3)*20
        d.rounded_rectangle([nxx, y+nav_h//2-8, nxx+lw, y+nav_h//2+8], radius=6, fill=MUTED+(140,))
        nxx += lw + 34
    # cta button
    btn_w = int(W*0.12)
    d.rounded_rectangle([W-int(W*0.045)-btn_w, y+nav_h//2-24, W-int(W*0.045), y+nav_h//2+24],
                         radius=24, fill=ACCENT)
    y += nav_h

    # hero section
    hero_h = int(H*0.46)
    d.rectangle([0, y, W, y+hero_h], fill=BG)
    # glow accent top-right of hero
    glow = Image.new("RGBA", (int(W*0.5), int(W*0.5)), (0,0,0,0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse([0,0,glow.size[0],glow.size[1]], fill=ACCENT+(70,))
    glow = glow.filter(ImageFilter.GaussianBlur(80))
    im.paste(Image.alpha_composite(im.crop((W-glow.size[0], y, W, y+glow.size[1])).convert("RGBA"), glow).convert("RGB"),
             (W-glow.size[0], y))

    padx = int(W*0.045)
    ty = y + int(hero_h*0.16)
    # eyebrow
    d.rounded_rectangle([padx, ty, padx+220, ty+34], radius=8, fill=ACCENT+(200,))
    ty += 70
    # headline lines (blocky)
    for wfrac in (0.42, 0.30, 0.36):
        lw = int(W*wfrac)
        lh = int(H*0.052)
        d.rounded_rectangle([padx, ty, padx+lw, ty+lh], radius=10, fill=TEXT)
        ty += lh + int(H*0.018)
    ty += int(H*0.02)
    # lead paragraph lines
    for wfrac in (0.34, 0.26):
        lw = int(W*wfrac)
        lh = int(H*0.018)
        d.rounded_rectangle([padx, ty, padx+lw, ty+lh], radius=6, fill=MUTED+(160,))
        ty += lh + int(H*0.012)
    ty += int(H*0.03)
    # buttons
    bw, bh = int(W*0.14), int(H*0.05)
    d.rounded_rectangle([padx, ty, padx+bw, ty+bh], radius=bh//2, fill=ACCENT)
    d.rounded_rectangle([padx+bw+24, ty, padx+bw+24+int(bw*0.78), ty+bh], radius=bh//2, outline=BORDER, width=3)

    # hero photo (right)
    photo = Image.open(PHOTO).convert("RGB")
    ph_w = int(W*0.40)
    ph_h = int(hero_h*0.82)
    photo = fit_cover(photo, ph_w, ph_h)
    px = W - int(W*0.045) - ph_w
    py = y + int(hero_h*0.09)
    im.paste(photo, (px, py))

    y += hero_h

    # clients marquee strip
    strip_h = int(H*0.10)
    d.rectangle([0, y, W, y+strip_h], fill=BG2)
    d.line([(0, y), (W, y)], fill=BORDER, width=2)
    d.line([(0, y+strip_h), (W, y+strip_h)], fill=BORDER, width=2)
    cx = int(W*0.03)
    card_h = int(strip_h*0.5)
    while cx < W - int(W*0.03):
        cw = random.randint(int(W*0.045), int(W*0.075))
        d.rounded_rectangle([cx, y+(strip_h-card_h)//2, cx+cw, y+(strip_h+card_h)//2],
                             radius=10, fill=SURFACE, outline=BORDER, width=2)
        cx += cw + int(W*0.018)
    y += strip_h

    # remaining body content (portfolio grid blocks)
    rest_h = H - y
    d.rectangle([0, y, W, H], fill=BG)
    gx, gy = int(W*0.045), y+int(rest_h*0.12)
    gap = int(W*0.018)
    cell_w = (W - 2*gx - 5*gap)//6
    cell_h = int(rest_h*0.30)
    for i in range(6):
        cxx = gx + i*(cell_w+gap)
        d.rounded_rectangle([cxx, gy, cxx+cell_w, gy+cell_h], radius=14, fill=SURFACE, outline=BORDER, width=2)

    return im

def draw_logo(draw, x, y, font_logo, dot_color=ACCENT, text_color=TEXT):
    draw.text((x, y), "VIZUROIU", font=font_logo, fill=text_color)
    lw = text_w(draw, font_logo, "VIZUROIU")
    draw.text((x+lw+4, y), ".", font=font_logo, fill=dot_color)
    return lw

def make_teaser(W, H, out_name, sizes):
    base = build_site_mockup(W, H)
    blurred = base.filter(ImageFilter.GaussianBlur(sizes["blur"]))

    # dark scrim for contrast/legibility
    scrim = Image.new("RGBA", (W, H), (11, 12, 16, sizes["scrim_alpha"]))
    img = Image.alpha_composite(blurred.convert("RGBA"), scrim).convert("RGB")

    # extra centered vignette glow behind text
    vg = Image.new("RGBA", (W, H), (0,0,0,0))
    vgd = ImageDraw.Draw(vg)
    vgd.ellipse([W*0.5-sizes["vignette_r"], H*0.5-sizes["vignette_r"],
                 W*0.5+sizes["vignette_r"], H*0.5+sizes["vignette_r"]],
                fill=(11,12,16,150))
    vg = vg.filter(ImageFilter.GaussianBlur(120))
    img = Image.alpha_composite(img.convert("RGBA"), vg).convert("RGB")

    draw = ImageDraw.Draw(img, "RGBA")

    f_eyebrow = ImageFont.truetype(FP + "Poppins-Bold.ttf", sizes["eyebrow"])
    f_big     = ImageFont.truetype(FP + "Poppins-Bold.ttf", sizes["big"])
    f_date    = ImageFont.truetype(FP + "Poppins-Bold.ttf", sizes["date"])
    f_sub     = ImageFont.truetype(FL + "LiberationSans-Regular.ttf", sizes["sub"])
    f_logo    = ImageFont.truetype(FP + "Poppins-Bold.ttf", sizes["logo"])

    PAD = sizes["pad"]

    # eyebrow top-left
    ex, ey = PAD, sizes["eyebrow_y"]
    draw.rectangle([ex, ey+15, ex+56, ey+19], fill=ACCENT)
    draw.text((ex+72, ey), "VIZUROIU  •  ÎN CURÂND", font=f_eyebrow, fill=ACCENT)

    # centered big teaser text
    line1 = "LANSAREA"
    line2 = "14 AUGUST"
    w1 = text_w(draw, f_big, line1)
    w2 = text_w(draw, f_date, line2)
    cy = sizes["center_y"]
    draw.text(((W-w1)//2, cy), line1, font=f_big, fill=TEXT)
    cy += sizes["big_gap"]
    draw.text(((W-w2)//2, cy), line2, font=f_date, fill=None, stroke_width=4, stroke_fill=ACCENT2)
    cy += sizes["date_gap"]

    # keyword strip to anchor the lower empty space
    if "keywords_y" in sizes:
        f_kw = ImageFont.truetype(FP + "Poppins-Bold.ttf", sizes["kw_size"])
        kw_text = "PORTOFOLIU   •   REZULTATE   •   PROCES   •   BRANDING"
        kww = text_w(draw, f_kw, kw_text)
        draw.text(((W-kww)//2, sizes["keywords_y"]), kw_text, font=f_kw, fill=MUTED+(90,))
        # accent dot row
        dot_y = sizes["keywords_y"] - 40
        dot_gap = 26
        total_dots_w = 5*10 + 4*dot_gap
        dx = (W-total_dots_w)//2
        for i in range(5):
            draw.ellipse([dx, dot_y, dx+10, dot_y+10], fill=(ACCENT if i==2 else BORDER))
            dx += 10+dot_gap

    # footer
    foot_y = H - sizes["foot_offset"]
    draw.line([(PAD, foot_y), (W-PAD, foot_y)], fill=BORDER, width=2)
    draw_logo(draw, PAD, foot_y+sizes["foot_pad"], f_logo)
    tag = "VIZUROIU.RO"
    tw = text_w(draw, f_logo, tag)
    draw.text((W-PAD-tw, foot_y+sizes["foot_pad"]), tag, font=f_logo, fill=ACCENT2)

    img.save(out_name, "PNG")
    print("saved", out_name)

# HORIZONTAL 2560x1440
make_teaser(2560, 1440, "vizuroiu-cover-08-teaser.png", dict(
    blur=34, scrim_alpha=150, vignette_r=780,
    eyebrow=30, big=150, date=140, sub=36, logo=44,
    pad=110, eyebrow_y=90, center_y=520, big_gap=168, date_gap=178,
    foot_offset=110, foot_pad=26,
    keywords_y=1190, kw_size=26,
))

# VERTICAL 1080x1920
make_teaser(1080, 1920, "vizuroiu-cover-vert-08-teaser.png", dict(
    blur=26, scrim_alpha=160, vignette_r=620,
    eyebrow=26, big=112, date=104, sub=32, logo=36,
    pad=80, eyebrow_y=90, center_y=880, big_gap=136, date_gap=144,
    foot_offset=130, foot_pad=30,
    keywords_y=1610, kw_size=22,
))
