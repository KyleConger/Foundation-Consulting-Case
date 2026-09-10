# Solving Playbook

The companion to `Framestorming-Playbook.md`. That one ends when you have frames worth testing. This one covers what happens next: turning a frame into a number, a recommendation, and a decision someone can act on.

Core rule: **a frame that does not produce its own number was decoration.**

---

## 1. Carry the frames in — one number each

The bridge between the two playbooks is arithmetic. If the framing survives into the analysis only as section headings, it did no work.

Make each root frame generate its own serviceable-market figure (or other decision-relevant number), and let the frames disagree about size. The disagreement is often the finding — one frame relocating the recommendation is only visible once every frame has been forced to produce a number instead of a paragraph.

---

## 2. Commit to a number

A range with no point estimate is an evasion dressed as rigor. Give the range **and** the number.

- **Round in the direction that costs you.** State that you rounded down (or up, if upside is the risk) and why.
- **Say which number is the deliverable.** One headline figure, not four competing ones.
- If you genuinely cannot commit, name the single input that is blocking you and what it would cost to retrieve — that is a more useful answer than a wide range.

---

## 3. Build it twice, and know when agreement means nothing

Build top-down and bottom-up independently, then reconcile out loud.

The trap: two builds that land close together look like validation and often are not. If both use the same estimated construct (band share, attach rate, conversion), they are **correlated by construction**. Agreement then proves the arithmetic is consistent, not that the answer is right. Say this explicitly when it is true.

**Real validation requires structurally different routes that share no inputs.** Agreement across independent routes is worth something. Agreement between two builds sharing a key assumption is not.

---

## 4. Show the arithmetic: one assumption per line, with a line ID

Give every input an ID (A1, A2, B7) and write derived lines as formulas that reference them — `A10 = A2 × A9`.

This is not formatting. It does three jobs:

1. A reader can recompute the whole chain and land on your number.
2. A sensitivity test becomes trivial, because you know what feeds what.
3. **It catches your own errors.** Writing the chain out line by line is how silent inconsistencies between sections surface.

---

## 5. Retrieved versus estimated, then weigh it

Tag every input as **RETRIEVED** (from a named source) or **ESTIMATED** (your judgment). Never blur them, and never let an estimate inherit the credibility of the filing next to it.

Then do the part most analyses skip: **weigh the tags by how much of the answer they carry.** Counting inputs is not enough — many retrieved lines can cover the smaller share of the dollars. Report the dollar-weighted split.

---

## 6. Convert every geography, channel, and currency on its own line

Retrieved figures almost never arrive in the shape you need. Make each conversion visible and flagged, because conversions are where a sourced number quietly becomes an estimate.

Never let a global or regional total stand in silently for a national one. If someone asks "did you separate the geographies?", the answer should be a line number.

---

## 7. Watch for precision migration

Rigor drifts toward the data that exists, not the data that matters. Filings and government tables are precise and available, so that is where effort goes — often onto the least leveraged part of the model. Guard against it:

1. Rank every estimated input by how far the answer moves across a plausible low/base/high.
2. Compare that ranking against where you actually spent your time.
3. If they do not match, stop refining and go retrieve.

---

## 8. Recompute your own numbers in code before shipping

Run the whole chain in a script and diff it against your prose. Fluency is not accuracy, and **your own memo is not exempt** — a number carried by hand across three sections will drift.

Check specifically:
- Every weighted average against its stated weights.
- Every total against the sum of its parts.
- Every percentage against its base.
- Rounded values that later get multiplied — round at the end, not the middle.

---

## 9. Size is not opportunity: no viable channel, no market

A market you cannot profitably serve is not addressable, however large. Always put unit economics between the market size and the recommendation.

Run contribution by channel — price, fees, landed cost, acquisition cost — before you write a recommendation. The market size does not choose the channel. The contribution math does, and it often overturns the obvious plan.

---

## 10. Sequence retrieval by leverage ÷ cost, and mark what is decision-critical

Rank the estimates you would most like to convert, then reorder by cost and speed. Cheap binary questions that can end the project go first, regardless of how interesting the big analysis is.

Note the common inversion: the highest-leverage input on the market size is often **not** the first thing to buy, because a cheap regulatory, cost, or legal gate can make the whole question moot.

---

## 11. Write the kill rule before you write the recommendation

State in advance what evidence would make the answer no. Written afterward, it is decoration; written first, it is a constraint. Make it conjunctive and testable.

Then pair it with the mirror discipline: a short, explicit list of **what you are unwilling to claim.**

---

## 12. Correction discipline

When your own number changes, change it in the open. State the corrected figure, name what caused the change, mark the superseded document, and move on. No relitigating and no apology tour — one plain sentence and the new arithmetic.

If the recommendation survives the correction, say that too. Readers need to know which changed: the magnitude, the decision, or both.

Never leave two live documents carrying different headline numbers.

---

## 13. Use AI where it is strong

The solving phase sits in the half of the process where AI is genuinely strong — but the two steps that decide quality are still yours.

| Stage | Who leads | What it looks like here |
| --- | --- | --- |
| Work plan | AI as virtual expert | Turn prioritized questions into analyses, sequencing, owners |
| Analyze | AI as virtual expert | Build the model, retrieve filings, compute sensitivities |
| **Synthesize** | **You** | Choose the number, resolve the contradictions, own the recommendation |
| Communicate | AI as virtual expert | Memo, tables, exhibits, anticipated questions |

Prompt controls that matter specifically for solving: force a point estimate rather than a range; require each frame to produce its own number; require channel-level contribution; demand the kill rule up front; and require every assumption on its own line tagged retrieved or estimated with low-confidence figures flagged visibly rather than footnoted.

---

## 14. Closing move

Lead with the number and the decision, not the method. The build belongs below the answer, and the audit belongs below the build.

Then end on the honest sentence: what share of the build is estimate, which leveraged input has no retrieved anchor, and what the next dollars of retrieval should buy. A number presented without its weaknesses invites either false confidence or total dismissal, and both are worse than a flagged estimate.

---

## 15. Pre-delivery gate

Do not deliver a solving artifact until all ten are true. This list is mirrored in `framestorm-and-solve.mdc`; change both together.

1. Each root frame has produced its own number.
2. A single headline number is stated, with a range, and it is the first thing in the deliverable.
3. Two builds exist and are reconciled, and shared assumptions between them are disclosed.
4. At least one cross-check uses a structurally different route that shares no inputs.
5. Every input is tagged retrieved or estimated; low-confidence figures are flagged visibly, not in footnotes; anyone who funded a cited survey is named.
6. A sensitivity ranking exists and the top-leverage inputs are identified.
7. The arithmetic has been recomputed in code and matches the prose.
8. Channel contribution has been run and the recommendation follows from it.
9. A kill rule and an "unwilling to claim" list are present.
10. If a prior number is being changed, the correction is stated plainly and the old document is marked superseded.

### Solving a framestorm that already exists

Read the framing before analyzing it. Carry those frames forward rather than re-deriving your own, and never leave two live documents carrying different headline numbers.
