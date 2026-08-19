# 47 — EDM Plan (Email + SMS)
## Tap That Brewery

| | |
|---|---|
| **Document** | EDM Plan — catalogue #47 |
| **Engagement** | Jewell Projects × Tap That Brewery |
| **Phase** | 02 Design |
| **Status** | Draft v01 — Internal |
| **Date** | 19 August 2026 |
| **Prepared by** | Jewell Projects |

*Pre-CP1 draft — produced ahead of Discover sign-off; census data, membership pricing reconciliation and competitor verification may revise inputs.*

---

## Why EDM is the highest-ROI channel available

Tap That Brewery already owns the lists — it just doesn't work them. The 3-month buying cycle is "currently nurtured by memory" (D06), churn management is one hand-sent monthly SMS, and the mailing list is literally a membership tier (Brew Buds). Email and SMS cost near-zero per send, need no ad-policy approvals, and are the only channels that can run the 90-day nurture and the 60/75/90-day lifecycle clock at zero media budget. On a loss-making P&L, this channel comes **before** paid media, not after.

## List assets today

| List | Size / mechanics | State |
|---|---|---|
| **Brew Buds** (free membership = mailing list) | Free tier, 50 Tap Tokens on join, in-venue signup ("5 ways to support us" sign) | Exists; size **[TBC]**; engagement history unknown |
| **Giveaway entrants** | ~1,000 entries per round, 2×/yr — the largest intent list the business builds | Collected each cycle; unclear whether entrants roll into an ongoing list with consent **[TBC]** |
| **Member base** | Keg Crew ($250/yr — pricing to reconcile) + Mug Club ($120/yr) | Known customers, highest value; count **[TBC]** |
| **Refill customer records** | 220 active + at-risk + churned, with phone numbers (SMS winback proves it) | In GoTab; not yet a segmented marketing list — see #48 |

First job before any sequence: audit consent (Spam Act 2003 — express or inferred consent per contact, working unsubscribe, sender ID) and confirm giveaway entry forms capture marketing opt-in for ongoing use, not just the promotion.

## The six sequences to build (in this order)

| # | Sequence | Trigger | Shape | Why this priority |
|---|---|---|---|---|
| 1 | **Giveaway nurture (90 days)** | Giveaway entry | Matches the #07 phasing — Spark (days 0–14): welcome, "that's a keg system?" content, taproom invite. Negotiate (15–60): one objection per touch — Afterpay/Zip and at-cost honesty; her taps (the 1/3 non-beer wall); footprint proof + 5L mini $225; census stat (70% of daily users pour 1–2 kegs/month). Close (61–90): 50%-off close (proven 22–25 conversions), lease-to-buy once live, Keg Crew attached at purchase. Post-90: slow lane — seasonal releases, next giveaway | The proven conversion mechanic with the proven list; directly serves KR 1.2 (35+ per cycle) |
| 2 | **New-owner onboarding** | System purchase in GoTab | Day 0 setup + pour guide; day 3 "first weekend" check-in; day 7 membership pitch (the $30-off maths repays $250/yr in ~4 months at 2 refills/month); day 21 refill reminder + Kegged & Ready board; day 30 referral ask (1,000 Tap Tokens per system referral) | Sets the refill cadence at the moment habit forms; feeds KR 1.4 (60% membership attach) |
| 3 | **Refill cadence reminder** | ~21–25 days since last fill (cadence ≈ 2 kegs/month) | "What's pouring" email built off the coolroom Kegged & Ready pipeline (Tropical Hazy, Smuggler's Haze, Espresso Martini…) — answers the range-paralysis pain ("I just get the lager because I don't know what's pouring") | Keeps actives active — cheaper than any save |
| 4 | **At-risk save (60/75/90)** | Days since last keg | Day 60 email: fresh-range nudge, no discount. Day 75 (at-risk): SMS + email, service angle ("drop the corny Tuesday, ready Friday") or delivery once live. Day 90: winback offer fires (below) | Replaces the post-churn patch with a pre-churn save; serves KR 2.2 (≥40% at-risk save) |
| 5 | **Winback ladder** | Crossing 90 days | Offer ladder, tracked per offer: $20-off/2-week window (current) → Marie's Pizza Buttercard test → next tested offer. Tone acknowledges the truth: churned customers are lapsed, not lost ("hadn't gotten around to it") | Automates today's manual SMS; serves KR 2.3 (30 winbacks) |
| 6 | **Member renewal** | 45 / 14 / 0 days pre-expiry | Restate the used value in dollars ("your $30-off saved you $X this year"), birthday 5L keg reminder, tasting-night invite as the emotional hook | Protects the LTV engine; blocked until membership pricing is reconciled |

Sequences 4–6 fire off GoTab transaction data — they are designed here but **delivered by the #48 CRM build**. Sequences 1–3 can start manually-triggered (CSV upload per giveaway cycle) before any integration lands.

## Content style

House voice as observed in venue: cheeky, pun-forward, effort-free Aussie warmth — "Tap That Knockoffs", "Skittle Me This", "5 ways to support us — total $0.00". Rules: subject lines earn the pun, body copy earns the click; kudos/connection lead, cost closes (the dirty-little-secret rule); every send has exactly one job and one button; SMS reserved for time-critical touches only (at-risk day 75, winback, event-day) — it is the channel that already works and over-use burns it. Responsible-consumption footer on all sends; 18+ list only.

## Tooling

**[TBC — current ESP unknown.]** Discovery surfaced no email platform; SMS is sent manually today. Requirements for selection: native or Zapier-grade connection to GoTab/Fishbowl (the #48 dependency), combined email+SMS in one tool so lifecycle logic isn't split, behaviour-triggered flows, AU compliance features, and pricing that fits a loss-making P&L — entry-level lifecycle tools run roughly **$0–100/month at these list sizes**; anything quoted materially above that band is over-buying at this stage. Fishbowl itself may cover part of this (it is a hospitality CRM/marketing product) — evaluate before adding a second tool.

## Measurement and kill criteria

- Per sequence: delivery, open, click, and the truth metric — transactions in GoTab within the window (entries→systems for seq 1; refills for seq 3–5; renewals for seq 6).
- Giveaway nurture is validated if cycle conversion beats the 22–25 baseline; kill individual touches, not the sequence, on underperformance.
- At-risk save: if the 75-day SMS saves fewer customers than the old monthly blast over one quarter, rework the offer before adding volume.
- List health: unsubscribe >2% on any send = content/frequency review before the next send.

## Assumptions & open items

- List sizes, ESP status, and consent state all **[TBC]** — audit is the first deliverable.
- Giveaway entry forms may need rebuilding to capture ongoing marketing consent and ad-matching consent (feeds #46 custom audiences).
- Sequences 4–6 depend on the GoTab/Fishbowl integration (timeline is a named D06 production gate).
- Membership renewal sequence blocked on pricing reconciliation ($250/yr vs $300 + $120/yr posters).
- The census moderation stat (70% / 1–2 kegs) must be re-verified from raw data before appearing in customer-facing copy (#07 open item).
- Cadence trigger (~21–25 days) is inferred from ~2 kegs/month; tune against actual GoTab inter-purchase data.

---

*Feeds into: #48 CRM Plan (trigger delivery), #46 Paid Media Plan (entrant audiences), DS03 Marketing Plan. Depends on: consent audit, ESP decision, GoTab/Fishbowl integration.*
