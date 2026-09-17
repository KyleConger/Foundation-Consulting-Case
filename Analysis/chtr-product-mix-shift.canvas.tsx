/**
 * Live Cursor canvas. Project copy to pull from later:
 *   Analysis/chtr-product-mix-shift.canvas.tsx
 * Assignment anchor Q1 2026; Q2 labeled later public fact.
 * Arithmetic: Analysis/product_mix_model.py
 * Does not supersede GAP, Root C, or customer-performance.md.
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

const P1 = [46.6, 46.7, 47.2, 47.5, 48.2, 48.7, 49.0, 48.8, 48.9, 48.7, 48.5, 48.0, 47.7, 47.4];
const P2 = [32.5, 32.6, 32.6, 32.6, 32.5, 32.6, 32.7, 33.1, 33.4, 33.8, 34.1, 34.5, 34.8, 35.1];
const P3 = [20.9, 20.7, 20.2, 19.9, 19.3, 18.8, 18.3, 18.0, 17.7, 17.5, 17.4, 17.5, 17.5, 17.6];

const H2_HH = [9851, 9905, 9923, 9904, 9851, 9843, 9847, 9918, 9991, 10079, 10139, 10215, 10249, 10276];
const H3_HH = [6335, 6289, 6149, 6045, 5850, 5676, 5511, 5394, 5295, 5218, 5174, 5182, 5154, 5153];

const VID_SHARE = [39.24, 38.69, 37.29, 36.4, 36.21, 35.94, 34.69, 33.84, 33.21, 32.53, 31.83, 31.12, 30.99, 30.42];
const MOB_SHARE = [4.58, 4.98, 5.41, 5.83, 6.35, 6.85, 7.44, 8.05, 8.48, 8.59, 8.96, 9.33, 10.02, 10.58];
const INET_SHARE = [52.74, 52.96, 53.78, 54.11, 53.97, 53.95, 54.53, 54.81, 55.01, 55.66, 56.09, 56.52, 55.77, 55.8];

const VID_ATTACH = [50.1, 49.3, 48.1, 47.3, 46.0, 44.9, 44.1, 44.0, 43.5, 43.4, 43.3, 43.7, 43.7, 43.9];
const MOB_PER_INET = [0.203, 0.224, 0.244, 0.263, 0.28, 0.301, 0.32, 0.34, 0.359, 0.377, 0.395, 0.411, 0.426, 0.442];

function SignedBarChart({
  categories,
  series,
  height = 220,
  valueSuffix = "",
}: {
  categories: string[];
  series: Array<{ name: string; data: number[]; tone?: ChartTone }>;
  height?: number;
  valueSuffix?: string;
}) {
  const theme = useHostTheme();
  const pad = { top: 20, right: 12, bottom: 48, left: 56 };
  const width = Math.max(420, categories.length * 88);
  const innerW = width - pad.left - pad.right;
  const innerH = height - pad.top - pad.bottom;
  const all = series.flatMap((s) => s.data);
  const lo = Math.min(0, ...all) * 1.12;
  const hi = Math.max(0, ...all) * 1.12;
  const span = hi - lo || 1;
  const yScale = (v: number) => pad.top + ((hi - v) / span) * innerH;
  const zeroY = yScale(0);
  const groupW = innerW / categories.length;
  const barW = Math.min(28, groupW * 0.45);

  const fill = (tone: ChartTone | undefined) => {
    if (tone === "danger") return theme.category.red;
    if (tone === "success") return theme.category.green;
    if (tone === "info") return theme.category.blue;
    return theme.category.gray;
  };

  const fmt = (v: number) => {
    const sign = v < 0 ? "−" : v > 0 ? "+" : "";
    return `${sign}${Math.abs(v)}${valueSuffix}`;
  };

  return (
    <svg width="100%" viewBox={`0 0 ${width} ${height}`} style={{ display: "block" }}>
      {[lo, 0, hi].map((t) => (
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
        const v = series.reduce((s, ser) => s + (ser.data[ci] ?? 0), 0);
        const tone = series.find((ser) => (ser.data[ci] ?? 0) !== 0)?.tone;
        const y1 = yScale(v);
        const top = Math.min(zeroY, y1);
        const h = Math.max(v === 0 ? 0 : 2, Math.abs(y1 - zeroY));
        return (
          <g key={cat}>
            <rect
              x={gx - barW / 2}
              y={v === 0 ? zeroY : top}
              width={barW}
              height={h}
              fill={fill(tone)}
            >
              <title>{`${cat}: ${fmt(v)}`}</title>
            </rect>
            <text
              x={gx}
              y={v < 0 ? y1 + 14 : y1 - 6}
              textAnchor="middle"
              fill={theme.text.secondary}
              fontSize={11}
              fontWeight={600}
            >
              {fmt(v)}
            </text>
            <text
              x={gx}
              y={height - 16}
              textAnchor="middle"
              fill={theme.text.tertiary}
              fontSize={11}
            >
              {cat}
            </text>
          </g>
        );
      })}
    </svg>
  );
}

export default function ChtrProductMixShift() {
  return (
    <Stack gap={28}>
      <Stack gap={8}>
        <Row gap={8} align="center" wrap>
          <Pill tone="warning">DRAFT — analysis, not a recommendation</Pill>
          <Pill tone="info">Q1 2026 assignment anchor</Pill>
          <Pill tone="neutral">Q2 2026 later public fact</Pill>
        </Row>
        <H1>
          Charter lost 1.18 million three-or-more-product households and added
          0.42 million two-product ones — the mix flipped after 24Q3
        </H1>
        <Text tone="secondary">
          Commit: <Text as="span" weight="semibold">−1.18 million</Text> 3+
          residential households from 23Q1 to 26Q2 (range about −1.15 to −1.21
          million at 0.1 ppt disclosure rounding). Two-product{" "}
          <Text as="span" weight="semibold">+0.42 million</Text> on a base that
          shrank 1.03 million. Mix points: 3+{" "}
          <Text as="span" weight="semibold">−3.3 ppt</Text> (20.9% → 17.6%),
          2-product <Text as="span" weight="semibold">+2.6 ppt</Text> (32.5% →
          35.1%). Dollar twin: video’s share of residential revenue{" "}
          <Text as="span" weight="semibold">−8.8 ppt</Text>; mobile{" "}
          <Text as="span" weight="semibold">+6.0 ppt</Text>. Q1 2026 is already
          −1.18 million / +0.40 million; Q2 continues the 2-product climb with
          3+ floored. Does not re-rate the Internet print (Root C).
        </Text>
      </Stack>

      <Grid columns={4} gap={12}>
        <Stat value="−1.18M" label="3+ households, 23Q1–26Q2" tone="danger" />
        <Stat value="+0.42M" label="2-product households" tone="info" />
        <Stat value="+2.6 ppt" label="2-product mix (32.5% → 35.1%)" tone="info" />
        <Stat value="−8.8 ppt" label="Video share of residential $" tone="danger" />
      </Grid>
      <Text size="small" tone="tertiary">
        Households = disclosed penetration × disclosed residential customer
        relationships (DERIVED). Mix % and revenue $ are RETRIEVED. Source:
        FY2025 trending (restated, incl. mobile-only) · Ex99.1 Q1 2026 · Ex99.1
        Q2 2026 · 23Q1–26Q2
      </Text>

      <Callout tone="info" title="The mix is not a snapshot — it changed character">
        Phase 1 (23Q1–24Q3): Charter unbundled. One-product rose 46.6% → 49.0%;
        two-product was flat at 32.5–32.7%; three-or-more fell 20.9% → 18.3%.
        Phase 2 (24Q3–26Q2): it reconverged on a different pair. Two-product
        rose every quarter to 35.1%; one-product reversed 1.6 ppt from the
        peak; three-or-more floored near 17.5%. Life Unlimited is visible in
        the mix table. Internet net adds are not.
      </Callout>

      <Divider />

      <Stack gap={8}>
        <H2>
          Two-product mix has risen every quarter since 24Q3; three-or-more
          floored near 17.5%
        </H2>
        <LineChart
          categories={QTRS}
          series={[
            { name: "One-product %", data: P1, tone: "neutral" },
            { name: "Two-product % (story)", data: P2, tone: "info" },
            { name: "Three-or-more %", data: P3, tone: "danger" },
          ]}
          beginAtZero={false}
          yMin={15}
          yMax={52}
          valueSuffix="%"
          height={260}
        />
        <Text size="small" tone="tertiary">
          Axis zoomed 15–52% so the 2.6 / 3.3 ppt moves are readable — not a
          zero baseline. 24Q3 is the 1-product peak (49.0%) and the first of
          seven consecutive 2-product gains. 26Q2 1+2+3 = 100.1% on disclosed
          rounding. Source: Ex99.1 operating statistics, note (j)/(f) · restated
          residential penetration · 23Q1–26Q2
        </Text>
      </Stack>

      <Stack gap={8}>
        <H2>
          Three-or-more households fell 1.18 million — more than the entire
          residential-base loss
        </H2>
        <SignedBarChart
          categories={["1-product", "2-product", "3-or-more"]}
          series={[
            { name: "Other mix buckets (000s)", data: [-248, 425, 0], tone: "neutral" },
            { name: "3-or-more (000s)", data: [0, 0, -1182], tone: "danger" },
          ]}
          valueSuffix="k"
        />
        <Text size="small" tone="tertiary">
          Change in derived household counts, 23Q1 → 26Q2. Residential CR
          −1,034k. 3+ −1,182k more than explains the lost relationships;
          2-product added +425k while the base shrank. 1-product −248k after
          peaking in 24Q3. Bars from zero. Source: same penetration × CR
          identity · thousands of residential households
        </Text>
      </Stack>

      <Grid columns={2} gap={24}>
        <Stack gap={8}>
          <H2>Video’s share of residential revenue fell 8.8 points</H2>
          <LineChart
            categories={QTRS}
            series={[{ name: "Video % of residential revenue", data: VID_SHARE, tone: "danger" }]}
            beginAtZero={false}
            yMin={28}
            yMax={41}
            valueSuffix="%"
            height={220}
          />
          <Text size="small" tone="tertiary">
            Axis zoomed 28–41% (movement inside a band). 39.24% → 30.42%.
            Q2 2026 video $ includes $251M seamless-entertainment allocation
            netted in the line ($67M year-ago) — part of the drop is accounting.
            Source: trending / Ex99.1 residential video ÷ residential revenue
          </Text>
        </Stack>
        <Stack gap={8}>
          <H2>Mobile’s share of residential revenue rose 6.0 points</H2>
          <LineChart
            categories={QTRS}
            series={[{ name: "Mobile % of residential revenue", data: MOB_SHARE, tone: "info" }]}
            beginAtZero
            valueSuffix="%"
            height={220}
          />
          <Text size="small" tone="tertiary">
            4.58% → 10.58%. Zero baseline (series starts near 5%). Internet’s
            residential share only +3.1 ppt (52.7% → 55.8%) while Internet
            customers fell — rate/mix, not volume. Source: trending / Ex99.1
            mobile service ÷ residential revenue · 23Q1–26Q2
          </Text>
        </Stack>
      </Grid>

      <Divider />

      <Stack gap={10}>
        <H2>Each frame’s own number</H2>
        <Table
          headers={["Frame", "Its number", "What it decides"]}
          columnAlign={["left", "right", "left"]}
          rows={[
            [
              "Bundle mix (1/2/3+)",
              "−1.18M 3+ hh; +0.42M 2P",
              "The lost relationships are the old cable bundle, not the 2-product add",
            ],
            [
              "Dollar mix (res. P&L)",
              "Video −8.8 ppt; mobile +6.0 ppt",
              "Video still sheds more residential share than mobile gains",
            ],
            [
              "Attach (derived)",
              "Video/Internet −6.2 ppt; mobile lines/Internet +0.24",
              "Voice −9.8 ppt. Pair leaving is video+voice; pair arriving is mobile lines",
            ],
          ]}
          rowTone={["danger", "danger", "info"]}
        />
        <Text size="small" tone="tertiary">
          Frames disagree about how complete the substitution is (0.42M in vs
          1.18M out on households; +6.0 vs −8.8 ppt on dollars). That gap is
          the finding. 2-product = Internet+Mobile is INTERPRETIVE — Charter
          does not disclose which two products.
        </Text>
      </Stack>

      <Grid columns={2} gap={16}>
        <Card>
          <CardHeader>Two builds</CardHeader>
          <CardBody>
            <Stack gap={8}>
              <Text>
                <Text as="span" weight="semibold">Build 1 — customers.</Text>{" "}
                Disclosed 1/2/3+ % × residential CR. 3+ 6,335k → 5,153k. 2P
                9,851k → 10,276k. Q1 2026 already 5,154k / 10,249k.
              </Text>
              <Text>
                <Text as="span" weight="semibold">Build 2 — dollars.</Text>{" "}
                Residential P&L shares. Video $4,254M → $3,149M (−$1,105M).
                Mobile $497M → $1,095M (+$598M). Internet +$58M on a smaller
                base.
              </Text>
              <Text tone="secondary">
                No shared identity (headcount is not dollars). They agree on
                direction. That is two filing tables pointing the same way —
                not proof that 2-product is Internet+Mobile, and not a churn
                rate.
              </Text>
            </Stack>
          </CardBody>
        </Card>
        <Card>
          <CardHeader>Cross-check that shares no mix %</CardHeader>
          <CardBody>
            <Stack gap={8}>
              <Text>
                Programming expense (a cost account): $2,799M → $2,035M
                (−27.3%). Video revenue −26.0%. Video customers −16.0%.
                Revenue fell faster than customers — disclosed as a higher mix
                of lower-priced video packages.
              </Text>
              <Text>
                Adding back Q2 2026’s $251M allocation (23Q1 treated as $0,
                ESTIMATED): video −20.1%, programming −18.3%. Same direction,
                smaller hole. Allocation is why the printed video-share drop
                overstates the economic mix shift in 2026.
              </Text>
            </Stack>
          </CardBody>
        </Card>
      </Grid>

      <Stack gap={8}>
        <H2>The two phases, in the numbers</H2>
        <Table
          headers={["", "Phase 1 · 23Q1–24Q3 unbundle", "Phase 2 · 24Q3–26Q2 reconverge"]}
          rows={[
            ["1-product mix", "46.6% → 49.0% (peak)", "49.0% → 47.4% (reversed 1.6 ppt)"],
            ["2-product mix", "32.5–32.7% (flat seven quarters)", "32.7% → 35.1% (up every quarter)"],
            ["3+ mix", "20.9% → 18.3%", "18.3% → 17.6% (floor ~17.5%)"],
            ["2P households", "9,851k → 9,847k (flat)", "9,847k → 10,276k (+429k)"],
            ["3+ households", "6,335k → 5,511k (−824k)", "5,511k → 5,153k (−358k, slowing)"],
            ["Video / Internet", "50.1% → 44.1%", "44.1% → 43.9% (also floored)"],
            ["Mobile lines / Internet", "0.20 → 0.32", "0.32 → 0.44"],
          ]}
          rowTone={[undefined, "info", "danger", "info", "danger", "danger", "info"]}
        />
        <Text size="small" tone="tertiary">
          Products per residential CR (3+ counted as 3, DERIVED) fell 1.743 →
          1.688 by 25Q1–25Q2, then ticked up to 1.704 — intensity stopped
          falling once 2-product attach outran remaining 3+ roll-off. Source:
          same operating-statistics table
        </Text>
      </Stack>

      <Divider />

      <Stack gap={8}>
        <H2>Size is not opportunity: mix working does not close the Internet print</H2>
        <Table
          headers={["Product / mix bucket", "Q1 2026 revenue share", "Can it close Internet −120k / −$78M?"]}
          columnAlign={["left", "right", "left"]}
          rows={[
            ["Internet", "43.0% ($5,852M / $13,597M)", "This is the print"],
            ["2-product mix (35% of res. CR)", "Not a P&L line", "No — mix can rise while Internet customers leave"],
            ["Mobile service", "7.7%", "No — Root C; lower-margin MVNO; lines ≠ Internet customers"],
            ["Video", "23.9%", "No — secular + allocation; 3+ already floored"],
            ["Voice", "2.5%", "No"],
          ]}
          rowTone={["danger", "warning", "neutral", "neutral", "neutral"]}
        />
        <Text size="small" tone="tertiary">
          Q1 2026: mobile +$138M YoY fills the connectivity subtotal (+$60M)
          and does not re-rate Internet −$78M. Q2 later fact: Internet −$193M,
          mobile +$174M, connectivity −$19M. Connectivity first crossed 50% of
          company revenue in 25Q2 (50.05%), not as a 2026 event.
        </Text>
      </Stack>

      <Grid columns={2} gap={16}>
        <Stack gap={8}>
          <H3>Dollar-weighted origin</H3>
          <Text>
            Every mix percentage and every revenue dollar in the headline is
            RETRIEVED. Estimated share of the dollar answer:{" "}
            <Text as="span" weight="semibold">0%</Text>. Household counts are
            formulas on two retrieved series (flagged DERIVED). The 23Q1
            allocation = $0 add-back is ESTIMATED.
          </Text>
          <Text tone="secondary">
            The missing input — which two products sit in the 2-product
            bucket — carries none of the dollar answer and all of the leverage
            on a GTM claim. Stop refining −1.18 million. Go retrieve the
            composition, or treat “Internet+Mobile” as a hypothesis.
          </Text>
        </Stack>
        <Stack gap={8}>
          <H3>Sensitivity / leverage</H3>
          <Table
            headers={["Input", "If it moves", "What breaks"]}
            rows={[
              ["2P composition", "Internet+video, not +mobile", "The Life Unlimited read"],
              ["Seamless allocation", "Q2 $251M of video $", "Printed −8.8 ppt overstates"],
              ["0.1 ppt rounding", "±~30k households", "Not the 1.18M"],
              ["3 vs 4 inside 3+", "Unknown", "Products/CR only"],
            ]}
            framed={false}
          />
        </Stack>
      </Grid>

      <Callout tone="warning" title="Kill rule (before any recommendation)">
        If two consecutive quarters show 3+ mix rising ≥0.5 ppt while Internet
        net adds stay negative, kill “unbundling is the live mix story” — it
        has already floored. If 2-product mix is flat for two quarters while
        mobile lines still grow ≥300k, kill “2-product is the mobile-attach
        vehicle” (multi-lining on the existing 2P base). If video’s share,
        adding back allocation, stops falling and Internet dollars grow, kill
        “mix is a durable P&L drag” — that is FY2025 rate/mix again. Do not
        launch a bundle program from this file. Net mix cannot tell save-rate
        from sell-in.
      </Callout>

      <Stack gap={8}>
        <H2>Unwilling to claim</H2>
        <Text>
          That 2-product is specifically Internet+Mobile (not disclosed). A
          churn rate, or that mix shift caused Internet losses. Product-level
          EBITDA or that mobile dollars replace video dollars at the same
          margin. That two builds agreeing proves anything other than table
          consistency. That 3+ ticking 17.5% → 17.6% in 26Q2 is a turn. Mixed
          pre/post Q4 2025 customer bases. That this supersedes GAP or Root C.
        </Text>
      </Stack>

      <Divider />

      <Stack gap={6}>
        <H3>Quarterly mix (lookup)</H3>
        <Table
          headers={["Qtr", "1P %", "2P %", "3+ %", "2P hh (k)", "3+ hh (k)", "Video % res $", "Mobile % res $", "Vid/Inet %"]}
          columnAlign={["left", "right", "right", "right", "right", "right", "right", "right", "right"]}
          striped
          stickyHeader
          rows={QTRS.map((q, i) => [
            q,
            P1[i].toFixed(1),
            P2[i].toFixed(1),
            P3[i].toFixed(1),
            H2_HH[i].toLocaleString(),
            H3_HH[i].toLocaleString(),
            VID_SHARE[i].toFixed(1),
            MOB_SHARE[i].toFixed(1),
            VID_ATTACH[i].toFixed(1),
          ])}
          rowTone={QTRS.map((q) =>
            q === "24Q3" ? "warning" : q === "26Q1" ? "info" : q === "26Q2" ? "neutral" : undefined,
          )}
        />
        <Text size="small" tone="tertiary">
          24Q3 highlighted as the phase break. 26Q1 is the assignment anchor.
          Internet residential share (not shown): 52.7% → 55.8%, peaked 56.5%
          in 25Q4. Mobile lines per residential Internet customer:{" "}
          {MOB_PER_INET[0].toFixed(2)} → {MOB_PER_INET[MOB_PER_INET.length - 1].toFixed(2)}.
          Inet residential $ share last print {INET_SHARE[INET_SHARE.length - 1].toFixed(1)}%.
          Arithmetic in Analysis/product_mix_model.py matches this canvas.
        </Text>
      </Stack>

      <Text size="small" tone="tertiary">
        Does not clobber GAP, the if-lost-to-X playbook, or
        Analysis/customer-performance.md. Those remain the Internet-print
        files. This file is the mix path those snapshots sit on.
      </Text>
    </Stack>
  );
}
