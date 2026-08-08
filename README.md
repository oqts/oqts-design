# OQTS design

Brand assets and the design system for the **Oxford Quantitative Trading
Society**. This repository is the single editable source of truth for OQTS
styling — the public site (`oqts/oqts.org`) and the member platform
(`oqts-platform`) consume from here and never define styling of their own.

**Read [`brand.md`](brand.md) first.** It carries the identity, colour, type
and logo specification, including the locked construction of the mark.

---

## Layout

```
oqts-design/
├── brand.md          the design doc — colour, type, logo spec, rules
├── assets/           everything you consume
│   ├── logo/         17 production SVGs — the source of truth
│   ├── logo-png/     raster exports at 1x / 2x / 3x
│   ├── favicon/      favicon.ico, PNG icons, apple-touch, Open Graph cards
│   ├── oqts.css      ONE import: faces, colour, type scale, spacing
│   └── fonts/        the two brand faces, with their licences
├── demo/             a sample page proving the whole system
├── lab/              the type tester and the scripts that build assets/
└── archive/          superseded artwork and the exploration history
```

## Using the assets

Reach for `assets/logo/*.svg` first — the PNGs exist only for contexts that
cannot take vector (email clients, some slide software, social cards).

| You need | Use |
|---|---|
| Site masthead, letterhead, decks, email | `logo/oqts-lockup.svg` |
| The same on a dark surface | `logo/oqts-lockup-reverse.svg` |
| A flat file with the background baked in | `logo/oqts-lockup-on-{beige,white,navy}.svg` |
| Narrow or portrait space | `logo/oqts-lockup-stacked.svg` |
| The name is already on the page | `logo/oqts-mark.svg` |
| Social avatar, app icon | `logo/oqts-mark-on-navy.svg` |
| Browser tab, ≤ 32px | `favicon/favicon.ico` |
| iOS home screen | `favicon/apple-touch-icon.png` |
| Link previews | `favicon/og-card.png` (or `-navy`) |

Transparent SVGs are the primaries. The `-on-*` variants bake a background
plus 40 units of clear space, for slides and anywhere CSS is not available.

**Minimum sizes:** lockup ≥ 180px wide, mark alone ≥ 48px, and below 32px use
the favicon — its entries collapse to four dots. Latin Modern's strokes are
fine, so do not push past these.

## Using the type

```html
<link rel="stylesheet" href="assets/oqts.css">
```

One import, and a project has everything: both families, the colour tokens,
the type scale and the spacing scale, all as CSS custom properties
(`--oqts-ivory`, `--oqts-bronze`, `--oqts-body`, `--oqts-space-5`, …).
Reach for a role, never a raw value.

**Latin Modern Mono** leads — logo, display, headings, eyebrows, figures and
tables. **STIX Two Text** carries the reading — body copy, UI, forms, portal.
No third family. Latin Modern has only three cuts, so take hierarchy from size
and letter-spacing rather than weight, and never set it below 13px.

> Convert both faces to WOFF2 before production. They ship here as OTF/TTF,
> which is 2–4× larger than it needs to be over the wire.

## Regenerating

Every asset is generated; nothing is hand-drawn, so never edit an SVG by hand.
The logo specification lives at the top of `lab/tools/build-logos.py` and that
is the only place any of those numbers is edited.

```bash
uv run --with fonttools python lab/tools/build-logos.py        # assets/logo/
uv run --with cairosvg --with pillow python lab/tools/build-exports.py  # PNGs, icons, OG cards
```

## The lab

`lab/index.html` is the interactive type tester that produced the current
spec — it renders the mark and lockup across the whole font library with live
controls for size, gap, tracking and letter spread, and can flip the matrix
between typeset and constructed glyphs.

To add a face: drop the `.ttf` into `lab/fonts/` and run
`lab/tools/refresh-fonts.sh`. That measures it, classifies its Q, and rebuilds
`fonts.css` and `catalog.js`, which the tester reads. No HTML editing needed.

Serve the directory to view `demo/` or `lab/` in a browser:

```bash
python3 -m http.server 8001 -d oqts-design
# then http://<host>:8001/demo/  and  http://<host>:8001/lab/
```

## Licences

This repository is licensed in **two parts** — see [`LICENSE`](LICENSE).

- **Code, tokens and docs are MIT.** The build scripts, `oqts.css`, the demo
  page, the type tester and the documentation are yours to reuse.
- **The brand assets are all rights reserved.** The mark, wordmark, lockups
  and their exports identify the Society and are published here so that our
  own sites, our members and our sponsors can reproduce them correctly. That
  is the extent of the permission. Reproduce them as specified in `brand.md`,
  unaltered, and ask at oqts@oqts.org for anything else.

The typefaces are third-party and carry their own licences, which are
unaffected: Latin Modern is under the GUST Font License, STIX Two Text under
the SIL Open Font License 1.1, both permitting commercial use and
redistribution. Full texts sit beside the fonts. The logo carries its glyphs
as **outlines**, so deployed artwork has no font dependency.
