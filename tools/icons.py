#!/usr/bin/env python3
"""Localfit app icon: a white "L" that is also a route, ending in a position marker, on black.

One drawing, used by the CI build (Android launcher icons) and for the store graphics.

  python3 tools/icons.py android <path to android/app/src/main/res>
  python3 tools/icons.py store   <output folder>        # icon-512.png (Google Play) and icon-1024.png (App Store)

Needs: pip install pillow
"""
import os
import sys
from PIL import Image, ImageDraw

SS = 4  # supersampling for smooth edges


def glyph(size, fill, bg=(0, 0, 0, 255)):
    """The mark, centred, taking `fill` (0..1) of the canvas width. bg=None gives a transparent background."""
    n = size * SS
    im = Image.new("RGBA", (n, n), bg if bg else (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    g = n * fill            # glyph box edge in px
    x0 = (n - g) / 2
    y0 = (n - g) / 2
    u = g / 100.0           # one unit of the 100 x 100 glyph box

    def P(x, y):
        return (x0 + x * u, y0 + y * u)

    w = 16 * u              # stroke width
    white = (255, 255, 255, 255)
    top = P(8, 8)
    corner = P(8, 78)
    end = P(78, 78)
    # the L as one polygon (square corner), plus a round cap at the top
    left, right = corner[0] - w / 2, corner[0] + w / 2
    d.polygon([(left, top[1]), (right, top[1]), (right, corner[1] - w / 2), (end[0], corner[1] - w / 2),
               (end[0], corner[1] + w / 2), (left, corner[1] + w / 2)], fill=white)
    d.ellipse([top[0] - w / 2, top[1] - w / 2, top[0] + w / 2, top[1] + w / 2], fill=white)
    # the position marker: ring at the end of the route
    r_out, r_in = 22 * u, 9 * u
    d.ellipse([end[0] - r_out, end[1] - r_out, end[0] + r_out, end[1] + r_out], fill=white)
    d.ellipse([end[0] - r_in, end[1] - r_in, end[0] + r_in, end[1] + r_in], fill=(0, 0, 0, 255) if bg else (0, 0, 0, 0))
    return im.resize((size, size), Image.LANCZOS)


def android(res):
    black = (0, 0, 0, 255)
    sizes = {"mdpi": (48, 108), "hdpi": (72, 162), "xhdpi": (96, 216), "xxhdpi": (144, 324), "xxxhdpi": (192, 432)}
    for name, (legacy, fg) in sizes.items():
        d = os.path.join(res, "mipmap-" + name)
        os.makedirs(d, exist_ok=True)
        # adaptive icon foreground: transparent, the mark inside the 66 % safe zone of the 108 dp canvas
        f = glyph(fg, 0.50, bg=None)
        # the hole of the ring must show the black background layer, so cut it transparent (done in glyph)
        f.save(os.path.join(d, "ic_launcher_foreground.png"))
        glyph(legacy, 0.56).save(os.path.join(d, "ic_launcher.png"))
        big = glyph(legacy * SS, 0.52)
        mask = Image.new("L", big.size, 0)
        ImageDraw.Draw(mask).ellipse([0, 0, big.size[0] - 1, big.size[1] - 1], fill=255)
        big.putalpha(mask)
        big.resize((legacy, legacy), Image.LANCZOS).save(os.path.join(d, "ic_launcher_round.png"))
    vd = os.path.join(res, "values")
    os.makedirs(vd, exist_ok=True)
    with open(os.path.join(vd, "ic_launcher_background.xml"), "w") as f:
        f.write('<?xml version="1.0" encoding="utf-8"?>\n<resources>\n    <color name="ic_launcher_background">#000000</color>\n</resources>\n')


def store(out):
    os.makedirs(out, exist_ok=True)
    # Google Play and the App Store apply their own mask, so these are full squares without transparency
    glyph(512, 0.52).convert("RGB").save(os.path.join(out, "icon-512.png"))
    glyph(1024, 0.52).convert("RGB").save(os.path.join(out, "icon-1024.png"))


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] not in ("android", "store"):
        sys.exit(__doc__)
    (android if sys.argv[1] == "android" else store)(sys.argv[2])
    print("done")
