/**
 * Charter MAN6930 — committed base frame (one-pager).
 * Source of truth for role labels: chtr-industry-vs-firm-framestorm.canvas.tsx §4–5.
 * Disclosed figures from PrimarySources/CORE-INFORMATION.md (Q1 2026 anchor).
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
  Stat,
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
          From industry-vs-firm framestorm §4–5. Q1 2026 disclosed figures from
          CORE-INFORMATION (Ex99.1 / 10-K). CMCSA peer overlay is not in that
          file — relative-performance. Assignment anchor: end Q1 2026.
        </Text>
      </Stack>

      <Stack gap={10}>
        <H1>
          Same fiber/FWA wind; Charter’s Internet slope is worse than
          Comcast’s — and the hole is the core plant, not rural
        </H1>
        <Text tone="secondary">
          Root B: relative underperformance on{" "}
          <Text as="span" weight="semibold">
            broadband product and competitive positioning
          </Text>{" "}
          (Internet trajectory vs CMCSA), not valuation. CORE-INFORMATION locks
          the Charter print: Q1 Internet −120k, roughly double Q1’25 (−59k).
          Rural is already in that print (+41k CR). The unresolved game is the
          rest of the footprint.
        </Text>
        <Callout tone="warning" title="Why this is the base">
          Contradicts pure industry fatalism. Falsified if DMA-mix adjusted
          Internet loss rates — on the non-rural base — converge with CMCSA.
          Stock de-rating is a symptom of the broadband gap, not the problem to
          solve. Role: root frame B (firm), PROMOTED.
        </Callout>
      </Stack>

      <Grid columns={4} gap={12}>
        <Stat value="−120k" label="Internet adds Q1’26 (CORE)" tone="danger" />
        <Stat value="−61k" label="YoY vs own Q1’25 (−59k)" tone="danger" />
        <Stat value="+41k" label="Rural CR adds Q1’26 (in the print)" tone="info" />
        <Stat value="−163k" label="Company CR adds Q1’26" tone="warning" />
      </Grid>
      <Text size="small" tone="tertiary">
        CORE-INFORMATION §5 / §8: Ex99.1 Q1 2026. Internet −120k is the Root B
        metric. Q4’25 restated customer relationships to include mobile-only —
        rural CR is not disclosed as Internet. Peer overlay (not CORE): CMCSA
        domestic resid. BB −65k Q1 / YoY +118k → slope gap −179k.
      </Text>

      <Callout tone="info" title="Operating mechanism under Root B (draft)">
        Not “light more rural passings.” CORE already has the rural program
        running (YE2025: $7.7B, 1.3M passings; Q1: 89k passings, +41k CR).
        Conversion split: core CR −204k in Q1. Improve the current broadband
        product on the core plant (offer, quality, overlap GTM) — not
        perception/IR, not more rural as the slope closer. Detail:
        chtr-broadband-expansion-diagnosis · chtr-rural-core-conversion.
      </Callout>

      <Stack gap={8}>
        <H2>Q1 2026 disclosed (CORE-INFORMATION)</H2>
        <Table
          headers={["Line", "Figure", "Use in Root B"]}
          columnAlign={["left", "right", "left"]}
          rowTone={["danger", "danger", "info", "warning", undefined, undefined]}
          rows={[
            [
              "Internet customers / Q1 adds",
              "29,560k ending · −120k",
              "The priced operating line (Root C gates recs on this print)",
            ],
            [
              "Internet adds Q1’25 (restated)",
              "−59k",
              "YoY slope −61k — Charter vs itself, before the peer overlay",
            ],
            [
              "Rural passings / CR Q1",
              "89k activated · +41k CR",
              "Expansion already inside the company print — not a future lever",
            ],
            [
              "Customer relationships Q1",
              "31,683k ending · −163k",
              "Company −163k = rural +41k + core −204k (trending subset)",
            ],
            [
              "Internet revenue Q1",
              "$5,852M (−1.3% YoY)",
              "Dollars down with volume; mobile +15.1% does not net against this",
            ],
            [
              "Mobile lines Q1 / AT&T·VZ FTTH overlap",
              "+368k · 27% / 16% of footprint",
              "Mobile is not the Root B metric. Overlap is the industry floor (A)",
            ],
          ]}
          striped
        />
        <Text size="small" tone="tertiary">
          YE2025 (CORE §4 / §8): Internet 29,680k (−393k residential Internet in
          2025); passings 58,399k; rural inception $7.7B / ~1.3M passings;
          FY2025 capex $11,659M of which rural initiative $2,208M. Q1 passings
          58,661k. MD&A: “competitive environment continued to challenge
          Internet customer growth.”
        </Text>
      </Stack>

      <Divider />

      <Stack gap={10}>
        <H2>Still live — not the base</H2>
        <Text tone="secondary">
          Floor or gate, not the operating root. CORE facts sit under all three.
        </Text>
        <Grid columns={2} gap={12}>
          <Card>
            <CardHeader trailing={<Pill tone="deleted">Root A · Industry</Pill>}>
              Structural share-shift to fiber / FWA
            </CardHeader>
            <CardBody>
              <Stack gap={6}>
                <Text size="small">
                  10-K: FTTH from AT&T and Verizon on ~27% and ~16% of the
                  footprint; FWA from national MNOs in Charter markets. Explains
                  peer losses and the sector multiple.
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
                  CORE Q1: Internet −120k and −1.3% $; mobile +368k / +15.1% $;
                  FCF $1.4B. Cash and mobile do not buy the multiple; the tape
                  prices Internet YoY surprise.
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
              "10-K: Spectrum Mobile is an MVNO on Verizon",
            ],
            [
              "HFC / DOCSIS credibility vs FTTH",
              "Rival mechanism under A",
              "Network evolution targeted end-2027 — CORE, not a Q1 slope closer",
            ],
            [
              "Buybacks / ‘undervalued’ / stage capital",
              "Decision architecture — DEMOTED",
              "Q1: 4.3M shares / $963M. Symptom after we know the operating problem",
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
              • Mix-adjusted Internet loss rates vs CMCSA on the non-rural base
              (still unrun — Root B falsifier)
            </Text>
            <Text size="small">
              • Win/loss reasons on the core plant (ops sampling — call-center
              caution)
            </Text>
            <Text size="small">
              • Price/promo gap vs FWA and fiber in overlapping zips
            </Text>
            <Text size="small">
              • Rural Internet vs rural CR (CORE discloses CR only)
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
              • That rural passings have fixed the slope — CORE + conversion
              say otherwise
            </Text>
            <Text size="small">
              • A recommendation — this page is the committed problem frame only
            </Text>
          </Stack>
        </Stack>
      </Grid>

      <Stack gap={8}>
        <H2>Ask the CEO — internal only, one answer each</H2>
        <Text size="small" tone="secondary">
          CORE-INFORMATION already gives the raw Charter print. These four are
          in the operating file. Ask one, stop, record the answer before the
          next.
        </Text>
        <Table
          headers={["Ask", "Direct response", "What it decides"]}
          columnAlign={["left", "left", "left"]}
          rows={[
            [
              "After DMA mix and fiber/FWA intensity, did Charter’s Q1 Internet loss rate still exceed Comcast’s?",
              "Yes or no",
              "Falsifier for Root B. Yes keeps the firm frame; no is mix, not GTM.",
            ],
            [
              "What percent of Q1 Internet disconnects sat in fiber-overbuild zips?",
              "A percent",
              "Whether the hole is overbuild geography or the rest of the plant.",
            ],
            [
              "In the worst-loss overlap zips, was Spectrum’s in-market promo above the offer the customer took?",
              "Yes or no",
              "Price/promo as the firm lever vs product or structure.",
            ],
            [
              "In the Q1 disconnect sample — not agent codes — what is the single largest reason?",
              "One named reason",
              "Binds the mechanism: fiber, FWA, price, WiFi/reliability, or moves.",
            ],
          ]}
          striped
        />
        <Text size="small" tone="tertiary">
          Do not re-ask −120k / +41k rural / −163k CR. If two people give
          different answers to the mix question, you have a data fight, not a
          diagnosis.
        </Text>
      </Stack>

      <Text size="small" tone="tertiary">
        Sources: PrimarySources/CORE-INFORMATION.md (§4–5, §8, §10, §11) ·
        chtr-industry-vs-firm-framestorm §4–5 · chtr-relative-performance
        (CMCSA overlay) · chtr-rural-core-conversion · diagnosis:
        chtr-broadband-expansion-diagnosis. Assignment anchor: end Q1 2026.
      </Text>
    </Stack>
  );
}
