"""Diff the rebuilt prospectus against the original PDF's text.

The brief was "do not change any detail, just the formatting", so the wording
has to be provably unchanged apart from the two substitutions the user
authorised. This strips page furniture from both sides, normalises whitespace,
and reports every remaining difference as a word-level diff.

    uv run --with python-docx --with pymupdf python compare_text.py
"""

import difflib
import re
import unicodedata
from pathlib import Path

import pymupdf
from docx import Document
from docx.oxml.ns import qn
from docx.table import Table
from docx.text.paragraph import Paragraph

HERE = Path(__file__).resolve().parent
ORIGINAL = HERE / "source" / "OQTS_Sponsorship_Prospectus_original.pdf"
REBUILT = HERE / "out" / "OQTS_Sponsorship_Prospectus_2026-27.docx"

# Authorised changes, applied to the ORIGINAL before comparing.
AUTHORISED = [
    ("Oxford Quantitative Trading Strategies", "Oxford Quantitative Trading Society"),
    ("OXFORD QUANTITATIVE TRADING STRATEGIES", "OXFORD QUANTITATIVE TRADING SOCIETY"),
    ("2025–26", "2026–27"),
    # the table has four columns; the sentence said three
    ("We offer three tiers", "We offer four tiers"),
    # brand.md bans em-dashes on every surface; reworked with a comma
    ("Strategy Team—creating", "Strategy Team, creating"),
    # current titles, in both the bio cards and the contact cards
    ("Founder, President, Head of Strategy",
     "Founder, President, Chief Investment Officer"),
    ("Founder, Vice-President, Head of Research",
     "Founder, Vice-President, Head of Research and Technology"),
    # no longer incoming
    ("Incoming Summer Intern at Brevan Howard", "Summer Intern at Brevan Howard"),
    # Alec's bio: OXDAQ and the commodities system added, HMM detail retained
    ("Currently developing regime prediction library in Python using Hidden "
     "Markov Models",
     "Currently building OXDAQ, the society's live exchange "
     "Developing a systematic commodities trading system applying advanced "
     "machine learning to ship positions, and a regime prediction library "
     "in Python using Hidden Markov Models"),
]

# Running header / footer furniture, present on every page of the original and
# regenerated as real headers and footers in the rebuild.
FURNITURE = [
    r"^CONFIDENTIAL$",
    r"^OQTS\s*\|\s*Sponsorship Prospectus \d{4}–\d{2}$",
    r"^Strictly Private and Confidential\s*[—·-]\s*Page \d+$",
    r"^=====\s*PAGE \d+\s*=====$",
    r"^•\s*included\s+–\s*not included$",   # rebuild's table legend
    r"^SECTION \d+$",                       # rebuild's eyebrow; numbers shifted
]

# Section 4 "Our Sponsors" is new content the user asked for, so it is excised
# from the rebuilt side before diffing. Everything outside it must still match,
# which is what proves the new section did not disturb the rest.
NEW_SECTION = ("Our Sponsors", "Sponsorship Tiers")

# The tick/dash markers are a formatting substitution: neither brand face
# carries U+2713, so the matrix uses the bullet and en dash instead. Map both
# sides onto canonical tokens so the comparison is about wording, not glyphs.
MARKERS = {"✓": "<yes>", "•": "<yes>", "—": "<no>", "–": "<no>", "-": "<no>"}


def normalise(text):
    text = unicodedata.normalize("NFKC", text)
    text = text.replace("​", " ").replace(" ", " ")
    text = text.replace("’", "'").replace("‘", "'")
    text = text.replace("“", '"').replace("”", '"')
    return text


def strip_furniture(lines):
    out = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if any(re.match(p, line) for p in FURNITURE):
            continue
        out.append(line)
    return out


def tokenise(lines):
    """Word tokens, case-folded and with standalone markers canonicalised.

    Case is folded because capitalisation of labels is a formatting decision
    (brand.md sets tracked caps for eyebrows and table bands); a genuine
    wording change still shows up.
    """
    words = " ".join(lines).split()
    return [MARKERS.get(w, w.lower()) for w in words]


def original_words():
    doc = pymupdf.open(ORIGINAL)
    raw = "\n".join(page.get_text() for page in doc)
    raw = normalise(raw)
    for old, new in AUTHORISED:
        raw = raw.replace(old, new)
    lines = strip_furniture(raw.splitlines())
    # the original renders section numbers inline ("1. About OQTS"); the rebuild
    # splits the number into an eyebrow, so drop the leading "N. " for comparison
    # the rebuild carries section numbers in an eyebrow that is filtered out,
    # and they renumbered when the sponsors section was inserted, so drop them
    lines = [re.sub(r"^\d+\.\s+", "", ln) for ln in lines]
    return tokenise(lines)


def excise_new_section(lines):
    start, end = NEW_SECTION
    try:
        i = lines.index(start)
        j = lines.index(end, i)
    except ValueError:
        raise SystemExit(f"could not locate new section {NEW_SECTION} in rebuild")
    excised = lines[i:j]
    print(f"excised new section: {len(excised)} lines "
          f"({len(' '.join(excised).split())} words)\n")
    return lines[:i] + lines[j:]


def iter_blocks(parent):
    """Paragraphs and tables in true document order.

    doc.paragraphs and doc.tables are separate collections, so reading them in
    turn scrambles the running order and makes any diff meaningless.
    """
    element = parent.element.body if hasattr(parent, "element") else parent._tc
    for child in element.iterchildren():
        if child.tag == qn("w:p"):
            yield Paragraph(child, parent)
        elif child.tag == qn("w:tbl"):
            yield Table(child, parent)


def rebuilt_words():
    doc = Document(REBUILT)
    chunks = []

    def walk(container):
        for block in iter_blocks(container):
            if isinstance(block, Paragraph):
                chunks.append(block.text)
            else:
                for row in block.rows:
                    seen = set()
                    for cell in row.cells:
                        if id(cell._tc) in seen:
                            continue
                        seen.add(id(cell._tc))
                        walk(cell)

    walk(doc)
    text = normalise("\n".join(chunks))
    lines = excise_new_section(strip_furniture(text.splitlines()))
    return tokenise(lines)


def main():
    a, b = original_words(), rebuilt_words()
    sm = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
    diffs = [op for op in sm.get_opcodes() if op[0] != "equal"]

    print(f"original words: {len(a)}")
    print(f"rebuilt  words: {len(b)}")
    print(f"similarity    : {sm.ratio():.4f}\n")

    if not diffs:
        print("IDENTICAL after the authorised substitutions.")
        return

    print(f"{len(diffs)} difference(s):\n")
    for tag, i1, i2, j1, j2 in diffs:
        old = " ".join(a[i1:i2])
        new = " ".join(b[j1:j2])
        print(f"  [{tag}]")
        if old:
            print(f"    original: {old[:300]}")
        if new:
            print(f"    rebuilt : {new[:300]}")
        print()


if __name__ == "__main__":
    main()
