#!/usr/bin/env python3
"""Store graphics into docs/store/: icons (512 Play, 1024 App Store) and the feature graphic 1024x500.

Needs: pip install pillow fonttools brotli
Run from the repository root: python3 tools/store-graphics.py
"""
import os
import sys
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import brand  # noqa: E402
import icons  # noqa: E402

ROOT = os.path.join(HERE, "..")
OUT = os.path.join(ROOT, "docs", "store")
os.makedirs(OUT, exist_ok=True)


bold_font = lambda px, wght=700: brand.font(px, wght)


icons.store(OUT)

# Feature graphic: mark on the left, name and promise on the right
W, H = 1024, 500
im = Image.new("RGB", (W, H), "black")
mark = icons.glyph(300, 0.80).convert("RGB")
im.paste(mark, (70, 100))
d = ImageDraw.Draw(im)
d.text((400, 120), "Localfit", font=bold_font(110), fill="white")
d.text((404, 262), "Your runs. Your routes. Your phone.", font=bold_font(32, 600), fill="white")
d.text((404, 312), "Private and open source.", font=bold_font(32, 400), fill=(190, 190, 190))
d.text((404, 352), "No account, no tracking, no cloud.", font=bold_font(32, 400), fill=(190, 190, 190))
im.save(os.path.join(OUT, "feature-graphic-1024x500.png"))
print("written to", OUT)
