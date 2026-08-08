"""Measure how closely each candidate font matches the constructed matrix glyphs.

Two targets, both taken from the mark's own geometry (Z1-U rev 2):
  * stroke / cap-height = 14 / 62 = 0.2258   (the glyphs are monoline stroke 14,
    and their ink height is 62 = 48 centreline + 2 x 7 half-stroke)
  * O aspect = 1.000                          (the O is a true circle, r24)

Stem width is measured by rasterising "H" and scanning a horizontal line near the
top of the glyph, above the crossbar, where only the two stems carry ink.
Cap height comes from the rasterised "H" ink box, which is what the eye actually
compares -- more reliable across these fonts than trusting OS/2 sCapHeight.

Writes fonts/metrics.json (consumed by matrix-font.html) and prints a ranked table.
"""
import glob
import json
import os

from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FONTS = os.path.join(ROOT, "fonts")

TARGET_STEM = 14 / 62      # 0.2258
TARGET_ASPECT = 1.0
PX = 400                   # rasterisation size; big enough that stems are many px wide


def ink_box(font, ch):
    img = Image.new("L", (PX * 3, PX * 3), 0)
    ImageDraw.Draw(img).text((PX // 2, PX // 2), ch, font=font, fill=255)
    return img, img.getbbox()


def measure(path):
    try:
        f = TTFont(path, lazy=True, fontNumber=0)
        names = {n.nameID: n.toUnicode() for n in f["name"].names if n.nameID in (1, 2, 16, 17)}
        family = names.get(16) or names.get(1)
        sub = names.get(17) or names.get(2)
        weight = f["OS/2"].usWeightClass
        f.close()
    except Exception as e:
        return {"file": os.path.basename(path), "error": str(e)}

    pil = ImageFont.truetype(path, PX)

    img_h, bb_h = ink_box(pil, "H")
    if not bb_h:
        return {"file": os.path.basename(path), "error": "no ink for H"}
    cap_px = bb_h[3] - bb_h[1]

    # scan above the crossbar: two separate stems there
    px = img_h.load()
    y = bb_h[1] + int(cap_px * 0.14)
    runs, run = [], 0
    for x in range(bb_h[0], bb_h[2]):
        if px[x, y] > 128:
            run += 1
        elif run:
            runs.append(run)
            run = 0
    if run:
        runs.append(run)
    stem_px = min(runs) if runs else 0

    _, bb_o = ink_box(pil, "O")
    o_w = bb_o[2] - bb_o[0] if bb_o else 0
    o_h = bb_o[3] - bb_o[1] if bb_o else 1

    return {
        "file": os.path.basename(path),
        "family": family,
        "sub": sub,
        "weight": weight,
        "capRatio": round(cap_px / PX, 4),          # cap height per em -> for sizing
        "stemRatio": round(stem_px / cap_px, 4) if cap_px else 0,
        "oAspect": round(o_w / o_h, 4) if o_h else 0,
        "nRuns": len(runs),
    }


rows = []
for p in sorted(glob.glob(os.path.join(FONTS, "*.ttf"))) + sorted(glob.glob(os.path.join(FONTS, "*.otf"))):
    r = measure(p)
    if "error" not in r and r["nRuns"] == 2:      # sanity: H must show exactly two stems
        r["stemErr"] = round(abs(r["stemRatio"] - TARGET_STEM), 4)
        r["aspErr"] = round(abs(r["oAspect"] - TARGET_ASPECT), 4)
        # combined: stroke weight and roundness weighted equally
        r["score"] = round(r["stemErr"] / TARGET_STEM + r["aspErr"], 4)
        rows.append(r)
    else:
        print("skip", r.get("file"), r.get("error") or f"H gave {r.get('nRuns')} runs")

with open(os.path.join(FONTS, "metrics.json"), "w") as fh:
    json.dump(rows, fh, indent=1)

print(f"\ntarget: stem/cap={TARGET_STEM:.4f}  O aspect={TARGET_ASPECT:.3f}\n")
print(f"{'family':30s} {'sub':10s} {'wt':>4s} {'stem/cap':>9s} {'Oaspect':>8s} {'score':>7s}")
print("-" * 76)
for r in sorted(rows, key=lambda r: r["score"])[:34]:
    print(f"{r['family'][:30]:30s} {str(r['sub'])[:10]:10s} {r['weight']:>4} "
          f"{r['stemRatio']:>9.3f} {r['oAspect']:>8.3f} {r['score']:>7.3f}")
