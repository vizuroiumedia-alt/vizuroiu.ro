from PIL import Image, ImageDraw, ImageFont

BG_PAGE = (18, 19, 24)
FP = "/usr/share/fonts/truetype/google-fonts/"
FL = "/usr/share/fonts/truetype/liberation2/"

COLORS = [
    ("#0B0C10", (11, 12, 16),  "Fundal principal",        ""),
    ("#101218", (16, 18, 24),  "Fundal secundar",         ""),
    ("#161922", (22, 25, 34),  "Suprafață (carduri)",     ""),
    ("#242837", (36, 40, 55),  "Bordură / linii",         ""),
    ("#F4F5F7", (244, 245, 247), "Text principal",        "recomandat pt. subtitrare clară"),
    ("#9AA0B0", (154, 160, 176), "Text secundar / muted", "recomandat pt. subtitrare discretă"),
    ("#FF5436", (255, 84, 54),   "Accent 1",              "recomandat pt. cuvinte-cheie"),
    ("#FF9A3C", (255, 154, 60),  "Accent 2",              "recomandat pt. accent secundar"),
]

W = 1000
row_h = 130
swatch_w = 170
pad = 40
H = pad * 2 + row_h * len(COLORS)

img = Image.new("RGB", (W, H), BG_PAGE)
d = ImageDraw.Draw(img)

f_hex   = ImageFont.truetype(FP + "Poppins-Bold.ttf", 34)
f_label = ImageFont.truetype(FP + "Poppins-Bold.ttf", 26)
f_note  = ImageFont.truetype(FL + "LiberationSans-Italic.ttf", 22)

y = pad
for hexcode, rgb, label, note in COLORS:
    d.rounded_rectangle([pad, y, pad + swatch_w, y + row_h - 24], radius=16, fill=rgb, outline=(60, 63, 75), width=1)

    tx = pad + swatch_w + 36
    # pick readable text color depending on swatch brightness for the hex label chip (not needed, text drawn outside swatch)
    d.text((tx, y + 4), hexcode, font=f_hex, fill=(244, 245, 247))
    d.text((tx, y + 46), label, font=f_label, fill=(154, 160, 176))
    if note:
        d.text((tx, y + 78), note, font=f_note, fill=(120, 125, 138))

    y += row_h

img.save("branding/paleta-culori-vizuroiu.png", "PNG")
print("saved")
