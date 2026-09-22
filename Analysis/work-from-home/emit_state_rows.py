"""Emit canvas STATE_ROWS from CSV — must match one-decimal rounding."""
from __future__ import annotations

import csv
import pathlib

out = pathlib.Path(__file__).resolve().parent / "out"
rows = list(csv.DictReader((out / "acs2024_wfh_by_state.csv").open(encoding="utf-8")))
states = [r for r in rows if r["geo_level"] == "state"]
states.sort(key=lambda r: -float(r["wfh_rate_pct"]))

print("const STATE_ROWS: (string | number)[][] = [")
for i, r in enumerate(states, 1):
    name = r["geography"]
    rate = round(float(r["wfh_rate_pct"]), 1)
    workers = int(float(r["workers_16_plus"]))
    wfh = int(float(r["worked_from_home"]))
    print(
        f'  ["{i}", "{name}", "{rate}%", "{workers:,}", "{wfh:,}"],'
    )
print("];")

# verify US
us = next(r for r in rows if r["geo_level"] == "nation")
print("US", round(float(us["wfh_rate_pct"]), 1), int(float(us["workers_16_plus"])), int(float(us["worked_from_home"])))
