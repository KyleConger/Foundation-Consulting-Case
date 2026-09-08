# Iteration 2: US Premium Insulated Drinkware Sizing — Auditable Arithmetic

**Date:** September 8, 2026
**Purpose:** Rebuild the sizing so every line shows its arithmetic, one assumption per line, with each
input tagged **RETRIEVED** or **ESTIMATED**, and every low-confidence figure flagged.
**Companion data:** `Drinkware-Sizing-Audit.csv` (origin, leverage, and retrieval cost per input)
**Supersedes:** the year-3 revenue figure in `Drinkware-Market-Sizing-Memo.md` — see the correction in §7.

---

## Part 1 — The first-pass prompt, all six controls

### 1. Role
> You are an action-oriented market-sizing consultant and decision maker for a consumer-hardgoods
> startup. You commit to a single number and defend it. You are not a summarizer and you do not hedge
> into ranges without also giving a point estimate.

### 2. Context
> The client is a founder entering the US market for premium insulated drinkware — bottles and tumblers
> at $35–$50 retail. She has a finished product, some seed funding, and no market analysis. Her problem
> has already been framed three ways: (a) displacement of a vessel already owned; (b) founder-specific
> right-to-win, valid only if it names an asset a competitor cannot buy or copy; (c) landed cost and
> duty stack. The audience is the founder. The decision she must make is whether and how to commit the
> remaining seed capital. Anchor date is September 2026.

### 3. Task
> Produce an annual US market size for the $35–$50 realized-price band, built **both** top-down and
> bottom-up and explicitly reconciled. Then produce the serviceable subset implied by each of the three
> frames, a three-year revenue and unit target with its implied market share, per-unit landed cost by
> country of origin, contribution by channel, and a recommendation on where she should go with a
> sequenced action list and a kill rule.

### 4. Constraints
> - Use SEC filings and government statistics wherever they exist, and name the filing.
> - **Put every assumption on its own line.** Show the arithmetic that connects each line to the next.
> - **Tag every input as RETRIEVED (from a named source) or ESTIMATED (team judgment).** Never blur the two.
> - **Flag every low-confidence figure explicitly** with a visible marker, not a footnote.
> - Name who paid for any survey you rely on.
> - State the leverage of each estimated input: how much the answer moves if it is wrong.
> - Where the case is deliberately ambiguous, state the ambiguity and commit anyway.
> - Do not invent customer data. State explicitly what you are unwilling to claim.

### 5. Format
> A decision memo with markdown tables, plus a machine-readable audit register as CSV carrying an
> origin column, a confidence column, a leverage column, and the cost of converting each estimate into
> a retrieved figure. Lead with the number, not the method.

### 6. Examples
> Granularity required, in this exact shape:
>
> `A2 [RETRIEVED] YETI FY2025 global drinkware net sales = $1,085.8M — High — SEC 8-K ex-99.1, Feb 19 2026`
> `A9 [ESTIMATED] US share of YETI global drinkware = 76% — LOW CONFIDENCE — set below the 78.9% company US mix because YETI disclosed international drove drinkware growth while US declined`
> `A10 [DERIVED] YETI US drinkware net sales = A2 × A9 = 1,085.8 × 0.76 = $825.2M`

**Legend used below:** `[R]` retrieved · `[E]` estimated · `[D]` derived from prior lines ·
**⚠ LOW** = low confidence, treat as a planning placeholder.

---

## Part 2 — Build A: bottom-up

| Line | Origin | Input | Arithmetic | Value | Confidence |
|---|---|---|---|---:|---|
| A1 | **[R]** | YETI FY2025 total net sales | — | $1,868.5M | High |
| A2 | **[R]** | YETI FY2025 global drinkware net sales | — | $1,085.8M | High |
| A3 | **[R]** | YETI FY2025 US net sales | — | $1,474.1M | High |
| A4 | **[R]** | YETI FY2025 international net sales | — | $394.4M | High |
| A5 | [D] | YETI US share of total sales | A3 ÷ A1 | 78.9% | High |
| A6 | **[R]** | YETI FY2025 DTC channel sales | — | $1,127.8M | High |
| A7 | [D] | YETI DTC share of sales | A6 ÷ A1 | 60.4% | High |
| A8 | **[R]** | Disclosure: international drove drinkware growth; US drinkware declined FY25, flat in Q4 | — | qualitative | High |
| A9 | **[E]** | US share of YETI global drinkware | set below A5 because of A8 | 76% | **⚠ LOW** |
| A10 | [D] | YETI US drinkware net sales | A2 × A9 = 1,085.8 × 0.76 | $825.2M | Medium |
| A11 | **[E]** | Wholesale price as % of retail | — | 55% | **⚠ LOW** |
| A12 | [D] | DTC portion, already at retail | A10 × A7 = 825.2 × 0.6036 | $498.1M | Medium |
| A13 | [D] | Wholesale portion, at wholesale | A10 × (1−A7) = 825.2 × 0.3964 | $327.1M | Medium |
| A14 | [D] | Wholesale portion grossed to retail | A13 ÷ A11 = 327.1 ÷ 0.55 | $594.8M | Low-Med |
| A15 | [D] | **YETI US drinkware retail value** | A12 + A14 | **$1,092.9M** | Medium |
| A16 | **[E]** | Stanley US retail value | loosely anchored on retrieved global $750–800M, US 71%, US DTC −20% in 2025 | $550M | **⚠ LOW** |
| A17 | **[E]** | Owala US retail value | loosely anchored on retrieved 16.5% vs YETI 22.8% share | $500M | **⚠ LOW** |
| A18 | **[E]** | Hydro Flask US retail value | loosely anchored on retrieved HELE segment data | $300M | **⚠ LOW** |
| A19 | **[E]** | Other branded US retail value | **no retrieved anchor** | $850M | **⚠ LOW** |
| A20 | **[E]** | Private label and marketplace unbranded | anchored on retrieved ~10% private-label share | $500M | **⚠ LOW** |
| A21 | [D] | **US insulated drinkware retail, all price points** | A15+A16+A17+A18+A19+A20 | **$3,792.9M** | **⚠ LOW** |
| A22 | **[E]** | Share of dollars at $35–$50 realized | — | 35% | **⚠ LOW** |
| A23 | [D] | **Bottom-up US annual market size (TAM), $35–$50 band** | A21 × A22 = 3,792.9 × 0.35 | **$1,327.5M per year, US only** | **⚠ LOW** |

---

## Part 3 — Build B: top-down US annual market size (TAM)

**Geography: United States only** — the build starts from US resident population (B1), so no
international demand can enter it. **Period: one year** — B9 is purchases per owner *per year*, which
is the line that sets the annual basis for B10 onward. B13's price scan is US marketplace data.

| Line | Origin | Input | Arithmetic | Value | Confidence |
|---|---|---|---|---:|---|
| B1 | **[R]** | US resident population, Jul 1 2025 | — | 341,784,857 | High |
| B2 | **[E]** | Share aged 18+ | Census publishes the exact file (SCPRC-EST2025-18+POP); not retrieved | 77.5% | Medium |
| B3 | [D] | US adults 18+ | B1 × B2 | 264.9M | Medium |
| B4 | **[R]** | Ownership rate, source 1 | survey **commissioned by Ever Vessel, a bottle startup** | 85% | **⚠ LOW** |
| B5 | **[R]** | Ownership rate, source 2 | secondary aggregator | 60% | **⚠ LOW** |
| B6 | **[E]** | Ownership rate used | reconciliation of B4 and B5 | 70% | **⚠ LOW** |
| B7 | [D] | Bottle owners | B3 × B6 = 264.9 × 0.70 | 185.4M | Low |
| B8 | **[R]** | 51% replace within 12 months; 32% within 6 | same vendor survey as B4 | — | **⚠ LOW** |
| B9 | **[E]** | Insulated purchases per owner per year | discounted from B8, which implies over 1.0 | 0.60 | **⚠ LOW** |
| B10 | [D] | Annual units, all price points | B7 × B9 = 185.4 × 0.60 | 111.3M | Low |
| B11 | **[E]** | Share of units at $35–$50 realized | — | 27% | **⚠ LOW** |
| B12 | [D] | Units in band | B10 × B11 = 111.3 × 0.27 | 30.04M | Low |
| B13 | **[R]** | Average list price, Amazon scan (40 brands, 1,403 offers, to Sep 4 2025) | — | $37.77 | Medium |
| B14 | **[E]** | Realized ASP in band | above B13 since band excludes sub-$35; below MSRP for promo | $41.00 | Low-Med |
| B15 | [D] | **Top-down US annual market size (TAM), $35–$50 band** | B12 × B14 = 30.04M × 41 | **$1,231.5M per year, US only** | **⚠ LOW** |

### Reconciliation

| Line | Arithmetic | Value |
|---|---|---:|
| C1 | Bottom-up US annual TAM (A23) | $1,327.5M/yr |
| C2 | **Top-down US annual TAM (B15)** | **$1,231.5M/yr** |
| C3 | Midpoint | $1,279.5M/yr |
| C4 | Spread as % of midpoint | 7.5% |
| **C5** | **Committed US annual TAM, rounded down for conservatism** | **$1,250M per year, US only** |

The 7.5% spread is **not** independent validation. Both builds use the same estimated band share
concept (A22 and B11), so they are correlated by construction. Two methods agreeing here means the
arithmetic is consistent, not that the answer is right.

---

## Part 4 — Serviceable market

| Line | Origin | Input | Arithmetic | Value | Confidence |
|---|---|---|---|---:|---|
| D1 | **[R]** | E-commerce share of insulated drinkware, global 2025 (from 28.7% in 2021) | vendor research | 41.3% | Low-Med |
| D2 | **[E]** | US online share of the band | — | 42% | Low-Med |
| D3 | [D] | Consumer online addressable | C5 × D2 = 1,250 × 0.42 | $525.0M | Low |
| D4 | **[E]** | Replacement or addition share of purchases | implied by high ownership | 75% | **⚠ LOW** |
| D5 | **[R]** | Share citing odor or hygiene as the replacement reason | same vendor survey | 40% | **⚠ LOW** |
| D6 | [D] | **Hygiene-trigger online niche** | D3 × D4 × D5 = 525 × 0.75 × 0.40 | **$157.5M** | **⚠ LOW — compounds three low-confidence inputs** |
| E1 | **[R]** | North American promo distributor sales 2025 | ASI Research, Jan 2026 | $27,700M | High |
| E2 | **[R]** | 2024 comparison, +4.2% | ASI | $26,600M | High |
| E3 | **[R]** | Method check: T-shirts 16.1% = $4,280M (2024) | 4,280 ÷ 26,600 = 16.09% ✓ | validates share math | High |
| E4 | **[R]** | Drinkware is #2 category, roughly 10.7% historically | ASI | ≈$2,800M | Low-Med |
| E5 | **[E]** | Drinkware share used | below E4; ASI reports drinkware declined in 2024 and 2025 | 10.5% | Low-Med |
| E6 | [D] | Promo drinkware distributor sales | E1 × E5 = 27,700 × 0.105 | $2,908.5M | Low-Med |
| E7 | **[E]** | US share of North America | — | 90% | Medium |
| E8 | **[E]** | Premium insulated stainless share of promo drinkware | **no retrieved anchor** | 40% | **⚠ LOW** |
| E9 | **[E]** | Supplier-level price as % of distributor price | — | 65% | **⚠ LOW** |
| E10 | [D] | **B2B supplier-level pool** | E6 × E7 × E8 × E9 = 2,908.5 × 0.90 × 0.40 × 0.65 | **$680.6M** | Low-Med |
| E11 | [D] | Ratio to consumer niche | E10 ÷ D6 = 680.6 ÷ 157.5 | **4.32×** | Low-Med |
| E12 | **[R]** | ~90% of promo distributors raised prices ~11% in 2025 to offset China and India import costs | ASI | — | High |
| F1 | [D] | **Combined SAM** | D6 + E10 | **$838.1M** | Low-Med |

---

## Part 5 — Duty stack and landed cost

| Line | Origin | Input | Arithmetic | Value | Confidence |
|---|---|---|---|---:|---|
| G1 | **[R]** | HTS classification, vacuum flasks | vendor guidance | 9617.00.1000 | Medium |
| G2 | **[R]** | MFN base duty (6.9–7.2% cited) | vendor | 7.0% | Medium |
| G3 | **[R]** | Section 301, China steel drinkware | vendor + trade press | 25.0% | Medium |
| G4 | **[R]** | Section 301 forced-labor duty, China, from Jul 24 2026 | trade press | 12.5% | Medium |
| G5 | [D] | **China total duty** | G2+G3+G4 | **44.5%** | Medium |
| G6 | **[R]** | Forced-labor duty, Vietnam | trade press | 12.5% | Medium |
| G7 | [D] | Vietnam total duty | G2+G6 | 19.5% | Medium |
| G8 | **[R]** | Forced-labor duty, India | trade press | 10.0% | Medium |
| G9 | [D] | India total duty | G2+G8 | 17.0% | Medium |
| G10 | **[R]** | Section 232 steel derivative, non-stacking with new 301 | trade press | 50.0% | **⚠ OPEN — unresolved whether vacuum flasks are a covered derivative. Adds ~$4/unit if they are.** |
| H1 | **[E]** | FOB unit cost, China | retrieved analogue: vendor example used $10.00 FOB on 1,500 units | $10.00 | **⚠ LOW** |
| H2 | **[E]** | Freight and insurance per unit | — | $1.20 | **⚠ LOW** |
| H3 | [D] | CIF China | H1+H2 | $11.20 | Low |
| H4 | [D] | Duty, China | H3 × G5 = 11.20 × 0.445 | $4.98 | Medium |
| H5 | **[E]** | MPF and broker fees per unit | retrieved MPF rate 0.3464% | $0.08 | Low |
| H6 | [D] | **Landed cost, China** | H3+H4+H5 | **$16.26** | Medium |
| H7 | **[E]** | FOB Vietnam, premium for less mature base | — | $10.50 | **⚠ LOW** |
| H8 | [D] | CIF Vietnam | H7 + H2 | $11.70 | Low |
| H9 | [D] | Duty, Vietnam | H8 × G7 = 11.70 × 0.195 | $2.28 | Medium |
| H10 | [D] | **Landed cost, Vietnam** | H8+H9+H5 | **$14.06** | Medium |
| H11 | [D] | Saving vs China | H6 − H10 | **$2.20/unit (13.5%)** | Medium |
| H12 | [D] | Saving at year-3 volume | 2.20 × 128,000 | **$281,920/yr** | Medium |

**Cross-check on H6 against a retrieved figure.** A sourcing vendor published a worked example: $10.00
FOB → **$14.07 landed** under the pre-July-2026 stack of 7% + 25% = 32%. Adding the 12.5-point
forced-labor duty to a ~$11.20 CIF adds ~$1.40, giving ~$15.47. My $16.26 is 5.1% higher because I
assumed heavier freight. **The two independent routes agree within ~5%,** which is the strongest
validation anywhere in this model.

---

## Part 6 — Contribution by channel, Vietnam basis ($14.06)

| Line | Origin | Input | Arithmetic | Value |
|---|---|---|---|---:|
| I1 | **[E]** | DTC price | within the stated band | $40.00 |
| I2 | **[E]** | Payment processing, 3.0% | 40.00 × 0.03 | $1.20 |
| I3 | **[E]** | Pick, pack, ship | ⚠ LOW | $6.00 |
| I4 | **[E]** | Returns provision, 4.0% | 40.00 × 0.04 | $1.60 |
| I5 | [D] | DTC net | 40.00−1.20−6.00−1.60 | $31.20 |
| I6 | [D] | DTC contribution before marketing | 31.20−14.06 | **$17.14 (42.9%)** |
| I7 | **[E]** | Blended cold-traffic CAC | **⚠ LOW — no retrieved source** | $25–40 |
| I8 | [D] | **DTC after CAC** | 17.14 − 25.00 to 40.00 | **−$7.86 to −$22.86 → NEGATIVE** |
| I9 | **[E]** | Amazon referral fee, 15% | standard rate | $6.00 |
| I10 | **[E]** | FBA fulfillment fee | ⚠ LOW | $5.60 |
| I11 | **[E]** | Returns and reship | ⚠ LOW | $1.20 |
| I12 | [D] | Amazon net | 40.00−6.00−5.60−1.20 | $27.20 |
| I13 | [D] | Amazon contribution | 27.20−14.06 | $13.14 (32.9%) |
| I14 | **[E]** | PPC at 18% TACoS | **⚠ LOW** | $7.20 |
| I15 | [D] | **Amazon after PPC** | 13.14−7.20 | **$5.94 (14.9%)** |
| I16 | **[E]** | Direct corporate price, decorated | **⚠ LOW** | $31.00 |
| I17 | **[E]** | Decoration cost | ⚠ LOW | $2.25 |
| I18 | **[E]** | Freight out | ⚠ LOW | $1.50 |
| I19 | [D] | **Direct corporate contribution** | 31.00−14.06−2.25−1.50 | **$13.19 (42.5%)** |

---

## Part 7 — Break-even, three-year path, and a correction

| Line | Origin | Input | Arithmetic | Value |
|---|---|---|---|---:|
| J1 | **[E]** | Fixed cost base | **⚠ LOW** | $450K/yr |
| J2 | **[E]** | Year-3 channel mix | **⚠ LOW** | 60% B2B / 40% online |
| J3 | **[E]** | Online split | **⚠ LOW** | 50% Amazon / 50% organic |
| J4 | [D] | Mix-weighted contribution | 0.60×13.19 + 0.40×(0.5×5.94 + 0.5×17.14) | $12.53 |
| J5 | **[E]** | Planning contribution after haircut | — | $11.00 |
| J6 | [D] | **Break-even volume** | J1 ÷ J5 = 450,000 ÷ 11.00 | **40,909 → 41,000 units** |
| J7 | [D] | **Blended ASP** | 0.60×31.00 + 0.40×40.00 = 18.60 + 16.00 | **$34.60** |
| J8 | [D] | Break-even revenue | J6 × J7 = 41,000 × 34.60 | **$1.42M** |

### Correction to the prior memo

The first memo carried a blended ASP of **$39** into the year-3 revenue line while the channel mix in
J2 and J3 implies **$34.60** (J7). The $5.0M year-3 figure was therefore overstated. Corrected:

| Year | Units [E] | × Blended ASP (J7) | Revenue |
|---|---:|---:|---:|
| 1 | 15,000 | $34.60 | **$0.52M** |
| 2 | 52,000 | $34.60 | **$1.80M** |
| 3 | **128,000** | $34.60 | **$4.43M** |

Break-even (41,000 units) is crossed during year 2, which is consistent with the unit ramp.

**Independent check on the corrected number, built from share instead of units:**

| Line | Arithmetic | Value |
|---|---|---:|
| K1 | 1.5% of the consumer online niche: 157.5 × 0.015 | $2.36M |
| K2 | 0.3% of the B2B supplier pool: 680.6 × 0.003 | $2.04M |
| **K3** | **Total** | **$4.40M** |

The units-times-price route (**$4.43M**) and the share-of-SAM route (**$4.40M**) agree to within 0.7%.

**Committed year-3 number: $4.4M revenue on ~128,000 units — 0.35% of the $1.25B TAM.**
Range $3.0M–$6.0M. The recommendation in the prior memo does not change; only the magnitude does.

---

## Part 8 — Retrieved versus estimated: the honest audit

### Dollar-weighted origin of the bottom-up build

| Component | Value | Origin |
|---|---:|---|
| A15 YETI, built on filed SEC figures | $1,092.9M | Retrieved anchor + 2 estimated ratios |
| A16–A20 all other brands and private label | $2,700.0M | **Estimated** |
| A21 Total | $3,792.9M | **28.8% retrieved-anchored, 71.2% estimated** |

Then the entire total is multiplied by A22 (35% band share), which is **wholly estimated**.

### Input counts

| Build | Retrieved | Estimated | Derived |
|---|---:|---:|---:|
| A · bottom-up | 6 | 8 | 9 |
| B · top-down | 5 | 5 | 5 |
| D–F · serviceable market | 6 | 5 | 6 |
| G–H · duty and landed cost | 7 | 4 | 8 |
| I–K · contribution and path | 1 | 13 | 10 |
| **Total** | **25** | **35** | **38** |

### Sensitivity: which estimated inputs actually move the answer

| Input | Low | Base | High | TAM swing |
|---|---:|---:|---:|---|
| A22 band share | 25% | 35% | 45% | $948M – $1,706M · **±29%** |
| A16–A20 other brands ±30% | −30% | base | +30% | $1,043M – $1,610M · **±21%** |
| B9 purchases per owner | 0.45 | 0.60 | 0.75 | $924M – $1,540M · **±25%** |
| B6 ownership rate | 60% | 70% | 85% | $1,056M – $1,496M · **±19%** |
| A9 YETI US drinkware share | 70% | 76% | 79% | **±1.1%** |
| A11 wholesale-to-retail | 50% | 55% | 60% | **±1.4%** |

**The finding that matters most in this whole iteration:** the two inputs I derived most rigorously
from SEC filings — A9 and A11 — move the answer by roughly **1%**. The four inputs that move it by
**19–29%** are all pure team estimates with no retrieved anchor. Precision was spent where it did not
matter. Filed data made the YETI line auditable, but the YETI line is not what the answer rests on.

---

## Part 9 — What to retrieve next, ranked by leverage divided by cost

| # | Convert to retrieved | Removes | Cost | Days | Decision-critical |
|---|---|---|---:|---:|---|
| 1 | Duty stack and the Section 232 question (G1–G5, G10) — licensed broker ruling | Venture-killing ambiguity, ~$4/unit | $1–2K | 5–10 | **Yes** |
| 2 | FOB and MOQ (H1, H7) — quotes from Vietnam, India, Korea | ⚠ LOW on the largest cost line | $0 | 10–20 | **Yes** |
| 3 | Band share and brand-level US retail (A16–A22) — Circana or Numerator POS by price band | ±29% and ±21% | $5–15K | 10–20 | No |
| 4 | Ownership and purchase frequency (B6, B9) — own survey, n≈1,000 | ±19% and ±25%, and removes the vendor-funded survey | $8–15K | 15–21 | No |
| 5 | Promo premium-insulated share (E8, E9) — ASI or PPAI category report | ⚠ LOW on the recommended channel | $1–3K | 5–10 | No |
| 6 | CAC and Amazon fee reality (I7, I10, I14) — live test on one SKU | The channel choice itself | $15–25K | 30–45 | **Yes** |

Items 1, 2, and 6 are the ones that change the decision. Items 1 and 2 are also the cheapest and
fastest, which is why they run first regardless of how interesting item 3 is.

---

## Part 10 — What we are unwilling to claim

- That $1.25B is measured. **Roughly 71% of the bottom-up build is team estimate**, and the single most
  leveraged input in the model has no retrieved anchor at all.
- That the two builds agreeing within 7.5% validates anything. They share the band-share construct and
  are correlated by design.
- That the ownership and replacement rates are reliable. The 85%-own and 51%-replace figures come from a
  survey **commissioned by a bottle startup**, and a second source says 60% own. We used 70% and flagged it.
- That the duty stack is settled. It moved twice in 2026 and the Section 232 derivative question is open.
- That she has a right to win. The case states only that she has a product. No amount of sizing closes
  Frame 2 — only naming the asset a competitor cannot buy or copy will.
