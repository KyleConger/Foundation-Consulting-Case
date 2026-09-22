"""Download ABS Characteristics of Businesses zips and inspect WORKHOME tables."""
from __future__ import annotations

import pathlib
import zipfile
import io
import urllib.request

RAW = pathlib.Path(__file__).resolve().parent / "raw"
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}


def get(url: str, name: str) -> pathlib.Path | None:
    dest = RAW / name
    req = urllib.request.Request(url, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            data = r.read()
        dest.write_bytes(data)
        print("OK", name, len(data))
        return dest
    except Exception as e:
        print("FAIL", name, e)
        return None


def list_zip(path: pathlib.Path) -> None:
    print("===", path.name, "===")
    with zipfile.ZipFile(path) as z:
        for info in z.infolist():
            print(f"  {info.filename}  {info.file_size}")


def main() -> None:
    base23 = "https://www2.census.gov/programs-surveys/abs/data/2023/"
    base22 = "https://www2.census.gov/programs-surveys/abs/data/2022/"
    base25 = "https://www2.census.gov/programs-surveys/abs/data/2025/"

    # list 2025
    req = urllib.request.Request(base25, headers=UA)
    try:
        html = urllib.request.urlopen(req, timeout=60).read().decode("utf-8", "replace")
        (RAW / "abs2025_ftp.html").write_text(html, encoding="utf-8")
        print("2025 listing bytes", len(html))
        import re
        for h in re.findall(r'href="([^"]+)"', html):
            if h.endswith(".zip") or h.endswith(".xlsx") or h.endswith("/"):
                if "css" not in h:
                    print(" 2025:", h)
    except Exception as e:
        print("2025 fail", e)

    files = [
        (base23 + "AB2300CSCB04.zip", "AB2300CSCB04.zip"),
        (base23 + "AB2300CSCB01.zip", "AB2300CSCB01.zip"),
        (base23 + "AB2300CSCBO.zip", "AB2300CSCBO.zip"),
        (base22 + "ABSCB2022.zip", "ABSCB2022.zip"),
        (base22 + "AB2200CSCB04.zip", "AB2200CSCB04.zip"),
    ]
    for url, name in files:
        p = get(url, name)
        if p:
            list_zip(p)


if __name__ == "__main__":
    main()
