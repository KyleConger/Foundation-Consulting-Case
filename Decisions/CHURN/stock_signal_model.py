"""
If-lost-to-X stock signal — Root C (the tape prices the Internet print)
plus the CEO charge (share-price trajectory).

Question: if the material leak is identified AND the matching play works,
is the close large enough for investors to notice? Not a buy/sell. Not a
price target.

Recomputes Decisions/CHURN/ifxy-stock-signal.md and the chtr-ifix-y-stock-signal
canvas. Run:

  python "Decisions/CHURN/stock_signal_model.py"

Shared with network-churn / customer-performance (disclosed, not independent):
  peer net-loss rate (CMCSA domestic resid. BB), FY25 Internet $/sub,
  committed 54k excess (round down from 54.4k).
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# RETRIEVED inputs
# ---------------------------------------------------------------------------

# Internet net adds (000s) — Ex99.1 Q1 2026 / trending
CHTR_INET_Q1_26 = -120
CHTR_INET_Q1_25 = -59
CHTR_RES_INET_Q1_26 = -117
CHTR_RES_INET_YE25 = 27641  # Q1'26 begin
CHTR_SMB_INET_Q1_26 = -3

# CMCSA domestic residential broadband — Ex99.1 Q1 2026 (000s)
CMCSA_BB_EOP_Q1_26 = 28654
CMCSA_BB_ADD_Q1_26 = -65
CMCSA_BB_EOP_Q1_25 = 29190
CMCSA_BB_ADD_Q1_25 = -183

# Priced print — Ex99.1 Q1 2026 ($M except %)
INET_REV_Q1 = (5852, 5930)  # 2026, 2025
EBITDA_Q1 = (5637, 5763)
FCF_Q1 = (1372, 1564)
CAPEX_Q1 = (2855, 2399)

# FY25 Internet $/sub — 10-K / Ex99.1
INET_REV_FY25 = 23765  # $M
INET_YE24, INET_YE25 = 30083, 29680
FCF_FY25 = 5004  # $M

# Capex intensity — existing CMCSA C&P work (RETRIEVED filings)
CHTR_CAPEX_PCT_REV_FY25 = 21.3
CMCSA_CP_CAPEX_PCT_REV = 10.8

# Stock path — Team Case Brief (assignment language, not a filing)
STOCK_5Y_PCT = 80  # "roughly 80%"
STOCK_1D_PCT = 25  # "about 25%" in one day after Q1

# Rural / remainder — existing conversion work (derived from retrieved)
RURAL_CR_Q1 = 41
RURAL_REMAINDER_LOW = 120  # k lifetime at stuck 38% take
RURAL_REMAINDER_HIGH = 170  # k at company 54% take

# Q2 2026 later public fact — Ex99.1 Q2; does not replace Q1 anchor
Q2_INET_ADD = -172

# Commits reused from network-churn (round against "Charter is worse")
COMMITTED_EXCESS = 54  # k; unrounded 54.4
COMMITTED_RATIO = 1.8  # unrounded 1.87
COMMITTED_EXCESS_REV_M = 43  # $M/yr; network-churn H2 on unrounded excess × FY25 $/sub


def yoy_pct(new: float, old: float) -> float:
    return (new / old - 1.0) * 100.0


def loss_rate(add: int, begin: int) -> float:
    return abs(add) / begin


def main() -> None:
    rows: list[tuple[str, str, str, str]] = []

    def add(rid: str, label: str, val: str, tag: str) -> None:
        rows.append((rid, label, val, tag))

    # ----- Frame 1: the print that was priced -----
    yoy_slope = CHTR_INET_Q1_26 - CHTR_INET_Q1_25  # −61
    priced_deterioration = abs(yoy_slope)  # 61k
    inet_pct = yoy_pct(INET_REV_Q1[0], INET_REV_Q1[1])
    ebitda_pct = yoy_pct(EBITDA_Q1[0], EBITDA_Q1[1])
    fcf_pct = yoy_pct(FCF_Q1[0], FCF_Q1[1])
    capex_pct = yoy_pct(CAPEX_Q1[0], CAPEX_Q1[1])
    fcf_hole = FCF_Q1[1] - FCF_Q1[0]  # 192
    capex_delta = CAPEX_Q1[0] - CAPEX_Q1[1]  # 456
    midpoint_print = (CHTR_INET_Q1_26 + CHTR_INET_Q1_25) / 2.0  # −89.5
    # Material bar: closer to last year (−59) than to Q1 (−120).
    # Need print > midpoint (less negative). Close at least 120 − 89.5 = 30.5k.
    # Round against "it matters": require 31k.
    material_close_k = 31
    material_print = CHTR_INET_Q1_26 + material_close_k  # −89

    add("A1", "Q1'26 total Internet net adds", f"{CHTR_INET_Q1_26}k", "RETRIEVED Ex99.1")
    add("A2", "Q1'25 total Internet net adds", f"{CHTR_INET_Q1_25}k", "RETRIEVED Ex99.1")
    add("A3", "A1-A2 YoY Internet slope (priced surprise)", f"{yoy_slope}k", "derived")
    add("A4", "Priced deterioration |A3|", f"{priced_deterioration}k", "derived")
    add("A5", "Internet $ YoY %", f"{inet_pct:.1f}%", "RETRIEVED/derived Ex99.1")
    add("A6", "Adj. EBITDA YoY %", f"{ebitda_pct:.1f}%", "RETRIEVED/derived")
    add("A7", "FCF YoY %", f"{fcf_pct:.1f}%", "RETRIEVED/derived")
    add("A8", "Capex YoY %", f"{capex_pct:.1f}%", "RETRIEVED/derived")
    add("A9", "One-day share-price drop after Q1", f"~{STOCK_1D_PCT}%", "RETRIEVED Team Case Brief")
    add("A10", "Five-year share-price loss", f"~{STOCK_5Y_PCT}%", "RETRIEVED Team Case Brief")
    add("A11", "Midpoint print (-120 vs -59)", f"{midpoint_print:.1f}k", "derived")
    add("A12", "Material-close bar (round against)", f"{material_close_k}k → {material_print}k print", "commit")

    # ----- Frame 2: what the playbook can close -----
    cmcsa_begin = CMCSA_BB_EOP_Q1_26 - CMCSA_BB_ADD_Q1_26
    cmcsa_rate = loss_rate(CMCSA_BB_ADD_Q1_26, cmcsa_begin)
    chtr_rate = loss_rate(CHTR_RES_INET_Q1_26, CHTR_RES_INET_YE25)
    ratio = chtr_rate / cmcsa_rate
    expected_res = cmcsa_rate * CHTR_RES_INET_YE25
    excess_unrounded = abs(CHTR_RES_INET_Q1_26) - expected_res
    close_k = COMMITTED_EXCESS
    print_res = CHTR_RES_INET_Q1_26 + close_k  # −63
    print_tot = CHTR_INET_Q1_26 + close_k  # −66  (SMB −3 held)
    half_close = close_k // 2  # 27; round against
    print_half = CHTR_INET_Q1_26 + half_close  # −93
    close_to_q125 = abs(CHTR_INET_Q1_26 - CHTR_INET_Q1_25)  # 61
    close_to_zero = abs(CHTR_INET_Q1_26)  # 120
    shortfall_vs_q125 = close_to_q125 - close_k  # 7

    avg_inet = (INET_YE24 + INET_YE25) / 2.0
    arpu_y = INET_REV_FY25 * 1000.0 / avg_inet  # $/sub-year
    excess_rev_unrounded = excess_unrounded * arpu_y / 1000.0  # $M
    excess_rev_on_commit = close_k * arpu_y / 1000.0

    add("B1", "CMCSA resid. BB Q1'26 begin", f"{cmcsa_begin:,}k", "RETRIEVED Ex99.1")
    add("B2", "CMCSA Q1'26 net-loss rate", f"{100 * cmcsa_rate:.2f}%", "derived")
    add("B3", "CHTR res. Internet Q1'26 net-loss rate", f"{100 * chtr_rate:.2f}%", "derived")
    add("B4", "Rate ratio unrounded", f"{ratio:.2f}x", "derived · shared w/ network-churn")
    add("B5", "Committed ratio (round down)", f"{COMMITTED_RATIO:.1f}x", "commit · shared")
    add("B6", "Expected CHTR res. losses at CMCSA rate", f"{expected_res:.1f}k", "derived")
    add("B7", "Excess vs peer rate unrounded", f"{excess_unrounded:.1f}k", "derived")
    add("B8", "Committed excess (round down)", f"{close_k}k", "commit · shared")
    add("B9", "FY25 Internet $/sub-year", f"${arpu_y:,.0f}", "derived · shared")
    add("B10", "B7×B9 annual Internet $ unrounded", f"${excess_rev_unrounded:.1f}M", "derived")
    add("B11", "Committed excess $ (network-churn H2)", f"${COMMITTED_EXCESS_REV_M}M/yr", "commit · shared")
    add("B12", "B8×B9 on committed 54k", f"${excess_rev_on_commit:.1f}M", "derived")

    add("C1", "Playbook best: Q1 print + 54k close (total Internet)", f"{print_tot}k", "derived")
    add("C2", "Playbook best: residential Internet print", f"{print_res}k", "derived")
    add("C3", "Half excess (round against) print", f"{print_half}k", "derived")
    add("C4", "Close needed to match Q1'25 (-59k)", f"{close_to_q125}k", "derived")
    add("C5", "Close needed to reach zero net adds", f"{close_to_zero}k", "derived")
    add("C6", "Shortfall vs Q1'25 after 54k close", f"{shortfall_vs_q125}k", "derived")
    add("C7", "SMB Internet held at Q1", f"{CHTR_SMB_INET_Q1_26}k", "RETRIEVED · shared identity")

    # ----- Cross-check 1: fraction of the priced 61k slope (no $/sub) -----
    frac_priced = close_k / priced_deterioration
    frac_priced_pct = int(frac_priced * 100)  # 88; truncates against "covers the tape"
    frac_zero = close_k / close_to_zero
    add("D1", "54k / 61k share of priced YoY slope", f"{100 * frac_priced:.1f}%", "derived · no $/sub")
    add("D2", "Committed share of priced slope (trunc.)", f"{frac_priced_pct}%", "commit")
    add("D3", "54k / 120k share of path to zero", f"{100 * frac_zero:.0f}%", "derived")

    # ----- Cross-check 2: FCF dollars, not the net-add identity -----
    qtr_rev_of_close = COMMITTED_EXCESS_REV_M / 4.0
    fcf_share_q1 = COMMITTED_EXCESS_REV_M / FCF_Q1[0] * 100.0
    fcf_share_fy = COMMITTED_EXCESS_REV_M / FCF_FY25 * 100.0
    qtr_vs_fcf_hole = qtr_rev_of_close / fcf_hole * 100.0
    add("E1", "Q1 FCF $M", f"${FCF_Q1[0]:,}", "RETRIEVED Ex99.1")
    add("E2", "Q1 FCF hole vs Q1'25 $M", f"${fcf_hole}", "derived")
    add("E3", "Q1 capex increment $M", f"${capex_delta}", "derived")
    add("E4", "$43M / Q1 FCF", f"{fcf_share_q1:.1f}%", "derived · independent of 61k slope")
    add("E5", "$43M / FY25 FCF", f"{fcf_share_fy:.2f}%", "derived")
    add("E6", "Quarterly $ of 54k (~$11M) / FCF hole", f"{qtr_vs_fcf_hole:.1f}%", "derived")
    add("E7", "Capex increment / FCF hole", f"{capex_delta / fcf_hole:.1f}x", "derived")

    # ----- Rural / peer slope gap (cannot close) -----
    cmcsa_yoy = CMCSA_BB_ADD_Q1_26 - CMCSA_BB_ADD_Q1_25  # +118
    slope_gap = abs(yoy_slope) + cmcsa_yoy  # 61+118 = 179
    frac_gap = close_k / slope_gap
    frac_gap_pct = int(frac_gap * 100)  # 30
    add("F1", "CMCSA BB YoY (Q1'26 - Q1'25)", f"{cmcsa_yoy:+}k", "RETRIEVED")
    add("F2", "Peer YoY slope gap |A3|+F1", f"{slope_gap}k", "derived · rural-conversion identity")
    add("F3", "54k / 179k of peer slope gap", f"{frac_gap_pct}%", "commit trunc.")
    add("F4", "Rural CR Q1 (wrong unit)", f"+{RURAL_CR_Q1}k", "RETRIEVED · cannot close F2")
    add("F5", "Rural remainder lifetime stock", f"{RURAL_REMAINDER_LOW}-{RURAL_REMAINDER_HIGH}k", "derived · existing")

    # ----- Capex intensity still sits -----
    intensity_ratio = CHTR_CAPEX_PCT_REV_FY25 / CMCSA_CP_CAPEX_PCT_REV
    add("G1", "CHTR FY25 capex / revenue", f"{CHTR_CAPEX_PCT_REV_FY25}%", "RETRIEVED · shared capex work")
    add("G2", "CMCSA C&P capex / C&P revenue", f"{CMCSA_CP_CAPEX_PCT_REV}%", "RETRIEVED · shared")
    add("G3", "Intensity ratio", f"{intensity_ratio:.2f}x (~2×)", "derived")

    # ----- Q2 later fact -----
    q2_after_close = Q2_INET_ADD + close_k  # −118
    add("H1", "Q2 Internet net adds (later fact)", f"{Q2_INET_ADD}k", "RETRIEVED Ex99.1 Q2 · later")
    add("H2", "Q2 print after 54k close", f"{q2_after_close}k", "derived · still Q1-like")

    # ----- Revealed sensitivity identity (NOT a target) -----
    ppt_per_k = STOCK_1D_PCT / priced_deterioration
    naive_reverse = ppt_per_k * close_k
    add("I1", "Revealed ppt per 1k YoY Internet (25/61)", f"{ppt_per_k:.3f} ppt", "identity · NOT a forecast")
    add("I2", "Naive 54×I1 (do not use as a target)", f"{naive_reverse:.1f} ppt", "do not claim")

    # ----- Dollar-weighted origin of the $43M -----
    # Every dollar in $43M is retrieved Internet $ × retrieved bases × derived rate.
    # Closability (the play works) is ESTIMATED and carries 100% of Frame 2 leverage.
    add("J1", "$43M arithmetic retrieved-anchored", "100%", "FY25 $ and bases from filings")
    add("J2", "Closability of 54k", "ESTIMATED", "play works · 100% of Frame 2 leverage")
    add("J3", "Priced 61k slope retrieved-weighted", "100%", "A1 and A2 both Ex99.1")

    print("ID  Line                                              Value                    Tag")
    print("-" * 96)
    for rid, label, val, tag in rows:
        print(f"{rid:<4} {label:<48} {val:>18}  {tag}")

    # ----- commits -----
    committed_print = print_tot  # −66
    committed_range = (print_half, print_tot)  # −93 to −66
    verdict_matter = (
        abs(committed_print) < abs(midpoint_print)
        and close_k >= material_close_k
        and frac_priced_pct >= 80
    )
    verdict_rerate = False  # never from this close alone

    print()
    print("HEADLINE")
    print(
        f"  MATTER vs Q1 tape: YES, if the full {close_k}k peer excess closes "
        f"(subsequent quarterly Internet print {committed_print}k vs sold "
        f"{CHTR_INET_Q1_26}k). Half a close ({print_half}k) still looks like Q1."
    )
    print(
        f"  RE-RATE five-year ~{STOCK_5Y_PCT}%: NO. Capex still ~2× CMCSA C&P; "
        f"${COMMITTED_EXCESS_REV_M}M/yr is {fcf_share_q1:.1f}% of Q1 FCF "
        f"${FCF_Q1[0]/1000:.2f}B; rural remainder cannot close a {slope_gap}k "
        f"quarterly peer gap."
    )
    print(
        f"  Point estimate {committed_print}k (range {committed_range[0]}k to "
        f"{committed_range[1]}k). Cannot claim {CHTR_INET_Q1_25}k (need "
        f"{close_to_q125}k) or 0 (need {close_to_zero}k)."
    )
    print(
        f"  Cross-check (no $/sub): {close_k}k is {frac_priced_pct}% of the "
        f"{priced_deterioration}k YoY slope the tape sold."
    )
    print(
        f"  Cross-check (no net-add identity): ${COMMITTED_EXCESS_REV_M}M is "
        f"{fcf_share_q1:.1f}% of Q1 FCF; quarterly ~${qtr_rev_of_close:.0f}M "
        f"is {qtr_vs_fcf_hole:.1f}% of the ${fcf_hole}M FCF hole. Capex "
        f"+${capex_delta}M is the cash print."
    )
    print(
        f"  Q2 later fact: {Q2_INET_ADD}k; 54k close would leave "
        f"{q2_after_close}k — still a Q1-like print if that is the run-rate."
    )

    print()
    print("KILL RULE")
    print(
        "  If the tracker fill shows the leak is move-out matching Comcast "
        "(industry housing), the playbook cannot produce a Charter-specific "
        "print the tape will pay for. Closable excess → 0."
    )
    print("UNWILLING")
    print("  Price target; mobile as offset; 2027 evolution alone re-rates; which X is largest.")

    # ----- asserts -----
    assert yoy_slope == -61
    assert priced_deterioration == 61
    assert abs(inet_pct - (-1.3)) < 0.05
    assert abs(ebitda_pct - (-2.2)) < 0.05
    assert abs(fcf_pct - (-12.3)) < 0.05
    assert abs(capex_pct - 19.0) < 0.05
    assert fcf_hole == 192
    assert capex_delta == 456
    assert COMMITTED_RATIO <= ratio + 0.001
    assert COMMITTED_EXCESS <= excess_unrounded + 0.01
    assert print_tot == -66
    assert print_res == -63
    assert print_half == -93
    assert close_to_q125 == 61
    assert close_to_zero == 120
    assert shortfall_vs_q125 == 7
    assert slope_gap == 179
    assert frac_priced_pct == 88
    assert frac_gap_pct == 30
    assert q2_after_close == -118
    assert FCF_Q1[0] == 1372
    assert abs(arpu_y - 795) < 1  # $795/sub-year
    assert 42.0 < excess_rev_on_commit < 44.0
    assert 43.0 < excess_rev_unrounded < 44.0
    assert verdict_matter is True
    assert verdict_rerate is False
    assert abs(committed_print) < abs(midpoint_print)
    assert abs(print_half) > abs(midpoint_print)  # half-close still repeat zone
    print()
    print("OK -- identities hold; -66k is on the last-year side of the midpoint; -93k is not.")
    print("OK — $43M is not the FCF story; 54k is 88% of the priced 61k slope.")

    print()
    print("CANVAS LOCKS")
    print(f"  priced_deterioration_k={priced_deterioration}")
    print(f"  material_close_k={material_close_k} material_print={material_print}")
    print(f"  committed_excess_k={close_k}")
    print(f"  committed_print_tot={print_tot} committed_print_res={print_res}")
    print(f"  range_low={print_half} range_high={print_tot}")
    print(f"  close_to_q125={close_to_q125} close_to_zero={close_to_zero}")
    print(f"  shortfall_vs_q125={shortfall_vs_q125}")
    print(f"  frac_priced_pct={frac_priced_pct}")
    print(f"  slope_gap={slope_gap} frac_gap_pct={frac_gap_pct}")
    print(f"  excess_rev_m={COMMITTED_EXCESS_REV_M}")
    print(f"  fcf_q1={FCF_Q1[0]} fcf_hole={fcf_hole} capex_delta={capex_delta}")
    print(f"  fcf_share_q1={fcf_share_q1:.1f} qtr_vs_fcf_hole={qtr_vs_fcf_hole:.1f}")
    print(f"  intensity_ratio={intensity_ratio:.2f}")
    print(f"  q2_after_close={q2_after_close}")
    print(f"  arpu_y={arpu_y:.0f}")
    print(f"  inet_pct={inet_pct:.1f} ebitda_pct={ebitda_pct:.1f} fcf_pct={fcf_pct:.1f} capex_pct={capex_pct:.1f}")
    print(f"  verdict_matter={verdict_matter} verdict_rerate={verdict_rerate}")
    print(f"  naive_reverse_ppt={naive_reverse:.1f}  # do not put on canvas as a target")


if __name__ == "__main__":
    main()
