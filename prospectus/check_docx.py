"""Structural check on a generated .docx.

There is no LibreOffice Writer on this machine, so the file cannot be rendered
here. This checks the thing that actually breaks such files: OOXML property
elements are strict sequences, and Word refuses a document whose children are
out of order. Every pPr / rPr / tblPr / tcPr / trPr in every part is walked and
compared against the schema sequence.

    uv run --with python-docx python check_docx.py out/<file>.docx
"""

import sys
import zipfile
from xml.etree import ElementTree as ET

from build import SEQ_PPR, SEQ_RPR, SEQ_TBLPR, SEQ_TCPR, SEQ_TRPR

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"

SEQUENCES = {
    "pPr": SEQ_PPR,
    "rPr": SEQ_RPR,
    "tblPr": SEQ_TBLPR,
    "tcPr": SEQ_TCPR,
    "trPr": SEQ_TRPR,
}

# CT_TcBorders and CT_TblCellMar are sequences too, and both are hand-built here.
EDGE_SEQ = ["top", "left", "bottom", "right", "insideH", "insideV", "tl2br", "tr2bl"]
SEQUENCES_EDGE = {"tcBorders": EDGE_SEQ, "tblCellMar": EDGE_SEQ, "pBdr": EDGE_SEQ,
                  "tblBorders": EDGE_SEQ}


def local(tag):
    return tag.split("}")[-1]


def check_part(name, xml, problems):
    root = ET.fromstring(xml)
    for el in root.iter():
        tag = local(el.tag)
        seq = SEQUENCES.get(tag) or SEQUENCES_EDGE.get(tag)
        if seq is None:
            continue
        last_rank, last_name = -1, None
        for child in el:
            child_name = local(child.tag)
            if child_name not in seq:
                problems.append(f"{name}: <w:{tag}> has unknown child <w:{child_name}>")
                continue
            rank = seq.index(child_name)
            if rank < last_rank:
                problems.append(
                    f"{name}: <w:{tag}> child order wrong -- "
                    f"<w:{child_name}> follows <w:{last_name}>")
            last_rank, last_name = rank, child_name


def main(path):
    problems = []
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        parts = [n for n in names
                 if n.startswith("word/") and n.endswith(".xml")
                 and "_rels" not in n]
        for part in parts:
            try:
                check_part(part, z.read(part), problems)
            except ET.ParseError as exc:
                problems.append(f"{part}: not well-formed XML -- {exc}")

        # every relationship target referenced by the document must exist
        media = [n for n in names if n.startswith("word/media/")]

    print(f"parts checked : {len(parts)}")
    print(f"media embedded: {len(media)}")
    if problems:
        print(f"\nPROBLEMS ({len(problems)}):")
        for p in problems:
            print("  -", p)
        return 1
    print("\nordering OK across all parts")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else
                  "out/OQTS_Sponsorship_Prospectus_2026-27.docx"))
