# 75 — Tracking Setup
## Tap That Brewery · Instrumenting before spending

| | |
|---|---|
| **Document** | Tracking Setup — catalogue #75 |
| **Engagement** | Jewell Projects × Tap That Brewery |
| **Phase** | 03 Deploy |
| **Status** | Draft v01 — Internal |
| **Date** | 20 August 2026 |
| **Prepared by** | Jewell Projects |
| **Descends from** | #26 Measurement Plan · #48 CRM Plan |

*Pre-CP1/CP2 draft — Deploy runbooks are written ahead of both gates. Nothing here should be executed until the Design plan it descends from is approved.*

---

## The sequencing rule

Nothing spends before it measures. This runbook is the first Deploy build in the calendar and every other runbook lists it as a dependency. It is also the cheapest: most of what follows is configuration, not money.

## The one number everything rolls up to

**Active keg customers.** The definition is unresolved — 45-day gives ~96, 75-day gives ~113 (open item #11), and this must be settled before the first report, not after. Every other metric here exists to explain a movement in that number or to attribute it to a channel.

## Phase 1 — Web and analytics (week 1)

| # | Step | Owner | Done |
|---|---|---|---|
| 1.1 | GA4 property, AU data region, 14-month retention, IP anonymisation on | Jewell | Realtime shows a test visit |
| 1.2 | Consent banner meeting Australian Privacy Principles; analytics only fires on consent | Jewell | Verified in an incognito session |
| 1.3 | Google Tag Manager container; all tags via GTM, none hard-coded | Jewell | Preview mode clean |
| 1.4 | Meta pixel + Conversions API, deduplicated on event ID | Jewell | Event Manager shows both, no duplicates |
| 1.5 | Google Search Console + Business Profile insights connected | Jewell | 28 days of data flowing |
| 1.6 | UTM convention published and enforced: `source / medium / campaign / content` — `campaign` is always the window code (C1, C2…) | Jewell | One-page convention filed |

## Phase 2 — The event map

Nine events, no more. An analytics setup with forty events is one nobody reads.

| Event | Fires when | Why it exists |
|---|---|---|
| `giveaway_entry` | Entry form submitted | The proven demand mechanic; the entry point of the 90-day nurture |
| `demo_booking` | Demo or Bring a Mate request submitted | 63% said they'd host — this is where that gets counted |
| `calculator_use` | Cost calculator completed | Cost is purchase driver #2 (2.75); this is the intent signal for it |
| `refill_page_view` | "We fill any system" page | The switcher lane — ~116 of 206 owners bought elsewhere |
| `range_page_view` | What's pouring / range | Taste & freshness is driver #1 (2.19) |
| `membership_view` | Keg Crew page | Members leak at 18% vs 44% — attachment is a churn metric |
| `contact_submit` | Any enquiry form | Catch-all with a source field |
| `directions_click` | Map or directions | Taproom is 22% of acquisition and the venue is hard to find |
| `phone_click` | Tel link on mobile | The oldest conversion in hospitality |

Every event carries the UTM campaign and, where the user is known, a hashed identifier so it can be joined to the CRM record.

## Phase 3 — The join that makes attribution real

Web analytics cannot see a refill. GoTab can't see an ad. The join is the whole game.

| Link | Method | Owner | Interim if blocked |
|---|---|---|---|
| Ad → site | UTM on every destination URL | Jewell | — |
| Site → enquiry | Hidden UTM fields on every form | Jewell | — |
| Enquiry → customer | Mobile number as the key, captured at the counter ("what number do we text when it's ready?") | Raef/Harry | Already works for corny customers |
| Customer → refill | GoTab transaction attached to the record | Raef/Harry | **Manual fortnightly export** until GoTab × Fishbowl lands (date outstanding, open item #4) |
| First-touch source | Asked once at first sale, stored on the record | Bar staff | Counter script |

The counter question is the load-bearing element. Without it, paid media has no denominator and every cost-per-acquisition figure in #68 is an estimate.

## Phase 4 — Baselines frozen before anything launches

Recorded once, dated, filed in #65. These are the numbers the engagement will be judged against and they cannot be reconstructed later.

| Baseline | Value at 20 Aug 2026 | Source |
|---|---|---|
| System owners in database | 206 | Client business records |
| Active customers | 96 or ~113 — **record both, with the definition used** | GoTab export |
| Bought system elsewhere | ~116 of 206 (56%) | Business records. The census's 31% is response-biased and is **not** the baseline |
| Kegs per customer per month | 1.55 weighted mean | Census |
| Acquisition mix | Taproom 22% · Google 20% · Referral 18% · Social 16% · Giveaway 10% | Census |
| Giveaway conversion | 22–25 systems per ~1,000-entry cycle | Client records |
| Keg Crew membership | 67% of respondents | Census |
| Member vs non-member leakage | 18% vs 44% | Census |
| Referral awareness (system) | 43.8% | Census |
| NPS | ≈ +80, 86% promoters | Census |
| Meta spend and results | Whatever the prior agency's account shows | Ad account export (#68 Phase 0) |

## Phase 5 — Reporting cadence

| Frequency | Contents | Owner | Audience |
|---|---|---|---|
| Weekly, 10 minutes | Spend, cost per result, entries, unattached transactions | Jewell | Raef/Harry |
| Monthly, one page | Actives vs target, new actives by source, cost per new active, at-risk saves, winbacks, membership attach | Jewell | Justin, founders |
| Quarterly | 90-day cohort read — the only honest conversion view when 43% of buyers take 3+ months | Jewell | Founders |

The 30-day number is a leading indicator and is labelled as one on every report. Treating it as the verdict would kill campaigns that are working.

## Data protection

Personal data stays in GoTab, Fishbowl and the ESP — not in spreadsheets on personal devices beyond the interim export, which is deleted after each fortnightly cycle. Marketing consent is stored per channel and honoured across all of them. Ad-matching audiences are built from hashed data only.

## Stop conditions

Any campaign launching with an unverified event · any report published without the active-customer definition stated on it · any personal-data export retained past its cycle.

## Dependencies

Website access · domain DNS · GoTab export permissions · ad account access (open item #16) · founder decision on the active definition (open item #11) · integration date (open item #4).

*Feeds into: every runbook in this phase, #76 Optimisation Backlog, #65 Case Study Evidence Pack.*
