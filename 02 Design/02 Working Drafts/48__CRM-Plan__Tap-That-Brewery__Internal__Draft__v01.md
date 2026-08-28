# 48 – CRM Plan
## Tap That Brewery

| | |
|---|---|
| **Document** | CRM Plan – catalogue #48 |
| **Engagement** | Jewell Projects × Tap That Brewery |
| **Phase** | 02 Design |
| **Status** | Draft v01 – Internal |
| **Date** | 28 August 2026 |
| **Prepared by** | Jewell Projects |

*Pre-CP1 draft – produced ahead of Discover sign-off; census data, membership pricing reconciliation and competitor verification may revise inputs.*

---

## Why this is the highest-leverage plan in the Design set

Every growth number in this engagement runs through one machine: knowing, per customer, **when they last bought a keg**. The lifecycle rules already exist (active <75 days, at-risk 75–90, churned 90+), the winback offer already exists ($20 off), and the customers already exist (206 owners / 96–113 active plus an untracked churned pool). What doesn’t exist is the system: churn management is a hand-sent monthly SMS, wholesale leads die between first DM reply and manager contact, and the GoTab/Fishbowl integration that fixes both is "pending" with no date. This plan costs approximately no media dollars and directly serves O2 (stop the refill leak) – on a loss-making P&L it is the first thing to build.

## Data model (the minimum viable customer record)

One record per customer in Fishbowl, keyed to GoTab transactions:

| Field group | Fields | Source | Why |
|---|---|---|---|
| **Identity** | Name, mobile, email, suburb/postcode, marketing consent (email/SMS/ad-matching), 18+ confirmed | GoTab checkout, membership signup, giveaway entry | Consent per channel is the legal gate for #46/#47; postcode drives delivery-launch targeting (#51) |
| **System owned** | Owns system Y/N · bought from **Tap That Brewery / elsewhere** (the switcher flag) · type (2/3/4/6-tap, integrated, 5L mini, Benchy) · purchase date | GoTab sale record; asked at first fill for walk-in switchers | The switcher flag is the single most valuable field in the model – 116 of 206 owners (56%) bought elsewhere and KR 1.1 (90 switcher acquisitions) is unmeasurable without it |
| **Refill history** | Every keg transaction: date, keg type (plastic/corny), size (5L/20L/50L), tier (core/premium/top shelf), price paid, **days-since-last-keg** (computed nightly) | GoTab | Days-since-last-keg is the field the whole lifecycle engine keys on |
| **Membership** | Tier (Keg Crew/Mug Club/Brew Buds/none), join date, renewal date, price paid | GoTab/Fishbowl | Renewal automation (#47 seq 6); attach-rate reporting (KR 1.4) |
| **Tokens & referrals** | Tap Token balance, referral events (1,000 tokens system/venue, 500 refill) | Loyalty system | Referral is a tracked acquisition channel, not folklore; leaderboard already gamifies it |
| **Provenance** | First-touch source (giveaway cycle, taproom, referral, search, wholesale) | Entry forms, staff prompt at first sale | CAC-by-channel truth for #46 kill criteria |

Data hygiene rule (KR 2.4): **100% of keg transactions attached to a customer record.** A counter script for staff ("what number do we text when it’s ready?") is the whole capture mechanism – it already works for corny customers.

## Lifecycle automation: each customer's own clock, not ours

**This section was rebuilt after the 27 August review.** The first version fired at a fixed 60, 75 and 90 days for everybody. The review's objection is the right one:

> "People are creatures of habit and likely go through kegs at about the same rate, so a 90-day SMS is a bit tone-deaf. We know their purchase patterns, so customise the contact and be Johnny on the spot."

A fixed calendar is only correct for the average customer, and almost nobody is the average customer. Roughly **10% buy monthly, 60% about every three months, and 40% run longer**. At day 60, a monthly buyer is a month overdue and probably gone; a quarterly buyer is on schedule and being nagged. The same message is late for one and rude to the other.

**So the trigger is relative to each customer's own interval.** Fishbowl computes a rolling median gap between kegs per customer from at least three purchases, and the flow fires against that.

| Trigger | State | Automated action | Replaces |
|---|---|---|---|
| **0.85 × their interval** | Cadence due | "What's kegged and ready" (#47 seq 3). Arrives just before they would normally reorder – the *Johnny on the spot* touch | Nothing – new revenue protection |
| **1.15 × their interval** | Drifting | Nudge, no discount. Range and freshness angle | Nothing |
| **1.5 × their interval** | **At-risk** | SMS and email: service and convenience (corny Tue→Fri, delivery when live). Still no discount – do not train discount-waiting | The untargeted blast |
| **2 × their interval**, or 90 days, whichever is later | **Churned** | Winback ladder, tracked per offer: $20-off/2-week window → Marie's Pizza Buttercard → next tested offer | The manual monthly SMS |
| Churned + 60 days | Dormant | Quarterly-max touch: giveaway invite, seasonal release, event invite | Nothing – the list currently goes dark |

**Fallback.** Customers with fewer than three recorded purchases have no interval yet, so they run on the flat 60/75/90 rails until one exists. That is a starting state, not the design.

**The 40% is the priority inside this.** The band that runs longest between kegs is the largest and the most winnable: they have **cut back rather than defected**, and the system is still in the backyard. Where they are also Keg Crew members they are paying for something they have stopped using, which is both the strongest reason to act and the easiest message to write. The product answer belongs with it — a low-alcohol or healthier line, framed as hydration rather than beer, reactivates them without asking anyone to drink more (#14).

Every send and every response is written back to the record, so the at-risk save rate (KR 2.2 target ≥40%) and winback count (KR 2.3 target 30/yr) become dashboard numbers instead of anecdotes.

## Loyalty: simplify before automating

Two review findings sit here, and both cut against building more machinery.

**The points system may be its own cost driver.** Tap Tokens require administration, reconciliation and explanation, and the review's question is whether that cost is bought back in loyalty. The proposed alternative is blunt and legible: **every tenth keg free.** A customer can hold that in their head, it needs almost no administration, and it rewards exactly the behaviour the business needs. Tokens do not have to go, but the burden of proof is now on keeping them rather than on replacing them.

**Referral should be a free keg for both sides.** When a mate buys a system, both parties get a keg. That is simpler than a token balance and it pays out at the moment of goodwill rather than at some later threshold. Pay-with-a-tweet and a discount for tagging sit alongside it as low-cost UGC mechanics.

Neither is a decision for us. Both belong in the same conversation as the membership price (open item #2), because the answer changes what the CRM has to track.

## Segmentation views (saved, standing views in Fishbowl)

| View | Definition | Used by |
|---|---|---|
| **Switcher targets** | Owns system, bought elsewhere, <2 fills with us | "We fill any system" campaign (#46); counter conversion scripts |
| **At-risk** | 75–90 days since last keg | Daily automation + weekly human review of high-value names |
| **Dormant/churned** | 90+ days | Winback ladder; quarterly re-permission |
| **High-value** | Top quartile by 12-month refill spend, or Keg Crew + 2+ kegs/month | Tasting-night invites (#50), referral asks, first delivery-launch access – protect these relationships personally |
| **Membership expiring** | Renewal within 45 days | #47 seq 6 |
| **Giveaway cohort (per cycle)** | Entrants by cycle, with converted Y/N | KR 1.2 measurement; #46 retargeting audiences |

## Wholesale pipeline (fixing the DM follow-up leak)

Discovery’s admission: social DMs get responses, venues pass on a manager’s contact, and "follow-up wasn’t as tight as it could have been." The fix is a pipeline, not a platform – a simple board (Fishbowl if it supports B2B records, else a shared sheet until it does):

| Stage | SLA | Owner |
|---|---|---|
| Lead (DM reply / referral / venue-hire enquiry) | Logged same day, every lead | Harry |
| Contact passed (manager name/number received) | **First follow-up within 48 hours** (KR 3.4) | Harry → founder for closes |
| Tasting/match made (style-matched: J-Lager → Japanese, Cerveza → Mexican, craft → craft bars) | Within 2 weeks of contact | Chris (product credibility) |
| Pouring / won | Handover to refill cadence tracking – wholesale accounts get lifecycle states too | – |
| Lost/parked | Reason logged (contract, CUB exclusivity, no taps) – parked ≠ dead; contract end dates are diarised | – |

Target: 6 new style-matched venue accounts in 12 months (KR 3.4). Sports-club white-label leads (10%/10% model) run on the same board with a tap-infrastructure qualifier.

## Integration dependency timeline

| Step | Gate | Target |
|---|---|---|
| 1. Get the real GoTab/Fishbowl integration status + date from the vendors | Named D06 production gate – currently "pending", undated | Week 1–2 post-CP1 |
| 2. Interim manual layer: weekly GoTab transaction export → days-since-last-keg sheet → hand-triggered 75/90 sends | None – do not wait for the integration | Immediately |
| 3. Data model fields configured; switcher flag + provenance capture live at counter | GoTab field configuration | Month 1 |
| 4. Automated interval-based flows live (60/75/90 fallback included) | Integration complete; KR 2.1 says live within 90 days of that | Integration + 90 days |
| 5. Delivery (Uber Direct) and lease-to-buy data folded in | Respective GoTab features live | When shipped |

The interim manual layer matters most: at 206 owners / 96–113 active, a weekly export and a sorted spreadsheet is a 30-minute job that captures most of the automation’s value **now**, while proving the send-and-save logic the automation will inherit.

## Cost and kill criteria

Incremental spend ≈ **$0 media**; costs are Fishbowl/GoTab subscription (already paid), possible ESP (#47, [TBC]), and Harry’s hours (~2–3 hrs/week interim). Kill criteria: if after two quarters the at-risk save rate sits below 15% and winbacks below 10, the offers are wrong – rework offers, not the system; the system’s data value stands regardless. There is no scenario at current scale where this build is abandoned.

## Assumptions & open items

- Fishbowl capability set (B2B records, flow builder, SMS) unverified – may push the wholesale board and sends to companion tools **[TBC]**.
- GoTab/Fishbowl integration date unknown – the whole automation tier is hostage to it; interim manual layer is the hedge.
- Churn-rate, attach-rate and at-risk baselines are TBC pending GoTab cohort data (#19).
- Consent state of existing phone/email records unaudited (Spam Act) – audit before any automated sending (#47).
- Membership pricing reconciliation required before renewal flows and LTV maths lock.

---

*Feeds into: #47 EDM Plan (delivery layer), #46 Paid Media Plan (audiences + attribution), #50 Events Plan (high-value invites), DS03 Marketing Plan, and the franchise playbook thesis (#18 – documented, replicable systems).*
