# 53 – Website Brief
## Build brief for tapthatbrewery.com.au

| | |
|---|---|
| **Document** | Website Brief – catalogue #53 |
| **Engagement** | Jewell Projects × Tap That Brewery |
| **Phase** | 02 Design |
| **Status** | Draft v01 – Internal |
| **Date** | 19 August 2026 |
| **Prepared by** | Jewell Projects |

> **Evidence note (19 Aug 2026).** Figures in this draft predate the client’s census and planning documents. Several have been corrected; some interpretations are still under revision. Read `20A Evidence Reconciliation` before citing anything here.

*Pre-CP1 draft – produced ahead of Discover sign-off; census data, membership pricing reconciliation and competitor verification may revise inputs.*

---

## The job

Rebuild tapthatbrewery.com.au as the digital half of the funnel the venue already runs. Discovery’s finding (#12): the taproom converts 20–30% [unverified – see #20B] of visitors because the proof is on the walls – the web carries almost none of it, and the 3-month buying cycle happens away from the venue. The site’s job is to carry the same proof to people mid-cycle. *(Source plan: website strategy/sitemap document not yet drafted – this brief works from the Discover base and #12's deployment map; reconcile if a sitemap document lands.)*

## Pages

| Page | Must contain |
|---|---|
| **Home** | Trust bar (Brewer’s Choice at Crafted, first year entering; Gold Coast Bulletin press); the two funnels split clearly: "Get a system" / "Already own one? We fill any system" |
| **Keg systems** | 2-tap $975 → 6-tap $2,550 (+ bonus credits $40–100), integrated from $1,750, 5L mini $225, assembly $300; Afterpay/Zip prominently; **demo booking CTA**; objection content (partner veto → 1/3 non-beer taps; "I’ll drink too much" → census: 57% pour daily or most days, yet the weighted average is just **~1.55 kegs a month** – 57% of owners buy one keg or fewer (census)) |
| **We Fill Any System** (switcher) | Tue-drop→Fri-ready corny promise as mechanism; plastic vs corny explainer; first-fill offer [TBC]; refill referral (500 Tap Tokens) |
| **Refills & pricing** | 20L member/non-member three-band pricing; **savings calculator** (kegs/month → $ vs bottle-o and pub; ~$2.70/schooner at home); "why 20L" freshness explainer |
| **Tap list** | All 27 taps, ABVs, non-beer filter ("a third of these aren’t beer") – from the live menu data |
| **Membership** | Keg Crew / Mug Club / Brew Buds – **blocked until price reconciliation (#52 Kit 4)**; Tap Token + leaderboard explainer |
| **Benchy** | Portable tap for 4WD/camping/boating; partner logos as they sign |
| **Taproom & functions** | Hours, happy hour, events, function/keg-hire enquiry form (mezzanine ~40 / venue ~120–130 seated) |
| **Giveaway** | Standing capture page, live only during cycles |
| **About** | Founding story (Chris Smith, Justin Mistry), award, social-responsibility commitments |

## Functionality

1. **Demo booking** – form or calendar; delivers to cheers@tapthatbrewery.com.au and logs to CRM (#58). Fields: name, mobile, email, suburb, segment self-select ("backyard / shed / office / club"), own-a-system Y/N.
2. **Giveaway capture** – same fields; consent checkbox for marketing (SPAM Act, see #57); writes to Fishbowl list.
3. **GoTab links** – takeaway/refill ordering and (when live) Uber Direct delivery deep-linked, not rebuilt.
4. **Afterpay/Zip messaging** on every system price display.
5. Calculator: client-side, no login, sharable result.

## SEO requirements

Per #55: URL structure and on-page targets for the priority clusters ("keg refills gold coast", "beer keg system home", "we fill any system" variants); schema (LocalBusiness, Product, FAQ); GBP linkage. Site must not launch pages that #55 will restructure.

## Analytics

GA4 + Meta Pixel (age-gated audiences per #56). Events: demo_booked, giveaway_entry, calculator_used, gotab_click, membership_click, function_enquiry. UTM discipline documented for Harry.

## Acceptance criteria

1. Every price on the site matches the reconciled price list – zero conflicts (the two-poster failure never reaches the web).
2. Demo booking and giveaway entries arrive in CRM with all fields intact, tested end-to-end.
3. All six #12 differentiators visibly deployed on the mapped pages.
4. Age gate on entry; DrinkWise/responsible-service footer; gluten-*reduced* wording only.
5. Mobile-first passes Core Web Vitals; site editable by Harry without a developer for prices, tap list and events.

## Assumptions & open items

- Current site not yet audited – scope (rebuild vs restructure) confirmed after review. Platform choice [TBC].
- Membership page, first-fill offer, Benchy pricing, lease-to-buy mention all gated on client confirmations.
- Deadline [TBC – must precede #56 paid launch; paid traffic does not land on the current site].

---

*Feeds into: #55 SEO Brief, #56 Paid Media Brief, #57 EDM Brief, #58 CRM Brief, #61 Final Brief Pack.*
