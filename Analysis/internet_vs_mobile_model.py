"""
Internet vs mobile volumes, and implied Internet ARPU.

ACCURATE for: total Internet customers / net adds, total mobile lines /
  net adds, disclosed 10-K/10-Q Internet volume vs rate bridges.
DERIVED: monthly implied residential Internet ARPU
  = Internet revenue × 1000 / 3 / average residential Internet customers.
NOT ACCURATE for: a gig-tier list price, promotional stand-alone rate,
  product-level EBITDA, that bundled allocation is "price."

Run: python Analysis/internet_vs_mobile_model.py
"""

from __future__ import annotations

QTRS = [
    "23Q1", "23Q2", "23Q3", "23Q4",
    "24Q1", "24Q2", "24Q3", "24Q4",
    "25Q1", "25Q2", "25Q3", "25Q4",
    "26Q1", "26Q2",
]

# Total Internet customers / net adds (000s) — the operating print
INET_EOP = [30510, 30587, 30651, 30590, 30518, 30370, 30260, 30083, 30024, 29908, 29799, 29680, 29560, 29388]
INET_ADD = [76, 77, 64, -61, -72, -148, -110, -177, -59, -116, -109, -119, -120, -172]

# Total mobile lines / net adds (000s)
MOB_EOP = [5977, 6624, 7217, 7761, 8244, 8796, 9336, 9858, 10365, 10856, 11338, 11766, 12134, 12540]
MOB_ADD = [685, 647, 593, 544, 483, 552, 540, 522, 507, 491, 482, 428, 368, 406]

# Residential Internet for ARPU (revenue line is residential)
REV_INET = [5718, 5733, 5776, 5805, 5826, 5806, 5872, 5856, 5930, 5969, 5971, 5895, 5852, 5776]
RES_INET_EOP = [28479, 28549, 28606, 28544, 28472, 28318, 28205, 28034, 27979, 27868, 27760, 27641, 27524, 27358]
RES_INET_ADD = [67, 70, 57, -62, -72, -154, -113, -171, -55, -111, -108, -119, -117, -166]

REV_MOB = [497, 539, 581, 626, 685, 737, 801, 860, 914, 921, 954, 973, 1052, 1095]
RES_MOB_EOP = [5781, 6408, 6984, 7514, 7984, 8518, 9039, 9543, 10031, 10502, 10964, 11370, 11714, 12099]
RES_MOB_ADD = [665, 627, 576, 530, 470, 534, 521, 504, 488, 471, 462, 406, 344, 385]

# Disclosed blended residential ARPU — NOT Internet pricing
ARPU_RES = [119.39, 118.91, 117.71, 117.64, 118.53, 118.60, 119.02, 118.65, 120.07, 119.70, 119.16, 117.19, 118.44, 117.52]


def implied_arpu(rev_m: float, add_k: int, end_k: int) -> float:
    begin = end_k - add_k
    avg = (begin + end_k) / 2.0
    return rev_m * 1000.0 / 3.0 / avg


def _idx(q: str) -> int:
    return QTRS.index(q)


def verify_primary_sources() -> None:
    """Fail if a canvas input disagrees with PrimarySources originals.

    Hierarchy (CORE-INFORMATION): original Ex99.1 / 10-K / 10-Q beats the
    unofficial trending extract. Trending is used only where this pack has
    no Ex99.1 (23Q1–24Q3 customers; 23Q1–24Q3 quarterly Internet $).
    """
    # --- Ex99.1 Q2 2026 addendum (Jun 26 / Mar 26 / Dec 25 / Jun 25) ---
    assert INET_EOP[_idx("26Q2")] == 29388
    assert INET_EOP[_idx("26Q1")] == 29560
    assert INET_EOP[_idx("25Q4")] == 29680
    assert INET_EOP[_idx("25Q2")] == 29908
    assert INET_ADD[_idx("26Q2")] == -172
    assert INET_ADD[_idx("26Q1")] == -120
    assert INET_ADD[_idx("25Q4")] == -119
    assert INET_ADD[_idx("25Q2")] == -116
    assert MOB_EOP[_idx("26Q2")] == 12540
    assert MOB_EOP[_idx("26Q1")] == 12134
    assert MOB_EOP[_idx("25Q4")] == 11766
    assert MOB_EOP[_idx("25Q2")] == 10856
    assert MOB_ADD[_idx("26Q2")] == 406
    assert MOB_ADD[_idx("26Q1")] == 368
    assert MOB_ADD[_idx("25Q4")] == 428
    assert MOB_ADD[_idx("25Q2")] == 491
    assert RES_INET_EOP[_idx("26Q2")] == 27358
    assert RES_INET_EOP[_idx("26Q1")] == 27524
    assert RES_INET_ADD[_idx("26Q2")] == -166
    assert RES_INET_ADD[_idx("26Q1")] == -117
    assert RES_MOB_EOP[_idx("26Q2")] == 12099
    assert RES_MOB_EOP[_idx("26Q1")] == 11714
    assert RES_MOB_ADD[_idx("26Q2")] == 385
    assert RES_MOB_ADD[_idx("26Q1")] == 344
    assert ARPU_RES[_idx("26Q2")] == 117.52
    assert ARPU_RES[_idx("26Q1")] == 118.44
    assert ARPU_RES[_idx("25Q4")] == 117.19
    assert ARPU_RES[_idx("25Q2")] == 119.70
    assert REV_INET[_idx("26Q2")] == 5776  # Ex99.1 Q2 2026 P&L
    assert REV_INET[_idx("25Q2")] == 5969
    assert REV_MOB[_idx("26Q2")] == 1095
    assert REV_MOB[_idx("25Q2")] == 921

    # --- Ex99.1 Q1 2026 (Mar 26 / Dec 25 / Mar 25) ---
    assert INET_EOP[_idx("25Q1")] == 30024
    assert INET_ADD[_idx("25Q1")] == -59
    assert MOB_EOP[_idx("25Q1")] == 10365
    assert MOB_ADD[_idx("25Q1")] == 507
    assert RES_INET_EOP[_idx("25Q1")] == 27979
    assert RES_INET_ADD[_idx("25Q1")] == -55
    assert RES_MOB_EOP[_idx("25Q1")] == 10031
    assert RES_MOB_ADD[_idx("25Q1")] == 488
    assert ARPU_RES[_idx("25Q1")] == 120.07
    assert REV_INET[_idx("26Q1")] == 5852
    assert REV_INET[_idx("25Q1")] == 5930
    assert REV_MOB[_idx("26Q1")] == 1052
    assert REV_MOB[_idx("25Q1")] == 914

    # --- Ex99.1 FY2025 addendum (Dec 25 / Sep 25 / Dec 24) ---
    assert INET_EOP[_idx("25Q3")] == 29799
    assert INET_ADD[_idx("25Q3")] == -109
    assert INET_EOP[_idx("24Q4")] == 30083
    assert INET_ADD[_idx("24Q4")] == -177
    assert MOB_EOP[_idx("25Q3")] == 11338
    assert MOB_ADD[_idx("25Q3")] == 482
    assert MOB_EOP[_idx("24Q4")] == 9858
    assert MOB_ADD[_idx("24Q4")] == 522
    assert RES_INET_EOP[_idx("25Q4")] == 27641
    assert RES_INET_EOP[_idx("25Q3")] == 27760
    assert RES_INET_EOP[_idx("24Q4")] == 28034
    assert RES_INET_ADD[_idx("25Q4")] == -119
    assert RES_INET_ADD[_idx("25Q3")] == -108
    assert RES_INET_ADD[_idx("24Q4")] == -171
    assert ARPU_RES[_idx("25Q3")] == 119.16
    assert ARPU_RES[_idx("24Q4")] == 118.65
    assert REV_INET[_idx("25Q4")] == 5895
    assert REV_INET[_idx("24Q4")] == 5856
    assert REV_MOB[_idx("25Q4")] == 973
    assert REV_MOB[_idx("24Q4")] == 860

    # --- 10-K FY2025 annual Internet $ (beats trending FY sums) ---
    assert sum(REV_INET[_idx("25Q1") : _idx("25Q4") + 1]) == 23765
    assert sum(REV_INET[_idx("24Q1") : _idx("24Q4") + 1]) == 23360
    assert sum(REV_INET[_idx("23Q1") : _idx("23Q4") + 1]) == 23032
    assert sum(REV_MOB[_idx("25Q1") : _idx("25Q4") + 1]) == 3762
    assert sum(REV_MOB[_idx("24Q1") : _idx("24Q4") + 1]) == 3083
    assert sum(REV_MOB[_idx("23Q1") : _idx("23Q4") + 1]) == 2243

    # --- 10-Q / 10-K Internet $ YoY (retrieved rate/volume split is in the 10-Q text) ---
    assert (REV_INET[_idx("26Q1")] - REV_INET[_idx("25Q1")]) == -78  # 10-Q: −87 vol +9 rate
    assert (REV_INET[_idx("26Q2")] - REV_INET[_idx("25Q2")]) == -193  # 10-Q: −104 vol −89 rate
    assert (sum(REV_INET[_idx("25Q1") : _idx("25Q4") + 1])
            - sum(REV_INET[_idx("24Q1") : _idx("24Q4") + 1])) == 405  # 10-K: +785 rate −380 vol

    # --- Restated trending (no Ex99.1 in this pack for 23Q1–24Q3) ---
    trending_inet_eop = {
        "23Q1": 30510, "23Q2": 30587, "23Q3": 30651, "23Q4": 30590,
        "24Q1": 30518, "24Q2": 30370, "24Q3": 30260,
    }
    trending_inet_add = {
        "23Q1": 76, "23Q2": 77, "23Q3": 64, "23Q4": -61,
        "24Q1": -72, "24Q2": -148, "24Q3": -110,
    }
    trending_mob_eop = {
        "23Q1": 5977, "23Q2": 6624, "23Q3": 7217, "23Q4": 7761,
        "24Q1": 8244, "24Q2": 8796, "24Q3": 9336,
    }
    trending_mob_add = {
        "23Q1": 685, "23Q2": 647, "23Q3": 593, "23Q4": 544,
        "24Q1": 483, "24Q2": 552, "24Q3": 540,
    }
    for q, v in trending_inet_eop.items():
        assert INET_EOP[_idx(q)] == v, q
    for q, v in trending_inet_add.items():
        assert INET_ADD[_idx(q)] == v, q
    for q, v in trending_mob_eop.items():
        assert MOB_EOP[_idx(q)] == v, q
    for q, v in trending_mob_add.items():
        assert MOB_ADD[_idx(q)] == v, q

    # EOP identity from 23Q2 on (23Q1 add is vs undisclosed 22Q4)
    for i in range(1, len(QTRS)):
        assert INET_EOP[i] - INET_EOP[i - 1] == INET_ADD[i], QTRS[i]
        assert MOB_EOP[i] - MOB_EOP[i - 1] == MOB_ADD[i], QTRS[i]
        assert RES_INET_EOP[i] - RES_INET_EOP[i - 1] == RES_INET_ADD[i], QTRS[i]
        assert RES_MOB_EOP[i] - RES_MOB_EOP[i - 1] == RES_MOB_ADD[i], QTRS[i]

    print("verify_primary_sources: OK")


def main() -> None:
    verify_primary_sources()
    inet_arpu = [round(implied_arpu(r, a, e), 2) for r, a, e in zip(REV_INET, RES_INET_ADD, RES_INET_EOP)]
    mob_arpu = [round(implied_arpu(r, a, e), 2) for r, a, e in zip(REV_MOB, RES_MOB_ADD, RES_MOB_EOP)]
    print("implied residential Internet ARPU", inet_arpu)
    print("implied residential mobile ARPU  ", mob_arpu)
    peak_i = inet_arpu.index(max(inet_arpu))
    print(f"peak {inet_arpu[peak_i]} at {QTRS[peak_i]}")
    print(f"23Q1 {inet_arpu[0]} -> 26Q2 {inet_arpu[-1]} ({inet_arpu[-1] - inet_arpu[0]:+.2f})")
    yoy = [None] * 4 + [round(inet_arpu[i] - inet_arpu[i - 4], 2) for i in range(4, 14)]
    print("YoY implied Internet ARPU from 24Q1", yoy[4:])
    i25q3 = QTRS.index("25Q3")
    print(f"giveback from peak {inet_arpu[-1] - inet_arpu[i25q3]:+.2f}")
    print(f"Internet EOP {INET_EOP[0]} -> {INET_EOP[-1]} ({INET_EOP[-1] - INET_EOP[0]:+d}k)")
    print(f"Mobile   EOP {MOB_EOP[0]} -> {MOB_EOP[-1]} ({MOB_EOP[-1] - MOB_EOP[0]:+d}k)")
    print(f"index Inet 26Q2 {100 * INET_EOP[-1] / INET_EOP[0]:.1f}")
    print(f"index Mob  26Q2 {100 * MOB_EOP[-1] / MOB_EOP[0]:.1f}")
    # Q2 2026 official rate vs derived ARPU × base
    q2 = QTRS.index("26Q2")
    begin = RES_INET_EOP[q2] - RES_INET_ADD[q2]
    avg = (begin + RES_INET_EOP[q2]) / 2.0
    yoy_arpu = inet_arpu[q2] - inet_arpu[q2 - 4]
    implied_rate_m = yoy_arpu * 3 * avg / 1000.0
    print(f"Q2 YoY ARPU {yoy_arpu:+.2f} × 3 × avg {avg:.1f}k = ${implied_rate_m:.0f}M vs 10-Q rate −$89M")
    assert inet_arpu[QTRS.index("26Q1")] == 70.72
    assert yoy[-1] == -1.09


if __name__ == "__main__":
    main()
