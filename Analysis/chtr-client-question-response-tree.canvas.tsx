/**
 * Diagnostic response tree for the bite-sized CEO questions.
 * Pairs with chtr-industry-vs-firm-framestorm.canvas.tsx
 * Method: one answer at a time → what it shows → where to go next.
 */
import {
  Callout,
  Card,
  CardBody,
  CardHeader,
  CollapsibleSection,
  Divider,
  H1,
  H2,
  Pill,
  Row,
  Stack,
  Swatch,
  Table,
  Text,
  computeDAGLayout,
  useHostTheme,
} from "cursor/canvas";

type Branch = {
  ifTheySay: string;
  shows: string;
  favors: string;
  next: string;
};

function BranchTable({ rows }: { rows: Branch[] }) {
  return (
    <Table
      headers={["If they say…", "What it shows", "Favors", "Next"]}
      columnAlign={["left", "left", "left", "left"]}
      rows={rows.map((r) => [
        r.ifTheySay,
        r.shows,
        r.favors,
        r.next,
      ])}
      striped
    />
  );
}

function FlowDag() {
  const theme = useHostTheme();
  const layout = computeDAGLayout({
    nodes: [
      { id: "q1" },
      { id: "q2" },
      { id: "stop" },
      { id: "q3" },
      { id: "rootA" },
      { id: "causes" },
      { id: "q8" },
      { id: "q9" },
    ],
    edges: [
      { from: "q1", to: "q2" },
      { from: "q2", to: "stop" },
      { from: "q2", to: "q3" },
      { from: "q3", to: "rootA" },
      { from: "q3", to: "causes" },
      { from: "causes", to: "q8" },
      { from: "rootA", to: "q8" },
      { from: "q8", to: "q9" },
    ],
    direction: "vertical",
    nodeWidth: 150,
    nodeHeight: 44,
    rankGap: 48,
    nodeGap: 28,
    padding: 12,
  });

  const labels: Record<string, string> = {
    q1: "Q1 Observe",
    q2: "Q2 How know?",
    stop: "Stop / measure",
    q3: "Q3 vs CMCSA",
    rootA: "Lean Root A",
    causes: "Q4–Q7 causes",
    q8: "Q8 Said no",
    q9: "Q9 Rank + kill",
  };

  const byId = Object.fromEntries(layout.nodes.map((n) => [n.id, n]));

  return (
    <div style={{ position: "relative", width: layout.width, height: layout.height }}>
      <svg
        width={layout.width}
        height={layout.height}
        style={{ position: "absolute", inset: 0 }}
      >
        {layout.edges.map((e, i) => (
          <line
            key={i}
            x1={e.sourceX}
            y1={e.sourceY}
            x2={e.targetX}
            y2={e.targetY}
            stroke={theme.stroke.secondary}
            strokeWidth={1.5}
            strokeDasharray={e.to === "stop" ? "4 4" : undefined}
          />
        ))}
      </svg>
      {layout.nodes.map((n) => (
        <div
          key={n.id}
          style={{
            position: "absolute",
            left: n.x,
            top: n.y,
            width: 150,
            height: 44,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            textAlign: "center",
            padding: "4px 6px",
            background: theme.bg.elevated,
            border: `1px solid ${theme.stroke.primary}`,
            color: theme.text.primary,
            fontSize: 12,
            lineHeight: 1.2,
          }}
        >
          {labels[n.id]}
        </div>
      ))}
    </div>
  );
}

export default function ChtrClientQuestionResponseTree() {
  return (
    <Stack gap={24}>
      <Stack gap={8}>
        <Row gap={8} wrap>
          <Pill tone="info">Diagnostic tree</Pill>
          <Pill tone="warning">Ask in order · one answer each</Pill>
        </Row>
        <H1>What each client answer can show</H1>
        <Text tone="secondary">
          Maps the bite-sized CEO questions to frame weight: Root A (industry
          share-shift), Root B (Charter-relative), Root C (market lens / Internet
          print). Also flags data-quality dead ends so you do not treat narrative
          as measurement.
        </Text>
      </Stack>

      <Callout tone="info" title="How to use this">
        Do not skip to Q4–Q7. Q1–Q2 are gates on whether you can trust any cause
        story. Q3 is the cheap A-vs-B fork. Q9 is synthesis only after the rest.
      </Callout>

      <Stack gap={8}>
        <H2>Master flow</H2>
        <FlowDag />
        <Text size="small" tone="tertiary">
          Dashed path = stop cause questions until you have measurement.
        </Text>
      </Stack>

      <Divider />

      <CollapsibleSection
        title="Q1 · What did you actually see about Internet losses?"
        count={4}
        leading={<Swatch color="blue" />}
        trailing={<Pill size="sm">Gate · observation</Pill>}
        defaultOpen
      >
        <BranchTable
          rows={[
            {
              ifTheySay: "Internet losses accelerated YoY (≈ doubled vs Q1’25)",
              shows: "Confirms the assignment trigger as an operating fact, not just a stock story",
              favors: "Proceed — symptom locked",
              next: "Q2 (how do you know?)",
            },
            {
              ifTheySay: "Losses happened but improved vs plan / vs last year",
              shows: "Their internal scoreboard disagrees with the public print — or they are talking a different base",
              favors: "Neither A nor B yet",
              next: "Reconcile restated vs old customers, then re-ask Q1 on Internet only",
            },
            {
              ifTheySay: "Connectivity / mobile grew, so the Internet print is overweighted",
              shows: "Strategy narrative vs market lens conflict (diagnostic canvas)",
              favors: "Root C is live; does not clear A vs B",
              next: "Still force Q1/Q2 on Internet customers alone",
            },
            {
              ifTheySay: "We do not see it at that grain / I don’t know the number",
              shows: "CEO office may be one level above the operating file",
              favors: "Data gap",
              next: "Ask who owns the Internet P&L file; do not invent causes",
            },
          ]}
        />
      </CollapsibleSection>

      <CollapsibleSection
        title="Q2 · How do you know — measured, coded, or inferred?"
        count={4}
        leading={<Swatch color="cyan" />}
        trailing={<Pill size="sm">Gate · epistemology</Pill>}
        defaultOpen
      >
        <BranchTable
          rows={[
            {
              ifTheySay: "Sampled calls / truck rolls / CRM outcomes (direct)",
              shows: "Cause questions can be asked; still check coding bias later",
              favors: "Usable evidence path",
              next: "Q3",
            },
            {
              ifTheySay: "Agent- or sales-coded win/loss reasons only",
              shows: "Looks like data; class caution — favorite codes distort",
              favors: "Treat as ESTIMATED",
              next: "Q3, but discount Q4–Q7 until a sample audit exists",
            },
            {
              ifTheySay: "Inference / ‘competitive environment’ narrative",
              shows: "No observation underneath the industry story",
              favors: "Cannot pick A vs B from this",
              next: "Stop cause tree; build a measurement plan (Week 5 / DMA)",
            },
            {
              ifTheySay: "No win/loss file; we do not log that",
              shows: "Firm is flying without the instrument Root B needs",
              favors: "Process gap (firm) even if industry wind is real",
              next: "Flag as hard diligence item; skip to what *is* measured (overlap %, promo)",
            },
          ]}
        />
      </CollapsibleSection>

      <CollapsibleSection
        title="Q3 · Did anyone compare your YoY Internet slope to Comcast’s?"
        count={4}
        leading={<Swatch color="purple" />}
        trailing={<Pill size="sm">A vs B fork</Pill>}
        defaultOpen
      >
        <BranchTable
          rows={[
            {
              ifTheySay: "Yes — mix-adjusted — our gap remains",
              shows: "Same wind, worse relative game",
              favors: "Root B",
              next: "Q4–Q7 to find which lever (fiber / FWA / price / service)",
            },
            {
              ifTheySay: "Yes — after footprint / overbuild mix, gap vanishes",
              shows: "Peer gap was composition, not GTM skill",
              favors: "Root A",
              next: "Skim Q4–Q5 for which industry mechanism; deprioritize Charter-only GTM",
            },
            {
              ifTheySay: "Compared raw totals only (no mix)",
              shows: "A vs B still unresolved — the cheap gate is half-done",
              favors: "Incomplete",
              next: "Do mix control before heavy cause work",
            },
            {
              ifTheySay: "Never compared to Comcast that way",
              shows: "Team (and maybe client) skipped the cheapest industry-vs-firm test",
              favors: "Homework, not diagnosis",
              next: "Run the comparison yourselves; return to Q3 before Q9",
            },
          ]}
        />
      </CollapsibleSection>

      <Divider />

      <Text weight="semibold">Cause branches (only after Q1–Q3 clear)</Text>

      <CollapsibleSection
        title="Q4 · What share of losses sat in fiber-overbuild zips?"
        count={3}
        leading={<Swatch color="orange" />}
      >
        <BranchTable
          rows={[
            {
              ifTheySay: "Most losses in high fiber-overlap zips",
              shows: "FTTH share-shift is the dominant local physics",
              favors: "Root A · fiber mechanism",
              next: "Q5 still — FWA can coexist; Q6 if peers keep more in same zips",
            },
            {
              ifTheySay: "Most losses outside heavy fiber overlap",
              shows: "Not primarily an overbuild story in the loss file",
              favors: "Weakens pure fiber-A; opens FWA / price / service",
              next: "Q5, then Q6–Q7",
            },
            {
              ifTheySay: "No zip / DMA split",
              shows: "Cannot separate industry structure from footprint luck",
              favors: "Blocks clean A vs B",
              next: "Prioritize DMA overlay before recommending firm GTM",
            },
          ]}
        />
      </CollapsibleSection>

      <CollapsibleSection
        title="Q5 · What share do you attribute to FWA — measured or estimated?"
        count={4}
        leading={<Swatch color="yellow" />}
      >
        <BranchTable
          rows={[
            {
              ifTheySay: "High share, measured (porting / win-loss / panel)",
              shows: "FWA is a real taker of Internet homes",
              favors: "Root A · FWA mechanism",
              next: "Q6 — if you are priced above FWA while CMCSA closed the gap, lean B",
            },
            {
              ifTheySay: "High share, estimated / narrative only",
              shows: "Convenient industry story without instrumentation",
              favors: "Weak A",
              next: "Get a measured split; do not size a fix on this alone",
            },
            {
              ifTheySay: "Low FWA share",
              shows: "Attacker mix is elsewhere (fiber, moves, voluntary churn)",
              favors: "Not FWA-A",
              next: "Q4 / Q7 / housing residual",
            },
            {
              ifTheySay: "We cannot separate FWA from ‘wireless broadband’ / other",
              shows: "Category blur in the file",
              favors: "Data quality",
              next: "Redefine codes before using FWA in the pitch",
            },
          ]}
        />
      </CollapsibleSection>

      <CollapsibleSection
        title="Q6 · In the worst overlap zips, how did Spectrum promo price compare?"
        count={3}
        leading={<Swatch color="green" />}
      >
        <BranchTable
          rows={[
            {
              ifTheySay: "We were materially more expensive than FWA / fiber promos",
              shows: "A switcher’s math favored the attacker; peers may have matched sooner",
              favors: "Root B · price / promo lever",
              next: "Q7 only to see if price was the whole story; then Q8–Q9",
            },
            {
              ifTheySay: "Parity or cheaper — still lost",
              shows: "Not a sticker-price problem in those zips",
              favors: "Not price-B; back toward A or service-B",
              next: "Q7 product/service; revisit fiber/FWA intensity",
            },
            {
              ifTheySay: "We do not systematically shop competitor offers by zip",
              shows: "Blind on the firm lever most CEOs reach for first",
              favors: "Process gap under B",
              next: "Competitor price shop is a cheap analysis before any price recommendation",
            },
          ]}
        />
      </CollapsibleSection>

      <CollapsibleSection
        title="Q7 · What share cited speed, WiFi, reliability, or service pain?"
        count={3}
        leading={<Swatch color="red" />}
      >
        <BranchTable
          rows={[
            {
              ifTheySay: "High share, from sampled truth (not just codes)",
              shows: "Product/experience failure is binding in the loss file",
              favors: "Root B · ops / WiFi / reliability",
              next: "Q8 for whether refusals already name the same pain",
            },
            {
              ifTheySay: "Low / competitive on service metrics",
              shows: "Not an experience story",
              favors: "Weakens service-B",
              next: "Weight Q4–Q6 more; do not pitch ‘better service’ as the trajectory fix",
            },
            {
              ifTheySay: "High only in agent codes; sample disagrees",
              shows: "Classic coding distortion (O’Donnell call-center lesson)",
              favors: "Discard the code; keep the sample",
              next: "Re-run Q7 on the sample only",
            },
          ]}
        />
      </CollapsibleSection>

      <Divider />

      <CollapsibleSection
        title="Q8 · Who has already said no — and is it in the file?"
        count={4}
        leading={<Swatch color="pink" />}
        trailing={<Pill size="sm">Refusal inventory</Pill>}
      >
        <BranchTable
          rows={[
            {
              ifTheySay: "Named MDUs / bulk / landlords refused current Internet offer",
              shows: "Planogram / gatekeeper room is live — not only household switchers",
              favors: "Root B · access / bulk channel",
              next: "Q9 with that channel as a candidate lever",
            },
            {
              ifTheySay: "Win-back or save desk systematically loses to a named offer",
              shows: "Concrete competitive ‘no’ with a price/product object",
              favors: "B if peer handles saves better; A if the offer is structurally unbeatable",
              next: "Tie to Q6 object; Q9 kill rule on that offer",
            },
            {
              ifTheySay: "Wall Street / rating agencies rejected the connectivity story",
              shows: "Belief refusal — matches Root C and the Apr 24 tape",
              favors: "Root C",
              next: "Q9 must change the Internet print path, not the IR deck",
            },
            {
              ifTheySay: "Nobody has said no / we never logged refusals",
              shows: "Either no systematic external veto, or the team never looked",
              favors: "Empty cupboard — high self-risk of ratifying the current plan",
              next: "Q9 only after forcing one external ‘no’ search (buyer, save desk, MDU)",
            },
          ]}
        />
      </CollapsibleSection>

      <CollapsibleSection
        title="Q9 · Which one factor, and what would change your mind?"
        count={4}
        leading={<Swatch color="gray" />}
        trailing={<Pill size="sm">Synthesis only</Pill>}
        defaultOpen
      >
        <BranchTable
          rows={[
            {
              ifTheySay: "Names one factor + a clear kill / update rule",
              shows: "Client can decide; frame set is usable",
              favors: "Whatever they named — if it matches Q3–Q8 evidence",
              next: "Build the work plan on that factor; write the kill rule into the pitch",
            },
            {
              ifTheySay: "Industry only — with no mix-adjusted peer evidence",
              shows: "Anchoring on Root A; may be avoiding firm accountability",
              favors: "Challenge A",
              next: "Return to Q3; do not accept A as settled",
            },
            {
              ifTheySay: "Everything / ‘perfect storm’",
              shows: "Unfalsifiable — universality failure",
              favors: "No frame",
              next: "Force a rank order; pick the top lever only",
            },
            {
              ifTheySay: "Stock is undervalued; keep buying back / wait for 2027",
              shows: "Decision architecture / founder’s head — demoted in the framestorm",
              favors: "Not a diagnosis",
              next: "Redirect to Internet run-rate inside ~24 months (hard gate C)",
            },
          ]}
        />
      </CollapsibleSection>

      <Divider />

      <Card>
        <CardHeader>Terminal leaves — what you are allowed to claim</CardHeader>
        <CardBody>
          <Table
            headers={["Evidence path", "Claim you can make", "Claim you cannot make"]}
            columnAlign={["left", "left", "left"]}
            rowTone={["danger", "warning", "info", undefined]}
            rows={[
              [
                "Q2 = inference only, or no file",
                "We lack the instrumentation to separate industry from firm",
                "Any confident Root A or B pitch",
              ],
              [
                "Q3 = mix-adjusted gap gone",
                "Industry structure dominates; peer gap was footprint",
                "‘Charter uniquely mismanaged broadband’",
              ],
              [
                "Q3 = mix-adjusted gap remains + Q6 or Q7 measured",
                "Firm lever exists inside the industry wind",
                "‘Only industry — nothing to do’",
              ],
              [
                "Q8/Q9 = belief refusal without Internet path",
                "Market lens (C) is binding for share-price trajectory",
                "IR / buyback as the trajectory fix",
              ],
            ]}
            striped
          />
        </CardBody>
      </Card>

      <Callout tone="warning" title="Discipline">
        One question, then stop. Record which branch you are on before asking
        the next. If two people answer different branches for Q2, you do not yet
        have a team diagnosis — you have a data fight.
      </Callout>

      <Text size="small" tone="tertiary">
        Pairs with chtr-industry-vs-firm-framestorm.canvas.tsx · Root A/B/C as
        defined there · Assignment anchor end Q1 2026
      </Text>
    </Stack>
  );
}
