"""
Build Analysis/CHTR-MBB-Financial-Analyses.xlsx — all 9 MBB analyses.

Assignment still anchors to Q1 2026. Q2 2026 is a later public fact and is labeled.
Blue inputs = labeled assumptions. Black = disclosed or formula.
Georgia throughout (team convention).
"""
from __future__ import annotations

from copy import copy
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.styles.fonts import DEFAULT_FONT

DEFAULT_FONT.name = GEORGIA if False else "Georgia"
DEFAULT_FONT.size = 10
from openpyxl.utils import get_column_letter
from openpyxl.chart import BarChart, LineChart, Reference, ScatterChart, Series
from openpyxl.chart.label import DataLabelList
from openpyxl.chart.marker import Marker
from openpyxl.chart.series import SeriesLabel
from openpyxl.chart.shapes import GraphicalProperties
from openpyxl.drawing.line import LineProperties
from openpyxl.chart.trendline import Trendline
from openpyxl.workbook.defined_name import DefinedName

OUT = Path(__file__).resolve().parent / "CHTR-MBB-Financial-Analyses.xlsx"

# --- styles ---
GEORGIA = "Georgia"
thin = Border(
    left=Side(style="thin", color="B0B0B0"),
    right=Side(style="thin", color="B0B0B0"),
    top=Side(style="thin", color="B0B0B0"),
    bottom=Side(style="thin", color="B0B0B0"),
)
font = Font(name=GEORGIA, size=10)
font_b = Font(name=GEORGIA, size=10, bold=True)
font_title = Font(name=GEORGIA, size=16, bold=True)
font_h = Font(name=GEORGIA, size=12, bold=True, color="FFFFFF")
font_sec = Font(name=GEORGIA, size=11, bold=True)
font_blue = Font(name=GEORGIA, size=10, color="0000FF")  # assumption
font_blue_b = Font(name=GEORGIA, size=10, bold=True, color="0000FF")
font_note = Font(name=GEORGIA, size=9, italic=True, color="595959")
fill_head = PatternFill("solid", fgColor="1F4E79")
fill_sec = PatternFill("solid", fgColor="2E75B6")
fill_disc = PatternFill("solid", fgColor="E2EFDA")  # disclosed
fill_assump = PatternFill("solid", fgColor="DDEBF7")  # assumption
fill_calc = PatternFill("solid", fgColor="FFF2CC")  # calculated
fill_warn = PatternFill("solid", fgColor="FCE4D6")
fill_fail = PatternFill("solid", fgColor="F8CBAD")
fill_pass = PatternFill("solid", fgColor="C6EFCE")
fill_later = PatternFill("solid", fgColor="E2D5F1")  # later public fact
fill_alt = PatternFill("solid", fgColor="F2F2F2")
wrap = Alignment(wrap_text=True, vertical="center")
left = Alignment(wrap_text=True, vertical="center", horizontal="left")
right = Alignment(vertical="center", horizontal="right")


def apply_font(ws):
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.page_setup.orientation = "landscape"
    ws.sheet_view.showGridLines = False
    ws.freeze_panes = "A2"
    ws.sheet_properties.tabColor = "1F4E79"


def style_range_georgia(ws):
    for row in ws.iter_rows():
        for c in row:
            if c.font is None or c.font.name != GEORGIA:
                bold = c.font.bold if c.font else False
                color = c.font.color if c.font else None
                size = c.font.size if c.font and c.font.size else 10
                italic = c.font.italic if c.font else False
                c.font = Font(name=GEORGIA, size=size, bold=bold, italic=italic, color=color)


def put(ws, r, c, value, *, kind="disc", fmt=None, bold=False, width_note=None):
    cell = ws.cell(r, c, value)
    if kind == "assump":
        cell.font = font_blue_b if bold else font_blue
        cell.fill = fill_assump
    elif kind == "calc":
        cell.font = font_b if bold else font
        cell.fill = fill_calc
    elif kind == "head":
        cell.font = font_h
        cell.fill = fill_head
        cell.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
    elif kind == "sec":
        cell.font = Font(name=GEORGIA, size=11, bold=True, color="FFFFFF")
        cell.fill = fill_sec
    elif kind == "later":
        cell.font = font
        cell.fill = fill_later
    elif kind == "note":
        cell.font = font_note
        cell.alignment = left
    elif kind == "fail":
        cell.font = font_b if bold else font
        cell.fill = fill_fail
    elif kind == "pass":
        cell.font = font_b if bold else font
        cell.fill = fill_pass
    elif kind == "warn":
        cell.font = font_b if bold else font
        cell.fill = fill_warn
    else:
        cell.font = font_b if bold else font
        if kind == "disc":
            cell.fill = fill_disc
    if fmt:
        cell.number_format = fmt
    cell.alignment = wrap if kind in ("head", "note") else Alignment(vertical="center")
    cell.border = thin
    return cell


def widths(ws, mapping):
    for col, w in mapping.items():
        ws.column_dimensions[col].width = w


def header_row(ws, r, labels):
    for i, lab in enumerate(labels, 1):
        put(ws, r, i, lab, kind="head")
    ws.row_dimensions[r].height = 28


def section(ws, r, c, text, span=8):
    put(ws, r, c, text, kind="sec")
    if span > 1:
        ws.merge_cells(start_row=r, start_column=c, end_row=r, end_column=c + span - 1)


def bisection(f, lo, hi, n=80):
    for _ in range(n):
        mid = (lo + hi) / 2
        if f(mid) > 0:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2


def levered_pv(fcf0, g, ke, g_term, years=5):
    """PV of growing FCF for `years` then Gordon terminal on year-N FCF."""
    pv = 0.0
    for t in range(1, years + 1):
        pv += fcf0 * (1 + g) ** t / (1 + ke) ** t
    fcf_n = fcf0 * (1 + g) ** years
    if ke <= g_term:
        return float("inf")
    tv = fcf_n * (1 + g_term) / (ke - g_term)
    pv += tv / (1 + ke) ** years
    return pv


def gordon_g(price, fcf0, ke):
    # P = FCF0*(1+g)/(ke-g)  => g = (P*ke - FCF0)/(P + FCF0)
    return (price * ke - fcf0) / (price + fcf0)


def implied_stage_g(target, fcf0, ke, g_term, years=5):
    def f(g):
        return levered_pv(fcf0, g, ke, g_term, years) - target

    # value rises with g
    return bisection(lambda g: -f(g) if False else (levered_pv(fcf0, g, ke, g_term, years) - target), -0.45, 0.25)


def implied_stage_g_ok(target, fcf0, ke, g_term, years=5):
    def err(g):
        return levered_pv(fcf0, g, ke, g_term, years) - target

    lo, hi = -0.45, 0.25
    # err increases with g; we want err=0. If err(lo)>0 target is below even crash g
    if err(lo) > 0:
        return lo
    if err(hi) < 0:
        return hi
    return bisection(err, lo, hi)


# ---------------------------------------------------------------------------
# Disclosed inputs (dollars in millions unless noted)
# ---------------------------------------------------------------------------
SHARES_YE25 = 126_631_549
SHARES_Q1 = 122_984_536
SHARES_Q2 = 119_277_492  # later
PX_APR23 = 241.78
PX_APR24 = 180.13
PX_JAN30 = 206.12
PX_JUL23 = 126.50
PX_JUL24 = 123.31  # later

REV_FY25, REV_FY24 = 54774, 55085
EBIT_FY25 = 12908  # income from operations
DA_FY25 = 8711
INT_FY25 = 5042
TAX_FY25 = 1692
NI_FY25 = 4987
NCI_NI_FY25 = 779
EBITDA_FY25 = 22708
EBITDA_FY24 = 22569
FCF_FY25 = 5004
FCF_FY24 = 4257
OCF_FY25 = 16077
CAPEX_FY25 = 11659
CAPEX_FY24 = 11269

# Q1 2026
REV_Q1, REV_Q1_LY = 13597, 13735
INTL_REV_Q1, INTL_REV_Q1_LY = 5852, 5930
MOB_REV_Q1, MOB_REV_Q1_LY = 1052, 914
EBITDA_Q1, EBITDA_Q1_LY = 5637, 5763
FCF_Q1, FCF_Q1_LY = 1372, 1564
FCF_LTM_Q1, FCF_LTM_Q1_LY = 4812, 5463
CAPEX_Q1 = 2855
NI_Q1 = 1163
NCI_NI_Q1 = 200
INT_Q1 = 1256
TAX_Q1 = 465
EBIT_Q1 = 3208
DA_Q1 = 2211

# Q2 2026 later
INTL_REV_Q2, INTL_REV_Q2_LY = 5776, 5969
MOB_REV_Q2 = 1095
EBITDA_Q2, EBITDA_Q2_LY = 5449, 5693
FCF_Q2, FCF_Q2_LY = 969, 1046
CAPEX_Q2 = 2871
NI_Q2 = 1292

# FY revenue mix
REV_INTL_25, REV_INTL_24 = 23765, 23360
REV_MOB_25, REV_MOB_24 = 3762, 3083
REV_VID_25, REV_VID_24 = 13703, 15129
REV_VOICE_25 = 1350
REV_SMB_25 = 4346
REV_MM_25 = 2969
REV_ADS_25 = 1468
REV_OTH_25, REV_OTH_24 = 3411, 3042
VOL_INTL_25, MIX_INTL_25 = -380, 785  # 10-K residential Internet

# costs
PROG_25, PROG_24 = 8822, 9653
OCOR_25, OCOR_24 = 6704, 6351
FIELD_25 = 5165
CUST_25 = 3115
MKT_25 = 3782
OTHER_EXP_25 = 4459
STOCK_25 = 673
TRANS_25 = 19
OPEX_25 = 32739
TAX_RATE_ETR = 0.227
STAT_FED = 0.21
CASH_TAX_25 = 893
WAVG_INT = 0.051  # blended YE2025 disclosed
CREDIT_WAVG = 0.056
NOTES_WAVG = 0.051

# BS Q1
CASH_Q1 = 517
LTD_Q1 = 94414
EIP_Q1 = 1596
NCI_Q1 = 4685
EQ_Q1 = 16385
PPE_Q1 = 47198
FRAN_Q1 = 67471
GW_Q1 = 29710
CASH_YE25 = 477
LTD_YE25 = 94006
CURR_DEBT_YE25 = 750
EIP_YE25 = 1447
NCI_YE25 = 4465
EQ_YE25 = 16054
PPE_YE25 = 46444

# customers 000s restated
INET = {
    "23Q4": 30590,  # 24Q1 EOP 30518 − (−72)
    "24Q1": 30518,
    "24Q2": 30370,
    "24Q3": 30260,
    "24Q4": 30083,
    "25Q1": 30024,
    "25Q2": 29908,
    "25Q3": 29799,
    "25Q4": 29680,
    "26Q1": 29560,
    "26Q2": 29388,
}
MOB = {
    "24Q1": 8244,
    "24Q2": 8796,
    "24Q3": 9336,
    "24Q4": 9858,
    "25Q1": 10365,
    "25Q2": 10856,
    "25Q3": 11338,
    "25Q4": 11766,
    "26Q1": 12134,
    "26Q2": 12540,
}
INET_ADDS = {
    "24Q1": -72,
    "24Q2": -148,
    "24Q3": -110,
    "24Q4": -177,
    "25Q1": -59,
    "25Q2": -116,
    "25Q3": -109,
    "25Q4": -119,
    "26Q1": -120,
    "26Q2": -172,
}
INET_REV_Q = {
    "23Q1": 5718,
    "23Q2": 5733,
    "23Q3": 5776,
    "23Q4": 5805,
    "24Q1": 5826,
    "24Q2": 5806,
    "24Q3": 5872,
    "24Q4": 5856,
    "25Q1": 5930,
    "25Q2": 5969,
    "25Q3": 5971,
    "25Q4": 5895,
    "26Q1": 5852,
    "26Q2": 5776,
}
FCF_Q = {
    "24Q1": 358,
    "24Q2": 1296,
    "24Q3": 1619,
    "24Q4": 984,
    "25Q1": 1564,
    "25Q2": 1046,
    "25Q3": 1621,
    "25Q4": 773,
    "26Q1": 1372,
    "26Q2": 969,
}
UPG_Q = {
    "24Q1": 481,
    "24Q2": 389,
    "24Q3": 358,
    "24Q4": 543,
    "25Q1": 395,
    "25Q2": 457,
    "25Q3": 484,
    "25Q4": 601,
    "26Q1": 675,
    "26Q2": 657,
}
RURAL_Q = {
    "24Q1": 427,
    "24Q2": 565,
    "24Q3": 577,
    "24Q4": 575,
    "25Q1": 467,
    "25Q2": 543,
    "25Q3": 580,
    "25Q4": 612,
    "26Q1": 426,
    "26Q2": 390,
}
CAPEX_Q = {
    "24Q1": 2791,
    "24Q2": 2853,
    "24Q3": 2563,
    "24Q4": 3062,
    "25Q1": 2399,
    "25Q2": 2874,
    "25Q3": 3051,
    "25Q4": 3335,
    "26Q1": 2855,
    "26Q2": 2871,
}
EBITDA_Q = {
    "24Q1": 5497,
    "24Q2": 5665,
    "24Q3": 5647,
    "24Q4": 5760,
    "25Q1": 5763,
    "25Q2": 5693,
    "25Q3": 5561,
    "25Q4": 5691,
    "26Q1": 5637,
    "26Q2": 5449,
}

QTRS = ["24Q1", "24Q2", "24Q3", "24Q4", "25Q1", "25Q2", "25Q3", "25Q4", "26Q1", "26Q2"]
PRIOR_EOP = {
    "24Q1": INET["23Q4"],
    "24Q2": INET["24Q1"],
    "24Q3": INET["24Q2"],
    "24Q4": INET["24Q3"],
    "25Q1": INET["24Q4"],
    "25Q2": INET["25Q1"],
    "25Q3": INET["25Q2"],
    "25Q4": INET["25Q3"],
    "26Q1": INET["25Q4"],
    "26Q2": INET["26Q1"],
}
LY_Q = {
    "24Q1": "23Q1",
    "24Q2": "23Q2",
    "24Q3": "23Q3",
    "24Q4": "23Q4",
    "25Q1": "24Q1",
    "25Q2": "24Q2",
    "25Q3": "24Q3",
    "25Q4": "24Q4",
    "26Q1": "25Q1",
    "26Q2": "25Q2",
}
# prior-year average customers need LY eop pair
LY_EOP_START = {
    "24Q1": None,  # filled if we have 22Q4; skip or use 23Q1 only
    "24Q2": INET["23Q4"] if False else 30590,  # 23Q1 prior = 23Q0 unknown; use 23Q1 eop as proxy later
}

# Reconstruct 23Q EOP from 24Q1 working backward with disclosed 2024 adds only.
# 23Q4 restated = 30590. 23Q3/Q2/Q1 EOP not needed if we use FY 10-K for 2024 and quarterly from 24Q1.
# For 24Q1 YoY volume we need 23Q1 avg customers. 23Q1 EOP from prior work 30510 (old) — use 10-K path:
# Residential Internet 2025 vs 2024 10-K is the audited volume/mix. Quarterly derived from trending.

# Earnings events
EARN = [
    ("Jan 31 2025 / Q4 24", -177, None, 336.62, 345.49, 2.6, "Losses large, not a new slope"),
    ("Apr 25 2025 / Q1 25", -59, 13, 335.33, 373.65, 11.4, "Mobile/video beat; Internet miss ignored"),
    ("Jul 25 2025 / Q2 25", -116, 32, 380.00, 309.75, -18.5, "Miss vs ~73k expected (Visible Alpha/Reuters)"),
    ("Oct 31 2025 / Q3 25", -109, 1, 230.92, 233.84, 1.3, "EPS miss; open −5.6%"),
    ("Jan 30 2026 / Q4 25", -119, 58, 191.52, 206.12, 7.6, "Almost same adds as Q1 26, opposite tape"),
    ("Apr 24 2026 / Q1 26", -120, -61, 241.78, 180.13, -25.5, "Assignment trigger. CMCSA −12.9% same day"),
    ("Jul 24 2026 / Q2 26", -172, -56, 126.50, 123.31, -2.5, "Later public fact; already de-rated"),
]

# CMCSA
CMCSA_PX_APR23 = 31.64
CMCSA_PX_APR24 = 27.51
CMCSA_SHARES_M = 3572.228  # Class A 3,562.784 + Class B 9.444, Apr 15 2026 10-Q
CMCSA_FCF_Q1 = 3901
CMCSA_EBITDA_Q1 = 7929
CMCSA_RET_APR24 = (27.51 / 31.64) - 1

# Buybacks
BUYBACK_FY25_SH = 17.1  # million shares/units
BUYBACK_FY25_USD = 5400
BUYBACK_Q1_USD = 963
BUYBACK_Q2_USD = 838
BUYBACK_Q1_SH = 4.3
BUYBACK_Q2_SH = 4.0
AUTH_REMAIN_Q2 = 365
CUMUL_BUY_USD = 80600  # through 30 Jun 2026
COX_CASH = 4200  # Q2 10-Q
COX_NET_DEBT = 12400  # Q2 10-Q later; 10-K was 12600
COX_UNITS = 33.6
LEV_Q1 = 4.15
LEV_TARGET_LT = 3.50
LEV_BAND_HI = 4.50
CAPEX_GUIDE_26 = 11400

# LTM Q1
EBITDA_LTM_Q1 = EBITDA_FY25 - EBITDA_Q1_LY + EBITDA_Q1  # 22582
FCF_LTM_Q2 = FCF_LTM_Q1 - FCF_Q2_LY + FCF_Q2  # 4735 later
EBITDA_LTM_Q2 = EBITDA_FY25 - 5691 + EBITDA_Q2  # wait YE includes Q4. LTM Q2 = Q3+Q4+Q1+Q2 2025/26
# YE25 EBITDA 22708 = Q1-Q4 25. LTM Q2 26 = 22708 - 5763 - 5693 + 5637 + 5449
EBITDA_LTM_Q2 = 22708 - 5763 - 5693 + 5637 + 5449

NET_DEBT_CO_Q1 = LTD_Q1 - CASH_Q1  # company-style (ex-EIP): 93897
NET_DEBT_ALL_Q1 = LTD_Q1 + EIP_Q1 - CASH_Q1

# --- WACC assumptions (labeled) ---
RF = 0.043  # ~10Y Apr-2026 order of magnitude
ERP = 0.050  # McKinsey-typical
BETA = 1.05  # levered, labeled
KE = RF + BETA * ERP  # 0.0955
KD = WAVG_INT
TAX_WACC = TAX_RATE_ETR
# Target structure: 3.5x EBITDA net debt, mid-cycle EV at 6.5x EBITDA
MID_EBITDA_MULT = 6.5
TARGET_LEV = 3.5
MID_EV = MID_EBITDA_MULT * EBITDA_LTM_Q1
TARGET_ND = TARGET_LEV * EBITDA_LTM_Q1
TARGET_EQ = MID_EV - TARGET_ND - NCI_Q1
WACC = (TARGET_EQ / MID_EV) * KE + (TARGET_ND / MID_EV) * KD * (1 - TAX_WACC) + (NCI_Q1 / MID_EV) * KE

# Current-weight WACC (circular; shown as sensitivity only)
MKT_APR23 = PX_APR23 * SHARES_Q1 / 1e6  # $M
MKT_APR24 = PX_APR24 * SHARES_Q1 / 1e6
EV_APR23 = MKT_APR23 + NET_DEBT_CO_Q1 + NCI_Q1
EV_APR24 = MKT_APR24 + NET_DEBT_CO_Q1 + NCI_Q1
WACC_SPOT_23 = (MKT_APR23 / EV_APR23) * KE + (NET_DEBT_CO_Q1 / EV_APR23) * KD * (1 - TAX_WACC) + (NCI_Q1 / EV_APR23) * KE

G_TERM = 0.000  # mature cable; labeled
STAGE_YEARS = 5

# Unit-econ assumptions
MOB_WHOLESALE = 0.60  # of mobile *service* revenue
DEV_REV_FY25 = 2200  # of Other $3,411; labeled (10-K says Other +$369 primarily devices)
DEV_MARGIN = 0.00
INET_CHURN_M = 0.015  # monthly, labeled (not disclosed)
MOB_CHURN_M = 0.020
MKT_SHARE_INET = 0.40
MKT_SHARE_MOB = 0.20
CPE_SHARE_INET = 0.70
DISC_R = 0.08  # unit NPV discount, labeled
# Shared opex allocation for crude SOP (labeled)
FIELD_INET, FIELD_MOB = 0.70, 0.05
CUST_INET, CUST_MOB = 0.55, 0.15
MKT_INET, MKT_MOB = 0.40, 0.20
OTHX_INET, OTHX_MOB = 0.40, 0.08
# residual other COR after devices and mobile wholesale
# OCOR = devices + mobile wholesale + residual (franchise, ads, sports, internet backbone)
# residual allocated 50% internet / 10% mobile / 40% video+ads

# Initiative assumptions (illustrative — not a team recommendation)
INIT_A_OPEX = 2000  # $M over 24 months to get Internet to zero net adds
INIT_A_MONTHS = 24
INIT_B_CAPEX = 8000  # competitive-footprint quality / targeted fiber, 5 years
INIT_B_YEARS = 5
INIT_B_CAPTURE = 0.50  # of full-potential equity gap
INIT_C_BUYBACK_CUT = 5400  # stop FY-run-rate buybacks for a year

# Full-potential paths
INET_Q1 = 29560
CONTRIB_INET_Y = None  # filled after unit econ
ARPU_INET_M = None
ARPU_MOB_M = None


def avg_cust(eop0, eop1):
    return (eop0 + eop1) / 2.0


def bridge_quarter(q):
    eop = INET[q]
    prior = PRIOR_EOP[q]
    avg = avg_cust(prior, eop)
    ly = LY_Q[q]
    # LY eop pair
    if ly.startswith("23"):
        # 23Q1–Q3 EOP not in restated series except 23Q4. Use revenue/customer identity on 23Q4 for 24Q4 only;
        # for 24Q1–Q3 use FY-trending revenue and approximate LY avg from linear path 23Q4 back.
        # Conservative: use 23Q4 EOP as end, and 23Qn start = 23Q4 + remaining 2024-style.
        # Better: 10-K says 2024 YE 30,083 and 2025 YE 29,680. For 2023 YE restated:
        # 24Q1 adds -72 from 30,590. For 23Q1–Q3 we do not have restated EOP.
        # Use only quarters where both sides exist: 25Q1 onward have full LY restated EOP.
        # For 24Q1–24Q4 construct LY avg from 23 revenue / implied rpc using 23Q4 and a 23 start.
        pass
    ly_map_eop_end = {
        "23Q1": 30680,  # assumption: interpolate 23Q4 30590 backward at ~+30k/q (pre-decline). LABELED.
        "23Q2": 30650,
        "23Q3": 30620,
        "23Q4": 30590,
        "24Q1": 30518,
        "24Q2": 30370,
        "24Q3": 30260,
        "24Q4": 30083,
        "25Q1": 30024,
        "25Q2": 29908,
        "25Q3": 29799,
        "25Q4": 29680,
    }
    ly_map_eop_start = {
        "23Q1": 30720,
        "23Q2": 30680,
        "23Q3": 30650,
        "23Q4": 30620,
        "24Q1": 30590,
        "24Q2": 30518,
        "24Q3": 30370,
        "24Q4": 30260,
        "25Q1": 30083,
        "25Q2": 30024,
        "25Q3": 29908,
        "25Q4": 29799,
    }
    avg_ly = avg_cust(ly_map_eop_start[ly], ly_map_eop_end[ly])
    rev = INET_REV_Q[q]
    rev_ly = INET_REV_Q[ly]
    rpc_ly = rev_ly / avg_ly  # $000 per thousand customers = $ per customer
    volume = (avg - avg_ly) * rpc_ly
    price = (rev - rev_ly) - volume
    return {
        "avg": avg,
        "avg_ly": avg_ly,
        "rev": rev,
        "rev_ly": rev_ly,
        "d_rev": rev - rev_ly,
        "volume": volume,
        "price": price,
        "rpc_ly": rpc_ly,
    }


def main():
    global CONTRIB_INET_Y, ARPU_INET_M, ARPU_MOB_M

    wb = Workbook()

    # =====================================================================
    # 01 Assumptions (build first so other sheets can hardcode computed
    # values that are also shown as identities on this sheet)
    # =====================================================================
    # Pre-compute identities
    avg_inet_25 = avg_cust(INET["24Q4"], INET["25Q4"])
    avg_inet_24 = avg_cust(INET["23Q4"], INET["24Q4"])
    avg_mob_25 = avg_cust(MOB["24Q4"], MOB["25Q4"])
    avg_mob_q1 = avg_cust(MOB["25Q4"], MOB["26Q1"])
    avg_inet_q1 = avg_cust(INET["25Q4"], INET["26Q1"])
    ARPU_INET_M = REV_INTL_25 / avg_inet_25 / 12  # $ per customer
    ARPU_MOB_M = REV_MOB_25 / avg_mob_25 / 12
    ARPU_INET_Q1 = INTL_REV_Q1 / avg_inet_q1 / 3
    ARPU_MOB_Q1 = MOB_REV_Q1 / avg_mob_q1 / 3

    nopat_fy25 = EBIT_FY25 * (1 - TAX_RATE_ETR)
    ic_ye25 = EQ_YE25 + NCI_YE25 + CURR_DEBT_YE25 + LTD_YE25 + EIP_YE25 - CASH_YE25
    ic_q1 = EQ_Q1 + NCI_Q1 + LTD_Q1 + EIP_Q1 - CASH_Q1
    roic_fy25 = nopat_fy25 / ic_ye25
    ep_fy25 = (roic_fy25 - WACC) * ic_ye25

    # Mobile / Internet allocated EBITDA (crude SOP)
    mob_wholesale_usd = REV_MOB_25 * MOB_WHOLESALE
    residual_ocor = OCOR_25 - DEV_REV_FY25 - mob_wholesale_usd
    if residual_ocor < 0:
        residual_ocor = 0
    inet_ocor = residual_ocor * 0.50
    mob_ocor_res = residual_ocor * 0.10
    inet_ebitda = (
        REV_INTL_25
        - inet_ocor
        - FIELD_25 * FIELD_INET
        - CUST_25 * CUST_INET
        - MKT_25 * MKT_INET
        - OTHER_EXP_25 * OTHX_INET
    )
    mob_ebitda = (
        REV_MOB_25
        - mob_wholesale_usd
        - mob_ocor_res
        - FIELD_25 * FIELD_MOB
        - CUST_25 * CUST_MOB
        - MKT_25 * MKT_MOB
        - OTHER_EXP_25 * OTHX_MOB
        + DEV_REV_FY25 * DEV_MARGIN
    )
    # Video stub: programming + leftover shared
    vid_ebitda = REV_VID_25 - PROG_25 - residual_ocor * 0.40 - FIELD_25 * 0.15 - CUST_25 * 0.15 - MKT_25 * 0.15 - OTHER_EXP_25 * 0.15

    CONTRIB_INET_Y = (REV_INTL_25 - inet_ocor - FIELD_25 * FIELD_INET * 0.5) / avg_inet_25
    # per-customer annual contribution after direct + half of allocated field (avoid double counting)
    # Cleaner unit contribution: product margin before shared corporate
    inet_direct_margin = (REV_INTL_25 - inet_ocor) / avg_inet_25  # $000s / thousand = $ per sub-year
    # avg_inet_25 is in thousands, REV in $M → $M / thousands = $000 per sub. *1000 = $ per sub
    inet_rev_per = REV_INTL_25 / avg_inet_25 * 1000  # $ per sub-year
    inet_ocor_per = inet_ocor / avg_inet_25 * 1000
    inet_contrib_y = inet_rev_per - inet_ocor_per  # after backbone/franchise residual only
    # add half field as variable cost to serve
    inet_field_per = (FIELD_25 * FIELD_INET * 0.50) / avg_inet_25 * 1000
    inet_contrib_y -= inet_field_per
    CONTRIB_INET_Y = inet_contrib_y

    mob_rev_per = REV_MOB_25 / avg_mob_25 * 1000
    mob_wh_per = mob_wholesale_usd / avg_mob_25 * 1000
    mob_contrib_y = mob_rev_per - mob_wh_per

    inet_churn_y = 1 - (1 - INET_CHURN_M) ** 12
    mob_churn_y = 1 - (1 - MOB_CHURN_M) ** 12
    inet_disc = inet_churn_y * avg_inet_25
    inet_net_25 = INET["25Q4"] - INET["24Q4"]  # -403
    inet_gross = inet_disc + inet_net_25  # still ~thousands
    mob_gross = MOB["25Q4"] - MOB["24Q4"]  # 1908 reported adds; treat as net≈gross if churn on growing base
    # more honest: gross = net + churn*avg
    mob_disc = mob_churn_y * avg_mob_25
    mob_gross = (MOB["25Q4"] - MOB["24Q4"]) + mob_disc

    inet_cac = (MKT_25 * MKT_SHARE_INET) / max(inet_gross, 1) * 1000  # $ per gross add
    inet_cpe = (2260 * CPE_SHARE_INET) / max(inet_gross, 1) * 1000
    inet_sac = inet_cac + inet_cpe
    mob_cac = (MKT_25 * MKT_SHARE_MOB) / max(mob_gross, 1) * 1000

    inet_npv = inet_contrib_y / (DISC_R + inet_churn_y) - inet_sac
    mob_npv = mob_contrib_y / (DISC_R + mob_churn_y) - mob_cac

    # Reverse DCF
    g_gord_23 = gordon_g(MKT_APR23, FCF_LTM_Q1, KE)
    g_gord_24 = gordon_g(MKT_APR24, FCF_LTM_Q1, KE)
    g5_23 = implied_stage_g_ok(MKT_APR23, FCF_LTM_Q1, KE, G_TERM, STAGE_YEARS)
    g5_24 = implied_stage_g_ok(MKT_APR24, FCF_LTM_Q1, KE, G_TERM, STAGE_YEARS)
    # also at ke=12% (trajectory risk)
    KE_HI = 0.12
    g_gord_23_hi = gordon_g(MKT_APR23, FCF_LTM_Q1, KE_HI)
    g_gord_24_hi = gordon_g(MKT_APR24, FCF_LTM_Q1, KE_HI)

    # Full potential 8-year UFCF model
    years = list(range(2026, 2034))
    ufcf0 = FCF_FY25 + INT_FY25 * (1 - TAX_RATE_ETR)  # constant-debt identity

    def capex_path(y):
        return {2026: 11400, 2027: 10500, 2028: 8500, 2029: 8200, 2030: 8000, 2031: 8000, 2032: 8000, 2033: 8000}[y]

    def inet_path(scenario, y, start=INET_Q1):
        """Year-end Internet customers (000s)."""
        # start = 31 Mar 2026. Model year-end 2026 = start + 3 remaining quarters + path
        # Simplify: year-end 2025 = 29680; apply annual net adds each year-end.
        eop = INET["25Q4"]
        for yy in range(2026, y + 1):
            if scenario == "base":
                annual = -480 if yy <= 2028 else -320
            elif scenario == "full":
                # linear to 0 by YE2028: 2026 -360, 2027 -180, 2028 0, then 0
                annual = {2026: -360, 2027: -180, 2028: 0}.get(yy, 0)
            else:  # bear
                annual = -600 if yy <= 2028 else -400
            eop = eop + annual
        return eop

    def ebitda_path(scenario, y):
        # volume vs 2025 avg; mix $0 in base/bear, +$200M/yr in full (partial return of 2025 mix)
        eop_y = inet_path(scenario, y)
        eop_prev = INET["25Q4"] if y == 2026 else inet_path(scenario, y - 1)
        avg_y = avg_cust(eop_prev, eop_y)
        vol = (avg_y - avg_inet_25) * (CONTRIB_INET_Y / 1000)  # $M : CONTRIB is $/sub, avg is thousands
        # avg_y thousands * ($/sub) / 1000 = $M. CONTRIB_INET_Y is $/sub-year. avg_y * CONTRIB / 1000 = $M
        vol_m = (avg_y - avg_inet_25) * CONTRIB_INET_Y / 1000
        mix = 200 * (y - 2025) if scenario == "full" else 0
        # other EBITDA drift: video decline −$400M/yr fading; mobile +$150M
        other = -250 * (y - 2025)  # net other drag
        if scenario == "full":
            other = -100 * (y - 2025)
        if scenario == "bear":
            other = -400 * (y - 2025)
        return EBITDA_FY25 + vol_m + mix + other

    def ufcf_path(scenario, y):
        ebitda = ebitda_path(scenario, y)
        # UFCF ≈ EBITDA - cash tax on EBIT - capex, with EBIT ≈ EBITDA - DA, DA ~ $8.7B flat
        ebit = ebitda - DA_FY25
        nopat = ebit * (1 - TAX_RATE_ETR)
        # NWC ~ 0; stock comp add-back skip (conservative)
        return nopat + DA_FY25 - capex_path(y)

    def ev_of(scenario):
        pv = 0.0
        last = 0.0
        for i, y in enumerate(years, 1):
            u = ufcf_path(scenario, y)
            last = u
            pv += u / (1 + WACC) ** i
        tv = last * (1 + G_TERM) / (WACC - G_TERM) if WACC > G_TERM else last / WACC
        pv += tv / (1 + WACC) ** len(years)
        return pv, last

    ev_base, ufcf_base_n = ev_of("base")
    ev_full, ufcf_full_n = ev_of("full")
    ev_bear, ufcf_bear_n = ev_of("bear")
    eq_base = ev_base - NET_DEBT_CO_Q1 - NCI_Q1
    eq_full = ev_full - NET_DEBT_CO_Q1 - NCI_Q1
    eq_bear = ev_bear - NET_DEBT_CO_Q1 - NCI_Q1
    prize = eq_full - eq_base
    prize_vs_mkt = eq_full - MKT_APR24

    # Initiatives
    # A: pay INIT_A_OPEX over 2 years (after tax), capture 80% of prize if run-rate actually changes
    init_a_cost_pv = INIT_A_OPEX * (1 - TAX_RATE_ETR) * (1 / (1 + WACC) + 1 / (1 + WACC) ** 2) / 2 * 2
    # simple: $2B pretax, 50/50 two years, after tax
    init_a_cost_pv = sum(INIT_A_OPEX / 2 * (1 - TAX_RATE_ETR) / (1 + WACC) ** t for t in (1, 2))
    init_a_benefit = 0.80 * prize
    init_a_npv = init_a_benefit - init_a_cost_pv
    # B: $8B capex over 5 years, 50% of prize, delay 3 years to print
    init_b_cost_pv = sum(INIT_B_CAPEX / INIT_B_YEARS / (1 + WACC) ** t for t in range(1, INIT_B_YEARS + 1))
    init_b_benefit = INIT_B_CAPTURE * prize / (1 + WACC) ** 3
    init_b_npv = init_b_benefit - init_b_cost_pv
    # C: wait — keep FCF, no Internet inflection. Equity stays at base. NPV vs doing nothing = 0
    # vs full potential: you forgo the prize. "Value of waiting" = eq_base - MKT_APR24 (maybe undervalued already)
    init_c_npv = eq_base - MKT_APR24  # if the market is wrong on cash but right on trajectory
    init_c_vs_move = -prize  # opportunity cost of not moving

    # Funding box
    fcf_26_assumed = 4800
    lev_room_up = (LEV_BAND_HI - LEV_Q1) * EBITDA_LTM_Q1
    lev_room_down = (LEV_Q1 - LEV_TARGET_LT) * EBITDA_LTM_Q1
    uses_cox = COX_CASH
    uses_init_a = INIT_A_OPEX
    residual_if_cut_bb = fcf_26_assumed - uses_cox  # if buybacks stop

    # Quarterly bridges
    bridges = {q: bridge_quarter(q) for q in QTRS}

    # =====================================================================
    # Workbook
    # =====================================================================
    ws0 = wb.active
    ws0.title = "00_ReadMe"

    # ---------- ReadMe ----------
    apply_font(ws0)
    widths(ws0, {"A": 28, "B": 88, "C": 28, "D": 22})
    put(ws0, 1, 1, "Charter — nine MBB financial analyses", kind="sec")
    ws0.merge_cells("A1:D1")
    ws0["A1"].font = font_title
    ws0["A1"].fill = PatternFill("solid", fgColor="FFFFFF")
    ws0["A1"].border = Border()
    put(
        ws0,
        3,
        1,
        "Purpose",
        kind="note",
    )
    ws0.merge_cells("B3:D3")
    put(
        ws0,
        3,
        2,
        "Complete the McKinsey/Bain toolkit for the MAN6930 CEO engagement: diagnose, then convert a move into equity value, cost, and months-to-print. Analysis — not a filing. Do not copy conclusions into CORE-INFORMATION.md.",
        kind="note",
    )
    rows = [
        (5, "Assignment anchor", "End of Q1 2026 (31 Mar 2026). Later public facts (Q2 2026, Jul 24 print) are purple-tinted and labeled."),
        (6, "Color key", "Green = disclosed figure. Blue font / blue fill = labeled assumption. Yellow = calculated. Orange = caution. Purple = later public fact."),
        (7, "Units", "Customers in thousands. Dollars in millions except per-share, ARPU, and per-sub NPV (those are labeled on the sheet)."),
        (8, "WACC convention", "Target-structure WACC (3.5x net debt / 6.5x mid-cycle EV), not spot market weights. Spot weights are circular after a crash and are shown only as a sensitivity."),
        (9, "What this is not", "Not a team recommendation. Initiative NPV sizes three archetypal moves the diagnosis implies. Pick one, then replace the blue inputs."),
        (10, "Sources", "CHTR 10-K FY2025, 10-Q/Ex99.1 Q1 2026, Ex99.1 Q2 2026; Yahoo close-to-close on earnings dates; CMCSA Ex99.1 Q1 2026 and 10-Q share count; TIKR/Devyara for published CMCSA multiples (labeled)."),
    ]
    for r, a, b in rows:
        put(ws0, r, 1, a, kind="disc", bold=True)
        ws0.merge_cells(start_row=r, start_column=2, end_row=r, end_column=4)
        put(ws0, r, 2, b, kind="note")
        ws0.row_dimensions[r].height = 36

    header_row(ws0, 12, ["#", "Analysis", "Sheet", "Status"])
    catalog = [
        ("1", "Issue tree + hypothesis tests", "02_IssueTree", "Complete"),
        ("2", "Internet revenue bridge — volume vs price/mix", "03_InternetBridge", "Complete"),
        ("3", "Trading comps + earnings-day event study", "04_CompsEvent", "Complete (was partial)"),
        ("4", "Reverse DCF / market-implied expectations", "05_ReverseDCF", "Complete"),
        ("5", "ROIC vs WACC / economic profit + crude SOP", "06_ROIC_EP", "Complete"),
        ("6", "Unit economics — NPV per Internet sub vs mobile line", "07_UnitEconomics", "Complete"),
        ("7", "Full potential vs current trajectory", "08_FullPotential", "Complete"),
        ("8", "Initiative NPV / size the prize", "09_InitiativeNPV", "Complete (illustrative moves)"),
        ("9", "Capital allocation / funding box", "10_FundingBox", "Complete"),
    ]
    for i, row in enumerate(catalog):
        for j, v in enumerate(row, 1):
            put(ws0, 13 + i, j, v, kind="pass" if j == 4 else "disc")
    put(ws0, 23, 1, "Scorecard", kind="note")
    put(ws0, 23, 2, "See 11_Scorecard for pass/fail against a CEO recommendation.", kind="note")
    put(ws0, 25, 1, "Legend (cells)", kind="disc", bold=True)
    put(ws0, 25, 2, "Disclosed", kind="disc")
    put(ws0, 25, 3, "Assumption", kind="assump")
    put(ws0, 25, 4, "Calculated", kind="calc")

    # ---------- Assumptions ----------
    ws = wb.create_sheet("01_Assumptions")
    apply_font(ws)
    widths(ws, {"A": 36, "B": 18, "C": 16, "D": 16, "E": 72})
    put(ws, 1, 1, "Inputs — disclosed vs labeled assumptions", kind="sec")
    ws.merge_cells("A1:E1")
    header_row(ws, 2, ["Item", "Value", "Unit", "Kind", "Source / note"])

    assumps = [
        ("Assignment / prices", None, None, "sec", None),
        ("Class A shares, 31 Mar 2026", SHARES_Q1, "#,##0", "disc", "10-Q Q1 2026"),
        ("Class A shares, 31 Dec 2025", SHARES_YE25, "#,##0", "disc", "10-K FY2025"),
        ("Class A shares, 30 Jun 2026", SHARES_Q2, "#,##0", "later", "10-Q Q2 2026 — later public fact"),
        ("CHTR close 23 Apr 2026 (pre-print)", PX_APR23, "0.00", "disc", "Yahoo Finance daily close"),
        ("CHTR close 24 Apr 2026 (print day)", PX_APR24, "0.00", "disc", "Yahoo Finance daily close"),
        ("CMCSA close 23 Apr 2026", CMCSA_PX_APR23, "0.00", "disc", "Yahoo / contemporaneous (Deadline $31.64)"),
        ("CMCSA close 24 Apr 2026", CMCSA_PX_APR24, "0.00", "disc", "Yahoo / Deadline $27.51"),
        ("CMCSA shares (A+B), 15 Apr 2026, millions", CMCSA_SHARES_M, "0.000", "disc", "CMCSA 10-Q Q1 2026 cover"),
        ("FY2025 / Q1 2026 P&L", None, None, "sec", None),
        ("Revenue FY2025", REV_FY25, "#,##0", "disc", "10-K"),
        ("Internet revenue FY2025", REV_INTL_25, "#,##0", "disc", "10-K Item 7"),
        ("Mobile service revenue FY2025", REV_MOB_25, "#,##0", "disc", "10-K Item 7"),
        ("Video revenue FY2025", REV_VID_25, "#,##0", "disc", "10-K Item 7"),
        ("Other revenue FY2025", REV_OTH_25, "#,##0", "disc", "10-K; +$369 primarily mobile devices"),
        ("Income from operations FY2025", EBIT_FY25, "#,##0", "disc", "10-K"),
        ("D&A FY2025", DA_FY25, "#,##0", "disc", "10-K"),
        ("Interest expense, net FY2025", INT_FY25, "#,##0", "disc", "10-K"),
        ("Income tax expense FY2025", TAX_FY25, "#,##0", "disc", "10-K"),
        ("Effective tax rate FY2025", TAX_RATE_ETR, "0.0%", "disc", "10-K rate reconciliation 22.7%"),
        ("Adj. EBITDA FY2025", EBITDA_FY25, "#,##0", "disc", "Ex99.1 / 10-K non-GAAP"),
        ("Free cash flow FY2025", FCF_FY25, "#,##0", "disc", "Charter non-GAAP"),
        ("FCF LTM Q1 2026", FCF_LTM_Q1, "#,##0", "disc", "Ex99.1 Q1 2026 LTM column"),
        ("Adj. EBITDA Q1 2026", EBITDA_Q1, "#,##0", "disc", "Ex99.1 Q1 2026"),
        ("Adj. EBITDA Q1 2025", EBITDA_Q1_LY, "#,##0", "disc", "Ex99.1 Q1 2026"),
        ("Internet revenue Q1 2026", INTL_REV_Q1, "#,##0", "disc", "Ex99.1 Q1 2026"),
        ("Mobile service revenue Q1 2026", MOB_REV_Q1, "#,##0", "disc", "Ex99.1 Q1 2026"),
        ("Programming cost FY2025", PROG_25, "#,##0", "disc", "10-K note / Ex99.1"),
        ("Other costs of revenue FY2025", OCOR_25, "#,##0", "disc", "10-K — includes mobile wholesale + devices"),
        ("Field & technology FY2025", FIELD_25, "#,##0", "disc", "10-K segment expense table"),
        ("Customer operations FY2025", CUST_25, "#,##0", "disc", "10-K"),
        ("Marketing & residential sales FY2025", MKT_25, "#,##0", "disc", "10-K"),
        ("Other expense FY2025", OTHER_EXP_25, "#,##0", "disc", "10-K"),
        ("Capex FY2025", CAPEX_FY25, "#,##0", "disc", "10-K NCTA total"),
        ("CPE FY2025", 2260, "#,##0", "disc", "10-K"),
        ("Mobile capex FY2025", 267, "#,##0", "disc", "10-K"),
        ("2026 capex guide (ex-Cox)", CAPEX_GUIDE_26, "#,##0", "disc", "Ex99.1 Q1 2026"),
        ("Balance sheet / leverage", None, None, "sec", None),
        ("Cash 31 Mar 2026", CASH_Q1, "#,##0", "disc", "Ex99.1 Q1 2026"),
        ("Long-term debt 31 Mar 2026", LTD_Q1, "#,##0", "disc", "Ex99.1 Q1 2026 (current portion $0)"),
        ("EIP facility 31 Mar 2026", EIP_Q1, "#,##0", "disc", "Ex99.1 Q1 2026 — excluded from company leverage"),
        ("NCI book 31 Mar 2026", NCI_Q1, "#,##0", "disc", "Ex99.1 Q1 2026"),
        ("Charter equity 31 Mar 2026", EQ_Q1, "#,##0", "disc", "Ex99.1 Q1 2026"),
        ("Company net debt (LTD − cash) Q1", NET_DEBT_CO_Q1, "#,##0", "calc", "Matches ~4.15× LTM EBITDA"),
        ("All interest-bearing net debt Q1", NET_DEBT_ALL_Q1, "#,##0", "calc", "Includes EIP"),
        ("Stated leverage Q1 2026", LEV_Q1, "0.00", "disc", "10-Q Q1 2026"),
        ("Long-term leverage target (post-Cox)", LEV_TARGET_LT, "0.00", "disc", "10-K / 10-Q — 3.5× (Q2 text)"),
        ("Leverage band high (pre-close)", LEV_BAND_HI, "0.00", "disc", "4.0–4.5× stated range"),
        ("Blended weighted-avg interest YE2025", WAVG_INT, "0.0%", "disc", "10-K: 5.1% blended"),
        ("Customers (000s, restated)", None, None, "sec", None),
        ("Internet EOP 31 Dec 2025", INET["25Q4"], "#,##0", "disc", "Ex99.1 / 10-K"),
        ("Internet EOP 31 Mar 2026", INET["26Q1"], "#,##0", "disc", "Ex99.1 Q1 2026"),
        ("Internet EOP 30 Jun 2026", INET["26Q2"], "#,##0", "later", "Ex99.1 Q2 2026"),
        ("Mobile EOP 31 Dec 2025", MOB["25Q4"], "#,##0", "disc", "Ex99.1"),
        ("Mobile EOP 31 Mar 2026", MOB["26Q1"], "#,##0", "disc", "Ex99.1 Q1 2026"),
        ("Internet FY2025 10-K volume", VOL_INTL_25, "#,##0", "disc", "10-K: −$380M residential volume"),
        ("Internet FY2025 10-K rate/mix", MIX_INTL_25, "#,##0", "disc", "10-K: +$785M"),
        ("WACC (target structure)", None, None, "sec", None),
        ("Risk-free rate", RF, "0.0%", "assump", "Labeled: ~U.S. 10-year, Apr 2026 order of magnitude — not a print"),
        ("Equity risk premium", ERP, "0.0%", "assump", "McKinsey Valuation typical 4.5–5.5%; use 5.0%"),
        ("Levered equity beta", BETA, "0.00", "assump", "Labeled. High financial leverage; not a Bloomberg print"),
        ("Cost of equity", KE, "0.0%", "calc", "Rf + beta × ERP"),
        ("Cost of debt (pre-tax)", KD, "0.0%", "disc", "YE2025 blended 5.1%"),
        ("Mid-cycle EV / EBITDA", MID_EBITDA_MULT, "0.0", "assump", "Pre-crash cable neighborhood; used only for target weights"),
        ("Target net debt / EBITDA", TARGET_LEV, "0.00", "disc", "Company long-term 3.5×"),
        ("WACC (target weights)", WACC, "0.0%", "calc", "Avoids crash-circular spot weights"),
        ("WACC at Apr 23 spot weights", WACC_SPOT_23, "0.0%", "calc", "Sensitivity only — circular"),
        ("Terminal growth (Gordon / DCF)", G_TERM, "0.0%", "assump", "Mature last-mile; 0% real-ish. Do not use 2.5% GDP"),
        ("High ke (trajectory risk)", KE_HI, "0.0%", "assump", "If the market applies a 12% cost of equity to CHTR"),
        ("Unit economics (labeled)", None, None, "sec", None),
        ("MVNO wholesale / mobile service rev", MOB_WHOLESALE, "0.0%", "assump", "Not disclosed. Cable-MVNO working range 50–70%"),
        ("Device revenue inside Other FY2025", DEV_REV_FY25, "#,##0", "assump", "Other is $3,411; +$369 was primarily devices. $2.2B is a split, not a line item"),
        ("Device margin", DEV_MARGIN, "0.0%", "assump", "Working assumption: pass-through"),
        ("Internet monthly churn", INET_CHURN_M, "0.0%", "assump", "Not disclosed. 1.5%/mo ≈ 16.6% annual"),
        ("Mobile monthly churn", MOB_CHURN_M, "0.0%", "assump", "Not disclosed. 2.0%/mo ≈ 21.5% annual"),
        ("Marketing allocated to Internet", MKT_SHARE_INET, "0.0%", "assump", "Of $3,782M marketing"),
        ("Marketing allocated to mobile", MKT_SHARE_MOB, "0.0%", "assump", "Of $3,782M marketing"),
        ("CPE allocated to Internet", CPE_SHARE_INET, "0.0%", "assump", "Of $2,260M CPE"),
        ("Unit NPV discount rate", DISC_R, "0.0%", "assump", "Separate from WACC; customer-level"),
        ("Field ops to Internet / mobile", f"{FIELD_INET:.0%}/{FIELD_MOB:.0%}", None, "assump", "Labeled allocation — single segment reporter"),
        ("Full potential / initiatives", None, None, "sec", None),
        ("Internet contribution $/sub-year", CONTRIB_INET_Y, "#,##0", "calc", "Internet rev − allocated residual COR − 50% of allocated field, / avg subs"),
        ("Capex 2027 (post-guide)", 10500, "#,##0", "assump", "Network evolution still on; labeled"),
        ("Capex 2028+ (post evolution)", 8500, "#,##0", "assump", "Company: largely complete end-2027"),
        ("Initiative A opex (24 months)", INIT_A_OPEX, "#,##0", "assump", "Retention / price-lock / FWA response — ILLUSTRATIVE"),
        ("Initiative A capture of prize", 0.80, "0.0%", "assump", "If the run-rate actually goes to zero and stays"),
        ("Initiative B capex (5 years)", INIT_B_CAPEX, "#,##0", "assump", "Targeted competitive-footprint quality — ILLUSTRATIVE"),
        ("Initiative B capture of prize", INIT_B_CAPTURE, "0.0%", "assump", "Half the full-potential gap, delayed 3 years"),
        ("Cox cash at close", COX_CASH, "#,##0", "later", "Q2 10-Q ~$4.2B; 10-K was $4.0B cash package"),
        ("Cox net debt assumed", COX_NET_DEBT, "#,##0", "later", "Q2 10-Q ~$12.4B; 10-K $12.6B"),
        ("FY2025 buybacks $", BUYBACK_FY25_USD, "#,##0", "disc", "Ex99.1 FY2025 17.1M shares/units / ~$5.4B"),
        ("Remaining repurchase authority 30 Jun", AUTH_REMAIN_Q2, "#,##0", "later", "Ex-Liberty; Q2 10-Q"),
    ]

    r = 3
    for item, val, fmt, kind, note in assumps:
        if kind == "sec":
            section(ws, r, 1, item, 5)
            r += 1
            continue
        put(ws, r, 1, item, kind="disc")
        put(ws, r, 2, val, kind=kind, fmt=fmt, bold=(kind == "calc"))
        put(ws, r, 3, "see note" if fmt is None else ("$M" if fmt == "#,##0" and "share" not in item.lower() and "ARPU" not in item else ""), kind="note")
        put(ws, r, 4, {"disc": "Disclosed", "assump": "Assumption", "calc": "Calculated", "later": "Later fact"}.get(kind, kind), kind=kind)
        put(ws, r, 5, note or "", kind="note")
        r += 1

    # named-ish key outputs block
    r += 1
    section(ws, r, 1, "Key calculated identities used by every sheet", 5)
    r += 1
    header_row(ws, r, ["Identity", "Value", "Unit", "Kind", "Formula"])
    r += 1
    keys = [
        ("Market cap 23 Apr 2026", MKT_APR23, "#,##0.0", "$M", "241.78 × 122,984,536"),
        ("Market cap 24 Apr 2026", MKT_APR24, "#,##0.0", "$M", "180.13 × 122,984,536"),
        ("EV 23 Apr (co. net debt + NCI)", EV_APR23, "#,##0.0", "$M", "Mkt + 93,897 + 4,685"),
        ("EV 24 Apr (co. net debt + NCI)", EV_APR24, "#,##0.0", "$M", "Mkt + 93,897 + 4,685"),
        ("LTM EBITDA Q1 2026", EBITDA_LTM_Q1, "#,##0", "$M", "22,708 − 5,763 + 5,637"),
        ("Invested capital YE2025 (book)", ic_ye25, "#,##0", "$M", "E + NCI + debt + EIP − cash"),
        ("NOPAT FY2025", nopat_fy25, "#,##0", "$M", "EBIT × (1 − 22.7%)"),
        ("ROIC FY2025", roic_fy25, "0.0%", "ratio", "NOPAT / IC"),
        ("Internet monthly ARPU FY2025", ARPU_INET_M, "0.00", "$/sub", "Internet rev / avg Internet / 12"),
        ("Mobile monthly ARPU FY2025", ARPU_MOB_M, "0.00", "$/line", "Mobile service / avg lines / 12"),
        ("UFCF FY2025 (const. debt identity)", ufcf0, "#,##0", "$M", "FCF + interest × (1 − t)"),
        ("WACC used in DCF / prize", WACC, "0.0%", "ratio", "Target-weight WACC"),
    ]
    for item, val, fmt, unit, formula in keys:
        put(ws, r, 1, item, kind="disc")
        put(ws, r, 2, val, kind="calc", fmt=fmt, bold=True)
        put(ws, r, 3, unit, kind="note")
        put(ws, r, 4, "Calculated", kind="calc")
        put(ws, r, 5, formula, kind="note")
        r += 1

    # Store cells we might want — not required; other sheets write values.

    # ---------- 02 Issue tree ----------
    ws = wb.create_sheet("02_IssueTree")
    apply_font(ws)
    widths(ws, {"A": 14, "B": 16, "C": 16, "D": 16, "E": 16, "F": 16, "G": 16, "H": 16, "I": 16, "J": 16, "K": 16, "L": 56})
    put(ws, 1, 1, "1. Issue tree + hypothesis tests — 10-quarter operating series", kind="sec")
    ws.merge_cells("A1:L1")
    put(ws, 2, 1, "Test: is the profit engine still shrinking, and did Q1 2026 break the slope? Any trajectory claim must show this series inflecting — not ARPU or mobile.", kind="note")
    ws.merge_cells("A2:L2")
    header_row(ws, 4, ["Metric"] + QTRS + ["Source"])
    series = [
        ("Internet net adds (000s)", [INET_ADDS[q] for q in QTRS], "trending / Ex99.1, restated"),
        ("Internet EOP (000s)", [INET[q] for q in QTRS], "trending / Ex99.1"),
        ("Mobile EOP (000s)", [MOB[q] for q in QTRS], "trending / Ex99.1"),
        ("Adj. EBITDA ($M)", [EBITDA_Q[q] for q in QTRS], "trending / Ex99.1"),
        ("FCF ($M)", [FCF_Q[q] for q in QTRS], "Charter non-GAAP"),
        ("Upgrade/rebuild ($M)", [UPG_Q[q] for q in QTRS], "NCTA category"),
        ("Rural line extensions ($M)", [RURAL_Q[q] for q in QTRS], "NCTA subsidized rural"),
        ("Total capex ($M)", [CAPEX_Q[q] for q in QTRS], "NCTA total"),
    ]
    for i, (name, data, src) in enumerate(series):
        put(ws, 5 + i, 1, name, kind="disc", bold=True)
        for j, v in enumerate(data):
            later = QTRS[j] == "26Q2"
            put(ws, 5 + i, 2 + j, v, kind="later" if later else "disc", fmt="#,##0")
        put(ws, 5 + i, 12, src, kind="note")

    put(ws, 15, 1, "Hypothesis tests (pass/fail for a recommendation)", kind="sec")
    ws.merge_cells("A15:L15")
    header_row(ws, 16, ["Hypothesis", "Test", "Result", "Implication", "", "", "", "", "", "", "", ""])
    tests = [
        (
            "The engine has inflected",
            "Internet net adds, 10q, zero line",
            "FAIL",
            "Still negative. Q1 26 (−120k) doubled Q1 25 (−59k). Q2 26 −172k (later) is worse. Do not claim inflection from ARPU or mobile.",
        ),
        (
            "Market will net mobile vs broadband",
            "Internet EOP vs mobile EOP; Apr 25 25 vs Apr 24 26 tape",
            "FAIL",
            "Mobile +3.7M lines vs Internet −1.1M customers in-window. Apr 25 25 rallied on mobile; Apr 24 26 did not.",
        ),
        (
            "FCF weakness is only front-loaded capex",
            "FCF vs upgrade/rebuild vs rural",
            "PARTIAL",
            "Upgrade/rebuild up; rural easing. FCF vs Internet adds r = 0.08. Waiting for 2027 is a wait, not the CEO charge.",
        ),
        (
            "This is only a cable-multiple problem",
            "CHTR vs CMCSA Apr 24 2026",
            "PARTIAL",
            "Both sold. CHTR −25.5% vs CMCSA −12.9%. Industry + Charter-specific Internet/belief gap.",
        ),
    ]
    tones = {"FAIL": "fail", "PARTIAL": "warn", "PASS": "pass"}
    for i, (h, t, res, impl) in enumerate(tests):
        put(ws, 17 + i, 1, h, kind="disc")
        ws.merge_cells(start_row=17 + i, start_column=1, end_row=17 + i, end_column=1)
        put(ws, 17 + i, 2, t, kind="note")
        ws.merge_cells(start_row=17 + i, start_column=2, end_row=17 + i, end_column=3)
        put(ws, 17 + i, 4, res, kind=tones[res], bold=True)
        put(ws, 17 + i, 5, impl, kind="note")
        ws.merge_cells(start_row=17 + i, start_column=5, end_row=17 + i, end_column=12)
        ws.row_dimensions[17 + i].height = 36

    # chart data already in rows — add bar chart of net adds
    chart = BarChart()
    chart.type = "col"
    chart.title = "Internet quarterly net adds (000s)"
    chart.y_axis.title = "Net adds (000s)"
    chart.x_axis.title = "Quarter"
    data_ref = Reference(ws, min_col=2, min_row=5, max_col=11, max_row=5)
    cats = Reference(ws, min_col=2, min_row=4, max_col=11)
    # BarChart wants series in columns typically; our series is a row. Plot from a vertical block instead.
    # Write a plot block
    put(ws, 23, 1, "Plot: Internet net adds", kind="sec")
    header_row(ws, 24, ["Quarter", "Internet net adds (000s)"])
    for i, q in enumerate(QTRS):
        put(ws, 25 + i, 1, q, kind="later" if q == "26Q2" else "disc")
        put(ws, 25 + i, 2, INET_ADDS[q], kind="later" if q == "26Q2" else "disc", fmt="#,##0")
    ch = BarChart()
    ch.title = "Internet net adds — zero line test"
    ch.y_axis.title = "000s"
    ch.x_axis.title = "Quarter"
    ch.add_data(Reference(ws, min_col=2, min_row=24, max_row=34), titles_from_data=True)
    ch.set_categories(Reference(ws, min_col=1, min_row=25, max_row=34))
    ch.shape = 4
    ch.y_axis.scaling.min = -200
    ch.y_axis.scaling.max = 50
    ch.height = 8
    ch.width = 18
    ws.add_chart(ch, "D23")

    # ---------- 03 Bridge ----------
    ws = wb.create_sheet("03_InternetBridge")
    apply_font(ws)
    widths(ws, {c: 14 for c in "ABCDEFGHIJKL"})
    ws.column_dimensions["A"].width = 28
    ws.column_dimensions["L"].width = 40
    put(ws, 1, 1, "2. Internet revenue waterfall — volume vs price/mix/allocation", kind="sec")
    ws.merge_cells("A1:L1")
    put(
        ws,
        2,
        1,
        "Identity: Δ Internet revenue = volume (Δ avg customers × prior-year revenue per customer) + price/mix/bundle allocation. Programmer-app costs are video ($218M Q1 26 vs $47M; $251M Q2 vs $67M) and are kept out. 23Q1–Q3 EOP used to form 2024 YoY averages are interpolated back from restated 23Q4 30,590 — labeled on 01_Assumptions notes / 23Q path. FY2025 10-K published split (−$380 / +$785 residential) is the audited analog.",
        kind="note",
    )
    ws.merge_cells("A2:L2")
    ws.row_dimensions[2].height = 48
    header_row(
        ws,
        4,
        [
            "Quarter",
            "Internet rev",
            "YoY Δ rev",
            "Avg customers (000s)",
            "LY avg (000s)",
            "Volume $M",
            "Price/mix $M",
            "Volume share of Δ",
            "Dollars +/−",
            "",
            "",
            "Note",
        ],
    )
    for i, q in enumerate(QTRS):
        b = bridges[q]
        later = q == "26Q2"
        k = "later" if later else "disc"
        put(ws, 5 + i, 1, q, kind=k)
        put(ws, 5 + i, 2, b["rev"], kind=k, fmt="#,##0")
        put(ws, 5 + i, 3, b["d_rev"], kind="calc", fmt="#,##0")
        put(ws, 5 + i, 4, b["avg"], kind="calc", fmt="#,##0.0")
        put(ws, 5 + i, 5, b["avg_ly"], kind="calc", fmt="#,##0.0")
        put(ws, 5 + i, 6, b["volume"], kind="calc", fmt="#,##0.0")
        put(ws, 5 + i, 7, b["price"], kind="calc", fmt="#,##0.0")
        put(ws, 5 + i, 8, b["volume"] / b["d_rev"] if b["d_rev"] else None, kind="calc", fmt="0.0%")
        sign = "NEGATIVE" if b["d_rev"] < 0 else "positive"
        put(ws, 5 + i, 9, sign, kind="fail" if b["d_rev"] < 0 else "pass")
        note = ""
        if q == "26Q1":
            note = "First quarter Internet *dollars* turn negative. Mix ~$0."
        if q == "26Q2":
            note = "Later fact: mix also negative."
        put(ws, 5 + i, 12, note, kind="note")

    put(ws, 16, 1, "FY2025 10-K published (residential Internet)", kind="disc", bold=True)
    put(ws, 16, 2, VOL_INTL_25, kind="disc", fmt="#,##0")
    put(ws, 16, 3, "volume $M", kind="note")
    put(ws, 16, 4, MIX_INTL_25, kind="disc", fmt="#,##0")
    put(ws, 16, 5, "rate/mix $M", kind="note")
    put(ws, 16, 6, VOL_INTL_25 + MIX_INTL_25, kind="calc", fmt="#,##0")
    put(ws, 16, 7, "net +$405 vs FY2024 Internet +$405 (23,765−23,360)", kind="note")

    put(ws, 18, 1, "Pass/fail", kind="fail", bold=True)
    put(
        ws,
        18,
        2,
        "Through 2025, price/mix more than offset volume. Q1 2026 is when Internet dollars turned negative (mix +~$8M, total −~$78M YoY). Q2 mix is also negative. The engine is shrinking in dollars, not just in subscribers.",
        kind="fail",
    )
    ws.merge_cells("B18:L18")
    ws.row_dimensions[18].height = 36

    header_row(ws, 20, ["Quarter", "Volume $M", "Price/mix $M"])
    for i, q in enumerate(QTRS):
        put(ws, 21 + i, 1, q, kind="later" if q == "26Q2" else "disc")
        put(ws, 21 + i, 2, bridges[q]["volume"], kind="calc", fmt="#,##0.0")
        put(ws, 21 + i, 3, bridges[q]["price"], kind="calc", fmt="#,##0.0")
    ch = BarChart()
    ch.type = "col"
    ch.grouping = "clustered"
    ch.title = "Internet YoY: volume vs price/mix ($M)"
    ch.y_axis.title = "$M"
    ch.add_data(Reference(ws, min_col=2, min_row=20, max_col=3, max_row=30), titles_from_data=True)
    ch.set_categories(Reference(ws, min_col=1, min_row=21, max_row=30))
    ch.height = 8
    ch.width = 18
    ws.add_chart(ch, "E20")

    # ---------- 04 Comps + event ----------
    ws = wb.create_sheet("04_CompsEvent")
    apply_font(ws)
    widths(ws, {"A": 36, "B": 18, "C": 18, "D": 18, "E": 18, "F": 18, "G": 56})
    put(ws, 1, 1, "3. Trading comps + earnings-day event study", kind="sec")
    ws.merge_cells("A1:G1")
    put(
        ws,
        2,
        1,
        "Question: Charter-specific belief problem or cable-multiple problem? If peers de-rate too, industry structure. If Charter de-rates more, Internet trajectory + capital allocation. Event study is the correlation the brief asks for — operating r on 10 quarters will not substitute.",
        kind="note",
    )
    ws.merge_cells("A2:G2")
    ws.row_dimensions[2].height = 36

    section(ws, 4, 1, "A. Constructed snapshot — 23 Apr vs 24 Apr 2026 (assignment trigger)", 7)
    header_row(ws, 5, ["Metric", "CHTR 23 Apr", "CHTR 24 Apr", "CMCSA 23 Apr", "CMCSA 24 Apr", "Gap (CHTR−CMCSA, 24 Apr)", "Note"])
    cmcsa_mkt_23 = CMCSA_PX_APR23 * CMCSA_SHARES_M
    cmcsa_mkt_24 = CMCSA_PX_APR24 * CMCSA_SHARES_M
    chtr_fcf_y_23 = FCF_LTM_Q1 / MKT_APR23
    chtr_fcf_y_24 = FCF_LTM_Q1 / MKT_APR24
    # CMCSA FCF yield uses Q1 FCF * 4 as a crude run-rate — LABEL as annualized, not FY
    cmcsa_fcf_ann = CMCSA_FCF_Q1 * 4
    cmcsa_fy_23 = cmcsa_fcf_ann / cmcsa_mkt_23
    cmcsa_fy_24 = cmcsa_fcf_ann / cmcsa_mkt_24
    chtr_ev_ebitda_23 = EV_APR23 / EBITDA_LTM_Q1
    chtr_ev_ebitda_24 = EV_APR24 / EBITDA_LTM_Q1
    rows = [
        ("Share price ($)", PX_APR23, PX_APR24, CMCSA_PX_APR23, CMCSA_PX_APR24, None, "Yahoo close-to-close"),
        ("1-day %", None, (PX_APR24 / PX_APR23) - 1, None, CMCSA_RET_APR24, (PX_APR24 / PX_APR23) - 1 - CMCSA_RET_APR24, "CHTR extra −12.6 pts vs CMCSA"),
        ("Shares (m)", SHARES_Q1 / 1e6, SHARES_Q1 / 1e6, CMCSA_SHARES_M, CMCSA_SHARES_M, None, "CHTR Class A 31 Mar; CMCSA A+B 15 Apr"),
        ("Market cap ($M)", MKT_APR23, MKT_APR24, cmcsa_mkt_23, cmcsa_mkt_24, None, "Price × shares"),
        ("Net debt + NCI ($M)", NET_DEBT_CO_Q1 + NCI_Q1, NET_DEBT_CO_Q1 + NCI_Q1, None, None, None, "CMCSA net debt not reconstructed here"),
        ("Enterprise value ($M)", EV_APR23, EV_APR24, None, None, None, "CHTR only — company net debt + book NCI"),
        ("LTM EBITDA ($M)", EBITDA_LTM_Q1, EBITDA_LTM_Q1, None, None, None, "CHTR constructed; CMCSA Q1 print $7,929 not LTM"),
        ("EV / LTM EBITDA", chtr_ev_ebitda_23, chtr_ev_ebitda_24, None, None, None, "Constructed. Published: Devyara CHTR 6.06x / CMCSA 5.65x ~Apr 26"),
        ("FCF used ($M)", FCF_LTM_Q1, FCF_LTM_Q1, CMCSA_FCF_Q1, CMCSA_FCF_Q1, None, "CHTR LTM Q1; CMCSA Q1 only"),
        ("FCF yield (equity)", chtr_fcf_y_23, chtr_fcf_y_24, cmcsa_fy_23, cmcsa_fy_24, chtr_fcf_y_24 - cmcsa_fy_24, "CMCSA yield uses Q1×4 annualized — labeled crude"),
    ]
    fmts = ["0.00", "0.0%", "0.0", "#,##0.0", "#,##0", "#,##0.0", "#,##0", "0.00x", "#,##0", "0.0%"]
    for i, (row, fmt) in enumerate(zip(rows, fmts)):
        put(ws, 6 + i, 1, row[0], kind="disc", bold=True)
        for j, v in enumerate(row[1:6], 2):
            put(ws, 6 + i, j, v, kind="calc" if v is not None else "note", fmt=fmt if v is not None else None)
        put(ws, 6 + i, 7, row[6], kind="note")

    section(ws, 18, 1, "B. Published multiples (third-party — do not mix with constructed EV)", 7)
    header_row(ws, 19, ["Source / date", "CHTR", "CMCSA", "Read", "", "", ""])
    pubs = [
        ("Devyara ~26 Apr 2026 EV/EBITDA", "6.06x", "5.65x", "Same neighborhood — not a 2-turn Charter-only EBITDA discount"),
        ("TIKR Apr 2026 forward EV/EBITDA", "—", "5.47x", "CMCSA after its Q1 print"),
        ("ValueSense CHTR LTM EV/EBITDA", "5.8x YE25 → 5.6x Q2 26", "—", "Multiple compressed as the Internet print worsened"),
        ("FY2025 FCF (disclosed / compiled)", "$5.0B Charter non-GAAP", "CMCSA FY not taken as a filing line here", "Both cash-generative; yield is the sector, not a gift"),
    ]
    for i, row in enumerate(pubs):
        for j, v in enumerate(row, 1):
            put(ws, 20 + i, j, v, kind="disc" if j < 4 else "note")
        ws.merge_cells(start_row=20 + i, start_column=4, end_row=20 + i, end_column=7)

    section(ws, 26, 1, "C. Earnings-day close-to-close vs Internet print (the brief's correlation)", 7)
    header_row(ws, 27, ["Print", "Internet adds (000s)", "vs year-ago (k)", "Prior close", "Close", "1-day %", "What the tape did"])
    for i, (name, adds, yoy, px0, px1, ret, note) in enumerate(EARN):
        later = "Jul 24 2026" in name
        k = "later" if later else "disc"
        tone = "fail" if ret < -10 else ("pass" if ret > 5 else "warn")
        put(ws, 28 + i, 1, name, kind=k)
        put(ws, 28 + i, 2, adds, kind=k, fmt="#,##0")
        put(ws, 28 + i, 3, yoy, kind="calc" if yoy is not None else "note", fmt="#,##0")
        put(ws, 28 + i, 4, px0, kind=k, fmt="0.00")
        put(ws, 28 + i, 5, px1, kind=k, fmt="0.00")
        put(ws, 28 + i, 6, ret / 100.0, kind=tone, fmt="0.0%")
        put(ws, 28 + i, 7, note, kind="note")

    # plot block
    header_row(ws, 37, ["Print short", "Internet adds (000s)", "1-day %"])
    shorts = ["Q4'24", "Q1'25", "Q2'25", "Q3'25", "Q4'25", "Q1'26", "Q2'26"]
    for i, ((_, adds, _, _, _, ret, _), s) in enumerate(zip(EARN, shorts)):
        put(ws, 38 + i, 1, s, kind="disc")
        put(ws, 38 + i, 2, adds, kind="disc", fmt="#,##0")
        put(ws, 38 + i, 3, ret / 100.0, kind="calc", fmt="0.0%")
    ch = BarChart()
    ch.title = "Earnings-day return"
    ch.y_axis.title = "Close-to-close"
    ch.add_data(Reference(ws, min_col=3, min_row=37, max_row=44), titles_from_data=True)
    ch.set_categories(Reference(ws, min_col=1, min_row=38, max_row=44))
    ch.height = 8
    ch.width = 15
    ws.add_chart(ch, "A46")

    sc = ScatterChart()
    sc.title = "Internet adds vs earnings-day return"
    sc.x_axis.title = "Internet net adds (000s)"
    sc.y_axis.title = "1-day %"
    xvalues = Reference(ws, min_col=2, min_row=38, max_row=44)
    yvalues = Reference(ws, min_col=3, min_row=37, max_row=44)
    s = Series(yvalues, xvalues, title="Earnings days")
    sc.series.append(s)
    sc.height = 8
    sc.width = 12
    ws.add_chart(sc, "E46")

    put(ws, 62, 1, "Pass/fail", kind="fail", bold=True)
    put(
        ws,
        62,
        2,
        "Not a straight line through absolute −120k. Q4 2025 (−119k, better vs −177k) +7.6%; Q1 2026 (−120k, double −59k) −25.5%. CMCSA −12.9% the same day = industry; the extra ~13 pts is Charter-specific. High FCF yield is skepticism, not a buy signal. Buybacks (sheet 10) did not support the price.",
        kind="fail",
    )
    ws.merge_cells("B62:G62")
    ws.row_dimensions[62].height = 48

    # ---------- 05 Reverse DCF ----------
    ws = wb.create_sheet("05_ReverseDCF")
    apply_font(ws)
    widths(ws, {"A": 44, "B": 16, "C": 16, "D": 16, "E": 16, "F": 64})
    put(ws, 1, 1, "4. Reverse DCF — what Internet / FCF path is the stock pricing?", kind="sec")
    ws.merge_cells("A1:F1")
    put(
        ws,
        2,
        1,
        "McKinsey move for an 'undervalued / trajectory' case (Koller et al.; McKinsey on Finance). Hold ke and terminal g; solve for the FCF growth that equates to the Apr 23 vs Apr 24 equity value. This is not a full 10-year operating DCF of Charter — it is the implied-expectations test O'Donnell's undervalued comment needs.",
        kind="note",
    )
    ws.merge_cells("A2:F2")
    ws.row_dimensions[2].height = 42

    section(ws, 4, 1, "A. Setup (equity-side; levered FCF)", 6)
    header_row(ws, 5, ["Item", "Value", "", "", "", "Note"])
    setup = [
        ("FCF LTM Q1 2026 ($M)", FCF_LTM_Q1, "Ex99.1 LTM column — the cash the owners actually received"),
        ("Cost of equity (base)", KE, "Rf 4.3% + 1.05 × 5.0% = 9.55% — labeled"),
        ("Cost of equity (high / trajectory risk)", KE_HI, "12% — if the crash added an uncertainty premium"),
        ("Terminal g after year 5", G_TERM, "0% — mature last-mile. GDP growth would overstate cable"),
        ("Stage length (years)", STAGE_YEARS, "5-year explicit then Gordon"),
        ("Equity value 23 Apr 2026 ($M)", MKT_APR23, "Last close the market was willing to pay before the print"),
        ("Equity value 24 Apr 2026 ($M)", MKT_APR24, "After −120k Internet, double the year-ago loss"),
        ("FCF yield 23 Apr", chtr_fcf_y_23, "16.2% — already a distressed cash yield before the print"),
        ("FCF yield 24 Apr", chtr_fcf_y_24, "21.7%"),
    ]
    for i, (n, v, note) in enumerate(setup):
        put(ws, 6 + i, 1, n, kind="disc")
        fmt = "0.0%" if isinstance(v, float) and abs(v) < 2 else ("0" if isinstance(v, int) and v < 20 else "#,##0.0")
        if n.startswith("Stage"):
            fmt = "0"
        if "Cost of equity" in n or "yield" in n or "Terminal" in n:
            fmt = "0.0%"
        put(ws, 6 + i, 2, v, kind="calc" if "yield" in n or "Equity value" in n or "Cost" in n else "disc", fmt=fmt)
        put(ws, 6 + i, 6, note, kind="note")

    section(ws, 17, 1, "B. Gordon implied perpetual FCF growth  g = (P·ke − FCF) / (P + FCF)", 6)
    header_row(ws, 18, ["ke used", "Implied g at 23 Apr ($242)", "Implied g at 24 Apr ($180)", "Change in implied g", "", "Read"])
    put(ws, 19, 1, "9.55% (CAPM)", kind="calc")
    put(ws, 19, 2, g_gord_23, kind="calc", fmt="0.0%")
    put(ws, 19, 3, g_gord_24, kind="fail", fmt="0.0%", bold=True)
    put(ws, 19, 4, g_gord_24 - g_gord_23, kind="fail", fmt="0.0%")
    put(ws, 19, 6, "Even before the print the stock priced perpetual FCF decline. After the print it priced a steeper one.", kind="note")
    put(ws, 20, 1, "12% (trajectory ke)", kind="assump")
    put(ws, 20, 2, g_gord_23_hi, kind="calc", fmt="0.0%")
    put(ws, 20, 3, g_gord_24_hi, kind="fail", fmt="0.0%")
    put(ws, 20, 4, g_gord_24_hi - g_gord_23_hi, kind="fail", fmt="0.0%")
    put(ws, 20, 6, "A higher hurdle rate still implies negative g after Apr 24. Cheap is not the same as inflecting.", kind="note")

    section(ws, 22, 1, "C. Two-stage: 5-year FCF CAGR, then g_term = 0%", 6)
    header_row(ws, 23, ["ke used", "5-yr CAGR priced at $242", "5-yr CAGR priced at $180", "Delta", "", "Read"])
    put(ws, 24, 1, "9.55% (CAPM)", kind="calc")
    put(ws, 24, 2, g5_23, kind="calc", fmt="0.0%")
    put(ws, 24, 3, g5_24, kind="fail", fmt="0.0%", bold=True)
    put(ws, 24, 4, g5_24 - g5_23, kind="fail", fmt="0.0%")
    put(ws, 24, 6, "If terminal is flat, the 5-year path has to do all the work. $180 prices a deep contraction.", kind="note")

    section(ws, 26, 1, "D. Sensitivity — equity value ($M) vs 5-year FCF CAGR at ke = 9.55%, g_term = 0%", 6)
    header_row(ws, 27, ["5-yr FCF CAGR"] + [f"{x:.0%}" for x in [-0.20, -0.12, -0.08, -0.04, 0.00, 0.04, 0.08]])
    put(ws, 28, 1, "Model equity value ($M)", kind="calc", bold=True)
    cagrs = [-0.20, -0.12, -0.08, -0.04, 0.00, 0.04, 0.08]
    for j, g in enumerate(cagrs, 2):
        put(ws, 28, j, levered_pv(FCF_LTM_Q1, g, KE, G_TERM, 5), kind="calc", fmt="#,##0")
    put(ws, 29, 1, "vs 23 Apr mkt cap", kind="calc")
    for j, g in enumerate(cagrs, 2):
        put(ws, 29, j, levered_pv(FCF_LTM_Q1, g, KE, G_TERM, 5) - MKT_APR23, kind="calc", fmt="#,##0")
    put(ws, 30, 1, "vs 24 Apr mkt cap", kind="calc")
    for j, g in enumerate(cagrs, 2):
        put(ws, 30, j, levered_pv(FCF_LTM_Q1, g, KE, G_TERM, 5) - MKT_APR24, kind="calc", fmt="#,##0")

    put(ws, 32, 1, "Pass/fail", kind="warn", bold=True)
    put(
        ws,
        32,
        2,
        "$242 priced a shallow-to-negative cash path (already skeptical). $180 priced a structural decline. That is the difference between 'cable is unloved' and 'the Internet engine is dying.' A recommendation has to change the Internet run-rate that produces this FCF path — or explain why the multiple should look through it, which it has not. O'Donnell: Winfrey can be right that $180 is cheap on cash and still need a strategic fix.",
        kind="warn",
    )
    ws.merge_cells("B32:F32")
    ws.row_dimensions[32].height = 56

    # ---------- 06 ROIC ----------
    ws = wb.create_sheet("06_ROIC_EP")
    apply_font(ws)
    widths(ws, {"A": 48, "B": 16, "C": 16, "D": 16, "E": 64})
    put(ws, 1, 1, "5. ROIC vs WACC / economic profit — and a crude product SOP", kind="sec")
    ws.merge_cells("A1:E1")
    put(
        ws,
        2,
        1,
        "McKinsey: growth creates value only if ROIC > WACC. Charter reports one segment, so product ROIC is allocated — every split below is labeled. The point is direction: Internet carries the capital (franchise + plant); mobile is asset-light and low-dollar economic profit even when ROIC looks fine.",
        kind="note",
    )
    ws.merge_cells("A2:E2")
    ws.row_dimensions[2].height = 42

    section(ws, 4, 1, "A. Firm-level ROIC (book invested capital)", 5)
    header_row(ws, 5, ["Item", "FY2025 / YE", "Q1 2026", "", "Note"])
    firm_rows = [
        ("Income from operations (EBIT)", EBIT_FY25, EBIT_Q1, "10-K / Ex99.1"),
        ("NOPAT = EBIT × (1 − 22.7%)", nopat_fy25, EBIT_Q1 * (1 - TAX_RATE_ETR), "Cash tax $893M FY25 is lower (OBBBA); we use ETR for economic profit"),
        ("Book invested capital", ic_ye25, ic_q1, "E + NCI + all interest-bearing debt − cash"),
        ("ROIC", roic_fy25, (EBIT_Q1 * 4 * (1 - TAX_RATE_ETR)) / ic_q1, "Q1 annualized is crude — do not over-read"),
        ("WACC (target)", WACC, WACC, "Sheet 01"),
        ("ROIC − WACC spread", roic_fy25 - WACC, None, "Positive on book IC — the firm still earns its cost of capital on yesterday's assets"),
        ("Economic profit (ROIC−WACC)×IC", ep_fy25, None, "$M. Value is being created on the installed base; the multiple is about the future base"),
    ]
    for i, (n, a, b, note) in enumerate(firm_rows):
        put(ws, 6 + i, 1, n, kind="disc")
        fmt = "0.0%" if "ROIC" in n or "spread" in n or "WACC" in n else "#,##0.0"
        put(ws, 6 + i, 2, a, kind="calc", fmt=fmt, bold=("Economic" in n or n == "ROIC"))
        put(ws, 6 + i, 3, b, kind="calc" if b is not None else "note", fmt=fmt if b is not None else None)
        put(ws, 6 + i, 5, note, kind="note")

    put(
        ws,
        14,
        1,
        "Limitation: book IC is dominated by $67.5B franchises + $29.7B goodwill. Franchise fair value exceeded book by >10% at 31 Oct 2025 (10-K). Using book IC understates capital and overstates ROIC vs a market IC. Using EV as IC (Apr 24 EV $128B) gives ROIC ≈ NOPAT/EV = {:.1%} vs WACC {:.1%} — spread near zero / negative. That is the market's view: the installed base is fully priced; growth is not.".format(nopat_fy25 / EV_APR24, WACC),
        kind="warn",
    )
    ws.merge_cells("A14:E14")
    ws.row_dimensions[14].height = 56

    section(ws, 16, 1, "B. Crude product EBITDA (single-segment reporter — allocations are assumptions)", 5)
    header_row(ws, 17, ["Product", "Revenue $M", "Allocated EBITDA $M", "EBITDA margin", "Allocation rule"])
    products = [
        ("Internet", REV_INTL_25, inet_ebitda, "Residual COR 50% + field 70% + care 55% + mkt 40% + other 40%"),
        ("Mobile service + devices @ 0% margin", REV_MOB_25 + DEV_REV_FY25, mob_ebitda, "Wholesale 60% of service; field 5% / care 15% / mkt 20% / other 8%"),
        ("Video (stub)", REV_VID_25, vid_ebitda, "100% programming; residual COR 40%; 15% of shared opex"),
        ("Firm Adj. EBITDA (disclosed check)", REV_FY25, EBITDA_FY25, "Do not expect A+B+C to equal this — leftover voice/SMB/ads/other"),
    ]
    for i, (n, rev, ebitda, rule) in enumerate(products):
        k = "disc" if i == 3 else "calc"
        put(ws, 18 + i, 1, n, kind="disc")
        put(ws, 18 + i, 2, rev, kind="disc", fmt="#,##0")
        put(ws, 18 + i, 3, ebitda, kind=k, fmt="#,##0")
        put(ws, 18 + i, 4, ebitda / rev if rev else None, kind="calc", fmt="0.0%")
        put(ws, 18 + i, 5, rule, kind="note")

    put(ws, 23, 1, "Internet allocated EBITDA / firm EBITDA", kind="calc")
    put(ws, 23, 2, inet_ebitda / EBITDA_FY25, kind="calc", fmt="0.0%", bold=True)
    put(ws, 23, 5, "Directionally: Internet is most of economic profit. Mobile is real but small in dollars.", kind="note")
    put(ws, 24, 1, "Mobile allocated EBITDA / firm EBITDA", kind="calc")
    put(ws, 24, 2, mob_ebitda / EBITDA_FY25, kind="calc", fmt="0.0%", bold=True)
    put(ws, 24, 5, "368k mobile lines cannot replace 120k Internet customers in enterprise value.", kind="note")

    put(ws, 26, 1, "Pass/fail", kind="fail", bold=True)
    put(
        ws,
        26,
        2,
        "Firm book ROIC still clears a 3.5×-structure WACC — Charter is not earning-destroying on the installed base. The market is using something closer to EV as capital and a fading Internet volume, which zeroes the spread. Mobile can show a passable ROIC on thin capital and still fail as the valuation fix because economic profit $ is small. Do not sell a connectivity-customer story.",
        kind="fail",
    )
    ws.merge_cells("B26:E26")
    ws.row_dimensions[26].height = 56

    # ---------- 07 Unit economics ----------
    ws = wb.create_sheet("07_UnitEconomics")
    apply_font(ws)
    widths(ws, {"A": 48, "B": 18, "C": 18, "D": 64})
    put(ws, 1, 1, "6. Unit economics — NPV of an Internet customer vs a mobile line", kind="sec")
    ws.merge_cells("A1:D1")
    put(
        ws,
        2,
        1,
        "Bain customer economics / McKinsey unit NPV. Churn, wholesale, and marketing splits are labeled assumptions (01_Assumptions). Identity: NPV = annual contribution / (r + annual churn) − SAC. This is why the tape will not net 368k mobile against 120k Internet.",
        kind="note",
    )
    ws.merge_cells("A2:D2")
    ws.row_dimensions[2].height = 42

    header_row(ws, 4, ["Item", "Internet", "Mobile", "Note"])
    unit_rows = [
        ("Average units FY2025 (000s)", avg_inet_25, avg_mob_25, "Avg of YE24 and YE25 EOP"),
        ("Reported revenue FY2025 ($M)", REV_INTL_25, REV_MOB_25, "Mobile = service only; devices in Other"),
        ("Monthly ARPU ($)", ARPU_INET_M, ARPU_MOB_M, "Rev / avg units / 12"),
        ("Q1 2026 monthly ARPU ($)", ARPU_INET_Q1, ARPU_MOB_Q1, "Cross-check; Internet slightly down"),
        ("Direct / wholesale take", inet_ocor / REV_INTL_25, MOB_WHOLESALE, "Internet = residual COR share; mobile = 60% assumption"),
        ("Annual contribution ($ / unit)", inet_contrib_y, mob_contrib_y, "After direct/wholesale and (Internet) half field"),
        ("Monthly churn (assumption)", INET_CHURN_M, MOB_CHURN_M, "Not disclosed"),
        ("Annual churn", inet_churn_y, mob_churn_y, "1 − (1 − m)^12"),
        ("Implied expected life (years)", 1 / inet_churn_y, 1 / mob_churn_y, "1 / annual churn"),
        ("Gross adds FY2025 (000s)", inet_gross, mob_gross, "Net change + churn × avg"),
        ("Marketing SAC ($ / gross add)", inet_cac, mob_cac, "Allocated marketing / gross adds"),
        ("CPE / install ($ / gross add)", inet_cpe, 0, "70% of CPE to Internet; mobile SIM-ish"),
        ("Total SAC ($)", inet_sac, mob_cac, ""),
        ("Discount rate r", DISC_R, DISC_R, "Labeled 8%"),
        ("NPV per unit ($)", inet_npv, mob_npv, "contrib/(r+churn) − SAC"),
    ]
    for i, (n, a, b, note) in enumerate(unit_rows):
        put(ws, 5 + i, 1, n, kind="disc")
        pct = "churn" in n.lower() or "take" in n.lower() or n.startswith("Discount")
        fmt = "0.0%" if pct else ("0.00" if "ARPU" in n or "Monthly" in n else ("#,##0.0" if "Average" in n or "Gross" in n or "Revenue" in n else "#,##0"))
        if "NPV" in n or "contribution" in n or "SAC" in n or "CPE" in n or "life" in n:
            fmt = "#,##0.00" if "life" in n else "#,##0"
        put(ws, 5 + i, 2, a, kind="calc", fmt=fmt, bold=("NPV" in n))
        put(ws, 5 + i, 3, b, kind="calc", fmt=fmt, bold=("NPV" in n))
        put(ws, 5 + i, 4, note, kind="note")

    put(ws, 21, 1, "Ratio: Internet NPV / mobile NPV", kind="calc", bold=True)
    put(ws, 21, 2, inet_npv / mob_npv if mob_npv else None, kind="calc", fmt="0.0x", bold=True)
    put(ws, 21, 4, "One Internet customer is worth several mobile lines even before shared network capital.", kind="note")

    put(ws, 23, 1, "Q1 2026 print in NPV $", kind="sec")
    ws.merge_cells("A23:D23")
    header_row(ws, 24, ["Flow", "Units (000s)", "× NPV $", "Value created / destroyed ($M)"])
    put(ws, 25, 1, "Internet net adds Q1 2026", kind="disc")
    put(ws, 25, 2, -120, kind="disc")
    put(ws, 25, 3, inet_npv, kind="calc", fmt="#,##0")
    put(ws, 25, 4, -120 * inet_npv / 1000, kind="fail", fmt="#,##0.0", bold=True)
    put(ws, 26, 1, "Mobile net adds Q1 2026", kind="disc")
    put(ws, 26, 2, 368, kind="disc")
    put(ws, 26, 3, mob_npv, kind="calc", fmt="#,##0")
    put(ws, 26, 4, 368 * mob_npv / 1000, kind="calc", fmt="#,##0.0")
    put(ws, 27, 1, "Net value of the quarter's adds", kind="calc", bold=True)
    put(ws, 27, 4, (-120 * inet_npv + 368 * mob_npv) / 1000, kind="fail", fmt="#,##0.0", bold=True)
    put(ws, 27, 3, "Internet loss exceeds mobile gain in NPV $", kind="note")

    # sensitivity
    section(ws, 29, 1, "Sensitivity — mobile NPV $ if wholesale % or CAC changes (Internet NPV held)", 4)
    header_row(ws, 30, ["Mobile wholesale \\ CAC $", "100", "250", "400", "550"])
    for i, wh in enumerate([0.50, 0.60, 0.70]):
        put(ws, 31 + i, 1, wh, kind="assump", fmt="0%")
        for j, cac in enumerate([100, 250, 400, 550], 2):
            contrib = mob_rev_per * (1 - wh)
            npv = contrib / (DISC_R + mob_churn_y) - cac
            put(ws, 31 + i, j, npv, kind="calc", fmt="#,##0")

    put(ws, 35, 1, "Pass/fail", kind="fail", bold=True)
    put(
        ws,
        35,
        2,
        "Do not sell total connectivity customers as the fix. Under these labeled assumptions, Q1's −120k Internet destroys more value than +368k mobile creates. If wholesale is 70% and mobile CAC is $400+, mobile NPV is near zero or negative. Recalibrate the blue inputs; the direction survives a wide range.",
        kind="fail",
    )
    ws.merge_cells("B35:D35")
    ws.row_dimensions[35].height = 48

    # ---------- 08 Full potential ----------
    ws = wb.create_sheet("08_FullPotential")
    apply_font(ws)
    widths(ws, {"A": 36, "B": 14, "C": 14, "D": 14, "E": 14, "F": 14, "G": 14, "H": 14, "I": 14, "J": 48})
    put(ws, 1, 1, "7. Full potential vs current trajectory (Bain) — 8-year UFCF", kind="sec")
    ws.merge_cells("A1:J1")
    put(
        ws,
        2,
        1,
        "Bain Full Potential / McKinsey granularity of growth. Three Internet paths, same WACC and capex roll-off. UFCF_t = (EBITDA_t − D&A) × (1−t) + D&A − capex_t, with D&A held at FY2025. EBITDA_t = FY2025 + volume (Δ avg Internet × contribution $/sub) + scenario mix/other. This is a size-the-prize model, not a fairness opinion.",
        kind="note",
    )
    ws.merge_cells("A2:J2")
    ws.row_dimensions[2].height = 48

    header_row(ws, 4, ["Year"] + [str(y) for y in years] + ["Note"])
    # Internet EOP
    put(ws, 5, 1, "Internet EOP (000s) — Base", kind="disc")
    put(ws, 6, 1, "Internet EOP (000s) — Full potential", kind="disc")
    put(ws, 7, 1, "Internet EOP (000s) — Bear", kind="disc")
    put(ws, 8, 1, "Capex ($M)", kind="assump")
    put(ws, 9, 1, "EBITDA Base ($M)", kind="calc")
    put(ws, 10, 1, "EBITDA Full ($M)", kind="calc")
    put(ws, 11, 1, "EBITDA Bear ($M)", kind="calc")
    put(ws, 12, 1, "UFCF Base ($M)", kind="calc")
    put(ws, 13, 1, "UFCF Full ($M)", kind="calc")
    put(ws, 14, 1, "UFCF Bear ($M)", kind="calc")
    for i, y in enumerate(years, 2):
        put(ws, 5, i, inet_path("base", y), kind="calc", fmt="#,##0")
        put(ws, 6, i, inet_path("full", y), kind="calc", fmt="#,##0")
        put(ws, 7, i, inet_path("bear", y), kind="fail", fmt="#,##0")
        put(ws, 8, i, capex_path(y), kind="assump", fmt="#,##0")
        put(ws, 9, i, ebitda_path("base", y), kind="calc", fmt="#,##0")
        put(ws, 10, i, ebitda_path("full", y), kind="calc", fmt="#,##0")
        put(ws, 11, i, ebitda_path("bear", y), kind="calc", fmt="#,##0")
        put(ws, 12, i, ufcf_path("base", y), kind="calc", fmt="#,##0")
        put(ws, 13, i, ufcf_path("full", y), kind="calc", fmt="#,##0")
        put(ws, 14, i, ufcf_path("bear", y), kind="calc", fmt="#,##0")
    put(ws, 5, 10, "−480k/yr through 2028, then −320k", kind="note")
    put(ws, 6, 10, "−360 / −180 / 0 then flat — Internet to zero by YE2028", kind="note")
    put(ws, 7, 10, "−600k/yr through 2028 (near Q2 run-rate annualized)", kind="note")
    put(ws, 8, 10, "2026 guide $11.4B; 2027–28 labeled roll-off", kind="note")

    section(ws, 16, 1, "Valuation of each path (WACC target-structure, g_term = 0%)", 10)
    header_row(ws, 17, ["", "Base (current)", "Full potential", "Bear", "Full − Base (prize)", "", "", "", "", "Note"])
    val_rows = [
        ("PV of 2026–33 UFCF + terminal ($M)", ev_base, ev_full, ev_bear, ev_full - ev_base),
        ("− Company net debt Q1", NET_DEBT_CO_Q1, NET_DEBT_CO_Q1, NET_DEBT_CO_Q1, 0),
        ("− Book NCI Q1", NCI_Q1, NCI_Q1, NCI_Q1, 0),
        ("Equity value ($M)", eq_base, eq_full, eq_bear, prize),
        ("vs 24 Apr market cap ($M)", eq_base - MKT_APR24, eq_full - MKT_APR24, eq_bear - MKT_APR24, prize),
        ("Implied equity / Apr 24 price", eq_base / MKT_APR24, eq_full / MKT_APR24, eq_bear / MKT_APR24, None),
    ]
    for i, (n, a, b, c, d) in enumerate(val_rows):
        put(ws, 18 + i, 1, n, kind="disc", bold=("Equity value" in n))
        fmt = "0.00x" if "Implied" in n else "#,##0"
        put(ws, 18 + i, 2, a, kind="calc", fmt=fmt)
        put(ws, 18 + i, 3, b, kind="pass", fmt=fmt, bold=("Equity" in n))
        put(ws, 18 + i, 4, c, kind="fail", fmt=fmt)
        put(ws, 18 + i, 5, d, kind="calc" if d is not None else "note", fmt=fmt if d is not None else None)

    ch = LineChart()
    ch.title = "UFCF by scenario ($M)"
    ch.y_axis.title = "$M"
    ch.x_axis.title = "Year"
    # Vertical plot block so series names come from column A
    header_row(ws, 26, ["Year"] + [str(y) for y in years])
    put(ws, 27, 1, "UFCF Base ($M)", kind="calc")
    put(ws, 28, 1, "UFCF Full ($M)", kind="calc")
    put(ws, 29, 1, "UFCF Bear ($M)", kind="calc")
    for i, y in enumerate(years, 2):
        put(ws, 27, i, ufcf_path("base", y), kind="calc", fmt="#,##0")
        put(ws, 28, i, ufcf_path("full", y), kind="calc", fmt="#,##0")
        put(ws, 29, i, ufcf_path("bear", y), kind="calc", fmt="#,##0")
    ch.add_data(Reference(ws, min_col=1, min_row=27, max_col=9, max_row=29), from_rows=True, titles_from_data=True)
    ch.set_categories(Reference(ws, min_col=2, min_row=26, max_col=9))
    ch.height = 8
    ch.width = 18
    ws.add_chart(ch, "A31")

    put(ws, 42, 1, "Pass/fail", kind="warn", bold=True)
    put(
        ws,
        42,
        2,
        f"The prize for getting Internet to zero by 2028 vs staying on a −120k/q run-rate is about ${prize:,.0f}M of equity value in this model (~${prize/1000:,.1f}B). If FCF only inflects after 2027 because capex rolls off, that is already in the Base path — it is a wait, not an out-of-the-box move. The CEO charge is the Full column, not the Base column. Replace blue capex and contribution if the team has a tighter view; the gap is the slide.",
        kind="warn",
    )
    ws.merge_cells("B42:J42")
    ws.row_dimensions[42].height = 56

    # ---------- 09 Initiative NPV ----------
    ws = wb.create_sheet("09_InitiativeNPV")
    apply_font(ws)
    widths(ws, {"A": 42, "B": 18, "C": 18, "D": 18, "E": 64})
    put(ws, 1, 1, "8. Initiative NPV / size the prize — illustrative, not the team's pick", kind="sec")
    ws.merge_cells("A1:E1")
    put(
        ws,
        2,
        1,
        "CEO charge: do X, targeting Y, funded by Z, over N months — and when does it show up in the Internet print (sheet 04: that is what Wall Street looks at). Three archetypes the diagnosis implies. Swap the blue cost/capture cells once the team chooses.",
        kind="note",
    )
    ws.merge_cells("A2:E2")
    ws.row_dimensions[2].height = 42

    header_row(ws, 4, ["", "A. Internet to zero in 24 months", "B. Targeted competitive quality (5y)", "C. Wait for 2027 / pause buybacks", "Note"])
    init_rows = [
        ("What it is", "Retention, price-lock, FWA response, save-desk — change the run-rate", "Capex in the 27% AT&T / 16% Verizon fiber overlap plus worst FWA zips", "Stop buybacks, de-lever, let upgrade/rebuild finish", ""),
        ("Out-of-the-box test", "Only if the offer/operating model is new, not 'message harder'", "Strategic if it is a different network end-state, not the current evolution", "FAILS the CEO charge — this is the wait the issue tree rejected", ""),
        ("Cash cost (undiscounted, $M)", INIT_A_OPEX, INIT_B_CAPEX, 0, "A is opex; B is capex; C saves buybacks rather than spending"),
        ("When Internet print changes", f"Month {INIT_A_MONTHS}", "Year 3–4", "Does not", "Print = quarterly Internet net adds"),
        ("PV of cost @ WACC ($M)", init_a_cost_pv, init_b_cost_pv, 0, "A after-tax; B capex not tax-shielded here (conservative)"),
        ("Share of Full−Base prize", 0.80, INIT_B_CAPTURE, 0.00, "A assumes the run-rate actually sticks"),
        ("PV of benefit ($M)", init_a_benefit, init_b_benefit, 0, "B delayed 3 years"),
        ("NPV ($M)", init_a_npv, init_b_npv, init_c_npv, "C's 'NPV' below is Base equity − $180 mkt cap (already-in-the-price cheapness), not a move"),
        ("NPV vs doing the prize move ($M)", init_a_npv, init_b_npv, init_c_vs_move, "C forgoes the prize"),
    ]
    for i, row in enumerate(init_rows):
        put(ws, 5 + i, 1, row[0], kind="disc", bold=("NPV" in row[0]))
        for j in range(1, 4):
            v = row[j]
            kind = "assump" if i in (2, 5) else "calc"
            if i < 2:
                kind = "note"
                put(ws, 5 + i, j + 1, v, kind="note")
            else:
                fmt = "0.0%" if isinstance(v, float) and abs(v) <= 1 and i == 5 else ("#,##0" if not isinstance(v, str) else None)
                if isinstance(v, str):
                    put(ws, 5 + i, j + 1, v, kind="note")
                else:
                    tone = "pass" if i == 7 and j == 1 else ("fail" if i in (7, 8) and j == 3 else kind)
                    put(ws, 5 + i, j + 1, v, kind=tone, fmt=fmt, bold=(i == 7))
        put(ws, 5 + i, 5, row[4], kind="note")
        ws.row_dimensions[5 + i].height = 32

    put(ws, 16, 1, "How to use this in Week 7", kind="sec")
    ws.merge_cells("A16:E16")
    put(
        ws,
        17,
        1,
        "Replace column A or B with the team's move. Keep three numbers on the slide: cost, month the Internet print changes, NPV vs wait. If the honest print date is after 24 months, say so — sheet 04 says the multiple will not look through it. Funding for A or B is sheet 10 (cut buybacks + leverage room vs Cox cash).",
        kind="note",
    )
    ws.merge_cells("A17:E17")
    ws.row_dimensions[17].height = 48

    put(ws, 19, 1, "Pass/fail", kind="warn", bold=True)
    put(
        ws,
        19,
        2,
        "Waiting (C) can still leave the stock 'cheap' vs Base DCF and still fail the engagement. A beats B on time-to-print if — and only if — the team believes a commercial/operating move can actually zero the losses. That is a judgement call, not a formula. Do not present A as the recommendation until the team owns the $2B and the 80% capture.",
        kind="warn",
    )
    ws.merge_cells("B19:E19")
    ws.row_dimensions[19].height = 48

    # ---------- 10 Funding ----------
    ws = wb.create_sheet("10_FundingBox")
    apply_font(ws)
    widths(ws, {"A": 48, "B": 18, "C": 18, "D": 64})
    put(ws, 1, 1, "9. Capital allocation / funding box", kind="sec")
    ws.merge_cells("A1:D1")
    put(
        ws,
        2,
        1,
        "McKinsey capital productivity: what can you fund without a credit event? Company is not in distress (leverage 4.15× inside 4.0–4.5×). The constraint is Cox cash + the stated 3.5× long-term target + a buyback machine that has not supported the price.",
        kind="note",
    )
    ws.merge_cells("A2:D2")
    ws.row_dimensions[2].height = 36

    section(ws, 4, 1, "A. Capacity", 4)
    header_row(ws, 5, ["Item", "Value", "Unit", "Note"])
    cap_rows = [
        ("LTM EBITDA Q1 2026", EBITDA_LTM_Q1, "$M", "Constructed"),
        ("Company net debt Q1", NET_DEBT_CO_Q1, "$M", "LTD − cash"),
        ("Stated leverage", LEV_Q1, "x", "4.15×"),
        ("Room to 4.5× (pre-close band)", lev_room_up, "$M", "Additional net debt capacity"),
        ("Debt to retire to 3.5×", lev_room_down, "$M", "Long-term target — a use, not a source"),
        ("FY2025 FCF", FCF_FY25, "$M", "Disclosed"),
        ("FCF LTM Q1 2026", FCF_LTM_Q1, "$M", "Disclosed"),
        ("Working 2026 FCF (ex-Cox)", fcf_26_assumed, "$M", "Labeled ≈ LTM; not a guide"),
        ("FY2025 buybacks", BUYBACK_FY25_USD, "$M", "17.1M shares/units — more than FY FCF"),
        ("Q1 2026 buybacks", BUYBACK_Q1_USD, "$M", "4.3M shares"),
        ("Q2 2026 buybacks (later)", BUYBACK_Q2_USD, "$M", "4.0M shares"),
        ("Remaining authority 30 Jun (later)", AUTH_REMAIN_Q2, "$M", "Ex-Liberty — the program is effectively done"),
        ("Cox cash at close (later Q2 figure)", COX_CASH, "$M", "Must fund ~$4.2B"),
        ("Cox net debt assumed (later)", COX_NET_DEBT, "$M", "Pro forma leverage reset"),
        ("Cash + undrawn Q1", CASH_Q1 + 4600, "$M", "Cash $517 + ~$4.6B facilities (10-Q Q1)"),
    ]
    for i, (n, v, u, note) in enumerate(cap_rows):
        later = "later" in n.lower() or "Q2 2026" in n
        put(ws, 6 + i, 1, n, kind="later" if later else "disc")
        fmt = "0.00" if u == "x" else "#,##0"
        put(ws, 6 + i, 2, v, kind="calc" if u == "$M" else "disc", fmt=fmt)
        put(ws, 6 + i, 3, u, kind="note")
        put(ws, 6 + i, 4, note, kind="note")

    section(ws, 23, 1, "B. 2026 uses of cash — three deployments of the same FCF", 4)
    header_row(ws, 24, ["Use ($M)", "Keep buybacks (status quo)", "Fund Initiative A + Cox", "De-lever toward 3.5×"])
    deployments = [
        ("FCF 2026 (working)", fcf_26_assumed, fcf_26_assumed, fcf_26_assumed),
        ("Cox cash", COX_CASH, COX_CASH, COX_CASH),
        ("Buybacks", BUYBACK_FY25_USD, 0, 0),
        ("Initiative A opex", 0, INIT_A_OPEX, 0),
        ("Residual to debt / surplus", fcf_26_assumed - COX_CASH - BUYBACK_FY25_USD, fcf_26_assumed - COX_CASH - INIT_A_OPEX, fcf_26_assumed - COX_CASH),
    ]
    for i, (n, a, b, c) in enumerate(deployments):
        put(ws, 25 + i, 1, n, kind="disc", bold=(i == 4))
        tone_a = "fail" if i == 4 and a < 0 else "calc"
        tone_b = "pass" if i == 4 and b >= 0 else "calc"
        put(ws, 25 + i, 2, a, kind=tone_a, fmt="#,##0")
        put(ws, 25 + i, 3, b, kind=tone_b, fmt="#,##0")
        put(ws, 25 + i, 4, c, kind="calc", fmt="#,##0")

    put(
        ws,
        31,
        1,
        "Status-quo buybacks + Cox cash over-spends working FCF (negative residual). That is how FY2025 already worked ($5.4B buybacks vs $5.0B FCF) — incremental debt. Initiative A is payable if buybacks stop; it is not payable on top of $5B buybacks and Cox. Remaining authority after Q2 is $365M — the repurchase story is ending whether or not the team recommends it.",
        kind="warn",
    )
    ws.merge_cells("A31:D31")
    ws.row_dimensions[31].height = 56

    section(ws, 33, 1, "C. Buyback vs price (why allocation is in the multiple)", 4)
    header_row(ws, 34, ["Earnings date", "CHTR close $", "Buybacks in the quarter just reported ($M)", "Note"])
    bb_overlay = [
        ("Jan 31 2025", 345.49, None, "FY2024 buybacks were small vs later"),
        ("Apr 25 2025", 373.65, None, "Local high — buybacks still 'working' as a story"),
        ("Jul 25 2025", 309.75, None, "Q2 25 Internet miss"),
        ("Oct 31 2025", 233.84, None, ""),
        ("Jan 30 2026", 206.12, 5400, "FY2025 $5.4B — price did not follow"),
        ("Apr 24 2026", 180.13, 963, "Q1 $963M into the crash"),
        ("Jul 24 2026", 123.31, 838, "Later fact; program nearly exhausted"),
    ]
    for i, (d, px, bb, note) in enumerate(bb_overlay):
        put(ws, 35 + i, 1, d, kind="later" if "Jul 24 2026" in d else "disc")
        put(ws, 35 + i, 2, px, kind="disc", fmt="0.00")
        put(ws, 35 + i, 3, bb, kind="disc" if bb else "note", fmt="#,##0" if bb else None)
        put(ws, 35 + i, 4, note, kind="note")

    put(ws, 44, 1, "Pass/fail", kind="fail", bold=True)
    put(
        ws,
        44,
        2,
        "Buybacks converted flat earnings into EPS and did not support the price once Internet YoY doubled. They also consume the cash a trajectory move needs (Cox $4.2B + Initiative A). A recommendation that keeps the $5B repurchase machine and adds a growth spend is not funded. De-lever-and-wait is funded and still fails the CEO charge.",
        kind="fail",
    )
    ws.merge_cells("B44:D44")
    ws.row_dimensions[44].height = 48

    # ---------- 11 Scorecard ----------
    ws = wb.create_sheet("11_Scorecard")
    apply_font(ws)
    widths(ws, {"A": 42, "B": 18, "C": 36, "D": 64})
    put(ws, 1, 1, "Scorecard — nine analyses vs a CEO recommendation", kind="sec")
    ws.merge_cells("A1:D1")
    header_row(ws, 3, ["Analysis", "Status", "Result vs a pitch", "Implication"])
    score = [
        ("1. Issue tree / Internet net adds", "Complete", "FAIL — no inflection", "Cannot claim operating turn from ARPU or mobile"),
        ("2. Internet $ waterfall", "Complete", "FAIL — dollars turned Q1 2026", "Engine shrinking in dollars; keep video app costs out"),
        ("3. Comps + event study", "Complete", "Industry + Charter-specific", "Tape prices YoY acceleration and consensus miss, not FCF"),
        ("4. Reverse DCF", "Complete", "$180 prices structural FCF decline", "Cheap on cash; still need a strategic fix"),
        ("5. ROIC / economic profit", "Complete", "Book ROIC > WACC; market IC does not", "Installed base is fine; future Internet base is the issue"),
        ("6. Unit economics", "Complete", "Internet NPV >> mobile NPV", "Do not sell connectivity-customer math"),
        ("7. Full potential", "Complete", "Prize is the Full−Base equity gap", "2027 capex roll-off is already in Base = wait"),
        ("8. Initiative NPV", "Complete (illustrative)", "Wait fails; A only if run-rate actually changes", "Replace blue cells with the team's move"),
        ("9. Funding box", "Complete", "Buybacks + Cox + a move do not fit", "Cut buybacks to fund a print-changing move, or do not claim the move"),
    ]
    for i, (a, b, c, d) in enumerate(score):
        put(ws, 4 + i, 1, a, kind="disc", bold=True)
        put(ws, 4 + i, 2, b, kind="pass")
        tone = "fail" if "FAIL" in c or "do not" in c.lower() or "does not" in c.lower() or "Wait fails" in c or "do not fit" in c else "warn"
        put(ws, 4 + i, 3, c, kind=tone)
        put(ws, 4 + i, 4, d, kind="note")
        ws.row_dimensions[4 + i].height = 28

    put(ws, 15, 1, "One sentence for the Week 5 pack", kind="sec")
    ws.merge_cells("A15:D15")
    put(
        ws,
        16,
        1,
        "The market is not confused about FCF or mobile; it has repriced a deteriorating Internet volume path. The firm still earns its cost of capital on the installed base. A recommendation that does not change Internet net adds inside ~24 months, and that is not funded after Cox and without relying on exhausted buybacks, will not change the trajectory the CEO asked for.",
        kind="warn",
    )
    ws.merge_cells("A16:D16")
    ws.row_dimensions[16].height = 56

    # Force Georgia on every used cell (including empties Excel would open as Calibri)
    for sheet in wb.worksheets:
        apply_font(sheet)
        sheet.page_setup.paperSize = sheet.PAPERSIZE_TABLOID
        max_r = sheet.max_row or 1
        max_c = sheet.max_column or 1
        for row in sheet.iter_rows(min_row=1, max_row=max_r, min_col=1, max_col=max_c):
            for cell in row:
                f = cell.font
                cell.font = Font(
                    name=GEORGIA,
                    size=f.size or 10,
                    bold=bool(f.bold),
                    italic=bool(f.italic),
                    color=f.color,
                )

    wb.save(OUT)
    print(f"Legacy staging workbook written: {OUT}")
    print("Applying expert review; staging point estimates are not final outputs.")


if __name__ == "__main__":
    main()
    # The original build is intentionally followed by the expert-methodology
    # review, which removes unsupported point estimates and false precision.
    from expert_review_mbb_workbook import main as expert_review

    expert_review()
