"""Probe Census ABS download locations and data.census.gov table endpoints."""
from __future__ import annotations

import pathlib
import re
import urllib.request

RAW = pathlib.Path(__file__).resolve().parent / "raw"
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}


def get(url: str, name: str | None = None) -> bytes | None:
    req = urllib.request.Request(url, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            data = r.read()
        print("OK", name or url[:100], len(data), data[:80])
        if name:
            (RAW / name).write_bytes(data)
        return data
    except Exception as e:
        print("FAIL", name or url[:100], e)
        return None


def list_ftp(url: str) -> None:
    data = get(url)
    if not data:
        return
    text = data.decode("utf-8", "replace")
    hrefs = re.findall(r'href="([^"]+)"', text)
    print("===", url, "===")
    for h in hrefs:
        if any(x in h.lower() for x in [".xlsx", ".csv", ".zip", ".txt", ".dat", "cb", "abs", "work", "/"]):
            if "css" in h or "bootstrap" in h or "font-awesome" in h:
                continue
            print(" ", h)


def main() -> None:
    list_ftp("https://www2.census.gov/programs-surveys/abs/data/")
    list_ftp("https://www2.census.gov/programs-surveys/abs/data/2023/")
    list_ftp("https://www2.census.gov/programs-surveys/abs/data/2022/")
    list_ftp("https://www2.census.gov/programs-surveys/abs/data/2024/")

    # data.census.gov candidate table IDs for WORKHOME x EMPSZFI
    table_ids = [
        "ABSCB2023.AB2300CSA04",
        "ABSCB2023.AB2300CBO04",
        "ABSCB2022.AB2200CSA04",
        "ABSCB2024.AB2400CSA04",
        "ABSCB2023.AB2300CBO08",
        "ABSCB2022.AB2200CBO04",
    ]
    for tid in table_ids:
        url = f"https://data.census.gov/table/{tid}"
        get(url, f"dctable_{tid.replace('.', '_')}.html")

    # Try Census key signup page info
    get("https://api.census.gov/data/key_signup.html", "census_key_signup.html")

    # BRS national xlsx via archived path patterns
    brs = [
        "https://www.bls.gov/brs/data/tables/2022/xlsx/brs-national.xlsx",
        "https://www.bls.gov/brs/data/tables/2022/download/brs-2022-national.xlsx",
        "https://www.bls.gov/brs/data/tables/2022/brs-2022-table-148.xlsx",
        "https://www.bls.gov/brs/data/tables/2022/xlsx/size-2.1.xlsx",
        "https://www.bls.gov/brs/data/tables/2022/xlsx/size-2-1.xlsx",
        "https://www.bls.gov/brs/data/tables/2022/xlsx/2.1-size.xlsx",
    ]
    for i, url in enumerate(brs):
        get(url, f"brs_try_{i}.bin")


if __name__ == "__main__":
    main()
