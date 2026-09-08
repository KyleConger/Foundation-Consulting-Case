import {
  Callout,
  Divider,
  H1,
  H2,
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

const rows = [
  [
    <Stack gap={6}>
      <Text weight="semibold">1 · Customer job, not category entry</Text>
      <Text size="small">
        Which specific customer and use occasion has an unresolved problem important enough to make this
        product worth switching to at $35–$50?
      </Text>
    </Stack>,
    <Stack gap={5}>
      <Bullet>“Premium insulated drinkware” is a category description, not a customer problem.</Bullet>
      <Bullet>Basic insulation is easy to copy; the unmet job may involve lid design, mobility, identity, safety, cleaning, or gifting.</Bullet>
      <Bullet>Recent category cooling suggests prior growth cannot be assumed to continue.</Bullet>
    </Stack>,
    <Stack gap={5}>
      <Bullet>Problem severity and frequency by customer/use occasion</Bullet>
      <Bullet>Observed workarounds and switching triggers</Bullet>
      <Bullet>Blind preference against named alternatives</Bullet>
      <Bullet>Unaided willingness to pay at $35, $40, and $50</Bullet>
      <Bullet>Trial-to-repeat, retention, and referral behavior</Bullet>
    </Stack>,
  ],
  [
    <Stack gap={6}>
      <Text weight="semibold">2 · Right-to-win, not product quality</Text>
      <Text size="small">
        Can an unknown entrant earn attention, trust, and distribution in a crowded category where incumbents
        already own distinctive positions?
      </Text>
    </Stack>,
    <Stack gap={5}>
      <Bullet>The product may be good enough; the scarce asset may be customer access.</Bullet>
      <Bullet>Leading brands compete through functional innovation, cultural relevance, communities, retail reach, and product drops—not insulation alone.</Bullet>
      <Bullet>Without a privileged audience or channel, paid acquisition could erase otherwise attractive margins.</Bullet>
    </Stack>,
    <Stack gap={5}>
      <Bullet>Founder’s proprietary advantage: IP, community, partnerships, channel, or story</Bullet>
      <Bullet>Customer-acquisition cost and conversion by channel</Bullet>
      <Bullet>Organic versus paid demand and creator productivity</Bullet>
      <Bullet>Retailer interest, shelf access, sell-through, and reorder rate</Bullet>
      <Bullet>Brand recall, trust, referral, and repeat purchase</Bullet>
    </Stack>,
  ],
  [
    <Stack gap={6}>
      <Text weight="semibold">3 · Capital allocation under uncertainty</Text>
      <Text size="small">
        Should she fund a broad US launch now, or preserve seed capital through staged tests, a narrower beachhead,
        another commercialization model, or no entry?
      </Text>
    </Stack>,
    <Stack gap={5}>
      <Bullet>“Enter” is not binary: preorder, niche DTC, B2B gifting, licensing, retail partnership, delay, and exit are alternatives.</Bullet>
      <Bullet>Inventory, tariffs, promotions, and launch spending create downside before demand is proven.</Bullet>
      <Bullet>The first return on seed capital may be decisive learning rather than revenue growth.</Bullet>
    </Stack>,
    <Stack gap={5}>
      <Bullet>Contribution margin by SKU and channel under tariff/promotion scenarios</Bullet>
      <Bullet>MOQ, inventory turns, cash-conversion cycle, burn, and runway</Bullet>
      <Bullet>Cost, speed, and decision value of each experiment</Bullet>
      <Bullet>Capital at risk and recoverability by entry path</Bullet>
      <Bullet>Predefined kill, continue, and scale thresholds</Bullet>
    </Stack>,
  ],
];

export default function PremiumDrinkwareFramestorm() {
  const theme = useHostTheme();

  return (
    <Stack
      gap={18}
      style={{
        padding: 24,
        maxWidth: 1280,
        margin: "0 auto",
        background: theme.bg.editor,
        color: theme.text.primary,
      }}
    >
      <Stack gap={8}>
        <Row gap={8} align="center" wrap>
          <Pill tone="info" active>Draft 1</Pill>
          <Pill tone="neutral">Thought-partner pressure test</Pill>
          <Text size="small" tone="tertiary">Market evidence used; conclusions remain provisional</Text>
        </Row>
        <H1>Three alternative framings of the premium drinkware decision</H1>
        <Text tone="secondary">
          The presenting question is whether to enter the US market. These frames challenge three different
          premises: that a meaningful customer problem exists, that this founder can win access to customers,
          and that a broad launch is the best use of scarce capital.
        </Text>
      </Stack>

      <Callout tone="warning" title="Skeptical partner challenge">
        Starting with market size would silently accept the client’s frame. A large category does not establish
        unmet demand, a right-to-win, or investable startup economics.
      </Callout>

      <Stack gap={10}>
        <H2>Draft framestorming matrix</H2>
        <Table
          headers={["Framing", "Underlying assumptions to test", "What it would make us measure"]}
          rows={rows}
          rowTone={["info", "neutral", "warning"]}
          striped
          stickyHeader
          style={{ maxHeight: 650 }}
        />
        <Text size="small" tone="tertiary">
          Research frame as of September 8, 2026. Measures are proposed tests, not asserted results.
        </Text>
      </Stack>

      <Divider />

      <Stack gap={8}>
        <H2>Market signals shaping—but not deciding—the draft</H2>
        <Text>
          • Circana data cited by Modern Retail show sporting-goods sales of bottles and insulated containers
          declined year over year each month from September 2024 through February 2025; category growth slowed
          from 38% in 2023 to 14% in 2024.
        </Text>
        <Text>
          • YETI reported 2025 drinkware sales of $1.086 billion, down 1%; US weakness was associated with a
          promotional market, cautious wholesale buying, and supply constraints. Companywide gross margin was
          57.4%, illustrating attractive gross economics at scale but not startup-level profitability.
        </Text>
        <Text>
          • Hydro Flask’s owner cited continued competition, softer consumer demand, and lower retailer
          replenishment, while noting stronger response to new launches. This supports testing specific product
          innovation rather than treating category softness as universal.
        </Text>
      </Stack>

      <Stack gap={5}>
        <H2>Sources for this iteration</H2>
        <Link href="https://www.modernretail.co/operations/stanley-shares-its-playbook-for-growth-as-sales-overall-cool-in-the-once-booming-drinkware-sector/">
          Modern Retail · Stanley’s growth playbook as drinkware sales cool
        </Link>
        <Link href="https://investors.yeti.com/news/news-details/2026/YETI-ReportsFourth-Quarter-and-Full-Year-2025-Results-Provides-Full-Year-2026-Outlook/default.aspx">
          YETI · FY2025 results and FY2026 outlook
        </Link>
        <Link href="https://www.outdoorsportswire.com/hydro-flask-tops-plan-and-osprey-posts-solid-growth-in-fiscal-fourth-quarter/">
          Outdoor Sportswire · Hydro Flask fiscal Q4 update
        </Link>
      </Stack>

      <Callout tone="info" title="Best synthesis question for the next iteration">
        What must be true for this founder to earn the right to commit scarce capital to a scalable US launch—and
        which assumption can we disprove fastest and cheapest?
      </Callout>
    </Stack>
  );
}
