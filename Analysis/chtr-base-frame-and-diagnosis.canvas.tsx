/**
 * Charter MAN6930 — working problem page (DRAFT framing/diagnosis).
 * Integrates committed Root B, rural/core conversion (audited), the
 * critical review, and the strongest public mix proxy vs Comcast.
 * Supersedes using chtr-base-frame + chtr-broadband-expansion-diagnosis
 * as two separate live commitments. Those files remain as history.
 * Assignment anchor: end Q1 2026. Q2 labeled later public fact.
 */
import {
  BarChart,
  Callout,
  Card,
  CardBody,
  CardHeader,
  CollapsibleSection,
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
  Swatch,
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

/** A-lines: Q1 2026 retrieved stocks / flows (thousands unless $). */
const A1_RURAL_PASS = 1385;
const A2_RURAL_CR = 527;
const A3_RURAL_PEN = A2_RURAL_CR / A1_RURAL_PASS; // 38.05%
const A4_CO_CR = 31683;
const A5_CO_INET = 29560;
const A6_CO_CR_ADD = -163;
const A7_RURAL_CR_ADD = 41;
const A8_CORE_CR_ADD = A6_CO_CR_ADD - A7_RURAL_CR_ADD; // -204
const A9_COVER = A7_RURAL_CR_ADD / Math.abs(A8_CORE_CR_ADD); // 0.201
const B1_CO_INET_ADD = -120;
const B2_CORE_INET = B1_CO_INET_ADD - A7_RURAL_CR_ADD; // -161
const B4_RURAL_ACCEL = 41 - 39; // +2
const B5_CHTR_INET_YOY = -120 - -59; // -61
const B6_CMCSA_YOY = -65 - -183; // +118
const B7_SLOPE_GAP = B5_CHTR_INET_YOY - B6_CMCSA_YOY; // -179
const B8_CORE_INET_YOY = -161 - -98; // -63
const B9_CORE_SLOPE = B8_CORE_INET_YOY - B6_CMCSA_YOY; // -181
const C1_RURAL_RES_REV = 167;
const C2_INET_REV_YOY = 5852 - 5930; // -78
const C5_RURAL_SHARE = 221 / 13597; // 1.625%
const D1_REMAINDER_PASS = 1700 - A1_RURAL_PASS; // 315
const D2_REMAINDER_38 = Math.floor(D1_REMAINDER_PASS * A3_RURAL_PEN); // 120
const D3_REMAINDER_54 = Math.floor(D1_REMAINDER_PASS * 0.54); // 170
const E_CONN = 30520;
const E_MOBILE_ONLY = E_CONN - A5_CO_INET; // 960
const E_VV_ONLY = A4_CO_CR - E_CONN; // 1163
const E_NON_INET = A4_CO_CR - A5_CO_INET; // 2123
const E_D_NON_INET = A6_CO_CR_ADD - B1_CO_INET_ADD; // -43
const E_D_CONN = -120;
const E_D_MOBILE_ONLY = E_D_CONN - B1_CO_INET_ADD; // 0

export default function ChtrBaseFrameAndDiagnosis() {
  return (
    <Stack gap={28}>
      <Stack gap={8}>
        <Row gap={8} align="center" wrap>
          <Pill tone="warning">DRAFT — working problem page</Pill>
          <Pill tone="deleted">Supersedes split base-frame + expansion-diagnosis</Pill>
          <Pill>Root B · hypothesis</Pill>
          <Pill>Q1 2026 anchor · Q2 later</Pill>
        </Row>
        <Text size="small" tone="tertiary">
          This is the live problem statement. Do not treat
          chtr-base-frame or chtr-broadband-expansion-diagnosis as separate
          commitments; those files stay as history. Role labels from
          industry-vs-firm framestorm §4–5. Critique:
          chtr-diagnosis-critical-review. Conversion audit:
          chtr-rural-core-conversion. Not a CEO recommendation.
        </Text>
      </Stack>

      <Stack gap={10}>
        <H1>
          Core Internet is where the slope broke versus Comcast. Rural converts
          and cannot close the gap. Mix-adjusted core rates are still unmeasured.
        </H1>
        <Text tone="secondary">
          Constraint, not a pre-chosen fix: Charter’s{" "}
          <Text as="span" weight="semibold">
            non-rural Internet trajectory versus Comcast
          </Text>
          , with the subsidized-rural program already running and too small to
          be the closer. Root B (worse YoY Internet slope than CMCSA) stays a
          hypothesis until a DMA / overbuild overlay exists. Rural expansion is
          an in-flight program, not the operating issue.
        </Text>
      </Stack>

      <Callout tone="danger" title="Working verdict (Q1 2026)">
        Company CR −163k = rural +41k + core −204k. Rural covered 20% of the
        core hole and is already inside the print. Company Internet −120k;
        rural CR as Internet proxy → core −161k versus Comcast domestic
        residential broadband −65k. Rural add acceleration versus Q1 2025 is
        only +2k — none of the −61k Internet YoY break. Remainder to the 1.7M
        passing floor is a one-time stock of 120k at current take, 170k at
        company take — both below the 179k quarterly slope gap. Promote: the
        slope break is in the core; leftover rural cannot close Comcast; rural
        is converting, so “just execute rural harder” is the wrong play. Do
        not promote: a proven firm GTM/product gap versus Comcast. That still
        needs mix-adjusted core rates.
      </Callout>

      <Grid columns={4} gap={12}>
        <Stat value="−204k" label="Core CR adds Q1’26 (company − rural)" tone="danger" />
        <Stat value="+41k" label="Rural CR adds (already in the −163k print)" tone="info" />
        <Stat value="170k" label="Remainder stock @54% take vs 179k qtr gap" tone="warning" />
        <Stat value="Unmeasured" label="Mix-adjusted core vs CMCSA" tone="danger" />
      </Grid>

      <UsageBar
        total={204}
        topLeftLabel="Rural covered 20% of the Q1 core CR hole — and is already in the company print"
        topRightLabel="+41k rural / 204k core losses"
        segments={[
          { id: "rural", value: 41, color: "blue" },
          { id: "uncovered", value: 163, color: "orange" },
        ]}
      />
      <Text size="small" tone="tertiary">
        A8 = A6 − A7 = −163 − 41 = −204. Cover A9 = 41 / 204 = 20%. Source:
        CHTR Q1 2026 Ex99.1 (company paid) · trending rural stocks (unofficial
        IR extract; +41k cross-checks to Ex99.1).
      </Text>

      <Stack gap={8}>
        <H2>Remainder stock versus the quarterly slope gap</H2>
        <Text>
          First three bars are Q1 2026 flows. Last two are lifetime customer
          stocks from leftover passings to the 1.7M floor — different units,
          shown together so the scale fail is visible. Point estimate, rounded
          toward the expansion thesis: 170k at company 54% take. Still below
          179k in one quarter.
        </Text>
        <SignedBarChart
          categories={[
            "Q1 slope gap vs CMCSA",
            "Q1 rural CR adds",
            "Core CR hole Q1",
            "Remainder @38%",
            "Remainder @54%",
          ]}
          series={[
            {
              name: "Thousands (quarterly flow vs lifetime remaining stock)",
              data: [Math.abs(B7_SLOPE_GAP), A7_RURAL_CR_ADD, Math.abs(A8_CORE_CR_ADD), D2_REMAINDER_38, D3_REMAINDER_54],
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
          D1 = 1,700 − 1,385 = 315k leftover passings. D2 = floor(315 × 0.381)
          = 120k. D3 = floor(315 × 0.540) = 170k. 1.7M is a 10-K floor (“over
          1.7 million”), not a cap. Q2 2026 activations (later public fact)
          shrink remainder further. Source: FY2025 10-K · Q1 trending rural
          page · CMCSA Ex99.1 Q1 2026.
        </Text>
      </Stack>

      <Divider />

      <Stack gap={10}>
        <H2>Committed root — still a hypothesis</H2>
        <Text>
          From framestorm §4–5: Root B is relative underperformance — peers
          face the same fiber/FWA attackers; Charter’s YoY Internet slope is
          worse than Comcast’s. The binding operating problem, if B holds, is
          Charter’s relative broadband game, not that cable alone is under
          attack and not that the equity is “mispriced.” Falsifier named then
          and still unrun: DMA-mix adjusted Internet loss rates converge with
          CMCSA.
        </Text>
        <Grid columns={2} gap={12}>
          <Card>
            <CardHeader trailing={<Pill tone="info" size="sm">Floor</Pill>}>
              Root A · Industry
            </CardHeader>
            <CardBody>
              <Text size="small">
                Structural share-shift to fiber / FWA. Explains peer losses
                and the sector multiple. Not the operating root we solve from
                — and not dropped.
              </Text>
            </CardBody>
          </Card>
          <Card>
            <CardHeader trailing={<Pill size="sm">Gate</Pill>}>
              Root C · Belief
            </CardHeader>
            <CardBody>
              <Text size="small">
                Tape prices Internet YoY surprise / run-rate, not cash or
                mobile. Hard constraint for any later rec — not the A-vs-B
                cause fork.
              </Text>
            </CardBody>
          </Card>
        </Grid>
        <Table
          headers={["Still live under A/B", "Role", "Note"]}
          columnAlign={["left", "left", "left"]}
          rows={[
            [
              "Installed-base / move drought (housing)",
              "Rival mechanism under A",
              "Industry gross-add weakness; does not alone explain CHTR vs CMCSA YoY",
            ],
            [
              "Price / promo in overlap zips",
              "Rival mechanism under B",
              "Live. Not a ‘small perception fix.’",
            ],
            [
              "HFC / DOCSIS credibility vs FTTH",
              "Rival mechanism under A/B",
              "Competes with GTM/pricing as the firm gap",
            ],
            [
              "Converged-attacker / MVNO (carriers own spectrum)",
              "Rival mechanism under A/B",
              "Competes with ‘just price better’ as the fix",
            ],
            [
              "Mix / footprint (overbuild & FWA intensity vs CMCSA)",
              "Cheap binary gate — still open",
              "If the gap vanishes after overlay, A dominates",
            ],
            [
              "Buybacks / ‘undervalued’ / stage capital",
              "Decision architecture — DEMOTED",
              "Symptom of de-rating after we know the operating problem",
            ],
          ]}
          striped
        />
        <Callout tone="warning" title="Strawman that must not return">
          The live rivals under Root B are mix, price/promo in overlap zips,
          HFC vs FTTH, and MVNO / converged-attacker — not IR narrative,
          perception campaigns, or “expand the product.” Expansion is how you
          would act if reach were the mechanism, after that test. Rural is
          already running.
        </Callout>
      </Stack>

      <Stack gap={10}>
        <H2>What the critique still holds — and what the split changed</H2>
        <Table
          headers={["Critique claim", "After rural/core split", "Status"]}
          columnAlign={["left", "left", "left"]}
          rowTone={["success", "warning", "danger", "success", "success", "danger"]}
          rows={[
            [
              "Rural is a program, not the cause",
              "Split confirms: rural +41k while company Internet −120k; remainder cannot close 179k",
              "Stands — and is now numbered",
            ],
            [
              "Root B is untested until mix control",
              "Split removes rural as the mix explanation (1.7% of CR). Core-overbuild mix vs CMCSA still missing",
              "Stands for core mix",
            ],
            [
              "‘Expand product’ smuggled a solution into the H1",
              "This page names the constraint (core trajectory vs CMCSA; rural too small). Does not pick GTM",
              "Corrected here",
            ],
            [
              "Perception vs expansion was a strawman",
              "Rivals restored: mix, price/promo, HFC vs FTTH, MVNO",
              "Corrected here",
            ],
            [
              "Buybacks / undervalued stay demoted; A is floor; C is gate",
              "Unchanged",
              "Stands",
            ],
            [
              "Units vs dollars: CHTR worse on adds, ahead on Internet $",
              "Still required on the page so diagnosis cannot ignore it",
              "Now on this page",
            ],
          ]}
          striped
        />
      </Stack>

      <Divider />

      <Stack gap={8}>
        <H2>1. Rural vs core customer-relationship flow</H2>
        <Text>
          Charter discloses subsidized-rural customer relationships as a subset
          of the company total. Subtracting them is retrieved arithmetic, not a
          “rural caused the loss” claim. Company −163k in Q1 2026 is the mix of
          +41k rural and −204k core.
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
        <H2>2. CR − Internet identity: what fills the −43k gap</H2>
        <Text>
          Company CR print −163k versus Internet −120k is not a mystery and is
          not mobile-only growth. After the Q4 2025 restatement, CR includes
          mobile-only. Connectivity = Internet and/or mobile. The Q1 flow
          identity:
        </Text>
        <Table
          headers={["Line", "Stock Q1’26 (000s)", "Q1 flow (000s)", "Tag"]}
          columnAlign={["left", "right", "right", "left"]}
          rows={[
            ["Customer relationships", "31,683", "−163", "RETRIEVED Ex99.1"],
            ["Internet customers", "29,560", "−120", "RETRIEVED Ex99.1"],
            ["Connectivity (Internet and/or mobile)", "30,520", "−120", "RETRIEVED Ex99.1"],
            ["Mobile-only (connectivity − Internet)", String(E_MOBILE_ONLY), String(E_D_MOBILE_ONLY), "derived"],
            ["Video/voice-only residual (CR − connectivity)", String(E_VV_ONLY), "−43", "derived"],
            ["Non-Internet CR (CR − Internet)", String(E_NON_INET), String(E_D_NON_INET), "derived; check: 960+1,163=2,123"],
          ]}
          striped
        />
        <Callout tone="info" title="Q1 2026: Δconnectivity = ΔInternet">
          Mobile-only stock was approximately flat company-wide (both
          connectivity and Internet fell 120k). The extra 43k of CR losses
          versus Internet sat in the video/voice-only residual, not in
          mobile-only. That cuts against “rural Internet adds are inflated by
          a mobile-only boom” at the firm level. It does not prove rural CR
          adds are 100% Internet — rural-specific mobile-only is undisclosed.
        </Callout>
      </Stack>

      <Stack gap={8}>
        <H2>3. Internet trajectory — rural CR as proxy, tagged ESTIMATED</H2>
        <Text>
          Rural CR is the closest public proxy for rural Internet (new plant;
          Spectrum Mobile is offered to Internet subscribers). Tag ESTIMATED
          on that identity. Even generously, rural added 41k in Q1 while
          company Internet fell 120k, so the core Internet proxy is −161k.
          Comcast domestic residential broadband: −65k. Definitions are not
          1:1 (CHTR total Internet vs CMCSA domestic residential BB) — use
          for direction and order of magnitude, not as a matched subtraction.
        </Text>
        <SignedBarChart
          categories={[...QTRS]}
          series={[
            { name: "Company Internet (000s)", data: CO_INET_ADD, tone: "warning" },
            { name: "Core Internet proxy (000s)", data: CORE_INET_PROXY, tone: "danger" },
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
          rowTone={["danger", "info", "danger", "warning", "danger", "warning"]}
          rows={[
            ["CHTR Internet adds", "−120k", "RETRIEVED Ex99.1"],
            ["Rural CR adds (Internet proxy)", "+41k", "RETRIEVED CR; ESTIMATED as Internet"],
            ["Core Internet proxy", "−161k", "B2 = B1 − A7"],
            ["CMCSA domestic resid. BB", "−65k", "RETRIEVED Ex99.1"],
            ["CHTR vs CMCSA print gap (includes rural)", "−55k (1.8×)", "derived; definition mismatch"],
            ["Core proxy vs CMCSA level gap", "−96k", "−161 − (−65)"],
          ]}
          striped
        />
        <Callout tone="warning" title="Slope attribution (the Root B symptom)">
          Company Internet YoY: −120k − (−59k) = −61k. Rural add YoY: 41 − 39
          = +2k. Core Internet-proxy YoY: −161k − (−98k) = −63k. Rural
          improved the company slope by 2k; the entire −61k break versus last
          year is the core. CMCSA YoY +118k. Headline slope gap −179k; core
          proxy versus CMCSA −181k.
        </Callout>
        <Callout tone="info" title="Q2 2026 (later public fact — not the assignment print)">
          CHTR Internet −172k vs CMCSA −167k — nearly tied on the level.
          Company CR −184k, rural +47k → core CR −231k; core Internet proxy
          −219k. Same shape, slightly worse. Q2 does not reverse the Q1 slope
          fact the assignment anchors on; it weakens any pitch that Charter is
          uniquely worse on the absolute print every quarter.
        </Callout>
      </Stack>

      <Stack gap={8}>
        <H2>4. Penetration — stock take, not a conversion funnel</H2>
        <Text>
          Rural take of activated passings sat in a 36.9–38.3% band for eight
          quarters (ends Q1’26 at 38.1%), while passings rose 582k → 1,385k.
          Company penetration fell 57.8% → 54.0%. “Sat at 38%” is a rounding
          of that band — it is passing-weighted stock penetration (CR /
          passings), not a disclosed new-passing conversion rate.
        </Text>
        <Grid columns={3} gap={12}>
          <Stat value="38.1%" label="Rural pen of passings (Q1’26)" tone="warning" />
          <Stat value="54.0%" label="Company pen of passings (Q1’26)" />
          <Stat value="38.7%" label="Incremental take Q2’24→Q1’26" tone="info" />
        </Grid>
        <LineChart
          categories={[...QTRS]}
          series={[
            { name: "Rural CR / rural passings (%)", data: RURAL_PEN, tone: "info" },
            { name: "Company CR / company passings (%)", data: CO_PEN, tone: "neutral" },
          ]}
          height={240}
          valueSuffix="%"
          beginAtZero={false}
          yMin={34}
          yMax={60}
        />
        <Text size="small" tone="tertiary">
          Incremental take = (527 − 216) / (1,385 − 582) = 311 / 803 = 38.7%.
          Flow conversion on new passings ≈ stock pen, so this is not just
          “build ahead of sell” with a lag that will snap to 54%. If 1.385M
          rural passings reached company 54% take: 748k CR vs 527k actual —
          221k “missing” on plant already lit.
        </Text>
      </Stack>

      <Stack gap={8}>
        <H2>5. Revenue conversion — real dollars, different base than Internet $</H2>
        <Text>
          Rural residential revenue is growing because the customer stock is
          growing. Do not set $167M rural residential against −$78M company
          Internet dollars as if they were the same P&L line. Rural
          residential is all products on those homes (Internet + video +
          mobile + voice). Company Internet is the Internet product firmwide.
        </Text>
        <Grid columns={4} gap={12}>
          <Stat value="$167M" label="Rural residential rev Q1’26" tone="info" />
          <Stat value="+$63M" label="YoY rural residential" tone="success" />
          <Stat value="−$78M" label="Company Internet rev YoY" tone="danger" />
          <Stat value="1.6%" label="Rural total / company total rev" />
        </Grid>
        <Table
          headers={["Line", "Q1’25", "Q1’26", "Read"]}
          columnAlign={["left", "right", "right", "left"]}
          rows={[
            ["Rural residential ($M)", "104", "167", "All products on rural homes; ARPU $113.71"],
            ["Rural subsidy ($M)", "28", "28", "RDOF-like run-rate, not product"],
            ["Rural other ($M)", "17", "26", "Includes SB / other"],
            ["Rural total ($M)", "149", "221", "221 / 13,597 = 1.6% of firm"],
            ["Company Internet ($M)", "5,930", "5,852", "−1.3% YoY; different base"],
          ]}
          striped
        />
        <Text size="small" tone="tertiary">
          Rural revenue from Q1 2026 trending rural page (company IR extract).
          Company Internet Ex99.1. $167M / $5,852M (2.9%) would overstate
          Internet contribution.
        </Text>
      </Stack>

      <Divider />

      <Stack gap={8}>
        <H2>Audit of the rural/core claims — what survived</H2>
        <Text tone="secondary">
          Team figures treated as evidence to check, not gospel. Arithmetic
          recomputed in code before shipping.
        </Text>
        <Table
          headers={["Claim", "Audit", "Disposition"]}
          columnAlign={["left", "left", "left"]}
          rowTone={["success", "success", "success", "warning", "success", "warning", "warning", "success"]}
          rows={[
            [
              "CR: rural +41k | core −204k | company −163k",
              "−163 − 41 = −204. Ex99.1 + trending stocks",
              "SURVIVED · RETRIEVED identity",
            ],
            [
              "Internet: rural +41k | core −161k | company −120k",
              "−120 − 41 = −161. Rural CR as Internet is the estimated step",
              "SURVIVED as ESTIMATED proxy",
            ],
            [
              "Rural covered 20% of the core hole; already in the print",
              "41/204 = 20.1%. Adding rural back is how you get −163k",
              "SURVIVED",
            ],
            [
              "Rural take sat at 38% for eight quarters",
              "Band 36.9–38.3%; Q1’26 38.1%. Stock pen, not a funnel rate. Incremental take 38.7%",
              "SURVIVED with precision flag",
            ],
            [
              "Rural res $167M, +$63M YoY, 1.6% of firm, vs −$78M Internet $",
              "167, 104→167 = +63, 221/13,597 = 1.6%, 5,852−5,930 = −78. Bases differ — labeled",
              "SURVIVED with base label",
            ],
            [
              "Rural add accel only +2k vs Q1’25; none of the −61k break",
              "41−39 = +2. −120−(−59) = −61. Core proxy YoY −63k",
              "SURVIVED · Q1’25 +39k from trending stocks not Ex99.1",
            ],
            [
              "Comcast slope +118k; remainder 120–170k vs 179k gap",
              "−65−(−183)=+118. 315×0.381→120; 315×0.540→170. Gap −61−118=−179",
              "SURVIVED · 1.7M is a floor; Q2 shrinks remainder (later)",
            ],
            [
              "Kill rural-closes-CMCSA and kill rural-is-not-converting",
              "170k stock < 179k qtr gap; +2k accel. 38% take and $167M/qtr residential",
              "SURVIVED both kills",
            ],
          ]}
          striped
        />

        <CollapsibleSection
          title="Rural CR as Internet proxy — does mobile-only inflate it?"
          leading={<Swatch color="orange" />}
          trailing={<Text size="small">ESTIMATED identity</Text>}
          defaultOpen
        >
          <Text size="small">
            After Q4 2025, customer relationships include mobile-only. Rural
            “Internet” +41k is CR, not a disclosed Internet line. Company-wide,
            connectivity adds equaled Internet adds in Q1 (−120k), so
            mobile-only was flat at the firm. Spectrum Mobile is offered to
            Internet subscribers (FY2025 10-K), which argues most new rural
            relationships are Internet homes — but mobile-only stock is 960k
            company-wide, so leakage is possible. Sensitivity: if only 80% /
            50% of rural CR is Internet, core Internet proxy is −153k / −141k —
            still worse than CMCSA −65k. The CR hole (−204k) is unchanged.
            Round against the expansion thesis: treat some of the +41k as
            non-Internet and the core Internet hole only gets smaller, never
            reversed.
          </Text>
        </CollapsibleSection>
        <CollapsibleSection
          title="Core = company − rural: subset math, not causation"
          leading={<Swatch color="yellow" />}
        >
          <Text size="small">
            Trending footnote: rural customer metrics are a subset of overall
            metrics. Those customers are inside the Internet total. Subtracting
            is the correct split. It does not say rural “caused” or “cured”
            the core. Rural is the only positive CR channel in the print;
            stopping it would worsen the headline. The claim is scale: rural
            cannot close the Comcast slope.
          </Text>
        </CollapsibleSection>
        <CollapsibleSection
          title="Remainder formula and the Q2 shrinking-stock caveat"
          leading={<Swatch color="yellow" />}
        >
          <Text size="small">
            Remainder = max(0, 1,700k − activated passings) × take. Assignment
            anchor end Q1 2026: 1,385k activated, 315k leftover. Q2 later:
            +127k rural passings activated → ~1,512k, leftover ~188k, ×54% ≈
            102k — even less able to close a quarterly gap. Using the 1.7M
            floor understates leftover if the true target is “over 1.7M.” At
            2.0M and 54% take: 615k × 0.54 = 332k lifetime — still ~1.9
            quarters of the 179k gap, one-time, then the program is done.
          </Text>
        </CollapsibleSection>
      </Stack>

      <Divider />

      <Stack gap={8}>
        <H2>Mix-adjusted core versus Comcast — as far as filings allow</H2>
        <Callout tone="danger" title="What mix control would require — still missing">
          DMA- or zip-level Internet loss rates for Charter and Comcast,
          matched on fiber-overbuild intensity and FWA intensity, on the same
          customer definition (residential vs total). Filings do not give that
          overlay. Do not fake a DMA map. Until it exists, Root B is a slope
          observation, not a proven firm GTM/product gap.
        </Callout>
        <Text>
          Strongest available proxy, not a substitute. Four pieces, none of
          which is a matched overbuild overlay.
        </Text>
        <H3>Proxy A — strip rural (CHTR only)</H3>
        <Text size="small">
          Rural is 527k of 31,683k CR (1.7%). Removing it makes Charter’s
          Internet path worse, not better, versus Comcast. Rural mix cannot be
          the explanation of the Q1 slope gap.
        </Text>
        <SignedBarChart
          categories={["Q1 2025", "Q1 2026", "Q2 2025", "Q2 2026 (later)"]}
          series={[
            {
              name: "CHTR company Internet (000s)",
              data: [-59, -120, -116, -172],
              tone: "warning",
            },
            {
              name: "CHTR core Internet proxy (000s)",
              data: [-98, -161, -164, -219],
              tone: "danger",
            },
            {
              name: "CMCSA domestic resid. BB (000s)",
              data: [-183, -65, -201, -167],
              tone: "info",
            },
          ]}
          height={260}
          valueSuffix="k"
          yMin={-240}
          yMax={40}
          zeroLabel="0"
        />
        <Text size="small" tone="tertiary">
          Thousands of net adds. CHTR core Q1’25 = −59 − 39; Q2’25 = −116 −
          48; Q2’26 (later) = −172 − 47. CMCSA series is domestic residential
          broadband — not 1:1 with CHTR total Internet. Source: CHTR/CMCSA
          Ex99.1. Core Q2’26 uses Ex99.1 rural CR +47k on an estimated ending
          stock.
        </Text>
        <H3>Proxy B — CHTR fiber overlap (no Comcast equivalent)</H3>
        <Text size="small">
          FY2025 10-K (company paid): terrestrial 100 Mbps+ competition from
          AT&T in ~27% of Charter’s operating footprint and Verizon in ~16%.
          Those shares are not additive — some homes see both. Comcast does
          not disclose a comparable passing-weighted overlap. Direction:
          Charter’s core is not an unoverbuilt island. Whether Comcast is more
          FiOS-dense (Northeast) or less AT&T-fiber-dense is the blocked
          comparison.
        </Text>
        <BarChart
          horizontal
          height={160}
          categories={["AT&T 100 Mbps+ overlap", "Verizon 100 Mbps+ overlap"]}
          series={[
            {
              name: "Share of CHTR operating footprint (%)",
              data: [27, 16],
              tone: "warning",
            },
          ]}
          valueSuffix="%"
          yMax={40}
        />
        <Text size="small" tone="tertiary">
          Source: CHTR FY2025 10-K Item 1 competition. RETRIEVED. Not a DMA
          overlay. Not additive to 43%.
        </Text>
        <H3>Proxy C — rural construction geography is a weak stand-in for core mix</H3>
        <Text size="small">
          Charter RDOF (Auction 904, CCO Holdings, ~1.06M locations): about
          42% Southeast, 39% Midwest, 13% Texas. Comcast did not bid RDOF;
          its disclosed BEAD provisional locations skew Florida / Virginia /
          Pennsylvania / Arizona / Illinois. That is rural-program geography,
          not core-footprint competitive intensity. Centroid-to-MSA miles on
          the rural canvases are ESTIMATED and were already over-claimed as
          “plant-adjacent competition.” Do not upgrade them to a mix control.
        </Text>
        <H3>Proxy D — Q2 robustness (later public fact)</H3>
        <Text size="small">
          Q2 2026 levels nearly tied (−172k vs −167k). Q1 slope remains the
          assignment fact (CHTR −61k vs CMCSA +118k). A story that “Charter
          uniquely bleeds every quarter” is weaker than a story that Q1 YoY
          inflection diverged. Mix control is still required for both.
        </Text>
        <Callout tone="warning" title="Sensitivity — does mix eat Root B?">
          If a true overbuild/FWA overlay explained the whole Q1 slope gap
          (−179k company, −181k core proxy), Root A dominates and firm GTM is
          the wrong room conversation. If a core gap remains after any honest
          overlay, Root B stays live. Public filings can already reject rural
          as the mix; they cannot accept or reject core-overbuild mix. That is
          still the cheap binary gate. Do not recommend GTM until it exists.
        </Callout>
      </Stack>

      <Divider />

      <Stack gap={8}>
        <H2>Each root produces a number</H2>
        <Text tone="secondary">
          A frame that stays a paragraph did no work. Let them disagree. Shared
          inputs between builds 1 and 2 (the rural CR series) mean their
          agreement is correlation by construction. The remainder/penetration
          stock check does not use net-add subtraction.
        </Text>
        <Table
          headers={["Frame", "Its number (Q1 2026)", "What that decides", "Tag"]}
          columnAlign={["left", "left", "left", "left"]}
          rowTone={["warning", "danger", "danger", "info"]}
          rows={[
            [
              "Root A — industry share-shift",
              "Attackers: VZ FWA +214k (RETRIEVED, prior pack) + TMUS FWA ~+470k (ESTIMATED trade recon) ≈ +684k. Cable: CHTR −120k + CMCSA −65k = −185k",
              "Industry flow is several times combined cable losses. Enough to be the floor. Not enough, by itself, to explain CHTR vs CMCSA",
              "Dollar-weight: TMUS FWA is the estimated piece",
            ],
            [
              "Root B — firm slope vs CMCSA",
              "Core Internet proxy −161k vs CMCSA −65k = 96k extra losses. YoY: core −63k vs CMCSA +118k = −181k slope. Company print −179k",
              "The symptom is in the core. Cause (mix vs offer vs HFC vs MVNO) untested. Do not take ‘firm GTM’ into the room yet",
              "Level gap uses mismatched definitions; slope direction is robust",
            ],
            [
              "Rural-as-lever",
              "Point estimate 170k lifetime remainder at company take (rounded toward expansion). Current take 120k. Quarterly gap 179k. Accel +2k",
              "Kill rural as the closer of the CMCSA slope. Rural is converting (38% take, $167M/qtr residential) so ‘execute rural harder’ is the wrong play",
              "1.7M floor; Q2 later shrinks remainder",
            ],
            [
              "Root C — tape gate (not a cause)",
              "Q1 Internet $ −1.3% (turned negative YoY) while mobile service +15.1% and FCF still positive. Same-day tape −25.5% vs CMCSA −12.9%",
              "A lever that does not move Internet run-rate inside ~24 months fails the market lens — industry or firm",
              "RETRIEVED prints; tape from relative-performance pack",
            ],
          ]}
          striped
        />
        <Text size="small">
          Dollar-weighted retrieved vs estimated on the conversion headline
          (A6/A7/A8): 100% retrieved. On Root A’s attacker total, TMUS ~470k
          of ~684k is estimated (~69% of the attacker add). On Root B’s cause,
          mix-adjusted rates are 0% retrieved — that is where leverage sits
          and where effort has not gone.
        </Text>
      </Stack>

      <Stack gap={8}>
        <H2>Dollar versus unit contradiction</H2>
        <Text>
          Charter lost more Internet customers than Comcast and kept more
          Internet dollars. A firm that is worse on units and ahead on revenue
          is consistent with harvesting ARPU, not only with “our product is
          uncompetitive so expand plant.” If Root C is right that the tape
          prices units, the live 24-month lever on the core is more likely
          price/promo/win-back than lighting leftover rural homes.
        </Text>
        <Grid columns={2} gap={16}>
          <Stack gap={6}>
            <Text size="small" weight="semibold">
              Broadband units — Q1 YoY change in net adds (000s)
            </Text>
            <SignedBarChart
              categories={["CHTR Internet", "CMCSA resid. BB"]}
              series={[
                {
                  name: "YoY Δ in quarterly net adds (000s)",
                  data: [B5_CHTR_INET_YOY, B6_CMCSA_YOY],
                  tone: "danger",
                },
              ]}
              height={200}
              valueSuffix="k"
              yMin={-80}
              yMax={140}
              zeroLabel="0"
            />
            <Text size="small" tone="tertiary">
              CHTR −61k vs CMCSA +118k. Source: Ex99.1 Q1 2026 both companies.
            </Text>
          </Stack>
          <Stack gap={6}>
            <Text size="small" weight="semibold">
              Internet / domestic BB revenue YoY (%)
            </Text>
            <SignedBarChart
              categories={["CHTR Internet $", "CMCSA dom. BB $"]}
              series={[
                {
                  name: "YoY %",
                  data: [-1.3, -5.1],
                  tone: "success",
                },
              ]}
              height={200}
              valueSuffix="%"
              yMin={-6}
              yMax={1}
              zeroLabel="0%"
            />
            <Text size="small" tone="tertiary">
              CHTR −1.3% vs CMCSA −5.1% (+3.8 ppt, Charter ahead on $). Source:
              relative-performance pack / Ex99.1. Adj. EBITDA −2.2% vs −6.0%
              same direction.
            </Text>
          </Stack>
        </Grid>
      </Stack>

      <Divider />

      <Stack gap={8}>
        <H2>Kill: mobile is not a connectivity bandaid for Root B</H2>
        <Text>
          Someone noted “taking mobile into account when it is the third
          smallest revenue driver.” Check the ranking before using that
          sentence. Among seven reported revenue lines, mobile service is the{" "}
          <Text as="span" weight="semibold">
            fourth largest
          </Text>
          — not third smallest unless you drop Other and count six product
          lines from the bottom (voice, ads, then mobile). It is also not
          third largest. Growing fast and still small versus Internet is the
          precise statement: bandaid / optics for the Internet print, not
          “irrelevant forever,” and not the operating problem.
        </Text>
        <BarChart
          horizontal
          height={260}
          categories={[
            "Internet",
            "Video",
            "Commercial",
            "Mobile service",
            "Other",
            "Advertising",
            "Voice",
          ]}
          series={[
            {
              name: "FY2025 revenue ($B)",
              data: [23.8, 13.7, 7.3, 3.8, 3.4, 1.5, 1.4],
              tone: "info",
            },
          ]}
          valuePrefix="$"
          valueSuffix="B"
        />
        <Text size="small" tone="tertiary">
          FY2025, company paid, Ex99.1 / 10-K: Internet $23,765M (43.4%),
          video $13,703M (25.0%), commercial $7,315M (13.4%), mobile service
          $3,762M (6.9%), other $3,411M (6.2%), advertising $1,468M (2.7%),
          voice $1,350M (2.5%). Total $54,774M. Q1 2026 same order: $5,852 /
          $3,252 / $1,839 / $1,052 / $906 / $358 / $338 million on $13,597M
          (mobile service 7.7%).
        </Text>
        <Grid columns={2} gap={16}>
          <Stack gap={6}>
            <Text size="small" weight="semibold">
              Q1 2026 units — Internet customers vs mobile lines (000s)
            </Text>
            <SignedBarChart
              categories={["Internet customers", "Mobile lines"]}
              series={[
                {
                  name: "Q1 2026 net adds (000s)",
                  data: [-120, 368],
                  tone: "warning",
                },
              ]}
              height={200}
              valueSuffix="k"
              yMin={-150}
              yMax={400}
              zeroLabel="0"
            />
            <Text size="small" tone="tertiary">
              Market will not net mobile lines against Internet customers
              (diagnostic graphs). +368k lines did not rescue the multiple.
              Mobile adds also decelerated vs Q1 2025 (+507k).
            </Text>
          </Stack>
          <Stack gap={6}>
            <Text size="small" weight="semibold">
              Q1 2026 dollars YoY — Internet vs mobile service ($M)
            </Text>
            <SignedBarChart
              categories={["Internet revenue", "Mobile service revenue"]}
              series={[
                {
                  name: "YoY $M",
                  data: [C2_INET_REV_YOY, 1052 - 914],
                  tone: "info",
                },
              ]}
              height={200}
              valuePrefix="$"
              valueSuffix="M"
              yMin={-100}
              yMax={160}
              zeroLabel="0"
            />
            <Text size="small" tone="tertiary">
              Internet −$78M YoY; mobile service +$138M YoY (+15.1%). Other
              +$113M is “primarily driven by higher mobile device sales” —
              devices are not connectivity customers either.
            </Text>
          </Stack>
        </Grid>
        <Callout tone="danger" title="Do not re-enter mobile as Root B or as the fix">
          Connectivity customers (Internet and/or mobile) fell 120k in Q1 —
          the same as Internet. Mobile-only stock was flat. Growing mobile
          dollars on a 6.9–7.7% revenue line while Internet customers fall is
          exactly the optics the tape has already refused to net. Keep mobile
          as a sub-branch, not a root.
        </Callout>
      </Stack>

      <Divider />

      <Grid columns={2} gap={16}>
        <Stack gap={8}>
          <H2>Kill rule (write this before any course of action)</H2>
          <Text size="small">
            Kill “rural expansion closes the CMCSA Internet slope” if (i)
            remainder customers even at company take are a one-time stock
            below the quarterly slope gap, and (ii) rural quarterly adds are
            not accelerating. Both true at Q1 2026 (170k vs 179k; +2k).
          </Text>
          <Text size="small">
            Kill “rural is not converting” if take were near zero or revenue
            were subsidy-only — falsified (38% take, $167M/qtr residential).
          </Text>
          <Text size="small">
            Kill Root B as the operating root if a DMA / overbuild overlay
            shows CHTR vs CMCSA core loss rates converging after mix — then
            industry (A) dominates. If the mix-adjusted gap remains, still do
            not default to rural or to mobile.
          </Text>
          <Text size="small">
            Kill mobile-as-connectivity-fix if the tape continues to move with
            Internet units while mobile lines grow — already the Q1 2026
            pattern.
          </Text>
        </Stack>
        <Stack gap={8}>
          <H2>Unwilling to claim</H2>
          <Stack gap={4}>
            <Text size="small">
              • That the Q1 YoY slope vs Comcast is a data error — it is not
            </Text>
            <Text size="small">
              • That industry share-shift is false — it remains the floor
            </Text>
            <Text size="small">
              • A mix-adjusted firm GTM/product gap — that number does not exist
            </Text>
            <Text size="small">
              • Rural Internet customers as a disclosed line (CR is what is public)
            </Text>
            <Text size="small">
              • That stopping rural would help the print (it is the only positive CR channel)
            </Text>
            <Text size="small">
              • A rural ROI year, or that rural NPV is negative
            </Text>
            <Text size="small">
              • That 1.7M passings is a cap (10-K: “over 1.7M” / “over $8B”)
            </Text>
            <Text size="small">
              • That price/GTM on the core is the answer — that would be a new untested mechanism
            </Text>
            <Text size="small">
              • That mobile or “connectivity customers” net against Internet losses
            </Text>
            <Text size="small">
              • A recommendation — this page is draft framing/diagnosis
            </Text>
          </Stack>
        </Stack>
      </Grid>

      <Stack gap={8}>
        <H2>Sequence — cheap gate still first</H2>
        <Table
          headers={["Order", "Work", "Why this order"]}
          columnAlign={["left", "left", "left"]}
          rowTone={["danger", "warning", "info", "neutral"]}
          rows={[
            [
              "1 — still first",
              "DMA / overbuild / FWA overlay: mix-adjusted core loss rates vs Comcast",
              "Binary. If the gap vanishes, stop using Root B. Filings cannot finish this; the client’s loss file or a data pack can",
            ],
            [
              "2",
              "Win/loss reasons in overlap zips (price/promo vs HFC vs FWA vs fiber)",
              "Only after mix. Distinguishes rival mechanisms under B. Class caution on call-center samples",
            ],
            [
              "3",
              "Do not spend the room on more rural passings, IR narrative, buybacks, or mobile-netting",
              "Those levers are already sized or demoted. Rural converts and cannot close the slope",
            ],
            [
              "Not yet",
              "GTM / packaging / plant recommendation",
              "Decision architecture. Comes after the gate, not in the problem statement",
            ],
          ]}
          striped
        />
      </Stack>

      <Callout tone="info" title="Question for the client next (not a pitch)">
        When Comcast’s residential broadband losses improved by 118k YoY in
        Q1 2026 while yours doubled, and your own rural program was already
        adding 41k relationships in the same quarter, what did the win/loss
        file show on the non-rural footprint — mix of fiber/FWA intensity
        versus Comcast, price/promo in overlap zips, HFC versus FTTH, or
        something else — and can we see mix-adjusted core loss rates, or is
        that overlay still unbuilt?
      </Callout>

      <Text size="small" tone="tertiary">
        Sources (company-paid filings unless noted): CHTR Q1 2026 Ex99.1 ·
        Q1 2026 trending schedule (rural page unofficial IR extract; CR adds
        cross-checked to Ex99.1) · FY2025 10-K (1.3M passings; $7.7B; over
        1.7M / over $8B; AT&T ~27% / VZ ~16% overlap; infrastructure-style
        returns) · CMCSA Ex99.1 Q1 2026 · Q2 2026 Ex99.1 labeled later public
        fact · TMUS FWA Q1 add ESTIMATED from prior relative-performance
        recon. Arithmetic recomputed in code. Role labels:
        chtr-industry-vs-firm-framestorm §4–5. Critique integrated:
        chtr-diagnosis-critical-review. Draft — not a recommendation.
        Assignment anchor: end Q1 2026.
      </Text>
    </Stack>
  );
}
