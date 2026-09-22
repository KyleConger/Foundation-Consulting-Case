/**
 * Work-from-home / telework rates for the Charter–Spectrum benefits-analogy case.
 * Descriptive rates only — no TAM, no recommendation, no kill rule.
 *
 * Arithmetic: Analysis/work-from-home/build_wfh_rates.py
 * Must match Analysis/work-from-home/out/*.csv
 *
 * Metrics are NOT interchangeable:
 *   ACS  = usually worked from home (journey-to-work), workers 16+
 *   ATUS = any work at home on days worked, employed 15+
 *   ABS  = share of firms that had any employees who worked from home
 */
import {
  BarChart,
  Callout,
  Card,
  CardBody,
  Divider,
  Grid,
  H1,
  H2,
  Link,
  Pill,
  Row,
  Stack,
  Stat,
  Table,
  Text,
} from "cursor/canvas";

/** RETRIEVED — ACS 2024 1-year B08301 via Census Reporter (acs2024_1yr). */
const ACS_US_RATE = 13.3;
const ACS_US_WORKERS = 165_360_450;
const ACS_US_WFH = 22_026_372;
const ACS_HIGH_NAME = "D.C.";
const ACS_HIGH_RATE = 22.9;
const ACS_HIGH_WORKERS = 388_136;
const ACS_LOW_NAME = "Mississippi";
const ACS_LOW_RATE = 6.2;
const ACS_LOW_WORKERS = 1_302_251;
const ACS_SPREAD_PP = 16.6;

/** Chart subset: five highest + five lowest ACS usually-WFH states (sorted by story). */
const STATE_CHART_CATS = [
  "D.C.",
  "Colorado",
  "Oregon",
  "Washington",
  "Arizona",
  "Alabama",
  "South Dakota",
  "Louisiana",
  "North Dakota",
  "Mississippi",
];
const STATE_CHART_HIGH = [22.9, 19.9, 17.1, 16.4, 16.3, 0, 0, 0, 0, 0];
const STATE_CHART_LOW = [0, 0, 0, 0, 0, 8.3, 8.0, 8.0, 7.1, 6.2];

/** RETRIEVED — BLS ATUS 2024 Tables 6–7 (news release). Seniority proxies only. */
const ATUS_OVERALL = 32.5;
const ATUS_MGMT = 48.1;
const ATUS_SERVICE = 10.5;
const ATUS_TOP_EARN = 51.0;
const ATUS_BOT_EARN = 13.3;
const ATUS_BACH = 50.0;
const ATUS_HS = 17.8;
const ATUS_FT = 33.4;
const ATUS_PT = 27.9;

const PROXY_CATS = [
  "Mgmt / business / finance",
  "Professional & related",
  "Top earnings quartile",
  "Bachelor's+",
  "ATUS overall",
  "HS, no college",
  "Bottom earnings quartile",
  "Service occupations",
];
const PROXY_FOCAL = [48.1, 0, 51.0, 0, 0, 0, 0, 0];
const PROXY_REST = [0, 46.5, 0, 50.0, 32.5, 17.8, 13.3, 10.5];

/** RETRIEVED — Census ABS ABSCB2023.AB2300CSCB04 B28 WORKHOME, EMPSZFI 655 vs 657. */
const ABS_LT500 = 35.8;
const ABS_GE500 = 77.5;

const CITE_ACS =
  "Source: U.S. Census Bureau, American Community Survey (ACS) 1-Year Estimates Detailed Tables, 2024 — table B08301 Means of Transportation to Work; universe Workers 16 years and over; variable B08301_021E “Worked from home” ÷ B08301_001E Total (usually worked from home as journey-to-work means). Retrieved via Census Reporter API release acs2024_1yr. URL used: https://api.censusreporter.org/1.0/data/show/latest?table_ids=B08301&geo_ids=040|01000US,01000US · Also: https://data.census.gov/table/ACSDT1Y2024.B08301 · Funded by: U.S. Census Bureau (federal statistical agency).";

const CITE_ATUS =
  "Source: U.S. Bureau of Labor Statistics, American Time Use Survey (ATUS), 2024 annual averages — Tables 6 and 7 in the June 26, 2025 news release. Measure: employed persons who worked at home on an average day as % of employed persons who worked on an average day; “working at home” includes any time at home (not only usual workplace = home); persons 15+. URL used: https://www.bls.gov/news.release/archives/atus_06262025.htm · PDF: https://www.bls.gov/news.release/archives/atus_06262025.pdf · Funded by: U.S. BLS (federal statistical agency). Different metric than ACS — do not mix in one comparison.";

const CITE_ABS =
  "Source: U.S. Census Bureau, Annual Business Survey (ABS) Characteristics of Businesses — table ABSCB2023.AB2300CSCB04 (employment size of firm); QDESC=B28 WORKHOME; BUSCHAR=EWA “Business had employees who worked from home” as % of EWTR total reporting (FIRMPDEMP_PCT); EMPSZFI 655 = firms with <500 employees, 657 = firms with 500+; file YEAR=2023. Firm-level (had any WFH employees), not a worker WFH rate. URL used: https://www2.census.gov/programs-surveys/abs/data/2023/AB2300CSCB04.zip · Table notes: https://data.census.gov/table/ABSCB2023.AB2300CSCB04 · Funded by: U.S. Census Bureau (federal statistical agency).";

/** Full state table — ACS 2024 usually-WFH; one decimal; sorted high→low. From CSV. */
const STATE_ROWS: (string | number)[][] = [
  ["1", "District of Columbia", "22.9%", "388,136", "88,726"],
  ["2", "Colorado", "19.9%", "3,167,362", "629,420"],
  ["3", "Oregon", "17.1%", "2,080,165", "354,930"],
  ["4", "Washington", "16.4%", "3,932,815", "645,514"],
  ["5", "Arizona", "16.3%", "3,571,875", "582,289"],
  ["6", "New Hampshire", "16.0%", "754,095", "120,950"],
  ["7", "Vermont", "16.0%", "340,565", "54,357"],
  ["8", "Virginia", "15.8%", "4,445,265", "703,153"],
  ["9", "Utah", "15.7%", "1,771,258", "277,963"],
  ["10", "Maryland", "15.6%", "3,227,926", "504,513"],
  ["11", "Florida", "15.5%", "11,086,922", "1,721,372"],
  ["12", "North Carolina", "15.4%", "5,375,927", "828,181"],
  ["13", "Georgia", "14.9%", "5,402,123", "803,593"],
  ["14", "Massachusetts", "14.8%", "3,752,433", "556,682"],
  ["15", "Minnesota", "14.7%", "3,009,002", "443,318"],
  ["16", "Maine", "14.7%", "702,479", "103,070"],
  ["17", "California", "14.1%", "18,893,770", "2,672,106"],
  ["18", "Pennsylvania", "13.8%", "6,390,587", "883,654"],
  ["19", "Illinois", "13.6%", "6,314,165", "857,301"],
  ["20", "New Jersey", "13.5%", "4,772,330", "644,549"],
  ["21", "Connecticut", "13.4%", "1,874,388", "250,606"],
  ["22", "Texas", "12.9%", "15,130,603", "1,956,349"],
  ["23", "Delaware", "12.9%", "500,340", "64,492"],
  ["24", "Idaho", "12.7%", "952,044", "120,976"],
  ["25", "Tennessee", "12.7%", "3,479,795", "441,140"],
  ["26", "South Carolina", "12.3%", "2,571,377", "316,801"],
  ["27", "Ohio", "11.9%", "5,765,669", "687,025"],
  ["28", "Wisconsin", "11.8%", "3,050,562", "360,127"],
  ["29", "Missouri", "11.8%", "3,054,047", "360,070"],
  ["30", "New York", "11.8%", "9,557,920", "1,124,869"],
  ["31", "Montana", "11.7%", "565,069", "66,029"],
  ["32", "Rhode Island", "11.6%", "565,855", "65,520"],
  ["33", "Nevada", "11.3%", "1,581,033", "179,164"],
  ["34", "Michigan", "11.2%", "4,800,270", "539,125"],
  ["35", "Kansas", "10.3%", "1,494,667", "153,539"],
  ["36", "New Mexico", "10.3%", "954,026", "97,946"],
  ["37", "Iowa", "9.9%", "1,649,748", "162,777"],
  ["38", "Nebraska", "9.7%", "1,036,126", "100,914"],
  ["39", "Wyoming", "9.7%", "294,920", "28,679"],
  ["40", "Indiana", "9.6%", "3,355,446", "323,341"],
  ["41", "Kentucky", "9.5%", "2,078,668", "197,124"],
  ["42", "Oklahoma", "8.9%", "1,876,156", "167,486"],
  ["43", "Hawaii", "8.9%", "716,578", "63,594"],
  ["44", "West Virginia", "8.8%", "759,466", "66,915"],
  ["45", "Arkansas", "8.6%", "1,386,650", "119,058"],
  ["46", "Alaska", "8.4%", "361,983", "30,477"],
  ["47", "Alabama", "8.3%", "2,323,881", "193,754"],
  ["48", "South Dakota", "8.0%", "475,913", "38,257"],
  ["49", "Louisiana", "8.0%", "2,043,342", "163,353"],
  ["50", "North Dakota", "7.1%", "422,457", "29,953"],
  ["51", "Mississippi", "6.2%", "1,302,251", "81,270"],
];

function Cite({ text }: { text: string }) {
  return (
    <Text size="small" tone="tertiary">
      {text}
    </Text>
  );
}

export default function ChtrWorkFromHomeRates() {
  return (
    <Stack gap={28} style={{ maxWidth: 1040, margin: "0 auto", padding: "28px 20px 48px" }}>
      <Stack gap={10}>
        <Row gap={8} align="center" wrap>
          <Pill active>Descriptive rates</Pill>
          <Pill tone="neutral">Not a sizing</Pill>
          <Pill tone="neutral">RETRIEVED only</Pill>
        </Row>
        <H1>
          Usually-WFH spans 16.6 points across states — D.C. 22.9% vs Mississippi 6.2%
        </H1>
        <Text tone="secondary">
          Denominator for the headline and state table: workers 16+ whose usual means of
          transportation to work was “worked from home” (ACS journey-to-work). Seniority and
          firm-size exhibits use different official surveys and say so on the exhibit. One decimal
          on charts; full precision in{" "}
          <Text weight="semibold">Analysis/work-from-home/out/</Text>.
        </Text>
      </Stack>

      <Callout tone="info" title="What this changes for the benefits analogy">
        The corporate → consumer Internet analogy only lands a Spectrum residential account if the
        employee actually works from home. These rates show that “home as workplace” is concentrated
        — by state, by occupation/earnings (seniority proxies), and at large firms — so any
        employer-provisioned home broadband motion is not a uniform share of all workers.
      </Callout>

      {/* US headline */}
      <Stack gap={10}>
        <H2>United States — usually worked from home</H2>
        <Grid columns={3} gap={12}>
          <Stat value={`${ACS_US_RATE}%`} label="US usually-WFH rate" tone="info" />
          <Stat value={`${(ACS_US_WORKERS / 1e6).toFixed(1)}M`} label="Workers 16+ (denominator)" />
          <Stat value={`${(ACS_US_WFH / 1e6).toFixed(1)}M`} label="Usually worked from home" />
        </Grid>
        <Cite text={CITE_ACS} />
      </Stack>

      <Divider />

      {/* State spread chart */}
      <Stack gap={10}>
        <H2>
          Highest usually-WFH states sit near 17–23%; lowest cluster at 6–8%
        </H2>
        <Text size="small" tone="secondary">
          Chart shows five highest and five lowest states only. Full 51-row table (50 states + D.C.)
          below. Sorted by rate, not alphabetically. Bars start at zero.
        </Text>
        <BarChart
          horizontal
          categories={STATE_CHART_CATS}
          series={[
            { name: "Highest five (ACS usually-WFH %)", data: STATE_CHART_HIGH, tone: "info" },
            { name: "Lowest five (ACS usually-WFH %)", data: STATE_CHART_LOW, tone: "neutral" },
          ]}
          beginAtZero
          valueSuffix="%"
          height={320}
        />
        <Row gap={16} wrap>
          <Text size="small">
            High: {ACS_HIGH_NAME} {ACS_HIGH_RATE}% (n={ACS_HIGH_WORKERS.toLocaleString()} workers 16+)
          </Text>
          <Text size="small">
            Low: {ACS_LOW_NAME} {ACS_LOW_RATE}% (n={ACS_LOW_WORKERS.toLocaleString()} workers 16+)
          </Text>
          <Text size="small">Spread: {ACS_SPREAD_PP} percentage points</Text>
        </Row>
        <Cite text={CITE_ACS} />
      </Stack>

      {/* Full state table */}
      <Stack gap={10}>
        <H2>All states + D.C. — ACS usually-WFH (2024)</H2>
        <Table
          headers={["Rank", "State", "Usually WFH %", "Workers 16+", "Worked from home"]}
          rows={STATE_ROWS}
          rowTone={STATE_ROWS.map((_, i) => (i < 5 ? ("info" as const) : i >= 46 ? ("neutral" as const) : undefined))}
        />
        <Cite text={CITE_ACS} />
      </Stack>

      <Divider />

      {/* Seniority proxies — ATUS */}
      <Stack gap={10}>
        <H2>
          Seniority proxies: management 48.1% and top earners 51.0% work at home on days worked —
          vs 10.5% in service jobs
        </H2>
        <Callout tone="warning" title="Different source and definition than the state table">
          Official surveys do not publish WFH by job level (VP vs individual contributor). Closest
          published cuts are occupation, usual weekly earnings quartile, and education — labeled
          here as seniority proxies. ATUS counts any work at home on days worked (2024), not ACS
          “usually worked from home.”
        </Callout>
        <Grid columns={4} gap={12}>
          <Stat value={`${ATUS_MGMT}%`} label="Mgmt / business / finance" tone="info" />
          <Stat value={`${ATUS_TOP_EARN}%`} label="Top earnings quartile" tone="info" />
          <Stat value={`${ATUS_SERVICE}%`} label="Service occupations" />
          <Stat value={`${ATUS_BOT_EARN}%`} label="Bottom earnings quartile" />
        </Grid>
        <BarChart
          horizontal
          categories={PROXY_CATS}
          series={[
            { name: "Story groups (mgmt / top earners)", data: PROXY_FOCAL, tone: "info" },
            { name: "Context (other ATUS cuts)", data: PROXY_REST, tone: "neutral" },
          ]}
          beginAtZero
          valueSuffix="%"
          height={300}
        />
        <Text size="small" tone="secondary">
          Also: bachelor&apos;s+ {ATUS_BACH}% vs high-school no college {ATUS_HS}%; full-time{" "}
          {ATUS_FT}% vs part-time {ATUS_PT}%; ATUS overall {ATUS_OVERALL}% of those who worked that
          day. All figures are % of employed persons who worked on an average day.
        </Text>
        <Cite text={CITE_ATUS} />
      </Stack>

      <Divider />

      {/* Firm size — ABS */}
      <Stack gap={10}>
        <H2>
          77.5% of firms with 500+ employees had any WFH workers — vs 35.8% of firms under 500
        </H2>
        <Callout tone="warning" title="Different source — firm-level, not worker-level">
          This is the share of employer firms that reported having employees who worked from home
          (ABS WORKHOME), not the share of workers at small vs large firms who WFH. ACS/ATUS do not
          publish a worker×firm-size cross; that break was not invented. Bins are EMPSZFI 655
          (&lt;500) and 657 (500+) — the SBA cutoff used elsewhere in this project.
        </Callout>
        <Grid columns={2} gap={12}>
          <Stat value={`${ABS_GE500}%`} label="Firms 500+ with any WFH employees" tone="info" />
          <Stat value={`${ABS_LT500}%`} label="Firms <500 with any WFH employees" />
        </Grid>
        <BarChart
          categories={["Firms <500 employees", "Firms 500+ employees"]}
          series={[
            {
              name: "% of firms that had employees who worked from home",
              data: [ABS_LT500, ABS_GE500],
              tone: "info",
            },
          ]}
          beginAtZero
          valueSuffix="%"
          height={220}
        />
        <Cite text={CITE_ABS} />
      </Stack>

      <Divider />

      {/* Conflicts + refused */}
      <Stack gap={10}>
        <H2>Source conflicts and breaks refused</H2>
        <Card>
          <CardBody>
            <Stack gap={8}>
              <Text weight="semibold">Definition conflict (not an error)</Text>
              <Text size="small">
                ACS US usually-WFH is {ACS_US_RATE}% of workers 16+. ATUS US any-work-at-home on days
                worked is {ATUS_OVERALL}%. Both are official; they answer different questions. State
                rankings use ACS only. Seniority uses ATUS only. Firm size uses ABS firm-level only.
              </Text>
              <Text weight="semibold">Refused to invent</Text>
              <Text size="small">
                • Job title / corporate seniority ladder (VP vs IC) — not in ACS, ATUS, or ABS.
              </Text>
              <Text size="small">
                • Worker-level WFH rate × firm size &lt;500 vs 500+ — ABS is firm-level; no
                industry-mix imputation.
              </Text>
              <Text size="small">
                • Hybrid vs fully remote worker shares by state — not in ACS B08301; ATUS day-level
                “any time at home” is not a hybrid schedule measure.
              </Text>
            </Stack>
          </CardBody>
        </Card>
        <Text size="small" tone="tertiary">
          Recompute script: Analysis/work-from-home/build_wfh_rates.py · CSVs:
          acs2024_wfh_by_state.csv, atus2024_work_at_home_breaks.csv,
          abs2023_workhome_by_firm_size.csv, assumption_register.csv · Every input tagged RETRIEVED;
          no ESTIMATED rates shipped.
        </Text>
        <Text size="small" tone="tertiary">
          Related framing (not re-litigated here):{" "}
          <Link href="chtr-ehb-benefits-analogy-corporate-to-consumer.canvas.tsx">
            benefits analogy canvas
          </Link>
          .
        </Text>
      </Stack>
    </Stack>
  );
}
