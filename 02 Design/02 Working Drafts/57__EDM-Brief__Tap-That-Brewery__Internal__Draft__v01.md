# 57 — EDM Brief
## Build brief: email/SMS sequences, in priority order

| | |
|---|---|
| **Document** | EDM Brief — catalogue #57 |
| **Engagement** | Jewell Projects × Tap That Brewery & Keghouse |
| **Phase** | 02 Design |
| **Status** | Draft v01 — Internal |
| **Date** | 19 August 2026 |
| **Prepared by** | Jewell Projects |

*Pre-CP1 draft — produced ahead of Discover sign-off; census data, membership pricing reconciliation and competitor verification may revise inputs.*

---

## The job

Build three automated sequences, in this order. Copy source: **Brand Copy Workbook** [not yet drafted — until it lands, draft copy from #27 opening messages and #12 contrast lines, flagged for voice pass]. Platform: Fishbowl (CRM of record, #58); SMS retained for lifecycle nudges since the current manual SMS proves the channel works.

## Sequence 1 — Giveaway nurture (FIRST)

The proven engine, currently unnurtured: ~1,000 entries/cycle, 50%-off close converts 22–25; target 35+ (#19 KR 1.2, H3). The 3-month buying cycle is currently nurtured by memory — this sequence replaces memory.

| # | Timing | Content | Job |
|---|---|---|---|
| 1 | Entry +0 | Confirmation + "while you wait" venue invite (tasting paddle) | Get them into the room where 20–30% convert |
| 2 | +7d | Which-system chooser (2-tap $975 → 6-tap) + at-cost explanation | Educate |
| 3 | +14d | Objection 1: partner veto → the 1/3 non-beer tap wall, her-drinks beat | Disarm |
| 4 | +21d | Objection 2: "I'll drink too much" → census (70% of daily users, 1–2 kegs/month) + cost maths as quiet close | Disarm + justify |
| 5 | +28d | Real-customer story (UGC from #54) + demo booking CTA | Social proof |
| 6 | Competition close | Winner announced + **50%-off offer, deadline explicit** | The close |
| 7–8 | Close +7d/+14d | Offer reminders; final: Afterpay/Zip + lease-to-buy [if live] | Sweep |

Non-winners who don't buy roll into a monthly newsletter (new taps from the Kegged & Ready board, events, leaderboard) for the rest of the 3-month cycle.

## Sequence 2 — At-risk automation (SECOND)

Replaces the hand-sent monthly $20-off SMS. Triggered off GoTab/Fishbowl lifecycle states (#58): active <75 days, at-risk 75–90, churned 90+. H4: pre-churn nudge beats post-churn discount.

| Trigger | Channel | Message |
|---|---|---|
| Day 60 since last keg | Email | No offer — new-on-tap tease from the coolroom board, "your keg's getting lonely" voice territory |
| Day 75 (at-risk) | SMS + email | Soft nudge + member reminder ($30 off applies) or light offer [TBC] |
| Day 90 (churned) | SMS | Winback ladder: $20-off/2-week window → Marie's Pizza Buttercard test → next tested offer; response rates recorded per offer (#19 KR 2.3) |

Kill condition for manual SMS: the day this sequence fires reliably, the manual process stops.

## Sequence 3 — Onboarding (THIRD)

New system buyer → refill habit + membership. Trigger: system purchase in GoTab.

1. +0: Welcome + setup/care guide + the $40–100 bonus credit reminder (it exists to force the first fill — say so warmly).
2. +7d: First-refill prompt + Keg Crew pitch (repays in ~4 months at 2 refills/month) — supports the 60% attach target (#19 KR 1.4). **Blocked on membership price reconciliation.**
3. +21d: Referral push (1,000 Tap Tokens per system referral, 500 per refill) + review ask (feeds #55).

## Data & trigger requirements (from #58)

- 100% of keg transactions attached to a customer record; last-keg-date computed field; lifecycle state flags; membership status; own-a-system-elsewhere flag; consent status + source.
- Web forms (#53) write directly to Fishbowl with consent timestamp.

## Compliance (Spam Act 2003 (Cth))

- Express or inferred consent recorded per contact before any commercial send; giveaway entry consent checkbox is explicit, not pre-ticked.
- Every email and SMS carries sender identity and a **functional unsubscribe**, honoured within 5 business days (automate immediately); SMS opt-out ("STOP") wired.
- Age-appropriate list hygiene: no known under-18 contacts; alcohol-offer content follows ABAC tone rules (#56).

## Success criteria

1. Sequences live in priority order; Sequence 2 fires from real transaction data, not manual lists.
2. Giveaway cycle conversion measured against the 22–25 baseline; at-risk save rate reportable (#19 KR 2.2 ≥ 40% target).
3. Zero sends without consent records; unsubscribe tested end-to-end before launch.

## Assumptions & open items

- Brand Copy Workbook pending — all copy above is structural, not final voice.
- Sequence 2 timing hostage to GoTab/Fishbowl integration (#58); interim: run day-60/75/90 pulls off exported lists semi-manually.
- Day-75 offer, incentive economics and lease-to-buy availability [TBC].

---

*Feeds into: #58 CRM Brief (trigger spec), #56 Paid Media Brief (scale gate), #61 Final Brief Pack.*
