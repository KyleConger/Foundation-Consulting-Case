/**
 * Geographic overview of Charter rural / RDOF footprint.
 * Activated 1.3M passings (YE2025) are reported nationally only.
 * State density uses FCC Auction 904 RDOF locations awarded to CCO Holdings
 * (~1.06M locations across 24 states) as the best public geographic proxy.
 */
import {
  BarChart,
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

/** Charter RDOF Phase I locations by state (FCC Auction 904, CCO Holdings). */
const RDOF: Array<{
  ab: string;
  name: string;
  loc: number;
  x: number;
  y: number;
}> = [
  { ab: "WI", name: "Wisconsin", loc: 143269, x: 580, y: 140 },
  { ab: "TX", name: "Texas", loc: 133993, x: 420, y: 420 },
  { ab: "NC", name: "North Carolina", loc: 128502, x: 760, y: 310 },
  { ab: "OH", name: "Ohio", loc: 112777, x: 680, y: 220 },
  { ab: "SC", name: "South Carolina", loc: 98670, x: 740, y: 350 },
  { ab: "TN", name: "Tennessee", loc: 79193, x: 640, y: 320 },
  { ab: "MO", name: "Missouri", loc: 61524, x: 520, y: 280 },
  { ab: "AL", name: "Alabama", loc: 56451, x: 640, y: 380 },
  { ab: "IN", name: "Indiana", loc: 54541, x: 620, y: 230 },
  { ab: "MI", name: "Michigan", loc: 35944, x: 640, y: 150 },
  { ab: "KY", name: "Kentucky", loc: 31747, x: 660, y: 280 },
  { ab: "LA", name: "Louisiana", loc: 25389, x: 540, y: 420 },
  { ab: "GA", name: "Georgia", loc: 23854, x: 700, y: 380 },
  { ab: "FL", name: "Florida", loc: 17869, x: 740, y: 460 },
  { ab: "OR", name: "Oregon", loc: 15139, x: 120, y: 120 },
  { ab: "MA", name: "Massachusetts", loc: 14344, x: 860, y: 160 },
  { ab: "VA", name: "Virginia", loc: 11369, x: 780, y: 260 },
  { ab: "PA", name: "Pennsylvania", loc: 5328, x: 780, y: 200 },
  { ab: "WA", name: "Washington", loc: 4625, x: 120, y: 70 },
  { ab: "CA", name: "California", loc: 1045, x: 80, y: 280 },
  { ab: "NH", name: "New Hampshire", loc: 1044, x: 870, y: 130 },
  { ab: "IL", name: "Illinois", loc: 501, x: 580, y: 240 },
  { ab: "NM", name: "New Mexico", loc: 485, x: 300, y: 360 },
  { ab: "VT", name: "Vermont", loc: 85, x: 850, y: 120 },
];

const TOTAL = RDOF.reduce((a, s) => a + s.loc, 0);
const MAX = Math.max(...RDOF.map((s) => s.loc));

function regionSum(abs: string[]) {
  return RDOF.filter((s) => abs.includes(s.ab)).reduce((a, s) => a + s.loc, 0);
}

const SE = regionSum(["NC", "SC", "TN", "AL", "GA", "FL", "VA", "KY"]);
const MW = regionSum(["WI", "OH", "IN", "MI", "MO", "IL"]);
const TX = regionSum(["TX"]);
const OTHER = TOTAL - SE - MW - TX;

/**
 * Miles from a representative rural point in each RDOF state to the nearest
 * Census MSA with 2020 population ≥250k (principal-city lat/lon as MSA
 * centroid proxy). Haversine, statute miles.
 *
 * Point choice: USGS/Census state geographic centroid for 22/24 states;
 * TX → Nacogdoches Co. (East Texas rural belt — geographic center sits in
 * West-Central empty land); OR → Roseburg / Douglas Co. (western foothills —
 * geographic center sits in High Desert). ESTIMATED distances; coordinates
 * RETRIEVED from public geographic centers / county seats / MSA principal cities.
 */
const METRO_DIST: Array<{
  ab: string;
  name: string;
  loc: number;
  metro: string;
  mi: number;
  point: string;
}> = [
  { ab: "WI", name: "Wisconsin", loc: 143269, metro: "Green Bay", mi: 80.9, point: "state centroid" },
  { ab: "TX", name: "Texas", loc: 133993, metro: "Shreveport-Bossier City", mi: 82.9, point: "Nacogdoches Co. (E. TX)" },
  { ab: "NC", name: "North Carolina", loc: 128502, metro: "Durham-Chapel Hill", mi: 40.9, point: "state centroid" },
  { ab: "OH", name: "Ohio", loc: 112777, metro: "Columbus", mi: 24.9, point: "state centroid" },
  { ab: "SC", name: "South Carolina", loc: 98670, metro: "Columbia", mi: 9.8, point: "state centroid" },
  { ab: "TN", name: "Tennessee", loc: 79193, metro: "Nashville", mi: 32.0, point: "state centroid" },
  { ab: "MO", name: "Missouri", loc: 61524, metro: "Springfield, MO", mi: 91.4, point: "state centroid" },
  { ab: "AL", name: "Alabama", loc: 56451, metro: "Montgomery", mi: 41.0, point: "state centroid" },
  { ab: "IN", name: "Indiana", loc: 54541, metro: "Indianapolis", mi: 10.9, point: "state centroid" },
  { ab: "MI", name: "Michigan", loc: 35944, metro: "Grand Rapids", mi: 96.4, point: "state centroid" },
  { ab: "KY", name: "Kentucky", loc: 31747, metro: "Louisville", mi: 55.5, point: "state centroid" },
  { ab: "LA", name: "Louisiana", loc: 25389, metro: "Lafayette", mi: 58.4, point: "state centroid" },
  { ab: "GA", name: "Georgia", loc: 23854, metro: "Atlanta", mi: 94.0, point: "state centroid" },
  { ab: "FL", name: "Florida", loc: 17869, metro: "Ocala", mi: 42.8, point: "state centroid" },
  { ab: "OR", name: "Oregon", loc: 15139, metro: "Eugene", mi: 59.1, point: "Roseburg / Douglas Co." },
  { ab: "MA", name: "Massachusetts", loc: 14344, metro: "Worcester", mi: 0.4, point: "state centroid" },
  { ab: "VA", name: "Virginia", loc: 11369, metro: "Lynchburg", mi: 17.5, point: "state centroid" },
  { ab: "PA", name: "Pennsylvania", loc: 5328, metro: "Harrisburg", mi: 63.6, point: "state centroid" },
  { ab: "WA", name: "Washington", loc: 4625, metro: "Yakima", mi: 54.0, point: "state centroid" },
  { ab: "CA", name: "California", loc: 1045, metro: "Fresno", mi: 35.5, point: "state centroid" },
  { ab: "NH", name: "New Hampshire", loc: 1044, metro: "Manchester-Nashua", mi: 47.7, point: "state centroid" },
  { ab: "IL", name: "Illinois", loc: 501, metro: "Peoria", mi: 49.6, point: "state centroid" },
  { ab: "NM", name: "New Mexico", loc: 485, metro: "Albuquerque", mi: 55.9, point: "state centroid" },
  { ab: "VT", name: "Vermont", loc: 85, metro: "Manchester-Nashua", mi: 95.8, point: "state centroid" },
];

const METRO_TOTAL = METRO_DIST.reduce((a, s) => a + s.loc, 0);
const WAVG_MI =
  METRO_DIST.reduce((a, s) => a + s.loc * s.mi, 0) / METRO_TOTAL;

function weightedMedianMi(rows: typeof METRO_DIST): number {
  const sorted = [...rows].sort((a, b) => a.mi - b.mi);
  let cum = 0;
  for (const r of sorted) {
    cum += r.loc;
    if (cum >= METRO_TOTAL / 2) return r.mi;
  }
  return sorted[sorted.length - 1].mi;
}

const WMED_MI = weightedMedianMi(METRO_DIST);

const BAND_LT25 = METRO_DIST.filter((s) => s.mi < 25).reduce((a, s) => a + s.loc, 0);
const BAND_25_50 = METRO_DIST.filter((s) => s.mi >= 25 && s.mi < 50).reduce(
  (a, s) => a + s.loc,
  0,
);
const BAND_50_100 = METRO_DIST.filter((s) => s.mi >= 50 && s.mi < 100).reduce(
  (a, s) => a + s.loc,
  0,
);
const BAND_100P = METRO_DIST.filter((s) => s.mi >= 100).reduce((a, s) => a + s.loc, 0);

const PCT_WITHIN_50 = (100 * (BAND_LT25 + BAND_25_50)) / METRO_TOTAL;
const PCT_100P = (100 * BAND_100P) / METRO_TOTAL;

const TOP_FAR = [...METRO_DIST].sort((a, b) => b.mi - a.mi).slice(0, 5);
const MIN_STATE = METRO_DIST.reduce((a, s) => (s.mi < a.mi ? s : a));
const MAX_STATE = METRO_DIST.reduce((a, s) => (s.mi > a.mi ? s : a));

function UsDensityMap() {
  const theme = useHostTheme();
  const w = 960;
  const h = 520;

  const rScale = (loc: number) => 6 + Math.sqrt(loc / MAX) * 42;

  return (
    <Stack gap={8}>
      <svg
        width="100%"
        viewBox={`0 0 ${w} ${h}`}
        style={{ display: "block", background: theme.fill.tertiary }}
      >
        {/* Rough US outline frame */}
        <rect
          x={40}
          y={40}
          width={880}
          height={440}
          fill="none"
          stroke={theme.stroke.secondary}
          strokeWidth={1}
          strokeDasharray="4 4"
        />
        <text x={48} y={32} fill={theme.text.tertiary} fontSize={11}>
          Contiguous U.S. — bubble size ∝ RDOF locations awarded to Charter
        </text>

        {/* Region bands (legend cues) */}
        <text x={500} y={500} fill={theme.text.tertiary} fontSize={10}>
          Southeast · Midwest · Texas dominate; West / Northeast mostly thin
        </text>

        {RDOF.map((s) => {
          const r = rScale(s.loc);
          const intensity = s.loc / MAX;
          const fill =
            intensity > 0.7
              ? theme.category.red
              : intensity > 0.35
                ? theme.category.orange
                : intensity > 0.1
                  ? theme.category.blue
                  : theme.category.gray;
          return (
            <g key={s.ab}>
              <circle
                cx={s.x}
                cy={s.y}
                r={r}
                fill={fill}
                opacity={0.75}
                stroke={theme.stroke.primary}
                strokeWidth={0.75}
              >
                <title>{`${s.name}: ${s.loc.toLocaleString()} RDOF locations (${((100 * s.loc) / TOTAL).toFixed(1)}%)`}</title>
              </circle>
              <text
                x={s.x}
                y={s.y + 4}
                textAnchor="middle"
                fill={theme.text.primary}
                fontSize={s.loc > 50000 ? 11 : 9}
                fontWeight={600}
              >
                {s.ab}
              </text>
            </g>
          );
        })}
      </svg>
      <Row gap={16} wrap>
        <Text size="small" tone="secondary">
          Red / orange = highest awarded density · Blue = mid · Gray = thin
        </Text>
        <Text size="small" tone="tertiary">
          Positions are schematic state centroids, not census-block pins
        </Text>
      </Row>
    </Stack>
  );
}

export default function ChtrRuralGeography() {
  const top10 = [...RDOF].sort((a, b) => b.loc - a.loc).slice(0, 10);

  return (
    <Stack gap={28}>
      <Stack gap={8}>
        <Row gap={8} wrap>
          <Pill tone="info">Rural geography</Pill>
          <Pill tone="warning">1.3M activated · national total only</Pill>
          <Pill>Map = FCC RDOF award proxy</Pill>
        </Row>
        <H1>Where the ~1.3M rural passings sit</H1>
        <Text tone="secondary">
          Charter reports ~1.3M subsidized rural passings activated since 2022
          as a national figure (target &gt;1.7M). It does not publish a state
          split of activations. The density map below uses FCC Auction 904
          locations awarded to CCO Holdings (Charter) — ~1.06M locations in 24
          states — the geographic backbone of the initiative, plus other
          state/municipal grants layered on top.
        </Text>
      </Stack>

      <Callout tone="warning" title="What this map is / is not">
        Is: best public state-level density for Charter’s rural program (RDOF
        Phase I). Is not: exact county pins of the 1.3M already lit, and not
        every non-RDOF ARPA/BEAD/state grant location. Activated passings can
        run ahead of or lag awarded locations by state as construction rolls.
      </Callout>

      <Grid columns={4} gap={12}>
        <Stat value="1.3M" label="Activated rural passings (YE2025)" tone="info" />
        <Stat value=">1.7M" label="Initiative target passings" />
        <Stat value="~1.06M" label="RDOF locations awarded (24 states)" tone="warning" />
        <Stat value="24" label="RDOF states (Charter PR / Spectrum)" />
      </Grid>

      <Divider />

      <Stack gap={8}>
        <H2>U.S. density map — Charter RDOF locations</H2>
        <UsDensityMap />
      </Stack>

      <Stack gap={8}>
        <H2>Regional concentration</H2>
        <Text>
          This is not “thin evenly across the Plains.” Awarded density clusters
          in the Southeast, industrial Midwest, Texas, and Wisconsin — largely
          adjacent to existing Spectrum footprint, matching management’s
          “states where we currently operate” language.
        </Text>
        <Grid columns={4} gap={12}>
          <Stat
            value={`${((100 * SE) / TOTAL).toFixed(0)}%`}
            label={`Southeast (~${(SE / 1000).toFixed(0)}k locs)`}
            tone="danger"
          />
          <Stat
            value={`${((100 * MW) / TOTAL).toFixed(0)}%`}
            label={`Midwest (~${(MW / 1000).toFixed(0)}k locs)`}
            tone="warning"
          />
          <Stat
            value={`${((100 * TX) / TOTAL).toFixed(0)}%`}
            label={`Texas alone (~${(TX / 1000).toFixed(0)}k locs)`}
            tone="info"
          />
          <Stat
            value={`${((100 * OTHER) / TOTAL).toFixed(0)}%`}
            label={`All other RDOF states`}
          />
        </Grid>
        <Text size="small" tone="tertiary">
          Southeast here = NC, SC, TN, AL, GA, FL, VA, KY. Midwest = WI, OH,
          IN, MI, MO, IL. Remainder includes MA, OR, WA, CA, PA, NH, NM, VT,
          etc.
        </Text>
      </Stack>

      <Stack gap={8}>
        <H2>Distance to nearest metro (award-weighted proxy)</H2>
        <Text>
          For each RDOF state, miles from a representative rural point to the
          nearest Census MSA with 2020 population ≥250k, then weight by FCC
          locations awarded. Not driveway-level; a state/award-weighted
          metro-adjacency proxy for the &quot;how far from metros&quot; question.
        </Text>
        <Grid columns={4} gap={12}>
          <Stat
            value={`${WAVG_MI.toFixed(0)} mi`}
            label="Location-weighted avg to nearest metro"
            tone="info"
          />
          <Stat
            value={`${WMED_MI.toFixed(0)} mi`}
            label="Location-weighted median"
          />
          <Stat
            value={`${PCT_WITHIN_50.toFixed(0)}%`}
            label="Share of locs within 50 mi"
            tone="success"
          />
          <Stat
            value={`${PCT_100P.toFixed(0)}%`}
            label="Share of locs beyond 100 mi"
            tone="warning"
          />
        </Grid>
        <Grid columns={2} gap={16}>
          <Stack gap={8}>
            <Text size="small" weight="semibold">
              Distance bands (% of Charter RDOF locations)
            </Text>
            <BarChart
              categories={["<25 mi", "25–50", "50–100", "100+"]}
              series={[
                {
                  name: "% of RDOF locations",
                  data: [
                    Math.round((100 * BAND_LT25) / METRO_TOTAL),
                    Math.round((100 * BAND_25_50) / METRO_TOTAL),
                    Math.round((100 * BAND_50_100) / METRO_TOTAL),
                    Math.round((100 * BAND_100P) / METRO_TOTAL),
                  ],
                  tone: "info",
                },
              ]}
              height={200}
              valueSuffix="%"
            />
            <Text size="small" tone="tertiary">
              Min {MIN_STATE.ab} {MIN_STATE.mi.toFixed(0)} mi · Max{" "}
              {MAX_STATE.ab} {MAX_STATE.mi.toFixed(0)} mi · Metro = MSA ≥250k
              pop (2020)
            </Text>
          </Stack>
          <Stack gap={8}>
            <Text size="small" weight="semibold">
              Top 5 longest-distance states
            </Text>
            <Table
              headers={["State", "Mi", "Nearest metro ≥250k", "RDOF locs"]}
              columnAlign={["left", "right", "left", "right"]}
              rows={TOP_FAR.map((s) => [
                s.ab,
                s.mi.toFixed(0),
                s.metro,
                s.loc.toLocaleString(),
              ])}
              striped
            />
          </Stack>
        </Grid>
        <Callout tone="warning" title="Method tags · ESTIMATED distances">
          RETRIEVED: FCC Auction 904 location counts by state; MSA ≥250k filter
          (2020 CBSA pop); public lat/lon for state geographic centers, two
          rural-county overrides (TX Nacogdoches, OR Roseburg), and MSA
          principal cities. ESTIMATED: haversine miles from that one point per
          state to nearest metro centroid — not census-block-to-MSA. Zero share
          beyond 100 mi is under this definition; block-level pins would widen
          the right tail inside large states (esp. WI / TX / MI).
        </Callout>
        <Table
          headers={[
            "State",
            "RDOF locs",
            "Nearest metro (≥250k)",
            "Distance (mi)",
            "Rural point used",
          ]}
          columnAlign={["left", "right", "left", "right", "left"]}
          rows={[...METRO_DIST]
            .sort((a, b) => b.loc - a.loc)
            .map((s) => [
              `${s.name} (${s.ab})`,
              s.loc.toLocaleString(),
              s.metro,
              s.mi.toFixed(1),
              s.point,
            ])}
          striped
        />
        <Text size="small" tone="secondary">
          Implication: under this proxy, Charter’s RDOF mass sits metro-adjacent
          (~{WAVG_MI.toFixed(0)} mi weighted avg; {PCT_WITHIN_50.toFixed(0)}%
          within 50 mi; none of the award weight beyond 100 mi) — consistent with
          adjacency / existing-plant buildout, not deep remote rural.
        </Text>
      </Stack>

      <Stack gap={8}>
        <H2>Top 10 states by RDOF locations awarded</H2>
        <Table
          headers={["Rank", "State", "Locations", "% of Charter RDOF", "Read"]}
          columnAlign={["right", "left", "right", "right", "left"]}
          rowTone={[
            "danger",
            "danger",
            "danger",
            "warning",
            "warning",
            "warning",
            undefined,
            undefined,
            undefined,
            undefined,
          ]}
          rows={top10.map((s, i) => [
            String(i + 1),
            `${s.name} (${s.ab})`,
            s.loc.toLocaleString(),
            `${((100 * s.loc) / TOTAL).toFixed(1)}%`,
            i < 5 ? "Core density" : "Material",
          ])}
          striped
        />
        <Text size="small" tone="tertiary">
          Top 5 (WI, TX, NC, OH, SC) ≈ 58% of Charter’s RDOF locations.
        </Text>
      </Stack>

      <Stack gap={8}>
        <H2>Full 24-state award table</H2>
        <Table
          headers={["State", "RDOF locations", "Share"]}
          columnAlign={["left", "right", "right"]}
          rows={[...RDOF]
            .sort((a, b) => b.loc - a.loc)
            .map((s) => [
              `${s.name} (${s.ab})`,
              s.loc.toLocaleString(),
              `${((100 * s.loc) / TOTAL).toFixed(1)}%`,
            ])}
          striped
        />
      </Stack>

      <Stack gap={8}>
        <H2>How this relates to the 1.3M activated</H2>
        <Table
          headers={["Metric", "Figure", "Source"]}
          columnAlign={["left", "left", "left"]}
          rows={[
            [
              "Activated subsidized rural passings",
              "~1.3M since early 2022 (YE2025)",
              "CHTR FY2025 10-K",
            ],
            [
              "Initiative target",
              ">1.7M passings; >$8B spend; >$2B grants",
              "CHTR FY2025 10-K",
            ],
            [
              "RDOF Phase I to Charter",
              "~1.06M locations · ~$1.22B / 10 yrs · 24 states",
              "FCC Auction 904 / Charter Feb 2021 PR",
            ],
            [
              "Other grants",
              "State/ARPA/BEAD etc. on top of RDOF",
              "10-K government assistance note",
            ],
            [
              "Geographic pattern",
              "SE + Midwest + TX/WI heavy; West/NE thin",
              "FCC state award table",
            ],
          ]}
          striped
        />
      </Stack>

      <Callout tone="info" title="Implication">
        Rural for Charter is geographically a Southeast–Midwest–Texas build
        adjacent to existing Spectrum plant — not a nationwide Starlink-style
        coverage layer. That supports the adjacency / scale thesis and
        concentrates Starlink/FWA competitive risk in those same rural
        counties, not uniformly across the U.S. map.
      </Callout>

      <Text size="small" tone="tertiary">
        Sources: CHTR FY2025 10-K (1.3M activated; map referenced but not
        digitized here) · FCC Auction 904 winning bidder summary (CCO Holdings
        by state) · Charter IR PR 1 Feb 2021 (24-state list) · Census 2020 CBSA
        pop ≥250k + public principal-city / state-centroid coordinates
        (metro-distance proxy). Analysis canvas.
      </Text>
    </Stack>
  );
}
