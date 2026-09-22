"""
Build work-from-home rates for the Charter / Spectrum case.

Primary metric (state + US): ACS 2024 1-year B08301 — share of workers 16+
whose means of transportation to work was "Worked from home" (usually WFH).

Seniority proxies: BLS ATUS 2024 Tables 6–7 — share of employed persons who
worked at home on an average day among those who worked that day (any time at
home; not restricted to usual workplace = home).

Firm size: Census ABS Characteristics of Businesses ABSCB2023.AB2300CSCB04 —
share of employer firms that had employees who worked from home (QDESC B28 /
BUSCHAR EWA), by EMPSZFI including <500 and 500+.

Does not impute. Suppressed cells stay missing. Every output row carries a
citation. Recomputes all percentages in code.
"""
from __future__ import annotations

import csv
import json
import pathlib
import zipfile
from typing import Any

ROOT = pathlib.Path(__file__).resolve().parent
RAW = ROOT / "raw"
OUT = ROOT / "out"
OUT.mkdir(parents=True, exist_ok=True)

# --- Citation blocks (URLs actually used) ------------------------------------

CITE_ACS = {
    "agency": "U.S. Census Bureau",
    "program": "American Community Survey (ACS) 1-Year Estimates Detailed Tables",
    "table": "B08301 Means of Transportation to Work",
    "year": "2024",
    "variable_or_question": (
        "B08301_021E Worked from home / B08301_001E Total; "
        "universe = Workers 16 years and over; "
        "usually worked from home as means of transportation to work "
        "(journey-to-work)"
    ),
    "url": (
        "https://api.censusreporter.org/1.0/data/show/latest"
        "?table_ids=B08301&geo_ids=040%7C01000US,01000US"
    ),
    "url_secondary": "https://data.census.gov/table/ACSDT1Y2024.B08301",
    "funded_by": "U.S. Census Bureau (federal statistical agency)",
    "origin": "RETRIEVED",
    "confidence": "high",
    "notes": (
        "Pulled via Census Reporter API wrapping ACS 2024 1-year release "
        "(release id acs2024_1yr). Direct api.census.gov calls required a key; "
        "counts match ACS table B08301."
    ),
}

CITE_ATUS = {
    "agency": "U.S. Bureau of Labor Statistics",
    "program": "American Time Use Survey (ATUS)",
    "table": "Tables 6 and 7, 2024 annual averages (news release)",
    "year": "2024",
    "variable_or_question": (
        "Employed persons who worked at home on an average day as percent of "
        "employed persons who worked on an average day; "
        "'Working at home' includes any time persons did work at home and is "
        "not restricted to persons whose usual workplace is their home. "
        "Persons 15+. Table 6: education / full- vs part-time. "
        "Table 7: occupation / usual weekly earnings quartiles "
        "(full-time wage and salary, single jobholders)."
    ),
    "url": "https://www.bls.gov/news.release/archives/atus_06262025.htm",
    "url_secondary": "https://www.bls.gov/news.release/archives/atus_06262025.pdf",
    "funded_by": "U.S. Bureau of Labor Statistics (federal statistical agency)",
    "origin": "RETRIEVED",
    "confidence": "high",
    "notes": (
        "Different metric than ACS usually-WFH. Do not mix with ACS state rates "
        "in one comparison. Job level (VP vs IC) is not published; occupation "
        "and earnings quartiles are seniority proxies only."
    ),
}

CITE_ABS = {
    "agency": "U.S. Census Bureau",
    "program": "Annual Business Survey (ABS) Characteristics of Businesses",
    "table": "ABSCB2023.AB2300CSCB04 (Sex/Ethnicity/Race/Veteran × Employment Size of Firm)",
    "year": "2023",
    "variable_or_question": (
        "QDESC=B28 WORKHOME; BUSCHAR=EWA "
        "'Business had employees who worked from home' as percent of "
        "BUSCHAR=EWTR 'Total reporting' (FIRMPDEMP_PCT). "
        "EMPSZFI 655 = firms with less than 500 employees; "
        "657 = firms with 500 employees or more. "
        "Firm-level (had any WFH employees), not worker WFH rate."
    ),
    "url": "https://www2.census.gov/programs-surveys/abs/data/2023/AB2300CSCB04.zip",
    "url_secondary": "https://data.census.gov/table/ABSCB2023.AB2300CSCB04",
    "funded_by": "U.S. Census Bureau (federal statistical agency)",
    "origin": "RETRIEVED",
    "confidence": "high",
    "notes": (
        "FTP YEAR field = 2023. Table notes on data.census.gov. "
        "This is not a worker telework rate and is not interchangeable with ACS/ATUS. "
        "SBA-style <500 vs 500+ bins are published as EMPSZFI 655 and 657."
    ),
}


def pct(num: float, den: float) -> float:
    return 100.0 * num / den


def write_csv(path: pathlib.Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise SystemExit(f"no rows for {path}")
    # stable column order: data fields then citation fields
    cite_keys = [
        "agency",
        "program",
        "table",
        "year",
        "variable_or_question",
        "url",
        "url_secondary",
        "funded_by",
        "origin",
        "confidence",
        "notes",
    ]
    all_keys: list[str] = []
    seen: set[str] = set()
    for r in rows:
        for k in r.keys():
            if k not in seen:
                seen.add(k)
                all_keys.append(k)
    data_keys = [k for k in all_keys if k not in cite_keys]
    fieldnames = data_keys + [k for k in cite_keys if k in seen]
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)


def build_acs_state() -> tuple[dict[str, Any], list[dict[str, Any]]]:
    data = json.loads((RAW / "censusreporter_b08301.json").read_text(encoding="utf-8"))
    assert data["release"]["id"] == "acs2024_1yr"

    rows: list[dict[str, Any]] = []
    us_row: dict[str, Any] | None = None

    for geo_id, payload in data["data"].items():
        est = payload["B08301"]["estimate"]
        err = payload["B08301"]["error"]
        total = est["B08301001"]
        wfh = est["B08301021"]
        if total is None or wfh is None or total == 0:
            continue
        name = data["geography"][geo_id]["name"]
        rate = pct(wfh, total)
        row = {
            "geo_id": geo_id,
            "geography": name,
            "geo_level": "nation" if geo_id == "01000US" else "state",
            "workers_16_plus": int(total),
            "worked_from_home": int(wfh),
            "wfh_rate_pct": rate,
            "workers_16_plus_moe": err.get("B08301001"),
            "worked_from_home_moe": err.get("B08301021"),
            **CITE_ACS,
        }
        if geo_id == "01000US":
            us_row = row
        else:
            rows.append(row)

    rows.sort(key=lambda r: r["wfh_rate_pct"], reverse=True)
    for i, r in enumerate(rows, start=1):
        r["rank_desc"] = i

    assert us_row is not None
    write_csv(OUT / "acs2024_wfh_by_state.csv", [us_row] + rows)
    return us_row, rows


def build_atus() -> list[dict[str, Any]]:
    """
    Values transcribed from BLS ATUS 2024 news release Tables 6 and 7
    (already retrieved HTML at the cited URL). Columns:
    total_employed_000s, worked_avg_day_000s, worked_at_home_000s,
    pct_of_those_who_worked.
    """
    # Source: https://www.bls.gov/news.release/archives/atus_06262025.htm
    # Table 6 / Table 7 — numbers in thousands; pct is of those who worked.
    records = [
        # Overall + FT/PT (Table 6)
        ("overall", "Total, 15 years and over", "Table 6", 172537, 112224, 36447, 32.5),
        ("hours", "Full-time workers", "Table 6", 134979, 93864, 31332, 33.4),
        ("hours", "Part-time workers", "Table 6", 37558, 18361, 5114, 27.9),
        # Education 25+ (Table 6) — seniority proxy
        ("education", "Less than a high school diploma", "Table 6", 8106, 5293, 266, 5.0),
        ("education", "High school graduates, no college", "Table 6", 38258, 25346, 4514, 17.8),
        ("education", "Some college or associate degree", "Table 6", 30545, 19362, 5012, 25.9),
        ("education", "Bachelor's degree and higher", "Table 6", 71811, 48943, 24467, 50.0),
        ("education", "Bachelor's degree only", "Table 6", 42196, 27820, 12899, 46.4),
        ("education", "Advanced degree", "Table 6", 29615, 21123, 11568, 54.8),
        # Occupation (Table 7) — seniority proxy (management vs others)
        ("occupation", "Management, business, and financial operations", "Table 7", 31374, 22176, 10670, 48.1),
        ("occupation", "Professional and related", "Table 7", 48324, 31756, 14753, 46.5),
        ("occupation", "Service", "Table 7", 28485, 15726, 1657, 10.5),
        ("occupation", "Sales and related", "Table 7", 13800, 8818, 2819, 32.0),
        ("occupation", "Office and administrative support", "Table 7", 15738, 9499, 2536, 26.7),
        ("occupation", "Construction and extraction", "Table 7", 7967, 5297, 875, 16.5),
        ("occupation", "Production", "Table 7", 8849, 5841, 484, 8.3),
        ("occupation", "Transportation and material moving", "Table 7", 11186, 7335, 426, 5.8),
        # Earnings quartiles FT wage/salary single job (Table 7)
        ("earnings_quartile", "$0 – $840 (lowest quartile)", "Table 7", 28317, 19508, 2593, 13.3),
        ("earnings_quartile", "$841 – $1,250", "Table 7", 28023, 18818, 4881, 25.9),
        ("earnings_quartile", "$1,251 – $1,970", "Table 7", 27215, 18042, 6414, 35.6),
        ("earnings_quartile", "$1,971 and higher (highest quartile)", "Table 7", 27837, 19363, 9879, 51.0),
    ]

    rows: list[dict[str, Any]] = []
    for break_type, label, table_name, tot, worked, home, published_pct in records:
        recomputed = pct(home, worked)
        # Guard: published one-decimal should match recomputed within 0.15
        if abs(recomputed - published_pct) > 0.15:
            raise SystemExit(
                f"ATUS mismatch {label}: published {published_pct} vs recomputed {recomputed:.3f}"
            )
        row = {
            "break_type": break_type,
            "group": label,
            "source_table": table_name,
            "total_employed_000s": tot,
            "worked_on_average_day_000s": worked,
            "worked_at_home_000s": home,
            "pct_worked_at_home_of_those_who_worked": recomputed,
            "published_pct_one_decimal": published_pct,
            "seniority_proxy": break_type
            in ("occupation", "education", "earnings_quartile"),
        }
        row.update(CITE_ATUS)
        row["table"] = f"{CITE_ATUS['table']} — {table_name}"
        rows.append(row)

    write_csv(OUT / "atus2024_work_at_home_breaks.csv", rows)
    return rows


def build_abs_firm_size() -> list[dict[str, Any]]:
    with zipfile.ZipFile(RAW / "AB2300CSCB04.zip") as z:
        lines = z.read("AB2300CSCB04.dat").decode("latin-1").splitlines()
    raw_rows = list(csv.DictReader(lines, delimiter="|"))

    want_sizes = {"655", "657", "001"}
    want_chars = {"EWA", "EWN", "EWTR"}
    rows: list[dict[str, Any]] = []

    for r in raw_rows:
        if r.get("QDESC") != "B28":
            continue
        if r.get("SEX") != "001":
            continue
        if r.get("ETH_GROUP") != "001":
            continue
        if r.get("RACE_GROUP") != "00":
            continue
        if r.get("VET_GROUP") != "001":
            continue
        if r.get("GEO_LABEL") != "United States":
            continue
        if r.get("EMPSZFI") not in want_sizes:
            continue
        if r.get("BUSCHAR") not in want_chars:
            continue

        firms = r.get("FIRMPDEMP")
        firms_pct = r.get("FIRMPDEMP_PCT")
        emp = r.get("EMP")
        emp_pct = r.get("EMP_PCT")
        # blanks / 'X' flags stay missing
        def num_or_none(x: str | None) -> float | None:
            if x is None or x.strip() == "" or x.strip().upper() == "X":
                return None
            try:
                return float(x)
            except ValueError:
                return None

        rows.append(
            {
                "empszfi": r["EMPSZFI"],
                "employment_size_of_firm": r["EMPSZFI_LABEL"],
                "buschar": r["BUSCHAR"],
                "business_characteristic": r["BUSCHAR_LABEL"],
                "employer_firms": num_or_none(firms),
                "pct_of_employer_firms": num_or_none(firms_pct),
                "employees": num_or_none(emp),
                "pct_of_employees": num_or_none(emp_pct),
                "firmpdemp_flag": r.get("FIRMPDEMP_F") or "",
                "firmpdemp_pct_flag": r.get("FIRMPDEMP_PCT_F") or "",
                "file_year": r.get("YEAR"),
                **CITE_ABS,
            }
        )

    # Recompute EWA share of EWTR for <500 and 500+ and verify published pct
    by_key = {(r["empszfi"], r["buschar"]): r for r in rows}
    for size in ("655", "657"):
        ewa = by_key[(size, "EWA")]
        ewtr = by_key[(size, "EWTR")]
        if ewa["employer_firms"] is None or ewtr["employer_firms"] is None:
            continue
        recomputed = pct(ewa["employer_firms"], ewtr["employer_firms"])
        published = ewa["pct_of_employer_firms"]
        if published is not None and abs(recomputed - published) > 0.15:
            raise SystemExit(
                f"ABS mismatch size {size}: published {published} vs {recomputed:.3f}"
            )
        ewa["recomputed_pct_of_total_reporting"] = recomputed

    write_csv(OUT / "abs2023_workhome_by_firm_size.csv", rows)
    return rows


def build_assumption_register(
    us: dict[str, Any],
    states: list[dict[str, Any]],
    atus: list[dict[str, Any]],
    abs_rows: list[dict[str, Any]],
) -> None:
    hi = states[0]
    lo = states[-1]
    mgmt = next(r for r in atus if r["group"].startswith("Management, business"))
    service = next(r for r in atus if r["group"] == "Service")
    top_earn = next(r for r in atus if "highest quartile" in r["group"])
    bot_earn = next(r for r in atus if "lowest quartile" in r["group"])
    bach = next(r for r in atus if r["group"] == "Bachelor's degree and higher")
    hs = next(r for r in atus if r["group"] == "High school graduates, no college")
    overall_atus = next(r for r in atus if r["group"].startswith("Total, 15"))
    small = next(
        r
        for r in abs_rows
        if r["empszfi"] == "655" and r["buschar"] == "EWA"
    )
    large = next(
        r
        for r in abs_rows
        if r["empszfi"] == "657" and r["buschar"] == "EWA"
    )

    lines = [
        {
            "line_id": "A1",
            "description": "US usually-WFH rate (ACS journey-to-work)",
            "value": round(us["wfh_rate_pct"], 6),
            "unit": "percent of workers 16+",
            "formula": "worked_from_home / workers_16_plus",
            **{k: us[k] for k in CITE_ACS},
        },
        {
            "line_id": "A2",
            "description": f"Highest state usually-WFH rate ({hi['geography']})",
            "value": round(hi["wfh_rate_pct"], 6),
            "unit": "percent of workers 16+",
            "formula": "state B08301_021E / B08301_001E",
            **{k: hi[k] for k in CITE_ACS},
        },
        {
            "line_id": "A3",
            "description": f"Lowest state usually-WFH rate ({lo['geography']})",
            "value": round(lo["wfh_rate_pct"], 6),
            "unit": "percent of workers 16+",
            "formula": "state B08301_021E / B08301_001E",
            **{k: lo[k] for k in CITE_ACS},
        },
        {
            "line_id": "B1",
            "description": "ATUS: any work at home on days worked — all employed 15+",
            "value": round(overall_atus["pct_worked_at_home_of_those_who_worked"], 6),
            "unit": "percent of persons who worked on an average day",
            "formula": "worked_at_home / worked_on_average_day",
            **{k: overall_atus[k] for k in CITE_ATUS},
        },
        {
            "line_id": "B2",
            "description": "Seniority proxy — management/business/financial occupation (ATUS)",
            "value": round(mgmt["pct_worked_at_home_of_those_who_worked"], 6),
            "unit": "percent of persons who worked on an average day",
            "formula": "worked_at_home / worked_on_average_day",
            **{k: mgmt[k] for k in CITE_ATUS},
        },
        {
            "line_id": "B3",
            "description": "Contrast — service occupations (ATUS)",
            "value": round(service["pct_worked_at_home_of_those_who_worked"], 6),
            "unit": "percent of persons who worked on an average day",
            "formula": "worked_at_home / worked_on_average_day",
            **{k: service[k] for k in CITE_ATUS},
        },
        {
            "line_id": "B4",
            "description": "Seniority proxy — highest usual weekly earnings quartile (ATUS)",
            "value": round(top_earn["pct_worked_at_home_of_those_who_worked"], 6),
            "unit": "percent of persons who worked on an average day",
            "formula": "worked_at_home / worked_on_average_day",
            **{k: top_earn[k] for k in CITE_ATUS},
        },
        {
            "line_id": "B5",
            "description": "Contrast — lowest usual weekly earnings quartile (ATUS)",
            "value": round(bot_earn["pct_worked_at_home_of_those_who_worked"], 6),
            "unit": "percent of persons who worked on an average day",
            "formula": "worked_at_home / worked_on_average_day",
            **{k: bot_earn[k] for k in CITE_ATUS},
        },
        {
            "line_id": "B6",
            "description": "Seniority proxy — bachelor's degree and higher (ATUS, age 25+)",
            "value": round(bach["pct_worked_at_home_of_those_who_worked"], 6),
            "unit": "percent of persons who worked on an average day",
            "formula": "worked_at_home / worked_on_average_day",
            **{k: bach[k] for k in CITE_ATUS},
        },
        {
            "line_id": "B7",
            "description": "Contrast — high school, no college (ATUS, age 25+)",
            "value": round(hs["pct_worked_at_home_of_those_who_worked"], 6),
            "unit": "percent of persons who worked on an average day",
            "formula": "worked_at_home / worked_on_average_day",
            **{k: hs[k] for k in CITE_ATUS},
        },
        {
            "line_id": "C1",
            "description": "Firms <500 employees that had any employees who WFH (ABS)",
            "value": small["pct_of_employer_firms"],
            "unit": "percent of employer firms (total reporting)",
            "formula": "EWA firms / EWTR firms (published FIRMPDEMP_PCT)",
            **{k: small[k] for k in CITE_ABS},
        },
        {
            "line_id": "C2",
            "description": "Firms 500+ employees that had any employees who WFH (ABS)",
            "value": large["pct_of_employer_firms"],
            "unit": "percent of employer firms (total reporting)",
            "formula": "EWA firms / EWTR firms (published FIRMPDEMP_PCT)",
            **{k: large[k] for k in CITE_ABS},
        },
        {
            "line_id": "X1",
            "description": "Job title / corporate seniority ladder (VP vs IC)",
            "value": None,
            "unit": "n/a",
            "formula": "NOT PUBLISHED — refused to invent",
            "agency": "n/a",
            "program": "n/a",
            "table": "n/a",
            "year": "n/a",
            "variable_or_question": (
                "No ACS/ATUS/ABS table publishes WFH by job level "
                "(VP / director / individual contributor). Closest official "
                "proxies used: occupation, earnings quartile, education."
            ),
            "url": "n/a",
            "url_secondary": "",
            "funded_by": "n/a",
            "origin": "ESTIMATED",
            "confidence": "n/a — break not constructed",
            "notes": "Do not impute a seniority ladder.",
        },
        {
            "line_id": "X2",
            "description": "Worker-level WFH rate crossed with firm size <500 vs 500+",
            "value": None,
            "unit": "n/a",
            "formula": "NOT PUBLISHED in ACS/ATUS — ABS is firm-level only",
            "agency": "U.S. Census Bureau",
            "program": "ABS Characteristics of Businesses (firm perspective)",
            "table": "ABSCB2023.AB2300CSCB04 B28 WORKHOME",
            "year": "2023",
            "variable_or_question": (
                "ABS publishes whether the firm had employees who worked from "
                "home, not the share of workers at small vs large firms who WFH. "
                "No imputation from industry mix."
            ),
            "url": CITE_ABS["url"],
            "url_secondary": CITE_ABS["url_secondary"],
            "funded_by": CITE_ABS["funded_by"],
            "origin": "RETRIEVED",
            "confidence": "high for firm-level; worker-level cross does not exist here",
            "notes": "Refused to invent worker×firm-size WFH rates.",
        },
    ]
    write_csv(OUT / "assumption_register.csv", lines)

    summary = {
        "us_acs_usually_wfh_pct": round(us["wfh_rate_pct"], 1),
        "us_acs_workers_16_plus": us["workers_16_plus"],
        "us_acs_worked_from_home": us["worked_from_home"],
        "state_high": {
            "name": hi["geography"],
            "pct": round(hi["wfh_rate_pct"], 1),
            "workers": hi["workers_16_plus"],
            "wfh": hi["worked_from_home"],
        },
        "state_low": {
            "name": lo["geography"],
            "pct": round(lo["wfh_rate_pct"], 1),
            "workers": lo["workers_16_plus"],
            "wfh": lo["worked_from_home"],
        },
        "state_spread_pp": round(hi["wfh_rate_pct"] - lo["wfh_rate_pct"], 1),
        "atus_overall_pct": round(overall_atus["pct_worked_at_home_of_those_who_worked"], 1),
        "atus_mgmt_pct": round(mgmt["pct_worked_at_home_of_those_who_worked"], 1),
        "atus_service_pct": round(service["pct_worked_at_home_of_those_who_worked"], 1),
        "atus_top_earn_pct": round(top_earn["pct_worked_at_home_of_those_who_worked"], 1),
        "atus_bot_earn_pct": round(bot_earn["pct_worked_at_home_of_those_who_worked"], 1),
        "atus_bach_pct": round(bach["pct_worked_at_home_of_those_who_worked"], 1),
        "atus_hs_pct": round(hs["pct_worked_at_home_of_those_who_worked"], 1),
        "abs_small_lt500_firm_wfh_pct": small["pct_of_employer_firms"],
        "abs_large_500plus_firm_wfh_pct": large["pct_of_employer_firms"],
        "citations": {"acs": CITE_ACS, "atus": CITE_ATUS, "abs": CITE_ABS},
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


def main() -> None:
    us, states = build_acs_state()
    atus = build_atus()
    abs_rows = build_abs_firm_size()
    build_assumption_register(us, states, atus, abs_rows)
    print("Wrote CSVs to", OUT)


if __name__ == "__main__":
    main()
