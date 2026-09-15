/**
 * Charter MAN6930 — draft diagnosis under Root B (firm).
 * Rival mechanism / course-of-action fork: expand broadband product vs
 * small-fix / perception stack. Not a new root; not a valuation thesis.
 * Facts from rural geography + CMCSA capex canvases; FY2025 10-K.
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
  Pill,
  Row,
  Stack,
  Stat,
  Table,
  Text,
} from "cursor/canvas";

export default function ChtrBroadbandExpansionDiagnosis() {
  return (
    <Stack gap={24}>
      <Stack gap={8}>
        <Row gap={8} align="center" wrap>
          <Pill tone="neutral">Root B base</Pill>
          <Pill tone="warning">Draft diagnosis</Pill>
          <Pill tone="added">Expand product not perception</Pill>
        </Row>
        <Text size="small" tone="tertiary">
          Role: rival mechanism / course-of-action fork under Root B (firm) —
          not a new Root A, not a market-cap narrative. Parent frame:
          chtr-base-frame.
        </Text>
      </Stack>

      <Stack gap={10}>
        <H1>
          Expand the broadband product — do not treat the gap as a stack of
          small perception fixes
        </H1>
        <Text tone="secondary">
          Under Root B, Charter’s relative underperformance is a{" "}
          <Text as="span" weight="semibold">
            broadband product and competitive-positioning
          </Text>{" "}
          problem (network reach/quality, offer, YoY Internet trajectory vs
          CMCSA) — not an equity-valuation or investor-optics problem.
        </Text>
        <Callout tone="danger" title="Reject: valuation-as-problem">
          “Undervalued,” buybacks, and perception campaigns aimed at the stock
          story are the wrong layer. Root C (Internet acceleration as priced
          variable) still gates recommendations — it does not turn the
          diagnosis into “fix the stock story.” Fix the product; the tape
          follows Internet outcomes.
        </Callout>
      </Stack>

      <Grid columns={3} gap={12}>
        <Stat value="1.3M" label="Activated rural passings (YE2025)" tone="info" />
        <Stat value=">$8B" label="Initiative spend target" />
        <Stat value=">$2B" label="Grants awarded to date" tone="success" />
      </Grid>

      <Divider />

      <Stack gap={10}>
        <H2>Two theses under Root B</H2>
        <Text tone="secondary">
          Same parent frame (worse Internet slope than CMCSA under shared
          attackers). They disagree on the operating lever.
        </Text>
        <Table
          headers={[
            "Dimension",
            "Small-fixes / perception thesis",
            "Product expansion thesis (this draft)",
          ]}
          columnAlign={["left", "left", "left"]}
          rows={[
            [
              "What the gap is",
              "Compounding nits: brand, ops tickets, messaging, investor story",
              "Core broadband product/network competitiveness and growth",
            ],
            [
              "Wrong play",
              "— (this is the wrong play)",
              "Treating a large product gap as small perception/ops patches",
            ],
            [
              "Right play",
              "Campaigns, service polish, IR narrative, video/mobile optics",
              "Expand/improve current broadband: reach, quality, offer vs peers",
            ],
            [
              "Broadband’s role",
              "One of several products to massage for sentiment",
              "Loss-leader / growth engine — the stock-relevant product to expand",
            ],
            [
              "Video / mobile",
              "Useful for perception and connectivity story",
              "Can distract; do not substitute for Internet trajectory relief",
            ],
            [
              "Falsify if…",
              "Perception lifts close CMCSA YoY Internet gap without product change",
              "Rural/network expansion converts to revenue and closes YoY Internet gap vs CMCSA",
            ],
          ]}
          striped
        />
      </Stack>

      <Divider />

      <Grid columns={2} gap={16}>
        <Card>
          <CardHeader trailing={<Pill tone="info" size="sm">Doing</Pill>}>
            What Charter is already doing
          </CardHeader>
          <CardBody>
            <Stack gap={8}>
              <Text size="small">
                Subsidized rural passings as the expansion vehicle: build
                network where grants offset cost; management frames “long-term
                infrastructure-style returns.”
              </Text>
              <Text size="small">
                ~1.3M passings activated since early 2022; initiative targets
                &gt;1.7M passings, &gt;$8B spend, &gt;$2B grants (RDOF / BEAD /
                state). ~$7.7B spent since 2022; ~$2.2B rural in 2025 alone.
              </Text>
              <Text size="small" tone="secondary">
                Geography (RDOF proxy): metro-adjacent SE / Midwest / TX belt —
                plant extension, not deep remote greenfield. No disclosed ROI
                year or payback schedule in public filings.
              </Text>
            </Stack>
          </CardBody>
        </Card>
        <Card>
          <CardHeader trailing={<Pill tone="added" size="sm">Measured</Pill>}>
            What was missing — now sized
          </CardHeader>
          <CardBody>
            <Stack gap={8}>
              <Text size="small">
                Q1 2026: rural +41k CR, core −204k CR. Rural covered 20% of
                the core hole and is already inside the company −163k print.
                Take stuck at 38% (company 54%). Residential revenue $167M
                (1.6% of the firm).
              </Text>
              <Text size="small">
                Rural add acceleration vs Q1’25: +2k. That is none of the
                −61k Internet YoY break; core proxy YoY −63k vs CMCSA +118k.
                Remainder to 1.7M: 120–170k lifetime customers vs a 179k
                quarterly slope gap.
              </Text>
              <Text size="small" tone="secondary">
                Conversion analysis: chtr-rural-core-conversion. Expansion
                converts and still cannot close Root B. Mix-adjusted core vs
                CMCSA is the measurement that remains.
              </Text>
            </Stack>
          </CardBody>
        </Card>
      </Grid>

      <Stack gap={8}>
        <H2>Known facts (retrieved)</H2>
        <Table
          headers={["Fact", "Figure", "Use in this diagnosis"]}
          columnAlign={["left", "left", "left"]}
          rows={[
            [
              "Activated subsidized rural passings",
              "~1.3M (YE2025)",
              "Expansion underway — network reach, not perception",
            ],
            [
              "Spend / grants / target",
              ">$8B spend · >$2B grants · >1.7M passings",
              "Subsidy-backed product expansion vehicle",
            ],
            [
              "Spent to date (inception 2022)",
              "~$7.7B · ~$2.2B in 2025",
              "Real cash into plant; intensity already elevated vs CMCSA",
            ],
            [
              "Management return frame",
              "“Long-term infrastructure-style returns”",
              "Explicitly not short-cycle FCF; no ROI years disclosed",
            ],
            [
              "Metro adjacency (RDOF proxy)",
              "Weighted avg ~40–50 mi to MSA ≥250k",
              "Plant-adjacent expansion — competitive with FWA/fiber in those counties",
            ],
            [
              "Internet YoY vs CMCSA (Q1’26)",
              "Worse slope (−179k swing)",
              "Product-positioning gap still open despite rural capex",
            ],
          ]}
          striped
        />
      </Stack>

      <Divider />

      <Stack gap={8}>
        <H2>Ask the CEO — internal only, one answer each</H2>
        <Text size="small" tone="secondary">
          Rural vs core conversion is already public (trending subset). These
          five are not. Ask one, stop, record the answer before the next.
        </Text>
        <Table
          headers={["Ask", "Direct response", "What it decides"]}
          columnAlign={["left", "left", "left"]}
          rows={[
            [
              "Of the 41k rural customer relationships added in Q1, how many were Internet?",
              "A thousand count",
              "Whether rural CR is Internet relief or a mixed/mobile-inflated add.",
            ],
            [
              "What is today’s take rate on rural passings activated in 2023?",
              "A percent",
              "Vintage ripening vs a permanently ~38% take — product competitiveness on plant already lit.",
            ],
            [
              "What payback year is written in the rural board pack?",
              "A calendar year, or none",
              "Whether rural is on a 24-month Internet clock or an infrastructure clock.",
            ],
            [
              "On the non-rural base, mix-adjusted vs Comcast, did Q1 Internet loss rates still exceed theirs?",
              "Yes / no / not run",
              "Whether the core hole is offer/GTM or footprint mix. Remaining Root B gate.",
            ],
            [
              "On the non-rural footprint, what is the single largest sampled disconnect reason in Q1?",
              "One named reason",
              "The lever on the −204k core hole — not more passings.",
            ],
          ]}
          striped
        />
        <Text size="small" tone="tertiary">
          Do not re-ask passings, grant dollars, or the 38% blended take — those
          are retrieved. If vintage take on 2023 plant is still ~38%, expansion
          is converting at a ceiling, not ramping.
        </Text>
      </Stack>

      <Divider />

      <Grid columns={2} gap={16}>
        <Stack gap={8}>
          <H2>Kill rule</H2>
          <Text size="small">
            Kill the product-expansion thesis if mix-adjusted Internet losses
            converge with CMCSA while rural/network spend stays flat — or if
            win/loss files show the binding gap is price/promo/ops nits that
            close without further network expansion. Kill the small-fixes
            thesis if perception/ops campaigns run and the YoY Internet gap vs
            CMCSA does not narrow.
          </Text>
        </Stack>
        <Stack gap={8}>
          <H2>Unwilling to claim</H2>
          <Stack gap={4}>
            <Text size="small">
              • That rural passings have already fixed the Root B Internet slope
            </Text>
            <Text size="small">
              • That perception or IR campaigns close the CMCSA broadband gap
            </Text>
            <Text size="small">
              • That market valuation / “undervalued” is the operating problem
            </Text>
            <Text size="small">
              • A disclosed rural ROI year or near-term revenue conversion rate
            </Text>
            <Text size="small">
              • That video or mobile substitutes for Internet trajectory relief
            </Text>
          </Stack>
        </Stack>
      </Grid>

      <Callout tone="info" title="Next measurement (what would falsify)">
        Rural vs core is now run (chtr-rural-core-conversion): rural converts
        and the YoY Internet gap vs CMCSA still widens on the non-rural base —
        expansion is the wrong scale/layer for the slope. Remaining gate is
        the mix-adjusted core question above. If those rates converge, Root B
        is mix not offer. Do not use stock move alone as the falsifier — use
        broadband outcomes.
      </Callout>

      <Text size="small" tone="tertiary">
        Sources: CHTR FY2025 10-K (1.3M; &gt;$8B / &gt;$2B; infrastructure-style
        returns) · chtr-rural-geography · chtr-cmcsa-capex ·
        chtr-relative-performance · chtr-rural-core-conversion · Root B:
        chtr-base-frame. Draft under Root B — not a recommendation.
        Assignment anchor: end Q1 2026.
      </Text>
    </Stack>
  );
}
