# Framestorming Playbook

A reusable method for framing a problem before solving it, written from the premium insulated
drinkware practice case (Sept 8, 2026) and the MAN6930 course notes. The worked example is in the four
`Drinkware-Framestorm-*.canvas.tsx` files in this folder.

Core rule, from class: **if your three framings are variations on your first one, you accepted its frame.**

---

## 1. Before writing anything, settle the contract

Two minutes here saved a wasted draft in the drinkware run.

- **Interrogate negative constraints.** "No market data" turned out to mean "I am not supplying data,"
  not "do not use data." A constraint that changes the whole method is worth one clarifying question.
- **Ask what stage the output is.** The instruction was "your first output should be a draft, not an
  answer." Drafts invite pushback; answers invite defense. Label the artifact accordingly.
- **Name the role you are playing.** Skeptical strategy partner, market researcher, expert for hire,
  pair of hands. The role determines whether you are allowed to challenge the client's premise at all.
- **Ask one question at a time.** Two questions in one sentence gets one answer and you will not know
  which one it answered.

---

## 2. Generate frames by changing where the problem lives

The reliable way to get non-overlapping frames is not to reword the question. It is to relocate the
problem into a different room. For any commercial case, walk these rooms and ask "what if the binding
problem is *here*?"

| Room | The problem sounds like |
| --- | --- |
| The customer's cupboard / installed base | They already own one; nothing triggers a replacement |
| The customer's identity | This is a fashion object on a trend cycle, not a durable good |
| The buyer's planogram | A merchant allocates the shelf; the consumer never gets to choose |
| The factory and the port | Landed cost, duty stack, minimum order quantity, cash cycle |
| The courtroom | Freedom to operate, design patents, trade dress, time to copy |
| The compliance file | Food contact, Prop 65, claims support, recall exposure |
| The returns dock | Reverse logistics and defect rates exceed what the price can fund |
| The cap table | Capital was raised against a story the category can no longer support |
| The founder's own head | The decision was already made; analysis is being used to ratify it |

Two starting questions from class that do most of the work: **what business is this company actually
in?** and **what did you actually see or measure, before what do you think is happening?**

---

## 3. Test the frame set before presenting it

A frame set fails if any of these is true.

- **Self-similarity.** Do all three frames send you to measure the same things? Then you have one frame
  in three costumes.
- **The checklist trap.** If the three collapse into desirability, then access, then viability, you have
  produced a generic market-entry checklist and accepted the client's frame with extra steps. Present
  frames as **rival claims about where the constraint sits**, and design research to find which fails
  first — not to tick all three.
- **Non-conflict.** Strong frames contradict each other. In the drinkware case, "buy the identity
  object" and "replace the failed object" cannot both be the dominant mechanism; that tension is what
  makes them worth testing.
- **Unfalsifiability.** "Right to win" absorbed channel, brand, IP, and acquisition cost, which made it
  impossible to be wrong. It became useful only when narrowed to "name the asset she holds that a
  competitor cannot buy or copy."
- **Depth.** Class critique of the Nike/DTC case: trees that stop at one or two levels have no juice.
  "Returns are high" is a location, not a cause. Push to sizing accuracy, fit guidance, defect rate.
- **Symptom mistaken for cause.** Where the number is bad is rarely where the problem is.

A sharp problem statement is a question, not a topic; names the decision-maker and the constraint; and
does not contain a pre-chosen solution.

---

## 4. Classify each perspective by role, on one dimension only

This was the highest-value step, and I got it wrong the first time. Do not rate perspectives by how
good they are. Rate them by **what job they do in the diagnosis**, which is a single dimension and
therefore comparable.

| Role | Definition | Where it goes |
| --- | --- | --- |
| Root frame | Could be the actual problem. Names a place the venture fails and could be shown wrong. | The framing deliverable |
| Rival mechanism | Explains *why* a root frame would hold. Competes with its siblings. | Nested under a root frame |
| Hard constraint (gate) | Pass or fail. Failure ends it; passing confers no advantage. | The work plan, sequenced early |
| Sub-branch | Only decisive after a prior choice is made. | Nested, never standing alone |
| Decision architecture | How to act once you know where the problem is. | The recommendation |

Two diagnostics that fall out of this taxonomy:

- **The universality test.** If a perspective would be equally true of any company in any category, it
  discriminates nothing about this situation. "Stage your bets and predefine kill thresholds" is sound
  advice and a weak diagnosis. It is decision architecture, not a frame.
- **The double-duty test.** If a perspective is doing two jobs, split it. "Copy war" was a legal gate
  (does she infringe?) plus a strategy question (how fast is she copied?). "Mouth-contact" was a
  compliance gate plus a genuine demand hypothesis (will anyone pay $40 to drink daily from an unknown
  brand?). Bundling the demand half with paperwork nearly buried it. Failing MECE inside a single row is
  itself a finding.

---

## 5. Guard against grading your own homework

In the first synthesis I rated exactly the three frames I had already chosen as "Strongest." That is
post-hoc justification wearing the costume of assessment. Countermeasures:

- Score on a dimension that cannot flatter your pick (role, not quality).
- Force at least one demotion and one promotion before you call an assessment finished.
- If everything you generated first survives, treat that as evidence of anchoring, not of good judgment.
- Class version of this: **seek disconfirmation.** If everyone on the team agrees with you, you have a
  team problem.

---

## 6. Sequence the work by cost of resolution, not by intellectual interest

Run the binary, cheap, potentially fatal checks first. In the drinkware case that meant a customs
classification, a factory quote, a freedom-to-operate search, and a batch lab test — days of work,
each capable of closing the question. There is no reason to spend three weeks on consumer research that
a duty rate would have made irrelevant. Then test the rival demand mechanisms against each other.
Then commit capital in stages with thresholds written down in advance.

---

## 7. Source hygiene

Fluency is not accuracy, and the model will tell you what you want to hear if you let it.

- Rank sources openly: SEC filings and earnings releases, then Reuters and trade press citing Circana or
  Consumer Edge, then vendor research, then SEO content farms. The drinkware run pulled all four tiers.
- Flag who paid for the number. The ownership-and-replacement survey that anchored one whole frame was
  commissioned by a bottle startup. Still usable, but say so and ask for replication.
- Mark anything that must be verified before it enters a pricing model. Duty stacks came from sourcing
  vendors' marketing pages; that needs a licensed broker before anyone prices a SKU on it.
- Separate what you measured from what you inferred, and **ask how they know.** Direct knowledge,
  secondhand report, and inference are three different things wearing the same clothes.

---

## 8. Use AI where it is strong, per the class model

| Stage | Who leads |
| --- | --- |
| Define | AI as thought partner |
| Disaggregate | AI as thought partner |
| Prioritize | You |
| Work plan | AI as virtual expert |
| Analyze | AI as virtual expert |
| Synthesize | You |
| Communicate | AI as virtual expert |

AI is weakest exactly where consulting adds the most value: prioritizing and synthesizing. Its
characteristic failure is overinterpreting a symptom as a root cause and stopping the tree too early.

**Multi-model technique that worked here:** run the identical prompt independently on different models,
explicitly forbidding each from using the previous run's ideas as a basis. Then do not pick a winner —
reclassify all the perspectives by role and rebuild one frame set from the parts. Nine perspectives from
three runs produced eleven roles once the double-duty entries were split, and the final three frames
included one perspective that no single run had ranked first.

---

## 9. Closing move

End a framing deliverable with the question you would ask the client next, not with a conclusion. The
best one from the drinkware case: **who has already said no** — a retail buyer, a factory that would not
tool the lid, a lab that would not certify the solder — **or has no one, because the only person consulted
so far is a hypothetical consumer?**
