# -*- coding: utf-8 -*-
"""Export Charter vs Comcast state-lead table to EH&B Excel. Read-only on CSVs."""
import csv
import json
from pathlib import Path

from openpyxl import Workbook, load_workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

ROOT = Path(r"c:\Users\Owner\Desktop\MAN6930 Case")
OUT = ROOT / "Analysis" / "cable-share-small-firm" / "out"
DEST_DIR = ROOT / "Decisions" / "EH&B"
DEST = DEST_DIR / "Comcast vs Charter.xlsx"

DEST_DIR.mkdir(parents=True, exist_ok=True)

with open(OUT / "summary.json", encoding="utf-8") as f:
    summary = json.load(f)

SOURCE_URL = "https://broadbandmap.fcc.gov/data-download"


def load_csv(path):
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def as_int(x):
    if x is None or x == "":
        return None
    return int(float(x))


def as_pct_1dp(x):
    """CSV stores res_st_pct as a 0–1 share. Exhibit is percentage points, 1 decimal."""
    if x is None or x == "":
        return None
    return round(float(x) * 100, 1)


def as_float(x):
    if x is None or x == "":
        return None
    return float(x)


def display_leader(raw):
    if raw == "neither present":
        return "Neither"
    return raw


header_font = Font(bold=True)
header_fill = PatternFill("solid", fgColor="F2F2F2")
wrap = Alignment(wrap_text=True, vertical="top")
pct_1dp = "0.0"
int_fmt = "#,##0"


def style_header(ws, ncols):
    for col in range(1, ncols + 1):
        cell = ws.cell(1, col)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(wrap_text=True, vertical="center")
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = ws.dimensions


def set_widths(ws, widths):
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w


rows = load_csv(OUT / "chtr_vs_cmcsa_state_leads.csv")
# CSV is already sorted by Charter-minus-Comcast margin (Charter leads at top).
assert len(rows) == 51

n_ch = sum(1 for r in rows if r["leader"] == "Charter")
n_cm = sum(1 for r in rows if r["leader"] == "Comcast")
n_neither = sum(1 for r in rows if r["leader"] == "neither present")
n_tie = sum(1 for r in rows if r["leader"] == "tie")
n_ch_present = sum(1 for r in rows if r["charter_present"] == "True")
n_cm_present = sum(1 for r in rows if r["comcast_present"] == "True")

assert n_ch == 19
assert n_cm == 27
assert n_neither == 5
assert n_tie == 0
assert n_ch_present == 42
assert n_cm_present == 41

STATE_HEADERS = [
    "State",
    "Abbr",
    "FIPS",
    "Charter estimated units",
    "Charter share of fabric (%)",
    "Comcast estimated units",
    "Comcast share of fabric (%)",
    "Margin (Charter − Comcast units)",
    "Leader",
    "State residential fabric units",
    "Charter present",
    "Comcast present",
    "Source URL",
]


def append_state_row(ws, r):
    ws.append(
        [
            r["state"],
            r["abbr"],
            r["state_fips"],
            as_int(r["charter_est_units"]),
            as_pct_1dp(r["charter_res_st_pct"]),
            as_int(r["comcast_est_units"]),
            as_pct_1dp(r["comcast_res_st_pct"]),
            as_int(r["margin_units_charter_minus_comcast"]),
            display_leader(r["leader"]),
            as_int(r["total_residential_units"]),
            "Yes" if r["charter_present"] == "True" else "No",
            "Yes" if r["comcast_present"] == "True" else "No",
            SOURCE_URL,
        ]
    )
    row = ws.max_row
    for col in (4, 6, 8, 10):
        if ws.cell(row, col).value is not None:
            ws.cell(row, col).number_format = int_fmt
    for col in (5, 7):
        if ws.cell(row, col).value is not None:
            ws.cell(row, col).number_format = pct_1dp


def write_state_sheet(wb, title, subset):
    ws = wb.create_sheet(title)
    ws.append(STATE_HEADERS)
    for r in subset:
        append_state_row(ws, r)
    style_header(ws, len(STATE_HEADERS))
    set_widths(ws, [22, 8, 8, 22, 24, 22, 24, 30, 12, 26, 14, 16, 48])
    return ws


wb = Workbook()

# ----- 1. Notes -----
ws = wb.active
ws.title = "Notes"
notes = [
    ("Title", "Charter vs Comcast by state — who reports more residential locations served"),
    (
        "Canvas",
        "chtr-vs-cmcsa-state-lead.canvas.tsx (read-only source; do not treat as subscriber share)",
    ),
    (
        "Metric definition",
        "FCC BDC residential location availability: share of residential units at "
        "Broadband Serviceable Locations where the holding company reports residential "
        "fixed broadband (res_st_pct). Estimated units = res_st_pct × state residential "
        "fabric units. THIS IS AVAILABILITY / LOCATIONS SERVED. It is NOT subscriber "
        "share, NOT Form 477 subscriptions, and NOT a 10-K state mix.",
    ),
    ("Vintage", "As of 31 December 2025 (D25)"),
    ("File revision", "15 Sep 2026"),
    ("Agency", "Federal Communications Commission"),
    ("Program", "Broadband Data Collection / National Broadband Map"),
    ("Source URL", SOURCE_URL),
    ("Provider-list file", "bdc_us_provider_list_D25_15sep2026.csv"),
    (
        "Provider-by-geography file",
        "bdc_us_provider_summary_by_geography_D25_15sep2026.csv "
        "(res_st_pct, geography_type = State, data_type = Fixed Broadband)",
    ),
    (
        "Fabric-units file",
        "bdc_us_fixed_broadband_summary_by_geography_D25_15sep2026.csv "
        "(total_units, State / Total / Any Technology / residential)",
    ),
    (
        "National provider file",
        "bdc_us_fixed_broadband_provider_summary_D25_15sep2026.csv",
    ),
    (
        "Charter identity",
        "Charter Communications (Spectrum) · FRN 0025646373 · provider ID 130235",
    ),
    (
        "Comcast identity",
        "Comcast Corporation (Xfinity) · FRN 0003768165 · provider ID 130317",
    ),
    (
        "Affiliates",
        "Affiliates not rolled in. Sonic Spectrum and Red Spectrum are unrelated.",
    ),
    ("States Charter leads", 19),
    ("States Comcast leads", 27),
    ("Neither present", 5),
    ("Ties", 0),
    (
        "Neither states",
        "Alaska, Iowa, North Dakota, Oklahoma, South Dakota",
    ),
    (
        "Charter footprint on this vintage",
        "42 states + DC with a positive residential res_st_pct (missing row or 0.0000 = absent)",
    ),
    (
        "Comcast footprint on this vintage",
        "41 states + DC with a positive residential res_st_pct (missing row or 0.0000 = absent)",
    ),
    (
        "Leader rule",
        "Beating = strictly larger res_st_pct. Missing provider row or 0.0000 treated as absent.",
    ),
    (
        "Top Charter unit leads",
        "NY +5.54M, OH +4.41M, NC +4.36M, TX +3.76M, WI +2.31M "
        "(estimated residential units; Charter minus Comcast)",
    ),
    (
        "Top Comcast unit leads",
        "PA −4.36M, IL −4.27M, MD −2.46M, MA −2.45M, WA −2.35M "
        "(estimated residential units; Charter minus Comcast)",
    ),
    (
        "What this is not",
        "Not subscriber share. Company 10-Ks do not publish state subscriber counts; "
        "national mix is not allocated to states. A location the provider can serve is not a customer.",
    ),
    (
        "Sheet guide",
        "State leads = all 51 (50 states + DC), sorted by Charter-minus-Comcast unit margin "
        "(Charter leads at top). Charter lead states = the 19. Comcast lead states = the 27. "
        "Neither = AK, IA, ND, OK, SD.",
    ),
    (
        "Source CSVs / script",
        "Analysis/cable-share-small-firm/out/chtr_vs_cmcsa_state_leads.csv · "
        "Script: Analysis/cable-share-small-firm/build_state_leads.py (read-only)",
    ),
]
ws.append(["Field", "Content"])
for field, content in notes:
    ws.append([field, content])
style_header(ws, 2)
ws.column_dimensions["A"].width = 34
ws.column_dimensions["B"].width = 110
for row in ws.iter_rows(min_row=2, max_row=ws.max_row, min_col=2, max_col=2):
    for cell in row:
        cell.alignment = wrap
for r in range(2, ws.max_row + 1):
    ws.row_dimensions[r].height = 48 if r in (4, 11, 12, 26, 27) else 20

# ----- 2–5. State tables -----
write_state_sheet(wb, "State leads", rows)
write_state_sheet(wb, "Charter lead states", [r for r in rows if r["leader"] == "Charter"])
write_state_sheet(wb, "Comcast lead states", [r for r in rows if r["leader"] == "Comcast"])
write_state_sheet(wb, "Neither", [r for r in rows if r["leader"] == "neither present"])

wb.save(DEST)
print("Saved:", DEST)
print("Sheets:", wb.sheetnames)

# ----- Verification -----
checks = []
ny = next(r for r in rows if r["abbr"] == "NY")
oh = next(r for r in rows if r["abbr"] == "OH")
nc = next(r for r in rows if r["abbr"] == "NC")
tx = next(r for r in rows if r["abbr"] == "TX")
wi = next(r for r in rows if r["abbr"] == "WI")
pa = next(r for r in rows if r["abbr"] == "PA")
il = next(r for r in rows if r["abbr"] == "IL")
md = next(r for r in rows if r["abbr"] == "MD")
ma = next(r for r in rows if r["abbr"] == "MA")
wa = next(r for r in rows if r["abbr"] == "WA")

checks.append(("count 51", len(rows), 51))
checks.append(("n Charter", n_ch, 19))
checks.append(("n Comcast", n_cm, 27))
checks.append(("n neither", n_neither, 5))
checks.append(("n tie", n_tie, 0))
checks.append(("Charter footprint", n_ch_present, 42))
checks.append(("Comcast footprint", n_cm_present, 41))
checks.append(("NY units", as_int(ny["charter_est_units"]), 5580990))
checks.append(("NY margin", as_int(ny["margin_units_charter_minus_comcast"]), 5536505))
checks.append(("NY pct", as_pct_1dp(ny["charter_res_st_pct"]), 60.2))
checks.append(("OH margin M", round(as_int(oh["margin_units_charter_minus_comcast"]) / 1e6, 2), 4.41))
checks.append(("NC margin M", round(as_int(nc["margin_units_charter_minus_comcast"]) / 1e6, 2), 4.36))
checks.append(("TX margin M", round(as_int(tx["margin_units_charter_minus_comcast"]) / 1e6, 2), 3.76))
checks.append(("WI margin M", round(as_int(wi["margin_units_charter_minus_comcast"]) / 1e6, 2), 2.31))
checks.append(("PA margin M", round(as_int(pa["margin_units_charter_minus_comcast"]) / 1e6, 2), -4.36))
checks.append(("IL margin M", round(as_int(il["margin_units_charter_minus_comcast"]) / 1e6, 2), -4.27))
checks.append(("MD margin M", round(as_int(md["margin_units_charter_minus_comcast"]) / 1e6, 2), -2.46))
checks.append(("MA margin M", round(as_int(ma["margin_units_charter_minus_comcast"]) / 1e6, 2), -2.45))
checks.append(("WA margin M", round(as_int(wa["margin_units_charter_minus_comcast"]) / 1e6, 2), -2.35))
checks.append(("summary n_ch", summary["n_charter_leads"], 19))
checks.append(("summary n_cm", summary["n_comcast_leads"], 27))
checks.append(("summary n_neither", summary["n_neither"], 5))

with open(DEST, "rb") as f:
    magic = f.read(2)
checks.append(("PK zip header", magic, b"PK"))

wb2 = load_workbook(DEST, data_only=True)
notes_ws = wb2["Notes"]
# Field/Content: States Charter leads is row with that field
notes_map = {row[0]: row[1] for row in notes_ws.iter_rows(min_row=2, values_only=True) if row[0]}
checks.append(("xlsx Notes Charter leads", notes_map.get("States Charter leads"), 19))
checks.append(("xlsx Notes Comcast leads", notes_map.get("States Comcast leads"), 27))
checks.append(("xlsx Notes Neither", notes_map.get("Neither present"), 5))
checks.append(("xlsx Notes Ties", notes_map.get("Ties"), 0))
checks.append(("xlsx Notes URL", notes_map.get("Source URL"), SOURCE_URL))

sl = wb2["State leads"]
checks.append(("xlsx NY A2", sl["A2"].value, "New York"))
checks.append(("xlsx NY D2 units", sl["D2"].value, 5580990))
checks.append(("xlsx NY E2 pct", sl["E2"].value, 60.2))
checks.append(("xlsx NY H2 margin", sl["H2"].value, 5536505))
checks.append(("xlsx NY I2 leader", sl["I2"].value, "Charter"))
checks.append(("xlsx NY J2 fabric", sl["J2"].value, 9267668))
checks.append(("xlsx NY M2 url", sl["M2"].value, SOURCE_URL))
checks.append(("xlsx last state PA", sl["A52"].value, "Pennsylvania"))
checks.append(("xlsx last margin", sl["H52"].value, -4356938))
checks.append(("xlsx last leader", sl["I52"].value, "Comcast"))
checks.append(("xlsx freeze", sl.freeze_panes, "A2"))

ch = wb2["Charter lead states"]
checks.append(("xlsx CH n", ch.max_row - 1, 19))
checks.append(("xlsx CH A2", ch["A2"].value, "New York"))
checks.append(("xlsx CH A20", ch["A20"].value, "Louisiana"))

cm = wb2["Comcast lead states"]
checks.append(("xlsx CM n", cm.max_row - 1, 27))
checks.append(("xlsx CM A2", cm["A2"].value, "Rhode Island"))
checks.append(("xlsx CM A28", cm["A28"].value, "Pennsylvania"))

ne = wb2["Neither"]
checks.append(("xlsx NE n", ne.max_row - 1, 5))
neither_names = [ne.cell(r, 1).value for r in range(2, 7)]
checks.append(
    ("xlsx NE states", neither_names, ["Alaska", "Iowa", "North Dakota", "Oklahoma", "South Dakota"])
)

print("\nVerification:")
all_ok = True
for name, got, expected in checks:
    ok = got == expected
    if not ok:
        all_ok = False
    print(f"  [{'OK' if ok else 'FAIL'}] {name}: got={got!r} expected={expected!r}")
print("ALL PASS" if all_ok else "SOME FAILED")
print("File size:", DEST.stat().st_size)
print("Sheet names:", wb2.sheetnames)
