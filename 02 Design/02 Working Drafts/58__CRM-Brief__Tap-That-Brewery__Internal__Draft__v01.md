# 58 — CRM Brief
## Implementation brief: GoTab × Fishbowl lifecycle engine

| | |
|---|---|
| **Document** | CRM Brief — catalogue #58 |
| **Engagement** | Jewell Projects × Tap That Brewery & Keghouse |
| **Phase** | 02 Design |
| **Status** | Draft v01 — Internal |
| **Date** | 19 August 2026 |
| **Prepared by** | Jewell Projects |

*Pre-CP1 draft — produced ahead of Discover sign-off; census data, membership pricing reconciliation and competitor verification may revise inputs.*

---

## The job

Complete the GoTab (POS) → Fishbowl (CRM) integration and stand up the lifecycle engine on top of it. This is the single highest-leverage build in the programme: every month it slips, retention stays a hand-sent monthly SMS and the warm list of 220 actives leaks refill revenue. It gates #57 Sequence 2 and the #56 scale-up (see critical path, #61).

## Integration scope

| In scope | Detail |
|---|---|
| Transaction sync | Every GoTab keg transaction (20L/5L/50L refill, corny fill, system, membership, Benchy) to the Fishbowl customer record, daily or better |
| Identity resolution | One customer = one record across POS, web forms (#53), giveaway entries, Tap Tokens; dedupe rule on mobile then email |
| Computed lifecycle state | days_since_last_keg → **Active <75 / At-risk 75–90 / Churned 90+**, recalculated nightly |
| Trigger events out | Day-60 / 75 / 90 events fire #57 automations (email + SMS), replacing the manual monthly SMS |
| Web capture in | demo_booked, giveaway_entry, function_enquiry land as records with consent timestamp + UTM source |
| Out of scope (phase 2) | Uber Direct delivery data, lease-to-buy contract handling, franchise reporting |

## The 60/75/90 trigger set (replaces manual SMS)

| Trigger | Fires | Condition guards |
|---|---|---|
| Day 60 | Nudge email (#57) | Skip if a purchase or an open winback offer exists |
| Day 75 | At-risk SMS + email | Tag cohort for save-rate reporting (#19 KR 2.2) |
| Day 90 | Winback SMS (offer ladder) | Offer variant recorded per send; suppress after 2 winback cycles without response [cadence TBC] |

## Required fields

customer_id · name · mobile · email · suburb/postcode · consent status/date/source · segment self-select (backyard/shed/office/club) · **own_system_elsewhere (Y/N)** — the switcher flag, set at first fill (#19 KR 1.1) · system_owned (type, purchase date, bought-from-us Y/N) · membership tier + expiry · last_keg_date · lifecycle_state · lifetime keg count/value · Tap Token balance (or link) · referral source · winback offers sent/redeemed.

## Required views (Raef + founders, no analyst)

1. **Active count this week** — the one number (#24 P6): actives, trend, vs the 220 → 1,000 path.
2. **At-risk board** — everyone at 60–90 days, last contact, next trigger due.
3. **Switcher intake** — new actives flagged own_system_elsewhere, monthly (target ~7–8/month).
4. **Membership attach** — memberships ÷ systems sold, monthly (target 60%).
5. **Giveaway cohort** — entrants by cycle: nurture stage, demo booked, purchased.

## Wholesale pipeline stages

Fixes the admitted DM-lead leakage. Simple pipeline, 48-hour first-follow-up SLA (#19 KR 3.4):

`Lead (DM/referral) → Contact identified → Tasting/style-match sent → Trial keg → Pouring (account) → Dormant`

Fields: venue name, style match (Japanese lager → Japanese restaurant etc.), decision-maker, source, next action + date. White-label club deals tracked in the same pipeline with a deal-type flag.

## Test plan

1. **Sync integrity:** 20 known transactions posted in GoTab appear correctly attached in Fishbowl within the sync window; target 100% attach rate on new transactions (#19 KR 2.4).
2. **Lifecycle maths:** seed test customers at day 59/61/74/76/89/91; verify state transitions and that exactly the right triggers fire — and suppress on purchase.
3. **End-to-end:** website demo form → record → consent stored → test sequence send → unsubscribe honoured → state visible in views.
4. **Backfill audit:** historic customer base imported, last_keg_date computed, current 220-active figure reconciled against the client's own count before go-live.
5. **Manual cutover:** run manual SMS and automation in parallel for one cycle; then manual stops.

## Success criteria

Integration live; triggers replacing manual SMS after one parallel cycle; the five views populated and used in the weekly review; wholesale pipeline holding every open lead with an SLA date.

## Assumptions & open items

- GoTab/Fishbowl integration capability and timeline unconfirmed — the named production gate from D06. If it slips past Stage 1, triggers run semi-manually off exported lists (per #24).
- Data ownership/API access, historic data quality, and Tap Tokens system-of-record [TBC].
- Winback suppression cadence and day-75 offer economics [TBC with client].

---

*Feeds into: #57 EDM Brief, #56 Paid Media Brief (scale gate + first_fill feedback), #60 Events Brief (capture flows), #61 Final Brief Pack.*
