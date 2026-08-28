# oqts-design: agent guidance

Read `../.github/CLAUDE.md` first. Human overview is `README.md`.

## What this repo is

Public. **The single editable source of truth for all OQTS styling.**
`oqts-site`, `oqts-platform` and the OXDAQ dashboards consume from here
via a git submodule and never define styling of their own.

`brand.md` explains and specifies. `demo/index.html` shows. Every rule in
the doc has a worked example on the demo page. Read `brand.md` before
writing a single style, anywhere in the org.

```bash
python3 -m http.server 8001 -d .   # demo/ is the visual reference
```

## The rules that get broken most

- **Never hand-code a hex value**, in this repo or any consumer. Every
  colour is a `--oqts-*` token in `assets/oqts.css`. Reach for a role,
  never a number.
- **Never hand-draw or CSS-approximate an asset.** Logos, matrix devices
  and dot patterns are *generated* from a spec by `lab/tools/`, so the
  numbers in `brand.md` and the artwork cannot drift apart. Regenerate,
  do not edit the output.
  - `build-logos.py` (the spec lives at the top of that file, and it is
    the only place those numbers are edited)
  - `build-matrix.py`, `build-patterns.mjs`, `build-exports.py`
- **Colour is measured, never eyeballed.** Every contrast figure in
  `brand.md` came from a calculation and every chart hue from the
  palette validator. **Re-validate after any change** to the data
  palette.
- **There is one ground and no dark mode.** `ivory` is the base;
  `oxford` is a band (title bar and footer), not a second theme. Navy
  opens and closes a page and does nothing in between.
- **One gold, two roles.** `bronze` for accent text, `camel` for rules
  and detail. They never swap: `camel` is 2.9:1 on ivory and is never
  used for text.
- **No em-dashes** in any copy on a surface we ship, UI microcopy
  included. Colon, comma, or full stop.

## Changing the brand

A change here propagates to every consumer, so it is always a design
decision. Present it before making it.

Consumers pin this repo as a submodule and copy assets in via their own
`scripts/sync-brand.mjs`. A brand change reaches a site only when that
consumer bumps its submodule pin and commits it. Bumping a consumer's
pin is a separate change set in that repo.

## Open items in brand.md

- Convert both faces to WOFF2 and subset before production (`TODO`, §5).
- Source Sans 3 for interface chrome if the platform's density outgrows
  a serif. **Do not introduce it pre-emptively** (§3).
- A dashboard subsection covering tabular density, live-updating numeric
  cells and status treatment, for the OXDAQ competition screens. Not yet
  written. The overarching theme does not change.
