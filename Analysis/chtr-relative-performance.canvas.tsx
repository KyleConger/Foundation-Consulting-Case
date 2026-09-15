/**
 * Charter relative performance vs cable peer (CMCSA) and broadband attackers.
 * Gaps shown as magnitudes for at-a-glance reads.
 * Assignment anchor: Q1 2026; Q2 labeled later public fact.
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

function GapPill({
  label,
  tone,
}: {
  label: string;
  tone?: "danger" | "success" | "warning" | "info" | "neutral";
}) {
  const pillTone =
    tone === "danger" ? "deleted" : tone === "neutral" ? undefined : tone;
  return <Pill tone={pillTone}>{label}</Pill>;
}

export default function ChtrRelativePerformance() {
  return (
    <Stack gap={28}>
      <Stack gap={8}>
        <Row gap={8} wrap>
          <Pill tone="info">Relative performance</Pill>
          <Pill tone="warning">Cable peer = CMCSA</Pill>
          <Pill>Q1 2026 anchor · Q2 later</Pill>
        </Row>
        <H1>Charter vs the market — where we stand</H1>
        <Text tone="secondary">
          Gaps are signed vs Comcast unless noted. Negative gap = Charter
          worse; positive = Charter ahead. Magnitudes first, then charts.
        </Text>
      </Stack>

      <Callout tone="warning" title="Definition note">
        Charter = total Internet; Comcast = domestic residential broadband.
        Mobile = Spectrum Mobile lines vs CMCSA domestic wireless. Stock
        multi-year returns from secondary screeners (≈ mid/late 2026) — verify
        on Yahoo before pitching exact %.
      </Callout>

      <Stack gap={8}>
        <H2>Gap at a glance (vs CMCSA)</H2>
        <Grid columns={4} gap={12}>
          <Stat
            value="−55k"
            label="Q1 BB: CHTR lost 55k more (1.8× peer losses)"
            tone="danger"
          />
          <Stat
            value="−179k"
            label="Q1 BB YoY slope gap (CHTR −61k vs CMCSA +118k)"
            tone="danger"
          />
          <Stat
            value="−67k"
            label="Q1 mobile: 15% fewer adds (−67k / 435k)"
            tone="warning"
          />
          <Stat
            value="+262k"
            label="Q1 video: 262k fewer losses than peer"
            tone="success"
          />
        </Grid>
        <Grid columns={4} gap={12}>
          <Stat
            value="−12.6ppt"
            label="Apr 24 tape: −25.5% vs −12.9% (~2.0×)"
            tone="danger"
          />
          <Stat
            value="−22ppt"
            label="≈1Y return gap (−46% vs −24%)"
            tone="danger"
          />
          <Stat
            value="−30ppt"
            label="≈5Y return gap (−82% vs −52%)"
            tone="danger"
          />
          <Stat
            value="+3.8ppt"
            label="Internet/$ BB YoY: −1.3% vs −5.1%"
            tone="success"
          />
        </Grid>
      </Stack>

      <Table
        headers={["Area", "CHTR", "CMCSA", "Gap (CHTR − peer)", "Read"]}
        columnAlign={["left", "right", "right", "right", "left"]}
        rowTone={[
          "danger",
          "danger",
          "warning",
          "success",
          "success",
          "info",
          "danger",
          "danger",
          "danger",
        ]}
        rows={[
          ["Broadband adds Q1’26", "−120k", "−65k", "−55k (1.8×)", "Worse"],
          ["Broadband YoY Δ Q1", "−61k", "+118k", "−179k swing", "Worse"],
          ["Mobile adds Q1’26", "+368k", "+435k", "−67k (−15%)", "Close / behind"],
          ["Video adds Q1’26", "−60k", "−322k", "+262k", "Ahead"],
          ["Internet / dom. BB $ YoY", "−1.3%", "−5.1%", "+3.8ppt", "Ahead on $"],
          ["Adj. EBITDA YoY*", "−2.2%", "−6.0%", "+3.8ppt", "Less down"],
          ["Apr 24 close-to-close", "−25.5%", "−12.9%", "−12.6ppt (~2×)", "Worse"],
          ["≈1Y total return", "−46%", "−24%", "−22ppt", "Worse"],
          ["≈5Y total return", "−82%", "−52%", "−30ppt", "Worse"],
        ]}
        striped
      />
      <Text size="small" tone="tertiary">
        *CHTR consolidated Adj. EBITDA vs CMCSA Resid. Connectivity & Platforms
        Adj. EBITDA. 1Y/5Y ≈ from peer comparison screens (BriMind / AltIndex
        class sources) — not Yahoo closes on a fixed end date.
      </Text>

      <Divider />

      <Stack gap={8}>
        <Row gap={8} align="center" wrap>
          <H2>1. Broadband net adds</H2>
          <GapPill label="Q1 gap −55k · 1.8× peer losses" tone="danger" />
        </Row>
        <Text>
          Both still negative. Absolute gap: Charter lost 55k more in Q1 than
          Comcast. Q2 later: −172k vs −167k (nearly tied on the print; YoY
          slope still worse).
        </Text>
        <SignedBarChart
          categories={["Q1 2025", "Q1 2026", "Q2 2025", "Q2 2026"]}
          series={[
            {
              name: "CHTR Internet (000s)",
              data: [-59, -120, -116, -172],
              tone: "danger",
            },
            {
              name: "CMCSA domestic resid. BB (000s)",
              data: [-183, -65, -201, -167],
              tone: "warning",
            },
          ]}
          height={260}
          valueSuffix="k"
          yMin={-220}
          yMax={40}
          zeroLabel="0"
        />
        <Text size="small" tone="tertiary">
          Thousands · CHTR Ex99.1 · CMCSA Ex99.1 · Q2 = later public fact
        </Text>
      </Stack>

      <Stack gap={8}>
        <Row gap={8} align="center" wrap>
          <H2>2. YoY change in broadband net adds</H2>
          <GapPill label="Q1 slope gap −179k" tone="danger" />
        </Row>
        <Text>
          Positive = improved vs year-ago. Charter −61k vs Comcast +118k is a
          179k relative swing — the largest operating gap in the set.
        </Text>
        <SignedBarChart
          categories={["Q1 YoY Δ", "Q2 YoY Δ (later)"]}
          series={[
            { name: "CHTR", data: [-61, -56], tone: "danger" },
            { name: "CMCSA", data: [118, 34], tone: "success" },
          ]}
          height={240}
          valueSuffix="k"
          yMin={-80}
          yMax={140}
          zeroLabel="Flat YoY"
        />
      </Stack>

      <Stack gap={8}>
        <Row gap={8} align="center" wrap>
          <H2>3. Mobile / wireless net adds</H2>
          <GapPill label="Q1 gap −67k (−15%)" tone="warning" />
        </Row>
        <SignedBarChart
          categories={["Q1 2025", "Q1 2026", "Q2 2026 (later)"]}
          series={[
            {
              name: "CHTR mobile lines (000s)",
              data: [507, 368, 406],
              tone: "info",
            },
            {
              name: "CMCSA domestic wireless (000s)",
              data: [323, 435, 448],
              tone: "success",
            },
          ]}
          height={240}
          valueSuffix="k"
          yMin={0}
          yMax={500}
          zeroLabel="0"
        />
        <Text size="small" tone="tertiary">
          Same order of magnitude; not the priced variable.
        </Text>
      </Stack>

      <Stack gap={8}>
        <Row gap={8} align="center" wrap>
          <H2>4. Video net adds</H2>
          <GapPill label="Q1 gap +262k fewer losses" tone="success" />
        </Row>
        <SignedBarChart
          categories={["Q1 2025", "Q1 2026", "Q2 2026 (later)"]}
          series={[
            {
              name: "CHTR video (000s)",
              data: [-181, -60, -21],
              tone: "info",
            },
            {
              name: "CMCSA domestic video (000s)",
              data: [-427, -322, -280],
              tone: "warning",
            },
          ]}
          height={240}
          valueSuffix="k"
          yMin={-460}
          yMax={40}
          zeroLabel="0"
        />
      </Stack>

      <Divider />

      <Stack gap={8}>
        <Row gap={8} align="center" wrap>
          <H2>5. Cable-like dollars — YoY % (Q1 2026)</H2>
          <GapPill label="BB $ +3.8ppt · EBITDA +3.8ppt" tone="success" />
        </Row>
        <SignedBarChart
          categories={[
            "Internet / Dom. BB $",
            "Mobile / Wireless svc $",
            "Adj. EBITDA*",
            "Total / Resid. C&P rev",
          ]}
          series={[
            {
              name: "CHTR YoY %",
              data: [-1.3, 15.1, -2.2, -1.0],
              tone: "danger",
            },
            {
              name: "CMCSA YoY %",
              data: [-5.1, 15.0, -6.0, -1.9],
              tone: "warning",
            },
          ]}
          height={280}
          valueSuffix="%"
          yMin={-8}
          yMax={18}
          zeroLabel="0%"
        />
        <Text size="small" tone="tertiary">
          Mobile service nearly tied (+15.1% vs +15.0%). Dollar lines are ahead
          even while the Internet sub print is behind.
        </Text>
      </Stack>

      <Stack gap={8}>
        <Row gap={8} align="center" wrap>
          <H2>6. Market share shift — attackers</H2>
          <GapPill label="TMUS FWA ≈ +470k vs CHTR −120k" tone="info" />
        </Row>
        <SignedBarChart
          categories={[
            "CHTR Internet",
            "CMCSA resid. BB",
            "VZ FWA",
            "TMUS FWA (≈)",
          ]}
          series={[
            {
              name: "Q1 2026 net adds (000s)",
              data: [-120, -65, 214, 470],
              tone: "info",
            },
          ]}
          height={260}
          valueSuffix="k"
          yMin={-150}
          yMax={520}
          zeroLabel="0"
        />
      </Stack>

      <Divider />

      <Stack gap={8}>
        <Row gap={8} align="center" wrap>
          <H2>7. Stock price — absolute and vs peer</H2>
          <GapPill label="Day −12.6ppt · 1Y −22ppt · 5Y −30ppt" tone="danger" />
        </Row>
        <Text>
          Operating gaps show up in price. Charter is down more on the trigger
          day, over ~1 year, and over ~5 years — the stock gap is larger than
          the Q1 broadband headcount gap alone would suggest.
        </Text>

        <Grid columns={3} gap={12}>
          <Stat value="$180.13" label="CHTR close Apr 24 2026" tone="danger" />
          <Stat value="$27.56" label="CMCSA close Apr 24 2026" tone="warning" />
          <Stat
            value="−12.6ppt"
            label="Same-day return gap (CHTR − CMCSA)"
            tone="danger"
          />
        </Grid>

        <H2>7a. Returns by horizon</H2>
        <SignedBarChart
          categories={["Apr 24 day", "≈1Y total", "≈5Y total"]}
          series={[
            {
              name: "CHTR %",
              data: [-25.5, -46, -82],
              tone: "danger",
            },
            {
              name: "CMCSA %",
              data: [-12.9, -24, -52],
              tone: "warning",
            },
          ]}
          height={260}
          valueSuffix="%"
          yMin={-90}
          yMax={5}
          zeroLabel="0%"
        />
        <Text size="small" tone="tertiary">
          Apr 24: Yahoo CHTR $241.78→$180.13 (−25.5%); CMCSA ≈$31.64→$27.56
          (−12.9%). 1Y/5Y ≈ screener totals (CHTR −46%/−82%; CMCSA −24%/−52%) —
          case brief also cites CHTR ~−80% over five years.
        </Text>

        <H2>7b. Excess drawdown vs peer (CHTR − CMCSA)</H2>
        <SignedBarChart
          categories={["Apr 24 day", "≈1Y", "≈5Y"]}
          series={[
            {
              name: "Extra CHTR underperformance (ppt)",
              data: [-12.6, -22, -30],
              tone: "danger",
            },
          ]}
          height={220}
          valueSuffix="ppt"
          yMin={-35}
          yMax={5}
          zeroLabel="0"
        />
        <Text size="small" tone="tertiary">
          How much farther Charter fell than Comcast on each horizon. Day gap
          ≈2.0× peer’s drop; 1Y ≈1.9×; 5Y ≈1.6×.
        </Text>

        <H2>7c. CHTR absolute price on earnings dates</H2>
        <SignedBarChart
          categories={[
            "Jan 31’25",
            "Apr 25’25",
            "Jul 25’25",
            "Oct 31’25",
            "Jan 30’26",
            "Apr 24’26",
            "Jul 24’26",
          ]}
          series={[
            {
              name: "CHTR close ($)",
              data: [345.49, 373.65, 309.75, 233.84, 206.12, 180.13, 123.31],
              tone: "danger",
            },
          ]}
          height={240}
          valuePrefix="$"
          yMin={0}
          yMax={400}
          zeroLabel="$0"
        />
        <Text size="small" tone="tertiary">
          Yahoo daily close on earnings date · issue-tree canvas series. From
          Apr 25’25 peak close ($373.65) to Jul 24’26 ($123.31) ≈ −67% on this
          earnings-date path alone.
        </Text>

        <Table
          headers={["Horizon", "CHTR", "CMCSA", "Gap", "Multiple of peer drop"]}
          columnAlign={["left", "right", "right", "right", "right"]}
          rowTone={["danger", "danger", "danger"]}
          rows={[
            ["Apr 24 2026 day", "−25.5%", "−12.9%", "−12.6ppt", "2.0×"],
            ["≈1 year", "−46%", "−24%", "−22ppt", "1.9×"],
            ["≈5 years", "−82%", "−52%", "−30ppt", "1.6×"],
          ]}
          striped
        />
      </Stack>

      <Divider />

      <Callout tone="info" title="Glance takeaway">
        Worst gaps: broadband YoY slope (−179k swing) and stock (−12.6ppt day /
        −22ppt 1Y / −30ppt 5Y). Best gaps: video (+262k) and Internet $ YoY
        (+3.8ppt). Mobile is close (−15%). Relative underperformance is
        concentrated in the Internet trajectory and the equity, not in every
        operating line.
      </Callout>

      <Text size="small" tone="tertiary">
        Sources: CHTR / CMCSA Ex99.1 Q1–Q2 2026 · Yahoo earnings-date closes ·
        VZ FOI Q1 2026 · TMUS FWA ≈ trade recon · 1Y/5Y peer screens
        (secondary). Analysis canvas, not a filing.
      </Text>
    </Stack>
  );
}
