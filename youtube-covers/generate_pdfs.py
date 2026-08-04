#!/usr/bin/env python3
import os, subprocess, time

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
COVERS_DIR = os.path.dirname(os.path.abspath(__file__))
LOGOS_DIR = os.path.join(COVERS_DIR, "logos")
OUT_DIR = "/Users/admin/Documents/vizuroiumedia.net/colaboratori logo"

CLIENTS = [
    ("Numa Cafe",          "numa-cafe.png",          "color"),
    ("Pizzeria Arena",     "pizzeria-arena.png",      "color"),
    ("Metalift",           "metalift.jpg",            "color"),
    ("CONAF",              "conaf.webp",              "color"),
    ("Hotel LaRocca",      "hotel-larocca.webp",      "color"),
    ("Autentic Gift",      "autentic-gift.png",       "color"),
    ("Autentic DDD",       "autentic-ddd.png",        "color"),
    ("Casa Ferrara",       "casa-ferrara.png",        "color"),
    ("Ciugulin Mob",       "ciugulin-mob.png",        "color"),
    ("Tabiet Good Food",   "tabiet-good-food.png",    "color"),
    ("Anemona Hotel",      "anemona-hotel.png",       "color"),
    ("Airport House",      "airport-house.jpg",       "color"),
    ("Craiova Events",     "craiova-events.png",      "color"),
    ("Ten Million Romania","ten-million.png",          "invert"),
    ("CCIABR",             "cciabr.png",              "color"),
    ("Restaurant Reset",   "restaurant-reset.webp",   "color"),
    ("AG Tiny House",      "ag-tiny-house.svg",       "invert"),
    ("Braila Imobiliare",  "braila-imobiliare.png",   "color"),
    ("Animall Delta",      "animall-delta.webp",      "color"),
    ("ONE Automobile",     "one-automobile.jpg",      "round"),
    ("Prontoo Pizza",      "prontoo-pizza.png",       "color"),
    ("Diego",              "diego.png",               "invert"),
]

HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1280px;height:720px;overflow:hidden}}
body{{
  background:#0B0C10;
  display:flex;
  align-items:center;
  justify-content:center;
  position:relative;
}}
body::before{{
  content:"";
  position:absolute;
  top:-80px;left:-80px;
  width:600px;height:600px;
  background:radial-gradient(circle,rgba(255,84,54,.22),transparent 65%);
  filter:blur(20px);
}}
body::after{{
  content:"";
  position:absolute;
  bottom:-100px;right:-60px;
  width:500px;height:500px;
  background:radial-gradient(circle,rgba(255,154,60,.14),transparent 65%);
  filter:blur(24px);
}}
img{{
  max-width:580px;
  max-height:340px;
  object-fit:contain;
  position:relative;
  z-index:1;
  {img_style}
}}
.wm{{
  position:absolute;
  bottom:24px;right:28px;
  font-family:system-ui,sans-serif;
  font-size:14px;
  font-weight:700;
  color:rgba(255,255,255,.18);
  letter-spacing:.04em;
  z-index:2;
}}
.wm span{{color:rgba(255,84,54,.35)}}
</style>
</head>
<body>
  <img src="file://{logo_path}" alt="{name}">
  <div class="wm">Vizuroiumedia<span>.</span></div>
</body>
</html>"""

def img_style(mode):
    if mode == "invert":
        return "filter:brightness(0) invert(1);"
    if mode == "round":
        return "border-radius:50%;width:280px;height:280px;max-width:none;max-height:none;object-fit:cover;"
    return ""

os.makedirs(OUT_DIR, exist_ok=True)

for name, logo_file, mode in CLIENTS:
    logo_path = os.path.join(LOGOS_DIR, logo_file)
    if not os.path.exists(logo_path):
        print(f"  SKIP (logo missing): {name}")
        continue

    html_content = HTML_TEMPLATE.format(
        name=name,
        logo_path=logo_path,
        img_style=img_style(mode),
    )

    html_path = os.path.join(COVERS_DIR, "_tmp_cover.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    safe_name = name.replace(" ", "_").replace("/", "-")
    pdf_path = os.path.join(OUT_DIR, f"{safe_name}.pdf")

    cmd = [
        CHROME,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--disable-web-security",
        f"--print-to-pdf={pdf_path}",
        "--no-margins",
        "--paper-width=13.33",
        "--paper-height=7.5",
        f"file://{html_path}",
    ]

    print(f"  Generez: {name}...")
    result = subprocess.run(cmd, capture_output=True, timeout=30)
    if os.path.exists(pdf_path):
        print(f"  OK -> {safe_name}.pdf")
    else:
        print(f"  EROARE: {name}")
        print(result.stderr.decode()[:300])

    time.sleep(0.5)

# cleanup
if os.path.exists(html_path):
    os.remove(html_path)

print("\nDone! PDF-urile sunt in:", OUT_DIR)
