"""Words for Tap That -- The Pivot.

Christy's draft, restyled. Content is hers; the only substantive edits are
listed in CHANGES below so nothing slips through unannounced.
"""

CHANGES = [
    # (slide, what moved, why)
    ("02", "Split six findings into two columns of three",
     "the sixth ran 0.4in off the bottom of the slide in the draft"),
    ("06", "Replaced two EMF flyer artworks with four PNG flyers",
     "the EMFs are vector-only and render blank outside PowerPoint"),
    ("09", "Census sample stated as 49, not ~50",
     "the raw response file has 49 rows, and the sample size is the argument"),
]

TITLE = {
    "brand": "TAP THAT",
    "head": "THE PIVOT",
    "sub": "From vanity to sanity. A strategic evolution, not a rebrand.",
    "foot": "Prepared by Jewell Projects for the founders of Tap That",
}

# ---------------------------------------------------------------- slide 02
SAW_HEARD = {
    "eyebrow": "WHAT WE SAW AND HEARD",
    "head": "The overall plan is sound. Focus and shape is the unlock.",
    "items": [
        ("The strategy is sound, the shape is not",
         ["Insightful, comprehensive, and Justin's mental model that everything "
          "feeds refills is spot on.",
          "But it reads as AI theoretical: too much equivalence, too many "
          "directions, and its own best insights are buried."]),
        ("Two business units cancelling each other out",
         ["Thought to be complementary, in reality pulling opposite ways. A great "
          "refill business takes traffic out of the Tap Room.",
          "Which means more spend to replace it, at a high cost per customer."]),
        ("The weakest unit is getting the support",
         ["Refills are at MVP, and only refills, and only beer.",
          "Marketing's time goes to propping up the unit that does not work, at "
          "the cost of the ones that do. Watering the weeds, not the flowers."]),
        ("The offer is good, but the stars cannot shine",
         ["We suspect a long tail of beer options is driving cost of goods.",
          "And we think it is causing choice paralysis at the point of sale."]),
        ("Chasing two rabbits, catching neither",
         ["For all the right reasons, marketing explores an idea, quits, moves on.",
          "Nothing gets the run it needs to prove itself either way."]),
        ("In danger of dying with a beautiful corpse",
         ["Running a brewery is hard. Hospitality is harder. Both on a skeleton "
          "staff is unreasonable.",
          "Permission is needed to reshape the business."]),
    ],
}

# ---------------------------------------------------------------- slide 03
VANITY = {
    "eyebrow": "THE CORE READ",
    "head": "TAP ROOM IS VANITY.\nREFILLS ARE SANITY.",
    "stats": [
        ("96-113", "Active refill customers, ordering repeatedly. "
                   "That is MVP status, reached without a push."),
        ("56%", "of refill customers bought their tap system somewhere else. "
                "The refill proposition is already validated."),
        ("20%", "of system buyers are said to have visited the Tap Room. "
                "That is correlation, not proven causation."),
    ],
    "foot": "The Tap Room works as an event and function destination. It does not "
            "work as a walk-in, because the footfall is not there. The task now is "
            "to brutally edit the losers and invest in what is proven.",
}

# ---------------------------------------------------------------- slides 04, 05
CORE = {
    "eyebrow": "WHERE TO FROM HERE / CORE",
    "head": "Get the core right, then go for more.",
    "moves": [
        {"n": "1", "title": "Tap Room:\nPause and pivot",
         "line": "Pause walk-in trading. Go all in on destination demand.",
         "proof": "Event and function nights are already profitable",
         "acts": ["PR to tourism, event and wedding planners",
                  "Own the tour circuit: Urban Legends booking tool, "
                  "Pineapple Tours, Crafted award callout",
                  "Ticketed events and collabs",
                  "Party rental, with minimum-guarantee kegs covering the "
                  "rental cost"]},
        {"n": "2", "title": "Convert the owners\nalready sold",
         "line": "Objections are already overcome for existing kegerator owners.",
         "proof": "56% bought their system elsewhere",
         "acts": ["Harvey Norman gift-with-purchase and point-of-sale tie-up, "
                  "plus buyer database",
                  "Buy Kegland and corny-keg owner databases",
                  "Official Benchy partnership and database",
                  "Co-branded outdoor BBQ and system bundle"]},
        {"n": "3", "title": "Remove all friction\nin refills",
         "line": "Every extra step in the refill process costs a sale.",
         "proof": "10% reorder monthly, 40% far later. One clock fails both",
         "acts": ["Free delivery always works, recover margin in dollars, not "
                  "percent",
                  "Replace the blanket 90-day SMS with consumption-triggered "
                  "reminders",
                  "Lead on the simplicity: no CO2, pick up and go",
                  "Simplify membership, refill-centric",
                  "Get Justin off the bar and onto the road"]},
        {"n": "4", "title": "Rationalise\nthe range",
         "line": "Create hero products, cut the non-productive tail.",
         "proof": "About 19 brew choices loses both curation and best-in-class",
         "acts": ["Deeper product marketing on the brews that remain",
                  "Introduce social proof cues, such as most popular",
                  "Free the shelf space and the brewing time for the heroes"]},
        {"n": "5", "title": "Ride the\nwellness wave",
         "line": "Also the way back to lapsed customers.",
         "proof": "40% of lapsed customers cite cutting back",
         "acts": ["Low, non-alcoholic, low-carb and protein range",
                  "Wellness influencer collabs, amplify or co-develop",
                  "Reframe for the cutting-back cohort as a healthier "
                  "alternative, not less beer"]},
    ],
}

MORE = {
    "eyebrow": "WHERE TO FROM HERE / MORE",
    "head": "Once the core is running, extend it.",
    "moves": [
        {"n": "6", "title": "Full press\non wholesale",
         "line": "Resourced, structured and measured. No more falling through "
                 "the cracks.",
         "proof": "One wholesale account is worth about ten households",
         "acts": ["Hire a full-timer or an agent",
                  "Set targets and KPIs",
                  "Custom systems for sporting clubs, minimum-guarantee kegs "
                  "per season",
                  "Move rigs from footy to cricket for year-round occupancy"]},
        {"n": "7", "title": "Design\nfor her",
         "line": "Covered is not the same as catered for.",
         "proof": "The passion for brews is real, the range does not reflect it",
         "acts": ["Romance the RTD properly",
                  "Build the hydration story through the wellness and light range",
                  "Products she is proud to serve",
                  "Systems designed to sit in eyesight at home"]},
        {"n": "8", "title": "Hyper-personalise\ncomms and LTV",
         "line": "This needs a process, not a message.",
         "proof": "Buying cycle: about 60% within three months, 40% longer",
         "acts": ["Track consumption to predict the next refill",
                  "Re-engage lapsed customers by actual reason: cutting back "
                  "versus forgot",
                  "Trigger-based outreach, not calendar-based",
                  "Personal details: anniversaries, footy finals"]},
        {"n": "9", "title": "Make the kegerator\nworth writing about",
         "line": "Turn the system itself into desire.",
         "proof": "1,000 giveaway entries is proven demand",
         "acts": ["User-generated content mechanic: tag Tap That, get a discount",
                  "Own your keg personalisation, like a whisky bottle",
                  "Explore short-term and occasion rental for parties"]},
        {"n": "10", "title": "Package around\nthe duopoly",
         "line": "Locked-in venues still have real pain points.",
         "proof": "Contractual lock-in is not the same as satisfaction",
         "acts": ["A packaged offer that works around existing contracts",
                  "Find the judo move that uses their size against them: no "
                  "lock-in, profit share, white labelling"]},
    ],
}

# ---------------------------------------------------------------- slide 06
FLYERS_SLIDE = {
    "eyebrow": "EVENT EXAMPLES",
    "head": "The destination business, sold the way the venue already sells it.",
    "note": "Format taken from Tap That's own in-venue flyer. Photography is the "
            "August site visit, not stock. Print-ready A4 at 200 dpi.",
    "captions": ["Weddings", "Bucks and hens", "Work functions",
                 "Tours and tastings"],
}

# ---------------------------------------------------------------- slide 07
WEDDING = {
    "eyebrow": "B2C FLYWHEEL / THE SIGNATURE WEDDING BREW",
    "head": "Turning hens and bucks days into wedding day volume.",
    "steps": [
        ("1", "The Tap Room event",
         "Private hens or bucks session. Guided flight tasting across 27 taps "
         "with interactive ingredient blending."),
        ("2", "Bespoke branding",
         "Co-branded custom label, naming, and beverage style selection: beer, "
         "sour, seltzer or RTD spirit."),
        ("3", "Wedding day reception",
         "Bulk supply delivered in 20L kegs or custom cans for the main event."),
        ("4", "Take-home flywheel",
         "Every wedding guest goes home with a branded sample and a QR code."),
    ],
    "impact": [
        ("High-margin function revenue",
         "Captures premium venue hire and group tasting packages upfront."),
        ("Guaranteed bulk volume",
         "Secures pre-sold beverage volume for the reception."),
        ("Organic customer acquisition",
         "Converts guests into hardware and subscription leads."),
    ],
    "strap": "THE ECOSYSTEM EFFECT   Every wedding is a live, self-funding brand "
             "activation that puts Tap That product into the hands of 100 or more "
             "targeted consumers.",
}

# ---------------------------------------------------------------- slide 08
CONCEPTS = {
    "eyebrow": "PARTNERSHIP CONCEPTS",
    "head": "What a co-branded system could look like.",
    "note": "Concept renders for discussion. No approach has been made to any "
            "brand shown, and none of these marks are licensed.",
    "images": [
        ("dewalt-collab.png", "Trade and worksite"),
        ("raptor-collab.png", "Four-wheel drive and touring"),
        ("harley-collab.png", "Motorcycle clubs"),
        ("tap-truck.png", "Mobile bar for events"),
    ],
}

# ---------------------------------------------------------------- slide 09
NOTES = {
    "eyebrow": "OTHER STRATEGIC NOTES",
    "head": "Two things to hold on to.",
    "cards": [
        ("Who is the real enemy?",
         "Overpriced pubs. Not the duopoly, not A&A, not the keg-delivery "
         "operators. Speak in unit economics everywhere, and do not get pulled "
         "into a keg price war you do not need to fight."),
        ("Handle the census with care",
         "49 people, forced-choice answers. People do not always know, or say, "
         "why they buy. Status, wanting to be seen as successful, compensating "
         "for something else: real drivers, rarely spoken. Useful colour. Not a "
         "strategy map."),
    ],
}

# ---------------------------------------------------------------- slide 10
HOUSEKEEPING = {
    "eyebrow": "HOUSEKEEPING / WEBSITE AND BRAND",
    "head": "Small fixes, disproportionate impact.",
    "rows": [
        ("Above the fold",
         "No hook, background film cut too fast to read, copy pollution, "
         "low-resolution static logo."),
        ("Missing proof",
         "The Crafted Brewers' Choice award, the fits-any-system callout and "
         "strong reviews are all buried below the fold."),
        ("Hierarchy",
         "Four business units treated equally. Prioritise the moments that "
         "matter: family, friends, the proud provider role."),
        ("Category",
         "Commercial brewer invites mainstream price and product comparisons. "
         "It needs an elevated category name of its own."),
        ("Channel language",
         "Wholesale should speak directly to restaurants and sporting clubs: "
         "cuisine matching, club-branded kegs, straight to the margin story."),
    ],
}

# ---------------------------------------------------------------- slide 11
HELP = {
    "eyebrow": "WHERE JEWELL PROJECTS CAN HELP",
    "head": "What we can pick up from here.",
    "cols": [
        ("FROM THE BRIEF", [
            "Website design optimisation",
            "SEO and GEO best-practice implementation",
            "PR outreach to tourism operators and experiential platforms",
            "Influencer outreach",
            "Partnerships outreach and project management: BBQ brands, "
            "system collabs",
            "Urban Legends collaborative booking tool",
        ]),
        ("ALSO WORTH ADDING", [
            "Trigger-based CRM and lifecycle build, which fixes the 90-day "
            "SMS problem",
            "Membership programme redesign",
            "Wholesale structure and KPI framework",
            "Event flyer and campaign artwork, in the format shown",
        ]),
    ],
}
