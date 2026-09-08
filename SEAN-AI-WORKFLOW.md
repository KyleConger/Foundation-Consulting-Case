# Sean O’Donnell’s AI workflow for consulting

_Course working guidance, not a Charter filing or assignment-brief quotation._

## Core principle

AI is weakest where consulting adds the most value.

Use AI to expand thinking, supply specialist capacity, execute analysis, and improve the form of communication. Keep human ownership over prioritization and synthesis: deciding what matters, exercising judgment, integrating conflicting evidence, and choosing the recommendation.

## Where AI is best in the process

1. **Define — AI as thought partner.** Use AI to challenge the initial problem statement, distinguish symptoms from causes, expose assumptions, and generate alternative framings. The consultant owns the final definition.
2. **Disaggregate — AI as thought partner.** Use AI to propose issue-tree branches, hypotheses, missing questions, and MECE tests. The consultant checks whether the structure fits the client’s actual situation.
3. **Prioritize — you.** Decide which branches matter, which evidence is decision-changing, and what the team will not pursue. Do not outsource judgment or trade-offs to AI.
4. **Work-plan — AI as virtual expert.** Ask AI to translate the prioritized questions into analyses, data requirements, owners, sequencing, milestones, and quality checks.
5. **Analyze — AI as virtual expert.** Give AI a specific professional role and require a verifiable deliverable. Use it for research, modeling, calculations, benchmarking, stress tests, and quality review. Verify sources, formulas, units, definitions, and assumptions.
6. **Synthesize — you.** Integrate the findings, resolve contradictions, decide what they mean for the client, and choose the recommendation. This is where consulting judgment creates disproportionate value.
7. **Communicate — AI as virtual expert.** Use AI to turn the team’s synthesis into client-ready exhibits, memos, slide language, speaker notes, and anticipated Q&A. The consultant remains accountable for accuracy, tone, and the recommendation.

## Six prompt controls, then iterate

A strong prompt is a controlled work order, not a topic.

### 1. Role

Tell AI first and foremost what you want it to be.

Examples: thought partner, cable-industry expert, corporate-finance expert, market-sizing consultant, skeptical reviewer, or CEO communications adviser.

### 2. Context

State the situation, audience, and limits.

Ask: Who is this for? What decision must they make? What facts or files govern the work? What is the time horizon? What must remain outside scope?

### 3. Task

Request a deliverable, not a topic.

Weak: “Analyze the insulated-drinkware market.”

Stronger: “Produce a top-down annual U.S. market-size estimate for premium insulated drinkware sold at $35 retail.”

### 4. Constraints

Specify length, exclusions, confidence requirements, and flags.

Examples: use only public sources; anchor facts to Q1 2026; exclude Q2 except as labeled context; separate disclosed facts from assumptions; flag weak evidence; do not invent missing customer data.

### 5. Format

Name the output form.

Examples: table, memo, bullets, issue tree, work plan, Excel model, slide outline, or chart specification.

### 6. Examples

Show the desired result as written. A concrete example controls terminology, granularity, and quality better than adjectives such as “professional” or “detailed.”

Then iterate: inspect the output, identify the highest-impact weakness, tighten the relevant control, and rerun. Do not merely ask AI to “make it better.”

## Sean’s example prompt

> You are a consultant sizing the U.S. premium insulated drinkware market ($35 retail) for a DTC startup. Give a top-down annual estimate. Every assumption on its own line. Flag figures you are not confident in. Return a table with assumptions and confidence ratings, with the assumption, value, and source status clearly shown.

## Applied to the Charter engagement

### Thought-partner prompt

> You are a skeptical strategy-consulting thought partner. The client is Charter’s CEO, and the symptom is an 80% five-year share-price decline. Using the Q1 2026 case facts, propose three materially different definitions of the underlying problem. For each, show the implied issue-tree branches, the evidence that would falsify it, and what recommendation space it opens or closes. Do not recommend a strategy. Return concise bullets and flag assumptions.

### Virtual-expert analysis prompt

> You are a corporate-finance expert supporting Charter’s CEO. Determine what deterioration the April 24, 2026 share price appears to embed. Use only the supplied filings and verified market prices. Separate disclosed facts, derived values, and assumptions. Use cost-of-equity and WACC ranges rather than unsupported point estimates. Flag ownership, debt, Cox, and terminal-value limitations. Return an auditable Excel analysis with sources and confidence ratings.

### Human-controlled synthesis questions

- Which finding changes the recommendation?
- What evidence is strong enough to put in front of the CEO?
- What trade-off are we choosing?
- What must be true for the recommendation to work?
- What are we unwilling to claim?

AI can help answer and challenge these questions. The team owns the answers.
