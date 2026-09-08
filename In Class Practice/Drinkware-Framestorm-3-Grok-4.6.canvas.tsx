import {
  Callout,
  Divider,
  Grid,
  H1,
  H2,
  H3,
  Link,
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

const frameRows = [
  [
    <Stack gap={6}>
      <Text weight="semibold">1 · The buyer is a retailer, not a drinker</Text>
      <Text size="small">
        Can she win a finite planogram, Amazon search slot, or exclusive calendar — or will the people who
        actually allocate shelf space never give her a place to be chosen?
      </Text>
    </Stack>,
    <Stack gap={5}>
      <Bullet>Assumes the scarce resource is retail and marketplace real estate, not latent consumer desire.</Bullet>
      <Bullet>Assumes Target, Dick’s, REI, and Amazon buyers optimize assortment as a knapsack: every SKU she wants displaces a proven one.</Bullet>
      <Bullet>Assumes incumbents already occupy the “event” calendar with retailer-exclusive drops, so a new brand arrives as residual fill, not as a destination.</Bullet>
      <Bullet>Assumes a $35–$50 unknown SKU must clear a velocity hurdle before it is reordered, and that first-order failure is fatal.</Bullet>
    </Stack>,
    <Stack gap={5}>
      <Bullet>Share of category facings, endcaps, and exclusive SKUs by retailer and by brand</Bullet>
      <Bullet>Buyer scorecards: minimum advertised price, on-time fill rate, return rate, and units per store per week to keep the slot</Bullet>
      <Bullet>Lead time from first buyer meeting to national planogram reset</Bullet>
      <Bullet>Amazon share of search, review volume, and Buy Box for her price band</Bullet>
      <Bullet>Chargebacks, markdown allowances, and slotting or co-op dollars required to enter</Bullet>
      <Bullet>Probability a first purchase order is reordered versus remaindered</Bullet>
    </Stack>,
  ],
  [
    <Stack gap={6}>
      <Text weight="semibold">2 · The category is a copy war with a legal perimeter</Text>
      <Text size="small">
        If she looks enough like a winner to sell at $35–$50, can she survive being copied downward and
        sued sideways — and does she own anything that cannot be litigated or knocked off?
      </Text>
    </Stack>,
    <Stack gap={5}>
      <Bullet>Assumes vacuum insulation is a commodity; the fight is over silhouettes, lids, names, and trade dress.</Bullet>
      <Bullet>Assumes incumbents now use design patents and trade-dress suits as a competitive weapon, not just as protection.</Bullet>
      <Bullet>Assumes marketplace listings at 70–85% below branded prices set the consumer’s reference price even if she never matches it.</Bullet>
      <Bullet>Assumes her seed round cannot fund both a launch and a two-year IP fight.</Bullet>
    </Stack>,
    <Stack gap={5}>
      <Bullet>Freedom-to-operate: design patents, utility patents, and trade dress overlapping her silhouette and lid</Bullet>
      <Bullet>Time-to-copy and price gap of the closest Amazon / Temu / discounter analogue</Bullet>
      <Bullet>Share of marketplace offers that are unbranded or private-label versus named brands</Bullet>
      <Bullet>Incumbent litigation cadence and typical cost and duration of a design-patent action</Bullet>
      <Bullet>Whether her claimed differentiator is ornamental (easy to copy or to sue over) or functional and novel</Bullet>
      <Bullet>Brand-confusion risk: would an ordinary observer place her next to a protected Quencher-like form?</Bullet>
    </Stack>,
  ],
  [
    <Stack gap={6}>
      <Text weight="semibold">3 · This is a mouth-contact product sold by a stranger</Text>
      <Text size="small">
        Will a US shopper, a retailer compliance desk, or a California plaintiff’s lawyer treat an unknown
        $40 vessel as safe enough to drink from — and if not, is “market entry” the wrong first problem?
      </Text>
    </Stack>,
    <Stack gap={5}>
      <Bullet>Assumes drinkware is closer to food than to apparel: the customer puts it to their lips daily.</Bullet>
      <Bullet>Assumes brand names in this category function as a hygiene and heavy-metal proxy, not only as style.</Bullet>
      <Bullet>Assumes the 2024 lead-in-solder scare trained shoppers and retailers to ask “who made this?” before “does it keep ice?”</Bullet>
      <Bullet>Assumes the gate is documentation and claims discipline (FDA food-contact, Prop 65, BPA-free, batch tests), not a marketing story.</Bullet>
    </Stack>,
    <Stack gap={5}>
      <Bullet>Willingness to buy an unaided unknown brand for a mouth-contact good versus a known brand at the same price</Bullet>
      <Bullet>Return, odor, leak, and “metallic taste” complaint rates by brand age and review volume</Bullet>
      <Bullet>Retailer and Amazon documentation checklists actually required to list or reset</Bullet>
      <Bullet>Batch-level third-party tests: 21 CFR food-contact, Prop 65 lead/cadmium, lid and straw polymers</Bullet>
      <Bullet>Claim risk: “lead-free,” “non-toxic,” “safe for kids” versus lab support</Bullet>
      <Bullet>Insurance, recall, and 60-day-notice exposure relative to seed capital</Bullet>
    </Stack>,
  ],
];

export default function PremiumDrinkwareFramestormGrok() {
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
          <Pill active>Draft 1</Pill>
          <Pill>Independent run</Pill>
          <Text size="small" tone="tertiary">
            Skeptical strategy partner · market evidence used · nothing concluded
          </Text>
        </Row>
        <H1>Three rival framings of the premium drinkware decision</H1>
        <Text tone="secondary">
          She has framed a market-entry question. These three frames locate the real problem in three different
          rooms: the buyer’s planogram, the courtroom and the copy factory, and the compliance file for a product
          people put in their mouths. If all three pointed at “is the category attractive,” the frame would
          already have been accepted.
        </Text>
      </Stack>

      <Callout tone="warning" title="The frame I am refusing to accept">
        Sizing the US premium insulated drinkware market at $35–$50 would treat demand as the unknown. A
        category can be large and still be closed to her if she cannot get a facing, cannot defend a form
        factor, or cannot be trusted as a food-contact brand.
      </Callout>

      <Stack gap={10}>
        <H2>Framestorming matrix</H2>
        <Table
          headers={[
            "Framing (stated as a decision question)",
            "Underlying assumptions the frame smuggles in",
            "What it would make us measure",
          ]}
          rows={frameRows}
          rowTone={["info", "warning", "danger"]}
          striped
          stickyHeader
          style={{ maxHeight: 680 }}
        />
        <Text size="small" tone="tertiary">
          Draft as of September 8, 2026. Measures are proposed tests, not findings. Frame 1 is a channel-power
          problem, Frame 2 is a property-rights problem, Frame 3 is a permission-to-ingest problem. They can
          all be true at once, but they would send three different workstreams first.
        </Text>
      </Stack>

      <Divider />

      <Stack gap={10}>
        <H2>Market evidence that made these frames worth holding</H2>
        <Grid columns={3} gap={16} align="start">
          <Stack gap={6}>
            <H3>Shelf is allocated, not earned by desire</H3>
            <Text size="small">
              Target treats planograms as a portfolio optimization problem across a national store network —
              a knapsack of facings, not an open catalog. Stanley still fills that calendar with
              Target-only collections (including 2026 seasonal drops in the $21–$45 band), which occupy the
              “destination” role a new brand would need. If the real customer is the merchant, consumer
              research is the second interview, not the first.
            </Text>
            <Text size="small" tone="tertiary">
              Supports Frame 1 · moderate confidence on the mechanism; exact facing shares need Circana or
              retailer sell-through
            </Text>
          </Stack>
          <Stack gap={6}>
            <H3>Copying is the strategy, suing is the moat</H3>
            <Text size="small">
              In November 2025, Stanley’s owner sued Five Below over alleged Quencher and IceFlow design-patent
              and trade-dress copies sold as cheap dupes. BruMate sued Corkcicle the same year over a leak-proof
              lid patent. A marketplace scan of US insulated-bottle offers found about 40 brands and 1,400
              listings around an average price of $38 — her exact band — with a middling 3.25 average rating.
              Industry reports put unbranded and private-label product 70–85% below comparable branded prices.
            </Text>
            <Text size="small" tone="tertiary">
              Supports Frame 2 · high confidence on litigation as a tactic; price-gap percents are
              vendor-research estimates
            </Text>
          </Stack>
          <Stack gap={6}>
            <H3>Unknown + mouth-contact is a different sale</H3>
            <Text size="small">
              Vacuum flasks are food-contact articles under FDA 21 CFR; California Prop 65 exposure for this
              category is typically coatings, inks, lids, and vacuum-seal solder rather than the steel body.
              Retailers and Amazon compliance desks now ask for batch-level tests, and a Prop 65 fight is
              routinely described by trade sources as a five-figure settlement risk per SKU. After the
              2024 lead-solder controversy around major tumbler brands, “who stands behind this” is part of
              the product.
            </Text>
            <Text size="small" tone="tertiary">
              Supports Frame 3 · high confidence on the regulatory file; consumer-trust haircut vs. named
              brands is a hypothesis until tested
            </Text>
          </Stack>
        </Grid>
      </Stack>

      <Divider />

      <Stack gap={10}>
        <H2>Frames I am keeping on the table, not discarding</H2>
        <Grid columns={3} gap={16} align="start">
          <Stack gap={6}>
            <Text weight="semibold" size="small">
              The real buyer may be a procurement office
            </Text>
            <Text size="small" tone="secondary">
              Corporate gifting, hospitality, gyms, and imprint programs buy vessels as branded merchandise.
              That would make her problem a B2B spec-and-MOQ sale, not a consumer brand launch — and it would
              invert which capabilities matter.
            </Text>
          </Stack>
          <Stack gap={6}>
            <Text weight="semibold" size="small">
              She may already have answered “enter”
            </Text>
            <Text size="small" tone="secondary">
              A finished product plus seed funding often means the decision under study is how to spend the
              rest of the money, not whether the market wants the object. That is a commitment-bias problem
              disguised as analysis.
            </Text>
          </Stack>
          <Stack gap={6}>
            <Text weight="semibold" size="small">
              Returns and 3PL may be the P&amp;L
            </Text>
            <Text size="small" tone="secondary">
              Drinkware fails in lids, leaks, dented powder coat, and “it tasted like metal.” If those rates
              look like apparel DTC, a $40 AOV cannot fund the reverse-logistics machine. That is an operations
              frame, not a demand frame.
            </Text>
          </Stack>
        </Grid>
      </Stack>

      <Stack gap={6}>
        <H2>Sources</H2>
        <Link href="https://hdl.handle.net/1721.1/155989">
          MIT / Target · An analytical framework for planogram portfolio optimization
        </Link>
        <Link href="https://particle.news/story/stanley-drops-target-exclusive-tile-collection">
          Particle · Stanley Target-exclusive Tile Collection pricing and assortment
        </Link>
        <Link href="https://www.reuters.com/legal/litigation/stanley-cup-maker-sues-five-below-allegedly-ripping-off-design-2025-11-07/">
          Reuters · Pacific Market International v. Five Below (Nov 7, 2025)
        </Link>
        <Link href="https://www.law.com/dailybusinessreview/2025/09/02/brumate-brings-bottle-battle-against-competitor-corkcicle-to-federal-court/">
          Law.com · BruMate v. Corkcicle lid-patent suit (Aug 2025)
        </Link>
        <Link href="https://www.indexbox.io/store/united-states-insulated-water-bottle-marketplace-brand-report/">
          IndexBox · US insulated water bottle marketplace brand analysis (data to Sep 4, 2025)
        </Link>
        <Link href="https://insulflaskio.com/prop-65-compliance-for-stainless-steel-tumblers-what-us-brands-need-to-prepare/">
          Industry compliance note · Prop 65 vs FDA food-contact files for stainless tumblers
        </Link>
      </Stack>

      <Callout tone="info" title="What I would ask her before choosing a frame">
        Who has already said no? A retailer buyer, a factory that would not tool a unique lid, a lab that would
        not certify the solder, or no one — because she has not asked anyone who can block her except a
        hypothetical consumer?
      </Callout>
    </Stack>
  );
}
