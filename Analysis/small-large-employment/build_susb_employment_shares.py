#!/usr/bin/env python3
"""
SUSB employment shares by enterprise size — US, state, MSA (2022).

RETRIEVED source:
  Census Bureau, Statistics of U.S. Businesses (SUSB) 2022 Annual Datasets
  by Establishment Industry, Data by Enterprise Employment Size.
  https://www.census.gov/data/datasets/2022/econ/susb/2022-susb.html

Files:
  - us_state_naics_detailedsizes_2022.txt  (US + states; detailed ENTRSIZE 01–26)
  - msa_3digitnaics_2022.txt               (MSA/µSA; standard ENTRSIZE 01–09)

Definition (one sentence for exhibits):
  SUSB employment is mid-March payroll employment at employer establishments,
  classified by the employment size of the enterprise (firm), not the
  establishment; nonemployers, most government, and agriculture (NAICS 11
  crop/animal except support) are out of scope.

Primary split: SBA small-business cutoff — employment at firms <500 vs 500+.
All inputs tagged RETRIEVED. Suppressed cells (EMPLFL_N in {S,D}) are flagged;
no imputation.
"""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path

YEAR = 2022
ROOT = Path(__file__).resolve().parent
RAW = ROOT / "raw"
OUT = ROOT / "out"

STATE_FILE = RAW / "us_state_naics_detailedsizes_2022.txt"
MSA_FILE = RAW / "msa_3digitnaics_2022.txt"

AGENCY = "U.S. Census Bureau"
PROGRAM = "Statistics of U.S. Businesses (SUSB)"
SOURCE_PAGE_URL = "https://www.census.gov/data/datasets/2022/econ/susb/2022-susb.html"
# Dataset landing page dated April 2025; US/state detailed-sizes file last-modified
# 2025-04-10 on www2.census.gov; MSA dataset revised 2025-07-22 (originally 2025-05-29).
STATE_RELEASE_NOTE = "reference year 2022; datasets page April 2025; file last-modified 2025-04-10"
MSA_RELEASE_NOTE = (
    "reference year 2022; MSA dataset originally released 2025-05-29, "
    "revised 2025-07-22 (extraneous estimates removed; remaining estimates unchanged)"
)
STATE_FILE_NAME = "us_state_naics_detailedsizes_2022.txt"
MSA_FILE_NAME = "msa_3digitnaics_2022.txt"
STATE_TABLE_URL = (
    "https://www2.census.gov/programs-surveys/susb/tables/2022/"
    "us_state_naics_detailedsizes_2022.txt"
)
MSA_TABLE_URL = (
    "https://www2.census.gov/programs-surveys/susb/datasets/2022/"
    "msa_3digitnaics_2022.txt"
)
ENTERPRISE_CODES_URL = (
    "https://www2.census.gov/programs-surveys/susb/technical-documentation/"
    "enterprise_codes_2017.txt"
)
MEASURE = (
    "mid-March payroll employment at employer establishments, "
    "classified by enterprise (firm) employment size; "
    "primary split firms <500 vs 500+ employees (SBA cutoff)"
)

# Back-compat aliases used elsewhere in this script
SOURCE_URL = SOURCE_PAGE_URL

# IMPORTANT: In the detailed US/state file, the ENTRSIZE field codes are NOT the
# documentation sequence 01–26 (e.g. published "<500" is ENTRSIZE=37, while
# ENTRSIZE=19 is "750-999"). Always key off the leading NN in ENTRSIZEDSCR
# ("19: <500"), which matches Census enterprise_codes_2017.txt.
#
# Documentation size-class numbers → analytic buckets (detailed file):
DETAILED_DOC_BUCKETS = {
    "lt5": {"02"},
    "5_9": {"03"},
    "10_19": {"04", "05"},  # 10-14 + 15-19
    "20_99": {"07", "08", "09", "10", "11", "12", "13"},
    "100_499": {"14", "15", "16", "17", "18"},
    "lt500": {"19"},
    "ge500": {"20", "21", "22", "23", "24", "25", "26"},
    "total": {"01"},
}

# MSA file: ENTRSIZE field DOES match documentation 01–09.
MSA_BUCKETS = {
    "lt5": {"02"},
    "5_9": {"03"},
    "10_19": {"04"},
    "20_99": {"06"},
    "100_499": {"07"},
    "lt500": {"08"},
    "ge500": {"09"},
    "lt20": {"05"},
    "total": {"01"},
}

SUPPRESS_FLAGS = {"S", "D"}


def open_csv(path: Path):
    # Census SUSB txt files are Latin-1 / Windows-1252 (ñ in place names).
    return open(path, newline="", encoding="latin-1")


def parse_emp(row: dict) -> tuple[int | None, str, bool]:
    """Return (employment or None, noise/suppress flag, is_suppressed)."""
    flag = (row.get("EMPLFL_N") or "").strip()
    suppressed = flag in SUPPRESS_FLAGS
    raw = (row.get("EMPL") or "").strip()
    if suppressed or raw == "":
        return None, flag, True
    try:
        return int(raw), flag, False
    except ValueError:
        return None, flag, True


def doc_size_code(entrsizedscr: str) -> str:
    """Leading NN from '19: <500' — the documentation size code, not ENTRSIZE."""
    text = (entrsizedscr or "").strip()
    if ":" in text:
        return text.split(":", 1)[0].strip().zfill(2)
    return text.zfill(2)


def accumulate_detailed(path: Path) -> dict[str, dict]:
    """US + states, all-industry (NAICS '--'), keyed by documentation size code."""
    geos: dict[str, dict] = {}
    with open_csv(path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["NAICS"].strip() != "--":
                continue
            state = row["STATE"].strip()
            code = doc_size_code(row["ENTRSIZEDSCR"])
            name = row["STATEDSCR"].strip()
            emp, flag, suppressed = parse_emp(row)
            if state not in geos:
                geos[state] = {
                    "geo_id": state,
                    "geo_name": name,
                    "geo_type": "us" if state == "00" else "state",
                    "by_code": {},
                    "flags": {},
                }
            geos[state]["by_code"][code] = emp
            geos[state]["flags"][code] = flag
            if suppressed:
                geos[state].setdefault("suppressed_codes", []).append(code)
    return geos


def accumulate_msa(path: Path) -> dict[str, dict]:
    """MSAs and Micro Areas, all-industry (NAICS '--'), standard size codes."""
    geos: dict[str, dict] = {}
    with open_csv(path) as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["NAICS"].strip() != "--":
                continue
            msa = row["MSA"].strip()
            code = row["ENTRSIZE"].strip()
            name = row["MSADSCR"].strip()
            emp, flag, suppressed = parse_emp(row)
            if "Metro Area" in name:
                area_type = "metro"
            elif "Micro Area" in name:
                area_type = "micro"
            else:
                area_type = "other"
            if msa not in geos:
                geos[msa] = {
                    "geo_id": msa,
                    "geo_name": name,
                    "geo_type": area_type,
                    "by_code": {},
                    "flags": {},
                }
            geos[msa]["by_code"][code] = emp
            geos[msa]["flags"][code] = flag
            if suppressed:
                geos[msa].setdefault("suppressed_codes", []).append(code)
    return geos


def sum_codes(by_code: dict, codes: set[str]) -> tuple[int | None, bool]:
    """Sum employment across codes. None if any needed cell missing/suppressed."""
    total = 0
    for c in codes:
        v = by_code.get(c)
        if v is None:
            return None, True
        total += v
    return total, False


def citation_for(geo_type: str) -> dict[str, str]:
    """Full source fields for csv rows (US/state vs MSA files)."""
    if geo_type in ("us", "state"):
        source_file = STATE_FILE_NAME
        source_url = STATE_TABLE_URL
        release_note = STATE_RELEASE_NOTE
    else:
        source_file = MSA_FILE_NAME
        source_url = MSA_TABLE_URL
        release_note = MSA_RELEASE_NOTE
    cite = (
        f"{AGENCY}, {PROGRAM}, 2022 Annual Datasets by Establishment Industry — "
        f"{source_file} (all-industry NAICS=--, enterprise employment size); "
        f"{release_note}; measures {MEASURE}. File: {source_url} "
        f"Landing page: {SOURCE_PAGE_URL}"
    )
    return {
        "origin": "RETRIEVED",
        "agency": AGENCY,
        "program": PROGRAM,
        "source": f"{AGENCY} {PROGRAM} 2022",
        "source_file": source_file,
        "source_url": source_url,
        "source_page_url": SOURCE_PAGE_URL,
        "release_note": release_note,
        "measure": MEASURE,
        "citation": cite,
    }


def build_shares(geo: dict, bucket_map: dict[str, set[str]], scheme: str) -> dict:
    by_code = geo["by_code"]
    out = {
        "geo_id": geo["geo_id"],
        "geo_name": geo["geo_name"],
        "geo_type": geo["geo_type"],
        "year": YEAR,
        "size_scheme": scheme,
        **citation_for(geo["geo_type"]),
    }

    values = {}
    any_suppress = False
    for label, codes in bucket_map.items():
        emp, missing = sum_codes(by_code, codes)
        values[label] = emp
        if missing:
            any_suppress = True
            out[f"{label}_suppressed"] = True

    total = values.get("total")
    lt500 = values.get("lt500")
    ge500 = values.get("ge500")

    # Prefer published 500+; if missing, derive from total − <500 when both present.
    if ge500 is None and total is not None and lt500 is not None:
        ge500 = total - lt500
        values["ge500"] = ge500
        out["ge500_derived"] = True

    # <100 = <5 + 5-9 + 10-19 + 20-99
    parts_lt100 = ["lt5", "5_9", "10_19", "20_99"]
    if all(values.get(k) is not None for k in parts_lt100):
        values["lt100"] = sum(values[k] for k in parts_lt100)
    else:
        values["lt100"] = None
        any_suppress = True

    out["employment_total"] = total
    out["employment_lt5"] = values.get("lt5")
    out["employment_5_9"] = values.get("5_9")
    out["employment_10_19"] = values.get("10_19")
    out["employment_20_99"] = values.get("20_99")
    out["employment_100_499"] = values.get("100_499")
    out["employment_lt100"] = values.get("lt100")
    out["employment_lt500"] = lt500
    out["employment_ge500"] = ge500
    out["any_size_class_suppressed"] = any_suppress

    def pct(num: int | None, den: int | None) -> float | None:
        if num is None or den is None or den == 0:
            return None
        return 100.0 * num / den

    out["share_lt5_pct"] = pct(values.get("lt5"), total)
    out["share_5_9_pct"] = pct(values.get("5_9"), total)
    out["share_10_19_pct"] = pct(values.get("10_19"), total)
    out["share_20_99_pct"] = pct(values.get("20_99"), total)
    out["share_100_499_pct"] = pct(values.get("100_499"), total)
    out["share_lt100_pct"] = pct(values.get("lt100"), total)
    out["share_lt500_pct"] = pct(lt500, total)
    out["share_ge500_pct"] = pct(ge500, total)

    # Integrity: size classes should sum to total (within noise).
    class_keys = ["lt5", "5_9", "10_19", "20_99", "100_499", "ge500"]
    if all(values.get(k) is not None for k in class_keys) and total is not None:
        class_sum = sum(values[k] for k in class_keys)
        out["size_class_sum"] = class_sum
        out["size_class_vs_total_diff"] = class_sum - total
        # Binary split check
        if lt500 is not None and ge500 is not None:
            out["binary_sum"] = lt500 + ge500
            out["binary_vs_total_diff"] = (lt500 + ge500) - total

    return out


def write_csv(path: Path, rows: list[dict], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        for row in rows:
            w.writerow(row)


def round1(x: float | None) -> float | None:
    if x is None:
        return None
    return round(x, 1)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)

    state_geos = accumulate_detailed(STATE_FILE)
    msa_geos = accumulate_msa(MSA_FILE)

    state_rows = [
        build_shares(g, DETAILED_DOC_BUCKETS, "detailed_doc_01_26")
        for g in state_geos.values()
    ]
    msa_rows = [
        build_shares(g, MSA_BUCKETS, "standard_01_09") for g in msa_geos.values()
    ]

    # Sort helpers
    def by_lt500_desc(r):
        s = r.get("share_lt500_pct")
        return (-1e18 if s is None else -s, r["geo_name"])

    us = next(r for r in state_rows if r["geo_id"] == "00")
    states = [r for r in state_rows if r["geo_id"] != "00"]
    states_sorted = sorted(states, key=by_lt500_desc)
    metros = [r for r in msa_rows if r["geo_type"] == "metro"]
    metros_sorted = sorted(
        [r for r in metros if r.get("share_lt500_pct") is not None],
        key=by_lt500_desc,
    )

    fieldnames = [
        "geo_id",
        "geo_name",
        "geo_type",
        "year",
        "size_scheme",
        "origin",
        "agency",
        "program",
        "source",
        "source_file",
        "source_url",
        "source_page_url",
        "release_note",
        "measure",
        "citation",
        "employment_total",
        "employment_lt5",
        "employment_5_9",
        "employment_10_19",
        "employment_20_99",
        "employment_100_499",
        "employment_lt100",
        "employment_lt500",
        "employment_ge500",
        "share_lt5_pct",
        "share_5_9_pct",
        "share_10_19_pct",
        "share_20_99_pct",
        "share_100_499_pct",
        "share_lt100_pct",
        "share_lt500_pct",
        "share_ge500_pct",
        "any_size_class_suppressed",
        "size_class_sum",
        "size_class_vs_total_diff",
        "binary_sum",
        "binary_vs_total_diff",
        "ge500_derived",
    ]

    write_csv(OUT / "us_employment_by_firm_size.csv", [us], fieldnames)
    write_csv(
        OUT / "state_employment_by_firm_size.csv",
        sorted(states, key=lambda r: r["geo_name"]),
        fieldnames,
    )
    write_csv(
        OUT / "msa_employment_by_firm_size.csv",
        sorted(msa_rows, key=lambda r: (r["geo_type"], r["geo_name"])),
        fieldnames,
    )
    write_csv(
        OUT / "msa_metro_only_employment_by_firm_size.csv",
        sorted(metros, key=lambda r: r["geo_name"]),
        fieldnames,
    )

    # Exhibit-ready summary (rounded to 1 decimal for display cross-check)
    high = states_sorted[0]
    low = states_sorted[-1]
    metro_high = metros_sorted[:10]
    metro_low = list(reversed(metros_sorted[-10:]))

    # Metro distribution vs US
    metro_shares = [r["share_lt500_pct"] for r in metros_sorted]
    metro_median = sorted(metro_shares)[len(metro_shares) // 2]

    summary = {
        "year": YEAR,
        "vintage_note": (
            "US, state, and MSA/µSA enterprise-size employment all from SUSB 2022 "
            "(same vintage; MSA revised 2025-07-22). No year mixing."
        ),
        "definition": (
            "SUSB employment is mid-March payroll employment at employer "
            "establishments, classified by enterprise (firm) employment size; "
            "excludes nonemployers, most government, and most of agriculture."
        ),
        "primary_cutoff": "SBA <500 employees (enterprise)",
        "agency": AGENCY,
        "program": PROGRAM,
        "source_page": SOURCE_PAGE_URL,
        "state_table_url": STATE_TABLE_URL,
        "msa_table_url": MSA_TABLE_URL,
        "enterprise_codes_url": ENTERPRISE_CODES_URL,
        "state_release_note": STATE_RELEASE_NOTE,
        "msa_release_note": MSA_RELEASE_NOTE,
        "measure": MEASURE,
        "citation_us_state": citation_for("us")["citation"],
        "citation_msa": citation_for("metro")["citation"],
        "origin": "RETRIEVED",
        "us": {
            "employment_total": us["employment_total"],
            "employment_lt500": us["employment_lt500"],
            "employment_ge500": us["employment_ge500"],
            "share_lt500_pct_full": us["share_lt500_pct"],
            "share_ge500_pct_full": us["share_ge500_pct"],
            "share_lt500_pct_1dp": round1(us["share_lt500_pct"]),
            "share_ge500_pct_1dp": round1(us["share_ge500_pct"]),
            "share_lt100_pct_1dp": round1(us["share_lt100_pct"]),
            "citation": us["citation"],
            "size_class_employment": {
                "lt5": us["employment_lt5"],
                "5_9": us["employment_5_9"],
                "10_19": us["employment_10_19"],
                "20_99": us["employment_20_99"],
                "100_499": us["employment_100_499"],
                "ge500": us["employment_ge500"],
            },
            "size_class_share_pct_1dp": {
                "lt5": round1(us["share_lt5_pct"]),
                "5_9": round1(us["share_5_9_pct"]),
                "10_19": round1(us["share_10_19_pct"]),
                "20_99": round1(us["share_20_99_pct"]),
                "100_499": round1(us["share_100_499_pct"]),
                "ge500": round1(us["share_ge500_pct"]),
            },
            "binary_vs_total_diff": us.get("binary_vs_total_diff"),
            "size_class_vs_total_diff": us.get("size_class_vs_total_diff"),
        },
        "states": {
            "n": len(states),
            "citation": citation_for("state")["citation"],
            "highest_lt500": {
                "name": high["geo_name"],
                "geo_id": high["geo_id"],
                "share_lt500_pct_1dp": round1(high["share_lt500_pct"]),
                "share_lt500_pct_full": high["share_lt500_pct"],
                "employment_total": high["employment_total"],
                "employment_lt500": high["employment_lt500"],
                "citation": high["citation"],
            },
            "lowest_lt500": {
                "name": low["geo_name"],
                "geo_id": low["geo_id"],
                "share_lt500_pct_1dp": round1(low["share_lt500_pct"]),
                "share_lt500_pct_full": low["share_lt500_pct"],
                "employment_total": low["employment_total"],
                "employment_lt500": low["employment_lt500"],
                "citation": low["citation"],
            },
            "range_pp_1dp": round1(
                high["share_lt500_pct"] - low["share_lt500_pct"]
            ),
            "all_sorted_by_lt500_desc": [
                {
                    "geo_id": r["geo_id"],
                    "geo_name": r["geo_name"],
                    "share_lt500_pct_1dp": round1(r["share_lt500_pct"]),
                    "share_lt500_pct_full": r["share_lt500_pct"],
                    "share_ge500_pct_1dp": round1(r["share_ge500_pct"]),
                    "share_lt100_pct_1dp": round1(r["share_lt100_pct"]),
                    "employment_total": r["employment_total"],
                    "employment_lt500": r["employment_lt500"],
                    "employment_ge500": r["employment_ge500"],
                }
                for r in states_sorted
            ],
            "top5": [
                {
                    "geo_name": r["geo_name"],
                    "share_lt500_pct_1dp": round1(r["share_lt500_pct"]),
                    "employment_total": r["employment_total"],
                }
                for r in states_sorted[:5]
            ],
            "bottom5": [
                {
                    "geo_name": r["geo_name"],
                    "share_lt500_pct_1dp": round1(r["share_lt500_pct"]),
                    "employment_total": r["employment_total"],
                }
                for r in states_sorted[-5:]
            ],
        },
        "metros": {
            "n_metro": len(metros),
            "n_metro_with_lt500_share": len(metros_sorted),
            "n_micro_in_file": sum(1 for r in msa_rows if r["geo_type"] == "micro"),
            "us_share_lt500_pct_1dp": round1(us["share_lt500_pct"]),
            "metro_median_lt500_pct_1dp": round1(metro_median),
            "citation": citation_for("metro")["citation"],
            "highest_10": [
                {
                    "geo_id": r["geo_id"],
                    "geo_name": r["geo_name"],
                    "share_lt500_pct_1dp": round1(r["share_lt500_pct"]),
                    "share_lt500_pct_full": r["share_lt500_pct"],
                    "employment_total": r["employment_total"],
                    "employment_lt500": r["employment_lt500"],
                }
                for r in metro_high
            ],
            "lowest_10": [
                {
                    "geo_id": r["geo_id"],
                    "geo_name": r["geo_name"],
                    "share_lt500_pct_1dp": round1(r["share_lt500_pct"]),
                    "share_lt500_pct_full": r["share_lt500_pct"],
                    "employment_total": r["employment_total"],
                    "employment_lt500": r["employment_lt500"],
                }
                for r in metro_low
            ],
        },
        "charter_footprint": {
            "applied": False,
            "reason": (
                "Repo sources state Charter serves 41 states but do not list the "
                "41 states or Spectrum service metros. Footprint filter not applied; "
                "need an official state/metro list to subset."
            ),
        },
        "suppression": {
            "states_with_any_size_class_issue": sum(
                1 for r in states if r.get("any_size_class_suppressed")
            ),
            "metros_missing_lt500_share": len(metros) - len(metros_sorted),
        },
    }

    with open(OUT / "summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    # Assumption / citation register for every headline number
    register_fields = [
        "line_id",
        "geography",
        "metric",
        "value",
        "unit",
        "year",
        "origin",
        "agency",
        "program",
        "source_file",
        "source_url",
        "source_page_url",
        "release_note",
        "measure",
        "citation",
        "notes",
    ]
    st_cite = citation_for("state")
    msa_cite = citation_for("metro")
    register_rows = [
        {
            "line_id": "A1",
            "geography": "United States",
            "metric": "SUSB total employment",
            "value": us["employment_total"],
            "unit": "persons",
            "year": YEAR,
            **{k: us[k] for k in (
                "origin", "agency", "program", "source_file", "source_url",
                "source_page_url", "release_note", "measure", "citation",
            )},
            "notes": "STATE=00 NAICS=-- ENTRSIZEDSCR 01: Total",
        },
        {
            "line_id": "A2",
            "geography": "United States",
            "metric": "Employment at enterprises <500",
            "value": us["employment_lt500"],
            "unit": "persons",
            "year": YEAR,
            **{k: us[k] for k in (
                "origin", "agency", "program", "source_file", "source_url",
                "source_page_url", "release_note", "measure", "citation",
            )},
            "notes": "ENTRSIZEDSCR 19: <500 (SBA cutoff)",
        },
        {
            "line_id": "A3",
            "geography": "United States",
            "metric": "Employment at enterprises 500+",
            "value": us["employment_ge500"],
            "unit": "persons",
            "year": YEAR,
            **{k: us[k] for k in (
                "origin", "agency", "program", "source_file", "source_url",
                "source_page_url", "release_note", "measure", "citation",
            )},
            "notes": "Sum of ENTRSIZEDSCR 20–26; equals A1−A2",
        },
        {
            "line_id": "A4",
            "geography": "United States",
            "metric": "Share employment <500",
            "value": us["share_lt500_pct"],
            "unit": "percent",
            "year": YEAR,
            **{k: us[k] for k in (
                "origin", "agency", "program", "source_file", "source_url",
                "source_page_url", "release_note", "measure", "citation",
            )},
            "notes": "Derived A2/A1; exhibit rounds to 45.9%",
        },
        {
            "line_id": "A5",
            "geography": "United States",
            "metric": "Share employment 500+",
            "value": us["share_ge500_pct"],
            "unit": "percent",
            "year": YEAR,
            **{k: us[k] for k in (
                "origin", "agency", "program", "source_file", "source_url",
                "source_page_url", "release_note", "measure", "citation",
            )},
            "notes": "Derived A3/A1; exhibit rounds to 54.1%",
        },
        {
            "line_id": "A6",
            "geography": "United States",
            "metric": "Share employment <100",
            "value": us["share_lt100_pct"],
            "unit": "percent",
            "year": YEAR,
            **{k: us[k] for k in (
                "origin", "agency", "program", "source_file", "source_url",
                "source_page_url", "release_note", "measure", "citation",
            )},
            "notes": "Sum of <5+5-9+10-19+20-99 over total; exhibit 32.4%",
        },
        {
            "line_id": "A7",
            "geography": high["geo_name"],
            "metric": "Share employment <500 (highest state)",
            "value": high["share_lt500_pct"],
            "unit": "percent",
            "year": YEAR,
            **{k: st_cite[k] for k in (
                "origin", "agency", "program", "source_file", "source_url",
                "source_page_url", "release_note", "measure", "citation",
            )},
            "notes": (
                f"STATE={high['geo_id']}; employment base "
                f"{high['employment_total']}; exhibit 66.3%"
            ),
        },
        {
            "line_id": "A8",
            "geography": low["geo_name"],
            "metric": "Share employment <500 (lowest state)",
            "value": low["share_lt500_pct"],
            "unit": "percent",
            "year": YEAR,
            **{k: st_cite[k] for k in (
                "origin", "agency", "program", "source_file", "source_url",
                "source_page_url", "release_note", "measure", "citation",
            )},
            "notes": (
                f"STATE={low['geo_id']}; employment base "
                f"{low['employment_total']}; exhibit 39.6%"
            ),
        },
        {
            "line_id": "A9",
            "geography": "Metro Areas (n=387)",
            "metric": "Median share employment <500",
            "value": round1(metro_median),
            "unit": "percent",
            "year": YEAR,
            **{k: msa_cite[k] for k in (
                "origin", "agency", "program", "source_file", "source_url",
                "source_page_url", "release_note", "measure", "citation",
            )},
            "notes": (
                "Median of Metropolitan Statistical Area <500 shares; "
                "Micro Areas excluded; exhibit 49.8%"
            ),
        },
    ]
    write_csv(OUT / "assumption_register.csv", register_rows, register_fields)

    # Console report for canvas author
    print("=== SUSB 2022 employment by enterprise size ===")
    print(f"US total employment: {us['employment_total']:,}")
    print(
        f"US <500: {us['employment_lt500']:,}  "
        f"({round1(us['share_lt500_pct'])}%)"
    )
    print(
        f"US 500+: {us['employment_ge500']:,}  "
        f"({round1(us['share_ge500_pct'])}%)"
    )
    print(
        f"US <100: {us['employment_lt100']:,}  "
        f"({round1(us['share_lt100_pct'])}%)"
    )
    print(
        f"Size-class sum vs total diff: {us.get('size_class_vs_total_diff')} "
        f"(noise/rounding expected small)"
    )
    print(
        f"State range <500 share: {high['geo_name']} "
        f"{round1(high['share_lt500_pct'])}% "
        f"(emp {high['employment_total']:,}) -> {low['geo_name']} "
        f"{round1(low['share_lt500_pct'])}% "
        f"(emp {low['employment_total']:,})"
    )
    print(f"Metros with share: {len(metros_sorted)} / {len(metros)}")
    print(f"Metro median <500 share: {round1(metro_median)}%")
    print(f"Wrote: {OUT}")


if __name__ == "__main__":
    main()
