# 68 – Paid Media Launch
## Tap That Brewery · Standing up the $1,500/month Meta programme

| | |
|---|---|
| **Document** | Paid Media Launch – catalogue #68 |
| **Engagement** | Jewell Projects × Tap That Brewery |
| **Phase** | 03 Deploy |
| **Status** | Draft v01 – Internal |
| **Date** | 28 August 2026 |
| **Prepared by** | Jewell Projects |
| **Descends from** | #46 Paid Media Plan · #56 Paid Media Brief |

*Pre-CP1/CP2 draft – Deploy runbooks are written ahead of both gates. Nothing here should be executed until the Design plan it descends from is approved.*

---

## What changed since #46 was drafted

Two facts arrived with the client’s documents and they reshape this runbook:

1. **A budget already exists.** $1,500/month is committed, split Awareness $500 · Taproom Traffic $400 · Competitor Switching $300 · Retargeting $300, with a scaling ladder of $20 → $30 → $50/day.
2. **A prior agency already ran Meta campaigns.** An ad account with historical creative and performance data exists. #46 was written assuming a standing start; it isn’t one.

So this is not a launch from zero. Step one is recovering what was already learned.

## Phase 0 – Account recovery (before a dollar is spent)

| # | Step | Owner | Timing | Done |
|---|---|---|---|---|
| 0.1 | Obtain admin access to the existing Meta Business Manager and ad account | Justin → Jewell | Week 1 | Jewell has admin, not partner-agency, access |
| 0.2 | Export 24 months of campaign, ad-set and ad-level performance | Jewell | Week 1 | CSV filed in `03 Deploy` |
| 0.3 | Identify top-5 and bottom-5 creatives by cost per result; note what was tested and what never was | Jewell | Week 2 | One-page read-out |
| 0.4 | Audit the pixel: is it installed, firing, and are events named usefully? | Jewell | Week 2 | Event Manager screenshot |
| 0.5 | Recover custom audiences, lookalikes and any retained entrant lists | Jewell | Week 2 | Audience inventory |
| 0.6 | Confirm page roles, payment method, spend limits and 18+ enforcement | Jewell | Week 2 | Settings screenshot |

If access cannot be recovered, say so in writing and rebuild – but do not rebuild first. Reconstructing an account that already exists wastes the one asset that came free.

## Phase 1 – Structure build (week 3)

Five campaigns, matching the committed split. Built paused.

| Campaign | Monthly | Objective | Audience construction | Creative lead |
|---|---|---|---|---|
| **Awareness** | $500 | Reach / video views | GC geo, 40–60 primary (65% of the base is 41–60), plus 28–40 secondary. Interest: craft beer, home entertaining, BBQ | Taste & freshness – the #1 driver (2.19). Brewery floor, award story |
| **Taproom traffic** | $400 | Traffic / store visits | 15km radius Burleigh Heads; event-night dayparting | Venue, music nights, what’s pouring. Taproom is the #1 acquisition source at 22% |
| **Competitor switching** | $300 | Conversions (first fill) | Behavioural: kegerator/homebrew interest, competitor engagers. **The prize is ~116 of 206 owners who bought elsewhere** | "We fill any system – whoever sold it to you." Freshness + member refill price |
| **Retargeting** | $300 | Conversions | 90-day windows on site visitors, video viewers, entrants – matched to the buying cycle | Objection ladder, one per fortnight. Close creative in days 61–90 |
| **Giveaway burst** | From the above, 2×/yr | Lead | Broad GC 18+, then entrant custom audience for the close | Enter-to-win, then the 50%-off close |

**Geo priority from the census**, replacing guesswork: 4213 Nerang/Carrara · 4209 Coomera · 4211 Mudgeeraba · 4218 Mermaid Waters · 4227 Robina. These carry a higher weight than the Burleigh radius for the switching and awareness campaigns – the customers do not live where the brewery is.

## Phase 2 – Timing the spend to the buying cycle

**43% of buyers take 3+ months; only 34% buy inside a month.** A four-week campaign measured on four weeks of conversions will read as a failure that isn’t one.

| Rule | Application |
|---|---|
| Retargeting windows | 90 days minimum, never 30 |
| Reporting window | Report at 30 days as a leading-indicator read only; the conversion verdict is at 90 |
| Giveaway close | Fires at day 60–90 of the entrant nurture, not at week 2 |
| Budget scaling | $20/day → $30 → $50 only after a full 14 days at the prior step with cost per result holding |

## Phase 3 – Go live (week 4)

Order of operations on launch day: confirm tracking (#75) → unpause Awareness and Taproom Traffic → 48h later unpause Switching → Retargeting unpauses once audiences reach size. Never launch all five the same hour; there is no way to read what happened.

## Compliance gates – blocking, every asset

| Gate | Requirement |
|---|---|
| Audience age | 18+ enforced at ad-set level on every campaign, no exceptions |
| ABAC | No consumption-rate claims, no under-25 talent, no drinking near vehicles or water, no health or performance claims |
| Price claims | Non-member price first, per #66. The live "$2.34 a schooner vs $14 at the pub" ad is pulled before this programme starts. It is not replaced with $2.98 – that figure is unsettled too (open item #19) – so no per-schooner claim runs until #19 closes |
| Alcohol delivery | No delivery creative until the service is licensed and live |

## Kill and scale criteria

| Signal | Action |
|---|---|
| Cost per new active exceeds first-year gross value on a 90-day read | Pause that campaign, reallocate to the best performer |
| An ad set spends $150 with zero landing-page conversions | Kill the creative, not the audience |
| Cost per result holds 14 days at current daily budget | Step up one rung on the ladder |
| Switching campaign beats giveaway on cost per new active | Shift budget toward switching at the next monthly review – it is the cheapest customer in the model |

## Measurement hooks

Weekly: spend, cost per result by campaign, frequency. Monthly into #26: new actives by campaign, cost per new active, and the 90-day cohort read on the previous quarter’s spend.

## Dependencies

Ad account access (open item #16) · pixel and conversion events (#75) · landing pages live · corrected price creative · GoTab postcode export.

*Feeds into: #75 Tracking Setup, #76 Optimisation Backlog, #65 Case Study Evidence Pack.*
