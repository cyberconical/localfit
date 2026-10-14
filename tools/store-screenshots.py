#!/usr/bin/env python3
"""Store screenshots: one design, rendered for Google Play (1080x1920) and the App Store (1290x2796).

  python3 tools/store-screenshots.py

Input:  docs/screenshots/*.png (raw app screens, see tools/screenshots.js; map-* are screens with the offline basemap)
Output: docs/store/play/NN-name.png and docs/store/apple/NN-name.png

Layout (the usual best practice for store screenshots): a headline of a few words, one supporting line, the app screen
below it cropped by the bottom edge, same position on every slide, black and white like the app.
Google Play requires the long side to be at most twice the short side, so its set is 9:16; Apple's 6.9" size is
1290x2796 and Apple scales it down for smaller phones.

Needs: pip install pillow fonttools brotli
"""
import os
import sys
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import brand  # noqa: E402
import icons  # noqa: E402

ROOT = os.path.join(HERE, "..")
SRC = os.path.join(ROOT, "docs", "screenshots")
OUT = os.path.join(ROOT, "docs", "store")

# (file, crop top in source pixels at the source's own width 540 for map-*, headline, supporting line, hero)
SLIDES = [
    ("map-live.png", 372, "Your runs. Your map. Your data.", "Private, open-source training with GPS and an offline map.", True),
    ("map-route.png", 120, "Every route stays on your phone.", "Pace, splits and route. No account, no uploads, no feed.", False),
    ("map-routes.png", 0, "All your runs on one map.", "Offline and private. Nothing leaves your device.", False),
    ("setup.png", 0, "A plan in one minute.", "5 km to marathon, or just get fitter. Pick your week, Localfit builds the plan.", False),
    ("week.png", 0, "Run, lift, climb, stretch.", "One plan for every sport. Adjust any session.", False),
    ("stats.png", 0, "See what works.", "Pace trends, shoes, time of day. Calculated on your phone.", False),
    ("map-live-dark.png", 372, "Open source. No tracking. No ads.", "No account, no cloud. The code is on GitHub (GPL-3.0).", False),
]
SIZES = {"play": (1080, 1920), "apple": (1290, 2796)}


def wrap(draw, text, font, width):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    lines.append(cur)
    return lines


def render(name, crop, head, sub, hero, W, H):
    s = W / 1080.0
    img = Image.new("RGB", (W, H), (0, 0, 0))
    d = ImageDraw.Draw(img)
    margin = int(84 * s)
    y = int(0.058 * H)
    if hero:
        m = int(150 * s)
        mark = icons.glyph(m, 0.80, bg=None)
        img.paste(mark, (margin - int(14 * s), y), mark)
        y += m + int(34 * s)
    f_head, f_sub = brand.font(int(90 * s), 700), brand.font(int(40 * s), 400)
    for line in wrap(d, head, f_head, W - 2 * margin):
        d.text((margin, y), line, font=f_head, fill=(255, 255, 255))
        y += int(100 * s)
    y += int(14 * s)
    for line in wrap(d, sub, f_sub, W - 2 * margin):
        d.text((margin, y), line, font=f_sub, fill=(190, 190, 190))
        y += int(54 * s)
    # the app screen, cropped by the bottom edge
    src = Image.open(os.path.join(SRC, name)).convert("RGB")
    if crop:
        src = src.crop((0, crop, src.width, src.height))
    pw = int(0.80 * W)
    ph = int(src.height * pw / src.width)
    shot = src.resize((pw, ph), Image.LANCZOS)
    top = int(643 * s)          # same distance from the top, in proportion to the width, on every size
    x = (W - pw) // 2
    rad = int(0.075 * pw)
    mask = Image.new("L", (pw, ph), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, pw - 1, ph + rad], radius=rad, fill=255)
    bw = max(3, int(5 * s))
    d.rounded_rectangle([x - bw, top - bw, x + pw + bw, H + rad], radius=rad + bw, fill=(70, 70, 70))
    img.paste(shot, (x, top), mask)
    return img


def main():
    for k, (W, H) in SIZES.items():
        out = os.path.join(OUT, k)
        os.makedirs(out, exist_ok=True)
        for f in os.listdir(out):
            if f.endswith(".png"):
                os.remove(os.path.join(out, f))
        for i, (name, crop, head, sub, hero) in enumerate(SLIDES, 1):
            render(name, crop, head, sub, hero, W, H).save(os.path.join(out, "%02d-%s" % (i, name.replace("map-", "").replace(".png", "") + ".png")))
        print(k, len(SLIDES), "slides", W, "x", H)


if __name__ == "__main__":
    main()
