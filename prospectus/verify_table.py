"""Verify the sponsorship tier matrix cell by cell against the original PDF.

The word-level diff maps every tick and dash onto canonical tokens, which makes
a genuine transcription error in the matrix look the same as a deliberate glyph
change. This checks the matrix directly: for each benefit row it reads the four
tier values out of the original PDF's text stream and compares them with the
four values in the rebuilt .docx.

    uv run --with python-docx --with pymupdf python verify_table.py
"""

import re
import sys
import unicodedata
from pathlib import Path

import pymupdf
from docx import Document
from docx.oxml.ns import qn
from docx.table import Table

HERE = Path(__file__).resolve().parent
ORIGINAL = HERE / "source" / "OQTS_Sponsorship_Prospectus_original.pdf"
REBUILT = HERE / "out" / "OQTS_Sponsorship_Prospectus_2026-27.docx"

YES, NO = "YES", "NO"
MARKERS = {"✓": YES, "•": YES, "—": NO, "–": NO}


def canon(s):
    s = unicodedata.normalize("NFKC", s)
    s = s.replace("​", "").replace(" ", " ")
    return re.sub(r"\s+", " ", s).strip()


def key(s):
    """Comparison key for a benefit label: letters and digits only."""
    return re.sub(r"[^a-z0-9]", "", canon(s).lower())


def original_rows():
    """Walk the original's text stream, pairing each label with the next 4 marks."""
    doc = pymupdf.open(ORIGINAL)
    tokens = []
    for page in doc:
        for line in page.get_text().splitlines():
            line = canon(line)
            if line:
                tokens.append(line)

    rows, i = [], 0
    while i < len(tokens):
        tok = tokens[i]
        if tok in MARKERS or re.fullmatch(r"£[\d,]+|\d+", tok):
            i += 1
            continue
        # collect label lines until we hit 4 consecutive value tokens
        label_parts = [tok]
        j = i + 1
        while j < len(tokens) and not (
                tokens[j] in MARKERS or re.fullmatch(r"£[\d,]+|\d+", tokens[j])):
            label_parts.append(tokens[j])
            j += 1
        values = []
        k = j
        while k < len(tokens) and len(values) < 4:
            t = tokens[k]
            if t in MARKERS:
                values.append(MARKERS[t])
            elif re.fullmatch(r"£[\d,]+|\d+", t):
                values.append(t)
            else:
                break
            k += 1
        if len(values) == 4:
            rows.append((" ".join(label_parts), values))
        i = j if j > i else i + 1
    return rows


def rebuilt_rows():
    doc = Document(REBUILT)
    tables = [Table(c, doc) for c in doc.element.body.iterchildren()
              if c.tag == qn("w:tbl")]
    # the tier matrix is the 5-column table
    matrix = [t for t in tables if len(t.columns) == 5]
    if len(matrix) != 1:
        sys.exit(f"expected exactly one 5-column table, found {len(matrix)}")
    rows = []
    for row in matrix[0].rows:
        cells = row.cells
        # band rows are merged across all five columns, so every entry in
        # row.cells points at the same <w:tc>
        if len({id(c._tc) for c in cells}) < 5:
            continue
        values = [canon(c.text) for c in cells[1:5]]
        if not any(values):
            continue
        rows.append((canon(cells[0].text), [MARKERS.get(v, v) for v in values]))
    return rows


def main():
    # A label in the original may have absorbed the band heading or page
    # furniture that precedes it, so match on suffix rather than equality.
    orig = [(key(l), l, v) for l, v in original_rows()]
    built = rebuilt_rows()

    checked, problems, matched_keys = 0, [], set()
    for label, values in built:
        k = key(label)
        if k == "benefit":
            continue
        hits = [(ok, ol, ov) for ok, ol, ov in orig if ok.endswith(k)]
        if not hits:
            problems.append(f"row not found in original: {label!r}")
            continue
        if len(hits) > 1:
            problems.append(f"row ambiguous in original ({len(hits)} hits): {label!r}")
            continue
        ok, o_label, o_values = hits[0]
        matched_keys.add(ok)
        checked += 1
        if o_values != values:
            problems.append(
                f"{label!r}\n      original: {o_values}\n      rebuilt : {values}")

    print(f"rows parsed from original : {len(orig)}")
    print(f"rows in rebuilt matrix    : {len(built) - 1}")
    print(f"rows compared             : {checked}")

    missing = [ol for ok, ol, _ in orig if ok not in matched_keys]
    if missing:
        print(f"\nin original but not matched to a rebuilt row ({len(missing)}):")
        for m in missing:
            print("  -", m[-120:])

    if problems:
        print(f"\nMISMATCHES ({len(problems)}):")
        for p in problems:
            print("  -", p)
        return 1
    print("\nevery compared row matches the original exactly")
    return 0


if __name__ == "__main__":
    sys.exit(main())
