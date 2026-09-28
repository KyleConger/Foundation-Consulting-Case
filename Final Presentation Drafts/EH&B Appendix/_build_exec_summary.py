# -*- coding: utf-8 -*-
"""Appendix slides from EH&B Executive Summary only. Does not touch the final deck."""
from __future__ import annotations

from pathlib import Path

from lxml import etree
from openpyxl import load_workbook
from pptx import Presentation
from pptx.chart.data import CategoryChartData
from pptx.dml.color import RGBColor
from pptx.enum.chart import XL_CHART_TYPE
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Emu, Inches, Pt

# Match the final deck's exact EMUs (13.333... in × 7.5 in) without opening that file.
SLIDE_W = 12192000
SLIDE_H = 6858000

ROOT = Path(r"c:\Users\Owner\Desktop\MAN6930 Case")
XLSX = ROOT / "Decisions" / "EH&B" / "MASTER.xlsx"
OUT = ROOT / "Final Presentation Drafts" / "EH&B Appendix" / "06 EH&B Executive Summary.pptx"

NAVY = RGBColor(0x0B, 0x1F, 0x3A)
BLUE = RGBColor(0x00, 0x72, 0xCE)
RED = RGBColor(0xC8, 0x10, 0x2E)
GRAY = RGBColor(0x5B, 0x66, 0x72)
MUTED = RGBColor(0x8A, 0x94, 0xA0)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
PALE = RGBColor(0xDC, 0xE9, 0xF7)
PANEL = RGBColor(0xF2, 0xF6, 0xFB)
LINE = RGBColor(0xD7, 0xE0, 0xEA)
BAR_GRAY = "C5CDD6"
BAR_RED = "C8102E"

FOOTER = (
    "Final Presentation  ·  “Changing the Trajectory”  ·  "
    "Charter Communications (CHTR)  ·  Anchored to Q1 2026; "
    "Q2 2026 labeled as later public fact where used"
)
MINUS = "\u2212"


def load_numbers():
    wb = load_workbook(XLSX, data_only=True)
    ws = wb["Executive Summary"]

    def row_map(header_row):
        out = {}
        r = header_row + 1
        while r <= ws.max_row and ws.cell(r, 1).value not in (None, ""):
            out[ws.cell(r, 1).value] = [ws.cell(r, c).value for c in range(1, 7)]
            r += 1
        return out

    # Tables are separated by exactly three blank rows. Locate by title.
    titles = {}
    for r in range(1, ws.max_row + 1):
        v = ws.cell(r, 1).value
        if v in {
            "Critical values",
            "Mix",
            "Rate vs volume",
            "Plant and leverage",
            "Play fit",
            "Do not claim",
        }:
            titles[v] = r

    crit = row_map(titles["Critical values"])
    mix_header = titles["Mix"] + 1
    mix = []
    r = mix_header + 1
    while ws.cell(r, 1).value and not str(ws.cell(r, 1).value).startswith("Sum"):
        mix.append(
            {
                "line": ws.cell(r, 1).value,
                "dollars": ws.cell(r, 2).value,
                "share": ws.cell(r, 3).value,
                "role": ws.cell(r, 4).value,
            }
        )
        r += 1
    rate = row_map(titles["Rate vs volume"])
    plant = row_map(titles["Plant and leverage"])
    return crit, mix, rate, plant


def assert_lock(crit, mix, rate, plant):
    company = crit["Company revenue"][1]
    internet = crit["Internet revenue"][1]
    prior = crit["Internet revenue, prior year"][1]
    change = crit["Internet revenue change"][1]
    share = crit["Internet share of revenue"][1]
    res_adds = crit["Residential Internet net additions (000s)"][1]
    vol = crit["Volume, printed bridge"][1]
    rate_mix = crit["Rate and product mix, printed bridge"][1]
    assert company == 13597
    assert internet == 5852
    assert prior == 5930
    assert change == -78
    assert abs(share - (5852 / 13597)) < 1e-4
    assert res_adds == -117
    assert vol == -87 and rate_mix == 9
    assert vol + rate_mix == change == -78

    dollars = [m["dollars"] for m in mix]
    assert sum(dollars) == 13597
    assert mix[0]["line"] == "Internet" and mix[0]["role"] == "Accent"
    for m in mix:
        assert abs(m["share"] - m["dollars"] / 13597) < 1e-12

    p_vol = rate["Printed volume"][1]
    p_rate = rate["Printed rate and mix"][1]
    p_net = rate["Printed net"][1]
    assert (p_vol, p_rate, p_net) == (-87, 9, -78)
    d_vol = rate["Derived volume, unrounded $ millions"][1]
    d_rate = rate["Derived rate, unrounded $ millions"][1]
    assert abs(d_vol - (-89.77630192990912)) < 1e-6
    assert abs(d_rate - 11.77630192990957) < 1e-6
    # Round-half-away is not used. Standard half-up of these values is -90 and +12.
    assert round(d_vol) == -90 and round(d_rate) == 12
    assert rate["FY2025 rate and mix"][1] == 785
    assert rate["FY2025 volume"][1] == -380
    assert rate["FY2025 net"][1] == 405
    assert rate["FY2025 customer change"][1] == -393000

    assert plant["Company customer-relationship penetration"][1] == 0.54
    assert plant["Estimated passings (000s)"][1] == 58661
    assert plant["Rural penetration of activated passings"][1] == 0.381
    assert plant["Rural passings (000s)"][1] == 1385
    assert plant["Rural customer relationships (000s)"][1] == 527
    assert abs(31683 / 58661 - 0.54) < 0.0002
    # 527 / 1,385 = 38.0505%, which the filings and the sheet print as 38.1%.
    assert plant["Rural penetration of activated passings"][1] == 0.381
    assert round(527 / 1385 * 100, 1) == 38.1
    assert plant["Subsidized rural construction spend ($ billions)"][1] == 7.7
    assert plant["Principal amount of debt ($ billions)"][1] == 93.8
    assert plant["Net leverage (times Adjusted EBITDA)"][1] == 4.18
    assert plant["Contribution per incremental Internet PSU"][2] in (None, "—", "-")
    # Column C is the period; the value cell is column B, which is blank.
    assert plant["Contribution per incremental Internet PSU"][1] in (None, "—", "-")
    assert plant["Consumer acquisition cost"][1] in (None, "—", "-")

    return {
        "company": company,
        "internet": internet,
        "prior": prior,
        "change": change,
        "res_adds_000s": res_adds,
        "vol": vol,
        "rate": rate_mix,
        "d_vol": d_vol,
        "d_rate": d_rate,
        "arpu_26": rate["Derived implied rate Q1 2026"][1],
        "arpu_25": rate["Derived implied rate Q1 2025"][1],
        "mix": mix,
        "fy_rate": 785,
        "fy_vol": -380,
        "fy_net": 405,
        "fy_cust": -393000,
        "pen": 0.54,
        "passings": 58661,
        "rels": 31683,
        "rural_pen": 0.381,
        "rural_pass": 1385,
        "rural_rels": 527,
        "spend": 7.7,
        "principal": 93.8,
        "leverage": 4.18,
        "q2_pen": plant["Q2 penetration"][1],
        "q2_pass": plant["Q2 estimated passings (000s)"][1],
    }


def _body(tf, anchor):
    tf.word_wrap = True
    body = tf._txBody.find(qn("a:bodyPr"))
    body.set("lIns", "0")
    body.set("tIns", "0")
    body.set("rIns", "0")
    body.set("bIns", "0")
    body.set("anchor", anchor)
    return body


def _run(p, text, size, bold, italic, color, spacing=None):
    run = p.add_run()
    run.text = text
    run.font.name = "Calibri"
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    rPr = run._r.get_or_add_rPr()
    for tag in ("a:latin", "a:ea", "a:cs"):
        el = rPr.find(qn(tag))
        if el is None:
            el = etree.SubElement(rPr, qn(tag))
        el.set("typeface", "Calibri")
    if spacing is not None:
        rPr.set("spc", str(spacing))
        rPr.set("kern", "0")
    return run


def _ppr(p, align=None, after=0):
    pPr = p._p.get_or_add_pPr()
    if pPr.find(qn("a:buNone")) is None:
        etree.SubElement(pPr, qn("a:buNone"))
    if align is not None:
        p.alignment = align
    if after:
        p.space_after = Pt(after)
    return pPr


def add_text(slide, l, t, w, h, paragraphs, anchor="t"):
    """paragraphs: list of (text, size, bold, italic, color, spacing|None, align|None)."""
    box = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tf = box.text_frame
    _body(tf, anchor)
    for i, spec in enumerate(paragraphs):
        text, size, bold, italic, color = spec[:5]
        spacing = spec[5] if len(spec) > 5 else None
        align = spec[6] if len(spec) > 6 else None
        after = spec[7] if len(spec) > 7 else 0
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        _ppr(p, align, after)
        _run(p, text, size, bold, italic, color, spacing)
    return box


def add_runs(slide, l, t, w, h, lines, anchor="t"):
    """lines: list of list of (text, size, bold, italic, color)."""
    box = slide.shapes.add_textbox(Inches(l), Inches(t), Inches(w), Inches(h))
    tf = box.text_frame
    _body(tf, anchor)
    for i, runs in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        _ppr(p)
        for spec in runs:
            _run(p, *spec)
    return box


def card(slide, l, t, w, h, fill):
    sh = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(l), Inches(t), Inches(w), Inches(h)
    )
    sh.adjustments[0] = 0.08
    sh.fill.solid()
    sh.fill.fore_color.rgb = fill
    sh.line.color.rgb = LINE
    sh.line.width = Emu(12700)
    # No shadow.
    spPr = sh._element.find(qn("p:spPr"))
    effect = spPr.find(qn("a:effectLst"))
    if effect is not None:
        spPr.remove(effect)
    return sh


def chrome(slide, eyebrow, title, source, page):
    add_text(
        slide,
        0.55,
        0.28,
        12.2,
        0.30,
        [(eyebrow, 11, True, False, BLUE, 200)],
        anchor="ctr",
    )
    add_text(
        slide,
        0.55,
        0.58,
        12.25,
        1.05,
        [(title, 22, True, False, NAVY, None)],
        anchor="t",
    )
    add_text(
        slide,
        0.55,
        6.48,
        12.2,
        0.48,
        [(source, 9, False, True, MUTED, None)],
        anchor="t",
    )
    add_text(
        slide,
        0.55,
        7.05,
        11.9,
        0.30,
        [(FOOTER, 9, False, False, MUTED, None)],
        anchor="ctr",
    )
    add_text(
        slide,
        12.45,
        7.05,
        0.70,
        0.30,
        [(page, 10, False, False, MUTED, None, PP_ALIGN.RIGHT)],
        anchor="ctr",
    )


def _set_solid(spPr_parent, hex_color):
    # Remove existing solid fill then set.
    existing = spPr_parent.find(qn("a:solidFill"))
    if existing is not None:
        spPr_parent.remove(existing)
    sf = etree.Element(qn("a:solidFill"))
    srgb = etree.SubElement(sf, qn("a:srgbClr"))
    srgb.set("val", hex_color)
    # Insert fill before line if present, else append.
    ln = spPr_parent.find(qn("a:ln"))
    if ln is not None:
        ln.addprevious(sf)
    else:
        spPr_parent.append(sf)


def style_series(series, hex_color, num_fmt):
    ser = series._element
    spPr = ser.find(qn("c:spPr"))
    if spPr is None:
        spPr = etree.SubElement(ser, qn("c:spPr"))
    _set_solid(spPr, hex_color)
    ln = spPr.find(qn("a:ln"))
    if ln is None:
        ln = etree.SubElement(spPr, qn("a:ln"))
    ln.set("w", "0")
    noFill = ln.find(qn("a:noFill"))
    if noFill is None:
        # clear solid line
        for child in list(ln):
            ln.remove(child)
        etree.SubElement(ln, qn("a:noFill"))

    dLbls = ser.find(qn("c:dLbls"))
    if dLbls is None:
        dLbls = etree.SubElement(ser, qn("c:dLbls"))
    def set_el(tag, **attrs):
        el = dLbls.find(qn(tag))
        if el is None:
            el = etree.SubElement(dLbls, qn(tag))
        for k, v in attrs.items():
            el.set(k, v)
        return el

    set_el("c:numFmt", formatCode=num_fmt, sourceLinked="0")
    set_el("c:dLblPos", val="outEnd")
    set_el("c:showLegendKey", val="0")
    set_el("c:showVal", val="1")
    set_el("c:showCatName", val="0")
    set_el("c:showSerName", val="0")
    set_el("c:showPercent", val="0")
    txPr = dLbls.find(qn("c:txPr"))
    if txPr is not None:
        dLbls.remove(txPr)
    txPr = etree.SubElement(dLbls, qn("c:txPr"))
    etree.SubElement(txPr, qn("a:bodyPr"))
    etree.SubElement(txPr, qn("a:lstStyle"))
    p = etree.SubElement(txPr, qn("a:p"))
    pPr = etree.SubElement(p, qn("a:pPr"))
    defRPr = etree.SubElement(pPr, qn("a:defRPr"))
    defRPr.set("sz", "1100")
    defRPr.set("b", "1")
    sf = etree.SubElement(defRPr, qn("a:solidFill"))
    c = etree.SubElement(sf, qn("a:srgbClr"))
    c.set("val", "0B1F3A")
    latin = etree.SubElement(defRPr, qn("a:latin"))
    latin.set("typeface", "Calibri")


def style_chart(chart, y_min, y_max, axis_fmt, reverse_cats=True):
    chart.has_legend = False
    chart.has_title = False
    plot = chart.plots[0]
    plot.gap_width = 50

    chart_el = chart._element
    # grouping stacked is already set by chart type. barChart is nested under plotArea.
    bar = chart_el.find(".//" + qn("c:barChart"))
    if bar is None:
        raise RuntimeError("stacked bar chart element missing")
    vary = bar.find(qn("c:varyColors"))
    if vary is None:
        vary = etree.Element(qn("c:varyColors"))
        anchor = bar.find(qn("c:grouping"))
        if anchor is None:
            bar.append(vary)
        else:
            anchor.addnext(vary)
    vary.set("val", "0")

    v = chart.value_axis
    v.has_major_gridlines = False
    v_scaling = v._element.find(qn("c:scaling"))
    if v_scaling is None:
        v_scaling = etree.Element(qn("c:scaling"))
        v._element.insert(0, v_scaling)
    for tag, val in (("c:min", str(y_min)), ("c:max", str(y_max))):
        el = v_scaling.find(qn(tag))
        if el is None:
            el = etree.SubElement(v_scaling, qn(tag))
        el.set("val", val)
    v.format.line.fill.background()
    v.tick_labels.font.size = Pt(9)
    v.tick_labels.font.name = "Calibri"
    v.tick_labels.font.color.rgb = MUTED
    v.tick_labels.number_format = axis_fmt
    vAx = v._element
    # delete axis line clutter but keep labels
    for tag, val in (("c:majorTickMark", "none"), ("c:minorTickMark", "none"), ("c:tickLblPos", "nextTo")):
        el = vAx.find(qn(tag))
        if el is None:
            el = etree.SubElement(vAx, qn(tag))
        el.set("val", val)

    cat = chart.category_axis
    cat.format.line.fill.background()
    cat.tick_labels.font.size = Pt(12)
    cat.tick_labels.font.name = "Calibri"
    cat.tick_labels.font.color.rgb = NAVY
    cat.has_major_gridlines = False
    cAx = cat._element
    scaling = cAx.find(qn("c:scaling"))
    if scaling is None:
        scaling = etree.SubElement(cAx, qn("c:scaling"))
    if reverse_cats:
        orient = scaling.find(qn("c:orientation"))
        if orient is None:
            orient = etree.SubElement(scaling, qn("c:orientation"))
        orient.set("val", "maxMin")
    for tag, val in (("c:majorTickMark", "none"), ("c:minorTickMark", "none"), ("c:tickLblPos", "nextTo")):
        el = cAx.find(qn(tag))
        if el is None:
            el = etree.SubElement(cAx, qn(tag))
        el.set("val", val)
    # drop chart border
    spPr = chart_el.find(qn("c:spPr"))
    if spPr is None:
        spPr = etree.SubElement(chart_el, qn("c:spPr"))
    ln = spPr.find(qn("a:ln"))
    if ln is None:
        ln = etree.SubElement(spPr, qn("a:ln"))
    for child in list(ln):
        ln.remove(child)
    etree.SubElement(ln, qn("a:noFill"))
    # plot area no fill
    plotArea = chart_el.find(".//" + qn("c:plotArea"))
    pSp = plotArea.find(qn("c:spPr"))
    if pSp is None:
        pSp = etree.SubElement(plotArea, qn("c:spPr"))
    if pSp.find(qn("a:noFill")) is None and pSp.find(qn("a:solidFill")) is None:
        pSp.append(etree.Element(qn("a:noFill")))


def add_hbar(slide, l, t, w, h, cats, gray_vals, accent_vals, y_max, axis_fmt, gray_fmt, accent_fmt):
    data = CategoryChartData()
    data.categories = cats
    data.add_series("Other", gray_vals)
    data.add_series("Story", accent_vals)
    graphic = slide.shapes.add_chart(
        XL_CHART_TYPE.BAR_STACKED, Inches(l), Inches(t), Inches(w), Inches(h), data
    )
    chart = graphic.chart
    style_chart(chart, 0, y_max, axis_fmt, reverse_cats=True)
    style_series(chart.series[0], BAR_GRAY, gray_fmt)
    style_series(chart.series[1], BAR_RED, accent_fmt)
    return graphic


def build(n):
    prs = Presentation()
    prs.slide_width = SLIDE_W
    prs.slide_height = SLIDE_H
    prs.core_properties.title = "EH&B Executive Summary — appendix"
    prs.core_properties.subject = "Appendix slides for copy into the final deck"
    blank = prs.slide_layouts[6]

    mix = n["mix"]
    shares = [round(m["dollars"] / n["company"] * 100, 1) for m in mix]
    # Display values must match one-decimal rounding of dollars / 13,597.
    assert shares[0] == 43.0
    cats = [m["line"] for m in mix]
    gray = [0 if m["role"] == "Accent" else s for m, s in zip(mix, shares)]
    accent = [s if m["role"] == "Accent" else 0 for m, s in zip(mix, shares)]

    # Slide 1 — mix
    s = prs.slides.add_slide(blank)
    chrome(
        s,
        "APPENDIX  ·  EH&B — REVENUE MIX",
        f"Internet is already 43% of Q1 2026 revenue, and it is the line that shrank ({MINUS}$78 million)",
        "Source: Charter Ex99.1, Q1 2026. Shares = line ÷ $13,597 million, one decimal. "
        f"Internet $5,852 million vs $5,930 million ({MINUS}1.3%). "
        f"{MINUS}117,000 is residential Internet net adds; total Internet was {MINUS}120,000.",
        "A1",
    )
    add_hbar(
        s, 0.40, 1.68, 8.45, 4.50,
        cats, gray, accent, y_max=55, axis_fmt='0"%"',
        gray_fmt='0.0"%";;', accent_fmt='0.0"%";;',
    )
    card(s, 9.00, 1.72, 3.80, 4.60, PANEL)
    add_text(s, 9.22, 1.88, 3.40, 0.28, [("READ", 10, True, False, BLUE, 150)], anchor="ctr")
    add_text(s, 9.22, 2.22, 3.40, 0.48, [("43%", 26, True, False, NAVY)], anchor="ctr")
    add_text(
        s, 9.22, 2.68, 3.40, 0.55,
        [("Internet share of $13,597 million", 12, False, False, GRAY)],
    )
    add_text(s, 9.22, 3.35, 3.40, 0.48, [(f"{MINUS}$78 million", 26, True, False, RED)], anchor="ctr")
    add_text(
        s, 9.22, 3.82, 3.40, 0.50,
        [(f"$5,852 vs $5,930 million ({MINUS}1.3%)", 12, False, False, GRAY)],
    )
    add_text(s, 9.22, 4.45, 3.40, 0.48, [(f"{MINUS}117,000", 26, True, False, RED)], anchor="ctr")
    add_text(
        s, 9.22, 4.95, 3.40, 0.85,
        [
            ("Residential Internet customers", 12, False, False, GRAY, None, None, 4),
            (f"Total Internet was {MINUS}120,000", 12, False, False, GRAY),
        ],
    )
    add_text(
        s, 9.22, 5.82, 3.40, 0.38,
        [("Shares from zero. Internet in red; every other line in gray.", 11, False, False, GRAY)],
    )

    # Slide 2 — printed bridge. Lengths are absolute millions; signs live in the labels.
    s = prs.slides.add_slide(blank)
    chrome(
        s,
        "APPENDIX  ·  EH&B — PRINTED Q1 BRIDGE",
        f"Residential Internet dollars fell $78 million because volume took $87 million and rate put back $9 million",
        "Source: Printed bridge — Charter Form 10-Q, quarter ended 31 March 2026, residential Internet revenues. "
        "FY2025 bridge — Form 10-K. Derived −$90 / +$12 is a cross-check and does not replace the print.",
        "A2",
    )
    add_hbar(
        s, 0.40, 1.85, 8.45, 2.55,
        ["Smaller average base", "Rate and product mix"],
        [0, 9],
        [87, 0],
        y_max=100,
        axis_fmt='$#,##0',
        gray_fmt='"+$"#,##0;;',
        accent_fmt=f'"{MINUS}"$#,##0;;',
    )
    # Signed callouts sit with the series: volume label reads −$87, rate +$9.
    # The chart labels are unsigned magnitudes. Replace with explicit signed labels
    # drawn beside the chart so the print direction cannot be dropped.
    add_text(
        s, 0.55, 4.40, 8.2, 0.70,
        [
            (
                f"Printed 10-Q: volume {MINUS}$87 million  ·  rate and mix +$9 million  ·  net {MINUS}$78 million.",
                14, True, False, NAVY, None, None, 4,
            ),
            (
                "Bar length is millions of dollars, from zero. The red bar is volume.",
                12, False, False, GRAY,
            ),
        ],
    )
    card(s, 9.00, 1.72, 3.80, 4.60, PANEL)
    add_text(s, 9.22, 1.86, 3.40, 0.26, [("PRINTED 10-Q", 10, True, False, BLUE, 150)])
    add_text(s, 9.22, 2.14, 3.40, 0.40, [(f"{MINUS}$87 million", 22, True, False, RED)])
    add_text(s, 9.22, 2.50, 3.40, 0.28, [("Volume — smaller average base", 12, False, False, GRAY)])
    add_text(s, 9.22, 2.82, 3.40, 0.40, [("+$9 million", 22, True, False, NAVY)])
    add_text(s, 9.22, 3.18, 3.40, 0.28, [("Rate and product mix", 12, False, False, GRAY)])
    add_text(s, 9.22, 3.48, 3.40, 0.36, [(f"Net {MINUS}$78 million", 16, True, False, RED)])
    add_text(s, 9.22, 4.00, 3.40, 0.24, [("DERIVED CROSS-CHECK", 10, True, False, MUTED, 120)])
    add_text(
        s, 9.22, 4.24, 3.40, 0.95,
        [
            (
                f"Rounds to {MINUS}$90 million and +$12 million "
                f"({MINUS}$89.8 and +$11.8 unrounded).",
                11, False, False, GRAY, None, None, 3,
            ),
            (
                f"Implied rate $70.72 vs $70.58. These figures do not replace {MINUS}$87 / +$9.",
                11, False, False, GRAY,
            ),
        ],
    )
    add_text(
        s, 9.22, 5.22, 3.40, 0.90,
        [
            ("FY2025, printed in the 10-K", 11, True, False, NAVY, None, None, 2),
            (
                f"Rate +$785 million covered volume {MINUS}$380 million, net +$405 million, on 393,000 fewer residential Internet customers.",
                11, False, False, GRAY,
            ),
        ],
    )

    # Slide 3 — plant. 0–100 so penetration reads as a share of passings.
    s = prs.slides.add_slide(blank)
    chrome(
        s,
        "APPENDIX  ·  EH&B — PLANT",
        f"Company take is 54.0% of 58.7 million passings; rural take is 38.1% after $7.7 billion",
        "Source: 54.0% = 31,683 ÷ 58,661 thousand estimated passings, Ex99.1, 31 March 2026 "
        "(table is 58.661 million). Rural 38.1% = 527 ÷ 1,385 thousand, Q1 2026 trending. "
        "$7.7 billion subsidized rural construction, FY2025 10-K, 2022 through 31 Dec 2025. "
        "$93.8 billion and 4.18× are 30 June 2026, labeled later public facts.",
        "A3",
    )
    add_hbar(
        s, 0.40, 1.78, 8.45, 2.35,
        ["Company, Q1 2026", "Rural lit plant, Q1 2026"],
        [54.0, 0],
        [0, 38.1],
        y_max=100,
        axis_fmt='0"%"',
        gray_fmt='0.0"%";;',
        accent_fmt='0.0"%";;',
    )
    add_text(
        s, 0.55, 4.15, 8.2, 0.70,
        [
            (
                "Bars are penetration of passings, from zero to 100%. Red is rural take on plant already lit.",
                12, False, False, GRAY, None, None, 3,
            ),
            (
                "Q2 2026, later public fact: 53.4% on 58.981 million passings. Same direction.",
                12, False, False, GRAY,
            ),
        ],
    )
    card(s, 9.00, 1.72, 3.80, 4.60, PANEL)
    add_text(s, 9.22, 1.86, 3.40, 0.26, [("ON THE PLANT", 10, True, False, BLUE, 150)])
    add_text(s, 9.22, 2.14, 3.40, 0.38, [("54.0%", 22, True, False, NAVY)])
    add_text(s, 9.22, 2.50, 3.40, 0.40, [("31,683 ÷ 58,661 thousand relationships / passings", 12, False, False, GRAY)])
    add_text(s, 9.22, 2.95, 3.40, 0.38, [("38.1%", 22, True, False, RED)])
    add_text(s, 9.22, 3.32, 3.40, 0.40, [("527 ÷ 1,385 thousand rural relationships / lit passings", 12, False, False, GRAY)])
    add_text(s, 9.22, 3.78, 3.40, 0.36, [("$7.7 billion", 20, True, False, NAVY)])
    add_text(
        s, 9.22, 4.14, 3.40, 0.40,
        [("Subsidized rural construction since 2022, through 31 Dec 2025", 12, False, False, GRAY)],
    )
    add_text(
        s, 9.22, 4.62, 3.40, 0.70,
        [
            ("Left blank — not disclosed", 11, True, False, NAVY, None, None, 2),
            ("Contribution per incremental Internet account", 11, False, False, GRAY, None, None, 1),
            ("Consumer acquisition cost", 11, False, False, GRAY),
        ],
    )
    add_text(
        s, 9.22, 5.28, 3.40, 0.90,
        [(
            "$93.8 billion principal and 4.18× at 30 June 2026 (later public fact). This density is not a price match, and it is not a reason to build more rural miles.",
            11, False, False, GRAY,
        )],
    )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    prs.save(OUT)
    return OUT


def main():
    crit, mix, rate, plant = load_numbers()
    n = assert_lock(crit, mix, rate, plant)
    # Printed bridge is the headline. Derived rounds must stay out of the chart series.
    assert n["vol"] == -87 and n["rate"] == 9
    path = build(n)
    print(path)


if __name__ == "__main__":
    main()
