# Small-fiber licensing cost (solving)

**Status:** analysis with a recommendation · does not overwrite GAP, `six-recommendation-areas.md` (54k / −66k), or `ifxy-stock-signal.md`  
**Anchor:** end Q1 2026 · Q2 labeled later public fact  
**Canvas:** [chtr-small-fiber-licensing-cost](C:/Users/Owner/.cursor/projects/c-Users-Owner-Desktop-MAN6930-Case/canvases/chtr-small-fiber-licensing-cost.canvas.tsx)  
**Model:** `Decisions/small_fiber_licensing_model.py` (recomputed; numbers below match the run)

---

## Headline

**$650 per customer-year to lease last-mile on smaller fiber (range $360–$1,404), 20-year PV $6,400 per connected home. Gigabit wholesale is 82% of Charter’s $790 Internet ARPU and leaves −$79 per sub-year after care, residual field, transit, and SAC. Cheaper than rural overbuild on access ($6,400 vs $15,486 per customer). Not a customer-performance fix, because COGS eats contribution.**

Charter-footprint small-fiber passings are **not disclosed**. That is the blocking input on any *scaled* dollar total. The unit costs still stand. Scenario overlapping homes: **200k / 500k / 2.0M**. At base 500k homes and a 40% take with Charter as the only ISP (upper bound), annual COGS is **$130M** on 200k customers — 1.1% of FY2025 capex **$11.7B**, versus a Q1 upgrade/rebuild increment of **$280M**.

Frame B inputs that produce −$79 are **93% retrieved-anchored / 7% estimated** (dollar-weighted). Any scaled total is **100% estimated**, because the homes are unretrieved.

---

## Deal definition

“Licensing deals on the smaller fiber networks” here means Charter paying for **wholesale / open-access / IRU last-mile access** on *non-AT&T / non-Verizon* fiber — munis, independents, regional overbuilders, electric co-ops — so Spectrum can sell Internet on plant it does not own.

It is **not** content licensing, **not** brand licensing, and **not** “license Spectrum onto Cox” (already Area 5 in `six-recommendation-areas.md`).

It is **not** AT&T ~27% or Verizon ~16% of Charter’s footprint. Those are the large overbuilders (FY2025 10-K: terrestrial 100 Mbps+ competition). Smaller = everyone else in the 10-K competitive set: municipal WiFi, open-access networks, other FTTH.

**Rival mechanism (named, not the headline).** FY2024 10-K listed Frontier as a primary FTTH competitor. FY2025 dropped Frontier from “primary.” Frontier had **8.8M** fiber locations at Q3 2025 and **closed into Verizon on 20 January 2026**. At the Q1 2026 anchor that plant is Verizon, not “smaller,” and Verizon will not wholesale last-mile to Charter. Content/brand licensing is a different product and is not sized here.

NTIA’s June 2025 BEAD restructuring **eliminated** the NOFO’s non-statutory open-access / wholesale last-mile encouragement. Middle-mile interconnection remains a statutory remnant. Charter cannot count on BEAD to force last-mile access.

---

## Each frame’s own number

| Frame | What it measures | Point estimate | Range |
|---|---|---:|---:|
| **A** | 20-year PV of lit last-mile access **per connected home** @ 8% | **$6,400** | Dark-IRU cross-check **$600/passing** (different product); plant-IRU **$2,560/passing** at 40% take |
| **B** | Wholesale COGS **per customer-year** vs Internet ARPU / contribution | **$650 COGS → −$79 contribution** | COGS $360–$1,404; contribution **+$212 to −$832** |

The frames disagree about *access cost versus rural build* (A says cheaper) and *whether the deal earns money* (B says no). That disagreement is the finding. Size is not opportunity.

---

## Kill rule (before the recommendation)

Do **not** fund a small-fiber licensing program if **any** of these hold:

1. Public gigabit wholesale MRC stays at or above **$54/month** ($650/year) **and** Charter’s Internet ARPU on those homes stays at or below **$790/year** — contribution after remaining opex is negative.  
2. The counterparty is a **closed retail** network (MetroNet, Kinetic, Brightspeed, Google Fiber, co-op retail, EPB-style muni) that will not sell last-mile to Spectrum. No tariff, no deal.  
3. The fill of the net-loss tracker (Area 1) does **not** name small-fiber overlap as the leak. This is not a substitute for the 54k / −66k core play.  
4. A live tariff in a Charter-overlap open-access network is **not** at or below **~$32.50/month** (Grant PUD 100 Mbps analog) **with** a Spectrum price that still clears remaining opex (~$218/year).

If (1)–(4) all fail — i.e. a PUD/open-access gigabit tariff prints below ~$35/month, the network overlaps or sits adjacent to Charter, and the owner will transact — a **local pilot** can be sized. That is not this memo’s program.

---

## Unwilling to claim

- A Charter-footprint small-fiber passing count. The 10-K does not give one. National × housing-unit share is **not** overlap.  
- That AT&T 27% / Verizon 16% is the addressable set.  
- That two builds agreeing on arithmetic validates the market. Lit PV and Frame B COGS **share** the Jefferson $54 MRC (correlation by construction). The dark-IRU route does **not** share that input and disagrees by an order of magnitude because it is spare-strand middle-mile, not lit last-mile.  
- That MetroNet / Kinetic / Brightspeed / co-op retail will wholesale to Charter.  
- That BEAD still requires open-access last-mile (NTIA removed that in June 2025).  
- That this closes 54k Internet customers or changes the −66k print claim. Putting the 54k cohort on wholesale would cost **$35.1M/year** COGS and **−$4.2M/year** contribution.  
- Product-level Internet contribution as a filing fact. Remaining opex uses retrieved care/field totals allocated by customer relationship, plus estimated residual field / transit / SAC.  
- That dark-fiber IRU at **$600/passing** is a substitute for last-mile access to the home.

---

## Recommendation

**Do not pursue licensing deals on smaller fiber networks as a Q1 Internet-print or customer-performance play.** Public gigabit wholesale tariffs consume 82% of Internet ARPU before Charter has paid care, a CPE truck, or a save desk. The deal is cheaper than building rural plant (**$6,400 vs $15,486 per customer**) and still loses money on the customer. Sequence is unchanged: tracker first; one core reason-play; capex mix; rural take-not-miles. If an open-access PUD in the footprint posts a Grant-100-like tariff, size that one network as a pilot — do not scale from this memo.

---

## Frame B — wholesale COGS vs contribution

Point estimate **$650/customer-year** wholesale, **−$79** contribution. Round: COGS up from $648; ARPU down from $790.26; contribution more negative than −$78.36.

### ARPU (retrieved ÷ retrieved)

| ID | Line | Figure | Tag |
|---|---|---:|---|
| A7 | Q1 2026 Internet revenue | $5,852M | RETRIEVED · Ex99.1 |
| B1 | Avg total Internet customers Q1 | 29,620,000 | DERIVED · YE 29,680k / EOP 29,560k |
| B2 | Internet ARPU | **$65.86/mo** | DERIVED retrieved/retrieved |
| B3 | ×12 | $790.26/year | DERIVED |
| B6 | **Commit ARPU** (round down) | **$790/year** | COMMIT |
| B4 | Same $ / residential Internet customers | $70.72/mo · $849/year | DERIVED; matches `customer-performance.md`. Higher ARPU; not used for the commit (would help the deal). |

### Wholesale analogs (public tariffs; operator/ratepayer-funded, not vendor surveys)

| ID | Analog | MRC | $/year | Who paid for the number |
|---|---|---:|---:|---|
| B9 / B13 | UTOPIA Fiber infrastructure (customer-billed unless Charter absorbs) | $30 | $360 | UTOPIA public pricing (member cities) |
| W1 | Grant PUD Rate Schedule 100, 100 Mbps, Res. 9058, eff. 1 Aug 2024 | $32.50 | $390 | Grant PUD tariff |
| B7 | Grant PUD gigabit access | $52.50 | $630 | Grant PUD tariff |
| B8 / B11 | Jefferson County PUD wholesale PON 1 Gbps (2025 rates) | $54 | $648 | Jefferson PUD tariff |
| B10 / B14 | Jefferson wholesale PON 3 Gbps | $117 | $1,404 | Jefferson PUD tariff |

**B12 commit $650/year** = Jefferson $54 × 12, rounded up. Higher of the two gigabit wholesale tariffs. Grant + $10 premium support is $62.50/mo and would make the deal worse; not stacked onto Jefferson.

UTOPIA’s $30 is billed to the *customer*, with the ISP charging ~$35–$50 on top. If Charter absorbs it to keep a single Spectrum bill, COGS is $360/year and contribution turns **+$212** (B24) — the only analog that clears. That is not gigabit wholesale on a PUD; it is a two-bill open-access model that either raises the customer’s total price or compresses Charter’s retail.

### Remaining opex (last-mile rented)

| ID | Line | Figure | Tag |
|---|---|---:|---|
| A9 → B15 | Q1 customer ops $766M × 4 | $3,064M | RETRIEVED · Ex99.1 |
| B16 | Care/billing per CR-year | $96.71 | DERIVED retrieved/retrieved · / 31,683k CR |
| A10 → B17 | Field ops annualized / CR | $159 | DERIVED retrieved/retrieved |
| B18 | Residual field (30% of B17) | $47.65 | **ESTIMATED** · CPE truck / WiFi remain |
| B19 | Incremental transit / NNI | $24 | **ESTIMATED** · Charter already has a national backbone |
| B20 | SAC amortization | $50 | **ESTIMATED** · $150 / 3-year life, rounded up |
| B21 | Remaining opex | **$218/year** | mixed |

On owned plant, last-mile is mostly capex (D&A), not COGS. Renting last-mile at $650/year replaces ~$159 of field opex with a $650 invoice. That is why contribution goes negative even though rural construction looks expensive.

### Contribution

| ID | Line | Figure |
|---|---|---:|
| B22 | Gross after wholesale ($790 − $650) | $140 |
| B23 | After remaining opex | **−$78.36** |
| B26 | **Commit** (round against) | **−$79 / sub-year** |
| B27 | Wholesale / ARPU | **82%** |
| B24 | At UTOPIA $30 | +$212 |
| B25 | At Jefferson 3 Gbps | −$832 |
| B28 | 54k cohort × $650 (does **not** overwrite 54k) | $35.1M/year COGS |
| B29 | 54k × −$78.36 | −$4.2M/year |

---

## Frame A — $ per passing / connected home

Point estimate **$6,400 PV per connected home**. Round up from $6,382.

| ID | Line | Figure | Tag |
|---|---|---:|---|
| A26 | 20-year annuity of $650 @ 8% | $6,382 | DERIVED · WACC **ESTIMATED** at 8% (cash interest ~5.3% on ~$95B; equity higher) |
| A27 | **Commit PV / connected** | **$6,400** | COMMIT |
| A28 | ÷ plant at 40% take | $2,560 / passing | take **ESTIMATED** (FBA fiber take ~47%; co-op ~50%; 40% rounds against empty-passing leverage) |
| A20 | NRTC homes per fiber-mile | 10.57 (29,600 / 2,800) | RETRIEVED-derived · **NRTC and NRECA funded** the 2025 survey of 78 co-ops |
| A22–A24 | Laurinburg 20-year IRU $1,500/strand-mile × 2 strands × 0.0946 mi/home + $300/path-mile maint, PV @ 8% | $562 | RETRIEVED tariff (City of Laurinburg ordinance) × **ESTIMATED** strands |
| A25 | **Dark-IRU commit** (round up) | **$600 / passing** | COMMIT · **not lit last-mile** |
| A29 | Rural $/passing | $5,900 | RETRIEVED-derived · `decisions.md` ~$8.1B / 1.385M |
| A30 | Rural $/CR at 38.1% take | **$15,486** | DERIVED (live file rounds to ~$15,400) |
| A31 | Rural capital recovery / CR-year @ 8%/20y | $1,577 | vs wholesale $650 |
| A32 | Wholesale PV / rural CR capex | 0.41× | DERIVED |
| A33 | Rural EAC / passing-year | $601 | vs wholesale $260/passing-year at 40% take (A34) |

**Two builds, shared assumption disclosed.** Lit PV (A) and wholesale COGS (B) both use Jefferson $54. Agreement that “$650/year is the analog” is **correlation by construction**, not validation.

**Real cross-check that shares no inputs:** City of Laurinburg 20-year IRU ($1,500/strand-mile + $300/path-mile/year) and City of Decatur IL IRU ($1,000/strand-mile, 2021 contract), converted with NRTC miles/home. CTC’s Virginia Beach study (city-funded, 2017) ranged $325–$2,000/strand-mile. That path lands at **$600/passing** and does **not** use Grant/Jefferson MRC, Internet ARPU, or Charter opex. It disagrees with $6,400 because spare-strand dark fiber is not a drop to the home. Palo Alto’s 2025 dark-fiber *monthly* license ($476/fiber-mile/month) is an urban outlier and is not used.

---

## Geography conversion (on its own lines)

Charter does **not** publish other-FTTH overlap. Do not invent a passing count without these lines.

| ID | Retrieved as | Needed as | Conversion |
|---|---|---|---|
| G1 | US housing units 1 Jul 2025 **148,260,882** (Census vintage 2025) | Charter share of US plant | — |
| G2 | Occupied HU Q1 2026 **133,701,000** (Census HVS / FRED EOCCUSQ176N) | Occupied-base share | — |
| A1 | Charter passings 31 Mar 2026 **58,661,000** (Ex99.1) | Numerator | — |
| G3 | — | Charter / US HU | **39.57%** |
| G4 | — | Charter / occupied HU | **43.87%** |
| G5 | AT&T 27% + Verizon 16% | Large-overbuilder overlap | **43%** of *Charter* footprint — **not** smaller fiber |

National small-fiber (ex-AT&T, ex-Verizon at Q1 2026):

| ID | Line | Figure | Tag |
|---|---:|---:|---|
| G6 | Co-op survey 78 × 29,600 homes | 2.31M | RETRIEVED-anchored · NRTC/NRECA funded |
| G7 | Scale mean to “more than 240” deployed | 7.10M | **ESTIMATED** · survey mean applied to all 240 |
| G8 | MetroNet 3.0M (Nov 2025) + Kinetic 1.9M + Brightspeed 1.82M | 6.72M | RETRIEVED operator press |
| G9 | Municipal homes passed | 3.0M | **ESTIMATED** · ILSR map (ILSR-funded advocacy) counts 400+ networks / 700 communities, **no** national homes-passed total |
| G10 | Google Fiber + other independents | 3.0M | **ESTIMATED** · Google does not disclose passings |
| G11 | Raw sum | 19.82M | mixed |
| G12 | **Commit national small-fiber** (round up) | **20M** | COMMIT |
| G13 | FBA 84.6M − AT&T Q1 ~37M − Verizon+Frontier ~30M | 17.6M | DERIVED · **includes cable FTTH** · FBA funded its own YE2025 report — not a small-fiber count |
| G14 | Frontier 8.8M | now Verizon | rival mechanism |
| G15 | 20M × 39.57% | 7.91M | naive HU-share — **not overlap** |
| G16 | In-polygon factor | 40% | **ESTIMATED — blocking if treated as fact** |
| G17 | Overlap in Charter footprint | 3.17M | **ESTIMATED** |
| G18 | Wholesale-willing share | 15% | **ESTIMATED — blocking** · most small fiber is closed retail |
| G19 | Wholesale-willing overlapping homes | 0.47M | **ESTIMATED** |
| G20 | **Blocking input** | Charter-footprint small-fiber passings | **none retrieved** |

Precision did **not** migrate into AT&T 27% / Verizon 16%. Those shares are retrieved and unused as the addressable set. Effort on analog tariffs is where the unit-cost leverage is.

### Scenario range (because G20 is empty)

Upper bound assumes Charter captures **100%** of connected homes at 40% take. Open-access networks with many ISPs (UTOPIA lists 14) would give Charter a slice of that take. Unit costs do not change.

| Scenario | Overlapping HP | Customers (40% take) | Annual COGS | 20-yr PV | Rural-build instead | Contribution |
|---|---:|---:|---:|---:|---:|---:|
| Low (open-access-like) | 200k | 80k | **$52M** | $512M | $1.18B | −$6M |
| **Base** | **500k** | **200k** | **$130M** | **$1.28B** | $2.95B | **−$16M** |
| High | 2.0M | 800k | $520M | $5.12B | $11.8B | −$63M |

Base COGS is 1.1% of FY2025 capex **$11,659M** and 46% of the Q1 upgrade/rebuild increment **$280M**. Cheaper than overbuilding those homes. Still a negative-contribution channel.

---

## Dollar-weighted origin

**Unit economics (the headline −$79 / $650):**

| Bucket | $ in the Frame B identity | Origin |
|---:|---:|---|
| ARPU $790 + COGS $650 + care $97 | $1,537 | Retrieved-anchored |
| Residual field + transit + SAC | $122 | Estimated |
| **Retrieved share** | | **93%** |
| **Estimated share** | | **7%** |

**Scaled totals:** homes are unretrieved → **100% of $130M / $1.28B is estimated-homes × retrieved rate**. Do not quote $130M as a filing-quality cost.

---

## Sensitivity / leverage (estimated inputs ranked)

Wholesale MRC is retrieved (tariffs) and still the largest swing on contribution. Among *estimated* inputs, SAC and overlap move scaled dollars; residual field and transit move unit contribution less.

| Rank | Input | Low → high | Swing | Origin |
|---|---|---|---:|---|
| 1 | WACC on Frame A PV | 6% → 10% | ±$961 / connected | ESTIMATED |
| 2 | Take rate on Frame A $/passing | 25% → 55% | ±$960 / passing | ESTIMATED |
| 3 | Wholesale MRC | $30 → $117/mo | ±$522 / sub-year contribution | RETRIEVED analogs |
| 4 | SAC amort | $0 → $150 | ±$75 / sub-year | ESTIMATED |
| 5 | In-polygon overlap (scaled $M) | 20% → 60% | ±$62M/year | ESTIMATED |
| 6 | Transit | $0 → $96 | ±$48 / sub-year | ESTIMATED |
| 7 | Residual field share | 10% → 50% | ±$32 / sub-year | ESTIMATED |
| 8 | ARPU identity | $65.86 vs $70.72/mo | ±$29 / sub-year | RETRIEVED identities |

**Cheap binary that can kill (leverage ÷ cost):** one signed term sheet from a Charter-overlap open-access / PUD network stating MRC at 1 Gbps. If it is ≥ $54, stop. If it is ≤ $32.50, re-open Frame B. That is cheaper than buying a national small-fiber passing file.

---

## Channel contribution (size is not opportunity)

Wholesale at the committed analog **destroys** Internet contribution (−$79/sub-year). It cannot fund the 54k print close. It cannot substitute for overlap-zip save (Area 2 fiber branch) or for rural take on plant already lit (Area 4). Adjacent unserved small-fiber is a *capex alternative* to $5,900/passing rural build — and still fails unless the MRC is in the Grant-100 / absorbed-UTOPIA band.

Comparisons the files already committed:

| Comparison | Figure | Read |
|---|---:|---|
| Rural | ~$5,900/passing · ~$15,400–$15,486/CR | Wholesale PV $6,400/CR is 41% of rural CR capex |
| FY2025 capex | $11.7B | Base COGS $130M = 1.1% |
| Q1 upgrade/rebuild increment | $280M ($675M vs $395M) | Base COGS is 46% of that increment, every year, forever |
| 54k excess vs Comcast | 54k · −66k print | $35.1M/year COGS, −$4.2M contribution — not a closer |

---

## What to retrieve next (sequence)

1. **Binary, cheap, can kill:** one overlap open-access / PUD gigabit MRC in a Charter state.  
2. **Blocking on scale, not on the unit verdict:** Charter (or FCC BDC) other-FTTH homes inside the 58.661M passing polygon, split open-access vs closed retail.  
3. Do **not** spend the next cycle refining AT&T 27% / Verizon 16%.

---

*Sources: CHTR Ex99.1 Q1 2026 / 10-K FY2025; Census vintage 2025 HU and HVS occupied HU; Grant PUD Rate Schedule 100 (Res. 9058, 1 Aug 2024); Jefferson County PUD 2025 wholesale PON rates; UTOPIA Fiber public residential infrastructure fee; City of Laurinburg fiber ordinance IRU; City of Decatur IL IRU (2021); CTC Virginia Beach fiber model (city-funded, 2017); CPUC dark-fiber white paper; NRTC/NRECA 2025 Rural Electric Broadband Benchmarking Report (NRTC+NRECA funded); Fiber Broadband Association YE2025 passings (FBA funded); AT&T / Verizon / Frontier / MetroNet / Kinetic / Brightspeed operator disclosures; NTIA BEAD NOFO (2022) and BEAD Restructuring Policy Notice (6 Jun 2025); ILSR Community Network Map (ILSR-funded). Arithmetic in `small_fiber_licensing_model.py` matches this memo. Does not clobber 54k / −66k.*
