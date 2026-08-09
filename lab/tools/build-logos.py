"""Generate the production OQTS logo set from the finalised spec.

Locked spec (Alec, 2026-08-08):
  face      Latin Modern Mono -- matrix letters in Light 10 Bold, wordmark in 10 Regular
  size      wordmark ink height = 70% of the bracket height
  gap       50 units between bracket and wordmark
  track     0.090 em letter-spacing on the wordmark
  spread    100 units centre-to-centre between matrix letters

Every glyph is converted to an OUTLINE, so the artwork carries no font dependency
and renders identically everywhere. Latin Modern is under the GUST Font License,
which permits this.
"""
import os

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)                     # design/lab
DESIGN = os.path.dirname(ROOT)                   # design
FONTS = os.path.join(ROOT, "fonts")              # the full type library
OUT = os.path.join(DESIGN, "assets", "logo")     # production SVGs
os.makedirs(OUT, exist_ok=True)

# ---- locked spec ----
H = 216.0            # bracket ink height, the mark's reference dimension
CENTRE = 140.0       # centre of the bracket in pre-scale coords: (40+240)/2
SPREAD = 100.0      # centre-to-centre distance between matrix letters
CAP_U = 62.0         # cap height of the matrix letters, in pre-scale units
BR = 16.0 / 14.0     # bracket stroke : glyph stem, inherited from the drawn mark
FILL, GAP, TRACK, LH = 0.70, 50.0, 0.090, 1.30

MARK_FONT = os.path.join(FONTS, "lmm-lmmonolt10-bold.otf")
TEXT_FONT = os.path.join(FONTS, "lmm-lmmono10-regular.otf")
MARK_STEM, TEXT_CAP = 0.1352, 0.61          # measured by tools/analyse-fonts.py

NAVY, PAPER, WHITE = "#002147", "#F4EDDC", "#FFFFFF"
IVORY = "#FBF8F1"   # the page ground; the default baked background
LINES = ["OXFORD", "QUANTITATIVE", "TRADING SOCIETY"]


class Face:
    def __init__(self, path, cap_ratio):
        self.tt = TTFont(path, lazy=True)
        self.gs = self.tt.getGlyphSet()
        self.upem = self.tt["head"].unitsPerEm
        self.cmap = self.tt.getBestCmap()
        self.hmtx = self.tt["hmtx"]
        self.cap = cap_ratio * self.upem       # cap height in font units

    def name(self, ch):
        return self.cmap[ord(ch)]

    def advance(self, ch):
        return self.hmtx[self.name(ch)][0]

    def path(self, ch):
        pen = SVGPathPen(self.gs)
        self.gs[self.name(ch)].draw(pen)
        return pen.getCommands()


mark_face = Face(MARK_FONT, 0.61)
text_face = Face(TEXT_FONT, TEXT_CAP)


def glyph_path(face, ch, size_cap, x, baseline_y, centre_on_advance=True):
    """Place one glyph as an outlined <path>, cap height scaled to size_cap."""
    s = size_cap / face.cap
    dx = x - (face.advance(ch) * s / 2 if centre_on_advance else 0)
    d = face.path(ch)
    if not d:
        return ""
    return (f'<path d="{d}" transform="translate({dx:.3f},{baseline_y:.3f}) '
            f'scale({s:.6f},{-s:.6f})"/>')


def string_paths(face, text, size_cap, x, baseline_y, tracking):
    """Lay out a string as outlines, honouring letter-spacing. Returns (svg, width)."""
    s = size_cap / face.cap
    out, cx = [], x
    for ch in text:
        if ch != " ":
            d = face.path(ch)
            if d:
                out.append(f'<path d="{d}" transform="translate({cx:.3f},{baseline_y:.3f}) '
                           f'scale({s:.6f},{-s:.6f})"/>')
        cx += face.advance(ch) * s + tracking
    return "".join(out), cx - tracking - x


def build_mark(colour):
    """The bracketed matrix. Returns (svg fragment, width, height) with ink at 0,0."""
    stem = MARK_STEM * CAP_U
    w = stem * BR
    tick = 22.0 * (w / 16.0)
    edge = 40.0 - w / 2.0
    k = H / (200.0 + w)
    d = SPREAD / 2.0

    brackets = (f'<g fill="none" stroke="{colour}" stroke-width="{w:.3f}">'
                f'<path d="M {40+tick:.2f} 40 L 40 40 L 40 240 L {40+tick:.2f} 240"/>'
                f'<path d="M {240-tick:.2f} 40 L 240 40 L 240 240 L {240-tick:.2f} 240"/></g>')

    cells = [("O", CENTRE - d, CENTRE - d), ("Q", CENTRE + d, CENTRE - d),
             ("T", CENTRE - d, CENTRE + d), ("S", CENTRE + d, CENTRE + d)]
    glyphs = "".join(glyph_path(mark_face, ch, CAP_U, cx, cy + CAP_U / 2.0)
                     for ch, cx, cy in cells)

    frag = (f'<g transform="scale({k:.6f}) translate({-edge:.3f},{-edge:.3f})">'
            f'{brackets}<g fill="{colour}">{glyphs}</g></g>')
    return frag, H, H


def wordmark_metrics():
    fs_cap = (H * FILL) / (2 * LH + TEXT_CAP) * TEXT_CAP   # cap height in units
    fs_em = fs_cap / TEXT_CAP                              # nominal em size
    L = LH * fs_em
    y0 = H / 2.0 - (2 * L - fs_cap) / 2.0
    return fs_cap, fs_em, L, y0


def build_wordmark(colour, x0, tracking_scale=None):
    fs_cap, fs_em, L, y0 = wordmark_metrics()
    track = TRACK * fs_em
    parts, widest = [], 0.0
    for i, line in enumerate(LINES):
        svg, wdt = string_paths(text_face, line, fs_cap, x0, y0 + i * L, track)
        parts.append(svg)
        widest = max(widest, wdt)
    return f'<g fill="{colour}">{"".join(parts)}</g>', widest, y0, L, fs_cap


def svg_doc(body, w, h, bg=None, title=""):
    rect = f'<rect width="{w:.2f}" height="{h:.2f}" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.2f} {h:.2f}" '
            f'width="{w:.2f}" height="{h:.2f}" role="img" aria-label="{title}">'
            f"<!-- {title}. Latin Modern Mono, outlined. Spec: size {int(FILL*100)}%, "
            f"gap {int(GAP)}, track {TRACK}, spread {int(SPREAD)}. -->"
            f"{rect}{body}</svg>")


PAD = 16.0        # breathing room on transparent files
PAD_BG = 40.0     # generous clear space when a background is baked in
CIRCLE_KEEP = 0.92  # circlesafe: ink diagonal held to 92% of the crop circle
written = []


def pad_for(bg):
    return PAD_BG if bg else PAD


def write(name, body, w, h, bg, title):
    path = os.path.join(OUT, name)
    with open(path, "w") as fh:
        fh.write(svg_doc(body, w, h, bg, title) + "\n")
    written.append((name, f"{w:.0f}x{h:.0f}"))


# ---------- 1. mark only ----------
for suffix, colour, bg in [("", NAVY, None), ("-reverse", PAPER, None),
                           ("-on-ivory", NAVY, IVORY), ("-on-paper", NAVY, PAPER),
                           ("-on-white", NAVY, WHITE), ("-on-navy", PAPER, NAVY)]:
    p = pad_for(bg)
    frag, w, h = build_mark(colour)
    body = f'<g transform="translate({p},{p})">{frag}</g>'
    write(f"oqts-mark{suffix}.svg", body, w + 2 * p, h + 2 * p, bg, "OQTS mark")

# circlesafe mark: opaque ground, ink diagonal cleared for a circular crop
for suffix, colour, bg in [("-on-white-circlesafe", NAVY, WHITE),
                           ("-on-ivory-circlesafe", NAVY, IVORY),
                           ("-on-paper-circlesafe", NAVY, PAPER),
                           ("-on-navy-circlesafe", PAPER, NAVY)]:
    frag, w, h = build_mark(colour)
    side = h * 2 ** 0.5 / CIRCLE_KEEP
    p = (side - h) / 2.0
    body = f'<g transform="translate({p:.3f},{p:.3f})">{frag}</g>'
    write(f"oqts-mark{suffix}.svg", body, side, side, bg, "OQTS mark")

# ---------- 2. horizontal lockup ----------
for suffix, colour, bg in [("", NAVY, None), ("-reverse", PAPER, None),
                           ("-on-ivory", NAVY, IVORY), ("-on-paper", NAVY, PAPER),
                           ("-on-white", NAVY, WHITE), ("-on-navy", PAPER, NAVY)]:
    p = pad_for(bg)
    frag, mw, mh = build_mark(colour)
    x0 = H + GAP
    wm, wmw, y0, L, fs_cap = build_wordmark(colour, x0)
    total_w = x0 + wmw
    body = f'<g transform="translate({p},{p})">{frag}{wm}</g>'
    write(f"oqts-lockup{suffix}.svg", body, total_w + 2 * p, mh + 2 * p, bg,
          "OQTS horizontal lockup")

# ---------- 3. stacked lockup ----------
for suffix, colour, bg in [("", NAVY, None), ("-reverse", PAPER, None),
                           ("-on-ivory", NAVY, IVORY), ("-on-navy", PAPER, NAVY)]:
    p = pad_for(bg)
    frag, mw, mh = build_mark(colour)
    stack_gap = 46.0
    # mark and wordmark share a left edge, matching the horizontal lockup's ranging
    wm, wmw, y0, L, fs_cap = build_wordmark(colour, 0)
    total_w = max(mw, wmw)
    block_top = y0 - fs_cap
    shift = mh + stack_gap - block_top
    body = (f'<g transform="translate({p},{p})">'
            f'{frag}<g transform="translate(0,{shift:.2f})">{wm}</g></g>')
    total_h = mh + stack_gap + (2 * L + fs_cap)
    write(f"oqts-lockup-stacked{suffix}.svg", body, total_w + 2 * p, total_h + 2 * p,
          bg, "OQTS stacked lockup")

# ---------- 4. wordmark only ----------
for suffix, colour, bg in [("", NAVY, None), ("-reverse", PAPER, None),
                           ("-on-ivory", NAVY, IVORY), ("-on-navy", PAPER, NAVY)]:
    p = pad_for(bg)
    wm, wmw, y0, L, fs_cap = build_wordmark(colour, 0)
    top = y0 - fs_cap
    body = f'<g transform="translate({p},{p - top:.2f})">{wm}</g>'
    write(f"oqts-wordmark{suffix}.svg", body, wmw + 2 * p,
          (2 * L + fs_cap) + 2 * p, bg, "OQTS wordmark")

# ---------- 5. favicon: dots fallback for <=32px ----------
for suffix, colour, bg in [("", NAVY, None), ("-on-navy", PAPER, NAVY)]:
    p = pad_for(bg)
    body = (f'<g transform="translate({p},{p}) scale({H/280.0:.6f}) translate(-40,-40)">'
            f'<g fill="none" stroke="{colour}" stroke-width="22">'
            f'<path d="M 62 40 L 40 40 L 40 240 L 62 240"/>'
            f'<path d="M 218 40 L 240 40 L 240 240 L 218 240"/></g>'
            f'<g fill="{colour}">'
            f'<circle cx="100" cy="100" r="18"/><circle cx="180" cy="100" r="18"/>'
            f'<circle cx="100" cy="180" r="18"/><circle cx="180" cy="180" r="18"/></g></g>')
    size = H * (200 + 22) / 200.0
    write(f"oqts-favicon{suffix}.svg", body, size + 2 * p, size + 2 * p, bg,
          "OQTS favicon")

print(f"wrote {len(written)} files to build/")
for n, dim in written:
    print(f"  {n:34s} {dim}")

fs_cap, fs_em, L, y0 = wordmark_metrics()
stem = MARK_STEM * CAP_U
print(f"\nderived spec: bracket stroke {stem*BR:.2f}  glyph stem {stem:.2f}  "
      f"wordmark em {fs_em:.2f}  cap {fs_cap:.2f}  leading {L:.2f}  track {TRACK*fs_em:.2f}")
