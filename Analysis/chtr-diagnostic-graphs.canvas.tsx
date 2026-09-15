/**
 * Live Cursor canvas. Project copy to pull from later:
 *   Analysis/chtr-diagnostic-graphs.canvas.tsx
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
  H3,
  LineChart,
  Pill,
  Row,
  Stack,
  Stat,
  Table,
  Text,
  useHostTheme,
} from "cursor/canvas";
import type { ChartTone } from "cursor/canvas";

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

/** Custom bars — Canvas BarChart clips / hides negatives when the axis zooms past 0. */
function SignedBarChart({
  categories,
  series,
  height = 240,
  valuePrefix = "",
  valueSuffix = "",
  yMin,
  yMax,
  zeroLabel = "0",
}: {
  categories: string[];
  series: Array<{ name: string; data: number[]; tone?: ChartTone }>;
  height?: number;
  valuePrefix?: string;
  valueSuffix?: string;
  yMin?: number;
  yMax?: number;
  zeroLabel?: string;
}) {
  const theme = useHostTheme();
  const pad = { top: 16, right: 12, bottom: 48, left: 52 };
  const width = Math.max(520, categories.length * (series.length > 1 ? 56 : 44));
  const innerW = width - pad.left - pad.right;
  const innerH = height - pad.top - pad.bottom;
  const all = series.flatMap((s) => s.data);
  const lo = yMin ?? Math.min(0, ...all) * 1.08;
  const hi = yMax ?? Math.max(0, ...all) * 1.08;
  const span = hi - lo || 1;
  const yScale = (v: number) => pad.top + ((hi - v) / span) * innerH;
  const zeroY = yScale(0);
  const groupW = innerW / categories.length;
  const barW = Math.min(18, (groupW * 0.7) / series.length);

  const toneFill = (tone: ChartTone | undefined, i: number) => {
    if (tone === "danger") return theme.category.red;
    if (tone === "warning") return theme.category.orange;
    if (tone === "success") return theme.category.green;
    if (tone === "info") return theme.category.blue;
    if (tone === "neutral") return theme.category.gray;
    const cycle = [
      theme.category.blue,
      theme.category.orange,
      theme.category.purple,
      theme.category.cyan,
    ] as const;
    return cycle[i % cycle.length];
  };

  const fmt = (v: number) => {
    const sign = v < 0 ? "−" : "";
    return `${sign}${valuePrefix}${Math.abs(v)}${valueSuffix}`;
  };

  const ticks = [lo, 0, hi].filter((v, i, a) => a.indexOf(v) === i);

  return (
    <Stack gap={6}>
      <svg width="100%" viewBox={`0 0 ${width} ${height}`} style={{ display: "block" }}>
        {ticks.map((t) => (
          <g key={t}>
            <line
              x1={pad.left}
              x2={width - pad.right}
              y1={yScale(t)}
              y2={yScale(t)}
              stroke={theme.stroke.tertiary}
              strokeWidth={t === 0 ? 1.5 : 1}
              strokeDasharray={t === 0 ? undefined : "3 3"}
            />
            <text
              x={pad.left - 6}
              y={yScale(t) + 3}
              textAnchor="end"
              fill={theme.text.tertiary}
              fontSize={10}
            >
              {t === 0 ? zeroLabel : fmt(Math.round(t * 10) / 10)}
            </text>
          </g>
        ))}
        {categories.map((cat, ci) => {
          const gx = pad.left + ci * groupW + groupW / 2;
          return (
            <g key={cat}>
              {series.map((s, si) => {
                const v = s.data[ci] ?? 0;
                const y0 = zeroY;
                const y1 = yScale(v);
                const top = Math.min(y0, y1);
                const h = Math.max(2, Math.abs(y1 - y0));
                const x =
                  gx - (series.length * barW + (series.length - 1) * 3) / 2 + si * (barW + 3);
                return (
                  <rect
                    key={s.name}
                    x={x}
                    y={top}
                    width={barW}
                    height={h}
                    fill={toneFill(s.tone, si)}
                  >
                    <title>{`${s.name}: ${fmt(v)}`}</title>
                  </rect>
                );
              })}
              <text
                x={gx}
                y={height - 10}
                textAnchor="middle"
                fill={theme.text.tertiary}
                fontSize={10}
              >
                {cat}
              </text>
            </g>
          );
        })}
      </svg>
      {series.length > 1 ? (
        <Row gap={12} wrap>
          {series.map((s, i) => (
            <span key={s.name} style={{ display: "inline-flex", alignItems: "center", gap: 6 }}>
              <span
                style={{
                  width: 10,
                  height: 10,
                  background: toneFill(s.tone, i),
                  display: "inline-block",
                }}
              />
              <Text size="small" tone="secondary">
                {s.name}
              </Text>
            </span>
          ))}
        </Row>
      ) : null}
    </Stack>
  );
}

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
        <SignedBarChart
          categories={QTRS}
          series={[
            {
              name: "Internet quarterly net adds (000s)",
              data: [-72, -148, -110, -177, -59, -116, -109, -119, -120, -172],
              tone: "danger",
            },
          ]}
          height={240}
          valueSuffix="k"
          yMin={-200}
          yMax={40}
          zeroLabel="0"
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
