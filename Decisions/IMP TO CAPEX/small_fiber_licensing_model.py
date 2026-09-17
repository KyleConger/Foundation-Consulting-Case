"""
Small-fiber licensing cost — Charter paying for wholesale / open-access / IRU
last-mile access on non-AT&T / non-Verizon fiber (munis, independents,
regional overbuilders, electric co-ops) so Spectrum can sell Internet on
plant it does not own.

Assignment anchor: end Q1 2026. Q2 labeled later public fact.
Does not overwrite: six-recommendation-areas 54k / −66k; ifxy-stock-signal;
customer-performance.

Deal definition (not sized as the primary): not content licensing, not brand
licensing, not "license Spectrum onto Cox" (Area 5). Rival mechanism noted
if Frontier-as-other-FTTH (YE2025 10-K) — Frontier closed into Verizon on
20 Jan 2026 and is no longer "smaller."

Run: python "Decisions/IMP TO CAPEX/small_fiber_licensing_model.py"
"""

from __future__ import annotations

import math

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def annuity_pv(pmt: float, r: float, n: int) -> float:
    """PV of an ordinary annuity: pmt at end of each year."""
    if r == 0:
        return pmt * n
    return pmt * (1.0 - (1.0 + r) ** (-n)) / r


def tag_dollars(retrieved: float, estimated: float) -> tuple[float, float, float]:
    total = retrieved + estimated
    return total, (retrieved / total if total else 0.0), (estimated / total if total else 0.0)


# ===========================================================================
# RETRIEVED inputs
# ===========================================================================

# --- Charter operating (Q1 2026 / FY2025) ---
A1_CHTR_PASSINGS_Q1_26 = 58_661_000  # Ex99.1 Q1 2026 estimated passings
A2_CHTR_INET_Q1_26 = 29_560_000  # Ex99.1 ending Internet customers
A3_CHTR_INET_YE25 = 29_680_000  # 10-K / Ex99.1
A4_CHTR_RES_INET_Q1_26 = 27_524_000  # Ex99.1
A5_CHTR_RES_INET_YE25 = 27_641_000  # 10-K
A6_CHTR_CR_Q1_26 = 31_683_000  # Ex99.1
A7_INET_REV_Q1_26_M = 5_852.0  # $M Ex99.1
A8_INET_REV_FY25_M = 23_765.0  # $M 10-K
A9_CUSTOPS_Q1_26_M = 766.0  # $M Ex99.1
A10_FIELD_Q1_26_M = 1_258.0  # $M Ex99.1
A11_CAPEX_FY25_M = 11_659.0  # $M 10-K / Ex99.1  (~$11.7B)
A12_UPGRADE_Q1_26_M = 675.0  # $M Ex99.1
A13_UPGRADE_Q1_25_M = 395.0  # $M Ex99.1
A14_RURAL_PER_PASSING = 5_900.0  # decisions.md: ~$8.1B / 1.385M
A15_RURAL_TAKE_Q1 = 0.381  # trending 38.1%
A16_EXCESS_VS_CMCSA = 54_000  # ifxy / six-rec commit (round down from 54.4k)
A17_ATT_OVERLAP = 0.27  # 10-K FY2025 terrestrial 100 Mbps+ ; NOT "smaller"
A18_VZ_OVERLAP = 0.16  # 10-K FY2025 ; NOT "smaller"
A19_RURAL_CR_COST = 15_400.0  # decisions.md derived before grants

# --- Geography (US) ---
G1_US_HU_JUL2025 = 148_260_882  # Census vintage 2025 housing units 1 Jul 2025
G2_US_OCC_HU_Q1_26 = 133_701_000  # Census HVS occupied HU Q1 2026 (FRED EOCCUSQ176N)

# --- National fiber (to subtract large overbuilders; FBA funded its own report) ---
N1_FBA_FIBER_HP_YE25 = 84_600_000  # Fiber Broadband Association YE2025 homes passed
N2_ATT_FIBER_YE25 = 32_000_000  # AT&T FY2025: 32.0M consumer+business fiber locations
N3_ATT_FIBER_Q1_26 = 37_000_000  # AT&T Q1 2026 "over 37 million" incl. >4M Lumen MM
N4_VZ_FRONTIER_Q1_26 = 30_000_000  # Verizon Jan 2026: "over 30 million" incl. Frontier
N5_FRONTIER_Q3_25 = 8_800_000  # Frontier Q3 2025 fiber locations; closed to VZ 20 Jan 2026
N6_METRONET_NOV25 = 3_000_000  # MetroNet Nov 2025 homes+businesses
N7_KINETIC_HP = 1_900_000  # Uniti/Kinetic 1.9M homes passed (2025/26 releases)
N8_BRIGHTSPEED_YE24 = 1_820_000  # Brightspeed 7 Jan 2025: 1.82M fiber-enabled
N9_COOP_SURVEY_N = 78  # NRTC/NRECA 2025 benchmarking; NRTC+NRECA funded
N10_COOP_AVG_HP = 29_600  # average homes passed among 78 surveyed
N11_COOP_AVG_MI = 2_800  # average fiber miles among 78 surveyed
N12_COOP_DEPLOYED = 240  # "more than 240" electric members have deployed broadband

# --- Wholesale / IRU analogs (public tariffs; operator-funded, not vendor surveys) ---
W1_GRANT_100_MRC = 32.50  # Grant PUD Rate Schedule 100, Res. 9058, eff. 1 Aug 2024
W2_GRANT_250_MRC = 42.50
W3_GRANT_GIG_MRC = 52.50
W4_GRANT_PREMIUM = 10.00  # optional 24/7 premium support per premises
W5_JEFF_GIG_MRC = 54.00  # Jefferson County PUD wholesale PON 1 Gbps 2025
W6_JEFF_150_MRC = 47.00  # Jefferson wholesale PON 150 Mbps
W7_JEFF_3G_MRC = 117.00  # Jefferson wholesale PON 3 Gbps
W8_UTOPIA_INFRA_MRC = 30.00  # UTOPIA Fiber customer-billed infrastructure (not ISP COGS unless absorbed)
W9_IRU_STRAND_MILE = 1_500.0  # Laurinburg NC ordinance: 20-yr IRU $/strand-mile
W10_IRU_MAINT_PATH_MI = 300.0  # Laurinburg annual $/path-mile
W11_DEC_IRU_STRAND_MI = 1_000.0  # City of Decatur IL 2021 IRU $/strand-mile
W12_CTC_IRU_LOW = 325.0  # CTC for Virginia Beach (city-funded 2017): 20-yr $/strand-mile
W13_CTC_IRU_HIGH = 2_000.0
W14_CTC_MAINT = 250.0  # CTC typical annual maintenance $/mile

# --- Capital / comparison ---
K1_TERM_YEARS = 20
K2_WACC = 0.08  # ESTIMATED blended; Charter cash interest ~5.3% on ~$95B, equity higher
K3_TAKE_OA = 0.40  # ESTIMATED open-access / co-op take; FBA ~47% fiber take, co-op ~50%
K4_FIELD_REMAIN = 0.30  # ESTIMATED share of field opex that remains when last-mile is rented (CPE truck, WiFi)
K5_SAC_AMORT = 50.0  # ESTIMATED $/sub-year; $150 SAC / 3-year life, rounded up
K6_TRANSIT_YR = 24.0  # ESTIMATED; Charter already has a national backbone; NNI is small at scale
K7_STRANDS = 2  # ESTIMATED pair for dark IRU analog
K8_IN_POLYGON = 0.40  # ESTIMATED: of naive HU-share, share actually inside Charter last-mile polygon
K9_WHOLESALE_WILLING = 0.15  # ESTIMATED share of small fiber that will sell last-mile to Charter
K10_MUNI_HP = 3_000_000  # ESTIMATED; ILSR has 400+ muni networks / 700 communities, no homes-passed total (ILSR-funded map)
K11_GOOGLE_OTHER_HP = 3_000_000  # ESTIMATED Google Fiber + other independents not in N6–N8

# Scenario passings in Charter footprint (because overlap is the blocking input)
S_LOW_HP = 200_000  # open-access / PUD-like only
S_BASE_HP = 500_000  # working scale if a handful of regional OA networks transact
S_HIGH_HP = 2_000_000  # naive HU-share of wholesale-willing plant, rounded against us


def main() -> None:
    rows: list[tuple[str, str, str, str]] = []

    def add(rid: str, label: str, val, origin: str) -> None:
        if isinstance(val, float):
            if abs(val) >= 100:
                s = f"{val:,.0f}"
            elif abs(val) >= 1:
                s = f"{val:,.2f}"
            else:
                s = f"{val:.4f}"
        else:
            s = f"{val:,}" if isinstance(val, int) and abs(val) >= 1000 else str(val)
        rows.append((rid, label, s, origin))

    # ----- Frame B: unit economics (decision-critical) -----
    avg_tot_inet = 0.5 * (A3_CHTR_INET_YE25 + A2_CHTR_INET_Q1_26)
    arpu_mo_tot = A7_INET_REV_Q1_26_M * 1000.0 / 3.0 / (avg_tot_inet / 1000.0)
    # A7 is $M, avg is counts: $M * 1e6 / 3 / avg_customers = $/mo
    arpu_mo_tot = A7_INET_REV_Q1_26_M * 1_000_000.0 / 3.0 / avg_tot_inet
    arpu_yr_tot = arpu_mo_tot * 12.0

    avg_res_inet = 0.5 * (A5_CHTR_RES_INET_YE25 + A4_CHTR_RES_INET_Q1_26)
    arpu_mo_resalloc = A7_INET_REV_Q1_26_M * 1_000_000.0 / 3.0 / avg_res_inet
    arpu_yr_resalloc = arpu_mo_resalloc * 12.0

    add("B1", "Avg total Internet customers Q1'26", avg_tot_inet, "DERIVED A2,A3")
    add("B2", "Internet ARPU $/mo (total $ / total inet)", arpu_mo_tot, "DERIVED retrieved/retrieved")
    add("B3", "Internet ARPU $/year (B2×12) — HEADLINE ARPU", arpu_yr_tot, "DERIVED; round down later")
    add("B4", "Res-allocated ARPU $/mo (total $ / res inet)", arpu_mo_resalloc, "DERIVED; matches customer-performance $70.72")
    add("B5", "Res-allocated ARPU $/year", arpu_yr_resalloc, "DERIVED")

    # Commit ARPU rounding DOWN (against the deal)
    arpu_yr_commit = 790.0
    add("B6", "Committed Internet ARPU $/sub-year (round down)", arpu_yr_commit, "COMMIT vs B3")

    w_base_mrc = W5_JEFF_GIG_MRC  # higher of Grant gig $52.50 and Jefferson gig $54
    w_low_mrc = W8_UTOPIA_INFRA_MRC
    w_high_mrc = W7_JEFF_3G_MRC
    w_base_yr = w_base_mrc * 12.0
    w_low_yr = w_low_mrc * 12.0
    w_high_yr = w_high_mrc * 12.0
    w_commit_yr = 650.0  # round UP from 54×12 = 648

    add("B7", "Grant PUD gigabit wholesale MRC $/mo", W3_GRANT_GIG_MRC, "RETRIEVED Grant tariff 8/2024")
    add("B8", "Jefferson PUD wholesale PON 1 Gbps MRC $/mo", W5_JEFF_GIG_MRC, "RETRIEVED Jefferson 2025 rates")
    add("B9", "UTOPIA infrastructure MRC $/mo (customer-billed analog)", W8_UTOPIA_INFRA_MRC, "RETRIEVED UTOPIA public pricing")
    add("B10", "Jefferson 3 Gbps wholesale MRC $/mo (high)", W7_JEFF_3G_MRC, "RETRIEVED Jefferson 2025")
    add("B11", "Base wholesale $/sub-year (B8×12)", w_base_yr, "DERIVED")
    add("B12", "Committed wholesale COGS $/sub-year (round UP)", w_commit_yr, "COMMIT vs B11")
    add("B13", "Low wholesale $/sub-year (UTOPIA×12)", w_low_yr, "DERIVED")
    add("B14", "High wholesale $/sub-year (3G×12)", w_high_yr, "DERIVED")

    # Remaining opex on a rented last-mile
    custops_yr_m = A9_CUSTOPS_Q1_26_M * 4.0
    field_yr_m = A10_FIELD_Q1_26_M * 4.0
    care_per = custops_yr_m * 1_000_000.0 / A6_CHTR_CR_Q1_26
    field_owned_per = field_yr_m * 1_000_000.0 / A6_CHTR_CR_Q1_26
    field_remain_per = field_owned_per * K4_FIELD_REMAIN
    remain_opex = care_per + field_remain_per + K6_TRANSIT_YR + K5_SAC_AMORT

    add("B15", "Q1 customer ops annualized $M", custops_yr_m, "DERIVED A9×4")
    add("B16", "Care/billing $/CR-year (B15 / CR)", care_per, "DERIVED; retrieved/retrieved")
    add("B17", "Owned-plant field $/CR-year", field_owned_per, "DERIVED A10×4 / CR")
    add("B18", "Residual field on wholesale $/sub-year (30% of B17)", field_remain_per, "ESTIMATED K4")
    add("B19", "Incremental transit/NNI $/sub-year", K6_TRANSIT_YR, "ESTIMATED")
    add("B20", "SAC amortization $/sub-year", K5_SAC_AMORT, "ESTIMATED")
    add("B21", "Remaining opex on wholesale $/sub-year", remain_opex, "DERIVED B16+B18+B19+B20")

    gross_after_w = arpu_yr_commit - w_commit_yr
    contrib_base = arpu_yr_commit - w_commit_yr - remain_opex
    contrib_low = arpu_yr_commit - w_low_yr - remain_opex  # UTOPIA absorbed
    contrib_high = arpu_yr_commit - w_high_yr - remain_opex
    # Round contribution AGAINST the deal (more negative / less positive)
    contrib_commit = -90.0  # round  (will set after seeing number)

    add("B22", "Gross after wholesale $/sub-year (B6-B12)", gross_after_w, "DERIVED")
    add("B23", "Contribution after remaining opex — BASE", contrib_base, "DERIVED")
    add("B24", "Contribution at UTOPIA $30 (low COGS)", contrib_low, "DERIVED")
    add("B25", "Contribution at Jefferson 3G (high COGS)", contrib_high, "DERIVED")

    # Frame B headline: commit contribution rounded against (more negative)
    contrib_commit = math.floor(contrib_base)  # round against the deal
    add("B26", "Committed Frame B contribution $/sub-year (round against)", contrib_commit, "COMMIT")
    add("B27", "Wholesale as % of ARPU (B12/B6)", 100.0 * w_commit_yr / arpu_yr_commit, "DERIVED")

    # 54k close COGS (does not overwrite the 54k headline)
    cogs_54k_m = A16_EXCESS_VS_CMCSA * w_commit_yr / 1_000_000.0
    contrib_54k_m = A16_EXCESS_VS_CMCSA * contrib_base / 1_000_000.0
    add("B28", "COGS if 54k excess were on wholesale $M/yr", cogs_54k_m, "DERIVED; does not overwrite 54k")
    add("B29", "Contribution if 54k on wholesale $M/yr", contrib_54k_m, "DERIVED")

    # ----- Frame A: $ per passing / connected home -----
    pv_connected = annuity_pv(w_commit_yr, K2_WACC, K1_TERM_YEARS)
    pv_commit = 6400.0  # round UP
    homes_per_mi = N10_COOP_AVG_HP / N11_COOP_AVG_MI
    mi_per_home = 1.0 / homes_per_mi
    dark_nrc = W9_IRU_STRAND_MILE * K7_STRANDS * mi_per_home
    dark_maint_yr = W10_IRU_MAINT_PATH_MI * mi_per_home
    dark_pv = dark_nrc + annuity_pv(dark_maint_yr, K2_WACC, K1_TERM_YEARS)
    dark_commit = 600.0  # round UP from ~$560s

    add("A20", "Homes per fiber-mile (NRTC avg 29,600 / 2,800)", homes_per_mi, "DERIVED retrieved/retrieved; NRTC+NRECA funded")
    add("A21", "Miles per home", mi_per_home, "DERIVED")
    add("A22", "Dark IRU NRC $/passing (Laurinburg $1,500 × 2 strands × mi/home)", dark_nrc, "DERIVED; ESTIMATED strands")
    add("A23", "Dark IRU maint $/passing-year", dark_maint_yr, "DERIVED")
    add("A24", "Dark IRU 20-yr PV $/passing @ 8%", dark_pv, "DERIVED")
    add("A25", "Committed dark-IRU $/passing (round UP)", dark_commit, "COMMIT — NOT last-mile lit")
    add("A26", "Lit wholesale 20-yr PV $/connected @ 8% (annuity of B12)", pv_connected, "DERIVED")
    add("A27", "Committed Frame A PV $/connected home (round UP)", pv_commit, "COMMIT")
    add("A28", "Plant-IRU $/passing at 40% take (A27×K3)", pv_commit * K3_TAKE_OA, "DERIVED ESTIMATED take")
    add("A29", "Rural $/passing (comparison)", A14_RURAL_PER_PASSING, "RETRIEVED-derived decisions.md")
    add("A30", "Rural $/CR at 38.1% take", A14_RURAL_PER_PASSING / A15_RURAL_TAKE_Q1, "DERIVED")
    rural_cr = A14_RURAL_PER_PASSING / A15_RURAL_TAKE_Q1
    add("A31", "Rural 20-yr capital recovery $/CR-year @ 8%", rural_cr / annuity_pv(1.0, K2_WACC, K1_TERM_YEARS), "DERIVED")
    add("A32", "Wholesale vs rural CR capex (A27 / A30)", pv_commit / rural_cr, "DERIVED")

    # Equivalent annual cost of rural passing at 8%/20y
    rural_eac_passing = A14_RURAL_PER_PASSING / annuity_pv(1.0, K2_WACC, K1_TERM_YEARS)
    add("A33", "Rural EAC $/passing-year @ 8%/20y", rural_eac_passing, "DERIVED")
    add("A34", "Wholesale $/passing-year at 40% take (B12×K3)", w_commit_yr * K3_TAKE_OA, "DERIVED")

    # ----- Geography conversion (blocking overlap) -----
    chtr_hu_share = A1_CHTR_PASSINGS_Q1_26 / G1_US_HU_JUL2025
    chtr_occ_share = A1_CHTR_PASSINGS_Q1_26 / G2_US_OCC_HU_Q1_26
    add("G3", "Charter passings / US housing units", chtr_hu_share, "DERIVED G1,A1 — conversion line")
    add("G4", "Charter passings / occupied HU", chtr_occ_share, "DERIVED G2,A1 — conversion line")
    add("G5", "AT&T+Verizon overlap of Charter footprint (NOT smaller)", A17_ATT_OVERLAP + A18_VZ_OVERLAP, "RETRIEVED 10-K; do not use as small-fiber")

    coop_survey_hp = N9_COOP_SURVEY_N * N10_COOP_AVG_HP
    coop_scale_hp = N12_COOP_DEPLOYED * N10_COOP_AVG_HP
    retrieved_indie = N6_METRONET_NOV25 + N7_KINETIC_HP + N8_BRIGHTSPEED_YE24 + coop_survey_hp
    est_add = (coop_scale_hp - coop_survey_hp) + K10_MUNI_HP + K11_GOOGLE_OTHER_HP
    nat_small = retrieved_indie + est_add
    nat_commit = 20_000_000  # round UP against (higher homes → higher scaled $)

    add("G6", "Co-op survey homes (78 × 29,600)", coop_survey_hp, "RETRIEVED-anchored; NRTC+NRECA funded")
    add("G7", "Co-op scaled to 240 members (ESTIMATED)", coop_scale_hp, "ESTIMATED; applies survey mean to all 240")
    add("G8", "MetroNet + Kinetic + Brightspeed HP", N6_METRONET_NOV25 + N7_KINETIC_HP + N8_BRIGHTSPEED_YE24, "RETRIEVED 10-K-adjacent press")
    add("G9", "Muni HP national (ESTIMATED; ILSR has no total)", K10_MUNI_HP, "ESTIMATED; ILSR-funded map, 400+ networks")
    add("G10", "Google Fiber + other independents (ESTIMATED)", K11_GOOGLE_OTHER_HP, "ESTIMATED")
    add("G11", "National small-fiber HP (ex AT&T/VZ) raw sum", nat_small, "MIXED")
    add("G12", "Committed national small-fiber HP (round UP)", nat_commit, "COMMIT")

    fba_remainder_q1 = N1_FBA_FIBER_HP_YE25 - N3_ATT_FIBER_Q1_26 - N4_VZ_FRONTIER_Q1_26
    add("G13", "FBA YE25 minus AT&T Q1 minus VZ+Frontier", fba_remainder_q1, "DERIVED; INCLUDES cable FTTH — not a small-fiber count")
    add("G14", "Frontier Q3'25 (now Verizon — rival mechanism, not smaller)", N5_FRONTIER_Q3_25, "RETRIEVED; closed 20 Jan 2026")

    naive_chtr = nat_commit * chtr_hu_share
    overlap_est = naive_chtr * K8_IN_POLYGON
    willing = overlap_est * K9_WHOLESALE_WILLING
    add("G15", "Naive Charter HU-share of national small-fiber", naive_chtr, "DERIVED G12×G3 — NOT overlap")
    add("G16", "In-polygon overlap factor", K8_IN_POLYGON, "ESTIMATED — BLOCKING if treated as fact")
    add("G17", "Estimated overlapping small-fiber HP in Charter footprint", overlap_est, "ESTIMATED")
    add("G18", "Wholesale-willing share", K9_WHOLESALE_WILLING, "ESTIMATED — BLOCKING")
    add("G19", "Estimated wholesale-willing overlapping HP", willing, "ESTIMATED")
    add("G20", "BLOCKING INPUT", "Charter-footprint small-fiber passings not disclosed", "none retrieved")

    add("S1", "Scenario LOW overlapping HP (open-access-like)", S_LOW_HP, "SCENARIO")
    add("S2", "Scenario BASE overlapping HP", S_BASE_HP, "SCENARIO")
    add("S3", "Scenario HIGH overlapping HP", S_HIGH_HP, "SCENARIO")

    def scale(hp: int) -> dict:
        subs = hp * K3_TAKE_OA  # if Charter captured ALL connected homes — upper bound
        return {
            "hp": hp,
            "subs": subs,
            "cogs_m": subs * w_commit_yr / 1e6,
            "contrib_m": subs * contrib_base / 1e6,
            "pv_m": subs * pv_commit / 1e6,
            "rural_build_m": hp * A14_RURAL_PER_PASSING / 1e6,
        }

    for label, hp in (("LOW", S_LOW_HP), ("BASE", S_BASE_HP), ("HIGH", S_HIGH_HP)):
        d = scale(hp)
        add(f"S_{label}_subs", f"{label} customers at 40% take (upper bound: 100% ISP share)", d["subs"], "DERIVED ESTIMATED take")
        add(f"S_{label}_cogs", f"{label} annual wholesale COGS $M", d["cogs_m"], "DERIVED")
        add(f"S_{label}_contrib", f"{label} annual contribution $M", d["contrib_m"], "DERIVED")
        add(f"S_{label}_pv", f"{label} 20-yr PV $M", d["pv_m"], "DERIVED")
        add(f"S_{label}_rural", f"{label} rural-build $M if overbuilt instead", d["rural_build_m"], "DERIVED")

    # Comparisons
    upgrade_inc = A12_UPGRADE_Q1_26_M - A13_UPGRADE_Q1_25_M
    add("C1", "FY25 capex $M", A11_CAPEX_FY25_M, "RETRIEVED")
    add("C2", "Q1 upgrade/rebuild increment $M", upgrade_inc, "DERIVED 675-395")
    add("C3", "BASE COGS / FY25 capex", scale(S_BASE_HP)["cogs_m"] / A11_CAPEX_FY25_M, "DERIVED")
    add("C4", "BASE PV / FY25 capex", scale(S_BASE_HP)["pv_m"] / A11_CAPEX_FY25_M, "DERIVED")

    # ----- Dollar-weighted origin of the UNIT headline ($650) -----
    # $650 is 54×12 rounded; 54 is retrieved Jefferson. Remaining opex mix:
    care_r = care_per  # retrieved/retrieved
    est_opex = field_remain_per + K6_TRANSIT_YR + K5_SAC_AMORT
    unit_cogs_ret = w_commit_yr  # tariff-anchored
    # Frame B contribution uses ARPU (retrieved) − COGS (retrieved) − remaining (mixed)
    ret_in_contrib_inputs = arpu_yr_commit + w_commit_yr + care_per
    est_in_contrib_inputs = field_remain_per + K6_TRANSIT_YR + K5_SAC_AMORT
    _, ret_share, est_share = tag_dollars(ret_in_contrib_inputs, est_in_contrib_inputs)
    add("O1", "Retrieved-anchored $ in Frame B inputs (ARPU+COGS+care)", ret_in_contrib_inputs, "weight")
    add("O2", "Estimated $ in Frame B inputs (field remain+transit+SAC)", est_in_contrib_inputs, "weight")
    add("O3", "Dollar-weighted retrieved share of Frame B inputs", 100.0 * ret_share, "weight")
    add("O4", "Dollar-weighted estimated share of Frame B inputs", 100.0 * est_share, "weight")

    # Scaled BASE total: homes are estimated
    base = scale(S_BASE_HP)
    # COGS total = estimated homes × retrieved rate
    _, ret_s, est_s = tag_dollars(0.0, base["cogs_m"])  # homes estimated → 100% estimated dollars
    add("O5", "BASE annual COGS $M is estimated-homes × retrieved rate", base["cogs_m"], "homes ESTIMATED")
    add("O6", "Estimated share of any scaled total (homes unretrieved)", 100.0, "weight — blocking")

    # ----- Sensitivity of Frame B contribution (leverage ranking) -----
    def contrib(w_yr, remain):
        return arpu_yr_commit - w_yr - remain

    base_c = contrib(w_commit_yr, remain_opex)
    sens = []
    for name, lo, hi, is_est in [
        ("Wholesale MRC (UTOPIA $30 → 3G $117)", w_low_yr, w_high_yr, False),
        ("Internet ARPU ($70.72 res-alloc vs $65.86 total)", arpu_yr_resalloc, arpu_yr_tot, False),
        ("Residual field share (10% → 50%)", field_owned_per * 0.10, field_owned_per * 0.50, True),
        ("SAC amort ($0 → $150)", 0.0, 150.0, True),
        ("Transit ($0 → $96)", 0.0, 96.0, True),
        ("WACC on Frame A PV (6% → 10%)", None, None, True),
        ("Take rate Frame A $/passing (25% → 55%)", 0.25, 0.55, True),
        ("In-polygon overlap (20% → 60%) on scaled $", 0.20, 0.60, True),
    ]:
        if name.startswith("Wholesale"):
            c_lo = contrib(lo, remain_opex)
            c_hi = contrib(hi, remain_opex)
            swing = abs(c_hi - c_lo) / 2.0
            sens.append((swing, name, c_lo, c_hi, "COGS analog", is_est))
        elif name.startswith("Internet"):
            # hold COGS+remain; swap ARPU
            c_lo = lo - w_commit_yr - remain_opex
            c_hi = hi - w_commit_yr - remain_opex
            swing = abs(c_hi - c_lo) / 2.0
            sens.append((swing, name, c_lo, c_hi, "ARPU identity", is_est))
        elif name.startswith("Residual"):
            c_lo = contrib(w_commit_yr, care_per + lo + K6_TRANSIT_YR + K5_SAC_AMORT)
            c_hi = contrib(w_commit_yr, care_per + hi + K6_TRANSIT_YR + K5_SAC_AMORT)
            swing = abs(c_hi - c_lo) / 2.0
            sens.append((swing, name, c_lo, c_hi, "ESTIMATED", is_est))
        elif name.startswith("SAC"):
            c_lo = contrib(w_commit_yr, remain_opex - K5_SAC_AMORT + lo)
            c_hi = contrib(w_commit_yr, remain_opex - K5_SAC_AMORT + hi)
            swing = abs(c_hi - c_lo) / 2.0
            sens.append((swing, name, c_lo, c_hi, "ESTIMATED", is_est))
        elif name.startswith("Transit"):
            c_lo = contrib(w_commit_yr, remain_opex - K6_TRANSIT_YR + lo)
            c_hi = contrib(w_commit_yr, remain_opex - K6_TRANSIT_YR + hi)
            swing = abs(c_hi - c_lo) / 2.0
            sens.append((swing, name, c_lo, c_hi, "ESTIMATED", is_est))
        elif name.startswith("WACC"):
            pv_lo = annuity_pv(w_commit_yr, 0.06, 20)
            pv_hi = annuity_pv(w_commit_yr, 0.10, 20)
            swing = abs(pv_hi - pv_lo) / 2.0
            sens.append((swing, name, pv_lo, pv_hi, "Frame A $", is_est))
        elif name.startswith("Take"):
            v_lo = pv_commit * lo
            v_hi = pv_commit * hi
            swing = abs(v_hi - v_lo) / 2.0
            sens.append((swing, name, v_lo, v_hi, "Frame A $/passing", is_est))
        elif name.startswith("In-polygon"):
            naive = nat_commit * chtr_hu_share
            v_lo = naive * lo * K9_WHOLESALE_WILLING * w_commit_yr / 1e6 * K3_TAKE_OA
            v_hi = naive * hi * K9_WHOLESALE_WILLING * w_commit_yr / 1e6 * K3_TAKE_OA
            swing = abs(v_hi - v_lo) / 2.0
            sens.append((swing, name, v_lo, v_hi, "scaled $M", is_est))

    sens.sort(key=lambda x: -x[0])
    add("L0", "Sensitivity ranking (swing units vary — see labels)", "see L1+", "rank")
    for i, (swing, name, lo, hi, unit, is_est) in enumerate(sens, 1):
        add(f"L{i}", f"{name} [{unit}]", f"lo={lo:,.0f} hi={hi:,.0f} swing±{swing:,.0f} {'EST' if is_est else 'RET'}", "leverage")

    # Shared assumptions between builds
    add("X1", "SHARED: wholesale MRC $54 (Jefferson) feeds Frame B COGS and Frame A lit PV", "correlation by construction", "disclose")
    add("X2", "NOT SHARED: dark IRU Laurinburg/Decatur vs Grant/Jefferson MRC vs ARPU", "real cross-check", "disclose")
    add("X3", "Dark IRU $600/passing vs lit PV $6,400/connected disagree because they are different products", "finding", "disclose")

    # Print
    print("=" * 88)
    print("SMALL-FIBER LICENSING COST  |  Q1 2026 anchor")
    print("Deal: wholesale/open-access/IRU last-mile on non-AT&T/non-Verizon fiber")
    print("=" * 88)
    for rid, label, val, origin in rows:
        print(f"{rid:16}  {label[:62]:62}  {str(val)[:28]:28}  {origin}".encode("ascii", "replace").decode("ascii"))
    print("=" * 88)
    print("HEADLINE")
    print(f"  Frame B: ${w_commit_yr:.0f}/customer-year wholesale  (range ${w_low_yr:.0f}-{w_high_yr:.0f})")
    print(f"           vs ${arpu_yr_commit:.0f} Internet ARPU  → contribution ${contrib_base:,.0f}/sub-year")
    print(f"           commit contribution ${contrib_commit:,.0f}/sub-year (round against)")
    print(f"  Frame A: ${pv_commit:,.0f} 20-yr PV per connected home  (lit wholesale @ 8%)")
    print(f"           dark-IRU cross-check ${dark_commit:,.0f}/passing (NOT last-mile; shares no tariff)")
    print(f"  Blocking: Charter-footprint small-fiber passings NOT disclosed")
    print(f"  Scenarios overlapping HP: {S_LOW_HP/1e3:.0f}k / {S_BASE_HP/1e3:.0f}k / {S_HIGH_HP/1e3:.0f}k")
    print(f"  BASE annual COGS ${base['cogs_m']:.0f}M on {base['subs']/1e3:.0f}k subs (40% take, 100% ISP share = upper bound)")
    print(f"  Dollar-weighted Frame B inputs retrieved {100*ret_share:.0f}% / estimated {100*est_share:.0f}%")
    print(f"  Scaled totals: homes unretrieved → treat 100% of scaled $ as estimated")
    print(f"  Beats rural $5,900/passing on access PV per CR ({pv_commit:,.0f} vs {rural_cr:,.0f}) but FAILS contribution")
    print(f"  54k × ${w_commit_yr:.0f} = ${cogs_54k_m:.1f}M/yr COGS; contribution ${contrib_54k_m:.1f}M/yr")
    print(f"  FY25 capex ${A11_CAPEX_FY25_M/1e3:.1f}B; Q1 upgrade increment ${upgrade_inc:.0f}M")
    print("=" * 88)

    # Assertions so memo cannot drift
    assert abs(arpu_mo_tot - 65.86) < 0.05, arpu_mo_tot
    assert abs(arpu_mo_resalloc - 70.72) < 0.05, arpu_mo_resalloc
    assert abs(w_base_yr - 648.0) < 0.01
    assert w_commit_yr == 650.0
    assert arpu_yr_commit == 790.0
    assert pv_commit == 6400.0
    assert abs(pv_connected - 6378) < 30  # 650 * 9.8181 ≈ 6382
    assert contrib_base < 0
    assert upgrade_inc == 280.0
    print("ASSERTIONS OK")


if __name__ == "__main__":
    main()
