/**
 * Customer network performance and churn — Decision Planning.
 * Under Root B: is the core Internet hole a network-quality churn story
 * or a competitive net-loss-rate story? Q1 2026 anchor.
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

const RATE_QTRS = [
  "24Q1",
  "24Q2",
  "24Q3",
  "24Q4",
  "25Q1",
  "25Q2",
  "25Q3",
  "25Q4",
  "26Q1",
];
/** CHTR total Internet net losses as % of beginning stock. */
const CHTR_INET_RATE = [0.24, 0.49, 0.36, 0.59, 0.2, 0.39, 0.36, 0.4, 0.4];

export default function ChtrNetworkChurn() {
  return (
    <Stack gap={28}>
      <Stack gap={8}>
        <Row gap={8} wrap>
          <Pill tone="info">Decision Planning</Pill>
          <Pill tone="warning">Network vs churn</Pill>
          <Pill>Q1 2026 anchor · Root B</Pill>
        </Row>
        <H1>
          Charter’s residential Internet net-loss rate is 1.8× Comcast’s —
          and the public network lines moved the other way
        </H1>
        <Text tone="secondary">
          Gross churn is not disclosed. This page uses net-loss rate (% of
          starting customers) so Charter residential Internet can sit next to
          Comcast domestic residential broadband. Network performance is tested
          with the disclosed ops and capex lines, not with a speed lab.
        </Text>
      </Stack>

      <Callout tone="danger" title="Headline (commit)">
        Q1 2026: Charter residential Internet net-loss rate 0.42% of starting
        base vs Comcast 0.23% — 1.87× unrounded, commit 1.8× (rounded down).
        Applying Comcast’s rate to Charter’s base implies 63k losses; actual
        was 117k. Excess 54k (rounded down from 54.4k). A year earlier Charter
        was better on rate (0.20% vs 0.62%). Comcast cut its loss rate;
        Charter’s doubled.
      </Callout>

      <Grid columns={4} gap={12}>
        <Stat value="0.42%" label="CHTR res. Internet net-loss rate Q1’26" tone="danger" />
        <Stat value="0.23%" label="CMCSA resid. BB net-loss rate Q1’26" />
        <Stat value="1.8×" label="Committed rate ratio (1.87 unrounded)" tone="danger" />
        <Stat value="54k" label="Excess vs peer rate (round down)" tone="warning" />
      </Grid>
      <Text size="small" tone="tertiary">
        Net-loss rate = |quarterly net adds| / beginning customers. CHTR
        residential Internet begin 27,641k (YE2025) · −117k Q1. CMCSA domestic
        residential BB begin 28,719k · −65k. Sources: CHTR Ex99.1 / 10-K ·
        CMCSA Ex99.1 Q1 2026. Not gross churn.
      </Text>

      <Divider />

      <Stack gap={8}>
        <H2>1. Rate space — the Root B slope as churn</H2>
        <Text>
          Headcount gaps can be base-size. Rates are not. Charter and Comcast
          started Q1 within ~1M residential broadband customers of each other.
          Charter’s Q1’25 rate was a third of Comcast’s; by Q1’26 it was 1.8×.
        </Text>
        <BarChart
          categories={["Q1 2025", "Q1 2026"]}
          series={[
            {
              name: "CHTR res. Internet net-loss rate (%)",
              data: [0.2, 0.42],
              tone: "danger",
            },
            {
              name: "CMCSA domestic resid. BB net-loss rate (%)",
              data: [0.62, 0.23],
              tone: "info",
            },
          ]}
          height={240}
          valueSuffix="%"
          yMin={0}
          yMax={0.75}
        />
        <Text size="small" tone="tertiary">
          Percent of beginning residential broadband customers lost, net, in
          the quarter. Source: CHTR Ex99.1 · CMCSA Ex99.1 Q1 2026. Comcast
          Q1’25 begin = 29,190 − (−183) = 29,373k.
        </Text>
        <LineChart
          categories={RATE_QTRS}
          series={[
            {
              name: "CHTR total Internet net-loss rate (% of begin)",
              data: CHTR_INET_RATE,
              tone: "danger",
            },
          ]}
          height={220}
          valueSuffix="%"
          yMin={0}
          yMax={0.7}
        />
        <Text size="small" tone="tertiary">
          Total Internet (residential + small business), not the residential
          cut used in the peer bars. Q1’25 (0.20%) is the series low; Q1’26
          (0.40%) is a double, not a new high (Q4’24 was 0.59%).
        </Text>
      </Stack>

      <Stack gap={8}>
        <H2>2. Network-performance frame — public lines do not support it</H2>
        <Text>
          If Q1’s doubling were a network-quality or service-failure churn
          wave, field and care costs typically rise (truck rolls, calls). They
          fell. Upgrade/rebuild capex rose 71% in the same quarter. Invincible
          WiFi launched in February — one month of Q1, and Q1’25 was already
          before that product.
        </Text>
        <Grid columns={3} gap={12}>
          <Stat value="−$30M" label="Field + customer ops opex YoY" tone="success" />
          <Stat value="+71%" label="Upgrade/rebuild capex YoY ($675M vs $395M)" tone="info" />
          <Stat value="Feb’26" label="Invincible WiFi launch (1 month of Q1)" />
        </Grid>
        <Table
          headers={["Network / service line (Q1’26)", "Figure", "Churn read"]}
          columnAlign={["left", "right", "left"]}
          rowTone={["success", "success", "info", undefined, "warning"]}
          rows={[
            [
              "Field and technology ops",
              "$1,258M (−1.8%)",
              "Lower labor — not a truck-roll spike",
            ],
            [
              "Customer operations",
              "$766M (−0.8%)",
              "Release: driven by lower bad debt, not more contacts",
            ],
            [
              "In-house premise transactions (FY25)",
              ">80%",
              "Ops model unchanged as a disclosed quality claim",
            ],
            [
              "Speed claim in the Q1 release",
              "Opensignal fastest among top 5 (May 2025)",
              "Management’s own network-quality exhibit, lagging the Q1 print",
            ],
            [
              "Video net adds vs CMCSA",
              "−60k vs −322k",
              "If company-wide service failed, video should worsen too — it improved",
            ],
          ]}
          striped
        />
        <Callout tone="warning" title="What this frame’s number is">
          Network-ops evidence can explain $0 of the 54k rate-excess without a
          sampled disconnect file. That is not proof that WiFi/reliability is
          irrelevant in overlap zips — only that it is not visible in the
          disclosed cost or product-claim lines. One-product penetration fell
          48.9% → 47.7% (more two-product from mobile), so the Q1 hole is not
          “more internet-only customers.”
        </Callout>
      </Stack>

      <Divider />

      <Stack gap={8}>
        <H2>3. Competitive-overlap frame — rates under two scenarios</H2>
        <Text>
          10-K: AT&T terrestrial 100 Mbps+ on ~27% of footprint, Verizon ~16%.
          Not additive (union unknown). Applying company 54% CR penetration to
          AT&T passings is ESTIMATED — overlap take may differ.
        </Text>
        <Grid columns={2} gap={16}>
          <Card>
            <CardHeader>Proportional (losses follow footprint)</CardHeader>
            <CardBody>
              <Text size="small">
                27% of −120k = 32k in AT&T overlap; 88k on the other 73%. Rates
                look similar on and off overlap. This scenario does not produce
                Root B by itself.
              </Text>
            </CardBody>
          </Card>
          <Card>
            <CardHeader>Concentrated (all −120k in AT&T overlap)</CardHeader>
            <CardBody>
              <Text size="small">
                ~8.6M estimated customers on AT&T-overlap plant. 120k / 8,553k
                = 1.40% quarterly net loss there, ~0% elsewhere. That would be
                competitive churn, not a disclosed outage. Unrun without zip
                files.
              </Text>
            </CardBody>
          </Card>
        </Grid>
        <Text size="small" tone="tertiary">
          AT&T passings 0.27 × 58,661k = 15,838k. × 0.540 pen = 8,553k
          (ESTIMATED). Verizon 16% is a second disclosed slice; union ≤ 43%
          if no overlap, ≥ 27% if Verizon sits inside AT&T.
        </Text>
      </Stack>

      <Stack gap={8}>
        <H2>4. Core vs rural — where the net losses sit</H2>
        <Text>
          Company CR −163k includes rural +41k. Core CR −204k on 31,360k
          beginning core = 0.65% quarterly net-loss rate vs 0.51% company-wide.
          Rural is not the churn problem; it is the only disclosed positive CR
          channel.
        </Text>
        <Grid columns={3} gap={12}>
          <Stat value="0.65%" label="Core CR net-loss rate Q1" tone="danger" />
          <Stat value="0.51%" label="Company CR net-loss rate Q1" />
          <Stat value="+8.4%" label="Rural CR vs YE2025 rural stock" tone="info" />
        </Grid>
      </Stack>

      <Divider />

      <Stack gap={8}>
        <H2>Two builds, then a cross-check that does not share the rate identity</H2>
        <Table
          headers={["Build", "Headline", "Shared?", "Tag"]}
          columnAlign={["left", "left", "left", "left"]}
          rowTone={["danger", "warning", "info"]}
          rows={[
            [
              "1. Residential rate vs CMCSA",
              "0.42% vs 0.23% = 1.8×; excess 54k",
              "Uses Q1 net adds / begin",
              "RETRIEVED stocks and adds",
            ],
            [
              "2. Total Internet vs same CMCSA rate",
              "0.40% vs 0.23%; excess 53k",
              "Same CMCSA rate as build 1",
              "Correlated by construction on the peer rate",
            ],
            [
              "3. Cross-check (opex / video / mix)",
              "Field+care −$30M; video ahead +262k vs peer; one-product mix down",
              "No customer-count identity — cost and product mix",
              "RETRIEVED Ex99.1 opex and video",
            ],
          ]}
          striped
        />
        <Text size="small">
          Builds 1 and 2 agreeing on ~53–54k excess is the same peer rate
          applied to two Charter bases. The opex/video cross-check does not
          use net adds and still says “network failure” is the wrong default
          for Q1.
        </Text>
      </Stack>

      <Stack gap={8}>
        <H2>Assumption register</H2>
        <Table
          headers={["ID", "Input / formula", "Value", "Tag"]}
          columnAlign={["left", "left", "right", "left"]}
          rows={[
            ["A1", "CHTR res. Internet YE2025 (Q1 begin)", "27,641k", "RETRIEVED"],
            ["A2", "CHTR res. Internet Q1’26 adds", "−117k", "RETRIEVED"],
            ["A3", "A2 / A1 net-loss rate", "0.42%", "derived"],
            ["B1", "CMCSA resid. BB Q1 begin (28,654+65)", "28,719k", "RETRIEVED"],
            ["B2", "65 / B1 CMCSA net-loss rate", "0.23%", "derived"],
            ["C3", "A3 / B2 (unrounded)", "1.87×", "derived"],
            ["C4", "Committed ratio (round down)", "1.8×", "commit"],
            ["C5", "B2 × A1 expected losses", "62.6k", "derived"],
            ["C7", "|A2| − C5, round down", "54k", "commit"],
            ["D1 / D2", "Q1’25 rates CHTR res / CMCSA", "0.20% / 0.62%", "derived"],
            ["E3", "Core CR −204k / 31,360k begin", "0.65%", "derived"],
            ["F1", "AT&T FTTH share of footprint", "27%", "RETRIEVED 10-K"],
            ["F2", "F1 × passings × 54% pen", "8,553k", "ESTIMATED"],
            ["G1", "Field + care opex YoY", "−$30M", "RETRIEVED"],
            ["H1", "FY25 Internet $ / avg sub", "$795/yr", "derived"],
            ["H2", "54k × H1", "$43M/yr", "derived; round down"],
          ]}
          striped
        />
        <Text size="small" tone="tertiary">
          Dollar-weighted: the 1.8× headline is 100% retrieved stocks and adds.
          F2 (overlap customers) is the high-leverage estimate and does not
          enter the headline. Gross adds / true churn: not disclosed — unused.
          Arithmetic recomputed in Decision Planning/network_churn_model.py.
        </Text>
      </Stack>

      <Grid columns={2} gap={16}>
        <Stack gap={8}>
          <H2>Channel contribution</H2>
          <Text size="small">
            Rate-excess 54k is ~$43M of annual Internet revenue at FY25
            $/sub — too small to be the cash story, large enough to be the
            Root C print. Network evolution (end-2027) and Invincible WiFi
            (Feb) are not Q1 slope closers. Working overlap GTM or core offer
            is the channel that can move the 1.8× rate; more rural passings
            and more upgrade/rebuild (already +71%) did not.
          </Text>
        </Stack>
        <Stack gap={8}>
          <H2>Kill rule</H2>
          <Text size="small">
            Kill “network performance caused the Q1 doubling” if field+care
            stay down while losses rise and the sampled (not coded) disconnect
            file does not name speed/reliability/WiFi as the single largest
            reason on the core. Live on opex. Kill “overlap is irrelevant” if
            that sample or a zip overlay shows losses concentrated on the 27%
            AT&T / 16% Verizon plant at the 1.4% scenario rate.
          </Text>
        </Stack>
      </Grid>

      <Stack gap={8}>
        <H2>Unwilling to claim</H2>
        <Stack gap={4}>
          <Text size="small">• Gross churn or disconnect counts (not disclosed)</Text>
          <Text size="small">
            • That HFC is equivalent to FTTH in overlap zips — no zip file
          </Text>
          <Text size="small">
            • That Opensignal “fastest” means customers do not churn on WiFi
          </Text>
          <Text size="small">
            • Overlap customer counts (F2 applies company pen to AT&T passings)
          </Text>
          <Text size="small">
            • That $43M of Internet $ is the CEO charge — Root C prices the
            print, not this cohort’s revenue
          </Text>
        </Stack>
      </Stack>

      <Callout tone="info" title="Ask the CEO (internal — one answer)">
        In the Q1 core disconnect sample — not agent codes — was
        speed, WiFi, or reliability the single largest reason? Yes or no. If
        no, the 1.8× rate is competitive/GTM until mix control is run. If yes,
        this page’s opex test was the wrong instrument.
      </Callout>

      <Text size="small" tone="tertiary">
        Sources: CHTR Ex99.1 Q1 2026 / FY2025 10-K / trending (CORE-INFORMATION
        §4–5, §8, §10–11) · CMCSA Ex99.1 Q1 2026 (28,654k EOP; 59,164k resid.
        passings; 48.4% pen) · chtr-rural-core-conversion · Root B:
        chtr-base-frame. Model: Decision Planning/network_churn_model.py.
        Assignment anchor: end Q1 2026. Not a recommendation.
      </Text>
    </Stack>
  );
}
