"""Raster exports derived from the production SVGs in assets/logo/.

SVG is the source of truth; nothing here is drawn from scratch. Run after
build-logos.py whenever the mark changes.

Produces:
  assets/logo-png/   1x / 2x / 3x PNGs of the lockup, stacked lockup and mark
  assets/favicon/    favicon.ico (16/32/48), PNG icons, apple-touch-icon,
                     and a 1200x630 Open Graph card
"""
import os

import cairosvg
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
DESIGN = os.path.dirname(os.path.dirname(HERE))
LOGO = os.path.join(DESIGN, "assets", "logo")
PNG = os.path.join(DESIGN, "assets", "logo-png")
ICON = os.path.join(DESIGN, "assets", "favicon")
for d in (PNG, ICON):
    os.makedirs(d, exist_ok=True)

NAVY, PAPER = "#002147", "#F4EDDC"
written = []


def render(svg, out, width=None, height=None, bg=None):
    cairosvg.svg2png(url=os.path.join(LOGO, svg), write_to=out,
                     output_width=width, output_height=height,
                     background_color=bg)
    written.append((os.path.relpath(out, DESIGN), f"{width or ''}x{height or ''}"))


# ---- 1. logo PNGs at 1x/2x/3x. Base widths chosen from real use:
#         lockup 600 (masthead/email), stacked 360, mark 256 (avatar/app icon).
for svg, base in [("oqts-lockup.svg", 600), ("oqts-lockup-reverse.svg", 600),
                  ("oqts-lockup-stacked.svg", 360), ("oqts-lockup-stacked-reverse.svg", 360),
                  ("oqts-mark.svg", 256), ("oqts-mark-reverse.svg", 256),
                  ("oqts-wordmark.svg", 480)]:
    stem = svg[:-4]
    for mult in (1, 2, 3):
        suffix = "" if mult == 1 else f"@{mult}x"
        render(svg, os.path.join(PNG, f"{stem}{suffix}.png"), width=base * mult)

# ---- 2. favicons. The dots cut is the only thing legible at these sizes.
for px in (16, 32, 48, 64):
    render("oqts-favicon.svg", os.path.join(ICON, f"favicon-{px}.png"), width=px)

ico_sizes = [16, 32, 48]
frames = [Image.open(os.path.join(ICON, f"favicon-{s}.png")).convert("RGBA") for s in ico_sizes]
frames[0].save(os.path.join(ICON, "favicon.ico"), format="ICO",
               sizes=[(s, s) for s in ico_sizes])
written.append((os.path.relpath(os.path.join(ICON, "favicon.ico"), DESIGN),
                "/".join(str(s) for s in ico_sizes)))

# apple-touch-icon must be opaque and square: the mark reversed on navy
render("oqts-mark-on-navy.svg", os.path.join(ICON, "apple-touch-icon.png"),
       width=180, height=180)

# maskable / PWA icon, same artwork at 512
render("oqts-mark-on-navy.svg", os.path.join(ICON, "icon-512.png"),
       width=512, height=512)

# ---- 3. Open Graph card, 1200x630, lockup centred on paper ----
def og_card(name, logo_svg, bg):
    W, Hh = 1200, 630
    tmp = os.path.join(ICON, "_tmp-og.png")
    cairosvg.svg2png(url=os.path.join(LOGO, logo_svg), write_to=tmp, output_width=720)
    fg = Image.open(tmp).convert("RGBA")
    card = Image.new("RGB", (W, Hh), bg)
    card.paste(fg, ((W - fg.width) // 2, (Hh - fg.height) // 2), fg)
    card.save(os.path.join(ICON, name))
    os.remove(tmp)
    written.append((os.path.relpath(os.path.join(ICON, name), DESIGN), f"{W}x{Hh}"))


og_card("og-card.png", "oqts-lockup.svg", PAPER)
og_card("og-card-navy.png", "oqts-lockup-reverse.svg", NAVY)

print(f"wrote {len(written)} files")
for n, dim in written:
    print(f"  {n:46s} {dim}")
