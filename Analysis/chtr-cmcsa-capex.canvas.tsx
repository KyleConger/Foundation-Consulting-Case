/**
 * Capex analysis: Charter vs Comcast (cable-like Connectivity & Platforms).
 * CHTR is almost all connectivity; CMCSA consolidated includes parks/media —
 * primary peer cut is C&P. Assignment anchor Q1 2026; Q2/H1 labeled later.
 */
import {
  Callout,
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
  useHostTheme,
} from "cursor/canvas";
import type { ChartTone } from "cursor/canvas";

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
  const pad = { top: 18, right: 12, bottom: 52, left: 52 };
  const width = Math.max(480, categories.length * (series.length > 1 ? 70 : 50));
  const innerW = width - pad.left - pad.right;
  const innerH = height - pad.top - pad.bottom;
  const all = series.flatMap((s) => s.data);
  const lo = yMin ?? Math.min(0, ...all) * 1.05;
  const hi = yMax ?? Math.max(0, ...all) * 1.08;
  const span = hi - lo || 1;
  const yScale = (v: number) => pad.top + ((hi - v) / span) * innerH;
  const zeroY = yScale(0);
  const groupW = innerW / categories.length;
  const barW = Math.min(20, (groupW * 0.72) / series.length);

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
          <g key={String(t)}>
            <line
              x1={pad.left}
              x2={width - pad.right}
              y1={yScale(t)}
              y2={yScale(t)}
              stroke={theme.stroke.tertiary}
              strokeWidth={t === 0 ? 1.25 : 1}
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
                  (series.length * barW + (series.length - 1) * 3) / 2 +
                  si * (barW + 3);
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

export default function ChtrCmscaCapex() {
  return (
    <Stack gap={28}>
      <Stack gap={8}>
        <Row gap={8} wrap>
          <Pill tone="info">Capex analysis</Pill>
          <Pill tone="warning">Peer cut = CMCSA Connectivity & Platforms</Pill>
          <Pill>FY2025 + H1 2026</Pill>
        </Row>
        <H1>Capex: Charter vs Comcast</H1>
        <Text tone="secondary">
          Absolute dollars look similar at the company level. Intensity does
          not. Charter is a connectivity pure-play spending ~21¢ of every
          revenue dollar on capex; Comcast’s cable-like Connectivity &
          Platforms segment spends ~11¢.
        </Text>
      </Stack>

      <Callout tone="warning" title="Apples-to-apples">
        Do not compare CHTR total capex to CMCSA consolidated without noting
        parks/media. Primary peer cut = CMCSA Connectivity & Platforms (C&P).
        CHTR has no equivalent non-connectivity bucket. CMCSA also reports
        cash paid for capitalized software/intangibles separately from PP&E
        capex; CHTR NCTA tables are PP&E-style capital expenditures.
      </Callout>

      <Grid columns={4} gap={12}>
        <Stat value="21.3%" label="CHTR FY25 capex / revenue" tone="danger" />
        <Stat value="10.8%" label="CMCSA C&P FY25 capex / C&P rev" tone="warning" />
        <Stat value="~2.0×" label="CHTR intensity vs CMCSA C&P" tone="danger" />
        <Stat value="$11.4B" label="CHTR FY26 guide (ex-Cox)" tone="info" />
      </Grid>

      <Divider />

      <Stack gap={8}>
        <H2>1. Annual totals — company vs cable-like</H2>
        <Text>
          Consolidated CMCSA capex ≈ CHTR in dollars ($11.8–12.2B vs
          $11.3–11.7B). Strip out Content & Experiences and the cable
          businesses diverge: C&P is ~$8.3–8.7B while Charter still spends
          ~$11.3–11.7B on a smaller revenue base.
        </Text>
        <SignedBarChart
          categories={["FY2024", "FY2025"]}
          series={[
            {
              name: "CHTR total ($B)",
              data: [11.27, 11.66],
              tone: "danger",
            },
            {
              name: "CMCSA C&P ($B)",
              data: [8.29, 8.72],
              tone: "info",
            },
            {
              name: "CMCSA consolidated ($B)",
              data: [12.18, 11.75],
              tone: "neutral",
            },
          ]}
          height={260}
          valuePrefix="$"
          valueSuffix="B"
          yMin={0}
          yMax={14}
          zeroLabel="$0"
        />
        <Text size="small" tone="tertiary">
          $B · CHTR 10-K FY2025 · CMCSA trending schedule (rev. Mar 16 2026)
        </Text>
      </Stack>

      <Stack gap={8}>
        <H2>2. Intensity — the relative read that matters</H2>
        <Text>
          Capex as % of revenue and of Adj. EBITDA. Charter’s network evolution
          + rural build keep intensity elevated into the 2027 completion target.
        </Text>
        <SignedBarChart
          categories={["Capex / revenue", "Capex / Adj. EBITDA"]}
          series={[
            {
              name: "CHTR FY2025",
              data: [21.3, 51.3],
              tone: "danger",
            },
            {
              name: "CMCSA C&P FY2025",
              data: [10.8, 27.2],
              tone: "info",
            },
          ]}
          height={240}
          valueSuffix="%"
          yMin={0}
          yMax={55}
          zeroLabel="0%"
        />
        <Table
          headers={["Metric (FY2025)", "CHTR", "CMCSA C&P", "Gap"]}
          columnAlign={["left", "right", "right", "right"]}
          rowTone={["danger", "danger", undefined]}
          rows={[
            ["Capex ($M)", "11,659", "8,723", "CHTR +2,936"],
            ["Revenue ($M)", "54,774", "81,069", "CMCSA C&P larger"],
            ["Adj. EBITDA ($M)", "22,708", "32,089", "—"],
            ["Capex / revenue", "21.3%", "10.8%", "+10.5ppt"],
            ["Capex / Adj. EBITDA", "51.3%", "27.2%", "+24.1ppt"],
            ["FCF ($M, company)", "5,004", "— (consol. different)", "CHTR FCF after heavy PP&E"],
          ]}
          striped
        />
        <Text size="small" tone="tertiary">
          CHTR: 11,659 / 54,774; 11,659 / 22,708. CMCSA C&P: 8,723 / 81,069;
          8,723 / 32,089 (trending FY2025).
        </Text>
      </Stack>

      <Stack gap={8}>
        <H2>3. Category mix (FY2025) — where the dollars go</H2>
        <Text>
          NCTA-style buckets. Charter’s line extensions (esp. subsidized rural
          ~$2.2B) and upgrade/rebuild (network evolution) are the structural
          extras vs Comcast C&P, which skews more to scalable infrastructure.
        </Text>
        <SignedBarChart
          categories={["CPE", "Scalable", "Upgrade / line*", "Support"]}
          series={[
            {
              name: "CHTR ($B)",
              data: [2.26, 1.54, 5.88, 1.99],
              tone: "danger",
            },
            {
              name: "CMCSA C&P ($B)",
              data: [2.19, 3.16, 2.69, 0.69],
              tone: "info",
            },
          ]}
          height={260}
          valuePrefix="$"
          valueSuffix="B"
          yMin={0}
          yMax={6.5}
          zeroLabel="$0"
        />
        <Text size="small" tone="tertiary">
          *CHTR bar = upgrade/rebuild ($1.94B) + total line extensions
          ($3.94B). CMCSA C&P reports line extensions as one line ($2.69B) and
          does not publish a separate “upgrade/rebuild” NCTA line in the
          trending schedule — scalable ($3.16B) is the closest network-capacity
          analog. Not identical taxonomies.
        </Text>
        <Table
          headers={["CHTR NCTA ($M)", "2025", "2024", "Δ"]}
          columnAlign={["left", "right", "right", "right"]}
          rows={[
            ["CPE", "2,260", "2,172", "+88"],
            ["Scalable infrastructure", "1,536", "1,422", "+114"],
            ["Upgrade / rebuild (network evolution)", "1,937", "1,771", "+166"],
            ["Support capital", "1,986", "1,688", "+298"],
            ["Subsidized rural line extensions", "2,202", "2,144", "+58"],
            ["Other line extensions", "1,738", "2,072", "−334"],
            ["Total", "11,659", "11,269", "+390"],
            ["Of which: rural initiative", "2,208", "2,152", "+56"],
            ["Of which: mobile", "267", "245", "+22"],
          ]}
          striped
        />
      </Stack>

      <Divider />

      <Stack gap={8}>
        <H2>4. Recent quarters — still elevated into 2026</H2>
        <Text>
          Q1 2026: Charter +19% YoY ($2.86B vs $2.40B) on CPE and
          upgrade/rebuild. Comcast C&P +13% YoY to ~$1.8B. H1 2026 Charter
          $5.73B vs $5.27B prior year; guide still ~$11.4B ex-Cox for FY2026.
        </Text>
        <SignedBarChart
          categories={["Q1’25", "Q1’26", "Q2’25", "Q2’26", "H1’25", "H1’26"]}
          series={[
            {
              name: "CHTR total ($B)",
              data: [2.4, 2.86, 2.87, 2.87, 5.27, 5.73],
              tone: "danger",
            },
            {
              name: "CMCSA C&P ($B)",
              data: [1.63, 1.85, 1.91, 2.3, 3.54, 4.15],
              tone: "info",
            },
          ]}
          height={260}
          valuePrefix="$"
          valueSuffix="B"
          yMin={0}
          yMax={6.2}
          zeroLabel="$0"
        />
        <Text size="small" tone="tertiary">
          CHTR Ex99.1 / 10-Q. CMCSA C&P: FY2025 trending Q1–Q2’25; Q1’26 ≈
          $1.85B (+13.4% on $1.629B); Q2’26 ≈ $2.3B (+19.9% on $1.914B). H1
          C&P ≈ sum of quarters.
        </Text>
        <Table
          headers={["Period", "CHTR", "YoY", "CMCSA C&P", "YoY"]}
          columnAlign={["left", "right", "right", "right", "right"]}
          rowTone={[undefined, "warning", undefined, undefined, "warning"]}
          rows={[
            ["Q1 2025", "$2.40B", "—", "$1.63B", "—"],
            ["Q1 2026", "$2.86B", "+19%", "~$1.85B", "+13%"],
            ["Q2 2025", "$2.87B", "—", "$1.91B", "—"],
            ["Q2 2026 (later)", "$2.87B", "≈ flat", "~$2.3B", "+20%"],
            ["H1 2026 (later)", "$5.73B", "+9% vs H1’25", "~$4.15B", "+17%"],
            ["FY2026 guide", "~$11.4B ex-Cox", "slightly below FY25", "not used here", "—"],
          ]}
          striped
        />
      </Stack>

      <Stack gap={8}>
        <H2>5. What Charter’s extra intensity is buying</H2>
        <Table
          headers={["Bucket", "Scale", "Strategic intent", "Investor read"]}
          columnAlign={["left", "left", "left", "left"]}
          rows={[
            [
              "Network evolution (in upgrade/rebuild)",
              "On track; largely complete end-2027",
              "Symmetrical multi-gig on HFC vs full FTTH overbuild",
              "Capex step-down thesis after 2027 — only if Internet print stabilizes",
            ],
            [
              "Subsidized rural",
              "~$2.2B in 2025; $7.7B since 2022; ~1.3M passings activated",
              "Infrastructure-style returns + subsidy milestones",
              "Real cash out; timing/penalty risk; not short-cycle FCF",
            ],
            [
              "CPE / mobile",
              "CPE up sharply Q1’26 (+41% class note); mobile capex still small ($267M FY25)",
              "WiFi / Invincible WiFi / MVNO experience",
              "Supports product story; does not replace last-mile spend",
            ],
            [
              "Cox transition",
              "$34M Q2’26 transition in capex footnote",
              "Integration prep pre-close",
              "Guide excludes Cox impacts — post-close intensity may rise",
            ],
          ]}
          striped
        />
      </Stack>

      <Callout tone="info" title="Implication for the engagement">
        Capex is an industry feature (both C&P and CHTR are still investing) and
        a Charter-specific intensity problem (~2× C&P capex/revenue). Waiting
        for 2027 roll-off is the base-case capital story — the issue-tree already
        flags that as unlikely to satisfy the CEO charge by itself. Any
        recommendation that adds capex must clear a higher bar than Comcast’s
        cable segment would face; any that funds growth from capex deferral must
        name what gets cut (rural pace, evolution timing, CPE).
      </Callout>

      <Text size="small" tone="tertiary">
        Sources: CHTR 10-K FY2025 / Ex99.1 Q1–Q2 2026 / 10-Q · CMCSA trending
        schedule (Mar 16 2026) · CMCSA Ex99.1 Q1–Q2 2026. Analysis, not a
        filing.
      </Text>
    </Stack>
  );
}
