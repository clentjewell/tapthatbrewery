# 26 — Measurement Plan
## Tap That Brewery & Keghouse

| | |
|---|---|
| **Document** | Measurement Plan — catalogue #26 |
| **Engagement** | Jewell Projects × Tap That Brewery & Keghouse |
| **Phase** | 02 Design |
| **Status** | Draft v01 — Internal |
| **Date** | 19 August 2026 |
| **Prepared by** | Jewell Projects |

*Pre-CP1 draft — produced ahead of Discover sign-off; census data, membership pricing reconciliation and competitor verification may revise inputs.*

---

One rule: if a number doesn't move active keg customers or explain why they moved, it isn't reported. Sized for Raef (~70% marketing) plus two founders — a one-page weekly, a one-hour monthly, nothing more.

## North-star metric

**Active keg customers** — customers with a keg purchase within 75 days (the business's own definition). Today 220; target 1,000; every phase gate in #25 is denominated in it. Reported with its two shadows: **at-risk** (75–90 days) and **churned** (90+).

## Supporting metrics

| Metric | Definition | Why it matters | Source |
|---|---|---|---|
| Refills/month | 20L-equivalent fills per month, and per active (baseline ~2) | Validates the ~$200/month economics behind the ~$2.6M target | GoTab |
| Churn & saves | Actives crossing 90 days; at-risk customers recovered by 60/75/90-day touches | The leak automation exists to plug (H4) | GoTab + Fishbowl |
| Switcher adds | New refill customers whose system wasn't bought here | P1's headline; the 50%-organic figure becomes a managed channel (H1) | GoTab (flag at first fill) |
| Giveaway → purchase | Entrants (~1,000/cycle) → systems bought; today 22–25 via the 50% close | Nurture (H3) must beat this or it isn't working | Entry list + GoTab |
| Taproom → system | % of visitors buying a system (client estimate 20–30%) | The venue's entire justification, measured | Demo QR/CTA capture + GoTab |
| CAC by channel | Spend ÷ new actives: switcher ads, giveaway, taproom, referral, JV/club | Decides where next dollar and Raef-hour go | Meta/Buffer spend + GoTab |
| Member share of refills | % of refills on Keg Crew ($250/yr, $30 off/refill) | Membership is the retention lock; also flags lapsed members early | GoTab |
| Referral redemptions | Tap Token referral rewards claimed (1,000/system, 500/refill) | Cheapest channel; currently wall-signage only | GoTab / Tap Tokens |

## Data sources and their jobs

- **GoTab (POS)** — transactions, refill cadence, membership, lifecycle clock. The system of record for the north star.
- **Fishbowl (CRM)** — segments, automated lifecycle sends, open/click/redemption. *Integration pending — until live, lifecycle metrics run off manual GoTab exports.*
- **Buffer + @tapthatbreweryandkeghouse socials** — reach/engagement as diagnostics only; never in the headline row.
- **Site analytics (tapthatbrewery.com.au)** — switcher landing page traffic and conversion; giveaway entries.
- **Census + surveys** — objection tracking (n=50 baseline: 70% of daily users drink 1–2 kegs/month); repeat annually.

## Current measurement gaps

1. **No churn-rate baseline** — 75/90-day definitions exist, but no counted monthly flow between states. First job after integration.
2. **Switchers aren't flagged** — the 50% figure is an estimate; add a one-question flag at first fill ("where's your system from?").
3. **Taproom conversion is folklore** — 20–30% is a client estimate with no capture mechanism.
4. **No channel attribution** — spend and Raef-hours aren't tied to new actives anywhere.
5. **Giveaway entrants aren't tracked post-competition** — the 3-month cycle happens in the dark.
6. **Census data not yet received** (Clent → Jules, carried action) — pillar messaging and delivery pricing rest on headline figures only.

## Reporting rhythm

**Weekly (15 min, Raef compiles Monday):** actives / at-risk / churned counts; refills last 7 days; switcher adds; new system sales; one line on what changed. Single page, same template, posted where founders see it.

**Monthly (1 hour, Raef + Chris + Justin):** north star vs phase gate (#25); churn and saves; CAC by channel; member share; giveaway funnel when a cycle is live; one decision recorded — what gets more effort, what gets less. Kill or scale one thing every month.

**Quarterly (within monthly, extended):** milestone gate review against #25; hypothesis scorecard (H1–H7: supported / refuted / untested); census or pricing refresh check.

## Assumptions & open items

- Assumes GoTab can export lifecycle-state counts and flag switchers/members per transaction — capability to confirm.
- Fishbowl integration timing unknown; until live, weekly numbers are manual exports (~30 min, acceptable short-term).
- CAC requires spend logging discipline from day one — a shared sheet is fine [needs P&L data for fully loaded CAC].
- Site analytics tooling unconfirmed — verify what tapthatbrewery.com.au currently runs.

---

*Feeds into: #23 Business Plan (financial validation), #25 Growth Roadmap (phase gates), the Design-phase Marketing Plan, and Deploy-phase reporting.*
