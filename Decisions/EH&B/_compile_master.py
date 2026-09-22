"""Compile every EH&B .xlsx into MASTER.xlsx. Does not modify sources."""
from __future__ import annotations

from copy import copy
from datetime import date
from pathlib import Path
from zipfile import ZipFile

from openpyxl import Workbook, load_workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

FOLDER = Path(r"c:\Users\Owner\Desktop\MAN6930 Case\Decisions\EH&B")
DEST = FOLDER / "MASTER.xlsx"
TODAY = date.today().isoformat()

# Source order matches the brief. Prefixes keep names unique and <= 31 chars.
SOURCES = [
    {
        "file": "Small Large Employment Shares.xlsx",
        "prefix": "Emp",
        "rename": {
            "Notes": "Emp-Notes",
            "United States": "Emp-US",
            "States": "Emp-States",
            "Metros Exhibit High Low": "Emp-MetrosHiLo",
            "Metros Full (387)": "Emp-MetrosFull",
            "MSA Full File": "Emp-MSAFull",
            "Cutoff Sensitivity": "Emp-CutoffSens",
        },
    },
    {
        "file": "Work from Home Rates.xlsx",
        "prefix": "WFH",
        "rename": {
            "Notes": "WFH-Notes",
            "United States": "WFH-US",
            "States": "WFH-States",
            "Seniority proxies": "WFH-Seniority",
            "Firm size": "WFH-FirmSize",
        },
    },
    {
        "file": "Brokerage Metrics.xlsx",
        "prefix": "Brok",
        "rename": {
            "Notes": "Brok-Notes",
            "Core metrics": "Brok-Core",
            "Later demoted": "Brok-Later",
            "Already in hand": "Brok-InHand",
        },
    },
    {
        "file": "Brokerage Metrics Breakdown.xlsx",
        "prefix": "BrkDn",
        "rename": {
            "Notes": "BrkDn-Notes",
            "Scorecard": "BrkDn-Score",
            "M1": "BrkDn-M1",
            "M2": "BrkDn-M2",
            "M5": "BrkDn-M5",
            "M9": "BrkDn-M9",
            "M13": "BrkDn-M13",
            "Analogues": "BrkDn-Analogues",
        },
    },
    {
        "file": "Comcast vs Charter.xlsx",
        "prefix": "CvC",
        "rename": {
            "Notes": "CvC-Notes",
            "State leads": "CvC-Leads",
            "Charter lead states": "CvC-Charter",
            "Comcast lead states": "CvC-Comcast",
            "Neither": "CvC-Neither",
        },
    },
    {
        "file": "State Region Density Maps.xlsx",
        "prefix": "Dens",
        "rename": {
            "Notes": "Dens-Notes",
            "State combined": "Dens-State",
            "Division rollup": "Dens-Division",
            "A Charter vs Comcast": "Dens-A-CvC",
            "B WFH ACS": "Dens-B-WFH",
            "C Large-firm 500+": "Dens-C-Large",
        },
    },
]


def cell_value(cell):
    """Copy stored values only — never formulas — so MASTER cannot #REF!."""
    v = cell.value
    if isinstance(v, str) and v.startswith("="):
        return None
    return v


def copy_sheet(src, dest):
    dest.sheet_properties.tabColor = copy(src.sheet_properties.tabColor)
    dest.freeze_panes = src.freeze_panes
    dest.sheet_view.showGridLines = src.sheet_view.showGridLines
    if src.auto_filter and src.auto_filter.ref:
        dest.auto_filter.ref = src.auto_filter.ref
    dest.sheet_view.zoomScale = src.sheet_view.zoomScale
    dest.page_setup.orientation = src.page_setup.orientation
    dest.page_setup.fitToPage = src.page_setup.fitToPage
    dest.page_setup.fitToWidth = src.page_setup.fitToWidth
    dest.page_setup.fitToHeight = src.page_setup.fitToHeight
    dest.page_setup.paperSize = src.page_setup.paperSize
    dest.print_title_rows = src.print_title_rows
    dest.print_title_cols = src.print_title_cols
    dest.page_margins = copy(src.page_margins)

    for row in src.iter_rows():
        for cell in row:
            new = dest.cell(row=cell.row, column=cell.column, value=cell_value(cell))
            if cell.has_style:
                new.font = copy(cell.font)
                new.border = copy(cell.border)
                new.fill = copy(cell.fill)
                new.number_format = cell.number_format
                new.protection = copy(cell.protection)
                new.alignment = copy(cell.alignment)
            if cell.hyperlink:
                new.hyperlink = copy(cell.hyperlink)
            if cell.comment:
                new.comment = copy(cell.comment)

    for letter, dim in src.column_dimensions.items():
        d = dest.column_dimensions[letter]
        d.width = dim.width
        d.hidden = dim.hidden
        d.bestFit = dim.bestFit

    for idx, dim in src.row_dimensions.items():
        d = dest.row_dimensions[idx]
        d.height = dim.height
        d.hidden = dim.hidden

    for merged in src.merged_cells.ranges:
        dest.merge_cells(str(merged))

    for cf in src.conditional_formatting._cf_rules.values():
        for rule in cf:
            dest.conditional_formatting.add(rule.sqref if hasattr(rule, "sqref") else None, rule)


def style_toc(ws):
    thin = Border(
        left=Side(style="thin", color="D0D0D0"),
        right=Side(style="thin", color="D0D0D0"),
        top=Side(style="thin", color="D0D0D0"),
        bottom=Side(style="thin", color="D0D0D0"),
    )
    header_fill = PatternFill("solid", fgColor="4A4A4A")
    header_font = Font(name="Calibri", bold=True, color="FFFFFF", size=11)
    title_font = Font(name="Calibri", bold=True, size=16, color="1A1A1A")
    note_font = Font(name="Calibri", italic=True, size=10, color="555555")
    body = Font(name="Calibri", size=11)
    wrap = Alignment(wrap_text=True, vertical="center")

    ws["A1"] = "EH&B MASTER — compiled copy of every workbook in this folder"
    ws["A1"].font = title_font
    ws.merge_cells("A1:D1")
    ws.row_dimensions[1].height = 22

    ws["A2"] = (
        f"Compiled {TODAY}. Every number is a copy. Source workbooks remain the originals "
        "and are unchanged. Do not treat MASTER as the system of record."
    )
    ws["A2"].font = note_font
    ws["A2"].alignment = wrap
    ws.merge_cells("A2:D2")
    ws.row_dimensions[2].height = 32

    headers = ["Source file", "Date compiled", "MASTER tabs from this file", "Source sheets (original names)"]
    for col, h in enumerate(headers, 1):
        cell = ws.cell(3, col, h)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(wrap_text=True, vertical="center")
        cell.border = thin
    ws.row_dimensions[3].height = 20
    ws.freeze_panes = "A4"
    return thin, body, wrap


def write_toc(ws, rows):
    thin, body, wrap = style_toc(ws)
    for i, row in enumerate(rows, 4):
        for col, val in enumerate(row, 1):
            cell = ws.cell(i, col, val)
            cell.font = body
            cell.alignment = wrap
            cell.border = thin
        ws.row_dimensions[i].height = 36
    ws.column_dimensions["A"].width = 42
    ws.column_dimensions["B"].width = 16
    ws.column_dimensions["C"].width = 62
    ws.column_dimensions["D"].width = 62


def unique_name(used: set[str], proposed: str) -> str:
    name = proposed[:31]
    if name not in used:
        used.add(name)
        return name
    n = 2
    while True:
        suffix = f"-{n}"
        candidate = (proposed[: 31 - len(suffix)] + suffix)
        if candidate not in used:
            used.add(candidate)
            return candidate
        n += 1


def main():
    found_xlsx = sorted(
        p.name
        for p in FOLDER.glob("*.xlsx")
        if not p.name.startswith("~$") and p.name.upper() != "MASTER.XLSX"
    )
    planned = [s["file"] for s in SOURCES]
    unexpected = [n for n in found_xlsx if n not in planned]
    missing = [n for n in planned if n not in found_xlsx]

    out = Workbook()
    toc = out.active
    toc.title = "TOC"

    toc_rows = []
    used_names = {"TOC"}
    copied = []

    for spec in SOURCES:
        path = FOLDER / spec["file"]
        if not path.exists():
            toc_rows.append(
                (spec["file"], TODAY, "(file not found — no tabs copied)", "")
            )
            continue
        src = load_workbook(path, data_only=False)
        dest_tabs = []
        src_names = []
        rename = spec["rename"]
        for src_name in src.sheetnames:
            src_names.append(src_name)
            proposed = rename.get(src_name, f"{spec['prefix']}-{src_name}")
            dest_name = unique_name(used_names, proposed)
            dest = out.create_sheet(dest_name)
            copy_sheet(src[src_name], dest)
            dest_tabs.append(dest_name)
            copied.append((spec["file"], src_name, dest_name))
        src.close()
        toc_rows.append(
            (
                spec["file"],
                TODAY,
                ", ".join(dest_tabs),
                ", ".join(src_names),
            )
        )

    if unexpected:
        toc_rows.append(
            (
                "; ".join(unexpected),
                TODAY,
                "(present but not in planned list — not copied)",
                "",
            )
        )

    write_toc(toc, toc_rows)
    out.save(DEST)
    out.close()

    # Verify PK zip + sheet inventory
    with ZipFile(DEST) as zf:
        names = zf.namelist()
        if "xl/workbook.xml" not in names:
            raise SystemExit("MASTER is not a valid xlsx (missing xl/workbook.xml)")
        pk_ok = True

    wb = load_workbook(DEST, data_only=False)
    print("DEST", DEST)
    print("exists", DEST.exists(), "size", DEST.stat().st_size)
    print("pk_ok", pk_ok)
    print("sheet_count", len(wb.sheetnames))
    print("sheets", wb.sheetnames)
    print("missing", missing)
    print("unexpected", unexpected)
    print("copied_pairs", len(copied))
    toc_ws = wb["TOC"]
    ref_hits = []
    for row in toc_ws.iter_rows():
        for cell in row:
            if isinstance(cell.value, str) and "#REF!" in cell.value:
                ref_hits.append(cell.coordinate)
            if isinstance(cell.value, str) and cell.value.startswith("="):
                ref_hits.append((cell.coordinate, cell.value))
    print("toc_ref_or_formula", ref_hits)
    for spec in SOURCES:
        path = FOLDER / spec["file"]
        if not path.exists():
            print("MISSING_FILE", spec["file"])
            continue
        src = load_workbook(path, data_only=False)
        for src_name in src.sheetnames:
            dest_name = spec["rename"].get(src_name, f"{spec['prefix']}-{src_name}")
            dest_name = dest_name[:31]
            ok = dest_name in wb.sheetnames
            print(f"  map {spec['file']} :: {src_name} -> {dest_name} present={ok}")
        src.close()
    wb.close()


if __name__ == "__main__":
    main()
