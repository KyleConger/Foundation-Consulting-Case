"""Parse ABS AB2300CSCB04.dat for WORKHOME (B28) by employment size."""
from __future__ import annotations

import csv
import pathlib
import zipfile

RAW = pathlib.Path(__file__).resolve().parent / "raw"
OUT = pathlib.Path(__file__).resolve().parent / "out"
OUT.mkdir(exist_ok=True)

FIELDS = [
    ("GEO_ID", 30),
    ("GEO_LABEL", 255),
    ("GEO_ID_F", 4),
    ("GEOTYPE", 2),
    ("ST", 2),
    ("NAICS2022", 8),
    ("NAICS2022_LABEL", 255),
    ("NAICS2022_F", 4),
    ("SEX", 3),
    ("SEX_LABEL", 255),
    ("ETH_GROUP", 3),
    ("ETH_GROUP_LABEL", 255),
    ("RACE_GROUP", 2),
    ("RACE_GROUP_LABEL", 255),
    ("VET_GROUP", 3),
    ("VET_GROUP_LABEL", 255),
    ("EMPSZFI", 3),
    ("EMPSZFI_LABEL", 255),
    ("QDESC", 6),
    ("QDESC_LABEL", 255),
    ("BUSCHAR", 10),
    ("BUSCHAR_LABEL", 255),
    ("YEAR", 4),
    ("FIRMPDEMP", 10),
    ("FIRMPDEMP_F", 1),
    ("FIRMPDEMP_PCT", 10),
    ("FIRMPDEMP_PCT_F", 1),
    ("RCPPDEMP", 11),
    ("RCPPDEMP_F", 1),
    ("RCPPDEMP_PCT", 10),
    ("RCPPDEMP_PCT_F", 1),
    ("EMP", 10),
    ("EMP_F", 1),
    ("EMP_PCT", 10),
    ("EMP_PCT_F", 1),
    ("PAYANN", 11),
    ("PAYANN_F", 1),
    ("PAYANN_PCT", 10),
    ("PAYANN_PCT_F", 1),
    ("FIRMPDEMP_S", 10),
    ("FIRMPDEMP_S_F", 1),
    ("FIRMPDEMP_PCT_S", 10),
    ("FIRMPDEMP_PCT_S_F", 1),
    ("RCPPDEMP_S", 10),
    ("RCPPDEMP_S_F", 1),
    ("RCPPDEMP_PCT_S", 10),
    ("RCPPDEMP_PCT_S_F", 1),
    ("EMP_S", 10),
    ("EMP_S_F", 1),
    ("EMP_PCT_S", 10),
    ("EMP_PCT_S_F", 1),
    ("PAYANN_S", 10),
    ("PAYANN_S_F", 1),
    ("PAYANN_PCT_S", 10),
    ("PAYANN_PCT_S_F", 1),
]


def parse_fixed(line: str) -> dict[str, str]:
    row = {}
    pos = 0
    for name, length in FIELDS:
        row[name] = line[pos : pos + length].strip()
        pos += length
    return row


def main() -> None:
    with zipfile.ZipFile(RAW / "AB2300CSCB04.zip") as z:
        raw = z.read("AB2300CSCB04.dat")

    # Detect delimiter
    sample = raw[:500]
    print("sample bytes", sample[:120])
    text = raw.decode("latin-1")
    lines = text.splitlines()
    print("nlines", len(lines), "linelen0", len(lines[0]) if lines else None)
    expected = sum(L for _, L in FIELDS)
    print("expected width", expected)

    # Try pipe first
    if "|" in lines[0]:
        reader = csv.DictReader(lines, delimiter="|")
        rows = list(reader)
        print("pipe cols", list(rows[0].keys())[:10])
    else:
        rows = [parse_fixed(L) for L in lines if L.strip()]

    # Filter US total demographics, B28
    b28 = []
    for r in rows:
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
        # US only
        geo = r.get("GEO_ID") or r.get("GEO_LABEL") or ""
        if not (geo.startswith("0100000US") or r.get("GEO_LABEL") == "United States" or r.get("ST") in ("", "00")):
            # keep if GEO_LABEL is US
            if "United States" not in (r.get("GEO_LABEL") or ""):
                continue
        b28.append(r)

    print("B28 US total-demo rows", len(b28))
    # show unique QDESC_LABEL / YEAR
    if b28:
        print("year", b28[0].get("YEAR"), "qdesc_label", b28[0].get("QDESC_LABEL"))
    for r in b28:
        print(
            r.get("EMPSZFI"),
            r.get("EMPSZFI_LABEL"),
            r.get("BUSCHAR"),
            r.get("BUSCHAR_LABEL"),
            "firms",
            r.get("FIRMPDEMP"),
            "pct",
            r.get("FIRMPDEMP_PCT"),
            "emp",
            r.get("EMP"),
            "emp_pct",
            r.get("EMP_PCT"),
            "flag",
            r.get("FIRMPDEMP_F"),
            r.get("FIRMPDEMP_PCT_F"),
        )

    # Also dump all QDESC labels seen for total demo EMPSZFI=001
    qlabels = {}
    for r in rows:
        if r.get("SEX") == "001" and r.get("ETH_GROUP") == "001" and r.get("RACE_GROUP") == "00" and r.get("VET_GROUP") == "001":
            if (r.get("GEO_LABEL") == "United States" or (r.get("GEO_ID") or "").startswith("0100000US")):
                if r.get("EMPSZFI") == "001":
                    qlabels[r.get("QDESC")] = r.get("QDESC_LABEL")
    print("QDESC map", qlabels)


if __name__ == "__main__":
    main()
