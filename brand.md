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
| `camel` | `#B08D57` | Accent for **rules and detail only** on light — 2.9:1, not text-safe. On navy → `#CDB183`. |
| `oldgold` | `#A5843E` | Accent for **rules and detail only** on light — 3.3:1, not text-safe. On navy → `#C8A85E`. |

Rules of use:

- **Two grounds only:** `ivory` (default) and `oxford` (title bar, feature
  bands, footer). `paper` is a tint on top of `ivory`, not a third ground.
  No greys, no gradients.
- `oxford` on `ivory` is the primary text pair (15.1:1). `paper` on `oxford`
  for dark surfaces (13.8:1).
- **Gold is not text-safe on light grounds.** Measured: `camel` 2.9:1 and
  `oldgold` 3.3:1 on `ivory` — both below the 4.5:1 floor at any size. Accent
  *text* therefore uses `bronze`; the two golds are for rules, marks and
  detail. Reversed on navy the constraint disappears: `camel` 7.8:1 and
  `oldgold` 7.0:1 both pass, so gold text is fine on dark.
- The accent is earned, not sprinkled: if a page uses gold in more than
  rules, labels, and one marker, it is over-dressed. The logo itself is
  always monochrome — accents never enter the mark.
- The **title bar is `oxford`**, full-bleed, carrying the reversed lockup. It
  is the first thing on the page and should read as a distinct band, not as a
  continuation of the ground.
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

## 4. The signature device: the closing rule

In ledger typography a **double rule** under a column means *the total —
this account is settled.* It is the one piece of visual language that is
simultaneously editorial, institutional, and from the society's actual
subject.

Usage:

- A single hairline (`1px chalk` on light, translucent `paper` on oxford)
  opens a section; the **double rule** (two 1px lines, 3px apart, in
  `camel`/`oldgold`) closes it — under mastheads, under section ends, under
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

`TODO` — convert both faces to WOFF2 and subset before production; ship the
type scale as a token file alongside `assets/fonts/fonts.css`.

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
- Visible keyboard focus: 2px `oxford` outline on light, `oldgold` navy
  variant `#C8A85E` on oxford.
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
