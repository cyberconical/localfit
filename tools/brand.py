"""Shared helpers for the store graphics: the font (Instrument Sans, bundled in fonts/) in the weights we need."""
import os
from PIL import ImageFont
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
_CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".font-cache")


def font(px, wght=700):
    os.makedirs(_CACHE, exist_ok=True)
    ttf = os.path.join(_CACHE, "instrument-%d.ttf" % wght)
    if not os.path.exists(ttf):
        f = TTFont(os.path.join(ROOT, "fonts", "instrument-sans-latin-wdth-normal.woff2"))
        f.flavor = None
        instancer.instantiateVariableFont(f, {"wght": wght, "wdth": 100}).save(ttf)
    return ImageFont.truetype(ttf, px)
