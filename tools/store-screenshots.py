#!/usr/bin/env python3
"""Store screenshots: one design, rendered for Google Play (1080x1920) and the App Store (1290x2796).

  python3 tools/store-screenshots.py

Input:  docs/screenshots/*.png (raw app screens, see tools/screenshots.js; map-* are screens with the offline basemap)
Output: docs/store/play/NN-name.png and docs/store/apple/NN-name.png

Layout (the usual best practice for store screenshots): a headline of a few words, one supporting line, the whole app screen
inside a neutral phone body below it (nothing cropped, no brand marks), same layout on every slide, black and white like the app.
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
    ("map-live.png", 0, "Your runs. Your map. Your data.", "Private, open-source training with GPS and an offline map.", True),
    ("map-route.png", 0, "Every route stays on your phone.", "Pace, splits and route. No account, no uploads, no feed.", False),
    ("map-routes.png", 0, "All your runs on one map.", "Offline and private. Nothing leaves your device.", False),
    ("setup.png", 0, "A plan in one minute.", "5 km to marathon, or just get fitter. Pick your week, Localfit builds the plan.", False),
    ("week.png", 0, "Run, lift, climb, stretch.", "One plan for every sport. Adjust any session.", False),
    ("stats.png", 0, "See what works.", "Pace trends, shoes, time of day. Calculated on your phone.", False),
    ("map-live-dark.png", 0, "Open source. No tracking. No ads.", "No account, no cloud. The code is on GitHub (GPL-3.0).", False),
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


def phone(src, sw):
    """The whole app screen inside a neutral phone body: dark case, thin rim, punch-hole camera. 4x supersampled."""
    k = 4
    sh = int(src.height * sw / src.width)
    bz = max(6, int(0.034 * sw))
    pw, ph = sw + 2 * bz, sh + 2 * bz
    R = int(0.13 * pw)
    big = Image.new("RGBA", (pw * k, ph * k), (0, 0, 0, 0))
    d = ImageDraw.Draw(big)
    side = int(0.012 * pw) * k          # hardware buttons, stick out of the case by a few pixels
    pad = side
    full = Image.new("RGBA", ((pw + 2 * int(0.012 * pw)) * k, ph * k), (0, 0, 0, 0))
    fd = ImageDraw.Draw(full)
    ox = pad
    fd.rounded_rectangle([ox, 0, ox + pw * k - 1, ph * k - 1], radius=R * k, fill=(92, 92, 96, 255))
    rim = max(2, int(0.006 * pw)) * k
    fd.rounded_rectangle([ox + rim, rim, ox + pw * k - 1 - rim, ph * k - 1 - rim], radius=R * k - rim, fill=(18, 18, 20, 255))
    for (y0, y1, left) in ((0.20, 0.27, False), (0.30, 0.42, False), (0.27, 0.36, True)):
        x0, x1 = (0, ox + rim) if left else (ox + pw * k - rim, ox + pw * k + side)
        fd.rounded_rectangle([x0, int(y0 * ph * k), x1, int(y1 * ph * k)], radius=side // 2, fill=(70, 70, 74, 255))
    sr = R * k - bz * k - rim
    sc = src.convert("RGB").resize((sw * k, sh * k), Image.LANCZOS)
    mask = Image.new("L", (sw * k, sh * k), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, sw * k - 1, sh * k - 1], radius=max(2, R * k - bz * k), fill=255)
    full.paste(sc, (ox + bz * k, bz * k), mask)
    # punch-hole camera
    cr = int(0.018 * pw) * k
    cx, cy = ox + pw * k // 2, (bz + int(0.026 * pw)) * k
    fd.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=(8, 8, 10, 255))
    return full.resize((full.width // k, full.height // k), Image.LANCZOS)


def render(name, crop, head, sub, hero, W, H):
    s = W / 1080.0
    img = Image.new("RGB", (W, H), (0, 0, 0))
    d = ImageDraw.Draw(img)
    margin = int(84 * s)
    y = int(0.058 * H)
    f_head, f_sub = brand.font(int(82 * s), 700), brand.font(int(38 * s), 400)
    for line in wrap(d, head, f_head, W - 2 * margin):
        d.text((margin, y), line, font=f_head, fill=(255, 255, 255))
        y += int(92 * s)
    y += int(12 * s)
    for line in wrap(d, sub, f_sub, W - 2 * margin):
        d.text((margin, y), line, font=f_sub, fill=(190, 190, 190))
        y += int(50 * s)
    # the whole app screen in a phone, centred in the space below the text
    src = Image.open(os.path.join(SRC, name)).convert("RGB")
    top = int(0.058 * H) + int((2 * 92 + 12 + 2 * 50 + 44) * s)   # same phone size and position on every slide
    bottom_gap = int(64 * s)
    avail = H - top - bottom_gap
    aspect = src.height / src.width
    # phone outer height = sw*aspect + 2*bezel, bezel = 0.034*sw
    sw = int(min(0.78 * W / 1.068, avail / (aspect + 0.068)))
    ph_img = phone(src, sw)
    x = (W - ph_img.width) // 2
    yy = top + (avail - ph_img.height) // 2
    img.paste(ph_img, (x, yy), ph_img)
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
