# OQTS Brand & Design System

**Oxford Quantitative Trading Society** — brand identity and design doc.
Status: **v1.1** (2026-08-08) — **logo and type system final.** Palette revised:
lighter `ivory` ground, `paper` demoted to a tint, `bronze` added for accent
text. Remaining open
items are noted inline as `TODO`.
This file is the single editable source of truth for all OQTS styling. The
public site (`oqts/oqts.org`) and the member platform (`oqts-platform`)
consume tokens and assets from this repo; styling is never defined elsewhere.

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

### Positioning line

> Oxford's first dedicated quantitative trading society.

(Carried over from the current site — it is true and it is enough.)

---

## 2. Colour

| Token | Hex | Role |
|---|---|---|
| `ivory` | `#FBF8F1` | **Base ground.** A warm off-white — the same hue as `paper`, lifted. Carries every light page. |
| `oxford` | `#002147` | **Base ink and dark ground.** Text on light; full-bleed for the title bar, feature bands and footer. Oxford Blue — the University's colour is free to use; its crest is not. |
| `paper` | `#F4EDDC` | **Secondary.** The original beige, now a tint rather than a ground: panels, cards, banded sections. Reads as a soft inset against `ivory`. |
| `chalk` | `#E0D5BC` | Secondary. Hairlines and borders. |
| `slate` | `#46586A` | Secondary text on light (bylines, captions, metadata). 6.9:1 on `ivory`. |
| `bronze` | `#856B32` | **Accent text.** The only gold safe for type on a light ground — 4.8:1 on `ivory`. Eyebrows, small-caps labels, links on hover. |
| `camel` | `#B08D57` | Accent for **rules and detail only** on light — 2.9:1, not text-safe. On navy → `#CDB183`, where it is text-safe at 7.8:1. |

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

## 5. Logo — the matrix monogram

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

Transparent files are the primaries; the `-on-*` files bake a background
and 40 units of clear space for slide decks and anywhere a flat file is
easier than CSS.

| File | Use |
|---|---|
| `oqts-lockup.svg` / `-reverse` | **Primary.** Site masthead, letterhead, decks, email footer |
| `oqts-lockup-on-beige` / `-on-white` / `-on-navy` | Flat-background versions of the above |
| `oqts-lockup-stacked.svg` / `-reverse` / `-on-navy` | Narrow and vertical contexts — posters, pull-ups, portrait slides |
| `oqts-mark.svg` / `-reverse` / `-on-beige` / `-on-white` / `-on-navy` | Mark alone where the name is already present; social avatar; app icon |
| `oqts-wordmark.svg` / `-reverse` | Where the mark appears separately on the same surface |
| `oqts-favicon.svg` / `-on-navy` | **≤ 32px only** — entries collapse to four dots `[::]` |

Rasters are derived from those SVGs by `lab/tools/build-exports.py`, never
drawn separately:

| File | Use |
|---|---|
| `assets/logo-png/*.png`, `@2x`, `@3x` | Email, slide software, anywhere vector is refused |
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

## 6. Layout & structure

- Grid: 12-col, max content width 1120px; long-form text column 680px.
- Section headers: tracked-caps `camel` eyebrow in Latin Modern Mono, then
  the heading in Latin Modern Mono.
- Structural devices must encode information: rules open/close sections;
  numbered markers only for true sequences (competition tiers, process
  steps); tables get hairline row rules and a closing double rule on the
  final/total row.
- Motion: one orchestrated page-load reveal at most; scroll effects and
  ambient animation are off-brand. `prefers-reduced-motion` respected.

## 7. Accessibility floor

- All text pairs ≥ 4.5:1. Verified on `ivory`: `oxford` 15.1, `slate` 6.9,
  `bronze` 4.8. `camel` (2.9) and `chalk` (1.4) are **never** used for text.
- Visible keyboard focus: 2px `oxford` outline on light, `camel-rev`
  `#CDB183` on oxford.
- Latin Modern Mono is a fine-stroked 10pt design: never below 13px, and
  prefer dark-on-light for anything small.
- Responsive to 360px. Semantic headings, one `h1` per page.

## 8. Single source of truth

Per society policy, everything is editable in exactly one place:

| Thing | Edited in | Displayed in |
|---|---|---|
| Styling, tokens, logo assets | this repo (`oqts/design`) | site, platform, docs |
| Society hierarchy, teams, permissions | GitHub org | site (read-only via API) |
| Member roster / mailing list | platform DB | platform |
