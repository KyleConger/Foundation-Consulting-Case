/**
 * Issue-tree charts for Charter (MAN6930) — six pass/fail tests.
 *
 * Live canvas (open beside chat):
 *   C:\Users\Owner\.cursor\projects\c-Users-Owner-Desktop-MAN6930-Case\canvases\chtr-issue-tree-charts.canvas.tsx
 *
 * Project copy: Analysis/chtr-issue-tree-charts.canvas.tsx
 *
 * Operating series: CHTR-Critical-Tables / Ex99.1 / unofficial trending.
 * Internet volume vs price/mix: derived (Δ avg Internet customers × prior-year
 * revenue per customer). FY2025 10-K published split is +$785M mix / −$380M
 * volume (residential). Programmer-app costs are video, not in this bridge.
 * Prices: Yahoo Finance close-to-close on earnings dates. CMCSA Apr 24 2026
 * from contemporaneous reporting. Analysis, not a filing.
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

export default function ChtrIssueTreeCharts() {
  return (
    <Stack gap={28}>
      <Stack gap={8}>
        <H1>Issue-tree charts — six tests for a Charter recommendation</H1>
        <Text tone="secondary">
          Each chart is a pass/fail for a CEO claim. Assignment still anchors
          to Q1 2026; Q2 2026 is a later public fact and is labeled as such.
        </Text>
        <Row gap={8} wrap>
          <Pill tone="deleted">Internet still shrinking</Pill>
          <Pill tone="warning">Dollars turned in Q1 2026</Pill>
          <Pill tone="info">Industry de-rated; Charter more</Pill>
        </Row>
      </Stack>

      <Grid columns={4} gap={12}>
        <Stat value="−120k" label="Q1 2026 Internet net adds" tone="danger" />
        <Stat value="−172k" label="Q2 2026 Internet net adds (later)" tone="danger" />
        <Stat value="−25.5%" label="CHTR Apr 24 2026 (close)" tone="danger" />
        <Stat value="−13%" label="CMCSA same day" tone="warning" />
      </Grid>

      <Divider />

      <Stack gap={8}>
        <Row gap={8} align="center">
          <H2>1. Internet net adds — is the profit engine still shrinking?</H2>
          <Pill tone="deleted">Fail: no inflection</Pill>
        </Row>
        <Text>
          Test: did Q1 2026 break the prior slope? Q1 2025 was −59k; Q1 2026
          was −120k. Q2 2026 (−172k) is worse still. A trajectory claim that
          only cites ARPU or mobile fails this chart.
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
          referenceLines={[{ value: 0, label: "Zero", tone: "neutral" }]}
        />
        <Text size="small" tone="tertiary">
          Thousands · restated basis · Source: trending / Ex99.1 · 2024Q1–2026Q2
        </Text>
      </Stack>

      <Stack gap={8}>
        <Row gap={8} align="center">
          <H2>2. Internet customers vs mobile lines — will the market net them?</H2>
          <Pill tone="warning">Do not sell connectivity as the fix</Pill>
        </Row>
        <Text>
          Mobile lines rose from 8.2M to 12.5M while Internet customers fell
          from 30.5M to 29.4M. Apr 25 2025 the stock rallied on a mobile/video
          beat despite −59k Internet. Apr 24 2026 it did not: −120k Internet
          and +368k mobile, and the stock fell 25.5%. History since the
          assignment trigger says the multiple will not net the two.
        </Text>
        <LineChart
          categories={QTRS}
          series={[
            {
              name: "Internet customers (000s)",
              data: [
                30518, 30370, 30260, 30083, 30024, 29908, 29799, 29680, 29560,
                29388,
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
          Period-end, thousands · restated basis · Source: trending / Ex99.1
        </Text>
      </Stack>

      <Stack gap={8}>
        <Row gap={8} align="center">
          <H2>3. Internet revenue — volume vs price/mix (not video app costs)</H2>
          <Pill tone="deleted">Dollars turned Q1 2026</Pill>
        </Row>
        <Text>
          Derived bridge: change in average Internet customers × prior-year
          revenue per customer (volume), remainder is price/mix and bundle
          allocation. Programmer-app costs are netted in video revenue ($218M
          in Q1 2026 vs $47M; $251M in Q2 vs $67M) and are kept out of this
          chart. FY2025 10-K published split (+$785M mix, −$380M residential
          volume) is the audited analog; quarterly figures below are the same
          identity on trending/Ex99.1.
        </Text>
        <BarChart
          categories={QTRS}
          series={[
            {
              name: "Volume effect ($M)",
              data: [15, -20, -57, -85, -95, -91, -89, -84, -86, -98],
              tone: "danger",
            },
            {
              name: "Price / mix / allocation ($M)",
              data: [93, 93, 153, 136, 199, 254, 188, 123, 8, -95],
              tone: "info",
            },
          ]}
          height={260}
          valuePrefix="$"
          valueSuffix="M"
          referenceLines={[{ value: 0, label: "Zero", tone: "neutral" }]}
        />
        <Text size="small" tone="tertiary">
          YoY change in Internet revenue ($M) · Source: trending Internet
          revenue and customers; Q1–Q2 2026 revenue from Ex99.1 (5,852 and
          5,776)
        </Text>
        <LineChart
          categories={QTRS}
          series={[
            {
              name: "Internet revenue ($M)",
              data: [
                5826, 5806, 5872, 5856, 5930, 5969, 5971, 5895, 5852, 5776,
              ],
              tone: "danger",
            },
          ]}
          beginAtZero={false}
          height={200}
          valuePrefix="$"
          valueSuffix="M"
        />
        <Text size="small" tone="tertiary">
          Internet revenue ($M) · 2024–2025 trending; 2026 Ex99.1
        </Text>
        <Callout tone="warning" title="Pass/fail">
          Through 2025, price/mix more than offset volume. Q1 2026 mix is
          almost zero (+$8M) and total Internet revenue is −$78M YoY. Q2 2026
          mix is also negative (−$95M). The profit engine is now shrinking in
          dollars, not just in subscribers.
        </Callout>
      </Stack>

      <Stack gap={8}>
        <Row gap={8} align="center">
          <H2>4. FCF vs upgrade/rebuild vs rural line extensions</H2>
          <Pill tone="warning">Capex is front-loaded; FCF is not the multiple</Pill>
        </Row>
        <Text>
          If FCF is weak only because network evolution and rural spend peak
          in 2026–27, waiting until 2027 is a wait — not an out-of-the-box
          move. Upgrade/rebuild steps up into 2026; rural line extensions
          actually ease. FCF still swings with accrued capex, not with
          Internet net adds (r = 0.08).
        </Text>
        <LineChart
          categories={QTRS}
          series={[
            {
              name: "Free cash flow ($M)",
              data: [358, 1296, 1619, 984, 1564, 1046, 1621, 773, 1372, 969],
              tone: "warning",
            },
            {
              name: "Upgrade / rebuild ($M)",
              data: [481, 389, 358, 543, 395, 457, 484, 601, 675, 657],
              tone: "info",
            },
            {
              name: "Subsidized rural line extensions ($M)",
              data: [427, 565, 577, 575, 467, 543, 580, 612, 426, 390],
              tone: "neutral",
            },
          ]}
          beginAtZero
          height={260}
          valuePrefix="$"
          valueSuffix="M"
        />
        <Text size="small" tone="tertiary">
          $M · FCF is Charter non-GAAP · Capex NCTA categories from trending /
          Q1 10-Q trending / Q2 10-Q · 2026 guide ~$11.4B excluding Cox;
          network evolution targeted largely complete by end of 2027
        </Text>
      </Stack>

      <Divider />

      <Stack gap={8}>
        <Row gap={8} align="center">
          <H2>5. CHTR vs CMCSA — cable multiple or Charter-specific?</H2>
          <Pill tone="info">Both de-rated; Charter more</Pill>
        </Row>
        <Text>
          Apr 24 2026 is the clean test: Comcast had already reported (beat)
          and still fell ~13% the next day as Charter printed. Charter fell
          25.5%. Industry structure is in the multiple; Internet trajectory
          plus capital allocation is the extra Charter gap.
        </Text>
        <BarChart
          categories={["Apr 24 2026 close-to-close"]}
          series={[
            { name: "CHTR", data: [-25.5], tone: "danger" },
            { name: "CMCSA", data: [-12.9], tone: "warning" },
          ]}
          height={200}
          valueSuffix="%"
        />
        <Text size="small" tone="tertiary">
          CHTR: Yahoo close $241.78 → $180.13. CMCSA: TIKR/Deadline ~$31.64 →
          $27.51 (−12.9% to −13%).
        </Text>
        <Table
          headers={["Snapshot", "CHTR", "CMCSA", "Read"]}
          columnAlign={["left", "right", "right", "left"]}
          rows={[
            [
              "EV / EBITDA (published, ~Apr 2026)",
              "6.06x (Devyara Apr 26)",
              "5.65x / 5.47x fwd (TIKR)",
              "Same neighborhood — not a 2-turn Charter-only discount on EBITDA",
            ],
            [
              "ValueSense CHTR LTM EV/EBITDA",
              "5.8x YE2025 → 5.6x Q2 2026",
              "—",
              "Multiple compressed as the Internet print worsened",
            ],
            [
              "FCF (FY2025)",
              "$5.0B",
              "$19.2B",
              "Both still cash-generative",
            ],
            [
              "Mkt cap × FCF (order of magnitude, Apr 2026)",
              "~$22–31B cap vs $5B FCF → mid-teens to 20%+ yield after the crash",
              "~$100B cap vs ~$19B FCF → ~19% (pre-guide-down)",
              "High FCF yield is the sector, not a Charter-only gift",
            ],
            [
              "FY2025 buybacks",
              "17.1M shares / ~$5.4B",
              "Returned capital (div + buyback); not 1:1",
              "Charter buybacks did not support the price into Q1 2026",
            ],
          ]}
          striped
        />
        <Text>
          Price path while buybacks continued (Yahoo close on earnings dates):
        </Text>
        <LineChart
          categories={[
            "Jan 31 25",
            "Apr 25 25",
            "Jul 25 25",
            "Oct 31 25",
            "Jan 30 26",
            "Apr 24 26",
            "Jul 24 26",
          ]}
          series={[
            {
              name: "CHTR close on earnings date ($)",
              data: [345.49, 373.65, 309.75, 233.84, 206.12, 180.13, 123.31],
              tone: "danger",
            },
          ]}
          beginAtZero={false}
          height={220}
          valuePrefix="$"
        />
        <Text size="small" tone="tertiary">
          Yahoo Finance daily close on the earnings date · not split-adjusted
          beyond what Yahoo reports (no CHTR split in period)
        </Text>
      </Stack>

      <Stack gap={8}>
        <Row gap={8} align="center">
          <H2>6. Earnings-day return vs Internet print</H2>
          <Pill tone="deleted">Not a straight line — YoY acceleration is</Pill>
        </Row>
        <Text>
          Close-to-close on the announcement date. This is the correlation the
          brief asks for. Absolute Internet losses of ~110–120k produced
          +7.6%, −18.5%, and −25.5% depending on whether the print was an
          improvement vs last year or a doubling. Consensus miss (Q2 2025:
          −116k vs ~−73k expected) also sold the stock.
        </Text>
        <BarChart
          categories={[
            "Q4'24 −177k",
            "Q1'25 −59k",
            "Q2'25 −116k",
            "Q3'25 −109k",
            "Q4'25 −119k",
            "Q1'26 −120k",
            "Q2'26 −172k",
          ]}
          series={[
            {
              name: "Earnings-day close-to-close (%)",
              data: [2.6, 11.4, -18.5, 1.3, 7.6, -25.5, -2.5],
              tone: "danger",
            },
          ]}
          beginAtZero={false}
          height={240}
          valueSuffix="%"
          referenceLines={[{ value: 0, label: "Flat", tone: "neutral" }]}
        />
        <Text size="small" tone="tertiary">
          Yahoo: Jan 31 2025 $336.62→$345.49; Apr 25 2025 $335.33→$373.65; Jul
          25 2025 $380.00→$309.75; Oct 31 2025 $230.92→$233.84 (open $218,
          −5.6% gap); Jan 30 2026 $191.52→$206.12; Apr 24 2026
          $241.78→$180.13; Jul 24 2026 $126.50→$123.31 (open $111.80, −11.6%
          gap)
        </Text>
        <Table
          headers={[
            "Print",
            "Internet net adds",
            "vs year-ago",
            "1-day %",
            "What the tape did",
          ]}
          columnAlign={["left", "right", "right", "right", "left"]}
          rowTone={[
            undefined,
            "success",
            "danger",
            undefined,
            "info",
            "danger",
            "warning",
          ]}
          rows={[
            ["Jan 31 2025 / Q4 2024", "−177k", "n/a in this window", "+2.6%", "Losses large but not a new slope"],
            ["Apr 25 2025 / Q1 2025", "−59k", "better than −72k", "+11.4%", "Mobile/video beat; Internet miss ignored"],
            ["Jul 25 2025 / Q2 2025", "−116k", "better than −148k", "−18.5%", "Miss vs ~73k expected (Visible Alpha/Reuters)"],
            ["Oct 31 2025 / Q3 2025", "−109k", "flat vs −110k", "+1.3% close / −5.6% open", "EPS miss; close recovered"],
            ["Jan 30 2026 / Q4 2025", "−119k", "better than −177k", "+7.6%", "Absolute losses similar to Q1 2026, opposite tape"],
            ["Apr 24 2026 / Q1 2026", "−120k", "double −59k", "−25.5%", "Assignment trigger. CMCSA −13% same day"],
            ["Jul 24 2026 / Q2 2026", "−172k", "worse than −116k", "−2.5% close / −11.6% open", "Later public fact; already de-rated"],
          ]}
          striped
        />
        <Callout tone="info" title="What Wall Street is looking at">
          Not FCF (r = 0.08 vs Internet adds). Not the stock of mobile lines.
          The tape prices Internet surprise and YoY acceleration. Q4 2025
          (−119k, improvement vs −177k) rallied; Q1 2026 (−120k, double −59k)
          collapsed. Any recommendation has to change that Internet run-rate
          inside ~24 months, or explain why the multiple should look through
          it — which it has not.
        </Callout>
      </Stack>

      <Card>
        <CardHeader trailing={<Pill tone="deleted">Six tests</Pill>}>
          Scorecard for the Week 5 pack
        </CardHeader>
        <CardBody>
          <Table
            headers={["Chart", "Result", "Implication for the pitch"]}
            columnAlign={["left", "left", "left"]}
            rowTone={["danger", "warning", "danger", "warning", "info", "danger"]}
            rows={[
              [
                "Internet net adds, zero line",
                "Still negative; Q1 2026 doubled YoY; Q2 worse",
                "Cannot claim an operating inflection from ARPU or mobile",
              ],
              [
                "Internet vs mobile",
                "Mobile +3.7M lines; Internet −1.1M customers over the window",
                "Do not sell total connectivity customers as the valuation fix",
              ],
              [
                "Internet $ waterfall",
                "Mix covered volume until Q1 2026; Q2 mix also negative",
                "The engine is now shrinking in dollars",
              ],
              [
                "FCF vs upgrade vs rural",
                "Upgrade/rebuild up; rural easing; FCF noisy",
                "Waiting for 2027 capex roll-off is not the CEO charge",
              ],
              [
                "CHTR vs CMCSA",
                "Both sold Apr 24; CHTR −25.5% vs CMCSA −13%",
                "Industry structure + a Charter-specific Internet/belief gap",
              ],
              [
                "Earnings-day vs Internet",
                "YoY acceleration and consensus miss, not the absolute −120k",
                "That is the market lens the recommendation must change",
              ],
            ]}
            striped
          />
        </CardBody>
      </Card>
    </Stack>
  );
}
