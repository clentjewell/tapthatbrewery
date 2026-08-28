# 66 – Campaign Launch Runbook
## Tap That Brewery · How a campaign window goes live

| | |
|---|---|
| **Document** | Campaign Launch Runbook – catalogue #66 |
| **Engagement** | Jewell Projects × Tap That Brewery |
| **Phase** | 03 Deploy |
| **Status** | Draft v01 – Internal |
| **Date** | 28 August 2026 |
| **Prepared by** | Jewell Projects |
| **Descends from** | #43 In-Market Activation Plan · #45 Campaign Calendar |

*Pre-CP1/CP2 draft – Deploy runbooks are written ahead of both gates. Nothing here should be executed until the Design plan it descends from is approved.*

---

## What this runbook is

One repeatable sequence for taking any of the four campaign windows in #45 from approved plan to live in market. It is deliberately channel-agnostic: the channel runbooks (#67–#74) are the sub-procedures this one calls. Run it once per window – C1 Switcher (Sep 26), C2 Giveaway cycle 1 (Oct–Dec 26), C3 Giveaway cycle 2 (Jan–Feb 27), C4 Benchy (Mar–May 27).

The whole sequence is sized for one marketer at ~70% capacity plus Jewell build support. If a step has no named owner on the day, the window moves – it does not stack.

## T-minus schedule

| When | Step | Owner | Done looks like |
|---|---|---|---|
| T-21d | **Window brief locked** – objective, audience, offer, budget, one primary metric | Jewell | One page, signed by Justin. No creative starts before it |
| T-21d | Confirm the Design plan this window executes is CP2-approved | Jewell | Written confirmation, or the window does not open |
| T-18d | **Claim audit** on every price/saving statement in the brief | Jewell | See "Claim audit" below – blocking |
| T-14d | Landing page or entry page built and QA’d on mobile | Jewell | Loads <3s on 4G, form submits to a real inbox, consent tick present |
| T-14d | Tracking live before any creative (#75) | Jewell | Test event fires end-to-end and lands in the report |
| T-10d | Creative produced – 3 concepts minimum per audience | Jewell + Harry/Harry | Files named `C{n}-{audience}-{concept}-{ratio}` |
| T-10d | Alcohol-advertising review (ABAC) on every asset | Jewell | Checklist below signed |
| T-7d | Ad accounts built, audiences saved, budgets set but **paused** (#68) | Jewell | Screenshot filed |
| T-7d | Organic content scheduled in Buffer (#67) | Harry/Harry | 2 weeks queued |
| T-5d | Lifecycle sends built and test-sent (#69) | Jewell | Test to three internal addresses, links clicked |
| T-3d | **Counter script briefed to bar staff** | Harry/Harry | Staff can say the offer without reading it |
| T-2d | Stock, prize or product availability confirmed | Chris | Written confirmation from production |
| T-1d | Go/no-go call, 15 minutes | Justin, Harry/Harry, Jewell | Every pre-flight line green or explicitly waived |
| T-0 | **Unpause paid, publish organic, send email 1** in that order | Jewell then Harry/Harry | First conversions visible in the report inside 24h |

## Pre-flight checklist (the go/no-go call reads this aloud)

| # | Check | Blocking? |
|---|---|---|
| 1 | Every price claim is true for a **non-member** or is explicitly labelled member-only | **Yes** |
| 2 | Tracking fires and the destination report shows the test event | **Yes** |
| 3 | Consent capture on every form: email, SMS and ad-matching ticked separately, 18+ confirmed | **Yes** |
| 4 | Responsible-consumption line on every public asset; no audience under 18 in targeting | **Yes** |
| 5 | Landing page price list matches what the till charges today | **Yes** |
| 6 | Membership pricing shown matches the reconciled figure (open item #2 – if unresolved, membership is **omitted**, not guessed) | **Yes** |
| 7 | Staff can answer the top three questions the campaign will generate | No – but brief within 48h |
| 8 | Rollback path known: which ads to pause, which page to unpublish | **Yes** |

## Claim audit – mandatory, every window

Two known errors must not enter any new creative:

| Claim | Status | Correct form |
|---|---|---|
| "$2.34 a schooner" | **Wrong as run** – it is member-only. But the replacement is not settled either: our $2.98 assumes a $140 keg at 47 schooners, while the verified price list gives $2.55 member and $3.19 non-member, and Christy's figure is $2.70. Open item #19. | Pull the claim. Do not substitute a number until #19 closes; run the creative without a per-schooner figure in the meantime. |
| Keg Crew break-even "6 kegs" | **Wrong as briefed to staff.** $250 ÷ $30 = 8.33 | "Pays for itself at nine refills a year" |

Rule: any comparative claim ("vs $14 at the pub") is written with its assumptions on the same asset, in legible type. If the assumption doesn’t fit, the claim doesn’t run.

## What "live" means, and what it doesn’t

A window is live when paid is delivering, organic is publishing on cadence, the lifecycle sequence is firing, and the counter script is being spoken. It is **not** live because the ads are approved. The day-1 job is confirming all four, not celebrating the launch.

## Stop conditions

Pause the window – all channels, same hour – if any of these occur:

- A price or saving claim is found to be wrong in market.
- A complaint is received on responsible-service or audience-age grounds.
- The landing page or entry form is failing to capture (zero submissions in 24h with traffic arriving).
- Stock, prize or install capacity cannot meet the offer being made.

Restart requires a corrected asset and a second go/no-go call. Nobody restarts a paused window alone.

## Measurement hooks

Every window reports the same five lines in the monthly one-pager (#26): new actives attributed, cost per new active, primary-metric result vs target, spend vs budget, and one sentence on what to change. Baselines are frozen in #65 before T-0 – the campaign cannot be its own baseline.

## Dependencies

CP2 sign-off · tracking build (#75) · reconciled membership pricing (open item #2) · GoTab postcode export for geo-targeting · prize budget sign-off for giveaway windows (Justin).

*Feeds into: #75 Tracking Setup, #76 Optimisation Backlog, #65 Case Study Evidence Pack.*
