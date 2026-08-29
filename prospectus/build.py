"""Build the OQTS Sponsorship Prospectus in the house brand.

Source: OQTS_Sponsorship_Prospectus_3.0.docx (Google Docs export), kept at
source/OQTS_Sponsorship_Prospectus_original.pdf. Wording is carried over
verbatim apart from the changes listed below, each of which was asked for and
each of which is registered in compare_text.py so the diff stays provable:

  1. "Strategies" -> "Society" in the society's name, so the document agrees
     with the logo lockup, brand.md, the site and data/society.yml.
  2. "2025-26" -> "2026-27" in the title and the running header.
  3. "three tiers" -> "four tiers": the matrix has four columns.
  4. The one em-dash reworked to a comma (brand.md bans them on every surface).
  5. Current titles: Chief Investment Officer, Head of Research and Technology.
  6. "Incoming Summer Intern" -> "Summer Intern".
  7. Alec's bio gains OXDAQ and the commodities system; the HMM library stays.
  8. New section 4, "Our Sponsors", read from the site's sponsors.yml.

The section 5 tier matrix is read from tiers.yml, which is deliberately not
in this repository: it is the commercial substance of the prospectus and
oqts-design is public. Fetch it from Google Drive before building.

Styling follows oqts-design/brand.md v1.1.

    uv run --with python-docx --with pyyaml python build.py
"""

from pathlib import Path

from docx import Document
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Mm, Pt, RGBColor

HERE = Path(__file__).resolve().parent
ASSETS = HERE.parent / "assets"
OUT = HERE / "out"
# Sponsors are edited in exactly one place (brand.md section 11), so read them
# rather than retyping. Fails loudly if the site repo moves.
SPONSORS_YML = HERE.parents[1] / "oqts-site" / "data" / "sponsors.yml"
# The tier matrix is commercial, not layout, so it is not in this public repo.
# It lives in Google Drive alongside out/ and source/. Fails loudly if absent.
TIERS_YML = HERE / "tiers.yml"
# Section 8 contact cards: personal mobile numbers, one of them not the
# repo owner's. Same treatment as the tier matrix, and for a stronger
# reason.
CONTACTS_YML = HERE / "contacts.yml"

# -- brand tokens (brand.md section 2) ---------------------------------------
IVORY = "FBF8F1"   # base ground
OXFORD = "002147"  # base ink, and the dark ground
PAPER = "F4EDDC"   # tint for panels, cards, bands
CHALK = "E0D5BC"   # hairlines and borders
SLATE = "46586A"   # supporting text on light
BRONZE = "8A6933"  # accent TEXT on light
CAMEL = "B08D57"   # accent RULES on light, never text
PAPER_REV = "F4EDDC"

# sponsor tier metals -- medal pins and rules only, never text
TIER_METAL = {
    "Bronze": "9C5F35",
    "Silver": "A6ADB5",
    "Gold": "C9A24B",
    "Founder": CAMEL,
}

DISPLAY = "Latin Modern Mono"  # logo, display, headings, eyebrows, figures
TEXT = "STIX Two Text"         # body copy

# Latin Modern is drawn at a 10pt optical size and renders thin. brand.md sets
# a 13px screen floor; in print the equivalent restraint is to keep mono
# furniture at 8.5pt or above and never reverse it small.
S_TITLE = 23
S_COVER_SUB = 13
S_LEDE = 12
S_SECTION = 16
S_SUB = 12
S_BODY = 11
S_EYEBROW = 10
S_TABLE_HEAD = 10
S_TABLE = 10.5
S_MICRO = 9

YES = "•"   # bullet -- "included". Neither brand face carries U+2713.
NO = "–"    # en dash -- "not included"
NO_INK = SLATE  # chalk is 1.4:1 and brand.md forbids it for text; slate is 6.9:1


# -- low-level helpers -------------------------------------------------------

def _el(tag, **attrs):
    e = OxmlElement(tag)
    for k, v in attrs.items():
        e.set(qn("w:" + k), str(v))
    return e


# OOXML property elements are strict sequences: appending is not enough, Word
# and LibreOffice both reject a file whose children are out of order.
SEQ_PPR = ["pStyle", "keepNext", "keepLines", "pageBreakBefore", "framePr",
           "widowControl", "numPr", "suppressLineNumbers", "pBdr", "shd", "tabs",
           "suppressAutoHyphens", "kinsoku", "wordWrap", "overflowPunct",
           "topLinePunct", "autoSpaceDE", "autoSpaceDN", "bidi", "adjustRightInd",
           "snapToGrid", "spacing", "ind", "contextualSpacing", "mirrorIndents",
           "suppressOverlap", "jc", "textDirection", "textAlignment",
           "textboxTightWrap", "outlineLvl", "divId", "cnfStyle", "rPr", "sectPr"]

SEQ_RPR = ["rStyle", "rFonts", "b", "bCs", "i", "iCs", "caps", "smallCaps",
           "strike", "dstrike", "outline", "shadow", "emboss", "imprint",
           "noProof", "snapToGrid", "vanish", "webHidden", "color", "spacing",
           "w", "kern", "position", "sz", "szCs", "highlight", "u", "effect",
           "bdr", "shd", "fitText", "vertAlign", "rtl", "cs", "em", "lang"]

SEQ_TBLPR = ["tblStyle", "tblpPr", "tblOverlap", "bidiVisual",
             "tblStyleRowBandSize", "tblStyleColBandSize", "tblW", "jc",
             "tblCellSpacing", "tblInd", "tblBorders", "shd", "tblLayout",
             "tblCellMar", "tblLook", "tblCaption", "tblDescription"]

SEQ_TCPR = ["cnfStyle", "tcW", "gridSpan", "hMerge", "vMerge", "tcBorders",
            "shd", "noWrap", "tcMar", "textDirection", "tcFitText", "vAlign",
            "hideMark"]

SEQ_TRPR = ["cnfStyle", "divId", "gridBefore", "gridAfter", "wBefore", "wAfter",
            "cantSplit", "trHeight", "tblHeader", "tblCellSpacing", "jc", "hidden"]


def _tag(el):
    return el.tag.split("}")[-1]


def insert_ordered(parent, child, seq, *, replace=True):
    """Insert `child` into `parent` at its schema position, replacing any existing."""
    name = _tag(child)
    if replace:
        for existing in parent.findall(qn("w:" + name)):
            parent.remove(existing)
    rank = seq.index(name)
    for el in parent:
        other = _tag(el)
        if other not in seq or seq.index(other) > rank:
            el.addprevious(child)
            return child
    parent.append(child)
    return child


def style_run(run, *, font=TEXT, size=S_BODY, color=OXFORD,
              bold=False, italic=False, track=None, caps=False):
    """Apply a face, size, colour and optional letter-spacing to a run.

    `track` is em-relative, matching brand.md's tracking figures; Word wants
    twentieths of a point, so it is converted against the run's own size.
    """
    run.font.name = font
    run.font.size = Pt(size)
    run.font.color.rgb = RGBColor.from_string(color)
    run.font.bold = bold
    run.font.italic = italic
    rpr = run._element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = insert_ordered(rpr, _el("w:rFonts"), SEQ_RPR)
    for attr in ("ascii", "hAnsi", "cs"):
        rfonts.set(qn("w:" + attr), font)
    if track:
        insert_ordered(rpr, _el("w:spacing", val=int(round(track * size * 20))),
                       SEQ_RPR)
    if caps:
        run.text = run.text.upper()
    return run


def para(container, text="", *, align=None, space_before=0, space_after=6,
         line=1.5, indent_left=0, keep_with_next=False, **run_kw):
    p = container.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(space_before)
    pf.space_after = Pt(space_after)
    pf.line_spacing = line
    pf.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    pf.left_indent = Pt(indent_left)
    pf.keep_with_next = keep_with_next
    pf.widow_control = True
    if align is not None:
        p.alignment = align
    if text:
        style_run(p.add_run(text), **run_kw)
    return p


def rich(container, parts, *, align=None, space_before=0, space_after=6,
         line=1.38, base=None):
    """A paragraph built from (text, override_kwargs) pairs, for inline emphasis."""
    base = dict(base or {})
    p = para(container, align=align, space_before=space_before,
             space_after=space_after, line=line)
    for text, over in parts:
        kw = {**base, **over}
        style_run(p.add_run(text), **kw)
    return p


def _borders(pf_el, **edges):
    """Attach w:pBdr edges. Each edge is (val, eighths_of_pt, space_pt, colour)."""
    pbdr = _el("w:pBdr")
    for edge in ("top", "bottom"):
        spec = edges.get(edge)
        if spec:
            val, sz, space, color = spec
            pbdr.append(_el("w:" + edge, val=val, sz=sz, space=space, color=color))
    insert_ordered(pf_el, pbdr, SEQ_PPR)


def hairline(container, *, space_before=4, space_after=10, keep_with_next=False):
    """A single chalk hairline -- opens a section (brand.md section 4)."""
    p = para(container, space_before=space_before, space_after=space_after,
             line=1, keep_with_next=keep_with_next)
    p.paragraph_format.space_after = Pt(space_after)
    _borders(p._p.get_or_add_pPr(), bottom=("single", 6, 1, CHALK))
    style_run(p.add_run(""), size=1)
    return p


def close_section(doc):
    """Draw the ledger double rule on the section's own last paragraph.

    Emitted as a paragraph of its own it is free to land on a page by itself
    when a section ends flush with the page bottom, which is exactly what
    happened: page 3 of the last export carried the rule and nothing else.
    Bound to the last paragraph it cannot be separated from the copy it closes.
    A section ending in a table needs nothing, since the table already carries
    a closing double rule on its final row.
    """
    last = None
    for child in doc.element.body.iterchildren():
        if child.tag == qn("w:p"):
            # only a paragraph carrying text is a safe anchor; an empty spacer
            # can be pushed onto a page of its own exactly like a rule can
            if "".join(child.itertext()).strip():
                last = child
        elif child.tag == qn("w:tbl"):
            last = None
    if last is None:
        return
    ppr = last.get_or_add_pPr()
    _borders(ppr, bottom=("double", 6, 10, CAMEL))
    spacing = ppr.find(qn("w:spacing"))
    if spacing is None:
        spacing = insert_ordered(ppr, _el("w:spacing"), SEQ_PPR)
    spacing.set(qn("w:after"), "0")


def double_rule(container, *, space_before=14, space_after=14):
    """The ledger double rule in camel -- closes a section. Never decorative."""
    p = para(container, space_before=space_before, space_after=space_after, line=1)
    _borders(p._p.get_or_add_pPr(), bottom=("double", 6, 1, CAMEL))
    style_run(p.add_run(""), size=1)
    return p


# -- table helpers -----------------------------------------------------------

def shade(cell, color):
    insert_ordered(cell._tc.get_or_add_tcPr(),
                   _el("w:shd", val="clear", fill=color), SEQ_TCPR)


def cell_borders(cell, **edges):
    """Merge edges into the cell's existing tcBorders rather than replacing it."""
    tcpr = cell._tc.get_or_add_tcPr()
    tcb = tcpr.find(qn("w:tcBorders"))
    if tcb is None:
        tcb = insert_ordered(tcpr, _el("w:tcBorders"), SEQ_TCPR)
    order = ["top", "left", "bottom", "right"]
    for edge in order:
        spec = edges.get(edge)
        if spec is None:
            continue
        for existing in tcb.findall(qn("w:" + edge)):
            tcb.remove(existing)
        if spec == "nil":
            el = _el("w:" + edge, val="nil")
        else:
            val, sz, color = spec
            el = _el("w:" + edge, val=val, sz=sz, space=0, color=color)
        rank = order.index(edge)
        for child in tcb:
            name = _tag(child)
            if name in order and order.index(name) > rank:
                child.addprevious(el)
                break
        else:
            tcb.append(el)


def cell_margins(table, top=4, bottom=4, left=8, right=8):
    mar = _el("w:tblCellMar")
    for edge, v in (("top", top), ("left", left), ("bottom", bottom), ("right", right)):
        mar.append(_el("w:" + edge, w=int(v * 20), type="dxa"))
    insert_ordered(table._tbl.tblPr, mar, SEQ_TBLPR)
    # Word aligns cell *content* to the margin, so the border hangs into the
    # margin by the left padding. Indent the table back by the same amount.
    insert_ordered(table._tbl.tblPr,
                   _el("w:tblInd", w=int(left * 20), type="dxa"), SEQ_TBLPR)


def cell_text(cell, text, *, align=WD_ALIGN_PARAGRAPH.LEFT, space=2, **run_kw):
    cell.text = ""
    p = cell.paragraphs[0]
    p.alignment = align
    pf = p.paragraph_format
    pf.space_before = Pt(space)
    pf.space_after = Pt(space)
    pf.line_spacing = 1.25
    pf.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    if text:
        style_run(p.add_run(text), **run_kw)
    cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    return p


TWIPS_PER_MM = 1440 / 25.4


def set_widths(table, widths_mm):
    table.autofit = False  # python-docx emits w:tblLayout itself
    # pin the overall width too, or Word re-fits the table on open
    total = int(sum(widths_mm) * TWIPS_PER_MM)
    insert_ordered(table._tbl.tblPr, _el("w:tblW", w=total, type="dxa"), SEQ_TBLPR)
    # Word takes column widths from the cells (tcW); LibreOffice takes them
    # from tblGrid, which python-docx leaves at equal defaults. Set both, or
    # the table renders with every column the same width in one of the two.
    grid = table._tbl.find(qn("w:tblGrid"))
    if grid is not None:
        for col, w in zip(grid.findall(qn("w:gridCol")), widths_mm):
            col.set(qn("w:w"), str(int(w * TWIPS_PER_MM)))
    for row in table.rows:
        for cell, w in zip(row.cells, widths_mm):
            cell.width = Mm(w)


def no_borders(table):
    borders = _el("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        borders.append(_el("w:" + edge, val="nil"))
    insert_ordered(table._tbl.tblPr, borders, SEQ_TBLPR)


def keep_row_together(row, repeat_header=False):
    trpr = row._tr.get_or_add_trPr()
    insert_ordered(trpr, _el("w:cantSplit"), SEQ_TRPR)
    if repeat_header:
        insert_ordered(trpr, _el("w:tblHeader"), SEQ_TRPR)


# -- document furniture ------------------------------------------------------

def set_page_background(doc, color):
    """Ivory ground (brand.md: 'there is one ground')."""
    bg = _el("w:background", color=color)
    doc.element.insert(0, bg)
    settings = doc.settings.element
    # CT_Settings is a strict sequence; displayBackgroundShape follows these.
    preceding = ["writeProtection", "view", "zoom", "removePersonalInformation",
                 "removeDateAndTime", "doNotDisplayPageBoundaries"]
    idx = 0
    for i, child in enumerate(settings):
        tag = child.tag.split("}")[-1]
        if tag in preceding:
            idx = i + 1
    settings.insert(idx, _el("w:displayBackgroundShape"))


def page_number_field(paragraph, **run_kw):
    for kind, attrs in (("begin", {}), (None, {}), ("end", {})):
        run = paragraph.add_run()
        style_run(run, **run_kw)
        if kind:
            run._r.append(_el("w:fldChar", fldCharType=kind))
        else:
            instr = OxmlElement("w:instrText")
            instr.set(qn("xml:space"), "preserve")
            instr.text = "PAGE"
            run._r.append(instr)


def build_header(section, title_line):
    hdr = section.header
    hdr.is_linked_to_previous = False
    p = hdr.paragraphs[0]
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1
    # left CONFIDENTIAL, right OQTS | <title>, on one tab-separated line
    tabs = p.paragraph_format.tab_stops
    tabs.add_tab_stop(Mm(146), WD_ALIGN_PARAGRAPH.RIGHT)
    style_run(p.add_run("CONFIDENTIAL"), font=DISPLAY, size=S_MICRO - 0.5,
              color=BRONZE, track=0.14)
    p.add_run("\t")
    style_run(p.add_run("OQTS"), font=DISPLAY, size=S_MICRO - 0.5,
              color=OXFORD, track=0.06)
    style_run(p.add_run("  |  " + title_line), font=DISPLAY,
              size=S_MICRO - 0.5, color=SLATE)
    _borders(p._p.get_or_add_pPr(), bottom=("single", 6, 6, CHALK))


def build_footer(section):
    ftr = section.footer
    ftr.is_linked_to_previous = False
    p = ftr.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.line_spacing = 1
    kw = dict(font=DISPLAY, size=S_MICRO - 0.5, color=SLATE)
    style_run(p.add_run("Strictly Private and Confidential"), **kw)
    style_run(p.add_run("  ·  Page "), **kw)
    page_number_field(p, **kw)


# -- content blocks ----------------------------------------------------------

def section_head(doc, number, title, *, first=False):
    """Eyebrow, heading, opening hairline (brand.md section 9).

    Every section opens a page. The closing double rule is emitted first, so it
    settles on the tail of the outgoing section rather than heading the new one.
    The eyebrow carries the break itself, rather than a separate break
    paragraph, so no empty paragraph is left behind to collect stray spacing.
    """
    if not first:
        close_section(doc)
    eyebrow = para(doc, f"Section {number}", font=DISPLAY, size=S_EYEBROW,
                   color=BRONZE, track=0.14, caps=True, space_before=0,
                   space_after=4, line=1.2, keep_with_next=True)
    eyebrow.paragraph_format.page_break_before = True
    para(doc, title, font=DISPLAY, size=S_SECTION, color=OXFORD, track=0.015,
         space_before=0, space_after=0, line=1.2, keep_with_next=True)
    # the rule must not be stranded from the copy it opens
    hairline(doc, space_before=6, space_after=10, keep_with_next=True)


def sub_head(doc, title, *, page_break=False):
    p = para(doc, title, font=DISPLAY, size=S_SUB, color=OXFORD, track=0.02,
             space_before=10, space_after=5, line=1.3, keep_with_next=True)
    if page_break:
        p.paragraph_format.page_break_before = True
    return p


def body(doc, text, **kw):
    # 1.42 rather than 1.5: reclaims roughly a line every fourteen, which is
    # what stops a section spilling two lines onto a page of its own. No words
    # change. brand.md sets 1.65 for screen; print carries tighter leading.
    return para(doc, text, font=TEXT, size=S_BODY, color=OXFORD,
                space_after=6, line=1.38, **kw)


def bullet(doc, text):
    p = para(doc, space_after=4, line=1.40, indent_left=18)
    p.paragraph_format.first_line_indent = Pt(-12)
    style_run(p.add_run("•   "), font=DISPLAY, size=S_BODY, color=CAMEL)
    style_run(p.add_run(text), font=TEXT, size=S_BODY, color=OXFORD)
    return p


def framed_panel(doc, width_mm=146):
    """A paper card with the 1px camel frame. Borderless paper cards do not
    exist in the system (brand.md section 4)."""
    t = doc.add_table(rows=1, cols=1)
    set_widths(t, [width_mm])
    keep_row_together(t.rows[0])  # a card must never break across a page
    cell = t.cell(0, 0)
    shade(cell, PAPER)
    cell_borders(cell,
                 top=("single", 8, CAMEL), left=("single", 8, CAMEL),
                 bottom=("single", 8, CAMEL), right=("single", 8, CAMEL))
    cell_margins(t, top=8, bottom=8, left=10, right=10)
    cell.text = ""
    return cell


def build_cover(doc):
    para(doc, space_after=0, line=1)  # top air
    doc.paragraphs[-1].paragraph_format.space_after = Pt(46)

    logo = ASSETS / "logo-png" / "oqts-lockup-stacked-on-ivory@3x.png"
    p = para(doc, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=34, line=1)
    p.add_run().add_picture(str(logo), width=Mm(56))

    # The plate: the closing rule's construction bent into a frame around the
    # title area. No closing rule sits beneath a plate.
    t = doc.add_table(rows=1, cols=1)
    set_widths(t, [146])
    keep_row_together(t.rows[0])
    cell = t.cell(0, 0)
    cell_borders(cell,
                 top=("double", 6, CAMEL), left=("double", 6, CAMEL),
                 bottom=("double", 6, CAMEL), right=("double", 6, CAMEL))
    cell_margins(t, top=20, bottom=20, left=12, right=12)
    cell.text = ""

    title = cell.paragraphs[0]
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title.paragraph_format.space_after = Pt(0)
    title.paragraph_format.line_spacing = 1.16
    style_run(title.add_run("OXFORD QUANTITATIVE"), font=DISPLAY, size=S_TITLE,
              color=OXFORD, track=0.015)
    p2 = para(cell, "TRADING SOCIETY", align=WD_ALIGN_PARAGRAPH.CENTER,
              font=DISPLAY, size=S_TITLE, color=OXFORD, track=0.015,
              space_after=14, line=1.16)
    inner = para(cell, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=12, line=1)
    _borders(inner._p.get_or_add_pPr(), bottom=("single", 6, 1, CAMEL))
    style_run(inner.add_run(""), size=1)
    para(cell, "Sponsorship Prospectus 2026–27", align=WD_ALIGN_PARAGRAPH.CENTER,
         font=DISPLAY, size=S_COVER_SUB, color=OXFORD, track=0.02,
         space_after=0, line=1.3)

    para(doc, "The First Quantitative Trading Society at the University of Oxford",
         align=WD_ALIGN_PARAGRAPH.CENTER, font=TEXT, size=S_LEDE, color=SLATE,
         space_before=22, space_after=0, line=1.5)

    p = para(doc, space_after=0, line=1)
    p.paragraph_format.space_after = Pt(120)

    para(doc, "Strictly private and confidential", align=WD_ALIGN_PARAGRAPH.CENTER,
         font=DISPLAY, size=S_EYEBROW, color=BRONZE, track=0.14, caps=True,
         space_after=0, line=1.3)
    # no explicit break: section 1's eyebrow carries page_break_before


# -- the tier matrix ---------------------------------------------------------

def load_tiers():
    """Read the tier matrix from tiers.yml.

    The matrix is the commercial substance of the prospectus: four tiers,
    their fees, and the twenty benefit rows. oqts-design is public, so it
    is kept out of the repository and read at build time, exactly as the
    sponsor list already is (brand.md section 11).

    Returns:
        (tiers, rows), where tiers is a list of tier names and rows is a
        list of (kind, label, values) triples. `kind` is one of "fee",
        "band" or "row"; a band has no values.

    The int/string distinction in `values` is load-bearing and is
    preserved by YAML: a bare 1 becomes a tick, a quoted "1" becomes a
    literal 1 in the cell. See build_tier_table.
    """
    import yaml

    if not TIERS_YML.exists():
        raise SystemExit(
            f"tier matrix not found at {TIERS_YML}\n"
            "It is deliberately not in this repository: fetch tiers.yml from "
            "Google Drive alongside out/ and source/. See README.md."
        )
    data = yaml.safe_load(TIERS_YML.read_text())
    rows = [(r["kind"], r["label"], r.get("values")) for r in data["rows"]]
    return data["tiers"], rows


WIDTHS = [58, 22, 22, 22, 22]


def build_tier_table(doc, tier_names, tier_rows):
    t = doc.add_table(rows=len(tier_rows) + 1, cols=5)
    no_borders(t)
    set_widths(t, WIDTHS)
    cell_margins(t, top=5, bottom=5, left=7, right=7)

    head = t.rows[0]
    keep_row_together(head, repeat_header=True)
    cell_text(head.cells[0], "Benefit", font=DISPLAY, size=S_TABLE_HEAD,
              color=PAPER_REV, track=0.06)
    shade(head.cells[0], OXFORD)
    cell_borders(head.cells[0], bottom=("single", 8, OXFORD))
    for i, tier in enumerate(tier_names, start=1):
        c = head.cells[i]
        cell_text(c, tier, align=WD_ALIGN_PARAGRAPH.CENTER, font=DISPLAY,
                  size=S_TABLE_HEAD, color=PAPER_REV, track=0.06)
        shade(c, OXFORD)
        # the one sanctioned use of the tier metals: a rule at the tier label
        cell_borders(c, top=("single", 20, TIER_METAL[tier]),
                     bottom=("single", 8, OXFORD))

    for r, (kind, label, values) in enumerate(tier_rows, start=1):
        row = t.rows[r]
        keep_row_together(row)
        if kind == "band":
            # merge across the full width, or a long label wraps inside col 1
            merged = row.cells[0].merge(row.cells[4])
            shade(merged, PAPER)
            cell_borders(merged, top=("single", 8, CAMEL),
                         bottom=("single", 6, CHALK))
            cell_text(merged, label, font=DISPLAY, size=S_TABLE_HEAD - 0.5,
                      color=BRONZE, track=0.12, caps=True, space=4)
            continue

        emph = kind == "fee"
        cell_text(row.cells[0], label, font=TEXT, size=S_TABLE,
                  color=OXFORD, bold=emph)
        cell_borders(row.cells[0], bottom=("single", 6, CHALK))
        for i, v in enumerate(values, start=1):
            c = row.cells[i]
            if isinstance(v, int):
                mark, color = (YES, OXFORD) if v else (NO, NO_INK)
                cell_text(c, mark, align=WD_ALIGN_PARAGRAPH.CENTER, font=DISPLAY,
                          size=S_TABLE + 1, color=color)
            else:
                cell_text(c, v, align=WD_ALIGN_PARAGRAPH.CENTER, font=DISPLAY,
                          size=S_TABLE, color=OXFORD)
            cell_borders(c, bottom=("single", 6, CHALK))

    # closing double rule on the final row, as a table total would take
    for c in t.rows[-1].cells:
        cell_borders(c, bottom=("double", 6, CAMEL))

    para(doc, f"{YES}  included        {NO}  not included",
         font=DISPLAY, size=S_MICRO, color=SLATE, space_before=6,
         space_after=4, line=1.3)


TIER_SLUG_METAL = {
    "founder": CAMEL,
    "gold": TIER_METAL["Gold"],
    "silver": TIER_METAL["Silver"],
    "bronze": TIER_METAL["Bronze"],
}


def load_sponsors():
    """Read the confirmed sponsor list from the site's single source of truth."""
    import yaml

    if not SPONSORS_YML.exists():
        raise SystemExit(f"sponsor data not found at {SPONSORS_YML}")
    data = yaml.safe_load(SPONSORS_YML.read_text())
    tiers = []
    for tier in data["tiers"]:
        firms = []
        for s in tier["sponsors"]:
            blurb = " ".join(str(s.get("blurb", "")).split())
            firms.append((s["name"], blurb.replace("'", "’")))
        tiers.append((tier["name"], tier["slug"], firms))
    return tiers


def build_sponsor_table(doc, tiers):
    """Sponsors grouped by tier, in the same language as the tier matrix:
    a merged paper band per tier wearing that tier's metal rule."""
    rows = sum(1 + len(firms) for _, _, firms in tiers)
    t = doc.add_table(rows=rows, cols=2)
    no_borders(t)
    set_widths(t, [44, 102])
    cell_margins(t, top=6, bottom=6, left=7, right=7)

    r = 0
    for tier_name, slug, firms in tiers:
        band = t.rows[r]
        keep_row_together(band)
        merged = band.cells[0].merge(band.cells[1])
        shade(merged, PAPER)
        cell_borders(merged,
                     top=("single", 20, TIER_SLUG_METAL[slug]),
                     bottom=("single", 6, CHALK))
        cell_text(merged, tier_name, font=DISPLAY, size=S_TABLE_HEAD - 0.5,
                  color=BRONZE, track=0.12, caps=True, space=4)
        r += 1
        for name, blurb in firms:
            row = t.rows[r]
            keep_row_together(row)
            cell_text(row.cells[0], name, font=DISPLAY, size=S_TABLE,
                      color=OXFORD, track=0.02)
            cell_text(row.cells[1], blurb, font=TEXT, size=S_TABLE, color=SLATE)
            for c in row.cells:
                cell_borders(c, bottom=("single", 6, CHALK))
            r += 1

    for c in t.rows[-1].cells:
        cell_borders(c, bottom=("double", 6, CAMEL))


def keep_table_together(table):
    """Stop a short table breaking across a page.

    cantSplit only keeps an individual row intact; it does nothing to stop the
    table splitting between rows. Binding every row but the last to the one
    after it makes the whole table move as a unit.
    """
    for row in table.rows[:-1]:
        for cell in row.cells:
            for p in cell.paragraphs:
                p.paragraph_format.keep_with_next = True


def build_headcount_table(doc):
    rows = [("Management", "5"), ("Senior Analysts", "7"), ("Analysts", "8-12")]
    t = doc.add_table(rows=len(rows) + 1, cols=2)
    no_borders(t)
    set_widths(t, [58, 30])
    cell_margins(t, top=5, bottom=5, left=7, right=7)

    head = t.rows[0]
    keep_row_together(head, repeat_header=True)
    for i, label in enumerate(("Role", "Headcount")):
        c = head.cells[i]
        cell_text(c, label, align=WD_ALIGN_PARAGRAPH.LEFT if i == 0 else WD_ALIGN_PARAGRAPH.CENTER,
                  font=DISPLAY, size=S_TABLE_HEAD, color=PAPER_REV, track=0.06)
        shade(c, OXFORD)

    for r, (role, count) in enumerate(rows, start=1):
        row = t.rows[r]
        keep_row_together(row)
        cell_text(row.cells[0], role, font=TEXT, size=S_TABLE, color=OXFORD)
        cell_text(row.cells[1], count, align=WD_ALIGN_PARAGRAPH.CENTER,
                  font=DISPLAY, size=S_TABLE, color=OXFORD)
        edge = ("double", 6, CAMEL) if r == len(rows) else ("single", 6, CHALK)
        for c in row.cells:
            cell_borders(c, bottom=edge)

    keep_table_together(t)


def build_person(doc, name, role, college, points):
    cell = framed_panel(doc)
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(1)
    p.paragraph_format.line_spacing = 1.3
    style_run(p.add_run(name), font=DISPLAY, size=S_SUB, color=OXFORD, track=0.02)
    # role on its own line: run in beside the name it wraps mid-title on the
    # longer ones, and the contact cards already set it this way
    para(cell, role, font=DISPLAY, size=S_SUB - 1.5, color=BRONZE, track=0.02,
         space_after=1, line=1.3)
    para(cell, college, font=TEXT, size=S_BODY - 0.5, color=SLATE,
         space_after=6, line=1.4)
    for i, point in enumerate(points):
        q = para(cell, space_after=0 if i == len(points) - 1 else 3,
                 line=1.4, indent_left=16)
        q.paragraph_format.first_line_indent = Pt(-11)
        style_run(q.add_run("•   "), font=DISPLAY, size=S_BODY - 0.5, color=CAMEL)
        style_run(q.add_run(point), font=TEXT, size=S_BODY - 0.5, color=OXFORD)
    para(doc, space_after=0, line=1).paragraph_format.space_after = Pt(10)


def load_contacts():
    """Read the section 8 contact cards from contacts.yml.

    Kept out of this public repository because they are personal mobile
    numbers, one of them belonging to someone other than the repo owner.

    Returns:
        A list of dicts with name, role, email and phone.
    """
    import yaml

    if not CONTACTS_YML.exists():
        raise SystemExit(
            f"contact cards not found at {CONTACTS_YML}\n"
            "Deliberately not in this repository: fetch contacts.yml from "
            "Google Drive alongside tiers.yml. See README.md."
        )
    return yaml.safe_load(CONTACTS_YML.read_text())["contacts"]


def build_contact_card(doc, name, role, email, phone):
    cell = framed_panel(doc)
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.3
    style_run(p.add_run(name), font=DISPLAY, size=S_SUB, color=OXFORD, track=0.02)
    para(cell, role, font=TEXT, size=S_BODY - 0.5, color=SLATE,
         space_after=5, line=1.4)
    q = para(cell, space_after=0, line=1.45)
    style_run(q.add_run(email), font=DISPLAY, size=S_BODY - 1, color=BRONZE)
    style_run(q.add_run("     "), font=DISPLAY, size=S_BODY - 1, color=SLATE)
    style_run(q.add_run(phone), font=DISPLAY, size=S_BODY - 1, color=OXFORD)
    para(doc, space_after=0, line=1).paragraph_format.space_after = Pt(10)


# -- the document ------------------------------------------------------------

def build():
    doc = Document()
    set_page_background(doc, IVORY)

    normal = doc.styles["Normal"]
    normal.font.name = TEXT
    normal.font.size = Pt(S_BODY)
    normal.font.color.rgb = RGBColor.from_string(OXFORD)
    normal.paragraph_format.space_after = Pt(8)

    s = doc.sections[0]
    s.page_width, s.page_height = Mm(210), Mm(297)
    s.top_margin, s.bottom_margin = Mm(26), Mm(24)
    s.left_margin = s.right_margin = Mm(32)
    s.header_distance, s.footer_distance = Mm(13), Mm(13)
    s.different_first_page_header_footer = True
    build_header(s, "Sponsorship Prospectus 2026–27")
    build_footer(s)
    # cover keeps the footer but not the running header
    s.first_page_header.is_linked_to_previous = False
    fp = s.first_page_footer
    fp.is_linked_to_previous = False
    p = fp.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.line_spacing = 1
    kw = dict(font=DISPLAY, size=S_MICRO - 0.5, color=SLATE)
    style_run(p.add_run("Strictly Private and Confidential  ·  Page "), **kw)
    page_number_field(p, **kw)

    build_cover(doc)

    # -- 1 ------------------------------------------------------------------
    section_head(doc, 1, "About OQTS", first=True)
    rich(doc, [
        ("Oxford Quantitative Trading Society (OQTS) is the ", {}),
        ("first dedicated quantitative trading society", {"bold": True}),
        (" at the University of Oxford. We exist to bridge the gap between "
         "Oxford’s talent and the quantitative finance industry by providing "
         "our members with unparalleled exposure to systematic trading, "
         "quantitative research, and live strategy development. One of our "
         "primary aims is learning: we aim to create a highly selective society "
         "that receives top-quality teaching and lecturing on quantitative "
         "strategies, both from our partners and the faculty at Oxford.", {}),
    ], base=dict(font=TEXT, size=S_BODY, color=OXFORD), space_after=6)

    sub_head(doc, "Mission")
    body(doc, "To provide insight on and preparation for the world of quantitative "
              "trading by combining talks with rigorous academic foundations and "
              "hands-on experience in live, systematic macro trading.")

    sub_head(doc, "What Sets Us Apart")
    rich(doc, [
        ("Unlike generalist finance or investment societies, OQTS is exclusively "
         "focused on quantitative and systematic approaches to the markets. Our "
         "long-term objective is to construct and deploy macro-oriented "
         "quantitative strategies on a live exchange. Our focus is on ", {}),
        ("systematic macro strategies", {"bold": True}),
        (" (rather than high-frequency trading or similar), reflecting the "
         "practical infrastructure constraints of a student-society. It is highly "
         "likely that our ability to run complex and compute-heavy algorithms "
         "will be controlled by sponsorship levels - proof-of-concept for cloud "
         "computing and live data feeds has generated positive but expensive "
         "results.", {}),
    ], base=dict(font=TEXT, size=S_BODY, color=OXFORD), space_after=6)

    sub_head(doc, "Membership and Selection")
    body(doc, "OQTS will operate a two-tier membership model. The society will be "
              "open to all Oxford students who wish to attend speaker events, "
              "workshops, and networking sessions. For the core team itself, we will "
              "launch a highly competitive applications process for admission at the "
              "end of November, comprising testing in probability, statistics, and "
              "financial knowledge, followed by structured interviews assessing "
              "analytical reasoning, programming ability, and ambition. We expect the "
              "core team to consist of around 15-20 members, likely including some "
              "postgraduates.")
    body(doc, "We would appreciate guidance from sponsors on the design of this "
              "admissions test.")

    # -- 2 ------------------------------------------------------------------
    section_head(doc, 2, "Society Activities")
    sub_head(doc, "Phase 1: Speaker Events and Industry Engagement")
    body(doc, "To spread publicity, OQTS will focus on establishing a high-profile "
              "events programme. We intend to host senior practitioners from leading "
              "quantitative hedge funds, proprietary trading firms, systematic asset "
              "managers, and academic research groups. Events will include keynote "
              "lectures, fireside chats, panel discussions, and technical workshops "
              "covering topics such as:")
    for point in [
        "Factor investing and systematic macro strategy design",
        "Career pathways in quantitative research, trading, and technology",
        "Statistical arbitrage and mean-reversion frameworks",
        "Machine learning applications in alpha generation",
        "Risk management and portfolio construction for systematic funds",
    ]:
        bullet(doc, point)
    body(doc, "We greatly appreciate speakers from our sponsors, and we are also in "
              "touch with others beyond this immediate circle.",
         space_before=8)

    # Section 2 runs about 7% over a page, which left a two-line tail page.
    # Splitting at the Phase 1 / Phase 2 boundary is font-independent: it gives
    # two two-thirds-full pages instead of one full page and a stub, and it
    # cannot regress when the metrics change. Tightening spacing to claw back
    # two lines would only hold for whichever face happened to be installed.
    sub_head(doc, "Phase 2: The Strategy Team and Live Trading", page_break=True)
    rich(doc, [
        ("Once OQTS has built sufficient institutional credibility, we will recruit "
         "a Strategy Team of exceptional students through the competitive process "
         "described above. This team will be responsible for the full lifecycle of "
         "quantitative strategy development: ideation, data sourcing, backtesting, "
         "risk modelling, and ultimately live execution. ", {}),
        ("We believe this is our key differentiator - those who have been part of "
         "our strategy team will enter the workplace having already experienced "
         "many of the real-world issues that implementing strategies generates.",
         {"bold": True}),
    ], base=dict(font=TEXT, size=S_BODY, color=OXFORD), space_after=6)
    body(doc, "The Strategy Team will focus on macro-style systematic strategies, "
              "taking directional and relative-value positions informed by "
              "macroeconomic data, cross-asset momentum, carry, and value signals. "
              "Strategies will be deployed on a live exchange via an electronic "
              "execution platform.")
    body(doc, "We are still researching the logistics and legal issues surrounding "
              "this, but two Oxford societies already run live funds that do not "
              "require extensive paperwork and regulation. We will also establish "
              "clear safeguards including stop-loss procedures and strict "
              "prohibitions on leveraging and certain instruments. No money will be "
              "withdrawn from the fund once put in, and we aim to use initial "
              "sponsorship money as a seed investment.")

    # -- 3 ------------------------------------------------------------------
    section_head(doc, 3, "Why Sponsor OQTS?")
    body(doc, "Partnering with OQTS offers sponsors a direct and differentiated "
              "channel to Oxford’s most analytically talented students. Our "
              "hyper-selective Strategy Team recruitment process ensures that "
              "sponsors engage with candidates who have already demonstrated "
              "elite-level quantitative ability.")

    sub_head(doc, "Talent Pipeline")
    rich(doc, [
        ("Oxford consistently produces graduates who go on to thrive in "
         "quantitative finance. ", {}),
        ("By sponsoring OQTS, firms gain privileged, early access to the best of "
         "these candidates before they enter broader recruitment cycles. They will "
         "have experience and education that their peers cannot even get near.",
         {"bold": True}),
        (" The rigorous selection process for the Strategy Team functions as a "
         "pre-vetted talent pipeline.", {}),
    ], base=dict(font=TEXT, size=S_BODY, color=OXFORD), space_after=6)

    sub_head(doc, "Brand Visibility")
    body(doc, "OQTS will be the first and only purely quantitative trading society "
              "at Oxford, guaranteeing sponsors a unique position within the "
              "university’s financial societies landscape. Sponsor branding will "
              "feature prominently across our events, digital channels, and "
              "recruitment materials.")

    sub_head(doc, "Intellectual Engagement")
    body(doc, "Sponsors can contribute directly to the society’s intellectual "
              "programme by providing speakers, setting challenge problems, or "
              "mentoring the Strategy Team, creating authentic engagement that "
              "resonates with high-calibre candidates. It presents a unique "
              "opportunity for firms to market themselves to top candidates.")

    # -- 4 ------------------------------------------------------------------
    tiers = load_sponsors()
    total = sum(len(firms) for _, _, firms in tiers)
    section_head(doc, 4, "Our Sponsors")
    body(doc, f"OQTS is supported by {total} firms across the four tiers set out "
              "in the next section. They span quantitative research, market "
              "making, proprietary trading, and systematic asset management.")
    build_sponsor_table(doc, tiers)

    # -- 5 ------------------------------------------------------------------
    section_head(doc, 5, "Sponsorship Tiers")
    body(doc, "We offer four tiers of partnership, each designed to provide "
              "increasing levels of engagement and visibility. All packages are "
              "structured on an annual basis and are renewable at preferential terms.")
    tier_names, tier_rows = load_tiers()
    build_tier_table(doc, tier_names, tier_rows)

    # -- 6 ------------------------------------------------------------------
    section_head(doc, 6, "Use of Funds")
    body(doc, "Sponsorship contributions will be allocated across the following "
              "areas to ensure the sustainable growth and operational excellence "
              "of OQTS:")

    sub_head(doc, "Events Programme")
    body(doc, "Venue hire, catering, audio-visual equipment, and speaker hospitality "
              "for our termly programme of talks, panels, and workshops. A full "
              "spreadsheet of estimates is given too, but it is a rough estimate.")

    sub_head(doc, "Technology Infrastructure")
    body(doc, "Cloud computing resources for backtesting and strategy development, "
              "market data subscriptions, and execution platform costs once the "
              "Strategy Team commences live trading. We will tailor our use of cloud "
              "compute to our budget, not the other way around. Data feeds are "
              "expensive, but we hope to reach a sort of sponsorship deal with one "
              "of our partners on this (talks ongoing).")

    sub_head(doc, "Seed Capital")
    rich(doc, [
        ("A portion of sponsorship funds may be allocated as initial trading capital "
         "for the Strategy Team’s live strategies, subject to appropriate "
         "governance and risk controls. In the first year, this would be larger but "
         "in future years it would be strictly limited as a % of income. ", {}),
        ("All profits generated by the fund remain within the fund (as per other "
         "Oxford societies) - they may not be withdrawn.", {"bold": True}),
    ], base=dict(font=TEXT, size=S_BODY, color=OXFORD), space_after=6)

    sub_head(doc, "Operations and Administration")
    body(doc, "Website development and hosting, marketing and promotional materials, "
              "society registration and insurance costs, and any regulatory or legal "
              "advisory fees.")

    sub_head(doc, "Setup/One-off Costs")
    body(doc, "We anticipate some costs that are not immediately predictable now - "
              "these include legal advice, registration fees, and insurance costs.")

    # -- 7 ------------------------------------------------------------------
    section_head(doc, 7, "Governance and Risk Management")
    body(doc, "OQTS is committed to operating with the highest standards of "
              "governance and transparency. All financial activities will be subject "
              "to robust oversight.")

    sub_head(doc, "Committee Structure")
    body(doc, "The society will be governed by a management team comprising a "
              "President, Vice-President, Treasurer, Head of Strategy, Head of "
              "Research, Head of Sponsorship, and Events and Communications Officer. "
              "The Treasurer will be responsible for all financial reporting. There "
              "will be five management team members, with both the President and "
              "Vice-President taking another role.")
    body(doc, "We are also considering the possibility of an external advisory board "
              "consisting of Gold/Founder tier sponsors and academic faculty. This "
              "would provide a level of rigorous oversight (for special cases such as "
              "a large fund drawdown) that students alone could not provide. See "
              "table below for rough numbers.")

    sub_head(doc, "Risk Framework")
    body(doc, "The Strategy Team will operate within a clearly defined risk "
              "framework, including position limits, maximum drawdown thresholds, and "
              "portfolio-level Value-at-Risk constraints. All strategies will undergo "
              "extensive backtesting and paper trading before any live capital "
              "deployment.")
    body(doc, "We will also institute a hard stop-loss on our live portfolio. Should "
              "certain drawdown levels be reached over a period of time (i.e. x% in "
              "24 hours, or y% over 30 days), then there will be a forced liquidation "
              "of all positions. Position size and correlation limits will also be "
              "imposed.")
    body(doc, "As in Committee Structure, we also hope to utilise an academic "
              "supervisory system for the fund.")

    para(doc, space_after=0, line=1).paragraph_format.space_after = Pt(6)
    build_headcount_table(doc)

    sub_head(doc, "About Us")
    build_person(
        doc, "Nikolai Dahl", "Founder, President, Chief Investment Officer",
        "First year MPhys, Physics, at The Queen’s College",
        ["Developed novel armoured droplet production method in school laboratory",
         "Further studied method directly with Nobel Laureate Professor Kostya Novoselov",
         "Currently developing a Python systemic regime filter using Random Matrix "
         "Theory on correlation matrices and applied density matrices"])
    build_person(
        doc, "Alec Mitchell-Thomson", "Founder, Vice-President, Head of Research and Technology",
        "2nd year, MEng, Engineering Science at New College",
        ["Summer Intern at Brevan Howard",
         "7th/200 in Preliminary Examinations",
         "Currently building OXDAQ, the society’s live exchange",
         "Developing a systematic commodities trading system applying advanced "
         "machine learning to ship positions, and a regime prediction library "
         "in Python using Hidden Markov Models"])

    # -- 8 ------------------------------------------------------------------
    section_head(doc, 8, "Contact and Next Steps")
    body(doc, "We welcome the opportunity to discuss how a partnership with OQTS can "
              "align with your firm’s recruitment strategy, brand objectives, and "
              "broader engagement with the academic community.")
    body(doc, "To arrange an introductory meeting or to request further information, "
              "please contact:")
    para(doc, space_after=0, line=1).paragraph_format.space_after = Pt(4)
    for c in load_contacts():
        build_contact_card(doc, c["name"], c["role"], c["email"], c["phone"])

    double_rule(doc, space_before=8, space_after=8)
    para(doc, "Oxford Quantitative Trading Society", align=WD_ALIGN_PARAGRAPH.CENTER,
         font=TEXT, size=S_BODY, color=SLATE, space_after=0, line=1.4)

    OUT.mkdir(exist_ok=True)
    path = OUT / "OQTS_Sponsorship_Prospectus_2026-27.docx"
    doc.save(path)
    print("wrote", path)
    return path


if __name__ == "__main__":
    build()
