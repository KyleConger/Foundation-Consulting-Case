"""Expert-review the Charter MBB workbook and remove false precision.

Loads the prior workbook, preserves the disclosed operating issue tree, and
rebuilds the other analysis sheets with defensible ranges and break-even tests.
"""
from pathlib import Path

from openpyxl import load_workbook
from openpyxl.chart import BarChart, LineChart, Reference, ScatterChart, Series
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

HERE = Path(__file__).resolve().parent
BOOK = HERE / "CHTR-MBB-Financial-Analyses.xlsx"
GEORGIA = "Georgia"

GREEN = "E2EFDA"
BLUE = "DDEBF7"
YELLOW = "FFF2CC"
ORANGE = "FCE4D6"
RED = "F8CBAD"
PURPLE = "E2D5F1"
NAVY = "1F4E79"
MIDBLUE = "2E75B6"
WHITE = "FFFFFF"
GRAY = "595959"
thin = Border(
    left=Side(style="thin", color="B0B0B0"),
    right=Side(style="thin", color="B0B0B0"),
    top=Side(style="thin", color="B0B0B0"),
    bottom=Side(style="thin", color="B0B0B0"),
)


def f(size=10, bold=False, italic=False, color="000000"):
    return Font(name=GEORGIA, size=size, bold=bold, italic=italic, color=color)


def cell(ws, row, col, value, kind="disclosed", fmt=None, bold=False):
    c = ws.cell(row, col, value)
    fills = {
        "disclosed": GREEN,
        "assumption": BLUE,
        "calculated": YELLOW,
        "caution": ORANGE,
        "fail": RED,
        "later": PURPLE,
        "header": NAVY,
        "section": MIDBLUE,
    }
    if kind in fills:
        c.fill = PatternFill("solid", fgColor=fills[kind])
    color = WHITE if kind in ("header", "section") else ("0000FF" if kind == "assumption" else "000000")
    if kind == "note":
        color = GRAY
    c.font = f(11 if kind == "section" else 10, bold or kind in ("header", "section"), kind == "note", color)
    c.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center" if kind == "header" else "left")
    c.border = thin
    if fmt:
        c.number_format = fmt
    return c


def setup(ws, widths):
    ws.sheet_view.showGridLines = False
    ws.freeze_panes = "A4"
    ws.page_setup.orientation = "landscape"
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    for col, width in widths.items():
        ws.column_dimensions[col].width = width


def title(ws, text, end_col):
    cell(ws, 1, 1, text, "section")
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=end_col)
    ws["A1"].font = f(16, True, False, WHITE)
    ws.row_dimensions[1].height = 26


def note(ws, row, text, end_col):
    cell(ws, row, 1, text, "note")
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=end_col)
    ws.row_dimensions[row].height = 42


def headers(ws, row, labels):
    for col, label in enumerate(labels, 1):
        cell(ws, row, col, label, "header")
    ws.row_dimensions[row].height = 28


def section(ws, row, text, end_col):
    cell(ws, row, 1, text, "section")
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=end_col)


def remove_and_create(wb, name, index=None):
    if name in wb.sheetnames:
        wb.remove(wb[name])
    ws = wb.create_sheet(name, index)
    return ws


def levered_value(fcf0, stage_growth, ke, terminal_growth=0.0, years=5):
    pv = sum(fcf0 * (1 + stage_growth) ** t / (1 + ke) ** t for t in range(1, years + 1))
    fcf_n = fcf0 * (1 + stage_growth) ** years
    terminal = fcf_n * (1 + terminal_growth) / (ke - terminal_growth)
    return pv + terminal / (1 + ke) ** years


def solve_stage_growth(target, fcf0, ke, terminal_growth=0.0, years=5):
    lo, hi = -0.60, 0.30
    for _ in range(100):
        mid = (lo + hi) / 2
        if levered_value(fcf0, mid, ke, terminal_growth, years) < target:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def incremental_stabilization_value(contribution, wacc, terminal_growth=0.0):
    """PV of incremental after-tax contribution from retained customers.

    Full-potential path: annual net adds -360k, -180k, then zero.
    Base path: -480k through 2028, -320k thereafter.
    """
    tax = 0.227
    base_adds = [-480, -480, -480, -320, -320, -320, -320, -320]
    full_adds = [-360, -180, 0, 0, 0, 0, 0, 0]
    base_eop = full_eop = 29680
    prior_diff = 0
    pv = 0
    annual = []
    for t, (b, g) in enumerate(zip(base_adds, full_adds), 1):
        base_eop += b
        full_eop += g
        diff = full_eop - base_eop
        avg_diff = (prior_diff + diff) / 2
        after_tax_cf = avg_diff * contribution / 1000 * (1 - tax)
        pv += after_tax_cf / (1 + wacc) ** t
        annual.append((2025 + t, base_eop, full_eop, diff, avg_diff, after_tax_cf))
        prior_diff = diff
    last_cf = annual[-1][-1]
    terminal = last_cf * (1 + terminal_growth) / (wacc - terminal_growth)
    pv += terminal / (1 + wacc) ** len(annual)
    return pv, annual


def initiative_break_even(spend, years_spend, benefit_start, contribution, wacc, tax, capex=False):
    """Required steady-state customer equivalents for NPV=0."""
    annual_spend = spend / years_spend
    pv_cost = sum(
        annual_spend * (1 if capex else 1 - tax) / (1 + wacc) ** t
        for t in range(1, years_spend + 1)
    )
    # Perpetual after-tax benefit starts at benefit_start.
    pv_factor = (1 - tax) / wacc / (1 + wacc) ** (benefit_start - 1)
    required_ebitda = pv_cost / pv_factor
    required_customers = required_ebitda * 1_000_000 / contribution
    return pv_cost, required_ebitda, required_customers


def force_georgia(wb):
    for ws in wb.worksheets:
        for row in ws.iter_rows():
            for c in row:
                old = c.font
                c.font = Font(
                    name=GEORGIA,
                    size=old.size or 10,
                    bold=bool(old.bold),
                    italic=bool(old.italic),
                    color=old.color,
                )


def main():
    wb = load_workbook(BOOK)

    # Core disclosed inputs ($M except shares/prices)
    shares = 122_984_536
    px_pre, px_post = 241.78, 180.13
    market_pre = px_pre * shares / 1e6
    market_post = px_post * shares / 1e6
    fcf_ltm = 4812
    an_ownership = 0.11
    class_a_fcfe_screen = fcf_ltm * (1 - an_ownership)
    ebit_25 = 12908
    tax = 0.227
    nopat = ebit_25 * (1 - tax)
    ic_24 = 15587 + 4120 + 1799 + 92134 + 1072 - 459
    ic_25 = 16054 + 4465 + 750 + 94006 + 1447 - 477
    avg_ic = (ic_24 + ic_25) / 2
    roic = nopat / avg_ic
    fcf_yield_pre = class_a_fcfe_screen / market_pre
    fcf_yield_post = class_a_fcfe_screen / market_post

    # Defensible valuation ranges: do not bless one CAPM output.
    ke_cases = [0.10, 0.12, 0.14]
    implied = [
        (ke, solve_stage_growth(market_pre, class_a_fcfe_screen, ke), solve_stage_growth(market_post, class_a_fcfe_screen, ke))
        for ke in ke_cases
    ]
    wacc_cases = [0.075, 0.085, 0.095]
    contribution_cases = [500, 650, 800]
    stabilization = {
        (c, w): incremental_stabilization_value(c, w)[0]
        for c in contribution_cases
        for w in wacc_cases
    }

    # Rebuild all sheets carrying valuation or assumptions.
    preserve = {"02_IssueTree"}
    for name in list(wb.sheetnames):
        if name not in preserve:
            wb.remove(wb[name])

    # 00 ReadMe
    ws = wb.create_sheet("00_ReadMe", 0)
    setup(ws, {"A": 31, "B": 86, "C": 22, "D": 24})
    title(ws, "Charter — expert-reviewed MBB financial analyses", 4)
    note(
        ws,
        2,
        "Expert review v2. The prior draft was directionally useful but overreached: it treated arbitrary product cost allocations, churn, WACC, and initiative capture assumptions as precise conclusions. This version keeps disclosed diagnostics, replaces false precision with ranges and break-even tests, and states what cannot be concluded from public data.",
        4,
    )
    headers(ws, 4, ["# / analysis", "Expert disposition", "Sheet", "Confidence"])
    catalog = [
        ("1. Issue tree + hypotheses", "Retained. Operating facts are defensible; causal claims remain hypotheses.", "02_IssueTree", "High"),
        ("2. Internet revenue bridge", "Rebuilt using 2025Q1–2026Q2 only; no invented 2023 quarterly customers.", "03_InternetBridge", "High / derived"),
        ("3. Trading comps + event study", "Rebuilt. No annualized CMCSA Q1 FCF yield or mixed constructed/published multiples.", "04_CompsEvent", "Medium"),
        ("4. Reverse DCF", "Rebuilt as a cost-of-equity range. Output is implied FCFE path, not an Internet forecast.", "05_ReverseDCF", "Medium"),
        ("5. ROIC / economic profit", "Rebuilt on average invested capital; product ROIC removed as non-estimable.", "06_ROIC_EP", "Medium-high"),
        ("6. Unit economics", "Rebuilt as a sensitivity range. Point NPV and Q1 value destruction claim removed.", "07_UnitEconomics", "Low-medium"),
        ("7. Full potential", "Replaced whole-company $42B DCF with incremental stabilization value range.", "08_FullPotential", "Medium"),
        ("8. Initiative NPV", "Replaced circular '% of prize' benefits with break-even customer thresholds.", "09_InitiativeNPV", "Medium / illustrative"),
        ("9. Funding box", "Rebuilt as sources/uses and leverage bounds; no unsupported 'payable' claim.", "10_FundingBox", "Medium-high"),
    ]
    for r, row in enumerate(catalog, 5):
        for c, value in enumerate(row, 1):
            kind = "disclosed" if c < 4 else ("caution" if "Low" in value or "Medium" in value else "calculated")
            cell(ws, r, c, value, kind)
        ws.row_dimensions[r].height = 35
    cell(ws, 14, 1, "Model governance", "caution", bold=True)
    cell(ws, 14, 2, "Core ROIC, unit-economics, and funding outputs now use live Excel formulas. Reverse-DCF solver and stabilization sensitivities are generated by the accompanying Python model and remain screening analyses—not an integrated, fully formula-linked operating model.", "caution")
    ws.merge_cells("B14:D14")
    ws.row_dimensions[14].height = 42
    section(ws, 16, "Color and interpretation", 4)
    rows = [
        ("Green", "Disclosed/public fact", "Source named on sheet", ""),
        ("Blue", "Assumption or scenario", "Change it; do not cite as fact", ""),
        ("Yellow", "Calculated/derived", "Depends on source and assumptions", ""),
        ("Purple", "Later than Q1 2026 anchor", "Context only; explicitly labeled", ""),
        ("Orange/red", "Caution / failed hypothesis", "Judgment, not a filing statement", ""),
    ]
    for r, row in enumerate(rows, 17):
        for c, value in enumerate(row, 1):
            cell(ws, r, c, value, "note" if c > 1 else "disclosed")

    # 01 Assumptions
    ws = wb.create_sheet("01_Assumptions", 1)
    setup(ws, {"A": 42, "B": 18, "C": 18, "D": 75})
    title(ws, "Inputs and assumption ranges", 4)
    note(ws, 2, "Assignment anchor: 31 Mar 2026. Q2 2026 later facts are purple. Ranges are deliberately wider than the prior draft; a consulting model should reveal what must be true, not hide uncertainty behind a single decimal.", 4)
    headers(ws, 4, ["Input", "Value / range", "Type", "Source / interpretation"])
    inputs = [
        ("CHTR shares, 31 Mar 2026", shares, "Disclosed", "10-Q Q1 2026", "#,##0"),
        ("CHTR close, 23 Apr 2026", px_pre, "Disclosed", "Yahoo close", "$0.00"),
        ("CHTR close, 24 Apr 2026", px_post, "Disclosed", "Yahoo close", "$0.00"),
        ("LTM FCF at Q1 2026", fcf_ltm, "Disclosed", "Ex99.1 Q1 2026; Charter non-GAAP", "$#,##0"),
        ("FY2025 EBIT", ebit_25, "Disclosed", "10-K FY2025", "$#,##0"),
        ("FY2025 effective tax rate", tax, "Disclosed", "10-K tax reconciliation", "0.0%"),
        ("Cost of equity range", "10% / 12% / 14%", "Assumption", "Reverse DCF sensitivity; no single beta is asserted", None),
        ("Marginal pre-tax debt cost", "6.5%–7.25%", "Assumption", "January 2026 notes issued at 7.000% and 7.375%; use market YTM for decision-grade WACC", None),
        ("WACC range", "7.5% / 8.5% / 9.5%", "Assumption", "Interim sensitivity; not a claimed point estimate", None),
        ("Terminal growth", "0.0%", "Assumption", "Mature U.S. cable; conservative", None),
        ("Internet contribution / retained sub-year", "$500 / $650 / $800", "Assumption", "Public filings do not disclose product contribution margin", None),
        ("Internet contribution margin range", "60% / 70% / 80%", "Assumption", "Unit economics sensitivity", None),
        ("Mobile contribution margin range", "15% / 30% / 40%", "Assumption", "After MVNO wholesale; not disclosed", None),
        ("Internet annual churn range", "15% / 20% / 25%", "Assumption", "Not disclosed; used only in sensitivity", None),
        ("Mobile annual churn range", "20% / 27.5% / 35%", "Assumption", "Not disclosed; used only in sensitivity", None),
        ("Internet SAC range", "$300 / $550 / $800", "Assumption", "Not disclosed; acquisition cost, not total annual marketing", None),
        ("Mobile SAC range", "$100 / $250 / $400", "Assumption", "Not disclosed", None),
    ]
    for r, (name, value, typ, source, fmt) in enumerate(inputs, 5):
        kind = "assumption" if typ == "Assumption" else "disclosed"
        cell(ws, r, 1, name, kind)
        cell(ws, r, 2, value, kind, fmt)
        cell(ws, r, 3, typ, kind)
        cell(ws, r, 4, source, "note")

    # 03 Internet bridge: use only quarters with both current and LY customer bases.
    ws = wb.create_sheet("03_InternetBridge", 3)
    setup(ws, {"A": 14, "B": 17, "C": 17, "D": 20, "E": 20, "F": 17, "G": 19, "H": 55})
    title(ws, "2. Internet revenue bridge — volume vs price/mix/allocation", 8)
    note(ws, 2, "Expert adjustment: 2024 quarterly estimates were removed because the prior model invented 2023Q1–Q3 customer counts. The defensible quarterly bridge begins in Q1 2025, when both current and prior-year period-end customer counts are available. FY2025's 10-K bridge remains the primary audited evidence.", 8)
    headers(ws, 4, ["Quarter", "Internet revenue", "YoY Δ revenue", "Average customers (000s)", "LY average (000s)", "Volume effect", "Price/mix residual", "Interpretation"])
    q = [
        ("25Q1", 5930, 5826, 30053.5, 30554.0, -95, 199, "Price/mix still covers volume"),
        ("25Q2", 5969, 5806, 29966.0, 30444.0, -91, 254, "Price/mix still covers volume"),
        ("25Q3", 5971, 5872, 29853.5, 30315.0, -89, 188, "Price/mix still covers volume"),
        ("25Q4", 5895, 5856, 29739.5, 30171.5, -84, 123, "Price/mix still covers volume"),
        ("26Q1", 5852, 5930, 29620.0, 30053.5, -86, 8, "First negative Internet dollars"),
        ("26Q2", 5776, 5969, 29474.0, 29966.0, -98, -95, "Later fact: residual also negative"),
    ]
    for r, row in enumerate(q, 5):
        later = row[0] == "26Q2"
        for c, value in enumerate(row, 1):
            if c in (6, 7):
                kind = "calculated"
            elif later:
                kind = "later"
            else:
                kind = "disclosed" if c <= 3 else "calculated"
            fmt = "$#,##0" if c in (2, 3, 6, 7) else ("#,##0.0" if c in (4, 5) else None)
            cell(ws, r, c, value, kind, fmt)
    section(ws, 13, "FY2025 disclosed bridge (primary evidence)", 8)
    headers(ws, 14, ["Period", "Volume", "Rate/product mix", "Net change", "Reported Internet revenue", "", "", "Source"])
    for c, value in enumerate(["FY2025 vs FY2024", -380, 785, 405, 23765, "", "", "CHTR 10-K FY2025; residential volume/rate-mix attribution"], 1):
        cell(ws, 15, c, value, "disclosed" if c != 4 else "calculated", "$#,##0" if c in (2, 3, 4, 5) else None)
    cell(ws, 17, 1, "Finding", "fail", bold=True)
    cell(ws, 17, 2, "Q1 2026 is the inflection from subscriber pressure to negative Internet dollars. The bridge is an attribution identity—not proof that price or bundle allocation caused churn.", "fail")
    ws.merge_cells("B17:H17")
    ws.row_dimensions[17].height = 38
    headers(ws, 20, ["Quarter", "Volume effect", "Price/mix residual"])
    for r, row in enumerate(q, 21):
        cell(ws, r, 1, row[0], "later" if row[0] == "26Q2" else "disclosed")
        cell(ws, r, 2, row[5], "calculated")
        cell(ws, r, 3, row[6], "calculated")
    chart = BarChart()
    chart.title = "Internet YoY revenue bridge ($M)"
    chart.y_axis.title = "$M"
    chart.x_axis.title = "Quarter"
    chart.add_data(Reference(ws, min_col=2, min_row=20, max_col=3, max_row=26), titles_from_data=True)
    chart.set_categories(Reference(ws, min_col=1, min_row=21, max_row=26))
    chart.height, chart.width = 8, 16
    ws.add_chart(chart, "E20")

    # 04 Comps and event study
    ws = wb.create_sheet("04_CompsEvent", 4)
    setup(ws, {"A": 31, "B": 18, "C": 18, "D": 18, "E": 65})
    title(ws, "3. Trading comps and earnings-day event study", 5)
    note(ws, 2, "Expert adjustment: removed CMCSA FCF yield annualized from one quarter and stopped mixing a constructed CHTR EV with third-party peer multiples as if they were one comparable set. Public-data conclusion is directional: cable de-rated, and Charter de-rated more on the Q1 Internet print.", 5)
    section(ws, 4, "A. Same-day industry control — 24 Apr 2026", 5)
    headers(ws, 5, ["Company", "23 Apr close", "24 Apr close", "Return", "Interpretation"])
    controls = [
        ("CHTR", 241.78, 180.13, 180.13 / 241.78 - 1, "Q1 Internet losses doubled YoY"),
        ("CMCSA", 31.64, 27.51, 27.51 / 31.64 - 1, "Industry/cable control"),
        ("CHTR minus CMCSA", "", "", (180.13 / 241.78 - 1) - (27.51 / 31.64 - 1), "Approximate Charter-specific excess decline; not a beta-adjusted abnormal return"),
    ]
    for r, row in enumerate(controls, 6):
        for c, value in enumerate(row, 1):
            cell(ws, r, c, value, "calculated" if c == 4 else "disclosed", "0.0%" if c == 4 else ("$0.00" if c in (2, 3) and value != "" else None))
    section(ws, 11, "B. Published valuation snapshots (different vendors/methods; range, not precision)", 5)
    headers(ws, 12, ["Source/date", "CHTR EV/EBITDA", "CMCSA EV/EBITDA", "Basis", "Use"])
    pubs = [
        ("Devyara ~26 Apr 2026", "6.06x", "5.65x", "Published snapshot", "Directional cross-check only"),
        ("TIKR Apr 2026", "—", "5.47x", "Forward", "Do not compare mechanically to LTM"),
        ("ValueSense Q2 2026", "5.6x", "—", "LTM; later fact", "CHTR multiple continued compressing"),
    ]
    for r, row in enumerate(pubs, 13):
        for c, value in enumerate(row, 1):
            cell(ws, r, c, value, "later" if "Q2" in row[0] else "disclosed")
    section(ws, 18, "C. Earnings-day event study", 5)
    headers(ws, 19, ["Print", "Internet net adds (000s)", "YoY change (000s)", "Close-to-close", "Interpretation"])
    events = [
        ("Q4 2024", -177, "", 0.026, "Large loss, but no new deterioration"),
        ("Q1 2025", -59, 13, 0.114, "Improved YoY; mobile/video could dominate"),
        ("Q2 2025", -116, 32, -0.185, "Missed consensus (~−73k cited) despite YoY improvement"),
        ("Q3 2025", -109, 1, 0.013, "Close recovered from negative open"),
        ("Q4 2025", -119, 58, 0.076, "Improved YoY"),
        ("Q1 2026", -120, -61, -0.255, "Almost same absolute print as Q4; doubled YoY"),
        ("Q2 2026", -172, -56, -0.025, "Later fact; −11.6% opening gap, then recovery"),
    ]
    for r, row in enumerate(events, 20):
        for c, value in enumerate(row, 1):
            kind = "later" if row[0] == "Q2 2026" else ("fail" if c == 4 and isinstance(value, float) and value < -0.10 else "disclosed")
            cell(ws, r, c, value, kind, "0.0%" if c == 4 else ("#,##0" if c in (2, 3) and value != "" else None))
    cell(ws, 29, 1, "Finding", "caution", bold=True)
    cell(ws, 29, 2, "The evidence supports a market lens—Internet surprise and YoY acceleration—but seven events are not enough to estimate a stable causal coefficient. Present paired cases, not a regression claim.", "caution")
    ws.merge_cells("B29:E29")
    ws.row_dimensions[29].height = 42

    # 05 Reverse DCF
    ws = wb.create_sheet("05_ReverseDCF", 5)
    setup(ws, {"A": 28, "B": 22, "C": 22, "D": 22, "E": 68})
    title(ws, "4. Reverse DCF — market-implied levered FCF path", 5)
    note(ws, 2, "Expert adjustment: the prior 9.55% cost of equity looked like an answer, but its beta was unsupported. This version uses a 10%–14% range and adjusts consolidated FCF by A/N's approximately 11% effective common ownership to make the Class A screen more consistent. It remains an approximation: distributions, debt flows, Cox and dilution are not modeled.", 5)
    headers(ws, 4, ["Cost of equity", "Implied 5-yr FCF CAGR at $241.78", "Implied 5-yr FCF CAGR at $180.13", "Change", "Interpretation"])
    for r, (ke, pre_g, post_g) in enumerate(implied, 5):
        cell(ws, r, 1, ke, "assumption", "0.0%")
        cell(ws, r, 2, pre_g, "calculated", "0.0%")
        cell(ws, r, 3, post_g, "calculated", "0.0%")
        cell(ws, r, 4, post_g - pre_g, "calculated", "0.0%")
        cell(ws, r, 5, "Both prices imply contraction; Apr 24 requires a materially steeper path.")
    section(ws, 10, "Market facts held fixed", 5)
    facts = [
        ("Consolidated LTM FCF ($M)", fcf_ltm, "Ex99.1 Q1 2026", "$#,##0"),
        ("A/N effective common ownership", an_ownership, "10-Q Q1 2026; approximately 11%", "0.0%"),
        ("Class A FCFE screen ($M)", class_a_fcfe_screen, "Consolidated FCF × (1−11%); approximation", "$#,##0"),
        ("Market cap 23 Apr ($M)", market_pre, "Price × Q1 shares", "$#,##0"),
        ("Market cap 24 Apr ($M)", market_post, "Price × Q1 shares", "$#,##0"),
        ("Approx. Class A FCFE yield 23 Apr", fcf_yield_pre, "89% × consolidated LTM FCF / Class A market cap", "0.0%"),
        ("Approx. Class A FCFE yield 24 Apr", fcf_yield_post, "89% × consolidated LTM FCF / Class A market cap", "0.0%"),
        ("Terminal growth", 0.0, "Assumption", "0.0%"),
    ]
    headers(ws, 11, ["Input", "Value", "Source/formula", "", ""])
    for r, (name, value, src, fmt) in enumerate(facts, 12):
        cell(ws, r, 1, name)
        cell(ws, r, 2, value, "assumption" if name == "Terminal growth" else "calculated", fmt)
        cell(ws, r, 3, src, "note")
    cell(ws, 22, 1, "Finding", "caution", bold=True)
    cell(ws, 22, 2, "Robust conclusion: the print increased the contraction embedded in the equity. Non-robust conclusion removed: '$180 prices a specific Internet run-rate.' FCFE also reflects capex, interest, taxes, working capital, ownership claims, debt flows and Cox.", "caution")
    ws.merge_cells("B22:E22")
    ws.row_dimensions[22].height = 48

    # 06 ROIC
    ws = wb.create_sheet("06_ROIC_EP", 6)
    setup(ws, {"A": 42, "B": 18, "C": 18, "D": 20, "E": 65})
    title(ws, "5. Enterprise ROIC vs WACC — product ROIC is not publicly estimable", 5)
    note(ws, 2, "Expert adjustment: ROIC now uses average 2024/2025 invested capital. The prior 'Internet/mobile/video EBITDA' allocation was deleted: Charter reports one segment, and arbitrary allocations cannot support a CEO recommendation.", 5)
    headers(ws, 4, ["Metric", "Value", "Basis", "Confidence", "Interpretation"])
    roic_rows = [
        ("FY2025 EBIT", ebit_25, "10-K", "High", "Operating earnings before financing"),
        ("NOPAT", nopat, "EBIT × (1−22.7%)", "Medium-high", "Uses effective tax rate, not unusually low cash taxes"),
        ("YE2024 invested capital", ic_24, "Equity + NCI + debt + EIP − cash", "Medium", "Financing-side approximation"),
        ("YE2025 invested capital", ic_25, "Same", "Medium", "Includes goodwill/franchises"),
        ("Average invested capital", avg_ic, "Average of YE2024 and YE2025", "Medium", "Correct denominator for FY flow"),
        ("Enterprise ROIC", roic, "NOPAT / average IC", "Medium", "Installed base remains economically productive"),
    ]
    for r, row in enumerate(roic_rows, 5):
        for c, value in enumerate(row, 1):
            fmt = "0.0%" if row[0] == "Enterprise ROIC" and c == 2 else ("$#,##0" if c == 2 and isinstance(value, (int, float)) else None)
            cell(ws, r, c, value, "calculated" if c == 2 and row[0] not in ("FY2025 EBIT",) else "disclosed", fmt)
    # Make core calculations live in Excel.
    ws["B6"] = "=B5*(1-22.7%)"
    ws["B9"] = "=AVERAGE(B7:B8)"
    ws["B10"] = "=B6/B9"
    section(ws, 13, "Economic-profit sensitivity ($M)", 5)
    headers(ws, 14, ["WACC", "ROIC − WACC", "Economic profit", "", "Read"])
    for r, wacc in enumerate(wacc_cases, 15):
        ep = (roic - wacc) * avg_ic
        cell(ws, r, 1, wacc, "assumption", "0.0%")
        cell(ws, r, 2, f"=$B$10-A{r}", "calculated", "0.0%")
        cell(ws, r, 3, f"=B{r}*$B$9", "calculated", "$#,##0")
        cell(ws, r, 5, "Positive on book invested capital" if ep > 0 else "Below hurdle", "note")
    section(ws, 20, "What can and cannot be said by product", 5)
    statements = [
        ("Internet", "Can estimate revenue/customer and revenue bridge.", "Cannot estimate product ROIC or EBITDA from filings.", "High / not estimable"),
        ("Mobile", "Can estimate service revenue/line.", "Cannot isolate Verizon wholesale, device margin, or retention benefit.", "High / not estimable"),
        ("Video", "Programming cost is disclosed at company level.", "Cannot assign all programming/shared costs to a clean product P&L.", "Medium / not estimable"),
    ]
    headers(ws, 21, ["Product", "Defensible", "Not defensible", "Confidence", ""])
    for r, row in enumerate(statements, 22):
        for c, value in enumerate(row, 1):
            cell(ws, r, c, value, "disclosed" if c < 3 else "caution")
    cell(ws, 27, 1, "Finding", "caution", bold=True)
    cell(ws, 27, 2, "Enterprise book ROIC is approximately 8.7%. Whether it clears WACC depends on a reasonable 6.5%–8.5% range. That supports 'not in distress'; it does not prove that incremental mobile growth offsets broadband erosion.", "caution")
    ws.merge_cells("B27:E27")
    ws.row_dimensions[27].height = 42

    # 07 Unit economics
    ws = wb.create_sheet("07_UnitEconomics", 7)
    setup(ws, {"A": 43, "B": 18, "C": 18, "D": 52, "E": 50, "F": 14, "G": 14, "H": 14, "I": 14, "J": 14, "K": 14})
    title(ws, "6. Unit economics — sensitivity, not a disclosed point estimate", 5)
    note(ws, 2, "Expert adjustment: removed the prior $2,156 Internet / $293 mobile point estimates and the claim that Q1 net adds destroyed a specific dollar amount. Churn, CAC, wholesale cost, and product contribution are not disclosed. The decision-useful output is a range and the conditions under which mobile economics fail.", 5)
    avg_inet = (30083 + 29680) / 2
    avg_mobile = (9858 + 11766) / 2
    inet_arpu = 23765 / avg_inet * 1000 / 12
    mobile_arpu = 3762 / avg_mobile * 1000 / 12
    headers(ws, 4, ["Metric", "Internet", "Mobile", "Type", "Source / limitation"])
    unit_facts = [
        ("Average units FY2025 (000s)", avg_inet, avg_mobile, "Calculated", "Average YE2024/YE2025"),
        ("Service revenue FY2025 ($M)", 23765, 3762, "Disclosed", "10-K; mobile excludes devices"),
        ("Revenue per unit/month", inet_arpu, mobile_arpu, "Calculated", "Gross product revenue, not margin"),
    ]
    for r, row in enumerate(unit_facts, 5):
        for c, value in enumerate(row, 1):
            fmt = "$0.00" if row[0] == "Revenue per unit/month" and c in (2, 3) else ("#,##0" if c in (2, 3) else None)
            cell(ws, r, c, value, "calculated" if row[3] == "Calculated" and c in (2, 3) else "disclosed", fmt)
    section(ws, 10, "Lifetime contribution NPV per unit: revenue × margin / (10% + annual churn) − SAC", 5)
    headers(ws, 11, ["Case", "Internet NPV", "Mobile NPV", "Assumptions", "Interpretation", "Inet margin", "Inet churn", "Inet SAC", "Mobile margin", "Mobile churn", "Mobile SAC"])
    cases = [
        ("Low", 0.60, 0.25, 800, 0.15, 0.35, 400),
        ("Base", 0.70, 0.20, 550, 0.30, 0.275, 250),
        ("High", 0.80, 0.15, 300, 0.40, 0.20, 100),
    ]
    for r, (name, im, ic, isac, mm, mc, msac) in enumerate(cases, 12):
        inet_npv = inet_arpu * 12 * im / (0.10 + ic) - isac
        mobile_npv = mobile_arpu * 12 * mm / (0.10 + mc) - msac
        assumptions = f"Internet: {im:.0%} margin, {ic:.0%} churn, ${isac} SAC. Mobile: {mm:.0%} margin, {mc:.1%} churn, ${msac} SAC."
        cell(ws, r, 1, name, "assumption")
        cell(ws, r, 2, f"=$B$7*12*F{r}/(10%+G{r})-H{r}", "calculated", "$#,##0")
        cell(ws, r, 3, f"=$C$7*12*I{r}/(10%+J{r})-K{r}", "calculated", "$#,##0")
        cell(ws, r, 4, assumptions, "assumption")
        cell(ws, r, 5, "Mobile can be near-zero/negative at low margins; Internet remains larger across these cases.", "note")
        for col, value, fmt in [
            (6, im, "0.0%"), (7, ic, "0.0%"), (8, isac, "$#,##0"),
            (9, mm, "0.0%"), (10, mc, "0.0%"), (11, msac, "$#,##0"),
        ]:
            cell(ws, r, col, value, "assumption", fmt)
    cell(ws, 17, 1, "Finding", "caution", bold=True)
    cell(ws, 17, 2, "The robust result is ordinal, not precise: Internet customer economics are likely materially larger because revenue/unit is >2× and mobile bears MVNO wholesale cost. The workbook cannot prove an exact ratio without Charter churn, CAC, wholesale, and retention data.", "caution")
    ws.merge_cells("B17:E17")
    ws.row_dimensions[17].height = 48

    # 08 Full potential
    ws = wb.create_sheet("08_FullPotential", 8)
    setup(ws, {"A": 38, "B": 18, "C": 18, "D": 18, "E": 18, "F": 65})
    title(ws, "7. Full potential — incremental value of stabilizing Internet", 6)
    note(ws, 2, "Expert adjustment: removed the prior whole-company $42B 'prize.' That result was driven by an unsupported 6.53% WACC, arbitrary EBITDA drift, and a terminal value applied to those assumptions. This model values only the incremental retained Internet base versus the stated Base path.", 6)
    section(ws, 4, "A. Operating paths (000s net adds)", 6)
    headers(ws, 5, ["Scenario", "2026", "2027", "2028", "2029 onward", "Definition"])
    paths = [
        ("Base/current", -480, -480, -480, -320, "−120k/q through 2028, then modest improvement"),
        ("Stabilize/full potential", -360, -180, 0, 0, "Linear stabilization by YE2028"),
    ]
    for r, row in enumerate(paths, 6):
        for c, value in enumerate(row[:5], 1):
            cell(ws, r, c, value, "assumption", "#,##0" if c > 1 else None)
        cell(ws, r, 6, row[5], "assumption")
    section(ws, 10, "B. Incremental equity value ($M) of stabilization vs Base", 6)
    headers(ws, 11, ["Contribution / retained sub-year", "WACC 7.5%", "WACC 8.5%", "WACC 9.5%", "Interpretation", ""])
    for r, contribution in enumerate(contribution_cases, 12):
        cell(ws, r, 1, contribution, "assumption", "$#,##0")
        for c, wacc in enumerate(wacc_cases, 2):
            cell(ws, r, c, stabilization[(contribution, wacc)], "calculated", "$#,##0")
        cell(ws, r, 5, "Incremental after-tax cash flow + terminal; no multiple re-rating is added.", "note")
        ws.merge_cells(start_row=r, start_column=5, end_row=r, end_column=6)
    base_pv, annual = incremental_stabilization_value(650, 0.085)
    section(ws, 17, "C. Midpoint mechanics ($650 contribution, 8.5% WACC)", 6)
    headers(ws, 18, ["Year", "Base EOP (000s)", "Stabilize EOP (000s)", "Incremental avg customers", "After-tax incremental cash flow", ""])
    for r, (year, base_eop, full_eop, diff, avg_diff, cf) in enumerate(annual, 19):
        cell(ws, r, 1, year, "assumption")
        cell(ws, r, 2, base_eop, "calculated", "#,##0")
        cell(ws, r, 3, full_eop, "calculated", "#,##0")
        cell(ws, r, 4, avg_diff, "calculated", "#,##0")
        cell(ws, r, 5, cf, "calculated", "$#,##0")
    cell(ws, 29, 1, "Finding", "caution", bold=True)
    cell(ws, 29, 2, f"At the midpoint assumptions, stabilizing by YE2028 is worth about ${base_pv:,.0f}M—not $42B. The defensible range is the matrix, and it excludes any separate price/mix recovery, capex differential, Cox, or re-rating. Those should be explicit add-ons, not hidden in 'other EBITDA drift.'", "caution")
    ws.merge_cells("B29:F29")
    ws.row_dimensions[29].height = 50

    # 09 Initiative business case
    ws = wb.create_sheet("09_InitiativeNPV", 9)
    setup(ws, {"A": 35, "B": 18, "C": 18, "D": 18, "E": 70})
    title(ws, "8. Initiative business case — break-even thresholds", 5)
    note(ws, 2, "Expert adjustment: removed benefits defined as an arbitrary percentage of the Full-Potential prize. A valid initiative case models operational drivers. Until the team selects a move, the honest question is: how many durable Internet customer-equivalents must it save to cover its cost?", 5)
    headers(ws, 4, ["Illustrative spend", "PV cost", "Required annual EBITDA", "Required durable customer-equivalents", "Assumptions"])
    initiative_cases = [
        ("$1B opex over 2 years", 1000, 2, 3, False),
        ("$2B opex over 2 years", 2000, 2, 3, False),
        ("$3B opex over 2 years", 3000, 2, 3, False),
        ("$4B capex over 4 years", 4000, 4, 4, True),
        ("$8B capex over 5 years", 8000, 5, 4, True),
    ]
    for r, (label, spend, spend_years, start, capex) in enumerate(initiative_cases, 5):
        pv_cost, req_ebitda, req_customers = initiative_break_even(spend, spend_years, start, 650, 0.085, tax, capex)
        cell(ws, r, 1, label, "assumption")
        cell(ws, r, 2, pv_cost, "calculated", "$#,##0")
        cell(ws, r, 3, req_ebitda, "calculated", "$#,##0")
        cell(ws, r, 4, req_customers / 1000, "calculated", "#,##0")
        cell(ws, r, 5, f"8.5% WACC, $650 annual contribution/customer, 22.7% tax; steady benefit begins year {start}. {'Capex gets no tax shield in this screen.' if capex else 'Opex is tax-deductible.'}", "note")
    section(ws, 12, "How to replace this screen with the team's recommendation", 5)
    steps = [
        ("1", "Define the mechanism", "Example: reduce involuntary churn, defend FWA-sensitive cohorts, acquire rural customers—not 'improve trajectory.'"),
        ("2", "Define measurable unit impact", "Customers retained/acquired, ARPU effect, contribution, ramp, cannibalization."),
        ("3", "Define cost and timing", "Opex/capex by year and the first earnings print affected."),
        ("4", "Calculate NPV and downside", "Use the operational cash flows directly; do not multiply by a percent of a valuation gap."),
    ]
    headers(ws, 13, ["Step", "Required input", "Standard", "", ""])
    for r, row in enumerate(steps, 14):
        cell(ws, r, 1, row[0], "disclosed")
        cell(ws, r, 2, row[1], "disclosed")
        cell(ws, r, 3, row[2], "note")
        ws.merge_cells(start_row=r, start_column=3, end_row=r, end_column=5)
    cell(ws, 20, 1, "Finding", "caution", bold=True)
    cell(ws, 20, 2, "A $2B opex move does not have a +$32B NPV merely because it 'captures 80%' of a scenario gap. It must durably save roughly the customer-equivalent threshold shown above, with evidence that the quarterly Internet print changes inside the CEO's horizon.", "caution")
    ws.merge_cells("B20:E20")
    ws.row_dimensions[20].height = 48

    # 10 Funding box
    ws = wb.create_sheet("10_FundingBox", 10)
    setup(ws, {"A": 42, "B": 18, "C": 18, "D": 70, "E": 24})
    title(ws, "9. Capital allocation and funding box", 5)
    note(ws, 2, "Expert adjustment: distinguishes liquidity, annual internally generated cash, debt capacity, and board authorization. The prior model treated all as interchangeable and concluded an illustrative initiative was 'payable.' That cannot be concluded without Cox closing financing and covenant/rating analysis.", 5)
    headers(ws, 4, ["Item", "Amount", "Type", "Interpretation"])
    funding = [
        ("Cash, 31 Mar 2026", 517, "Liquidity", "Disclosed"),
        ("Undrawn facilities, 31 Mar 2026", 4600, "Liquidity", "Approximate, disclosed"),
        ("Cash + facilities", 5117, "Liquidity", "Not recurring cash generation; drawing raises debt"),
        ("LTM FCF, Q1 2026", 4812, "Annual cash generation", "Charter non-GAAP"),
        ("FY2025 repurchases", 5400, "Discretionary use", "Shares + units; exceeded FY2025 FCF"),
        ("Q1 2026 repurchases", 963, "Discretionary use", "4.3M shares"),
        ("Cox cash purchase price at anchor", 4000, "Transaction use", "FY2025 10-K / announcement package"),
        ("Cox cash purchase price, Q2 update", 4200, "Later transaction use", "Q2 10-Q; later fact"),
        ("Cox convertible preferred claim", 6000, "Transaction financing claim", "6.875% coupon; FY2025 10-K"),
        ("Annual Cox preferred dividend", 413, "Fixed cash charge", "Cox presentation; approximately $412.5M"),
        ("Cox common units issued", 33.6, "Dilution (million units)", "Exchangeable one-for-one; FY2025 10-K"),
        ("Stated leverage, Q1 2026", 4.15, "Leverage", "Company net debt / LTM EBITDA"),
        ("Pre-close upper band", 4.50, "Leverage", "Not a target or committed capacity"),
        ("Arithmetic room to 4.5×", (4.50 - 4.15) * 22582, "Debt headroom screen", "Pre-Cox EBITDA only; ignores ratings, covenants, fees, and transaction EBITDA"),
        ("Debt reduction to 3.5×", (4.15 - 3.50) * 22582, "Long-term constraint", "Before Cox EBITDA/debt; directional only"),
    ]
    for r, row in enumerate(funding, 5):
        later = "Q2" in row[0]
        for c, value in enumerate(row, 1):
            fmt = "0.00x" if row[2] == "Leverage" and c == 2 else ("$#,##0" if c == 2 and row[2] != "Leverage" else None)
            kind = "later" if later else ("calculated" if row[0] in ("Cash + facilities", "Arithmetic room to 4.5×", "Debt reduction to 3.5×") else "disclosed")
            cell(ws, r, c, value, kind, fmt)
    section(ws, 22, "One-year sources / uses screen ($M; not a financing plan)", 5)
    headers(ws, 23, ["Scenario", "FCF/Liquidity source", "Cox cash", "Repurchases / initiative", "Residual / financing need"])
    screens = [
        ("Repeat FY2025 repurchases + Cox", 4812, -4000, -5400),
        ("Pause repurchases + Cox", 4812, -4000, 0),
        ("Pause repurchases + Cox + $2B opex", 4812, -4000, -2000),
    ]
    for r, row in enumerate(screens, 24):
        for c, value in enumerate(row, 1):
            cell(ws, r, c, value, "assumption" if r > 21 or c == 1 else "calculated", "$#,##0" if c > 1 else None)
        cell(ws, r, 5, f"=SUM(B{r}:D{r})", "calculated", "$#,##0")
    cell(ws, 29, 1, "Finding", "caution", bold=True)
    cell(ws, 29, 2, "Pausing buybacks creates financial flexibility; it does not create value by itself. Cox plus a material initiative likely requires some combination of retained FCF, liquidity, debt, preferred distributions and sequencing. A recommendation must show the pro-forma Cox EBITDA/FCF, leverage, dilution and fixed charges—not simply call buybacks a funding source.", "caution")
    ws.merge_cells("B29:E29")
    ws.row_dimensions[29].height = 50

    # 11 scorecard
    ws = wb.create_sheet("11_Scorecard", 11)
    setup(ws, {"A": 40, "B": 20, "C": 55, "D": 65})
    title(ws, "Expert scorecard — what the nine analyses actually support", 4)
    headers(ws, 3, ["Analysis", "Confidence", "Supported conclusion", "Do not claim"])
    score = [
        ("1. Issue tree", "High", "Internet trajectory is the central operating hypothesis.", "That subscriber losses alone explain every stock move."),
        ("2. Revenue bridge", "High / derived", "Internet dollars turned negative in Q1 2026 as mix stopped covering volume.", "That price changes caused churn."),
        ("3. Comps/event", "Medium", "Apr 24 contained industry and Charter-specific components.", "A statistically stable causal coefficient from seven events."),
        ("4. Reverse DCF", "Medium", "The print increased contraction embedded in FCFE.", "A precise Internet net-add path implied by $180."),
        ("5. ROIC/EP", "Medium-high", "Enterprise book ROIC is ~8.7%; Charter is not in distress.", "Product ROIC or EBITDA from arbitrary allocations."),
        ("6. Unit economics", "Low-medium", "Internet economics likely exceed mobile across reasonable cases.", "Exact NPV per unit without churn/CAC/wholesale data."),
        ("7. Full potential", "Medium", "Stabilization has material incremental value; use the sensitivity matrix.", "A $42B prize or whole-company fair value."),
        ("8. Initiative case", "Medium / illustrative", "Break-even thresholds define what a move must deliver.", "Positive NPV based on an arbitrary share of a valuation gap."),
        ("9. Funding box", "Medium-high", "Buyback pause adds flexibility; Cox constrains sequencing.", "That an initiative is funded without a financing/leverage plan."),
    ]
    for r, row in enumerate(score, 4):
        for c, value in enumerate(row, 1):
            cell(ws, r, c, value, "caution" if c in (2, 4) else "disclosed")
        ws.row_dimensions[r].height = 35
    section(ws, 15, "CEO-ready synthesis", 4)
    cell(ws, 16, 1, "The defensible story", "calculated", bold=True)
    cell(ws, 16, 2, "Charter remains economically productive on its installed asset base, but the Q1 print caused investors to embed a materially steeper cash-flow contraction. Mobile growth is not demonstrably large enough in economic profit to offset Internet erosion. Stabilizing Internet has material value, but public data support a range—not the prior $42B point estimate. The recommendation still needs a mechanism, break-even customer impact, time-to-print, and financing plan.", "calculated")
    ws.merge_cells("B16:D16")
    ws.row_dimensions[16].height = 72

    # Move retained issue-tree sheet into #2 position and relabel its finding.
    issue = wb["02_IssueTree"]
    issue.sheet_properties.tabColor = NAVY

    # Reorder to exact analysis flow.
    order = [
        "00_ReadMe",
        "01_Assumptions",
        "02_IssueTree",
        "03_InternetBridge",
        "04_CompsEvent",
        "05_ReverseDCF",
        "06_ROIC_EP",
        "07_UnitEconomics",
        "08_FullPotential",
        "09_InitiativeNPV",
        "10_FundingBox",
        "11_Scorecard",
    ]
    wb._sheets = [wb[name] for name in order]
    force_georgia(wb)
    wb.calculation.fullCalcOnLoad = True
    wb.calculation.forceFullCalc = True
    wb.calculation.calcMode = "auto"
    wb.save(BOOK)
    print(f"Expert-reviewed workbook written: {BOOK}")
    print(f"ROIC={roic:.2%}; midpoint stabilization PV=${base_pv:,.0f}M")
    print("Reverse DCF:", [(f"{k:.0%}", f"{a:.1%}", f"{b:.1%}") for k, a, b in implied])


if __name__ == "__main__":
    main()
