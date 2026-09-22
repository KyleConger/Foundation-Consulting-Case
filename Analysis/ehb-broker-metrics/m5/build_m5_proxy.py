"""
M5 validation support — NOT a serviceable-home rate.

M5 (from Decisions/EH&B/Brokerage Metrics.xlsx, Core metrics):
  Numerator: enrolled (or broker-covered) employees whose residential
  address passes a Spectrum residential serviceability check.
  Denominator: enrolled / covered employees in the pilot book who supply
  a home address.
  Unit: percent. Hard fail for out-of-footprint homes.

This script does not compute M5. There is no employer roster and no
address-to-BSL match in the repo.

What it does compute, labeled ESTIMATED and biased:
  Share of SUSB 2022 payroll employment that sits in jurisdictions where
  Charter files any residential fixed-broadband availability (FCC BDC D25).

That share is a crude ceiling on *workplace geography*, not home
serviceability. It is not M5. Do not multiply it by state location share
and call the product an employee-level rate — that conversion is refused.

Inputs (already in repo; not re-downloaded):
  Analysis/cable-share-small-firm/out/chtr_vs_cmcsa_state_leads.csv
  Analysis/small-large-employment/out/state_employment_by_firm_size.csv
  Analysis/small-large-employment/out/us_employment_by_firm_size.csv
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[2]
OUT = ROOT / "out"
OUT.mkdir(parents=True, exist_ok=True)

LEADS = REPO / "Analysis" / "cable-share-small-firm" / "out" / "chtr_vs_cmcsa_state_leads.csv"
STATE_EMP = (
    REPO / "Analysis" / "small-large-employment" / "out" / "state_employment_by_firm_size.csv"
)
US_EMP = REPO / "Analysis" / "small-large-employment" / "out" / "us_employment_by_firm_size.csv"


def _truthy(v: str) -> bool:
    return str(v).strip().lower() in {"true", "1", "yes"}


def _fips(v: str) -> str:
    return str(v).strip().zfill(2)


def load_leads() -> dict[str, dict]:
    out: dict[str, dict] = {}
    with LEADS.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            fips = _fips(row["state_fips"])
            pct_raw = row["charter_res_st_pct"].strip()
            units_raw = row["charter_est_units"].strip()
            out[fips] = {
                "state": row["state"],
                "abbr": row["abbr"],
                "charter_present": _truthy(row["charter_present"]),
                "charter_res_st_pct": float(pct_raw) if pct_raw else None,
                "charter_est_units": int(units_raw) if units_raw else 0,
                "total_residential_units": int(row["total_residential_units"]),
            }
    return out


def load_state_emp() -> dict[str, int]:
    out: dict[str, int] = {}
    with STATE_EMP.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["geo_type"] != "state":
                continue
            out[_fips(row["geo_id"])] = int(row["employment_total"])
    return out


def load_us_emp() -> int:
    with US_EMP.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["geo_type"] == "us":
                return int(row["employment_total"])
    raise SystemExit("US employment row missing")


def main() -> None:
    leads = load_leads()
    emp = load_state_emp()
    us_emp = load_us_emp()

    fips_51 = sorted(set(leads) | set(emp))
    missing_leads = sorted(set(emp) - set(leads))
    missing_emp = sorted(set(leads) - set(emp))
    if missing_leads or missing_emp:
        raise SystemExit(f"FIPS mismatch leads={missing_leads} emp={missing_emp}")

    rows = []
    present_emp = 0
    absent_emp = 0
    present_n = 0
    present_units = 0
    fabric_units_present = 0
    fabric_units_all = 0

    for fips in fips_51:
        L = leads[fips]
        e = emp[fips]
        present = bool(L["charter_present"])
        if present:
            present_n += 1
            present_emp += e
            present_units += L["charter_est_units"]
            fabric_units_present += L["total_residential_units"]
        else:
            absent_emp += e
        fabric_units_all += L["total_residential_units"]
        rows.append(
            {
                "state_fips": fips,
                "state": L["state"],
                "abbr": L["abbr"],
                "charter_present": present,
                "charter_res_st_pct": L["charter_res_st_pct"],
                "charter_est_units": L["charter_est_units"],
                "total_residential_units": L["total_residential_units"],
                "susb_employment_2022": e,
                "origin_presence": "RETRIEVED",
                "origin_employment": "RETRIEVED",
            }
        )

    sum_states = present_emp + absent_emp
    if sum_states != us_emp:
        raise SystemExit(f"State employment {sum_states} != US {us_emp}")

    share_emp_present = present_emp / us_emp
    share_emp_absent = absent_emp / us_emp

    # Intra-state plant share among the 42 present jurisdictions only.
    # RETRIEVED plant metric. Not an employee rate. Not multiplied by employment.
    pcts = [
        r["charter_res_st_pct"]
        for r in rows
        if r["charter_present"] and r["charter_res_st_pct"] is not None
    ]
    pcts_sorted = sorted(pcts)
    mid = len(pcts_sorted) // 2
    median_pct = (
        (pcts_sorted[mid - 1] + pcts_sorted[mid]) / 2
        if len(pcts_sorted) % 2 == 0
        else pcts_sorted[mid]
    )

    national_loc_share_in_present = present_units / fabric_units_present
    national_loc_share_vs_us_fabric = present_units / fabric_units_all

    # The conversion we refuse: employment-weighted state location share.
    # Computed only so the register can say the number exists and is not M5.
    weighted_num = 0.0
    for r in rows:
        if r["charter_present"] and r["charter_res_st_pct"] is not None:
            weighted_num += r["susb_employment_2022"] * r["charter_res_st_pct"]
    refused_emp_weighted_loc = weighted_num / us_emp

    rows.sort(key=lambda r: (-int(r["charter_present"]), r["state"]))

    present_path = OUT / "charter_present_employment.csv"
    with present_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(
            f,
            fieldnames=[
                "state_fips",
                "state",
                "abbr",
                "charter_present",
                "charter_res_st_pct",
                "charter_est_units",
                "total_residential_units",
                "susb_employment_2022",
                "origin_presence",
                "origin_employment",
            ],
        )
        w.writeheader()
        for r in rows:
            out_row = dict(r)
            if out_row["charter_res_st_pct"] is not None:
                out_row["charter_res_st_pct"] = f"{out_row['charter_res_st_pct']:.6f}"
            w.writerow(out_row)

    assumptions = [
        {
            "line_id": "A1",
            "item": "M5 definition",
            "value": "enrolled/covered employees whose home address passes Spectrum residential serviceability ÷ enrolled/covered employees who supply a home address",
            "origin": "RETRIEVED",
            "source": "Decisions/EH&B/Brokerage Metrics.xlsx · Core metrics · M5; chtr-ehb-broker-channel-core-metrics.canvas.tsx",
        },
        {
            "line_id": "A2",
            "item": "M5 number for any broker book",
            "value": "none — no roster, no address match",
            "origin": "BLOCKING",
            "source": "repo contains no employer/broker home-address file",
        },
        {
            "line_id": "B1",
            "item": "Charter-present jurisdictions (50 states + DC)",
            "value": present_n,
            "origin": "RETRIEVED",
            "source": "FCC BDC D25 as of 2025-12-31, revision 15 Sep 2026; Analysis/cable-share-small-firm/out/chtr_vs_cmcsa_state_leads.csv; charter_present = any residential fixed-broadband filing",
        },
        {
            "line_id": "B2",
            "item": "Charter-absent jurisdictions",
            "value": 51 - present_n,
            "origin": "RETRIEVED",
            "source": "same BDC file; absent = AK, AR, DC, DE, IA, ND, OK, SD, UT",
        },
        {
            "line_id": "C1",
            "item": "US SUSB 2022 payroll employment",
            "value": us_emp,
            "origin": "RETRIEVED",
            "source": "U.S. Census Bureau SUSB 2022; Analysis/small-large-employment/out/us_employment_by_firm_size.csv",
        },
        {
            "line_id": "C2",
            "item": "SUSB employment in Charter-present jurisdictions",
            "value": present_emp,
            "origin": "DERIVED",
            "source": "C1 geography joined to B1; workplace establishment employment, not home address",
        },
        {
            "line_id": "C3",
            "item": "SUSB employment in Charter-absent jurisdictions",
            "value": absent_emp,
            "origin": "DERIVED",
            "source": "C1 − C2",
        },
        {
            "line_id": "C4",
            "item": "Share of US SUSB employment in Charter-present jurisdictions",
            "value": round(share_emp_present, 6),
            "origin": "ESTIMATED as crude ceiling — not M5",
            "source": "C2 ÷ C1. Bias: workplace not home; any-presence not plant coverage; broker book ≠ national employment; intra-state plant often far below 100%",
        },
        {
            "line_id": "D1",
            "item": "Charter estimated residential units in present jurisdictions",
            "value": present_units,
            "origin": "RETRIEVED / DERIVED in BDC build",
            "source": "res_st_pct × state residential fabric; Analysis/cable-share-small-firm",
        },
        {
            "line_id": "D2",
            "item": "Residential fabric units in Charter-present jurisdictions",
            "value": fabric_units_present,
            "origin": "RETRIEVED",
            "source": "FCC BDC state residential fabric (total_units)",
        },
        {
            "line_id": "D3",
            "item": "Charter location share of fabric inside the 42 present jurisdictions",
            "value": round(national_loc_share_in_present, 6),
            "origin": "DERIVED — plant metric, not M5",
            "source": "D1 ÷ D2. Homes Charter can serve among BSLs in states where it files, not employee homes.",
        },
        {
            "line_id": "D4",
            "item": "Charter location share of all 51-jurisdiction residential fabric",
            "value": round(national_loc_share_vs_us_fabric, 6),
            "origin": "DERIVED — plant metric, not M5",
            "source": "D1 ÷ sum of 51-jurisdiction fabric. Still not an employee-home rate.",
        },
        {
            "line_id": "X1",
            "item": "Employment-weighted state location share (REFUSED as M5)",
            "value": round(refused_emp_weighted_loc, 6),
            "origin": "REFUSED — do not cite as serviceable-home share",
            "source": "Σ (state employment × charter_res_st_pct) ÷ US employment. Shares two wrong substitutions: workplace for home, and random BSL for employee address. Computed only to document the conversion we will not ship as M5.",
        },
        {
            "line_id": "X2",
            "item": "What this file is not",
            "value": "Not M5. Not TAM. Not subscriber share. Not a national serviceable-employee percent.",
            "origin": "n/a",
            "source": "n/a",
        },
    ]

    with (OUT / "assumption_register.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["line_id", "item", "value", "origin", "source"])
        w.writeheader()
        w.writerows(assumptions)

    absent_names = [r["state"] for r in rows if not r["charter_present"]]
    present_sorted_pct = sorted(
        [r for r in rows if r["charter_present"] and r["charter_res_st_pct"] is not None],
        key=lambda r: r["charter_res_st_pct"],
        reverse=True,
    )

    summary = {
        "metric": "M5 Serviceable-home share of enrolled employees",
        "m5_verdict_on_metric": "valid — footprint hard gate for corporate → consumer internet",
        "m5_verdict_on_number": "cannot claim — no roster × BSL/addressability match",
        "m5_value": None,
        "blocking_input": "employer or broker roster of enrolled/eligible employees with home addresses, consented, geocoded, matched to Charter residential serviceability / FCC BSL",
        "charter_present_jurisdictions": present_n,
        "charter_absent_jurisdictions": 51 - present_n,
        "absent_names": absent_names,
        "us_susb_employment_2022": us_emp,
        "employment_in_present": present_emp,
        "employment_in_absent": absent_emp,
        "share_employment_in_present": share_emp_present,
        "share_employment_in_present_rounded_pct": round(share_emp_present * 100, 1),
        "share_employment_in_present_label": "ESTIMATED crude ceiling — workplace employment in states with any Charter filing; not serviceable-home share",
        "charter_est_residential_units_in_present": present_units,
        "fabric_units_in_present": fabric_units_present,
        "fabric_units_51": fabric_units_all,
        "charter_location_share_of_present_fabric": national_loc_share_in_present,
        "charter_location_share_of_51_fabric": national_loc_share_vs_us_fabric,
        "present_state_location_share_min": min(pcts) if pcts else None,
        "present_state_location_share_max": max(pcts) if pcts else None,
        "present_state_location_share_median": median_pct,
        "highest_present": {
            "state": present_sorted_pct[0]["state"],
            "pct": present_sorted_pct[0]["charter_res_st_pct"],
        },
        "lowest_present": {
            "state": present_sorted_pct[-1]["state"],
            "pct": present_sorted_pct[-1]["charter_res_st_pct"],
        },
        "refused_employment_weighted_location_share": refused_emp_weighted_loc,
        "refused_note": "X1 is not M5 and must not be quoted as a serviceable-employee percent.",
        "sources": {
            "definition": "Decisions/EH&B/Brokerage Metrics.xlsx Core metrics M5",
            "bdc": "Analysis/cable-share-small-firm/out/chtr_vs_cmcsa_state_leads.csv",
            "susb": "Analysis/small-large-employment/out/state_employment_by_firm_size.csv",
            "bdc_vintage": "December 31, 2025 (D25), revision 15 Sep 2026",
            "susb_vintage": "2022 mid-March payroll employment",
        },
        "arithmetic_checks": {
            "present_n_plus_absent_n": present_n + (51 - present_n),
            "present_emp_plus_absent_emp": present_emp + absent_emp,
            "equals_us_emp": present_emp + absent_emp == us_emp,
            "c4_recomputed": present_emp / us_emp,
        },
    }

    with (OUT / "summary.json").open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
