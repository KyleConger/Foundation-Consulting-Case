# EH&B — Employee Health & Benefits (corporate → consumer Internet)

**Naming collision — read this first.** Elsewhere in this repo, **EH&B** means *existing homes & businesses* (grow Internet on plant already built; `Decisions/decisions.md`, `Decisions/six-recommendation-areas.md`). **This folder is not that definition.** It is Kyle’s **Employee Health & Benefits** analogy: insurance brokers already place benefits; the test is whether that channel can open a **residential Spectrum Internet** account. The motion lands *inside* the existing-plant growth problem. It does not replace Rec 1 (tracker, then one reason-play).

This file is an **index + slide briefing**. It is not a memo and not a recommendation. Use it to pick the right exhibit. Do not invent take-up, commissions, serviceable %, or channel net adds.

---

## How to make a slide

1. Write one claim (finding + direction + magnitude).
2. Pick the file: **pdf** for print, **xlsx** for numbers, **canvas** for live titles/charts.
3. Copy the canvas `<H2>` as the slide title. Do not invent a topic title.
4. Put the source line on the slide (agency, table, year). Units stay on the exhibit.
5. One message, one accent, rest gray, bars at zero. No pie. No dual axis.

---

## Files in this folder

Verified 2026-09-22. No critic files here. `State Region Density Maps.xlsx` is **absent — in progress**. Filename `Chtr Small Large Employment Shares.pdf` is **not present**; the PDF is `Small Large Employment Shares.pdf`.

| File | What it is | Slide it supports | Source of numbers |
|---|---|---|---|
| `README.md` | This index | Do not put on a slide | — |
| `Kyle's Thoughts.docx` | Kyle’s Employee Health & Benefits chronology + corporate→consumer pitch. Industry context, not a verified firm history. | Framing / “why this analogy” only. No quantitative slide. | Kyle (approximate). Do not cite as Census/FCC/Ex99.1. |
| `Small Large Employment Shares.pdf` | Print exhibit: US / state / metro payroll employment at firms &lt;500 vs 500+. | “Large firms hold 54.1% of payroll jobs; state mix is not national.” | Census SUSB 2022. Build: `Analysis/small-large-employment/`. Live title: `chtr-small-large-employment-shares`. |
| `Small Large Employment Shares.xlsx` | Same numbers, sheets: Notes, United States, States, Metros Exhibit High Low, Metros Full (387), MSA Full File, Cutoff Sensitivity. | Recalc / appendix tables. | Same SUSB 2022 files as `Analysis/small-large-employment/out/`. |
| `Work from Home Rates.pdf` | Print exhibit: ACS usual-WFH, ATUS any-work-at-home, ABS firm-had-WFH. | WFH **only if** each panel is labeled as a different question. | ACS 2024 B08301; ATUS 2024; ABS 2023 AB2300CSCB04. Build: `Analysis/work-from-home/`. Live: `chtr-work-from-home-rates`. |
| `Work from Home Rates.xlsx` | Same numbers, sheets: Notes, United States, States, Seniority proxies, Firm size. | Recalc / appendix. | Same as `Analysis/work-from-home/out/summary.json`. |
| `Brokerage Metrics.pdf` | Print of the **metric register** (what to measure next). Not a results deck. | “Eight core pulls; M-metrics without a number stay blank.” | Register only. Live: `chtr-ehb-broker-channel-core-metrics`. |
| `Brokerage Metrics.xlsx` | Register workbook: Notes, Core metrics (M10, M12, M1, M2, M5, M6, M9, M13), Later demoted, Already in hand. | Spec / appendix. Blank cells are intentional. | Definitions from this xlsx. In-hand cites point at SUSB + ACS/ATUS/ABS summaries. |
| `Brokerage Metrics Breakdown.pdf` | Print of pressure-tests on M1, M2, M5, M9, M13. | One metric per slide. Copy the matching canvas H2. | `Analysis/ehb-broker-metrics/m1`–`m13`. Canvases `chtr-ehb-m1-*` … `chtr-ehb-m13-*`. |
| `Brokerage Metrics Breakdown.xlsx` | Same: Notes, Scorecard, M1, M2, M5, M9, M13, Analogues. | Recalc / appendix. | Same Analysis folders. |
| `Comcast vs Charter.pdf` | Print: state location leads (availability). | “Charter leads 19 states, Comcast 27, neither 5 — locations, not subscribers.” | FCC BDC D25, 31 Dec 2025, rev. 15 Sep 2026. Build: `Analysis/cable-share-small-firm/`. Live: `chtr-vs-cmcsa-state-lead`. |
| `Comcast vs Charter.xlsx` | Same: Notes, State leads, Charter lead states, Comcast lead states, Neither. | Recalc / 51-row table. | `Analysis/cable-share-small-firm/out/chtr_vs_cmcsa_state_leads.csv`. |
| `State Region Density Maps.xlsx` | **In progress — file not in this folder.** | Do not build a density-map slide until the file exists. | — |

There is no `chtr-ehb-state-density-*` canvas.

---

## Related (do not move)

### Live canvases

Path: `C:\Users\Owner\.cursor\projects\c-Users-Owner-Desktop-MAN6930-Case\canvases\`

Copy the **H2**, not a topic title.

| Canvas | Use for | Committed H2 / claim to copy |
|---|---|---|
| `chtr-ehb-benefits-analogy-corporate-to-consumer.canvas.tsx` | Framing. Analogy holds only if a residential Internet account opens. | H1: “Benefits reframing → Spectrum: corporate sale that puts Internet in the home.” Productivity is the pitch, not the KPI. |
| `chtr-ehb-broker-channel-core-metrics.canvas.tsx` | Metric register / sequence of pulls. | “Forced cut — pull these eight next.” |
| `chtr-small-large-employment-shares.canvas.tsx` | SUSB employment. | “Large firms (500+) employ 54.1% of U.S. payroll workers; small firms hold 45.9%.” State: “66.3% in Montana to 39.6% in Florida.” Metro: “median … 49.8%.” |
| `chtr-work-from-home-rates.canvas.tsx` | WFH — three different questions. | ACS: “Highest usually-WFH states sit near 17–23%; lowest cluster at 6–8%.” ATUS and ABS have their own H2s; do not merge. |
| `chtr-vs-cmcsa-state-lead.canvas.tsx` | FCC location leads. | “Largest unit leads: New York for Charter, Pennsylvania for Comcast.” |
| `chtr-ehb-m1-broker-covered-lives.canvas.tsx` | M1 — no lives number. | Do not title a slide with SUSB 45.9% as M1. ESI overlay is not M1. |
| `chtr-ehb-m2-large-broker-concentration.canvas.tsx` | M2 proxy. | “Top 10 EH&B filing names hold 44% of Form 5500 compensation; 56% is a long tail.” |
| `chtr-ehb-m5-serviceable-home-share.canvas.tsx` | M5 — **no employee number**. | “94.6% of payroll jobs are in a state where Charter files at least once — ESTIMATED, and biased high.” That is **not** M5. |
| `chtr-ehb-m9-payor-takeup.canvas.tsx` | M9 — no Charter take-up. | Analogues are offer rates, not Charter enrollment. |
| `chtr-ehb-m13-net-new-residential.canvas.tsx` | M13 = P − E − D. | Channel count is blank. “−117k” is **company** Q1’26 residential Internet, not the channel. |
| `chtr-ehb-economies-of-scale.canvas.tsx` | Why price-match is blocked; plant vs channel scale. | H1 names **$93.8B principal (4.18x)**. Not a TAM. |
| `chtr-churn-plays-strategies-regions.canvas.tsx` | Team play scores + Census-division plant context. | “EH&B is Best on plays 1 and 4, Works on 2 and 5, and No on 3 and 6.” |

Workspace copy of the WFH canvas also sits at `Analysis/work-from-home/chtr-work-from-home-rates.canvas.tsx`. Prefer the live canvases folder for titles.

### Analysis (arithmetic; do not relocate)

| Folder | Feeds |
|---|---|
| `Analysis/small-large-employment/` | SUSB 2022 US / state / metro. `out/summary.json` is the lock. |
| `Analysis/work-from-home/` | ACS / ATUS / ABS. `out/summary.json` is the lock. |
| `Analysis/cable-share-small-firm/` | FCC BDC D25 state leads. `out/summary.json` and `out/chtr_vs_cmcsa_state_leads.csv`. |
| `Analysis/ehb-broker-metrics/` | M1, M2, M5, M9, M13 registers and proxies. Blank channel numbers stay blank. |
| `Analysis/sellside-coverage/covering_analysts.csv` | Named covering analysts. **Do not paste sell-side research text.** |

### Churn attach (existing-plant play, not a replacement)

EH&B (this analogy / existing-plant GTM) **attaches to churn scenarios 1 and 4**. Team score also **Works on 2 and 5**. Official Rec 1 sequence is unchanged: fill the net-loss tracker first, then one reason-play on existing-plant core (`Decisions/six-recommendation-areas.md`). This folder is a **candidate play**, not a substitute for that sequence.

| File | Role |
|---|---|
| `Decisions/CHURN/README.md` | Type 1 folder index. Tracker cells empty on purpose. |
| `Decisions/CHURN/CHTR_Rec1_AttributionPlaybook.pptx` | Plays 1–6 definitions. |
| `Decisions/CHURN/CHTR Rec1 Attribution Dashboard.xlsx` | Attribution dashboard. |
| `Decisions/CHURN/Plays Strategies by Region.xlsx` | **Locked team scores.** Built by `build_plays_strategies_by_region.py`. |
| `Decisions/CHURN/chtr-churn-attribution-navigator.html` | Interactive navigator (plus `_2.html`). |
| `Decisions/six-recommendation-areas.md` | Official sequence. Areas 1–2 = CHURN; this motion is a candidate under existing-plant growth, not Areas 5–6 as written (those are Cox gate + non-mover model). |

**Team play scores (lock)**

| Play | Name | EH&B score |
|---:|---|---|
| 1 | FWA-driven losses | **Best** |
| 2 | Fiber-driven losses | **Works** |
| 3 | LEO-satellite-driven losses | **No** |
| 4 | Housing-driven losses | **Best** |
| 5 | Economic / non-pay churn | **Works** |
| 6 | Null result — no dominant driver | **No** |

Footnote if you use Works on 2 and 5: an earlier validation said **No** on 2 and 5. The workbook and `chtr-churn-plays-strategies-regions` keep the **team** scores.

---

## Committed numbers (do not drift)

If a slide needs a different figure, it is a new analysis — do not “round toward the story.”

| Figure | Definition | Year / as-of | Source | Do not confuse with |
|---|---|---|---|---|
| **45.9% / 54.1%** | Share of US mid-March **payroll employment** at employer firms **&lt;500** / **500+** (SBA enterprise cutoff) | SUSB **2022** | Census SUSB; `Analysis/small-large-employment/out/summary.json` | Broker-placed **lives**. ESI persons. Charter subscribers. M1. |
| **MT 66.3% · FL 39.6%** | State share of employment at firms &lt;500 | SUSB **2022** | Same | Metro rates. Charter footprint (not applied). |
| **49.8%** | Median &lt;500 employment share across **387** Metro Areas | SUSB **2022** (MSA file rev. 2025-07-22) | Same | US 45.9% (includes non-metro). Micro areas. |
| **13.3%** | US workers 16+ who **usually** worked from home (journey-to-work) | ACS **2024** B08301 | `Analysis/work-from-home/out/summary.json` | ATUS 32.5%. ABS 35.8 / 77.5. |
| **DC 22.9% · MS 6.2%** | Highest / lowest ACS usual-WFH | ACS **2024** | Same | ATUS occupation cuts. |
| **32.5%** | Employed persons who did **any** work at home on an average day worked | ATUS **2024** | BLS ATUS news release | ACS usual-WFH. Do not put on the same unlabeled bar. |
| **35.8% / 77.5%** | Share of **firms** (&lt;500 / 500+) that **had any** WFH employees | ABS **2023** | Census ABS AB2300CSCB04 | Worker telework rate. SUSB employment mix. |
| **19 / 27 / 5** | States (+DC) where Charter / Comcast / neither has the larger **residential location** count | FCC BDC **31 Dec 2025** (D25, rev. 15 Sep 2026) | `Analysis/cable-share-small-firm/out/summary.json` | **Subscriber** share. Internet net adds. M5. |
| **$93.8B · 4.18x** | Principal debt and net leverage | **30 Jun 2026** | Ex99.1 / 10-Q Q2 2026 (later public fact vs Q1 course anchor); `chtr-ehb-economies-of-scale` | Cox $12.6B. Rural remainder. |
| **44%** | Top-10 share of US health-and-welfare **Form 5500 compensation** (PlanOptica) | PlanOptica table used in M2 | `Analysis/ehb-broker-metrics/m2/out/summary.json` | Covered **lives** (M2 specified unit — still blank). BI revenue ranks. |
| **M13 = P − E − D** | Path-tagged residential Internet provisions minus already-Spectrum minus same-window job-exit disconnects | Channel: **blank** | `Analysis/ehb-broker-metrics/m13/assumption_register.csv` | Enrollments. Passings. Reach. |
| **−117k** | Company **residential** Internet quarterly net additions | Q1 **2026** | Ex99.1; M13 canvas / register X1 | Channel M13. Company **total** Internet **−120k** (−117k res + −3k SMB). |
| **M5 = no number** | Serviceable-home share of **enrolled employees** | — | `Analysis/ehb-broker-metrics/m5/out/summary.json` | Anything below. |
| **94.6%** | Share of 2022 SUSB **jobs** in the 42 jurisdictions with **any** Charter residential BDC filing | Jobs 2022 × plant 31 Dec 2025 | M5 summary C4 | **Not M5.** Not employee homes. Not a broker book. Biased high. |

---

## Slide rules for other agents

- One message per slide. Takeaway title = finding + direction + magnitude.
- One accent color; everything else gray. Bars begin at zero. No pie. No dual axis.
- Never put ACS WFH, ATUS, and ABS on one comparison without labeling **different questions**.
- Never treat SUSB employment as broker-placed lives (not M1, not M2 lives).
- Never treat FCC locations as subscribers.
- The EH&B analogy holds only if a **residential Spectrum Internet** account opens (**M13**). Productivity is the pitch, not the KPI.
- Official Rec 1 sequence still: fill the net-loss tracker first, then one reason-play on existing-plant core. This channel is a candidate play, not a replacement.
- **Kill** (stop the slide / stop the pitch): no broker authority; no serviceable home; M13 ≈ 0 because all P is E or D; no employer will fund or ballot.
- Do not invent take-up, commissions, serviceable %, or channel net adds.
- Copyright: do not paste sell-side research. Analysts are listed in `Analysis/sellside-coverage/`.

### Unwilling to claim (lock)

- Any Charter internet-as-benefit take-up rate.
- An M1 lives % or an M2 lives-concentration %.
- An employee-level M5.
- Channel M13, or that this path closes any share of −117k / −120k.
- That 94.6% jobs-in-42-states is serviceable-home share.
- A Charter footprint filter on SUSB metros (official 41-state list not in repo; M5 uses 42 BDC-present jurisdictions — do not silently equate them).
)
