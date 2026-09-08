# Solving Playbook

The companion to `Framestorming-Playbook.md`. That one ends when you have frames worth testing. This
one covers what happens next: turning a frame into a number, a recommendation, and a decision someone
can act on. Written from the premium insulated drinkware sizing (Sept 8, 2026); the worked example is
`Drinkware-Sizing-Iteration-2.md` and `Drinkware-Sizing-Audit.csv` in this folder.

Core rule: **a frame that does not produce its own number was decoration.**

---

## 1. Carry the frames in — one number each

The bridge between the two playbooks is arithmetic. If the framing survives into the analysis only as
section headings, it did no work.

Make each root frame generate its own serviceable-market figure, and let the frames disagree about
size. In the drinkware case:

| Frame | Its own number | What that number decided |
| --- | --- | --- |
| Displacement of a vessel already owned | $157.5M consumer online niche | Big enough for a product claim, too small for a media budget |
| Founder-specific right-to-win | $680.6M B2B supplier-level pool | 4.3× the consumer niche — **relocated the entire recommendation** |
| Landed cost and duty stack | $2.20/unit, $281.9K/yr at volume | Largest single controllable lever in the model |

The second frame changed the answer. That only became visible because it was made to produce a
number instead of a paragraph.

---

## 2. Commit to a number

A range with no point estimate is an evasion dressed as rigor. Give the range **and** the number.

- **Round in the direction that costs you.** Midpoint of the two drinkware builds was $1,279.5M; the
  committed figure was **$1.25B**. State that you rounded down and why.
- **Say which number is the deliverable.** One headline figure, not four competing ones.
- If you genuinely cannot commit, name the single input that is blocking you and what it would cost to
  retrieve — that is a more useful answer than a wide range.

---

## 3. Build it twice, and know when agreement means nothing

Build top-down and bottom-up independently, then reconcile out loud.

The trap: the two drinkware builds landed 7.5% apart, which looks like validation and is not. Both
used the same estimated "share of dollars in the $35–$50 band" construct, so they were **correlated by
construction**. Two methods agreeing there proved the arithmetic was consistent, not that the answer
was right. Say this explicitly when it is true.

**Real validation requires structurally different routes that share no inputs.** The year-3 figure
was checked two ways that did not overlap:

- Units × blended ASP: 128,000 × $34.60 = **$4.43M**
- Share of SAM: 1.5% of $157.5M + 0.3% of $680.6M = **$4.40M**

Agreement within 0.7% across independent routes is worth something. Agreement between two builds
sharing a key assumption is not.

---

## 4. Show the arithmetic: one assumption per line, with a line ID

Give every input an ID (A1, A2, B7) and write derived lines as formulas that reference them —
`A10 = A2 × A9 = 1,085.8 × 0.76 = $825.2M`.

This is not formatting. It does three jobs:

1. A reader can recompute the whole chain and land on your number.
2. A sensitivity test becomes trivial, because you know what feeds what.
3. **It catches your own errors.** Writing the chain out line by line is how the drinkware blended ASP
   error surfaced (see §7).

---

## 5. Retrieved versus estimated, then weigh it

Tag every input as **RETRIEVED** (from a named source) or **ESTIMATED** (your judgment). Never blur
them, and never let an estimate inherit the credibility of the filing next to it.

Then do the part most analyses skip: **weigh the tags by how much of the answer they carry.**

| Drinkware bottom-up build | Value | Origin |
| --- | ---: | --- |
| YETI line, built on filed SEC figures | $1,092.9M | Retrieved anchor + 2 estimated ratios |
| All other brands and private label | $2,700.0M | Estimated, one with no anchor at all |
| **Total** | **$3,792.9M** | **28.8% retrieved-anchored, 71.2% estimated** |

Counting inputs is not enough — 25 retrieved against 35 estimated understated the problem, because the
retrieved ones covered the smaller share of the dollars. Report the dollar-weighted split.

---

## 6. Convert every geography, channel, and currency on its own line

Retrieved figures almost never arrive in the shape you need. Make each conversion visible and
flagged, because conversions are where a sourced number quietly becomes an estimate.

| Retrieved as | Needed as | Conversion line |
| --- | --- | --- |
| YETI drinkware $1,085.8M, global | US only | × 76%, set below the 78.9% company US mix on a disclosure |
| ASI promo $27.7B, North America | US only | × 90% |
| E-commerce 41.3%, global | US band | separate estimated line at 42%, flagged |
| Net sales (wholesale + DTC) | Retail sell-through | DTC left at retail, wholesale ÷ 0.55 |

Never let a global total stand in silently for a national one. If someone asks "did you separate US
from global?", the answer should be a line number.

---

## 7. Watch for precision migration

The most useful thing the drinkware pass revealed:

> The two inputs derived most carefully from SEC filings moved the answer by about **1%**. The four
> inputs with no retrieved anchor moved it **19–29%**.

Rigor drifts toward the data that exists, not the data that matters. Filings are precise and
available, so that is where the effort went — and it was spent on the least leveraged part of the
model. Guard against it:

1. Rank every estimated input by how far the answer moves across a plausible low/base/high.
2. Compare that ranking against where you actually spent your time.
3. If they do not match, stop refining and go retrieve.

| Input | Low → High | Swing |
| --- | --- | --- |
| Band share | 25% → 45% | **±29%** |
| Purchases per owner per year | 0.45 → 0.75 | **±25%** |
| Other brands' US retail | ±30% | **±21%** |
| Ownership rate | 60% → 85% | **±19%** |
| YETI US drinkware share | 70% → 79% | ±1.1% |
| Wholesale-to-retail ratio | 50% → 60% | ±1.4% |

---

## 8. Recompute your own numbers in code before shipping

Run the whole chain in a script and diff it against your prose. Fluency is not accuracy, and **your own
memo is not exempt** — a number carried by hand across three sections will drift.

This is not hypothetical. The first drinkware memo carried a **$39 blended ASP** into the year-3
revenue line while the stated channel mix implied **$34.60**. That overstated the headline by 13%:
$5.0M where the arithmetic gave **$4.43M**. Nothing caught it except recomputing the chain.

Check specifically:
- Every weighted average against its stated weights.
- Every total against the sum of its parts.
- Every percentage against its base.
- Rounded values that later get multiplied — round at the end, not the middle.

---

## 9. Size is not opportunity: no viable channel, no market

A market you cannot profitably serve is not addressable, however large. Always put unit economics
between the market size and the recommendation.

The drinkware case: a $1.25B band, and paid direct-to-consumer still failed. At $40 retail, $14.06
landed:

| Channel | Contribution | Acquisition cost | Verdict |
| --- | ---: | ---: | --- |
| Own DTC, paid media | $17.14 | $25–40 | **Negative on first order** |
| Amazon after PPC | $5.94 | in the $5.94 | Thin but positive |
| Direct corporate, decorated | $13.19 | none | **Best available** |

The market size did not choose the channel. The contribution math did — and it overturned the obvious
plan. Run this before you write a recommendation, not after.

---

## 10. Sequence retrieval by leverage ÷ cost, and mark what is decision-critical

Rank the estimates you would most like to convert, then reorder by cost and speed. Cheap binary
questions that can end the project go first, regardless of how interesting the big analysis is.

| Priority driver | Drinkware example | Cost | Days |
| --- | --- | ---: | ---: |
| Cheap, binary, can kill the venture | Broker ruling on the duty stack and the Section 232 question | $1–2K | 5–10 |
| Free, decides the largest cost line | Factory quotes for FOB and MOQ | $0 | 10–20 |
| Expensive, high leverage, not decision-critical | POS data by price band | $5–15K | 10–20 |
| Decides the channel, needs a live test | Real CAC on one SKU | $15–25K | 30–45 |

Note the inversion: the highest-leverage input on the market size (band share, ±29%) is **not** the
first thing to buy, because a $1–2K duty ruling can make the whole question moot.

---

## 11. Write the kill rule before you write the recommendation

State in advance what evidence would make the answer no. Written afterward, it is decoration; written
first, it is a constraint. Make it conjunctive and testable:

> If landed cost cannot get below $16, **and** there is no defensible product claim, **and** fewer than
> 3 of 20 corporate buyers will pilot at $28 or more — do not scale. Pivot to licensing and preserve
> the remaining capital.

Then pair it with the mirror discipline: a short, explicit list of **what you are unwilling to claim.**
For the drinkware work that was four items — the TAM is not measured, the two builds agreeing proves
nothing, the survey behind the consumer path was vendor-funded, and no amount of sizing can establish
a right to win.

---

## 12. Correction discipline

When your own number changes, change it in the open. State the corrected figure, name what caused the
change, mark the superseded document, and move on. No relitigating and no apology tour — one plain
sentence and the new arithmetic.

If the recommendation survives the correction, say that too. The drinkware headline moved from $5.0M
to $4.4M and the recommendation did not change; the magnitude did. Readers need to know which.

---

## 13. Use AI where it is strong, per the class model

The solving phase sits in the half of the process where AI is genuinely strong — but the two steps that
decide quality are still yours.

| Stage | Who leads | What it looks like here |
| --- | --- | --- |
| Work plan | AI as virtual expert | Turn prioritized questions into analyses, sequencing, owners |
| Analyze | AI as virtual expert | Build the model, retrieve filings, compute sensitivities |
| **Synthesize** | **You** | Choose the number, resolve the contradictions, own the recommendation |
| Communicate | AI as virtual expert | Memo, tables, exhibits, anticipated questions |

Prompt controls that matter specifically for solving, beyond the framing versions: force a point
estimate rather than a range; require each frame to produce its own number; require channel-level
contribution; demand the kill rule up front; and require every assumption on its own line tagged
retrieved or estimated with low-confidence figures flagged visibly rather than footnoted.

---

## 14. Closing move

Lead with the number and the decision, not the method. The build belongs below the answer, and the
audit belongs below the build.

Then end on the honest sentence. For the drinkware case it was: **roughly 71% of this build is team
estimate, the single most leveraged input has no retrieved anchor, and the first $20K should be spent
converting four estimates into facts.** That sentence is what makes the $1.25B usable — a number
presented without its weaknesses invites either false confidence or total dismissal, and both are worse
than a flagged estimate.

---

## 15. Pre-delivery gate

Do not deliver a solving artifact until all ten are true. This list is mirrored in
`.cursor/rules/solving.mdc`; change both together.

1. Each root frame has produced its own number.
2. A single headline number is stated, with a range, and it is the first thing in the deliverable.
3. Two builds exist and are reconciled, and shared assumptions between them are disclosed.
4. At least one cross-check uses a structurally different route that shares no inputs.
5. Every input is tagged retrieved or estimated; low-confidence figures are flagged visibly, not in
   footnotes; anyone who funded a cited survey is named.
6. A sensitivity ranking exists and the top-leverage inputs are identified.
7. The arithmetic has been recomputed in code and matches the prose.
8. Channel contribution has been run and the recommendation follows from it.
9. A kill rule and an "unwilling to claim" list are present.
10. If a prior number is being changed, the correction is stated plainly and the old document is
    marked superseded.

### Solving a framestorm that already exists

Read the framing before analyzing it. In this project that means the framestorm canvases and the
reclassified synthesis in `In Class Practice/`, plus any memo or CSV that already committed a number.
Carry those frames forward rather than re-deriving your own, and never leave two live documents
carrying different headline numbers.
