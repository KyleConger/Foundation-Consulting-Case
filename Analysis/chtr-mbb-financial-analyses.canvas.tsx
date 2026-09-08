/**
 * McKinsey / Bain financial toolkit vs what this Charter engagement has done.
 * Live canvas. Project copy: Analysis/chtr-mbb-financial-analyses.canvas.tsx
 *
 * Sources for the toolkit (published, not internal): Koller/Goedhart/Wessels
 * Valuation (McKinsey); McKinsey on Finance (ROIC, reverse DCF, capital
 * allocation); Zook Profit from the Core and Bain Full Potential / Results
 * Delivery. Course overlay: CEO charge in FoC-Team-Case-Brief; Sternfels
 * “double market cap” in class notes. Analysis, not a filing.
 */
import {
  Callout,
  Card,
  CardBody,
  CardHeader,
  Divider,
  Grid,
  H1,
  H2,
  Pill,
  Row,
  Stack,
  Stat,
  Table,
  Text,
} from "cursor/canvas";

export default function ChtrMbbFinancialAnalyses() {
  return (
    <Stack gap={28}>
      <Stack gap={8}>
        <H1>McKinsey / Bain analyses on a problem like this</H1>
        <Text tone="secondary">
          The problem is not distress. It is a cash-generative company whose
          owners no longer believe the strategy. MBB would not open with a
          10-year DCF of Charter. They would diagnose what the market is
          pricing, where value is created or destroyed, then size a move in
          dollars and months — the CEO’s “what would it take, cost, and how
          long to matter.”
        </Text>
        <Row gap={8} wrap>
          <Pill tone="success">Diagnostic layer: done</Pill>
          <Pill tone="warning">Value layer: not started</Pill>
          <Pill tone="info">Fits Week 5 → Week 7, not a redo</Pill>
        </Row>
      </Stack>

      <Grid columns={3} gap={12}>
        <Stat value="6" label="Issue-tree tests already built" />
        <Stat value="2 of 9" label="MBB financial analyses complete" />
        <Stat value="3" label="Next analyses that feed the pitch" />
      </Grid>

      <Callout tone="info" title="Have we not done any?">
        You have done real financial analysis: volume vs price/mix, FCF vs
        capex mix, peer multiples, and an earnings-day event study. That is
        the diagnostic McKinsey would run before a model. What you have not
        done is convert a recommendation into equity value, cost, and time —
        which is what the rubric scores as “support” and “actionability.”
      </Callout>

      <H2>What they actually run (this problem, not the CFA list)</H2>
      <Table
        headers={["Analysis", "Firm / book", "What it answers here", "Status"]}
        columnAlign={["left", "left", "left", "left"]}
        rowTone={[
          "success",
          "success",
          "warning",
          "danger",
          "danger",
          "danger",
          "warning",
          "danger",
          "info",
        ]}
        rows={[
          [
            "Issue tree + hypothesis tests",
            "Both (standard)",
            "Is the problem Internet trajectory, capital allocation, or a cable multiple?",
            "Done — six charts, pass/fail",
          ],
          [
            "Revenue / profit bridge (volume vs price/mix)",
            "Both; McKinsey value-driver tree",
            "When did Internet dollars turn, not just subs?",
            "Done — Q1 2026; video app costs kept out",
          ],
          [
            "Trading comps (EV/EBITDA, FCF yield) + event study",
            "Both (IB-style comps; MBB uses them as a check)",
            "Charter-specific vs industry de-rate; what the tape prices",
            "Partial — snapshots + Apr 24 CHTR vs CMCSA, not a football field",
          ],
          [
            "Reverse DCF / market-implied expectations",
            "McKinsey Valuation; McKinsey on Finance",
            "What Internet run-rate and terminal multiple is ~$180 pricing vs ~$242 the day before?",
            "Not done — this is the “is it undervalued?” test O’Donnell flagged",
          ],
          [
            "ROIC vs WACC / economic profit by activity",
            "McKinsey Valuation; Bain economic profit",
            "Does growth in mobile create value, or only Internet?",
            "Not done — the reason the market will not net mobile against broadband",
          ],
          [
            "Unit economics (NPV per Internet sub vs mobile line)",
            "Both; Bain customer / loyalty economics",
            "ARPU, margin, churn, cost to acquire — why one sub is not one sub",
            "Not done — filings give ARPU and adds, not fully loaded CAC",
          ],
          [
            "Full potential vs current trajectory",
            "Bain Full Potential / Results Delivery; McKinsey “granularity of growth”",
            "How much equity value if Internet net adds go to zero vs stay at −120k run-rate",
            "Not done — needs a simple three-scenario model, not a full DCF",
          ],
          [
            "Initiative NPV / “size the prize”",
            "Both; maps 1:1 to the CEO charge",
            "Do X, targeting Y, funded by Z, over N months — FCF and print by year",
            "Not done — no recommendation yet, so no business case yet",
          ],
          [
            "Capital allocation / funding box",
            "McKinsey capital productivity; Bain M&A + cash deployment",
            "Buybacks vs network vs Cox leverage: what can you fund without a credit event",
            "Facts in hand (buybacks, 4.15–4.18x, Cox debt) — no decision math",
          ],
        ]}
        striped
      />
      <Text size="small" tone="tertiary">
        Toolkit from published McKinsey Valuation (Koller et al.), McKinsey on
        Finance, Bain Full Potential / Profit from the Core (Zook). Status vs
        this repo as of the issue-tree canvas. Assignment still anchors to Q1
        2026.
      </Text>

      <Divider />

      <Stack gap={8}>
        <H2>What they would not lead with</H2>
        <Text>
          A WACC-heavy 10-year DCF of the whole company is investment-banking
          work. MBB uses DCF as the engine inside reverse DCF and initiative
          cases, not as the pitch. Cost-cut / zero-based work is the wrong
          center of gravity: the brief says the company is not in distress.
          A kitchen-sink correlation matrix on 10 quarters is also not their
          method — you already discarded it (Internet adds vs FCF r = 0.08).
        </Text>
      </Stack>

      <Grid columns={2} gap={16}>
        <Card>
          <CardHeader trailing={<Pill tone="success">You have this</Pill>}>
            Diagnostic (Week 5)
          </CardHeader>
          <CardBody>
            <Text>
              Symptom vs problem: share price is the symptom; Internet
              trajectory plus belief is the problem. Dollars turned negative
              in Q1 2026. The tape prices YoY acceleration and consensus
              miss, not FCF. Peers de-rated; Charter more. Mobile is not a
              substitute in the multiple.
            </Text>
          </CardBody>
        </Card>
        <Card>
          <CardHeader trailing={<Pill tone="warning">Pitch still needs this</Pill>}>
            Value + feasibility (Week 7)
          </CardHeader>
          <CardBody>
            <Text>
              Three questions the CEO already asked: what to do, what it
              costs, how long until it shows up in the Internet print (because
              that is what Wall Street is looking at). That is reverse DCF +
              a three-scenario value bridge + one initiative case — not a
              fourth operating chart.
            </Text>
          </CardBody>
        </Card>
      </Grid>

      <H2>Build these three next — in MBB order</H2>
      <Table
        headers={["#", "Analysis", "How to keep it client-ready", "What “good” looks like"]}
        columnAlign={["right", "left", "left", "left"]}
        rows={[
          [
            "1",
            "Reverse DCF: what is priced in",
            "Hold WACC and terminal multiple in a tight range; solve for the Internet net-add path that equates to the Apr 23 vs Apr 24 market cap",
            "One slide: “$242 priced a shallow decline; $180 priced a structural one.” Ties O’Donnell’s undervalued comment to a number",
          ],
          [
            "2",
            "Internet vs mobile economic profit (or a crude SOP)",
            "Use disclosed Internet/mobile revenue, disclosed margins where they exist, and a stated assumption for mobile wholesale cost — label every assumption",
            "Shows why adding 368k mobile lines cannot offset −120k Internet in enterprise value",
          ],
          [
            "3",
            "Three-scenario equity bridge, then initiative NPV",
            "Base = current run-rate; “look-through” = Internet to zero net adds by 2028; “move” = your recommendation’s cost and year-by-year print",
            "“Do X, funded by Z, Internet print inflects in month N, equity value +$A to +$B.” That is the rubric",
          ],
        ]}
        striped
      />
      <Text size="small" tone="tertiary">
        Do not wait for a Week 5 “data pack” to start #1–2; filings already
        support a labeled, assumption-explicit version. The data pack, if it
        arrives, is for competitive grain (overbuild / FWA), not for replacing
        this math.
      </Text>

      <Callout tone="warning" title="Sternfels overlay (class notes)">
        Clients pay consultants to find ways to double market cap. On Charter,
        that is not “run a DCF until EV is 2×.” It is: name a move that can
        change the Internet run-rate the market is pricing, show the cost and
        the month it would show up in the print, and be honest if the honest
        answer is that no in-footprint network move does that inside 24
        months.
      </Callout>
    </Stack>
  );
}
