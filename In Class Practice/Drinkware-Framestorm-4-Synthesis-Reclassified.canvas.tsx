import {
  Callout,
  Divider,
  Grid,
  H1,
  H2,
  H3,
  Pill,
  Row,
  Stack,
  Table,
  Text,
  useHostTheme,
} from "cursor/canvas";

const Bullet = ({ children }: { children: string }) => (
  <Text size="small">• {children}</Text>
);

const roleRows = [
  [
    <Stack gap={4}>
      <Text weight="semibold">Displacement of a vessel already owned</Text>
      <Text size="small" tone="tertiary">was: “Customer job” · rated Strongest</Text>
    </Stack>,
    <Pill active>Root frame</Pill>,
    <Text size="small">
      Survives as a candidate problem definition, but only in its sharpened form. “Which customer has an
      unresolved job?” is a container; “what makes someone displace or add to the bottle they already own at
      $35–$50?” is a claim that can be wrong.
    </Text>,
  ],
  [
    <Stack gap={4}>
      <Text weight="semibold">Founder-specific right-to-win</Text>
      <Text size="small" tone="tertiary">was: rated Strongest</Text>
    </Stack>,
    <Pill active>Root frame</Pill>,
    <Text size="small">
      Retained but narrowed. As originally written it absorbed channel, brand, IP, and acquisition cost, which
      makes it unfalsifiable. It earns root status only when it names the asset she holds that a competitor
      cannot buy or copy.
    </Text>,
  ],
  [
    <Stack gap={4}>
      <Text weight="semibold">Landed cost and duty stack</Text>
      <Text size="small" tone="tertiary">was: “Factory and port economics” · Essential diligence</Text>
    </Stack>,
    <Pill active>Hard constraint · sequence first</Pill>,
    <Text size="small">
      Upgraded. A China-origin insulated vessel now carries a duty stack in the mid-40% range against a
      $35–$50 shelf price. That can invalidate the venture independent of demand, and it is the cheapest thing
      on this list to resolve — one broker opinion and one factory quote.
    </Text>,
  ],
  [
    <Stack gap={4}>
      <Text weight="semibold">Replacement trigger</Text>
      <Text size="small" tone="tertiary">was: “Replacement market” · Very useful</Text>
    </Stack>,
    <Pill>Rival demand mechanism</Pill>,
    <Text size="small">
      Re-nested rather than demoted. It is not a peer of the displacement frame; it is the best-evidenced
      explanation of why displacement happens — hygiene, odor, leaks, loss. It also rests on the weakest
      source in the set, a vendor-commissioned survey, so it needs replication before it carries weight.
    </Text>,
  ],
  [
    <Stack gap={4}>
      <Text weight="semibold">Fashion and identity cycle</Text>
      <Text size="small" tone="tertiary">was: “Useful hypothesis”</Text>
    </Stack>,
    <Pill>Rival demand mechanism</Pill>,
    <Text size="small">
      Promoted to equal standing with the replacement trigger. The cycle evidence is at least as strong as the
      saturation evidence, and the two mechanisms contradict each other: one says buy the identity object, the
      other says replace the failed object. That conflict is what makes the pair worth testing.
    </Text>,
  ],
  [
    <Stack gap={4}>
      <Text weight="semibold">Trust in an unknown mouth-contact brand</Text>
      <Text size="small" tone="tertiary">split out of “Mouth-contact trust and compliance” · Gate, not frame</Text>
    </Stack>,
    <Pill>Rival demand mechanism</Pill>,
    <Text size="small">
      Promoted. Bundling this with paperwork was the error. Whether a shopper will pay $40 to drink daily from
      a brand they have never heard of is a demand question, and if the answer is no, it explains a launch
      failure that no compliance binder would have prevented.
    </Text>,
  ],
  [
    <Stack gap={4}>
      <Text weight="semibold">Compliance file and claims discipline</Text>
      <Text size="small" tone="tertiary">split out of “Mouth-contact trust and compliance”</Text>
    </Stack>,
    <Pill>Hard constraint · gate</Pill>,
    <Text size="small">
      Unchanged in role, now stated separately. Food-contact testing, Prop 65 exposure, and label claims are
      pass-or-fail conditions of selling at all. Passing confers no advantage, which is precisely why it is a
      gate and not a frame.
    </Text>,
  ],
  [
    <Stack gap={4}>
      <Text weight="semibold">Freedom to operate</Text>
      <Text size="small" tone="tertiary">split out of “Copy war” · Secondary screen</Text>
    </Stack>,
    <Pill>Hard constraint · gate</Pill>,
    <Text size="small">
      Upgraded from secondary. Whether her silhouette or lid infringes a live design patent is binary and
      answerable now, and an adverse answer stops the launch. Incumbents in this category litigate, so this is
      not a theoretical risk.
    </Text>,
  ],
  [
    <Stack gap={4}>
      <Text weight="semibold">Defensibility and time to copy</Text>
      <Text size="small" tone="tertiary">split out of “Copy war”</Text>
    </Stack>,
    <Pill>Sub-branch of right-to-win</Pill>,
    <Text size="small">
      The other half of the copy war is not a gate at all. How fast her differentiator gets duplicated is a
      question about the durability of her advantage, which belongs inside the right-to-win frame rather than
      beside it.
    </Text>,
  ],
  [
    <Stack gap={4}>
      <Text weight="semibold">Retailer and planogram power</Text>
      <Text size="small" tone="tertiary">was: “Conditional”</Text>
    </Stack>,
    <Pill>Sub-branch · contingent on channel</Pill>,
    <Text size="small">
      Explicitly nested. It becomes decisive only if wholesale retail is the route, and that choice is itself
      an open question one level up. Left standing alone, it quietly eliminates direct-to-consumer,
      marketplace, business-to-business, and licensing paths the case never ruled out.
    </Text>,
  ],
  [
    <Stack gap={4}>
      <Text weight="semibold">Staged capital commitment</Text>
      <Text size="small" tone="tertiary">was: “Capital allocation” · rated Strongest</Text>
    </Stack>,
    <Pill>Decision architecture · not a diagnosis</Pill>,
    <Text size="small">
      Demoted, and this is the largest change. “Stage your bets and predefine kill thresholds” is sound advice
      that would be equally true of any seed-funded venture in any category, which means it discriminates
      nothing about her situation. It describes how to act once we know where the problem is.
    </Text>,
  ],
];

const recommendedRows = [
  [
    <Stack gap={5}>
      <Text weight="semibold">1 · The problem is in the cupboard</Text>
      <Text size="small">
        What makes a specific customer displace, or add to, the insulated vessel they already own at
        $35–$50 — and is that trigger frequent and painful enough to build a business on?
      </Text>
    </Stack>,
    <Stack gap={4}>
      <Bullet>Widespread ownership means category participation is not available demand.</Bullet>
      <Bullet>The purchase is triggered by an event or an identity, not by a decision to start hydrating.</Bullet>
      <Bullet>Having built the product is not evidence that anyone needs it.</Bullet>
    </Stack>,
    <Stack gap={4}>
      <Bullet>Installed base per person and stated trigger for the last purchase</Bullet>
      <Bullet>Complaint and warranty incidence by failure mode</Bullet>
      <Bullet>Blind preference and switching against named alternatives</Bullet>
      <Bullet>Unaided willingness to pay at $35, $40, and $50</Bullet>
      <Bullet>Replacement, additional-unit, and gifting shares of purchases</Bullet>
    </Stack>,
  ],
  [
    <Stack gap={5}>
      <Text weight="semibold">2 · The problem is that she is nobody yet</Text>
      <Text size="small">
        What does she hold that an incumbent cannot buy or copy within a season, and through which beachhead
        does it convert into customer access?
      </Text>
    </Stack>,
    <Stack gap={4}>
      <Bullet>A market can be attractive and still be closed to this entrant.</Bullet>
      <Bullet>Insulation is commodity; advantage must come from IP, audience, meaning, or privileged access.</Bullet>
      <Bullet>No channel should be presumed before the routes are compared.</Bullet>
    </Stack>,
    <Stack gap={4}>
      <Bullet>The specific proprietary or privileged asset, named</Bullet>
      <Bullet>Time to copy and price gap of the nearest dupe</Bullet>
      <Bullet>Acquisition cost, conversion, and reorder rate by route</Bullet>
      <Bullet>Organic versus paid demand</Bullet>
      <Bullet>Unknown-brand trust penalty for a mouth-contact good</Bullet>
    </Stack>,
  ],
  [
    <Stack gap={5}>
      <Text weight="semibold">3 · The problem is decided before the market sees it</Text>
      <Text size="small">
        Can a compliant, non-infringing unit be landed at a cost and cash cycle that leaves a viable margin at
        $35–$50 — and if not, does the demand question matter at all?
      </Text>
    </Stack>,
    <Stack gap={4}>
      <Bullet>The binding constraint may be duty, minimum order quantity, and working capital rather than interest.</Bullet>
      <Bullet>Trade policy is a live variable that moves faster than a pricing decision.</Bullet>
      <Bullet>Compliance and freedom to operate are pass-fail conditions, not marketing problems.</Bullet>
    </Stack>,
    <Stack gap={4}>
      <Bullet>Landed cost by origin, decomposed to duty and freight</Bullet>
      <Bullet>Classification and total duty rate confirmed by a broker</Bullet>
      <Bullet>Contribution margin at each price after channel fees and promotion</Bullet>
      <Bullet>Minimum order quantity, cash cycle, and runway consumed by one order</Bullet>
      <Bullet>Freedom-to-operate opinion and batch-level test results</Bullet>
    </Stack>,
  ],
];

export default function PremiumDrinkwareFramestormSynthesis() {
  const theme = useHostTheme();

  return (
    <Stack
      gap={20}
      style={{
        padding: 24,
        maxWidth: 1320,
        margin: "0 auto",
        background: theme.bg.editor,
        color: theme.text.primary,
      }}
    >
      <Stack gap={8}>
        <Row gap={8} align="center" wrap>
          <Pill active>Reclassified</Pill>
          <Text size="small" tone="tertiary">
            Three independent drafts assessed against the case facts · September 8, 2026
          </Text>
        </Row>
        <H1>Which framings actually fit the case, and what job each one does</H1>
        <Text tone="secondary">
          The client has a product and seed funding and no market analysis. The question is not which
          perspective is cleverest but which could be the binding problem, which is a testable explanation
          underneath it, and which is a condition she must satisfy regardless of what the answer turns out to
          be.
        </Text>
      </Stack>

      <Callout tone="warning" title="Two defects in my previous assessment">
        The old “Fit” column mixed two incompatible dimensions — how good a perspective is, and what job it
        does — so “Strongest” and “Gate, not frame” were not comparable ratings. Worse, it rated exactly the
        three frames I had already chosen as the Strongest three, which is post-hoc justification rather than
        assessment. The reclassification below scores one dimension only: role in the diagnosis.
      </Callout>

      <Grid columns={4} gap={16} align="start">
        <Stack gap={5}>
          <H3>Root frame</H3>
          <Text size="small">
            Could be the actual problem. Names a location where the venture fails, and could be shown wrong.
          </Text>
        </Stack>
        <Stack gap={5}>
          <H3>Rival mechanism</H3>
          <Text size="small">
            Explains why a root frame would be true. Competes with the other mechanisms; they should not all
            survive.
          </Text>
        </Stack>
        <Stack gap={5}>
          <H3>Hard constraint</H3>
          <Text size="small">
            Pass or fail. Failure ends the venture; passing confers no advantage. Belongs in the work plan.
          </Text>
        </Stack>
        <Stack gap={5}>
          <H3>Sub-branch</H3>
          <Text size="small">
            Becomes decisive only after a prior choice is made. Dangerous when left standing alone.
          </Text>
        </Stack>
      </Grid>

      <Divider />

      <Stack gap={10}>
        <H2>Reclassification of the nine perspectives</H2>
        <Table
          headers={["Perspective", "Role", "Why this role, and what changed"]}
          rows={roleRows}
          rowTone={[
            "info",
            "info",
            "danger",
            "neutral",
            "neutral",
            "neutral",
            "danger",
            "danger",
            "warning",
            "warning",
            "success",
          ]}
          columnAlign={["left", "left", "left"]}
          striped
          stickyHeader
          style={{ maxHeight: 700 }}
        />
        <Text size="small" tone="tertiary">
          Nine perspectives produce eleven rows because the original set was not mutually exclusive: “copy war”
          was doing two jobs (a legal gate and a durability-of-advantage question) and “mouth-contact” was doing
          two (a compliance gate and a demand hypothesis). Both are split here. Ordering is by role, then by
          how early the work should be sequenced.
        </Text>
      </Stack>

      <Divider />

      <Stack gap={10}>
        <H2>Revised three-frame submission</H2>
        <Text tone="secondary">
          Staged capital commitment drops out of the framing and moves to the recommendation, where it belongs.
          The cost-structure perspective takes its place, because it is the one candidate that can end the
          venture on its own and the one we can resolve fastest.
        </Text>
        <Table
          headers={["Framing", "Underlying assumptions to test", "What it would make us measure"]}
          rows={recommendedRows}
          rowTone={["info", "info", "danger"]}
          striped
          stickyHeader
          style={{ maxHeight: 700 }}
        />
      </Stack>

      <Callout tone="warning" title="The critique that still applies">
        Cupboard, credibility, and cost structure can still be read as a desirability–access–viability
        checklist, and if we present them that way we will have accepted her frame with extra steps. They are
        rival claims about where the binding constraint sits. The research design should ask which one fails
        first, not tick all three.
      </Callout>

      <Stack gap={7}>
        <H2>Sequencing implied by the reclassification</H2>
        <Text>
          Run the hard constraints first, out of order of intellectual interest. A customs classification, a
          factory quote, a freedom-to-operate search, and a batch test are days of work and can each close the
          question entirely. There is no reason to spend weeks on consumer research that a duty rate would have
          made irrelevant.
        </Text>
        <Text>
          Then test the demand mechanisms against each other. The replacement trigger and the identity cycle
          predict different products, different pricing, and different marketing, so design the research to
          separate them rather than to confirm either.
        </Text>
        <Text>
          Only then commit capital in stages, with the kill thresholds written down in advance. That was always
          good practice; it was never a diagnosis.
        </Text>
      </Stack>

      <Callout tone="info" title="Best single synthesis question">
        Which of the three — a customer with no reason to switch, a founder with no defensible asset, or a unit
        that cannot be landed profitably at $35–$50 — fails first, and what is the cheapest test that would
        tell us?
      </Callout>
    </Stack>
  );
}
