# Sponsorship Prospectus

The OQTS Sponsorship Prospectus 2026–27, generated from the 2025–26 Google Docs
original and re-set in the house brand (`../brand.md` v1.1).

The `.docx` is the source of record; the `.pdf` is produced from it by
LibreOffice, so the two cannot drift.

```
tiers.yml   the tier matrix: fees and the twenty benefit rows
contacts.yml  the section 8 contact cards
source/     the original Google Docs export, kept for verification
out/        the deliverables: .docx and .pdf
```

**None of those four are in this repository, and none should be.**
`oqts-design` is public. The tier matrix is the commercial substance of
the prospectus: four tiers, their fees, and what each one buys.
`contacts.yml` holds personal mobile numbers, one of them belonging to
someone other than the repo owner. Their home is Google Drive, per
`../../planning/DATA-HOMES.md`. The typesetting tooling is tracked here;
the data it renders is not.

Fetch all four from Drive before building. `build.py` exits with a
pointer to this file if `tiers.yml` or `contacts.yml` is missing, and
`compare_text.py` cannot run without `source/`.

**Neither directory is in this repository, and neither should be.**
`oqts-design` is public, and the prospectus carries sponsorship tier
pricing and the sponsor list. Those are private commercial documents and
their home is Google Drive, per `../../planning/DATA-HOMES.md`. The build
tooling is tracked here; what it produces is not.

Fetch both from Drive before building or verifying. `compare_text.py` in
particular cannot run without `source/`.

## Build

```bash
uv run --with python-docx --with pyyaml python build.py
soffice --headless --convert-to pdf --outdir out out/OQTS_Sponsorship_Prospectus_2026-27.docx
```

Both brand faces must be installed system-wide or the render silently
substitutes. On this machine they already are; `fc-list | grep -iE "latin
modern mono|stix two"` should return seven entries.

## Verify

Three checks, all of which should be run after any edit.

```bash
uv run --with python-docx python check_docx.py                      # OOXML validity
uv run --with python-docx --with pymupdf python compare_text.py     # wording vs original
uv run --with python-docx --with pymupdf python verify_table.py     # tier matrix, cell by cell
```

- **check_docx.py** walks every `pPr` / `rPr` / `tblPr` / `tcPr` / `trPr` in
  every part and compares child order against the schema sequence. OOXML
  property elements are strict sequences; append in the wrong order and Word
  refuses the file outright. Expect *ordering OK across all parts*.
- **compare_text.py** diffs the built document against the original PDF at word
  level, having applied the authorised substitutions listed in `AUTHORISED` to
  the original first. The new sponsors section is excised before diffing, so
  the check still proves that inserting it disturbed nothing else. Expect
  **11 differences**, all glyph or heading formatting.
- **verify_table.py** checks the sponsorship matrix directly, since the word
  diff canonicalises ticks and dashes and would hide a transcription error in
  exactly the place it matters most. Expect **20/20 rows exact**.

## Things that bite

- **Column widths must be set twice.** Word reads them from each cell (`tcW`),
  LibreOffice from `tblGrid`. Set only one and the table renders with equal
  columns in the other. `set_widths()` does both.
- **The closing double rule is a paragraph border, not a paragraph.** As its
  own paragraph it lands on a page by itself whenever a section ends flush
  with the page bottom.
- **`cantSplit` does not keep a table together.** It keeps a *row* intact.
  Use `keep_table_together()` for short tables that must not break.
- **No italic cut ships in the brand asset set.** `italic=True` makes the
  renderer shear the roman, which is a fake italic. Secondary text is roman in
  `slate` instead. Add STIX Two Text Italic to `../assets/fonts` if italics are
  ever wanted.
- **Latin Modern Mono's bold cut reports its family as `Latin Modern Mono
  Light`**, so asking for `Latin Modern Mono` + bold silently fails and gets
  faux-bolded. Nothing requests it today; keep it that way.
- **Sponsors are read from `../../oqts-site/data/sponsors.yml`** at build time,
  per brand.md §11. Edit them there, not here.
