/**
 * Conversion analysis for the broadband-expansion diagnosis “what is still
 * missing” section: rural passings/capex vs Internet / CR relief vs CMCSA,
 * with rural split from the core footprint.
 * Assignment anchor Q1 2026; Q2 labeled later public fact.
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
  LineChart,
  Pill,
  Row,
  Stack,
  Stat,
  Table,
  Text,
  UsageBar,
  useHostTheme,
} from "cursor/canvas";
import type { ChartTone } from "cursor/canvas";

/** Custom bars — built-in BarChart clips negatives when the axis zooms past 0. */
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
  const pad = { top: 16, right: 12, bottom: 52, left: 56 };
  const width = Math.max(480, categories.length * (series.length > 1 ? 72 : 52));
  const innerW = width - pad.left - pad.right;
  const innerH = height - pad.top - pad.bottom;
  const all = series.flatMap((s) => s.data);
  const lo = yMin ?? Math.min(0, ...all) * 1.1;
  const hi = yMax ?? Math.max(0, ...all) * 1.1;
  const span = hi - lo || 1;
  const yScale = (v: number) => pad.top + ((hi - v) / span) * innerH;
  const zeroY = yScale(0);
  const groupW = innerW / categories.length;
  const barW = Math.min(22, (groupW * 0.72) / series.length);

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
    const sign = v < 0 ? "−" : v > 0 ? "+" : "";
    return `${sign}${valuePrefix}${Math.abs(v)}${valueSuffix}`;
  };

  const ticks = [lo, 0, hi].filter((v, i, a) => a.indexOf(v) === i);

  return (
    <Stack gap={6}>
      <svg width="100%" viewBox={`0 0 ${width} ${height}`} style={{ display: "block" }}>
        {ticks.map((t) => (
          <g key={String(t)}>
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
                const y1 = yScale(v);
                const top = Math.min(zeroY, y1);
                const h = Math.max(2, Math.abs(y1 - zeroY));
                const x =
                  gx -
                  (series.length * barW + (series.length - 1) * 4) / 2 +
                  si * (barW + 4);
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
                y={height - 12}
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
            <span
              key={s.name}
              style={{ display: "inline-flex", alignItems: "center", gap: 6 }}
            >
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

const QTRS = ["24Q2", "24Q3", "24Q4", "25Q1", "25Q2", "25Q3", "25Q4", "26Q1"] as const;

/** Rural CR net adds (000s). Sequential difference of trending stocks. */
const RURAL_CR_ADD = [39, 42, 42, 39, 48, 53, 46, 41];
/** Company CR net adds (000s). Trending / Ex99.1. */
const CO_CR_ADD = [-115, -75, -156, -54, -100, -87, -127, -163];
/** Core = company − rural. Identity, not a third source. */
const CORE_CR_ADD = CO_CR_ADD.map((c, i) => c - RURAL_CR_ADD[i]);
/** Company Internet net adds (000s). */
const CO_INET_ADD = [-148, -110, -177, -59, -116, -109, -119, -120];
/** ESTIMATED: rural CR treated as Internet-equivalent. */
const CORE_INET_PROXY = CO_INET_ADD.map((c, i) => c - RURAL_CR_ADD[i]);

const RURAL_PEN = [37.1, 37.1, 36.9, 37.6, 37.8, 38.3, 37.5, 38.1];
const CO_PEN = [57.8, 57.2, 56.7, 56.3, 55.7, 55.2, 54.5, 54.0];

export default function ChtrRuralCoreConversion() {
  return (
    <Stack gap={28}>
      <Stack gap={8}>
        <Row gap={8} wrap>
          <Pill tone="info">Conversion analysis</Pill>
          <Pill tone="warning">Fills diagnosis “what is still missing”</Pill>
          <Pill>Q1 2026 anchor · Q2 later</Pill>
        </Row>
        <H1>
          Rural is converting. The core is where the slope broke. Remainder
          cannot close Comcast.
        </H1>
        <Text tone="secondary">
          The expansion diagnosis asked for rural penetration and Internet
          contribution split from the core footprint — passings and grant
          drawdown are not the same as net-add relief. That split is now
          measured. Parent: chtr-broadband-expansion-diagnosis under Root B
          (chtr-base-frame).
        </Text>
      </Stack>

      <Callout tone="danger" title="Headline (Q1 2026)">
        Core (non-rural) lost 204k customer relationships. Rural added 41k —
        covering 20% of the core hole, already inside the company print of
        −163k. Rural’s quarterly add accelerated by only +2k vs Q1 2025, so it
        explains none of the −61k Internet YoY deterioration vs Comcast’s
        +118k (slope gap −179k).
      </Callout>

      <Grid columns={4} gap={12}>
        <Stat value="−204k" label="Core CR adds Q1’26 (company − rural)" tone="danger" />
        <Stat value="+41k" label="Rural CR adds Q1’26 (already in the print)" tone="info" />
        <Stat value="20%" label="Rural cover of the core hole (41 / 204)" tone="warning" />
        <Stat value="+2k" label="Rural add acceleration vs Q1’25 (41 − 39)" />
      </Grid>

      <UsageBar
        total={204}
        topLeftLabel="Rural covered 20% of the Q1 core CR hole"
        topRightLabel="+41k rural / 204k core losses"
        segments={[
          { id: "rural", value: 41, color: "blue" },
          { id: "uncovered", value: 163, color: "orange" },
        ]}
      />
      <Text size="small" tone="tertiary">
        Remainder of the bar is core CR losses still uncovered after rural.
        Source: A6 − A7 identity · Q1 2026 trending / Ex99.1.
      </Text>

      <Divider />

      <Stack gap={8}>
        <H2>1. Rural vs core customer-relationship flow</H2>
        <Text>
          Charter discloses subsidized-rural customer relationships as a
          subset of the company total. Subtracting them is retrieved
          arithmetic, not a new estimate. Company −163k in Q1 2026 is the
          mix of +41k rural and −204k core.
        </Text>
        <SignedBarChart
          categories={[...QTRS]}
          series={[
            { name: "Rural CR adds (000s)", data: RURAL_CR_ADD, tone: "info" },
            { name: "Core CR adds (000s)", data: CORE_CR_ADD, tone: "danger" },
          ]}
          height={260}
          valueSuffix="k"
          yMin={-230}
          yMax={70}
          zeroLabel="0"
        />
        <Text size="small" tone="tertiary">
          Thousands of customer relationships · rural stocks from Q1 2026
          trending “Subsidized Rural Construction Initiative” page · company
          stocks from the same schedule / Ex99.1. Core = company − rural.
          24Q1 rural add omitted (YE2023 rural stock not in the Q1’26 extract).
        </Text>
        <Table
          headers={["Quarter", "Rural CR add", "Company CR add", "Core CR add"]}
          columnAlign={["left", "right", "right", "right"]}
          rowTone={[
            undefined,
            undefined,
            undefined,
            undefined,
            undefined,
            undefined,
            undefined,
            "danger",
          ]}
          rows={QTRS.map((q, i) => [
            q,
            `+${RURAL_CR_ADD[i]}k`,
            `${CO_CR_ADD[i]}k`,
            `${CORE_CR_ADD[i]}k`,
          ])}
          striped
        />
      </Stack>

      <Stack gap={8}>
        <H2>2. Product competitiveness — penetration is stuck, not ramping</H2>
        <Text>
          Rural take of activated passings has sat in a 37–38% band for eight
          quarters while passings nearly tripled (582k → 1,385k). Company
          penetration fell from 57.8% to 54.0% over the same span. Flat rural
          take while the vintage ages is a competitiveness read, not just
          “build ahead of sell.”
        </Text>
        <Grid columns={3} gap={12}>
          <Stat value="38.1%" label="Rural pen of passings (Q1’26)" tone="warning" />
          <Stat value="54.0%" label="Company pen of passings (Q1’26)" />
          <Stat value="−16ppt" label="Rural vs company take gap" tone="danger" />
        </Grid>
        <LineChart
          categories={[...QTRS]}
          series={[
            { name: "Rural CR / rural passings (%)", data: RURAL_PEN, tone: "info" },
            {
              name: "Company CR / company passings (%)",
              data: CO_PEN,
              tone: "neutral",
            },
          ]}
          height={240}
          valueSuffix="%"
          beginAtZero={false}
          yMin={34}
          yMax={60}
        />
        <Text size="small" tone="tertiary">
          Penetration = residential + small-business customer relationships /
          estimated passings. Source: Q1 2026 trending schedule. If the 1.385M
          rural passings reached company 54% take: 748k CR vs 527k actual —
          221k “missing” on plant already lit (D4).
        </Text>
      </Stack>

      <Divider />

      <Stack gap={8}>
        <H2>3. Internet trajectory — rural does not move the YoY slope</H2>
        <Text>
          Rural CR adds are the closest public proxy for rural Internet (new
          plant; Spectrum Mobile requires Internet). Tag ESTIMATED on that
          identity. Even generously, rural added 41k in Q1 while company
          Internet fell 120k, so the core Internet proxy is −161k. Comcast
          domestic residential broadband: −65k.
        </Text>
        <SignedBarChart
          categories={[...QTRS]}
          series={[
            {
              name: "Company Internet (000s)",
              data: CO_INET_ADD,
              tone: "warning",
            },
            {
              name: "Core Internet proxy (000s)",
              data: CORE_INET_PROXY,
              tone: "danger",
            },
            { name: "Rural CR adds (000s)", data: RURAL_CR_ADD, tone: "info" },
          ]}
          height={260}
          valueSuffix="k"
          yMin={-240}
          yMax={70}
          zeroLabel="0"
        />
        <Table
          headers={["Q1 comparison", "Figure", "Tag"]}
          columnAlign={["left", "right", "left"]}
          rowTone={["danger", "info", "danger", "warning", "danger"]}
          rows={[
            ["CHTR Internet adds", "−120k", "RETRIEVED Ex99.1"],
            ["Rural CR adds (Internet proxy)", "+41k", "RETRIEVED CR; ESTIMATED as Internet"],
            ["Core Internet proxy", "−161k", "B1 − A7"],
            ["CMCSA domestic resid. BB", "−65k", "RETRIEVED Ex99.1"],
            ["CHTR vs CMCSA print gap", "−55k (1.8×)", "Already includes rural"],
          ]}
          striped
        />
        <Callout tone="warning" title="Slope attribution (the Root B symptom)">
          Company Internet YoY: −120k − (−59k) = −61k. Rural add YoY: 41k −
          39k = +2k. Core Internet-proxy YoY: −161k − (−98k) = −63k. Rural
          improved the company slope by 2k; the entire −61k break vs last
          year is the core. CMCSA YoY +118k. Headline slope gap −179k; core
          proxy vs CMCSA −181k.
        </Callout>
      </Stack>

      <Stack gap={8}>
        <H2>4. Revenue conversion — real dollars, 1.6% of the firm</H2>
        <Text>
          Rural residential revenue is growing because the customer stock is
          growing. It is not large enough to offset company Internet dollar
          decline, and subsidy is a material slice of reported rural revenue.
        </Text>
        <Grid columns={4} gap={12}>
          <Stat value="$167M" label="Rural residential rev Q1’26" tone="info" />
          <Stat value="+$63M" label="YoY rural res (+61%)" tone="success" />
          <Stat value="−$78M" label="Company Internet rev YoY" tone="danger" />
          <Stat value="1.6%" label="Rural total / company total rev" />
        </Grid>
        <Table
          headers={["Line", "Q1’25", "Q1’26", "Read"]}
          columnAlign={["left", "right", "right", "left"]}
          rows={[
            ["Rural residential ($M)", "104", "167", "Stock growing; ARPU $113.71"],
            ["Rural subsidy ($M)", "28", "28", "RDOF-like run-rate, not product"],
            ["Rural other ($M)", "17", "26", "Includes SB / other"],
            ["Rural total ($M)", "149", "221", "1.6% of company $13,597M"],
            ["Company Internet ($M)", "5,930", "5,852", "−1.3% YoY"],
            ["Rural res ARPU vs company", "$113.29 vs $120.07", "$113.71 vs $118.44", "Similar, slightly lower"],
          ]}
          striped
        />
        <Text size="small" tone="tertiary">
          Rural revenue from Q1 2026 trending rural page. Company Internet
          Ex99.1. Rural residential is all products, not Internet-only — so
          $167M / $5,852M (2.9%) overstates Internet contribution.
        </Text>
      </Stack>

      <Divider />

      <Stack gap={8}>
        <H2>5. Remainder vs the gap the diagnosis cited</H2>
        <Text>
          Initiative target is &gt;1.7M passings (floor, not a cap). At Q1
          1.385M activated, 315k remain. Even lighting every leftover passing
          at company 54% take produces a one-time stock of ~170k customers —
          smaller than the 179k quarterly YoY slope gap vs Comcast, and not
          repeatable. Current 38% take on the remainder is ~120k. Rounded
          toward the expansion thesis (54% take): still not enough.
        </Text>
        <SignedBarChart
          categories={[
            "Q1 slope gap vs CMCSA",
            "Q1 rural CR adds",
            "Core CR hole Q1",
            "Remainder @38% take",
            "Remainder @54% take",
          ]}
          series={[
            {
              name: "Thousands (quarterly flow vs lifetime remaining stock)",
              data: [179, 41, 204, 120, 170],
              tone: "danger",
            },
          ]}
          height={240}
          valueSuffix="k"
          yMin={0}
          yMax={230}
          zeroLabel="0"
        />
        <Text size="small" tone="tertiary">
          First three bars are quarterly flows. Last two are lifetime customer
          stocks from leftover passings — different units, shown together to
          make the scale fail visible. 315k × 0.381 = 120k; 315k × 0.540 =
          170k.
        </Text>
        <Grid columns={2} gap={16}>
          <Card>
            <CardHeader>Unit cost already spent</CardHeader>
            <CardBody>
              <Stack gap={6}>
                <Text size="small">
                  YE2025: $7.7B / 1.3M ≈ $5,900 per passing. Q1’26 cumulative
                  ≈ $8.1B / 1.385M ≈ $5,870 per passing; ≈ $15,400 per rural
                  CR before grants, ≈ $11,600 after $2B awarded (not all cash
                  received).
                </Text>
                <Text size="small" tone="secondary">
                  “Over $8B” is a floor. At $5,900 × 315k leftover ≈ $1.9B
                  more; total near $10B. Infrastructure-style, not a 24-month
                  slope closer.
                </Text>
              </Stack>
            </CardBody>
          </Card>
          <Card>
            <CardHeader>Yield on capital (Q1 run-rate)</CardHeader>
            <CardBody>
              <Stack gap={6}>
                <Text size="small">
                  Annualized rural earned revenue ex-subsidy: ($167M + $26M)
                  × 4 = $772M on $8.1B in = 9.5% revenue / capital. Applying
                  company Adj. EBITDA margin 41.5% (ESTIMATED for rural) →
                  ~3.9% EBITDA yield.
                </Text>
                <Text size="small" tone="secondary">
                  Matches management’s “long-term infrastructure-style
                  returns.” Fails Root C’s clock: Internet run-rate inside
                  ~24 months.
                </Text>
              </Stack>
            </CardBody>
          </Card>
        </Grid>
      </Stack>

      <Divider />

      <Stack gap={8}>
        <H2>Two builds, then a cross-check that does not share the flow identity</H2>
        <Table
          headers={["Build", "Headline", "Shared?", "Tag"]}
          columnAlign={["left", "left", "left", "left"]}
          rowTone={["danger", "warning", "info"]}
          rows={[
            [
              "1. CR identity",
              "Q1 core CR −204k; rural cover 20%",
              "Uses rural CR stocks",
              "RETRIEVED − RETRIEVED",
            ],
            [
              "2. Internet proxy",
              "Q1 core Internet −161k; slope −63k vs CMCSA +118k",
              "Same rural CR series as build 1",
              "ESTIMATED identity rural CR ≈ Internet",
            ],
            [
              "3. Cross-check (stock, not flow)",
              "Rural take 38% vs company 54%; 221k missing on plant already lit; remainder 120–170k stock vs 179k quarterly gap",
              "No shared flow identity — ratios of stocks and leftover plant",
              "RETRIEVED pens; remaining = floor target − Q1 passings",
            ],
          ]}
          striped
        />
        <Text size="small">
          Builds 1 and 2 agreeing is correlation by construction: both
          subtract the same rural CR series. The penetration / remainder
          cross-check does not use net-add subtraction and still says rural
          is converting below company take and is the wrong scale for the
          CMCSA slope.
        </Text>
        <Callout tone="info" title="Q2 2026 (later public fact — not the assignment print)">
          Rural +47k CR; company CR −184k → core −231k. Company Internet
          −172k → core proxy −219k. H1 core CR −435k vs rural +88k. Same
          shape, slightly worse. Q2 rural ending stocks estimated as Q1
          trending + Ex99.1 adds (1,512k passings, 574k CR, 38.0% pen).
        </Callout>
      </Stack>

      <Stack gap={8}>
        <H2>Assumption register (one line, one ID)</H2>
        <Table
          headers={["ID", "Input / formula", "Value", "Tag"]}
          columnAlign={["left", "left", "right", "left"]}
          rows={[
            ["A1", "Rural passings Q1’26", "1,385k", "RETRIEVED trending"],
            ["A2", "Rural CR Q1’26", "527k", "RETRIEVED trending"],
            ["A3", "A2 / A1 rural penetration", "38.1%", "derived"],
            ["A4", "Company CR Q1’26", "31,683k", "RETRIEVED Ex99.1"],
            ["A6", "Company CR adds Q1’26", "−163k", "RETRIEVED Ex99.1"],
            ["A7", "Rural CR adds Q1’26", "+41k", "RETRIEVED Ex99.1 / 527−486"],
            ["A8", "A6 − A7 core CR adds", "−204k", "derived"],
            ["A9", "A7 / |A8| cover of core hole", "20%", "derived; rounded"],
            ["B1", "Company Internet adds Q1’26", "−120k", "RETRIEVED Ex99.1"],
            ["B2", "B1 − A7 core Internet proxy", "−161k", "ESTIMATED identity"],
            ["B4", "Rural add Q1’26 − Q1’25 (41−39)", "+2k", "derived"],
            ["B5", "CHTR Internet YoY (−120−(−59))", "−61k", "RETRIEVED"],
            ["B6", "CMCSA BB YoY (−65−(−183))", "+118k", "RETRIEVED"],
            ["B7", "B5 − B6 slope gap", "−179k", "derived"],
            ["C1", "Rural residential revenue Q1’26", "$167M", "RETRIEVED trending"],
            ["C5", "Rural total / company total rev", "1.6%", "221 / 13,597"],
            ["D1", "Remainder passings to 1.7M floor", "315k", "1,700 − A1"],
            ["D2", "D1 × A3 remainder @ current take", "120k CR", "derived; rounded down"],
            ["D3", "D1 × 54.0% remainder @ company take", "170k CR", "generous vs D2"],
            ["E1", "Cumulative rural spend Q1’26", "~$8.1B", "7.7 + 0.427"],
          ]}
          striped
        />
        <Text size="small" tone="tertiary">
          Dollar-weighted: the CR headline (A6/A7/A8) is 100% retrieved. B2
          is the only estimated identity in the operating split. EBITDA yield
          applies company 41.5% margin to rural (ESTIMATED). Trending rural
          page is unofficial IR extract; A7 cross-checks to Ex99.1 (+41k).
        </Text>
      </Stack>

      <Stack gap={8}>
        <H2>Sensitivity — where leverage actually is</H2>
        <Table
          headers={["Input", "Base", "Shock", "What moves"]}
          columnAlign={["left", "right", "right", "left"]}
          rows={[
            [
              "Rural CR = Internet (B2)",
              "100%",
              "80% / 50%",
              "Core Internet −153k / −141k — still worse than CMCSA −65k; A8 −204k unchanged",
            ],
            [
              "Remainder take rate",
              "38%",
              "54% company",
              "Leftover stock 120k → 170k — still < 179k quarterly slope gap",
            ],
            [
              "Target passings",
              "1.7M floor",
              "2.0M",
              "Remainder 615k × 38% = 234k stock — one-time, still not a quarterly closer",
            ],
            [
              "Rural add acceleration",
              "+2k",
              "Would need ~+179k",
              "To close B7 on rural alone; 4× current quarterly rural adds, every quarter",
            ],
          ]}
          striped
        />
        <Text size="small">
          Precision went to the retrieved CR split (highest leverage on the
          “is rural fixing Root B?” question). Mix-adjusted CHTR vs CMCSA
          loss rates are still unrun — they do not change this conversion
          math; they change whether the core hole is mix or offer.
        </Text>
      </Stack>

      <Divider />

      <Grid columns={2} gap={16}>
        <Stack gap={8}>
          <H2>Channel contribution (before any rec)</H2>
          <Text size="small">
            Rural: only positive CR channel in the print (~40–50k/qtr), 38%
            take, $167M/qtr residential, cannot close −179k YoY vs CMCSA.
            Core: −204k CR in Q1, 54% take and falling, is the slope. Working
            rural harder adds another ~40k to a 204k hole. Size of remaining
            rural is not the opportunity to fix Root B.
          </Text>
        </Stack>
        <Stack gap={8}>
          <H2>Kill rule</H2>
          <Text size="small">
            Kill “rural expansion closes the CMCSA Internet slope” if (i)
            remainder customers even at company take are a one-time stock
            below the quarterly slope gap, and (ii) rural quarterly adds are
            not accelerating. Both true at Q1 2026 (170k stock vs 179k gap;
            +2k acceleration). Kill “rural is not converting” if take were
            near zero or revenue were subsidy-only — falsified (38% take,
            $167M/qtr residential).
          </Text>
        </Stack>
      </Grid>

      <Stack gap={8}>
        <H2>Unwilling to claim</H2>
        <Stack gap={4}>
          <Text size="small">• Rural Internet customers as a disclosed line (CR is what is public)</Text>
          <Text size="small">• A rural ROI year or payback schedule</Text>
          <Text size="small">
            • That DMA-mix-adjusted core vs CMCSA is worse — mix control is
            still unrun
          </Text>
          <Text size="small">
            • That stopping rural would help the print (it is the only
            positive CR channel)
          </Text>
          <Text size="small">
            • That 1.7M passings is a cap (10-K says “over $8B” / “over 1.7M”)
          </Text>
          <Text size="small">• A recommendation — this page sizes the missing conversion</Text>
        </Stack>
      </Stack>

      <Callout tone="info" title="What this does to the diagnosis">
        The product-expansion thesis is not empty: rural converts at 38% and
        puts real residential revenue on the books. It is the wrong scale
        and the wrong layer for the Root B symptom the diagnosis cited. If
        rural converts and the YoY Internet gap vs CMCSA still widens on the
        non-rural base — which is what Q1 2026 shows — expansion is
        incomplete or aimed at the competitive layer that is not producing
        the slope. Next measurement that still matters: mix-adjusted core
        loss rates vs CMCSA, not more passings.
      </Callout>

      <Text size="small" tone="tertiary">
        Sources: CHTR Q1 2026 trending schedule (rural page; unofficial IR
        extract, CR adds cross-checked to Ex99.1) · Ex99.1 Q1 2026 · Ex99.1
        Q2 2026 (later) · FY2025 10-K (1.3M; $7.7B; &gt;1.7M / &gt;$8B) ·
        CMCSA Ex99.1 Q1 2026. Arithmetic recomputed in code before shipping.
        Assignment anchor: end Q1 2026. Not a recommendation.
      </Text>
    </Stack>
  );
}
