"""OQTS seating plan: a seating spreadsheet -> easel posters + a catering copy.

    uv run --with openpyxl --with weasyprint python build.py SHEET.xlsx \
        --title "OQTS Launch Dinner" --line "Wednesday 28 October 2026, the Divinity School" \
        --out DIR

Writes to DIR:
  OQTS_Seating_Plan_Easel_A1.pdf    page 1 table plan, page 2 find-your-table index
  OQTS_Seating_Plan_Catering_A3.pdf plan with dietaries + dietary ledger

The spreadsheet is the source of record: make seat and table changes there,
then rebuild. Its format is in README.md. It holds personal data (names and
dietaries), so it and the PDFs never enter this public repository.

Brand tokens and faces come from this repo (brand.md v1.1); no colour is
defined here.
"""
import argparse
import re
from collections import Counter
from math import ceil, cos, radians, sin
from pathlib import Path

import openpyxl
from weasyprint import HTML

DESIGN = Path(__file__).resolve().parent.parent

# Brand tokens, read from the single source of truth.
CSS = (DESIGN / "assets/oqts.css").read_text()
T = dict(re.findall(r"--oqts-([a-z-]+):\s*(#[0-9A-Fa-f]{6})", CSS))


def load(path):
    """Rows as dicts keyed by header. A table called "Table N" is number N;
    any other name (a sponsor's table, say) takes the number in the Table
    column and is shown as a label on the table."""
    ws = openpyxl.load_workbook(path, read_only=True).active
    it = ws.iter_rows(values_only=True)
    hdr = next(it)
    rows = []
    for v in it:
        r = {h: c for h, c in zip(hdr, v) if h}
        if r.get("Table") is None:
            continue
        name = str(r["Table name"] or "")
        m = re.fullmatch(r"Table\s+(\d+)", name.strip())
        r["n"] = int(m.group(1)) if m else int(r["Table"])
        r["label"] = None if m else name
        rows.append(r)
    return rows


def person(r):
    name = r["Name"]
    if not name:
        return None
    name = re.sub(r"\s*\(.*?\)\s*$", "", name)  # e.g. "(shellfish)": that lives in Dietary
    role = r["Role"]
    if role == "sponsor":
        tag = r["Firm or college"]
    elif role == "committee":
        tag = "OQTS committee"
    else:
        tag = r["Firm or college"] or ""
    diet = " · ".join(
        s.strip().capitalize() for v in (r["Dietary"], r["Meal"]) if v for s in [v]
    )
    return {"name": name, "role": role, "tag": tag, "diet": diet,
            "dietary": r["Dietary"], "meal": r["Meal"]}


MONO, SERIF = "Latin Modern Mono", "STIX Two Text"
TEXT = {  # class -> (family, size, tracking), in mm user units
    "eb": (MONO, 4.2, 0.6), "eb sm": (MONO, 3.2, 0.4), "num": (MONO, 22, 0),
    "seat": (MONO, 3.4, 0), "nm": (SERIF, 6.4, 0), "nm empty": (SERIF, 6.4, 0),
    "tag": (MONO, 3.5, 0.45), "diet": (MONO, 3.5, 0.45),
}


def text(x, y, cls, fill, body, anchor="middle"):
    fam, size, track = TEXT[cls]
    return (f'<text x="{x:.2f}" y="{y:.2f}" text-anchor="{anchor}" font-family="{fam}" '
            f'font-size="{size}" letter-spacing="{track}" fill="{fill}">{body}</text>')


def esc(s):
    return (s or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ── One round table as SVG, in millimetres ──
R_DISC, R_CHAIR, R_DOT = 25, 31.5, 3.6
SLOT = 17  # vertical spacing of name labels, for up to 5 a side


def table_svg(n, label, seats, catering):
    w, h = 240, 92  # drawn at 290 x 111mm: about 1.2x the user units
    cx, cy = w / 2, h / 2
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
         f'width="290mm" height="111mm">']
    o.append(f'<circle cx="{cx}" cy="{cy}" r="{R_DISC}" fill="{T["paper"]}" '
             f'stroke="{T["camel"]}" stroke-width="0.5"/>')
    o.append(text(cx, cy - 9, "eb", T["bronze"], "TABLE"))
    o.append(text(cx, cy + 9, "num", T["oxford"], n))
    if label:
        o.append(text(cx, cy + 17, "eb sm", T["bronze"], esc(label.upper())))
    n_seats = len(seats)
    n_right = ceil(n_seats / 2)
    step = 360 / n_seats
    for i, p in enumerate(seats):  # seat i+1, clockwise from top right
        ang = radians(step / 2 + step * i)
        dx, dy = R_CHAIR * sin(ang), -R_CHAIR * cos(ang)
        right = i < n_right
        k, m = (i, n_right) if right else (n_seats - 1 - i, n_seats - n_right)
        ly = (k - (m - 1) / 2) * SLOT * 5 / max(m, 5)
        x0 = cx + dx + (7 if right else -7)
        anchor = "start" if right else "end"
        # chair
        if p is None:
            fill, stroke, ink = T["ivory"], T["chalk"], T["slate"]
        elif p["role"] == "sponsor":
            fill, stroke, ink = T["oxford"], T["oxford"], T["ivory"]
        elif p["role"] == "committee":
            fill, stroke, ink = T["camel"], T["camel"], T["oxford"]
        else:
            fill, stroke, ink = T["ivory"], T["oxford"], T["oxford"]
        dash = ' stroke-dasharray="1.2 1"' if p is None else ""
        o.append(f'<circle cx="{cx + dx:.2f}" cy="{cy + dy:.2f}" r="{R_DOT}" '
                 f'fill="{fill}" stroke="{stroke}" stroke-width="0.45"{dash}/>')
        o.append(text(cx + dx, cy + dy + 1.15, "seat", ink, i + 1))
        # label: name, then tag (and dietary on the catering copy)
        lines = []
        if p is None:
            lines.append(("nm empty", T["slate"], "Open seat"))
        else:
            lines.append(("nm", T["oxford"], p["name"]))
            if p["tag"]:
                lines.append(("tag", T["bronze"] if p["role"] == "sponsor" else T["slate"],
                              p["tag"].upper()))
            if catering and p["diet"]:
                lines.append(("diet", T["bronze"], p["diet"].upper()))
        top = cy + ly - (len(lines) - 1) * 2.6
        y = top + 2.2
        for j, (cls, col, txt) in enumerate(lines):
            if cls == "diet":  # a bronze diamond marks a dietary line
                d = x0 + 1.6 if right else x0 - 1.6
                o.append(f'<path d="M{d:.2f} {y - 2.9:.2f}l1.4 1.4l-1.4 1.4l-1.4 -1.4z" '
                         f'fill="{T["bronze"]}"/>')
                o.append(text(x0 + (4 if right else -4), y, cls, col, esc(txt), anchor))
            else:
                o.append(text(x0, y, cls, col, esc(txt), anchor))
            y += 5.6 if j == 0 else 4.4
    o.append("</svg>")
    return "".join(o)


def head(eyebrow, ev):
    lockup = (DESIGN / "assets/logo/oqts-lockup-reverse.svg").as_uri()
    return f"""
<header class="bar">
  <img class="lockup" src="{lockup}">
  <div class="title">
    <div class="eyebrow-rev">{esc(eyebrow)}</div>
    <h1>{esc(ev[0])}</h1>
    <div class="line">{esc(ev[1])}</div>
  </div>
</header>"""


FOOT = """<footer class="bar foot"><span>Oxford Quantitative Trading Society</span>
<span>oqts.org</span></footer>"""


def legend(catering):
    def dot(fill, stroke):
        return (f'<svg viewBox="0 0 10 10" width="7mm" height="7mm"><circle cx="5" cy="5" '
                f'r="4.2" fill="{fill}" stroke="{stroke}" stroke-width="0.6"/></svg>')
    items = [(dot(T["oxford"], T["oxford"]), "Sponsor"),
             (dot(T["camel"], T["camel"]), "OQTS committee"),
             (dot(T["ivory"], T["oxford"]), "Guest")]
    diamond = (f'<svg viewBox="0 0 10 10" width="5mm" height="5mm"><path d="M5 1l4 4l-4 4l-4 -4z" '
               f'fill="{T["bronze"]}"/></svg>')
    extra = (f'<span class="li">{diamond}<span>Dietary requirement</span></span>'
             if catering else "")
    return ('<div class="legend">' + "".join(
        f'<span class="li">{d}<span>{t}</span></span>' for d, t in items) + extra +
        '<span class="li note">Seats numbered clockwise from the top</span></div>')


def plan_page(tables, catering, ev):
    cells = "".join(
        f'<div class="cell">{table_svg(n, lab, seats, catering)}</div>'
        for n, lab, seats in tables)
    eb = "Seating plan · catering copy" if catering else "Seating plan"
    return (f'<section class="page">{head(eb, ev)}{legend(catering)}'
            f'<div class="grid">{cells}</div><div class="close"></div>{FOOT}</section>')


def index_page(tables, ev):
    people = sorted(
        ((p["name"], n) for n, _, seats in tables for p in seats if p),
        key=lambda t: t[0].casefold())
    per = -(-len(people) // 3)
    cols = [people[i:i + per] for i in range(0, len(people), per)]
    html = "".join(
        '<ol class="col">' + "".join(
            f'<li><span class="who">{esc(nm)}</span><span class="lead"></span>'
            f'<span class="tn">{n}</span></li>' for nm, n in c) + "</ol>"
        for c in cols)
    return (f'<section class="page">{head("Find your table", ev)}'
            f'<div class="ixhead"><span>Name, A to Z by first name</span><span>Table</span></div>'
            f'<div class="index">{html}</div><div class="close"></div>{FOOT}</section>')


def ledger_page(tables, ev):
    rows, totals = [], Counter()
    for n, _, seats in tables:
        for i, p in enumerate(seats):
            if p and p["diet"]:
                rows.append((n, i + 1, p))
                for v in (p["dietary"], p["meal"]):
                    if v:
                        totals[v.strip().capitalize()] += 1
    body = "".join(
        f'<tr><td class="c">{n}</td><td class="c">{s}</td><td>{esc(p["name"])}</td>'
        f'<td>{esc(p["tag"])}</td><td>{esc((p["dietary"] or "").capitalize())}</td>'
        f'<td>{esc((p["meal"] or "").capitalize())}</td></tr>' for n, s, p in rows)
    tot = ", ".join(f"{k} {v}" for k, v in sorted(totals.items(), key=lambda kv: -kv[1]))
    return (f'<section class="page">{head("Dietary requirements · catering copy", ev)}'
            f'<table class="ledger"><thead><tr><th>Table</th><th>Seat</th><th>Name</th>'
            f'<th>Affiliation</th><th>Dietary note</th><th>Meal</th></tr></thead>'
            f'<tbody>{body}</tbody><tfoot><tr><td colspan="6">{len(rows)} guests with a '
            f'requirement. By note: {esc(tot)}</td></tr></tfoot></table>'
            f'<div class="close"></div>{FOOT}</section>')


STYLE = f"""
@page {{ size: A1 portrait; margin: 0; }}
html, body {{ margin: 0; }}
body {{ background: {T['ivory']}; color: {T['oxford']}; font-family: var(--oqts-text); }}
.page {{ width: 594mm; height: 841mm; position: relative; page-break-after: always;
  background: {T['ivory']} url('{(DESIGN / 'assets/patterns/oqts-dots-ground-1.svg').as_uri()}');
  overflow: hidden; }}
.page:last-child {{ page-break-after: auto; }}
.bar {{ background: {T['oxford']}; color: {T['paper']}; }}
header.bar {{ height: 118mm; display: flex; align-items: center; padding: 0 30mm;
  box-sizing: border-box; gap: 24mm; }}
.lockup {{ height: 52mm; }}
.title {{ margin-left: auto; text-align: right; }}
.eyebrow-rev {{ font-family: var(--oqts-display); color: {T['camel-rev']};
  font-size: 9mm; letter-spacing: .14em; text-transform: uppercase; }}
h1 {{ font-family: var(--oqts-display); font-weight: 400; font-size: 19mm;
  letter-spacing: .01em; margin: 3mm 0 3mm; line-height: 1.1; }}
.line {{ font-size: 8mm; color: {T['slate-rev']}; }}
.legend {{ display: flex; gap: 12mm; align-items: center; padding: 9mm 30mm 0;
  font-size: 8mm; color: {T['slate']}; }}
.li {{ display: flex; align-items: center; gap: 3mm; white-space: nowrap; }}
.li.note {{ margin-left: auto; }}
.grid {{ display: flex; flex-wrap: wrap; padding: 10mm 7mm 0; }}
.cell {{ width: 290mm; height: 118mm; display: flex; justify-content: center; }}
.close {{ position: absolute; left: 30mm; right: 30mm; bottom: 46mm; height: 2.4mm;
  border-top: .5mm solid {T['camel']}; border-bottom: .5mm solid {T['camel']}; }}
footer.foot {{ position: absolute; bottom: 0; left: 0; right: 0; height: 32mm;
  display: flex; justify-content: space-between; align-items: center; padding: 0 30mm;
  font-family: var(--oqts-display); font-size: 7mm; letter-spacing: .09em;
  text-transform: uppercase; color: {T['slate-rev']}; }}
.ixhead {{ display: flex; justify-content: space-between; margin: 16mm 30mm 4mm;
  font-family: var(--oqts-display); font-size: 7mm; letter-spacing: .14em;
  text-transform: uppercase; color: {T['bronze']}; padding-bottom: 3mm;
  border-bottom: .4mm solid {T['chalk']}; }}
.index {{ display: flex; gap: 14mm; margin: 0 30mm; }}
.col {{ list-style: none; margin: 0; padding: 0; flex: 1; }}
.col li {{ display: flex; align-items: baseline; height: 18.4mm;
  border-bottom: .3mm solid {T['chalk']}; font-size: 8.4mm; }}
.who {{ white-space: nowrap; }}
.lead {{ flex: 1; }}
.tn {{ font-family: var(--oqts-display); font-size: 10mm; min-width: 12mm; text-align: right; }}
.ledger {{ margin: 18mm 30mm 0; width: calc(100% - 60mm); border-collapse: collapse;
  font-size: 7.6mm; }}
.ledger th {{ font-family: var(--oqts-display); font-weight: 400; text-align: left;
  font-size: 6mm; letter-spacing: .14em; text-transform: uppercase; color: {T['bronze']};
  padding: 0 3mm 4mm; border-bottom: .4mm solid {T['chalk']}; }}
.ledger td {{ padding: 3.4mm 3mm; border-bottom: .3mm solid {T['chalk']}; }}
.ledger td.c {{ font-family: var(--oqts-display); text-align: center; }}
.ledger tfoot td {{ border-bottom: 0; color: {T['slate']};
  padding-top: 6mm; }}
"""


def render(pages, path, zoom=1.0):
    doc = f"<!doctype html><html><head><meta charset='utf-8'><style>{STYLE}</style></head>" \
          f"<body>{''.join(pages)}</body></html>"
    HTML(string=doc, base_url=str(DESIGN / "assets") + "/").write_pdf(
        path, zoom=zoom, stylesheets=[str(DESIGN / "assets/oqts.css")])


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("sheet", type=Path)
    ap.add_argument("--title", required=True, help="event name, e.g. 'OQTS Launch Dinner'")
    ap.add_argument("--line", required=True, help="date and venue line under the title")
    ap.add_argument("--out", type=Path, required=True,
                    help="output folder; keep it outside this repository")
    a = ap.parse_args()
    if a.out.resolve().is_relative_to(DESIGN) or a.sheet.resolve().is_relative_to(DESIGN):
        ap.error("the sheet and the PDFs hold personal data: keep them outside oqts-design")
    a.out.mkdir(parents=True, exist_ok=True)
    ev = (a.title, a.line)

    rows = load(a.sheet)
    tables = []
    for n in sorted({r["n"] for r in rows}):
        rs = sorted((r for r in rows if r["n"] == n), key=lambda r: r["Seat"])
        tables.append((n, rs[0]["label"], [person(r) for r in rs]))

    render([plan_page(tables, False, ev), index_page(tables, ev)],
           a.out / "OQTS_Seating_Plan_Easel_A1.pdf")
    render([plan_page(tables, True, ev), ledger_page(tables, ev)],
           a.out / "OQTS_Seating_Plan_Catering_A3.pdf", zoom=0.5)
    for n, lab, seats in tables:
        print(n, lab or "", "|", "; ".join(p["name"] if p else "-" for p in seats))


if __name__ == "__main__":
    main()
