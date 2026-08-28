# 70 – CRM Workflow Deployment
## Tap That Brewery · Standing up the customer record and the lifecycle engine

| | |
|---|---|
| **Document** | CRM Workflow Deployment – catalogue #70 |
| **Engagement** | Jewell Projects × Tap That Brewery |
| **Phase** | 03 Deploy |
| **Status** | Draft v01 – Internal |
| **Date** | 20 August 2026 |
| **Prepared by** | Jewell Projects |
| **Descends from** | #48 CRM Plan · #58 CRM Brief |

*Pre-CP1/CP2 draft – Deploy runbooks are written ahead of both gates. Nothing here should be executed until the Design plan it descends from is approved.*

---

## The blocking unknown, and the way around it

The GoTab × Fishbowl integration date is **outstanding**. Everything in #48 assumes it. This runbook therefore ships in two tracks that run in parallel: a **manual track** that delivers most of the value inside four weeks with a spreadsheet, and an **automated track** that replaces it whenever the integration lands. Nothing waits.

## The definition that has to be settled first

The client’s own documents give three active-customer definitions: 45 days (Customer Success System), 75 days (One-Page Plan), and "2–3 months" (elsewhere). Depending on which is chosen the active base is **96 or ~113**. This is a founders' decision, not a research task, and it must be made before the engine is built – every trigger day, every report line and every target in #19 keys off it.

| Option | Active base | Consequence |
|---|---|---|
| 45-day | ~96 | Tighter, earlier intervention; more customers flagged at-risk who aren’t |
| 75-day | ~113 | Matches the existing winback rhythm; slower to catch drift |

**Recommendation: 75 days**, because the existing lifecycle comms already run on it and changing the clock and building the engine in the same quarter makes failure unattributable. Revisit with six months of real cadence data.

## Phase 1 – Manual track (weeks 1–4, no integration required)

| # | Step | Owner | Output |
|---|---|---|---|
| 1.1 | Export the full customer list from GoTab with last-keg date | Harry/Harry | 206-owner base file |
| 1.2 | Build the minimum viable record in a shared sheet: identity, consent per channel, system owned, **bought-here flag**, last keg date, days-since, membership, tokens, first-touch source | Jewell | One row per customer |
| 1.3 | Backfill the switcher flag from known history; leave unknown blank rather than guessing | Harry/Harry | ~116 of 206 expected to be "elsewhere" |
| 1.4 | Compute the three bands: active, at-risk, churned | Jewell | Three tabs, refreshed fortnightly |
| 1.5 | Counter-capture script live: "what number do we text when it’s ready?" plus "did you buy the system here?" | Harry/Harry, bar staff | Every fill attaches to a record |
| 1.6 | Fortnightly cycle: refresh, segment, hand to #69 | Harry/Harry | 15 minutes, diarised |

The switcher flag is the single most valuable field in the model. **~116 of 206 owners (56%) bought their system elsewhere** – the census’s 31% is response-biased and is not used here. Without the flag, the largest addressable pool in the business is invisible.

## Phase 2 – Automated track (on integration)

| # | Step | Owner | Pre-condition |
|---|---|---|---|
| 2.1 | Confirm the integration writes transaction-level data, not daily totals | Jewell | Vendor confirmation in writing |
| 2.2 | Map GoTab fields to Fishbowl record fields; agree the unique key (mobile) | Jewell | Field map signed off |
| 2.3 | Nightly job computing days-since-last-keg | Jewell | Runs for 7 days in shadow before any send fires |
| 2.4 | Build the 60/75/90 triggers | Jewell | Shadow-run: log who *would* have been messaged, compare to the manual list |
| 2.5 | Cut over sequences 4–5 from manual to automated | Jewell | Two consecutive shadow weeks matching manual within 5% |
| 2.6 | Retire the manual fortnightly pull | Harry/Harry | Only after two clean automated cycles |

Cut-over rule: no sequence goes live off new data until it has shadowed the manual process for two cycles. An automation that mails the wrong 40 people once costs more than three months of spreadsheets.

## The lifecycle engine

| Day | State | Action | Tone rule |
|---|---|---|---|
| 21–25 | Cadence due | "What’s kegged & ready" | Brewery update |
| 60 | Drifting | Range nudge, **no discount** | Brewery update |
| 75 | At-risk | SMS + email, service angle (corny in Tuesday, ready Friday) | Never mention absence |
| 90 | Churned | Winback ladder – $20 off, 7-day window | Never mention absence |
| 150 | Dormant | Quarterly-max: giveaway, seasonal release, event | Invitation only |

Member vs non-member is the strongest predictor available: **18% leakage among Keg Crew members against 44% among non-members.** The engine treats membership attachment as a churn intervention, not a revenue product.

## Data hygiene standard

100% of keg transactions attached to a customer record. Measured weekly as unattached-transaction count; a week above 5% unattached triggers a staff re-brief, not a system change.

## What the CRM must not do yet

- **No subscription launch.** 41% expressed interest and the client’s own analyst recommends against it. Nothing in this build assumes recurring billing.
- **No delivery workflow** until the service is licensed and live; the fields exist (postcode, stock-up flag) but the triggers stay off.
- **No lead-scoring model.** There is no occupational data and no reliable revenue-per-customer figure until Square/GoTab history is accessible (open item #12).

## Measurement hooks

Weekly: unattached transactions, band counts (active / at-risk / churned). Monthly into #26: at-risk save rate, winbacks, switcher acquisitions, member share of refills, membership attach rate on new systems.

## Stop conditions

Integration writing incorrect or partial data · any automated send firing against an unshadowed trigger · consent field missing on any record entering a send.

## Dependencies

Founder decision on the active definition (open item #11) · GoTab × Fishbowl date (open item #4) · Square historical access (open item #12) · consent audit from #69 Phase 0.

*Feeds into: #69 EDM Deployment, #75 Tracking Setup, #65 Case Study Evidence Pack.*
