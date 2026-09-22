# -*- coding: utf-8 -*-
"""Export WFH canvas exhibit to PDF via HTML + Chrome headless (same route as employment PDF)."""
from __future__ import annotations

import csv
import json
import subprocess
import time
from pathlib import Path

ROOT = Path(r"c:\Users\Owner\Desktop\MAN6930 Case")
OUT = ROOT / "Analysis" / "work-from-home" / "out"
DEST_DIR = ROOT / "Decisions" / "EH&B"
PDF_PATH = DEST_DIR / "Work from Home Rates.pdf"
HTML_PATH = Path(r"C:\Users\Owner\AppData\Local\Temp\chtr-work-from-home-rates.html")
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

DEST_DIR.mkdir(parents=True, exist_ok=True)

with open(OUT / "summary.json", encoding="utf-8") as f:
    summary = json.load(f)


def load_csv(path):
    with open(path, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


acs = load_csv(OUT / "acs2024_wfh_by_state.csv")
atus = load_csv(OUT / "atus2024_work_at_home_breaks.csv")
abs_rows = load_csv(OUT / "abs2023_workhome_by_firm_size.csv")

us = next(r for r in acs if r["geo_level"] == "nation")
states = sorted(
    [r for r in acs if r["geo_level"] == "state"],
    key=lambda r: -float(r["wfh_rate_pct"]),
)

cite_acs = summary["citations"]["acs"]
cite_atus = summary["citations"]["atus"]
cite_abs = summary["citations"]["abs"]


def r1(x):
    return round(float(x), 1)


def fmt_int(x):
    return f"{int(float(x)):,}"


def esc(s: str) -> str:
    return (
        str(s)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def display_geo(name: str) -> str:
    return "D.C." if name == "District of Columbia" else name


def cite_block(c: dict) -> str:
    return (
        f"Source: {c['agency']}, {c['program']} — {c['table']}; year {c['year']}. "
        f"Question/variable: {c['variable_or_question']}. "
        f"URL used: {c['url']} · Also: {c['url_secondary']}. "
        f"Funded by: {c['funded_by']}."
    )


CITE_ACS = cite_block(cite_acs)
CITE_ATUS = cite_block(cite_atus)
CITE_ABS = cite_block(cite_abs)

ACS_US = r1(us["wfh_rate_pct"])
ACS_WORKERS = int(float(us["workers_16_plus"]))
ACS_WFH = int(float(us["worked_from_home"]))
DC = states[0]
MS = states[-1]
ACS_HIGH = r1(DC["wfh_rate_pct"])
ACS_LOW = r1(MS["wfh_rate_pct"])
ACS_SPREAD = r1(ACS_HIGH - ACS_LOW)


def atus_find(substr: str):
    # Prefer exact group match when substr is a full group name fragment
    for r in atus:
        if r["group"].strip().lower() == substr.lower():
            return r
    for r in atus:
        if substr.lower() in r["group"].lower():
            return r
    raise KeyError(substr)


ATUS_OVERALL = r1(atus_find("Total, 15").get("published_pct_one_decimal"))
ATUS_MGMT = r1(atus_find("Management, business").get("published_pct_one_decimal"))
ATUS_PROF = r1(atus_find("Professional and related").get("published_pct_one_decimal"))
ATUS_SERVICE = r1(atus_find("Service").get("published_pct_one_decimal"))
ATUS_TOP = r1(atus_find("highest quartile").get("published_pct_one_decimal"))
ATUS_BOT = r1(atus_find("lowest quartile").get("published_pct_one_decimal"))
ATUS_BACH = r1(atus_find("Bachelor").get("published_pct_one_decimal"))
ATUS_HS = r1(atus_find("High school graduates, no college").get("published_pct_one_decimal"))
ATUS_FT = r1(atus_find("Full-time").get("published_pct_one_decimal"))
ATUS_PT = r1(atus_find("Part-time").get("published_pct_one_decimal"))

ABS_LT = next(r for r in abs_rows if r["empszfi"] == "655" and r["buschar"] == "EWA")
ABS_GE = next(r for r in abs_rows if r["empszfi"] == "657" and r["buschar"] == "EWA")
ABS_LT500 = r1(ABS_LT["pct_of_employer_firms"])
ABS_GE500 = r1(ABS_GE["pct_of_employer_firms"])

# Chart: five highest + five lowest
chart_states = states[:5] + states[-5:]


def state_trs() -> str:
    rows = []
    for i, r in enumerate(states):
        cls = ' class="hi"' if i < 5 else (' class="lo"' if i >= len(states) - 5 else "")
        name = display_geo(r["geography"])
        rows.append(
            f'<tr{cls}><td>{i + 1}</td><td>{esc(name)}</td>'
            f'<td class="num">{r1(r["wfh_rate_pct"]):.1f}%</td>'
            f'<td class="num">{fmt_int(r["workers_16_plus"])}</td>'
            f'<td class="num">{fmt_int(r["worked_from_home"])}</td></tr>'
        )
    return "\n".join(rows)


def bar_row(label: str, pct: float, accent: bool = False, label_wide: bool = True) -> str:
    cls = "accent" if accent else ""
    lab_cls = "bar-label wide" if label_wide else "bar-label"
    width = max(pct, 0.4)  # visible stub for zero not needed here
    return (
        f'<div class="bar-row"><div class="{lab_cls}">{esc(label)}</div>'
        f'<div class="bar-track"><div class="bar-fill {cls}" style="width:{pct}%"></div></div>'
        f'<div class="bar-val">{pct:.1f}%</div></div>'
    )


css = """
@page { size: letter; margin: 0.5in; }
* { box-sizing: border-box; }
body { font-family: "Segoe UI", Calibri, Arial, sans-serif; color: #1a1a1a; font-size: 10.5pt; line-height: 1.4; margin: 0; }
h1 { font-size: 18pt; margin: 6px 0; font-weight: 650; }
h2 { font-size: 12.5pt; margin: 18px 0 6px; font-weight: 650; page-break-after: avoid; }
h3 { font-size: 11pt; margin: 12px 0 4px; font-weight: 600; page-break-after: avoid; }
p { margin: 5px 0; }
.muted { color: #555; }
.small, .src { font-size: 7.5pt; color: #555; line-height: 1.35; margin: 4px 0 8px; word-break: break-word; }
.src { color: #444; }
.pills { display: flex; gap: 6px; flex-wrap: wrap; }
.pill { border: 1px solid #c8c8c8; border-radius: 999px; padding: 2px 9px; font-size: 8.5pt; color: #444; background: #f5f5f5; }
.pill.info { background: #e8f1fb; border-color: #9bb8d9; color: #1a4a7a; }
.callout { border: 1px solid #d0d0d0; background: #fafafa; padding: 8px 10px; margin: 8px 0; border-radius: 4px; page-break-inside: avoid; }
.callout.warn { background: #fff8e8; border-color: #e0c88a; }
.callout.info { background: #f0f6fc; border-color: #b7cce3; }
.callout-title { font-weight: 650; margin-bottom: 3px; }
.stats { display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; margin: 8px 0; }
.stats.two { grid-template-columns: 1fr 1fr; }
.stats.four { grid-template-columns: 1fr 1fr 1fr 1fr; }
.stat { border: 1px solid #e0e0e0; padding: 10px; border-radius: 4px; page-break-inside: avoid; }
.stat .v { font-size: 18pt; font-weight: 650; }
.stat .l { font-size: 8.5pt; color: #666; }
.stat.info .v { color: #1a5fb4; }
hr { border: none; border-top: 1px solid #ddd; margin: 14px 0; }
.bar-row { display: flex; align-items: center; margin: 3px 0; page-break-inside: avoid; }
.bar-label { width: 70px; font-size: 9pt; flex-shrink: 0; }
.bar-label.wide { width: 210px; }
.bar-track { flex: 1; background: #eee; height: 14px; }
.bar-fill { height: 100%; background: #9aa0a6; }
.bar-fill.accent { background: #1a5fb4; }
.bar-val { width: 48px; text-align: right; font-size: 9pt; margin-left: 5px; }
table { width: 100%; border-collapse: collapse; font-size: 8pt; margin: 6px 0; }
th, td { border-bottom: 1px solid #e5e5e5; padding: 3px 5px; text-align: left; }
th { font-weight: 650; border-bottom: 1.5px solid #bbb; background: #f7f7f7; }
td.num, th.num { text-align: right; font-variant-numeric: tabular-nums; }
tr.hi td { background: #eef4fb; }
tr.lo td { background: #f5f5f5; }
.card { border: 1px solid #ddd; padding: 8px 10px; border-radius: 4px; margin: 8px 0; page-break-inside: avoid; }
.card-h { font-weight: 650; margin-bottom: 3px; }
.legend { display: flex; gap: 14px; font-size: 8.5pt; margin: 4px 0 6px; color: #555; }
.swatch { display: inline-block; width: 10px; height: 10px; margin-right: 3px; vertical-align: -1px; }
.swatch.gray { background: #9aa0a6; } .swatch.blue { background: #1a5fb4; }
"""

chart_bars = "\n".join(
    bar_row(
        display_geo(r["geography"]),
        r1(r["wfh_rate_pct"]),
        accent=(i < 5),
    )
    for i, r in enumerate(chart_states)
)

proxy_items = [
    ("Mgmt / business / finance", ATUS_MGMT, True),
    ("Professional & related", ATUS_PROF, False),
    ("Top earnings quartile", ATUS_TOP, True),
    ("Bachelor's+", ATUS_BACH, False),
    ("ATUS overall", ATUS_OVERALL, False),
    ("HS, no college", ATUS_HS, False),
    ("Bottom earnings quartile", ATUS_BOT, False),
    ("Service occupations", ATUS_SERVICE, False),
]
proxy_bars = "\n".join(bar_row(lab, pct, accent=acc) for lab, pct, acc in proxy_items)

html = f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"/>
<title>Work from Home Rates — Charter EH&amp;B</title>
<style>{css}</style></head><body>
<div class="pills">
  <span class="pill info">Descriptive rates</span>
  <span class="pill">Not a sizing</span>
  <span class="pill">RETRIEVED only</span>
</div>
<h1>Usually-WFH spans {ACS_SPREAD:.1f} points across states — {display_geo(DC["geography"])} {ACS_HIGH:.1f}% vs {MS["geography"]} {ACS_LOW:.1f}%</h1>
<p class="muted">Denominator for the headline and state table: workers 16+ whose usual means of transportation to work was “worked from home” (ACS journey-to-work). Seniority and firm-size exhibits use different official surveys and say so on the exhibit. One decimal on charts; full precision in Analysis/work-from-home/out/.</p>

<div class="callout info"><div class="callout-title">What this changes for the benefits analogy</div>
The corporate → consumer Internet analogy only lands a Spectrum residential account if the employee actually works from home. These rates show that “home as workplace” is concentrated — by state, by occupation/earnings (seniority proxies), and at large firms — so any employer-provisioned home broadband motion is not a uniform share of all workers.
</div>

<h2>United States — usually worked from home</h2>
<div class="stats">
  <div class="stat info"><div class="v">{ACS_US:.1f}%</div><div class="l">US usually-WFH rate</div></div>
  <div class="stat"><div class="v">{ACS_WORKERS / 1e6:.1f}M</div><div class="l">Workers 16+ (denominator)</div></div>
  <div class="stat"><div class="v">{ACS_WFH / 1e6:.1f}M</div><div class="l">Usually worked from home</div></div>
</div>
<p class="small">Counts: {fmt_int(ACS_WFH)} worked from home ÷ {fmt_int(ACS_WORKERS)} workers 16+ = {ACS_US:.1f}% (exhibit rounding to 1 decimal; CSV full precision {float(us["wfh_rate_pct"]):.6f}%)</p>
<p class="src">{esc(CITE_ACS)}</p>
<hr/>

<h2>Highest usually-WFH states sit near 17–23%; lowest cluster at 6–8%</h2>
<p class="muted">Chart shows five highest and five lowest states only. Full 51-row table (50 states + D.C.) below. Sorted by rate, not alphabetically. Bars start at zero.</p>
<div class="legend"><span><span class="swatch blue"></span>Highest five</span><span><span class="swatch gray"></span>Lowest five</span></div>
{chart_bars}
<p class="small">High: {display_geo(DC["geography"])} {ACS_HIGH:.1f}% (n={fmt_int(DC["workers_16_plus"])} workers 16+) · Low: {MS["geography"]} {ACS_LOW:.1f}% (n={fmt_int(MS["workers_16_plus"])} workers 16+) · Spread: {ACS_SPREAD:.1f} percentage points</p>
<p class="src">{esc(CITE_ACS)}</p>

<h3>All states + D.C. — ACS usually-WFH (2024)</h3>
<table><thead><tr><th>Rank</th><th>State</th><th class="num">Usually WFH %</th><th class="num">Workers 16+</th><th class="num">Worked from home</th></tr></thead>
<tbody>
{state_trs()}
</tbody></table>
<p class="small">Sorted descending by usually-WFH rate · percentages to 1 decimal · every row from acs2024_wfh_by_state.csv</p>
<p class="src">{esc(CITE_ACS)}</p>
<hr/>

<h2>Seniority proxies: management {ATUS_MGMT:.1f}% and top earners {ATUS_TOP:.1f}% work at home on days worked — vs {ATUS_SERVICE:.1f}% in service jobs</h2>
<div class="callout warn"><div class="callout-title">Different source and definition than the state table</div>
Official surveys do not publish WFH by job level (VP vs individual contributor). Closest published cuts are occupation, usual weekly earnings quartile, and education — labeled here as seniority proxies. ATUS counts any work at home on days worked (2024), not ACS “usually worked from home.”
</div>
<div class="stats four">
  <div class="stat info"><div class="v">{ATUS_MGMT:.1f}%</div><div class="l">Mgmt / business / finance</div></div>
  <div class="stat info"><div class="v">{ATUS_TOP:.1f}%</div><div class="l">Top earnings quartile</div></div>
  <div class="stat"><div class="v">{ATUS_SERVICE:.1f}%</div><div class="l">Service occupations</div></div>
  <div class="stat"><div class="v">{ATUS_BOT:.1f}%</div><div class="l">Bottom earnings quartile</div></div>
</div>
<div class="legend"><span><span class="swatch blue"></span>Story groups (mgmt / top earners)</span><span><span class="swatch gray"></span>Context (other ATUS cuts)</span></div>
{proxy_bars}
<p class="small">Also: bachelor's+ {ATUS_BACH:.1f}% vs high-school no college {ATUS_HS:.1f}%; full-time {ATUS_FT:.1f}% vs part-time {ATUS_PT:.1f}%; ATUS overall {ATUS_OVERALL:.1f}% of those who worked that day. All figures are % of employed persons who worked on an average day.</p>
<p class="src">{esc(CITE_ATUS)}</p>
<hr/>

<h2>{ABS_GE500:.1f}% of firms with 500+ employees had any WFH workers — vs {ABS_LT500:.1f}% of firms under 500</h2>
<div class="callout warn"><div class="callout-title">Different source — firm-level, not worker-level</div>
This is the share of employer firms that reported having employees who worked from home (ABS WORKHOME), not the share of workers at small vs large firms who WFH. ACS/ATUS do not publish a worker×firm-size cross; that break was not invented. Bins are EMPSZFI 655 (&lt;500) and 657 (500+) — the SBA cutoff used elsewhere in this project.
</div>
<div class="stats two">
  <div class="stat info"><div class="v">{ABS_GE500:.1f}%</div><div class="l">Firms 500+ with any WFH employees</div></div>
  <div class="stat"><div class="v">{ABS_LT500:.1f}%</div><div class="l">Firms &lt;500 with any WFH employees</div></div>
</div>
<div class="legend"><span><span class="swatch blue"></span>% of firms that had employees who worked from home</span></div>
{bar_row("Firms &lt;500 employees", ABS_LT500, accent=True)}
{bar_row("Firms 500+ employees", ABS_GE500, accent=True)}
<p class="src">{esc(CITE_ABS)}</p>
<hr/>

<h2>Source conflicts and breaks refused</h2>
<div class="card"><div class="card-h">Definition conflict (not an error)</div>
ACS US usually-WFH is {ACS_US:.1f}% of workers 16+. ATUS US any-work-at-home on days worked is {ATUS_OVERALL:.1f}%. Both are official; they answer different questions. State rankings use ACS only. Seniority uses ATUS only. Firm size uses ABS firm-level only.
</div>
<div class="card"><div class="card-h">Refused to invent</div>
• Job title / corporate seniority ladder (VP vs IC) — not in ACS, ATUS, or ABS.<br/>
• Worker-level WFH rate × firm size &lt;500 vs 500+ — ABS is firm-level; no industry-mix imputation.<br/>
• Hybrid vs fully remote worker shares by state — not in ACS B08301; ATUS day-level “any time at home” is not a hybrid schedule measure.
</div>

<h3>Sources and reproducibility</h3>
<p class="src">{esc(CITE_ACS)}</p>
<p class="src">{esc(CITE_ATUS)}</p>
<p class="src">{esc(CITE_ABS)}</p>
<p class="src">Recompute script: Analysis/work-from-home/build_wfh_rates.py · CSVs: acs2024_wfh_by_state.csv, atus2024_work_at_home_breaks.csv, abs2023_workhome_by_firm_size.csv, assumption_register.csv · Every input tagged RETRIEVED; no ESTIMATED rates shipped. CSV is the source of truth if a canvas figure differs.</p>
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
    "13.3%",
    "22.9%",
    "6.2%",
    "48.1%",
    "51.0%",
    "35.8%",
    "77.5%",
    "census.gov",
    "bls.gov",
    "U.S. Census Bureau",
    "American Time Use Survey",
    "Annual Business Survey",
]
for c in checks:
    print(f"FOUND[{c}]={c in text}")
# Prefer a full URL hit
url_hits = [
    "https://www.bls.gov/news.release/archives/atus_06262025.htm",
    "https://data.census.gov/table/ACSDT1Y2024.B08301",
    "https://www2.census.gov/programs-surveys/abs/data/2023/AB2300CSCB04.zip",
    "census.gov",
    "bls.gov",
]
for u in url_hits:
    print(f"URL[{u}]={u in text}")
print("TEXT_LEN", len(text))
print("PATH", PDF_PATH)
