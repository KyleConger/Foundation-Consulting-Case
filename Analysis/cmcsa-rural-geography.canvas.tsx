/**
 * Geographic overview of Comcast rural / subsidized expansion footprint.
 * Closest rural figure: ~1/4 of ~1.3M FY2025 new homes/businesses passed ≈ ~0.3M
 * (national estimate only; CMCSA 10-K does not publish activated rural passings).
 * Comcast did not bid FCC Auction 904 (RDOF). State density uses BEAD provisional
 * award locations where published (Telecompetitor / state lists) as the best public
 * geographic proxy — incomplete vs company claim of ~34 BEAD states.
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

/**
 * Comcast BEAD provisional locations by state (disclosed counts only).
 * Source: Telecompetitor Benefit-of-the-Bargain provisional award roundup
 * (updated Dec 2025) + VA location count from Telecompetitor VA rankings.
 * Dollar-only award states are listed in the full table, not plotted here.
 */
const BEAD: Array<{
  ab: string;
  name: string;
  loc: number;
  x: number;
  y: number;
}> = [
  { ab: "FL", name: "Florida", loc: 35772, x: 740, y: 460 },
  { ab: "VA", name: "Virginia", loc: 24343, x: 780, y: 260 },
  { ab: "PA", name: "Pennsylvania", loc: 20835, x: 780, y: 200 },
  { ab: "AZ", name: "Arizona", loc: 13495, x: 220, y: 380 },
  { ab: "IL", name: "Illinois", loc: 13023, x: 580, y: 240 },
  { ab: "MS", name: "Mississippi", loc: 10809, x: 580, y: 400 },
  { ab: "LA", name: "Louisiana", loc: 6561, x: 540, y: 420 },
  { ab: "KY", name: "Kentucky", loc: 5777, x: 660, y: 280 },
  { ab: "AR", name: "Arkansas", loc: 3242, x: 540, y: 360 },
  { ab: "NM", name: "New Mexico", loc: 2760, x: 300, y: 360 },
  { ab: "MN", name: "Minnesota", loc: 2760, x: 520, y: 120 },
  { ab: "UT", name: "Utah", loc: 1787, x: 240, y: 260 },
  { ab: "MO", name: "Missouri", loc: 1357, x: 520, y: 280 },
  { ab: "CO", name: "Colorado", loc: 1047, x: 300, y: 280 },
  { ab: "OH", name: "Ohio", loc: 835, x: 680, y: 220 },
  { ab: "NH", name: "New Hampshire", loc: 573, x: 870, y: 130 },
  { ab: "NY", name: "New York", loc: 390, x: 820, y: 160 },
  { ab: "ME", name: "Maine", loc: 71, x: 900, y: 100 },
];

/** Dollar-only provisional awards (locations not published in source roundup). */
const BEAD_DOLLAR_ONLY: Array<{ ab: string; name: string; awardM: number }> = [
  { ab: "CA", name: "California", awardM: 399.7 },
  { ab: "AL", name: "Alabama", awardM: 157.2 },
  { ab: "OR", name: "Oregon", awardM: 107.8 },
  { ab: "WV", name: "West Virginia", awardM: 61.3 },
  { ab: "MD", name: "Maryland", awardM: 50.2 },
  { ab: "NJ", name: "New Jersey", awardM: 50.1 },
  { ab: "TN", name: "Tennessee", awardM: 38.3 },
  { ab: "MI", name: "Michigan", awardM: 29.3 },
  { ab: "GA", name: "Georgia", awardM: 20.2 },
  { ab: "WA", name: "Washington", awardM: 14.5 },
  { ab: "IN", name: "Indiana", awardM: 14.2 },
  { ab: "MA", name: "Massachusetts", awardM: 11.4 },
  { ab: "SC", name: "South Carolina", awardM: 3.6 },
  { ab: "DE", name: "Delaware", awardM: 3.8 },
  { ab: "VT", name: "Vermont", awardM: 3.3 },
  { ab: "CT", name: "Connecticut", awardM: 0.6 },
  { ab: "WI", name: "Wisconsin", awardM: 5.9 },
];

const TOTAL = BEAD.reduce((a, s) => a + s.loc, 0);
const MAX = Math.max(...BEAD.map((s) => s.loc));
const N_BEAD_STATES = BEAD.length + BEAD_DOLLAR_ONLY.length;

function regionSum(abs: string[]) {
  return BEAD.filter((s) => abs.includes(s.ab)).reduce((a, s) => a + s.loc, 0);
}

/** Same conceptual bands as CHTR canvas; TX empty for Comcast disclosed BEAD locs. */
const SE = regionSum(["FL", "KY", "LA", "MS", "VA", "AR"]);
const MW = regionSum(["IL", "MN", "MO", "OH"]);
const TX = regionSum(["TX"]);
const OTHER = TOTAL - SE - MW - TX;

/**
 * Miles from a representative rural point in each disclosed-location BEAD
 * state to the nearest Census MSA with 2020 population ≥250k (principal-city
 * lat/lon as MSA centroid proxy). Haversine, statute miles.
 *
 * Point choice: USGS/Census state geographic centroid for all 18 states with
 * published location counts. Dollar-only BEAD award states are excluded from
 * the weighted average (no location weights). ESTIMATED distances; coordinates
 * RETRIEVED from public geographic centers / MSA principal cities. Overlapping
 * CHTR-state centroids reuse the same coords so distances match that canvas.
 */
const METRO_DIST: Array<{
  ab: string;
  name: string;
  loc: number;
  metro: string;
  mi: number;
  point: string;
}> = [
  { ab: "FL", name: "Florida", loc: 35772, metro: "Ocala", mi: 42.8, point: "state centroid" },
  { ab: "VA", name: "Virginia", loc: 24343, metro: "Lynchburg", mi: 17.5, point: "state centroid" },
  { ab: "PA", name: "Pennsylvania", loc: 20835, metro: "Harrisburg", mi: 63.6, point: "state centroid" },
  { ab: "AZ", name: "Arizona", loc: 13495, metro: "Phoenix", mi: 61.8, point: "state centroid" },
  { ab: "IL", name: "Illinois", loc: 13023, metro: "Peoria", mi: 49.6, point: "state centroid" },
  { ab: "MS", name: "Mississippi", loc: 10809, metro: "Jackson", mi: 42.7, point: "state centroid" },
  { ab: "LA", name: "Louisiana", loc: 6561, metro: "Lafayette", mi: 58.4, point: "state centroid" },
  { ab: "KY", name: "Kentucky", loc: 5777, metro: "Louisville", mi: 55.5, point: "state centroid" },
  { ab: "AR", name: "Arkansas", loc: 3242, metro: "Little Rock", mi: 13.4, point: "state centroid" },
  { ab: "NM", name: "New Mexico", loc: 2760, metro: "Albuquerque", mi: 55.9, point: "state centroid" },
  { ab: "MN", name: "Minnesota", loc: 2760, metro: "Minneapolis", mi: 103.1, point: "state centroid" },
  { ab: "UT", name: "Utah", loc: 1787, metro: "Provo", mi: 64.1, point: "state centroid" },
  { ab: "MO", name: "Missouri", loc: 1357, metro: "Springfield, MO", mi: 91.4, point: "state centroid" },
  { ab: "CO", name: "Colorado", loc: 1047, metro: "Colorado Springs", mi: 40.6, point: "state centroid" },
  { ab: "OH", name: "Ohio", loc: 835, metro: "Columbus", mi: 24.9, point: "state centroid" },
  { ab: "NH", name: "New Hampshire", loc: 573, metro: "Manchester-Nashua", mi: 47.7, point: "state centroid" },
  { ab: "NY", name: "New York", loc: 390, metro: "Syracuse", mi: 32.0, point: "state centroid" },
  { ab: "ME", name: "Maine", loc: 71, metro: "Portland ME", mi: 128.3, point: "state centroid" },
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
          Contiguous U.S. — bubble size ∝ BEAD locations (disclosed counts only)
        </text>

        <text x={420} y={500} fill={theme.text.tertiary} fontSize={10}>
          FL · VA · PA lead disclosed locs; CA/AL/OR large $ awards omitted (no loc count)
        </text>

        {BEAD.map((s) => {
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
                <title>{`${s.name}: ${s.loc.toLocaleString()} BEAD locations (${((100 * s.loc) / TOTAL).toFixed(1)}% of disclosed)`}</title>
              </circle>
              <text
                x={s.x}
                y={s.y + 4}
                textAnchor="middle"
                fill={theme.text.primary}
                fontSize={s.loc > 10000 ? 11 : 9}
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
          Red / orange = highest disclosed density · Blue = mid · Gray = thin
        </Text>
        <Text size="small" tone="tertiary">
          Positions are schematic state centroids, not census-block pins
        </Text>
      </Row>
    </Stack>
  );
}

export default function CmcsaRuralGeography() {
  const top10 = [...BEAD].sort((a, b) => b.loc - a.loc).slice(0, 10);
  const top5Share = top10
    .slice(0, 5)
    .reduce((a, s) => a + s.loc, 0);

  const fullRows = [
    ...[...BEAD]
      .sort((a, b) => b.loc - a.loc)
      .map((s) => [
        `${s.name} (${s.ab})`,
        s.loc.toLocaleString(),
        `${((100 * s.loc) / TOTAL).toFixed(1)}%`,
      ]),
    ...[...BEAD_DOLLAR_ONLY]
      .sort((a, b) => b.awardM - a.awardM)
      .map((s) => [
        `${s.name} (${s.ab})`,
        `n/a · $${s.awardM.toFixed(1)}M award`,
        "—",
      ]),
  ];

  return (
    <Stack gap={28}>
      <Stack gap={8}>
        <Row gap={8} wrap>
          <Pill tone="info">Rural geography</Pill>
          <Pill tone="warning">~0.3M rural share · national estimate only</Pill>
          <Pill>Map = BEAD award proxy (not RDOF)</Pill>
        </Row>
        <H1>Where Comcast&apos;s rural expansion sits</H1>
        <Text tone="secondary">
          Comcast does not publish a Charter-style “activated subsidized rural
          passings” total. Closest disclosed figures: domestic homes and
          businesses passed rose ~1.3M to ~65.0M in FY2025 (10-K), and Comcast
          corporate materials state that about one quarter of ~1.25M 2025 new
          passings were in rural communities (~0.3M). It did not participate in
          FCC Auction 904 (RDOF). The density map below uses BEAD provisional
          award locations where states published counts — ~145k locations in 18
          states — as the best public geographic proxy; 17 further states have
          dollar awards without published location counts.
        </Text>
      </Stack>

      <Callout tone="warning" title="What this map is / is not">
        Is: best public state-level density for Comcast’s subsidized rural /
        unserved build using BEAD provisional awards with disclosed location
        counts. Is not: RDOF (Comcast did not bid), not exact pins of the ~0.3M
        estimated rural share of 2025 passings, and not a complete 34–35-state
        BEAD location file — California, Alabama, Oregon, West Virginia and
        others have large dollar awards omitted from bubbles because location
        counts were not published in the source roundup. Activated / edged-out
        passings can lead or lag awards by state.
      </Callout>

      <Grid columns={4} gap={12}>
        <Stat
          value="~0.3M"
          label="Est. rural share of 2025 new passings"
          tone="info"
        />
        <Stat value="~1.3M" label="Total new homes/biz passed (FY2025)" />
        <Stat
          value="$0"
          label="RDOF Auction 904 (did not bid)"
          tone="warning"
        />
        <Stat
          value={String(N_BEAD_STATES)}
          label="BEAD provisional award states"
        />
      </Grid>

      <Divider />

      <Stack gap={8}>
        <H2>U.S. density map — Comcast BEAD locations (disclosed)</H2>
        <UsDensityMap />
      </Stack>

      <Stack gap={8}>
        <H2>Regional concentration</H2>
        <Text>
          On disclosed BEAD location counts, density clusters in Florida, the
          Mid-Atlantic (VA/PA), Illinois, and the Deep South — not a Texas-heavy
          RDOF pattern like Charter. Texas has no Comcast row in the provisional
          location table used here. Large West Coast dollar awards (especially
          California) are missing from these shares until location counts are
          published.
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
            label={`All other disclosed BEAD states`}
          />
        </Grid>
        <Text size="small" tone="tertiary">
          Southeast here = FL, KY, LA, MS, VA, AR (same South / Mid-South
          priority as the Charter canvas; NC/SC/TN/AL/GA lack disclosed Comcast
          location counts in the source). Midwest = IL, MN, MO, OH. Texas = none
          in this disclosed set. Remainder includes AZ, PA, NM, UT, CO, NH, NY,
          ME.
        </Text>
      </Stack>

      <Stack gap={8}>
        <H2>Distance to nearest metro (award-weighted proxy)</H2>
        <Text>
          For each disclosed-location BEAD state, miles from a representative
          rural point to the nearest Census MSA with 2020 population ≥250k,
          then weight by published BEAD locations. Not driveway-level; a
          state/award-weighted metro-adjacency proxy for the &quot;how far from
          metros&quot; question. Same method as the Charter RDOF canvas.
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
              Distance bands (% of disclosed Comcast BEAD locations)
            </Text>
            <BarChart
              categories={["<25 mi", "25–50", "50–100", "100+"]}
              series={[
                {
                  name: "% of BEAD locations",
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
              headers={["State", "Mi", "Nearest metro ≥250k", "BEAD locs"]}
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
          RETRIEVED: Telecompetitor BEAD provisional location counts (18
          states); MSA ≥250k filter (2020 CBSA pop); public lat/lon for state
          geographic centers and MSA principal cities. ESTIMATED: haversine
          miles from that one point per state to nearest metro centroid — not
          census-block-to-MSA. Excluded from the weighted average:{" "}
          {BEAD_DOLLAR_ONLY.length} dollar-only BEAD states (CA, AL, OR, WV,
          and 13 others) with no published location counts — adding them would
          change the average only if their (unknown) loc mass differs from the
          disclosed pattern.
        </Callout>
        <Table
          headers={[
            "State",
            "BEAD locs",
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
          Implication: under this proxy, Comcast’s disclosed BEAD mass is also
          metro-adjacent (~{WAVG_MI.toFixed(0)} mi weighted avg vs Charter RDOF
          ~51 mi; {PCT_WITHIN_50.toFixed(0)}% within 50 mi) — slightly closer on
          average than Charter, with a thin right tail (MN + ME ≈{" "}
          {PCT_100P.toFixed(0)}% of locs beyond 100 mi). Incomplete until CA and
          other $-only states publish location counts.
        </Text>
      </Stack>

      <Stack gap={8}>
        <H2>Top 10 states by BEAD locations (disclosed)</H2>
        <Table
          headers={["Rank", "State", "Locations", "% of disclosed Comcast BEAD", "Read"]}
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
          Top 5 (FL, VA, PA, AZ, IL) ≈ {((100 * top5Share) / TOTAL).toFixed(0)}%
          of Comcast’s disclosed BEAD locations (~{TOTAL.toLocaleString()}{" "}
          locs / 18 states).
        </Text>
      </Stack>

      <Stack gap={8}>
        <H2>Full BEAD award table (locations + dollar-only states)</H2>
        <Table
          headers={["State", "BEAD locations / note", "Share of disclosed"]}
          columnAlign={["left", "right", "right"]}
          rows={fullRows}
          striped
        />
        <Text size="small" tone="tertiary">
          Dollar-only rows are provisional award amounts from the same roundup;
          they are excluded from shares and the bubble map so percentages are
          not invented.
        </Text>
      </Stack>

      <Stack gap={8}>
        <H2>How this relates to the ~0.3M rural share</H2>
        <Table
          headers={["Metric", "Figure", "Source"]}
          columnAlign={["left", "left", "left"]}
          rows={[
            [
              "Est. rural share of new passings",
              "~0.3M (≈1/4 of ~1.25–1.3M 2025 new passings)",
              "Comcast corporate BEAD note · applied to FY2025 passings growth",
            ],
            [
              "Total new homes/businesses passed",
              "~1.3M to ~65.0M domestic (FY2025)",
              "CMCSA FY2025 10-K",
            ],
            [
              "Rural / unserved initiative target",
              "No Charter-style >1.7M rural passings target disclosed",
              "CMCSA 10-K (edge-out + subsidies, no rural KPI)",
            ],
            [
              "RDOF Phase I to Comcast",
              "$0 · did not participate (few adjacent rural areas vs regulatory cost)",
              "Q2 2020 earnings call (Watson) · Lightwave / FCC Auction 904 results",
            ],
            [
              "BEAD provisional awards",
              `~${TOTAL.toLocaleString()} disclosed locs / 18 states; ${N_BEAD_STATES} states with $ awards; company cites ~34`,
              "Telecompetitor provisional lists · Comcast corporate",
            ],
            [
              "Other grants (examples)",
              "FL rural PPP ~64k by YE2026; IN Next Level ~10k+; CA/VA ARPA/VATI projects",
              "Comcast / state PRs (layered on BEAD; not in map)",
            ],
            [
              "Geographic pattern",
              "FL + Mid-Atlantic + IL/Deep South on disclosed locs; TX empty; CA $ large but loc n/a",
              "BEAD provisional location table",
            ],
          ]}
          striped
        />
      </Stack>

      <Callout tone="info" title="Implication">
        Rural for Comcast is not an RDOF adjacency build like Charter’s
        Southeast–Midwest–Texas Spectrum plant extension. Comcast sat out Auction
        904 and is instead stacking BEAD and state/ARPA partnerships across a
        broader footprint, with disclosed location density heaviest in Florida
        and the Mid-Atlantic. That weakens any one-to-one “same rural counties”
        CHTR–CMCSA comparison and shifts Starlink/FWA rural risk mapping to
        BEAD/state-grant geographies — incomplete until California and other
        dollar-only states publish location counts.
      </Callout>

      <Text size="small" tone="tertiary">
        Sources: CMCSA FY2025 10-K (homes/businesses passed +1.3M to ~65.0M) ·
        Comcast corporate “Delivering on BEAD’s Promise” (~1.25M new passings;
        ~1/4 rural; ~34 BEAD states) · Telecompetitor BEAD Benefit-of-the-Bargain
        provisional awards by state (location counts where published; VA locs
        from Telecompetitor VA rankings) · Lightwave / FCC Auction 904 (Comcast
        did not bid; Watson Q2 2020) · state/Comcast PRs for FL/IN examples ·
        Census 2020 CBSA pop ≥250k + public principal-city / state-centroid
        coordinates (metro-distance proxy; disclosed-loc states only). Analysis
        canvas.
      </Text>
    </Stack>
  );
}
