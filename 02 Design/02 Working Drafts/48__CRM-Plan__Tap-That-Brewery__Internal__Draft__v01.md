# 48 – CRM Plan
## Tap That Brewery

| | |
|---|---|
| **Document** | CRM Plan – catalogue #48 |
| **Engagement** | Jewell Projects × Tap That Brewery |
| **Phase** | 02 Design |
| **Status** | Draft v01 – Internal |
| **Date** | 19 August 2026 |
| **Prepared by** | Jewell Projects |

> **Evidence note (19 Aug 2026).** Figures in this draft predate the client’s census and planning documents. Several have been corrected; some interpretations are still under revision. Read `20A Evidence Reconciliation` before citing anything here.

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

## Lifecycle automation: the 60/75/90 engine

Replaces the manual monthly SMS with triggers computed from days-since-last-keg:

| Day | State | Automated action | Replaces |
|---|---|---|---|
| ~21–25 | Active, cadence due | "What’s kegged & ready" email (#47 seq 3) | Nothing – new revenue protection |
| 60 | Active, drifting | Email nudge, no discount – range/freshness angle | Nothing |
| 75 | **At-risk** | SMS + email: service/convenience angle (corny Tue→Fri, delivery when live). No discount yet – don’t train discount-waiting | The untargeted blast |
| 90 | **Churned** | Winback ladder fires: $20-off/2-week window → Marie’s Pizza Buttercard → next tested offer; response rate logged per offer | The manual monthly SMS |
| 90 + 60 | Dormant | Quarterly-max touch: giveaway invite, seasonal release, event invite | Nothing (list currently goes dark) |

Every send and every response is written back to the record, so the at-risk save rate (KR 2.2 target ≥40%) and winback count (KR 2.3 target 30/yr) become dashboard numbers instead of anecdotes.

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
| Lead (DM reply / referral / venue-hire enquiry) | Logged same day, every lead | Raef |
| Contact passed (manager name/number received) | **First follow-up within 48 hours** (KR 3.4) | Raef → founder for closes |
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
| 4. Automated 60/75/90 flows live | Integration complete; KR 2.1 says live within 90 days of that | Integration + 90 days |
| 5. Delivery (Uber Direct) and lease-to-buy data folded in | Respective GoTab features live | When shipped |

The interim manual layer matters most: at 206 owners / 96–113 active, a weekly export and a sorted spreadsheet is a 30-minute job that captures most of the automation’s value **now**, while proving the send-and-save logic the automation will inherit.

## Cost and kill criteria

Incremental spend ≈ **$0 media**; costs are Fishbowl/GoTab subscription (already paid), possible ESP (#47, [TBC]), and Raef’s hours (~2–3 hrs/week interim). Kill criteria: if after two quarters the at-risk save rate sits below 15% and winbacks below 10, the offers are wrong – rework offers, not the system; the system’s data value stands regardless. There is no scenario at current scale where this build is abandoned.

## Assumptions & open items

- Fishbowl capability set (B2B records, flow builder, SMS) unverified – may push the wholesale board and sends to companion tools **[TBC]**.
- GoTab/Fishbowl integration date unknown – the whole automation tier is hostage to it; interim manual layer is the hedge.
- Churn-rate, attach-rate and at-risk baselines are TBC pending GoTab cohort data (#19).
- Consent state of existing phone/email records unaudited (Spam Act) – audit before any automated sending (#47).
- Membership pricing reconciliation required before renewal flows and LTV maths lock.

---

*Feeds into: #47 EDM Plan (delivery layer), #46 Paid Media Plan (audiences + attribution), #50 Events Plan (high-value invites), DS03 Marketing Plan, and the franchise playbook thesis (#18 – documented, replicable systems).*
