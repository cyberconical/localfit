#!/usr/bin/env python3
"""Localfit app icon: three white steps, one sport each (yoga, bouldering, running), on black.

One drawing, used by the CI build (Android launcher icons) and for the store graphics.

  python3 tools/icons.py android <path to android/app/src/main/res>
  python3 tools/icons.py store   <output folder>        # icon-512.png (Google Play) and icon-1024.png (App Store)

Needs: pip install pillow
"""
import os
import sys
from PIL import Image, ImageDraw

SS = 4  # supersampling for smooth edges


def _stroke(d, pts, w, fill):
    """A polyline with round caps and joins (circles stamped along it)."""
    for a, b in zip(pts, pts[1:]):
        steps = max(2, int(((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5 / (w * 0.15)))
        for i in range(steps + 1):
            x = a[0] + (b[0] - a[0]) * i / steps
            y = a[1] + (b[1] - a[1]) * i / steps
            d.ellipse([x - w / 2, y - w / 2, x + w / 2, y + w / 2], fill=fill)


def _dot(d, c, r, fill):
    d.ellipse([c[0] - r, c[1] - r, c[0] + r, c[1] + r], fill=fill)


def _figures(d, bx, by, s, P, U):
    """Three pictograms, one per step, drawn as holes (0) into the white boxes. Coordinates are 0..1 inside a box."""
    def Z(x, y):
        return P(bx + x * s, by + y * s)

    def fig(segs, head, w):
        _dot(d, Z(head[0], head[1]), head[2] * s * U, 0)
        for pts in segs:
            _stroke(d, [Z(*p) for p in pts], w * s * U, 0)
    return fig, Z


def glyph(size, fill, bg=(0, 0, 0, 255)):
    """The mark, centred, taking `fill` (0..1) of the canvas width. bg=None gives a transparent background.

    Three white steps climbing to the top right, one sport per step: yoga, bouldering, running.
    The pictograms are cut out of the boxes, so on a transparent canvas they show whatever lies behind.
    """
    n = size * SS
    g = n * fill
    x0 = (n - g) / 2
    y0 = (n - g) / 2
    u = g / 100.0

    def P(x, y):
        return (x0 + x * u, y0 + y * u)

    m = Image.new("L", (n, n), 0)
    d = ImageDraw.Draw(m)
    s = 32
    pos = [(5, 63), (34, 34), (63, 5)]
    for (x, y) in pos:
        a, b = P(x, y), P(x + s, y + s)
        d.rounded_rectangle([a[0], a[1], b[0], b[1]], radius=6.5 * u, fill=255)
    # yoga: tree pose
    fig, Z = _figures(d, pos[0][0], pos[0][1], s, P, u)
    fig([[(.50, .46), (.50, .66)], [(.50, .50), (.27, .32), (.50, .06)], [(.50, .50), (.73, .32), (.50, .06)],
         [(.50, .66), (.50, .92)], [(.50, .66), (.76, .74), (.52, .80)]], (.50, .31, .075), .09)
    # bouldering: hands and feet on holds, two free holds
    fig, Z = _figures(d, pos[1][0], pos[1][1], s, P, u)
    fig([[(.46, .36), (.48, .62)], [(.46, .40), (.62, .30), (.74, .14)], [(.46, .44), (.32, .52), (.22, .44)],
         [(.48, .62), (.68, .66), (.68, .82)], [(.48, .62), (.36, .78), (.36, .92)]], (.38, .22, .085), .095)
    for hx, hy in ((.74, .14), (.22, .44), (.68, .82), (.36, .92)):
        _dot(d, Z(hx, hy), .068 * s * u, 0)
    for hx, hy in ((.86, .46), (.14, .70)):
        _dot(d, Z(hx, hy), .05 * s * u, 0)
    # running
    fig, Z = _figures(d, pos[2][0], pos[2][1], s, P, u)
    fig([[(.52, .36), (.42, .62)], [(.52, .40), (.70, .50), (.80, .42)], [(.52, .40), (.34, .44), (.26, .56)],
         [(.42, .62), (.62, .68), (.60, .88)], [(.42, .62), (.28, .78), (.12, .74)]], (.60, .18, .095), .105)

    im = Image.new("RGBA", (n, n), bg if bg else (0, 0, 0, 0))
    im.paste(Image.new("RGBA", (n, n), (255, 255, 255, 255)), (0, 0), m)
    return im.resize((size, size), Image.LANCZOS)


def android(res):
    black = (0, 0, 0, 255)
    sizes = {"mdpi": (48, 108), "hdpi": (72, 162), "xhdpi": (96, 216), "xxhdpi": (144, 324), "xxxhdpi": (192, 432)}
    for name, (legacy, fg) in sizes.items():
        d = os.path.join(res, "mipmap-" + name)
        os.makedirs(d, exist_ok=True)
        # adaptive icon foreground: transparent, the mark inside the 66 % safe zone of the 108 dp canvas
        f = glyph(fg, 0.50, bg=None)
        f.save(os.path.join(d, "ic_launcher_foreground.png"))
        glyph(legacy, 0.80).save(os.path.join(d, "ic_launcher.png"))
        big = glyph(legacy * SS, 0.72)
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
    glyph(512, 0.72).convert("RGB").save(os.path.join(out, "icon-512.png"))
    glyph(1024, 0.72).convert("RGB").save(os.path.join(out, "icon-1024.png"))


if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] not in ("android", "store"):
        sys.exit(__doc__)
    (android if sys.argv[1] == "android" else store)(sys.argv[2])
    print("done")
