"""
Customer performance by disclosed LOB — Q1 2026 assignment anchor.

ACCURATE for: ending customers, net adds, revenue, disclosed ARPU
  by Internet / mobile / video / voice / residential vs SMB vs
  mid-market & large / rural CR as a subset.
NOT ACCURATE for: gross churn, disconnect reasons, overlap-zip losses,
  retention quality. Filings do not disclose gross adds vs disconnects.
  A net-add analysis is not a churn analysis.

Recomputes the canvas / memo arithmetic. Run:
  python Decisions/customer_performance_model.py
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# RETRIEVED inputs (thousands of customers except $M and $ ARPU)
# Sources: Ex99.1 Q1 2026, 10-K FY2025, Q1 trending (restated basis).
# Do not mix pre-Q4 2025 customer methodology.
# ---------------------------------------------------------------------------

# Q1 2026 ending / YE2025 begin / Q1 2025 ending / YE2024 begin
RES_CR = dict(ye24=29964, q1_25=29914, ye25=29609, q1_26=29452)
SMB_CR = dict(ye24=2250, q1_25=2246, ye25=2237, q1_26=2231)
RES_INET = dict(ye24=28034, q1_25=27979, ye25=27641, q1_26=27524)
SMB_INET = dict(ye24=2049, q1_25=2045, ye25=2039, q1_26=2036)
TOT_INET = dict(ye24=30083, q1_25=30024, ye25=29680, q1_26=29560)
RES_MOB = dict(ye24=9543, q1_25=10031, ye25=11370, q1_26=11714)
SMB_MOB = dict(ye24=315, q1_25=334, ye25=396, q1_26=420)
TOT_MOB = dict(ye24=9858, q1_25=10365, ye25=11766, q1_26=12134)
RES_VID = dict(ye24=12327, q1_25=12160, ye25=12072, q1_26=12021)
SMB_VID = dict(ye24=565, q1_25=551, ye25=533, q1_26=524)
TOT_VID = dict(ye24=12892, q1_25=12711, ye25=12605, q1_26=12545)
RES_VOICE = dict(ye24=5636, q1_25=5372, ye25=4832, q1_26=4665)
SMB_VOICE = dict(ye24=1248, q1_25=1234, ye25=1214, q1_26=1207)
TOT_VOICE = dict(ye24=6884, q1_25=6606, ye25=6046, q1_26=5872)
MM_PSU = dict(ye24=340, q1_25=344, ye25=357, q1_26=360)

# Disclosed quarterly net adds (000s) — Q1 2026 / Q1 2025
Q1_26_ADDS = dict(
    res_cr=-157,
    smb_cr=-6,
    tot_cr=-163,
    res_inet=-117,
    smb_inet=-3,
    tot_inet=-120,
    res_mob=344,
    smb_mob=24,
    tot_mob=368,
    res_vid=-51,
    smb_vid=-9,
    tot_vid=-60,
    tot_voice=-174,
    mm_psu=3,
    rural_cr=41,
)
Q1_25_ADDS = dict(
    tot_inet=-59,
    res_inet=-55,
    tot_mob=507,
    tot_vid=-181,
    tot_voice=-278,
    tot_cr=-54,
    rural_cr=None,  # not used
)

# Revenue $M
REV_Q1 = {
    "internet": (5852, 5930),  # 2026, 2025
    "mobile": (1052, 914),
    "video": (3252, 3580),
    "voice": (338, 356),
    "residential": (10494, 10780),
    "smb": (1090, 1088),
    "mm": (749, 734),
    "ads": (358, 340),
    "other": (906, 793),
    "total": (13597, 13735),
}
REV_FY = {
    "internet": (23765, 23360),
    "mobile": (3762, 3083),
    "video": (13703, 15129),
    "voice": (1350, 1437),
    "residential": (42580, 43009),
    "smb": (4346, 4376),
    "mm": (2969, 2878),
    "total": (54774, 55085),
}

# FY2025 10-K MD&A bridges ($M) — RETRIEVED
FY25_INET_RATE_MIX = 785
FY25_INET_VOLUME = -380
FY25_MOB_VOLUME = 714
FY25_MOB_RATE = -35
FY25_VID_VOLUME = -813
FY25_VID_ALLOC = -322
FY25_VID_RATE = -291
FY25_VOICE_VOLUME = -230
FY25_VOICE_RATE = 143

# Disclosed ARPU $
ARPU_RES_Q1 = (118.44, 120.07)  # 2026, 2025
ARPU_SMB_Q1 = (162.71, 161.31)
ARPU_RES_FY25 = (119.05, 118.71)

# Video seamless entertainment allocation netted in video revenue ($M)
VID_ALLOC_Q1 = (218, 47)

# Rural subset — trending subsidized rural initiative page
RURAL_CR = dict(ye25=486, q1_26=527)
RURAL_PASS_Q1 = 1385
RURAL_PEN_Q1 = 0.381
RURAL_REV_Q1 = 221  # total rural revenue $M
RURAL_RES_REV_Q1 = 167
RURAL_SUBSIDY_Q1 = 28
RURAL_ARPU_RES_Q1 = 113.71

# Peer overlay — CMCSA domestic residential broadband only (apples-to-apples)
CMCSA_BB_EOP_Q1_26 = 28654
CMCSA_BB_ADD_Q1_26 = -65
CMCSA_BB_EOP_Q1_25 = 29190
CMCSA_BB_ADD_Q1_25 = -183

# Q2 2026 later public facts (labeled; not the assignment headline)
Q2_INET_ADD = -172
Q2_MOB_ADD = 406
Q2_VID_ADD = -21
Q2_CR_ADD = -184
Q2_RURAL_CR_ADD = 47
REV_Q2 = {"internet": (5776, 5969), "mobile": (1095, 921), "total": (13526, 13766)}


def avg_k(begin: int, end: int) -> float:
    return (begin + end) / 2.0


def monthly_arpu(rev_m: float, begin_k: int, end_k: int) -> float:
    """$ per customer per month. rev in $M, customers in thousands."""
    return rev_m * 1000.0 / 3.0 / avg_k(begin_k, end_k)


def yoy_pct(new: float, old: float) -> float:
    return (new / old - 1.0) * 100.0


def loss_rate(add: int, begin: int) -> float:
    return abs(add) / begin


def main() -> None:
    rows: list[tuple[str, str, str, str]] = []

    def add(rid: str, label: str, val: str, tag: str) -> None:
        rows.append((rid, label, val, tag))

    # --- identities ---
    tot_inet_q1 = Q1_26_ADDS["res_inet"] + Q1_26_ADDS["smb_inet"]
    tot_cr_q1 = Q1_26_ADDS["res_cr"] + Q1_26_ADDS["smb_cr"]
    tot_mob_q1 = Q1_26_ADDS["res_mob"] + Q1_26_ADDS["smb_mob"]
    tot_vid_q1 = Q1_26_ADDS["res_vid"] + Q1_26_ADDS["smb_vid"]
    res_prod_rev_q1 = (
        REV_Q1["internet"][0]
        + REV_Q1["mobile"][0]
        + REV_Q1["video"][0]
        + REV_Q1["voice"][0]
    )
    company_rev_q1 = (
        REV_Q1["residential"][0]
        + REV_Q1["smb"][0]
        + REV_Q1["mm"][0]
        + REV_Q1["ads"][0]
        + REV_Q1["other"][0]
    )
    fy25_inet_bridge = FY25_INET_RATE_MIX + FY25_INET_VOLUME
    fy25_inet_delta = REV_FY["internet"][0] - REV_FY["internet"][1]
    fy25_mob_bridge = FY25_MOB_VOLUME + FY25_MOB_RATE
    fy25_mob_delta = REV_FY["mobile"][0] - REV_FY["mobile"][1]
    fy25_vid_bridge = FY25_VID_VOLUME + FY25_VID_ALLOC + FY25_VID_RATE
    fy25_vid_delta = REV_FY["video"][0] - REV_FY["video"][1]

    add("A1", "Res. Internet YE2025 (Q1 begin)", f"{RES_INET['ye25']:,}k", "RETRIEVED 10-K/Ex99.1")
    add("A2", "Res. Internet Q1'26 ending", f"{RES_INET['q1_26']:,}k", "RETRIEVED Ex99.1")
    add("A3", "Res. Internet Q1'26 net adds", f"{Q1_26_ADDS['res_inet']:,}k", "RETRIEVED Ex99.1")
    add("A4", "SMB Internet Q1'26 net adds", f"{Q1_26_ADDS['smb_inet']:,}k", "RETRIEVED Ex99.1")
    add("A5", "Total Internet Q1'26 net adds", f"{Q1_26_ADDS['tot_inet']:,}k", "RETRIEVED Ex99.1")
    add("A6", "A3+A4 identity check", f"{tot_inet_q1:,}k", "derived")
    add("A7", "Total Internet Q1'25 net adds", f"{Q1_25_ADDS['tot_inet']:,}k", "RETRIEVED Ex99.1")
    add("A8", "Q1 Internet YoY slope break", f"{Q1_26_ADDS['tot_inet'] - Q1_25_ADDS['tot_inet']:,}k", "derived")

    inet_26, inet_25 = REV_Q1["internet"]
    inet_d = inet_26 - inet_25
    add("B1", "Internet revenue Q1'26 $M", f"${inet_26:,}", "RETRIEVED Ex99.1")
    add("B2", "Internet revenue Q1'25 $M", f"${inet_25:,}", "RETRIEVED Ex99.1")
    add("B3", "Internet $ YoY", f"${inet_d:+,}", "derived")
    add("B4", "Internet $ YoY %", f"{yoy_pct(inet_26, inet_25):.1f}%", "derived")
    add("B5", "Internet share of Q1'26 revenue", f"{100 * inet_26 / REV_Q1['total'][0]:.1f}%", "derived")

    arpu_inet_26 = monthly_arpu(inet_26, RES_INET["ye25"], RES_INET["q1_26"])
    arpu_inet_25 = monthly_arpu(inet_25, RES_INET["ye24"], RES_INET["q1_25"])
    avg_26 = avg_k(RES_INET["ye25"], RES_INET["q1_26"])
    avg_25 = avg_k(RES_INET["ye24"], RES_INET["q1_25"])
    vol_inet = (avg_26 - avg_25) * arpu_inet_25 * 3 / 1000
    rate_inet = inet_d - vol_inet
    add("C1", "Implied Internet ARPU Q1'26 $/mo", f"${arpu_inet_26:.2f}", "DERIVED retrieved/retrieved")
    add("C2", "Implied Internet ARPU Q1'25 $/mo", f"${arpu_inet_25:.2f}", "DERIVED")
    add("C3", "Volume effect holding Q1'25 ARPU $M", f"${vol_inet:+.0f}", "DERIVED")
    add("C4", "Rate/mix residual $M", f"${rate_inet:+.0f}", "DERIVED")
    # break-even ARPU to hold dollars
    be_arpu = inet_25 * 1000 / 3 / avg_26
    add("C5", "ARPU to hold Internet $ flat", f"${be_arpu:.2f}", "DERIVED")
    add("C6", "ARPU gap vs hold-flat", f"${arpu_inet_26 - be_arpu:.2f}", "DERIVED")

    add("D1", "FY25 Internet $ YoY (10-K)", f"${fy25_inet_delta:+,}", "RETRIEVED")
    add("D2", "FY25 Internet rate/mix bridge", f"${FY25_INET_RATE_MIX:+,}", "RETRIEVED 10-K")
    add("D3", "FY25 Internet volume bridge", f"${FY25_INET_VOLUME:+,}", "RETRIEVED 10-K")
    add("D4", "FY25 residential Internet customers", f"{RES_INET['ye25'] - RES_INET['ye24']:,}k", "RETRIEVED")

    mob_26, mob_25 = REV_Q1["mobile"]
    mob_d = mob_26 - mob_25
    arpu_mob_26 = monthly_arpu(mob_26, RES_MOB["ye25"], RES_MOB["q1_26"])
    arpu_mob_25 = monthly_arpu(mob_25, RES_MOB["ye24"], RES_MOB["q1_25"])
    add("E1", "Mobile lines Q1'26 net adds", f"{Q1_26_ADDS['tot_mob']:+,}k", "RETRIEVED")
    add("E2", "Mobile service revenue Q1'26 $M", f"${mob_26:,}", "RETRIEVED")
    add("E3", "Mobile $ YoY", f"${mob_d:+,}", "derived")
    add("E4", "Mobile $ YoY %", f"{yoy_pct(mob_26, mob_25):.1f}%", "derived")
    add("E5", "Implied mobile ARPU Q1'26 $/mo", f"${arpu_mob_26:.2f}", "DERIVED")
    add("E6", "Implied mobile ARPU Q1'25 $/mo", f"${arpu_mob_25:.2f}", "DERIVED")
    add("E7", "FY25 mobile rate/volume bridge", f"${fy25_mob_delta:+,} = {FY25_MOB_VOLUME:+}/{FY25_MOB_RATE:+}", "RETRIEVED")
    add("E8", "Do not credit mobile vs Internet (Root C)", "not a tape offset", "constraint")

    conn_26 = inet_26 + mob_26
    conn_25 = inet_25 + mob_25
    add("E9", "Connectivity $ (Internet+mobile) YoY", f"${conn_26 - conn_25:+,}", "derived")

    vid_26, vid_25 = REV_Q1["video"]
    vid_d = vid_26 - vid_25
    alloc_d = VID_ALLOC_Q1[0] - VID_ALLOC_Q1[1]
    vid_ex_alloc = vid_d + alloc_d  # allocation increase reduces reported video $
    arpu_vid_26 = monthly_arpu(vid_26, RES_VID["ye25"], RES_VID["q1_26"])
    arpu_vid_25 = monthly_arpu(vid_25, RES_VID["ye24"], RES_VID["q1_25"])
    add("F1", "Video customers Q1'26 net adds", f"{Q1_26_ADDS['tot_vid']:,}k", "RETRIEVED")
    add("F2", "Video revenue Q1'26 $M", f"${vid_26:,}", "RETRIEVED")
    add("F3", "Video $ YoY", f"${vid_d:+,}", "derived")
    add("F4", "Seamless allocation Q1'26 vs Q1'25", f"${VID_ALLOC_Q1[0]} vs ${VID_ALLOC_Q1[1]}", "RETRIEVED Ex99.1")
    add("F5", "Allocation YoY drag on video $", f"${-alloc_d:+,}", "derived")
    add("F6", "Video $ YoY ex allocation drag", f"${vid_d + alloc_d:+,}", "DERIVED")
    add("F7", "Implied video ARPU Q1'26 $/mo", f"${arpu_vid_26:.2f}", "DERIVED")
    add("F8", "Implied video ARPU Q1'25 $/mo", f"${arpu_vid_25:.2f}", "DERIVED")

    voi_26, voi_25 = REV_Q1["voice"]
    arpu_voi_26 = monthly_arpu(voi_26, RES_VOICE["ye25"], RES_VOICE["q1_26"])
    arpu_voi_25 = monthly_arpu(voi_25, RES_VOICE["ye24"], RES_VOICE["q1_25"])
    add("G1", "Voice customers Q1'26 net adds", f"{Q1_26_ADDS['tot_voice']:,}k", "RETRIEVED")
    add("G2", "Voice revenue Q1 $ YoY", f"${voi_26 - voi_25:+,}", "derived")
    add("G3", "Implied voice ARPU Q1'26 $/mo", f"${arpu_voi_26:.2f}", "DERIVED")
    add("G4", "Implied voice ARPU Q1'25 $/mo", f"${arpu_voi_25:.2f}", "DERIVED")

    smb_26, smb_25 = REV_Q1["smb"]
    arpu_smb_chk = monthly_arpu(smb_26, SMB_CR["ye25"], SMB_CR["q1_26"])
    add("H1", "SMB relationships Q1'26 net adds", f"{Q1_26_ADDS['smb_cr']:,}k", "RETRIEVED")
    add("H2", "SMB revenue Q1 $ YoY", f"${smb_26 - smb_25:+,}", "derived")
    add("H3", "Disclosed SMB ARPU Q1'26", f"${ARPU_SMB_Q1[0]:.2f}", "RETRIEVED")
    add("H4", "Recomputed SMB ARPU Q1'26", f"${arpu_smb_chk:.2f}", "DERIVED identity")

    mm_26, mm_25 = REV_Q1["mm"]
    add("I1", "Mid-market PSUs Q1'26 net adds", f"{Q1_26_ADDS['mm_psu']:+,}k", "RETRIEVED")
    add("I2", "Mid-market revenue Q1 $ YoY", f"${mm_26 - mm_25:+,}", "derived")
    add("I3", "Mid-market $ vs Internet $ hole", f"{mm_26 - mm_25} / {abs(inet_d)} = {100 * (mm_26 - mm_25) / abs(inet_d):.0f}%", "derived")

    res_26, res_25 = REV_Q1["residential"]
    arpu_res_chk = monthly_arpu(res_26, RES_CR["ye25"], RES_CR["q1_26"])
    add("J1", "Residential CR Q1'26 net adds", f"{Q1_26_ADDS['res_cr']:,}k", "RETRIEVED")
    add("J2", "Residential revenue Q1 $ YoY", f"${res_26 - res_25:+,}", "derived")
    add("J3", "Disclosed res. ARPU Q1'26", f"${ARPU_RES_Q1[0]:.2f}", "RETRIEVED")
    add("J4", "Recomputed res. ARPU Q1'26", f"${arpu_res_chk:.2f}", "DERIVED identity")
    add("J5", "Res. products $ identity (I+M+V+Vo)", f"${res_prod_rev_q1:,}", "derived")

    add("K1", "Rural CR Q1'26 net adds", f"{Q1_26_ADDS['rural_cr']:+,}k", "RETRIEVED Ex99.1")
    add("K2", "Rural CR ending Q1'26", f"{RURAL_CR['q1_26']:,}k", "RETRIEVED trending")
    add("K3", "Core CR adds (company - rural)", f"{Q1_26_ADDS['tot_cr'] - Q1_26_ADDS['rural_cr']:,}k", "derived identity")
    add("K4", "Rural total revenue Q1'26 $M", f"${RURAL_REV_Q1}", "RETRIEVED trending")
    add("K5", "Rural share of company revenue", f"{100 * RURAL_REV_Q1 / REV_Q1['total'][0]:.1f}%", "derived")
    add("K6", "Rural take of passings", f"{100 * RURAL_PEN_Q1:.1f}%", "RETRIEVED")
    add("K7", "Rural is CR subset, not Internet cut", "not an Internet LOB", "constraint")

    # Peer overlay — residential broadband only
    chtr_rate = loss_rate(Q1_26_ADDS["res_inet"], RES_INET["ye25"])
    cmcsa_begin = CMCSA_BB_EOP_Q1_26 - CMCSA_BB_ADD_Q1_26
    cmcsa_rate = loss_rate(CMCSA_BB_ADD_Q1_26, cmcsa_begin)
    ratio = chtr_rate / cmcsa_rate
    expected = cmcsa_rate * RES_INET["ye25"]
    excess = abs(Q1_26_ADDS["res_inet"]) - expected
    committed_ratio = 1.8
    committed_excess = 54
    add("L1", "CMCSA resid. BB Q1'26 net adds", f"{CMCSA_BB_ADD_Q1_26:,}k", "RETRIEVED CMCSA Ex99.1")
    add("L2", "CHTR res. Internet net-loss rate", f"{100 * chtr_rate:.2f}%", "derived")
    add("L3", "CMCSA resid. BB net-loss rate", f"{100 * cmcsa_rate:.2f}%", "derived")
    add("L4", "Rate ratio unrounded", f"{ratio:.2f}x", "derived")
    add("L5", "Committed ratio (round down)", f"{committed_ratio:.1f}x", "commit · reuse network-churn")
    add("L6", "Excess vs peer rate (unrounded)", f"{excess:.1f}k", "derived")
    add("L7", "Committed excess (round down)", f"{committed_excess}k", "commit · reuse")

    tot_26, tot_25 = REV_Q1["total"]
    add("M1", "Company revenue Q1 $ YoY", f"${tot_26 - tot_25:+,}", "derived")
    add("M2", "Company revenue identity", f"${company_rev_q1:,}", "derived")

    # Q2 later public fact
    q2_inet_d = REV_Q2["internet"][0] - REV_Q2["internet"][1]
    add("N1", "Q2 Internet net adds (later fact)", f"{Q2_INET_ADD:,}k", "RETRIEVED Ex99.1 Q2 · later")
    add("N2", "Q2 Internet $ YoY (later fact)", f"${q2_inet_d:+,}", "RETRIEVED Ex99.1 Q2 · later")
    add("N3", "Q2 mobile net adds (later fact)", f"{Q2_MOB_ADD:+,}k", "RETRIEVED · later")

    # Dollar-weighted origin
    retrieved_q1_rev = tot_26  # every revenue line is retrieved
    estimated_q1_rev = 0
    add("O1", "Q1 revenue $ retrieved-weighted", "100%", "all LOB $ from Ex99.1")
    add("O2", "Q1 revenue $ estimated-weighted", "0%", "no estimated $ in headline")
    add("O3", "Gross churn in this model", "missing", "not disclosed · high leverage")

    print("ID  Line                                              Value                    Tag")
    print("-" * 96)
    for rid, label, val, tag in rows:
        print(f"{rid:<4} {label:<48} {val:>18}  {tag}")

    print()
    print("HEADLINE")
    print(
        f"  ACCURATE for net LOB customer + revenue performance; "
        f"NOT ACCURATE as a churn / retention-quality analysis."
    )
    print(
        f"  Q1 2026 residential Internet {Q1_26_ADDS['res_inet']}k customers and "
        f"${inet_d}M revenue (volume ${vol_inet:+.0f}M, rate/mix ${rate_inet:+.0f}M). "
        f"Internet is {100 * inet_26 / tot_26:.0f}% of Q1 revenue."
    )
    print(
        f"  Mobile {Q1_26_ADDS['tot_mob']:+}k lines and ${mob_d:+}M — do not credit "
        f"against Internet for the tape (Root C). Connectivity $ still "
        f"${conn_26 - conn_25:+}M because mobile > Internet $ hole."
    )
    print(
        f"  Peer (resid. BB only): {committed_ratio:.1f}x Comcast net-loss rate; "
        f"excess {committed_excess}k (reuse; round down from {ratio:.2f}x / {excess:.1f}k)."
    )
    print(
        f"  Rural +{Q1_26_ADDS['rural_cr']}k CR / ${RURAL_REV_Q1}M (1.6% of revenue) "
        f"is a disclosed subset, not an Internet product cut. Core CR "
        f"{Q1_26_ADDS['tot_cr'] - Q1_26_ADDS['rural_cr']}k."
    )

    # --- asserts: identities and commits ---
    assert tot_inet_q1 == Q1_26_ADDS["tot_inet"]
    assert tot_cr_q1 == Q1_26_ADDS["tot_cr"]
    assert tot_mob_q1 == Q1_26_ADDS["tot_mob"]
    assert tot_vid_q1 == Q1_26_ADDS["tot_vid"]
    assert res_prod_rev_q1 == res_26
    assert company_rev_q1 == tot_26
    assert fy25_inet_bridge == fy25_inet_delta
    assert fy25_mob_bridge == fy25_mob_delta
    assert fy25_vid_bridge == fy25_vid_delta
    assert abs(arpu_res_chk - ARPU_RES_Q1[0]) < 0.05
    assert abs(arpu_smb_chk - ARPU_SMB_Q1[0]) < 0.15
    assert committed_ratio <= ratio + 0.001
    assert committed_excess <= excess + 0.01
    assert inet_d == -78
    assert mob_d == 138
    assert Q1_26_ADDS["res_inet"] == -117
    assert Q1_26_ADDS["tot_inet"] == -120
    # round-against: volume drag larger than headline $ decline
    assert vol_inet < inet_d < 0
    print()
    print("OK — identities hold; committed peer figures round against 'Charter is worse'.")
    print("OK — Internet $ decline is volume, not a rate collapse.")

    # committed canvas figures (must match prose)
    print()
    print("CANVAS LOCKS")
    print(f"  res_inet_adds={Q1_26_ADDS['res_inet']}")
    print(f"  tot_inet_adds={Q1_26_ADDS['tot_inet']}")
    print(f"  inet_dollar_yoy={inet_d}")
    print(f"  inet_vol={vol_inet:.0f} inet_rate={rate_inet:.0f}")
    print(f"  implied_inet_arpu_26={arpu_inet_26:.2f} 25={arpu_inet_25:.2f}")
    print(f"  mob_adds={Q1_26_ADDS['tot_mob']} mob_dollar_yoy={mob_d}")
    print(f"  implied_mob_arpu_26={arpu_mob_26:.2f} 25={arpu_mob_25:.2f}")
    print(f"  vid_adds={Q1_26_ADDS['tot_vid']} vid_dollar_yoy={vid_d} alloc_drag={alloc_d}")
    print(f"  voice_adds={Q1_26_ADDS['tot_voice']} voice_dollar_yoy={voi_26 - voi_25}")
    print(f"  smb_adds={Q1_26_ADDS['smb_cr']} smb_dollar_yoy={smb_26 - smb_25}")
    print(f"  mm_adds={Q1_26_ADDS['mm_psu']} mm_dollar_yoy={mm_26 - mm_25}")
    print(f"  rural_cr={Q1_26_ADDS['rural_cr']} core_cr={Q1_26_ADDS['tot_cr'] - Q1_26_ADDS['rural_cr']}")
    print(f"  rural_rev={RURAL_REV_Q1} rural_share={100 * RURAL_REV_Q1 / tot_26:.1f}")
    print(f"  conn_dollar_yoy={conn_26 - conn_25}")
    print(f"  peer_ratio={committed_ratio} peer_excess={committed_excess}")
    print(f"  q2_inet_adds={Q2_INET_ADD} q2_inet_dollar={q2_inet_d}")


if __name__ == "__main__":
    main()
