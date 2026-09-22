"""Download official WFH source tables into raw/."""
from __future__ import annotations

import json
import pathlib
import re
import urllib.request

RAW = pathlib.Path(__file__).resolve().parent / "raw"
RAW.mkdir(parents=True, exist_ok=True)
UA = {"User-Agent": "Mozilla/5.0 (compatible; MAN6930-research/1.0)"}


def get(url: str, name: str | None = None) -> bytes | None:
    req = urllib.request.Request(url, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            data = r.read()
        print(f"OK {name or url[:90]} bytes={len(data)}")
        if name:
            (RAW / name).write_bytes(data)
        return data
    except Exception as e:
        print(f"FAIL {name or url[:90]}: {e}")
        return None


def main() -> None:
    # Census Reporter already saved; refresh for completeness
    get(
        "https://api.censusreporter.org/1.0/data/show/latest"
        "?table_ids=B08301&geo_ids=040%7C01000US,01000US",
        "censusreporter_b08301.json",
    )

    # ABS API probes (2023 reference year = 2024 ABS)
    abs_urls = [
        (
            "abs_workhome_us.json",
            "https://api.census.gov/data/2023/abscb"
            "?get=NAME,FIRMPDEMP,FIRMPDEMP_PCT,EMP,EMPSZFI,QDESC,BUSCHAR"
            "&for=us:*&NAICS2022=00&SEX=001&ETH_GROUP=001&RACE_GROUP=00"
            "&VET_GROUP=001&QDESC=B28",
        ),
        (
            "abs_workhome_empsize.json",
            "https://api.census.gov/data/2023/abscs"
            "?get=NAME,FIRMPDEMP,FIRMPDEMP_PCT,EMP,EMPSZFI"
            "&for=us:*&NAICS2022=00",
        ),
    ]
    for name, url in abs_urls:
        get(url, name)

    # FTP directory listing for ABS excel
    html = get("https://www2.census.gov/programs-surveys/abs/data/2024/", "abs2024_ftp.html")
    if html:
        text = html.decode("utf-8", "replace")
        links = re.findall(r'href="([^"]+)"', text)
        print("FTP links:")
        for link in links:
            print(" ", link)

    # Common ABS table naming patterns for WORKHOME x employment size
    candidates = [
        "https://www2.census.gov/programs-surveys/abs/data/2024/abs2024_cb_workhome.xlsx",
        "https://www2.census.gov/programs-surveys/abs/data/2023/abs2023_cb_workhome.xlsx",
        "https://www2.census.gov/programs-surveys/abs/data/2024/ABSCB2023.dat",
        "https://api.census.gov/data/2023/abscb"
        "?get=GEO_ID,NAME,NAICS2022,SEX,ETH_GROUP,RACE_GROUP,VET_GROUP,"
        "EMPSZFI,QDESC,BUSCHAR,YEAR,FIRMPDEMP,FIRMPDEMP_F,FIRMPDEMP_PCT,"
        "FIRMPDEMP_PCT_F,RCPPDEMP,RCPPDEMP_F,RCPPDEMP_PCT,RCPPDEMP_PCT_F,"
        "EMP,EMP_F,EMP_PCT,EMP_PCT_F,PAYANN,PAYANN_F,PAYANN_PCT,PAYANN_PCT_F,"
        "FIRMPDEMP_S,FIRMPDEMP_PCT_S,RCPPDEMP_S,RCPPDEMP_PCT_S,EMP_S,EMP_PCT_S,"
        "PAYANN_S,PAYANN_PCT_S"
        "&for=us:*&QDESC=B28&SEX=001&ETH_GROUP=001&RACE_GROUP=00&VET_GROUP=001"
        "&NAICS2022=00",
    ]
    for i, url in enumerate(candidates):
        get(url, f"abs_candidate_{i}")


if __name__ == "__main__":
    main()
