# 76 – Optimisation Backlog (v1 seed)
## Tap That Brewery · The queue, before any results exist

| | |
|---|---|
| **Document** | Optimisation Backlog – catalogue #76 |
| **Engagement** | Jewell Projects × Tap That Brewery |
| **Phase** | 03 Deploy |
| **Status** | Draft v01 – Internal · **SEED – populated with real tests once Deploy runs** |
| **Date** | 28 August 2026 |
| **Prepared by** | Jewell Projects |
| **Descends from** | #26 Measurement Plan · the full Deploy set (#66–#75) |

*Pre-CP1/CP2 draft – Deploy runbooks are written ahead of both gates. Nothing here should be executed until the Design plan it descends from is approved.*

---

## What this is

A standing queue of tests, ranked by expected value against effort. It is seeded here from what the census and the client’s own documents already show is broken or unproven – so that the first optimisation cycle starts with a list rather than a blank page. Items are added as Deploy generates evidence and removed when they are resolved either way.

Scoring: **Impact** (1–5, on active customers) × **Confidence** (1–5, in the evidence) ÷ **Effort** (1–5, in Harry/Harry-days). Anything scoring above 3.0 is a candidate for the next sprint (#77).

## Fix first – these are errors, not tests

| # | Item | Why | Owner | Score |
|---|---|---|---|---|
| F1 | **"$2.34 a schooner" ad running live** – the figure is member-only. The non-member figure is itself unsettled (open item #19: $2.98, $3.19 and $2.70 are all in circulation), so the fix is to pull the claim, not to swap the number | Advertising-standards exposure on a claim currently in market | Jewell + Justin | Not scored – immediate |
| F2 | **Keg Crew break-even briefed to staff as 6 kegs; it is 8.33** ($250 ÷ $30) | Staff are making a promise the maths doesn’t keep | Justin | Not scored – immediate |
| F3 | **Two conflicting membership posters in venue** ($250/yr vs $300 + $120 renewal, different token bonuses) | Customers are being quoted two prices in one room | Justin | Not scored – immediate |
| F4 | Product name inconsistency – "Bong Water" vs "Bone Water" IPA | Menu, collateral and web disagree | Harry/Harry | Not scored – immediate |

None of these wait for a sprint.

## Added by the advisory review (28 Aug 2026)

*These entered from #20B and outrank most of what follows. They are not scored on the same scale because two of them are business decisions rather than marketing tests.*

| # | Item | Why it ranks | Owner |
|---|---|---|---|
| A1 | **Buy the system-owner databases** — Harvey Norman, Keg Land / Kegmaster, BenchTop | Every name already owns a system, so the $975 objection is pre-cleared. At ~$70 GP per keg the data pays for itself | Justin + Jewell |
| A2 | **Direct deal with Harvey Norman** — POS QR, referral rebate per keg, or free keg with purchase if liquor rules allow | A conversation, not a campaign. Monk holds point contacts | Justin |
| A3 | **Tour operators** — refresh the write-ups for Hop On, Urban Legends and Pineapple Tours; build Urban Legends a booking widget that always includes Tap That | The operator picks the breweries, so the write-up is the whole game. Ours omits the award | Harry |
| A4 | **Wholesale with structure** — goals, KPIs and a dedicated person or agent | One commercial account is worth ten households | Justin |
| A5 | **Taproom hours and format** — restrict to a tasting and event window rather than a drop-in | The zero-sum call at the centre of the business | Founders |
| A6 | **Cut the range to ~6 core beers plus seasonals** | 27 taps is decision anxiety for the customer and a live cost driver for the business | Founders + Chris |
| A7 | **Lease-to-buy or rental**, framed as a gym membership at $50–100/month | Removes the upfront barrier on a reverse razor-and-blades model | Justin |
| A8 | **A low-alcohol or healthy line** | Lapsed members still own the system and still need to drink something. Reactivates them without asking anyone to drink more | Chris |
| A9 | **Personalised reorder prompts** replacing the 90-day blanket SMS | The 40% who buy less often than quarterly are where the growth is, and a blanket message is tone-deaf to all of them | Jewell |
| A10 | **Simplify loyalty** — every tenth keg free instead of a points system | The points administration is itself a cost driver | Justin |
| A11 | **Profile Chris.** The head brewer is well regarded and invisible | Regulars have never had the tasting notes explained to them | Harry |

**Demoted by the same review:** pulling people into the taproom through social media, which the queue below still treats as core.

## The queue

| # | Test | Evidence it comes from | Impact | Conf | Effort | Score |
|---|---|---|---|---|---|---|
| 1 | **Referral awareness campaign** – lift system-referral awareness from 43.8% toward 70% | Referral is 18% of acquisition; fewer than half the base knows the reward exists | 5 | 5 | 2 | **12.5** |
| 2 | **Membership push to non-members** | Non-member leakage 44% vs member 18% – the single strongest retention correlate available | 5 | 4 | 2 | **10.0** |
| 3 | **Switcher lane at scale** – target the ~116 of 206 owners who bought elsewhere | 56% of the installed base, already switching unprompted | 5 | 4 | 3 | 6.7 |
| 4 | **Bring a Mate demo program** | 63% would host; no program exists | 4 | 5 | 3 | 6.7 |
| 5 | **Move members' tastings to Saturday afternoon** | 73% don’t attend; 73% of would-attenders prefer Saturday afternoon | 3 | 5 | 1 | **15.0** |
| 6 | **Fix venue wayfinding signage** | Taproom is 22% of acquisition and the precinct is industrial with low foot traffic | 4 | 4 | 2 | 8.0 |
| 7 | **Extend retargeting windows from 30 to 90 days** | 43% of buyers take 3+ months; a 30-day window misses most of the market | 4 | 5 | 1 | **20.0** |
| 8 | **Facebook-weighted creative and copy** | 54% name Facebook primary vs Instagram 38%; base skews 41–60 | 3 | 4 | 1 | 12.0 |
| 9 | **Delivery launch to stock-up buyers only** | 79% interest among stock-up vs 40% top-up; fee tolerance $20–30 | 4 | 4 | 4 | 4.0 |
| 10 | **Postcode-weighted geo-targeting** (4213, 4209, 4211, 4218, 4227) | Customers do not live where the brewery is | 3 | 4 | 1 | 12.0 |
| 11 | **Workplace group offer** to the six named groups already buying | Warm, proven, unworked | 3 | 4 | 2 | 6.0 |
| 12 | **Cost messaging in the open feed**, not retargeting-only | Cost ranks #2 (2.75), just behind taste (2.19) – the "dirty little secret" read is not supported | 3 | 4 | 1 | 12.0 |
| 13 | **Giveaway nurture for the ~975 non-winners** | 22–25 conversions per ~1,000 entries; the rest currently get silence | 4 | 3 | 3 | 4.0 |
| 14 | **Weekend-only segment treatment** (35% of base, all ≤1 keg/month) | A volume message to this segment is wasted; a range message may not be | 2 | 3 | 1 | 6.0 |
| 15 | Subscription offer | 41% interest – **but the client’s own analyst recommends against launching it** | 3 | 1 | 4 | 0.75 |

Item 15 sits in the queue deliberately, scored low, so that it is visibly parked rather than quietly forgotten. It is not a next-sprint candidate.

## What the queue does not yet contain

Anything that needs live performance data: creative winners, audience performance, landing-page conversion rates, EDM subject-line tests, cost-per-acquisition comparisons between channels. These are the items that will dominate v2 and they cannot be written before the first campaign runs.

## Working method

| Step | Detail |
|---|---|
| **Cadence** | Reviewed monthly, in the same hour as the #26 report |
| **Sprint size** | Three items maximum per month – one marketer at ~70% capacity |
| **One variable** | Each test changes one thing; two changes make an unreadable result |
| **Run length** | Minimum 30 days for leading indicators, **90 days before any conversion verdict** – the buying cycle forbids shorter |
| **Recording** | Hypothesis, what changed, dates, result, decision. A test with no written hypothesis is not a test |
| **Retirement** | Won, lost or abandoned – all three are recorded. Abandoned items say why |

## Stop conditions

No new test starts while an F-item is unresolved · no test runs on a channel whose tracking (#75) is unverified · no two tests run on the same audience at the same time.

## Dependencies

Tracking (#75) live · founder decisions on the active-customer definition and membership pricing · CP2 sign-off before any Design-derived test.

*Feeds into: #77 Next Sprint Priorities, #65 Case Study Evidence Pack.*
