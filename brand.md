# OQTS Brand & Design System

**Oxford Quantitative Trading Society.** Status **v1.1** (2026-08-08) — logo,
type, colour, charts and imagery all specified. Open items are marked `TODO`.

This file is the single editable source of truth for OQTS styling. The public
site (`oqts/oqts.org`) and the member platform (`oqts-platform`) consume tokens
and assets from this repo and never define styling of their own.

---

## How to use this document

**This doc explains and specifies. [`demo/`](demo/index.html) shows.**

Every rule below has a worked example on the demo page. Nothing in the brand is
described here without being visible there.

There is **one ground**. Oxford appears as a band inside a light page — the
title bar and the footer — but that is a surface, not a second theme. The brand
has no dark mode.

| This doc | Explains | See it |
|---|---|---|
| §2 Colour | Why two grounds and why the accent splits by job | demo §2 — every token with its live contrast against the current ground |
| §3 Type | Why a monospace leads and a journal serif carries | demo §3 — every scale role rendered at real size with its token |
| §4 Signature device | Why a ledger double rule closes a section | demo §5 — the rule, the hairline and the bracketed block |
| §5 Logo | The locked construction and the asset set | demo §1 — every colourway, the size ladder, clear space, and six ways to get it wrong |
| §6 Charts | Why these hues, and where red/green costs you | demo §6 — bar, line, diverging, scatter, both ramps, and the returns table |
| §7 Imagery | Why full colour rather than duotone | demo §7 — the two crops, the scrim, the escape hatch |
| §8 Texture | The one permitted whitespace texture and its recipe | demo §8 — the dot field over ivory at real densities |
| §9 Layout | Grid, measure and rhythm | demo §4 — the spacing scale drawn to size |
| §10 Accessibility | The floor everything is measured against | demo §2 and §6 — contrast shown, not asserted |

Serve it locally:

```bash
python3 -m http.server 8001 -d oqts-design
# demo/  — the visual reference · lab/ — the type tester that produced the spec
```

**Two habits keep this honest.** Colour decisions are *measured*, never
eyeballed — every contrast figure in this doc came from a calculation and every
chart hue from the palette validator. And every asset is *generated* from a
spec, never hand-drawn, so the numbers in §5 and the artwork cannot drift apart.

---

## 1. Identity

### Who this brand speaks to

1. **Oxford students** considering quantitative careers — mathematically
   strong, allergic to hype.
2. **Sponsor firms** (G-Research, Jane Street, Optiver, Hudson River
   Trading) — organisations with famously restrained, confident brands of
   their own.
3. **The University** — OQTS is a Proctors-registered society; the brand
   uses "Oxford" in the name but never the University arms, crest, or logo.

### Voice

Understated confidence. The brand of a research institution that happens to
be run by students, not a student club that mentions research. Specific
beats clever; numbers beat adjectives. Sentence case everywhere except
small-caps labels.

**No em-dashes, anywhere.** Rework the sentence with a colon, a comma, or
a full stop. (House rule, 2026-08-08; applies to every surface, including
UI microcopy.)

### Positioning line

> Oxford's first dedicated quantitative trading society.

(Carried over from the current site — it is true and it is enough.)

---

## 2. Colour

> **See it —** [demo §2](demo/index.html#colour): every token as a swatch with its measured
> contrast against the current ground, and the accent split shown side by side.

| Token | Hex | Role |
|---|---|---|
| `ivory` | `#FBF8F1` | **Base ground.** A warm off-white — the same hue as `paper`, lifted. Carries every light page. |
| `oxford` | `#002147` | **Base ink and dark ground.** Text on light; full-bleed for the title bar and the footer. Oxford Blue — the University's colour is free to use; its crest is not. |
| `paper` | `#F4EDDC` | **Secondary.** The original beige, now a tint rather than a ground: panels, cards, banded sections. Reads as a soft inset against `ivory`. |
| `chalk` | `#E0D5BC` | Secondary. Hairlines and borders. |
| `slate` | `#46586A` | Secondary text on light (bylines, captions, metadata). 6.9:1 on `ivory`. On navy → `slate-rev` `#A9B6C6`, 7.8:1. |
| `bronze` | `#8A6933` | **Accent text.** The only gold safe for type on a light ground — 4.8:1 on `ivory`. Eyebrows, small-caps labels, links on hover. |
| `camel` | `#B08D57` | Accent for **rules and detail only** on light — 2.9:1, not text-safe. On navy → `camel-rev` `#CEB083`, where it is text-safe at 7.8:1. |

Rules of use:

- **Two grounds only:** `ivory` (default) and `oxford` (title bar, feature
  bands, footer). `paper` is a tint on top of `ivory`, not a third ground.
  No greys, no gradients.
- `oxford` on `ivory` is the primary text pair (15.1:1). `paper` on `oxford`
  for dark surfaces (13.8:1).
- **One gold, two roles.** On light grounds gold is not text-safe — `camel`
  measures 2.9:1 on `ivory`, below the 4.5:1 floor at any size. So accent
  *text* is `bronze` and accent *rules* are `camel`, and the two never swap.
  Reversed on navy the constraint disappears (`camel-rev` 7.8:1), so gold text
  is fine on dark.
- The accent is earned, not sprinkled: if a page uses gold in more than
  rules, labels, and one marker, it is over-dressed. The logo itself is
  always monochrome — accents never enter the mark.
- The **title bar is `oxford`**, full-bleed, carrying the reversed lockup. It
  is the first thing on the page and should read as a distinct band, not as a
  continuation of the ground.
- **Navy opens and closes a page, and does nothing in between.** Title bar and
  footer only. A third navy band mid-page makes the page read as striped
  rather than bookended — use a `paper` tint for feature sections instead.
- Chart colours are **not** brand colours; the data palette is defined
  separately when the first chart ships (dataviz tokens, validated for
  contrast in both modes).

## 3. Type

> **See it —** [demo §3](demo/index.html#type): the whole scale rendered at real size, each
> role labelled with its token, in both faces.

Two families. No third.

| Role | Face | Notes |
|---|---|---|
| Logo, display, headings, eyebrows, figures & data | **Latin Modern Mono** | The typewriter face of Computer Modern — literally the type of every LaTeX paper on arXiv. Chosen because it is the society's own subject rendered as type, and because it is what the mark itself is set in. GUST Font License (LPPL-based), free for commercial use, self-hosted. Not on Google Fonts. |
| Body copy, UI, forms, member portal | **STIX Two Text** | Scientific and Technical Information Exchange — commissioned by the AIP, ACS, AMS, IEEE and Elsevier for scholarly journals, and the text companion to STIX Two Math. Serious, academic, and built to sit beside mathematical notation, which is exactly the job here. SIL OFL, self-hostable. |

Type rules:

- **Latin Modern Mono leads, STIX Two Text carries.** The mono is the voice
  of the brand — masthead, headings, section eyebrows, numbers, tables,
  anything that should feel measured. The serif does the reading work.
- Latin Modern Mono has only three usable cuts (Light, Regular, and the
  oddly-named Light Bold). Do not ask it for a weight ramp; get hierarchy
  from **size and letter-spacing**, which is how the logo does it.
- It is drawn as a 10pt optical size, so it renders thin on screen. Never
  set it below 13px, and prefer `oxford` on `ivory` rather than reversed at
  small sizes.
- Caps + tracking is the mono's idiom: eyebrows 12–13px at 0.14em;
  the logo wordmark at 0.090em. Never faux-bold either face.
- Body 17px/1.65 on `ivory`. Long-form measure ≤ 70ch — in STIX, never mono.
  Monospaced paragraphs are a readability cost with no upside.
- Tabular figures (`font-variant-numeric: tabular-nums`) in any column of
  numbers. Latin Modern Mono is monospaced, so it is already tabular.
- `TODO` — if the member portal's UI density outgrows a serif, add **Source
  Sans 3** for interface chrome only (never body, never display). Do not
  introduce it pre-emptively.

### The type scale

Every size is a token in `assets/oqts.css`. Reach for a role, never a number.

| Token | Size | Face | Line | Tracking | Use |
|---|---|---|---|---|---|
| `--oqts-display-xl` | 30→46 fluid | mono | 1.16 | .01em | Page title, one per page |
| `--oqts-display-l` | 22→28 fluid | mono | 1.25 | .015em | Section heading |
| `--oqts-display-m` | 20px | mono | 1.30 | .02em | Sub-heading |
| `--oqts-label` | 16px | mono | 1.35 | .06em caps | Card and table headings |
| `--oqts-data` | 15px | mono | 1.50 | — | Tables, figures, tabular numerals |
| `--oqts-eyebrow` | 13px | mono | 1.40 | .14em caps | Section eyebrow, in `bronze` |
| `--oqts-micro` | 13px | mono | 1.50 | .03em | Colophon, figure captions |
| `--oqts-lede` | 20px | serif | 1.55 | — | Standfirst under a title |
| `--oqts-body` | 17px | serif | 1.65 | — | Body copy |
| `--oqts-body-s` | 14px | serif | 1.60 | — | Captions, notes, secondary |

- **13px is a hard floor for Latin Modern**, which is why the eyebrow is 13
  and not 12. The serif may go to 14; nothing goes below that.
- Hierarchy in the display column comes from **size and tracking**, never
  weight — Latin Modern has no weight ramp to give.
- Caps always take tracking; lower case never does.

### Spacing and layout

A 4px grid, also tokenised. Steps 1–4 work inside a component, 5–7 between
components, 8–10 between sections.

| Token | Value | Typical use |
|---|---|---|
| `--oqts-space-1…4` | 4 / 8 / 12 / 16px | Padding, gaps, label-to-field |
| `--oqts-space-5…7` | 24 / 32 / 48px | Component padding, card gutters |
| `--oqts-space-8…10` | 64 / 96 / 128px | Section rhythm |
| `--oqts-measure` | 68ch | Long-form column — never wider |
| `--oqts-content` | 1120px | Page max width |
| `--oqts-gutter` | 32px, 20px ≤640px | Page padding |
| `--oqts-rule` | 1px | Hairline weight, in `chalk` |


## 4. The signature device: the closing rule

> **See it —** [demo §5](demo/index.html#components): the double rule closing a section, the
> hairline opening one, and the bracket reused as a content frame.

In ledger typography a **double rule** under a column means *the total —
this account is settled.* It is the one piece of visual language that is
simultaneously editorial, institutional, and from the society's actual
subject.

Usage:

- A single hairline (`1px chalk` on light, translucent `paper` on oxford)
  opens a section; the **double rule** (two 1px lines, 3px apart, in
  `camel`) closes it — under mastheads, under section ends, under
  table totals.
- The double rule closes sections and totals, and nowhere else. Never
  decorate with it mid-content. It does **not** appear in the logo — the
  mark's own signature is the bracket.

### The plate

The device family's third member: a **1px `chalk` frame** around a page's
title area, with the dot-field texture (§8) running inside it, flush to
the frame on every edge. The closing rule sits *outside*, below the
frame. One plate per page at most — it marks the hero, and nothing else;
repeated down a page it would decay into boxes. Paper panels are never
plated and never textured.

Interactive panels take a hover affordance: a `1px` `oxford` outline
(drawn as an inset shadow, so nothing reflows).

## 5. Logo — the matrix monogram

> **See it —** [demo §1](demo/index.html#logo): all five artefacts in every colourway, the
> size ladder down to 16px, clear space drawn, and six ways to get it wrong.

The identity is a **2×2 matrix whose entries are the society's initials** —
`[O Q / T S]` — set in Latin Modern Mono inside drawn brackets. It reads as
a matrix, which is the society's subject, and as a monogram. Always
monochrome: `oxford` on light, `paper` on navy. It replaces the temporary
interlocked-OQTS JPEG.

### Locked construction

All values in mark units, where the **bracket ink height = 216** is the
reference dimension. The mark is normalised to that height regardless of
stroke weight, so it always occupies the same optical space.

| Parameter | Value |
|---|---|
| Matrix letters | Latin Modern Mono **Light 10 Bold**, cap height **62** |
| Wordmark | Latin Modern Mono **10 Regular** |
| Spread (letter centre-to-centre) | **100**, both axes, about the bracket centre (140,140) |
| Glyph stem (measured) | 8.38 |
| Bracket stroke | **9.58** — always stem × 16/14, the ratio inherited from the drawn mark |
| Bracket arms | 22 × (stroke/16), spanning the 200×200 inner square |
| Wordmark size | **70%** — its ink height, cap-top of line 1 to baseline of line 3, equals 0.70 × bracket height |
| Wordmark tracking | **0.090 em** (4.24 units at the locked size) |
| Wordmark leading | 1.30 em (61.23 units) |
| Gap, bracket to wordmark | **50** |
| Wordmark alignment | Three lines, **left aligned**, ink centred on the mark's centre |

The wordmark always breaks `OXFORD / QUANTITATIVE / TRADING SOCIETY` over
three lines. Never two, never four, never on one line.

**All production artwork carries the glyphs as outlines**, not live text, so
the files have no font dependency and render identically everywhere. The
GUST Font License permits this. Regenerate the whole set with
`lab/tools/build-logos.py` — the spec lives at the top of that file, and
it is the single place any of these numbers is edited.

### Asset set

Transparent files are the primaries; the `-on-*` files bake a background and
40 units of clear space. Reach for a baked file wherever **you do not control
the surface** — Word, PowerPoint, Keynote, Slack, email clients and anything
that composites onto its own background. A transparent logo dropped into a
dark-themed Slack becomes navy-on-near-black and vanishes.

`-on-ivory` is the default light choice, matching the page ground. `-on-paper`
sits on a panel tint, `-on-white` is for documents and print, `-on-navy` for
dark surfaces.

| File | Use |
|---|---|
| `oqts-lockup.svg` / `-reverse` | **Primary.** Site masthead, letterhead, decks, email footer |
| `oqts-lockup-on-ivory` / `-on-paper` / `-on-white` / `-on-navy` | Baked-background versions of the above |
| `oqts-lockup-stacked.svg` / `-reverse` / `-on-ivory` / `-on-navy` | Narrow and vertical contexts — posters, pull-ups, portrait slides |
| `oqts-mark.svg` / `-reverse` / `-on-ivory` / `-on-paper` / `-on-white` / `-on-navy` | Mark alone where the name is already present; social avatar; app icon |
| `oqts-wordmark.svg` / `-reverse` / `-on-ivory` / `-on-navy` | Where the mark appears separately on the same surface |
| `oqts-favicon.svg` / `-on-navy` | **≤ 32px only** — entries collapse to four dots `[::]` |

Rasters are derived from those SVGs by `lab/tools/build-exports.py`, never
drawn separately:

| File | Use |
|---|---|
| `assets/logo-png/*.png`, `@2x`, `@3x` | Email, slide software, anywhere vector is refused. Every SVG has a PNG; the `-on-*` PNGs are **flattened to RGB with no alpha channel**, so nothing can composite them wrongly |
| `assets/favicon/favicon.ico` | Browser tab — 16/32/48 in one file |
| `assets/favicon/apple-touch-icon.png` | iOS home screen, 180×180, opaque navy |
| `assets/favicon/icon-512.png` | PWA / Android maskable icon |
| `assets/favicon/og-card.png` / `-navy` | Link previews, 1200×630 |

`TODO` — convert both faces to WOFF2 and subset before production.

### Rules

- **Colourways:** `oxford` on `ivory`, `paper` or white; `paper` on `oxford`. Nothing
  else. The mark is always monochrome — accents never enter it.
- **Clear space:** one bracket-arm length (22 units, ≈ 10% of the mark
  height) on all sides. The baked-background files already include it.
- **Minimum sizes:** lockup ≥ 180px wide; mark alone ≥ 48px; below 32px use
  the dots favicon. Latin Modern's strokes are fine, so do not push these.
- Never stretch, recolour, outline, add shadows, place on photography, or
  set the wordmark in any other face.
- The University crest or arms never appear alongside the mark.
- Assets live in `assets/logo/` (SVG, source of truth), `assets/logo-png/`
  and `assets/favicon/`. See `README.md` for which file to reach for.
- Exploration history and superseded artwork are in `archive/`; the
  interactive type tester that produced this spec is `lab/index.html`.

### Matrix devices (parametric)

The mark's construction is open, under control, to other words. A
**matrix device** sets a word in the bracket grid using the identical
locked spec — same face and cap height, same 100-unit cell pitch, same
bracket stroke and arms, same 216-unit ink normalisation — so every
device sits beside the mark as an equal-weight sibling. The first is
`JOIN`, the masthead's recruiting mark.

- Up to 4 letters take the 2×2 grid; 5-9 letters take a 3×3 at the same
  pitch. **Unused cells are filled with dots** (the favicon idiom), never
  left empty.
- Generate only via `lab/tools/build-matrix.py`; assets land in
  `assets/matrix/`. Hand-drawn or CSS-approximated matrices are forbidden
  — that is how the geometry drifts.
- A device is UI furniture, not identity: it never replaces the mark,
  never appears in the masthead's logo position, and at most one device
  appears per surface.
- Colourways and don'ts follow the logo rules above.

## 6. Data visualisation

> **See it —** [demo §6](demo/index.html#charts): ranked bars, two-series lines, the diverging
> attribution chart, the four-slot scatter and both ramps — all built from the tokens, so the
> theme toggle repaints them.

Charts are the most brand-critical thing this society produces — research
notes, OXDAQ standings, fund reports. Every value here came out of the
six-checks validator, not out of taste, and **must be re-validated after any
change**. Tokens live in `assets/oqts.css`.

### The rules that are not negotiable

- **One axis.** Never two y-scales on one chart. Two measures of different
  scale become two charts, small multiples, or an index to a common base.
- **Colour follows the entity, never its rank.** Filtering a series out must
  not repaint the survivors.
- **Assign slots in fixed order, never cycled.** A ninth series folds into
  "Other", facets or small multiples — never a generated hue.
- **Text wears text tokens, never the series colour.** A coloured mark beside
  a label carries identity; the label itself stays in ink.
- **Sequential is one hue light→dark. Diverging is two hues with a neutral
  midpoint.** Never a rainbow, never a hue at the midpoint.
- A legend is present for two or more series; four or fewer are also direct
  labelled, so identity is never colour alone. A table view always exists.

### Categorical

Eight slots. Slots 1 and 2 are the brand, so most charts read as OQTS
without effort.

| Slot | Hue | Hex |
|---|---|---|
| 1 | oxford blue *(brand)* | `#1E5C99` |
| 2 | gold *(brand)* | `#B8821E` |
| 3 | violet | `#7A5BB0` |
| 4 | teal | `#0E8A72` |
| 5 | orange | `#C4611A` |
| 6 | crimson | `#8E2740` |
| 7 | magenta | `#C2529E` |
| 8 | green | `#2F6B1E` |

Validated for **adjacent** pairs — bars, stacks, lines — worst ΔE 10.6, all
five checks pass on ivory.

**Scatter, bubble and small multiples use slots 1, 2, 4 and 6 only.** There
any two marks can touch, so all pairs must separate — validated at ΔE 10.4.
Beyond four series, facet; do not add slots.

> `slate` is deliberately absent. It measures below the chroma floor — in a
> chart it reads as grey, not as a colour. It stays a text token.

### Sequential

One hue, the brand blue, light to dark: `--oqts-seq-100` … `-800`. Steps 100–400
are for continuous fills only, where the lightest may recede into the surface.
**Ordinal marks — tiers, buckets, funnel stages — start at 500**, the first
step clearing 3:1.

### Diverging — and its one real weakness

Red ↔ green with a neutral midpoint, chosen deliberately for an audience that
reads P&L. It carries a cost worth stating plainly.

| | midpoint → extreme |
|---|---|
| negative | `#C8442E` `#A82A22` `#7F1D1D` |
| midpoint | `#DCD5C6` |
| positive | `#46A876` `#2A8A5F` `#1E6B4F` |

Corresponding steps — a +2% against a −2% — clear ΔE 8.3–10.1, which passes.
**But non-corresponding steps drop to ΔE 4.3.** Wherever arbitrary steps can
abut — a returns table, a correlation matrix, a heat grid — the sign must also
be carried by a signed value or a label. Never by hue alone. This is the one
place the palette leans on something other than colour, and it is not optional.

For tables and heat grids, use the **cell tints** (`--oqts-div-cell-*`): the
same two hues composited over ivory so ink stays at 6:1 or better on every
cell. A full-strength diverging fill behind text fails contrast.

### Status

Reserved. Never a series colour, always shipped with an icon and a label.

| Role | Hex | on ivory | on oxford |
|---|---|---|---|
| good | `#0CA30C` | 3.16 | 4.78 |
| warning | `#FAB219` | 1.73 | 8.75 |
| serious | `#EC835A` | 2.49 | 6.08 |
| critical | `#D03B3B` | 4.53 | 3.34 |

`warning` and `serious` are sub-3:1 on ivory by design — the icon and label
are the mitigation, which is why status colour never travels alone.

### Chrome

Surface `ivory`. Ink `oxford`. Secondary `slate`. Axis and labels `#6B6555`.
Gridlines `chalk` — recessive, always. Baseline `#C9BB9C`.

> If a dark chart surface is ever needed, its steps must be **selected and
> re-validated** against that surface. Never flip these.

Marks: thin, 2px lines, markers ≥ 8px, a 2px surface gap between adjacent
fills and stacked segments, direct labels used selectively — never a number
on every point.

## 7. Imagery

> **See it —** [demo §7](demo/index.html#imagery): the only two crops, the scrim treatment for
> type over an image, and the escape hatch.

Photography is **full colour**, governed by a grading rule rather than a
filter. The society needs to look like a real community, which duotone and
monochrome both undercut; the price is that the rule has to be enforced.

**Shooting and selection**

- Natural light wherever possible. No on-camera flash, no filters, no heavy
  vignettes, no lifted or crushed blacks.
- Neutral white balance. A warm or blue cast is the single most common way a
  set of photos stops looking like one set.
- Plain or architectural backgrounds. Oxford stone, plain walls, clean
  interiors — never a cluttered room.
- Eye-level for people. No extreme angles.
- Crops: 3:2 landscape or 4:5 portrait. Nothing else.

**Grading**

- One consistent, slight warmth so images sit with `ivory`. Grade the set
  together, never image by image.
- Headshots share one framing — head and shoulders, same crop, same
  background treatment across the whole committee.
- No stock photography, and in particular none of traders-at-screens.

**Placement**

- Never set type directly on a busy photograph. If text must sit over an
  image, use an `oxford` scrim at 70% and put the type on that.
- **If a photograph cannot be graded into the set, do not use it.** A data
  figure or a type-led card is always better than one off-brand image, and
  this rule is what stops the site drifting once other people upload.

## 8. Texture

> **See it —** [demo §8](demo/index.html#texture): the field over ivory with text at
> real densities; [lab/textures.html](lab/textures.html) is the tester that produced the recipe.

Whitespace may carry one texture: a noise-modulated **dot field** in
`oxford` ink. It is the favicon's dot idiom dissolved into the page — dots
grow and fade in smooth clusters, reading as data points, not decoration.
No other texture exists; hexagons, bars and grids were tested and retired.

**The canonical recipe** (regenerate only via `lab/tools/build-patterns.mjs`;
the assets ship in `assets/patterns/`):

```
{"pattern":"dots","seed":5994,"cell":14,"szmin":0,"szmax":4,
 "amin":0,"amax":0.105,"cluster":6,"detail":0.5,"cut":0}
```

The workhorse cut ships as a numbered set, `oqts-dots-right-1.svg` …
`-6.svg`, identical in recipe and **differing only in seed**. Rotate
through the set: adjacent placements must wear different numbers, so no
two fields a reader can compare are ever the same constellation. Each
carries explicit pixel dimensions (1200×760) and renders at a **fixed
intrinsic scale** (`background-size:auto`): dot size never varies with
the height of the section wearing it. **The field always ramps
right-to-left**: densest at the right edge, the last and smallest dots
landing around the middle of the page, with a baked bottom fade so tall
sections dissolve rather than crop. `oqts-dots-uniform.svg` (no ramp)
exists for sparse full-width areas.

Rules of use:

- **`oxford` ink on `ivory` only.** Never on `paper` panels or cards, never
  on navy, never under imagery. The texture is a property of the page
  ground, not of components.
- Opacity is baked into the asset and peaks at 0.105. Do not raise it, and
  do not tint the dots — one ink, screened, like everything else.
- The field fills plain whitespace wherever content leaves it: heroes and
  any section whose content is a narrow column. Never behind body copy at
  reading density; the ramp exists so dots fade out before the measure
  column, and it always runs right-to-left.
- Keep max dot diameter between one-fifth and one-third of cell spacing
  (the recipe sits at 4/14). Coarser reads as halftone; finer as grime.
- A re-tune happens in the lab, lands here as a new recipe, and regenerates
  the assets — the site never carries a private variant.

## 9. Layout & structure

> **See it —** [demo §4](demo/index.html#space): the 4px scale drawn to size, step by step.

- Grid: 12-col, max content width 1120px; long-form text column 680px.
- Section headers: tracked-caps `camel` eyebrow in Latin Modern Mono, then
  the heading in Latin Modern Mono.
- Structural devices must encode information: rules open/close sections;
  numbered markers only for true sequences (competition tiers, process
  steps); tables get hairline row rules and a closing double rule on the
  final/total row.
- Motion: one orchestrated page-load reveal at most; scroll effects and
  ambient animation are off-brand. `prefers-reduced-motion` respected.

## 10. Accessibility floor

> **See it —** [demo §2](demo/index.html#colour) shows live contrast per token; every status
> chip in [demo §5](demo/index.html#components) ships with its icon and word.

- All text pairs ≥ 4.5:1. Verified on `ivory`: `oxford` 15.1, `slate` 6.9,
  `bronze` 4.8. `camel` (2.9) and `chalk` (1.4) are **never** used for text.
- Visible keyboard focus: 2px `oxford` outline on light, `camel-rev`
  `#CEB083` on oxford.
- Latin Modern Mono is a fine-stroked 10pt design: never below 13px, and
  prefer dark-on-light for anything small.
- Responsive to 360px. Semantic headings, one `h1` per page.

## 11. Single source of truth

Per society policy, everything is editable in exactly one place:

| Thing | Edited in | Displayed in |
|---|---|---|
| Styling, tokens, logo assets | this repo (`oqts/design`) | site, platform, docs |
| Society hierarchy, teams, permissions | GitHub org | site (read-only via API) |
| Member roster / mailing list | platform DB | platform |
