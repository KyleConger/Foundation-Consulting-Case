# -*- coding: utf-8 -*-
"""Q1 2026 residential Internet rate vs volume for the EH&B executive talk track.

The Q1 10-Q prints the bridge. That printed split is the exhibit.
The implied-ARPU identity is recomputed here and labeled DERIVED.
It does not override the printed bridge.
"""
from __future__ import annotations

import json
from pathlib import Path

OUT = Path(__file__).resolve().parent / "out"
OUT.mkdir(parents=True, exist_ok=True)

# RETRIEVED — Ex99.1 Q1 2026 financials ($ millions) and operating stats (000s).
REV_TOTAL_26 = 13597
REV_TOTAL_25 = 13735
REV_INET_26 = 5852
REV_INET_25 = 5930
REV_MOB_26 = 1052
REV_MOB_25 = 914
REV_VID_26 = 3252
REV_VID_25 = 3580
REV_VOICE_26 = 338
REV_VOICE_25 = 356
REV_SMB_26 = 1090
REV_MM_26 = 749
REV_ADS_26 = 358
REV_OTHER_26 = 906
REV_RES_26 = 10494

RES_INET_END_26 = 27524  # thousands, 31 Mar 2026
RES_INET_ADD_26 = -117
RES_INET_END_25 = 27979  # thousands, 31 Mar 2025
RES_INET_ADD_25 = -55
PASSINGS_Q1 = 58661  # thousands
PEN_Q1 = 54.0
CR_Q1 = 31683  # thousands

# RETRIEVED — Q1 2026 10-Q printed residential Internet bridge ($ millions).
PRINTED_VOLUME = -87
PRINTED_RATE = 9
PRINTED_NET = -78

# RETRIEVED — FY2025 10-K residential Internet bridge ($ millions) and customers.
FY25_RATE = 785
FY25_VOLUME = -380
FY25_NET = 405
FY25_CUSTOMERS = -393000

# RETRIEVED — Q1 trending subsidized rural; 10-K cumulative spend.
RURAL_PASSINGS_Q1 = 1385  # thousands
RURAL_CR_Q1 = 527  # thousands
RURAL_PEN_PRINTED = 38.1  # percent, trending schedule
RURAL_SPEND_B = 7.7  # 10-K, since inception through 31 Dec 2025

# RETRIEVED — Q2 2026 Ex99.1 (later public fact) and 10-Q leverage.
PASSINGS_Q2 = 58981  # thousands
PEN_Q2 = 53.4
DEBT_PRINCIPAL_B = 93.8  # 30 Jun 2026 Ex99.1
LEVERAGE = 4.18  # 30 Jun 2026 10-Q

MOBILE_LINES_ADD = 368  # thousands, total lines, Ex99.1
MOBILE_REV_DELTA = REV_MOB_26 - REV_MOB_25

MIX_LINES = [
    ("Internet", REV_INET_26),
    ("Video", REV_VID_26),
    ("Small business", REV_SMB_26),
    ("Mobile service", REV_MOB_26),
    ("Other", REV_OTHER_26),
    ("Mid-market and large business", REV_MM_26),
    ("Advertising sales", REV_ADS_26),
    ("Voice", REV_VOICE_26),
]


def monthly_arpu(rev_m: float, begin_k: float, end_k: float) -> float:
    """Charter's disclosed ARPU identity: quarterly $ / 3 / average customers."""
    avg_k = (begin_k + end_k) / 2.0
    return rev_m * 1000.0 / 3.0 / avg_k


def main() -> None:
    mix_sum = sum(v for _, v in MIX_LINES)
    assert mix_sum == REV_TOTAL_26, mix_sum
    assert REV_INET_26 + REV_MOB_26 + REV_VID_26 + REV_VOICE_26 == REV_RES_26
    assert REV_INET_26 - REV_INET_25 == PRINTED_NET
    assert PRINTED_VOLUME + PRINTED_RATE == PRINTED_NET
    assert FY25_RATE + FY25_VOLUME == FY25_NET
    assert MOBILE_REV_DELTA == 138
    assert round(CR_Q1 / PASSINGS_Q1 * 100, 1) == PEN_Q1
    rural_pen = RURAL_CR_Q1 / RURAL_PASSINGS_Q1 * 100
    assert round(rural_pen, 1) == RURAL_PEN_PRINTED

    begin_26 = RES_INET_END_26 - RES_INET_ADD_26
    begin_25 = RES_INET_END_25 - RES_INET_ADD_25
    avg_26 = (begin_26 + RES_INET_END_26) / 2.0
    avg_25 = (begin_25 + RES_INET_END_25) / 2.0
    arpu_26 = monthly_arpu(REV_INET_26, begin_26, RES_INET_END_26)
    arpu_25 = monthly_arpu(REV_INET_25, begin_25, RES_INET_END_25)
    # Hold last year's implied rate on this year's smaller average base.
    derived_volume = (avg_26 - avg_25) * arpu_25 * 3.0 / 1000.0
    derived_rate = (arpu_26 - arpu_25) * avg_26 * 3.0 / 1000.0
    derived_net = derived_volume + derived_rate
    arpu_hold_flat = REV_INET_25 * 1000.0 / 3.0 / avg_26
    arpu_gap = arpu_hold_flat - arpu_26

    assert abs(derived_net - PRINTED_NET) < 0.6, derived_net
    # Rounded derived split is the talk-track −$90 / +$12. It is not the filing.
    assert round(derived_volume) == -90
    assert round(derived_rate) == 12
    assert round(arpu_26, 2) == 70.72
    assert round(arpu_25, 2) == 70.58
    assert round(arpu_gap, 2) == 0.94

    shares = [
        {
            "line": name,
            "revenue_m": rev,
            "share": rev / REV_TOTAL_26,
            "share_pct_1dp": round(rev / REV_TOTAL_26 * 100, 1),
            "accent": name == "Internet",
        }
        for name, rev in sorted(MIX_LINES, key=lambda x: -x[1])
    ]

    payload = {
        "headline_split": "RETRIEVED",
        "printed_bridge": {
            "label": "RETRIEVED",
            "volume_m": PRINTED_VOLUME,
            "rate_mix_m": PRINTED_RATE,
            "net_m": PRINTED_NET,
            "source": "PrimarySources/readable/CHTR-10-Q-Q1-2026.md",
            "note": "Printed residential Internet bridge. Use this, not the derived split.",
        },
        "derived_bridge": {
            "label": "DERIVED",
            "volume_m": derived_volume,
            "rate_mix_m": derived_rate,
            "net_m": derived_net,
            "volume_m_rounded": round(derived_volume),
            "rate_mix_m_rounded": round(derived_rate),
            "arpu_26": round(arpu_26, 2),
            "arpu_25": round(arpu_25, 2),
            "arpu_hold_flat": round(arpu_hold_flat, 2),
            "arpu_gap_per_month": round(arpu_gap, 2),
            "avg_customers_26_k": avg_26,
            "avg_customers_25_k": avg_25,
            "begin_26_k": begin_26,
            "begin_25_k": begin_25,
            "formula_arpu": "quarterly Internet $ millions × 1,000 / 3 / average customers (thousands)",
            "formula_average": "average = (ending − quarterly net adds + ending) / 2",
            "formula_volume": "(avg_26 − avg_25) × ARPU_25 × 3 / 1,000",
            "formula_rate": "(ARPU_26 − ARPU_25) × avg_26 × 3 / 1,000",
            "formula_hold_flat": "ARPU to hold dollars flat = Q1 2025 Internet $ × 1,000 / 3 / avg_26; gap = that ARPU − ARPU_26",
            "note": "Cross-check only. Rounds to −$90 million volume and +$12 million rate. Does not override the printed −$87 / +$9.",
        },
        "mix": shares,
        "revenue_total_m": REV_TOTAL_26,
        "internet_yoy_pct": (REV_INET_26 - REV_INET_25) / REV_INET_25,
        "res_inet_net_adds_k": RES_INET_ADD_26,
        "fy25": {
            "rate_mix_m": FY25_RATE,
            "volume_m": FY25_VOLUME,
            "net_m": FY25_NET,
            "residential_internet_customers": FY25_CUSTOMERS,
            "label": "RETRIEVED",
        },
        "plant": {
            "q1_passings_k": PASSINGS_Q1,
            "q1_penetration_pct": PEN_Q1,
            "q1_customer_relationships_k": CR_Q1,
            "rural_passings_k": RURAL_PASSINGS_Q1,
            "rural_cr_k": RURAL_CR_Q1,
            "rural_penetration_pct": round(rural_pen, 1),
            "rural_spend_b": RURAL_SPEND_B,
            "q2_passings_k": PASSINGS_Q2,
            "q2_penetration_pct": PEN_Q2,
            "debt_principal_b": DEBT_PRINCIPAL_B,
            "leverage_x": LEVERAGE,
        },
        "mobile": {
            "lines_net_adds_k": MOBILE_LINES_ADD,
            "service_revenue_delta_m": MOBILE_REV_DELTA,
            "label": "RETRIEVED",
        },
    }
    path = OUT / "summary.json"
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(json.dumps({
        "printed": payload["headline_split"],
        "printed_volume": PRINTED_VOLUME,
        "printed_rate": PRINTED_RATE,
        "derived_volume_rounded": round(derived_volume),
        "derived_rate_rounded": round(derived_rate),
        "arpu_26": round(arpu_26, 2),
        "arpu_25": round(arpu_25, 2),
        "arpu_gap": round(arpu_gap, 2),
        "internet_share_pct": shares[0]["share_pct_1dp"],
        "video_share_pct": next(s["share_pct_1dp"] for s in shares if s["line"] == "Video"),
        "mobile_share_pct": next(s["share_pct_1dp"] for s in shares if s["line"] == "Mobile service"),
        "rural_pen": round(rural_pen, 4),
        "wrote": str(path),
    }, indent=2))


if __name__ == "__main__":
    main()
