"""Extract data.census.gov links from the 2024 ABS characteristics page."""
from __future__ import annotations

import pathlib
import re
import urllib.request

RAW = pathlib.Path(__file__).resolve().parent / "raw"
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

url = "https://www.census.gov/data/tables/2024/econ/abs/2024-abs-characteristics-of-businesses.html"
req = urllib.request.Request(url, headers=UA)
html = urllib.request.urlopen(req, timeout=60).read().decode("utf-8", "replace")
(RAW / "abs2024_characteristics_page.html").write_text(html, encoding="utf-8")

# Find all data.census.gov links
links = sorted(set(re.findall(r'https?://data\.census\.gov[^"\s<>]+', html)))
print("data.census.gov links:", len(links))
for L in links:
    print(L)

# Also look for workhome-ish text near hrefs
for m in re.finditer(r'href="([^"]+)"[^>]*>([^<]{0,80})', html):
    href, text = m.group(1), m.group(2)
    blob = (href + " " + text).lower()
    if any(k in blob for k in ["workhome", "work from", "perwhome", "facwhome", "employment size", "abscb"]):
        print("NEAR:", text.strip()[:60], "->", href[:120])
