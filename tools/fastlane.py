#!/usr/bin/env python3
"""Store texts and images in the fastlane layout that F-Droid reads from the source repository.

  python3 tools/fastlane.py

Reads docs/store/listing.md (texts) and docs/store/ (images), writes fastlane/metadata/android/en-US/.
Run it after changing the listing or the store images (tools/store-graphics.py, tools/store-screenshots.py).
"""
import os
import re
import shutil

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
STORE = os.path.join(ROOT, "docs", "store")
OUT = os.path.join(ROOT, "fastlane", "metadata", "android", "en-US")


def section(text, heading):
    m = re.search(r"^## " + re.escape(heading) + r".*?\n\n(.*?)(?=\n## |\Z)", text, re.S | re.M)
    if not m:
        raise SystemExit("section not found in listing.md: " + heading)
    return m.group(1).strip() + "\n"


listing = open(os.path.join(STORE, "listing.md"), encoding="utf-8").read()
shutil.rmtree(os.path.join(OUT, "images"), ignore_errors=True)   # changelogs/ (written by hand, one file per versionCode) stays
os.makedirs(os.path.join(OUT, "images", "phoneScreenshots"))
open(os.path.join(OUT, "title.txt"), "w", encoding="utf-8").write(section(listing, "App name"))
open(os.path.join(OUT, "short_description.txt"), "w", encoding="utf-8").write(section(listing, "Short description"))
open(os.path.join(OUT, "full_description.txt"), "w", encoding="utf-8").write(section(listing, "Full description"))
shutil.copy(os.path.join(STORE, "icon-512.png"), os.path.join(OUT, "images", "icon.png"))
shutil.copy(os.path.join(STORE, "feature-graphic-1024x500.png"), os.path.join(OUT, "images", "featureGraphic.png"))
shots = sorted(f for f in os.listdir(os.path.join(STORE, "play")) if f.endswith(".png"))
for i, f in enumerate(shots, 1):
    shutil.copy(os.path.join(STORE, "play", f), os.path.join(OUT, "images", "phoneScreenshots", "%d.png" % i))
print("fastlane metadata:", len(shots), "screenshots ->", os.path.relpath(OUT, ROOT))
