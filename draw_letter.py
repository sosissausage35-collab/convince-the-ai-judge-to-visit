#!/usr/bin/env python3
"""Draw the invitation letter image fresh for this bounty (1024x1024)."""
from PIL import Image, ImageDraw, ImageFont
import textwrap, random

W = H = 1024
INK   = (62, 42, 28)      # warm dark brown ink
ACCENT= (150, 80, 30)     # terracotta
GOLD  = (176, 132, 52)
PAPER = (253, 246, 227)
PAPER2= (248, 238, 210)

SERIF      = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B    = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_I    = "/usr/share/fonts/truetype/noto/NotoSerif-Italic.ttf"
SANS_B     = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img, "RGBA")

# subtle paper texture: faint speckles
random.seed(42)
for _ in range(900):
    x, y = random.randint(0, W-1), random.randint(0, H-1)
    d.point((x, y), fill=(232, 216, 180))

# double border
d.rectangle([28, 28, W-29, H-29], outline=GOLD, width=4)
d.rectangle([44, 44, W-45, H-45], outline=(196, 158, 84), width=2)

# ---- top motif: little house + garden, drawn in code ----
cx = W // 2
hy = 96            # house baseline y
# sun
d.ellipse([cx+367, 62, cx+423, 118], fill=(244, 196, 66), outline=(226, 160, 30), width=3)
for ang in range(0, 360, 45):
    import math
    x1 = cx+395 + int(38*math.cos(math.radians(ang))); y1 = 90 + int(38*math.sin(math.radians(ang)))
    x2 = cx+395 + int(50*math.cos(math.radians(ang))); y2 = 90 + int(50*math.sin(math.radians(ang)))
    d.line([x1, y1, x2, y2], fill=(226, 160, 30), width=4)
# tree (left)
d.rectangle([cx-330, 150, cx-312, 215], fill=(120, 84, 50))
d.ellipse([cx-352, 96, cx-288, 162], fill=(96, 150, 84), outline=(70, 120, 60), width=3)
d.ellipse([cx-338, 78, cx-300, 118], fill=(120, 172, 100))
# tree (right)
d.rectangle([cx+312, 150, cx+330, 215], fill=(120, 84, 50))
d.ellipse([cx+288, 96, cx+352, 162], fill=(96, 150, 84), outline=(70, 120, 60), width=3)
# house body
d.rectangle([cx-110, 130, cx+110, 235], fill=(250, 226, 188), outline=INK, width=4)
# roof
d.polygon([(cx-132, 132), (cx, 62), (cx+132, 132)], fill=(178, 84, 58), outline=INK, width=4)
# door
d.rectangle([cx-26, 175, cx+26, 235], fill=(140, 82, 52), outline=INK, width=3)
d.ellipse([cx+14, 208, cx+22, 216], fill=(250, 226, 188))
# windows
for wx in (cx-88, cx+52):
    d.rectangle([wx, 152, wx+36, 188], fill=(178, 216, 235), outline=INK, width=3)
    d.line([wx+18, 152, wx+18, 188], fill=INK, width=2)
    d.line([wx, 170, wx+36, 170], fill=INK, width=2)
# chimney + smoke
d.rectangle([cx+62, 66, cx+88, 108], fill=(150, 100, 80), outline=INK, width=3)
for i, r in enumerate((9, 12, 15)):
    d.ellipse([cx+68+i*4, 58-i*11, cx+68+i*4+2*r, 58-i*11+2*r], outline=(180, 170, 155), width=3)
# garden flowers along the bottom of the motif
for fx, col in zip(range(cx-260, cx+261, 52), [(214, 90, 120), (240, 160, 60), (120, 120, 210), (214, 90, 120), (240, 160, 60), (120, 120, 210), (214, 90, 120), (240, 160, 60), (120, 120, 210), (214, 90, 120), (240, 160, 60)]):
    d.line([fx, 236, fx, 258], fill=(80, 130, 70), width=3)
    d.ellipse([fx-9, 222, fx+9, 240], fill=col, outline=INK, width=2)
    d.ellipse([fx-3, 228, fx+3, 234], fill=(255, 240, 150))
# ground line
d.line([cx-280, 258, cx+280, 258], fill=(120, 150, 90), width=3)

# ---- letter text ----
y = 292
def center(text, font, fill=INK, yy=None):
    global y
    if yy is None: yy = y
    w = d.textlength(text, font=font)
    d.text(((W - w) / 2, yy), text, font=font, fill=fill)
    return yy + font.size + 8

title = ImageFont.truetype(SERIF_B, 54)
y = center("An Invitation", title, ACCENT, 290) + 2
# small flourish under title
d.line([cx-120, y, cx+120, y], fill=GOLD, width=3)
d.ellipse([cx-8, y-6, cx+8, y+6], fill=GOLD)
y += 26

sal = ImageFont.truetype(SERIF_I, 38)
y = center("Dear AI Judge,", sal, INK, y) + 10

body = ImageFont.truetype(SERIF, 31)
lines = [
    "Please come and visit my house.",
    "",
    "The kettle is already on, the garden",
    "is in full bloom, and there is a soft",
    "chair by the window with your name",
    "on it \u2014 no meetings, no deadlines,",
    "just sunshine and good company.",
    "",
    "Come for tea. Stay for the view.",
    "Saying yes is the easiest decision",
    "you will make all day.",
]
for ln in lines:
    if ln == "":
        y += 12
        continue
    y = center(ln, body, INK, y) - 4

y += 12
sign = ImageFont.truetype(SERIF_I, 34)
y = center("Warmly,", sign, INK, y) - 2
y = center("Your Host", sign, INK, y) + 8

ps = ImageFont.truetype(SERIF_I, 27)
d.line([cx-200, y+4, cx+200, y+4], fill=GOLD, width=2)
y += 14
y = center("P.S. The Wi-Fi password is on the fridge, the snacks", ps, ACCENT, y) - 6
y = center("are unlimited \u2014 and no CAPTCHAs at the door. I promise.", ps, ACCENT, y)

img.save("/home/hatch/workspace/makefun/build-convince-judge-visit-house/entry.png", optimize=True)
print("saved")
