"""Raster exports derived from the production SVGs in assets/logo/.

SVG is the source of truth; nothing here is drawn from scratch. Run after
build-logos.py whenever the mark changes.

Produces:
  assets/logo-png/   1x / 2x / 3x PNGs of the lockup, stacked lockup and mark
  assets/matrix-png/ 1x / 2x / 3x PNGs of every matrix device
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
MATRIX = os.path.join(DESIGN, "assets", "matrix")
MATRIX_PNG = os.path.join(DESIGN, "assets", "matrix-png")
ICON = os.path.join(DESIGN, "assets", "favicon")
for d in (PNG, MATRIX_PNG, ICON):
    os.makedirs(d, exist_ok=True)

NAVY, PAPER = "#002147", "#F4EDDC"
written = []


def render(svg, out, width=None, height=None, bg=None, src=None):
    cairosvg.svg2png(url=os.path.join(src or LOGO, svg), write_to=out,
                     output_width=width, output_height=height,
                     background_color=bg)
    written.append((os.path.relpath(out, DESIGN), f"{width or ''}x{height or ''}"))


# ---- 1. logo PNGs at 1x/2x/3x. Base widths chosen from real use:
#         lockup 600 (masthead/email), stacked 360, mark 256 (avatar/app icon).
#
# Transparent PNGs are the flexible case but they break wherever the host
# supplies its own background -- Word, PowerPoint, Slack, email clients. So the
# baked variants are exported too, and those are FLATTENED to RGB so no alpha
# channel survives to be composited badly.
BASE_WIDTH = {"lockup": 600, "lockup-stacked": 360, "mark": 256, "wordmark": 480}


def base_for(stem):
    if "circlesafe" in stem:
        return 512          # profile-photo use: @2x lands on 1024
    body = stem[len("oqts-"):]
    for key in ("lockup-stacked", "lockup", "wordmark", "mark"):
        if body.startswith(key):
            return BASE_WIDTH[key]
    return 480


def export_dir(src, dest):
    for svg in sorted(os.listdir(src)):
        if not svg.endswith(".svg") or "favicon" in svg:
            continue
        stem = svg[:-4]
        base = base_for(stem)
        backed = "-on-" in stem
        for mult in (1, 2, 3):
            suffix = "" if mult == 1 else f"@{mult}x"
            out = os.path.join(dest, f"{stem}{suffix}.png")
            render(svg, out, width=base * mult, src=src)
            if backed:
                # flatten: a baked background must not ship an alpha channel
                im = Image.open(out)
                if im.mode in ("RGBA", "LA", "P"):
                    Image.alpha_composite(
                        Image.new("RGBA", im.size, (255, 255, 255, 255)),
                        im.convert("RGBA")).convert("RGB").save(out)


export_dir(LOGO, PNG)
export_dir(MATRIX, MATRIX_PNG)

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
