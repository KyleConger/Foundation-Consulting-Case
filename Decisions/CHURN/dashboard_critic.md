# Critic — CHTR Rec 1 Attribution Dashboard

**Reviewed:** `Decisions/CHURN/CHTR Rec1 Attribution Dashboard.xlsx` (Dashboard first) and `Decisions/CHURN/build_attribution_dashboard.py`  
**Also read:** `CHTR_Rec1_AttributionPlaybook.pptx`, `Decisions/six-recommendation-areas.md`  
**Method:** openpyxl static pass + Excel COM calculate on a copy. Did not edit the xlsx.  
**Note:** a fixer is mid-flight. This is the live file at review time (xlsx and `.py` already diverge on a few formula guards). `verify()` in the builder will still **pass** most of what is wrong below.

**Empty-state Excel (Q1 2026 selected):** title = “Fill the quarterly net-loss tracker first”; print = (117,000); CMCSA = (65,000); excess = **54,440**; largest reason = EMPTY; scenario = HOLD; B29 = the fake Comcast sentence; bar chart = seven zeros on seven blank categories. No `#REF!` / `#VALUE!` / `#DIV/0!` on Dashboard. Intentional `#N/A` lives on tracker chart-feed rows 53–54. Assumptions!F9 is `#NAME?`.

What fails first for a Charter analyst: they open **Dashboard**, see −117k / −65k / 54,440 already filled, and a title that says the tracker is empty. There is nowhere yellow to paste. The first successful paste path (reason counts + T3, residual leftover) can **fire a play on Residual**.

---

## Findings

### 1. Blocker — Dashboard + Attribution — Residual can be the “dominant driver” and fire a play

**Wrong.** Sorted engine is seven rows (A1–A6 + residual). `C48` / `D48` / rank include residual. Takeaway C15: if residual is largest and ≥ P4, “Residual accounts for X% … **Fire that one play on the core.**” Lights go RED. Parameters itself says residual largest = incomplete sample, do not fire a plant program. PPTX Scenario 6 is the floor for a diffuse/unmapped file. Six-areas: do not fire a reason play from a bad fill.

**Fixed.** Residual is a data-quality flag, never a scenario key. Rank / MAX / “largest reason” use A1–A6 only. If residual share ≥ material (already ~2% FLAG), diagnosis = “sample incomplete — HOLD,” not S1–S5.

---

### 2. Blocker — Dashboard!B29 — fake multi-quarter vs-Comcast claim presented as the exhibit title

**Wrong.** `IF('Net-loss tracker'!J11="","…public spine…","Charter residential Internet stayed worse than Comcast in every quarter both prints exist")`. J11 is Q2 2025 print-used — always filled. Excel shows the second sentence on open. Comcast is retrieved for **one** quarter (Q1 2026). The sentence is not computed from overlapping pairs. That is a fact-shaped claim the public file does not support.

**Fixed.** Title is a formula over quarters where **both** T6 and T9 exist. One overlap → “Q1 2026: CHTR −117k vs CMCSA −65k (only quarter both prints exist).” Do not gate on J11. Or drop the comparison title until ≥2 overlapping quarters are entered.

---

### 3. Blocker — Dashboard bar chart — empty mix plots as seven zeros

**Wrong.** E20:F26 = `IFERROR(N(Attribution!E54:F60),0)`. Excel series values: `0|0|0|0|0|0|0` twice. Caption admits it. A zeroed rank chart is a measured mix of nothing. Template contract: no fake attribution as fact. Storytelling: one claim per chart — this chart’s claim on open is “no leaks.”

**Fixed.** Categories and values are `NA()` (or hide the chart) until `Attribution!C49="Yes"` **and** a real base exists. Zeros are for a filled zero cell, not for EMPTY.

---

### 4. Blocker — Attribution + Parameters — “Percent” mode does not accept percents

**Wrong.** P15 “Counts / Percent” only changes A9’s fallback base to `|T6|`. Yellow cells stay counts. Enter 40 or 0.40 and shares become `40/117000` or `0.40/117000`. There is no % grid and no “inputs are shares” branch. First analyst who believes the dropdown gets a silent wrong mix that can still clear 40% and fire.

**Fixed.** Either delete Percent mode or add a yellow % block that must sum to 100% and is clearly labeled PLACEHOLDER allocation of the print — and still cannot fire a scaled play (experiments only / HOLD).

---

### 5. Blocker — Dashboard!C16 — routes PPTX scenarios off reason shares, not the PPTX sensor

**Wrong.** Slide 4 sensor is exposure class (fiber-overbuilt / FWA-covered / satellite-only / uncontested) plus tenure, ARPU, audited exit. Slide 6–8 signals are FWA-**covered** losses, fiber-**DMA** losses, satellite-**only** blocks, move-out **plus** gross-adds-down, etc. C16 tests `INDEX(Attribution!D40:D45, n)` (reason-count shares) and a hardcoded `N(Segments!D71)>=0.3` for S1. Exposure rows 66–73 never touch the router. An analyst who fills the deck’s sensor and leaves reason codes empty gets HOLD. An analyst who fills reasons only can fire S1–S5. Inverted from the pptx.

Six-areas / GAP is reason-first (move-out / FWA / fiber / nonpay). The sheet labels the output “S1–S6” as if it were the deck.

**Fixed.** One router, one tree, labeled. Either: (A) pptx path — exposure shares vs uncontested + exit/tenure/ARPU corroborators, reason as audit; or (B) GAP path — R1–R4 reason, and do not call it Scenario 1–6. Do not OR them quietly. S1 price-exit 30% belongs on Parameters if it stays.

---

### 6. Major — Dashboard — empty-state title contradicts the KPIs

**Wrong.** Public spine is already in. Excel: −117,000 / −65,000 / 54,440. Row 2 still says fill the **tracker** first. Attribution is what is empty. An analyst will either ignore the title or think the template is already a filled diagnosis.

**Fixed.** “Public prints are retrieved. Attribution / disconnect sample is empty — the playbook does not fire.” Keep −117k / −166k as labeled RETRIEVED, not as a mix.

---

### 7. Major — Dashboard!H6 — 54,440 shown as the excess; playbook commits 54k

**Wrong.** T15 computes 117,000 − (65,000/28,719,000)×27,641,000 = 54,440. Subtitle says “Q1 playbook commit 54k.” Six-areas / `network_churn_model.py` **round down to 54,000**. The KPI is the unrounded identity sitting next to EMPTY reason — reads like a sized leak.

**Fixed.** Display the commit (P18 = 54,000) or `ROUNDDOWN` the identity, and subtitle “unallocated until first fill — not a cell in the mix.” Do not show 54,440 as if it were more true than the commit.

---

### 8. Major — Dashboard!C15 — “Fire that one play **on the core**” ignores WHERE

**Wrong.** Dominant takeaway always says “on the core.” F2 (Segments!C79) can say rural is the leak, or neither cut clears P10. Six-areas W1/W2 and kill 5: do not add rural miles to fix a core leak; do not fire the core play on a rural Internet hole.

**Fixed.** Dominant sentence reads F2. Core ≥ P10 → “on the core, no new miles.” Rural ≥ P10 → W2 language. WHERE empty → “WHERE untested — do not pick miles vs core yet.”

---

### 9. Major — Dashboard + Playbook sheet — two playbooks, one router

**Wrong.** C16 lead plays are pptx (convergence pricing, DOCSIS re-sequence, rural activation). Six-areas Area 2 / `decisions.md` GAP: TOS/MDU 6 months; 12-month FWA rate-lock on and off overlap; overlap gig/symmetry + node-split only if sample names speed; payment arrangement / 90-day first-bill. Playbook sheet has both, stacked. Dashboard fires the deck’s verbs. A Charter ops lead using six-areas will execute the wrong offer.

**Fixed.** Router text = the rec the case is actually taking (GAP if this is the six-areas template; pptx if this is Rec 1 the deck). The other set is reference, not the light.

---

### 10. Major — Parameters!C16 / Dashboard!K57 — two-quarter interlock is a toggle, not a test

**Wrong.** PPTX slide 11: full-scale needs **two consecutive quarters** over the threshold; experiments may start on one. K6 only echoes whether the user left P12 = Yes. One fat quarter still goes RED “fire one play.”

**Fixed.** Compare this quarter and prior quarter’s largest-share / scenario. One quarter → “EXPERIMENT ONLY.” Two consecutive → “FULL-SCALE armed.” Empty prior → not armed.

---

### 11. Major — Usability — Dashboard has zero INPUT cells; paste fails on protection

**Wrong.** Dashboard: yellow = 0, unlocked = 0, `ProtectContents=True` (no password). Analyst opens the first sheet and cannot type. Intended paste is tracker E7:P8, Attribution E6:P11, Segments grids. Cover explains; Dashboard does not. A block paste that includes locked label columns A–D is rejected. Tracker auto-filter is `$A$5:$P$5` (header only). Print areas cut the engines: tracker `A1:P32` (engine 32–48), Attribution `A1:P36` (shares / exposure / dashboard feed below), Segments `A1:P28` (ARPU / exit / flags below).

**Fixed.** Dashboard row 3 (or a banner): “Paste yellow on Net-loss tracker (T2/T3), Attribution (A1–A6), Segments. This sheet is output.” Unlock only yellow; document the start cell (E7 / E6 / E7). Filter `A5:P22`. Print areas include the input grid the analyst uses, or say “not a print sheet.”

---

### 12. Major — Storytelling — one sheet, four claims; empty title is a process note

**Wrong.** Last-mile / SwD: one message per exhibit; takeaway = finding + direction + magnitude. Live Dashboard is (1) process title, (2) three public KPIs + 54,440, (3) zeroed reason bars, (4) CHTR time series, (5) seven kill rules. Line chart has markers on every point. Bar/line have bottom legends. B29 is a topic/claim hybrid that is false. No pie, bars at zero (value axis min=0) — those two are fine.

**Fixed.** Dashboard exhibit = one sentence + one visual. Empty: **no chart**, KPI strip, HOLD. Filled: reason bars **or** CHTR vs CMCSA, not both. Kill rules appendix. Title is the diagnosis sentence only when a real mix exists.

---

### 13. Major — build_attribution_dashboard.py vs xlsx drift

**Wrong.** Live Dashboard!B18 and K13 still key off `C49="No"` only. The script now also guards `C48=""`. A rebuild and the file on disk will not match. `verify()` checks paren balance, no `NA()` **on Dashboard**, Dash_Print, freeze A4, prints −117k/−166k, yellow empty. It does not check residual exclusion, B29, Percent mode, exposure wiring, or 54k rounding. A green verify is not a working template.

**Fixed.** One source. Rebuild after every Dashboard edit, or stop editing the xlsx by hand. Extend `verify()` to the blockers above (and to `Assumptions!F9`).

---

### 14. Minor — Assumptions!F9 — `#NAME?`

**Wrong.** Citation text `=gross-disconnects` is stored as a formula. Excel: `#NAME?`.

**Fixed.** Plain text `'T2-T3` or `"T2 − T3"` without a leading `=`.

---

### 15. Minor — Dashboard layout / print / names / panes

**Wrong (not hiding content, still sloppy).** Freeze A4 is fine (SplitRow=3; KPIs start row 5). ~50 merges on KPI/diagnosis cards — any unprotect+sort wrecks the sheet. Line chart is oneCellAnchor at B36; kill block starts row 50 — tight on print. `fitToWidth=1` still squeezes 12 quarter columns. Named ranges exist; most formulas ignore them. P3 highlight hex is unused (charts hardcode `2E75B6`). Excess row 33 is on the sheet and not in the line chart (good) but looks like a third series.

**Fixed.** Fewer merges (cell styles, not 3-wide cards). Two-cell anchors so charts don’t cover the kill table when row heights change. Print to the chart+diagnosis, kills on page 2. Either use names everywhere or drop them.

---

### 16. Minor — playbook gaps that are labeled but still leak

**Wrong.** Satellite 25% is a template default (deck has no cut) — OK if ESTIMATED stays loud. S4 does not test “gross adds down / competitor churn flat.” S2 does not test overlap WHERE. Rural CR +41k/+47k is correctly **not** T6. Company −120k/−172k is correctly off the KPI. Agent codes are a process kill (K4) with no cell — acceptable. Mobile-offset refusal is only in K7 prose, not a light.

**Fixed.** Optional: a standing K8 “do not credit mobile / video against this print.” Keep rural CR in a clearly non-T6 box (already true).

---

## What is already true (do not “fix” these)

- Yellow INPUT on tracker T2/T3, Attribution A1–A6, Segments cuts are empty. Public −117,000 / −166,000 are green RETRIEVED. Empty scenario is HOLD. K2 untested until a fill. No pie. Bar value axis starts at 0. Rural CR is not the Internet print. Cover’s client question matches six-areas. Unbalanced C16/K51 that previously broke parse appear **fixed** in the live file (re-verify after the next rebuild).

---

## Fixer list (same findings, short)

1. **Blocker / Attribution+Dashboard** — Residual must not win rank / C48 / “fire that play.” HOLD if residual is largest or material.  
2. **Blocker / Dashboard!B29** — Stop gating a vs-Comcast story on J11. Title only from quarters where both prints exist (today: one quarter).  
3. **Blocker / Dashboard E20:F26** — Do not plot EMPTY as zeros. `NA()` or hide chart until a real mix+base.  
4. **Blocker / Parameters P15** — Percent mode is a trap (no % inputs). Remove or build a real share block that cannot fire at scale.  
5. **Blocker / C16** — Router is reason-share labeled as pptx S1–S6. Pick exposure-sensor (deck) or R1–R4 (GAP). Wire that tree only.  
6. **Major / B2·C15** — Empty title must say attribution/sample is empty, not “fill the tracker” while −117k is on the page.  
7. **Major / H6** — Show committed 54k, labeled unallocated — not 54,440 as a leak.  
8. **Major / C15** — Do not append “on the core” unless F2 says core.  
9. **Major / Playbook text** — Dashboard verbs must match the rec in force (GAP vs pptx), not both.  
10. **Major / K6** — Two-quarter test, not a Yes/No parameter echo.  
11. **Major / UX** — Paste banner, unlock yellow only, filter+print areas that include the input grids.  
12. **Major / Story** — One claim, one chart; no chart when EMPTY; kills off the exhibit.  
13. **Major / process** — xlsx and `.py` have drifted; `verify()` is a false green. Rebuild from one source; test residual / B29 / Percent / zeros.  
14. **Minor / Assumptions!F9** — `#NAME?` from `=gross-disconnects`.  
15. **Minor / layout** — merge sprawl, print squeeze, unused names, unused P3 hex.  
16. **Minor / fidelity** — S4/S2 missing corroborators; optional mobile-offset light.
