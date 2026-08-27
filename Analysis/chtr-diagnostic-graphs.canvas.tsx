/**
 * Saved copy of the Cursor canvas "Charter diagnostic graphs."
 *
 * Live canvas (open beside chat):
 *   C:\Users\Owner\.cursor\projects\c-Users-Owner-Desktop-MAN6930-Case\canvases\chtr-diagnostic-graphs.canvas.tsx
 *
 * This file is the project copy to pull from later (git, other chats, teammates).
 * Keep the two in sync if the live canvas is edited.
 *
 * Content: which graphs/formulas to use for the CHTR case; Pearson r on
 * 2024Q1–2026Q2 from CHTR-Critical-Tables.xlsx Quarterly_Trend. Analysis,
 * not a filing. Do not mix into CORE-INFORMATION.md.
 */
import {
  BarChart,
  Callout,
  Card,
  CardBody,
  CardHeader,
  Divider,
  Grid,
  H1,
  H2,
  H3,
  LineChart,
  Pill,
  Row,
  Stack,
  Stat,
  Table,
  Text,
} from "cursor/canvas";

const QTRS = [
  "24Q1",
  "24Q2",
  "24Q3",
  "24Q4",
  "25Q1",
  "25Q2",
  "25Q3",
  "25Q4",
  "26Q1",
  "26Q2",
];

export default function ChtrDiagnosticGraphs() {
  return (
    <Stack gap={28}>
      <Stack gap={8}>
        <H1>What to plot for Charter — and what not to correlate</H1>
        <Text tone="secondary">
          The CEO charge is share-price trajectory. The Q1 2026 trigger was
          Internet net adds, not a cash-flow miss. Ten quarters of operating
          data will not produce a reliable Pearson r with the stock. Use
          identities and event charts, then one competitive overlay.
        </Text>
        <Row gap={8} wrap>
          <Pill tone="deleted">Internet is the priced variable</Pill>
          <Pill tone="warning">Mobile is not a substitute in the multiple</Pill>
          <Pill tone="neutral">FCF is a lagging residual</Pill>
        </Row>
      </Stack>

      <Callout tone="warning" title="Do not run a kitchen-sink correlation matrix">
        Pearson r on 10 quarters mostly captures a shared time trend. Mobile
        lines outstanding vs Internet customers outstanding is r = −0.995 —
        that is two near-linear series (one up, one down), not evidence that
        mobile causes broadband loss. Internet quarterly net adds vs FCF is r
        = 0.08: cash and the profit engine do not move together in the
        quarter, which is exactly why the market looks through FCF to
        subscribers.
      </Callout>

      <Row gap={24} wrap>
        <Stat value="0.08" label="r: Internet net adds vs FCF" />
        <Stat value="0.56" label="r: Internet customers vs revenue" />
        <Stat value="−0.995" label="r: mobile lines vs Internet (spurious)" tone="warning" />
        <Stat value="0.64" label="r: revenue vs Adj. EBITDA" />
      </Row>
      <Text size="small" tone="tertiary">
        Source: Quarterly_Trend in CHTR-Critical-Tables.xlsx · 2024Q1–2026Q2 ·
        restated customer basis · Pearson r, n = 10. 2024–2025 from unofficial
        trending (cross-check Ex99.1); 2026 from Ex99.1.
      </Text>

      <Stack gap={8}>
        <H2>Graph 1 — Internet net adds (the priced operating print)</H2>
        <Text>
          This is the series that crystallized the bear case. Q1 2026 −120k vs
          Q1 2025 −59k is the earnings-day trigger. Q2 2026 −172k is a later
          public fact after the assignment anchor.
        </Text>
        <BarChart
          categories={QTRS}
          series={[
            {
              name: "Internet quarterly net adds (000s)",
              data: [-72, -148, -110, -177, -59, -116, -109, -119, -120, -172],
              tone: "danger",
            },
          ]}
          beginAtZero={false}
          height={240}
          valueSuffix="k"
          referenceLines={[{ value: 0, label: "Zero net adds", tone: "neutral" }]}
        />
        <Text size="small" tone="tertiary">
          Internet quarterly net additions (thousands) · Source: trending /
          Ex99.1 · 2024Q1–2026Q2
        </Text>
      </Stack>

      <Grid columns={2} gap={20}>
        <Stack gap={8}>
          <H2>Graph 2 — Mix the market will not net</H2>
          <Text>
            Mobile lines rise while Internet customers fall. Management
            presents “connectivity”; the multiple still prices Internet.
          </Text>
          <LineChart
            categories={QTRS}
            series={[
              {
                name: "Internet customers (000s)",
                data: [
                  30518, 30370, 30260, 30083, 30024, 29908, 29799, 29680,
                  29560, 29388,
                ],
                tone: "danger",
              },
              {
                name: "Mobile lines (000s)",
                data: [
                  8244, 8796, 9336, 9858, 10365, 10856, 11338, 11766, 12134,
                  12540,
                ],
                tone: "success",
              },
            ]}
            beginAtZero={false}
            height={240}
            valueSuffix="k"
          />
          <Text size="small" tone="tertiary">
            Period-end customers (000s) · restated basis · Source: trending /
            Ex99.1
          </Text>
        </Stack>
        <Stack gap={8}>
          <H2>Graph 3 — Cash does not rescue the multiple</H2>
          <Text>
            Adj. EBITDA is sticky; FCF swings with capex and accrued PP&E.
            Buybacks convert that residual into EPS. The stock still fell.
          </Text>
          <LineChart
            categories={QTRS}
            series={[
              {
                name: "Adj. EBITDA ($M)",
                data: [
                  5497, 5665, 5647, 5760, 5763, 5693, 5561, 5691, 5637, 5449,
                ],
                tone: "info",
              },
              {
                name: "Free cash flow ($M)",
                data: [358, 1296, 1619, 984, 1564, 1046, 1621, 773, 1372, 969],
                tone: "warning",
              },
            ]}
            beginAtZero={false}
            height={240}
            valuePrefix="$"
            valueSuffix="M"
          />
          <Text size="small" tone="tertiary">
            Charter-defined non-GAAP · Source: trending / Ex99.1 · 2024Q1–2026Q2
          </Text>
        </Stack>
      </Grid>

      <Divider />

      <Stack gap={10}>
        <H2>Formulas that actually move a recommendation</H2>
        <Text>
          Prefer accounting identities and bridges over r. These six are the
          ones a CEO can act on.
        </Text>
      </Stack>

      <Grid columns={2} gap={16}>
        <Card>
          <CardHeader>1. Internet revenue bridge (volume vs price/mix)</CardHeader>
          <CardBody>
            <Text>
              Δ Internet revenue ≈ (Δ customers × prior ARPU) + (Δ ARPU ×
              ending customers) ± bundle allocation. FY2025 10-K already
              splits this: +$785M rate/mix, −$380M fewer average residential
              Internet customers. Q1 2026 is when volume beat price: Internet
              revenue itself fell 1.3%. If you cannot show this bridge
              turning, the multiple will not.
            </Text>
          </CardBody>
        </Card>
        <Card>
          <CardHeader>2. One more Internet sub vs one more mobile line</CardHeader>
          <CardBody>
            <Text>
              Incremental contribution ≈ Δ revenue − Δ variable cost (MVNO
              wholesale for mobile; programming is video, not Internet). The
              case turns on whether a mobile line’s margin can ever replace an
              Internet sub in EBITDA. If it cannot, “connectivity customers”
              is a reporting construct, not a valuation construct.
            </Text>
          </CardBody>
        </Card>
        <Card>
          <CardHeader>3. FCF identity (why FCF can rise while the stock falls)</CardHeader>
          <CardBody>
            <Text>
              FCF = operating cash flow − PP&E ± change in accrued capex.
              FY2025 FCF rose 18% while Internet customers fell 403k. Capex
              guide ~$11.4B excluding Cox; network evolution is supposed to
              inflect after 2027. Plot FCF against upgrade/rebuild, not
              against Internet net adds.
            </Text>
          </CardBody>
        </Card>
        <Card>
          <CardHeader>4. What the market is discounting</CardHeader>
          <CardBody>
            <Text>
              Implied Internet trajectory: if the current run-rate of ~120–170k
              quarterly Internet losses persists, years to a 10% smaller
              Internet base ≈ 0.10 × 29.6M / 120k ≈ 25 quarters. Pair that
              with EV / LTM Adj. EBITDA (leverage 4.15–4.18x stated). The
              pitch is: which action changes that run-rate inside 24 months,
              at what cash cost.
            </Text>
          </CardBody>
        </Card>
        <Card>
          <CardHeader>5. Earnings-day event study (the actual correlation to solve)</CardHeader>
          <CardBody>
            <Text>
              For each earnings date: CHTR abnormal return vs Internet net-add
              surprise vs consensus, and vs FCF surprise. Q1 2026 is the
              extreme (−25% in one day on −120k Internet). If stock moves
              track Internet surprise and ignore FCF surprise, you have
              explained Wall Street’s lens. Need Yahoo/Bloomberg around
              30 Jan 2026, 24 Apr 2026, 24 Jul 2026 plus prior years.
            </Text>
          </CardBody>
        </Card>
        <Card>
          <CardHeader>6. Competitive overlay (the causal graph)</CardHeader>
          <CardBody>
            <Text>
              10-K: AT&T 100 Mbps+ overlap ~27% of footprint, Verizon ~16%.
              The graph that would solve causality is Internet net adds in
              fiber-overbuild vs FWA-heavy vs residual DMAs. Filings do not
              give DMA splits. Until a data pack does, treat fiber + FWA +
              housing (fewer moves) as jointly identified — do not attribute
              all −120k to one rival.
            </Text>
          </CardBody>
        </Card>
      </Grid>

      <H2>Build these next — mapped to the issue tree</H2>
      <Table
        headers={["Chart", "Tests", "Pass / fail for a recommendation"]}
        columnAlign={["left", "left", "left"]}
        rowTone={["danger", "warning", "info", "neutral", "success", "warning"]}
        rows={[
          [
            "Internet net adds, 8–10 quarters, zero line",
            "Is the profit engine still shrinking, and did Q1 2026 break the prior slope?",
            "Any ‘trajectory’ claim must show this series inflecting, not just ARPU or mobile.",
          ],
          [
            "Internet customers vs mobile lines (two series)",
            "Will the market net mobile against broadband?",
            "If they do not (history says they do not), do not sell a connectivity-customer story as the fix.",
          ],
          [
            "Internet revenue waterfall: volume vs price/mix vs bundle allocation",
            "When did Internet dollars turn negative, not just subs?",
            "Q1 2026. Programmer-app costs netted in video are a separate distortion — keep them out of this bridge.",
          ],
          [
            "FCF vs upgrade/rebuild vs rural line extensions",
            "Is FCF weak because the engine is dying, or because 2026–27 capex is front-loaded?",
            "If FCF inflects only after 2027, that is a wait — not an out-of-the-box move.",
          ],
          [
            "CHTR vs CMCSA / peer EV/EBITDA and FCF yield, with buyback overlay",
            "Is this a Charter-specific belief problem or a cable-multiple problem?",
            "If peers de-rate too, the answer is industry structure. If Charter de-rates more, the answer is Internet trajectory + capital allocation.",
          ],
          [
            "Earnings-day return vs Internet surprise scatter",
            "What is Wall Street actually looking at?",
            "This is the correlation the brief asks you to find. Operating r’s among 10 quarters will not substitute.",
          ],
        ]}
        striped
      />

      <H3>What not to spend Week 5 on</H3>
      <Text>
        A 20-variable correlation heatmap of ARPU, voice, ads, CPE, and
        mobile net adds. Voice and video are secular; ads are political-year
        noise; CPE follows adds. Those belong in an appendix, not the CEO
        narrative. Cox close terms ($650M contribution cash / ~$12.4B net
        debt in the Q2 10-Q) change scale and leverage — they do not, by
        themselves, change the Internet slope the multiple is discounting.
      </Text>
    </Stack>
  );
}
