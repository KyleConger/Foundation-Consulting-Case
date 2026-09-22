# -*- coding: utf-8 -*-
"""
Build Decisions/EH&B/State Region Density Maps.xlsx

Merge already-retrieved state files only. No new Census vintage. No metro
operator share. No TAM. No launch rec.

Sources (RETRIEVED):
- FCC BDC D25 state leads: Analysis/cable-share-small-firm/out/chtr_vs_cmcsa_state_leads.csv
- ACS 2024 B08301 usually-WFH: Analysis/work-from-home/out/acs2024_wfh_by_state.csv
- SUSB 2022 firm-size employment: Analysis/small-large-employment/out/state_employment_by_firm_size.csv
- Census 9-division / 4-region map: same as Decisions/CHURN/build_plays_strategies_by_region.py
"""
from __future__ import annotations

import csv
import json
import statistics
from collections import defaultdict
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.worksheet import Worksheet

ROOT = Path(r"c:\Users\Owner\Desktop\MAN6930 Case")
LEADS = ROOT / "Analysis" / "cable-share-small-firm" / "out" / "chtr_vs_cmcsa_state_leads.csv"
WFH = ROOT / "Analysis" / "work-from-home" / "out" / "acs2024_wfh_by_state.csv"
SUSB = ROOT / "Analysis" / "small-large-employment" / "out" / "state_employment_by_firm_size.csv"
OUT = ROOT / "Decisions" / "EH&B" / "State Region Density Maps.xlsx"
CANVAS_JSON = ROOT / "Decisions" / "EH&B" / "_density_maps_canvas.json"

# Census Bureau divisions (9). DC is in South Atlantic.
# Same map as Decisions/CHURN/build_plays_strategies_by_region.py
DIVISION: dict[str, tuple[str, str]] = {
    "CT": ("New England", "Northeast"),
    "ME": ("New England", "Northeast"),
    "MA": ("New England", "Northeast"),
    "NH": ("New England", "Northeast"),
    "RI": ("New England", "Northeast"),
    "VT": ("New England", "Northeast"),
    "NJ": ("Middle Atlantic", "Northeast"),
    "NY": ("Middle Atlantic", "Northeast"),
    "PA": ("Middle Atlantic", "Northeast"),
    "IL": ("East North Central", "Midwest"),
    "IN": ("East North Central", "Midwest"),
    "MI": ("East North Central", "Midwest"),
    "OH": ("East North Central", "Midwest"),
    "WI": ("East North Central", "Midwest"),
    "IA": ("West North Central", "Midwest"),
    "KS": ("West North Central", "Midwest"),
    "MN": ("West North Central", "Midwest"),
    "MO": ("West North Central", "Midwest"),
    "NE": ("West North Central", "Midwest"),
    "ND": ("West North Central", "Midwest"),
    "SD": ("West North Central", "Midwest"),
    "DE": ("South Atlantic", "South"),
    "DC": ("South Atlantic", "South"),
    "FL": ("South Atlantic", "South"),
    "GA": ("South Atlantic", "South"),
    "MD": ("South Atlantic", "South"),
    "NC": ("South Atlantic", "South"),
    "SC": ("South Atlantic", "South"),
    "VA": ("South Atlantic", "South"),
    "WV": ("South Atlantic", "South"),
    "AL": ("East South Central", "South"),
    "KY": ("East South Central", "South"),
    "MS": ("East South Central", "South"),
    "TN": ("East South Central", "South"),
    "AR": ("West South Central", "South"),
    "LA": ("West South Central", "South"),
    "OK": ("West South Central", "South"),
    "TX": ("West South Central", "South"),
    "AZ": ("Mountain", "West"),
    "CO": ("Mountain", "West"),
    "ID": ("Mountain", "West"),
    "MT": ("Mountain", "West"),
    "NV": ("Mountain", "West"),
    "NM": ("Mountain", "West"),
    "UT": ("Mountain", "West"),
    "WY": ("Mountain", "West"),
    "AK": ("Pacific", "West"),
    "CA": ("Pacific", "West"),
    "HI": ("Pacific", "West"),
    "OR": ("Pacific", "West"),
    "WA": ("Pacific", "West"),
}

DIV_ORDER = [
    "New England",
    "Middle Atlantic",
    "East North Central",
    "West North Central",
    "South Atlantic",
    "East South Central",
    "West South Central",
    "Mountain",
    "Pacific",
]
REG_ORDER = ["Northeast", "Midwest", "South", "West"]

GEORGIA = "Georgia"
NAVY = "1F4E79"
INK = "1A1A1A"
GRAY = "595959"
thin = Border(
    left=Side(style="thin", color="D0D0D0"),
    right=Side(style="thin", color="D0D0D0"),
    top=Side(style="thin", color="D0D0D0"),
    bottom=Side(style="thin", color="D0D0D0"),
)
font = Font(name=GEORGIA, size=10, color=INK)
font_b = Font(name=GEORGIA, size=10, bold=True, color=INK)
font_title = Font(name=GEORGIA, size=14, bold=True, color=NAVY)
font_h = Font(name=GEORGIA, size=10, bold=True, color="FFFFFF")
font_note = Font(name=GEORGIA, size=9, italic=True, color=GRAY)
font_small = Font(name=GEORGIA, size=8, color=GRAY)
fill_head = PatternFill("solid", fgColor=NAVY)
fill_chtr = PatternFill("solid", fgColor="D6E3F0")
fill_hyp = PatternFill("solid", fgColor="C6EFCE")
fill_neither = PatternFill("solid", fgColor="FFF2CC")
fill_white = PatternFill("solid", fgColor="FFFFFF")
fill_note = PatternFill("solid", fgColor="F7F7F7")
wrap = Alignment(wrap_text=True, vertical="center")
left = Alignment(wrap_text=True, vertical="center", horizontal="left")
center = Alignment(wrap_text=True, vertical="center", horizontal="center")

CITE_FCC = (
    "Federal Communications Commission, Broadband Data Collection / National Broadband Map, "
    "as of 31 Dec 2025 (D25), file revision 15 Sep 2026. Metric: res_st_pct = share of "
    "residential units at Broadband Serviceable Locations where the holding company reports "
    "residential fixed broadband availability. Estimated units = res_st_pct × state residential "
    "fabric units. Availability, not subscribers. Charter Communications (Spectrum, provider_id "
    "130235, FRN 0025646373); Comcast Corporation (Xfinity, provider_id 130317, FRN 0003768165). "
    "Files: bdc_us_provider_list_D25_15sep2026.csv; "
    "bdc_us_provider_summary_by_geography_D25_15sep2026.csv; "
    "bdc_us_fixed_broadband_summary_by_geography_D25_15sep2026.csv; "
    "bdc_us_fixed_broadband_provider_summary_D25_15sep2026.csv. "
    "URL: https://broadbandmap.fcc.gov/data-download"
)
CITE_ACS = (
    "U.S. Census Bureau, American Community Survey (ACS) 1-Year Estimates Detailed Tables, "
    "2024, table B08301 Means of Transportation to Work. Variable: B08301_021E Worked from home "
    "/ B08301_001E Total; universe = Workers 16 years and over; usually worked from home as "
    "means of transportation to work (journey-to-work). Pulled via Census Reporter API wrapping "
    "ACS 2024 1-year release (release id acs2024_1yr). Do not mix with ATUS (any work at home on "
    "days worked) or ABS (share of firms with any WFH employees). "
    "URL: https://data.census.gov/table/ACSDT1Y2024.B08301 · "
    "Census Reporter: https://api.censusreporter.org/1.0/data/show/latest?table_ids=B08301&geo_ids=040%7C01000US,01000US"
)
CITE_SUSB = (
    "U.S. Census Bureau, Statistics of U.S. Businesses (SUSB), 2022 Annual Datasets by "
    "Establishment Industry — us_state_naics_detailedsizes_2022.txt (all-industry NAICS=--, "
    "enterprise employment size); reference year 2022; datasets page April 2025; file "
    "last-modified 2025-04-10. Mid-March payroll employment at employer establishments, "
    "classified by enterprise (firm) employment size; primary split firms <500 vs 500+ "
    "employees (SBA cutoff). File: https://www2.census.gov/programs-surveys/susb/tables/2022/"
    "us_state_naics_detailedsizes_2022.txt · Landing page: "
    "https://www.census.gov/data/datasets/2022/econ/susb/2022-susb.html"
)
CITE_DIV = (
    "U.S. Census Bureau Geographic Division and Census Region definitions (9 divisions, "
    "4 regions). District of Columbia is in South Atlantic / South. Same map as "
    "Decisions/CHURN/build_plays_strategies_by_region.py. "
    "https://www.census.gov/programs-surveys/popest/guidance-geographies/terms-and-definitions.html"
)


def load_csv(path: Path) -> list[dict]:
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def num(x, default=None):
    if x is None or x == "":
        return default
    return float(x)


def fips2(x: str) -> str:
    return str(x).zfill(2)


def apply_header(ws: Worksheet, ncols: int, row: int = 1):
    for col in range(1, ncols + 1):
        cell = ws.cell(row, col)
        cell.font = font_h
        cell.fill = fill_head
        cell.alignment = wrap
        cell.border = thin
    ws.freeze_panes = f"A{row + 1}"
    ws.auto_filter.ref = f"A{row}:{get_column_letter(ncols)}{ws.max_row}"


def set_widths(ws: Worksheet, widths: list[float]):
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w


def paint(ws: Worksheet, r: int, c: int, value, fmt=None, fill=None, align=None, fnt=None):
    cell = ws.cell(r, c, value)
    cell.font = fnt or font
    cell.alignment = align or wrap
    cell.border = thin
    if fmt:
        cell.number_format = fmt
    if fill:
        cell.fill = fill
    return cell


def median_51(values: list[float]) -> float:
    assert len(values) == 51
    return float(statistics.median(values))


def main():
    leads = load_csv(LEADS)
    wfh_raw = load_csv(WFH)
    susb_raw = load_csv(SUSB)

    wfh_us = next(r for r in wfh_raw if r["geo_level"] == "nation")
    wfh_states = [r for r in wfh_raw if r["geo_level"] == "state"]
    assert len(leads) == 51
    assert len(wfh_states) == 51
    assert len(susb_raw) == 51

    wfh_by_fips = {r["geo_id"][-2:]: r for r in wfh_states}
    susb_by_fips = {fips2(r["geo_id"]): r for r in susb_raw}

    rows = []
    for r in leads:
        fips = fips2(r["state_fips"])
        abbr = r["abbr"]
        assert abbr in DIVISION, abbr
        div, reg = DIVISION[abbr]
        w = wfh_by_fips[fips]
        s = susb_by_fips[fips]
        assert w["geography"] == r["state"] or (
            r["state"] == "District of Columbia" and w["geography"] == "District of Columbia"
        )
        assert s["geo_name"] == r["state"]
        leader = r["leader"]
        if leader == "neither present":
            leader_flag = "Neither"
        else:
            leader_flag = leader
        rec = {
            "fips": fips,
            "state": r["state"],
            "abbr": abbr,
            "division": div,
            "region": reg,
            "leader": leader_flag,
            "charter_lead": leader == "Charter",
            "total_residential_units": int(float(r["total_residential_units"])),
            "charter_res_st_pct": num(r["charter_res_st_pct"]),
            "comcast_res_st_pct": num(r["comcast_res_st_pct"]),
            "charter_est_units": int(float(r["charter_est_units"])) if r["charter_est_units"] else None,
            "comcast_est_units": int(float(r["comcast_est_units"])) if r["comcast_est_units"] else None,
            "margin_units": int(float(r["margin_units_charter_minus_comcast"])),
            "margin_pp": float(r["margin_pp_charter_minus_comcast"]),
            "workers_16_plus": int(float(w["workers_16_plus"])),
            "worked_from_home": int(float(w["worked_from_home"])),
            "wfh_rate_pct": float(w["wfh_rate_pct"]),
            "employment_total": int(float(s["employment_total"])),
            "employment_ge500": int(float(s["employment_ge500"])),
            "employment_lt500": int(float(s["employment_lt500"])),
            "share_ge500_pct": float(s["share_ge500_pct"]),
            "share_lt500_pct": float(s["share_lt500_pct"]),
            "origin": "RETRIEVED",
        }
        rows.append(rec)

    assert len(rows) == 51
    assert {r["abbr"] for r in rows} == set(DIVISION)

    wfh_rates = [r["wfh_rate_pct"] for r in rows]
    ge500_shares = [r["share_ge500_pct"] for r in rows]
    wfh_med = median_51(wfh_rates)
    ge500_med = median_51(ge500_shares)

    for r in rows:
        r["wfh_above_median"] = r["wfh_rate_pct"] > wfh_med
        r["ge500_above_median"] = r["share_ge500_pct"] > ge500_med
        r["ehb_plausible"] = (
            r["charter_lead"] and r["wfh_above_median"] and r["ge500_above_median"]
        )

    n_chtr = sum(1 for r in rows if r["leader"] == "Charter")
    n_cmcsa = sum(1 for r in rows if r["leader"] == "Comcast")
    n_neither = sum(1 for r in rows if r["leader"] == "Neither")
    n_hyp = sum(1 for r in rows if r["ehb_plausible"])
    hyp_states = [r for r in rows if r["ehb_plausible"]]

    us_workers = int(float(wfh_us["workers_16_plus"]))
    us_wfh = int(float(wfh_us["worked_from_home"]))
    us_wfh_pct = us_wfh / us_workers * 100
    us_emp = sum(r["employment_total"] for r in rows)
    us_ge500 = sum(r["employment_ge500"] for r in rows)
    us_ge500_pct = us_ge500 / us_emp * 100

    # Sanity: ACS US row vs sum of states (ACS US includes PR? nation row is 165360450;
    # 51-state+DC sum should be close but not identical if PR excluded from state file).
    state_workers = sum(r["workers_16_plus"] for r in rows)
    state_wfh = sum(r["worked_from_home"] for r in rows)

    def rollup(key: str, order: list[str]):
        out = []
        for name in order:
            grp = [r for r in rows if r[key] == name]
            workers = sum(r["workers_16_plus"] for r in grp)
            wfh_n = sum(r["worked_from_home"] for r in grp)
            emp = sum(r["employment_total"] for r in grp)
            ge500 = sum(r["employment_ge500"] for r in grp)
            units = sum(r["total_residential_units"] for r in grp)
            ch_u = sum(r["charter_est_units"] or 0 for r in grp)
            cm_u = sum(r["comcast_est_units"] or 0 for r in grp)
            rec = {
                "name": name,
                "n_states": len(grp),
                "n_charter_lead": sum(1 for r in grp if r["leader"] == "Charter"),
                "n_comcast_lead": sum(1 for r in grp if r["leader"] == "Comcast"),
                "n_neither": sum(1 for r in grp if r["leader"] == "Neither"),
                "n_ehb_plausible": sum(1 for r in grp if r["ehb_plausible"]),
                "margin_units": sum(r["margin_units"] for r in grp),
                "charter_est_units": ch_u,
                "comcast_est_units": cm_u,
                "total_residential_units": units,
                "workers_16_plus": workers,
                "worked_from_home": wfh_n,
                "wfh_rate_pct_weighted": (wfh_n / workers * 100) if workers else None,
                "employment_total": emp,
                "employment_ge500": ge500,
                "share_ge500_pct_weighted": (ge500 / emp * 100) if emp else None,
                "states": ", ".join(r["abbr"] for r in sorted(grp, key=lambda x: x["abbr"])),
            }
            out.append(rec)
        return out

    div_roll = rollup("division", DIV_ORDER)
    reg_roll = rollup("region", REG_ORDER)

    # Sorted views
    by_margin = sorted(rows, key=lambda r: r["margin_units"], reverse=True)
    by_wfh = sorted(rows, key=lambda r: r["wfh_rate_pct"], reverse=True)
    by_ge500 = sorted(rows, key=lambda r: r["share_ge500_pct"], reverse=True)

    top_chtr = [r for r in by_margin if r["leader"] == "Charter"][:1][0]
    top_cmcsa = [r for r in by_margin if r["leader"] == "Comcast"][-1]
    # largest Comcast lead = most negative margin
    max_cmcsa = min((r for r in rows if r["leader"] == "Comcast"), key=lambda r: r["margin_units"])
    max_chtr = max((r for r in rows if r["leader"] == "Charter"), key=lambda r: r["margin_units"])

    # Division with most Charter-lead states and largest unit margin
    div_by_margin = sorted(div_roll, key=lambda d: d["margin_units"], reverse=True)
    div_by_chtr_n = sorted(div_roll, key=lambda d: (d["n_charter_lead"], d["margin_units"]), reverse=True)
    div_by_wfh = sorted(div_roll, key=lambda d: d["wfh_rate_pct_weighted"], reverse=True)
    div_by_ge500 = sorted(div_roll, key=lambda d: d["share_ge500_pct_weighted"], reverse=True)
    reg_by_wfh = sorted(reg_roll, key=lambda d: d["wfh_rate_pct_weighted"], reverse=True)
    reg_by_ge500 = sorted(reg_roll, key=lambda d: d["share_ge500_pct_weighted"], reverse=True)

    finding_b = (
        f"ACS usual-WFH ranges from {by_wfh[0]['wfh_rate_pct']:.1f}% in {by_wfh[0]['state']} "
        f"to {by_wfh[-1]['wfh_rate_pct']:.1f}% in {by_wfh[-1]['state']}; "
        f"worker-weighted, {div_by_wfh[0]['name']} is highest among the 9 divisions at "
        f"{div_by_wfh[0]['wfh_rate_pct_weighted']:.1f}% vs {div_by_wfh[-1]['name']} at "
        f"{div_by_wfh[-1]['wfh_rate_pct_weighted']:.1f}% "
        f"(US {us_wfh_pct:.1f}%; 51-state+DC worker-weighted {state_wfh / state_workers * 100:.1f}%)."
    )
    finding_c = (
        f"{by_ge500[0]['state']} has the highest 500+ firm employment share at "
        f"{by_ge500[0]['share_ge500_pct']:.1f}%; {by_ge500[-1]['state']} is lowest at "
        f"{by_ge500[-1]['share_ge500_pct']:.1f}%; employment-weighted, "
        f"{div_by_ge500[0]['name']} is the most large-firm-dense division at "
        f"{div_by_ge500[0]['share_ge500_pct_weighted']:.1f}% vs {div_by_ge500[-1]['name']} at "
        f"{div_by_ge500[-1]['share_ge500_pct_weighted']:.1f}% "
        f"(US / 51-state+DC {us_ge500_pct:.1f}%)."
    )

    wsc = next(d for d in div_roll if d["name"] == "West South Central")
    wnc = next(d for d in div_roll if d["name"] == "West North Central")
    esc = next(d for d in div_roll if d["name"] == "East South Central")
    finding_a = (
        f"Charter leads Comcast on residential locations in {n_chtr} of 51 states "
        f"(+{max_chtr['margin_units'] / 1e6:.2f}M units in {max_chtr['state']}) against "
        f"{n_cmcsa} Comcast-lead states ({max_cmcsa['margin_units'] / 1e6:.2f}M in "
        f"{max_cmcsa['state']}); by Census division the only positive Charter unit margins "
        f"are West South Central ({wsc['margin_units'] / 1e6:+.2f}M, Texas-driven), "
        f"West North Central ({wnc['margin_units'] / 1e6:+.2f}M), and East South Central "
        f"({esc['margin_units'] / 1e6:+.2f}M)."
    )

    # --- Excel ---
    wb = Workbook()

    # Notes
    ws = wb.active
    ws.title = "Notes"
    notes = [
        ("State + region density maps — EH&B diagnostic (not a recommendation)",),
        (),
        ("What this is", "State-level density of three already-retrieved EH&B inputs, rolled to Census division and region. No TAM. No launch rec. No metro operator share."),
        ("What this is not", "Not subscriber share. Not Form 477. Not ATUS or ABS WFH. Not a new Census vintage. Not a recommendation."),
        (),
        ("A. Charter vs Comcast", "FCC BDC D25 residential location availability (res_st_pct). Leader = strictly larger res_st_pct. Missing provider row = absent. Estimated units = res_st_pct × fabric units. Origin: RETRIEVED."),
        ("B. Work-from-home", "ACS 2024 B08301 usually worked from home, workers 16+. State WFH = ACS only. Division/region rates are worker-weighted (sum WFH / sum workers). Origin: RETRIEVED."),
        ("C. Large-firm density", "SUSB 2022 share of mid-March payroll employment at firms with 500+ employees (enterprise). Division/region shares are employment-weighted. Origin: RETRIEVED."),
        ("D. Combined table", "One row per state: three metrics + division + Charter leader flag. Optional HYPOTHESIS score labeled as such."),
        (),
        ("HYPOTHESIS rule (not a recommendation)", "EH&B-plausible = Charter-lead AND above-median ACS usual-WFH AND above-median SUSB 500+ employment share. Medians are unweighted across 51 states+DC. Show the rule; do not call it a recommendation."),
        ("Median ACS usual-WFH (51)", round(wfh_med, 6)),
        ("Median SUSB 500+ share (51)", round(ge500_med, 6)),
        ("States hitting EH&B-plausible", n_hyp),
        ("EH&B-plausible states", ", ".join(f"{r['abbr']} ({r['state']})" for r in hyp_states) or "none"),
        (),
        ("Census geography", CITE_DIV),
        ("Vintages differ", "FCC BDC as-of 2025-12-31 (D25); ACS 2024 1-year; SUSB reference year 2022. Do not treat as the same year."),
        ("Unwilling to claim", "Metro-level Charter vs Comcast share (not in the retrieved state files). Subscriber share. That the hypothesis flags a launch market."),
        ("Prior EH&B files", "Does not change headline numbers in Comcast vs Charter.xlsx, Work from Home Rates.xlsx, or Small Large Employment Shares.xlsx. This workbook adds the merge + division rollups."),
        (),
        ("Finding A", finding_a),
        ("Finding B", finding_b),
        ("Finding C", finding_c),
        (),
        ("Citations",),
        ("FCC BDC", CITE_FCC),
        ("ACS B08301", CITE_ACS),
        ("SUSB 2022", CITE_SUSB),
        (),
        ("Builder", "Decisions/EH&B/build_state_region_density_maps.py — recomputes rollups from the three CSVs."),
    ]
    for i, row in enumerate(notes, 1):
        if not row:
            continue
        ws.cell(i, 1, row[0]).font = font_b if i == 1 or row[0] in {
            "What this is", "What this is not", "A. Charter vs Comcast", "B. Work-from-home",
            "C. Large-firm density", "D. Combined table", "HYPOTHESIS rule (not a recommendation)",
            "Census geography", "Vintages differ", "Unwilling to claim", "Prior EH&B files",
            "Finding A", "Finding B", "Finding C", "Citations", "FCC BDC", "ACS B08301",
            "SUSB 2022", "Builder", "Median ACS usual-WFH (51)", "Median SUSB 500+ share (51)",
            "States hitting EH&B-plausible", "EH&B-plausible states",
        } else font
        if i == 1:
            ws.cell(i, 1).font = font_title
        if len(row) > 1:
            ws.cell(i, 2, row[1]).font = font
            ws.cell(i, 2).alignment = wrap
        ws.row_dimensions[i].height = 36 if i == 1 or (len(row) > 1 and isinstance(row[1], str) and len(row[1]) > 80) else 18
    ws.column_dimensions["A"].width = 36
    ws.column_dimensions["B"].width = 110
    ws.row_dimensions[1].height = 22

    # State combined
    ws = wb.create_sheet("State combined")
    headers = [
        "fips", "state", "abbr", "census_division", "census_region",
        "leader", "charter_lead_flag",
        "charter_res_st_pct", "comcast_res_st_pct",
        "charter_est_units", "comcast_est_units",
        "margin_units_chtr_minus_cmcsa", "margin_pp_chtr_minus_cmcsa",
        "total_residential_units",
        "acs_wfh_rate_pct", "acs_workers_16_plus", "acs_worked_from_home",
        "susb_share_ge500_pct", "susb_employment_ge500", "susb_employment_total",
        "wfh_above_median", "ge500_above_median",
        "ehb_plausible_HYPOTHESIS", "origin",
    ]
    ws.append(headers)
    apply_header(ws, len(headers))
    for i, r in enumerate(sorted(rows, key=lambda x: x["state"]), 2):
        vals = [
            r["fips"], r["state"], r["abbr"], r["division"], r["region"],
            r["leader"], "Yes" if r["charter_lead"] else "No",
            None if r["charter_res_st_pct"] is None else r["charter_res_st_pct"] * 100,
            None if r["comcast_res_st_pct"] is None else r["comcast_res_st_pct"] * 100,
            r["charter_est_units"], r["comcast_est_units"],
            r["margin_units"], r["margin_pp"],
            r["total_residential_units"],
            r["wfh_rate_pct"], r["workers_16_plus"], r["worked_from_home"],
            r["share_ge500_pct"], r["employment_ge500"], r["employment_total"],
            "Yes" if r["wfh_above_median"] else "No",
            "Yes" if r["ge500_above_median"] else "No",
            "Yes" if r["ehb_plausible"] else "No",
            "RETRIEVED",
        ]
        fill = fill_hyp if r["ehb_plausible"] else (fill_chtr if r["charter_lead"] else (fill_neither if r["leader"] == "Neither" else fill_white))
        for c, v in enumerate(vals, 1):
            paint(ws, i, c, v, fill=fill)
        for c in (8, 9, 13, 15, 18):
            ws.cell(i, c).number_format = "0.00"
        for c in (10, 11, 12, 14, 16, 17, 19, 20):
            ws.cell(i, c).number_format = "#,##0"
    set_widths(ws, [6, 22, 6, 22, 12, 10, 12, 14, 14, 16, 16, 18, 14, 16, 12, 16, 16, 14, 16, 16, 12, 14, 18, 12])
    ws.auto_filter.ref = ws.dimensions
    note_row = 54
    ws.cell(note_row, 1, "HYPOTHESIS (green): Charter-lead AND ACS WFH > median AND SUSB 500+ share > median. Not a recommendation. Blue = Charter-lead only. Yellow = neither operator present in FCC state summary.").font = font_note
    ws.merge_cells(start_row=note_row, start_column=1, end_row=note_row, end_column=8)

    # Division rollup
    ws = wb.create_sheet("Division rollup")
    ws["A1"] = "Census division rollup (9) and region rollup (4) — weighted rates"
    ws["A1"].font = font_title
    ws.merge_cells("A1:R1")
    ws["A2"] = (
        "WFH rate = sum(ACS worked-from-home) / sum(ACS workers 16+). "
        "500+ share = sum(SUSB 500+ employment) / sum(SUSB employment). "
        "Unit margin = sum(Charter est. units − Comcast est. units). RETRIEVED inputs; DERIVED rollups."
    )
    ws["A2"].font = font_note
    ws.merge_cells("A2:R2")

    div_headers = [
        "level", "name", "n_states", "n_charter_lead", "n_comcast_lead", "n_neither",
        "n_ehb_plausible_HYPOTHESIS", "margin_units_chtr_minus_cmcsa",
        "charter_est_units", "comcast_est_units", "total_residential_units",
        "acs_workers_16_plus", "acs_worked_from_home", "acs_wfh_rate_pct_weighted",
        "susb_employment_total", "susb_employment_ge500", "susb_share_ge500_pct_weighted",
        "states",
    ]
    start = 4
    for c, h in enumerate(div_headers, 1):
        paint(ws, start, c, h, fill=fill_head, fnt=font_h)
    rr = start + 1
    for rec in div_roll:
        vals = [
            "division", rec["name"], rec["n_states"], rec["n_charter_lead"],
            rec["n_comcast_lead"], rec["n_neither"], rec["n_ehb_plausible"],
            rec["margin_units"], rec["charter_est_units"], rec["comcast_est_units"],
            rec["total_residential_units"], rec["workers_16_plus"], rec["worked_from_home"],
            rec["wfh_rate_pct_weighted"], rec["employment_total"], rec["employment_ge500"],
            rec["share_ge500_pct_weighted"], rec["states"],
        ]
        for c, v in enumerate(vals, 1):
            paint(ws, rr, c, v)
        for c in (8, 9, 10, 11, 12, 13, 15, 16):
            ws.cell(rr, c).number_format = "#,##0"
        for c in (14, 17):
            ws.cell(rr, c).number_format = "0.00"
        rr += 1
    rr += 1
    for c, h in enumerate(div_headers, 1):
        paint(ws, rr, c, h, fill=fill_head, fnt=font_h)
    rr += 1
    for rec in reg_roll:
        vals = [
            "region", rec["name"], rec["n_states"], rec["n_charter_lead"],
            rec["n_comcast_lead"], rec["n_neither"], rec["n_ehb_plausible"],
            rec["margin_units"], rec["charter_est_units"], rec["comcast_est_units"],
            rec["total_residential_units"], rec["workers_16_plus"], rec["worked_from_home"],
            rec["wfh_rate_pct_weighted"], rec["employment_total"], rec["employment_ge500"],
            rec["share_ge500_pct_weighted"], rec["states"],
        ]
        for c, v in enumerate(vals, 1):
            paint(ws, rr, c, v)
        for c in (8, 9, 10, 11, 12, 13, 15, 16):
            ws.cell(rr, c).number_format = "#,##0"
        for c in (14, 17):
            ws.cell(rr, c).number_format = "0.00"
        rr += 1
    rr += 1
    paint(ws, rr, 1, "Geography map (documented)", fnt=font_b)
    rr += 1
    paint(ws, rr, 1, CITE_DIV)
    ws.merge_cells(start_row=rr, start_column=1, end_row=rr, end_column=8)
    ws.row_dimensions[rr].height = 48
    set_widths(ws, [10, 22, 10, 14, 14, 10, 16, 18, 16, 16, 16, 16, 16, 16, 16, 16, 16, 40])
    ws.freeze_panes = "A5"

    def metric_sheet(title: str, claim: str, cite: str, headers: list[str], data_rows: list[list], formats: dict[int, str], extra_notes: list[str]):
        sh = wb.create_sheet(title)
        sh["A1"] = claim
        sh["A1"].font = font_title
        sh.merge_cells("A1:L1")
        sh.row_dimensions[1].height = 48
        sh["A2"] = cite
        sh["A2"].font = font_note
        sh.merge_cells("A2:L2")
        sh.row_dimensions[2].height = 56
        for c, h in enumerate(headers, 1):
            paint(sh, 4, c, h, fill=fill_head, fnt=font_h)
        for i, vals in enumerate(data_rows, 5):
            for c, v in enumerate(vals, 1):
                paint(sh, i, c, v)
            for c, fmt in formats.items():
                sh.cell(i, c).number_format = fmt
        sh.freeze_panes = "A5"
        sh.auto_filter.ref = f"A4:{get_column_letter(len(headers))}{4 + len(data_rows)}"
        nr = 6 + len(data_rows)
        for note in extra_notes:
            sh.cell(nr, 1, note).font = font_note
            sh.merge_cells(start_row=nr, start_column=1, end_row=nr, end_column=min(8, len(headers)))
            sh.row_dimensions[nr].height = 32
            nr += 1
        set_widths(sh, [22] + [14] * (len(headers) - 1))
        return sh

    # A sheet — all 51 sorted by margin
    metric_sheet(
        "A Charter vs Comcast",
        finding_a,
        CITE_FCC,
        [
            "sort_rank", "state", "abbr", "census_division", "census_region", "leader",
            "margin_units_chtr_minus_cmcsa", "margin_pp",
            "charter_res_st_pct", "comcast_res_st_pct",
            "charter_est_units", "comcast_est_units", "total_residential_units",
            "chart_chtr_lead_m", "chart_cmcsa_lead_m", "origin",
        ],
        [
            [
                i,
                r["state"], r["abbr"], r["division"], r["region"], r["leader"],
                r["margin_units"], r["margin_pp"],
                None if r["charter_res_st_pct"] is None else r["charter_res_st_pct"] * 100,
                None if r["comcast_res_st_pct"] is None else r["comcast_res_st_pct"] * 100,
                r["charter_est_units"], r["comcast_est_units"], r["total_residential_units"],
                r["margin_units"] / 1e6 if r["margin_units"] > 0 else 0.0,
                abs(r["margin_units"]) / 1e6 if r["margin_units"] < 0 else 0.0,
                "RETRIEVED",
            ]
            for i, r in enumerate(by_margin, 1)
        ],
        {7: "#,##0", 8: "0.00", 9: "0.00", 10: "0.00", 11: "#,##0", 12: "#,##0", 13: "#,##0", 14: "0.00", 15: "0.00"},
        [
            "Chart columns chart_chtr_lead_m / chart_cmcsa_lead_m are millions of estimated residential units; split so Charter-lead and Comcast-lead can be drawn as two series (one accent). Axis must start at zero.",
            "5 states have neither operator in the FCC state summary (AK, IA, ND, OK, SD); margin = 0. Beating = strictly larger res_st_pct. Availability, not subscribers.",
        ],
    )

    # B sheet
    metric_sheet(
        "B WFH ACS",
        finding_b,
        CITE_ACS,
        [
            "sort_rank", "state", "abbr", "census_division", "census_region",
            "acs_wfh_rate_pct", "acs_workers_16_plus", "acs_worked_from_home",
            "above_us_13_3", "above_median", "leader", "origin",
        ],
        [
            [
                i, r["state"], r["abbr"], r["division"], r["region"],
                r["wfh_rate_pct"], r["workers_16_plus"], r["worked_from_home"],
                "Yes" if r["wfh_rate_pct"] > us_wfh_pct else "No",
                "Yes" if r["wfh_above_median"] else "No",
                r["leader"], "RETRIEVED",
            ]
            for i, r in enumerate(by_wfh, 1)
        ],
        {6: "0.00", 7: "#,##0", 8: "#,##0"},
        [
            f"US ACS usual-WFH = {us_wfh_pct:.6f}% on {us_workers:,} workers 16+ ({us_wfh:,} usually WFH). "
            f"51-state+DC sum = {state_workers:,} workers / {state_wfh:,} WFH "
            f"({state_wfh / state_workers * 100:.6f}%). Nation row includes geographies beyond the 51; use the nation row for US, worker-weight the 51 for division/region.",
            f"Unweighted median of 51 state rates = {wfh_med:.6f}%. Used only for the HYPOTHESIS flag. Division averages are worker-weighted, not an unweighted mean of state rates.",
            "State WFH on this sheet is ACS B08301 only. ATUS and ABS are different metrics and are not mapped here.",
        ],
    )

    # C sheet
    metric_sheet(
        "C Large-firm 500+",
        finding_c,
        CITE_SUSB,
        [
            "sort_rank", "state", "abbr", "census_division", "census_region",
            "susb_share_ge500_pct", "susb_employment_ge500", "susb_employment_total",
            "susb_share_lt500_pct", "above_us_54_1", "above_median", "leader", "origin",
        ],
        [
            [
                i, r["state"], r["abbr"], r["division"], r["region"],
                r["share_ge500_pct"], r["employment_ge500"], r["employment_total"],
                r["share_lt500_pct"],
                "Yes" if r["share_ge500_pct"] > us_ge500_pct else "No",
                "Yes" if r["ge500_above_median"] else "No",
                r["leader"], "RETRIEVED",
            ]
            for i, r in enumerate(by_ge500, 1)
        ],
        {6: "0.00", 7: "#,##0", 8: "#,##0", 9: "0.00"},
        [
            f"51-state+DC SUSB employment total = {us_emp:,}; 500+ = {us_ge500:,}; share = {us_ge500_pct:.6f}%. "
            "Matches the published US all-industry figure in the source analysis when the US row is used separately (US row includes the same 51).",
            f"Unweighted median of 51 state 500+ shares = {ge500_med:.6f}%. Used only for the HYPOTHESIS flag. Division averages are employment-weighted.",
        ],
    )

    wb.save(OUT)

    # Canvas payload
    def pack_state(r):
        return {
            "abbr": r["abbr"],
            "state": r["state"],
            "division": r["division"],
            "region": r["region"],
            "leader": r["leader"],
            "margin_units": r["margin_units"],
            "margin_m": round(r["margin_units"] / 1e6, 2),
            "chtr_m": round(r["margin_units"] / 1e6, 2) if r["margin_units"] > 0 else 0.0,
            "cmcsa_m": round(abs(r["margin_units"]) / 1e6, 2) if r["margin_units"] < 0 else 0.0,
            "charter_pct": None if r["charter_res_st_pct"] is None else round(r["charter_res_st_pct"] * 100, 1),
            "comcast_pct": None if r["comcast_res_st_pct"] is None else round(r["comcast_res_st_pct"] * 100, 1),
            "wfh_pct": round(r["wfh_rate_pct"], 1),
            "workers": r["workers_16_plus"],
            "ge500_pct": round(r["share_ge500_pct"], 1),
            "emp": r["employment_total"],
            "ehb_plausible": r["ehb_plausible"],
            "wfh_above_med": r["wfh_above_median"],
            "ge500_above_med": r["ge500_above_median"],
        }

    payload = {
        "n_charter": n_chtr,
        "n_comcast": n_cmcsa,
        "n_neither": n_neither,
        "n_hyp": n_hyp,
        "hyp_states": [f"{r['abbr']}" for r in hyp_states],
        "wfh_med": round(wfh_med, 4),
        "ge500_med": round(ge500_med, 4),
        "us_wfh_pct": round(us_wfh_pct, 2),
        "us_ge500_pct": round(us_ge500_pct, 2),
        "state_wfh_pct": round(state_wfh / state_workers * 100, 2),
        "finding_a": finding_a,
        "finding_b": finding_b,
        "finding_c": finding_c,
        "by_margin": [pack_state(r) for r in by_margin],
        "by_wfh": [pack_state(r) for r in by_wfh],
        "by_ge500": [pack_state(r) for r in by_ge500],
        "div_roll": [
            {
                **{k: rec[k] for k in rec if k != "states"},
                "states": rec["states"],
                "margin_m": round(rec["margin_units"] / 1e6, 2),
                "wfh_pct": round(rec["wfh_rate_pct_weighted"], 1),
                "ge500_pct": round(rec["share_ge500_pct_weighted"], 1),
            }
            for rec in div_roll
        ],
        "reg_roll": [
            {
                **{k: rec[k] for k in rec if k != "states"},
                "states": rec["states"],
                "margin_m": round(rec["margin_units"] / 1e6, 2),
                "wfh_pct": round(rec["wfh_rate_pct_weighted"], 1),
                "ge500_pct": round(rec["share_ge500_pct_weighted"], 1),
            }
            for rec in reg_roll
        ],
    }
    CANVAS_JSON.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print("WROTE", OUT)
    print("N_HYP", n_hyp, payload["hyp_states"])
    print("WFH_MED", wfh_med)
    print("GE500_MED", ge500_med)
    print("US_WFH", us_wfh_pct, "STATE_WFH", state_wfh / state_workers * 100)
    print("US_GE500", us_ge500_pct)
    print("FINDING_A", finding_a)
    print("FINDING_B", finding_b)
    print("FINDING_C", finding_c)
    print("DIV_MARGIN")
    for d in div_roll:
        print(f"  {d['name']}: chtr={d['n_charter_lead']} cmcsa={d['n_comcast_lead']} neither={d['n_neither']} margin={d['margin_units']:,} wfh={d['wfh_rate_pct_weighted']:.2f} ge500={d['share_ge500_pct_weighted']:.2f} hyp={d['n_ehb_plausible']}")
    print("REG")
    for d in reg_roll:
        print(f"  {d['name']}: chtr={d['n_charter_lead']} cmcsa={d['n_comcast_lead']} margin={d['margin_units']:,} wfh={d['wfh_rate_pct_weighted']:.2f} ge500={d['share_ge500_pct_weighted']:.2f} hyp={d['n_ehb_plausible']}")
    print("HYP DETAIL")
    for r in hyp_states:
        print(f"  {r['abbr']} {r['state']} wfh={r['wfh_rate_pct']:.2f} ge500={r['share_ge500_pct']:.2f} margin={r['margin_units']:,}")


if __name__ == "__main__":
    main()
