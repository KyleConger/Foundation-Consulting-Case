# -*- coding: utf-8 -*-
"""Export Charter vs Comcast state-lead exhibit to PDF via HTML + Chrome headless."""
from __future__ import annotations

import csv
import json
import subprocess
import time
from pathlib import Path

ROOT = Path(r"c:\Users\Owner\Desktop\MAN6930 Case")
OUT = ROOT / "Analysis" / "cable-share-small-firm" / "out"
DEST_DIR = ROOT / "Decisions" / "EH&B"
PDF_PATH = DEST_DIR / "Comcast vs Charter.pdf"
HTML_PATH = Path(r"C:\Users\Owner\AppData\Local\Temp\chtr-vs-cmcsa-state-lead.html")
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

DEST_DIR.mkdir(parents=True, exist_ok=True)

with open(OUT / "summary.json", encoding="utf-8") as f:
    summary = json.load(f)

SOURCE_URL = "https://broadbandmap.fcc.gov/data-download"


def load_csv(path):
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def as_int(x):
    if x is None or x == "":
        return None
    return int(float(x))


def as_pct(x):
    if x is None or x == "":
        return None
    return round(float(x) * 100, 1)


def esc(s: str) -> str:
    return (
        str(s)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def fmt_units(n: int | None) -> str:
    if n is None:
        return "—"
    if abs(n) >= 1_000_000:
        return f" {n / 1_000_000:.2f}M".replace(" 0.", " 0.").strip() if False else f"{n / 1_000_000:.2f}M".replace("0.00M", "0")
    if abs(n) >= 10_000:
        return f"{n / 1_000:.0f}k"
    return f"{n:,}"


def fmt_units_display(n: int | None) -> str:
    """Match canvas rounding: 5.58M, 44k, 2,211, 4,407."""
    if n is None:
        return "—"
    if abs(n) >= 1_000_000:
        val = n / 1_000_000
        text = f"{val:.2f}M"
        if text.endswith("0M"):
            text = f"{val:.1f}M"
        return text
    if abs(n) >= 10_000:
        return f"{round(n / 1_000):,}k" if n >= 100_000 else f"{round(n / 1_000)}k"
    return f"{n:,}"


def fmt_margin(n: int) -> str:
    sign = "+" if n > 0 else ("−" if n < 0 else "")
    mag = abs(n)
    if mag >= 1_000_000:
        val = mag / 1_000_000
        text = f"{val:.2f}M"
        if text.endswith("0M"):
            text = f"{val:.1f}M"
        return f"{sign}{text}"
    if mag >= 10_000:
        return f"{sign}{round(mag / 1_000)}k"
    if mag == 0:
        return "—"
    return f"{sign}{mag:,}"


def fmt_share(pct: float | None, units: int | None) -> str:
    if units is None or pct is None:
        return "—"
    if pct < 0.1:
        return f"{fmt_units_display(units)} · <0.1%"
    return f"{fmt_units_display(units)} · {pct:.1f}%"


def fmt_fabric(n: int) -> str:
    if n >= 1_000_000:
        val = n / 1_000_000
        text = f"{val:.2f}M"
        if text.endswith("0M"):
            text = f"{val:.1f}M"
        return text
    return f"{round(n / 1_000)}k"


rows = load_csv(OUT / "chtr_vs_cmcsa_state_leads.csv")
assert len(rows) == 51

n_ch = sum(1 for r in rows if r["leader"] == "Charter")
n_cm = sum(1 for r in rows if r["leader"] == "Comcast")
n_neither = sum(1 for r in rows if r["leader"] == "neither present")
n_tie = sum(1 for r in rows if r["leader"] == "tie")
n_ch_present = sum(1 for r in rows if r["charter_present"] == "True")
n_cm_present = sum(1 for r in rows if r["comcast_present"] == "True")
assert (n_ch, n_cm, n_neither, n_tie) == (19, 27, 5, 0)
assert (n_ch_present, n_cm_present) == (42, 41)

ch_lead = [r for r in rows if r["leader"] == "Charter"]
cm_lead = [r for r in rows if r["leader"] == "Comcast"]
neither = [r for r in rows if r["leader"] == "neither present"]
cm_by_size = sorted(cm_lead, key=lambda r: as_int(r["margin_units_charter_minus_comcast"]))

top5_ch = ch_lead[:5]
top5_cm = cm_by_size[:5]
chart_rows = ch_lead[:10] + list(reversed(cm_by_size[:10]))

CITE = (
    "Source: Federal Communications Commission, Broadband Data Collection / "
    "National Broadband Map, as of 31 Dec 2025 (D25), revision 15 Sep 2026. "
    "Files: bdc_us_provider_list_D25_15sep2026.csv (holding company / FRN / provider ID); "
    "bdc_us_provider_summary_by_geography_D25_15sep2026.csv (res_st_pct, geography_type = State, "
    "data_type = Fixed Broadband); "
    "bdc_us_fixed_broadband_summary_by_geography_D25_15sep2026.csv "
    "(total_units, State / Total / Any Technology / residential). "
    f"Download: {SOURCE_URL}. "
    "Charter: Charter Communications, FRN 0025646373, provider ID 130235. "
    "Comcast: Comcast Corporation, FRN 0003768165, provider ID 130317. "
    "Affiliates not rolled in (Sonic Spectrum and Red Spectrum are unrelated). "
    "Missing row or 0.0000 treated as absent. "
    "Recomputed in Analysis/cable-share-small-firm/build_state_leads.py."
)

css = """
@page { size: letter; margin: 0.5in; }
* { box-sizing: border-box; }
body { font-family: "Segoe UI", Calibri, Arial, sans-serif; color: #1a1a1a; font-size: 10.5pt; line-height: 1.4; margin: 0; }
h1 { font-size: 16.5pt; margin: 6px 0 8px; font-weight: 650; }
h2 { font-size: 12.5pt; margin: 16px 0 6px; font-weight: 650; page-break-after: avoid; }
h3 { font-size: 11pt; margin: 12px 0 4px; font-weight: 600; page-break-after: avoid; }
p { margin: 5px 0; }
.muted { color: #555; }
.small, .src { font-size: 7.5pt; color: #555; line-height: 1.35; margin: 4px 0 8px; word-break: break-word; }
.src { color: #444; }
.pills { display: flex; gap: 6px; flex-wrap: wrap; }
.pill { border: 1px solid #c8c8c8; border-radius: 999px; padding: 2px 9px; font-size: 8.5pt; color: #444; background: #f5f5f5; }
.pill.info { background: #e8f1fb; border-color: #9bb8d9; color: #1a4a7a; }
.pill.warn { background: #fff8e8; border-color: #e0c88a; color: #6a5200; }
.callout { border: 1px solid #d0d0d0; background: #fafafa; padding: 8px 10px; margin: 8px 0; border-radius: 4px; page-break-inside: avoid; }
.callout.warn { background: #fff8e8; border-color: #e0c88a; }
.callout.info { background: #f0f6fc; border-color: #b7cce3; }
.callout-title { font-weight: 650; margin-bottom: 3px; }
.stats { display: grid; grid-template-columns: 1fr 1fr 1fr 1fr; gap: 10px; margin: 8px 0; }
.stat { border: 1px solid #e0e0e0; padding: 10px; border-radius: 4px; page-break-inside: avoid; }
.stat .v { font-size: 18pt; font-weight: 650; }
.stat .l { font-size: 8.5pt; color: #666; }
.stat.info .v { color: #1a5fb4; }
.stat.warn .v { color: #8a6d00; }
hr { border: none; border-top: 1px solid #ddd; margin: 14px 0; }
.bar-row { display: flex; align-items: center; margin: 2px 0; page-break-inside: avoid; }
.bar-label { width: 36px; font-size: 8.5pt; flex-shrink: 0; font-variant-numeric: tabular-nums; }
.bar-track { flex: 1; background: #eee; height: 13px; }
.bar-fill { height: 100%; background: #9aa0a6; }
.bar-fill.accent { background: #1a5fb4; }
.bar-val { width: 52px; text-align: right; font-size: 8.5pt; margin-left: 5px; font-variant-numeric: tabular-nums; }
table { width: 100%; border-collapse: collapse; font-size: 8pt; margin: 6px 0; }
th, td { border-bottom: 1px solid #e5e5e5; padding: 3px 5px; text-align: left; }
th { font-weight: 650; border-bottom: 1.5px solid #bbb; background: #f7f7f7; }
td.num, th.num { text-align: right; font-variant-numeric: tabular-nums; }
tr.ch td { background: #eef4fb; }
tr.ne td { background: #fff8e8; }
.grid2 { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
.legend { display: flex; gap: 14px; font-size: 8.5pt; margin: 4px 0 6px; color: #555; }
.swatch { display: inline-block; width: 10px; height: 10px; margin-right: 3px; vertical-align: -1px; }
.swatch.gray { background: #9aa0a6; } .swatch.blue { background: #1a5fb4; }
"""


def bar_row(abbr: str, lead_m: float, charter: bool) -> str:
    max_m = 5.54
    width = max((lead_m / max_m) * 100, 0.6 if lead_m > 0 else 0)
    cls = "accent" if charter else ""
    sign = "" if charter else "−"
    return (
        f'<div class="bar-row"><div class="bar-label">{esc(abbr)}</div>'
        f'<div class="bar-track"><div class="bar-fill {cls}" style="width:{width:.2f}%"></div></div>'
        f'<div class="bar-val">{sign}{lead_m:.2f}M</div></div>'
    )


chart_bars = []
for r in chart_rows:
    margin = as_int(r["margin_units_charter_minus_comcast"])
    lead_m = round(abs(margin) / 1_000_000, 2)
    chart_bars.append(bar_row(r["abbr"], lead_m, r["leader"] == "Charter"))
chart_html = "\n".join(chart_bars)


def top_table(subset, charter: bool) -> str:
    body = []
    for r in subset:
        ch_u = as_int(r["charter_est_units"])
        cm_u = as_int(r["comcast_est_units"])
        ch_p = as_pct(r["charter_res_st_pct"])
        cm_p = as_pct(r["comcast_res_st_pct"])
        cls = "ch" if charter else ""
        body.append(
            f'<tr class="{cls}"><td>{esc(r["state"])}</td>'
            f'<td class="num">{esc(fmt_share(ch_p, ch_u))}</td>'
            f'<td class="num">{esc(fmt_share(cm_p, cm_u))}</td>'
            f'<td class="num">{esc(fmt_margin(as_int(r["margin_units_charter_minus_comcast"])))}</td>'
            f'<td class="num">{esc(fmt_fabric(as_int(r["total_residential_units"])))}</td></tr>'
        )
    return (
        "<table><thead><tr><th>State</th><th class='num'>Charter</th>"
        "<th class='num'>Comcast</th><th class='num'>Margin</th>"
        "<th class='num'>State fabric</th></tr></thead><tbody>"
        + "\n".join(body)
        + "</tbody></table>"
    )


def all_trs() -> str:
    out = []
    for r in rows:
        leader = "Neither" if r["leader"] == "neither present" else r["leader"]
        cls = "ch" if leader == "Charter" else ("ne" if leader == "Neither" else "")
        ch_u = as_int(r["charter_est_units"])
        cm_u = as_int(r["comcast_est_units"])
        ch_p = as_pct(r["charter_res_st_pct"])
        cm_p = as_pct(r["comcast_res_st_pct"])
        margin = as_int(r["margin_units_charter_minus_comcast"])
        margin_txt = "—" if leader == "Neither" else fmt_margin(margin)
        out.append(
            f'<tr class="{cls}"><td>{esc(r["state"])} ({esc(r["abbr"])})</td>'
            f"<td>{esc(leader)}</td>"
            f'<td class="num">{esc(fmt_share(ch_p, ch_u))}</td>'
            f'<td class="num">{esc(fmt_share(cm_p, cm_u))}</td>'
            f'<td class="num">{esc(margin_txt)}</td>'
            f'<td class="num">{esc(fmt_fabric(as_int(r["total_residential_units"])))}</td></tr>'
        )
    return "\n".join(out)


html = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"/>
<title>Comcast vs Charter — state leads, FCC BDC availability</title>
<style>{css}</style></head><body>
<div class="pills">
  <span class="pill info">Availability, not subscribers</span>
  <span class="pill">FCC BDC D25 · 31 Dec 2025</span>
  <span class="pill warn">19 / 27 / 5</span>
</div>
<h1>Charter leads Comcast on residential locations served in 19 states; Comcast leads in 27, by 5.5 million units in New York and 4.4 million in Pennsylvania</h1>
<p class="muted">Metric: share of residential units at FCC Broadband Serviceable Locations where Charter Communications (Spectrum, provider ID 130235) or Comcast Corporation (Xfinity, provider ID 130317) reports residential fixed broadband availability. Estimated units = that share × the state’s residential fabric units. Beating = strictly larger share. This is availability / locations served — not subscriber share.</p>

<div class="stats">
  <div class="stat info"><div class="v">19</div><div class="l">States Charter leads</div></div>
  <div class="stat"><div class="v">27</div><div class="l">States Comcast leads</div></div>
  <div class="stat warn"><div class="v">5</div><div class="l">Neither present</div></div>
  <div class="stat"><div class="v">0</div><div class="l">Ties</div></div>
</div>

<div class="callout warn"><div class="callout-title">What this is not</div>
Not subscriber share, not Form 477 subscriptions, and not small-firm employment. Company 10-Ks do not publish state subscriber counts; national mix is not allocated to states. A location the provider can serve is not a customer. Charter files in 42 states on this vintage; Comcast in 41. Neither operator reports a positive residential footprint in Alaska, Iowa, North Dakota, Oklahoma, or South Dakota.
</div>

<h2>Largest unit leads: New York for Charter, Pennsylvania for Comcast</h2>
<p class="muted">Top 10 Charter leads and top 10 Comcast leads, sorted by Charter-minus-Comcast margin. Bars start at zero. Units are estimated residential locations served, millions.</p>
<div class="legend"><span><span class="swatch blue"></span>Charter unit lead (M)</span><span><span class="swatch gray"></span>Comcast unit lead (M)</span></div>
{chart_html}
<p class="small">Estimated residential units served, millions. Axis starts at zero. Source: FCC Broadband Data Collection, National Broadband Map, as of 31 Dec 2025 (D25), file revision 15 Sep 2026 — provider summary by geography × state residential fabric units.</p>

<div class="grid2">
  <div>
    <h3>Five largest Charter leads</h3>
    {top_table(top5_ch, True)}
  </div>
  <div>
    <h3>Five largest Comcast leads</h3>
    {top_table(top5_cm, False)}
  </div>
</div>
<p class="small">Fabric units are the state’s residential Broadband Serviceable Location units (the denominator). Hawaii covers 92% of a 604k-unit state (+557k) — a high percentage, a small lead next to New York.</p>
<p class="src">{esc(CITE)}</p>
<hr/>

<h2>All 51 jurisdictions, sorted by Charter-minus-Comcast unit margin</h2>
<table><thead><tr>
  <th>State</th><th>Leader</th>
  <th class="num">Charter locations · share</th>
  <th class="num">Comcast locations · share</th>
  <th class="num">Margin (CH−CM)</th>
  <th class="num">State fabric units</th>
</tr></thead>
<tbody>
{all_trs()}
</tbody></table>
<p class="small">Sorted by margin (Charter leads at top), not alphabetically. 19 Charter · 27 Comcast · 5 neither (AK, IA, ND, OK, SD) · 0 ties. Charter 42-state footprint / Comcast 41-state footprint on this vintage.</p>
<p class="src">{esc(CITE)}</p>
</body></html>"""

HTML_PATH.write_text(html, encoding="utf-8")

if PDF_PATH.exists():
    try:
        PDF_PATH.unlink()
    except OSError as e:
        print("WARN unlink", e)

cmd = [
    CHROME,
    "--headless=new",
    "--disable-gpu",
    "--no-pdf-header-footer",
    f"--print-to-pdf={PDF_PATH}",
    HTML_PATH.as_uri(),
]
r = subprocess.run(cmd, capture_output=True, text=True)
print("chrome_rc", r.returncode)
if r.stderr:
    print("chrome_err", r.stderr[:800])
time.sleep(1.5)

assert PDF_PATH.exists(), "PDF missing"
data = PDF_PATH.read_bytes()
print("BYTES", len(data))
print("HEADER", data[:8])

import pypdf

reader = pypdf.PdfReader(str(PDF_PATH))
print("PAGES", len(reader.pages))
text = "\n".join(p.extract_text() or "" for p in reader.pages)
checks = [
    "19",
    "27",
    "New York",
    "Pennsylvania",
    "FCC",
    "broadbandmap.fcc.gov",
    "availability",
    "not subscriber",
    "Alaska",
]
for c in checks:
    print(f"FOUND[{c}]={c.lower() in text.lower() if c != '19' else (c in text)}")
print("TEXT_LEN", len(text))
print("PATH", PDF_PATH)
