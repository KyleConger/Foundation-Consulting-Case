/**
 * Charter MAN6930 — committed base frame (one-pager).
 * Source of truth for role labels: chtr-industry-vs-firm-framestorm.canvas.tsx §4–5.
 * DRAFT framing commitment — not a recommendation.
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
  Table,
  Text,
} from "cursor/canvas";

export default function ChtrBaseFrame() {
  return (
    <Stack gap={24}>
      <Stack gap={8}>
        <Row gap={8} align="center" wrap>
          <Pill tone="warning">DRAFT — framing commitment</Pill>
          <Pill tone="added">PROMOTED / BASE</Pill>
          <Pill tone="neutral">Root B · Firm</Pill>
        </Row>
        <Text size="small" tone="tertiary">
          From industry-vs-firm framestorm §4–5. Downstream relative-performance,
          client Q tree, and rural work operate under this root.
        </Text>
      </Stack>

      <Stack gap={10}>
        <H1>
          Relative underperformance: peers face the same fiber/FWA attackers;
          Charter’s YoY Internet trajectory is worse than Comcast’s
        </H1>
        <Text tone="secondary">
          Same wind, worse slope — on{" "}
          <Text as="span" weight="semibold">
            broadband product and competitive positioning
          </Text>{" "}
          (Internet trajectory vs CMCSA), not on market valuation. The binding
          operating problem is Charter’s relative broadband game — not that
          cable alone is under attack, and not that the equity is
          “mispriced.”
        </Text>
        <Callout tone="warning" title="Why this is the base">
          Contradicts pure industry fatalism. Falsified if DMA-mix adjusted
          Internet loss rates converge with CMCSA. Role: root frame B (firm) —
          labeled PROMOTED in the framestorm. Stock de-rating is a symptom of
          the broadband gap, not the problem to solve.
        </Callout>
        <Callout tone="info" title="Operating mechanism under Root B (draft)">
          Expand/improve the current broadband product (incl. rural passings as
          network expansion) rather than a stack of small perception/ops fixes
          or investor-story patches. Detail:
          chtr-broadband-expansion-diagnosis.canvas.tsx.
        </Callout>
      </Stack>

      <Divider />

      <Stack gap={10}>
        <H2>Still live — not the base</H2>
        <Text tone="secondary">
          These stay in the diagnosis. They are floor or gate, not the operating
          root we solve from.
        </Text>
        <Grid columns={2} gap={12}>
          <Card>
            <CardHeader trailing={<Pill tone="deleted">Root A · Industry</Pill>}>
              Structural share-shift to fiber / FWA
            </CardHeader>
            <CardBody>
              <Stack gap={6}>
                <Text size="small">
                  Cable Internet relationships are being permanently reallocated.
                  Explains peer losses and the sector multiple.
                </Text>
                <Text size="small" tone="secondary">
                  Role: industry floor — not the operating root. Peer gaps are
                  not noise under Root B.
                </Text>
              </Stack>
            </CardBody>
          </Card>
          <Card>
            <CardHeader trailing={<Pill tone="info">Root C · Belief</Pill>}>
              Internet acceleration is the priced variable
            </CardHeader>
            <CardBody>
              <Stack gap={6}>
                <Text size="small">
                  Cash and mobile do not buy the multiple; the tape prices
                  Internet YoY surprise / run-rate.
                </Text>
                <Text size="small" tone="secondary">
                  Role: hard constraint / gate for recommendations — not the
                  A-vs-B cause fork.
                </Text>
              </Stack>
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
              "Converged-attacker asymmetry (carriers own spectrum; CHTR is MVNO)",
              "Rival mechanism under A/B",
              "Competes with ‘just price better’ as the fix",
            ],
            [
              "HFC / DOCSIS credibility vs FTTH",
              "Rival mechanism under A",
              "Competes with GTM/pricing as the firm gap",
            ],
            [
              "Buybacks / ‘undervalued’ / stage capital",
              "Decision architecture — DEMOTED",
              "Symptom of de-rating after we know the operating problem",
            ],
          ]}
          striped
        />
      </Stack>

      <Divider />

      <Grid columns={2} gap={16}>
        <Stack gap={8}>
          <H2>What this makes us measure</H2>
          <Stack gap={4}>
            <Text size="small">
              • Footprint-adjusted loss rates CHTR vs CMCSA (mix control)
            </Text>
            <Text size="small">
              • Win/loss reasons (ops sampling — class call-center caution)
            </Text>
            <Text size="small">
              • Price/promo gap vs FWA and fiber in overlapping zips
            </Text>
            <Text size="small">
              • Bundle attach; Advanced / Invincible WiFi retention lift
            </Text>
            <Text size="small">
              • Earnings-day reaction vs Internet surprise after any GTM change
            </Text>
          </Stack>
        </Stack>
        <Stack gap={8}>
          <H2>What we are not claiming</H2>
          <Stack gap={4}>
            <Text size="small">
              • That industry share-shift is false — it is the floor (Root A)
            </Text>
            <Text size="small">
              • That Internet belief is irrelevant — it gates recs (Root C)
            </Text>
            <Text size="small">
              • That buybacks or “undervalued” is the root diagnosis
            </Text>
            <Text size="small">
              • That Mobile / connectivity nets against Internet customers
            </Text>
            <Text size="small">
              • A recommendation — this page is the committed problem frame only
            </Text>
          </Stack>
        </Stack>
      </Grid>

      <Callout tone="info" title="Question for the client next (not a conclusion)">
        When Comcast’s residential broadband losses improved by ~117k YoY in Q1
        2026 while yours roughly doubled, what did you actually see in the
        win/loss file — footprint mix, price gap to FWA, fiber overbuild
        intensity, or something else — and has anyone outside Spectrum already
        said no to the current Internet offer in a way that would show up in
        that file?
      </Callout>

      <Text size="small" tone="tertiary">
        Source: chtr-industry-vs-firm-framestorm.canvas.tsx §4–5 · Operates under
        this base: chtr-relative-performance, client Q tree, rural geography,
        broadband-expansion diagnosis. Assignment anchor: end Q1 2026.
      </Text>
    </Stack>
  );
}
