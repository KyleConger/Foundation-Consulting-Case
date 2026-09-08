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
      <Text weight="semibold">A · She is entering the fashion business, not the drinkware business</Text>
      <Text size="small">
        Should she build a trend-cycle brand whose unit of competition is the colorway, drop, and collectibility
        of an identity object — and is she funded and built to survive a cycle turn?
      </Text>
    </Stack>,
    <Stack gap={5}>
      <Bullet>Assumes purchase is driven by self-expression and social signaling, not thirst or insulation.</Bullet>
      <Bullet>Assumes the winning capability is cultural timing, drop cadence, and creator distribution — a merchandising skill, not a manufacturing one.</Bullet>
      <Bullet>Assumes demand is inherently perishable: what a trend gives, it takes back, and dupes compress the window.</Bullet>
      <Bullet>Assumes the $35–$50 band buys style permission rather than performance.</Bullet>
    </Stack>,
    <Stack gap={5}>
      <Bullet>Trend position: search and social interest curve for the category and for incumbents, by month</Bullet>
      <Bullet>Sell-through velocity and markdown rate per colorway and per drop</Bullet>
      <Bullet>Share of purchases that are second, third, or fifth units in a household</Bullet>
      <Bullet>Dupe price gap and time-to-copy after a design launch</Bullet>
      <Bullet>Design-to-shelf lead time versus incumbents’ drop cadence</Bullet>
      <Bullet>Age of inventory and obsolescence write-down risk at cycle turn</Bullet>
    </Stack>,
  ],
  [
    <Stack gap={6}>
      <Text weight="semibold">B · There is no acquisition market left, only a replacement market</Text>
      <Text size="small">
        Given near-universal ownership, what specific failure of the bottle already in the customer’s cupboard
        would make her product the replacement — and is that failure frequent and painful enough to build on?
      </Text>
    </Stack>,
    <Stack gap={5}>
      <Bullet>Assumes the competitor is the customer’s existing bottle and packaged beverages, not the brands on the shelf next to hers.</Bullet>
      <Bullet>Assumes purchases are triggered by an event — odor, mold, leaking, loss, breakage, a lifestyle change, or a gift — not by a decision to start hydrating.</Bullet>
      <Bullet>Assumes the durable-goods promise is self-defeating: a product that lasts forever must be re-bought for non-durability reasons.</Bullet>
      <Bullet>Assumes she can name and design against one dominant failure mode.</Bullet>
    </Stack>,
    <Stack gap={5}>
      <Bullet>Installed base per household and per person, by segment</Bullet>
      <Bullet>Replacement interval and the stated trigger for the last replacement</Bullet>
      <Bullet>Incidence and severity of hygiene, cleaning, odor, leak, and lid-failure complaints in reviews and warranty claims</Bullet>
      <Bullet>Gifting share of category purchases and its seasonality</Bullet>
      <Bullet>Substitution rate to packaged beverages by occasion</Bullet>
      <Bullet>Measured performance of her product against the specific failure mode versus incumbents</Bullet>
    </Stack>,
  ],
  [
    <Stack gap={6}>
      <Text weight="semibold">C · The outcome is decided at the factory and the port, not in the market</Text>
      <Text size="small">
        Before demand is the question, can she land a compliant unit at a cost and cash cycle that leaves a
        viable margin at $35–$50 — and if not, does the market question even matter?
      </Text>
    </Stack>,
    <Stack gap={5}>
      <Bullet>Assumes the binding constraint is landed cost, duty exposure, and working capital, not customer interest.</Bullet>
      <Bullet>Assumes a vacuum-insulated steel vessel is a commodity manufacture, so cost position is inherited from sourcing decisions and scale she does not yet have.</Bullet>
      <Bullet>Assumes trade policy is a live variable, not a fixed input, and can move faster than a pricing decision.</Bullet>
      <Bullet>Assumes safety and compliance exposure — materials, lead, labeling, recalls — is a survival risk for an undercapitalized entrant.</Bullet>
    </Stack>,
    <Stack gap={5}>
      <Bullet>Landed cost per unit by origin country, decomposed into FOB, duty stack, freight, and fees</Bullet>
      <Bullet>Correct HTS classification and total duty rate, confirmed by a customs broker</Bullet>
      <Bullet>Factory minimum order quantity, lead time, tooling cost, and dual-sourcing options</Bullet>
      <Bullet>Contribution margin at $35, $40, and $50 after retailer or marketplace fees and promotions</Bullet>
      <Bullet>Cash-conversion cycle, inventory turns, and months of runway consumed by a first purchase order</Bullet>
      <Bullet>Compliance, testing, warranty, and product-liability cost per unit and defect rate</Bullet>
    </Stack>,
  ],
];

const reserveFrames = [
  {
    title: "The price band itself is the trap",
    body:
      "At $35–$50 she sits between viral premium brands with cultural reach and private-label or dupe product at half the price. The problem may be a positioning and price-architecture decision rather than an entry decision.",
  },
  {
    title: "Drinkware is not one market",
    body:
      "Bottles, tumblers, travel mugs, and cupholder-format vessels have different buyers, growth rates, and incumbents. Choosing the form factor may determine the outcome more than choosing to enter.",
  },
  {
    title: "The real question may be personal, not commercial",
    body:
      "With a product and seed money already committed, the decision she owns may be what she is building toward — an operating business, a brand asset for sale, or a licensing play — which changes what winning means.",
  },
];

export default function PremiumDrinkwareFramestormOpus() {
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
          The client has framed this as a market-entry question, which quietly assumes the market is the thing
          she needs to understand. These three frames deliberately conflict with one another: each locates her
          real problem in a different place — in the trend cycle, in the customer’s cupboard, and in the duty
          stack — and each would send us to measure different things first.
        </Text>
      </Stack>

      <Callout tone="warning" title="The frame I am refusing to accept">
        “Size the US premium drinkware market” is the request, not the problem. A market can be large, growing,
        and still be unenterable for this founder at this price with this capital. If all three of my frames
        pointed at demand, I would have accepted her frame and simply decorated it.
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
          Draft as of September 8, 2026. Measures are proposed tests, not findings. Frames A and B are rival
          explanations of the same purchase and should not both survive contact with data.
        </Text>
      </Stack>

      <Divider />

      <Stack gap={10}>
        <H2>Market evidence that made these frames worth holding</H2>
        <Grid columns={3} gap={16} align="start">
          <Stack gap={6}>
            <H3>Cycle risk is observable</H3>
            <Text size="small">
              Stanley went from roughly $73 million in revenue in 2019 to an estimated $750–800 million by
              2023–24, then saw US direct-to-consumer spend fall about 20% in 2025 with a volatile 2026, per
              Consumer Edge data cited by Modern Retail. Circana data cited by Modern Retail and Fast Company
              show sporting-goods sales of bottles and insulated containers declining year over year every
              month from September 2024 through February 2025, with full-year category growth slowing from 38%
              in 2023 to 14% in 2024.
            </Text>
            <Text size="small" tone="tertiary">Supports Frame A · moderate confidence, third-party estimates</Text>
          </Stack>
          <Stack gap={6}>
            <H3>The base is already saturated</H3>
            <Text size="small">
              A 2024 Statista survey of over 3,000 US adults reports 85% already own a reusable bottle, owning
              about four each, with 36% owning five or more; 51% replaced within a year and 40% cited odor or
              hygiene. Circana’s analyst attributed category softness partly to widespread availability and to
              consumers spending more on packaged energy and sports drinks.
            </Text>
            <Text size="small" tone="tertiary">
              Supports Frame B · low-to-moderate confidence, survey was commissioned by a bottle startup and
              needs independent replication
            </Text>
          </Stack>
          <Stack gap={6}>
            <H3>Duty stack is material</H3>
            <Text size="small">
              Insulated vessels classify under HTS 9617.00.1000 at roughly 7% most-favored-nation duty, plus a
              25% Section 301 tariff on Chinese-origin steel drinkware, plus the 12.5% Section 301 forced-labor
              duty that replaced the expired Section 122 surcharge on July 24, 2026 — a stack in the mid-40%
              range before fees. Incumbents felt it: YETI reported about $100 million in tariff cost and
              230 basis points of gross-margin pressure in fiscal 2025, and Helen of Troy guided to $60–70
              million gross unmitigated tariff impact while dual-sourcing away from China.
            </Text>
            <Text size="small" tone="tertiary">
              Supports Frame C · rate stack must be confirmed with a licensed customs broker before use in any
              pricing model
            </Text>
          </Stack>
        </Grid>
      </Stack>

      <Divider />

      <Stack gap={10}>
        <H2>Frames I am keeping on the table, not discarding</H2>
        <Grid columns={3} gap={16} align="start">
          {reserveFrames.map((frame) => (
            <div key={frame.title}>
              <Stack gap={6}>
                <Text weight="semibold" size="small">{frame.title}</Text>
                <Text size="small" tone="secondary">{frame.body}</Text>
              </Stack>
            </div>
          ))}
        </Grid>
      </Stack>

      <Stack gap={6}>
        <H2>Sources</H2>
        <Link href="https://www.modernretail.co/operations/brands-briefing-stanley-1913s-next-era-focuses-on-storage-international-growth-and-sports/">
          Modern Retail · Stanley 1913’s next era, with Consumer Edge DTC spend data
        </Link>
        <Link href="https://www.fastcompany.com/91503591/whats-next-for-stanley-after-quencher-craze">
          Fast Company · What’s next for Stanley after the Quencher craze, citing Circana
        </Link>
        <Link href="https://evervessel.com/blog/the-dirty-truth-about-reusable-water-bottles-in-2024-why-they-re-getting-replaced-fast/">
          Ever Vessel and Statista · 2024 survey of 3,000+ US adults on ownership and replacement
        </Link>
        <Link href="https://investors.yeti.com/news/news-details/2026/YETI-ReportsFourth-Quarter-and-Full-Year-2025-Results-Provides-Full-Year-2026-Outlook/default.aspx">
          YETI · Fiscal 2025 results and fiscal 2026 outlook
        </Link>
        <Link href="https://www.portless.com/blogs/section-301-tariffs-china">
          Portless · Section 301 changes for China effective July 24, 2026
        </Link>
        <Link href="https://www.chilltitan.com/us-tariffs-bottles-tumblers-hs-9617/">
          ChillTitan · HS 9617 duty stack and landed-cost walkthrough (vendor source, verify independently)
        </Link>
      </Stack>

      <Callout tone="info" title="What I would ask her before choosing a frame">
        Not “how big is the market,” but: what did you actually observe that made you believe someone would pay
        $40 for your bottle instead of using the one they own — and what would have to be true for you to walk
        away from this?
      </Callout>
    </Stack>
  );
}
