#!/usr/bin/env python3
"""Draws the Google Play graphics into docs/store/: icon 512x512 and feature graphic 1024x500.

Needs: pip install pillow fonttools brotli
Run from the repository root: python3 tools/store-graphics.py
The motif is the same as the launcher icon the CI build draws (a line towards a finish bar, with ticks).
"""
import os
from PIL import Image, ImageDraw, ImageFont
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
OUT = os.path.join(ROOT, "docs", "store")
os.makedirs(OUT, exist_ok=True)


def motif(size, safe):
    im = Image.new("RGBA", (size, size), (0, 0, 0, 255))
    d = ImageDraw.Draw(im)
    m = size * (1 - safe) / 2
    x0, x1, cy = m, size - m, size / 2
    w = x1 - x0
    th = size * 0.075
    d.rectangle([x0, cy - th / 2, x0 + w * 0.7, cy + th / 2], fill="white")
    d.rectangle([x0 + w * 0.7, cy - th / 6, x1, cy + th / 6], fill="white")
    for k in (0, 5, 10, 15, 20):
        x = x0 + w * k / 21.1
        d.rectangle([x - size * 0.007, cy + th * 0.9, x + size * 0.007, cy + th * 1.9], fill="white")
    d.rectangle([x1 - size * 0.014, cy - size * 0.2, x1 + size * 0.014, cy + th * 1.9], fill="white")
    return im


def bold_font(px):
    ttf = os.path.join(OUT, ".instrument-bold.ttf")
    if not os.path.exists(ttf):
        f = TTFont(os.path.join(ROOT, "fonts", "instrument-sans-latin-wdth-normal.woff2"))
        f.flavor = None
        f = instancer.instantiateVariableFont(f, {"wght": 700, "wdth": 100})
        f.save(ttf)
    return ImageFont.truetype(ttf, px)


# Icon: Google Play adds its own rounded mask, so the image is a full square.
motif(512, 0.74).convert("RGB").save(os.path.join(OUT, "icon-512.png"))

# Feature graphic
W, H = 1024, 500
im = Image.new("RGB", (W, H), "black")
d = ImageDraw.Draw(im)
big = bold_font(120)
small = bold_font(34)
d.text((72, 120), "Localfit", font=big, fill="white")
d.text((78, 270), "Local-first training plans.", font=small, fill="white")
d.text((78, 316), "No account, no tracking, no cloud.", font=small, fill=(190, 190, 190))
# the line towards the finish bar along the bottom
y = 430
d.rectangle([72, y - 7, 72 + (W - 144) * 0.7, y + 7], fill="white")
d.rectangle([72 + (W - 144) * 0.7, y - 2, W - 72, y + 2], fill="white")
d.rectangle([W - 72 - 3, y - 40, W - 72 + 3, y + 22], fill="white")
for k in range(0, 21, 5):
    x = 72 + (W - 144) * k / 21.1
    d.rectangle([x - 2, y + 12, x + 2, y + 34], fill="white")
im.save(os.path.join(OUT, "feature-graphic-1024x500.png"))
os.remove(os.path.join(OUT, ".instrument-bold.ttf"))
print("written to", OUT)
