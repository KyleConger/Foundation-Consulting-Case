"""Recompute numbers in Kishore Decisions Analyses.docx vs CORE-INFORMATION.

Kishore committed: Q1 Internet -120k; Q2 -172k; capex +19%; FCF -12.3%;
combined network >70M homes; Cox debt ~$12B. EBITDA 'weakened' (unquantified).
"""

from __future__ import annotations

CORE = {
    "q1_2026_internet_net_adds_k": -120,  # Ex99.1 Q1 2026
    "q2_2026_internet_net_adds_k": -172,  # Ex99.1 Q2 2026 (later public fact)
    "q1_2026_capex_m": 2855,  # Ex99.1 table
    "q1_2025_capex_m": 2399,
    "q1_2026_fcf_m": 1372,
    "q1_2025_fcf_m": 1564,
    "q1_2026_ebitda_m": 5637,
    "q1_2025_ebitda_m": 5763,
    "q1_2026_passings_k": 58661,  # Ex99.1 Q1 2026
    "cox_passings_m": 12.0,  # Cox PR / 10-K: ~12 million
    "cox_customers_m": 6.0,  # Cox PR: 6 million existing customers
    "cox_net_debt_10k_b": 12.6,  # 10-K FY2025
    "cox_net_debt_q2_b": 12.4,  # 10-Q Q2 2026 update
    "q1_2025_one_time_ebitda_m": 75,  # 10-Q Q1 2026 base-period item
}

KISHORE = {
    "q1_internet_k": -120_000 / 1000,
    "q2_internet_k": -172_000 / 1000,
    "capex_pct": 19.0,
    "fcf_pct": -12.3,
    "combined_homes_m": 70.0,  # 'more than 70 million'
    "cox_debt_b": 12.0,  # 'roughly $12 billion'
}

capex_pct = CORE["q1_2026_capex_m"] / CORE["q1_2025_capex_m"] - 1
fcf_pct = CORE["q1_2026_fcf_m"] / CORE["q1_2025_fcf_m"] - 1
ebitda_pct = CORE["q1_2026_ebitda_m"] / CORE["q1_2025_ebitda_m"] - 1
ebitda_ex_base = (CORE["q1_2026_ebitda_m"] - (CORE["q1_2025_ebitda_m"] - CORE["q1_2025_one_time_ebitda_m"])) / (
    CORE["q1_2025_ebitda_m"] - CORE["q1_2025_one_time_ebitda_m"]
)
combined_naive_m = CORE["q1_2026_passings_k"] / 1000 + CORE["cox_passings_m"]
release_round_capex = 2.9 / 2.4 - 1

rows = [
    (
        "Q1 Internet net adds (000s)",
        KISHORE["q1_internet_k"],
        CORE["q1_2026_internet_net_adds_k"],
        "MATCH",
    ),
    (
        "Q2 Internet net adds (000s) — later public fact",
        KISHORE["q2_internet_k"],
        CORE["q2_2026_internet_net_adds_k"],
        "MATCH (not the Q1 assignment print)",
    ),
    (
        "Q1 capex YoY %",
        KISHORE["capex_pct"],
        round(capex_pct * 100, 2),
        "MATCH vs 2,855/2,399; NOT vs rounded $2.9B/$2.4B",
    ),
    (
        "Q1 FCF YoY %",
        KISHORE["fcf_pct"],
        round(fcf_pct * 100, 2),
        "MATCH CORE (12.3%); decisions.md rounds to -12%",
    ),
    (
        "Q1 Adj. EBITDA YoY % (he said 'weakened' only)",
        None,
        round(ebitda_pct * 100, 2),
        "True direction; unquantified; Q1'25 had $75M one-time",
    ),
    (
        "Combined homes (million passings, naive add)",
        KISHORE["combined_homes_m"],
        round(combined_naive_m, 2),
        "OK as PR-style add; no overlap line; not a net-add closer",
    ),
    (
        "Cox assumed net debt ($B)",
        KISHORE["cox_debt_b"],
        CORE["cox_net_debt_10k_b"],
        "UNDERSTATES 10-K $12.6B / Q2 10-Q $12.4B",
    ),
]

print("Kishore vs CORE-INFORMATION")
print("-" * 88)
for name, k, core, note in rows:
    k_s = "—" if k is None else k
    print(f"{name:48} kishore={k_s!s:>8}  core={core!s:>8}  {note}")

print()
print(f"capex exact: {CORE['q1_2026_capex_m']}/{CORE['q1_2025_capex_m']} - 1 = {capex_pct:.6%}")
print(f"capex if $2.9B/$2.4B rounded: {release_round_capex:.6%}")
print(f"fcf exact: {CORE['q1_2026_fcf_m']}/{CORE['q1_2025_fcf_m']} - 1 = {fcf_pct:.6%}")
print(f"ebitda exact: {CORE['q1_2026_ebitda_m']}/{CORE['q1_2025_ebitda_m']} - 1 = {ebitda_pct:.6%}")
print(
    "ebitda if strip $75M Q1'25 one-time from base: "
    f"{CORE['q1_2026_ebitda_m']} vs {CORE['q1_2025_ebitda_m'] - CORE['q1_2025_one_time_ebitda_m']} "
    f"= {ebitda_ex_base:.6%}"
)
print(f"naive combined passings: {CORE['q1_2026_passings_k']/1000:.3f} + {CORE['cox_passings_m']:.1f} = {combined_naive_m:.3f}M")
print(f"Cox debt gap vs 10-K: {KISHORE['cox_debt_b'] - CORE['cox_net_debt_10k_b']:+.1f}B")
print(f"Cox debt gap vs Q2 10-Q: {KISHORE['cox_debt_b'] - CORE['cox_net_debt_q2_b']:+.1f}B")
