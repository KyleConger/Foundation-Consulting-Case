"""
Charter product-mix shift over time.

ACCURATE for: disclosed 1/2/3+ residential penetration, product
  customer counts, residential and company revenue mix, programming
  expense as a video-volume cross-check.
NOT ACCURATE for: which two products sit in the 2-product bucket,
  gross adds vs disconnects, product-level EBITDA, a churn rate.

Recomputes the canvas arithmetic. Run:
  python Analysis/product_mix_model.py

Sources: FY2025 trending (restated), Ex99.1 Q1 2026, Ex99.1 Q2 2026.
Q2 2026 is a later public fact after the Q1 assignment anchor.
Do not mix pre-Q4 2025 customer methodology.
"""

from __future__ import annotations

QTRS = [
    "23Q1",
    "23Q2",
    "23Q3",
    "23Q4",
    "24Q1",
    "24Q2",
    "24Q3",
    "24Q4",
    "25Q1",
    "25Q2",
    "25Q3",
    "25Q4",
    "26Q1",
    "26Q2",
]

# --- RETRIEVED: residential CR (000s), restated incl. mobile-only ---
RES_CR = [
    30310,
    30382,
    30440,
    30379,
    30312,
    30192,
    30114,
    29964,
    29914,
    29819,
    29734,
    29609,
    29452,
    29276,
]

# --- RETRIEVED: residential 1 / 2 / 3+ product penetration (%) ---
P1 = [46.6, 46.7, 47.2, 47.5, 48.2, 48.7, 49.0, 48.8, 48.9, 48.7, 48.5, 48.0, 47.7, 47.4]
P2 = [32.5, 32.6, 32.6, 32.6, 32.5, 32.6, 32.7, 33.1, 33.4, 33.8, 34.1, 34.5, 34.8, 35.1]
P3 = [20.9, 20.7, 20.2, 19.9, 19.3, 18.8, 18.3, 18.0, 17.7, 17.5, 17.4, 17.5, 17.5, 17.6]

# --- RETRIEVED: residential product units (000s) ---
RES_INET = [
    28479,
    28549,
    28606,
    28544,
    28472,
    28318,
    28205,
    28034,
    27979,
    27868,
    27760,
    27641,
    27524,
    27358,
]
RES_MOB_LINES = [
    5781,
    6408,
    6984,
    7514,
    7984,
    8518,
    9039,
    9543,
    10031,
    10502,
    10964,
    11370,
    11714,
    12099,
]
RES_VID = [
    14260,
    14071,
    13751,
    13503,
    13111,
    12718,
    12437,
    12327,
    12160,
    12087,
    12023,
    12072,
    12021,
    12010,
]
RES_VOICE = [
    7473,
    7248,
    6960,
    6712,
    6438,
    6170,
    5895,
    5636,
    5372,
    5161,
    4967,
    4832,
    4665,
    4494,
]
RES_CONN = [
    28810,
    28938,
    29052,
    29038,
    29007,
    28917,
    28878,
    28763,
    28758,
    28705,
    28658,
    28563,
    28446,
    28306,
]

# --- RETRIEVED: residential product revenue ($M) ---
REV_INET = [5718, 5733, 5776, 5805, 5826, 5806, 5872, 5856, 5930, 5969, 5971, 5895, 5852, 5776]
REV_MOB = [497, 539, 581, 626, 685, 737, 801, 860, 914, 921, 954, 973, 1052, 1095]
REV_VID = [4254, 4189, 4005, 3905, 3909, 3868, 3736, 3616, 3580, 3488, 3389, 3246, 3252, 3149]
REV_VOICE = [373, 365, 379, 393, 374, 350, 360, 353, 356, 346, 332, 316, 338, 331]
REV_RES = [10842, 10826, 10741, 10729, 10794, 10761, 10769, 10685, 10780, 10724, 10646, 10430, 10494, 10351]
REV_TOT = [13653, 13659, 13584, 13711, 13679, 13685, 13795, 13926, 13735, 13766, 13672, 13601, 13597, 13526]
REV_CONN = [6215, 6272, 6357, 6431, 6511, 6543, 6673, 6716, 6844, 6890, 6925, 6868, 6904, 6871]

# --- RETRIEVED: programming expense ($M). 26Q1 = H1 4123 − Q2 2035 ---
PROG = [2799, 2740, 2595, 2504, 2570, 2472, 2336, 2275, 2302, 2253, 2184, 2083, 2088, 2035]

# Seamless entertainment allocation netted in video revenue AND programming.
# 23Q1–25Q2 not disclosed as a quarterly series here; material from late 2025.
ALLOC_26Q1 = (218, 47)  # 26 vs 25
ALLOC_26Q2 = (251, 67)

RES_ARPU = [
    119.39,
    118.91,
    117.71,
    117.64,
    118.53,
    118.60,
    119.02,
    118.65,
    120.07,
    119.70,
    119.16,
    117.19,
    118.44,
    117.52,
]


def pct(part: float, whole: float) -> float:
    return 100.0 * part / whole


def households(pen_pct: list[float], cr: list[int]) -> list[float]:
    return [p / 100.0 * c for p, c in zip(pen_pct, cr)]


def products_per_cr(p1: float, p2: float, p3: float, three_as: float = 3.0) -> float:
    return (1 * p1 + 2 * p2 + three_as * p3) / 100.0


def main() -> None:
    i0, i1 = 0, -1  # 23Q1, 26Q2
    i_peak_1p = P1.index(max(P1))
    i_q1 = QTRS.index("26Q1")

    h1 = households(P1, RES_CR)
    h2 = households(P2, RES_CR)
    h3 = households(P3, RES_CR)

    print("=" * 72)
    print("BUILD 1 — residential bundle mix (penetration × CR)")
    print("=" * 72)
    print(f"  1-product {P1[i0]:.1f}% → {P1[i1]:.1f}%  ({P1[i1] - P1[i0]:+.1f} ppt)")
    print(f"            peak {P1[i_peak_1p]:.1f}% in {QTRS[i_peak_1p]}, then {P1[i_peak_1p] - P1[i1]:.1f} ppt reverse")
    print(f"  2-product {P2[i0]:.1f}% → {P2[i1]:.1f}%  ({P2[i1] - P2[i0]:+.1f} ppt)")
    print(f"  3-or-more {P3[i0]:.1f}% → {P3[i1]:.1f}%  ({P3[i1] - P3[i0]:+.1f} ppt)")
    print()
    print(f"  1P households {h1[i0]:,.1f}k → {h1[i1]:,.1f}k  ({h1[i1] - h1[i0]:+,.1f}k)")
    print(f"  2P households {h2[i0]:,.1f}k → {h2[i1]:,.1f}k  ({h2[i1] - h2[i0]:+,.1f}k)")
    print(f"  3+ households {h3[i0]:,.1f}k → {h3[i1]:,.1f}k  ({h3[i1] - h3[i0]:+,.1f}k)")
    cr_delta = RES_CR[i1] - RES_CR[i0]
    print(f"  Res CR        {RES_CR[i0]:,}k → {RES_CR[i1]:,}k  ({cr_delta:+,}k)")
    print(f"  3+ loss vs CR loss: {h3[i1] - h3[i0]:,.1f}k vs {cr_delta:+,}k")
    print(f"  2P added while CR shrank: {h2[i1] - h2[i0]:+,.1f}k")

    # Q1 assignment-anchor cut
    print()
    print(f"  Q1'26 anchor: 2P {P2[i_q1]:.1f}% ({P2[i_q1] - P2[i0]:+.1f} ppt vs 23Q1)")
    print(f"                3+ {P3[i_q1]:.1f}% ({P3[i_q1] - P3[i0]:+.1f} ppt)")
    print(f"                2P hh {h2[i_q1]:,.1f}k ({h2[i_q1] - h2[i0]:+,.1f}k)")
    print(f"                3+ hh {h3[i_q1]:,.1f}k ({h3[i_q1] - h3[i0]:+,.1f}k)")

    ppc0 = products_per_cr(P1[i0], P2[i0], P3[i0], 3.0)
    ppc1 = products_per_cr(P1[i1], P2[i1], P3[i1], 3.0)
    print(f"  Products/CR (3+ counted as 3): {ppc0:.3f} → {ppc1:.3f} ({ppc1 - ppc0:+.3f})")
    ppc0b = products_per_cr(P1[i0], P2[i0], P3[i0], 3.2)
    ppc1b = products_per_cr(P1[i1], P2[i1], P3[i1], 3.2)
    print(f"  Products/CR (3+ counted as 3.2): {ppc0b:.3f} → {ppc1b:.3f} ({ppc1b - ppc0b:+.3f})")

    print()
    print("=" * 72)
    print("BUILD 2 — residential dollar mix (P&L shares)")
    print("=" * 72)
    for name, series in [
        ("Internet", REV_INET),
        ("Mobile", REV_MOB),
        ("Video", REV_VID),
        ("Voice", REV_VOICE),
    ]:
        s0, s1 = pct(series[i0], REV_RES[i0]), pct(series[i1], REV_RES[i1])
        d0, d1 = series[i0], series[i1]
        print(
            f"  {name:8s} ${d0:,}M → ${d1:,}M ({d1 - d0:+,}M)  "
            f"share {s0:.2f}% → {s1:.2f}% ({s1 - s0:+.2f} ppt)"
        )
    print(
        f"  Res tot  ${REV_RES[i0]:,}M → ${REV_RES[i1]:,}M ({REV_RES[i1] - REV_RES[i0]:+,}M)"
    )

    print()
    print("  Company-revenue shares")
    for name, series in [
        ("Internet", REV_INET),
        ("Mobile", REV_MOB),
        ("Video", REV_VID),
        ("Connectivity", REV_CONN),
    ]:
        s0, s1 = pct(series[i0], REV_TOT[i0]), pct(series[i1], REV_TOT[i1])
        print(f"    {name:12s} {s0:.2f}% → {s1:.2f}% ({s1 - s0:+.2f} ppt)")

    # Connectivity first crossed 50%
    conn_share = [pct(c, t) for c, t in zip(REV_CONN, REV_TOT)]
    first_50 = next(i for i, s in enumerate(conn_share) if s >= 50.0)
    print(f"  Connectivity first ≥50% of company revenue: {QTRS[first_50]} ({conn_share[first_50]:.2f}%)")
    print(f"  26Q2 connectivity share: {conn_share[i1]:.2f}%")
    print(f"  26Q1 connectivity share: {conn_share[i_q1]:.2f}%")

    print()
    print("=" * 72)
    print("RECONCILE — direction only; no shared identity")
    print("=" * 72)
    print("  Build 1: 3+ mix and 3+ households down; 2P mix and 2P households up.")
    print("  Build 2: video $ share down; mobile $ share up.")
    print("  Agreement is two filing tables pointing the same way, not validation")
    print("  that 2-product = Internet+Mobile (not disclosed).")

    print()
    print("=" * 72)
    print("CROSS-CHECK — programming expense (cost account, not P&L mix %)")
    print("=" * 72)
    print(f"  Programming ${PROG[i0]:,}M → ${PROG[i1]:,}M ({PROG[i1] - PROG[i0]:+,}M, {pct(PROG[i1], PROG[i0]) - 100:+.1f}%)")
    print(f"  Video rev   ${REV_VID[i0]:,}M → ${REV_VID[i1]:,}M ({REV_VID[i1] - REV_VID[i0]:+,}M, {pct(REV_VID[i1], REV_VID[i0]) - 100:+.1f}%)")
    vid_cust = [14260 + 606, 12010 + 514]  # 23Q1 / 26Q2 total video from trending + Q2
    # Use total video if we have it — residential + SMB
    tot_vid_23q1 = 14906
    tot_vid_26q2 = 12524
    print(f"  Video cust  {tot_vid_23q1:,}k → {tot_vid_26q2:,}k ({tot_vid_26q2 - tot_vid_23q1:+,}k, {pct(tot_vid_26q2, tot_vid_23q1) - 100:+.1f}%)")

    # Add back Q2'26 allocation; 23Q1 allocation not disclosed — treat as 0 (ESTIMATED)
    vid_gross_26q2 = REV_VID[i1] + ALLOC_26Q2[0]
    prog_gross_26q2 = PROG[i1] + ALLOC_26Q2[0]
    print(f"  Video $ + Q2'26 alloc ${vid_gross_26q2:,}M vs 23Q1 ${REV_VID[i0]:,}M ({vid_gross_26q2 - REV_VID[i0]:+,}M, {pct(vid_gross_26q2, REV_VID[i0]) - 100:+.1f}%)")
    print(f"  Prog  $ + Q2'26 alloc ${prog_gross_26q2:,}M vs 23Q1 ${PROG[i0]:,}M ({prog_gross_26q2 - PROG[i0]:+,}M, {pct(prog_gross_26q2, PROG[i0]) - 100:+.1f}%)")
    print("  23Q1 allocation treated as $0 — ESTIMATED (App Store Oct 2025).")

    print()
    print("=" * 72)
    print("ATTACH RATES (derived from retrieved ÷ retrieved)")
    print("=" * 72)
    v_att0 = pct(RES_VID[i0], RES_INET[i0])
    v_att1 = pct(RES_VID[i1], RES_INET[i1])
    m_line0 = RES_MOB_LINES[i0] / RES_INET[i0]
    m_line1 = RES_MOB_LINES[i1] / RES_INET[i1]
    voice0 = pct(RES_VOICE[i0], RES_INET[i0])
    voice1 = pct(RES_VOICE[i1], RES_INET[i1])
    print(f"  Video / Internet     {v_att0:.1f}% → {v_att1:.1f}% ({v_att1 - v_att0:+.1f} ppt)")
    print(f"  Voice / Internet     {voice0:.1f}% → {voice1:.1f}% ({voice1 - voice0:+.1f} ppt)")
    print(f"  Mobile lines / Inet  {m_line0:.3f} → {m_line1:.3f} ({m_line1 - m_line0:+.3f})")
    mob_only0 = RES_CONN[i0] - RES_INET[i0]
    mob_only1 = RES_CONN[i1] - RES_INET[i1]
    print(f"  Mobile-only (conn − inet) {mob_only0:,}k → {mob_only1:,}k")

    print()
    print("=" * 72)
    print("IDENTITIES")
    print("=" * 72)
    for i, q in enumerate(QTRS):
        s_pen = P1[i] + P2[i] + P3[i]
        s_rev = REV_INET[i] + REV_MOB[i] + REV_VID[i] + REV_VOICE[i]
        ok_pen = abs(s_pen - 100.0) < 0.15
        ok_rev = s_rev == REV_RES[i]
        if not ok_pen or not ok_rev or q in ("23Q1", "24Q3", "26Q1", "26Q2"):
            print(
                f"  {q} pen {s_pen:.1f}%  res products ${s_rev} vs ${REV_RES[i]} "
                f"{'OK' if ok_rev else 'GAP ' + str(s_rev - REV_RES[i])}"
            )

    print()
    print("=" * 72)
    print("CHANNEL CONTRIBUTION — can mix close the Internet print?")
    print("=" * 72)
    inet_26q1 = REV_INET[i_q1]
    tot_26q1 = REV_TOT[i_q1]
    print(f"  Internet is {pct(inet_26q1, tot_26q1):.1f}% of Q1'26 company revenue (${inet_26q1}M / ${tot_26q1}M)")
    print(f"  Q1'26 Internet $ {REV_INET[i_q1] - REV_INET[QTRS.index('25Q1')]:+}M YoY")
    print(f"  Q1'26 Mobile   $ {REV_MOB[i_q1] - REV_MOB[QTRS.index('25Q1')]:+}M YoY")
    print(f"  Q2'26 Internet $ {REV_INET[i1] - REV_INET[QTRS.index('25Q2')]:+}M YoY")
    print(f"  Q2'26 Mobile   $ {REV_MOB[i1] - REV_MOB[QTRS.index('25Q2')]:+}M YoY")
    print("  Mobile $ fills connectivity subtotal; does not re-rate the Internet print (Root C).")

    print()
    print("=" * 72)
    print("PHASES")
    print("=" * 72)
    print("  Phase 1 23Q1–24Q3: 1P 46.6→49.0 (unbundle); 2P flat 32.5–32.7; 3+ 20.9→18.3")
    print("  Phase 2 24Q3–26Q2: 1P 49.0→47.4 (reattach); 2P 32.7→35.1 every quarter; 3+ 18.3→17.6 floor")

    print()
    print("=" * 72)
    print("ORIGIN WEIGHT")
    print("=" * 72)
    print("  Every mix % and every revenue $ in the headline is RETRIEVED.")
    print("  Household counts = disclosed % × disclosed CR (DERIVED).")
    print("  2-product = Internet+Mobile is INTERPRETIVE — not a filing fact.")
    print("  23Q1 seamless allocation = $0 is ESTIMATED.")

    print()
    print("=" * 72)
    print("HEADLINE CANDIDATES (round in the direction that costs you)")
    print("=" * 72)
    # 3+ loss 1,182k → claim 1.18M not 1.2M
    # 2P add 425k → claim 0.42M not 0.43M if we round down the add
    d3 = h3[i1] - h3[i0]
    d2 = h2[i1] - h2[i0]
    print(f"  3+ households {d3:,.1f}k → commit −1.18 million (not −1.2M)")
    print(f"  2P households {d2:,.1f}k → commit +0.42 million (round down)")
    print(f"  2P mix +{P2[i1] - P2[i0]:.1f} ppt; 3+ mix {P3[i1] - P3[i0]:+.1f} ppt")
    vshare0 = pct(REV_VID[i0], REV_RES[i0])
    vshare1 = pct(REV_VID[i1], REV_RES[i1])
    mshare0 = pct(REV_MOB[i0], REV_RES[i0])
    mshare1 = pct(REV_MOB[i1], REV_RES[i1])
    print(f"  Video share of res {vshare0:.2f}% → {vshare1:.2f}% ({vshare1 - vshare0:+.2f} ppt) → commit −8.8 ppt")
    print(f"  Mobile share of res {mshare0:.2f}% → {mshare1:.2f}% ({mshare1 - mshare0:+.2f} ppt) → commit +6.0 ppt")

    # dollar-weighted retrieved
    print()
    print(f"  Q2'26 residential $ {REV_RES[i1]}M: 100% retrieved.")
    print(f"  Estimated share of the dollar answer: 0%.")
    print("  The 2P composition (which two products) carries none of the $")
    print("  and all of the leverage on a GTM claim.")


if __name__ == "__main__":
    main()
