"""
Render Charter GAP / decisions analysis to a client-readable PDF.

Source of truth: Decisions/decisions.md (Q1 2026 anchor).
Companion canvases: canvases/chtr-gap-analysis.canvas.tsx,
canvases/chtr-churn-response-playbook.canvas.tsx
Draft work-plan, not a recommendation. Tracker category cells stay empty.
Playbook is conditional and does not fire until those cells are filled.
"""
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    HRFlowable,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(r"c:\Users\Owner\Desktop\MAN6930 Case")
OUT = ROOT / "Decisions" / "CHTR-GAP-Analysis.pdf"

# Palette — gray first, one accent (same family as Analysis/render_relative_performance_pdf.py)
RED = colors.HexColor("#C44B4B")
BLUE = colors.HexColor("#2E6FA8")
GRAY = colors.HexColor("#666666")
GRAY_BAR = colors.HexColor("#9A9A9A")
LIGHT = colors.HexColor("#F4F4F4")
LIGHT_RED = colors.HexColor("#F8ECEC")
LIGHT_BLUE = colors.HexColor("#E8F0F7")
LINE = colors.HexColor("#DDDDDD")
INK = colors.HexColor("#1A1A1A")
HEADER_BG = colors.HexColor("#2A2A2A")
EMPTY_BG = colors.HexColor("#FBF3E4")


def grouped_bars(
    data_rows,
    categories,
    series_meta,
    width=480,
    height=165,
    y_max=None,
    value_suffix="",
):
    """Grouped bars that always begin at zero. series_meta: list of (name, color)."""
    from reportlab.graphics.shapes import Drawing, Line, Rect, String

    all_vals = [v for row in data_rows for v in row]
    lo = 0
    hi = y_max if y_max is not None else max(all_vals) * 1.18
    if hi <= 0:
        hi = 1
    span = hi - lo

    d = Drawing(width, height)
    pad_l, pad_r, pad_t, pad_b = 36, 12, 16, 36
    inner_w = width - pad_l - pad_r
    inner_h = height - pad_t - pad_b

    def y_scale(v):
        return pad_b + ((v - lo) / span) * inner_h

    zero_y = y_scale(0)
    d.add(Line(pad_l, zero_y, width - pad_r, zero_y, strokeColor=GRAY, strokeWidth=1))
    d.add(String(4, zero_y - 3, "0", fontSize=7, fillColor=GRAY))

    n_cat = len(categories)
    n_ser = len(data_rows)
    group_w = inner_w / n_cat
    bar_w = min(22, (group_w * 0.72) / max(n_ser, 1))

    for ci, cat in enumerate(categories):
        gx = pad_l + ci * group_w + group_w / 2
        for si, row in enumerate(data_rows):
            v = row[ci]
            y1 = y_scale(v)
            h = max(1.5, abs(y1 - zero_y))
            x = gx - (n_ser * bar_w + (n_ser - 1) * 4) / 2 + si * (bar_w + 4)
            d.add(Rect(x, zero_y, bar_w, h, fillColor=series_meta[si][1], strokeColor=None))
            label = f"{v:g}{value_suffix}"
            d.add(String(x, y1 + 2, label, fontSize=6.5, fillColor=INK))
        cat_label = cat if len(cat) <= 28 else cat[:27] + "…"
        d.add(String(gx - min(40, len(cat_label) * 2.1), 8, cat_label, fontSize=7, fillColor=GRAY))

    lx = pad_l
    for name, col in series_meta:
        d.add(Rect(lx, height - 12, 8, 8, fillColor=col, strokeColor=None))
        d.add(String(lx + 11, height - 11, name, fontSize=7, fillColor=INK))
        lx += 8 + 6 + min(140, len(name) * 4.2) + 12

    return d


def _styles():
    styles = getSampleStyleSheet()
    title = ParagraphStyle(
        "Title2",
        parent=styles["Heading1"],
        fontSize=15,
        textColor=INK,
        spaceAfter=6,
        leading=19,
    )
    h2 = ParagraphStyle(
        "H2",
        parent=styles["Heading2"],
        fontSize=10.5,
        textColor=INK,
        spaceBefore=11,
        spaceAfter=4,
        leading=13.5,
    )
    body = ParagraphStyle(
        "Body2",
        parent=styles["Normal"],
        fontSize=8.5,
        textColor=INK,
        leading=11.2,
        spaceAfter=4,
    )
    small = ParagraphStyle(
        "Small",
        parent=styles["Normal"],
        fontSize=7,
        textColor=GRAY,
        leading=9,
        spaceAfter=3,
    )
    cell = ParagraphStyle(
        "Cell",
        parent=styles["Normal"],
        fontSize=7.5,
        textColor=INK,
        leading=9.5,
        alignment=TA_LEFT,
    )
    cell_r = ParagraphStyle(
        "CellR",
        parent=cell,
        alignment=TA_CENTER,
    )
    cell_h = ParagraphStyle(
        "CellH",
        parent=cell,
        textColor=colors.white,
        fontName="Helvetica-Bold",
        fontSize=7.5,
    )
    glance = ParagraphStyle(
        "Glance",
        parent=styles["Normal"],
        fontSize=8,
        textColor=INK,
        leading=10.5,
        alignment=TA_CENTER,
    )
    callout = ParagraphStyle(
        "Callout",
        parent=styles["Normal"],
        fontSize=9,
        textColor=INK,
        leading=12,
        alignment=TA_LEFT,
    )
    bullet = ParagraphStyle(
        "Bullet",
        parent=body,
        leftIndent=12,
        bulletIndent=0,
        spaceAfter=2,
    )
    return title, h2, body, small, cell, cell_r, cell_h, glance, callout, bullet


def _header_row(headers, cell_h):
    return [Paragraph(f"<b>{h}</b>", cell_h) for h in headers]


def _table(data, col_widths, extra_style=None):
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style = [
        ("BACKGROUND", (0, 0), (-1, 0), HEADER_BG),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 7.5),
        ("GRID", (0, 0), (-1, -1), 0.4, LINE),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT]),
    ]
    if extra_style:
        style.extend(extra_style)
    t.setStyle(TableStyle(style))
    return t


def build():
    title, h2, body, small, cell, cell_r, cell_h, glance, callout, bullet = _styles()

    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=letter,
        leftMargin=0.55 * inch,
        rightMargin=0.55 * inch,
        topMargin=0.48 * inch,
        bottomMargin=0.48 * inch,
        title="Charter GAP Analysis - Quarterly Net-Loss Tracker",
        author="MAN6930 Analysis",
    )
    story = []
    cw = 7.4 * inch

    # --- Headline ---
    story.append(
        Paragraph(
            "The stock fell on capex, rural, and a dead add engine — ops and "
            "marketing cannot act without a quarterly loss tracker by category",
            title,
        )
    )
    story.append(
        Paragraph(
            "Draft work-plan, not a recommendation · Anchor: end Q1 2026 · "
            "Parent frames: Root B (firm underperformance vs Comcast on Internet) · "
            "Root C (the tape prices the Internet print)",
            small,
        )
    )
    story.append(
        Paragraph(
            "Three priced facts: capital is not buying Internet growth; the rural "
            "program cannot close the hole and is expensive to leave; the old add "
            "engine (people moving, video as lock-in) is gone. Those causes stay "
            "un-actionable because Charter has no standing <b>system that tracks "
            "quarterly net Internet loss by category</b>. They see a company-level "
            "net print (−120k Q1) and cannot see (a) the churn <i>rate</i> (gross "
            "disconnects / base vs failed acquisition) or (b) the <i>division of "
            "where</i> they are losing. That is the first gap to close.",
            body,
        )
    )

    glance_data = [
        [
            Paragraph("<b>~80%</b><br/>Five-year share-price loss", glance),
            Paragraph("<b>~25%</b><br/>Q1 2026 one-day drop", glance),
            Paragraph("<b>−120k</b><br/>Q1 Internet customers", glance),
            Paragraph("<b>−1.3%</b><br/>Q1 Internet revenue", glance),
            Paragraph("<b>+19% / −12%</b><br/>Q1 capex / FCF", glance),
        ]
    ]
    gt = Table(glance_data, colWidths=[cw / 5.0] * 5)
    gt.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), LIGHT_RED),
                ("BOX", (0, 0), (-1, -1), 0.5, LINE),
                ("INNERGRID", (0, 0), (-1, -1), 0.4, LINE),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    story.append(Spacer(1, 6))
    story.append(gt)
    story.append(
        Paragraph(
            "Q1 Adj. EBITDA −2.2% (RETRIEVED · Ex99.1). Internet −120k ≈2× Q1’25 "
            "(RETRIEVED · Ex99.1). Stock path RETRIEVED · Team Case Brief. "
            "The company is not in financial distress. Owners sold the "
            "<i>direction</i>: spend went up, the profit engine shrank, and the "
            "programs that were supposed to offset it (rural, network evolution, "
            "video/mobile optics) did not change the Internet slope. "
            "Source: Ex99.1 / Team Case Brief · Q1 2026 anchor.",
            small,
        )
    )
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width="100%", thickness=0.5, color=LINE))

    # --- Cause 1: capex ---
    story.append(
        Paragraph(
            "Charter spends twice Comcast’s cable-like intensity and still lost the Internet print",
            h2,
        )
    )
    story.append(
        Paragraph(
            "Poor capex is conversion, not a missing upgrade program. Charter spent "
            "<b>$11.7B</b> in FY2025 — <b>21.3% of revenue</b>, <b>51% of Adj. EBITDA</b>. "
            "Comcast’s cable-like Connectivity &amp; Platforms segment spent "
            "<b>10.8% of C&amp;P revenue</b> and <b>27% of C&amp;P EBITDA</b> "
            "(RETRIEVED). Charter is a connectivity pure-play spending ~2× the peer’s intensity.",
            body,
        )
    )
    story.append(
        grouped_bars(
            [[21.3, 51], [10.8, 27]],
            ["Capex / revenue", "Capex / Adj. EBITDA"],
            [("CHTR FY2025", RED), ("CMCSA C&P FY2025", GRAY_BAR)],
            y_max=62,
            value_suffix="%",
        )
    )
    story.append(
        Paragraph(
            "Percent. CHTR ~2× peer intensity on both ratios. Bars begin at zero. "
            "CHTR: $11.7B FY2025. Do not compare CHTR to CMCSA consolidated "
            "(parks/media). Source: CHTR 10-K FY2025 · CMCSA trending · RETRIEVED.",
            small,
        )
    )
    story.append(
        Paragraph(
            "Q1 2026 made the conversion failure visible in one quarter: capex "
            "<b>$2.86B vs $2.40B</b> (+19%); upgrade/rebuild <b>+71%</b> ($675M vs $395M); "
            "CPE +41%; Internet <b>−120k</b> and Internet dollars <b>−1.3%</b>; FCF <b>−12%</b>. "
            "Network-evolution completion is still <b>end-2027</b>. Invincible WiFi launched "
            "in February — one month of the print. The market is not punishing "
            "“too little plant.” It is punishing plant that does not produce Internet "
            "customers. Waiting for 2027 roll-off is the base-case capital story; it "
            "does not satisfy the CEO charge by itself.",
            body,
        )
    )
    story.append(
        Paragraph(
            "<b>Need to be on:</b> capex productivity — dollars of capital per "
            "<i>net Internet add</i> (currently negative), not miles of plant or "
            "“on-time vs 2027.” Any new spend must clear a higher bar than Comcast’s "
            "cable segment. Any deferral must name what gets cut (rural pace, evolution timing, CPE).",
            body,
        )
    )

    # --- Cause 2: rural ---
    story.append(
        Paragraph(
            "Rural remainder is a one-time 170k stock — smaller than one quarter of the Comcast slope gap",
            h2,
        )
    )
    story.append(
        Paragraph(
            "The rural initiative is doing what it was built to do, and it still cannot "
            "close the hole. Rural CR +41k covered 20% of the Q1 core CR hole (−204k). "
            "Remainder at a generous 54% take is a <b>one-time stock of 170k</b> — smaller "
            "than one quarter of the Comcast slope gap (179k), and not repeatable. "
            "Management’s own words are “long-term infrastructure-style returns.” "
            "Estimated EBITDA yield on capital is ~3.9% (company margin applied to "
            "rural — <b>ESTIMATED</b>). That is not a 24-month Internet closer.",
            body,
        )
    )
    story.append(
        grouped_bars(
            [[170, 179]],
            ["Rural remainder @54% take (one-time, 000s)", "YoY Internet slope gap vs CMCSA (one quarter, 000s)"],
            [("Customers (000s)", RED)],
            y_max=220,
        )
    )
    story.append(
        Paragraph(
            "Thousands of customers. Remainder = 315k leftover passings × 54% company "
            "take = 170k (derived; one-time). Slope gap 179k in one quarter (derived). "
            "At 38% rural take the remainder is 120k. Bars begin at zero. Single series "
            "accent = the comparison the closer thesis fails. Source: Ex99.1 Q1 2026 / "
            "trending · derived identities.",
            small,
        )
    )

    rural_header = _header_row(["Line", "Q1 2026", "Tag"], cell_h)
    rural_rows = [
        rural_header,
        [
            Paragraph("Rural CR adds", cell),
            Paragraph("<b>+41k</b>", cell_r),
            Paragraph("RETRIEVED · Ex99.1", cell),
        ],
        [
            Paragraph("Core CR adds (company − rural)", cell),
            Paragraph("<b>−204k</b>", cell_r),
            Paragraph("derived · identity", cell),
        ],
        [
            Paragraph("Rural cover of the core hole", cell),
            Paragraph("20%", cell_r),
            Paragraph("derived", cell),
        ],
        [
            Paragraph("Rural add vs Q1 2025", cell),
            Paragraph("+2k", cell_r),
            Paragraph("derived — explains none of the −61k Internet YoY break", cell),
        ],
        [
            Paragraph("Rural take of activated passings", cell),
            Paragraph("38.1% (stuck 37–38% for 8 quarters)", cell_r),
            Paragraph("RETRIEVED · trending", cell),
        ],
        [
            Paragraph("Company take of passings", cell),
            Paragraph("54.0%", cell_r),
            Paragraph("RETRIEVED", cell),
        ],
        [
            Paragraph("Rural share of company revenue", cell),
            Paragraph("1.6% ($221M / $13,597M)", cell_r),
            Paragraph("RETRIEVED", cell),
        ],
        [
            Paragraph("Cumulative spend / passings", cell),
            Paragraph("~$8.1B / 1.385M ≈ <b>$5,900 per passing</b>", cell_r),
            Paragraph("RETRIEVED spend; derived unit cost", cell),
        ],
        [
            Paragraph("Cost per rural CR before grants", cell),
            Paragraph("≈ <b>$15,400</b>", cell_r),
            Paragraph("derived", cell),
        ],
        [
            Paragraph("Remainder to 1.7M floor", cell),
            Paragraph("315k passings → 120k CR at 38% take, 170k at 54%", cell_r),
            Paragraph("derived", cell),
        ],
        [
            Paragraph("YoY Internet slope gap vs Comcast", cell),
            Paragraph("179k in <i>one quarter</i>", cell_r),
            Paragraph("derived", cell),
        ],
    ]
    story.append(
        _table(
            rural_rows,
            [2.15 * inch, 2.85 * inch, 2.4 * inch],
        )
    )
    story.append(
        Paragraph(
            "<b>Hard to get out of.</b> Since 2022 Charter has spent <b>$7.7B</b> and "
            "targeted <b>&gt;1.7M</b> passings, <b>&gt;$8B</b> total, <b>&gt;$2B</b> in "
            "RDOF / BEAD / state awards (RETRIEVED). The 10-K is explicit: miss RDOF "
            "rules and the FCC can treat Charter as in default — penalties, forfeitures, "
            "withheld support. Pole-permitting and subsidy milestones sit on the same "
            "clock. Sunk plant plus a ten-year subsidy operating obligation is not a "
            "program you pause because the core is bleeding.",
            body,
        )
    )
    story.append(
        Paragraph(
            "<b>Need to be on:</b> raise take on plant already lit (38% → 54% is 221k "
            "“missing” customers on 1.385M passings) <i>or</i> stop treating leftover "
            "passings as the slope closer. Do not add rural miles to fix a core-product "
            "gap. Do not assume an exit that the subsidy contracts do not allow.",
            body,
        )
    )

    # --- Cause 3: market ---
    story.append(
        Paragraph(
            "The add engine assumed movers and video lock-in — both retired",
            h2,
        )
    )
    story.append(
        Paragraph(
            "Three structural shifts hit at once. They are the floor (Root A). They do "
            "<b>not</b> by themselves explain why Charter’s residential Internet "
            "net-loss rate is <b>1.8× Comcast’s</b> in Q1 (0.42% vs 0.23%; excess "
            "<b>54k</b>, rounded down). Industry weather plus a worse firm slope is "
            "the full story. Rate = |quarterly net adds| / beginning customers — "
            "<b>not gross churn</b> (not disclosed).",
            body,
        )
    )
    mkt_header = _header_row(["Market shift", "What broke", "Need to be on"], cell_h)
    mkt_rows = [
        mkt_header,
        [
            Paragraph("<b>Reduced moving</b>", cell),
            Paragraph(
                "10-K: ability to gain new customers “is dependent to some extent on "
                "growth in occupied housing.” Team Case Brief: a slow housing market "
                "means fewer people moving and signing up. The industry’s cheapest "
                "gross-add event was a truck at a new address. That event shrank.",
                cell,
            ),
            Paragraph(
                "A growth model that does not assume housing-driven gross adds return.",
                cell,
            ),
        ],
        [
            Paragraph("<b>Switching costs changed shape</b>", cell),
            Paragraph(
                "FWA lowered the cost of leaving (self-install box, no truck). Winning "
                "a non-mover got more expensive — displace an incumbent, do not greet "
                "a mover. Not a contradiction: fewer inbound events, easier outbound "
                "for attackers. Same carriers attacking broadband that Charter resells "
                "as an MVNO.",
                cell,
            ),
            Paragraph(
                "Price/promo and overlap GTM vs fiber and FWA, not vs last year’s mover.",
                cell,
            ),
        ],
        [
            Paragraph("<b>Reduced need for broadband TV</b>", cell),
            Paragraph(
                "Video is still large and structurally declining: FY2025 video revenue "
                "<b>−9.4%</b>; Q1 <b>−9.2%</b> and <b>−60k</b> customers (losses "
                "<i>moderating</i>, not reversing — RETRIEVED · Ex99.1). Programmer-app "
                "bundling manages the decline. Cord-cutting and vMVPDs removed the glue. "
                "Internet now has to win on its own.",
                cell,
            ),
            Paragraph(
                "Internet that wins standalone. Mobile deepens the bundle for some; "
                "it is lower-margin and the market will not credit it against broadband decline.",
                cell,
            ),
        ],
    ]
    story.append(_table(mkt_rows, [1.55 * inch, 3.55 * inch, 2.3 * inch]))
    story.append(
        Paragraph(
            "Sources: CHTR Ex99.1 · CMCSA Ex99.1 Q1 2026 · 10-K Item 1A housing language · "
            "Team Case Brief. Excess 54k is a net-loss-rate proxy vs Comcast, not a churn rate.",
            small,
        )
    )

    # --- Internal gap ---
    story.append(HRFlowable(width="100%", thickness=0.5, color=LINE))
    story.append(
        Paragraph(
            "Ops and marketing see −120k, not the rate or WHERE — they need a quarterly net-loss-by-category system",
            h2,
        )
    )
    story.append(
        Paragraph(
            "The three causes above are what the tape priced. They do not tell plant "
            "ops where to hold the line, or marketing which offer/segment is leaking. "
            "That is a <b>shared operations and/or marketing capability gap</b>, not a "
            "choice of which department owns the data (filings do not prove a single owner).",
            body,
        )
    )
    story.append(
        Paragraph(
            "<b>What they can see today.</b> Company-level net Internet adds: "
            "<b>−120k</b> in Q1 (RETRIEVED · Ex99.1). Rural CR <b>+41k</b> is a disclosed "
            "program add, not a residential-Internet loss tracker. The existing "
            "network-churn work therefore used a <b>net-loss rate</b> vs Comcast "
            "(1.8×; excess 54k) as a company-level proxy — and stated outright that "
            "<b>gross churn is unused because it is not disclosed</b>. We will not invent "
            "a filled-in breakdown they do not have. The cells below are empty on purpose. "
            "The system is the gap.",
            body,
        )
    )
    story.append(
        Paragraph(
            "<b>What they cannot see.</b> (a) The true churn <i>rate</i> — gross "
            "disconnects / beginning base — versus failed acquisition (gross adds "
            "collapsing). Net −120k is the residual of both. (b) The <i>division of "
            "where</i> they are losing: core vs rural; overlap vs rest of footprint; "
            "move-out vs competitive vs involuntary; tenure; product mix at leave. "
            "Call-center reason codes are not that tracker (instructor: agents have "
            "favorite codes — sample the disconnect, do not trust coded tickets). "
            "Working assumption, to confirm with the CEO rather than assert as fact: "
            "past customer data has not been tracked in a usable form.",
            body,
        )
    )

    trk_header = _header_row(["Category the system must cut", "Q1 2026 cell", "Tag"], cell_h)
    trk_rows = [
        trk_header,
        [
            Paragraph("Company residential Internet (only filled line)", cell),
            Paragraph("<b>−120k net</b>", cell),
            Paragraph("RETRIEVED · Ex99.1", cell),
        ],
        [
            Paragraph("Core vs rural", cell),
            Paragraph("Empty — rural +41k CR is not this cut", cell),
            Paragraph("not tracked", cell),
        ],
        [
            Paragraph(
                "Overlap vs rest of footprint (AT&amp;T ~27% / Verizon ~16% terrestrial 100 Mbps+)",
                cell,
            ),
            Paragraph("Empty", cell),
            Paragraph(
                "~27% / ~16% = footprint mix, RETRIEVED; <i>losses in those zips</i> = not tracked",
                cell,
            ),
        ],
        [
            Paragraph(
                "Reason: move-out vs competitive (FWA vs fiber) vs involuntary/nonpay",
                cell,
            ),
            Paragraph("Empty", cell),
            Paragraph("not tracked; not agent codes", cell),
        ],
        [
            Paragraph("Product mix at leave: Internet-only / +mobile / +video", cell),
            Paragraph("Empty", cell),
            Paragraph("not tracked", cell),
        ],
        [
            Paragraph("Tenure (if available)", cell),
            Paragraph("Empty", cell),
            Paragraph("not tracked", cell),
        ],
    ]
    story.append(
        _table(
            trk_rows,
            [3.15 * inch, 2.15 * inch, 2.1 * inch],
            extra_style=[
                ("BACKGROUND", (1, 2), (1, -1), EMPTY_BG),
            ],
        )
    )
    story.append(
        Paragraph(
            "Empty cells are empty on purpose — we will not invent a breakdown. "
            "Unit of the system: quarterly net loss, or gross adds vs disconnects if "
            "obtainable. Run every quarter. Only filled cell: CHTR Ex99.1 Q1 2026. "
            "Overlap shares are footprint mix, not a loss split.",
            small,
        )
    )

    # --- Four gaps ---
    story.append(
        Paragraph("GAP analyses — what they are on vs what they need to be on", h2)
    )
    story.append(
        Paragraph(
            "Four gaps. <b>G1 is the gate</b> — it blocks the other three. Dollar-weighted: "
            "G2 and G3 are where the cash sits ($11.7B capex, $8B+ rural). G4 is the "
            "demand regime. Effort should not migrate to refining NCTA capex tables "
            "(precise, available, low leverage) while the category tracker (high leverage, missing) stays unbuilt.",
            body,
        )
    )
    gap_header = _header_row(["ID", "Gap", "On today", "Need to be on"], cell_h)
    gap_rows = [
        gap_header,
        [
            Paragraph("<b>G1</b>", cell_r),
            Paragraph(
                "<b>Quarterly net-loss-by-category tracker</b> — shared ops/marketing insight system",
                cell,
            ),
            Paragraph(
                "Company-level net Internet adds only (−120k Q1). No churn rate. No standing "
                "division of where they lose. Working assumption (confirm with CEO): past "
                "customer data not tracked in a usable form.",
                cell,
            ),
            Paragraph(
                "A quarterly system whose unit is net loss (prefer: gross adds vs disconnects) "
                "cut by core vs rural; overlap (AT&amp;T ~27% / Verizon ~16%) vs rest; reason "
                "(move-out / FWA / fiber / nonpay, sampled from the disconnect); product mix "
                "at leave; tenure if available. Cells stay empty until the system exists.",
                cell,
            ),
        ],
        [
            Paragraph("<b>G2</b>", cell_r),
            Paragraph("<b>Capex productivity</b>", cell),
            Paragraph(
                "Intensity 21¢ per revenue dollar vs Comcast C&amp;P 11¢. Spend classified "
                "by NCTA bucket, not by Internet-add yield. Q1 spend up, Internet and FCF down.",
                cell,
            ),
            Paragraph(
                "$ of capex per net Internet add, by bucket (evolution / rural / CPE / other). "
                "A 2027 completion date is not a productivity metric.",
                cell,
            ),
        ],
        [
            Paragraph("<b>G3</b>", cell_r),
            Paragraph("<b>Rural as closer</b>", cell),
            Paragraph(
                "+41k CR / quarter, 38% take, 1.6% of revenue, remainder 120–170k lifetime "
                "stock vs a 179k <i>quarterly</i> peer gap. RDOF/BEAD make pause/exit costly.",
                cell,
            ),
            Paragraph(
                "Treat rural as a long-cycle infrastructure book. Close the core hole on the "
                "plant already built. Raise take on lit rural plant if that is cheaper than new miles.",
                cell,
            ),
        ],
        [
            Paragraph("<b>G4</b>", cell_r),
            Paragraph("<b>Market model</b>", cell),
            Paragraph(
                "Strategy still talks as if more plant + simpler bundles + video apps restore "
                "connectivity growth. Housing and video are named as risks, not as a retired add engine.",
                cell,
            ),
            Paragraph(
                "Gross-add plan for a low-mobility, FWA-easy-out, video-optional customer. "
                "Price/promo and overlap GTM vs fiber and FWA, not vs last year’s mover.",
                cell,
            ),
        ],
    ]
    story.append(
        _table(
            gap_rows,
            [0.45 * inch, 1.7 * inch, 2.6 * inch, 2.65 * inch],
            extra_style=[("BACKGROUND", (0, 1), (-1, 1), LIGHT_RED)],
        )
    )
    story.append(
        Paragraph(
            "<b>What would falsify “this is the gap.”</b> G1: the tracker already exists "
            "and is used quarterly — then skip “stand up tracking” and run mix control "
            "immediately. G2: mix-adjusted core Internet losses converge with Comcast "
            "while intensity stays high — then the spend <i>is</i> buying the print, just "
            "with lag. G3: remainder + take-rate lift closes the Comcast <i>quarterly</i> "
            "slope — the arithmetic already says it cannot. G4: housing turnover and "
            "video attach recover <i>and</i> Charter’s loss rate converges with Comcast without offer change.",
            small,
        )
    )

    # --- Next step ---
    story.append(
        Paragraph(
            "Next step — broadband churn analysis = stand up (or pull) the tracker",
            h2,
        )
    )
    story.append(
        Paragraph(
            "<b>Do this first.</b> Build or pull the category breakdown they do not have, "
            "so they can see the <b>rate</b> and the <b>division of losses</b>. Every later "
            "recommendation (cut rural, retarget capex, reprice vs FWA, change the overlap "
            "offer) needs to know whether Q1 was <i>failed acquisition</i> (housing / fewer "
            "movers), <i>failed retention</i> (competitive disconnects on the core), or both "
            "— and <i>where</i>. Company net adds cannot tell them apart.",
            body,
        )
    )
    story.append(Paragraph("<b>Why this is the gap</b>", body))
    why_items = [
        "Charter discloses <b>net</b> Internet adds. Gross adds and gross disconnects are not in the 10-K, 10-Q, or earnings release. There is no public churn <i>rate</i>.",
        "Field + customer-ops opex <b>fell $30M</b> YoY in Q1 while Internet losses doubled. That is evidence against a company-wide network-failure churn wave. It is <b>not</b> a substitute for a category tracker.",
        "Rural <b>+41k</b> is already inside the company <b>−163k</b> CR print. Without a standing core-vs-rural <i>Internet</i> cut, rural mix will keep looking like “the company almost held” when the core lost <b>204k</b> CR. That identity is a one-off reconstruction, not a quarterly system.",
        "Working assumption, to confirm with the client: <b>past customer data has not been tracked</b> in a form that supports this split. If that is wrong, the step collapses to turning the existing feed into the tracker, not building one from scratch.",
    ]
    for item in why_items:
        story.append(Paragraph(f"• {item}", bullet))

    out_header = _header_row(["Output the system must produce each quarter", "Why it decides something"], cell_h)
    out_rows = [
        out_header,
        [
            Paragraph(
                "Gross adds vs gross disconnects, 8 quarters, residential Internet — or net loss if gross is unavailable",
                cell,
            ),
            Paragraph(
                "Separates housing-add drought from retention failure; produces a rate, not only a net print",
                cell,
            ),
        ],
        [
            Paragraph("Disconnect mix: move-out / competitive (FWA vs fiber) / involuntary", cell),
            Paragraph("Tells GTM vs credit vs housing", cell),
        ],
        [
            Paragraph(
                "Core vs rural vs AT&amp;T-overlap (~27%) vs Verizon-overlap (~16%) vs rest of footprint",
                cell,
            ),
            Paragraph(
                "Tests whether Root B is an overlap-zip story; gives ops a plant cut and marketing a GTM cut",
                cell,
            ),
        ],
        [
            Paragraph("Tenure at disconnect (if available)", cell),
            Paragraph("New-customer quality vs long-life erosion", cell),
        ],
        [
            Paragraph("Product mix at leave (Internet-only / +mobile / +video)", cell),
            Paragraph("Tests whether video lock-in actually left, and whether mobile holds", cell),
        ],
    ]
    story.append(
        _table(
            out_rows,
            [3.7 * inch, 3.7 * inch],
            extra_style=[("BACKGROUND", (0, 1), (-1, -1), EMPTY_BG)],
        )
    )
    story.append(
        Paragraph(
            "Each line is a number — currently empty. Until those cells are filled, we "
            "will not claim a single “churn rate,” will not invent a where-they-lose mix, "
            "will not attribute the 54k excess to network quality, and will not recommend "
            "more upgrade/rebuild as a Q1 slope closer (already +71%).",
            small,
        )
    )

    # --- CEO question ---
    ceo_box = Table(
        [
            [
                Paragraph(
                    "<b>Ask the CEO one binary question</b> (cheap, can kill the “stand up tracking” work)<br/><br/>"
                    "<b>Will you stand up — or do you already have — a quarterly "
                    "net-loss-by-category tracker for residential Internet on the core: yes or no?</b><br/><br/>"
                    "The tracker’s unit is quarterly net loss (prefer gross adds vs disconnects). "
                    "Categories: core vs rural; overlap vs rest (AT&amp;T ~27% / Verizon ~16% "
                    "terrestrial 100 Mbps+); reason (move-out vs competitive FWA vs competitive "
                    "fiber vs involuntary/nonpay, sampled from the disconnect — not agent codes); "
                    "product mix at leave (Internet-only / +mobile / +video); tenure if available."
                    "<br/><br/>"
                    "<b>Yes</b> → send the last eight quarters (or stand it up and send Q1). "
                    "Churn analysis is a mix-control read, not a data build.<br/>"
                    "<b>No</b> → that is G1. The next step is to stand up the system and fill "
                    "the empty cells before we touch capex or rural as a course of action.",
                    callout,
                )
            ]
        ],
        colWidths=[cw],
    )
    ceo_box.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), LIGHT_BLUE),
                ("BOX", (0, 0), (-1, -1), 1, BLUE),
                ("LEFTPADDING", (0, 0), (-1, -1), 10),
                ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                ("TOPPADDING", (0, 0), (-1, -1), 10),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ]
        )
    )
    story.append(Spacer(1, 8))
    story.append(ceo_box)
    story.append(
        Paragraph(
            "Sequence (leverage ÷ cost): (1) the binary CEO question; (2) if no, stand up "
            "the system; (3) if yes, run mix control immediately and skip G1 build; "
            "(4) only after the first fill do capex-productivity (G2) and rural-take (G3) "
            "become decision-sized rather than narrative.",
            small,
        )
    )

    # --- Kill rule + unwilling ---
    kill = Paragraph(
        "<b>Kill rule</b> (written before a recommendation)<br/><br/>"
        "If a quarterly net-loss-by-category tracker <b>already exists</b> for residential "
        "Internet that cuts core vs rural, overlap vs rest, reason (move-out / competitive / "
        "nonpay — sampled, not agent codes), and product mix at leave, <b>do not</b> spend "
        "the step building tracking — go to mix control.<br/><br/>"
        "If that tracker, once in hand, shows <b>move-out as the single largest reason</b> "
        "and Charter’s <i>competitive</i> loss rate matches Comcast on the core, <b>kill</b> "
        "“Charter-specific product failure” as the Q1 story and treat housing + industry FWA "
        "as the floor (Root A). The CEO charge then has to be answered with a growth model "
        "that does not wait for movers, not with more rural miles.<br/><br/>"
        "If field + care opex stay down, losses stay up, <b>and</b> the sample does "
        "<b>not</b> name speed / WiFi / reliability as the largest reason on the core, "
        "<b>kill</b> “network performance caused the doubling.”",
        cell,
    )
    unwilling = Paragraph(
        "<b>Unwilling to claim</b><br/><br/>"
        "• Gross churn, a churn <i>rate</i>, or any filled category breakdown of where they "
        "lose — not disclosed; unused; we will not invent one.<br/><br/>"
        "• That housing alone explains Charter vs Comcast. Both firms face the mover drought; "
        "only Charter’s residential Internet net-loss rate doubled into 1.8× the peer.<br/><br/>"
        "• That rural NPV is zero. We have a low yield and a scale fail, not a full DCF.<br/><br/>"
        "• That RDOF/BEAD can be walked away from at book value. The 10-K names penalties, "
        "forfeitures, and withheld support.<br/><br/>"
        "• That the 2027 network-evolution date re-rates the stock without an Internet-print "
        "change (Root C).<br/><br/>"
        "• That mobile +368k or video losses “moderating” offset Internet −120k for the tape.<br/><br/>"
        "• That call-center reason codes are a breakdown. They are not.",
        cell,
    )
    ku = Table([[kill, unwilling]], colWidths=[3.7 * inch, 3.7 * inch])
    ku.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (0, 0), LIGHT),
                ("BACKGROUND", (1, 0), (1, 0), EMPTY_BG),
                ("BOX", (0, 0), (-1, -1), 0.5, LINE),
                ("INNERGRID", (0, 0), (-1, -1), 0.4, LINE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    story.append(Spacer(1, 10))
    story.append(ku)

    # --- DRAFT playbook (conditional; does not fire) ---
    story.append(Spacer(1, 12))
    story.append(HRFlowable(width="100%", thickness=0.8, color=INK))
    story.append(
        Paragraph(
            "DRAFT playbook — if lost to X, do Y (does not fire until tracker cells are filled)",
            h2,
        )
    )
    story.append(
        Paragraph(
            "We <b>can</b> propose a response for each leak once the quarterly "
            "net-loss-by-category tracker exists. We <b>will not</b> fire any of those "
            "responses until the cells are filled. This is a dormant map, not a mix we "
            "have measured. Company print remains −120k Internet; peer gap remains 1.8× / "
            "54k excess. No cell is the largest. Call-center codes are not the file that "
            "turns a branch on.",
            body,
        )
    )
    story.append(
        Paragraph(
            "<b>Material-leak gate.</b> A branch fires only if it is the largest — or a "
            "co-equal — cell in the first fill <b>and</b> closing Charter’s gap vs Comcast "
            "in that cell would absorb a material share of the 54k excess. Co-equal: fire "
            "the cheaper lever first. Two expensive levers do not fire in the same quarter. "
            "Company-wide upgrade/rebuild (already +71%) and more rural miles (remainder "
            "120–170k lifetime vs 179k quarterly peer gap) are not the default answer to "
            "any leak.",
            body,
        )
    )
    story.append(
        Paragraph(
            "Sequence: (0) CEO binary — tracker exist? (1) <b>Reason mix</b> first "
            "(move / FWA / fiber / nonpay, sampled disconnect) — MECE, decides housing vs "
            "GTM vs credit vs plant. (2) WHERE (core/rural; AT&amp;T ~27% / Verizon ~16% vs "
            "rest) targets the lever and can veto a mislabel. (3) WHO (mix at leave; tenure "
            "if available) sizes the offer. (4) Spend only after 1–3.",
            small,
        )
    )

    play_rows = [
        _header_row(
            ["If this is the material leak", "Do (X → Y, funded by Z, over N)", "Kill — wrong play if"],
            cell_h,
        ),
        [
            Paragraph("<b>Move-out</b>", cell),
            Paragraph(
                "Same-day transfer-of-service + MDU/landlord capture, targeting occupied-housing "
                "events, funded by sales-ops and by stopping retention promo on vacated addresses, "
                "6 months. Not more plant.",
                cell,
            ),
            Paragraph(
                "Move-out rate matches Comcast and competitive disconnects still produce 1.8× → "
                "housing is the floor (Root A); grow without waiting for movers.",
                cell,
            ),
        ],
        [
            Paragraph("<b>Competitive FWA</b>", cell),
            Paragraph(
                "12-month Internet rate-lock / FWA-match + self-install WiFi, Internet-only / "
                "price-sensitive, on <i>and</i> off overlap (FWA is wireless-nationwide). Test "
                "2 quarters. Funded by not adding remainder rural miles (~$1.9B) or by video "
                "promo — not by upgrade/rebuild.",
                cell,
            ),
            Paragraph(
                "Sample names speed, not price — especially on the 27%/16% plant → FWA was the "
                "vehicle, fiber is the competitor. On-overlap FWA may be a fiber stepping-stone: "
                "do not FWA-match.",
                cell,
            ),
        ],
        [
            Paragraph("<b>Competitive fiber</b>", cell),
            Paragraph(
                "Overlap-zip GTM: gig/symmetry save targeting AT&amp;T ~27% / Verizon ~16% zips, "
                "Internet-only first, 2–4 quarters. Nodes only in those zips and only if the "
                "sample names speed. Funded by redirecting a slice of +$280M YoY upgrade/rebuild "
                "($675M vs $395M) off non-overlap plant. Do not wait for end-2027.",
                cell,
            ),
            Paragraph(
                "Losses follow footprint (proportional) → overlap is not Root B. Field+care stay "
                "down and sample does not name speed → offer, not nodes. Fiber-labeled loss "
                "off-overlap is a mislabel.",
                cell,
            ),
        ],
        [
            Paragraph("<b>Involuntary / nonpay</b>", cell),
            Paragraph(
                "Payment arrangement before disconnect, origination screen on new tenure, 90-day "
                "first-bill save, new-tenure Internet-only, 2 quarters. Funded by restoring a "
                "slice of the $30M field+care opex decline. Not from capex.",
                cell,
            ),
            Paragraph(
                "Nonpay concentrated on rural new-connects (38% take) → origination quality, not "
                "a core reprice.",
                cell,
            ),
        ],
        [
            Paragraph("<b>WHERE: core</b>", cell),
            Paragraph(
                "Fire the reason play on the core. Do not add rural miles. CR identity already "
                "says core −204k vs rural +41k — not the Internet tracker.",
                cell,
            ),
            Paragraph(
                "Core Internet rate already matches Comcast. Remainder 120–170k lifetime cannot "
                "close a 179k quarterly peer gap.",
                cell,
            ),
        ],
        [
            Paragraph("<b>WHERE: rural</b>", cell),
            Paragraph(
                "Raise take on lit plant (38% → 54% = 221k missing on 1.385M), 4–8 quarters. "
                "Do not pause RDOF/BEAD. Stop remainder miles if take stays stuck.",
                cell,
            ),
            Paragraph(
                "Rural CR is already the only disclosed positive CR channel. More rural miles "
                "is almost never the response to core competitive loss.",
                cell,
            ),
        ],
        [
            Paragraph("<b>WHERE: overlap vs rest</b>", cell),
            Paragraph(
                "Overlap material: concentrate the reason play on those zips (fiber GTM or "
                "FWA-as-stepping-stone). Rest material: fiber is the wrong play — hand to FWA / "
                "move-out / nonpay.",
                cell,
            ),
            Paragraph(
                "Do not fire on the 10-K 27%/16% footprint shares alone (not a loss split). "
                "Union unknown.",
                cell,
            ),
        ],
        [
            Paragraph("<b>WHO: mix / tenure</b>", cell),
            Paragraph(
                "Internet-only: save on price/WiFi, not video reattach (video $ −9.4% FY25). "
                "+mobile at leave: bundle did not hold; do not scale mobile as the Internet "
                "closer (Root C). New tenure: 90-day onboarding; cut CPE +41% if adds are low "
                "quality. Long-life: overlay onto FWA or fiber save, not a welcome kit.",
                cell,
            ),
            Paragraph(
                "Mobile +368k does not offset Internet −120k for the tape. New-tenure rate "
                "matching Comcast → tightening origination worsens the gross-add drought. "
                "Tenure only if available.",
                cell,
            ),
        ],
    ]
    story.append(
        _table(
            play_rows,
            [1.45 * inch, 3.15 * inch, 2.8 * inch],
            extra_style=[
                ("BACKGROUND", (0, 1), (0, 4), LIGHT_RED),
                ("BACKGROUND", (0, 5), (0, 7), EMPTY_BG),
            ],
        )
    )
    story.append(
        Paragraph(
            "Funding pools (grounded; intensity already 21¢ vs Comcast C&amp;P 11¢): "
            "<b>P1</b> upgrade/rebuild increment +$280M — overlap nodes only if fiber + "
            "speed-named sample. <b>P2</b> rural remainder ~$1.9B avoided — not new rural "
            "miles as a core-churn response. <b>P3</b> field+care −$30M — restore if nonpay. "
            "<b>P4</b> CPE +41% — cut if new-tenure quality. Do not fund from “more plant.”",
            small,
        )
    )
    story.append(
        Paragraph(
            "<b>Playbook kill / unwilling.</b> Do not fire two of {FWA price-match, overlap "
            "rebuild, collections restore, mover MDU} in the same quarter. Do not treat "
            "call-center codes as the trigger. Unwilling: which X is largest; any filled "
            "percentage; that a named response is the Q1 course of action; that the 54k "
            "excess sits in any one cell; that more plant, more rural miles, or more mobile "
            "closes the Internet print.",
            small,
        )
    )

    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=0.5, color=LINE))
    story.append(
        Paragraph(
            "Sources: Team Case Brief (stock path); CHTR Ex99.1 Q1 2026 / FY2025 10-K / "
            "trending (CORE-INFORMATION); CMCSA Ex99.1 Q1 2026; existing conversion and "
            "capex work in Analysis/chtr-rural-core-conversion, Analysis/chtr-cmcsa-capex, "
            "Analysis/chtr-network-churn. Working document: Decisions/decisions.md. "
            "Playbook companion canvas: chtr-churn-response-playbook. "
            "Arithmetic already recomputed in those files and Decision Planning/network_churn_model.py. "
            "Draft work-plan. Conditional playbook — not a recommendation that has fired. "
            "MAN6930 · Q1 2026 anchor.",
            small,
        )
    )

    doc.build(story)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    build()
