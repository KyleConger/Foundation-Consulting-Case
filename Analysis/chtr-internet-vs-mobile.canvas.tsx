/**
 * Live Cursor canvas. Project copy:
 *   Analysis/chtr-internet-vs-mobile.canvas.tsx
 * Internet vs mobile volumes, and implied Internet ARPU.
 * Arithmetic: Analysis/internet_vs_mobile_model.py
 * Does not supersede Root C, diagnostic Graph 1, or product-mix.
 */
import {
  Callout,
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
  useHostTheme,
} from "cursor/canvas";
import type { ChartTone } from "cursor/canvas";

const QTRS = [
  "23Q1",
  "23Q2",
  "23Q3",
  "23Q4",
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

const INET_ADD = [76, 77, 64, -61, -72, -148, -110, -177, -59, -116, -109, -119, -120, -172];
const MOB_ADD = [685, 647, 593, 544, 483, 552, 540, 522, 507, 491, 482, 428, 368, 406];

const INET_ARPU = [
  67.01, 67.02, 67.37, 67.72, 68.12, 68.16, 69.26, 69.42, 70.58, 71.25, 71.56,
  70.94, 70.72, 70.16,
];
const YOY_QTRS = QTRS.slice(4);
const YOY_ARPU = [1.11, 1.14, 1.89, 1.7, 2.46, 3.09, 2.3, 1.52, 0.14, -1.09];

const REV_INET = [5718, 5733, 5776, 5805, 5826, 5806, 5872, 5856, 5930, 5969, 5971, 5895, 5852, 5776];

function signedK(n: number): string {
  if (n > 0) return `+${n}k`;
  if (n < 0) return `−${Math.abs(n)}k`;
  return "0";
}

function signedM(n: number): string {
  if (n > 0) return `+$${n}M`;
  if (n < 0) return `−$${Math.abs(n)}M`;
  return "$0";
}

const ARPU_RES = [
  119.39, 118.91, 117.71, 117.64, 118.53, 118.6, 119.02, 118.65, 120.07, 119.7,
  119.16, 117.19, 118.44, 117.52,
];

function SignedBarChart({
  categories,
  series,
  height = 220,
  valueSuffix = "",
  yMin,
  yMax,
}: {
  categories: string[];
  series: Array<{ name: string; data: number[]; tone?: ChartTone }>;
  height?: number;
  valueSuffix?: string;
  yMin?: number;
  yMax?: number;
}) {
  const theme = useHostTheme();
  const pad = { top: 16, right: 8, bottom: 44, left: 48 };
  const width = Math.max(480, categories.length * (series.length > 1 ? 52 : 40));
  const innerW = width - pad.left - pad.right;
  const innerH = height - pad.top - pad.bottom;
  const all = series.flatMap((s) => s.data);
  const lo = yMin ?? Math.min(0, ...all) * 1.1;
  const hi = yMax ?? Math.max(0, ...all) * 1.1;
  const span = hi - lo || 1;
  const yScale = (v: number) => pad.top + ((hi - v) / span) * innerH;
  const zeroY = yScale(0);
  const groupW = innerW / categories.length;
  const barW = Math.min(16, (groupW * 0.7) / series.length);

  const fill = (tone: ChartTone | undefined) => {
    if (tone === "danger") return theme.category.red;
    if (tone === "info") return theme.category.blue;
    if (tone === "success") return theme.category.green;
    return theme.category.gray;
  };

  const fmt = (v: number) => {
    const sign = v < 0 ? "−" : v > 0 ? "+" : "";
    return `${sign}${Math.abs(v)}${valueSuffix}`;
  };

  const ticks = [lo, 0, hi].filter((v, i, a) => a.indexOf(v) === i);

  return (
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
            {t === 0 ? "0" : fmt(Math.round(t))}
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
              const h = Math.max(v === 0 ? 0 : 2, Math.abs(y1 - zeroY));
              const x =
                gx -
                (series.length * barW + (series.length - 1) * 3) / 2 +
                si * (barW + 3);
              return (
                <rect
                  key={s.name}
                  x={x}
                  y={v === 0 ? zeroY : top}
                  width={barW}
                  height={h}
                  fill={fill(s.tone)}
                >
                  <title>{`${s.name}: ${fmt(v)}`}</title>
                </rect>
              );
            })}
            <text
              x={gx}
              y={height - 14}
              textAnchor="middle"
              fill={theme.text.tertiary}
              fontSize={9}
            >
              {cat}
            </text>
          </g>
        );
      })}
    </svg>
  );
}

export default function ChtrInternetVsMobile() {
  return (
    <Stack gap={28}>
      <Stack gap={8}>
        <Row gap={8} align="center" wrap>
          <Pill tone="warning">DRAFT — analysis, not a recommendation</Pill>
          <Pill tone="success">Verified vs PrimarySources</Pill>
          <Pill tone="info">Q1 2026 assignment anchor</Pill>
          <Pill tone="neutral">Q2 2026 later public fact</Pill>
        </Row>
        <H1>
          Internet has not printed a positive quarter since 23Q3; mobile added
          lines every quarter — and by Q2 even Internet’s rate offset flipped
        </H1>
        <Text tone="secondary">
          Two separate claims, two charts. Volumes: total Internet customers
          −1.12 million from 23Q1 to 26Q2 while mobile lines +6.56 million.
          Pricing: implied residential Internet ARPU is not a list price. It
          rose $67.01 → $71.56 (25Q3 peak), then gave back $1.40 to $70.16.
          The Q2 2026 10-Q is the retrieved print: Internet{" "}
          <Text as="span" weight="semibold">rate −$89M</Text> on top of
          volume −$104M. Does not re-rate Internet as the tape (Root C).
        </Text>
      </Stack>

      <Grid columns={4} gap={12}>
        <Stat value="−1.12M" label="Internet customers, 23Q1–26Q2" tone="danger" />
        <Stat value="+6.56M" label="Mobile lines, 23Q1–26Q2" tone="info" />
        <Stat value="$71.56" label="Implied Internet ARPU peak (25Q3)" tone="warning" />
        <Stat value="−$89M" label="Q2 2026 Internet rate bridge" tone="danger" />
      </Grid>
      <Text size="small" tone="tertiary">
        Checked against PrimarySources originals (CORE hierarchy: Ex99.1 /
        10-K / 10-Q beat unofficial trending). Identities and source map
        below. Implied ARPU is DERIVED. Rate −$89M is RETRIEVED (10-Q Q2 2026).
      </Text>

      <Table
        headers={["Series", "Periods on this canvas", "Primary source", "Status"]}
        rows={[
          [
            "Internet / mobile EOP and net adds",
            "24Q4–26Q2",
            "Ex99.1 FY2025, Q1 2026, Q2 2026 addenda (restated)",
            "Matches",
          ],
          [
            "Internet / mobile EOP and net adds",
            "23Q1–24Q3",
            "FY2025 trending, current methodology (unofficial extract; no Ex99.1 in this pack)",
            "Matches trending; EOP identity holds",
          ],
          [
            "Internet / mobile service revenue",
            "25Q1–26Q2",
            "Ex99.1 Q1/Q2 2026 and FY2025 (Q4). Q3’25 from trending; four quarters sum to 10-K $23,765 / $3,762",
            "Matches",
          ],
          [
            "Internet / mobile service revenue",
            "23Q1–24Q4",
            "FY2025 trending. Annual sums match 10-K $23,032 / $2,243 (2023) and $23,360 / $3,083 (2024)",
            "Matches 10-K totals",
          ],
          [
            "Disclosed residential ARPU",
            "24Q4–26Q2",
            "Same Ex99.1 addenda",
            "Matches",
          ],
          [
            "Internet rate/volume $",
            "FY2025, Q1’26, Q2’26",
            "10-K FY2025 (+$785 / −$380 / +$405); 10-Q Q1 (−$87 / +$9 / −$78); 10-Q Q2 (−$104 / −$89 / −$193)",
            "Matches",
          ],
          [
            "Implied Internet ARPU",
            "23Q1–26Q2",
            "DERIVED: Internet $ ÷ 3 ÷ avg residential Internet customers. Not a list price. Q2 YoY ≈ −$90M vs 10-Q rate −$89M",
            "Formula only",
          ],
        ]}
        rowTone={["success", "warning", "success", "info", "success", "success", "neutral"]}
      />

      <Divider />

      <Stack gap={10}>
        <H2>
          Mobile line adds do not make up Internet losses — +368k lines vs
          −120k broadband customers is the wrong net
        </H2>
        <Table
          headers={[
            "Test",
            "Internet (broadband)",
            "Mobile",
            "Does mobile close it?",
          ]}
          rows={[
            [
              "Unit",
              "Customers",
              "Lines (phones / tablets)",
              "No — not the same object",
            ],
            [
              "Q1 2026 net adds (the tape)",
              "−120k",
              "+368k",
              "No — multiple prices the left column",
            ],
            [
              "Q1 2026 revenue YoY",
              "−$78M",
              "+$138M",
              "No — connectivity +$60M is not the Internet print",
            ],
            [
              "Implied ARPU / month (DERIVED)",
              "$70.72",
              "$30.38",
              "No — mobile is ~43% of Internet rate",
            ],
            [
              "FY2025 10-K",
              "−403k customers; $ still +$405M on rate/mix",
              "+1.9M lines; +$679M ($714M volume, −$35M rate)",
              "No — volume engine at a declining rate",
            ],
            [
              "Q2 2026 (later public fact)",
              "−172k customers; $ −$193M",
              "+406k lines; $ +$174M",
              "No — connectivity went −$19M; Internet still the print",
            ],
          ]}
          rowTone={["warning", "danger", "danger", "neutral", "neutral", "danger"]}
        />
        <Text size="small" tone="tertiary">
          Q1 2026 is the assignment anchor (Ex99.1 / 10-Q). Mobile implied ARPU
          = mobile service revenue ÷ 3 ÷ average residential mobile lines.
          FY2025 bridges: 10-K Item 7. Q2 connectivity $6,871 vs $6,890. Root C:
          do not net lines against Internet customers.
        </Text>
      </Stack>

      <Stack gap={8}>
        <H2>
          Every quarter since 23Q4, naive netting of mobile adds against
          Internet losses is positive — and Internet still printed negative
        </H2>
        <Table
          headers={[
            "Quarter",
            "Internet net adds",
            "Mobile line adds",
            "Naive net (wrong unit)",
            "Internet $ YoY",
            "Broadband made whole?",
          ]}
          columnAlign={["left", "right", "right", "right", "right", "left"]}
          striped
          stickyHeader
          rows={QTRS.map((q, i) => {
            const naive = INET_ADD[i] + MOB_ADD[i];
            const inetDown = INET_ADD[i] < 0;
            const dol =
              i < 4 ? "—" : signedM(REV_INET[i] - REV_INET[i - 4]);
            return [
              q,
              signedK(INET_ADD[i]),
              signedK(MOB_ADD[i]),
              signedK(naive),
              dol,
              inetDown ? "No" : "Internet was still adding",
            ];
          })}
          rowTone={QTRS.map((q, i) =>
            q === "26Q1" || q === "26Q2"
              ? "danger"
              : INET_ADD[i] < 0
                ? "warning"
                : "success",
          )}
        />
        <Text size="small" tone="tertiary">
          Naive net = Internet customer adds + mobile line adds. That sum is
          the trap: it is positive in all 14 quarters while Internet has been
          negative for 11. Dollars YoY from 24Q1 (Ex99.1 where filed; earlier
          quarters foot to 10-K). 23Q1–24Q3 customer counts: restated trending.
          24Q4–26Q2: Ex99.1.
        </Text>
      </Stack>

      <Divider />

      <Grid columns={2} gap={24}>
        <Stack gap={8}>
          <H2>Internet net adds have been negative for 11 straight quarters</H2>
          <SignedBarChart
            categories={QTRS}
            series={[
              {
                name: "Total Internet net adds (000s)",
                data: INET_ADD,
                tone: "danger",
              },
            ]}
            valueSuffix="k"
            yMin={-200}
            yMax={100}
          />
          <Text size="small" tone="tertiary">
            Thousands of total Internet customers. Last positive print: 23Q3
            (+64k) — FY2025 restated trending. From 24Q4 the series is Ex99.1.
            Q1 2026 −120k is the assignment trigger (Ex99.1 Q1); Q2 −172k is
            a later public fact (Ex99.1 Q2). Bars from zero. Restated basis ·
            23Q1–26Q2
          </Text>
        </Stack>
        <Stack gap={8}>
          <H2>Mobile still added 368–685k lines every quarter in this window</H2>
          <SignedBarChart
            categories={QTRS}
            series={[
              {
                name: "Total mobile line net adds (000s)",
                data: MOB_ADD,
                tone: "info",
              },
            ]}
            valueSuffix="k"
            yMin={0}
            yMax={750}
          />
          <Text size="small" tone="tertiary">
            Thousands of mobile lines — not customers. Slowing (685k → 368k)
            but never negative. Own scale so the Internet slope on the left
            stays readable. 24Q4–26Q2 from Ex99.1; 23Q1–24Q3 from restated
            trending. 23Q1–26Q2
          </Text>
        </Stack>
      </Grid>

      <Callout tone="warning" title="Root C — do not net the two panels">
        Lines are not Internet customers, and the multiple still prices the
        left chart. Mobile +6.56 million lines does not offset Internet
        −1.12 million customers for the tape. Same refusal as the diagnostic
        canvas; this file just extends it through 23Q1 and puts price next to
        it.
      </Callout>

      <Divider />

      <Stack gap={8}>
        <H2>
          Implied Internet ARPU rose through 25Q3, then gave back $1.40 — not
          a list price
        </H2>
        <LineChart
          categories={QTRS}
          series={[
            {
              name: "Implied residential Internet ARPU ($/mo)",
              data: INET_ARPU,
              tone: "danger",
            },
          ]}
          beginAtZero={false}
          yMin={66}
          yMax={73}
          valuePrefix="$"
          height={240}
          referenceLines={[
            { value: 71.56, label: "25Q3 peak $71.56", tone: "neutral" },
          ]}
        />
        <Text size="small" tone="tertiary">
          Axis zoomed $66–$73 so the $4.55 climb and $1.40 giveback are
          readable — not a zero baseline. Formula: quarterly Internet revenue
          × 1,000 ÷ 3 ÷ average residential Internet customers (begin/end
          average). Includes promotional step-ups, rate adjustments, bundled
          revenue allocation, and the Q4 2025 free-months promo. Filings do
          not disclose a gig-tier list-price series. Internet $ from Ex99.1
          where filed (25Q1–26Q2 and FY totals); earlier quarters from
          trending that foot to the 10-K. DERIVED · 23Q1–26Q2
        </Text>
      </Stack>

      <Stack gap={8}>
        <H2>
          Q2 2026 is the first year-over-year implied-ARPU decline in the
          comparable window
        </H2>
        <SignedBarChart
          categories={YOY_QTRS}
          series={[
            {
              name: "YoY implied Internet ARPU still up ($)",
              data: YOY_ARPU.map((v, i) => (i === YOY_ARPU.length - 1 ? 0 : v)),
              tone: "neutral",
            },
            {
              name: "Q2 2026 YoY implied Internet ARPU ($)",
              data: YOY_ARPU.map((v, i) => (i === YOY_ARPU.length - 1 ? v : 0)),
              tone: "danger",
            },
          ]}
          valueSuffix=""
          yMin={-1.5}
          yMax={3.5}
        />
        <Text size="small" tone="tertiary">
          Dollars per month, year-over-year change in implied ARPU. 24Q1–26Q1
          all positive; 26Q2 −$1.09. Cross-check: −$1.09 × 3 × 27,441k average
          residential Internet customers ≈ −$90M, vs the 10-Q Q2 retrieved
          rate line of −$89M. Bars from zero. Help collapsed before it flipped:
          26Q1 was only +$0.14 YoY.
        </Text>
      </Stack>

      <Stack gap={8}>
        <H2>Retrieved rate/volume bridges — the pricing print the 10-Q actually filed</H2>
        <Table
          headers={["Period", "Internet volume", "Internet rate / mix", "Net Internet $", "Tag"]}
          columnAlign={["left", "right", "right", "right", "left"]}
          rows={[
            ["FY2025 vs FY2024 (10-K)", "−$380M", "+$785M", "+$405M", "RETRIEVED"],
            ["Q1 2026 vs Q1 2025 (10-Q)", "−$87M", "+$9M", "−$78M", "RETRIEVED"],
            ["Q2 2026 vs Q2 2025 (10-Q)", "−$104M", "−$89M", "−$193M", "RETRIEVED"],
          ]}
          rowTone={["neutral", "warning", "danger"]}
        />
        <Text size="small" tone="tertiary">
          Q1 still had a small rate/mix help. Q2 is the first period in this
          set where the company labeled an Internet{" "}
          <Text as="span" weight="semibold">decrease related to rate</Text>
          {" "}(Ex99.1: “pricing and packaging mix,” partly offset by more
          favorable bundled allocation). FY2025 rate/mix still more than
          covered volume — that is the regime Q1–Q2 broke.
        </Text>
      </Stack>

      <Callout tone="info" title="Do not use blended residential ARPU as Internet pricing">
        Disclosed residential ARPU ($119.39 → $117.52) mixes Internet, mobile,
        video, and voice, and is pulled down by seamless-entertainment
        allocation netted in video. 25Q4 blended ARPU $117.19 is a video-
        accounting print, not an Internet price cut. Implied Internet ARPU
        that quarter was $70.94.
      </Callout>

      <Table
        headers={["Qtr", "Inet adds (k)", "Mobile adds (k)", "Implied Inet ARPU", "YoY ARPU", "Disclosed res. ARPU"]}
        columnAlign={["left", "right", "right", "right", "right", "right"]}
        striped
        stickyHeader
        rows={QTRS.map((q, i) => [
          q,
          (INET_ADD[i] > 0 ? "+" : "") + String(INET_ADD[i]),
          "+" + String(MOB_ADD[i]),
          "$" + INET_ARPU[i].toFixed(2),
          i < 4 ? "—" : (YOY_ARPU[i - 4] > 0 ? "+" : "") + YOY_ARPU[i - 4].toFixed(2),
          "$" + ARPU_RES[i].toFixed(2),
        ])}
        rowTone={QTRS.map((q) =>
          q === "25Q3" ? "warning" : q === "26Q1" ? "info" : q === "26Q2" ? "danger" : undefined,
        )}
      />
      <Text size="small" tone="tertiary">
        25Q3 = implied ARPU peak. 26Q1 = assignment anchor. 26Q2 = later
        public fact and the rate flip. Arithmetic and PrimarySources asserts
        in Analysis/internet_vs_mobile_model.py. Does not clobber diagnostic
        Graph 1, product-mix, or GAP.
      </Text>
    </Stack>
  );
}
