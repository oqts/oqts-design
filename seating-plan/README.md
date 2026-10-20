# Seating plan

Typesets an event seating plan from a seating spreadsheet, in the house brand
(`../brand.md` v1.1). First used for the OQTS Launch Dinner, October 2026.

Two PDFs, both portrait:

```
OQTS_Seating_Plan_Easel_A1.pdf     for the easels in the room
  page 1  the plan: every round table, chairs numbered clockwise from the top,
          sponsors in navy with their firm, committee in camel
  page 2  find your table: every name A to Z by first name, with its table
OQTS_Seating_Plan_Catering_A3.pdf  for the venue and the committee
  page 1  the same plan, with each guest's dietary note under their name
  page 2  a ledger of every guest with a requirement, by table and seat
```

The easel plan is vector throughout, so the A1 file prints sharp at A2 or A0.
The catering copy is the A1 layout set at half scale.

**The spreadsheet and the PDFs are not in this repository, and never should
be.** `oqts-design` is public, and both hold names and dietary requirements,
some of them health or religious information. Their home is Google Drive, per
`../../planning/DATA-HOMES.md`. `build.py` refuses a sheet or an output folder
inside this repository. The tooling is tracked here; what it reads and writes
is not.

## The spreadsheet

One row per seat, first sheet, headers in row 1:

| Column | Holds |
|---|---|
| `Table` | Table number. Used only when `Table name` is not `Table N`. |
| `Table name` | `Table N`, or a name such as a sponsor's (shown on the table). |
| `Seat` | 1 to N, clockwise from the top. |
| `Name` | Blank for an open seat. A trailing `(note)` is dropped from display. |
| `Role` | `sponsor`, `committee`, `student`, or anything else (shown as a guest). |
| `Firm or college` | Shown under sponsors' names, and under anyone else's if filled. |
| `Level` | Not printed. |
| `Dietary`, `Meal` | Catering copy only. |

Make every seat and table change in the spreadsheet, then rebuild. The sheet
is the source of record; the PDFs are derived and never edited.

## Build

```bash
uv run --with openpyxl --with weasyprint python build.py PATH/TO/sheet.xlsx \
    --title "OQTS Launch Dinner" \
    --line "Wednesday 28 October 2026, the Divinity School" \
    --out PATH/OUTSIDE/THIS/REPO
```

Both brand faces must be installed system-wide or the SVG text inside each
table silently falls back to DejaVu. Check with `pymupdf`'s `get_fonts()` that
only `Latin-Modern-Mono` and `STIX-Two-Text` are embedded.

## Things that bite

- **WeasyPrint does not cascade page CSS into inline SVG.** A `class` on an SVG
  `<text>` is ignored and the text comes out at 16 units in DejaVu Sans. Every
  SVG text carries its font as attributes, via `text()` and the `TEXT` table.
- **No italic cut ships in the brand asset set**, so nothing here is italic;
  `font-style: italic` would shear the roman. Secondary text is `slate`.
- **The diamond marking a dietary line is drawn, not typed.** `◆` is in
  neither brand face and pulls in a fallback font.
- **Layout is tuned for ten tables of ten**: two columns of five on A1. Seat
  count per table is free (labels respace above five a side), but more than
  ten tables will run off the page.
