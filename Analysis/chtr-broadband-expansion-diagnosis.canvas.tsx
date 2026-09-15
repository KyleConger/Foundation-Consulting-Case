/**
 * Charter MAN6930 — draft diagnosis under Root B (firm).
 * Lever fork: core broadband product/offer vs small-fix / perception stack.
 * Not a new root; not a valuation thesis; rural is the in-flight program,
 * not the closer. Disclosed figures: CORE-INFORMATION.md (Q1 2026).
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
          <Pill tone="added">Core product — not perception, not more rural</Pill>
        </Row>
        <Text size="small" tone="tertiary">
          Role: rival mechanism / course-of-action fork under Root B (firm) —
          not a new Root A, not a market-cap narrative. Parent: chtr-base-frame.
          Q1 2026 figures from CORE-INFORMATION unless tagged as conversion.
        </Text>
      </Stack>

      <Stack gap={10}>
        <H1>
          The gap is on the core footprint — do not treat it as perception,
          and do not treat more rural passings as the closer
        </H1>
        <Text tone="secondary">
          Under Root B, Charter’s relative underperformance is a{" "}
          <Text as="span" weight="semibold">
            broadband product and competitive-positioning
          </Text>{" "}
          problem on the plant that is already built (offer, quality, overlap
          GTM vs CMCSA) — not an equity-optics problem, and not a missing
          rural-construction program. CORE-INFORMATION already shows that
          program running inside a deteriorating Internet print.
        </Text>
        <Callout tone="danger" title="Reject: valuation-as-problem">
          “Undervalued,” buybacks, and perception campaigns aimed at the stock
          story are the wrong layer. Root C still gates recs on the Internet
          print. Fix the core product; the tape follows Internet outcomes.
        </Callout>
      </Stack>

      <Grid columns={4} gap={12}>
        <Stat value="−120k" label="Internet adds Q1’26 (CORE)" tone="danger" />
        <Stat value="+41k" label="Rural CR adds Q1’26 (CORE)" tone="info" />
        <Stat value="−204k" label="Core CR adds (company − rural)" tone="danger" />
        <Stat value="−179k" label="YoY slope gap vs CMCSA (peer overlay)" tone="warning" />
      </Grid>
      <Text size="small" tone="tertiary">
        CORE §5 / §8: Internet −120k; CR −163k; rural +41k CR on 89k passings.
        Core −204k = −163k − (+41k). Peer overlay not in CORE: CMCSA resid. BB
        −65k / YoY +118k vs CHTR Internet YoY −61k.
      </Text>

      <Divider />

      <Stack gap={10}>
        <H2>Two theses under Root B</H2>
        <Text tone="secondary">
          Same parent frame (worse Internet slope than CMCSA). They disagree on
          the operating lever. Rural construction is the in-flight program —
          already in CORE — not a third root.
        </Text>
        <Table
          headers={[
            "Dimension",
            "Small-fixes / perception thesis",
            "Core product thesis (this draft)",
          ]}
          columnAlign={["left", "left", "left"]}
          rows={[
            [
              "What the gap is",
              "Compounding nits: brand, ops tickets, messaging, investor story",
              "Core-plant broadband competitiveness (offer, quality, overlap GTM)",
            ],
            [
              "Wrong play",
              "— (this is the wrong play)",
              "Treating a core product gap as perception patches — or as more rural passings",
            ],
            [
              "Right play",
              "Campaigns, service polish, IR narrative, video/mobile optics",
              "Improve current broadband on the core footprint vs peers",
            ],
            [
              "Rural’s role (CORE)",
              "A talking point for the infrastructure / connectivity story",
              "In-flight, converting, wrong scale — Q1 +41k CR vs −204k core hole",
            ],
            [
              "Video / mobile (CORE Q1)",
              "Useful for perception (video −60k; mobile +368k)",
              "Do not substitute for Internet trajectory relief (−120k / −1.3% $)",
            ],
            [
              "Falsify if…",
              "Perception lifts close CMCSA YoY Internet gap without product change",
              "Mix-adjusted core Internet losses converge with CMCSA, or win/loss is price/ops nits only",
            ],
          ]}
          striped
        />
      </Stack>

      <Divider />

      <Grid columns={2} gap={16}>
        <Card>
          <CardHeader trailing={<Pill tone="info" size="sm">CORE — already doing</Pill>}>
            Rural program (disclosed)
          </CardHeader>
          <CardBody>
            <Stack gap={8}>
              <Text size="small">
                YE2025: $7.7B spent since 2022; ~1.3M subsidized rural passings
                activated; 2025 spend $2.2B; 483k passings that year. Target
                &gt;1.7M passings, &gt;$8B spend, &gt;$2B grants (RDOF / BEAD /
                state). Management: “long-term infrastructure-style returns.”
              </Text>
              <Text size="small">
                Q1 2026: 89k passings activated; rural-footprint customer
                relationships +41k. Q1 rural initiative capex $427M. Company
                capex $2.9B (line extensions $812M).
              </Text>
              <Text size="small" tone="secondary">
                Geography (RDOF proxy, not CORE): metro-adjacent SE / Midwest /
                TX. No ROI year in filings.
              </Text>
            </Stack>
          </CardBody>
        </Card>
        <Card>
          <CardHeader trailing={<Pill tone="added" size="sm">Conversion — sized</Pill>}>
            Core vs rural (what CORE does not split)
          </CardHeader>
          <CardBody>
            <Stack gap={8}>
              <Text size="small">
                Trending rural subset: Q1 rural CR 527k / 1,385k passings =
                38% take vs company 54%. Rural residential revenue $167M
                (1.6% of firm). Company Internet $5,852M (−$78M YoY).
              </Text>
              <Text size="small">
                Rural add acceleration vs Q1’25: +2k. None of the −61k
                Internet YoY break. Remainder to 1.7M floor: 120–170k lifetime
                customers vs a 179k quarterly slope gap vs CMCSA.
              </Text>
              <Text size="small" tone="secondary">
                chtr-rural-core-conversion. Rural converts and cannot close
                Root B. Mix-adjusted core vs CMCSA remains.
              </Text>
            </Stack>
          </CardBody>
        </Card>
      </Grid>

      <Stack gap={8}>
        <H2>Known facts (CORE-INFORMATION)</H2>
        <Table
          headers={["Fact", "Figure", "Use in this diagnosis"]}
          columnAlign={["left", "left", "left"]}
          rows={[
            [
              "Internet Q1’26 / Q1’25",
              "−120k / −59k (YoY −61k)",
              "Root B symptom — CORE §5; MD&A names competitive environment",
            ],
            [
              "Internet customers / $ Q1",
              "29,560k · $5,852M (−1.3%)",
              "Volume and dollars both down; not an ARPU-only story",
            ],
            [
              "CR Q1 / rural CR Q1",
              "−163k company · +41k rural",
              "Rural already inside the print; core identity −204k",
            ],
            [
              "Rural inception / Q1 build",
              "$7.7B · 1.3M YE25 · Q1 89k passings",
              "Program is running — not a missing expansion decision",
            ],
            [
              "Mobile / video Q1",
              "+368k lines · video −60k",
              "Cannot substitute for Internet trajectory (Root C)",
            ],
            [
              "FTTH overlap (10-K)",
              "AT&T ~27% · Verizon ~16% of footprint",
              "Industry floor (Root A) — mix control still unrun vs CMCSA",
            ],
          ]}
          striped
        />
      </Stack>

      <Divider />

      <Stack gap={8}>
        <H2>Ask the CEO — internal only, one answer each</H2>
        <Text size="small" tone="secondary">
          CORE already has rural +41k CR, Internet −120k, and the $7.7B
          program. These five are not in CORE. Ask one, stop, record the
          answer before the next.
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
              "Vintage ripening vs a permanently ~38% take on plant already lit.",
            ],
            [
              "What payback year is written in the rural board pack?",
              "A calendar year, or none",
              "24-month Internet clock vs infrastructure clock (CORE is silent).",
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
      </Stack>

      <Divider />

      <Grid columns={2} gap={16}>
        <Stack gap={8}>
          <H2>Kill rule</H2>
          <Text size="small">
            Kill “more rural closes Root B” — already: remainder stock
            120–170k vs 179k quarterly slope gap, rural acceleration +2k.
            Kill the core-product thesis if mix-adjusted core Internet losses
            converge with CMCSA, or if win/loss shows price/promo/ops nits
            that close without a product change. Kill small-fixes if
            perception/ops campaigns run and the YoY Internet gap vs CMCSA
            does not narrow.
          </Text>
        </Stack>
        <Stack gap={8}>
          <H2>Unwilling to claim</H2>
          <Stack gap={4}>
            <Text size="small">
              • That rural passings have fixed the Root B Internet slope
            </Text>
            <Text size="small">
              • That perception or IR campaigns close the CMCSA broadband gap
            </Text>
            <Text size="small">
              • That market valuation / “undervalued” is the operating problem
            </Text>
            <Text size="small">
              • A disclosed rural ROI year (CORE is silent; trending gives
              revenue, not payback)
            </Text>
            <Text size="small">
              • That video or mobile substitutes for Internet trajectory relief
            </Text>
            <Text size="small">
              • Rural CR = Internet (CORE discloses relationships only)
            </Text>
          </Stack>
        </Stack>
      </Grid>

      <Callout tone="info" title="Next measurement (what would falsify)">
        CORE + conversion: rural converts and the YoY Internet gap vs CMCSA
        still widens on the non-rural base. Remaining gate is the
        mix-adjusted core question above. If those rates converge, Root B is
        mix not offer. Do not use stock move alone — use broadband outcomes.
      </Callout>

      <Text size="small" tone="tertiary">
        Sources: PrimarySources/CORE-INFORMATION.md (§4–5, §8, §10, §11) ·
        Q1 2026 trending rural page (conversion) · chtr-rural-core-conversion
        · chtr-relative-performance (CMCSA) · Root B: chtr-base-frame. Draft
        under Root B — not a recommendation. Assignment anchor: end Q1 2026.
      </Text>
    </Stack>
  );
}
