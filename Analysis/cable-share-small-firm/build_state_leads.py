"""
Charter vs Comcast by state: who reports more residential fixed-broadband
locations in the FCC Broadband Data Collection.

Metric: FCC BDC provider `res_st_pct` (share of residential units in
broadband-serviceable locations in the geography where the holding company
reports residential fixed broadband availability), vintage D25
(as of 2025-12-31, file revision 15 Sep 2026).

This is availability / locations served. It is NOT subscriber share.

Holding companies (FCC Provider List; affiliates not rolled in):
  Charter Communications  provider_id 130235  FRN 0025646373
  Comcast Corporation     provider_id 130317  FRN 0003768165

Do not treat Sonic Spectrum, Inc. or Red Spectrum Communications LLC as Charter.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RAW = ROOT / "raw"
OUT = ROOT / "out"
OUT.mkdir(parents=True, exist_ok=True)

PROVIDER_LIST = RAW / "provider_list" / "bdc_us_provider_list_D25_15sep2026.csv"
PROVIDER_GEO = (
    RAW / "provider_summary_geo" / "bdc_us_provider_summary_by_geography_D25_15sep2026.csv"
)
PROVIDER_FIXED = (
    RAW
    / "provider_summary_fixed"
    / "bdc_us_fixed_broadband_provider_summary_D25_15sep2026.csv"
)
GEO_SUMMARY = (
    RAW / "geo_summary" / "bdc_us_fixed_broadband_summary_by_geography_D25_15sep2026.csv"
)

CHARTER_ID = "130235"
COMCAST_ID = "130317"
CHARTER_HOCO = "Charter Communications"
COMCAST_HOCO = "Comcast Corporation"
CHARTER_FRN = "0025646373"
COMCAST_FRN = "0003768165"

# 50 states + DC. Territories excluded from the 51-row comparison.
STATES_51 = {
    "01": "Alabama",
    "02": "Alaska",
    "04": "Arizona",
    "05": "Arkansas",
    "06": "California",
    "08": "Colorado",
    "09": "Connecticut",
    "10": "Delaware",
    "11": "District of Columbia",
    "12": "Florida",
    "13": "Georgia",
    "15": "Hawaii",
    "16": "Idaho",
    "17": "Illinois",
    "18": "Indiana",
    "19": "Iowa",
    "20": "Kansas",
    "21": "Kentucky",
    "22": "Louisiana",
    "23": "Maine",
    "24": "Maryland",
    "25": "Massachusetts",
    "26": "Michigan",
    "27": "Minnesota",
    "28": "Mississippi",
    "29": "Missouri",
    "30": "Montana",
    "31": "Nebraska",
    "32": "Nevada",
    "33": "New Hampshire",
    "34": "New Jersey",
    "35": "New Mexico",
    "36": "New York",
    "37": "North Carolina",
    "38": "North Dakota",
    "39": "Ohio",
    "40": "Oklahoma",
    "41": "Oregon",
    "42": "Pennsylvania",
    "44": "Rhode Island",
    "45": "South Carolina",
    "46": "South Dakota",
    "47": "Tennessee",
    "48": "Texas",
    "49": "Utah",
    "50": "Vermont",
    "51": "Virginia",
    "53": "Washington",
    "54": "West Virginia",
    "55": "Wisconsin",
    "56": "Wyoming",
}

ABBR = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "District of Columbia": "DC",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
}

SOURCE_URL = "https://broadbandmap.fcc.gov/data-download"
FILING = "December 31, 2025 (D25)"
REVISION = "15 Sep 2026"
FILE_GEO = "bdc_us_provider_summary_by_geography_D25_15sep2026.csv"
FILE_UNITS = "bdc_us_fixed_broadband_summary_by_geography_D25_15sep2026.csv"
FILE_LIST = "bdc_us_provider_list_D25_15sep2026.csv"
FILE_NATL = "bdc_us_fixed_broadband_provider_summary_D25_15sep2026.csv"


def fnum(x: str) -> float:
    return float(x) if x not in (None, "") else 0.0


def verify_holding_companies() -> dict:
    found = {}
    with PROVIDER_LIST.open(encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            if row["provider_id"] in (CHARTER_ID, COMCAST_ID):
                found[row["provider_id"]] = row
    assert found[CHARTER_ID]["holding_company"] == CHARTER_HOCO
    assert found[CHARTER_ID]["frn"] == CHARTER_FRN
    assert found[COMCAST_ID]["holding_company"] == COMCAST_HOCO
    assert found[COMCAST_ID]["frn"] == COMCAST_FRN
    return found


def national_location_counts() -> dict:
    out = {
        CHARTER_HOCO: {"cable_loc_res": 0, "fiber_loc_res": 0, "cable_unit_res": 0, "fiber_unit_res": 0},
        COMCAST_HOCO: {"cable_loc_res": 0, "fiber_loc_res": 0, "cable_unit_res": 0, "fiber_unit_res": 0},
    }
    with PROVIDER_FIXED.open(encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            if row["provider_id"] not in (CHARTER_ID, COMCAST_ID):
                continue
            hoco = row["holding_company"]
            loc = int(row["location_count_res"])
            units = int(row["unit_count_res"])
            tech = row["technology_code_desc"]
            if tech == "Cable":
                out[hoco]["cable_loc_res"] = loc
                out[hoco]["cable_unit_res"] = units
            elif tech == "Fiber to the Premises":
                out[hoco]["fiber_loc_res"] = loc
                out[hoco]["fiber_unit_res"] = units
    return out


def state_total_units() -> dict[str, int]:
    """Residential fabric units by state (Total / Any Technology / biz_res=R)."""
    units: dict[str, int] = {}
    with GEO_SUMMARY.open(encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            if (
                row["geography_type"] == "State"
                and row["area_data_type"] == "Total"
                and row["technology"] == "Any Technology"
                and row["biz_res"] == "R"
                and row["geography_id"] in STATES_51
            ):
                units[row["geography_id"]] = int(row["total_units"])
    missing = set(STATES_51) - set(units)
    if missing:
        raise SystemExit(f"Missing state unit totals: {sorted(missing)}")
    return units


def provider_state_pct() -> dict[str, dict[str, float]]:
    """res_st_pct by provider_id by state FIPS. Missing => provider absent."""
    pct: dict[str, dict[str, float]] = {CHARTER_ID: {}, COMCAST_ID: {}}
    with PROVIDER_GEO.open(encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            if (
                row["geography_type"] == "State"
                and row["data_type"] == "Fixed Broadband"
                and row["provider_id"] in (CHARTER_ID, COMCAST_ID)
                and row["geography_id"] in STATES_51
            ):
                pct[row["provider_id"]][row["geography_id"]] = fnum(row["res_st_pct"])
    return pct


def present_pct(pct: float | None) -> float | None:
    """A 0.0000 filing is not a footprint. Treat as absent."""
    if pct is None or pct == 0.0:
        return None
    return pct


def classify(ch_pct: float | None, cm_pct: float | None) -> str:
    ch_present = ch_pct is not None
    cm_present = cm_pct is not None
    if not ch_present and not cm_present:
        return "neither present"
    if ch_present and not cm_present:
        return "Charter"
    if cm_present and not ch_present:
        return "Comcast"
    # Both present. Beating = strictly larger on res_st_pct.
    if ch_pct > cm_pct:
        return "Charter"
    if cm_pct > ch_pct:
        return "Comcast"
    return "tie"


def fmt_pct(x: float | None) -> str:
    if x is None:
        return ""
    return f"{x * 100:.1f}%"


def fmt_int(n: int | None) -> str:
    if n is None:
        return ""
    return f"{n:,}"


def main() -> None:
    verify_holding_companies()
    natl = national_location_counts()
    units = state_total_units()
    pct = provider_state_pct()

    rows = []
    for fips, name in STATES_51.items():
        ch_raw = pct[CHARTER_ID].get(fips)
        cm_raw = pct[COMCAST_ID].get(fips)
        ch_pct = present_pct(ch_raw)
        cm_pct = present_pct(cm_raw)
        total = units[fips]
        ch_units = None if ch_pct is None else round(ch_pct * total)
        cm_units = None if cm_pct is None else round(cm_pct * total)
        leader = classify(ch_pct, cm_pct)
        ch_u = 0 if ch_units is None else ch_units
        cm_u = 0 if cm_units is None else cm_units
        margin_units = ch_u - cm_u
        ch_p = 0.0 if ch_pct is None else ch_pct
        cm_p = 0.0 if cm_pct is None else cm_pct
        margin_pp = (ch_p - cm_p) * 100
        rows.append(
            {
                "state_fips": fips,
                "state": name,
                "abbr": ABBR[name],
                "total_residential_units": total,
                "charter_res_st_pct": ch_pct,
                "comcast_res_st_pct": cm_pct,
                "charter_est_units": ch_units,
                "comcast_est_units": cm_units,
                "charter_present": ch_pct is not None,
                "comcast_present": cm_pct is not None,
                "leader": leader,
                "margin_units_charter_minus_comcast": margin_units,
                "margin_pp_charter_minus_comcast": round(margin_pp, 2),
            }
        )

    rows.sort(key=lambda r: (-r["margin_units_charter_minus_comcast"], r["state"]))

    n_ch = sum(1 for r in rows if r["leader"] == "Charter")
    n_cm = sum(1 for r in rows if r["leader"] == "Comcast")
    n_tie = sum(1 for r in rows if r["leader"] == "tie")
    n_neither = sum(1 for r in rows if r["leader"] == "neither present")
    assert n_ch + n_cm + n_tie + n_neither == 51

    unclassified = [r["state"] for r in rows if r["leader"] in ("tie", "neither present")]
    ch_lead = [r for r in rows if r["leader"] == "Charter"]
    cm_lead = [r for r in rows if r["leader"] == "Comcast"]
    # Comcast leads sorted by size of Comcast's unit lead (most negative margin first).
    cm_lead_by_size = sorted(cm_lead, key=lambda r: r["margin_units_charter_minus_comcast"])

    top5_ch = ch_lead[:5]
    top5_cm = cm_lead_by_size[:5]

    # Chart subset: 10 largest Charter unit leads + 10 largest Comcast unit leads.
    chart_ch = ch_lead[:10]
    chart_cm = cm_lead_by_size[:10]
    chart_rows = chart_ch + list(reversed(chart_cm))  # Charter leads on top, Comcast on bottom

    csv_path = OUT / "chtr_vs_cmcsa_state_leads.csv"
    fieldnames = [
        "state_fips",
        "state",
        "abbr",
        "total_residential_units",
        "charter_res_st_pct",
        "comcast_res_st_pct",
        "charter_est_units",
        "comcast_est_units",
        "charter_present",
        "comcast_present",
        "leader",
        "margin_units_charter_minus_comcast",
        "margin_pp_charter_minus_comcast",
        "origin_pct",
        "origin_units",
        "origin_est_units",
        "notes",
    ]
    with csv_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow(
                {
                    **{k: r[k] for k in fieldnames if k in r},
                    "charter_res_st_pct": "" if r["charter_res_st_pct"] is None else f"{r['charter_res_st_pct']:.6f}",
                    "comcast_res_st_pct": "" if r["comcast_res_st_pct"] is None else f"{r['comcast_res_st_pct']:.6f}",
                    "charter_est_units": "" if r["charter_est_units"] is None else r["charter_est_units"],
                    "comcast_est_units": "" if r["comcast_est_units"] is None else r["comcast_est_units"],
                    "origin_pct": "RETRIEVED",
                    "origin_units": "RETRIEVED",
                    "origin_est_units": "DERIVED = res_st_pct × total_residential_units",
                    "notes": (
                        "Missing provider row = not in FCC state summary (treated as absent). "
                        "Beating = strictly larger res_st_pct. Availability, not subscribers."
                    ),
                }
            )

    assumptions = [
        {
            "line_id": "A1",
            "item": "BDC vintage",
            "value": FILING,
            "origin": "RETRIEVED",
            "source": f"FCC National Broadband Map data download; process filing December 31, 2025; file revision {REVISION}",
            "url": SOURCE_URL,
        },
        {
            "line_id": "A2",
            "item": "Charter holding company / FRN / provider_id",
            "value": f"{CHARTER_HOCO} / FRN {CHARTER_FRN} / provider_id {CHARTER_ID}",
            "origin": "RETRIEVED",
            "source": FILE_LIST,
            "url": SOURCE_URL,
        },
        {
            "line_id": "A3",
            "item": "Comcast holding company / FRN / provider_id",
            "value": f"{COMCAST_HOCO} / FRN {COMCAST_FRN} / provider_id {COMCAST_ID}",
            "origin": "RETRIEVED",
            "source": FILE_LIST,
            "url": SOURCE_URL,
        },
        {
            "line_id": "A4",
            "item": "Charter national residential cable locations",
            "value": natl[CHARTER_HOCO]["cable_loc_res"],
            "origin": "RETRIEVED",
            "source": FILE_NATL,
            "url": SOURCE_URL,
        },
        {
            "line_id": "A5",
            "item": "Comcast national residential cable locations",
            "value": natl[COMCAST_HOCO]["cable_loc_res"],
            "origin": "RETRIEVED",
            "source": FILE_NATL,
            "url": SOURCE_URL,
        },
        {
            "line_id": "B1",
            "item": "State leader rule",
            "value": "Strictly larger res_st_pct on Fixed Broadband; missing row = absent; equal pct = tie",
            "origin": "RETRIEVED metric + stated rule",
            "source": FILE_GEO,
            "url": SOURCE_URL,
        },
        {
            "line_id": "B2",
            "item": "Estimated residential units served",
            "value": "round(res_st_pct × total_residential_units); same-state ranking identical to pct ranking",
            "origin": "DERIVED from two RETRIEVED inputs",
            "source": f"{FILE_GEO} × {FILE_UNITS}",
            "url": SOURCE_URL,
        },
        {
            "line_id": "X1",
            "item": "What this is not",
            "value": "Not subscriber share. Not Form 477 subscriptions. Not SUSB employment. National 49/51 mix not allocated to states.",
            "origin": "n/a",
            "source": "n/a",
            "url": "",
        },
    ]
    with (OUT / "assumption_register.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["line_id", "item", "value", "origin", "source", "url"])
        w.writeheader()
        w.writerows(assumptions)

    def slim(r: dict, extras: bool = True) -> dict:
        d = {
            "abbr": r["abbr"],
            "state": r["state"],
            "leader": r["leader"],
            "charter_pct": None if r["charter_res_st_pct"] is None else round(r["charter_res_st_pct"] * 100, 1),
            "comcast_pct": None if r["comcast_res_st_pct"] is None else round(r["comcast_res_st_pct"] * 100, 1),
            "charter_units": r["charter_est_units"],
            "comcast_units": r["comcast_est_units"],
            "margin_units": r["margin_units_charter_minus_comcast"],
            "margin_pp": r["margin_pp_charter_minus_comcast"],
            "total_units": r["total_residential_units"],
            "charter_present": r["charter_present"],
            "comcast_present": r["comcast_present"],
        }
        return d

    # Chart: margin in millions of estimated residential units; two non-negative series.
    chart_categories = [r["abbr"] for r in chart_rows]
    chart_ch_m = [
        round(r["margin_units_charter_minus_comcast"] / 1_000_000, 2)
        if r["leader"] == "Charter"
        else 0.0
        for r in chart_rows
    ]
    chart_cm_m = [
        round(abs(r["margin_units_charter_minus_comcast"]) / 1_000_000, 2)
        if r["leader"] == "Comcast"
        else 0.0
        for r in chart_rows
    ]

    summary = {
        "metric": (
            "Share of residential units at FCC Broadband Serviceable Locations "
            "where the holding company reports residential fixed broadband availability "
            "(res_st_pct). Estimated units = res_st_pct × state residential fabric units."
        ),
        "vintage": FILING,
        "revision": REVISION,
        "agency": "Federal Communications Commission",
        "program": "Broadband Data Collection / National Broadband Map",
        "files": [FILE_LIST, FILE_GEO, FILE_UNITS, FILE_NATL],
        "url": SOURCE_URL,
        "charter_id": {"holding_company": CHARTER_HOCO, "provider_id": CHARTER_ID, "frn": CHARTER_FRN, "brand": "Spectrum"},
        "comcast_id": {"holding_company": COMCAST_HOCO, "provider_id": COMCAST_ID, "frn": COMCAST_FRN, "brand": "Xfinity"},
        "national_cable_locations_res": {
            "charter": natl[CHARTER_HOCO]["cable_loc_res"],
            "comcast": natl[COMCAST_HOCO]["cable_loc_res"],
        },
        "n_charter_leads": n_ch,
        "n_comcast_leads": n_cm,
        "n_tie": n_tie,
        "n_neither": n_neither,
        "unclassified_states": unclassified,
        "top5_charter": [slim(r) for r in top5_ch],
        "top5_comcast": [slim(r) for r in top5_cm],
        "chart": {
            "categories": chart_categories,
            "charter_lead_m_units": chart_ch_m,
            "comcast_lead_m_units": chart_cm_m,
            "rows": [slim(r) for r in chart_rows],
        },
        "all_states": [slim(r) for r in rows],
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print("=== HEADLINE ===")
    print(f"Charter leads Comcast in {n_ch} states+DC; Comcast leads in {n_cm}; neither {n_neither}; tie {n_tie}")
    print()
    print("Top 5 Charter unit leads:")
    for r in top5_ch:
        print(
            f"  {r['abbr']:3}  CH {fmt_pct(r['charter_res_st_pct']):>6} ({fmt_int(r['charter_est_units']):>12} u)  "
            f"CM {fmt_pct(r['comcast_res_st_pct']):>6} ({fmt_int(r['comcast_est_units']):>12} u)  "
            f"margin {r['margin_units_charter_minus_comcast']:+,}  of {r['total_residential_units']:,} fabric units"
        )
    print("Top 5 Comcast unit leads:")
    for r in top5_cm:
        print(
            f"  {r['abbr']:3}  CH {fmt_pct(r['charter_res_st_pct']):>6} ({fmt_int(r['charter_est_units']):>12} u)  "
            f"CM {fmt_pct(r['comcast_res_st_pct']):>6} ({fmt_int(r['comcast_est_units']):>12} u)  "
            f"margin {r['margin_units_charter_minus_comcast']:+,}  of {r['total_residential_units']:,} fabric units"
        )
    print()
    print("Neither / tie:", unclassified)
    print("Charter present states:", sum(1 for r in rows if r["charter_present"]))
    print("Comcast present states:", sum(1 for r in rows if r["comcast_present"]))
    print("National cable locations CH/CM:", natl[CHARTER_HOCO]["cable_loc_res"], natl[COMCAST_HOCO]["cable_loc_res"])
    print("Wrote", csv_path)


if __name__ == "__main__":
    main()
