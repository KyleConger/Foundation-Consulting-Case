"""Print canvas-ready table rows. Not a second model — reads the CSV."""
import csv
import json
from pathlib import Path

p = Path(__file__).resolve().parent / "out" / "chtr_vs_cmcsa_state_leads.csv"
rows = list(csv.DictReader(p.open(encoding="utf-8")))


def fmt_pct(s: str) -> str:
    if s == "":
        return "—"
    x = float(s) * 100
    if x < 0.05:
        return "<0.1%"
    return f"{x:.1f}%"


def fmt_u(s: str) -> str:
    if s == "":
        return "—"
    n = int(s)
    if n >= 1_000_000:
        return f"{n / 1_000_000:.2f}M"
    if n >= 10_000:
        return f"{n / 1_000:.0f}k"
    return f"{n:,}"


def fmt_margin(s: str, leader: str) -> str:
    n = int(s)
    if leader == "neither present":
        return "—"
    if n == 0:
        return "0"
    sign = "+" if n > 0 else "−"
    v = abs(n)
    if v >= 1_000_000:
        return f"{sign}{v / 1_000_000:.2f}M"
    if v >= 10_000:
        return f"{sign}{v / 1_000:.0f}k"
    return f"{sign}{v:,}"


out = []
for r in rows:
    leader = {
        "Charter": "Charter",
        "Comcast": "Comcast",
        "neither present": "Neither",
        "tie": "Tie",
    }[r["leader"]]
    tone = {
        "Charter": "info",
        "Comcast": "neutral",
        "Neither": "warning",
        "Tie": "warning",
    }[leader]
    ch = (
        "—"
        if r["charter_est_units"] == ""
        else f"{fmt_u(r['charter_est_units'])} · {fmt_pct(r['charter_res_st_pct'])}"
    )
    cm = (
        "—"
        if r["comcast_est_units"] == ""
        else f"{fmt_u(r['comcast_est_units'])} · {fmt_pct(r['comcast_res_st_pct'])}"
    )
    out.append(
        {
            "cells": [
                f"{r['state']} ({r['abbr']})",
                leader,
                ch,
                cm,
                fmt_margin(r["margin_units_charter_minus_comcast"], r["leader"]),
                fmt_u(r["total_residential_units"]),
            ],
            "tone": tone,
        }
    )

print(json.dumps(out, indent=2))
