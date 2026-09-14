/**
 * Charter — macro industry vs firm framestorm (DRAFT).
 * Method: In Class Practice/Framestorming-Playbook.md
 * Prior canvases: chtr-issue-tree-charts, chtr-diagnostic-graphs
 * Assignment anchor: end Q1 2026; Q2 labeled as later public fact.
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
  H3,
  Pill,
  Row,
  Stack,
  Stat,
  Table,
  Text,
} from "cursor/canvas";

const Bullet = ({ children }: { children: string }) => (
  <Text size="small">• {children}</Text>
);

export default function ChtrIndustryVsFirmFramestorm() {
  return (
    <Stack gap={28}>
      <Stack gap={8}>
        <Row gap={8} align="center" wrap>
          <Pill tone="warning">DRAFT — framing, not a recommendation</Pill>
          <Pill tone="info">Week 2 industry + Week 3 problem definition</Pill>
        </Row>
        <H1>Industry problem or Charter problem?</H1>
        <Text tone="secondary">
          Macro competitive map for who attacks Spectrum products, then rival
          frames for where the binding constraint sits. Built from the
          Framestorming Playbook rooms method and the pass/fail already in the
          issue-tree and diagnostic canvases. Not a pitch answer.
        </Text>
      </Stack>

      <Callout tone="info" title="Working draft verdict (falsifiable)">
        Both — sequenced, not blended. Cable broadband is in a structural
        share-shift to fiber overbuild and FWA; that is in every peer’s
        multiple. Inside that wind, Charter’s Q1 2026 Internet print worsened
        YoY while Comcast’s improved YoY, and CHTR sold ~2× as hard as CMCSA
        on the same day. Treat “industry” as the floor and “Charter-relative
        trajectory + belief” as the gap a CEO strategy can still move.
      </Callout>

      <Grid columns={4} gap={12}>
        <Stat value="−120k" label="CHTR Internet Q1’26" tone="danger" />
        <Stat value="−65k" label="CMCSA resid. BB Q1’26" tone="warning" />
        <Stat value="−25.5%" label="CHTR Apr 24 close" tone="danger" />
        <Stat value="−13%" label="CMCSA same day" tone="warning" />
      </Grid>
      <Text size="small" tone="tertiary">
        CHTR Ex99.1 Q1 2026 · CMCSA Ex99.1 Q1 2026 (domestic residential
        broadband) · Yahoo/TIKR closes from issue-tree canvas. Different
        definitions (total Internet vs domestic residential broadband) — use
        for direction, not 1:1 subtraction.
      </Text>

      <Divider />

      <Stack gap={10}>
        <H2>1. What business Charter is in — and who attacks each product</H2>
        <Text>
          Opening diagnostic from class: what business is this company in?
          Broadband connectivity (HFC last-mile + MVNO mobile + declining
          video), not “a cable-TV company that also has internet.” Competitors
          are product-specific; “telecom” is too coarse.
        </Text>
        <Table
          headers={[
            "Spectrum product",
            "Profit / role",
            "Primary attackers",
            "Attacker’s offer",
            "Industry vs firm read",
          ]}
          columnAlign={["left", "left", "left", "left", "left"]}
          rows={[
            [
              "Internet (profit engine)",
              "~43% of FY25 revenue; priced variable in the multiple",
              "AT&T Fiber (~27% of CHTR footprint @100Mbps+); Verizon Fiber (~16%); T-Mobile / Verizon / AT&T FWA; LEO (Starlink; Kuiper later)",
              "FTTH multi-gig; 5G home box at lower promo; satellite in thin markets",
              "Industry structure. Relative loss rate vs CMCSA is the firm test.",
            ],
            [
              "Mobile (growth, lower margin)",
              "MVNO on Verizon; T-Mobile for Business from 2026",
              "AT&T, Verizon, T-Mobile postpaid; other MVNOs",
              "Converged wireless + home; own spectrum economics Charter resells",
              "Industry: growth is real. Firm: market will not net mobile vs Internet (diagnostic canvas).",
            ],
            [
              "Video",
              "Large, structurally declining (−9.4% FY25 $)",
              "YouTube TV, Hulu Live, Sling, Philo, DirecTV Stream, SVOD, FAST, piracy",
              "App bundles without truck roll; programmer leverage",
              "Industry secular. Not the Apr 2026 trigger.",
            ],
            [
              "Voice",
              "Secular decline (−12% customers FY25)",
              "Wireless + OTT calling",
              "Included in mobile plans",
              "Industry residual. Do not frame around it.",
            ],
            [
              "SMB / Enterprise",
              "Steadier; mid-market fiber growing",
              "Telco fiber, cloud, managed IT; Cox commercial fiber in deal",
              "Ethernet / SD-WAN / cloud",
              "Partial firm optionality via Cox commercial — sub-branch after broadband frame.",
            ],
            [
              "Advertising (Reach)",
              "Political-cycle volatile (−17.6% FY25)",
              "Digital / CTV platforms",
              "Targeted inventory",
              "Industry ad shift. Not trajectory-defining.",
            ],
          ]}
          striped
        />
        <Text size="small" tone="tertiary">
          Footprint overlap: CHTR FY2025 10-K. Revenue mix: CHTR FY2025 10-K /
          case background. FWA stock: VZ ~6.0M FWA end Q1’26; TMUS ~8.45M FWA
          end 2025 (Q1’26 FWA disclosure diluted — trade press ~470k adds).
        </Text>
      </Stack>

      <Stack gap={10}>
        <H2>2. Macro scoreboard — same wind, different YoY slope</H2>
        <Text>
          The clean industry-vs-firm test is not “is cable losing broadband?”
          (yes). It is “facing the same attackers, is Charter’s Internet
          trajectory worse than the closest peer?”
        </Text>
        <BarChart
          categories={["Q1 2025", "Q1 2026", "Q2 2025", "Q2 2026 (later)"]}
          series={[
            {
              name: "CHTR Internet net adds (000s)",
              data: [-59, -120, -116, -172],
              tone: "danger",
            },
            {
              name: "CMCSA domestic resid. BB net adds (000s)",
              data: [-183, -65, -201, -167],
              tone: "warning",
            },
          ]}
          beginAtZero={false}
          height={260}
          valueSuffix="k"
          referenceLines={[{ value: 0, label: "Zero", tone: "neutral" }]}
        />
        <Text size="small" tone="tertiary">
          Thousands · CHTR Ex99.1 / trending · CMCSA Ex99.1 Q1–Q2 2026.
          Definitions differ; YoY direction is the usable signal.
        </Text>

        <Grid columns={2} gap={16}>
          <Card>
            <CardHeader>Industry evidence (shared)</CardHeader>
            <CardBody>
              <Stack gap={6}>
                <Bullet>
                  Both cable majors still print negative broadband net adds in
                  2026.
                </Bullet>
                <Bullet>
                  Attackers are still adding: VZ FWA +214k in Q1’26 (to ~6.0M);
                  TMUS FWA accelerating vs +424k in Q1’25; AT&T Q2’26 advanced
                  connectivity +646k (367k fiber + 279k FWA).
                </Bullet>
                <Bullet>
                  Apr 24 2026: CMCSA already reported a beat and still fell
                  ~13% the day Charter printed — sector de-rate is real.
                </Bullet>
                <Bullet>
                  EV/EBITDA for CHTR and CMCSA sit in the same neighborhood
                  (~5.5–6x published Apr 2026) — not a 2-turn Charter-only
                  EBITDA discount (issue-tree chart 5).
                </Bullet>
              </Stack>
            </CardBody>
          </Card>
          <Card>
            <CardHeader>Charter-specific evidence (gap)</CardHeader>
            <CardBody>
              <Stack gap={6}>
                <Bullet>
                  Q1’26: CHTR Internet losses doubled YoY (−59k → −120k);
                  CMCSA residential BB losses improved YoY (−183k → −65k).
                </Bullet>
                <Bullet>
                  Same-day tape: CHTR −25.5% vs CMCSA −13% — extra Charter
                  gap on top of sector.
                </Bullet>
                <Bullet>
                  CHTR Internet revenue itself turned negative YoY in Q1’26;
                  price/mix stopped covering volume (issue-tree chart 3).
                </Bullet>
                <Bullet>
                  Mobile +368k lines in Q1’26 did not rescue the multiple —
                  history since the assignment trigger says connectivity netting
                  fails (diagnostic canvas).
                </Bullet>
              </Stack>
            </CardBody>
          </Card>
        </Grid>

        <Callout tone="warning" title="What this does not yet prove">
          We still lack a DMA-level split of fiber-overbuild vs FWA-heavy vs
          residual markets inside Charter’s footprint (diagnostic canvas flag).
          Until the Week 5 pack or public BDC overlays give that, “Charter
          underperforms peers” could partly be footprint mix, not only GTM.
          Flag as ESTIMATED causal attribution.
        </Callout>
      </Stack>

      <Divider />

      <Stack gap={10}>
        <H2>3. Rooms walk — relocate the problem before picking a frame</H2>
        <Text tone="secondary">
          Per playbook: frames come from changing where the problem lives, not
          from rewording “broadband competition.”
        </Text>
        <Table
          headers={["Room", "If the binding problem is here…", "Sounds like"]}
          columnAlign={["left", "left", "left"]}
          rows={[
            [
              "Installed base / cupboard",
              "Broadband is saturated; growth only comes from switches and moves",
              "Housing freeze + FWA/fiber switch offers — not ‘category growth’",
            ],
            [
              "Planogram / gatekeeper",
              "MDUs, landlords, and bulk deals allocate the last mile",
              "Community Solutions / right-of-entry share vs overbuilders",
            ],
            [
              "Factory / network",
              "HFC upgrade path is slower or less credible than FTTH/FWA cost",
              "DOCSIS 4.0 by end-2027 may blunt but not eliminate (10-K / class)",
            ],
            [
              "Returns dock / ops",
              "Churn and service failure exceed what promo price can fund",
              "Insourced ops as asset or as fixed-cost trap (~91.9k FTEs)",
            ],
            [
              "Cap table",
              "Leverage + buybacks + Cox/Liberty reset the claim on FCF",
              "~4.15x leverage; buybacks did not support price into Q1’26",
            ],
            [
              "Founder’s / CEO’s head",
              "‘Undervalued’ is already decided; analysis is ratification",
              "Instructor hypothesis — treat as claim to test, not fact",
            ],
            [
              "Attacker’s bundle",
              "Carriers converge wireless + home; Charter converges as reseller",
              "MVNO economics while the same carriers peel Internet homes",
            ],
          ]}
          striped
        />
      </Stack>

      <Stack gap={10}>
        <H2>4. Role classification — one dimension only</H2>
        <Text>
          Do not grade frames by quality. Rate by job in the diagnosis. Forced
          moves vs the issue-tree’s implicit framing: promote
          Charter-vs-Comcast relative trajectory to a root frame; demote
          “buybacks aren’t working / undervalued” from root to decision
          architecture / symptom.
        </Text>
        <Table
          headers={["Perspective", "Role", "Why that role"]}
          columnAlign={["left", "left", "left"]}
          rowTone={[
            "danger",
            "warning",
            undefined,
            undefined,
            undefined,
            "info",
            undefined,
            undefined,
            undefined,
          ]}
          rows={[
            [
              "Structural share-shift: fiber + FWA permanently reprice cable Internet relationships",
              "Root frame A (industry)",
              "Explains peer losses, sector multiple, and why ‘run harder’ may not restore growth. Falsified if cable Internet net adds turn sustainably positive without footprint retreat.",
            ],
            [
              "Relative underperformance: same wind, Charter’s YoY Internet slope is worse than Comcast’s",
              "Root frame B (firm) — PROMOTED",
              "Contradicts pure industry fatalism. Falsified if DMA-mix adjusted loss rates converge with CMCSA and the extra stock gap closes.",
            ],
            [
              "Installed-base / move drought (housing)",
              "Rival mechanism under A",
              "Explains industry gross-add weakness. Does not explain CHTR vs CMCSA YoY divergence alone.",
            ],
            [
              "Converged-attacker asymmetry (carriers own spectrum; Charter is MVNO)",
              "Rival mechanism under A/B",
              "Why attackers can grow FWA while defending wireless. Competes with ‘just price better’ as the fix.",
            ],
            [
              "HFC / DOCSIS credibility vs FTTH",
              "Rival mechanism under A",
              "Technology story the market may not believe even if upgrade spends. Competes with GTM/pricing as the firm gap.",
            ],
            [
              "Internet surprise / YoY acceleration is what the tape prices",
              "Hard constraint (gate for any rec)",
              "From issue-tree chart 6. A recommendation that does not change the Internet run-rate inside ~24 months fails the market lens — industry or firm.",
            ],
            [
              "Cox + Liberty close (scale, ownership, +debt)",
              "Hard constraint / sub-branch",
              "Binary on timing and leverage path. Passing confers no Internet inflection by itself.",
            ],
            [
              "Mobile / ‘connectivity’ as valuation fix",
              "Sub-branch — do not elevate",
              "Diagnostic canvas: market will not net mobile lines against Internet customers.",
            ],
            [
              "Buybacks failed; stock is undervalued; stage capital",
              "Decision architecture / symptom — DEMOTED",
              "Universality test: true of many de-rated cash compounders. Describes how to act or how Wall Street feels after we know where the operating problem is.",
            ],
          ]}
          striped
        />
      </Stack>

      <Stack gap={10}>
        <H2>5. Draft root frames — assumptions and what to measure</H2>
        <Text tone="secondary">
          Default playbook deliverable: framing / assumptions / measures. Strong
          frames conflict; research should find which fails first.
        </Text>

        <Card>
          <CardHeader trailing={<Pill tone="deleted">Root A · Industry</Pill>}>
            The problem is the category: cable Internet relationships are being
            permanently reallocated to fiber and FWA
          </CardHeader>
          <CardBody>
            <Grid columns={2} gap={16}>
              <Stack gap={6}>
                <H3>Underlying assumptions</H3>
                <Bullet>
                  Overbuild and FWA capacity keep expanding into Charter
                  passings through at least 2027–28.
                </Bullet>
                <Bullet>
                  Network evolution blunts but does not reverse share shift
                  (company’s own competitive language).
                </Bullet>
                <Bullet>
                  Housing stays soft enough that move-driven gross adds cannot
                  offset competitive losses.
                </Bullet>
                <Bullet>
                  Any single MSO faces the same physics; peer gaps are noise.
                </Bullet>
              </Stack>
              <Stack gap={6}>
                <H3>What it would make us measure</H3>
                <Bullet>
                  Competitive overlap by DMA: AT&T/VZ fiber %, FWA win rates
                </Bullet>
                <Bullet>
                  Industry cable Internet net adds vs FWA+fiber net adds (share
                  shift identity)
                </Bullet>
                <Bullet>
                  Gross adds vs churn; move-rate correlation to signups
                </Bullet>
                <Bullet>
                  Post-2027 FCF inflection if Internet relationships keep falling
                </Bullet>
              </Stack>
            </Grid>
          </CardBody>
        </Card>

        <Card>
          <CardHeader trailing={<Pill tone="warning">Root B · Firm</Pill>}>
            The problem is Charter’s relative game: peers face the same attackers
            and are losing less badly / improving YoY
          </CardHeader>
          <CardBody>
            <Grid columns={2} gap={16}>
              <Stack gap={6}>
                <H3>Underlying assumptions</H3>
                <Bullet>
                  CMCSA’s YoY broadband improvement is achievable under the same
                  industry structure (not only better footprint mix).
                </Bullet>
                <Bullet>
                  Charter’s promo/bundle, WiFi/product, or service model is
                  losing switchers that a peer would keep.
                </Bullet>
                <Bullet>
                  Extra stock gap vs CMCSA is operating belief, not only
                  leverage optics.
                </Bullet>
                <Bullet>
                  A firm-level GTM or product move can change the Internet print
                  inside the horizon the tape cares about.
                </Bullet>
              </Stack>
              <Stack gap={6}>
                <H3>What it would make us measure</H3>
                <Bullet>
                  Footprint-adjusted loss rates CHTR vs CMCSA (mix control)
                </Bullet>
                <Bullet>
                  Win/loss reasons coded carefully (ops sampling — class
                  call-center caution)
                </Bullet>
                <Bullet>
                  Price/promo gap vs FWA and fiber in overlapping zips
                </Bullet>
                <Bullet>
                  Bundle attach, Advanced WiFi / Invincible WiFi retention lift
                </Bullet>
                <Bullet>
                  Earnings-day reaction vs Internet surprise after any GTM change
                </Bullet>
              </Stack>
            </Grid>
          </CardBody>
        </Card>

        <Card>
          <CardHeader trailing={<Pill tone="info">Root C · Belief (narrow)</Pill>}>
            The problem is the market lens: Internet acceleration is the priced
            variable; cash and mobile do not buy the multiple
          </CardHeader>
          <CardBody>
            <Grid columns={2} gap={16}>
              <Stack gap={6}>
                <H3>Underlying assumptions</H3>
                <Bullet>
                  Q4’25 (−119k, better YoY) rallied; Q1’26 (−120k, double YoY)
                  collapsed — acceleration, not the absolute level (issue-tree).
                </Bullet>
                <Bullet>
                  FCF vs Internet adds r ≈ 0.08 — cash does not move the tape in
                  quarter.
                </Bullet>
                <Bullet>
                  “Undervalued” without an Internet path is PR, not strategy.
                </Bullet>
              </Stack>
              <Stack gap={6}>
                <H3>What it would make us measure</H3>
                <Bullet>
                  Consensus Internet net-add expectations vs print
                </Bullet>
                <Bullet>
                  Time-to-credibility: what print sequence would re-rate peers
                </Bullet>
                <Bullet>
                  Whether any non-Internet catalyst (Cox close, capex guide)
                  historically moved CHTR without Internet
                </Bullet>
              </Stack>
            </Grid>
            <Text size="small" tone="tertiary">
              Role note: C is a root for “what problem the engagement must
              solve for the CEO charge,” but it is not a substitute for A vs B
              on operating cause. It gates recommendation design.
            </Text>
          </CardBody>
        </Card>
      </Stack>

      <Divider />

      <Stack gap={10}>
        <H2>6. Failure tests on this frame set</H2>
        <Table
          headers={["Test", "Status", "Check"]}
          columnAlign={["left", "left", "left"]}
          rows={[
            [
              "Self-similarity",
              "Pass if held",
              "A and B send you to different measures (industry share-shift identity vs footprint-adjusted peer gap). If both collapse to ‘competition,’ reject.",
            ],
            [
              "Checklist trap",
              "Watch",
              "Do not restate as desirability / access / viability of Spectrum Mobile. That accepts the client’s connectivity frame.",
            ],
            [
              "Non-conflict",
              "Pass",
              "A says firm skill cannot restore Internet growth; B says it can relative to peers. They cannot both be dominant.",
            ],
            [
              "Unfalsifiability",
              "Fixed by demotion",
              "‘Undervalued / buybacks’ absorbed everything; demoted. Root B narrowed to YoY peer slope + mix-adjusted losses.",
            ],
            [
              "Depth",
              "Open",
              "‘Losing to FWA’ is a location. Push to price gap, capacity constraints, and which CHTR zips.",
            ],
            [
              "Symptom vs cause",
              "Flagged",
              "Share price and buyback failure are symptoms. Internet print is closer; A vs B is the cause fork.",
            ],
          ]}
          striped
        />
      </Stack>

      <Stack gap={10}>
        <H2>7. Cheap gates first (sequence by cost of resolution)</H2>
        <Table
          headers={["Order", "Gate", "Why cheap / fatal", "If it fails"]}
          columnAlign={["right", "left", "left", "left"]}
          rows={[
            [
              "1",
              "Mix-adjusted CHTR vs CMCSA loss rates (DMA / overbuild intensity)",
              "Week 5 pack or public BDC/FCC overlays; binary for Root A vs B",
              "If gap vanishes after mix control → industry frame dominates",
            ],
            [
              "2",
              "Internet print is still the priced variable (reconfirm with next earnings)",
              "Event study already done; one more quarter",
              "If tape starts paying for FCF/mobile → belief frame (C) weakens",
            ],
            [
              "3",
              "Cox / Liberty timing and leverage path",
              "Binary deal facts; does not fix Internet alone",
              "Adverse close changes capital constraint, not root A vs B",
            ],
            [
              "4",
              "Win/loss and promo gap vs FWA/fiber in overlap zips",
              "Harder; only after mix test",
              "Feeds firm GTM hypotheses under Root B",
            ],
          ]}
          striped
        />
      </Stack>

      <Card>
        <CardHeader>Source hygiene (who paid / tier)</CardHeader>
        <CardBody>
          <Stack gap={6}>
            <Bullet>
              Tier 1: CHTR / CMCSA / VZ Ex99.1 and 10-K/10-Q (company-paid
              disclosures; still primary for their own metrics).
            </Bullet>
            <Bullet>
              Tier 2: contemporaneous earnings coverage for TMUS FWA when
              company disclosure thinned in Q1’26 — treat ending FWA stock as
              approximate until IR pack confirms.
            </Bullet>
            <Bullet>
              Tier 2/3: Motley Fool / Mobilewalla / CostQuest for narrative
              share-shift — use for hypotheses, not for sizing models without
              replication.
            </Bullet>
            <Bullet>
              Prior team canvases: issue-tree and diagnostic — reuse their
              CHTR/CMCSA tape and Internet bridge; do not invent a second
              headline stock story.
            </Bullet>
          </Stack>
        </CardBody>
      </Card>

      <Callout tone="info" title="Question for the client next (not a conclusion)">
        When Comcast’s residential broadband losses improved by ~117k YoY in
        Q1 2026 while yours roughly doubled, what did you actually see in the
        win/loss file — footprint mix, price gap to FWA, fiber overbuild
        intensity, or something else — and has anyone outside Spectrum already
        said no to the current Internet offer in a way that would show up in
        that file?
      </Callout>

      <Text size="small" tone="tertiary">
        Related: chtr-issue-tree-charts.canvas.tsx (chart 5–6 industry vs firm
        tape) · chtr-diagnostic-graphs.canvas.tsx (what the multiple prices) ·
        Framestorming-Playbook.md. Assignment still anchors to end Q1 2026.
      </Text>
    </Stack>
  );
}
