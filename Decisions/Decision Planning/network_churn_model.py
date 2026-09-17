"""
Customer network performance and churn — Q1 2026 anchor.
Recomputes the Decision Planning canvas arithmetic. Run:
  python "Decision Planning/network_churn_model.py"
"""

from __future__ import annotations

# --- RETRIEVED: CHTR Ex99.1 / trending (000s) ---
CHTR_INET_EOP = {
    "24Q1": 30518,
    "24Q2": 30370,
    "24Q3": 30260,
    "24Q4": 30083,
    "25Q1": 30024,
    "25Q2": 29908,
    "25Q3": 29799,
    "25Q4": 29680,
    "26Q1": 29560,
}
CHTR_INET_ADD = {
    "24Q1": -72,
    "24Q2": -148,
    "24Q3": -110,
    "24Q4": -177,
    "25Q1": -59,
    "25Q2": -116,
    "25Q3": -109,
    "25Q4": -119,
    "26Q1": -120,
}
CHTR_RES_INET_YE25 = 27641
CHTR_RES_INET_ADD_Q1_26 = -117
CHTR_RES_INET_YE24 = 28034
CHTR_RES_INET_ADD_Q1_25 = -55
CHTR_CR_YE25 = 31846
CHTR_CR_ADD_Q1 = -163
RURAL_CR_YE25 = 486
RURAL_CR_ADD_Q1 = 41
PASSINGS_Q1 = 58661  # thousand
PEN_CR_Q1 = 0.540
ATT_FTTH = 0.27
VZ_FTTH = 0.16

# --- RETRIEVED: CMCSA Ex99.1 Q1 2026 (000s) ---
CMCSA_BB_EOP_Q1_26 = 28654
CMCSA_BB_ADD_Q1_26 = -65
CMCSA_BB_EOP_Q1_25 = 29190
CMCSA_BB_ADD_Q1_25 = -183
CMCSA_PASSINGS_Q1_26 = 59164
CMCSA_PEN_Q1_26 = 0.484

# --- RETRIEVED: opex / capex $M ---
FIELD_Q1_26, FIELD_Q1_25 = 1258, 1282
CARE_Q1_26, CARE_Q1_25 = 766, 772
UPG_Q1_26, UPG_Q1_25 = 675, 395
INET_REV_FY25 = 23765  # $M
INET_YE24, INET_YE25 = 30083, 29680

# --- derived ---
def loss_rate(add: int, begin: int) -> float:
    return abs(add) / begin


def main() -> None:
    qtrs = list(CHTR_INET_ADD)
    rates = []
    print("ID  Line                                              Value           Tag")
    print("-" * 78)
    for q in qtrs:
        add = CHTR_INET_ADD[q]
        begin = CHTR_INET_EOP[q] - add
        r = loss_rate(add, begin)
        rates.append(r)
        print(f"     CHTR Internet net-loss rate {q}                 {100*r:6.3f}% of begin")

    a1 = CHTR_RES_INET_YE25
    a2 = CHTR_RES_INET_ADD_Q1_26
    a3 = loss_rate(a2, a1)
    b1 = CMCSA_BB_EOP_Q1_26 - CMCSA_BB_ADD_Q1_26
    b2 = loss_rate(CMCSA_BB_ADD_Q1_26, b1)
    c1 = CHTR_RES_INET_YE24
    c2 = loss_rate(CHTR_RES_INET_ADD_Q1_25, c1)
    d1 = CMCSA_BB_EOP_Q1_25 - CMCSA_BB_ADD_Q1_25
    d2 = loss_rate(CMCSA_BB_ADD_Q1_25, d1)
    ratio = a3 / b2
    expected = b2 * a1
    excess = abs(a2) - expected
    tot_begin = INET_YE25
    tot_rate = loss_rate(-120, tot_begin)
    tot_expected = b2 * tot_begin
    tot_excess = 120 - tot_expected

    core_begin = CHTR_CR_YE25 - RURAL_CR_YE25
    core_add = CHTR_CR_ADD_Q1 - RURAL_CR_ADD_Q1
    core_rate = loss_rate(core_add, core_begin)

    att_pass = PASSINGS_Q1 * ATT_FTTH
    att_cust = att_pass * PEN_CR_Q1
    conc_rate = 120 / att_cust
    prop_losses = 120 * ATT_FTTH

    avg_inet = (INET_YE24 + INET_YE25) / 2
    arpu_y = INET_REV_FY25 * 1000 / avg_inet  # $ per sub-year
    excess_rev = excess * arpu_y / 1000  # $M  (excess is thousands)

    field_care_yoy = (FIELD_Q1_26 + CARE_Q1_26) - (FIELD_Q1_25 + CARE_Q1_25)
    upg_yoy = UPG_Q1_26 / UPG_Q1_25 - 1

    committed_ratio = 1.8  # rounded down from 1.87
    committed_excess = 54  # rounded down from 54.4k

    rows = [
        ("A1", "CHTR res. Internet YE2025 (Q1 begin)", f"{a1:,}k", "RETRIEVED 10-K/Ex99.1"),
        ("A2", "CHTR res. Internet Q1'26 adds", f"{a2:,}k", "RETRIEVED Ex99.1"),
        ("A3", "A2/A1 CHTR res. net-loss rate", f"{100*a3:.2f}%", "derived"),
        ("B1", "CMCSA resid. BB Q1'26 begin", f"{b1:,}k", "RETRIEVED Ex99.1"),
        ("B2", "CMCSA Q1'26 net-loss rate", f"{100*b2:.2f}%", "derived"),
        ("C3", "A3/B2 rate ratio (unrounded)", f"{ratio:.2f}x", "derived"),
        ("C4", "Committed ratio (round down)", f"{committed_ratio:.1f}x", "commit"),
        ("C5", "B2*A1 expected CHTR res. losses", f"{expected:.1f}k", "derived"),
        ("C6", "|A2|-C5 excess vs peer rate", f"{excess:.1f}k", "derived"),
        ("C7", "Committed excess (round down)", f"{committed_excess}k", "commit"),
        ("D1", "CHTR res. Q1'25 net-loss rate", f"{100*c2:.2f}%", "derived"),
        ("D2", "CMCSA Q1'25 net-loss rate", f"{100*d2:.2f}%", "derived"),
        ("E1", "Core CR begin (co - rural YE25)", f"{core_begin:,}k", "derived"),
        ("E2", "Core CR Q1 adds (-163-41)", f"{core_add}k", "derived"),
        ("E3", "Core CR net-loss rate", f"{100*core_rate:.2f}%", "derived"),
        ("F1", "AT&T FTTH share of footprint", f"{100*ATT_FTTH:.0f}%", "RETRIEVED 10-K"),
        ("F2", "F1*passings*company pen (est. cust)", f"{att_cust:,.0f}k", "ESTIMATED pen"),
        ("F3", "If all -120k in F2, overlap rate", f"{100*conc_rate:.2f}%", "scenario"),
        ("F4", "Proportional AT&T share of -120k", f"{prop_losses:.0f}k", "scenario"),
        ("G1", "Field+care opex YoY $M", f"{field_care_yoy:+.0f}", "RETRIEVED Ex99.1"),
        ("G2", "Upgrade/rebuild capex YoY", f"{100*upg_yoy:.0f}%", "RETRIEVED"),
        ("H1", "FY25 Internet $/sub-year", f"${arpu_y:,.0f}", "derived"),
        ("H2", "C7*H1 annual Internet $ of excess", f"${excess_rev:.0f}M", "derived"),
        ("I1", "CHTR total Internet Q1 rate", f"{100*tot_rate:.2f}%", "derived"),
        ("I2", "Total excess vs CMCSA rate", f"{tot_excess:.1f}k", "derived"),
        ("J1", "CMCSA BB pen of resid. passings", f"{100*CMCSA_PEN_Q1_26:.1f}%", "RETRIEVED"),
        ("J2", "CHTR CR pen of passings", f"{100*PEN_CR_Q1:.1f}%", "RETRIEVED (not same def)"),
    ]
    for rid, label, val, tag in rows:
        print(f"{rid:<4} {label:<48} {val:>12}  {tag}")

    print()
    print("HEADLINE")
    print(
        f"  Q1 residential Internet net-loss rate {100*a3:.2f}% vs Comcast {100*b2:.2f}% "
        f"= {ratio:.2f}x unrounded; commit {committed_ratio:.1f}x (round down)."
    )
    print(
        f"  Excess vs peer rate: {excess:.1f}k; commit {committed_excess}k. "
        f"Annual Internet $ of that cohort ~${excess_rev:.0f}M."
    )
    print(
        f"  A year earlier Charter was better on rate ({100*c2:.2f}% vs {100*d2:.2f}%). "
        f"Comcast cut its loss rate; Charter's doubled."
    )
    assert committed_excess <= excess + 0.01
    assert committed_ratio <= ratio + 0.001
    print("OK — committed figures round against the 'Charter is worse' claim.")


if __name__ == "__main__":
    main()
