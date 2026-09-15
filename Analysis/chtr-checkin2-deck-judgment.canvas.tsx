/**
 * Check-in #2 deck vs prior analysis notes.
 * Source: CHTR_Checkin2_Deck.pptx (10 slides, Sep 2026).
 * Compared to: diagnostic graphs, issue-tree charts, industry-vs-firm
 * framestorm, client-question tree, CORE-INFORMATION.
 * Assignment anchor: end Q1 2026. Q2 labeled later public fact.
 */
import {
  Callout,
  Card,
  CardBody,
  CardHeader,
  CollapsibleSection,
  Divider,
  Grid,
  H1,
  H2,
  H3,
  Pill,
  Row,
  Stack,
  Stat,
  Swatch,
  Table,
  Text,
} from "cursor/canvas";

export default function ChtrCheckin2DeckJudgment() {
  return (
    <Stack gap={28}>
      <Stack gap={8}>
        <Row gap={8} wrap>
          <Pill tone="warning">Judgment, not a rewrite of the deck</Pill>
          <Pill tone="info">Check-in #2 · 10 slides</Pill>
        </Row>
        <H1>Check-in #2: what to keep, what to deny</H1>
        <Text tone="secondary">
          Transcribed from CHTR_Checkin2_Deck.pptx (Josh / Kishore / Justin /
          Kyle, working session with O’Donnell). Claims checked against the
          filings and against the diagnostic, issue-tree, and industry-vs-firm
          notes already in this project. Numbers are Q1 2026 unless marked
          later.
        </Text>
      </Stack>

      <Callout tone="danger" title="Headline verdict: deny the title, keep the tree">
        The deck is right that this is not an operating-cost problem, and
        right that Internet volume is the leak. It is wrong that the market
        is pricing a cash-access problem. Our notes already show the tape
        prices Internet surprise and YoY acceleration. Cash is a constraint
        on how you fund a fix — not the variable Wall Street is looking at.
        Slide 8’s own punchline (“repricing terminal value of the subscriber
        base”) contradicts slide 1.
      </Callout>

      <Grid columns={4} gap={12}>
        <Stat value="6" label="Claims to keep" tone="success" />
        <Stat value="1" label="Headline to drop" tone="danger" />
        <Stat value="4" label="Split / reframe" tone="warning" />
        <Stat value="1" label="Cheap gate missing" tone="info" />
      </Grid>
      <Text size="small" tone="tertiary">
        Keep: symptom/problem split, not-distress, H1 killed, volume leak,
        mobile arithmetic, contracting asks. Drop: “cash-access” as what the
        market prices. Split: H2, Branch C, Branch D, corridor order. Missing:
        mix-adjusted CHTR vs CMCSA.
      </Text>

      <Divider />

      <Stack gap={10}>
        <H2>The deck fights itself</H2>
        <Text>
          Two sentences cannot both be the diagnosis. The title is a cost
          instinct that survived falsification by moving below EBITDA. The
          market-lens slide already named the better frame.
        </Text>
        <Grid columns={2} gap={16}>
          <Card>
            <CardHeader trailing={<Pill tone="deleted" size="sm">Deny</Pill>}>
              Slide 1 title
            </CardHeader>
            <CardBody>
              <Stack gap={8}>
                <Text weight="semibold">
                  “The market is not pricing a cost problem. It is pricing a
                  cash-access problem.”
                </Text>
                <Text size="small" tone="secondary">
                  Speaker note: original cost hypothesis failed; reframed
                  below the EBITDA line, “still cost-flavored.”
                </Text>
                <Text size="small">
                  Why deny: FY2025 FCF rose 18% while Internet fell 403k and
                  the stock was still crushed. Internet net adds vs FCF is r =
                  0.08 over 10 quarters. Q4 2025 printed the weakest FCF in
                  the window ($773M) and the stock rallied +7.6% because
                  Internet improved YoY. Accessible cash is not the priced
                  variable.
                </Text>
              </Stack>
            </CardBody>
          </Card>
          <Card>
            <CardHeader trailing={<Pill tone="added" size="sm">Keep this line</Pill>}>
              Slide 8 punchline
            </CardHeader>
            <CardBody>
              <Stack gap={8}>
                <Text weight="semibold">
                  “The market is repricing terminal value of the subscriber
                  base, not punishing operations.”
                </Text>
                <Text size="small" tone="secondary">
                  Follow-on: EPS engineering cannot outrun a shrinking-asset
                  narrative.
                </Text>
                <Text size="small">
                  Why keep: this is the issue-tree / diagnostic conclusion.
                  Q4 2025 (−119k, better YoY) rallied; Q1 2026 (−120k, double
                  YoY) fell 25.5%. Same cash stack, opposite tape. Promote
                  this sentence to the title and demote cash-access to a
                  funding constraint.
                </Text>
              </Stack>
            </CardBody>
          </Card>
        </Grid>
      </Stack>

      <Stack gap={8}>
        <H2>Killer test the deck did not run</H2>
        <Text>
          H2 says the market will not pay for EBITDA it cannot access. If
          that were true, weak FCF should sell the stock and strong FCF
          should buy it. Earnings-day tape does not do that. It tracks
          Internet YoY slope.
        </Text>
        <Table
          headers={[
            "Print",
            "Internet",
            "vs year-ago",
            "FCF ($M)",
            "1-day %",
            "H2 prediction",
          ]}
          columnAlign={["left", "right", "right", "right", "right", "left"]}
          rowTone={[
            undefined,
            "success",
            "danger",
            undefined,
            "success",
            "danger",
            "warning",
          ]}
          rows={[
            ["Q4’24", "−177k", "—", "984", "+2.6%", "Weak cash, not sold"],
            ["Q1’25", "−59k", "better", "1,564", "+11.4%", "Cash helped; Internet also better"],
            ["Q2’25", "−116k", "better vs ’24", "1,046", "−18.5%", "Sold on consensus miss, not FCF"],
            ["Q3’25", "−109k", "flat", "1,621", "+1.3% close", "Best FCF; tape indifferent"],
            ["Q4’25", "−119k", "better than −177k", "773", "+7.6%", "Worst FCF, stock up — falsifies H2"],
            ["Q1’26", "−120k", "double −59k", "1,372", "−25.5%", "Both moved wrong; cannot isolate cash"],
            ["Q2’26 (later)", "−172k", "worse", "969", "−2.5% / −11.6% open", "Already de-rated"],
          ]}
          striped
        />
        <Text size="small" tone="tertiary">
          Internet and FCF: Ex99.1 / trending. Returns: Yahoo close-to-close
          on earnings dates from the issue-tree canvas. Q4’25 is the clean
          falsifier: cash-access got worse, Internet YoY got better, the
          tape paid for Internet.
        </Text>
        <Callout tone="warning" title="H2’s own falsification test is cherry-picked">
          Slide 4 says H2 would be false if “FCF conversion improving while
          subs decline (it is not: FCF −12% in Q1).” That uses the one
          quarter where cash and subs both went the wrong way. FY2025 already
          showed FCF +18% while Internet customers fell 403k. Run that test
          on FY2025 and H2 as a market-lens claim is already dead.
        </Callout>
      </Stack>

      <Divider />

      <Stack gap={10}>
        <H2>Claim-by-claim</H2>
        <Text tone="secondary">
          Affirm means: keep this in the O’Donnell session. Deny means: do
          not defend it. Split means: the fact is right, the role in the
          diagnosis is wrong.
        </Text>
        <Table
          headers={["Deck claim", "Call", "Why"]}
          columnAlign={["left", "left", "left"]}
          rowTone={[
            "danger",
            "info",
            "success",
            "success",
            "success",
            "success",
            "success",
            "success",
            "warning",
            "warning",
            "success",
            "warning",
            "danger",
            "info",
          ]}
          rows={[
            [
              "Title: market prices a cash-access problem",
              "Deny",
              "Priced variable is Internet surprise / YoY acceleration (issue-tree chart 6). FCF vs Internet adds r = 0.08. Q4’25 FCF trough + rally.",
            ],
            [
              "Problem: market no longer believes connectivity relationships return to growth at an acceptable cash cost",
              "Split — rewrite",
              "Keep the growth-belief half. “Acceptable cash cost” is a constraint, not the belief being priced. Slide 2 is better than slide 1; still overweights cash.",
            ],
            [
              "Symptom is the share price, not distress",
              "Affirm",
              "FY2025: $54.8B revenue, $22.7B Adj. EBITDA, $5.0B FCF, ~41% margin. Matches the brief and CORE-INFORMATION. This is the 10-point problem-definition slide — it works.",
            ],
            [
              "Not a pricing collapse (ARPU ~$119 by design)",
              "Affirm",
              "$118.71 → $119.05 → $118.44. Volume, not price. FY2025 10-K Internet bridge: +$785M mix, −$380M volume.",
            ],
            [
              "H1 (opex compressing profit) rejected",
              "Affirm",
              "Opex $33.2B → $32.7B; margin 41.0% → 41.5%. Q1 EBITDA −2.2% vs revenue −1.0% is mix plus a $75M one-time in Q1’25 — even less of a cost story.",
            ],
            [
              "Branch A: Internet volume is the primary leak",
              "Affirm — this is the operating diagnosis",
              "Internet −464k y/y; Q1 −120k vs −59k. Internet revenue itself fell 1.3% in Q1. This is the profit engine and the tape’s trigger.",
            ],
            [
              "Mobile cannot arithmetically cover the leak",
              "Affirm",
              "$23.8B Internet vs $3.8B mobile, MVNO margin. Diagnostic canvas: market will not net mobile lines against Internet customers. Do not elevate connectivity customers.",
            ],
            [
              "Branch B (opex → EBITDA) killed",
              "Affirm",
              "Showing a killed branch is the right check-in move. Invite O’Donnell to attack H2, not to revive H1.",
            ],
            [
              "Branch C: 73¢ of every EBITDA dollar spoken for (capex + interest)",
              "Split",
              "Arithmetic holds: ($11.7B + $5.0B) / $22.7B ≈ 73.5%; FCF ≈ 22% of EBITDA. Role is wrong: this is a hard cash constraint, not the cause of the Apr 24 tape. Capex is not the same claim as interest — rural still adds customers; upgrade/rebuild is the fiber response.",
            ],
            [
              "Q1 capex +19%, FCF −12%, wait for 2027 step-down",
              "Split",
              "Facts hold. Implication does not: waiting for network-evolution completion is the base-case capital story and fails the out-of-the-box test unless the Internet print inflects inside ~24 months.",
            ],
            [
              "Thin equity on ~$95B debt: ±0.5x EV/EBITDA ≈ ±$11B ≈ ±45% equity",
              "Affirm as mechanics",
              "0.5 × $22.7B = $11.4B. Post-crash equity ~$22B on 123M shares × $180.13, not the deck’s ~$25B from FY diluted WAS. Order of magnitude is right; leverage amplifies the tape. It does not tell you what the tape is looking at.",
            ],
            [
              "Buybacks ($79.7B since 2016) are not holding the price",
              "Affirm observation; deny as unique support for H2",
              "True under both a cash-access frame and an Internet-trajectory frame. Instructor’s ~$10B framing is correctly caveated. Demoted in the framestorm to decision architecture.",
            ],
            [
              "H2 as working hypothesis (market will not pay for inaccessible EBITDA)",
              "Deny as the working hypothesis",
              "Keep it as a cash-identity: equity sees ~22¢ of each EBITDA dollar. Do not use it as the explanation of Wall Street’s lens. Slide 8 already has the better explanation.",
            ],
            [
              "Three corridors, Week 7 will pick one",
              "Split — invert the order",
              "Corridor C (attack the volume leak) is the operating work. Corridor B is capital-structure after diagnosis. Corridor A (make 2027 capex step-down believable) is the move most likely to fail O’Donnell’s test if it stands alone.",
            ],
          ]}
          striped
        />
      </Stack>

      <Stack gap={8}>
        <H2>Number audit — the deck’s facts mostly hold</H2>
        <Text>
          Do not pick a fight with O’Donnell on arithmetic. The fights are
          role and missing comparison.
        </Text>
        <Table
          headers={["Figure on the slide", "Check", "Note"]}
          columnAlign={["left", "left", "left"]}
          rowTone={["success", "success", "success", "warning", "info", "success"]}
          rows={[
            [
              "−80% / −25% / Internet −120k",
              "Holds",
              "Brief + Yahoo: $241.78 → $180.13 on Apr 24 2026 (−25.5%). Q1 Internet −120k vs Q1’25 −59k (deck says ~60k).",
            ],
            [
              "EBITDA margin 41.0 / 41.5 / 41.5",
              "Holds",
              "22,569/55,085 = 41.0%; 22,708/54,774 = 41.5%; 5,637/13,597 = 41.5%.",
            ],
            [
              "73% of EBITDA spoken for; FCF ~22%",
              "Holds as identity",
              "(11,659 + 5,042) / 22,708 = 73.5%. FCF 5,004 / 22,708 = 22.0%. Residual ~$1B is taxes/WC/other as the notes say.",
            ],
            [
              "Market cap ~$25B at Q1 close",
              "Slightly high",
              "Deck: 137.7M diluted WAS × ~$180. Class A outstanding 3/31/26 = 123.0M × $180.13 ≈ $22.2B. Use outstanding, not FY diluted.",
            ],
            [
              "Q1 EBITDA −2.2% “tracks revenue −1.0% + mix”",
              "Directionally true; omit the $75M",
              "10-Q: Q1’25 had $75M one-time favorable. Strip it and underlying EBITDA is ~flat vs revenue. Strengthens the Branch B kill.",
            ],
            [
              "Chart: Internet −464k y/y, mobile +1.77M",
              "Holds",
              "30,024 → 29,560 and 10,365 → 12,134. Level change, not quarterly net adds — label is accurate (“Q1 2026 vs Q1 2025”).",
            ],
          ]}
          striped
        />
      </Stack>

      <Divider />

      <Stack gap={10}>
        <H2>What the deck never tested — and our notes already did</H2>
        <Text>
          Check-in #2 is scored on analysis. The cheap industry-vs-firm gate
          is absent. That is the gap O’Donnell can open in one question.
        </Text>
        <Table
          headers={["Prior note", "What it showed", "In the deck?"]}
          columnAlign={["left", "left", "left"]}
          rowTone={["danger", "warning", "info", "warning", "info"]}
          rows={[
            [
              "CHTR vs CMCSA YoY Internet slope (framestorm Root A vs B)",
              "Q1’26: CHTR −59k → −120k (worse). CMCSA residential BB −183k → −65k (better). Same-day tape −25.5% vs −13%. Same neighborhood EV/EBITDA (~5.5–6x) — not a Charter-only EBITDA discount.",
              "Missing. Corridor C asks for a churn-by-overlap cut; it never asks “did Comcast face the same wind and lose less?”",
            ],
            [
              "Earnings-day vs Internet acceleration (issue-tree chart 6)",
              "Absolute −110k to −120k produced +7.6%, −18.5%, and −25.5% depending on YoY and consensus. That is Wall Street’s lens.",
              "Slide 8 gestures at terminal value. No event-study exhibit.",
            ],
            [
              "FCF does not rescue the multiple (diagnostic)",
              "r = 0.08; FY2025 FCF +18% while the engine shrank. Graph 3: EBITDA sticky, FCF a capex residual.",
              "Inverted: FCF weakness is treated as the thing being priced.",
            ],
            [
              "Footprint mix still unidentified",
              "Until DMA / overbuild overlay, “Charter underperforms” could be mix, not GTM. Flag as ESTIMATED.",
              "Partially: asks for FWA vs fiber vs uncontested split. Good ask. Not done yet — do not speak as if Branch A is geographically located.",
            ],
            [
              "Capex intensity vs Comcast (capex canvas)",
              "Charter spends ~2× cable-peer capex/revenue. Rural is a real cash sink that still adds customers (Q1 rural relationships +41k).",
              "Branch C treats capex as a homogeneous prior claim, like interest. It is not.",
            ],
          ]}
          striped
        />
        <Callout tone="info" title="Question O’Donnell can ask that the deck cannot answer">
          When Comcast’s residential broadband losses improved by ~117k YoY
          in Q1 2026 while yours doubled, what did you actually see — footprint
          mix, price gap to FWA, fiber overbuild, or something else? That is
          the next-client question already written in the framestorm. Put it
          on the asks slide.
        </Callout>
      </Stack>

      <Stack gap={10}>
        <H2>Corridors — invert before Week 7</H2>
        <Text>
          Directional-not-final is the right posture for this check-in. The
          order still tells O’Donnell what the team thinks the diagnosis is.
          Right now it reads: cash first, then capital structure, then the
          leak. That is H2 leaking into the recommendation set.
        </Text>
        <Grid columns={3} gap={12}>
          <Card>
            <CardHeader trailing={<Pill tone="added" size="sm">Promote</Pill>}>
              Corridor C — volume leak
            </CardHeader>
            <CardBody>
              <Stack gap={6}>
                <Text size="small">
                  FWA-exposed vs fiber-overbuilt vs residual. Different plays.
                  This is Root A vs B work. It is the only corridor that can
                  change the priced print inside ~24 months.
                </Text>
                <Text size="small" tone="secondary">
                  Keep the test: churn split by competitive overlap. Add the
                  Comcast mix-adjusted gate before GTM recommendations.
                </Text>
              </Stack>
            </CardBody>
          </Card>
          <Card>
            <CardHeader trailing={<Pill tone="warning" size="sm">Constraint</Pill>}>
              Corridor B — claims on cash
            </CardHeader>
            <CardBody>
              <Stack gap={6}>
                <Text size="small">
                  Leverage band, buyback vs paydown, CBRS/MVNO economics.
                  Real, and Cox will reset them. Not a diagnosis of why the
                  multiple moved.
                </Text>
                <Text size="small" tone="secondary">
                  Use after you know which Internet path you are funding. Do
                  not pitch “stop buybacks / pay down debt” as the trajectory
                  fix.
                </Text>
              </Stack>
            </CardBody>
          </Card>
          <Card>
            <CardHeader trailing={<Pill tone="deleted" size="sm">Demote</Pill>}>
              Corridor A — 2027 cash inflection
            </CardHeader>
            <CardBody>
              <Stack gap={6}>
                <Text size="small">
                  Prove post-2027 capex step-down. That is management’s
                  existing story. O’Donnell already flagged “run the upgrade
                  harder” as the move most likely to fail the out-of-the-box
                  test.
                </Text>
                <Text size="small" tone="secondary">
                  Keep as a milestone overlay on whatever operating move you
                  pick — not as the recommendation.
                </Text>
              </Stack>
            </CardBody>
          </Card>
        </Grid>
      </Stack>

      <Stack gap={8}>
        <H2>What to say in the room</H2>
        <Table
          headers={["If O’Donnell pushes on…", "Do not defend", "Say instead"]}
          columnAlign={["left", "left", "left"]}
          rows={[
            [
              "The title / H2",
              "“The market cannot access the cash.”",
              "We killed opex. Cash conversion is a constraint (~22¢ of EBITDA). The tape on Apr 24 was the Internet print doubling YoY — Q4’25 had worse FCF and rallied.",
            ],
            [
              "Is this just cable / industry?",
              "“Everyone is losing broadband.”",
              "Industry is the floor. Comcast’s Q1 slope improved while ours worsened, and we sold twice as hard the same day. We have not mix-adjusted yet — that is the first ask.",
            ],
            [
              "Mobile / connectivity",
              "“Connectivity customers are growing.”",
              "Mobile is $3.8B on a $23.8B Internet base, lower margin, and the multiple has not netted it. Arithmetic, not taste.",
            ],
            [
              "Buybacks / undervalued",
              "“We should keep buying / the stock is cheap.”",
              "Buybacks are not holding the price. That is a symptom. Cheap FCF yield is the sector (CMCSA too). The CEO charge is a strategic path that changes Internet run-rate.",
            ],
            [
              "2027 network evolution",
              "“Once capex steps down, FCF inflects and the stock follows.”",
              "That is the current plan. It does not change the print the market has been trading. We will not hang the pitch on a wait.",
            ],
          ]}
          striped
        />
      </Stack>

      <Callout tone="success" title="Keep slide 10 almost as written">
        The asks are the strongest page: measured vs coded churn reasons
        (O’Donnell’s call-center lesson), overlap split of the 464k, capex
        committed vs discretionary, post-2027 steady-state, CBRS at scale,
        leverage/buyback negotiability, Cox treatment, time horizon, and
        “kill a hypothesis today.” Add one ask: mix-adjusted Internet loss
        rate vs Comcast. Ask them one at a time.
      </Callout>

      <Divider />

      <Stack gap={8}>
        <H2>Slide-by-slide transcript</H2>
        <Text tone="secondary">
          Full text from the .pptx, including speaker notes. Use this if you
          do not have the deck open.
        </Text>

        <CollapsibleSection
          title="1 · Title"
          leading={<Swatch color="red" />}
          trailing={<Pill size="sm">Deny headline</Pill>}
          defaultOpen
        >
          <Stack gap={6}>
            <Text size="small" tone="tertiary">
              MAN 6930 · Foundations of Consulting · Check-in #2 · Josh,
              Kishore, Justin, Kyle · Sep 2026
            </Text>
            <Text weight="semibold">
              The market is not pricing a cost problem. It is pricing a
              cash-access problem.
            </Text>
            <Text size="small">
              Diagnostic read-out and working hypotheses for the Office of
              the CEO, Charter Communications.
            </Text>
            <Text size="small" italic tone="secondary">
              Notes: Set the frame in one breath: we tested the team’s
              original cost-side hypothesis against the filings, it failed
              falsification, and the reframed hypothesis is stronger and
              still cost-flavored — the cost problem lives below the EBITDA
              line.
            </Text>
          </Stack>
        </CollapsibleSection>

        <CollapsibleSection
          title="2 · Problem definition"
          leading={<Swatch color="green" />}
          trailing={<Pill size="sm">Keep, rewrite last clause</Pill>}
        >
          <Stack gap={6}>
            <Text>
              Symptom: a collapsing share price. Problem: the market no
              longer believes connectivity relationships return to growth at
              an acceptable cash cost.
            </Text>
            <Text size="small">
              Symptom: −80% over five years; −25% in one day after Q1 2026.
              Trigger: Internet −120k, roughly double ~60k in Q1 2025, and
              Internet revenue fell for the first time (−1.3%).
            </Text>
            <Text size="small">
              What it is not: not distress (FY2025 $54.8B / $22.7B Adj.
              EBITDA +0.6% / $5.0B FCF +18% / ~41% margin); not a pricing
              collapse (ARPU ~$119); not an opex blowout (costs fell, EBITDA
              grew).
            </Text>
            <Text size="small">
              Engagement question: why is Wall Street looking at Charter this
              way — and what strategic move credibly changes the trajectory
              (not a communications patch)?
            </Text>
            <Text size="small" italic tone="secondary">
              Notes: Separate symptom from problem explicitly — this is 10 of
              40 points. The right column pre-loads the falsification of the
              naive cost hypothesis.
            </Text>
          </Stack>
        </CollapsibleSection>

        <CollapsibleSection
          title="3 · Issue tree (A–D)"
          leading={<Swatch color="orange" />}
          trailing={<Pill size="sm">Keep A/B; re-role C/D</Pill>}
        >
          <Stack gap={6}>
            <Text>Why is CHTR equity value collapsing?</Text>
            <Text size="small">
              A · Active, primary leak — Revenue: subs × ARPU. Internet
              −464k y/y; ARPU flat; mobile +1.7M lines, lower-margin resale.
            </Text>
            <Text size="small">
              B · Tested, killed — Operating cost → EBITDA. Opex fell; margin
              ~41%; FY2025 EBITDA grew.
            </Text>
            <Text size="small">
              C · Active, reframed cost — Below the line: $11.7B capex +
              $5.0B interest consume ~73% of EBITDA. Q1: capex +19%, FCF
              −12%.
            </Text>
            <Text size="small">
              D · Active, valuation lens — 4.15x leverage; ~$95B debt; small
              EV multiple moves swing thin equity. Buybacks not rewarded.
            </Text>
            <Text size="small" italic tone="secondary">
              Notes: Walk left to right. A is the revenue leak, B is dead, C
              is where the team’s cost instinct actually lives, D translates
              A+C into the share price.
            </Text>
          </Stack>
        </CollapsibleSection>

        <CollapsibleSection
          title="4 · H1 rejected / H2 working"
          leading={<Swatch color="red" />}
          trailing={<Pill size="sm">Keep H1 kill; drop H2 as lens</Pill>}
        >
          <Stack gap={6}>
            <Text size="small">
              H1 rejected: “Rising operating costs are compressing profit and
              driving the share-price decline.” Test: margin compression and
              opex outgrowing revenue. Observed: opex $32.7B vs $33.2B; Adj.
              EBITDA +0.6%; Q1 EBITDA −2.2% tracks revenue; ARPU flat.
            </Text>
            <Text size="small">
              H2 working: “The cost problem is real but lives below EBITDA:
              capex + interest consume the cash before equity can touch it,
              while the revenue engine shrinks — so the market will not pay
              for EBITDA it cannot access.”
            </Text>
            <Text size="small">
              Stated falsifiers: FCF conversion improving while subs decline
              (cited Q1 −12%); market rewarding buybacks (not: $79.7B
              retired, 10-year lows); losses concentrated where network
              evolution is complete (open data-pack test).
            </Text>
            <Text size="small" italic tone="secondary">
              Notes: Showing a killed branch is the point. Invite O’Donnell
              to attack H2.
            </Text>
          </Stack>
        </CollapsibleSection>

        <CollapsibleSection
          title="5 · Branch A revenue"
          leading={<Swatch color="green" />}
          trailing={<Pill size="sm">Affirm</Pill>}
        >
          <Stack gap={6}>
            <Text>
              The leak is volume: mobile growth cannot arithmetically offset
              internet losses.
            </Text>
            <Text size="small">
              $23.8B FY2025 Internet vs $3.8B mobile service (+22%),
              lower-margin MVNO. ARPU $118.71 → $119.05 → $118.44. Q1 2026
              Internet revenue −1.3% — first time subs pulled dollars down.
            </Text>
            <Text size="small">
              Chart: Customer net change Q1 2026 vs Q1 2025 (000s) — Internet
              −464, mobile +1,769.
            </Text>
            <Text size="small" italic tone="secondary">
              Notes: Anticipate “is mobile the answer?” — mobile deepens
              bundles and cuts churn but cannot replace internet economics at
              6× the revenue base and higher margin.
            </Text>
          </Stack>
        </CollapsibleSection>

        <CollapsibleSection
          title="6 · Branch B opex (killed)"
          leading={<Swatch color="green" />}
          trailing={<Pill size="sm">Affirm</Pill>}
        >
          <Stack gap={6}>
            <Text>
              Operating costs are not the problem: costs fell, EBITDA grew,
              margin held.
            </Text>
            <Text size="small">
              41.0% FY2024 · 41.5% FY2025 · 41.5% Q1 2026. Q1 EBITDA −2.2%
              tracks revenue + mix. Chart: Revenue 55.1 → 54.8; opex 33.2 →
              32.7; Adj. EBITDA 22.6 → 22.7 ($B).
            </Text>
            <Text size="small" italic tone="secondary">
              Notes: Disconfirming exhibit. If anyone wants the cost story,
              move it below the line to slide 7.
            </Text>
          </Stack>
        </CollapsibleSection>

        <CollapsibleSection
          title="7 · Branch C below the line"
          leading={<Swatch color="yellow" />}
          trailing={<Pill size="sm">Affirm identity; deny lens</Pill>}
        >
          <Stack gap={6}>
            <Text>
              ~73¢ of every EBITDA dollar is spoken for before shareholders
              see a cent.
            </Text>
            <Text size="small">
              $22.7B Adj. EBITDA − $11.7B capex − $5.0B interest − ~$1.0B
              taxes/WC/other = $5.0B FCF. Q1: capex +19% (CPE +41%,
              upgrade/rebuild +71%) → FCF −12%. Network evolution targeted
              end-2027.
            </Text>
            <Text size="small" italic tone="secondary">
              Notes: Money slide. 73% = (capex + interest) / EBITDA. This is
              where the team’s cost instinct is right — just below the line.
            </Text>
          </Stack>
        </CollapsibleSection>

        <CollapsibleSection
          title="8 · Branch D market lens"
          leading={<Swatch color="blue" />}
          trailing={<Pill size="sm">Keep punchline; drop as H2 support</Pill>}
        >
          <Stack gap={6}>
            <Text>
              Thin equity on a $95B debt stack: why buybacks are not holding
              the price.
            </Text>
            <Text size="small">
              $79.7B repurchased since Sep 2016 (~184M shares/units) vs ~$25B
              market cap at Q1 close. 4.15x net leverage; plan 4.0–4.5x until
              Cox. ±0.5x EV/EBITDA ≈ ±$11B EV ≈ ±45% equity.
            </Text>
            <Text size="small" weight="semibold">
              Read: the market is repricing terminal value of the subscriber
              base, not punishing operations.
            </Text>
            <Text size="small" italic tone="secondary">
              Notes: Answers “why is Wall Street looking at it this way.”
              Caveat on instructor’s ~$10B vs $79.7B program total. Market
              cap ≈ 137.7M × ~$180.
            </Text>
          </Stack>
        </CollapsibleSection>

        <CollapsibleSection
          title="9 · Three corridors"
          leading={<Swatch color="orange" />}
          trailing={<Pill size="sm">Invert order</Pill>}
        >
          <Stack gap={6}>
            <Text size="small">
              A · Make the cash inflection believable — post-2027 capex
              step-down, committed vs discretionary, pre-commit freed FCF.
            </Text>
            <Text size="small">
              B · Restructure the claims on cash — leverage below 4.0x,
              buybacks toward paydown, CBRS/5G offload vs MVNO.
            </Text>
            <Text size="small">
              C · Attack the volume leak — FWA-exposed vs fiber-overbuilt vs
              rural infill; churn split by overlap.
            </Text>
            <Text size="small" italic tone="secondary">
              Notes: Deliberately directional. Each corridor names the test
              it still needs.
            </Text>
          </Stack>
        </CollapsibleSection>

        <CollapsibleSection
          title="10 · Asks for the working session"
          leading={<Swatch color="green" />}
          trailing={<Pill size="sm">Affirm; add CMCSA</Pill>}
        >
          <Stack gap={6}>
            <H3>On the data pack</H3>
            <Text size="small">
              Which fields are measured vs coded? Churn split by FWA vs fiber
              vs uncontested — what % of the 464k? Of ~$11.4B 2026 capex, how
              much is committed vs discretionary? What is post-2027
              steady-state capex, and has the market been told? Has CBRS/5G
              offload been modeled to mobile gross margin at scale?
            </Text>
            <H3>On scope and constraints</H3>
            <Text size="small">
              Are 4.0–4.5x and the buyback program negotiable? Treat Cox as
              closed, pending, or in scope to challenge? Horizon: next 8
              quarters or 2030? What is off the table (asset sales, footprint
              exits, video divestiture, going private)? Would you rather see
              a hypothesis killed today than defended to Week 7?
            </Text>
            <Text size="small" italic tone="secondary">
              Notes: Ask one at a time; force numbers, dates, instances;
              separate observation from interpretation; ask how they know.
            </Text>
          </Stack>
        </CollapsibleSection>
      </Stack>

      <Divider />

      <Stack gap={8}>
        <H2>Rewrite we would defend</H2>
        <Text>
          Symptom: collapsing share price. Problem: the market no longer
          believes Internet relationships return to growth on a horizon it
          will pay for. Cash conversion and leverage decide what we can fund;
          they are not what Apr 24 priced. Industry share-shift is the floor;
          Charter’s worse YoY slope vs Comcast is the gap still in play.
        </Text>
        <Text size="small" tone="tertiary">
          Compared against: chtr-diagnostic-graphs (priced variable, r =
          0.08), chtr-issue-tree-charts (event study, CHTR vs CMCSA tape),
          chtr-industry-vs-firm-framestorm (Root A/B/C), 
          chtr-client-question-response-tree (asks order), CORE-INFORMATION
          (filings). Assignment still anchors to 31 Mar 2026.
        </Text>
      </Stack>
    </Stack>
  );
}
