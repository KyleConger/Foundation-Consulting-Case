# Customer performance by disclosed LOB (draft)

**Status:** analysis, not a recommendation · does not supersede GAP or the if-lost-to-X playbook  
**Anchor:** end Q1 2026 · Q2 labeled later public fact  
**Companion:** [chtr-customer-performance canvas](C:/Users/Owner/.cursor/projects/c-Users-Owner-Desktop-MAN6930-Case/canvases/chtr-customer-performance.canvas.tsx) · `Analysis/customer_performance_model.py` · LOB scorecard (not moved into `CHURN/`)

---

## Headline

**Partially: filings support an accurate net-customer and revenue LOB read, not a churn analysis.** Q1 2026 residential Internet **−117k** customers and **−$78M** revenue, because volume (**−$90M**) beat a **+$12M** rate/mix help. Internet is **43%** of Q1 revenue ($5,852M / $13,597M). Mobile **+368k** lines and **+$138M** fills the connectivity subtotal (**+$60M**) and **does not** re-rate the Internet print (Root C).

Peer overlay, residential broadband only: Charter’s residential Internet net-loss rate is **1.8×** Comcast’s (commit, round down from 1.87×); excess **54k** (round down from 54.4k). Reused from the network-churn work — not a new competing headline.

---

## Accuracy limit

| Accurate for | Not accurate for |
|---|---|
| Ending customers, quarterly **net** adds, revenue, disclosed residential / SMB ARPU | Gross adds, gross disconnects, a churn *rate* |
| Internet (residential and total), mobile lines, video, voice | Disconnect reasons, overlap-zip losses |
| Small-business relationships, mid-market & large PSUs | Retention quality, “customer performance” as save-rate |
| Rural CR as a **disclosed subset** (not a product) | Treating net adds as churn |

Do not mix pre/post Q4 2025 customer restatement bases. All customer counts here are restated.

---

## Each LOB’s own numbers (Q1 2026)

Customers in thousands. Dollars in millions. Restated basis.

| LOB | Ending | Net adds | Revenue | $ YoY | Tag |
|---|---:|---:|---:|---:|---|
| Residential Internet | 27,524 | **−117** | 5,852 | **−78 (−1.3%)** | RETRIEVED |
| Total Internet | 29,560 | −120 | (residential Internet line) | — | RETRIEVED; SMB Internet −3 |
| Mobile lines | 12,134 | **+368** | 1,052 | **+138 (+15.1%)** | RETRIEVED; lines ≠ customers |
| Video | 12,545 | −60 | 3,252 | −328 (−9.2%) | RETRIEVED; **$171M** allocation drag |
| Voice | 5,872 | −174 | 338 | −18 (−5.0%) | RETRIEVED |
| Small business CR | 2,231 | −6 | 1,090 | +2 (+0.2%) | RETRIEVED; ARPU $162.71 |
| Mid-market & large PSUs | 360 | +3 | 749 | +15 (+2.1%) | RETRIEVED |
| Rural CR (subset) | 527 | +41 | 221 | 1.6% of company | RETRIEVED trending |
| Residential CR | 29,452 | −157 | 10,494 | −286 (−2.7%) | RETRIEVED; ARPU $118.44 |
| Company | — | CR −163 | 13,597 | −138 (−1.0%) | RETRIEVED |

FY2025 contrast (retrieved 10-K bridge): Internet **+$405M** = rate/mix **+$785M** + volume **−$380M** on **−393k** residential Internet. Q1 is when dollars turned with the base.

Q1 identities (recomputed): residential products Internet + mobile + video + voice = **$10,494M**. Company residential + SMB + mid-market + ads + other = **$13,597M**. Res. Internet −117 + SMB Internet −3 = total Internet **−120**. Company CR −163 − rural +41 = core CR **−204**.

---

## Two builds

**Build 1 — customers (operating-statistics table).** Residential Internet −117k; total Internet −120k vs −59k in Q1 2025 (slope break −61k). Mobile +368k. Video −60k. Voice −174k. SMB CR −6k. Mid-market +3k PSUs.

**Build 2 — dollars (P&L).** Internet −$78M. Mobile +$138M. Video −$328M. Voice −$18M. SMB +$2M. Mid-market +$15M.

They share no identity (headcount is not dollars). They agree on direction. That is consistency of two filing tables, **not** validation of retention quality, and **not** a churn rate.

**Internet volume/rate split (derived from retrieved ÷ retrieved).** Implied residential Internet ARPU $70.72 vs $70.58. Holding last year’s ARPU, the smaller average base costs **−$90M**; rate/mix **+$12M**; net **−$78M**. ARPU would have needed **$71.66** (+$0.94) to hold dollars flat. Rounded to whole millions against “price collapsed.”

Mobile implied ARPU $30.38 vs $31.13 — dollars up on volume despite a lower rate. FY2025 10-K: mobile +$714M volume, −$35M rate.

Video: $171M of the $328M decline is seamless-entertainment allocation ($218M vs $47M). Residual ~−$157M. Implied ARPU $89.98 vs $97.47.

Disclosed residential ARPU identity: $10,494M / 3 / avg CR = **$118.45** vs disclosed **$118.44**.

---

## Dollar-weighted origin

Every Q1 revenue dollar in the headline ($13,597M) is **RETRIEVED**. Estimated share of the dollar answer: **0%**. Implied product ARPUs are formulas on two retrieved series (flagged DERIVED, not filing facts).

The missing input — gross adds vs disconnects — carries **none** of the dollar answer and **all** of the leverage on a retention-quality claim. Precision has already migrated to the available net-add arithmetic. Stop refining $78M.

---

## Size is not opportunity

| LOB | Q1 revenue share | Can it close the Internet print? |
|---|---:|---|
| Internet | 43% | This **is** the print |
| Video | 24% | No — secular + allocation; not the connectivity tape |
| Mobile | 7.7% | No — Root C; lower-margin MVNO; lines ≠ Internet customers |
| SMB | 8.0% | No — flat |
| Mid-market | 5.5% | No — +$15M is 19% of the Internet $ hole, different customers |
| Voice | 2.5% | No |
| Rural subset | 1.6% | No — +41k CR, wrong unit and wrong scale vs −117k Internet |

Connectivity dollars still grew +$60M. Do not credit that against Internet for the tape.

Peer: apples-to-apples is residential broadband only (CHTR res. Internet −117k vs CMCSA domestic resid. BB −65k). Not total Internet vs residential. Not mobile vs broadband.

---

## Sensitivity / leverage

1. **Gross adds vs disconnects** — not in the model — can flip Q1 from failed acquisition to failed retention.  
2. **Internet implied ARPU** — $0.94/mo would have held Internet $ flat; small vs volume.  
3. **Video allocation** — $171M of video’s $ decline; irrelevant to the Internet print.  
4. **Rural Internet net adds** — not disclosed (only rural CR).

---

## Kill rule (before a recommendation)

If a later quarter shows Internet revenue growing while residential Internet net adds stay negative, **and** the 10-K-style bridge shows rate/mix more than offsetting volume, **kill** “Q1 was a durable regime change to volume printing through” — that is FY2025 again.

If Charter discloses gross adds and disconnects, this memo is still **not** a churn analysis until those series are used.

If rural *Internet* net adds (once disclosed) close the residential Internet hole, **kill** “rural cannot close” — we do not have that cut.

Do **not** launch a retention program from this file. Net adds cannot tell retention from acquisition. That remains the GAP tracker (G1).

---

## Unwilling to claim

- A churn rate, gross churn, or retention quality.  
- Disconnect reasons or overlap-zip losses (AT&T ~27% / Verizon ~16% is footprint mix).  
- That mobile +368k / +$138M offsets Internet for the tape.  
- That rural +41k is Internet conversion.  
- Product-level ARPU as a filing fact.  
- Mixed pre/post Q4 2025 customer bases.  
- That two builds agreeing proves anything other than table consistency.

---

## Q2 2026 (later public fact)

Internet **−172k** and Internet revenue **−$193M** (−3.2%). Mobile **+406k**. Rural CR **+47k**. The Q1 dollar inflection continued. Does not replace the Q1 assignment anchor.

---

*Sources: CHTR Ex99.1 Q1 2026 / 10-K FY2025 / Q1 trending (CORE-INFORMATION); CMCSA Ex99.1 Q1 2026. Arithmetic in `customer_performance_model.py` matches this memo. Does not clobber GAP or the if-lost-to-X playbook.*
