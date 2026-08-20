# 69 — EDM Deployment
## Tap That Brewery · Building and firing the six sequences

| | |
|---|---|
| **Document** | EDM Deployment — catalogue #69 |
| **Engagement** | Jewell Projects × Tap That Brewery |
| **Phase** | 03 Deploy |
| **Status** | Draft v01 — Internal |
| **Date** | 20 August 2026 |
| **Prepared by** | Jewell Projects |
| **Descends from** | #47 EDM Plan · #57 EDM Brief |

*Pre-CP1/CP2 draft — Deploy runbooks are written ahead of both gates. Nothing here should be executed until the Design plan it descends from is approved.*

---

## The rule that governs every send

The client's own lifecycle plan sets it and it overrides house tone: **never reference inactivity. Every message is a brewery update, not a "we miss you".** A customer who hasn't refilled in 80 days did not decide to leave — 44% leakage among non-members is drift, not defection. The send that names the drift creates it.

## What already runs, and must not be broken

Three lifecycle comms are live today and this build absorbs them rather than replacing them cold:

| Live today | Cadence | Absorbed into |
|---|---|---|
| Stock email to all system owners | Fortnightly | Sequence 3 (refill cadence) — same content, now triggered per customer |
| At-risk nudge | Monthly | Sequence 4 (60/75/90) |
| Lapsed SMS + $20-off, 7-day window | Manual | Sequence 5 (winback ladder) |

Rule: the manual sends continue on their existing rhythm until the automated equivalent has passed two full cycles. No gap between the old and the new.

## Phase 0 — Consent and list hygiene (blocking, week 1–2)

| # | Step | Owner | Done |
|---|---|---|---|
| 0.1 | Export all lists: Brew Buds, Keg Crew, Mug Club, giveaway entrants, GoTab customer records | Raef/Harry | One CSV each, dated |
| 0.2 | Classify consent per contact per channel — express, inferred, or none (Spam Act 2003) | Jewell | Consent column populated; "none" is suppressed, not mailed |
| 0.3 | Confirm giveaway entry forms captured **ongoing** marketing opt-in, not promotion-only | Jewell | If not: those entrants get one permission-request send, then suppression |
| 0.4 | De-duplicate across lists on mobile then email | Jewell | Single record per person |
| 0.5 | Remove role addresses, hard bounces, and anyone under 18 | Jewell | Clean count reported |

## Phase 1 — Deliverability foundations (week 2, before any send)

This was missing from #47 and is not optional.

| Item | Action | Owner |
|---|---|---|
| **SPF** | Publish a single SPF record authorising the chosen ESP; verify no more than 10 DNS lookups | Jewell + domain host |
| **DKIM** | Enable ESP signing, publish the selector, verify pass on a test send | Jewell |
| **DMARC** | Start at `p=none` with `rua` reporting to a monitored inbox; move to `p=quarantine` after 30 days of clean reports | Jewell |
| **Sending domain** | Use a subdomain (e.g. `mail.`) so a marketing reputation problem can't take down transactional or business mail | Jewell |
| **Warm-up** | Week 1: 500/day to the most engaged 20%. Week 2: 1,500/day. Week 3: full list. Never full-blast a cold domain | Jewell |
| **List cleaning** | Suppress 180-day non-openers from broadcast; keep them in trigger-based flows only | Jewell |
| **Reputation monitoring** | Google Postmaster Tools connected; check weekly for the first quarter | Jewell |

Thresholds: bounce >2% or spam complaints >0.1% on any send **stops the programme** until diagnosed.

## Phase 2 — Sequence build order

Built in this order because each one's data feeds the next.

| # | Sequence | Trigger | Build | Live by |
|---|---|---|---|---|
| 1 | **Giveaway nurture (90 days)** | Entry | 5 emails + 2 SMS across days 0–90, closing in the 61–90 window where **43% of the market actually decides** | Before C2 opens |
| 2 | **New-owner onboarding** | System purchase | Day 0 setup · day 3 check-in · day 7 membership · day 21 first-refill reminder · day 30 referral ask | Week 4 |
| 3 | **Refill cadence** | ~21–25 days since last fill | "What's kegged & ready" — replaces the fortnightly blast with a per-customer clock | Week 5 |
| 4 | **At-risk (60/75/90)** | Days since last keg | Day 60 range nudge, no discount · day 75 SMS + email on service/convenience · day 90 hands to sequence 5 | On CRM integration (#70) |
| 5 | **Winback ladder** | Crossing 90 days | $20-off / 7-day window as today, then tested alternatives; response logged per offer | On CRM integration |
| 6 | **Member renewal** | 45 / 14 / 0 days pre-expiry | Value restated in dollars actually saved | **Blocked** on membership pricing reconciliation (open item #2) |

Sequences 1–3 run on manual CSV triggers from day one. Sequences 4–5 need the transaction feed; until GoTab × Fishbowl lands (**date outstanding**), Raef/Harry runs a fortnightly manual pull: export days-since-last-keg, filter to the 60/75/90 bands, upload as three segments, fire the sends. Fifteen minutes a fortnight is the interim price of an unknown integration date.

## Segmentation that the census earned

| Segment | Definition | Treatment |
|---|---|---|
| **Stock-up buyers** | 2+ kegs per fill | 79% delivery interest — first to receive the delivery announcement |
| **Top-up buyers** | ≤1 keg | 40% delivery interest — no delivery push; cadence and range content instead |
| **Weekend-only users** | 35% of base, all ≤1 keg/month | Friday-morning send timing; never a volume message |
| **Members** | Keg Crew / Mug Club | 18% leakage vs 44% — protect hard; renewal and tasting-night invites |
| **Non-members** | Everyone else | 44% leakage — membership maths is the primary message, once the pricing is reconciled |

## Content standards

One job and one button per send. Taste and freshness lead (driver #1 at 2.19); cost is stated plainly and second (driver #2 at 2.75) — not buried. SMS reserved for day-75, winback and event-day only. Every send: unsubscribe that works, physical sender address, responsible-consumption footer, 18+ list.

## Measurement hooks

Per sequence: delivery, open, click, and the conversion the sequence exists to cause. Programme-level into #26: refills triggered by sequence 3, at-risk saves by sequence 4, winbacks by sequence 5, and giveaway entrant → purchase against the 22–25 baseline.

## Stop conditions

Bounce >2%, complaints >0.1%, any send referencing inactivity, or any membership price stated before reconciliation.

## Dependencies

ESP selection (**[TBC]** — evaluate Fishbowl's own marketing module before buying a second tool) · domain DNS access · GoTab export · integration date (open item #4) · membership pricing (open item #2).

*Feeds into: #70 CRM Workflow Deployment, #75 Tracking Setup, #76 Optimisation Backlog.*
