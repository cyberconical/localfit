#!/usr/bin/env python3
"""Store graphics into docs/store/: icons (512 Play, 1024 App Store), the feature graphic 1024x500 and the logo with the name.

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

def tight(size_w):
    """The mark cropped to its own bounds and scaled to a given width (transparent background)."""
    g = icons.glyph(2000, 1.0, bg=None)
    g = g.crop(g.getbbox())
    return g.resize((size_w, int(g.height * size_w / g.width)), Image.LANCZOS)


def fit_text(d, text, width, wght=700):
    """Largest font size at which the text is `width` px wide."""
    lo, hi = 20, 600
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if d.textlength(text, font=bold_font(mid, wght)) > width:
            hi = mid
        else:
            lo = mid
    return bold_font(lo, wght)


# Feature graphic: mark on the left, name and promise on the right
W, H = 1024, 500
im = Image.new("RGB", (W, H), "black")
mark = tight(330)
im.paste(mark, (60, (H - mark.height) // 2), mark)
d = ImageDraw.Draw(im)
f = fit_text(d, "LocalFit", 520)
d.text((440, 70), "LocalFit", font=f, fill="white")
d.text((444, 245), "Your runs. Your routes. Your phone.", font=bold_font(32, 600), fill="white")
d.text((444, 300), "Private and open source.", font=bold_font(32, 400), fill=(190, 190, 190))
d.text((444, 342), "No account, no tracking, no cloud.", font=bold_font(32, 400), fill=(190, 190, 190))
im.save(os.path.join(OUT, "feature-graphic-1024x500.png"))

# Logo with the name, for the README and the web: square, black; the name is exactly as wide as the steps
L = 1200
logo = Image.new("RGB", (L, L), "black")
m = tight(800)
d = ImageDraw.Draw(logo)
f = fit_text(d, "LocalFit", 800)
th = f.getbbox("LocalFit")[3]
gap = 70
top = (L - (m.height + gap + th)) // 2
logo.paste(m, ((L - 800) // 2, top), m)
d.text(((L - 800) // 2, top + m.height + gap - f.getbbox("L")[1] // 2), "LocalFit", font=f, fill="white")
logo.save(os.path.join(OUT, "logo.png"))
print("written to", OUT)
