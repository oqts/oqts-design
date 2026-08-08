"""Classify each face's capital Q as 'crossing' or not.

Alec's criterion: the tail should run from about the middle of the circle to just
outside it -- i.e. the same construction as the mark, whose tail goes from
(c+8,c+8) to (c+24,c+24) on a bowl of r24.

Test, done on the raster rather than by eye:
  1. Render O; its ink box gives the bowl centre and outer radius, and a scan
     through the centre row gives the stroke width, hence the counter radius.
  2. Render Q at the same size and anchor. Count ink inside 0.85 * counter radius.
     A tail that merely hangs off the ring leaves that region empty; a crossing
     tail fills part of it.
  3. Measure how far the ink reaches past the outer radius, so a tail that drops
     into a long descender can be told apart from one stopping just outside.
"""
import glob
import json
import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FONTS = os.path.join(ROOT, "fonts")
PX, CANVAS = 300, 900


def render(path, ch, size):
    img = Image.new("L", (CANVAS, CANVAS), 0)
    ImageDraw.Draw(img).text((CANVAS // 2, CANVAS // 2), ch,
                             font=ImageFont.truetype(path, size), fill=255, anchor="mm")
    return img


def classify(path):
    o = render(path, "O", PX)
    bb = o.getbbox()
    if not bb:
        return None
    cx, cy = (bb[0] + bb[2]) / 2, (bb[1] + bb[3]) / 2
    rx, ry = (bb[2] - bb[0]) / 2, (bb[3] - bb[1]) / 2

    # stroke width from a scan through the centre row of the O
    px = o.load()
    runs, run = [], 0
    for x in range(bb[0], bb[2]):
        if px[x, int(cy)] > 128:
            run += 1
        elif run:
            runs.append(run)
            run = 0
    if run:
        runs.append(run)
    if len(runs) != 2:
        return None
    stroke = sum(runs) / 2
    counter_r = max(rx - stroke, 4)

    q = render(path, "Q", PX)
    qpx = q.load()
    qbb = q.getbbox()

    inside = total = 0
    for y in range(int(cy - counter_r), int(cy + counter_r)):
        for x in range(int(cx - counter_r), int(cx + counter_r)):
            if math.hypot(x - cx, y - cy) <= counter_r * 0.85:
                total += 1
                if qpx[x, y] > 128:
                    inside += 1
    fill = inside / total if total else 0

    # furthest ink from centre, as a multiple of the outer radius
    far = 0.0
    for y in range(qbb[1], qbb[3]):
        for x in range(qbb[0], qbb[2]):
            if qpx[x, y] > 128:
                far = max(far, math.hypot((x - cx) / rx, (y - cy) / ry))

    return {"counterFill": round(fill, 4), "reach": round(far, 3),
            "crossing": fill > 0.02 and far > 1.02}


out = {}
for p in sorted(glob.glob(os.path.join(FONTS, "*.ttf"))):
    r = classify(p)
    if r:
        out[os.path.basename(p)] = r

with open(os.path.join(FONTS, "qshape.json"), "w") as fh:
    json.dump(out, fh, indent=1)

metrics = {m["file"]: m for m in json.load(open(os.path.join(FONTS, "metrics.json")))}
rows = []
for f, r in out.items():
    m = metrics.get(f)
    if not m:
        continue
    rows.append((r["crossing"], m["family"], m["sub"], m["weight"],
                 r["counterFill"], r["reach"], m["oAspect"], m["stemRatio"]))

print(f"{'X':2s} {'family':26s} {'sub':10s} {'wt':>4s} {'fill':>6s} {'reach':>6s} {'Oasp':>6s} {'stem':>6s}")
print("-" * 74)
for r in sorted(rows, key=lambda r: (not r[0], abs(r[6] - 1.0))):
    print(f"{'*' if r[0] else ' ':2s} {r[1][:26]:26s} {str(r[2])[:10]:10s} {r[3]:>4} "
          f"{r[4]:>6.3f} {r[5]:>6.2f} {r[6]:>6.3f} {r[7]:>6.3f}")
