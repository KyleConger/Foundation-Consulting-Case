"""
Render Charter relative-performance canvas content to PDF.
Mirrors canvases/chtr-relative-performance.canvas.tsx data.
"""
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    HRFlowable,
    KeepTogether,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

OUT = Path(r"c:\Users\Owner\Desktop\MAN6930 Case\Decisions\CHTR-Relative-Performance.pdf")

# Palette (flat, print-friendly)
RED = colors.HexColor("#C44B4B")
ORANGE = colors.HexColor("#C47A2B")
GREEN = colors.HexColor("#2F7D4F")
BLUE = colors.HexColor("#2E6FA8")
GRAY = colors.HexColor("#666666")
LIGHT = colors.HexColor("#F4F4F4")
LINE = colors.HexColor("#DDDDDD")
INK = colors.HexColor("#1A1A1A")


def signed_bars(data_rows, categories, series_meta, width=460, height=150, y_min=None, y_max=None):
    """
    data_rows: list of series, each a list of numbers aligned to categories
    series_meta: list of (name, color)
    Returns a flowable Drawing via reportlab.graphics
    """
    from reportlab.graphics.shapes import Drawing, Line, Rect, String

    all_vals = [v for row in data_rows for v in row]
    lo = y_min if y_min is not None else min(0, min(all_vals)) * 1.1
    hi = y_max if y_max is not None else max(0, max(all_vals)) * 1.1
    if hi == lo:
        hi = lo + 1
    span = hi - lo

    d = Drawing(width, height)
    pad_l, pad_r, pad_t, pad_b = 48, 12, 12, 36
    inner_w = width - pad_l - pad_r
    inner_h = height - pad_t - pad_b

    def y_scale(v):
        return pad_b + ((v - lo) / span) * inner_h

    zero_y = y_scale(0)
    # zero line
    d.add(Line(pad_l, zero_y, width - pad_r, zero_y, strokeColor=GRAY, strokeWidth=1))
    d.add(String(4, zero_y - 3, "0", fontSize=7, fillColor=GRAY))

    n_cat = len(categories)
    n_ser = len(data_rows)
    group_w = inner_w / n_cat
    bar_w = min(16, (group_w * 0.7) / max(n_ser, 1))

    for ci, cat in enumerate(categories):
        gx = pad_l + ci * group_w + group_w / 2
        for si, row in enumerate(data_rows):
            v = row[ci]
            y0 = zero_y
            y1 = y_scale(v)
            top = min(y0, y1)
            h = max(1.5, abs(y1 - y0))
            x = gx - (n_ser * bar_w + (n_ser - 1) * 3) / 2 + si * (bar_w + 3)
            d.add(Rect(x, top, bar_w, h, fillColor=series_meta[si][1], strokeColor=None))
        # category label (truncate)
        label = cat if len(cat) <= 12 else cat[:11] + "…"
        d.add(String(gx - 18, 8, label, fontSize=6.5, fillColor=GRAY))

    # legend
    lx = pad_l
    for name, col in series_meta:
        d.add(Rect(lx, height - 10, 8, 8, fillColor=col, strokeColor=None))
        d.add(String(lx + 11, height - 9, name, fontSize=7, fillColor=INK))
        lx += 8 + 6 + min(120, len(name) * 4.2) + 10

    return d


def build():
    styles = getSampleStyleSheet()
    title = ParagraphStyle(
        "Title2",
        parent=styles["Heading1"],
        fontSize=16,
        textColor=INK,
        spaceAfter=6,
        leading=20,
    )
    h2 = ParagraphStyle(
        "H2",
        parent=styles["Heading2"],
        fontSize=11,
        textColor=INK,
        spaceBefore=12,
        spaceAfter=4,
        leading=14,
    )
    body = ParagraphStyle(
        "Body2",
        parent=styles["Normal"],
        fontSize=8.5,
        textColor=INK,
        leading=11,
        spaceAfter=4,
    )
    small = ParagraphStyle(
        "Small",
        parent=styles["Normal"],
        fontSize=7,
        textColor=GRAY,
        leading=9,
        spaceAfter=4,
    )
    gap = ParagraphStyle(
        "Gap",
        parent=styles["Normal"],
        fontSize=8,
        textColor=INK,
        leading=10,
        alignment=TA_CENTER,
    )

    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=letter,
        leftMargin=0.6 * inch,
        rightMargin=0.6 * inch,
        topMargin=0.5 * inch,
        bottomMargin=0.5 * inch,
        title="Charter Relative Performance vs Market",
        author="MAN6930 Analysis",
    )
    story = []

    story.append(Paragraph("Charter vs the market — where we stand", title))
    story.append(
        Paragraph(
            "Relative performance vs cable peer (Comcast / CMCSA) and broadband attackers. "
            "Gaps signed vs CMCSA: negative = Charter worse; positive = Charter ahead. "
            "Q1 2026 anchor; Q2 labeled later public fact. Recreated from the Cursor canvas "
            "(canvases do not export to PDF natively).",
            body,
        )
    )
    story.append(
        Paragraph(
            "Definition note: CHTR = total Internet; CMCSA = domestic residential broadband. "
            "Mobile = Spectrum Mobile vs CMCSA domestic wireless. 1Y/5Y stock returns ≈ secondary screeners — verify before pitching.",
            small,
        )
    )
    story.append(Spacer(1, 6))
    story.append(HRFlowable(width="100%", thickness=0.5, color=LINE))

    # Gap at a glance — 2x4 table of big numbers
    story.append(Paragraph("Gap at a glance (vs CMCSA)", h2))
    glance = [
        [
            Paragraph("<b>−55k</b><br/>Q1 BB: 55k more losses (1.8×)", gap),
            Paragraph("<b>−179k</b><br/>Q1 BB YoY slope swing", gap),
            Paragraph("<b>−67k</b><br/>Q1 mobile: −15% fewer adds", gap),
            Paragraph("<b>+262k</b><br/>Q1 video: fewer losses", gap),
        ],
        [
            Paragraph("<b>−12.6ppt</b><br/>Apr 24 tape (~2.0×)", gap),
            Paragraph("<b>−22ppt</b><br/>≈1Y return gap", gap),
            Paragraph("<b>−30ppt</b><br/>≈5Y return gap", gap),
            Paragraph("<b>+3.8ppt</b><br/>Internet/$ BB YoY", gap),
        ],
    ]
    gt = Table(glance, colWidths=[115, 115, 115, 115])
    gt.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), LIGHT),
                ("BOX", (0, 0), (-1, -1), 0.5, LINE),
                ("INNERGRID", (0, 0), (-1, -1), 0.4, LINE),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    story.append(gt)
    story.append(Spacer(1, 8))

    # Scorecard
    story.append(Paragraph("Gap scorecard", h2))
    score_header = ["Area", "CHTR", "CMCSA", "Gap (CHTR − peer)", "Read"]
    score_rows = [
        score_header,
        ["Broadband adds Q1’26", "−120k", "−65k", "−55k (1.8×)", "Worse"],
        ["Broadband YoY Δ Q1", "−61k", "+118k", "−179k swing", "Worse"],
        ["Mobile adds Q1’26", "+368k", "+435k", "−67k (−15%)", "Close / behind"],
        ["Video adds Q1’26", "−60k", "−322k", "+262k", "Ahead"],
        ["Internet / dom. BB $ YoY", "−1.3%", "−5.1%", "+3.8ppt", "Ahead on $"],
        ["Adj. EBITDA YoY*", "−2.2%", "−6.0%", "+3.8ppt", "Less down"],
        ["Apr 24 close-to-close", "−25.5%", "−12.9%", "−12.6ppt (~2×)", "Worse"],
        ["≈1Y total return", "−46%", "−24%", "−22ppt", "Worse"],
        ["≈5Y total return", "−82%", "−52%", "−30ppt", "Worse"],
    ]
    st = Table(score_rows, colWidths=[130, 70, 70, 100, 70])
    st_style = [
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2A2A2A")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 7.5),
        ("GRID", (0, 0), (-1, -1), 0.4, LINE),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("ALIGN", (1, 1), (-1, -1), "RIGHT"),
        ("ALIGN", (0, 0), (0, -1), "LEFT"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, LIGHT]),
    ]
    # tint worse/ahead rows
    for i, read in enumerate(
        ["Worse", "Worse", "Close / behind", "Ahead", "Ahead on $", "Less down", "Worse", "Worse", "Worse"],
        start=1,
    ):
        if "Worse" in read:
            st_style.append(("TEXTCOLOR", (3, i), (4, i), RED))
        elif "Ahead" in read or "Less" in read:
            st_style.append(("TEXTCOLOR", (3, i), (4, i), GREEN))
        else:
            st_style.append(("TEXTCOLOR", (3, i), (4, i), ORANGE))
    st.setStyle(TableStyle(st_style))
    story.append(st)
    story.append(
        Paragraph(
            "*CHTR consolidated Adj. EBITDA vs CMCSA Resid. C&P Adj. EBITDA. Sources: Ex99.1 Q1–Q2 2026; Yahoo; secondary 1Y/5Y screens.",
            small,
        )
    )

    # Chart 1 broadband
    story.append(Paragraph("1. Broadband net adds — Q1 gap −55k · 1.8× peer losses", h2))
    story.append(
        signed_bars(
            [[-59, -120, -116, -172], [-183, -65, -201, -167]],
            ["Q1’25", "Q1’26", "Q2’25", "Q2’26"],
            [("CHTR Internet (000s)", RED), ("CMCSA resid. BB (000s)", ORANGE)],
            y_min=-220,
            y_max=40,
        )
    )

    story.append(Paragraph("2. YoY Δ broadband — Q1 slope gap −179k", h2))
    story.append(
        signed_bars(
            [[-61, -56], [118, 34]],
            ["Q1 YoY Δ", "Q2 YoY Δ"],
            [("CHTR", RED), ("CMCSA", GREEN)],
            y_min=-80,
            y_max=140,
        )
    )

    story.append(Paragraph("3. Mobile net adds — Q1 gap −67k (−15%)", h2))
    story.append(
        signed_bars(
            [[507, 368, 406], [323, 435, 448]],
            ["Q1’25", "Q1’26", "Q2’26"],
            [("CHTR mobile", BLUE), ("CMCSA wireless", GREEN)],
            y_min=0,
            y_max=500,
        )
    )

    story.append(Paragraph("4. Video net adds — Q1 gap +262k fewer losses", h2))
    story.append(
        signed_bars(
            [[-181, -60, -21], [-427, -322, -280]],
            ["Q1’25", "Q1’26", "Q2’26"],
            [("CHTR video", BLUE), ("CMCSA video", ORANGE)],
            y_min=-460,
            y_max=40,
        )
    )

    story.append(Paragraph("5. Cable-like dollars YoY % (Q1) — BB $ / EBITDA +3.8ppt", h2))
    story.append(
        signed_bars(
            [[-1.3, 15.1, -2.2, -1.0], [-5.1, 15.0, -6.0, -1.9]],
            ["BB $", "Mobile $", "EBITDA", "Resid rev"],
            [("CHTR %", RED), ("CMCSA %", ORANGE)],
            y_min=-8,
            y_max=18,
        )
    )

    story.append(Paragraph("6. Attackers — Q1 2026 net adds (000s)", h2))
    story.append(
        signed_bars(
            [[-120, -65, 214, 470]],
            ["CHTR", "CMCSA", "VZ FWA", "TMUS≈"],
            [("Net adds (000s)", BLUE)],
            y_min=-150,
            y_max=520,
        )
    )

    # Stock section
    story.append(Paragraph("7. Stock price — absolute and vs peer", h2))
    story.append(
        Paragraph(
            "CHTR close Apr 24 2026: <b>$180.13</b> · CMCSA: <b>$27.56</b> · same-day return gap <b>−12.6ppt</b> (~2.0×).",
            body,
        )
    )
    story.append(Paragraph("7a. Returns by horizon", h2))
    story.append(
        signed_bars(
            [[-25.5, -46, -82], [-12.9, -24, -52]],
            ["Apr 24 day", "≈1Y", "≈5Y"],
            [("CHTR %", RED), ("CMCSA %", ORANGE)],
            y_min=-90,
            y_max=5,
        )
    )
    story.append(Paragraph("7b. Excess drawdown vs peer (CHTR − CMCSA, ppt)", h2))
    story.append(
        signed_bars(
            [[-12.6, -22, -30]],
            ["Apr 24", "≈1Y", "≈5Y"],
            [("Extra underperformance (ppt)", RED)],
            y_min=-35,
            y_max=5,
        )
    )
    story.append(Paragraph("7c. CHTR absolute close on earnings dates ($)", h2))
    story.append(
        signed_bars(
            [[345.49, 373.65, 309.75, 233.84, 206.12, 180.13, 123.31]],
            ["1/31/25", "4/25/25", "7/25/25", "10/31/25", "1/30/26", "4/24/26", "7/24/26"],
            [("CHTR close ($)", RED)],
            y_min=0,
            y_max=400,
        )
    )
    story.append(
        Paragraph(
            "From Apr 25’25 peak close ($373.65) to Jul 24’26 ($123.31) ≈ −67% on this earnings-date path.",
            small,
        )
    )

    stock_tbl = Table(
        [
            ["Horizon", "CHTR", "CMCSA", "Gap", "× peer drop"],
            ["Apr 24 2026 day", "−25.5%", "−12.9%", "−12.6ppt", "2.0×"],
            ["≈1 year", "−46%", "−24%", "−22ppt", "1.9×"],
            ["≈5 years", "−82%", "−52%", "−30ppt", "1.6×"],
        ],
        colWidths=[110, 80, 80, 90, 80],
    )
    stock_tbl.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2A2A2A")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
                ("GRID", (0, 0), (-1, -1), 0.4, LINE),
                ("ALIGN", (1, 0), (-1, -1), "RIGHT"),
                ("TEXTCOLOR", (1, 1), (-1, -1), RED),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    story.append(Spacer(1, 6))
    story.append(stock_tbl)

    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=0.5, color=LINE))
    story.append(
        Paragraph(
            "<b>Glance takeaway:</b> Worst gaps — broadband YoY slope (−179k swing) and stock "
            "(−12.6ppt day / −22ppt 1Y / −30ppt 5Y). Best gaps — video (+262k) and Internet $ YoY "
            "(+3.8ppt). Mobile close (−15%). Relative underperformance concentrates in Internet "
            "trajectory and equity, not every operating line.",
            body,
        )
    )
    story.append(
        Paragraph(
            "Source canvas: chtr-relative-performance.canvas.tsx · MAN6930 · Analysis PDF recreation",
            small,
        )
    )

    doc.build(story)
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    build()
